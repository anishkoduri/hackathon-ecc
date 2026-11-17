# Dry-run #46, Leg 3 — /demo A/V table (from the QA stills)

`qa.mjs` exit 0 twice, "No BLOCKING findings from the automated checks" in both runs.
12/12 stills rendered (`out/qa/`). Viewed directly this session: `00111_problem.png`
and `00973_planweek.png`; the other 10 beats' claims are as recorded by `qa.mjs`
(claim-vs-screen is one of its automated checks) and match the #37–#45 fixture.

| Beat | Claim in narration | On screen |
|---|---|---|
| problem | Maya opens her pantry, sees dinner nowhere; six ingredients, no plan | Caption bar matches; card is the app's plain cream ground (no spinner/empty state) |
| wow | Pantry Pal sees the whole week from the same six ingredients | App beat filmed (mark present) |
| edge | Recipe apps hand you a shopping list; Pantry Pal never does | App beat filmed (mark present) |
| pantry | Six ingredients: chicken, rice, chickpeas, tomatoes, onions, garam masala | Pantry list shows the six ingredients |
| planweek | One click: six dinners; Monday curry, Tuesday chickpea rice, Wednesday remix | Week plan shows "6 dinners · $0 extra · 1 pot"; Monday chicken curry 25 min; Tuesday chickpea rice 20 min; Wednesday leftover remix (viewed) |
| curry | Monday chicken curry, 25 minutes, one pan | Monday curry 25 minutes |
| cost | Six dinners, zero dollars extra | "6 dinners · $0 extra" |
| onepot | One pot to wash; every dinner in the same pan | One-pot claim on screen |
| remix | Wednesday remix: yesterday's rice, today's curry | Leftover remix card |
| plan2 | Tuesday chickpea rice, 20 minutes | Tuesday chickpea rice 20 minutes |
| arch | No model calls, no backend; static HTML, no runtime code | Arch diagram shows "static HTML — no runtime code" |
| close | Six dinners, zero extra shopping, one pot | Close card shows the serif "Pantry Pal" in self-hosted Instrument Serif |

**Not done (same as #37–#45):** no full render (`demo.mp4`), no 10-second mix listen
(no voice provider, no music bed — `musicBed: false`, narration estimated at 81.7s).
Record warnings (minor, not BLOCKING): `wow.click` and `planweek.click` sub-actions
skipped ("Execution context was destroyed, most likely because of a navigation");
footage for both beats exists, only the mid-shot clicks did not execute.
