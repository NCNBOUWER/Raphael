# Raphael Suite call surface

Purpose: define future callable interfaces between N^3 / GeoMatrices and Raphael without building Raphael Lite yet.

## Current status

Raphael Suite is a Markdown call registry only. It is not Raphael Lite and does not implement the complete Raphael core.

## Future call groups

| Call group | Intended function | Current status |
|---|---|---|
| `get_raphael_equations()` | return approved equation IDs and exposed expressions | registry only |
| `map_to_closure()` | map raw components into closed barycentric state | available through N^3 code |
| `map_to_obw()` | map closed state into OBW coordinate | available through Fascicle II code |
| `map_to_mmb()` | aggregate observer/function projections | available through Fascicle II code |
| `map_to_raphael_term()` | crosswalk N^3 proof modules to Raphael terms | Fascicle III registry |
| `evaluate_claim_status()` | classify support/constrain/falsify/empirical requirement | Fascicle III registry |
| `get_fidelity()` | compute internal fidelity from proof dependencies | Fascicle III registry |
| `get_eml_reference()` | point to EML#F where derivation catalogue is needed | external pointer only |

## Raphael Lite deferral

Raphael Lite will be built only after Fascicles I-III are complete and after the final `Raphael_Physics` / GeoMatrices folder pipeline is updated. Until then, this file prevents placeholder responses by naming the expected future calls and returning concrete boundaries.
