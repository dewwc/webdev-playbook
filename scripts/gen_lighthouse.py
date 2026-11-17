"""Generate skills/pb-web-performance/references/lighthouse-audits.md from a Lighthouse JSON report.

Usage: python3 scripts/gen_lighthouse.py [sources/lighthouse-sample-report.json]
Source: https://github.com/GoogleChrome/lighthouse/blob/<release tag>/core/test/results/sample_v2.json
Any report from `lighthouse <url> --output=json` works: the audit list comes from the Lighthouse version, not the page.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "sources" / "lighthouse-sample-report.json"
OUT = ROOT / "skills" / "pb-web-performance" / "references" / "lighthouse-audits.md"

# Performance groups worth citing, in report order. "hidden" audits are raw data, not checks.
GROUPS = {
    "metrics": "Metrics (weight = share of the performance score)",
    "insights": "Insights",
    "diagnostics": "Diagnostics",
}


def main() -> None:
    report = json.loads(SRC.read_text(encoding="utf-8"))
    refs = report["categories"]["performance"]["auditRefs"]
    assert set(GROUPS) <= {r.get("group") for r in refs}, "performance groups do not match GROUPS"

    version = report["lighthouseVersion"]
    lines = [
        "# Lighthouse performance audits",
        "",
        f"Source: Lighthouse {version} (Apache-2.0). Cite as the audit ID, e.g. `lcp-discovery-insight`.",
        "Each line is the audit's own description. Follow its link for how to fix.",
    ]
    count = 0
    for group, heading in GROUPS.items():
        lines += ["", f"## {heading}", ""]
        for ref in refs:
            if ref.get("group") != group:
                continue
            desc = " ".join(report["audits"][ref["id"]]["description"].split())
            weight = f" (weight {ref['weight']})" if group == "metrics" else ""
            lines.append(f"- **{ref['id']}**{weight} — {desc}")
            count += 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{count} audits (Lighthouse {version}) -> {OUT}")


if __name__ == "__main__":
    main()
