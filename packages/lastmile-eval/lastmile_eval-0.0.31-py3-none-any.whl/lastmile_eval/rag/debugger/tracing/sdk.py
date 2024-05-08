"""
File to describe the APIs and SDKs that users can use in code, see example
folder for example on how it can be implemented
"""

import json
from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional, Sequence
from urllib.parse import urlencode

import requests
from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace.span import INVALID_SPAN, Span
from opentelemetry.util import types
from requests import Response
from requests.adapters import HTTPAdapter, Retry

from lastmile_eval.rag.debugger.api import (
    LastMileTracer,
    RAGIngestionEvent,
    RAGQueryEvent,
    RAGTraceEventResult,
)

from ..common.core import IndexingTraceID
from ..common.utils import SHOW_DEBUG, get_lastmile_api_token
from .exporter import LastMileOTLPSpanExporter
from .trace_data_singleton import TraceDataSingleton

SHOW_RAG_TRACE_IDS = False


class _LastMileTracerProvider(TracerProvider):
    """
    Subclass of TracerProvider that defines the connection between LastMile
    Jaeger collector endpoint to the _LastMileTracer
    """

    def __init__(
        self,
        lastmile_api_token: str,
        output_filepath: Optional[str] = None,
    ):
        super().__init__()

        # If output_filepath is defined, then save trace data to that file
        # instead of forwarding to an OpenTelemetry collector. This is useful
        # for debugging and demo purposes but not recommended for production.
        if output_filepath is not None:
            output_destination = open(output_filepath, "w", encoding="utf-8")
            exporter = ConsoleSpanExporter(out=output_destination)
        else:
            exporter = LastMileOTLPSpanExporter(
                log_rag_query_func=lambda: _log_all_trace_events_and_reset_trace_state(
                    lastmile_api_token
                ),
                endpoint="https://lastmileai.dev/api/trace/create",
                headers={
                    "authorization": f"Bearer {lastmile_api_token}",
                    "Content-Type": "application/json",
                },
                # TODO: Add timeout argument and have default here
            )

        # We need to use SimpleSpanProcessor instead of BatchSpanProcessor
        # because BatchSpanProcessor does not call the exporter.export()
        # method until it is finished batching, but we need to call it at the
        # end of each span to reset the trace-level data otherwise we can
        # error.

        # The future workaround is to make all the trace-level data checks and
        # trace-data resetting occur OUTSIDE of the exporter.export() method,
        # and simply do those. Then we can have a state-level manager dict
        # where we keep track of traceId, and the state corresponding to that
        # so that when we call the callback log_rag_query_func(), it will take
        # in a trace_id arg to know which trace data to log
        span_processor = SimpleSpanProcessor(exporter)
        self.add_span_processor(span_processor)


class _LastMileTracer(
    LastMileTracer,
):
    """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer`"""

    def __init__(
        self,
        lastmile_api_token: str,
        tracer_implementor: trace_api.Tracer,
        tracer_name: str,
        # TODO: Don't make params Any type
        # Global params are the parameters that are saved with every trace
        global_params: Optional[dict[str, Any]],
    ):
        self.lastmile_api_token = lastmile_api_token
        TraceDataSingleton(global_params=global_params)
        self.tracer_implementor: trace_api.Tracer = tracer_implementor

        self.project_name = tracer_name
        self.project_id = None
        self.set_project()

    @contextmanager
    # pylint: disable=too-many-arguments
    def start_as_current_span(
        self,
        name: str,
        context: Optional[context_api.Context] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Iterator[Span]:
        with self.tracer_implementor.start_as_current_span(
            name,
            context,
            kind,
            attributes,
            links,
            start_time,
            record_exception,
            set_status_on_exception,
            end_on_exit,
        ) as span:
            _set_trace_if_needed(span=span)
            yield span

    # pylint: disable=too-many-arguments
    def start_span(
        self,
        name: str,
        context: Optional[context_api.Context] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Sequence[trace_api.Link] = (),
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
    ) -> Span:
        span = self.tracer_implementor.start_span(
            name,
            context,
            kind,
            attributes,
            links,
            start_time,
            record_exception,
            set_status_on_exception,
        )
        _set_trace_if_needed(span=span)
        return span

    def mark_rag_ingestion_trace_event(
        self,
        event: RAGIngestionEvent,
        span: Optional[Span] = None,
    ) -> RAGTraceEventResult:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.mark_rag_ingestion_trace_event()`"""
        current_span: Span = span or trace_api.get_current_span()
        if current_span == INVALID_SPAN:
            return RAGTraceEventResult(
                is_success=False,
                message=f"No span to log RAGIngestionEvent: {event}",
            )

        # Store event so we can log it to RagIngestionTrace table after the trace
        # has ended
        trace_data_singleton = TraceDataSingleton()
        trace_data_singleton.add_rag_ingestion_event(event)

        # TODO: Add event to current span once we have defined ingestion events

        return RAGTraceEventResult(
            is_success=True,
            message=f"Logged RAGIngestionEvent {event} to span id '{_convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
        )

    def mark_rag_query_trace_event(
        self,
        event: RAGQueryEvent,
        indexing_trace_id: Optional[str] = None,
        span: Optional[Span] = None,
    ) -> RAGTraceEventResult:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.mark_rag_query_trace_event()`"""
        if indexing_trace_id is not None:
            indexing_trace_id = IndexingTraceID(indexing_trace_id)

        current_span: Span = span or trace_api.get_current_span()
        if current_span == INVALID_SPAN:
            return RAGTraceEventResult(
                is_success=False,
                message=f"No span to log RAGQueryEvent: {event}",
            )

        # Store event so we can log it to RagQueryTrace table after the trace
        # has ended
        trace_data_singleton = TraceDataSingleton()
        trace_data_singleton.add_rag_query_event(event)

        # Add event to current span
        current_span.add_event(
            type(event).__name__,
            attributes={
                "rag_query_event": event.model_dump_json(),
                # types.AttributeValue does not contain None so have to cast to str
                # "test_set_id": str(test_set_id),
                "indexing_trace_id": str(
                    indexing_trace_id  # TODO: Use hex value of TraceID
                ),
            },
        )

        return RAGTraceEventResult(
            is_success=True,
            message=f"Logged RAGQueryEvent {event} to span id '{_convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
        )

    def add_rag_event(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Optional[dict[Any, Any]] = None,
        output: Optional[dict[Any, Any]] = None,
        event_data: Optional[dict[Any, Any]] = None,
    ) -> None:
        """
        Add RagEvent to the trace-level data. Duplicate from
        add_rag_query_event for now just to get unblocked
        """
        if input is not None and output is None:
            raise ValueError(
                "If you pass in input, you must also define an output value for this event"
            )
        if input is None and output is not None:
            raise ValueError(
                "If you pass in output, you must also define an input value for this event"
            )

        if input is None and output is None:
            if event_data is None:
                raise ValueError(
                    "If input and output are not set, you must pass in event_data"
                )

        trace_data_singleton = TraceDataSingleton()
        try:
            # Check if args are JSON serializable, otherwise won't be able to
            # export trace data in the collector
            json.dumps(event_data)
            json.dumps(input)
            json.dumps(output)
        except TypeError as e:
            raise TypeError(
                f"Error adding rag event to trace {trace_data_singleton.trace_id}"
            ) from e

        current_span: Span = span or trace_api.get_current_span()
        if current_span != INVALID_SPAN:
            # Wrap try-catch to catch objects that aren't json serializable
            try:
                event_payload = {
                    "event_name": event_name,
                    "span_id": _convert_int_id_to_hex_str(
                        current_span.get_span_context().span_id
                    ),
                    "input": input or {},
                    "output": output or {},
                    "event_data": event_data or {},
                }
                trace_data_singleton = TraceDataSingleton()
                trace_data_singleton.add_rag_event(event_payload)
            except Exception as e:
                if SHOW_DEBUG:
                    print(f"Error adding rag event: {e}")

    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ):
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.register_param()`"""

        trace_data_singleton = TraceDataSingleton()
        try:
            # Check if value is JSON serializable, otherwise won't be able to
            # export trace data in the collector
            json.dumps(value)
        except TypeError as e:
            raise TypeError(
                f"Error registering parameter to trace {trace_data_singleton.trace_id}"
            ) from e

        trace_data_singleton.register_param(key, value)

        # Log this also in the current span to help with debugging if needed
        if should_also_save_in_span:
            current_span: Span = span or trace_api.get_current_span()
            if current_span != INVALID_SPAN:
                if isinstance(value, (dict, Dict)):
                    value = json.dumps(value)
                current_span.set_attribute(
                    key,
                    value,
                )

    # TODO: Don't make params Any type
    def get_params(self) -> dict[str, Any]:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.get_params()`"""
        trace_data_singleton = TraceDataSingleton()
        return trace_data_singleton.get_params()

    def log_feedback(
        self,
        # TODO: Yo what up my dawg, do a helper get_trace to pass this is better duuuuuude
        feedback: str | dict[str, Any],
        trace_id: Optional[str] = None,
        # TODO: Create macro for default timeout value
        timeout: int = 60,
    ) -> None:
        """
        Feedback is a string and optionally a free-form JSON serializable object that can be
        """
        lastmile_endpoint = (
            "https://lastmileai.dev/api/evaluation/feedback/create"
        )
        payload = {
            "feedback": {"text": feedback},
            "projectId": self.project_id,
        }
        if trace_id is not None:
            payload["traceId"] = trace_id

        response: Response = requests.post(
            lastmile_endpoint,
            headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
            json=payload,
            timeout=timeout,
        )
        # TODO: Handle response errors
        return response.json()

    def set_project(self) -> None:
        """
        Gets the project or creates a new one if it doesn't exist.
        TODO: allow user to specify project visibility to allow personal project in an org
        """

        list_project_endpoint = f"https://lastmileai.dev/api/evaluation_projects/list?{urlencode({'name': self.project_name})}"
        response = requests.get(
            list_project_endpoint,
            headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
            timeout=60,
        )
        evaluation_projects = response.json()["evaluationProjects"]
        project_exists = len(evaluation_projects) > 0

        if not project_exists:
            # TODO: Make wrapper function to handle retries automatically
            # in all our request calls
            create_project_endpoint = (
                "https://lastmileai.dev/api/evaluation_projects/create"
            )
            request_session = requests.Session()
            retries = Retry(
                total=3,
                backoff_factor=1,  # 0s, 2s, 4s, 8s, 16s
                # status_forcelist=[ 502, 503, 504 ]
            )
            request_session.mount("https://", HTTPAdapter(max_retries=retries))
            response = request_session.post(
                create_project_endpoint,
                headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
                json={
                    "name": self.project_name,
                },
                timeout=60,  # TODO: Remove hardcoding
            )
            self.project_id = response.json()["id"]
        else:
            self.project_id = evaluation_projects[0]["id"]


def get_lastmile_tracer(
    tracer_name: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Don't make params Any type
    initial_params: Optional[dict[str, Any]] = None,
    output_filepath: Optional[str] = None,
    # TODO: Better typing later
) -> Any:
    """
    Return a tracer object that uses the OpenTelemetry SDK to instrument
    tracing in your code as well as other functionality such as logging
    the RAGQueryEvent data and registered parameters.

    See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer for available
    APIs and more details

    @param tracer_name Optional(str): The name of the tracer to be used
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens
    @param initial_params Optional(dict[str, Any]): The K-V pairs to be
        registered and saved with ALL traces created using the returned tracer
        object. Defaults to None (empty dict).
    @param output_filepath Optional(str): By default, trace data is exported to
        an OpenTelemetry collector and saved into a hosted backend storage such
        as ElasticSearch. However if an output_filepath is defined,
        then the trace data is saved to that file instead. This is useful for
        debugging and demo purposes, but not recommened for production use.

    @return LastMileTracer: The tracer object to log OpenTelemetry data.
    """
    token = get_lastmile_api_token(lastmile_api_token)
    provider = _LastMileTracerProvider(token, output_filepath)
    trace_api.set_tracer_provider(provider)
    tracer_implementor: trace_api.Tracer = trace_api.get_tracer(tracer_name)
    return _LastMileTracer(
        token,
        tracer_implementor,
        tracer_name,
        initial_params,
    )


def get_trace_data(
    trace_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the raw trace and span data from the trace_id

    @param trace_id (str): The trace_id to get the trace data from. This is
        often the hexadecmial string representation of the trace_id int from
        the OpenTelemetry SDK.
        Ex: int_id = 123456789 -> hex value = 0x75BCD15 --> str = "75BCD15"
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The trace data from the trace_id
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/trace/read?id={trace_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


def list_ingestion_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of ingestion trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the ingestion trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_ingestion_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


def get_latest_ingestion_trace_id(
    lastmile_api_token: Optional[str] = None,
) -> str:
    """
    Convenience function to get the latest ingestion trace id.
    You can pass in this ID into the `mark_rag_query_trace_event` method to
    link a query trace with an ingestion trace

    @param lastmile_api_token Optional(str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return str: The trace id corresponding to ingestion trace data
    """
    ingestion_traces: dict[str, Any] = list_ingestion_trace_events(
        take=1, lastmile_api_token=lastmile_api_token
    )
    # TODO: Handle errors
    ingestion_trace_id: str = ingestion_traces["ingestionTraces"][0]["traceId"]
    return ingestion_trace_id


def get_query_trace_event(
    query_trace_event_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the query trace event from the query_trace_event_id

    @param query_trace_event_id (str): The ID for the table row under which
        this RAG query trace event is stored
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/read?id={query_trace_event_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


def list_query_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of query trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


## Helper functions
def _set_trace_if_needed(
    span: Optional[Span] = None,
):
    """
    Helper function to set the trace_id if it hasn't
    already been initialized. This should only happen when we first start a
    new trace (create new span without a parent span attached to it)
    """
    trace_data_singleton = TraceDataSingleton()
    if SHOW_DEBUG:
        trace_id_before = trace_data_singleton.trace_id
        print(f"{trace_id_before=}")

    if trace_data_singleton.trace_id is None:
        # We need to pass in a span object directly sometimes because if
        # tracer.start_span() is run as the root span without context manager
        # (with statement or annotation), it will create a new span
        # and get_current_span is not linked to the get_current_span().
        # current_span WON'T have the id of the span created by start_span
        current_span: Span = span or trace_api.get_current_span()
        trace_data_singleton.trace_id = _convert_int_id_to_hex_str(
            current_span.get_span_context().trace_id
        )

    if SHOW_DEBUG:
        trace_id_after = trace_data_singleton.trace_id
        print(f"{trace_id_after=}")


def _convert_int_id_to_hex_str(int_id: int) -> str:
    """
    Helper function to convert an integer id to a hex string. This is
    needed because Jaeger does trace and span queries using hex strings
    instead of integer values.

    Ex: int_id = 123456789 -> hex value = 0x75BCD15 --> str = "75BCD15"

    @param int_id (int): The integer id to convert to a hex string

    @return str: The hex string representation of the integer id
    """
    return str(hex(int_id)).split("x")[1]


def _log_structured_rag_trace_events(
    lastmile_api_token: str,
    # TODO: Allow user to specify the type of rag trace (Ingestion vs. Query)
) -> Response:
    """
    Log the trace-level data to the relevant rag traces table (ingestion or
    query). This is for the structured RAG events
    """
    # TODO: Add error handling for response
    trace_data_singleton = TraceDataSingleton()
    response = trace_data_singleton.log_to_rag_traces_table(lastmile_api_token)
    if SHOW_DEBUG:
        print("Results from rag traces create endpoint:")
        print(response.json())
    return response


def _log_individual_rag_events(
    lastmile_api_token: str,
) -> None:
    """
    Log the trace-level data to the relevant rag traces table (ingestion or
    query). This is for the unstructured individual RAG events
    """
    # TODO: Add error handling for response
    trace_data_singleton = TraceDataSingleton()
    trace_data_singleton.log_unstructured_rag_events(lastmile_api_token)
    # TODO: move within internal function
    # if SHOW_DEBUG:
    #     print("Results from rag events create endpoint:")
    #     print(response.json())
    return None


def _log_all_trace_events_and_reset_trace_state(
    lastmile_api_token: str,
    # TODO: Allow user to specify the type of rag trace (Ingestion vs. Query)
) -> None:
    """
    Log the trace-level data to the relevant rag traces table. This logs both
    the structured RAG events and the unstructured ones in two separate.
    It then resets the trace-level state
    """

    # TODO: Remove _log_rag_trace_events_and_reset_trace_state call once we
    # verify that logging individual response is good enough
    _log_structured_rag_trace_events(lastmile_api_token)
    _log_individual_rag_events(lastmile_api_token)

    # Reset current trace data so we can start a
    # new trace in a fresh state
    trace_data_singleton = TraceDataSingleton()
    trace_data_singleton.reset()
    return
