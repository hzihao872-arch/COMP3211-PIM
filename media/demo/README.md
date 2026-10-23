# System Demo

Final format: MP4. Maximum duration: 4 minutes.

Suggested demonstration path:

1. Start the application.
2. Create representative PIRs.
3. Print records.
4. Run a compound search.
5. Update and delete records.
6. Save to a `.pim` file.
7. Load the file and show restored data.

Keep the script, shot list, and captions here. MP4 files are ignored by ordinary Git because recordings can exceed GitHub's normal file-size limit; coordinate final transfer separately or use Git LFS if the team explicitly decides to do so.

The current final exit warns because note 5 remains unsaved; this is expected and does not update the saved snapshot. `python tools/verify_demo.py` checks the maintained two-process transcript. Optional rehearsal: use `help load`, create an unsaved edit, then compare ordinary load with `load "snapshot.pim" force=true`.
