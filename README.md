# webdev-playbook

Personal playbook of AI agent skills for building and reviewing web apps. Each skill checks code against a recognised standard and cites the standard's own IDs in its findings.

## Skills

| Skill | Use for | Standard |
|---|---|---|
| [`pb-secure-coding`](skills/pb-secure-coding/SKILL.md) | Write and review code for security (auth, authorization, input, files, tokens, secrets) | OWASP ASVS 5.0 |
| [`pb-accessibility`](skills/pb-accessibility/SKILL.md) | Build and review UI for accessibility (keyboard, focus, contrast, forms, ARIA) | WCAG 2.2 A/AA |
| [`pb-logging`](skills/pb-logging/SKILL.md) | Add and audit structured logging and error tracking | OpenTelemetry, W3C Trace Context |
| [`pb-web-performance`](skills/pb-web-performance/SKILL.md) | Build and review pages for loading speed, responsiveness, and layout stability | Core Web Vitals, Lighthouse |
| [`pb-code-quality`](skills/pb-code-quality/SKILL.md) | Write and review server code for reliability, efficiency, and maintainability | ISO/IEC 5055 (CISQ) as CWE IDs, AWS Well-Architected Reliability Pillar |
| [`pb-api-design`](skills/pb-api-design/SKILL.md) | Design and review HTTP API contracts (methods, status codes, errors, pagination, compatibility) | RFC 9110, RFC 9457, OpenAPI, Zalando RESTful API Guidelines |
| [`pb-privacy`](skills/pb-privacy/SKILL.md) | Write and review code that handles personal data (consent, retention, deletion, sharing) | Thailand PDPA, GDPR, NIST Privacy Framework 1.0 |

## เรียกใช้ skill ไหน เมื่อไหร่

ตอนเขียน code ไม่ต้องเรียกเอง: skill ทำงานเองเมื่องานตรงกับเงื่อนไขในตาราง ตอนต้องการตรวจ ให้พิมพ์คำสั่งตามตัวอย่าง หรือเรียกตรงด้วย `/<ชื่อ skill>`

| เมื่อเจอสถานการณ์นี้ | ใช้ skill | ตัวอย่างคำสั่งตรวจ |
|---|---|---|
| ทำ login, สิทธิ์การเข้าถึง, รับ input จากผู้ใช้, query ฐานข้อมูล, upload ไฟล์, token, secret | `pb-secure-coding` | "review security ของ PR นี้" |
| ทำหน้าเว็บ, form, modal, เมนู, ตาราง, รูปภาพ, สี, การใช้งานด้วย keyboard | `pb-accessibility` | "ตรวจ accessibility หน้านี้" |
| ตั้งค่า logger, exception handler, background job หรือหา error ใน production ไม่เจอ | `pb-logging` | "audit logging ทั้งโปรเจกต์" |
| หน้าเว็บโหลดช้า กดแล้วหน่วง หรือ layout กระตุก, ใส่รูป font script, คะแนน Lighthouse ต่ำ | `pb-web-performance` | "ทำไมหน้านี้ช้า" |
| เรียก API หรือฐานข้อมูลภายนอก, ระบบล่มตาม service อื่น, query ช้า, code ซ้ำหรือใหญ่เกิน | `pb-code-quality` | "audit code quality" |
| ออกแบบหรือแก้ endpoint, status code, รูปแบบ error, pagination, กังวลเรื่อง breaking change | `pb-api-design` | "review API design" |
| เก็บข้อมูลส่วนบุคคล, cookie banner, analytics, ลบบัญชี, ส่งข้อมูลให้บริการภายนอก | `pb-privacy` | "ตรวจ PDPA ของ feature นี้" |

งานเดียวอาจใช้หลาย skill พร้อมกัน เช่น endpoint สมัครสมาชิกใช้ `pb-secure-coding`, `pb-api-design` และ `pb-privacy`

ถ้าคำแนะนำของ skill ขัดกัน security และ privacy ชนะ performance และความสะดวกในการ debug เช่น ข้อมูลอ่อนไหวไม่ถูก cache แม้จะทำให้หน้าเว็บช้าลง

## Install (Claude Code)

From the repo root, symlink every skill into your personal skills folder (`-sfn` replaces an existing link instead of nesting a new one inside it):

```sh
for s in skills/*/; do ln -sfn "$(pwd)/$s" ~/.claude/skills/"$(basename "$s")"; done
```

Each skill works on its own. Where one skill points to another, it says "if installed".

## Updating generated references

Reference files are generated from official sources in `sources/`. Do not edit them by hand; re-running a script overwrites them.

Regenerate one skill's references from the source already in `sources/`:

```sh
python3 scripts/gen_asvs.py sources/asvs-5.0.0.csv                      # skills/pb-secure-coding/references/asvs/
python3 scripts/gen_wcag.py sources/wcag-2.2.json                       # skills/pb-accessibility/references/wcag/
python3 scripts/gen_cwe.py sources/cwe-1305-cisq.xml.zip                # skills/pb-code-quality/references/cwe/
python3 scripts/gen_lighthouse.py sources/lighthouse-sample-report.json # skills/pb-web-performance/references/lighthouse-audits.md
python3 scripts/gen_zalando.py sources/zalando-restful-api-guidelines   # skills/pb-api-design/references/zalando-rules.md
python3 scripts/gen_nist_pf.py sources/nist-privacy-framework-1.0.json  # skills/pb-privacy/references/nist-pf/
```

Download the latest version of every source and regenerate everything in one step:

```sh
python3 scripts/update_sources.py   # then review with: git diff --stat
```

| Source | What `update_sources.py` does |
|---|---|
| CWE view 1305, Lighthouse, Zalando guidelines | Downloads the newest release or commit and regenerates. |
| WCAG 2.2, NIST Privacy Framework 1.0 | Downloads the current file of that version again (picks up errata). |
| OWASP ASVS | Reports when a newer release exists. A new version can change the chapters, so update `VERSION` and `SLUGS` in `scripts/gen_asvs.py` by hand. |

A line of its output that starts with `!` needs a manual step. A new major version of WCAG or the NIST Privacy Framework is not detected: it lives at a new URL.

The workflow in `.github/workflows/check-sources.yml` runs the same command on the first day of each month and opens an issue when anything changed upstream. GitHub pauses scheduled workflows in a repository with no activity for 60 days.

Files that are written by hand, and need a manual check when a standard or framework changes: every `SKILL.md`, `references/stacks/*.md`, and `pb-web-performance/references/core-web-vitals.md`, `pb-code-quality/references/resilience.md`, `pb-code-quality/references/audit.md`, `pb-api-design/references/http-semantics.md`, `pb-privacy/references/law.md`, `pb-logging/references/*.md`.

`pb-privacy/references/law.md` is a code-level checklist, not legal advice. Have a lawyer or DPO review it before relying on it for a client.

## License and attribution

The ASVS content in `sources/` and `skills/pb-secure-coding/references/asvs/` is from the
[OWASP Application Security Verification Standard 5.0.0](https://github.com/OWASP/ASVS),
© OWASP Foundation, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The WCAG content in `sources/` and `skills/pb-accessibility/references/wcag/` is from
[Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/).
Copyright © World Wide Web Consortium, used under the
[W3C Document License](https://www.w3.org/copyright/document-license-2023/).

The CWE content in `sources/` and `skills/pb-code-quality/references/cwe/` is from
[CWE view 1305, CISQ Quality Measures (2020)](https://cwe.mitre.org/data/definitions/1305.html).
Copyright © 2006–2026, The MITRE Corporation. Used under the
[CWE Terms of Use](https://cwe.mitre.org/about/termsofuse.html): "The MITRE Corporation hereby grants you a
non-exclusive, royalty-free license to use CWE for research, development, and commercial purposes. Any copy
you make for such purposes is authorized on the condition that you reproduce MITRE's copyright designation
and this license in any such copy."

The Lighthouse content in `sources/` and `skills/pb-web-performance/references/lighthouse-audits.md` is from
[Lighthouse](https://github.com/GoogleChrome/lighthouse), © Google LLC, licensed under
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

The API guideline content in `sources/zalando-restful-api-guidelines/` and
`skills/pb-api-design/references/zalando-rules.md` is from the
[Zalando RESTful API Guidelines](https://github.com/zalando/restful-api-guidelines) (the commit is recorded in
`sources/zalando-restful-api-guidelines/COMMIT`),
© Zalando SE, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The rule index keeps
rule titles only.

The Privacy Framework content in `sources/` and `skills/pb-privacy/references/nist-pf/` is from the
[NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework), National Institute of Standards and
Technology, U.S. Department of Commerce. Not subject to copyright in the United States.
