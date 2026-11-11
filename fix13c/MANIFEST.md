# MANIFEST — Fix program #13c (coordinator): fix the 2 minors from dry-run #15

Finding source: dry-run #15 (Campus Eats) on the fix-#13b build — 0 blocking / 2 minor, NOT CLEAN. Audit #43 on the same build: ZERO ERRORS. This round fixes both minors, then Audit #44 + dry-run #16 run on the same build.

## 0. Build record

- `build.sh` pre-fix13c: 22,316 lines, md5 `52019e0a317fff632e8f73bfc8b16967`. Backup: `build.sh.before-fix13c` (same md5).
- `build.sh` post-fix13c: 22,361 lines (+45), md5 `a1fade6ce94bf120bdcbc39b19726f0b`. `bash -n` OK.
- Rebuilds: build 1 exit 0; build 2 exit 0. **Manifest diff between build 1 and build 2 = 0 (reproducible).** Manifests: `fix13c/manifest-build1.txt`, `fix13c/manifest-build2.txt` (3,383 files each).
- Counts: **169 skills, 72 agents, 123 rules, 96 commands, 15 wired hook events (16 scripts incl. adapter.js) — UNCHANGED.** Size: **57 MB — UNCHANGED.** No new skills/agents/rules/commands. No pins touched. No zip/upload. Repo/bundle untouched.
- Scripts: `fix13c/fix13c.py` (staged-source edit, count==1 assert) + `fix13c/fix13c-assemble.py` (build.sh block insertion, preflight anchors count==1 against the post-fix13b built tree; idempotency guard; backup). Logs: `fix13c/build1.log`, `fix13c/build2.log`.

## 1. The 2 minors — re-traced in the built pre-fix13c tree, both CONFIRMED

- **Minor 1 CONFIRMED (substantive)** — `skills/orch-build-mvp/SKILL.md:40` (step 4, GAN-loop step) stated the distinctiveness bar ("Verify the built app's primary screens against the distinctiveness bar — …") with NO executor named, while the GAN evaluator's rubric scored "Distinctive, cohesive visual identity" (`skills/gan-style-harness/SKILL.md:121`, Design Quality 7-8) — a second screen judge before browser-qa's step-6 loop. Audit #43's scope-8 claim ("no second executor anywhere") did not cover the rubric.
- **Minor 2 CONFIRMED (wording only)** — `skills/polish-pass/reference/impeccable-critique.md:222`: the example critique question offered "warmer/bolder/more playful" as tonal options, presenting "bolder" as a direction a user might choose, in mild tension with the "more, not bolder" posture.

## 2. Changes — file:line IN THE BUILT PLUGIN (all verified by grep)

### Staged source (fix13c.py)
- **impeccable-critique.md:222** — "should it feel warmer/bolder/more playful?" → "should it feel warmer / more playful / more distinctive?" Staged source `round2-skills/polish-pass/reference/impeccable-critique.md` is byte-identical to the built copy (diff empty). "warmer/bolder" hits in the built file: **0**.

### Build.sh block fix13c (LAST, just before STEP 5; block at build.sh:22307, STEP 5 at :22352)
- **orch-build-mvp SKILL.md:40** (M1a) — step-4 bar statement now reads: "The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — …" and ends: "The GAN evaluator does NOT judge screen distinctiveness: its Design Quality / Originality rows defer to browser-qa (see `gan-style-harness`)." Old sentence residue: **0**.
- **gan-style-harness SKILL.md:118** (M1b) — scoping note added INSIDE the rubric ```markdown fence (fence opens :115, note at :118, so it lands in `gan-harness/eval-rubric.md` too): "**Screen distinctiveness is NOT scored here.** Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by `browser-qa` in the visual loop (orch-build-mvp step 6) — never by this evaluator. The Design Quality and Originality rows below score the recorded direction and its code-level application only (direction recorded in `docs/design-tokens.md`; tokens, type, and spacing trace to it in the code). A screen that reads as a default template is a browser-qa finding, not a rubric deduction — do not raise or lower a score for screen distinctiveness."
- **gan-style-harness SKILL.md:123 / :129** (M1b) — the two 7-8 rows now defer: Design Quality 7-8 "…in the recorded direction and its code-level application — screen distinctiveness itself is judged ONLY by browser-qa, never here"; Originality 7-8 "…in the recorded direction — screen distinctiveness itself is judged ONLY by browser-qa, never here". Old bare rows residue: **0**.
- **commands/gan-design.md:36** (M1c) — evaluator-prompt line gains the deferral: "… — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md`, which carries that deferral." Added because /gan-design is the design-focused GAN loop whose evaluator prompt ("would this win a design award?") would otherwise invite a second screen-distinctiveness judgment; its evaluator scores against `eval-rubric.md`, which now carries the deferral. No change to the generator prompt or weights.

## 3. Single-executor verification (built tree)

- "SOLE executor" statements: `browser-qa/SKILL.md:68`, `orch-build-mvp/SKILL.md:40` (new), `orch-build-mvp/SKILL.md:49`, `orchestrate/SKILL.md:193` — all four name browser-qa; no other file names a distinctiveness-bar executor.
- The evaluator agent (`agents/ecc-gan-evaluator.md`) contains no rubric text and no "distinctive" wording — it reads `gan-harness/eval-rubric.md` (Step 1) and scores against it (Step 4), so the skill-rubric constraint is the single point of control. `commands/gan-build.md` likewise reads `eval-rubric.md` — no change needed. The planner agent (`agents/ecc-gan-planner.md`) writes `eval-rubric.md` from the skill's rubric — no rubric rows of its own.

## 4. Considered and LEFT (not second executors — reasoning for Audit #44 to challenge)

- `gan-style-harness/SKILL.md:269` results table ("| Design | Generic AI slop | Distinctive, polished | N/A |") — Anthropic's published Solo-Agent-vs-GAN results, descriptive, not a judgment instruction. Left.
- `commands/gan-design.md:39` generator prompt ("Push for creative leaps — unusual layouts, custom animations, distinctive color work") — a generation instruction (aim for distinctive work), not a judge of screens. Left.
- `skills/frontend-slides/SKILL.md:26` ("Distinctive design: avoid generic purple-gradient… decks") — a slide-deck style guideline, not the distinctiveness bar and not a screen judge. Left.
- `skills/polish-pass/reference/scoring.md:9` ("Distinctiveness matters" for Persuade surfaces) — a scoring dimension in a reference, not a bar executor. Left.

## 5. Regression greps (built tree)

- Old step-4 sentence ("Verify the built app's primary screens against the distinctiveness bar"): **0**. Old bare rubric rows: **0**. "warmer/bolder": **0** in critique file.
- Grok pin intact: `grok-4.7-high` ×4 in orchestrate SKILL.md; `grok-4.7[` bracket syntax: **0** tree-wide. Posture "more, not bolder": ×1 in orch-build-mvp, ×1 in orchestrate.
- Counts/size unchanged (see §0). No new gates/waits/questions; §7 + deferred-six carve-out untouched; pins + SSML truth untouched; no fix11-stage.py re-run; no pip pinning pass.
