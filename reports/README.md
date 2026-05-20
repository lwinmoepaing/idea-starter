# reports/

Browser-walkthrough reports + screenshots. Written by `playwalkthrough` after `mvp-execute` ships a build.

## What lands here
- `#NNNN-<slug>-walkthrough.md` — pass/fail of the root plan's `Demo flow`, walked step-by-step in a real browser via the `playwright` MCP, with the deferred `[?]` runtime checks resolved
- `#NNNN-<slug>-screens/` — per-step screenshots referenced by the report (`01-dashboard.png`, …)

Slug + ID thread from `workflow/*/#NNNN-<slug>.md`. Re-running a walkthrough overwrites the report — it reflects the current build, not an append-only log.

## Flow
1. `mvp-execute` ships every phase for an ID → MVP demo-ready, dev server running
2. `playwalkthrough <id>` drives the demo flow in Chromium, screenshots each step, and turns each `[?]` into a real pass/fail here
3. On a broken step it reports + proposes a fix and waits for your go-ahead — the demo is the test, so walk it before pitching
