# webdev-playbook

Personal playbook of AI agent skills for building and reviewing web apps.

## Skills

| Skill | Use for |
|---|---|
| [`secure-coding`](skills/secure-coding/SKILL.md) | Write and review code against OWASP ASVS 5.0 (auth, authorization, input, files, tokens, secrets, logging) |

## Install (Claude Code)

Symlink a skill into your personal skills folder:

```sh
ln -s "$(pwd)/skills/secure-coding" ~/.claude/skills/secure-coding
```

## Updating ASVS references

`skills/secure-coding/references/asvs/*.md` are generated from the official CSV in `sources/`:

```sh
python3 scripts/gen_asvs.py sources/asvs-5.0.0.csv
```

## License and attribution

The ASVS content in `sources/` and `skills/secure-coding/references/asvs/` is from the
[OWASP Application Security Verification Standard 5.0.0](https://github.com/OWASP/ASVS),
© OWASP Foundation, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
