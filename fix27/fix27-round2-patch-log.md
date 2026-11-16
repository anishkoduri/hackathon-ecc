# fix27 round-2 patch log (audit #74, build-time half)

Date: Nov 16, 2026. Worker: build-time half only — `fix27/fix27.py`,
`fix27/verify27.py`, `fix25/callmap/generate_call_map.py`. The staged
half (orchestrate, hackathon-mode §5/§6/§7, dispatch-prompt, B3, B4,
B12-staged, B14, M1, M2, M8) belongs to the staged-edits worker and is
NOT touched here. No push, no full build, no fix11 re-run, no subagents.

## Count moves (final)

- Skills 66 → **67** (motionsites-web-builder vendored; STEP 2 copies
  `new-skills/motionsites-web-builder/` into `skills/`).
- Agents **45** (unchanged).
- Rules **123** (unchanged).
- Commands 60 → **55** (learn-eval, project-init, projects, promote,
  prune CUT; 32 dropped total).
- Trigger keys **49** (unchanged); coverage.skills 66 → **67**.
- Tokens 18 → **19** (+ MOTIONSITES_F27).

## Patches added to fix27.py

### §4 trigger table
- `coverage.skills` 66 → 67.
- M3: `notes` deferred list `production-audit, delivery-gate,
  codehealth-mcp, santa-method, security-scan, verification-loop` →
  `verification-loop, production-audit, delivery-gate. (DEFER3_F27)`.

### §5 README
- Count lines 66/60 → 67/55 (4 subs, anchors unchanged from round 1).
- M5: marketplace list drops `brainstorming`,
  `dispatching-parallel-agents`, `agents-md-generator` (:26-27);
  `codebase-memory` :29 line reworded to "cut in fix #27 … explore
  with grep-and-read and the `ecc-code-explorer` agent instead";
  :36 "Playwright MCP, codebase-memory MCP," → "Playwright MCP";
  "Commands (highlights — 3 of 87)" → "3 of 55"; :54-56 deferred set
  → `verification-loop`, `production-audit`, `delivery-gate`, and the
  `/security-scan` mention in :56 removed. NOT touched: :11
  "codebase-memory MCP servers" — that line describes the stock ECC
  profile as shipped upstream, where the server genuinely ships;
  audit M5 did not list it.

### §7a B1 — inherit-legacy-style re-route (REROUTE_F27)
- `skills/orch-add-feature/SKILL.md:33`,
  `skills/orch-change-feature/SKILL.md:36`,
  `skills/orch-fix-defect/SKILL.md:36`,
  `skills/orch-refine-code/SKILL.md:35`:
  `legacy style drift: + `inherit-legacy-style`` →
  `legacy style drift: handled inside the design package — no separate
  skill (fix #27, REROUTE_F27)`.
- `skills/orch-build-mvp/SKILL.md:41`: `legacy drift: +
  `inherit-legacy-style`` → same re-route wording.
- `skills/ui-ux-pro-max/SKILL.md:363`: `On a hand-written legacy
  codebase, run `inherit-legacy-style` before writing UI, …` →
  `… legacy style drift is handled inside the design package — no
  separate skill (fix #27, REROUTE_F27) — so new work follows …`.
  (orchestrate's own copies + dispatch-prompt.md:24 are staged-owned.)

### §7b B2 — theme cage lifted, ECC-origin E1 copies (THEME-START_F27)
- `skills/orch-build-mvp/SKILL.md:43`,
  `skills/ui-ux-pro-max/SKILL.md:274` (3 subs each, mirroring
  orchestrate:148 / design-taste-frontend:423):
  bound (2) `fit the theme's material world — material, tokens, palette
  balance, do-nots;` → same + ` — **or a recorded departure from
  it** (D19 reason required) (fix #27, THEME-START_F27);`
  `NOT within reason: a new theme (re-deal instead, Taste step 4); a new
  palette` → `NOT within reason: a new palette`
  `… (craft-floor bans are absolute; the Hallmark floor binds). Each
  invented element's` → `… binds). Inventing a theme direction is a
  recorded D19 decision, not a forbidden move (fix #27,
  THEME-START_F27): a departure from the dealt theme is recorded with
  what was departed from and why the job needs it — a re-deal is the
  easy path, a recorded departure is the permitted one. Each invented
  element's`

### §7c B5 — prp-commit re-route
- `commands/prp-commit.md:59`: `Draft the message with the
  `conventional-commit-review` skill
  (`skills/conventional-commit-review/SKILL.md`, fix #25 §1)` →
  `Draft the message with the `git-workflow` skill
  (`skills/git-workflow/SKILL.md`)` (same as orchestrate §6).

### §7d B6 — CLv2 remnants in kept commands
- `commands/skill-create.md`: delete `:16` `/skill-create --instincts`
  usage line; delete `:24` `4. **Optionally Creates Instincts**` step;
  delete whole Step 4 CLv2 section `:139-160` (heading + instinct YAML
  template); delete `## Related Commands` `:171-174`
  (`/instinct-import`, `/instinct-status`, `/evolve` — all dropped).
- `commands/ecc-guide.md:85`: delete ``- `/project-init` for stack-aware
  ECC onboarding of a target project``.
- `commands/epic-sync.md:20-22`: delete `Compatibility aliases:` +
  ``- `/projects`` (dropped command).

### §7e B7 — /security-scan pointers → kept security-review
- `commands/ecc-guide.md:89`: ``- `/security-scan` (END-ONLY) …`` →
  ``- `security-review` skill (END-ONLY) …``.
- `commands/fastapi-review.md:39`: `- Command: `/security-scan` …` →
  `- Skill: `security-review` …`.
- `commands/harness-audit.md:2`: `… use the security-scan command
  (END-ONLY …)` → `… use the `security-review` skill (END-ONLY …)`.
- `rules/react-native-security.mdc:43`: `Use `/security-scan`
  (AgentShield, END-ONLY …)` → `Use the `security-review` skill
  (END-ONLY …)`.
- `scripts/harness-audit.js:582-589`: `security-scan-command` check
  re-pointed — `path` → `skills/security-review/SKILL.md`,
  `description` → `Security review skill exists`, `pass` →
  `fileExists(rootDir, 'skills/security-review/SKILL.md')`, `fix` →
  `Add skills/security-review with the security review workflow.`
  Check id NOT renamed (referenced elsewhere).

### §7f B8 — council santa-method re-route
- `skills/council/SKILL.md:37`: `… at the end of the project:
  `santa-method`` → `… at the end of the project: `verification-loop` /
  `production-audit``.
- `:40`: `` `code-reviewer` or, at the end of the project, `santa-method` ``
  → `` `code-reviewer` or, at the end of the project,
  `verification-loop` / `production-audit` ``.
- `:184-185` (also M6): delete both Related Skills lines
  (`` `santa-method` — adversarial verification (END-ONLY) `` and
  `` `architecture-decision-records` — formalize the outcome … ``).

### §7g B9 — integration re-routes (REROUTE_F27)
- `:21`: `… (that is `mcp-server-patterns`)` → `… (hand-roll the client
  via `api-integration`) (fix #27, REROUTE_F27 — `mcp-server-patterns`
  was cut)`.
- `:46`: `Use `skill-scout` to search …` → `Use `documentation-lookup`
  (grep-and-read over the plugin's own skill list) to search … (fix
  #27, REROUTE_F27 — `skill-scout` was cut)`.
- `:60`: `Use `mcp-server-patterns` for the server setup and wiring …`
  → `Use a hand-rolled client via `api-integration` for the server
  setup and wiring … (fix #27, REROUTE_F27 — `mcp-server-patterns` was
  cut)`.
- `:122`: composition list drops `skill-scout` and
  `mcp-server-patterns`, with `(fix #27, REROUTE_F27 — `skill-scout`
  and `mcp-server-patterns` were cut)` appended.

### §7h B10 — ai-feature-spec re-route
- `skills/ai-feature-spec/SKILL.md:3`: `For non-AI features use
  intent-driven-development; …` → `For non-AI features use
  hackathon-scope; …`.

### §7i B11 — ecc-agent-evaluator self-contained (OWED-5 RESOLVED)
- `agents/ecc-agent-evaluator.md:3`: delete `, or when the
  agent-self-evaluation skill is active`.
- `:24`: delete `Read `skills/agent-self-evaluation/SKILL.md` for the
  detailed scoring rubric. ` (the rubric is the 5 axes in this file).
- `:54`: `Work through the 5 axes from the `agent-self-evaluation`
  skill:` → `Work through the 5 axes defined below:`.
- `:69`: `… (matches `skills/agent-self-evaluation/scripts/evaluate.py`
  output):` → `… (defined in this file):`.
- `:110`: `… matching the
  `skills/agent-self-evaluation/scripts/evaluate.py` output format
  exactly.` → `… matching the output format defined in this file
  exactly.`

### §7j B12 (build-time half) — mobile-ship
- `skills/mobile-ship/SKILL.md:9`: `belongs to react-native-patterns /
  dart-flutter-patterns.` → `belongs to react-native-patterns.`
  (hackathon-mode.mdc §6 is staged-owned.)

### §7k B13 — systematic-debugging
- `skills/systematic-debugging/SKILL.md:3`: delete the parenthetical
  `(agent-introspection-debugging)`.

### §7l B15 — skill-create / skill-health descriptions
- `commands/skill-create.md:3`: `check the skill-scout skill first …`
  → `check the plugin's own skill list (grep-and-read) first …`.
- `commands/skill-health.md:3`: `… use the skill-stocktake skill.` →
  `… use the plugin's own skill list and verify scripts.`

### §7m M4 — delivery-gate "shipped" claims
- `skills/delivery-gate/SKILL.md:3`: `Complements
  agent-self-evaluation (the shipped equivalent …)` → `Complements the
  `ecc-agent-evaluator` agent (whose 5-axis rubric is defined in the
  agent file itself) …`.
- `:13`: `… (like the shipped `agent-self-evaluation` skill — the
  upstream `self-audit` skill is not shipped …): …;
  agent-self-evaluation checks output quality across four reasoning
  dimensions.` → `… (like the former `agent-self-evaluation` skill —
  cut in fix #27; its 5-axis rubric now lives in the
  `ecc-agent-evaluator` agent file): …; the evaluator checks output
  quality across five reasoning dimensions.`
- `:15`: `- **agent-self-evaluation** (shipped; …)` → `-
  **`ecc-agent-evaluator`** (reasoning-quality gate; the 5-axis rubric
  formerly in `agent-self-evaluation` now lives in the agent file
  itself): …`.
- `:111`: ``- `agent-self-evaluation` — Reasoning quality gate
  (completeness/consistency/groundedness/honesty; shipped equivalent
  …)`` → ``- `ecc-agent-evaluator` — Reasoning quality gate
  (accuracy/completeness/clarity/actionability/conciseness; the 5-axis
  rubric formerly in `agent-self-evaluation` now lives in the agent
  file itself)``.

### §7n M6 — dangling "see skill" pointers
- `skills/contract-first/SKILL.md:15`: delete `, and
  `ai-regression-testing`, which guards fixed bugs from returning.`;
  `:284`: delete the ``- `ai-regression-testing` - regression tests …``
  Related Skills line.
- `agents/ecc-database-reviewer.md:93`: `see skills:
  `postgres-patterns` and `database-migrations`.` → `see skill:
  `postgres-patterns`.`.
- `skills/tdd-workflow/SKILL.md:300`: delete ` See the `bun-runtime`
  skill for runtime, install, and bundler details.`
- `skills/postgres-patterns/SKILL.md:143`: delete the ``- Skill:
  `clickhouse-io` - ClickHouse analytics patterns`` line.
- `skills/react-patterns/SKILL.md:269`: delete `, [accessibility]
  (../accessibility/SKILL.md), [angular-developer]
  (../angular-developer/SKILL.md) for framework comparison`.
- `skills/typescript-patterns/SKILL.md:589`: delete the
  ``- `nestjs-patterns` — …`` line; `:592`: delete the
  ``- `prisma-patterns` — …`` line.
- `skills/react-native-patterns/SKILL.md:324`: delete the
  ``- `coding-standards` — TypeScript/JavaScript idioms …`` line.
- `skills/strategic-compact/SKILL.md:153`: ``- `continuous-learning`
  skill — Extracts patterns before session ends`` → ``- `/learn`
  command — Extracts patterns before session ends``.
- `scripts/lib/resolve-ecc-root.js:25`: `DEFAULT_SKILL_PROBE =
  path.join('skills', 'continuous-learning-v2')` →
  `path.join('skills', 'orchestrate')`, and the comment above it now
  says the sentinel moved from continuous-learning-v2 to orchestrate
  in fix #27.

### §7o B6-adjacent (census-found, not in audit #74)
- `commands/skill-health.md:46`: `… suggest running /evolve` →
  `… suggest running /learn`. The check-12 census found this live
  dispatch to the dropped /evolve command; /learn is the kept
  session-review tool that extracts declining patterns as candidate
  skills.

### Other fix27.py changes
- `DROPPED_COMMANDS`: + learn-eval, project-init, projects, promote,
  prune (27 → 32); `COMMAND_DECISIONS` gains one entry each
  (learn-eval duplicates /learn, rubric source removed; project-init
  is ECC onboarding, example names removed CLv2; projects/promote/
  prune run the removed instinct-cli.py).
- Stale-count scan: also flags `66 skills` / `60 commands`; the
  generator-owned call map is excluded (regenerated by the fix25
  generator, whose EXPECTED counts guard it).
- OWED list rewritten (M9): OWED-1 RESOLVED (call map regenerated);
  OWED-4 RESOLVED (all CLv2 commands dropped; learn KEPT);
  OWED-5 RESOLVED (B11); OWED-6 RESOLVED (feature-expansion
  re-routed, round 1); OWED-7 RESOLVED (M3); OWED-9 RESOLVED (M4);
  OWED-10 RESOLVED (B15 — and the round-1 "advisory" label corrected:
  these were imperative routing lines in descriptions);
  OWED-12 LANDED (staged worker, this round — B12/B14);
  OWED-13 CORRECTED (blanket "all prose-history" claim replaced with
  the census record; full file:line list is in the fix27.py OWED-13
  text). OWED-2/3/8 unchanged (RESOLVED); OWED-11 unchanged
  (rules-debloat follow-up).

## verify27.py changes
- `KEPT_SKILLS` + `motionsites-web-builder` (66 → 67);
  `DROPPED_COMMANDS` + 5 (27 → 32); `KEPT_COMMANDS` − 5 (60 → 55);
  `F27_TOKENS` + `MOTIONSITES_F27` (18 → 19).
- Checks 1/5/6/7 updated to 67/45/123/55, coverage.skills 67, README
  67/55, 19 tokens; check 6 stale scan also flags `66 skills` /
  `60 commands`; MOTIONSITES_F27 asserted in
  `skills/motionsites-web-builder/SKILL.md`.
- Check 10b added: one assertion per round-2 patch (new text present
  ×1, old text gone).
- Check 11: patch-log path now derived from BASE (same file for the
  default tree; the scratch run log for a scratch tree) and asserts 0
  errors with 100 skills + 32 commands accounted for (tolerates the
  "already absent" scratch form).
- Check 12 added (audit #74 M10): CUT-name sweep over skills/,
  agents/, commands/, rules/ (excluding the regenerated call map).
  Two tiers — STRONG (backticked / pathed / slashed / skill-adjacent)
  for every name, BARE word-boundary only for non-generic names;
  generic bare-word uses (accessibility, brainstorming, evolve,
  projects, promote, prune) are counted as noise, never failing.
  Allow-list: file → allowed lines, each justified (see below).

## generate_call_map.py changes (5 places)
- Docstring counts 66/60 → 67/55; `EXPECTED` skills 66 → 67,
  commands 60 → 55; section headers `Skills (66)` → `Skills (67)`,
  `Commands (60)` → `Commands (55)`.

## Check-12 allow-list summary (101 whole-line + 1 name-scoped)
- Prose-history "was cut / NOT invoked" (REROUTE_F27): delivery-gate
  :13, :15, :111; feature-expansion :49, :100, :188, :190, :192, :193,
  :204; integration :21, :46, :60, :122.
- Generic verb / upstream attribution: feature-expansion :3, :211.
- Negative statements: ecc-spec-miner :3, :40, :201 ("does not
  require"); learn.md:2 (distinguishes from CLv2); hackathon-mode
  :37, :38 ("is not used", "deliberately NOT wired").
- Pointer-style (M7/OWED-11 class): react-patterns :254,
  react-performance :566, react-testing :247, :359,
  polish-pass/vercel-checklist.md :105, :108, :111, :115, :118, :121,
  :124, :127, :139, :146, :171 (citations), ecc-a11y-architect :148,
  ecc-react-reviewer :161, ecc-typescript-reviewer :119,
  react-review :169, react-test :263, and the rules/*.mdc "See skill"
  lines — golang-coding-style :31, golang-patterns :44,
  golang-testing :30, kotlin-coding-style :39, kotlin-patterns :50,
  kotlin-testing :38, angular-patterns :249, angular-testing :164,
  cpp-coding-style :44, cpp-patterns :51, cpp-security :51,
  cpp-testing :44, dart-patterns :260, :261, java-coding-style :113,
  :114, java-patterns :145, :146, :147, java-testing :114, :115, :131,
  :132, :133, nuxt-coding-style :45, nuxt-hooks :37, nuxt-patterns
  :51, nuxt-security :46, nuxt-testing :47, perl-coding-style :46,
  perl-patterns :76, perl-testing :54, react-patterns :194,
  rust-coding-style :151, rust-patterns :168, rust-security :140,
  rust-testing :154.
- Data (not skill references): design-taste-frontend demo.html :74,
  index.json :5569 (icon ids); ui-ux-pro-max
  phosphor-icons-upstream.json :8306, :22481, :22557, :28089, :28112,
  :32160, :32184, scripts/core.py :232, :233, :240, :264, :594,
  design_system.py :622, :805, reasoning_contract.py :41,
  tests/fixtures/relevance-cases.json :27, :29, :36, :39, :105.
- Name-scoped: hackathon-mode.mdc:46 `product-lens` /
  `intent-driven-development` ("do not scope hackathons"); the
  `brainstorming` name on that line is NOT allowed (live B12 dispatch).
- Generic bare-word noise (counted, never failing): 294 lines
  (projects 156, accessibility 132, promote 4, brainstorming 3,
  evolve 1, prune 1).

## Scratch-test evidence
Method: the live built tree already has round 1 applied, so the
scratch tree was reconstructed to pre-fix27 with
`fix27/scratch/f27r2-revert-round1.py` (reverts the round-1 text
patches, restores the 15 pruned trigger keys with their exact pre-fix27
phrases from `fix27/scratch/call-map-data-before-f27.json`, coverage
166/64). The 100 CUT skill dirs / 27 agents / 27 round-1 commands
were NOT restored — fix27.py tolerates already-absent removals — so
the scratch run reports "0 dirs (100 already absent)"; the real build
will report "100 dirs". Scratch tree:
`fix27/scratch/f27r2-test/` (+ `new-skills/motionsites-web-builder/`
copied into its `skills/`, mimicking STEP 2).

- fix27.py on scratch: **exit 0, 86 changes, 0 errors**
  (`fix27/scratch/f27r2-fix27-run.log`; run log at
  `fix27/scratch/fix27/fix27-patch-log.md`). Scratch tree after the
  run: 67 skills / 45 agents / 123 rules / 55 commands; trigger keys
  49, coverage.skills 67; 5 round-2 commands removed;
  MOTIONSITES_F27 ×2 in the vendored skill.
- Census (`fix27/scratch/f27r2-census.py`, output
  `fix27/scratch/f27r2-census.txt`): **110 hits** → 101 allow-listed,
  9 staged-owned live dispatches (see Un-done).
- Generator (shadow root `fix27/scratch/shadow/`, updated
  `generate_call_map.py`): **exit 0**, counts 67/45/123/55/15/49 all
  OK; map headers `Skills (67)` / `Commands (55)`; no rows for
  learn-eval / project-init / projects / promote / prune;
  `motionsites-web-builder` called (via staged orchestrate /
  hackathon-mode / design-taste-frontend). Regenerated map copied
  into the scratch tree before verify27 ran.
- verify27.py on the faithful scratch tree: **71/73 pass**. Failures:
  check 8 (banned terms — see Un-done #1) and check 12 (the 9
  staged-owned hits).
- verify27.py on the staged-simulation tree
  (`fix27/scratch/f27r2-test-staged-sim/`, built with
  `fix27/scratch/f27r2-simulate-staged.py`, TEST-ONLY minimal
  re-routes of the staged worker's B1/B3/B4/B12 items — never shipped):
  **72/73 pass; check 12 PASSES** (0 un-allow-listed, 102
  allow-listed). Only check 8 fails there. This validates the check-12
  logic end to end: it fails exactly on the staged-owned dispatches
  and passes once they are re-routed.

## Un-done (with reasons)
1. **verify27 check 8 (banned terms) FAILS on the vendored
   motionsites-web-builder skill** — 5 hits: `SKILL.md:25, :36`
   (raw GitHub URLs containing the upstream repo name
   `Motionsites-AI/claude-skill`), `references/builders.md:10`
   ("Cursor / Claude Code"), `LICENSE:1` ("MotionSites Web Builder —
   Claude skill"). The two URL occurrences cannot be reworded without
   breaking the use-time fetch; the staged skill files are read-only
   for this worker; no exception was added to check 8 (weakening a
   guardrail was not authorized). Coordinator decision needed:
   narrow check-8 exception for the upstream `claude-skill` repo-name
   URLs (and the LICENSE/builders rows), a staged-source edit, or
   dropping the skill. The skill is otherwise wired (counts, token).
2. **verify27 check 12 FAILS on 9 staged-owned live dispatches** —
   `skills/orchestrate/SKILL.md:3` (B4 dispatching-parallel-agents),
   `:65` (B1 inherit-legacy-style), `:136` (B3 ecc-recipes + `/prune`
   + continuous-learning), `:138` (B1),
   `skills/orchestrate/references/dispatch-prompt.md:24` (B1),
   `rules/hackathon-mode.mdc:46` brainstorming (B12), `:48` (B4),
   `:53` (B12 dart-flutter-patterns), `:55` (B12 codebase-memory).
   These are the staged worker's half; verify27 check 12 passes once
   they land and the tree is rebuilt (proven by the staged-sim run:
   72/73, check 12 PASS). Deliberately NOT allow-listed.
3. **B14** (hackathon-mode §7 precondition vs orchestrate:57),
   **B3** (orchestrate:136 ecc-recipes), **B4** (orchestrate:3,
   hackathon-mode:48), **M1/M2/M8** — staged worker's or out of
   scope; not touched.
4. **M7 / OWED-11 rules pointers** — carried to the rules-debloat
   follow-up by design; allow-listed as pointers in check 12.
5. **M11 prior verifiers** (verify26/verify25 crash on the reduced
   tree) — not in this worker's scope; not touched.
6. **harness-audit.js:526-529 `continuous-learning-v2` skill-exists
   check** (fails by design now, same class as B7's
   security-scan-command check) and the CLv2 hook machinery
   (`scripts/hooks/observe-runner.js`,
   `scripts/hooks/posttooluse-dispatcher.js` — audit #74 already
   classified as not wired) — not assigned in this round; check 12
   does not sweep `scripts/`, so they do not block verification.
   Flagged for the coordinator.
7. **README:11 "codebase-memory MCP servers"** left alone deliberately
   (stock-profile description; audit M5 did not list it).
8. **Allow-list fragility**: `rules/hackathon-mode.mdc:37, :38` sit in
   a staged-owned file — if the staged worker's edits shift lines
   above them, re-run the census (`fix27/scratch/f27r2-census.py`)
   and update the line numbers in verify27.py. The name-scoped
   `:46` entry needs no update: it passes the moment the staged B12
   fix lands.

## Coordinator additions (Nov 16, 2026, after Worker B)
- fix27.py §7e (B7 extension): harness-audit.js `memory-learning-skill` check re-pointed from removed `skills/continuous-learning-v2/SKILL.md` to kept `skills/growth-log/SKILL.md` (same class as B7 — asserts a removed skill exists, fails by design on every run; found by the coordinator while triaging Worker B's report). Check id unchanged.
- verify27.py: F27_TOKENS 19 → 20 (+PALETTE-FIRST_F27, in design-taste-frontend + orchestrate + hackathon-mode); check-7 name updated; 3 PALETTE-FIRST location checks added (total checks 73 → 76).
- verify27.py check 8 rewritten: file-level grep → line-level grep with a 3-line allow-list (skills/motionsites-web-builder/SKILL.md:25, :36 — raw-GitHub fetch URLs carrying the upstream repo name "claude-skill", rewording breaks the fetch; skills/motionsites-web-builder/LICENSE:1 — upstream license title, MIT notice ships verbatim). Narrow exception, not a weakening: a functional address + a license document, not Claude-product branding. Decision: keep the skill (MIT permits the vendoring; the promo was already stripped) rather than drop it over 3 unavoidable lines.

## Coordinator addition (Nov 16, 2026 — verify27 75/76 follow-up)
- verify27.py check-12 ALLOW_LIST: added "skills/orchestrate/SKILL.md": {136: "prose-history: 'ecc-recipes was cut' (REROUTE_F27)"}. The line's other two flagged names (continuous-learning, /prune) were removed from the staged source (see staged-patch-log) because they referenced removed things; only the prose-history note remains.
