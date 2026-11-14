# Audit #52 — hackathon-ecc Cursor plugin (fix round #14)

- **Built tree:** `~/workspace/hackathon-plugin/hackathon-ecc/`
- **build.sh:** 23,160 lines, md5 `6253677ce02c8625dadb41e1acf32e6b`
- **Built-tree manifest:** `39602dd2c80de00b60bb5852a68f1d69` (in both `fix14/manifest1.txt` and `fix14/manifest2.txt`; diff 0 — independently reproduced here by re-hashing the built tree, same digest)
- **Counts confirmed:** 169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB
- **Scope of this round:** one item only — `less-flat-ui` gained treatment #23, Soft Shadow, from the @lnunesdesigns reel. The standalone source `~/workspace/cursor-skills/less-flat-ui/SKILL.md` was edited (8 substitutions in `fix14/fix14.py`); the build.sh W2-C1 patch anchor changed "## The 22 treatments" to "## The 23 treatments" (2 lines).
- **Method:** READ-ONLY. No file in the plugin tree or `build.sh` was edited. Every finding below was verified by reading the built files directly. `fix14/verify14.py` was re-run by this auditor: **24/24 pass**.
- **Result: ZERO ERRORS — 0 blocking, 0 minor.**

## Blocking findings

None.

## Minor findings

None.

## (a) The fix14 change — verified in full, in the built tree

The staged skill was read end to end (`skills/less-flat-ui/SKILL.md`, 535 lines) and diffed against the standalone source; `build.sh` was diffed against `build.sh.before-fix14`.

### The 23 treatments — numbering and content

- **Treatment headings number 1–23 exactly, no gaps, no duplicates.** `grep -n "### [0-9]*\."` returns :104 (1. Felt texture), :120 (2. Fluted glass), :142 (3. Thermal gradients), :158 (4. Water ripples), :173 (5. Speckled graphite), :187 (6. Single-hue landscapes), :199 (7. Blueprint grids), :217 (8. Halftone), :231 (9. Grainy gradients), :243 (10. Grass texture), :258 (11. Dithered images), :276 (12. Paper texture), :292 (13. Contour lines), :307 (14. Cloud sky), :323 (15. Pixel mosaics), :337 (16. Lens distortion), :361 (17. Stippled gradients), :377 (18. Square-dot grids), :394 (19. Blurred photos), :415 (20. Iridescent shapes), :431 (21. Impressionist paintings), :449 (22. ASCII and pixels), :485 (23. Soft shadow).
- **:485 — `### 23. Soft shadow`.** :487 Best for line: "Best for: cards, buttons, modals, floating panels — any raised surface that needs depth without a pattern. The quietest treatment on this list: it adds dimension while leaving the surface itself untouched." CSS blocks: :490 `.soft-shadow {` (three-layer `box-shadow`: `0 1px 2px rgba(30, 30, 60, 0.06)`, `0 8px 16px -4px rgba(30, 30, 60, 0.10)`, `0 24px 48px -12px rgba(30, 30, 60, 0.18)`), :504 `.soft-shadow-sm {`, :514 `.soft-shadow-lg {`. :499 layering explanation ("Three layers, not one: a tight contact shadow grounds the element, a mid shadow lifts it, and a large soft shadow (24–48px blur, low opacity) sells the height"). :524 layering note: "Layers with everything: a shadow is a depth cue, not a pattern, so it stacks on top of any other treatment without competing. Never put two separate drop shadows on one element (the layered single `box-shadow` above is the treatment; a second one reads as a mistake)." The section ends cleanly at :526 `## Record what you applied` — the new treatment was appended after #22 (ASCII and pixels), whose closing line ("Characters cluster into a soft radial blob. Keep opacity low; ASCII is texture, not content, so it must never be readable as text or selectable.") is intact directly above :485.

### Every "22" count updated to "23"

- **:3 frontmatter** — "description: Make the UI more striking with 23 textured treatments (felt, fluted glass, thermal gradients, halftone, grainy gradients, blueprint grids, contour lines, pixel mosaics, iridescent shapes, ASCII/pixel art, and more)."
- **:8 source line** — "Source of the 23 treatments: Instagram reel by @charles.unemployed, "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)"; plus Instagram reel by @lnunesdesigns, "How to make your design feel less flat in under 10 seconds" — 9 of its 10 treatments were already covered (thermal gradients, blueprint grids, water ripples, speckled graphite, fluted glass, contour lines, grainy gradients, single-hue landscapes, grass texture); Soft Shadow is the new one from it. The reels frame them as backgrounds, but each one is a texture/pattern treatment that can go on any surface: page backgrounds, cards, buttons, dividers, headings, modals, nav."
- **:100 heading** — "## The 23 treatments".
- **Quoted reel title correctly preserved:** the only "22" left in the file is the reel's own title, "22 Backgrounds to Make Designs Less Flat (In under 30 seconds)", in the :8 source line. `grep "22 treatments\|22 textured"` on the staged file returns 0 hits.

### Soft Shadow wired into the picker and surface tables

- **:44 picker, Premium row** — "| Premium, soft, wellness, beauty | Paper texture, cloud sky, felt texture, grainy gradients, soft shadow |".
- **:61 surface table, cards** — "| Cards and panels | Felt, paper, fluted glass, grainy gradients, speckled graphite, soft shadow |".
- **:62 surface table, buttons** — "| Buttons and CTAs | Thermal gradients, iridescent shapes, grainy gradients, soft shadow |".
- **:65 surface table, modals** — "| Modals and overlays | Fluted glass, blurred photos, soft shadow |".
- **No duplicate treatments:** each of the other 9 @lnunesdesigns reel items appears exactly once as a `### N.` heading (Thermal gradients 1, Blueprint grids 1, Water ripples 1, Speckled graphite 1, Fluted glass 1, Contour lines 1, Grainy gradients 1, Single-hue landscapes 1, Grass texture 1) — verified by per-name `grep -c "^### [0-9]*\. <name>"`.

### The 3 runtime-patch additions survived the rebuild

- **Patch 1 (wow-moment rule), :32** — "- **Texture in service of the wow moment, not decoration:** apply treatments where they amplify the page's captivating moment; never texture for its own sake — if a treatment does not make the memorable moment stronger, leave that surface flat."
- **Patch 2 (design-tokens record line), :74** — the Shared-utilities intro line now ends "…Do not cram data-URI SVGs into Tailwind arbitrary values. Record every treatment applied, on which surface, in `docs/design-tokens.md` (or MASTER.md on a dashboard-only build) — later slices and polish-pass read the record from there, not from the CSS."
- **Patch 3 (re-tint warning), :101–102** — "Re-tint every example below to the project's dealt palette and tokens before using it — the hex values are placeholders, not the palette. Never copy a purple/violet gradient onto a landing page (Hallmark gate 2a and Taste §6 Never ban it); the craft floor's purple-blue-gradient ban applies the same way on app surfaces." — inserted directly under the `## The 23 treatments` heading, i.e. after the W2-C1 anchor rename, so the anchor still matches.

### Staged differs from standalone ONLY by those 3 patch hunks

`diff ~/workspace/cursor-skills/less-flat-ui/SKILL.md hackathon-ecc/skills/less-flat-ui/SKILL.md` returns exactly three hunks: `31a32` (wow-moment insert), `73c74` (record-line append, a one-line replace), `99a101,102` (re-tint insert). No other difference. The standalone source itself carries the fix (23 `### N.` headings, "Source of the 23 treatments" at its :8, "## The 23 treatments" at its :99), so the staged copy is a faithful build of the edited source plus the three known patches.

### build.sh change scope

`diff build.sh.before-fix14 build.sh` → exactly 2 changed lines, **0 additions, 0 deletions**: line 22069 and line 22072, both `"""## The 22 treatments` → `"""## The 23 treatments` — the old and new strings of the single W2-C1 patch tuple (`# W2-C1: example hexes are placeholders — re-tint to the dealt palette.`, anchor `## The 23 treatments\n\n### 1. Felt texture`). `grep "## The 22 treatments"` on build.sh returns 0; `grep -c "## The 23 treatments"` returns 2. The fix14 source edit is consistent with this: `fix14.py` applied 8 substitutions to the standalone skill (frontmatter, source line, picker row, 3 surface rows, heading, new #23 section) and the 2-line anchor rename in build.sh.

### Consistency checks across the whole tree

- **No stale "22" count anywhere:** `grep -rn "22 treatments\|22 textured"` over the entire built tree returns 0 hits. No other file in the tree mentions a treatment count at all — `grep -rn "23 treatments\|23 textured"` outside `skills/less-flat-ui/` returns 0 hits, so no cross-file count reference was left un-updated.
- **Quoted reel title is the only "22" in the count's neighbourhood:** `grep -rn "22 Backgrounds"` in the built tree returns exactly 1 hit (the :8 source line). No other file quotes the reel title.
- **No other build.sh reference to the count:** `grep -n "22" build.sh | grep -i "treatment\|less-flat"` returns 0; the only `less-flat-ui` touch points in build.sh are the fresh copy at :258 (`cp -r "$HOME/workspace/cursor-skills/less-flat-ui" "$PLUGIN_DIR/skills/less-flat-ui"`) and the three patch blocks (Batch E wow-moment, W2-G9 record line, W2-C1 re-tint).
- **fix13j change intact:** the snapshot-manifest-in-appendix rule still reads in both engines (orchestrate :60, orch-build-mvp :53) — the fix14 round touched nothing else.
- **Build reproducibility:** both build logs end "build complete: /home/hatch/workspace/hackathon-plugin/hackathon-ecc"; the built-tree manifest is identical in `fix14/manifest1.txt` and `fix14/manifest2.txt` (`39602dd2c80de00b60bb5852a68f1d69`), and re-hashing the built tree here reproduces that same digest.

## (b) Standing #13 invariants — verified clean

- **Single build engine per run:** orchestrate :50 ("One build engine per run — orchestrate IS the first-build engine… orchestrate never invokes it"), orch-build-mvp :13 ("One build engine per run: this skill is the STANDALONE pipeline… One engine per run, never both"), and `rules/hackathon-mode.mdc` :12 ("One build engine per run: Orchestrate IS the first-build engine").
- **Cold-start direction chain:** orchestrate :10 ("Start of run — read the decision record first. Before planning or delegating anything, read `docs/decision-record.md`"); orch-build-mvp "When to Use" — runs "from the record/scope — `docs/decision-record.md` + `docs/scope.md` by default"; a doc path in `$ARGUMENTS` "is only the standalone fallback when neither record file exists — the record/scope is the default, never the doc path".
- **Grok 4.7 High pin + picker instruction:** `grok-4.7-high` in slug form in 10 files (orchestrate, orch-build-mvp, orch-add-feature, orch-change-feature, orch-fix-defect, orch-refine-code, `ecc-gan-planner`, `gan-build`/`gan-design` commands, README). Zero bracket-syntax hits (`grok-4.7-high[` → 0). Picker instruction present in orch-build-mvp :40 ("select Grok 4.7 High in Cursor's model picker before the first build, or the pin may silently fall back — file-level pin only, the live smoke test decides") and the same wording in orchestrate step 4 / row 10.
- **Anti-derivative rule:** orchestrate :92 ("No design based on a searched reference (anti-derivative rule). … No design may be based off a searched external reference — not a marketing website, not a Dribbble shot, not a template, not any found page… the direction is GENERATED through the package skills"); mirrored in orch-build-mvp :40 and the four orch-* skills.
- **"More, not bolder" posture:** orchestrate :90 ("Posture — more, not bolder. The package is applied fully, not conservatively: more design decisions made deliberately through the skills, more of the package applied, more craft… NOT necessarily bolder"); orch-build-mvp :40 ("Posture is more, not bolder").
- **Auto-approval / auto-expansion:** `rules/hackathon-mode.mdc` §7 (:56, :60–63) — first build runs fully autonomously after grill-me, "do not ask the user anything, do not wait for an approval, and do not stop for a decision"; "Every approval gate auto-approves"; "The ambiguity gate does not ask"; "Escalations do not wait"; the narration-key prompt is the one sanctioned prompt. §1 (:12) — expansion Phases 0–3 run pre-build automatically, Phases 4–6 inside the build, "built as part of the first build with no user approval gate".
- **Deferred-six §3/§7 carve-out:** `rules/hackathon-mode.mdc` :22 lists the six (`production-audit`, `delivery-gate`, `codehealth-mcp`, `verification-loop`, `santa-method`, `security-scan`), "never fire during the first build", with the single named end-of-project run as the only permitted invocation; :58 repeats the carve-out in §7. Both engines run the six by name before the final report (orchestrate :8 also names them, noting `security-review`/`security-reviewer` are NOT deferred).
- **Single-executor rule (browser-qa alone issues pass/fail verdicts on rendered screens):** orchestrate Verify step 5 ("`browser-qa` is the SOLE executor of this bar inside the visual loop") and Verify step 6 ("only `browser-qa`'s verdict decides whether a fix is owed"; Specificity under 3 and finish-review template observations are candidate evidence only); orch-build-mvp step 6 (same, plus `skills/gan-style-harness/SKILL.md` :118 "Screen distinctiveness is NOT scored here… judged ONLY by `browser-qa`"); `sloplint.mjs` :2961 comment confirms Gate 38iii is a static/code-level check, "not a pass/fail verdict on a rendered screen — that verdict is `browser-qa`'s alone". Gates 63 (template punctuation), 65 (the named look), 67 (tracked-caps label) in `gates.md` (:11, :68, :85, :219) are static text-pattern gates — code-level proxies, not screen verdicts. Static sloplint app-scope (`--scope app`) does not prove distinctiveness — stated in both engines.
- **SSML truth:** `skills/pitch-deck-video/SKILL.md` :335–352 and :539–541 (v2 family takes `<break>` up to 3s; `eleven_turbo_v2_5` deprecated; v3/v4 do NOT support breaks; Piper and `say` have no SSML) match `skills/pitch-deck-video/template/scripts/tts.mjs` :88–91 (same v2/v3/v4 and deprecation statements) and the voice-setting defaults in code (`tts.mjs` :103–106: stability 0.5, similarity_boost 0.75, style 0.0, speed 1.0).
- **Pins:** `puppeteer-core@25.17.0` pinned wherever the render tier is invoked (orchestrate Verify :195, orch-build-mvp step 6, design-taste-frontend :312; 7 occurrences tree-wide). Other `npm install` hits are version-pinned (e.g. tailwindcss@4.3.5, @modelcontextprotocol/sdk@1.32.2).
- **Revert mechanics (prior rounds):** whole-tree file-copy snapshot excluding `.hackathon/` (self-referential) and `.hallmark/candidate-evidence.md` (live run state); run state never restored by a revert (rounds-used line and Superseded markings survive); untracked-file deletion in revert (2); redesign-id uniqueness (`-2`, `-3`, …). Present and identical in both engines (orchestrate :60, orch-build-mvp :53).
- **Deploy-on-hold explicit:** both engines state the hold blocks only the redesign and the reverted verified tree is deployed/filmed/reported.

## Structural checks

- **Counts:** skills 169, agents 72, rules 123, commands 96, hooks 15 events in `hooks/hooks.json` (15 hook scripts + `hooks/adapter.js` = 16 `.js` files in `hooks/`; adapter is the live Cursor stdin adapter, not a hook event). 57 MB. No empty `SKILL.md` files.
- **Frontmatter:** all 169 skills have `SKILL.md` with `name:` matching the directory (0 mismatches). All 72 agents have frontmatter `name:` equal to the filename minus the `ecc-` prefix (0 mismatches; the `ecc-code-reviewer` → `code-reviewer` reversion is the intended qc_patch behaviour, not a defect).
- **Commands:** 71/96 command files carry only `description:` frontmatter — matches the adjudicated count, not a defect.
- **JSON validity:** `hooks/hooks.json`, `mcp.json`, `package.json` all parse.
- **`agent-emit-pi.js`:** `scripts/lib/agent-emit-pi.js` (134 lines, Pi emitter) is unreferenced by any other file in the tree (0 referencing files) — Pi-native dead code by design, not re-flagged.
- **montage / explainer:** `skills/pitch-deck-video/SKILL.md` :469, :479, :487 — OpenMontage modes are opt-in only.

## (c) Full-tree sweep for count-change fallout

- **Zero stale "22" count references** in the built tree, the standalone source, and build.sh (see §(a) consistency checks).
- **One comment checked and not flagged:** `build.sh` :20973–20974, inside the Batch E (fix #4) block, says "no build.sh patch touches skills/less-flat-ui/SKILL.md". Read in execution order it is accurate: Batch E's block sits at :20967, before the W2-G9 (:~22060) and W2-C1 (:22069) patch blocks, so when Batch E's substitution runs, no earlier patch has touched the file — the sentence describes its own anchor's precondition, not the final state of the file. The fix14 count change did not cause this wording, and the patch order makes it true where it matters. Not a finding.

## Not flagged (per audit brief)

- OpenMontage runtime-fetch unpinned clone (`pitch-deck-video/references/openmontage/runtime-fetch.md:13,21`) — documented opt-in, parent decision.
- Unpinned `pip install` lines in restored upstream skills — the separate pending pip pinning pass, out of scope for this audit.
- Adjudicated design items listed in the brief (explicit `--domain` plain search as reference rows only; byte-identical assets; `git checkout` explanatory text; dry-run observation that landing-redesign Gates apply; landing-page sloplint `--scope app` wording) — none re-flagged.

## Verdict

**ZERO ERRORS — 0 blocking, 0 minor.** The fix14 change is correctly and consistently applied end to end: Soft Shadow is treatment #23 in the staged skill with its full CSS block, Best-for line, layering note, picker and surface-table wiring; every "22" count reads "23" with the reel's own "22 Backgrounds" title correctly preserved; the three runtime-patch additions survived the rebuild and the staged file differs from the standalone source only by those three hunks; build.sh changed by exactly the 2-line W2-C1 anchor; all standing #13 invariants hold; and the full-tree sweep found no stale count reference. The audit loop closes when dry-run #24 and the sweep are also clean.
