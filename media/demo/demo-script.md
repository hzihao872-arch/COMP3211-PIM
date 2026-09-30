# System demo recording script

**Product baseline:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`<br>
**Group:** 89. Member names and student IDs await group input.<br>
**Deliverable:** `System_Demo.mp4`, maximum **4:00** under the official Project Description. The sections below are a recording plan, not observed video timings.

## Prepare the two-process demonstration

From the repository root in PowerShell, create a new empty working directory so record IDs and the snapshot path are predictable:

```powershell
$repo = (Resolve-Path .).Path
$demoDir = New-Item -ItemType Directory -Path (Join-Path $env:TEMP ("comp3211-pim-demo-" + [guid]::NewGuid().ToString("N")))
Set-Location $demoDir.FullName
python (Join-Path $repo 'src/main.py')
```

Enter **SESSION 1** from [demo-commands.txt](demo-commands.txt), excluding the `# SESSION` comment. After `exit`, start a **new** process with the same `python (Join-Path $repo 'src/main.py')` command and enter **SESSION 2**. Keep the same working directory. `snapshot.pim` is relative to it. Do not paste both sessions into one process: lines after the first `exit` would not run.

The complete commands are in [demo-commands.txt](demo-commands.txt). [demo-expected-output.txt](demo-expected-output.txt) records the frozen-program output from a clean two-process run on 2026-09-30, with invisible trailing prompt spaces removed: both processes exited 0 and the snapshot existed. Its absolute `D:\comp3211\tmp\wp06-demo` path identifies that verification run; a recording from another directory will print that directory instead. No command produced `Error:`.

## Narration and screen plan

| Planned segment | Screen action | Short narration cue |
|---|---|---|
| Opening | Show the fresh PowerShell directory and start `python src/main.py` via the command above. | “Each run starts with an empty collection. We will save and reload it across two processes.” |
| Create and inspect | Add note, task, event, and contact; run `show 2` and `list`. | “The four PIR schemas share unique increasing IDs. The task keeps its description and local deadline.” |
| Define and execute a search | Enter the complete compound `search` line. | “This one command defines a criterion and runs it. The type-and-deadline branch finds task 2; the text branch finds note 1.” |
| Change the result | Run `update 2 description "revised"`, `show 2`, and `delete 1`. | “We changed a matched record and removed the note. Its ID will not be reused.” |
| Persist | Run `save "snapshot.pim"` and `exit`. | “Save writes the collection and next-ID counter; exit alone does not save.” |
| Restore in a new process | Start the CLI again, `load`, `show all`, `add note "after load"`, and `show 5`. | “Load restores three records. The new note receives ID 5, so the deleted ID 1 is not reused.” |

Keep typing and narration concise enough to finish the **actual MP4** by 4:00. Only a timed human rehearsal or the recording's measured duration can establish compliance; these segment labels are a plan.

## Recovery during rehearsal

- If a command is mistyped, read the `Error:` category, correct it, and continue only if the output and remaining IDs still match the script. For the final take, restart in a **new empty directory** for the deterministic sequence.
- If `snapshot.pim` is not found in session 2, return to the directory used by session 1 and restart the second process. `load` resolves relative paths against the process working directory.
- If the result differs from the captured output, stop and compare the typed command and program commit. Do not present an improvised result as the frozen demonstration.
