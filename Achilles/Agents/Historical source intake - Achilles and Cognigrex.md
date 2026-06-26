# Historical source intake - Achilles and Cognigrex

Date: 26 June 2026

Purpose: extract useful agent-system structure from older Achilles / LightSpeed / Operations / Data source files into the current Achilles agent setup.

## Sources inspected

| Source | Repository | Extracted use |
|---|---|---|
| `Achilles` | `achillesromer-coder/LightSpeed` | Workspace hub, tool categories, resource/navigation model |
| `Directory` | `achillesromer-coder/Data` | Repeated datahub structure and W1-W6 workspace taxonomy |
| `W2; GOS` | `achillesromer-coder/Operations` | Ops tracker layout, active/recent/queued/log/connection pattern |
| `W6; PAL` | `achillesromer-coder/Data` | Dataspace master-contract principles and source-of-truth structure |

## Extracted workspace taxonomy

| Workspace | Name | Current Achilles use |
|---|---|---|
| W1 | Deposit Analysis | Archive/source intake, data characterization, target/source extraction |
| W2 | Luke II Catch / Hold | Task execution queue and operations tracker pattern |
| W3 | RFS & EMFF | Keep as historical technical stream; do not confuse with EML#F |
| W4 | Supply Chain & Trajectory | Handoff, route, dependency, and throughput mapping |
| W5 | Mission Planning GMAT | Scheduling, run windows, and validation sequencing |
| W6 | Asset Library Dataspace | Canonical source registry, normalization, QA, publishing, pass-off packs |

## Extracted tool/resource pattern

Older LightSpeed/Data sources define a hub pattern with calculators, simulators, library, GMAT interface, Achilles AI, Docs/Governance, Dash, and workspace dataspace links. Current Achilles should preserve this as a broad navigation model, not as a Raphael-only model.

## Extracted ops tracker pattern

The Operations source uses a visible three-column execution layout:

1. Active tasks.
2. Recent completions.
3. Mission log / connections.

Current Achilles responses and registers should continue to use:

- active tasks;
- recent completions;
- queued work;
- blockers;
- logs;
- cross-stream dependencies.

## Extracted W6 dataspace principles

The W6 PAL source establishes a canonical dataspace contract pattern:

- contract metadata;
- source-of-truth list;
- embed rules;
- source registry;
- pipeline configuration;
- taxonomy rules;
- normalization rules;
- QA rules;
- publish rules;
- workspace responsibilities;
- queues;
- handoff contracts.

Current Achilles should use these as the backbone for archive-data amalgamation and workbook collapse.

## Current implementation updates

This intake supports:

- `Achilles/Agents/Achilles Assistant Agent.md`;
- `Achilles/Agents/Cognigrex steady stream.md`;
- `Achilles/Workbooks/Workbook collapse controller.md`;
- `OPEN_TASKS.csv` task routing.

## Boundary

This is extraction and consolidation only. It does not start the deferred Z stack and does not assert that historical placeholder metrics are current operational values.
