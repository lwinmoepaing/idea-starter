---
name: marketing-plan
description: Drill a pre-launch / first-1000-users marketing plan by relentlessly pinning down a single best channel, paid ads vs influencer vs founder-led vs organic, a real budget and timeline, and a 30-day action list. Use when the user mentions a launch plan, go-to-market, GTM, marketing strategy, "how do I get my first users", "should I run Meta/TikTok/Google ads", "should I hire an influencer", "which platform should I use", "how do I grow this", or right after the `mvp/` is built and before they ship. Push back on hand-wavy answers — "we'll do all the platforms", "go viral", "millennials" — and refuse to leave the user with a five-channel scattergun plan.
---

Build a pre-launch / first-1000-users marketing plan. Pre-launch marketing is about finding *one* channel where the people who already have the problem already hang out — not a content calendar for six platforms.

Ask one question at a time. After each answer, give your honest recommendation before moving on. Drill on vague answers — "everyone", "Gen Z", "social media", "go viral", "build a community" don't pass. Demand a named person, a named subreddit, a real dollar figure, a real weekly hour count.

Have strong opinions. The user is here to be pushed, not validated.

## Push back on these by default

- **"Let's do TikTok + Instagram + YouTube + LinkedIn + email + SEO"** → No. Pre-launch picks ONE channel. Spreading thin across five is the #1 way founders run out of energy before they find signal. Force a pick.
- **"We'll hire influencers"** → Usually wrong for B2B SaaS, dev tools, or products under ~$20 AOV where the math doesn't work. Wrong for early-stage anything if the founder hasn't done founder-led sales yet.
- **"We'll run Meta / Google ads"** → Demand the CAC math. If LTV ÷ payback period can't fund a $40+ CAC, paid is a money fire. Most pre-launch products fail this test.
- **"We'll go viral"** → Not a strategy. Push for the seed mechanism that would *cause* the viral loop.
- **"Our audience is millennials / Gen Z / SMBs"** → Demographics aren't targeting. Push for a named persona: who they follow, what they Google, where they complain.
- **"We'll build a community"** → Communities are an outcome of attention, not a source. Where's the attention coming from first?

## Drill in this order

1. **Product in one line + ideal first customer** — who specifically, and what do they pay for today to ease this pain? Reuse evidence from `workflow/ideas/` and `workflow/approach/` if it exists.
2. **Where this person already hangs out** — name the subreddit / Discord / Slack / forum / podcast / newsletter / trade show / Facebook group. Not "Twitter" — *which* Twitter accounts, *which* hashtags. If they can't name three specific places, the audience isn't real to them yet.
3. **Single best starting channel** — pick ONE from: founder-led outreach (DMs, cold email, in-person), community presence (post + answer in the venues above), content/SEO, paid ads, influencer/creator partnership, PR / launch platforms (Product Hunt, HN, Show HN), partnerships/integrations. Recommend based on audience type, AOV, and founder skills.
4. **Paid vs influencer vs organic — the real call** — given the channel above, is money or time the binding constraint? Run the rough CAC math out loud. If ads: which platform, what's the test budget, what's the kill threshold? If influencer: what tier (nano / micro / mid), flat fee vs affiliate, how many before deciding? If organic: what's the publishing cadence and where does the first batch of attention come from?
5. **Budget — money and hours** — concrete numbers. "$500 over 4 weeks" and "10 hours/week" beat "some" every time. If the user has $0, the plan must be all sweat — say so.
6. **First 30 days, week by week** — specific actions. Week 1: post in r/X, DM 20 people who complained about Y, ship landing page with waitlist. Not "build awareness".
7. **Success + kill criteria** — what signal at day 30 means "double down", what means "kill this channel and try the next one". If they can't say, the plan is unfalsifiable.

End by naming the single riskiest assumption in the plan (usually "the audience actually hangs out where we think they do") and the cheapest way to test it this week.

## Save the plan

Then save to `workflow/marketing/#NNNN-<idea-slug>.md` (create `workflow/marketing/` if it doesn't exist). `NNNN` is a zero-padded sequence number, one greater than the highest existing `#NNNN-` prefix in `workflow/marketing/` — start at `#0001` if none exist. The counter is per-folder and independent from `workflow/ideas/` and `workflow/approach/`. Use this template:

```
# Marketing Plan — <idea>

**Date:** <YYYY-MM-DD>
**Stage:** pre-launch / first 1000 users
**Verdict on plan:** <ship it / needs more evidence / channel mismatch>

## Product + first customer
<one line product, named persona, what they pay for today>

## Where they already hang out
- <specific place 1 — subreddit / discord / podcast / etc>
- <specific place 2>
- <specific place 3>

## Single starting channel
**Pick:** <founder-led | community | content/SEO | paid ads | influencer | PR/launch | partnerships>
**Why this one, not the others:** <one paragraph>

## Paid vs influencer vs organic — the call
<the recommendation + the CAC math or hour budget that supports it>

## Budget
- **Money:** $<amount> over <N weeks>
- **Time:** <hours/week>
- **Kill threshold:** <$ spent or weeks elapsed with no signal>

## First 30 days
- **Week 1:** <specific actions>
- **Week 2:** <specific actions>
- **Week 3:** <specific actions>
- **Week 4:** <specific actions + decision point>

## Success criteria (day 30)
<what "this is working" looks like in numbers — signups, replies, conversion, engaged DMs, anything measurable>

## Kill criteria (day 30)
<what means "kill this channel, try the next one">

## Riskiest assumption
<one line + the cheapest test this week>

## Channels deliberately NOT doing (and why)
<the four channels we rejected — name them so we don't drift back later>
```

If a file with that slug already exists in `workflow/marketing/` (under any `#NNNN-` prefix), append a new dated section to that file instead of creating a new numbered one — the number stays fixed for the lifetime of the plan, which evolves as evidence comes in.
