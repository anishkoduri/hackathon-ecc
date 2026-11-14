# Sweep #16 report — extended stale-check (fix program #16, hackathon-ecc)

Sweep run: Wed 2026-11-11 (evening CST). Scope: built tree `hackathon-ecc/` (except `node_modules`), staged sources `new-skills/` + `round2-skills/` + `~/workspace/cursor-skills/less-flat-ui/`, `LIVE_SMOKE_TEST.md`, shipped README `hackathon-ecc/README.md`, `.cursor-plugin/marketplace.json`. Out of scope per the task: `fix16/` working files, scratch dirs, audit backups. `build.sh` inventoried separately (check 12), not swept for a zero-hit verdict.

## State verified (not assumed)

- `build.sh`: **23,221 lines, md5 `5d6ec4674214d89af8dd84856c5db987`** — matches the stated state.
- Built-tree counts: **skills 166, agents 72, rules 123, commands 87**. Hooks: **15 hook scripts** in `hackathon-ecc/hooks/` (excluding `adapter.js`) + `hooks.json` with **15 event keys / 15 entries** — the '15 hooks' baseline holds (the `ls` count of 17 files in `hooks/` is 15 scripts + `adapter.js` + `hooks.json`).
- Pins in the built tree: `grok-4.7-high` **45 lines / 52 occurrences**; `cursor-grok-4.6-high-fast` **98 lines / 99 occurrences** — matches the coordinator-verified counts. Full scope: `grok-4.7-high` 61 lines / 71 occurrences; `cursor-grok-4.6-high-fast` 114 lines / 116 occurrences.

## Verdict: NOT CLEAN — 1 blocking, 4 minor

The **shipped tree is clean on every banned term** (`composer-2.5`, `claude`, `codex`, `anthropic`, `opus` all 0 in `hackathon-ecc/`, 0 in `LIVE_SMOKE_TEST.md`, 0 in `marketplace.json`, 0 in `less-flat-ui/`), and `Claude Code-only` labels are gone (0). The verdict is NOT CLEAN because of one live non-Grok model default in shipped code (blocking), stale terms still sitting in the staged sources the sweep explicitly covers, stale counts in two shipped/checked docs, stale model-name comments in shipped scripts, and a `build.sh` inventory whose non-OLD hits fall outside the acknowledged exception's letter (all verified scrubbed in the final tree — see F5 and the adjudication note).

## Finding list

### F1 — BLOCKING (check 6): live `sonnet` default in shipped `agent-compress.js`

- **Location:** `hackathon-ecc/scripts/lib/agent-compress.js:118` — `model: frontmatter.model || 'sonnet',` inside `loadAgent()`. Any agent file without a `model:` frontmatter field would be catalogued as `sonnet`.
- **Mitigation (why it cannot fire today):** all 72 built agent files carry a `model:` pin (verified: zero agent files lack one); the module is currently **unwired** (no `require` of `agent-compress` anywhere in the tree or `build.sh` — only the file itself mentions it); and `scripts/lib/agent-ir.js:28` strictly validates tiers (`VALID_MODELS = ['cursor-grok-4.6-high-fast', 'grok-4.7-high']`, throws otherwise), so the two loaders disagree about what is valid.
- **Fix:** change the fallback to `'cursor-grok-4.6-high-fast'` (or drop the default and let the missing-pin case fail loudly like `agent-ir.js` does).

### F2 — MINOR (checks 2/3/4): stale `claude` / `codex` / `anthropic` terms remain in the staged sources (59 unique lines, 15 files)

Zero in the built tree, the smoke test, the marketplace file, and `less-flat-ui/` — every one of these is **staged-source only**, and every built counterpart is already scrubbed by `fix16.py`. But the sweep's scope explicitly includes the staged sources, and the staged text has **diverged from the built output**: the next rebuild only stays clean because `fix16.py` re-applies the rewrite each time. Counts: `claude` 38 lines (36 `new-skills/` + 2 `round2-skills/`), `codex` 18 lines (16 + 2), `anthropic` 10 lines (all `new-skills/`); 59 unique (file,line) pairs across the three terms. Full list with classification is Appendix B; by kind:

- **Icon brand catalog (33 lines)** — `new-skills/design-taste-frontend/assets/icons/{index.json, demo/icons-credits.json, demo.html}` list Claude / Claude Code / Codex / Anthropic as logo entries alongside Gemini, OpenAI, Mistral, etc. (e.g. `index.json:781-783` `"id": "claude", "name": "Claude"`; `icons-credits.json:708-722` Claude Code + Claude entries with `markUrl: https://claude.com/product/claude-code`). Not model pins; the built copies have exactly these 4 entries stripped (built `index.json` has 927 `"id"` entries vs staged 931 — the 4 removed are claude, claude-code, codex, anthropic; Gemini/OpenAI ids remain).
- **Upstream provenance prose (4 lines)** — `design-taste-frontend/SKILL.md:415` 'This skill was written for Claude Code. … (the Claude Code `Stop` hook was removed…)'; `:419` '…Included in hackathon-ecc with only the Claude Code hook removed…'; `integration/SKILL.md:128` '(`claude-code-skills`)' repo name in an exclusion note; `feature-expansion/SKILL.md:205` '**claude-handoff** (`cliffordcollinsglobal/agent-skills`…)' attribution. The INVENTORY (§6, design-taste row) already flagged :415/:419 as 'need rewording' — the staged source was never reworded; only the built copy was rewritten (`hackathon-ecc/.../SKILL.md:416` now reads 'This skill was written for Cursor. … (the Cursor `Stop` hook was removed…)').
- **Multi-host hook docs + gate script (16 lines)** — `design-taste-frontend/references/gate.md:136,138-141,145,147,155,161,167,173` (Claude Code / `$CLAUDE_*` paths / `.claude/settings.json` hook wiring) and `references/hallmark/references/gates.md:243` ('a subagent in Claude Code'); `scripts/gate.mjs:11,71,111,112` (`--hook claude|codex|antigravity`, `const MODES = { claude: 'block', codex: 'block', antigravity: 'continue' }`). Functional multi-host code in the staged script; the built copy is Cursor-only (`MODES = { cursor: 'block' }`, `--hook takes cursor`).
- **Removal-note / tool-name prose (6 lines)** — `orchestrate/SKILL.md:32` ('…removed in fix #16 — they invoked external Codex/Gemini CLIs'; built copy says 'external model CLIs'); `round2-skills/mobile-ship/references/launch-marketing.md:7` ('Claude Motion (the code-built video artifact type)…'); `round2-skills/polish-pass/reference/capture.md:33` ('Claude in Chrome, ChatGPT in Chrome…'); `round2-skills/polish-pass/reference/impeccable-critique.md:38` ('the Codex permission question included'); `round2-skills/polish-pass/reference/impeccable-detector-rules.json:563` (`"id": "codex-grid-background"`); `design-taste-frontend/assets/layout/heroes.json:636` (`"from": "Anthropic, Stripe Press, Mercury, …"` — a design-credit line).

### F3 — MINOR (check 6): stale `Haiku` model mentions in shipped script comments (2 lines)

- `hackathon-ecc/skills/continuous-learning-v2/agents/start-observer.sh:5` — '# Starts the background observer agent … Uses Haiku model for cost efficiency.'
- `hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh:149` — '#   - ECC observing its own Haiku observer sessions (self-loop)'.
- Not pins (comments only) and the observer spawn itself is gone (`observer-loop.sh` has zero model references; the observer is disabled by default in config). But the comments still name the old model in shipped files. Fix: reword or drop the Haiku references.

### F4 — MINOR (check 11): stale counts in the shipped README and the smoke test (3 lines)

- `hackathon-ecc/README.md:13` — '169 skills, 72 agents, 123 rules, and 96 commands in total.' (skills should be **166**, commands **87**).
- `hackathon-ecc/README.md:40` — 'structured process — 169 skills, 72 agents, 96 commands, …' (same staleness).
- `LIVE_SMOKE_TEST.md:17` (step 1) — '(counts should read 168 skills, 72 agents, 123 rules, 96 commands).' (skills should be **166**, commands **87**; agents 72 and rules 123 are current). This step was already known-stale at '168 skills' before this round — it is still stale, and '96 commands' is stale too.
- The current counts appear **nowhere** in scope: '166 skills' 0 hits, '87 commands' 0 hits. No stale hook count anywhere ('15 hooks' is current per `hooks.json`). Source of the README staleness: the README heredoc baked into `build.sh:18337` and `:18364` (outside the sweep scope, noted here as the fix location).

### F5 — MINOR, process (check 12): 371 `build.sh` hits fall outside the acknowledged exception's letter — all verified scrubbed/deleted in the final tree

The acknowledged exception covers OLD-side match strings and their comments: **408 (a) + 53 (b) = 461 of 832 hits**. The remaining **371 hits are (c)-class**: 368 NEW-side patch text strings (c1), 1 heredoc file write (c2), 2 build-time source paths (c3). None of the 371 is a live model pin (zero `model:` lines among them; the 2 `opus` c1 hits are prose — 'Run two independent reviewers (Claude Opus + an external model)' at `build.sh:8377` and the '400k Opus 4.x' example at `:6925`). None survives into the final built tree: the tree greps are 0 for every banned term, and the mechanism is verified — `build.sh:23204-23210` runs `fix16/fix16.py` as the **last** build step (generic tree-wide scrub at `fix16.py:1160-1239` plus targeted edits and deletions); spot checks confirm the scrub in place (e.g. `build.sh:3523` NEW 'Default to `claude`…' → built `commands/project-init.md:42` 'Default to `cursor`.'; `:3940` 'Manage Claude Code session history' → built `commands/sessions.md:2` 'Manage Cursor session history'; `:18296` heredoc 'describes the Claude Code hooks format' → built `schemas/cursor-hooks.schema.json:50` 'describes the Cursor hooks format'; `:18702` 'not a Claude Code-only or unwired script' → built `hooks/adapter.js:8` 'not an unwired script'). Of the 368 c1 hits, **273 target files that ship** (scrubbed in place) and **95 target files that do not ship** (deleted by `fix16.py`, e.g. `commands/cost-report.md`, `commands/multi-*.md`, `scripts/lib/llm-summary.js` — verified absent from the tree; 0 c1 rows have no patch target (step-1/2 setup region).

**Adjudication note (for the coordinator):** check 12's exception, as written, covers OLD-side strings and their comments only, and says a 'reference that would land in the built tree' is a blocking finding. Read literally ('lands at any point mid-build'), the 273 shipping-target c1 hits + the 1 heredoc write would be blocking — but they land only transiently in STEP 3 and are deterministically removed by the final STEP 4 scrub, and the shipped tree is verified 0-hit. I have counted this as **one minor process finding** (dependence of final cleanliness on the last-step scrub) rather than 274 blocking findings, and the full inventory in Appendix A gives the exact lines if you want to re-call it. The one thing the exception's letter unambiguously does NOT cover, and which is a genuine fragility, is that a future `fix16.py` generic-pass miss would ship a stale term — the (c1) list is the watchlist for that.

## Per-check results

| # | Check | Hits | Result |
|---|---|---|---|
| 1 | `composer-2.5` anywhere in scope | **0** | PASS |
| 2 | `claude` (case-insensitive) | **38 lines** (0 built tree / 0 smoke test / 0 marketplace / 0 less-flat-ui; 36 `new-skills/` + 2 `round2-skills/`) | FAIL → F2 |
| 3 | `codex` (case-insensitive) | **18 lines** (0 built; 16 `new-skills/` + 2 `round2-skills/`) | FAIL → F2 |
| 4 | `anthropic` (case-insensitive) | **10 lines** (0 built; all `new-skills/`) | FAIL → F2 |
| 5 | `opus` as a model/vendor word | **0** (no hits at all in scope; a bare-substring check found nothing to disambiguate) | PASS |
| 6 | Non-Grok model pins (`model:` fields, pin tables, pin examples) | **1 live default** (`sonnet`, F1); 0 banned IDs as `model:` values | FAIL → F1 (plus F3) |
| 7 | `grok-4.7[` bracket hits | **0** | PASS |
| 8 | Bare `grok-4.6-high-fast` (not preceded by `cursor-`) | **0**; `cursor-grok-4.6-high-fast` is the form everywhere (98 lines/99 occ built tree; 114 lines/116 occ full scope) | PASS |
| 9 | Composer-feature distinction | **50 lines**, all PHP Composer / CSS `.composer` / prose / icon data; 0 model pins; 0 Cursor Composer UI feature mentions (1 borderline 'composer session' quoted below) | PASS (with note) |
| 10 | `LIVE_SMOKE_TEST.md` §14 | §14 exists, covers the 4.6 pin, step 7 names `grok-4.7-high`; no stale model name in the doc | PASS on models; step-1 stale counts → F4 |
| 11 | Stale counts | **3 stale lines** (README ×2, smoke test ×1); '166 skills'/'87 commands' 0× in scope; 72 agents / 123 rules / 15 hooks verified current | FAIL → F4 |
| 12 | `build.sh` exception inventory | **832 hits** inventoried: (a) 408, (b) 53, (c1) 368, (c2) 1, (c3) 2; 0 live pins; 0 survive in the final tree | INVENTORIED → F5 |
| 13 | 'Claude Code-only' labels gone | **0**; reworded labels spot-checked (5 quotes below) | PASS |

### Check 6 detail — every non-Grok model mention, and why it is or is not a pin

- **BAD — live pin (F1):** `hackathon-ecc/scripts/lib/agent-compress.js:118` — `model: frontmatter.model || 'sonnet',` (the only `model:` value in scope that is not a Grok slug).
- **All `model:` fields otherwise Grok:** 71× `model: cursor-grok-4.6-high-fast` (line 4 of agent files) + 5× `model: grok-4.7-high`; `agent-TEMPLATE.md` example pins are `cursor-grok-4.6-high-fast, grok-4.7-high`; pin tables are Grok (`rules/common-performance.mdc` Model Selection Strategy; `commands/model-route.md` routing heuristic); `schemas/agent.schema.json:35-36` enum is `["cursor-grok-4.6-high-fast", "grok-4.7-high"]` ('Grok model slugs only in v1'). No banned ID appears as a `model:` value (grep `model:\s*…(gemini|gpt-|sonnet|haiku|opus|composer|claude)` = 0). Other `model:`-looking lines are code passthroughs (`model: a.model`, `model: data.model?.display_name`, `model: cursorInput.model`, `model: frontmatter.model || …`) or non-LLM (`model: tts.model ?? 'speech-2.8-hd'`).
- **`sonnet` (1 line, the F1 line above) and `haiku` (2 lines, F3)** — nothing else.
- **`gemini` (31 lines, all verified non-pins):** brand-icon data (`design-taste-frontend/assets/icons/index.json` 4 + `demo/icons-credits.json` 4 + `demo.html` 1, each in staged and built copies); tool/CLI docs (`angular-developer/references/mcp.md:3,51,53` — 'Gemini CLI', '`.gemini/settings.json`'); hackathon prize logistics (`track-picker/SKILL.md:76` — 'the Gemini prize', 'a Gemini API project number', staged + built); integration trigger/API-key names (`integration/SKILL.md:17` 'using the Gemini API', `:65` '`GEMINI_API_KEY`', staged + built); a README badge (`readme-writer/references/badges.md:34` — shields.io Gemini badge); removal-note prose (`orchestrate/SKILL.md:32` staged only — 'external Codex/Gemini CLIs').
- **`gpt-` (4 lines, all verified non-pins):** advice prose (`hackathon-scope/SKILL.md:110` — 'The judges don't care that you used GPT-4.'; `hackathon-pitch/references/win-secrets.md:347` — '"We used GPT-4"' as the weak-version example) and a detector-rule id (`impeccable-detector-rules.json:545` — `"id": "gpt-thin-border-wide-shadow"`, staged + built).

### Check 9 detail — the 50 Composer lines (all classified, none a model pin)

- **PHP Composer CLI / files (27):** `rules/php-coding-style.mdc:3`, `php-hooks.mdc:3`, `php-patterns.mdc:3`, `php-security.mdc:3,18`, `php-testing.mdc:3` (`composer.json` globs; `composer audit`); `skills/laravel-verification/SKILL.md` ×12 (`composer --version` / `validate` / `dump-autoload -o` / `composer audit`, incl. 'Phase 1.5: Composer and Autoload'); `skills/laravel-plugin-discovery/SKILL.md:59` ('Full Composer package name'); `skills/codebase-onboarding/SKILL.md:29` (`composer.json` in stack markers); `agents/ecc-php-reviewer.md:77` (`composer audit`); `scripts/lib/project-detect.js` ×10 (`composer.json` / `composer.lock` reads, `getComposerDeps`); `scripts/lib/gateguard-search-filters.js:43` (`'composer.lock'`); `skills/ui-ux-pro-max/SKILL.md:77` (`composer.json` in stack detection).
- **CSS `.composer` (10):** `scripts/lib/plan-canvas/ui.js:171-179,517` (`.composer`, `.composer .hint`, `.composer textarea`, … — a chat-input-box style class).
- **Reply-composer UI constraint (1):** `skills/ui-ux-pro-max/data/ui-reasoning.csv:165` ('Reply composer cues', `"constraint:reply-composer"` — a forum UI pattern, not Cursor's Composer).
- **Video-composer app name (4):** `remotion-composer/` + 'composer app' in `pitch-deck-video/references/openmontage/{runtime-fetch.md:39, README.md:35}` (staged + built copies).
- **Prose (2):** `skills/dev-team/SKILL.md:14` ('it is not a free-form team composer'); `scripts/hooks/cursor-session-env.js:3` ('inject ECC_AGENT_DATA_HOME for the composer session' — see borderline note below).
- **Cursor's Composer UI feature:** zero mentions as a feature name. **Borderline, reported:** `cursor-session-env.js:3` 'the composer session' refers to the Cursor session the `sessionStart` hook runs in (file header cites `https://cursor.com/docs/hooks`); it is session-scope prose, not the Composer agent-mode feature and not a pin — flagged here so the coordinator can judge, not silently passed over.

### Check 10 detail — `LIVE_SMOKE_TEST.md` §14 (quoted)

> ## 14. Grok pins hold — 4.7 High design, 4.6 High Fast task tier (fix programs #13, #16)
>
> - [ ] **Picker selection:** before the first build, select **Grok 4.7 High** in Cursor's model picker. The plugin pins its design role to `grok-4.7-high` (slug form only — no bracket syntax), but Cursor's subagent model allowlist is coupled to the picker dropdown, so the pin can silently fall back to another model if Grok 4.7 High is not selected.
> - [ ] **Design role runs on Grok 4.7 High:** on a build with UI work, confirm the design lead (the agent/skill doing design direction — Taste theme deal, ui-ux-pro-max direction, polish-pass) actually runs on Grok 4.7 High, not on another model. Note what it ran on and any error or fallback.
> - [ ] **Fast tier runs on Grok 4.6 High Fast:** on a mechanical task, confirm the fast-worker / scout actually runs on Grok 4.6 High Fast (`cursor-grok-4.6-high-fast` — the `cursor-` prefix is part of the pin), not on another model. Note what it ran on and any error or fallback.
> - [ ] **"High" cost note:** "High" is a reasoning effort, not a price tier — higher effort generates more reasoning tokens and burns the Cursor weekly usage pool faster. Note whether usage feels materially higher; this does not change the model choice.
>
> **Record the answer here:** the design role ran on ____________________ (Grok 4.7 High / another model — which one / fell back silently). The fast tier ran on ____________________ (Grok 4.6 High Fast / another model — which one / fell back silently).

Step 7 also names the pin: 'Ask for a reasoning-heavy task (should use deep-reasoner → `grok-4.7-high`).' Step 6 likewise checks deep-reasoner reports itself 'with model `grok-4.7-high`'. No stale model name anywhere in the doc (checks 1–5 all 0 for this file).

### Check 13 detail — reworded labels, spot-checked (5)

1. `hackathon-ecc/hooks/adapter.js:2-8` — 'Cursor Hook Adapter (live Cursor hook infrastructure) / Transforms Cursor stdin JSON to the format the hook scripts expect … is live infrastructure — not an unwired script.' (the 'not a Claude Code-only…' clause is gone; `transformToClaude` is now `transformToHookPayload`, `CLAUDE_SESSION_ID` → `ECC_SESSION_ID`.)
2. `hackathon-ecc/scripts/lib/agent-emit-pi.js:15-17` — 'The source model tier is preserved as a YAML comment (`# source model tier: grok-4.7-high`) rather than a `model:` field, because Grok slugs are not valid Pi model ids.'
3. `hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs:11,111-112` — '`node <skill>/scripts/gate.mjs --hook cursor`'; '`const MODES = { cursor: 'block' };`'; '`gate: --hook takes cursor`'.
4. `hackathon-ecc/skills/design-taste-frontend/references/gate.md:136,155-161,167` — 'In Cursor the skill's own frontmatter adds the gate as a Stop hook…'; '`--hook cursor`'; '**Antigravity**, `.agents/hooks.json`…'.
5. `hackathon-ecc/skills/orchestrate/SKILL.md:32` — '…they invoked external model CLIs.' (was: 'external Codex/Gemini CLIs' in the staged source).

## What was NOT done (per the task)

No plugin file was edited, no rebuild was run, nothing was committed, bundled, or pushed, and the Campus Eats artifact was not touched. `fix16/` working files were not swept (only read to understand the scrub mechanism: `fix16.py` deletions + targeted edits + the generic tree-wide pass at lines 1160–1239, which is the last build step at `build.sh:23210`).

## Appendix A — `build.sh` exception inventory (all 832 hits)

Class key: **(a)** OLD-side match pattern (string that must match upstream/previously-written text for a patch to locate its target — the acknowledged exception, with (b) comments); **(b)** comment explaining a match; **(c1)** NEW-side patch text — written into the built tree by STEP 3 and removed/rewritten by the `fix16.py` final scrub (or its target file is deleted by `fix16.py`); **(c2)** staged file write (heredoc straight into the built tree, likewise scrubbed); **(c3)** build-time source path in a copy command (the path string itself never lands in the tree; the copied content is patched/scrubbed downstream). Counts: (a) 408, (b) 53, (c1) 368, (c2) 1, (c3) 2; per term — `composer-2.5` 0; `claude` 702 = a 337, b 48, c1 314, c2 1, c3 2; `codex` 103 = a 51, b 1, c1 51; `anthropic` 5 = a 3, b 1, c1 1; `opus` 22 = a 17, b 3, c1 2.

How the classes were determined: every hit line was located inside its enclosing construct in `build.sh` — `audit_patch` / `audit15_patch` / `audit3_patch` / `audit2_patch` / `audit6_patch` `(OLD, NEW)` pairs (first element = (a), second = (c1)), `old = …` / `new = …` assignments, `mapping`/`re.search` match logic (a), `#` comments (b), and the four `cat >`/`cat >>` heredocs (c2). Single-line `("…", "…")` pairs were split by element position (first = (a), second = (c1)) after reading each pair; `append_desc` text is (c1). The `ships?` column says whether the patch target file exists in the final built tree (True = scrubbed in place by `fix16.py`; False = deleted by `fix16.py`). Excerpts are cut at 100 chars.

### Class (a) OLD-side match pattern — 408 hits

| term | build.sh:line | target file | ships? | excerpt |
|---|---|---|---|---|
| anthropic | 7678 | `skills/ui-ux-pro-max/SKILL.md` | True | - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| anthropic | 12834 | `skills/gan-style-harness/SKILL.md` | True | description: "GAN-inspired Generator-Evaluator agent harness for building high-quality applications  |
| anthropic | 12842 | `skills/gan-style-harness/SKILL.md` | True | > Inspired by [Anthropic's Harness Design for Long-Running Application Development](https://www.anth |
| claude | 415 | `agents` | True | pat_file = re.compile(rf"(?<!ecc/)(?<!claude/rules/)({RULE_DIRS})/({RULE_FILES})\.md") |
| claude | 486 | `skills/delivery-gate/SKILL.md` | True | mkdir -p ~/.claude/scripts |
| claude | 487 | `skills/delivery-gate/SKILL.md` | True | cp skills/delivery-gate/hooks/quality-gate.py ~/.claude/scripts/ |
| claude | 490 | `skills/delivery-gate/SKILL.md` | True | Add to `~/.claude/settings.json`: |
| claude | 497 | `skills/delivery-gate/SKILL.md` | True | "command": "python3 ~/.claude/scripts/quality-gate.py", |
| claude | 593 | `skills/delivery-gate/SKILL.md` | True | "description: Stop hook that blocks Claude from finishing until quality checks pass. Detects rationa |
| claude | 599 | `skills/delivery-gate/SKILL.md` | True | "description: Run a six-phase verification of a Claude Code session's work — build, type check, lint |
| claude | 602 | `skills/delivery-gate/SKILL.md` | True | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, |
| claude | 888 | `skills/security-scan/SKILL.md` | True | - Setting up a new Claude Code project |
| claude | 889 | `skills/security-scan/SKILL.md` | True | - After modifying `.claude/settings.json`, `CLAUDE.md`, or MCP configs |
| claude | 891 | `skills/security-scan/SKILL.md` | True | - When onboarding to a new repository with existing Claude Code configs |
| claude | 944 | `skills/security-scan/SKILL.md` | True | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use fo |
| claude | 1035 | `skills/security-scan/SKILL.md` | True | "uv run python -m scripts.run --dry-run ~/.claude/skills/search-first/SKILL.md", |
| claude | 1535 | `commands/cost-report.md` | False | ("""Summarize local Claude Code spend by day, model, and session from the metrics |
| claude | 1541 | `commands/cost-report.md` | False | `~/.claude/metrics/costs.jsonl`. Each row is a **cumulative snapshot for that |
| claude | 1567 | `commands/cost-report.md` | False | 1. Check that `~/.claude/metrics/costs.jsonl` exists. If it does not, tell the |
| claude | 2213 | `commands/learn-eval.md` | True | - **Global** (`~/.claude/skills/<pattern-name>/SKILL.md`): Generic patterns usable across 2+ project |
| claude | 2214 | `commands/learn-eval.md` | True | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowle |
| claude | 2216 | `commands/learn-eval.md` | True | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| claude | 2239 | `commands/learn-eval.md` | True | `~/.claude/skills/`, project `.claude/skills/`, or `MEMORY.md` as |
| claude | 2265 | `commands/learn-eval.md` | True | - [ ] Grep `~/.claude/skills/` and relevant project `.claude/skills/` files by keyword to check for  |
| claude | 2293 | `commands/learn.md` | True | Create a skill at `~/.claude/skills/<pattern-name>/SKILL.md`: |
| claude | 2319 | `commands/learn.md` | True | inside the approved skill root (`~/.claude/skills/`). |
| claude | 2345 | `commands/learn.md` | True | 5. Save to `~/.claude/skills/<pattern-name>/SKILL.md` |
| claude | 2373 | `commands/loop-status.md` | False | The CLI scans local Claude transcript JSONL files under |
| claude | 2374 | `commands/loop-status.md` | False | `~/.claude/projects/**` and reports stale `ScheduleWakeup` calls or `Bash` |
| claude | 2400 | `commands/loop-status.md` | False | - `ecc loop-status --watch --write-dir ~/.claude/loops` maintains |
| claude | 2446 | `commands/multi-backend.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2547 | `commands/multi-execute.md` | False | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Mu |
| claude | 2549 | `commands/multi-execute.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2569 | `commands/multi-execute.md` | False | ('- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missi |
| claude | 2646 | `commands/multi-execute.md` | False | ("""/ Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/revi |
| claude | 2723 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| claude | 2728 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| claude | 2769 | `commands/multi-frontend.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2872 | `commands/multi-plan.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2899 | `commands/multi-plan.md` | False | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by  |
| claude | 2901 | `commands/multi-plan.md` | False | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, |
| claude | 2918 | `commands/multi-plan.md` | False | ('- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan file |
| claude | 2945 | `commands/multi-plan.md` | False | ("""/ Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/a |
| claude | 2994 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| claude | 3011 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| claude | 3038 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| claude | 3043 | `commands/multi-plan.md` | False | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| claude | 3068 | `commands/multi-workflow.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 3088 | `commands/multi-workflow.md` | False | ('- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call S |
| claude | 3140 | `commands/multi-workflow.md` | False | ("""/ Analysis / `~/.claude/.ccg/prompts/codex/analyzer.md` / `~/.claude/.ccg/prompts/antigravity/an |
| claude | 3141 | `commands/multi-workflow.md` | False | / Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/archi |
| claude | 3142 | `commands/multi-workflow.md` | False | / Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/reviewer |
| claude | 3199 | `commands/multi-workflow.md` | False | node scripts/orchestrate-worktrees.js .claude/plan/workflow-e2e-test.json --execute |
| claude | 3270 | `commands/multi-workflow.md` | False | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/ta |
| claude | 3501 | `commands/project-init.md` | True | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gem |
| claude | 3549 | `commands/project-init.md` | True | ## CLAUDE.md Guidance |
| claude | 3551 | `commands/project-init.md` | True | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it  |
| claude | 3567 | `commands/project-init.md` | True | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| claude | 3848 | `commands/santa-loop.md` | False | #### Reviewer A: Claude Agent (always runs) |
| claude | 3856 | `commands/santa-loop.md` | False | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| claude | 3876 | `commands/santa-loop.md` | False | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second Claude Agent (s |
| claude | 3904 | `commands/security-scan.md` | True | - `path` (optional): defaults to the current project. Use a `.claude/` path, a repo root, or a check |
| claude | 3927 | `commands/sessions.md` | True | description: Manage Claude Code session history, aliases, and session metadata. |
| claude | 3932 | `commands/sessions.md` | True | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/sessi |
| claude | 3958 | `commands/sessions.md` | True | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.clau |
| claude | 3959 | `commands/sessions.md` | True | - Aliases are stored in `~/.claude/session-aliases.json` |
| claude | 3984 | `commands/skill-create.md` | True | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that te |
| claude | 4027 | `rules/common-agents.mdc` | True | Located in `~/.claude/agents/`: |
| claude | 4121 | `rules/common-git-workflow.mdc` | True | Note: ECC-managed installs set `"includeCoAuthoredBy": false` in `~/.claude/settings.json`, so commi |
| claude | 4165 | `rules/common-hooks.mdc` | True | - Configure `permissions.allow` rules in `~/.claude/settings.json` (or a project's `.claude/settings |
| claude | 4246 | `rules/common-performance.mdc` | True | In Claude Code, adaptive reasoning lets the model choose how much to think for each task. |
| claude | 4251 | `rules/common-performance.mdc` | True | - **Effort**: Use `/effort` in a session, `--effort <level>` at launch, or `CLAUDE_CODE_EFFORT_LEVEL |
| claude | 4253 | `rules/common-performance.mdc` | True | - **Fixed budget**: Claude Code ignores positive `MAX_THINKING_TOKENS` values on adaptive reasoning  |
| claude | 4256 | `rules/common-performance.mdc` | True | See [Claude Code model configuration](https://code.claude.com/docs/en/model-config#adjust-effort-lev |
| claude | 4257 | `rules/common-performance.mdc` | True | and [environment variables](https://code.claude.com/docs/en/env-vars) for supported controls. |
| claude | 4490 | `skills/ai-regression-testing/SKILL.md` | True | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| claude | 4519 | `skills/ai-regression-testing/SKILL.md` | True | <!-- .claude/commands/bug-check.md --> |
| claude | 4588 | `skills/browser-qa/SKILL.md` | True | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| claude | 4612 | `skills/ck/SKILL.md` | True | `~/.claude/skills/ck/commands/` for a manual install, or the ck skill inside the ECC |
| claude | 4613 | `skills/ck/SKILL.md` | True | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| claude | 4614 | `skills/ck/SKILL.md` | True | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| claude | 4641 | `skills/ck/SKILL.md` | True | ~/.claude/ck/ |
| claude | 4669 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| claude | 4721 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| claude | 4730 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| claude | 4757 | `skills/ck/SKILL.md` | True | ("""node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| claude | 4765 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| claude | 4776 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| claude | 4801 | `skills/ck/SKILL.md` | True | ("""node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| claude | 4809 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| claude | 4813 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run""", |
| claude | 4827 | `skills/ck/SKILL.md` | True | ('\n---\n\n## SessionStart Hook\n\nThe hook at `hooks/session-start.mjs` in this skill\'s directory  |
| claude | 4829 | `skills/ck/SKILL.md` | True | ("""unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| claude | 4970 | `skills/config-gc/SKILL.md` | False | description: Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (sk |
| claude | 4975 | `skills/config-gc/SKILL.md` | False | # Config GC — Garbage Collection for Claude Code Setups |
| claude | 5015 | `skills/context-budget/SKILL.md` | True | / Claude Code / `/context` / Shows the live context breakdown. Use `/context all` for expanded items |
| claude | 5018 | `skills/context-budget/SKILL.md` | True | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/c |
| claude | 5043 | `skills/context-budget/SKILL.md` | True | [`/context` and `/usage` commands (`/cost` is an alias)](https://code.claude.com/docs/en/commands). |
| claude | 5093 | `skills/continuous-learning-v2/SKILL.md` | True | No extra `settings.json` hook block is required. Claude Code v2.1+ auto-loads the plugin `hooks/hook |
| claude | 5095 | `skills/continuous-learning-v2/SKILL.md` | True | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreTool |
| claude | 5097 | `skills/continuous-learning-v2/SKILL.md` | True | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| claude | 5155 | `skills/council/SKILL.md` | True | - the in-context Claude voice |
| claude | 5236 | `skills/council/SKILL.md` | True | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| claude | 5293 | `skills/delivery-gate/SKILL.md` | True | # Delivery Gate — Mechanical Quality Gate for Claude Code |
| claude | 5295 | `skills/delivery-gate/SKILL.md` | True | A **Stop hook** that checks three things before Claude can finish a session, using only **determinis |
| claude | 5329 | `skills/delivery-gate/SKILL.md` | True | The hook blocks a given Stop at most once. When Claude Code re-runs it with `stop_hook_active: true` |
| claude | 5333 | `skills/delivery-gate/SKILL.md` | True | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a differe |
| claude | 5359 | `skills/delivery-gate/SKILL.md` | True | Create these files in your project's memory directory (`~/.claude/projects/<encoded-project-path>/me |
| claude | 5751 | `skills/inherit-legacy-style/SKILL.md` | True | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit convent |
| claude | 5798 | `skills/inherit-legacy-style/SKILL.md` | True | ('- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & Sta |
| claude | 6178 | `skills/orch-pipeline/SKILL.md` | True | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| claude | 6376 | `skills/santa-method/SKILL.md` | True | ### Pattern A: Claude Code Subagents (Recommended) |
| claude | 6381 | `skills/santa-method/SKILL.md` | True | # In a Claude Code session, use the Agent tool to spawn reviewers |
| claude | 6425 | `skills/security-scan/SKILL.md` | True | description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities,  |
| claude | 6432 | `skills/security-scan/SKILL.md` | True | Audit your Claude Code configuration for security issues using [AgentShield](https://github.com/affa |
| claude | 6461 | `skills/security-scan/SKILL.md` | True | / `CLAUDE.md` / Hardcoded secrets, auto-run instructions, prompt injection patterns / |
| claude | 6487 | `skills/security-scan/SKILL.md` | True | Run against the current project's `.claude/` directory: |
| claude | 6494 | `skills/security-scan/SKILL.md` | True | npx ecc-agentshield scan --path /path/to/.claude |
| claude | 6527 | `skills/security-scan/SKILL.md` | True | Scaffold a new secure `.claude/` configuration from scratch: |
| claude | 6553 | `skills/security-scan/SKILL.md` | True | - `CLAUDE.md` with security best practices |
| claude | 6579 | `skills/security-scan/SKILL.md` | True | - Auto-run instructions in CLAUDE.md (prompt injection vector) |
| claude | 6607 | `skills/skill-stocktake/SKILL.md` | True | Slash command (`/skill-stocktake`) that audits all Claude skills and commands using a quality checkl |
| claude | 6633 | `skills/skill-stocktake/SKILL.md` | True | / `~/.claude/skills/` / Global skills (all projects) / |
| claude | 6634 | `skills/skill-stocktake/SKILL.md` | True | / `{cwd}/.claude/skills/` / Project-level skills (if the directory exists) / |
| claude | 6661 | `skills/skill-stocktake/SKILL.md` | True | If the project has no `.claude/skills/` directory, only global skills and commands are evaluated. |
| claude | 6681 | `skills/skill-stocktake/SKILL.md` | True | ('/------/---------/---------/\n/ Quick Scan / `results.json` exists (default) / 5–10 min /\n/ Full  |
| claude | 6683 | `skills/skill-stocktake/SKILL.md` | True | ('\nRun this entire block in **one Bash invocation**. It prints the inventory for the agent and init |
| claude | 6685 | `skills/skill-stocktake/SKILL.md` | True | ('      / .mode = "full"\n      / .batch_progress = {\n          total: ($inventory.skills / length) |
| claude | 6687 | `skills/skill-stocktake/SKILL.md` | True | ('\nThe subagent reads each assigned skill, applies the checklist, and returns a JSON object with a  |
| claude | 6695 | `skills/skill-stocktake/SKILL.md` | True | RESULTS_JSON=~/.claude/skills/skill-stocktake/results.json |
| claude | 6715 | `skills/skill-stocktake/SKILL.md` | True | ('    if (.skills / length) == .batch_progress.total then\n      {skills: {}, mode: "full", batch_pr |
| claude | 6723 | `skills/skill-stocktake/SKILL.md` | True | `~/.claude/skills/skill-stocktake/results.json`: |
| claude | 6749 | `skills/skill-stocktake/SKILL.md` | True | "~/.claude/skills/skill-name/SKILL.md": { |
| claude | 6750 | `skills/skill-stocktake/SKILL.md` | True | "path": "~/.claude/skills/skill-name/SKILL.md", |
| claude | 6884 | `skills/strategic-compact/SKILL.md` | True | **Installed as a plugin?** No setup is needed. The plugin's `hooks/hooks.json` already registers `su |
| claude | 6886 | `skills/strategic-compact/SKILL.md` | True | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| claude | 6913 | `skills/strategic-compact/SKILL.md` | True | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smalle |
| claude | 6971 | `skills/tdd-workflow/SKILL.md` | True | # Use the configured plugin root or standalone install (~/.claude or |
| claude | 6972 | `skills/tdd-workflow/SKILL.md` | True | # $CLAUDE_CONFIG_DIR). For a reviewed and explicitly authorized ECC checkout: |
| claude | 6973 | `skills/tdd-workflow/SKILL.md` | True | # export CLAUDE_PLUGIN_ROOT="/absolute/path/to/reviewed/ECC" |
| claude | 6974 | `skills/tdd-workflow/SKILL.md` | True | ECC_ROOT="${CLAUDE_PLUGIN_ROOT:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}" |
| claude | 6975 | `skills/tdd-workflow/SKILL.md` | True | [ -f "$ECC_ROOT/scripts/setup-package-manager.js" ] // { echo "ECC scripts not found in the selected |
| claude | 6979 | `skills/tdd-workflow/SKILL.md` | True | The resolution lines use the configured plugin root or standalone install and stop when the selected |
| claude | 6981 | `skills/tdd-workflow/SKILL.md` | True | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`,  |
| claude | 7060 | `skills/verification-loop/SKILL.md` | True | A comprehensive verification system for Claude Code sessions. |
| claude | 7105 | `skills/agents-md-generator/SKILL.md` | True | description: Automatically generate comprehensive AGENTS.md files that teach AI agents how to work w |
| claude | 7270 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --domain <do |
| claude | 7296 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<product_type> <indus |
| claude | 7303 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "beauty spa wellness s |
| claude | 7336 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-sys |
| claude | 7362 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<query>" --design-sys |
| claude | 7388 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "internal analytics da |
| claude | 7394 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --domain < |
| claude | 7426 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "<keyword>" --stack <s |
| claude | 7452 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "AI search tool modern |
| claude | 7455 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "keyboard focus modal" |
| claude | 7458 | `skills/ui-ux-pro-max/SKILL.md` | True | python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" "suspense streaming bu |
| claude | 7665 | `skills/ui-ux-pro-max/SKILL.md` | True | - **Rules are system-injected**: `.claude/rules/*.md` files load automatically every session. Unlike |
| claude | 7670 | `skills/ui-ux-pro-max/SKILL.md` | True | claude /mail                    # Email-only triage |
| claude | 7671 | `skills/ui-ux-pro-max/SKILL.md` | True | claude /slack                   # Slack-only triage |
| claude | 7672 | `skills/ui-ux-pro-max/SKILL.md` | True | claude /today                   # All channels + calendar + todo |
| claude | 7673 | `skills/ui-ux-pro-max/SKILL.md` | True | claude /schedule-reply "Reply to Sarah about the board meeting" |
| claude | 7678 | `skills/ui-ux-pro-max/SKILL.md` | True | - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| claude | 7786 | `skills/ui-ux-pro-max/SKILL.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| claude | 7793 | `skills/ui-ux-pro-max/SKILL.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| claude | 7800 | `skills/ui-ux-pro-max/SKILL.md` | True | - Keep Claude as the writer: Astra reviews in a read-only sandbox and returns a structured verdict,  |
| claude | 7889 | `skills/ui-ux-pro-max/SKILL.md` | True | 3. Log checkpoint to `.claude/checkpoints.log`: |
| claude | 7892 | `skills/ui-ux-pro-max/SKILL.md` | True | echo "$(date +%Y-%m-%d-%H:%M) / $CHECKPOINT_NAME / $(git rev-parse --short HEAD)" >> .claude/checkpo |
| claude | 7915 | `skills/ui-ux-pro-max/SKILL.md` | True | - `/security-scan` for Claude/OpenCode configuration security review |
| claude | 8074 | `skills/ui-ux-pro-max/SKILL.md` | True | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 8102 | `skills/ui-ux-pro-max/SKILL.md` | True | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 8300 | `skills/ui-ux-pro-max/SKILL.md` | True | ("""> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| claude | 8302 | `skills/ui-ux-pro-max/SKILL.md` | True | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts |
| claude | 8332 | `skills/ui-ux-pro-max/SKILL.md` | True | **Claude Commands:** /pm2-all, /pm2-all-stop, /pm2-{port}, /pm2-{port}-stop, /pm2-logs, /pm2-status |
| claude | 8364 | `skills/ui-ux-pro-max/SKILL.md` | True | Run two independent reviewers (Claude Opus + an external model) against the current task output. Bot |
| claude | 8408 | `skills/ui-ux-pro-max/SKILL.md` | True | #### Reviewer A: Claude Agent (always runs) |
| claude | 8416 | `skills/ui-ux-pro-max/SKILL.md` | True | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)""", |
| claude | 8436 | `skills/ui-ux-pro-max/SKILL.md` | True | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent  |
| claude | 8486 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8606 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8638 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8670 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8702 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8732 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8762 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8820 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8852 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8884 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 8994 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 9024 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 9056 | `skills/ui-ux-pro-max/SKILL.md` | True | Configure in `~/.claude/settings.json`: |
| claude | 9494 | `skills/ui-ux-pro-max/SKILL.md` | True | ('1. CLAUDE.md (commands, architecture, key files)\n2. setup.sh (one-command bootstrap, make executa |
| claude | 9738 | `skills/ui-ux-pro-max/SKILL.md` | True | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| claude | 9905 | `skills/ui-ux-pro-max/SKILL.md` | True | ('\nBe rigorous. Your job is to find problems, not to approve.\n"""\n```\n\n```python\n# Spawn revie |
| claude | 11064 | `agents/ecc-opensource-packager.md` | True | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, se |
| claude | 11575 | `commands/astra-review.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| claude | 11582 | `commands/astra-review.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| claude | 11634 | `commands/cost-report.md` | False | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for |
| claude | 11640 | `commands/cost-report.md` | False | Summarize local Claude Code spend by day, model, and session from the metrics""", |
| claude | 11654 | `commands/evolve.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--gene |
| claude | 11657 | `commands/evolve.md` | True | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| claude | 11660 | `commands/evolve.md` | True | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py evolve [--generate] |
| claude | 11706 | `commands/instinct-import.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-o |
| claude | 11709 | `commands/instinct-import.md` | True | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| claude | 11712 | `commands/instinct-import.md` | True | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url> |
| claude | 11743 | `commands/learn-eval.md` | True | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowle |
| claude | 11745 | `commands/learn-eval.md` | True | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| claude | 11769 | `commands/learn-eval.md` | True | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| claude | 11795 | `commands/learn-eval.md` | True | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check |
| claude | 11851 | `commands/multi-backend.md` | False | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the b |
| claude | 11880 | `commands/multi-execute.md` | False | description: Execute a multi-model implementation plan while preserving Claude as the only filesyste |
| claude | 11885 | `commands/multi-execute.md` | False | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Mu |
| claude | 11913 | `commands/multi-frontend.md` | False | ("""> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the b |
| claude | 11962 | `commands/projects.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| claude | 11965 | `commands/projects.md` | True | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| claude | 11968 | `commands/projects.md` | True | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py projects |
| claude | 11996 | `commands/promote.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [insti |
| claude | 11999 | `commands/promote.md` | True | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| claude | 12002 | `commands/promote.md` | True | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py promote [instinct-id] [--for |
| claude | 12030 | `commands/prune.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| claude | 12033 | `commands/prune.md` | True | Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation): |
| claude | 12036 | `commands/prune.md` | True | python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py prune |
| claude | 12062 | `commands/resume-session.md` | True | description: Load the most recent session file from ~/.claude/session-data/ and resume work with ful |
| claude | 12080 | `commands/save-session.md` | True | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be re |
| claude | 12339 | `rules/dart-hooks.mdc` | True | { "type": "command", "command": "dart format $CLAUDE_FILE_PATHS" } |
| claude | 12425 | `scripts/gan-harness.sh` | False | ('  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log " |
| claude | 12427 | `scripts/gan-harness.sh` | False | ('  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i- |
| claude | 12429 | `scripts/gan-harness.sh` | False | ('    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    e |
| claude | 12724 | `skills/continuous-learning/SKILL.md` | True | ("""- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| claude | 12752 | `skills/continuous-learning-v2/agents/observer-loop.sh` | True | ('  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # doe |
| claude | 12877 | `skills/plankton-code-quality/SKILL.md` | True | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Cla |
| claude | 13001 | `skills/skill-comply/SKILL.md` | False | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| claude | 13004 | `skills/skill-comply/SKILL.md` | False | uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md |
| claude | 13050 | `skills/strategic-compact/SKILL.md` | True | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings. |
| claude | 13052 | `skills/strategic-compact/SKILL.md` | True | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| claude | 13060 | `skills/strategic-compact/SKILL.md` | True | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| claude | 13064 | `skills/strategic-compact/SKILL.md` | True | "hooks": [{ "type": "command", "command": "node ~/.claude/scripts/hooks/suggest-compact.js" }] |
| claude | 13416 | `commands/multi-backend.md` | False | "description: Run a backend-focused multi-model workflow for APIs, algorithms, data, and business lo |
| claude | 13419 | `commands/multi-execute.md` | False | ("description: Execute a multi-model implementation plan while preserving Claude as the only filesys |
| claude | 13426 | `commands/multi-frontend.md` | False | "description: Run a frontend-focused multi-model workflow for components, layouts, animation, and UI |
| claude | 13436 | `commands/multi-workflow.md` | False | "description: Run a full multi-model development workflow with research, planning, execution, optimi |
| claude | 13453 | `skills/strategic-compact/SKILL.md` | True | ("(Claude Code-origin — the manual-compaction advice applies in Cursor; the hook example below is Cu |
| claude | 13479 | `scripts/lib/multi-harness-setup.js` | False | ("""    previewClaude: request => require('../setup').reconcileClaudePlugin( |
| claude | 13480 | `scripts/lib/multi-harness-setup.js` | False | { dryRun: true, hooks: request.claudeHooks, scope: request.claudeScope } |
| claude | 13483 | `scripts/lib/multi-harness-setup.js` | False | ("""    applyClaude: request => require('../setup').reconcileClaudePlugin( |
| claude | 13484 | `scripts/lib/multi-harness-setup.js` | False | { dryRun: false, hooks: request.claudeHooks, scope: request.claudeScope } |
| claude | 13533 | `commands/evolve.md` | True | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/evolved/` |
| claude | 13534 | `commands/evolve.md` | True | - Global fallback: `~/.claude/homunculus/evolved/`""", |
| claude | 13541 | `commands/instinct-import.md` | True | ("""   - Project scope: `~/.claude/homunculus/projects/<project-id>/instincts/inherited/` |
| claude | 13542 | `commands/instinct-import.md` | True | - Global scope: `~/.claude/homunculus/instincts/inherited/`""", |
| claude | 13546 | `commands/instinct-import.md` | True | ("""New instincts saved to: ~/.claude/homunculus/instincts/inherited/""", |
| claude | 13551 | `commands/instinct-status.md` | True | ("""2. Read project instincts from `~/.claude/homunculus/projects/<project-id>/instincts/` |
| claude | 13552 | `commands/instinct-status.md` | True | 3. Read global instincts from `~/.claude/homunculus/instincts/`""", |
| claude | 13560 | `commands/projects.md` | True | ("""1. Read `~/.claude/homunculus/projects.json`""", |
| claude | 13567 | `commands/promote.md` | True | ("""4. Write promoted instincts to `~/.claude/homunculus/instincts/personal/` with `scope: global`"" |
| claude | 13574 | `commands/sessions.md` | True | ("""description: Manage Claude Code session history, aliases, and session metadata.""", |
| claude | 13684 | `skills/skill-comply/SKILL.md` | False | ("""uv run python -m scripts.run ~/.claude/rules/common/testing.md""", |
| claude | 13811 | `scripts/lib/resolve-ecc-root.js` | True | (""" *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code} |
| claude | 13812 | `scripts/lib/resolve-ecc-root.js` | True | *   5. Fallback to ~/.claude/ (original behaviour)""", |
| claude | 13820 | `scripts/lib/resolve-ecc-root.js` | True | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| claude | 13832 | `scripts/lib/resolve-ecc-root.js` | True | return claudeDir; |
| claude | 13861 | `scripts/lib/resolve-ecc-root.js` | True | (""" * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| claude | 13863 | `scripts/lib/resolve-ecc-root.js` | True | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| claude | 13864 | `scripts/lib/resolve-ecc-root.js` | True | * under ~/.claude/plugins/, and the versioned plugin cache — only far enough to |
| claude | 13963 | `scripts/lib/resolve-ecc-root.js` | True | old = 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" ' + arg |
| claude | 13971 | `scripts/lib/resolve-ecc-root.js` | True | old = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| claude | 13972 | `scripts/lib/resolve-ecc-root.js` | True | "./.claude/scripts/astra-review.js" \\''' |
| claude | 14668 | `skills/continuous-learning-v2/SKILL.md` | True | (r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `script |
| claude | 14696 | `skills/delivery-gate/hooks/quality-gate.py` | True | ('"""\nStop hook: quality gate with delivery check.\nDetects incomplete work, stale learning logs, a |
| claude | 15373 | `commands/multi-execute.md` | False | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 15385 | `commands/multi-plan.md` | False | (r"""**If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 15408 | `scripts/lib/resolve-ecc-root.js` | True | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| claude | 15409 | `scripts/lib/resolve-ecc-root.js` | True | *   6. Fallback to ~/.claude/ (original behaviour)""", |
| claude | 15627 | `scripts/lib/harness-adapter-compliance.js` | True | (r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (claude -> pi)',''' |
| claude | 15839 | `rules/web-hooks.mdc` | True | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.js |
| claude | 15843 | `rules/web-hooks.mdc` | True | (r'''Block oversized writes from tool input content, not from a file that may not exist yet. This wa |
| claude | 15845 | `rules/web-hooks.mdc` | True | (r'''This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` eve |
| claude | 15994 | `manifests/context-packs/skill-triggers@1.json` | True | "audit claude config", |
| claude | 15995 | `manifests/context-packs/skill-triggers@1.json` | True | "claudemd security", |
| claude | 16256 | `agents/ecc-code-reviewer.md` | True | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| claude | 16356 | `commands/setup-pm.md` | True | 1. **Environment variable**: `CLAUDE_PACKAGE_MANAGER` |
| claude | 16357 | `commands/setup-pm.md` | True | 2. **Project config**: `.claude/package-manager.json` |
| claude | 16360 | `commands/setup-pm.md` | True | 5. **Global config**: `~/.claude/package-manager.json` |
| claude | 16367 | `commands/setup-pm.md` | True | // ~/.claude/package-manager.json |
| claude | 16406 | `commands/setup-pm.md` | True | // .claude/package-manager.json |
| claude | 16433 | `commands/setup-pm.md` | True | Set `CLAUDE_PACKAGE_MANAGER` to override all other detection methods: |
| claude | 16437 | `commands/setup-pm.md` | True | $env:CLAUDE_PACKAGE_MANAGER = "pnpm" |
| claude | 16440 | `commands/setup-pm.md` | True | export CLAUDE_PACKAGE_MANAGER=pnpm |
| claude | 16479 | `commands/skill-create.md` | True | `.claude/skills/`; a global skill uses `~/.claude/skills/`. |
| claude | 17063 | `scripts/lib/package-manager.js` | True | const { commandExists, getClaudeDir, readFile, writeFile } = require('./utils'); |
| claude | 17091 | `scripts/lib/package-manager.js` | True | return path.join(getClaudeDir(), 'package-manager.json'); |
| claude | 17159 | `scripts/lib/package-manager.js` | True | * 1. Environment variable CLAUDE_PACKAGE_MANAGER |
| claude | 17160 | `scripts/lib/package-manager.js` | True | * 2. Project-specific config (in .claude/package-manager.json) |
| claude | 17163 | `scripts/lib/package-manager.js` | True | * 5. Global user preference (in ~/.claude/package-manager.json) |
| claude | 17197 | `scripts/lib/package-manager.js` | True | const envPm = process.env.CLAUDE_PACKAGE_MANAGER; |
| claude | 17225 | `scripts/lib/package-manager.js` | True | const projectConfigPath = path.join(projectDir, '.claude', 'package-manager.json'); |
| claude | 17317 | `scripts/lib/package-manager.js` | True | const configDir = path.join(projectDir, '.claude'); |
| claude | 17353 | `scripts/lib/package-manager.js` | True | message += '  - Global: Set CLAUDE_PACKAGE_MANAGER environment variable\n'; |
| claude | 17354 | `scripts/lib/package-manager.js` | True | message += '  - Or add to ~/.claude/package-manager.json: {"packageManager": "pnpm"}\n'; |
| claude | 17435 | `scripts/setup-package-manager.js` | True | Package Manager Setup for Claude Code |
| claude | 17442 | `scripts/setup-package-manager.js` | True | --global <pm>   Set global preference (saves to ~/.claude/package-manager.json) |
| claude | 17443 | `scripts/setup-package-manager.js` | True | --project <pm>  Set project preference (saves to .claude/package-manager.json) |
| claude | 17481 | `scripts/setup-package-manager.js` | True | console.log(`  Environment var: ${process.env.CLAUDE_PACKAGE_MANAGER // 'not set'}`); |
| claude | 17507 | `scripts/setup-package-manager.js` | True | console.log('  Saved to: ~/.claude/package-manager.json'); |
| claude | 17534 | `scripts/setup-package-manager.js` | True | console.log('  Saved to: .claude/package-manager.json'); |
| claude | 17565 | `skills/laravel-plugin-discovery/SKILL.md` | True | LaraPlugins MCP server must be configured. Add to your `~/.claude.json` mcpServers: |
| claude | 17625 | `skills/rules-distill/SKILL.md` | True | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| claude | 17631 | `skills/rules-distill/SKILL.md` | True | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| claude | 17682 | `skills/santa-method/SKILL.md` | True | ### Pattern A: Claude Code Subagents (Recommended) |
| claude | 17712 | `skills/skill-scout/SKILL.md` | True | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null / grep -iE "keyword/synonym" |
| claude | 17713 | `skills/skill-scout/SKILL.md` | True | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null / grep -iE "keyword/syno |
| claude | 17737 | `skills/skill-scout/SKILL.md` | True | (r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null / grep -iE "keyword |
| claude | 17743 | `skills/skill-scout/SKILL.md` | True | grep -RilE "keyword/synonym" ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null |
| claude | 17834 | `skills/continuous-learning-v2/SKILL.md` | True | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreTool |
| claude | 17844 | `skills/continuous-learning-v2/SKILL.md` | True | (r'''**If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`:''' |
| claude | 17882 | `rules/dart-hooks.mdc` | True | (r'''The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same  |
| claude | 17912 | `agents/ecc-opensource-packager.md` | True | (r'''See [CLAUDE.md](CLAUDE.md) for detailed commands and architecture.''', |
| claude | 18094 | `skills/tdd-workflow/SKILL.md` | True | (r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAG |
| claude | 18105 | `rules/nuxt-hooks.mdc` | True | (r'''These are Claude Code harness hooks for Nuxt work. They run via the harness, not Claude.''', |
| claude | 18232 | `skills/ui-ux-pro-max/scripts/tests/test_ime_composition.py` | True | ".claude/skills/ui-ux-pro-max/references/quick-reference.md"): |
| claude | 18491 | `skills/opensource-pipeline/SKILL.md` | True | (r'''/ `/opensource package PROJECT` / Generate CLAUDE.md + setup.sh + README /''', |
| claude | 18526 | `commands/multi-plan.md` | False | (r'''/ccg:execute .claude/plan/actual-feature-name.md''', |
| claude | 18532 | `commands/multi-plan.md` | False | (r'''/ccg:execute .claude/plan/<feature-name>.md''', |
| claude | 18551 | `commands/multi-execute.md` | False | (r'''/ccg:execute .claude/plan/feature-name.md''', |
| claude | 18692 | `hooks/adapter.js` | True | * Cursor-to-Claude Code Hook Adapter |
| claude | 18693 | `hooks/adapter.js` | True | * Transforms Cursor stdin JSON to Claude Code hook format, |
| claude | 22050 | `manifests/install-modules.json` | True | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| claude | 22387 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| claude | 22391 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| claude | 22395 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Claude Code only — no Cursor equivalent in this plugin)''', |
| claude | 22403 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''Use when a feature should be built autonomously through generator and evaluator iteration until  |
| claude | 22408 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''### Via Claude Code (Manual) |
| claude | 22567 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''- Quick single-file fixes (use standard `claude -p`)''', |
| claude | 22571 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''### Via Claude Code (Manual)''', |
| claude | 22577 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into  |
| claude | 22580 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev serve |
| claude | 22583 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read E |
| claude | 22586 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. |
| claude | 22611 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in  |
| claude | 22644 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specifi |
| codex | 2444 | `commands/multi-backend.md` | False | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| codex | 2569 | `commands/multi-execute.md` | False | ('- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missi |
| codex | 2646 | `commands/multi-execute.md` | False | ("""/ Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/revi |
| codex | 2685 | `commands/multi-execute.md` | False | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| codex | 2686 | `commands/multi-execute.md` | False | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| codex | 2692 | `commands/multi-execute.md` | False | - Codex: Handle backend part |
| codex | 2720 | `commands/multi-execute.md` | False | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| codex | 2722 | `commands/multi-execute.md` | False | 1. **Codex Review** (`run_in_background: true`): |
| codex | 2723 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| codex | 2736 | `commands/multi-execute.md` | False | 1. Synthesize Codex + Antigravity review feedback |
| codex | 2737 | `commands/multi-execute.md` | False | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| codex | 2898 | `commands/multi-plan.md` | False | - **Mandatory Parallel**: Codex/Antigravity calls MUST use `run_in_background: true` (including sing |
| codex | 2918 | `commands/multi-plan.md` | False | ('- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan file |
| codex | 2945 | `commands/multi-plan.md` | False | ("""/ Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/a |
| codex | 2989 | `commands/multi-plan.md` | False | **Parallel call** Codex and Antigravity (`run_in_background: true`): |
| codex | 2993 | `commands/multi-plan.md` | False | 1. **Codex Backend Analysis**: |
| codex | 2994 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| codex | 3015 | `commands/multi-plan.md` | False | Wait for both models' complete results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and ` |
| codex | 3066 | `commands/multi-workflow.md` | False | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Re |
| codex | 3088 | `commands/multi-workflow.md` | False | ('- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call S |
| codex | 3140 | `commands/multi-workflow.md` | False | ("""/ Analysis / `~/.claude/.ccg/prompts/codex/analyzer.md` / `~/.claude/.ccg/prompts/antigravity/an |
| codex | 3141 | `commands/multi-workflow.md` | False | / Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/archi |
| codex | 3142 | `commands/multi-workflow.md` | False | / Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/reviewer |
| codex | 3233 | `commands/multi-workflow.md` | False | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| codex | 3236 | `commands/multi-workflow.md` | False | Wait for results with `TaskOutput`. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| codex | 3263 | `commands/multi-workflow.md` | False | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| codex | 3270 | `commands/multi-workflow.md` | False | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/ta |
| codex | 3289 | `commands/multi-workflow.md` | False | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| codex | 3501 | `commands/project-init.md` | True | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gem |
| codex | 4490 | `skills/ai-regression-testing/SKILL.md` | True | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| codex | 5013 | `skills/context-budget/SKILL.md` | True | / Codex CLI / `/status` / Shows current token usage and remaining context capacity. Use `/statusline |
| codex | 5014 | `skills/context-budget/SKILL.md` | True | / Codex app / `/status` / Shows current thread context usage and rate limits. / |
| codex | 5018 | `skills/context-budget/SKILL.md` | True | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/c |
| codex | 5133 | `skills/council-multi-model/SKILL.md` | False | ('- suppresses model-visible skill instructions and shell environment inheritance;\n- uses an epheme |
| codex | 7786 | `skills/ui-ux-pro-max/SKILL.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| codex | 7793 | `skills/ui-ux-pro-max/SKILL.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| codex | 7805 | `skills/ui-ux-pro-max/SKILL.md` | True | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| codex | 7806 | `skills/ui-ux-pro-max/SKILL.md` | True | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_ |
| codex | 7862 | `skills/ui-ux-pro-max/SKILL.md` | True | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP  |
| codex | 7864 | `skills/ui-ux-pro-max/SKILL.md` | True | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review hap |
| codex | 7866 | `skills/ui-ux-pro-max/SKILL.md` | True | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without c |
| codex | 11575 | `commands/astra-review.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| codex | 11582 | `commands/astra-review.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| codex | 11612 | `commands/astra-review.md` | True | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP  |
| codex | 11614 | `commands/astra-review.md` | True | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review hap |
| codex | 11616 | `commands/astra-review.md` | True | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without c |
| codex | 11841 | `commands/multi-backend.md` | False | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| codex | 11863 | `commands/multi-backend.md` | False | - Codex-led, Gemini for auxiliary reference""", |
| codex | 11925 | `commands/multi-frontend.md` | False | - Antigravity-led, Codex for auxiliary reference""", |
| codex | 11947 | `commands/multi-workflow.md` | False | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Re |
| codex | 13580 | `scripts/ci/validate-skill-host-compat.js` | False | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| opus | 157 | `agents` | True | mapping = {"sonnet": "cursor-grok-4.6-high-fast", "opus": "grok-4.7-high", "haiku": "cursor-grok-4.6 |
| opus | 164 | `agents` | True | m = re.search(r"^model: (sonnet/opus/haiku)\s*$", txt, re.M) |
| opus | 3850 | `commands/santa-loop.md` | False | Launch an Agent (subagent_type: `code-reviewer`, model: `opus`) with the full rubric + all files und |
| opus | 3876 | `commands/santa-loop.md` | False | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second Claude Agent (s |
| opus | 4211 | `rules/common-performance.mdc` | True | **Opus 5** (Deepest reasoning): |
| opus | 4247 | `rules/common-performance.mdc` | True | For Fable models, Sonnet 5 and later, and Opus 4.7 and later, use effort to control reasoning |
| opus | 4251 | `rules/common-performance.mdc` | True | - **Effort**: Use `/effort` in a session, `--effort <level>` at launch, or `CLAUDE_CODE_EFFORT_LEVEL |
| opus | 4252 | `rules/common-performance.mdc` | True | - **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux), or `alwaysThinkingEnabled` in settings. Thes |
| opus | 4253 | `rules/common-performance.mdc` | True | - **Fixed budget**: Claude Code ignores positive `MAX_THINKING_TOKENS` values on adaptive reasoning  |
| opus | 6912 | `skills/strategic-compact/SKILL.md` | True | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection.  |
| opus | 7788 | `skills/ui-ux-pro-max/SKILL.md` | True | model: opus |
| opus | 7795 | `skills/ui-ux-pro-max/SKILL.md` | True | This command runs on **Opus** (`model: opus`). Opus orchestrates, verifies findings, checks every di |
| opus | 7800 | `skills/ui-ux-pro-max/SKILL.md` | True | - Keep Claude as the writer: Astra reviews in a read-only sandbox and returns a structured verdict,  |
| opus | 7829 | `skills/ui-ux-pro-max/SKILL.md` | True | ('- **PASS** with MEDIUM/LOW findings: list them, fix the ones that are clearly correct, and finish. |
| opus | 7831 | `skills/ui-ux-pro-max/SKILL.md` | True | ('     ```bash\n     node <astra-review.js path> --consent-to-openai --fix-findings <dir>/confirmed. |
| opus | 7839 | `skills/ui-ux-pro-max/SKILL.md` | True | Fixer:      [Fable / Astra (Fable usage limit) / Opus] |
| opus | 8364 | `skills/ui-ux-pro-max/SKILL.md` | True | Run two independent reviewers (Claude Opus + an external model) against the current task output. Bot |

### Class (b) comment explaining a match — 53 hits

| term | build.sh:line | target file | ships? | excerpt |
|---|---|---|---|---|
| anthropic | 23204 | `skills/ui-ux-pro-max/SKILL.md` | True | # --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic --- |
| claude | 150 | `(step-1/2 setup)` | None | # Pin ECC agent models to Grok IDs (fix #16). The install ships bare Claude aliases |
| claude | 174 | `agents` | True | # Claude Code review loop the plugin does not ship). Drop it. |
| claude | 414 | `agents` | True | # or by a Claude Code ~/.claude/rules/ path, which is not a plugin path) |
| claude | 473 | `agents` | True | # The stock example installs quality-gate.py as a Claude Code Stop hook at |
| claude | 474 | `agents` | True | # ~/.claude/scripts/. That path does not exist in Cursor, and an automatic |
| claude | 13371 | `skills/ui-ux-pro-max/SKILL.md` | True | # replaces it with the Claude Code Task (Explore agent) fallback, since the |
| claude | 13372 | `skills/ui-ux-pro-max/SKILL.md` | True | # multi-* commands are Claude Code-only. |
| claude | 13413 | `skills/hackathon-pitch/references/presentation-winning.md` | True | # --- Fix 5: multi-* commands — Claude Code-only labels + misleading Cursor fallback --- |
| claude | 13439 | `commands/multi-workflow.md` | False | # --- Fix 6: gan-harness.sh — Claude Code-only header (script shells out to claude -p / claude mcp)  |
| claude | 13448 | `scripts/gan-harness.sh` | False | # --- Fix 7: strategic-compact — adjudicated NOT Claude Code-only --- |
| claude | 13451 | `scripts/gan-harness.sh` | False | # this skill is Claude Code-only was wrong. Label rewritten to say so. |
| claude | 13457 | `skills/strategic-compact/SKILL.md` | True | # --- Fix 8: continuous-learning v1 — weak label; make the Claude Code-only status explicit --- |
| claude | 13475 | `scripts/lib/terminal-welcome.js` | True | # in the previewClaude/applyClaude factories, so each factory is replaced |
| claude | 13728 | `skills/strategic-compact/SKILL.md` | True | # only CLAUDE_PLUGIN_ROOT / ~/.claude — no Cursor fallback. Fix: the shared |
| claude | 15256 | `skills/ui-ux-pro-max/scripts/search.py` | True | #  - D7 (claude-project-scripts-package.json) -- NO CHANGE: the audit premise |
| claude | 15258 | `skills/ui-ux-pro-max/scripts/search.py` | True | #    claude-project.js and must stay. |
| claude | 15359 | `skills/skill-stocktake/SKILL.md` | True | # --- D2: multi-* commands — Claude Code tool names -> Cursor wording --- |
| claude | 15456 | `skills/unified-memory/SKILL.md` | True | # --- D10: gan agents — '(Claude Code only — no Cursor equivalent)' in descriptions --- |
| claude | 16348 | `commands/quality-gate.md` | True | # --- Fixer B (Cleanliness): Claude-Code-only env var / config paths; add the Cursor equivalents (CU |
| claude | 16471 | `commands/setup-pm.md` | True | # --- Fixer B (Cleanliness): skill install paths named .claude/skills/ only; add the Cursor paths (. |
| claude | 17055 | `scripts/lib/harness-adapter-compliance.js` | True | # --- Fixer B (Cleanliness): Claude-Code-only package-manager detection; make it host-aware (CURSOR_ |
| claude | 17402 | `scripts/lib/package-manager.js` | True | # --- Fixer B (Cleanliness): setup script named Claude Code only; host-aware wording and getConfigPa |
| claude | 17557 | `scripts/setup-package-manager.js` | True | # --- Fixer B (Cleanliness): LaraPlugins MCP setup named ~/.claude.json only; Cursor-first with the  |
| claude | 17616 | `skills/laravel-plugin-discovery/SKILL.md` | True | # --- Fixer B (Cleanliness): scan commands named Claude Code paths only; add the Cursor paths. |
| claude | 17674 | `skills/rules-distill/SKILL.md` | True | # --- Fixer B (Cleanliness): 'Claude Code Subagents' heading in a Cursor plugin; Cursor Subagents. |
| claude | 17704 | `skills/santa-method/SKILL.md` | True | # --- Fixer B (Cleanliness): skill search paths named ~/.claude only; check ~/.cursor/skills and the |
| claude | 17976 | `skills/laravel-verification/SKILL.md` | True | # is true in Claude Code (ECC runs post-edit-format.js as a PostToolUse hook |
| claude | 17977 | `skills/laravel-verification/SKILL.md` | True | # there) and the skill is labelled Claude Code-only in its description, but |
| claude | 17979 | `skills/laravel-verification/SKILL.md` | True | # Claude Code-only and name the Cursor equivalent (Audit #11 fixed the |
| claude | 18088 | `agents/ecc-django-build-resolver.md` | True | # --- LOW Cleanliness 1: tdd-workflow — :104 stated a Claude-only |
| claude | 18098 | `skills/tdd-workflow/SKILL.md` | True | # --- LOW Cleanliness 2: nuxt-hooks.mdc — :13 framed the hooks as Claude |
| claude | 18475 | `skills/ecc-recipes/SKILL.md` | True | # names were the upstream Claude Code command set. Reword to stages. |
| claude | 18510 | `skills/opensource-pipeline/SKILL.md` | True | # commands (Claude Code only, not shipped in this plugin). Qualify once up |
| claude | 18633 | `scripts/hooks/posttooluse-dispatcher.js` | True | # adapter is live Cursor hook infrastructure, not a Claude Code-only / |
| claude | 18687 | `commands/evolve.md` | True | # it Claude Code-only / not-wired: every hooks/*.js script does |
| claude | 19027 | `rules/react-testing.mdc` | True | # standard "(Claude Code only — no Cursor equivalent in this plugin)" label |
| claude | 19029 | `rules/react-testing.mdc` | True | # .claude/plans/ and references ECC_HOOK_PROFILE; the hookify commands and |
| claude | 19030 | `rules/react-testing.mdc` | True | # skill name Claude Code explicitly in their bodies. |
| claude | 19125 | `skills/hookify-rules/SKILL.md` | True | # Claude Code-only label, mirroring the 7 labelled unwired PostToolUse |
| claude | 19126 | `skills/hookify-rules/SKILL.md` | True | # scripts. Reads stdin from the Claude Code runtime, registered in |
| claude | 19129 | `skills/hookify-rules/SKILL.md` | True | # Claude Code-only label, mirroring the labelled hookify set. Evaluates |
| claude | 19130 | `skills/hookify-rules/SKILL.md` | True | # rules against Claude Code lifecycle payloads; reachable only from the |
| claude | 19230 | `scripts/hooks/hookify-runtime.js` | True | # Claude Code-only, never run in Cursor, and carried no "Claude Code-only / |
| claude | 19636 | `commands/security-scan.md` | True | # Claude Code PreToolUse/PostToolUse bash-dispatch entry points; Cursor's |
| claude | 22405 | `skills/ui-ux-pro-max/SKILL.md` | True | # B7b gan-style-harness "Via Claude Code (Manual)" section: those commands |
| claude | 22565 | `skills/ui-ux-pro-max/SKILL.md` | True | # 11a gan-style-harness :30: scope the claude -p reference. |
| claude | 22573 | `skills/ui-ux-pro-max/SKILL.md` | True | # 11c gan-style-harness commands: scope each claude -p command in place. |
| claude | 23204 | `skills/ui-ux-pro-max/SKILL.md` | True | # --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic --- |
| codex | 23204 | `skills/ui-ux-pro-max/SKILL.md` | True | # --- fix16: re-pin all model pins to Grok; scrub Claude/Codex/Anthropic --- |
| opus | 151 | `(step-1/2 setup)` | None | # (sonnet/opus/haiku), which are not Cursor model IDs. Map: sonnet -> |
| opus | 152 | `(step-1/2 setup)` | None | # cursor-grok-4.6-high-fast, opus -> grok-4.7-high, haiku -> |
| opus | 210 | `agents` | True | # only the opus bracket pin was removed; cursor-grok-4.6-high-fast remains |

### Class (c1) NEW-side patch text (written into tree mid-build, scrubbed by fix16.py) — 368 hits

| term | build.sh:line | target file | ships? | excerpt |
|---|---|---|---|---|
| anthropic | 12844 | `skills/gan-style-harness/SKILL.md` | True | '---\nname: gan-style-harness\ndescription: "GAN-inspired Generator-Evaluator agent harness for buil |
| claude | 551 | `skills/delivery-gate/SKILL.md` | True | append_desc("agents-md-generator", ". Use ONLY when the user explicitly asks for an AGENTS.md file.  |
| claude | 603 | `skills/delivery-gate/SKILL.md` | True | "description: Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, |
| claude | 945 | `skills/security-scan/SKILL.md` | True | "description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use fo |
| claude | 1036 | `skills/security-scan/SKILL.md` | True | "uv run python -m scripts.run --dry-run ~/.claude/skills/tdd-workflow/SKILL.md", |
| claude | 1548 | `commands/cost-report.md` | False | """Summarize local Claude Code spend by day, model, and session from the metrics |
| claude | 1554 | `commands/cost-report.md` | False | `~/.claude/metrics/costs.jsonl` (Claude Code only — no Cursor equivalent in this plugin). Each row i |
| claude | 1580 | `commands/cost-report.md` | False | 1. Check that `~/.claude/metrics/costs.jsonl` (Claude Code only) exists. If it does not, tell the |
| claude | 2227 | `commands/learn-eval.md` | True | - **Project** (`.claude/skills/<pattern-name>/SKILL.md` in current project): Project-specific knowle |
| claude | 2229 | `commands/learn-eval.md` | True | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| claude | 2252 | `commands/learn-eval.md` | True | `skills/` in this plugin, project `.claude/skills/`, or `MEMORY.md` as |
| claude | 2278 | `commands/learn-eval.md` | True | - [ ] Grep `skills/` in this plugin and relevant project `.claude/skills/` files by keyword to check |
| claude | 2458 | `commands/multi-backend.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2559 | `commands/multi-execute.md` | False | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Mu |
| claude | 2561 | `commands/multi-execute.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2570 | `commands/multi-execute.md` | False | '- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missin |
| claude | 2666 | `commands/multi-execute.md` | False | """/ Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/revie |
| claude | 2746 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| claude | 2751 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/reviewer.md` |
| claude | 2781 | `commands/multi-frontend.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2884 | `commands/multi-plan.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 2912 | `commands/multi-plan.md` | False | - **Code Sovereignty**: External models have **zero filesystem write access**, all modifications by  |
| claude | 2914 | `commands/multi-plan.md` | False | - **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files, |
| claude | 2919 | `commands/multi-plan.md` | False | '- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files |
| claude | 2965 | `commands/multi-plan.md` | False | """/ Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/ar |
| claude | 3007 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| claude | 3024 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/analyzer.md` |
| claude | 3051 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/antigravity/architect.md` |
| claude | 3056 | `commands/multi-plan.md` | False | #### 2.4 Generate Implementation Plan (Claude Final Version) |
| claude | 3080 | `commands/multi-workflow.md` | False | > **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the base  |
| claude | 3089 | `commands/multi-workflow.md` | False | '- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Sp |
| claude | 3164 | `commands/multi-workflow.md` | False | """/ Analysis / `~/.claude/.ccg/prompts/codex/analyzer.md` / `~/.claude/.ccg/prompts/antigravity/ana |
| claude | 3165 | `commands/multi-workflow.md` | False | / Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/archi |
| claude | 3166 | `commands/multi-workflow.md` | False | / Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/reviewer |
| claude | 3283 | `commands/multi-workflow.md` | False | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/ta |
| claude | 3523 | `commands/project-init.md` | True | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gem |
| claude | 3563 | `commands/project-init.md` | True | ## CLAUDE.md Guidance |
| claude | 3565 | `commands/project-init.md` | True | If the user wants a `CLAUDE.md` starter, generate it separately from the installer plan and keep it  |
| claude | 3577 | `commands/project-init.md` | True | Never replace an existing `CLAUDE.md` without showing a diff and receiving approval. |
| claude | 3861 | `commands/santa-loop.md` | False | #### Reviewer A: Claude Agent (always runs) |
| claude | 3869 | `commands/santa-loop.md` | False | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| claude | 3889 | `commands/santa-loop.md` | False | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent  |
| claude | 3940 | `commands/sessions.md` | True | description: Manage Claude Code session history, aliases, and session metadata. |
| claude | 3945 | `commands/sessions.md` | True | Manage Claude Code session history - list, load, alias, and edit sessions stored in `~/.claude/sessi |
| claude | 3969 | `commands/sessions.md` | True | - Sessions are stored as markdown files in `~/.claude/session-data/` with legacy reads from `~/.clau |
| claude | 3970 | `commands/sessions.md` | True | - Aliases are stored in `~/.claude/session-aliases.json` (Claude Code only) |
| claude | 3993 | `commands/skill-create.md` | True | Analyze your repository's git history to extract coding patterns and generate SKILL.md files that te |
| claude | 4134 | `rules/common-git-workflow.mdc` | True | Note: this paragraph describes Claude Code installs and does not apply to this Cursor plugin install |
| claude | 4182 | `rules/common-hooks.mdc` | True | - Configure Cursor permissions in the project's Cursor settings instead of Claude Code's `~/.claude/ |
| claude | 4503 | `skills/ai-regression-testing/SKILL.md` | True | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| claude | 4596 | `skills/browser-qa/SKILL.md` | True | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| claude | 4629 | `skills/ck/SKILL.md` | True | plugin). The commands below refer to the skill directory as `${CLAUDE_SKILL_DIR}`, |
| claude | 4630 | `skills/ck/SKILL.md` | True | which Claude Code fills in; in other hosts, replace it with the absolute path of the |
| claude | 4682 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/init.mjs" |
| claude | 4743 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/resume.mjs" [arg] |
| claude | 4752 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| claude | 4779 | `skills/ck/SKILL.md` | True | """node "${CLAUDE_SKILL_DIR}/commands/info.mjs" [arg] |
| claude | 4787 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/list.mjs" |
| claude | 4798 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| claude | 4814 | `skills/ck/SKILL.md` | True | """node "${CLAUDE_SKILL_DIR}/commands/forget.mjs" [name] |
| claude | 4822 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" |
| claude | 4826 | `skills/ck/SKILL.md` | True | node "${CLAUDE_SKILL_DIR}/commands/migrate.mjs" --dry-run"""), |
| claude | 4840 | `skills/ck/SKILL.md` | True | """unsaved sessions, git activity since last save, and goal mismatches vs CLAUDE.md. |
| claude | 4979 | `skills/config-gc/SKILL.md` | False | description: Garbage collection for your Claude Code configuration (Claude Code only — this skill ta |
| claude | 4984 | `skills/config-gc/SKILL.md` | False | # Config GC — Garbage Collection for Claude Code Setups |
| claude | 5030 | `skills/context-budget/SKILL.md` | True | / Claude Code (Claude Code only) / `/context` / Shows the live context breakdown. Use `/context all` |
| claude | 5033 | `skills/context-budget/SKILL.md` | True | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/c |
| claude | 5051 | `skills/context-budget/SKILL.md` | True | [`/context` and `/usage` commands (Claude Code only; `/cost` is an alias)](https://code.claude.com/d |
| claude | 5108 | `skills/continuous-learning-v2/SKILL.md` | True | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreTool |
| claude | 5110 | `skills/continuous-learning-v2/SKILL.md` | True | **If installed manually** to `~/.claude/skills`, add this to your `~/.claude/settings.json`: |
| claude | 5249 | `skills/council/SKILL.md` | True | Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from this skill. |
| claude | 5350 | `skills/delivery-gate/SKILL.md` | True | Claude Code's built-in checks cover code quality (build → type → lint → test). But there's a differe |
| claude | 5763 | `skills/inherit-legacy-style/SKILL.md` | True | description: Prevent AI style drift on legacy projects by scanning the codebase for implicit convent |
| claude | 5799 | `skills/inherit-legacy-style/SKILL.md` | True | '- **[Golden Files]** — real exemplar paths annotated with what they demonstrate\n- **[Naming & Stat |
| claude | 6202 | `skills/orch-pipeline/SKILL.md` | True | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| claude | 6389 | `skills/santa-method/SKILL.md` | True | ### Pattern A: Claude Code Subagents (Recommended) |
| claude | 6904 | `skills/strategic-compact/SKILL.md` | True | **Installed as a plugin?** No setup is needed. Do not copy the block below into `~/.claude/settings. |
| claude | 6906 | `skills/strategic-compact/SKILL.md` | True | **If installed manually** (`./install.sh`), add to your `~/.claude/settings.json`: |
| claude | 6926 | `skills/strategic-compact/SKILL.md` | True | - `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Claude Code's native auto-compact trigger, which may be smalle |
| claude | 7001 | `skills/tdd-workflow/SKILL.md` | True | It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CLAUDE_PACKAGE_MANAGER`,  |
| claude | 7808 | `skills/ui-ux-pro-max/SKILL.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| claude | 7815 | `skills/ui-ux-pro-max/SKILL.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| claude | 7902 | `skills/ui-ux-pro-max/SKILL.md` | True | 3. Log checkpoint to `.claude/checkpoints.log`: |
| claude | 7905 | `skills/ui-ux-pro-max/SKILL.md` | True | echo "$(date +%Y-%m-%d-%H:%M) / $CHECKPOINT_NAME / $(git rev-parse --short HEAD)" >> .claude/checkpo |
| claude | 8087 | `skills/ui-ux-pro-max/SKILL.md` | True | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 8115 | `skills/ui-ux-pro-max/SKILL.md` | True | **If ace-tool MCP is NOT available**, use Claude Code built-in tools as fallback: |
| claude | 8313 | `skills/ui-ux-pro-max/SKILL.md` | True | """> **Need requirements first?** Use `/plan-prd` for a lean PRD at `.claude/prds/{name}.prd.md`. |
| claude | 8315 | `skills/ui-ux-pro-max/SKILL.md` | True | > **Need the legacy PRP flow?** Use `/prp-plan` for deep PRP planning with `.claude/PRPs/` artifacts |
| claude | 8377 | `skills/ui-ux-pro-max/SKILL.md` | True | Run two independent reviewers (Claude Opus + an external model) against the current task output. Bot |
| claude | 8421 | `skills/ui-ux-pro-max/SKILL.md` | True | #### Reviewer A: Claude Agent (always runs) |
| claude | 8429 | `skills/ui-ux-pro-max/SKILL.md` | True | #### Reviewer B: External Model (Claude fallback if no external reviewer is ready)"""), |
| claude | 8449 | `skills/ui-ux-pro-max/SKILL.md` | True | **Claude Agent fallback:** If the subshell prints `CLAUDE_FALLBACK`, launch a second named subagent  |
| claude | 9495 | `skills/ui-ux-pro-max/SKILL.md` | True | """1. CLAUDE.md (commands, architecture, key files) |
| claude | 9762 | `skills/ui-ux-pro-max/SKILL.md` | True | Match the language reviewer to the repo (see the repo's own `CLAUDE.md`). |
| claude | 11074 | `agents/ecc-opensource-packager.md` | True | description: Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, se |
| claude | 11592 | `commands/astra-review.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| claude | 11598 | `commands/astra-review.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| claude | 11642 | `commands/cost-report.md` | False | description: Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for |
| claude | 11648 | `commands/cost-report.md` | False | Summarize local Claude Code spend by day, model, and session from the metrics"""), |
| claude | 11670 | `commands/evolve.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--gene |
| claude | 11673 | `commands/evolve.md` | True | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| claude | 11722 | `commands/instinct-import.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-o |
| claude | 11725 | `commands/instinct-import.md` | True | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| claude | 11758 | `commands/learn-eval.md` | True | - Use the directory form exactly. Claude Code treats `<name>/SKILL.md` as |
| claude | 11826 | `commands/loop-status.md` | False | description: Inspect active loop state, progress, failure signals, and recommended intervention. (Cl |
| claude | 11864 | `commands/multi-backend.md` | False | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the ba |
| claude | 11888 | `commands/multi-execute.md` | False | description: Execute a multi-model implementation plan while preserving Claude as the only filesyste |
| claude | 11893 | `commands/multi-execute.md` | False | Multi-model collaborative execution - Get prototype from plan → Claude refactors and implements → Mu |
| claude | 11926 | `commands/multi-frontend.md` | False | """> **Prerequisite:** Requires the external `ccg-workflow` runtime, which is **not** part of the ba |
| claude | 11978 | `commands/projects.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" projects |
| claude | 11981 | `commands/projects.md` | True | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| claude | 12012 | `commands/promote.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [insti |
| claude | 12015 | `commands/promote.md` | True | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| claude | 12046 | `commands/prune.md` | True | python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" prune |
| claude | 12049 | `commands/prune.md` | True | Or, relative to the plugin root (manual installation, `CLAUDE_PLUGIN_ROOT` not set): |
| claude | 12070 | `commands/resume-session.md` | True | description: Load the most recent session file from ~/.claude/session-data/ and resume work with ful |
| claude | 12088 | `commands/save-session.md` | True | description: Save current session state to a dated file in ~/.claude/session-data/ so work can be re |
| claude | 12195 | `rules/arkts-hooks.mdc` | True | Run hvigor build to check for ArkTS compilation errors. This was a Claude Code hook block; in Cursor |
| claude | 12199 | `rules/arkts-hooks.mdc` | True | Validate permission and ability declarations. This was a Claude Code hook block; in Cursor, wire it  |
| claude | 12203 | `rules/arkts-hooks.mdc` | True | Reinstall dependencies. This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit`  |
| claude | 12209 | `rules/arkts-hooks.mdc` | True | Warn when code contains V1 state management decorators. This was a Claude Code pre-write hook block; |
| claude | 12358 | `rules/dart-hooks.mdc` | True | The hook configuration below was a Claude Code `settings.json` block. In Cursor, wire the same behav |
| claude | 12378 | `rules/web-hooks.mdc` | True | Use the project's existing formatter entrypoint after edits. This was a Claude Code hook block; in C |
| claude | 12384 | `rules/web-hooks.mdc` | True | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.js |
| claude | 12390 | `rules/web-hooks.mdc` | True | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.js |
| claude | 12404 | `rules/web-hooks.mdc` | True | This was a Claude Code hook block; in Cursor, wire it as an `afterFileEdit` entry in `hooks/hooks.js |
| claude | 12410 | `rules/web-hooks.mdc` | True | Block oversized writes from tool input content, not from a file that may not exist yet. This was a C |
| claude | 12416 | `rules/web-hooks.mdc` | True | This was a Claude Code stop-hook block; the Cursor equivalent is already wired — the `stop` event in |
| claude | 12426 | `scripts/gan-harness.sh` | False | '  phase "PHASE 1: Planning — SKIPPED (spec.md exists)"\nelse\n  phase "PHASE 1: Planning"\n  log "L |
| claude | 12428 | `scripts/gan-harness.sh` | False | '  FEEDBACK_CONTEXT=""\n  if [ $i -gt 1 ] && [ -f "${FEEDBACK_DIR}/feedback-$(printf \'%03d\' $((i-1 |
| claude | 12430 | `scripts/gan-harness.sh` | False | '    fail "Run \'claude mcp get playwright\' to inspect its status, then retry the harness."\n    ex |
| claude | 12737 | `skills/continuous-learning/SKILL.md` | True | """- Reviewing or curating learned skills in `~/.claude/skills/learned/` |
| claude | 12753 | `skills/continuous-learning-v2/agents/observer-loop.sh` | True | '  # slower — consider raising ECC_OBSERVER_TIMEOUT_SECONDS (default 120s) so the watchdog\n  # does |
| claude | 12844 | `skills/gan-style-harness/SKILL.md` | True | '---\nname: gan-style-harness\ndescription: "GAN-inspired Generator-Evaluator agent harness for buil |
| claude | 12886 | `skills/plankton-code-quality/SKILL.md` | True | description: "Write-time code quality enforcement using Plankton — auto-formatting, linting, and Cla |
| claude | 12989 | `skills/skill-comply/SKILL.md` | False | description: Visualize whether skills, rules, and agent definitions are actually followed — auto-gen |
| claude | 13014 | `skills/skill-comply/SKILL.md` | False | uv run python -m scripts.run ~/.claude/rules/common/testing.md |
| claude | 13037 | `skills/strategic-compact/SKILL.md` | True | description: Suggests manual context compaction at logical intervals to preserve context through tas |
| claude | 13082 | `skills/strategic-compact/SKILL.md` | True | **Installed as a plugin?** No setup is needed. Do not copy the block below into your `hooks/hooks.js |
| claude | 13420 | `commands/multi-execute.md` | False | "description: Execute a multi-model implementation plan while preserving Claude as the only filesyst |
| claude | 13430 | `commands/multi-plan.md` | False | "for a single-model plan with no extra runtime use /plan. (Claude Code only — no Cursor equivalent i |
| claude | 13444 | `scripts/gan-harness.sh` | False | # Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in a Cu |
| claude | 13454 | `skills/strategic-compact/SKILL.md` | True | "(Compaction advice that applies in Cursor; originated in Claude Code; the hook example below is in  |
| claude | 13460 | `skills/continuous-learning/SKILL.md` | True | 'description: "[DEPRECATED - Claude Code only, use continuous-learning-v2] Legacy v1 stop-hook skill |
| claude | 13482 | `scripts/lib/multi-harness-setup.js` | False | "    previewClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in t |
| claude | 13486 | `scripts/lib/multi-harness-setup.js` | False | "    applyClaude: () => { throw new Error('multi-harness-setup: scripts/setup/ is not shipped in thi |
| claude | 13537 | `commands/evolve.md` | True | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-lea |
| claude | 13545 | `commands/instinct-import.md` | True | - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-lea |
| claude | 13556 | `commands/instinct-status.md` | True | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learn |
| claude | 13563 | `commands/projects.md` | True | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learn |
| claude | 13570 | `commands/promote.md` | True | Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `skills/continuous-learn |
| claude | 13575 | `commands/sessions.md` | True | """description: Manage Claude Code session history, aliases, and session metadata. (Claude Code only |
| claude | 13813 | `scripts/lib/resolve-ecc-root.js` | True | """ *   4. Plugin cache auto-detection — scans ~/.claude/plugins/cache/{ecc,everything-claude-code}/ |
| claude | 13817 | `scripts/lib/resolve-ecc-root.js` | True | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| claude | 13818 | `scripts/lib/resolve-ecc-root.js` | True | *   6. Fallback to ~/.claude/ (original behaviour)"""), |
| claude | 13835 | `scripts/lib/resolve-ecc-root.js` | True | const cacheBase = path.join(claudeDir, 'plugins', 'cache', slug); |
| claude | 13850 | `scripts/lib/resolve-ecc-root.js` | True | // is no ~/.claude and no CLAUDE_PLUGIN_ROOT, so all the probing above |
| claude | 13859 | `scripts/lib/resolve-ecc-root.js` | True | return claudeDir; |
| claude | 13868 | `scripts/lib/resolve-ecc-root.js` | True | """ * When CLAUDE_PLUGIN_ROOT is set (as Claude Code does for plugin hooks and |
| claude | 13870 | `scripts/lib/resolve-ecc-root.js` | True | * locations resolveEccRoot() knows about — ~/.claude, the exact plugin roots |
| claude | 13871 | `scripts/lib/resolve-ecc-root.js` | True | * under ~/.claude/plugins/, and the versioned plugin cache — then, as an |
| claude | 13874 | `scripts/lib/resolve-ecc-root.js` | True | * so it also finds the plugin in a Cursor install with no ~/.claude. Only |
| claude | 13875 | `scripts/lib/resolve-ecc-root.js` | True | * then does it fall back to ~/.claude. The Cursor scan tests candidates |
| claude | 13877 | `scripts/lib/resolve-ecc-root.js` | True | * ~/.claude-first for any directory the module loads from."""), |
| claude | 13907 | `scripts/lib/resolve-ecc-root.js` | True | // resolver's ~/.claude-first answer for any directory the module loads |
| claude | 13974 | `scripts/lib/resolve-ecc-root.js` | True | new = '''for candidate in "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/scripts/astra-review.js" \\ |
| claude | 13976 | `scripts/lib/resolve-ecc-root.js` | True | "./.claude/scripts/astra-review.js" \\''' |
| claude | 14207 | `scripts/lib/harness-adapter-compliance.js` | True | // rules/common/, .claude-plugin/plugin.json, |
| claude | 14222 | `skills/ck/SKILL.md` | True | r'''or picking up a project without re-explaining it. (Claude Code only — this skill uses Claude Cod |
| claude | 14228 | `skills/ck/SKILL.md` | True | > **Claude Code only** — this skill uses Claude Code's SessionStart hook and ~/.claude/ck storage; i |
| claude | 14239 | `scripts/lib/llm-summary.js` | False | * Claude Code only: the `claude` CLI does not exist under Cursor, so |
| claude | 14262 | `scripts/lib/llm-summary.js` | False | * True only when a `claude` executable is findable on PATH. Pure filesystem |
| claude | 14263 | `scripts/lib/llm-summary.js` | False | * check (no subprocess): under Cursor there is no `claude` binary, so the |
| claude | 14266 | `scripts/lib/llm-summary.js` | False | function claudeCliAvailable() { |
| claude | 14267 | `scripts/lib/llm-summary.js` | False | const names = process.platform === 'win32' ? ['claude.cmd', 'claude.exe', 'claude'] : ['claude']; |
| claude | 14285 | `scripts/lib/llm-summary.js` | False | // Claude Code only: skip the doomed `claude -p` spawn when the binary is |
| claude | 14287 | `scripts/lib/llm-summary.js` | False | if (!claudeCliAvailable()) { |
| claude | 14288 | `scripts/lib/llm-summary.js` | False | onSkip('claude CLI not available (not running under Claude Code)'); |
| claude | 14295 | `scripts/lib/llm-summary.js` | False | r"""module.exports = { generateSessionSummary, extractConversationText, getContextRemainingPct, getC |
| claude | 14669 | `skills/continuous-learning-v2/SKILL.md` | True | r"""- Existing global instincts can be migrated from `~/.claude/homunculus/instincts/` with `skills/ |
| claude | 15418 | `scripts/lib/resolve-ecc-root.js` | True | *      finds the plugin in a Cursor install, where ~/.claude does not exist) |
| claude | 15419 | `scripts/lib/resolve-ecc-root.js` | True | *   7. Fallback to ~/.claude/ (original behaviour)"""), |
| claude | 15459 | `agents/ecc-gan-evaluator.md` | True | r'''description: "GAN Harness — Evaluator agent. Tests the live running application via Playwright,  |
| claude | 15463 | `agents/ecc-gan-generator.md` | True | r'''description: "GAN Harness — Generator agent. Implements features according to the spec, reads ev |
| claude | 15467 | `agents/ecc-gan-planner.md` | True | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specifi |
| claude | 15628 | `scripts/lib/harness-adapter-compliance.js` | True | r'''      'canonical ECC agents (agents/) portable via scripts/agent-convert.js (not shipped in this |
| claude | 15844 | `rules/web-hooks.mdc` | True | r'''Block oversized writes from tool input content, not from a file that may not exist yet. This was |
| claude | 15846 | `rules/web-hooks.mdc` | True | r'''This was a Claude Code stop-hook block; it is NOT wired in this plugin. The `stop` event in `hoo |
| claude | 16269 | `agents/ecc-code-reviewer.md` | True | When available, also check project-specific conventions from `CLAUDE.md` or project rules: |
| claude | 16380 | `commands/setup-pm.md` | True | 1. **Environment variable**: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude C |
| claude | 16381 | `commands/setup-pm.md` | True | 2. **Project config**: `.cursor/package-manager.json`, then `.claude/package-manager.json` |
| claude | 16384 | `commands/setup-pm.md` | True | 5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.json` in Cursor, `~/.cl |
| claude | 16393 | `commands/setup-pm.md` | True | // Claude Code: ~/.claude/package-manager.json |
| claude | 16420 | `commands/setup-pm.md` | True | // (an existing .claude/package-manager.json is still honoured on read) |
| claude | 16453 | `commands/setup-pm.md` | True | Set `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Claude |
| claude | 16492 | `commands/skill-create.md` | True | `.cursor/skills/` in Cursor (this plugin's host) or `.claude/skills/` in |
| claude | 16493 | `commands/skill-create.md` | True | Claude Code; a global skill uses `~/.cursor/skills/` or `~/.claude/skills/`. |
| claude | 16933 | `manifests/install-modules.json` | True | "claude", |
| claude | 16934 | `manifests/install-modules.json` | True | "claude-project", |
| claude | 17076 | `scripts/lib/package-manager.js` | True | const { commandExists, getClaudeDir, getHomeDir, readFile, writeFile } = require('./utils'); |
| claude | 17115 | `scripts/lib/package-manager.js` | True | // ~/.claude in Claude Code — see scripts/lib/agent-data-home.js) |
| claude | 17117 | `scripts/lib/package-manager.js` | True | return path.join(getClaudeDir(), 'package-manager.json'); |
| claude | 17127 | `scripts/lib/package-manager.js` | True | function getClaudeGlobalConfigPath() { |
| claude | 17128 | `scripts/lib/package-manager.js` | True | return path.join(getHomeDir(), '.claude', 'package-manager.json'); |
| claude | 17134 | `scripts/lib/package-manager.js` | True | * (~/.cursor/package-manager.json) and Claude Code |
| claude | 17135 | `scripts/lib/package-manager.js` | True | * (~/.claude/package-manager.json) global paths. |
| claude | 17141 | `scripts/lib/package-manager.js` | True | getClaudeGlobalConfigPath() |
| claude | 17177 | `scripts/lib/package-manager.js` | True | *    CLAUDE_PACKAGE_MANAGER (Claude Code) |
| claude | 17179 | `scripts/lib/package-manager.js` | True | *    .claude/package-manager.json) |
| claude | 17183 | `scripts/lib/package-manager.js` | True | *    ~/.cursor/package-manager.json, then ~/.claude/package-manager.json) |
| claude | 17210 | `scripts/lib/package-manager.js` | True | // 1. Check environment variable (Cursor first, then Claude Code) |
| claude | 17211 | `scripts/lib/package-manager.js` | True | const envPm = process.env.CURSOR_PACKAGE_MANAGER // process.env.CLAUDE_PACKAGE_MANAGER; |
| claude | 17251 | `scripts/lib/package-manager.js` | True | // 2. Check project-specific config (.cursor first, then .claude) |
| claude | 17252 | `scripts/lib/package-manager.js` | True | for (const configDir of ['.cursor', '.claude']) { |
| claude | 17295 | `scripts/lib/package-manager.js` | True | * ~/.claude/package-manager.json in Claude Code. A preference saved at |
| claude | 17296 | `scripts/lib/package-manager.js` | True | * ~/.cursor/package-manager.json or ~/.claude/package-manager.json is still |
| claude | 17332 | `scripts/lib/package-manager.js` | True | * existing .claude/package-manager.json is still honoured on read as a |
| claude | 17333 | `scripts/lib/package-manager.js` | True | * fallback for Claude Code installs (see getPackageManager step 2). |
| claude | 17367 | `scripts/lib/package-manager.js` | True | message += '  - Global: Set CURSOR_PACKAGE_MANAGER (Cursor) or CLAUDE_PACKAGE_MANAGER (Claude Code)  |
| claude | 17368 | `scripts/lib/package-manager.js` | True | message += '  - Or add to ~/.cursor/package-manager.json or ~/.claude/package-manager.json: {"packag |
| claude | 17456 | `scripts/setup-package-manager.js` | True | Package Manager Setup for Cursor (also works in Claude Code) |
| claude | 17465 | `scripts/setup-package-manager.js` | True | ~/.claude/package-manager.json in Claude Code; |
| claude | 17468 | `scripts/setup-package-manager.js` | True | an existing .claude/package-manager.json is still honoured) |
| claude | 17494 | `scripts/setup-package-manager.js` | True | console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER // process.env.CLAUDE_PACKAGE_M |
| claude | 17521 | `scripts/setup-package-manager.js` | True | console.log('  (Also read from ~/.cursor/package-manager.json and ~/.claude/package-manager.json)'); |
| claude | 17548 | `scripts/setup-package-manager.js` | True | console.log('  (An existing .claude/package-manager.json is still honoured on read)'); |
| claude | 17606 | `skills/laravel-plugin-discovery/SKILL.md` | True | In Claude Code, add the same entry to your `~/.claude.json` `mcpServers` |
| claude | 17651 | `skills/rules-distill/SKILL.md` | True | Claude Code (this skill also works there): |
| claude | 17654 | `skills/rules-distill/SKILL.md` | True | bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh |
| claude | 17665 | `skills/rules-distill/SKILL.md` | True | Claude Code: |
| claude | 17668 | `skills/rules-distill/SKILL.md` | True | bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh |
| claude | 17730 | `skills/skill-scout/SKILL.md` | True | # Claude Code (this skill also works there) — same searches under ~/.claude |
| claude | 17731 | `skills/skill-scout/SKILL.md` | True | find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null / grep -iE "keyword/synonym" |
| claude | 17732 | `skills/skill-scout/SKILL.md` | True | find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null / grep -iE "keyword/syno |
| claude | 17750 | `skills/skill-scout/SKILL.md` | True | r'''find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null / grep -iE "keyword/ |
| claude | 17756 | `skills/skill-scout/SKILL.md` | True | grep -RilE "keyword/synonym" ~/.cursor/skills ~/.cursor/plugins/marketplaces ~/.claude/skills ~/.cla |
| claude | 17825 | `skills/continuous-learning-v2/SKILL.md` | True | r'''/ Observation / Stop hook (session end) / PreToolUse/PostToolUse (Claude Code only) /'''), |
| claude | 17827 | `skills/continuous-learning-v2/SKILL.md` | True | r'''      / Claude Code hooks capture prompts + tool use (Claude Code only)'''), |
| claude | 17839 | `skills/continuous-learning-v2/SKILL.md` | True | **In Claude Code, if installed as a plugin** (recommended): |
| claude | 17843 | `skills/continuous-learning-v2/SKILL.md` | True | If you previously copied `observe.sh` into `~/.claude/settings.json`, remove that duplicate `PreTool |
| claude | 17845 | `skills/continuous-learning-v2/SKILL.md` | True | r'''**If installed manually in Claude Code** to `~/.claude/skills`, add this to your `~/.claude/sett |
| claude | 17850 | `skills/continuous-learning-v2/SKILL.md` | True | r'''In Claude Code, hooks fire on every tool call, deterministically. This means: |
| claude | 17861 | `commands/learn.md` | True | r'''continuous-learning-v2 is a separate, configurable Stop/PreToolUse/PostToolUse hook-observation  |
| claude | 17876 | `skills/verification-loop/SKILL.md` | True | r'''This skill complements manual review (and, in Claude Code, PostToolUse hooks) but provides deepe |
| claude | 17883 | `rules/dart-hooks.mdc` | True | r'''The bullets below describe the intended Dart hook behaviour (originally a Claude Code `settings. |
| claude | 17913 | `agents/ecc-opensource-packager.md` | True | r'''See `CLAUDE.md` (generated in the target repo) for detailed commands and architecture.'''), |
| claude | 17984 | `skills/plankton-code-quality/SKILL.md` | True | r'''/ Code quality enforcement / PostToolUse hooks (Prettier, tsc) — Claude Code only; in Cursor, po |
| claude | 18095 | `skills/tdd-workflow/SKILL.md` | True | r'''It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSOR_PACKAGE_MANAGE |
| claude | 18106 | `rules/nuxt-hooks.mdc` | True | r'''These were Claude Code harness hooks for Nuxt work; in Cursor, wire them as `afterFileEdit` entr |
| claude | 18492 | `skills/opensource-pipeline/SKILL.md` | True | r'''/ `package PROJECT` / Generate CLAUDE.md + setup.sh + README /'''), |
| claude | 18517 | `commands/multi-plan.md` | False | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow run |
| claude | 18527 | `commands/multi-plan.md` | False | r'''/multi-execute .claude/plan/actual-feature-name.md'''), |
| claude | 18533 | `commands/multi-plan.md` | False | r'''/multi-execute .claude/plan/<feature-name>.md'''), |
| claude | 18544 | `commands/multi-execute.md` | False | > **Note on `/ccg:*` names below:** `/ccg:plan` and `/ccg:execute` are the external ccg-workflow run |
| claude | 18552 | `commands/multi-execute.md` | False | r'''/multi-execute .claude/plan/feature-name.md'''), |
| claude | 18578 | `scripts/hooks/post-edit-typecheck.js` | True | r''' * Claude Code-only PostToolUse hook: TypeScript check after editing .ts/.tsx files (not wired i |
| claude | 18580 | `scripts/hooks/post-edit-typecheck.js` | True | r''' * Runs after Edit tool use on TypeScript files in Claude Code. Walks up from the file's'''), |
| claude | 18590 | `scripts/hooks/ecc-context-monitor.js` | True | r''' * ECC Context Monitor — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cu |
| claude | 18594 | `scripts/hooks/ecc-metrics-bridge.js` | True | r''' * ECC Metrics Bridge — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cur |
| claude | 18598 | `scripts/hooks/governance-capture.js` | True | r''' * Claude Code-only PreToolUse/PostToolUse hook (not wired in this Cursor plugin) that detects g |
| claude | 18602 | `scripts/hooks/session-activity-tracker.js` | True | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin) that records sanitized pe |
| claude | 18606 | `scripts/hooks/skill-run-tracker.js` | True | r''' * Claude Code-only PostToolUse hook (not wired in this Cursor plugin): record Skill tool invoca |
| claude | 18611 | `scripts/hooks/posttooluse-dispatcher.js` | True | r''' * Claude Code-only: consolidates PostToolUse hooks into one synchronous and one asynchronous |
| claude | 18702 | `hooks/adapter.js` | True | * is live infrastructure — not a Claude Code-only or unwired script. |
| claude | 19064 | `commands/loop-start.md` | True | r'''with safety gates before starting one. (Claude Code only — no Cursor equivalent in this plugin)' |
| claude | 19070 | `commands/hookify.md` | True | r'''for authoring or editing rules directly. (Claude Code only — no Cursor equivalent in this plugin |
| claude | 19074 | `commands/hookify-configure.md` | True | r'''description: Enable or disable hookify rules interactively (Claude Code only — no Cursor equival |
| claude | 19078 | `commands/hookify-list.md` | True | r'''description: List all configured hookify rules (Claude Code only — no Cursor equivalent in this  |
| claude | 19082 | `commands/hookify-help.md` | True | r'''description: Get help with the hookify system (Claude Code only — no Cursor equivalent in this p |
| claude | 19086 | `skills/hookify-rules/SKILL.md` | True | r'''such as blocking dangerous commands, .env edits, or debug code. (Claude Code only — no Cursor eq |
| claude | 19193 | `scripts/hooks/ecc-statusline.js` | True | r''' * ECC Statusline — Claude Code-only statusLine command (not wired in this Cursor plugin — regis |
| claude | 19199 | `scripts/hooks/hookify-runtime.js` | True | r''' * ECC-native Hookify runtime — Claude Code-only (not wired in this Cursor plugin — reachable on |
| claude | 19264 | `scripts/hooks/mcp-health-check.js` | True | r''' * MCP health-check hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no Pre |
| claude | 19268 | `scripts/hooks/doc-file-warning.js` | True | r''' * Doc file warning hook (PreToolUse - Write) — Claude Code-only (not wired in this Cursor plugi |
| claude | 19272 | `scripts/hooks/config-protection.js` | True | r''' * Config Protection Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no Pr |
| claude | 19276 | `scripts/hooks/desktop-notify.js` | True | r''' * Desktop Notification Hook (Stop) — Claude Code-only (not wired in this Cursor plugin — Cursor |
| claude | 19280 | `scripts/hooks/pre-bash-commit-quality.js` | True | r''' * PreToolUse Hook: Pre-commit Quality Check — Claude Code-only (not wired in this Cursor plugin |
| claude | 19284 | `scripts/hooks/pre-write-doc-warn.js` | True | r''' * Backward-compatible doc warning hook entrypoint — Claude Code-only (not wired in this Cursor  |
| claude | 19288 | `scripts/hooks/auto-tmux-dev.js` | True | r''' * Auto-Tmux Dev Hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no PreToo |
| claude | 19292 | `scripts/hooks/context-prompt-suggestions.js` | True | r''' * UserPromptSubmit hook — Claude Code-only (not wired in this Cursor plugin — Cursor has no Use |
| claude | 19296 | `scripts/hooks/plan-canvas-pending.js` | True | r''' * Plan Canvas undelivered-feedback guard (Stop) — Claude Code-only (not wired in this Cursor pl |
| claude | 19300 | `scripts/hooks/plan-canvas-sessions.js` | True | r''' * Plan Canvas open-session surfacing (SessionStart) — Claude Code-only (not wired in this Curso |
| claude | 19304 | `scripts/hooks/gateguard-fact-force.js` | True | r''' * PreToolUse Hook: GateGuard Fact-Forcing Gate — Claude Code-only (not wired in this Cursor plu |
| claude | 19308 | `scripts/hooks/insaits-security-wrapper.js` | True | r''' * InsAIts Security Monitor — Claude Code-only wrapper for run-with-flags compatibility (not wir |
| claude | 19312 | `scripts/hooks/session-start-bootstrap.js` | True | r''' * Bootstrap loader for the ECC SessionStart hook — Claude Code-only (not wired in this Cursor p |
| claude | 19321 | `scripts/hooks/pre-bash-git-push-reminder.js` | True | * Git push reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has |
| claude | 19330 | `scripts/hooks/pre-bash-tmux-reminder.js` | True | * Tmux reminder — Claude Code-only PreToolUse hook (not wired in this Cursor plugin — Cursor has no  |
| claude | 19339 | `scripts/hooks/post-bash-build-complete.js` | True | * Build-complete notifier — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cur |
| claude | 19348 | `scripts/hooks/post-bash-command-log.js` | True | * Command logger — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor has n |
| claude | 19357 | `scripts/hooks/post-bash-pr-created.js` | True | * PR-created handler — Claude Code-only PostToolUse hook (not wired in this Cursor plugin — Cursor h |
| claude | 19366 | `scripts/hooks/check-hook-enabled.js` | True | * Hook-enabled check — Claude Code-only helper (not wired in this Cursor plugin — invoked only from  |
| claude | 19375 | `scripts/hooks/lifecycle-hook-bootstrap.js` | True | * Lifecycle hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no lifec |
| claude | 19384 | `scripts/hooks/plugin-hook-bootstrap.js` | True | * Plugin hook bootstrap — Claude Code-only (not wired in this Cursor plugin — Cursor has no hook eve |
| claude | 19670 | `scripts/hooks/pre-bash-dispatcher.js` | True | * Claude Code-only: PreToolUse bash-dispatch entry point (runPreBash). |
| claude | 19680 | `scripts/hooks/post-bash-dispatcher.js` | True | * Claude Code-only: PostToolUse bash-dispatch entry point (runPostBash). |
| claude | 19689 | `scripts/hooks/run-with-flags-shell.sh` | True | # Claude Code-only: shell counterpart of run-with-flags.js (not wired in this Cursor plugin — it nev |
| claude | 22054 | `manifests/install-modules.json` | True | - `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome) |
| claude | 22388 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Cl |
| claude | 22392 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Cursor subagent — launched by `/gan-build` / `/gan-design`; the upstream `claude -p` path is Cl |
| claude | 22396 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''(Cursor subagent — launched by `/gan-build`; the upstream `claude -p` path is Claude Code only a |
| claude | 22404 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''Use when a feature should be built autonomously through generator and evaluator iteration until  |
| claude | 22412 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''### Via Claude Code (Manual) |
| claude | 22414 | `skills/ui-ux-pro-max/SKILL.md` | True | > In this plugin these `claude -p` commands are NOT executed — the loop runs in Cursor via `/gan-bui |
| claude | 22568 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''- Quick single-file fixes (Claude Code only — use standard `claude -p` there; in this plugin use |
| claude | 22572 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''### Via Claude Code (Manual — Claude Code only, never executed in this plugin)'''), |
| claude | 22592 | `skills/ui-ux-pro-max/SKILL.md` | True | # Claude Code only — never executed in this plugin; upstream documentation only. |
| claude | 22593 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Product Planner. Read PLANNER_PROMPT.md. Expand this brief into  |
| claude | 22596 | `skills/ui-ux-pro-max/SKILL.md` | True | # Claude Code only — never executed in this plugin; upstream documentation only. |
| claude | 22597 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Generator. Read spec.md. Implement Sprint 1. Start the dev serve |
| claude | 22600 | `skills/ui-ux-pro-max/SKILL.md` | True | # Claude Code only — never executed in this plugin; upstream documentation only. |
| claude | 22601 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet --allowedTools "Read,Bash,mcp__playwright__*" "You are an Evaluator. Read E |
| claude | 22604 | `skills/ui-ux-pro-max/SKILL.md` | True | # Claude Code only — never executed in this plugin; upstream documentation only. |
| claude | 22605 | `skills/ui-ux-pro-max/SKILL.md` | True | claude -p --model sonnet "You are a Generator. Read spec.md and feedback-001.md. Address all issues. |
| claude | 22612 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''# Claude Code only — this script shells out to 'claude -p' and 'claude mcp'; it will not run in  |
| claude | 22645 | `skills/ui-ux-pro-max/SKILL.md` | True | r'''description: "GAN Harness — Planner agent. Expands a one-line prompt into a full product specifi |
| codex | 2456 | `commands/multi-backend.md` | False | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| codex | 2570 | `commands/multi-execute.md` | False | '- **Prerequisite**: Only execute after user explicitly replies "Y" to `/ccg:plan` output (if missin |
| codex | 2666 | `commands/multi-execute.md` | False | """/ Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/revie |
| codex | 2701 | `commands/multi-execute.md` | False | 4. **Codex is backend logic authority, leverage its logical reasoning and debug capabilities** |
| codex | 2702 | `commands/multi-execute.md` | False | 5. If plan contains `CODEX_SESSION`: prefer `resume <CODEX_SESSION>` |
| codex | 2708 | `commands/multi-execute.md` | False | - Codex: Handle backend part |
| codex | 2743 | `commands/multi-execute.md` | False | **After changes take effect, MUST immediately parallel call** Codex and Antigravity for Code Review: |
| codex | 2745 | `commands/multi-execute.md` | False | 1. **Codex Review** (run in parallel): |
| codex | 2746 | `commands/multi-execute.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/reviewer.md` |
| codex | 2759 | `commands/multi-execute.md` | False | 1. Synthesize Codex + Antigravity review feedback |
| codex | 2760 | `commands/multi-execute.md` | False | 2. Weigh by trust rules: Backend follows Codex, Frontend follows Antigravity |
| codex | 2911 | `commands/multi-plan.md` | False | - **Mandatory Parallel**: Codex/Antigravity calls MUST run in parallel (including single model calls |
| codex | 2919 | `commands/multi-plan.md` | False | '- **Planning Only**: This command allows reading context and writing to `.claude/plan/*` plan files |
| codex | 2965 | `commands/multi-plan.md` | False | """/ Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/ar |
| codex | 3002 | `commands/multi-plan.md` | False | **Parallel call** Codex and Antigravity (run them in parallel): |
| codex | 3006 | `commands/multi-plan.md` | False | 1. **Codex Backend Analysis**: |
| codex | 3007 | `commands/multi-plan.md` | False | - ROLE_FILE: `~/.claude/.ccg/prompts/codex/analyzer.md` |
| codex | 3028 | `commands/multi-plan.md` | False | Wait for both models' complete results (their returned output). **Save SESSION_ID** (`CODEX_SESSION` |
| codex | 3078 | `commands/multi-workflow.md` | False | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Re |
| codex | 3089 | `commands/multi-workflow.md` | False | '- **Claude (self)** – Orchestration, planning, execution, delivery\n\n---\n\n## Multi-Model Call Sp |
| codex | 3164 | `commands/multi-workflow.md` | False | """/ Analysis / `~/.claude/.ccg/prompts/codex/analyzer.md` / `~/.claude/.ccg/prompts/antigravity/ana |
| codex | 3165 | `commands/multi-workflow.md` | False | / Planning / `~/.claude/.ccg/prompts/codex/architect.md` / `~/.claude/.ccg/prompts/antigravity/archi |
| codex | 3166 | `commands/multi-workflow.md` | False | / Review / `~/.claude/.ccg/prompts/codex/reviewer.md` / `~/.claude/.ccg/prompts/antigravity/reviewer |
| codex | 3250 | `commands/multi-workflow.md` | False | - Codex: Use analyzer prompt, output technical feasibility, solutions, risks |
| codex | 3253 | `commands/multi-workflow.md` | False | Wait for their returned output. **Save SESSION_ID** (`CODEX_SESSION` and `ANTIGRAVITY_SESSION`). |
| codex | 3276 | `commands/multi-workflow.md` | False | - Codex: Use architect prompt + `resume $CODEX_SESSION`, output backend architecture |
| codex | 3283 | `commands/multi-workflow.md` | False | **Claude Synthesis**: Adopt Codex backend plan + Antigravity frontend plan, save to `.claude/plan/ta |
| codex | 3302 | `commands/multi-workflow.md` | False | - Codex: Use reviewer prompt, focus on security, performance, error handling |
| codex | 3523 | `commands/project-init.md` | True | 1. Identify the target harness. Default to `claude` unless the user asks for `cursor`, `codex`, `gem |
| codex | 4503 | `skills/ai-regression-testing/SKILL.md` | True | - AI agent (Claude Code, Cursor, Codex) has modified API routes or backend logic |
| codex | 5028 | `skills/context-budget/SKILL.md` | True | / Codex CLI (Codex only) / `/status` / Shows current token usage and remaining context capacity. Use |
| codex | 5029 | `skills/context-budget/SKILL.md` | True | / Codex app (Codex only) / `/status` / Shows current thread context usage and rate limits. / |
| codex | 5033 | `skills/context-budget/SKILL.md` | True | These commands are documented in the [Codex command reference](https://developers.openai.com/codex/c |
| codex | 7808 | `skills/ui-ux-pro-max/SKILL.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| codex | 7815 | `skills/ui-ux-pro-max/SKILL.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| codex | 7827 | `skills/ui-ux-pro-max/SKILL.md` | True | - Codex CLI installed and logged in with ChatGPT: `codex login` |
| codex | 7828 | `skills/ui-ux-pro-max/SKILL.md` | True | - `gpt-6-astra` available on the account (check with `codex` model picker; override with `ECC_ASTRA_ |
| codex | 7872 | `skills/ui-ux-pro-max/SKILL.md` | True | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP  |
| codex | 7874 | `skills/ui-ux-pro-max/SKILL.md` | True | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review hap |
| codex | 7876 | `skills/ui-ux-pro-max/SKILL.md` | True | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without c |
| codex | 11592 | `commands/astra-review.md` | True | description: Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cro |
| codex | 11598 | `commands/astra-review.md` | True | Cross-provider second opinion. Claude writes the code; GPT-6-Astra (OpenAI, running through the loca |
| codex | 11624 | `commands/astra-review.md` | True | - Web search is disabled for the reviewer, the user-level Codex config is not loaded, and every MCP  |
| codex | 11626 | `commands/astra-review.md` | True | - If Codex is missing, fall back to `/code-review` and say clearly that no cross-provider review hap |
| codex | 11628 | `commands/astra-review.md` | True | - `--fix-findings` cannot be combined with a scope flag. `--dry-run` prints the fix prompt without c |
| codex | 11849 | `commands/multi-backend.md` | False | Backend-focused workflow (Research → Ideation → Plan → Execute → Optimize → Review), Codex-led. |
| codex | 11876 | `commands/multi-backend.md` | False | - Codex-led, Gemini for auxiliary reference"""), |
| codex | 11938 | `commands/multi-frontend.md` | False | - Antigravity-led, Codex for auxiliary reference"""), |
| codex | 11955 | `commands/multi-workflow.md` | False | Multi-model collaborative development workflow (Research → Ideation → Plan → Execute → Optimize → Re |
| codex | 13583 | `scripts/ci/validate-skill-host-compat.js` | False | *      .agents/skills/, or a Codex/Cursor copy name: does not match its |
| codex | 16937 | `manifests/install-modules.json` | True | "codex", |
| opus | 6925 | `skills/strategic-compact/SKILL.md` | True | - `ECC_CONTEXT_WINDOW_TOKENS` — Explicit context-window size, in tokens, overriding auto-detection.  |
| opus | 8377 | `skills/ui-ux-pro-max/SKILL.md` | True | Run two independent reviewers (Claude Opus + an external model) against the current task output. Bot |

### Class (c2) staged file write (heredoc into built tree, scrubbed by fix16.py) — 1 hits

| term | build.sh:line | target file | ships? | excerpt |
|---|---|---|---|---|
| claude | 18296 | `schemas/cursor-hooks.schema.json (heredoc)` | False | "description": "Configuration for Cursor hooks, as shipped in hooks/hooks.json. Cursor format: camel |

### Class (c3) build-time source path (copy source, not shipped text) — 2 hits

| term | build.sh:line | target file | ships? | excerpt |
|---|---|---|---|---|
| claude | 265 | `agents` | True | cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max" "$PLUGIN_DIR/skills/ui-ux-pro-max" |
| claude | 298 | `agents` | True | cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch" "$PLUGIN_DIR/skills/hackathon-pitch" |

## Appendix B — staged-source hits, checks 2/3/4 (59 unique lines)

Every unique (file,line) hit by `claude` / `codex` / `anthropic` (case-insensitive) across `new-skills/` + `round2-skills/` (`less-flat-ui/` is 0). Built-tree counterparts are all clean; the 'built' column states what the built copy says instead (or that the built file was verified 0-hit). Excerpts cut at 150 chars.

| file:line | terms | excerpt |
|---|---|---|
| `new-skills/design-taste-frontend/SKILL.md:415` | claude | This skill was written for Claude Code. In this Cursor plugin the finish gate does not auto-run on stop (the Claude Code `Stop` hook was removed from … |
| `new-skills/design-taste-frontend/SKILL.md:419` | claude | Taste skill (design-taste-frontend, v2.5.1) by Leonxlnx, MIT licensed. Source: https://github.com/Leonxlnx/taste-skill. Included in hackathon-ecc with… |
| `new-skills/design-taste-frontend/assets/icons/demo.html:48` | claude,codex,anthropic | <h3 class="demo-h">AI <span class="muted">53</span></h3><div class="ic-chip-row demo-chips"><span class="ic-chip" title="gemini"><img class="ic ic-24"… |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:194` | anthropic | "file": "anthropic.svg", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:195` | anthropic | "icon": "logos:anthropic-icon", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:196` | anthropic | "name": "Anthropic", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:203` | anthropic | "markUrl": "https://www.anthropic.com/" |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:708` | claude | "file": "claude-code.svg", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:709` | claude | "icon": "logos:claude-code", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:710` | claude | "name": "Claude Code", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:717` | claude | "markUrl": "https://claude.com/product/claude-code" |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:720` | claude | "file": "claude.svg", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:721` | claude | "icon": "logos:claude-icon", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:722` | claude | "name": "Claude", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:729` | claude | "markUrl": "https://claude.ai/" |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:816` | codex | "file": "codex.svg", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:817` | codex | "icon": "logos:codex", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:818` | codex | "name": "Codex", |
| `new-skills/design-taste-frontend/assets/icons/demo/icons-credits.json:825` | codex | "markUrl": "https://openai.com/codex/" |
| `new-skills/design-taste-frontend/assets/icons/index.json:772` | anthropic | "id": "anthropic", |
| `new-skills/design-taste-frontend/assets/icons/index.json:773` | anthropic | "name": "Anthropic", |
| `new-skills/design-taste-frontend/assets/icons/index.json:774` | anthropic | "icon": "logos:anthropic-icon", |
| `new-skills/design-taste-frontend/assets/icons/index.json:781` | claude | "id": "claude", |
| `new-skills/design-taste-frontend/assets/icons/index.json:782` | claude | "name": "Claude", |
| `new-skills/design-taste-frontend/assets/icons/index.json:783` | claude | "icon": "logos:claude-icon", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1373` | claude | "id": "claude-code", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1374` | claude | "name": "Claude Code", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1375` | claude | "icon": "logos:claude-code", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1392` | codex | "id": "codex", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1393` | codex | "name": "Codex", |
| `new-skills/design-taste-frontend/assets/icons/index.json:1394` | codex | "icon": "logos:codex", |
| `new-skills/design-taste-frontend/assets/icons/index.json:7964` | anthropic | "logos:anthropic-icon": [ |
| `new-skills/design-taste-frontend/assets/icons/index.json:7970` | claude | "logos:claude-icon": [ |
| `new-skills/design-taste-frontend/assets/icons/index.json:8348` | claude | "logos:claude-code": [ |
| `new-skills/design-taste-frontend/assets/icons/index.json:8360` | codex | "logos:codex": [ |
| `new-skills/design-taste-frontend/assets/layout/heroes.json:636` | anthropic | "from": "Anthropic, Stripe Press, Mercury, private banks and advisers", |
| `new-skills/design-taste-frontend/references/gate.md:136` | claude | In Claude Code the skill's own frontmatter adds the gate as a Stop hook once the skill is invoked. The |
| `new-skills/design-taste-frontend/references/gate.md:138` | claude | `gate.mjs` it finds, in this order: `$CLAUDE_SKILL_DIR/scripts/`, `$CLAUDE_PLUGIN_ROOT/scripts/` and |
| `new-skills/design-taste-frontend/references/gate.md:139` | claude | `$CLAUDE_PLUGIN_ROOT/skills/design-taste-frontend/scripts/` (a plugin install), each only when the variable is |
| `new-skills/design-taste-frontend/references/gate.md:140` | claude | set; then the install folders by name, `$CLAUDE_PROJECT_DIR/.claude/skills/design-taste-frontend/`, |
| `new-skills/design-taste-frontend/references/gate.md:141` | claude | `$CLAUDE_PROJECT_DIR/.agents/skills/design-taste-frontend/`, `~/.claude/skills/design-taste-frontend/` |
| `new-skills/design-taste-frontend/references/gate.md:145` | claude | there or one folder below it prints `tasteskill gate: gate.mjs not found (CLAUDE_PLUGIN_ROOT=...)` on |
| `new-skills/design-taste-frontend/references/gate.md:147` | claude | folder name, other apps, or a Claude Code without skill hooks take one of these. Each runs in every |
| `new-skills/design-taste-frontend/references/gate.md:155` | claude | **Claude Code**, `.claude/settings.json` (blocks with JSON on stdout): |
| `new-skills/design-taste-frontend/references/gate.md:161` | claude | { "hooks": [ { "type": "command", "command": "node \"/path/to/skill/scripts/gate.mjs\" --hook claude", "timeout": 600 } ] } |
| `new-skills/design-taste-frontend/references/gate.md:167` | claude,codex | **Codex**, `.codex/hooks.json` (the same output as Claude Code: `{"decision":"block","reason":...}`): |
| `new-skills/design-taste-frontend/references/gate.md:173` | codex | { "hooks": [ { "type": "command", "command": "node \"/path/to/skill/scripts/gate.mjs\" --hook codex", "timeout": 600 } ] } |
| `new-skills/design-taste-frontend/references/hallmark/references/gates.md:243` | claude | The thread that built the page is its weakest reviewer. Two reviews run with no inherited transcript (a subagent in Claude Code): the **hero review** … |
| `new-skills/design-taste-frontend/scripts/gate.mjs:11` | claude,codex | node <skill>/scripts/gate.mjs --hook claude/codex/antigravity   the same as an agent's Stop hook (stdin: the hook JSON) |
| `new-skills/design-taste-frontend/scripts/gate.mjs:71` | claude,codex | Hook mode blocks with exit 0 and JSON on stdout: {"decision":"block","reason":...} for claude and codex, |
| `new-skills/design-taste-frontend/scripts/gate.mjs:111` | claude,codex | const MODES = { claude: 'block', codex: 'block', antigravity: 'continue' }; |
| `new-skills/design-taste-frontend/scripts/gate.mjs:112` | claude,codex | if (HOOK !== null && !MODES[HOOK]) { console.error('gate: --hook takes claude, codex or antigravity'); process.exit(HOOK === true ? 2 : 0); } |
| `new-skills/feature-expansion/SKILL.md:205` | claude | - **claude-handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the execution contract used in Phase 4: implementers implement their assigne… |
| `new-skills/integration/SKILL.md:128` | claude | - `integrations` by whawkinsiv (claude-code-skills): NOT used. The skill does not exist in the actual repo (it appears only in the learn-skills.dev mi… |
| `new-skills/orchestrate/SKILL.md:32` | codex | Installed as part of the hackathon-ecc Cursor plugin: the three agents and the /orchestrate command register automatically — nothing to copy. The orch… |
| `round2-skills/mobile-ship/references/launch-marketing.md:7` | claude | - **Tooling:** Claude Motion (the code-built video artifact type) was a Team/Enterprise beta in October 2026. If it isn't listed in the Artifact types… |
| `round2-skills/polish-pass/reference/capture.md:33` | claude | 1. **Browser tool in your harness**: Claude in Chrome, ChatGPT in Chrome / ChatGPT agent browser, `agent-browser`, Playwright MCP, Chrome DevTools MCP… |
| `round2-skills/polish-pass/reference/impeccable-critique.md:38` | codex | **Native platforms** (`ios` / `android` / `adaptive`): Assessment B does not apply, because `impeccable detect` and the browser overlay read only web … |
| `round2-skills/polish-pass/reference/impeccable-detector-rules.json:563` | codex | "id": "codex-grid-background", |

Total unique staged lines: 59 (term-hits: claude 38, codex 18, anthropic 10 = 66; 7 lines hit 2–3 terms).

## Appendix C — Composer-feature list (check 9, all 50 lines)

| file:line | classification | excerpt |
|---|---|---|
| `hackathon-ecc/rules/php-coding-style.mdc:3` | PHP Composer CLI / files | globs: ["**/*.php", "**/composer.json"] |
| `hackathon-ecc/rules/php-hooks.mdc:3` | PHP Composer CLI / files | globs: ["**/*.php", "**/composer.json", "**/phpstan.neon", "**/phpstan.neon.dist", "**/psalm.xml"] |
| `hackathon-ecc/rules/php-patterns.mdc:3` | PHP Composer CLI / files | globs: ["**/*.php", "**/composer.json"] |
| `hackathon-ecc/rules/php-security.mdc:3` | PHP Composer CLI / files | globs: ["**/*.php", "**/composer.lock", "**/composer.json"] |
| `hackathon-ecc/rules/php-security.mdc:18` | PHP Composer CLI / files | - Review package trust before adding dependencies. (`composer audit` is END-ONLY — run only at the very end of the project or when the user explicitly… |
| `hackathon-ecc/rules/php-testing.mdc:3` | PHP Composer CLI / files | globs: ["**/*.php", "**/phpunit.xml", "**/phpunit.xml.dist", "**/composer.json"] |
| `hackathon-ecc/skills/laravel-plugin-discovery/SKILL.md:59` | PHP Composer CLI / files | - `package` (string, required): Full Composer package name (e.g. "spatie/laravel-permission") |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:22` | PHP Composer CLI / files | - Environment and Composer checks gate everything else; stop immediately if they fail. |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:31` | PHP Composer CLI / files | composer --version |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:46` | PHP Composer CLI / files | ## Phase 1.5: Composer and Autoload |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:49` | PHP Composer CLI / files | composer validate |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:50` | PHP Composer CLI / files | composer dump-autoload -o |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:89` | PHP Composer CLI / files | composer audit  # END-ONLY: run only at the very end of the project or when the user explicitly asks (deferred security audit, see hackathon-mode §3) |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:153` | PHP Composer CLI / files | composer --version |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:155` | PHP Composer CLI / files | composer validate |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:159` | PHP Composer CLI / files | composer audit  # END-ONLY (see Phase 4) |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:168` | PHP Composer CLI / files | composer validate |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:169` | PHP Composer CLI / files | composer dump-autoload -o |
| `hackathon-ecc/skills/laravel-verification/SKILL.md:173` | PHP Composer CLI / files | composer audit  # END-ONLY (see Phase 4) |
| `hackathon-ecc/skills/dev-team/SKILL.md:14` | "team composer" prose | adversarial challenge (`council`), and it is not a free-form team composer |
| `hackathon-ecc/skills/codebase-onboarding/SKILL.md:29` | PHP Composer CLI / files | Gemfile, composer.json, mix.exs, pubspec.yaml |
| `hackathon-ecc/skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39` | video-composer app (OpenMontage remotion-composer) | / `styles/*.yaml`, `remotion-composer/`, `ink-theater/`, `backlot/`, `docs/`, `tests/` / Playbooks, composer app, review UI, docs, tests / Out of scop… |
| `hackathon-ecc/skills/pitch-deck-video/references/openmontage/README.md:35` | video-composer app (OpenMontage remotion-composer) | - Schemas, styles/playbooks, remotion-composer, ink-theater, backlot, |
| `hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:77` | PHP Composer CLI / files | - **Stack**: detect from the project — check `package.json` deps (react/next/vue/svelte/nuxt/@angular), `pubspec.yaml` (Flutter), `*.xcodeproj`/`Packa… |
| `hackathon-ecc/skills/ui-ux-pro-max/data/ui-reasoning.csv:165` | reply-composer UI constraint (forum pattern) | 164,Forum / Discussion Board,Community/Forum Landing,Dark Mode (OLED) + Flat Design,Dark neutral + topic accent colors + unread indicator + reputation… |
| `hackathon-ecc/agents/ecc-php-reviewer.md:77` | PHP Composer CLI / files | composer audit                             # Dependency vulnerabilities # END-ONLY — run only at the very end of the project or when the user explicit… |
| `hackathon-ecc/scripts/hooks/cursor-session-env.js:3` | Cursor session prose (borderline — see check 9) | * Cursor sessionStart hook — inject ECC_AGENT_DATA_HOME for the composer session. |
| `hackathon-ecc/scripts/lib/gateguard-search-filters.js:43` | PHP Composer CLI / files | json: ['*.json', '*.sarif', 'composer.lock'], |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:171` | CSS .composer class | .composer{padding:10px 14px 14px;border-top:1px solid var(--border);display:flex;flex-direction:column;gap:8px} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:172` | CSS .composer class | .composer .hint{font-size:10px;color:var(--text3)} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:173` | CSS .composer class | .composer textarea{width:100%;min-height:60px;max-height:160px;resize:vertical;background:var(--bg3);border:1px solid var(--border);border-radius:6px;… |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:174` | CSS .composer class | .composer textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:175` | CSS .composer class | .composer .row{display:flex;gap:8px;align-items:center} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:176` | CSS .composer class | .composer .send{flex:1;height:32px;border:none;border-radius:6px;background:var(--accent);color:#fff;font-size:12.5px;font-weight:600;cursor:pointer;t… |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:177` | CSS .composer class | .composer .send:hover{background:var(--accent-dim)} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:178` | CSS .composer class | .composer .send:disabled{opacity:.5;cursor:default} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:179` | CSS .composer class | .composer .status{font-size:10.5px;color:var(--text3)} |
| `hackathon-ecc/scripts/lib/plan-canvas/ui.js:517` | CSS .composer class | <div class="composer"> |
| `hackathon-ecc/scripts/lib/project-detect.js:85` | PHP Composer CLI / files | markers: ['composer.json', 'composer.lock'], |
| `hackathon-ecc/scripts/lib/project-detect.js:305` | PHP Composer CLI / files | * Read composer.json for PHP package dependencies |
| `hackathon-ecc/scripts/lib/project-detect.js:309` | PHP Composer CLI / files | function getComposerDeps(projectDir) { |
| `hackathon-ecc/scripts/lib/project-detect.js:311` | PHP Composer CLI / files | const composerPath = path.join(projectDir, 'composer.json'); |
| `hackathon-ecc/scripts/lib/project-detect.js:312` | PHP Composer CLI / files | if (!fs.existsSync(composerPath)) return []; |
| `hackathon-ecc/scripts/lib/project-detect.js:313` | PHP Composer CLI / files | const composer = JSON.parse(fs.readFileSync(composerPath, 'utf8')); |
| `hackathon-ecc/scripts/lib/project-detect.js:314` | PHP Composer CLI / files | return [...Object.keys(composer.require // {}), ...Object.keys(composer['require-dev'] // {})]; |
| `hackathon-ecc/scripts/lib/project-detect.js:397` | PHP Composer CLI / files | const composerDeps = getComposerDeps(projectDir); |
| `hackathon-ecc/scripts/lib/project-detect.js:423` | PHP Composer CLI / files | depList = composerDeps; |
| `hackathon-ecc/scripts/lib/project-detect.js:487` | PHP Composer CLI / files | getComposerDeps, |
| `new-skills/pitch-deck-video/references/openmontage/runtime-fetch.md:39` | video-composer app (OpenMontage remotion-composer) | / `styles/*.yaml`, `remotion-composer/`, `ink-theater/`, `backlot/`, `docs/`, `tests/` / Playbooks, composer app, review UI, docs, tests / Out of scop… |
| `new-skills/pitch-deck-video/references/openmontage/README.md:35` | video-composer app (OpenMontage remotion-composer) | - Schemas, styles/playbooks, remotion-composer, ink-theater, backlot, |

Total: 50 lines. None is a model pin; none names Cursor's Composer UI feature (1 borderline session-prose line, flagged in check 9).
