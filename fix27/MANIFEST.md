# Fix #27 — MANIFEST

**Fix:** debloat the plugin to a lean winning-build set (166 → 67 skills), loosen the
theme cage to a starting point, always-lead orchestration (Grok 4.7 High leads every
prompt), usage cuts, the missing weekend rules, DESIGNPKG-AUTO (design package is the
automatic routing for ALL design decisions), MotionSites vendored as a free-sample
component source, and palette-first design order. Animaster Lib investigated and LEFT
OUT (fully paywalled — see below).
**Authority:** `fix27/SPEC.md` (§0–§8) + `fix27/PARENT-GUIDANCE.md` + the three user
steers folded into this fix (DESIGNPKG-AUTO, MotionSites, Animaster + palette-first).
**Close date:** Nov 16, 2026. **Coordinator:** fix #27 coordinator.
**Status:** CLOSED — with the §7 criterion exceptions in §4 and the open parent
adjudications in §5 recorded as they are, not as verified. The audit and sweep
criteria read NOT MET as written (see §4); the post-audit and post-sweep fixes are
recorded and re-verified by rebuild + verifier, not by a re-audit or re-sweep.

## Results

- build.sh: 24,100 lines, md5 `dcfedbae1bda45e0dc36189ae8cb11bb` (pre-sweep-fix md5
  `ff7fe0015210b3583f69afb4f5a40816`; the move is the Sweep #35 prose fix only —
  comment/docstring rewords, 0 net lines; +12 lines vs fix #26's 24,088, exactly the
  fix27 invocation block).
- verify27.py: **79/79 checks, exit 0** — run 7 on the final build (run 8, logged in
  `fix27/build-log-run8.txt`). Run 6 was 79/79 on the first run-8 build; the logged
  rebuild is deterministic (same md5, same counts).
- fix27.py: **102 changes** on the final build, 13 OWED items recorded, "fix27: OK"
  (`fix27/fix27-patch-log.md`).
- Audit loop: Audit #74 NOT PASS (15 blocking, 11 minor) → Audit #75 NOT PASS
  (1 blocking, 6 minor) → Audit #76 NOT PASS (0 blocking, 1 minor — M-new-7, fixed
  post-audit). Sweep #35 NOT CLEAN (0 blocking, 1 minor — stale round-1 counts in
  prose, fixed post-sweep). Dry-run #42 PASS (see §3).
- Counts: **67 skills / 45 agents / 123 rules / 55 commands / 15 hooks / 49 trigger
  keys.** 100 skills CUT + 1 MotionSites added = 67; 27 agents removed; 32 commands
  dropped (27 round-1 + 5 round-2). Rules unchanged at 123 by design (§1(d)).
- Call map: md5 `d82aec31bd98831533afd850f2861927` (run-6 map, unchanged by the
  post-sweep prose fixes); uncalled 16, second-order orphans 7 (dry-run #42 Leg 5).
- Grok pins: `grok-4.7-high` 56, `cursor-grok-4.6-high-fast` 74, bare
  `grok-4.6-high-fast` 0 (built tree, excl. node_modules).
- Banned terms: 0 unallowed; exactly 3 allow-listed MotionSites lines
  (`skills/motionsites-web-builder/SKILL.md:25`, `:38`; `LICENSE:1`) — the 2 fetch
  URLs + the license line, allow-listed by content in verify27 check 8.
- Anchor tokens: 20 `_F27` tokens (see §2). Token census: 92 staged / 113 built;
  every delta is a documented build-time patch (sweep #35).
- Builds: all 8 runs with the fix #26 env-redirected invocation (`TMPDIR` /
  `UIPRO_DIR` / `SKILL_SRC` to disk; `ECC_REPO` stays hardcoded to
  `/tmp/ecc-repo-clean`). fix11/fix11-stage.py never re-run. Staged sources only;
  build.sh is the source of truth.

## §1 Scope

§1–§8 per `fix27/SPEC.md` plus the three steers. Staged sources only, never the
built tree; build.sh is the source of truth; `fix11/fix11-stage.py` never re-run.
Upstream halves are patched at build time by `fix27/fix27.py` (same pattern as
fix26/fix26.py), invoked by build.sh after fix26, before STEP 5 Counts — §7
(original) + §7a–§7o (round 2) + §8 (round 3) patch blocks; 102 changes on the
final build. No bundle, no commit, no push by fix workers — the push is the
coordinator's step after this manifest (see §7).

Builds: run 1 exit 0 (~225 s); run 2 exit 0 (~161 s); run 3 exit 0 (~173 s);
run 4 exit 0; run 5 exit 0; run 6 exit 0; run 7 exit 0 (after the M-new-7 fix);
run 8 exit 0 (after the Sweep #35 prose fixes; re-run logged to
`fix27/build-log-run8.txt` to keep a full log of the shipping build).

## §2 Disposition table

Every SPEC item, what happened to it, and where it lives. Anchor tokens are the
stable locators (line numbers drift).

| Item | Disposition | Location |
| --- | --- | --- |
| §1(a) Skill cut — 100 CUT | DONE. 100 skills removed at build time: the 91 in `fix27/skill-inventory.md`'s CUT list + the 10 REVIEW adjudications in SPEC §1(a), minus gan-style-harness (KEPT — the inventory's duplication claim was contradicted by dispatch evidence; it IS the MVP inner loop, `/gan-build`). Includes bengali-nlp (the "Bengali something" skill — a Bengali writing helper; no hackathon-build use) and the other language-specific writing helpers and niche non-hackathon skills. Growth-log KEPT (delivery-gate's hook blocks a complex task when growth-log is stale). Full per-skill KEEP/CUT/REVIEW record in `fix27/skill-inventory.md`. | Build-time: `fix27/fix27.py` §7/§7a–§7o/§8; inventory `fix27/skill-inventory.md`; weekend audit `fix27/weekend-audit.md` |
| §1(a) +1 MotionSites skill | DONE (steer 2). Net skills 166 − 100 + 1 = 67. See MotionSites row below. | Staged: `new-skills/motionsites-web-builder/`; build.sh new-skills loop (`build.sh:217`) |
| §1(b) Mechanism — build-time removal | DONE. fix27.py removes the CUT skills/agents/commands, prunes 15 trigger keys (64 → 49), prunes pi-core.json (skills.include 93 → 30, commands.include 24 → 18), and applies the text patches with exactly-once anchors (fails loudly on mismatch). Idempotent-tolerant on removals. | `fix27/fix27.py`; patch log `fix27/fix27-patch-log.md` |
| §1(b) Commands dropped — 32 | DONE. 27 round-1 + 5 round-2 (learn-eval, project-init, projects, promote, prune) = 32; `DROPPED_COMMANDS` asserted `len == 32` (`fix27/fix27.py:187`). learn KEPT (user-invoked, on-demand; distinguishes itself from CLv2). project-init CUT (ECC install/onboarding, not a build step). Epic commands NOT cut: `fix27/fix27.py:163` ("epic-decompose [is] NOT [a] candidate (SPEC §1(b)) and [is] untouched"); all 7 epic commands are in `KEPT_COMMANDS` (`fix27/verify27.py:201–202`) and ship in the built tree. | `fix27/fix27.py:169–187`; `fix27/verify27.py:190–215` |
| §1(b) Agents removed — 27 | DONE. 72 → 45. Includes the 13 coordinator-adjudicated removals (ecc-conversation-analyzer, ecc-cpp/go/java/php/ruby/swift build-resolvers and reviewers, ecc-marketing-agent). ecc-a11y-architect KEPT (serves kept frontend-a11y). | `fix27/fix27.py` |
| §1(c) Call map | DONE. Regenerated from the reduced tree; EXPECTED 67/45/123/55/15/49 in the generator; md5 `d82aec31bd98831533afd850f2861927`. | `fix25/callmap/generate_call_map.py`; `hackathon-ecc/skills/orchestrate/references/call-map.md` |
| §1(d) What is NOT cut | DONE as specified. Rules (123) NOT cut in this fix — the ~80 per-language rule files are a follow-up debloat candidate (open parent adjudication, §5). Their dangling skill pointers are pointer-style only (OWED-11/M7). | Open item §5 |
| §2 Themes — starting point, not cage | DONE. Hallmark theme deal demoted from cage to starting point; bound-(2) relaxation + new-theme inversion are verbatim identical across all four E1 copies (`skills/orchestrate/SKILL.md:148`, `skills/design-taste-frontend/SKILL.md:425`, `skills/orch-build-mvp/SKILL.md:43`, `skills/ui-ux-pro-max/SKILL.md:274`). Design package + D19 reasoning stay. | Token `THEME-START_F27` |
| §3 Orchestration — always-lead | DONE. The 3 gating points that limited Grok 4.7 High to the first prompt are removed; the orchestrator leads every prompt/interaction. B14 agrees (`skills/orchestrate/SKILL.md:57` vs `rules/hackathon-mode.mdc` §7:60/:62, including the §7 carve-out). | Token `ALWAYSLEAD_F27` |
| §4(a) W1 — implementer-model contradiction | DONE. The contradiction (orchestrator vs implementer model) reconciled — the largest usage lever. | Token `IMPL46_F27` |
| §4(b) W2 — blind-parallel second deep-reasoner pass | DONE. Gated. | Token `W2_F27` |
| §4(c) W3 — verification layers capped | DONE. | Token `W3_F27` |
| §4(d) W4 — record-keeping bounded | DONE. | Token `W4_F27` |
| §5(a) CEILING — lock-in rule | DONE. New rule: flag the quality/score ceiling the moment it is knowable; never let the user discover a low ceiling the night it is due. (Was MISSING before this fix.) | Token `CEILING_F27` |
| §5(b) DELRISK — unmet-deliverable rule | DONE. New rule + hackathon-mode §7 carve-out: if a deliverable cannot be met, say so immediately and let the user decide (best honest framing, try our best, or a workaround); never silently drop it. (Was PARTIAL and conflicted with hackathon-mode §7 before this fix.) | Token `DELRISK_F27` |
| §5(c) CHECKSRC + AUDITGUIDE + exact verified numbers | DONE. New rules: check the source before stating scoring, timing, or logistics; audits are a guide, not the source; deliverable prompts cite the exact spec and use only exact verified numbers. (Were MISSING before this fix.) | Tokens `CHECKSRC_F27`, `AUDITGUIDE_F27` |
| §5(d) TESTNOTBQA — test passage is not browser verification | DONE. One-liner rule: test passage and agent self-reports are NOT browser verification; browser-qa is the sole executor of pass/fail screen verdicts. | Token `TESTNOTBQA_F27` |
| §5(e) NOCOAUTHOR — no `Co-authored-by: Cursor` trailer | DONE. New rule: commits carry author Anish Koduri <akoduri05@gmail.com> only, no Co-authored-by/Cursor trailer; never list Cursor or any AI tool as a contributor/author/team member. (Was NOWHERE in the shipped tree before this fix.) | Token `NOCOAUTHOR_F27` |
| §5(f) Grill-me holes | DONE. Grill-me well encoded with 2 holes closed (header + capture). | Tokens `GRILLHDR_F27`, `CAPTURE1_F27`, `TESTPASS_F27` |
| §6 DESIGNPKG-AUTO — design package automatic for ALL design decisions (steer 1) | DONE. Every design decision (layout, color, type, spacing, motion, component choice, hierarchy, any visual call) routes through the design package automatically, not opt-in. Byte-identical in `skills/orchestrate/SKILL.md:35` and `rules/hackathon-mode.mdc:44` (same 10-skill list, same MotionSites gloss). The audit loop checks design decisions went through it (verify27 token census + sweep weaving check (a)). | Token `DESIGNPKG-AUTO_F27` |
| MotionSites — vendored, cleaned (steer 2) | DONE. Upstream `github.com/Motionsites-AI/claude-skill`, skill `motionsites-web-builder` (700+ designs; agent reads 2–3 of 40 free example prompts, picks from 50+ hosted hero videos). **Fit-check finding: the upstream skill DOES inject promo links** — SKILL.md carries a mandatory "MotionSites Unlimited" upgrade block (UTM link) on every delivery plus upsell nudges and an "Always keep the UTM links" rule. It was NOT added as-shipped. Instructions/references/scripts are MIT-licensed (modification explicitly permitted), so a CLEANED copy was vendored: sponsor section + upgrade block + nudges + UTM rule all removed; free sample only; never the paid Unlimited library. The vendored skill contains zero promo/UTM content. License boundary: SKILL.md + references/ + scripts/shoot.py = MIT (vendored, incl. the upstream LICENSE file); examples/ (40 files + INDEX.md) + media/ (MEDIA.md + 6 sheet jpgs) = © MotionSites — usable to build sites but NOT resellable/redistributable as a collection, and the built tree IS published to the public GitHub repo, so examples/media were NOT vendored; they are fetched from upstream raw GitHub URLs at use time (`SKILL.md:25` INDEX.md, `SKILL.md:38` MEDIA.md). Use-time upsell fixed: the fetched INDEX.md carries a "Go Unlimited" UTM upsell, so the vendored SKILL.md step 2 (`:26`) carries an ignore-upsell line (free sample only; never premium/paid content; never reproduce the upsell link). Wired as a consulted source, not a template cage: framing header scopes it (Taste leads the build; browser-qa owns the visual verdict; step 6's shoot-and-fix maps to browser-qa; shoot.py is an optional capture helper, never the verdict; fonts static/self-hosted). Staged fixes: step-1 "references/techniques.md" → "references/techniques/INDEX.md" (upstream bug); step 5 "Google Fonts" → self-hosted fonts (plugin rule); builders.md:10 "Cursor / Claude Code" → "Cursor". Check-8 allow: exactly the 3 lines (2 fetch URLs by content, LICENSE:1). | Staged: `new-skills/motionsites-web-builder/` (SKILL.md 84 lines, references/ 5 files + 7 techniques, scripts/shoot.py, LICENSE); build.sh new-skills loop (`build.sh:217`); token `MOTIONSITES_F27`; wired in `DESIGNPKG-AUTO` (orchestrate:35, hackathon-mode:44) |
| Animaster Lib — LEFT OUT (steer 3a) | INVESTIGATED, NOT ADDED. animmasterlib.dev fetched live twice: "300 PRO UI COMPONENTS FOR MODERN WEB PRODUCTS"; PRO $4.99 (struck $10), Premium $8 (struck $20), one-time; FAQ verbatim: "You'll receive access to a Google Drive folder containing all the components" (after purchase), "This is a one-time purchase with access to materials for a lifetime", "60% HTML/CSS/JS / 30% React / 10% Next.js". NO free tier, free sample, or free download anywhere on the 720-line homepage — only thumbnail previews. Commenters on the promoting reels confirm ("you have to pay", "Paid service, don't waste your time"). Verdict: effectively fully paywalled — NOT vendored, NOT wired, NOT a dependency, NOT in the PALETTE-FIRST palette (not even as inspiration-only: thumbnails carry no code and pointing the design flow at a paywall invites friction). The user can overrule if he wants it as inspiration. Standing rule (free tiers only) upheld; no money spent, no paid gate added. | Record: `fix27/animaster-fit-check.md`; confirmed live by Audit #76 |
| Palette-first design order (steer 3b) | DONE. The flip: inventory the available components/designs FIRST, base the design on that palette, tailor to needs, then build — instead of plan-first-then-reject-components. Palette-inventory step at the top of step 4 in design-taste-frontend (`:224`), before the Hallmark theme deal (`:258`) and the step-4a freeze (`:413`); agreed palette contents in all three files with zero Animaster anywhere. Palette = motionsites-web-builder (free sample only) + ui-ux-pro-max, less-flat-ui, motion-foundations, motion-patterns, motion-advanced, make-interfaces-feel-better, design-system + dealt Hallmark theme as starting point. A design direction naming no palette components is incomplete; the audit checks the design-direction record names the palette components used. | Token `PALETTE-FIRST_F27` (design-taste-frontend:224, orchestrate:35, hackathon-mode:44) |
| §7 Verification criteria | See §4 — recorded honestly, criterion by criterion. | — |
| §8 Non-goals | HELD. No fix #14–#26 adjudication re-litigated; no frozen verifier-asserted text rewritten except the one authorized §7 update (none was needed — no build.sh comment it describes was edited); rules not cut (§1(d)); smoke test's live questions not pre-decided; no Campus Eats render built; no live-render requirement added. | — |

Anchor tokens (20 `_F27`): `DESIGNPKG-AUTO_F27`, `CEILING_F27`, `DELRISK_F27`,
`CHECKSRC_F27`, `AUDITGUIDE_F27`, `NOCOAUTHOR_F27`, `THEME-START_F27`,
`ALWAYSLEAD_F27`, `IMPL46_F27`, `GRILLHDR_F27`, `CAPTURE1_F27`, `TESTNOTBQA_F27`,
`DEFER3_F27`, `W2_F27`, `W3_F27`, `W4_F27`, `TESTPASS_F27`, `REROUTE_F27`,
`MOTIONSITES_F27`, `PALETTE-FIRST_F27`. (SPEC §7 lists 11; round 2/3 added 9:
CAPTURE1, TESTNOTBQA, W2, W3, W4, TESTPASS, REROUTE, MOTIONSITES,
PALETTE-FIRST.) Deferred lists shrunk six → three (`DEFER3_F27`: verification-loop,
production-audit, delivery-gate).

## §3 Audit-loop record

- **Audit #74** (`fix27/audit74-report.md`): NOT PASS — BLOCKING 15, MINOR 11.
  Debloat landed cleanly but 14 live dispatches to removed skills/commands still
  shipped in kept files + a hackathon-mode §7 vs orchestrate:57 contradiction on the
  grill-me-missed question + theme cage surviving in 2 copies + verify27 had no
  CUT-name sweep + prior verifiers crash rather than failing on codified tails.
  All fixed in round 2.
- **Audit #75** (`fix27/audit75-report.md`): NOT PASS — BLOCKING 1, MINOR 6. All 15
  B-items + M1–M8 fixed; M7 correctly carried; counts exact; MotionSites /
  palette-first / Animaster verified. Blocker B-new-1: `agents/ecc-typescript-reviewer.md:119`
  live imperative dispatch to CUT `coding-standards`, hidden by check 12's
  whole-line allow-list. Minors M-new-1 (19 dangling `accessibility` pointers),
  M-new-2 (OWED-13 stale), M-new-3 (prior-verifier retirement unrecorded), M-new-4
  (install/Pi manifests stale), M-new-5 (MotionSites use-time upsell), M-new-6 (no
  verify27 assertion on the memory-learning-skill re-point). All fixed in round 3.
- **Audit #76** (`fix27/audit76-report.md`): NOT PASS — BLOCKING 0, MINOR 1.
  Everything in #75 verified fixed with file:line evidence; verify27 re-run 79/79
  twice by the auditor; the auditor's own independent CUT-name sweep matched check
  12 exactly (0 un-allow-listed, 83 allow-listed, 293 noise — and the same sweep
  finds 28 hits on the round-2 tree, so it discriminates); check 12b proven
  discriminating by the auditor itself; pi-core prune judged sound;
  install-modules/components leave-out judged sound. The single minor M-new-7:
  OWED-13's noise breakdown still said "accessibility 132" when the live count is
  131 (the staged worker's vercel-checklist :93 re-point was not recorded). Fixed
  post-audit by the coordinator: OWED-13 in `fix27/fix27.py:1086` now says
  "accessibility 131" + enumerates vercel:93; rebuild run 7 exit 0; verify27
  re-run 79/79 (`fix27/verify27-run5.log`). **Audit #76 itself did not pass and no
  re-audit ran after the M-new-7 fix; the fix was confirmed by Sweep #35's
  independent re-derivation (see below), not by a new audit.**
- **Sweep #35** (`fix27/sweep35-report.md`): NOT CLEAN — BLOCKING 0, MINOR 1,
  weaving-coherence CLEAN. All six weaving checks (a–f) agree: DESIGNPKG-AUTO
  byte-identical in orchestrate:35 and hackathon-mode:44; PALETTE-FIRST orders the
  inventory before every direction-finalizing step in all three files; THEME-START
  identical across all four E1 copies; B14 agrees; DEFER3 names exactly the three
  kept checks; check-12 allow-list exactly 82 whole-line + 1 name-scoped = 83.
  M-new-7 fix verified with independent re-derivation (OWED-13 in fix27.py:1086 and
  the regenerated patch-log:157 byte-identical, 4,204 chars; the sweeper's own
  replication gives 293 noise lines with accessibility 131 / projects 156 /
  promote 4 / brainstorming 3 / evolve 1 / prune 1; vercel-checklist now zero
  `accessibility` hits). The one minor: stale round-1 counts (66 skills / 60
  commands / 27 dropped commands) in three live descriptions — `build.sh:24081–24082`,
  `fix27/fix27.py:256`, `fix27/verify27.py:8–10` — while the tree ships 67/55/32.
  Fixed post-sweep by the coordinator (three one-line prose edits, plus a fourth
  instance the coordinator's own grep found in the `fix27.py` header docstring
  `:16–24`, which cited SPEC §1's round-1 numbers as the script's own behavior —
  now states the actuals with the SPEC citation marked superseded). Rebuild run 8
  exit 0; verify27 re-run 79/79 (runs 6 and 7). **Sweep #35 itself stands as NOT
  CLEAN as written; no second sweep re-ran after the prose fixes** (the fixes are
  comment/docstring-only, verified by grep + rebuild + verifier).
- **Dry-run #42** (`fix27/dryrun42/dryrun42-report.md`): **PASS.** Leg 1 fixtures
  101/101 (42/42 Dry-run #37 regression + 59/59 fix #23, verbatim runners). Leg 2
  Home Run re-run: all 17 §6 assertions PASS at 4 widths × 13 states, 52
  measurements, 0 console errors, 0 failed requests; Campus Eats v5: 6/7 dimensions
  pass statically (68/66 re-trace), dimension 7 (alignment) OWED, never passed — no
  live Campus Eats render exists. Leg 3 /demo 59/59 (qa.mjs exit 0 twice, 12/12
  stills + 2 sheets, 0 Google Fonts requests; Playwright installer worked first try).
  Leg 4 Cursor-readiness 37/37 incl. 13 live C-1 hook pipe tests. Leg 5 call-graph
  17 EXERCISED / 19 STATIC-OK / 5 DORMANT / 0 BROKEN against the run-6 map; 55/55
  commands resolve; technical-depth fixture 11/11 automated + 6/6 live probe.
  - **Correction to the dry-run report (coordinator investigation, Nov 16):** the
    report states in several places that the epic commands were DROPPED in fix #27
    §1(b) ("The 8 epic/`/prune` commands were DROPPED"; "the `epic-unblock.md`
    file … was dropped in the cut"; "the epic commands no longer exist") and on that
    basis flags `hackathon-ecc/README.md:67–68` as stale prose listing dropped
    `/epic-*` commands as shipping. **That premise is wrong.** The epic commands
    were never cut: `DROPPED_COMMANDS` (`fix27/fix27.py:169–187`, asserted length
    32) contains no epic-* entry; all 7 epic commands are in `KEPT_COMMANDS`
    (`fix27/verify27.py:201–202`); all 7 `epic-*.md` files ship in the built tree
    (`hackathon-ecc/commands/`, total 55 commands); the call map has live rows for
    all 7 (`/epic-claim`, `/epic-decompose`, `/epic-publish`, `/epic-review`,
    `/epic-sync`, `/epic-unblock`, `/epic-validate`); Audit #75:108 calls them kept
    commands; `fix27/fix27.py:163` says epic-decompose is NOT a §1(b) candidate.
    Only `/prune` (1 of the "8") was dropped (round 2). The README:67–68 line
    ("The plugin's Node scripts (`/harness-audit`, `/skill-host-compat`, the
    `/epic-*` commands, `validate-skills.js`) ship with their dependencies vendored…",
    generated by build.sh STEP 4 at `build.sh:18397–18399`) is therefore ACCURATE
    and was left unchanged. Likewise the "0 `loop-status` hits" fact is right but
    its stated cause is wrong — `epic-unblock.md` still exists; the alias was
    removed in fix #25 option (b). And orchestrate:136's "stay dormant in use"
    note is prose-history per Audit #76 (B3) — the commands ship and are dormant
    in use, which is the same disposition the dry-run's Leg 5 dormant wire records,
    under the wrong reason. The dry-run's PASS verdict stands (all legs green on
    the actual tree; 0 BROKEN); only its epic narrative and the README observation
    are refuted. The dry-run report file itself is not rewritten — this manifest is
    the correcting record.

## §4 SPEC §7 criterion statuses (honest)

| Criterion (SPEC §7) | Status |
| --- | --- |
| Audit: ZERO blocking, ZERO minor | **NOT MET as written.** Final audit (#76): 0 blocking, 1 minor (M-new-7). The minor was fixed post-audit and its fix confirmed by Sweep #35's re-derivation, but Audit #76 itself did not pass and no re-audit ran. |
| Sweep: CLEAN, weaving-coherence CLEAN | **NOT MET as written (sweep half).** Sweep #35: NOT CLEAN, 0 blocking, 1 minor (stale prose, fixed post-sweep). Weaving-coherence: CLEAN. No second sweep re-ran after the prose fixes. |
| Dry-run: PASS | **MET.** Dry-run #42: PASS, all 5 legs green (see §3), with the epic-premise correction recorded in §3. |
| verify27.py: checks for every placement, exit 0 | **MET.** 79/79, exit 0, run 7 on the final build. Note: SPEC §7's count line (skills 166 → 66, commands 87 → 60) is superseded by the actuals (67, 55) — causes traced: MotionSites +1 skill; 5 round-2 command cuts. The verifier codifies the actuals. |
| Prior verifiers: re-run; fails only the codified tails | **NOT MET as written — RETIRED, not passing.** verify26.py crashes (FileNotFoundError: `skills/django-verification/SKILL.md`) and verify25.py crashes (KeyError: `'skills'` at second_order_orphans) against the reduced tree (M-new-3/M11). They assume the old tree shape and cannot run at all — this is beyond the "codified tails" the SPEC anticipated. Recorded here as RETIRED/obsolete; do not claim the prior-verifier criterion passed. |
| Banned terms: 0; Grok pins only | **MET WITH EXCEPTION.** Banned terms: 0 unallowed; exactly 3 allow-listed MotionSites lines (SKILL.md:25, :38; LICENSE:1) — the SPEC's "0" predates the MotionSites fetch-URL/license lines, which verify27 check 8 allows by content. Grok pins: 56 / 74 / 0 — exact. |
| Counts: 66 / 45 / 123 / 60 / 15; triggers 64 → 49; anchor tokens | **NOT MET as written on two numbers; exact on the rest.** Actuals 67 / 45 / 123 / 55 / 15; triggers 64 → 49 exact. Causes traced (MotionSites +1; 5 round-2 command cuts). Anchor tokens: 20 `_F27` (SPEC lists 11; +9 in rounds 2/3); census reconciles staged + built (92 / 113). |
| Manifest: disposition table, anchor tokens, open adjudications, dry-run caveat | **MET.** This file. |
| Builds: fix #26 env-redirected invocation; never re-run fix11 | **MET.** All 8 runs; fix11 never re-run; staged sources only; build.sh source of truth. |

## §5 Open parent adjudications

1. **Rules trim (follow-up debloat candidate).** Rules stay at 123 in this fix per
   SPEC §1(d). The ~80 per-language rule files for cut languages remain; their
   dangling skill pointers are pointer-style only (OWED-11/M7). A future fix may
   cut them — needs a parent decision (rule-cut changes the alwaysApply surface).
2. **install-modules.json / install-components.json left unpruned** (M-new-4).
   Upstream-catalog artifacts: machinery derives the live surface from `skills/` at
   load time and silently skips missing paths (plan.js:155–157); a paths-only prune
   would leave a misleading `skill-unified-memory` module still referenced by
   install-profiles.json:85. pi-core.json WAS pruned (93 → 30 skills, 24 → 18
   commands, asserted by verify27).
3. **Prior verifiers retired** (M-new-3/M11): verify26.py and verify25.py crash
   against the reduced tree — recorded as RETIRED/obsolete in §4, not passing.
4. **SPEC §7 counts superseded** (66/60 → actuals 67/55, causes traced in §4).
   The SPEC file itself was not rewritten; this manifest is the superseding record.
5. **Netlify row in deploy-fast needs a touch-up after Dec 4, 2026** (open from
   fix #26, carried — §8 non-goal, not re-litigated here).
6. **MotionSites vendored copy** contains zero promo/UTM content; if Anish wants
   the skill gone entirely, it is one staged skill + wiring lines to remove
   (`new-skills/motionsites-web-builder/` + DESIGNPKG-AUTO / PALETTE-FIRST mentions).
7. **Animaster Lib left out** by the free-tier rule; Anish can overrule if he wants
   it as inspiration-only (record: `fix27/animaster-fit-check.md`).

## §6 Owed / environment-limited items (recorded, not verified)

- **Live smoke test (skipped Nov 15 ~00:42, still the gate for live behavior):**
  live execution of the 55 commands, live invocation of the 67 on-request skills,
  live commit drafting via prp-commit, live recipes-lookup replacement
  (REROUTE_F27), live trigger firing, live Cursor behaviour of the ck wire — the
  sandbox runs prove the Node mechanics only.
- **Campus Eats benchmark dimension 7 (alignment): OWED, never passed.** No live
  Campus Eats render exists (`~/workspace/cold-start-render/campus-eats/` holds
  only `docs/design-tokens.md`). Per SPEC §8: RECORDED DECISION, not a pass.
- **Fix #17 R1/R4: OWED as defined.** Home Run implements iris-opens in a different
  placement and no hero loop; a live Campus Eats render implementing #67/#68 would
  be needed and none will be built (Anish's Nov 11 call).
- **Dry-run #42 runtime note:** narration runtime (84.1s) was estimated from
  voice durations — no voice provider in the sandbox; measured narration still owed.
- **Scratch artifact with stale prose (intentionally untouched):**
  `fix27/scratch/f27r3-verify27-12b-test.py:8–10` still carries the round-1 docstring
  ("166 -> 66 skills", "87 -> 60"). It is a round-3 test copy in scratch, not a live
  file; left as the historical record of that test run.

## §7 Push

- Remote: `github.com/anishkoduri/hackathon-ecc`, branch `main`. Pre-fix HEAD:
  `736c3667` (fix #26). **Do NOT push commit `b2444de`** (predates fixes #14–#25).
- Method: sync the working copy's changes into `fix27/scratch-repo` (restored from
  the fix #26 bundle), commit as Anish Koduri <akoduri05@gmail.com> with NO
  "Co-authored-by: Cursor" trailer and no AI tool listed as contributor/author,
  set remote to the GitHub URL, push, verify the new commit. Fresh bundle after
  the push.
- The push commit hash is verified by the coordinator after pushing and reported
  in the final report (this manifest is the pre-push record, per the fix #26
  convention — it does not contain its own commit's hash).
