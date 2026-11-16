# Dry-run #43, Leg 3 — /demo A/V table (from viewed stills)

Fixture: `demo-sample-video/` (fresh copy of the rebuilt template +
dry-run #37–#42 `shots.json`, 12 beats) + `sample-app/` (Pantry Pal,
served at `http://localhost:5180`). Stills viewed this session:
`out/qa/sheet_01.png` + `out/qa/sheet_02.png` (all 12 stills) —
`qa.mjs` reports "No BLOCKING findings".

| Beat | Claim in narration | On screen |
|---|---|---|
| problem | Maya opens her pantry, sees dinner nowhere; six ingredients | Caption "Maya opens her pantry and sees dinner nowhere. Six ingredients." over the pantry view |
| wow | Pantry Pal sees the whole week in the same six ingredients | Week plan "6 dinners · $0 extra · 1 pot"; caption "ingredients and sees the whole week." |
| edge | Pantry Pal never does (takeaway) | Caption "Pantry Pal never does." |
| pantry | Starts with what is actually there: chicken, rice, chickpeas, tomatoes | Pantry list: chicken thighs 1.2 kg, basmati rice 800 g, chickpeas 2 cans, tomatoes 5, onions 4, garam masala 1 jar — six items |
| planweek | Planned from what she already owns; 6 dinners, $0 extra, 1 pot | "6 dinners · $0 extra · 1 pot"; Mon curry / Tue chickpea rice / Wed leftover remix |
| curry | Monday is chicken curry, 25 minutes, one pan | "Monday — Chicken curry … 25 minutes."; caption "Monday is chicken curry. Twenty-five minutes, one pan," |
| cost | Zero dollars extra | "6 dinners · $0 extra · 1 pot"; caption "zero dollars extra." |
| onepot | Every dinner cooks in the same pan | Caption "Every dinner cooks in the same pan," |
| remix | Yesterday's rice meets today's curry | "Wednesday — Leftover remix … 10 minutes."; caption "Yesterday's rice meets today's curry," |
| plan2 | The week never asks for more time than a weeknight has | Week plan again; caption "The week never asks for more time than a weeknight has." |
| arch | The whole app is static HTML, no runtime code | "How it works" diagram: Your pantry → Week planner → Your week; caption "The whole app is static HTML — no runtime code" |
| close | Pantry Pal — six dinners, zero extra shopping, one pot to wash | Serif "Pantry Pal" close card: "Six dinners. Zero extra shopping. One pot to wash." in self-hosted Instrument Serif |

**All 12 beats' claims match what is on screen.**

Not executed: the 10-second mix listen — the fixture has no music bed
(`musicBed: false`) and no narration (no voice provider), so there is no
mix to listen to. Runtime **84.1s** from `src/vo-durations.json` (LEAD 0.7
+ sum(dur+gap) + TAIL 1.7), under the 130s hard / 150s absolute caps — but
the durations are word-count estimates (~150 wpm, "available providers:
none"), not measured narration; the "measured" part is owed to a real
narrated run, same caveat as dry-runs #37–#42.
