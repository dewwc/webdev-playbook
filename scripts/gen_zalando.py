"""Generate skills/pb-api-design/references/zalando-rules.md from the Zalando RESTful API Guidelines chapters.

Usage: python3 scripts/gen_zalando.py [sources/zalando-restful-api-guidelines]
Source: https://github.com/zalando/restful-api-guidelines (the `chapters/` folder; its commit is recorded in the COMMIT file beside the chapters)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "zalando-restful-api-guidelines"
OUT = ROOT / "skills" / "pb-api-design" / "references" / "zalando-rules.md"
URL = "https://opensource.zalando.com/restful-api-guidelines/"

# A rule is an anchor line followed by a heading: "[#159]\n== {MUST} support pagination"
RULE = re.compile(r"^\[#(\d+)\]\n=+ (.+)$", re.M)
LEVEL = re.compile(r"\{(MUST|SHOULD|MAY)\}", re.I)  # the source has one "{Should}"


def clean(title: str) -> tuple[str, str]:
    """Split a rule heading into (level, text) and drop AsciiDoc markup."""
    level = "/".join(m.upper() for m in LEVEL.findall(title))
    text = LEVEL.sub("", title)
    text = re.sub(r"<<(\d+)[^>]*>>", r"#\1", text)  # cross reference to another rule
    text = re.sub(r"\{([\w-]+)\}", r"\1", text)  # attribute reference, e.g. {RFC-9457}
    return level, " ".join(text.lstrip(" /").split())  # "{MUST}/{SHOULD} x" leaves a leading slash


def main() -> None:
    lines = [
        "# Zalando RESTful API Guidelines: rule index",
        "",
        f"Source: Zalando RESTful API Guidelines, commit {(SRC / 'COMMIT').read_text().strip()} (CC BY 4.0). Cite as `Zalando #<id>`, e.g. `Zalando #159`.",
        f"Each line is the rule's title. Full text, rationale and examples: {URL}#<id>",
        "MUST = required, SHOULD = expected unless there is a stated reason, MAY = optional. A line without a level has none in the source.",
    ]
    count = 0
    for path in sorted(SRC.glob("*.adoc")):
        text = path.read_text(encoding="utf-8")
        rules = RULE.findall(text)
        if not rules:
            continue
        chapter = re.search(r"^= (.+)$", text, re.M).group(1)
        lines += ["", f"## {chapter}", ""]
        for rule_id, title in rules:
            level, body = clean(title)
            lines.append(f"- **#{rule_id}** {level + ': ' if level else ''}{body}")
        count += len(rules)
    assert count > 100, f"only {count} rules found; the chapter format may have changed"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{count} rules -> {OUT}")


if __name__ == "__main__":
    main()
