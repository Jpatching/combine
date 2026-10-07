# Triage labels

Draft cards use Project single-select fields, not repository issue labels.

| Canonical role | Triage state option |
| --- | --- |
| needs-triage | needs-triage |
| needs-info | needs-info |
| ready-for-agent | ready-for-agent |
| ready-for-human | ready-for-human |
| wontfix | wontfix |

Category roles `bug` and `enhancement` map to the `Triage category` field.
Each triaged card has exactly one category and one state. These fields are separate
from Work status. Prepared tickets from to-tickets do not need triage.
For field operations and notes, read [tracker operations](issue-tracker.md).
