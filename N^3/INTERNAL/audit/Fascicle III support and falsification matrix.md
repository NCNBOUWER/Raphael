# Fascicle III support and falsification matrix

Purpose: harden the Raphael integration layer using the scientific disproof method.

## Falsification logic

For every claim, ask:

```text
What would make this false?
What would make it unsupported?
What exact inherited proof does it rely on?
What empirical test would lift it beyond internal proof?
```

## Matrix

| Claim family | Internal support | Required disproof test | Pass condition | Fail condition | Fidelity ceiling before empirical work |
|---|---|---|---|---|---:|
| Closure claims | Fascicle I normalization | Sum check | `abs(sum(p)-1)<=tol` | closure breach | 110% |
| Mode/centrality claims | product PMF unique mode | enumerate all states | unique max at `(7,...,7)` | non-unique product mode | 110% |
| OBW containment | convex combination proof | point-in-hull / non-negative weights | point remains inside hull | escape from hull | 110% |
| Transport claims | Gamma + derivative tangent | tangent-sum test | `sum(V)=0`, `sum(D)=0` | non-zero closure drift | 110% |
| MMB claims | observer aggregate closure + bias bound | observer bias simulation | bias decreases by observer-count bound | bias amplification under controlled map | 110% |
| Irregular geometry | dual regular/irregular map | residual tolerance | residual bounded | residual uncontrolled | 110% |
| Raphael equation crosswalk | exact equation map + proof dependency | dependency audit | every term has status and failure route | missing dependency | 110% until empirical |
| CMB asymmetry | irregular-boundary representation | empirical residual against CMB data | residual/tolerance accepted | residual/tolerance rejected | <200% |
| Biological trajectory | ATGC compositional closure | dataset closure + trajectory fit | trajectory model predicts/retrodicts | no stable model | <200% |
| Macro-social simplex | fiscal/demographic closure | reproducible source data + residual | stable closure map | non-stationary/unclosed data | <200% |

## Hard stance

Fascicle III is not conservative in purpose. It asserts that GeoMatrices can be used as a universal representational, proof-assistance, validation, and falsification architecture across closed systems. It remains scientific by requiring every elevated domain claim to specify its disproof route.

## Expert and empirical escalation

- 100%: proof-locked within stated mathematics.
- 110%: proof-locked plus corroborating internal proof path.
- 200%: empirical validation by suitable data, method, or qualified party.
- 250%: second independent empirical validation method.
