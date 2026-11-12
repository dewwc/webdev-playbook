# ASP.NET Core (.NET 8+)

Always log through `ILogger<T>`. Choose either the built-in JSON console or Serilog. If the project already uses one, keep it.

## Setup

Built-in (no extra package):

```csharp
builder.Logging.ClearProviders();
builder.Logging.AddJsonConsole(o => o.IncludeScopes = true);
```

Serilog (`Serilog.AspNetCore`, `Serilog.Formatting.Compact`):

```csharp
builder.Host.UseSerilog((ctx, lc) => lc
    .ReadFrom.Configuration(ctx.Configuration)
    .Enrich.FromLogContext()
    .Enrich.WithProperty("service.name", "ev-api")
    .WriteTo.Console(new CompactJsonFormatter()));
// ...
app.UseSerilogRequestLogging(); // one line per request: method, path, status, elapsed
```

Without Serilog, use the built-in `builder.Services.AddHttpLogging(...)` + `app.UseHttpLogging()`, or rely on OpenTelemetry for request telemetry.

## Message templates

```csharp
// ✅ structured: ChargerId becomes a field
_logger.LogWarning("OCPP call slow {ChargerId} {DurationMs}", chargerId, ms);
// ❌ string interpolation: no fields, no grouping
_logger.LogWarning($"OCPP call slow {chargerId} {ms}");
```

## Trace ID

ASP.NET Core creates an `Activity` per request with W3C Trace Context by default. `Activity.Current?.TraceId` is the trace ID. With `IncludeScopes` or Serilog `FromLogContext` + OpenTelemetry (`OpenTelemetry.Extensions.Hosting`), the trace ID is attached to log lines.

## Global exception handling

```csharp
builder.Services.AddProblemDetails(o => o.CustomizeProblemDetails = c =>
    c.ProblemDetails.Extensions["traceId"] = Activity.Current?.TraceId.ToString() ?? c.HttpContext.TraceIdentifier);
builder.Services.AddExceptionHandler<GlobalExceptionHandler>(); // IExceptionHandler: log once, return false to use ProblemDetails
// ...
app.UseExceptionHandler();
```

Inside `GlobalExceptionHandler.TryHandleAsync`, call `_logger.LogError(exception, "Unhandled exception")` once. Do not use `DeveloperExceptionPage` in production.

## Jobs

`BackgroundService` / Hangfire / Quartz jobs: try/catch around each run, `LogError(ex, ...)` once, and log start/end with duration. An unhandled exception in `ExecuteAsync` stops the host by default since .NET 6.
