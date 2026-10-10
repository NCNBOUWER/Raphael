# PrintSpace — DBR compaction and live network handoff source crosswalk
**Date:** 2026-10-08 (Brisbane). **Status:** owner-review derivative; no machine runtime, network transfer, compactor, reset, or deletion is deployed. Do not overwrite canonical CGX, DBR, LightSpeed, Raphael, Post-Mix or RootAuthority schemas.

## Founder decisions
- DBR is **Digitally Backed Receipt**. The spoken DBI was a mispronunciation, not a new schema.
- A local-only printer may lose its sole receipt/history copy upon reset. A networked printer can choose full authorised erasure or compact its multiple source DBRs to one network-held DBR.
- For selected compaction, transmit and verify internally, without a routine completion prompt. Successful network acceptance must be independently read back before any local history is cleared.
- If transmission, acknowledgement, integrity check or connectivity fails, preserve every local source DBR and a durable **LIVE_PENDING** handoff across restart. Retry when connection and authority permit, using the same idempotency identity and bounded backoff, until verifiably completed. Never claim transfer occurred while offline.
- Significant quota, storage exhaustion, corrupted data, lapsed authority or security failure remain available to diagnostics, and prompt the owner where necessary. Safety-critical safeguards cannot rely on network access or AI.

## Existing source semantics — READ ONLY, not newest-wins
- [CGX Filespace Comprehensive Manual v0.1](https://docs.google.com/document/d/1obdzmT5xXCNOG8rLAaxciEz1c4UIjQQkWXJFDucFRdE/edit) specifies Object ID, State Root, DBR Root, payload/reference and manifest as minimal object concepts; network replicas compare Object ID, State Root, DBR Root, capability root and last event. Offline reconnection reconciles ancestry instead of simply accepting later timestamps.
- [CGX Filespace Phase A Whitepaper v0.1](https://docs.google.com/document/d/1fxauxq9fZ4L9cLD5aSv_jUCTEqS4yYA0XDORDJGRI-I/edit) describes DBR as the living proof root binding object identity, state root, event head and significant checkpoints. Reproducible representations need not all be retained, but important publication, transfer, legal/archive, approval and qualification boundaries create checkpoints.
- [Achilles CGX/LightSpeed handoff](https://docs.google.com/document/d/1W5BIxf8pm5WTbpjzgYQIlSh39B82Ji-vrgIevAN8pao/edit) retains existing original receipts/source paths and forbids a duplicate orchestration or CGX master. It is not a ratified wire-format.
- [PrintSpace transit queue](TRANSIT_DECISION_GATE_QUEUE_2026-10-08.json) founder decisions D22–D24 remain the specific printer/application requirements; cross-lane authorities have not authorised production implementation.

## Candidate receiver proof (REQUIRES DBR OWNER ACCEPTANCE)
The candidate compacted receipt binds source device **Object ID**, **State Root**, **DBR Root** and event head; deterministic child DBR IDs/count/order/digests and provenance/checkpoints; selected compaction mode, destination identity, authorisation, transaction/idempotency ID and receiver receipt. A separate verification step reads back a durable destination commitment matching the compacted bytes/root and source closure. No receipt field names or hashing/signing algorithms are asserted as canonical until the DBR owner confirms them.

**Compaction is not necessarily backup.** A **recoverable archive** must include its own payload or a fully resolvable authorised content-addressed closure for restoration; a **proof-only compact receipt** can preserve integrity/provenance without retaining all original bytes. These modes must never be marketed as equivalent. Original history that was not preserved or cannot be resolved cannot be reconstructed by assertion.

## Candidate deterministic lifecycle
LOCAL_SNAPSHOT → COMPACTED_LOCAL → LIVE_PENDING → SUBMITTED → DESTINATION_STAGED → ACK_DURABLE → READBACK_VERIFIED → LOCAL_CLEAR_ELIGIBLE → LOCAL_CLEARED.

- **Only READBACK_VERIFIED enables clearing**, subject to the user's selected policy, legal retention and independently protected safety-critical records. Transmission or an unverified ACK is insufficient.
- Offline/disconnected, timed out, crashed, restarted, or negative-ACK handoffs stay **LIVE_PENDING** with intact source receipts and a persistent local outbox.
- Retry with the same idempotency key, no duplicate network receipts; back off to avoid flooding, and reauthorise if consent/lease expires.
- Reject digest mismatch, omitted required child, state/root mismatch, conflicting source ordering, destination mismatch or receiver rollback. Preserve source history and enter diagnostic/retry or owner review.
- Clear cache, clear history, factory reset and archive-then-clear must be distinct operations. Do not silently erase pending receipts through any reset.
- Printed or sourced hardware component substitutions are logged; like-for-like noncritical replacement need not cause full requalification, while containment/safety-critical change has its own independent verification gate.

## Proposed conformance tests (NOT RUN AS DEVICE TESTS)
1. Normal transmission + durable ACK + matching readback → eligible local clear, silent completion.
2. Offline, interrupted, delayed or absent ACK → retained local history and outbox, reconnect retries.
3. Crash and restart in any preverified stage → resume without data loss.
4. Duplicate send / duplicate ACK → one accepted network transaction.
5. Wrong destination digest, missing child or altered state root → no local clear; integrity hold.
6. Expired permission, full local storage, network outage or rejected payload → bounded retry/owner escalation, never false success.
7. Local-only reset warns data can be irretrievable; no implied cloud.
8. Proof-only compaction may not claim it can restore absent source payloads.

## Ownership and concrete open gate
**CGX Filespace/DBR owner:** confirm current canonical receipt structure, cryptographic commitment/ack proof, lineage closure and whether a one-receipt archive is recoverable or proof-only. **LightSpeed:** accept or reject the persistent outbox/retry integration contract, no duplicate bus. **Achilles/security:** legal retention, data-owner authority, local privacy and deletion boundary. **PrintSpace:** apply only approved contract to identified printer instances and prove safety/functional separation.

**Next founder decision, not assumed:** should **one compact network DBR** default to a **recoverable archive of historical records** or a **proof-only summary** (where originals can no longer be restored)? Both could be distinct options, with separately declared consequences.

No independent physical printer, actual network handoff, DBR service, local reset, root promotion or successful runtime conformance is claimed by this document.
