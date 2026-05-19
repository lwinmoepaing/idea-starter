---
name: mvp-execute
description: Walk an MVP build plan to completion — read plans/{id}-plan-root.md, execute the phase files in plans/todo/{id}-*.md in dependency order, ship each phase to plans/done/ as it lands. Use whenever the user wants to "build the MVP", "execute the plan", "run the build", "ship phase NN", "make the demo work", or follow up an `mvp-plan` session with actual code. Spawns `phase-executor` sub-agents — fans out parallel-safe phases concurrently, pauses between groups so the user can verify the dev server. Pitch-demo scope only — happy-path React + RR + Zustand, no auth/deploy/tests.
---

The user has a plan written by `mvp-plan`. Now they want it built — phase by phase, in the right order. You are the **orchestrator**: read the root plan, decide which phases are runnable, spawn `phase-executor` sub-agents (in parallel when phases are parallel-safe), ship each phase by moving its file to `plans/done/`, and surface a working dev server between groups so the user can sanity-check.

The phases were designed to be independently buildable — trust the plan. But re-read the root plan and the `todo/` folder each iteration, because the user may have pivoted mid-build (edited the plan, added a phase) and the loop needs to pick those changes up.

## What you do vs. what you delegate

| You (orchestrator)                                            | Sub-agents you spawn                                                                 |
|---------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Read root plan; compute the next runnable group from the DAG  | `phase-executor` — reads one phase file, writes the React/Zustand/RR code in `mvp/`  |
| Spawn N `phase-executor`s **in the same turn** for parallel-safe groups | `phase-executor` walks the done-when checklist as it implements; returns status, files, results, notes |
| `mv` shipped phase files from `plans/todo/` to `plans/done/`  |                                                                                      |
| Run `npm install` / `npm run dev` between groups, share URL   |                                                                                      |
| Pause for user verification before starting the next group    |                                                                                      |
| When `plans/todo/{id}-*.md` empties, spawn `pitch-summary`    | `pitch-summary` — synthesizes workflow + plans into `docs/#{id}-<slug>-pitch.md`     |
| Surface final report + doc path to the user                   |                                                                                      |

Why this split: sub-agents have the heavy file-writing tools and narrow jobs (implement a phase / render a doc). The orchestrator owns coordination + the dev server + interactive checkpoints + when to trigger the summary, because those are stateful and can't be safely fanned out.

## Process

### 1. Get the ID

Ask the user for an idea ID if not given. Normalize to four digits (`1` → `0001`). If `plans/{id}-plan-root.md` doesn't exist, stop — direct them to run `mvp-plan` first. The plan must exist before you can execute it.

### 2. Read state (re-do this every loop iteration)

Read these things, **every time you start a new group** — the user may have pivoted:

- `plans/{id}-plan-root.md` — DAG, parallel groups, demo flow, assumptions, the **Builds on** / **Already in `mvp/`** sections
- `plans/todo/{id}-*.md` — remaining phases for the current drop (glob)
- `plans/done/{id}-*.md` — current-drop phases already shipped (glob) — used for dependency checks
- `plans/done/*.md` (any ID) — **all** shipped phases across prior feature drops. Skim these to keep a fresh "what's already in `mvp/`" summary, which you'll pass to every `phase-executor`. Remember: this is one product growing over multiple IDs.

If `plans/todo/{id}-*.md` is empty, this feature drop is done. Start the dev server one last time, share the URL, tell the user, stop.

### 3. Compute the next runnable group

A phase is **runnable** if every entry in its `Blocked by:` header is already present in `plans/done/{id}-*.md` (or is `none`). The root plan's **Parallel groups** section tells you which set of runnable phases fan out together.

If a phase in `todo/` lists a blocker that exists neither in `todo/` nor `done/`, stop and tell the user — the plan and the filesystem have drifted. Don't guess.

### 4. Spawn phase-executor(s) for the group

For each phase in the runnable group, spawn one `phase-executor` sub-agent **in the same turn** so they run concurrently. Pass each one:

- `phase_file` — absolute path to `plans/todo/{id}-{NN}-{slug}.md`
- `project_root` — the repo root (executor writes under `<project_root>/mvp/`)
- `already_shipped` — a short summary of every shipped phase in `plans/done/` (all IDs, not just the current drop), so the executor reuses existing components/routes/store-slices instead of rebuilding them. Include prior-ID work — that's the existing product the executor is extending.

If the runnable group is just one phase, fine — spawn one. Single-call parallel is the same code path as N-call parallel.

**Shared-file caution.** If two parallel-safe phases both touch a shared file (e.g., `App.tsx` for route registration, `store.ts` for store slices), that's a dependency-mapper bug. Fall back to serial execution for that group and tell the user — better safe than a merge mess.

### 5. Ship each phase as its executor returns

When an executor reports `status: done`:

1. `mv plans/todo/{id}-{NN}-{slug}.md plans/done/` — keep the filename so the root plan's links stay valid.
2. Check the executor's done-when results. If any item is `[ ]` (unimplemented) or `[?]` (needs runtime check), flag it for the user when you summarize the group. Still ship; flag it as "verify in the dev server".

If an executor reports `status: partial` or `status: blocked`:

- **Don't** move the file.
- Surface the blocker / partial-implementation notes to the user verbatim.
- Stop the loop. The user decides whether to edit the phase file, run a targeted fix, or skip.

### 6. After the group finishes, start the dev server

Once every executor in the group has returned and shipped (or one has blocked the group):

1. If `mvp/node_modules` doesn't exist, run `cd mvp && npm install`.
2. Start the dev server in the background: `cd mvp && npm run dev` (use `run_in_background: true`).
3. Wait briefly, then read the background log to find the Vite URL (look for `Local:` line). Report it to the user.
4. If a dev server is *already* running on the port, don't start another — just tell the user it's still up.

Summarize for the user:

```
Shipped: 0001-02-routing-shell, 0001-03-zustand-store
Dev server: http://localhost:5173/
Demo path to try: / → /dashboard → click a card → /recipe/:id
Caveats: phase 03 done-when "[?] store persists across reload" — needs your eye.
Ready when you are. Say "continue" to start the next group.
```

### 7. Wait for user, then loop

Don't auto-advance. Wait for the user to say "continue" / "looks good" / "next" — or to flag a bug, in which case stop and help them fix it before resuming.

When they confirm, go back to Step 2 (re-read state — the user may have edited files while clicking around).

Loop until `plans/todo/{id}-*.md` is empty.

### 8. Generate the pitch summary — delegate to `pitch-summary`

When the last group ships and `plans/todo/{id}-*.md` is empty, spawn the `pitch-summary` sub-agent with `{ id, project_root }` **before** reporting back to the user. It reads the workflow trio + root plan + shipped phases and writes `docs/#{id}-<slug>-pitch.md` — a presentation-ready summary (Story → Idea → Problem → Solution → Purpose). This is the artifact the founder will turn into slides next month, so it must always be in sync with what actually shipped.

If `pitch-summary` returns `blocked` (e.g., workflow files all missing), don't fail the run — just note in the final report that the pitch summary couldn't be generated and what was missing.

### 9. Final report

After the pitch summary is written, tell the user:

- All phases for `#{id}` are in `plans/done/`
- The demo URL is still live at <url>
- The pitch summary is at `docs/#{id}-<slug>-pitch.md`
- A bulleted recap of any done-when boxes that shipped as `[?]` so they can verify each
- A reminder that the demo IS the test — they should walk the full flow from the root plan's "Demo flow" section before pitching

## Edge cases

**Half-shipped plan, re-running the skill.** The skill is idempotent. State lives entirely in `plans/todo/` vs `plans/done/`. Re-running picks up at whatever's still in `todo/`. No flags or resume tokens needed.

**The user pivoted mid-build.** Because Step 2 re-reads everything every loop iteration, edits to the root plan or new phase files in `todo/` get picked up automatically on the next group. New blockers? Re-computed. Removed phases? Won't run.

**A phase has no visible UI change** (store setup, seed data, type plumbing). The executor will say so in its notes. Don't insist on something to click — the dev server will still be running for the *prior* visible phase.

**Done-when can't be programmatically verified** ("shows three project cards"). Trust the executor's `[?]` and flag it for the user. The whole point of the dev-server pause is for the human to verify these.

**`npm install` fails or dev server won't start.** Stop the loop. Report the error verbatim. Don't try to patch package.json yourself — that almost certainly means a phase spec was wrong (missing dep, mismatched version) and the user needs to see it.

**`mvp/` doesn't exist yet** (executor for phase 01 = scaffold). The scaffold phase's executor creates it. After phase 01 ships, the rest of the flow is normal.

## Stack reminder

Same as `mvp-plan`: React + React Router + Zustand + Vite, fake-DB, happy path. If a phase spec asks for something out of scope (real auth, real backend, automated tests, deploy config), **don't have the executor build it** — stop and ask the user. That's almost certainly a planning bug and silently building it pushes the demo off-track.

## What you don't do

- Don't write code yourself. The executor does that. (If you find yourself wanting to "just patch this one line", spawn an executor for a small fix-up phase instead — keeps the audit trail clean.)
- Don't run automated tests. There aren't any; this is pitch-demo scope.
- Don't deploy. Out of scope.
- Don't `git commit`. The user commits when they're ready.
- Don't renumber phases or rename slugs. The root plan and `done/` already reference the existing filenames.
