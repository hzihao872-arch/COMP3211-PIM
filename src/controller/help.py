"""Command syntax, explanations and examples shared by help and diagnostics."""

COMMAND_HELP = {
    "help": ('help [COMMAND]', 'Show the overview or detailed help for one command.', 'help search'),
    "add": ('add TYPE "FIELD"...',
            'Fields in order: note: text; task: description deadline; event: description start_time alarm_time; '
            'contact: name address mobile_number. All fields are required. Text is trimmed and single-line. '
            'Times use YYYY-MM-DD HH:mm. Values with spaces need double quotes; inside quotes only \\" and \\\\ are escapes.',
            'add task "Prepare demo" "2026-11-01 09:00"'),
    "list": ('list [TYPE]', 'List summaries in ascending ID order; optionally filter by note, task, event or contact.', 'list task'),
    "show": ('show ID | show all', 'Print every field of one PIR or all PIRs in ascending ID order.', 'show 1'),
    "update": ('update ID FIELD "VALUE"',
               'Change one data field. ID and type cannot change. Invalid updates preserve the original PIR. '
               'Use the field names shown by help add and the same quoting/time rules.', 'update 1 text "Revised note"'),
    "delete": ('delete ID', 'Remove one PIR from memory. Save afterward to keep the deletion.', 'delete 1'),
    "search": ('search EXPR',
               'Atoms: type = "TYPE"; FIELD contains "TEXT"; TIME_FIELD <, >, or = "YYYY-MM-DD HH:mm". '
               'Text fields: text, description, name, address, mobile_number. Time fields: deadline, start_time, alarm_time. '
               'All literals need double quotes. Text matching ignores case. An absent field is false. '
               'Combine with !, &&, || and parentheses; precedence: parentheses, !, &&, ||. '
               'Only \\" and \\\\ are quoted escapes. Errors report a one-based character position in EXPR; '
               'a missing token points just past the end.', 'search type = "task" && deadline < "2026-11-01 00:00"'),
    "save": ('save "PATH.pim"',
             'Write the full snapshot and next ID. The path is required, the suffix must be lowercase .pim, '
             'and a relative path uses the working directory. Successful save clears the unsaved flag. '
             'Inside quoted Windows paths, double each backslash or use forward slashes.', 'save "data/records.pim"'),
    "load": ('load "PATH.pim" [force=true|force=false]',
             'Replace the collection after validating the whole file. Unsaved changes block loading unless force=true '
             'explicitly discards them. force=false (the default) keeps protection. Save first to preserve changes. '
             'A failed load preserves records, next ID and the unsaved flag. Successful load clears the flag. '
             'Paths follow help save.', 'load "records.pim" force=true'),
    "exit": ('exit', 'End the session. Unsaved changes produce a warning but are not saved automatically. '
             'End of input behaves the same way; save before exiting to keep your work.', 'exit'),
}


def command_help(command: str) -> str:
    usage, details, example = COMMAND_HELP[command]
    return f"Usage: {usage}\n{details}\nExample: {example}\n"
