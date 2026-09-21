# Team Decisions

Update this file only after the team agrees. Record the date and reason so later documents remain consistent.

## Confirmed baseline

| Topic | Decision | Date | Reason |
|---|---|---|---|
| Language | Python | 2026-09-21 | Fast implementation and standard-library support |
| Repository | Private GitHub repository | 2026-09-21 | Group collaboration and controlled access |
| Default branch | `main` | 2026-09-21 | Simple pull-request workflow |
| Test framework | `unittest` | 2026-09-21 | Included in the Python standard library |
| Source separation | `model`, `controller`, `storage` | 2026-09-21 | Keeps model testable and satisfies the project requirement |

## Team decisions still required

| Topic | Recommended choice | Final decision | Owner/date |
|---|---|---|---|
| PIR identifier | Increasing positive integer | TBD | |
| Date/time format | `YYYY-MM-DD HH:mm` | TBD | |
| Command case sensitivity | Case-insensitive command names | TBD | |
| Text-search case sensitivity | Case-insensitive | TBD | |
| Load behavior | Replace current records after full validation | TBD | |
| Search precedence | `!`, then `&&`, then `||`; parentheses supported | TBD | |
| `.pim` representation | UTF-8 JSON content with `.pim` extension | TBD | |
| Invalid input behavior | Explain error, preserve data, continue running | TBD | |

## Decision record template

```text
Date:
Decision:
Reason:
Affected requirements/files:
Members present:
```
