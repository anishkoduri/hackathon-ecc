# Audit #75 — Fix #27, round 2 (re-audit after the Audit #74 fixes)

**Date:** Nov 16, 2026
**Auditor:** independent subagent audit (read-only; no plugin file edited, no build run, no generator run, no push, no fix11 re-run, no subagents)
**Scope:** the fix #27 updated repo in `~/workspace/hackathon-plugin/` — built tree `hackathon-ecc/`, staged sources (`new-skills/`, `rewritten-skills/`, `round2-skills/`, `new-rules/`), `fix27/SPEC.md`, `fix27/audit74-report.md`, `fix27/fix27.py`, `fix27/verify27.py`, `fix27/staged-patch-log.md`, `fix27/fix27-patch-log.md`, `fix27/fix27-round2-patch-log.md`, `fix27/animaster-fit-check.md`, `fix27/build-log-run4.txt`, `fix27/verify27-run2.log`, `fix25/callmap/generate_call_map.py`, `build.sh` wiring.
**Method:** read Audit #74 and the SPEC §7 criteria in full; read both patch logs, fix27.py's OWED list, and verify27.py in full; re-ran `verify27.py` myself; counted the built tree directly; re-read every Audit #74 B1–B15 and M1–M11 item in the built tree at its cited lines; ran my own CUT-name sweep over `skills/`, `agents/`, `commands/`, `rules/`, `scripts/`, `hooks/`, `manifests/` and `README.md`; read **every** one of verify27.py check-12's 102 whole-line + 1 name-scoped allow-list entries in context; spot-checked the MotionSites upstream URLs live (raw GitHub fetch) and the Animaster site live (homepage fetch Nov 16, 2026); re-ran the prior verifiers verify26.py / verify25.py.

## Verdict

**BLOCKING: 1, MINOR: 6**

Round 2 landed almost everything Audit #74 asked for: all 15 blocking items B1–B15 are fixed in the built tree (each verified at its cited lines below), all 11 minor items M1–M11 are fixed or correctly dispositioned except for two record gaps (M9, M11), the counts are exact, the call map is regenerated, and verify27.py passes 76/76 on my own re-run. The one failure is new, not a round-2 miss on an old item: **a live imperative dispatch to CUT `coding-standards` ships in a kept agent file, and verify27.py check 12 passes while it ships because the whole-line allow-list exempts the entire line** (`agents/ecc-typescript-reviewer.md:119`). That is a broken dispatch hidden by a verifier gap — blocking by this audit's definition. The six minor findings are stale pointers allow-listed instead of fixed, two stale OWED/record items, stale install manifests, one upstream-upsell leak at the MotionSites use-time fetch boundary, and one missing verifier assertion.

---

## BLOCKING findings

### B-new-1. Live imperative dispatch to CUT `coding-standards` in the kept evaluator agent — hidden by the check-12 whole-line allow-list

- `agents/ecc-typescript-reviewer.md:119` (full line, read in the built tree): "For detailed TypeScript and JavaScript patterns, use the `typescript-patterns` skill, plus `coding-standards` and `frontend-patterns` or `backend-patterns` based on the code being reviewed."

"Use the X skill" is an imperative routing instruction — the same verb class Audit #74 called BLOCKING in B15 ("check the X skill first", "use the X skill"). `coding-standards` was CUT in fix #27 (SPEC §1(a) REVIEW adjudication; `verify27.py` CUT_SKILLS; the dir is absent — the exact KEPT set of 67 skills is verified by check 1). An agent following this line tries to load a skill that does not exist. The other two names on the line (`typescript-patterns`, `frontend-patterns`/`backend-patterns`) are kept, so the line is a mixed line: one live dispatch to a removed skill bundled with kept ones.

Why the verifier misses it: `verify27.py` check 12 allow-lists this line whole (`ALLOW_LIST["agents/ecc-typescript-reviewer.md"][119]`, justified as "pointer: skills-list entry (M7 class)"), and the sweep exempts a whole line when any allow entry covers it. The line is not a skills-list entry — it is a "use the skill" instruction. The same whole-line mechanism is what the name-scoped `ALLOW_NAMES` entry for `rules/hackathon-mode.mdc:46` was designed to avoid (that line correctly allows only the negative names and still fails on a dispatch name). The whole-line allow for :119 does the opposite: it hides the dispatch.

This is also a verifier gap of the class M10 was created to close: check 12 passes 76/76 ("0 un-allow-listed, 103 allow-listed") while a live dispatch ships.

**Must change:** reword `agents/ecc-typescript-reviewer.md:119` to drop `coding-standards` (route to `typescript-patterns` + `frontend-patterns`/`backend-patterns` only — the kept stack that SPEC §1(a) says covers it), and remove the :119 whole-line allow-list entry from `verify27.py` (or convert it to a name-scoped entry only if a negative mention remains). Consider converting every whole-line allow entry that sits on a line mixing kept and CUT names to name-scoped allows, so this class cannot re-form.

---

## MINOR findings

### M-new-1. Dangling pointers allow-listed instead of fixed (check-12 residue, non-rules files)

The census found pointers Audit #74's M6 did not list, and round 2 allow-listed them rather than fixing them. None is an imperative dispatch — all are pointer-style — but each points at a removed dir, and the allow-list now permanently excuses them:

- `skills/polish-pass/reference/vercel-checklist.md:105, :108, :111, :115, :118, :121, :124, :127, :139, :146, :171` — 11 coverage citations to the removed `accessibility` skill, e.g. :115 "Covered in part by: `accessibility` skill:119 (\"Div-Buttons\")", :118 "`frontend-a11y` (alt); `accessibility` skill:122". The kept `frontend-a11y` skill is cited alongside on several of the same lines, so the re-point target already exists.
- `skills/react-patterns/SKILL.md:254` — cross-link `[skills/accessibility/SKILL.md](../accessibility/SKILL.md)`; `skills/react-performance/SKILL.md:566`, `skills/react-testing/SKILL.md:247, :359` — skills-list / cross-link entries naming `accessibility`.
- `agents/ecc-a11y-architect.md:148` — "See skill `accessibility` to transform raw UI requirements into platform-specific accessible code (WAI-ARIA, SwiftUI, or Jetpack Compose) based on WCAG 2.2 criteria." Pointer-style ("See skill"), but it sits in the agent's core workflow and names the removed skill as the source for its central transform.
- `agents/ecc-react-reviewer.md:161`, `commands/react-review.md:169`, `commands/react-test.md:263` — skills-list entries naming `skills/accessibility/`.

(The `rules/*.mdc` "See skill" pointers are NOT re-listed here — they are M7, correctly carried to the rules-debloat follow-up; see Checks.)

**Must change:** re-point `accessibility` → `frontend-a11y` (the kept a11y skill) or delete each pointer, and drop the corresponding allow-list entries. This is the same treatment round 2 gave the 10 M6 items.

### M-new-2. OWED-13 record is stale in two places (M9 carried, partially)

`fix27/fix27.py:936` / `fix27/fix27-patch-log.md:144` (OWED-13 CORRECTED):

1. It cites "the post-fix census (fix27/scratch/f27r2-census.txt, 101 allow-listed lines)". The allow-list now holds **102 whole-line entries + 1 name-scoped entry = 103** (counted from `verify27.py`'s `ALLOW_LIST`/`ALLOW_NAMES` literals; verify27.py itself reports "103 allow-listed"). The +1 whole-line entry is `skills/orchestrate/SKILL.md:136`, added by the coordinator after the census; it does not appear in OWED-13's enumeration at all.
2. Its final sentence still presents the 9 staged-owned dispatches as outstanding: "NOT prose-history — live dispatches owned by the staged worker this round: skills/orchestrate/SKILL.md:3 (B4), :65 (B1), :136 (B3), :138 (B1), skills/orchestrate/references/dispatch-prompt.md:24 (B1), rules/hackathon-mode.mdc:46 brainstorming (B12), :48 (B4), :53 (B12), :55 (B12)." All 9 have landed (verified in the built tree — see B1/B3/B4/B12/B14 below), so the standing record reads as if 9 live dispatches remain.

The "all prose-history" blanket claim itself is correctly gone (the text now says the round-1 claim "was wrong"), and OWED-1/4/5/6/12 are accurately recorded (see Checks). Only OWED-13's census count, its enumeration, and its closing sentence need updating.

**Must change:** update OWED-13 at manifest time (or in fix27.py + the patch log): 102 whole-line + 1 name-scoped allow-listed lines, add `skills/orchestrate/SKILL.md:136` to the enumeration, and reword the closing sentence to past tense (the 9 staged-owned dispatches landed in round 2).

### M-new-3. SPEC §7 prior-verifier criterion still unmet and still unrecorded as retired (M11 carried)

- Re-run by this auditor: `fix26/verify26.py` crashes — `FileNotFoundError: …/skills/django-verification/SKILL.md` (the dir fix27 removed); `fix25/verify25.py` crashes — `KeyError: 'skills'` at `second_order_orphans` (the regenerated call map changed shape). Same crashes as Audit #74.
- No record treats them as obsolete/retired. The only mentions are Audit #74's M11 and `fix27/fix27-round2-patch-log.md` Un-done #5 ("M11 prior verifiers … not in this worker's scope; not touched"). `fix27/fix27.py`'s OWED list and `fix27/fix27-patch-log.md` say nothing about them, and the manifest where M11 said to record the retirement does not exist (see SPEC §7 below).

Nothing claims the §7 prior-verifier criterion passed, so this is a record gap, not a false claim — minor.

**Must change:** record both verifiers as retired/obsolete against the reduced tree in `fix27/MANIFEST.md` when written (or update them to tolerate the removal); do not claim the §7 prior-verifier criterion passed.

### M-new-4. Install / Pi manifests still list removed skills and commands (stale, install-time only)

- `manifests/pi-core.json` `skills.include`: 93 entries, **63 of them CUT skills** (including `accessibility`, `agent-introspection-debugging`, `agent-self-evaluation`, `angular-developer`, `bengali-nlp`, `coding-standards`, `inherit-legacy-style`, `intent-driven-development`, `mcp-server-patterns`, `product-lens`, `vue-patterns`). Its `description` claims "skills.include lists the shipped subset only; upstream ECC catalog entries not shipped in this plugin were removed" — that claim is now false for the fix #27 cut.
- `manifests/pi-core.json` `commands.include`: 24 entries, **6 dropped commands** (`cpp-test`, `flutter-test`, `go-test`, `gradle-build`, `kotlin-test`, `rust-test`); the file also maps `learn-eval.md` (:369) and `project-init.md` (:382) as included commands.
- `manifests/install-modules.json`: mentions all 100 CUT skill names (module path catalog).
- `manifests/install-components.json`: 5 CUT skill mentions (`coding-standards`, `continuous-learning`, `unified-memory`, `vue-patterns`, `windows-desktop-e2e`).

Judgment: minor, not blocking. No Cursor-runtime code reads `pi-core.json` (the only references in the built tree are the call map's `[shipped]` evidence rows, which by the map's own method "do NOT count as an invocation"); `install-modules.json` / `install-components.json` are read only by install-time machinery (`scripts/lib/install-manifests.js:233-250`, `scripts/lib/install/plan.js:37`), not by the Cursor plugin path. The SPEC §1(b) mechanism never tasked fix27 with pruning these manifests. This is stale install-time metadata, same class as Audit #74's M3/M5 — not a live dispatch.

**Must change:** prune `pi-core.json` `skills.include` (63 CUT) and `commands.include` (6 dropped) to the kept set and reconcile `install-modules.json` / `install-components.json`, or record the three manifests as unpruned upstream-catalog artifacts in the manifest.

### M-new-5. MotionSites promo-stripping is partial at the use-time fetch boundary

The vendored skill itself is clean (see §3 below: the only banned-term hits are the 3 allow-listed lines; no upgrade block, no UTM link, no upsell nudge in the shipped copy). But its step 2 instructs the agent to fetch the upstream `examples/INDEX.md` at use time, and that upstream file — fetched live by this auditor — carries the upsell the vendoring stripped:

- `https://raw.githubusercontent.com/Motionsites-AI/claude-skill/main/plugins/motionsites-web-builder/skills/motionsites-web-builder/examples/INDEX.md:6-7`: "> These are a free sample. MotionSites Unlimited has 500+ premium prompts like these, plus animated backgrounds, section prompts, 40+ Lovable templates and the MotionSites MCP: [Go Unlimited](https://motionsites.ai/unlimited?utm_source=claude-skill&utm_medium=skill&utm_campaign=web-builder&utm_content=examples-index)"

The vendored SKILL.md:6 framing header promises "This plugin never appends sponsor, upsell, or promotional blocks or links to a delivery" — reading the fetched index does not append anything to a delivery, so the letter of the promise holds, but the agent will see the "Go Unlimited" UTM upsell in context on every use of the skill's step 2. The stripping is complete in the shipped tree and incomplete at the use-time boundary.

**Must change:** add one line to vendored `SKILL.md` step 2 telling the agent to ignore the Unlimited upsell block in the fetched index (free sample only), or have step 2 fetch the individual `examples/<name>.md` files without the index header. No change to the vendored copy's own text is needed — it is already clean.

### M-new-6. verify27.py has no assertion on the coordinator-added `memory-learning-skill` re-point

`scripts/harness-audit.js:522-529` (`memory-learning-skill` check, id kept) was correctly re-pointed from removed `skills/continuous-learning-v2/SKILL.md` to kept `skills/growth-log/SKILL.md` (verified in the built tree — see B7 below). But verify27.py check 10b asserts only the `security-scan-command` re-point; nothing asserts the `memory-learning-skill` one, and check 12 does not sweep `scripts/`. A later rebuild that reverts the re-point would pass 76/76 silently — the same verifier-gap shape as B-new-1, on a check that fails by design when wrong.

**Must change:** add a check-10b assertion for the `memory-learning-skill` check (id kept, `path: 'skills/growth-log/SKILL.md'`, `pass: fileExists(rootDir, 'skills/growth-log/SKILL.md')`).

---

## Audit #74 BLOCKING B1–B15 — all verified fixed

### B1. `inherit-legacy-style` re-routes (9 copies) — FIXED

Zero hits for `inherit-legacy-style` anywhere in `skills/`, `agents/`, `commands/`, `rules/` (grep, built tree). All 9 copies carry the re-route: orchestrate SKILL.md:65 (step 3) and :138 (row-10 rule), `skills/orchestrate/references/dispatch-prompt.md:24`, `skills/orch-add-feature/SKILL.md:33`, `skills/orch-build-mvp/SKILL.md:41`, `skills/orch-change-feature/SKILL.md:36`, `skills/orch-fix-defect/SKILL.md:36`, `skills/orch-refine-code/SKILL.md:35`, `skills/ui-ux-pro-max/SKILL.md:363` — each now reads "handled inside the design package — no separate skill (fix #27, REROUTE_F27)". verify27.py B1 checks pass (6/6).

### B2. Theme cage lifted in orch-build-mvp:43 + ui-ux-pro-max:274 — FIXED

Both E1 blocks read verbatim (read in full): bound (2) now "fit the theme's material world — material, tokens, palette balance, do-nots — **or a recorded departure from it** (D19 reason required) (fix #27, THEME-START_F27)"; the new-theme clause is deleted ("NOT within reason: a new palette …" only); the inversion sentence is present ("Inventing a theme direction is a recorded D19 decision, not a forbidden move (fix #27, THEME-START_F27)"). Zero "a new theme (re-deal" hits remain in either file. Matches the fixed copies in orchestrate:148 / design-taste-frontend:423.

### B3. `ecc-recipes` re-route (orchestrate:136) — FIXED

Built `skills/orchestrate/SKILL.md:136` (read in full; staged `new-skills/orchestrate/SKILL.md:136` is byte-identical): "**Multi-command pipeline lookup (fix #27, REROUTE_F27 — `ecc-recipes` was cut).** When a run needs a multi-command pipeline and the orchestrator does not already know which command group runs it, read the `commands/` directory directly…". The shipped line names no CUT skill/command as a dispatch: the only CUT name is `ecc-recipes` inside the "(… was cut)" note; the coordinator's reword dropped the "continuous-learning families" and "`/prune`" references (neither string appears on the line — verified), and the epic-* guard names only kept commands (`/epic-decompose`, `/epic-claim`, `/epic-validate`, `/epic-review`, `/epic-unblock`, `/epic-sync`, `/epic-publish`).

### B4. `dispatching-parallel-agents` re-routes — FIXED

- `skills/orchestrate/SKILL.md:3` (frontmatter description): "Do NOT use for concurrent failure investigation (the orchestrator's own parallel dispatch owns that — fix #27, REROUTE_F27)".
- `rules/hackathon-mode.mdc:48` (§6): "The orchestrator's own parallel dispatch is for concurrent failure investigation (fix #27, REROUTE_F27)."

### B5. prp-commit → git-workflow — FIXED

`commands/prp-commit.md:59`: "Draft the message with the `git-workflow` skill (`skills/git-workflow/SKILL.md`)…". Zero `conventional-commit-review` hits in the file.

### B6. projects / promote / prune / learn-eval / project-init CUT; skill-create CLv2 sections gone — FIXED

- Dirs/files absent: `skills/continuous-learning-v2/`, `commands/projects.md`, `commands/promote.md`, `commands/prune.md`, `commands/learn-eval.md`, `commands/project-init.md` (all `ls: cannot access`).
- `commands/skill-create.md`: zero hits for `instinct`, `continuous-learning-v2`, `skill-scout` (the `--instincts` flag line, the "Optionally Creates Instincts" step, the Step 4 CLv2 section, and the Related Commands instinct lines are all gone).
- `commands/ecc-guide.md`: zero `/project-init` hits (the :85 pointer is gone); `commands/epic-sync.md`: zero `/projects` hits (the compatibility alias is gone).
- Bonus fix verified: `commands/skill-health.md:46` now reads "suggest running /learn" (was `/evolve`).

### B7. `/security-scan` pointers → security-review; harness checks re-pointed — FIXED

- `commands/ecc-guide.md:89`, `commands/fastapi-review.md:39`, `commands/harness-audit.md:2`, `rules/react-native-security.mdc:43` all now name the `security-review` skill. Zero `security-scan` hits remain in `skills/`, `agents/`, `commands/`, `rules/` (the only hit in the whole built tree is the check id below).
- `scripts/harness-audit.js:582-589`: `security-scan-command` check re-pointed — `path: 'skills/security-review/SKILL.md'`, `description: 'Security review skill exists'`, `pass: fileExists(rootDir, 'skills/security-review/SKILL.md')`, `fix: 'Add skills/security-review with the security review workflow.'` — check id `'security-scan-command'` kept.
- Coordinator-added extension verified: `scripts/harness-audit.js:522-529` `memory-learning-skill` check re-pointed from removed `skills/continuous-learning-v2/SKILL.md` to kept `skills/growth-log/SKILL.md` (`path`/`pass`/`fix` all name growth-log), id `'memory-learning-skill'` kept. (No verify27 assertion covers this re-point — see M-new-6.)

### B8. council santa-method → verification-loop / production-audit — FIXED

- `skills/council/SKILL.md:37`: "… at the end of the project: `verification-loop` / `production-audit`".
- `skills/council/SKILL.md:40`: "`code-reviewer` or, at the end of the project, `verification-loop` / `production-audit`".
- Related Skills: zero `santa-method` and zero `architecture-decision-records` hits in the file (both lines deleted).

### B9. integration re-routes — FIXED

- `skills/integration/SKILL.md:21`: "hand-roll the client via `api-integration` (fix #27, REROUTE_F27 — `mcp-server-patterns` was cut)".
- `:46`: "Use `documentation-lookup` (grep-and-read over the plugin's own skill list) … (fix #27, REROUTE_F27 — `skill-scout` was cut)".
- `:60`: "Use a hand-rolled client via `api-integration` … (fix #27, REROUTE_F27 — `mcp-server-patterns` was cut)".
- `:122`: composition list names only kept skills (`documentation-lookup`, `api-integration`, …) with "(fix #27, REROUTE_F27 — `skill-scout` and `mcp-server-patterns` were cut)".

### B10. ai-feature-spec → hackathon-scope — FIXED

`skills/ai-feature-spec/SKILL.md:3` (frontmatter description): "For non-AI features use hackathon-scope; for API contracts use contract-first." Zero `intent-driven-development` hits in the file.

### B11. ecc-agent-evaluator self-contained — FIXED

Zero `agent-self-evaluation` hits in `agents/ecc-agent-evaluator.md`. The rubric is genuinely inline, not just de-referenced: `:20` "Score agent output on 5 axes: Accuracy, Completeness, Clarity, Actionability, Conciseness"; `:54` "Work through the 5 axes defined below:" followed by the five axes with per-axis scoring instructions (:54-58) and the report format (:69 "Use this exact format (defined in this file):", :110 "matching the output format defined in this file exactly").

### B12. hackathon-mode §6 + mobile-ship:9 re-routes — FIXED

- `rules/hackathon-mode.mdc:46` (§6): "`feature-expansion` owns later ideation on a specific feature or problem (fix #27, REROUTE_F27)" (was `brainstorming`).
- `:53`: "Writing screens or features belongs to `react-native-patterns` (fix #27, REROUTE_F27)" (dart-flutter-patterns dropped).
- `:55`: "Grep-and-read / `ecc-code-explorer` is the kept exploration path … (fix #27, REROUTE_F27)" (was `codebase-memory` owns …).
- `skills/mobile-ship/SKILL.md:9`: "belongs to react-native-patterns." (dart-flutter-patterns dropped).

### B13. systematic-debugging description — FIXED

`skills/systematic-debugging/SKILL.md:3`: "… after symptom inspection rules out an agent failure and broken-button state bugs (click-path-audit)." The `(agent-introspection-debugging)` parenthetical is gone; zero hits in the file.

### B14. hackathon-mode §7 vs orchestrate:57 contradiction — RESOLVED (they now agree)

Read both texts in full:

- `skills/orchestrate/SKILL.md:57`: "If the check finds no record and no explicit skip, that is itself a finding (fix #27, GRILLHDR_F27): state in the first reply that grill-me did not run and why (no trigger / no record), and ask the user whether to grill now (one prompt) or proceed — the one-question exception to §7. Do not silently proceed on a raw prompt."
- `rules/hackathon-mode.mdc:60` (§7 precondition): "If neither holds, do not auto-approve with zero recorded decisions and no check, and do not silently proceed on the raw prompt: state in the first reply that grill-me did not run and why (no trigger / no record), and ask the user whether to grill now (one prompt) or proceed — the one-question grill-now-or-proceed ask, the second one-question exception to §7 alongside the deliverable-at-risk flag (fix #27, GRILLHDR_F27). Do not re-run `grill-me` unasked." The same paragraph's "do not ask the user anything" now reads "(except the one-question grill-now-or-proceed ask above)".
- `rules/hackathon-mode.mdc:62` (§7 override): "§7 overrides any ask/stop/wait instruction … — except the one-question grill-now-or-proceed ask above (fix #27, GRILLHDR_F27)."

Both texts now say the same thing: no silent proceed; state grill-me-missed in the first reply; one grill-now-or-proceed question; that question is carved out of §7's override. The contradiction is resolved.

### B15. skill-create / skill-health descriptions — FIXED

- `commands/skill-create.md:3`: "… check the plugin's own skill list (grep-and-read) first to avoid duplicating an existing local, marketplace, or GitHub skill."
- `commands/skill-health.md:3`: "… for a qualitative compliance or quality audit use the plugin's own skill list and verify scripts."

---

## Audit #74 MINOR M1–M11 — all fixed or correctly dispositioned (except M9/M11 record gaps)

### M1. W2 gate qualification — FIXED

- `skills/orchestrate/SKILL.md:295`: "**Fire on any one signal — only when the gate above is met (fix #27, W2_F27):** …" (gate not widened).
- `skills/orchestrate/references/patterns.md:28`: "… launch two deep-reasoner passes blind, then reconcile — only when the gate above is met (first pass flagged genuine uncertainty, or two genuinely different priors exist) (fix #27, W2_F27)."

### M2. NOCOAUTHOR in orchestrate step 6 — FIXED

`skills/orchestrate/SKILL.md:104` (step 6): "The commit-message check also fails a commit carrying a `Co-authored-by:` trailer for any AI tool (including Cursor) or naming any AI tool as author or contributor; the commit author is the user (fix #27, NOCOAUTHOR_F27)." The rule itself remains correct in `rules/common-git-workflow.mdc:16`.

### M3. Trigger notes — FIXED

`manifests/context-packs/skill-triggers@1.json` `notes`: "Deferred: verification-loop, production-audit, delivery-gate. (DEFER3_F27)" — only the three kept checks; zero `codehealth-mcp` / `santa-method` / `security-scan` in the notes. Trigger keys 49, coverage.skills 67 (verified by count).

### M4. delivery-gate "shipped" claims — FIXED

`skills/delivery-gate/SKILL.md:13, :15, :111` reworded to past tense ("the former `agent-self-evaluation` skill — cut in fix #27; its 5-axis rubric now lives in the `ecc-agent-evaluator` agent file") and the reasoning-quality-gate entry now points at `ecc-agent-evaluator`. Zero "shipped" claims remain (grep).

### M5. README — FIXED

- Marketplace list (`README.md:26-27`) now names only `systematic-debugging`, `verification-before-completion`; zero `brainstorming` / `dispatching-parallel-agents` / `agents-md-generator` in the file.
- `README.md:29`: "`codebase-memory` was cut in fix #27 and is not shipped. Explore unfamiliar code with grep-and-read and the `ecc-code-explorer` agent instead…".
- Deferred set (`README.md:54-56`): "`verification-loop`, `production-audit`, and `delivery-gate`"; zero `/security-scan` in the file. Counts read 67/55 throughout; the stock-ECC line (144/69) is untouched by design. (The `:11` "codebase-memory MCP servers" line was deliberately left alone — it describes the stock ECC profile, where the server genuinely ships; Audit #74 did not list it.)

### M6. Dangling pointers (all 10) — FIXED

Verified each: `contract-first` (`ai-regression-testing` :15/:284 gone), `ecc-database-reviewer` (`database-migrations` gone, "see skill: `postgres-patterns`."), `tdd-workflow` (`bun-runtime` gone), `postgres-patterns` (`clickhouse-io` gone), `react-patterns` (accessibility/angular-developer links gone), `typescript-patterns` (`nestjs-patterns`/`prisma-patterns` gone), `react-native-patterns` (`coding-standards` gone), `council` (`architecture-decision-records` gone, see B8), `strategic-compact` (`continuous-learning` → "`/learn` command"), `scripts/lib/resolve-ecc-root.js:25` (sentinel now `path.join('skills', 'orchestrate')`, comment records the move from continuous-learning-v2). All 10 verify27 M6 checks pass.

### M7. Rules pointers — CORRECTLY DISPOSITIONED (carried, not fixed)

`fix27/fix27.py:934` (OWED-11): "Rules are NOT cut in this fix (SPEC §1(d)); left alone — carried to the rules-debloat follow-up. Pointer-style only, not dispatches (audit #74 M7)." The record says exactly what Audit #74 asked it to say. The pointers remain (verified: e.g. `rules/react-patterns.mdc:194`, `rules/angular-patterns.mdc:249` and the full per-language set in the check-12 allow-list) — that is the expected state, not a failure.

### M8. slop-checklist departure allowance — FIXED (header-note option)

`skills/polish-pass/reference/slop-checklist.md:27` (Theme-match precondition): "… A D19-recorded departure satisfies the fit criterion (fix #27, THEME-START_F27)." The six per-check lines were deliberately left unedited; the header note governs them, which is the option Audit #74 allowed.

### M9. OWED-record corrections — MOSTLY FIXED, one stale item (see M-new-2)

- The "all prose-history" blanket claim is gone: OWED-13 now opens "CORRECTED (round 2): the round-1 blanket claim ('All are prose-history or single-mention references') was wrong" and names the re-routed dispatches (B1/B8/B9/B10/B13).
- OWED-1 (call map regenerated — verified, see §6), OWED-4 (all CLv2 commands dropped incl. projects/promote/prune; learn KEPT; learn-eval/project-init dropped — verified, see B6), OWED-5 (evaluator rubric inline — verified, see B11), OWED-6 (feature-expansion re-routed — verified via check 12), OWED-12 (staged worker landed B12/B14 — verified in the built tree) are all accurately recorded in `fix27/fix27.py:924-936` and `fix27/fix27-patch-log.md:132-144`.
- Remaining: OWED-13's census count/enumeration and its closing sentence are stale — see M-new-2.

### M10. verify27 check 12 — EXISTS AND PASSES, but the allow-list hides one live dispatch (see B-new-1)

- Re-ran `verify27.py` myself: **76/76, exit 0** (matches `fix27/verify27-run2.log`). Check 12 reports "0 un-allow-listed, 103 allow-listed, 294 generic bare-word noise lines".
- The CUT-name sweep exists (two tiers: STRONG for every name, BARE for non-generic names) and passes.
- I read **every** allow-listed line in context (102 whole-line entries across 52 files + 1 name-scoped entry, counted from the `ALLOW_LIST`/`ALLOW_NAMES` literals; total 103, matching the sweep's own count). Classification: prose-history / "was cut" notes (delivery-gate :13/:15/:111, feature-expansion :49/:100/:188/:190/:192/:193/:204, integration :21/:46/:60/:122, orchestrate:136), negatives (ecc-spec-miner :3/:40/:201, learn.md:2, hackathon-mode :37/:38, name-scoped :46 product-lens/intent-driven-development), generic-verb/attribution (feature-expansion :3/:211), data (icon ids, search keywords, test fixtures), and pointer-style lines — **except one**: `agents/ecc-typescript-reviewer.md:119`, which is an imperative "use the `coding-standards` skill" dispatch (see B-new-1). The remaining pointer-style lines are M-new-1.
- The new `skills/orchestrate/SKILL.md:136` allow-list entry is genuinely prose-history only (see B3) — correctly allow-listed.

### M11. Prior verifiers — crashes confirmed; retirement unrecorded (see M-new-3)

`fix26/verify26.py` crashes (`FileNotFoundError: …/skills/django-verification/SKILL.md`); `fix25/verify25.py` crashes (`KeyError: 'skills'` at `second_order_orphans`). Same as Audit #74. The record still does not treat them as obsolete/retired — see M-new-3.

---

## MotionSites (new skill) — verified, with one use-time-boundary note

**(a) Promo stripped?** Yes, in the vendored copy. Grep over `skills/motionsites-web-builder/` for upgrade-block / UTM / Unlimited marketing returns only: the framing header's own disclosure of the removal (`SKILL.md:6`, not a finding — it states the "Sponsored by MotionSites" section, upgrade block, upsell nudges and UTM-link rule were removed), two prohibitions ("never the paid MotionSites Unlimited library", "never use premium/paid MotionSites content" — `SKILL.md:6, :36`), and non-promo uses of the words ("Upgrade an existing page" is a use-case heading, `SKILL.md:70`; "Premium parameters" / "premium heroes" are technique adjectives in `references/techniques/`; "Pricing (material, toggle)" in `references/spec-template.md:136` is a UI component of a site being built). Zero UTM links, zero "Sponsored by", zero upsell nudges in the shipped copy. Caveat: the use-time fetch re-introduces an upsell — see M-new-5.

**(b) License boundary.** `examples/` and `media/` are NOT vendored: the built skill contains exactly `SKILL.md`, `references/` (7 files incl. `techniques/`), `scripts/shoot.py`, and `LICENSE` — 16 files, no `examples/`, no `media/`. The framing header (`SKILL.md:6`) states the MIT parts only and that `examples/`/`media/` are © MotionSites and not shipped. The upstream references are well-formed raw GitHub URLs pointing at the upstream repo: `https://raw.githubusercontent.com/Motionsites-AI/claude-skill/main/plugins/motionsites-web-builder/skills/motionsites-web-builder/examples/INDEX.md` (`SKILL.md:25`) and `…/media/MEDIA.md` (`SKILL.md:36`). The examples URL was fetched live by this auditor and resolves (200): the upstream index lists "The 40 most-liked free prompts on motionsites.ai" with 40 entries.

**(c) Build wiring.** `build.sh:217` includes `motionsites-web-builder` in the new-skills loop (`for s in grill-me feature-expansion integration design-taste-frontend codebase-memory motionsites-web-builder; do`). The built tree contains `skills/motionsites-web-builder/` with the cleaned `SKILL.md` (promo stripped per (a)).

**(d) DESIGNPKG-AUTO lists it in both files.** `skills/orchestrate/SKILL.md:35` and `rules/hackathon-mode.mdc:44` both list `motionsites-web-builder` in the design-package skill list and carry the gloss "`motionsites-web-builder` — cinematic components, motion patterns, hero treatments and media (free sample only; consulted, never a template) (fix #27, MOTIONSITES_F27)."

**(e) Check-8 allow-list: exactly the 3 lines, all genuinely un-rewordable.** Banned-term grep over the whole skill dir returns exactly `SKILL.md:25`, `SKILL.md:36`, `LICENSE:1` — the same 3 lines in `verify27.py`'s `CHECK8_ALLOW`. :25 and :36 are raw-GitHub fetch URLs carrying the upstream repo name `claude-skill` (rewording breaks the fetch); `LICENSE:1` is the upstream license title "MotionSites Web Builder — Claude skill" (the MIT notice ships verbatim). No other banned-term hits exist in the skill.

**(f) builders.md reword landed.** `skills/motionsites-web-builder/references/builders.md:10` reads "| **Cursor** | …" (was "Cursor / Claude Code"). Zero "Claude Code" hits remain in the staged skill or the built copy.

---

## Palette-first (token PALETTE-FIRST_F27) — verified

- Token present in all three files: `skills/design-taste-frontend/SKILL.md:224`, `skills/orchestrate/SKILL.md:35`, `rules/hackathon-mode.mdc:44` (verify27.py's three PALETTE-FIRST checks pass).
- Ordering in design-taste-frontend: the palette step sits at :224 — "**Palette first — inventory the available components BEFORE the direction is finalized (fix #27, PALETTE-FIRST_F27).** Before any deal in this step — before the Hallmark theme deal and before the palette deal below — the design-lead inventories the available component palette FIRST and bases the design direction on it…". The Hallmark theme deal is at :258 ("Deal a Hallmark theme for the direction first") and the step-4a freeze at :413 ("Define the design system before building any UI"). The inventory step is before every direction-finalization step. The palette listed is MotionSites + the design package + the dealt Hallmark theme.
- Audit hook stated in all three: each file carries "The audit checks the design-direction record names the palette components used (sources + components + tailoring); a direction with no palette attribution is a finding" (design-taste-frontend:224, orchestrate:35, hackathon-mode:44).
- "Animaster" appears in none of the three files (grep count 0 in each).

---

## Animaster (left out) — verified justified

- Not wired anywhere: grep for `animaster` (case-insensitive) over the built tree (`skills/`, `agents/`, `commands/`, `rules/`) and the staged sources (`new-skills/`, `rewritten-skills/`, `round2-skills/`, `new-rules/`) plus `build.sh` and `fix27/*.py` returns zero hits. The only hits in the repo are `fix27/animaster-fit-check.md` and the `staged-patch-log.md` record of the decision.
- Leave-out justified — spot-checked live against the site. Fetched `https://animmasterlib.dev/` Nov 16, 2026 (crawled 26 min before the fetch): "300 PRO UI COMPONENTS FOR MODERN WEB PRODUCTS"; pricing PRO $10 struck through → **$4.99**, Premium $20 struck through → **$8**; FAQ verbatim: "This is a one-time purchase with access to materials for a lifetime", "This is code, all components built from scratch, tested and optimized", "You'll receive access to a Google Drive folder containing all the components", "60% of components are HTML, CSS, JS / 30% React / 10% Next JS". No free tier, free sample, or free download anywhere in the 720-line fetch — only thumbnail gallery previews. The fit-check's prices, FAQ quotes, and "effectively fully paywalled" verdict are all confirmed against the live site. Leaving it out (and out of the PALETTE-FIRST palette) is the correct call under the standing free-tiers-only rule.

---

## Counts + call map — verified

- Counted the built tree directly: **67 skills / 45 agents / 123 rules / 55 commands**; `hooks/hooks.json` has **15 hook entries** (the `hooks/` dir lists 17 files because it also contains `hooks.json` itself and `adapter.js`); trigger keys **49**, coverage.skills 67 (read from the trigger file).
- Build run 4: `fix27/build-log-run4.txt` records "fix27: 89 change(s)", "fix27: 13 OWED item(s) recorded in the patch log", "fix27: OK", then STEP 5 counts 67/45/123/55, hooks 15, "build complete". `fix27/fix27-patch-log.md` records "## Errors (0)", "skills removed: 100 dirs", "commands dropped: 32 files".
- Call map regenerated from the reduced tree: counts table `skills/orchestrate/references/call-map.md:8-14` reads 67/45/123/55/15/49 (all "Expected" matching); **no rows for the 5 cut commands** (grep for `learn-eval`, `project-init`, `/projects`, `promote`, `prune` over the call map returns zero hits — no rows at all, not even historical notes); `motionsites-web-builder` row present at :104 with STRONG invokers (`rules/hackathon-mode.mdc`, `design-taste-frontend/SKILL.md`, `skills/orchestrate/SKILL.md`, each built + staged); B6 DOCUMENTATION-ONLY note intact at :38; staged md5 == built md5 **`8879cb900933e9032486da78ad7ac34b`** (checked both `new-skills/orchestrate/references/call-map.md` and the built copy).

---

## SPEC §7 criteria — judged

| Criterion | Verdict | Evidence |
|---|---|---|
| Audit #74 (or next number): ZERO blocking, ZERO minor | **NOT MET** | This audit (#75): BLOCKING 1, MINOR 6. |
| Sweep #35 (or next number): CLEAN, weaving-coherence CLEAN | **NOT MET** | No sweep file exists in `fix27/` (no `MANIFEST.md`, sweep, or dry-run files at all as of this audit). |
| Dry-run #42 (or next number): PASS | **NOT MET** | No dry-run file exists in `fix27/`. |
| verify27.py: checks for every placement, exit 0 | **MET** | 76/76, exit 0, re-run by this auditor (matches `verify27-run2.log`). One gap remains inside it: no assertion on the `memory-learning-skill` re-point (M-new-6), and the whole-line allow-list hid B-new-1. |
| Prior verifiers: fails only the codified tails | **NOT MET** | verify26/verify25 crash (see M-new-3); retirement unrecorded. |
| Banned terms: 0 in the built tree | **MET with the allow-listed exception** | 0 except the 3 MotionSites lines (SKILL.md:25, :36; LICENSE:1), each genuinely un-rewordable (see §3(e)). |
| Grok pins only | **MET** | `grok-4.7-high` ×56, `cursor-grok-4.6-high-fast` ×74, bare `grok-4.6-high-fast` ×0 (verify27 check 9, re-run). |
| Counts: 67 / 45 / 123 / 55, hooks 15, triggers 49 | **MET** | Counted directly (see §6). |
| Anchor tokens: 20 `_F27` tokens | **MET** | All 20 present (verify27 check 7, re-run). |
| Manifest: fix27/MANIFEST.md | **NOT MET** | Does not exist yet. |

The manifest, sweep #35, and dry-run #42 do not exist yet — that is an open item, not a blocking finding on the tree itself (the tree is what this audit judges; the missing verification artifacts are recorded here and in Open items).

---

## Held-command check (learn / learn-eval / project-init)

- **learn — KEPT, confirmed.** `commands/learn.md` exists; its description distinguishes itself from the removed CLv2 system. No change needed.
- **learn-eval — CUT, confirmed.** File gone. Zero pointers to it in `skills/`, `agents/`, `commands/`, `rules/` outside the call map (grep empty); the call map itself has no row for it at all (regenerated from the reduced tree).
- **project-init — CUT, confirmed.** File gone. Zero pointers to it in `skills/`, `agents/`, `commands/`, `rules/` outside the call map (the `commands/ecc-guide.md:85` pointer was removed in round 2 — verified, zero hits); the call map has no row for it. Its example naming a removed skill goes with the file.
- The only remaining mentions of either command anywhere in the built tree are `manifests/pi-core.json:369` (`learn-eval.md`) and `:382` (`project-init.md`) — part of the manifest staleness in M-new-4, not live dispatches.

---

## Checks passed (verified clean, with evidence)

1. **verify27.py re-run by this auditor: 76/76, exit 0** (same as `fix27/verify27-run2.log`).
2. **Counts + exact dir sets:** 67/45/123/55, hooks 15, triggers 49; skill dir set exactly the 67 KEPT skills; all 100 CUT skill dirs, 27 removed agents, 32 dropped commands absent (verify27 checks 1–4 + direct listing).
3. **All 20 `_F27` tokens present**, including MOTIONSITES_F27 and PALETTE-FIRST_F27 in their three files each.
4. **All 15 Audit #74 blocking items fixed** (B1–B15, each re-read at its cited lines above).
5. **M1–M8, M10 (sweep exists/passes) fixed; M7 correctly dispositioned** (rules carried to the debloat follow-up per OWED-11).
6. **Call map regenerated** (counts table, no cut-command rows, motionsites row with STRONG invokers, B6 note intact, staged md5 == built md5 `8879cb900933e9032486da78ad7ac34b`).
7. **MotionSites vendoring clean** (promo stripped in the shipped copy, MIT parts only, examples/media absent, URLs resolve live, build.sh loop includes it, DESIGNPKG-AUTO lists it in both files, check-8 allow-list exactly the 3 un-rewordable lines, builders.md reword landed).
8. **Palette-first ordering verified** (:224 before the :258 theme deal and the :413 freeze; audit hook in all three files; no Animaster in any of the three).
9. **Animaster leave-out justified** (zero wiring; prices/FAQ/no-free-tier verified live against animmasterlib.dev).
10. **Banned terms 0** except the 3 allow-listed MotionSites lines; **Grok pins only** (56/74, bare 0).
11. **Checked and NOT a finding:** CLv2 hook machinery (`scripts/hooks/observe-runner.js:9` references `skills/continuous-learning-v2/hooks/observe.sh`; `scripts/hooks/posttooluse-dispatcher.js:5` states "Not wired in this Cursor plugin — it never runs"; `scripts/lib/observer-sessions.js:143` mentions `instinct-cli.py` in a string) — dead/unwired code, same classification as Audit #74; the staged-vs-built `orchestrate:136` text is byte-identical; the `README.md:11` "codebase-memory MCP servers" line remains by design (stock-profile description, not listed by Audit #74).

## Open items carried forward

- **Manifest / sweep / dry-run still to run:** `fix27/MANIFEST.md` does not exist; Sweep #35 (CLEAN, weaving-coherence CLEAN) and Dry-run #42 (PASS) have not run. SPEC §7 requires all three. The OWED-13 corrections in M-new-2 and the verifier retirements in M-new-3 should be folded into the manifest when written.
- **Rules (123) NOT cut** — per SPEC §1(d), the per-language rule families for cut languages remain a follow-up debloat candidate; their dangling skill pointers are M7 (record verified accurate in OWED-11).
- **Prior verifiers** — verify26.py / verify25.py are obsolete against the reduced tree (M-new-3); decide whether to update them or record them as retired in the manifest.
- **Install / Pi manifests** — prune or record as unpruned (M-new-4).
- **Netlify row touch-up** (due after Dec 4, 2026) — unchanged, still open from fix #26.

## Verdict

**NOT PASS — BLOCKING: 1, MINOR: 6.** Do not push until B-new-1 is re-routed (drop `coding-standards` from `agents/ecc-typescript-reviewer.md:119` and fix the check-12 allow-list entry that hid it) and M-new-1–M-new-6 are dispositioned. Everything Audit #74 blocked on is fixed; the single blocker is a new live dispatch the round-2 census allow-listed instead of catching.
