# Sweep #31 RE-RUN — Fix #23 (hackathon-ecc) — CHECK-ONLY report

**SWEEP #31 RE-RUN: CLEAN — 0 blocking, 0 minor**

Scope: built tree `~/workspace/hackathon-plugin/hackathon-ecc/` (node_modules excluded
everywhere), `build.sh`, staged sources (`new-skills/`, `round2-skills/`), fix23 working
files. Check-only: no plugin file edited, no `build.sh` run, no fix/apply/verify script
edited or run except read-only runs of `fix23/verify23.py`, `fix22/verify22.py`,
`fix21/verify21.py`. No bundle, commit, push, or message sent.

This is a RE-RUN of Sweep #31 (which was CLEAN on the 24,030-line build). The only
change since is the Audit #70 M1 fix: one sentence added to the DYNAMIC-BQA-01
paragraph in browser-qa, via a new `build.sh` runtime-patch block (sub
DYNAMIC-BQA-01-M1), plus a rebuild. Every number below was re-derived by this
sweeper's own greps/commands listed in §8; nothing was copied from sweep #31,
Audit #70, or coordinator reports without re-running.

Read first, in full: `fix23/SPEC.md` (§0–§9), `fix23/PARENT-GUIDANCE.md`,
`fix23/disposition-merged.md`, `fix23/sweep31-report.md`, `fix23/verify23.py`.

## 1. Build fingerprint + diff

| Item | Re-derived value | Expected | Result |
|---|---|---|---|
| `build.sh` lines | 24,059 (`wc -l`) | 24,059 | PASS |
| `build.sh` md5 | `df2cb85055efc87637d3cb0b1e7061a2` | same | PASS |
| `build.sh.before-fix23` lines / md5 | 23,774 / `4799a819791b9c3ec4c19136ad698397` | same | PASS |
| `diff build.sh.before-fix23 build.sh` | **+285 / −0** (single hunk `23764a23765,24049`) | +285/−0 | PASS |

Eight fix23 blocks, all additions, in order, immediately before `# STEP 5 — Counts`
(`build.sh:24050`):

| Block | Lines | Size | Marker line |
|---|---|---|---|
| W1 — motion default (§2) | 23765–23820 | 56 | 23765 |
| §3 — type audit / fonts | 23821–23854 | 34 | 23821 |
| W3 — hero + functionality (§4/§5) | 23855–23893 | 39 | 23855 |
| §6 — alignment + centering | 23894–23930 | 37 | 23894 |
| §9 — dynamic interface | 23931–23974 | 44 | 23931 |
| CORE — memorability verdict (§1) | 23975–24020 | 46 | 23975 |
| **M1 — DYNAMIC-BQA-01 undrivable-interaction disposition (Audit #70)** | **24021–24049** | **29** | **24021** |

56+34+39+37+44+46+29 = 285. Block order verified: §9 marker (23931) < CORE marker
(23975) < M1 marker (24021) < STEP 5 (24050), as required (MEMORABLE-BQA-02 anchors
on the Dynamic row DYNAMIC-BQA-02 inserts; M1 anchors on the DYNAMIC-BQA-01 text
the §9 block inserts, so M1 must come after §9 — it does). The M1 block header
(lines 24021–24028) states the Audit #70 M1 rationale, the placement, and that the
added sentence carries no DYNAMIC_F23 token. The M1 sub tuple is at `build.sh:24034`.

## 2. Anchor table — every `_F23` token re-derived

`grep -rn` over `skills agents commands rules hooks` (excl. node_modules). Line counts
are lines carrying the token; occurrences are literal substring counts. **Every token
matches sweep #31 exactly — no line or occurrence count changed under the M1 rebuild.**
Multi-occurrence lines re-checked individually: `orchestrate/SKILL.md:149`
AMBITION_F23 ×2, `:72` MOTION_F23 ×2, `:127` TYPEAUDIT_F23 ×3,
`polish-pass/SKILL.md:101` DYNAMIC_F23 ×2 + MEMORABLE_F23 ×2.

| Token | Lines / Occ | Locations (file:line) |
|---|---|---|
| INVENTORY_F23 | 4 / 4 | orchestrate/SKILL.md:66; orchestrate/references/design-inventory.md:1, :17; orchestrate/references/dispatch-prompt.md:24 |
| AMBITION_F23 | 6 / 7 | orchestrate/SKILL.md:66, :68, :70, :149 (×2); design-inventory.md:8, :161 |
| MOTION_F23 | 9 / 10 | orchestrate/SKILL.md:70, :72 (×2), :83; motion-foundations/SKILL.md:205, :243; motion-patterns/SKILL.md:47; motion-advanced/SKILL.md:49; make-interfaces-feel-better/SKILL.md:109; ui-ux-pro-max/SKILL.md:607 |
| TYPEAUDIT_F23 | 14 / 18 | browser-qa/SKILL.md:78; orch-build-mvp/SKILL.md:78; orchestrate/SKILL.md:127 (×3); polish-pass/SKILL.md:22, :101; polish-pass/reference/lenses/typeset.md:61, :98; polish-pass/reference/slop-checklist.md:670, :672, :681, :743, :745, :748; ui-ux-pro-max/SKILL.md:270 |
| TRIO_F23 | 1 / 1 | orchestrate/SKILL.md:127 |
| F7VAR_F23 | 2 / 2 | ui-ux-pro-max/SKILL.md:270; slop-checklist.md:747 |
| HERO_F23 | 8 / 9 | design-taste-frontend/SKILL.md:55, :254, :507, :552; design-taste-frontend/references/hallmark/references/review-hero.md:3, :13; orchestrate/SKILL.md:70, :81 |
| FUNC_F23 | 8 / 9 | design-taste-frontend/SKILL.md:411, :507, :552; design-taste-frontend/references/diagrams.md:12; orchestrate/SKILL.md:70, :81, :83; ui-ux-pro-max/SKILL.md:49 |
| FUNC-DIAG_F23 | 4 / 4 | design-taste-frontend/SKILL.md:411; diagrams.md:12; orchestrate/SKILL.md:81; ui-ux-pro-max/SKILL.md:49 |
| HERO-BQA_F23 | 3 / 3 | browser-qa/SKILL.md:80, :82; design-taste-frontend/SKILL.md:507 |
| FUNC-BQA_F23 | 2 / 2 | browser-qa/SKILL.md:71; design-taste-frontend/SKILL.md:507 |
| FUNC-UIPRO_F23 | 1 / 1 | ui-ux-pro-max/SKILL.md:49 |
| ALIGN_F23 | 15 / 16 | browser-qa/SKILL.md:61, :118; polish-pass/SKILL.md:98; polish-pass/reference/alignment.md:1, :30, :38, :50, :57, :69, :71, :80, :93, :97, :100, :111 |
| COVER_F23 | 4 / 4 | browser-qa/SKILL.md:65, :69; orchestrate/SKILL.md:91; alignment.md:113 |
| BLOCK_F23 | 5 / 5 | browser-qa/SKILL.md:69, :125, :134; orchestrate/SKILL.md:91; alignment.md:132 |
| DYNAMIC_F23 | 8 / 9 | browser-qa/SKILL.md:56, :112; motion-advanced/SKILL.md:94; motion-foundations/SKILL.md:243; motion-patterns/SKILL.md:124; orchestrate/SKILL.md:70, :83; polish-pass/SKILL.md:101 (×2) |
| MEMORABLE_F23 | 4 / 5 | browser-qa/SKILL.md:82, :113; orchestrate/SKILL.md:70; polish-pass/SKILL.md:101 (×2) |

- **Files carrying `_F23`: 17** (re-derived by `grep -rl`), identical to sweep #31:
  browser-qa, design-taste-frontend SKILL + diagrams.md + review-hero.md,
  make-interfaces-feel-better, motion-advanced, motion-foundations, motion-patterns,
  orch-build-mvp, orchestrate SKILL + design-inventory.md + dispatch-prompt.md,
  polish-pass SKILL + alignment.md + typeset.md + slop-checklist.md, ui-ux-pro-max.
- **DYNAMIC_F23 unchanged at 8 lines / 9 occurrences**, as the M1 block header
  promises: the added sentence carries no token. Verified: the M1 sentence sits on
  `browser-qa/SKILL.md:56`, the same line that already carried DYNAMIC_F23 once.
- **M1 sentence present exactly once** in the built tree:
  `skills/browser-qa/SKILL.md:56` — "If the harness cannot drive an interaction the
  job calls for, record that interaction as unverified — a gap, never a silent pass;
  the Dynamic row is not ✓ on an interaction never driven." (`grep -c` = 1 for both
  "record that interaction as unverified" and "the Dynamic row is not"). It is
  appended immediately after the FAIL sentence ("A control that does not respond, or
  a state that changes without motion, FAILS the build.") inside the
  Dynamic-interface live check paragraph — the correct home, and it adds no new line
  (line 56 is one long line before and after), so no downstream line number moved.
- **No orphans:** every token named in a pointer resolves to its home file (e.g.
  FUNC_F23 at ui-ux-pro-max:49 is inside the pointer sentence "The full rule lives in
  `design-taste-frontend` step 4a (FUNC_F23)…"; AMBITION_F23 at design-inventory.md:8
  is a cross-reference to the orchestrate bar). No token is defined twice in
  conflicting senses.
- **Apply-script sub ids** (occurrence counts via `grep -o`): each occurs **×1 as a
  tuple** in `build.sh` and **0× in the built tree**, by design — including the new
  **DYNAMIC-BQA-01-M1 (tuple ×1, total in build.sh ×2, built tree 0×)**. Totals in
  build.sh (tuple + trailing comment / header mentions): MOTION-01–05 ×1 each;
  BQA-TYPEAUDIT, UIPRO-F7VAR, ORCH-TYPEAUDIT ×2 each; ALIGN_F23-A–E ×1 each;
  DYNAMIC-01/02/03 ×2 each; DYNAMIC-BQA-02 ×3; MEMORABLE-BQA-01 ×2;
  MEMORABLE-BQA-02 ×3. **DYNAMIC-BQA-01 total is now ×6, not ×2** — explained, not a
  defect: tuple + trailing comment on `build.sh:23958` (×2), M1 block header marker
  `24021` (×1) + header comment `24022` (×1), M1 tuple + trailing comment on `24034`
  (×2, the M1 sub id contains DYNAMIC-BQA-01 as a substring). All match verify23.py's
  assertions (which assert the tuple count, not the raw total, for DYNAMIC-BQA-01).

## 3. /demo never-automatic re-check

- Zero `demo` mentions (case-insensitive) inside the fix23 `build.sh` blocks
  (lines 23765–24049, all eight blocks); zero `auto-invok` / `automatically` there.
  Zero `demo` mentions inside the new M1 block alone (lines 24021–24049).
- Full-tree `/demo` grep (excl. node_modules): 163 matching lines, of which the
  overwhelming majority are asset demo pages (`assets/moments/*/demo.html`,
  `demo.css`, `demo.js` paths) and the pitch-deck-video skill's own usage docs —
  none of these is a pipeline dispatch. (Sweep #31 counted 172; the delta is grep
  scope — this run's count is over `skills agents commands rules hooks`, same as the
  anchor census. The command-dispatch sites below are unchanged, line for line.)
  The command-dispatch sites:
  - orchestrate SKILL.md:95 — "Demo — never automatic … NEVER dispatched by this
    pipeline. It runs ONLY when the user invokes `/demo` explicitly"
    (DEMOGATE_O4_F22); :97 — "(A demo video is filmed only when the user invokes
    `/demo` explicitly — it is never part of this order… DEMOGATE_O9_F22)".
  - orch-build-mvp SKILL.md:85 — "Demo — never automatic … `/demo` is not filmed
    here" (DEMOGATE_B2S1_F22).
  - orch-change-feature SKILL.md:51 — re-film only "If the user asks for a re-film,
    re-film via `/demo --rebuild`" (DEMOGATE_B3S1_F22); :52 — "never by a phantom
    upload, never by an automatic re-film".
  - rules/hackathon-mode.mdc:12 — "/demo is never part of this sequence — it runs
    ONLY when the user invokes it explicitly" (DEMOGATE_H2_F22); :68 — "The first
    build does NOT film `/demo` automatically" (DEMOGATE_H1_F22).
  - commands/demo.md + skills/pitch-deck-video/SKILL.md — the command's own
    definition; invocation is user-driven by construction, incl. `--rebuild` /
    `--script` / `--render` variants and opt-in `--montage` / `--explainer`
    ("opt-in, ask the user first").
  - `commands/orch-build-mvp.md:36` — "Do NOT film via `/demo` here — `/demo` runs
    ONLY when the user invokes it explicitly".
  - orchestrate/references/dispatch-prompt.md:30 — narration-key context carried
    "on a /demo dispatch when a narration key was received mid-build" (conditional
    on a dispatch, not a dispatch itself); design-inventory.md:147 — "Bang Motion
    layer (pitch-deck-video, /demo only)" (a catalog row, not an invocation).
- **All six DEMOGATE sites present at the same lines as sweep #31:**
  DEMOGATE_O4_F22 (:95), DEMOGATE_O9_F22 (:97), DEMOGATE_B2S1_F22
  (orch-build-mvp:85), DEMOGATE_B3S1_F22 (orch-change-feature:51),
  DEMOGATE_H1_F22 (hackathon-mode:68), DEMOGATE_H2_F22 (hackathon-mode:12).
- **Narration-key prompt fires ONLY when the user asked for a demo video:**
  orchestrate:58 — "ONLY when the user asked for a demo video; it never blocks the
  build" (also: "If the user did NOT ask for a demo video, do NOT send this prompt");
  hackathon-mode.mdc:12 — "only when the user asked for a demo video" (line 59
  repeats the guard); orch-build-mvp:32 — "If the user did NOT ask for a demo video,
  do NOT send this prompt". No fix23 text adds any narration-key or /demo invocation.
- No auto-invocation wording introduced by fix #23 or by the M1 change anywhere in
  the built tree.

## 4. Weaving-coherence pass — per-section table

Method: for each section, read the placed lines in context and confirmed (a) the
item sits in the SPEC'd flow (design-package step / named skill step / QA phase),
not appended at a file end; (b) its pointers resolve to a real home; (c) it does
not duplicate an existing rule without a recorded reason (duplication is either
explicitly pointer-only or carries a stated distinction). Line numbers below are
re-derived by this sweep; they match sweep #31's anchor table (no drift since the
M1 rebuild — the M1 sentence adds no line).

| Section | Placement (re-derived) | Coherence verdict |
|---|---|---|
| §1 Ambition | orchestrate SKILL.md:66 (inventory read), :68 (ambition bar: USED vs CONSIDERED-AND-REJECTED, blanket line fails, small-slice fails, without-package fails, MORE-not-louder, F6 primary gate), :149 (step-6 F6-primary-gate extension); inventory `skills/orchestrate/references/design-inventory.md` (INVENTORY_F23 :1, currency :17, usage rule :161, §1–§10 coverage); dispatch-prompt.md:24 (§5a) | CLEAN. All three ambition paragraphs sit inside the step-3 design-package flow, read-before-deciding is explicit ("READ `references/design-inventory.md` … BEFORE deciding"). Inventory covers all SPEC'd groups (counts spot-verified in §5 via verify23: styles 89, palettes 192, pairings 74, guidelines 120, icons 105, GSAP 17, charts 25, stacks 22, Taste 18 moments/13 dealt, Hallmark 50, Impeccable 62, less-flat-ui 23, motion A1–A20/B1–B20/17 examples, slop C1–C20/D1–D20, Vercel 16/104, glossary G1–G20, 11 libraries). No duplicate rule: the F6-primary-gate extension at :149 extends the step-3 bar rather than restating it. |
| THE CORE (§1) | orchestrate SKILL.md:70 (memorable paragraph, cross-references AMBITION/MOTION/HERO/FUNC/DYNAMIC_F23 ×1 each, no restatement); browser-qa SKILL.md:82 (Memorability verdict, MEMORABLE-BQA-01, "browser-qa's alone"); browser-qa:113 (Memorability report row, MEMORABLE-BQA-02); polish-pass SKILL.md:101 (memorability candidates, MEMORABLE_F23 ×2) | CLEAN. CORE sits between the AMBITION paragraph (:68) and the MOTION paragraph (:72) in the design-package step; the browser-qa verdict sits in the visual loop immediately after the hero verdict (:80); the report row sits after the Dynamic row (:112). "Over the top = ambition/impact, not loudness" and "quiet palette, cannot be forgettable" stated in all three homes. No D19_RULE rewrite (verify23 asserts D19_RULE byte-identical in Taste + orchestrate). |
| §2 Motion | orchestrate SKILL.md:72 (motion default, in design-package step after CORE); motion-foundations:205, motion-patterns:47, motion-advanced:49, make-interfaces-feel-better:109, ui-ux-pro-max:607 — each after `## Rules` / `### Motion` / `## Before Delivering App UI` as SPEC'd | CLEAN. Each insertion is at its documented anchor inside the skill's rules flow, not appended. Token routing (stagger 30ms, press 0.97, dropdowns 150–250ms) verified present in motion-foundations. Scroll-ban scope guard for Taste landing pages present in the MOTION-01 add-text and the W1 block header. Reduced-motion fallback carried on every MOTION_F23 line (verify23 asserts). |
| §3 Fonts | typeset lens `skills/polish-pass/reference/lenses/typeset.md:61` (full home: measurement method, T1a–T1d/T2/T3, clearance); slop-checklist.md:670 (checklist half); polish-pass SKILL.md:22 (harmony) + :101 (non-negotiable 5 wiring); browser-qa SKILL.md:78 (type-audit verdict, BQA-TYPEAUDIT); ui-ux-pro-max SKILL.md:270 (F7VAR_F23); orch-build-mvp SKILL.md:78 (static checks, ORCH-TYPEAUDIT); orchestrate SKILL.md:127 (Type list feeds audit + trio re-deal, TRIO_F23) | CLEAN. Fail conditions are concrete and checkable (T1a body ≤40% build share, T1b ≤55% per screen, T1c display ≥25%, T1d hero display > body, T2 trio re-deal, T3 variety floor max(3, ceil(N/20)) with ≥5% per face; clearance: T1a/T1b scoped-exception only with T1c still binding, T1c/T1d/T3 no clearance). The slop-checklist half explicitly states candidate-evidence-only standing ("NEVER a pass/fail verdict… browser-qa alone issues verdicts"). F4 unchanged (verify23 asserts the fix #19/#21 scope text untouched; enforcement is new caps/floor, not a rule rewrite). No duplication: typeset = full rule, slop = checklist half, browser-qa = verdict, each by pointer. |
| §4 Hero | design-taste-frontend SKILL.md:55 (House rules, after "Captivating hero" paragraph), :254 (Picks-block Hero-moment row), :507 (step-6 static checks), :552 (§5 Checklist first-screen bullet); review-hero.md:3 (inputs line) + :13 (review question); browser-qa SKILL.md:80 (hero verdict, HERO-BQA_F23); orchestrate SKILL.md:81 (per-slice brief) | CLEAN. Hero rule lives in Taste's House rules (the deal's home), consumed by the Hallmark hero review via the Picks block, judged by browser-qa as highest-weight with "merely adequate fails F6". Calibration present in all three homes (home/feed IS the hero surface; bar calibrated to the product's job; never a generic hero section pasted on). Static checks at Taste:507 are completeness-only with verdict reserved to browser-qa. |
| §5 Functionality | design-taste-frontend SKILL.md:411 (step 4a, after Anti-generic paragraph), :507 (step-6 static checks); diagrams.md:12 (FUNC-DIAG_F23, "THIS build's mechanism"); browser-qa SKILL.md:71 (Phase 3 step 5, FUNC-BQA_F23); ui-ux-pro-max SKILL.md:49 (pointer, FUNC-UIPRO_F23: "The full rule lives in `design-taste-frontend` step 4a"); orchestrate SKILL.md:81 (per-slice brief) | CLEAN. Rule is THIS-build-specific by construction (own pipeline/data/stack, real figures; preset = layout, never content). F2 stack labels covered/unchanged (verify23 asserts F2_RULE verbatim in Taste). The ui-ux-pro-max home is an explicit pointer, not a restatement — no duplication. Mechanism visible early ("hero surface or the first screen after it") in Taste, diagrams, and browser-qa. |
| §6 Alignment | browser-qa SKILL.md:61 (8 assertions a–h), :65 (widths), :69 (every-flow-state coverage), :118 (Alignment report section), :125 (coverage row), :134 (blocking-gap rule); polish-pass/reference/alignment.md (checklist file; assertions :30 OVERFLOW, :38 CENTER, :50 NAV, :57 GRID, :69 CLIP, :80 LABELS, :93 ACTIONS, :100 PANELS; tolerances + `getBoundingClientRect()` + align-audit.mjs model :15–26; coverage matrix :113; blocking-gap rule :132); polish-pass SKILL.md:98 (pointer, candidate evidence); orchestrate SKILL.md:91 (alignment coverage gate, BLOCK_F23 + COVER_F23) | CLEAN. Assertions are programmatic (0px overflow; ≤2px centering/grid/spacing; `scrollWidth - innerWidth == 0`; mid-band hero-GROUP centering with equal outer margins — the Home Run audit's −209px frame-only nuance is handled, not asserted naively; declared-intentional-bleed is the only escape with page overflow still 0). Coverage is mandatory at 1440 / 900 (band 768–1100, breakpoint ±1 probe + mid full-page shot) / 390 for EVERY flow state, and the new widths explicitly supersede the old 375/768/1440 breakpoints (bqa:65). The gate is blocking (DO NOT SHIP; empty matrix cell never SHIP / SHIP WITH FIXES / INCONCLUSIVE-as-pass). polish-pass runs the checklist as candidate evidence only, browser-qa remains sole verdict executor. |
| §9 Dynamic | motion-foundations SKILL.md:243 (DYNAMIC-01), motion-patterns:124 (DYNAMIC-02), motion-advanced:94 (DYNAMIC-03) — each after `## Decision Guidance`, fresh anchors, no collision with W1's MOTION-01–03 after `## Rules`; browser-qa SKILL.md:56 (Phase 2 step 6 live check + FAIL, DYNAMIC-BQA-01), :112 (Interactions/Dynamic report row, DYNAMIC-BQA-02); orchestrate SKILL.md:83 (dynamic story per slice brief, after HERO/FUNC paragraph); polish-pass SKILL.md:101 (reads story from decision record, DYNAMIC_F23 ×2) | CLEAN. The §9-vs-§2 distinction is stated in the text itself (orch:83: §2 is the motion-presence rule, §9 is the state-change/interactivity rule; live data IS the functionality showing, without restating §5) — no duplication. Each DYNAMIC add-text carries the complete reduced-motion fallback line and a full seven-dimension D19 line. Calibration ("dynamic never means gratuitous; motion serves the state change") present in DYNAMIC-01/02/03 and orch:83. |

### M1 coherence with §6 (the check this re-run was asked to make)

**CONFIRMED — the M1 sentence coheres with the §6 alignment section's
"wherever the harness allows" language (same disposition principle).** The §6
alignment assertions at browser-qa:61 open with "run these programmatic assertions
**wherever the harness allows**, on the live rendered page" — i.e. a capability
limit is a scope limit, not a silent pass. The M1 sentence at browser-qa:56 applies
the identical principle to interactions: "If the harness cannot drive an interaction
the job calls for, **record that interaction as unverified — a gap, never a silent
pass**; the Dynamic row is not ✓ on an interaction never driven." It is also
consistent with the §6 blocking-gap rule at browser-qa:134 ("A build with an
unverified width or an unverified flow state is NOT shippable — the gap is a blocking
finding, not a note"): an undrivable interaction is now recorded as unverified, so it
feeds the same gap machinery instead of vanishing. This closes the §7.4 open item
from sweep #31 (the DYNAMIC-BQA-01 undrivable-interaction note) — it is no longer
open; it is implemented in the built tree and asserted by verify23.py (check
"browser-qa dynamic live check: undrivable interaction recorded as unverified, never
a silent pass (M1)", PASS).

### Documentation note (not a plugin finding)

The §6 prose tables in `fix23/disposition-merged.md` and in sweep #31 §4 cite the
browser-qa alignment paragraph as `:60`, widths as `:64`, coverage as `:68`. The
re-derived values are **:61, :65, :69** (grep-verified above; sweep #31's own anchor
table already said :61/:65/:69). This is pre-existing prose drift in those documents,
not a build change: the M1 sentence lives inside line 56 and adds no line, so it
cannot have shifted any downstream line number, and every other browser-qa anchor
(:71, :78, :80, :82, :113, :125, :134) matches the disposition exactly. The plugin
text is correct and complete; the two prose tables should be corrected to :61/:65/:69
when next edited. Not flagged as a finding — it changes nothing in the built tree.

## 5. Verifiers re-run by this sweep

| Verifier | Result (re-run here) | Expected | FAILs |
|---|---|---|---|
| fix23/verify23.py | **211/212** | 211/212, sole FAIL owed manifest | Only: `fix23/MANIFEST.md exists and records build.sh lines + md5 (OWED…)` — `fix23/MANIFEST.md` does not exist yet (`ls` confirms). Excluding it: 211/211. |
| fix22/verify22.py | **368/369** | 368/369 | Only the frozen post-fix22 build.sh fingerprint (expects 23,774 lines / md5 `4799a819…`, now superseded by fix #23 + M1). |
| fix21/verify21.py | **96/102** | 96/102 | Only the frozen post-fix21 fingerprint (`build.sh is 23647 lines, md5 8dfacb47…`) + its 5 cascades (`fix15/17/18/19/20 verifier still passes` lines) — the allowed pattern. |

verify23.py's own prior-verifier leg also passed all seven (fix15 42/44, fix17 58/60,
fix18 69/72, fix19 71/76, fix20 164/169, fix21 96/102, fix22 368/369, each with only
the allowed fails). Note the verify23 total moved 210/211 → 211/212 vs sweep #31:
the new check is the M1 assertion (undrivable interaction recorded as unverified),
which PASSES; the sole FAIL remains the owed manifest.

## 6. Banned terms, Grok pins, counts

- **Banned terms 0** — `grep -riE "claude|codex|anthropic|opus|sonnet|haiku|composer-2.5"`
  over skills/agents/commands/rules/hooks/README.md (excl. node_modules): 0 files.
- **Grok pins only** — `grok-4.7-high` in 26 files; `cursor-grok-4.6-high-fast` in
  85 files; bare `grok-4.6-high-fast` 0 lines.
- **Counts re-derived:** skills 166, agents 72, rules 123, commands 87, hooks 15
  (entries in `hooks/hooks.json`; the `hooks/` dir holds 17 files — 16 `.js` +
  `hooks.json`); trigger keys 64 (`withTriggers` == 64 == len(triggers)).

## 7. Open items (carried, explicitly — not findings this round)

1. **Manifest owed (known close step, NOT flagged this round):** `fix23/MANIFEST.md`
   does not exist; it is the sole verify23 FAIL (211/212). The manifest worker writes
   it; nothing in this sweep creates it.
2. **styles.csv 89 vs header 80:** verified as recorded, not resolved — csv has 89
   data rows (`wc -l` − header); ui-ux-pro-max header says "80 searchable styles
   (51 active)" (SKILL.md:3, :8); inventory:29 records both with "the csv is the
   inventory source"; inventory:157 lists styles (89 rows). If the header is the
   intended count, the inventory's styles line needs a correction — parent call.
3. **B3/B15/B4 conflicts (carried verbatim from fix #22, parent adjudicates):**
   verified present as flags in two places — inventory:104 tail ("known open
   conflicts (B3 30ms vs Rule 5 floor 0.05s; B15 0.8x vs quick-reference ~60–70%;
   B4 0.97 vs `scale.press` 0.95) are carried as flags, never silently resolved")
   and the W1 block header in `build.sh` (lines 23781–23783) / `fix23/apply-w1.py:45–47`
   (also fix22-era comment at build.sh:23654). No token value changed by this fix.
4. **DYNAMIC-BQA-01 undrivable-interaction note — CLOSED by M1 (was open in sweep
   #31 §7.4):** the live check at browser-qa:56 now explicitly says to record an
   undrivable interaction as unverified rather than silently pass (sentence quoted
   in §2, `grep -c` = 1). No longer open; listed here only to record the closure.
5. **daisyUI 65 → 68 correction:** verified — the built inventory says **68 twice**
   (design-inventory.md:133 "The daisyUI 5 component menu (68 components)"; :146
   "daisyUI `daisyui@5.7.50` (Tailwind v4 plugin, 68 components)") and **65 zero
   times** (`grep -c '65'` on the inventory file = 0); design-system/SKILL.md:40
   agrees ("68 components"). The 65 was the §17 research count, corrected to the
   plugin's recorded 68.

## 8. Commands run (method)

All run read-only from `~/workspace/hackathon-plugin` (built-tree greps from
`hackathon-ecc/`):

- `wc -l build.sh build.sh.before-fix23 && md5sum build.sh build.sh.before-fix23`
  + `diff build.sh.before-fix23 build.sh | grep -c '^>'` / `'^<'`
  + `diff build.sh.before-fix23 build.sh | grep -E '^[0-9]'` (single hunk
  `23764a23765,24049`)
- `grep -n "^# --- fix23" build.sh; grep -n "^# STEP 5" build.sh`
  + `sed -n '24021,24049p' build.sh` (M1 block read in full)
  + python block-size computation (56/34/39/37/44/46/29 = 285)
- `ls hackathon-ecc/skills|wc -l` (×4 dirs) + python json counts for hooks/triggers
- Per-token census loop: `grep -rn/ -l/ -rho` for all 17 `_F23` tokens; `grep -rl "_F23"`
  (17 files); per-line multi-occurrence checks via `grep -o … | wc -l`; full
  `grep -rn` location dump for all 17 tokens (line numbers in §2)
- M1 sentence: `grep -n "record that interaction as unverified"` (= 1, bqa:56),
  `grep -c "the Dynamic row is not"` (= 1); `grep -n "DYNAMIC-BQA-01-M1" build.sh`
- Sub-id loop: `grep -o "('<id>'," build.sh | wc -l`, `grep -o "<id>" build.sh | wc -l`,
  `grep -rho "<id>" hackathon-ecc/{skills,agents,commands,rules,hooks} | wc -l`
  for all 21 sub ids incl. DYNAMIC-BQA-01-M1; `grep -n "DYNAMIC-BQA-01" build.sh`
  (explains the ×6 total)
- `sed -n '23765,24049p' build.sh | grep -ci demo` (= 0) and `auto-invok|automatically`
  (= 0); M1 block alone `sed -n '24021,24049p' build.sh | grep -ci demo` (= 0)
- `/demo` tree grep (163 lines over skills/agents/commands/rules/hooks), DEMOGATE grep
  (6 sites, lines re-derived), narration-key exact-string greps (orchestrate:58,
  hackathon-mode.mdc:12/:59, orch-build-mvp:32)
- Banned-term `grep -riE … -l` (= 0 files); Grok pin file counts (26 / 85 / 0)
- `sed -n` spot-reads: bqa :56/:60–70/:118/:125/:134, orchestrate :56–58/:66–83/:149,
  alignment.md :1/:15–26/:30/:38/:50/:57/:69/:80/:93/:100/:113/:132, inventory
  :29/:104/:133/:146/:157, uipro SKILL.md:3/:8, design-system:40
- Open-item greps: styles.csv row count (89), `grep -c "65"` on inventory (= 0),
  B3/B15/B4 flag lines (inventory:104, build.sh:23782, build.sh:23654)
- `python3 fix23/verify23.py` → 211/212; `python3 fix22/verify22.py` → 368/369;
  `python3 fix21/verify21.py` → 96/102 (tails + FAIL lines re-read directly)

## Verdict

**SWEEP #31 RE-RUN: CLEAN — 0 blocking, 0 minor.**

The M1 change is exactly as described: one 29-line runtime-patch block in `build.sh`
(lines 24021–24049, sub DYNAMIC-BQA-01-M1 ×1 as a tuple), adding one sentence to
`browser-qa/SKILL.md:56` with no `_F23` token, no new line, and no downstream line
shift. The new build is 24,059 lines, md5 `df2cb85055efc87637d3cb0b1e7061a2`,
diff +285/−0. Every `_F23` token count is unchanged from sweep #31, every sub id
resolves ×1 as a tuple with 0× in the built tree, the /demo gates are intact at all
six sites, weaving coherence is CLEAN for §1–§6 + §9 + THE CORE, the M1 sentence
coheres with §6's "wherever the harness allows" principle and closes the
DYNAMIC-BQA-01 open item, verify23 passes 211/212 with the sole FAIL the owed
manifest, and prior verifiers show only the allowed frozen-fingerprint fails.
Banned terms 0, Grok pins only, counts 166/72/123/87/15, trigger keys 64. The only
failing check anywhere is the owed `fix23/MANIFEST.md` (verify23 211/212), which the
task explicitly excludes from flagging this round. Open items §7.2–§7.3 and §7.5 are
carried parent adjudications, verified present as recorded flags, not silently
resolved; §7.4 is closed by M1.
