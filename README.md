# webdev-playbook

Personal playbook of AI agent skills for building and reviewing web apps.

## Skills

| Skill | Use for |
|---|---|
| [`secure-coding`](skills/secure-coding/SKILL.md) | Write and review code against OWASP ASVS 5.0 (auth, authorization, input, files, tokens, secrets, logging) |
| [`accessibility`](skills/accessibility/SKILL.md) | Build and review UI against WCAG 2.2 A/AA (keyboard, focus, contrast, forms, ARIA) |

## Install (Claude Code)

Symlink a skill into your personal skills folder:

```sh
ln -s "$(pwd)/skills/secure-coding" ~/.claude/skills/secure-coding
```

## Updating generated references

Reference files are generated from official sources in `sources/`. Do not edit them by hand; re-running a script overwrites them.

```sh
python3 scripts/gen_asvs.py sources/asvs-5.0.0.csv   # skills/secure-coding/references/asvs/
python3 scripts/gen_wcag.py sources/wcag-2.2.json    # skills/accessibility/references/wcag/
```

## License and attribution

The ASVS content in `sources/` and `skills/secure-coding/references/asvs/` is from the
[OWASP Application Security Verification Standard 5.0.0](https://github.com/OWASP/ASVS),
© OWASP Foundation, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The WCAG content in `sources/` and `skills/accessibility/references/wcag/` is from
[Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/).
Copyright © World Wide Web Consortium, used under the
[W3C Document License](https://www.w3.org/copyright/document-license-2023/).
