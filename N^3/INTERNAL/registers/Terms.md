# Terms

Purpose: shared terminology and call surface for all N^3 fascicles, GeoMatrices, Raphael crosswalks, and smoke tests. This file is intentionally concise, canonical, and reusable. It is not a proof document by itself.

## Naming rules

- File and folder names use clear plain-language names.
- Capitalise only the first word unless the term is a fixed acronym or established project name.
- Avoid version numbers in front-facing titles.
- Keep source-specific work in its own folder until the final GeoMatrices merge.

## Project hierarchy

| Term | Canonical meaning | Build status | Notes |
|---|---|---:|---|
| N^3 | The total project/findings/system for the three-fascicle build. | Active | Holds Fascicles 1-3 as build logs before final GeoMatrices merge. |
| Fascicle I | Mathematics and probability layer. | Built | Contains Trinity Probability Well and finite product-measure proofs. |
| Fascicle II | Classical-physics analysis and architectural-geometry layer. | Build next | Formalises OBW, MMB, transport, bounded geometry, and classical correspondence tests. |
| Fascicle III | Raphael integration layer. | Deferred | Uses Fascicles I-II to support, constrain, and test Raphael. |
| GeoMatrices | The eventual unified folder/system after all fascicles are complete. | Future merge | Not a single fascicle; the final merged operational framework. |
| Raphael | Broader fixed framework/equation set. | External core | Treated as complete and source-governed, not rewritten by N^3. |
| Raphael Lite | Minimal future runtime/callable subset of Raphael. | Deferred | Do not build until after all three fascicles are complete. |
| Raphael Suite | Housing/call surface for future Raphael references and integration points. | Deferred | Replaces all-caps housing terminology. |
| EML#F | Separate folder for the EML Function source work. | Separate | Not EM Function, EMFF, or RFS. |

## Core mathematical terms

| Term | Canonical meaning | Proof relation | Smoke-test expectation |
|---|---|---:|---|
| Trinity Probability Well | Finite probability-geometric model over three independent 2d6 sum variables. | P0/P1 | Returns count vector, support, PMF, mode, normalization. |
| 2d6 sum variable | Sum of two fair six-sided dice with support 2-12. | P0 | Returns counts `[1,2,3,4,5,6,5,4,3,2,1]`. |
| Primitive ordered outcomes | Ordered microstates for three independent 2d6 variables. | P0 | Returns `36^3 = 46656`. |
| Sum-state triples | Triples of observed sums `(a,b,c)` over support 2-12. | P0 | Returns `11^3 = 1331`. |
| Product PMF | `P(a,b,c)=n(a)n(b)n(c)/36^3`. | P1 | Sums exactly to `1`. |
| Modal triple | Unique maximum-probability triple. | P1 | Returns `(7,7,7)` and probability `1/216`. |
| N-variable product mode | Finite independent N-variable extension. | P1 | Returns `(7,...,7)` as unique product-measure mode. |
| Barycentric map | Normalised coordinate embedding into the simplex. | P1/P3 | Returns simplex coordinates summing to `1`. |
| Centroid set | Equal-triple set mapping to barycentric centre. | P1 | Returns 11 equal triples, not only `(7,7,7)`. |
| Modal-centroid selector | Product probability selects `(7,7,7)` from centroid states. | P1 | Returns unique probability-selected centroid member. |
| Gamma bridge | Piecewise-linear trajectory interpolation through simplex states. | P1/P3 | Returns bounded interpolation, not physical field proof. |

## Fascicle II GeoMatrices terms

| Term | Canonical meaning | Build use | Proof boundary |
|---|---|---|---|
| Omnicompounded Barycentric Well | OBW; bounded, compounded barycentric container/well geometry. | Fascicle II primary object | Prove closure/containment before physical claims. |
| Multi-Observer Multi-Function Breakdown | MMB; observer-decomposition and multi-function mapping system. | Fascicle II primary object | Test variance/error behaviour; do not assume physical realism. |
| Bounded container | A finite or normalised domain whose mapped states must remain within admissible bounds. | OBW | Failure condition: mapped states escape boundary. |
| Observer decomposition | Multiple mapped views/functions over the same base state. | MMB | Must preserve source state identity and map definitions. |
| Classical correspondence | Mapping between finite geometry/transport and classical physics language. | Fascicle II | Correspondence/support unless independently proven. |
| Covariant transport | Transport-like language over mapped state sequences or fields. | Fascicle II | Start from discrete transport; tensor/field use requires explicit map. |
| Discrete-to-continuous bridge | Extension of Gamma bridge into controlled classical analysis language. | Fascicle II | Interpolation/trajectory proof only unless additional physics is proven. |

## EML Function terms

| Term | Canonical meaning | Boundary |
|---|---|---|
| EML Function | Third-party EML operator/work to be used as a source, catalogue, and derivation-library analogue. | Separate from N^3 until later merge. |
| EML operator | `eml(x,y)=exp(x)-ln(y)`. | Grammar/syntax, not a physical law by itself. |
| EML grammar | Binary-tree expression grammar for reduced model discovery. | Methodological source. |
| Activation-suppression module | Depth-one EML-generated non-monotone response module. | Useful analogue for hidden/adaptive dynamics. |
| EML cascade | Solvable feedforward hierarchy with hidden depth and convolution structure. | Candidate catalogue logic; not Raphael proof. |

## Raphael interaction terms

| Term | Canonical meaning | Boundary |
|---|---|---|
| Raphael equations | Fixed private/source-governed equation set. | Refer, crosswalk, constrain; do not rewrite. |
| Raphael bridge | Minimal adapter interface for future Raphael linkage. | Current placeholder boundary. |
| Raphael Lite | Future callable subset/suite to be built after all fascicles. | Deferred. |
| Crosswalk | Relation map between N^3 structures and Raphael terms. | Support, constrain, or disprove; not automatic proof. |
| Falsification register | File/register listing failure conditions. | Required before claim promotion. |
| Open tasks | Live task register; replaces static citation-register approach. | Tasks are removed/closed when completed. |

## Proof classes

| Code | Meaning |
|---|---|
| P0 | Exact finite enumeration/direct counting. |
| P1 | Algebraic derivation from defined objects. |
| P2 | Computational verification. |
| P3 | Geometric/compositional visualisation. |
| P4 | Analogy/correspondence. |
| P5 | Hypothesis / source-governed / unsupported as proof. |
| PR-0 | Exact identity. |
| PR-1 | Direct finite proof. |
| PR-2 | Derived consequence. |
| PR-3 | Computational verification. |
| PR-4 | Structural correspondence. |
| PR-5 | Analogy / visualisation. |
| PR-6 | Hypothesis only. |
| PR-X | Blocked / disproved relation. |

## Fidelity scale

| Score | Meaning |
|---:|---|
| 100% | Mathematically proof-locked within stated assumptions. |
| 110% | Proof-locked and corroborated by a second internal proof path. |
| 200% | Empirically validated. |
| 250% | Empirically validated by an additional independent empirical method. |

## Smoke-test call surface

Use these names in future tests and runners so they return concrete project data instead of placeholders.

| Call name | Expected return |
|---|---|
| `get_project_scope()` | `N^3 = Fascicles I-III; GeoMatrices = future unified merge.` |
| `get_fascicle_status()` | Fascicle I built; Fascicle II next; Fascicle III deferred. |
| `get_core_tpw_facts()` | `1331`, `46656`, `(7,7,7)`, `1/216`, `1/46656`. |
| `get_terms_registry()` | This file's canonical glossary. |
| `get_proof_classes()` | P0-P5 and PR-0-PR-X tables. |
| `get_fidelity_scale()` | 100/110/200/250 scale. |
| `get_raphael_boundary()` | Raphael equations fixed; N^3 crosswalks/supports/constrains/disproves only. |
| `get_eml_boundary()` | EML#F is separate third-party source/library; not EMFF/RFS and not proof of Raphael. |
| `get_fascicle_ii_objects()` | OBW, MMB, bounded container, observer decomposition, classical correspondence, covariant transport. |
| `get_open_tasks()` | Current OPEN_TASKS register. |

## Hard exclusions

- Do not call EML “EM Function”.
- Do not conflate EML with EMFF or RFS.
- Do not build Raphael Lite before Fascicles I-III are complete.
- Do not rewrite Raphael equations to match N^3.
- Do not promote physical claims from P5 without a proof or validation pathway.
- Do not treat EML grammar as a physical interaction law by itself.
