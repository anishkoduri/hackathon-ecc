# Fix #17 — parent guidance for the implementation phase

The analysis coordinator completed (Nov 11, ~16:38 CST) and closed; the
implementation phase needs a FRESH coordinator spawn once fix #16 is closed
and the v5 render edit has landed. Do not resume the analysis coordinator —
it is completed. Read this file plus fix17/INVENTORY-V4.md, the SPEC draft,
and the skill map before starting.

## Analysis findings (from the handoff, Nov 11 ~16:38 CST)
- v4 inventory: **54 elements literal** (v1 25 → v2 32 → v3 40 → v4 54).
  By kind: Component 28, Treatment 6, Visual 1, Motion 15, Moment 1,
  Type 2, Effect 0, Diagram 1. The v4 delta is +14, of which 13 is Motion;
  under the stricter reading (motion layered onto existing pieces is not a
  new element) v4 is 46, +15%. Both readings are recorded in
  fix17/INVENTORY-V4.md. 23 back-port gaps + 1 minor; 6 elements already
  covered by fix #15.
- Reconciliation notes: budget-bar scale ticks are excluded as detailing
  (v2 is +7, not +8); R1 iris-opens + R4 hero loop appear NOWHERE in the
  artifact deltas — an open compliance question, not a rule gap.
- Skill map: fix #15 anchors 30/30 present. SPEC draft: rules U1/T1/F1/
  M1–M6/E1, predicted 33.
- Fix #16 status at analysis time: NOT closed (no MANIFEST.md; build.sh
  23,213 lines, md5 42dd82b4…, still carrying 366 claude + 102 codex hits).

## Decisions (parent, Nov 11)
1. THEME CLASHES — Anish's direct feedback overrides the theme do-nots
   where they conflict (he asked for these elements and approved the
   render containing them). Record SCOPED, NAMED exceptions in sticker.md;
   do not weaken the do-nots generally:
   (a) hand-drawn ink scribble/doodle: permitted as a one-off ink-on-paper
       element in theme colors — it is ink on the theme's paper, not a
       mascot or a drawn-sticker character. The "Never a drawn sticker,
       mascot or doodle" do-not stays intact for everything else.
   (b) scroll rise-and-settle entrances: permitted as sticker motion.
       The "nothing on scroll" do-not stays intact beyond that motion.
   Each exception gets a one-line note in the theme file naming the
   reason: added at Anish's direction in the Campus Eats cold-start
   render, Nov 11, 2026 — so a future audit reads it as a decided
   exception, not drift.
2. RE-TRACE TARGET — correct the SPEC draft's 30–34 band: it was built on
   the mistaken premise that 32 was the final count. The target is the
   FINAL artifact's literal count ±2, revised once v5 lands and the live
   artifact is inventoried. Use ONE counting rule applied identically to
   the re-trace and the final inventory (default: BASELINE.md's literal
   rule). Record both readings in the manifest; the pass/fail target is
   the literal one.
3. R1 iris-opens + R4 hero loop compliance — surface it in the re-trace.
   If those rules do not fire in a cold-start rebuild, report it as a
   rule-effectiveness finding with the evidence; do not hide it, and do
   not silently "fix" it by changing the count.
4. SEQUENCING — no file edits until fix #16 is closed (fix16/MANIFEST.md
   exists AND build.sh md5 matches that manifest). The implementation
   coordinator's checker baselines are the latest clean numbers at the
   time it runs (read fix16/MANIFEST.md).

## Added Nov 11 (Anish): creativity push — fold into the E1 rule
Anish, on the v5 render: "add in the skill to be more creative and push
boundaries, just not in a dumb way and in a trailblazing way."
Implementation: strengthen E1 from permission ("may invent within
reason") to an ACTIVE PUSH: the design-lead must push boundaries and aim
to be trailblazing — original, first-of-its-kind decisions, not safe or
derivative ones. "Not in a dumb way" = every boundary push must still
serve the page's job, stay theme-matched and coherent (no broken layout,
no illegibility, no gimmick that fights usability or comprehension), and
stay anti-derivative (generated through the skills, never copied from a
reference). Place the rule where E1 lives (Taste + the design-package
rule + the design skills carrying the canonical block), worded
consistently. The re-trace must show the push firing: at least one
genuinely original element per build that a template would not produce.
- v5 added 7 new elements: hover sticker-peel corner on the price ladder,
  washi tape strips pinning the ramen photo, pink marker checks that draw
  themselves in as the step cards reveal (×3), a five-coin stack that
  fills in step with the budget stepper, a perforated Northgate Loop
  bus-pass ticket tucked under the napkin receipt, a tappable five-sticker
  sheet (taco, coffee, star, heart, burger) in the ink band, and drifting
  confetti stars there. All existing motion/interactions still work
  (scroll reveals with fail-safe, Roll a craving, Tried-it stamps,
  budget stepper, hovers). Audit passed; live probe drove $8 → $12 with
  the $10 row flipping to "Fits"; Taco sticker click registered.
- FINAL literal count: v4 54 + v5 7 = **61 elements**. The re-trace target
  is therefore **61 ± 2 (59–63)**, literal counting, kinds matching the
  final inventory. Do not use the old 30–34 band.
