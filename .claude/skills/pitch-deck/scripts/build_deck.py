#!/usr/bin/env python3
"""Render a pitch deck PDF from a slide-spec JSON.

This is the deterministic half of the `pitch-deck` skill: all the judgment
(what goes on each slide) happens upstream in the deck-builder sub-agent, which
distills a `#NNNN-<slug>-pitch.md` into the spec this script consumes. Keeping
rendering here means every deck looks the same and the sub-agent never has to
reinvent reportlab layout code.

Output is a landscape 16:9 deck (PowerPoint's 13.333" x 7.5" = 960 x 540 pt) in
a bold, type-driven, one-idea-per-slide style — the look ref.md's "Presentation"
weight rewards: readable from the back of the room.

Usage:
    python build_deck.py <spec.json> <output.pdf>

Spec schema (see references/spec-schema.md for the annotated version):
    {
      "title":    "FridgeChef",                 # used for PDF metadata
      "accent":   "#E8553A",                    # optional, one accent color
      "slides": [
        {"kind": "title",     "title": "...", "subtitle": "...", "meta": "..."},
        {"kind": "bullets",   "label": "THE PROBLEM", "headline": "...",
                              "bullets": ["...", "..."]},
        {"kind": "steps",     "label": "LIVE DEMO", "headline": "...",
                              "steps": ["...", "..."]},
        {"kind": "statement", "headline": "the one line to land on",
                              "meta": "..."}
      ]
    }

Only `kind` is required per slide; missing fields render as empty. Unknown kinds
fall back to `bullets`. The script never asks questions — it renders what it's
given, so keep slide text tight upstream (≤6 bullets, headlines that fit a line
or two). Long text wraps automatically; if a slide overflows its body area the
body font steps down once rather than spilling off the page.
"""
import json
import sys

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

# 16:9 landscape, in points. Matches PowerPoint/Keynote "Widescreen".
PAGE_W, PAGE_H = 960, 540
MARGIN = 72  # generous left/right gutter — whitespace is the point

# Palette. Charcoal (not pure black) reads softer; gray for body keeps the
# headline dominant. Accent is the only color that varies per deck.
INK = HexColor("#1A1A1A")
BODY = HexColor("#555555")
PAPER = HexColor("#FFFFFF")
DEFAULT_ACCENT = "#E8553A"

FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def tint(color, factor):
    """Lighten a color toward white by `factor` (0=unchanged, 1=white)."""
    return Color(
        color.red + (1 - color.red) * factor,
        color.green + (1 - color.green) * factor,
        color.blue + (1 - color.blue) * factor,
    )


def wrap(text, font, size, max_width):
    """Word-wrap `text` into lines that fit `max_width` at the given font."""
    return simpleSplit(str(text), font, size, max_width)


def draw_tracked(c, text, x, y, font, size, color, tracking, center_w=None):
    """Draw a single line with manual letter-spacing.

    reportlab 4.x has no public canvas char-spacing setter, so we place each
    glyph by hand. Tracking on uppercase kickers is what makes the minimal
    style read as intentional rather than plain. If `center_w` is given the
    line is centered within that width.
    """
    text = str(text)
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    cx = (center_w - total) / 2 if center_w is not None else x
    for ch, w in zip(text, widths):
        c.drawString(cx, y, ch)
        cx += w + tracking
    return total


def draw_wrapped(c, text, x, y, font, size, max_width, leading, color):
    """Draw wrapped text top-down from baseline `y`; return the y below it."""
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(text, font, size, max_width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_kicker(c, label, accent, x, y):
    """Small uppercase accent label that sits above a headline."""
    if not label:
        return y
    draw_tracked(c, str(label).upper(), x, y, FONT_BOLD, 14, accent, tracking=2)
    return y - 8


def fit_body_size(items, base_size, leading_ratio, max_width, max_height,
                  font, gap):
    """Pick a body font size so all items fit max_height; step down once."""
    for size in (base_size, base_size - 3):
        leading = size * leading_ratio
        total = 0
        for item in items:
            lines = len(wrap(item, font, size, max_width))
            total += lines * leading + gap
        if total <= max_height:
            return size
    return base_size - 3


# ---- slide renderers --------------------------------------------------------


def slide_title(c, s, accent):
    """Cover slide: solid accent field, white type, idea name dominant."""
    c.setFillColor(accent)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    x = MARGIN
    title = s.get("title", "")
    size = 60
    # Shrink the title until it fits two lines, so long product names behave.
    while size > 34 and len(wrap(title, FONT_BOLD, size, PAGE_W - 2 * MARGIN)) > 2:
        size -= 4
    lines = wrap(title, FONT_BOLD, size, PAGE_W - 2 * MARGIN)
    block_h = len(lines) * size * 1.1
    y = PAGE_H / 2 + block_h / 2 - size * 0.8
    c.setFont(FONT_BOLD, size)
    c.setFillColor(PAPER)
    for line in lines:
        c.drawString(x, y, line)
        y -= size * 1.1

    subtitle = s.get("subtitle", "")
    if subtitle:
        y -= 10
        draw_wrapped(c, subtitle, x, y, FONT, 22, PAGE_W - 2 * MARGIN, 28,
                     PAPER)

    meta = s.get("meta", "")
    if meta:
        draw_tracked(c, str(meta).upper(), x, MARGIN - 24, FONT_BOLD, 13,
                     PAPER, tracking=1)


def _content_header(c, s, accent):
    """Shared kicker + headline + accent rule for content slides.

    Returns the y baseline where the body should start.
    """
    x = MARGIN
    top = PAGE_H - MARGIN
    y = draw_kicker(c, s.get("label", ""), accent, x, top)

    headline = s.get("headline", "")
    hsize = 34
    max_w = PAGE_W - 2 * MARGIN
    while hsize > 22 and len(wrap(headline, FONT_BOLD, hsize, max_w)) > 2:
        hsize -= 2
    y = draw_wrapped(c, headline, x, y - hsize, FONT_BOLD, hsize, max_w,
                     hsize * 1.12, INK)

    # Short accent rule under the headline — the one graphic flourish.
    y -= 6
    c.setFillColor(accent)
    c.rect(x, y, 56, 4, fill=1, stroke=0)
    return y - 30


def slide_bullets(c, s, accent):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    y = _content_header(c, s, accent)

    bullets = [b for b in s.get("bullets", []) if str(b).strip()]
    x = MARGIN
    text_x = x + 24
    max_w = PAGE_W - text_x - MARGIN
    size = fit_body_size(bullets, 19, 1.35, max_w, y - MARGIN, FONT, 14)
    leading = size * 1.35
    for b in bullets:
        lines = wrap(b, FONT, size, max_w)
        # Accent dot aligned to the first line's cap height.
        c.setFillColor(accent)
        c.circle(x + 5, y + size * 0.32, 4, fill=1, stroke=0)
        c.setFont(FONT, size)
        c.setFillColor(BODY)
        for line in lines:
            c.drawString(text_x, y, line)
            y -= leading
        y -= 14


def slide_steps(c, s, accent):
    """Like bullets but numbered — used for the demo walkthrough beats."""
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    y = _content_header(c, s, accent)

    steps = [s_ for s_ in s.get("steps", []) if str(s_).strip()]
    x = MARGIN
    text_x = x + 34
    max_w = PAGE_W - text_x - MARGIN
    size = fit_body_size(steps, 19, 1.35, max_w, y - MARGIN, FONT, 16)
    leading = size * 1.35
    for i, step in enumerate(steps, 1):
        lines = wrap(step, FONT, size, max_w)
        # Accent numbered chip.
        chip_r = 11
        cy = y + size * 0.32
        c.setFillColor(accent)
        c.circle(x + chip_r, cy, chip_r, fill=1, stroke=0)
        c.setFont(FONT_BOLD, 12)
        c.setFillColor(PAPER)
        c.drawCentredString(x + chip_r, cy - 4, str(i))
        c.setFont(FONT, size)
        c.setFillColor(BODY)
        for line in lines:
            c.drawString(text_x, y, line)
            y -= leading
        y -= 16


def slide_statement(c, s, accent):
    """Dark slide, big centered line — for the closing / mission beat."""
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    headline = s.get("headline", "")
    max_w = PAGE_W - 2 * MARGIN
    size = 44
    while size > 26 and len(wrap(headline, FONT_BOLD, size, max_w)) > 4:
        size -= 2
    lines = wrap(headline, FONT_BOLD, size, max_w)
    leading = size * 1.18
    block_h = len(lines) * leading
    y = PAGE_H / 2 + block_h / 2 - size
    c.setFont(FONT_BOLD, size)
    c.setFillColor(PAPER)
    for line in lines:
        c.drawCentredString(PAGE_W / 2, y, line)
        y -= leading

    # Accent period — a small full stop centered under the line.
    c.setFillColor(accent)
    c.rect(PAGE_W / 2 - 18, y - 4, 36, 4, fill=1, stroke=0)

    meta = s.get("meta", "")
    if meta:
        draw_tracked(c, str(meta).upper(), 0, MARGIN - 24, FONT_BOLD, 12,
                     tint(INK, 0.55), tracking=1, center_w=PAGE_W)


RENDERERS = {
    "title": slide_title,
    "bullets": slide_bullets,
    "steps": slide_steps,
    "statement": slide_statement,
}


def draw_page_number(c, n, accent):
    c.setFont(FONT, 10)
    c.setFillColor(tint(INK, 0.6))
    c.drawRightString(PAGE_W - MARGIN, MARGIN - 30, str(n))


def build(spec, out_path):
    accent = HexColor(spec.get("accent") or DEFAULT_ACCENT)
    slides = spec.get("slides", [])
    if not slides:
        raise SystemExit("spec has no slides")

    c = canvas.Canvas(out_path, pagesize=(PAGE_W, PAGE_H))
    c.setTitle(spec.get("title", "Pitch Deck"))
    c.setAuthor("pitch-deck skill")

    for i, s in enumerate(slides):
        kind = s.get("kind", "bullets")
        renderer = RENDERERS.get(kind, slide_bullets)
        renderer(c, s, accent)
        # Page numbers on interior content slides only — not the cover/closing.
        if kind in ("bullets", "steps") and i not in (0, len(slides) - 1):
            draw_page_number(c, i + 1, accent)
        c.showPage()

    c.save()


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path) as f:
        spec = json.load(f)
    build(spec, out_path)
    print(f"wrote {out_path} ({len(spec.get('slides', []))} slides)")


if __name__ == "__main__":
    main()
