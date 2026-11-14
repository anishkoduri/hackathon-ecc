# Fix #17 — manifest (back-port ALL Campus Eats render feedback)

- **Status:** CLOSED. Audit #57 CLEAN (0/0), dry-run #28 PASS, sweep #20 CLEAN.
- **Engine:** `fix17/fix17.py` (preflight + staged edits + build.sh block; 22 edits, all count==1 asserts).
- **`build.sh`:** 23,276 lines, md5 `1a999d763e6ec1fb16985d346b106df0` (post-fix-up; pre-fix-up `0775d6f33c5eeb4cf509fdee1cd319d7`; pre-fix17 `532ab5458c22d6341444fdc92cf67ffd`). Backup `build.sh.before-fix17`.
- **Counts:** 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks — unchanged.
- **Goal (Anish):** back-port ALL render feedback into the package "such that if I asked you to redo the render it would look like this final version we're at rather than the first one."

## 1. What changed — every rule change (file:line, anchor → addition)

Full rule texts live in `fix17/fix17.py` (constants U1_RULE, T1_RULE, F1_RULE, E1_RULE, M1_RULE, M2_RULE, M3_RULE, M4_RULE, M5_RULE, STATIC_CHECKS, etc.). Line numbers are the BUILT tree after build 4.

### Staged sources (edited directly; build.sh copies them verbatim)

| # | File (staged → built line) | Anchor (old) | Addition (new) |
|---|---|---|---|
| 1 | `new-skills/design-taste-frontend/SKILL.md` → Taste :248/:250/:252/:254 | Step-4a R5 sentence end ("…distinct from the surface carrying it.") | U1 + T1 + F1 + E1 as four new bold lines after the step-4a paragraph (conflict C1: not appended into the giant :246 line) |
| 2 | Taste → :302 | Step-6 paragraph end ("…whose FAILs block like the checker's:") | Consolidated "Fix #17 static checks" paragraph (U1 count, F1 Source cells, T1 fill ratio + dead-space, M1–M6 Motion-list record, E1 bound checklist) |
| 3 | `new-skills/orchestrate/SKILL.md` → :94 | Canonical block last sentence ("…kind, theme-fit).") | E1 (active push) after the canonical block in the design-package rule |
| 4 | orchestrate → :61 | Verify 5a R1 sentence end ("…(fix #15 R1).") | Same consolidated static-checks paragraph (engine-side mirror) |
| 5 | `round2-skills/polish-pass/SKILL.md` → :22 | Harmony C3 sentence end ("…(fix #15 C3 — consistency only).") | F1 + T1 verification (Source cells, fill ratios — consistency only, never a verdict) |
| 6 | `round2-skills/polish-pass/reference/lenses/typeset.md` → :78 | Rules checkbox "Text zooms to 200%…" | T1 Rules checkbox (fill ≥ 60%, no dead space/overflow/crowding) |
| 7 | typeset.md → :97 | Verify bullet "Typography should rise…" | T1 Verify bullet (fill + 25% dead-space band as a finding) |
| 8 | `~/workspace/cursor-skills/less-flat-ui/SKILL.md` → built :14 | R3 second-kind sentence ("The second kind must be theme-matched…") | R3 widening: a theme-matched handmade surface treatment (tape, perforation, washi, hand-drawn ink mark) counts as a treatment kind; the 23-entry catalogue is the vocabulary, not the limit |
| 9 | less-flat-ui → built :530 | Record-section sentence end ("…not instead of it.") | U1 record: per screen, record page-only elements alongside treatments; handmade treatments record the same way and count toward the two-kinds check |
| 10 | `new-skills/design-taste-frontend/references/hallmark/references/themes/sticker.md` → :88–91 | Last do-not ("…the fills carry the page.") | New "## Scoped exceptions (decided, not drift)" section: exception A (hand-drawn ink marks) + exception B (scroll rise-and-settle entrances), each named, scoped, dated |
| 11 | sticker.md → :74 | Motion line "nothing on scroll." (REPLACEMENT) | "nothing on scroll, except the scoped exception in 'Scoped exceptions' below (scroll rise-and-settle entrances as sticker motion)." |

### build.sh patch block (11 subs, upstream files, no staged source)

| # | File (built line) | Anchor (old) | Addition (new) |
|---|---|---|---|
| 12 | `skills/ui-ux-pro-max/SKILL.md` → :95/:97 | Anti-generic bar end ("…this skill never states a screen pass/fail.") | U1 (app surfaces, ≥1 per primary surface) + E1 (app) |
| 13 | ui-ux-pro-max → :89 | Type-scale C1 sentence ("…(fix #15 C1).") | T1 + F1 (app surfaces) |
| 14 | `skills/motion-patterns/SKILL.md` → :55/:56 | Rules rule 8 ("All token values are imported…") | Rule 9 = M1 (scroll entrances, motion-governed surfaces, Option B scope) + rule 10 = M2 (1500ms fail-safe) |
| 15 | motion-patterns → :271 | Scroll-reveal code-block end (transition line + `/>` + fence) | Fail-safe note (M2; points at `useScrollRevealSafe` — see fix-up below) |
| 16 | `skills/motion-foundations/SKILL.md` → :60/:61 | Rules rule 8 ("Never read `window`…") | Rule 9 = M1 + rule 10 = M2 |
| 17 | motion-foundations → :179 | Accessibility "Motion must degrade gracefully…" sentence | M6 note (reduced-motion gating in both layers; built page must contain the CSS block + JS guard; step-6 record notes the render) |
| 18 | `skills/motion-advanced/SKILL.md` → :336–343 | `useScrollReveal` Usage block end | `useScrollRevealSafe` fail-safe variant (1500ms timer forces the visible state) |
| 19 | `skills/make-interfaces-feel-better/SKILL.md` → :108/:110/:112/:114 | Motion "Icon swaps…" bullet end | Default motion set (v4-level) + M3 + M4 + M5 full rules |
| 20 | make-interfaces-feel-better → :162–164 | Checklist last item ("Small controls still have usable hit areas.") | M3/M4/M5 checklist items |
| 21 | `skills/orch-build-mvp/SKILL.md` → :42 | Step-4 GAN-evaluator sentence ("…(see `gan-style-harness`).") | E1 (standalone-engine mirror) |
| 22 | orch-build-mvp → :53 | Step-6 R1 sentence end ("…(fix #15 R1).") | Same consolidated static-checks paragraph (engine-side mirror) |

## 2. Scoped exceptions recorded (parent decision 1)

In `sticker.md` ("## Scoped exceptions (decided, not drift)", :88–91); the do-nots are otherwise intact:

- **Exception A — hand-drawn ink marks.** A hand-drawn ink scribble underline, doodle trail, or drawn seal/emblem (e.g. a Taco Compass) is permitted as a one-off ink-on-paper element in theme colours — ink on the theme's paper, not a mascot or a drawn-sticker character. The "Never a drawn sticker, mascot or doodle" do-not stays intact for everything else. Added at Anish's direction in the Campus Eats cold-start render, Nov 11, 2026. Covers inventory gaps #8 (scribble), #9 (doodle trail), #7 (compass seal, same one-off ink-on-paper rationale).
- **Exception B — scroll rise-and-settle entrances.** Content sections may enter on scroll with a staggered rise-and-settle entrance (with the 1500ms fail-safe, M2) as sticker motion. The "nothing on scroll" motion rule stays intact beyond that motion. Added at Anish's direction in the Campus Eats cold-start render, Nov 11, 2026. Covers inventory gap #14 (scroll entrances + fail-safe).

## 3. Re-trace — dry-run #28 (PASS)

Target (parent decision 2, overriding SPEC-DRAFT §C's 30–34 band): the FINAL artifact's literal count ±2 = **59–63**. Counting rule: `fix15/BASELINE.md` literal rule, applied identically to the re-trace and the final inventory.

### Recount (final artifact v5)

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
| **Total** | **54** | **+7** | **61 — PASS** | **60** |

- Literal (primary): **61, inside 59–63. PASS.**
- Stricter reading (motion layered onto existing pieces is not a new element; same rule as v4's 46): **60** — only the confetti loop excluded.
- Per-instance sensitivity (marker checks ×3 counted individually, per the v3 #44 precedent note): **63** — still inside the band.
- Full report: `fix17/dryrun28-report.md`.

### Coverage mapping — 0 unmapped, 0 remaining back-port gaps

All 61 elements map to ≥1 rule. 7 are **generic-only** (U1/E1 invention, no named pattern): marquee ticker, picks row, heart pin, fork-flag pin, napkin receipt, coin stack, bus-pass ticket. The rest map to M1–M6 (motion/interactivity), T1 (fill-sizing), F1 (font citations), the sticker exceptions A/B, or fix #15 R1–R5/C1–C3. R3 widening names washi explicitly. M3/M4 verified verbatim in the built tree.

### R1 / R4 rule-effectiveness finding (with evidence)

**R1 (iris-opens) and R4 (hero loop) have no recorded application anywhere in the available source** — the tokens file (`~/workspace/cold-start-render/campus-eats/docs/design-tokens.md:16`) lists iris-opens as dealt only, and a grep for "loop" across the artifact directory returns zero hits. **Caveat (stated, not hidden): this is UNVERIFIED against the live render, not proven absent.** The artifact's live source does not exist in this workspace (`~/workspace/cold-start-render/campus-eats/` holds only the v1-era tokens file, `.hallmark/log.json`, and `.taste-skill/` histories — no `index.html`, no assets, no JS/CSS to grep). That same tokens file omits all 36 v2–v5 elements known to be in the render, so absence from it proves nothing about the live page. The count was NOT adjusted for this. Verification against the live artifact requires the live artifact.

### Rebuild simulation (informational, NOT pass/fail)

A fresh Campus Eats rebuild under the new rules, starting from the fix #15 after-state (30), compels **33** (30 + U1's +3; kinds illustrative C20/T3/V1/Mtn3/Mom2/Ty3/E0/D1) — matching the SPEC draft's prediction — with a realistic **34** if the design-lead takes the permitted scroll-entrance system (+1 Motion via exception B). The pass/fail target is the recount above (61), not this simulation.

## 4. Creativity push — proof it fires

E1 was strengthened from the SPEC draft's permission ("MAY invent") to an **ACTIVE PUSH** ("MUST push boundaries and aim to be trailblazing… a build with no element a template would not produce has not pushed far enough"), placed identically in 4 files (Taste :254, orchestrate :94, orch-build-mvp :42, ui-ux-pro-max :97; sweep-verified identical, md5 `e9d210257261`, 1724 chars; zero "may invent" tree-wide). The push fires in the re-trace: the 7 generic-only elements (§3) and all 7 v5-delta elements (peel, washi, marker checks, coin stack, bus ticket, sticker sheet, confetti) are inventions a template would not produce, each mapped to U1/E1 — and U1 now REQUIRES at least 3 such inventions per build (backed by the nine-point bound checklist in each Unique-list entry, with a floor/ban break blocking). A rebuild that invents nothing is now an incomplete build, not a permitted outcome.

## 5. Checker results — audit / dry-run / sweep

| Check | Result | Report |
|---|---|---|
| Audit #56 (first round) | **NOT CLEAN — 0 blocking, 1 minor** (MINOR-1: fail-safe note pointed at a hook that has the timer inside it) | `fix17/audit56-report.md` |
| Dry-run #28 | **PASS** — 61 literal (in 59–63); stricter 60; coverage 0 unmapped, 0 gaps | `fix17/dryrun28-report.md` |
| Sweep #19 (post-build 2) | **CLEAN (0/0)** — banned terms 0; pins unchanged; 0 fix17 residues; exceptions inventory 798, delta 0 vs fix16; E1 identical ×4; M1/M2 identical ×2; STATIC_CHECKS identical ×3 | `fix17/sweep19-report.md` |
| Audit #57 (re-audit after fix-up) | **CLEAN — 0 blocking, 0 minor** | `fix17/audit57-report.md` |
| Sweep #20 (re-sweep after fix-up) | **CLEAN (0/0)** — same measurements re-verified after the fix-up | `fix17/sweep20-report.md` |

### The fix-up (between audit #56 and audit #57)

- **Fault:** the M2 fail-safe note at `motion-patterns:271` pointed at `useScrollReveal`, but the timer lives in `useScrollRevealSafe` (`motion-advanced:339`). The note was a pointer to a hook that would never make the content appear.
- **Change:** one word in `fix17.py:151` (STAGED_SUBS, motion-patterns fail-safe note) + the build.sh fix17 block regenerated from it (build.sh:23235). Built-tree diff build 1/2 → 3/4 touches exactly ONE file: `skills/motion-patterns/SKILL.md` (hash `096206b2…` → `061fd1fc…`; identifier via `sha256sum` of its `SKILL.md`). No other built file changed.
- **Check:** remaining `useScrollReveal` hits are only the hook definition/uses in motion-advanced (incl. inside `useScrollRevealSafe` itself), not a fail-safe pointer; the note now points at the hook with the 1500ms timer (`motion-advanced:336–343`).

### Builds (build.sh, all exit 0)

| Build | Lines (md5) | Manifest hash | Diff vs previous | Note |
|---|---|---|---|---|
| 1 | 23,276 (`0775d6f3…`) | `3be418fa…` | — (first post-fix17) | 2,665 files; ERRORS: 0 |
| 2 | 23,276 (`0775d6f3…`) | `3be418fa…` | 0 (identical; md5 equality proves build 2 tree = build 1 tree) | dry-run recount taken here |
| 3 | 23,276 (`1a999d76…`) | `d4f04f10…` | exactly 1 entry (motion-patterns) | post-fix-up |
| 4 | 23,276 (`1a999d76…`) | `d4f04f10…` | 0 | final; verify17 59/59, verify15 43/43 |

### Verifiers

- **`fix17/verify17.py`: 59/59 PASS** (all placements + counts; 23 anchors, M6 deferred rules, E1 ×4, sticker exceptions, line-inventory). Also re-run after the fix-up (grep evidence fallback) — 59/59, builds 3/4.
- **`fix15/verify15.py`: 43/43 PASS.** Baseline (check #8) updated to the post-fix17 build record (23,276 lines / `1a999d76…`; before that 23,276 / `0775d6f3…`) — a baseline update, NOT an anchor change (fix #16 precedent: 23,221 / `532ab545…`).

## 6. Standing rules — no regressions (all sweep-verified)

- Staged sources only edited; built tree edited only by build.sh. Build.sh is the source of truth.
- `fix11/fix11-stage.py` NOT re-run. Fix #15 canonical variety + theme-match block verbatim ×11 (11 files) — intact. Fix #15 anchors — `verify15.py` 43/43.
- Fix #16 Grok pins untouched: whole-tree `grok-4.7-high` ×52 occ, `cursor-grok-4.6-high-fast` ×100 occ; bare `grok-4.6-high-fast` 0; bracket syntax 0; `effort=` 0; banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5) 0. **Record correction:** audit #56 reported 71× / 4× — a scope miscount (its grep ran subject-directory-only on the audit12 window, not the whole tree); re-verified whole-tree (excl. `node_modules`). The audit #57 coordinator's `reasoning_effort` count is 2, not 1 (the second is `orchestrate/SKILL.md:160`, pre-dating fix17).
- Rules presented as **static checks / candidate evidence only**, never verdicts — browser-qa remains the sole executor of pass/fail verdicts on screens (all 9 static-check placements say so, and the M1–M6 Motion-list record blocks the build, not the render).
- Design posture "more, not bolder"; craft-floor bans absolute; Hallmark floor binds; no violet introduced; anti-derivative; snapshot-before-redesign; 2-round fresh-verdict budget; no adjudicated re-flags; "30–34" band 0 hits; "SPEC draft" 0; bare "v4 motion set" 0; "may invent" 0.
- Staged-source counts (built tree): 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks — unchanged.

## 7. Decisions and deviations from SPEC-DRAFT.md

- **Re-trace target (binding):** SPEC-DRAFT §C's 30–34 band is wrong (it built on 32 as final). The real target is the final artifact's literal count ±2 = **59–63**; the recount is an independent recount of the final artifact + coverage mapping, NOT the SPEC draft's rebuild simulation (§C predicts 33). The simulation is reported as informational only (§3).
- **M1 scope = Option B:** keep the Taste landing-page scroll ban in `references/motion.md`; scroll entrances on Sticker builds are licensed by sticker exception B, not by M1.
- **R3 widening (not new inventory):** a theme-matched handmade surface treatment counts as a treatment kind. Treatments stay exactly 1..23; no new catalogue entries (colours stay exactly 1..7; header/date are metadata, not entries).
- **M6 as a note, not a numbered rule:** reduced-motion gating lives as a note in motion-foundations Accessibility (:179) + the M2 reduced-motion clause + step-6 static checks — documented judgment, not a numbered rule (it would otherwise upgrade motion-foundations rule count).
- **U1's per-instance counting note:** the recount counts marker checks ×3 as ONE feature per the v3 #44 precedent (similar deployments of the same tool on three surfaces are one feature); per-instance = 63, still in band.

## 8. Artifacts and evidence files

- `fix17/fix17.py` — engine (preflight + 22 edits + build.sh block; 22 count==1 asserts; preflight 11 staged anchors + 11 built anchors, banned-term scan clean).
- `fix17/verify17.py` — 59/59.
- `fix17/SPEC-DRAFT.md`, `fix17/PARENT-GUIDANCE.md`, `fix17/SKILL-MAP.md`, `fix17/INVENTORY-V4.md` — inputs.
- `fix17/audit56-report.md`, `fix17/dryrun28-report.md`, `fix17/sweep19-report.md`, `fix17/audit57-report.md`, `fix17/sweep20-report.md`, `fix17/build1-4.log`, `fix17/manifest1-4.txt`, `fix17/manifest1-4-files.txt`, `build.sh.before-fix17`.
- The Campus Eats artifact (`~/workspace/cold-start-render/campus-eats/`) was NOT touched; it is read-only reference (only the v1-era design-tokens file, `.hallmark/log.json`, `.taste-skill/` histories — no live `index.html` or assets; see §3 caveats).

## 9. Left open

- **Fix #18 implementation** (SPEC at `fix18/SPEC.md`) — gated on fix16/MANIFEST.md AND this manifest both existing, and build.sh md5 matching the latest of the two. FRESH coordinator, not this one. No files touched yet.
- The live smoke test in Anish's Cursor remains a separate open item (not part of fix #17).
- No commit, no bundle, no GitHub touch was made by this fix (per instructions).
- The R1/R4 finding's verification against the live Campus Eats artifact requires the live artifact (the workspace copy has no render source); if the live artifact shows iris-opens / hero loop present, the finding becomes "present but unrecorded"; if absent, it is a real rule-effectiveness gap for a future fix.
