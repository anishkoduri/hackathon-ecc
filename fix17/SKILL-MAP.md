# Fix #17 — skill map (ANALYSIS ONLY)

Worker 2 of 3, plugin fix program #17. No plugin file edited, no build run,
Campus Eats untouched. All line numbers are in the **built tree**
(`~/workspace/hackathon-plugin/hackathon-ecc/skills/`) as read
Wed Nov 11, 2026, ~16:40 CST.

## Provisionality warning — read first

**Every anchor in this map is provisional pending fix #16's close.**
Fix #16 (Grok-only re-pin + Claude/Codex scrub) is concurrently editing
`build.sh` and staged sources while this map was written:

- `build.sh` is now **23,213 lines, md5 `42dd82b4…`** (fix #15 closed at
  23,217 lines, md5 `1f1a2325…`). Diff vs `build.sh.before-fix15` = **160
  non-equal opcodes**: the fix #15 57-line insert is still intact
  (now-lines 23146–23203) plus ~155 single-line replaces and one 4-line
  delete — consistent with fix #16's scrub, not fix #15 decay.
- Staged sources already carry fix #16 edits the built tree does not have
  yet: `new-skills/design-taste-frontend/SKILL.md` differs from built in
  11 lines (frontmatter scope tightening, lines 9–13: 5 lines staged vs 6
  built — **downstream Taste lines shift −1 on the next build**);
  `new-skills/orchestrate/SKILL.md` differs in 18 lines (Grok-only pins
  replacing `claude-opus-5` / `composer-2.5`, same line counts — no shift);
  `round2-skills/polish-pass/SKILL.md` differs in 8 lines
  (`design-taste-frontend` removed from its design-direction lists,
  single-line replaces — no shift).
- Fix #17's implementer **must re-anchor every line below after fix #16
  rebuilds**, and must re-run `fix15/verify15.py` (expect the two
  build.sh-diff checks to pass again once fix #16 closes and its own
  baseline is taken).

## Fix #15 verification result — built tree

- `fix15/verify15.py` re-run: **41/43 checks pass.** The 2 failures are
  ONLY the build.sh-diff checks (§8: "exactly one insert" / "the one
  insert is the 57-line fix15 block") — caused by fix #16's concurrent
  `build.sh` edits above, not by any fix #15 content loss. Every content
  check passes.
- **Manifest line anchors: 30/30 present at the claimed lines, 0 missing,
  0 drifted.**
  - Canonical variety + theme-match block: **11/11 files**, byte-identical
    (sha `f7e956a7a132`), count ×1 each, all at the manifest's claimed
    lines: Taste `:55`, ui-ux-pro-max `:16`, less-flat-ui `:16`,
    polish-pass `:45`, hallmark-floor `:20`, make-interfaces-feel-better
    `:15`, motion-foundations `:46`, motion-patterns `:43`,
    motion-advanced `:45`, orchestrate `:92`, orch-build-mvp `:42`.
  - R1: Taste step 4 `:244`, step-6 static check `:290`, orchestrate 5a
    `:61`, orch-build-mvp step 6 `:51`. R2: Taste §3 table `:153`.
    R3: less-flat-ui surface check `:14`. R4: Taste step 5 `:268`.
    R5: Taste step 4a `:246`.
  - C1: Taste step 4a `:246`, ui-ux-pro-max type-scale `:89`.
    C2: Taste step 4a `:246`. C3: Taste step 6 `:290`, polish-pass
    harmony `:22`.
  - D1: Taste step 6 `:310`; orchestrate step 5 `:60` + final-report
    `:66`; polish-pass Capture `:104`; orch-build-mvp step 6 `:51` +
    final-report `:59`.
  - Counts still **169/72/123/96/15**; less-flat-ui treatments still
    1–23; staged-vs-standalone less-flat-ui diff still exactly the 3
    fix #14 hunks; `gates.md` staged == staged source, no canonical
    block in it.
- Note: orch-build-mvp step 6 `:51` already hosts **two** fix #15 rules
  on one line (R1 static check + D1 rule) — see conflict C3 below.

## Placement table — fix #17 rules

Anchor lines are built-tree lines. "Primary" = where the rule is decided;
"Enforce / verify" = where it is counted or checked. One-line rule
statements are written as they would read in the skill.

### (a) Unique page-only elements — FORCE a few per build, invented for that page, never copied, theme-matched, enforced by a count

| Placement | Skill file | Anchor (built-tree line) | One-line rule as written |
|---|---|---|---|
| Primary — landing | `skills/design-taste-frontend/SKILL.md` | Step 4a anti-generic principles, `:246` (append as its own bold line after the paragraph, same pattern as R5) | "Every build carries at least 3 page-only elements — invented for this page through the package skills, never copied from a reference — each theme-matched and recorded per surface in `docs/design-tokens.md` with its kind; a build with none is incomplete (static check in step 6)." |
| Primary — app surfaces | `skills/ui-ux-pro-max/SKILL.md` | Anti-generic bar, `:93` | "Each primary app surface carries at least 1 page-only element (invented through this skill's styles/palettes/pairings, never a searched reference), recorded in `docs/design-tokens.md`; a surface with none is candidate evidence for `browser-qa`." |
| Count — app/dashboard | `skills/less-flat-ui/SKILL.md` | Surface check, `:14` (R3's home) + Record what you applied, `:528` | "Per screen, record the page-only elements alongside the treatments (surface → page-only elements, kind, theme-fit); a screen with none records `none — <reason>`." |
| Enforce | `skills/design-taste-frontend/SKILL.md` | Step 6 static check, `:290` (alongside R1) | Static check, not a screen verdict: the tokens file lists ≥3 page-only elements with kind + theme-fit, or the build is incomplete. |
| Enforce | `skills/orchestrate/SKILL.md` | Verify 5a, `:61` (alongside R1) | Same static check, orchestrate-side. |
| Enforce | `skills/orch-build-mvp/SKILL.md` | Step 6, `:51` (alongside R1 + D1) | Same static check, standalone-engine side. |
| Cite only | `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md` | 6-axis critique, Variety axis, `:80` | No edit: the Variety axis ("differs from the log") already scores difference-from-past-runs; cite it as the pre-emit cross-check for (a). |

Notes: no "unique / one-of-a-kind / page-only" language exists anywhere in
the 11 SKILL.md files today — this is new vocabulary; define "page-only"
in Taste step 4a when adding it. The count minimum ("a few") is
**undefined in the skills — fix #17 SPEC must fix the number; this map
proposes 3 per build (landing) / 1 per primary app surface**. Reuse the
existing record pattern (surface → elements, kind, theme-fit) with a
page-only flag; no new record file. Do NOT fold (a) into the canonical
block itself — it is verbatim ×11 and re-issuing it in 11 files for this
would be pure churn (see conflict C4).

### (b) Type filling bubble space — display/figure/label type sized to fill its bubble/card/tile, no dead space, bounded by no-overflow/no-crowding, verified in the step-6 screenshot check

| Placement | Skill file | Anchor (built-tree line) | One-line rule as written |
|---|---|---|---|
| Primary — landing | `skills/design-taste-frontend/SKILL.md` | Step 4a Typography, `:246` (own bold line after the paragraph — see conflict C1) | "Display, figure and label type is sized to fill its bubble, card or tile — no dead space inside the frame — bounded by no-overflow and no-crowding (measure, line-height and padding hold); checked in the step-6 screenshot QA." |
| Primary — app | `skills/ui-ux-pro-max/SKILL.md` | Step 2 type-scale, `:89` (C1's home) | Same rule, app surfaces: sizing decided by the dealt pairing / type scale, recorded per surface in the Type list. |
| Verify | `skills/design-taste-frontend/SKILL.md` | Step 6 D1 screenshot QA, `:310` | "The screenshot QA checks fill vs overflow/crowding on desktop + mobile captures: type that leaves dead space, overflows, or crowds is a fix-batch finding (browser-qa alone verdicts)." |
| Verify only | `skills/polish-pass/SKILL.md` | Typeset lens, `:56` + harmony check, `:22` | "The typeset lens checks fill (dead space inside bubbles/cards/tiles) against the recorded Type list — consistency only, never a verdict." |

Notes: **no existing anchor.** No "bubble / dead space / fill" type-sizing
language exists in any of the 11 SKILL.md files (the only "bubble" hit is
less-flat-ui `:431`, a soap-bubble texture variant — unrelated). This is a
new sub-rule, not an extension of an existing one. Adjacent but NOT the
home: make-interfaces-feel-better Text Wrapping, `:51` (wrapping rules,
not sizing — cite as a bound). Overflow/crowding bounds already have
checkers (consistency.mjs collide / off-viewport, Taste §5 Checklist) —
the rule must name the step-6 screenshot check as the arbiter and state
browser-qa alone verdicts.

### (c) Font decisions through the skill — every face/weight/size/tracking choice cites the skills' type system, no default or flat choice, enforced and recorded per surface in the Type list

| Placement | Skill file | Anchor (built-tree line) | One-line rule as written |
|---|---|---|---|
| Primary — landing | `skills/design-taste-frontend/SKILL.md` | Step 4a Typography, `:246` (C1/C2's home — see conflict C1) | "Every face, weight, size and tracking choice cites the skills' type system (dealt pairing + type scale, recorded in `docs/design-tokens.md`) — no default, unchosen or flat choice; each surface's choices are recorded per surface in the Type list (surface → face/weight/size/tracking/measure/contrast)." |
| Primary — app | `skills/ui-ux-pro-max/SKILL.md` | Step 2 type-scale, `:89` (C1's home) | Same rule, app surfaces: the `--design-system` pairing/scale is the cited source for every face/weight/size/tracking choice. |
| Enforce | `skills/design-taste-frontend/SKILL.md` | Step 6, `:290` (C3's home) | Extend the C3 line: copy + type checks enforced and recorded — now including weight/tracking per surface. |
| Verify only | `skills/polish-pass/SKILL.md` | Harmony check, `:22` (C3's home) | Extend the C3 verification: the harmony check verifies the Type list including weight/tracking traceability — consistency only, never a verdict. |

Notes: (c) is the generalisation of fix #15 C1 (faces only) + C3 (Type
list recorded) to weight/size/tracking. **No new record format needed:**
extend the existing Type list (surface → face/size/measure/contrast) with
weight/tracking columns. Follow the C1 split precedent: the rule goes in
BOTH Taste step 4a (landing) and ui-ux-pro-max Step 2 (app) and the two
must stay in sync. Cited bounds: hallmark-floor rule 9 (tracked-capitals
ban) and rule 1 (tokens) — cite, don't edit.

### (d) Motion/interactivity density — v4-level motion set as default: scroll entrances with a 1500ms fail-safe, hover micro-interactions, life in existing pieces, ≥1 small interactive bit per page where the page has one — routed through the motion skills, reduced-motion respected

| Placement | Skill file | Anchor (built-tree line) | One-line rule as written |
|---|---|---|---|
| Primary — mechanism | `skills/motion-patterns/SKILL.md` | Rules, `:45`–`:55` (add rule 9) + Scroll reveal example, `:254` | "Every scroll entrance carries a 1500ms fail-safe: if the reveal has not fired within 1500ms of the element entering the viewport, the content is shown anyway — nothing ever stays hidden because an observer never fired." |
| Primary — mechanism | `skills/motion-foundations/SKILL.md` | Rules, `:48`–`:60` (add rule 9) + Accessibility, `:168` | "All reveals resolve within 1500ms (fail-safe); under reduced motion the fail-safe still reveals, opacity-only ≤0.2s (rule 3 governs)." |
| Primary — implementation | `skills/motion-advanced/SKILL.md` | `useScrollReveal` hook, `:315`–`:336` | Implement the fail-safe in the hook (the shared implementation point for scroll reveals). |
| Primary — feel/routing | `skills/make-interfaces-feel-better/SKILL.md` | Motion, `:93`–`:107` + Checklist, `:141`–`:153` | "Default motion set (v4-level): scroll entrances (1500ms fail-safe), hover micro-interactions on every interactive element, life in existing pieces (loops, counts, live states) — decided here for feel/timing, implemented with the motion-* skills." |
| Density floor — landing | `skills/design-taste-frontend/SKILL.md` | House rule 5, `:35`–`:38` (hover already mandated) + step 4a motion line, `:246` | "House rule 5 extends: every page carries the default motion set — scroll entrances, hover micro-interactions, life in existing pieces — and at least one small interactive bit per page where the page has one (a control, toggle, loop or live piece the user can act on)." |
| Enforce (count) | `skills/design-taste-frontend/SKILL.md` | Step 6 static check, `:290` | Static check: the tokens file records the per-page interactive bit (or `none — <reason>` where the page has none); a page with an interactive bit that never got one is incomplete. |
| Enforce (count) | `skills/orchestrate/SKILL.md` / `skills/orch-build-mvp/SKILL.md` | Orchestrate 5a, `:61` / mvp step 6, `:51` | Same static check, engine-side. |
| Route | `skills/orchestrate/SKILL.md` | Design-package rule, `:90` (motion work row already names `make-interfaces-feel-better`) | No new line needed: the existing routing (motion work → make-interfaces-feel-better → motion-*) already covers (d); the rule text there should cite the 1500ms fail-safe by name. |

Notes: **the 1500ms fail-safe is new** — no `1500` / `fail-safe` / `failsafe`
appears in any of the 11 SKILL.md files (the only `1500` hits tree-wide
are asset files). The hook + pattern example are where the number must
live as code; the Rules sections are where it must live as law.
**"v4-level motion set" is undefined in the skills** — fix #17 SPEC must
enumerate the set (this map proposes: scroll entrances + hover
micro-interactions + life in existing pieces + ≥1 interactive bit) or
point at a concrete reference (Taste `motion.md`); do not ship the phrase
bare. Reduced-motion bounds already exist (motion-foundations rule 3 +
Accessibility `:168`, Taste §5 Checklist Motion bullet, §6 Never) — (d)
adds to them, never weakens them. "Where the page has one" needs a
record convention: `none — <reason>` in the tokens file, mirroring R3's
`none — <reason>` for untreated surfaces.

### (e) Creative freedom within reason — the design-lead MAY invent page-specific elements within reason, bounded by theme-match, craft floor, Hallmark floor, no violet, anti-derivative, browser-qa's verdict

| Placement | Skill file | Anchor (built-tree line) | One-line rule as written |
|---|---|---|---|
| Primary — permission | `skills/orchestrate/SKILL.md` | Design-package rule, `:90` + "Routing — every design decision goes through the package", `:98` | "The design-lead MAY invent page-specific elements — a new moment, type treatment, component or interaction built for this page only — within reason: it traces to the dealt theme, passes the craft floor and the Hallmark floor, uses no violet, is never based on a searched reference, and stands or falls on `browser-qa`'s verdict." |
| Primary — build time | `skills/design-taste-frontend/SKILL.md` | Step 4a anti-generic principles, `:246` | "Invention is a step-4a decision: anything the deal did not fix, the lead may invent for this page — within the bounds in orchestrate's design-package rule — and records it per surface in `docs/design-tokens.md` with the deciding skill named." |
| Primary — app | `skills/ui-ux-pro-max/SKILL.md` | "Generated direction — never based on a searched reference" (~`:91`) + Anti-generic bar, `:93` | Same permission, app surfaces: invented elements are generated through this skill's own styles/palettes/pairings, never from a searched reference. |
| Bound | `skills/design-taste-frontend/SKILL.md` | §6 Never, `:396`–`:409` | No edit: the Never list (incl. violet `:404`, copying a reference) is already the hard bound on invention; cite it. |
| Bound | `skills/orchestrate/SKILL.md` | "Posture — more, not bolder", `:94` + anti-derivative rule, `:96` | No edit: cite both as bounds — invention is "more", never "bolder for its own sake", and never derivative. |
| Cite only | `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md` | 6-axis pre-emit critique, `:62`–`:81` | No edit: use the critique (Philosophy / Hierarchy / Execution / Restraint axes) as the pre-emit "within reason" test. Do NOT add permission language to the floor — its 16 rules are non-waivable. |

**What counts as "within reason" (proposed definition for fix #17 SPEC to
ratify):** an invented element is within reason iff ALL five hold —
(1) theme-matched (canonical block: material, tokens, palette balance,
do-nots); (2) passes the craft floor and the Hallmark floor bans
(including no violet, no purple-blue gradient, no card-in-card, no emoji
icon); (3) not based on a searched reference (anti-derivative); (4)
recorded per surface in `docs/design-tokens.md` with the deciding skill
named; (5) survives `browser-qa`'s verdict (candidate evidence, never
self-verdict). Fails any one → not within reason → cut or re-dealt.

## Placement conflicts

- **C1 — Taste `:246` pile-up (biggest).** Step 4a is one enormous line
  that already hosts R5, C1 and C2. Rules (b), (c) and (e) all want it
  too. Do NOT keep appending long sentences into the same line.
  Recommendation: split step 4a into one bold line per decision
  (typography / colour / spacing / components / nav / responsive /
  motion / a11y / states) with the fix #15 + #17 sentences as short
  lines under their decision — or, minimum, append each fix #17 rule as
  its own bold line immediately after `:246`, the way R5 was appended.
- **C2 — Taste step 6 `:290` pile-up.** Already hosts the R1 static check
  + C3. Rules (a) count check, (b) screenshot fill verification and (d)
  density count all want step 6. Recommendation: consolidate into one
  "Step-6 static checks" list (R1 applied/re-dealt; (a) page-only count;
  (c) Type list incl. weight/tracking; (d) per-page interactive bit)
  instead of four separate sentences; the D1 screenshot rule at `:310`
  stays the verification home for (b).
- **C3 — orch-build-mvp step 6 `:51` already hosts two rules** (R1 + D1)
  on one line; (a) and (d) checks would make it three (orchestrate 5a
  `:61` + D1 `:60` are the same pattern). Same consolidation
  recommendation as C2; do not grow the line further.
- **C4 — Canonical block is verbatim ×11.** Rule (a) must NOT be folded
  into the canonical block — that would force an 11-file re-issue and
  re-verification for a rule that only needs Taste + less-flat-ui +
  orchestrate homes. Attach (a) as a separate line after the block.
- **C5 — polish-pass scope.** Polish never restyles, never invents, never
  adds motion. Rules (a)/(b)/(c) get verification-only lines there
  (harmony `:22`, typeset lens `:56`); rule (e) gets nothing there
  (invention is build-time only); rule (d) gets nothing there beyond
  fixing broken feedback motion (already in scope). Any placement that
  asks polish-pass to decide a look is a scope violation.
- **C6 — Motion skills have no page/count concept.** Rule (d)'s per-page
  minimum cannot live in motion-* (they define patterns, not pages);
  it needs Taste/orchestrate enforcement. Conversely Taste step 6 cannot
  define the fail-safe mechanism — that lives in motion-patterns /
  motion-foundations / the `useScrollReveal` hook. Both halves are
  required; neither alone suffices.
- **C7 — less-flat-ui scope.** Texture only, on surfaces the page system
  leaves unstyled (Taste §1 texture boundary). Rule (a) on landing pages
  belongs to Taste/moments, not less-flat-ui; less-flat-ui gets the
  app/dashboard count only (same scoping as R3).
- **C8 — hallmark-floor.md is a floor, not a permission slip.** Cite it as
  a bound for (a) (Variety axis `:80`) and (e) (6-axis critique); do not
  add "may invent" language to a file whose 16 rules are non-waivable.
- **C9 — ui-ux-pro-max vs Taste duplication (C1 precedent).** Rules (b)
  and (c) need both homes (landing vs app) and must stay in sync; the
  single source of truth remains `docs/design-tokens.md` (Type list).
- **C10 — Two undefined terms need SPEC numbers.** "A few" in (a):
  propose 3 per build / 1 per primary app surface. "V4-level motion set"
  in (d): propose the enumerated set in (d)'s table, or a pointer to
  Taste `motion.md`. Neither phrase should ship bare.
- **C11 — Conflict C1's fix in the staged sources.** Note that fix #16's
  staged Taste frontmatter change shortens the file by 1 line above
  `:246`, so the `:246` anchor will read as `:245` after rebuild — the
  implementer re-anchors anyway per the provisionality warning.

## Skills with no fix #17 placement

- `motion-foundations` / `motion-patterns` / `motion-advanced`: (d) only.
- `make-interfaces-feel-better`: (d) only (plus (b) bounds cited at `:51`).
- `less-flat-ui`: (a) count only (app/dashboard scope).
- `hallmark-floor.md`: cited as a bound for (a) and (e); no rule text
  added.
- `polish-pass`: verification-only lines for (a)/(b)/(c); nothing for
  (d)/(e) beyond existing scope.
