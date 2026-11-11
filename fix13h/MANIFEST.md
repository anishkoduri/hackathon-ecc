# Fix round #13h — MANIFEST

## Build
- build.sh: 23,058 lines (was 22,932), md5 `d2b1b856d7b5bef96da11d3bb1f36144`
- Built tree manifest (two clean builds): `143e5ee3c1f43a60a61a10864a1a345e`, diff = 0
- Counts: 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- Build 1 + build 2: exit 0, "fix13h upstream block applied"

## Method
- `fix13h/fix13h.py`: 35 staged subs + 14 staged globals (orchestrate, gates.md,
  Taste step 4a, impeccable-craft-floor, polish.md, polish-pass SKILL.md,
  impeccable-critique) + preflight of 21 build-patch anchors + 2 build-patch
  globals against the post-fix13g built tree — all as expected before any
  write. (Preflight first failed on one count — "step-6 finish-review template
  observations" is 1 hit, the second occurrence is the short form "step-6
  template observations" — the expectation was corrected to 1+1 and the
  preflight then passed clean; nothing was written before the pass.)
- `fix13h/build-patch-h.txt`: build.sh block inserted LAST, just before STEP 5
  (after the fix13g block). 21 subs + 2 counted globals.
- `fix13h/verify13h.py`: 97 present/gone checks against the BUILT tree — all
  pass.
- Staged == built verified by diff for 5 staged files (orchestrate, gates.md,
  impeccable-craft-floor.md, polish.md, impeccable-critique.md). Taste
  SKILL.md and polish-pass SKILL.md differ from built only in the pre-existing
  build-time regions (frontmatter scoping; 11 and 8 changed lines, same regions
  as before fix13h); every edited line in those two files is identical staged
  vs built (Taste 4a staged:241 = built:242; polish-pass SKILL.md :92, :96,
  harmony line 22 identical).

## Scope (4 blocking + 11 minor, all implemented)

### BLOCKING
1. **B1 — orchestrate step-6 no-candidate-evidence guard**
   (`skills/orchestrate/SKILL.md:195`): the step-6 fresh-verdict paragraph now
   ends "If the Hallmark audit produces no candidate evidence (no Specificity
   under 3, no template observations), no fresh round is spent — record that in
   the ledger (rounds used unchanged)." — same wording as standalone
   (`skills/orch-build-mvp/SKILL.md:49`).
2. **B2 — whole-tree snapshot + revert that restores residue (both engines)**
   (`skills/orchestrate/SKILL.md:60`, `skills/orch-build-mvp/SKILL.md:53`):
   snapshot intro is now "SNAPSHOTS the whole tree"; the snapshot rule copies
   the WHOLE tree into `.hackathon/redesign-snapshot/<redesign-id>/` and records
   the full file list + per-file hashes (the brief enumeration is not the
   snapshot boundary); the post-build check compares the changed-file list
   against the snapshot manifest (no coverage gap by construction; a manifest
   miss is a snapshot-integrity failure); revert (1) copies the whole-tree
   snapshot back (restores the verified state exactly); revert (2) deletes
   every file the redesign created that the snapshot does not contain
   (changed-file list + `git status` untracked listing, or tree-vs-manifest
   comparison), restores modified files from the SNAPSHOT COPY — never from
   version control alone (`git checkout` restores HEAD, not the verified state,
   and never deletes untracked files; nothing is committed to restore from in
   the normal first-build timeline) — and verifies with `git status` plus a
   diff restricted to snapshot-listed paths. Gone in both files:
   "copy every file the redesign will touch", `git checkout -- <file>`,
   "diff the tree against the snapshot directory".
3. **B3 — cold-start direction chain (record first)**
   (`commands/gan-build.md:24` step 0, `:23` always-path, `:25` step 1, `:37`
   Phase 2 generator; `commands/gan-design.md:17` Setup step 0, `:12` intro):
   step 0 reads `docs/decision-record.md` FIRST and adopts its recorded
   direction when one exists (writing it into `docs/design-tokens.md` if the
   tokens file lacks it or differs); the design-lead is invoked only when
   neither the record nor the tokens file carries a direction. Precedence
   stated in both commands: the decision record wins over spec.md (spec.md is
   derived from the record/scope, so a divergence means the translation
   drifted; the record is authoritative), and the tokens file carries the
   record's direction. Phase 2 generator read list is now "Read spec.md and
   `docs/design-tokens.md`" with the same precedence rule. Taste and
   ui-ux-pro-max have no direction-adoption lines that read the record
   (0 hits for `decision-record` in both) — nothing to change there.
4. **B4 — Impeccable Refuse template patterns to candidate evidence**
   - `skills/polish-pass/reference/impeccable-craft-floor.md:30` carries the
     exception clause (the two page-level template patterns are candidate
     evidence, never a rewrite on this check alone); `:34` same-size-cards and
     `:35` hero-metric template each append to `.hallmark/candidate-evidence.md`
     and are not rewritten on this check alone. (:30 is the general preamble,
     not itself a template pattern — scoped via the exception, not rewritten
     as a template item. :36 kicker/eyebrow is explicitly "a ban, not a
     default" — left alone.)
   - Gloss corrected in `skills/polish-pass/reference/polish.md:39`,
     `skills/polish-pass/SKILL.md:92`, and
     `skills/design-taste-frontend/SKILL.md:242` (step 4a): bans are absolute
     as static/code-level checks — design guidance / static-check evidence,
     never a pass/fail verdict on a rendered screen — with the template-pattern
     exception; Taste keeps its Hallmark gate 2b exception.
   - `skills/ui-ux-pro-max/SKILL.md:87` verified intact and NOT touched (it
     already carries the correct carve-out).

### MINOR
- **M1** (orchestrate `:60`, orch-build-mvp `:53`): "working-context memory.;"
  → "working-context memory;" in both. "memory.;" now 0 hits in both files.
- **M2** (orchestrate `:60`, orch-build-mvp `:53`): the duplicated "After the
  run, the orchestrator records…" sentence removed in both 5b/6b; the round
  definition is the single source. (See Held back: the same sentence remains
  in the step-6 fresh-run paragraphs.)
- **M3** (orchestrate `:183–195`): Verification-stage items renamed "Verify
  step 1" … "Verify step 6" (`:183`, `:184`, `:185`, `:187`, `:191`, `:193`,
  `:195`) and every in-text Verification reference renamed consistently
  ("across 5b and Verify step 6" ×2, "Verify-step-6 finish-review…" ×2,
  "browser-qa's Verify-step-5 captures", "Verify-step-5 visual loop" ×3,
  "Verify-step-6 design audit", "Verify step 5 below", "Verify-step-5 …
  consumed caps"). Orchestrate's own steps untouched: "6. Commit, README,
  then final report" (`:64`), "the step-6 README/final report" (`:61`),
  "per orchestrate step 5 above" (`:279`), "see design-taste-frontend step 6"
  (`:195`, Taste's own step).
- **M4** (`gates.md:3` staged-scope note): §6 Step 6 (hero review) / Step 7
  (finish review) numbers named as the upstream Hallmark build/review walk's
  own numbering, not steps in this plugin.
- **M5** (orchestrate `:61` 5c): "The hold blocks only the redesign: deploy
  the reverted verified tree and record its URL and deploy path in
  `.hackathon/run-ledger.md`; only the deploy of the held redesign is
  forbidden." — mirroring standalone step 8 (`orch-build-mvp:56`).
- **M6** (orch-build-mvp `:49`): "first run sloplint on the landing page" →
  "run sloplint on the landing page before the Hallmark landing audit".
- **M7** (orchestrate `:195`, orch-build-mvp `:49`): (a) the render-absent
  fallback now passes `.hallmark/hero-review.md` to the fresh-verdict run
  (via `.hallmark/candidate-evidence.md`), not the already-run visual loop;
  (b) both finish-review input lists gain "the page's HTML or component
  source" (the input `review-finish.md:3` names).
- **M8** (orchestrate `:193` + `:195`, orch-build-mvp `:49`): entries the
  visual loop fixes are marked `Resolved in visual loop — do not re-judge`
  (screen + fix) in `.hallmark/candidate-evidence.md`, and both fresh runs
  are scoped to unresolved candidate evidence (orchestrate `:195` "scoped to
  unresolved candidate evidence"; standalone `:49` "scoped to the unresolved
  candidate evidence").
- **M9** (orchestrate `:60`, `:61`, `:64`; orch-build-mvp `:53`, `:55`, `:56`):
  every `re-verification: PASSED/BLOCKED` entry is now keyed per redesign-id
  (`re-verification <redesign-id>: PASSED/BLOCKED`) — orchestrate 2 PASSED +
  6 BLOCKED, standalone 3 PASSED + 7 BLOCKED; plain entries 0 hits in both
  files. The 5c/Verify-step-6 and step-7/step-8 checks consult the entry for
  that redesign-id.
- **M10** (`impeccable-critique.md:595`, `:598`, `:599`, `:601`): Excellent
  "Minor polish only; informs candidate evidence, never a ship verdict";
  Poor "Major UX issues; … — record as candidate evidence for `browser-qa`";
  Critical "Redesign indicated, not decided; … — record as candidate
  evidence for `browser-qa`"; plus "The bands inform candidate evidence for
  `browser-qa`; only `browser-qa`'s verdict establishes a finding." under the
  table. "ship it" / "Redesign needed" / "Major UX overhaul required" now
  0 hits in the file; the bands appear nowhere else in the file.
- **M11** (polish-pass `SKILL.md:22` harmony section + `:96`, `polish.md:24`
  Step 7 + `:79` table): Harmony records per-screen consistency
  ("consistent / diverges, with the tokens cited"; table column
  "<consistent / diverges (tokens cited)>"), not pass/fail. The
  distinctiveness-bar sentences ("pass/fail verdicts on rendered screens,
  executed by `browser-qa` ONLY") are untouched in both files.

## Held back (with reasons)
- **M2 scope**: the duplicated ledger-update sentence was removed only in 5b
  (`:60`) and 6b (`:53`), as specified. The same sentence still appears once
  in each engine's step-6 fresh-run paragraph (orchestrate `:195` "(see the
  round definition in 5b)", standalone `:49` "— see the round definition in
  6b —"). Same duplication pattern, left for a follow-up decision rather than
  expanding the specified scope.
- **B4 file citation**: the task cites `craft-floor.md` for the Refuse items
  (`:30`, `:34`, `:35`), but that file has no Refuse list — the Refuse list
  lives in `impeccable-craft-floor.md:28–35`. Fixed there (staged source
  exists and flows into the build); `craft-floor.md` itself needed no change
  (its `:111` already routes template-pattern bans to candidate evidence).
- **B3 scope**: `orch-build-mvp` step 4 (`:38–39`, where spec.md is translated
  from the record/scope) was not touched — it is not in the task's file list;
  the precedence rule lives in gan-build step 0 + Phase 2 generator and
  gan-design, which is where the record is read and where the generator reads.
- **M3 numbering**: the Verification stage has TWO items numbered 4
  (orchestrate `:187` UI-diff item and `:191` adversarial audit) — both
  renamed "Verify step 4" as-is. Renumbering was out of scope and would have
  broken the task's own "Verify step 5 / Verify step 6" example.
- **ui-ux-pro-max**: not touched, per the task — its `:87` carve-out was
  verified correct and left intact.

## Bounds kept
No new gates/waits/questions; no new skills/agents/rules/commands; deferred-six
carve-out, Grok 4.7 High pin + picker instruction, anti-derivative rule,
"more, not bolder" posture, CBM phrasing untouched; direction lenses /
live-generate stay out; frontend-slides stays on-demand; pins + SSML truth
held; no fix11 re-run; no pip pinning; no repo/bundle touching. GATE patch
inserted after fix13g, still before STEP 5.

## Checks (to be filled by Audit #49 / dry-run #21 / sweep)
- Audit #49: (pending)
- Dry-run #21: (pending)
- Single-executor sweep: (pending)
