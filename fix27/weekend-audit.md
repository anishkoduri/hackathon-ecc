# Fix #27 — Weekend Audit (Nov 14–15, 2026 builds)

**Scope:** read-only audit of the shipped plugin tree
`~/workspace/hackathon-plugin/hackathon-ecc/` against the user's weekend
feedback. Staged sources checked where they differ:
`new-skills/`, `round2-skills/`, `rewritten-skills/`, `new-rules/`.
Staged-vs-shipped diffs are trivial (orchestrate `SKILL.md` 389 lines both,
differing only in agent-file references, e.g. L96/L261/L268 naming
`agents/ecc-code-reviewer.md`; design-taste-frontend 637 staged vs 638
shipped lines) — all anchors below are to the **shipped** tree unless marked
"staged".

**Method:** read the listed skills in full (or their operative lines where
lines run to several KB), grepped the built tree for the theme list,
orchestration gating, and the claim 4–6 rules. A claim is marked ENCODED only
where the shipped skill text actually states it; "closest existing text" is
quoted so the implementer can see the gap precisely.

**Headline:** the theme cage, the orchestration gate, and the biggest usage
burn are all real and all locatable. Verification's *screen-verdict*
monopoly is well encoded; its *check-the-source* half is entirely missing.
The lock-in rule and the immediate-deliverable rule are both missing, and the
immediate-deliverable rule currently **conflicts** with hackathon-mode §7's
no-questions rule. The no-`Co-authored-by: Cursor` rule is nowhere in the
plugin text at all.

---

## Claim 1 — VISUAL QUALITY / THEME CAGE: CONFIRMED, mechanism found

### Where the theme list lives

Not in `frontend-design-direction` — that skill explicitly forbids hackathon
use (`skills/frontend-design-direction/SKILL.md:8-10`, frontmatter description:
"in a hackathon project, do NOT use this skill for UI work") and contains no
theme list. The list lives in **Hallmark inside design-taste-frontend**:

- `skills/orchestrate/references/design-inventory.md:65` — "Theme catalog —
  50 themes | Fifty dealt themes (almanac, arcade, atelier, bloom, blueprint,
  broadside, brutal, carnival, cobalt, console, coral, darkroom, dose, dusk,
  editorial, …)" and `:159` (same catalog in the §10 summary table).
- `skills/design-taste-frontend/references/hallmark/references/themes/` —
  50 theme files + `index.json` (cited at inventory `:65`).
- `skills/design-taste-frontend/SKILL.md:259` — the deal command:
  `node <skill>/references/hallmark/scripts/theme.mjs deal --genre <genre>
  --prompt "<the brief>" --log .hallmark/log.json`.
- `skills/design-taste-frontend/SKILL.md:262` — the deal returns **3 themes**
  from the 50-theme catalog; pick the one whose material can carry the brief;
  the deal reads the recent 3 log entries to avoid re-dealing recent themes.
- `skills/orchestrate/SKILL.md:66` — the inventory (including the 50-theme
  catalog) must be read FIRST, before deciding anything.

### How the cage works (six interlocking constraints)

1. **Direction must come from the deal.** `skills/orchestrate/SKILL.md:169`
   ("No design based on a searched reference"): "the direction is GENERATED
   through the package skills: the Hallmark theme deal (50-theme catalog) for
   the direction, …". `skills/design-taste-frontend/SKILL.md:256`: "Deal a
   Hallmark theme for the direction first."
2. **Every slice brief mandates the dealt theme.** `skills/orchestrate/SKILL.md:62`
   (slice step) and `:127` (row 10 design-package rule): landing —
   "`design-taste-frontend` (design lead) + the dealt Hallmark theme +
   `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony".
3. **Every invented element must fit the theme's material world.**
   `skills/design-taste-frontend/SKILL.md:423` trailblazing rule, bound (2):
   "fit the theme's material world — material, tokens, palette balance,
   do-nots"; bound (4): "be theme-matched (fix #15 rule A)"; bound (6):
   "pass the Hallmark floor". Same at `skills/orchestrate/SKILL.md:137`
   (bounds (2)/(3) of the E1 push-boundaries rule).
4. **No new theme allowed — re-deal is the only escape.**
   `skills/design-taste-frontend/SKILL.md:423`: "NOT within reason: a new
   theme (re-deal instead, Taste step 4); a new palette (the T…".
5. **Genre funnel collapses 50 themes to 4 buckets.**
   `skills/design-taste-frontend/SKILL.md:262`: "tech/dark/atmospheric →
   `atmospheric`; SaaS/devtool/B2B → `modern-minimal`; playful/fun/kids/games
   → `playful`; anything else → `editorial` (default)." Both weekend builds
   (a feedlot-ops dashboard platform and a video pipeline) map to the same
   one or two genres, so the "50 themes" are effectively ~2 genres × 3 dealt
   options in practice.
6. **Hallmark floor: 16 non-waivable rules.**
   `skills/design-taste-frontend/SKILL.md:262` ("16 non-waivable rules + the
   6-axis pre-emit critique", `references/hallmark/references/hallmark-floor.md`,
   81 lines) + sloplint gates (`skills/orchestrate/SKILL.md:272`,
   `skills/design-taste-frontend/SKILL.md:529-535`) + hero/finish reviews
   (`:537` and orchestrate `:272`).

### The dashboard path is a second, quieter cage

BRDashboard is a dashboard, so row 10 does **not** give it a Hallmark theme
at all — `skills/orchestrate/SKILL.md:127`: dashboard/app surface —
"`ui-ux-pro-max` (design lead) + Impeccable via `polish-pass` + Harmony +
`less-flat-ui` where the surface is dull/flat". Its direction is generated
from inventoried catalog elements instead
(`skills/ui-ux-pro-max/SKILL.md:91`: "choose from its inventoried elements —
the direction is generated from the…"; catalogs per
`skills/orchestrate/references/design-inventory.md:159-160`: styles 89 rows,
colors 192, typography 74, icons 105, charts 25, UX-guidelines 120, motion/
GSAP presets 17, stacks 22; Impeccable detector catalog, 62 rules). Same
shape as the theme cage — pick-from-catalog — with no dealt moment and no
hero-moment line. The "generic" complaint therefore has two sources, and a
theme-only fix leaves the dashboard path untouched.

### Why this produces "generic" despite the anti-generic machinery

The plugin already demands amazing: `skills/browser-qa/SKILL.md:80`
(HERO-BQA_F23 — "a merely adequate hero FAILS F6"), `:82` (MEMORABLE_F23 —
"rule-correct but unambitious, unimpressive, or forgettable all fail"),
`:83` (BENCHMARK_V5_F25 — beat the v5 figures per dimension, "a tie on any
dimension is below the bar"), `skills/orchestrate/SKILL.md:137` /
`skills/design-taste-frontend/SKILL.md:423` (E1 trailblazing — "a build with
no element a template would not produce has not pushed far enough"), and
orchestrate `:96` (U1 — ≥3 unique elements). So **judgment demands
amazing while generation is caged inside the dealt theme's material world**.
The gap is generation-side, not verdict-side: the design-lead may only
*extend* the theme, never leave it.

### Change proposal (claim 1)

1. `skills/design-taste-frontend/SKILL.md:256-262` — demote the theme deal
   from "the direction" to "the starting point": the deal still runs first
   and still supplies tokens/material, but add: "The dealt theme is the
   starting point, not the cage. The design-lead may depart from the theme's
   material where the brief's job demands it, recording the departure as a
   D19-reasoned decision (what was departed from, why the job needs it)."
   Delete or invert the `:423` "NOT within reason: a new theme (re-deal
   instead…)" line so inventing a theme direction is a recorded D19 decision,
   not a forbidden move.
2. `skills/design-taste-frontend/SKILL.md:262` — widen the genre map: add
   genres for ops/technical-tooling, data/video-pipeline, and scientific
   domains (or drop the map and let the deal take the brief's domain words
   directly). At minimum, stop defaulting everything unlisted to
   `editorial`.
3. `skills/orchestrate/SKILL.md:137` and `skills/design-taste-frontend/SKILL.md:423`
   — relax bound (2) from "fit the theme's material world" to "fit the
   theme's material world **or a recorded departure from it** (D19 reason
   required)". Keep bounds (1) serve-the-job, (3) type/space rules, (5)
   craft floor, (6) Hallmark floor, (8) anti-derivative: the Hallmark floor
   stays a floor, the theme stops being a ceiling.
4. `skills/orchestrate/SKILL.md:127` (row 10) — give dashboards/apps a
   dealt moment too: add "dashboard/app surfaces also record a hero-moment
   line for their home surface (the moment, not a marketing hero)" so the
   HERO-BQA/MEMORABLE bars have something to judge on non-landing builds.
   Keep D19, the design package, "more, not bolder"
   (`skills/orchestrate/SKILL.md:68,72,167`; `skills/browser-qa/SKILL.md:82`),
   and the anti-derivative rule (`skills/orchestrate/SKILL.md:169`) untouched.

---

## Claim 2 — ORCHESTRATION: Grok 4.7 High leads ONLY the first build, and only if the user picks it by hand

### The gating, located (three gates, not one)

**Gate A — the pin is a manual picker selection, with silent fallback.**
`skills/orchestrate/SKILL.md:14`: "Grok 4.7 High (`grok-4.7-high`,
selected in the model picker before the first build — see the picker note in
step 4)." `:89` (step 4, "Before the first build — Grok 4.7 High in the
model picker"): "Cursor's subagent model allowlist is coupled to the
model-picker dropdown, so a frontmatter pin can fail or silently fall back,
reportedly running on another model, if Grok 4.7 High is not selected in the
dropdown… or the design pin may silently fall back to another model. This is
a setup note read before building starts; it never pauses the build and never
asks the user anything mid-build. File-level pin only — the live smoke test
decides whether the pin holds". There is **no programmatic enforcement** and
no check that the pin held — the skill itself says the smoke test decides.
Worse, `:14` hedges the pin away: "The mechanics work under any lead model
and any effort setting the user has chosen — the routing rule, not the lead's
horsepower, is what keeps expensive-model spend on the work that needs it —
but the pin is Grok 4.7 High."

**Gate B — orchestrate's scope is the first build only.**
`skills/orchestrate/SKILL.md:50-56`: "Hackathon first build — sequence
(after grill-me)… One build engine per run — orchestrate IS the first-build
engine." The routing table then sends everything else elsewhere:
`:109` ("Default: do the work directly in the main context; use orchestrate
only when the user asks to orchestrate/delegate in general terms or the work
spans several pieces at once"), `:116` row 3 (single-feature/bug/change/
refactor → the `/orch-*` pipelines, "not the main context and not a fan-out
here"), `:114` row 2 (trivial work → main context), `:175` ("A slice inside
a multi-feature first build is NOT single-feature work"). `rules/hackathon-mode.mdc`
§6 confirms: "`orchestrate` owns general delegation and fan-out…
single-feature, single-bug, single-change, and single-refactor work goes to
the `/orch-*` pipelines — not to the main context and not to `orchestrate`".
So after the first build, the user is talking to the main context or an
`/orch-*` pipeline on whatever model is in the picker — Grok 4.7 is not
leading anything. The weekend's second-day work (fixes, packaging, ZIP
rebuilds, video re-renders) ran outside orchestrate's scope by design.

**Gate C — grill-me / orchestrate have no live entry points; the trigger is
documentation-only.** `skills/orchestrate/references/call-map.md:38`
(method note B6): "trigger router has no live Cursor entry point (fix #26:
DOCUMENTATION-ONLY)"; `:586`: "`skill:grill-me` … on-request
(trigger-routed; no live Cursor entry — see method note B6)". There is no
`/grill-me` command in `commands/` (and no `/orchestrate` gating to first
builds — `commands/orchestrate.md:9` just says "Show the plan first (after
grill-me and the narration-key prompt on a first build…)"). Invocation
depends on `rules/hackathon-mode.mdc` `alwaysApply: true` §1 ("run
`grill-me` FIRST…") plus trigger phrases in
`manifests/context-packs/skill-triggers@1.json:222-223` ("grill me", …).
If the alwaysApply rule does not fire on a fresh chat, nothing invokes
grill-me or orchestrate — and orchestrate `:54` then *licenses* proceeding
without it (see claim 7).

### Change proposal (claim 2)

1. `skills/orchestrate/SKILL.md:14` — delete the "works under any lead
   model" hedge; state the pin as binding: "The orchestrator runs on Grok
   4.7 High. If the session is not on Grok 4.7 High, say so in the first
   reply and proceed only as the fallback the user accepts — never silently."
2. `skills/orchestrate/SKILL.md:89` — add a pin check at step 0: the
   orchestrator states the model it is running on in the first reply / run
   ledger (`MODEL-PIN: grok-4.7-high | other: <name>`). A pin that cannot be
   verified is recorded as unverified, not assumed held. (Cannot be enforced
   in skill text alone — flag to the user that Cursor-side enforcement would
   need a plugin-level model default, not more prose.)
3. `skills/orchestrate/SKILL.md:50-56` + `rules/hackathon-mode.mdc` §6 —
   extend orchestrate's remit: "orchestrate leads every multi-piece run for
   the life of the project, not only the first build; the first-build
   sequence (grill → scope → expansion → build) applies to the first build,
   and the routing table + verification stage apply to every later run."
   Route post-first-build multi-piece work back to orchestrate instead of
   leaving it in the main context by default (`:109`).
4. `skills/orchestrate/references/call-map.md:38` (B6) — the DOCUMENTATION-ONLY
   trigger router is a known fix #26 item; for fix #27, at minimum add the
   grill-me trigger phrases to `rules/hackathon-mode.mdc` §1 itself so the
   alwaysApply rule fires on a bare first prompt, not only on "grill me".

---

## Claim 3 — USAGE: the burn is in the roster, the double pass, and the verification stack

Cursor usage hit ~2% left on Nov 15 afternoon. The plugin's own text names
the following burn sources. Ordered by likely size.

### W1 — Slice implementers run on Grok 4.7 High (biggest single item; also a contradiction)

`skills/orchestrate/SKILL.md:89`: "Slice-builder implementers spawn on the
implementation tier — model `grok-4.7-high` (slug form only)." But the roster
(`:22-28`) has **no "implementation tier"** — only you (4.7), deep-reasoner
(4.7), fast-worker (4.6-fast), scout (4.6-fast), design-lead (4.7) — and the
hierarchy rule (`:30`, fix #20 H1) says "Grok 4.7 High decides, Grok 4.6
High executes" and "no execution a 4.6 worker could do runs on the 4.7
mind", repeated at `:129` ("executors implement on Grok 4.6 High — no big
decision runs on a 4.6 worker, no execution a 4.6 worker could do runs on
the 4.7 mind"). L89 and L30/L129 directly contradict each other, and L89
is the operative line for the build waves — every slice built on the
expensive model. If the weekend's slices ran on 4.7, this alone explains a
large share of the burn.

**Fix:** reconcile in one place. Either (a) define the implementer tier as
`cursor-grok-4.6-high-fast` for fully-specified slices (4.7 only where the
slice still contains a design decision), and change `:89` accordingly; or
(b) if 4.7 implementers were deliberate, delete the "no execution on the
4.7 mind" sentence from `:30`/`:129` and record the cost explicitly. Do not
leave both texts live.

### W2 — Blind-parallel second deep-reasoner pass (2× 4.7 on high-stakes work)

`skills/orchestrate/SKILL.md:18` (second strong-tier pass), `:117` (routing
row 4: high-stakes → "two deep-reasoner passes in parallel, blind to each
other"), `:278`/`:282`: "A second pass is the same distribution, not a
decorrelated prior — so a disagreement on this path stops the run instead of
being settled", and `:282`: "it resamples the same model and tends to repeat
the same error confidently." The skill itself concedes the second pass adds
little signal for double the top-tier cost; the first-build carve-out
(`:18`, `:211`) only avoids *stopping* on disagreement, it still pays for
both passes. `:240` adds a second pass when a deep-reasoner loops.

**Fix:** gate row 4: single deep-reasoner pass by default; second pass only
when the first pass flags genuine uncertainty or when two genuinely
different priors exist (the row-8 case, `:121`). Record the skipped second
pass in the ledger. Expected saving: one 4.7 pass per high-stakes decision.

### W3 — Verification runs in layers that re-cover the same screens

Count the layers a first build pays for:

1. **Per-wave reviewers** — `skills/orchestrate/SKILL.md:96` ("Verify steps
   1–4b run per wave"): step 2 blind `code-reviewer` (`:261`), step 3
   deep-reasoner-tier reviewer for large/risk-domain diffs (`:262`, "even
   when tests pass"), step 4a blind UI-diff reviewer on **any** UI diff
   (`:264`), step 4b adversarial audit (`:268`). Fix #24 already stopped
   the *static* checks from re-running per wave (`:96`: "the static checks
   below run once") — that fix is present and correct; the per-wave
   *reviewer subagents* were not capped.
2. **Whole-build verification (expansion Phase 5)** —
   `skills/feature-expansion/SKILL.md:161-165`: "expansion Phase 5 IS
   orchestrate's Verification stage… runs the checks BY NAME —
   `browser-qa` / `click-path-audit` / `verification-before-completion` per
   feature", after the MVP is built. This re-verifies features the per-wave
   checks already passed.
3. **Visual loop** — `skills/browser-qa/SKILL.md:76`: "the caller caps rounds
   (max 3, then note diminishing returns and move on)" — capped, good; plus
   Hallmark audit "at most 1 fix round per problem list; rounds consumed
   here count against the same 2" (`skills/orchestrate/SKILL.md:272`) —
   shared budget, good.
4. **Fresh-context reviews** — hero review in a fresh context
   (`skills/design-taste-frontend/SKILL.md:537`), finish review in a fresh
   context (`skills/orchestrate/SKILL.md:272`), fresh-verdict runs, 2-round
   shared budget (`:97-101`, `:272`). Each fresh context re-reads the review
   prompt + screenshots.
5. **Double capture** — `skills/polish-pass/SKILL.md:112` captures the full
   Capture Matrix ({light, dark} × {desktop 1440×900, mobile 390×844});
   `skills/browser-qa/SKILL.md` Phase 3 re-screenshots 3 widths × every flow
   state (COVER_F23). browser-qa does reuse polish-pass captures *as the
   baseline* ("when `polish-pass` ran first, use
   `.polish-pass/captures/after/capture.json` + its PNGs as the committed
   baseline — no baseline ⇒ report INCONCLUSIVE"), but both skills still
   capture full matrices.
6. **End-of-project verification-loop** — six phases
   (`skills/verification-loop/SKILL.md`: build, type check, lint, tests +
   coverage, security grep, diff review) — correctly deferred to the end by
   `rules/hackathon-mode.mdc` §3; not waste, but it is a *fourth* verification
   layer after per-wave, Phase 5, and browser-qa.
7. **Four parallel brainstorm subagents** —
   `skills/feature-expansion/SKILL.md:54`: "Dispatch four brainstorm
   subagents in parallel, in one message", each returning 5–9 candidates
   (OVERDRIVE, `:40`). Appropriate for a first build; wasteful if re-run on
   later small expansions — Phase 5's trigger (`:161`) says it runs "exactly
   once", but nothing caps re-running Phases 0–3 on a later ask.

**Fixes:** (a) cap per-wave reviewers: step 2/4a reviewers run per wave only
while waves are large; small waves get the step-1 cheap check only
(`:260` already allows this — make it the default, reviewer the exception);
(b) merge the hero review and finish review into ONE fresh-context review
when both apply (`:537` + orchestrate `:272`); (c) single capture run:
polish-pass captures once, browser-qa consumes those captures and shoots
only what the matrix lacks; (d) cap the beat-v5 re-deal loop — see extra
gap G3; (e) do not re-run expansion Phases 0–3 after the first build except
on explicit ask.

### W4 — Record-keeping context burn (keep, but bound)

`skills/orchestrate/SKILL.md:66` (read the whole design inventory FIRST +
record USED vs CONSIDERED-AND-REJECTED per entry), `:68` (D19 reasons "never
a blanket line"), `:96` (D19 six-dimension lines per decision-record entry;
BENCHMARK_V5 per-dimension table; TECHDEPTH per-CORE-flow blocks with ≥3
edge cases), `skills/design-taste-frontend/SKILL.md:411` (Type list per
text element, F7). This is quality spend, not waste — but the USED-vs-
REJECTED verdict is demanded for *every* inventory entry, and the inventory
has 11 sections. **Fix:** USED-vs-REJECTED only for entries actually
considered for this build; untouched sections record one line ("not
considered — <reason>").

### What is NOT waste (confirmed correct)

- `/demo` gating: `skills/pitch-deck-video/SKILL.md:221,225` ("runs only on
  explicit invocation (fix #22 gate)"), `:291` ("films the LOCAL app"),
  `:102` (2:10 hard rule, 2:30 absolute max), `rules/hackathon-mode.mdc` §7
  ("/demo … runs ONLY when the user invokes it explicitly … never as a
  pipeline step, never by default"). Duration canonical in hackathon-mode
  §6 and `skills/hackathon-pitch/SKILL.md:32`.
- `/demo` cost: ElevenLabs free tier, 10,000 chars/month
  (`rules/hackathon-mode.mdc` §7), "about 7 demos a month free"
  (`skills/pitch-deck-video/SKILL.md:829`); `--script`/`--render` reuse
  avoids re-rendering (`:546-548`); narration-key prompt sent once, never
  re-asked (`rules/hackathon-mode.mdc` §7; `skills/orchestrate/SKILL.md:58`).
- Audit deferral: `rules/hackathon-mode.mdc` §3 defers `production-audit`,
  `delivery-gate`, `codehealth-mcp`, `verification-loop`, `santa-method`,
  `security-scan` to the end — the single biggest usage saving already in
  place; do not weaken it.
- Resume guards: `skills/orchestrate/SKILL.md:58,60-61` (steps 0–2 verify
  artifacts exist and run each piece once only if missing; "do NOT re-run
  `grill-me`", "do NOT re-run `hackathon-scope` / Phases 0–3").

---

## Claim 4 — VERIFICATION: screen-verdict monopoly ENCODED; check-the-source MISSING

### 4a. browser-qa as sole executor of screen verdicts — ENCODED (strong)

- `skills/browser-qa/SKILL.md:76` — "this skill is the SOLE executor of the
  distinctiveness bar inside the visual loop"; `:78` type-audit verdict
  ("Only this skill renders the type-audit verdict; `polish-pass` records
  the evidence, never the verdict. No other step judges screen
  distinctiveness"); `:80` hero verdict ("This verdict is `browser-qa`'s
  alone: no other step judges the hero"); `:82` memorability verdict
  ("This verdict is `browser-qa`'s alone: no other step judges
  memorability"); `:83` beat-v5 live verdicts ("this skill's verdict alone
  — a dimension that cannot be scored live is recorded as owed, never as
  passed").
- `skills/browser-qa/SKILL.md:134-136` — verdict ∈ SHIP / SHIP WITH FIXES /
  DO NOT SHIP; INCONCLUSIVE if no visual baseline; BLOCK_F23: "A coverage
  matrix with an empty cell is never reported as SHIP, SHIP WITH FIXES, or
  INCONCLUSIVE-as-pass".
- `skills/browser-qa/SKILL.md:76` (visual loop) — "Never claim visual
  verification without actually inspecting the rendered interface."
- `skills/orchestrate/SKILL.md:272` (Verify stage 6) and
  `skills/design-taste-frontend/SKILL.md:509,537` — static checks and
  sloplint/hero-review findings are candidate evidence, "never a screen
  verdict"; "the verdicts themselves … are `browser-qa`'s alone".
- `skills/verification-before-completion/SKILL.md:38,45` — claim table:
  "Agent completed | VCS diff shows changes | Agent reports 'success'";
  red flag: "Trusting agent success reports". `skills/verification-loop/SKILL.md:102`
  (Target acceptance): "Passing local checks, review, merge, or release does
  not establish target acceptance."
- `skills/orchestrate/SKILL.md:262` — "Passing tests never waive it" (the
  step-3 reviewer runs even when tests pass).

**Gap inside 4a:** no single sentence states "test passage is NOT browser
verification". The pieces exist (above) but the rule is never written as
one line, so an agent can report "34/34 tests pass" in the final report and
a reader takes it as verified. **Fix:** add to
`skills/verification-before-completion/SKILL.md` (claim table) a row:
"UI verified | browser-qa verdict on the rendered screen | test suite
passing, screenshots described but not inspected, agent report" — and to
`skills/orchestrate/SKILL.md:270` (Verify step 5): "Test passage is not a
screen verdict; a green suite never substitutes for the visual loop."

### 4b. Check-the-source before stating scoring / timing / logistics — MISSING

Zero hits for "check the source" anywhere in the shipped skills; zero hits
for "exact spec" or "verified number". Consequences, each traceable to the
weekend:

- **Scoring:** no scoring source exists in the plugin. Grep for
  "bonus"/"extra points" across `hackathon-pitch`, `pitch-deck-video`,
  `hackathon-scope` returns nothing (only `pitch-deck-video/SKILL.md:460`,
  "extra runtime (FILM_F6)"). The weekend correction — a 5-minute video
  DOES earn extra points — has no anchor the agent could have checked. The
  plugin's own duration canon (`rules/hackathon-mode.mdc` §6;
  `skills/hackathon-pitch/SKILL.md:32`) states lengths, never points.
- **Timing:** `skills/hackathon-scope/SKILL.md:98-105` has the rule of
  thirds and "NEVER assume '5 more hours = 5 more features' — risk grows
  non-linearly", but nothing says "re-measure durations; never restate an
  estimate as a fact". The Challenge 2 batch was quoted as 4–8 hours, then
  measured at ~17 hours — the plugin never required the measurement to
  replace the estimate in the record. Same for the finalist time (4:00 vs
  4:30 PM): no rule to re-read the spec/invite before stating a time.
- **Logistics:** `skills/hackathon-scope/SKILL.md:111` picks a category by
  rubric match, but no rule says "before stating any scoring, timing, or
  logistics fact in a report or reply, re-read the source document (spec,
  invite, rubric) and cite it".

**Fix (new rule, belongs in `skills/orchestrate/SKILL.md` step 6 final
report + `skills/hackathon-scope/SKILL.md`):** "CHECK-THE-SOURCE: every
scoring, timing, or logistics claim in a final report, reply, or deliverable
prompt cites the source document it was read from (spec section, invite,
rubric) with the value as written there. An estimate is labelled an estimate
with its basis; a measured value replaces the estimate in the record the
moment it is measured. Never restate a remembered number as a fact." Add a
final-report checklist line: "Scoring/timing/logistics claims — source cited
per claim, or the claim is removed."

### 4c. Audits are a guide, not the source — MISSING as a sentence

The *mechanism* exists for design audits: sloplint flags and hero-review
template observations are "candidate evidence, never a verdict"
(`skills/browser-qa/SKILL.md:76`;
`skills/design-taste-frontend/SKILL.md:537`). But there is no general rule
that an audit (any audit — design, code, or the weekend's deliverable
audits) is advisory and the spec/source is authoritative, and no rule that
**deliverable prompts must cite the exact spec and use only exact verified
numbers**. That second rule is entirely absent: nothing in `hackathon-pitch`,
`orchestrate` step 6, or `feature-expansion` Phase 6 constrains prompt
numbers to verified values.

**Fix:** add to `skills/orchestrate/SKILL.md` step 6 (final report) and
`skills/hackathon-pitch/SKILL.md`: "AUDIT-AS-GUIDE: an audit (sloplint,
reviewer, or any checklist pass) is a guide, never the source. The source is
the spec / the rendered screen / the measured run. Where an audit and the
source disagree, the source wins and the disagreement is recorded. Every
number in a deliverable prompt or submission cites the exact spec section
and uses only exact verified numbers — no rounded, remembered, or inferred
figures."

---

## Claim 5 — "LOCK IN" (flag the quality/score ceiling when knowable): MISSING

No occurrence of "ceiling" in `skills/orchestrate/SKILL.md` (the only
"ceiling" hits in the plugin are unrelated: `pitch-deck-video` 2:30
"absolute ceiling" and theme-file text). Closest existing text, and why each
falls short:

- `skills/hackathon-scope/SKILL.md:47-67` — project assessment
  (strengths / weaknesses / opportunities / constraints / recommended
  direction) and the wow test ("if there is no such moment, the must-have
  list is not done"). Written into `docs/scope.md`, never surfaced to the
  user as a ceiling, and never revisited when the build proves thinner than
  scoped.
- `skills/hackathon-scope/SKILL.md:111-115` — winnable-category pick ("A
  safe silver in a small category beats trying for gold in the
  megacategory"). A category choice, not a ceiling flag.
- `skills/feature-expansion/SKILL.md:130` — planner rubric scores
  feasibility 1–3 per candidate. Feasibility is scored and then buried in
  the planner's verdict; the user never sees "this build tops out at X".
- `skills/hackathon-scope/SKILL.md:67` ("No silent re-scope") +
  TECHDEPTH_F25 cut-substance lines — records *cuts* in docs, not the
  *ceiling* to the user. A cut recorded in `docs/scope.md` is invisible
  until the user reads the final report — which is exactly the failure mode
  (discovering a low ceiling the night it is due).
- `skills/orchestrate/SKILL.md:209` / `rules/hackathon-mode.mdc` §7 —
  "mark it blocked with evidence, and note it in the final report" — again
  final-report-only disclosure.

**Fix (new rule, belongs in `skills/hackathon-scope/SKILL.md` + a
`CEILING` line in `skills/orchestrate/SKILL.md` step 6):**

> **LOCK-IN (ceiling flag).** The moment the achievable quality/score
> ceiling is knowable — at scoping (weak rubric match, missing hard
> substance, a core flow with no real algorithm/data), at expansion
> (planner feasibility ≤ the floor), or mid-build (a cut that lowers the
> ceiling) — state it to the user immediately, in the reply, not only in a
> doc: what the ceiling is, what sets it, and what would raise it. Never let
> the user discover a low ceiling the night it is due. The ceiling line is
> re-stated in every final report (`Ceiling: <level> — set by <cause> —
> raising it needs <change>`).

Note the interaction with claim 6: a ceiling flag is a *message*, not a
blocking question — the build continues on the best honest path unless the
user redirects. That distinction is what makes it compatible with §7's
autonomy (see claim 6).

---

## Claim 6 — UNMET DELIVERABLES (say so immediately; let the user decide): PARTIAL, and in conflict with §7

### What exists

- `rules/hackathon-mode.mdc` §1: "Never fabricate completion — say plainly
  what could not be tested or verified; it belongs in the final report as a
  remaining issue, not as done."
- `rules/hackathon-mode.mdc` §7 + `skills/orchestrate/SKILL.md:209`: "if no
  reversible option exists, skip it, mark it blocked with evidence, and note
  it in the final report."
- `skills/orchestrate/SKILL.md:233` — executor report contract:
  `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`, ≤20 lines;
  "Executors never silently deliver work they're unsure about."
- `skills/feature-expansion/SKILL.md` Phase 6 — Blocked / Rejected-or-cut /
  Not-built lists with files and fallbacks.
- `skills/grill-me/SKILL.md` steps 2/5 — accepted unknowns carry an owner
  and a resolution point; never silently guessed.

### What is missing — and the conflict

1. **Timing:** every existing disclosure lands in the **final report**,
   which the user reads on return. Nothing requires telling the user
   *immediately* when a deliverable cannot be met, and nothing offers the
   user the decision (best honest framing / try our best / workaround).
2. **Direct conflict with hackathon-mode §7:**
   `rules/hackathon-mode.mdc` §7: "after that, do not ask the user anything,
   do not wait for an approval, and do not stop for a decision." And
   `skills/orchestrate/SKILL.md:58`: "This is the ONE sanctioned user prompt
   during the first build besides grill-me itself" (the narration-key
   prompt). An immediate "this deliverable cannot be met — how do you want
   to handle it?" prompt is currently **non-compliant** with the plugin's
   own rules. The implementer must resolve this conflict explicitly; it
   cannot be fixed by adding the new rule alone.

**Fix (new rule + §7 carve-out, belongs in `rules/hackathon-mode.mdc` §7
and `skills/orchestrate/SKILL.md` step 6):**

> **DELIVERABLE-AT-RISK (second sanctioned prompt).** If a deliverable
> cannot be met as specified — a required feature, a submission artifact, a
> spec-mandated number or format — flag it to the user immediately, in the
> reply, with the three options: (a) best honest framing (ship what exists,
> stated plainly), (b) try our best (attempt it with the shortfall named),
> (c) a workaround (a substitute that meets the intent). The flag is a
> message, not a gate: unless the user replies, proceed on (b) — try our
> best with the shortfall named — and record the flag + the default taken in
> the run ledger and the final report. Never silently drop a deliverable,
> never silently substitute an easier version (see also "No silent
> re-scope", `skills/hackathon-scope/SKILL.md:67`), and never present the
> easy version as the hard one.

Add to §7: "The deliverable-at-risk flag is the second sanctioned user
prompt during the first build, alongside the narration-key prompt. It never
blocks the build."

---

## Claim 7 — GRILL-ME: ENCODED, with two holes

### What is encoded (strong)

`skills/grill-me/SKILL.md` — runs FIRST after the first project prompt,
before scoping/building/expansion (description + When to Use); one question
at a time (`:26`, format `### Decision <N> — <topic>` + Recommended / Why /
Tradeoff / Question); mandatory order product → hours-left (Q2) → named API
(Q3); ~6-question cap, stop when the user stops answering; skip path
(`:18`: "skip the grilling" / "just build it" → straight to
`hackathon-scope`); big-prompt EXECUTION posture vs vague-prompt REASONING
posture with Source tags USER-STATED / INFERRED / ASSUMED (fix #25 ADAPT_F25,
step 2 — "do not re-ask what the user already decided"); incremental record
write after EVERY answer (step 2); proceed-on-next-message (step 3: any
non-answer reply proceeds on the partial record immediately); unanswered
branches become accepted unknowns with owner + resolution point, never
blockers (step 5). `rules/hackathon-mode.mdc` §1 and §7 repeat all of it,
and §7 states the autonomy consequence: "Once the check passes, the first
build runs fully autonomously until it is done." `skills/orchestrate/SKILL.md:10`
(read the decision record first) and `:54` (precondition check) wire it in.

### Hole 1 — the precondition check licenses silent no-grill

`skills/orchestrate/SKILL.md:54`: "If neither holds [no record, no explicit
skip], do not proceed without a check: run the check (record exists, or
explicit skip), and once that check is done, proceed on the raw user prompt
with a stated assumption recorded in the stage ledger — do NOT re-run
`grill-me`. The check is what licenses proceeding; proceeding without any
check is what is forbidden, not proceeding itself." Combined with Gate C
(claim 2 — no live entry point, trigger is documentation-only), the failure
mode is: the alwaysApply rule misfires on a fresh chat, no grill-me runs, no
explicit skip exists, and orchestrate *proceeds anyway* on the raw prompt
with a ledger note the user never sees. Grill-me is the default in prose
and optional in practice.

**Fix:** in `skills/orchestrate/SKILL.md:54`, add: "If the check finds no
record and no explicit skip, that is itself a finding: state in the first
reply that grill-me did not run and why (no trigger / no record), and ask
the user whether to grill now (one prompt) or proceed — the one-question
exception to §7. Do not silently proceed on a raw prompt." Also fix
`skills/hackathon-scope/SKILL.md` (stub-record path): a stub record written
when grill-me was skipped must be marked `grill-me: SKIPPED`, never left
looking like a grilled record.

### Hole 2 — no way to know grill-me ran vs. was skipped, after the fact

The only signal is the existence of `docs/decision-record.md`, and
hackathon-scope writes a stub record in the skip case — so "record exists"
cannot distinguish grilled from skipped. **Fix:** the record's header must
carry `grill-me: RAN | SKIPPED (user said "<phrase>") | MISSED (no trigger)`
— grill-me step 5 writes RAN; hackathon-scope writes SKIPPED/MISSED.

---

## Claim 8 — DURABLE RULES: all present EXCEPT the git-attribution rule

Verified present (do not remove):

| Rule | Anchor |
|---|---|
| 9 alwaysApply production gates (80% coverage/TDD, plan-first, mandatory code review, functions <50 lines, files <800 lines) | `rules/common-testing.mdc:2,7` (80%); `rules/common-development-workflow.mdc:23` (80%+); `rules/common-code-review.mdc:34,41,101-102` (50 lines, 80% minimum, 800 lines); `rules/common-coding-style.mdc:47`; `rules/hackathon-mode.mdc` §4 (ECC process applies in full) |
| D19 — every UI decision carries a recorded reason across the FULL experience; distinct brand identity; weaving total and BINDING | `skills/orchestrate/SKILL.md:96` (D19: all six dimension lines — Motion/Theme/Texture/Visuals/Techniques/Colors — per decision-record entry; note fix #24 count convention: read "six" as seven with Depth); `:62,64,68,72,74,79,83,85,86`; `:32` (BIND); `:34` (INNOV); `:171` (routing — every decision through the package); `rules/hackathon-mode.mdc` §6 (BIND/INNOV) |
| Fraunces BODY-ONLY | `skills/orchestrate/SKILL.md:151` (fix #20 body-only scope); `skills/design-taste-frontend/SKILL.md:411` (F4, F2) |
| Fonts static + self-hosted | `skills/design-taste-frontend/SKILL.md:411` (F2: static instances, one bundled woff2 per weight, `@font-face`, no variable file as shipped format, no `system-ui`/generic fallback); `skills/orchestrate/SKILL.md:96` (F2 static check) |
| Design package forced for any UI/UX | `skills/orchestrate/SKILL.md:127` (row 10), `:171`; `skills/design-taste-frontend/SKILL.md:411` (step 4a) |
| "More, not bolder" | `skills/orchestrate/SKILL.md:68,72,167`; `skills/browser-qa/SKILL.md:82`; `skills/design-taste-frontend/SKILL.md:55,264` |
| Anti-derivative rule | `skills/orchestrate/SKILL.md:169`; `skills/design-taste-frontend/SKILL.md:423` (bound 8) |
| Feature expansion ~1.75x | `skills/feature-expansion/SKILL.md:40,54,108`; `skills/orchestrate/SKILL.md:61`; `rules/hackathon-mode.mdc` §1 |
| Anti-drift guard | `skills/feature-expansion/SKILL.md:40` ("anti-drift bound stays and is explicit"); `skills/orchestrate/SKILL.md:61`; `rules/hackathon-mode.mdc` §1 |
| Two agents never edit the same folder simultaneously | `skills/orchestrate/SKILL.md:254` ("Parallel workers that edit files concurrently must be serialized"); `skills/dispatching-parallel-agents/SKILL.md` (independence / non-interference) — note: phrased as serialization, not as an outright ban; adequate, keep as is |
| Git commits: NO "Co-authored-by: Cursor" trailer, NO AI tool as contributor/author | **MISSING — zero hits for "Co-authored-by" in the entire shipped plugin tree** (`skills/`, `rules/`, `commands/`, `agents/`). The rule lives only in memory/fix notes. The weekend's repos were pushed without the trailer only because the human/commit process avoided it, not because the plugin says so. |

**Fix for the missing rule:** add to `rules/common-git-workflow.mdc` (or
`skills/orchestrate/SKILL.md` step 6, commit step — cite the exact location
in the implementation): "Commit messages carry no `Co-authored-by:` trailer
for any AI tool (including Cursor) and name no AI tool as author or
contributor. The commit author is the user." Add it to the step-6 static
check list so the audit fails a commit carrying the trailer.

---

## Other weekend-relevant gaps found

**G1 — Deliverable prompts: cite the exact spec, only exact verified
numbers — MISSING.** See claim 4c. No skill constrains numbers in prompts
or submissions to verified values. The weekend's deliverable prompts were
written under this rule by the parent agent, not by the plugin.

**G2 — Audits are a guide, not the source — MISSING as a general rule.**
See claim 4c. Only the design-audit instance (candidate evidence, never a
verdict) is encoded.

**G3 — Unbounded beat-v5 re-deal loop.**
`skills/orchestrate/SKILL.md:96` (BENCHMARK_V5_F25 static check): "a table
that is missing, or any dimension that ties or trails v5, is an incomplete
build — the design-lead re-deals or redesigns until every dimension beats
v5." No cap. Under a usage crunch this is an unbounded loop. **Fix:** cap
at 2 re-deals/redesigns; after that the trailing dimension is recorded as
owed with its cause (which is also the ceiling flag — claim 5).

**G4 — No duration-measurement rule.** See claim 4b. Add: "Replace every
estimate with the measured value the moment it is measured; the record
never keeps a superseded estimate."

**G5 — Verification-before-completion has no browser-verification row.**
See claim 4a. One-line addition.

**G6 — `frontend-design-direction`'s rendered finish gate is not wired
into hackathon flow.** That skill's gate ("Source inspection alone cannot
pass this gate") is sound and already matches browser-qa's stance, but
`rules/hackathon-mode.mdc` §5 deliberately excludes the skill from hackathon
UI work. No change proposed — just noted so the implementer does not
re-invent it: browser-qa already owns the rendered gate.

**G7 — Staged/shipped drift is trivial but real.** orchestrate `SKILL.md`
differs only in agent-file references (staged bare `code-reviewer` vs
shipped `agents/ecc-code-reviewer.md`, L96/L261/L268); design-taste-frontend
differs by 1 line. No action beyond keeping the staged sources as the edit
source and rebuilding.

---

## Prioritized change list for the implementation step

1. **P0 — Reconcile the implementer-model contradiction (W1).**
   `skills/orchestrate/SKILL.md:89` vs `:30`/`:129`. Decide: implementers on
   4.6-fast (change `:89`) or 4.7 by design (delete the "no execution on the
   4.7 mind" sentences). Largest usage lever; also the only outright
   contradiction found.
2. **P0 — Theme: starting point, not cage (claim 1).**
   `skills/design-taste-frontend/SKILL.md:256-262,423`;
   `skills/orchestrate/SKILL.md:127,137,169`. Demote the deal, widen the
   genre map, allow recorded departure, give dashboards a dealt moment.
3. **P0 — Orchestration: always-lead (claim 2).** Remove the `:14` hedge;
   add a first-reply pin statement (`:89`); extend orchestrate past the
   first build (`:50-56`, `:109`; `rules/hackathon-mode.mdc` §6).
4. **P0 — LOCK-IN ceiling flag (claim 5, new rule).**
   `skills/hackathon-scope/SKILL.md` + `skills/orchestrate/SKILL.md` step 6.
5. **P0 — Deliverable-at-risk flag + §7 carve-out (claim 6, new rule).**
   `rules/hackathon-mode.mdc` §7 + `skills/orchestrate/SKILL.md` step 6.
   Must resolve the §7 conflict explicitly.
6. **P1 — Check-the-source rule (claim 4b) + audit-as-guide +
   exact-verified-numbers for deliverable prompts (claim 4c, G1, G2).**
   `skills/orchestrate/SKILL.md` step 6 + `skills/hackathon-pitch/SKILL.md`
   + `skills/hackathon-scope/SKILL.md`.
7. **P1 — Usage caps (W2, W3, G3).** Gate the blind-parallel second pass
   (`skills/orchestrate/SKILL.md:18,117,278,282`); cap per-wave reviewers;
   merge hero + finish fresh-context reviews; single capture run
   (polish-pass + browser-qa); cap beat-v5 re-deals at 2 (`:96`).
8. **P1 — Grill-me holes (claim 7).** `skills/orchestrate/SKILL.md:54`
   (state when grill-me missed; one-question exception); record header
   `grill-me: RAN | SKIPPED | MISSED`.
9. **P1 — "Test passage is not browser verification" one-liner (claim 4a).**
   `skills/verification-before-completion/SKILL.md` claim table +
   `skills/orchestrate/SKILL.md:270`.
10. **P1 — Encode the no-`Co-authored-by: Cursor` rule (claim 8).**
    `rules/common-git-workflow.mdc` + orchestrate step-6 static checks.
    Currently nowhere in the plugin.
11. **P2 — Bound the record-keeping (W4).** USED-vs-REJECTED only for
    entries actually considered (`skills/orchestrate/SKILL.md:66,68`).
12. **P2 — Duration-measurement rule (G4).** Replace estimates with
    measured values in the record (`skills/hackathon-scope/SKILL.md`).

**Explicitly not changed:** the 9 alwaysApply gates, D19, Fraunces
body-only, static self-hosted fonts, the forced design package, "more, not
bolder", the anti-derivative rule, ~1.75x expansion, the anti-drift guard,
the serialization rule, the /demo gate (explicit invocation only, local app
only, 2:10 / 2:30 max), audit deferral to end-of-project
(`rules/hackathon-mode.mdc` §3), and the fix #24 resume guards
(`skills/orchestrate/SKILL.md:58,60-61,96`).
