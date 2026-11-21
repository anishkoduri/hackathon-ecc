# Fix #35 — Audit #116 (independent item-by-item audit)

**Scope:** every deliverable in `fix35/SPEC.md` + `fix35/BLOCKER-canonical-vs-fix32-scan.md`,
checked against the verified built tree (build run 4, fakehome35) by direct
inspection, independent of verify35's own assertions. Factory reference state:
the committed round-14 + amendment tree (bundle clone `fix35/fac14-clone`,
HEAD 4f82e38) — not the live factory tree.

## Items

1. **Kitchen skill** — staged from the factory's committed source, pinned by
   raw sha256 `ff93f5280b95f2d8b35605ed5a9dd39f48b1f4c3b075e552e9e27bea0db36916`
   (staged == built in the factory). Sole adaptation: header cite
   "(factory round 14, KITCHEN_F32)" → "(fix #35, KITCHEN_F35)". Built copy
   carries no other factory cite; dir contains only SKILL.md (catalog + copy
   guide, no vendored source). **PASS**
2. **Canonical DESIGNPKG-AUTO (decision B, D35-6)** — the parenthetical in
   built orchestrate + hackathon-mode is character-identical to Anish's
   chosen string and to the amended factory's; the two blocks are
   byte-identical to each other (fix31/fix34 mirror assertions + fix35
   post-assertion). fix32.py untouched; its lead scan passes on this
   geometry (the build's fix32 step ran clean). **PASS**
3. **Taste parity edits** — palette list kitchen-last + the factory's two
   closing citation sentences; depth-bullet GSAP cite (§11; usage skill,
   inventory §12); Fraunces role rule in factory-raw cite forms
   ("(fix #19 F4)", "under fix #19 F3 / fix #20 F5"); 4a typography gloss;
   4a motion clause (GSAP engine + React Bits / Kitchen supply); contract
   move = exactly the two needle ops (join + split). One placement defect
   found by the staged normalized diff and fixed as weave A9 (D35-7):
   fix #34 had placed the motion bullet after a blank line where the
   factory carries it directly under the depth D19 line. **PASS**
4. **getlayers layer role** — the factory's bold "**Layer role:
   foundation**" sentence sits immediately before the Plugin-rules
   sentence in the Hackathon-ecc note. **PASS**
5. **Citation renumber** — built-tree census of `design-inventory.md`
   cites in skills: §12 ×3 (getlayers, gsap, kitchen layer roles),
   §14 ×2 (motion-principles, threeui), §15 ×1 (prebuild-research);
   no stale §13 cite in motion-principles/threeui. **PASS**
6. **Inventory parity rewrite (D35-5, build-time)** — all 17 differing
   regions reconciled (preamble, §0 layer map, Type-row Fraunces rule,
   §10 cross-note, §12 home para + GetLayers sentence + 4 row layer
   roles + Hairline tail + Kitchen row in the reversed cite form
   "(KITCHEN_F35, fix #35)", §13 MotionSites, §14/§15 literal
   "Factory round N" headers, §14 intro "(DECISION-F-35/F-35)",
   §15 Home-line factory-routing clause, contract-row "before
   dispatch", §16 header + verbatim factory-history intro + bullet
   tail). Normalized hash equals the factory's: 8360e40d…. **PASS**
7. **browser-qa** — MOTION-QA + CONTRACT-QA paragraphs are the factory
   texts with provenance re-cited "(fix #35, …)"; scripted-evidence
   paragraph inserted between the contract paragraph and the
   Design-decision pointer (single-newline join, as the factory);
   Evidence report line after the Contract row; report rows for
   Motion/Contract unchanged from fix #34. **PASS**
8. **Counts** — skills 77 (76 + kitchen), agents 45, rules 48, commands
   55, hooks 15, trigger keys 48; README at 77 in all 4 count lines +
   fix #35 note before the fix #34 note; coverage {77, 48}; kitchen
   carries no trigger key (fix #31 precedent). **PASS**
9. **Parity manifest** — `manifests/design-parity.json` generated at
   build time; all 8 normalized hashes equal the factory's published
   values; the file is byte-identical to the factory's manifest
   (sha256 55ddcc27f916ac6edaa74a48771c37268847fa526dd1802292b3b2c7d49c4372
   on both sides). **PASS**
10. **Untouched surfaces** — deploy-fast Netlify pricing row
    byte-identical (fix34 assertion re-run clean); MODELSEL pin census
    unchanged (cursor-grok-4.6-high-fast ×72, "Grok 4.7 High" ×2);
    fix32.py not edited; factory tree not written. **PASS**

## Defects found during the build (both fixed, both recorded)

- **D35-9 (build run 1):** fix34.py's census asserted exactly 76 built
  skills; kitchen flows through STEP 2 before fix34.py runs, so the
  tree already carried 77. fix34.py census amended 76 → 77 (in-file
  comment); no other fix34 assertion changed.
- **D35-10 (build run 2):** the inventory's ported decision cites were
  written DECISION-D35, which the factory's DECISION-F-192
  normalization renders "DECISION-X", while the factory's own
  DECISION-F-170 renders "DECISION-X#" (the F-\d+ rule runs before the
  DECISION rule). Cites corrected to DECISION-F-35 forms; fix35.py +
  verify35.py now embed the factory's `_norm` byte-for-byte (the
  earlier reconstruction also differed on drop-test case sensitivity).

**Verdict: PASS** — all SPEC items landed; verifier 626/626 (run 2,
post-regeneration build).
