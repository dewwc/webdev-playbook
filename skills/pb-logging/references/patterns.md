# Logging patterns

Field names follow OpenTelemetry semantic conventions so logs work with any backend (Loki, Elastic, Seq, Cloud Logging, Datadog, Sentry).

## 1. Log shape

One JSON object per line, written to **stdout**. The platform (Docker, Kubernetes, systemd, cloud agent) collects it. The app does not manage log files or rotation.

```json
{
  "timestamp": "2026-11-12T10:15:03.120Z",
  "level": "error",
  "message": "charging start failed",
  "service.name": "ev-api",
  "deployment.environment": "production",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "event.name": "charging.start_failed",
  "charger.id": "CP-021",
  "user.id": "u_88",
  "duration_ms": 3012,
  "exception.type": "OcppError",
  "exception.message": "Rejected",
  "exception.stacktrace": "OcppError: Rejected\n    at ..."
}
```

| Field | Rule |
|---|---|
| `message` | Short and constant ("charging start failed"). Variable data goes in fields, so logs can be grouped and searched. |
| `trace_id`, `span_id` | Required on every line written during a request. Source: W3C Trace Context (`traceparent` header). Most frameworks or OpenTelemetry create it; otherwise generate one per request and keep it in async context. |
| `event.name` | Stable dotted name for business and security events (`auth.login_failed`, `order.paid`). |
| `exception.*` | `exception.type`, `exception.message`, `exception.stacktrace` (OTel exception conventions). |
| IDs | Log IDs (`user.id`, `order.id`) instead of whole objects. |
| HTTP | `http.request.method`, `http.route` (template, e.g. `/chargers/:id`), `http.response.status_code`, `duration_ms`. |

## 2. Levels

Order follows RFC 5424 severities.

| Level | Use for | Production |
|---|---|---|
| `error` | Request or job failed and someone may need to act. Unhandled exceptions, 5xx, failed external calls with no fallback. | On, alert on rate |
| `warn` | Unexpected but handled: retry succeeded, fallback used, slow call over threshold, 4xx caused by a client bug. | On |
| `info` | Request log line, business events, job start/end, app start/stop. | On |
| `debug` | Detailed flow for development. | Off by default, switchable by config without redeploy if possible |

Expected client errors (validation 400, 401, 404) are `info` or `warn`, not `error`. Otherwise error alerts become noise.

## 3. Errors: log once, at the boundary

```
controller → service → repository → external API
                                         ↑ throws
global exception handler  ← logs it here, once, with stack + trace_id
```

- Inner layers either handle the error (and log a `warn` if it was unexpected) or let it propagate, optionally wrapped with context (`cause`). They do not log and rethrow.
- Exception: at the edge of an external call, logging the target and duration of the failure is fine if the handler would not otherwise know them. Then the handler must not log the same failure again.
- Background jobs have no HTTP handler: wrap each run in its own try/catch that logs once.

## 4. Error responses (RFC 9457)

Clients get a safe body with the trace ID, never the stack or internal message:

```json
{
  "type": "about:blank",
  "title": "Internal Server Error",
  "status": 500,
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

Set `Content-Type: application/problem+json`. Also return the ID in a response header (e.g. `traceparent` or `X-Request-Id`) so frontend error reports can include it. Support finds the logs by searching this ID.

## 5. Never log

Configure redaction centrally in the logger, not by hoping each call is careful.

- `Authorization`, `Cookie`, `Set-Cookie` headers; passwords; access, refresh, and reset tokens; API keys; OTPs; connection strings
- Full request or response bodies of auth, payment, or personal-data endpoints
- Full personal data (national ID, phone, address, card number). Mask it (`****1234`) or use an internal ID.
- Raw user input placed into the message string without encoding (log injection: newlines can forge log lines). Structured fields avoid this.

## 6. Storage and error tracking

- **Logs:** stdout → collector → a searchable store with retention (Grafana Loki, Elastic/OpenSearch, Seq, cloud logging). Choose based on what the project already deploys on.
- **Error tracking:** an error tracker (e.g. Sentry, self-hosted or SaaS) groups identical errors, shows first/last seen and release, and alerts. Use it for backend and frontend, and attach the trace ID.
- **Retention:** keep logs long enough to investigate incidents and meet policy or law; security logs usually longer. Ask the user if unknown.

## References

- OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- OpenTelemetry exception conventions: https://opentelemetry.io/docs/specs/semconv/exceptions/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- RFC 9457 Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- RFC 5424 Syslog severities: https://www.rfc-editor.org/rfc/rfc5424
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
