"""Download the latest official sources into sources/ and regenerate every reference file.

Usage: python3 scripts/update_sources.py
Review the result with `git diff --stat`. A line that starts with "!" needs a manual step.
Set GITHUB_TOKEN to avoid the GitHub API rate limit (optional).
"""
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

import gen_asvs

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
ZALANDO = SRC / "zalando-restful-api-guidelines"
GENERATORS = ["gen_asvs", "gen_wcag", "gen_cwe", "gen_lighthouse", "gen_zalando", "gen_nist_pf"]


def get(url: str) -> bytes:
    headers = {"User-Agent": "webdev-playbook-update"}
    if "api.github.com" in url and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def github(path: str):
    return json.loads(get(f"https://api.github.com/repos/{path}"))


def asvs() -> str:
    # A new ASVS version can change the chapters, so it is reported, not downloaded.
    tags = [r["tag_name"] for r in github("OWASP/ASVS/releases?per_page=30")]
    versions = [m.group(1) for t in tags if (m := re.fullmatch(r"v(\d+\.\d+\.\d+)_release", t))]
    newest = max(versions, key=lambda v: tuple(map(int, v.split("."))))
    if newest == gen_asvs.VERSION:
        return f"{newest} is the newest release"
    return (f"! {newest} is out, the playbook uses {gen_asvs.VERSION}. Download its CSV from "
            "https://github.com/OWASP/ASVS/releases, then update VERSION and SLUGS in scripts/gen_asvs.py")


def wcag() -> str:
    (SRC / "wcag-2.2.json").write_bytes(get("https://www.w3.org/WAI/WCAG22/wcag.json"))
    return "2.2 downloaded (a newer WCAG version needs a new URL in scripts/gen_wcag.py)"


def cwe() -> str:
    data = get("https://cwe.mitre.org/data/xml/views/1305.xml.zip")
    with zipfile.ZipFile(io.BytesIO(data)) as z:  # fail here, before overwriting, if the download is not a zip
        head = z.read(z.namelist()[0])[:600].decode("utf-8", "replace")
    (SRC / "cwe-1305-cisq.xml.zip").write_bytes(data)
    return "CWE " + " ".join(re.findall(r'(?:Version|Date)="([^"]+)"', head)[-2:])


def lighthouse() -> str:
    tag = github("GoogleChrome/lighthouse/releases/latest")["tag_name"]
    data = get(f"https://raw.githubusercontent.com/GoogleChrome/lighthouse/{tag}/core/test/results/sample_v2.json")
    json.loads(data)  # fail here, before overwriting, if the download is not JSON
    (SRC / "lighthouse-sample-report.json").write_bytes(data)
    return tag


def zalando() -> str:
    commit = github("zalando/restful-api-guidelines/commits/main")
    label = f"{commit['sha'][:7]} ({commit['commit']['committer']['date'][:10]})"
    if (ZALANDO / "COMMIT").read_text().strip() == label:
        return f"{label}, unchanged"
    data = get(f"https://codeload.github.com/zalando/restful-api-guidelines/tar.gz/{commit['sha']}")
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        chapters = {
            Path(m.name).name: tar.extractfile(m).read()
            for m in tar.getmembers()
            if m.isfile() and re.fullmatch(r"[^/]+/chapters/[\w.-]+\.adoc", m.name)
        }
    assert chapters, "no chapters/*.adoc found in the download"
    for old in ZALANDO.glob("*.adoc"):
        old.unlink()
    for name, content in chapters.items():  # written by base name only, so an archive path cannot escape the folder
        (ZALANDO / name).write_bytes(content)
    (ZALANDO / "COMMIT").write_text(label + "\n")
    return label


def nist_pf() -> str:
    url = "https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/pf_1_0_0/export/json?element=all"
    data = get(url)
    assert json.loads(data)["response"]["elements"]["elements"], "empty NIST export"
    (SRC / "nist-privacy-framework-1.0.json").write_bytes(data)
    return "1.0 downloaded (version 1.1 is not detected: check https://www.nist.gov/privacy-framework)"


def main() -> None:
    sources = {"OWASP ASVS": asvs, "WCAG": wcag, "CWE view 1305": cwe, "Lighthouse": lighthouse,
               "Zalando API guidelines": zalando, "NIST Privacy Framework": nist_pf}
    for name, update in sources.items():
        try:
            status = update()
        except Exception as error:  # one unreachable source must not stop the others
            status = f"! update failed: {error!r}"
        prefix, text = ("! ", status[2:]) if status.startswith("! ") else ("  ", status)
        print(f"{prefix}{name}: {text}", flush=True)

    print()
    for name in GENERATORS:
        run = subprocess.run([sys.executable, str(ROOT / "scripts" / f"{name}.py")], capture_output=True, text=True)
        print(f"  {name}: {run.stdout.strip()}" if run.returncode == 0 else f"! {name} failed: {run.stderr.strip().splitlines()[-1]}")

    changed = subprocess.run(["git", "status", "--short", "--", "sources", "skills"], cwd=ROOT, capture_output=True, text=True).stdout
    print("\nChanged files:\n" + changed if changed else "\nNo file changed.")


if __name__ == "__main__":
    main()
