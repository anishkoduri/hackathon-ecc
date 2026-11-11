# Dry-run #22 — hackathon-ecc first build (Campus Eats) — report

- Build: `~/workspace/hackathon-plugin/build.sh`, 23,117 lines, md5 `cb12ab81c3334dba68054ba18c1d4f15` (verified)
- Built tree: `~/workspace/hackathon-plugin/hackathon-ecc/`
- Built-tree manifests: `fix13i/manifest1.txt` and `manifest2.txt` both `eecb5315311c70d9675951db4b37ff7f` (diff = 0, verified — read, not rebuilt)
- Counts verified: 169 skills / 72 agents / 123 rules / 96 commands / 15 hook events in `hooks/hooks.json` / 57 MB
- Fix round under test: #13i (`~/workspace/hackathon-plugin/fix13i/MANIFEST.md` read first)
- Method: read-only simulation of the Campus Eats first build end-to-end (grill-me → scope → expansion Phases 0–3 → slices → Verification stage Verify steps 1–6 → 5b polish + polish-routed redesign → 5c deploy → 5d demo → step 6 commit/README/final report), plus the standalone `orch-build-mvp` branch (steps 6 + 6b) and the cold-start `/gan-build` / `/gan-design` path. Every finding verified by reading the built file at the cited line — never from memory or the fixer's report.
- Verdict: **NOT CLEAN — 0 BLOCKING, 1 MINOR**

## Verdict

**NOT CLEAN, on one minor only.** All 12 fix-#13i items (1 blocking + 11 minor) verified as implemented with file:line evidence — dry-run #21's B1 and M1–M7 are all closed, and the three sweep items are in place. The single remaining finding is new, pre-existing (not introduced by #13i, and missed by dry-run #21): the snapshot rule tells the orchestrator to write the whole-tree file list + per-file hashes into `.hackathon/run-ledger.md`, which directly violates the same skill's 20-line ledger cap. Minor, not blocking: the manifest still lands somewhere durable either way, and the revert can still execute — but the two rules cannot both be followed literally, and the revert's "snapshot manifest" has no unambiguous home.

## MINOR (1)

### M1 — Snapshot manifest location contradicts the 20-line ledger cap (orchestrate)
- `skills/orchestrate/SKILL.md:8` (Process rule): "The **stage ledger** stays a short run-state file (20 lines max), not a PRD. Bulky loads overflow to `docs/run-ledger-appendix.md` (one line per item) with a one-line pointer in the ledger — the 20-line cap applies to the ledger file itself."
- `skills/orchestrate/SKILL.md:60` (5b snapshot rule, stated twice in the same line): "record the snapshot path + the full file list (excluding those two paths) + per-file hashes in `.hackathon/run-ledger.md`"; same wording in `skills/orch-build-mvp/SKILL.md:53` (6b).
- Simulated step: 5b / 6b polish-routed redesign, snapshot-before-redesign on the Campus Eats tree.
- What breaks: a whole-tree file list + per-file hashes is dozens to hundreds of lines for any real app — an order of magnitude over the 20-line cap, and exactly the kind of bulky load the overflow rule exists for. The orchestrator must violate one rule or the other: follow the snapshot rule literally and the ledger stops being the ≤20-line run memory it is re-read at every fan-in (burying the `fresh-verdict rounds used: N/2` line and the `re-verification <id>:` entries in a hundred-line file); follow the cap and the manifest lands in `docs/run-ledger-appendix.md`, where the revert steps never say to look — revert step (2) only says "verify against the snapshot manifest alone", naming no file. The 5b intro itself uses the appendix pattern for verification outcomes ("Record each Verification-stage check's outcome … in `docs/run-ledger-appendix.md`, with a one-line pointer … in `.hackathon/run-ledger.md`"), so the snapshot rule is the outlier.
- Scope note: the conflict is orchestrate-only as written — standalone states no ledger cap — but standalone shares the snapshot-rule wording, and the ledger is the same file in both engines.
- Fix direction: route the snapshot manifest to `docs/run-ledger-appendix.md` (one line per file + hash, per the overflow rule) with a one-line pointer in `.hackathon/run-ledger.md`, in both engines; and have revert step (2) name the manifest's file. Alternatively, keep the manifest in the ledger and exempt it from the cap explicitly — but the exemption must be stated, since the cap as written admits none.

## Fix-#13i scope — all verified implemented

### B1 (blocking) — Snapshot excludes run state; revert never restores it
- `skills/orchestrate/SKILL.md:60` (5b) and `skills/orch-build-mvp/SKILL.md:53` (6b), identical text. Snapshot: "copy the WHOLE tree EXCEPT `.hackathon/` and `.hallmark/candidate-evidence.md` into `.hackathon/redesign-snapshot/<redesign-id>/`", with both reasons stated (snapshot dir lives inside the tree being copied, so a literal whole-tree copy would copy the snapshot into itself; `.hackathon/` and `.hallmark/candidate-evidence.md` hold live run state, not tree state).
- Revert (1): "the live `.hackathon/run-ledger.md` and `.hallmark/candidate-evidence.md` are NEVER overwritten by a revert, so the ledger's `fresh-verdict rounds used: N/2` line and the `Superseded by redesign <redesign-id> — do not re-judge` markings survive a revert as written."
- Revert (3): "the ledger's `fresh-verdict rounds used: N/2` line is untouched by the revert — run state is never restored — so the round spent on the failed re-verification stays spent."
- Coverage check exempts both paths: "except the two excluded run-state paths (`.hackathon/`, `.hallmark/candidate-evidence.md`), which are never in the manifest by design and are never a coverage failure."
- Revert (2): deletion of redesign-created files exempts "the excluded run-state paths (`.hackathon/`, `.hallmark/candidate-evidence.md`), which are never deleted."
- Dry-run #21 B1 is closed: the stale-ledger restore and the self-referential copy are both excluded by construction. Full failing-redesign trace in (a) below.

### DR-M1 — "5c/Verify-step-6 checks below" → "the 5c and step-6 checks below"
- Orchestrate `:60`: "the 5c and step-6 checks below consult the entry for that redesign-id (`re-verification <redesign-id>: PASSED/BLOCKED`), not working-context memory." The checks below 5b are 5c deploy (`:61`) and step 6 commit (`:64`), both of which carry their own correctly worded re-verification checks. `5c/Verify-step-6`: 0 hits in both engines. Standalone 6b keeps the correct "the step-7/step-8 checks below" (`:53`).

### DR-M2 — Verify step 4a / 4b renumber
- Orchestrate `:187`: "Verify step 4a. **Any diff that touches a UI surface (any size)** → a blind reviewer ALWAYS runs…"; `:191`: "**Verify step 4b. Adversarial audit (a distinct named step — after the reviewer pass, before deploy).**" Stage numbering is now 1, 2, 3, 4a, 4b, 5, 6 (`:183`, `:184`, `:185`, `:187`, `:191`, `:193`, `:195`). Bare "Verify step 4" (not followed by a/b): 0 hits anywhere in `skills/`, `commands/`, `rules/`, `agents/`. Dry-run #21 M2 closed.

### DR-M3 — Redesign-id uniqueness rule, both engines
- Orchestrate `:60` and standalone `:53`: "Two redesigns never share an id: if a snapshot directory or a `re-verification <redesign-id>:` ledger entry with that id already exists, append `-2`, `-3`, … until the id is unused." Dry-run #21 M3 closed.

### DR-M4 — `git status` no-repo fallback, both engines
- Orchestrate `:60` and standalone `:53`, revert (2): "verify with `git status` (when the tree is a git repo) plus a diff restricted to snapshot-listed paths (each restored path diffed against its snapshot copy); when the tree has no repo, verify against the snapshot manifest alone — each restored path diffed against its snapshot copy and its recorded hash — the manifest check is the fallback and the authority, `git status` is only a convenience." `git checkout` hits in both engines are only the explanatory warning text ("never from version control alone (`git checkout` restores HEAD, not the verified state…)"), per the parent note — not re-flagged. Dry-run #21 M4 closed.

### DR-M5 — Fresh-verdict budget initialized to 0/2, both engines
- Orchestrate `:60` and standalone `:53`: "the line is created as `fresh-verdict rounds used: 0/2` in `.hackathon/run-ledger.md` when the run ledger is first created (at Gate 1, before the Verification stage) — if it is missing when first consulted, create it as `0/2` before spending, never spend from a missing line." `fresh-verdict rounds used: 0/2` hits: exactly the two engine lines. Dry-run #21 M5 closed. (Observation, not a finding: the creation instruction lives in the 5b/6b consumer text, not in orch-pipeline's Gate 1 procedure — but the missing-line fallback makes the ordering safe; see Observations.)

### DR-M6 — Detector carve-out in polish.md Step 5.2
- `skills/polish-pass/reference/polish.md` Step 5.2: "Re-run the Impeccable detector too … and fix real findings the same way — EXCEPT a template-pattern finding (e.g. `icon-tile-stack`: a small rounded-square icon container above a heading is the universal AI feature-card template): append it to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`, and fix it only on `browser-qa`'s verdict — never rewrite a template pattern on the detector's say-so alone." `icon-tile-stack` is rule id at `skills/polish-pass/reference/impeccable-detector-rules.json:175`. A detector finding can no longer route to a rewrite without `browser-qa`'s verdict. Dry-run #21 M6 closed.

### DR-M7 — Duplicated ledger-update sentence removed from both step-6 fresh-run paragraphs
- "after the run, the orchestrator records `fresh-verdict rounds used: N/2`": 0 hits in both engines. Orchestrate `:195` and standalone `:49` now read "the round definition in 5b/6b states the ledger update, and the orchestrator consults that line before spending more." Dry-run #21 M7 closed.

### Sweep M1 — gates.md gate 68 routed to candidate evidence
- `skills/design-taste-frontend/references/hallmark/references/gates.md:225`: gate 68 ends "The wireframe read is candidate evidence of a generated look, for `browser-qa` to weigh at a glance."

### Sweep M2/M3 — First-word vocabulary end-to-end
- `review-finish.md:5`: "First line: one of `recapture` … `findings` (craft findings follow — a first viewport that fails the idea or the theme wholesale is named explicitly among them), `no-findings` … The first word is a craft status, not a ship/fix/rebuild verdict."
- `review-hero.md:5`: "First line: `findings` or `no-findings`. The word is a craft status, not a ship/fix verdict."
- Orchestrate `:195`: "Act on its first word (`recapture` / `findings` / `no-findings`) for the gates, plain defects, copy, and layout findings…"
- Standalone `:49`: "Act on its first word (`recapture` / `findings` / `no-findings`) for its gates, plain defects, copy, and layout findings…"
- Taste `skills/design-taste-frontend/SKILL.md:314`: "Act on its first word (`no-findings` / `findings`) for the craft findings…"
- `gates.md:245`: "Send the recaptures back for one scoring round only when a finding names a first-viewport wholesale failure or a Floor gate"; stamp record `hero-review: findings · 4 findings · 4 resolved`.
- No `ship` / `fix` / `rebuild` first-word value or consumer remains anywhere in `skills/` / `commands/` (grep for first-word/first-line review values: only the six hits above plus the two review-file definitions). The gates.md §6 "Nothing ships with an open `FAIL`" sentence is the adjudicated ship rule, not a first-word value — not re-adjudicated, per the manifest.

### Audit M1 — Five polish.md links resolve
- `skills/polish-pass/reference/polish.md:18,19,39,40`: `[impeccable-detector-rules.json](impeccable-detector-rules.json)`, `[impeccable-critique.md](impeccable-critique.md)`, `[impeccable-craft-floor.md](impeccable-craft-floor.md)`, `[impeccable-onboard.md](impeccable-onboard.md)`, `[impeccable-extract.md](impeccable-extract.md)` — all five targets exist in the same directory. Remaining `reference/` mentions in polish.md (`:7`, `:40`, prose `reference/lenses/`) match the established skill-dir-relative convention in `polish-pass/SKILL.md:41,45-46`, and `SKILL.md:92` keeps its `reference/craft-floor.md` link, correct from the skill root.

## Traces

### (a) Failing polish-routed redesign → revert → deploy/commit (orchestrate path)
Simulated: Campus Eats landing reads as a generic template; polish (5b, `:60`) routes redesign `landing-template`; Verify step 6 had already consumed 1 fresh-verdict round (finish-review re-inspection), so the ledger reads `fresh-verdict rounds used: 1/2`.
1. Snapshot BEFORE any redesign file is overwritten: whole tree except `.hackathon/` and `.hallmark/candidate-evidence.md` → `.hackathon/redesign-snapshot/landing-template/`; file list + hashes recorded in the ledger. The snapshot excludes itself: its destination lives under `.hackathon/`, which is excluded — no self-referential copy.
2. Budget check passes (1/2, one round remains) → design skill builds the redesign; candidate-evidence entries about the landing are marked `Superseded by redesign landing-template — do not re-judge`.
3. Fresh `browser-qa` verdict run on the redesigned screens → consumes round 2 → ledger updated to `2/2`. Verdict FAILS.
4. Revert (1): snapshot files copied back; live ledger and candidate-evidence NEVER overwritten → `2/2` line and `Superseded by redesign` markings survive as written.
5. Revert (2): redesign-created files not in the snapshot deleted (except the two excluded run-state paths); modified files restored from the snapshot copy, never from version control alone; verified by `git status` + diff on snapshot-listed paths (manifest-only when no repo).
6. Revert (3): `re-verification landing-template: BLOCKED` + snapshot path + reverted files recorded; ledger line untouched → the spent round stays spent at `2/2`.
7. Revert (4) + 5c (`:61`): deploy of the redesign HELD; the reverted verified tree is deployed and its URL recorded. 5d (`:62`): the demo films the LOCAL verified tree. Step 6 (`:64`): the redesign's files are not committed (already reverted); `BLOCKED` recorded; Gate 2 auto-approval never covers an unverified redesign.
8. **Budget regain check:** `fresh-verdict rounds used` appears ONLY in the two engine lines (orchestrate `:60`, standalone `:53`); no other writer and no reset instruction exists anywhere in `skills/` / `commands/` / `rules/` / `agents/`. The revert explicitly preserves the line. No path regains a spent round. The standalone path (6b `:53` → step 7 `:55` → step 8 `:56`) carries the identical mechanics.
- One residual wrinkle in this trace is M1 above: the snapshot manifest the revert verifies against is recorded "in `.hackathon/run-ledger.md`" per the snapshot rule, against the 20-line cap at orchestrate `:8`.

### (b) 0/2 initialization ordering
- Both engines create the line at Gate 1 (before the Verification stage), and the first consultations are Verify step 6's fresh run (orchestrate `:195`, standalone `:49`) and the 5b/6b budget check — all after Gate 1. The visual loop (Verify step 5) draws on its own separate caps (max 3 rounds total, ≤2 fix rounds per problem list), never on this budget. No spend can precede creation; the missing-line fallback covers a ledger created without the line.

### (c) Verify-step-4a/4b numbering
- See DR-M2 above: unambiguous, no bare "Verify step 4" dereference anywhere. The only other "step 4a" in the tree is `design-taste-frontend`'s own step 4a (a different skill's step, reached only inside Taste), no collision with the Verification-stage labels.

### (d) First-word vocabulary
- See Sweep M2/M3 above: definitions and all five consumers agree on `recapture` / `findings` / `no-findings`.

### (e) Detector carve-out
- See DR-M6 above: a template-pattern detector finding (`icon-tile-stack`, rules.json:175) is appended to candidate evidence and fixed only on `browser-qa`'s verdict.

### (f) Gate 68 routing
- See Sweep M1 above.

### (g) Five polish.md links
- See Audit M1 above: all five resolve to existing files in the same directory.

## Rest of the flow (spot-verified, no findings)

- **Grill-me → scope → expansion:** `grill-me/SKILL.md:25-26` maintains the running decision record incrementally, finalized into `docs/decision-record.md` (`:46`); orchestrate steps 1–2 and standalone steps 1–2 run `hackathon-scope` then `feature-expansion` Phases 0–3 automatically with no user gate (`feature-expansion/SKILL.md:12,18`); orch-pipeline Gates 1/2 auto-approve in a first build (`orch-pipeline/SKILL.md`, Gates 1/2).
- **Browser-qa as sole distinctiveness executor:** orchestrate Verify step 5 (`:193`) and step 6 (`:195`), standalone step 6 (`:49`) — `browser-qa` alone renders the verdict; verdict values `SHIP / SHIP WITH FIXES / DO NOT SHIP` at `browser-qa/SKILL.md:106`. No-candidate-evidence guard present in both engines ("If the Hallmark audit produces no candidate evidence …, no fresh round is spent — record that in the ledger (rounds used unchanged)").
- **Deploy-fast:** Timing rule at `deploy-fast/SKILL.md:32` (security-review pre-deployment checklist gates the final deploy, not the first-hour deploy); orchestrate 5c runs it before the final deploy.
- **Pitch-deck-video local-only filming:** `commands/demo.md:11` ("never set `shots.json` `app.url` to [the deployed URL]"), `pitch-deck-video/SKILL.md:155` (`app.url` is the local dev-server URL); orchestrate 5d / standalone step 8 film the verified tree after any revert.
- **Readme-writer:** takes deployed URL + demo video path from the ledger (`readme-writer/SKILL.md:95`); runs after commit, before the final report, in both engines.
- **Cold-start direction chain:** `commands/gan-build.md:23-24` step 0 runs ALWAYS including under `--skip-planner`, reads `docs/decision-record.md` FIRST, adopts its direction into `docs/design-tokens.md`, invokes the design-lead (grok-4.7-high) only when neither record nor tokens carry a direction; `commands/gan-design.md:12,17` carry the identical chain; record wins over spec.md on both paths.
- **Sloplint scope guard:** `sloplint-render.mjs:740-747` (`observeSpace` skips template gates on app scope, mirroring `APP_SKIP`); `memory.;`: 0 hits in both engines.
- **Orchestrate / standalone parity:** shared fresh-verdict budget (2 rounds, one `browser-qa` verdict run = one round) stated identically in both engines; per-redesign-id `re-verification <id>: PASSED/BLOCKED` entries consulted by 5c/step 6 (orchestrate) and step 7/step 8 (standalone), never from working-context memory.

## Observations (not findings)

- **Gate-1 creation point is specified only in the consumer.** The 0/2 creation instruction ("when the run ledger is first created (at Gate 1…)") lives in the 5b/6b round definition; orch-pipeline's Gate 1 procedure itself only records the approved `task_list` in `docs/run-ledger-appendix.md` with a pointer in the ledger, and never mentions the budget line. Harmless as written because the missing-line fallback ("if it is missing when first consulted, create it as `0/2` before spending") closes the gap — no spend can occur from a missing line — but a future edit that drops the fallback would reopen dry-run #21's M5.
- **Standalone step-6 shorthand.** Standalone `:49` says entries a redesign supersedes are marked "`Superseded` — see 6b", while 6b (`:53`) defines the full marking "`Superseded by redesign <redesign-id> — do not re-judge`". The cross-reference resolves it; the shorthand is not a competing marking.

## Counts

- BLOCKING: 0
- MINOR: 1 (M1 — snapshot manifest location vs 20-line ledger cap; pre-existing, not #13i scope)
- Fix-#13i items verified: 12 of 12 (B1 + DR-M1–M7 + Sweep M1–M3 + Audit M1)
- Verdict: **NOT CLEAN**
