# Audit #54 — fix #16 (hackathon-ecc) — report

- Build: `~/workspace/hackathon-plugin/build.sh`, 23,221 lines, md5 `5d6ec4674214d89af8dd84856c5db987` (verified by `wc -l` + `md5sum` before auditing; fix #15 baseline was 23,217 / `1f1a232572b9e12332733688838e1233`)
- Built tree: `~/workspace/hackathon-plugin/hackathon-ecc/`
- Built-tree manifests: `fix16/manifest-build8.txt` and `fix16/manifest-build9.txt` — sha256 both `796a48d1734329193288ed6814ce10c4bab7f589970423d8968850cabcf0c977`, diff = 0, 2,669 files each
- Counts verified by listing the built tree and by the STEP 5 lines in `fix16/build9.log` (`skills: 166`, `agents: 72`, `rules: 123`, `commands: 87`, `hooks: 15`): **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks** (`hooks/hooks.json` hooks array length 15)
- Fix round under test: #16 (`~/workspace/hackathon-plugin/fix16/CHANGES.md`, `INVENTORY.md` read first; `fix16/fix16-run-log.md` consulted for edit provenance)
- Method: every key claim re-verified independently from the built files — never from memory or the implementer's report. `python3 fix15/verify15.py` re-run (39/43 pass; the 4 failures are analysed in §6). Nothing in the plugin tree or `build.sh` was edited; no build was executed; no commit, bundle, GitHub, or Campus Eats artifact touch.
- Verdict: **NOT CLEAN — 1 BLOCKING, 5 MINOR**

## Verdict

**NOT CLEAN.** Fix #16's core scrub is real: all five banned terms are 0 tree-wide, all 72 agent pins are Grok, the alias-mapping dict is exactly as specified, the 4 opus agents are on `grok-4.7-high`, `session-guardian.sh` is gone with no dangling reference, the smoke test and both READMEs carry the new pins, and every fix #15 anchor and standing #13 invariant re-verified intact. But one live code line still pins a non-Grok model — `scripts/lib/agent-compress.js:118` defaults `model:` to `'sonnet'` — which is a literal violation of the fix's own "ALL model pins must be Grok, no exceptions" mandate, even though the file is currently dead code. Five minor items ride with it: stale skill/command counts in the built README and in the smoke test's own expectation line, two orphaned "Haiku" comments on a removed observer mechanism, `gates.md` no longer byte-identical to its staged upstream source (the fix15 "untouched" invariant, broken by the generic scrub pass), and an overstated "18/18" JS-syntax claim in CHANGES.md (one listed path does not exist).

## BLOCKING (1)

**B1 — Non-Grok model pin survives in code: `scripts/lib/agent-compress.js:118`.**
`model: frontmatter.model || 'sonnet',` — the fallback value of a `model:` field is the `sonnet` tier alias. This is exactly the §2 criterion ("`sonnet` as [an] ID in any `model:` field"). It is the ONLY surviving `sonnet`/`haiku`/`opus`-as-ID pin in the tree (all other `sonnet`/`haiku` hits are prose — see M3). Mitigating facts, verified: the file has zero callers anywhere in the tree (no `require`/`import`, no `build.sh` reference, no `package.json` reference), so the fallback never fires today; all 72 agent files carry Grok pins, so `frontmatter.model` is always set for real inputs. It is dead code carrying a live pin. Fix: re-point the default to `'cursor-grok-4.6-high-fast'` (or drop the default).

## MINOR (5)

**M1 — Stale counts in the built README: `hackathon-ecc/README.md:13, :36, :38, :40`.**
`:13` "169 skills, 72 agents, 123 rules, and 96 commands in total." — true counts are now 166 skills / 87 commands. The same stale numbers repeat in the comparison paragraphs: `:36` ("169 skills widen the routing surface"), `:38` ("56 MB and 169 skills against a minimal set"), `:40` ("169 skills, 72 agents, 96 commands"). Arithmetic confirmed: 169−3 skills (skill-comply, council-multi-model, config-gc deleted) = 166; 96−9 commands (santa-loop, 5× multi-*, loop-status, cost-report, skill-host-compat deleted) = 87. The repo-root `README.md` states no counts (clean).

**M2 — Stale counts in the smoke test's own expectation: `LIVE_SMOKE_TEST.md:17`.**
"counts should read 168 skills, 72 agents, 123 rules, 96 commands" — should read 166 skills, 87 commands. Note the 168 was already wrong at audit #53 time (verified counts then were 169); the line is now wrong on two numbers and will read as a failure when the live test is run.

**M3 — Orphaned "Haiku" model name in two comments on a removed mechanism.**
- `hackathon-ecc/skills/continuous-learning-v2/agents/start-observer.sh:5` — "Uses Haiku model for cost efficiency."
- `hackathon-ecc/skills/continuous-learning-v2/hooks/observe.sh:149` — "ECC observing its own Haiku observer sessions (self-loop)"
The observer's model spawn was removed under D13 and `ECC_OBSERVER_MODEL` has 0 references tree-wide, so both comments describe a mechanism that no longer exists. Prose only, no functional effect.

**M4 — `gates.md` is no longer byte-identical to its staged upstream source.**
Built `hackathon-ecc/skills/design-taste-frontend/references/hallmark/references/gates.md:243` differs from staged `new-skills/design-taste-frontend/references/hallmark/references/gates.md:243` in one hunk only (diff = 4 lines): "a subagent in Claude Code" → "a subagent in Cursor", and "(in Claude Code, `run_in_background: false`)" → "(in Cursor, `run_in_background: false`)". This breaks audit #53 §(f) ("gates.md untouched; staged verbatim from upstream") and fails `verify15.py`'s gates check. Provenance: no targeted edit in `fix16-run-log.md` — the change came from the fix16 generic scrub pass; the staged source still says "Claude Code". Needs a coordinator call: keep the scrubbed wording (scrub mandate wins, and the fix15 "untouched" invariant is superseded) or restore upstream-verbatim and exempt `gates.md`.

**M5 — CHANGES.md "18/18" JS-syntax claim overstates by one file.**
CHANGES.md ("Post-build self-check") lists 18 surgically edited `.js` files as "18/18 pass", including `scripts/lib/hooks/hookify-runtime.js`. That path does not exist: there is no `scripts/lib/hooks/` directory in the built tree, the fix16 run log touches only `scripts/hooks/hookify-runtime.js`, `build.sh` references only `scripts/hooks/hookify-runtime.js` (4 hits, all that path), and upstream `/tmp/ecc-repo-clean` has no `scripts/lib/hooks/hookify-runtime.js` either. The 17 real files all pass `node --check` (verified below, §9). Reporting error only — no tree defect.

## (1) Pins — all verified except B1

- Orchestrator: `skills/orchestrate/SKILL.md:14` "the session's main model, Grok 4.7 High (`grok-4.7-high`, selected in the model picker before the run — see the picker note in step 4)"; roster `:24` you/orchestrator `grok-4.7-high`, `:25` deep-reasoner `grok-4.7-high`, `:26` fast-worker `cursor-grok-4.6-high-fast`, `:27` scout `cursor-grok-4.6-high-fast (read-only)`, `:28` design-lead `grok-4.7-high` (unchanged).
- Implementer tier pin added at step 4, `skills/orchestrate/SKILL.md:57`: "Slice-builder implementers spawn on the implementation tier — model `grok-4.7-high` (slug form only). Purely mechanical, fully-specified sub-tasks inside a slice still dispatch to fast-worker (`cursor-grok-4.6-high-fast`)." The same line carries the strengthened picker instruction: "Select **Grok 4.7 High** in Cursor's model picker before the first build — the orchestrator itself runs as Grok 4.7 High (`grok-4.7-high`)".
- Fallback pins, `skills/orchestrate/SKILL.md:158`: "deep-reasoner tier `grok-4.7-high`, fast-worker tier `cursor-grok-4.6-high-fast`, scout tier `cursor-grok-4.6-high-fast`, design-lead tier `grok-4.7-high` (slug form only — never bracket syntax for either Grok pin; the `cursor-` prefix on the fast tier is part of the slug. Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin, so the pin is the slug alone)".
- Alias-mapping dict, `build.sh:157` (verbatim): `mapping = {"sonnet": "cursor-grok-4.6-high-fast", "opus": "grok-4.7-high", "haiku": "cursor-grok-4.6-high-fast"}`; comment at `:152–153` rewritten to the Grok mapping.
- Agents: `grep -rn "model:" hackathon-ecc/agents/` = 72 lines: 68× `model: cursor-grok-4.6-high-fast`, 4× `model: grok-4.7-high`. The 4 are `deep-reasoner`, `ecc-architect`, `ecc-healthcare-reviewer`, `ecc-spec-miner` (all `:4`). GAN agents all fast: `ecc-gan-planner` / `ecc-gan-generator` / `ecc-gan-evaluator` (`:4` each, `cursor-grok-4.6-high-fast`).
- `model-route.md`: haiku row → `` `cursor-grok-4.6-high-fast` `` (deterministic, low-risk mechanical), sonnet row → `` `grok-4.7-high` `` (default for implementation and refactors), opus row → `` `grok-4.7-high` `` (architecture, deep review).
- `evolve.md:172` (generated-example `debugger` agent): `model: cursor-grok-4.6-high-fast`.
- `astra-review.md`: `scripts/lib/astra-review/codex.js` delegate gone (only `commands/astra-review.md` matches `*astra-review*` in the tree); Step 2 = blind deep-reasoner on `grok-4.7-high` (`:24`, `:39`), fixes to fast-worker / deep-reasoner (`:32`). `build.sh:7810–7825` still embeds the old Astra text ("Astra applies the fixes instead") — verified as the qc_patch OLD side (match pattern), per D18 deliberate retention; built tree has 0 "Astra applies" hits.
- `dispatch-prompt.md:197` worked example: "Spawn a general subagent (model: cursor-grok-4.6-high-fast)".
- `agent-TEMPLATE.md:4` (`skills/orchestrate/references/agent-TEMPLATE.md`): "model: CHANGE-ME (REQUIRED — pin exactly one Grok model ID (e.g. cursor-grok-4.6-high-fast, grok-4.7-high); …)".
- Trio files rewritten: `agents/scout.md:4` `model: cursor-grok-4.6-high-fast` (comment: slug form only, never a bare alias); `agents/fast-worker.md:4` same pin; `agents/deep-reasoner.md:4` `model: grok-4.7-high` (comment: "strongest Grok tier, first-party to Cursor (no third-party billing)").
- `schemas/agent.schema.json:36`: `"enum": ["cursor-grok-4.6-high-fast", "grok-4.7-high"]`. `scripts/lib/agent-ir.js:28`: `VALID_MODELS = ['cursor-grok-4.6-high-fast', 'grok-4.7-high']`. `hooks/adapter.js:112` `transformToHookPayload`, `:200` `ECC_SESSION_ID`, `:248` export; 0 hits for `transformToClaude` / `CLAUDE_SESSION_ID` in the file.
- `gan-build.md`: `grok-4.7-high` ×2 occurrences, `claude-opus-5` ×0, `composer-2.5` ×0. `gan-design.md`: `grok-4.7-high` ×3, `claude-opus-5` ×0, `composer-2.5` ×0.
- `rules/common-performance.mdc:9,11,13,30`: fast tier `cursor-grok-4.6-high-fast` (scout + fast-worker rows), deep tier `grok-4.7-high`; `:30` "Do not use effort controls — Grok takes per-vendor `reasoning_effort`, which Cursor does not expose in a pin."

## (2) Banned terms / non-Grok pins — 0 except B1

Case-insensitive greps over the whole built tree (including `node_modules/`, 619 files — 0 hits there too):

| Term | Hits |
|---|---|
| `composer-2.5` | 0 |
| `claude` | 0 |
| `codex` | 0 |
| `anthropic` | 0 |
| `opus` | 0 |
| `grok-4.7[` (bracket syntax) | 0 |
| bare `grok-4.6-high-fast` (without the `cursor-` prefix) | 0 lines (`grep -rn "grok-4.6-high-fast" | grep -v "cursor-grok-4.6-high-fast"` = 0) |

Pin counts in the built tree: `grok-4.7-high` 45 lines / 52 occurrences; `cursor-grok-4.6-high-fast` 98 lines / 99 occurrences — CHANGES.md's "×45, ×98" are line counts, consistent.

Remaining `gemini` / `gpt-` / `sonnet` / `haiku` hits, each checked and NOT a model pin:
- `gemini` (17 lines): "Gemini CLI" MCP docs (`skills/angular-developer/references/mcp.md:3,51,53`), "Best Use of Gemini API" sponsor prize + `GEMINI_API_KEY` env instruction (`skills/integration/SKILL.md:17,65`), Gemini icon demo data (`skills/design-taste-frontend/assets/icons/demo.html:48`, `demo/icons-credits.json:1601–1610`, `assets/icons/index.json:205–207,7580`), "Best Use of Gemini API" / "Gemini API project number" (`skills/track-picker/SKILL.md:23,76`), Gemini badge (`skills/readme-writer/references/badges.md:34`). All are third-party tool docs, sponsor-prize names, or demo/icon data — none is a `model:` field, pin table, or example pin for the plugin's own execution.
- `gpt-` (3 lines): rule ID `gpt-thin-border-wide-shadow` (`skills/polish-pass/reference/impeccable-detector-rules.json:545`), example bad pitch copy "We used GPT-4" (`skills/hackathon-scope/SKILL.md:110`, `skills/hackathon-pitch/references/win-secrets.md:347`). Prose/examples only.
- `sonnet` / `haiku` (3 lines total): B1 (`agent-compress.js:118`, the one pin) + M3 (the two Haiku comments). No other occurrences.
- Other `model:` lines in code are pass-throughs or type descriptors, not pins: `hooks/adapter.js:130` `model: cursorInput.model`, `scripts/hooks/ecc-statusline.js:138` `model: data.model?.display_name`, `scripts/lib/eval-harness/envelope.js:47` `model: 'string'` (schema type), `scripts/lib/transcript-context.js:61` JSDoc `@returns {{ tokens: number, model: string }}`.

## (3) session-guardian.sh deletion — clean

- `find hackathon-ecc -name '*session-guardian*'` = 0 files; `grep -rn "session-guardian" hackathon-ecc/` = 0 hits.
- `observer-loop.sh` live: `skills/continuous-learning-v2/agents/observer-loop.sh` (199 lines), path set at `start-observer.sh:27` (`OBSERVER_LOOP_SCRIPT="${SCRIPT_DIR}/observer-loop.sh"`), invoked at `start-observer.sh:222` (`"$OBSERVER_LOOP_SCRIPT" >> "$LOG_FILE" 2>&1 &`), existence checked at `:200–201`.
- Its `:24–25` comment reworded per the run log: "Resolve this script's own directory so relative helpers / (../scripts/instinct-cli.py) resolve correctly…" (was "so sibling scripts (session-guardian.sh)…"). No dangling reference to the deleted file anywhere in the tree (0 `session-guardian` hits, 0 `guardian` hits in both observer files).

## (4) LIVE_SMOKE_TEST.md — clean except M2

- §14 at `:130`: "## 14. Grok pins hold — 4.7 High design, 4.6 High Fast task tier (fix programs #13, #16)". Extended to the 4.6 pin at `:134`: "Fast tier runs on Grok 4.6 High Fast: on a mechanical task, confirm the fast-worker / scout actually runs on Grok 4.6 High Fast (`cursor-grok-4.6-high-fast` — the `cursor-` prefix is part of the pin), not on another model." Picker selection at `:132` (Grok 4.7 High).
- Step 7 deep-reasoner pin at `:70`: "see if the agent that runs reports itself as `deep-reasoner` with model `grok-4.7-high`"; `:80` deep-reasoner → `grok-4.7-high`; `:81` fast-worker → `cursor-grok-4.6-high-fast`; `:78` slug-form pins example.
- Stale-model-name grep (`claude|codex|opus|sonnet|haiku|composer-2.5|anthropic|gemini|gpt-`, case-insensitive) = 0 hits in the doc.
- One defect lives here: M2 (`:17` stale counts).

## (5) README picker note — clean except M1

- Repo-root `README.md:17` and built `hackathon-ecc/README.md:68` (identical text): "Before the first build — Grok 4.7 High in the model picker: the plugin pins its design role to `grok-4.7-high`. … Task agents pin to Grok 4.6 High Fast (`cursor-grok-4.6-high-fast`); the orchestrator and the design/implementation roles pin to Grok 4.7 High (`grok-4.7-high`)."
- Stale-model-name grep over both READMEs (`claude|codex|opus|sonnet|haiku|composer-2.5|anthropic`) = 0 hits.
- One defect lives here: M1 (stale counts at built README `:13, :36, :38, :40`).

## (6) Fix #15 rules — intact (with M4 noted)

`python3 fix15/verify15.py` re-run against the built tree: **39/43 pass.** The 4 failures:
1. "counts 169/72/123/96/15 unchanged" — FAIL because counts are now 166/72/123/87/15. Expected: fix16's removals (3 skills, 9 commands). Not a defect.
2. "gates.md staged == staged source (verbatim upstream, untouched)" — FAIL. This is M4.
3. "build.sh diff vs before-fix15 is exactly one insert" — FAIL because fix16 changed `build.sh` beyond the fix15 insert. Expected.
4. "the one insert is the 57-line fix15 block" — same cause. The companion check "build.sh contains the fix15 block marker" PASSES — the fix15 insert is still present.

All other 39 checks pass, re-verified independently below:

- Canonical variety+theme-match block: byte-identical (sha256 prefix `f7e956a7a132`, same as audit #53) exactly ×1 in all 11 files: `skills/design-taste-frontend/SKILL.md:55`, `skills/ui-ux-pro-max/SKILL.md:16`, `skills/less-flat-ui/SKILL.md:16`, `skills/polish-pass/SKILL.md:45`, `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md:20`, `skills/make-interfaces-feel-better/SKILL.md:15`, `skills/motion-foundations/SKILL.md:46`, `skills/motion-patterns/SKILL.md:43`, `skills/motion-advanced/SKILL.md:45`, `skills/orchestrate/SKILL.md:92`, `skills/orch-build-mvp/SKILL.md:42`. (In orch-build-mvp the 692-char block text matches exactly; the paragraph has no blank line after it, so a naive paragraph extraction merges the following list item — verified by direct text comparison, not the paragraph hash.)
- R1: Taste `:244` + static check `:290`, orchestrate `:61`, orch-build-mvp `:51` — all present with "never a screen verdict" framing.
- R2: Taste asset table `:153` — software column "1-2 by default, pulsing; 0 only with a recorded reason in the section plan"; hardware "0-2, pulsing", product "0-1, still" unchanged. (No literal "fix #15 R2" tag ever existed — the anchor is the table text, which is intact.)
- R3: `skills/less-flat-ui/SKILL.md:14` — "at least TWO DISTINCT treatment kinds must be recorded per screen … (fix #15 R3 — baseline: 2 treatment applications, both Soft Shadow, one kind)".
- R4: Taste `:268` — dealt hero's loop implemented or waived.
- R5: Taste `:246` — each Range pattern's named lead element is its own element.
- C1: Taste `:246` + `skills/ui-ux-pro-max/SKILL.md:89` — dealt pairing is the ONLY permitted faces.
- C2: Taste `:246` — display faces self-hosted.
- C3: Taste `:290` + `skills/polish-pass/SKILL.md:22` — Type list verified, "candidate evidence, never a verdict".
- D1: Taste `:310`, orchestrate `:60`, polish-pass `:104`, orch-build-mvp `:51` — rule text present exactly once each; final-report lines at orchestrate `:66` and orch-build-mvp `:59`.
- Treatments still 23: headings `### 1.`–`### 23.` count 23; `### 23. Soft shadow` at `skills/less-flat-ui/SKILL.md:487`; 0 hits for "22 treatments" / "22 textured".

## (7) Standing invariants — all intact

- "More, not bolder": once in each engine — orchestrate `:94` ("Posture — more, not bolder."; line shifted from `:90` in audit #53 by fix16 edits, wording intact), orch-build-mvp `:40`.
- Browser-qa sole executor: 0 files outside `skills/browser-qa/` contain `DO NOT SHIP` or `SHIP WITH FIXES`; "browser-qa alone issues pass/fail verdicts on rendered screens" present in all four D1 files (Taste `:310`, orchestrate `:60`, polish-pass `:104`, mvp `:51`).
- Impeccable craft-floor bans absolute as static checks: kicker/eyebrow ban at `skills/polish-pass/reference/impeccable-craft-floor.md:36` ("A kicker or eyebrow above a heading. This one is a ban, not a default: no brief earns it back") and `skills/polish-pass/reference/craft-floor.md:131` ("Eyebrow/kicker labels … above every section heading" in the banned-patterns list). Gradient text is a sloplint FAIL under gates 2a/2b (`skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs:1186–1187`, same lines as audit #53).
- Hallmark floor intact; no violet introduced: the only `violet` occurrences in the changed files are bans — Taste `:230` ("never violet: deal again"), Taste `:404` (Never-list item "Violet or lavender in the page's own design…"), less-flat-ui `:104` ("Never copy a purple/violet gradient onto a landing page…").
- Anti-derivative rule: orchestrate `:96` ("No design based on a searched reference (anti-derivative rule)…"), orch-build-mvp `:40` ("never based on a searched external reference (orchestrate row-10 rule)").
- Snapshot-before-redesign: "BEFORE any redesign file is overwritten" ×1 in each engine (orchestrate, orch-build-mvp).
- Shared 2-round fresh-verdict budget: "fresh-verdict rounds used: 0/2" ×1 in each engine; "2 rounds total" ×2 in each.
- Grok slug-only pins, no bracket syntax: orchestrate `:158` states the rule; 0 `grok-4.7[` hits tree-wide; `reasoning_effort` (not `effort`) at orchestrate `:158` and `rules/common-performance.mdc:30`; 0 `effort=xhigh` in either engine file.
- `fix11/fix11-stage.py` NOT re-run: 0 hits for `fix11-stage` in `build.sh`. Critique.md fix-#12 edits intact: "warmer / more playful / more distinctive" at `impeccable-critique.md:224` in BOTH the staged source (`round2-skills/polish-pass/reference/impeccable-critique.md`) and the built copy; 0 "warmer/bolder" hits tree-wide. (Line cited `:222` in the fix13e audit is now `:224` — a +2 shift, content intact.) The only staged-vs-built diff in the critique file is `:38`, where fix16 removed ", the Codex permission question included" — a scrub edit, not a clobber of fix-#12 content.
- Dangling references: `preflightClaudeSettingsOperations` / `planClaudeHooksOperations` / `findPreviousManagedHooks` / `validateRecordedManagedHooks` = 0 hits tree-wide. `Cursor-Code-only` = 0 hits. Surviving `~/.ecc` = 1 hit, `skills/unified-memory/SKILL.md:48` (`` `~/.ecc/memory/` ``) — verified upstream-identical per CHANGES.md, left as-is.

## (8) Counts — verified, with M1/M2 as the only stale statements

- Built tree (STEP 5, `fix16/build9.log:1871–1876`): skills 166, agents 72, rules 123, commands 87, hooks 15. `plugin.json`: hackathon-ecc 1.0.0 (`hackathon-ecc/.cursor-plugin/plugin.json`). Build log footer: "ERRORS: 0 NOTES: 11 CHANGES: 624 REMOVALS: 88".
- Stale statements found (both are findings M1/M2; no others): built README (169/96) and `LIVE_SMOKE_TEST.md:17` (168/96). No other count statements found in the tree, root README, or `.cursor-plugin/marketplace.json`.

## (9) JS syntax / JSON — 17/17 real files pass; 1 phantom path (M5)

`node --check` passed on all 17 existing surgically edited `.js` files (correct paths):
`scripts/lib/install/apply.js`, `scripts/lib/install-lifecycle.js`, `scripts/lib/install/plan.js`, `scripts/lib/install-targets/registry.js`, `scripts/lib/install/content-transform.js`, `scripts/lib/install-manifests.js`, `scripts/lib/install-executor.js`, `scripts/lib/session-adapters/registry.js`, `scripts/lib/session-adapters/canonical-session.js`, `scripts/lib/context-profile-commands.js`, `scripts/lib/context-carriers.js`, `scripts/lib/install/guarded-write.js`, `scripts/lib/install/contained-fs.js`, `scripts/lib/install/file-lock.js`, `scripts/lib/harness-capabilities.js`, `scripts/lib/harness-adapter-compliance.js`, `scripts/hooks/hookify-runtime.js`.
The 18th CHANGES.md entry, `scripts/lib/hooks/hookify-runtime.js`, does not exist (M5). All JSON files in the built tree parse (0 failures, `node_modules/` excluded).

## Adjudicated items — not re-flagged

Explicit `--domain` plain search reference rows; `hooks/adapter.js` is live Cursor infrastructure; byte-identical assets are not defects; `agent-emit-pi.js` dead code is Pi-native; command files with only `description:` frontmatter — 64/87, restated as "most command files", not a defect.

## What was verified clean (summary)

- Fix #16 pins: orchestrator / design-lead / implementer / deep-reasoner on `grok-4.7-high`; scout, fast-worker, GAN agents, and the 61 specialist agents on `cursor-grok-4.6-high-fast`; alias dict verbatim; model-route rows; schema enum; adapter rename; GAN command pins ×2/×3; `session-guardian.sh` deleted with no dangling reference; observer-loop.sh live with the reworded comment; smoke test §14 extended to the 4.6 pin; READMEs carry the Grok picker note; banned terms 0 across the tree including `node_modules/`.
- Fix #15 rules intact (39/43 verify15 checks pass; the 3 non-gates failures are explained by fix16's intended changes) and all standing #13 invariants re-verified with file:line evidence.
- Counts 166/72/123/87/15 consistent between the tree listing and the STEP 5 log; manifests 8↔9 identical (sha `796a48d1…`, 2,669 files); builds 8 and 9 both end "build complete".

## Open items (not findings)

- The `gates.md` question (M4) needs a coordinator call: keep the scrubbed wording or restore upstream-verbatim.
- B1's fix is a one-string change in dead code; M1–M3 are doc/comment edits.

## Counts

- BLOCKING: 1
- MINOR: 5
- Verdict: **NOT CLEAN** — fix round #16 does not close at zero errors; 1 blocking + 5 minor findings listed above.
