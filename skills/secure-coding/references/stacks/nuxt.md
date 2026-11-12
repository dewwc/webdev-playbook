# Nuxt (Vue)

How to meet common ASVS requirements in Nuxt 3+. Remember that the browser code is public and the server code in `server/` is the trust boundary.

## Output and XSS (V1, V3)
- Vue escapes `{{ }}` by default. Avoid `v-html`. If it is required, sanitize with DOMPurify first.
- Never build URLs for `href` / `navigateTo` from user input without checking the protocol (`http:`/`https:` only, no `javascript:`).
- Open redirects: only allow relative paths or allowlisted hosts for `?redirect=` style parameters.

## Security headers (V3)
- Use the `nuxt-security` module (CSP, HSTS, X-Frame-Options / frame-ancestors, etc.), or set headers in `routeRules`. Start CSP in report-only mode if needed.

## Secrets (V13, V14)
- `runtimeConfig.public.*` is sent to the browser. Put API keys and secrets only in private `runtimeConfig` and use them only in `server/`.
- Do not store access tokens or refresh tokens in `localStorage`. Prefer `httpOnly` + `Secure` + `SameSite` cookies set by the server.

## Server routes (V2, V4, V8)
- Validate every input in `server/api/*` with `readValidatedBody` / `getValidatedQuery` + zod.
- Check auth and ownership in each server route (or in server middleware). Client-side route guards are UX only, not security.
- Cookie-based auth with state-changing routes: enforce `SameSite` and check `Origin`, or use a CSRF token.

## Errors (V16)
- In production, `createError` must not include stack traces or internal details for the client.
