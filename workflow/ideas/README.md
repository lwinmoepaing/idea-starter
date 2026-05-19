# workflow/ideas/

Raw idea write-ups from the `validate-idea` skill. One file per idea: **Problem → User → Pain → Alternatives → Why you**, ending with the weakest link and the single riskiest assumption to test next.

## File format

`#NNNN-<slug>.md` — zero-padded sequence, kebab-case slug from the idea name (e.g. `#0001-realtime-collab-editor.md`). Re-running on the same idea appends a new dated section; the number and slug stay fixed.

## Template

```
# <idea name>

**Date:** <YYYY-MM-DD>
**Verdict:** <go / kill / needs more evidence>

## Problem
## User
## Pain & willingness to pay
## Alternatives
## Why you
## Weakest link
## Riskiest assumption to test next
```

Next stop: `pain-hunt` builds the demand-evidence plan in `../approach/`.
