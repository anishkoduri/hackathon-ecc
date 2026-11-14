# Audit #51 — hackathon-ecc Cursor plugin (fix round #13j)

- **Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
- **build.sh:** 23,160 lines, md5 `b7432cc6ff576dbdf620b8d26bd87984`
- **Built-tree manifest:** `a188d10d2900e5b022d5ca173627fa07` (in both `fix13j/manifest1.txt` and `fix13j/manifest2.txt`)
- **Counts confirmed:** 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- **Scope of this round:** one item only — the snapshot manifest now lives in `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, with a one-line pointer in `.hackathon/run-ledger.md`, in BOTH engines.
- **Method:** READ-ONLY. No file in the plugin tree or `build.sh` was edited. Every finding below was verified by reading the built files directly. `fix13j/verify13j.py` was re-run by this auditor: **23/23 pass**.
- **Result: ZERO ERRORS — 0 blocking, 0 minor.**

## Blocking findings

None.

## Minor findings

None.

## (a) The fix13j change — verified in full, both engines

Both engine files were read end to end (`skills/orchestrate/SKILL.md`, 307 lines; `skills/orch-build-mvp/SKILL.md`, 68 lines).

### Orchestrate (`skills/orchestrate/SKILL.md`)

- **:8 — 20-line ledger cap intact.** "The **stage ledger** stays a short run-state file (20 lines max), not a PRD. Bulky loads overflow to `docs/run-ledger-appendix.md` (one line per item) with a one-line pointer in the ledger."
- **:60, step 5b snapshot intro** — the manifest (file list + per-file hashes) is recorded in `docs/run-ledger-appendix.md` (one line per file: relative path + hash), with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path + appendix file + line count), BEFORE any redesign file is overwritten.
- **:60, snapshot rule** — the manifest (snapshot path + full file list excluding `.hackathon/` and `.hallmark/candidate-evidence.md` + per-file hashes, one line per file) lives in `docs/run-ledger-appendix.md` under a `<redesign-id>` heading, with a one-line pointer in the ledger. States explicitly: "The manifest lives in the appendix, never in the ledger itself: a whole-tree file list is a bulky load, and the ledger stays a short run-state file."
- **:60, coverage check** — names the manifest file: "compares the design skill's changed-file list against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section)".
- **:60, revert step (2)** — both branches name the manifest file: created-file identification via "comparing the post-redesign tree against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section)", and the no-repo fallback: "verify against the snapshot manifest in `docs/run-ledger-appendix.md` (the `<redesign-id>` section) alone — each restored path diffed against its snapshot copy and its recorded hash". The `git checkout` mentions in the revert paragraph are explanatory warning text ("restores HEAD, not the verified state, and never deletes untracked files"), not restore instructions — not re-flagged per adjudication.
- **Per-redesign-id entries and budget line stay in the ledger:** `re-verification <redesign-id>: PASSED/BLOCKED` and `fresh-verdict rounds used: N/2` are recorded in `.hackathon/run-ledger.md` (single lines, not bulky loads). The `0/2` initialisation rule is present ("created as `fresh-verdict rounds used: 0/2` … when the run ledger is first created (at Gate 1…)").
- **5c deploy hold is scoped correctly:** "The hold blocks only the redesign: deploy the reverted verified tree and record its URL and deploy path in `.hackathon/run-ledger.md`." Step 6 re-verification check present.

### Standalone (`skills/orch-build-mvp/SKILL.md`)

- **:53, step 6b** — byte-identical wording to orchestrate for: snapshot intro (manifest in appendix, one-line pointer with snapshot path + appendix file + line count), snapshot rule (appendix under `<redesign-id>` heading, "manifest lives in the appendix, never in the ledger itself"), coverage check naming `docs/run-ledger-appendix.md` (the `<redesign-id>` section), revert step (2) identification and no-repo fallback naming the same file/section.
- **Self-contained appendix definition:** the rule defines the appendix inline ("bulky records go to the appendix (one line per item) with a one-line pointer in the ledger") — no standalone-wide ledger-cap rule was invented, as specified.
- **Shared fresh-verdict budget:** "2 rounds total across 6b and step 6 (ONE shared budget, not two)", `fresh-verdict rounds used: 0/2` created at Gate 1, round definition identical to orchestrate.
- **Steps 7/8 re-verification checks present**, both consulting the per-id ledger entry, with the deploy/commit hold scoped to the redesign and the reverted verified tree deployed/committed instead.

### Consistency checks across the whole tree

- **No stale wording remains:** `grep` for "per-file hashes in `.hackathon/run-ledger" returns 0 hits anywhere in the built tree.
- **No other file records the manifest:** "snapshot manifest" / "redesign-snapshot" appear only in the two engine files. The only other `run-ledger-appendix` reference is `skills/orch-pipeline/SKILL.md:81`, which records the approved `task_list` (one line per slice) in the appendix — a one-line-per-item overflow, not a manifest, and consistent with the cap rule.
- **Nothing else writes a bulky list into the ledger:** every `record … in .hackathon/run-ledger.md` instruction in both engines is a single line (re-verification entry, one-line pointer, deploy URL/path, merge decision).
- **Pointer format is usable:** snapshot path + appendix file + line count — the pointer names the file and the line count, and the manifest sits under a `<redesign-id>` heading, so the orchestrator can locate the exact section; the coverage check and both revert branches cite that same file + section.
- **Staged == built:** `diff new-skills/orchestrate/SKILL.md hackathon-ecc/skills/orchestrate/SKILL.md` → identical.
- **build.sh change scope:** `diff build.sh.before-fix13j build.sh` → 43 added lines, **0 deletions** — the fix13j patch block only (standalone patch, inserted last before STEP 5, with build-time asserts). No other file changed in this round.

## (b) Standing #13 invariants — verified clean

- **Single build engine per run:** orchestrate ("One build engine per run — orchestrate IS the first-build engine… orchestrate never invokes it") and orch-build-mvp ("One build engine per run… standalone only") agree; also in `rules/hackathon-mode.mdc` §1.
- **Cold-start direction chain:** orchestrate reads `docs/decision-record.md` first ("Start of run — read the decision record first"); orch-build-mvp step 1 reads record + scope by default, spec doc only as fallback.
- **Grok 4.7 High pin + picker instruction:** `grok-4.7-high` in slug form in orchestrate, orch-build-mvp, all four orch-* skills, `ecc-gan-planner`, `gan-build`/`gan-design` commands, README. Zero bracket-syntax hits (`grok-4.7-high[` → 0). Picker instruction (select Grok 4.7 High before the first build or the pin may silently fall back; file-level pin only, live smoke test decides) present in both engines.
- **Anti-derivative rule:** orchestrate row-10 section — "No design may be based off a searched external reference… the direction is GENERATED through the package skills"; mirrored in orch-build-mvp step 4.
- **"More, not bolder" posture:** orchestrate ("The package is applied fully, not conservatively: more design decisions… NOT necessarily bolder"); orch-build-mvp step 4 ("Posture is more, not bolder").
- **Auto-approval / auto-expansion:** `rules/hackathon-mode.mdc` §7 (gates auto-approve, ambiguity gate does not ask, escalations do not wait, narration-key prompt is the one sanctioned prompt) and §1 (feature-expansion Phases 0–3 automatic, no user gate; Phases 4–6 inside the build). End-of-project deferred-six run named in both engines and §3.
- **Deferred-six §3/§7 carve-out:** `rules/hackathon-mode.mdc` §3 lists the six (`production-audit`, `delivery-gate`, `codehealth-mcp`, `verification-loop`, `santa-method`, `security-scan`), "never fire during the first build", with the single named end-of-project run as the only permitted invocation; §7 repeats the carve-out. Both engines run the six by name before the final report.
- **Single-executor rule (browser-qa alone issues pass/fail verdicts on rendered screens):** orchestrate Verify step 5 ("`browser-qa` is the SOLE executor of this bar inside the visual loop"), Verify step 6 ("only `browser-qa`'s verdict decides whether a fix is owed"; Specificity under 3 and finish-review template observations are candidate evidence only); orch-build-mvp step 6 (same, plus `gan-style-harness` :118 "Screen distinctiveness is NOT scored here… judged ONLY by `browser-qa`"); `sloplint.mjs:2961` comment confirms Gate 38iii is a static/code-level check, "not a pass/fail verdict on a rendered screen — that verdict is `browser-qa`'s alone". Gates 63 (template punctuation), 65 (the named look), 67 (tracked-caps label) in `gates.md` are static text-pattern gates — code-level proxies, not screen verdicts. Static sloplint app-scope (`--scope app`) does not prove distinctiveness — stated in both engines.
- **SSML truth:** `skills/pitch-deck-video/SKILL.md:335-352` and `:539` (v2 family takes `<break>` up to 3s; `eleven_turbo_v2_5` deprecated; v3/v4 do NOT support breaks; Piper and `say` have no SSML) match `template/scripts/tts.mjs:88-91` and the voice-setting defaults in code (`tts.mjs:103-106`: stability 0.5, similarity_boost 0.75, style 0.0, speed 1.0).
- **Pins:** `puppeteer-core@25.17.0` pinned wherever the render tier is invoked (orchestrate Verify 6, orch-build-mvp step 6, design-taste-frontend, hallmark PROVENANCE). Other `npm install` hits are version-pinned (e.g. tailwindcss@4.3.5, @modelcontextprotocol/sdk@1.32.2).
- **Revert mechanics (prior rounds):** whole-tree file-copy snapshot excluding `.hackathon/` (self-referential) and `.hallmark/candidate-evidence.md` (live run state); run state never restored by a revert (rounds-used line and Superseded markings survive); untracked-file deletion in revert (2); redesign-id uniqueness (`-2`, `-3`, …). Present and identical in both engines.
- **Deploy-on-hold explicit:** both engines state the hold blocks only the redesign and the reverted verified tree is deployed/filmed/reported.

## Structural checks

- **Counts:** skills 169, agents 72, rules 123, commands 96, hooks 15 events in `hooks/hooks.json` (15 hook scripts + `hooks/adapter.js` = 16 `.js` files in `hooks/`; adapter is the live Cursor stdin adapter, not a hook event). 57 MB. No empty `SKILL.md` files.
- **Frontmatter:** all 169 skills have `SKILL.md` with `name:` matching the directory (0 mismatches). All 72 agents have frontmatter `name:` equal to the filename minus the `ecc-` prefix (uniform; the `ecc-code-reviewer` → `code-reviewer` reversion is the intended qc_patch behaviour, not a defect).
- **Commands:** 71/96 command files carry only `description:` frontmatter — matches the adjudicated count, not a defect.
- **`$ARGUMENTS` ask lines:** `commands/orch-add-feature.md:36`, `orch-change-feature.md:40`, `orch-fix-defect.md:40`, `orch-refine-code.md:41`, `plan-prd.md:31` ask the user when arguments are empty, each with the first-build carve-out; `commands/orch-build-mvp.md:41` says do NOT ask (defaults to record + scope) — as specified.
- **JSON validity:** `hooks/hooks.json`, `mcp.json`, `package.json` all parse.
- **`ui-ux-pro-max` --force:** `:112-114` — `--persist` skips writing unless `--force`; "Never use `--force` without explicit user authorization."
- **`orch-pipeline` "two human gates":** frontmatter description retains the wording — as specified.
- **montage / explainer:** `skills/pitch-deck-video/SKILL.md:469,479,487` — OpenMontage modes are opt-in only.
- **`agent-emit-pi.js`:** `scripts/lib/agent-emit-pi.js` (134 lines, Pi emitter) is unreferenced by any other file in the tree — Pi-native dead code by design, not re-flagged.
- **`triggersDigest`:** stored digest in `manifests/context-packs/skill-triggers@1.json:443` is stale by design — not re-flagged.
- **`themes/terminal.md`:** header block is theme material — not re-flagged per adjudication.

## Not flagged (per audit brief)

- OpenMontage runtime-fetch unpinned clone (`pitch-deck-video/references/openmontage/runtime-fetch.md:13,21`) — documented opt-in, parent decision.
- Unpinned `pip install` lines in restored upstream skills (e.g. `bengali-nlp`, `django-*`, `windows-desktop-e2e`, `pitch-deck-video` Piper fallback) — the separate pending pip pinning pass, out of scope for this audit.
- Adjudicated design items listed in the brief (explicit `--domain` plain search as reference rows only; byte-identical assets; `git checkout` explanatory text; dry-run observation that landing-redesign Gates apply; landing-page sloplint `--scope app` wording) — none re-flagged.

## Verdict

**ZERO ERRORS — 0 blocking, 0 minor.** The fix13j change is correctly and consistently routed in both engines, the 20-line ledger cap and all standing #13 invariants hold, and no new defect was found in the full-tree sweep. The audit loop closes when dry-run #23 and the sweep are also clean.
