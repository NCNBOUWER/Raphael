# Irregular geometry and CMB mapping

## Purpose

Fascicle II must account for reality's asymmetry. Regular polygons and regular polyhedra are reference models; natural systems are often irregular.

## Dual map principle

The same observed structure may be represented in two mathematically distinct ways:

1. **Regular geometry with irregular probability:** vertices remain fixed and symmetric; weights carry the irregularity.
2. **Irregular geometry with regularised probability:** weights are regularised; vertices carry the irregularity.

Both maps can describe the same system from different analytical views.

## Equation

Let regular vertices be `v_i` and irregular vertices be `u_i = v_i + δ_i`.

Regular-boundary map:

```text
X_R = sum_i p_i v_i
```

Irregular-boundary map:

```text
X_I = sum_i q_i u_i
```

A calibration is successful when:

```text
||X_R - X_I|| <= tolerance
```

for a defined tolerance and dataset.

## Fractal sub-variable zoom

A component `x_k` can be decomposed into subcomponents:

```text
x_k = sum_a x_{k,a}
p_{k,a} = x_{k,a} / x_k
sum_a p_{k,a} = 1.
```

This nests a smaller OBW inside a vertex/region of a larger OBW.

For dice, this lets the analyst zoom from:

```text
pair-sum state -> individual die one / die two states -> face-level probabilities
```

without changing the parent closure.

## CMB use later

The Cosmic Microwave Background can be treated as an empirical asymmetry field for later Raphael/physics work. In Fascicle II the role is architectural:

- define an irregular boundary map,
- compare it against a regular reference map,
- isolate perturbation potentials,
- record residuals for Fascicle III.

## Failure conditions

The irregular map fails if closure cannot be maintained, the residual cannot be bounded, sub-variable zoom changes the parent value, or the chosen geometry hides rather than isolates asymmetry.
