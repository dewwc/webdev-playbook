# ASP.NET Core (.NET)

How the weaknesses show up in .NET and what to use against them. Check the `*.csproj` and `Program.cs` for what is already set up. Each heading names the characteristic its findings are reported under.

## Outbound HTTP (Reliability; CWE-1088, REL05)
- Get clients from `IHttpClientFactory` (`AddHttpClient`), or keep one static client with `SocketsHttpHandler.PooledConnectionLifetime` set. `new HttpClient()` per call exhausts sockets; a static client without that setting never sees DNS changes. A vendor SDK that owns its client is not a finding; check its timeout and retry options instead.
- Resilience: `Microsoft.Extensions.Http.Resilience`, `.AddStandardResilienceHandler()` (retry, circuit breaker, 10 s per attempt, 30 s total). It retries every HTTP method by default: call `options.Retry.DisableForUnsafeHttpMethods()` unless the target endpoints are idempotent. Raise `AttemptTimeout` and `TotalRequestTimeout` for calls that take longer (AI generation, reports).
- Take a `CancellationToken` parameter in each action and pass it to `HttpClient` and EF Core calls. After a slow or paid call returns, save its result with `CancellationToken.None`, so a client disconnect does not lose it.

## Async (Reliability)
- No `.Result`, `.Wait()`, or `GetAwaiter().GetResult()` on tasks: they block threads and can deadlock.
- No `async void` outside event handlers: its exceptions cannot be caught and crash the process.

## EF Core (Efficiency, unless noted)
- N+1 (CWE-1050, CWE-1073): a query inside a loop, or lazy-loading proxies read in a loop. Load in one query with `Include`, or better a `Select` projection.
- Several collection `Include`s in one query multiply rows (CWE-1049): add `AsSplitQuery()`.
- Read-only queries that return many rows or large graphs: `AsNoTracking()`. A single-row read is not a finding.
- Bulk changes (CWE-1050): `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF Core 7+) instead of loading rows and saving them one by one.
- Paginate in the database, before `ToListAsync`: a keyset `Where` with `Take` (the kind `pb-api-design` prefers), or `OrderBy` with `Skip`/`Take`.
- Indexes (CWE-1067): declare them for filter and sort columns with `HasIndex` in the model configuration.
- Connections (CWE-1072): ADO.NET pools them by default; keep pooling on in the connection string. `AddDbContextPool` pools context objects, not connections, and is optional.
- The command timeout defaults to 30 s. Change it with `CommandTimeout` for the queries that need it.
- Reliability: `DbContext` is not thread-safe (CWE-662): one per scope, never shared across parallel tasks.
- Reliability: a rule such as "one per user" is a unique index (`HasIndex(...).IsUnique()`, filtered with `HasFilter` when it applies to some rows), not a read before the insert (CWE-662). Catch the violation (`DbUpdateException` whose inner exception is the provider's unique violation, e.g. Npgsql `PostgresException.SqlState == "23505"`) and re-read or answer 409.
- Reliability: changes that must succeed together go in one `SaveChangesAsync`, or in `BeginTransactionAsync` when they need several.

## Resources (Reliability; CWE-404)
- `using` / `await using` for every `IDisposable` / `IAsyncDisposable` the code creates that holds a stream, connection, handle, or lock (`HttpResponseMessage`, `Stream`, `DbConnection`). Content built from a string or bytes (`StringContent`, `FormUrlEncodedContent`) holds nothing to release.

## Background work (Reliability; CWE-703, REL04-BP04)
- An exception that escapes `BackgroundService.ExecuteAsync` stops the host (.NET 6+). Catch and log inside the loop, per iteration.
- A `BackgroundService` is a singleton: create a scope with `IServiceScopeFactory` for each run to get a `DbContext`.

## Health checks (Reliability)
- `AddHealthChecks()`; liveness `MapHealthChecks("/health/live", new() { Predicate = _ => false })` runs no dependency checks; readiness maps the checks tagged for it and answers 503 when one fails.

## Maintainability thresholds (Maintainability)
- Enable nullable reference types (`<Nullable>enable</Nullable>`, CWE-476) and analyzers (`<AnalysisLevel>latest-recommended</AnalysisLevel>`).
- The code-metrics analyzer rules give the numbers: CA1502 (complexity), CA1506 (class coupling), CA1501 (inheritance depth), CA1505 (maintainability index). Use the project's `.editorconfig` values when set.
