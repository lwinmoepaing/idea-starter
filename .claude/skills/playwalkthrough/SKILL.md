---
name: playwalkthrough
description: Drive a real browser through an MVP's happy-path demo flow with the Playwright MCP, then verify the runtime checks that code can't prove on its own — the count-up that should land on the right number, the streak that should tick, the "money moment" that should complete. Reads plans/{id}-plan-root.md's "Demo flow" as the script, walks each step in Chromium, screenshots it, and writes a pass/fail report to reports/. Use right after `mvp-execute` finishes a build, or whenever the user says "walk the demo", "play through the happy flow", "verify the demo in the browser", "drive the demo with Playwright", "check the [?] runtime items", "/playwalkthrough {id}", or wants the founder's 5-minute pitch path clicked through end-to-end before they present. This is how the deferred `[?]` done-when boxes from a build get resolved into real pass/fail — don't leave them to the human's eyeballs when a browser can confirm them.
---

After `mvp-execute` ships a build, a pile of done-when checks come back as `[?]` — "the dashboard looks alive", "the streak ticks 12→13", "the money moment looks credible". Code review and `npm run build` can't settle those; they need a human (or a browser) to actually click through the app. That's this skill. You open the built MVP in a real Chromium via the **Playwright MCP**, walk the exact pitch script the founder will run, and turn each `[?]` into a verified `[x]` or a flagged failure — with screenshots, so the user sees what you saw.

You are the **driver + reporter**. You do not rewrite the app. If a step is broken you report it and *offer* a fix, then wait for the user's go-ahead before any code changes — the same checkpoint discipline `mvp-execute` uses, because silently editing a shipped demo right before a pitch is exactly when you want a human in the loop.

## Prerequisites — check these first

1. **The Playwright MCP must be connected.** Look for tools named `mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`, etc. If they're absent, the server isn't loaded — tell the user to add it and restart Claude Code (it only loads at session start):
   ```json
   // .mcp.json
   "playwright": { "type": "stdio", "command": "npx", "args": ["@playwright/mcp@latest"] }
   ```
   Then stop — you can't walk anything without the browser. (First browser launch may need `npx playwright install chromium`.)
2. **The MVP must be built.** `plans/{id}-plan-root.md` must exist and `plans/done/{id}-*.md` should hold shipped phases. If the plan is missing, point the user at `mvp-plan`; if `todo/` still has phases, point them at `mvp-execute` — there's no finished demo to walk yet.

## Process

### 1. Get the ID

Normalize to four digits (`1` → `0001`). If not given, ask. Derive the slug from `workflow/ideas/#{id}-*.md` (or the root-plan filename) — you'll need it for the report path, e.g. `tiny-workout-consistency`.

### 2. Read the script and the open questions

- `plans/{id}-plan-root.md` — the **`## Demo flow`** section is your script. Each numbered item is one walkthrough step with an embedded *expected observation* ("a 12-day streak", "today's calendar dot is now green", "Premium badge appears"). The **Demo target** line tells you which screen is the hero shot. Read the **Assumptions** too — they tell you what's deliberately fake (e.g. "store reseeds on reload", "any phone number works") so you don't flag intended behavior as a bug.
- `plans/done/{id}-*.md` — collect every `[?]` (and any unchecked `[ ]`) item from the "Done when" lists. These are the open questions the walkthrough exists to answer. Map each one to the demo-flow step that exercises it, so the report can close the loop: phase 04's "`[?]` dashboard looks alive" is settled by step 1, phase 05's "`[?]` celebration lands" by step 3-4, and so on.

The Demo flow is the source of truth, not your memory of how you built it — the user may have edited the plan since.

### 3. Ensure the dev server is up

Check the port before launching anything: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/` (and `lsof -ti:5173`). If it's already serving, reuse it. If not, start it in the background — `cd mvp && npm run dev` with `run_in_background: true` — wait briefly, read the log, and grab the **actual** `Local:` URL (Vite picks 5174+ if 5173 is taken; don't assume). If `mvp/node_modules` is missing, `npm install` first.

### 4. Walk the happy path in the browser

Drive snapshot-first, not selector-first. The Playwright MCP's `browser_snapshot` returns an accessibility tree with a `ref` for each element — read it, find the element by its visible text/role, then act on it by `ref`. This adapts to whatever the build actually rendered instead of betting on CSS selectors that may not exist.

The loop for each demo-flow step:
1. **Settle the page.** Animations are part of these demos — a streak counts up from 0, panels fade/stagger in. Give them a beat (`browser_wait_for` on the expected text, or a short time wait) before you read or shoot, or you'll screenshot a half-played animation and misjudge it.
2. **Snapshot** to see current state and get refs.
3. **Act** — `browser_navigate`, `browser_click`, `browser_type` — to perform the step.
4. **Verify** the step's expected observation against a fresh snapshot. Did the number land on what the script claims? Did the route change? Did the badge appear?
5. **Screenshot** with `browser_take_screenshot` into the report's screens folder, named by step (`01-dashboard.png`, `03-session-finish.png`).
6. **Record** PASS / FAIL / UNCLEAR with one line of what you actually observed vs. what was expected.

Two things that matter for these specific demos:
- **Use the Skip / fast-forward control** in any timed player. Pitch demos are built so a 5-minute workout can be skipped to the finish — don't sit through real-time countdowns. The Demo flow usually says so explicitly.
- **Check the console.** Call `browser_console_messages` after the run (and after the heaviest interaction). A polished demo should have no red errors; surface any in the report, since a console error mid-pitch is exactly the kind of thing the demo-polish phase was supposed to prevent.

Optional, if a phase left a `[?]` about responsive/mobile width: `browser_resize` to ~390px wide, snapshot the hero screen, and note whether the shell degrades gracefully.

### 5. Write the report + screenshots

Create `reports/` if it doesn't exist. Write the markdown report to `reports/#{id}-{slug}-walkthrough.md` and put screenshots in `reports/#{id}-{slug}-screens/`. Re-running overwrites — a walkthrough reflects the current build, it's not an append-only log.

Use this structure:

```markdown
# Walkthrough — {App name} (#{id})

**Run:** {date} · **URL:** {dev url} · **Result:** {N}/{M} steps passed

## Demo flow
| # | Step (from root plan) | Expected | Observed | Result | Shot |
|---|-----------------------|----------|----------|--------|------|
| 1 | Land on / | 12-day streak, ~78% consistency | streak rendered 12, consistency 75% | PASS | 01-dashboard.png |
| ... |

## Runtime checks resolved
Each `[?]` / `[ ]` from plans/done/{id}-*.md, now answered:
- [x] (phase 04) dashboard "looks alive" — confirmed, step 1
- [ ] (phase 05) celebration lands — FAILED, see step 4
- ...

## Console
{clean, or the errors observed}

## Failures & proposed fixes
{omit if all green; otherwise one block per failure — see step 6}
```

### 6. On a broken step — report, then offer a fix (don't just dive in)

For each failure, give the user enough to decide:
- **What broke** — the step, expected vs. observed, the screenshot.
- **Likely cause** — trace it to a phase/file. Read the relevant `plans/done/{id}-*.md` and the implicated source under `mvp/src/` to pin it down (e.g. "the streak shows 12 and never ticks — the seed marks today done, so `completeToday` no-ops"). A concrete diagnosis is worth more than "step 4 failed".
- **Proposed fix** — the specific change, scoped small.

Then **wait for the user's go-ahead.** When they approve, delegate the change to a `phase-executor` sub-agent (the house pattern — keeps code-writing in the agent that owns it; pass it the file and the precise change), or make a small targeted edit yourself for a one-liner. After the fix, re-walk just the affected step(s) and update the report. Don't renumber or re-ship phase files — the build already happened; you're patching it.

If multiple steps fail, present them all at once so the user can triage, rather than stopping at the first red.

### 7. Final summary

Tell the user: the result (`N/M` passed), the report path, where the screenshots are, the dev URL (still live), and a one-line callout of any `[?]` that flipped to FAIL. If everything's green, say so plainly — the founder can walk the pitch with confidence.

## Scope — what this skill does not do

- **It doesn't rebuild the app.** It verifies and reports. Fixes happen only with user approval, scoped to what the walkthrough found.
- **It's happy-path only.** You're confirming the pitch script runs, not fuzzing edge cases or auth or error states — those are out of demo scope by design.
- **It trusts the Assumptions.** Reseed-on-reload, fake payments, English-only copy, desktop-first — if the root plan calls it a deliberate shortcut, it's not a bug.
- **It doesn't deploy, commit, or run a test suite.** There isn't one; this *is* the test.
```