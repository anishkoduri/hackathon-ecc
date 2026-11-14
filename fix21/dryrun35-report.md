# Dry-run #35 — Fix #21 font-scope + per-element-decision check

- **Date:** 2026-11-11, evening CST. Worker: dry-run worker (fix #21), check-only.
- **Scope kept:** read-only against the plugin tree and the built tree. Two files written, both inside `fix21/`: this report and the fixture runner `fix21/dryrun35-fixtures.py`. No staged source, `build.sh`, built-tree file, or verifier edited; no `fix21/MANIFEST.md` written; no commit, no bundle, no GitHub touch. Campus Eats artifact not touched (and not read — see §0).
- **What this dry-run is:** a font-scope + per-element-decision check, NOT an element recount (SPEC §6). No count target; the re-trace is the nine checks below.
- **Verdict: PASS.** All nine SPEC §6 items pass (see §1–§9).

## 0. Source limitations — read this first

1. **The workspace Campus Eats artifact is v1-era and STALE.** `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` still records `--font-body: "Sofia Sans", ui-sans-serif, system-ui, sans-serif;` and pre-repair typography lines. It does NOT reflect the Nov 11 evening font repair. Per SPEC §1, it is NOT evidence of the repair and was not used in this dry-run at all — not even as a negative demonstration. **This worker did NOT read any Campus Eats artifact file.**
2. **Repair compliance (§3) is REPAIR-REPORTED, NOT re-verified.** The statement that the repaired artifact complies with the refined scope rests on the repair's verified solution as recorded in `fix19/SPEC.md` §1 and `fix21/SPEC.md` §1, plus the recorded fix #20 findings in `fix20/SPEC.md` §11 — not on any source this worker could inspect. **This worker did NOT re-verify the repair from this VM — the live artifact source does not exist in this workspace.** If the parent wants independent verification, it needs the live repaired artifact source.
3. **No dry-run #31 / #32 report file exists in this workspace.** The `.btn` / `.roll-btn` findings are cited from the recorded text in `fix20/SPEC.md` §11 (which itself records dry-run #31 item 3 and the dry-run #32 `.step-btn` correction) and from `fix21/SPEC.md` §1. No separate dryrun31/dryrun32 report file was found under `~/workspace/hackathon-plugin/` (searched; only `fix20/SPEC.md`, `fix20/MANIFEST.md`, and `fix21/SPEC.md` mention them).
4. The built-tree evidence (§1, §2, §9) IS independently verified: `verify21.py` was re-run by this worker this session, and the greps below were run against `~/workspace/hackathon-plugin/hackathon-ecc/skills/` this session. The fixture evidence (§4–§8, plus the §3 supporting fixture) IS produced by this worker: `fix21/dryrun35-fixtures.py` applies the STATIC21/F4_TIGHT/F7 logic, importing the rule constants from `fix21/fix21.py` — the rule texts are never retyped from memory.

## 1. Rule presence — verify21.py re-run by this worker: PASS (101/101)

Re-ran `python3 fix21/verify21.py` from `~/workspace/hackathon-plugin/` this session (exit 0). Final line: **101/101 checks pass.** The run's tail (all lines PASS) confirms, among others:

- `PASS F4_TIGHT Taste step 4a` / `F7 Taste step 4a` / `fix21 rules sit after the X1 rule in Taste step 4a` (same three for the orchestrate design-package rule)
- `PASS F4_TIGHT_APP ui-ux-pro-max anti-generic bar` / `F7_APP ...` / app mirrors after X1_APP (same for orch-build-mvp step 4)
- `PASS STATIC21 Taste step 6` / `orchestrate Verify 5a` / `orch-build-mvp step 6`; after STATIC20 in each; before the 5b bullet in orchestrate; contains the F7 per-element item
- `PASS POLISH_F21 present in polish-pass harmony` / after POLISH_F20; `TYPESET_F21 present in typeset lens` / after TYPESET_F20; typeset checkbox updated to fix #21 (fix20 checkbox gone); checkbox names the F7 per-element decision
- Fix20 anchors intact (F4_SCOPE/F5/F6/B1/X1, app mirrors, STATIC20 ×3); fix19 anchors intact (F4_RULE, D19_RULE, F4_APP, STATIC19 ×3, D19_APP); canonical block verbatim ×1 in all 11 files; D1 rule still in all four files; fix18 FEATURES_CUTS_SECTION and fix17 E1 still present
- `PASS vantage.md still names Geologica for display AND body (unchanged)`
- `PASS counts 166/72/123/87/15 (unchanged)`
- `PASS banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)`
- `PASS build.sh contains the fix21 block marker` (+ fix20/fix19/fix17/fix15 markers); `PASS build.sh has MORE lines than post-fix20 (23,609)`
- `NOTE: fix21/MANIFEST.md not yet written by the coordinator; measured build.sh lines=23647, md5=8dfacb47a2a6698d47e4b4a5f8d9126c` — measured independently by this worker with `wc -l` + `md5sum`: **23,647 lines, md5 `8dfacb47a2a6698d47e4b4a5f8d9126c`**, matching the task's stated gate numbers. (No MANIFEST exists yet, so the verifier's check 10 passes on the measured lines + md5, as its docstring provides; the coordinator still has to write `fix21/MANIFEST.md`.)
- `PASS fix15 verifier still passes (44/44 checks pass)` / `fix17 verifier still passes (60/60 checks pass)` / `fix18 verifier still passes (72/72 checks pass)` / `fix19 verifier still passes (76/76 checks pass)` / `fix20 verifier still passes (169/169 checks pass)`
- Interconnection checks (see §9): F4_TIGHT/F7 tokens resolve; design-package rule exists and carries the new rules; all 32 pointer lines target the design-package rule.

**Item 1: PASS.**

## 2. Criteria coverage — every scope token named as a check trigger in STATIC21: PASS

The STATIC21 paragraph is present verbatim ×3 in the built tree — `design-taste-frontend/SKILL.md:333`, `orchestrate/SKILL.md:69` (inside the 5a paragraph), `orch-build-mvp/SKILL.md:76`. Quoted in full from `design-taste-frontend/SKILL.md:333`:

> "**Fix #21 static checks (all static checks, never screen verdicts).** (F4 tight) The Type list marks the body face as long-body-and-small-text-only — no token for main visible text points at the body face; the body face serves long-length body text and small incidental text only. (F7) Every text element in the Type list — or every genuinely uniform text class — carries its recorded artistic font decision (face + why + job + theme/brand fit); a text element with no recorded decision is an incomplete build; a main visible text element (heading, display, hero, prominent label, price, name, call to action) set in the body face is an incomplete build; a blanket 'all text' class line is not a class decision. (F7 record) The decision record lists the font decision per text element or per uniform class; the D19 reason covers the font choice."

Token-by-token coverage against the three scope tokens SPEC §6 item 2 names:

| # | Scope token (SPEC §6 item 2) | Covered? | Covering trigger phrase in STATIC21 (built tree, all three files) |
|---|---|---|---|
| 2a | Body face only for long body + small incidental text | YES | "(F4 tight) The Type list marks the body face as long-body-and-small-text-only"; "the body face serves long-length body text and small incidental text only" |
| 2b | Every text element has a recorded artistic font decision | YES | "(F7) Every text element in the Type list — or every genuinely uniform text class — carries its recorded artistic font decision (face + why + job + theme/brand fit); a text element with no recorded decision is an incomplete build"; "(F7 record) The decision record lists the font decision per text element or per uniform class" |
| 2c | Main visible text uses the display/artistic face (never the body face as a default) | YES | "no token for main visible text points at the body face"; "a main visible text element (heading, display, hero, prominent label, price, name, call to action) set in the body face is an incomplete build" — the main-visible element list is spelled out in full. The positive side (display/artistic face) is stated in the co-located F7 rule text (`design-taste-frontend/SKILL.md:277` line range, F4_TIGHT + F7 after X1): "Main text we see visually … uses the unique important font (fix #20 F5) or another artistic face chosen through the skills, never the body face as a default" |

One honest note, in the dry-run #30 style: STATIC21's trigger for 2c is phrased as the prohibition (a main visible token in the body face is an incomplete build) rather than the positive prescription (use the display/artistic face). The positive prescription lives in the F7 rule text in the same skill file, one step up (step 4a, F4_TIGHT/F7 at `design-taste-frontend/SKILL.md:277` onward, verified present by verify21 check 1). The check fires on the bug through the prohibition; the rule text supplies the positive direction. This is coverage by the check text as a whole, not by the STATIC21 paragraph alone — recorded here so the parent can decide whether the positive wording belongs in STATIC21 too.

**Item 2: PASS** (3/3 scope tokens named as check triggers in the STATIC21 text, with the 2c note above).

## 3. Repair compliance — REPAIR-REPORTED, NOT re-verified: PASS as reported

**Status, stated explicitly: this is the repair's verified solution as recorded in `fix19/SPEC.md` §1 and `fix21/SPEC.md` §1, plus the recorded fix #20 findings in `fix20/SPEC.md` §11. This worker did NOT re-verify it from this VM — the live artifact source does not exist in this workspace (see §0). No Campus Eats artifact file was read.**

What the recorded sources state as the repair's verified solution (`fix19/SPEC.md` §1):

- Self-hosted, preloaded STATIC font files — Fraunces static woff2 instances (400/500/600/700/800, latin + latin-ext, opsz 24, WONK off), generated from the OFL Fraunces variable font with fontTools instancer/subsetter, confirmed static (no fvar) with correct usWeightClass.
- The variable Sofia Sans files were deleted; zero remaining 'Sofia' or 'system-ui' references; zero generic sans-serif fallbacks; preloads for the four first-paint faces; `font-synthesis: none`; `text-size-adjust: 100%`; inline SVG text stacks updated.
- Display type stays Bowlby One SC.

Compliance of that reported solution against the fix #21 refined scope:

| Refined-scope requirement | Reported repair fact | Complies? |
|---|---|---|
| Long body text in Fraunces (the recorded free stand-in for Tiempos) | Body is Fraunces, the recorded stand-in, set at the 1.55 reading line-height per `fix19/SPEC.md` §1 | **YES, as reported.** Long-length body text is exactly the first permitted home of the body face. |
| Small incidental text in Fraunces (the fix #20 F5 small-labels permission: ordinary small labels — nav links, table heads, captions, chips, form labels, meta rows — a step smaller, sentence case, untracked) | The repair set plain text in Fraunces broadly (`fix21/SPEC.md` §1); the small-labels class is the body face's second permitted home under fix #21, now conditioned on a recorded F7 decision per element or per genuinely uniform class | **YES, as reported, for the scope.** The scope permits small text in Fraunces. Caveat: the repair record does not state whether each small-text element carries its recorded F7 decision — F7's recording requirement is a build-record matter, not a repair fact, and F7 did not exist when the repair was made. The parent should not read this as evidence the decisions are recorded. |
| No main visible text in the body face | **EXCEPTION — recorded:** the artifact's CTA buttons `.btn` (`index.html:193`) and `.roll-btn` (`:679`) are set in Fraunces, the body face — a genuine F5 leak in a pre-fix-#20 artifact (`fix20/SPEC.md` §11, recording dry-run #31 item 3). `.step-btn` is NOT a leak — `font-family: "Bowlby One SC", "Fraunces", Georgia, serif` at `:485`, display face primary with Fraunces only as fallback (dry-run #32 correction, same section). | **NO — as recorded, the two CTAs remain leaks.** A call to action is main visible text; under fix #21 it fails F4_TIGHT (body face for main text) and F7 (no recorded artistic font decision for those buttons). The package rule correctly catches exactly this leak (dry-run #31 item 4 proved it for STATIC20; this dry-run's §4-style fixture proves it for F4_TIGHT/F7 — see below). Any future build re-traced through the fixed package fails STATIC21 on its CTAs until re-dealt in the display face with a recorded decision. |

Supporting fixture (run by this worker in `fix21/dryrun35-fixtures.py`, modelling the recorded finding — no artifact file read):

- `item3 F7: recorded .btn/.roll-btn Fraunces CTAs, no decision -> FAIL` — "element '.btn CTA' has NO recorded artistic font decision; main visible token '.btn CTA' set in the body face; element '.roll-btn CTA' has NO recorded artistic font decision; main visible token '.roll-btn CTA' set in the body face"
- `item3 F4_TIGHT: recorded .btn/.roll-btn Fraunces CTAs -> FAIL` — "main visible token '.btn CTA' points at body face 'Fraunces (stand-in for Tiempos)'; main visible token '.roll-btn CTA' points at body face 'Fraunces (stand-in for Tiempos)'"

**Stale-workspace caveat, recorded explicitly:** the workspace tokens file `~/workspace/cold-start-render/campus-eats/docs/design-tokens.md` is v1-era/stale and is NOT evidence of the repair. It was not used in this dry-run.

**Item 3: PASS as repair-reported** — the repaired artifact complies with the refined scope for its long body text and small incidental text (Fraunces, per the repair's verified solution), and its known `.btn` / `.roll-btn` Fraunces CTAs remain recorded F5 leaks, now also F7 failures. The compliance claim depends entirely on the repair's own verification; no independent check was possible from this VM.

## 4. Negative demonstration (default leak) — price token in Fraunces, no decision, FAILS F7: PASS

Fixture (from `fix21/dryrun35-fixtures.py`, script output quoted verbatim):

> `PASS item4 F7: price token in Fraunces, no recorded decision -> FAIL`
> `     element 'price' has NO recorded artistic font decision; main visible token 'price' set in the body face`

The fixture is a Type list with one token: element `price` (role: main visible text), face `Fraunces (stand-in for Tiempos)`, decision `None`. The script's F7 check fails it on two independent grounds — no recorded decision, and a main visible token set in the body face. That is the default leak Anish named: a price set in the body face by default, with no artistic font decision behind it. The check fires on the default.

**Item 4: PASS.**

## 5. Negative demonstration (missing decision) — button without a decision FAILS; with the decision PASSES: PASS

Fixtures (script output quoted verbatim):

> `PASS item5a F7: button with no font-decision line -> FAIL`
> `     element 'button (.btn)' has NO recorded artistic font decision`
> `PASS item5b F7: same button WITH its decision -> PASS`
> `     every text element carries its recorded artistic font decision (face + why + job + theme/brand fit); no blanket class; no main visible text in the body face`

5a: element `button (.btn)`, face the display face (Bowlby One SC), decision `None` — fails F7 on the missing decision alone, even though the face itself is correct. This is the control that proves the check fires on the missing decision, not on the element's presence or its face.

5b: the same button, same face, WITH the decision recorded — face Bowlby One SC; why "the dealt display face carries the call to action so it reads as the one loud moment on the card"; job "make the CTA the visual anchor and the click target"; theme/brand fit "matches the sticker theme's loud display type and the brand's bold, playful voice" — passes F7. Same element, same face; only the decision changes. The check fires on the missing decision.

**Item 5: PASS.**

## 6. Negative demonstration (body face for main text) — heading in Fraunces FAILS F4_TIGHT; in the display face PASSES: PASS

Fixtures (script output quoted verbatim):

> `PASS item6a F4_TIGHT: heading token in Fraunces -> FAIL`
> `     main visible token 'heading (h1)' points at body face 'Fraunces (stand-in for Tiempos)'`
> `PASS item6b F4_TIGHT: same heading in the display face -> PASS`
> `     no main visible token points at the body face; body face serves long body / small text only`
> `PASS item6b F7: same heading, decision recorded -> PASS`
> `     every text element carries its recorded artistic font decision (face + why + job + theme/brand fit); no blanket class; no main visible text in the body face`

6a: element `heading (h1)`, face `Fraunces (stand-in for Tiempos)` — fails F4_TIGHT. 6b: the same heading, face Bowlby One SC (the dealt display face), with its full decision recorded (face + why + job + theme/brand fit) — passes both F4_TIGHT and F7. Same element, only the face (and the recorded decision) changes. The check fires on the body face for main visible text.

**Item 6: PASS.**

## 7. Positive demonstration (permitted uses) — long body in Fraunces PASSES; small caption/meta row in Fraunces with a class decision PASSES: PASS

Fixtures (script output quoted verbatim):

> `PASS item7a F4_TIGHT: long body paragraph in Fraunces -> PASS`
> `     no main visible token points at the body face; body face serves long body / small text only`
> `PASS item7a F7: long body paragraph, decision recorded -> PASS`
> `     every text element carries its recorded artistic font decision (face + why + job + theme/brand fit); no blanket class; no main visible text in the body face`
> `PASS item7b F4_TIGHT: caption/meta row in Fraunces (small text) -> PASS`
> `     no main visible token points at the body face; body face serves long body / small text only`
> `PASS item7b F7: caption/meta row, uniform class decision recorded -> PASS`
> `     every text element carries its recorded artistic font decision (face + why + job + theme/brand fit); no blanket class; no main visible text in the body face`

7a: element `body paragraph (long)`, role long-body, face Fraunces, with its decision recorded (why: the body face is the reading face at 1.55 line-height; job: carry running paragraphs of reading prose; theme fit: the theme's warm reading voice) — passes F4_TIGHT and F7. The long-body permission works.

7b: elements `caption` and `meta row`, role small, face Fraunces, sharing ONE recorded class decision for the class `captions/meta rows` (face + why + job + theme/brand fit, naming the class) — the class is genuinely uniform (same face, same smaller step, same job across its members) — passes F4_TIGHT and F7. The small-text permission works, including through a genuine uniform-class decision. This is the fix #20 F5 small-labels permission with the fix #21 F7 condition attached, exactly as SPEC §5 resolves the tension.

**Item 7: PASS.**

## 8. Negative demonstration (blanket class abused) — "all text: Fraunces" FAILS F7: PASS

Fixture (script output quoted verbatim):

> `PASS item8 F7: blanket 'all text: Fraunces' class line -> FAIL`
> `     element 'heading (h1)' is covered only by a blanket 'all text' class line -- not a class decision; main visible token 'heading (h1)' set in the body face; element 'price' is covered only by a blanket 'all text' class line -- not a class decision; main visible token 'price' set in the body face; element 'body paragraph (long)' is covered only by a blanket 'all text' class line -- not a class decision`

The fixture records ONE class decision, class `all text`, face Fraunces, covering a heading, a price, and a long body paragraph. The script's F7 check fails every element on the blanket ground: a blanket default masquerading as a class decision is not a class decision — the class must be genuinely uniform, and "all text" is not a class (it spans main visible text, prices, and body prose with different jobs and different permitted faces). The heading and price fail additionally on the body-face-for-main-text ground. Contrast with §7 item 7b, where the genuinely uniform class `captions/meta rows` passes: the check distinguishes a real class decision from a blanket default.

**Item 8: PASS.**

## 9. Interconnection — F4_TIGHT/F7 tokens resolve; the §10 pointer chain targets the design-package rule, which carries the new rules: PASS

Evidence, verified by this worker this session (two independent legs: verify21 check 12, and this worker's own greps):

- verify21 check 12 (re-run §1): `PASS interconnection: F4_TIGHT token resolves to a defining phrase in the built tree`; `PASS interconnection: F7 token resolves to a defining phrase in the built tree`; `PASS interconnection: the design-package rule exists in built orchestrate`; `PASS interconnection: the design-package rule carries the new F4_TIGHT/F7 rules (no dead end)`; `PASS interconnection: all 32 design-decision pointer lines still target the design-package rule (no duplicate lines added)`.
- This worker's own greps (built tree, `~/workspace/hackathon-plugin/hackathon-ecc/skills/`):
  - `grep -rn "Design-decision pointer:" skills --include="SKILL.md" | wc -l` → **32** pointer lines.
  - Lines among them NOT containing `design-package rule` → **0** (every pointer targets the design-package rule).
  - `Long body and small text only` (the F4_TIGHT defining phrase) occurs ×1 in `skills/design-taste-frontend/SKILL.md` and ×1 in `skills/orchestrate/SKILL.md` (Taste step 4a line 277; orchestrate line 122).
  - `Every text element gets an artistic font design decision` (the F7 defining phrase) occurs ×1 in each of the same two files.
  - The design-package rule exists in built orchestrate (`skills/orchestrate/SKILL.md:98`, "**Design-package rule (row 10 — relevance by surface type, never by size).**") and carries the F4_TIGHT + F7 rules (orchestrate line 122, after X1 — verify21 check 1 confirms the ordering).
- No duplicate pointer lines were added by this fix: the pointer count is still 32, the same count fix #20's verify20 check 14 asserted. The chain is pointer → design-package rule → F4_TIGHT/F7, connected, with no dead end — the same reasoning `fix20/SPEC.md` §12.5 gives for BIND/INNOV/H1, applied here to the fix #21 rules, which live IN the design-package rule (Taste step 4a / orchestrate) per `fix21/SPEC.md` §3.

**Item 9: PASS.**

## Verdict summary

| # | SPEC §6 item | Result |
|---|---|---|
| 1 | Rule presence — verify21.py passes | **PASS** — re-run by this worker, 101/101, exit 0; build.sh 23,647 lines, md5 `8dfacb47a2a6698d47e4b4a5f8d9126c` |
| 2 | Criteria coverage — all three scope tokens named as check triggers in STATIC21 | **PASS** — 3/3 (see the 2c note in §2: the positive display-face prescription lives in the F7 rule text, not literally inside the STATIC21 paragraph) |
| 3 | Repair compliance | **PASS as repair-reported** — NOT re-verified from this VM; `.btn`/`.roll-btn` remain recorded F5 leaks, now also F7 failures; stale-workspace caveat recorded |
| 4 | Negative demonstration (default leak) — price in Fraunces, no decision, FAILS F7 | **PASS** — script-produced FAIL |
| 5 | Negative demonstration (missing decision) — button without decision FAILS, with decision PASSES | **PASS** — script-produced FAIL then PASS |
| 6 | Negative demonstration (body face for main text) — heading in Fraunces FAILS F4_TIGHT, in display face PASSES | **PASS** — script-produced FAIL then PASS |
| 7 | Positive demonstration (permitted uses) — long body PASSES; caption/meta row with class decision PASSES | **PASS** — script-produced PASS ×4 |
| 8 | Negative demonstration (blanket class abused) — "all text: Fraunces" FAILS F7 | **PASS** — script-produced FAIL |
| 9 | Interconnection — F4_TIGHT/F7 resolve; §10 pointer chain targets the design-package rule, which carries the new rules | **PASS** — verify21 check 12 + own greps (32 pointers, 0 off-target) |

**Overall: PASS.**

## Notes for the parent / audit worker

1. **The 2c wording call (§2).** STATIC21's trigger for main-visible text is phrased as the prohibition (a main visible token in the body face is an incomplete build); the positive prescription (use the display/artistic face) lives in the F7 rule text in the same skill file. If the audit wants every token literal inside STATIC21 itself, that is a one-line wording addition, not a rule gap — the check fires on the bug either way.
2. **F7 recording for the repair (§3).** The repair record confirms the pairing (Bowlby One SC + Fraunces) and the permitted-scope facts, but does not state whether each small-text element carries its recorded F7 decision — F7 did not exist when the repair was made. That is a build-record matter for a future build, not a defect in the repair.
3. **`fix21/MANIFEST.md` not yet written.** verify21's check 10 passes on measured lines + md5 (23,647 / `8dfacb47a2a6698d47e4b4a5f8d9126c`), as its docstring provides; the coordinator still has to write the MANIFEST. This dry-run did NOT write it (out of scope for this worker).
4. **No dry-run #31 / #32 report files in the workspace (§0.3).** The `.btn` / `.roll-btn` / `.step-btn` findings are cited from `fix20/SPEC.md` §11 and `fix21/SPEC.md` §1. If the audit wants the original dry-run reports, they are not under `~/workspace/hackathon-plugin/`.

## Files / evidence used (read-only, except the two files written)

- `~/workspace/hackathon-plugin/fix21/SPEC.md` (§1 evidence, §2 rules, §6 dry-run definition, §7 verify script)
- `~/workspace/hackathon-plugin/fix21/fix21.py` (rule constants imported by the fixture runner — never retyped)
- `~/workspace/hackathon-plugin/fix21/verify21.py` (re-run this session: **101/101**, exit 0)
- `~/workspace/hackathon-plugin/fix21/dryrun35-fixtures.py` (written this session; run: **13/13 fixture expectations met**, exit 0)
- `~/workspace/hackathon-plugin/fix19/SPEC.md` §1 (repair's verified solution)
- `~/workspace/hackathon-plugin/fix20/SPEC.md` §11 (recorded `.btn`/`.roll-btn` F5 leaks; `.step-btn` not a leak)
- `~/workspace/hackathon-plugin/fix19/dryrun30-report.md` (format example)
- Built tree (read-only greps this session): `~/workspace/hackathon-plugin/hackathon-ecc/skills/design-taste-frontend/SKILL.md:277, 333`; `orchestrate/SKILL.md:69, 98, 122`; `orch-build-mvp/SKILL.md:76`; 32 `Design-decision pointer:` lines, 0 off-target
- Artifact: NO Campus Eats artifact file was read by this worker (see §0)
