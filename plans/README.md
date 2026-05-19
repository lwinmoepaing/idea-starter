# plans/

MVP build plans, phase-by-phase. Written by `mvp-plan` (orchestrator) + `phase-writer` (sub-agent, N in parallel). One plan per feature drop; `done/` accumulates phases across every drop as the product grows.

## Layout
- `#NNNN-plan-root.md` — parent: idea summary, demo flow, phase DAG, parallel groups, critical path, assumptions
- `todo/#NNNN-NN-<slug>.md` — one file per phase (goal, modules, state shape, MVP shortcuts, done-when)
- `done/` — phases moved here after they ship

## Conventions
- `NNNN` = workflow ID (matches `workflow/*/#NNNN-*.md`)
- `NN` = phase order (`01`, `02`, …)
- slug = per-phase, kebab-case (`design-system`, `dashboard`, `polish`)

## Execution

`mvp-execute` walks the DAG: spawns `phase-executor` for each runnable phase, fans out parallel-safe groups, `mv`s files to `done/` as they ship, pauses between groups for dev-server checks. By hand: run phases in dependency order per the root plan, then `mv plans/todo/<file>.md plans/done/`. All in `done/` → MVP demo-ready.

## Scope

Pitch-demo only. React + RR + Zustand fake-DB, happy path. No real auth/backend/tests. See `.claude/skills/mvp-plan/SKILL.md`.
