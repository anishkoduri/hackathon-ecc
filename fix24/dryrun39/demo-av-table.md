# Dry-run #39 — /demo A/V table (Pantry Pal fixture)

Fixture app: `sample-app/` (Pantry Pal, served at http://localhost:5180,
verified 200 on `/` and `/plan.html`). Video project:
`demo-sample-video/` (fresh copy of the build #4 pitch-deck-video
template + the Dry-run #37/38 `shots.json`: 12 beats, edge at position 3,
6 features, 1 recorded cut, arch fallback, theme pulled from the app's own
tokens, `theme.vignette: 0`, `music.gain.under: 0.14`, bang block with
opener concept 5 + "Editorial light" + 3 kinetic-type rows + 2 camera-move
rows).

- Narration: `node scripts/tts.mjs` exit 0; no voice provider in this
  sandbox, so beat lengths are word-count estimates. Narration total with
  gaps **81.7s**; runtime total LEAD 0.7 + 81.7 + TAIL 1.7 = **84.1s**,
  under the 130s cap (absolute max 150s). No key used or written anywhere.
- Recording: `node scripts/record.mjs` exit 1 at `chromium.launch()` —
  Playwright browser binary missing
  (`~/.cache/ms-playwright/chromium_headless_shell-1243/...` does not
  exist). Environmental, same as dry-runs #37/#38; install not re-attempted.
- QA: `node scripts/qa.mjs` exit 1 — the known environmental caveat
  (runtime Google Fonts fetch from `fonts.gstatic.com` fails inside Chrome
  in this sandbox with `net::ERR_SSL_PROTOCOL_ERROR` on all three woff2
  files; the same URL returns 200 via curl). The `-p` invocation resolved
  and ran; Remotion printed "rendering 12 stills…" before failing.

Per-beat A/V table — completed as far as the app source allows:

| Beat | Say (narration) | Visual (filmed app) | Audio |
| --- | --- | --- | --- |
| problem | "Every Sunday, Maya opens her pantry…" | app home, pantry list | narration (estimated) |
| wow | "Pantry Pal looks at the same six ingredients…" | click "Plan my week" | narration (estimated) |
| edge | "Recipe apps hand you a shopping list…" | focus "Zero extra shopping" | narration (estimated) |
| pantry | "It starts with what is actually there…" | focus "Your pantry" | narration (estimated) |
| planweek | "One click. Six dinners, planned…" | waitFor "Your week, planned" | narration (estimated) |
| curry | "Monday is chicken curry…" | focus "Monday" | narration (estimated) |
| cost | "The number that matters: six dinners, zero dollars extra." | focus "6 dinners" | narration (estimated) |
| onepot | "And one pot to wash…" | focus "One pot to wash" | narration (estimated) |
| remix | "Wednesday is the remix…" | focus "Leftover remix" | narration (estimated) |
| plan2 | "Tuesday's chickpea rice takes twenty minutes…" | focus "Chickpea rice" | narration (estimated) |
| arch | "No model calls. No backend…" | arch card (How it works) | narration (estimated) |
| close | "Six dinners. Zero extra shopping. One pot to wash." | close card | narration (estimated) |

**Stills column: UNVERIFIED (no stills)** — `out/qa/` is empty; no footage,
no render, no video. The 10-second mix listen was not done (no bed, no
rendered video). Music fetch not attempted (`yt-dlp` not installed;
warn-and-continue by design).
