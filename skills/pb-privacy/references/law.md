# Privacy obligations in code

Each row is an obligation a reviewer can check in code. PDPA = Thailand's Personal Data Protection Act B.E. 2562 (2019), cited by section. GDPR = Regulation (EU) 2016/679, cited by article. Section and article numbers were checked in November 2026; sub-regulations change, so confirm the details with the project's lawyer or DPO.

## 1. Collect

| Obligation | In code | PDPA | GDPR |
|---|---|---|---|
| Purpose limitation | Each personal data field has a stated purpose, and is used only for it. A new use needs a new notice or consent. | s.21 | Art. 5(1)(b) |
| Data minimisation | No field collected "in case it is useful". Fields the purpose does not need are optional or absent. Store the derived value (age over 18: yes) instead of the source (date of birth) when that is enough. | s.22 | Art. 5(1)(c) |
| Notice at collection | The form or screen that collects data links to a notice with the purpose, retention period, recipients, controller contact, and the person's rights. | s.23 | Art. 13 |
| Lawful basis | Each kind of processing has one recorded basis: consent, contract, legal obligation, vital interest, public task, or legitimate interest (PDPA adds research, statistics, and archives). | s.19, s.24 | Art. 6 |
| Sensitive data | Explicit consent, stored separately or encrypted per field, and access limited to the roles that need it. | s.26 | Art. 9, Art. 10 |
| Government identifiers | National ID, passport, and tax numbers are collected only when a law or the purpose requires them, encrypted per field, and masked on screen. | s.22, s.37(1) | Art. 5(1)(c), Art. 87 |
| Children | Consent from a parent or guardian where the law requires it. | s.20 | Art. 8 |
| Accuracy | The person can correct their data, and corrections reach the copies. | s.35, s.36 | Art. 5(1)(d), Art. 16 |
| Privacy by default | The most private setting is the default: optional sharing, public profiles, and marketing start switched off. | — | Art. 25 |

## 2. Consent

Consent is one lawful basis among several. Use these rules wherever it is the basis.

| Obligation | In code | PDPA | GDPR |
|---|---|---|---|
| Freely given and specific | One checkbox per purpose, unticked by default, separate from accepting the terms. Refusing optional processing does not block the service. | s.19 | Art. 7, Art. 4(11) |
| Provable | Store a consent record: person, purpose, wording version, timestamp, and channel. | s.19 | Art. 7(1) |
| Withdrawable | Withdrawing is as easy as giving (same screen, one action), and processing for that purpose stops, including in third-party tools. | s.19 | Art. 7(3) |
| Cookies and trackers | Non-essential cookies, pixels, and SDKs are not loaded or set before opt-in. "Reject" is as visible as "Accept". The choice is stored and respected on every page. | s.19 (when the identifier relates to a person) | ePrivacy Directive Art. 5(3), GDPR Art. 7 |
| Direct marketing | Every marketing message has a working unsubscribe, and the person can object at any time. | s.32 | Art. 21 |

## 3. Rights

The system can do each of these for one person in time: PDPA gives 30 days for an access request (s.30); GDPR gives one month for any request (Art. 12(3)).

| Right | In code | PDPA | GDPR |
|---|---|---|---|
| Access | Find and return all data about one person across every store. | s.30 | Art. 15 |
| Portability | Export it in a structured, machine-readable format (JSON, CSV). | s.31 | Art. 20 |
| Objection | A flag that stops a given kind of processing for that person. | s.32 | Art. 21 |
| Erasure | Delete or anonymise across every copy: database, caches, search indexes, files, analytics, third parties. Backups are covered by their expiry. Rows kept for a legal duty (invoices) are kept, with the rest removed. A row that is only flagged as deleted is left out of every read until it is removed. | s.33 | Art. 17 |
| Restriction | Mark data as "stored but not used" while a dispute is open. | s.34 | Art. 18 |
| Rectification | Correct data and pass the correction on. | s.35, s.36 | Art. 16 |
| Identity check | The request comes from the person themselves: an authenticated session or an equivalent check, before any data is returned or deleted. | s.37(1) | Art. 12(6) |

- Anonymised means the person can no longer be identified by anyone. Replacing the name while keeping the email or user ID is not anonymised.

## 4. Retention

| Obligation | In code | PDPA | GDPR |
|---|---|---|---|
| Storage limitation | Each kind of personal data has a retention period, and a scheduled job deletes or anonymises it when the period ends or consent is withdrawn. | s.37(3) | Art. 5(1)(e) |
| All copies | The period also applies to logs, exports, uploaded files, soft-deleted rows, and analytics. A soft-deleted row is still personal data. | s.37(3) | Art. 5(1)(e) |
| Record of processing | A maintained inventory: data categories, purposes, retention, recipients. Code changes that add personal data update it. | s.39 | Art. 30 |

## 5. Sharing

| Obligation | In code | PDPA | GDPR |
|---|---|---|---|
| Disclosure within purpose | Data goes to a third party only for a purpose the person was told about. Send the minimum fields, not the whole object. | s.27 | Art. 5(1)(b) |
| Processors | Every third-party service that receives personal data (email, analytics, error tracking, payment, AI APIs) is listed and has a data processing agreement. | s.40 | Art. 28 |
| Transfers abroad | Know the country where each third party stores data. A transfer outside the country (PDPA) or outside the EEA (GDPR) needs an adequate destination or a legal safeguard. | s.28, s.29 | Art. 44–49 |
| Third-party scripts | Analytics and session-replay tools mask form fields and do not receive names, emails, or IDs in URLs or event properties. | s.27 | Art. 5(1)(c) |

## 6. Security and breach

| Obligation | In code | PDPA | GDPR |
|---|---|---|---|
| Security measures | Encryption in transit and at rest, access control, and masking. Details: `pb-secure-coding` (ASVS V14), if installed. | s.37(1) | Art. 32 |
| Breach notification | A breach is reported to the regulator within 72 hours. Access logs must be able to show which records and which people were affected. | s.37(4) | Art. 33, Art. 34 |

## References

- PDPA B.E. 2562, unofficial English translation (MDES): https://mdes.go.th/law/detail/3577-Personal-Data-Protection-Act-B-E--2562--2019-
- GDPR full text: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- OWASP Top 10 Privacy Risks: https://owasp.org/www-project-top-10-privacy-risks/
