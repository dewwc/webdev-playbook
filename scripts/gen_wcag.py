"""Generate skills/pb-accessibility/references/wcag/*.md from the official W3C WCAG 2.2 JSON.

Usage: python3 scripts/gen_wcag.py [sources/wcag-2.2.json]
Source: https://www.w3.org/WAI/WCAG22/wcag.json
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "wcag-2.2.json"
OUT = ROOT / "skills" / "pb-accessibility" / "references" / "wcag"
VERSION = "2.2"
UNDERSTANDING = "https://www.w3.org/WAI/WCAG22/Understanding/{}.html"


def to_text(content: str) -> str:
    """Flatten the criterion HTML to markdown, keeping exception lists (<dt>/<dd>) as sub-bullets."""
    s = " ".join(content.split())
    s = re.sub(r"<dt>\s*", "\x00**", s)
    s = re.sub(r"\s*</dt>\s*", "**: ", s)
    s = re.sub(r"<li>\s*", "\x00", s)
    s = re.sub(r"<[^>]+>", " ", s)
    parts = [" ".join(html.unescape(p).split()) for p in s.split("\x00")]
    return parts[0] + "".join(f"\n  - {p}" for p in parts[1:] if p)


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for p in data["principles"]:
        lines = [
            f"# {p['num']}. {p['handle']}",
            "",
            f"Source: W3C WCAG {VERSION} (W3C Document License). Cite as `WCAG <num> (<level>)`, e.g. `WCAG 1.1.1 (A)`.",
            "Level: A = minimum, AA = usual target (includes A), AAA = enhanced.",
            f"Each criterion links to its W3C *Understanding* page, which explains intent and sufficient techniques.",
        ]
        for g in p["guidelines"]:
            lines += ["", f"## {g['num']} {g['handle']}", ""]
            for sc in g["successcriteria"]:
                if VERSION not in sc.get("versions", []):  # e.g. 4.1.1 Parsing, removed in 2.2
                    continue
                total += 1
                new = " *(new in 2.2)*" if sc["versions"] == [VERSION] else ""
                lines.append(
                    f"- **{sc['num']} {sc['handle']}** ({sc['level']}){new} — "
                    f"{to_text(sc['content'])} [Understanding]({UNDERSTANDING.format(sc['id'])})"
                )
        (OUT / f"{p['num']}-{p['id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert total > 80, f"unexpected criteria count: {total}"
    print(f"{total} success criteria -> {len(data['principles'])} files in {OUT}")


if __name__ == "__main__":
    main()
