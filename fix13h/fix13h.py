#!/usr/bin/env python3
"""Fix round #13h — staged-source edits + preflight of the build patch.

Staged sources edited here (verified staged == built by diff before writing
where the build copies them verbatim; Taste + polish-pass SKILL.md differ from
built only in regions build.sh patches at build time — frontmatter scoping —
so those two are verified by built-tree present-checks after rebuild instead):
- new-skills/orchestrate/SKILL.md (B1 guard, B2 whole-tree snapshot + revert,
  M1 typo, M2 dup ledger sentence, M3 Verify-step numbering, M5 deploy of the
  reverted verified tree, M7 hero-review routing + HTML source input, M8
  resolved-marking + fresh-run scoping, M9 per-redesign-id re-verification)
- new-skills/design-taste-frontend/references/hallmark/references/gates.md
  (M4: Step 6/7 numbers named as the upstream Hallmark walk's own numbering)
- new-skills/design-taste-frontend/SKILL.md (B4: step 4a Impeccable gloss)
- round2-skills/polish-pass/reference/impeccable-craft-floor.md (B4: Refuse
  :34/:35 scoped to candidate evidence; :30 carries the exception clause.
  NOTE: the task cites craft-floor.md for the Refuse items, but the Refuse
  list lives in impeccable-craft-floor.md :28-35 — craft-floor.md has no
  Refuse list. craft-floor.md :111 already routes template bans.)
- round2-skills/polish-pass/reference/polish.md (B4 gloss :39, M11 Harmony)
- round2-skills/polish-pass/SKILL.md (B4 gloss :92, M11 Harmony :96 + harmony
  section; the distinctiveness-bar sentence is NOT touched)
- round2-skills/polish-pass/reference/impeccable-critique.md (M10 score bands)

ECC-base files (no staged source) are NOT edited here. Their edits live in
fix13h/build-patch-h.txt: a build.sh patch block in the fix13g format
(python heredoc, subs + count==1 asserts, plus counted global replaces),
to be inserted LAST, just before STEP 5 (after the fix13g block). Files it
covers: skills/orch-build-mvp/SKILL.md (B2, M1, M2, M6, M7, M8, M9),
commands/gan-build.md (B3 record-first step 0 + Phase 2 generator read list),
commands/gan-design.md (B3 record-first Setup step 0 + intro).
ui-ux-pro-max is NOT touched: it already carries the correct carve-out
("absolute as static/code-level checks ... never a pass/fail verdict").

Two-phase: ALL anchors (staged subs + staged globals + build-patch
old-strings, checked against the CURRENT built tree) are verified BEFORE any
write. On failure the script exits non-zero having written nothing.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")

# Shared wording -----------------------------------------------------------
# Whole-tree snapshot rule (same in both engines).
SNAP_RULE_OLD = (
    "before the design skill overwrites any file, copy every file the redesign"
    " will touch (the redesigned screens' source files, enumerated from the"
    " polish routing / redesign brief) into"
    " `.hackathon/redesign-snapshot/<redesign-id>/` (one directory per redesign;"
    " `<redesign-id>` is the polish finding's short id, e.g. `landing-template`),"
    " preserving relative paths, and record the snapshot path + file list in"
    " `.hackathon/run-ledger.md`."
)
SNAP_RULE_NEW = (
    "before the design skill overwrites any file, copy the WHOLE tree into"
    " `.hackathon/redesign-snapshot/<redesign-id>/` (one directory per redesign;"
    " `<redesign-id>` is the polish finding's short id, e.g. `landing-template`),"
    " preserving relative paths, and record the snapshot path + the full file list"
    " + per-file hashes in `.hackathon/run-ledger.md`. The snapshot covers every"
    " file in the tree, not just the files the redesign brief enumerates — the"
    " brief enumeration is not the snapshot boundary."
)
COVERAGE_OLD = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot file list; any file the redesign touched outside"
    " the enumeration is recorded in `.hackathon/run-ledger.md` as a"
    " snapshot-coverage gap before the fresh verdict runs (restored on revert per"
    " step (2) below, or named as unreverted if no copy exists)."
)
COVERAGE_NEW = (
    "After the build, the orchestrator compares the design skill's changed-file"
    " list against the snapshot manifest; every file the redesign touched is"
    " covered by the whole-tree snapshot, so there is no snapshot-coverage gap by"
    " construction — a file on the changed-file list that is missing from the"
    " manifest is recorded in `.hackathon/run-ledger.md` as a snapshot-integrity"
    " failure before the fresh verdict runs (and the hold stands until the"
    " snapshot is repaired or the redesign is abandoned)."
)
REVERT2_OLD = (
    "confirm the reverted files match the snapshot (re-read or diff) AND diff the"
    " tree against the snapshot directory to catch any file the redesign touched"
    " outside the snapshot enumeration — any such file is restored from version"
    " control if the tree is under it (`git checkout -- <file>` where the file was"
    " committed), otherwise named in the ledger and final report as a"
    " snapshot-coverage gap (the hold stands regardless)"
)
REVERT2_NEW = (
    "confirm the reverted files match the snapshot (re-read or diff) AND delete"
    " every file the redesign created that the snapshot does not contain —"
    " identify created files from the design skill's changed-file list plus the"
    " `git status` untracked listing, or by comparing the post-redesign tree"
    " against the snapshot manifest — then restore modified files from the SNAPSHOT"
    " COPY, never from version control alone (`git checkout` restores HEAD, not"
    " the verified state, and never deletes untracked files; nothing is committed"
    " to restore from in the normal first-build timeline), and verify with"
    " `git status` plus a diff restricted to snapshot-listed paths (each restored"
    " path diffed against its snapshot copy). A file that cannot be restored from"
    " the snapshot is named in the ledger and final report as a snapshot-coverage"
    " gap (the hold stands regardless)"
)
SNAP_INTRO_OLD = (
    "the orchestrator first SNAPSHOTS the screens being redesigned (see the"
    " snapshot rule at the end of this bullet — copy the affected files to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list in"
    " `.hackathon/run-ledger.md`, BEFORE any redesign file is overwritten)"
)
SNAP_INTRO_NEW = (
    "the orchestrator first SNAPSHOTS the whole tree (see the snapshot rule at"
    " the end of this bullet — copy the whole tree to"
    " `.hackathon/redesign-snapshot/<redesign-id>/` and record the file list +"
    " per-file hashes in `.hackathon/run-ledger.md`, BEFORE any redesign file is"
    " overwritten)"
)
REVERT1_OLD = (
    "(1) copy every file in the snapshot back over the tree at its recorded"
    " relative path;"
)
REVERT1_NEW = (
    "(1) copy every file in the snapshot back over the tree at its recorded"
    " relative path (the snapshot is the whole tree, so this restores the verified"
    " state exactly);"
)

# (relative path, old text, new text, label) — staged sources only, count==1.
SUBS = [
# ------------------------------------------------- B1 (orchestrate step 6 guard)
("new-skills/orchestrate/SKILL.md",
 """If that run's final verdict still fails, the template finding stands and routes into the 5b redesign/hold/revert path: it becomes a polish-routed redesign in 5b (snapshot BEFORE the redesign is built, re-verification on the same shared budget, hold + revert to the snapshot on failure).""",
 """If that run's final verdict still fails, the template finding stands and routes into the 5b redesign/hold/revert path: it becomes a polish-routed redesign in 5b (snapshot BEFORE the redesign is built, re-verification on the same shared budget, hold + revert to the snapshot on failure). If the Hallmark audit produces no candidate evidence (no Specificity under 3, no template observations), no fresh round is spent — record that in the ledger (rounds used unchanged).""",
 "B1 orchestrate step 6: no-candidate-evidence guard, mirroring standalone"),
# ------------------------------------------------- B2 (orchestrate snapshot intro)
("new-skills/orchestrate/SKILL.md", SNAP_INTRO_OLD, SNAP_INTRO_NEW,
 "B2 orchestrate 5b: snapshot is the whole tree"),
# ------------------------------------------------- B2 (orchestrate snapshot rule)
("new-skills/orchestrate/SKILL.md", SNAP_RULE_OLD, SNAP_RULE_NEW,
 "B2 orchestrate 5b: whole-tree snapshot + file list + hashes"),
# ------------------------------------------------- B2 (orchestrate coverage check)
("new-skills/orchestrate/SKILL.md", COVERAGE_OLD, COVERAGE_NEW,
 "B2 orchestrate 5b: changed-file list checked against the snapshot manifest"),
# ------------------------------------------------- B2 (orchestrate revert step 1)
("new-skills/orchestrate/SKILL.md", REVERT1_OLD, REVERT1_NEW,
 "B2 orchestrate 5b: revert (1) whole-tree restore restores verified state"),
# ------------------------------------------------- B2 (orchestrate revert step 2)
("new-skills/orchestrate/SKILL.md", REVERT2_OLD, REVERT2_NEW,
 "B2 orchestrate 5b: revert (2) delete created files, restore from snapshot copy, never git alone"),
# ------------------------------------------------- M1 (orchestrate typo)
("new-skills/orchestrate/SKILL.md",
 "working-context memory.; the redesign decision follows",
 "working-context memory; the redesign decision follows",
 "M1 orchestrate 5b: stray period removed"),
# ------------------------------------------------- M2 (orchestrate dup ledger sentence)
("new-skills/orchestrate/SKILL.md",
 """ the redesign decision follows `browser-qa`'s verdict. After the run, the orchestrator records `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` (see the round definition above) and consults that line before spending more.""",
 """ the redesign decision follows `browser-qa`'s verdict.""",
 "M2 orchestrate 5b: duplicated ledger-update sentence removed (round definition is the single source)"),
# ------------------------------------------------- M3 (orchestrate Verification headers)
("new-skills/orchestrate/SKILL.md",
 "1. **Cheaply verifiable**",
 "Verify step 1. **Cheaply verifiable**",
 "M3 orchestrate Verification item 1 renamed"),
("new-skills/orchestrate/SKILL.md",
 "2. **Not cheaply verifiable**",
 "Verify step 2. **Not cheaply verifiable**",
 "M3 orchestrate Verification item 2 renamed"),
("new-skills/orchestrate/SKILL.md",
 "3. **Large (≈>20 files)",
 "Verify step 3. **Large (≈>20 files)",
 "M3 orchestrate Verification item 3 renamed"),
("new-skills/orchestrate/SKILL.md",
 "4. **Any diff that touches a UI surface",
 "Verify step 4. **Any diff that touches a UI surface",
 "M3 orchestrate Verification item 4 (UI diff) renamed"),
("new-skills/orchestrate/SKILL.md",
 "**4. Adversarial audit",
 "**Verify step 4. Adversarial audit",
 "M3 orchestrate Verification item 4 (adversarial audit) renamed — second 4 in the existing numbering, preserved as-is"),
("new-skills/orchestrate/SKILL.md",
 "**5. Visual iteration loop",
 "**Verify step 5. Visual iteration loop",
 "M3 orchestrate Verification item 5 renamed"),
("new-skills/orchestrate/SKILL.md",
 "**6. Hallmark audit",
 "**Verify step 6. Hallmark audit",
 "M3 orchestrate Verification item 6 renamed"),
# ------------------------------------------------- M5 (orchestrate 5c deploy reverted tree)
("new-skills/orchestrate/SKILL.md",
 """the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). The 5d demo""",
 """the deploy of the redesign is HELD: do not deploy the redesigned build, record `re-verification: BLOCKED` in `.hackathon/run-ledger.md` and the final report, and do not proceed to deploy the redesign in this run (this is a safety hold, not a user question — it never asks the user anything). The hold blocks only the redesign: deploy the reverted verified tree and record its URL and deploy path in `.hackathon/run-ledger.md`; only the deploy of the held redesign is forbidden. The 5d demo""",
 "M5 orchestrate 5c: deploy the reverted verified tree, mirroring standalone step 8"),
# ------------------------------------------------- M7a (orchestrate hero-review routing)
("new-skills/orchestrate/SKILL.md",
 "passing `.hallmark/hero-review.md` to the browser-qa visual loop as an input file",
 "passing `.hallmark/hero-review.md` to the fresh-verdict run as an input file (via `.hallmark/candidate-evidence.md`)",
 "M7a orchestrate step 6: hero-review routes to the fresh-verdict run, not the already-run visual loop"),
# ------------------------------------------------- M7b (orchestrate finish-review inputs)
("new-skills/orchestrate/SKILL.md",
 "pass the render-tier screenshots, the stamp theme/idea line, the theme file, and the hero review's findings",
 "pass the render-tier screenshots, the page's HTML or component source, the stamp theme/idea line, the theme file, and the hero review's findings",
 "M7b orchestrate step 6: finish-review input list gains the HTML/component source"),
# ------------------------------------------------- M8a (orchestrate visual-loop resolved marking)
("new-skills/orchestrate/SKILL.md",
 "Evidence never overrides your verdict — you make the call.",
 "Evidence never overrides your verdict — you make the call. Entries the visual loop fixes are marked resolved in `.hallmark/candidate-evidence.md` (`Resolved in visual loop — do not re-judge`, with the screen + fix), so the Verify-step-6 fresh run does not spend a round re-judging already-fixed screens.",
 "M8a orchestrate Verify step 5: fixed entries marked resolved in candidate evidence"),
# ------------------------------------------------- M8b (orchestrate fresh-run scoping)
("new-skills/orchestrate/SKILL.md",
 "before polish/deploy, and only `browser-qa`'s verdict decides whether a fix is owed.",
 "before polish/deploy, and only `browser-qa`'s verdict decides whether a fix is owed. The run is scoped to unresolved candidate evidence about the affected screens (entries marked `Resolved in visual loop — do not re-judge` are not re-judged).",
 "M8b orchestrate step 6: fresh run scoped to unresolved evidence"),
# ------------------------------------------------- M4 (gates.md staged-scope note)
("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
 """In this plugin's staged flow: §1–§3 drive the pre-emit pass (gates.md §3), §4 the build, §5 the Finish checks and the judged clauses at the finish review, §6 the two reviews (hero + finish).""",
 """In this plugin's staged flow: §1–§3 drive the pre-emit pass (gates.md §3), §4 the build, §5 the Finish checks and the judged clauses at the finish review, §6 the two reviews (hero + finish). The 'Step 6' (hero review) and 'Step 7' (finish review) numbers in §6 are the upstream Hallmark build/review walk's own numbering, not steps in this plugin.""",
 "M4 gates.md: §6 Step 6/7 numbers named as the upstream walk's numbering"),
# ------------------------------------------------- B4 (impeccable-craft-floor :30 exception)
("round2-skills/polish-pass/reference/impeccable-craft-floor.md",
 "recognizing that means rewriting the element, not softening it.",
 "recognizing that means rewriting the element, not softening it — except the two page-level template patterns below (same-size cards as the page structure; the hero-metric template), which are candidate evidence for `browser-qa`, never a rewrite on this check alone (see craft-floor.md).",
 "B4 impeccable-craft-floor :30: template-pattern exception to the rewrite compulsion (:30 is the general preamble, not itself a template pattern)"),
# ------------------------------------------------- B4 (impeccable-craft-floor :34)
("round2-skills/polish-pass/reference/impeccable-craft-floor.md",
 "- Same-size cards of icon plus heading plus text as the page structure. Cards are the lazy container; nested cards are always wrong.",
 "- Same-size cards of icon plus heading plus text as the page structure. Cards are the lazy container; nested cards are always wrong. As a page-level template pattern this is candidate evidence for `browser-qa` — append it (screen + pattern) to `.hallmark/candidate-evidence.md`; do not rewrite on this check alone.",
 "B4 impeccable-craft-floor :34: same-size-cards pattern to candidate evidence"),
# ------------------------------------------------- B4 (impeccable-craft-floor :35)
("round2-skills/polish-pass/reference/impeccable-craft-floor.md",
 "- The hero-metric template: big number, small label, supporting stats, accent.",
 "- The hero-metric template: big number, small label, supporting stats, accent. As a page-level template pattern this is candidate evidence for `browser-qa` — append it (screen + pattern) to `.hallmark/candidate-evidence.md`; do not rewrite on this check alone.",
 "B4 impeccable-craft-floor :35: hero-metric template to candidate evidence"),
# ------------------------------------------------- B4 (polish.md :39 gloss)
("round2-skills/polish-pass/reference/polish.md",
 "its bans are absolute; where the two floors disagree, the stricter ban wins.",
 "its bans are absolute as static/code-level checks — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone); where the two floors disagree, the stricter ban wins — except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite decided here.",
 "B4 polish.md:39: absolute-bans gloss corrected"),
# ------------------------------------------------- M11 (polish.md Step 7 record)
("round2-skills/polish-pass/reference/polish.md",
 "then check each primary screen for consistency of tokens/type/color/spacing against that direction. Record per-screen pass/fail for the report.",
 "then check each primary screen for consistency of tokens/type/color/spacing against that direction. Record per-screen consistency (consistent / diverges, with the tokens cited) for the report.",
 "M11 polish.md Step 7: Harmony record is consistency, not pass/fail"),
# ------------------------------------------------- M11 (polish.md Harmony table)
("round2-skills/polish-pass/reference/polish.md",
 "| <screen> | <consistent / inconsistent + evidence> | <pass/fail on consistency only> |",
 "| <screen> | <consistent / inconsistent + evidence> | <consistent / diverges (tokens cited)> |",
 "M11 polish.md Harmony table: Result column is consistency, not pass/fail"),
# ------------------------------------------------- B4 (polish-pass SKILL.md :92 gloss)
("round2-skills/polish-pass/SKILL.md",
 "its bans are absolute (a pinned brief never overrides a ban); where the two floors disagree, the stricter ban wins.",
 "its bans are absolute as static/code-level checks (a pinned brief never overrides a ban) — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone); where the two floors disagree, the stricter ban wins — except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite decided here.",
 "B4 polish-pass SKILL.md:92: absolute-bans gloss corrected"),
# ------------------------------------------------- M11 (polish-pass SKILL.md harmony section)
("round2-skills/polish-pass/SKILL.md",
 """and record per-screen pass/fail in the report under "Harmony check".""",
 """and record per-screen consistency (consistent / diverges, with the tokens cited) in the report under "Harmony check".""",
 "M11 polish-pass SKILL.md harmony section: Harmony record is consistency, not pass/fail"),
# ------------------------------------------------- M11 (polish-pass SKILL.md :96)
("round2-skills/polish-pass/SKILL.md",
 "check each primary screen for consistency only, and record per-screen pass/fail in the report.",
 "check each primary screen for consistency only, and record per-screen consistency (consistent / diverges, with the tokens cited) in the report.",
 "M11 polish-pass SKILL.md:96: Harmony record is consistency, not pass/fail"),
# ------------------------------------------------- B4 (Taste step 4a gloss)
("new-skills/design-taste-frontend/SKILL.md",
 """its bans are absolute — a pinned brief never overrides a ban — and where it and this skill disagree, the stricter ban wins — except that on a landing page Hallmark gate 2b's guarded single-hue gradient-text ramp is permitted (gates.md §4 governs there; the polish detector's gradient-text tell does not apply to it).""",
 """its bans are absolute as static/code-level checks — a pinned brief never overrides a ban — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone) — and where it and this skill disagree, the stricter ban wins — except that on a landing page Hallmark gate 2b's guarded single-hue gradient-text ramp is permitted (gates.md §4 governs there; the polish detector's gradient-text tell does not apply to it), and except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite on this check alone.""",
 "B4 design-taste-frontend step 4a: absolute-bans gloss corrected, gate 2b exception preserved"),
# ------------------------------------------------- M10 (critique bands)
("round2-skills/polish-pass/reference/impeccable-critique.md",
 "| 36–40 | Excellent | Minor polish only; ship it |",
 "| 36–40 | Excellent | Minor polish only; informs candidate evidence, never a ship verdict |",
 "M10 critique: Excellent band is evidence language, not a ship verdict"),
("round2-skills/polish-pass/reference/impeccable-critique.md",
 "| 12–19 | Poor | Major UX overhaul required; core experience broken |",
 "| 12–19 | Poor | Major UX issues; core experience broken — record as candidate evidence for `browser-qa` |",
 "M10 critique: Poor band is evidence language, not an overhaul verdict"),
("round2-skills/polish-pass/reference/impeccable-critique.md",
 "| 0–11 | Critical | Redesign needed; unusable in current state |",
 "| 0–11 | Critical | Redesign indicated, not decided; unusable in current state — record as candidate evidence for `browser-qa` |",
 "M10 critique: Critical band is evidence language, not a redesign verdict"),
("round2-skills/polish-pass/reference/impeccable-critique.md",
 "When heuristics were scored `n/a`, the maximum is lower than 40;",
 "The bands inform candidate evidence for `browser-qa`; only `browser-qa`'s verdict establishes a finding.\n\nWhen heuristics were scored `n/a`, the maximum is lower than 40;",
 "M10 critique: bands framed as candidate evidence under the table"),
]

# (relative path, old text, new text, expected count, label) — staged globals.
GSUBS = [
# ------------------------------------------------- M3 (orchestrate Verification refs)
("new-skills/orchestrate/SKILL.md",
 "2 rounds total across 5b and step 6", "2 rounds total across 5b and Verify step 6", 2,
 "M3 orchestrate: shared-budget refs are Verify step 6"),
("new-skills/orchestrate/SKILL.md",
 "rounds the step-6 finish-review re-inspection consumes", "rounds the Verify-step-6 finish-review re-inspection consumes", 1,
 "M3 orchestrate: budget refs are Verify step 6"),
("new-skills/orchestrate/SKILL.md",
 "the 5c/step-6 checks below consult that ledger entry, not working-context memory.",
 "the 5c/Verify-step-6 checks below consult the entry for that redesign-id (`re-verification <redesign-id>: PASSED/BLOCKED`), not working-context memory.", 1,
 "M3+M9 orchestrate: 5c/Verify-step-6 checks consult the per-redesign-id entry"),
("new-skills/orchestrate/SKILL.md",
 "step-6 finish-review template observations", "Verify-step-6 finish-review template observations", 1,
 "M3 orchestrate: template-observation refs are Verify step 6"),
("new-skills/orchestrate/SKILL.md",
 "step-6 template observations", "Verify-step-6 template observations", 1,
 "M3 orchestrate: template-observation refs are Verify step 6 (short form)"),
("new-skills/orchestrate/SKILL.md",
 "browser-qa's step-5 captures", "browser-qa's Verify-step-5 captures", 1,
 "M3 orchestrate: captures refs are Verify step 5"),
("new-skills/orchestrate/SKILL.md",
 "the step-5 visual loop (`browser-qa`, the sole executor)", "the Verify-step-5 visual loop (`browser-qa`, the sole executor)", 1,
 "M3 orchestrate: visual-loop refs are Verify step 5"),
("new-skills/orchestrate/SKILL.md",
 "happens in the step-5 visual loop (`browser-qa`, sole executor)", "happens in the Verify-step-5 visual loop (`browser-qa`, sole executor)", 1,
 "M3 orchestrate: visual-loop refs are Verify step 5"),
("new-skills/orchestrate/SKILL.md",
 "(the enumerated screens from step 5)", "(the enumerated screens from Verify step 5)", 1,
 "M3 orchestrate: enumerated-screens refs are Verify step 5"),
("new-skills/orchestrate/SKILL.md",
 "this app-screen audit IS the step-6 design audit", "this app-screen audit IS the Verify-step-6 design audit", 1,
 "M3 orchestrate: design-audit refs are Verify step 6"),
("new-skills/orchestrate/SKILL.md",
 "(step 5 below)", "(Verify step 5 below)", 1,
 "M3 orchestrate: cross-ref is Verify step 5"),
("new-skills/orchestrate/SKILL.md",
 "the step-5 visual loop's consumed caps", "the Verify-step-5 visual loop's consumed caps", 1,
 "M3 orchestrate: budget refs are Verify step 5"),
# ------------------------------------------------- M9 (orchestrate per-redesign-id)
("new-skills/orchestrate/SKILL.md",
 "`re-verification: PASSED`", "`re-verification <redesign-id>: PASSED`", 2,
 "M9 orchestrate: PASSED entries keyed per redesign-id"),
("new-skills/orchestrate/SKILL.md",
 "`re-verification: BLOCKED`", "`re-verification <redesign-id>: BLOCKED`", 6,
 "M9 orchestrate: BLOCKED entries keyed per redesign-id"),
]

# Old-strings from build-patch-h.txt, verified count==1 against the CURRENT
# built tree (preflight only — this script does not apply them).
PATCH_ANCHORS = [
 ("skills/orch-build-mvp/SKILL.md", SNAP_INTRO_OLD),
 ("skills/orch-build-mvp/SKILL.md", SNAP_RULE_OLD),
 ("skills/orch-build-mvp/SKILL.md", COVERAGE_OLD),
 ("skills/orch-build-mvp/SKILL.md", REVERT1_OLD),
 ("skills/orch-build-mvp/SKILL.md", REVERT2_OLD),
 ("skills/orch-build-mvp/SKILL.md",
  "working-context memory.; the redesign decision follows"),
 ("skills/orch-build-mvp/SKILL.md",
  """ the redesign decision follows `browser-qa`'s verdict. After the run, the orchestrator records `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` (see the round definition above) and consults that line before spending more."""),
 ("skills/orch-build-mvp/SKILL.md",
  "Then, on a build with a landing page, first run sloplint on the landing page:"),
 ("skills/orch-build-mvp/SKILL.md",
  "passing `.hallmark/hero-review.md` to the browser-qa visual loop as an input file"),
 ("skills/orch-build-mvp/SKILL.md",
  "passing the render-tier screenshots, the stamp theme/idea line, the theme file, and the hero review's findings (`.hallmark/hero-review.md`, written by the landing slice) as file paths"),
 ("skills/orch-build-mvp/SKILL.md",
  "fix and re-inspect within the same caps as orchestrate (max 3 rounds total, at most 2 fix rounds per problem list; if the app cannot run, record that as blocked with evidence instead of iterating)."),
 ("skills/orch-build-mvp/SKILL.md",
  "the run is scoped to the candidate evidence about the affected screens (entries a redesign supersedes are marked `Superseded` — see 6b)."),
 ("skills/orch-build-mvp/SKILL.md",
  "the step-7/step-8 checks below consult that ledger entry, not working-context memory."),
 ("commands/gan-build.md",
  "0. Design-direction check (cold start) — BEFORE launching the planner, check whether `docs/design-tokens.md` carries a direction recorded by the design-lead (model `grok-4.7-high`)."),
 ("commands/gan-build.md",
  "If it does, pass it to the planner as in step 1; if it does not (cold start — no direction recorded yet), INVOKE the design-lead (model `grok-4.7-high`) first to generate the direction through the package skills (`design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface, per the design-package rule) and record it in `docs/design-tokens.md`, then launch the planner with that recorded direction."),
 ("commands/gan-build.md",
  "step 0 is the cold-start path: the design-lead generates the direction first and records it in `docs/design-tokens.md` — the first UI slice then writes its tokens FROM that recorded direction, never inventing one."),
 ("commands/gan-build.md",
  "plus the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` (step 0 records it first on a cold start) — the direction comes from the design-lead BEFORE the loop;"),
 ("commands/gan-build.md",
  "    - Read spec.md\n    - If iteration > 1: read feedback/feedback-{iteration-1}.md"),
 ("commands/gan-design.md",
  "0. Design-direction check (cold start) — BEFORE writing the spec or rubric, check whether `docs/design-tokens.md` carries a direction recorded by the design-lead (model `grok-4.7-high`)."),
 ("commands/gan-design.md",
  "If it does, proceed as below; if it does not (cold start — no direction recorded yet), INVOKE the design-lead (model `grok-4.7-high`) first to generate the direction through the package skills (`design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface, per the design-package rule) and record it in `docs/design-tokens.md`, then restate that recorded direction in the brief/spec and proceed."),
 ("commands/gan-design.md",
  "the brief IS the spec, and the brief RESTATES the design direction recorded by the design-lead (model `grok-4.7-high`) in `docs/design-tokens.md` (Setup step 0 records it first on a cold start) — the direction lives in the file, never in the brief alone"),
]

# (relative path, old text, expected count) — build-patch globals in the
# built tree (preflight only).
PATCH_GLOBALS = [
 ("skills/orch-build-mvp/SKILL.md", "`re-verification: PASSED`", 3),
 ("skills/orch-build-mvp/SKILL.md", "`re-verification: BLOCKED`", 7),
]


def main():
    # Phase 1 — verify every staged anchor count==1 (preflight, no writes).
    failures = []
    for rel, old, _new, label in SUBS:
        txt = open(os.path.join(PLUGIN_ROOT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != 1:
            failures.append(f"STAGED {label}: count={n}")
    for rel, old, _new, want, label in GSUBS:
        txt = open(os.path.join(PLUGIN_ROOT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != want:
            failures.append(f"STAGED-GLOBAL {label}: count={n} want={want}")
    # Phase 1b — verify every build-patch anchor count==1 in the built tree.
    for rel, old in PATCH_ANCHORS:
        txt = open(os.path.join(BUILT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != 1:
            failures.append(f"PATCH-ANCHOR {rel}: count={n} :: {old[:70]!r}")
    for rel, old, want in PATCH_GLOBALS:
        txt = open(os.path.join(BUILT, rel), encoding="utf-8").read()
        n = txt.count(old)
        if n != want:
            failures.append(f"PATCH-GLOBAL {rel}: count={n} want={want} :: {old[:50]!r}")
    if failures:
        print("PREFLIGHT FAILED — wrote nothing:")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print(f"Preflight OK: {len(SUBS)} staged subs + {len(GSUBS)} staged globals + "
          f"{len(PATCH_ANCHORS)} patch anchors + {len(PATCH_GLOBALS)} patch globals, all as expected.")

    # Phase 2 — apply staged subs.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        txt = open(p, encoding="utf-8").read()
        assert txt.count(old) == 1, label
        open(p, "w", encoding="utf-8").write(txt.replace(old, new))
        print(f"  applied: {label}")
    # Phase 3 — apply staged globals (assert expected count at apply time).
    for rel, old, new, want, label in GSUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        txt = open(p, encoding="utf-8").read()
        assert txt.count(old) == want, label
        open(p, "w", encoding="utf-8").write(txt.replace(old, new))
        print(f"  applied (x{want}): {label}")
    print(f"Wrote {len(SUBS)} staged subs + {len(GSUBS)} staged globals. Built tree untouched; build.sh untouched.")


if __name__ == "__main__":
    main()
