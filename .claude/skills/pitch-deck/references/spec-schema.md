# Deck spec schema

`build_deck.py` consumes one JSON file describing the deck. The deck-builder
sub-agent writes this file (to `docs/#{id}-<slug>-deck.json`) and then renders it.
Keeping the spec on disk means a human can tweak wording and re-render without
regenerating from the pitch.

## Top level

| Field    | Required | Notes |
|----------|----------|-------|
| `title`  | no       | Goes into the PDF's metadata title. Use the idea name. |
| `accent` | no       | One hex color, e.g. `"#E8553A"`. Drives cover, kickers, dots, rules, the closing period. Defaults to `#E8553A`. Pick something legible as a solid background (the cover fills with it). |
| `slides` | **yes**  | Ordered array of slide objects. |

## Slide kinds

Every slide needs a `kind`. Unknown kinds render as `bullets`.

### `title` — the cover
```json
{"kind": "title", "title": "FridgeChef",
 "subtitle": "Turn tonight's random fridge into dinner.",
 "meta": "#0001 · 2026-05-21"}
```
Solid accent field, white type. `title` shrinks to fit two lines. `subtitle` is
the one-line hook (use the pitch's Demo target). `meta` renders small-caps at the
bottom — use `"#<id> · <date>"`.

### `bullets` — the workhorse (Problem, Solution, Impact)
```json
{"kind": "bullets", "label": "THE PROBLEM",
 "headline": "6pm, a full fridge, and still no idea what's for dinner",
 "bullets": ["short point one", "short point two", "short point three"]}
```
`label` is the uppercase kicker. `headline` is the slide's single claim (shrinks
to fit two lines). Keep `bullets` to **2–5 short items** — one line each is ideal.
A small accent dot precedes each. Interior bullets slides get a page number.

### `steps` — the live-demo walkthrough
```json
{"kind": "steps", "label": "LIVE DEMO",
 "headline": "Three taps from fridge to plate",
 "steps": ["Land on /cook → tick what's in the fridge",
           "Tap Suggest → recipes ranked by what you have",
           "Pick one → step-by-step mode"]}
```
Same as `bullets` but each item gets a numbered accent chip. Use for the demo
flow so the founder can run the screen while this is up.

### `statement` — the closing line
```json
{"kind": "statement",
 "headline": "Nobody should waste a night staring into a full fridge.",
 "meta": "FridgeChef · #0001"}
```
Dark slide, big centered line, accent full-stop underneath. Use once, at the end,
for the single sentence the pitch lands on (the pitch's Purpose). No page number.

## Hard rules for whoever writes the spec

- **Plain text only.** The renderer prints characters literally — strip markdown
  (`*`, `_`, `` ` ``, `#`, `>`) and link syntax. `*cook*` would show the asterisks.
- **Tight text.** Headlines ≤ ~10 words; bullets ≤ ~14 words. Overflow auto-wraps
  and the body font steps down once, but a wall of text defeats the format.
- **Unicode is fine** for arrows (→), em dashes (—), and curly quotes — Helvetica
  has them. Avoid emoji and sub/superscript glyphs (they render as boxes).
