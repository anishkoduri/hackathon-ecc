# Dry-run #40, Leg 2 — Campus Eats v5 benchmark re-trace (fix #25 §4(d))

Method: the dry-runs #25–#28 paper re-trace. The SAME Campus Eats brief
("pretend I told you to make a site" — no design direction; campus
food-discovery landing for Texas A&M students) re-traced under the CURRENT
rules (fix #25: BENCHMARK_V5_F25 bar, TECHDEPTH_F25, ADAPT_F25, REASON_F25,
CREATIVE_F25, plus all prior rules), counting with the fix #15 BASELINE.md
literal rule exactly (one discrete, deliberate design application = one
count; instances count individually; one kind per element by precedence
Moment > Effect > Visual > Diagram > Treatment > Component > Motion >
Type; copy words, sections, the theme itself, and a dealt item with no
recorded application do NOT count). This is a paper enumeration through
the skills, not a count of a rebuilt artifact and not an assertion — no
live Campus Eats render exists in this workspace to measure (only the
v1-era tokens file). Every added element below is traced to the rule that
compels or pushes it.

## §1 Re-derivation of E's dynamic count of 8 (from the record, not on trust)

Sources re-read: `fix17/INVENTORY-V4.md` (elements #1–#66),
`fix17/dryrun28-report.md` (§A recount, §C R1/R4 finding),
`fix17/PARENT-GUIDANCE.md` (:78–79 live probes),
`new-skills/orchestrate/references/design-benchmark-v5.md` (§1).

E's 8 interactive / live-state items, each verified against the record:

| # | Item | Record |
|---|---|---|
| 1 | Budget stepper with live total | INVENTORY #19 stepper + #20 running total; live probe drove $8 → $12, $10 row flipping to "Fits" (PARENT-GUIDANCE:78–79) |
| 2 | "Roll a craving" interactive bit, aria-live | #59 |
| 3 | "Tried it" stamps on pick cards (one feature) | #44 (counted once as one feature) |
| 4 | Tappable five-sticker sheet in the ink band | #65; live probe: Taco sticker click registered (PARENT-GUIDANCE:79) |
| 5 | Search bar inside the app-frame | #4 (input control) |
| 6 | Marquee pauses on hover | #58 |
| 7 | Sticker-peel hover on the price ladder | #60 |
| 8 | Five-coin stack filling in step with the budget stepper | #63 (live state driven by the stepper) |

**Reproduced: 8, item for item.** But the boundary E used is a judgment
call, and the benchmark file does not state it: E counts state-changing
features while excluding pure hover micros (#47–#50 photo tilt, name
warms, tap-to-pop, wiggle; #54 compass grows) and ambient loops
(#51–#53, #55–#57, #66). No stated distinction separates #60 (peel) and
#58 (marquee pause) — both hover-driven — from #47–#50/#54. Consistent
alternatives, both defensible from the same record:

- **Narrow** (only controls with persistent/operable state; hover-only
  behaviours out): #4, #19, #44, #59, #63, #65 = **6** (drops #58, #60).
- **Broad** (every hover-driven state change counts): 8 + #47, #48, #49,
  #50, #54 = **13** (ambient loops stay out as non-interactive).

So the v5 dynamic figure is **8 under E's list, with a defensible range
of 6–13**. The beat-v5 criterion (≥ 9 items) is anchored to E's 8; the
re-trace passes it under E's and the broad reading and fails under the
narrow reading (see §3, dimension 5). Recorded here, not smoothed over.

Cross-surface state drives, re-derived: **1** — the stepper drives the
live total AND the coin stack AND the $10 row flip. No other drive is
recorded: Roll-a-craving surfaces a suggestion but drives nothing else;
the sticker sheet tap changes only the sticker; no record of the search
bar filtering anything. **Stands at 1.**

Live-data surfaces, re-derived: **2** — the app-frame spot list
(open/closed tags, prices) and the budget stepper (live total). The coin
stack is the same stepper state, not a separate surface. **Stands at 2.**

## §2 The re-traced element list (v5 + 7)

v5 as recorded: 61 literal / 60 stricter — Component 31, Treatment 8,
Visual 1, Motion 17, Moment 1, Type 2, Effect 0, Diagram 1. The re-trace
keeps every v5 element (a re-trace under current rules is additive here:
nothing in the new rules removes a v5 element) and adds seven, each
rule-traced:

| # | New element | Kind | Rule trace |
|---|---|---|---|
| 67 | iris-opens APPLIED as the section transition (hero → picks) | Moment | R1 (fix #15) + BENCHMARK Dim 3 + Taste deal. Dealt-but-unapplied in v5 (dry-run #28 §C); the beat-v5 bar makes applying it (or the hero loop) part of beating v5. Counts under both readings (a moment application, not layered motion). |
| 68 | R4 hero loop APPLIED inside the app-frame window (spot rows cycle; steam wisp over the ramen photo in the window) | Motion | R4 / M4 + BENCHMARK Dim 3. Literal only: an ambient loop on an existing piece, excluded under stricter reading A (same class as v4 #51 float-card bob). |
| 69 | Dietary filter chips (veg / late-night / under-$10) above the spot list — tap filters spot rows live and updates the live count figure | Component | U1/E1 + CREATIVE_F25 (filtering is a capability — what the product DOES, not polish) + Dim 5/6. Both readings. Interactive item +1. Cross-surface drive +1 (chips → spot rows + count figure). |
| 70 | Budget preset chips ($5 / $10 / $15) beside the stepper — tap sets the stepper value | Component | U1/E1 + Dim 5. Both readings. Interactive item +1. Feeds the existing stepper drive (not a new drive). |
| 71 | Live "N open now" count figure in the app-frame header, updating with the filters and time of day | Type | Dim 6 (the third live-data surface) + CREATIVE_F25. Precedent: #20 running total is a Type figure. Both readings. |
| 72 | Frosted-glass backdrop-blur on the sticky app-frame header (backdrop-filter blur + saturate) | Effect | E1 push + Dim 2 (variety needs a kind above v5; Effect is 0 at every version v1–v5 — the first Effect ever). Both readings (an applied effect, not motion). |
| 73 | Filter-chip hover micro (chip lifts + check draws on hover) | Motion | M3 (hover micros) + Dim 4 stricter. Both readings: the hover-micro class is KEPT under stricter reading A (same as #47–#50). |

Re-traced totals:

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

Kinds represented: 7 → **8** (Effect joins). Kinds strictly above v5:
Component 31→33, Motion 17→19, Moment 1→2, Type 2→3, Effect 0→1 —
**five** kinds. No nonzero v5 kind drops.

E1 creative push (at least one genuinely original element per build):
#69/#71 (filter chips + live open-now count — a filtering capability no
template produces) and #72 (the first Effect in the inventory). The
substance half (TECHDEPTH_F25) is not scored in this design leg: the
re-trace is a design enumeration, and no `docs/scope.md` exists for it;
the technical-depth check is Leg 5's collab-editor fixture, not this leg.

## §3 Per-dimension scoring

| # | Dimension | v5 figure | Re-traced figure | Criterion | Result |
|---|---|---|---|---|---|
| 1 | Element count | 61 literal / 60 stricter | **68 literal / 66 stricter** | ≥ 62 / ≥ 61 | **PASS** |
| 2 | Variety | 7 kinds; Effect 0 | **8 kinds; 5 kinds above v5** (C, Motion, Moment, Type, Effect); no kind drops | ≥ 7 kinds AND ≥ 2 kinds above v5 | **PASS** |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop recorded | Full v5 hero inventory **+ (a) R4 hero loop applied (#68) AND (b) second dealt moment applied (#67, section transition at the hero→picks boundary)** | Full inventory AND (a) OR (b) | **PASS (static)** — the STRENGTH verdict (does the hero stop a judge) is browser-qa's alone: **OWED** |
| 4 | Motion | 17 literal / 16 stricter | **19 literal / 17 stricter** | ≥ 18 / ≥ 17 | **PASS** |
| 5 | Dynamic interface | 8 items; 1 cross-surface drive | **10 items** (8 + #69 chips + #70 presets); **2 drives** (stepper drive + filter drive) | ≥ 9 items AND ≥ 2 drives | **PASS (static)** under E's count — live behaviour (controls respond, changes choreographed) is browser-qa's alone: **OWED**. Sensitivity: narrow reading (v5=6) → re-trace 8 < 9 **FAILS**; broad reading (v5=13) → re-trace 15 ≥ 14 **PASSES**. |
| 6 | Functionality | 2 live-data surfaces | **3 live-data surfaces** (spot list, stepper total, #71 live count); mechanism on the hero/first screen (spot list + budget in the app-frame) | ≥ 3 surfaces, mechanism on hero/first screen | **PASS (static)** — whether the mechanism actually shows and works is browser-qa's live verdict (FUNC-BQA_F23): **OWED** |
| 7 | Alignment | NONE RECORDED | **— (cannot be scored)** | 0 problems across the full ALIGN_F23 matrix (COVER_F23), browser-qa live verdict | **OWED — never passed.** No live Campus Eats render exists in this workspace to run browser-qa on. A leg that cannot score a dimension does not PASS on that dimension. |

**Benchmark result: 6 of 7 dimensions pass statically; dimension 7
(alignment) is OWED.** The re-trace beats v5 on every dimension that can
be scored in this sandbox. The Home Run render re-run (Leg 2's other
half) is the live alignment evidence that exists — 52 measurements, 0
problems — but it is evidence about Home Run, not Campus Eats, and is not
counted toward dimension 7 here.
