# webdev-playbook

Personal playbook of AI agent skills for building and reviewing web apps.

## Skills

| Skill | Use for |
|---|---|
| [`pb-secure-coding`](skills/pb-secure-coding/SKILL.md) | Write and review code against OWASP ASVS 5.0 (auth, authorization, input, files, tokens, secrets, logging) |
| [`pb-accessibility`](skills/pb-accessibility/SKILL.md) | Build and review UI against WCAG 2.2 A/AA (keyboard, focus, contrast, forms, ARIA) |
| [`pb-logging`](skills/pb-logging/SKILL.md) | Add and audit structured logging and error tracking (OpenTelemetry fields, W3C trace IDs, RFC 9457 errors) |

## Install (Claude Code)

From the repo root, symlink every skill into your personal skills folder (`-sfn` replaces an existing link instead of nesting a new one inside it):

```sh
for s in skills/*/; do ln -sfn "$(pwd)/$s" ~/.claude/skills/"$(basename "$s")"; done
```

## Updating generated references

Reference files are generated from official sources in `sources/`. Do not edit them by hand; re-running a script overwrites them.

```sh
python3 scripts/gen_asvs.py sources/asvs-5.0.0.csv   # skills/pb-secure-coding/references/asvs/
python3 scripts/gen_wcag.py sources/wcag-2.2.json    # skills/pb-accessibility/references/wcag/
```

## License and attribution

The ASVS content in `sources/` and `skills/pb-secure-coding/references/asvs/` is from the
[OWASP Application Security Verification Standard 5.0.0](https://github.com/OWASP/ASVS),
© OWASP Foundation, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The WCAG content in `sources/` and `skills/pb-accessibility/references/wcag/` is from
[Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/).
Copyright © World Wide Web Consortium, used under the
[W3C Document License](https://www.w3.org/copyright/document-license-2023/).
