# Resilience patterns

How code that calls anything over a network stays up when that thing is slow or down. IDs: `REL` = AWS Well-Architected Framework, Reliability Pillar best practice; `CWE` = `cwe/reliability.md`. Sections 7, 8, and 10 have no `REL` ID; cite them by CWE or by section number.

## 1. Timeouts (REL05-BP05, CWE-1088)

Every outbound call has an explicit timeout. Library defaults are too long or absent:

| Client | Default | Set with |
|---|---|---|
| `fetch` (Node, undici) | 300 s for headers and for body; no total limit | `signal: AbortSignal.timeout(ms)` |
| `$fetch` (Nuxt, ofetch) | none | `timeout` option, on a shared `$fetch.create()` instance |
| .NET `HttpClient` | 100 s | `Timeout` on the client from `IHttpClientFactory`, plus a `CancellationToken` per request |
| Database | 30 s per command in ADO.NET (SqlClient, Npgsql); none in most Node database clients | command or statement timeout, and pool acquire timeout, in the driver or ORM config |

- Pass the request's cancellation signal down (`AbortSignal`, `CancellationToken`), so work stops when the caller has gone.
- An inner timeout is shorter than the timeout of the request it serves.

## 2. Retries (REL05-BP03)

- Retry only transient failures: timeout, connection error, 502, 503, 504, and 429 (wait for `Retry-After`).
- Retry only idempotent operations, or ones that carry an idempotency key (section 3).
- Exponential backoff with jitter, and a maximum of 2–3 attempts.
- Retry at one layer only. A retry in the client, the service, and the gateway multiplies load on a struggling dependency.
- Use the stack's resilience library rather than a hand-written loop (.NET: `Microsoft.Extensions.Http.Resilience`).

## 3. Idempotency (REL04-BP04)

- An endpoint or consumer that can be called twice (client retry, queue redelivery, double click) produces the same result as one call.
- Use an idempotency key stored with the result, or a unique constraint on the natural key. See `pb-api-design`, if installed, for the header.
- Queue consumers assume at-least-once delivery and handle duplicates.

## 4. Fail fast and limit queues (REL05-BP04)

- Validate input and check preconditions before starting expensive work.
- Queues, buffers, and concurrent work have a fixed limit. When full, reject (503 or 429) instead of growing.
- A dependency that keeps failing gets a circuit breaker: stop calling it for a while and fail immediately.

## 5. Graceful degradation (REL05-BP01)

- When an optional dependency fails (recommendations, analytics, avatar service), return the core response without it: a cached value, a default, or an empty section. Only a failure of a required dependency fails the request.

## 6. Stateless processes (REL05-BP06)

- State needed by a later request lives in a shared store (database, Redis, object storage), not in process memory or on local disk. Otherwise a restart or a second instance loses it.

## 7. Graceful shutdown

On `SIGTERM`: stop accepting new requests, finish the ones in flight, then close pools and consumers (CWE-404, CWE-459).

- .NET: the host handles `SIGTERM`; put cleanup in `IHostedService.StopAsync` and raise `HostOptions.ShutdownTimeout` if work needs more than the default 30 s (.NET 6+).
- Containers: start the app in exec form (`ENTRYPOINT ["dotnet", "Api.dll"]`, `CMD ["node", ".output/server/index.mjs"]`), so the app itself receives the signal. A shell or `npm start` in between does not reliably pass it on.

## 8. Health checks

- Liveness answers "is the process stuck?" and checks nothing outside the process. If it checks the database, a database outage restarts every instance.
- Readiness answers "can this instance take traffic?" and checks required dependencies.
- .NET: `AddHealthChecks()` with `MapHealthChecks`.

## 9. Throttling (REL05-BP02)

Rate limits on incoming requests are owned by `pb-secure-coding` (ASVS V2.4).

## 10. Work that spans two systems

A database write and a call to another system cannot share one transaction.

- Save the record in a pending state first, call the other system with an idempotency key, then record the outcome.
- A job finds records left pending and completes or cancels them.
- An external side effect (charge, email, webhook) made before the local write is untracked when that write fails.

## References

- AWS Well-Architected Reliability Pillar, REL04: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-interactions-in-a-distributed-system-to-prevent-failures.html
- AWS Well-Architected Reliability Pillar, REL05: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-interactions-in-a-distributed-system-to-mitigate-or-withstand-failures.html
- Kubernetes liveness and readiness probes: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
- Google SRE Book, "Handling Overload" and "Addressing Cascading Failures": https://sre.google/sre-book/table-of-contents/
