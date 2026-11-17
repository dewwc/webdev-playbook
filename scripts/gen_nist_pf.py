"""Generate skills/pb-privacy/references/nist-pf/*.md from the official NIST Privacy Framework Core JSON.

Usage: python3 scripts/gen_nist_pf.py [sources/nist-privacy-framework-1.0.json]
Source: https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/pf_1_0_0/export/json?element=all
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "nist-privacy-framework-1.0.json"
OUT = ROOT / "skills" / "pb-privacy" / "references" / "nist-pf"
VERSION = "1.0"


def main() -> None:
    elements = json.loads(SRC.read_text(encoding="utf-8"))["response"]["elements"]["elements"]
    by_type = {t: [e for e in elements if e["element_type"] == t] for t in ("function", "category", "subcategory")}
    assert all(by_type.values()), "functions, categories or subcategories missing from the JSON"

    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for fn in by_type["function"]:
        fid = fn["element_identifier"]  # e.g. "CT-P"
        prefix = fid.split("-")[0] + "."  # categories of this function start with "CT."
        name = fn["title"].removesuffix("-P").capitalize()
        lines = [
            f"# {name} ({fid})",
            "",
            f"Source: NIST Privacy Framework {VERSION} Core (NIST, public domain). Cite as `PF <id>`, e.g. `PF CT.DM-P4`.",
            " ".join(fn["text"].split()),
        ]
        for cat in by_type["category"]:
            cid = cat["element_identifier"]  # e.g. "CT.DM-P"
            if not cid.startswith(prefix):
                continue
            lines += ["", f"## {cid} {cat['title']}", "", " ".join(cat["text"].split()), ""]
            subs = [s for s in by_type["subcategory"] if re.fullmatch(re.escape(cid) + r"\d+", s["element_identifier"])]
            for sub in sorted(subs, key=lambda s: int(s["element_identifier"][len(cid):])):
                lines.append(f"- **{sub['element_identifier']}** {' '.join(sub['text'].split())}")
            count += len(subs)
        (OUT / f"{name.lower()}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert count == len(by_type["subcategory"]), "some subcategories were not matched to a category"

    print(f"{count} subcategories -> {len(by_type['function'])} files in {OUT}")


if __name__ == "__main__":
    main()
