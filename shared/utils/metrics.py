# from prometheus_client import Counter, Histogram, Gauge
# import time
# from starlette.middleware.base import BaseHTTPMiddleware

# REQUEST_COUNT = Counter(
#     "http_requests_total",
#     "Total HTTP requests",
#     ["method", "endpoint", "http_status"]
# )

# REQUEST_LATENCY = Histogram(
#     "http_request_duration_seconds",
#     "HTTP request latency",
#     ["method", "endpoint"]
# )

# TOKEN_USAGE = Counter(
#     "llm_token_usage_total",
#     "Tokens used by LLM calls",
#     ["model", "type"]  # type: prompt/completion
# )

# def record_request(method: str, endpoint: str, status_code: int, duration: float):
#     REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
#     REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

# def record_token_usage(model: str, prompt_toks: int, completion_toks: int):
#     TOKEN_USAGE.labels(model=model, type="prompt").inc(prompt_toks)
#     TOKEN_USAGE.labels(model=model, type="completion").inc(completion_toks)

# class PrometheusMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         start = time.time()
#         response = await call_next(request)
#         duration = time.time() - start
#         record_request(
#             method=request.method,
#             endpoint=request.url.path,
#             status_code=response.status_code,
#             duration=duration,
#         )
#         return response


from prometheus_client import make_asgi_app
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

def init_metrics(resource):
    """
    Sets up OTel MeterProvider with a Prometheus exporter.
    Must be called BEFORE FastAPIInstrumentor.instrument_app(app).
    """
    reader = PrometheusMetricReader()
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
    return provider

def get_metrics_app():
    """ASGI app to mount at /metrics for Prometheus scraping."""
    return make_asgi_app()