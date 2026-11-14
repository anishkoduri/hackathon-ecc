# Design Benchmark — Campus Eats v5 (fix #25 §4(d), BENCHMARK_V5_F25)

The bar the design package must now beat. A build that would have scored
like v5 is BELOW the bar. This file is frozen at v5: its figures are the
recorded v5 figures and are not edited. A future fix that re-baselines
writes a new benchmark file and cites it; it does not rewrite this one.

Staged source: `new-skills/orchestrate/references/design-benchmark-v5.md`;
shipped as `skills/orchestrate/references/design-benchmark-v5.md` (the
whole `references/` directory ships with orchestrate — see `build.sh:224`).
The design package reads this file alongside `design-inventory.md` at the
design-package step, BEFORE deciding. The decision record carries the
per-dimension beat-v5 table (see §2); the static checks are in
orchestrate step 5a (BENCHMARK_V5_F25) and polish-pass non-negotiable 5.
Every verdict on a rendered screen stays browser-qa's alone.

## §1 The v5 figures (as recorded — read from the record, not asserted)

Source: fix #17 dry-run #28 recount (`fix17/dryrun28-report.md`), the v4
inventory (`fix17/INVENTORY-V4.md`), and the parent guidance
(`fix17/PARENT-GUIDANCE.md`), all under the fix #15 counting rule
(`fix15/BASELINE.md`: one discrete, deliberate design application = one
count; instances count individually; exactly one kind per element, by
precedence Moment > Effect > Visual > Diagram > Treatment > Component >
Motion > Type; copy words, sections, the theme itself, and a dealt item
with no recorded application do NOT count).

### Counts

| Kind | v4 | v5 delta | v5 total (literal) | v5 total (stricter) |
|---|---|---|---|---|
| Component | 28 | +3 (coin stack, bus-pass ticket, sticker sheet) | **31** | 31 |
| Treatment | 6 | +2 (washi, marker checks ×3 as ONE feature) | **8** | 8 |
| Visual | 1 | 0 | **1** | 1 |
| Motion | 15 | +2 (sticker-peel, confetti) | **17** | 16 |
| Moment | 1 | 0 | **1** | 1 |
| Type | 2 | 0 | **2** | 2 |
| Effect | 0 | 0 | **0** | 0 |
| Diagram | 1 | 0 | **1** | 1 |
| **Total** | **54** | **+7** | **61** | **60** |

- v5 total, literal (primary reading): **61 elements**. v4 54 + v5 7 = 61.
  Growth v4 → v5: **+7 (+13% on 54)**. Motion 15 → 17 (**+13%**).
  The SPEC's "motion/interactivity +10–15% over v4" is that +13% band
  (total and Motion alike). Note, honestly: the v4 brief's own
  "motion +10-15%" label was FLAGged in INVENTORY-V4.md §4 as
  inconsistent with the literal count (v4 literal is +14 on v3, +35%;
  +15% is reachable only under alternative reading A, which excludes
  motion layered onto existing pieces). The +13% here is the measured
  v4 → v5 literal growth, not the brief label.
- Stricter reading: **60** (Motion 16 — the confetti-stars ambient loop
  #66 excluded, same class as the v4 #51 float-card bob reading A
  excludes). Sensitivity, recorded not hidden: marker checks counted
  per instance (×3) instead of as one feature → Treatment 10,
  **total 63**; confetti kept under the stricter reading → stricter 61.
- The v5 delta, element by element (#60–#66): hover sticker-peel corner
  on the price ladder (Motion); washi tape strips pinning the ramen
  photo (Treatment); pink marker checks that draw themselves in as the
  step cards reveal, ×3 counted as ONE feature (Treatment); five-coin
  stack filling in step with the budget stepper (Component); perforated
  Northgate Loop bus-pass ticket under the napkin receipt (Component);
  tappable five-sticker sheet in the ink band — taco, coffee, star,
  heart, burger (Component); drifting confetti stars in the ink band
  (Motion).
- Version history (literal): v1 25 → v2 32 → v3 40 → v4 54 → **v5 61**.
  No Effect has been applied at any version (v1–v5).

### Theme, hero, moments

- Theme: **Sticker** (light/display-heavy/chromatic-magenta). Hero deal:
  **`centred`**. Moments dealt: **letters-assemble + iris-opens**.
- letters-assemble is APPLIED (ink-band statement "EAT WELL. SPEND
  LESS."). **iris-opens is DEALT but has NO recorded application
  anywhere in the available source** (dry-run #28 §C) — the tokens file
  lists it as dealt only, and a grep for "loop" across the artifact
  directory returns zero hits. The R4 hero loop likewise has no recorded
  application. This is a finding about what is RECORDED, not a proven
  fact about the live render (see the caveat below).
- Hero inventory (v5): centred deal + hero entrance (Motion #10) +
  app-frame window (Visual #3) + news pill + button pair + search bar +
  spot rows ×3 + floating cards ×2. No recorded hero loop.

### Dynamic interface and functionality (enumerated from the record)

The v5 interactive / live-state inventory, enumerated from the render
history in INVENTORY-V4.md and PARENT-GUIDANCE.md — **8 items**. This
enumeration is derived from prose descriptions, not counted from live
source; the dry-run worker re-derives it from the same history and
records any disagreement, it does not take this list on trust:

1. Budget stepper with live total (live probe: drove $8 → $12, the $10
   row flipping to "Fits").
2. "Roll a craving" interactive bit, with aria-live announcement.
3. "Tried it" stamps on pick cards (one interactive feature).
4. Tappable five-sticker sheet in the ink band (live probe: Taco sticker
   click registered).
5. Search bar inside the app-frame.
6. Marquee pauses on hover.
7. Sticker-peel hover on the price ladder.
8. Five-coin stack filling in step with the budget stepper.

Cross-surface state drives in v5: **1** — the stepper drives the live
total AND the coin stack AND the $10 row flip. Live-data surfaces in
v5: **2** — the app-frame spot list (open/closed tags, prices) and the
budget stepper (live total). All other v5 motion/interactions still
work (scroll reveals with fail-safe, hovers).

### Alignment

**No Campus Eats alignment figure exists anywhere in the record.**
Campus Eats was never alignment-measured. The fix #23 alignment
assertions (ALIGN_F23) were verified on Home Run (52 measurements, 0
problems, 4 widths × 13 states) — not on Campus Eats. The alignment
bar for the re-trace is therefore not "beat a v5 number" but the
assertions themselves (§2, dimension 7).

### Caveat on provenance (stated, not hidden)

The live v5 artifact is NOT in this workspace:
`~/workspace/cold-start-render/campus-eats/` holds only the v1-era
`docs/design-tokens.md` (114 lines, pre-fix15 direction) — no
`index.html`, no assets, no JS/CSS to measure. The v5 counts above
are the v4 inventory (54, from render history) + the v5 delta (7
elements, as named in the parent guidance), classified by the
BASELINE.md rule from one-line descriptions. The tokens file omits
all 36 v2–v5 elements known to be in the render, so absence from it
proves nothing about the live page — including the iris-opens / hero
loop non-application above. A live re-measure against the real
artifact would supersede these figures; until then they are the
recorded benchmark, and the dry-run scores against them as written.

## §2 "Beats v5" — pass criteria per dimension

The re-traced design beats v5 only if it passes ALL SEVEN dimensions.
Failing any one dimension = below the bar. A design that ties v5 on
any dimension is below the bar on that dimension — a tie is not a beat.
"Better" is measured on these dimensions, not count alone.

| # | Dimension | v5 figure | Beat-v5 pass criterion (re-trace) | How scored |
|---|---|---|---|---|
| 1 | Element count | 61 literal / 60 stricter | **≥ 62 literal AND ≥ 61 stricter** (BASELINE.md literal rule; instances count individually; one kind per element by precedence) | Statically, from `docs/design-tokens.md` + the re-traced element list |
| 2 | Variety | 7 kinds represented (Component, Treatment, Visual, Motion, Moment, Type, Diagram); Effect 0 | **≥ 7 kinds represented AND ≥ 2 kinds strictly above their v5 counts** (growth spread across kinds, not all in one — the fix #15 spread rule, raised). No nonzero v5 kind may drop below its v5 count without a recorded D19 reason. | Statically, from the same re-traced list |
| 3 | Hero strength | Centred deal + entrance + app-frame + 1 dealt moment applied; no recorded hero loop | Hero carries the full v5 hero inventory **AND at least one of: (a) the R4 hero loop applied, (b) a second dealt moment applied in/near the hero.** The STRENGTH verdict itself (does the hero stop a judge) is browser-qa's alone — the static check is the inventory + the loop/moment application, recorded in `docs/design-tokens.md`. | Static inventory + browser-qa live verdict (owed, never claimed statically) |
| 4 | Motion | 17 literal / 16 stricter | **Motion ≥ 18 literal AND ≥ 17 stricter** | Statically, from the re-traced list (both readings) |
| 5 | Dynamic interface | 8 interactive / live-state items (§1); 1 cross-surface state drive | **≥ 9 interactive / live-state items AND ≥ 2 cross-surface state drives** (a control whose state change drives another surface). Whether controls actually respond and changes are actually choreographed is browser-qa's live check alone. | Static count + browser-qa live verdict (owed) |
| 6 | Functionality | 2 live-data surfaces; mechanism (spot list + budget) shown on the app surface | **≥ 3 live-data surfaces with real state (not frozen mock content), mechanism visible on the hero surface or the first screen after it.** Whether the mechanism actually shows and works is browser-qa's live check alone (FUNC-BQA_F23). | Static count + browser-qa live verdict (owed) |
| 7 | Alignment | NONE RECORDED (no v5 figure) | **0 problems across the full ALIGN_F23 coverage matrix** — desktop 1440, mid 900 (band 768–1100), mobile 390, every flow state measured + screenshotted (COVER_F23) — executed by browser-qa. A build with an unverified width or state is not shippable (BLOCK_F23). | browser-qa live verdict (owed, never claimed statically) |

## §3 How the dry-run scores it (Leg 2 benchmark definition)

The dry-run's design leg (Leg 2) re-traces the SAME Campus Eats brief
("pretend I told you to make a site" — no design direction from the
user; campus food-discovery landing for Texas A&M students) under the
current rules, by the dry-runs #25–#28 method: a paper re-trace through
the updated skills, counting with the BASELINE.md literal rule exactly
(same kinds, same precedence, same instances-count rule) — not a count
of a rebuilt artifact and not an assertion. The re-trace then scores
per dimension against the §2 table above, and the leg reports a
per-dimension table (dimension, v5 figure, re-traced figure, PASS /
FAIL), not a single number.

- Dimensions 1, 2, 4 score statically from the re-traced element list.
  Dimension 3 scores statically on inventory + loop/moment
  application; its strength verdict is owed to browser-qa.
- Dimensions 5 and 6 score statically on counts (items / drives /
  live-data surfaces); whether the controls respond, the changes are
  choreographed, and the mechanism works is owed to browser-qa's live
  verdict — the dry-run records it as OWED, never as verified.
- Dimension 7 is entirely browser-qa's live verdict (ALIGN_F23 +
  COVER_F23); the dry-run records the matrix coverage statically and
  the verdict as OWED where the live run cannot execute in the sandbox.
- If a dimension cannot be scored — statically or live — the leg says
  which, and records it as a gap (owed), not as a pass. A leg that
  cannot score a dimension does not PASS on that dimension.
- The re-trace target is the §2 table, not the old bands: the fix #15
  band (+4 to +5, ≥4 kinds) and the fix #17 band (61 ± 2) are
  superseded for this purpose — a re-trace landing at 61 ties v5 and
  FAILS dimension 1, however well it does elsewhere.
