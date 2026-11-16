# Fix #27 SPEC — Debloat to a lean winning-build plugin, loosen the theme cage, always-lead orchestration, usage cuts, and the missing weekend rules

## §0 Origin

Anish, Nov 15, ~11:54 PM CST (after the AISFS × Merck hackathon closed):
"update the hackathon-skills repo to match [everything this weekend]... there
is a skill called bengali something that makes bengali writing easier to
understand, we dont need that or other stuff like that at all, let's try to
minimize usage, cut unneeded skills, add skills that we DO need based off of
this weekend, the biggest thing is visual quality and mindblowing renders for
it and designs and everything, the themes were constricting, let it be
creative within the thinking method confines of the skills, and also help
reduce overall usage by making sure the orchestration model is always used
and not only after the first prompt and stuff like that. do that, run a full
audit of our work this weekend and update the hackathon skill as needed,
debloat and everything, and then run the audit loop on the repo."

Anish, Nov 16, ~00:10 CST (addition to the scope): "Make the design skill
package an AUTOMATIC link every time ANY design decision is made... every
design decision (layout, color, type, spacing, motion, component choice,
hierarchy, any visual call) must route through the design package
automatically, not only when explicitly invoked... a single design
intelligence threading every decision, so the whole build feels like one
coherent vision."

Baseline: build.sh 24,088 lines, md5
`e1944a6e2b81bf3b869c191633c04aae` (post-fix #26). Counts: 166 skills /
72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys.

Evidence base (read before implementing): `fix27/skill-inventory.md`
(all 166 skills, KEEP 64 / CUT 91 / REVIEW 11) and
`fix27/weekend-audit.md` (theme cage, orchestration gates, usage waste,
missing rules — all with file:line anchors to the shipped tree). Staged
sources are the edit source for staged skills; ECC/marketplace/MIT-origin
files are patched at build time by `fix27/fix27.py` (same pattern as
`fix26/fix26.py`). Never re-run `fix11/fix11-stage.py`. Never edit the
built tree directly.

## §1 Skill debloat — 166 → 65 skills

### §1(a) The cut (100 skills)

The 91 CUT skills from `fix27/skill-inventory.md` §"CUT list" PLUS the
10 REVIEW adjudications below, MINUS `gan-style-harness` (KEPT — see
below). The inventory's CUT list is authoritative; do not re-litigate
its rows — each has a stack-fit or duplication reason.

REVIEW adjudications (coordinator-made, from the inventory's settle notes):
- `growth-log` — **KEEP**. `delivery-gate` enforces it: its hook blocks a
  complex task when growth-log is stale
  (`skills/delivery-gate/hooks/quality-gate.py:220-222`), and
  `delivery-gate/SKILL.md:29,97` states the blocking condition. Cutting it
  would break the gate's learning-capture enforcement. It is the only
  REVIEW item kept.
- `agent-introspection-debugging` — CUT (meta diagnosis of failed agent
  runs, not building).
- `brainstorming` — CUT (grill-me + feature-expansion already cover
  ideation; no separate user-facing ideation step is wanted).
- `bun-runtime` — CUT (npm/pnpm is the supported path).
- `coding-standards` — CUT (typescript-patterns + python-patterns cover
  the stack; no framework-neutral fallback is wanted).
- `continuous-learning-v2` — CUT (meta-learning; ck + growth-log cover
  memory).
- `database-migrations` — CUT (app-scaffold/Supabase own migrations;
  postgres-patterns kept for schema work).
- `intent-driven-development` — CUT (grill-me/hackathon-scope cover
  scoping).
- `mcp-server-patterns` — CUT (no MCP-server track is targeted).
- `prisma-patterns` — CUT (Supabase client is the data path).
- `redis-patterns` — CUT (no Redis need in weekend builds).

**`gan-style-harness` — KEPT (coordinator adjudication, overturning
the inventory's CUT row).** The inventory cut it as duplicating "the
orch-build-mvp / orchestrate generator-evaluator loop" — but the
dispatch evidence shows the opposite: orch-build-mvp's inner loop IS
/gan-build (orch-build-mvp/SKILL.md :39, :62, :95; orch-pipeline :37,
:97; commands/orch-build-mvp.md:31). The GAN harness is the loop, not a
duplicate of it. Cutting it would break a KEPT skill's core mechanism.
Its 3 agents (ecc-gan-evaluator/generator/planner) and 2 commands
(gan-build, gan-design) are likewise KEPT.

Result: **66 skills kept** (64 KEEP + growth-log + gan-style-harness).
Skills go from 166 to 66 (60% smaller).

### §1(b) Mechanism — build-time removal in fix27.py

Do NOT delete the skills from build.sh STEP 2 (the STEP 3 patches assume
the full tree — their anchors live in the skills being cut, and deleting
up-front would break the build). Instead `fix27/fix27.py`, invoked by
build.sh after fix26 and before STEP 5 Counts (same pattern as
fix24/25/26), removes the 101 skill dirs from the built tree, then:
- removes the companion agents whose sole skill is CUT (27 total: the
  17 found by the inventory worker — bengali, csharp, django x2, flutter,
  fsharp, kotlin x2, opensource x3, rust x2, vue — PLUS the 13 from the
  coordinator's OWED-8 adjudication: conversation-analyzer, cpp x2, dart,
  go x2, java x2, php, ruby, swift x2, marketing-agent — whose only
  language skills are CUT (or absent) and whose only referrers are
  dropped commands or the call map. KEPT: ecc-a11y-architect (serves
  kept frontend-a11y) and the 3 gan agents (gan-style-harness is KEPT));
- drops commands whose sole target is a CUT skill/agent (27 total: the
  18 verified by the inventory worker PLUS cpp-build, cpp-review,
  cpp-test, go-build, go-review, go-test, gradle-build, evolve,
  instinct-export, instinct-import, instinct-status — each verified by
  reading the command file. HELD (not dropped): learn, learn-eval,
  project-init — learn/learn-eval are skill-creation workflows, not
  continuous-learning-v2 commands, and project-init takes --skills as a
  parameter; recorded as OWED for the audit to adjudicate. KEPT:
  gan-build, gan-design (gan stays));
- prunes `manifests/context-packs/skill-triggers@1.json` entries whose
  skill is CUT (the table is DOCUMENTATION-ONLY per fix #26 B6, but it
  must not route to removed skills; record the pruned key count — 15
  keys, 64 → 49);
- updates the STEP 4 README count lines in the built tree to the new
  counts (skills 66, agents 45, rules 123, commands 60);
- shrinks the deferred check lists to the three kept checks
  (verification-loop, production-audit, delivery-gate) in orchestrate
  (:8, :103, :370) and orch-build-mvp (:86) — codehealth-mcp,
  santa-method and security-scan are CUT. (hackathon-mode.mdc §3 carries
  the same list in staged sources — the staged-edits worker owns it.)
- patches the one dangling soft pointer the cut creates:
  `skills/delivery-gate/SKILL.md:97` "pair with `agent-self-evaluation`"
  (agent-self-evaluation is CUT) — reword to pair with a manual review of
  the recorded entries. Any other dispatch reference to a CUT skill found
  by grepping the KEPT tree is patched the same way (route to the kept
  equivalent, or remove the line) and recorded; a reference that is prose
  history (not a dispatch) is left alone and noted.

### §1(c) Call map

The call map (`skills/orchestrate/references/call-map.md`, staged) lists
166 skills. Regenerate it from the REDUCED tree with the fix25 generator
(`fix25/callmap/generate_call_map.py`) using the prescribed copy-aside →
run → diff → restore procedure (fix26 MANIFEST §2, generator incident:
the generator takes no output argument and rewrites the staged file in
place; never probe it with `--help`). If the generator cannot produce a
clean reduced map, record the call map as OWED in the manifest with the
exact failure — do not hand-edit 100+ rows, do not ship a map that lists
removed skills.

### §1(d) What is NOT cut in this fix

- **Rules (123) are NOT cut.** The per-language rule families for cut
  languages (~80 files) are a follow-up debloat candidate, recorded as an
  open parent adjudication in the manifest. Rationale: rules are
  file-scoped (they load only when their language is used), so they are
  not the usage lever the skills are; cutting them would also touch
  STEP 3 rule patches. The skill cut is the usage lever.
- `context-budget` is KEPT (uncalled, deliberately — it is the live usage
  meter behind the usage-burn complaint).
- `codebase-memory` is CUT (fresh weekend builds have no large unfamiliar
  codebase to query) — note the MCP server `codebase-memory` in mcp.json
  stays; only the skill goes. If the sweep flags the MCP/skill split,
  record it; do not re-add the skill.

## §2 Themes — starting point, not cage (P0)

Per `fix27/weekend-audit.md` claim 1. The theme deal stays (it runs first
and supplies tokens/material), but it stops being a ceiling. Edits in
staged sources (`new-skills/design-taste-frontend/SKILL.md`,
`new-skills/orchestrate/SKILL.md`):

- design-taste-frontend `:256-262` — demote the theme deal from "the
  direction" to "the starting point": add "The dealt theme is the
  starting point, not the cage. The design-lead may depart from the
  theme's material where the brief's job demands it, recording the
  departure as a D19-reasoned decision (what was departed from, why the
  job needs it)."
- design-taste-frontend `:423` — delete or invert the "NOT within reason:
  a new theme (re-deal instead…)" line so inventing a theme direction is
  a recorded D19 decision, not a forbidden move.
- design-taste-frontend `:262` — widen the genre map: add genres for
  ops/technical-tooling, data/video-pipeline, and scientific domains (or
  drop the map and let the deal take the brief's domain words directly).
  At minimum, stop defaulting everything unlisted to `editorial`.
- orchestrate `:137` + design-taste-frontend `:423` — relax bound (2)
  from "fit the theme's material world" to "fit the theme's material
  world **or a recorded departure from it** (D19 reason required)".
- orchestrate `:127` (row 10) — give dashboards/apps a dealt moment too:
  "dashboard/app surfaces also record a hero-moment line for their home
  surface (the moment, not a marketing hero)" so the HERO-BQA/MEMORABLE
  bars have something to judge on non-landing builds.
- Keep untouched: D19, the design package, "more, not bolder", the
  anti-derivative rule, the Hallmark floor (it stays a floor).

## §3 Orchestration — always-lead (P0)

Per `fix27/weekend-audit.md` claim 2. Grok 4.7 High leads every run, not
only the first build. Edits in staged `new-skills/orchestrate/SKILL.md`
and `new-rules/hackathon-mode.mdc`:

- `:14` — delete the "The mechanics work under any lead model and any
  effort setting the user has chosen" hedge; state the pin as binding:
  "The orchestrator runs on Grok 4.7 High. If the session is not on
  Grok 4.7 High, say so in the first reply and proceed only as the
  fallback the user accepts — never silently."
- `:89` (step 4) — add a pin check at step 0: the orchestrator states
  the model it is running on in the first reply / run ledger
  (`MODEL-PIN: grok-4.7-high | other: <name>`). A pin that cannot be
  verified is recorded as unverified, not assumed held. Flag in the
  manifest that Cursor-side enforcement would need a plugin-level model
  default, not more prose — skill text cannot enforce the pin.
- `:50-56` + hackathon-mode.mdc §6 — extend orchestrate's remit:
  "orchestrate leads every multi-piece run for the life of the project,
  not only the first build; the first-build sequence (grill → scope →
  expansion → build) applies to the first build, and the routing table +
  verification stage apply to every later run." Route post-first-build
  multi-piece work back to orchestrate instead of leaving it in the main
  context by default (`:109`).
- call-map.md:38 (B6) — the DOCUMENTATION-ONLY trigger router stays as
  fix #26 decided; for this fix, at minimum add the grill-me trigger
  phrases to hackathon-mode.mdc §1 itself so the alwaysApply rule fires
  on a bare first prompt, not only on "grill me".

## §4 Usage cuts (P0–P1)

Per `fix27/weekend-audit.md` claim 3. All edits in staged
`new-skills/orchestrate/SKILL.md` unless noted.

### §4(a) W1 — reconcile the implementer-model contradiction (P0, largest lever)

`:89` says slice-builder implementers spawn on `grok-4.7-high`; `:30`
and `:129` say "no execution a 4.6 worker could do runs on the 4.7
mind". Decide option (a): define the implementer tier as
`cursor-grok-4.6-high-fast` for fully-specified slices (4.7 only where
the slice still contains a design decision — design-lead work stays
4.7), and change `:89` accordingly. Do NOT leave both texts live. The
roster (`:22-28`) gains an explicit "implementation tier" row so the
contradiction cannot re-form.

### §4(b) W2 — gate the blind-parallel second deep-reasoner pass (P1)

`:18,117,278,282` — single deep-reasoner pass by default; second pass
only when the first pass flags genuine uncertainty or when two genuinely
different priors exist (the row-8 case, `:121`). Record the skipped
second pass in the ledger.

### §4(c) W3 — cap the verification layers (P1)

- Per-wave reviewers (`:96,261-268`): step 2/4a reviewers run per wave
  only while waves are large; small waves get the step-1 cheap check
  only (`:260` already allows this — make it the default, reviewer the
  exception).
- Merge the hero review and finish review into ONE fresh-context review
  when both apply (design-taste-frontend `:537` + orchestrate `:272`).
- Single capture run: polish-pass captures once, browser-qa consumes
  those captures and shoots only what the matrix lacks
  (`round2-skills/polish-pass/SKILL.md:112`,
  `skills/browser-qa/SKILL.md` Phase 3 — build-time patch via fix27.py,
  browser-qa is ECC-origin).
- Cap the beat-v5 re-deal loop (`:96`): at most 2 re-deals/redesigns;
  after that the trailing dimension is recorded as owed with its cause
  (which is also the ceiling flag — §5(a)).
- Do not re-run expansion Phases 0–3 after the first build except on
  explicit ask (`new-skills/feature-expansion/SKILL.md:161` trigger).

### §4(d) W4 — bound the record-keeping (P2)

`:66,68` — USED-vs-REJECTED only for inventory entries actually
considered for this build; untouched sections record one line
("not considered — <reason>").

## §5 The missing weekend rules (P0–P1)

### §5(a) LOCK-IN — flag the quality/score ceiling when knowable (P0, new rule)

Belongs in `rewritten-skills/hackathon-scope/SKILL.md` + a `CEILING`
line in orchestrate step 6 (staged). Text:

> **LOCK-IN (ceiling flag).** The moment the achievable quality/score
> ceiling is knowable — at scoping (weak rubric match, missing hard
> substance, a core flow with no real algorithm/data), at expansion
> (planner feasibility ≤ the floor), or mid-build (a cut that lowers the
> ceiling) — state it to the user immediately, in the reply, not only in
> a doc: what the ceiling is, what sets it, and what would raise it.
> Never let the user discover a low ceiling the night it is due. The
> ceiling line is re-stated in every final report
> (`Ceiling: <level> — set by <cause> — raising it needs <change>`).
> A ceiling flag is a message, not a blocking question — the build
> continues on the best honest path unless the user redirects.

### §5(b) DELIVERABLE-AT-RISK — say so immediately, let the user decide (P0, new rule + §7 carve-out)

Belongs in `new-rules/hackathon-mode.mdc` §7 + orchestrate step 6
(staged). This rule CONFLICTS with §7's "do not ask the user anything"
as written — resolve the conflict explicitly in the same edit:

> **DELIVERABLE-AT-RISK (second sanctioned prompt).** If a deliverable
> cannot be met as specified — a required feature, a submission artifact,
> a spec-mandated number or format — flag it to the user immediately, in
> the reply, with the three options: (a) best honest framing (ship what
> exists, stated plainly), (b) try our best (attempt it with the
> shortfall named), (c) a workaround (a substitute that meets the
> intent). The flag is a message, not a gate: unless the user replies,
> proceed on (b) — try our best with the shortfall named — and record
> the flag + the default taken in the run ledger and the final report.
> Never silently drop a deliverable, never silently substitute an easier
> version (see also "No silent re-scope",
> `skills/hackathon-scope/SKILL.md:67`), and never present the easy
> version as the hard one.

Add to §7: "The deliverable-at-risk flag is the second sanctioned user
prompt during the first build, alongside the narration-key prompt. It
never blocks the build."

### §5(c) CHECK-THE-SOURCE + AUDIT-AS-GUIDE + exact verified numbers (P1, new rules)

Belongs in orchestrate step 6 (final report) + hackathon-scope +
`skills/hackathon-pitch/SKILL.md` (MIT-origin — build-time patch via
fix27.py). Text:

> **CHECK-THE-SOURCE.** Every scoring, timing, or logistics claim in a
> final report, reply, or deliverable prompt cites the source document
> it was read from (spec section, invite, rubric) with the value as
> written there. An estimate is labelled an estimate with its basis; a
> measured value replaces the estimate in the record the moment it is
> measured. Never restate a remembered number as a fact. Final-report
> checklist line: "Scoring/timing/logistics claims — source cited per
> claim, or the claim is removed."
>
> **AUDIT-AS-GUIDE.** An audit (sloplint, reviewer, or any checklist
> pass) is a guide, never the source. The source is the spec / the
> rendered screen / the measured run. Where an audit and the source
> disagree, the source wins and the disagreement is recorded. Every
> number in a deliverable prompt or submission cites the exact spec
> section and uses only exact verified numbers — no rounded, remembered,
> or inferred figures.
>
> **DURATION-MEASUREMENT.** Replace every estimate with the measured
> value the moment it is measured; the record never keeps a superseded
> estimate. (P2, in hackathon-scope.)

### §5(d) "Test passage is not browser verification" (P1, one-liner)

Add a row to `skills/verification-before-completion/SKILL.md` claim
table (marketplace-origin — build-time patch via fix27.py): "UI verified
| browser-qa verdict on the rendered screen | test suite passing,
screenshots described but not inspected, agent report". And to
orchestrate `:270` (Verify step 5, staged): "Test passage is not a
screen verdict; a green suite never substitutes for the visual loop."

### §5(e) No `Co-authored-by: Cursor` trailer (P1, new rule — currently nowhere in the plugin)

Add to `rules/common-git-workflow.mdc` (ECC-origin — build-time patch
via fix27.py): "Commit messages carry no `Co-authored-by:` trailer for
any AI tool (including Cursor) and name no AI tool as author or
contributor. The commit author is the user." Add it to the orchestrate
step-6 static check list so the audit fails a commit carrying the
trailer.

### §5(f) Grill-me holes (P1)

- orchestrate `:54` (staged): add "If the check finds no record and no
  explicit skip, that is itself a finding: state in the first reply that
  grill-me did not run and why (no trigger / no record), and ask the user
  whether to grill now (one prompt) or proceed — the one-question
  exception to §7. Do not silently proceed on a raw prompt."
- Record header: the decision record's header must carry
  `grill-me: RAN | SKIPPED (user said "<phrase>") | MISSED (no trigger)`
  — grill-me step 5 writes RAN; hackathon-scope writes SKIPPED/MISSED
  (staged `new-skills/grill-me/SKILL.md` + `rewritten-skills/hackathon-scope/SKILL.md`).

## §6 DESIGNPKG-AUTO — the design package is the automatic routing for ALL design decisions (P0, new user requirement Nov 16)

The design package (Taste / design-taste-frontend, ui-ux-pro-max,
less-flat-ui, Hallmark, Impeccable via polish-pass, Harmony, motion-*,
design-system) is already invoked for UI/UX surfaces (orchestrate row
10, step-3 "Design package in every UI slice brief"). It is NOT
consistently invoked for every design decision. This section makes it
automatic.

Definition: a **design decision** is any call about layout, color, type,
spacing, motion, component choice, hierarchy, visual state, or any visual
call, wherever it arises — UI slice, demo-video template, docs/diagrams,
dashboard, component, pitch visual, any rendered surface.

Rule text (added to staged `new-skills/orchestrate/SKILL.md` next to
BIND `:32`, and to `new-rules/hackathon-mode.mdc` §6):

> **DESIGNPKG-AUTO.** Every design decision routes through the design
> package automatically. The named skill for a design decision is always
> a design-package skill (design-taste-frontend / ui-ux-pro-max /
> less-flat-ui / polish-pass / motion-foundations / motion-patterns /
> motion-advanced / make-interfaces-feel-better / design-system, with
> the design-lead deciding which leads). A design decision with no
> package skill named in its brief/directive is off-skill improvisation
> and fails the audit. The design-lead (Taste, grok-4.7-high) decides
> the direction; the theme deal is the starting point (see §2), not the
> cage. This is the design half of BIND: BIND says every decision routes
> through a named skill; DESIGNPKG-AUTO says a design decision's named
> skill is always a package skill.

Concretely: extend the step-3 "Design package in every UI slice brief"
rule to "Design package in every brief that contains a design decision"
— including non-UI slices that make a visual call, the demo-video
template, and docs/diagram work. The orchestrator does not wait for a UI
surface to invoke the package; the package is linked the moment a design
decision exists. Directives keep carrying exact values + D19 reasons
(DIRECTIVES_F22, unchanged).

Audit-loop check: verify27.py asserts the `DESIGNPKG-AUTO` token exists
in staged orchestrate, staged hackathon-mode.mdc, and the built tree;
the sweep's weaving pass checks that the plugin's own design artifacts
obey the rule — every design-inventory entry names its owning package
skill (it already does — "grouped by owning skill"), and any design
decision recorded in the repo's own docs (design-inventory,
design-benchmark, render decision records) cites a package skill. A
design decision in the plugin's own artifacts with no package skill
named is a sweep finding.

## §7 Verification criteria

- Audit #74 (or next number): ZERO blocking, ZERO minor. Standalone
  report file in `fix27/` (per the AGENTS.md record-keeping rule).
- Sweep #35 (or next number): CLEAN, weaving-coherence CLEAN for the
  whole tree. Standalone report file in `fix27/`.
- Dry-run #42 (or next number): PASS — Leg 1 fixtures, Leg 2 render
  re-run, Leg 3 /demo, Leg 4 Cursor-readiness, Leg 5 call-graph.
- verify27.py: checks for every placement, exit 0. It also codifies the
  prior-verifier tails after this fix (the skill cut moves counts: skills
  166 → 66, agents 72 → 45, commands 87 → 60, triggers 64 → 49 — exact
  numbers measured by the build, not assumed; record any move with its
  cause traced to the files).
- Prior verifiers: re-run; fails must be only the codified tails (the
  count moves from §1 + the README count updates). No regressions. The
  ONLY verifier edit authorized in this fix is updating a verifier's
  additions-only diff invariant in the same change as the build.sh
  comment it describes, per the fix #25/§3 precedent — and only if such
  a comment is actually edited.
- Banned terms: 0 in the built tree (same list as fix #26). Grok pins
  only: `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- Counts: skills 66, agents 45, rules 123 (unchanged), commands 60,
  hooks 15 (unchanged); trigger keys reduced by the §1(b) prune (64 →
  49). Anchor tokens: new `_F27` family
  (`DESIGNPKG-AUTO_F27`, `CEILING_F27`, `DELRISK_F27`, `CHECKSRC_F27`,
  `AUDITGUIDE_F27`, `NOCOAUTHOR_F27`, `THEME-START_F27`, `ALWAYSLEAD_F27`,
  `IMPL46_F27`, `GRILLHDR_F27`, `DEFER3_F27`) — census reconciles staged + built.
- Manifest: fix27/MANIFEST.md, with the disposition table, the anchor
  tokens, the open parent adjudications, and the dry-run caveat if any
  check is environment-limited.
- Builds use the fix #26 env-redirected invocation (TMPDIR / UIPRO_DIR /
  MS_DIR / SKILL_SRC to disk; ECC_REPO stays hardcoded to
  `/tmp/ecc-repo-clean` — see fix26/build-log-run3.txt for the exact
  invocation; `fetch_repo` re-clones from GitHub if /tmp was wiped).
  Never re-run fix11/fix11-stage.py. Staged sources only, never the
  built tree. build.sh is the source of truth.

## §8 Non-goals

- Do not re-litigate fixes #14–#26 adjudications (C2/C3 scope splits,
  FILM_F1/F5/F6, /demo gates, Casberry bar, APCA informational, THE
  CORE, the inventory, the call map, epic-commands reachability, the B6
  documentation-only disposition, benchmark Dim 7 owed, Netlify row
  touch-up due after Dec 4, 2026).
- Do not rewrite frozen verifier-asserted texts — except the one
  authorized §7 update, and only that.
- Do not cut rules in this fix (§1(d)) — record as an open adjudication.
- Do not pre-decide the smoke test's live questions. Do not build a
  Campus Eats render. Do not add a live-render requirement anywhere.
- No new skill, command, rule, agent, hook, or trigger unless the
  manifest justifies it — the §5/§6 rules are edits to existing skills
  and rules, not new skills. (If an implementer finds a genuinely new
  skill is needed, that is a parent decision, not an implementer call.)
- No bundle, no commit, no push by the fix workers — the coordinator
  handles the push after the loops are clean.
