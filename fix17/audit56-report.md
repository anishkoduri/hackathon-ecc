# Audit #56 — fix #17 (back-port ALL Campus Eats render feedback)

**Date:** Nov 11, 2026 (~18:35 CST)
**Auditor:** audit worker (check only — no plugin file edited, build.sh not run,
Campus Eats artifact not touched)
**Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
**Build state:** build.sh 23,276 lines, md5 `0775d6f33c5eeb4cf509fdee1cd319d7`
(post-fix17, matches the implementation report). Two builds: manifest sha256
`3be418faa2f340890dcb7b07e284f20b825c08996e2114de9f3f80da727070ec` on both,
file lists identical, diff 0; build logs end "build complete", Errors (0).
**Verifiers re-run by this audit:** `fix17/verify17.py` 59/59 PASS;
`fix15/verify15.py` 43/43 PASS.

## Verdict: NOT CLEAN — 0 BLOCKING, 1 MINOR

The single finding is a wrong cross-reference target in one fix17 note
(the fail-safe pointer names the base hook, not the fail-safe hook). Every
rule, placement, exception, count, pin, and standing rule checked out.

## Finding

### MINOR-1 — motion-patterns fail-safe note points at the wrong hook
**File:** `hackathon-ecc/skills/motion-patterns/SKILL.md:271`
**Text:** "See `motion-advanced` `useScrollReveal` for the shared implementation."
**Problem:** the shared implementation of the 1500ms fail-safe is
`useScrollRevealSafe` (`skills/motion-advanced/SKILL.md:336-343`, which wraps
`useScrollReveal` and adds `setTimeout(() => setRevealed(true), 1500)`).
`useScrollReveal` itself (`motion-advanced/SKILL.md:323-332`) contains no
timer and no fail-safe. A reader following the pointer lands on a hook
without the fail-safe and could implement M2 without one.
**Why MINOR, not BLOCKING:** the fail-safe is correctly implemented
(`useScrollRevealSafe`, verified), M2's rule text is correct and identical in
both motion skills (`motion-patterns/SKILL.md:56`,
`motion-foundations/SKILL.md:61`), and the note's own first two sentences
correctly describe the mechanism — only the cross-reference target is wrong.
**Fix:** one-word change in the fix17 build.sh patch block (or the next fix):
`useScrollReveal` → `useScrollRevealSafe` at `motion-patterns/SKILL.md:271`.

## What was checked and passed

### Fix #17 rules — present at assigned placements, verbatim, x1 each
- **U1** Taste step 4a `skills/design-taste-frontend/SKILL.md:248` (full rule,
  ≥3 per build, four-part test, six-field entries, ≥1 on primary page);
  app mirror `skills/ui-ux-pro-max/SKILL.md:95`; record
  `skills/less-flat-ui/SKILL.md:530`; static checks Taste `:302`,
  orchestrate `:61`, orch-build-mvp `:53` — STATIC_CHECKS verbatim x1 in all
  three (re-checked independently, not just verify17's substring checks).
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
  / "MAY invent" / "may invent within reason" in the built tree (case-insensitive
  grep, excl. node_modules) — the SPEC draft's permission wording did not leak.
- **M1** motion-patterns rule 9 `:55` + motion-foundations rule 9 `:60`
  (verbatim, identical); **M2** rule 10 in both (`:56`, `:61`); fail-safe note
  motion-patterns `:271` (see MINOR-1); `useScrollRevealSafe`
  motion-advanced `:336-343` with `setTimeout(..., 1500)`; **M3–M5**
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

### Sticker exceptions — scoped, named, dated; do-nots intact
- `skills/design-taste-frontend/references/hallmark/references/themes/sticker.md`:
  exception A (hand-drawn ink marks) and exception B (scroll rise-and-settle
  entrances) in a "Scoped exceptions (decided, not drift)" section; each
  states the do-not stays intact beyond it and carries "Added at Anish's
  direction in the Campus Eats cold-start render, Nov 11, 2026."
- Motion line points at the exception ("nothing on scroll, except the scoped
  exception in 'Scoped exceptions' below…"). All five do-nots otherwise
  verbatim, including "Never a drawn sticker, mascot or doodle" and "Never
  pink text on the paper".
- Exception A naming the drawn seal/emblem (Taco Compass) is within parent
  decision 1(a)'s "hand-drawn ink scribble/doodle … one-off ink-on-paper
  element" scope.

### R3 widening — present, no catalogue entries added
- `skills/less-flat-ui/SKILL.md:14`: "A theme-matched handmade surface
  treatment — tape, perforation, washi, a hand-drawn ink mark — counts as a
  treatment kind (fix #17): the kind is the treatment application on one
  surface, not the catalogue entry; the 23-entry catalogue is the vocabulary,
  not the limit." Treatments still number exactly 1..23; staged-vs-standalone
  less-flat-ui diff still exactly the 3 patch hunks (verify17).

### Fix #15 anchors — no regression (spot-checked beyond verify17)
- Canonical block verbatim x1 in all 11 files (verify17); D1 in Taste /
  orchestrate / polish-pass / orch-build-mvp (verify17).
- R1 Taste `:244`; R2 diagram row `:153` ("1-2 by default, pulsing; 0 only
  with a recorded reason"); R3 less-flat-ui `:14`; R4 Taste `:276`;
  R5 Taste `:246`; C1/C2 Taste `:246`; C3 Taste `:298`; D1 Taste (verify17).
  (Note: "fix #15 R2"/"fix #15 R3" have 0 literal hits in Taste because R2 is
  the table-row replacement and R3 lives in less-flat-ui — both present in
  their fix15 forms, not regressions.)

### Fix #16 — no regression
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5): 0 in
  the whole built tree excl. node_modules (this audit's scope-wide grep, not
  just verify17's subset). ("claude" strings in `fix17/build1.log` are the
  fix16 scrub's own log lines describing removals, not built-tree content.)
- Model pins untouched: `model: cursor-grok-4.6-high-fast` 71×,
  `model: grok-4.7-high` 4×; zero bare `grok-4.6-high-fast`; zero bracket
  syntax on slugs (`grok-4.7-high[`, `cursor-grok-4.6-high-fast[` — 0 hits);
  `reasoning_effort` 2×, no bare `effort:` model param. Remaining
  `model:` lines are benign non-pins (Vue `v-model`, the agent-TEMPLATE
  `CHANGE-ME` placeholder instructing a Grok pin, `hooks/adapter.js`
  `model: cursorInput.model` runtime passthrough — adjudicated live infra,
  `envelope.js` schema type, pi.js comment — the adjudicated dead code).
- Counts unchanged at the fix16 final state (fix16/MANIFEST.md: skills 166,
  agents 72, rules 123, commands 87, hooks 15).

### Standing rules — all intact
- "more, not bolder" present (7 files); craft-floor bans absolute
  (kicker/eyebrow ban `impeccable-craft-floor.md:36`, "no brief earns it back";
  gradient-text governed via Taste `:246` guarded exception + polish
  detector; Taste `:246` restates "its bans are absolute as
  static/code-level checks"); Hallmark floor binds (5 files); no violet
  introduced (fix17.py contains "violet" exactly once — the E1 ban, bound 7;
  the only other "violet" in fix17-touched files is the pre-existing
  less-flat-ui `:104` purple/violet-gradient ban); anti-derivative (6 files);
  snapshot-before-redesign + 2-round fresh-verdict budget (`fresh-verdict
  rounds used: N/2`, shared across 5b and Verify step 6) intact in
  orchestrate `:62` and orch-build-mvp `:53`.
- No adjudicated item re-flagged and none mentioned in any fix17 addition
  (`--domain` plain search, hooks/adapter.js, byte-identical assets,
  agent-emit-pi.js dead code — 0 hits in fix17.py additions).
- fix11/fix11-stage.py NOT re-run: `impeccable-critique.md` still carries the
  fix #12 edits — the fix #12 scoped §7 carve-out is present with the
  literal line `Questions skipped: first build — proceeding on stated
  assumptions (hackathon-mode §7)` (carve-out paragraph + Final-question
  gate + Recommended Actions from stated assumptions).
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
  intact) and names exception B as "the theme's decision, not this rule's";
  the mife default set (`:108`) and STATIC_CHECKS both repeat the same
  qualifier ("landing pages keep the Taste scroll ban except where a theme
  file records a scoped exception").
- U1_APP's per-surface floor (≥1, ui-ux-pro-max `:95`) vs U1's per-build
  floor (≥3): no contradiction — the sentence defers explicitly ("The full
  U1 rule (at least three per build, four-part uniqueness test) lives in
  `design-taste-frontend` step 4a"), and its "surface with none records
  `none — <reason>`" follows the package's record-the-exemption pattern
  (same as R3 and M5).

## Not checked
- The Campus Eats artifact itself (out of scope; must not be touched) — the
  re-trace target (59–63, final 61 literal) is not re-derived here.
- Live behaviour (no browser run in this audit): whether the built rules
  fire in a cold-start rebuild, and the parent-guidance open item on R1
  iris-opens + R4 hero loop compliance in the artifact, are for the re-trace
  / dry-run, not this tree audit.
- `build.sh.before-fix17` backup exists (confirmed present).
