# Fix #26 §7 — Fix #17 R1/R4 verification against the Home Run render: OWED

## Verdict

R1 (iris-opens) and R4 (hero loop) are OWED, not verified. The Home Run
render files do NOT substantiate both moments as defined. Do not record
them as verified.

Scope of this check: the Home Run live render
(`~/workspace/cold-start-render/home-run/`), NOT Campus Eats. No live
Campus Eats render exists in this workspace (see fix26/dim7-note.md),
so nothing here verifies anything about Campus Eats.

## What R1/R4 are (fix #17)

- R1 iris-opens + R4 hero loop: dealt design elements with no recorded
  application in the Campus Eats record (fix17/MANIFEST.md:81,
  fix17/PARENT-GUIDANCE.md:18, :47). Fix #17 states verification against
  the live Campus Eats artifact requires the live artifact — which is
  not in this workspace.
- The benchmark's beat-v5 applications of them (dry-run #40 re-trace,
  `fix25/dryrun40/dryrun40-benchmark.md` rows 67–68) are:
  - #67: iris-opens APPLIED as the section transition (hero → picks).
  - #68: R4 hero loop APPLIED inside the app-frame window (spot rows
    cycle; steam wisp over the ramen photo in the window).
- Both #67/#68 are paper re-trace additions under current rules, not
  measurements of a live render. The re-trace is a Campus Eats
  re-derivation; it is not Home Run evidence.

## What the Home Run render actually contains

### R1 iris-opens: APPLIED in Home Run — but NOT as the benchmark's hero → picks transition

The iris-opens moment IS implemented and live-rendered in Home Run, as
the trip-screen delivery-code panel reveal:

- `cold-start-render/home-run/index.html:179–180` — `<div class="iris-wrap"
  id="iris-wrap">` + `<div class="iris-disc">` inside the trip view.
- `cold-start-render/home-run/styles.css:425–446` — `.iris-disc` (hairline
  green ring), `@keyframes iris-ring` (scale 0.2 → 1.6, 0.7s), `.iris-open
  .code-panel` with `@keyframes iris-open` (`clip-path: circle(0% …)` →
  `circle(150% …)`, 0.6s).
- `cold-start-render/home-run/app.js:190–192` — `enterTrip()` adds the
  `iris-open` class 120ms after entering the trip view (once per trip,
  skipped under reduced motion); `app.js:384,392–393` resets it.
- `cold-start-render/home-run/docs/design-tokens.md:199–202,245,342` —
  records the moment: "the code panel opens through the iris disc
  (hairline green ring)"; "iris-opens: the disc opens 0.6s ease-in-out".
- Live-measurement corroboration: dry-run #40 Leg 2 assertion (e) CLIP
  records `.iris-disc` beyond the phone frame in 8 measurements
  (trip + trip-wrongcode × 4 widths), bleed declared — the disc element
  exists and renders in the live run.

Gap for R1 as defined: this is a trip-view code-panel reveal, not the
hero → picks section transition (#67). No hero → picks transition exists
in Home Run — Home Run has no "picks" section and no ramen photo. The
#67 application exists only in the Campus Eats paper re-trace, not in
any live render in this workspace.

### R4 hero loop: NOT applied anywhere in the Home Run render

- Grep for `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval`
  across `index.html`, `styles.css`, `app.js`: zero hits. No interval,
  no cycling rows, no steam wisp, no looping hero element of any kind.
- Grep for `loop` in `docs/design-tokens.md`: zero hits.
- The only repeating animation machinery is one-shot: the counter-roll
  (`app.js:182–184`, `requestAnimationFrame`, 0.6s, rolls once on entry
  then rests) and the wrong-code shake (`app.js:233` area, 0.65s reset).
  Neither loops.
- The Home Run hero (home/feed view, `index.html:50–76`) is a static
  statement + subline + one live-run card + sort keys + feed list.
  Nothing in or around it cycles.

Gap for R4 as defined: the #68 hero loop (spot rows cycling; steam wisp
over the ramen photo inside the app-frame window) exists only in the
Campus Eats paper re-trace. No live render in this workspace implements
it.

## Why the SPEC §7 premise does not close this

SPEC §7 cites dry-run #40's re-trace ("hero loop + iris-opens applied")
alongside "17/17 §6 assertions passing on the Home Run render" as if
one record. They are two different records:

- The "hero loop + iris-opens applied" phrase is the Campus Eats
  benchmark re-trace (`dryrun40-benchmark.md` rows 67–68, summarised in
  `dryrun40-report.md` §2.3 and fix25/MANIFEST.md §4(d) Leg 2 row) —
  paper additions under current rules, scored statically.
- The 17/17 §6 assertions (`dryrun40-report.md` §2.1) are Home Run
  ALIGNMENT assertions (a)–(h) + coverage: overflow, centering, nav,
  grid, clip, labels, actions, panels. They pass with 0 flags and say
  nothing about moment/loop application — except assertion (e), which
  corroborates the iris-disc's existence (see above).

Conflating the two would claim a live verification the record does not
support. The benchmark file itself states the limit (§1 "Caveat on
provenance"): "absence from it proves nothing about the live page —
including the iris-opens / hero loop non-application above."

## Disposition

- R1: OWED as defined (hero → picks section transition). Partial
  adjacent evidence recorded above: the iris-opens moment is applied
  and live-rendered in Home Run in a different placement (trip
  code-panel reveal). That does not verify #67.
- R4: OWED as defined (hero loop in the app-frame window). No adjacent
  evidence: no looping hero element exists in any live render in this
  workspace.
- What would close them: a live Campus Eats render implementing #67 and
  #68, measured by browser-qa. None will be built for this purpose
  (Anish's Nov 11 call, see fix26/dim7-note.md). They stay owed.

## No code change

Recording only. No render file was modified; no benchmark figure was
edited.
