"""Generate skills/pb-code-quality/references/cwe/*.md from the official CWE view 1305 XML (CISQ Quality Measures).

Usage: python3 scripts/gen_cwe.py [sources/cwe-1305-cisq.xml.zip]
Source: https://cwe.mitre.org/data/xml/views/1305.xml.zip
"""
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "cwe-1305-cisq.xml.zip"
OUT = ROOT / "skills" / "pb-code-quality" / "references" / "cwe"

# Grouping ID -> name. Security is not generated (pb-secure-coding covers it); it only flags overlaps.
GROUPS = {"1306": "Reliability", "1307": "Maintainability", "1309": "Efficiency"}
OTHER = {**GROUPS, "1308": "Security"}


def main() -> None:
    with zipfile.ZipFile(SRC) as z:
        root = ET.fromstring(z.read(z.namelist()[0]))
    ns = {"c": root.tag[1 : root.tag.index("}")]}

    weaknesses = {w.get("ID"): w for w in root.iterfind(".//c:Weakness", ns)}
    members = {
        g.get("ID"): {m.get("CWE_ID") for m in g.iterfind(".//c:Has_Member", ns)}
        for g in root.iterfind(".//c:Grouping", ns)
    }
    assert set(OTHER) <= set(members), "CISQ groupings 1306-1309 not found in the XML"

    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for gid, name in GROUPS.items():
        lines = [
            f"# {name} (CISQ / ISO/IEC 5055)",
            "",
            f'Source: CWE {root.get("Version")} ({root.get("Date")}), view CWE-1305 "CISQ Quality Measures (2020)", '
            f"grouping CWE-{gid}. © The MITRE Corporation, CWE Terms of Use. Cite as `CWE-<id>`.",
            f"These are the weaknesses the CISQ measures (published as ISO/IEC 5055:2021) count for {name}.",
            "`(also …)` = the weakness is counted in another CISQ characteristic too.",
            "",
        ]
        for cid in sorted(members[gid], key=int):
            w = weaknesses[cid]
            desc = " ".join("".join(w.find("c:Description", ns).itertext()).split())
            also = [n for g, n in OTHER.items() if g != gid and cid in members[g]]
            suffix = f" *(also {', '.join(also)})*" if also else ""
            lines.append(f"- **CWE-{cid}** {w.get('Name')} — {desc}{suffix}")
        (OUT / f"{name.lower()}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        total += len(members[gid])

    print(f"{total} weaknesses -> {len(GROUPS)} files in {OUT}")


if __name__ == "__main__":
    main()
