"""Generate skills/pb-secure-coding/references/asvs/*.md from the official OWASP ASVS CSV.

Usage: python3 scripts/gen_asvs.py [sources/asvs-5.0.0.csv]
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "asvs-5.0.0.csv"
OUT = ROOT / "skills" / "pb-secure-coding" / "references" / "asvs"
VERSION = "5.0.0"

SLUGS = {
    "V1": "encoding-injection", "V2": "validation-business-logic", "V3": "web-frontend",
    "V4": "api-web-service", "V5": "file-handling", "V6": "authentication",
    "V7": "session", "V8": "authorization", "V9": "tokens-jwt", "V10": "oauth-oidc",
    "V11": "cryptography", "V12": "tls", "V13": "config-secrets", "V14": "data-protection",
    "V15": "secure-coding-deps", "V16": "logging-errors", "V17": "webrtc",
}


def filename(chapter_id: str) -> str:
    return f"v{int(chapter_id[1:]):02d}-{SLUGS[chapter_id]}.md"


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    assert rows and set(SLUGS) == {r["chapter_id"] for r in rows}, "CSV chapters do not match SLUGS"

    chapters = defaultdict(list)
    for r in rows:
        chapters[r["chapter_id"]].append(r)

    OUT.mkdir(parents=True, exist_ok=True)
    for cid, reqs in chapters.items():
        lines = [
            f"# {cid} {reqs[0]['chapter_name']}",
            "",
            f"Source: OWASP ASVS {VERSION} (CC BY-SA 4.0). Cite as `v{VERSION}-<id>`, e.g. `v{VERSION}-{reqs[0]['req_id'][1:]}`.",
            "Level = minimum level where the requirement applies (L1 ⊂ L2 ⊂ L3).",
        ]
        section = None
        for r in reqs:
            if r["section_id"] != section:
                section = r["section_id"]
                lines += ["", f"## {section} {r['section_name']}", ""]
            desc = " ".join(r["req_description"].split())
            lines.append(f"- **{r['req_id'][1:]}** (L{r['L']}) {desc}")
        (OUT / filename(cid)).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(rows)} requirements -> {len(chapters)} files in {OUT}")


if __name__ == "__main__":
    main()
