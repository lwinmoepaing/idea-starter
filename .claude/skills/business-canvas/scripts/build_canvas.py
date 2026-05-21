#!/usr/bin/env python3
"""
Build the tldraw shapes JSON for a Lean Canvas, applying the warm-light design system.

The model does the thinking (synthesizing each cell's bullets); this script owns the
layout, color system, header/body card split, and — critically — keeps ALL text inside
geo shapes so nothing collapses in headless export. Hand-building 30 shapes by hand is
where coordinate slips and the standalone-text bug creep in; let this do it.

USAGE
  python build_canvas.py <input.json> <output_shapes.json> [--theme color|mono]

Then pass the printed JSON (stdout) straight to the tldraw MCP `create_tldraw_diagram`
`shapes` argument, and keep <output_shapes.json> as the editable source in docs/.

INPUT SHAPE  (only `body` + optional `weak` per cell — headers are fixed)
{
  "id": "0001",
  "name": "Myanmar Serial Reader",
  "cells": {
    "problem":   {"body": "• ...\n• ...", "weak": false},
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
A cell that is missing, blank, or has "weak": true is rendered red ("homework"),
because an honest empty cell is the whole point of a Lean Canvas.
"""
import json, sys, argparse

# --- canonical Lean Canvas layout (tldraw px). Same grid the skill documents. ---
# key: (header label, region, x, y, w, h)
LAYOUT = {
    "problem":   ("PROBLEM",            "how",   0,    0,   300, 600),
    "solution":  ("SOLUTION",           "how",   300,  0,   300, 300),
    "metrics":   ("KEY METRICS",        "how",   300,  300, 300, 300),
    "uvp":       ("UNIQUE VALUE PROP",  "heart", 600,  0,   300, 600),
    "advantage": ("UNFAIR ADVANTAGE",   "who",   900,  0,   300, 300),
    "channels":  ("CHANNELS",           "how",   900,  300, 300, 300),
    "segments":  ("CUSTOMER SEGMENTS",  "who",   1200, 0,   300, 600),
    "cost":      ("COST STRUCTURE",     "money", 0,    600, 750, 300),
    "revenue":   ("REVENUE STREAMS",    "money", 750,  600, 450, 300),
    "adopters":  ("EARLY ADOPTERS",     "who",   1200, 600, 300, 300),
}

REGION_COLOR = {"how": "light-blue", "heart": "orange", "who": "yellow", "money": "light-green"}
INSET, HEAD_H = 7, 44
GRID_W, GRID_H = 1500, 900


def geo(id_, x, y, w, h, color, fill, text="", font="sans", size="m", va="start", al="start"):
    return {"id": id_, "type": "geo", "x": x, "y": y,
            "props": {"geo": "rectangle", "w": w, "h": h, "color": color, "fill": fill,
                      "dash": "solid", "size": size, "font": font, "text": text,
                      "align": al, "verticalAlign": va}}


def build(data, theme):
    name = data.get("name", "Untitled")
    idn = str(data.get("id", "")).lstrip("#").zfill(4)
    cells = data.get("cells", {})

    shapes = [{"type": "cameraUpdate", "width": 1560, "height": 1075, "x": -28, "y": -120}]

    # soft board so the cards float (color theme only; mono stays paper-white)
    if theme == "color":
        shapes.append(geo("board", -12, -112, GRID_W + 24, GRID_H + 136, "grey", "semi"))

    # title band — title text lives INSIDE the geo, so it can never collapse
    shapes.append(geo("band", INSET, -108, GRID_W - 2 * INSET, 62, "orange", "semi",
                      text=f"LEAN CANVAS  ·  {name}  ·  (#{idn})",
                      font="serif", size="l", va="middle"))
    # amber accent rule
    shapes.append(geo("rule", INSET, -42, GRID_W - 2 * INSET, 6, "orange", "solid"))

    for key, (header, region, x, y, w, h) in LAYOUT.items():
        cell = cells.get(key, {}) or {}
        body = (cell.get("body") or "").strip()
        weak = bool(cell.get("weak")) or body == ""
        if weak and body == "":
            body = "⚠ unknown — open question"

        if weak:
            head_color, body_color, body_fill = "red", "light-red", "semi"
        elif theme == "mono":
            head_color, body_color, body_fill = "orange", "orange", "none"
        else:
            head_color = body_color = REGION_COLOR[region]
            body_fill = "semi"

        shapes.append(geo(f"{key}_h", x + INSET, y + INSET, w - 2 * INSET, HEAD_H,
                          head_color, "solid", text=header, font="serif", size="m", va="middle"))
        shapes.append(geo(f"{key}_b", x + INSET, y + INSET + HEAD_H, w - 2 * INSET,
                          h - 2 * INSET - HEAD_H, body_color, body_fill, text=body,
                          font="sans", size="m", va="start"))

    # color-key legend as chips (geo + text inside = robust + self-documenting)
    if theme == "color":
        chips = [("light-blue", "HOW it works"), ("orange", "the HEART"),
                 ("yellow", "WHO it's for"), ("light-green", "the MONEY"),
                 ("light-red", "weak — homework")]
    else:
        chips = [("orange", "section"), ("light-red", "weak — homework")]
    cw = (GRID_W - (len(chips) - 1) * 12) // len(chips)
    x = INSET
    for i, (col, lab) in enumerate(chips):
        shapes.append(geo(f"chip{i}", x, GRID_H + 16, cw, 40, col, "semi",
                          text=lab, font="sans", size="m", va="middle", al="middle"))
        x += cw + 12
    return shapes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--theme", choices=["color", "mono"], default="color")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    shapes = build(data, args.theme)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(shapes, f, ensure_ascii=False, indent=2)
    # compact one-liner for pasting into the MCP `shapes` arg
    print(json.dumps(shapes, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
