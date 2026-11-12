---
name: pb-logging
description: add, fix, and audit application logging and error tracking so production problems can be traced. use when writing or reviewing request handlers, exception handlers or filters, background jobs, cron, calls to databases or external apis, logger setup, error responses, or when asked to "add logging", "audit logging", "check logs", "track errors", "why can't we see this error", set up structured logs, trace ids / correlation ids, sentry, or opentelemetry, in any stack (node/nestjs, .net, python, nuxt/vue).
---

# Logging and error tracking

Goal: when something fails in production, one ID leads to every log line of that request, and every error is logged exactly once with enough context to fix it.

Log at a few **choke points** that every request or error passes through. Do not log "everywhere": noise hides the signal and costs money.

## Workflow

### Write mode (new or changed code)

1. Read `references/patterns.md` (log shape, levels, what never to log, error responses).
2. Detect the stack (`package.json`, `*.csproj`, `pyproject.toml` / `requirements.txt`, `nuxt.config.*`) and read the matching file in `references/stacks/` if one exists. If none exists, apply `patterns.md` with the stack's standard structured logger.
3. Reuse the project's existing logger and setup. Add a logging library only if none exists.
4. If the change touches a choke point (table below), make sure it is logged per `patterns.md`.

### Audit mode ("audit logging", "check logs across the project")

1. Read `references/patterns.md` and `references/audit.md`.
2. Follow the audit steps in `audit.md`. Check each choke point once for the whole app, then scan for anti-patterns.
3. Report findings first, one per line, ordered by impact: `path:line — <problem>. <fix>.` Group them as **Missing**, **Wrong** (duplicate, wrong level, unstructured), **Leak** (secrets or personal data).
4. Fix only when the user asks. Fix choke points first (central setup, exception handler, request log, trace ID), because they cover most gaps with the fewest changes.

## Choke points

| # | Where | One log per… |
|---|---|---|
| 1 | Logger setup at startup | — (JSON to stdout, service name, environment, level from config, redaction) |
| 2 | Request middleware | request: method, route, status, duration, trace ID |
| 3 | Global exception handler / filter | unhandled error: exception type, message, stack, trace ID |
| 4 | Calls to external systems (DB if slow, HTTP APIs, queues, devices) | failure or slow call: target, operation, duration, outcome |
| 5 | Important business events | state change that matters to users or money (started, failed, paid, cancelled) |
| 6 | Security events | login failure, access denied, password or permission change (see ASVS V16 in `pb-secure-coding` if installed) |
| 7 | Background jobs and cron | run: start, end, failure, duration, items processed |
| 8 | Frontend | uncaught JS error / failed API call, sent to an error tracker with the trace ID |

## Rules

- Never log passwords, tokens, API keys, cookies, OTPs, full card numbers, or full reset links. Mask personal data unless needed to debug.
- Log an error **once**, where it is handled. Do not catch → log → rethrow.
- Use structured fields, not values glued into the message string.
- Never swallow an exception silently (empty `catch`).
- Do not change log output format or levels in a way that breaks existing dashboards or alerts without telling the user.
