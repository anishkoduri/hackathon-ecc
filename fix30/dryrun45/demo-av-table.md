# Dry-run #45, Leg 3 — /demo A/V table (completed from the viewed stills)

Fixture: `fix30/dryrun45/demo-sample-video/` (fresh copy of the rebuilt
template, byte-identical except the fixture `shots.json`) + Pantry Pal sample
app served at `http://localhost:5180`. `qa.mjs` exit 0 twice; 12/12 stills
rendered + 2 ffmpeg contact sheets; 0 Google Fonts requests in any log.
Runtime **84.1s** from `src/vo-durations.json` (12 beats, LEAD 0.7 +
sum(dur+gap) + TAIL 1.7) — under the 130s hard / 150s absolute caps.

The 10-second mix listen was NOT done: the fixture has no music bed
(`musicBed: false`) and no narration (no voice provider), so there is no mix
to listen to. Narration durations are word-count estimates (~150 wpm), not
measured narration — the same caveat as dry-runs #37–#44.

| Beat | Claim (say-line) | Still shows | Match |
|---|---|---|---|
| problem | "Maya opens her pantry and sees dinner nowhere. Six ingredients." | Caption card with that line; app frame mostly empty cream | YES |
| wow | "Pantry Pal looks at the same six ingredients and sees the whole week." | Week plan: "6 dinners · $0 extra · 1 pot"; Monday curry 25 min, Tuesday chickpea rice 20 min, Wednesday leftover remix | YES |
| edge | "Recipe apps hand you a shopping list. Pantry Pal never does." | Same plan view; caption "Pantry Pal never does." | YES |
| pantry | "It starts with what is actually there. Chicken, rice, chickpeas, tomatoes, onions, one jar of garam masala." | Pantry list shows the six ingredients with quantities (chicken thighs 1.2 kg, basmati 800 g, chickpeas 2 cans, tomatoes 5, onions 4, garam masala 1 jar) | YES |
| planweek | "One click. Six dinners, planned from what she already owns. Monday curry…" | Week plan view; caption "planned from what she already owns. Monday curry," | YES |
| curry | "Monday is chicken curry. Twenty-five minutes, one pan…" | Monday — Chicken curry, "25 minutes"; caption "Monday is chicken curry. Twenty-five minutes, one pan," | YES |
| cost | "six dinners, zero dollars extra" | "6 dinners · $0 extra · 1 pot" on screen; caption "zero dollars extra." | YES |
| onepot | "Every dinner cooks in the same pan" | Caption "Every dinner cooks in the same pan,"; header "One pot to wash" | YES |
| remix | "Wednesday is the remix. Yesterday's rice meets today's curry" | Wednesday — Leftover remix, "Yesterday's rice, today's curry. 10 minutes."; caption "Yesterday's rice meets today's curry," | YES |
| plan2 | "Tuesday's chickpea rice takes twenty minutes. The week never asks for more time than a weeknight has." | Tuesday — Chickpea rice, "20 minutes"; caption "The week never asks for more time than a weeknight has." | YES |
| arch | "No model calls. No backend. The whole app is static pages served locally" | "How it works" diagram: Your pantry → Week planner (static HTML — no runtime code) → Your week; caption "The whole app is static pages served locally —" | YES |
| close | "Six dinners. Zero extra shopping. One pot to wash." | Serif "Pantry Pal" in the self-hosted Instrument Serif face; tagline "Six dinners. Zero extra shopping. One pot to wash." | YES |

**12/12 beats' claims match what is on screen.** Record warnings (minor,
not BLOCKING): `capture/marks.json` carries 2 warnings and `capture/failures/`
holds 2 PNGs — the `wow.click` and `planweek.click` sub-actions were skipped
("Execution context was destroyed, most likely because of a navigation").
The footage for both beats exists (marks present, stills render); only the
mid-shot click actions did not execute — a navigation race in `record.mjs`,
not a missing beat. Same warnings as #41/#42/#43/#44.
