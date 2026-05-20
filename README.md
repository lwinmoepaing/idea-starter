# idea-starter

Idea-to-MVP scaffolding: drill a problem, hunt unsolicited demand evidence, sketch on a tldraw canvas, build the MVP, then walk its demo in a real browser. Each stage has its own folder.

## Mental model — one product per repo

This repo holds **one product**. Different business → clone the scaffolding into a separate folder.

Inside one repo, IDs are **feature drops on the same product**:

- `#0001` is the first drop — usually the core MVP. Lays down `mvp/`'s scaffold, design system, and the first demoable slice.
- `#0002`, `#0003`, … **extend** `mvp/`. Each has its own `workflow/{ideas,approach,marketing}/#NNNN-*.md` trio, its own `plans/{id}-plan-root.md`, its own phase files.
- `mvp/` keeps growing as IDs ship. `plans/done/` is the running log of every phase that landed.

When `mvp-plan` plans `#0002+`, it reads `plans/done/*.md` across all IDs so new phases extend existing routes/components/store-slices rather than duplicate them.

## Layout

| Folder                  | Purpose                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `workflow/`             | Stage-by-stage evidence for an idea (subfolders below)                                                             |
| `workflow/ideas/`       | Raw idea write-ups — `validate-idea`                                                                               |
| `workflow/approach/`    | Demand-evidence hunt plans — `pain-hunt`                                                                           |
| `workflow/marketing/`   | Pre-launch marketing plans — `marketing-plan`                                                                      |
| `tools/`                | Local dev tools + bootstrap scripts                                                                                |
| `tools/drawing/`        | React + Vite + TypeScript + tldraw v3 canvas                                                                       |
| `tools/scripts/`        | Shell scripts — `setup-mcp.sh` builds project-scope MCPs                                                           |
| `docs/`                 | Specs, Lean Canvas PNGs (`business-canvas`), pitch summaries (`pitch-summary`)                                     |
| `plans/`                | Build plans — `{id}-plan-root.md` + phases in `todo/` → `done/` when shipped (`mvp-plan`)                          |
| `mvp/`                  | Prototype code (Vite + React + RR + Zustand), built phase-by-phase                                                 |
| `reports/`              | Browser-walkthrough reports + screenshots — `playwalkthrough` (`#{id}-<slug>-walkthrough.md`)                      |
| `.claude/skills/`       | Project-local Claude Code skills (table below)                                                                     |
| `.claude/agents/`       | Sub-agents invoked by skills via the Agent tool (table below)                                                      |

Files in `workflow/*/` use `#NNNN-<slug>.md` — `NNNN` is a zero-padded per-folder sequence (start at `#0001`). One ID threads through all three subfolders for one idea.

## Prerequisites

- Node 18+ and npm
- [Bun](https://bun.sh) (used by the tldraw MCP build)
- Git
- [Claude Code](https://claude.com/claude-code) for the skills + MCP

## First-time setup

```bash
git clone <this-repo>
cd idea-starter
bash tools/scripts/setup-mcp.sh   # clones + builds the tldraw MCP into .mcp-servers/
```

`setup-mcp.sh` pulls `bassimeledath/tldraw-render-mcp` (not on npm) and builds it. First run downloads Chromium via Playwright (~150MB). Re-run any time to update.

## Drawing app

```bash
cd tools/drawing
npm install
npm run dev
```

Opens a full-viewport tldraw canvas at the URL Vite prints.

## Claude Code skills (`.claude/skills/`)

| Skill              | What it does                                                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validate-idea`    | Drills problem / user / pain / alternatives → `workflow/ideas/#NNNN-<slug>.md`                                                                       |
| `pain-hunt`        | Plans the unsolicited-demand hunt → `workflow/approach/#NNNN-<slug>.md`                                                                              |
| `marketing-plan`   | Pins one channel + budget + 30-day actions → `workflow/marketing/#NNNN-<slug>.md`                                                                    |
| `business-canvas`  | Reads the three workflow files for an ID, renders a Lean Canvas PNG via the `tldraw` MCP → `docs/#NNNN-<slug>-canvas.png`                            |
| `mvp-plan`         | Reads the workflow + checks `mvp/package.json`, writes `plans/{id}-plan-root.md` + per-phase files in `todo/`. Orchestrates 4 sub-agents             |
| `mvp-execute`      | Walks the plan in DAG order via `phase-executor`, `mv`s shipped phases to `done/`, pauses between groups for dev-server checks. When the last phase ships, spawns `pitch-summary` to write `docs/#{id}-<slug>-pitch.md` |
| `playwalkthrough`  | Drives the built MVP through its root-plan `Demo flow` in a real browser (`playwright` MCP), turns the deferred `[?]` runtime checks into pass/fail with screenshots → `reports/#{id}-<slug>-walkthrough.md`. Run after `mvp-execute`, before pitching |
| `frontend-design`  | Builds distinctive, production-grade UI for `tools/drawing/` and `mvp/` — bold aesthetic, not generic AI defaults                                    |
| `skill-creator`    | Author / iterate skills                                                                                                                              |

Pinned in `skills-lock.json`.

## Sub-agents (`.claude/agents/`)

Workers that skills delegate to via the Agent tool (`subagent_type: <name>`). Keeps the orchestrator's context lean and lets parallelizable work fan out.

| Agent                  | What it does                                                                                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow-reader`      | Reads `workflow/{ideas,approach,marketing}/#NNNN-*.md` for an ID, returns a structured digest + gap list                                                    |
| `scaffold-inspector`   | Inspects `mvp/`, returns framework / router / state / tokens / gaps + a scaffold-phase recommendation                                                       |
| `dependency-mapper`    | Takes phase specs, returns the DAG (blocked-by, parallel-safe, critical path)                                                                               |
| `phase-writer`         | Renders one phase spec → one markdown file. Spawned N-wide in parallel by `mvp-plan`                                                                        |
| `phase-executor`       | Implements one phase: reads `plans/todo/{id}-{NN}-<slug>.md`, writes React/Zustand/RR code into `mvp/`, returns done-when results. Spawned N-wide by `mvp-execute` for parallel-safe groups |
| `pitch-summary`        | Synthesizes the workflow trio + root plan + shipped phases into `docs/#{id}-<slug>-pitch.md` (Story / Idea / Problem / Solution / Purpose). Auto-triggered when an ID's last phase ships |

## MCP servers (`.mcp.json`)

| Server   | Purpose                                          | Source                                                                                  |
| -------- | ------------------------------------------------ | --------------------------------------------------------------------------------------- |
| `tldraw`     | Headless tldraw renderer (PNG/SVG) for agent use      | [`bassimeledath/tldraw-render-mcp`](https://github.com/bassimeledath/tldraw-render-mcp) |
| `playwright` | Headless Chromium to walk the MVP demo (`playwalkthrough`) | [`microsoft/playwright-mcp`](https://github.com/microsoft/playwright-mcp) — `@playwright/mcp`, via `npx` |

Project-scope — Claude Code prompts to enable on first open. `tldraw` is built locally by `tools/scripts/setup-mcp.sh` into `.mcp-servers/` (gitignored); `playwright` needs no build — `npx` fetches `@playwright/mcp` on first use (first launch may download Chromium via `npx playwright install chromium`). MCP servers attach only at Claude Code startup, so **restart after editing `.mcp.json`**.

## Typical flow

1. Drop a raw idea into `workflow/ideas/`, or describe it to Claude.
2. `validate-idea` — drills the problem, saves a verdict.
3. `pain-hunt` — plans where to find unsolicited complaints.
4. Sketch UX in `tools/drawing/` (optional, by hand).
5. `marketing-plan` — one channel + budget + 30-day actions.
6. `business-canvas` — renders the Lean Canvas PNG from the workflow trio.
7. `mvp-plan` — decomposes into phases, maps dependencies, writes `plans/{id}-plan-root.md` + per-phase files in `todo/`.
8. `mvp-execute` — walks the DAG: spawns `phase-executor` per runnable phase, fans out parallel-safe groups, `mv`s shipped files to `done/`, pauses for dev-server checks. When the last phase ships, `pitch-summary` drops `docs/#{id}-<slug>-pitch.md` — slide-ready source material. All in `done/` = MVP demo-ready.
9. `playwalkthrough` — drives the finished MVP through the root plan's `Demo flow` in a real browser via the `playwright` MCP, turning the deferred `[?]` runtime checks into pass/fail with screenshots → `reports/#{id}-<slug>-walkthrough.md`. The demo is the test — walk it before pitching.
