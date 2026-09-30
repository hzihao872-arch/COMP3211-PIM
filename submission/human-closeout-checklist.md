# Human Closeout — Group 89

**Current state:** pre-video release candidate only. The two real MP4s and completed official Honour Declaration have not been supplied. Do not upload the candidate ZIP as the final submission. The official deadline is 2026-11-20 20:00.

## 1. Supply and confirm real group information

- [ ] Confirm the four real member names and student IDs against the group roster. Replace `MEMBER_A`–`MEMBER_D` in the speaking plan with verified identities; do not infer them from repository accounts.
- [ ] Agree each member's actual contribution percentage. Record the four values in the official Honour Declaration and verify their sum is 100%.
- [ ] Review `submission/ai-use-log.md` with the group and accurately disclose GenAI-assisted content in the official form. Confirm any additional human or tool contributions since this log was written.
- [ ] Obtain and complete the **official** `Honour Declaration for Group Project`, including every required real signature or confirmation. Export it as `Honour_Declaration_for_Group_Project.pdf`; inspect it visually and place it at the ZIP root. This checklist is not the form.

## 2. Record the two different videos

- [ ] Run the two-process demonstration in `media/demo/demo-script.md` and `demo-commands.txt` against frozen source SHA `4d3508db0447a3ac6346a2a2789da89208f88fd5`. Record the real system demonstration as `System_Demo.mp4` and verify its measured duration is **at most 4:00**.
- [ ] Record the presentation using `artifacts/presentation/Presentation.pdf` and `media/presentation/presentation-script.md` as a starting plan. Export the real `Presentation_Recording.mp4` and verify its measured duration is **at most 5:00**.
- [ ] Time each person's actual speaking interval in the final presentation MP4. Each member must speak for **at least 1:00**. Check each real student ID card and face at the beginning of that person's presentation, and keep the current speaker's face visible throughout their speech. Record the measured intervals and review result in `media/presentation/presentation-script.md` or a signed group record.
- [ ] Play back both exported MP4s for audio, readable screen/slides, correct commands, identities, and transitions. Planned script windows are not proof of compliance.

## 3. Put the real files in the release tree

From the repository root in PowerShell, copy the **actual reviewed** files. The prompts request paths to the files supplied by the group; nothing is generated or filled in for them:

```powershell
$releaseDir = (Resolve-Path 'output/COMP3211_Group_Project').Path
$demoSource = Read-Host 'Path to the reviewed System_Demo.mp4'
$presentationSource = Read-Host 'Path to the reviewed Presentation_Recording.mp4'
$declarationSource = Read-Host 'Path to the official signed declaration PDF'
Copy-Item -LiteralPath $demoSource -Destination (Join-Path $releaseDir '04_Demo/System_Demo.mp4')
Copy-Item -LiteralPath $presentationSource -Destination (Join-Path $releaseDir '05_Presentation/Presentation_Recording.mp4')
Copy-Item -LiteralPath $declarationSource -Destination (Join-Path $releaseDir 'Honour_Declaration_for_Group_Project.pdf')
```

The required destinations are:

```text
output/COMP3211_Group_Project/04_Demo/System_Demo.mp4
output/COMP3211_Group_Project/05_Presentation/Presentation_Recording.mp4
output/COMP3211_Group_Project/Honour_Declaration_for_Group_Project.pdf
```

Do not put empty placeholders there. Use a media inspector such as `ffprobe` (if installed) to measure each actual MP4, for example:

```powershell
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$releaseDir\04_Demo\System_Demo.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$releaseDir\05_Presentation\Presentation_Recording.mp4"
```

The numeric results are seconds; check ≤240 and ≤300 respectively. With `ffprobe` installed, this also makes the limits fail explicitly:

```powershell
if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) { throw 'Install ffprobe or use another measured-duration tool' }
$demoSeconds = [double](ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$releaseDir\04_Demo\System_Demo.mp4")
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect System_Demo.mp4' }
$presentationSeconds = [double](ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$releaseDir\05_Presentation\Presentation_Recording.mp4")
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect Presentation_Recording.mp4' }
if ($demoSeconds -le 0 -or $presentationSeconds -le 0) { throw 'A recording has no measurable positive duration' }
if ($demoSeconds -gt 240 -or $presentationSeconds -gt 300) { throw 'Recording duration exceeds the official limit' }
```

Also inspect the files as videos, since metadata alone cannot establish the speaker or identity rules. If `ffprobe` is unavailable, use another trusted player or media inspector that shows measured duration and record the tool/result. No duration can be claimed until the real files exist.

## 4. Reverify, hash, ZIP, and upload

- [ ] Re-run the Developer Manual's launch, 33-test command, and model coverage from a **freshly extracted or copied** `03_Implementation`. Keep Python 3.11 labelled unverified unless a real 3.11 run is recorded.
- [ ] Open every PDF and check that `Requirements_Coverage.pdf` and `Test_Coverage.pdf` are directly in `03_Implementation`, and the signed Honour Declaration is directly in the ZIP root.
- [ ] Update `submission/manifest.md` with the real MP4/PDF SHA-256 hashes, measured durations, identities/face review, declaration review, and exact verification evidence. `Get-FileHash -Algorithm SHA256 <path>` prints each hash. Remove the three pending-artifact entries only after their checks pass.
- [ ] Search the release tree for `__pycache__`, `.pyc`, virtual environments, secret files, personal absolute paths, and stale placeholders. Keep the two human MP4s and declaration; do not include working `.pim` data or temporary files.
- [ ] Create the **final** ZIP from the *contents* of the release directory so `01_SRS/`, `02_Design/`, `03_Implementation/`, `04_Demo/`, `05_Presentation/`, and `Honour_Declaration_for_Group_Project.pdf` are at the archive root:

```powershell
$releaseDir = (Resolve-Path 'output/COMP3211_Group_Project').Path
$zipPath = Join-Path (Resolve-Path 'output').Path 'COMP3211_Group_Project.zip'
foreach ($required in @('04_Demo/System_Demo.mp4', '05_Presentation/Presentation_Recording.mp4', 'Honour_Declaration_for_Group_Project.pdf')) {
    if (-not (Test-Path -LiteralPath (Join-Path $releaseDir $required))) { throw "Missing real human artifact: $required" }
}
Compress-Archive -Path (Join-Path $releaseDir '*') -DestinationPath $zipPath -Force
Add-Type -AssemblyName System.IO.Compression
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try { $zip.Entries | Select-Object -ExpandProperty FullName } finally { $zip.Dispose() }
```

- [ ] Open that final ZIP independently, verify all required entries, inspect all three real human files and both coverage-report locations, and repeat the clean extraction test. Upload the verified ZIP before the official deadline and keep the real upload receipt.

Until every box above is supported by real evidence, the release remains a **pre-video candidate**, not a final submission.
