# Fix round #15 — manifest

## Build
- `build.sh` **23,217 lines** (was 23,160; +57 = the fix15 patch block only),
  md5 `1f1a232572b9e12332733688838e1233`
- Backup: `build.sh.before-fix15` (23,160 lines, md5
  `6253677ce02c8625dadb41e1acf32e6b` — the verified starting state).
  Diff vs current build.sh is exactly one 57-line insert (the fix15 block,
  build.sh:23151–23207, verified by `fix15/verify15.py` via difflib).
- Three clean builds, exit 0 (`fix15/build1.log`, `fix15/build2.log`,
  `fix15/build3.log` — see note below on build 3). Counts
  **169 skills / 72 agents / 123 rules / 96 commands / 15 hooks** (unchanged).
- Built-tree manifest hash `35a525fd3796229eb4f85cbb5275c36f`
  (`fix15/manifest1.txt`, `fix15/manifest2.txt`, diff = 0).
- Method: `fix15/fix15.py` (preflight + count==1 asserts) + `fix15/verify15.py`:
  **43/43 checks pass against the BUILT tree**, exit 0.

## What changed (SPEC.md sections A–D; line numbers are in the BUILT tree)

Canonical block (§A, verbatim identical everywhere — one constant in
`fix15.py`, cross-checked against the block quoted in SPEC.md):
- `skills/design-taste-frontend/SKILL.md:55` (after the Captivating-hero bar)
- `skills/ui-ux-pro-max/SKILL.md:16` (after the Captivating bar)
- `skills/less-flat-ui/SKILL.md:16` (after the surface check)
- `skills/polish-pass/SKILL.md:45` (before the Lenses table)
- `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md:20`
  (Hallmark placement — see below)
- `skills/make-interfaces-feel-better/SKILL.md:15`
- `skills/motion-foundations/SKILL.md:46`
- `skills/motion-patterns/SKILL.md:43`
- `skills/motion-advanced/SKILL.md:45`
- `skills/orchestrate/SKILL.md:92` (after the design-package rule)
- `skills/orch-build-mvp/SKILL.md:42` (after the design-package rule)

R1 (every dealt moment applied or re-dealt; baseline gap iris-opens):
Taste step 4 `:244`, step-6 static check `:290`; orchestrate 5a `:61`;
orch-build-mvp step 6 `:51`. All framed as static checks, never screen verdicts.

R2 (one diagram by default on software pages; baseline 0 diagrams):
Taste §3 asset table `:153` — software column `0-2, pulsing` →
`1-2 by default, pulsing; 0 only with a recorded reason in the section plan`.
Hardware / product / place columns unchanged.

R3 (two distinct treatment kinds per app screen; baseline 2 applications,
both Soft Shadow, one kind): `skills/less-flat-ui/SKILL.md:14`
(surface check). No kind hard-coded; the second kind must be theme-matched.

R4 (dealt hero's loop implemented or waived; baseline gap: centred-hero
loop never applied): Taste step 5 `:268`.

R5 (Range pattern's named lead element is its own element; baseline: Bento
lead tile's lone figure folded into the tile): Taste step 4a `:246`.

C1 (dealt faces only): Taste step 4a Typography line `:246`;
ui-ux-pro-max type-scale step `:89`.
C2 (self-host display faces; `@font-face` checkable): Taste step 4a `:246`.
C3 (copy + type checks enforced and recorded in the Type list):
Taste step 6 `:290`; polish-pass harmony verifies the Type list
(consistency only, never a verdict) `:22`.

D1 (screenshot QA at least once before finish; counts from whichever
existing tooling ran it — no duplicate pass):
Taste step 6 `:310`; orchestrate step 5 `:60` + step-6 final-report line `:66`;
polish-pass Capture and verification `:104`; orch-build-mvp step 6 `:51` +
step-9 final-report line `:59`. Findings feed the fix batch like other
checks; browser-qa alone issues pass/fail verdicts on rendered screens.

## Hallmark placement — why gates.md was NOT touched
`references/hallmark/references/gates.md` is staged verbatim from upstream
Nutlope/hallmark v2.0.0 (per PROVENANCE.md) — it was not edited and
verify15.py checks staged == staged source with no canonical block in it.
`references/hallmark/references/hallmark-floor.md` is plugin-authored
(condensed for this plugin from upstream SKILL.md + gates.md §3, per
PROVENANCE.md), so the canonical block went there (`:20`).

## Files edited
- Staged sources (build.sh copies verbatim): `new-skills/design-taste-frontend/SKILL.md`
  (8 subs: canonical + R1/R2/R4/R5/C1+C2/R1-check+C3/D1),
  `new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md`
  (canonical), `new-skills/orchestrate/SKILL.md` (canonical + D1×2 + R1),
  `round2-skills/polish-pass/SKILL.md` (canonical + C3 + D1),
  `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (R3 + canonical).
- `build.sh`: one 57-line patch block appended before STEP 5 (10 upstream
  subs: ui-ux-pro-max ×2, make-interfaces-feel-better, motion-×3,
  orch-build-mvp ×4). No other build.sh line changed.
- Treatments still 1–23; the 3 fix14 less-flat-ui runtime-patch hunks are
  intact (staged vs standalone diff still exactly 3 hunks).

## Deviations / repairs (all recorded, none hidden)
1. **T8/P3 prepend bug, caught before building.** `fix15.py` first wrote the
   Taste step-6 D1 rule as an append after the "Hallmark sloplint" heading
   (wrong place) and the polish-pass D1 as an append that duplicated the
   Capture sentence. Both were repaired in the staged sources before any
   build (D1 now precedes its anchor paragraph in both files; Capture
   sentence appears once), and `fix15.py` was corrected so the two D1
   insertions are REPLACEMENTS, not appends. The script was then only used
   as the record — it was not re-run (single-shot by design; its preflight
   asserts the pre-fix15 state).
2. **Manifest timing + build 3.** `manifest1.txt` was not snapshotted after
   build 1 (procedural miss). Instead, the tree hash after build 2
   (`35a525fd…`) was saved as `manifest1.txt`, the build was run a third
   time (`fix15/build3.log`, exit 0), and the tree re-hashed as
   `manifest2.txt` — identical hash, diff = 0. The diff-0 property is
   therefore established across two consecutive builds (2 → 3) rather
   than (1 → 2). Builds 1 and 2 both exited 0 with identical counts and
   logs. `verify15.py` was re-run after build 3: still 43/43.

## Verification — all three checkers CLEAN (loop closed)

- **Audit #53 (fix15/audit53-report.md): CLEAN — 0 BLOCKING, 0 MINOR.**
  Re-verified from the built files: build.sh 23,217 lines, md5
  `1f1a232572b9e12332733688838e1233`; verify15.py re-run 43/43, exit 0;
  canonical block byte-identical (sha `f7e956a7a132`) ×1 in all 11 files at
  the lines listed above; R1–R5 / C1–C3 / D1 anchors all present at the cited
  lines, framed as static checks / candidate evidence, never verdicts;
  treatments still 1–23; counts 169/72/123/96/15 unchanged; build.sh diff
  exactly the one 57-line insert (23151–23207); gates.md byte-identical to
  staged source, no canonical block; hallmark-floor.md is the correct
  plugin-authored placement (PROVENANCE.md:32–33); standing #13 invariants
  re-verified (sole executor, craft-floor bans, Hallmark floor, no violet,
  anti-derivative, more-not-bolder, snapshot-before-redesign, 2-round
  fresh-verdict budget, Grok slug-only pin). Nothing edited, committed,
  bundled, or re-run; Campus Eats untouched.
- **Dry-run #25 (fix15/dryrun25-report.md): CLEAN — 0 BLOCKING, 0 MINOR.**
  Re-traced Campus Eats under the new rules using BASELINE.md's counting
  rule exactly (not the edited artifact): **25 → 30 elements, +5, +20%**,
  spread across **5 gaining kinds** — Component 18 (0), Treatment 2→3 (+1 R3),
  Visual 1 (0), Motion 2→3 (+1 R4), Moment 1→2 (+1 R1), Type 1→2 (+1 R5),
  Effect 0 (0), Diagram 0→1 (+1 R2). Every R1–R5 moves the count by the +1
  its SPEC claims, each verified against its source spec and rule anchor.
  C1–C3 and D1 anchors present with correct framing; screenshot QA runs at
  least once before finish in both engines, from existing tooling, recorded
  in ledger + final report; standing #13 invariants re-verified clean.
- **Sweep #15 (fix15/sweep15-report.md): CLEAN — 0 BLOCKING, 0 MINOR.**
  332 verdict-shaped hits read (274 md/mjs/py + 58 js/json); every
  fix15-introduced hit explicitly routed (static check / candidate evidence /
  consistency only), never a verdict; canonical block byte-identical in all
  11 files; 0 occurrences in verbatim-staged gates.md; stale counts
  `22 treatments` / `22 textured` = 0 tree-wide and 0 in build.sh; all
  R1–R5 / C1–C3 / D1 anchors verified by reading the lines.

## Results summary

| Measure | Before | After | Change |
|---|---|---|---|
| Design elements (Campus Eats re-trace) | 25 | 30 | **+5, +20%** |
| Gaining kinds | — | — | 5 (Moment, Diagram, Treatment, Motion, Type) |
| build.sh lines | 23,160 | 23,217 | +57 (one insert) |
| build.sh md5 | `6253677c…` | `1f1a2325…` | — |
| verify15.py checks | — | 43/43 | exit 0 |
| Treatments | 23 | 23 | unchanged (no new inventory) |
| Counts (skills/agents/rules/commands/hooks) | 169/72/123/96/15 | 169/72/123/96/15 | unchanged |

## Not done / out of scope (per SPEC)
- No commit, no git bundle, no GitHub touch, no Campus Eats artifact touch.
- No new inventory (no new treatments, skills, or themes).
- No standing rule weakened: "more, not bolder" untouched; screen-verdict
  language appears only as browser-qa's sole-executor statements; craft-floor
  bans, Hallmark floor, no-violet, anti-derivative, snapshot-before-redesign,
  and the shared 2-round fresh-verdict budget are unchanged. No adjudicated
  item re-flagged; fix11 not re-run.
- The Campus Eats re-trace (expected 25 → 30, +20%) is a separate worker's
  job (SPEC §E); this round delivers the rules only.
