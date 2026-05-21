---
name: pitch-deck
description: Turn a feature drop's pitch summary into a presentation-deck PDF — a bold, type-driven slide deck rendered from `docs/#NNNN-<slug>-pitch.md`, structured Problem → Solution → Impact for a 3–5 minute pitch. Use whenever the user wants to "make a pitch deck", "turn the pitch into a PDF", "create a presentation / slides", "build the deck for #0001", "generate slides from the pitch", "I need a deck for the demo day", or runs `/pitch-deck`. Reach for this right after `pitch-summary` or `mvp-execute` produces a pitch file, or whenever someone needs the founder's slide deck as a PDF. This builds the *deck PDF*; it is not for editing existing PDFs (use `pdf`) or for the Lean Canvas image (use `business-canvas`).
---

# pitch-deck

Render a presentation-deck **PDF** from a drop's pitch summary. The pitch file
(`docs/#NNNN-<slug>-pitch.md`, written by the `pitch-summary` agent) is the story;
this skill turns it into slides a founder presents.

You are the **orchestrator**. The judgment of what goes on each slide belongs to
the `deck-builder` sub-agent — you find the target pitch file(s), make sure the
renderer can run, fan out one sub-agent per drop, and report what landed. Don't
write slide content or PDF code yourself; that's the sub-agent's and the script's
job, and keeping it there means many drops can render in parallel.

The deck's shape (Problem → Solution → Impact, demo-led, one line to close) comes
from the house pitch reference `ref.md`. You don't need to read it — that framing
is baked into the `deck-builder` agent.

## 1. Pick the target pitch file(s)

Pitch files live at `docs/#NNNN-<slug>-pitch.md`. Resolve which one(s) to build:

- **User named a drop** ("#0001", "0001", "the fridgechef one") → target that
  `docs/#<id>-*-pitch.md`.
- **No drop named** → `Glob: docs/*-pitch.md` and branch on the count:
  - **none** → there's nothing to deck yet. Tell the user pitch files are written
    by `pitch-summary` after `mvp-execute` ships a drop's last phase, and stop.
    Don't fabricate a pitch.
  - **one** → use it (mention which one you're building).
  - **several** → **ask which** with `AskUserQuestion`; list each by id + slug, and
    offer an "all of them" option. Don't silently build every deck — that's a lot
    of surprise output.

## 2. Make the renderer runnable (once)

The deck renderer needs `reportlab`. Resolve a working interpreter a single time
and reuse it for every sub-agent:

```bash
PYBIN="$(bash "<project_root>/.claude/skills/pitch-deck/scripts/ensure_deps.sh")"
```

It prints an interpreter path on stdout (installing into a skill-local `.venv` the
first time if your system Python lacks reportlab). If it exits non-zero, surface
its stderr — the user may need to install reportlab manually — and stop.

## 3. Fan out one deck-builder per drop

Spawn the `deck-builder` sub-agent with `subagent_type: deck-builder` — **one per
target pitch file, all in a single message** so independent drops render
concurrently. Pass each:

```
id: 0001
project_root: <abs repo path>
skill_dir: <project_root>/.claude/skills/pitch-deck
python_bin: <PYBIN from step 2>
accent: <hex, only if the user asked for a brand color — else omit>
```

Accent is optional; omit it unless the user specifies a color (the renderer has a
sensible default). If they mention a brand color, pass it as a hex string.

## 4. Report

Relay each sub-agent's slide map and output path — the user wants to know what got
made and where. Keep it tight:

- `docs/#0001-fridgechef-deck.pdf` — 6 slides (Title · Problem · Solution · Demo · Impact · Close)
- note any slide a sub-agent dropped for lack of evidence

The editable spec is saved next to each PDF as `docs/#NNNN-<slug>-deck.json` — tell
the user they can tweak wording there and re-render with `build_deck.py` without
regenerating from the pitch. Then offer the natural next step: open the PDF, or
walk the live demo (`/playwalkthrough <id>`) that the deck's demo slide cues.

## Scope

- **In:** pitch.md → slide-deck PDF (+ its regenerable spec JSON), one per drop.
- **Out:** writing the pitch summary itself (that's `pitch-summary`), the Lean
  Canvas image (`business-canvas`), and general PDF surgery — merging, splitting,
  form-filling, editing an existing PDF (that's the `pdf` skill).
