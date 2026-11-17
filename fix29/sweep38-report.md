# Sweep #38 — fix #29 — INDEPENDENT RE-SWEEP REPORT

**Verdict: SWEEP #38: CLEAN** — 0 blocking, 0 minor. The run-12 built tree
passes every check in the sweep #37 scope, adapted to fix #29.

**Scope.** Re-sweep of the run-12 built tree (`hackathon-ecc/`) + staged
sources (`new-skills/`, `new-rules/`), same scope as sweep #37: weaving
coherence (all 7 `_F29` tokens, GLOBAL-ROUTING byte-identity, the 9 §2(c)
reconciliations, correction-brief sites, dispatch-prompt templates),
staged-vs-built scoping check, stale-count sweep, dangling-reference
sweep, README consistency, SPEC §6 criterion cross-check, plus the two
carried observations (F35 fragility, F-O scope note). Read-only except
this report. I did not trust the coordinator's claims: every item below
was verified by my own greps, diffs, and file reads. `verify29.py` was
re-run by me (315/315, exit 0 — see below), not merely read. No
live-browser or Cursor-session check was needed or performed. `build.sh`
was not run; `fix11/fix11-stage.py` was not run; nothing was committed,
pushed, or messaged. No scratch mirror was needed (no mutations run);
nothing was left behind in `/tmp` or `fix29/scratch-tmp/`.

---

## BLOCKING findings

None. (Numbered 38-Ax: none issued.)

---

## MINOR findings

None. (Numbered 38-Bx: none issued.)

---

## Notes / observations (checked and cleared)

### (a) Weaving coherence — CLEAN

- **All 7 `_F29` tokens present in their homes** (own Python counter over
  the built tree, excl. `node_modules`; totals are occurrences):
  ORCHESTRATOR-ONLY_F29 11 in 11 files, FACTORY-DISPATCH_F29 4 in 4,
  DIRECTOR-BRIEF_F29 9 in 7, NO-GUESSING_F29 18 in 9, VERIFY-MERGE_F29 8
  in 6, GLOBAL-ROUTING_F29 24 in 18, COST-AWARE_F29 6 in 6.
  Every one of the 10 in-scope skills carries `_F29` tokens on disk
  (orchestrate 11, orch-pipeline 8, feature-expansion 8,
  gan-style-harness 8, orch-build-mvp 4, orch-refine-code 3,
  orch-add-feature 2, orch-change-feature 2, orch-fix-defect 2,
  design-taste-frontend 1 in SKILL.md + 7 in `redesign.md`;
  hackathon-mode 7). Every covered-by-reference site carries a token:
  `rules/common-agents.mdc:26` (full factory line, incl. both COST-AWARE
  rules), `commands/gan-build.md:12`, `commands/gan-design.md:10`,
  `commands/react-build.md:9`, `commands/astra-review.md:34`,
  `commands/orch-refine-code.md:33` (step-2 qualification, plus the
  skill's step-2 line at `skills/orch-refine-code/SKILL.md:35`),
  `agents/deep-reasoner.md:17` (rewritten NO-GUESSING bound).
  `agents/ecc-gan-planner.md` carries zero `_F29` tokens — see
  observation (h) below; the re-route itself is present and asserted.
- **GLOBAL-ROUTING block byte-identical staged = built = golden.**
  Extracted the block line from each of the four sources and compared
  against `fix29/global-routing-block.txt`: stripped md5 `68206505…`
  in staged + built orchestrate (`:36`) and staged + built
  hackathon-mode (`:45`, after the established `- ` bullet-marker
  strip); raw golden-file md5 `bdf1720f…`, matching the manifest's
  recorded values. Length 2,285 chars in all four.
- **"Factory routing (fix #29" in exactly 13 files ×1 each**
  (astra-review, gan-build, gan-design, react-build, redesign.md,
  feature-expansion, gan-style-harness, orch-add-feature,
  orch-build-mvp, orch-change-feature, orch-fix-defect, orch-pipeline,
  orch-refine-code skill). Orchestrate + hackathon-mode carry the full
  block instead of the pointer string, as designed; DTF SKILL.md:455
  carries the lowercase pointer clause, not the bold string.
- **The 9 §2(c) reconciliations hold live** (each spot-checked by
  reading the live lines, not by trusting the manifest):
  1. Belief vs NO-GUESSING: exactly 5 "Belief in the brief" copies
     (feature-expansion, orch-build-mvp, orch-pipeline, orchestrate,
     dispatch-prompt.md), all carved; tie-breaker
     ("When in doubt which side an ambiguity falls on, return the
     question") on 6 lines in 5 files (the 5 copies + the fast-worker
     preamble short form, via dispatch-prompt.md ×2); "pick the
     reasonable option" on 5 lines (10 occurrences — Belief sentence +
     carve-out quotation per line, per the #93-A precision note);
     unbounded "state the assumption you made and proceed" 0×
     tree-wide; "instead of NEEDS_CONTEXT" 0×; "state the assumption"
     on 11 lines in exactly the 6 known bounded files
     (deep-reasoner, orchestrate, dispatch-prompt.md ×4, polish-pass
     ×3, impeccable-critique, systematic-debugging). First-build
     carve-out reconciled at the six sites (status vocabulary :52,
     mechanical preamble :96/:99, reasoning :151, worked example
     :215/:218); deep-reasoner.md:17 reads "return NEEDS_CONTEXT
     naming exactly what is missing — do not guess" with the identical
     NO-GUESSING bound + tie-breaker.
  2. Merge-order bridges at all 3 sites: orchestrate:93, MVP:71
     (both "applies only if partitioning failed and two [drones /
     implementers] touched the same file anyway — sequential dispatch
     for overlapping scopes is the prevention rule"), FE:160
     ("Collision procedure (sequential dispatch for overlapping scopes
     is the prevention rule; this is what happens if a collision still
     occurs)").
  3. Feature-expansion Team shape vs factory cap: FE:141 "one
     implementer per feature, up to 4 in parallel" with dependency
     waves + sequential overlap, inside the factory paragraph at :139.
  4. Feature-expansion brief format: items 1–9 present, with item 2
     naming files explicitly OUT of scope (:146), 4a acceptance
     criteria (:148) / 4b verification steps (:149) split, item 9
     return format (:154), item 3 constraints (:147).
  5. GAN evaluator vs VERIFY-MERGE: orchestrator verify step in the
     skill (:69, :155 mirror) and in the wiring
     (gan-build.md ORCHESTRATOR-CHECK :63, planner-spec check 3a :30,
     CHECK SCORE gated); rubric-pass-with-failed-criterion-is-a-fail
     stated at all three; GENERATE block carries Verification steps
     and Return format lines.
  6. Orchestrate contract vs DIRECTOR-BRIEF: dispatch-prompt.md:15
     enumerates all seven fields; :4 no-drop rule reads "delete no
     DIRECTOR-BRIEF field — a field with nothing to list is written
     as `none`, never deleted". Per-template field counts (own
     section-scoped count): recon / mechanical / reasoning / worked
     example 7/7 each (Goal, Inputs, Constraints, Interface,
     Acceptance check, Verification steps, Return format — Interface:
     at recon :70, mechanical :107, reasoning :139, worked example
     :230); blind reviewer 6/7 (no Interface: — exempt by design, own
     verification-gate contract at :15/:170–207, and it does carry
     Verification steps: at :197); second-pass exempt, opinion-only
     (only a Constraints slot; NEEDS_CONTEXT line at :167).
  7. Correction brief constructed at all 8 sites, each naming the
     failed criterion: "correction brief naming the failed" occurs on
     11 lines — gan-style-harness :69/:155 (paragraph + mirror),
     orch-pipeline :74, feature-expansion :158, redesign.md :68,
     orchestrate ladder :252, gan-build planner-spec 3a :30,
     gan-build ORCHESTRATOR-CHECK :63, react-build step 6 :18,
     astra-review :35. All 11 lines read in full; every one names the
     failed acceptance criterion and the required correction.
  8. Harness-gate clause ("slots refill per wave, not per completion")
     in all 5 factory paragraphs (orch-pipeline, feature-expansion,
     gan-style-harness, redesign.md, orchestrate step 4 — 1× each).
  9. Staged-vs-built drift: see (b).
- **Dispatch-prompt step-0 / pointer lines:** gan-build.md:26 carries
  the inline-invocation parenthetical verbatim ("the design-lead is
  invoked inline as the orchestrator here, not spawned as a drone — a
  spawned execution must carry a director brief"); gan-design.md:19
  carries the identical parenthetical; gan-design.md:10 carries the
  full factory pointer; astra-review.md:34 pointer + :35 extended
  second blind pass (naming the fix brief's acceptance criteria,
  correction brief, cap of two re-dispatches).

### (b) Scoping check — the 41 staged-vs-built diff lines are BY DESIGN

Own `diff` of each of the 7 staged files against its built counterpart
(`diff | grep -c '^[<>]'`):

| Staged file | Diff lines | Hunks |
|---|---|---|
| orchestrate SKILL.md | 6 | :100, :274, :281 agent-citation expansions |
| hackathon-mode.mdc | 2 | :38 `claude -p` → CLI-subprocess |
| feature-expansion SKILL.md | 22 | :3, :12, :33–34, :49, :137, :164, :196, :198–199, :217 (11 changed lines) |
| design-taste-frontend SKILL.md | 11 | description block :9–14, 5 lines → 6 |
| dispatch-prompt.md | 0 | — |
| deep-reasoner.md | 0 | — |
| fast-worker.md | 0 | — |

Total **41 diff lines across 4 files, zero `_F29` hunks** (own grep of
every diff output for `_F29`: 0 in all 7). The hunks match the recorded
by-design transforms exactly: the orchestrate :100/:274/:281 lines are
bare `` `code-reviewer` `` / `` `security-reviewer` `` becoming house
form `` `code-reviewer` agent (`agents/ecc-code-reviewer.md`) ``; the
hackathon-mode :38 line is the fix16 scrub. The fix16 anchor was
verified by reading the code, not just the citation:
`fix16/fix16.py:3807` opens the `sub(` call, `:3808` carries the anchor
string "(its upstream `claude -p` invocation path does not run in
Cursor", the call spans 3807–3809, and `build.sh:23222` runs fix16 on
every build — syncing staged :38 to the built text would break the
build, as the manifest records. The FE hunks are the build.sh rewrites
(:580, :622, :746 per the manifest) plus the same citation-expansion
class; the DTF hunk is the description-block scoping rewrite. No
`_F29` line differs staged-vs-built anywhere (check 7e, re-run green).

### (c) Stale-count sweep — CLEAN

Counts reproduced on disk by my own counts (not the manifest's):
67 skills / 45 agents / 48 rules / 55 commands (directory listings),
15 hooks (`hooks/hooks.json`, 15 events), 49 trigger keys
(`manifests/context-packs/skill-triggers@1.json`, 49 keys, 252 phrases).
Base pattern (`spawn|subagent|sub-agent|Task tool|delegate|delegat|
implementer`, case-insensitive, `*.md`/`*.mdc`, skills/rules/commands/
agents) reproduced with the corrected invocation
`grep -r -a -n -i -E`: **168 matching lines in 49 files**; whole-tree
170 lines / 50 files (the +2 are the README documentation hits).
Methodology note: my first grep with the task brief's shorter pattern
(`spawn|dispatch|subagent|Task tool|delegate|implementer`) returned
286 lines / 60 files — a different pattern, not drift; the auditors'
pattern above is the one that reproduces 168/49, and it agrees with
the per-file counts in #94-A (orchestrate 40, feature-expansion 26,
impeccable-critique 11, dispatch-prompt 7 — spot-checked via the same
grep). Zero occurrences in the built tree (excl. `node_modules`) of
"123 rules", "121 rules", "166 skills", "72 agents", "87 commands",
"66 skills", "60 commands". The stock-ECC line "144 skills, 69 agents,
121 rules, 94 commands" is present at `README.md:11` — upstream stock
text, not our counts, correctly not counted as a failure. `verify29.py`
re-run: **315/315, exit 0** (see (g)).

### (d) Dangling-reference sweep — CLEAN

Own path-reference extraction from the five routing-relevant files
(`skills|agents|commands|rules|references/`-prefixed paths, resolved
relative to each file's own directory):

- `dispatch-prompt.md`: 1 path ref
  (`skills/orchestrate/references/design-inventory.md`) — resolves.
- `orch-pipeline/SKILL.md`: 7 path refs (3 agents, 3 common-*.mdc
  rules, `skills/orchestrate/references/dispatch-prompt.md`) — all
  resolve.
- `gan-style-harness/SKILL.md`: 2 path refs (`commands/gan-build.md`,
  `skills/orchestrate/references/dispatch-prompt.md`) — both resolve.
- `redesign.md`: 0 bare path refs — the file itself is reached via the
  DTF SKILL.md:455 pointer
  (`references/hallmark/references/redesign.md`), which resolves to the
  file swept above.
- `orchestrate/SKILL.md`: 18 path refs — the 5 `references/*` entries
  resolve under `skills/orchestrate/` (verified by `ls`:
  agent-TEMPLATE.md, design-benchmark-v5.md, design-inventory.md,
  dispatch-prompt.md, patterns.md all present); all others resolve
  from the tree root (agents, commands/demo.md, the four Hallmark
  references files + sloplint.mjs, git-workflow, hackathon-scope).
- GAN GENERATE block's `spec.md` reference is real: the planner writes
  per-feature acceptance criteria into `gan-harness/spec.md`
  (`agents/ecc-gan-planner.md:29`, `:108`); `gan-build.md:9/:28/:30`
  reads the same path. `gan-harness/spec.md` is a project-runtime file,
  not a plugin-tree file — correct as referenced.
- Call map: the built tree's `skills/orchestrate/references/call-map.md`
  md5 is `b066413a1a7dd6efcd8571c8abf93942`, exactly the fix28 value
  recorded in the manifest — the map was restored byte-identical after
  the regeneration check, as claimed. Its `astra-review` / `react-build`
  / `gan-build` / `gan-design` mentions name real commands.
- No tree file is newer than `fix29/build-log-run12.txt` (own `find
  -newer` — empty), so no post-build drift.

### (e) README consistency — CLEAN

Every count the README states about the plugin reads 67 skills / 45
agents / 48 rules / 55 commands (line 13: "67 skills, 45 agents, 48
rules, and 55 commands in total (42 agents as-shipped + 3 staged
orchestrate agents; 46 rules as-shipped + 2 new rules — `hackathon-mode`,
`ponytail` …)"; lines 36, 38, 40 use 67 skills / 45 agents / 55 commands
consistently). No `_F29` token or "Factory routing" note appears in the
README — correct per the manifest: unlike fix #27/#28, all 7 tokens
live in skill/rule text in the built tree, so no README provenance note
is needed. No inconsistency found.

### (f) SPEC §6 criterion cross-check — MIXED, honestly: sweep MET, full section NOT MET as written (dry-run outstanding)

Numbering note (as in #37): **SPEC.md has no section numbered §6.**
Its headers are Goal, Rules / mechanisms, Honest limits, Scope,
Verification — no numbered sections at all. The task brief's "SPEC §6"
does not exist as written. The closest text is the **Verification**
section, whose criteria are: audit loop (at least 2 rounds) + sweep +
dry-run, with HONEST verdicts. Evaluated against the tree / verifier /
audit record:

- **Audit loop: MET.** 15 rounds (#80–#94), closed with final round
  #94 PASS on both halves (0 blocking, 0 minor). I read the #94-A and
  #94-B verdict lines directly ("Verdict: PASS — 0 blocking, 0 minor"
  in both reports); both auditors independently re-ran verify29.py at
  315/315.
- **Sweep: MET.** This sweep is CLEAN (0 blocking, 0 minor), with
  weaving coherence CLEAN for the whole tree (see (a)).
- **Dry-run: NOT YET RUN.** Manifest status line: "Next: sweep #38,
  then dry-run #44". No dry-run #44 record exists in `fix29/`.
  The SPEC also requires the dry-run to include a factory leg (queue
  of independent tasks dispatched through slots with retire-and-refill,
  verifying partitioning, brief completeness, no-guessing, and
  orchestrator merge/verification) — that leg cannot be verified until
  the dry-run runs.
- **Overall Verification section as written: NOT MET yet** — solely
  because the dry-run is outstanding. That is the expected pre-dry-run
  state, not a defect in the tree: nothing in the tree blocks the
  dry-run, and no fix #29 content depends on it having run. Per the
  fix #27 convention, I record NOT MET as written rather than
  stretching the section to fit the sweep alone.

### (g) Verifier runs — my own re-runs

- **`verify29.py`, re-run by me: 315/315 checks pass, exit 0.**
  (Tail: "PASS CUT-name sweep: zero live dispatches to CUT
  skills/agents/commands (check-12 allow-list only)", "PASS check 12b:
  no imperative dispatch to a CUT skill/agent/command hides in an
  allow-listed line", "315/315 checks pass".) The 315 total is the
  verifier's own count (210 top-level `check(` calls, the rest from
  loop-registered checks such as 7d(b)); I report the run's own
  "315/315", not a recount of call sites.
- **Build log run 12** (`fix29/build-log-run12.txt`, read): ends "build
  complete", counts 67/45/48/55/15, "fix29: 33 change(s)", "fix29: OK".
- **`fix29.py` md5 == template**: `fbd459c7eb72a643fe985d321282d141`
  for both, matching the manifest's recorded value.
- **Model pins unchanged:** zero `deepseek-`/`qwen-` slugs in the
  built tree outside the pre-existing `manifests/pi-core.json:243`
  `deepseek-harness-setup` entry (provider-config key, pre-existing)
  and the three allow-listed icon-data files; DeepSeek/Qwen names occur
  only on the two GLOBAL-ROUTING lines (one of each per block), per
  verify29 check 9b, which passed in my re-run. One scoping precision,
  not a finding: 9b's grep scope is skills/agents/commands/rules/hooks/
  README.md, so `scripts/lib/install/content-transform.js:4` (a
  pre-existing code comment mentioning "Qwen/Antigravity/Copilot" as
  transform targets) and `manifests/pi-core.json` sit outside 9b by
  design. Neither is a model assignment; both are pre-existing
  non-routing text. (A binary `.webp` under DTF assets also matches a
  case-insensitive "qwen" grep — image bytes, not a reference.)

### (h) Carried observations — both still stand as recorded

- **F35 fragility (hackathon-mode block move caught only via check-12
  collateral): CONFIRMED still standing.** The GLOBAL-ROUTING block
  sits at `rules/hackathon-mode.mdc:45`; the file carries exactly one
  `_F29` line, so check 7e is vacuous for it; `ALLOW_NAMES:47` in
  verify29.py sits directly below the block (the `intent-driven-
  development` / `product-lens` allow-list). A block move to EOF would
  shift line 47 → 46 and fail only via the check-12 collateral, exactly
  as #92-B/#93-B/#94-B recorded. The gap has NOT opened; the mechanism
  still holds. Not a finding: the verifier does fail the mutation as
  written, and the block is a self-contained rule statement whose
  meaning does not depend on its neighbours.
- **F-O scope note (agents/fast-worker.md:16 unasserted, pre-existing
  ECC text): CONFIRMED still standing.** Line 16 reads "If a real
  **design decision** surfaces, or the spec is ambiguous enough that
  you'd have to guess at intent, **stop and return that** — do not
  invent an answer." — pre-existing ECC role text, already the bound
  form. `verify29.py` contains zero mentions of the string
  `fast-worker.md` (5 mentions of `fast-worker` are the tier name in
  other checks). The fix #29 coverage for this behavior is the
  dispatch-prompt preamble check (N10 adjudication), not this file.
  Not a finding, not a fix #29 regression path.
- **Related, confirmed not a finding:** `agents/ecc-gan-planner.md`
  carries zero `_F29` tokens, but its re-routed fallback is present
  verbatim at :44 ("STOP and return NEEDS_CONTEXT naming the missing
  direction to the orchestrator instead of invoking the design-lead
  itself") and asserted by verify29's scoped 92-B4 check
  (verify29.py:1777–1779, Direction-source line). The manifest §2(b)
  record never required a token at this site, and 15 audit rounds
  verified it as written. No action.
- **Manifest bookkeeping, not a tree item:** MANIFEST.md §4 (SPEC §6
  criterion statuses) and §5 (open parent adjudications) still read
  "(to be filled)". That is coordinator paperwork for after the sweep
  and dry-run, not a defect in the built tree. The §6 statuses in §4
  should record the (f) verdict above once the parent adjudicates it.

### Other

- No file was edited, created, or deleted except this report.
  `build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing was
  committed, pushed, or messaged.
