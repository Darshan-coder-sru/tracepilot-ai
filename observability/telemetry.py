import logging
import os

from dotenv import load_dotenv

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Load variables from .env
load_dotenv()

# Create application information
resource = Resource.create({"service.name": "tracepilot-ai"})

# Get SigNoz configuration
signoz_endpoint = os.getenv("SIGNOZ_ENDPOINT")
signoz_key = os.getenv("SIGNOZ_INGESTION_KEY")
_otlp_headers = {"signoz-access-token": signoz_key}


# ---------------------------------------------------------------------------
# Traces
# ---------------------------------------------------------------------------

trace_provider = TracerProvider(resource=resource)

otlp_span_exporter = OTLPSpanExporter(
    endpoint=f"{signoz_endpoint}/v1/traces",
    headers=_otlp_headers,
)

trace_provider.add_span_processor(BatchSpanProcessor(otlp_span_exporter))
trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer("tracepilot-ai")


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

otlp_metric_exporter = OTLPMetricExporter(
    endpoint=f"{signoz_endpoint}/v1/metrics",
    headers=_otlp_headers,
)

metric_reader = PeriodicExportingMetricReader(
    otlp_metric_exporter,
    export_interval_millis=10000,
)

meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter("tracepilot-ai")

# Reusable instruments. Import these into agent/pipeline code and call
# .add() / .record() at the relevant points (see docstrings below).
run_counter = meter.create_counter(
    name="tracepilot.agent.runs",
    unit="1",
    description="Number of agent runs started",
)

error_counter = meter.create_counter(
    name="tracepilot.agent.errors",
    unit="1",
    description="Number of agent runs that ended in an error",
)

latency_histogram = meter.create_histogram(
    name="tracepilot.agent.latency",
    unit="s",
    description="End-to-end agent run latency",
)

token_counter = meter.create_counter(
    name="tracepilot.agent.tokens",
    unit="1",
    description="Total tokens consumed across agent runs",
)

cost_counter = meter.create_counter(
    name="tracepilot.agent.cost_usd",
    unit="USD",
    description="Estimated cumulative cost of agent runs",
)


# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------

otlp_log_exporter = OTLPLogExporter(
    endpoint=f"{signoz_endpoint}/v1/logs",
    headers=_otlp_headers,
)

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))
set_logger_provider(logger_provider)

# Standard library logging handler that ships records to SigNoz and
# auto-attaches the active trace_id/span_id, so a log line emitted inside
# a span can be pivoted back to that trace in the SigNoz UI.
_otel_log_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

logger = logging.getLogger("tracepilot-ai")
logger.setLevel(logging.INFO)
if not any(isinstance(h, LoggingHandler) for h in logger.handlers):
    logger.addHandler(_otel_log_handler)

# Also mirror to stdout so `streamlit run` logs stay readable locally.
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    _console_handler = logging.StreamHandler()
    _console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(_console_handler)


def shutdown_telemetry():
    """Flush and close all exporters. Call on app/process shutdown so the
    final batch of spans, metrics, and logs isn't lost."""
    trace_provider.shutdown()
    meter_provider.shutdown()
    logger_provider.shutdown()