# ASP.NET Core (.NET)

How to meet common ASVS requirements in ASP.NET Core. Check the `*.csproj` and `Program.cs` for what is already set up.

## Input validation (V2, V15)
- Use DataAnnotations or FluentValidation on every request DTO, plus `[ApiController]` for automatic 400 responses.
- Bind to request DTOs, never directly to EF entities (blocks mass assignment / overposting).

## Injection (V1)
- EF Core: use LINQ, `FromSqlInterpolated` or `FromSql($"...")`. Never use `FromSqlRaw` / `ExecuteSqlRaw` with concatenated input.
- Dapper: always pass parameters (`new { id }`).
- Dynamic sort columns: map them through an allowlist dictionary.
- `Process.Start`: use `ProcessStartInfo.ArgumentList`, not a single argument string built from input.

## Authentication and passwords (V6)
- Use ASP.NET Core Identity / `PasswordHasher<T>`, or Argon2/bcrypt. Never hash passwords yourself with SHA.
- Use the rate limiting middleware (`AddRateLimiter`, .NET 7+) on login, OTP and reset endpoints.
- Use Identity lockout (`LockoutOptions`), or an equivalent throttle.

## Authorization (V8)
- Set a fallback policy (`options.FallbackPolicy = RequireAuthenticatedUser`), so new endpoints are not public by default.
- For ownership checks, use resource-based authorization (`IAuthorizationService.AuthorizeAsync(user, resource, policy)`) or filter by the owner/tenant ID in the query.

## JWT (V9)
- `AddJwtBearer` with `TokenValidationParameters`: `ValidateIssuer`, `ValidateAudience`, `ValidateLifetime`, `ValidateIssuerSigningKey` all `true`. Set `ValidAlgorithms` explicitly and keep `ClockSkew` small.

## HTTP and frontend (V3, V4, V12)
- Production: `UseHsts()` and `UseHttpsRedirection()`.
- CORS: `WithOrigins(...)` allowlist. Never use `AllowAnyOrigin()` together with credentials.
- Cookies: `HttpOnly`, `Secure`, `SameSite`. For cookie-based auth, use antiforgery for unsafe methods.
- Set request size limits (`RequestSizeLimit`, `FormOptions.MultipartBodyLengthLimit`).

## File upload (V5)
- `IFormFile`: check the size, check the content signature (magic bytes), store under a generated name outside `wwwroot`, and never use `FileName` in a path.

## Secrets and config (V13)
- Use User Secrets in dev and Key Vault / environment variables in prod. No secrets in `appsettings.json` committed to git.
- Turn off `DeveloperExceptionPage` and Swagger in production, or put Swagger behind auth.

## Errors and logging (V16)
- Use `UseExceptionHandler` + `ProblemDetails` with no exception details in production.
- Use structured logging (Serilog/ILogger) for auth failures, access denied and admin actions. Never log passwords, tokens or connection strings.
