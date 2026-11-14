# Fix #20 — SPEC: Tiempos is body-only, important text gets a unique important font, impressive is the bar

## 0. Goal

Refine the scope of fix #19's font rules so a future build cannot use the
body face for important text, cannot set important text in anything but a
unique, important display face, and cannot be rule-correct yet unimpressive
— the design just has to be impressive, and that is the governing bar. It also instills branding (every build carries a distinct brand identity, recorded in the decision record) and the component-as-experience rule (each component is designed as a moment/interaction, with its experience stated in its recorded reasoning alongside the six D19 dimensions). It also weaves the whole design-decision rule set into every applicable skill at its decision points (§10), so the agent applies the rules subconsciously when deciding, rather than having to deliberately remember to consult a separate rule file.

Anish's refinement (Nov 11 evening, his words): "The rule of that font is
just for basic text, anything that's supposed to be important should be a
unique important font, and most of all the design just has to be
impressive."

Gate (verified before writing this SPEC): `fix19/MANIFEST.md` exists;
`build.sh` is 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`
(post-fix19). Checker numbers entering fix #20: Audit #61 CLEAN (0/0),
dry-run #30 PASS, sweep #24 CLEAN; verify15 43/43, verify17 59/59,
verify18 72/72, verify19 75/75. Counts 166 skills / 72 agents / 123 rules /
87 commands / 15 hooks.

## 1. Evidence — the gap fix #19 left open

Fix #19's F4 says body/plain text uses Tiempos (or the Fraunces
stand-in) — but it never states the scope: it does not say the body face
is for basic text ONLY, and it does not forbid using the body face for
important text. A build could set its headings, hero lines, and calls to
action in Fraunces and be fully F4-compliant — that is the leak this fix
closes. The Campus Eats repair's final pairing complies with the refined
scope: Bowlby One SC for display/important text, Fraunces for body text
only — display face for what matters, body face for basic text.

Measured data (Nov 11, post-fix19 built tree):

- Exactly ONE theme file names the same face for display and body:
  `vantage.md:29` — `--font-display: "Geologica"; --font-body:
  "Geologica";`. Every other theme (50 of 51) names distinct faces
  (e.g. sticker.md: display "Bowlby One SC", body "Sofia Sans").
  The vantage collision is the scope rule's live case: the rule governs
  the DEAL (re-deal a distinct display face, or record a scoped
  exception), not the theme file — theme files are reference data, not
  delivery instructions (fix #19 precedent, SPEC §5).
- Zero theme files name Fraunces as a body face — the stand-in is a
  build-time choice, not a theme voice.
- One staged source DOES deal a body-stand-in family as the display
  face: Taste's type catalogue pairing `fraunces` (`library/type.json`,
  display Fraunces, text Figtree) — a live, dealable path (fix #19's
  live run dealt it, per fix19/sweep24-report.md). Sweep #25 caught
  this: read literally, F4_SCOPE's "NEVER used for important text"
  forbids it. Resolution (fix-up, Nov 12): the scope rule binds the
  face IN ITS ROLE as the body/reading face — a pairing that deals
  Fraunces as the display face, with a different face as body, is
  governed by F3/F5, not F4. F4_SCOPE now carries that role-scoping
  sentence; the pairing stays. The leak fix #20 closes remains the
  absence of a scope statement for the body face.
- Sweep #25 also found the Hallmark gates (gates 64/67, hallmark-floor
  rule 9) prescribe the body face for labels/captions/table heads/nav
  links/tags/chips while F5 says "key labels" use the display face,
  with "key label" undefined. Resolution: F5 now defines "key label"
  (a label meant to stand out — featured
  section label, emphasis badge, price label); ordinary small labels follow the
  Hallmark gates in the body face.

Anish's follow-up (same evening, folded into this program, not a separate one): instill BRANDING — every build must carry a distinct brand identity, the product's own brand (wordmark, identity tokens, voice), recorded in the decision record, not a generic template look; the brand is the through-line, and every surface, component, and decision expresses it. And every COMPONENT is an EXPERIENCE — each component is designed as a moment/interaction, not a static functional block, and its recorded reasoning states what experience it creates (what it feels like, what moment it is) alongside the six D19 dimensions. Both rules have existing hooks: Taste step 4a already defines a visual identity and a component hierarchy — these rules make them required, recorded, and checked, not optional.

## 2. Rules

### F4_SCOPE — the Tiempos rule is body-only (fix #20, scopes fix #19 F4)

F4_SCOPE = """**Body-only scope for the Tiempos rule (fix #20 — fix #19 F4 is body-only).** Tiempos and the Fraunces stand-in are for BASIC text only — body copy and plain reading text. They are NEVER used for important text. This binds each face in its role as the body/reading face: when Tiempos/Fraunces is the body face, it is never used for important text. A pairing that deals Fraunces (or Tiempos) as the *display* face, with a different face as the body face — for example the `fraunces` pairing in Taste's type catalogue (display Fraunces, Figtree body) — is governed by fix #19 F3 / fix #20 F5, not by this scope rule: on that build the face is the display face, not the body stand-in. Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses the display face (fix #20 F5), never the body face. A build that sets a heading, hero line, call to action, or key label in the body face is an incomplete build — a static check item in step 6, never a screen verdict. Boundary: fix #19 F3 governs the display/important face; fix #19 F4 governs basic text only. A face is either the display face (important text) or the body face (basic text), never both on the same build — except a scoped, recorded exception under this scope rule. Where a dealt theme names the same face for display and body, the design-lead deals a distinct display face and records it in `docs/design-tokens.md`; keeping the collision is a scoped, recorded exception with a fix #19 D19 reason AND the impressive-bar justification (fix #20 F6) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback)."""

### F5 — Important text uses a unique, important font

F5 = """**Important text uses a unique, important font (fix #20 F5).** Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses a UNIQUE, IMPORTANT font: a distinctive display face, chosen through the design skills (the dealt display face in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with its fix #19 D19 reason and its impressive-bar justification (fix #20 F6). Not the body face, not a generic/system font. A 'key label' is a label meant to stand out — a featured section label, an emphasis badge or price label. Ordinary small labels — nav links, table heads, captions, chips, form labels, meta rows — follow the Hallmark gates: the body face, a step smaller, sentence case, untracked. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2). A build that sets important text in the body face, or in a generic/system font, is an incomplete build — a static check item in step 6, never a screen verdict."""

### F6 — The design just has to be impressive (the governing bar)

F6 = """**The design just has to be impressive (fix #20 F6 — the governing bar).** The font rules serve this standard; a font choice that is correct per the rules but leaves the design unimpressive still fails. The finish review judges impressiveness as a verdict — browser-qa's visual verdict on the rendered screens, never a static check — and the decision record must state, for the important font on each surface, why it is the impressive choice for that surface (what makes it stand out, what it beats, why this surface earns it). A decision record that cannot say why the important font is impressive is an incomplete build. This bar connects to, and does not replace, the existing posture: more-not-bolder (fix #13), the E1 creativity push (trailblazing, not dumb), and fix #19 D19 (the six-dimension reason). A design that is rule-correct but unimpressive fails at the finish review; a design that is impressive but breaks a ban still fails — the bar governs, the bans bind."""

### Fix #20 static checks (mirrors fix #19 STATIC19)

STATIC20 = """**Fix #20 static checks (all static checks, never screen verdicts).** (F4 scope) The Type list marks the body face as body-only — the body face is the face serving as body/reading text on that build, so a pairing that deals Fraunces as the display face (with a different body face) is checked under F5, not here; no heading, display, hero, call-to-action, or key-label token points at the body face; a dealt theme naming the same face for display and body is either re-dealt with a distinct display face or recorded as a scoped exception with a fix #19 D19 reason and a fix #20 F6 justification. (F5) Every important-text token points at the display face; the display face is recorded with its fix #19 D19 reason and its fix #20 F6 justification; a build setting important text in the body face or a generic/system font is an incomplete build. (F6 record) The decision record states, for the important font on each surface, why it is the impressive choice for that surface; a record that cannot say so is an incomplete build. (F6 verdict) The impressiveness verdict itself is browser-qa's at the finish review, never a static check. (B1) The decision record names the build's brand identity (wordmark, identity tokens, voice); a build with no recorded brand identity is an incomplete build. (X1) Every component entry in the decision record states the experience it creates (what it feels like, what moment it is) alongside the six D19 dimension lines; a component recorded only as a functional block is an incomplete build."""

### B1 — Every build carries a distinct brand identity

B1 = """**Every build carries a distinct brand identity (fix #20 B1).** The build carries the product's own brand — its wordmark, its identity tokens (the name, the mark, the voice, the palette and type that are its own), and its voice — recorded in the decision record (`docs/design-tokens.md` / MASTER.md on app surfaces). The brand is the through-line: every surface, component, and decision expresses it. A build with no recorded brand identity — no wordmark, no identity tokens, no voice on the record — is an incomplete build — a static check item in step 6, never a screen verdict. The brand is generated through the skills (the dealt direction in Taste step 4a / the ui-ux-pro-max identity), never inherited from a template; a build that reads as a generic template has, by definition, no brand. When a project already has a brand (a real product, a real wordmark), the record names it and the build conforms to it; when it does not, the build deals one and records it."""

### X1 — Every component is an experience

X1 = """**Every component is an experience (fix #20 X1).** Each component is designed as a moment/interaction, not a static functional block. Every component entry in the decision record states the experience it creates — what it feels like, what moment it is — alongside its six fix #19 D19 dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors). A component recorded only as a functional block ("a card that shows X", "a list of items") with no experience statement is an incomplete build — a static check item in step 6, never a screen verdict. The experience statement is the component's own: what the user feels using it, what moment it stages, what it does that a static block would not. A component with no interactive or felt quality records that explicitly (`no felt moment — <reason>`, e.g. a legally-required static notice) — an explicit none, never a missing line."""

### App mirrors (fix #20 F4_SCOPE / F5 / F6 / B1 / X1 on app surfaces)

F4_SCOPE_APP = """**Body-only scope for the Tiempos rule (fix #20 — F4 is body-only, app surfaces).** On app surfaces, Tiempos and the Fraunces stand-in are for basic text only — body copy and plain reading text, never important text. Headings, display type, hero text, emphasis, key labels, and calls to action use the display face (fix #20 F5). Role-scoped (fix #20 fix-up): this binds the face as the body face; a pairing that deals Fraunces as the display face, with a different face as body, is governed by F3/F5, not by this scope rule. The full scope rule lives in `design-taste-frontend` step 4a."""

F5_APP = """**Important text uses a unique, important font (fix #20 F5, app surfaces).** On app surfaces, anything supposed to be important uses a unique, important display face, chosen through this skill's type scale and recorded in MASTER.md with its fix #19 D19 reason and its fix #20 F6 justification — never the body face, never a generic/system font. A 'key label' is a label meant to stand out (featured section label, emphasis badge, price label); ordinary small labels follow the Hallmark gates in the body face. The full F5 rule lives in `design-taste-frontend` step 4a."""

F6_APP = """**The design just has to be impressive (fix #20 F6, app surfaces).** On app surfaces, a font choice that is correct per the rules but leaves the design unimpressive still fails; the finish review (browser-qa's visual verdict) judges impressiveness, and MASTER.md states why the important font is the impressive choice for each surface. The full F6 rule lives in `design-taste-frontend` step 4a."""

B1_APP = """**Every build carries a distinct brand identity (fix #20 B1, app surfaces).** On app surfaces, the build carries the product's own brand — wordmark, identity tokens, voice — recorded in MASTER.md; every surface, component, and decision expresses it. A build with no recorded brand identity is an incomplete build. The full B1 rule lives in `design-taste-frontend` step 4a."""

X1_APP = """**Every component is an experience (fix #20 X1, app surfaces).** On app surfaces, each component is designed as a moment/interaction, not a static functional block; every component entry in MASTER.md states the experience it creates (what it feels like, what moment it is) alongside its six fix #19 D19 dimension lines. A component recorded only as a functional block is an incomplete build. The full X1 rule lives in `design-taste-frontend` step 4a."""

### Typeset lens (polish-pass)

TYPESET_F20 = """**Body-only scope; important text gets the display face (fix #20).** The body face (Tiempos or the Fraunces stand-in) is for basic text only — a heading, hero line, call to action, or key label set in the body face is a finding. Important text uses the dealt display face; check the Type list for the face's fix #19 D19 reason and its fix #20 F6 justification (why it is the impressive choice for that surface) — a display face with no recorded justification is a finding. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size."""

TYPESET_CHECKBOX20 (replaces the fix #19 checkbox in the typeset lens):
Old: "- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2)."
New: "- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for basic text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20)."

### Polish-pass harmony

POLISH_F20 (appended after POLISH_F19 in the harmony check):
" The harmony check also verifies the font scope (fix #20): each Type-list body-face row is marked body-only, and no heading, display, hero, call-to-action, or key-label token points at the body face — a token that does is a harmony divergence, recorded as candidate evidence, never a verdict. It also verifies the important font's record (fix #20 F5/F6): the display face is recorded with its fix #19 D19 reason and its fix #20 F6 justification (why it is the impressive choice for that surface) — consistency only, never a verdict. It also verifies the brand identity is recorded (fix #20 B1) and each component entry states the experience it creates (fix #20 X1) — consistency only, never a verdict."

## 3. Placement (fix #15 / fix #17 / fix #19 pattern)

The canonical variety + theme-match block is NOT modified (verify15.py's
verbatim check must keep passing — the block stays verbatim ×1 in all 11
files). The fix20 rules are placed as new bold rules adjacent to the fix19
rules, mirroring fix19's placement. One source of truth; build.sh patches
where the built tree needs them. The implementation engine MUST NOT edit
any fix19 rule text in place — F2/F3/F4/D19/F2_APP/F3_APP/F4_APP/D19_APP
and STATIC19 are verify19 anchors (full-text `in` checks); fix20 appends
new rules after them and asserts the old ones are still present verbatim.

### Staged sources (edited directly; build.sh copies them verbatim)

| # | File | Change |
|---|---|---|
| 1 | `new-skills/design-taste-frontend/SKILL.md` (step 4a) | Append F4_SCOPE + F5 + F6 + B1 + X1 after the D19 rule. Anchor: the D19 ending "the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check." (count==1 in this file). |
| 2 | Taste step 6 | Append STATIC20 after STATIC19. Anchor: the STATIC19 paragraph (count==1 in this file); STATIC20 sits after the fix19 checks. |
| 3 | `new-skills/orchestrate/SKILL.md` (design-package rule) | Append F4_SCOPE + F5 + F6 + B1 + X1 after the D19 rule. Anchor: the D19 ending (count==1 in this file). |
| 4 | orchestrate Verify 5a | Append STATIC20 after STATIC19. Per the fix19 deviation-3 precedent: append after the 5a paragraph's final sentence (NOT after the two-line "…5b. Final polish" anchor) and assert it sits before the 5b bullet. |
| 5 | `round2-skills/polish-pass/SKILL.md` (harmony) | Append POLISH_F20 (now including the B1/X1 sentence) after POLISH_F19. Anchor: the POLISH_F19 ending "consistency only, never a verdict." (count==1 in this file). |
| 6 | `round2-skills/polish-pass/reference/lenses/typeset.md` | Append TYPESET_F20 after TYPESET_F19 (anchor: the TYPESET_F19 tail "font-optical-sizing: auto" — count==1); replace the fix19 checkbox with TYPESET_CHECKBOX20 (old text at line 74, count==1). |

### build.sh patch block (upstream, no staged source)

| # | File (built) | Change |
|---|---|---|
| 7 | `skills/ui-ux-pro-max/SKILL.md` | Append F4_SCOPE_APP + F5_APP + F6_APP + B1_APP + X1_APP after D19_APP (anti-generic bar area). NOTE: D19_APP occurs TWICE in build.sh (once per patched file) — anchor within this file's patch block, never a bare build.sh-wide count. |
| 8 | `skills/orch-build-mvp/SKILL.md` | Append F4_SCOPE_APP + F5_APP + F6_APP + B1_APP + X1_APP after D19_APP (step 4, within this file's patch block); append STATIC20 in step 6 after STATIC19 (STATIC19 occurs once in build.sh — the orch-build-mvp patch). |

Weaving placements are governed by §10 (the census decides the skill list; the weave table is recorded in the manifest, not in this §3 table).

## 4. What the canonical block does NOT get

The canonical variety + theme-match block stays verbatim ×1 in all 11
files (verify15.py must keep passing 43/43). Do not append the fix20
rules INTO the block. The motion-* skills, make-interfaces-feel-better,
and hallmark-floor.md get no direct fix20 edit: their entries are covered
by the record-level D19/F6 checks, and they do not decide fonts. No
Verify-step-5 edit: the visual loop's giant line is not touched — F6's
verdict instruction lives in the design-package rule (which the loop reads
as its direction) and the STATIC20 record check is the static side; the
loop already executes verdicts per that direction, and browser-qa's
existing distinctiveness bar (a surface that reads as a default template
fails) is the verdict the impressive bar extends. If the audit finds a
motion skill deciding a font, that is a finding for the audit, not a new
edit in this fix.

## 5. Conflicts resolved in this SPEC

- **Typeset lens check #4 vs F5.** The lens asks "Are display or script
  faces used in buttons, labels, inputs, or data?" as a smell — and F5
  says key labels and calls to action (small text) use the display face.
  NOT a contradiction: F5 governs WHICH face (display, not body) for
  important text; the lens's check #4 governs HOW (scale, weight,
  tracking — a display face set badly in a label is a finding, but the
  face choice itself follows F5). A sticker-style pill button set in the
  dealt display face at the right scale is exactly the intended outcome.
  Recorded as a resolved tension, not a defect.
- **vantage.md display == body (Geologica).** Theme files are reference
  data, not delivery instructions (fix #19 precedent). NOT edited: the
  scope rule governs the DEAL — re-deal a distinct display face, or
  record a scoped exception with a D19 reason + F6 justification. The
  dry-run uses vantage.md as its collision demonstration (§6).
- **F3 vs F4 boundary.** F3 governs the display/important face; F4
  governs basic text only — stated in F4_SCOPE. The two rules never
  fight: a face is either the display face or the body face, never both
  on the same build, except a scoped, recorded exception under the scope
  rule. Where a theme's body or display face conflicts with this scope,
  the scope rule decides.
- **Banned tokens in rule text.** The phrases naming the font's owner
  and the product whose reading text it sets are banned tokens under the
  fix #16 scrub — the fix20 rule constants use "Tiempos" and "Fraunces
  (stand-in for Tiempos)" only, as fix #19 did. The engine's preflight
  MUST scan every added text for banned tokens (claude, codex,
  anthropic, opus, sonnet, haiku, composer-2.5) and fail before any
  edit if one is present.
- **B1 vs the anti-generic bar.** Complementary, not conflicting: the bar (browser-qa's visual-loop verdict — a surface that reads as a default template fails) judges the RESULT; B1 supplies the identity that makes the result possible. A build cannot pass the bar without a brand, and a recorded brand that is never expressed on any surface is a D19 failure (the record must match what was built). No contradiction.
- **X1 vs the motion rules (M1–M6) and dealt moments (R1).** Complementary: a component-as-experience is expressed through motion (entrances, hovers, loops) and through dealt moments; X1 does not add a motion requirement beyond M1–M6 — it adds the RECORDED experience statement. A component with no motion records its experience in still terms (what it feels like at rest, what moment it stages) or an explicit `no felt moment — <reason>`.

## 6. Dry-run — dry-run #31

The dry-run is a font-scope + impressive-bar check, not an element
recount. PASS requires all of:

1. **Rule presence:** verify20.py passes (see §7).
2. **Criteria coverage:** every scope token — body face never for
   important text, important text uses the display face, display==body
   collision handled (re-deal or scoped exception), the F6 record
   (impressive-choice justification per surface) — is named as a check
   trigger in the STATIC20 text.
3. **Repair compliance (repair-reported):** the repaired Campus Eats
   artifact complies with the refined scope — Bowlby One SC for
   display/important text, Fraunces for body text only — per the
   repair's verified solution. The workspace tokens file is v1-era/stale
   and is NOT evidence of the repair.
4. **Negative demonstration (scope leak):** a fixture Type list with a
   heading token pointing at "Fraunces (stand-in for Tiempos)" FAILS
   the F4-scope check — proving the check fires on the leak.
5. **Negative demonstration (collision):** the vantage.md tokens
   (display == body == Geologica) FAIL the scope check as dealt, and
   PASS under both compliant paths (a re-dealt distinct display face;
   a scoped exception with a D19 reason + F6 justification) — proving
   the check fires on the collision and accepts the two cures.
6. **Negative demonstration (impressive bar):** a fixture decision
   record for an important font with a D19 reason but NO impressive-
   choice justification FAILS the F6-record check; the same record WITH
   the justification PASSES — proving the check fires on the missing
   justification, not on the reason's presence alone.
7. **Criteria coverage (F6 verdict):** the verdict mechanism
   (browser-qa's finish visual verdict, never a static check) is named
   in the F6 rule text, and the static/record side (STATIC20's F6
   record item) is named separately — proving the two halves are not
   conflated.
8. **Negative demonstration (branding):** a fixture decision record with no brand identity (no wordmark, no identity tokens, no voice) FAILS the B1 check — proving the check fires on a missing brand.
9. **Negative demonstration (component):** a fixture component entry recorded only as a functional block ("a card that shows three items") with no experience statement FAILS the X1 check; the same entry WITH an experience statement ("the card stages the reveal moment — it feels like opening a pack") PASSES — proving the check fires on the missing experience, not on the component's presence.
10. **Weaving census recorded:** the census lists every staged skill as in-scope (makes UI/design decisions) or out-of-scope with a reason; no skill is left unclassified.
11. **Weaving coverage:** every in-scope skill carries the design-decision pointers at its decision points (routing, triggers, decision points, checklists); every trigger key resolves to a real skill dir; coverage.withTriggers matches the key count. A re-traced build's decision points invoke the rules (the dry-run traces at least one decision through a woven pointer).

The dry-run report (`fix20/dryrun31-report.md`) records the stale-
workspace caveat and the repair-reported status explicitly. No count
target: the re-trace is the check above, not an element recount.

## 7. Verify script — fix20/verify20.py

Follows the fix19/verify19.py pattern (read-only, against the BUILT
tree; imports rule constants from fix15, fix17, fix18, fix19, fix20).
Checks:

1. F4_SCOPE/F5/F6/B1/X1 anchors present in Taste (built) and orchestrate
   (built).
2. F4_SCOPE_APP/F5_APP/F6_APP/B1_APP/X1_APP present in ui-ux-pro-max
   (built) and orch-build-mvp (built).
3. STATIC20 present ×3 (Taste step 6, orchestrate Verify 5a,
   orch-build-mvp step 6); after STATIC19 in each; in orchestrate
   before the 5b bullet; STATIC20 contains the B1 and X1 items.
4. POLISH_F20 present in polish-pass (including the B1/X1 sentence);
   TYPESET_F20 present in the typeset lens; TYPESET_CHECKBOX20_NEW
   present and the fix19 checkbox GONE.
5. Fix19 anchors intact: F4_RULE still present verbatim in Taste and
   orchestrate; F4_APP still present in ui-ux-pro-max; STATIC19 still
   present ×3; D19_RULE still present in Taste and orchestrate.
6. Canonical block still verbatim ×1 in all 11 files; D1 rule still
   present in Taste/orchestrate/polish-pass/orch-build-mvp.
7. vantage.md UNCHANGED in the built tree (display and body still
   Geologica) — this fix governs the deal, it does not rewrite theme
   data; the scope rule text names the collision handling.
8. Counts unchanged post-fix19: 166/72/123/87/15.
9. No banned terms (fix #16 scrub) in the built skill tree (excl.
   node_modules).
10. build.sh is the post-fix20 file (lines + md5 as recorded in
    fix20/MANIFEST.md) and still contains the fix15 + fix17 + fix19 +
    fix20 blocks intact.
11. verify15.py 43/43, verify17.py 59/59, verify18.py 72/72,
    verify19.py 75/75 (run as subprocesses, exit 0 required).
12. Weaving (§10): every in-scope skill (per the census recorded in
    fix20/MANIFEST.md and as a constant in verify20.py) carries the
    design-decision pointer at its decision points; every trigger key in
    skill-triggers@1.json resolves to a real skill dir;
    coverage.withTriggers equals the key count; no staged skill is left
    unclassified in the census.

## 8. Checkers

- Audit #62, dry-run #31, sweep #25 (following fix #19's #61 / #30 / #24).
- Build twice (exit 0, diff 0) before the checkers; the fix-up round
  pattern from fix #17/#18/#19 applies (re-audit + re-sweep after any
  fix-up; the bound holds: a bound-holding diff triggers no re-run).
- Backup: `build.sh.before-fix20` (first pre-fix20 copy, kept).
- The audit/dry-run/sweep run AFTER the weaving pass (§10), against the
  final tree (rules + weave).

## 9. Untouched / non-goals

- Fix #16 Grok pins and the Claude/Codex scrub (banned terms stay 0).
- Fix #15 anchors (43/43), fix #17 anchors (59/59), fix #18 anchors
  (72/72), fix #19 anchors (75/75).
- The 11-file canonical block (verbatim).
- The Campus Eats artifact (read-only reference; do not touch).
- `fix11/fix11-stage.py` (never re-run).
- No commit, no bundle, no GitHub touch.
- No new inventory: no new less-flat-ui catalogue entries, no new
  Hallmark themes, no new font catalogue entries, no theme-file edits.
  Tiempos and Fraunces are named in rule text, not added as catalogue
  items.

## 10. Weaving — the rules at every decision point (added Nov 11 evening, Anish's direction)

Anish's direction (his words): "Weave ALL of these design decisions into
ALL the applicable skills in the plugin — not just the canonical block in
the design skills. The rules must be woven into the skills themselves at
the points where decisions are made — routing, triggers, decision points,
checklists — so the agent thinks about the design SUBCONSCIOUSLY when
making decisions, rather than having to deliberately remember to consult
a separate rule file. A skill that makes UI/design decisions but doesn't
carry the rules at its decision points fails the check."

### The rule set being woven

The design-decision rule set: fix #19 F2 (font identity), F3 (forced
unique pairing), F4 (body-only Tiempos), fix #19 D19 (thought-out
decision across the full experience), fix #20 F4_SCOPE (body-only
scope), F5 (unique important font), F6 (impressive bar), B1 (branding),
X1 (component-as-experience). The full rule texts live in the
design-package rule (Taste step 4a / orchestrate) — the weave carries
POINTERS, not copies: a concise line at each decision point naming the
applicable rules and pointing at the canonical home.

### The weave mechanism (Nov 10 weaving program pattern)

Follow weave1/weave2 (see `weave1/MANIFEST.md`, `weave1/weave1.py`,
`weave2/MANIFEST.md`): staged-source edits (each asserting
exactly-one-match per substitution) + one build.sh patch block placed
LAST just before STEP 5 (upstream files + trigger JSON). Each weave is a
named connection: producer → consumer → carrier, recorded in the
manifest.

- At each decision point (a routing line, a trigger line, a checklist
  item, a decision line — anywhere a skill decides something about
  UI/design), add a concise pointer: the applicable rules by name
  (F2/F3/F4/F5/F6/D19/B1/X1 as relevant) + the pointer "design-package
  rule — Taste step 4a / orchestrate". The pointer is ONE line, not the
  full rule text. A decision point that decides UI/design and carries no
  pointer is a gap.
- Trigger keys: every in-scope skill must have a trigger key in
  `manifests/context-packs/skill-triggers@1.json` that resolves to its
  real skill dir; `coverage.withTriggers` is updated to the new total.
  A key that does not resolve is a defect. (Baseline entering this
  weave: 58 keys, all resolving — the Nov 10 weaving program's count.)
- Census first: list every staged skill and classify it as IN SCOPE
  (makes UI/design decisions) or OUT OF SCOPE (recorded with its
  reason, following weave1's reasonableness bound — stack-specific,
  meta/ops, business skills are legitimately on-demand). The census is
  recorded in the manifest and as a constant in verify20.py. A skill
  classified out of scope with no reason is a gap.

### The check

A skill that makes UI/design decisions but doesn't carry the rules at
its decision points FAILS the check. The sweep asserts it (every
in-scope skill carries the pointers at its decision points); the
dry-run re-traces a build and shows the decision points invoking the
rules; verify20 gains weaving checks (see §7 check 12). The weave does
not change the rules, the canonical block (still verbatim), or any pin.

## 11. Fix-up (Nov 12, 2026 — audit #62 / dry-run #31 / sweep #25)

Applied by `fix20/fixup20.py` after the audit loop's first pass. Not a
new fix: three rulings on the rule text as written.

1. **F4_SCOPE role-scoping (sweep #25 Finding 1).** The `fraunces`
   pairing in Taste's type catalogue deals Fraunces as the DISPLAY face
   (Figtree body) — a live, dealable path. Read literally, F4_SCOPE's
   "NEVER used for important text" forbids it, so SPEC §1's claim that
   no staged source deals a body-stand-in family as display was wrong
   (it had only measured theme files). Ruling: the scope rule binds the
   face IN ITS ROLE as the body/reading face; a pairing that deals
   Fraunces as the display face, with a different face as body, is
   governed by F3/F5, not F4. F4_SCOPE, F4_SCOPE_APP, and STATIC20 now
   carry that role-scoping sentence. The pairing stays.
2. **F5 "key label" defined (sweep #25 Minor).** A key label is a label
   meant to stand out — featured section label,
   emphasis badge or price label. Ordinary small labels (nav links,
   table heads, captions, chips, form labels, meta rows) follow the
   Hallmark gates: the body face, a step smaller, sentence case,
   untracked. F5 and F5_APP carry the definition.
3. **coverage.skills 169 → 166 (audit #62).** The upstream
   skill-triggers manifest still recorded the Oct 30 count (169); the
   tree has 166 skills since the fix #16 era. The fix-up patches it at
   build time; verify20 gains check 13 asserting it.

Known deviations recorded, NOT fixed here (pre-existing, out of scope):
- Dry-run #31 item 3: the read-only Campus Eats reference artifact's
  CTA buttons `.btn` (`index.html:193`) and `.roll-btn` (`:679`) are set
  in Fraunces, the body face — a genuine F5 leak in a pre-fix-#20
  artifact. (Correction, dry-run #32: `.step-btn` is NOT a leak — it is
  `font-family: "Bowlby One SC", "Fraunces", Georgia, serif` at :485,
  display face primary with Fraunces only as fallback. An earlier
  record listed it as a leak; that was wrong.) The artifact is
  read-only; the package rule correctly catches exactly this leak
  (dry-run item 4 proves it). Any future build re-traced through the
  fixed package fails STATIC20 on its CTAs until re-dealt in the
  display face.
- Staged "claude" occurrences in `rewritten-skills/app-scaffold/` and
  `new-rules/hackathon-mode.mdc:38` are pre-existing fix #16
  staged/built drift; the built tree is scrubbed by `fix16/fix16.py`
  `generic_pass()` and verify20's banned-term check passes.

## Fix-up #2 (Nov 12, 2026 — sweep #26, 0 blocking / 3 minor)

Applied by `fix20/fixup20b.py` after audit #63 (ZERO ERRORS), dry-run #32
(13/13 PASS), and sweep #26 (NOT CLEAN — 0 blocking, 3 minor).

1. **F5 examples (MINOR-1).** Dropped "hero eyebrow or kicker" from
   the key-label examples (Hallmark gate 54 bans eyebrows; floor rule 9
   opens "Never an eyebrow"). The DEFINITION ("a label meant to stand
   out") is unchanged — only the illustration. Examples now: featured
   section label, emphasis badge, price label.
2. **Section cite (MINOR-2).** "hackathon-mode §37" → §5 (5
   occurrences in verify20.py / weave20.py). The exclusion lives at §5,
   line 38; the file has only §1–§7. (weave1/MANIFEST.md:127 hedges the
   same cite — a closed historical manifest, left as-is.)
3. **Batch E comment (MINOR-3).** build.sh's fix #4-era Batch E comment
   claimed the block sat last before STEP 5 and that no build.sh patch
   touches less-flat-ui — both false since weave1/weave20. Comment
   corrected in place (comment-only, zero behavior).

## 12. Fix-up #3 (fixup20c — Nov 12, 2026 — steers #3/#4/#5 + sweep #27 leftovers)

Applied by `fix20/fixup20c.py`. Three Anish steers from Nov 11 evening
(total/interconnected weave, model roles, OVERDRIVE expansion; binding
weave; creativity-through-the-skills balance) plus the leftovers sweep
#27 found in the fixup20b loop (NOT CLEAN: 1 finding + observations).

### 12.1 Sweep #27 leftovers (verified by the coordinator)

- **FINDING 1 (comment-only).** MINOR-2 was NOT fully resolved: the
  embedded weave20 block in build.sh:23475 still cites
  "hackathon-mode section 37" — `fix20/weave20.py:478` was corrected to
  §5, but the already-inserted copy in build.sh never was. Fix: one-line
  comment edit in build.sh (this engine). Zero behavior.
- **MINOR-3 re-opened — DECISION: normalize all of them.** The false
  "placed LAST — just before STEP 5" claim persists in ~60 more build.sh
  block headers (fix #4-era boilerplate; each block was last when
  written, every later block made the claim false). The coordinator
  re-opens MINOR-3 for the whole pattern: this engine replaces every
  placement-"LAST" phrase in build.sh with the same wording minus the
  false claim (64 replacements, line count unchanged — validated on a
  /tmp copy first). The only "LAST" lines left are the two TRUE ones:
  "This patch runs LAST (after every audit_patch and qc_patch …)" —
  intra-block patch order, not file placement. The fixup20c block's own
  header uses "Placement: before STEP 5" from the start, so no future
  block can stale it.
- **Generator consistency.** The fix #20 program's own generators emit
  the same header strings into build.sh, so their emitted strings are
  updated to match the normalized copies (weave20.py BLOCK header,
  fix20.py / fixup20.py / fixup20b.py block headers). Docstrings and
  code comments describing the historical action ("appended LAST") are
  left as-is — they were true when the action ran. The fix15/17/18/19
  generators are left historical (one-shot, not regenerated since those
  programs closed); only their embedded build.sh copies are normalized.
- **fixup20b.py re-import fix.** Like fixup20.py before it, fixup20b.py
  could not be re-imported post-application (module-level
  `F5_NEW2 = F5.replace(...)` is a no-op once fix20.py holds the amended
  text, so the assert fails — sweep #27 had to reconstruct the old texts
  by hand to regenerate the block). Fixed with the same reversal the
  coordinator applied to fixup20.py: import the amended texts as the
  NEW values and derive the OLD values by reversing the substitution.
  Import succeeds after this; a re-RUN is still refused by preflight
  (one-shot applicator, by design).
- **Observation (not a finding, out of scope).** Taste's component
  library still ships eyebrow elements (`.cx-eyebrow`) while Hallmark
  gate 54 + floor rule 9 ban eyebrows. Pre-existing library/lint
  tension; the ban is enforced by lint, so this is not a fix #20
  regression. Left as-is, recorded here.

### 12.2 H1 — model hierarchy (steer #3 item 2)

Grok 4.7 High is the ORCHESTRATOR and the main mind behind big
decisions; Grok 4.6 High are the underlings — fast execution workers.
Matches the fix #16 pins; the job is to make the hierarchy explicit
and woven into orchestrate and the design-package rule.

> **Model hierarchy — Grok 4.7 High decides, Grok 4.6 High executes
> (fix #20 H1).** Grok 4.7 High (`grok-4.7-high`) is the ORCHESTRATOR
> and the main mind behind big decisions: the orchestrator, the
> design-lead, the deep-reasoner, and every big-decision role run on
> Grok 4.7 High. Grok 4.6 High (`cursor-grok-4.6-high-fast`) are the
> underlings — fast execution workers: scout, fast-worker, and the
> other composer-tier agents execute fully-specified work and never
> decide. A 4.6 worker that faces a decision routes it up to the 4.7
> mind (orchestrator / deep-reasoner / design-lead); it never decides
> on its own. A dispatch that puts a big decision on a 4.6 model, or
> execution a 4.6 worker could do on a 4.7 model, is a routing error —
> a static check item, never a screen verdict.

Placements: full text in orchestrate (new block before "## Setup",
after the team table) and in hackathon-mode §6 (bullet); a one-line
pointer in the design-package rule paragraph (orchestrate row 10):
"Model hierarchy (fix #20 H1): the design-lead decides on Grok 4.7
High; executors implement on Grok 4.6 High — no big decision runs on
a 4.6 worker, no execution a 4.6 worker could do runs on the 4.7
mind."

### 12.3 OVERDRIVE expansion (steer #3 item 3)

Brainstorm / new-feature expansion runs ~1.75x more — about 75% more
features/tools surfaced per build. Anchored to the original idea and
the grill-me decision record; the anti-drift bound stays and is
explicit. Current volume rules (found in `feature-expansion` only):
Phase 1 = 4 lenses x 3–5 candidates each (12–20 raw); Phase 2 =
"Keep it to 4–7 features." (SKILL.md:104).

> **OVERDRIVE expansion (fix #20).** Expansion runs in OVERDRIVE:
> about 75% more features/tools surfaced per build (~1.75x the old
> volume) — each brainstorm lens returns 5–9 candidates (was 3–5),
> the shortlist keeps 7–12 features (was 4–7). The anti-drift bound
> stays and is explicit: expansion stays anchored to the original
> idea and the grill-me decision record (Phase 0 grounding pastes
> them inline); expansion PROPOSES, the planner APPROVES / TWEAKS /
> REJECTS (Phase 3) — a feature that contradicts a recorded decision
> is rejected, never tweaked around it; a feature that does not fit
> the one coherent product story is tweaked or rejected; nothing that
> drifts from the OG idea gets built. 7–12 is a CAP, not a quota —
> never pad to reach it; fewer exceptional features still beat many
> mediocre ones. With 7–12 features the proposal table usually
> exceeds the 20-line ledger — that is expected; the full table goes
> in `docs/expansion.md` and the ledger carries a one-line pointer
> (the existing overflow rule); never cut features to fit the ledger.

Placements: full rule before Phase 0 in `feature-expansion`; Phase 1
line ("Each returns 3–5 candidates") → 5–9 with an OVERDRIVE pointer;
Phase 2 line ("Keep it to 4–7 features") → 7–12 with the cap-not-quota
and overflow sentences; OVERDRIVE pointers in orchestrate step 2 and
hackathon-mode §1 (next to the expansion sentence). The hackathon-mode
§1 "fewer exceptional features beat many mediocre ones" line stays
untouched — it IS the anti-padding guard, not a contradiction of the
new volume. Orchestrate step 2 also keeps its "No double-run" rule
(expansion Phases 0–3 run ONCE per run).

### 12.4 BIND + INNOV — binding weave, creativity through the skills (steers #4 + #5)

The weaving must be BINDING, not just present: every decision routes
through a named skill; the skills are the only path. This is the fix
#13 standing rule ("every design decision is made BY a named package
skill; Grok executes THROUGH the package, never replaces it") extended
to the whole weave. AND the binding must NOT kill creativity: agents
stay creative and innovative — but BASED OFF the skills. Innovation
extends, combines, and pushes the skills; it never bypasses them. The
balance is: bound to the skills, creative within and through them.
This channels the fix #17 E1 creativity push (trailblazing, not dumb)
through the skills rather than suppressing it.

> **Binding routing — the skills are the only path (fix #20 BIND).**
> Every decision routes through a NAMED skill: the operating skill
> for the work is named in the brief before the work starts, and the
> work is done by that skill's rules. A decision with no named
> operating skill is not a decision — it is refused and routed to the
> skill that owns it; where NO skill owns it, the recorded-gap fallback
> below applies. Work produced without a named skill in its brief is an
> incomplete build — a static check item, never a screen verdict —
> unless it is a recorded-gap fallback (below). Grok executes THROUGH
> the package, never replaces it (fix #13: every design decision is made
> BY a named package skill): no freelance work, no off-skill
> improvisation. The audit and the dry-run FAIL any decision or work done
> outside a named skill where a skill exists and was bypassed — that is
> off-skill improvisation. **Recorded-gap fallback (fix #20):** binding
> never blocks needed work. When a needed step has no skill covering it,
> the agent does NOT stop: it records the gap in the decision record
> (what was needed, why no skill covers it), does the work by the
> closest skill's principles (building off the skills), and flags it so
> the gap can become a skill later. A needed step done through the
> recorded-gap fallback PASSES the audit/dry-run — it is not off-skill
> improvisation. Priority order: (1) everything needed gets done, (2) on
> the skills wherever a skill exists, (3) through the recorded-gap
> fallback where none does.

> **Innovation builds on the skills (fix #20 INNOV).** Binding routing
> does not kill creativity: agents stay creative and innovative — but
> BASED OFF the skills. An original element or approach that extends,
> combines, or pushes a skill's principles is on-skill innovation: it
> PASSES, recorded with its fix #19 D19 reason (what skill principle
> it builds on, why the extension serves the surface). Innovation
> extends, combines, and pushes the skills; it never bypasses them.
> This channels the fix #17 E1 creativity push (trailblazing, not dumb)
> through the skills rather than suppressing it. The audit and the
> dry-run FAIL off-skill improvisation but do NOT fail on-skill
> innovation.

Placements: full texts in orchestrate (same block as H1, before
"## Setup") and in hackathon-mode §6 (bullets); a pointer sentence in
the design-package rule paragraph (orchestrate row 10); short pointer
sentences in the built orch-build-mvp (design-package bullet) and
orch-pipeline ("Each phase delegates") files via the build.sh block.
The dry-run demonstrates both branches: an off-skill decision FAILS,
an on-skill original element PASSES.

**Recorded-gap fallback (steer #6, Nov 12).** The binding must NOT
shut down needed work: everything needed still gets done, and the
agent is never blocked just because something isn't on the skills.
When a needed step has no skill covering it, the agent does NOT stop —
it takes the documented fallback path (record the gap in the decision
record: what was needed, why no skill covers it; do the work by the
closest skill's principles; flag it so the gap can become a skill
later). The audit/dry-run check FAILS only off-skill improvisation
where a skill exists and was bypassed — it must NOT fail a needed step
done through the recorded-gap fallback. Priority order: (1) everything
needed gets done, (2) on the skills wherever a skill exists, (3)
through the recorded-gap fallback where none does. The dry-run
demonstrates three branches: off-skill work where a skill exists
FAILS, on-skill innovation PASSES, a needed step through the
recorded-gap fallback PASSES.

### 12.5 Fix-up #4 (fixup20d — Nov 12, 2026 — sweep #28 MINOR-1, comment-only)

Sweep #28 (NOT CLEAN — 0 blocking, 1 minor) found the fixup20c
MINOR-3 normalization missed a lowercase family: 20 build.sh block
headers say "The coordinator inserts this block last, just before
STEP 5." (or "The patch agent inserts …"). The fixup20c probe only
counted uppercase `LAST`, so the family was never counted. Same false
claim, different casing — fixed by `fix20/fixup20d.py` (20
replacements: 13 single-line + 7 split-line, line count unchanged,
built tree byte-identical to the fixup20c build — diff 0 across the
3,284-file manifests). The lowercase "Runs last so it sees …" at
build.sh:15853 is TRUE intra-block patch order and is left alone, as
are the two TRUE uppercase "runs LAST (after every …" lines and the
Batch E note ("this block does not sit last"). verify20 check 18
gained a lowercase assertion ("inserts this block last" == 0,
"last, just before STEP 5" == 0) — verify20 is now 168 checks. The
fix19:330 section label (which still said "post-fixup20b") was
corrected to post-fixup20d with the pin bump.

Note on the loop: audit #65 (ZERO ERRORS) and dry-run #34 (15/15
PASS) ran against the fixup20c-built tree; fixup20d is comment-only
and the built-tree diff 0 proves the tree they verified is the tree
being delivered, so neither needs re-running for this fix-up.

**Pointer-chain reasoning (why the 32 woven pointers are NOT
re-edited).** The pointers invoke the design-package rule ("Taste
step 4a / orchestrate"), and the design-package rule — which lives in
orchestrate — now carries the BIND/INNOV + H1 pointer sentences. So a
decision point whose pointer invokes the rule is bound by it: the
chain pointer → design-package rule → BIND/INNOV/H1 is connected, with
no dead end. Re-editing all 32 pointer lines to name the new tokens
would duplicate the reference without adding a connection. Check 14
proves the chain (every pointer token resolves, every pointer targets
the design-package rule, the rule carries the new pointers).

### 12.5 Interconnection (steer #3 item 1) + new verify20 checks 14–18

Total and interconnected: every rule, trigger, and decision point
connects to the design/product-thinking core — no orphan rules, no
dead-end references. Check 14 proves it: every rule token
(F2/F3/F4/F5/F6/D19/B1/X1/H1/BIND/INNOV) resolves to a defining phrase
in the built tree; every Design-decision pointer line's tokens all
resolve; every pointer targets the design-package rule, which exists
in built orchestrate and carries the H1 + BIND/INNOV pointers.
Check 15: H1 in orchestrate + hackathon-mode §6 + design-package
pointer. Check 16: OVERDRIVE (5–9, 7–12, cap-not-quota, overflow,
orchestrate + hackathon-mode pointers, anti-drift guard intact, old
3–5 / 4–7 gone). Check 17: BIND/INNOV in orchestrate + hackathon-mode
§6 + design-package pointer + orch-build-mvp + orch-pipeline pointers,
with the fail/pass distinction and the E1 channeling. Check 18:
build.sh hygiene — "section 37" == 0, "LAST" appears only in the two
TRUE "runs LAST (after every …" lines, and the fix #20 program's
block headers read "before STEP 5" (generator = embedded copy).
