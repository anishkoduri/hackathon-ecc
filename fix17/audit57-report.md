# Audit #57 — fix #17 re-audit (after the MINOR-1 fix-up)

**Date:** Nov 11, 2026 (~18:44 CST)
**Auditor:** re-audit worker (check only — no plugin file edited, build.sh not run,
Campus Eats artifact not touched)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state:** build.sh 23,276 lines, md5 `1a999d763e6ec1fb16985d346b106df0`
(post-fix-up). Builds 3 and 4: manifest sha256
`d4f04f1031a0931c6c695d76eb1af689abfe835954e48875277163c424840031` on both,
file lists identical, diff 0; build logs end "build complete", "ERRORS: 0".
**Verifiers re-run by this audit:** `fix17/verify17.py` 59/59 PASS;
`fix15/verify15.py` 43/43 PASS.

## Verdict: CLEAN — 0 BLOCKING, 0 MINOR

Audit #56's single finding (MINOR-1) is fixed, and the fix-up touched
exactly one built file. Every rule, placement, exception, count, pin, and
standing rule re-checked out.

## Finding

None. MINOR-1 from audit #56 is verified fixed (see below).

## MINOR-1 fix verified

- `hackathon-ecc/skills/motion-patterns/SKILL.md:271` now reads:
  "See `motion-advanced` `useScrollRevealSafe` for the shared implementation."
- The corrected pointer is also in the source of the fix-up:
  `fix17/fix17.py:151` (PATTERNS_FAILSAFE_NOTE) and in the build.sh fix17
  block (`build.sh:23235`).
- No stale `useScrollReveal` pointer remains. The remaining `useScrollReveal`
  hits in the built tree are all legitimate, not pointers to the fail-safe:
  `motion-advanced/SKILL.md:22,34` (catalogue mentions of the hook),
  `:315` (hook heading), `:323` (the hook definition itself),
  `:332` and `:340` (used inside its own Usage example and inside
  `useScrollRevealSafe`, which wraps it and adds
  `setTimeout(() => setRevealed(true), 1500)` at `:339-343`).

## One-file manifest diff verified

`diff fix17/manifest1-files.txt fix17/manifest3-files.txt` touches exactly
one entry:

```
< 096206b2b0b47eb4518e018661fdc66093fe553adefe04a6a00655ab317b4100  ./skills/motion-patterns/SKILL.md
> 061fd1fc53786b257cf9fdd7ec845d9b1331615d55cdc480bae032e730a69498  ./skills/motion-patterns/SKILL.md
```

`diff manifest3-files.txt manifest4-files.txt` is empty (diff 0).
Manifest hashes: build 1/2 `3be418fa…` → build 3/4 `d4f04f10…`, matching the
task statement. No other file changed in the fix-up.

## What was checked and passed

### Fix #17 rules — present at assigned placements, verbatim, x1 each
- **U1** Taste step 4a `skills/design-taste-frontend/SKILL.md:248` (full rule,
  ≥3 per build, four-part test, six-field entries, ≥1 on primary page);
  app mirror `skills/ui-ux-pro-max/SKILL.md:95`; record
  `skills/less-flat-ui/SKILL.md:530`; static checks Taste `:302`,
  orchestrate `:61`, orch-build-mvp `:53` — STATIC_CHECKS x1 in all three.
- **T1** Taste `:250`, ui-ux-pro-max `:89` (verbatim x1 each); typeset lens
  Rules `:78` + Verify `:97`; polish-pass harmony `:22`. 60% fill ratio and
  25% dead-space band present as specified.
- **F1** Taste `:252`, ui-ux-pro-max `:89` (verbatim x1 each, "extends fix
  #15 C1–C3, does not replace them"); polish-pass harmony `:22` (Source cells,
  consistency only).
- **E1** verbatim x1 in all four files — Taste `:254`, orchestrate `:94`,
  orch-build-mvp `:42`, ui-ux-pro-max `:97`. Wording is the ACTIVE PUSH
  ("MUST push boundaries and aim to be trailblazing", nine-point bounds,
  "Distinctiveness itself is browser-qa's verdict alone"). Zero "may invent"
  (case-insensitive grep, whole built tree excl. node_modules) — the SPEC
  draft's permission wording did not leak.
- **M1** motion-patterns rule 9 `:55` + motion-foundations rule 9 `:60`
  (verbatim, identical); **M2** rule 10 in both (`:56`, `:61`); fail-safe
  note motion-patterns `:271` (fixed — see above); `useScrollRevealSafe`
  motion-advanced `:339-343` with `setTimeout(..., 1500)`; **M3–M5**
  make-interfaces-feel-better Motion section (`:108` "Default motion set
  (fix #17, v4-level)" + full M3/M4/M5 texts) and checklist `:162-164`;
  **M6** motion-foundations Accessibility `:179` (CSS block + JS guard,
  reduced-motion render noted-or-recorded-as-not-run).
- Rule numbering clean: both motion skills had rules 1–8 pre-existing;
  M1/M2 are 9/10 with no collision. M1's "(motion-patterns rule 7)" citation
  is correct (rule 7 at motion-patterns `:53`, example at `:266`).
- **Framing:** every fix17 rule is a static check / candidate evidence /
  consistency check, never a screen verdict. U1/F1/STATIC_CHECKS say "never
  a screen verdict"; M2/M3/M4 findings are "a finding, fed to the fix batch";
  E1 bound (9) and STATIC_CHECKS defer distinctiveness to "browser-qa's
  verdict alone". The only "blocks" is E1's "a floor/ban break blocks", which
  is the SPEC draft's own wording for a blocking static-check failure.
  (Re-checked independently this audit, not just verify17's substring checks.)

### Sticker exceptions — scoped, named, dated; do-nots intact
- `skills/design-taste-frontend/references/hallmark/references/themes/sticker.md`:
  exception A (hand-drawn ink marks) `:90` and exception B (scroll
  rise-and-settle entrances) `:91` in a "Scoped exceptions (decided, not
  drift)" section (`:88`); each states the do-not stays intact beyond it and
  carries "Added at Anish's direction in the Campus Eats cold-start render,
  Nov 11, 2026."
- Motion line `:74` points at the exception ("nothing on scroll, except the
  scoped exception in 'Scoped exceptions' below…"). All five do-nots otherwise
  verbatim, including "Never a drawn sticker, mascot or doodle" and "Never
  pink text on the paper".

### R3 widening — present, no catalogue entries added
- `skills/less-flat-ui/SKILL.md:14`: "A theme-matched handmade surface
  treatment — tape, perforation, washi, a hand-drawn ink mark — counts as a
  treatment kind (fix #17)…" Treatments still number exactly 1..23
  (`### 1.` through `### 23.`, `:106`–`:487`).

### Fix #15 anchors — no regression (spot-checked beyond verify17)
- Canonical block verbatim x1 in all 11 files (verify17, plus this audit's
  independent count: 11 files contain "Every element application is recorded
  per surface").
- D1 in Taste / orchestrate / polish-pass / orch-build-mvp (verify17).
- R1 Taste `:244`; R4 Taste `:276`; R5 Taste `:246`; C1/C2 Taste `:246`;
  C3 Taste `:298`. fix #12 carve-out still present in
  `impeccable-critique.md` ("Questions skipped: first build — proceeding on
  stated assumptions (hackathon-mode §7)") — fix11/fix11-stage.py NOT re-run.

### Fix #16 — no regression
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5): 0 in
  the whole built tree excl. node_modules (this audit's scope-wide grep).
- Model pins untouched: `grok-4.7-high` 52 whole-tree occurrences,
  `cursor-grok-4.6-high-fast` 100; zero bare `grok-4.6-high-fast`; zero
  bracket syntax on slugs; `reasoning_effort` 2×, no bare `effort:` model param.
- Counts unchanged at the fix16 final state (verify17): skills 166, agents 72,
  rules 123, commands 87, hooks 15 (hooks.json declares 15; the `hooks/`
  directory holds 17 files because `adapter.js` + `hooks.json` are not hook
  entries).

### Standing rules — all intact
- "more, not bolder" present (6 files); craft-floor bans absolute (Taste
  `:246` restates "its bans are absolute as static/code-level checks");
  Hallmark floor binds; no violet introduced by fix17 (the "violet" hits in
  the tree are pre-existing: the no-violet bans themselves, the Ultraviolet
  and lumen theme files, and E1 bound 7 "use no violet"); anti-derivative;
  snapshot-before-redesign + 2-round fresh-verdict budget
  (`fresh-verdict rounds used: N/2`, shared across 5b and Verify step 6)
  intact in orchestrate `:62` and orch-build-mvp `:53`.
- No adjudicated item re-flagged and none mentioned in any fix17 addition.
- SPEC draft §C 30–34 band did not leak: 0 hits for "30–34"/"30-34" in the
  built tree. (Parent override to 59–63 is in fix17.py's header; the band
  itself is a re-trace target, not tree text.)

### No new inventory; 1500ms fail-safe is a pattern, not inventory
- Counts unchanged (166/72/123/87/15, verify17). No new skill, treatment,
  or theme. `useScrollRevealSafe` is a hook variant inside the existing
  motion-advanced skill, as the spec allows for M2.

### Internal consistency — coherent, no contradictions
- U1/T1/F1/E1/M1–M6 wordings identical across placements (verbatim x1
  checks above; T1/F1 identical in Taste and ui-ux-pro-max; E1 identical in
  all four files; M1/M2 identical in both motion skills).
- M1 Option B scope vs sticker exception B cohere, not contradict: M1
  keeps the Taste landing-page scroll ban
  (`references/motion.md:38` "Scrolling moves nothing but the dealt moment",
  intact) and names exception B as "the theme's decision, not this rule's".

## Not checked
- The Campus Eats artifact itself (out of scope; must not be touched) — the
  re-trace target (59–63, final 61 literal) is not re-derived here.
- Live behaviour (no browser run in this audit): whether the built rules
  fire in a cold-start rebuild, and the parent-guidance open item on R1
  iris-opens + R4 hero loop compliance in the artifact, are for the re-trace
  / dry-run, not this tree audit.
- `build.sh.before-fix17` backup exists (confirmed present, carried over from
  audit #56).
