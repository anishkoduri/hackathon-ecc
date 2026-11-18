# Audit #112-A — fix #33 round 33d re-audit (correctness of the fix + the tree)

- **Auditor:** A (correctness of the fix itself + the tree)
- **Date:** Tue Nov 17, 2026 (evening, CST)
- **Fix dir:** `~/workspace/hackathon-plugin/fix33/`
- **Scratch repo:** `~/workspace/hackathon-plugin/fix33/scratch-repo`, git HEAD `dd106ade`
- **Scope:** fix round 33d's fixes for audit #111-B (B-B1..B-B6 blocking + B-M1/B-M2/B-M3 minor) and audit #111-A (A-M1, A-M2), as claimed in `fix-round-33d-report.md`. The worker's report was read but every claim was re-verified from scratch. Nothing was edited, nothing committed.

## Verdict: NOT PASS (minor findings only — no blocking defect)

All six bypasses are **genuinely closed**: each MODEL check was read in the built tree at the claimed line, before the first work step or dispatch on its path, and the trigger paths were re-traced. B-M2, A-M1, and A-M2 are **fixed at every spot audit #111 assigned**. The verifier passes **586/586** on my own re-run, both scans pass, the unpin census holds, the rebuild is intact, and the diff stat is consistent everywhere.

What fails the verdict is **two stale wordings in live SPEC lines** — one wrong census number and one leftover of the exact incoherence A-M2 was assigned to reword. Neither changes the tree, neither makes any guardrail bypassable, and the rework is two one-line SPEC edits — but under the stated verdict rules ("PASS only if everything checks out; any real defect = NOT PASS", minor = docs inaccuracy that doesn't change the tree) and the audit #110 precedent (a stale number in a live doc is NOT PASS), this is NOT PASS.

- Blocking findings: **none** (no A-B item).
- Minor findings: **A-M1, A-M2** below.

## Findings

### A-M1 (minor) — SPEC §3(e) (16f) still says "fast 70"; the true count is 71 pre / 72 post

`SPEC.md:201` (the live §3(e) summary of the §16 checks):

> "(16f) fix33 patch log (0 errors, census 20 ID + 5 PROSE replaced, keeps x2, **fast 70**)"

The true fast count, measured in the same round's own artifacts:

- Patch log `fix33-patch-log.md:7` (regenerated run 10): "`cursor-grok-4.6-high-fast` **x71**".
- `verify33.py:2278` (§16f check): asserts "`cursor-grok-4.6-high-fast` **x71**" in the patch log; `:2265` comment: "fast-worker pin **71 pre / 72 post**"; `:1208`: "fast-worker pin `cursor-grok-4.6-high-fast` at **x72** (71 + 1 schema description, D33-17)".
- `fix33.py:59`: "FAST **x71** unchanged".
- My own grep of the built tree: `cursor-grok-4.6-high-fast` **x72** (71 pre-existing + 1 schema description).

"fast 70" matches neither 71 nor 72. It is the original, pre-D33-16 derivation number — SPEC D33-16 itself says "FAST is x71, **not x70**: the fix33 staged weave added one fast mention". The worker disclosed this line as "known, out of scope, left as-is" (fix-round-33d-report §6); disclosure does not correct the number, and the brief for this audit explicitly asked for a judgment on its own merits. On those merits: a wrong census number in a live SPEC line is exactly audit #110's 110-M1 class. It is the **only** "fast 70" occurrence in the live docs (grep over SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`: one hit, this line).

**Fix:** "fast 70" → "fast 71 pre / 72 post" (or "fast 71" for the pre-state census this clause describes) in `SPEC.md:201`.

### A-M2 (minor) — SPEC §3(h) still carries the "Step 0 (before the size classifier)" incoherence

`SPEC.md:217` (the live §3(h) summary of the D33-22 weave):

> "full MODEL check at the entries of `commands/gan-build.md`, `commands/gan-design.md`, `commands/astra-review.md`, and `skills/orch-pipeline/SKILL.md` **Step 0 (before the size classifier)**"

Step 0 **is** the size classifier (`## Step 0 — Classify size`); the MODEL check is its first content, before the classifier's *scoring* text. That is the correction D33-33 itself states ("Step 0 IS the classifier — the MODEL check is the first content of Step 0, before the classifier's scoring text"), and it is the wording now used in SPEC D33-22 (`:108`), `fix33.py` DECISION-33-22, and the regenerated patch log. The `:217` parenthetical positions Step 0 *before* the classifier — the same incoherence A-M2 was assigned to reword, surviving in a fifth spot the #111-A list did not name (its four assigned spots are all fixed; see §2 below). A charitable reading ("before the classifier's scoring text") is possible, but as written the line contradicts D33-33 in the same document, and a reader following it looks for a classifier that sits *after* Step 0.

**Fix:** reword `SPEC.md:217` to the D33-33 formulation ("Step 0 — the MODEL check is its first content, before the classifier's scoring text").

## 1. Per-bypass verification (built tree, read by me — not the verifier alone)

Standard check wording (all six): "**MODEL check (fix #33, MODELSEL_F33):** before anything else, state the model the orchestrator is running on and record it in the run ledger (`MODEL: <name>` — the actual selected model). If the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback."

### B-B1 — `/orch-change-feature` removal branch: CLOSED

`skills/orch-change-feature/SKILL.md` (built):

- `:45` `## Removing a feature`
- `:47` full MODEL check — first content of the section (blank `:46` between header and check)
- `:49` "When the request is to remove a feature — including a one-prompt removal of a first-build feature routed here by orchestrate:"
- `:51` step 1 "Find the feature's files from the final report's feature-to-files inventory, or, if there is no inventory, trace the feature with `code-explorer` first…"

The check precedes **all 6 removal steps** (step 1 delete-trace is `:51`; steps 2–6 follow). `MODEL` occurs exactly **1x** in the skill — the check itself. Trigger path re-traced: `skill-triggers@1.json:229` `skill:orch-change-feature` ("remove a feature" / "remove this feature") loads the skill directly → same section, same check. Command routing confirmed: `commands/orch-change-feature.md:27` routes removals to this section "instead of the change steps below". The section still never invokes the engine — correctly, since the check now lives in the section itself.

### B-B2 — `/orch-build-mvp` step 1 runs Step 0 first: CLOSED

`skills/orch-build-mvp/SKILL.md:36` (step 1, one long line), read in full:

> "1. Run orch-pipeline **Step 0 first (Classify size — the MODEL check, fix #33, MODELSEL_F33, is the first content of Step 0 and runs before anything else: if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback)**, then Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan). This step does NOT run the full orch-pipeline engine (phase mask 0→6)…"

Both allowed mechanisms are present: step 1 names Step 0 explicitly **and** restates the MODEL ask inline. Within-line order verified: MODELSEL_F33 precedes "ending at Gate 1 (slice plan)", precedes "This step does NOT run the full orch-pipeline engine", and precedes step 2's "Expand automatically". No step runs before the check — step 1 *is* the first step, and the check is inside its first clause. `MODEL` occurs exactly **1x** in the skill. Command file corrected the same way: `commands/orch-build-mvp.md:29` — "This is orch-build-mvp step 1 = orch-pipeline Step 0 (MODEL check + Classify) first, then Phases 0–2 only — it never runs the full engine."

The 33c self-contradiction is corrected, not deleted: SPEC D33-22 (`:108`) now carries "[Corrected in round 33d (D33-25/D33-26/D33-33…)]" and states the choke point "was verified genuine for three orch-* commands only… it was NOT genuine for orch-change-feature's removal branch… or for orch-build-mvp"; the 33c report §1.3 carries the correction banner (quoted in §5 below). The downstream step-4 `/gan-build` drive still re-checks after the model is picked — no second ask, as designed.

### B-B3 — `/feature-dev`: CLOSED

`commands/feature-dev.md` (built):

- `:5` full MODEL check, immediately after the frontmatter (`---` `:1–3`, blank `:4`)
- `:19` first dispatch: "- use `code-explorer` agent (`agents/ecc-code-explorer.md`) to analyze the relevant existing code"

Check (`:5`) precedes the first dispatch (`:19`) and every later step (`code-architect`, implementation, `code-reviewer`).

### B-B4 — `/react-build`: CLOSED

`commands/react-build.md` (built):

- `:5` full MODEL check, immediately after the frontmatter
- `:9` "This command invokes the **react-build-resolver** agent to incrementally fix React build errors…"
- `:11` "**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the react-build-resolver runs as a single-task factory drone with a director brief…"

Check (`:5`) precedes the factory routing/dispatch (`:11`). Drone pins and dispatch text are untouched — `:11` reads exactly as audit #111-B quoted it, and the verifier's _F29 checks (factory routing intact) pass.

### B-B5 — trigger-routed `grill-me`: CLOSED

Built `skills/grill-me/SKILL.md` and staged `new-skills/grill-me/SKILL.md` are **byte-identical**:

- `:6` `# Grill Me`
- `:8` full MODEL check (first content under the heading)
- `:24` `## Workflow`

Check (`:8`) precedes the Workflow (`:24`). Trigger path re-traced: `skill-triggers@1.json:160` `skill:grill-me` ("grill me", "ask me questions about my idea", …) loads the skill directly → the check is in the skill itself.

### B-B6 — trigger-routed `feature-expansion`: CLOSED

Built `skills/feature-expansion/SKILL.md` (staged `new-skills/feature-expansion/SKILL.md` carries the same check at the same line):

- `:6` full MODEL check (first content of the file body, after the frontmatter)
- `:8` decision-record read ("Before proposing anything, read `docs/decision-record.md`…")
- `:45` `### Phase 0 — Ground in what exists (5 minutes, main agent)`
- `:55` `### Phase 1 — Brainstorm with subagents (parallel, four lenses)`
- `:57` "Dispatch four brainstorm subagents **in parallel, in one message**."

Check (`:6`) precedes the decision-record read, Phase 0 grounding, and the Phase 1 four-subagent dispatch. Trigger path re-traced: `skill-triggers@1.json:121` `skill:feature-expansion` ("make it much better", "expand this", …) loads the skill directly → the check is in the skill itself.

Precision note (not a finding): staged vs built `feature-expansion` are **not** byte-identical — they differ in 9 hunks, all pre-existing build transformations (agent short-name → `agent (agents/ecc-*.md)` path rewrites at `:14`, `:51`, `:139`, `:166`, `:198`, `:200–201`, `:219`; the description `:3` gains the brainstorming-carve-out sentence; `:35–36` the ECC-process bullets). The MODEL check line itself is identical, at the same line number, in both copies. The 33d report's "flows verbatim" holds for the guardrail line; the other diffs are not 33d changes.

## 2. B-M2 / A-M1 / A-M2 — all three #111 findings fixed (at their assigned spots)

### B-M2 — latent re-pin path in build.sh: FIXED for the flagged lines

- `build.sh` `grok-4.7-high` lines: **39** (was 44). "The design role runs on model `grok-4.7-high`" occurrences in build.sh: **0**.
- fix13-A header comment updated (`build.sh:22197`); model-agnostic wording verified in the patch text: orch-build-mvp `:22208` ("The design role runs on the model selected in this chat (the design-lead tier inherits the chat model — see the picker note in orchestrate SKILL.md step 4)."), orch-change-feature `:22219`, fix13e orch-add-feature `:22696`, orch-fix-defect `:22701`, orch-refine-code `:22707` (last four: "The design role runs on the model selected in this chat.").
- Built orch-* skills contain **zero** `grok-4.7-high` (grep over `skills/orch-*/SKILL.md` + `commands/orch-*.md`: no matches). Built-tree total: only the two strategic-compact keeps (`skills/strategic-compact/SKILL.md:68`, `:102`).
- The 5 fix33.py scrub tuples are gone: "design role runs on model" occurs **0x** in `fix33.py`. REPLACEMENTS is still **35** tuples (5 scrub out, 5 guardrail in — B-B1, B-B2, B-B3, B-B4 + the orch-build-mvp command correction), and the patch log still reads "Changes (41)".
- **No other build.sh patch writes the pin into any skill** — verified by classifying all 39 `grok-4.7-high` lines in build.sh as old-side vs new-side of their patch tuples (r-string span analysis): the NEW-side pin writes target only `agents/ecc-gan-planner.md` (`:22662`, `:22666`, `:22785`), `commands/gan-build.md` (`:22674`, `:22774`, `:22781`, `:22889`, `:23005`, `:23009`), `commands/gan-design.md` (`:22678`, `:22790`, `:22796`, `:22901`, `:22905`, `:23027`, `:23031`, `:23035`), and `README.md` (`:22686`); the rest are old-side match patterns, the PROC-P3 old side (`:23706`), or comments (`:24129`, `:24139`). **Zero** NEW-side pin writes target any file under `skills/`. The `skills/gan-style-harness/SKILL.md` pins fix33.py still scrubs arrive via the upstream clone source, not a build.sh patch (present in `fix26/scratch-clones/ecc-repo-clean/.../gan-style-harness/SKILL.md`).
- `fix24.py` change is **only** the G-4 sub removal: `git diff` is a single hunk (`@@ -266,9 +266,14 @@`, 8 insertions / 3 deletions) — the third G-4 `sub()` deleted, replaced by an 8-line explanatory comment; the other two G-4 subs untouched. Canonical + scratch md5-identical (`2aa3de92d46263f58aa268a1b4f79c87`). Old parenthetical now **0** occurrences in `fix24.py` and `build.sh` (survives only in the historical assemble scripts and `fix24.py:581`, the README F-1/F-2 old-side anchor).
- Run-10 log: `fix24: 113 change(s)` + `fix24: OK` (was 114 — the removed sub), `fix33: 41 change(s)` + `fix33: OK`, fix31/fix32 OK, `BUILD EXIT: 0`, `ERRORS: 0`.

### A-M1 — stale guardrail-home line numbers: FIXED

Measured by me in the current built `skills/orchestrate/SKILL.md` (staged identical at every cited line): MODELSEL_F33 exactly **2x** (`:14` identity + `:52` pre-grill block); `:52` is the pre-grill block ("**MODEL check — first, before grill-me (fix #33, MODELSEL_F33):** in the first reply, state the model…"); `:64` carries the step-0 back-reference ("**MODEL check (fix #33):** already ran before grill-me (see the MODEL check above) — if the model is still Auto… stop and ask again"); `:95` carries the picker note ("select a specific model in the model picker…"). **L52/L64/L95 confirmed.**

- SPEC D33-5 (`:91`): "L14 … and L52 (the MODEL check…)… The picker note (L95)…"; §3(c) Guards (`:191`): "MODELSEL_F33 present in orchestrate L14 + L52".
- MANIFEST section header (`:201`): "## Decisions (D33-1 … D33-35; full text in SPEC.md §2 and fix33.py)"; summary (`:205`): "guardrail home (orchestrate L14/L52/L95…)".
- Implementation report D33-5 (`:123–124`): L52 + L95, "step 0 (L64) only a back-reference".
- `fix33.py:537` DECISION-33-19 string: "orchestrate L14 + pre-grill MODEL check L52 + L95 picker note (MODELSEL_F33 x2), and the MODEL check is an orchestrate pre-grill block (step 0, L64, carries only a back-reference to it)".
- `verify33.py:3526` §16c check name: "L95 picker note names the specific-model selection"; §16c header comment (`:51`): "L14 + pre-grill MODEL check L52 + L95 picker note".
- Remaining L62/L93 mentions in live docs are all history-framed, exactly as audit #111-A exempted (SPEC §3(a) table `:27`, derivation `:76`, D33-19 as-of-then wording `:105`, replacement text `:136–138`, §3(h) `:216`; MANIFEST `:20`/`:108`; implementation report `:37`). "Step-0 procedure" survives only in SPEC D33-19's as-of-then wording (`:105`, exempted history) and in negations/corrections ("not a step-0 procedure", SPEC `:119`/`:227`, `fix33.py:550`, patch log `:81`).

### A-M2 / S-M1 / B-M1 — "Phase 0" → "Step 0": FIXED at all four assigned spots

- SPEC D33-22 (`:108`): "pointing at the operative check (orch-pipeline **Step 0** / the orchestrate skill)" + "Step 0 is the classifier section — the MODEL check is its first content, before the classifier's scoring text and before Phase 0 Intake".
- SPEC §6 OWED-33-4 (`:230`, `:259`): "RE-OPENED by audit #111-B, FIXED again in round 33d (D33-25/D33-26)".
- `fix33.py:540` DECISION-33-22 + OWED-33-4 strings: Step 0 wording, "before the classifier's scoring text"; patch log regenerated (`:71` DECISION-33-22, `:80` D33-31) with the same Step 0 text.
- `verify33.py` §16m header comment (`:3680`) + check names (`:3697` "full MODEL check ask opens orch-pipeline Step 0 (shared choke point)", `:3702` "points at the orch-pipeline Step 0 MODEL check"): all Step 0. The only remaining "Phase 0" strings in `verify33.py` are legitimate: `:3711` `### Phase 0: Setup` (gan-build's real section anchor) and `:3792–3793` (feature-expansion's real Phase 0 in the B-B6 check name). Remaining "Phase 0" in SPEC/fix33.py/patch-log are likewise legitimate ("before Phase 0 Intake", "Phase 0 grounding", "NOT Phase 0 (Intake)", D33-33's own correction note). The one leftover is A-M2 above (`SPEC.md:217`).

## 3. Verifier + scans — re-run by me, §16n read, probe confirms detection

- `python3 verify33.py <built-tree>`: **586/586 checks pass, exit 0** (my run, `/tmp/audit112-verify.txt`; 586 PASS lines, 0 FAILs). Matches the saved `verify33-run33d.txt`.
- Scan r4 (re-run in place): **76/76, ALL PASS, exit 0** (`/tmp/audit112-r4.txt`).
- Scan r5 (re-run in a probe dir with `fix32.py` + `fix32-patch-log.md` adjacent, probe deleted after): **100/100, ALL PASS, exit 0** (`/tmp/audit112-r5.txt`).
- **§16n read, not just executed** (`verify33.py:3727–3805`, **21 checks**: B-B1 ×2, B-B2 ×5, B-B3 ×2, B-B4 ×2, B-B5 ×3, B-B6 ×3, B-M2 ×2, patch-log ×2). They genuinely assert per-bypass presence **plus order**: B-B1 section-header < MODELSEL < "When the request is to remove a feature" < "1. Find the feature's files"; B-B2 "Run orch-pipeline Step 0 first" plus within-line order (MODELSEL < Gate 1, < "does NOT run the full engine", < step-2 "Expand automatically") plus the command-file "Step 0 (MODEL check + Classify) first"; B-B3 guard before `### 1. Discovery` (earlier than the first dispatch); B-B4 guard before `## What This Command Does`; B-B5/B-B6 built **and staged** presence plus guard before `## Workflow` / `### Phase 0` + `### Phase 1`; B-M2 two string-absence checks on build.sh/fix24.py; patch-log D33-25…D33-35 + OWED-33-5 + OWED-33-4 RE-OPENED.
- **Probe (planted violation, full probe copy under `fix33/audit112-probe/`, deleted after):**
  - Clean copy: **586/586, exit 0** (harness faithful; the first attempt failed outright — verify33.py resolves `build.sh`, `fix28/`/`fix29/`/`fix33/` patch logs and staged sources relative to the plugin root, so a bare built-tree copy is not a valid probe target).
  - Probe: deleted the B-B1 MODEL check line (`skills/orch-change-feature/SKILL.md:47`) from the probe copy → **584/586, exit 1**, exactly the 2 related §16n checks fail ("MODELSEL_F33 present in skills/orch-change-feature/SKILL.md", "full MODEL check ask is the first content of the Removing a feature section"). The verifier detects a missing bypass check precisely.
- **§12 CUT allow-list re-numbering verified:** the 8 feature-expansion entries are at 51, 102, 194, 196, 198, 199, 210, 217 with the re-numbering comment (49→51, 100→102, 192→194, 194→196, 196→198, 197→199, 208→210, 215→217); each line's content re-read in the built file (e.g. `:194` "the `brainstorming` skill is NOT invoked (fix #27, REROUTE_F27)", `:51` "`code-tour` was cut"). Final verifier 586/586 confirms the sweep is green (check-12: 0 un-allow-listed, 47 allow-listed).

## 4. Diff stat, census, and consistency — all verified

- `git diff --stat` (scratch-repo, HEAD `dd106ade`): **47 files changed, +196/−126** (measured by me). Quoted identically in `MANIFEST.md:67` and `fix33-implementation-report.md:230`.
- Grep for stale `+135` / `+136` / `+166` across SPEC, MANIFEST, implementation report, `fix33.py`, `verify33.py`: **zero matches**. (The 33c report's own +166 quote is that round's history, correctly framed.)
- Trigger manifest: **48 keys** (`skill-triggers@1.json`, `grep -c '"skill:'` = 48); built counts **72 skills / 45 agents / 48 rules / 55 commands / 15 hooks** (16 `.js` files in `hooks/` = 15 hooks + `adapter.js`; 17 files incl. `hooks.json`) — the call-map sidecar counts 72/45/48/55/15/48 agree.
- Unpin census re-measured by me (built tree): **ID x0, PROSE x2** (both keeps in `skills/strategic-compact/SKILL.md`, `:68` + `:102`), **XID x0, XPROSE x0, fast x72**. Frontmatter `model:`: **4× `inherit` + 41× `cursor-grok-4.6-high-fast`**, zero others. Drones/fast tier untouched.
- Patch log regenerated on run 10 (md5 `8ae4664f7a64a1bf5ae6fd7cfa044ea0` in both copies; "Changes (41)"; census "grok-4.7-high x20, 'Grok 4.7 High' x7, fast x71 pre"; D33-25…D33-35 recorded; OWED-33-5 recorded; OWED-33-4 RE-OPENED by audit #111-B, fixed again in round 33d). `fix33.py` md5 `cda0e5be0c9ed0030f73fddf07c527c0` in both copies; 33d report md5 `c7ba60150f05f5e65e69023ecdb0af88` in both copies.
- OWED-33-4 re-open + re-fix history recorded (not just re-marked): SPEC §6 (`:230`, `:259`), SPEC D33-23 (`:109`, kept as the superseded history), MANIFEST, `fix33.py:561` OWED string, patch log. OWED-33-5 recorded: SPEC §6 (`:260`) + D33-34 (`:121`), MANIFEST (`:230`), `fix33.py:560`, patch log.
- 33c report §1.3 correction banner present (`fix-round-33c-report.md:86–91`): "[Correction, round 33d (audit #111-B B-B1/B-B2): the choke-point claim in this section was false for two paths… The sentences below are corrected in place; the original wording is preserved in git history.]"

## 5. Shortfall check — fix13/fix13e-assemble.py: claim verified

- `fix13/fix13-assemble.py` carries the old pin text (`grok-4.7-high` ×2, e.g. `:54`, `:65`); `fix13e/fix13e-assemble.py` carries it ×8.
- `grep -n "assemble.py" scratch-repo/build.sh`: **zero matches** (the only "assemble" hits in build.sh are `hvigorw assembleHap` ArkTS hook text). The worker's "never invoked by build.sh, left as history" claim is **verified**. Not a finding.

## Observations (not findings)

- **O-1 — fix33.py is still load-bearing for the gan-build/gan-design/ecc-gan-planner/README pins.** B-M2 moved only the five orch-* design-role lines into build.sh. The fix13e NEW-side pin writes into `agents/ecc-gan-planner.md`, `commands/gan-build.md`, `commands/gan-design.md`, and `README.md` (see §2, B-M2) are still scrubbed by fix33.py's remaining tuples; a build run without fix33.py would reintroduce those pins. This is disclosed in the patch log's DECISION-33-31 ("all still scrubbed by fix33.py") and was known to audit #111-B, which scoped B-M2 to the orch-* lines — so it is not a new finding against this round, but the latent re-pin dependency is narrowed, not eliminated.
- **O-2 — the verifier is static, not execution proof.** §16n asserts presence + line order within files (now routing-aware per bypass, which is the advance over §16m). It cannot prove a skill executes Step 0 or a trigger loads the skill; the re-audit re-traces manually (§1 above). The live test in a real Cursor chat is still owed and can only be done by Anish on Windows.
- **O-3 — the §12 CUT allow-list is still line-number based and fragile to top-of-file insertions** (the B-B6 insertion broke it once already this round; the fix was mechanical re-numbering). Unchanged.
- **O-4 — B-M3 (review-only dispatches) stays unfixed by design**, recorded as OWED-33-5. Outside claimed scope; no code written, no commit, no deploy on those paths.

## Files checked (built tree unless noted)

`skills/orch-change-feature/SKILL.md` (Removing section `:45–51`, full), `skills/orch-build-mvp/SKILL.md` (`:36`, full), `commands/orch-build-mvp.md` (`:29`), `commands/orch-change-feature.md` (`:27`), `commands/feature-dev.md` (`:1–25`), `commands/react-build.md` (`:1–14`), `skills/grill-me/SKILL.md` (staged + built, `:1–30`), `skills/feature-expansion/SKILL.md` (staged + built, `:1–60`, Phase 0/1, allow-listed lines), `skills/orchestrate/SKILL.md` (staged + built, L14/L52/L62/L64/L95), `skills/orch-pipeline/SKILL.md` (Step 0), `manifests/context-packs/skill-triggers@1.json` (48 keys; `:121`/`:160`/`:229`); `build.sh` (fix13-A `:22197–22225`, fix13e `:22690–22710`, all 39 `grok-4.7-high` lines classified old/new by r-string span analysis; opus mapping; assemble references); `fix24/fix24.py` (G-4 hunk, full `git diff`); `fix13/fix13-assemble.py`, `fix13e/fix13e-assemble.py`; `fix33/SPEC.md` (D33-5, D33-22, D33-25…D33-35, §3(c)/(e)/(h), §6 OWED-33-4/33-5), `fix33/MANIFEST.md`, `fix33/fix33-implementation-report.md`, `fix33/fix33.py` (REPLACEMENTS AST count 35, DECISION-33-19/22/31–35, OWED strings), `fix33/verify33.py` (§16c, §16f, §16m, §16n `:3727–3805`, §12 ALLOW_LIST `:2003+`), `fix33/fix33-patch-log.md` (census `:7`, `:71`, `:80–82`), `fix33/build-log-run10.txt`, `fix33/verify33-run33d.txt`, `fix33/scan32-r4-run-fix33d.txt`, `fix33/scan32-r5-run-fix33d.txt`, `fix33/fix-round-33c-report.md` (§1.3 banner), `fix33/fix-round-33d-report.md`, `fix33/audit111-report-A.md`, `fix33/audit111-report-B.md`.

## Exact commands / results

```
cd scratch-repo && git diff --stat | tail -1
  -> 47 files changed, 196 insertions(+), 126 deletions(-)
cd scratch-repo/hackathon-ecc
  grep -n "MODEL" skills/orch-change-feature/SKILL.md   -> 1 (L47 only)
  sed -n '36p' skills/orch-build-mvp/SKILL.md           -> "1. Run orch-pipeline Step 0 first (Classify size — the MODEL check …"
  grep -n "code-explorer" commands/feature-dev.md        -> 19
  grep -n "Factory routing" commands/react-build.md      -> 11
  grep -n "^## Workflow" skills/grill-me/SKILL.md       -> 24
  grep -n "^### Phase 0\|^### Phase 1\|Dispatch four" skills/feature-expansion/SKILL.md -> 45, 55, 57
  grep -c '"skill:' manifests/context-packs/skill-triggers@1.json -> 48
  grep -rn "grok-4.7-high" . | grep -v strategic-compact | wc -l -> 0
  grep -ro "cursor-grok-4.6-high-fast" . | wc -l        -> 72
  grep -rh "^model:" agents/ | sort | uniq -c           -> 41 fast, 4 inherit
grep -c "grok-4.7-high" scratch-repo/build.sh             -> 39
grep -c "The design role runs on model \`grok-4.7-high\`" scratch-repo/build.sh -> 0
cd scratch-repo && git diff -- fix24/fix24.py            -> 1 hunk, 8+/3-, G-4 third sub removed only
grep -n "BUILD EXIT\|fix24:\|fix33:" fix33/build-log-run10.txt
  -> BUILD EXIT: 0; fix24: 113 change(s), OK; fix33: 41 change(s), OK
cd fix33 && python3 verify33.py <built-tree>             -> 586/586 checks pass, EXIT 0
python3 scan32-r4-test-fix33.py <built-tree>             -> RESULT: ALL PASS (76 checks), EXIT 0
# r5 from probe dir with fix32.py + fix32-patch-log.md adjacent
python3 scan32-r5-test-fix33.py <built-tree>             -> RESULT: ALL PASS (100 checks), EXIT 0
# probe copy (full scratch-repo copy under fix33/audit112-probe/, deleted after)
python3 verify33.py <probe>/hackathon-ecc                -> 586/586, EXIT 0 (clean)
# Probe: delete probe skills/orch-change-feature/SKILL.md:47
                                                      -> 584/586, EXIT 1 (exactly 2 §16n B-B1 FAILs)
grep -rn "+135\|+136\|+166" SPEC.md MANIFEST.md fix33-implementation-report.md fix33.py verify33.py -> zero matches
grep -rn "fast 70" SPEC.md MANIFEST.md fix33-implementation-report.md fix33.py verify33.py -> SPEC.md:201 only
md5sum fix33.py / patch-log / fix24.py / 33d report (canonical vs scratch) -> identical in all four pairs
```

Nothing was edited or committed by this audit. The probe copy under `fix33/audit112-probe/` was deleted after the probes; my verifier/scan outputs are at `/tmp/audit112-verify.txt`, `/tmp/audit112-r4.txt`, `/tmp/audit112-r5.txt`, `/tmp/audit112-probe-clean.txt`, `/tmp/audit112-probe-bb1.txt` (ephemeral).

## Recommended rework (small, docs-only, two SPEC lines)

1. `SPEC.md:201`: "fast 70" → "fast 71 pre / 72 post" (A-M1).
2. `SPEC.md:217`: reword "Step 0 (before the size classifier)" to the D33-33 formulation (A-M2).

No tree change, no rebuild, no verifier change is needed. After those two edits, round 33d should pass re-audit.
