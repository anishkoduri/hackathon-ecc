# Audit #74 — Fix #27 (debloat + weekend lessons)

**Date:** Nov 16, 2026
**Auditor:** independent subagent audit (read-only; no plugin file edited, no build run, no generator run, no push, no fix11 re-run)
**Scope:** the fix #27 updated repo in `~/workspace/hackathon-plugin/` — built tree `hackathon-ecc/`, staged sources (`new-skills/`, `rewritten-skills/`, `round2-skills/`, `new-rules/`), `fix27/SPEC.md`, `fix27/skill-inventory.md`, `fix27/weekend-audit.md`, `fix27/fix27.py`, `fix27/verify27.py`, `fix27/staged-patch-log.md`, `fix27/fix27-patch-log.md`, `fix27/build-log-run2.txt`, `fix25/callmap/generate_call_map.py`, `build.sh` wiring.
**Method:** read the SPEC, inventory, weekend audit, both patch logs, fix27.py, and verify27.py in full; re-ran `verify27.py` myself; counted the built tree directly; ran a full CUT-name sweep (all 100 CUT skill names) over the built tree excluding only the regenerated call map and the trigger manifest, then read every remaining mention in context to classify live dispatch vs prose history; spot-checked every token location; diffed staged vs built copies of the 7 staged-edited files; checked build-log-run2 and re-ran the prior verifiers verify26.py / verify25.py.

## Verdict

**BLOCKING: 15, MINOR: 11**

The debloat itself landed cleanly (counts exact, all 100 CUT skill dirs gone, call map regenerated, all 18 tokens present, verify27.py 37/37 on re-run). What did **not** land is the reference cleanup the cut requires: **14 live dispatches to removed skills/commands still ship in kept files**, plus **one direct contradiction between two shipped rules** (hackathon-mode §7 vs orchestrate:57 on the grill-me-missed question). The pattern is systematic, not a typo: the fix removed the skill dirs and re-routed only the copies its workers owned (feature-expansion, orchestrate's commit line, security-review, the deferred lists), while identical dispatch lines in ECC-origin files (orch-*, ui-ux-pro-max, council, integration, prp-commit, the CLv2 commands, harness-audit.js) and in the staged-owned hackathon-mode.mdc §5/§6 were never touched — and OWED-13 mis-recorded most of them as "prose-history". The fix must not push until the blocking items are re-routed or removed.

---

## BLOCKING findings

### B1. Live dispatch to CUT `inherit-legacy-style` in the design-package rule family — 9 locations

`inherit-legacy-style` was CUT (inventory: fresh builds have no legacy codebase), but the design-package rule still routes legacy-drift work to it in every copy of the rule:

- `skills/orchestrate/SKILL.md:138` (row 10): "work drifting from a legacy system — + `inherit-legacy-style`"
- `skills/orchestrate/SKILL.md:65` (step 3, DESIGNPKG-AUTO paragraph): "legacy drift: + `inherit-legacy-style`"
- `skills/orchestrate/references/dispatch-prompt.md:24` (5a): "legacy drift — + `inherit-legacy-style`"
- `skills/orch-add-feature/SKILL.md:33`, `skills/orch-build-mvp/SKILL.md:41`, `skills/orch-change-feature/SKILL.md:36`, `skills/orch-fix-defect/SKILL.md:36`, `skills/orch-refine-code/SKILL.md:35` (UI-change rule in each orch-* skill): "legacy style drift: + `inherit-legacy-style`"
- `skills/ui-ux-pro-max/SKILL.md:363`: "On a hand-written legacy codebase, run `inherit-legacy-style` before writing UI"

These are imperative routing lines ("+ skill" in a brief-components list; "run X before writing UI"), not prose history. The feature-expansion copy was correctly re-routed to "drift handled inside the design package" (REROUTE_F27) — the same re-route was never applied to these 9 copies.
**Must change:** replace all 9 with the feature-expansion re-route (legacy drift handled inside the design package, no separate skill), and fix the OWED-13 record, which lists the orch-* copies as "prose-history".

### B2. Theme cage NOT fully lifted — E1 "new theme forbidden" survives in two copies

- `skills/orch-build-mvp/SKILL.md:43` and `skills/ui-ux-pro-max/SKILL.md:274` (E1 block, verbatim in both): bound (2) still reads "fit the theme's material world — material, tokens, palette balance, do-nots" with **no** "or a recorded departure" relaxation, and the block still says "NOT within reason: a new theme (re-deal instead, Taste step 4)".
- This directly contradicts the fixed copies: `skills/orchestrate/SKILL.md:148` and `skills/design-taste-frontend/SKILL.md:423`, where bound (2) carries "**or a recorded departure from it** (D19 reason required)" and the new-theme clause is deleted with the inversion sentence ("Inventing a theme direction is a recorded D19 decision, not a forbidden move").

SPEC §2 required the :423 inversion (and its orchestrate mirror); the two ECC-origin copies were never patched. An agent following orch-build-mvp or ui-ux-pro-max hits the old cage; an agent following orchestrate/Taste hits the new rule. The theme-as-starting-point is therefore not consistent across the tree.
**Must change:** apply the same two edits (relax bound (2), delete the new-theme clause, add the inversion sentence) to orch-build-mvp:43 and ui-ux-pro-max:274, via a build-time patch (both are ECC-origin files).

### B3. Live dispatch to CUT `ecc-recipes` in orchestrate

- `skills/orchestrate/SKILL.md:136`: "**Multi-command pipeline lookup — `ecc-recipes` (fix #25 §1, RECIPES_F25).** When a run needs a multi-command pipeline and the orchestrator does not already know which command group runs it, consult the `ecc-recipes` skill: it maps a described workflow to the right ECC command group with run-order and stop condition, read live from the `commands/` directory each run".

"Consult the X skill" in the top-level orchestrator is a live dispatch to a removed skill. Not listed in any OWED item.
**Must change:** re-route to a kept equivalent (the orchestrator's own command knowledge / `commands/` directory read directly) or delete the lookup step.

### B4. Live dispatch to CUT `dispatching-parallel-agents` — orchestrate description + hackathon-mode §6

- `skills/orchestrate/SKILL.md:3` (frontmatter description — the text Cursor reads to route): "Do NOT use for concurrent failure investigation (`dispatching-parallel-agents` owns that)"
- `rules/hackathon-mode.mdc:48` (§6): "`dispatching-parallel-agents` is for concurrent failure investigation only."

Both assign ownership of concurrent failure investigation to the removed skill. The feature-expansion copy was correctly re-routed to "the orchestrator's own parallel dispatch (Phase 1, one message)" (REROUTE_F27); these two were not.
**Must change:** re-route both to the orchestrator's own parallel dispatch.

### B5. Live dispatch to CUT `conventional-commit-review` in prp-commit

- `commands/prp-commit.md:59`: "Draft the message with the `conventional-commit-review` skill (`skills/conventional-commit-review/SKILL.md`, fix #25 §1) — it reads the repo's own history norms … for type, scope, and length instead of the generic table below; the table is the fallback when the skill cannot run."

Fix #25 wired /prp-commit via this skill; fix #27 cut the skill and re-routed only orchestrate's copy (fix27.py §6 → `git-workflow`). prp-commit's own dispatch was missed. verify27.py check 10 asserts only that `conventional-commit-review` is absent from orchestrate, so the verifier passes while this dispatch ships.
**Must change:** re-route prp-commit:59 to `git-workflow` (same as the orchestrate re-route).

### B6. Live dispatch to the removed continuous-learning-v2 instinct system — 3 commands + skill-create

The skill dir `skills/continuous-learning-v2/` (including `scripts/instinct-cli.py`) was removed, but these kept commands still invoke it:

- `commands/projects.md:17,23`: `python3 "$ECC_ROOT/skills/continuous-learning-v2/scripts/instinct-cli.py" projects` / `python3 skills/continuous-learning-v2/scripts/instinct-cli.py projects`
- `commands/promote.md:17,23`: same script, `promote [instinct-id]`
- `commands/prune.md:17,23`: same script, `prune`
- `commands/skill-create.md:16` (`/skill-create --instincts` — "Also generate instincts for continuous-learning-v2"), `:24`, and Step 4 (`:141`, "For continuous-learning-v2 integration:" + instinct YAML template)

fix27.py dropped `evolve` / `instinct-export` / `instinct-import` / `instinct-status` for exactly this reason, but projects/promote/prune were never examined — OWED-4 mentions only learn/learn-eval/project-init. verify27.py bakes all three into KEPT_COMMANDS, so the verifier asserts the broken commands present.
**Must change:** drop projects/promote/prune (same adjudication as evolve/instinct-*) or re-point them at a kept learning store; remove the `--instincts` / Step 4 CLv2 section from skill-create. Update verify27.py's KEPT_COMMANDS accordingly.

### B7. Live dispatch to dropped `/security-scan` + a harness check that now fails by design

- `commands/ecc-guide.md:89`: "`/security-scan` (END-ONLY) for agent configuration security review"
- `commands/fastapi-review.md:39`: "Command: `/security-scan` (END-ONLY — end of project or on explicit ask)"
- `commands/harness-audit.md:2` (description): "for a security-specific audit use the security-scan command (END-ONLY …)"
- `rules/react-native-security.mdc:43`: "Use `/security-scan` (AgentShield, END-ONLY — end of project or on explicit ask) on the agent configuration itself."
- `scripts/harness-audit.js:582-589` (`security-scan-command` check, category Security Guardrails, 2 points): `pass: fileExists(rootDir, 'commands/security-scan.md')`, `fix: 'Add commands/security-scan.md with scan and remediation workflow.'`

The command file was dropped by fix27.py, so the first four are pointers to a nonexistent command (the kept `security-review` skill / `ecc-security-reviewer` agent is the mid-build checklist, not this command's target), and the harness-audit check now **fails** on every run of the shipped audit script. fix27.py patched only `skills/security-review/SKILL.md` ("use security-scan" removal).
**Must change:** re-point ecc-guide/fastapi-review/harness-audit/react-native-security to the kept `security-review` skill, and remove or re-point the `security-scan-command` check in harness-audit.js.

### B8. Live routing to CUT `santa-method` in council

- `skills/council/SKILL.md:37` (When-NOT table): "Verifying whether output is correct | mid-build: `verification-before-completion`; at the end of the project: `santa-method`"
- `skills/council/SKILL.md:40`: "Reviewing code for bugs or security | `code-reviewer` or, at the end of the project, `santa-method`"
- `skills/council/SKILL.md:184` (Related Skills): "`santa-method` — adversarial verification (END-ONLY)"

The table rows are routing assignments (end-of-project verification → santa-method), not prose history; the kept end-gates are `verification-loop` / `production-audit` / `delivery-gate`. OWED-13 mis-records council's santa-method mention as prose-history.
**Must change:** re-route the two table rows to the kept end-of-project checks (e.g. `verification-loop` / `production-audit`) and drop the Related Skills entry.

### B9. Live dispatches in integration — CUT `mcp-server-patterns` + CUT `skill-scout`

- `skills/integration/SKILL.md:21`: "for building an MCP server from scratch (that is `mcp-server-patterns`)"
- `skills/integration/SKILL.md:46`: "Use `skill-scout` to search for a skill that already covers this integration (a vendor skill, an SDK skill, a sponsor skill)."
- `skills/integration/SKILL.md:60`: "Use `mcp-server-patterns` for the server setup and wiring, and treat the MCP tools as the adapter."
- `skills/integration/SKILL.md:122` (composition list): "This skill composes the plugin's own skills (`skill-scout`, `documentation-lookup`, …, `mcp-server-patterns`, `app-scaffold`)"

"Use X" × 2 plus an ownership assignment plus a composition list are live dispatches, not prose history. OWED-13 mis-records them ("names mcp-server-patterns (x3) + skill-scout (x2) … prose-history").
**Must change:** re-route :46 to `documentation-lookup` / grep-and-read (the kept discovery path), :21/:60/:122 to the kept fallback (hand-rolled client via `api-integration`, or the recorded-gap fallback), or delete the MCP-server path.

### B10. Live dispatch to CUT `intent-driven-development` in ai-feature-spec

- `skills/ai-feature-spec/SKILL.md:3` (frontmatter description — a routing surface): "For non-AI features use intent-driven-development; for API contracts use contract-first."

"For non-AI features use X" routes all non-AI feature work to the removed skill. OWED-13 mis-records it as prose-history.
**Must change:** re-route to `hackathon-scope` (the kept scoping skill, per the SPEC's own adjudication that grill-me/hackathon-scope cover scoping).

### B11. Live dispatch to CUT `agent-self-evaluation` rubric in the kept evaluator agent

- `agents/ecc-agent-evaluator.md:24`: "Read `skills/agent-self-evaluation/SKILL.md` for the detailed scoring rubric."
- `agents/ecc-agent-evaluator.md:54`: "Work through the 5 axes from the `agent-self-evaluation` skill"
- `agents/ecc-agent-evaluator.md:69`: "Use this exact format (matches `skills/agent-self-evaluation/scripts/evaluate.py` output)"
- `agents/ecc-agent-evaluator.md:110`: "Always include the structured report above, matching the `skills/agent-self-evaluation/scripts/evaluate.py` output format exactly."
- `agents/ecc-agent-evaluator.md:3` (description): "… or when the agent-self-evaluation skill is act[ive]"

The evaluator's entire rubric and output format are the removed skill's files. OWED-5 records this accurately ("No kept rubric replaces it; coordinator decides the evaluator's rubric source") — but the record does not fix the shipped breakage: invoking the kept agent reads two nonexistent paths. Mitigating fact, not an excuse: the call map lists `ecc-agent-evaluator` as uncalled (no textual dispatch path), so it fires only if the user invokes it by description — which its description invites ("Use after any non-trivial task when the user wants a quality assessment").
**Must change:** per OWED-5, the coordinator must supply a kept rubric source (inline the 5-axis rubric in the agent file, or point it at `verification-before-completion` / `code-reviewer`) — the agent cannot ship reading removed files.

### B12. Affirmative CUT routing in alwaysApply `rules/hackathon-mode.mdc` §5/§6 (+ mobile-ship)

- `rules/hackathon-mode.mdc:46` (§6): "`brainstorming` is for later ideation on a specific feature or problem."
- `rules/hackathon-mode.mdc:55` (§6): "`codebase-memory` owns exploring and understanding code you did not write: tracing callers/callees, finding where a feature lives, dead-code hunts, and impact analysis before a change."
- `rules/hackathon-mode.mdc:53` (§6): "Writing screens or features belongs to `react-native-patterns` / `dart-flutter-patterns`."
- `skills/mobile-ship/SKILL.md:9`: "belongs to react-native-patterns / dart-flutter-patterns" (same ownership line)

These are ownership assignments ("X is for …", "X owns …", "belongs to …") in the alwaysApply rule file — the highest-authority routing text in the plugin. OWED-12 recorded hackathon-mode's CUT references but the staged-edits worker (who owned this file) fixed none of them; the staged-patch-log's 5 hackathon-mode edits cover §1, §6-ALWAYSLEAD, §7-DELRISK, §6-DESIGNPKG-AUTO only. (The negative statements in the same file are fine and are NOT findings: `product-lens` / `intent-driven-development` "do not scope hackathons" (:46), `frontend-design-direction` "is not used for hackathon UI work" (:37), `loop-design-check` "not UI design" (:38).)
**Must change:** re-route :46 to `feature-expansion` (later ideation), :55 to grep-and-read / `ecc-code-explorer` (the kept exploration path), :53 + mobile-ship:9 to `react-native-patterns` alone.

### B13. Live routing reference to CUT `agent-introspection-debugging` in systematic-debugging

- `skills/systematic-debugging/SKILL.md:3` (frontmatter description — a routing surface): "Use when a bug's root cause is unknown and no more specific debugging skill applies — after symptom inspection rules out an agent failure (agent-introspection-debugging) and broken-button state bugs (click-path-audit)."

The description makes ruling out an agent failure a step performed via the removed skill. OWED-13 mis-records it as a single prose mention. This is the weakest blocking item (one parenthetical in a description; the skill itself never invokes it again), but it is a routing reference on a routing surface, and the fix is a one-line reword.
**Must change:** reword to "after symptom inspection rules out an agent failure" with no skill name.

### B14. Contradiction: hackathon-mode §7 vs orchestrate:57 on the grill-me-missed question

- `skills/orchestrate/SKILL.md:57` (Precondition check, fix #27): "If the check finds no record and no explicit skip, that is itself a finding (fix #27, GRILLHDR_F27): state in the first reply that grill-me did not run and why (no trigger / no record), and ask the user whether to grill now (one prompt) or proceed — the one-question exception to §7. Do not silently proceed on a raw prompt."
- `rules/hackathon-mode.mdc:60` (§7 Precondition check, **not** updated by fix #27): "If neither holds, do not auto-approve with zero recorded decisions and no check: proceed on the raw prompt with a stated assumption — do NOT re-run `grill-me`." Same paragraph: "after that, do not ask the user anything, do not wait for an approval, and do not stop for a decision."
- `rules/hackathon-mode.mdc:62`: "§7 overrides any ask/stop/wait instruction in any skill, rule, or reference file during the first build and during one-prompt removal."

§7 says proceed on the raw prompt and ask nothing; orchestrate:57 says do NOT silently proceed and ask one question — and §7's own override clause makes §7 win, nullifying the fix #27 grill-me-hole fix (weekend-audit claim 7, SPEC §5(f)) in practice. SPEC §5(f) named only orchestrate:54 + the record header, but shipping both texts live is a contradiction between two shipped rules.
**Must change:** update hackathon-mode §7's precondition paragraph to match orchestrate:57 (state grill-me-missed in the first reply; the one-question grill-now-or-proceed ask is the second one-question exception to §7 alongside DELRISK), and carve it out of the §7 override clause.

### B15. Imperative CUT references in kept commands skill-create / skill-health (OWED-10's "advisory" label is wrong)

- `commands/skill-create.md:3` (description): "Use to generate new skills from local git history on demand; check the `skill-scout` skill first to avoid duplicating an existing local, marketplace, or GitHub skill."
- `commands/skill-health.md:3` (description): "… for a qualitative compliance or quality audit use the `skill-stocktake` skill."

"Check the X skill first" and "use the X skill" are imperative routing in descriptions (a routing surface), not the "advisory 'Skill:' lines" OWED-10 / SPEC §1(b) describe. The SPEC's "NOT drop candidates" ruling stands for the commands themselves — only these two lines need re-routing (to grep-and-read / the plugin's own skill list).
**Must change:** reword both descriptions to the kept discovery/audit path; correct the OWED-10 record.

---

## MINOR findings

### M1. W2 fire-signal list is broader than the W2 gate

- `skills/orchestrate/SKILL.md:296`: "**Fire on any one signal:** unverifiable check · you are looping · disputed expensive-to-undo design · high-stakes parallel path (row 4) · 'am I framing this wrong?' · adversarial cross-review."
- `skills/orchestrate/references/patterns.md:28`: "**High-stakes parallel path (row 4).** High blast radius *and* hard to verify: launch two deep-reasoner passes blind, then reconcile." (no gate qualifier)
- `rules/hackathon-mode.mdc:67`: "Escalations do not wait: if two deep-reasoner passes fail or disagree, record both positions …" (conditional, weaker)

The gate (orchestrate:128 row 4, :289) allows a second pass **only** when the first pass flags genuine uncertainty or two genuinely different priors exist. The signal list permits it on looping / unverifiable-check / disputed-design / adversarial grounds that the gate does not name. The SKILL.md list sits under a gated section, so the gate arguably scopes it — but patterns.md:28, the per-signal explanation the SKILL.md points to, states row 4 unconditionally.
**Must change:** qualify patterns.md:28 and the :296 signal list with the gate ("only when the gate above is met"), or widen the gate's two conditions to name the signals that are genuinely allowed.

### M2. NOCOAUTHOR missing from the orchestrate step-6 static check list (SPEC §5(e) second placement)

The rule itself is present and correct in `rules/common-git-workflow.mdc:16` ("Commit messages carry no `Co-authored-by:` trailer for any AI tool (including Cursor) and name no AI tool as author or contributor. The commit author is the user. (NOCOAUTHOR_F27)"). But SPEC §5(e) also required: "Add it to the orchestrate step-6 static check list so the audit fails a commit carrying the trailer." No `Co-authored-by` / `NOCOAUTHOR` text exists anywhere in `skills/orchestrate/SKILL.md` (grep: 0 hits). The token census confirms NOCOAUTHOR_F27 occurs only in common-git-workflow.mdc.
**Must change:** add the trailer check to orchestrate step 6's static-check list.

### M3. OWED-7: trigger-file notes still name CUT deferred skills

`manifests/context-packs/skill-triggers@1.json`, `notes` field: "Deferred: production-audit, delivery-gate, codehealth-mcp, santa-method, security-scan, verification-loop." The 15 keys were correctly pruned (64 → 49, verified), but the notes prose still lists three removed skills as deferred. The file is DOCUMENTATION-ONLY per B6, so nothing routes — stale prose only.
**Must change:** edit the notes string to the three kept deferred checks.

### M4. OWED-9: delivery-gate still describes agent-self-evaluation as "shipped"

- `skills/delivery-gate/SKILL.md:3` (description): "Complements agent-self-evaluation …"
- `:13`: "This is distinct from reasoning gates (like the shipped `agent-self-evaluation` skill …)"
- `:15`: "`agent-self-evaluation` (shipped; upstream `self-audit` is not shipped in this plugin)"
- `:111`: "`agent-self-evaluation` — Reasoning quality gate (… shipped equivalent of upstream `self-audit` …)"

Only :97 was reworded per SPEC §1(b). The remaining four lines now state a falsehood (the skill is not shipped) and :15/:111 read as a reasoning-gate list entry. Descriptive, not a dispatch — minor.
**Must change:** reword to past tense / remove the "shipped" claims; point the reasoning-quality-gate entry at the kept replacement (see B11).

### M5. README stale CUT references

- `README.md:26-27`: marketplace-skills list still includes `brainstorming`, `dispatching-parallel-agents`, `agents-md-generator` as plugin contents.
- `README.md:29`: "`codebase-memory` queries a local knowledge graph of the repo …" presented as a plugin feature.
- `README.md:54-56`: deferred set named as "`codehealth-mcp`, `verification-loop`, `santa-method`, and `security-scan`" and "`/security-scan` … still reference them; the deferral wins".

fix27.py updated only the README count lines. Prose only, not dispatch.
**Must change:** update the three passages to the reduced set (deferred = verification-loop / production-audit / delivery-gate).

### M6. Dangling "see skill" / Related-Skills pointers in kept skills (not dispatches)

Single-mention reference-list pointers to removed skill dirs — no imperative "use":

- `skills/contract-first/SKILL.md:15` ("… and `ai-regression-testing`, which guards fixed bugs from returning") and `:284` (Related Skills list entry)
- `agents/ecc-database-reviewer.md:93` ("see skills: `postgres-patterns` and `database-migrations`")
- `skills/tdd-workflow/SKILL.md:300` ("See the `bun-runtime` skill for runtime, install, …")
- `skills/postgres-patterns/SKILL.md:143` ("Skill: `clickhouse-io` - ClickHouse analytics patterns")
- `skills/react-patterns/SKILL.md:269` (links to `../accessibility/SKILL.md`, `../angular-developer/SKILL.md`)
- `skills/typescript-patterns/SKILL.md:589` (`nestjs-patterns`), `:592` (`prisma-patterns`)
- `skills/react-native-patterns/SKILL.md:324` ("`coding-standards` — TypeScript/JavaScript idioms that apply to RN code.")
- `skills/council/SKILL.md:184` (Related Skills: `architecture-decision-records`)
- `skills/strategic-compact/SKILL.md:153` (Related: "`continuous-learning` skill — Extracts patterns before session ends")
- `scripts/lib/resolve-ecc-root.js:25`: `DEFAULT_SKILL_PROBE = path.join('skills', 'continuous-learning-v2')` — a probe path constant pointing at a removed dir (usage not traced in this audit; flag for the sweep, not asserted as a break).

**Must change:** re-point or delete each pointer at the next pass; none blocks on its own.

### M7. OWED-11 residue: rules/*.mdc dangling pointers (record accurate, residue remains)

Sampled, all pointer-style (not imperative dispatch):

- `rules/react-patterns.mdc:194`: "For accessibility see `skills/accessibility/SKILL.md`."
- `rules/angular-patterns.mdc:249`: "See skill: `angular-developer` for deep guidance on signals, forms, routing, DI, SSR, and accessibility patterns."

plus the per-language rule families named in OWED-11 (angular/dart/kotlin/rust/nuxt/perl/cpp/java). Rules were deliberately NOT cut per SPEC §1(d), so this residue is expected — but the pointers dangle and the follow-up rules debloat should take them.
**Must change:** none in this fix; carry to the rules-debloat follow-up.

### M8. polish-pass slop-checklist theme-fit criteria lack the departure allowance

`skills/polish-pass/reference/slop-checklist.md:100, :136, :152, :168, :200, :218` — check criteria such as "fit the theme's material world" / "diagram must fit the theme's material world" with no "or a recorded departure" qualifier. A checker following the list literally would flag a legitimate D19 departure as a finding, contradicting THEME-START in orchestrate:148 / design-taste-frontend:423.
**Must change:** add the departure qualifier to the six checklist lines (or a header note: a D19-recorded departure satisfies the fit criterion).

### M9. OWED-record inaccuracies (the record, not the tree)

1. **OWED-13 is wrong in its blanket claim.** `fix27/fix27.py:465` (and `fix27-patch-log.md`): "All are prose-history or single-mention references". False for: inherit-legacy-style in the orch-* files (B1), integration's mcp-server-patterns/skill-scout (B9), ai-feature-spec's intent-driven-development (B10), council's santa-method (B8), systematic-debugging's agent-introspection-debugging (B13). Each needed a read before patching — the read now shows live dispatches.
2. **OWED-4 omits the CLv2 commands.** `fix27/fix27.py:456` covers evolve/instinct-* + the three HELD commands only; projects/promote/prune (B6) appear nowhere in the patch log's command decisions or OWED list.
3. **OWED-1 and OWED-6 texts in `fix27-patch-log.md` are stale snapshots.** OWED-1 still says the call map "still lists all 166 skills" (it was regenerated — verified, see Checks); OWED-6 still lists feature-expansion's CUT dispatches (they were re-routed — verified, see Checks). The resolutions are recorded only in `staged-patch-log.md`'s coordinator appendix ("update the OWED list at manifest time"), not in the patch log itself.
4. **OWED-12's handoff did not land.** `fix27/fix27.py:464`: "hackathon-mode.mdc is a staged source; the staged-edits worker owns it" — the worker's 5 hackathon-mode edits did not touch the §5/§6 CUT routings (B12).

**Must change:** correct the OWED list at manifest time (fix27/MANIFEST.md); do not carry the "all prose-history" claim forward.

### M10. verify27.py scope gap — 37/37 passes while 14 live dispatches ship

verify27.py checks exact dir sets, specific anchors, tokens, banned terms, and Grok pins — but it has **no CUT-name sweep over kept files**. Consequences observed: `conventional-commit-review` is asserted absent only in orchestrate (check 10), not in prp-commit (B5); projects/promote/prune are baked into KEPT_COMMANDS (B6); no check reads council, integration, ai-feature-spec, the orch-* files, or hackathon-mode §6 for CUT names. The 37/37 pass is therefore real for what it checks and silent on the largest residual risk class.
**Must change:** add a check 12 to verify27.py (or the next verifier): every CUT skill/agent/command name must occur zero times as a live dispatch in kept files — at minimum a grep census that fails on the names in B1–B13/B15, with the prose-history exceptions allow-listed by file:line.

### M11. SPEC §7 prior-verifier criterion not met — verify26/verify25 crash, they do not fail on codified tails

SPEC §7: "Prior verifiers: re-run; fails must be only the codified tails (the count moves from §1 + the README count updates)."

- `fix26/verify26.py` (re-run by this auditor): crashes — `FileNotFoundError: …/skills/django-verification/SKILL.md` (the dir fix27 removed).
- `fix25/verify25.py` (re-run by this auditor): crashes — `KeyError: 'skills'` at `second_order_orphans` (the regenerated call map changed shape).

Neither fails cleanly on the codified count tails. The crash causes are the expected removals/regeneration, so this is verifier tooling obsolescence, not a shipped-tree defect — but the SPEC §7 criterion as written is not met, and the "only codified tails" claim cannot be evidenced from a crash.
**Must change:** record both verifiers as obsolete-against-the-reduced-tree in the manifest (or update them to tolerate the removal); do not claim the §7 prior-verifier criterion passed.

---

## HELD-command adjudications (learn / learn-eval / project-init)

Evidence base: the command files themselves; the regenerated call map (`skills/orchestrate/references/call-map.md`); a tree-wide grep for callers.

### learn — KEEP

- `commands/learn.md:2` (description): "Extract reusable patterns from the current session and save them as candidate skills or guidance. … continuous-learning-v2 is a separate, configurable … hook-observation and instinct-evolution system … and is not an automatic equivalent of this command." The command distinguishes itself from the removed CLv2 system in its own description — it is not a CLv2 command.
- Call map row: "`/learn` | commands/learn-eval.md [strong]; commands/learn.md [struct-command]" — its only textual caller is learn-eval, which is itself UNCALLED (call-map:45; second-order orphans, call-map:56: "commands: 2 — `learn`, `python-review`").
- It is a user-invoked, on-demand session-review tool (`Run /learn at any point during a session when you've solved a non-trivial problem`): zero build-time cost, never fires unless asked.
- Same standing as the kept `skill-create` / `skill-health` commands, which SPEC §1(b) explicitly keeps as user-invoked plugin-maintenance commands.
- **Recommendation: KEEP.** If learn-eval is cut (below), learn's only textual caller goes with it — but commands are structurally user-invocable via `/name`, so "uncalled" does not mean unused; the keep rests on user-invocation, not on learn-eval.

### learn-eval — CUT

- Call map: "`/learn-eval` ⚠ UNCALLED | commands/learn-eval.md [struct-command]; manifests/pi-core.json [shipped]" (call-map:338; uncalled-commands list, call-map:45). No skill, agent, rule, or command invokes it.
- `commands/learn-eval.md`: "Extends `/learn` with a quality gate, save-location decision, and knowledge-placement awareness before writing any skill file." It duplicates /learn; its distinguishing piece is a quality gate whose natural rubric source — the `agent-self-evaluation` skill — was removed (see B11). No live dispatch to a CUT skill was found in its own file, so this is a clean cut, not a repair.
- **Recommendation: CUT.** /learn covers the workflow; the quality-gate extension has no caller and no rubric source.

### project-init — CUT

- `commands/project-init.md`: "Detect a project's stack and produce a dry-run ECC onboarding plan … Use to onboard ECC into a target project via a reviewable dry-run plan." This is ECC installation/onboarding (plugin maintenance), the same category as CUT `agent-sort` ("Builds an ECC install plan for a repo") — not a hackathon build step. A hackathon project opens with the plugin already installed.
- Call map row: "`/project-init` | commands/ecc-guide.md [strong]; commands/project-init.md [struct-command]" (call-map:351) — its only caller is the guide's pointer (`commands/ecc-guide.md:85`: "`/project-init` for stack-aware ECC onboarding of a target project").
- Its own example is stale: `commands/project-init.md:16` — `/project-init --skills continuous-learning-v2,security-review` — names a removed skill.
- The "--skills as a parameter" hold rationale is real but does not save it: a generic parameter does not make an install/onboarding command a build command.
- **Recommendation: CUT.** Cutting requires updating the `commands/ecc-guide.md:85` pointer. (If the coordinator wants to keep an ECC-onboarding path, the command needs its example fixed and a stated owner — that is a keep-with-repair, not a keep-as-is.)

---

## Checks passed (verified clean, with evidence)

1. **verify27.py re-run by this auditor: 37/37, exit 0** (same counts as `fix27/verify27-run1.log`).
2. **Counts + exact dir sets:** built tree has 66 skills / 45 agents / 123 rules / 60 commands (`ls | wc -l`); skill dir set is exactly the 66 KEPT skills; all 100 CUT skill dirs absent; all 27 removed agents and 27 dropped commands absent (verify27 checks 1–4 + direct listing). `growth-log` and `gan-style-harness` present (kept per adjudication).
3. **All 18 _F27 tokens present in the built tree**, in the right files (auditor census): DESIGNPKG-AUTO_F27 in orchestrate + hackathon-mode; CEILING_F27 in orchestrate + hackathon-scope; DELRISK_F27 in orchestrate + hackathon-mode; CHECKSRC_F27/AUDITGUIDE_F27 in orchestrate + hackathon-scope + hackathon-pitch; NOCOAUTHOR_F27 in common-git-workflow.mdc; THEME-START_F27 in orchestrate + design-taste-frontend + hackathon-mode + feature-expansion; ALWAYSLEAD_F27 in orchestrate + hackathon-mode; IMPL46_F27 in orchestrate; GRILLHDR_F27 in grill-me + orchestrate + hackathon-scope; CAPTURE1_F27 in browser-qa; TESTNOTBQA_F27 in verification-before-completion; DEFER3_F27 in hackathon-mode + orchestrate; W2/W3/W4_F27 in orchestrate (+W3 in feature-expansion/design-taste-frontend/polish-pass); TESTPASS_F27 in orchestrate; REROUTE_F27 in feature-expansion.
4. **Call map regenerated from the reduced tree:** counts table 66/45/123/60/15/49 (`skills/orchestrate/references/call-map.md:8-14`); staged md5 == built md5 `06aab4c10bca5dfe99e78aa252fb9878`; B6 DOCUMENTATION-ONLY note intact (:38); sampled CUT names have 0 rows (bengali-nlp, santa-method, codehealth-mcp, brainstorming, security-scan, product-lens); kept `gan-style-harness` 5 rows, `growth-log` 2 rows. Generator EXPECTED updated to 66/45/123/60/15/49 (`fix25/callmap/generate_call_map.py:100-101`).
5. **Theme cage lifted where the workers edited:** design-taste-frontend:256 ("The dealt theme is the starting point, not the cage"), :262 (genre map widened: ops/technical-tooling, data/video-pipeline, scientific domains; "Nothing defaults to `editorial`"), :423 (bound (2) relaxed + inversion sentence); orchestrate:138 (dashboard hero-moment line), :148 (bound (2) relaxed + inversion); feature-expansion:152, :196 (dealt theme as the starting point). (The two unpatched copies are B2.)
6. **Orchestration always-lead:** hedge deleted — orchestrate:14 now states the pin as binding ("If the session is not on Grok 4.7 High, say so in the first reply … never silently"); MODEL-PIN check present (:61, `MODEL-PIN: grok-4.7-high | other: <name>`, unverified recorded as unverified); always-lead remit (:59, :120; hackathon-mode §6); grill-me trigger phrases in hackathon-mode §1 (:12); implementation tier `cursor-grok-4.6-high-fast` (:29, :92); no "two deep-reasoner passes" mandate in orchestrate SKILL.md — row 4 gated (:128), gate at :289, "single pass by default" throughout.
7. **Usage cuts:** W2 gate (:128, :289); W3 per-wave reviewer cap (small waves get the step-1 cheap check only, :272 + 5a); hero + finish merged into ONE fresh-context review (orchestrate:283, design-taste-frontend:537); beat-v5 re-deal capped at most 2 (orchestrate:73 + 5a static check, "after that the trailing dimension is recorded as owed with its cause (which is also the ceiling flag)"); single capture run (browser-qa:67 CAPTURE1_F27; polish-pass W3); Phases 0–3 run once (feature-expansion); W4 bound (orchestrate:69/:71, untouched sections record one line "not considered — <reason>").
8. **Durable rules intact:** 9+ alwaysApply gates present (common-agents, common-code-review, common-coding-style, common-development-workflow, common-git-workflow, common-hooks, common-patterns, common-performance, common-security, common-testing all `alwaysApply: true`, plus hackathon-mode + ponytail); 80% coverage (common-testing.mdc:7, :22; common-development-workflow.mdc:23), functions <50 lines (common-code-review.mdc:34, :101; common-coding-style.mdc:47), files <800 lines (common-code-review.mdc:102); D19 (28 mentions in orchestrate); Fraunces body-only (orchestrate:162, :174); browser-qa sole screen verdict (browser-qa:77-83, HERO-BQA/MEMORABLE/beat-v5 verdicts); grill-me first + header (grill-me:39 writes `grill-me: RAN`; hackathon-scope:9 stub carries SKIPPED/MISSED; orchestrate:57); /demo local-only + under 2:10 hard rule, 2:30 absolute max (pitch-deck-video:102, :208; hackathon-mode §7); no-Co-authored-by rule (common-git-workflow.mdc:16 — second placement missing, see M2); deferred lists name only the three kept checks (orchestrate:8, :114, :381; orch-build-mvp:86; hackathon-mode:22); zero "six deferred" remnants in the built tree.
9. **Banned terms 0; Grok pins only:** verify27 checks 8–9 pass on re-run (grok-4.7-high ×56, cursor-grok-4.6-high-fast ×74, bare grok-4.6-high-fast ×0). Note: the staged hackathon-mode.mdc:38 still carries the upstream `claude -p` wording by design (fix16.py:3807 asserts on it and rewrites it at build time; staged-patch-log appendix documents the attempted-then-reverted reword) — the built tree is clean.
10. **build.sh wiring + fix27.py behavior + log match:** fix27 invocation present after fix26, before STEP 5 (`build.sh:24080-24089`); fix27.py exits non-zero on anchor errors (`fix27/fix27.py:486-490`, `sys.exit(1)`); build-log-run2 records "fix27: 23 change(s)", "fix27: 13 OWED item(s) recorded", "fix27: OK", then STEP 5 counts 66/45/123/60, hooks 15 — matching `fix27-patch-log.md` (23 changes, 0 errors, 100/27/27 removed).
11. **Kept essentials intact:** gan-style-harness + ecc-gan-evaluator/generator/planner agents + gan-build/gan-design commands all present and called (call map); growth-log present; all nine design-package skills present (design-taste-frontend, ui-ux-pro-max, less-flat-ui, polish-pass, motion-foundations, motion-patterns, motion-advanced, make-interfaces-feel-better, design-system); hackathon-mode §7 DELRISK coherent with orchestrate step 6 (three options, default (b), ledger + final-report recording) — except for the §7 precondition contradiction (B14).
12. **OWED dispositions verified accurate:** OWED-1 RESOLVED (call map regenerated, above); OWED-2 RESOLVED (gan kept; dispatch evidence orch-build-mvp:39, :62, :95 / orch-pipeline:37, :97 confirmed by the call map's /gan-build row); OWED-3 RESOLVED (deferred lists three-only, above); OWED-5 record accurate (evaluator rubric source missing — the dispatch itself is B11); OWED-6 RESOLVED for feature-expansion (remaining CUT mentions are all "was cut" / "NOT invoked" notes with REROUTE_F27 at :49, :100, :188, :190, :192-193, :204); OWED-8 RESOLVED (27 agents removed, exact set verified).
13. **Checked and NOT a finding:** `accessibility` (65 files match the name, but sampled uses are the generic English word — aria-labels, focus containment — in agents/ecc-a11y-architect.md and reviewers; the only skill-pointer is the dangling link in M6/M7); `brainstorming` as a generic verb in hackathon-pitch/references/win-secrets.md:19, :165 ("Spend 10 minutes brainstorming a name"); `codebase-onboarding` in ecc-spec-miner.md:3, :40, :201 (explicitly negative — "does not require `codebase-onboarding`"); `frontend-design-direction` / `product-lens` / `intent-driven-development` / `loop-design-check` negative statements in hackathon-mode §5/§6 ("is not used", "do not scope hackathons", "not UI design"); CLv2 hook machinery in scripts/hooks/observe-runner.js + posttooluse-dispatcher.js (not wired — posttooluse-dispatcher.js:5 states "Not wired in this Cursor plugin — it never runs"; observe-runner.js is referenced only by upstream scripts, not by hooks.json's 15 entries); staged-vs-built diffs for the 7 staged files are small (0–22 lines) and consistent with known build-time patches (fix16 rewrites, agent-file references, fix27.py's DEFER3 patch at orchestrate:381).

## Open items carried forward

- **Rules (123) NOT cut** — per SPEC §1(d), the per-language rule families for cut languages remain a follow-up debloat candidate; their dangling skill pointers are M7. (Known open item; record verified accurate.)
- **fix27/MANIFEST.md does not exist yet** (no MANIFEST/sweep/dry-run files in `fix27/` as of this audit). SPEC §7 requires the manifest (disposition table, anchor tokens, open parent adjudications, dry-run caveat), Sweep #35 (CLEAN, weaving-coherence CLEAN), and Dry-run #42 (PASS) — all still to run. The OWED corrections in M9 should be folded into the manifest when written.
- **OWED-5 rubric source** (evaluator's replacement rubric) — coordinator decision outstanding; it is B11 until resolved.
- **HELD commands** — coordinator to decide on the adjudications above (learn KEEP, learn-eval CUT, project-init CUT).
- **Prior verifiers** — verify26.py / verify25.py are obsolete against the reduced tree (M11); decide whether to update them or record them as retired.
- **Netlify row touch-up** (due after Dec 4, 2026) — unchanged, still open from fix #26.

## Verdict

**NOT PASS — BLOCKING: 15, MINOR: 11.** Do not push until B1–B15 are re-routed or removed and M1–M11 are dispositioned; the largest single work item is the CUT-dispatch sweep across the kept ECC-origin files (B1, B2, B3, B5–B11, B13), which verify27.py does not cover and should be added to it (M10).
