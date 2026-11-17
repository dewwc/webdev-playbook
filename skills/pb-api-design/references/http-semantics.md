# HTTP API contract

What each part of an endpoint must mean. `§` numbers are sections of RFC 9110 (HTTP Semantics); `#` numbers are rules in `zalando-rules.md`.

## 1. Methods (§9)

| Method | Safe | Idempotent | Use for | Success |
|---|---|---|---|---|
| `GET` | yes | yes | Read. No side effects, no request body. | 200 |
| `POST` | no | no | Create under a collection; run an action that is not idempotent. | 201 + `Location` (created), 200 or 204 (action), 202 (accepted, runs later) |
| `PUT` | no | yes | Replace the whole resource at a URL the client knows. | 200 or 204; 201 if it created |
| `PATCH` (RFC 5789) | no | no | Change some fields. | 200 or 204 |
| `DELETE` | no | yes | Remove. | 204, or 200 with a body |

- Safe (§9.2.1): the client asks for no state change. Idempotent (§9.2.2): sending the request twice leaves the same state as sending it once, so a client may retry it.
- URLs name resources with nouns; the method is the verb (#141, #138). #148 and #149 hold the full method rules.

## 2. Status codes (§15)

| Situation | Code | § |
|---|---|---|
| Success with a body | 200 | 15.3.1 |
| Resource created | 201 + `Location` | 15.3.2, 10.2.2 |
| Accepted, processed later | 202 | 15.3.3 |
| Success without a body | 204 | 15.3.5 |
| Malformed request, failed validation | 400 (some APIs use 422 for well-formed but invalid data; pick one per API) | 15.5.1, 15.5.21 |
| Missing or invalid credentials | 401 + `WWW-Authenticate` | 15.5.2 |
| Authenticated, not allowed | 403 | 15.5.4 |
| No such resource (or its existence is hidden) | 404 | 15.5.5 |
| Method not supported on this URL | 405 + `Allow` | 15.5.6 |
| Conflict with current state: duplicate, wrong state for the action | 409 | 15.5.10 |
| `If-Match` precondition failed | 412 | 15.5.13 |
| Request media type not supported | 415 | 15.5.16 |
| Rate limited | 429 + `Retry-After` (#153) | RFC 6585 §4 |
| Unhandled server error | 500 | 15.6.1 |
| A dependency failed or timed out | 502, 504 | 15.6.3, 15.6.5 |
| Temporarily unable to serve | 503 + `Retry-After` | 15.6.4 |

- The status code alone tells success from failure: an error never returns 200 with an error body (§15). A stream (`text/event-stream`) that has already sent 200 can report a later failure only inside the stream; that is not a finding, but a failure known before the first byte gets a status code.
- Work that can outlast client or proxy timeouts (often 30–60 s): 202 with a status resource (#253), or a stream.
- The spec lists every success and error response of each endpoint (#151).

## 3. Errors (RFC 9457)

Every error response of the API uses one shape, problem details, with `Content-Type: application/problem+json` (#176):

```json
{
  "type": "https://example.com/problems/validation-error",
  "title": "Your request is not valid.",
  "status": 422,
  "detail": "2 fields failed validation.",
  "instance": "/orders/8f14e45f",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "errors": [
    { "pointer": "#/email", "detail": "must be an email address" },
    { "pointer": "#/quantity", "detail": "must be greater than 0" }
  ]
}
```

| Member | Rule |
|---|---|
| `type` | URI that identifies the kind of problem; clients branch on this, not on `title`. `about:blank` when the status code says it all. |
| `title` | Short, the same for every occurrence of this `type`. |
| `status` | Same number as the HTTP status code. |
| `detail` | Explains this occurrence, written for the client developer. No stack trace, SQL, or internal host name (#177). |
| `instance` | URI of this occurrence. Optional. |
| extensions | Extra members such as `traceId` (the request's trace ID; see `pb-logging`, if installed) and `errors` for per-field validation messages. |

The `errors` array above follows the RFC's own example. A framework's built-in validation shape (see the stack file) is fine when every validation error of the API uses it.

## 4. Concurrency and repeat requests

- Lost updates: where several clients edit one resource, return an `ETag` on read and require `If-Match` on its `PUT`, `PATCH`, and `DELETE`. A stale tag gets 412 (§13.1.1, #182).
- Repeated `POST`: where a duplicate does harm (payment, order), accept an `Idempotency-Key` header and return the stored result for a repeated key (#230), or reject the duplicate through a unique business key (#231). Design `POST` and `PATCH` to be idempotent where it is cheap (#229).

## 5. Collections

- Every list that can grow is paginated, with a maximum page size enforced on the server (#159).
- A list response is a JSON object with the items in a named array, never a top-level array, so fields can be added later (#110).
- Prefer cursor-based pagination; offset pagination skips or repeats rows when data changes and gets slow on deep pages (#160). Avoid returning a total count unless the client needs it (#254).
- Filtering and sorting use query parameters with the same names across the API (#137, #236).

## 6. Compatibility (#106–#108)

| Compatible | Breaking |
|---|---|
| Add an optional request field or query parameter | Remove or rename a field, parameter, or endpoint |
| Add a response field | Change a field's type, format, or meaning |
| Add an endpoint or method | Make an optional input required; add a required input |
| Add an enum value to a *request* field | Add an enum value to a *response* field, unless documented as open-ended (#112) |
| Loosen validation of input | Tighten validation; change a status code or the error shape |

- Clients ignore response fields they do not know (#108), so servers may add them.
- Before removing anything: mark it `deprecated: true` in the spec (#187), add `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) response headers (#189), and remove it only after its usage has stopped (#188).
- Versioning: avoid needing it by making compatible changes (#113). When a breaking change is unavoidable, use the scheme the API already has. Zalando requires media type versioning and forbids URL versioning (#114, #115); a project with `/v1` in its URLs keeps that scheme.

## 7. OpenAPI

- The spec is the source of truth for the contract (#101) and is published (#192). A new spec uses OpenAPI 3.1 or later (3.2 is current); a 3.0 spec from the project's existing generator is not a finding.
- Each operation declares: parameters, request body schema, every response code with its schema (#151), and the problem details schema for errors.
- Schemas state `required`, types, and standard `format`s: `date-time` (RFC 3339), `uuid`, `email`, `int64` (#238, #169, #171).
- ASP.NET Core generates the spec from the code (`Microsoft.AspNetCore.OpenApi`): declare response types and status codes on each endpoint, so the generated spec matches the behaviour.

## 8. Caching (RFC 9111)

- Cacheable endpoints say so in the spec and set `Cache-Control` (#227).
- Responses with per-user or sensitive data set `no-store` (ASVS 14.3.2 in `pb-secure-coding`, if installed). A shared cache does not store a response to a request with `Authorization` unless the response allows it (RFC 9111 §3.5), so a missing header there is Improve, not Wrong.

## References

- RFC 9110 HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110
- RFC 9111 HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111
- RFC 9457 Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- RFC 5789 PATCH: https://www.rfc-editor.org/rfc/rfc5789
- RFC 6585 Additional HTTP Status Codes (429): https://www.rfc-editor.org/rfc/rfc6585
- RFC 8594 Sunset header: https://www.rfc-editor.org/rfc/rfc8594
- RFC 9745 Deprecation header: https://www.rfc-editor.org/rfc/rfc9745
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
