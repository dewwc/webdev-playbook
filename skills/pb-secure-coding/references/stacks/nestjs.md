# NestJS

How to meet common ASVS requirements in NestJS. Check `package.json` for what the project already uses before adding a library.

## Input validation (V2, V15)
- Global `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true })`. `whitelist` drops unknown fields and blocks mass assignment.
- Every DTO field has `class-validator` decorators. Use `@IsUUID()`, `@IsInt()`, `@Max()`, `@MaxLength()` and `@IsIn([...])` for enum-like strings.
- Do not pass a request body straight into `repository.save()` / `update()`. Map the allowed fields explicitly.

## Injection (V1)
- TypeORM: use `.where('u.id = :id', { id })`, and never use template strings inside `.where()` / `.query()`.
- Prisma: use `$queryRaw` with a tagged template. Do not use `$queryRawUnsafe` with user input.
- Sort and column names cannot be parameterized. Check them against an allowlist (`@IsIn(['createdAt','name'])`).
- `child_process`: use `execFile` / `spawn` with an args array. Never pass user input to `exec`.

## Authentication and passwords (V6)
- Hash with `argon2` (argon2id) or `bcrypt` (cost ≥ 10). Never use plain SHA/MD5.
- Use `@nestjs/throttler` on login, OTP, password reset and registration routes.
- Give the same response and similar timing whether the user exists or not.
- Reset tokens: random (`crypto.randomBytes(32)`), store only a hash, single use, short expiry.

## Authorization (V8)
- Apply a global `JwtAuthGuard` with an `@Public()` opt-out, so a new route is not public by accident.
- A role guard is not enough. Inside the service, check that the resource belongs to the user or tenant (`where: { id, ownerId: user.id }`), and return 404/403 if it does not.
- For multi-tenant data, always filter queries by the tenant ID from the token, never from the request body.

## JWT (V9)
- `JwtModule.register({ signOptions: { algorithm, expiresIn }, verifyOptions: { algorithms: [...] , audience, issuer } })`. Pin the algorithms.
- Keep access tokens short-lived. Refresh tokens are stored hashed, rotated on use, and revoked on logout or password change.

## HTTP and frontend (V3, V4)
- Use `helmet()`.
- CORS: `enableCors({ origin: [allowlist], credentials: true })`. Never use `origin: true` together with credentials.
- Set body size limits in the express/fastify body parser config.

## File upload (V5)
- `FileInterceptor` with `limits: { fileSize }`.
- Check the real type from the content (`file-type` magic bytes), not only `mimetype` or the extension.
- Generate the stored filename (UUID). Never use `originalname` in a path. Store outside static/public folders.

## Secrets and config (V13)
- Use `@nestjs/config` with schema validation (Joi/zod). Fail on startup if a secret is missing, and never fall back to a default secret.
- Swagger: disable it in production or put it behind auth.

## Errors and logging (V16)
- A global exception filter returns a generic message plus a correlation ID. Do not send a stack trace or DB error to the client.
- Log auth failures, access denied, and admin actions. Never log passwords, tokens, OTPs or full reset links.
- Use `ClassSerializerInterceptor` + `@Exclude()` on entity fields such as `password` and `refreshTokenHash`.
