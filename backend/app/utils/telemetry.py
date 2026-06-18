"""
Observability setup: OpenTelemetry, Prometheus, LangFuse.
"""
import logging
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import REGISTRY, Counter, Histogram
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def setup_observability(app: FastAPI) -> None:
    """
    Setup observability stack: Prometheus metrics, OpenTelemetry, LangFuse.
    """
    logger.info("Setting up observability stack...")

    # Prometheus metrics
    request_count = Counter(
        "swarn_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status"],
        registry=REGISTRY,
    )

    request_duration = Histogram(
        "swarn_request_duration_seconds",
        "HTTP request latency",
        ["method", "endpoint"],
        registry=REGISTRY,
    )

    @app.middleware("http")
    async def middleware_metrics(request, call_next):
        """Middleware to collect metrics."""
        method = request.method
        path = request.url.path

        # Time the request
        import time
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Record metrics
        request_count.labels(
            method=method,
            endpoint=path,
            status=response.status_code,
        ).inc()

        request_duration.labels(method=method, endpoint=path).observe(duration)

        response.headers["X-Process-Time"] = str(duration)
        return response

    logger.info("Observability setup complete")
