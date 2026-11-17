---
name: pb-code-quality
description: write and review server and shared code against the iso/iec 5055 (cisq) reliability, efficiency, and maintainability weaknesses, cited as cwe ids. use when writing or reviewing calls to databases, http apis, queues, or caches (timeouts, retries, idempotency), error handling, resource cleanup, graceful shutdown, health checks, background jobs, queries in loops, n+1 queries, indexes, connection pools, or large, duplicated, or dead code, or when asked for a code quality, reliability, resilience, backend performance, maintainability, or tech debt review or audit.
---

# Code quality (ISO/IEC 5055)

ISO/IEC 5055 measures code on four characteristics. This skill covers three: **Reliability** (keeps working when something fails), **Efficiency** (does not waste database, CPU, or memory), **Maintainability** (cheap to change). The fourth, Security, belongs to `pb-secure-coding`.

Scope: code that runs on a server, including Nuxt server routes and data fetched during server rendering. Code that runs only in the browser belongs to `pb-web-performance`.

## Workflow

1. Identify which characteristic the task touches (routing table below). Most tasks touch one.
2. Load only the matching files from `references/`. Detect the stack (`*.csproj` → `dotnet.md`) and load the match from `references/stacks/`.
3. Write the code so it introduces none of the loaded weaknesses. Reuse the project's existing HTTP client, retry library, ORM, and linter settings.
4. Before finishing, check the result against the loaded files. Briefly report which items were applied and any that could not be met, citing `CWE-<id>`, or the `REL` ID for an item of `resilience.md` that has no CWE.

## Routing table

Paths are relative to `references/`.

| Task touches | Load |
|---|---|
| Calls to HTTP APIs, databases, queues, caches; timeouts, retries, idempotency; shutdown; health checks; queue consumers and jobs | `resilience.md`, `cwe/reliability.md` |
| Error handling, return values, null handling, resource cleanup, shared state across threads or requests, type and number conversion | `cwe/reliability.md` |
| Database queries, ORM usage, loops over data, indexes, connection pools, string building in loops | `cwe/efficiency.md` (slow algorithms are CWE-407, in `cwe/maintainability.md`) |
| Refactoring, module structure, large files or functions, duplicated or dead code, hard-coded values | `cwe/maintainability.md` |

## Audit mode

When asked to audit or review code quality across a project, a folder, a diff, or a PR:

1. Load `references/audit.md`, `references/resilience.md`, the three `cwe/` files, and the stack file of Workflow step 2.
2. Follow the two passes of `audit.md`: choke points first, then the scan. Then check each rule of the stack file.
3. Read each hit to confirm it before reporting; a search result alone is not a finding.
4. Report only findings, one per line: `path:line — <ID> (<characteristic>): <problem>. <fix>.` `<ID>` is the CWE; where no CWE fits, the `REL` ID; where neither exists, the section it comes from (`resilience.md §8`, `stacks/dotnet.md`). For something missing, anchor the finding at the file where it belongs. Group as **Reliability**, **Efficiency**, **Maintainability**, in that order; a CWE listed under two characteristics goes in the group of the harm you describe.
5. Fix only when the user asks. Fix choke points first (shared HTTP client, database setup, job runner), because one change there covers every call site.

## Rules

- Skip weaknesses the language rules out: manual memory management, destructors, and pointer copying do not apply to C# or TypeScript. Null dereference (CWE-476) does apply.
- *(also Security)* on an entry is information only. Report the weakness here.
- Rate limiting belongs to `pb-secure-coding` (ASVS V2.4).
- The standard gives no number for "excessive". For Maintainability, use the project's linter thresholds; without them, report only clear outliers and state what was measured (lines, parameters, copies).
- Retry only operations that are idempotent or carry an idempotency key.
- Change only what the task covers. Report other weaknesses found on the way instead of refactoring them.
