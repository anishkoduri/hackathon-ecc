# fix35 patch log

## Decisions

- DECISION-35-1 (D35-1, role decisions): where the two trees' role decisions conflicted, the REGULAR tree's decisions win (ui-ux-pro-max stays lookup-only; Taste leads); where content was richer in the factory (the inventory catalog, browser-qa wording), the factory's content wins. Pins and drone machinery are untouched in both trees.
- DECISION-35-2 (D35-2, numbering): the factory's inventory section numbering wins — MotionSites takes §13 and the fix #34 sections renumber to §14/§15/§16; the §14/§15 headers carry the factory's literal 'Factory round N' forms (capital F is outside the parity normalization, so the literal form is what parity requires).
- DECISION-35-3 (D35-3, browser-qa): the factory's stricter MOTION-QA / CONTRACT-QA wording wins; provenance is re-cited '(fix #35, ...)' in the regular tree (the _F34 ID stems are unchanged).
- DECISION-35-4 (D35-4, IDs): the only new rule ID is KITCHEN_F35; ported IDs keep their _F34 forms; the ported decision cites in the inventory use the stem DECISION-F-35 (see D35-10 for why the hyphenated F form is required).
- DECISION-35-5 (D35-5, build-time inventory): ALL inventory edits run at build time in fix35.py, because fix34.py asserts the old §13/§14/§15 inventory headers earlier in the same build; the staged inventory keeps the fix #34 state.
- DECISION-35-6 (D35-6, canonical parenthetical — Anish's decision B): the canonical DESIGNPKG-AUTO parenthetical is '(design-taste-frontend / ui-ux-pro-max / less-flat-ui / polish-pass / motion-foundations / motion-patterns / motion-advanced / make-interfaces-feel-better / design-system / motionsites-web-builder / kitchen / motion-principles / threeui / getlayers / gsap / react-bits / hairline-create / hairline-adopt, with the design-lead deciding which leads)'; fix32.py is NOT edited (its lead scan passes on this geometry). The Taste palette-first list keeps kitchen LAST per the SPEC (it scans clean).
- DECISION-35-7 (D35-7, A9 placement): fix #34 placed Taste's motion bullet after a blank line where the factory carries it directly under the depth D19 line; weave35 A9 (apply-a9.py) moves the blank line to after the bullet — a placement-only correction inside the parity file.
- DECISION-35-8 (D35-8, exclusion allowlist): verify35's factory-exclusion census (and fix35.py's post-assertion) carries a needle-pinned allowlist for exactly two lines in skills/orchestrate/references/design-inventory.md — the §15 Home line's factory-routing clause and the §16 bullet's factory-variant clause — the only 'orchestrator-briefing' occurrences fix #35 intentionally introduces (they are what makes those lines drop under the parity normalization, as the factory's own lines do). Any other occurrence is a defect.
- DECISION-35-10 (D35-10, defect found at build run 2): the inventory's ported decision cites were first written DECISION-D35, which the factory's DECISION-F-192 normalization renders 'DECISION-X' — but the factory's own DECISION-F-170 renders 'DECISION-X#', because the F-\d+ substitution runs BEFORE the DECISION rule and eats the hyphenated number first. Parity therefore requires the hyphenated form on the regular side too: the cites are DECISION-F-35 (and DECISION-F-35/F-35 in §14). The pre-fix35 census normalizer also differed from the factory's in two smaller ways (case-insensitive drop test; per-line substitution); fix35.py and verify35.py now embed the factory's _norm byte-for-byte.
- DECISION-35-9 (D35-9, defect found at build run 1): fix34.py's pre-state census asserts exactly 76 built skills, but kitchen is a staged skill and flows through the STEP 2 loop before fix34.py runs, so the built tree already carries 77 at that census and the build stopped there. Amended fix34.py's census 76 -> 77 (with an in-file D35-9 comment and its census CHANGES line updated); no other fix34 assertion changed — its README/coverage pre- and post-states are unaffected because fix35.py runs after it. Same pattern as fix #33 amending fix24.py's stale anchor. fix32.py is NOT edited (per the task).
- APPROVAL (recorded): Anish approved in plain words on Fri Nov 20, 2026, 21:02 CT: 'go ahead and run the build machinery' — build.sh, its fix scripts, hooks-bearing content, the verifier, and git operations in the scratch-repo, in both plugin trees. This fix ran under that approval. No push to GitHub and no upload was made or is authorized by it.

## Changes

- census: counts skills 77 (76 + kitchen), agents 45, rules 48, commands 55
- census: MODELSEL pin census holds at the fix #33 post-state
- census: README at 76 in all 4 count lines; trigger coverage 76/48
- census: staged weave landed (21 needles across 8 built files)
- census: inventory at the fix #34 state (§13/§14/§15 headers) — fix35 edits start here
- census: browser-qa at the fix #34 state (both verdicts present once, no scripted-evidence paragraph)
- inventory preamble (factory wording): skills/orchestrate/references/design-inventory.md
- inventory §0 layer map inserted: skills/orchestrate/references/design-inventory.md
- inventory Type row Fraunces role rule: skills/orchestrate/references/design-inventory.md
- inventory §10 cross-note (factory wording): skills/orchestrate/references/design-inventory.md
- inventory §12 home para gains kitchen: skills/orchestrate/references/design-inventory.md
- inventory §12 GetLayers weight sentence (factory wording): skills/orchestrate/references/design-inventory.md
- inventory §12 GetLayers row layer role: skills/orchestrate/references/design-inventory.md
- inventory §12 GSAP row layer role: skills/orchestrate/references/design-inventory.md
- inventory §12 React Bits row layer role: skills/orchestrate/references/design-inventory.md
- inventory §12 Hairline row layer role: skills/orchestrate/references/design-inventory.md
- inventory §12 Hairline row tail (factory wording): skills/orchestrate/references/design-inventory.md
- inventory §12 Kitchen row inserted: skills/orchestrate/references/design-inventory.md
- inventory §13 MotionSites inserted; §14 header takes the factory's literal form: skills/orchestrate/references/design-inventory.md
- inventory §14 intro provenance: skills/orchestrate/references/design-inventory.md
- inventory §14 trigger-key sentence gains Kitchen: skills/orchestrate/references/design-inventory.md
- inventory §15 header takes the factory's literal form: skills/orchestrate/references/design-inventory.md
- inventory §15 Home line: factory-routing clause appended (D35-8 allowlist line 1): skills/orchestrate/references/design-inventory.md
- inventory §15 contract row: factory's 'before dispatch': skills/orchestrate/references/design-inventory.md
- inventory §16 header: skills/orchestrate/references/design-inventory.md
- inventory §16 intro (factory history adopted verbatim, F-193; DECISION-F-35): skills/orchestrate/references/design-inventory.md
- inventory §16 bullet tail (D35-8 allowlist line 2): skills/orchestrate/references/design-inventory.md
- browser-qa MOTION-QA paragraph (factory wording): skills/browser-qa/SKILL.md
- browser-qa CONTRACT-QA paragraph (factory wording): skills/browser-qa/SKILL.md
- browser-qa scripted-evidence paragraph: skills/browser-qa/SKILL.md
- browser-qa Evidence report line: skills/browser-qa/SKILL.md
- README count line 1: README.md
- README count line 2: README.md
- README count line 3: README.md
- README count line 4: README.md
- README: fix #35 provenance note added before the fix #34 note
- trigger coverage.skills 76 -> 77: manifests/context-packs/skill-triggers@1.json
- parity: manifests/design-parity.json written; all 8 normalized hashes equal the factory's published values
- parity: design-parity.json sha256 = 55ddcc27f916ac6edaa74a48771c37268847fa526dd1802292b3b2c7d49c4372
- post: README 77 in all 4 lines; coverage 77/48; browser-qa carries both factory verdicts + scripted evidence + Evidence line
- post: inventory carries §0 + §13 + the factory-literal §14/§15 headers + §16; old headers gone
- post: no excluded machinery (briefing/drones/cm_dispatch/factory IDs) anywhere in the built tree, except the two D35-8 allowlisted inventory lines
- post: deploy-fast Netlify pricing row byte-untouched
- post: DESIGNPKG-AUTO byte-identical in orchestrate + hackathon-mode, canonical decision-B parenthetical in both
- post: MODELSEL pin census unchanged by the fix #35 writes

## OWED

- OWED-35-1 (call map): the call map is generator-owned and NOT regenerated by the build — fix35.py does not assert it. The coordinator regenerates it after the build (fix28/callmap/generate_call_map.py, EXPECTED skills 76 -> 77 — the EXPECTED bump is part of weave35) and rebuilds so the staged copy flows into the built tree; verify35.py asserts the regenerated map (kitchen called; uncalled set unchanged).
- OWED-35-2 (live use): kitchen routing, the layer map, and the scripted-evidence discipline are file-level rules; whether Cursor runs them as written is decided by live project use (the fix #30 live-test pattern), not by this build.
- OWED-35-3 (factory side): the factory's round-14 amendment (decision B geometry + R-7 wording) is committed on the factory side at 4f82e38 and its bundle regenerated (hackathon-ecc-factory-round14.bundle, 91,200,859 bytes); the parity targets asserted here are the amended manifest values. Nothing in this fix pushes or uploads either tree.
