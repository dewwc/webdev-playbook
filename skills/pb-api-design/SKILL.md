---
name: pb-api-design
description: design and review http api contracts against rfc 9110 http semantics, rfc 9457 problem details, openapi, and the zalando restful api guidelines. use when adding or changing rest endpoints, routes, controllers, dtos, request or response shapes, status codes, error responses, pagination, filtering, sorting, versioning, deprecation, idempotency, an openapi / swagger spec, or when asked for an api design review, api consistency check, or breaking change check.
---

# API design (RFC 9110, OpenAPI, Zalando guidelines)

An API is a contract: once a client depends on it, every change is either compatible or breaking. Design each endpoint so that HTTP means what the standard says, the whole API behaves one way, and existing clients keep working.

## Workflow

1. Find the API's existing conventions before designing anything: the OpenAPI spec (file or generated), and how current endpoints name things, paginate, and return errors.
2. Load `references/http-semantics.md` and `references/zalando-rules.md`. Detect the stack (`*.csproj` → `dotnet.md`) and load the match from `references/stacks/`.
3. Design the endpoint to meet the RFC rules and the Zalando MUST and SHOULD rules. The project's own naming and versioning convention stays (see Rules).
4. Update the OpenAPI spec or its annotations in the same change.
5. Before finishing, report which rules were applied and any deliberate deviation, citing `RFC 9110 §<n>`, `RFC 9111`, `RFC 9457`, or `Zalando #<id>`.

## Review mode

When asked to review an endpoint, spec, diff, or PR:

1. Load the files of Workflow step 2.
2. If the change touches an existing endpoint, compare the old and new contract (`http-semantics.md` section 6). With no earlier contract (a new API, or a whole-project review), the Breaking group is empty; say so.
3. Check every endpoint in scope against each section of `http-semantics.md` and each rule of the stack file. Then read through `zalando-rules.md` for MUST rules that apply and were not reached that way.
4. Report only findings, one per line: `path:line — <RFC 9110 §n | RFC 9111 | RFC 9457 | Zalando #id (MUST|SHOULD|MAY)>: <problem>. <fix>.` A stack-file rule with no ID is cited as `stacks/<file>`. For something missing, anchor the finding at the file where it belongs. Group as **Breaking** (an existing client stops working), **Wrong** (contradicts HTTP semantics or a MUST rule), **Inconsistent** (differs from the rest of this API), **Improve** (SHOULD and MAY rules).
5. If the project has an OpenAPI linter set up (Spectral, Redocly), run it and include its errors.

## Rules

- A breaking change to a published endpoint needs the user's confirmation. Offer the compatible alternative first (add a field or endpoint, keep the old one).
- One convention per API. A consistent existing convention wins over the casing and naming-style rules (#118, #129, #130, #132), the base path rule (#135), and the versioning rules (#113–#115), and over nothing else: HTTP semantics and the other MUST rules still apply to an API that breaks them consistently.
- Rules outside a code review of an HTTP API; skip them:
  - Zalando's own platform: #183, #184, #233 (proprietary headers), #215, #219, #223, #224 (API registry and hostnames), #173, #249 (company data models).
  - Process: #100, #102, #103, #185, #186, #191, #193.
  - The `EVENT` chapters, unless the code publishes or consumes events.
  - Security (#104, #105, #225): authentication, authorization, input validation, and rate limits belong to `pb-secure-coding` (ASVS V2, V4, V6, V8).
- Error bodies carry no stack trace or internal message (#177).
- If a rule conflicts with the user's instruction, follow the user but state the effect on clients in one line.
