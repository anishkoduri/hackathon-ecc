# Sweep #18 — Extended Stale-Check Sweep (fix program #16)

- Date: 2026-11-11 (evening CST)
- Scope: built tree `hackathon-ecc/` (all files except `node_modules`), staged sources `new-skills/` + `round2-skills/` + `~/workspace/cursor-skills/less-flat-ui/`, `LIVE_SMOKE_TEST.md`, shipped README `hackathon-ecc/README.md`, `.cursor-plugin/marketplace.json`. NOT swept: `fix16/` working files (historical record), scratch dirs, audit backups. `build.sh` inventoried separately (check 16) under the acknowledged exception.
- Method: case-insensitive `grep -rni` over the scope for each banned term; every hit read and classified. `build.sh` hits (798 lines) classified by AST analysis of the embedded Python heredocs (string-literal role: OLD vs NEW argument of `patch`/`audit*_patch`/`replace_desc_line`/`replace_text`/`sub`/`txt.replace`, regex pattern, dict key, comment, `print` log, `cp` path), plus bash-comment / heredoc / `cp`-path detection.

## Verdict

**CLEAN — 0 blocking, 0 minor.**

M1/M2 (sweep #17) are fixed and verified (check 7). Audit #55 + dry-run #27's clean verdicts stand: manifest diff 14→15 touches ONLY `skills/strategic-compact/SKILL.md`, manifest diff 15→16 is empty.

## State verification (not assumed)

- `build.sh`: 23,221 lines, md5 `532ab5458c22d6341444fdc92cf67ffd` — matches the stated state.
- Counts (recounted): skills 166, agents 72, rules 123, commands 87, hooks 15 (15 events in `hooks/hooks.json`; 15 `.js` hook scripts + `adapter.js` + `hooks.json` in `hooks/`). Manifests `fix16/manifest-build15.txt` / `manifest-build16.txt`: 2,665 files each.
- `diff manifest-build14.txt manifest-build15.txt`: exactly one line — `skills/strategic-compact/SKILL.md` hash changed. `diff manifest-build15.txt manifest-build16.txt`: empty (diff 0).
- `fix16/build15.log` and `fix16/build16.log`: both end with the standard build-complete footer (`plugin.json: hackathon-ecc 1.0.0`, `build complete: .../hackathon-ecc`); both record `JS SYNTAX FAILURES: 0`, `JSON FAILURES: 0`, `ERRORS: 0`. `fix16/build16.log:897`: `TOTAL BANNED-TERM HITS: 0`.
- Pins: `grok-4.7-high` 45 lines / 52 occurrences in the built tree; `cursor-grok-4.6-high-fast` 99 lines / 100 occurrences in the built tree — both match the stated state.
- `fix15/verify15.py`: **43/43 checks pass**.

## Per-check results

| # | Check | Hits | Result |
|---|---|---|---|
| 1 | `composer-2.5` in scope | 0 | PASS |
| 2 | `claude` in scope | 0 | PASS |
| 3 | `codex` in scope | 0 | PASS |
| 4 | `anthropic` in scope | 0 | PASS |
| 5 | `opus` as a model/vendor word in scope | 0 | PASS (no hits at all — no real-word uses such as "magnum opus" either) |
| 6 | `sonnet` / `haiku` in scope | 0 / 0 | PASS. `fix16.py` self-check term list includes both (`fix16.py:1304` list `r"sonnet", r"haiku"`, also `:976` `AGENT_OWNER_RE`, `:1248-1249` `model: sonnet`/`model: haiku` rewrite rules) |
| 7 | M1/M2 fixed | 0 stray suffixes | PASS — see §M1/M2 verification |
| 8 | Non-Grok model pins (`model:` fields, pin tables, pin examples) | 0 pins | PASS — see §Check 8 detail |
| 9 | `grok-4.7[` bracket hits | 0 | PASS |
| 10 | Bare `grok-4.6-high-fast` (not preceded by `cursor-`) | 0 | PASS. `cursor-` form: 117 occurrences on 115 lines scope-wide (built tree alone: 100 occurrences / 99 lines) |
| 11 | Composer-feature distinction | 50 occurrences, all classified | PASS — none is a model pin, none names Cursor's Composer UI feature — see §Composer-feature list |
| 12 | `LIVE_SMOKE_TEST.md` | §14 present, counts current, 0 stale names | PASS |
| 13 | Stale counts | 0 | PASS |
| 14 | `Claude Code-only` | 0 | PASS — 3 reworded labels quoted below |
| 15 | Antigravity | 14 lines in 6 files, exactly as expected | PASS — no gate-mode reference — see §Antigravity verification |
| 16 | `build.sh` acknowledged exception | 798 lines inventoried | PASS — (a) 389 / (b) 52 / (c1) 355 / (c2) 0 / (c3) 2; zero live pins — see §Check 16 |

### Check 5 — `opus`
0 hits scope-wide. Nothing to list; there is no real-word "opus" use in scope either.

### Check 6 — `sonnet` / `haiku`
0 hits each scope-wide. `fix16.py` self-check term list verified to include both: `fix16.py:1304` (`r"sonnet", r"haiku"` in the banned-term list), `fix16.py:976` (`AGENT_OWNER_RE` includes `sonnet|opus|haiku`), `fix16.py:1248-1249` (rewrite rules `model: sonnet` / `model: haiku` → `model: cursor-grok-4.6-high-fast`).

### Check 8 detail — non-Grok model pins: 0
- `model:` fields matching `gemini|gpt|sonnet|haiku|opus|composer|claude` as the ID: **0**. All `model:` values in scope are Grok slugs (75× `model: cursor-grok-4.6-high-fast`, 5× `model: grok-4.7-high`, 1× `Model: grok-4.7-high`) plus non-pin code/prose tokens (`model:open`, `model:content`, `model: agent.model`, etc. — identifiers, not model IDs).
- A wider grep for `gemini|gpt-[0-9]|sonnet|haiku|\bopus\b|composer-2|claude-[0-9]` returned **32 lines**, every one a non-pin mention, none in a `model:` field, pin table, or pin example:
  - **Gemini API / Gemini CLI / sponsor prize (not a model pin):** `skills/angular-developer/references/mcp.md:3,51,53` (Gemini CLI as an AI assistant in the Angular MCP docs); `skills/integration/SKILL.md:17,65` ("using the Gemini API" sponsor track, `GEMINI_API_KEY`); `skills/track-picker/SKILL.md:23,76` (MLH "Best Use of Gemini API" prize, Gemini API project number); plus the same lines in staged `new-skills/integration/SKILL.md:17,65` and `round2-skills/track-picker/SKILL.md:23,76`.
  - **Gemini brand icon in an icon catalog:** `skills/design-taste-frontend/assets/icons/demo.html:48`, `assets/icons/demo/icons-credits.json:1601-1610`, `assets/icons/index.json:205-207,7580`; same files under staged `new-skills/design-taste-frontend/`.
  - **Gemini shields.io badge:** `skills/readme-writer/references/badges.md:34`.
  - **"GPT-4" in pitch-advice prose (not a pin):** `skills/hackathon-scope/SKILL.md:110` ("The judges don't care that you used GPT-4. They care that the demo works.") and `skills/hackathon-pitch/references/win-secrets.md:347` (weak-pitch example "We used GPT-4" vs a strong outcome line). Both are rhetoric about what judges care about, not a model selection; no `model:` field, no instruction to use GPT-4.
  - A bare-`gpt` grep adds only: `skills/polish-pass/reference/capture.md:33` ("ChatGPT in Chrome" as a browser-tool option), `skills/polish-pass/reference/impeccable-detector-rules.json:545` (detector-rule id `gpt-thin-border-wide-shadow`), `skills/ui-ux-pro-max/data/phosphor-icons-upstream.json:21458` (icon name `chatgpt`); same in `round2-skills/polish-pass/`. None is a model pin.

### Check 12 — `LIVE_SMOKE_TEST.md` (147 lines)
- §14 exists at line 130: `## 14. Grok pins hold — 4.7 High design, 4.6 High Fast task tier (fix programs #13, #16)`, and covers `cursor-grok-4.6-high-fast` (line 134: "confirm the fast-worker / scout actually runs on Grok 4.6 High Fast (`cursor-grok-4.6-high-fast` — the `cursor-` prefix is part of the pin)").
- Step 7 names `grok-4.7-high` (line 80: "Ask for a reasoning-heavy task (should use deep-reasoner → `grok-4.7-high`)"; also lines 78, 132).
- Step 1 counts read 166 skills / 72 agents / 123 rules / 87 commands (line 17).
- Stale-model-name grep over the whole doc (`composer-2.5|claude|codex|anthropic|opus|sonnet|haiku|gemini|gpt-`): **0 hits**.

### Check 13 — stale counts: 0
- `169 skills`, `168 skills`, `96 commands`, `167 skills`, `95 commands`, `88 commands`: **0 hits** scope-wide. Broader sweep for `16[789] skills` / `9[568] commands` / `8[89] commands`: **0 hits**.
- Current counts verified present: "166 skills" — `hackathon-ecc/README.md` ×4 (`:13,36,38,40`) + `LIVE_SMOKE_TEST.md:17`; "87 commands" — README ×2 (`:13,40`) + smoke test `:17`; "72 agents" — README ×2 (`:13,40`) + smoke test `:17`; "123 rules" — README ×1 (`:13`) + smoke test `:17`; hooks count 15 — stated as "hooks (15 events …)" (`README.md:11`), "all 15 hook scripts" (`hooks/adapter.js:6`), and `hooks/hooks.json` contains exactly 15 events (verified by parse). Staged sources contain no count statements at all.
- `README.md:13`: "166 skills, 72 agents, 123 rules, and 87 commands in total." `du -sh hackathon-ecc/` = 56M, matching the README's "56 MB" (both lines 38, 40).

### Check 14 — `Claude Code-only`: 0 hits. Spot-check of 3 reworded labels (was `Claude Code-only`, now `Cursor only`), verified verbatim in the built tree:
- `hackathon-ecc/skills/ck/SKILL.md:13`: `> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc/ck storage.`
- `hackathon-ecc/skills/continuous-learning/SKILL.md:3`: `description: "[DEPRECATED - Cursor only, use continuous-learning-v2] Legacy v1 stop-hook skill extractor. …"`
- `hackathon-ecc/commands/hookify-configure.md:2`: `description: Enable or disable hookify rules interactively (Cursor only — no Cursor equivalent in this plugin)`
- (4th, for the record) `hackathon-ecc/skills/plankton-code-quality/SKILL.md:3`: `… (Cursor only — uses PostToolUse hooks; the auto-fix subprocess was removed in fix #16, so Plankton reports violations instead of auto-fixing)`

## M1/M2 verification

- `hackathon-ecc/skills/strategic-compact/SKILL.md:68` now reads: `- `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection. Set this for large-window models whose reported id lacks a `[1m]` marker (e.g. 500k Grok 4.7 High, or a new 1M-window model family) so the threshold scales to the real window instead of defaulting to 200k and overstating context usage.` — 500k is the verified Grok 4.7 High long-context figure; the bogus "Grok 4.7 High 4.x" is gone.
- `hackathon-ecc/skills/strategic-compact/SKILL.md:102` now reads: `> Cursor **2.1.233 removed the todo/task tools by default** on Grok 4.7 High, Grok 4.6 High Fast,` — no stray " 5" (grep for ` 5` on that line: 0).
- Scope-wide grep for `Grok 4.7 High [0-9]` / `Grok 4.6 High Fast [0-9]` (built tree + staged sources + `LIVE_SMOKE_TEST.md` + shipped README + marketplace.json): **0 hits**.
- Manifest evidence: diff 14→15 touches ONLY `skills/strategic-compact/SKILL.md` (one hash line changed); diff 15→16 is empty.

## Composer-feature list

50 `composer`/`Composer` occurrences in scope, all classified. **None is a model pin and none names Cursor's Composer UI feature.**

### PHP Composer CLI / `composer.json` / `composer.lock` / `composer audit|validate|dump-autoload` (33)
- `hackathon-ecc/rules/php-coding-style.mdc:3:globs: ["**/*.php", "**/composer.json"]`
- `hackathon-ecc/rules/php-hooks.mdc:3:globs: ["**/*.php", "**/composer.json", "**/phpstan.neon", "**/phpstan.neon.dist", "**/psalm.xml"]`
- `hackathon-ecc/rules/php-patterns.mdc:3:globs: ["**/*.php", "**/composer.json"]`
- `hackathon-ecc/rules/php-security.mdc:3:globs: ["**/*.php", "**/composer.lock", "**/composer.json"]`
- `hackathon-ecc/rules/php-security.mdc:18:- Review package trust before adding dependencies. (`composer audit` is END-ONLY — run only at the very end of the project or when the user explicitly asks — deferred security audit, see hackathon-mode §3)`
- `hackathon-ecc/rules/php-testing.mdc:3:globs: ["**/*.php", "**/phpunit.xml", "**/phpunit.xml.dist", "**/composer.json"]`
- `hackathon-ecc/skills/laravel-plugin-discovery/SKILL.md:59:- `package` (string, required): Full Composer package name (e.g. "spatie/laravel-permission")`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:22:- Environment and Composer checks gate everything else; stop immediately if they fail.`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:31:composer --version`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:46:## Phase 1.5: Composer and Autoload`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:49:composer validate`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:50:composer dump-autoload -o`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:89:composer audit  # END-ONLY: run only at the very end of the project or when the user explicitly asks (deferred security audit, see hackathon-mode §3)`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:153:composer --version`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:155:composer validate`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:159:composer audit  # END-ONLY (see Phase 4)`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:168:composer validate`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:169:composer dump-autoload -o`
- `hackathon-ecc/skills/laravel-verification/SKILL.md:173:composer audit  # END-ONLY (see Phase 4)`
- `hackathon-ecc/skills/dev-team/SKILL.md:14:adversarial challenge (`council`), and it is not a free-form team composer`
- `hackathon-ecc/skills/codebase-onboarding/SKILL.md:29:     Gemfile, composer.json, mix.exs, pubspec.yaml`
- `hackathon-ecc/skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39:| `styles/*.yaml`, `remotion-composer/`, `ink-theater/`, `backlot/`, `docs/`, `tests/` | Playbooks, composer app, review UI, docs, tests | Out of scope for a hackathon demo video |`
- `hackathon-ecc/skills/pitch-deck-video/references/openmontage/README.md:35:- Schemas, styles/playbooks, remotion-composer, ink-theater, backlot,`
- `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:77:- **Stack**: detect from the project — check `package.json` deps (react/next/vue/svelte/nuxt/@angular), `pubspec.yaml` (Flutter), `*.xcodeproj`/`Package.swift` (SwiftUI), `composer.json` (Laravel), or React Native markers (`app.json` + `react-native` dep). If nothing is detectable and stack guidance matters, ask the user — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you do NOT ask: resolve by stated assumption with the safe/reversible default and proceed. **Never assume a stack** — a hardcoded default silently misroutes every recommendation.`
- `hackathon-ecc/skills/ui-ux-pro-max/data/ui-reasoning.csv:165:164,Forum / Discussion Board,Community/Forum Landing,Dark Mode (OLED) + Flat Design,Dark neutral + topic accent colors + unread indicator + reputation badge,Readable + Community-first typography,Thread expand/collapse + Reply composer cues,"{""must_have"":[""constraint:thread-list"",""constraint:reply-composer"",""constraint:vote-signals"",""constraint:moderation-tools"",""constraint:user-badges""],""if_content_focused"":[""constraint:prioritize-clarity""],""if_ux_focused"":[""constraint:optimize-touch-targets""]}",No moderation cues + cluttered threads + hidden post state,HIGH,"discussion UX depends on scan-friendly threads, reputation cues, and visible moderation states",0.93`
- `hackathon-ecc/agents/ecc-php-reviewer.md:77:composer audit                             # Dependency vulnerabilities # END-ONLY — run only at the very end of the project or when the user explicitly asks`
- `hackathon-ecc/scripts/hooks/cursor-session-env.js:3: * Cursor sessionStart hook — inject ECC_AGENT_DATA_HOME for the composer session.`
- `hackathon-ecc/scripts/lib/gateguard-search-filters.js:43:  json: ['*.json', '*.sarif', 'composer.lock'],`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:171:  .composer{padding:10px 14px 14px;border-top:1px solid var(--border);display:flex;flex-direction:column;gap:8px}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:172:  .composer .hint{font-size:10px;color:var(--text3)}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:173:  .composer textarea{width:100%;min-height:60px;max-height:160px;resize:vertical;background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:8px 10px;color:var(--text);font-size:12.5px;font-family:var(--font);outline:none;transition:all .15s}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:174:  .composer textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:175:  .composer .row{display:flex;gap:8px;align-items:center}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:176:  .composer .send{flex:1;height:32px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-size:12.5px;font-weight:600;cursor:pointer;transition:all .12s}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:177:  .composer .send:hover{background:var(--accent-dim)}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:178:  .composer .send:disabled{opacity:.5;cursor:default}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:179:  .composer .status{font-size:10.5px;color:var(--text3)}`
- `hackathon-ecc/scripts/lib/plan-canvas/ui.js:517:    <div class="composer">`
- `hackathon-ecc/scripts/lib/project-detect.js:85:    markers: ['composer.json', 'composer.lock'],`
- `hackathon-ecc/scripts/lib/project-detect.js:305: * Read composer.json for PHP package dependencies`
- `hackathon-ecc/scripts/lib/project-detect.js:309:function getComposerDeps(projectDir) {`
- `hackathon-ecc/scripts/lib/project-detect.js:311:    const composerPath = path.join(projectDir, 'composer.json');`
- `hackathon-ecc/scripts/lib/project-detect.js:312:    if (!fs.existsSync(composerPath)) return [];`
- `hackathon-ecc/scripts/lib/project-detect.js:313:    const composer = JSON.parse(fs.readFileSync(composerPath, 'utf8'));`
- `hackathon-ecc/scripts/lib/project-detect.js:314:    return [...Object.keys(composer.require || {}), ...Object.keys(composer['require-dev'] || {})];`
- `hackathon-ecc/scripts/lib/project-detect.js:397:  const composerDeps = getComposerDeps(projectDir);`
- `hackathon-ecc/scripts/lib/project-detect.js:423:          depList = composerDeps;`
- `hackathon-ecc/scripts/lib/project-detect.js:487:  getComposerDeps,`
- `new-skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39:| `styles/*.yaml`, `remotion-composer/`, `ink-theater/`, `backlot/`, `docs/`, `tests/` | Playbooks, composer app, review UI, docs, tests | Out of scope for a hackathon demo video |`
- `new-skills/pitch-deck-video/references/openmontage/README.md:35:- Schemas, styles/playbooks, remotion-composer, ink-theater, backlot,`

- Classification of the 50, by file:line:
  - **PHP Composer (33):** `hackathon-ecc/rules/php-coding-style.mdc:3`, `php-hooks.mdc:3`, `php-patterns.mdc:3`, `php-security.mdc:3,18`, `php-testing.mdc:3` (globs `**/composer.json`, `**/composer.lock`; `composer audit` END-ONLY); `skills/laravel-plugin-discovery/SKILL.md:59` (Composer package name); `skills/laravel-verification/SKILL.md:22,31,46,49,50,89,153,155,159,168,169,173` (`composer --version` / `validate` / `dump-autoload -o` / `audit`); `skills/codebase-onboarding/SKILL.md:29` (`composer.json` as a project marker); `skills/ui-ux-pro-max/SKILL.md:77` (`composer.json` as a Laravel stack marker); `agents/ecc-php-reviewer.md:77` (`composer audit` END-ONLY); `scripts/lib/gateguard-search-filters.js:43` (`composer.lock` in a JSON/SARIF filter list); `scripts/lib/project-detect.js:85,305,309,311,312,313,314,397,423,487` (`composer.json`/`composer.lock` markers, `getComposerDeps()`).
  - **"team composer" prose (1):** `skills/dev-team/SKILL.md:14` ("it is not a free-form team composer") — ordinary English, not a feature.
  - **"Reply composer" UI prose (1):** `skills/ui-ux-pro-max/data/ui-reasoning.csv:165` ("Reply composer cues" — forum-thread UI constraint).
  - **remotion-composer, the OpenMontage video-composer app directory (4):** `skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39` and `references/openmontage/README.md:35`, in the built tree and again in staged `new-skills/pitch-deck-video/` (same two lines). It is a directory/app name inside the vendored OpenMontage reference docs, not Cursor's Composer.
  - **CSS `.composer` class, plan-canvas UI (10):** `scripts/lib/plan-canvas/ui.js:171-179` (`.composer`, `.composer .hint`, `.composer textarea`, `.composer .row`, `.composer .send`, `.composer .status` styles) and `:517` (`<div class="composer">`).
  - **"composer session" = the Cursor session (1):** `scripts/hooks/cursor-session-env.js:3`: `* Cursor sessionStart hook — inject ECC_AGENT_DATA_HOME for the composer session.` Verified by reading the file: it is the Cursor sessionStart hook; "composer session" is the Cursor agent session the hook runs in (the file's header cites `https://cursor.com/docs/hooks` and the hook passes session-scoped env to later hooks). NOT the Composer UI feature.

## Antigravity verification

Exactly **14 lines in 6 files**, matching the expected list line for line:
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

File spread: `angular-developer/references/mcp.md` ×2 (Antigravity IDE MCP docs), `scripts/lib/install-lifecycle.js` ×5 (legacy install-state warnings, `legacy-antigravity-layout`), `scripts/lib/install/apply.js` ×3 (fix #16 removal comment + empty `antigravityMigrationWarnings` carrier), `scripts/lib/install/content-transform.js` ×1 (historical comment), `scripts/lib/install/stale-operations-reconciliation.js` ×2 (legacy-compat), `scripts/auto-update.js` ×1 (migrate message). Staged `design-taste-frontend` skill: **0 hits** (verified separately over `new-skills/design-taste-frontend`; staged sources overall: 0 hits). Hooks dir (`hackathon-ecc/hooks/`): **0 hits**.

**Gate-mode check:** the install-target gate accepts only `cursor` — `scripts/lib/install/request.js:6` `const LEGACY_INSTALL_TARGETS = ['cursor'];` (also `plan.js:223` `const target = options.target || 'cursor';`). The one line that looks gate-adjacent, `stale-operations-reconciliation.js:52` `return !(request && request.legacyMode && plan.target === 'antigravity');`, is inside `materializesWholeModules()` — a legacy-compat filter for old install *plans* (pure-legacy plans share a module id across languages; an absent operation is not stale there). It does not accept, select, or gate any install target; no hook mode, no model pin, no banned term. **No antigravity gate-mode reference found.**

## Check 16 — build.sh acknowledged-exception inventory (798 lines)

Method: every line of `build.sh` matching `composer-2.5|claude|codex|anthropic|opus|sonnet|haiku` (case-insensitive) was classified by AST analysis of the embedded Python heredocs (string-literal role: OLD vs NEW argument of `patch`/`audit*_patch`/`replace_desc_line`/`replace_text`/`append_desc`/`sub`/`txt.replace`, regex pattern, dict key, comparison test, `print` log string), plus bash-comment / heredoc / `cp`-path detection. Three-tuple subs blocks (`for rel, old, new in subs:`) were classified by tuple position (element 1 = OLD, element 2 = NEW), confirmed against the consumer loop (`assert t.count(old) == 1; t.replace(old, new)`).

| Class | Count | Meaning | Ships a banned term? |
|---|---|---|---:|
| (a) OLD-side match pattern | 389 | Upstream text / regex the build patches *away from* (e.g. `re.search(r"^model: (sonnet\|opus\|haiku)\s*$")` at :164, the `{"sonnet": …, "opus": …, "haiku": …}` mapping at :157, OLD args of `sub`/`audit*_patch` pairs) | No — matched and replaced, never written out |
| (b) Comment / build log | 52 | Bash comments (23) + Python comments (29) + `print` log strings | No — not shipped |
| (c1) NEW-side patch text | 355 | Replacement text written into the tree mid-build by the audit-fix heredocs | **No — see resolution below.** Written mid-build, then rewritten/removed by fix16 (the last build step); final tree grep = 0 for every banned term, and fix16's own self-check reads `TOTAL BANNED-TERM HITS: 0` (`fix16/build16.log:897`). |
| (c2) Heredoc file write | 0 | No banned-term hit inside any `cat >` / `cat >>` file-write heredoc (4 such heredocs: marketplace.json, plugin.json, github-coordination.js append, README.md) | — |
| (c3) Build-time source path | 2 | :265 `cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" …`, :298 `cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" …` | No — upstream-layout paths, not shipped text |
| **Total** | **798** | | **0 live pins; 0 shipped banned terms** |

Per-term line counts (case-insensitive substring; a line can carry >1 term): `claude` 701, `codex` 103, `anthropic` 5, `opus` 22, `sonnet` 23, `haiku` 13, `composer-2.5` 0. Per-term occurrence counts: `claude` 930, `codex` 126, `anthropic` 8, `opus` 26, `sonnet` 24, `haiku` 13. (Sweep #17 reported slightly different per-term totals — 679/96/5/18/23/11 — a counting-convention difference; the 798-line total and the class totals 389/52/355/0/2 match exactly, re-derived here independently.)

### (c2) heredoc verification
`build.sh:18296` reads: `"description": "Configuration for Cursor hooks, as shipped in hooks/hooks.json. Cursor format: camelCase event names as keys, each mapping to an array of items with a command, the event name, and an optional description. This is distinct from schemas/hooks.schema.json, which describes the legacy hooks format (PascalCase events, matcher entries with {type, command} items) and does not accept this file.",` — it says **"the legacy hooks format"**, not "Claude Code hooks format". ✓
### (c3) path verification
`:265` and `:298` are the verified upstream-layout `.claude/skills/` `cp` source paths (shown in the table above). ✓

### Zero live pins among the (c) hits — verification
17 (c1) lines contain a pin-like reference (`model: sonnet/haiku`, `--model sonnet`, `'haiku'` default, `gpt-6-astra`, `claude -p --model sonnet`). Each was traced to its target file and checked in the shipped tree:
- `:15142` `audit7_patch` on `skills/continuous-learning-v2/scripts/instinct-cli.py`: OLD `content += "model: sonnet\ntools: Read, Grep, Glob\n---\n"` → NEW `content += "model: sonnet\n---\n"` — the NEW text still carries `model: sonnet`. In the shipped tree, `hackathon-ecc/skills/continuous-learning-v2/scripts/instinct-cli.py:2017` reads `content += "model: cursor-grok-4.6-high-fast\n---\n"` — fix16's re-pin rule (`fix16.py:1248`) rewrote it. **Scrubbed, not shipped.**
- `:13020` (`--gen-model haiku --model sonnet` example, target `skills/skill-comply/SKILL.md`), `:14258` (`|| 'haiku'` default, target `scripts/lib/llm-summary.js`): neither target file exists in the shipped tree — both were removed upstream of the final tree. **Not shipped.**
- `:7808/:7815/:7828` + `:11592/:11598` (GPT-6-Astra / Codex CLI, target `commands/astra-review.md`): the shipped file's description now reads "Deep, blind code review … by a fresh Grok deep-reasoner … (The Astra review backend was removed in fix #16; review now runs via Grok reviewers in Cursor.)" **Scrubbed, not shipped.**
- `:22593/:22597/:22601/:22605` (`claude -p --model sonnet` in gan-style-harness docs), `:3523` (harness list naming `claude`/`codex`/`gemini`), `:5124` ("Haiku agent"), `:8377` ("Claude Opus"), `:6925`/`:11876`/`:12753` (other model-name prose in NEW text): final-tree grep for `model: (sonnet|haiku|opus)`, `--model (sonnet|haiku|opus)`, `gpt-6-astra`, `claude -p` = **0**. **Scrubbed, not shipped.**
- The (c1) class as a whole contains 350 lines mentioning `claude`/`codex`/`anthropic` — all of it mid-build NEW text (mostly "Claude Code only — no Cursor equivalent" labels and upstream `claude -p` docs) that fix16 rewrote or removed. The final-tree greps in checks 1–6 (0 hits for every banned term) are the ground truth that none of it ships.

### Full build.sh inventory table
`line | class | term(s) | text (truncated at 150 chars)`
| 150 | b | claude | # Pin ECC agent models to Grok IDs (fix #16). The install ships bare Claude aliases |
| 151 | b | haiku,opus,sonnet | # (sonnet/opus/haiku), which are not Cursor model IDs. Map: sonnet -> |
| 152 | b | haiku,opus | # cursor-grok-4.6-high-fast, opus -> grok-4.7-high, haiku -> |
| 157 | a | haiku,opus,sonnet | mapping = {"sonnet": "cursor-grok-4.6-high-fast", "opus": "grok-4.7-high", "haiku": "cursor-grok-4.6-high-fast"} |
| 164 | a | haiku,opus,sonnet | m = re.search(r"^model: (sonnet\|opus\|haiku)\s*$", txt, re.M) |
| 174 | b | claude | # Claude Code review loop the plugin does not ship). Drop it. |
| 210 | b | opus | # only the opus bracket pin was removed; cursor-grok-4.6-high-fast remains |
| 265 | c3 | claude | cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" "$PLUGIN_DIR/skills/ui-ux-pro-max" |
| 298 | c3 | claude | cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" "$PLUGIN_DIR/skills/hackathon-pitch" |
| 414 | b | claude | # or by a Claude Code ~/.claude/rules/ path, which is not a plugin path) |
| 415 | a | claude | pat_file = re.compile(rf"(?<!ecc/)(?<!claude/rules/)({RULE_DIRS})/({RULE_FILES})\.md") |
| 473 | b | claude | # The stock example installs quality-gate.py as a Claude Code Stop hook at |
| 474 | b | claude | # ~/.claude/scripts/. That path does not exist in Cursor, and an automatic |
| 486 | a | claude | mkdir -p ~/.claude/scripts |
| 487 | a | claude | cp skills/delivery-gate/hooks/quality-gate.py ~/.claude/scripts/ |
| 490 | a | claude | Add to `~/.claude/settings.json`: |
| 497 | a | claude | "command": "python3 ~/.claude/scripts/quality-gate.py", |
| 551 | c1 | claude | append_desc("agents-md-generator", ". Use ONLY when the user explicitly asks for an AGENTS.md file. Do not use for CLAUDE.md onboarding (codebase-onbo |
| 593 | a | claude | "description: Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (surface text heuristics), stale |
| 599 | a | claude | "description: Run a six-phase verification of a Claude Code session's work — build, type check, lint, tests with coverage, security grep, and diff rev |
| 602 | a | claude | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using Agen |
| 603 | c1 | claude | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using Agen |
| 888 | a | claude | - Setting up a new Claude Code project |
| 889 | a | claude | - After modifying `.claude/settings.json`, `CLAUDE.md`, or MCP configs |
| 891 | a | claude | - When onboarding to a new repository with existing Claude Code configs |
| 944 | a | claude | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spen |
| 945 | c1 | claude | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spen |
| 1035 | a | claude | "uv run python -m scripts.run --dry-run ~/.claude/skills/search-first/SKILL.md", |
| 1036 | c1 | claude | "uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md", |
| 1535 | a | claude | ("""Summarize local Claude Code spend by day, model, and session from the metrics |
| 1541 | a | claude | `~/.claude/metrics/costs.jsonl`. Each row is a **cumulative snapshot for that |
| 1548 | c1 | claude | """Summarize local Claude Code spend by day, model, and session from the metrics |
| 1554 | c1 | claude | `~/.claude/metrics/costs.jsonl` (Claude Code only — no Cursor equivalent in this plugin). Each row is a **cumulative snapshot for that |
| 1567 | a | claude | 1. Check that `~/.claude/metrics/costs.jsonl` exists. If it does not, tell the |
| 1580 | c1 | claude | 1. Check that `~/.claude/metrics/costs.jsonl` (Claude Code only) exists. If it does not, tell the |
| 2213 | a | claude | - **Global** (`~/.claude/skills/<pattern-name>/SKILL.md`): Generic patterns usable across 2+ projects (bash compatibility, LLM API behavior, debugging |
| 2214 | a | claude | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a particular config file, project-s |
| 2216 | a | claude | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 2227 | c1 | claude | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a particular config file, project-s |
| 2229 | c1 | claude | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 2239 | a | claude | `~/.claude/skills/`, project `.claude/skills/`, or `MEMORY.md` as |
| 2252 | c1 | claude | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| 2265 | a | claude | - [ ] Grep `~/.claude/skills/` and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 2278 | c1 | claude | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 2293 | a | claude | Create a skill at `~/.claude/skills/<pattern-name>/SKILL.md`: |
| 2319 | a | claude | inside the approved skill root (`~/.claude/skills/`). |
| 2345 | a | claude | 5. Save to `~/.claude/skills/<pattern-name>/SKILL.md` |
| 2373 | a | claude | The CLI scans local Claude transcript JSONL files under |
| 2374 | a | claude | `~/.claude/projects/**` and reports stale `ScheduleWakeup` calls or `Bash` |
| 2400 | a | claude | - `ecc loop-status --watch --write-dir ~/.claude/loops` maintains |
| 2444 | a | codex | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 2446 | a | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2456 | c1 | codex | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 2458 | c1 | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2547 | a | claude | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and delivery. |
| 2549 | a | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2559 | c1 | claude | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and delivery. |
| 2561 | c1 | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2569 | a | claude,codex | ('- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missing, must confirm first)\n\n---\n\n## Multi-Model C |
| 2570 | c1 | claude,codex | '- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missing, must confirm first)\n\n---\n\n## Multi-Model Ca |
| 2646 | a | claude,codex | ("""\| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 2666 | c1 | claude,codex | """\| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 2685 | a | codex | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| 2686 | a | codex | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| 2692 | a | codex | - Codex: Handle backend part |
| 2701 | c1 | codex | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| 2702 | c1 | codex | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| 2708 | c1 | codex | - Codex: Handle backend part |
| 2720 | a | codex | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| 2722 | a | codex | 1. **Codex Review** (`run_in_background: true`): |
| 2723 | a | claude,codex | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| 2728 | a | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| 2736 | a | codex | 1. Synthesize Codex + Antigravity review feedback |
| 2737 | a | codex | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| 2743 | c1 | codex | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| 2745 | c1 | codex | 1. **Codex Review** (run in parallel): |
| 2746 | c1 | claude,codex | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| 2751 | c1 | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| 2759 | c1 | codex | 1. Synthesize Codex + Antigravity review feedback |
| 2760 | c1 | codex | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| 2769 | a | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2781 | c1 | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2872 | a | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2884 | c1 | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 2898 | a | codex | - **Mandatory Parallel**: Codex/Antigravity calls MUST use `run_in_background: true` (including single model calls, to avoid blocking main thread) |
| 2899 | a | claude | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by Claude |
| 2901 | a | claude | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify production code** |
| 2911 | c1 | codex | - **Mandatory Parallel**: Codex/Antigravity calls MUST run in parallel (including single model calls, to avoid blocking main thread) |
| 2912 | c1 | claude | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by Claude |
| 2914 | c1 | claude | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify production code** |
| 2918 | a | claude,codex | ('- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify production code**\n\n---\n\n |
| 2919 | c1 | claude,codex | '- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, but **NEVER modify production code**\n\n---\n\n# |
| 2945 | a | claude,codex | ("""\| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 2965 | c1 | claude,codex | """\| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 2989 | a | codex | **Parallel call** Codex and Antigravity (`run_in_background: true`): |
| 2993 | a | codex | 1. **Codex Backend Analysis**: |
| 2994 | a | claude,codex | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| 3002 | c1 | codex | **Parallel call** Codex and Antigravity (run them in parallel): |
| 3006 | c1 | codex | 1. **Codex Backend Analysis**: |
| 3007 | c1 | claude,codex | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| 3011 | a | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| 3015 | a | codex | Wait for both models' complete results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3024 | c1 | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| 3028 | c1 | codex | Wait for both models' complete results (their returned output). **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3038 | a | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| 3043 | a | claude | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| 3051 | c1 | claude | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| 3056 | c1 | claude | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| 3066 | a | codex | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intelligent routing: Frontend → Antigr |
| 3068 | a | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 3078 | c1 | codex | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intelligent routing: Frontend → Antigr |
| 3080 | c1 | claude | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workflow` |
| 3088 | a | claude,codex | ('- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Specification\n\n**Call syntax** (parallel: `run_in |
| 3089 | c1 | claude,codex | '- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Specification\n\n**Call syntax** (parallel: run the  |
| 3140 | a | claude,codex | ("""\| Analysis \| `~/.claude/.ccg/prompts/codex/analyzer.md` \| `~/.claude/.ccg/prompts/antigravity/analyzer.md` \| |
| 3141 | a | claude,codex | \| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 3142 | a | claude,codex | \| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 3164 | c1 | claude,codex | """\| Analysis \| `~/.claude/.ccg/prompts/codex/analyzer.md` \| `~/.claude/.ccg/prompts/antigravity/analyzer.md` \| |
| 3165 | c1 | claude,codex | \| Planning \| `~/.claude/.ccg/prompts/codex/architect.md` \| `~/.claude/.ccg/prompts/antigravity/architect.md` \| |
| 3166 | c1 | claude,codex | \| Review \| `~/.claude/.ccg/prompts/codex/reviewer.md` \| `~/.claude/.ccg/prompts/antigravity/reviewer.md` \| |
| 3199 | a | claude | node scripts/orchestrate-worktrees.js .claude/plan/workflow-e2e-test.json --execute |
| 3233 | a | codex | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| 3236 | a | codex | Wait for results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3250 | c1 | codex | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| 3253 | c1 | codex | Wait for their returned output. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| 3263 | a | codex | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| 3270 | a | claude,codex | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/task-name.md` after user approval. |
| 3276 | c1 | codex | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| 3283 | c1 | claude,codex | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/task-name.md` after user approval. |
| 3289 | a | codex | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| 3302 | c1 | codex | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| 3501 | a | claude,codex | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gemini`, `opencode`, `codebuddy`, `joycode`, or `qwen |
| 3523 | c1 | claude,codex | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gemini`, `opencode`, `codebuddy`, `joycode`, or `qwen |
| 3549 | a | claude | ## CLAUDE.md Guidance |
| 3551 | a | claude | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it minimal:""", |
| 3563 | c1 | claude | ## CLAUDE.md Guidance |
| 3565 | c1 | claude | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it minimal:"""), |
| 3567 | a | claude | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| 3577 | c1 | claude | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| 3848 | a | claude | #### Reviewer A: Claude Agent (always runs) |
| 3850 | a | opus | Launch an Agent (subagent_type: `code-reviewer`, model: `opus`) with the full rubric + all files under review. The prompt must include: |
| 3856 | a | claude | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| 3861 | c1 | claude | #### Reviewer A: Claude Agent (always runs) |
| 3869 | c1 | claude | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| 3876 | a | claude,opus | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second Claude Agent (subagent_type: `code-reviewer`, model: `opus`) with |
| 3889 | c1 | claude | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `ecc-code-reviewer` with the rubric and file conte |
| 3904 | a | claude | - `path` (optional): defaults to the current project. Use a `.claude/` path, a repo root, or a checked-in template directory. |
| 3927 | a | claude | description: Manage Claude Code session history, aliases, and session metadata. |
| 3932 | a | claude | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/session-data/` with legacy reads from `~/.claude/sessio |
| 3940 | c1 | claude | description: Manage Claude Code session history, aliases, and session metadata. |
| 3945 | c1 | claude | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/session-data/` with legacy reads from `~/.claude/sessio |
| 3958 | a | claude | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.claude/sessions/` |
| 3959 | a | claude | - Aliases are stored in `~/.claude/session-aliases.json` |
| 3969 | c1 | claude | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.claude/sessions/` (Claude Code only) |
| 3970 | c1 | claude | - Aliases are stored in `~/.claude/session-aliases.json` (Claude Code only) |
| 3984 | a | claude | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that teach Claude your team's practices. |
| 3993 | c1 | claude | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that teach Claude your team's practices. |
| 4027 | a | claude | Located in `~/.claude/agents/`: |
| 4121 | a | claude | Note: ECC-managed installs set `"includeCoAuthoredBy": false` in `~/.claude/settings.json`, so commits carry no `Co-Authored-By` trailer by default. T |
| 4134 | c1 | claude | Note: this paragraph describes Claude Code installs and does not apply to this Cursor plugin install — Cursor commit attribution follows the project's |
| 4165 | a | claude | - Configure `permissions.allow` rules in `~/.claude/settings.json` (or a project's `.claude/settings.json`) instead |
| 4182 | c1 | claude | - Configure Cursor permissions in the project's Cursor settings instead of Claude Code's `~/.claude/settings.json`. |
| 4201 | a | haiku,sonnet | **Haiku 4.5** (90% of Sonnet capability, 3x cost savings): |
| 4206 | a | sonnet | **Sonnet 5** (Best coding model): |
| 4211 | a | opus | **Opus 5** (Deepest reasoning): |
| 4246 | a | claude | In Claude Code, adaptive reasoning lets the model choose how much to think for each task. |
| 4247 | a | opus,sonnet | For Fable models, Sonnet 5 and later, and Opus 4.7 and later, use effort to control reasoning |
| 4251 | a | claude,opus | - **Effort**: Use `/effort` in a session, `--effort <level>` at launch, or `CLAUDE_CODE_EFFORT_LEVEL`. Save a per-model level in `modelSettings` in `~ |
| 4252 | a | opus,sonnet | - **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux), or `alwaysThinkingEnabled` in settings. These cannot disable thinking on Opus 5.5, Sonnet 5.5, |
| 4253 | a | claude,opus,sonnet | - **Fixed budget**: Claude Code ignores positive `MAX_THINKING_TOKENS` values on adaptive reasoning models. On Opus 4.6 or Sonnet 4.6, set `CLAUDE_COD |
| 4256 | a | claude | See [Claude Code model configuration](https://code.claude.com/docs/en/model-config#adjust-effort-level) |
| 4257 | a | claude | and [environment variables](https://code.claude.com/docs/en/env-vars) for supported controls. |
| 4490 | a | claude,codex | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| 4503 | c1 | claude,codex | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| 4519 | a | claude | <!-- .claude/commands/bug-check.md --> |
| 4588 | a | claude | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 4596 | c1 | claude | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 4612 | a | claude | `~/.claude/skills/ck/commands/` for a manual install, or the ck skill inside the ECC |
| 4613 | a | claude | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| 4614 | a | claude | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| 4629 | c1 | claude | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| 4630 | c1 | claude | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| 4641 | a | claude | ~/.claude/ck/ |
| 4669 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| 4682 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| 4721 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| 4730 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4743 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| 4752 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4757 | a | claude | ("""node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4765 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| 4776 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4779 | c1 | claude | """node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| 4787 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| 4798 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4801 | a | claude | ("""node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4809 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| 4813 | a | claude | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run""", |
| 4814 | c1 | claude | """node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| 4822 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| 4826 | c1 | claude | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run"""), |
| 4827 | a | claude | ('\n---\n\n## SessionStart Hook\n\nThe hook at `hooks/session-start.mjs` in this skill\'s directory must be registered in\n`~/.claude/settings.json` t |
| 4829 | a | claude | ("""unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| 4840 | c1 | claude | """unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| 4970 | a | claude | description: Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, cac |
| 4975 | a | claude | # Config GC — Garbage Collection for Claude Code Setups |
| 4979 | c1 | claude | description: Garbage collection for your Claude Code configuration (Claude Code only — this skill targets a Claude Code install, not this Cursor plugi |
| 4984 | c1 | claude | # Config GC — Garbage Collection for Claude Code Setups |
| 5013 | a | codex | \| Codex CLI \| `/status` \| Shows current token usage and remaining context capacity. Use `/statusline` and enable **Context stats** plus **Token counte |
| 5014 | a | codex | \| Codex app \| `/status` \| Shows current thread context usage and rate limits. \| |
| 5015 | a | claude | \| Claude Code \| `/context` \| Shows the live context breakdown. Use `/context all` for expanded items. \| |
| 5018 | a | claude,codex | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/cli/slash-commands) and [Claude Code command refere |
| 5028 | c1 | codex | \| Codex CLI (Codex only) \| `/status` \| Shows current token usage and remaining context capacity. Use `/statusline` and enable **Context stats** plus * |
| 5029 | c1 | codex | \| Codex app (Codex only) \| `/status` \| Shows current thread context usage and rate limits. \| |
| 5030 | c1 | claude | \| Claude Code (Claude Code only) \| `/context` \| Shows the live context breakdown. Use `/context all` for expanded items. \| |
| 5033 | c1 | claude,codex | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/cli/slash-commands) and [Claude Code command refere |
| 5043 | a | claude | [`/context` and `/usage` commands (`/cost` is an alias)](https://code.claude.com/docs/en/commands). |
| 5051 | c1 | claude | [`/context` and `/usage` commands (Claude Code only; `/cost` is an alias)](https://code.claude.com/docs/en/commands). |
| 5093 | a | claude | No extra `settings.json` hook block is required. Claude Code v2.1+ auto-loads the plugin `hooks/hooks.json`, and `observe.sh` is already registered th |
| 5095 | a | claude | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` block. Duplicating the plugin |
| 5097 | a | claude | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| 5108 | c1 | claude | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` block. Duplicating the plugin |
| 5110 | c1 | claude | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| 5116 | a | haiku | 2. **Background observer** - Haiku agent analyzing in parallel |
| 5124 | c1 | haiku | 2. **Background observer** - Haiku agent analyzing in parallel |
| 5133 | a | codex | ('- suppresses model-visible skill instructions and shell environment inheritance;\n- uses an ephemeral, read-only session with approval escalation di |
| 5155 | a | claude | - the in-context Claude voice |
| 5236 | a | claude | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| 5249 | c1 | claude | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| 5293 | a | claude | # Delivery Gate — Mechanical Quality Gate for Claude Code |
| 5295 | a | claude | A **Stop hook** that checks three things before Claude can finish a session, using only **deterministic checks** — file modification timestamps, disk  |
| 5329 | a | claude | The hook blocks a given Stop at most once. When Claude Code re-runs it with `stop_hook_active: true` (Claude already continued once because of this ho |
| 5333 | a | claude | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a different failure mode: the agent produces working code w |
| 5350 | c1 | claude | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a different failure mode: the agent produces working code w |
| 5359 | a | claude | Create these files in your project's memory directory (`~/.claude/projects/<encoded-project-path>/memory/`, where every non-alphanumeric character of  |
| 5751 | a | claude | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conflicts with the operator one at |
| 5763 | c1 | claude | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conflicts with the operator one at |
| 5798 | a | claude | ('- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & State-Control Rules]** — concrete, checkable conventi |
| 5799 | c1 | claude | '- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & State-Control Rules]** — concrete, checkable conventio |
| 6178 | a | claude | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 6202 | c1 | claude | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 6376 | a | claude | ### Pattern A: Claude Code Subagents (Recommended) |
| 6381 | a | claude | # In a Claude Code session, use the Agent tool to spawn reviewers |
| 6389 | c1 | claude | ### Pattern A: Claude Code Subagents (Recommended) |
| 6425 | a | claude | description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using Agent |
| 6432 | a | claude | Audit your Claude Code configuration for security issues using [AgentShield](https://github.com/affaan-m/agentshield). |
| 6461 | a | claude | \| `CLAUDE.md` \| Hardcoded secrets, auto-run instructions, prompt injection patterns \| |
| 6487 | a | claude | Run against the current project's `.claude/` directory: |
| 6494 | a | claude | npx ecc-agentshield scan --path /path/to/.claude |
| 6527 | a | claude | Scaffold a new secure `.claude/` configuration from scratch: |
| 6553 | a | claude | - `CLAUDE.md` with security best practices |
| 6579 | a | claude | - Auto-run instructions in CLAUDE.md (prompt injection vector) |
| 6607 | a | claude | Slash command (`/skill-stocktake`) that audits all Claude skills and commands using a quality checklist + AI holistic judgment. Supports two modes: Qu |
| 6633 | a | claude | \| `~/.claude/skills/` \| Global skills (all projects) \| |
| 6634 | a | claude | \| `{cwd}/.claude/skills/` \| Project-level skills (if the directory exists) \| |
| 6661 | a | claude | If the project has no `.claude/skills/` directory, only global skills and commands are evaluated. |
| 6681 | a | claude | ('\|------\|---------\|---------\|\n\| Quick Scan \| `results.json` exists (default) \| 5–10 min \|\n\| Full Stocktake \| `results.json` absent, or `/skill-stoc |
| 6683 | a | claude | ('\nRun this entire block in **one Bash invocation**. It prints the inventory for the agent and initializes a new full run only when there is no unfin |
| 6685 | a | claude | ('      \| .mode = "full"\n      \| .batch_progress = {\n          total: ($inventory.skills \| length),\n          evaluated: (.skills \| length), status |
| 6687 | a | claude | ('\nThe subagent reads each assigned skill, applies the checklist, and returns a JSON object with a `skills` map keyed by the inventory path. Each ent |
| 6695 | a | claude | RESULTS_JSON=~/.claude/skills/skill-stocktake/results.json |
| 6715 | a | claude | ('    if (.skills \| length) == .batch_progress.total then\n      {skills: {}, mode: "full", batch_progress: (.batch_progress + {\n        evaluated: ( |
| 6723 | a | claude | `~/.claude/skills/skill-stocktake/results.json`: |
| 6749 | a | claude | "~/.claude/skills/skill-name/SKILL.md": { |
| 6750 | a | claude | "path": "~/.claude/skills/skill-name/SKILL.md", |
| 6884 | a | claude | **Installed as a plugin?** No setup is needed. The plugin's `hooks/hooks.json` already registers `suggest-compact.js` (hook id `pre:edit-write:suggest |
| 6886 | a | claude | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 6904 | c1 | claude | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings.json` — `~/.claude/scripts/` does not exist on plu |
| 6906 | c1 | claude | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 6912 | a | opus | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection. Set this for large-window models whose reported id |
| 6913 | a | claude | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smaller than the model's context window. For context-win |
| 6925 | c1 | opus | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection. Set this for large-window models whose reported id |
| 6926 | c1 | claude | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smaller than the model's context window. For context-win |
| 6971 | a | claude | # Use the configured plugin root or standalone install (~/.claude or |
| 6972 | a | claude | # $CLAUDE_CONFIG_DIR). For a reviewed and explicitly authorized ECC checkout: |
| 6973 | a | claude | # export CLAUDE_PLUGIN_ROOT="/absolute/path/to/reviewed/ECC" |
| 6974 | a | claude | ECC_ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}" |
| 6975 | a | claude | [ -f "$ECC_ROOT/scripts/setup-package-manager.js" ] \|\| { echo "ECC scripts not found in the selected root (set CLAUDE_PLUGIN_ROOT to an authorized ECC |
| 6979 | a | claude | The resolution lines use the configured plugin root or standalone install and stop when the selected root lacks the helper. For an ECC checkout you ha |
| 6981 | a | claude | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/package-manager.json`, the `package.json` |
| 7001 | c1 | claude | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/package-manager.json`, the `package.json` |
| 7060 | a | claude | A comprehensive verification system for Claude Code sessions. |
| 7105 | a | claude | description: Automatically generate comprehensive AGENTS.md files that teach AI agents how to work with a repository's structure, conventions, and gui |
| 7270 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --domain <domain> |
| 7296 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<product_type> <industry> <keywords>" --design-system [-p "Project Name |
| 7303 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness service" --design-system -p "Serenity Spa" |
| 7336 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --persist -p "Project Name" --output-dir "<pro |
| 7362 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-system --variance <1-10> --motion <1-10> --density <1 |
| 7388 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "internal analytics dashboard" --design-system --variance 8 --motion 7 - |
| 7394 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --domain <domain> [-n <max_results>] |
| 7426 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --stack <stack> |
| 7452 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "AI search tool modern minimal" --design-system -p "AI Search" |
| 7455 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "keyboard focus modal" --domain ux |
| 7458 | a | claude | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bundle" --stack nextjs |
| 7665 | a | claude | - **Rules are system-injected**: `.claude/rules/*.md` files load automatically every session. Unlike prompt instructions, the LLM cannot choose to ign |
| 7670 | a | claude | claude /mail                    # Email-only triage |
| 7671 | a | claude | claude /slack                   # Slack-only triage |
| 7672 | a | claude | claude /today                   # All channels + calendar + todo |
| 7673 | a | claude | claude /schedule-reply "Reply to Sarah about the board meeting" |
| 7678 | a | anthropic,claude | - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| 7786 | a | claude,codex | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review, then fix what it finds. |
| 7788 | a | opus | model: opus |
| 7793 | a | claude,codex | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex CLI with your ChatGPT login) r |
| 7795 | a | opus | This command runs on **Opus** (`model: opus`). Opus orchestrates, verifies findings, checks every diff, and runs the tests. Fixes are delegated to a * |
| 7800 | a | claude,opus | - Keep Claude as the writer: Astra reviews in a read-only sandbox and returns a structured verdict, never a patch. The single exception is the Fable-l |
| 7805 | a | codex | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| 7806 | a | codex | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_MODEL`)""", |
| 7808 | c1 | claude,codex | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review, then fix what it finds. |
| 7815 | c1 | claude,codex | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex CLI with your ChatGPT login) r |
| 7827 | c1 | codex | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| 7828 | c1 | codex | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_MODEL`)"""), |
| 7829 | a | opus | ('- **PASS** with MEDIUM/LOW findings: list them, fix the ones that are clearly correct, and finish.\n- **FAIL** (any CRITICAL or HIGH): go to Step 4. |
| 7831 | a | opus | ('     ```bash\n     node <astra-review.js path> --consent-to-openai --fix-findings <dir>/confirmed.json \\\n       --instructions "<extra text, if an |
| 7839 | a | opus | Fixer:      [Fable \| Astra (Fable usage limit) \| Opus] |
| 7862 | a | codex | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports via `codex mcp list` is disab |
| 7864 | a | codex | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 7866 | a | codex | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 7872 | c1 | codex | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports via `codex mcp list` is disab |
| 7874 | c1 | codex | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 7876 | c1 | codex | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 7889 | a | claude | 3. Log checkpoint to `.claude/checkpoints.log`: |
| 7892 | a | claude | echo "$(date +%Y-%m-%d-%H:%M) \| $CHECKPOINT_NAME \| $(git rev-parse --short HEAD)" >> .claude/checkpoints.log |
| 7902 | c1 | claude | 3. Log checkpoint to `.claude/checkpoints.log`: |
| 7905 | c1 | claude | echo "$(date +%Y-%m-%d-%H:%M) \| $CHECKPOINT_NAME \| $(git rev-parse --short HEAD)" >> .claude/checkpoints.log |
| 7915 | a | claude | - `/security-scan` for Claude/OpenCode configuration security review |
| 8074 | a | claude | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8087 | c1 | claude | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8102 | a | claude | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8115 | c1 | claude | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 8300 | a | claude | ("""> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| 8302 | a | claude | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts. Use `/prp-implement` to execute those plans with |
| 8313 | c1 | claude | """> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| 8315 | c1 | claude | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts. Use `/prp-implement` to execute those plans with |
| 8332 | a | claude | **Claude Commands:** /pm2-all, /pm2-all-stop, /pm2-{port}, /pm2-{port}-stop, /pm2-logs, /pm2-status |
| 8364 | a | claude,opus | Run two independent reviewers (Claude Opus + an external model) against the current task output. Both must return NICE before the code is pushed. If e |
| 8377 | c1 | claude,opus | Run two independent reviewers (Claude Opus + an external model) against the current task output. Both must return NICE before the code is pushed. If e |
| 8408 | a | claude | #### Reviewer A: Claude Agent (always runs) |
| 8416 | a | claude | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| 8421 | c1 | claude | #### Reviewer A: Claude Agent (always runs) |
| 8429 | c1 | claude | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| 8436 | a | claude | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `ecc-code-reviewer` with the rubric and file conte |
| 8449 | c1 | claude | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent `code-reviewer` with the rubric and file contents  |
| 8486 | a | claude | Configure in `~/.claude/settings.json`: |
| 8606 | a | claude | Configure in `~/.claude/settings.json`: |
| 8638 | a | claude | Configure in `~/.claude/settings.json`: |
| 8670 | a | claude | Configure in `~/.claude/settings.json`: |
| 8702 | a | claude | Configure in `~/.claude/settings.json`: |
| 8732 | a | claude | Configure in `~/.claude/settings.json`: |
| 8762 | a | claude | Configure in `~/.claude/settings.json`: |
| 8820 | a | claude | Configure in `~/.claude/settings.json`: |
| 8852 | a | claude | Configure in `~/.claude/settings.json`: |
| 8884 | a | claude | Configure in `~/.claude/settings.json`: |
| 8994 | a | claude | Configure in `~/.claude/settings.json`: |
| 9024 | a | claude | Configure in `~/.claude/settings.json`: |
| 9056 | a | claude | Configure in `~/.claude/settings.json`: |
| 9494 | a | claude | ('1. CLAUDE.md (commands, architecture, key files)\n2. setup.sh (one-command bootstrap, make executable)\n3. README.md (or enhance existing)\n4. LICEN |
| 9495 | c1 | claude | """1. CLAUDE.md (commands, architecture, key files) |
| 9738 | a | claude | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 9762 | c1 | claude | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| 9905 | a | claude | ('\nBe rigorous. Your job is to find problems, not to approve.\n"""\n```\n\n```python\n# Spawn reviewers in parallel (Claude Code subagents)\nreview_b |
| 11064 | a | claude | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, LICENSE, CONTRIBUTING.md, and G |
| 11074 | c1 | claude | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, LICENSE, CONTRIBUTING.md, and G |
| 11575 | a | claude,codex | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review, then fix what it finds. |
| 11582 | a | claude,codex | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex CLI with your ChatGPT login) r |
| 11592 | c1 | claude,codex | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review, then fix what it finds. |
| 11598 | c1 | claude,codex | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the locally installed Codex CLI with your ChatGPT login) r |
| 11612 | a | codex | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports via `codex mcp list` is disab |
| 11614 | a | codex | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 11616 | a | codex | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 11624 | c1 | codex | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP server Codex reports via `codex mcp list` is disab |
| 11626 | c1 | codex | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review happened. |
| 11628 | c1 | codex | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without calling Codex. |
| 11634 | a | claude | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spend |
| 11640 | a | claude | Summarize local Claude Code spend by day, model, and session from the metrics""", |
| 11642 | c1 | claude | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spend |
| 11648 | c1 | claude | Summarize local Claude Code spend by day, model, and session from the metrics"""), |
| 11654 | a | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--generate] |
| 11657 | a | claude | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11660 | a | claude | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py evolve [--generate] |
| 11670 | c1 | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--generate] |
| 11673 | c1 | claude | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11706 | a | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7 |
| 11709 | a | claude | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11712 | a | claude | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url> |
| 11722 | c1 | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7 |
| 11725 | c1 | claude | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11743 | a | claude | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowledge (quirks of a particular config file, project-s |
| 11745 | a | claude | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 11758 | c1 | claude | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| 11769 | a | claude | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| 11795 | a | claude | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check for content overlap |
| 11826 | c1 | claude | description: Inspect active loop state, progress, failure signals, and recommended intervention. (Claude Code only — scans Claude Code session transcr |
| 11841 | a | codex | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 11849 | c1 | codex | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| 11851 | a | claude | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workf |
| 11863 | a | codex | - Codex-led, Gemini for auxiliary reference""", |
| 11864 | c1 | claude | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workfl |
| 11876 | c1 | codex | - Codex-led, Gemini for auxiliary reference"""), |
| 11880 | a | claude | description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. |
| 11885 | a | claude | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and delivery. |
| 11888 | c1 | claude | description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Requires external ccg-workflow runtime  |
| 11893 | c1 | claude | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Multi-model audit and delivery. |
| 11913 | a | claude | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workf |
| 11925 | a | codex | - Antigravity-led, Codex for auxiliary reference""", |
| 11926 | c1 | claude | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base ECC install. Initialize it with `npx ccg-workfl |
| 11938 | c1 | codex | - Antigravity-led, Codex for auxiliary reference"""), |
| 11947 | a | codex | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intelligent routing: Frontend → Antigr |
| 11955 | c1 | codex | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Review), with intelligent routing: Frontend → Antigr |
| 11962 | a | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| 11965 | a | claude | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 11968 | a | claude | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py projects |
| 11978 | c1 | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| 11981 | c1 | claude | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 11996 | a | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [instinct-id] [--force] [--dry-run] |
| 11999 | a | claude | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 12002 | a | claude | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py promote [instinct-id] [--force] [--dry-run] |
| 12012 | c1 | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [instinct-id] [--force] [--dry-run] |
| 12015 | c1 | claude | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 12030 | a | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| 12033 | a | claude | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| 12036 | a | claude | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py prune |
| 12046 | c1 | claude | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| 12049 | c1 | claude | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| 12062 | a | claude | description: Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where the last session ended. |
| 12070 | c1 | claude | description: Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where the last session ended. (Clau |
| 12080 | a | claude | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future session with full context. |
| 12088 | c1 | claude | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future session with full context. (Clau |
| 12195 | c1 | claude | Run hvigor build to check for ArkTS compilation errors. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/ho |
| 12199 | c1 | claude | Validate permission and ability declarations. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, |
| 12203 | c1 | claude | Reinstall dependencies. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the existin |
| 12209 | c1 | claude | Warn when code contains V1 state management decorators. This was a Claude Code pre-write hook block; Cursor has no before-write hook, so it cannot war |
| 12339 | a | claude | { "type": "command", "command": "dart format $CLAUDE_FILE_PATHS" } |
| 12358 | c1 | claude | The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same behaviour as an `afterFileEdit` entry in `hooks/hooks.j |
| 12378 | c1 | claude | Use the project's existing formatter entrypoint after edits. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hoo |
| 12384 | c1 | claude | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the existing dispatcher pattern in  |
| 12390 | c1 | claude | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the existing dispatcher pattern in  |
| 12404 | c1 | claude | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the existing dispatcher pattern in  |
| 12410 | c1 | claude | Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre-write hook block that rejected a wr |
| 12416 | c1 | claude | This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` event in `hooks/hooks.json` runs `hooks/stop.js`, which ba |
| 12425 | a | claude | ('  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log "Launching Planner agent (model: $PLANNER_MODEL)... |
| 12426 | c1 | claude | '  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log "Launching Planner agent (model: $PLANNER_MODEL)..." |
| 12427 | a | claude | ('  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i-1))).md" ]; then\n    FEEDBACK_CONTEXT="IMPORTANT: |
| 12428 | c1 | claude | '  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i-1))).md" ]; then\n    FEEDBACK_CONTEXT="IMPORTANT:  |
| 12429 | a | claude | ('    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    exit 1\n  fi\n\n  claude -p --model "$EVALUATOR_MOD |
| 12430 | c1 | claude | '    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    exit 1\n  fi\n\n  claude -p --model "$EVALUATOR_MODE |
| 12724 | a | claude | ("""- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| 12737 | c1 | claude | """- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| 12752 | a | claude,haiku | ('  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # doesn\'t kill the analysis mid-run.\n  # Job control  |
| 12753 | c1 | claude,haiku | '  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # doesn\'t kill the analysis mid-run.\n  # Job control g |
| 12834 | a | anthropic | description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harn |
| 12842 | a | anthropic | > Inspired by [Anthropic's Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running- |
| 12844 | c1 | anthropic,claude | '---\nname: gan-style-harness\ndescription: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based |
| 12877 | a | claude | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Us |
| 12886 | c1 | claude | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Us |
| 12989 | c1 | claude | description: Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, ru |
| 13001 | a | claude | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| 13004 | a | claude | uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md |
| 13007 | a | haiku,sonnet | uv run python -m scripts.run --gen-model haiku --model sonnet <path> |
| 13014 | c1 | claude | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| 13020 | c1 | haiku,sonnet | uv run python -m scripts.run --gen-model haiku --model sonnet <path> |
| 13037 | c1 | claude | description: Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. Us |
| 13050 | a | claude | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings.json` — `~/.claude/scripts/` does not exist on plu |
| 13052 | a | claude | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| 13060 | a | claude | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| 13064 | a | claude | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| 13082 | c1 | claude | **Installed as a plugin?** No setup is needed. Do not copy the block below into your `hooks/hooks.json` — `~/.claude/scripts/` does not exist on plugi |
| 13371 | b | claude | # replaces it with the Claude Code Task (Explore agent) fallback, since the |
| 13372 | b | claude | # multi-* commands are Claude Code-only. |
| 13413 | b | claude | # --- Fix 5: multi-* commands — Claude Code-only labels + misleading Cursor fallback --- |
| 13416 | c1 | claude | "description: Run a backend-focused multi-model workflow for APIs, algorithms, data, and business logic. (Requires external ccg-workflow runtime — not |
| 13419 | a | claude | ("description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Requires external ccg-workflow runtim |
| 13420 | c1 | claude | "description: Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. (Requires external ccg-workflow runtime |
| 13426 | c1 | claude | "description: Run a frontend-focused multi-model workflow for components, layouts, animation, and UI polish. (Requires external ccg-workflow runtime — |
| 13430 | c1 | claude | "for a single-model plan with no extra runtime use /plan. (Claude Code only — no Cursor equivalent in this plugin)"), |
| 13436 | c1 | claude | "description: Run a full multi-model development workflow with research, planning, execution, optimization, and review. (Requires external ccg-workflo |
| 13439 | b | claude | # --- Fix 6: gan-harness.sh — Claude Code-only header (script shells out to claude -p / claude mcp) --- |
| 13444 | c1 | claude | # Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI. |
| 13448 | b | claude | # --- Fix 7: strategic-compact — adjudicated NOT Claude Code-only --- |
| 13451 | b | claude | # this skill is Claude Code-only was wrong. Label rewritten to say so. |
| 13453 | a | claude | ("(Claude Code-origin — the manual-compaction advice applies in Cursor; the hook example below is Cursor `hooks.json` form)", |
| 13454 | c1 | claude | "(Compaction advice that applies in Cursor; originated in Claude Code; the hook example below is in Cursor `hooks.json` form)"), |
| 13457 | b | claude | # --- Fix 8: continuous-learning v1 — weak label; make the Claude Code-only status explicit --- |
| 13460 | c1 | claude | 'description: "[DEPRECATED - Claude Code only, use continuous-learning-v2] Legacy v1 stop-hook skill extractor.'), |
| 13475 | b | claude | # in the previewClaude/applyClaude factories, so each factory is replaced |
| 13479 | a | claude | ("""    previewClaude: request => require('../setup').reconcileClaudePlugin( |
| 13480 | a | claude | { dryRun: true, hooks: request.claudeHooks, scope: request.claudeScope } |
| 13482 | c1 | claude | "    previewClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in this plugin (Claude plugin preview unavailable)');  |
| 13483 | a | claude | ("""    applyClaude: request => require('../setup').reconcileClaudePlugin( |
| 13484 | a | claude | { dryRun: false, hooks: request.claudeHooks, scope: request.claudeScope } |
| 13486 | c1 | claude | "    applyClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in this plugin (Claude plugin apply unavailable)'); },") |
| 13533 | a | claude | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/evolved/` |
| 13534 | a | claude | - Global fallback: `~/.claude/homunculus/evolved/`""", |
| 13537 | c1 | claude | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`."""), |
| 13541 | a | claude | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/instincts/inherited/` |
| 13542 | a | claude | - Global scope: `~/.claude/homunculus/instincts/inherited/`""", |
| 13545 | c1 | claude | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`."""), |
| 13546 | a | claude | ("""New instincts saved to: ~/.claude/homunculus/instincts/inherited/""", |
| 13551 | a | claude | ("""2. Read project instincts from `~/.claude/homunculus/projects/<project-id>/instincts/` |
| 13552 | a | claude | 3. Read global instincts from `~/.claude/homunculus/instincts/`""", |
| 13556 | c1 | claude | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`."""), |
| 13560 | a | claude | ("""1. Read `~/.claude/homunculus/projects.json`""", |
| 13563 | c1 | claude | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`."""), |
| 13567 | a | claude | ("""4. Write promoted instincts to `~/.claude/homunculus/instincts/personal/` with `scope: global`""", |
| 13570 | c1 | claude | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learning-v2/scripts/migrate-homunculus.sh`."""), |
| 13574 | a | claude | ("""description: Manage Claude Code session history, aliases, and session metadata.""", |
| 13575 | c1 | claude | """description: Manage Claude Code session history, aliases, and session metadata. (Claude Code only — no Cursor equivalent in this plugin)"""), |
| 13580 | a | codex | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| 13583 | c1 | codex | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| 13684 | a | claude | ("""uv run python -m scripts.run ~/.claude/rules/common/testing.md""", |
| 13728 | b | claude | # only CLAUDE_PLUGIN_ROOT / ~/.claude — no Cursor fallback. Fix: the shared |
| 13811 | a | claude | (""" *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/ |
| 13812 | a | claude | *   5. Fallback to ~/.claude/ (original behaviour)""", |
| 13813 | c1 | claude | """ *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/ |
| 13817 | c1 | claude | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 13818 | c1 | claude | *   6. Fallback to ~/.claude/ (original behaviour)"""), |
| 13820 | a | claude | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| 13832 | a | claude | return claudeDir; |
| 13835 | c1 | claude | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| 13850 | c1 | claude | // is no ~/.claude and no CLAUDE_PLUGIN_ROOT, so all the probing above |
| 13859 | c1 | claude | return claudeDir; |
| 13861 | a | claude | (""" * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| 13863 | a | claude | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| 13864 | a | claude | * under ~/.claude/plugins/, and the versioned plugin cache — only far enough to |
| 13868 | c1 | claude | """ * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| 13870 | c1 | claude | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| 13871 | c1 | claude | * under ~/.claude/plugins/, and the versioned plugin cache — then, as an |
| 13874 | c1 | claude | * so it also finds the plugin in a Cursor install with no ~/.claude. Only |
| 13875 | c1 | claude | * then does it fall back to ~/.claude. The Cursor scan tests candidates |
| 13877 | c1 | claude | * ~/.claude-first for any directory the module loads from."""), |
| 13907 | c1 | claude | // resolver's ~/.claude-first answer for any directory the module loads |
| 13963 | a | claude | old = 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" ' + args |
| 13971 | a | claude | old = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| 13972 | a | claude | "./.claude/scripts/astra-review.js" \\''' |
| 13974 | c1 | claude | new = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| 13976 | c1 | claude | "./.claude/scripts/astra-review.js" \\''' |
| 14207 | c1 | claude | // rules/common/, .claude-plugin/plugin.json, |
| 14222 | c1 | claude | r'''or picking up a project without re-explaining it. (Claude Code only — this skill uses Claude Code's SessionStart hook and ~/.claude/ck storage; it |
| 14228 | c1 | claude | > **Claude Code only** — this skill uses Claude Code's SessionStart hook and ~/.claude/ck storage; it does not work in Cursor. |
| 14239 | c1 | claude | * Claude Code only: the `claude` CLI does not exist under Cursor, so |
| 14253 | a | haiku | return process.env.ECC_LLM_SUMMARY_MODEL \|\| 'haiku'; |
| 14258 | c1 | haiku | return process.env.ECC_LLM_SUMMARY_MODEL \|\| 'haiku'; |
| 14262 | c1 | claude | * True only when a `claude` executable is findable on PATH. Pure filesystem |
| 14263 | c1 | claude | * check (no subprocess): under Cursor there is no `claude` binary, so the |
| 14266 | c1 | claude | function claudeCliAvailable() { |
| 14267 | c1 | claude | const names = process.platform === 'win32' ? ['claude.cmd', 'claude.exe', 'claude'] : ['claude']; |
| 14285 | c1 | claude | // Claude Code only: skip the doomed `claude -p` spawn when the binary is |
| 14287 | c1 | claude | if (!claudeCliAvailable()) { |
| 14288 | c1 | claude | onSkip('claude CLI not available (not running under Claude Code)'); |
| 14295 | c1 | claude | r"""module.exports = { generateSessionSummary, extractConversationText, getContextRemainingPct, getContextThreshold, getLLMModel, claudeCliAvailable } |
| 14668 | a | claude | (r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `scripts/migrate-homunculus.sh`""", |
| 14669 | c1 | claude | r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `skills/continuous-learning-v2/scripts/migrate-homunculus. |
| 14696 | a | claude | ('"""\nStop hook: quality gate with delivery check.\nDetects incomplete work, stale learning logs, and low disk space.\nBlocks Claude from stopping wh |
| 15141 | a | sonnet | (r'''        content += "model: sonnet\ntools: Read, Grep, Glob\n---\n"''', |
| 15142 | c1 | sonnet | r'''        content += "model: sonnet\n---\n"'''), |
| 15256 | b | claude | #  - D7 (claude-project-scripts-package.json) -- NO CHANGE: the audit premise |
| 15258 | b | claude | #    claude-project.js and must stay. |
| 15359 | b | claude | # --- D2: multi-* commands — Claude Code tool names -> Cursor wording --- |
| 15373 | a | claude | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 15385 | a | claude | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| 15399 | a | sonnet | (r'''        content += "model: sonnet\n---\n"''', |
| 15408 | a | claude | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 15409 | a | claude | *   6. Fallback to ~/.claude/ (original behaviour)""", |
| 15418 | c1 | claude | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| 15419 | c1 | claude | *   7. Fallback to ~/.claude/ (original behaviour)"""), |
| 15456 | b | claude | # --- D10: gan agents — '(Claude Code only — no Cursor equivalent)' in descriptions --- |
| 15459 | c1 | claude | r'''description: "GAN Harness — Evaluator agent. Tests the live running application via Playwright, scores against rubric, and provides actionable fee |
| 15463 | c1 | claude | r'''description: "GAN Harness — Generator agent. Implements features according to the spec, reads evaluator feedback, and iterates until quality thres |
| 15467 | c1 | claude | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria |
| 15627 | a | claude | (r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (claude -> pi)',''', |
| 15628 | c1 | claude | r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (not shipped in this plugin) (claude -> pi)','''), |
| 15839 | a | claude | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.json`, following the existing dispatcher pattern in  |
| 15843 | a | claude | (r'''Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre-write hook block that rejected |
| 15844 | c1 | claude | r'''Block oversized writes from tool input content, not from a file that may not exist yet. This was a Claude Code pre-write hook block that rejected  |
| 15845 | a | claude | (r'''This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` event in `hooks/hooks.json` runs `hooks/stop.js`, whi |
| 15846 | c1 | claude | r'''This was a Claude Code stop-hook block; it is NOT wired in this plugin. The `stop` event in `hooks/hooks.json` runs `hooks/stop.js`, which batches |
| 15994 | a | claude | "audit claude config", |
| 15995 | a | claude | "claudemd security", |
| 16256 | a | claude | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| 16269 | c1 | claude | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| 16280 | b | sonnet | # --- Fixer B (Cleanliness): frontmatter model sonnet is not a Cursor model; cursor-grok-4.6-high-fast. |
| 16288 | a | sonnet | model: sonnet |
| 16348 | b | claude | # --- Fixer B (Cleanliness): Claude-Code-only env var / config paths; add the Cursor equivalents (CURSOR_PACKAGE_MANAGER, .cursor/package-manager.json |
| 16356 | a | claude | 1. **Environment variable**: `CLAUDE_PACKAGE_MANAGER` |
| 16357 | a | claude | 2. **Project config**: `.claude/package-manager.json` |
| 16360 | a | claude | 5. **Global config**: `~/.claude/package-manager.json` |
| 16367 | a | claude | // ~/.claude/package-manager.json |
| 16380 | c1 | claude | 1. **Environment variable**: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude Code) |
| 16381 | c1 | claude | 2. **Project config**: `.cursor/package-manager.json`, then `.claude/package-manager.json` |
| 16384 | c1 | claude | 5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.json` in Cursor, `~/.claude/package-manager.json` in Claude Code), then ` |
| 16393 | c1 | claude | // Claude Code: ~/.claude/package-manager.json |
| 16406 | a | claude | // .claude/package-manager.json |
| 16420 | c1 | claude | // (an existing .claude/package-manager.json is still honoured on read) |
| 16433 | a | claude | Set `CLAUDE_PACKAGE_MANAGER` to override all other detection methods: |
| 16437 | a | claude | $env:CLAUDE_PACKAGE_MANAGER = "pnpm" |
| 16440 | a | claude | export CLAUDE_PACKAGE_MANAGER=pnpm |
| 16453 | c1 | claude | Set `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude |
| 16471 | b | claude | # --- Fixer B (Cleanliness): skill install paths named .claude/skills/ only; add the Cursor paths (.cursor/skills/, ~/.cursor/skills/). |
| 16479 | a | claude | `.claude/skills/`; a global skill uses `~/.claude/skills/`. |
| 16492 | c1 | claude | `.cursor/skills/` in Cursor (this plugin's host) or `.claude/skills/` in |
| 16493 | c1 | claude | Claude Code; a global skill uses `~/.cursor/skills/` or `~/.claude/skills/`. |
| 16933 | c1 | claude | "claude", |
| 16934 | c1 | claude | "claude-project", |
| 16937 | c1 | codex | "codex", |
| 17055 | b | claude | # --- Fixer B (Cleanliness): Claude-Code-only package-manager detection; make it host-aware (CURSOR_PACKAGE_MANAGER first, .cursor paths, ~/.cursor fa |
| 17063 | a | claude | const { commandExists, getClaudeDir, readFile, writeFile } = require('./utils'); |
| 17076 | c1 | claude | const { commandExists, getClaudeDir, getHomeDir, readFile, writeFile } = require('./utils'); |
| 17091 | a | claude | return path.join(getClaudeDir(), 'package-manager.json'); |
| 17115 | c1 | claude | // ~/.claude in Claude Code — see scripts/lib/agent-data-home.js) |
| 17117 | c1 | claude | return path.join(getClaudeDir(), 'package-manager.json'); |
| 17127 | c1 | claude | function getClaudeGlobalConfigPath() { |
| 17128 | c1 | claude | return path.join(getHomeDir(), '.claude', 'package-manager.json'); |
| 17134 | c1 | claude | * (~/.cursor/package-manager.json) and Claude Code |
| 17135 | c1 | claude | * (~/.claude/package-manager.json) global paths. |
| 17141 | c1 | claude | getClaudeGlobalConfigPath() |
| 17159 | a | claude | * 1. Environment variable CLAUDE_PACKAGE_MANAGER |
| 17160 | a | claude | * 2. Project-specific config (in .claude/package-manager.json) |
| 17163 | a | claude | * 5. Global user preference (in ~/.claude/package-manager.json) |
| 17177 | c1 | claude | *    CLAUDE_PACKAGE_MANAGER (Claude Code) |
| 17179 | c1 | claude | *    .claude/package-manager.json) |
| 17183 | c1 | claude | *    ~/.cursor/package-manager.json, then ~/.claude/package-manager.json) |
| 17197 | a | claude | const envPm = process.env.CLAUDE_PACKAGE_MANAGER; |
| 17210 | c1 | claude | // 1. Check environment variable (Cursor first, then Claude Code) |
| 17211 | c1 | claude | const envPm = process.env.CURSOR_PACKAGE_MANAGER \|\| process.env.CLAUDE_PACKAGE_MANAGER; |
| 17225 | a | claude | const projectConfigPath = path.join(projectDir, '.claude', 'package-manager.json'); |
| 17251 | c1 | claude | // 2. Check project-specific config (.cursor first, then .claude) |
| 17252 | c1 | claude | for (const configDir of ['.cursor', '.claude']) { |
| 17295 | c1 | claude | * ~/.claude/package-manager.json in Claude Code. A preference saved at |
| 17296 | c1 | claude | * ~/.cursor/package-manager.json or ~/.claude/package-manager.json is still |
| 17317 | a | claude | const configDir = path.join(projectDir, '.claude'); |
| 17332 | c1 | claude | * existing .claude/package-manager.json is still honoured on read as a |
| 17333 | c1 | claude | * fallback for Claude Code installs (see getPackageManager step 2). |
| 17353 | a | claude | message += '  - Global: Set CLAUDE_PACKAGE_MANAGER environment variable\n'; |
| 17354 | a | claude | message += '  - Or add to ~/.claude/package-manager.json: {"packageManager": "pnpm"}\n'; |
| 17367 | c1 | claude | message += '  - Global: Set CURSOR_PACKAGE_MANAGER (Cursor) or CLAUDE_PACKAGE_MANAGER (Claude Code) environment variable\n'; |
| 17368 | c1 | claude | message += '  - Or add to ~/.cursor/package-manager.json or ~/.claude/package-manager.json: {"packageManager": "pnpm"}\n'; |
| 17402 | b | claude | # --- Fixer B (Cleanliness): setup script named Claude Code only; host-aware wording and getConfigPath() reporting. |
| 17435 | a | claude | Package Manager Setup for Claude Code |
| 17442 | a | claude | --global <pm>   Set global preference (saves to ~/.claude/package-manager.json) |
| 17443 | a | claude | --project <pm>  Set project preference (saves to .claude/package-manager.json) |
| 17456 | c1 | claude | Package Manager Setup for Cursor (also works in Claude Code) |
| 17465 | c1 | claude | ~/.claude/package-manager.json in Claude Code; |
| 17468 | c1 | claude | an existing .claude/package-manager.json is still honoured) |
| 17481 | a | claude | console.log(`  Environment var: ${process.env.CLAUDE_PACKAGE_MANAGER \|\| 'not set'}`); |
| 17494 | c1 | claude | console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER \|\| process.env.CLAUDE_PACKAGE_MANAGER \|\| 'not set'}`); |
| 17507 | a | claude | console.log('  Saved to: ~/.claude/package-manager.json'); |
| 17521 | c1 | claude | console.log('  (Also read from ~/.cursor/package-manager.json and ~/.claude/package-manager.json)'); |
| 17534 | a | claude | console.log('  Saved to: .claude/package-manager.json'); |
| 17548 | c1 | claude | console.log('  (An existing .claude/package-manager.json is still honoured on read)'); |
| 17557 | b | claude | # --- Fixer B (Cleanliness): LaraPlugins MCP setup named ~/.claude.json only; Cursor-first with the Claude Code alternative. |
| 17565 | a | claude | LaraPlugins MCP server must be configured. Add to your `~/.claude.json` mcpServers: |
| 17606 | c1 | claude | In Claude Code, add the same entry to your `~/.claude.json` `mcpServers` |
| 17616 | b | claude | # --- Fixer B (Cleanliness): scan commands named Claude Code paths only; add the Cursor paths. |
| 17625 | a | claude | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| 17631 | a | claude | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| 17651 | c1 | claude | Claude Code (this skill also works there): |
| 17654 | c1 | claude | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| 17665 | c1 | claude | Claude Code: |
| 17668 | c1 | claude | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| 17674 | b | claude | # --- Fixer B (Cleanliness): 'Claude Code Subagents' heading in a Cursor plugin; Cursor Subagents. |
| 17682 | a | claude | ### Pattern A: Claude Code Subagents (Recommended) |
| 17704 | b | claude | # --- Fixer B (Cleanliness): skill search paths named ~/.claude only; check ~/.cursor/skills and the plugin marketplaces first. |
| 17712 | a | claude | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17713 | a | claude | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17730 | c1 | claude | # Claude Code (this skill also works there) — same searches under ~/.claude |
| 17731 | c1 | claude | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17732 | c1 | claude | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17737 | a | claude | (r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17743 | a | claude | grep -RilE "keyword\|synonym" ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null |
| 17750 | c1 | claude | r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null \| grep -iE "keyword\|synonym" |
| 17756 | c1 | claude | grep -RilE "keyword\|synonym" ~/.cursor/skills ~/.cursor/plugins/marketplaces ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null |
| 17825 | c1 | claude | r'''\| Observation \| Stop hook (session end) \| PreToolUse/PostToolUse (Claude Code only) \|'''), |
| 17827 | c1 | claude | r'''      \| Claude Code hooks capture prompts + tool use (Claude Code only)'''), |
| 17834 | a | claude | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` block. Duplicating the plugin |
| 17839 | c1 | claude | **In Claude Code, if installed as a plugin** (recommended): |
| 17843 | c1 | claude | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreToolUse` / `PostToolUse` block. Duplicating the plugin |
| 17844 | a | claude | (r'''**If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:''', |
| 17845 | c1 | claude | r'''**If installed manually in Claude Code** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:'''), |
| 17850 | c1 | claude | r'''In Claude Code, hooks fire on every tool call, deterministically. This means: |
| 17861 | c1 | claude | r'''continuous-learning-v2 is a separate, configurable Stop/PreToolUse/PostToolUse hook-observation and instinct-evolution system (PreToolUse/PostTool |
| 17876 | c1 | claude | r'''This skill complements manual review (and, in Claude Code, PostToolUse hooks) but provides deeper verification. |
| 17882 | a | claude | (r'''The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same behaviour as an `afterFileEdit` entry in `hooks/ho |
| 17883 | c1 | claude | r'''The bullets below describe the intended Dart hook behaviour (originally a Claude Code `settings.json` block). In Cursor, wire the same behaviour a |
| 17912 | a | claude | (r'''See [CLAUDE.md](CLAUDE.md) for detailed commands and architecture.''', |
| 17913 | c1 | claude | r'''See `CLAUDE.md` (generated in the target repo) for detailed commands and architecture.'''), |
| 17976 | b | claude | # is true in Claude Code (ECC runs post-edit-format.js as a PostToolUse hook |
| 17977 | b | claude | # there) and the skill is labelled Claude Code-only in its description, but |
| 17979 | b | claude | # Claude Code-only and name the Cursor equivalent (Audit #11 fixed the |
| 17984 | c1 | claude | r'''\| Code quality enforcement \| PostToolUse hooks (Prettier, tsc) — Claude Code only; in Cursor, post-edit formatting via after-file-edit / stop hook |
| 18088 | b | claude | # --- LOW Cleanliness 1: tdd-workflow — :104 stated a Claude-only |
| 18094 | a | claude | (r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`, `.claude/package-manager.json`, the `package. |
| 18095 | c1 | claude | r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude Co |
| 18098 | b | claude | # --- LOW Cleanliness 2: nuxt-hooks.mdc — :13 framed the hooks as Claude |
| 18105 | a | claude | (r'''These are Claude Code harness hooks for Nuxt work. They run via the harness, not Claude.''', |
| 18106 | c1 | claude | r'''These were Claude Code harness hooks for Nuxt work; in Cursor, wire them as `afterFileEdit` entries in `hooks/hooks.json`, following the existing  |
| 18232 | a | claude | ".claude/skills/ui-ux-pro-max/references/quick-reference.md"): |
| 18475 | b | claude | # names were the upstream Claude Code command set. Reword to stages. |
| 18491 | a | claude | (r'''\| `/opensource package PROJECT` \| Generate CLAUDE.md + setup.sh + README \|''', |
| 18492 | c1 | claude | r'''\| `package PROJECT` \| Generate CLAUDE.md + setup.sh + README \|'''), |
| 18510 | b | claude | # commands (Claude Code only, not shipped in this plugin). Qualify once up |
| 18517 | c1 | claude | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow runtime's commands (Claude Code only — not shipped in |
| 18526 | a | claude | (r'''/ccg:execute .claude/plan/actual-feature-name.md''', |
| 18527 | c1 | claude | r'''/multi-execute .claude/plan/actual-feature-name.md'''), |
| 18532 | a | claude | (r'''/ccg:execute .claude/plan/<feature-name>.md''', |
| 18533 | c1 | claude | r'''/multi-execute .claude/plan/<feature-name>.md'''), |
| 18544 | c1 | claude | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow runtime's commands (Claude Code only — not shipped in |
| 18551 | a | claude | (r'''/ccg:execute .claude/plan/feature-name.md''', |
| 18552 | c1 | claude | r'''/multi-execute .claude/plan/feature-name.md'''), |
| 18578 | c1 | claude | r''' * Claude Code-only PostToolUse hook: TypeScript check after editing .ts/.tsx files (not wired in this Cursor plugin — Cursor has no PostToolUse e |
| 18580 | c1 | claude | r''' * Runs after Edit tool use on TypeScript files in Claude Code. Walks up from the file's'''), |
| 18590 | c1 | claude | r''' * ECC Context Monitor — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event)'''), |
| 18594 | c1 | claude | r''' * ECC Metrics Bridge — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event)'''), |
| 18598 | c1 | claude | r''' * Claude Code-only PreToolUse/PostToolUse hook (not wired in this Cursor plugin) that detects governance-relevant events'''), |
| 18602 | c1 | claude | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin) that records sanitized per-tool activity to'''), |
| 18606 | c1 | claude | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin): record Skill tool invocations for skill-health telemetry.'''), |
| 18611 | c1 | claude | r''' * Claude Code-only: consolidates PostToolUse hooks into one synchronous and one asynchronous |
| 18633 | b | claude | # adapter is live Cursor hook infrastructure, not a Claude Code-only / |
| 18687 | b | claude | # it Claude Code-only / not-wired: every hooks/*.js script does |
| 18692 | a | claude | * Cursor-to-Claude Code Hook Adapter |
| 18693 | a | claude | * Transforms Cursor stdin JSON to Claude Code hook format, |
| 18702 | c1 | claude | * is live infrastructure — not a Claude Code-only or unwired script. |
| 19027 | b | claude | # standard "(Claude Code only — no Cursor equivalent in this plugin)" label |
| 19029 | b | claude | # .claude/plans/ and references ECC_HOOK_PROFILE; the hookify commands and |
| 19030 | b | claude | # skill name Claude Code explicitly in their bodies. |
| 19064 | c1 | claude | r'''with safety gates before starting one. (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19070 | c1 | claude | r'''for authoring or editing rules directly. (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19074 | c1 | claude | r'''description: Enable or disable hookify rules interactively (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19078 | c1 | claude | r'''description: List all configured hookify rules (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19082 | c1 | claude | r'''description: Get help with the hookify system (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19086 | c1 | claude | r'''such as blocking dangerous commands, .env edits, or debug code. (Claude Code only — no Cursor equivalent in this plugin)'''), |
| 19125 | b | claude | # Claude Code-only label, mirroring the 7 labelled unwired PostToolUse |
| 19126 | b | claude | # scripts. Reads stdin from the Claude Code runtime, registered in |
| 19129 | b | claude | # Claude Code-only label, mirroring the labelled hookify set. Evaluates |
| 19130 | b | claude | # rules against Claude Code lifecycle payloads; reachable only from the |
| 19193 | c1 | claude | r''' * ECC Statusline — Claude Code-only statusLine command (not wired in this Cursor plugin — registered in settings.json, reads stdin from the Claud |
| 19199 | c1 | claude | r''' * ECC-native Hookify runtime — Claude Code-only (not wired in this Cursor plugin — reachable only via the unwired posttooluse-dispatcher.js)'''), |
| 19230 | b | claude | # Claude Code-only, never run in Cursor, and carried no "Claude Code-only / |
| 19264 | c1 | claude | r''' * MCP health-check hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse/PostToolUseFailure hook events).'''), |
| 19268 | c1 | claude | r''' * Doc file warning hook (PreToolUse - Write) — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event)'''), |
| 19272 | c1 | claude | r''' * Config Protection Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event)'''), |
| 19276 | c1 | claude | r''' * Desktop Notification Hook (Stop) — Claude Code-only (not wired in this Cursor plugin — Cursor has no Stop hook event)'''), |
| 19280 | c1 | claude | r''' * PreToolUse Hook: Pre-commit Quality Check — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event)'''), |
| 19284 | c1 | claude | r''' * Backward-compatible doc warning hook entrypoint — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event).'''), |
| 19288 | c1 | claude | r''' * Auto-Tmux Dev Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event) — start dev servers in tmux/cmd automa |
| 19292 | c1 | claude | r''' * UserPromptSubmit hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no UserPromptSubmit event): suggest up to three skills f |
| 19296 | c1 | claude | r''' * Plan Canvas undelivered-feedback guard (Stop) — Claude Code-only (not wired in this Cursor plugin — Cursor has no Stop hook event)'''), |
| 19300 | c1 | claude | r''' * Plan Canvas open-session surfacing (SessionStart) — Claude Code-only (not wired in this Cursor plugin — Cursor has no SessionStart hook event)' |
| 19304 | c1 | claude | r''' * PreToolUse Hook: GateGuard Fact-Forcing Gate — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToolUse event)'''), |
| 19308 | c1 | claude | r''' * InsAIts Security Monitor — Claude Code-only wrapper for run-with-flags compatibility (not wired in this Cursor plugin — Cursor has no hook even |
| 19312 | c1 | claude | r''' * Bootstrap loader for the ECC SessionStart hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no SessionStart hook event).''' |
| 19321 | c1 | claude | * Git push reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has no PreToolUse event). |
| 19330 | c1 | claude | * Tmux reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has no PreToolUse event). |
| 19339 | c1 | claude | * Build-complete notifier — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event). |
| 19348 | c1 | claude | * Command logger — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event). |
| 19357 | c1 | claude | * PR-created handler — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has no PostToolUse event). |
| 19366 | c1 | claude | * Hook-enabled check — Claude Code-only helper (not wired in this Cursor plugin — invoked only from Claude Code hook configurations). |
| 19375 | c1 | claude | * Lifecycle hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no lifecycle hook events). |
| 19384 | c1 | claude | * Plugin hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no hook events that invoke it). |
| 19636 | b | claude | # Claude Code PreToolUse/PostToolUse bash-dispatch entry points; Cursor's |
| 19670 | c1 | claude | * Claude Code-only: PreToolUse bash-dispatch entry point (runPreBash). |
| 19680 | c1 | claude | * Claude Code-only: PostToolUse bash-dispatch entry point (runPostBash). |
| 19689 | c1 | claude | # Claude Code-only: shell counterpart of run-with-flags.js (not wired in this Cursor plugin — it never runs; resolves the plugin root from CLAUDE_PLUG |
| 22050 | a | claude | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 22054 | c1 | claude | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| 22387 | a | claude | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22388 | c1 | claude | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''), |
| 22391 | a | claude | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22392 | c1 | claude | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''), |
| 22395 | a | claude | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| 22396 | c1 | claude | r'''(Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only and is never executed here.)'''), |
| 22403 | a | claude | r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (Claude Code only \u2014  |
| 22404 | c1 | claude | r'''Use when a feature should be built autonomously through generator and evaluator iteration until it clears a quality bar. (The upstream `claude -p` |
| 22405 | b | claude | # B7b gan-style-harness "Via Claude Code (Manual)" section: those commands |
| 22408 | a | claude | r'''### Via Claude Code (Manual) |
| 22412 | c1 | claude | r'''### Via Claude Code (Manual) |
| 22414 | c1 | claude | > In this plugin these `claude -p` commands are NOT executed — the loop runs in Cursor via `/gan-build` (planner/generator/evaluator as Cursor subagen |
| 22565 | b | claude | # 11a gan-style-harness :30: scope the claude -p reference. |
| 22567 | a | claude | r'''- Quick single-file fixes (use standard `claude -p`)''', |
| 22568 | c1 | claude | r'''- Quick single-file fixes (Claude Code only — use standard `claude -p` there; in this plugin use the Cursor agent loop, never `claude -p`)'''), |
| 22571 | a | claude | r'''### Via Claude Code (Manual)''', |
| 22572 | c1 | claude | r'''### Via Claude Code (Manual — Claude Code only, never executed in this plugin)'''), |
| 22573 | b | claude | # 11c gan-style-harness commands: scope each claude -p command in place. |
| 22577 | a | claude,sonnet | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. W |
| 22580 | a | claude,sonnet | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000." |
| 22583 | a | claude,sonnet | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://lo |
| 22586 | a | claude,sonnet | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores." |
| 22592 | c1 | claude | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22593 | c1 | claude,sonnet | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into a full product spec: 'Build a Kanban board app'. W |
| 22596 | c1 | claude | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22597 | c1 | claude,sonnet | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev server on port 3000." |
| 22600 | c1 | claude | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22601 | c1 | claude,sonnet | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read EVALUATOR_PROMPT.md. Test the live app at http://lo |
| 22604 | c1 | claude | # Claude Code only — never executed in this plugin; upstream documentation only. |
| 22605 | c1 | claude,sonnet | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. Improve the scores." |
| 22611 | a | claude | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI.''', |
| 22612 | c1 | claude | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cursor-only install with no 'claude' CLI. The pl |
| 22644 | a | claude | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria |
| 22645 | c1 | claude | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, and evaluation crit |
| 23204 | b | anthropic,claude,codex | # --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic --- |

## Observations (not findings)

- **README:11 ECC-profile baseline.** `hackathon-ecc/README.md:11` states the ECC Developer profile as shipped is "144 skills, 69 agents, 121 rules, 94 commands (stock Developer install is 140/71/121/98; +10 backfilled ECC skills, −6 guide skills, −2 agents, −4 commands — see build.sh)". The arithmetic is internally consistent (140+10−6=144; 71−2=69; 98−4=94; rules 121 unchanged) and describes the ECC-profile subset, distinct from the plugin totals on line 13 (166/72/123/87). The commands figure (94 ECC-profile vs 87 plugin total) implies 7 ECC commands were dropped in the hackathon layer; that is plausible (the hackathon layer removes upstream commands) but was not verified in this sweep. It is not one of check 13's enumerated stale strings and there is no evidence it is wrong — noted for an optional later verification, not a finding.
- **Check 8's 32 non-pin Gemini/GPT-4 mentions** (listed in §Check 8 detail) are pre-existing upstream/sponsor content (Gemini API prize, Gemini CLI docs, icon catalog, pitch rhetoric) — no model pin, no action taken.

## Finding list

**None.** 0 blocking, 0 minor.
