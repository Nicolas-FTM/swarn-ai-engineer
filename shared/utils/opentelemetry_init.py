from shared.config import settings
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def init_telemetry(service_name: str):
    # Common Resource
    resource = Resource(attributes={
        "service.name": service_name,
        "service.version": "0.1.0",
        "deployment.environment": settings.environment
    })

    # ----- Traces -----
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=settings.otel_exporter_otlp_endpoint,
        insecure=True
    )
    trace_provider.add_span_processor(
        BatchSpanProcessor(otlp_trace_exporter)
    )
    trace.set_tracer_provider(trace_provider)

    # Instrument FASTAPI (it will be called from main.py)
    return trace_provider, resource
