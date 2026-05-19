---
name: validate-idea
description: Stress-test a business idea by drilling into the underlying problem, target user, and willingness to pay before any code is written. Use when the user wants to validate an idea, says "validate this idea", "is this worth building", "should I build this", drops a new product/business concept, or mentions an `workflow/ideas/` entry.
---

Stress-test the user's business idea before they build anything. Start with the problem, not the solution.

Ask one question at a time. Drill into vague answers — "everyone", "lots of pain", "it's better" don't pass. Demand a concrete example or moment.

Cover in order:

1. **Problem** — which exact problem are you solving? Describe a real moment it happens to a real person.
2. **User** — who has this problem? How many? How are they solving it today?
3. **Pain** — how often does it hurt, and enough that they'd pay? How much?
4. **Alternatives** — what do they use instead, and why isn't that enough?
5. **You** — why you? Unfair advantage, insight, or distribution.

End by naming the weakest link in the idea and the single riskiest assumption to test next.

Then save the session as `workflow/ideas/#NNNN-<slug>.md` — kebab-case slug from the idea name; `NNNN` is a zero-padded sequence number, one greater than the highest existing `#NNNN-` prefix in `workflow/ideas/` (start at `#0001` if none exist). Use this template:

```
# <idea name>

**Date:** <YYYY-MM-DD>
**Verdict:** <go / kill / needs more evidence>

## Problem
<answer>

## User
<answer>

## Pain & willingness to pay
<answer>

## Alternatives
<answer>

## Why you
<answer>

## Weakest link
<one line>

## Riskiest assumption to test next
<one line + how to test it cheaply>
```

If a file with that slug already exists in `workflow/ideas/` (under any `#NNNN-` prefix), append a new dated section to that file instead of creating a new numbered one — the number stays fixed for the lifetime of the idea.
