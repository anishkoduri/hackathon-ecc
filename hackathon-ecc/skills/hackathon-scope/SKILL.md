---
name: hackathon-scope
description: >
  Hackathon MVP scoping strategy. Activates after grill-me — or after the user skips grilling — defining the absolute minimum viable demo, identifying scope traps (overly ambitious features), the demo-first development principle, time budgeting (build vs demo vs slack), choosing a winnable category, and shipping vertical slices rather than horizontal layers.
---

# Hackathon MVP Scoping

This skill runs after grill-me has recorded the project decisions — or after the user skips grilling. Read `docs/decision-record.md` first if it exists — it is the source of the must-have/cut lists, the demo storyboard, and the hours-left number below. If the record file does not exist (the user said "just build it" or skipped grilling), do not block: use the raw prompt plus any scope the user gave as the record instead, and write a stub `docs/decision-record.md` noting what is undecided — each undecided item as an accepted unknown with owner: the builder and resolution point: during the build. Never invent decisions, and never write blanks. Then WRITE the scoping output to `docs/scope.md` in the project (see "Write docs/scope.md" below) before handing off: the file is the durable record the build, expansion, and demo skills read. The project directory IS the project root — the folder opened in Cursor; no separate directory is created, and all `docs/…` paths are relative to it (create `docs/` under the project root before the first `docs/` write).

## The hackathon trap
Most teams lose by being too ambitious. They start building the "real" version, run out of time, and present something broken. Winning teams scope a demo so small it's embarrassing — then polish.

## The single rule of hackathon scoping
**Build for the demo, not the product.**

The judges will see 2–4 minutes of your work. Optimize every hour of build time toward what makes those minutes great. Which length governs what: the live demo storyboard is 2–4 min; the demo video is 1:30–1:50; the pitch storyboard is under 90 seconds.

## Day 1, hour 1: the demo storyboard
Before writing a line of code, write the demo:
```
The demo:
1. (0:00-0:30) Show the problem with a concrete example
2. (0:30-1:30) Live demo — user does X, system responds Y
3. (1:30-2:30) Show the "wow moment" — the surprising capability
4. (2:30-3:30) Show one extension or implication
5. (3:30-4:00) Wrap with what you'd build next

Required for this demo:
- Working: user can do X (CORE)
- Working: system responds Y (CORE)
- Looks good: a UI that doesn't embarrass us (POLISH)
- Optional: extension that hints at scope (NICE)
- NOT needed: everything else
```

If you cannot write this storyboard, you don't understand your project yet. Fallback — do not block on it: build a default storyboard from the decision record's demo description (the core demo and wow moment as recorded, timed into the 0:00–4:00 slots as best they fit), or, if the record has no demo description either, note the gap as an assumption in `docs/scope.md` and in the final report and proceed with the must-have list as the storyboard. Don't start building until you can write the storyboard or have recorded the fallback.

## Write docs/scope.md

WRITE the scoping output to `docs/scope.md` in the project before handing off. It must contain, filled in from `docs/decision-record.md` (or from the stub record written above when grill-me was skipped — never left as blanks or placeholders):

- The must-have list (the CORE demo flows) and the cut list (everything explicitly out of scope for this demo) — plus the wow test: does this make a judge stop and stare? Name the one moment that makes the project unforgettable; if there is no such moment, the must-have list is not done
- The project assessment — a concise assessment, one or two lines each: **strengths** (what this project has going for it), **weaknesses** (where it is thin or risky), **opportunities** (what could make it stand out), **constraints** (time, skills, APIs, rules that bound it), and **recommended direction** (the one-sentence call on where to aim the build). For a first build the record/scope IS the research — this assessment is written from the decision record and the scoping above, not a new research phase; if the record is thin, say so in one line and proceed
- Unknowns / assumptions — the unknowns and assumptions carried from the decision record (each with owner and resolution point). Unknowns from the record flow into `docs/scope.md` here; they are not blockers, and they are resolved during the build by the safe/reversible default per hackathon-mode §7's assumption rule
- The filled demo storyboard above, with the 0:00–4:00 timings (a 2–4 min live demo)
- The hours-left number, copied from the decision record, plus the time budget split (build vs demo vs slack, rule of thirds below)
- The design direction, copied from the decision record's `Design direction:` line (theme/axes/mood, named) — if the record has no such line, record the stated default as an assumption in `docs/scope.md` (derived from the brief's mood/domain, marked assumed, not user-stated), never leave it blank; orchestrate's slice briefs and `docs/design-tokens.md` build on this line
- The chosen winnable category

If the decision record has no hours-left number, do not block and do not leave the number blank to proceed: use the recorded assumption — the remaining time until the demo deadline if known, else 8 hours — write it into `docs/scope.md` marked as an assumption, and proceed.

Then NAME the next step in the file and in your reply: `feature-expansion` runs next (automatically, during the first build, right after this scoping step), and after expansion the build runs via `orchestrate` (the first-build engine — one engine per run; `orch-build-mvp` is standalone-only and never runs in a first build orchestrate is driving). Do not end scoping without the file written and the next step named.

## Vertical slices, not horizontal layers
**Wrong (horizontal):**
- Day 1: build full data model
- Day 1.5: build full API
- Day 2: build full frontend
- Day 2.5: integrate
- Result: nothing works end-to-end until the very end

**Right (vertical):**
- Hour 1-2: hacky end-to-end of the single most important demo flow
- Then: improve each layer, but always keep end-to-end working

The hacky version is uglier but de-risks the demo from hour 2.

## Scope traps to recognize
These traps apply ONLY to unrequested infra — generic auth, database, or deploy work nobody asked for and the demo does not need. They do NOT apply to infra the user required: if the brief or `docs/decision-record.md` names auth, a database, or a deployment target, that infra is required, is preserved, and is built properly — off-the-shelf, per "Off-the-shelf maximalism" below (Auth0 / Clerk for auth, Vercel / Railway for deploy), never hardcoded away and never cut as a "trap". The rule is: unrequested infra gets the antidote in this table; user-required infra gets the real, off-the-shelf implementation.
| Trap | Symptom | Antidote |
|------|---------|----------|
| **"Real" auth** | "We need login first" | Hardcode a demo user |
| **Real database** | "Let's set up Postgres" | In-memory dict, JSON file |
| **Real deploy** | "Let's set up CI/CD" | Demo from laptop, ngrok if needed |
| **Edge case obsession** | "What if the user enters X" | Demo doesn't enter X |
| **Generality** | "Make it work for any input" | Hardcode the demo input |
| **Architecture astronautism** | "Let's use microservices" | One file. Maybe two. |
| **Real ML training** | "Train a custom model" | Use an off-the-shelf API |
| **Real scale** | "Make it handle 1000 users" | One user is fine for judging |
| **Generic UI** | Polished design system | The 3 screens for the demo, that's it |

## Time budget (rule of thirds)
- **First third**: build core flow end-to-end (hacky)
- **Middle third**: make the demo flow work reliably + look good
- **Last third**: rehearse, fix demo blockers, polish, slack
  - NEVER skip rehearsal time
  - NEVER assume "5 more hours = 5 more features" — risk grows non-linearly

For a 24-hour hackathon: 8h build core, 8h polish demo, 8h rehearse + buffer.

For a 48-hour: 16h / 16h / 16h.

## Choose a winnable category
Pick the category where:
- The judging rubric matches what you can deliver (technical innovation? user experience? business impact?)
- The competition is weakest (smaller categories = better odds)
- Your team's strengths apply (ML team in ML track; design team in UX track)

A safe silver in a small category beats trying for gold in the megacategory.

## Off-the-shelf maximalism
Hackathons reward outcomes, not from-scratch implementations:
- LLM API > training your own
- Auth0 / Clerk > rolling your own auth
- Vercel / Railway > setting up servers
- Tailwind + shadcn > custom CSS
- Use templates, starter kits, last weekend's project as a base (read the rules!)

The judges don't care that you used GPT-4. They care that the demo works.

This is also how user-required infra gets built: when the brief or the decision record names auth, a database, or deploy, use the off-the-shelf option above (Auth0 / Clerk, Vercel / Railway) and build it properly — that is the opposite of the scope-trap antidotes, which are only for infra nobody requested.

## Pre-empt demo-killing failures
- **Wifi unreliable** → cache responses, have offline fallback
- **API down** → have a recording or screenshot backup
- **Live coding** → never. always have a recorded backup ready to swap
- **One person owns demo** → another person can drive if owner gets sick
- **Single dependency on hot-path service** → have a fallback path

## What "MVP" means at a hackathon
A minimum viable PRESENTATION, not a minimum viable PRODUCT.
- "Viable product" = something users could rely on (months of work)
- "Viable presentation" = something judges find compelling for 2–4 min (24-48h)

Optimize for the latter ruthlessly.

## Common pitfalls
- Picking too ambitious a project → broken demo, no win
- Building features you won't demo
- "We'll polish at the end" → no time left at the end
- No demo rehearsal → live demo blows up
- One person solos the demo → bus factor 1
- No backup video → live failure is the whole impression
- Building generic infra (auth, deploy) when the demo doesn't need it
- Skipping sleep → terrible decisions and bugs in the last hours

---

Original by RR-AMATOK (hackathon-mvp-scoping), used verbatim in hackathon-ecc as hackathon-scope.
