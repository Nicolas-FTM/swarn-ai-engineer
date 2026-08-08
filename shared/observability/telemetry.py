"""
telemetry.py

OpenTelemetry initialization shared across backend and rag_service.

This module provides functions for:
- Configuring a TracerProvider with an OTLP exporter (Tempo)
- Returning the resource/provider for further instrumentation in main.py
- Generic OpenTelemetry span decorator for internal function instrumentation
  (Wrapping any callable with an OTel span, named after the function)

Example:
    trace_provider, resource = init_telemetry(service_name="rag_service")

    @traced_span()
    def chunk_documents(documents: list[Document]) -> list[Document]:
"""

# ============================================================================
# Packages
# ============================================================================
# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Project imports
from shared.config.settings import settings

# System
import functools
from typing import Callable, Any

# ============================================================================
# Constants
# ============================================================================
SERVICE_VERSION = "0.1.0"

# ============================================================================
# Services
# ============================================================================
def get_current_otel_trace_id() -> str:
    """Return the current OpenTelemetry trace_id, formatted as a 32-char hex string.

    Returns:
        The current span's trace_id in hex format, or an empty string if
        there is no active span.
    """
    span = trace.get_current_span()
    span_context = span.get_span_context()

    if span_context.trace_id == 0:
        return ""

    return format(span_context.trace_id, "032x")


def init_telemetry(service_name: str) -> tuple[TracerProvider, Resource]:
    """Initialize and register a global OpenTelemetry TracerProvider.

    This must be called once at startup by each service (backend,
    rag_service), before instrumenting FastAPI in main.py.

    Args:
        service_name: Name identifying the service in Tempo (e.g. "backend").

    Returns:
        A tuple of (trace_provider, resource), in case the caller needs to
        reuse the resource for additional instrumentation (e.g. metrics).
    """
    # Common resource attributes, shared by every span emitted by this service
    resource = Resource(attributes={
        "service.name": service_name,
        "service.version": SERVICE_VERSION,
        "deployment.environment": settings.environment,
    })

    # Build the trace provider and wire it to the OTLP exporter (Tempo)
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=settings.otel_exporter_otlp_endpoint,
        insecure=settings.otel_exporter_otlp_insecure,
    )
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))

    # Register globally so trace.get_tracer(__name__) works anywhere in the service
    trace.set_tracer_provider(trace_provider)

    return trace_provider, resource

def traced_span(name: str | None = None) -> Callable:
    """Build a decorator that wraps a function call in an OTel span.

    Args:
        name: Optional span name. Defaults to the function's qualified name.

    Returns:
        A decorator that wraps the target function with span creation.
    """
    def decorator(func: Callable) -> Callable:
        span_name = name or func.__qualname__
        tracer = trace.get_tracer(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with tracer.start_as_current_span(span_name):
                return func(*args, **kwargs)

        return wrapper
    return decorator
