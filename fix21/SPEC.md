# Fix #21 — SPEC: Long body and small text only; every text element gets an artistic font design decision

## 0. Goal

Tighten the scope of the Tiempos/Fraunces rule so a future build cannot
use the body face as a general default, and make every text element
carry a deliberate, recorded artistic font design decision. Anish's
refinement (Nov 11 evening, his words): "the font usage of the one i
said to use for plaintext is too much, every text should have an
artistic font design decision behind it, not just default to this this
is only for long length body text or small text here and there, not for
main text we see visually."

The body face (Tiempos / the Fraunces stand-in) is for LONG-LENGTH
body text and SMALL incidental text only. Main text we see visually
uses the unique important font (fix #20 F5) or another artistic face
chosen through the skills — never the body face as a default. No text
element defaults to the body face without a recorded artistic font
design decision.

Gate (verified before writing this SPEC): `fix20/MANIFEST.md` exists;
`build.sh` is 23,609 lines, md5 `785fb40580a4d91f7a480e1cdbc21f24`
(post-fix20). Checker numbers entering fix #21: Audit #65 ZERO (0/0),
dry-run #34 15/15 PASS, sweep #28 0 blocking / 1 minor (fixed,
built tree byte-identical); verify15 44/44, verify17 60/60,
verify18 72/72, verify19 76/76, verify20 169/169. Counts 166 skills /
72 agents / 123 rules / 87 commands / 15 hooks.

## 1. Evidence — the gap fix #20 left open

Fix #19's F4 says "Body and plain text use Tiempos" — and fix #20's
F4_SCOPE says the body face is "for BASIC text only ... NEVER used for
important text." Neither states the body face is NOT a default: a build
could set every non-important text element — labels, captions, buttons,
prices, names, meta rows, table heads — in Fraunces by default, with no
artistic font decision behind any of them, and be fully compliant with
F4 and F4_SCOPE. That is the leak this fix closes, and it is the leak
Anish named: the Fraunces usage is too much.

Measured data (Nov 11, post-fix20 built tree):

- The broad F4 statement is a verify19 anchor (full-text `in` check):
  `fix19.py` F4_RULE says "Body and plain text use Tiempos (Klim,
  paid, NOT bundleable). The canonical free stand-in is Fraunces, set
  at a 1.55 reading line-height." It is NOT edited by this fix. The
  tightened reading is stated by the new F4_TIGHT rule (SPEC §2):
  "body and plain text" reads, after this fix, as long-length body
  text and small incidental text only.
- Fix #20 F5's small-labels permission ("Ordinary small labels —
  nav links, table heads, captions, chips, form labels, meta rows —
  follow the Hallmark gates: the body face, a step smaller, sentence
  case, untracked") is the permitted set's second half: those small
  labels ARE the "small text here and there" where the body face is
  allowed — but only with a recorded artistic font decision (fix #21
  F7). The permission was never a blanket default.
- Campus Eats repair evidence (recorded fix #20 findings, dry-run
  #31/#32 — the artifact is read-only, the workspace tokens file is
  v1-era/stale and is NOT evidence): the repair set plain text in
  Fraunces broadly, and its CTA buttons `.btn` (`index.html:193`)
  and `.roll-btn` (`:679`) are set in Fraunces, the body face — a
  genuine F5 leak in a pre-fix-#20 artifact. `.step-btn` is NOT a
  leak — it is `font-family: "Bowlby One SC", "Fraunces", Georgia,
  serif` at `:485`, display face primary with Fraunces only as
  fallback. The package rule correctly catches exactly this leak
  (dry-run #31 item 4 proves it). Any future build re-traced through
  the fixed package fails STATIC21 on its CTAs until re-dealt in the
  display face — and now also fails F7 on any text element with no
  recorded font decision.

## 2. Rules

### F4_TIGHT — the Tiempos rule tightened: long body and small text only (fix #21, tightens fix #19 F4 / fix #20 F4_SCOPE)

F4_TIGHT = """**Long body and small text only — the Tiempos rule tightened (fix #21 — fix #19 F4 tightened).** Tiempos and the Fraunces stand-in are for LONG-LENGTH body text and SMALL incidental text only — running paragraphs of reading prose, and small text here and there (ordinary small labels: captions, meta rows, table heads, form labels, chips, small nav links). They are NOT a default for text generally, and they are NEVER used for main text we see visually. 'Body and plain text use Tiempos' (fix #19 F4) reads, after this fix, as long-length body text and small incidental text only. A build that sets its labels, captions, buttons, prices, names, or any other text element in the body face by default — with no artistic font decision behind it — is an incomplete build, even if no single element is 'important' text. The body face is the face serving as body/reading text on that build; the role-scoping from fix #20 stands (a pairing that deals Fraunces as the display face, with a different face as body, is governed by fix #19 F3 / fix #20 F5, not by this scope rule)."""

### F7 — Every text element gets an artistic font design decision

F7 = """**Every text element gets an artistic font design decision (fix #21 F7).** Every text element — heading, label, caption, button, price, name, body, meta row, table head, chip, nav link, call to action — has a deliberate, recorded artistic font design decision behind it: which face, why this face, what job it serves, how it matches the theme and the brand. The decision is recorded in the decision record's Type list, per text element — or per text class where the class is genuinely uniform (one decision line per class, naming the class and the face and the reason; a blanket 'all text' line is not a class decision). No text element defaults to the body face without a decision. Main text we see visually — headings, display type, hero text, prominent labels, prices, names — uses the unique important font (fix #20 F5) or another artistic face chosen through the skills, never the body face as a default. A text element with no recorded artistic font decision, or a main visible text element set in the body face, is an incomplete build — a static check item in step 6, never a screen verdict. The decision is covered by its fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions); the font decision is the D19 reason for that text element's font choice."""

### Fix #21 static checks (mirrors fix #19 STATIC19 / fix #20 STATIC20)

STATIC21 = """**Fix #21 static checks (all static checks, never screen verdicts).** (F4 tight) The Type list marks the body face as long-body-and-small-text-only — no token for main visible text points at the body face; the body face serves long-length body text and small incidental text only. (F7) Every text element in the Type list — or every genuinely uniform text class — carries its recorded artistic font decision (face + why + job + theme/brand fit); a text element with no recorded decision is an incomplete build; a main visible text element (heading, display, hero, prominent label, price, name, call to action) set in the body face is an incomplete build; a blanket 'all text' class line is not a class decision. (F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice."""

### App mirrors (fix #21 F4_TIGHT / F7 on app surfaces)

F4_TIGHT_APP = """**Long body and small text only (fix #21 — F4 tightened, app surfaces).** On app surfaces, Tiempos and the Fraunces stand-in are for long-length body text and small incidental text only — never a default for text generally, never main visible text. The full tightened scope rule lives in `design-taste-frontend` step 4a."""

F7_APP = """**Every text element gets an artistic font design decision (fix #21 F7, app surfaces).** On app surfaces, every text element has a deliberate, recorded artistic font design decision — which face, why, what job it serves, how it matches the theme and the brand — recorded in MASTER.md's Type list, per text element or per genuinely uniform text class. No element defaults to the body face without a decision; main visible text uses the display face (fix #20 F5) or another artistic face chosen through the skills. The full F7 rule lives in `design-taste-frontend` step 4a."""

### Typeset lens (polish-pass)

TYPESET_F21 = """**Long body and small text only; every text element gets an artistic font decision (fix #21).** The body face (Tiempos or the Fraunces stand-in) is for long-length body text and small incidental text only — a heading, hero line, call to action, key label, price, name, or prominent label set in the body face is a finding. Every text element needs a recorded artistic font decision (face + why + job + theme/brand fit) in the Type list — an element with no recorded decision is a finding, and a blanket 'all text' class line is not a decision. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size."""

TYPESET_CHECKBOX21 (replaces the fix #20 checkbox in the typeset lens):
Old: "- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for basic text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20)."
New: "- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for long-length body text and small incidental text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20); every text element has a recorded artistic font decision (fix #21 F7)."

### Polish-pass harmony

POLISH_F21 (appended after POLISH_F20 in the harmony check):
" It also verifies the tightened font scope (fix #21): each Type-list body-face row is marked long-body-and-small-text-only, no main visible text token points at the body face, and every text element carries its recorded artistic font decision — a token or element that does not is a harmony divergence, recorded as candidate evidence, never a verdict."

## 3. Placement (fix #15 / fix #17 / fix #19 / fix #20 pattern)

The canonical variety + theme-match block is NOT modified (verify15.py's
verbatim check must keep passing — the block stays verbatim ×1 in all 11
files). The fix21 rules are placed as new bold rules adjacent to the
fix20 rules, mirroring fix20's placement. One source of truth; build.sh
patches where the built tree needs them. The implementation engine MUST
NOT edit any fix19 or fix20 rule text in place — F4_RULE / STATIC19 /
D19_RULE and F4_SCOPE / F5 / F6 / B1 / X1 / STATIC20 are verify19 /
verify20 anchors (full-text `in` checks); fix21 appends new rules after
them and asserts the old ones are still present verbatim.

### Staged sources (edited directly; build.sh copies them verbatim)

| # | File | Change |
|---|---|---|
| 1 | `new-skills/design-taste-frontend/SKILL.md` (step 4a) | Append F4_TIGHT + F7 after the X1 rule. Anchor: the full X1 constant from fix20.py (measured count==1 in this file). |
| 2 | Taste step 6 | Append STATIC21 after STATIC20. Anchor: the full STATIC20 constant (measured count==1 in this file). |
| 3 | `new-skills/orchestrate/SKILL.md` (design-package rule) | Append F4_TIGHT + F7 after the X1 rule. Anchor: the full X1 constant (measured count==1 in this file). |
| 4 | orchestrate Verify 5a | Append STATIC21 after STATIC20. Per the fix19 deviation-3 precedent: append after the 5a paragraph's final sentence (NOT after the two-line "…5b. Final polish" anchor) and assert it sits before the 5b bullet. |
| 5 | `round2-skills/polish-pass/SKILL.md` (harmony) | Append POLISH_F21 after POLISH_F20. Anchor: the full POLISH_F20 constant (measured count==1 in this file). |
| 6 | `round2-skills/polish-pass/reference/lenses/typeset.md` | Append TYPESET_F21 after TYPESET_F20 (anchor: the full TYPESET_F20 constant, measured count==1); replace the fix20 checkbox with TYPESET_CHECKBOX21 (old text = fix20's TYPESET_CHECKBOX_NEW, measured count==1). |

### build.sh patch block (upstream, no staged source)

| # | File (built) | Change |
|---|---|---|
| 7 | `skills/ui-ux-pro-max/SKILL.md` | Append F4_TIGHT_APP + F7_APP after X1_APP (anti-generic bar area). NOTE: X1_APP occurs TWICE in build.sh (once per patched file) — anchor within this file's fix20 patch-block entry, never a bare build.sh-wide count (same per-entry technique fix20.py used for D19_APP inside the fix19 block). |
| 8 | `skills/orch-build-mvp/SKILL.md` | Append F4_TIGHT_APP + F7_APP after X1_APP (step 4, within this file's fix20 patch-block entry); append STATIC21 in step 6 after STATIC20 (STATIC20 occurs once in build.sh — the orch-build-mvp fix20 step-6 entry). |

No new weave pointers: the §10 weave (fix #20) carries pointers to
the design-package rule, and the new rules live IN the design-package
rule (Taste step 4a / orchestrate) — the chain pointer → design-package
rule → F4_TIGHT/F7 is connected, with no dead end. verify21 asserts
the F4_TIGHT/F7 tokens resolve (see §7 check 12) rather than adding
duplicate pointer lines.

## 4. What the canonical block does NOT get

The canonical variety + theme-match block stays verbatim ×1 in all 11
files (verify15.py must keep passing 44/44). Do not append the fix21
rules INTO the block. The motion-* skills, make-interfaces-feel-better,
and hallmark-floor.md get no direct fix21 edit: their entries are
covered by the record-level D19/F7 checks, and they do not decide
fonts. No Verify-step-5 edit: the visual loop's giant line is not
touched — F7's verdict side is the same screen verdict mechanism the
finish review already runs (browser-qa's visual verdict), and the
STATIC21 record check is the static side. If the audit finds a motion
skill deciding a font, that is a finding for the audit, not a new edit
in this fix.

## 5. Conflicts resolved in this SPEC

- **Typeset lens check #4 vs F7.** The lens asks "Are display or
  script faces used in buttons, labels, inputs, or data?" as a smell —
  and F7 says every text element, including buttons and labels, gets a
  deliberate artistic face chosen through the skills. NOT a
  contradiction (same ruling as fix #20 §5): F7 governs WHICH face (an
  artistic face, recorded with its decision); the lens's check #4
  governs HOW (scale, weight, tracking — a display face set badly in
  a label is a finding, but the face choice itself follows F7). A
  sticker-style pill button set in the dealt display face at the right
  scale is exactly the intended outcome. Recorded as a resolved
  tension, not a defect.
- **Fix #20 F5 small-labels permission vs F7.** NOT a contradiction:
  the F5 permission names WHERE the body face is allowed (ordinary
  small labels: nav links, table heads, captions, chips, form labels,
  meta rows); F7 names the CONDITION (a recorded artistic font
  decision, per element or per genuinely uniform class). A small label
  in the body face WITH its class decision recorded passes both; a
  small label in the body face by default, with no decision, fails F7.
  The "small text here and there" in Anish's words is exactly this
  F5 small-labels class.
- **F4_RULE not edited.** Fix #19's F4_RULE is a verify19 anchor
  (full-text `in` check). F4_TIGHT scopes it by interpretation
  ("reads, after this fix, as long-length body text and small
  incidental text only") without touching its text — same pattern as
  fix #20's F4_SCOPE, which scoped F4 without editing it.
- **STATIC19 not edited.** STATIC19's (F4) item ("Body/plain text is
  Tiempos or the recorded stand-in at 1.55 line-height") is a verify19
  anchor. STATIC21 is appended after STATIC20 and states the
  tightened reading; the F4 item is now read through F4_TIGHT.
- **Banned tokens in rule text.** The phrases naming the font's owner
  and the product whose reading text it sets are banned tokens under
  the fix #16 scrub — the fix21 rule constants use "Tiempos" and
  "Fraunces (stand-in for Tiempos)" only, as fix #19 and fix #20 did.
  The engine's preflight MUST scan every added text for banned tokens
  (claude, codex, anthropic, opus, sonnet, haiku, composer-2.5) and
  fail before any edit if one is present.
- **F7 vs the D19 reason.** Complementary, not duplicative: D19
  requires a reason for every UI decision (font included) across six
  dimensions; F7 makes the font decision explicit and checkable PER
  TEXT ELEMENT (or per genuinely uniform class) in the Type list. A
  D19 reason that covers the font choice satisfies F7's decision
  requirement; F7 adds the coverage check (every element listed, no
  element defaulting).

## 6. Dry-run — dry-run #35

The dry-run is a font-scope + per-element-decision check, not an
element recount. PASS requires all of:

1. **Rule presence:** verify21.py passes (see §7).
2. **Criteria coverage:** every scope token — body face only for
   long body + small incidental text; every text element has a
   recorded artistic font decision; main visible text uses the
   display/artistic face — is named as a check trigger in the
   STATIC21 text.
3. **Repair compliance (repair-reported):** the repaired Campus Eats
   artifact complies with the refined scope for its long body text
   and small incidental text (Fraunces, per the repair's verified
   solution) — and its known `.btn` / `.roll-btn` Fraunces CTAs
   remain recorded F5 leaks (fix #20 §11), now also F7 failures
   (no recorded artistic font decision for those buttons). The
   workspace tokens file is v1-era/stale and is NOT evidence of
   the repair.
4. **Negative demonstration (default leak):** a fixture Type list
   with a price token pointing at "Fraunces (stand-in for
   Tiempos)" with no recorded decision FAILS the F7 check —
   proving the check fires on the default.
5. **Negative demonstration (missing decision):** a fixture
   decision record where a button has no font-decision line FAILS
   the F7 check; the same record WITH the decision (face + why +
   job + theme/brand fit) PASSES — proving the check fires on the
   missing decision, not on the element's presence.
6. **Negative demonstration (body face for main text):** a fixture
   heading token pointing at Fraunces FAILS the F4_TIGHT check;
   the same heading in the display face PASSES — proving the check
   fires on the body face for main visible text.
7. **Positive demonstration (permitted uses):** a long body
   paragraph in Fraunces PASSES; a small caption / meta row in
   Fraunces with a recorded class decision PASSES — proving the
   permitted set still works.
8. **Negative demonstration (blanket class abused):** a fixture
   that records one blanket class decision "all text: Fraunces"
   FAILS the F7 check — proving a blanket default masquerading as
   a class decision is not a class decision; the class must be
   genuinely uniform.
9. **Interconnection:** the F4_TIGHT/F7 tokens resolve in the built
   tree; the §10 pointer chain still targets the design-package
   rule, which carries the new rules (no dead end, no duplicate
   pointer lines needed).

The dry-run report (`fix21/dryrun35-report.md`) records the stale-
workspace caveat and the repair-reported status explicitly. No count
target: the re-trace is the check above, not an element recount.

## 7. Verify script — fix21/verify21.py

Follows the fix20/verify20.py pattern (read-only, against the BUILT
tree; imports rule constants from fix15, fix17, fix18, fix19, fix20,
fix21). Checks:

1. F4_TIGHT/F7 anchors present in Taste (built) and orchestrate
   (built), after the X1 rule in each.
2. F4_TIGHT_APP/F7_APP present in ui-ux-pro-max (built) and
   orch-build-mvp (built), after X1_APP in each.
3. STATIC21 present ×3 (Taste step 6, orchestrate Verify 5a,
   orch-build-mvp step 6); after STATIC20 in each; in orchestrate
   before the 5b bullet; STATIC21 contains the F7 per-element item.
4. POLISH_F21 present in polish-pass; TYPESET_F21 present in the
   typeset lens; TYPESET_CHECKBOX21_NEW present and the fix20
   checkbox GONE.
5. Fix20 anchors intact: F4_SCOPE/F5/F6/B1/X1 still present verbatim
   in Taste and orchestrate; F4_SCOPE_APP/F5_APP/F6_APP/B1_APP/X1_APP
   still present in ui-ux-pro-max and orch-build-mvp; STATIC20 still
   present ×3. Fix19 anchors intact: F4_RULE still present verbatim
   in Taste and orchestrate; F4_APP still present in ui-ux-pro-max;
   STATIC19 still present ×3; D19_RULE still present in Taste and
   orchestrate; D19_APP still present in ui-ux-pro-max and
   orch-build-mvp.
6. Canonical block still verbatim ×1 in all 11 files; D1 rule still
   present in Taste/orchestrate/polish-pass/orch-build-mvp.
7. vantage.md UNCHANGED in the built tree (display and body still
   Geologica) — this fix governs the deal, it does not rewrite theme
   data; the scope rule text names the collision handling.
8. Counts unchanged post-fix20: 166/72/123/87/15.
9. No banned terms (fix #16 scrub) in the built skill tree (excl.
   node_modules).
10. build.sh is the post-fix21 file (lines + md5 as recorded in
    fix21/MANIFEST.md) and still contains the fix15 + fix17 + fix19 +
    fix20 + fix21 blocks intact.
11. verify15.py 44/44, verify17.py 60/60, verify18.py 72/72,
    verify19.py 76/76, verify20.py 169/169 (run as subprocesses,
    exit 0 required).
12. Interconnection: the F4_TIGHT/F7 tokens resolve to defining
    phrases in the built tree; every §10 pointer line still targets
    the design-package rule, which carries the new rules (the
    pointer chain is connected, no dead end, no duplicate pointer
    lines added by this fix).

## 8. Checkers

- Audit #66, dry-run #35, sweep #29 (following fix #20's #65 / #34 /
  #28).
- Build twice (exit 0, diff 0) before the checkers; the fix-up round
  pattern from fix #17/#18/#19/#20 applies (re-audit + re-sweep after
  any fix-up; the bound holds: a bound-holding diff triggers no
  re-run).
- Backup: `build.sh.before-fix21` (first pre-fix21 copy, kept).
- The audit/dry-run/sweep run AFTER the implementation, against the
  final tree (rules in place).

## 9. Untouched / non-goals

- Fix #16 Grok pins and the Claude/Codex scrub (banned terms stay 0).
- Fix #15 anchors (44/44), fix #17 anchors (60/60), fix #18 anchors
  (72/72), fix #19 anchors (76/76), fix #20 anchors (169/169).
- The 11-file canonical block (verbatim).
- The Campus Eats artifact (read-only reference; do not touch).
- `fix11/fix11-stage.py` (never re-run).
- No commit, no bundle, no GitHub touch.
- No new inventory: no new less-flat-ui catalogue entries, no new
  Hallmark themes, no new font catalogue entries, no theme-file edits.
  Tiempos and Fraunces are named in rule text, not added as catalogue
  items.
