# #0007 — ShiftLedger

**Date:** 2026-05-21
**Drop:** #0007 — extends #0003
**Demo target:** A shift manager closes the night and payroll-ready hours are already correct — no spreadsheet, no Sunday reconciliation.

## Story
The founder managed three coffee shops and spent every Sunday rebuilding the week's hours from paper sign-in sheets and a group chat full of "can someone cover me?" messages. One payroll run was wrong by 11 hours across the team and it took two days to untangle. The realization: the hours data already exists in a dozen places — it's just never in one place when payroll needs it.

## Idea
ShiftLedger is the closing-shift companion for small multi-location service businesses. We already shipped scheduling and swaps (#0003); this drop adds the part owners actually lose sleep over — turning what really happened on the floor into payroll-ready hours automatically, so nobody hand-tallies a sign-in sheet again.

## Problem
For a small operator, payroll is a weekly act of archaeology. Hours live on paper sheets, in text-message cover requests, and in the manager's memory. Reconciling them is hours of unpaid Sunday work, and mistakes cost real money and trust. One owner described it as *"doing detective work every week to pay people what I already owe them."* Off-the-shelf payroll assumes the hours are already clean; for these businesses they never are.

## Solution
What we built, as the demo runs:
- "Manager hits **Close night** → every clock-in/out for the shift is summed per person"
- "Swaps and approved cover requests are already folded in — the hours reflect who actually worked"
- "Anything ambiguous surfaces as a one-tap exception to confirm, not a spreadsheet to rebuild"
- Result: by the time the manager locks up, the week's payroll hours are correct

## Purpose
Small operators should spend Sunday with their families, not reverse-engineering their own payroll. ShiftLedger makes the hours true the moment the night closes.

## What shipped this drop
- Close-night flow that aggregates clock events per employee
- Swap/cover reconciliation folded into the hours total
- Exception queue for ambiguous punches
- Payroll-ready hours export

## Source files
- `workflow/ideas/#0007-shiftledger.md`
- `workflow/approach/#0007-shiftledger.md`
- `workflow/marketing/#0007-shiftledger.md` _(missing — no GTM evidence yet)_
- `plans/#0007-plan-root.md`
- `plans/done/#0007-*.md` (4 phases)
