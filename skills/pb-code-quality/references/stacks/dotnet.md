# ASP.NET Core (.NET)

How the weaknesses show up in .NET and what to use against them. Check the `*.csproj` and `Program.cs` for what is already set up.

## Outbound HTTP (CWE-1088, REL05)
- Get clients from `IHttpClientFactory` (`AddHttpClient`). `new HttpClient()` per call exhausts sockets; one static client never sees DNS changes.
- Resilience: `Microsoft.Extensions.Http.Resilience`, `.AddStandardResilienceHandler()` (retry, circuit breaker, 10 s per attempt, 30 s total). It retries every HTTP method by default: call `options.Retry.DisableForUnsafeHttpMethods()` unless the target endpoints are idempotent.
- Take a `CancellationToken` parameter in each action and pass it to `HttpClient` and EF Core calls.

## Async
- No `.Result`, `.Wait()`, or `GetAwaiter().GetResult()` on tasks: they block threads and can deadlock.
- No `async void` outside event handlers: its exceptions cannot be caught and crash the process.

## EF Core
- N+1 (CWE-1050, CWE-1073): a query inside a loop, or lazy-loading proxies read in a loop. Load in one query with `Include`, or better a `Select` projection.
- Several collection `Include`s in one query multiply rows (CWE-1049): add `AsSplitQuery()`.
- Read-only queries: `AsNoTracking()`.
- Bulk changes (CWE-1050): `ExecuteUpdateAsync` / `ExecuteDeleteAsync` (EF Core 7+) instead of loading rows and saving them one by one.
- Paginate in the database, before `ToListAsync`: a keyset `Where` with `Take` (the kind `pb-api-design` prefers), or `OrderBy` with `Skip`/`Take`.
- Indexes (CWE-1067): declare them for filter and sort columns with `HasIndex` in the model configuration.
- Connections (CWE-1072): ADO.NET pools them by default; keep pooling on in the connection string. `AddDbContextPool` pools context objects, not connections, and is optional.
- The command timeout defaults to 30 s. Change it with `CommandTimeout` for the queries that need it.
- `DbContext` is not thread-safe (CWE-662): one per scope, never shared across parallel tasks.

## Resources (CWE-404)
- `using` / `await using` for every `IDisposable` / `IAsyncDisposable` the code creates (streams, connections, `HttpResponseMessage`).

## Background work (CWE-703, REL04-BP04)
- An exception that escapes `BackgroundService.ExecuteAsync` stops the host (.NET 6+). Catch and log inside the loop, per iteration.
- A `BackgroundService` is a singleton: create a scope with `IServiceScopeFactory` for each run to get a `DbContext`.

## Health checks
- `AddHealthChecks()`; liveness `MapHealthChecks("/health/live", new() { Predicate = _ => false })` runs no dependency checks; readiness maps the checks tagged for it.

## Maintainability thresholds
- Enable nullable reference types (`<Nullable>enable</Nullable>`, CWE-476) and analyzers (`<AnalysisLevel>latest-recommended</AnalysisLevel>`).
- The code-metrics analyzer rules give the numbers: CA1502 (complexity), CA1506 (class coupling), CA1501 (inheritance depth), CA1505 (maintainability index). Use the project's `.editorconfig` values when set.
