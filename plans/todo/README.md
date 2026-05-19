# plans/todo/

Phase files waiting to ship. Written by the `phase-writer` sub-agent during `mvp-plan`.

## File format

`#NNNN-NN-<slug>.md` — one per phase. Contains: goal, blocked-by, parallel-safe-with, effort (S/M/L), modules, interfaces, state shape, routes, interactions, mock data, MVP shortcuts (deliberate), done-when checklist.

## Shipping

`mvp-execute` auto-`mv`s each phase to `../done/` after its `phase-executor` reports done-when passes. By hand: `mv plans/todo/#NNNN-NN-<slug>.md ../done/` — keep the filename so the root plan's links stay valid. Phase numbers and slugs don't change.
