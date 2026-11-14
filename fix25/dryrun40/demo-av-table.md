# Dry-run #40, Leg 3 — per-beat A/V table (completed from the stills)

Source: `demo-sample-video/out/qa/` — 12 stills + 2 contact sheets, rendered
by `qa.mjs` (exit 0, twice). Both sheets were viewed this session. No
spinners, skeletons, or empty states in any still; every still shows the
app in its own palette (cream #f6f1e7, green #2e5d3a, orange #e07b39 —
not the seed theme); captions are legible throughout. The arch/close
beats are cards by design (F1); all feature beats are filmed app footage.

| Beat | Kind | Claim (narration) | Still shows | Supports it? |
|---|---|---|---|---|
| problem | card | "Maya opens her pantry and sees dinner nowhere. Six ingredients." | Cream intro frame, caption "Maya opens her pantry and sees dinner nowhere. Six ingredients." (the six-item list itself is visible in the pantry still) | YES |
| wow | app | "Pantry Pal looks at the same six ingredients and sees the whole week." | Week plan: "6 dinners · $0 extra · 1 pot" + Mon–Wed dinners | YES |
| edge | app | "Recipe apps hand you a shopping list. Pantry Pal never does." | Week plan — dinners, no shopping list anywhere on screen | YES |
| pantry | app | "It starts with what is actually there. Chicken, rice, chickpeas, tomatoes." | "Your pantry — 6 items": chicken thighs, basmati rice, chickpeas, tomatoes, onions, garam masala | YES |
| planweek | app | "One click. Six dinners, planned from what she already owns." | "6 dinners · $0 extra · 1 pot" + Mon/Tue/Wed dinners | YES |
| curry | app | "Monday is chicken curry. Twenty-five minutes, one pan." | "Monday — Chicken curry … 25 minutes" | YES |
| cost | app | "The number that matters: six dinners, zero dollars extra." | "6 dinners · $0 extra · 1 pot" | YES |
| onepot | app | "And one pot to wash. Every dinner cooks in the same pan." | "1 pot" in the plan header | YES |
| remix | app | "Wednesday is the remix. Yesterday's rice meets today's curry." | "Wednesday — Leftover remix / Yesterday's rice, today's curry. 10 minutes." | YES |
| plan2 | app | "Tuesday's chickpea rice takes twenty minutes." | "Tuesday — Chickpea rice … 20 minutes" | YES |
| arch | card | "No model calls. No backend. The whole app is static pages served locally." | "How it works" INPUT/CODE/OUTPUT diagram; "static HTML — no runtime code"; Instrument Serif display type (self-hosted font painting) | YES |
| close | card | "Six dinners. Zero extra shopping. One pot to wash." | "Pantry Pal / Six dinners. Zero extra shopping. One pot to wash." (serif display type) | YES |

**Not executed (recorded, not passed): the 10-second mix listen.** The
fixture has no music bed (`musicBed: false`) and no narration (no voice
provider in the sandbox — `tts.mjs` wrote word-count estimates), so there
is no mix to listen to. Same caveat as dry-runs #37–#39; a real narrated
run with a bed is owed to the live smoke test.

**Record warnings (minor, not BLOCKING):** `capture/marks.json` carries
2 warnings and `capture/failures/` holds 2 PNGs — the `wow.click` and
`planweek.click` sub-actions were skipped ("Execution context was
destroyed, most likely because of a navigation"). The footage for both
beats exists (marks present, stills render); only the mid-shot click
actions did not execute — a navigation race in `record.mjs`, not a
missing beat. `qa.mjs` itself reports "No BLOCKING findings".
