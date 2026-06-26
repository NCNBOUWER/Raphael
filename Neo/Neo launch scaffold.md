# Neo launch scaffold

Purpose: prepare Neo as the future high-frequency stewardship and distribution layer without activating the deferred Z stack.

## Status

Neo is scaffolded, not fully launched as a separate automation. A separate Neo 12x-daily automation was requested but could not be created because the active automation limit has been reached. Until a slot is freed, Achilles automations carry Neo-prep tasks inside their prompts.

## Intended cadence

- Neo target cadence: 12 check-ins daily, evenly spread, equivalent to every two hours.
- Current interim: Achilles Continuity Check and Achilles Task Executor include Neo-prep review.
- Z stack operators: future two check-ins daily per operator after explicit launch.

## Role

Neo coordinates canonical file-set launch work across:

- LightSpeed;
- Raphael;
- Achilles;
- Library;
- Investor;
- dashboard queues;
- workbook queues;
- archive queues;
- asset queues;
- route proof queues;
- agent handoff queues.

## Activation gates

Neo may be activated as a separate automation only when:

1. an active automation slot is freed or account limit changes;
2. the current Achilles stack remains represented;
3. `Neo/Queues/file_extension_queues.json` exists;
4. `Neo/Agents/agent_distribution_plan.json` exists;
5. Z stack activation remains explicitly excluded unless separately approved.

## Launch prompt draft

Run Neo stewardship. Review canonical files, extension queues, task deltas, dashboard configs, asset manifest, workbook collapse plans, archive registers, and agent distribution plans. Execute safe file/register updates. Prepare launch-ready handoffs for subagents. Do not activate Z stack operators unless explicitly launched.

## Current blocker

Active automation limit prevents adding Neo as a new separate scheduled task at this pass.
