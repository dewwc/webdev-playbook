# Python (FastAPI / Django / Flask)

Use the stdlib `logging` module as the base so library logs go through the same pipeline. Add `structlog` (or `python-json-logger`) for JSON output. If the project already has one of these, keep it.

## Setup (structlog)

```python
import logging, structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,      # per-request fields (trace_id)
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.dict_tracebacks,         # exception -> structured stack
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)
log = structlog.get_logger(service_name="ev-api")

log.warning("ocpp call slow", charger_id=charger_id, duration_ms=ms)  # fields, not f-strings
```

Route stdlib logs (uvicorn, Django, SQLAlchemy) through the same JSON format with `structlog.stdlib.ProcessorFormatter`, or at least set them to JSON with `python-json-logger`.

## Trace ID and request log (FastAPI example)

```python
@app.middleware("http")
async def request_log(request, call_next):
    trace_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    structlog.contextvars.bind_contextvars(trace_id=trace_id)
    start = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        structlog.contextvars.unbind_contextvars("trace_id")
    route = getattr(request.scope.get("route"), "path", request.url.path)  # template, e.g. /chargers/{id}
    log.info("request", method=request.method, route=route, status=response.status_code,
             duration_ms=round((time.perf_counter() - start) * 1000), trace_id=trace_id)
    response.headers["X-Request-Id"] = trace_id
    return response
```

With OpenTelemetry (`opentelemetry-instrumentation-fastapi` / `-django` / `-flask` plus `opentelemetry-instrumentation-logging`), the trace ID comes from W3C `traceparent` and is injected into log records. Prefer that when OTel is in use.

## Global exception handler

- FastAPI: `@app.exception_handler(Exception)` → `log.exception("unhandled error")` once, return a problem+json `JSONResponse` with status 500 and `traceId`.
- Django: logging config for `django.request` plus `DEBUG = False` in production. Custom `handler500` returns a body without traceback.
- Flask: `@app.errorhandler(Exception)`.

`log.exception(...)` (or `exc_info=True`) inside `except` records the stack. Never use a bare `except: pass`.

## Jobs

Celery / RQ / APScheduler: log task start/end/failure once per run with task name and duration. Celery's `task_failure` signal is a single place to log failures.
