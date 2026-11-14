# Fix #16 — CHANGES.md

Re-pin ALL model pins to Grok and scrub Claude / Codex / Anthropic / Opus from
the hackathon-ecc Cursor plugin. Inventory: `fix16/INVENTORY.md` (4,457 lines).
Engine: `fix16/fix16.py` (4,186 lines, md5 bc35e47816749bba3e789cb877a725b9) —
invoked by `build.sh` as the last build step before STEP 5 (wired at
`build.sh:23210`, one line: `python3 "$PLUGIN_ROOT/fix16/fix16.py" "$PLUGIN_DIR"`).
(Fix #16 state was 4,078 lines, md5 be805a19862360c32a484ae1c15f4a45;
fix-up round: +85 lines — the 3 tolerant helpers, the B1/M3 rules, and the
tolerant call sites. Sweep #17 follow-up: +23 lines — the M1/M2 rules and
the Opus 4.x regex extension, build 15.)

## Mechanism

- **Staged-source edits** (files the plugin stages verbatim under `new-skills/`,
  `round2-skills/`, `~/workspace/cursor-skills/less-flat-ui/`): edited directly —
  orchestrate trio (`scout.md`, `fast-worker.md`, `deep-reasoner.md`), orchestrate
  `SKILL.md` roster table + picker instruction + step-4 implementation-tier pin,
  `dispatch-prompt.md` fallback pins + `:197` worked example,
  `agent-TEMPLATE.md` example pins, `LIVE_SMOKE_TEST.md`, repo-root `README.md`
  picker note, `design-taste-frontend/references/gate.md` (staged source for the
  `gate.mjs`/`gate.md` pair).
- **build.sh patch blocks** (upstream ECC files copied by `build.sh`): the
  alias-mapping dict (now `{"sonnet": "cursor-grok-4.6-high-fast", "opus":
  "grok-4.7-high", "haiku": "cursor-grok-4.6-high-fast"}` with its comment
  rewritten), global replaces of embedded pins (`composer-2.5[fast=false]` 125x,
  bare `composer-2.5` 18x, `claude-opus-5[effort=high]` 8x, bare `claude-opus-5`
  6x), the fix9 codex sweep removal (D17), `common-performance.mdc` NEW-side
  effort-controls sentence, shipped-README fast-tier sentence. The 72 agent pins
  are produced at build time by the alias-mapping block — the dict was changed,
  not 72 files.
- **fix16.py tree pass** (runs last, on the built tree): `do_deletes()` (files +
  dirs), targeted edits (part 1, part C prose round 2, installer round 2,
  session-paths round 2, context-profile round 2, misc targeted,
  manifests/schemas), the generic pass (G1–G14 mechanical rules), and
  `edit_post_generic()` (waves 1–4: subs whose old text only matches the
  post-generic-pass tree, plus stragglers found by dry-run self-checks).
  Per-run log (this run): `fix16/fix16-run-log.md`.

## Build results

| Build | Exit | fix16 errors | Notes | Changes | Removals | Outcome |
|---|---|---|---|---|---|---|
| 1 (real) | 1 | 2 | 7 | 126 | 65 | fix16 returned 1; `set -e` stopped the build before STEP 5 |
| 2 (real) | 1 | 75 | 12 | 453 | 86 | 3 JS syntax failures (context-profile-commands.js, install-lifecycle.js, install/apply.js) + registry smoke rc=1 |
| 3 (real) | 1 | 6 | 11 | 615 | 87 | JS syntax 0, JSON 0, registry smoke rc=0, total banned hits 23 — 5 `remove_function`/`replace_function` "not found" (template-literal brace-matcher bug) + 1 gate.md duplicate call |
| 4 (real) | 0 | 0 | 11 | 625 | 87 | **Clean.** Self-check all zero. Manifest `manifest-build4.txt` (2,670 files) |
| 5 (real) | 0 | 0 | 11 | 625 | 87 | **Clean.** Manifest `manifest-build5.txt` — diff vs build 4: **0 (identical)** |
| 6 (real) | 0 | 0 | 11 | 626 | 87 | **Clean** (wave-4 scan-skills fix). Manifest `manifest-build6.txt` (2,670 files) |
| 7 (real) | 0 | 0 | 11 | 626 | 87 | **Clean.** Manifest `manifest-build7.txt` — diff vs build 6: **0 (identical)** |
| 8 (real) | 0 | 0 | 11 | 624 | 88 | **Clean.** D13 follow-up: `session-guardian.sh` deleted (see below). Manifest `manifest-build8.txt` (2,669 files) |
| 9 (real) | 0 | 0 | 11 | 624 | 88 | **Clean.** Manifest `manifest-build9.txt` — diff vs build 8: **0 (identical)** |
| 10 (real) | 1 | 1 | 37 | 600 | 88 | fix16 returned 1; `set -e` stopped the build before STEP 5 — one missed tolerant rule: the gate.md "As a hook" paragraph sub (`fix16.py`, post-generic-pass old text) still expected the staged upstream wording the fix-up scrub had replaced. Made tolerant (`sub_if_new_present`); no other rule failed. Self-check was already all zero (TOTAL BANNED-TERM HITS 0). |
| 11 (real) | 0 | 0 | 38 | 600 | 88 | **Clean.** Self-check all zero (now incl. `BANNED sonnet: 0`, `BANNED haiku: 0`). Manifest `manifest-build11.txt` (2,665 files) |
| 12 (real) | 0 | 0 | 38 | 600 | 88 | **Clean.** Manifest `manifest-build12.txt` — diff vs build 11: **0 (identical)** |
| 13 (real) | 0 | 0 | 38 | 600 | 88 | **Clean.** Antigravity gate-doc removal (see below). Manifest `manifest-build13.txt` (2,665 files) |
| 14 (real) | 0 | 0 | 38 | 600 | 88 | **Clean.** Manifest `manifest-build14.txt` — diff vs build 13: **0 (identical)** |
| 15 (real) | 0 | 0 | 38 | 602 | 88 | **Clean.** Sweep #17 M1/M2 fix (see below). Manifest `manifest-build15.txt` (2,665 files) |
| 16 (real) | 0 | 0 | 38 | 602 | 88 | **Clean.** Manifest `manifest-build16.txt` — diff vs build 15: **0 (identical)** |

- `build.sh` after: **23,221 lines, md5 `532ab5458c22d6341444fdc92cf67ffd`**
  (fix-up round: README heredoc counts + the :18296 schema sentence; line
  count unchanged — all edits are same-line substitutions. Fix #16 state was
  23,221 lines, md5 `5d6ec4674214d89af8dd84856c5db987`). Backup of the
  pre-fix16 build.sh: `/tmp/fix16/build.sh.pre-fix16`.
- Final built-tree counts (STEP 5): skills 166, agents 72, rules 123, commands 87,
  hooks 15. `plugin.json: hackathon-ecc 1.0.0`. Unchanged across builds 7–16.
- Build logs: `fix16/build3.log` … `fix16/build16.log`. Manifests:
  `fix16/manifest-build4.txt` … `fix16/manifest-build16.txt` (2,670 files for
  builds 4–7, 2,669 files for builds 8–9, 2,665 files for builds 11–16 — the
  four-file drop is the deleted brand-icon SVGs; `find . -type f -not -path "./node_modules/*" | sort | xargs sha256sum`).
- Manifest sha256 (builds 8 and 9, identical):
  `796a48d1734329193288ed6814ce10c4bab7f589970423d8968850cabcf0c977`.
  Diff build 7 → build 8 touches exactly two entries: `observer-loop.sh`
  (comment reword, hash `0f733e0d…` → `a1cde281…`) and `session-guardian.sh`
  (removed). No other file changed.

## Post-build self-check (final tree, build 16)

(Re-verified identically on builds 13–16 after the Antigravity gate-doc
removal and the sweep #17 M1/M2 fix: same all-zero block below, same fix16
footer.)

```
```
BANNED composer-2\.5: 0
BANNED claude: 0
BANNED codex: 0
BANNED anthropic: 0
BANNED sonnet: 0
BANNED haiku: 0
OPUS (list individually; may false-positive): 0
GEMINI/GPT- in model-pin contexts: 0
JS SYNTAX FAILURES: 0
JSON FAILURES: 0
INSTALL REGISTRY SMOKE: rc=0 stdout='getInstallTargetAdapter,listInstallTargetAdapters,planInstallTargetScaffold\n[object Object]' stderr=''
commands/gan-build.md: grok-4.7-high x2, claude-opus-5 x0, composer-2.5 x0
commands/gan-design.md: grok-4.7-high x3, claude-opus-5 x0, composer-2.5 x0
TOTAL BANNED-TERM HITS: 0
```
```

(The build-9 block is superseded by the above: the self-check term list now
also greps `sonnet` and `haiku`. The build-9 counts in the sections below —
166/72/123/87/15, pins ×45/×98 — are unchanged except the fast pin, which is
now ×99 lines / ×100 occurrences: +1 is `scripts/lib/agent-compress.js:118`,
the B1 fix itself.)

Independent verification (outside fix16.py, same tree):

- `grep -ri "composer-2.5" / "claude" / "codex" / "anthropic" / "opus"` —
  **0 hits each** (opus list individually: none; the bare-substring check finds no
  ordinary-word false positives in this tree).
- `grep -ri "gemini\|gpt-"` in model-pin contexts (`model:` field / pin table):
  **0 surviving non-Grok pins**.
- `grep -rn "Cursor-Code-only"`: **0** (part D strips the run-1 mangling).
- `grep -rn "~/.ecc"`: **1 hit** — `skills/unified-memory/SKILL.md:48`
  `` `~/.ecc/memory/` `` — **verified upstream** (identical at
  `/tmp/ecc-repo-clean/skills/unified-memory/SKILL.md:48`): ECC's own user-scope
  memory vault, not a fix16 invention; contains no banned term; left as-is.
  (A second `~/.ecc` hit, `skills/rules-distill/scripts/scan-skills.sh:10`, was a
  real fix16 defect — the unguarded part-C catch-all rewrote a HOME path — fixed
  in wave 4 to `~/.cursor/skills`.)
- Grok pins in the built tree: `grok-4.7-high` ×45 lines / ×52 occurrences,
  `cursor-grok-4.6-high-fast` ×99 lines / ×100 occurrences (was ×98/×99; +1 is
  `scripts/lib/agent-compress.js:118`, the B1 fix).
- `node --check` on all 17 surgically edited .js files (apply.js, lifecycle.js,
  plan.js, install-targets/registry.js, content-transform.js, install-manifests.js,
  install-executor.js, session-adapters/registry.js, canonical-session.js,
  context-profile-commands.js, context-carriers.js, guarded-write.js,
  contained-fs.js, file-lock.js, harness-capabilities.js,
  harness-adapter-compliance.js,
  scripts/hooks/hookify-runtime.js): **17/17 pass**.
  (Correction, fix-up round: the earlier text claimed 18/18 and listed
  `scripts/lib/hooks/hookify-runtime.js`, a path that does not exist — there
  is no `scripts/lib/hooks/` directory in the built tree, in `build.sh`, or
  in upstream `/tmp/ecc-repo-clean`; the real file is
  `scripts/hooks/hookify-runtime.js`. Verified by re-running `node --check`
  on all 17 real files: 17 pass.)
- All 22 edited modules `require()` cleanly. Install registry dry-run:
  `listInstallTargetAdapters()` → `['cursor']` only;
  `getInstallTargetAdapter('cursor')` →
  `{"id":"cursor-project","target":"cursor","kind":"project","nativeRootRelativePath":".cursor"}`.
- Dangling references: `preflightClaudeSettingsOperations` 0,
  `planClaudeHooksOperations` 0, `findPreviousManagedHooks` 0,
  `validateRecordedManagedHooks` 0.
- gan-build.md `grok-4.7-high` ×2, gan-design.md ×3, `claude-opus-5` ×0,
  `composer-2.5` ×0.

## Decisions applied (D1–D20 + tier rule)

**Tier rule** (everything not explicitly decided): opus-tier → `grok-4.7-high`;
composer/sonnet/haiku-tier → `cursor-grok-4.6-high-fast`.

- **D1** GAN agents (`ecc-gan-planner`/`generator`/`evaluator`): ALL →
  `cursor-grok-4.6-high-fast`. Judgment lives in the design-lead's direction
  (4.7-high) and the evaluator's rubric; all three are bounded task bots.
  Files: `agents/ecc-gan-*.md` (via the build.sh alias-mapping block).
- **D2** Separate implementer tier on `grok-4.7-high`: the slice-builder
  implementer spawn pin was ADDED in `new-skills/orchestrate/SKILL.md` step 4
  ("Slice-builder implementers spawn on the implementation tier — model
  `grok-4.7-high` (slug form only). Purely mechanical, fully-specified sub-tasks
  inside a slice still dispatch to fast-worker (`cursor-grok-4.6-high-fast`).").
  `model-route.md` rows: haiku (deterministic low-risk mechanical) →
  `cursor-grok-4.6-high-fast`; sonnet (default for implementation and refactors)
  → `grok-4.7-high`; opus (architecture, deep review) → `grok-4.7-high`.
  `dispatch-prompt.md:197` worked example is the MECHANICAL-tier fallback: kept
  fast-worker persona, model → `cursor-grok-4.6-high-fast`. Fast-worker stays the
  mechanical sub-task tier (fast). 61 specialist agents stay fast.
- **D3** 11 architect-flavoured composer-tier agents stay fast; hard reasoning
  escalates to deep-reasoner. 4 opus agents (`deep-reasoner`, `ecc-architect`,
  `ecc-healthcare-reviewer`, `ecc-spec-miner`) → `grok-4.7-high`.
  Files: `new-skills/orchestrate/agents/deep-reasoner.md` (description + `model:`
  + comment rewritten), `fast-worker.md`, `scout.md` (all → fast slug, comments
  rewritten), plus the alias-mapping block for the 61 + 11.
- **D4** `evolve.md:172`: fast — sets the default for all future evolved agents.
- **D5** Astra review: DELETED the Astra review step and
  `scripts/lib/astra-review/codex.js` delegate (whole `scripts/astra-review.js`
  + `scripts/lib/astra-review/` dir). Review continues via Grok reviewers:
  `commands/astra-review.md` rewritten prose-only (Step 2 = blind deep-reasoner
  subagent dispatch, `grok-4.7-high`). Loss: Astra/Codex-backed review, the
  `--consent-to-openai` / `codex login` / `ECC_ASTRA_MODEL` flow.
- **D6** `gan-style-harness`: every `claude -p` invocation rewritten to the
  Cursor-native GAN loop (`/gan-build` + ecc-gan agents); deleted
  `scripts/gan-harness.sh`, the "Via Claude Code" doc block, and the "Evolution
  Across Model Capabilities" section (rewording Anthropic-model history to Grok
  would fabricate history). Model defaults → "Grok 4.6 High Fast
  (`cursor-grok-4.6-high-fast`) by default; raise via `GAN_*_MODEL=grok-4.7-high`".
  Loss: the Claude-Code-subprocess GAN path; the model-capability history section.
- **D7** `transcript-context.js` model→window table: constants are ABSOLUTE
  (200k standard / 1M large) and mismatch Grok's verified windows (4.7: 256k
  standard / 500k long context) → the model-specific table was dropped; the
  existing fallback/default + `ECC_CONTEXT_WINDOW_TOKENS` env override were wired
  in. No 4.6 window number was invented. `CLAUDE_CODE_AUTO_COMPACT_WINDOW`
  branches dropped; the `[1m]` marker check kept.
- **D8** `schemas/agent.schema.json` enum `["haiku","sonnet","opus"]` →
  `["cursor-grok-4.6-high-fast","grok-4.7-high"]` (no "inherit" was present).
  `agent-ir.js` `VALID_MODELS` + error message re-keyed; `agent-emit-pi.js`
  comments + tier counts re-keyed. Emitters still validate.
- **D9** `hooks/adapter.js`: `transformToClaude` → `transformToHookPayload`,
  `CLAUDE_SESSION_ID` → `ECC_SESSION_ID` (a name the plugin already uses).
  Payload shape UNCHANGED (transport contract). No Cursor API name invented.
- **D10** Multi-host installer: STRIPPED to Cursor-only via `build.sh` + the
  fix16 tree pass (the `rm -f` drop-pattern precedent). Removed: 15
  install-target adapters, 12 `scripts/lib/install/` host files, 7 top-level lib
  files, 3 session adapters, 3 mcp-inventory readers, `skill-host-compat`
  command + validator, `qwen-adapt-agents.js` (D14). Loss: installing/running
  under the other 16 harnesses (Claude Code, Codex, Gemini, Copilot, Opencode,
  Qwen, Pi, and the rest named in the inventory). The Cursor install path works
  (registry smoke rc=0, targets `['cursor']`).
- **D11** Attributions scrubbed to host-neutral wording. `resolve-ecc-root.js:26`
  `LEGACY_PLUGIN_SLUG = 'everything-claude-code'` — the legacy-migration branch
  using it was removed. Loss: legacy everything-claude-code installs are no
  longer auto-detected/migrated (also: `scripts/auto-update.js`
  `ECC_PACKAGE_NAMES` no longer trusts the `'everything-claude-code'` package
  name — legacy 1.x checkouts are no longer trusted for auto-update). Anthropic
  harness-paper citation → "the upstream multi-agent harness design paper"
  (orchestrate `:311`, Taste `:419`, gan-build/gan-design, gan agent files).
- **D12** `scripts/hooks/cost-tracker.js` + `scripts/lib/llm-summary.js` +
  `commands/cost-report.md` REMOVED (no verified Cursor cost source — none
  invented; llm-summary's mechanism is `claude -p`). Call sites in
  `hooks/stop.js`, `scripts/hooks/pre-compact.js`, `scripts/hooks/session-end.js`
  cleaned. Loss: cost tracking + LLM session summaries. (Deliberately left:
  `scripts/hooks/post-bash-command-log.js:20` `fileName: 'cost-tracker.log'` —
  its own log file, no banned term; `skills/pitch-deck-video/SKILL.md:554`
  mentions the cost-tracker design as not shipped.)
- **D13** `skills/skill-comply/` (whole dir), plankton's `claude -p` path only
  (rest of plankton kept — verified it functions as a reporter without
  auto-fix), observer's claude spawn (`observer-loop.sh` spawn block + watchdog
  removed, `analyze_observations` stubbed) + `migrate-homunculus.sh` REMOVED.
  No reimplementation on Cursor subagents (out of scope). Loss: skill-comply
  checks; Plankton's Claude-powered auto-fixes (it reports violations instead);
  background observer analysis; homunculus migration.
- **D14** `scripts/qwen-adapt-agents.js` + `preflightQwenAgentOperations`
  (apply.js) + qwen transform handling in `content-transform.js` (passthrough
  now throws on any named transform) REMOVED with D10. No gemini-adapt
  equivalent existed.
- **D15** `~/.claude` / `CLAUDE_*`: never invented a Cursor path. References
  belonging to a removed feature went with the feature. Descriptive mentions →
  neutral wording ("the agent's local state directory", "a host settings file").
  Project-local `.claude/` artifact dirs → `.ecc/` (the plugin-owned namespace).
  Functional paths re-pointed to VERIFIED Cursor paths only:
  `~/.cursor/ecc` (agent data home, verified in `agent-data-home.js`),
  `~/.cursor/mcp.json` (global MCP), `~/.cursor/skills`, `~/.cursor/rules`,
  `~/.cursor/plugins`. `CURSOR_PROJECT_DIR` / `CURSOR_PACKAGE_MANAGER` /
  `ECC_TRANSCRIPT_PATH` / `ECC_HOOK_EVENT_NAME` / `ECC_SESSION_ID` /
  `ECC_AGENT_DATA_HOME` envs (all already used by the plugin or verified Cursor
  envs). Surviving functional paths were all re-pointed; none was left to guess.
- **D16** `skills/council-multi-model/` (incl. `scripts/review-with-codex.js`),
  `commands/santa-loop.md`, the five `commands/multi-*.md`, `commands/loop-status.md`
  DELETED (CLI-only). The `council` skill itself STAYS (its second
  deep-reasoner pass already replaces the Codex peer, per orchestrate SKILL.md:32).
  Loss: dual-model adversarial review, the Antigravity path, model diversity.
  `commands/skill-host-compat.md` + its validator deleted with the same pass.
- **D17** fix9 sweep: `codex@0.167.1` removed from the registry-pin list AND its
  print line in `build.sh` (done in an earlier session; verified in build 4+).
- **D18** `build.sh` embeddings: EVERY embedding of old pins patched — alias dict
  + comment, 9× `claude-opus-5[effort=high]`, 1× bare `model: opus`, 2×
  `gpt-6-astra`, and ALL heredoc-embedded file contents (`composer-2.5` 125× +
  18× in `build.sh`). A rebuild does not reintroduce any old pin (verified:
  built-tree `composer-2.5` ×0 across builds 4–7).
  Deliberate retention: the astra-review `qc_patch` OLD side `model: opus` and
  `gpt-6-astra` OLD sides in `build.sh` are match patterns that must match
  upstream verbatim; the built-tree output is scrubbed by the fix16 pass instead.
- **D19** "Composer": ONLY the `composer-2.5` model pin goes. PHP Composer CLI
  (`composer audit`/`validate`, `composer.json`/`lock`), "team composer" prose,
  CSS `.composer` all STAY. Zero mentions of Cursor's Composer UI feature exist;
  none added.
- **D20** (round 2) Context-profile native execution removed — CLI-only (spawns
  codex/claude CLIs), no Cursor provider exists in the PROVIDERS table.
  Deleted: `context-profile-native.js`, `context-profile-native-executable.js`,
  `context-profile-native-discovery.js`, `context-profile-interactive.js`,
  `context-profile-launch.js`, `context-profile-proposal.js` (zero callers, dead
  code). `context-profile-commands.js` `execute()` replaced with a clean
  resolve + routing-index + store version (default target `'cursor'`).
  Carrier/resolve machinery kept (cursor layout exists in `context-carriers.js`
  LAYOUTS). Loss: native isolated execution (Codex/Claude CLI sandboxing,
  interactive native sessions, `run` launching).

## Deviations from D1–D19 (with reasons)

- **astra-review OLD-side retentions in build.sh** (see D18): match patterns must
  match upstream verbatim; built-tree output scrubbed by fix16 instead.
- **`.ecc/` instead of `.cursor/` for project-local artifact dirs** (D15):
  inventing a Cursor path would violate D15; `.ecc` is the plugin-owned namespace.
- **Adapter rename** to `transformToHookPayload` + `ECC_SESSION_ID` (D9): names the
  plugin already uses; no Cursor API name invented.
- **config-gc skill deleted** (round 2): its function is GC of the `~/.claude`
  config layout; no verified Cursor equivalent.
- **mcp-inventory whole dir deleted** (round 2): dead code, no importers in
  `.js`/`.md`/`.json`. The live secret scanner is the separate
  `scripts/hooks/pre-bash-commit-quality.js:134` (relabeled `'Anthropic API key'`
  → `'sk-ant API key'`; detection regexes kept).
- **file-lock.js created** (`scripts/lib/install/file-lock.js`): host-neutral file
  lock, same logic as the deleted `claude-settings-lock` module
  (`createFileLock`/`acquireFileLock`/`runWithFileLock`/`getFileLockIdentity`/
  `inspectFileLock`/`recoverFileLock`/`sameFileIdentity`, lock suffix `.ecc.lock`).
- **Commit-attribution write removed, not re-pointed**: no verified Cursor
  settings path exists to point it at.
- **createDisabledMigration passthrough** in `apply.js` (shape mirrors the
  upstream disabled migration); opencode legacy stubs return exactly the
  non-opencode upstream behavior; script-boundary check reduced to a no-op (the
  boundary copy is never produced for cursor); `prepareHookConsentMigration`
  reduced to a passthrough; `assertOpenCodeLeaseCoverage` kept as an exported
  no-op (install-lifecycle still calls it on the repair path).
- **inventory.js deleted outright** (zero callers — supersedes the earlier plan to
  rewrite it Cursor-only).
- **content-transform.js passthrough throws on any named transform** (no adapter
  can name one anymore).
- **install-targets/registry.js and session-adapters/registry.js rewritten
  whole-file** (cursor-only / dmux-tmux only).
- **`CURSOR_RULES_DIR` env rename; rules-distill global rules default
  `~/.cursor/rules`; `CLAUDE_TRANSCRIPT_PATH` → `ECC_TRANSCRIPT_PATH`;
  `CLAUDE_HOOK_EVENT_NAME` → `ECC_HOOK_EVENT_NAME`; `CLAUDE_CODE_ENTRYPOINT` →
  `ECC_ENTRYPOINT` (values `cli|sdk-ts|sdk-cli|cursor`)** — plugin-owned caller
  envs, mechanism unchanged; `CLAUDE_PROJECT_DIR` → `CURSOR_PROJECT_DIR`
  (verified Cursor env, same override semantics).
- **`CLAUDE.md` → `AGENTS.md` global rename** (AGENTS.md is the documented Cursor
  instruction file; the plugin's own root uses `~/AGENTS.md`).
- **`~/.claude.json` → `~/.cursor/mcp.json`** (Cursor global MCP file).
- **install-manifests/schema enum handling**: host entries dropped, never
  relabelled; an enum emptied by removal is fixed to `["cursor"]`.
- **Manifest catalog host labels**: the parenthetical dropped, not relabelled to
  "Cursor-only". Part D also repairs the run-1 mangling "Claude-Code-only" →
  "Cursor-Code-only" (36× in pi-core.json exclude reasons) by stripping the prefix.
- **insaits `DEFAULT_MODEL` → `grok-4.7-high`** (fingerprint label; the plugin's
  main model is the honest Cursor-era default).
- **security-scan deep-analysis section deleted**: the `ANTHROPIC_API_KEY` +
  `npx ecc-agentshield scan --opus` pipeline has no verified Grok equivalent.
- **gate.mjs MODES → `{ cursor: 'block' }`** with `--hook cursor` only.
- **`_warn_legacy_data` deleted** with the D13 migration removal; test fixture
  `.claude` → `.ecc` (synthetic tmp path); `.claude-mem` → `.ecc-mem` skip-path
  default; context-budget docs URLs dropped (code.claude.com is the Claude Code
  docs host, no verified Cursor docs URL on hand).
- **Session commands KEPT** (re-pointed to `~/.cursor/ecc/session-data`): the
  mechanism is host-agnostic once the data home is re-pointed; the
  "(Claude Code only)" label is reworded, not treated as a deletion trigger.
- **gan-style-harness reference titles de-branded** (the Anthropic paper title
  rewritten to "(upstream multi-agent harness design paper)"; the Epsilla title
  keeps its name) so the self-check stays at zero "anthropic" hits.
- **plankton subprocess tiers merged**: haiku+sonnet collapse into the single fast
  slug `"cursor-grok-4.6-high-fast"` with sonnet's 300s timeout kept (duplicate
  JSON keys are not allowed, so a 1:1 re-key was impossible); opus-tier keeps
  600s on `grok-4.7-high`.
- **frontend-design-direction install-from line dropped**: the `anthropics/skills`
  source contains a banned substring.
- **auto-update `ECC_PACKAGE_NAMES` drops `'everything-claude-code'`**
  (consistent with D11); **hook-flags `CLAUDE_PLUGIN_OPTION_*` fallbacks dropped**
  (keep `ECC_*` + managed config); **context-carrier schema narrowed to
  cursor-only enums**; **gateguard renames** use the established patterns
  (`CURSOR_PROJECT_DIR`, `ECC_TRANSCRIPT_PATH`, `ECC_HOOK_EVENT_NAME`, `.ecc`
  worktrees/settings); `isClaudeSettingsPath` → `isAgentSettingsPath` matching
  `.ecc/settings*.json` only (MCP config is not agent settings, D15);
  **`PLATFORM_SOURCE_PATH_OWNERS` narrowed to cursor-only**.
- **Template-literal brace-matcher bug (fixed in build 4)**: `_scan_string` stopped
  at the first `${` inside a template literal and the caller resumed code scanning
  there, so the literal's closing backtick was re-read as a NEW opening quote and
  the rest of the file was swallowed as "string" — `_brace_match_end` returned -1
  for any function whose body contains a `` `...${...}...` `` literal. Fixed by
  making `_scan_string` skip `${...}` interpolations internally (brace-matched,
  recursive, string-aware). Affected: `shouldSetClaudeCommitAttributionPreference`,
  `preflightClaudeSettingsOperations`, `planAntigravityLegacyInstall`,
  `inspectClaudeSettingsOperation`, `generatedManifest` (all verified removed /
  replaced afterwards on scratch copies, then in build 4).
- **gate.md Codex-section duplicate fixed**: the part-C `remove_section_by_heading`
  call could never match (the heading is bold text, not a markdown heading); the
  post-generic span deletion is the operative removal; the part-C call was deleted.
- **Session-path wave 3**: part B re-pointed the session commands' description
  labels, but 13 body/example lines in `commands/resume-session.md` (6×
  `session-data`, 2× `sessions`), `commands/save-session.md` (3×),
  `commands/sessions.md` (2× + 2×) still cited `~/.claude/...`. The generic pass
  deliberately skips `~/` home paths (D15 guard), so they were re-pointed in
  `edit_post_generic()` to `~/.cursor/ecc/session-data/` /
  `~/.cursor/ecc/sessions/` (verified counts, dry-run tested).
- **scan-skills wave 4**: the part-C catch-all `\.claude/skills` → `.ecc/skills`
  (unguarded) rewrote the HOME path in the `RULES_DISTILL_GLOBAL_DIR` comment
  (`scan-skills.sh:10`) to an invented `~/.ecc/skills`. Re-pointed in
  `edit_post_generic()` to `~/.cursor/skills` (the verified Cursor global skills dir).

## Notes (from the run log)

- rules/common-performance.mdc — effort-controls sentence already rewritten by the build.sh NEW-side patch; fix16 edit skipped (no-op)
- agent-data-home.js: Cursor home ~/.cursor/ecc is VERIFIED in this file (getDefaultCursorAgentDataHome + ECC_AGENT_DATA_HOME + .cursor/ecc-agent-data.json), so it becomes the only default. getAgentDataHome() callers (metrics, session aliases, package manager) now resolve under ~/.cursor/ecc automatically.
- scripts/lib/install-executor.js: pattern not found (verify manually): "target = 'claude'"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs: pattern not found (verify manually): 'for claude and codex'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh: pattern not found (verify manually): '\\$HOME/\\.claude/rules'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh: pattern not found (verify manually): '\\.claude/rules'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh: pattern not found (verify manually): '\\$HOME/\\.claude/skills'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh: pattern not found (verify manually): '\\$PWD/\\.claude/skills'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh: pattern not found (verify manually): '\\*/\\.claude/skills\\*'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh: pattern not found (verify manually): '\\.claude/skills'
- rules/common-hooks.mdc: pattern not found (verify manually): ' \\(or [^)]*\\.claude/settings\\.json[^)]*\\)'

## Removals (87) — file, what was removed, what is lost

- scripts/astra-review.js
- scripts/gan-harness.sh
- scripts/lib/install-targets/adal-project.js
- scripts/lib/install-targets/antigravity-project.js
- scripts/lib/install-targets/claude-home.js
- scripts/lib/install-targets/claude-project.js
- scripts/lib/install-targets/codebuddy-project.js
- scripts/lib/install-targets/codex-home.js
- scripts/lib/install-targets/copilot-project.js
- scripts/lib/install-targets/gemini-project.js
- scripts/lib/install-targets/hermes-home.js
- scripts/lib/install-targets/joycode-project.js
- scripts/lib/install-targets/kimi-project.js
- scripts/lib/install-targets/openclaw-home.js
- scripts/lib/install-targets/opencode-home.js
- scripts/lib/install-targets/qwen-home.js
- scripts/lib/install-targets/zed-project.js
- scripts/lib/install/antigravity-agent.js
- scripts/lib/install/antigravity-legacy-migration.js
- scripts/lib/install/antigravity-rule.js
- scripts/lib/install/claude-settings-lock.js
- scripts/lib/install/claude-settings.js
- scripts/lib/install/claude-skill-migration.js
- scripts/lib/install/codex-user-config.js
- scripts/lib/install/copilot-agent.js
- scripts/lib/install/copilot-rule.js
- scripts/lib/install/opencode-install-lock.js
- scripts/lib/install/opencode-legacy-migration.js
- scripts/lib/install/opencode-script-boundary.js
- scripts/lib/claude-plugin-setup.js
- scripts/lib/codex-plugin-setup.js
- scripts/lib/codex-legacy-sync.js
- scripts/lib/claude-scope-migration.js
- scripts/lib/claude-dry-run-sandbox.js
- scripts/lib/claude-commit-attribution.js
- scripts/lib/multi-harness-setup.js
- scripts/lib/session-adapters/claude-history.js
- scripts/lib/session-adapters/codex-worktree.js
- scripts/lib/session-adapters/opencode.js
- scripts/ci/validate-skill-host-compat.js
- commands/skill-host-compat.md
- scripts/qwen-adapt-agents.js
- scripts/hooks/cost-tracker.js
- scripts/lib/llm-summary.js
- commands/cost-report.md
- skills/continuous-learning-v2/scripts/migrate-homunculus.sh
- commands/santa-loop.md
- commands/multi-backend.md
- commands/multi-plan.md
- commands/multi-execute.md
- commands/multi-frontend.md
- commands/multi-workflow.md
- commands/loop-status.md
- scripts/lib/context-profile-native.js
- scripts/lib/context-profile-native-executable.js
- scripts/lib/context-profile-native-discovery.js
- scripts/lib/context-profile-interactive.js
- scripts/lib/context-profile-launch.js
- scripts/lib/context-profile-proposal.js
- scripts/lib/astra-review
- skills/skill-comply
- skills/council-multi-model
- skills/config-gc
- scripts/lib/mcp-inventory
- commands/astra-review.md — Astra review step + Codex delegate removed; review continues via Grok reviewers (D5). Loss: Codex-backed review; the `--consent-to-openai` / `codex login` / `ECC_ASTRA_MODEL` / MCP-Codex paths are gone.
- skills/gan-style-harness/SKILL.md — 'Via Shell Script', 'Via Claude Code' and 'Evolution Across Model Capabilities' sections removed (D6). Loss: the shell wrapper and the Anthropic-model-history narrative; the loop now runs only via /gan-build + ecc-gan-* Cursor subagents.
- skills/continuous-learning-v2/agents/observer-loop.sh — claude spawn, watchdog, and process helpers removed (D13). Loss: background instinct extraction; observations accumulate unanalyzed.
- skills/plankton-code-quality/SKILL.md — claude -p auto-fix delegation removed (D13). Loss: Claude-powered auto-fixes; Plankton now reports violations instead of auto-fixing.
- scripts/lib/llm-summary.js + call sites (D12). Loss: LLM-generated session summaries at pre-compact and session-end (and the context-low trigger that gated them); mechanical session summaries still run. scripts/hooks/cost-tracker.js + commands/cost-report.md removed with the same decision: no verified Cursor cost source exists.
- scripts/lib/resolve-ecc-root.js — legacy everything-claude-code migration branch removed (D11). Loss: legacy everything-claude-code installs are no longer auto-detected/migrated; resolution is ECC_PLUGIN_ROOT -> ~/.cursor/plugins scan -> selfRoot.
- install/content-transform.js host branches removed (D10/D14). Loss: Claude manual-plugin namespace projection, Qwen/Antigravity/Copilot frontmatter adaptation, OpenCode hook disabling — all host-specific, unused by Cursor plans.
- install/ownership-guard.js codex-user-config guard removed (D10). Loss: refusing to overwrite a user-edited Codex user config during install/repair (no Codex config exists in a Cursor-only install).
- scripts/lib/install/inventory.js
- scripts/lib/install/inventory.js deleted (round 2). Loss: the manual/managed Claude install discovery helpers (findManualClaudePlugin / findManagedClaudeInstalls / resolveClaudePaths) — nothing in the plugin called them; the Cursor install is discovered via the plugin root, not a Claude config dir.
- install/apply.js: commit-attribution preference write removed (D12/D15). Loss: the installer no longer writes the commit-attribution preference into the host settings file (default attribution behavior applies). The Claude-settings module it ran through is deleted and no verified Cursor settings path was invented for it.
- install/apply.js: legacy Claude-skill migration removed (D13). Loss: migrating legacy Claude flat skills into the install — replaced by the disabled-migration shape (plan operations only), so a Cursor install never moves legacy skill files.
- install-lifecycle.js: Claude settings repair/uninstall/inspect handlers removed (D12). Loss: doctor/repair/uninstall of update-claude-settings operations (Cursor installs never produce them; Cursor hooks live in the plugin's hooks.json).
- install-lifecycle.js: legacy OpenCode/Antigravity discovery + repair removed (D10). Loss: discovering/repairing legacy multi-host installs; doctor/repair now cover Cursor installs only.
- session-adapters: Claude-history / Codex-worktree / OpenCode adapters + their canonical-session normalizers removed (D10/F2). Loss: reading Claude/Codex/OpenCode session transcripts and worktrees as orchestrated sessions; dmux-tmux sessions are unaffected.
- context-profile native execution removed (D20). Loss: native isolated execution (Codex/Claude CLI sandboxing, interactive native sessions, `run` launching, prepare/rollback/recover native commands); the carrier/resolve/routing-index machinery for Cursor remains.
- design-taste-frontend brand icons (anthropic/claude/claude-code/codex) — removed from assets/icons/index.json + demo/icons-credits.json; the heroes.json 'from' attribution drops Anthropic (fix #16)
- harness-capabilities.js + harness-adapter-compliance.js non-Cursor entries — the cross-harness capability/compliance catalogs are now Cursor-only; the DeepSeek DSH bridge record goes with them (fix #16)
- unified-memory cross-host transfer — handoff flags now take cursor only; the Codex/Hermes/OpenCode paths are gone (fix #16)
- browser-qa claude-in-chrome MCP — not a Cursor MCP; Playwright / Puppeteer remain (fix #16)
- continuous-learning-v2 homunculus migration — migrate-homunculus.sh was deleted (D13); there is no migration path from the old `~/.claude/homunculus` location (fix #16)
- pi-core.json catalog entries for the deleted skills (council-multi-model, skill-comply, config-gc, claude-devfleet) and commands (multi-*, santa-loop, cost-report, skill-host-compat, loop-status)
- skills/security-scan/SKILL.md 'Grok 4.7 High Deep Analysis' section — the ANTHROPIC_API_KEY / npx ecc-agentshield scan --opus pipeline has no verified Grok equivalent; the rest of the skill is unchanged (fix #16)

## Changes (626) — file, old → new

Mechanism key: most entries are fix16.py tree-pass edits on the built tree
(`do_deletes` / targeted / generic-pass / post-generic); staged-source edits and
build.sh patches are named in the Decision section above and in the per-entry text
where they apply. Entries are truncated at ~80 characters in the run log; the full
old/new text is recoverable from `fix16.py` + the inventory.

- scripts/lib/transcript-context.js — 'Reads the latest assistant `usage` record from a Claude Code session' -> 'Reads the latest assistant `usage` record from an agent session'
- scripts/lib/transcript-context.js — dropped KNOWN_MODEL_WINDOW_TOKENS table + isKnownModelFamilyMatch (D7)
- scripts/lib/transcript-context.js — '  // Large-window model families without a [1m] marker fall through the checks\n ' -> ''
- scripts/lib/transcript-context.js — '  // Explicit window override wins: 400k models (e.g. Opus 4.x) match neither th' -> '  // Explicit window override wins: a model whose window matches neither the\n  /'
- scripts/lib/transcript-context.js — "  // Claude Code's CLAUDE_CODE_AUTO_COMPACT_WINDOW is the harness auto-compact\n " -> ''
- scripts/lib/transcript-context.js — ' * Detect the context window size for a turn.\n * 1M when the model id carries th' -> ' * Detect the context window size for a turn.\n * 1M when the model id carries th'
- scripts/lib/transcript-context.js — '(e.g. a 1M-context Opus tier, where the base tier is 200k and the' -> '(e.g. a 1M-context tier, where the base tier is 200k and the'
- scripts/lib/transcript-context.js — ' * `COMPACT_CONTEXT_THRESHOLD=0` disables the context signal entirely;\n * other ' -> ' * `COMPACT_CONTEXT_THRESHOLD=0` disables the context signal entirely;\n * other '
- scripts/lib/transcript-context.js — '  const defaultThreshold = windowTokens >= LARGE_CONTEXT_WINDOW_TOKENS ? DEFAULT' -> '  const defaultThreshold = windowTokens >= LARGE_CONTEXT_WINDOW_TOKENS ? DEFAULT'
- schemas/agent.schema.json — '"haiku", "sonnet", "opus"' -> '"cursor-grok-4.6-high-fast", "grok-4.7-high"'
- schemas/agent.schema.json — 'Claude aliases only in v1' -> 'Grok model slugs only in v1'
- schemas/agent.schema.json — 'agents/*.md Claude frontmatter' -> 'agents/*.md frontmatter'
- schemas/agent.schema.json — 'Claude tool identifiers such as Read, Grep' -> 'tool identifiers such as Read, Grep'
- schemas/agent.schema.json — 'Claude color tag' -> 'color tag'
- scripts/lib/agent-ir.js — "VALID_MODELS = ['haiku', 'sonnet', 'opus']" -> "VALID_MODELS = ['cursor-grok-4.6-high-fast', 'grok-4.7-high']"
- scripts/lib/agent-ir.js — '(expected haiku, sonnet, or opus)' -> '(expected cursor-grok-4.6-high-fast or grok-4.7-high)'
- scripts/lib/agent-ir.js — 'Claude frontmatter markdown' -> 'frontmatter markdown'
- scripts/lib/agent-ir.js — 'Claude agents use comma-separated strings' -> 'Agents use comma-separated strings'
- scripts/lib/agent-emit-pi.js — 'Claude tiers are not valid Pi model ids' -> 'Grok slugs are not valid Pi model ids'
- scripts/lib/agent-emit-pi.js — '# source model tier: opus' -> '# source model tier: grok-4.7-high'
- hooks/adapter.js — 'transformToClaude' -> 'transformToHookPayload'
- hooks/adapter.js — 'CLAUDE_SESSION_ID' -> 'ECC_SESSION_ID'
- hooks/adapter.js — 'not a Claude Code-only or unwired script' -> 'not an unwired script'
- hooks/session-start.js — 'CLAUDE_SESSION_ID' -> 'ECC_SESSION_ID'
- hooks/stop.js — 'CLAUDE_SESSION_ID' -> 'ECC_SESSION_ID'
- hooks/stop.js — removed whole cost-tracker hook if-block (D12)
- commands/model-route.md — '`haiku`' -> '`cursor-grok-4.6-high-fast`'
- commands/model-route.md — '`sonnet`' -> '`grok-4.7-high`'
- commands/model-route.md — '`opus`' -> '`grok-4.7-high`'
- commands/astra-review.md — rewritten prose-only (deep-reasoner blind review; D5)
- skills/gan-style-harness/SKILL.md — "Based on Anthropic's March 2026 harness design paper." -> 'Based on the upstream multi-agent harness design paper (March 2026).'
- skills/gan-style-harness/SKILL.md — '(The upstream `claude -p` invocation path is Claude Code only and does not run i' -> '(In this plugin the harness loop runs in Cursor through `/gan-build` + `/gan-des'
- skills/gan-style-harness/SKILL.md — "> Inspired by [Anthropic's Harness Design for Long-Running Application Developme" -> '> Inspired by the upstream multi-agent harness design paper (March 24, 2026)'
- skills/gan-style-harness/SKILL.md — '**Model:** Sonnet by default; raise via `GAN_PLANNER_MODEL=opus`' -> '**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise vi'
- skills/gan-style-harness/SKILL.md — '| `GAN_PLANNER_MODEL` | `sonnet` |' -> '| `GAN_PLANNER_MODEL` | `cursor-grok-4.6-high-fast` |'
- skills/gan-style-harness/SKILL.md — '**Model:** Sonnet by default; raise via `GAN_GENERATOR_MODEL=opus`' -> '**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise vi'
- skills/gan-style-harness/SKILL.md — '| `GAN_GENERATOR_MODEL` | `sonnet` |' -> '| `GAN_GENERATOR_MODEL` | `cursor-grok-4.6-high-fast` |'
- skills/gan-style-harness/SKILL.md — '**Model:** Sonnet by default; raise via `GAN_EVALUATOR_MODEL=opus`' -> '**Model:** Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`) by default; raise vi'
- skills/gan-style-harness/SKILL.md — '| `GAN_EVALUATOR_MODEL` | `sonnet` |' -> '| `GAN_EVALUATOR_MODEL` | `cursor-grok-4.6-high-fast` |'
- skills/gan-style-harness/SKILL.md — removed section 'Via Shell Script'
- skills/gan-style-harness/SKILL.md — removed section 'Via Claude Code'
- skills/gan-style-harness/SKILL.md — removed section 'Evolution Across Model Capabilities'
- skills/continuous-learning-v2/agents/observer-loop.sh — 'parallel Claude analysis processes' -> 'parallel analysis processes'
- skills/continuous-learning-v2/agents/observer-loop.sh — 'unset CLAUDECODE\n\n' -> ''
- skills/continuous-learning-v2/agents/observer-loop.sh — 'SLEEP_PID=""\nCLAUDE_PID=""\nCLAUDE_PROCESS_GROUP=0\nWATCHDOG_PID=""\n' -> 'SLEEP_PID=""\n'
- skills/continuous-learning-v2/agents/observer-loop.sh — deleted function claude_process_alive (D13)
- skills/continuous-learning-v2/agents/observer-loop.sh — deleted function signal_claude_process (D13)
- skills/continuous-learning-v2/agents/observer-loop.sh — deleted function stop_claude_process (D13)
- skills/continuous-learning-v2/agents/observer-loop.sh — deleted function wait_for_claude_analysis (D13)
- skills/continuous-learning-v2/agents/observer-loop.sh — '  if [ -n "$WATCHDOG_PID" ]; then\n    kill "$WATCHDOG_PID" 2>/dev/null || true\n ' -> ''
- skills/continuous-learning-v2/agents/observer-loop.sh — analyze_observations stubbed (D13)
- skills/plankton-code-quality/SKILL.md — 'Write-time code quality enforcement using Plankton — auto-formatting, linting, a' -> 'Write-time code quality enforcement using Plankton — auto-formatting, linting, a'
- skills/plankton-code-quality/SKILL.md — 'Phase 3: Delegate + Verify' -> 'Phase 3: Report + Verify'
- skills/plankton-code-quality/SKILL.md — '├─ Spawns claude -p subprocess with violations JSON' -> '├─ Reports violations JSON (no auto-fix subprocess since fix #16)'
- skills/plankton-code-quality/SKILL.md — '```bash\n# Install core dependencies\nbrew install jaq ruff uv\n\n# Install Python l' -> '```bash\n# Install core dependencies\nbrew install jaq ruff uv\n\n# Install Python l'
- scripts/lib/utils.js — '/**\n * Get the Claude config directory (alias of getAgentDataHome for backwards ' -> ''
- scripts/lib/utils.js — '  getAgentDataHome,\n  getClaudeDir,\n' -> '  getAgentDataHome,\n'
- scripts/lib/utils.js — 'Log to stderr (visible to user in Claude Code)' -> 'Log to stderr (visible to user)'
- scripts/lib/utils.js — 'Output to stdout (returned to Claude)' -> 'Output to stdout (returned to the agent)'
- scripts/lib/agent-data-home.js — "const CLAUDE_CONFIG_DIR_ENV = 'CLAUDE_CONFIG_DIR';\n" -> ''
- scripts/lib/agent-data-home.js — "const DEFAULT_CLAUDE_DIR_NAME = '.claude';\n" -> ''
- scripts/lib/agent-data-home.js — 'function getDefaultClaudeAgentDataHome() {\n  // Launcher-owned CLAUDE_CONFIG_DIR' -> ''
- scripts/lib/agent-data-home.js — 'within the default Cursor or Claude data directories.' -> 'within the default Cursor data directory.'
- scripts/lib/agent-data-home.js — '  const allowedRoots = [\n    getDefaultCursorAgentDataHome(),\n    getDefaultClau' -> '  const allowedRoots = [\n    getDefaultCursorAgentDataHome(),\n  ];'
- scripts/lib/agent-data-home.js — '    process.env.CLAUDE_PROJECT_DIR,\n' -> ''
- scripts/lib/agent-data-home.js — '  if (options.preferCursorDefault === true || isCursorHookRuntime()) {\n    retur' -> '  // Cursor-only: the default agent data home is ~/.cursor/ecc.\n  // (preferCurs'
- scripts/lib/agent-data-home.js — '  CLAUDE_CONFIG_DIR_ENV,\n' -> ''
- scripts/lib/agent-data-home.js — '  DEFAULT_CLAUDE_DIR_NAME,\n' -> ''
- scripts/lib/agent-data-home.js — '  getDefaultClaudeAgentDataHome,\n' -> ''
- scripts/lib/agent-data-home.js — 'which would create a circular\n * dependency and risk divergent defaults for `~/.' -> 'which would create a circular\n * dependency and risk divergent defaults.'
- scripts/hooks/session-end.js — regex "const \\{[^}]*generateSessionSummary[^}]*\\} = require\\('\\.\\./lib/llm-summary'\\);\\n" (1x)
- scripts/hooks/session-end.js — deleted maybeGenerateLlmSummary (D12)
- scripts/hooks/session-end.js — 'const llmSummary = transcriptPath && summary && transcriptExists ? maybeGenerate' -> 'const llmSummary = null; // LLM summary removed in fix #16 (no Cursor equivalent'
- scripts/hooks/pre-compact.js — "const { generateSessionSummary } = require('../lib/llm-summary');\n" -> ''
- scripts/hooks/pre-compact.js — '/**\n * PreCompact Hook - Save LLM-generated summary before context compaction\n *' -> '/**\n * PreCompact Hook - Log the compaction event before context compaction.\n *\n'
- scripts/hooks/pre-compact.js — removed LLM summary generation block (D12)
- scripts/hooks/pre-compact.js — "const SUMMARY_START_MARKER = '<!-- ECC:SUMMARY:START -->';\n" -> ''
- scripts/hooks/pre-compact.js — "const SUMMARY_END_MARKER = '<!-- ECC:SUMMARY:END -->';\n" -> ''
- scripts/hooks/pre-compact.js — removed now-unused escapeRegExp (D12)
- scripts/lib/resolve-ecc-root.js — "const CURRENT_PLUGIN_SLUG = 'ecc';\n// Legacy install id, kept for existing insta" -> "const CURRENT_PLUGIN_SLUG = 'ecc';\nconst CURRENT_PLUGIN_HANDLE = `${CURRENT_PLUG"
- scripts/lib/resolve-ecc-root.js — "a user's own ~/.claude/skills/ can" -> "a user's own agent data directory's skills/ can"
- scripts/lib/resolve-ecc-root.js — ' * Tries, in order:\n *   1. CLAUDE_PLUGIN_ROOT env var (set by Claude Code for h' -> ' * Tries, in order:\n *   1. ECC_PLUGIN_ROOT env var (set by the host for hooks, '
- scripts/lib/resolve-ecc-root.js — '@param {string} [options.envRoot]  Override CLAUDE_PLUGIN_ROOT (for testing)' -> '@param {string} [options.envRoot]  Override ECC_PLUGIN_ROOT (for testing)'
- scripts/lib/resolve-ecc-root.js — '  const envRoot = options.envRoot !== undefined\n    ? options.envRoot\n    : (pro' -> '  const envRoot = options.envRoot !== undefined\n    ? options.envRoot\n    : (pro'
- scripts/lib/resolve-ecc-root.js — '  const homeDir = options.homeDir || os.homedir();\n  const configuredDir = optio' -> '  const homeDir = options.homeDir || os.homedir();\n'
- scripts/lib/resolve-ecc-root.js — '  // Standard install — files are copied directly into ~/.claude/\n  if (isRoot(c' -> ''
- scripts/lib/resolve-ecc-root.js — removed legacy plugin roots scan (D11)
- scripts/lib/resolve-ecc-root.js — removed plugin cache scan (D11)
- scripts/lib/resolve-ecc-root.js — '  return claudeDir;\n}' -> '  return selfRoot;\n}'
- scripts/lib/resolve-ecc-root.js — removed now-unused convertWindowsPathToWSL loader
- scripts/lib/resolve-ecc-root.js — removed now-unused getInlineWslConversion
- scripts/lib/resolve-ecc-root.js — rewrote buildInlineResolve docstring (Cursor-only)
- scripts/lib/resolve-ecc-root.js — rewrote buildInlineResolve (Cursor-only inline)
- commands/auto-update.md — regenerated inline resolver blob (1x)
- commands/evolve.md — regenerated inline resolver blob (1x)
- commands/instinct-import.md — regenerated inline resolver blob (1x)
- commands/instinct-status.md — regenerated inline resolver blob (1x)
- commands/projects.md — regenerated inline resolver blob (1x)
- commands/promote.md — regenerated inline resolver blob (1x)
- commands/prune.md — regenerated inline resolver blob (1x)
- commands/sessions.md — regenerated inline resolver blob (6x)
- commands/skill-health.md — regenerated inline resolver blob (3x)
- scripts/lib/resolve-ecc-root.js — regenerated inline resolver blob (1x)
- inline resolver blobs regenerated in tree (17 blobs)
- scripts/lib/install-manifests.js — regex 'SUPPORTED_INSTALL_TARGETS\\s*=\\s*\\[[^\\]]*\\]' (1x)
- scripts/lib/install-manifests.js — "LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET[target || 'claude']" -> "LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET[target || 'cursor']"
- scripts/lib/install-executor.js — regex "adapterId:\\s*'claude'" (1x)
- scripts/lib/install-executor.js — regex "target \\|\\| 'claude'" (2x)
- scripts/lib/install/apply.js — regex "\\['claude',\\s*'claude-project'\\]" (1x)
- scripts/lib/install/content-transform.js — regex '[^\\n]*qwen-adapt-agents[^\\n]*\\n' (3x)
- scripts/lib/control-pane/state.js — 'AGENT_OWNER_RE = /(agent|claude|codex|hermes|gemini|opencode|qwen|joycode|codebu' -> 'AGENT_OWNER_RE = /(agent|grok|cursor|\\bbot\\b)/i'
- scripts/lib/install-manifests.js — regex 'const LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET = Object\\.freeze\\(\\{.*?\\n\\}\\);' (1x)
- scripts/lib/install-manifests.js — "const TARGET_DEFAULT_PROFILE_IDS = Object.freeze({\n  opencode: 'opencode',\n});\n" -> ''
- scripts/lib/install-manifests.js — 'const TARGET_DEFAULT_EXCLUSIONS = Object.freeze({\n  opencode: [\n    {\n      modu' -> ''
- scripts/lib/install-manifests.js — replaced function getTargetDefaultProfileId
- scripts/lib/install-manifests.js — replaced function getTargetDefaultExclusions
- scripts/lib/install-manifests.js — '|| LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET.claude;' -> '|| LEGACY_COMPAT_BASE_MODULE_IDS_BY_TARGET.cursor;'
- scripts/lib/install-manifests.js — "    ...(target === 'antigravity'\n      ? []\n      : canonicalLegacyLanguages.fla" -> '    ...canonicalLegacyLanguages.flatMap(language => LEGACY_LANGUAGE_EXTRA_MODULE'
- scripts/lib/install-executor.js — regex 'CLAUDE_ECC_NAMESPACE' (2x)
- scripts/lib/install-executor.js — regex 'planClaudeStyleLegacyInstall' (3x)
- scripts/lib/install-executor.js — regex "'legacy-claude-rules'" (3x)
- scripts/lib/install-executor.js — deleted function planClaudeLegacyInstall
- scripts/lib/install-executor.js — deleted function planClaudeProjectLegacyInstall
- scripts/lib/install-executor.js — deleted function planAntigravityLegacyInstall
- scripts/lib/install-executor.js — '    claudeRulesDir: options.claudeRulesDir || process.env.CLAUDE_RULES_DIR || nu' -> '    cursorRulesDir: options.cursorRulesDir || process.env.CURSOR_RULES_DIR || nu'
- scripts/lib/install-executor.js — "  let plan;\n  if (target === 'claude') {\n    plan = planClaudeLegacyInstall(cont" -> "  let plan;\n  if (target === 'cursor') {\n    plan = planCursorLegacyInstall(cont"
- scripts/lib/install-targets/registry.js — rewritten Cursor-only (D10)
- scripts/lib/install/content-transform.js — rewritten as passthrough (D10/D14)
- scripts/lib/install/request.js — "const LEGACY_INSTALL_TARGETS = ['claude', 'claude-project', 'cursor', 'antigravi" -> "const LEGACY_INSTALL_TARGETS = ['cursor'];"
- scripts/lib/install/request.js — "const target = options.target || config?.target || 'claude';" -> "const target = options.target || config?.target || 'cursor';"
- scripts/lib/install/request.js — "const supportsLocale = target === 'claude' || target === 'claude-project';" -> "const supportsLocale = target === 'cursor';"
- scripts/lib/install/request.js — "throw new Error('--locale can only be used with --target claude or --target clau" -> "throw new Error('--locale can only be used with --target cursor');"
- scripts/lib/install/runtime.js — regex 'claudeRulesDir' (4x)
- scripts/lib/install/plan.js — "const {\n  materializeManagedHooks,\n} = require('./claude-settings');\n" -> ''
- scripts/lib/install/plan.js — deleted function materializeClaudeSettingsOperation
- scripts/lib/install/plan.js — 'function materializeScaffoldOperation(sourceRoot, operation) {\n  if (operation.k' -> 'function materializeScaffoldOperation(sourceRoot, operation) {\n'
- scripts/lib/install/plan.js — "  const applicableTransform = (contentTransform === 'copilot-workflow-paths'\n   " -> '  // Cursor-only: no host frontmatter/workflow transform applies.\n  const applic'
- scripts/lib/install/plan.js — "  const target = options.target || 'claude';" -> "  const target = options.target || 'cursor';"
- scripts/lib/install/plan.js — '    // Persist this projection so install, doctor and repair compare the same\n  ' -> '    // Cursor-only: operations pass through unchanged (no host projection).\n    '
- scripts/lib/install/plan.js — deleted function isSelectedAntigravityLegacyRule
- scripts/lib/install/plan.js — '  const operations = dedupeCopyFileOperations(\n    options.legacyMode && target ' -> '  const operations = dedupeCopyFileOperations(materializedOperations);'
- scripts/lib/install/plan.js — '  // of them target the same path (e.g. a generic `commands/<name>.md` shadowed\n' -> '  // of them target the same path (e.g. a generic `commands/<name>.md` shadowed\n'
- scripts/lib/install-state.js — 'const {\n  CLAUDE_HOOKS_CONFIG_PATH,\n  getClaudeSettingsPath,\n  validateRecordedM' -> ''
- scripts/lib/install-state.js — removed update-claude-settings validation block
- scripts/lib/install/hook-consent.js — "    operation.kind === 'update-claude-settings'\n    || operation.moduleId === HO" -> '    operation.moduleId === HOOK_RUNTIME_MODULE_ID'
- scripts/lib/install/ownership-guard.js — "const { hasEditedCodexUserConfig } = require('./codex-user-config');\n" -> ''
- scripts/lib/install/ownership-guard.js — '    const editedConfig = previousOperation\n      && hasEditedCodexUserConfig(pla' -> '    const editedConfig = false;'
- scripts/lib/install/ownership-guard.js — '  const previousOperation = migration.previousManagedOperations.get(comparablePa' -> '  const previousOperation = migration.previousManagedOperations.get(comparablePa'
- scripts/lib/install/guarded-write.js — "const { sameFileIdentity } = require('./claude-settings-lock');\n" -> '// fix #16 (D10): the file-identity check lived in the deleted\n// claude-setting'
- scripts/lib/install/contained-fs.js — "const { assertClaudeSettingsPath } = require('./claude-settings');\n" -> ''
- scripts/lib/install/contained-fs.js — deleted function assertClaudeSettingsDestination
- scripts/lib/install/contained-fs.js — '  assertClaudeSettingsDestination,\n' -> ''
- scripts/lib/install-targets/helpers.js — regex "const \\{\\n  CLAUDE_HOOKS_CONFIG_PATH,\\n  getClaudeSettingsPath,\\n\\} = require\\('\\.\\./install/claude-settings'\\);\\n" (1x)
- scripts/lib/install-targets/helpers.js — deleted function planClaudeHooksOperations
- scripts/lib/install/plugin-namespace.js — regex '\\(install-apply --target claude\\|claude-project\\)' (1x)
- scripts/lib/install/excluded-paths-reconciliation.js — regex 'and Codex home targets\\)' (1x)
- scripts/lib/session-aliases.js — "const { acquireSettingsLock } = require('./install/claude-settings-lock');" -> "const { acquireFileLock } = require('./install/file-lock');"
- scripts/lib/session-aliases.js — "    release = acquireSettingsLock(aliasesPath, { label: 'session aliases', timeo" -> "    release = acquireFileLock(aliasesPath, { label: 'session aliases', timeoutMs"
- scripts/lib/session-aliases.js — 'Manages session aliases stored in $ECC_AGENT_DATA_HOME/session-aliases.json (def' -> 'Manages session aliases stored in $ECC_AGENT_DATA_HOME/session-aliases.json (def'
- scripts/lib/install/file-lock.js — created (host-neutral file lock, from the deleted claude-settings-lock logic)
- scripts/lib/install/apply.js — 'const {\n  hasExplicitCommitAttributionPreference,\n  withCommitAttributionDisable' -> ''
- scripts/lib/install/apply.js — 'const {\n  getClaudeSettingsPath,\n  mergeManagedHooks,\n  readSettings,\n  runWithS' -> ''
- scripts/lib/install/apply.js — 'const {\n  assertSafeClaudeSkillOperation,\n  prepareClaudeSkillMigration,\n  remov' -> ''
- scripts/lib/install/apply.js — "const { cleanupLegacyAntigravityInstall } = require('./antigravity-legacy-migrat" -> ''
- scripts/lib/install/apply.js — 'const { cleanupLegacyOpencodeInstall, getLegacyLocationForPlan, inspectLegacyOpe' -> '// fix #16 (D10): the OpenCode legacy-migration module is removed\n// (Cursor-onl'
- scripts/lib/install/apply.js — "const { withOpenCodeInstallLocks } = require('./opencode-install-lock');\n" -> ''
- scripts/lib/install/apply.js — "const { assertScriptBoundary, isScriptBoundary } = require('./opencode-script-bo" -> ''
- scripts/lib/install/apply.js — 'function isMarkdownPath(filePath) {' -> 'function uniqueOperations(operations) {\n  const byDestination = new Map();\n  for'
- scripts/lib/install/apply.js — regex '[ \\t]*assertSafeClaudeSkillOperation\\([^;]*;\\n' (5x)
- scripts/lib/install/apply.js — regex 'prepareClaudeSkillMigration\\(plan\\)' (2x)
- scripts/lib/install/apply.js — deleted function shouldSetClaudeCommitAttributionPreference
- scripts/lib/install/apply.js — deleted function writeClaudeCommitAttributionPreference
- scripts/lib/install/apply.js — deleted function preflightClaudeSettingsOperations
- scripts/lib/install/apply.js — deleted function findPreviousManagedHooks
- scripts/lib/install/apply.js — replaced function prepareHookConsentMigration
- scripts/lib/install/apply.js — replaced function assertOpenCodeScriptBoundary
- scripts/lib/install/apply.js — replaced function assertOpenCodeLeaseCoverage
- scripts/lib/install/apply.js — '  preflightClaudeSettingsOperations(appliedPlan);\n' -> ''
- scripts/lib/install/apply.js — "  if (plan.adapter?.target === 'opencode') {\n    assertSafeInstallOperation(plan" -> ''
- scripts/lib/install/apply.js — "  const isClaudeManualTarget = plan.adapter\n    && (plan.adapter.target === 'cla" -> '  return applyInstallPlanLocked(plan, dependencies, false);'
- scripts/lib/install/apply.js — '  const hookRemovalCount = appliedPlan.operations.filter(operation => (\n    oper' -> '  // fix #16 (D12): settings-hook removal is gone; this stays zero.\n  const hook'
- scripts/lib/install/apply.js — removed settings-apply branch from the install loop
- scripts/lib/install/apply.js — '      if (hasLegacyMigration) {\n        removeLegacyClaudeSkillFiles(migration, ' -> ''
- scripts/lib/install/apply.js — '  const hasLegacyMigration = migration.legacyOperationsToRemove.length > 0;\n' -> ''
- scripts/lib/install/apply.js — '      if (shouldSetClaudeCommitAttributionPreference(appliedPlan)) {\n        wri' -> ''
- scripts/lib/install/apply.js — removed legacy Antigravity cleanup block
- scripts/lib/install/apply.js — '  prepareHookConsentMigration,\n' -> '  prepareHookConsentMigration,\n  createDisabledMigration,\n'
- scripts/lib/install-lifecycle.js — "const { withOpenCodeInstallLocks } = require('./install/opencode-install-lock');" -> ''
- scripts/lib/install-lifecycle.js — "const { isCodexUserConfig } = require('./install/codex-user-config');\n" -> ''
- scripts/lib/install-lifecycle.js — "const {\n  prepareClaudeSkillMigration,\n} = require('./install/claude-skill-migra" -> ''
- scripts/lib/install-lifecycle.js — 'const {\n  getLegacyAntigravityLocation,\n  inspectLegacyAntigravityState,\n} = req' -> ''
- scripts/lib/install-lifecycle.js — "const {\n  getLegacyOpencodeLocation,\n  inspectLegacyOpencodeState,\n} = require('" -> ''
- scripts/lib/install-lifecycle.js — 'const {\n  acquireSettingsLock,\n  getClaudeSettingsPath,\n  inspectManagedHooks,\n ' -> ''
- scripts/lib/install-lifecycle.js — '  assertClaudeSettingsDestination,\n' -> ''
- scripts/lib/install-lifecycle.js — deleted function repairClaudeSettings
- scripts/lib/install-lifecycle.js — deleted function uninstallClaudeSettings
- scripts/lib/install-lifecycle.js — deleted function inspectClaudeSettingsOperation
- scripts/lib/install-lifecycle.js — replaced function acquireRepairSettingsLock
- scripts/lib/install-lifecycle.js — "    case 'update-claude-settings':\n      return repairClaudeSettings(operation, " -> ''
- scripts/lib/install-lifecycle.js — "    case 'update-claude-settings':\n      return uninstallClaudeSettings(operatio" -> ''
- scripts/lib/install-lifecycle.js — "    case 'update-claude-settings':\n      return inspectClaudeSettingsOperation(o" -> ''
- scripts/lib/install-lifecycle.js — '  if (operationHealth.invalidSettings.length > 0) {\n    issues.push(\n      build' -> ''
- scripts/lib/install-lifecycle.js — '    ...desiredPlan.operations\n      .filter(operation => (\n        operation.kin' -> ''
- scripts/lib/install-lifecycle.js — "    if (operation.kind === 'update-claude-settings') {\n      const sourcePath = " -> ''
- scripts/lib/install-lifecycle.js — '      if ((isCodexUserConfig(record, operation)\n        || (record.adapter.targe' -> "      if ((record.adapter.target === 'opencode'\n          && require('./install/"
- scripts/lib/install-lifecycle.js — '  const initialMigration = prepareClaudeSkillMigration(trustedPlan);' -> "  const initialMigration = require('./install/apply').createDisabledMigration(tr"
- scripts/lib/install-lifecycle.js — "  const migration = trustedPlan.target === 'opencode'\n    ? require('./install/a" -> '  const migration = guardedMigration;'
- scripts/lib/install-lifecycle.js — removed opencode/antigravity legacy branches from discoverInstalledStates
- scripts/lib/install-lifecycle.js — replaced opencode repair block with an error result
- scripts/lib/install-lifecycle.js — "      if (operations.some(operation => operation.kind === 'update-claude-setting" -> ''
- scripts/lib/install-lifecycle.js — "      const { isScriptBoundary, retainScriptBoundary } = require('./install/open" -> '      // fix #16 (D10): the scripts/package.json boundary copy is produced\n     '
- scripts/lib/session-manager.js — ' * Sessions are stored as markdown files in ~/.claude/session-data/ with\n * lega' -> ' * Sessions are stored as markdown files in ~/.cursor/ecc/session-data/ with\n * '
- scripts/lib/state-store/index.js — "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.claude', 'ecc', 'state.db'" -> "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.ecc', 'state.db');"
- scripts/lib/skill-improvement/observations.js — "  return path.join(resolveProjectRoot(options), '.claude', 'ecc', 'skills');" -> "  return path.join(resolveProjectRoot(options), '.ecc', 'skills');"
- scripts/lib/skill-evolution/tracker.js — "  return path.join(resolveHomeDir(options.homeDir), '.claude', 'state', 'skill-r" -> "  return path.join(resolveHomeDir(options.homeDir), '.cursor', 'ecc', 'state', '"
- scripts/lib/skill-evolution/provenance.js — "    learned: path.join(homeDir, '.claude', 'skills', 'learned'),\n    imported: p" -> "    learned: path.join(homeDir, '.cursor', 'ecc', 'skills', 'learned'),\n    impo"
- scripts/lib/observer-sessions.js — '  const envRoot = process.env.CLAUDE_PROJECT_DIR;' -> '  const envRoot = process.env.CURSOR_PROJECT_DIR;'
- scripts/lib/plan-canvas/sessions.js — '// The producer and the SessionStart/Stop hooks must land on one directory. The\n' -> '// The producer and the SessionStart/Stop hooks must land on one directory. The\n'
- scripts/lib/plan-canvas/sessions.js — "  return path.join(resolveClaudeConfigDir(env), 'plan-canvas');" -> "  return path.join(resolveAgentDataHome(env), 'plan-canvas');"
- scripts/lib/plan-canvas/markdown.js — ' * Renders .claude/plans/*.plan.md artifacts to HTML body content.' -> ' * Renders .ecc/plans/*.plan.md artifacts to HTML body content.'
- scripts/lib/orchestration-session.js — "    coordinationDir: path.join(cwd, '.claude', 'orchestration', targetPath)," -> "    coordinationDir: path.join(cwd, '.ecc', 'orchestration', targetPath),"
- scripts/lib/session-adapters/dmux-tmux.js — "  const coordinationDir = path.resolve(cwd, '.claude', 'orchestration', target);" -> "  const coordinationDir = path.resolve(cwd, '.ecc', 'orchestration', target);"
- scripts/lib/control-pane/state.js — "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.claude', 'ecc', 'state.db'" -> "const DEFAULT_STATE_STORE_RELATIVE_PATH = path.join('.ecc', 'state.db');"
- scripts/lib/control-pane/state.js — "  return path.join(homeDir(env), '.claude', 'ecc2.db');" -> "  return path.join(homeDir(env), '.cursor', 'ecc', 'ecc2.db');"
- scripts/lib/control-pane/state.js — "  const paths = [path.join(home, 'Library', 'Application Support', 'ecc2', 'conf" -> "  const paths = [path.join(home, 'Library', 'Application Support', 'ecc2', 'conf"
- scripts/lib/control-pane/state.js — "    paths.push(path.join(current, '.claude', 'ecc2.toml'));" -> "    paths.push(path.join(current, '.ecc', 'ecc2.toml'));"
- scripts/hooks/hookify-runtime.js — regex "'\\.claude'" (7x)
- scripts/hooks/hookify-runtime.js — regex '\\.claude/' (1x)
- scripts/hooks/mcp-health-check.js — claudeConfigDir() re-pointed to the agent data home (~/.cursor/ecc)
- scripts/hooks/plan-canvas-pending.js — claudeConfigDir() re-pointed to the agent data home (~/.cursor/ecc)
- scripts/hooks/plan-canvas-sessions.js — claudeConfigDir() re-pointed to the agent data home (~/.cursor/ecc)
- scripts/hooks/post-bash-command-log.js — claudeConfigDir() re-pointed to the agent data home (~/.cursor/ecc)
- scripts/hooks/ecc-statusline.js — "    const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '" -> '    const agentDataDir = process.env.ECC_AGENT_DATA_HOME || path.join(os.homedir'
- scripts/hooks/mcp-health-check.js — "  return [\n    path.join(cwd, '.claude.json'),\n    path.join(cwd, '.claude', 'se" -> "  return [\n    path.join(cwd, '.cursor', 'mcp.json'),\n    path.join(home, '.curs"
- scripts/hooks/mcp-health-check.js — '  // SECURITY: cloning a malicious repo must not auto-execute its MCP servers.\n ' -> '  // SECURITY: cloning a malicious repo must not auto-execute its MCP servers.\n '
- scripts/hooks/mcp-health-check.js — "    // A config file in the user's home directory (~/.claude.json or\n    // ~/.c" -> "    // A config file in the user's home directory (~/.cursor/mcp.json) is\n    //"
- scripts/hooks/mcp-health-check.js — "      const isWorkspaceSource = src === pathMod.join(cwd, '.claude.json')\n      " -> "      const isWorkspaceSource = src === pathMod.join(cwd, '.cursor', 'mcp.json')"
- scripts/lib/session-adapters/registry.js — rewritten dmux-tmux only (D10/F2)
- scripts/lib/session-adapters/canonical-session.js — deleted function deriveClaudeWorkerId
- scripts/lib/session-adapters/canonical-session.js — deleted function normalizeClaudeHistorySession
- scripts/lib/session-adapters/canonical-session.js — deleted function normalizeCodexWorktreeSession
- scripts/lib/session-adapters/canonical-session.js — deleted function normalizeOpencodeSession
- scripts/lib/session-adapters/canonical-session.js — '  normalizeClaudeHistorySession,\n' -> ''
- scripts/lib/session-adapters/canonical-session.js — '  normalizeCodexWorktreeSession,\n' -> ''
- scripts/lib/session-adapters/canonical-session.js — '  normalizeOpencodeSession,\n' -> ''
- scripts/lib/context-carriers.js — "const LAYOUTS = Object.freeze({\n  claude: { id: 'claude-plugin@1', skillRoot: 's" -> "const LAYOUTS = Object.freeze({\n  cursor: { id: 'cursor-project@1', skillRoot: '"
- scripts/lib/context-carriers.js — replaced function generatedManifest
- scripts/lib/context-profile-commands.js — "const NATIVE_COMMANDS = ['prepare-native', 'native-status', 'native-rollback', '" -> "const COMMANDS = ['resolve', 'set', 'mode', 'status', 'rollback', 'recover', 'ro"
- scripts/lib/context-profile-commands.js — "  '--target', '--selection', '--include', '--exclude', '--native-root'];" -> "  '--target', '--selection', '--include', '--exclude'];"
- scripts/lib/context-profile-commands.js — "} else if (!arg.startsWith('-') && !result.profileId && ['resolve', 'run', 'set'" -> "} else if (!arg.startsWith('-') && !result.profileId && ['resolve', 'set', 'mode"
- scripts/lib/context-profile-commands.js — "  const taskCommand = ['resolve', 'run'].includes(result.command);" -> "  const taskCommand = result.command === 'resolve';"
- scripts/lib/context-profile-commands.js — "  const allowed = result.command === 'start' ? ['--state-root', '--native-root']" -> "  const allowed = taskCommand\n    ? ['--task-input', '--previous', '--expected-d"
- scripts/lib/context-profile-commands.js — "  if ((NATIVE_COMMANDS.includes(result.command) || result.command === 'start') &" -> ''
- scripts/lib/context-profile-commands.js — "  if (result.command === 'start' && result.json && !result.dryRun) {\n    throw n" -> ''
- scripts/lib/context-profile-commands.js — replaced function execute
- scripts/lib/context-profile-commands.js — "  return { schemaVersion: 'ecc.profile-operation.v1', status: (value.launch?.sta" -> "  return { schemaVersion: 'ecc.profile-operation.v1', status: 'success',\n    sum"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — deleted function getClaudeGlobalConfigPath
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — regex '    getClaudeGlobalConfigPath\\(\\)\\n' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — '  // 2. Check project-specific config (.cursor first, then .claude)\n  for (const' -> "  // 2. Check project-specific config (.cursor)\n  for (const configDir of ['.cur"
- scripts/lib/package-manager.js — Cursor-only config paths (fix #16)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/setup-package-manager.js — '  --project <pm>  Set project preference (saves to .cursor/package-manager.json;' -> '  --project <pm>  Set project preference (saves to .cursor/package-manager.json)'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/setup-package-manager.js — '  console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER || proces' -> "  console.log(`  Environment var: ${process.env.CURSOR_PACKAGE_MANAGER || 'not s"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/setup-package-manager.js — "    console.log('  (Also read from ~/.cursor/package-manager.json and ~/.claude/" -> "    console.log('  (Also read from ~/.cursor/package-manager.json)');"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/setup-package-manager.js — "    console.log('  (An existing .claude/package-manager.json is still honoured o" -> ''
- scripts/setup-package-manager.js — Cursor-only config paths (fix #16)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/resolve-formatter.js — ' * Resolve the runner binary and prefix args for the configured package\n * manag' -> ' * Resolve the runner binary and prefix args for the configured package\n * manag'
- commands/setup-pm.md — Cursor-only package-manager config (fix #16)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/agent-tool-map.js — regex '\\bCLAUDE_TO_PI_TOOLS\\b' (4x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/agent-tool-map.js — "const CLAUDE_MODEL_TIERS = Object.freeze(['haiku', 'sonnet', 'opus']);" -> "const GROK_MODEL_TIERS = Object.freeze(['cursor-grok-4.6-high-fast', 'grok-4.7-h"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/agent-tool-map.js — '  CURSOR_TO_PI_TOOLS,\n  CLAUDE_MODEL_TIERS,' -> '  CURSOR_TO_PI_TOOLS,\n  GROK_MODEL_TIERS,'
- scripts/lib/agent-tool-map.js — CLAUDE_MODEL_TIERS -> GROK_MODEL_TIERS (Grok slugs)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/pre-bash-commit-quality.js — "{ pattern: /sk-ant-[a-zA-Z0-9_-]{20,}/, name: 'Anthropic API key' }," -> "{ pattern: /sk-ant-[a-zA-Z0-9_-]{20,}/, name: 'sk-ant API key' },"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/insaits-security-monitor.py — '  INSAITS_MODEL      LLM model identifier for fingerprinting. Default: claude-op' -> '  INSAITS_MODEL      LLM model identifier for fingerprinting. Default: grok-4.7-'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/insaits-security-monitor.py — 'DEFAULT_MODEL: str = "claude-opus"' -> 'DEFAULT_MODEL: str = "grok-4.7-high"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs — "const MODES = { claude: 'block', codex: 'block', antigravity: 'continue' };" -> "const MODES = { cursor: 'block' };"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs — "if (HOOK !== null && !MODES[HOOK]) { console.error('gate: --hook takes claude, c" -> "if (HOOK !== null && !MODES[HOOK]) { console.error('gate: --hook takes cursor');"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs — regex 'node <skill>/scripts/gate\\.mjs --hook claude\\|codex\\|antigravity' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/scripts/gate.mjs — regex '\\{\\"decision\\":\\"block\\",\\"reason\\":\\.\\.\\.\\} for claude and codex,\\n  \\{' (1x)
- skills/design-taste-frontend/scripts/gate.mjs — hook mode cursor-only (fix #16)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/references/gate.md — '{ "hooks": [ { "type": "command", "command": "node \\"/path/to/skill/scripts/gate' -> '{ "hooks": [ { "type": "command", "command": "node \\"/path/to/skill/scripts/gate'
- skills/design-taste-frontend/references/gate.md — cursor-only hook paths (fix #16)
- skills/design-taste-frontend/assets/icons/index.json — removed array entry 'anthropic'
- skills/design-taste-frontend/assets/icons/index.json — removed array entry 'claude'
- skills/design-taste-frontend/assets/icons/index.json — removed array entry 'claude-code'
- skills/design-taste-frontend/assets/icons/index.json — removed array entry 'codex'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/index.json — regex '  "logos:anthropic\\-icon": \\[\\n(?:   [^\\n]*\\n){4}  \\],\\n' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/index.json — regex '  "logos:claude\\-icon": \\[\\n(?:   [^\\n]*\\n){4}  \\],\\n' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/index.json — regex '  "logos:claude\\-code": \\[\\n(?:   [^\\n]*\\n){4}  \\],\\n' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/index.json — regex '  "logos:codex": \\[\\n(?:   [^\\n]*\\n){4}  \\],\\n' (1x)
- skills/design-taste-frontend/assets/icons/index.json — 4 brand icon entries + viewBox keys removed
- skills/design-taste-frontend/assets/icons/demo/icons-credits.json — removed array entry 'anthropic.svg'
- skills/design-taste-frontend/assets/icons/demo/icons-credits.json — removed array entry 'claude-code.svg'
- skills/design-taste-frontend/assets/icons/demo/icons-credits.json — removed array entry 'claude.svg'
- skills/design-taste-frontend/assets/icons/demo/icons-credits.json — removed array entry 'codex.svg'
- skills/design-taste-frontend/assets/icons/demo/icons-credits.json — 4 brand credit entries removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/layout/heroes.json — '"from": "Anthropic, Stripe Press, Mercury, private banks and advisers"' -> '"from": "Stripe Press, Mercury, private banks and advisers"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/README.md — "The plugin's Node scripts (`/harness-audit`, `/skill-host-compat`, the" -> "The plugin's Node scripts (`/harness-audit`, the"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/package.json — '"description": "Runtime dependencies for the hackathon-ecc Cursor plugin\'s Node ' -> '"description": "Runtime dependencies for the hackathon-ecc Cursor plugin\'s Node '
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/utils.js — ' * leading/trailing hyphens, and removes leading dots so hidden-dir names\n * lik' -> ' * leading/trailing hyphens, and removes leading dots so hidden-dir names\n * lik'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/hooks/after-file-edit.js — regex '\\bclaudeStr\\b' (4x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/evaluate-session.js — '    transcriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;' -> '    transcriptPath = process.env.ECC_TRANSCRIPT_PATH;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/gan-build.md — "This command orchestrates a three-agent build loop inspired by Anthropic's March" -> 'This command orchestrates a three-agent build loop inspired by the upstream mult'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/gan-design.md — 'This is the same mode Anthropic used for their frontend design experiments, wher' -> 'This mode was used for frontend design experiments, with creative breakthroughs '
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-planner.md — regex "\\(inspired by Anthropic's harness design paper, March 2026\\)" (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-generator.md — regex "\\(inspired by Anthropic's harness design paper, March 2026\\)" (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-evaluator.md — regex "\\(inspired by Anthropic's harness design paper, March 2026\\)" (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/rules/hackathon-mode.mdc — '(its upstream `claude -p` invocation path does not run in Cursor' -> '(its upstream CLI-subprocess invocation path does not run in Cursor'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "  // 'everything-claude-code' is the legacy package name, kept for older checkou" -> "  if (['ecc-universal'].includes(packageJson?.name)) {"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "    fileExists(rootDir, '.claude-plugin/plugin.json') &&" -> "    fileExists(rootDir, '.cursor-plugin/plugin.json') &&"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — '// The everything-claude-code entries below are legacy install ids, kept so\n// e' -> 'const ECC_PLUGIN_KEY_PATTERNS = [\n  /^ecc@/i,\n];\n\nconst ECC_LEGACY_PLUGIN_DIRS ='
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "  const pluginJson = path.join(installRoot, '.claude-plugin', 'plugin.json');" -> "  const pluginJson = path.join(installRoot, '.cursor-plugin', 'plugin.json');"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "    path.join(rootDir, '.claude', 'plugins'),\n    ...homeDirs.map(homeDir => pat" -> "    path.join(rootDir, '.cursor', 'plugins'),\n    ...homeDirs.map(homeDir => pat"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "    path.join(rootDir, '.claude', 'plugins', 'installed_plugins.json'),\n    ...h" -> "    path.join(rootDir, '.cursor', 'plugins', 'installed_plugins.json'),\n    ...h"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "  const projectHooks = safeRead(rootDir, '.claude/settings.json');" -> "  const projectHooks = safeRead(rootDir, '.ecc/settings.json');"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      path: '~/.claude/plugins/ecc/ (legacy everything-claude-code paths also su" -> "      path: '~/.cursor/plugins/hackathon-ecc/',"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      path: '.claude/',\n      description: 'Project-specific harness overrides e" -> "      path: '.ecc/',\n      description: 'Project-specific harness overrides exis"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      pass: fileExists(rootDir, 'AGENTS.md') || fileExists(rootDir, 'CLAUDE.md')" -> "      pass: fileExists(rootDir, 'AGENTS.md') || fileExists(rootDir, '.ecc/AGENTS"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      pass: fileExists(rootDir, '.mcp.json') || fileExists(rootDir, '.claude/set" -> "      pass: fileExists(rootDir, '.mcp.json') || fileExists(rootDir, '.ecc/settin"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      path: '.claude/memory.md',\n      description: 'Project memory or durable n" -> "      path: '.ecc/memory.md',\n      description: 'Project memory or durable note"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/harness-audit.js — "      path: '.claude/settings.json',\n      description: 'Project-local hook sett" -> "      path: '.ecc/settings.json',\n      description: 'Project-local hook setting"
- scripts/harness-audit.js — Cursor-only paths + legacy everything-claude-code ids removed
- scripts/lib/harness-capabilities.js — removed array entry 'claude'
- scripts/lib/harness-capabilities.js — removed array entry 'codex'
- scripts/lib/harness-capabilities.js — removed array entry 'kimi'
- scripts/lib/harness-capabilities.js — removed array entry 'antigravity'
- scripts/lib/harness-capabilities.js — removed array entry 'copilot'
- scripts/lib/harness-capabilities.js — removed array entry 'gemini'
- scripts/lib/harness-capabilities.js — removed array entry 'opencode'
- scripts/lib/harness-capabilities.js — removed array entry 'codebuddy'
- scripts/lib/harness-capabilities.js — removed array entry 'joycode'
- scripts/lib/harness-capabilities.js — removed array entry 'qwen'
- scripts/lib/harness-capabilities.js — removed array entry 'zed'
- scripts/lib/harness-capabilities.js — removed array entry 'adal'
- scripts/lib/harness-capabilities.js — removed array entry 'hermes'
- scripts/lib/harness-capabilities.js — removed array entry 'openclaw'
- scripts/lib/harness-capabilities.js — HARNESS_CAPABILITIES narrowed to the cursor entry
- scripts/lib/harness-adapter-compliance.js — removed array entry 'claude-code'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'codex'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'opencode'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'pi'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'gemini'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'zed'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'dmux'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'deepseek-harness'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'orca'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'superset'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'ghast'
- scripts/lib/harness-adapter-compliance.js — removed array entry 'terminal-only'
- scripts/lib/harness-adapter-compliance.js — ADAPTER_RECORDS narrowed to the cursor entry
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/statusline-render.js — 'Inspired by leeguooooo/claude-code-usage-bar (MIT). ECC re-implementation' -> 'Inspired by an open-source usage-bar project (MIT). ECC re-implementation'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/statusline-render.js — ' * @param {string} [claudeDir] selected profile root' -> ' * @param {string} [agentDataDir] selected profile root'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/statusline-render.js — 'function readInstalledPlugins(claudeDir, workspace) {\n  try {\n    const dir = cl' -> 'function readInstalledPlugins(agentDataDir, workspace) {\n  try {\n    const dir ='
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/statusline-render.js — "    const enabled = pluginEnablement([path.join(dir, 'settings.json'),\n      pat" -> "    const enabled = pluginEnablement([path.join(dir, 'settings.json')]);"
- scripts/lib/statusline-render.js — plugin scan re-pointed to ~/.cursor/ecc; .claude settings reads dropped
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — 'ecc memory search "authentication migration" --target-harness codex' -> 'ecc memory search "authentication migration" --target-harness cursor'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — '    --source-harness codex \\' -> '    --source-harness cursor \\'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — '  --from codex \\\n  --target claude \\' -> '  --from cursor \\\n  --target cursor \\'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — 'ECC_MEMORY_HARNESS=codex ecc-memory-mcp' -> 'ECC_MEMORY_HARNESS=cursor ecc-memory-mcp'
- skills/unified-memory/SKILL.md — narrowed to Cursor-only
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/context-budget/SKILL.md — regex '\\| Codex CLI \\(Codex only\\)[^\\n]*\\n' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/context-budget/SKILL.md — regex '\\| Codex app \\(Codex only\\)[^\\n]*\\n' (1x)
- skills/context-budget/SKILL.md — Codex rows/link removed; Cursor meter kept
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ai-feature-spec/SKILL.md — '  compatible_with:\n  - claude-code\n  - codex\n' -> '  compatible_with:\n  - cursor\n'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/polish-pass/reference/impeccable-critique.md — 'Run Assessment A alone in this context and skip both sub-agent gates below, the ' -> 'Run Assessment A alone in this context and skip both sub-agent gates below: with'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/integration/SKILL.md — '- `integrations` by whawkinsiv (claude-code-skills): NOT used.' -> "- `integrations` by whawkinsiv (whawkinsiv's skills repo): NOT used."
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/feature-expansion/SKILL.md — '- **claude-handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the ex' -> '- **handoff** (`cliffordcollinsglobal/agent-skills`, no license) — the execution'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-scout/SKILL.md — 'grep -RilE "keyword|synonym" ~/.cursor/skills ~/.cursor/plugins/marketplaces ~/.' -> 'grep -RilE "keyword|synonym" ~/.cursor/skills ~/.cursor/plugins/marketplaces 2>/'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — '# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.claude/skills so the' -> '# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.ecc/skills so the'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — '#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.claude/skills (for testing only;' -> '#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.cursor/skills (for testing only;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — regex '\\$HOME/\\.claude/skills' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — regex '\\$PWD/\\.claude/skills' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — regex '\\*/\\.claude/skills\\*' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — regex '\\.claude/skills' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/scan.sh — 'OBSERVATIONS="${SKILL_STOCKTAKE_OBSERVATIONS:-$HOME/.claude/observations.jsonl}"' -> 'OBSERVATIONS="${SKILL_STOCKTAKE_OBSERVATIONS:-$HOME/.cursor/ecc/observations.jso'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — '# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.claude/skills so the' -> '# When CWD_SKILLS_DIR is omitted, defaults to $PWD/.ecc/skills so the'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — '#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.claude/skills (for testing only;' -> '#   SKILL_STOCKTAKE_GLOBAL_DIR   Override ~/.cursor/skills (for testing only;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — regex '\\$HOME/\\.claude/skills' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — regex '\\$PWD/\\.claude/skills' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — regex '\\*/\\.claude/skills\\*' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-stocktake/scripts/quick-diff.sh — regex '\\.claude/skills' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh — regex '\\$HOME/\\.claude/skills' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh — regex '\\$PWD/\\.claude/skills' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh — regex '\\*/\\.claude/skills\\*' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh — regex '\\.claude/skills' (3x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh — regex '\\$HOME/\\.claude/rules' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-rules.sh — regex '\\.claude/rules' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/SKILL.md — 'bash ~/.claude/skills/rules-distill/scripts/scan-skills.sh' -> 'bash "$ECC_PLUGIN_ROOT/skills/rules-distill/scripts/scan-skills.sh"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/SKILL.md — 'bash ~/.claude/skills/rules-distill/scripts/scan-rules.sh' -> 'bash "$ECC_PLUGIN_ROOT/skills/rules-distill/scripts/scan-rules.sh"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/repo-scan/SKILL.md — 'REPO_SCAN_INSTALL_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/repo-scan"' -> 'REPO_SCAN_INSTALL_DIR="$ECC_PLUGIN_ROOT/skills/repo-scan"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/delivery-gate/hooks/quality-gate.py — "    cwd = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())" -> "    cwd = os.environ.get('CURSOR_PROJECT_DIR', os.getcwd())"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/delivery-gate/hooks/quality-gate.py — "    mem = os.path.expanduser(f'~/.claude/projects/{safe}/memory')" -> "    mem = os.path.expanduser(f'~/.cursor/ecc/projects/{safe}/memory')"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ecc-recipes/SKILL.md — '  "$HOME"/.claude/plugins/marketplaces/ecc/commands \\\n  "$HOME"/.claude/plugins/' -> '  "$HOME"/.cursor/plugins/local/hackathon-ecc/commands \\\n  "$HOME"/.cursor/plugi'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/living-docs-governance/SKILL.md — '- Codex and harness-neutral projects commonly use `AGENTS.md`.' -> '- Harness-neutral projects commonly use `AGENTS.md`.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/codehealth-mcp/SKILL.md — 'Paste into the project `AGENTS.md` or `CLAUDE.md`:' -> 'Paste into the project `AGENTS.md`:'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/browser-qa/SKILL.md — 'description: "Run automated post-deploy UI verification with a browser automatio' -> 'description: "Run automated post-deploy UI verification with a browser automatio'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/browser-qa/SKILL.md — 'Uses the browser automation MCP (claude-in-chrome, Playwright, or Puppeteer) to ' -> 'Uses the browser automation MCP (Playwright or Puppeteer) to interact with live '
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/browser-qa/SKILL.md — '- `mChild__claude-in-chrome__*` tools (preferred — uses your actual Chrome)\n' -> ''
- skills/browser-qa/SKILL.md — claude-in-chrome MCP removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/SKILL.md — regex '\\$\\{CLAUDE_SKILL_DIR\\}' (10x)
- skills/ck/SKILL.md — storage re-pointed to ~/.cursor/ecc/ck
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/strategic-compact/SKILL.md — 'Do not copy the block below into your `hooks/hooks.json` — `~/.claude/scripts/` ' -> 'Do not copy the block below into your `hooks/hooks.json` — plugin scripts live u'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/strategic-compact/SKILL.md — '| Memory files (`~/.claude/memory/`) | Multi-step conversation context |' -> "| Memory files (the agent's memory directory) | Multi-step conversation context "
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/strategic-compact/SKILL.md — '> `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` brings them back, but that is a per-machine\n' -> '> The tools cannot be re-enabled from this skill — **they do not travel with it*'
- skills/strategic-compact/SKILL.md — auto-compact/env + path re-points
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/SKILL.md — '  "learned_skills_path": "~/.claude/skills/learned/",' -> '  "learned_skills_path": "~/.cursor/ecc/skills/learned/",'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/SKILL.md — 'Add to your `~/.claude/settings.json`:' -> 'The plugin registers this hook itself via `hooks/hooks.json`; for a manual insta'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/SKILL.md — '        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"' -> '        "command": "$ECC_PLUGIN_ROOT/skills/continuous-learning/evaluate-session'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/config.json — '  "learned_skills_path": "~/.claude/skills/learned/",' -> '  "learned_skills_path": "~/.cursor/ecc/skills/learned/",'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — '# Hook config (in ~/.claude/settings.json):' -> "# Hook config (registered via the plugin's hooks/hooks.json):"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — '#         "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"' -> '#         "command": "$ECC_PLUGIN_ROOT/skills/continuous-learning/evaluate-sessi'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — '# Extracted skills saved to: ~/.claude/skills/learned/' -> '# Extracted skills saved to: ~/.cursor/ecc/skills/learned/'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — 'LEARNED_SKILLS_PATH="${HOME}/.claude/skills/learned"' -> 'LEARNED_SKILLS_PATH="${HOME}/.cursor/ecc/skills/learned"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — '    LEARNED_SKILLS_PATH=$(jq -r \'.learned_skills_path // "~/.claude/skills/learn' -> '    LEARNED_SKILLS_PATH=$(jq -r \'.learned_skills_path // "~/.cursor/ecc/skills/l'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning/evaluate-session.sh — '  transcript_path="${CLAUDE_TRANSCRIPT_PATH:-}"' -> '  transcript_path="${ECC_TRANSCRIPT_PATH:-}"'
- skills/continuous-learning — paths re-pointed to ~/.cursor/ecc/skills/learned
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — '| Storage | Global (`~/.claude/homunculus/`) | Project-scoped (`${XDG_DATA_HOME:' -> '| Storage | Global (`~/.local/share/ecc-homunculus/`) | Project-scoped (`${XDG_D'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — '1. **`CLAUDE_PROJECT_DIR` env var** (highest priority) -- honored as an explicit' -> '1. **`CURSOR_PROJECT_DIR` env var** (highest priority) -- honored as an explicit'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — 'Existing users with data at `~/.claude/homunculus` can migrate once:\n\n```bash\nba' -> ''
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — 'If you previously copied `observe.sh` into `~/.claude/settings.json`, remove tha' -> 'If you previously copied `observe.sh` into a host settings file, remove that dup'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — regex '"command": "~/\\.claude/skills/continuous-learning-v2/hooks/observe\\.sh"' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — '- Existing global instincts can be migrated from `~/.claude/homunculus/instincts' -> ''
- skills/continuous-learning-v2/SKILL.md — paths/env re-pointed; migration lines removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/detect-project.sh — regex '\\bCLAUDE_PROJECT_DIR\\b' (8x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/instinct-cli.py — regex '\\bCLAUDE_PROJECT_DIR\\b' (3x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/instinct-cli.py — '    _warn_legacy_data()\n' -> ''
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/instinct-cli.py — 'def _warn_legacy_data() -> None:\n    """Warn if legacy ~/.claude/homunculus/ con' -> ''
- skills/continuous-learning-v2/scripts/instinct-cli.py — CURSOR_PROJECT_DIR; legacy-data warning removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/test_parse_instinct.py — regex '\\bCLAUDE_PROJECT_DIR\\b' (5x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/scripts/test_parse_instinct.py — '    homunculus = tmp_path / ".claude" / "homunculus"' -> '    homunculus = tmp_path / ".ecc" / "homunculus"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — '# Can also be registered manually in ~/.claude/settings.json.' -> '# Can also be registered manually in a host settings file.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — '  case "${CLAUDE_HOOK_EVENT_NAME:-}" in' -> '  case "${ECC_HOOK_EVENT_NAME:-}" in'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — '    export CLAUDE_PROJECT_DIR="$_GIT_ROOT"' -> '    export CURSOR_PROJECT_DIR="$_GIT_ROOT"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — '    unset CLAUDE_PROJECT_DIR' -> '    unset CURSOR_PROJECT_DIR'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — 'case "${CLAUDE_CODE_ENTRYPOINT:-cli}" in\n  cli|sdk-ts|sdk-cli|claude-desktop|cla' -> 'case "${ECC_ENTRYPOINT:-cli}" in\n  cli|sdk-ts|sdk-cli|cursor) ;;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — '_ECC_SKIP_PATHS="${ECC_OBSERVE_SKIP_PATHS:-observer-sessions,.claude-mem}"' -> '_ECC_SKIP_PATHS="${ECC_OBSERVE_SKIP_PATHS:-observer-sessions,.ecc-mem}"'
- skills/continuous-learning-v2/hooks/observe.sh — Cursor env names
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/session-guardian.sh — '#   OBSERVER_LAST_RUN_LOG        default: ~/.claude/observer-last-run.log' -> '#   OBSERVER_LAST_RUN_LOG        default: ~/.cursor/ecc/observer-last-run.log'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/session-guardian.sh — 'LOG_PATH="${OBSERVER_LAST_RUN_LOG:-$HOME/.claude/observer-last-run.log}"' -> 'LOG_PATH="${OBSERVER_LAST_RUN_LOG:-$HOME/.cursor/ecc/observer-last-run.log}"'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/start-observer.sh — '# to prevent claude CLI failures from killing the observer loop.' -> '# to prevent agent CLI failures from killing the observer loop.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/observer-loop.sh — regex '# `claude` CLI, which has no Cursor equivalent\\.' (1x)
- skills/ecc-recipes/SKILL.md — regex '[^\\n]*multi-plan[^\\n]*\\n' (1x)
- skills/ecc-recipes/SKILL.md — regex '[^\\n]*santa-loop[^\\n]*\\n' (2x)
- commands/plan.md — 'for a dual-model (Codex/Antigravity) plan use /multi-plan' -> 'for a second deep-reasoner verification pass, dispatch a fresh deep-reasoner sub'
- rules/common-git-workflow.mdc — 'describes Claude Code installs' -> 'describes Cursor installs'
- rules/common-hooks.mdc — regex '[^\\n]*\\.claude/settings\\.json[^\\n]*\\n' (1x)
- skills/strategic-compact/SKILL.md — 'Fable 5, Mythos 5 and newer models' -> 'current models and newer'
- skills/continuous-learning/SKILL.md — regex '`~/.claude/skills/learned/`' (2x)
- skills/continuous-learning-v2/SKILL.md — regex '`~/.claude/skills/learned/`' (1x)
- manifests/install-modules.json:commands-core paths trimmed (8 -> 5)
- manifests/install-modules.json:workflow-quality paths trimmed (46 -> 43)
- manifests/install-modules.json — all module targets narrowed to ['cursor']
- manifests/pi-core.json:skills.exclude:council-multi-model removed
- manifests/pi-core.json:skills.exclude:skill-comply removed
- manifests/pi-core.json:skills.exclude:config-gc removed
- manifests/pi-core.json:skills.exclude:claude-devfleet removed
- manifests/pi-core.json:commands.exclude:multi-backend.md removed
- manifests/pi-core.json:commands.exclude:multi-execute.md removed
- manifests/pi-core.json:commands.exclude:multi-frontend.md removed
- manifests/pi-core.json:commands.exclude:multi-plan.md removed
- manifests/pi-core.json:commands.exclude:multi-workflow.md removed
- manifests/pi-core.json:commands.exclude:santa-loop.md removed
- manifests/pi-core.json:commands.exclude:cost-report.md removed
- manifests/pi-core.json:commands.exclude:skill-host-compat.md removed
- manifests/pi-core.json:commands.exclude:loop-status.md removed
- manifests/pi-core.json — deleted-feature entries removed; 'Cursor-Code-only' prefixes stripped; astra-review reason reworded to Grok review
- schemas/provenance.schema.json — 'Required in ~/.claude/skills/learned/* and ~/.claude/skills/imported/*' -> 'Required in ~/.cursor/ecc/skills/learned/* and ~/.cursor/ecc/skills/imported/*'
- schemas/context-carrier.schema.json — schema enum narrowed to ['cursor']
- schemas/context-carrier.schema.json — schema enum host entries dropped: ['pi-package@1', 'opencode-project@1', 'cursor-project@1']
- schemas/context-carrier.schema.json — schema enum host entries dropped: ['package.json']
- schemas/context-carrier.schema.json — schema enum narrowed to ['cursor']
- schemas/ecc-install-config.schema.json — schema enum narrowed to ['cursor']
- schemas/install-modules.schema.json — schema enum narrowed to ['cursor']
- schemas/install-state.schema.json — schema update-claude-settings conditional removed
- schemas/install-state.schema.json — schema update-claude-settings conditional removed
- generic pass — 189 files changed by mechanical rules
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — '// Config file path (host-aware agent data home: ~/.cursor/ecc in Cursor,\n// ~/.' -> '// Config file path (host-aware agent data home: ~/.cursor/ecc —\n// see scripts/'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — ' * Tries the host-aware config path first, then the explicit Cursor\n * (~/.curso' -> ' * Tries the host-aware config path first, then the explicit Cursor\n * (~/.curso'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — ' * 1. Environment variable CURSOR_PACKAGE_MANAGER (Cursor) or\n *    CLAUDE_PACKA' -> ' * 1. Environment variable CURSOR_PACKAGE_MANAGER\n * 2. Project-specific config '
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — '  // 1. Check environment variable (Cursor first, then Cursor)\n  const envPm = p' -> '  // 1. Check environment variable\n  const envPm = process.env.CURSOR_PACKAGE_MA'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — " * Set user's preferred package manager (global). Saved to the host-aware\n * con" -> " * Set user's preferred package manager (global). Saved to the host-aware\n * con"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — " * Set project's preferred package manager.\n * Saved to .cursor/package-manager." -> " * Set project's preferred package manager.\n * Saved to .cursor/package-manager."
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.js — "  message += '  - Global: Set CURSOR_PACKAGE_MANAGER (Cursor) or CLAUDE_PACKAGE_" -> "  message += '  - Global: Set CURSOR_PACKAGE_MANAGER environment variable\\n';\n  "
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/setup-package-manager.js — '                  ~/.cursor/ecc/package-manager.json in Cursor,\n                ' -> '                  ~/.cursor/ecc/package-manager.json;\n                  ~/.curso'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/tdd-workflow/SKILL.md — 'It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSO' -> 'It resolves the package manager (npm / pnpm / yarn / bun) from, in order: `CURSO'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/setup-pm.md — '1. **Environment variable**: `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAG' -> '1. **Environment variable**: `CURSOR_PACKAGE_MANAGER`'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/setup-pm.md — '5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.jso' -> '5. **Global config**: host-aware config path (`~/.cursor/ecc/package-manager.jso'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/setup-pm.md — '// Cursor: ~/.cursor/ecc/package-manager.json\n// (also read from ~/.cursor/packa' -> '// Cursor: ~/.cursor/ecc/package-manager.json\n// (also read from ~/.cursor/packa'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/setup-pm.md — '// Cursor: .cursor/package-manager.json\n// (an existing .ecc/package-manager.jso' -> '// Cursor: .cursor/package-manager.json\n'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/setup-pm.md — 'Set `CURSOR_PACKAGE_MANAGER` (Cursor) or `CLAUDE_PACKAGE_MANAGER` (Cursor\nCode) ' -> 'Set `CURSOR_PACKAGE_MANAGER` to override all other detection methods:'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/references/gate.md — 'command is one POSIX `sh` line (Git Bash on Windows, `sh` on macOS and Linux) th' -> 'command is one POSIX `sh` line (Git Bash on Windows, `sh` on macOS and Linux) th'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — 'description: Share durable, inspectable context and handoffs between Cursor, Cod' -> 'description: Share durable, inspectable context and handoffs between Cursor agen'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/unified-memory/SKILL.md — '- Hand work from Cursor to Codex, Hermes to Cursor, or any other harness pair.' -> '- Hand work between Cursor agents in the same project.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/context-budget/SKILL.md — 'description: Routes live context checks to the native Codex or Cursor meter with' -> 'description: Routes live context checks to the native Cursor meter without scann'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/context-budget/SKILL.md — 'These commands are documented in the [Codex command reference](https://developer' -> 'These commands are documented in the Cursor command reference.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/app-scaffold/SKILL.md — "- **Reuse across projects:** copy this `app-scaffold/` folder into any project's" -> "- **Reuse across projects:** copy this `app-scaffold/` folder into any project's"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/skill-scout/SKILL.md — '# Cursor (this skill also works there) — same searches under ~/.claude\nfind ~/.c' -> '# Cursor — same searches under ~/.cursor\nfind ~/.cursor/skills -maxdepth 2 -name'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/codehealth-mcp/SKILL.md — '**Cursor** (`~/.claude.json` → `mcpServers`):' -> '**Cursor** (`~/.cursor/mcp.json` → `mcpServers`):'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/SKILL.md — "(Cursor only — this skill uses Cursor's SessionStart hook and ~/.claude/ck stora" -> "(Cursor only — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc/ck s"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/SKILL.md — "> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.claude/ck " -> "> **Cursor only** — this skill uses Cursor's SessionStart hook and ~/.cursor/ecc"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/strategic-compact/SKILL.md — "- `CLAUDE_CODE_AUTO_COMPACT_WINDOW` — Cursor's native auto-compact trigger, whic" -> '- `ECC_CONTEXT_WINDOW_TOKENS` — an explicit override for the context window, use'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/strategic-compact/SKILL.md — '- Same rules in both `~/.claude/rules/` and project `.ecc/rules/`' -> '- Same rules in both `~/.cursor/rules/` and project `.ecc/rules/`'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — "Continuous-learning-v2 stores observer data outside `~/.claude` so Cursor's sens" -> 'Continuous-learning-v2 stores observer data under `~/.local/share/ecc-homunculus'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/SKILL.md — '**If installed manually in Cursor** to `~/.claude/skills`, add this to your `~/.' -> '**If installed manually** to `~/.cursor/skills`, add this to your hook config:'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh — "# wrapper's positional phase argument, but Cursor still exposes the hook\n# event" -> "# wrapper's positional phase argument, but the hook event name is\n# available in"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/session-guardian.sh — '# Called by observer-loop.sh before spawning any Cursor session.' -> '# Called by observer-loop.sh before spawning any agent session.'
- skills/security-scan/SKILL.md — Deep Analysis section removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/gan-style-harness/SKILL.md — '- Quick single-file fixes (Cursor only — use standard `claude -p` there; in this' -> '- Quick single-file fixes (use the Cursor agent loop, never a CLI subprocess)'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/gan-style-harness/SKILL.md — "Based on Anthropic's published results:" -> "Based on the upstream harness paper's published results:"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/gan-style-harness/SKILL.md — '- [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/en' -> '- Harness Design for Long-Running Apps (upstream multi-agent harness design pape'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/gan-style-harness/SKILL.md — '- [Epsilla: The GAN-Style Agent Loop](https://www.epsilla.com/blogs/anthropic-ha' -> '- Epsilla: The GAN-Style Agent Loop — Architecture deconstruction'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-planner.md — regex 'the upstream `claude -p` path is Cursor only and is never executed here' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-generator.md — regex 'the upstream `claude -p` path is Cursor only and is never executed here' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-gan-evaluator.md — regex 'the upstream `claude -p` path is Cursor only and is never executed here' (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/laravel-plugin-discovery/SKILL.md — 'In Cursor, add the same entry to your `~/.claude.json` `mcpServers`' -> 'In Cursor, add the same entry to your `~/.cursor/mcp.json` `mcpServers`'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/council/SKILL.md — 'Do **not** write ad-hoc notes to `~/.claude/notes` or other shadow paths from th' -> "Do **not** write ad-hoc notes to the agent's notes directory or other shadow pat"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/mcp-health-check.js — '// `~/.claude-work` resolves to one place rather than two.' -> '// `~/some-dir` resolves to one place rather than two.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/commands/init.mjs — regex '\\bclaudeMd\\b' (7x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/commands/shared.mjs — "resolve(homedir(), '.claude', 'ck')" -> "resolve(homedir(), '.cursor', 'ecc', 'ck')"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/commands/shared.mjs — "resolve(homedir(), '.claude', 'projects', encoded, 'memory')" -> "resolve(homedir(), '.cursor', 'ecc', 'projects', encoded, 'memory')"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — "resolve(homedir(), '.claude', 'ck')" -> "resolve(homedir(), '.cursor', 'ecc', 'ck')"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — '// Resolve SKILL.md next to this hook, so plugin installs work as well as ~/.cla' -> '// Resolve SKILL.md next to this hook, so plugin installs work as well as ~/.cur'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — regex '\\bextractClaudeMdGoal\\b' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — regex '\\bclaudeMdGoal\\b' (4x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — '// The host does not expand ${CLAUDE_SKILL_DIR} in hook output, so fill it in he' -> '// The host does not expand ${ECC_PLUGIN_ROOT}/skills/ck in hook output, so fill'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ck/hooks/session-start.mjs — ".replaceAll('${CLAUDE_SKILL_DIR}', () => shellSkillDir)" -> ".replaceAll('${ECC_PLUGIN_ROOT}/skills/ck', () => shellSkillDir)"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/agents/ecc-opensource-packager.md — 'claude    # Start Cursor — reads AGENTS.md automatically' -> '# Start Cursor in this project — it reads AGENTS.md automatically'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/evolve.md — '   - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with' -> '   - Legacy homunculus data is not read (the migration script was removed in fix'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/sessions.md — '- Aliases are stored in `~/.claude/session-aliases.json` (Cursor only)' -> '- Aliases are stored in `~/.cursor/ecc/session-aliases.json` (Cursor only)'
- skills/design-taste-frontend/references/gate.md — Codex hooks section removed
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install/apply.js — deleted function preflightQwenAgentOperations
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install/apply.js — regex '  preflightQwenAgentOperations\\(plan\\);\\n' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install/apply.js — "// 'remove-claude-settings-hooks' removal both targeted host" -> '// settings-hooks removal both targeted host'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install-lifecycle.js — '  // update-claude-settings operations, which Cursor installs never' -> '  // host settings-update operations, which Cursor installs never'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/demo.html — regex '<span class="ic-chip" title="(anthropic|claude|claude-code|codex)">.*?</span>' (4x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/assets/icons/demo.html — 'AI <span class="muted">53</span>' -> 'AI <span class="muted">49</span>'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/plankton-code-quality/SKILL.md — '| Model routing | Manual (`/model opus`) | Automatic (violation complexity → tie' -> '| Model routing | Manual (`/model grok-4.7-high`) | Automatic (violation complex'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/plankton-code-quality/SKILL.md — '      "haiku":  { "timeout": 120, "max_turns": 10 },\n      "sonnet": { "timeout"' -> '      "cursor-grok-4.6-high-fast": { "timeout": 300, "max_turns": 10 },\n      "g'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/auto-update.js — "// 'everything-claude-code' is the legacy 1.x package name, kept for existing ch" -> ''
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/auto-update.js — "const ECC_PACKAGE_NAMES = new Set(['ecc-universal', 'everything-claude-code']);" -> "const ECC_PACKAGE_NAMES = new Set(['ecc-universal']);"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/hook-flags.js — '  const raw = env.ECC_HOOKS_ENABLED !== undefined\n    ? env.ECC_HOOKS_ENABLED\n  ' -> '  const raw = env.ECC_HOOKS_ENABLED !== undefined\n    ? env.ECC_HOOKS_ENABLED\n  '
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/hook-flags.js — '  const selected = env.ECC_HOOK_PROFILE !== undefined\n    ? env.ECC_HOOK_PROFILE' -> '  const selected = env.ECC_HOOK_PROFILE !== undefined\n    ? env.ECC_HOOK_PROFILE'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/schemas/context-carrier.schema.json — '              "enum": [\n                "pi-package@1",\n                "opencod' -> '              "enum": [\n                "cursor-project@1"\n              ]'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/schemas/context-carrier.schema.json — '              "enum": [\n                "skills",\n                ".opencode/ski' -> '              "enum": [\n                ".cursor/skills"\n              ]'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/schemas/context-carrier.schema.json — '              "enum": [\n                null,\n                ".ecc-plugin/plugi' -> '              "enum": [\n                null\n              ]'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/session-adapters/registry.js — '// fix #16 (D10/F2): session adapters are dmux-tmux only. The Cursor-history,\n//' -> '// fix #16 (D10/F2): session adapters are dmux-tmux only. The other host\n// adap'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install-targets/helpers.js — "const PLATFORM_SOURCE_PATH_OWNERS = Object.freeze({\n  '.claude-plugin': 'claude'" -> "const PLATFORM_SOURCE_PATH_OWNERS = Object.freeze({\n  '.cursor': 'cursor',\n});"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install-targets/helpers.js — '// Source paths that home installs must never copy into a harness home\n// direct' -> '// Source paths that home installs must never copy into a harness home\n// direct'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install-targets/helpers.js — '  planClaudeHooksOperations,\n' -> ''
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/harness-adapter-compliance.js — '// rules/common/, .claude-plugin/plugin.json,' -> '// rules/common/,'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/agent-tool-map.js — regex '\\bclaudeTool\\b' (3x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install/guarded-write.js — '// claude-settings-lock module; it is a generic dev+ino comparison.' -> '// file-lock module; it is a generic dev+ino comparison.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/resolve-ecc-root.js — '  // otherwise a scripts-only ~/.claude short-circuits and every skill path' -> '  // otherwise a scripts-only agent-data short-circuits and every skill path'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/resolve-ecc-root.js — '  // is no ~/.claude and no ECC_PLUGIN_ROOT, so all the probing above' -> '  // is no agent data home and no ECC_PLUGIN_ROOT, so all the probing above'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-turn-scan.js — "/** Transcript path from the hook payload or CLAUDE_TRANSCRIPT_PATH; '' when non" -> "/** Transcript path from the hook payload or ECC_TRANSCRIPT_PATH; '' when none. "
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-turn-scan.js — 'process.env.CLAUDE_TRANSCRIPT_PATH' -> 'process.env.ECC_TRANSCRIPT_PATH'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — "const INSTRUCTION_BASENAMES = new Set([\n  'claude.md',\n  'agents.md',\n  'agent.m" -> "const INSTRUCTION_BASENAMES = new Set([\n  'agents.md',\n  'agent.md',\n  'skill.md"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — "const INSTRUCTION_DIRS = new Set(['.claude', 'agents', 'commands', 'skills', 'ru" -> "const INSTRUCTION_DIRS = new Set(['agents', 'commands', 'skills', 'rules', 'hook"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — 'const WORKTREE_PREFIX_PATTERN = /^\\.claude\\/worktrees\\/([^/]+)\\//;' -> 'const WORKTREE_PREFIX_PATTERN = /^\\.ecc\\/worktrees\\/([^/]+)\\//;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — regex 'process\\.env\\.CLAUDE_PROJECT_DIR' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — "  return fs.existsSync(paths.join(rootNative, '.claude', 'worktrees', name, '.gi" -> "  return fs.existsSync(paths.join(rootNative, '.ecc', 'worktrees', name, '.git')"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-target-class.js — "  loader: 'Name the harness/loader that reads this file (Cursor, Codex, Cursor, " -> "  loader: 'Name the harness/loader that reads this file (Cursor, …) and when it "
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/gateguard-search-evidence.js — 'process.env.CLAUDE_PROJECT_DIR' -> 'process.env.CURSOR_PROJECT_DIR'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — regex 'process\\.env\\.CLAUDE_PROJECT_DIR' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — 'const transcriptPath = (data && (data.transcript_path || data.transcriptPath)) |' -> 'const transcriptPath = (data && (data.transcript_path || data.transcriptPath)) |'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — 'function isClaudeSettingsPath(filePath) {\n  const normalized = normalizeForMatch' -> 'function isAgentSettingsPath(filePath) {\n  const normalized = normalizeForMatch('
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — regex '\\bisClaudeSettingsPath\\b' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/gateguard-fact-force.js — "  if (isAgentSettingsPath(filePath)) return 'claude-settings';" -> "  if (isAgentSettingsPath(filePath)) return 'agent-settings';"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/context-selection.js — regex "target = 'codex'" (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/context-profiles.js — regex "target = 'codex'" (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/context-profile-support.js — regex "target = 'codex'" (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/context-pack-registry.js — regex "target = 'codex'" (1x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/utils.d.ts — ' * Defaults to ~/.claude; override with ECC_AGENT_DATA_HOME (e.g. ~/.cursor/ecc)' -> ' * Defaults to ~/.cursor/ecc; override with ECC_AGENT_DATA_HOME.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/session-manager.d.ts — ' * ~/.claude/session-data/ with legacy read compatibility for ~/.claude/sessions' -> ' * ~/.cursor/ecc/session-data/ with legacy read compatibility for ~/.cursor/ecc/'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/session-aliases.d.ts — ' * Manages named aliases for session files, stored in $ECC_AGENT_DATA_HOME/sessi' -> ' * Manages named aliases for session files, stored in $ECC_AGENT_DATA_HOME/sessi'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.d.ts — ' * 1. CLAUDE_PACKAGE_MANAGER environment variable' -> ' * 1. CURSOR_PACKAGE_MANAGER environment variable'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.d.ts — ' * 5. Global user preference (~/.claude/package-manager.json)' -> ' * 5. Global user preference (~/.cursor/package-manager.json)'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.d.ts — ' * Saves to ~/.claude/package-manager.json.' -> ' * Saves to ~/.cursor/package-manager.json.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/package-manager.d.ts — ' * Saves to <projectDir>/.claude/package-manager.json.' -> ' * Saves to <projectDir>/.cursor/package-manager.json.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/suggest-compact.js — regex 'claude-tool-count-' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/suggest-compact.js — regex 'claude-context-bucket-' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/stop-format-typecheck.js — "  const roots = [path.join(cwd, '.claude', 'plugins')];" -> "  const roots = [path.join(cwd, '.cursor', 'plugins')];"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/stop-format-typecheck.js — "  if (homeDir) roots.push(path.join(homeDir, '.claude', 'plugins'));" -> "  if (homeDir) roots.push(path.join(homeDir, '.cursor', 'plugins'));"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/skill-run-tracker.js — ' * ~/.claude/state/skill-runs.jsonl was never written and' -> ' * ~/.cursor/ecc/state/skill-runs.jsonl was never written and'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/session-end.js — '  const envTranscriptPath = process.env.CLAUDE_TRANSCRIPT_PATH;' -> '  const envTranscriptPath = process.env.ECC_TRANSCRIPT_PATH;'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/session-end.js — ' * Without this, a parent session and any `claude -p ...` subprocess spawned by' -> ' * Without this, a parent session and any CLI subprocess spawned by'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/session-activity-tracker.js — ' * ~/.claude/metrics/tool-usage.jsonl for ECC2 metric sync.' -> ' * ~/.cursor/ecc/metrics/tool-usage.jsonl for ECC2 metric sync.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/session-activity-tracker.js — '  // Cursor does not set CLAUDE_HOOK_EVENT_NAME for hook subprocesses.' -> '  // Cursor does not set ECC_HOOK_EVENT_NAME for hook subprocesses.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/session-activity-tracker.js — "    input?.hook_event_name || env.CLAUDE_HOOK_EVENT_NAME || ''" -> "    input?.hook_event_name || env.ECC_HOOK_EVENT_NAME || ''"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/pre-compact.js — ' * written here was removed in fix #16: it needed `claude -p` and has no' -> ' * written here was removed in fix #16: it needed a CLI subprocess and has no'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/post-bash-command-log.js — '// `~/.claude-work` resolves to one place rather than two.' -> '// `~/some-dir` resolves to one place rather than two.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/plan-canvas-sessions.js — '// `~/.claude-work` resolves to one place rather than two.' -> '// `~/some-dir` resolves to one place rather than two.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/plan-canvas-pending.js — '// `~/.claude-work` resolves to one place rather than two.' -> '// `~/some-dir` resolves to one place rather than two.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/mcp-health-check.js — "  const eventName = process.env.CLAUDE_HOOK_EVENT_NAME || 'PreToolUse';" -> "  const eventName = process.env.ECC_HOOK_EVENT_NAME || 'PreToolUse';"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/insaits-security-monitor.py — '            session_name="claude-code-hook",' -> '            session_name="ecc-hook",'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/insaits-security-monitor.py — '            sender_id="claude-code",' -> '            sender_id="cursor",'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/governance-capture.js — "  const hookPhase = process.env.CLAUDE_HOOK_EVENT_NAME || 'unknown';" -> "  const hookPhase = process.env.ECC_HOOK_EVENT_NAME || 'unknown';"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/hooks/before-shell-execution.js — regex '\\bclaudeRaw\\b' (3x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/doc-file-warning.js — 'const STRUCTURED_DIRS = /(^|\\/)(docs|\\.claude|\\.github|commands|skills|benchmark' -> 'const STRUCTURED_DIRS = /(^|\\/)(docs|\\.cursor|\\.github|commands|skills|benchmark'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/skill-create.md — 'a global skill uses `~/.cursor/skills/` or `~/.claude/skills/`.' -> 'a global skill uses `~/.cursor/skills/`.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/save-session.md — 'mkdir -p ~/.claude/session-data' -> 'mkdir -p ~/.cursor/ecc/session-data'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/resume-session.md — 'SESSION LOADED: /Users/you/.claude/session-data/2024-01-15-abc123de-session.tmp' -> 'SESSION LOADED: /Users/you/.cursor/ecc/session-data/2024-01-15-abc123de-session.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/promote.md — '   Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `' -> '   Legacy homunculus data is not read (the migration script was removed in fix #'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/projects.md — '   Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `' -> '   Legacy homunculus data is not read (the migration script was removed in fix #'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/instinct-status.md — '   Legacy data under `~/.claude/homunculus/` is not read; migrate it once with `' -> '   Legacy homunculus data is not read (the migration script was removed in fix #'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/instinct-import.md — '   - Legacy data under `~/.claude/homunculus/` is not read; migrate it once with' -> '   - Legacy homunculus data is not read (the migration script was removed in fix'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/instinct-status.md — 'while a legacy `~/.claude/skills/continuous-learning-v2/` directory still' -> 'while a legacy `~/.cursor/skills/continuous-learning-v2/` directory still'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/project-init.md — '/project-init --target claude' -> '/project-init --target cursor'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/project-init.md — 'If `AGENTS.md`, `.ecc/settings.local.json`, `.cursor/`, `.codex/`, `.gemini/`, `' -> 'If `AGENTS.md`, `.ecc/settings.local.json`, or `.cursor/` already exists, inspec'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/project-init.md — '1. Identify the target harness. Default to `claude` unless the user asks for `cu' -> '1. Identify the target harness. Default to `cursor`.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/astra-review.md — '(The Astra/Codex backend was removed in fix #16; review now runs via Grok review' -> '(The Astra review backend was removed in fix #16; review now runs via Grok revie'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/astra-review.md — '> The Astra/Codex backend was removed in fix #16.' -> '> The Astra review backend was removed in fix #16.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/polish-pass/reference/impeccable-detector-rules.json — '    "id": "codex-grid-background",' -> '    "id": "grid-background",'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/orchestrate/SKILL.md — 'they invoked external Codex/Gemini CLIs.' -> 'they invoked external model CLIs.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/ai-regression-testing/SKILL.md — '- AI agent (Cursor, Cursor, Codex) has modified API routes or backend logic' -> '- AI agent (Cursor) has modified API routes or backend logic'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/frontend-design-direction/SKILL.md — 'Note: ECC intentionally does not rebundle the canonical Anthropic\n`frontend-desi' -> 'Note: ECC intentionally does not rebundle the canonical upstream\n`frontend-desig'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/documentation-lookup/SKILL.md — 'Applies across harnesses that have the Context7 MCP configured (e.g. Cursor, Cur' -> 'Applies in Cursor when the Context7 MCP is configured.'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/continuous-learning-v2/agents/observer-loop.sh — '  # `claude` CLI, which has no Cursor equivalent. Observations are' -> '  # a CLI subprocess, which has no Cursor equivalent. Observations are'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/lib/install/apply.js — '  const preparedClaudeSettings = preflightClaudeSettingsOperations(appliedPlan);' -> ''
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/context-budget/SKILL.md — '[`/context` and `/usage` commands (Cursor only; `/cost` is an alias)](https://co' -> '`/context` and `/usage` commands (Cursor only; `/cost` is an alias)'
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/scripts/hooks/hookify-runtime.js — "  const configured = String(env.CLAUDE_PROJECT_DIR || '').trim();" -> "  const configured = String(env.CURSOR_PROJECT_DIR || '').trim();"
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/resume-session.md — regex '~/\\.claude/session-data/' (6x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/resume-session.md — regex '~/\\.claude/sessions/' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/save-session.md — regex '~/\\.claude/session-data/' (3x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/sessions.md — regex '~/\\.claude/session-data/' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/commands/sessions.md — regex '~/\\.claude/sessions/' (2x)
- /home/hatch/workspace/hackathon-plugin/hackathon-ecc/skills/rules-distill/scripts/scan-skills.sh — '#   RULES_DISTILL_GLOBAL_DIR   Override ~/.ecc/skills (for testing only;' -> '#   RULES_DISTILL_GLOBAL_DIR   Override ~/.cursor/skills (for testing only;'

## D13 follow-up — session-guardian.sh deleted (builds 8–9)

- **`skills/continuous-learning-v2/agents/session-guardian.sh` — DELETED in the
  follow-up (builds 8–9), resolving the flagged item below.** Zero-caller
  evidence (verified on the live build-7 tree before deleting):
  - No mention in staged sources (`new-skills/`, `round2-skills/`,
    `rewritten-skills/` — grep rc=1) or in `build.sh` (grep rc=1); it arrives
    only via the ECC base install.
  - In the built tree its only mention was the comment in
    `agents/observer-loop.sh:24` plus its own self-references (header + echo
    strings). Its only call site, `observer-loop.sh:220-222` (the gate
    `if ! bash "${SCRIPT_DIR}/session-guardian.sh"`), was removed under D13
    and is absent from the built tree.
  - `observer-loop.sh` was NOT deleted: it is live — called by
    `agents/start-observer.sh:27`
    (`OBSERVER_LOOP_SCRIPT="${SCRIPT_DIR}/observer-loop.sh"`), which is called
    by `hooks/observe.sh:415`; `observe.sh` is additionally referenced by
    `scripts/hooks/observe-runner.js:9`. `hooks/hooks.json` registers no
    `observe.sh` entry (Cursor events only; observation is Stop-hook/manual
    `/learn`), but the in-tree call chain is intact and D13 deliberately kept
    the loop with analysis stubbed — so per the zero-callers-only rule the
    loop stays. Its dangling `:24` comment was reworded instead (see below).
- **Mechanism:** added the file to `fix16/fix16.py` `DELETE_FILES`
  (`fix16.py:156-158`, next to the D13 `migrate-homunculus.sh` entry);
  `do_deletes()` runs first in `main()` (`fix16.py:4036`), so no `rm` in
  `build.sh`. The two targeted edits that touched the file were removed so the
  engine never edits a deleted file (the build-3 failure mode; both were
  `if exists(f):`-guarded, so they would only have skipped silently):
  - `edit_prose_round2` header-comment reword (`fix16.py:2939-2942`, was the
    "before spawning any Cursor session" → "agent session" sub).
  - `edit_misc_targeted` OBSERVER_LAST_RUN_LOG re-point
    (`fix16.py:4014-4017`, was the `~/.claude/observer-last-run.log` →
    `~/.cursor/ecc/observer-last-run.log` comment + `LOG_PATH` subs).
  - New edit in `edit_observer_loop()` (`fix16.py:480-485`): `observer-loop.sh`
    lines 24–25 reworded from "so sibling scripts (session-guardian.sh) and
    relative helpers …" to "so relative helpers (../scripts/instinct-cli.py)
    resolve correctly whether". This does not collide with build.sh's
    audit2/audit9 patches on `observer-loop.sh` (build.sh:12751, 15688-15693),
    which anchor on other regions and run before fix16.
- **Results:** builds 8 and 9 both exit 0; fix16 ERRORS 0, NOTES 11,
  CHANGES 624 (626 − 3 removed edits + 1 new comment edit), REMOVALS 88
  (was 87). Counts unchanged: skills 166, agents 72, rules 123, commands 87,
  hooks 15. Manifests `manifest-build8.txt` / `manifest-build9.txt`: 2,669
  files each, sha256
  `796a48d1734329193288ed6814ce10c4bab7f589970423d8968850cabcf0c977`,
  diff 0. Post-build greps on the build-9 tree: `session-guardian` 0 hits;
  `observer-loop` only `start-observer.sh:27`; banned terms
  (composer-2.5, claude, codex, anthropic, opus, case-insensitive) all 0,
  TOTAL BANNED-TERM HITS 0; Grok pins unchanged by line count —
  `grok-4.7-high` 45 lines, `cursor-grok-4.6-high-fast` 98 lines (occurrence
  counts 52 / 99 — some lines carry the pin twice; unchanged from build 7,
  confirmed by the build 7 → 8 manifest diff touching only the two files
  above). `build.sh` unchanged: 23,221 lines, md5
  `5d6ec4674214d89af8dd84856c5db987`.

## NOT done / flagged for the coordinator

- **`~/.ecc/memory/` in `skills/unified-memory/SKILL.md:48`** — verified UPSTREAM
  (identical at `/tmp/ecc-repo-clean/skills/unified-memory/SKILL.md:48`); ECC's own
  user-scope memory vault. Not a fix16 invention; left as-is.
- **`scripts/hooks/post-bash-command-log.js:20` `fileName: 'cost-tracker.log'`** —
  left deliberately (its own log file, no banned term).
- **`skills/pitch-deck-video/SKILL.md:554`** mentions the cost-tracker design as
  not shipped — left, recorded.
- **Deliberate build.sh OLD-side retentions** (see D18): the astra-review
  `qc_patch` OLD side `model: opus` and `gpt-6-astra` OLD sides must match upstream
  verbatim; the built-tree output is scrubbed by the fix16 pass instead.
- MANIFEST.md is NOT written here (the coordinator assembles it).

## Fix-up round (audit #54 / dry-run #26 / sweep #16 — builds 10–11)

The first checkers found 1 blocking + 10 minor findings (audit #54: B1 +
M1–M5; dry-run #26: M1; sweep #16: F1–F5 — F1/B1/M1-dryrun are the same
issue). All fixed in one pass. `fix16/fix16.py` is now 4,163 lines, md5
`ea4f785a22c8ff13664f3834e8fc5831` (was 4,078 lines, md5
`be805a19862360c32a484ae1c15f4a45`).

### Fix list (file:line, old → new)

**1. B1/F1 (BLOCKING) — `scripts/lib/agent-compress.js:118`.**
`model: frontmatter.model || 'sonnet',` →
`model: frontmatter.model || 'cursor-grok-4.6-high-fast',`. Verified
upstream-identical at `/tmp/ecc-repo-clean/scripts/lib/agent-compress.js:118`
and `build.sh` contains 0 mentions of "agent-compress", so the file is
re-staged from upstream ECC every build — the fix is a new `fix16.py` rule
(`edit_prose_round2`, fix-up block), not a staged-source edit. The
self-check term list in `self_check()` now also greps `sonnet` and `haiku`
(`banned = [composer-2.5, claude, codex, anthropic, sonnet, haiku]`), so
this class of gap cannot hide again; the direct pre-check run of the new
engine proved it: `BANNED sonnet: 0`, `BANNED haiku: 0`.

**2. M3/F3 — Haiku comments.**
`skills/continuous-learning-v2/agents/start-observer.sh:5`:
"Uses Haiku model for cost efficiency." →
"Uses the fast-tier model for cost efficiency."
`skills/continuous-learning-v2/hooks/observe.sh:149`:
"ECC observing its own Haiku observer sessions (self-loop)" →
"ECC observing its own observer sessions (self-loop)".
Both files are upstream-copied (verified identical in
`/tmp/ecc-repo-clean`; no staged override in `new-skills/` or
`round2-skills/`), so both rewordings are new `fix16.py` rules alongside
the agent-compress rule.

**3. M1/F4 — shipped README counts.**
`build.sh` README heredoc: `:18337` "169 skills, 72 agents, 123 rules, and
96 commands in total." → "166 skills, 72 agents, 123 rules, and 87 commands
in total."; `:18360` "169 skills widen the routing surface" → "166 skills
widen the routing surface"; `:18362` "56 MB and 169 skills" → "56 MB and
166 skills"; `:18364` "169 skills, 72 agents, 96 commands" → "166 skills,
72 agents, 87 commands". No staged README copy exists (repo-root
`README.md` states no counts). Built `README.md:13, :36, :38, :40` now read
166/87. Additional same-class fix, not in the finding list:
`build.sh:18366` / built `README.md:42` "## Commands (highlights — 3 of 96)"
→ "3 of 87".

**4. M2/F4 — `LIVE_SMOKE_TEST.md:17`.**
"(counts should read 168 skills, 72 agents, 123 rules, 96 commands)" →
"(counts should read 166 skills, 72 agents, 123 rules, 87 commands)".
Staged doc, edited directly.

**5. M4 — gates.md (COORDINATOR DECISION: keep the scrubbed text).**
Anish's correction (zero Claude/Codex mentions in the built tree) overrides
the fix #15 "gates.md untouched" rule. `fix16.py` had scrubbed the built
copy only; the STAGED source now matches it:
`new-skills/design-taste-frontend/references/hallmark/references/gates.md:243`
"(a subagent in Claude Code)" → "(a subagent in Cursor)" and
"(in Claude Code, `run_in_background: false`)" →
"(in Cursor, `run_in_background: false`)". Staged vs built gates.md diff is
now 0. `fix15/verify15.py` updated (see below) and re-run: 43/43.

**6. M5 — JS claim corrected.**
CHANGES.md "Post-build self-check" claimed "18/18" including
`scripts/lib/hooks/hookify-runtime.js`, which does not exist (no
`scripts/lib/hooks/` directory in the built tree, in `build.sh`, or in
upstream `/tmp/ecc-repo-clean`; the real file is
`scripts/hooks/hookify-runtime.js`). Corrected to **17/17** with the right
path; `node --check` re-run on all 17 real files: 17 pass.

**7. F2 — staged sources scrubbed (59 lines, sweep #16 Appendix B).**
Coordinator-verified totals now 0 in `new-skills/` + `round2-skills/` for
`claude` / `codex` / `anthropic` (and for `sonnet` / `haiku`):
- Icon brand catalog (33 lines): the 4 brand entries removed from
  `design-taste-frontend/assets/icons/index.json` (ids anthropic, claude,
  claude-code, codex + their `logos:*-icon` viewBox keys; id count 931 → 927,
  matching the built copy) and from `demo/icons-credits.json` (entries for
  anthropic.svg, claude-code.svg, claude.svg, codex.svg); the 4 chips removed
  from `demo.html:48` (AI count 53 → 49); the 4 SVG files
  (`demo/anthropic.svg`, `demo/claude.svg`, `demo/claude-code.svg`,
  `demo/codex.svg`) deleted — verified referenced nowhere else (only
  `demo.html:48` and `icons-credits.json` mentioned them). Gemini/OpenAI/other
  brand icons stay. After scrubbing, staged index.json / icons-credits.json /
  demo.html are byte-identical to their built counterparts (diff 0).
- Provenance prose (4 lines): `design-taste-frontend/SKILL.md:415` "written
  for Claude Code" → "written for Cursor" (and the `Stop` hook likewise);
  `:419` "only the Claude Code hook removed" → "only the Cursor hook
  removed"; `integration/SKILL.md:128` "(claude-code-skills)" →
  "(whawkinsiv's skills repo)"; `feature-expansion/SKILL.md:205`
  "claude-handoff" → "handoff".
- Multi-host hook docs + gate script (16 lines): staged
  `references/gate.md` rewritten to the built form (Cursor section, env
  re-points, `--hook cursor`; Antigravity section removed in the builds
  13–14 follow-up, see below; Codex section removed — staged gate.md now
  byte-identical to built gate.md, diff 0);
  staged `gates.md:243` (see #5 above); staged `scripts/gate.mjs` set to the
  built scrubbed form (`--hook cursor`, `const MODES = { cursor: 'block' };`,
  error `gate: --hook takes cursor`; staged gate.mjs now byte-identical to
  built, diff 0). Callers checked: the only `--hook <mode>` invocation in
  the tree is the gate.md doc example `:161` `--hook cursor` (valid).
  Follow-up (builds 13–14): the stale Antigravity section flagged here is
  now removed, not left as-is. Staged `references/gate.md:167–177` — the
  whole "**Antigravity**, `.agents/hooks.json` ..." section, including the
  `:173` `--hook antigravity` JSON example — deleted (11 lines); staged
  `scripts/gate.mjs:72` — the header comment
  "`{\"decision\":\"continue\",\"reason\":...} for antigravity;`" deleted,
  leaving "`Hook mode blocks ... for cursor; it allows by printing
  nothing.`" Why: the scrubbed gate.mjs has only
  `MODES = { cursor: 'block' }`, so `--hook antigravity` prints an error
  and exits 0 (fail-open); the section told the user to wire up a mode the
  script rejects. Full staged-skill grep for `antigravity` (case-insensitive)
  found only those two files, and no other stale host-mode reference
  (`claude` / `codex` / `--hook <mode>`) remains in the skill. `fix16.py`
  untouched — its gate rules are tolerant and logged the same
  38 NOTEs / 600 CHANGEs / 88 REMOVALs on builds 13–14 (no-op on these
  files). No files added or deleted, so the removal count stays 88 and
  the file count stays 2,665. Staged gate.md / gate.mjs are again
  byte-identical to their built copies (diff 0 each).
- Removal-note / tool names (6 lines): `orchestrate/SKILL.md:32` "external
  Codex/Gemini CLIs" → "external model CLIs";
  `round2-skills/mobile-ship/references/launch-marketing.md:7` "Claude
  Motion" → "Cursor Motion"; `round2-skills/polish-pass/reference/capture.md:33`
  "Claude in Chrome" → "Cursor in Chrome";
  `round2-skills/polish-pass/reference/impeccable-critique.md:38` dropped
  ", the Codex permission question included";
  `round2-skills/polish-pass/reference/impeccable-detector-rules.json:563`
  `"codex-grid-background"` → `"grid-background"`;
  `design-taste-frontend/assets/layout/heroes.json:636` dropped "Anthropic, "
  from the `from` attribution.
- `fix16.py` kept as a safety net, and made tolerant where the staged scrub
  removed its old anchors: new helpers `sub_if_new_present`,
  `resub_if_present`, `remove_array_entry_if_present` (skip with a NOTE when
  the new text / absence is already in place; still ERROR if neither old nor
  new is found), applied to the gate.mjs (2 subs), gate.md (1 sub + the
  Codex-span deletion, now a NOTE-skip, + the "As a hook" paragraph sub — the
  last one was caught by build 10, which exited 1 on that single anchor
  before it was made tolerant; no other rule failed), demo.html (resub +
  AI-count sub), index.json (4 removals + 4 viewBox resubs), icons-credits.json
  (4 removals), heroes.json, detector-rules.json, orchestrate, critique,
  integration, feature-expansion. A direct pre-check run of the new engine
  against the build-9 tree proved the tolerance for the rules that were
  tolerant at the time (24 "already applied at staged source, skipped"
  NOTEs, zero new ERRORs from them; the run's 544 ERRORs were the
  pre-existing non-idempotent re-run artifacts — deletes of already-deleted
  files and already-applied strict subs — because fix16.py expects a fresh
  tree). The one rule the pre-check could not prove — the gate.md "As a
  hook" paragraph sub, which still fired normally on the build-9 tree —
  failed build 10 with a single ERROR and was then made tolerant too;
  builds 11–12 are the clean evidence (25 tolerant skips: 24 "already
  applied" NOTEs + the Codex-span skip NOTE).
- No `build.sh` patch breaks: none of the 59 old strings occurs in
  `build.sh` (grep 0 for each), so no audit_patch OLD side depends on them.
  Remaining staged-vs-built diffs for the touched files are only the
  build.sh-patch regions (`design-taste-frontend/SKILL.md:9-13` description,
  `integration/SKILL.md:3`, `feature-expansion/SKILL.md:3,32-33`) — no banned
  term in any of them.

**8. F5 — build.sh (c)-class inventory adjudicated (sweep #16 App. A, 832 rows).**
- (c2) heredoc `build.sh:18296`: the schema description "which describes
  the Claude Code hooks format" → "which describes the legacy hooks
  format", fixed in `build.sh` itself. (The built copy's "Cursor hooks
  format" came from the generic pass rewriting "Claude Code"; the legacy
  schema is the one being contrasted, so "legacy hooks format" is the
  coherent neutral sentence, not a doubled "Cursor hooks format".)
- (c3) paths `build.sh:265` (`cp -r "$UIPRO_DIR/.claude/skills/ui-ux-pro-max"`)
  and `:298` (`cp -r "$SKILL_SRC/flecto-shade/.claude/skills/hackathon-pitch"`):
  verified to exist exactly as written in the pinned checkouts
  (`/tmp/uipro/.claude/skills/ui-ux-pro-max`,
  `/tmp/skill-add/flecto-shade/.claude/skills/hackathon-pitch`) — the
  upstream repos store skills under `.claude/skills/`, so the paths are
  required for the build. Recorded as acknowledged build-time exceptions:
  they do not ship (only the copied content ships, scrubbed downstream).
  NOT renamed.
- (c1) NEW-side patch text (368 rows): verified — no row is a live pin.
  The only `model:`-valued rows are OLD-side match strings or superseded by
  a later re-pin patch: `build.sh:7788/7795` `model: opus` is the (a) OLD
  side (astra-review section; NEW side scrubbed, built tree 0 opus);
  `build.sh:15141-15142` `model: sonnet` NEW side of an audit7 patch for
  `instinct-cli.py` is superseded by the audit8 D3 patch at `:15399`
  (`model: sonnet` → `model: cursor-grok-4.6-high-fast`; built
  `instinct-cli.py` carries the fast pin); `build.sh:16288` `model: sonnet`
  is the Fixer B OLD side for `commands/evolve.md` (built `:172` →
  `model: cursor-grok-4.6-high-fast`). The 2 `opus` (c1) rows are prose, not
  pins: `:8377` "Run two independent reviewers (Claude Opus + an external
  model)" and `:6925` "400k Opus 4.x" (context-window example); both are
  rewritten by the generic pass's prose Opus rule and the built tree has 0
  `opus` hits. The remaining (c1) rows are ordinary prose/`~/.claude` path
  text that the final `fix16.py` scrub removes from shipping targets (or
  whose target file it deletes); the shipped tree is verified 0-hit for
  every banned term after builds 10–11.
- Extended exception definition: the fix #16 exception now covers (a)
  OLD-side match strings + their (b) comments (461 rows), (c1) NEW-side
  patch text that lands only transiently in STEP 3 and is deterministically
  removed/rewritten by the final `fix16.py` scrub or deleted with its target
  file (368 rows), (c2) the one heredoc file write (1 row, fixed in
  `build.sh:18296` itself in this round), and (c3) the two build-time source
  paths (2 rows, acknowledged exceptions, do not ship). What is NOT
  excepted: any banned term or non-Grok pin in the shipped tree — the
  post-build self-check (now also grepping `sonnet`/`haiku`) enforces 0 hits
  there, and the (c1) list remains the watchlist for a future generic-pass
  miss.

**9. Composer borderline — `scripts/hooks/cursor-session-env.js:3`.**
"Cursor sessionStart hook — inject ECC_AGENT_DATA_HOME for the composer
session." Read in context (file header cites `https://cursor.com/docs/hooks`;
body is session-scoped env plumbing): "composer session" is the Cursor
session the hook runs in, not Cursor's Composer UI feature (no feature name,
no agent-mode reference, not a pin). KEPT, recorded here.

**10. Gemini subset — 31 `gemini` lines in the built tree.**
Re-checked line by line; none instructs invoking a non-Grok CLI in a
workflow. `skills/angular-developer/references/mcp.md:3,51,53` documents the
Angular CLI MCP server (Gemini CLI listed as one host that can consume it;
the "Create `.gemini/settings.json`" section registers the *Angular* CLI
via `npx`, it does not dispatch plugin work to a Gemini CLI);
`skills/integration/SKILL.md:17,65` are a sponsor-track trigger ("using the
Gemini API") and the `GEMINI_API_KEY` env name; icon data
(`assets/icons/demo.html:48`, `demo/icons-credits.json:1601-1610`,
`assets/icons/index.json:205-207,7580`); prize/API-key names
(`skills/track-picker/SKILL.md:23,76`); badge
(`skills/readme-writer/references/badges.md:34`). Recorded as non-pin
mentions; nothing removed. (The `orchestrate/SKILL.md:32` removal-note
"Codex/Gemini CLIs" line is item 7 above, not part of this subset.)

### verify15.py update (fix #15 rules, post-fix16 state)

The 4 checks that failed 39/43 in audit #54 are updated to the post-fix16
values and the tool re-run (43/43 — see build results below):
- "counts 169/72/123/96/15 unchanged" → "counts 166/72/123/87/15
  (post-fix16)" (fix #16 deleted 3 skills, 9 commands).
- "gates.md staged == staged source (verbatim upstream, untouched)" →
  "gates.md staged == built (scrubbed Cursor wording, one documented
  hunk)": equality PLUS "(a subagent in Cursor)" and
  "(in Cursor, `run_in_background: false`)" present and "Claude Code"
  absent. The fix #15 "untouched" invariant is superseded by the
  coordinator decision in item 5 above.
- "build.sh diff vs before-fix15 is exactly one insert" → "build.sh is
  23,221 lines, md5 532ab5458c22d6341444fdc92cf67ffd (post-fix16 fix-up)".
  The md5 changed from the fix #15 baseline
  `1f1a232572b9e12332733688838e1233` and from the fix #16 state
  `5d6ec4674214d89af8dd84856c5db987` by this round's own `build.sh` edits
  (README heredoc counts + the :18296 schema sentence); line count is
  unchanged at 23,221 (all edits are same-line substitutions).
- "the one insert is the 57-line fix15 block" → "the 57-line fix15 block is
  still present intact in build.sh (fix15 header .. PYEOF)": locates the
  block by its `# --- fix15:` header and verifies the 57-line shape
  (header, PYEOF second-to-last, trailing blank, marker present) instead
  of diffing against before-fix15. "build.sh contains the fix15 block
  marker" is unchanged. Module docstring items 6/7/8 updated to match.

### Build results (fix-up round)

- Build 10: exit 1 — fix16 ERRORS 1 (the gate.md "As a hook" paragraph sub;
  see the Build results table). No STEP 5, no manifest. Self-check already
  all zero.
- Build 11: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 600, REMOVALS 88.
  STEP 5: skills 166, agents 72, rules 123, commands 87, hooks 15.
  Manifest `manifest-build11.txt`, 2,665 files, sha256
  `7bc56657b983c386b9a085f8562a9dfdca815c2a8f42f136e164d3a00f8d4601`.
- Build 12: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 600, REMOVALS 88
  (identical footer to build 11). Manifest `manifest-build12.txt` — diff vs
  build 11: **0 (identical)**, same sha256, 2,665 files.
- Build 13: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 600, REMOVALS 88
  (identical footer to builds 11–12; fix16.py a no-op on the gate files).
  Manifest `manifest-build13.txt`, 2,665 files, sha256
  `f1ffa31be9b1a721b068f2dc194de7fd51b6779d6f2f88c2d1123a2166ecb36a`.
- Build 14: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 600, REMOVALS 88
  (identical footer to build 13). Manifest `manifest-build14.txt` — diff vs
  build 13: **0 (identical)**, same sha256, 2,665 files.
- Manifest build 12 → build 13 touches exactly 2 entries: the two gate
  files (`skills/design-taste-frontend/references/gate.md`, Antigravity
  section removed; `skills/design-taste-frontend/scripts/gate.mjs`, header
  comment reworded). Every other file is byte-identical — the staged
  Antigravity removal produces built copies identical to the staged
  sources, by design. REMOVALS stays 88 and the file count stays 2,665:
  removing doc text removes no files.
- Manifest build 9 → build 11 touches exactly 11 lines: `README.md` (counts
  fix), `schemas/cursor-hooks.schema.json` (legacy-hooks-format sentence),
  `scripts/lib/agent-compress.js` (B1), `start-observer.sh` + `observe.sh`
  (M3), and the 4 deleted brand-icon SVGs. Every other file is byte-identical
  — the staged F2 scrub produces built copies identical to what fix16.py's
  tree pass already produced, by design.
- `python3 fix15/verify15.py`: **43/43 pass** (see the verify15.py update
  above), exit 0, re-run on the build-14 tree (still 43/43 after the
  Antigravity gate-doc removal).
- Independent post-build greps on the build-14 tree (excluding
  `node_modules/`): `composer-2.5` / `claude` / `codex` / `anthropic` /
  `opus` / `sonnet` / `haiku` all 0 (case-insensitive). `antigravity`: 0 in
  the staged design-taste-frontend skill and 0 in the built gate files; the
  built tree still carries 14 lines in 6 files, all legitimate and
  pre-existing (not gate hook modes): `skills/angular-developer/references/
  mcp.md:36,38` (Antigravity IDE MCP config docs), `scripts/lib/install-
  lifecycle.js:854–856,1688,1696` (legacy `.agent` install-state warnings),
  `scripts/lib/install/apply.js:804–805,866` (fix #16's own removal comment
  + the now-empty `antigravityMigrationWarnings` carrier),
  `scripts/lib/install/content-transform.js:4` (historical comment),
  `scripts/lib/install/stale-operations-reconciliation.js:46,52`
  (legacy-compat plan handling), `scripts/auto-update.js:188`
  (migrate-your-legacy-install user message). Staged sources
  (`new-skills/` + `round2-skills/` + `~/workspace/cursor-skills/less-flat-ui/`):
  `claude` / `codex` / `anthropic` / `sonnet` / `haiku` all 0. Grok pins:
  `grok-4.7-high` 45 lines / 52 occurrences (unchanged),
  `cursor-grok-4.6-high-fast` 99 lines / 100 occurrences (was 98/99; +1 is
  `agent-compress.js:118`, the B1 fix). `gemini`: 17 lines in the built tree,
  all verified non-pins / non-routing (see item 10 above). Counts re-verified
  by listing: 166/72/123/87/15.
- Fix-up change count: CHANGES 624 (build 9) → 600 (builds 11–12): the 24
  tolerant rules now log "already applied at staged source, skipped" NOTEs
  instead of CHANGE entries, and 3 new B1/M3 rules were added. NOTES 11 → 38
  (24 "already applied" + the gate.md Codex-span skip + 13 pre-existing
  "pattern not found (verify manually)" / header notes). REMOVALS unchanged
  at 88.

## Sweep #17 follow-up — M1/M2 version-suffix residue (builds 15–16)

Sweep #17 found 2 minor cosmetic residues, both in one file, both left by
`fix16.py`'s generic prose substitution when the source text carried a
version suffix the regex did not cover. Both are prose only — not pins, not
banned terms, no wrong model routed anywhere.

### Fix list (file:line, old → new)

**M1 — `skills/strategic-compact/SKILL.md:68`.**
Old (shipped, build 14): `(e.g. 400k Grok 4.7 High 4.x, or a new 1M-window
model family)` → new: `(e.g. 500k Grok 4.7 High, or a new 1M-window model
family)`. Source was `400k Opus 4.x` (audit NEW text, `build.sh:6925`); the
generic regex `Opus 4\.\d+` did not cover literal `4.x`, so the bare
`\bOpus\b` fallback replaced "Opus" and left " 4.x". The "400k" figure was
also wrong for Grok 4.7 High, whose verified window is 256k standard /
500k long context (Cursor Docs grok-4-7); 500k is the verified long-context
figure, no other number invented. Fixed by a new targeted `sub()` in
`edit_post_generic()` (sweep #17 block) whose old text is the
post-regex-fix form `(e.g. 400k Grok 4.7 High, or a new 1M-window model
family)` — the extended regex (below) already drops the " 4.x" in the
generic pass, so the sub only rewords the figure.

**M2 — `skills/strategic-compact/SKILL.md:102`.**
Old (shipped, build 14): `> Cursor **2.1.233 removed the todo/task tools by
default** on Grok 4.7 High, Grok 4.6 High Fast 5,` → new: `> Cursor
**2.1.233 removed the todo/task tools by default** on Grok 4.7 High, Grok
4.6 High Fast,`. The stray " 5" is left from "Sonnet 5" (the generic pass
replaced "Sonnet" but not its version number). Fixed by a targeted `sub()`
in the same sweep #17 block. Sentence stays coherent: the next line
continues `> current models and newer (...)`.

**Mechanism.** `strategic-compact` has NO staged copy in `new-skills/` or
`round2-skills/` — it is an upstream ECC skill copied by `build.sh`
(audit patches at `build.sh:1015`, `:6844`, `:13025`), so
`hackathon-ecc/` was NOT edited directly (the next build would wipe it).
Both fixes are `fix16.py` rules in `edit_post_generic()`, the same pattern
as the other targeted post-generic fixes.

**Regex extension — `fix16.py` `generic_pass()` (`:1254`).**
`r"\bOpus 4\.\d+(?:-class)?"` → `r"\bOpus 4\.(?:\d+|x)(?:-class)?"`.
Safe and specific: the pattern requires the literal `Opus`, so it cannot
match inside the Grok pin names — verified by simulation before the build:
`400k Opus 4.x` → `400k Grok 4.7 High`, `Opus 4.5-class` →
`Grok 4.7 High`, `Opus 4.7 and later` → `Grok 4.7 High and later`,
`Opus 4.x-class` → `Grok 4.7 High`; no match in `Grok 4.7 High`,
`grok-4.7-high`, `Grok 4.6 High Fast`, `cursor-grok-4.6-high-fast`,
`model: grok-4.7-high`, `500k Grok 4.7 High`, `Grok 4.7 High 4.x`. No
broad version-stripping rule was added: a naive rule stripping digits
after a Grok name would corrupt `Grok 4.7 High` itself.

### Build results (sweep #17)

- Build 15: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 602 (was 600; +2
  new subs), REMOVALS 88. STEP 5: skills 166, agents 72, rules 123,
  commands 87, hooks 15. Manifest `manifest-build15.txt`, 2,665 files,
  sha256 `616461b382ff0fc50fbb2cadb7b859ba4f29be3887f909c92e9b1252269a5674`.
- Build 16: exit 0 — fix16 ERRORS 0, NOTES 38, CHANGES 602, REMOVALS 88
  (identical footer to build 15). Manifest `manifest-build16.txt` — diff
  vs build 15: **0 (identical)**, same sha256, 2,665 files.
- Manifest build 14 → build 15 touches exactly **one** entry:
  `skills/strategic-compact/SKILL.md` (hash `586fe2c8…` → `5a7227b0…`).
  Every other file is byte-identical — the bound holds, so no audit /
  dry-run re-run is triggered by this change (the change is two prose
  lines in one skill file; counts, pins, and the banned-term self-check
  are all unchanged, verified below).
- `python3 fix15/verify15.py`: **43/43 pass**, exit 0, re-run on the
  build-16 tree.
- Independent post-build greps on the build-16 tree (excluding
  `node_modules/`), scope-wide incl. staged sources +
  `LIVE_SMOKE_TEST.md` + shipped `README.md` + `marketplace.json`:
  `Grok 4.7 High [0-9]` / `Grok 4.6 High Fast [0-9]` — **0 hits** (both
  residues gone, no others anywhere). `composer-2.5` / `claude` / `codex` /
  `anthropic` / `opus` / `sonnet` / `haiku` — **0 each** in the tree and
  **0 each** in staged sources. fix16 self-check: `TOTAL BANNED-TERM
  HITS: 0`, JS syntax 0, JSON 0, registry smoke rc=0. Counts re-verified
  by listing: 166/72/123/87/15. Grok pins unchanged: `grok-4.7-high` 45
  lines / 52 occurrences, `cursor-grok-4.6-high-fast` 99 lines / 100
  occurrences.
