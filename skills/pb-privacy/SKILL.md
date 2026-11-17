---
name: pb-privacy
description: write and review code that handles personal data against thailand's pdpa, gdpr, and the nist privacy framework. use when code collects, stores, shares, exports, or deletes personal data - signup and profile forms, user tables and migrations, consent and cookie banners, analytics, tracking pixels, third-party sdks, marketing email, data export, account deletion, retention jobs, sending data to external services or other countries - or when asked for a privacy / pdpa / gdpr review or audit.
---

# Privacy (PDPA, GDPR, NIST Privacy Framework)

Personal data is any data about an identifiable person: name, email, phone, national ID, address, location, device or cookie ID, IP address, photo, and anything linked to them. Code that handles it must be able to answer: why do we hold this, who allowed it, who receives it, and when is it deleted.

This skill finds code-level gaps. It is not legal advice: which lawful basis applies and how long data may be kept are decisions for the business and its lawyer or DPO.

## Workflow

1. List the personal data the task touches: each field, where it is stored, and every system it is sent to.
2. Load `references/law.md`. Detect the stack (`nuxt.config.*` → `nuxt.md`, `*.csproj` → `dotnet.md`) and load each match from `references/stacks/`.
3. Each new or changed field needs a purpose, a lawful basis, and a retention period. If one is not given, ask the user or state the assumption you used.
4. Write the code so every obligation in the matching sections of `law.md` is met.
5. Before finishing, report which obligations were applied and which decisions are still open, citing the PDPA and GDPR numbers of the `law.md` row.

## Routing table

Sections are in `references/law.md`.

| Task touches | `law.md` section | NIST categories |
|---|---|---|
| New personal data: form fields, columns, API fields, uploads | 1 Collect | ID.IM-P in `identify.md`, CT.DP-P in `control.md` |
| Consent, cookie banner, analytics, tracking pixels, marketing email | 2 Consent | CT.PO-P in `control.md`, CM.AW-P in `communicate.md` |
| View, export, correct, or delete a person's data; account deletion | 3 Rights | CT.DM-P in `control.md` |
| Retention, cleanup jobs, soft delete, backups, logs | 4 Retention | CT.DM-P in `control.md` |
| Third-party services and SDKs, webhooks, data sent abroad | 5 Sharing | ID.DE-P in `identify.md` |
| Encryption, access control, masking of personal data | 6 Security | PR.DS-P, PR.AC-P in `protect.md` |

The NIST files are in `references/nist-pf/`. Load one only when the user wants findings mapped to the NIST Privacy Framework, or says the project is under neither PDPA nor GDPR; then cite `PF <id>` as well. `govern.md` holds organisation-level requirements (policies, training, roles), for audits that ask about them.

## Review mode

When asked for a privacy review or audit of a feature, diff, PR, or project:

1. Load the files of Workflow step 2.
2. Build the data inventory: every personal data field, its store, and its recipients (database columns, logs, token claims, browser storage, analytics events, third-party calls, exports). Put it at the top of the report as a short list.
3. Check the inventory against each section of `law.md` and each rule of the stack files.
4. Report findings one per line, citing the PDPA and GDPR cells of the `law.md` row: `path:line — <PDPA s.n / GDPR Art. n>: <problem>. <fix>.` A stack-file rule cites the closest row of the `law.md` section it names. For something missing, anchor the finding at the file where it belongs. Group as **Collect**, **Consent**, **Rights**, **Retention**, **Sharing**, **Security**, matching the six sections. Within a group, the most sensitive data comes first: sensitive categories and government IDs, then contact data, then the rest.
5. List separately what code cannot show: the privacy notice text, contracts with processors, the chosen lawful basis, retention periods. The split: a missing mechanism (no notice link, no delete path, no cleanup job) is a finding; a missing decision (which basis, how long) goes in this list.

## Rules

- Collect a field only when a stated purpose needs it.
- Scripts and cookies that are not needed to deliver the service (analytics, ads, social embeds) load only after the user opts in.
- Sensitive data needs explicit consent: race, ethnicity, political opinion, religious or philosophical belief, sexual behaviour or orientation, criminal record, health, disability, trade union membership, genetic and biometric data.
- Deletion reaches every copy: main database, caches, search indexes, files, analytics, and third parties.
- Personal data stays out of URLs, logs, and analytics event names (log rules: `pb-logging`, `references/patterns.md` section 5 "Never log", if installed).
- Report personal data that is unprotected (readable without authentication, stored in plain text when sensitive) under **Security**. How to protect it belongs to `pb-secure-coding` (ASVS V14, V8, V11), if installed.
- If an obligation conflicts with the user's instruction, follow the user but state the legal risk in one line.
