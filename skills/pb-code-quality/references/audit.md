# Code quality audit

Two passes: choke points first (few files, biggest effect), then a scan for weaknesses. The ID in each row is what the finding cites; `—` means no CWE or REL ID fits, so cite the section named there.

## Pass 1: choke points

For each item, find where it lives (or confirm it is missing).

| # | Check | Where to look | Finding when |
|---|---|---|---|
| 1 | Outbound HTTP client | shared client or module setup (`AddHttpClient` in `Program.cs`; `$fetch.create` or a composable in Nuxt) | No timeout (CWE-1088), or every call site builds its own client (stack file) |
| 2 | Database setup | ORM or driver config | Connection pooling turned off (CWE-1072); no statement timeout where the driver has no default (CWE-1088, `resilience.md` section 1) |
| 3 | Retry policy | client setup, interceptors, queue config | Retries without limit or backoff, or on non-idempotent calls (REL05-BP03) |
| 4 | Queue consumers and jobs | consumers, schedulers, hosted services | A duplicate message repeats the side effect; one failure stops the loop (REL04-BP04, CWE-703) |
| 5 | Shutdown | app bootstrap, Dockerfile `CMD` | No shutdown hooks; pools and consumers never closed (CWE-404) |
| 6 | Health checks | health endpoints, deployment config | Missing, or liveness depends on the database (`resilience.md` section 8) |

## Pass 2: scan

Search, then open each hit to confirm. Adapt the patterns to the stack.

| Problem | Search for (examples) | Cite |
|---|---|---|
| Call without timeout | `new HttpClient(`, `fetch(`, `$fetch(` without a timeout nearby | CWE-1088 |
| Error detected, nothing done | empty `catch`, a caught error that is neither handled nor rethrown. | CWE-390 |
| Result or status not checked | ignored return value, HTTP response used without checking its status | CWE-252, CWE-394 |
| Resource not released | file, stream, connection, or lock opened without `using`, `with`, or `finally` | CWE-404 |
| Shared state without protection | module-level or static mutable state changed by request handlers; check-then-act on shared data | CWE-662 |
| Float equality | `==` between floating point numbers, including money held as a float | CWE-1077 |
| Query in a loop (N+1) | an ORM or repository call awaited inside `for`, `map`, `forEach`; a lazy-loaded relation read in a loop | CWE-1050, CWE-1073 |
| Slow algorithm | a linear search or a nested loop over the same collection, inside a loop | CWE-407 |
| Unbounded read | `ToListAsync()` or `ToArrayAsync()` on a table that grows, with no `Take` | — (`audit.md`, unbounded read) |
| Blocking call in async code | `.Result`, `.Wait()`, `GetAwaiter().GetResult()`, `Thread.Sleep` in request code | — (stack file) |
| External side effect before the local write | a payment, email, or webhook call made before the record is saved | — (`resilience.md` section 10) |
| Query without a usable index | `WHERE`, `ORDER BY`, or join columns that no index in the schema or migrations covers | CWE-1067 |
| Connection per request | a new database client or connection created inside a handler | CWE-1072 |
| String built in a loop | `+=` on a string inside a large loop | CWE-1046 |
| Dead and commented-out code | unused exports, unreachable branches, blocks of commented-out code | CWE-561, CWE-1085 |
| Duplicated code | the same block copied to several places | CWE-1041 |
| Circular dependencies | modules that import each other (projects that reference each other; in TypeScript, `npx madge --circular`) | CWE-1047 |
| Oversized units | very long files, functions with a long parameter list | CWE-1080, CWE-1064 |
| Hard-coded values | hosts, ports, URLs, and repeated magic numbers in code instead of config | CWE-1051, CWE-1052 |

## Report format

```
Reliability
- Services/PaymentGateway.cs:31 — CWE-1088 (Reliability): HttpClient is created per call with no timeout; a hung gateway holds the request for 100 s. Register it with AddHttpClient and set Timeout.
Efficiency
- Services/OrderService.cs:74 — CWE-1050 (Efficiency): loads the customer inside the loop, one query per order. Load them in one query with Include or a Select projection.
Maintainability
- Helpers/DateFormat.cs:12 — CWE-1041 (Maintainability): same date formatter copied in 4 files. Keep this one, call it from the others.
```

End with a short list of what to fix first, choke points before individual call sites.
