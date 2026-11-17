# Dry-run #46, Leg 2 — Campus Eats v5 benchmark re-trace (fix #31)

Re-trace method: same as dry-run #45 (`fix30/dryrun45/dryrun45-benchmark.md`, full
derivation there). This session re-verified the v5 file's figures and the five
rule-trace anchors live in the fix31 built tree; the 7 rule-traced additions
#67–#73 are carried from #45's derivation (unchanged inputs, unchanged anchors).

## §1 Fresh verification of the v5 figures

- `hackathon-ecc/skills/orchestrate/references/design-benchmark-v5.md`: **178 lines**,
  frozen at v5. Total row: literal **61**, stricter **60** (v4 54 + v5 delta 7 = 61).
  Kind sums re-added: 31+8+1+17+1+2+0+1 = **61**; stricter **60**. Matches the file.
- Dynamic inventory 8 items, 1 drive, 2 surfaces, as recorded in #45.
- Dynamic-count boundary re-derived from `fix17/INVENTORY-V4.md` (#47–#50, #54 hover
  micros; #58 marquee pause; #60 sticker-peel): E's 8 stands item for item; the
  defensible range **6–13** (narrow/broad) is unchanged.

## §2 Rule-trace anchors re-checked in the fix31 built tree

| Anchor | Location (this session) | Holds? |
|---|---|---|
| R1 | `design-taste-frontend/SKILL.md:409` — "Every dealt moment is applied or re-dealt" | Yes, same line and text as #45 |
| R4 | `fix15/SPEC.md:91` — "the dealt hero's loop is implemented or waived" | Yes |
| CREATIVE_F25 | `feature-expansion/SKILL.md:59,93,99` | Yes, same lines, anchor texts identical |
| E1 | as traced in #45 | Yes (carried; inputs unchanged) |
| M3 | `make-interfaces-feel-better/SKILL.md:127` | Yes, same line, anchor text identical |

Fix #31 touches `design-taste-frontend` (palette-first weave) but the R1 anchor sits
at the same line with identical text; no anchor moved.

## §3 Re-trace totals (carried from #45, anchors re-verified above)

- **Re-trace: 68 literal / 66 stricter** (v5 61/60 + the same 7 rule-traced additions
  #67–#73). Kinds 7 → 8, five kinds above v5.

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
`~/workspace/cold-start-render/campus-eats/` still contains only `docs/design-tokens.md`
(verified by listing this session) — no `index.html`, no CSS, no JS, no assets, so
browser-qa cannot run the ALIGN_F23 matrix on it. Disposition per fix28/SPEC.md §7:
RECORDED DECISION (owed, with the reason), not a pass. No Campus Eats render was built.
The Home Run 52-measurement / 0-problem run is live alignment evidence about Home Run,
not Campus Eats, and is not counted toward dimension 7.

**R1/R4 scope note (fix26/r1r4-note.md, as in #45):** the #67/#68 applications are
paper re-trace additions, scored statically — NOT measurements of a live render. The
Home Run render implements iris-opens in a different placement (trip code-panel
reveal) and implements no hero loop at all. Fix #17 R1/R4 stay OWED as defined.
The 6/7 re-trace result is unaffected: it never claimed a live verification of #67/#68.
