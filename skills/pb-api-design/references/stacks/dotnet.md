# ASP.NET Core (.NET)

How to meet the contract rules in ASP.NET Core. Check `Program.cs` for what is already set up.

## Errors (RFC 9457)
- `builder.Services.AddProblemDetails()` with `app.UseExceptionHandler()` and `app.UseStatusCodePages()` turns unhandled exceptions and empty error responses into problem details, with a `traceId` extension.
- `[ApiController]` answers failed model validation with a 400 `ValidationProblemDetails`, whose `errors` member is an object keyed by field name. Keep that shape for every validation error in the API.
- Map domain exceptions to status codes in one `IExceptionHandler` (.NET 8+), not in each action.
- Return errors with `Problem(...)` / `TypedResults.Problem(...)`, never a bare string or an anonymous object.

## Status codes and response types
- Controllers: return `ActionResult<T>` and declare each outcome with `[ProducesResponseType<T>(StatusCodes.Status200OK)]`, `[ProducesResponseType(StatusCodes.Status404NotFound)]`.
- Minimal APIs: return `TypedResults` with a `Results<Ok<T>, NotFound>` return type, so the OpenAPI document gets every response without attributes.
- Create: `CreatedAtAction(nameof(GetById), new { id }, dto)` or `TypedResults.Created($"/orders/{id}", dto)` sets `Location`.
- The rate limiting middleware rejects with 503 by default: set `RejectionStatusCode = StatusCodes.Status429TooManyRequests`.

## DTOs and JSON
- Request and response types are DTOs (records), never EF entities: an entity change must not change the contract.
- Nullable reference types and `required` members decide `required` and nullability in the generated schema; keep them accurate.
- `System.Text.Json` writes enums as numbers by default. Add `JsonStringEnumConverter`, so enum values are readable and can be reordered without breaking clients.

## OpenAPI
- .NET 9+: `AddOpenApi()` and `MapOpenApi()` from `Microsoft.AspNetCore.OpenApi` (OpenAPI 3.1 from .NET 10). Older projects: Swashbuckle.
- Mark an endpoint as deprecated in the document before removing it.

## Concurrency (§13.1.1)
- Give the entity a concurrency token (`[Timestamp]` row version, or `IsConcurrencyToken()`), send it as the `ETag`, and compare it with `If-Match`. Map `DbUpdateConcurrencyException` to 412.

## Versioning
- `Asp.Versioning.Http` / `Asp.Versioning.Mvc` supports URL segment, header, and media type versioning. Use the scheme the API already has.
