# Omnicompounded Barycentric Well

## Definition

The **Omnicompounded Barycentric Well** (OBW) is a bounded geometric matrix for mapping `K` weighted variables into a regular or irregular vertex container.

For weights `x=(x_1,...,x_K)`, `x_i>0`, define:

```text
S = sum_i x_i
p_i = x_i / S
sum_i p_i = 1
```

Given vertices `v_i in R^d`, the OBW coordinate is:

```text
X_OBW = sum_i p_i v_i
```

This is the centre-of-mass map for the system.

## Theorem 1 — Closure

If `x_i>0` and `S=sum_i x_i`, then:

```text
sum_i p_i = sum_i (x_i/S) = (sum_i x_i)/S = 1.
```

Proof class: **P1 / PR-1**.

## Theorem 2 — Convex containment

If `sum_i p_i=1` and every `p_i>=0`, then:

```text
X_OBW = sum_i p_i v_i
```

is a convex combination of vertices. Therefore `X_OBW` is inside the convex hull of `{v_i}`. This is the OBW hard wall: a valid closed state cannot leave the container unless a weight is negative, undefined, or closure is broken.

## Regular polygon map

For a regular `K`-gon on a unit circle:

```text
v_i = (cos(2πi/K), sin(2πi/K))
X_OBW = sum_i p_i v_i
```

Equal weights imply `p_i=1/K`, and symmetry gives:

```text
sum_i v_i = 0
X_OBW = 0.
```

The equilibrium hub lies at the polygon centre.

## Dice specialisation

For `K` independent two-dice sum variables, each variable has mode `7`. Therefore the product-measure mode is:

```text
(7,7,...,7)
```

The normalised contribution vector is:

```text
p_i = 7/(7K) = 1/K
```

so it maps to the OBW centre. This proves the dice-to-OBW centrality result without invoking Raphael physics.

## Shape expansion

| Geometry | Variables | Container role |
|---|---:|---|
| Triangle | 3 | First non-degenerate 2D OBW. |
| Square | 4 | Four-variable polygonal well. |
| Pentagon to icosikaihenagon | 5-21 | Increasingly circular discrete approximations. |
| Circle | Limit `K -> infinity` | Prime continuous boundary for many-variable systems. |

The circle is the high-variable prime view because a regular polygon converges to a circular boundary as `K` grows.

## Irregular and asymmetric OBW

Fascicle II permits two equivalent mapping modes:

1. **Regular boundary, irregular distribution:** keep `v_i` symmetric and allow `p_i` to vary.
2. **Irregular boundary, regularised distribution:** vary `v_i(x^mu)` and use a reference distribution to isolate boundary deformation.

Both modes preserve closure. The difference is interpretive: one attributes structure to probability; the other attributes structure to geometry.

## CMB/asymmetry note

For cosmological use later, the CMB can be treated as an empirical irregular boundary map. In Fascicle II this remains an architectural/correspondence object, not a proof of the Raphael physical equation set.
