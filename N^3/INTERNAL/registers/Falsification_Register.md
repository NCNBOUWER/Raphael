# Falsification Register

## Purpose

This register records conditions that would invalidate or constrain claims in the standalone TPW package.

| ID | Claim | Falsification condition | Status |
|---|---|---|---|
| F-001 | TPW enumeration has 1331 sum-state triples | complete enumeration over `{2,...,12}^3` does not produce 1331 rows | passed |
| F-002 | primitive ordered outcomes are 46656 | `36^3` does not equal 46656 | passed |
| F-003 | probability sum is 1 | exact rational sum differs from 1 | passed |
| F-004 | `(7,7,7)` is unique mode | any other triple has equal or greater product count | passed |
| F-005 | minimum corner class has 8 states | corner-state enumeration differs from 8 | passed |
| F-006 | Gamma path remains in simplex | interpolation leaves nonnegative unit-sum simplex | passed by convexity |
| F-007 | TPW proves physical equations | no such proof supplied inside this package | blocked as publish claim |

## Rule

If a future empirical or Raphael-side validation changes any claim status, update this register and the open task workbook together.
