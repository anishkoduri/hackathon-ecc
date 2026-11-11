# Fix round #13i — MANIFEST

## Build
- build.sh: 23,117 lines (was 23,058), md5 `cb12ab81c3334dba68054ba18c1d4f15`
- Built tree manifest (two clean builds): `eecb5315311c70d9675951db4b37ff7f`, diff = 0
- Counts: 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- Build 1 + build 2: exit 0, "fix13i upstream block applied"

## Method
- `fix13i/fix13i.py`: 23 staged subs + preflight of 9 build-patch anchors — all
  count==1 against the post-fix13h built tree before any write. (One script bug
  found and fixed before the run: `STAGED` shadowed as both the subs list and
  the root path; renamed the root to `PLUGIN_ROOT`. No writes happened before
  the preflight passed.)
- `fix13i/build-patch-i.txt`: build.sh block inserted LAST, just before STEP 5
  (after the fix13h block). 9 subs, all count==1 asserts.
- `fix13i/verify13i.py`: 63 present/gone checks against the BUILT tree — all
  pass.
- Staged == built verified by diff for 5 staged files (orchestrate, polish.md,
  gates.md, review-finish.md, review-hero.md). Taste SKILL.md differs from
  built only in the pre-existing build-time frontmatter region (lines 9–14,
  same region as before fix13h); the edited :314 line is identical staged vs
  built (verified by the present-checks).

## Scope (1 blocking + 11 minor, all implemented)

### BLOCKING
1. **B1 — whole-tree snapshot excludes live run state; revert never restores
   it** (orchestrate `:60`, standalone `:53`): the snapshot copy now excludes
   `.hackathon/` AND `.hallmark/candidate-evidence.md`; the snapshot rule
   states both reasons (self-referential copy; live run state, not tree
   state); revert (1) never overwrites the live ledger or candidate-evidence
   file, so the `fresh-verdict rounds used: N/2` line and the `Superseded by
   redesign` markings survive a revert as written; revert (3) records that the
   spent round stays spent; the coverage check exempts the two excluded paths
   (never in the manifest by design, never a coverage failure); revert (2)
   never deletes the excluded run-state paths.

### MINOR
- **Audit M1** (`polish.md:18,19,39,40`): the five `reference/…` links now
  drop the prefix (`[impeccable-detector-rules.json](…)`,
  `[impeccable-critique.md](…)`, `[impeccable-craft-floor.md](…)`,
  `[impeccable-onboard.md](…)`, `[impeccable-extract.md](…)`).
  `polish-pass/SKILL.md:92` keeps its `reference/` prefix (correct there —
  verified present).
- **DR-M1** (orchestrate `:60`): "the 5c/Verify-step-6 checks below" →
  "the 5c and step-6 checks below".
- **DR-M2** (orchestrate `:187`, `:191`): the two "Verify step 4" items are
  now "Verify step 4a" (blind UI reviewer) and "Verify step 4b" (adversarial
  audit). No other text dereferences "Verify step 4" (verified by grep);
  "Verify step 4a" elsewhere in the tree means `design-taste-frontend`
  step 4a, a different skill's step — no collision.
- **DR-M3** (both engines, snapshot rule): "Two redesigns never share an id:
  if a snapshot directory or a `re-verification <redesign-id>:` ledger entry
  with that id already exists, append `-2`, `-3`, … until the id is unused."
- **DR-M4** (both engines, revert (2)): "verify with `git status` (when the
  tree is a git repo) …; when the tree has no repo, verify against the snapshot
  manifest alone — each restored path diffed against its snapshot copy and its
  recorded hash — the manifest check is the fallback and the authority,
  `git status` is only a convenience."
- **DR-M5** (both engines, round definition): "the line is created as
  `fresh-verdict rounds used: 0/2` in `.hackathon/run-ledger.md` when the run
  ledger is first created (at Gate 1, before the Verification stage) — if it
  is missing when first consulted, create it as `0/2` before spending, never
  spend from a missing line".
- **DR-M6** (`polish.md` Step 5.2): the Impeccable-detector sentence now
  carries the carve-out — a template-pattern finding (e.g. `icon-tile-stack`,
  rules.json:175) is appended to `.hallmark/candidate-evidence.md` and fixed
  only on `browser-qa`'s verdict; "never rewrite a template pattern on the
  detector's say-so alone."
- **DR-M7** (orchestrate `:195`, standalone `:49`): the duplicated
  "after the run, the orchestrator records `fresh-verdict rounds used: N/2`…"
  sentence is gone from both step-6 fresh-run paragraphs; each now reads
  "the round definition in 5b/6b states the ledger update, and the
  orchestrator consults that line before spending more". "after the run, the
  orchestrator records `fresh-verdict rounds used: N/2`" is now 0 hits in
  both engines.
- **Sweep M1** (`gates.md:225` gate 68): appended "The wireframe read is
  candidate evidence of a generated look, for `browser-qa` to weigh at a
  glance."
- **Sweep M2** (`review-finish.md:5`): first line is now one of `recapture` /
  `findings` / `no-findings`; "`findings` (craft findings follow — a first
  viewport that fails the idea or the theme wholesale is named explicitly
  among them)"; "The first word is a craft status, not a ship/fix/rebuild
  verdict". Consumers updated: orchestrate `:195`, standalone `:49`
  ("Act on its first word (`recapture` / `findings` / `no-findings`)"),
  `gates.md:245` ("Send the recaptures back for one scoring round only when
  a finding names a first-viewport wholesale failure or a Floor gate";
  stamp record now `hero-review: findings · 4 findings · 4 resolved`).
- **Sweep M3** (`review-hero.md:5`): first line is now "`findings` or
  `no-findings`"; "The word is a craft status, not a ship/fix verdict".
  Consumer updated: Taste `:314` ("Act on its first word (`no-findings` /
  `findings`) for the craft findings").

## Held back / deviations (with reasons)
- None. Every scoped item is implemented in both engines where it applies.
  The gates §6 ship rule and the Taste gate were NOT re-adjudicated, per the
  task (already adjudicated in earlier rounds).
- Parent note honored: the `git checkout` hits in both engines are the
  explanatory warning text ("never from version control alone (`git checkout`
  restores HEAD…)"), not a restore instruction — not re-flagged, not changed.

## Bounds kept
No new gates/waits/questions; no new skills/agents/rules/commands; deferred-six
carve-out, Grok 4.7 High pin + picker instruction, anti-derivative rule,
"more, not bolder" posture, CBM phrasing untouched; direction lenses /
live-generate stay out; frontend-slides stays on-demand; pins + SSML truth
held; no fix11 re-run; no pip pinning; no repo/bundle touching; OpenMontage
runtime-fetch left as documented opt-in. GATE patch inserted after fix13h,
still before STEP 5.

## Checks (to be filled by Audit #50 / dry-run #22 / sweep)
- Audit #50: (pending)
- Dry-run #22: (pending)
- Single-executor sweep: (pending)
