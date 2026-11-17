# Zalando RESTful API Guidelines: rule index

Source: Zalando RESTful API Guidelines, commit 19a1905 (2026-09-29) (CC BY 4.0). Cite as `Zalando #<id>`, e.g. `Zalando #159`.
Each line is the rule's title. Full text, rationale and examples: https://opensource.zalando.com/restful-api-guidelines/#<id>
MUST = required, SHOULD = expected unless there is a stated reason, MAY = optional. A line without a level has none in the source.

## REST Operation

- **#192** MUST: publish OpenAPI specification for APIs
- **#193** SHOULD: monitor API usage

## REST Design - Compatibility

- **#106** MUST: not break backward compatibility
- **#107** SHOULD: prefer compatible extensions
- **#109** SHOULD: design APIs conservatively
- **#108** MUST: prepare clients to accept compatible API extensions
- **#111** MUST: treat OpenAPI specification as open for extension by default
- **#113** SHOULD: avoid versioning
- **#114** MUST: use media type versioning
- **#115** MUST: not use URL versioning
- **#110** MUST: always return JSON objects as top-level data structures
- **#112** SHOULD: use open-ended list of values (via `examples`) for enumeration types

## REST Basics - Data formats

- **#238** MUST: use standard data formats
- **#171** MUST: define a format for number and integer types
- **#239** MUST: encode binary data in `base64url`
- **#169** MUST: use standard formats for date and time properties
- **#255** SHOULD: use appropriate formats for date and time properties
- **#127** SHOULD: use standard formats for time duration and interval properties
- **#170** MUST: use standard formats for country, language and currency properties
- **#244** SHOULD: use content negotiation, if clients may choose from different resource representations
- **#144** SHOULD: only use UUIDs if necessary

## REST Design - Deprecation

- **#187** MUST: reflect deprecation in API specifications
- **#185** MUST: obtain approval of clients before API shut down
- **#186** MUST: collect external partner consent on deprecation time span
- **#188** MUST: monitor usage of deprecated API scheduled for sunset
- **#189** SHOULD: add `Deprecation` and `Sunset` header to responses
- **#190** SHOULD: add monitoring for `Deprecation` and `Sunset` header
- **#191** MUST: not start using deprecated APIs

## EVENT Basics - Event Types

- **#208** MUST: define events compliant with overall API guidelines
- **#194** MUST: treat events as part of the service interface
- **#195** MUST: make event schema available for review
- **#197** MUST: specify and register events as event types
- **#213** MUST: follow naming convention for event type names
- **#207** MUST: indicate ownership of event types
- **#245** MUST: carefully define the compatibility mode
- **#196** MUST: ensure event schema conforms to OpenAPI schema object
- **#210** SHOULD: avoid `additionalProperties` in event type schemas
- **#246** MUST: use semantic versioning of event type schemas
- **#198** MUST: ensure that events conform to an event category
- **#247** MUST: provide mandatory event metadata
- **#211** MUST: provide unique event identifiers
- **#201** MUST: use general events to signal steps in business processes
- **#203** SHOULD: provide explicit event ordering for general events
- **#202** MUST: use data change events to signal mutations
- **#242** MUST: provide explicit event ordering for data change events
- **#204** SHOULD: use the hash partition strategy for data change events
- **#200** SHOULD: avoid writing sensitive data to events
- **#214** MUST: be robust against duplicates when consuming events
- **#212** SHOULD: design for idempotent out-of-order processing
- **#199** MUST: ensure that events define useful business resources
- **#205** SHOULD: ensure that data change events match the APIs resources
- **#209** MUST: maintain backwards compatibility for events

## General guidelines

- **#100** MUST: follow API first principle
- **#101** MUST: provide API Specifications using OpenAPI
- **#102** SHOULD: provide API user manual
- **#103** MUST: write APIs using U.S. English
- **#234** MUST: only use durable and immutable remote references

## REST Basics - HTTP headers

- **#133** MAY: use standard headers
- **#132** SHOULD: use kebab-case with uppercase separate words for HTTP headers
- **#178** MUST: use `Content-*` headers correctly
- **#180** SHOULD: use `Location` header instead of `Content-Location` header
- **#179** MAY: use `Content-Location` header
- **#181** MAY: consider to support `Prefer` header to handle processing preferences
- **#182** MAY: consider to support `ETag` together with `If-Match`/`If-None-Match` header
- **#230** MAY: consider to support `Idempotency-Key` header
- **#183** SHOULD: use only the specified proprietary Zalando headers
- **#184** MUST: propagate proprietary headers
- **#233** MUST: support X-Flow-ID

## REST Basics - HTTP requests

- **#148** MUST: use HTTP methods correctly
- **#149** MUST: fulfill common method properties
- **#229** SHOULD: consider to design `POST` and `PATCH` idempotent
- **#231** Should use secondary key for idempotent `POST` design
- **#253** MAY: support asynchronous request processing
- **#154** MUST: define collection format of header and query parameters
- **#236** SHOULD: design simple query languages using query parameters
- **#237** SHOULD: design complex query languages using JSON
- **#226** MUST: document implicit response filtering

## REST Basics - HTTP status codes

- **#243** MUST: use official HTTP status codes
- **#151** MUST: specify success and error responses
- **#256** MUST: preserve end-to-end semantics of HTTP status codes
- **#257** SHOULD: be careful with interpreting 404 status code
- **#150** SHOULD: only use most common HTTP status codes
- **#220** MUST: use most specific HTTP status codes
- **#152** MUST: use code 207 for batch or bulk requests
- **#153** MUST: use code 429 with headers for rate limits
- **#176** MUST: support problem JSON
- **#177** MUST: not expose stack traces
- **#251** SHOULD: not use redirection codes

## REST Design - Hypermedia

- **#162** MUST: use REST maturity level 2
- **#163** MAY: use REST maturity level 3 - HATEOAS
- **#164** MUST: use common hypertext controls
- **#165** SHOULD: use simple hypertext controls for pagination and self-references
- **#217** MUST: use full, absolute URI for resource identification (with same host, if applicable)
- **#166** MUST: not use link headers with JSON entities

## REST Basics - JSON payload

- **#167** MUST: use JSON as payload data interchange format
- **#252** SHOULD: design single resource schema for reading and writing
- **#250** SHOULD: be aware of services not fully supporting JSON/unicode
- **#168** MAY: pass non-JSON media types using data specific standard formats
- **#172** SHOULD: use standard media types
- **#120** SHOULD: pluralize array names
- **#118** MUST: property names must be snake_case (and never camelCase)
- **#240** SHOULD: declare enum values using UPPER_SNAKE_CASE string
- **#235** SHOULD: use naming convention for date/time properties
- **#216** SHOULD: define maps using `additionalProperties`
- **#123** MUST: use same semantics for `null` and absent properties
- **#122** MUST: not use `null` for boolean properties
- **#124** SHOULD: not use `null` for empty arrays
- **#174** MUST: use common field names and semantics
- **#249** MUST: use the common address fields
- **#173** MUST: use the common money object

## REST Basics - Meta information

- **#218** MUST: contain API meta information
- **#116** MUST: use semantic versioning
- **#215** MUST: provide API identifiers
- **#219** MUST: provide API audience
- **#223** MUST-SHOULD-MAY use functional naming schema
- **#224** MUST: follow naming convention for hostnames

## REST Design - Pagination

- **#159** MUST: support pagination
- **#160** SHOULD: prefer cursor-based pagination, avoid offset-based pagination
- **#248** SHOULD: use pagination response page object
- **#161** SHOULD: use pagination links
- **#254** SHOULD: avoid a total result count

## REST Design - Performance

- **#155** SHOULD: reduce bandwidth needs and improve responsiveness
- **#156** SHOULD: use `gzip` compression
- **#157** SHOULD: support partial responses via filtering
- **#158** SHOULD: allow optional embedding of sub-resources
- **#227** MUST: document cacheable `GET`, `HEAD`, and `POST` endpoints

## REST Basics - Security

- **#104** MUST: secure endpoints
- **#105** MUST: define and assign permissions (scopes)
- **#225** MUST: follow the naming convention for permissions (scopes)

## REST Basics - URLs

- **#135** SHOULD: not use /api as base path
- **#134** MUST: pluralize resource names
- **#228** MUST: use URL-friendly resource identifiers
- **#129** MUST: use kebab-case for path segments
- **#136** MUST: use normalized paths without empty path segments and trailing slashes
- **#141** MUST: keep URLs verb-free
- **#138** MUST: avoid actions — think about resources
- **#140** SHOULD: define _useful_ resources
- **#142** MUST: use domain-specific resource names
- **#139** SHOULD: model complete business processes
- **#143** MUST: identify resources and sub-resources via path segments
- **#241** MAY: expose compound keys as resource identifiers
- **#145** MAY: consider using (non-) nested URLs
- **#146** SHOULD: limit number of resource types
- **#147** SHOULD: limit number of sub-resource levels
- **#130** MUST: use snake_case (never camelCase) for query parameters
- **#137** MUST: stick to conventional query parameters
