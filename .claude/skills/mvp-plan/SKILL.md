---
name: mvp-plan
description: Plan an MVP build phase-by-phase from an idea's workflow evidence. Use this skill whenever the user wants to turn a validated idea into a buildable MVP plan, asks to "plan the build", "break this into phases", "plan #0001", or wants a parallel-vs-blocking dependency map for what to build first. Reads workflow/{ideas,approach,marketing}/#NNNN-*.md, then writes plans/{id}-plan-root.md plus per-phase plans/todo/{id}-{NN}-{slug}.md files. Pitch-demo scope only — happy-path React + React Router + Zustand as fake DB, no auth/deploy/scale concerns.
---

The user has validated an idea, hunted for unsolicited demand evidence, and pinned a marketing plan. Now they need to turn that into something they can actually build and demo to pitch — fast.

You are the **orchestrator**. You handle the interactive bits (asking the user for ID, looping clarifying questions, deciding scope) and synthesize the final plan. Heavy mechanical work — reading workflow files, inspecting the scaffold, mapping dependencies, writing per-phase files — is delegated to four sub-agents.

The output is meant to be executed by the founder (or another Claude session) one phase at a time. The plan optimizes for **showing the happy path** to investors / first users, not for handling the edge cases that won't appear in a 5-minute demo.

## Mental model — one product per repo

This scaffolding is for **one product**. A completely different business → clone the scaffolding into a separate folder. Inside one repo:

- `#0001` is the first feature drop (usually the core MVP). Scaffold + first demoable slice.
- `#0002`, `#0003`, … are **subsequent feature drops on the same product** — they extend `mvp/`, they don't replace it. The `workflow/{ideas,approach,marketing}/#NNNN-*.md` files describe what's being added, not a new business.

So when you plan `#0002`, you are planning a feature drop on an already-built MVP. You **must** read what's already shipped before you can plan additions sensibly — otherwise you'll re-plan existing pages, miss reusable components, or break working routes.

## What "MVP scope" means here

Default stack — pick these unless the user explicitly overrides:
- **React** (functional components + hooks)
- **React Router** for navigation
- **Zustand** as the in-memory "database" — seed it with mock data on app load, mutate freely, no persistence
- **Vite** as the dev server / bundler
- **CSS** (or CSS modules / styled-components per the design system aesthetic). Avoid heavy UI kits unless the chosen aesthetic calls for one.
- Optional, only when a demo needs it: `react-hook-form` for forms, `motion` (Framer Motion v11+) for the animations that sell the pitch

Deliberately out of scope:
- Real auth (use a fake "logged in" toggle in Zustand)
- Real backend / DB / third-party APIs (use Zustand + mock JSON)
- Deployment, CI, monitoring, error tracking
- Edge cases, defensive validation, full a11y, i18n
- Automated tests (the demo *is* the test)

If the user explicitly asks for something out of scope ("use Supabase auth"), ask once whether they actually need it for the pitch or if a fake will do. Default to the fake — every real integration adds days and demo flake risk.

## Sub-agents you delegate to

| Agent                  | Use it for                                                                                   |
|------------------------|----------------------------------------------------------------------------------------------|
| `workflow-reader`      | Pull a structured digest of `workflow/{ideas,approach,marketing}/#{id}-*.md` (Step 2)        |
| `scaffold-inspector`   | Inspect `mvp/` and report stack + gaps (Step 3)                                              |
| `dependency-mapper`    | Take your phase specs and return the DAG with blocked-by + parallel-safe (Step 6)            |
| `phase-writer`         | Render one phase spec → one markdown file. Spawn N in parallel to write all phases at once (Step 7) |

Invoke each via the Agent tool with `subagent_type` set to the agent's name. Pass the input it expects (see each agent's SKILL for the contract). When the contract is straightforward (phase-writer, workflow-reader, scaffold-inspector), you don't need to re-explain what they do — just give them the data.

## Process

### 1. Get the ID

Ask the user for an idea ID (`1`, `01`, or `0001` — normalize to four digits, zero-padded). If they don't know one, glob `workflow/ideas/#*.md` and show the list.

### 2. Read the workflow context — delegate to `workflow-reader`

Spawn `workflow-reader` with `{ id, project_root }`. It returns a structured digest plus a `## Gaps` section listing any of the three workflow files that are missing.

If gaps are reported: tell the user which stages are missing and ask whether to proceed. The marketing channel often dictates the demo flow — proceeding without it means you'll guess. Document the gap regardless of the user's answer.

### 2.5. Read what's already shipped — glob `plans/done/*.md`

Glob `plans/done/*.md` (across all IDs, not just the current one) and read each file. These are the features already shipped in this product.

- **If empty** → this is the very first feature drop on a fresh repo. Phase 01 will be the design-system + scaffold (Step 3 will confirm).
- **If non-empty** → you are planning an **additive feature drop**. Build a short digest you'll carry through the rest of the steps: what routes exist, what pages/components/store-slices have been built, which design-system pieces are reusable. New phases must extend or compose with this, not duplicate it.

If a prior phase's done-when had `[?]` items (runtime checks the human verified at the dev-server pause), assume those passed unless the user says otherwise.

### 3. Detect existing MVP scaffold — delegate to `scaffold-inspector`

Spawn `scaffold-inspector` with `{ project_root }`. It returns whether the scaffold exists, the detected stack, conventions in use, gaps, and a one-sentence recommendation on the scaffold-phase shape:

- **Scaffold doesn't exist** → plan a full design-system + scaffold phase as phase 01. Before writing its spec, read `.claude/skills/frontend-design/SKILL.md` and use it to pick fonts, color tokens, motion vocabulary, and a tone that fits the idea (a productivity tool for accountants and a consumer fashion app should not look the same).
- **Scaffold exists, no gaps** → skip the scaffold phase. Anchor later phases on the conventions the inspector reported (router setup, store shape, component patterns).
- **Scaffold exists, but tokens / motion / layout shell are missing** → plan a *slim* phase 01 that only fills those gaps. Don't redo what's already there.

### 4. Loop-interview to fill thin spots

The workflow evidence is rarely complete enough to plan a build. Ask, one question at a time, about whatever you can't pin down. Don't batch-ask.

Useful prompts:
- **Who's on the first screen?** Logged-in user with seed data, or empty state with a "sign up" CTA that fakes auth?
- **What's the one "wow" interaction?** The thing in the demo that makes the investor lean forward.
- **Mock data shape?** Which entities exist (users, posts, listings, projects…) and what fields drive the demo?
- **Routes the demo touches?** List the URLs the founder walks through.
- **Anything custom?** Charts, maps, drag-drop, real-time updates — flag these because they'll dominate effort.

If the user shrugs at a question, propose a sensible default ("OK, I'll plan for a logged-in user with seed data — easier to demo") and move on. Don't stall.

### 5. Decompose into phase specs

A phase = one chunk of work that lands a *demoable* slice. Good phases are independently reviewable, not just "implement file X". They have a goal a non-engineer could verify ("the dashboard now shows three project cards").

Typical phase shapes for an idea-starter MVP — adapt, don't copy:

| Order | Phase                              | When it appears                                                                 |
|-------|------------------------------------|---------------------------------------------------------------------------------|
| 01    | Design system + scaffold           | scaffold-inspector says `mvp/` is empty                                          |
| 01    | Slim design tokens / shell fillers | scaffold-inspector says scaffold exists but tokens / shell are missing           |
| (skip)| —                                  | scaffold-inspector says scaffold exists with no gaps                             |
| 02    | Routing + layout shell             | After scaffold (if not already done) — `<Layout>`, nav, public vs gated routes  |
| 03    | Zustand store + seed data          | Mock entities, store hydration on app load, fake-auth toggle                    |
| 04+   | Feature pages                      | One phase per *demo screen*: landing, dashboard, detail, create-flow            |
| Last  | Demo polish                        | Loading shimmers, micro-animations, empty states for screenshots, video embed   |

A B2B dashboard idea will have very different phases than a consumer mobile-web app. Let the workflow context drive the shape.

For each phase you decompose, hold the full spec in working context (slug, goal, modules, interfaces, state shape, routes, interactions, mock data, MVP shortcuts, done-when). You'll pass these to `phase-writer` in Step 7.

### 6. Map dependencies — delegate to `dependency-mapper`

Pass your phase specs (just the name, goal, and modules-touched per phase) to `dependency-mapper`. It returns the DAG: who blocks whom, who's parallel-safe, the critical path. Use its DAG in the root plan table.

If the mapper flags missing or split-able phases in its **Notes**, take a hard look — that's usually correct.

### 7. Write the plan files — spawn `phase-writer` N times in parallel

Create `plans/`, `plans/todo/`, and `plans/done/` if they don't exist.

Then **spawn one `phase-writer` per phase, all in the same turn** so they run concurrently. Each call gets the full spec for that one phase (see `phase-writer`'s SKILL for the input shape) and the output path (`plans/todo/{id}-{NN}-{slug}.md`).

Write the root plan yourself — it's synthesis work, not mechanical rendering. Use the template below.

### 8. Report

Tell the user:
- Path to the root plan
- How many phases you wrote
- Which phases are parallel-safe (so they can split work across multiple sessions)
- Any thin spots in the workflow context you papered over with defaults — they may want to backfill those into the workflow files before building

## Layout

```
plans/
├── {id}-plan-root.md           ← you write this directly
├── todo/
│   ├── {id}-01-<slug>.md       ← written by phase-writer
│   ├── {id}-02-<slug>.md       ← written by phase-writer
│   └── ...
└── done/                       ← phases get moved here after they ship
```

Conventions:
- `{id}` is the same zero-padded four-digit ID as the workflow files (e.g. `0001`)
- Phase order is two-digit (`01`, `02`, …)
- Slugs are per-phase, kebab-case (e.g. `design-system`, `auth-stub`, `dashboard-page`)

## Root plan template (you write this)

```markdown
# MVP Plan — <idea name>

**Workflow ID:** #<id>
**Date:** <YYYY-MM-DD>
**Stack:** React + React Router + Zustand <+ anything else picked>
**Demo target:** <the one screen or flow the pitch leads with>
**Builds on:** <list prior shipped IDs, e.g. "#0001 (core MVP)", or "—" if this is the first drop>

## Idea summary
One short paragraph in the founder's voice — what this feature drop adds and who it's for.

## Already in `mvp/` (only if Builds on is non-empty)
Short digest from `plans/done/*.md` — what's shipped so far. Helps reviewers (and future Claude sessions) see what this drop extends.
- Routes: `/`, `/dashboard`, `/recipe/:id`
- Pages: `Dashboard`, `RecipeDetail`
- Components: `RecipeCard`, `EmptyState`
- Store slices: `recipes`, `auth`
- Design tokens: <one-line aesthetic note>

## Demo flow
The literal script the founder runs in front of an investor or first user.
1. Land on `/...`
2. Click ...
3. See ...
4. ...

## Workflow gaps (only if any workflow files are missing)
Which stages are missing, what you assumed in their place, and what to backfill before launch.

## Phases
<paste the table from dependency-mapper, mapped to phase filenames>

| #  | Phase                        | File                                  | Blocked by | Parallel-safe with |
|----|------------------------------|---------------------------------------|------------|--------------------|
| 01 | <phase>                      | todo/<id>-01-<slug>.md                | —          | —                  |
...

## Parallel groups (from dependency-mapper)
1. **01** alone
2. **02 + 03** can fan out
3. ...

## Critical path
<paste from dependency-mapper>

## Execution
Run phases in dependency order. Mark a phase done by moving its file from `plans/todo/` to `plans/done/`. When everything is in `done/`, the MVP is demo-ready.

## Assumptions made
Things the planner filled in because the user didn't pin them down — flag them so the founder can correct anything wrong before building.
- ...
```

## When the user runs this skill again on the same ID

If `plans/{id}-plan-root.md` already exists, don't blow it away. Read it, ask what changed (new pivot? scope cut? new demo target?), and edit/append phases rather than rewriting. The engineering work in `mvp/` already references those filenames, and renumbering breaks links.

## Effort estimates — be honest

Founders ask "how long?" Use S/M/L per phase: S = 1–2 focused hours, M = half-day, L = a day. Don't pad with hidden buffer; this is MVP scope and the buffer lives in the "MVP shortcuts" section of each phase. If a phase looks like more than L, it's actually two phases — split it.
