import os
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


# Load variables from .env
load_dotenv()

# Create application information
resource = Resource.create({
    "service.name": "agentwatch-ai"
})

# Create tracer provider
trace_provider = TracerProvider(resource=resource)

# Get SigNoz configuration
signoz_endpoint = os.getenv("SIGNOZ_ENDPOINT")
signoz_key = os.getenv("SIGNOZ_INGESTION_KEY")

# Configure the exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=f"{signoz_endpoint}/v1/traces",
    headers={
        "signoz-access-token": signoz_key
    }
)

# Send traces to SigNoz
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# Set the global tracer provider
trace.set_tracer_provider(trace_provider)

# Create tracer
tracer = trace.get_tracer("agentwatch-ai")