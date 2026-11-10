---
name: hackathon-scope
description: >
  Hackathon MVP scoping strategy. Activates after grill-me — defining the absolute minimum viable demo, identifying scope traps (overly ambitious features), the demo-first development principle, time budgeting (build vs demo vs slack), choosing a winnable category, and shipping vertical slices rather than horizontal layers.
---

# Hackathon MVP Scoping

This skill runs after grill-me has recorded the project decisions.

## The hackathon trap
Most teams lose by being too ambitious. They start building the "real" version, run out of time, and present something broken. Winning teams scope a demo so small it's embarrassing — then polish.

## The single rule of hackathon scoping
**Build for the demo, not the product.**

The judges will see 2-5 minutes of your work. Optimize every hour of build time toward what makes those minutes great.

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

If you cannot write this storyboard in 30 minutes, you don't understand your project yet. Don't start building until you can.

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

## Pre-empt demo-killing failures
- **Wifi unreliable** → cache responses, have offline fallback
- **API down** → have a recording or screenshot backup
- **Live coding** → never. always have a recorded backup ready to swap
- **One person owns demo** → another person can drive if owner gets sick
- **Single dependency on hot-path service** → have a fallback path

## What "MVP" means at a hackathon
A minimum viable PRESENTATION, not a minimum viable PRODUCT.
- "Viable product" = something users could rely on (months of work)
- "Viable presentation" = something judges find compelling for 2-5 min (24-48h)

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
