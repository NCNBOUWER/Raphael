# N3 - Trinity Probability Well Proof Pack

Author: Nathaniel Bouwer  
Version: v1_0 Complete Artifact Pass  
Scope: discrete mathematical TPW proof chain only.

## 1. Definitions

Let each component `X_i` be the sum of two independent fair six-sided dice. Then:

`X_i in {2,...,12}`

The single-component weight function is:

`W(k)=6-|7-k|`

The single-component probability is:

`P(X_i=k)=W(k)/36`

For a TPW state:

`x=(x1,x2,x3) in {2,...,12}^3`

the joint weight and probability are:

`W(x)=W(x1)W(x2)W(x3)`

`P(x)=W(x)/36^3`

## 2. Closure theorem

The state space contains `11^3=1331` states. The corresponding raw dice-outcome space contains `36^3=46656` equiprobable primitive outcomes.

Because each one-dimensional 2d6 distribution sums to 36, the independent product distribution sums to:

`(36/36)^3=1`

The validation report confirms the total joint probability exactly as `1/1`.

## 3. Simplex normalization

For each state define:

`S=x1+x2+x3`

`p_i=x_i/S`

Then:

`p1+p2+p3=1`

The normalized vector therefore lies in the closed two-simplex. This normalization is non-injective; the raw tuple and `S` must remain attached to every normalized point for auditability.

## 4. Ternary projection

Using vertices:

`V1=(1/2,sqrt(3)/2), V2=(0,0), V3=(1,0)`

the projected coordinates are:

`X=0.5*p1+p3`

`Y=(sqrt(3)/2)*p1`

The centroid `(1/3,1/3,1/3)` maps to:

`(1/2,sqrt(3)/6)`

## 5. Center collapse theorem

If `x1=x2=x3=a`, then each `p_i=a/(3a)=1/3`. Therefore every equal triple maps to the geometric centroid.

There are 11 such triples: `(2,2,2)` through `(12,12,12)`.

Only `(7,7,7)` is the probabilistic core, because `W(7)` is the unique maximum single-component weight.

## 6. Maximum probability theorem

Because the joint probability is a product of non-negative component weights and the single-component weight is uniquely maximized at `7`, the unique maximum joint-probability state is `(7,7,7)`.

## 7. Symmetry proposition

Permuting `(x1,x2,x3)` preserves:

- sum `S`
- joint weight
- joint probability
- entropy of normalized composition
- barycentric distance from centroid
- Cartesian distance from centroid

Dice reflection `rho(k)=14-k` preserves single-component weights and probabilities, but does not generally preserve simplex position because the normalized proportions and total `S` may change.

## 8. Distance identity

Let:

`d_B^2=sum_i (p_i-1/3)^2`

and let `d_E` be Euclidean distance after ternary projection. Algebraic expansion gives:

`d_E^2 = (1/2)d_B^2`

The validation report records the maximum numerical identity error over all 1331 rows.

## 9. Entropy status

The entropy functional:

`H(p)=-sum_i p_i log2(p_i)`

is maximized at the normalized centroid `(1/3,1/3,1/3)` under the simplex constraint. This is standard but remains marked as a citation/proof-expansion gap for publication-grade release.

## 10. Ring and well-status control

Geometric rings are finite level sets of the selected distance metric. Probability contours are finite level sets of joint probability or log probability.

These are distinct structures. Radial distance from the simplex centroid alone does not globally order joint probability, because probability depends on absolute proximity of each raw component to `7`, not only normalized proportion.

## 11. Spiral status control

Spiral behavior is not a raw-state theorem. It can be demonstrated only after imposing an ordering or parameterization over selected states or rings.

## 12. Current locked artifact result

TPW-001 now exists as the canonical enumeration dataset. Downstream proof objects should derive from it rather than from partial examples.

## v1_1 Governance Addendum

This proof pack is now governed by the following higher-control artifacts:

```text
00_Canonical_Control/NBT-000_Canonical_Scope_and_Proof_Control_Charter.md
03_Control_Registers/NBT-001_Falsification_Register.md
03_Control_Registers/NBT-004_Claim_Evidence_Matrix.md
04_Raphael_Equation_Audit/RAP-001A_Symbol_Governance_Table.md
04_Raphael_Equation_Audit/RAP-001_Canonical_Equation_Register.md
04_Raphael_Equation_Audit/RAP-004_Correspondence_Matrix.md
02_Proof_Appendices/APP-H_Mathematical_Verification_and_Literature_Concordance.md
```

Any Raphael-side physical interpretation is subordinate to RAP-004 and remains hypothesis/analogy unless separately audited.
