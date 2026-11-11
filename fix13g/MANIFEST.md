# Fix round #13g — MANIFEST

## Build
- build.sh: 22,932 lines (was 22,829), md5 `537193356d1173f418ab09f552989f3a`
- Built tree manifest (two clean builds): `16be505392f1dfa6039d10b58cb0f4cb`, diff = 0
- Counts: 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- Build 1 + build 2: exit 0, "fix13g upstream block applied"

## Method
- `fix13g/fix13g.py`: 10 staged subs (orchestrate, gates.md, craft-floor.md,
  impeccable-critique.md) + preflight of 19 build-patch anchors against the
  post-fix13f built tree — all count==1 before any write.
- `fix13g/build-patch-g.txt`: build.sh block inserted LAST, just before STEP 5
  (after the fix13f block). 19 subs.
- Staged == built verified by diff for all 4 staged files after rebuild.
- Built-tree verification: 35 present-checks OK, 7 old-string checks gone.

## Scope (4 blocking + 10 minor, all implemented)

### BLOCKING
1. **B1 — standalone step 6 fresh-verdict run + render fallback**
   (`skills/orch-build-mvp/SKILL.md` step 6): Hallmark landing audit now has a
   consumer — the ORCHESTRATOR runs the fresh verdict run on the affected
   screens (shared budget, ledger line after the run, scoped to evidence about
   the affected screens), before polish/commit/deploy; on failure the finding
   routes into the 6b redesign/hold/revert path; if the Hallmark audit produces
   no candidate evidence, no fresh round is spent (recorded in the ledger).
   Finish review now names its inputs (render-tier screenshots, stamp
   theme/idea line, theme file, `.hallmark/hero-review.md`) and carries the
   render fallback (skip as a named step, judge from browser-qa's step-6
   captures, never return `recapture`), mirroring orchestrate :195.
2. **B2 — sloplint landing run in standalone step 6**
   (`skills/orch-build-mvp/SKILL.md` step 6): `sloplint.mjs <built page>
   --render` (static tier always; render tier needs pinned
   `puppeteer-core@25.17.0` + Chrome, Windows `CHROME_PATH`; static-only +
   record if render cannot run, never claim a render pass); `--json` counts
   into the Verify fix list; fix every `FAIL`, fix or waive every `REFLEX`.
3. **B3 — shared fresh-verdict budget defined + accounted (both engines)**
   (`skills/orchestrate/SKILL.md` 5b + step 6; `skills/orch-build-mvp/SKILL.md`
   6b + step 6): a "round" is one `browser-qa` verdict run; a fix round costs
   one round (the re-verdict run that closes it); the orchestrator is the
   counter; after every consuming run it updates the single ledger line
   `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` and consults
   that line before spending more — never from working-context memory.
4. **B4 — standalone step 8 deploy on hold, explicit**
   (`skills/orch-build-mvp/SKILL.md` step 8): "The hold blocks only the
   redesign: deploy the reverted verified tree and record its URL and deploy
   path; only the deploy of the held redesign is forbidden." The "Otherwise,
   deploy the working MVP" conditional is gone — the deploy is unconditional
   (mirror of 5c's unconditional URL recording).

### MINOR
- **Audit M3** (`gates.md` staged-scope note): the Step 4/7 walk is named as
  the upstream Hallmark build/review walk (unstaged build-playbook), and the
  staged flow is restated (§1–§3 pre-emit pass, §4 build, §5 Finish checks +
  judged clauses at the finish review, §6 the two reviews).
- **Dry-run M1** (`commands/gan-build.md` step 0, `commands/gan-design.md`
  Setup step 0 + intro): the predicate is defined (file exists AND contains a
  named `Design direction:` line with tokens; empty/heading-only/no-line does
  NOT count). `gan-design` now checks the FILE, not the brief (intro: the
  brief RESTATES the direction; the direction lives in the file).
- **Dry-run M2** (`commands/gan-build.md` Phase 1): step 0 runs ALWAYS,
  including under `--skip-planner` (direction check, not planner work); on the
  `--skip-planner` path the design-lead generates the direction first and the
  first UI slice writes tokens FROM that recorded direction, never inventing
  one. `orch-build-mvp` step 4 carries the matching consistency clause.
- **Dry-run M3** (orchestrate 5b, orch-build-mvp 6b): budget check FIRST — if
  no rounds remain, HOLD immediately without building, record
  `re-verification: BLOCKED` (no fresh-verdict rounds remain), tree stays the
  verified state.
- **Dry-run M4** (orchestrate 5b, orch-build-mvp 6b snapshot rule + revert
  steps): after the build, the orchestrator compares the design skill's
  changed-file list against the snapshot file list (gap recorded before the
  fresh verdict runs); the revert diffs the tree against the snapshot
  directory — an extra file is restored from version control if the tree is
  under it, otherwise named as a snapshot-coverage gap (hold stands).
- **Dry-run M5** (orchestrate 5b, orch-build-mvp 6b): when the redesign is
  built, entries about the redesigned screens are marked `Superseded by
  redesign <redesign-id> — do not re-judge`; the fresh run is scoped to
  evidence about the redesigned screens only.
- **Dry-run M6** (`skills/orch-change-feature/SKILL.md` step 5): re-upload
  conditioned on account access existing AND a hosted link existing; account
  access is the exception — the default path is the blocked fallback.
- **Sweep M1** (`rules/web-design-quality.mdc`): Anti-Template Policy reworded
  as design guidance, not a ship verdict; template-looking surfaces route to
  `.hallmark/candidate-evidence.md` for `browser-qa` (mirrors ui-ux-pro-max
  :91); header + "Patterns to avoid" + checklist reworded the same way.
- **Sweep M2** (`craft-floor.md` :111, :168): template-pattern bans (centered-
  everything hero, hero-metric template, grids of identical cards,
  equal-weight text-only feature sections) append to candidate evidence and are
  fixed only on `browser-qa`'s verdict or a design-notes exception; the :168
  must-fix compulsion is scoped to non-template bans.
- **Sweep M3** (`impeccable-critique.md` :142): the specificity assessment goes
  only to `.hallmark/candidate-evidence.md`; Priority fixes carry a
  generic-template item only when `browser-qa`'s verdict established it.

## Held back (with reasons)
- `commands/orch-change-feature.md` wrapper (:25 "re-upload the video and
  update its link"): left as-is — it is a one-line summary of the skill; the
  skill (now conditioned) governs. Not an agent instruction to execute.
- `skills/devpost-autofiller/SKILL.md` :10/:93 re-upload lines: left as-is —
  user-facing guidance about the Devpost form (the USER holds the account and
  can re-upload); the agent-side removal instruction is the one fixed in
  orch-change-feature.
- Standalone step 7 (commit): left as-is — its text already states "they were
  already reverted to the snapshot (see 6b), so the tree being committed is the
  verified state", i.e. the commit of the verified tree proceeds; only step 8
  lacked the explicit instruction.
- `devpost-autofiller` checklist :93: same reason as :10 (user-facing).

## Bounds kept
No new gates/waits/questions; no new skills/agents/rules/commands; deferred-six
carve-out, Grok 4.7 High pin + picker instruction, anti-derivative rule,
"more, not bolder" posture, CBM phrasing untouched; direction lenses /
live-generate stay out; frontend-slides stays on-demand; pins + SSML truth
held; no fix11 re-run; no pip pinning; no repo/bundle touching. GATE patch
inserted after fix13f, still before STEP 5.

## Checks (to be filled by Audit #48 / dry-run #20 / sweep)
- Audit #48: **1 BLOCKING, 6 MINOR — NOT CLEAN.** All 7 findings coordinator-verified real against the built tree.
  - B1 (orchestrate SKILL.md:195): step-6 fresh-verdict run has no no-candidate-evidence guard; the shared budget can be burned on a run with no scope (standalone has the guard at orch-build-mvp:49; orchestrate has 0 hits for "no candidate evidence"). Fix: mirror the standalone clause into orchestrate step 6.
  - M1 (orchestrate:60, orch-build-mvp:53): typo "working-context memory.;" — my ROUND_DEF ends with a period and the original "; the redesign decision..." follows. Fix: "memory; the redesign decision…".
  - M2 (orchestrate:60, orch-build-mvp:53): duplicated ledger-update sentence — the definition already states the update; the later "After the run, the orchestrator records…" repeats it. Fix: delete the repeated sentence in both.
  - M3 (orchestrate:60, :195): "step 6" / "step-5" numbering collision — Verification-stage numbering vs orchestrate's own numbered steps (step 6 = Commit/README/report, runs no verdicts). Fix: qualify as "Verification step 6" / "Verification step 5".
  - M4 (gates.md:243): §6 Step 6 ("hero review once at Step 6… finish review at Step 7") not covered by the staged-scope note, which names only Step 4/7. Fix: extend the note to Step 6.
  - M5 (orchestrate:61, 5c): lacks the explicit "deploy the reverted verified tree" sentence (0 hits in orchestrate). Fix: add the mirroring sentence.
  - M6 (orch-build-mvp:49): "first run sloplint on the landing page" is confusing (follows the app-scope run). Fix: "then, before the Hallmark audit, run sloplint on the landing page".
- Dry-run #20: **2 BLOCKING, 6 MINOR — NOT CLEAN.** All 8 findings coordinator-verified real against the built tree.
  - B1 (orchestrate:60 5b, orch-build-mvp:53 6b, revert step 2): revert cannot restore redesign residue. `git checkout -- <file>` never deletes untracked files a redesign creates; in the normal first-build timeline nothing is committed to restore from (orchestrate commits only in step 6, :64 "verify → polish → deploy → demo → commit"; standalone only in step 7; only gan-build generator per-iteration commits exist, gan-build.md:41); `git checkout` restores HEAD, not the verified state, wiping legitimate uncommitted Verify fixes. "Diff the tree against the snapshot directory" is unimplementable as written — a literal diff flags every non-snapshotted file, no method given. Fix: snapshot the whole tree (or record pre-redesign hashes); on revert delete untracked created files, restore modified files from the snapshot copy (never git alone), verify with `git status` + a diff restricted to snapshot-listed paths.
  - B2 (gan-build.md:23-24 step 0, gan-design.md:17, orch-build-mvp:38-39 step 4, gan-build.md:36-38 Phase 2): cold-start direction chain broken on the standalone path. Step 0 never reads `docs/decision-record.md` (0 hits in gan-build.md, gan-design.md, Taste, ui-ux-pro-max); spec.md is translated from the record/scope BEFORE /gan-build runs, so spec.md and the freshly generated tokens direction can diverge with no precedence rule; the Phase 2 generator reads only spec.md + feedback, never `docs/design-tokens.md`, so "first UI slice writes tokens FROM that recorded direction" has no carrier into the loop. Fix: step 0 reads the decision record first and adopts its recorded direction when one exists (generate only when the record has none); add `docs/design-tokens.md` to the generator's read list; state spec.md's direction wins on divergence.
  - M1 = Audit M5 (orchestrate 5c lacks explicit "deploy the reverted verified tree").
  - M2 = Audit M3 (orchestrate "step 6" numbering collision).
  - M3 (orchestrate:195, orch-build-mvp:49): finish-review fallback routes `.hallmark/hero-review.md` to the visual loop that already ran (item 5 before item 6; earlier in step 6); the live consumer is the fresh-verdict run via candidate evidence. Also omits the HTML/component source that review-finish.md:3 names as an input. Fix: route hero-review.md to the fresh-verdict run via candidate evidence; add the built-page source to the passed paths.
  - M4: no resolved-marking for candidate evidence fixed in the visual loop (0 hits) — only `Superseded` exists, so the step-6 fresh run can spend a round re-judging already-fixed screens. Fix: mark entries resolved (screen + fix); scope the fresh run to unresolved entries.
  - M5: single global `re-verification: PASSED/BLOCKED` entry cannot distinguish two polish-routed redesigns (snapshots are per-redesign-id, the entry is not). Fix: key the entry per redesign-id; checks consult the entry for that redesign.
  - M6 = Audit M6 ("first run sloplint" wording).
- Single-executor sweep: **1 BLOCKING, 2 MINOR — NOT CLEAN.** All 3 findings coordinator-verified real against the built tree.
  - B1 (impeccable-craft-floor.md:16, :30, :34–35 + tie-breakers): the Impeccable craft floor's Refuse list compels rewrites of page-level template patterns on polish's own render judgment — :30 "recognizing that means rewriting the element, not softening it", :34 same-size-cards-as-page-structure, :35 hero-metric template — the IDENTICAL patterns craft-floor.md:111 routes to candidate evidence in #13g M2. The file itself says the Refuse items "are the category's defaults, not bans", yet polish.md:39 ("its bans are absolute; where the two floors disagree, the stricter ban wins"), design-taste-frontend ("its bans are absolute — a pinned brief never overrides a ban — and where it and this skill disagree, the stricter ban wins"), and polish-pass SKILL.md:92 carry the absolute-bans gloss, resolving the conflict against the M2 routing. Nuance: ui-ux-pro-max:87 already carries the correct carve-out ("absolute as static/code-level checks … design guidance / static-check evidence, never a pass/fail verdict"), so its fix is narrower. Fix: scope the two template-pattern Refuse items (:34, :35) to the M2 routing; correct the absolute-bans/stricter-wins gloss in polish.md:39, design-taste-frontend, and polish-pass SKILL.md:92.
  - M1 (impeccable-critique.md:593–599): Design Health Score bands frame ship/redesign decisions — :595 "36–40 Excellent | Minor polish only; ship it", :599 "0–11 Critical | Redesign needed; unusable in current state" — on Assessment A's rendered-page score, not browser-qa. No gate consumes the band (report wording only). Fix: reword to guidance without a ship/redesign verdict.
  - M2 (polish-pass SKILL.md:22, :96; polish.md:24, :79): Harmony check records per-screen "pass/fail" ("record per-screen pass/fail in the report under 'Harmony check'"; report template "<pass/fail on consistency only>") while the same file states pass/fail verdicts on rendered screens are browser-qa's alone. Fix: record "consistent / diverges (candidate evidence for browser-qa)" instead of "pass/fail".
