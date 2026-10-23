"""Assemble a new review candidate from current files; never overwrite old releases.

Run from the repository: python submission/build_candidate.py LABEL
This packages available materials only. It does not certify human recordings,
identities, contribution agreement or the official Honour Declaration.
"""

import argparse
import hashlib
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label", help="Unique lowercase release label")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", args.label):
        parser.error("label must contain only lowercase letters, digits and hyphens")
    stem = "COMP3211_Group_Project-" + args.label
    output = ROOT / "output"
    stage = output / stem
    archive = output / (stem + ".zip")
    if stage.exists() or archive.exists():
        parser.error("release already exists; choose a new label to preserve it")
    files = {}
    for folder in ("src", "tests", "tools"):
        for source in (ROOT / folder).rglob("*.py"):
            if "__pycache__" not in source.parts:
                files["03_Implementation/" + source.relative_to(ROOT).as_posix()] = source
    for name, folder in (("SRS", "01_SRS"), ("Design_Document", "02_Design"),
                         ("Developer_Manual", "03_Implementation"),
                         ("User_Manual", "03_Implementation"),
                         ("Requirements_Coverage", "03_Implementation"),
                         ("Test_Coverage", "03_Implementation")):
        files[f"{folder}/{name}.pdf"] = ROOT / "artifacts/documents" / (name + ".pdf")
    for suffix in ("pdf", "pptx"):
        files[f"05_Presentation/Presentation.{suffix}"] = ROOT / "artifacts/presentation" / f"Presentation.{suffix}"
    files["03_Implementation/README.md"] = ROOT / "submission/release-README.md"
    files["AI_Assistance_Record.md"] = ROOT / "submission/ai-use-log.md"
    for source in sorted((ROOT / "docs/reports").glob("independent-*.txt")):
        files["03_Implementation/evidence/" + source.name] = source
    for name in ("independent-traceability-2026-10-23.json", "independent-pdf-geometry-2026-10-23.json"):
        files["03_Implementation/evidence/" + name] = ROOT / "docs/reports" / name
    # Check the complete input list before creating the staging directory.
    for source in files.values():
        if not source.is_file():
            raise FileNotFoundError(source)
    stage.mkdir(parents=True)
    for relative, source in files.items():
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    (stage / "04_Demo").mkdir()
    (stage / "04_Demo/README.txt").write_text(
        "Pending real System_Demo.mp4 (at most 4 minutes). No recording has been fabricated.\n",
        encoding="utf-8")
    (stage / "00_README.txt").write_text(
        "COMP3211 Group 89 - INDEPENDENT REVIEW CANDIDATE\n"
        "Not a final submission: real System_Demo.mp4, Presentation_Recording.mp4 and\n"
        "the completed official Honour Declaration are still missing.\n"
        "Final deadline in the supplied course PDF: 20 November 2026, 20:00.\n"
        "Review genuine member details, contributions and AI disclosure before submission.\n"
        "Open 03_Implementation/README.md to run and test. Both required coverage PDFs\n"
        "are directly in that source-code root. Fresh evidence is in its evidence/ folder.\n"
        "The editable PPTX is included alongside the required presentation PDF.\n"
        "SHA256SUMS.txt lists every other payload file; it does not hash itself.\n",
        encoding="utf-8")
    payload = sorted(p for p in stage.rglob("*") if p.is_file())
    (stage / "SHA256SUMS.txt").write_text("".join(
        f"{digest(p)}  {p.relative_to(stage).as_posix()}\n" for p in payload), encoding="utf-8")
    payload = sorted(p for p in stage.rglob("*") if p.is_file())
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for source in payload:
            bundle.write(source, source.relative_to(stage).as_posix())
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert len(bundle.namelist()) == len(payload)
        for source in payload:
            assert bundle.read(source.relative_to(stage).as_posix()) == source.read_bytes()
    manifest = (
        "# Current candidate manifest - COMP3211 Group 89\n\n"
        f"**Candidate:** `output/{archive.name}`\n\n"
        f"**Assembly:** `output/{stage.name}/`\n\n"
        f"**ZIP SHA-256:** `{digest(archive)}`\n\n"
        f"**Payload:** {len(payload)} files; {archive.stat().st_size} ZIP bytes.\n\n"
        "Current working-tree files, including uncommitted fixes, identify this release. "
        "Historical commit 4d3508d is not the complete delivery. Older archives are retained.\n\n"
        "## Verification\n\n"
        "Payload byte equality and ZIP CRC checked during assembly. Repository runs: "
        "51 tests passed on Python 3.11.9/3.12.3/3.13.5; full-suite model coverage "
        "416/421 (98.81%); model-only 415/421 (98.57%). See "
        "`docs/reports/independent-review-2026-10-23.md` and the final clean-extraction log "
        "for post-packaging verification. Re-run after any subsequent change.\n\n"
        "## Pending real deliverables\n\n"
        "- `04_Demo/System_Demo.mp4`: actual recording, <=4 minutes.\n"
        "- `05_Presentation/Presentation_Recording.mp4`: <=5 minutes, each member >=1 minute; "
        "real IDs/faces at each speaker's start and face visible throughout.\n"
        "- `Honour_Declaration_for_Group_Project.pdf`: official form at ZIP root, "
        "with genuine details, agreed contributions and truthful AI disclosure.\n\n"
        "NFR-01's exact disconnected/no-graphical-session check remains unverified. "
        "Human group review remains pending. This is not a submitted or complete assignment.\n\n"
        "## Per-file SHA-256\n\n| Archive path | SHA-256 |\n|---|---|\n"
        + "".join(f"| `{p.relative_to(stage).as_posix()}` | `{digest(p)}` |\n" for p in payload)
    )
    (ROOT / "submission/manifest.md").write_text(manifest, encoding="utf-8")
    (ROOT / "submission" / f"manifest-{args.label}.md").write_text(manifest, encoding="utf-8")
    print(f"Created {archive}\nFiles: {len(payload)}\nSHA-256: {digest(archive)}")


if __name__ == "__main__":
    main()
