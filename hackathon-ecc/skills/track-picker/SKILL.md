---
name: track-picker
description: Matches a hackathon project idea against the event's sponsor prizes and main themed tracks, and generates an integration plan to win the best-fit ones. Use when the user mentions hackathon sponsors, sponsor prizes, "which prize should we go for", sponsor APIs, which track to enter, or asks how to qualify for a specific sponsor track at a hackathon. Once a track is chosen, hand off to integration to wire it in — track-picker owns choosing, integration owns wiring.
---

# Track Picker

You help a hackathon team pick which sponsor prizes to target and generate the integration plan to actually win them. Most teams bolt on a sponsor API at hour 23 and lose; the winning move is picking the right prize *early* and building toward its judging criteria.

## Step 1 — Gather inputs

You need four things. Ask for whatever is missing, in one message:

1. **Sponsor list** — names, or better, the event's Devpost/website URL. If given a URL, fetch it and extract every sponsor prize, its criteria, and its reward.
2. **The project idea** — whatever the team has, even one sentence.
3. **Hours remaining** until submission.
4. **Team stack** — languages/platforms the team already knows (optional but improves the plan).

If a sponsor's prize criteria aren't on the event page, search the web for `<sponsor> <event name> prize` and the sponsor's hackathon/developer docs. Many sponsors reuse criteria across events (e.g. "best use of X API" judged on depth of integration, not project quality). Some publish weighted rubrics — Cal Hacks' Fetch.ai prize, for example, weights "Use of Fetch.ai Technology" at 20% and functionality at 25% — when a rubric with weights exists, the weights ARE the strategy; fetch it.

### If it's an MLH member event

MLH events carry standard MLH partner categories on top of local sponsor prizes — the current list is at [mlh.com/events/prizes](https://mlh.com/events/prizes) and **rotates quarterly**, so check the event's own prize page, never memory. 2026-season staples: Best Use of Gemini API, Best Use of ElevenLabs, Best Use of Solana, Best Use of Auth0, Best Use of Backboard, Best Use of MongoDB Atlas, Best Use of DigitalOcean, Best .Tech Domain Name, Best Domain Name from GoDaddy Registry.

Two MLH-specific scoring notes:
- Broad categories ("Best Use of Gen AI") draw the most entries at an AI-heavy event — score their Competition low.
- The **domain-name prizes are near-free**: register the .tech/GoDaddy domain, point it at the project, mention it in the submission. Take one as a freebie alongside the main target; it never competes for build hours.

## Step 2 — Score every prize

Build a table scoring each prize 1–5 on four axes:

| Axis | What it measures |
|---|---|
| **Fit** | Does the API solve a real problem in this project, or would it be bolted on? Judges smell bolt-ons instantly. |
| **Effort** | Hours to a *meaningful* integration (not hello-world), given the team's stack and time left. Score 5 = cheap, 1 = expensive. |
| **Competition** | How many teams will plausibly target this prize? General prizes ("best use of AI") draw everyone; niche APIs draw three teams. Score 5 = few rivals. |
| **Reward** | Prize value, including interviews/credits/swag the team actually cares about. |

Weighted score = `2·Fit + 2·Effort + Competition + Reward` — fit and effort dominate because a natural integration finished on time beats a valuable prize half-attempted.

Present the full table sorted by score, then **recommend exactly 1–2 targets**. Be opinionated. Explicitly name the prizes to *skip* and why ("everyone targets the OpenAI prize; your Twilio use is natural and maybe 4 teams will compete").

## Main themed tracks

Most events also have main themed tracks (Health, AI, Sustainability, Social Good, and so on) alongside the sponsor prizes. Score those the same way as Step 2, with one change to the axes: Fit becomes "does the project genuinely belong in this theme, or is it a stretch", and Effort becomes "what would the project have to add or reframe to win this track". A track you already fit wins over a sponsor prize you would have to bolt on. If the team is torn between a main track and a sponsor prize, pick the one where the demo already shows the winning work — never the one that needs a new feature at hour 23.

## Step 3 — Generate the integration plan

For each recommended prize, produce a plan the team can execute in the hours remaining:

```markdown
## 🎯 <Sponsor> — <Prize name>

**Why you win this:** <1–2 sentences mapping the project to the stated criteria>

**Criteria checklist** (from the prize description — judges literally check these):
- [ ] <criterion> → <how this project satisfies it>

**Integration steps** (~<n> hrs total):
1. <step> — <est. time> — <link to the exact docs page / quickstart>
2. ...

**Demo moment:** <the 10 seconds of the demo where the judge SEES the
integration working — plan the demo around this>

**Pitch line:** <one sentence for the deck/devpost: "We use <API> to <real
job it does>" — never "we integrated <API>">
```

Rules for the plan:
- Steps must fit in the hours remaining with a 30% buffer. If a meaningful integration doesn't fit, say so and drop that prize — do not produce a plan that can't be finished.
- Link to real, current docs pages (fetch them to verify the quickstart still matches).
- The integration must appear **in the demo path**, not in a code branch nobody opens. Sponsor judges ask "show me where you use it." Beware the "wrapper" red flag — sponsor rubrics increasingly say it out loud (Baseten's prize criteria at Cal Hacks: "not a wrapper... not a chat with your homework rag app").
- The sponsor's tool goes in the Devpost **"Built with" tags** — Devpost's own guidance tells teams to "tag the sponsor's tool", and sponsor judges look for their tech there. Tags are freeform, so use the sponsor's exact product name.
- MLH submission portals also ask for the **prize categories you're entering**, a **GenAI usage disclosure**, and (for the Gemini prize) a **Gemini API project number** — flag these so the team captures them before the deadline rush.

## Step 4 — Offer follow-through

End by offering to scaffold step 1 of the top integration right now (install the SDK, write the client wrapper, stub the demo path). At a hackathon, the plan that's already 20% executed is the one that ships.

## Attribution

Adapted from sponsor-matchmaker by Asray Gopa, MIT licensed, for hackathon-ecc. Renamed to track-picker and extended with a main themed tracks section.
