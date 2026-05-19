---
name: pain-hunt
description: Build a hunt plan for unsolicited demand evidence — where to find people already complaining about a problem in their own words (Reddit, Twitter/X, Hacker News, niche Discords, G2/Capterra reviews of adjacent products, YouTube comments, Indie Hackers, plus traditional/offline channels), what queries to run, and how to run client interviews or surveys without leading questions. Use when the user wants to validate demand, find proof people already have this problem, asks "where do real users complain", "how do I find evidence for X", or right after a `validate-idea` session before any building starts.
---

Find people already complaining about this problem in their own words. Hypothetical "would you use it?" answers are worthless — only unsolicited pain counts.

Ask one question at a time. Drill on vague answers — push for specifics, not slogans.

Gather first:

1. **Problem in one line** — what exact phrase would a sufferer type into Google or Reddit?
2. **Region & language** — global, US-only, English-only, or specific country/language? This changes which platforms matter.
3. **Audience type** — online-native, traditional/offline, or mixed? Traditional audiences (tradespeople, older users, regulated industries) complain in Facebook groups, trade forums, industry publications, or in person — not Hacker News.
4. **Adjacent products** — which existing tools, services, or workarounds do sufferers already pay for or rage about?

Then save the plan to `workflow/approach/#NNNN-<idea-slug>.md` (create `workflow/approach/` if it doesn't exist). `NNNN` is a zero-padded sequence number, one greater than the highest existing `#NNNN-` prefix in `workflow/approach/` — start at `#0001` if none exist. The counter is per-folder and independent from `workflow/ideas/`. Use this template:

```
# Demand Evidence Plan — <idea>

**Complaint phrasing:** "<words a real sufferer would actually use>"
**Region / language:** <…>
**Audience:** <online-native / traditional / mixed>
**Adjacent products to mine:** <…>

## Where to hunt (online)
- **Reddit** — subs: <list>; query: `site:reddit.com/r/<sub> "<phrase>"`
- **Twitter/X** — accounts, hashtags, advanced-search query
- **Hacker News** — hn.algolia.com `"<phrase>"`, sort by relevance + by date
- **Niche Discords** — which servers; search channel history for the phrase
- **G2 / Capterra** — 1–3★ reviews of <adjacent product>; filter "wish", "frustrating", "missing"
- **YouTube comments** — videos on <topic>, sort Top, scan for pain
- **Indie Hackers** — search posts + comments for the phrase

## Where to hunt (traditional, if applicable)
- Facebook groups, trade-association forums, industry print/online publications
- In-person: meetups, trade shows, direct shop / site visits

## Client interview script (aim for 5–7)
- Opener targets past behavior, never the idea: "Walk me through the last time you <did task>."
- Banned questions: "Would you use…?", "Do you think…?", "Would you pay…?"
- Probe: what they tried, what they paid for, what they hated, what they hacked together, how often it bites them.

## Survey (only after interviews refine the questions)
- Recruit from: <where the unsolicited complaints came from>
- Sample: aim for <N>
- Past-tense, behavior-based questions only. No future hypotheticals, no leading ratings of unbuilt features.

## What to log per signal
- Verbatim quote + source link
- Workarounds already paid for or hacked together
- Intensity language: "every week I…", "I'd kill for…", "I literally pay X to avoid this"

## Kill criteria
- Fewer than ~5 unsolicited complaints after a serious hunt
- All evidence is mild ("would be nice") rather than acute pain
```

If a file with that slug already exists in `workflow/approach/` (under any `#NNNN-` prefix), append a new dated section to that file instead of creating a new numbered one — the number stays fixed for the lifetime of the plan.
