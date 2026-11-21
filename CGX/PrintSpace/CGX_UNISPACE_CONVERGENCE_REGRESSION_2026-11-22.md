# CGX / UniSpace / PrintSpace — consolidation and regression receipt (2026-11-22)

**Scope:** Additive, source-linked review implementation on existing Raphael PrintSpace PR #6.
**Status:** **DIGITAL SOFTWARE CI PASS; PHYSICAL / NETWORK ACCEPTANCE NOT CLAIMED.**
**No source master merge, mint, public publication, printer control, signed two-node interoperability, automatic payment, or live radio handover is claimed.**

## Evidence: reproducible GitHub Actions run

- Repository / draft PR: [NCNBOUWER/Raphael PR #6](https://github.com/NCNBOUWER/Raphael/pull/6)
- Verified branch-head commit: `a11ae2cbfd1750f7a5ef6cb021f1cde7920a5062`
- Workflow: `PrintSpace data and candidate routing checks`
- [Run 44962013660](https://github.com/NCNBOUWER/Raphael/actions/runs/44962013660) / job `137022695567`
- GitHub status: **completed / success**.
- Existing regression step: **84 tests run; OK (skipped=1)**.
- New `test_cgx_convergence_regression.py` step: **14 tests run; OK**.
- **Combined counted result: 98 tests, 97 passes, one optional skip, zero known failures.**
- Compilation, offline demo build, adaptive preview and artifact upload steps completed successfully.
- CI revision pins the geometry checkout to `4ffebc85b1f945b83359c824c2165a98eb036c86` (Raphael PR #7); its source is independent and is not merged into PR #6.
- Future runs must verify CURRENT checkout head and receipts anew. This document is a dated receipt, not an always-current quality status.

## Noncompeting source-linked implementation

| Component | Role | Governance |
|---|---|---|
| `cgx_printspace_shell.py` | Deterministic JSON binary baseline → reversible 6-trit-per-byte base-3 carrier → review-only T173 lookup → capability/dependency/rights plan → safe revision proposal | no hardware actuation, release or claimed compression |
| `cgx_printspace_t173_projection.py` | Read-only PR #7 reference-mesh role/alias crosswalk, with explicit missing slots and source hash references | no second geometry master or mint |
| `cgx_unispace_link_policy.py` | Stateless decision policy for verified warm LAN / Wi-Fi Direct / Bluetooth links and safe offline HOLD | no radio pairing, transmission, real authentication or lease transfer |
| `test_cgx_convergence_regression.py` | 14 scenarios: reversible bytes, invalid trits, alias and sentinel, bounded geometry coverage, DAG/cycles, rights, directionality, safe checkpoint, transport trust/freshness and expiry | synthetic and source-review test fixtures |
| `.github/workflows/printspace-data-tests.yml` | Pinned source data checkout and converged regression in existing CI | review-branch integration only |

**Single umbrella:** UniSpace is the product; FileSpace owns portable CGX source/identity/persistence; DataSpace conveys separately authenticated peer coordination and receipts; PrintSpace resolves geometry/material/process instructions via qualified machine capabilities. Agent identities remain independent of nodes and devices; remote compute may supply plans, not unchecked motor commands.

## Reconciled evidence and gaps

- T173 is **173 slot roles, not 173 unique independently printable solids**. Reviewed PR #7 data: **131 numeric Euclidean reference meshes + 9 shared aliases = 140 mesh-backed role slots; 33 roles remain without attached reference meshes**. Reserved **174** is empty, nonmintable.
- Unresolved geometry groups in this source snapshot: slots **131–143**, **152–155**, and **158–173**. The seven Raphael-proposed roles at 131–137 and remaining complex/nonconvex references need explicit source and geometry evidence.
- The Euclidean mesh reference is **not** a proven Raphael metric, validated print-scale surface, 4D-material interface or manufacturing qualification.
- PrintSpace candidate registry: **30 parametric geometry seeds, zero marked machine-ready**.
- Pairwise sequence model: **14 families × 14 = 196 ordered family pairs**; all remain production-unapproved.
- Directed material candidates: **72 directional routes**, zero production-approved.
- The handoff planner can distinguish existing machine capability, candidate first-manufactured tool, and external capability. It does **not** prove that a tool can be built or that a mobile/watch/phone/AI pet can be printed for material cost plus any proposed fee.
- The T173 join is an **implemented derived read-only crosswalk**, not a new canonical authority. The original full workspace/source workbooks have not all been independently reconciled.
- The trit codec expands one byte to six trits; it is **lossless radix representation, NOT a measured compressed file format**. FileSpace must benchmark or select an existing carrier separately.
- Transport selection uses signed-readback flags supplied *by the prospective adapter*; there is **no cryptographic pairing implementation**, no observed real Wi-Fi outage, no Bluetooth throughput result, no failover latency or actual two-node lease receipt.
- In-print revision is a proposal only. A DataSpace mutation needs signed root/readback, monotonic sequence, scope/rights, evidence, independent operator and safe machine checkpoint. Completed layers are immutable.
- Distribution policy: one source-linked object may have rights-cleared OPEN facets and paid recipe/qualification rights; no unreviewed patents/licenses, billing or commercial warranty implied.

## Entry/exit gates: remaining

1. **Source:** confirm current FileSpace Object_ID / State Root / DBR Root, PR #7 mesh catalogue revision, rights/aliases, original data owners and source root; do not promote derived projections.
2. **Geometry:** supply 33 absent Euclidean references or explicit unsupported classifications; prove face incidence/closed volumes, legal unitful dimensional scale, stacked/contact geometry and manufacturing tolerances; reconcile historical QA states.
3. **Materials:** independent directional A→B versus B→A coupons, layer bonds, surface treatments (roughening vs plating), thermal/chemical exposure budgets, atmosphere and encapsulation.
4. **Device:** authenticated calibrated PrintCeptor capability profile, real tool availability, verified interlocks; prove any 'build special tool first' chain, not merely a candidate label.
5. **Network/offline:** signed two independent nodes, pre-authorized link handover, readback counter/fencing, split-brain, stale leases and physical safe-stop tests; BLE is not presumed adequate for large mesh/toolpath transfers.
6. **Commercial:** rights-cleared open reference library, separate validated paid recipes and payment authorization. No customer production authorization from software regression alone.
7. **Release:** owner review of PR #6 and PR #7, independent acceptance of native root/DBR and safety, then controlled integration. Do not merge or publish on this receipt alone.

**No further competing scheduler/master/agent was introduced.** Future changes must be tests-first and source-bound, with binary baseline → reversible ternary conversion where appropriate → T173 geometry reference → conventional device instructions under hardware authority.
