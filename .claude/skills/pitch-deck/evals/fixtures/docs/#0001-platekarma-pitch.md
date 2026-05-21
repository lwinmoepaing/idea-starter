# #0001 — PlateKarma

**Date:** 2026-05-21
**Drop:** #0001
**Demo target:** Snap your fridge shelf, get three dinners you can cook tonight with zero shopping.

## Story
The founder cooks for one and kept throwing out half a bag of spinach every week. The breaking point was a Tuesday night standing in front of a full fridge, ordering $24 of pad thai because nothing in there "added up to a meal." Recipe apps all assumed a shopping trip first. Nobody had built the thing that starts from *what you already have at 6pm*.

## Idea
PlateKarma is a cook-tonight app for people who have food but no plan. You tell it what's in the fridge — by photo or a few taps — and it ranks dinners you can make right now, no shopping trip, no missing-ingredient dead ends. It's for the solo cook and the tired parent on a weeknight, not the meal-prep hobbyist.

## Problem
The 6pm fridge stare: a full fridge and still "nothing to eat." In the user's words: *"I have food but nothing to cook."* Recipe apps make it worse — they surface a beautiful recipe, then list four ingredients you don't have, so you give up and order in. Meanwhile the produce you did buy rots. People reported throwing out groceries weekly and feeling guilty about both the waste and the takeout spend.

## Solution
What we built, as the demo runs:
- "Land on `/cook` → snap the fridge shelf or tick a few staples" — the app reads what you have
- "Tap **Suggest** → three dinners ranked by how much you already have" — no recipe needs a shopping trip
- "Pick one → step-by-step cook mode" — no scrolling past a life story, just the steps
- Result: dinner decided in under a minute, and the spinach gets used

## Purpose
Nobody should waste food — or a whole evening — staring into a full fridge. PlateKarma turns "I have nothing to eat" into dinner on the table.

## Demo flow (for reference)
1. Open `/cook` — the fridge intake screen loads with a camera tile and a quick-add list of staples.
2. Tap three staples (eggs, spinach, parmesan) and hit **Suggest**.
3. Three recipe cards animate in, each showing a "you have 6 of 7 ingredients" match bar.
4. Tap the top card → cook mode opens at step 1 with a big timer.
5. Hit **I cooked this** → a "2 ingredients saved from the bin" confirmation slides up.

## What shipped this drop
- Fridge intake screen with photo tile + quick-add staples
- Recipe ranking by ingredient-match score
- Step-by-step cook mode with timers
- "Saved from the bin" waste-tracking confirmation

## Source files
- `workflow/ideas/#0001-platekarma.md`
- `workflow/approach/#0001-platekarma.md`
- `workflow/marketing/#0001-platekarma.md`
- `plans/#0001-plan-root.md`
- `plans/done/#0001-*.md` (4 phases)
