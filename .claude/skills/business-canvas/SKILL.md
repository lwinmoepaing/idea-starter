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

Call the `tldraw` MCP server's `tldraw_read_me` tool once. It returns the shape format reference (allowed shape types, color enums, the auto-conversion rules for IDs and rich text). Read it before building shapes — the format has subtleties (e.g., `text` props auto-convert to `richText`, plain string IDs work fine, arrow bindings have a shorthand).

## Step 5 — Lay out the canvas

The Lean Canvas grid is 5 columns wide on top with two of the columns split horizontally, and 2 cells across the bottom. Use these coordinates (units are tldraw px; canvas ends up ~1500×900):

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

> Maurya's original Lean Canvas tucks "Early Adopters" inside Customer Segments as a sub-list. Splitting it into its own bottom-right cell makes empty-vs-filled obvious at a glance, which is the point of the canvas for our flow. Keep this layout unless the user asks for the classic.

For each cell, draw two things:
1. A `geo` rectangle at the position+size above, no fill, thin border.
2. A `text` shape inside it — header on line 1 (bold or larger), then 2–4 bullets. Add ~16px of inner padding so text doesn't kiss the border.

Add a title above the grid: `Lean Canvas — <idea name> (#NNNN)` at roughly `(0, -60)`.

## Step 6 — Render and save

Call `create_tldraw_diagram` on the `tldraw` MCP with:

- `shapes`: the JSON array you built (as a string).
- `outputPath`: an **absolute** path like `<project-root>/docs/#NNNN-<slug>-canvas.png`. Make sure `docs/` exists; create it if not.
- `format`: `"png"` by default. Offer `"svg"` if the user asks for vector.

Then also write the same shapes JSON to `docs/#NNNN-<slug>-canvas.tldr.json` so the user can re-render or edit later. (The MCP takes shapes JSON directly, so this JSON file *is* the editable source.)

## Step 7 — Report

Tell the user three things:

1. Where the PNG landed (`docs/#NNNN-<slug>-canvas.png`).
2. Which cells were thin or empty, and which source file would fill them (e.g., "Channels is empty — run `marketing-plan` for #0001").
3. The single weakest cell — usually Unfair Advantage or Key Metrics for early-stage ideas — and the cheapest experiment to strengthen it.

If a file with the same name already exists in `docs/`, append a numeric suffix (`-canvas-v2.png`, `-v3`, etc.) — canvases evolve and old versions are useful to keep for diffing.
