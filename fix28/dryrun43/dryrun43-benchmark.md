# Dry-run #43, Leg 2 — Campus Eats v5 benchmark re-trace (fix #28)

Re-trace of the dry-run #42 §2.2 benchmark against the fix #28 run-6 built
tree. The re-trace additions (#67–#73) are paper re-trace additions scored
statically, NOT measurements of a live render.

## §1 Fresh verification of the v5 figures

- Benchmark file re-read this session:
  `hackathon-ecc/skills/orchestrate/references/design-benchmark-v5.md`
  (178 lines, frozen at v5). Kind sums re-added — literal
  31+8+1+17+1+2+0+1 = **61**, stricter **60**; matches the file's table
  (v4 54 + v5 delta 7 = 61).
- Dynamic inventory re-read: **8 items**, 1 drive, 2 surfaces, as recorded.
- Dynamic-count boundary re-derived from `fix17/INVENTORY-V4.md` (#47–#50,
  #54 hover micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item
  for item, defensible range **6–13** (narrow/broad) unchanged.
- Rule traces for the 7 re-trace additions re-checked in the rebuilt tree:
  R1 (`design-taste-frontend/SKILL.md:409` — same line as #42; text
  unchanged), R4 (`fix15/SPEC.md:91`), CREATIVE_F25
  (`feature-expansion/SKILL.md:59,93,99` — one line later than #42's
  58/92/98; anchor texts identical, trace holds), E1, M3
  (`make-interfaces-feel-better/SKILL.md:127` — two lines later than #42's
  :125; anchor text identical, trace holds). All hold. (Fix #28 touches
  none of these files; the +1/+2 line drift vs #42 is build-time patch
  application drift, not a fix #28 edit.)
- **Re-trace: 68 literal / 66 stricter** (v5 61/60 + the same 7 rule-traced
  additions #67–#73). Kinds 7 → 8, five kinds above v5.

## §2 Per-dimension table

| # | Dimension | v5 | Re-trace | Result |
|---|---|---|---|---|
| 1 | Element count | 61 / 60 | **68 / 66** | **PASS** (≥ 62 / ≥ 61) |
| 2 | Variety | 7 kinds, Effect 0 | **8 kinds, 5 above v5**, no drops | **PASS** |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop | Full inventory **+ hero loop AND second moment applied** | **PASS (static)**; strength verdict OWED to browser-qa |
| 4 | Motion | 17 / 16 | **19 / 17** | **PASS** (≥ 18 / ≥ 17) |
| 5 | Dynamic interface | 8 items; 1 drive | **10 items; 2 drives** | **PASS (static)**; live behaviour OWED. Sensitivity: fails only under the narrow (6) reading |
| 6 | Functionality | 2 live-data surfaces | **3 surfaces**; mechanism on hero/first screen | **PASS (static)**; live verdict OWED (FUNC-BQA_F23) |
| 7 | Alignment | NONE RECORDED | **— cannot be scored** | **OWED, never passed** |

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7 is OWED.**
`~/workspace/cold-start-render/campus-eats/` contains only
`docs/design-tokens.md` (verified by listing this session) — no `index.html`,
no CSS, no JS, no assets, so browser-qa cannot run the ALIGN_F23 matrix on
it. Disposition per fix28/SPEC.md §7 (same as fix27/SPEC.md §8): RECORDED
DECISION (owed, with the reason), not a pass. No Campus Eats render was
built. The Home Run 52-measurement / 0-problem run is live alignment
evidence about Home Run, not Campus Eats, and is not counted toward
dimension 7.

## §3 R1/R4 scope note (fix26/r1r4-note.md, verified this session)

The #67/#68 applications are paper re-trace additions, scored statically —
NOT measurements of a live render. The Home Run render implements iris-opens
in a different placement (trip code-panel reveal, `index.html:179–180`,
`styles.css:433–446`, `app.js:192`) and implements no hero loop at all
(zero `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval` hits
across its `index.html`/`styles.css`/`app.js`; zero `loop` hits in its
decision record). Fix #17 R1/R4 stay OWED as defined. The 6/7 re-trace
result is unaffected: it never claimed a live verification of #67/#68.
