# Fascicle II proof map

Scope: **Fascicle II — classical-physics analysis and architectural geometry for Raphael GeoMatrices**.

This fascicle builds from Fascicle I, but does not replace it. Fascicle I supplies the finite probability base. Fascicle II generalises the base into bounded geometry, observer decomposition, irregular geometry, and transport/covariant correspondence. Fascicle III will later perform the Raphael-specific integration.

## Canonical inheritance from Fascicle I

| Inherited object | Imported result | Use in Fascicle II |
|---|---|---|
| 2d6 sum count vector | `[1,2,3,4,5,6,5,4,3,2,1]` | Base finite probability source. |
| Three 2d6 trials | `11^3 = 1331` sum-state triples | Base lattice used for simplex tests. |
| Ordered microstates | `36^3 = 46656` primitive outcomes | Base sample-space volume. |
| Product PMF | `P(a,b,c)=n(a)n(b)n(c)/36^3` | Probability field used by log landscape. |
| Unique product mode | `(7,7,7)` with probability `1/216` | Modal selector for centroid state. |
| Barycentric map | `q_i = x_i / sum(x)` | Closure operator for OBW. |
| Gamma bridge | Piecewise-linear simplex interpolation | Discrete transport seed for Fascicle II. |

## Fascicle II primary objects

| Object | Name | Purpose | Proof class |
|---|---|---|---|
| OBW | Omnicompounded Barycentric Well | Bounded container geometry for K weighted variables. | P1 / PR-1 |
| MMB | Multi-Observer Multi-Function Breakdown | Face-projection/observer-decomposition model. | P2 / PR-3 / PR-4 |
| Covariant bridge | Gauge-corrected barycentric derivative | Preserve closure under local coordinate/shape changes. | PR-1 / PR-4 |
| Irregular geometry | Regular distribution vs irregular boundary dual | Model asymmetry without breaking closure. | P1 / PR-4 |
| RG/coarse graining | Micro-to-macro limit of bounded maps | Show convergence of high-K systems toward centre. | PR-2 / PR-4 |

## Build-mode claim classes

Fascicle II proves the following inside its stated mathematical assumptions:

1. **Closure preservation:** for positive weights `x_i`, `p_i=x_i/sum(x)` gives `sum(p_i)=1`.
2. **Convex containment:** any OBW point `X=sum(p_i v_i)` lies inside the convex hull of vertices `v_i`.
3. **Regular polygon centre:** equal weights map to the geometric centre of a centred regular polygon.
4. **Product-mode inheritance:** for independent identical 2d6 sources, all equal-to-seven vector states are the unique product-measure modes at their respective K.
5. **Observer averaging neutralisation:** independent observer maps in MMB reduce single-observer bias as observer count increases under equal or bounded weighting.
6. **Closure-preserving derivative:** the projected derivative `D_i = raw_i - p_i sum(raw)` satisfies `sum(D_i)=0` whenever `sum(p)=1`.

Fascicle II supports, but does not by itself externally validate, the following correspondences:

- classical phase-flow analogy,
- non-locality visualisation by face projection,
- CMB/asymmetric-boundary map analogy,
- future Raphael covariance/integration hooks.

## Minimum entry requirements

| Requirement | Minimum | Reason |
|---|---:|---|
| Variables / vertices | `K >= 3` | A non-degenerate 2D closed polygonal well requires at least three vertices. |
| Event outcomes | `N >= 3` | A binary event is a line segment; curved or polygonal internal field structure begins at three outcomes. |
| Positive weights | `x_i > 0` | Required for normalised contribution mapping by `sum(x)`. |
| Observer count for MMB | `M >= 2`, preferred `4-6` | At least two observers are required for comparison; 4-6 supports polyhedral face mapping. |

## Hard limits

- OBW does not make independent random trials physically influence each other.
- Historical trajectories can estimate empirical drift but do not change the exact probability of a fair future die roll.
- MMB is a structural/visual and statistical observer model unless tied to a formal physical experiment.
- Raphael equations remain fixed; Fascicle II provides architecture, crosswalks, and tests.
- EML Function belongs to `EML#F` as a separate source/library and is not EMFF/RFS.
