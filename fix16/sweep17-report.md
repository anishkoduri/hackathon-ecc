# Sweep #17 report — plugin fix program #16 (hackathon-ecc)

**Date:** Wed 2026-11-11 (evening, CST). **Sweeper:** re-sweep worker, sweep #17.
**Scope:** built tree `hackathon-ecc/` (except `node_modules`), staged sources `new-skills/` + `round2-skills/` + `~/workspace/cursor-skills/less-flat-ui/`, `LIVE_SMOKE_TEST.md`, shipped `hackathon-ecc/README.md`, `.cursor-plugin/marketplace.json`. `fix16/` working files, scratch dirs, and audit backups NOT swept (historical record). `build.sh` NOT swept for a zero-hit verdict (acknowledged exception) — inventoried separately in §15.

**State verified (not assumed):** `build.sh` 23,221 lines, md5 `532ab5458c22d6341444fdc92cf67ffd`. Counts: skills 166, agents 72, rules 123, commands 87, hooks 15 (hooks.json has 15 events), 2,665 files in the built tree (`find … | wc -l` = 2665). Pins: `grok-4.7-high` 45 lines / 52 occurrences in the tree; `cursor-grok-4.6-high-fast` 99 lines / 100 occurrences in the tree (117 occurrences scope-wide). Build 13 + build 14 logs end `build complete`, counts `skills: 166 / agents: 72 / rules: 123 / commands: 87 / hooks: 15`. fix16 run log self-check: `TOTAL BANNED-TERM HITS: 0`.

## Verdict: NOT CLEAN — 0 blocking, 2 minor

All 15 checks pass on their stated bar (zero banned terms, zero stale counts, zero live pins, zero bare fast slugs). The fix-up held: sweep #16's 1 blocking + 4 minor are all verified fixed. Two cosmetic residues of the fix-up's generic prose substitution remain in one shipped file — garbled Grok model names left by fix16's `generic_pass` when the source text carried a version suffix the substitution regex did not cover (`Opus 4.x` → `Grok 4.7 High 4.x`; `Sonnet 5` → `Grok 4.6 High Fast 5`). Both are prose only — not pins, not banned terms, no wrong model routed anywhere — so they are minor, not blocking.

### Findings

| # | Severity | File:line | Finding | Fix |
|---|----------|-----------|---------|-----|
| M1 | minor | `hackathon-ecc/skills/strategic-compact/SKILL.md:68` | Shipped prose reads `(e.g. 400k Grok 4.7 High 4.x, or a new 1M-window model family)` — `Grok 4.7 High 4.x` is not a real model name. Source was `400k Opus 4.x`; fix16 `generic_pass` (`fix16.py:1254`) only rewrites `Opus 4.\d+`, so the literal `4.x` survived the bare `\bOpus\b` → `Grok 4.7 High` replacement. | Reword the example, e.g. `(e.g. a 400k-window model, or a new 1M-window model family)` — or extend the fix16 regex to `Opus 4\.[\dx]+` and rebuild. |
| M2 | minor | `hackathon-ecc/skills/strategic-compact/SKILL.md:102` | Shipped prose reads `Cursor **2.1.233 removed the todo/task tools by default** on Grok 4.7 High, Grok 4.6 High Fast 5,` — trailing `5` is a leftover version digit (`Sonnet 5` → `Grok 4.6 High Fast` + ` 5` via the bare `\bSonnet\b` replacement, `fix16.py:1256`). | Drop the stray ` 5` (and check the sentence still parses: `…on Grok 4.7 High, Grok 4.6 High Fast, current models and newer…`). |

Residue sweep: `Grok 4.7 High [0-9.]` / `Grok 4.6 High Fast [0-9.]` across the whole scope returns only these two lines — no other garbled Grok names. The `plankton-code-quality/SKILL.md:16` double-`Grok 4.6 High Fast` (`Haiku` + `Sonnet` both collapsing to the fast slug) is the documented haiku+sonnet collapse (`fix16.py:3128`), not a residue.

## Per-check results

| Check | Bar | Result |
|---|---|---|
| 1. `composer-2.5` | 0 | **0 hits** in scope |
| 2. `claude` | 0 | **0 hits** in scope (sweep #16's 38 staged-source lines all gone) |
| 3. `codex` | 0 | **0 hits** in scope (sweep #16's 18 staged-source lines all gone) |
| 4. `anthropic` | 0 | **0 hits** in scope (sweep #16's 10 staged-source lines all gone) |
| 5. `opus` as model/vendor word | 0 | **0 hits** in scope — no individual hits to list |
| 6. `sonnet` / `haiku` as model IDs | 0 | **0 hits** in scope. All three sweep-#16 tree hits fixed: `agent-compress.js:118` now reads `model: frontmatter.model \|\| 'cursor-grok-4.6-high-fast'`; the 2 Haiku comments are gone (0 `haiku` hits tree-wide). `fix16.py` self-check term list verified to include both: `fix16.py:1299-1300` `banned = [r"composer-2\.5", r"claude", r"codex", r"anthropic", r"sonnet", r"haiku"]`. |
| 7. Non-Grok model pins (`model:` fields, pin tables, pin examples) | 0 | **0 hits.** `model:` grep for `gemini|gpt-|sonnet|haiku|opus|composer|claude` as the ID: 0 lines. Literal `model:` pins in the tree are Grok only: `model: grok-4.7-high` ×4, `model: cursor-grok-4.6-high-fast` ×72. |
| 8. `grok-4.7[` bracket hits | 0 | **0 hits** |
| 9. Bare `grok-4.6-high-fast` (not preceded by `cursor-`) | 0 | **0 bare hits.** `cursor-grok-4.6-high-fast` occurrences: 117 scope-wide (100 in the tree, 17 in staged sources + smoke test). |
| 10. Composer-feature distinction | list + classify | **50 lines, all classified below; none is a model pin, none names Cursor's Composer UI feature.** |
| 11. `LIVE_SMOKE_TEST.md` §14 + step 1 + step 7 | §14 exists, covers fast pin; step 1 counts 166/87 | **Pass** — §14 quoted below; step 1 reads `166 skills, 72 agents, 123 rules, 87 commands`; step 7 names `grok-4.7-high`; 0 stale model names anywhere in the doc. |
| 12. Stale counts | 0 × `169 skills` / `168 skills` / `96 commands`; `166 skills` + `87 commands` present; 72/123/15 current | **Pass** — stale strings 0 hits scope-wide (also checked `167 skills`, `95 commands`, `88 commands`: 0). `166 skills` + `87 commands` in README:13,40 and smoke test:17; `72 agents` + `123 rules` in the same lines; 15 hooks = 15 events in `hooks/hooks.json`, matching build 13/14 logs (`hooks: 15`). README `56 MB` matches `du -sh hackathon-ecc` = `56M`. |
| 13. `Claude Code-only` | 0 | **0 hits.** 3 reworded labels quoted below. |
| 14. Antigravity | verify the 14-line list; none a gate mode / pin / banned term | **Pass** — exactly the 14 expected lines in 6 files (listed below); install-target gate is `LEGACY_INSTALL_TARGETS = ['cursor']` (`scripts/lib/install/request.js:6`); the one `plan.target === 'antigravity'` hit is a legacy-compat reconciliation filter, not a gate mode. |
| 15. build.sh exception inventory | inventory every hit, verify :18296 / :265 / :298 / zero live pins | **Pass with the inventory below** — 798 hits, all classified: (a) 389 OLD-side, (b) 52 comments, (c1) 355 NEW-side, (c2) 0, (c3) 2. The two live-pin candidates (:12426, :15142) are resolved (deleted file / re-pinned by fix16 — see §15). Zero live pins ship. |

## Check 10 — Composer-feature distinction (all 50 lines)

**PHP Composer CLI / `composer.json` / `composer.lock` / `getComposerDeps` — 33 lines:**
`hackathon-ecc/rules/php-coding-style.mdc:3`, `hackathon-ecc/rules/php-hooks.mdc:3`, `hackathon-ecc/rules/php-patterns.mdc:3`, `hackathon-ecc/rules/php-security.mdc:3`, `hackathon-ecc/rules/php-security.mdc:18` (`composer audit`), `hackathon-ecc/rules/php-testing.mdc:3`, `hackathon-ecc/skills/laravel-plugin-discovery/SKILL.md:59` (`Full Composer package name`), `hackathon-ecc/skills/laravel-verification/SKILL.md:22,31,46,49,50,89,153,155,159,168,169,173` (`composer --version` / `validate` / `dump-autoload -o` / `audit`, `Phase 1.5: Composer and Autoload`), `hackathon-ecc/skills/codebase-onboarding/SKILL.md:29`, `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:77` (`composer.json` Laravel detect), `hackathon-ecc/agents/ecc-php-reviewer.md:77` (`composer audit`), `hackathon-ecc/scripts/lib/gateguard-search-filters.js:43` (`'composer.lock'`), `hackathon-ecc/scripts/lib/project-detect.js:85,305,309,311,312,313,314,397,423,487` (`composer.json`/`composer.lock` markers + `getComposerDeps`).

**CSS / UI `.composer` class — plugin's own plan-canvas dashboard (not Cursor's Composer) — 11 lines:**
`hackathon-ecc/scripts/lib/plan-canvas/ui.js:171,172,173,174,175,176,177,178,179` (`.composer`, `.composer .hint`, `.composer textarea`, `.composer .row`, `.composer .send`, `.composer .status` CSS) + `:517` (`<div class="composer">` message-composer box with textarea + send button in the plan-canvas web view) + `hackathon-ecc/skills/ui-ux-pro-max/data/ui-reasoning.csv:165` (`Reply composer cues`, `constraint:reply-composer` — forum/discussion-board UI pattern data).

**`remotion-composer` — OpenMontage demo-video reference app dir name — 4 lines:** `hackathon-ecc/skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39`, `hackathon-ecc/skills/pitch-deck-video/references/openmontage/README.md:35`, `new-skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39`, `new-skills/pitch-deck-video/references/openmontage/README.md:35`.

**Prose — 1 line:** `hackathon-ecc/skills/dev-team/SKILL.md:14` — `adversarial challenge (\`council\`), and it is not a free-form team composer` ("team composer" = composing a team of agents).

**`composer session` — 1 line, reading verified:** `hackathon-ecc/scripts/hooks/cursor-session-env.js:3`:
```
 * Cursor sessionStart hook — inject ECC_AGENT_DATA_HOME for the composer session.
```
Context (`cursor-session-env.js:1-7`): `#!/usr/bin/env node`, JSDoc `Cursor sessionStart hook`, `Cursor passes session-scoped env from sessionStart output to all later hooks`, `@see https://cursor.com/docs/hooks`. This is the Cursor agent session the sessionStart hook runs in — it names no Cursor Composer UI feature, no model, and no Composer action. Reading confirmed, not a model pin and not the Composer UI feature.

**Check 10 conclusion:** 0 model pins, 0 Composer-UI-feature references among the 50 lines.

## Check 11 — LIVE_SMOKE_TEST.md §14 (full quote)

Step 1 (`LIVE_SMOKE_TEST.md:17`):
```
- [ ] Confirm the plugin's skills, rules, agents, and commands are listed under its details (counts should read 166 skills, 72 agents, 123 rules, 87 commands).
```
Step 7 (`LIVE_SMOKE_TEST.md:76-88`) — names `grok-4.7-high`:
```
## 7. Agent `model:` slug-form pins

The agents pin models with slug-form pins (e.g. `model: grok-4.7-high`, `model: cursor-grok-4.6-high-fast`).

- [ ] Ask for a reasoning-heavy task (should use deep-reasoner → `grok-4.7-high`).
- [ ] Ask for a fast task (should use fast-worker → `cursor-grok-4.6-high-fast`).
- [ ] Note whether Cursor honors the model pin, ignores it, or errors on the pin.
```
§14 (`LIVE_SMOKE_TEST.md:130-140`):
```
## 14. Grok pins hold — 4.7 High design, 4.6 High Fast task tier (fix programs #13, #16)

- [ ] **Picker selection:** before the first build, select **Grok 4.7 High** in Cursor's model picker. The plugin pins its design role to `grok-4.7-high` (slug form only — no bracket syntax), but Cursor's subagent model allowlist is coupled to the picker dropdown, so the pin can silently fall back to another model if Grok 4.7 High is not selected.
- [ ] **Design role runs on Grok 4.7 High:** on a build with UI work, confirm the design lead (the agent/skill doing design direction — Taste theme deal, ui-ux-pro-max direction, polish-pass) actually runs on Grok 4.7 High, not on another model. Note what it ran on and any error or fallback.
- [ ] **Fast tier runs on Grok 4.6 High Fast:** on a mechanical task, confirm the fast-worker / scout actually runs on Grok 4.6 High Fast (`cursor-grok-4.6-high-fast` — the `cursor-` prefix is part of the pin), not on another model. Note what it ran on and any error or fallback.
- [ ] **"High" cost note:** "High" is a reasoning effort, not a price tier — higher effort generates more reasoning tokens and burns the Cursor weekly usage pool faster. Note whether usage feels materially higher; this does not change the model choice.
```
Stale-model-name grep over the whole doc (`claude|codex|anthropic|opus|sonnet|haiku|composer-2.5|gemini|gpt-`): **0 hits**.

## Check 13 — spot-check of 3 reworded labels (was `Claude Code-only`, now `Cursor only`)

- `hackathon-ecc/skills/ck/SKILL.md:13`: `> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc/ck storage.`
- `hackathon-ecc/skills/continuous-learning/SKILL.md:3`: `description: "[DEPRECATED - Cursor only, use continuous-learning-v2] Legacy v1 stop-hook skill extractor. …"`
- `hackathon-ecc/commands/hookify-configure.md:2`: `description: Enable or disable hookify rules interactively (Cursor only — no Cursor equivalent in this plugin)`
- (4th, for the record) `hackathon-ecc/skills/plankton-code-quality/SKILL.md:3`: `… (Cursor only — uses PostToolUse hooks; the auto-fix subprocess was removed in fix #16, so Plankton reports violations instead of auto-fixing)`

## Check 14 — Antigravity verification (all 14 lines)

- `hackathon-ecc/skills/angular-developer/references/mcp.md:36:### Antigravity IDE`
- `hackathon-ecc/skills/angular-developer/references/mcp.md:38:Create a file named `.antigravity/mcp.json` in your project's root:`
- `hackathon-ecc/scripts/lib/install-lifecycle.js:854:  antigravity: {`
- `hackathon-ecc/scripts/lib/install-lifecycle.js:855:    code: 'legacy-antigravity-layout',`
- `hackathon-ecc/scripts/lib/install-lifecycle.js:856:    message: 'Legacy Antigravity install-state remains under .agent. Review and move any preserved modified or unmanaged files out of .agent, then rerun the Antigravity install to finish migration.'`
- `hackathon-ecc/scripts/lib/install-lifecycle.js:1688:    if (record.legacyLayout === 'antigravity' && managedOperations.length > 0) {`
- `hackathon-ecc/scripts/lib/install-lifecycle.js:1696:        warning: 'Legacy Antigravity files were preserved because their provenance cannot be revalidated during uninstall. Rerun the Antigravity installer to migrate verified files, then review .agent manually.',`
- `hackathon-ecc/scripts/lib/install/apply.js:804:    // fix #16 (D10): legacy Antigravity cleanup removed with the adapter.`
- `hackathon-ecc/scripts/lib/install/apply.js:805:    let antigravityMigrationWarnings = [];`
- `hackathon-ecc/scripts/lib/install/apply.js:866:        ...antigravityMigrationWarnings,`
- `hackathon-ecc/scripts/lib/install/content-transform.js:4:// transforms (Cursor manual-plugin namespace, Qwen/Antigravity/Copilot`
- `hackathon-ecc/scripts/lib/install/stale-operations-reconciliation.js:46:  // plans share a module id across languages and Antigravity legacy-compat`
- `hackathon-ecc/scripts/lib/install/stale-operations-reconciliation.js:52:  return !(request && request.legacyMode && plan.target === 'antigravity');`
- `hackathon-ecc/scripts/auto-update.js:188:  return 'Found only a legacy Antigravity .agent install-state. Run the Antigravity installer once to migrate it to .agents before auto-updating.';`

File spread (6 files, as expected): `angular-developer/references/mcp.md` ×2 (Antigravity IDE MCP docs), `scripts/lib/install-lifecycle.js` ×4 (legacy install-state warnings, `legacy-antigravity-layout`), `scripts/lib/install/apply.js` ×3 (fix #16 removal comment + empty `antigravityMigrationWarnings` carrier), `scripts/lib/install/content-transform.js` ×1 (historical comment), `scripts/lib/install/stale-operations-reconciliation.js` ×2 (legacy-compat), `scripts/lib/auto-update.js` ×1 (migrate message). Staged `design-taste-frontend` skill: 0 hits (verified separately).

**Gate-mode check:** the install-target gate accepts only `cursor` — `scripts/lib/install/request.js:6` `const LEGACY_INSTALL_TARGETS = ['cursor'];` (also `plan.js:223` `const target = options.target || 'cursor';`). The one line that looks gate-adjacent, `stale-operations-reconciliation.js:52` `return !(request && request.legacyMode && plan.target === 'antigravity');`, is inside `materializesWholeModules()` — a legacy-compat filter for old install *plans* (pure-legacy plans share a module id across languages; an absent operation is not stale there). It does not accept, select, or gate any install target; no hook mode, no model pin, no banned term. **No antigravity gate-mode reference found.**

## Check 15 — build.sh acknowledged-exception inventory (798 hits)

Method: every line of `build.sh` matching `composer-2.5|claude|codex|anthropic|opus|sonnet|haiku` (case-insensitive) was classified by AST analysis of the embedded Python heredocs (string-literal role: OLD vs NEW argument of `patch`/`audit*_patch`/`replace_desc_line`/`replace_text`/`append_desc`/`sub`), plus bash-comment / heredoc / `cp`-path detection. Full table below; summary:

| Class | Count | Meaning | Ships a banned term? |
|---|---|---|---:|
| (a) OLD-side match pattern | 389 | Upstream text / regex the build patches *away from* (e.g. `re.search(r"^model: (sonnet\|opus\|haiku)\s*$")` at :164, the `{"sonnet": …, "opus": …, "haiku": …}` mapping at :157, OLD args of `sub`/`audit*_patch` pairs) | No — matched and replaced, never written out |
| (b) Comment / build log | 52 | Bash + Python comments (`# Pin ECC agent models to Grok IDs (fix #16)…` :150-152, `# --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic ---` :23204, audit section headers, `print` log strings) | No — not shipped |
| (c1) NEW-side patch text | 355 | Replacement text written into the tree mid-build by the audit-fix heredocs (e.g. audit3 Fix 5 adds `Claude Code only — no Cursor equivalent` labels at :13413+; audit sections rewrite multi-* command bodies with `claude -p` upstream docs) | **No — see resolution below.** Written mid-build, then rewritten/removed by fix16 (the last build step); final tree grep = 0 for every banned term, and fix16's own self-check reads `TOTAL BANNED-TERM HITS: 0`. |
| (c2) Heredoc file write | 0 | No banned-term hit inside any `cat >` / `cat >>` file-write heredoc | — |
| (c3) Build-time source path | 2 | :265 `cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" …`, :298 `cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" …` | No — upstream-layout paths, not shipped text |
| **Total** | **798** | | **0 live pins; 0 shipped banned terms** |

Term totals across the 798 (a line can carry >1 term): `claude` 679, `codex` 96, `opus` 18, `sonnet` 23, `haiku` 11, `anthropic` 5, `composer-2.5` 0. (`composer-2.5` appears nowhere in build.sh at all — only its replacement, the `cursor-` fast slug, does.)

### Verified sub-items

- **:18296 (c2 heredoc) — verified clean.** The `cursor-hooks.schema.json` heredoc (`cat > … <<'SCHEMA_EOF'`, lines 18246–~18323) line 18296 reads: `…which describes the legacy hooks format (PascalCase events, matcher entries with {type, command} items) and does not accept this file.` — `"Claude Code hooks format"` is gone, replaced by `"the legacy hooks format"` as recorded. (And (c2) = 0 hits overall: no banned term in any file-write heredoc.)
- **:265 / :298 (c3) — verified upstream-layout paths, pins match.** `:265` source `/tmp/uipro/.claude/skills/ui-ux-pro-max` exists; `/tmp/uipro` HEAD = `6ae86f61f520d6ca229d2f40e070410638c908c5` = `UIPRO_PIN`. `:298` source `/tmp/skill-add/flecto-shade/.claude/skills/hackathon-pitch` exists; `/tmp/skill-add/flecto-shade` HEAD = `3a0f7e52cdb53c52494c7c34235001a042dd9822` = `FLECTO_PIN`. Both are the `.claude/skills/` layout the upstream repos actually ship — recorded exceptions, verified live.
- **:12426 (c1) — not a live pin.** `claude -p --model "$PLANNER_MODEL"` in the audit2 NEW text for `scripts/gan-harness.sh` — a shell *variable*, not a literal pin. The file is deleted outright by fix16 D6 (`fix16.py` `DELETE_FILES`: `"scripts/gan-harness.sh"`); it does not exist in the built tree (`ls: No such file or directory`). Nothing ships.
- **:15142 (c1) — not a live pin.** Audit7 NEW text for `skills/continuous-learning-v2/scripts/instinct-cli.py`: `content += "model: sonnet\n---\n"` — a Python generator that would emit a `model: sonnet` frontmatter at runtime. Fix16 re-pins it: the shipped file's line 2017 reads `content += "model: cursor-grok-4.6-high-fast\n---\n"`. The `model: sonnet` does not survive to the tree (0 `sonnet` hits tree-wide).
- **Other model-word (c1) lines — all resolved by fix16:** `:5124` `Haiku agent` (continuous-learning/SKILL.md) → shipped as `Grok 4.6 High Fast agent` (:127); `:6925` `400k Opus 4.x` (strategic-compact/SKILL.md) → shipped as `400k Grok 4.7 High 4.x` — **see minor finding M1** (the `4.x` residue); `:8377` `Claude Opus + an external model` (ui-ux-pro-max/SKILL.md) → the NICE/NAUGHTY block is gone from the shipped file (0 `NAUGHTY` hits); `:13020` `--gen-model haiku --model sonnet` (skill-comply/SKILL.md) → the skill file is not shipped at all; `:14258` `|| 'haiku'` (llm-summary.js) → fix16 D12 deletes `scripts/lib/llm-summary.js` (absent from the tree).
- **(c1) NEW text containing banned terms is expected, not a defect, in this build:** build.sh encodes the audit history as (old → new) patches; several audit-fix NEW texts still mention Claude/Codex (e.g. the Fix 5 `Claude Code only` labels) because those audits predate fix #16. Fix16 — the final build step, running after every audit patch — rewrites them (`Cursor only`, Grok slugs, deletions) and then self-checks the whole tree to 0. Evidence it worked: tree grep 0 across all six banned terms; `fix16-run-log.md:741-754` self-check all `0`; builds 13/14 exit 0.

### Full inventory table (all 798 hits: build.sh line, class, detail, text truncated to 120 chars)

| Line | Class | Detail | Text |
|---:|---|---|---|
| 150 | b | bash comment | # Pin ECC agent models to Grok IDs (fix #16). The install ships bare Claude aliases |
| 151 | b | bash comment | # (sonnet/opus/haiku), which are not Cursor model IDs. Map: sonnet -> |
| 152 | b | bash comment | # cursor-grok-4.6-high-fast, opus -> grok-4.7-high, haiku -> |
| 157 | a | dict key (OLD-side mapping) | mapping = {"sonnet": "cursor-grok-4.6-high-fast", "opus": "grok-4.7-high", "haiku": "cursor-grok-4.6-high-fast"} |
| 164 | a | re.search pattern | m = re.search(r"^model: (sonnet\|opus\|haiku)\s*$", txt, re.M) |
| 174 | b | bash comment | # Claude Code review loop the plugin does not ship). Drop it. |
| 210 | b | bash comment | # only the opus bracket pin was removed; cursor-grok-4.6-high-fast remains |
| 265 | c3 | build-time source path (cp) | cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" "$PLUGIN_DIR/skills/ui-ux-pro-max" |
| 298 | c3 | build-time source path (cp) | cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" "$PLUGIN_DIR/skills/hackathon-pitch" |
| 414 | b | python comment | # or by a Claude Code ~/.claude/rules/ path, which is not a plugin path) |
| 415 | a | re.compile pattern | pat_file = re.compile(rf"(?<!ecc/)(?<!claude/rules/)({RULE_DIRS})/({RULE_FILES})\.md") |
| 473 | b | bash comment | # The stock example installs quality-gate.py as a Claude Code Stop hook at |
| 474 | b | bash comment | # ~/.claude/scripts/. That path does not exist in Cursor, and an automatic |
| 486 | a | assign old = (OLD-side text) | mkdir -p ~/.claude/scripts |
| 487 | a | assign old = (OLD-side text) | cp skills/delivery-gate/hooks/quality-gate.py ~/.claude/scripts/ |
| 490 | a | assign old = (OLD-side text) | Add to `~/.claude/settings.json`: |
| 497 | a | assign old = (OLD-side text) | "command": "python3 ~/.claude/scripts/quality-gate.py", |
| 551 | c1 | append_desc arg 1 (appended note) | append_desc("agents-md-generator", ". Use ONLY when the user explicitly asks for an AGENTS.md file. Do not use for CLAUD |
| 593 | a | replace_desc_line arg 1 | "description: Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (s |
| 599 | a | replace_desc_line arg 1 | "description: Run a six-phase verification of a Claude Code session's work — build, type check, lint, tests with coverag |
| 602 | a | replace_desc_line arg 1 | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations,  |
| 603 | c1 | replace_desc_line arg 2 | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations,  |
| 888 | a | assign old = (OLD-side text) | - Setting up a new Claude Code project |
| 889 | a | assign old = (OLD-side text) | - After modifying `.claude/settings.json`, `CLAUDE.md`, or MCP configs |
| 891 | a | assign old = (OLD-side text) | - When onboarding to a new repository with existing Claude Code configs |
| 944 | a | subs pair elem 0 (OLD) | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary |
| 945 | c1 | subs pair elem 1 (NEW) | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary |
| 1035 | a | subs pair elem 0 (OLD) | "uv run python -m scripts.run --dry-run ~/.claude/skills/search-first/SKILL.md", |
| 1036 | c1 | subs pair elem 1 (NEW) | "uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md", |
| 1535 | a | subs pair elem 0 (OLD) | ("""Summarize local Claude Code spend by day, model, and session from the metrics |
| 1541 | a | subs pair elem 0 (OLD) | `~/.claude/metrics/costs.jsonl`. Each row is a **cumulative snapshot for that |
| 1548 | c1 | subs pair elem 1 (NEW) | """Summarize local Claude Code spend by day, model, and session from the metrics |
| 1554 | c1 | subs pair elem 1 (NEW) | `~/.claude/metrics/costs.jsonl` (Claude Code only — no Cursor equivalent in this plugin). Each row is a **cumulative sna |
| 1567 | a | subs pair elem 0 (OLD) | 1. Check that `~/.claude/metrics/costs.jsonl` exists. If it does not, tell the |
| 1580 | c1 | subs pair elem 1 (NEW) | 1. Check that `~/.claude/metrics/costs.jsonl` (Claude Code only) exists. If it does not, tell the |
| 2213 | a | subs pair elem 0 (OLD) | - **Global** (`~/.claude/skills/<pattern-name>/SKILL.md`): Generic patterns usable across 2+ projects (bash compatibilit |
| 2214 | a | subs pair elem 0 (OLD) | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a par |
| 2216 | a | subs pair elem 0 (OLD) | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 2227 | c1 | subs pair elem 1 (NEW) | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a par |
| 2229 | c1 | subs pair elem 1 (NEW) | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 2239 | a | subs pair elem 0 (OLD) | `~/.claude/skills/`, project `.claude/skills/`, or `MEMORY.md` as |
| 2252 | c1 | subs pair elem 1 (NEW) | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| 2265 | a | subs pair elem 0 (OLD) | - [ ] Grep `~/.claude/skills/` and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 2278 | c1 | subs pair elem 1 (NEW) | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 2293 | a | subs pair elem 0 (OLD) | Create a skill at `~/.claude/skills/<pattern-name>/SKILL.md`: |
| 2319 | a | subs pair elem 0 (OLD) | inside the approved skill root (`~/.claude/skills/`). |
| 2345 | a | subs pair elem 0 (OLD) | 5. Save to `~/.claude/skills/<pattern-name>/SKILL.md` |
| 2373 | a | subs pair elem 0 (OLD) | The CLI scans local Claude transcript JSONL files under |
| 2374 | a | subs pair elem 0 (OLD) | `~/.claude/projects/**` and reports stale `ScheduleWakeup` calls or `Bash` |
| 2400 | a | subs pair elem 0 (OLD) | - `ecc loop-status --watch --write-dir ~/.claude/loops` maintains |
| 2444 | a | subs pair elem 0 (OLD) | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 2446 | a | subs pair elem 0 (OLD) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2456 | c1 | subs pair elem 1 (NEW) | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 2458 | c1 | subs pair elem 1 (NEW) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2547 | a | subs pair elem 0 (OLD) | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and  |
| 2549 | a | subs pair elem 0 (OLD) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2559 | c1 | subs pair elem 1 (NEW) | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and  |
| 2561 | c1 | subs pair elem 1 (NEW) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2569 | a | subs pair elem 0 (OLD) | ('- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missing, must confirm fir |
| 2570 | c1 | subs pair elem 1 (NEW) | '- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missing, must confirm firs |
| 2646 | a | subs pair elem 0 (OLD) | ("""\| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 2666 | c1 | subs pair elem 1 (NEW) | """\| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 2685 | a | subs pair elem 0 (OLD) | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| 2686 | a | subs pair elem 0 (OLD) | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| 2692 | a | subs pair elem 0 (OLD) | - Codex: Handle backend part |
| 2701 | c1 | subs pair elem 1 (NEW) | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| 2702 | c1 | subs pair elem 1 (NEW) | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| 2708 | c1 | subs pair elem 1 (NEW) | - Codex: Handle backend part |
| 2720 | a | subs pair elem 0 (OLD) | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| 2722 | a | subs pair elem 0 (OLD) | 1. **Codex Review** (`run_in_background: true`): |
| 2723 | a | subs pair elem 0 (OLD) | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| 2728 | a | subs pair elem 0 (OLD) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| 2736 | a | subs pair elem 0 (OLD) | 1. Synthesize Codex + Antigravity review feedback |
| 2737 | a | subs pair elem 0 (OLD) | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| 2743 | c1 | subs pair elem 1 (NEW) | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| 2745 | c1 | subs pair elem 1 (NEW) | 1. **Codex Review** (run in parallel): |
| 2746 | c1 | subs pair elem 1 (NEW) | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| 2751 | c1 | subs pair elem 1 (NEW) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| 2759 | c1 | subs pair elem 1 (NEW) | 1. Synthesize Codex + Antigravity review feedback |
| 2760 | c1 | subs pair elem 1 (NEW) | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| 2769 | a | subs pair elem 0 (OLD) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2781 | c1 | subs pair elem 1 (NEW) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2872 | a | subs pair elem 0 (OLD) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2884 | c1 | subs pair elem 1 (NEW) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 2898 | a | subs pair elem 0 (OLD) | - **Mandatory Parallel**: Codex/Antigravity calls MUST use `run_in_background: true` (including single model calls, to a |
| 2899 | a | subs pair elem 0 (OLD) | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by Claude |
| 2901 | a | subs pair elem 0 (OLD) | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify  |
| 2911 | c1 | subs pair elem 1 (NEW) | - **Mandatory Parallel**: Codex/Antigravity calls MUST run in parallel (including single model calls, to avoid blocking  |
| 2912 | c1 | subs pair elem 1 (NEW) | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by Claude |
| 2914 | c1 | subs pair elem 1 (NEW) | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify  |
| 2918 | a | subs pair elem 0 (OLD) | ('- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modif |
| 2919 | c1 | subs pair elem 1 (NEW) | '- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify |
| 2945 | a | subs pair elem 0 (OLD) | ("""\| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 2965 | c1 | subs pair elem 1 (NEW) | """\| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 2989 | a | subs pair elem 0 (OLD) | **Parallel call** Codex and Antigravity (`run_in_background: true`): |
| 2993 | a | subs pair elem 0 (OLD) | 1. **Codex Backend Analysis**: |
| 2994 | a | subs pair elem 0 (OLD) | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| 3002 | c1 | subs pair elem 1 (NEW) | **Parallel call** Codex and Antigravity (run them in parallel): |
| 3006 | c1 | subs pair elem 1 (NEW) | 1. **Codex Backend Analysis**: |
| 3007 | c1 | subs pair elem 1 (NEW) | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| 3011 | a | subs pair elem 0 (OLD) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| 3015 | a | subs pair elem 0 (OLD) | Wait for both models' complete results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION` |
| 3024 | c1 | subs pair elem 1 (NEW) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| 3028 | c1 | subs pair elem 1 (NEW) | Wait for both models' complete results (their returned output). **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SE |
| 3038 | a | subs pair elem 0 (OLD) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| 3043 | a | subs pair elem 0 (OLD) | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| 3051 | c1 | subs pair elem 1 (NEW) | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| 3056 | c1 | subs pair elem 1 (NEW) | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| 3066 | a | subs pair elem 0 (OLD) | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intellig |
| 3068 | a | subs pair elem 0 (OLD) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 3078 | c1 | subs pair elem 1 (NEW) | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intellig |
| 3080 | c1 | subs pair elem 1 (NEW) | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initial |
| 3088 | a | subs pair elem 0 (OLD) | ('- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Specification\n\n**Ca |
| 3089 | c1 | subs pair elem 1 (NEW) | '- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Specification\n\n**Cal |
| 3140 | a | subs pair elem 0 (OLD) | ("""\| Analysis \| `~/.claude/.ccg/prompts/codex/analyzer.md` \| `~/.claude/.ccg/prompts/antigravity/analyzer.md` \| |
| 3141 | a | subs pair elem 0 (OLD) | \| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 3142 | a | subs pair elem 0 (OLD) | \| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 3164 | c1 | subs pair elem 1 (NEW) | """\| Analysis \| `~/.claude/.ccg/prompts/codex/analyzer.md` \| `~/.claude/.ccg/prompts/antigravity/analyzer.md` \| |
| 3165 | c1 | subs pair elem 1 (NEW) | \| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 3166 | c1 | subs pair elem 1 (NEW) | \| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 3199 | a | subs pair elem 0 (OLD) | node scripts/orchestrate-worktrees.js .claude/plan/workflow-e2e-test.json --execute |
| 3233 | a | subs pair elem 0 (OLD) | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| 3236 | a | subs pair elem 0 (OLD) | Wait for results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3250 | c1 | subs pair elem 1 (NEW) | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| 3253 | c1 | subs pair elem 1 (NEW) | Wait for their returned output. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3263 | a | subs pair elem 0 (OLD) | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| 3270 | a | subs pair elem 0 (OLD) | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/task-name.md` after us |
| 3276 | c1 | subs pair elem 1 (NEW) | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| 3283 | c1 | subs pair elem 1 (NEW) | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/task-name.md` after us |
| 3289 | a | subs pair elem 0 (OLD) | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| 3302 | c1 | subs pair elem 1 (NEW) | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| 3501 | a | subs pair elem 0 (OLD) | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gemini`, `opencode`, `c |
| 3523 | c1 | subs pair elem 1 (NEW) | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gemini`, `opencode`, `c |
| 3549 | a | subs pair elem 0 (OLD) | ## CLAUDE.md Guidance |
| 3551 | a | subs pair elem 0 (OLD) | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it minimal:""", |
| 3563 | c1 | subs pair elem 1 (NEW) | ## CLAUDE.md Guidance |
| 3565 | c1 | subs pair elem 1 (NEW) | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it minimal:"""), |
| 3567 | a | subs pair elem 0 (OLD) | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| 3577 | c1 | subs pair elem 1 (NEW) | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| 3848 | a | subs pair elem 0 (OLD) | #### Reviewer A: Claude Agent (always runs) |
| 3850 | a | subs pair elem 0 (OLD) | Launch an Agent (subagent_type: `code-reviewer`, model: `opus`) with the full rubric + all files under review. The promp |
| 3856 | a | subs pair elem 0 (OLD) | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| 3861 | c1 | subs pair elem 1 (NEW) | #### Reviewer A: Claude Agent (always runs) |
| 3869 | c1 | subs pair elem 1 (NEW) | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| 3876 | a | subs pair elem 0 (OLD) | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second Claude Agent (subagent_type: `code- |
| 3889 | c1 | subs pair elem 1 (NEW) | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `ecc-code-reviewer`  |
| 3904 | a | subs pair elem 0 (OLD) | - `path` (optional): defaults to the current project. Use a `.claude/` path, a repo root, or a checked-in template direc |
| 3927 | a | subs pair elem 0 (OLD) | description: Manage Claude Code session history, aliases, and session metadata. |
| 3932 | a | subs pair elem 0 (OLD) | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/session-data/` with legac |
| 3940 | c1 | subs pair elem 1 (NEW) | description: Manage Claude Code session history, aliases, and session metadata. |
| 3945 | c1 | subs pair elem 1 (NEW) | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/session-data/` with legac |
| 3958 | a | subs pair elem 0 (OLD) | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.claude/sessions/` |
| 3959 | a | subs pair elem 0 (OLD) | - Aliases are stored in `~/.claude/session-aliases.json` |
| 3969 | c1 | subs pair elem 1 (NEW) | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.claude/sessions/` (Claud |
| 3970 | c1 | subs pair elem 1 (NEW) | - Aliases are stored in `~/.claude/session-aliases.json` (Claude Code only) |
| 3984 | a | subs pair elem 0 (OLD) | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that teach Claude your team |
| 3993 | c1 | subs pair elem 1 (NEW) | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that teach Claude your team |
| 4027 | a | subs pair elem 0 (OLD) | Located in `~/.claude/agents/`: |
| 4121 | a | subs pair elem 0 (OLD) | Note: ECC-managed installs set `"includeCoAuthoredBy": false` in `~/.claude/settings.json`, so commits carry no `Co-Auth |
| 4134 | c1 | subs pair elem 1 (NEW) | Note: this paragraph describes Claude Code installs and does not apply to this Cursor plugin install — Cursor commit att |
| 4165 | a | subs pair elem 0 (OLD) | - Configure `permissions.allow` rules in `~/.claude/settings.json` (or a project's `.claude/settings.json`) instead |
| 4182 | c1 | subs pair elem 1 (NEW) | - Configure Cursor permissions in the project's Cursor settings instead of Claude Code's `~/.claude/settings.json`. |
| 4201 | a | subs pair elem 0 (OLD) | **Haiku 4.5** (90% of Sonnet capability, 3x cost savings): |
| 4206 | a | subs pair elem 0 (OLD) | **Sonnet 5** (Best coding model): |
| 4211 | a | subs pair elem 0 (OLD) | **Opus 5** (Deepest reasoning): |
| 4246 | a | subs pair elem 0 (OLD) | In Claude Code, adaptive reasoning lets the model choose how much to think for each task. |
| 4247 | a | subs pair elem 0 (OLD) | For Fable models, Sonnet 5 and later, and Opus 4.7 and later, use effort to control reasoning |
| 4251 | a | subs pair elem 0 (OLD) | - **Effort**: Use `/effort` in a session, `--effort <level>` at launch, or `CLAUDE_CODE_EFFORT_LEVEL`. Save a per-model  |
| 4252 | a | subs pair elem 0 (OLD) | - **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux), or `alwaysThinkingEnabled` in settings. These cannot disable thi |
| 4253 | a | subs pair elem 0 (OLD) | - **Fixed budget**: Claude Code ignores positive `MAX_THINKING_TOKENS` values on adaptive reasoning models. On Opus 4.6  |
| 4256 | a | subs pair elem 0 (OLD) | See [Claude Code model configuration](https://code.claude.com/docs/en/model-config#adjust-effort-level) |
| 4257 | a | subs pair elem 0 (OLD) | and [environment variables](https://code.claude.com/docs/en/env-vars) for supported controls. |
| 4490 | a | subs pair elem 0 (OLD) | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| 4503 | c1 | subs pair elem 1 (NEW) | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| 4519 | a | subs pair elem 0 (OLD) | <!-- .claude/commands/bug-check.md --> |
| 4588 | a | subs pair elem 0 (OLD) | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 4596 | c1 | subs pair elem 1 (NEW) | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 4612 | a | subs pair elem 0 (OLD) | `~/.claude/skills/ck/commands/` for a manual install, or the ck skill inside the ECC |
| 4613 | a | subs pair elem 0 (OLD) | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| 4614 | a | subs pair elem 0 (OLD) | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| 4629 | c1 | subs pair elem 1 (NEW) | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| 4630 | c1 | subs pair elem 1 (NEW) | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| 4641 | a | subs pair elem 0 (OLD) | ~/.claude/ck/ |
| 4669 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| 4682 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| 4721 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| 4730 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4743 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| 4752 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4757 | a | subs pair elem 0 (OLD) | ("""node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4765 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| 4776 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4779 | c1 | subs pair elem 1 (NEW) | """node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4787 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| 4798 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4801 | a | subs pair elem 0 (OLD) | ("""node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4809 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| 4813 | a | subs pair elem 0 (OLD) | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run""", |
| 4814 | c1 | subs pair elem 1 (NEW) | """node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4822 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| 4826 | c1 | subs pair elem 1 (NEW) | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run"""), |
| 4827 | a | subs pair elem 0 (OLD) | ('\n---\n\n## SessionStart Hook\n\nThe hook at `hooks/session-start.mjs` in this skill\'s directory must be registered i |
| 4829 | a | subs pair elem 0 (OLD) | ("""unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| 4840 | c1 | subs pair elem 1 (NEW) | """unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| 4970 | a | subs pair elem 0 (OLD) | description: Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, |
| 4975 | a | subs pair elem 0 (OLD) | # Config GC — Garbage Collection for Claude Code Setups |
| 4979 | c1 | subs pair elem 1 (NEW) | description: Garbage collection for your Claude Code configuration (Claude Code only — this skill targets a Claude Code  |
| 4984 | c1 | subs pair elem 1 (NEW) | # Config GC — Garbage Collection for Claude Code Setups |
| 5013 | a | subs pair elem 0 (OLD) | \| Codex CLI \| `/status` \| Shows current token usage and remaining context capacity. Use `/statusline` and enable **Conte |
| 5014 | a | subs pair elem 0 (OLD) | \| Codex app \| `/status` \| Shows current thread context usage and rate limits. \| |
| 5015 | a | subs pair elem 0 (OLD) | \| Claude Code \| `/context` \| Shows the live context breakdown. Use `/context all` for expanded items. \| |
| 5018 | a | subs pair elem 0 (OLD) | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/cli/slash-commands) a |
| 5028 | c1 | subs pair elem 1 (NEW) | \| Codex CLI (Codex only) \| `/status` \| Shows current token usage and remaining context capacity. Use `/statusline` and e |
| 5029 | c1 | subs pair elem 1 (NEW) | \| Codex app (Codex only) \| `/status` \| Shows current thread context usage and rate limits. \| |
| 5030 | c1 | subs pair elem 1 (NEW) | \| Claude Code (Claude Code only) \| `/context` \| Shows the live context breakdown. Use `/context all` for expanded items. |
| 5033 | c1 | subs pair elem 1 (NEW) | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/cli/slash-commands) a |
| 5043 | a | subs pair elem 0 (OLD) | [`/context` and `/usage` commands (`/cost` is an alias)](https://code.claude.com/docs/en/commands). |
| 5051 | c1 | subs pair elem 1 (NEW) | [`/context` and `/usage` commands (Claude Code only; `/cost` is an alias)](https://code.claude.com/docs/en/commands). |
| 5093 | a | subs pair elem 0 (OLD) | No extra `settings.json` hook block is required. Claude Code v2.1+ auto-loads the plugin `hooks/hooks.json`, and `observ |
| 5095 | a | subs pair elem 0 (OLD) | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` |
| 5097 | a | subs pair elem 0 (OLD) | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| 5108 | c1 | subs pair elem 1 (NEW) | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` |
| 5110 | c1 | subs pair elem 1 (NEW) | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| 5116 | a | subs pair elem 0 (OLD) | 2. **Background observer** - Haiku agent analyzing in parallel |
| 5124 | c1 | subs pair elem 1 (NEW) | 2. **Background observer** - Haiku agent analyzing in parallel |
| 5133 | a | subs pair elem 0 (OLD) | ('- suppresses model-visible skill instructions and shell environment inheritance;\n- uses an ephemeral, read-only sessi |
| 5155 | a | subs pair elem 0 (OLD) | - the in-context Claude voice |
| 5236 | a | subs pair elem 0 (OLD) | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| 5249 | c1 | subs pair elem 1 (NEW) | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| 5293 | a | subs pair elem 0 (OLD) | # Delivery Gate — Mechanical Quality Gate for Claude Code |
| 5295 | a | subs pair elem 0 (OLD) | A **Stop hook** that checks three things before Claude can finish a session, using only **deterministic checks** — file  |
| 5329 | a | subs pair elem 0 (OLD) | The hook blocks a given Stop at most once. When Claude Code re-runs it with `stop_hook_active: true` (Claude already con |
| 5333 | a | subs pair elem 0 (OLD) | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a different failure mode: the |
| 5350 | c1 | subs pair elem 1 (NEW) | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a different failure mode: the |
| 5359 | a | subs pair elem 0 (OLD) | Create these files in your project's memory directory (`~/.claude/projects/<encoded-project-path>/memory/`, where every  |
| 5751 | a | subs pair elem 0 (OLD) | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conf |
| 5763 | c1 | subs pair elem 1 (NEW) | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conf |
| 5798 | a | subs pair elem 0 (OLD) | ('- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & State-Control Rules]**  |
| 5799 | c1 | subs pair elem 1 (NEW) | '- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & State-Control Rules]** — |
| 6178 | a | subs pair elem 0 (OLD) | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 6202 | c1 | subs pair elem 1 (NEW) | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 6376 | a | subs pair elem 0 (OLD) | ### Pattern A: Claude Code Subagents (Recommended) |
| 6381 | a | subs pair elem 0 (OLD) | # In a Claude Code session, use the Agent tool to spawn reviewers |
| 6389 | c1 | subs pair elem 1 (NEW) | ### Pattern A: Claude Code Subagents (Recommended) |
| 6425 | a | subs pair elem 0 (OLD) | description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, a |
| 6432 | a | subs pair elem 0 (OLD) | Audit your Claude Code configuration for security issues using [AgentShield](https://github.com/affaan-m/agentshield). |
| 6461 | a | subs pair elem 0 (OLD) | \| `CLAUDE.md` \| Hardcoded secrets, auto-run instructions, prompt injection patterns \| |
| 6487 | a | subs pair elem 0 (OLD) | Run against the current project's `.claude/` directory: |
| 6494 | a | subs pair elem 0 (OLD) | npx ecc-agentshield scan --path /path/to/.claude |
| 6527 | a | subs pair elem 0 (OLD) | Scaffold a new secure `.claude/` configuration from scratch: |
| 6553 | a | subs pair elem 0 (OLD) | - `CLAUDE.md` with security best practices |
| 6579 | a | subs pair elem 0 (OLD) | - Auto-run instructions in CLAUDE.md (prompt injection vector) |
| 6607 | a | subs pair elem 0 (OLD) | Slash command (`/skill-stocktake`) that audits all Claude skills and commands using a quality checklist + AI holistic ju |
| 6633 | a | subs pair elem 0 (OLD) | \| `~/.claude/skills/` \| Global skills (all projects) \| |
| 6634 | a | subs pair elem 0 (OLD) | \| `{cwd}/.claude/skills/` \| Project-level skills (if the directory exists) \| |
| 6661 | a | subs pair elem 0 (OLD) | If the project has no `.claude/skills/` directory, only global skills and commands are evaluated. |
| 6681 | a | subs pair elem 0 (OLD) | ('\|------\|---------\|---------\|\n\| Quick Scan \| `results.json` exists (default) \| 5–10 min \|\n\| Full Stocktake \| `results |
| 6683 | a | subs pair elem 0 (OLD) | ('\nRun this entire block in **one Bash invocation**. It prints the inventory for the agent and initializes a new full r |
| 6685 | a | subs pair elem 0 (OLD) | ('      \| .mode = "full"\n      \| .batch_progress = {\n          total: ($inventory.skills \| length),\n          evaluat |
| 6687 | a | subs pair elem 0 (OLD) | ('\nThe subagent reads each assigned skill, applies the checklist, and returns a JSON object with a `skills` map keyed b |
| 6695 | a | subs pair elem 0 (OLD) | RESULTS_JSON=~/.claude/skills/skill-stocktake/results.json |
| 6715 | a | subs pair elem 0 (OLD) | ('    if (.skills \| length) == .batch_progress.total then\n      {skills: {}, mode: "full", batch_progress: (.batch_prog |
| 6723 | a | subs pair elem 0 (OLD) | `~/.claude/skills/skill-stocktake/results.json`: |
| 6749 | a | subs pair elem 0 (OLD) | "~/.claude/skills/skill-name/SKILL.md": { |
| 6750 | a | subs pair elem 0 (OLD) | "path": "~/.claude/skills/skill-name/SKILL.md", |
| 6884 | a | subs pair elem 0 (OLD) | **Installed as a plugin?** No setup is needed. The plugin's `hooks/hooks.json` already registers `suggest-compact.js` (h |
| 6886 | a | subs pair elem 0 (OLD) | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 6904 | c1 | subs pair elem 1 (NEW) | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings.json` — `~/.claude/s |
| 6906 | c1 | subs pair elem 1 (NEW) | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 6912 | a | subs pair elem 0 (OLD) | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection. Set this for large-w |
| 6913 | a | subs pair elem 0 (OLD) | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smaller than the model's c |
| 6925 | c1 | subs pair elem 1 (NEW) | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection. Set this for large-w |
| 6926 | c1 | subs pair elem 1 (NEW) | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smaller than the model's c |
| 6971 | a | subs pair elem 0 (OLD) | # Use the configured plugin root or standalone install (~/.claude or |
| 6972 | a | subs pair elem 0 (OLD) | # $CLAUDE_CONFIG_DIR). For a reviewed and explicitly authorized ECC checkout: |
| 6973 | a | subs pair elem 0 (OLD) | # export CLAUDE_PLUGIN_ROOT="/absolute/path/to/reviewed/ECC" |
| 6974 | a | subs pair elem 0 (OLD) | ECC_ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}" |
| 6975 | a | subs pair elem 0 (OLD) | [ -f "$ECC_ROOT/scripts/setup-package-manager.js" ] \|\| { echo "ECC scripts not found in the selected root (set CLAUDE_PL |
| 6979 | a | subs pair elem 0 (OLD) | The resolution lines use the configured plugin root or standalone install and stop when the selected root lacks the help |
| 6981 | a | subs pair elem 0 (OLD) | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/package-man |
| 7001 | c1 | subs pair elem 1 (NEW) | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/package-man |
| 7060 | a | subs pair elem 0 (OLD) | A comprehensive verification system for Claude Code sessions. |
| 7105 | a | subs pair elem 0 (OLD) | description: Automatically generate comprehensive AGENTS.md files that teach AI agents how to work with a repository's s |
| 7270 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --domain <domain> |
| 7296 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<product_type> <industry> <keywords>" --d |
| 7303 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service" --design-sys |
| 7336 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --persist -p "Pr |
| 7362 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --variance <1-10 |
| 7388 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "internal analytics dashboard" --design-sy |
| 7394 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --domain <domain> [-n <max_res |
| 7426 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --stack <stack> |
| 7452 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "AI search tool modern minimal" --design-s |
| 7455 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "keyboard focus modal" --domain ux |
| 7458 | a | subs pair elem 0 (OLD) | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bundle" --stack nextjs |
| 7665 | a | subs pair elem 0 (OLD) | - **Rules are system-injected**: `.claude/rules/*.md` files load automatically every session. Unlike prompt instructions |
| 7670 | a | subs pair elem 0 (OLD) | claude /mail                    # Email-only triage |
| 7671 | a | subs pair elem 0 (OLD) | claude /slack                   # Slack-only triage |
| 7672 | a | subs pair elem 0 (OLD) | claude /today                   # All channels + calendar + todo |
| 7673 | a | subs pair elem 0 (OLD) | claude /schedule-reply "Reply to Sarah about the board meeting" |
| 7678 | a | subs pair elem 0 (OLD) | - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| 7786 | a | subs pair elem 0 (OLD) | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review,  |
| 7788 | a | subs pair elem 0 (OLD) | model: opus |
| 7793 | a | subs pair elem 0 (OLD) | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex  |
| 7795 | a | subs pair elem 0 (OLD) | This command runs on **Opus** (`model: opus`). Opus orchestrates, verifies findings, checks every diff, and runs the tes |
| 7800 | a | subs pair elem 0 (OLD) | - Keep Claude as the writer: Astra reviews in a read-only sandbox and returns a structured verdict, never a patch. The s |
| 7805 | a | subs pair elem 0 (OLD) | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| 7806 | a | subs pair elem 0 (OLD) | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_MODEL`)""", |
| 7808 | c1 | subs pair elem 1 (NEW) | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review,  |
| 7815 | c1 | subs pair elem 1 (NEW) | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex  |
| 7827 | c1 | subs pair elem 1 (NEW) | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| 7828 | c1 | subs pair elem 1 (NEW) | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_MODEL`)"""), |
| 7829 | a | subs pair elem 0 (OLD) | ('- **PASS** with MEDIUM/LOW findings: list them, fix the ones that are clearly correct, and finish.\n- **FAIL** (any CR |
| 7831 | a | subs pair elem 0 (OLD) | ('     ```bash\n     node <astra-review.js path> --consent-to-openai --fix-findings <dir>/confirmed.json \\\n       --in |
| 7839 | a | subs pair elem 0 (OLD) | Fixer:      [Fable \| Astra (Fable usage limit) \| Opus] |
| 7862 | a | subs pair elem 0 (OLD) | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports |
| 7864 | a | subs pair elem 0 (OLD) | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 7866 | a | subs pair elem 0 (OLD) | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 7872 | c1 | subs pair elem 1 (NEW) | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports |
| 7874 | c1 | subs pair elem 1 (NEW) | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 7876 | c1 | subs pair elem 1 (NEW) | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 7889 | a | subs pair elem 0 (OLD) | 3. Log checkpoint to `.claude/checkpoints.log`: |
| 7892 | a | subs pair elem 0 (OLD) | echo "$(date +%Y-%m-%d-%H:%M) \| $CHECKPOINT_NAME \| $(git rev-parse --short HEAD)" >> .claude/checkpoints.log |
| 7902 | c1 | subs pair elem 1 (NEW) | 3. Log checkpoint to `.claude/checkpoints.log`: |
| 7905 | c1 | subs pair elem 1 (NEW) | echo "$(date +%Y-%m-%d-%H:%M) \| $CHECKPOINT_NAME \| $(git rev-parse --short HEAD)" >> .claude/checkpoints.log |
| 7915 | a | subs pair elem 0 (OLD) | - `/security-scan` for Claude/OpenCode configuration security review |
| 8074 | a | subs pair elem 0 (OLD) | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8087 | c1 | subs pair elem 1 (NEW) | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8102 | a | subs pair elem 0 (OLD) | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8115 | c1 | subs pair elem 1 (NEW) | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8300 | a | subs pair elem 0 (OLD) | ("""> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| 8302 | a | subs pair elem 0 (OLD) | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts. Use `/prp-implemen |
| 8313 | c1 | subs pair elem 1 (NEW) | """> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| 8315 | c1 | subs pair elem 1 (NEW) | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts. Use `/prp-implemen |
| 8332 | a | subs pair elem 0 (OLD) | **Claude Commands:** /pm2-all, /pm2-all-stop, /pm2-{port}, /pm2-{port}-stop, /pm2-logs, /pm2-status |
| 8364 | a | subs pair elem 0 (OLD) | Run two independent reviewers (Claude Opus + an external model) against the current task output. Both must return NICE b |
| 8377 | c1 | subs pair elem 1 (NEW) | Run two independent reviewers (Claude Opus + an external model) against the current task output. Both must return NICE b |
| 8408 | a | subs pair elem 0 (OLD) | #### Reviewer A: Claude Agent (always runs) |
| 8416 | a | subs pair elem 0 (OLD) | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| 8421 | c1 | subs pair elem 1 (NEW) | #### Reviewer A: Claude Agent (always runs) |
| 8429 | c1 | subs pair elem 1 (NEW) | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| 8436 | a | subs pair elem 0 (OLD) | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `ecc-code-reviewer`  |
| 8449 | c1 | subs pair elem 1 (NEW) | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `code-reviewer` with |
| 8486 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8606 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8638 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8670 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8702 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8732 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8762 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8820 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8852 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8884 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 8994 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 9024 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 9056 | a | subs pair elem 0 (OLD) | Configure in `~/.claude/settings.json`: |
| 9494 | a | subs pair elem 0 (OLD) | ('1. CLAUDE.md (commands, architecture, key files)\n2. setup.sh (one-command bootstrap, make executable)\n3. README.md ( |
| 9495 | c1 | subs pair elem 1 (NEW) | """1. CLAUDE.md (commands, architecture, key files) |
| 9738 | a | subs pair elem 0 (OLD) | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 9762 | c1 | subs pair elem 1 (NEW) | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 9905 | a | subs pair elem 0 (OLD) | ('\nBe rigorous. Your job is to find problems, not to approve.\n"""\n```\n\n```python\n# Spawn reviewers in parallel (Cl |
| 11064 | a | subs pair elem 0 (OLD) | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, L |
| 11074 | c1 | subs pair elem 1 (NEW) | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, L |
| 11575 | a | subs pair elem 0 (OLD) | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review,  |
| 11582 | a | subs pair elem 0 (OLD) | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex  |
| 11592 | c1 | subs pair elem 1 (NEW) | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review,  |
| 11598 | c1 | subs pair elem 1 (NEW) | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex  |
| 11612 | a | subs pair elem 0 (OLD) | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports |
| 11614 | a | subs pair elem 0 (OLD) | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 11616 | a | subs pair elem 0 (OLD) | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 11624 | c1 | subs pair elem 1 (NEW) | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports |
| 11626 | c1 | subs pair elem 1 (NEW) | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 11628 | c1 | subs pair elem 1 (NEW) | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 11634 | a | subs pair elem 0 (OLD) | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary  |
| 11640 | a | subs pair elem 0 (OLD) | Summarize local Claude Code spend by day, model, and session from the metrics""", |
| 11642 | c1 | subs pair elem 1 (NEW) | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary  |
| 11648 | c1 | subs pair elem 1 (NEW) | Summarize local Claude Code spend by day, model, and session from the metrics"""), |
| 11654 | a | subs pair elem 0 (OLD) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--generate] |
| 11657 | a | subs pair elem 0 (OLD) | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11660 | a | subs pair elem 0 (OLD) | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py evolve [--generate] |
| 11670 | c1 | subs pair elem 1 (NEW) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--generate] |
| 11673 | c1 | subs pair elem 1 (NEW) | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11706 | a | subs pair elem 0 (OLD) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [ |
| 11709 | a | subs pair elem 0 (OLD) | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11712 | a | subs pair elem 0 (OLD) | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url> |
| 11722 | c1 | subs pair elem 1 (NEW) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [ |
| 11725 | c1 | subs pair elem 1 (NEW) | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11743 | a | subs pair elem 0 (OLD) | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a par |
| 11745 | a | subs pair elem 0 (OLD) | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 11758 | c1 | subs pair elem 1 (NEW) | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 11769 | a | subs pair elem 0 (OLD) | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| 11795 | a | subs pair elem 0 (OLD) | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 11826 | c1 | subs pair elem 1 (NEW) | description: Inspect active loop state, progress, failure signals, and recommended intervention. (Claude Code only — sca |
| 11841 | a | subs pair elem 0 (OLD) | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 11849 | c1 | subs pair elem 1 (NEW) | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 11851 | a | subs pair elem 0 (OLD) | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Ini |
| 11863 | a | subs pair elem 0 (OLD) | - Codex-led, Gemini for auxiliary reference""", |
| 11864 | c1 | subs pair elem 1 (NEW) | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Init |
| 11876 | c1 | subs pair elem 1 (NEW) | - Codex-led, Gemini for auxiliary reference"""), |
| 11880 | a | subs pair elem 0 (OLD) | description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. |
| 11885 | a | subs pair elem 0 (OLD) | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and  |
| 11888 | c1 | subs pair elem 1 (NEW) | description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Requires  |
| 11893 | c1 | subs pair elem 1 (NEW) | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and  |
| 11913 | a | subs pair elem 0 (OLD) | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Ini |
| 11925 | a | subs pair elem 0 (OLD) | - Antigravity-led, Codex for auxiliary reference""", |
| 11926 | c1 | subs pair elem 1 (NEW) | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Init |
| 11938 | c1 | subs pair elem 1 (NEW) | - Antigravity-led, Codex for auxiliary reference"""), |
| 11947 | a | subs pair elem 0 (OLD) | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intellig |
| 11955 | c1 | subs pair elem 1 (NEW) | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intellig |
| 11962 | a | subs pair elem 0 (OLD) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| 11965 | a | subs pair elem 0 (OLD) | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11968 | a | subs pair elem 0 (OLD) | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py projects |
| 11978 | c1 | subs pair elem 1 (NEW) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| 11981 | c1 | subs pair elem 1 (NEW) | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11996 | a | subs pair elem 0 (OLD) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [instinct-id] [--force] [- |
| 11999 | a | subs pair elem 0 (OLD) | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 12002 | a | subs pair elem 0 (OLD) | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py promote [instinct-id] [--force] [--dry-run] |
| 12012 | c1 | subs pair elem 1 (NEW) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [instinct-id] [--force] [- |
| 12015 | c1 | subs pair elem 1 (NEW) | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 12030 | a | subs pair elem 0 (OLD) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| 12033 | a | subs pair elem 0 (OLD) | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 12036 | a | subs pair elem 0 (OLD) | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py prune |
| 12046 | c1 | subs pair elem 1 (NEW) | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| 12049 | c1 | subs pair elem 1 (NEW) | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 12062 | a | subs pair elem 0 (OLD) | description: Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where |
| 12070 | c1 | subs pair elem 1 (NEW) | description: Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where |
| 12080 | a | subs pair elem 0 (OLD) | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future se |
| 12088 | c1 | subs pair elem 1 (NEW) | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future se |
| 12195 | c1 | subs pair elem 1 (NEW) | Run hvigor build to check for ArkTS compilation errors. This was a Claude Code hook block; in Cursor, wire it as an `aft |
| 12199 | c1 | subs pair elem 1 (NEW) | Validate permission and ability declarations. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit |
| 12203 | c1 | subs pair elem 1 (NEW) | Reinstall dependencies. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hook |
| 12209 | c1 | subs pair elem 1 (NEW) | Warn when code contains V1 state management decorators. This was a Claude Code pre-write hook block; Cursor has no befor |
| 12339 | a | subs pair elem 0 (OLD) | { "type": "command", "command": "dart format $CLAUDE_FILE_PATHS" } |
| 12358 | c1 | subs pair elem 1 (NEW) | The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same behaviour as an `afterFil |
| 12378 | c1 | subs pair elem 1 (NEW) | Use the project's existing formatter entrypoint after edits. This was a Claude Code hook block; in Cursor, wire it as an |
| 12384 | c1 | subs pair elem 1 (NEW) | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the e |
| 12390 | c1 | subs pair elem 1 (NEW) | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the e |
| 12404 | c1 | subs pair elem 1 (NEW) | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the e |
| 12410 | c1 | subs pair elem 1 (NEW) | Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre-write |
| 12416 | c1 | subs pair elem 1 (NEW) | This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` event in `hooks/hooks.json`  |
| 12425 | a | subs pair elem 0 (OLD) | ('  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log "Launching Planner ag |
| 12426 | c1 | subs pair elem 1 (NEW) | '  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log "Launching Planner age |
| 12427 | a | subs pair elem 0 (OLD) | ('  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i-1))).md" ]; then\n   |
| 12428 | c1 | subs pair elem 1 (NEW) | '  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i-1))).md" ]; then\n    |
| 12429 | a | subs pair elem 0 (OLD) | ('    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    exit 1\n  fi\n\n  cla |
| 12430 | c1 | subs pair elem 1 (NEW) | '    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    exit 1\n  fi\n\n  clau |
| 12724 | a | subs pair elem 0 (OLD) | ("""- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| 12737 | c1 | subs pair elem 1 (NEW) | """- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| 12752 | a | subs pair elem 0 (OLD) | ('  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # doesn\'t kill the analy |
| 12753 | c1 | subs pair elem 1 (NEW) | '  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # doesn\'t kill the analys |
| 12834 | a | subs pair elem 0 (OLD) | description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based  |
| 12842 | a | subs pair elem 0 (OLD) | > Inspired by [Anthropic's Harness Design for Long-Running Application Development](https://www.anthropic.com/engineerin |
| 12844 | c1 | subs pair elem 1 (NEW) | '---\nname: gan-style-harness\ndescription: "GAN-inspired Generator-Evaluator agent harness for building high-quality ap |
| 12877 | a | subs pair elem 0 (OLD) | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on |
| 12886 | c1 | subs pair elem 1 (NEW) | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on |
| 12989 | c1 | subs pair elem 1 (NEW) | description: Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at  |
| 13001 | a | subs pair elem 0 (OLD) | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| 13004 | a | subs pair elem 0 (OLD) | uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md |
| 13007 | a | subs pair elem 0 (OLD) | uv run python -m scripts.run --gen-model haiku --model sonnet <path> |
| 13014 | c1 | subs pair elem 1 (NEW) | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| 13020 | c1 | subs pair elem 1 (NEW) | uv run python -m scripts.run --gen-model haiku --model sonnet <path> |
| 13037 | c1 | subs pair elem 1 (NEW) | description: Suggests manual context compaction at logical intervals to preserve context through task phases rather than |
| 13050 | a | subs pair elem 0 (OLD) | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings.json` — `~/.claude/s |
| 13052 | a | subs pair elem 0 (OLD) | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 13060 | a | subs pair elem 0 (OLD) | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| 13064 | a | subs pair elem 0 (OLD) | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| 13082 | c1 | subs pair elem 1 (NEW) | **Installed as a plugin?** No setup is needed. Do not copy the block below into your `hooks/hooks.json` — `~/.claude/scr |
| 13371 | b | bash comment | # replaces it with the Claude Code Task (Explore agent) fallback, since the |
| 13372 | b | bash comment | # multi-* commands are Claude Code-only. |
| 13413 | b | python comment | # --- Fix 5: multi-* commands — Claude Code-only labels + misleading Cursor fallback --- |
| 13416 | c1 | subs pair elem 1 (NEW) | "description: Run a backend-focused multi-model workflow for APIs, algorithms, data, and business logic. (Requires exter |
| 13419 | a | subs pair elem 0 (OLD) | ("description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Require |
| 13420 | c1 | subs pair elem 1 (NEW) | "description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Requires |
| 13426 | c1 | subs pair elem 1 (NEW) | "description: Run a frontend-focused multi-model workflow for components, layouts, animation, and UI polish. (Requires e |
| 13430 | c1 | subs pair elem 1 (NEW) | "for a single-model plan with no extra runtime use /plan. (Claude Code only — no Cursor equivalent in this plugin)"), |
| 13436 | c1 | subs pair elem 1 (NEW) | "description: Run a full multi-model development workflow with research, planning, execution, optimization, and review.  |
| 13439 | b | python comment | # --- Fix 6: gan-harness.sh — Claude Code-only header (script shells out to claude -p / claude mcp) --- |
| 13444 | c1 | subs pair elem 1 (NEW) | # Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install wi |
| 13448 | b | python comment | # --- Fix 7: strategic-compact — adjudicated NOT Claude Code-only --- |
| 13451 | b | python comment | # this skill is Claude Code-only was wrong. Label rewritten to say so. |
| 13453 | a | subs pair elem 0 (OLD) | ("(Claude Code-origin — the manual-compaction advice applies in Cursor; the hook example below is Cursor `hooks.json` fo |
| 13454 | c1 | subs pair elem 1 (NEW) | "(Compaction advice that applies in Cursor; originated in Claude Code; the hook example below is in Cursor `hooks.json`  |
| 13457 | b | python comment | # --- Fix 8: continuous-learning v1 — weak label; make the Claude Code-only status explicit --- |
| 13460 | c1 | subs pair elem 1 (NEW) | 'description: "[DEPRECATED - Claude Code only, use continuous-learning-v2] Legacy v1 stop-hook skill extractor.'), |
| 13475 | b | python comment | # in the previewClaude/applyClaude factories, so each factory is replaced |
| 13479 | a | subs pair elem 0 (OLD) | ("""    previewClaude: request => require('../setup').reconcileClaudePlugin( |
| 13480 | a | subs pair elem 0 (OLD) | { dryRun: true, hooks: request.claudeHooks, scope: request.claudeScope } |
| 13482 | c1 | subs pair elem 1 (NEW) | "    previewClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in this plugin (Claude p |
| 13483 | a | subs pair elem 0 (OLD) | ("""    applyClaude: request => require('../setup').reconcileClaudePlugin( |
| 13484 | a | subs pair elem 0 (OLD) | { dryRun: false, hooks: request.claudeHooks, scope: request.claudeScope } |
| 13486 | c1 | subs pair elem 1 (NEW) | "    applyClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in this plugin (Claude plu |
| 13533 | a | subs pair elem 0 (OLD) | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/evolved/` |
| 13534 | a | subs pair elem 0 (OLD) | - Global fallback: `~/.claude/homunculus/evolved/`""", |
| 13537 | c1 | subs pair elem 1 (NEW) | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/mig |
| 13541 | a | subs pair elem 0 (OLD) | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/instincts/inherited/` |
| 13542 | a | subs pair elem 0 (OLD) | - Global scope: `~/.claude/homunculus/instincts/inherited/`""", |
| 13545 | c1 | subs pair elem 1 (NEW) | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/mig |
| 13546 | a | subs pair elem 0 (OLD) | ("""New instincts saved to: ~/.claude/homunculus/instincts/inherited/""", |
| 13551 | a | subs pair elem 0 (OLD) | ("""2. Read project instincts from `~/.claude/homunculus/projects/<project-id>/instincts/` |
| 13552 | a | subs pair elem 0 (OLD) | 3. Read global instincts from `~/.claude/homunculus/instincts/`""", |
| 13556 | c1 | subs pair elem 1 (NEW) | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migra |
| 13560 | a | subs pair elem 0 (OLD) | ("""1. Read `~/.claude/homunculus/projects.json`""", |
| 13563 | c1 | subs pair elem 1 (NEW) | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migra |
| 13567 | a | subs pair elem 0 (OLD) | ("""4. Write promoted instincts to `~/.claude/homunculus/instincts/personal/` with `scope: global`""", |
| 13570 | c1 | subs pair elem 1 (NEW) | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migra |
| 13574 | a | subs pair elem 0 (OLD) | ("""description: Manage Claude Code session history, aliases, and session metadata.""", |
| 13575 | c1 | subs pair elem 1 (NEW) | """description: Manage Claude Code session history, aliases, and session metadata. (Claude Code only — no Cursor equival |
| 13580 | a | subs pair elem 0 (OLD) | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| 13583 | c1 | subs pair elem 1 (NEW) | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| 13684 | a | subs pair elem 0 (OLD) | ("""uv run python -m scripts.run ~/.claude/rules/common/testing.md""", |
| 13728 | b | bash comment | # only CLAUDE_PLUGIN_ROOT / ~/.claude — no Cursor fallback. Fix: the shared |
| 13811 | a | subs pair elem 0 (OLD) | (""" *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/ |
| 13812 | a | subs pair elem 0 (OLD) | *   5. Fallback to ~/.claude/ (original behaviour)""", |
| 13813 | c1 | subs pair elem 1 (NEW) | """ *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/ |
| 13817 | c1 | subs pair elem 1 (NEW) | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 13818 | c1 | subs pair elem 1 (NEW) | *   6. Fallback to ~/.claude/ (original behaviour)"""), |
| 13820 | a | subs pair elem 0 (OLD) | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| 13832 | a | subs pair elem 0 (OLD) | return claudeDir; |
| 13835 | c1 | subs pair elem 1 (NEW) | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| 13850 | c1 | subs pair elem 1 (NEW) | // is no ~/.claude and no CLAUDE_PLUGIN_ROOT, so all the probing above |
| 13859 | c1 | subs pair elem 1 (NEW) | return claudeDir; |
| 13861 | a | subs pair elem 0 (OLD) | (""" * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| 13863 | a | subs pair elem 0 (OLD) | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| 13864 | a | subs pair elem 0 (OLD) | * under ~/.claude/plugins/, and the versioned plugin cache — only far enough to |
| 13868 | c1 | subs pair elem 1 (NEW) | """ * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| 13870 | c1 | subs pair elem 1 (NEW) | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| 13871 | c1 | subs pair elem 1 (NEW) | * under ~/.claude/plugins/, and the versioned plugin cache — then, as an |
| 13874 | c1 | subs pair elem 1 (NEW) | * so it also finds the plugin in a Cursor install with no ~/.claude. Only |
| 13875 | c1 | subs pair elem 1 (NEW) | * then does it fall back to ~/.claude. The Cursor scan tests candidates |
| 13877 | c1 | subs pair elem 1 (NEW) | * ~/.claude-first for any directory the module loads from."""), |
| 13907 | c1 | subs pair elem 1 (NEW) | // resolver's ~/.claude-first answer for any directory the module loads |
| 13963 | a | assign old = (OLD-side text) | old = 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" ' + args |
| 13971 | a | assign old = (OLD-side text) | old = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| 13972 | a | assign old = (OLD-side text) | "./.claude/scripts/astra-review.js" \\''' |
| 13974 | c1 | assign new = (NEW-side text) | new = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| 13976 | c1 | assign new = (NEW-side text) | "./.claude/scripts/astra-review.js" \\''' |
| 14207 | c1 | subs pair elem 1 (NEW) | // rules/common/, .claude-plugin/plugin.json, |
| 14222 | c1 | subs pair elem 1 (NEW) | r'''or picking up a project without re-explaining it. (Claude Code only — this skill uses Claude Code's SessionStart hoo |
| 14228 | c1 | subs pair elem 1 (NEW) | > **Claude Code only** — this skill uses Claude Code's SessionStart hook and ~/.claude/ck storage; it does not work in C |
| 14239 | c1 | subs pair elem 1 (NEW) | * Claude Code only: the `claude` CLI does not exist under Cursor, so |
| 14253 | a | subs pair elem 0 (OLD) | return process.env.ECC_LLM_SUMMARY_MODEL \|\| 'haiku'; |
| 14258 | c1 | subs pair elem 1 (NEW) | return process.env.ECC_LLM_SUMMARY_MODEL \|\| 'haiku'; |
| 14262 | c1 | subs pair elem 1 (NEW) | * True only when a `claude` executable is findable on PATH. Pure filesystem |
| 14263 | c1 | subs pair elem 1 (NEW) | * check (no subprocess): under Cursor there is no `claude` binary, so the |
| 14266 | c1 | subs pair elem 1 (NEW) | function claudeCliAvailable() { |
| 14267 | c1 | subs pair elem 1 (NEW) | const names = process.platform === 'win32' ? ['claude.cmd', 'claude.exe', 'claude'] : ['claude']; |
| 14285 | c1 | subs pair elem 1 (NEW) | // Claude Code only: skip the doomed `claude -p` spawn when the binary is |
| 14287 | c1 | subs pair elem 1 (NEW) | if (!claudeCliAvailable()) { |
| 14288 | c1 | subs pair elem 1 (NEW) | onSkip('claude CLI not available (not running under Claude Code)'); |
| 14295 | c1 | subs pair elem 1 (NEW) | r"""module.exports = { generateSessionSummary, extractConversationText, getContextRemainingPct, getContextThreshold, get |
| 14668 | a | subs pair elem 0 (OLD) | (r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `scripts/migrate-homunculus |
| 14669 | c1 | subs pair elem 1 (NEW) | r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `skills/continuous-learning- |
| 14696 | a | subs pair elem 0 (OLD) | ('"""\nStop hook: quality gate with delivery check.\nDetects incomplete work, stale learning logs, and low disk space.\n |
| 15141 | a | subs pair elem 0 (OLD) | (r'''        content += "model: sonnet\ntools: Read, Grep, Glob\n---\n"''', |
| 15142 | c1 | subs pair elem 1 (NEW) | r'''        content += "model: sonnet\n---\n"'''), |
| 15256 | b | bash comment | #  - D7 (claude-project-scripts-package.json) -- NO CHANGE: the audit premise |
| 15258 | b | bash comment | #    claude-project.js and must stay. |
| 15359 | b | python comment | # --- D2: multi-* commands — Claude Code tool names -> Cursor wording --- |
| 15373 | a | subs pair elem 0 (OLD) | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 15385 | a | subs pair elem 0 (OLD) | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 15399 | a | subs pair elem 0 (OLD) | (r'''        content += "model: sonnet\n---\n"''', |
| 15408 | a | subs pair elem 0 (OLD) | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 15409 | a | subs pair elem 0 (OLD) | *   6. Fallback to ~/.claude/ (original behaviour)""", |
| 15418 | c1 | subs pair elem 1 (NEW) | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 15419 | c1 | subs pair elem 1 (NEW) | *   7. Fallback to ~/.claude/ (original behaviour)"""), |
| 15456 | b | python comment | # --- D10: gan agents — '(Claude Code only — no Cursor equivalent)' in descriptions --- |
| 15459 | c1 | subs pair elem 1 (NEW) | r'''description: "GAN Harness — Evaluator agent. Tests the live running application via Playwright, scores against rubri |
| 15463 | c1 | subs pair elem 1 (NEW) | r'''description: "GAN Harness — Generator agent. Implements features according to the spec, reads evaluator feedback, an |
| 15467 | c1 | subs pair elem 1 (NEW) | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features |
| 15627 | a | subs pair elem 0 (OLD) | (r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (claude -> pi)',''', |
| 15628 | c1 | subs pair elem 1 (NEW) | r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (not shipped in this plugin) (claude ->  |
| 15839 | a | subs pair elem 0 (OLD) | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the e |
| 15843 | a | subs pair elem 0 (OLD) | (r'''Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre- |
| 15844 | c1 | subs pair elem 1 (NEW) | r'''Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre-w |
| 15845 | a | subs pair elem 0 (OLD) | (r'''This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` event in `hooks/hooks.j |
| 15846 | c1 | subs pair elem 1 (NEW) | r'''This was a Claude Code stop-hook block; it is NOT wired in this plugin. The `stop` event in `hooks/hooks.json` runs  |
| 15994 | a | subs pair elem 0 (OLD) | "audit claude config", |
| 15995 | a | subs pair elem 0 (OLD) | "claudemd security", |
| 16256 | a | subs pair elem 0 (OLD) | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| 16269 | c1 | subs pair elem 1 (NEW) | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| 16280 | b | python comment | # --- Fixer B (Cleanliness): frontmatter model sonnet is not a Cursor model; cursor-grok-4.6-high-fast. |
| 16288 | a | subs pair elem 0 (OLD) | model: sonnet |
| 16348 | b | python comment | # --- Fixer B (Cleanliness): Claude-Code-only env var / config paths; add the Cursor equivalents (CURSOR_PACKAGE_MANAGER |
| 16356 | a | subs pair elem 0 (OLD) | 1. **Environment variable**: `CLAUDE_PACKAGE_MANAGER` |
| 16357 | a | subs pair elem 0 (OLD) | 2. **Project config**: `.claude/package-manager.json` |
| 16360 | a | subs pair elem 0 (OLD) | 5. **Global config**: `~/.claude/package-manager.json` |
| 16367 | a | subs pair elem 0 (OLD) | // ~/.claude/package-manager.json |
| 16380 | c1 | subs pair elem 1 (NEW) | 1. **Environment variable**: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude Code) |
| 16381 | c1 | subs pair elem 1 (NEW) | 2. **Project config**: `.cursor/package-manager.json`, then `.claude/package-manager.json` |
| 16384 | c1 | subs pair elem 1 (NEW) | 5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.json` in Cursor, `~/.claude/package-manager |
| 16393 | c1 | subs pair elem 1 (NEW) | // Claude Code: ~/.claude/package-manager.json |
| 16406 | a | subs pair elem 0 (OLD) | // .claude/package-manager.json |
| 16420 | c1 | subs pair elem 1 (NEW) | // (an existing .claude/package-manager.json is still honoured on read) |
| 16433 | a | subs pair elem 0 (OLD) | Set `CLAUDE_PACKAGE_MANAGER` to override all other detection methods: |
| 16437 | a | subs pair elem 0 (OLD) | $env:CLAUDE_PACKAGE_MANAGER = "pnpm" |
| 16440 | a | subs pair elem 0 (OLD) | export CLAUDE_PACKAGE_MANAGER=pnpm |
| 16453 | c1 | subs pair elem 1 (NEW) | Set `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude |
| 16471 | b | python comment | # --- Fixer B (Cleanliness): skill install paths named .claude/skills/ only; add the Cursor paths (.cursor/skills/, ~/.c |
| 16479 | a | subs pair elem 0 (OLD) | `.claude/skills/`; a global skill uses `~/.claude/skills/`. |
| 16492 | c1 | subs pair elem 1 (NEW) | `.cursor/skills/` in Cursor (this plugin's host) or `.claude/skills/` in |
| 16493 | c1 | subs pair elem 1 (NEW) | Claude Code; a global skill uses `~/.cursor/skills/` or `~/.claude/skills/`. |
| 16933 | c1 | subs pair elem 1 (NEW) | "claude", |
| 16934 | c1 | subs pair elem 1 (NEW) | "claude-project", |
| 16937 | c1 | subs pair elem 1 (NEW) | "codex", |
| 17055 | b | python comment | # --- Fixer B (Cleanliness): Claude-Code-only package-manager detection; make it host-aware (CURSOR_PACKAGE_MANAGER firs |
| 17063 | a | subs pair elem 0 (OLD) | const { commandExists, getClaudeDir, readFile, writeFile } = require('./utils'); |
| 17076 | c1 | subs pair elem 1 (NEW) | const { commandExists, getClaudeDir, getHomeDir, readFile, writeFile } = require('./utils'); |
| 17091 | a | subs pair elem 0 (OLD) | return path.join(getClaudeDir(), 'package-manager.json'); |
| 17115 | c1 | subs pair elem 1 (NEW) | // ~/.claude in Claude Code — see scripts/lib/agent-data-home.js) |
| 17117 | c1 | subs pair elem 1 (NEW) | return path.join(getClaudeDir(), 'package-manager.json'); |
| 17127 | c1 | subs pair elem 1 (NEW) | function getClaudeGlobalConfigPath() { |
| 17128 | c1 | subs pair elem 1 (NEW) | return path.join(getHomeDir(), '.claude', 'package-manager.json'); |
| 17134 | c1 | subs pair elem 1 (NEW) | * (~/.cursor/package-manager.json) and Claude Code |
| 17135 | c1 | subs pair elem 1 (NEW) | * (~/.claude/package-manager.json) global paths. |
| 17141 | c1 | subs pair elem 1 (NEW) | getClaudeGlobalConfigPath() |
| 17159 | a | subs pair elem 0 (OLD) | * 1. Environment variable CLAUDE_PACKAGE_MANAGER |
| 17160 | a | subs pair elem 0 (OLD) | * 2. Project-specific config (in .claude/package-manager.json) |
| 17163 | a | subs pair elem 0 (OLD) | * 5. Global user preference (in ~/.claude/package-manager.json) |
| 17177 | c1 | subs pair elem 1 (NEW) | *    CLAUDE_PACKAGE_MANAGER (Claude Code) |
| 17179 | c1 | subs pair elem 1 (NEW) | *    .claude/package-manager.json) |
| 17183 | c1 | subs pair elem 1 (NEW) | *    ~/.cursor/package-manager.json, then ~/.claude/package-manager.json) |
| 17197 | a | subs pair elem 0 (OLD) | const envPm = process.env.CLAUDE_PACKAGE_MANAGER; |
| 17210 | c1 | subs pair elem 1 (NEW) | // 1. Check environment variable (Cursor first, then Claude Code) |
| 17211 | c1 | subs pair elem 1 (NEW) | const envPm = process.env.CURSOR_PACKAGE_MANAGER \|\| process.env.CLAUDE_PACKAGE_MANAGER; |
| 17225 | a | subs pair elem 0 (OLD) | const projectConfigPath = path.join(projectDir, '.claude', 'package-manager.json'); |
| 17251 | c1 | subs pair elem 1 (NEW) | // 2. Check project-specific config (.cursor first, then .claude) |
| 17252 | c1 | subs pair elem 1 (NEW) | for (const configDir of ['.cursor', '.claude']) { |
| 17295 | c1 | subs pair elem 1 (NEW) | * ~/.claude/package-manager.json in Claude Code. A preference saved at |
| 17296 | c1 | subs pair elem 1 (NEW) | * ~/.cursor/package-manager.json or ~/.claude/package-manager.json is still |
| 17317 | a | subs pair elem 0 (OLD) | const configDir = path.join(projectDir, '.claude'); |
| 17332 | c1 | subs pair elem 1 (NEW) | * existing .claude/package-manager.json is still honoured on read as a |
| 17333 | c1 | subs pair elem 1 (NEW) | * fallback for Claude Code installs (see getPackageManager step 2). |
| 17353 | a | subs pair elem 0 (OLD) | message += '  - Global: Set CLAUDE_PACKAGE_MANAGER environment variable\n'; |
| 17354 | a | subs pair elem 0 (OLD) | message += '  - Or add to ~/.claude/package-manager.json: {"packageManager": "pnpm"}\n'; |
| 17367 | c1 | subs pair elem 1 (NEW) | message += '  - Global: Set CURSOR_PACKAGE_MANAGER (Cursor) or CLAUDE_PACKAGE_MANAGER (Claude Code) environment variable |
| 17368 | c1 | subs pair elem 1 (NEW) | message += '  - Or add to ~/.cursor/package-manager.json or ~/.claude/package-manager.json: {"packageManager": "pnpm"}\n |
| 17402 | b | python comment | # --- Fixer B (Cleanliness): setup script named Claude Code only; host-aware wording and getConfigPath() reporting. |
| 17435 | a | subs pair elem 0 (OLD) | Package Manager Setup for Claude Code |
| 17442 | a | subs pair elem 0 (OLD) | --global <pm>   Set global preference (saves to ~/.claude/package-manager.json) |
| 17443 | a | subs pair elem 0 (OLD) | --project <pm>  Set project preference (saves to .claude/package-manager.json) |
| 17456 | c1 | subs pair elem 1 (NEW) | Package Manager Setup for Cursor (also works in Claude Code) |
| 17465 | c1 | subs pair elem 1 (NEW) | ~/.claude/package-manager.json in Claude Code; |
| 17468 | c1 | subs pair elem 1 (NEW) | an existing .claude/package-manager.json is still honoured) |
| 17481 | a | subs pair elem 0 (OLD) | console.log(`  Environment var: ${process.env.CLAUDE_PACKAGE_MANAGER \|\| 'not set'}`); |
| 17494 | c1 | subs pair elem 1 (NEW) | console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER \|\| process.env.CLAUDE_PACKAGE_MANAGER \|\| 'not set'} |
| 17507 | a | subs pair elem 0 (OLD) | console.log('  Saved to: ~/.claude/package-manager.json'); |
| 17521 | c1 | subs pair elem 1 (NEW) | console.log('  (Also read from ~/.cursor/package-manager.json and ~/.claude/package-manager.json)'); |
| 17534 | a | subs pair elem 0 (OLD) | console.log('  Saved to: .claude/package-manager.json'); |
| 17548 | c1 | subs pair elem 1 (NEW) | console.log('  (An existing .claude/package-manager.json is still honoured on read)'); |
| 17557 | b | python comment | # --- Fixer B (Cleanliness): LaraPlugins MCP setup named ~/.claude.json only; Cursor-first with the Claude Code alternat |
| 17565 | a | subs pair elem 0 (OLD) | LaraPlugins MCP server must be configured. Add to your `~/.claude.json` mcpServers: |
| 17606 | c1 | subs pair elem 1 (NEW) | In Claude Code, add the same entry to your `~/.claude.json` `mcpServers` |
| 17616 | b | python comment | # --- Fixer B (Cleanliness): scan commands named Claude Code paths only; add the Cursor paths. |
| 17625 | a | subs pair elem 0 (OLD) | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| 17631 | a | subs pair elem 0 (OLD) | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| 17651 | c1 | subs pair elem 1 (NEW) | Claude Code (this skill also works there): |
| 17654 | c1 | subs pair elem 1 (NEW) | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| 17665 | c1 | subs pair elem 1 (NEW) | Claude Code: |
| 17668 | c1 | subs pair elem 1 (NEW) | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| 17674 | b | python comment | # --- Fixer B (Cleanliness): 'Claude Code Subagents' heading in a Cursor plugin; Cursor Subagents. |
| 17682 | a | subs pair elem 0 (OLD) | ### Pattern A: Claude Code Subagents (Recommended) |
| 17704 | b | python comment | # --- Fixer B (Cleanliness): skill search paths named ~/.claude only; check ~/.cursor/skills and the plugin marketplaces |
| 17712 | a | subs pair elem 0 (OLD) | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17713 | a | subs pair elem 0 (OLD) | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17730 | c1 | subs pair elem 1 (NEW) | # Claude Code (this skill also works there) — same searches under ~/.claude |
| 17731 | c1 | subs pair elem 1 (NEW) | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17732 | c1 | subs pair elem 1 (NEW) | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17737 | a | subs pair elem 0 (OLD) | (r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17743 | a | subs pair elem 0 (OLD) | grep -RilE "keyword\|synonym" ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null |
| 17750 | c1 | subs pair elem 1 (NEW) | r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17756 | c1 | subs pair elem 1 (NEW) | grep -RilE "keyword\|synonym" ~/.cursor/skills ~/.cursor/plugins/marketplaces ~/.claude/skills ~/.claude/plugins/marketpl |
| 17825 | c1 | subs pair elem 1 (NEW) | r'''\| Observation \| Stop hook (session end) \| PreToolUse/PostToolUse (Claude Code only) \|'''), |
| 17827 | c1 | subs pair elem 1 (NEW) | r'''      \| Claude Code hooks capture prompts + tool use (Claude Code only)'''), |
| 17834 | a | subs pair elem 0 (OLD) | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` |
| 17839 | c1 | subs pair elem 1 (NEW) | **In Claude Code, if installed as a plugin** (recommended): |
| 17843 | c1 | subs pair elem 1 (NEW) | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` |
| 17844 | a | subs pair elem 0 (OLD) | (r'''**If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:''', |
| 17845 | c1 | subs pair elem 1 (NEW) | r'''**If installed manually in Claude Code** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:'''), |
| 17850 | c1 | subs pair elem 1 (NEW) | r'''In Claude Code, hooks fire on every tool call, deterministically. This means: |
| 17861 | c1 | subs pair elem 1 (NEW) | r'''continuous-learning-v2 is a separate, configurable Stop/PreToolUse/PostToolUse hook-observation and instinct-evoluti |
| 17876 | c1 | subs pair elem 1 (NEW) | r'''This skill complements manual review (and, in Claude Code, PostToolUse hooks) but provides deeper verification. |
| 17882 | a | subs pair elem 0 (OLD) | (r'''The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same behaviour as an `aft |
| 17883 | c1 | subs pair elem 1 (NEW) | r'''The bullets below describe the intended Dart hook behaviour (originally a Claude Code `settings.json` block). In Cur |
| 17912 | a | subs pair elem 0 (OLD) | (r'''See [CLAUDE.md](CLAUDE.md) for detailed commands and architecture.''', |
| 17913 | c1 | subs pair elem 1 (NEW) | r'''See `CLAUDE.md` (generated in the target repo) for detailed commands and architecture.'''), |
| 17976 | b | python comment | # is true in Claude Code (ECC runs post-edit-format.js as a PostToolUse hook |
| 17977 | b | python comment | # there) and the skill is labelled Claude Code-only in its description, but |
| 17979 | b | python comment | # Claude Code-only and name the Cursor equivalent (Audit #11 fixed the |
| 17984 | c1 | subs pair elem 1 (NEW) | r'''\| Code quality enforcement \| PostToolUse hooks (Prettier, tsc) — Claude Code only; in Cursor, post-edit formatting v |
| 18088 | b | python comment | # --- LOW Cleanliness 1: tdd-workflow — :104 stated a Claude-only |
| 18094 | a | subs pair elem 0 (OLD) | (r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/packag |
| 18095 | c1 | subs pair elem 1 (NEW) | r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAU |
| 18098 | b | python comment | # --- LOW Cleanliness 2: nuxt-hooks.mdc — :13 framed the hooks as Claude |
| 18105 | a | subs pair elem 0 (OLD) | (r'''These are Claude Code harness hooks for Nuxt work. They run via the harness, not Claude.''', |
| 18106 | c1 | subs pair elem 1 (NEW) | r'''These were Claude Code harness hooks for Nuxt work; in Cursor, wire them as `afterFileEdit` entries in `hooks/hooks. |
| 18232 | a | subs pair elem 0 (OLD) | ".claude/skills/ui-ux-pro-max/references/quick-reference.md"): |
| 18475 | b | python comment | # names were the upstream Claude Code command set. Reword to stages. |
| 18491 | a | subs pair elem 0 (OLD) | (r'''\| `/opensource package PROJECT` \| Generate CLAUDE.md + setup.sh + README \|''', |
| 18492 | c1 | subs pair elem 1 (NEW) | r'''\| `package PROJECT` \| Generate CLAUDE.md + setup.sh + README \|'''), |
| 18510 | b | python comment | # commands (Claude Code only, not shipped in this plugin). Qualify once up |
| 18517 | c1 | subs pair elem 1 (NEW) | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow runtime's commands (Cla |
| 18526 | a | subs pair elem 0 (OLD) | (r'''/ccg:execute .claude/plan/actual-feature-name.md''', |
| 18527 | c1 | subs pair elem 1 (NEW) | r'''/multi-execute .claude/plan/actual-feature-name.md'''), |
| 18532 | a | subs pair elem 0 (OLD) | (r'''/ccg:execute .claude/plan/<feature-name>.md''', |
| 18533 | c1 | subs pair elem 1 (NEW) | r'''/multi-execute .claude/plan/<feature-name>.md'''), |
| 18544 | c1 | subs pair elem 1 (NEW) | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow runtime's commands (Cla |
| 18551 | a | subs pair elem 0 (OLD) | (r'''/ccg:execute .claude/plan/feature-name.md''', |
| 18552 | c1 | subs pair elem 1 (NEW) | r'''/multi-execute .claude/plan/feature-name.md'''), |
| 18578 | c1 | subs pair elem 1 (NEW) | r''' * Claude Code-only PostToolUse hook: TypeScript check after editing .ts/.tsx files (not wired in this Cursor plugin |
| 18580 | c1 | subs pair elem 1 (NEW) | r''' * Runs after Edit tool use on TypeScript files in Claude Code. Walks up from the file's'''), |
| 18590 | c1 | subs pair elem 1 (NEW) | r''' * ECC Context Monitor — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostTool |
| 18594 | c1 | subs pair elem 1 (NEW) | r''' * ECC Metrics Bridge — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolU |
| 18598 | c1 | subs pair elem 1 (NEW) | r''' * Claude Code-only PreToolUse/PostToolUse hook (not wired in this Cursor plugin) that detects governance-relevant e |
| 18602 | c1 | subs pair elem 1 (NEW) | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin) that records sanitized per-tool activity to'' |
| 18606 | c1 | subs pair elem 1 (NEW) | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin): record Skill tool invocations for skill-heal |
| 18611 | c1 | subs pair elem 1 (NEW) | r''' * Claude Code-only: consolidates PostToolUse hooks into one synchronous and one asynchronous |
| 18633 | b | bash comment | # adapter is live Cursor hook infrastructure, not a Claude Code-only / |
| 18687 | b | python comment | # it Claude Code-only / not-wired: every hooks/*.js script does |
| 18692 | a | subs pair elem 0 (OLD) | * Cursor-to-Claude Code Hook Adapter |
| 18693 | a | subs pair elem 0 (OLD) | * Transforms Cursor stdin JSON to Claude Code hook format, |
| 18702 | c1 | subs pair elem 1 (NEW) | * is live infrastructure — not a Claude Code-only or unwired script. |
| 19027 | b | bash comment | # standard "(Claude Code only — no Cursor equivalent in this plugin)" label |
| 19029 | b | bash comment | # .claude/plans/ and references ECC_HOOK_PROFILE; the hookify commands and |
| 19030 | b | bash comment | # skill name Claude Code explicitly in their bodies. |
| 19064 | c1 | subs pair elem 1 (NEW) | r'''with safety gates before starting one. (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19070 | c1 | subs pair elem 1 (NEW) | r'''for authoring or editing rules directly. (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19074 | c1 | subs pair elem 1 (NEW) | r'''description: Enable or disable hookify rules interactively (Claude Code only — no Cursor equivalent in this plugin)' |
| 19078 | c1 | subs pair elem 1 (NEW) | r'''description: List all configured hookify rules (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19082 | c1 | subs pair elem 1 (NEW) | r'''description: Get help with the hookify system (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19086 | c1 | subs pair elem 1 (NEW) | r'''such as blocking dangerous commands, .env edits, or debug code. (Claude Code only — no Cursor equivalent in this plu |
| 19125 | b | bash comment | # Claude Code-only label, mirroring the 7 labelled unwired PostToolUse |
| 19126 | b | bash comment | # scripts. Reads stdin from the Claude Code runtime, registered in |
| 19129 | b | bash comment | # Claude Code-only label, mirroring the labelled hookify set. Evaluates |
| 19130 | b | bash comment | # rules against Claude Code lifecycle payloads; reachable only from the |
| 19193 | c1 | subs pair elem 1 (NEW) | r''' * ECC Statusline — Claude Code-only statusLine command (not wired in this Cursor plugin — registered in settings.js |
| 19199 | c1 | subs pair elem 1 (NEW) | r''' * ECC-native Hookify runtime — Claude Code-only (not wired in this Cursor plugin — reachable only via the unwired p |
| 19230 | b | bash comment | # Claude Code-only, never run in Cursor, and carried no "Claude Code-only / |
| 19264 | c1 | subs pair elem 1 (NEW) | r''' * MCP health-check hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse/PostToolUseF |
| 19268 | c1 | subs pair elem 1 (NEW) | r''' * Doc file warning hook (PreToolUse - Write) — Claude Code-only (not wired in this Cursor plugin — Cursor has no Pr |
| 19272 | c1 | subs pair elem 1 (NEW) | r''' * Config Protection Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event)'''), |
| 19276 | c1 | subs pair elem 1 (NEW) | r''' * Desktop Notification Hook (Stop) — Claude Code-only (not wired in this Cursor plugin — Cursor has no Stop hook ev |
| 19280 | c1 | subs pair elem 1 (NEW) | r''' * PreToolUse Hook: Pre-commit Quality Check — Claude Code-only (not wired in this Cursor plugin — Cursor has no Pre |
| 19284 | c1 | subs pair elem 1 (NEW) | r''' * Backward-compatible doc warning hook entrypoint — Claude Code-only (not wired in this Cursor plugin — Cursor has  |
| 19288 | c1 | subs pair elem 1 (NEW) | r''' * Auto-Tmux Dev Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event) — start  |
| 19292 | c1 | subs pair elem 1 (NEW) | r''' * UserPromptSubmit hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no UserPromptSubmit event) |
| 19296 | c1 | subs pair elem 1 (NEW) | r''' * Plan Canvas undelivered-feedback guard (Stop) — Claude Code-only (not wired in this Cursor plugin — Cursor has no |
| 19300 | c1 | subs pair elem 1 (NEW) | r''' * Plan Canvas open-session surfacing (SessionStart) — Claude Code-only (not wired in this Cursor plugin — Cursor ha |
| 19304 | c1 | subs pair elem 1 (NEW) | r''' * PreToolUse Hook: GateGuard Fact-Forcing Gate — Claude Code-only (not wired in this Cursor plugin — Cursor has no  |
| 19308 | c1 | subs pair elem 1 (NEW) | r''' * InsAIts Security Monitor — Claude Code-only wrapper for run-with-flags compatibility (not wired in this Cursor pl |
| 19312 | c1 | subs pair elem 1 (NEW) | r''' * Bootstrap loader for the ECC SessionStart hook — Claude Code-only (not wired in this Cursor plugin — Cursor has n |
| 19321 | c1 | subs pair elem 1 (NEW) | * Git push reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has no PreToolUse event |
| 19330 | c1 | subs pair elem 1 (NEW) | * Tmux reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has no PreToolUse event). |
| 19339 | c1 | subs pair elem 1 (NEW) | * Build-complete notifier — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolU |
| 19348 | c1 | subs pair elem 1 (NEW) | * Command logger — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event) |
| 19357 | c1 | subs pair elem 1 (NEW) | * PR-created handler — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse ev |
| 19366 | c1 | subs pair elem 1 (NEW) | * Hook-enabled check — Claude Code-only helper (not wired in this Cursor plugin — invoked only from Claude Code hook con |
| 19375 | c1 | subs pair elem 1 (NEW) | * Lifecycle hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no lifecycle hook events). |
| 19384 | c1 | subs pair elem 1 (NEW) | * Plugin hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no hook events that invoke it). |
| 19636 | b | bash comment | # Claude Code PreToolUse/PostToolUse bash-dispatch entry points; Cursor's |
| 19670 | c1 | subs pair elem 1 (NEW) | * Claude Code-only: PreToolUse bash-dispatch entry point (runPreBash). |
| 19680 | c1 | subs pair elem 1 (NEW) | * Claude Code-only: PostToolUse bash-dispatch entry point (runPostBash). |
| 19689 | c1 | subs pair elem 1 (NEW) | # Claude Code-only: shell counterpart of run-with-flags.js (not wired in this Cursor plugin — it never runs; resolves th |
| 22050 | a | subs tuple elem 1 (OLD) | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 22054 | c1 | subs tuple elem 2 (NEW) | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 22387 | a | subs tuple elem 1 (OLD) | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22388 | c1 | subs tuple elem 2 (NEW) | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and i |
| 22391 | a | subs tuple elem 1 (OLD) | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22392 | c1 | subs tuple elem 2 (NEW) | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and i |
| 22395 | a | subs tuple elem 1 (OLD) | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22396 | c1 | subs tuple elem 2 (NEW) | r'''(Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed |
| 22403 | a | subs tuple elem 1 (OLD) | r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality  |
| 22404 | c1 | subs tuple elem 2 (NEW) | r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality  |
| 22405 | b | python comment | # B7b gan-style-harness "Via Claude Code (Manual)" section: those commands |
| 22408 | a | subs tuple elem 1 (OLD) | r'''### Via Claude Code (Manual) |
| 22412 | c1 | subs tuple elem 2 (NEW) | r'''### Via Claude Code (Manual) |
| 22414 | c1 | subs tuple elem 2 (NEW) | > In this plugin these `claude -p` commands are NOT executed — the loop runs in Cursor via `/gan-build` (planner/generat |
| 22565 | b | python comment | # 11a gan-style-harness :30: scope the claude -p reference. |
| 22567 | a | subs tuple elem 1 (OLD) | r'''- Quick single-file fixes (use standard `claude -p`)''', |
| 22568 | c1 | subs tuple elem 2 (NEW) | r'''- Quick single-file fixes (Claude Code only — use standard `claude -p` there; in this plugin use the Cursor agent lo |
| 22571 | a | subs tuple elem 1 (OLD) | r'''### Via Claude Code (Manual)''', |
| 22572 | c1 | subs tuple elem 2 (NEW) | r'''### Via Claude Code (Manual — Claude Code only, never executed in this plugin)'''), |
| 22573 | b | python comment | # 11c gan-style-harness commands: scope each claude -p command in place. |
| 22577 | a | subs tuple elem 1 (OLD) | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: |
| 22580 | a | subs tuple elem 1 (OLD) | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000." |
| 22583 | a | subs tuple elem 1 (OLD) | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md.  |
| 22586 | a | subs tuple elem 1 (OLD) | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores. |
| 22592 | c1 | subs tuple elem 2 (NEW) | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22593 | c1 | subs tuple elem 2 (NEW) | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: |
| 22596 | c1 | subs tuple elem 2 (NEW) | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22597 | c1 | subs tuple elem 2 (NEW) | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000." |
| 22600 | c1 | subs tuple elem 2 (NEW) | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22601 | c1 | subs tuple elem 2 (NEW) | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md.  |
| 22604 | c1 | subs tuple elem 2 (NEW) | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22605 | c1 | subs tuple elem 2 (NEW) | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores. |
| 22611 | a | subs tuple elem 1 (OLD) | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only instal |
| 22612 | c1 | subs tuple elem 2 (NEW) | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only instal |
| 22644 | a | subs tuple elem 1 (OLD) | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features |
| 22645 | c1 | subs tuple elem 2 (NEW) | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features |
| 23204 | b | bash comment | # --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic --- |

## Observations (not findings — no action required by this sweep's bar)

- **GPT-4 prose mentions (2, not pins):** `hackathon-ecc/skills/hackathon-scope/SKILL.md:110` (`The judges don't care that you used GPT-4. They care that the demo works.`) and `hackathon-ecc/skills/hackathon-pitch/references/win-secrets.md:347` (example table: `We used GPT-4`). Prose/examples, not `model:` fields or pin tables — outside check 7's scope, not banned terms. Left as-is.
- **Gemini mentions (30 lines, not pins):** Gemini API / Gemini CLI as an integration target (`integration/SKILL.md:17,65`, `angular-developer/references/mcp.md:3,51,53`, `track-picker/SKILL.md:23,76`), the Gemini prize, a shields badge (`readme-writer/references/badges.md:34`), and icon-catalog entries (`design-taste-frontend/assets/icons/*`). None is a `model:` field or pin table. Left as-is.
- **Staged sources are clean:** `new-skills/`, `round2-skills/`, `~/workspace/cursor-skills/less-flat-ui/` contribute 0 hits to every banned-term grep; the only staged hits are the `cursor-grok-4.6-high-fast` pins (17 occurrences, all `cursor-`-prefixed) and the 4 `remotion-composer` lines above.

## What was NOT done (per task)

- No plugin file edited, no rebuild, no commit/bundle/GitHub, Campus Eats artifact untouched.
- `fix16/` working files, scratch dirs, and audit backups were not swept (historical record, out of scope).
