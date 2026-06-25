# Equation exposure register

Purpose: record which Raphael/GeoMatrices equations are allowed to appear in Git and how they are used.

Decision: exact equations may be displayed in Git. They remain source-governed; Fascicle III may crosswalk and test them, but must not rewrite them.

## Exposed equations

| ID | Equation / expression | Role | Editable? |
|---|---|---|---|
| EQ-CL-001 | `S=sum X_n; p_n=X_n/S; sum p_n=1.0` | closure law | no |
| EQ-DER-001 | `D_mu p_n = partial_mu p_n + [A_mu^n + T_mu_nu partial^nu v_n] p_n` | covariant barycentric derivative | no |
| EQ-LOG-001 | `L(p)=log10(P_joint+10^-5)` | non-linear field/log landscape | no |
| EQ-LAP-001 | `nabla^2 L(r)=-4 alpha` near centroid | equilibrium curvature statement | no |
| EQ-TOE-001 | `Psi_ToE = integral_over_simplex((nabla^d Psi_in) exp(i integral g_QG dt')) dV_4` | master overlapping event solver | no |

## Exposure rules

1. Equations can appear in Git documentation.
2. Equations are treated as fixed source objects.
3. Git files may create adapters, tests, crosswalks, and failure criteria.
4. Git files may not silently alter equation meaning.
5. Any later correction must be a named source-governed revision, not an untracked rewrite.

## Relationship to Raphael Lite

Raphael Lite is deferred. The current build may define a Raphael Suite call surface, but not a runtime implementation of the complete Raphael core.
