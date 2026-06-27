# Post-publish audit packet

Purpose: verify a published route after release and preserve rollback visibility.

## Required fields

| Field | Value |
|---|---|
| Published route | TBD |
| Published date | TBD |
| Source version | TBD |
| Visual check | pending |
| Link check | pending |
| Claim check | pending |
| Rollback status | TBD |

## Checks

- Published route is reachable.
- Source version or commit reference is recorded.
- Visual layout is reviewed on the target display class.
- Links resolve to intended public-safe targets.
- Route claims match approved claim gate packet wording.
- Rollback status is known and executable.

## Routing

Use this packet after preview promotion or public route exposure. Any failed check becomes an OPEN_TASKS item or task delta entry before further release work.
