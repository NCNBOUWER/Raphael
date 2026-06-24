# Expanded TPW and finite N-variable probability proofs

## N-variable object

Let `X_1,...,X_N` be independent 2d6 sum variables with support `{2,...,12}` and count function

```text
n(s)=6-|s-7|.
```

The finite product-measure probability of a state `x=(x_1,...,x_N)` is

```text
P_N(x)=Π_i n(x_i)/36^N.
```

## Normalization

```text
Σ_x P_N(x)
= Π_i (Σ_{s=2}^{12} n(s))/36^N
= 36^N/36^N
= 1.
```

## Unique N-variable mode

Since `n(s)` is uniquely maximized at `s=7`, every product factor is maximized only when `x_i=7`. Therefore

```text
argmax_x P_N(x) = (7,7,...,7).
```

This is a finite probability theorem. It is not, by itself, a mechanical N-body physics theorem.

## Use in N^3

This proof supplies a reusable normalized centrality structure for finite independent 2d6-derived variables. It supports correspondence, constraint, and falsification work against Raphael-side structures without rewriting those structures.
