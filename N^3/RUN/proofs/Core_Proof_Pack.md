# Core Proof Pack

## Object

Let each variable be the sum of two fair six-sided dice. The support is

```text
S = {2,3,4,5,6,7,8,9,10,11,12}
```

The count of ordered outcomes producing sum `s` is

```text
n(s) = 6 - |s - 7|.
```

Thus the count vector over sums `2..12` is

```text
1,2,3,4,5,6,5,4,3,2,1
```

and `sum_s n(s)=36`.

## Three-variable TPW product space

For three independent 2d6 sum variables, the sum-state space has

```text
11^3 = 1331
```

rows, while the primitive ordered dice-outcome space has

```text
36^3 = 46656
```

primitive outcomes.

## Joint probability

For state `(a,b,c)`:

```text
P(a,b,c)=n(a)n(b)n(c)/36^3.
```

Normalization follows directly:

```text
Σ_{a,b,c} n(a)n(b)n(c)/36^3
= (Σ_a n(a))(Σ_b n(b))(Σ_c n(c))/36^3
= 36^3/36^3
= 1.
```

## Unique mode theorem

Because `n(s)` is uniquely maximized at `s=7`, the product `n(a)n(b)n(c)` is uniquely maximized at `(7,7,7)`.

Therefore:

```text
P(7,7,7)=6^3/36^3=216/46656=1/216.
```

## Minimum class

The minimum count occurs at `s=2` and `s=12`, with `n(s)=1`. Therefore the minimum-probability triples are the eight corner states with each coordinate in `{2,12}`:

```text
P_min = 1/46656.
```

## Barycentric distinction

The barycentric coordinate map uses positive weights such as `n(s)` and normalizes:

```text
b(a,b,c) = (n(a),n(b),n(c))/(n(a)+n(b)+n(c)).
```

All equal triples `(s,s,s)` map to `(1/3,1/3,1/3)`. Thus barycentric centroid membership is not equivalent to probability-mode uniqueness.

Correct statement:

```text
(7,7,7) is the unique probability-selected member of the equal-triple centroid set.
```

## Proof status

| Claim | Status |
|---|---|
| finite enumeration | proven |
| joint PMF | proven |
| normalization | proven |
| unique mode `(7,7,7)` | proven |
| minimum corner class | proven |
| barycentric centroid distinction | proven |
| physical field-equation proof | not claimed |
