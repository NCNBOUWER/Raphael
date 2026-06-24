# Data

The authoritative generated enumeration is included in the local final source package as `Master_Enumeration.csv`.

For GitHub text review, regenerate/check the finite data from code:

```bash
python3 RUN/code/geomatrix_master.py --validate
```

The validation invariant is:

```text
sum-state rows = 1331
primitive ordered outcomes = 46656
probability sum = 1
unique mode = (7,7,7)
```

Large generated data may be regenerated rather than manually edited.
