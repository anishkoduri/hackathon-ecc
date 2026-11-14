# Fix #25, §4(d)–(f) — design + technical depth (worker E) — work note

Status: staged edits DONE. No rebuild, no loop run (per task — a later
worker builds and runs the loops). No `fix25.py` created (see §6).
`design-inventory.md`, all `verify*.py`, and all pitch-deck-video template
files NOT touched (parallel workers own them).

Anchor tokens (stable locators for the weave worker):
`BENCHMARK_V5_F25`, `TECHDEPTH_F25`, `ADAPT_F25`, `REASON_F25`,
`CREATIVE_F25`. Counts verified by grep after editing (see §7).

## §1 The v5 benchmark figures, as read from the record

Sources read: `fix17/dryrun28-report.md` (the v5 recount),
`fix17/INVENTORY-V4.md` (v1–v4 inventory + counting-rule discussion),
`fix17/PARENT-GUIDANCE.md` (v5 delta as named by the parent),
`fix15/BASELINE.md` (the counting rule), and
`~/workspace/cold-start-render/campus-eats/docs/design-tokens.md`
(the v1-era tokens file — 114 lines, pre-fix15 direction; the ONLY file
in the Campus Eats record dir).

- v5 total, literal (primary reading): **61 elements** (v4 54 + v5 7).
  Stricter reading: **60** (Motion 16 — confetti loop #66 excluded).
  Sensitivity: marker checks per instance (×3) → total 63.
- By kind, literal: Component **31**, Treatment **8**, Visual **1**,
  Motion **17**, Moment **1**, Type **2**, Effect **0**, Diagram **1**.
  Stricter: Motion 16, all else same, total 60.
- v5 delta +7 (Component +3, Treatment +2, Motion +2): #60 sticker-peel
  hover (Motion); #61 washi tape (Treatment); #62 marker checks ×3 as
  ONE feature (Treatment); #63 coin stack (Component); #64 bus-pass
  ticket (Component); #65 sticker sheet (Component); #66 confetti stars
  (Motion). Growth v4 → v5: +7 (+13% on 54); Motion 15 → 17 (+13%).
- Version history (literal): v1 25 → v2 32 → v3 40 → v4 54 → v5 61.
  No Effect at any version.
- Theme: Sticker. Hero deal: `centred`. Moments dealt:
  letters-assemble + iris-opens. letters-assemble APPLIED (ink-band
  statement). **iris-opens DEALT with NO recorded application**
  (dry-run #28 §C); R4 hero loop likewise no recorded application.
- Dynamic interface (my enumeration from the prose render history —
  see §8 caveat): 8 interactive / live-state items; 1 cross-surface
  state drive (stepper → live total + coin stack + $10 row flip);
  2 live-data surfaces (app-frame spot list; budget stepper).
  Live-probe facts on record: $8 → $12 drive, $10 row flips to
  "Fits"; Taco sticker click registered.
- Alignment: **NO Campus Eats alignment figure exists in the record.**
  The fix #23 alignment assertions were verified on Home Run only
  (52 measurements, 0 problems).
- SPEC wording notes (see §8): the SPEC's "motion/interactivity
  +10–15% over v4" is the measured +13% v4 → v5 growth (total and
  Motion alike); INVENTORY-V4.md §4 flagged the v4 brief's own
  "motion +10-15%" label as inconsistent with the literal count
  (v4 literal +35% on v3). The SPEC's "letters-assemble + iris-opens
  moments" reads as if both were applied; the record shows iris-opens
  dealt but unapplied — the benchmark treats applying it as part of
  beating v5.

## §2 Edits — §4(d) design bar

### E1 (NEW FILE) `new-skills/orchestrate/references/design-benchmark-v5.md` (178 lines)

The durable v5 benchmark reference, anchor `BENCHMARK_V5_F25`.
Ships automatically: `build.sh:224` copies the whole
`new-skills/orchestrate/references/` directory into the built tree
(verified by reading build.sh; the actual built-tree copy is owed to
the later build worker — I did not rebuild). Contents: §1 the v5
figures above (counts table, delta, theme/hero/moments, dynamic +
functionality enumeration, alignment gap, provenance caveat); §2 the
seven-dimension pass criteria (see §4 below); §3 the Leg 2 scoring
procedure. The file is frozen at v5 — a future re-baseline writes a
new file, never edits these figures.

### E2 `new-skills/orchestrate/SKILL.md` — design-bar paragraph (new, before the MEMORABLE paragraph, :70)

Old text: `**Memorable is the bar — above F6 (fix #23 §1, MEMORABLE_F23):**`
New text: the same line, preceded by the new paragraph:
`**Design bar — beat Campus Eats v5 (fix #25 §4(d), BENCHMARK_V5_F25).** The design package reads `references/design-benchmark-v5.md` alongside the inventory at this step, BEFORE deciding. The v5 figures: 61 elements literal (60 stricter) — Component 31, Treatment 8, Visual 1, Motion 17, Moment 1, Type 2, Effect 0, Diagram 1; Sticker theme, hero deal `centred`, moments letters-assemble (applied) + iris-opens (dealt, no recorded application); 8 interactive / live-state items, 1 cross-surface state drive, 2 live-data surfaces; no v5 alignment figure recorded. The decision record carries a per-dimension beat-v5 table (count, variety, hero, motion, dynamic interface, functionality, alignment — the benchmark file's §2 criteria): the re-traced design must beat v5 on ALL SEVEN — ≥ 62 literal / ≥ 61 stricter, ≥ 7 kinds with ≥ 2 kinds above their v5 counts, hero inventory + loop or second moment, Motion ≥ 18 / ≥ 17 stricter, ≥ 9 interactive items with ≥ 2 cross-surface drives, ≥ 3 live-data surfaces, 0 alignment problems across the full coverage matrix. A tie on any dimension is below the bar on that dimension. **A build that would have scored like v5 is now BELOW the bar** — the design-lead re-deals or redesigns until the table beats v5; a v5-level design does not proceed to build on a "good enough" reading. The static checks for the table live in orchestrate step 5a; the verdicts on rendered screens (hero strength, live dynamic behaviour, live functionality, alignment) stay browser-qa's alone — a dimension that cannot be scored is recorded as owed to browser-qa, never claimed.`

### E3 `new-skills/orchestrate/SKILL.md` — step 5a static checks (appended to the fix #21 paragraph)

Old text: `(F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice.`
New text: the same sentence, followed by:
`**Fix #25 static checks (all static checks, never screen verdicts).** (BENCHMARK_V5_F25) The decision record carries the per-dimension beat-v5 table from `references/design-benchmark-v5.md` §2 (count, variety, hero, motion, dynamic interface, functionality, alignment), each dimension showing the re-traced figure against the v5 figure; a table that is missing, or any dimension that ties or trails v5, is an incomplete build — the design-lead re-deals or redesigns until every dimension beats v5. The static check verifies the TABLE and the statically-scored figures (counts, kinds, hero inventory + loop/moment application, interactive-item and live-data-surface counts); the live verdicts (hero strength, whether controls respond and changes are choreographed, whether the mechanism works, alignment) are browser-qa's alone, and a dimension whose live verdict is owed is recorded as owed, never as passed. (TECHDEPTH_F25) `docs/scope.md` carries the Technical-substance block (see `hackathon-scope`) and every CORE flow in it names its architecture, its algorithm/data-structure choice, its performance budget, and at least 3 edge cases with handling; a CORE flow with a missing block, a missing algorithm/data-structure choice, a missing budget, or fewer than 3 named edge cases is an incomplete build. Where scope was cut, the decision record carries the cut-substance lines (what was cut, why) — a hard idea rebuilt as an easy one with no cut line is an incomplete build. (REASON_F25) Every decision-record entry carries the three-part reasoning block — INFERRED / CHOSEN / REJECTED (see the reasoning-format rule below); an entry missing any of the three lines is an incomplete build.`

### E4 `new-skills/orchestrate/SKILL.md` — final report (two insertions)

Old text: `- **Inventory used vs considered-and-rejected** — which design-inventory.md entries were USED on this build and which were CONSIDERED-AND-REJECTED, with specific D19 reasons (AMBITION_F23).`
New text: the same line, plus:
`- **Beat-v5 table** — the per-dimension benchmark table (BENCHMARK_V5_F25): each dimension's v5 figure vs this build's figure, PASS / FAIL per dimension, and any dimension whose live verdict is owed to browser-qa (hero strength, live dynamic behaviour, live functionality, alignment) recorded as owed, never as passed.`

Old text: `- **Important design + engineering decisions** — each decision that shaped the product (architecture, data model, key trade-offs, what was chosen and what was rejected and why), one line each, taken from the stage ledger's Decided/Rejected fields.`
New text: the same line, plus: ` The engineering half names the technical substance per CORE flow (TECHDEPTH_F25): the architecture, the algorithm/data-structure choice, the performance budget and whether it was met, the edge cases handled — and what technical substance was cut and why, if any was.`

### E5 `round2-skills/polish-pass/SKILL.md` — benchmark static check (non-negotiable 5) + variety pointer

Old text (non-negotiable 5, end of memorability paragraph): `whether the build is actually memorable is `browser-qa`'s finish-review verdict alone (MEMORABLE_F23). "Over the top" here is ambition and impact, not loudness: "more, not bolder" still governs styling, so a quiet-palette build with a strong moment is not flagged for being quiet.`
New text: the same sentences, followed by:
`Then run the beat-v5 benchmark check (fix #25 §4(d), BENCHMARK_V5_F25) on the same target — same standing: candidate evidence for `browser-qa`, never a verdict — and record its per-dimension table in `.hallmark/candidate-evidence.md` (dimension + v5 figure + this build's figure + PASS / FAIL per dimension) the same way slop findings are recorded. Count the build's elements with the fix #15 counting rule (one discrete, deliberate design application = one count; instances count individually; one kind per element by precedence Moment > Effect > Visual > Diagram > Treatment > Component > Motion > Type) from `docs/design-tokens.md` + the built screens, and score each dimension against `skills/orchestrate/references/design-benchmark-v5.md` §2 (count ≥ 62 literal / ≥ 61 stricter; variety ≥ 7 kinds with ≥ 2 kinds above v5; hero inventory + loop or second moment; Motion ≥ 18 / ≥ 17 stricter; ≥ 9 interactive items with ≥ 2 cross-surface drives; ≥ 3 live-data surfaces; 0 alignment problems across the full coverage matrix). A dimension that ties v5 is below the bar on that dimension — a tie is not a beat — and is recorded as candidate evidence, never a verdict: whether the hero is actually strong, the controls actually respond, the mechanism actually works, and the alignment actually holds is `browser-qa`'s live verdict alone, and a dimension that cannot be scored is recorded as owed, never as passed.`

Old text (Element variety paragraph): `Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).`
New text: the same sentence, plus: ` The bar the elements are judged against is the Campus Eats v5 benchmark (`skills/orchestrate/references/design-benchmark-v5.md`, BENCHMARK_V5_F25): a build that would have scored like v5 is below the bar — see non-negotiable 5 for the per-dimension check.`

## §3 Edits — §4(e) technical depth

### E6 `rewritten-skills/hackathon-scope/SKILL.md` — Technical-substance section (new, before "## Vertical slices")

Old text: `## Vertical slices, not horizontal layers`
New text: the same heading, preceded by the new section
`## Technical substance — hard ideas get hard builds (fix #25 §4(e), TECHDEPTH_F25)` requiring a Technical-substance block in `docs/scope.md`, one entry per CORE demo flow: Architecture (components + data flow, one line each); Algorithm / data structure (named choice + why; "look it up / call the API" is allowed if the build's work with the result is named — substance is the architecture/algorithms/system design AROUND the tools, never a from-scratch rewrite — off-the-shelf maximalism stands); Performance budget (named numbers, or explicit `no budget — <reason>`); Edge cases (at least 3 named per CORE flow, each with handling; "demo doesn't enter X" is a cut, not a handling). Plus the **No silent re-scope** rule: substance cuts go in the cut list as `cut substance: <what> — <why>` and in the decision record; a cut with no recorded reason is a scope gap.

### E7 `rewritten-skills/hackathon-scope/SKILL.md` — scope-traps table row

Old text: `| **Generic UI** | Polished design system | The 3 screens for the demo, that's it |`
New text: the same row, plus:
`| **Quiet re-scope** | Hard idea rebuilt as an easy one (real algorithm → canned output; real-time → static mock; real data flow → hardcoded demo data) | Name the substitution in `docs/scope.md`'s cut list with the reason — "cut substance: <what> — <why>" — and carry it in the decision record (TECHDEPTH_F25); never present the easy version as the hard one |`

### E8 `new-skills/orchestrate/SKILL.md` — technical substance in implementer briefs (new paragraph inside step 4)

Old text: `If two implementers in the same wave touch the same files, the orchestrator decides the merge order`
New text: the same sentence, preceded by the new paragraph:
`**Technical substance in every implementer brief (fix #25 §4(e), TECHDEPTH_F25).** Every implementer brief names the slice's technical substance, alongside its UI rule: (a) the architecture slice — the components and data flow this slice owns, one line each; (b) the algorithm / data-structure choice that does the hard work, named with why this choice (not a generic "we process the data"); (c) the performance budget — named numbers (latency, throughput, size, or render budget) the slice must meet, or an explicit `no budget — <reason>` where genuinely not applicable; (d) the edge cases — at least 3 named per slice, with the handling for each. Architecture and algorithm design route to deep-reasoner (routing row 7 — reasoning-heavy work), never to a fast-worker brief; a fast-worker slice that faces an algorithm or architecture decision routes it up. Depth lives in what the build DOES, not in re-implementing what an off-the-shelf tool does better (hackathon-scope's off-the-shelf maximalism stands): the substance is the architecture, algorithms, and system design around the chosen tools, never a from-scratch rewrite of one. A hard idea must not be quietly re-scoped down to an easy one: if the brief cuts technical substance (a real algorithm replaced by canned output, real-time replaced by a static mock, a real data flow replaced by hardcoded demo data), the brief says what was cut and why, and the decision record carries the same cut line — a cut with no recorded reason is an incomplete brief. Verify step 4b's adversarial audit probes the hard path (edge cases, performance budget, failure modes), not only the happy path.`

### E9 `new-skills/feature-expansion/SKILL.md` — brief item 8 + Phase 5 substance verification

Old text: `7. Tool/API: the proposal's Tool/API value for this feature, named explicitly (the named tool, API, SDK, or library from the Phase 2 table — or "none") — the implementer wires that tool, not a substitute it picks itself.`
New text: the same item, plus:
`8. Technical substance (fix #25 §4(e), TECHDEPTH_F25): the feature's architecture slice (components + data flow it owns), its algorithm / data-structure choice (named, with why), its performance budget (named numbers, or an explicit `no budget — <reason>`), and at least 3 named edge cases with handling. The completion evidence (item 4) exercises the real path — the hard input, the edge cases, the budget — not only the happy path. If the feature's substance is cut during implementation (real algorithm → canned output, real-time → static mock), the implementer reports the cut with its reason in its result instead of silently landing the easy version.`

Old text: `2. Confirm every landed feature with `verification-before-completion`: run it, read the output, then claim it.`
New text: `2. Confirm every landed feature with `verification-before-completion`: run it, read the output, then claim it. The confirmation exercises the feature's technical substance (TECHDEPTH_F25) — the real path, its named edge cases, its performance budget — not only the happy path: a feature that works on the demo input and fails its own edge cases is not confirmed.`

No new skill created for technical depth (default per task): the
substance rules live in the existing briefs/checks (scope, orchestrate
step 4, expansion Phases 4–5, orchestrate step 5a). The deferred six
(`production-audit`, `delivery-gate`, `codehealth-mcp`,
`verification-loop`, `santa-method`, `security-scan`) were NOT
un-deferred: substance verification sits in the build-time Verify
steps and the final report, as the task requires.

## §4 Edits — §4(f) adaptive + creative

### E10 `new-skills/grill-me/SKILL.md` — adaptivity in step 2

Old text: `2. Maintain a running decision record with: decision, chosen option, rationale, dependencies, and consequences. Update it after every answer; do not reopen a recorded decision unless new evidence conflicts with it.`
New text: the same sentences, plus:
`**Adapt to how much the user specified (fix #25 §4(f), ADAPT_F25).** Before the first question, assess specified-ness: count how many material decisions the prompt already makes (product, users, features, constraints, design direction, stack, named API). A big, complete prompt gets EXECUTION posture: verify the decisions are complete (the mandatory Q2/Q3 check below), write the record, and move on — do not re-ask what the user already decided. A vague one-liner gets REASONING posture: the questions do the reasoning work — infer the domain and its conventions, the user, the constraints, the demo, and the wow moment — propose options with reasons, and record every inference explicitly as INFERRED (see the record format in step 5), never as if the user stated it. Between the poles, the posture follows the prompt: ask only what is undecided, execute what is decided. Every record entry carries a Source tag — USER-STATED, INFERRED (with the reasoning one-liner), or ASSUMED (a default, marked assumed, not user-stated).`

### E11 `new-skills/grill-me/SKILL.md` — record format in step 5

Old text: `— a decision/choice/rationale/consequence table, the hours-left number (or the recorded hours-left assumption from step 2 if the user stopped answering before giving it), `### Risks`, accepted unknowns (each with an owner and a resolution point), rejected alternatives that matter, and `### Completion criteria`, plus one `Design direction:` line`
New text: `— a decision/choice/rationale/consequence table, with every entry in the mandatory three-part reasoning format (fix #25 §4(f), REASON_F25): **INFERRED** (what was inferred from the prompt or the domain, and the reasoning — or `none — everything user-stated`), **CHOSEN** (what was decided, with its rationale), **REJECTED** (what was considered and rejected, with the reason for each) — plus a Source tag per entry (USER-STATED / INFERRED / ASSUMED), the hours-left number (or the recorded hours-left assumption from step 2 if the user stopped answering before giving it), `### Risks`, accepted unknowns (each with an owner and a resolution point), rejected alternatives that matter, and `### Completion criteria`, plus one `Design direction:` line`

### E12 `new-skills/orchestrate/SKILL.md` — adaptivity paragraph (new, before step 4 "Build")

Old text: `4. **Build (expansion Phases 4–6 inside)** — implementers build the slices in parallel waves`
New text: the same line, preceded by:
`**Adapt to the idea — specified-ness sets the posture (fix #25 §4(f), ADAPT_F25).** The orchestrator and the design-lead adapt to the idea: its domain, its constraints, and how much the user specified — read from the decision record's Source tags (USER-STATED / INFERRED / ASSUMED, grill-me). A vague one-liner gets REASONING posture: the orchestrator and design-lead reason and gap-fill — infer the domain and its conventions, the user, the constraints, the demo, and the wow moment — and record every inference as INFERRED with its reasoning (see REASON_F25 below); a gap filled by inference is a stated inference, never a silent guess. A big prompt gets EXECUTION posture: execute the recorded decisions, do not re-ask them, do not re-derive them, do not re-open them — the decision record is the authority and a proposal that contradicts it loses to it. Between the poles, the posture follows the record: decide what is undecided, execute what is decided. The design-lead likewise adapts the direction to the idea's domain and constraints — the dealt theme and the design package bend to the product's job, never the other way round; a direction that fights the domain is re-dealt, not forced.`

### E13 `new-skills/orchestrate/SKILL.md` — reasoning-format rule (new paragraph after the Depth extension)

Old text: `a flat surface with a recorded `flat by choice — <reason>` satisfies the dimension.` + blank line + `**Body-only scope for the Tiempos rule (fix #20 — fix #19 F4 is body-only).**`
New text: the same Depth sentence, blank line, then the new paragraph, blank line, then the Body-only line:
`**Reasoning format — inferred / chosen / rejected (fix #25 §4(f), REASON_F25).** The D19 rule above is unchanged — the fix #19 D19 rule text is verbatim and stays byte-identical (verify19 asserts it as a substring). This line EXTENDS it: every decision-record entry now carries its reasoning as a mandatory three-part block — **INFERRED** (what was inferred from the prompt or the domain, and the reasoning behind the inference — or `none — everything user-stated` where nothing was inferred), **CHOSEN** (what was decided, with its rationale — the D19 reason lives here), **REJECTED** (what was considered and rejected, with the reason for each — never a blanket line). An inference recorded without its reasoning is a guess, not a decision; a rejection recorded without its reason is not a rejection. The three lines are checked by the step-2 reviewer and the step-5a static check (REASON_F25) — a static check on the record's presence, never a verdict on the reasoning's quality, which is the reviewer's and browser-qa's judgment.`
(This mirrors the established Depth-extension pattern: the frozen D19
paragraph itself was NOT edited — verified: the D19 sentence
"Every UI decision carries a thought-out reason across the FULL
experience" still appears exactly 1× in the file.)

### E14 `new-skills/feature-expansion/SKILL.md` — substance creativity

- Lens B: old text the Lens B paragraph; new text the same paragraph
  plus ` **Substance first (fix #25 §4(f), CREATIVE_F25):** every Lens B candidate names the technical approach it uses — the algorithm, data structure, system move, or data flow — in its Substance line (see the candidate shape below). A Lens B candidate whose substance is "none — UI-only" is not a depth candidate.`
- Lens D: old text the Lens D paragraph; new text the same paragraph
  plus ` The moment may be substantive — what the product DOES (a capability no other entry has) — not only how it looks; creativity applies to the product's behaviour, not only its surface.`
- Anti-pattern (new bullet after "No novelty chasing."):
  `- **No UI-only slate (fix #25 §4(f), CREATIVE_F25).** Creativity applies to what the product DOES, not only how it looks. A slate whose every candidate is UI-only — new screens, new polish, no new capability — is not a creative slate, however many candidates it holds. The balance check in Phase 2 enforces this: the shortlist must contain at least one substance item (see below).`
- Candidate shape: old text `- UI touched: [yes/no — which screen, if yes]`; new text the same line plus `- Substance: [the technical approach this feature uses — algorithm, data structure, system move, or data flow — or `none — UI-only`]`.
- Balance check: old text `3. **Check the balance.** The shortlist must contain at least one bold bet (Lens C) and at least one depth/quality item (Lens B).`; new text `3. **Check the balance.** The shortlist must contain at least one bold bet (Lens C), at least one depth/quality item (Lens B), and at least one substance item (fix #25 §4(f), CREATIVE_F25 — a feature whose value is what the product DOES: a named algorithm, data structure, system capability, or data flow, not how it looks).` (The shared-cap re-brainstorm round and terminal rule are unchanged — a missing substance item triggers the same one-round re-brainstorm as a missing bold bet / depth item.)
- Planner rubric: old text `**technical differentiation** (does it do something hard or novel, not a thin wrapper)`; new text `**technical differentiation** (does it do something hard or novel, not a thin wrapper — a 3 here requires a named algorithm, data structure, or system-design move, not just "uses an API")`.

## §5 Leg 2 benchmark definition (for the dry-run worker)

Leg 2 re-traces the SAME Campus Eats brief ("pretend I told you to
make a site" — no design direction; campus food-discovery landing for
Texas A&M students) under the current rules, by the dry-runs #25–#28
method: a paper re-trace through the updated skills, counting with the
BASELINE.md literal rule exactly (same kinds, same precedence, same
instances-count rule) — not a count of a rebuilt artifact, not an
assertion. Score per dimension against the §2 table in
`design-benchmark-v5.md` (reproduced here so the dry-run worker need
not re-derive it):

| # | Dimension | v5 figure | Beat-v5 pass criterion |
|---|---|---|---|
| 1 | Element count | 61 literal / 60 stricter | ≥ 62 literal AND ≥ 61 stricter |
| 2 | Variety | 7 kinds; Effect 0 | ≥ 7 kinds AND ≥ 2 kinds strictly above v5 counts; no nonzero v5 kind drops without a recorded D19 reason |
| 3 | Hero strength | Centred + entrance + app-frame + 1 moment applied; no hero loop recorded | Full v5 hero inventory AND (a) R4 hero loop applied OR (b) second dealt moment applied in/near hero. Strength verdict: browser-qa alone |
| 4 | Motion | 17 literal / 16 stricter | Motion ≥ 18 literal AND ≥ 17 stricter |
| 5 | Dynamic interface | 8 items; 1 cross-surface drive | ≥ 9 items AND ≥ 2 cross-surface drives. Live behaviour verdict: browser-qa alone |
| 6 | Functionality | 2 live-data surfaces | ≥ 3 live-data surfaces with real state; mechanism on hero/first screen. Live verdict: browser-qa alone |
| 7 | Alignment | NONE RECORDED | 0 problems across the full ALIGN_F23 matrix (COVER_F23). Verdict: browser-qa alone |

Pass = ALL SEVEN dimensions pass; a tie on any dimension fails that
dimension. Report a per-dimension table, not a single number. A
dimension that cannot be scored (statically or live) is recorded as a
gap / OWED, never as a pass. The old bands are superseded for this
purpose: fix #15 (+4 to +5, ≥4 kinds) and fix #17 (61 ± 2) — a
re-trace landing at 61 ties v5 and FAILS dimension 1. The Home Run
render re-run (dry-runs #38/#39 Leg 2) is unchanged by this fix and
still runs as its own leg item.

## §6 Leg 5 hard-idea fixture spec (for the dry-run worker)

Fixture idea (picked): **a real-time collaborative editor** — two or
more cursors editing the same document live, with presence, in the
browser, no page refresh.

Why it is hard (state it in the fixture brief): concurrent edits to
the same text must converge to the same document on every client
(conflict resolution, not last-write-wins); operations arrive out of
order and after disconnects (ordering + merge); presence (cursors,
selections) must track live without fighting the text sync; undo must
work across collaborators' interleaved edits; and it must stay
responsive while all of that happens. A thin version — one writer, or
a "collaborative" page that just polls and overwrites — is the quiet
re-scope this fix forbids; the fixture must show the hard parts, not
a demo that happens to run.

What the fixture build must show for the check to PASS (each with
evidence — running demo and/or test, not a description):

1. **Architecture** — named components + data flow: clients, sync
   channel (WebSocket or equivalent), op log / document store,
   presence channel; where state lives on each side and what happens
   when the channel drops.
2. **Algorithm / data-structure choice** — NAMED with why: a CRDT
   (e.g. a sequence CRDT / Yjs-style shared type) or OT with named
   transform functions — the choice, the invariant it preserves
   (convergence), and why it fits this document shape. "We sync the
   text" is not a choice.
3. **System design** — presence (cursor + selection per collaborator),
   persistence (document survives a reload), reconnect + merge (a
   client that goes offline and returns merges without losing edits),
   and permissions (who may edit) if the fixture claims them.
4. **Performance budget** — NAMED numbers, measured: keystroke to
   remote echo (target stated in the fixture brief, e.g. < 150 ms on
   localhost), op throughput under a burst (e.g. 100 ops), document
   size the fixture handles (e.g. 10k characters). A budget stated as
   an adjective ("fast") fails.
5. **Edge cases** — at least 3 named, each exercised, not just listed:
   simultaneous insert at the same position by two clients;
   offline-then-reconnect merge; undo of an edit interleaved with
   another collaborator's edit; a large paste while a collaborator
   types. The fixture brief picks its 3+; the check confirms each was
   exercised with evidence.

Alternatives considered and NOT picked (for the record): a
streaming-data pipeline (real-time ingest + windowing + backpressure
— hard, but its demo moment is a dashboard, and the check would lean
on numbers the dry-run cannot easily observe live); on-device
inference (model load + quantization + latency budget — hard, but
gated on model weights the sandbox may not have). The collaborative
editor was picked because concurrency + consistency + latency are
exercised directly in the demo (two clients, visible convergence),
with no external asset dependency.

Note on SPEC §5 wording: the technical-depth check sits in the
dry-run's Leg 5 (call-graph leg) per the SPEC; the dry-run worker
decides the exact leg placement if the call-graph leg's shape changes
— the fixture spec above is the check's content either way.

## §7 Verification of my own edits (re-read, not asserted)

- Every edit anchor was grepped count==1 before editing; post-edit
  anchor counts: `BENCHMARK_V5_F25` orchestrate 3 (bar paragraph,
  5a check, final-report line), polish-pass 2 (non-negotiable 5,
  variety pointer); `TECHDEPTH_F25` orchestrate 3 (5a check, step-4
  brief paragraph, final-report line), scope 2 (section + trap row),
  expansion 2 (brief item 8 + Phase 5); `ADAPT_F25` orchestrate 1,
  grill-me 1; `REASON_F25` orchestrate 3 (5a check, reasoning-format
  paragraph, ADAPT cross-reference), grill-me 1; `CREATIVE_F25`
  expansion 3 (Lens B, UI-only slate, balance check).
- Banned terms: grep for `claude|codex|anthropic|opus|sonnet|haiku|
  composer-2.5` across all six touched files returns 0 (the word
  "composer-tier" appears in orchestrate's pre-existing text and was
  not introduced by me — it is not a banned term).
- Grok pins untouched: no edit touches a model pin; pins remain
  `grok-4.7-high` / `cursor-grok-4.6-high-fast`.
- Frozen texts untouched: the fix #19 D19 paragraph is byte-identical
  (its lead sentence still 1×); the Depth-extension paragraph is
  byte-identical (its closing sentence still 1×); REASON_F25 was added
  as a NEW paragraph in the Depth-extension pattern, not an edit to a
  frozen paragraph. No `verify*.py` touched.
- Line counts after editing: orchestrate 380 → 387; feature-expansion
  210 → 213; grill-me 51 (inline appends only); hackathon-scope
  141 → 154; polish-pass 127 (inline appends only); new benchmark
  file 178 lines.
- `build.sh` NOT run; no rebuild; no loop run; `fix11/fix11-stage.py`
  NOT run. `/tmp` not used for test copies.

## §8 What I could not verify / what remains owed

1. **v5 figures are render-history figures, not live-measured ones.**
   The live Campus Eats v5 artifact is not in this workspace (only
   the v1-era tokens file). The counts, the kind split, and the
   iris-opens / hero-loop non-application are findings about what is
   RECORDED. A live re-measure against the real artifact would
   supersede them; until then the benchmark scores against them as
   written. The benchmark file states this caveat in full (§1).
2. **The dynamic-interface count of 8 is my enumeration** from prose
   descriptions in INVENTORY-V4.md / PARENT-GUIDANCE.md / dryrun28,
   not a live-source count. The dry-run worker must re-derive it from
   the same history and record any disagreement; the benchmark file
   says so explicitly.
3. **SPEC §4(d) parenthetical vs the record.** The SPEC says moments
   "letters-assemble + iris-opens" as if both were applied; the record
   shows iris-opens dealt but unapplied. I did NOT silently adopt the
   SPEC's reading: the benchmark records the discrepancy and makes
   applying iris-opens (or the hero loop) part of beating v5 on the
   hero dimension. Parent/coordinator to confirm this reading.
4. **"Motion/interactivity +10–15% over v4"** is the measured +13%
   v4 → v5 growth (total and Motion alike). INVENTORY-V4 flagged the
   v4 brief's own +10-15% label as inconsistent with the literal
   count; that flag is carried in the benchmark file, not smoothed
   over.
5. **Shipping of the new reference file** is by `build.sh:224`
   (whole `references/` dir copy) as read from build.sh — the actual
   built-tree copy is owed to the later build worker (no rebuild was
   run here). If the build step ever changes to an explicit file list,
   the benchmark file must be added to it.
6. **No fix25.py.** No upstream (non-staged) file needs a build-time
   patch for §4(d)–(f): browser-qa is upstream with no staged source,
   but the benchmark's live verdicts already sit inside its existing
   remit (F6 / AMBITION / memorability / hero / functionality /
   dynamic verdicts), so no browser-qa patch was written. If the
   coordinator wants an explicit browser-qa benchmark line, that is a
   follow-up for the weave worker, not something I invented here.
7. **Interaction with parallel workers.** My anchors are new tokens;
   the weave worker should check for collisions with the call-map
   worker's tokens and confirm the benchmark file is cited from the
   call map (design-package step). The verify25 worker must add checks
   for: the benchmark file's existence + its figures, the 5a static
   checks, the scope.md Technical-substance block, and the
   REASON_F25 three-line record format.
8. **Taste / ui-ux-pro-max were NOT edited.** The design-bar raise is
   wired through orchestrate + polish-pass only. If the weave worker
   finds a design-package step in Taste or ui-ux-pro-max that also
   needs the benchmark pointer (e.g. Taste step 4a / step 6), that is
   weave scope — flagged here, not done here, because those files are
   upstream-patched and outside my staged homes for this item.
