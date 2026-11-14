# /demo fixture — per-beat A/V table (dry-run #37)

Sample app: `fix22/dryrun37/sample-app/` (Pantry Pal, static HTML, served
at http://localhost:5180 — verified 200 on `/` and `/plan.html`).
Video project: `fix22/dryrun37/demo-sample-video/` (template copy +
dry-run `shots.json`, 12 beats, Edge at position 3).

**Status: the "stills support it" column is UNVERIFIED — no stills exist
yet.** `qa.mjs` renders stills from a Remotion composition, which needs a
recorded take (`capture/marks.json` + footage). The recording step
(`record.mjs`) could not run in this environment: no Playwright browser
binary is installed, and both `npx playwright install chromium` attempts
failed downloading Chrome 153.0.8010.12 from cdn.playwright.dev (attempt 1:
ENOSPC on the 512M /tmp tmpfs; attempt 2 with TMPDIR redirected: server
closed the connection at ~90%). A headless-shell-only install is in
progress at report time; if it lands, `record.mjs` will be re-run and this
table completed from the contact sheets. Until then, each row states the
claim, the expected frame (verified against the sample app's source), and
`UNVERIFIED (no stills)`.

## Beats

| Beat | Kind | Claim (`say`) | Expected frame (from app source) | Stills support it? |
|---|---|---|---|---|
| problem | card | "Every Sunday, Maya opens her pantry and sees dinner nowhere. Six ingredients. No plan. Another takeaway." | Hook card, tagline typography, theme colours (cream/green/orange) | UNVERIFIED (no stills) |
| wow | app | "Pantry Pal looks at the same six ingredients and sees the whole week. Watch what one click does." | Pantry page, cursor glides to "Plan my week", click, plan page loads | UNVERIFIED (no stills) |
| edge | app | "Recipe apps hand you a shopping list. Pantry Pal never does. Nothing to buy is the whole point." | Focus on "Zero extra shopping" line on the plan page | UNVERIFIED (no stills) |
| pantry | app | "It starts with what is actually there. Chicken, rice, chickpeas, tomatoes, onions, one jar of garam masala." | Focus on "Your pantry" list (6 items) | UNVERIFIED (no stills) |
| planweek | app | "One click. Six dinners, planned from what she already owns. Monday curry, Tuesday chickpea rice, Wednesday's remix." | Plan page after the click (cut re-anchors here) | UNVERIFIED (no stills) |
| curry | app | "Monday is chicken curry. Twenty-five minutes, one pan, the tomatoes and onions she already had." | Focus on Monday day card | UNVERIFIED (no stills) |
| cost | app | "The number that matters: six dinners, zero dollars extra. The pantry paid for the week already." | Focus on "6 dinners · $0 extra · 1 pot" figure | UNVERIFIED (no stills) |
| onepot | app | "And one pot to wash. Every dinner cooks in the same pan, so the week ends cleaner than it started." | Focus on "One pot to wash" line | UNVERIFIED (no stills) |
| remix | app | "Wednesday is the remix. Yesterday's rice meets today's curry, and leftovers stop being a chore." | Focus on "Leftover remix" day card | UNVERIFIED (no stills) |
| plan2 | app | "Tuesday's chickpea rice takes twenty minutes. The week never asks for more time than a weeknight has." | Focus on "Chickpea rice" day card, then pull back (`focus: null`) | UNVERIFIED (no stills) |
| arch | card | "No model calls. No backend. The whole app is static pages served locally — the plan is the product." | Arch card: Your pantry → Week planner (static HTML — no runtime code) → Your week | UNVERIFIED (no stills) |
| close | card | "Six dinners. Zero extra shopping. One pot to wash." | Close card, tagline left on screen | UNVERIFIED (no stills) |

## Kinetic-type rows (F5 — in the table as rows of their own)

| Row | Claim | Expected frame | Stills support it? |
|---|---|---|---|
| hook kinetic type | Split-text reveal: words stagger 40ms, 24px rise, 200ms, ease-out | Tagline words enter staggered, then settle fully still before the hold | UNVERIFIED (no stills) |
| edge kinetic type | Word slam on the beat: scale 1.15 → 1.0, 120ms, ease-out, then hold still | "Nothing to buy" lands on the beat and holds | UNVERIFIED (no stills) |
| close kinetic type | Letter stagger: 30ms stagger, 12px rise, close sentence only | Tagline letters enter one by one, then settle | UNVERIFIED (no stills) |

## Camera-move rows (F5 — in the table as rows of their own)

| Row | Claim | Expected frame | Stills support it? |
|---|---|---|---|
| planweek camera move | Push-through from pantry list into the planned week | Camera travels from the pantry page into the plan page (no fade cut) | UNVERIFIED (no stills) |
| cost camera move | Glide to the $0 figure, settle | Camera glides to "6 dinners · $0 extra · 1 pot" and settles | UNVERIFIED (no stills) |

## Anti-slide spot check (from the composition as specified)

- One continuous world: opener travels inside the app UI (opener concept 5,
  Journey inside the UI); beats change by camera moves, not fades — as
  specified in `shots.json` `bang` block. Not yet observable without footage.
- Persistent subject: the pantry/plan content persists across beats (same
  app, same week). Not yet observable without footage.
- Text levels: hook/edge/close cards carry one headline + at most one
  supporting line by construction; kinetic type is title/hero only.
- Smallest on-screen text in the motion-graphics layer: cards render at
  1920×1080 with headline-scale type; no sub-30px text is specified.
- Style direction "Editorial light" is theme-matched (warm cream/green
  editorial app) with a recorded reason in `shots.json`.

## Mix

- `music.gain.under` = 0.14 (≤ 0.20) — the 10-second mix listen is NOT
  DONE: no music bed exists (no yt-dlp fetch attempted in this fixture)
  and no video was rendered, so there is no middle-of-video audio to
  listen to. The listen is owed on a real render.
