# Fix #35 — Dry-run #55 (text-level routing trace)

**Method:** a sample brief is walked through the BUILT texts hop by
hop, citing the exact built wording that carries each hop. This is a
paper dry run over the shipped files — it proves the woven instructions
compose and no hop dead-ends. It is NOT a live Cursor run (live use is
OWED-35-2, the fix #30 live-test pattern).

**Sample brief:** "Landing page for a coffee subscription; the checkout
moment should print a paper receipt."

## Trace

1. **Scope → research.** Orchestrate's routing flow line (built):
   "scope → `prebuild-research` (step 1.5) → `feature-expansion`
   Phases 0–3 (automatic, right after the research step — …)". The
   research step is in the flow, not an orphan. ✓
2. **Design package routing.** Step 3's DESIGNPKG-AUTO names the
   package with the canonical parenthetical — kitchen is a named
   package skill ("…motionsites-web-builder / kitchen /
   motion-principles / threeui…"), and the gloss routes the brief:
   "`kitchen` — dqnamo's Kitchen, 15 copy-paste tactile components,
   ISC, copied from the page per project, never embedded
   (fix #35, KITCHEN_F35)." The receipt-printing checkout is the
   gloss's own example class ("a receipt-printing checkout" is the
   kitchen skill's description trigger). ✓
3. **Palette first.** Taste's palette paragraph lists the package with
   kitchen last and closes with the citation rule: every source USED
   or CONSIDERED-AND-REJECTED with a D19 reason; the Kitchen-specific
   guard follows immediately — a Kitchen piece whose motion breaks
   house rule 5 (no tilt, no carousel, no timed tabs) is recorded
   CONSIDERED-AND-REJECTED or re-implemented without the banned
   motion. The Receipt Printer piece (print animation, no banned
   motion) survives the guard. ✓
4. **Inventory.** The §0 layer map's Tactile row routes to §12; the
   §12 Kitchen row caps the piece ("one memorable physical-metaphor
   interaction per surface, at most"), names the entry point
   (`skills/kitchen/SKILL.md`, live page, ISC terms), and the skill
   itself repeats the cap and the copy-from-page rule. No hop sends
   the reader to a file that does not exist: `skills/kitchen/SKILL.md`
   is in the built tree. ✓
5. **Row-10 routing.** Orchestrate's step-3 dash form routes the
   surface: landing → Taste lead; the contract clause binds the slice
   ("every UI slice implements the design contract
   (`docs/design-contract.md`, DESIGNCONTRACT_F34) where one is
   issued"); the colon form's layer list names "`kitchen` (tactile,
   one piece per surface at most)". ✓
6. **Contract.** Taste step 4a issues the contract with the contract
   block now joined to the 4a paragraph (the A7/A8 move): the
   Components field takes "each named component + its inventory
   citation" — the Receipt Printer cites §12/Kitchen. ✓
7. **QA.** browser-qa's Motion verdict judges the print animation
   against the factory criteria (Doherty ≤400ms feedback, <300ms UI
   animation unless recorded as content, reduced-motion still); the
   mechanical evidence for the verdict may be gathered under the
   Scripted evidence collection paragraph (SCRIPT-FIRST_F34, one
   gated script, evidence never a verdict), and the report carries
   the Evidence line naming the script + gate record in the run
   ledger. ✓

## Findings

- No dead hops: every cross-reference the new text makes (kitchen
  skill, inventory §12/§13/§14/§15/§16, DESIGNCONTRACT_F34,
  SCRIPT-FIRST_F34, MOTION-QA_F34) resolves to a built file or
  section that exists with that number.
- One recorded placement exemption stands: orchestrate's step-2
  research-feed sentence is factory-only placement; the regular tree
  carries the same rule in feature-expansion (fix #34 port decision,
  unchanged by this fix).

**Verdict: PASS** — the parity weave composes end to end on paper.
Live behaviour in Cursor remains OWED-35-2.
