# Component paste packet

Purpose: prepare a paste-ready component without losing source trace or rollback path.

## Required fields

| Field | Value |
|---|---|
| Component name | TBD |
| Route target | TBD |
| Static fallback | required |
| Scripts required | none / local / external |
| External dependencies | TBD |
| Manual paste notes | TBD |
| Rollback instruction | TBD |

## Checks

- Static fallback exists.
- Route target confirmed.
- Component matches dashboard class.
- Field-specific brand asset applied.
- Rollback instruction present.
