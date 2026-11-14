# Fix #26 §6 — Benchmark dimension 7 (alignment) disposition: RECORDED DECISION, owed

## Verdict

Dim 7 stays OWED. This is a recorded decision, NOT a pass. The v5 figures
stay render-history figures, not live-measured ones. NO Campus Eats render
will be built to verify it (Anish's Nov 11 call: "It's ok render doesn't
matter anymore").

## Verification (1): no live Campus Eats render exists

`~/workspace/cold-start-render/` listing, checked this session:

- `campus-eats/` contains only:
  - `.hallmark/salt`, `.hallmark/log.json`
  - `.taste-skill/layout-history.json`, `.taste-skill/history.json`
  - `docs/design-tokens.md` (the v1-era tokens file)
- No `index.html`, no CSS, no JS, no assets, no app-frame window. There
  is nothing browser-qa could run the ALIGN_F23 matrix against.
- `home-run/` is a different app (intercity pickup marketplace) and is
  not a Campus Eats render; its alignment evidence does not count toward
  Dim 7.

## Verification (2): the owed record

- `new-skills/orchestrate/references/design-benchmark-v5.md` §2 Dim 7:
  v5 figure "NONE RECORDED (no v5 figure)"; the bar is "0 problems
  across the full ALIGN_F23 coverage matrix" executed by browser-qa, with
  the verdict "browser-qa live verdict (owed, never claimed statically)".
  §3: "If a dimension cannot be scored — statically or live — the leg
  says which, and records it as a gap (owed), not as a pass."
- `new-skills/orchestrate/references/design-benchmark-v5.md` §1, including
  its "Caveat on provenance" subsection (cited as "§1 + §8" in
  fix25/MANIFEST.md §6; the file itself numbers only §1–§3, and the
  caveat sits inside §1): the v5 figures are render-history figures; a
  live re-measure against the real artifact would supersede them.
- `fix25/dryrun40/dryrun40-report.md` §2.3, Leg 2: "Benchmark result: 6
  of 7 dimensions pass statically; dimension 7 is OWED. No live Campus
  Eats render exists in this workspace (only the v1-era tokens file), so
  browser-qa cannot run the ALIGN_F23 matrix on it in this sandbox. A leg
  that cannot score a dimension does not PASS on that dimension." The
  Home Run 52-measurement / 0-problem run is live alignment evidence
  about Home Run, not Campus Eats, and is not counted toward Dim 7.
- `fix25/MANIFEST.md` §6: "Benchmark dimension 7 (alignment) is OWED,
  never passed."

## What this closes

The open item is closed as a RECORDED DECISION (owed, with the reason),
per fix26/SPEC.md §6. It is not a pass, not a waiver of the ALIGN_F23
bar for future builds, and not a claim that Campus Eats v5 was aligned.
Any future live Campus Eats render + browser-qa run would supersede this
note; none is planned and none will be built for this purpose.

## No code change

Recording only. No render was built. No benchmark figure was edited
(`design-benchmark-v5.md` is frozen at v5).
