---
name: business-canvas
description: Draw an Ash-Maurya Lean Canvas (10 boxes) for an idea by reading its `#NNNN-<slug>.md` files from `workflow/ideas/`, `workflow/approach/`, and `workflow/marketing/`, synthesizing each cell, then rendering a PNG into `docs/` via the `tldraw` MCP server. Use whenever the user asks to "draw the canvas", "render a lean canvas", "make a business canvas", "visualize idea #0003", "turn my idea into a picture", "sketch the business model", or after they've finished `validate-idea` / `pain-hunt` / `marketing-plan` and want a single-page visual. Always ask which idea ID first (e.g., `0001` or `3`) — don't guess.
---

Render a Lean Canvas (Ash Maurya's 10-box variant — better than Osterwalder's 9-box for pre-launch ideas because it surfaces *problem*, *unfair advantage*, and *key metrics* explicitly) for one specific idea ID by pulling its evidence from the project's stage folders, building a tldraw shape document, and saving a PNG plus the editable source into `docs/`.

The canvas isn't art. It's a one-page compression of everything we already know. The point is to expose the weak cells — the ones with nothing to put in them — so the user can see what evidence is still missing.

## Step 1 — Get the idea ID

Ask the user which idea to canvas. Accept any of: `0001`, `1`, `#0001`, `#1`. Normalize to a 4-digit zero-padded form like `0001`. If they don't give you one and you can't infer it from the conversation, ask — don't pick one.

## Step 2 — Find and read context

Look in each of these folders for a file matching `#<NNNN>-*.md`:

- `workflow/ideas/#NNNN-*.md` — problem, user, pain, alternatives, "why you" (from `validate-idea`)
- `workflow/approach/#NNNN-*.md` — unsolicited-demand evidence and verbatim complaints (from `pain-hunt`)
- `workflow/marketing/#NNNN-*.md` — channel pick, budget, success/kill criteria, named persona (from `marketing-plan`)

A glob like `workflow/ideas/#0001-*.md` is the way — slug isn't known in advance. The slug will be the same across all three folders for a given ID; capture it from whichever file you find first.

If a folder has no match, that's fine — proceed and warn the user once at the end ("Customer Segments cell is thin because no `workflow/marketing/#NNNN-*.md` exists yet — run `marketing-plan` to fill it"). Don't refuse; partial canvases still teach.

If a folder has multiple matches for the same `#NNNN-` prefix (shouldn't happen under the project's numbering rules, but be defensive), use the first one alphabetically and note it.

## Step 3 — Synthesize the 10 cells

Lean Canvas cells map to the source files like this. Keep each cell to a *short header line* plus *2–4 punchy bullets* — the canvas is read at a glance, not in paragraphs.

| Cell | Pull from | What to write |
| ---- | --------- | ------------- |
| **Problem** | `workflow/ideas/` Problem + `workflow/approach/` verbatim quotes | Top 1–3 problems, ideally in the sufferer's own words |
| **Customer Segments** | `workflow/ideas/` User + `workflow/marketing/` named persona | Who has the problem; mark early adopters distinctly |
| **Unique Value Proposition** | `workflow/ideas/` core thesis + `workflow/marketing/` positioning | One-sentence "single, clear, compelling" message — what + for whom + why different |
| **Solution** | `workflow/ideas/` solution sketch + `mvp/` if it exists | Top 3 features only. Resist listing the roadmap. |
| **Channels** | `workflow/marketing/` "Single starting channel" + "Where they hang out" | The one channel that's been chosen; list the named venues |
| **Cost Structure** | `workflow/marketing/` Budget + a short interview if it's thin | Early-stage spend only. Most idea-starter users are software engineers building solo, so build-time is effectively free until proven otherwise — don't list "engineering salary" or production AWS bills. List the *actual* money flowing out: ad spend, influencer fees, tool subscriptions (Buffer, Mailchimp, basic analytics), domain, landing-page service. Example: `"$300/mo Meta ads test + $40/mo Buffer + $15/yr domain"`. |
| **Revenue Streams** | `workflow/ideas/` willingness-to-pay + `workflow/marketing/` pricing implications + interview if blank | Pricing model (one-time / subscription / freemium), price point ($5, $20, $99/mo — pick one), and rough LTV if guessable. Don't write "TBD" — push for a number you can both stress-test. |
| **Key Metrics** | `workflow/marketing/` Success criteria | The 1–3 numbers that will say "this is working" by day 30 / 90 |
| **Unfair Advantage** | `workflow/ideas/` "Why you" | Something a competitor can't easily copy. If empty, write `"⚠️ none yet — riskiest cell"` rather than fluffing it. |
| **Early Adopters** | `workflow/marketing/` named persona + `workflow/approach/` complainants | Specific people/segments who feel the pain *acutely*. Names, handles, or roles — not "small business owners". |

### Interview before you give up on a cell

Most idea-starter users are software engineers building solo. That means *Cost Structure*, *Revenue Streams*, *Key Metrics*, and sometimes *Channels* won't be in the source files in numeric form — and the user is the engineer, so their build labor is effectively free. Don't just write `"(no evidence yet)"`; ask them. Loop on vague answers the same way `validate-idea` and `marketing-plan` do — keep asking until the number is concrete enough to put on a canvas.

Sample questions you can ask in any order, one at a time:

- **Cost / budget split** — "You're the engineer here, so let's treat your build time as free. What can you spend per month on getting users while you test this? Rough is fine — $100? $500? $2000?"
- **Where the money goes** — "Of that, how would you split it? Paid ads vs an influencer payment vs tool subscriptions (Buffer, Mailchimp, analytics) vs landing-page service?"
- **One-time costs** — "Anything you'll pay once instead of monthly? Domain (~$15/yr), logo, Stripe fees, ConvertKit annual?"
- **Pricing** — "Are you charging from day 1, or running free → paid later? What price point — $5, $20, $99/mo? Pick one to stress-test; we can change it later."
- **Success metric** — "What single number at day 30 tells you 'this is working'? Signups, paid conversions, replies to outreach, demo bookings? Real number, not 'good engagement'."

"$some money for ads" doesn't pass. "$300/mo for 8 weeks then re-evaluate" passes. Push for that level of specificity.

### Typical early-stage budget tiers (for sanity-checking)

Use this to spot mismatches between the user's stated budget and the channel they picked in `workflow/marketing/`. If a mismatch exists, surface it in the final report (Step 7) — it's a more useful insight than a polished canvas.

| Budget tier | What it can fund | Mismatch warnings |
| ----------- | ---------------- | ----------------- |
| **$0/mo (pure sweat)** | Founder-led DMs, posts in subreddits/Discords, free tier of every tool | Picking "Meta ads" or "influencer" here is a mismatch — push them back toward community/founder-led |
| **$50–300/mo** | Tool stack (Buffer/Mailchimp/Plausible) + one tiny ad test ($50–100) | Not enough for an honest paid-ads test or any influencer fee |
| **$500–1500/mo** | Real ad test ($300–800), tool stack ($50–150), one nano/micro influencer ($100–500) | Enough to learn *something*; not enough to scale |
| **$2000+/mo** | Sustained ad spend, ongoing micro-influencer relationship, paid analytics | If the product can't fund $40+ CAC, this is still a money fire |

### When a cell is truly empty after the interview

If after asking the user *still* has no answer for a cell — they don't know their price, they don't know their metric — write `"⚠️ unknown — open question"` in that cell rather than fluffing it. Open questions on a Lean Canvas are the *whole point*; they're the user's homework. A fluffy guess is worse than an honest blank, because it hides the gap.

## Step 4 — Learn the tldraw shape format

Call the `tldraw` MCP server's `tldraw_read_me` tool once. It returns the shape format reference (allowed shape types, the 13 named colors, fill modes, auto-conversion rules). Read it before building shapes.

Two constraints shape everything below:

- **No hex colors.** tldraw accepts only 13 named colors (`orange`, `yellow`, `light-green`, `light-blue`, `red`, `grey`, …) and four fills (`none|semi|solid|pattern`). So the canvas's "design system" is a fixed *mapping* onto those names — you can't drop in this product's `#FAF3E7` / `#C8791A` tokens directly. The mapping below is chosen to read warm and light anyway.
- **Standalone `text` shapes are unreliable in headless export.** Their width is auto-measured before the web font loads, the measurement comes back ~0, and the text collapses into a tiny clipped box — so you silently lose your title or labels. Keep *every* piece of text inside a `geo` shape, which has a fixed `w` so text always wraps. The build script (Step 5) already does this; if you ever hand-edit shapes, hold that line.

## Step 5 — Build the canvas (design system + build script)

A Lean Canvas that looks like a bare wireframe gets glanced at and closed. A little design — warm color, a clear header/body split, a flagged weak cell — makes the user actually read it and *see the gaps*, which is the entire job of this artifact. So render it through a small design system rather than freehand boxes.

**Don't hand-build the ~30 shapes.** Use the bundled script — it owns the coordinates, the color system, the header/body card split, and the all-text-inside-geo rule, so you spend your attention on the *content* of each cell (Step 3) instead of pixel math. You only feed it the bullets.

```
python .claude/skills/business-canvas/scripts/build_canvas.py <input.json> <out.tldr.json> [--theme color|mono]
```

`input.json` carries only what you synthesized — headers and layout are fixed:

```json
{
  "id": "0001",
  "name": "Myanmar Serial Reader",
  "cells": {
    "problem":   {"body": "• one\n• two\n• three"},
    "solution":  {"body": "• ..."},
    "metrics":   {"body": "• ..."},
    "uvp":       {"body": "..."},
    "advantage": {"body": "..."},
    "channels":  {"body": "..."},
    "segments":  {"body": "..."},
    "cost":      {"body": "..."},
    "revenue":   {"body": "..."},
    "adopters":  {"body": "..."}
  }
}
```

A cell that is missing, blank, or marked `"weak": true` renders **red** (`⚠ unknown — open question`). Lean into that — an honest red cell is the user's homework and the most valuable thing on the page. Don't fluff a guess just to avoid the red.

The script writes the editable shapes JSON to `<out.tldr.json>` *and* prints the same JSON compactly to stdout — capture stdout and pass it straight to the render call in Step 6.

### The design system ("warm-light Lantern Canvas")

This product reads in a warm light "lantern-dawn" register (paper + amber + literary serif), so the canvas matches: **serif** title and headers, **sans** body, soft fills, an amber accent. The script offers two themes:

- **`color` (default)** — region color carries meaning, so the business model is legible at a glance:

  | Region | Cells | Color |
  | ------ | ----- | ----- |
  | How it works | Problem, Solution, Key Metrics, Channels | `light-blue` |
  | The heart | Unique Value Proposition | `orange` (amber) |
  | Who it's for | Customer Segments, Unfair Advantage, Early Adopters | `yellow` |
  | The money | Cost Structure, Revenue Streams | `light-green` |
  | Weak / empty (overrides region) | any cell | `red` header + `light-red` body |

- **`mono`** — every section in a single amber accent on white cards. Calmer, the most literal match to lantern-dawn. Less information (no region meaning); only weak cells still go red.

Render `color` by default. After it lands, tell the user the calmer `mono` version exists and re-render with `--theme mono` if they prefer it — this is the deliberate "user picks at render" step.

### What the design system draws (so you can sanity-check or override)

- **Cards, not cells.** Each of the 10 boxes is a `solid`-filled **header strip** (serif, the cell name in caps) stacked on a `semi`-filled **body card** (sans, the bullets). The strip gives hierarchy without needing bold.
- **Floating layout.** Cells are inset ~7px and sit on a soft `grey` board, so visible gutters make it read as a designed dashboard, not a tiled grid.
- **Decoration.** A full-width serif **title band** (`LEAN CANVAS · <name> · (#NNNN)`), an **amber accent rule** beneath it, and a **color-key legend** of chips along the bottom that documents the palette.
- **Readable sizes.** The canvas is ~1560px wide, where tldraw `size:"s"` text is unreadable — body/headers are `m`, the title is `l`. Keep bullets short (Step 3 already enforces this) so `m` text fits the 286px columns.

The fixed grid the script lays out (tldraw px, ~1500×900 before the title band):

| Cell | x | y | w | h |
| ---- | -- | -- | -- | -- |
| Problem | 0 | 0 | 300 | 600 |
| Solution | 300 | 0 | 300 | 300 |
| Key Metrics | 300 | 300 | 300 | 300 |
| Unique Value Proposition | 600 | 0 | 300 | 600 |
| Unfair Advantage | 900 | 0 | 300 | 300 |
| Channels | 900 | 300 | 300 | 300 |
| Customer Segments | 1200 | 0 | 300 | 600 |
| Cost Structure | 0 | 600 | 750 | 300 |
| Revenue Streams | 750 | 600 | 750 | 300 |
| Early Adopters | 1200 | 600 | 300 | 300 |

> Maurya's original tucks "Early Adopters" inside Customer Segments. Splitting it into its own bottom-right cell makes empty-vs-filled obvious at a glance — the point of the canvas for our flow. Keep this layout unless the user asks for the classic.

## Step 6 — Render and save

1. Run the build script (Step 5), pointing its `<out.tldr.json>` at `docs/#NNNN-<slug>-canvas.tldr.json` (create `docs/` if missing). That file *is* the editable source — the MCP takes shapes JSON directly, so the user can re-render or tweak it later.
2. Pass the JSON the script printed to `create_tldraw_diagram`:
   - `shapes`: the compact JSON string from stdout.
   - `outputPath`: an **absolute** path like `<project-root>/docs/#NNNN-<slug>-canvas.png`.
   - `format`: `"png"` by default — it embeds cleanly in slides and the pitch summary. Also offer/render `"svg"` when the canvas is text-dense or headed for print: vector text stays crisp at any zoom.

## Step 7 — Report

Tell the user three things:

1. Where the PNG landed (`docs/#NNNN-<slug>-canvas.png`).
2. Which cells were thin or empty (the red ones), and which source file would fill them (e.g., "Channels is empty — run `marketing-plan` for #0001").
3. The single weakest cell — usually Unfair Advantage or Key Metrics for early-stage ideas — and the cheapest experiment to strengthen it.
4. A one-liner offering the alternatives: the calmer `mono` theme, or an `svg` for print/slides — re-render on request.

If a file with the same name already exists in `docs/`, append a numeric suffix (`-canvas-v2.png`, `-v3`, etc.) — canvases evolve and old versions are useful to keep for diffing.
