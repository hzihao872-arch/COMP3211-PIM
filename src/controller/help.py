"""Command syntax, explanations and examples shared by help and diagnostics."""

from model.schema import FIELDS, TIME_FIELDS, TEXT_FIELDS, MAX_RECORD_ID


FIELD_ORDER = "; ".join(f"{kind}: {' '.join(fields)}" for kind, fields in FIELDS.items())

HELP_OVERVIEW = '''Commands:
  help [COMMAND]
  add TYPE "FIELD"...  ({field_order})
  list [TYPE]
  show ID | show all
  update ID FIELD "VALUE"
  delete ID
  search EXPR
  save "PATH.pim" | load "PATH.pim" [force=true|force=false]
  exit
Types/fields/commands ignore case. Values with spaces need double quotes; inside quotes use \\" and \\\\.
Time: YYYY-MM-DD HH:mm (local, 24-hour).
Search atoms: type = "TYPE"; FIELD contains "TEXT"; deadline/start_time/alarm_time <, >, or = "TIME".
Combine with !, &&, ||, and parentheses; precedence: parentheses, !, &&, ||.
Use help COMMAND for details and examples. Unsaved changes block load unless force=true.
Exit/EOF warn about unsaved changes; they do not save automatically.
'''.replace('{field_order}', FIELD_ORDER)

COMMAND_HELP = {
    "help": ('help [COMMAND]', 'Show the overview or detailed help for one command.', 'help search'),
    "add": ('add TYPE "FIELD"...',
            f'Fields in order: {FIELD_ORDER}. All fields are required. Text is trimmed and single-line. '
            'Times use YYYY-MM-DD HH:mm. Values with spaces need double quotes; inside quotes only \\" and \\\\ are escapes.',
            'add task "Prepare demo" "2026-11-01 09:00"'),
    "list": ('list [TYPE]', 'List summaries in ascending ID order; optionally filter by note, task, event or contact.', 'list task'),
    "show": ('show ID | show all', 'Print every field of one PIR or all PIRs in ascending ID order.', 'show 1'),
    "update": ('update ID FIELD "VALUE"',
               f'Change one data field. ID must be in 1..{MAX_RECORD_ID}. ID and type cannot change. Invalid updates preserve the original PIR. '
               'Use the field names shown by help add and the same quoting/time rules.', 'update 1 text "Revised note"'),
    "delete": ('delete ID', 'Remove one PIR from memory. Save afterward to keep the deletion.', 'delete 1'),
    "search": ('search EXPR',
               'Atoms: type = "TYPE"; FIELD contains "TEXT"; TIME_FIELD <, >, or = "YYYY-MM-DD HH:mm". '
               f'Text fields: {", ".join(sorted(TEXT_FIELDS))}. Time fields: {", ".join(sorted(TIME_FIELDS))}. '
               'All literals need double quotes. Text matching ignores case. An absent field is false. '
               'Combine with !, &&, || and parentheses; precedence: parentheses, !, &&, ||. '
               'Only \\" and \\\\ are quoted escapes. Errors report a one-based character position in EXPR; '
               'a missing token points just past the end.', 'search type = "task" && deadline < "2026-11-01 00:00"'),
    "save": ('save "PATH.pim"',
             'Write and fsync the full snapshot and next ID before atomic replacement. The path is required, the suffix must be lowercase .pim, '
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
