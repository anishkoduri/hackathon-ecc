# Audit #70 — Fix #23 (hackathon-ecc plugin) — CHECK-ONLY

**Verdict: AUDIT #70: NOT ZERO — 0 BLOCKING, 1 MINOR**

- 1 MINOR: DYNAMIC-BQA-01 (`skills/browser-qa/SKILL.md:56`) gives no disposition for an interaction the harness cannot drive — see Finding M1 below.
- 0 BLOCKING. No other finding. No regression in any prior verifier.
- verify23.py re-run by this audit: **210/211**, sole FAIL the owed manifest check (`fix23/MANIFEST.md` does not exist yet — expected, not a finding).

Method: read-only. No plugin file edited, no build.sh run, no fix/apply/verify script edited, no bundle/commit/push, no message sent. Every number below was re-derived by this audit with its own greps/reads (not copied from verifier output or any earlier report). verify23.py and the seven prior verifiers were re-run by this audit.

## Build state (verified, not trusted)

- `build.sh`: 24,030 lines, md5 `9af8562b6b4a342525f529a00a79e9ea` — matches the stated state.
- `diff build.sh.before-fix23 build.sh`: **+256 / −0** (additions only).
- Counts: **166 skills / 72 agents / 123 rules / 87 commands / 15 hooks**; trigger keys **64** (withTriggers == len(triggers) == 64, every key resolves to a real skill dir).
- Fix #23 `build.sh` blocks, in order: W1 §2 at 23765, §3 at 23821, W3 §4/§5 at 23855, §6 at 23894, §9 at 23931, CORE at 23975, `# STEP 5 — Counts` at 24021. §9 block < CORE block < STEP 5, as required (MEMORABLE-BQA-02 anchors on the Dynamic row DYNAMIC-BQA-02 inserts).
- `fix23/MANIFEST.md`: does not exist yet (owed to the manifest worker).

## 1. §1–§6 + §9 + CORE weave — all placements verified in full context

Token census re-derived by this audit (line counts / occurrences, excl. `node_modules`) — every count matches the disposition exactly:

| Token | Lines / occ | Files |
|---|---|---|
| INVENTORY_F23 | 4 / 4 | orchestrate SKILL.md, dispatch-prompt.md, design-inventory.md |
| AMBITION_F23 | 6 / 7 | orchestrate :68, :149 |
| MOTION_F23 | 9 / 10 | orchestrate :72, motion-foundations :205, motion-patterns :47, motion-advanced :49, make-interfaces-feel-better :109, ui-ux-pro-max :607 |
| TYPEAUDIT_F23 | 14 / 18 | typeset lens :61, slop-checklist :670, polish-pass SKILL.md :22/:101, browser-qa :78, orch-build-mvp :78, orchestrate :127, ui-ux-pro-max :270 |
| TRIO_F23 | 1 / 1 | orchestrate :127 |
| F7VAR_F23 | 2 / 2 | ui-ux-pro-max :270, slop-checklist :747 |
| HERO_F23 | 8 / 9 | Taste :55, :254, :507, :552; orchestrate :81; review-hero.md :3, :13 |
| FUNC_F23 | 8 / 9 | Taste :411, :507, :552; orchestrate :81 |
| FUNC-DIAG_F23 | 4 / 4 | diagrams.md :12 + pointers |
| HERO-BQA_F23 | 3 / 3 | browser-qa :80 + pointers |
| FUNC-BQA_F23 | 2 / 2 | browser-qa :71 + Taste :507 |
| FUNC-UIPRO_F23 | 1 / 1 | ui-ux-pro-max :49 |
| ALIGN_F23 | 15 / 16 | browser-qa :60, :118; polish-pass SKILL.md :98; alignment.md |
| COVER_F23 | 4 / 4 | browser-qa :64, :68; orchestrate :91; alignment.md :113 |
| BLOCK_F23 | 5 / 5 | browser-qa :125, :134; orchestrate :91; alignment.md :132 |
| DYNAMIC_F23 | 8 / 9 | motion-foundations :243, motion-patterns :124, motion-advanced :94, orchestrate :83, polish-pass :101 (×2), browser-qa :56, :112 |
| MEMORABLE_F23 | 4 / 5 | orchestrate :70, polish-pass :101 (×2), browser-qa :82, :113 |

**17 files carry `_F23`** — the exact 17 named in the disposition. No others.

Spot checks read in full context (all pass):

- **§1 Ambition / inventory** (`skills/orchestrate/SKILL.md:66,68`, `references/design-inventory.md`): inventory READ BEFORE deciding; USED vs CONSIDERED-AND-REJECTED with specific D19 reasons; blanket "we considered everything" fails; small-slice use without specific reasons FAILS; design usable without the package FAILS; MORE elements/motion/decisions, "More, not bolder" stands; F6 PRIMARY gate at :68 and step-6 extension at :149 ("rule-correct but unambitious design fails"). Inventory has §§1–10 + "How the record uses this file" (:161) + currency rule (:17: "any future fix that adds design elements updates it in the same change"). Inventory counts re-derived against the actual files: styles 89 csv rows, palettes 192, pairings 74, guidelines 120, icons 105, GSAP 17, charts 25, stacks 22; Taste moments 18 (kinds 4/4/1/7/2, 5 retired), palettes 64, type 39; Hallmark 50 themes in index.json + 50 theme .md files; Impeccable 62 rules; less-flat-ui 23 treatments; Vercel 16 groups / 104 rules; glossary G1–G20; Bang 10 style directions + 19 opener concepts; Thinking Orb 9 states, no "thinking" state. All match.
- **CORE** (orchestrate :70, browser-qa :82, :113, polish-pass :101): "Memorable is the bar — above F6… impressive is the floor, memorable is the bar"; "a build the user would forget the next day FAILS, however rule-correct"; "Browser-qa judges memorability as the TOP criterion"; over-the-top = ambition/impact not loudness, "do not just crank weight, color, or size"; "a build can be over the top and quiet in palette; it cannot be forgettable"; verdict is browser-qa's alone. Cross-references AMBITION/MOTION/HERO/FUNC/DYNAMIC without restating. See §6 below for the governing-bar confirmation.
- **§2 Motion**: motion default in all five sites, each carrying "feels static fails", token routing (stagger 30ms, press 0.97, dropdowns 150–250ms), D19 reason + token values, complete reduced-motion fallback; Taste scroll-ban scope guard present in motion-foundations :205.
- **§3 Fonts**: type-audit home in `reference/lenses/typeset.md:61` — visual share = Σ(size × visible characters) per face ÷ total, per screen + build roll-up; **T1a body ≤40% build share, T1b ≤55% per primary screen, T1c display/important ≥25%, T1d display > body on hero/home, T2 trio identical to previous build's FAILS without a recorded reuse reason, T3 variety floor max(3, ceil(N/20)), each counted face ≥5%**. Clearance: T1a/T1b only by scoped exception (D19 reason + theme-fit), T1c still binding; T1c/T1d/T3 have no clearance; a hit with no clearance is a FAIL. Slop-checklist type-audit section at :670 carries T1a–T3 + clearance; F7VAR_F23 at ui-ux-pro-max :270 (variety across the build, trio is a pattern not a default); orch-build-mvp :78 static record checks; orchestrate :127 (Type list feeds the audit, trio re-dealt per build). F4 stands unchanged (Fraunces long body + small incidental text only).
- **§4 Hero**: Taste :55 (dealt amazing moment, highest-weight surface, merely adequate fails F6, home/feed IS the hero surface, calibrated to the product's job, never a generic hero section, never louder); Picks Hero-moment row (:254); review-hero.md :3, :13 (judges the hero against the dealt moment); checklist first-screen (:552); step-6 static checks (:507); orchestrate :81 (brief without a hero moment is not ready); browser-qa hero verdict :80 (HERO-BQA_F23, browser-qa's alone).
- **§5 Functionality**: Taste :411 (mechanism visible early on hero or first screen after it, theme-matched, THIS build's pipeline/data/stack with own names and real figures, hides-what-it-does fails, never a generic "add a diagram"); diagrams.md :12 (FUNC-DIAG_F23); browser-qa :71 (FUNC-BQA_F23); ui-ux-pro-max :49 pointer (FUNC-UIPRO_F23, full rule lives in Taste); orchestrate :81 (brief without a functionality story is not ready). F2 stack labels unchanged — F2_RULE still verbatim in Taste (verified by import from fix19).
- **§6 Alignment**: `reference/alignment.md` read in full — all 8 assertions (OVERFLOW / CENTER / NAV / GRID / CLIP / LABELS / ACTIONS / PANELS) with tolerances 0px overflow / ≤2px centering-grid-spacing, `getBoundingClientRect()` measurement model, mid-band hero-GROUP rule (the −209px phone-alone vs 46px/46px group case correctly handled, naive frame-only check would false-fail), declared-intentional-bleed escape (`.iris-disc`, page overflow still 0), stagger escape for panel tops (26px at 1440). Coverage matrix: widths 1440 / 900 (band 768–1100, breakpoint ±1 probe + mid full-page shot) / 390; EVERY flow state (error/wrong-code, empty, success/delivered, accepted, scrolled) measured + screenshotted at all three widths. BLOCK_F23: unverified width/state = NOT shippable, DO NOT SHIP, empty cell never SHIP / SHIP WITH FIXES / INCONCLUSIVE-as-pass (browser-qa :125, :134; orchestrate :91; alignment.md :132).
- **§9 Dynamic**: motion-foundations :243 (state changes choreographed, no-motion gap), motion-patterns :124 (interactive depth — sortable/filterable/expandable/draggable, live state, immediate response), motion-advanced :94 (live and interactive pieces), orchestrate :83 (dynamic story per surface: WHAT changes / WHAT triggers it / HOW it moves; §9-vs-§2-vs-§5 distinction stated), browser-qa :56 live check + FAIL (DYNAMIC-BQA-01) and :112 report row (DYNAMIC-BQA-02), polish-pass :101 (reads the story, checks wiring/handlers/tokens statically; live response is browser-qa's alone). Reduced-motion fallback complete in each §9 sub. **Except Finding M1 below.**
- **D19_RULE NOT rewritten**: imported `D19_RULE` from `fix19/fix19.py` and confirmed byte-present in both orchestrate and Taste. The fix #22 seventh-dimension extension line is intact in both. verify19's own verbatim assertion passes within its 71/76 run (see §3).

## 2. /demo gates — read in full, all intact

- **(a) Callable**: `commands/demo.md` exists and is wired — loads `pitch-deck-video`, films the LOCAL app from the project dir only, never a deployed URL (`shots.json` `app.url` never the deployed URL); `/demo`, `/demo <path>`, `--rebuild/--script/--render/--montage/--explainer` all defined; narration-key prompt fires at the point the video is confirmed when the user invoked /demo directly.
- **(b) Never automatic — 0 auto-invocations**: read in full context — orchestrate SKILL.md (step 0, step 5 DEMOGATE_O4_F22 :95, step 6 DEMOGATE_O9_F22 :97, "Order: verify → polish → deploy → commit → README → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this order)"), orch-build-mvp (:32 narration-key prompt, :85 DEMOGATE_B2S1_F22 "/demo is not filmed here… Do NOT film via /demo here"), orch-change-feature (:51 DEMOGATE_B3S1_F22 re-film only "If the user asks for a re-film", "never by an automatic re-film"; B3S2–B3S7 present), `rules/hackathon-mode.mdc` §1 (DEMOGATE_H2_F22, "/demo is never part of this sequence"), §3 (audit deferral — no /demo path), §7 (DEMOGATE_H1_F22, "The first build does NOT film `/demo` automatically… never as a pipeline step, never by default"), `dispatch-prompt.md` Environment field ("only when the user asked for a demo video"). **Zero "demo" / "auto-invok" / "automatically" mentions inside the fix #23 `build.sh` blocks (lines 23765–24020)** — re-derived by this audit. No fix23 block reintroduced an auto-invocation. Narration-key prompt fires ONLY when the user asked for a demo video in all three sites (orchestrate step 0, orch-build-mvp :32, hackathon-mode §7).
- **(c) Contract intact**: pitch-deck-video carries **0 `_F23` tokens** (untouched by fix #23); the +256/−0 diff proves nothing existing was altered. Spot-checked in place: $10 cap present (`:805` "Default cap: $10 per video", `:815`), F1–F6 design-decision pointers present, voice rules present (narration/voice preflight, "The voice is the single biggest quality difference"), Bang Motion port §12 present (`:211`, GSAP 3.15.1 pinned), 2:10 cap present, local-only filming present. DEMOGATE tokens present at every site: O4/O9, B2S1 (+B2S2–B2S6), B3S1–B3S7, H1/H2.

## 3. Verifiers re-run by this audit

- **verify23.py: 210/211.** Sole FAIL: `fix23/MANIFEST.md exists and records build.sh lines + md5 (OWED — fails until the manifest worker writes it)`. Excluding it, 210/210.
- Prior verifiers (tails re-derived by this audit, FAIL lines listed and checked individually):
  - fix15 **42/44** — FAILs only: less-flat-ui 4-hunk diff pattern; frozen post-fix21 fingerprint.
  - fix17 **58/60** — FAILs only: same two.
  - fix18 **69/72** — FAILs only: frozen post-fix21 fingerprint + cascades (fix15/fix17 "still passes" lines).
  - fix19 **71/76** — FAILs only: less-flat-ui pattern, frozen fingerprint, cascades.
  - fix20 **164/169** — FAILs only: frozen fingerprint + cascades.
  - fix21 **96/102** — FAILs only: frozen fingerprint (23647-line form) + cascades.
  - fix22 **368/369** — sole FAIL: frozen post-fix22 fingerprint (23,774 lines, md5 `4799a819…`), superseded by fix #23.
  - **No fail outside the expected pattern. No real regression.**

## 4. Banned terms / Grok pins

- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5, case-insensitive, excl. node_modules): **0** in the built tree.
- Bare `grok-4.6-high-fast`: **0**. `grok-4.7-high` in 26 files, `cursor-grok-4.6-high-fast` in 85 files — matches the disposition.

## 5. Open items — stated explicitly

- **(a) styles.csv 89 vs skill header 80**: confirmed as recorded, not silently resolved. `data/styles.csv` has 89 rows; the ui-ux-pro-max header says "80 searchable styles (51 active)" (SKILL.md :3, :8). The inventory (:29) records both numbers and treats the csv as the source ("the csv is the inventory source"). Carried open as documented; no audit action.
- **(b) B3/B15/B4 token conflicts carried as flags**: confirmed. Inventory :104 records them verbatim as flags, never silently resolved: "B3 30ms vs Rule 5 floor 0.05s; B15 0.8x vs quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95". Carried open for parent adjudication.
- **(c) DYNAMIC-BQA-01 undrivable-interaction disposition**: **FINDING M1 (MINOR)** — see below. Verdict: the text needs the sentence.
- **(d) disposition-s9.md position-note inaccuracy**: confirmed as recorded. The s9 note said the orchestrate insertion sits "immediately BEFORE `**Two-pass briefing…**`"; in the built tree Two-pass is at orchestrate :79, **before** the HERO/FUNC paragraph (:81), and the DYNAMIC paragraph is at :83. The merged disposition records this inaccuracy and confirms the actual anchor (the HERO/FUNC paragraph's closing D19 line, count==1) was unambiguous and the insertion landed as specified. No further action; the record is correct.
- **(e) daisyUI 65 → 68 correction**: confirmed. The built inventory says "68 components" **twice** (:133 design-system row, :146 library (11) daisyUI pin) and "65" **zero times** in the whole inventory file. `skills/design-system/SKILL.md:40` says 68; fix22/MANIFEST.md agrees (re-checked by verify23). The §17 research count of 65 is corrected.

## Finding M1 (MINOR) — DYNAMIC-BQA-01 has no disposition for an interaction the harness cannot drive

**Evidence** — `skills/browser-qa/SKILL.md:56` (full text): "Dynamic-interface live check (fix #23 §9, DYNAMIC_F23): interact with the app like a user — click/press/hover every interactive control, and sort, filter, expand, and drag where the job calls for it — and confirm the interface responds immediately… A control that does not respond, or a state that changes without motion, FAILS the build."

- The check instructs driving sort/filter/expand/drag "where the job calls for it" with **no harness-capability qualifier** and **no disposition** for an interaction the harness cannot drive. Grep confirms: no occurrence of "unverified", "cannot drive", "undrivable", or "harness cannot" anywhere near any DYNAMIC_F23 placement (motion-foundations :243, motion-patterns :124, motion-advanced :94, orchestrate :83, polish-pass :101, browser-qa :56/:112). The only "unverified" occurrences in browser-qa are the §6 coverage ones (:69, :134).
- The asymmetry is inside the same file: the §6 alignment assertions explicitly say "run these programmatic assertions wherever the harness allows" (browser-qa :60) and BLOCK_F23 converts any unverified width/state into DO NOT SHIP. DYNAMIC-BQA-01 has no equivalent qualifier or conversion, and its Output Format row is binary `[✓/✗]` with no unverified state. A literal executor whose harness cannot drive drag has no instruction — silently skipping it yields a vacuous ✓, contradicting the skill's own "no baseline ⇒ report INCONCLUSIVE, never a silent PASS" principle (Phase 3 step 2).
- Why MINOR, not BLOCKING: SPEC §9 does not require the sentence, and all SPEC §9 requirements (live check, FAIL conditions, report row, decision-record story) are met. In practice the skill's never-silent-pass principles make a silent pass unlikely — but the disposition is genuinely unspecified where its sibling section specifies it, and the worker who wrote the text flagged it themselves.

**Fix (one sentence, in the DYNAMIC-BQA-01 paragraph at browser-qa :56):** "If the harness cannot drive an interaction the dynamic story names, record that interaction as unverified — a gap, never a silent pass; the Dynamic row is not ✓ on an interaction that was never driven." (Wording is the audit's suggestion; the parent may word it differently. Adding it requires a rebuild + verify23 re-run; it does not change any count, token, or gate.)

## 6. Behavior-change record — memorability above F6 as the governing bar

Confirmed supported everywhere it is claimed:

- **Orchestrate :70**: "Memorable is the bar — above F6… impressive is the floor, memorable is the bar. Browser-qa judges memorability as the TOP criterion at the finish review" and "it governs the ambition bar above (AMBITION_F23)".
- **Browser-qa :82**: "Memorability verdict — memorable is the bar, above F6… browser-qa judges memorability as the TOP criterion, above the F6 impressive bar… A build the user would forget the next day FAILS, however rule-correct".
- **Polish-pass :101**: memorability candidates are candidate evidence; "whether the build is actually memorable is `browser-qa`'s finish-review verdict alone (MEMORABLE_F23)"; quiet-palette builds with a strong moment are not flagged for being quiet.
- The F6-primary-gate extension (orchestrate :149) and the ambition bar (:68) are cross-referenced by the CORE paragraph, not rewritten by it — consistent with "impressive is the floor, memorable is the bar". The close report may state memorability above F6 as the governing bar.

## Owed / not findings

- `fix23/MANIFEST.md` — owed to the manifest worker (verify23's sole FAIL). Finding M1 may be fixed first (one sentence + rebuild) or carried open in the manifest as a parent adjudication; the audit does not silently resolve it either way.
- Open items (a), (b), (d), (e) above are carried as documented, not resolved.
