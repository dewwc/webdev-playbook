# Logging audit

Audit the whole project in two passes: choke points first (few files, biggest impact), then a scan for anti-patterns. Read files to confirm before reporting; search results alone are not findings.

## Pass 1: choke points

For each item, find where it lives (or confirm it is missing).

| # | Check | Where to look | Missing / wrong when |
|---|---|---|---|
| 1 | Central logger setup | app bootstrap (`main.ts`, `Program.cs`, `app/main.py`, `nuxt.config`, server plugins) | Plain-text output, logs to files inside the app, no level config, no redaction, `console.log` used as the logger |
| 2 | Trace ID per request | middleware, OpenTelemetry setup, logger context | Log lines from one request cannot be linked; ID not returned to the client |
| 3 | Request log | HTTP logging middleware | No per-request line, or it lacks route, status, or duration |
| 4 | Global exception handler | exception filter / `UseExceptionHandler` / framework error hook | Unhandled errors not logged, logged without stack, or stack sent to the client |
| 5 | External calls | HTTP clients, DB layer, queue, device/protocol clients | Failures not logged anywhere, or no duration on slow calls |
| 6 | Business events | services for the main user flows | Key state changes (payment, start/stop, cancel) leave no trace |
| 7 | Security events | auth and permission code | Login failure, access denied, password/role change not logged |
| 8 | Jobs and cron | schedulers, queue consumers, hosted services | Run failure not logged, or a failure stops the job silently |
| 9 | Frontend errors | Vue/Nuxt error handler, error tracker setup | Uncaught errors and failed API calls not reported |

## Pass 2: anti-patterns

Search, then open each hit to confirm. Adapt the patterns to the stack.

| Problem | Search for (examples) | Category |
|---|---|---|
| Silent catch | `catch\s*(\(\w*\))?\s*\{\s*\}`, `except.*:\s*pass`, `catch { }` | Missing |
| Catch, log, rethrow (duplicate logs) | a `catch` block that logs and then `throw`s | Wrong |
| Unstructured message | template strings or concatenation in log calls (`` log(`...${x}`) ``, `f"..."`, `$"..."`) | Wrong |
| Debug output left in code | `console.log`, `print(`, `Console.WriteLine` in server code | Wrong |
| Wrong level | `error` for 4xx/validation, `info` for real failures | Wrong |
| Secrets or personal data | log calls near `password`, `token`, `authorization`, `cookie`, `secret`, `otp`, logging whole `req`/`body`/`user` objects | Leak |
| Stack trace to client | error responses that include `stack`, `exception.ToString()`, `traceback` | Leak |

## Report format

```
Missing
- src/main.ts:12 — no global exception filter; unhandled errors are not logged. Add filter per stacks/nestjs.md.
Wrong
- src/charging/charging.service.ts:88 — catch logs then rethrows; error logged twice. Remove the log, keep the throw.
Leak
- src/auth/auth.service.ts:41 — logs reset link with token. Log user id only.
```

End with a short list of what to fix first, choke points before individual call sites.
