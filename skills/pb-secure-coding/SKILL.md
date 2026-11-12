---
name: pb-secure-coding
description: write and review web app and api code against OWASP ASVS 5.0 security requirements. use whenever code touches authentication, login, passwords, mfa, sessions, jwt or refresh tokens, oauth/oidc, authorization or permissions, user input, database queries, file upload or download, cookies, cors, security headers, secrets or config, cryptography or hashing, logging or error handling, or when asked for a security review, security check, or owasp/asvs compliance of a diff, pr, endpoint, or feature.
---

# Secure Coding (OWASP ASVS 5.0)

Treat security requirements as part of "done". When writing code, apply the relevant requirements by default. When reviewing, check them and cite IDs.

## Workflow

1. Identify which security areas the task touches (use the routing table below). Most tasks touch 1–3.
2. Load only the matching files from `references/asvs/`. Do not load all chapters.
3. Load the stack file from `references/stacks/` that matches the project (detect from `package.json`, `*.csproj`, `nuxt.config.*`). It shows how to meet requirements in that stack.
4. Target **Level 2** unless the user specifies another level. Requirements marked L1 and L2 apply; L3 are optional hardening.
5. Write the code so it meets the applicable requirements. Prefer framework built-ins over custom security code.
6. Before finishing, check the result against the loaded requirements. Briefly report which ones were applied and any that could not be met, citing `v5.0.0-<id>` (e.g. `v5.0.0-8.2.2`).

Requirements in a `.1 ... Documentation` section ask for a documented decision (allowed file types, timeout policy, permission rules). If that decision is not given and the code needs it, ask the user or state the assumption you used.

## Routing table

Paths are relative to `references/`.

| Task touches | Load |
|---|---|
| SQL/NoSQL queries, HTML/JS output, shell commands, deserialization, templating | `asvs/v01-encoding-injection.md` |
| Input validation, business rules, limits, rate limiting, anti-automation | `asvs/v02-validation-business-logic.md` |
| Browser-facing pages, cookies, CSP and security headers, CORS, iframes, SRI | `asvs/v03-web-frontend.md` |
| REST/GraphQL/WebSocket endpoints, HTTP parsing, request size | `asvs/v04-api-web-service.md` |
| File upload, storage, download, image/archive processing | `asvs/v05-file-handling.md` |
| Login, passwords, MFA, OTP, password reset, account recovery, IdP login | `asvs/v06-authentication.md` |
| Sessions, logout, timeouts, session cookies, re-authentication | `asvs/v07-session.md` |
| Permissions, roles, ownership checks, multi-tenant data, admin functions | `asvs/v08-authorization.md` |
| JWT or other signed/encrypted tokens | `asvs/v09-tokens-jwt.md` |
| OAuth 2 / OpenID Connect clients, resource servers, authorization servers | `asvs/v10-oauth-oidc.md` |
| Encryption, hashing, random values, keys, certificates | `asvs/v11-cryptography.md` |
| TLS, HTTPS, service-to-service connections | `asvs/v12-tls.md` |
| Config, environment variables, secrets, debug modes, information leakage | `asvs/v13-config-secrets.md` |
| Personal or sensitive data, caching, client-side storage | `asvs/v14-data-protection.md` |
| Dependencies, mass assignment, type juggling, concurrency, race conditions | `asvs/v15-secure-coding-deps.md` |
| Logging, audit trails, error handling, exception responses | `asvs/v16-logging-errors.md` |
| WebRTC, TURN/STUN, media streams | `asvs/v17-webrtc.md` |

Common combinations:
- New authenticated CRUD endpoint: v01, v02, v04, v08
- Login / password reset: v02, v06, v07, v16
- JWT auth setup: v06, v07, v09
- File upload feature: v04, v05, v08

## Security review mode

When asked to review a diff, PR, or feature:

1. Map each changed area to rows in the routing table and load those files.
2. Check the code against each applicable requirement at the target level.
3. Report only findings, one per line: `path:line — v5.0.0-<id> (L<n>): <problem>. <fix>.` Order by severity.
4. List requirements that could not be verified from the code alone (e.g. infrastructure, documentation) separately.

## Rules

- Never weaken an existing security control to make code work (disabling validation, CSRF, TLS checks, auth guards) without telling the user explicitly.
- Never put secrets, tokens, or passwords in code, logs, or error responses.
- Authorization is checked on the server for every request, including object ownership — not only "is logged in".
- If a requirement conflicts with the user's instructions, follow the user but state the risk in one line.
