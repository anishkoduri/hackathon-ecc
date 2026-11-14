# Dry-run #41, Leg 2 — Campus Eats v5 benchmark re-trace (fix #26 §6)

Method: the dry-runs #25–#28 paper re-trace, re-derived fresh this session
against the rebuilt tree (build.sh 24,088 lines, md5
e05bdc66599b694398e11f0d00dfdafd). Same Campus Eats brief, same current
rules, same fix #15 BASELINE.md literal rule. No Campus Eats render was
built (Anish Nov 11: "It's ok render doesn't matter anymore"; fix26/SPEC.md
§6). This is a paper enumeration through the skills, not a count of a
rebuilt artifact and not an assertion.

## §1 Fresh verification of the v5 figures (not taken on trust)

- Benchmark file re-read this session:
  `hackathon-ecc/skills/orchestrate/references/design-benchmark-v5.md`
  (178 lines, frozen at v5). Kind sums re-added: literal
  31+8+1+17+1+2+0+1 = **61**; stricter 31+8+1+16+1+2+0+1 = **60**. Both
  agree with the file's table. v4 54 + v5 delta 7 = 61.
- Dynamic inventory re-read (§1 of the benchmark file): **8 items**,
  listed 1–8 (stepper + live total; Roll a craving; Tried-it stamps;
  sticker sheet; search bar; marquee pause; sticker-peel; coin stack).
  Cross-surface drives **1** (stepper → total + coin stack + $10 row).
  Live-data surfaces **2** (spot list; stepper total).
- Dynamic-count boundary re-derived from `fix17/INVENTORY-V4.md`:
  #47 photo tilt, #48 name warms, #49 tap-to-pop, #50 wiggle, #54
  compass grows (all hover micros, excluded by E) and #58 marquee pause
  (included by E) all exist as recorded; #60 sticker-peel is the v5
  delta item in the benchmark file. E's boundary (state-changing
  features in, pure hover micros and ambient loops out) is a judgment
  call with no stated distinction separating #58/#60 from #47–#50/#54.
  Consistent alternatives from the same record: narrow **6** (drop
  #58, #60), broad **13** (add #47–#50, #54). Range 6–13 stands.
- R1/R4 non-application re-verified in `fix17/dryrun28-report.md` §C:
  iris-opens DEALT with no recorded application anywhere; grep for
  "loop" across the artifact directory zero hits; the tokens file omits
  all 36 v2–v5 elements, so absence proves nothing about the live page.
  This is a finding about what is RECORDED.
- Rule traces for the 7 re-trace additions re-checked in the rebuilt
  tree this session:
  - #67 iris-opens applied (hero → picks): R1 — "every dealt moment is
    applied or re-dealt" (`design-taste-frontend/SKILL.md:407`).
  - #68 hero loop applied: R4 — "the dealt hero's loop is implemented
    or waived" (`fix15/SPEC.md:91`).
  - #69/#70 filter + preset chips, #71 live count: CREATIVE_F25 —
    substance-first / no-UI-only slate
    (`feature-expansion/SKILL.md:58,92,98`).
  - #72 frosted-glass Effect: E1 push (Effect 0 at every version v1–v5;
    `design-taste-frontend` E1 references present).
  - #73 filter-chip hover micro: M3 — "hover micro-interactions on
    every interactive element"
    (`make-interfaces-feel-better/SKILL.md:125`).

## §2 Re-traced totals (unchanged from dry-run #40)

| Kind | v5 literal | v5 stricter | Re-trace literal | Re-trace stricter |
|---|---|---|---|---|
| Component | 31 | 31 | **33** (+#69, #70) | **33** |
| Treatment | 8 | 8 | **8** | **8** |
| Visual | 1 | 1 | **1** | **1** |
| Motion | 17 | 16 | **19** (+#68, #73) | **17** (+#73 only) |
| Moment | 1 | 1 | **2** (+#67) | **2** |
| Type | 2 | 2 | **3** (+#71) | **3** |
| Effect | 0 | 0 | **1** (+#72) | **1** |
| Diagram | 1 | 1 | **1** | **1** |
| **Total** | **61** | **60** | **68** | **66** |

Kinds 7 → **8** (Effect joins). Five kinds above v5 (Component,
Motion, Moment, Type, Effect). No nonzero v5 kind drops. Dynamic
items 8 → **10** (+#69 chips, +#70 presets); drives 1 → **2**
(stepper drive + filter drive); live-data surfaces 2 → **3**
(+#71 live "N open now" count).

## §3 Per-dimension scoring

| # | Dimension | v5 figure | Re-traced figure | Result |
|---|---|---|---|---|
| 1 | Element count | 61 / 60 | **68 / 66** | **PASS** (≥ 62 / ≥ 61) |
| 2 | Variety | 7 kinds, Effect 0 | **8 kinds, 5 above v5**, no drops | **PASS** |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop | Full inventory **+ hero loop AND second moment applied** | **PASS (static)**; strength verdict OWED to browser-qa |
| 4 | Motion | 17 / 16 | **19 / 17** | **PASS** (≥ 18 / ≥ 17) |
| 5 | Dynamic interface | 8 items; 1 drive | **10 items; 2 drives** | **PASS (static)**; live behaviour OWED. Sensitivity: fails only under the narrow (6) reading |
| 6 | Functionality | 2 live-data surfaces | **3 surfaces**; mechanism on hero/first screen | **PASS (static)**; live verdict OWED (FUNC-BQA_F23) |
| 7 | Alignment | NONE RECORDED | **— cannot be scored** | **OWED, never passed** |

## §4 Dimension 7 — OWED (verified this session, not inherited)

`~/workspace/cold-start-render/campus-eats/` contains only
`docs/design-tokens.md` (the v1-era tokens file) — no `index.html`, no
CSS, no JS, no assets. Confirmed by listing this session; matches
`fix26/dim7-note.md` §Verification (1). There is nothing browser-qa
could run the ALIGN_F23 matrix against. A leg that cannot score a
dimension does not PASS on that dimension. Disposition per
fix26/SPEC.md §6: RECORDED DECISION (owed, with the reason), not a
pass, not a waiver of the ALIGN_F23 bar. No Campus Eats render will be
built to verify it. The Home Run 52-measurement / 0-problem run is live
alignment evidence about Home Run, not Campus Eats, and is not counted
toward dimension 7.

## §5 R1/R4 scope note (fix26/r1r4-note.md)

The #67/#68 applications above are paper re-trace additions under
current rules, scored statically — they are NOT measurements of a live
render. The Home Run render implements iris-opens in a different
placement (trip code-panel reveal, `index.html:179–180`,
`styles.css:433–446`, `app.js:192`) and implements no hero loop at
all (zero `loop|steam|cycle|wisp|marquee|carousel|ticker|setInterval`
hits across its `index.html`/`styles.css`/`app.js`). Fix #17 R1/R4
stay OWED as defined. The re-trace result (6/7) is unaffected: it never
claimed a live verification of #67/#68.

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7 is OWED.**
