#!/usr/bin/env python3
"""Assemble fix22/MANIFEST.md (coordinator tool).

Writes the manifest from:
  - the prose sections below (scope, additions, placement map,
    adjudications, apply-time decisions, weaving/demo gates, results),
  - the 144-item disposition table copied verbatim from
    fix22/disposition-merged.md (line numbers in that table are as of
    the Audit #67 build; anchors/tokens are the stable locators).

Run by the coordinator AFTER the final build + verify22 + sweep #30c +
Audit #69 + dry-run #37 re-re-run, with the final numbers filled in the
RESULTS dict below.
"""
import os

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
FIX22 = os.path.join(PLUGIN, "fix22")

RESULTS = {
    # Final numbers at close time (Nov 13, 2026, ~02:20 UTC).
    "build_lines": "23774",
    "build_md5": "4799a819791b9c3ec4c19136ad698397",
    "build_diff": "+127/−0 (23,647 → 23,774 lines, exactly 2 hunks)",
    "verify22": "369/369 PASS (exit 0; 368 checks + 1 manifest-confirmation check that only runs once the manifest exists)",
    "audit68": "ZERO (0 blocking, 0 minor) — see fix22/audit69-report.md. Audit #68 re-run preceded it: NOT ZERO (0 blocking, 2 minor — M-1 :22 sequence, M-2 manifest pointer; both fixed).",
    "dryrun37": "42/42 fixtures + 58/59 /demo checks — 1 FAIL is ENVIRONMENTAL, not a plugin defect (see §6): node scripts/qa.mjs exits 1 only because Chrome cannot reach fonts.gstatic.com in this sandbox; the Remotion invocation fix is proven live (resolves past npx, bundles, begins rendering). Full live qa.mjs exit-0 on a normal network is OWED to the live smoke test. See fix22/dryrun37-rerun2-report.md.",
    "sweep30b": "CLEAN (0 blocking, 0 minor) — see fix22/sweep30c-report.md. Sweep #30b re-run preceded it: 1 blocking + 2 minor (Remotion invocation form; orch-build-mvp :32; manifest pointer — all fixed).",
    "weaving": "CLEAN for all §1–§17 (sweep #30c per-section table with current line numbers)",
    "demo_callable": "PASS by wiring + live partial execution — /demo command present/wired, explicit invocation reaches the filming pipeline (dry-run re-re-run 13/13 removal checks + 35/35 contract checks); no live film executed in this environment (see §6)",
    "demo_not_auto": "PASS — 0 auto-invocations anywhere (sweep #30c + Audit #69, full-context reads); 20 DEMOGATE tokens, each exactly once in the built tree (see §6)",
    "demo_contract": "PASS as written — F1–F6, voice rules, $10 cap, local-only filming, Bang port unchanged (Audit #69 + dry-run re-re-run 35/35); live film/render not executed in this environment (see §6)",
    "banned": "0 in the built tree (case-insensitive, excl. node_modules)",
    "counts": "166 skills / 72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys",
}

disp = open(os.path.join(FIX22, "disposition-merged.md"),
            encoding="utf-8").read().split("\n")
# Table rows: the header + separator + 144 item rows.
rows = [l for l in disp if l.startswith("| ")]
table = "\n".join(rows)

BODY = f"""# Fix #22 — MANIFEST

**Fix:** weave 7 @charles.unemployed reels (142 items) + H1/H2 accents + Mobbin + direct-don't-describe + 4 libraries + Bang Motion port + §13 3D/depth + §14 Thinking Orbs + §15 4 libraries + §16 Vercel web-design-guidelines + §17 3 libraries/tools into the hackathon-ecc Cursor plugin's design process.
**Authority:** `fix22/SPEC.md` (§1–§17) + `fix22/PARENT-GUIDANCE.md` + `fix22/parent-addendum-nov12.md`.
**Close date:** Nov 12–13, 2026. **Coordinator:** fix #22 follow-up coordinator (session 71cf20c8).
**Status:** CLOSED — with one environment-limited dry-run check recorded as owed (see Results and §6): the full live `qa.mjs` exit-0 on a normal network was not provable in this sandbox (Chrome egress blocked) and is owed to the live smoke test in Anish's Cursor. Nothing else is open.

## Results

build.sh lines: {RESULTS["build_lines"]}
build.sh md5: {RESULTS["build_md5"]}
- build.sh diff vs pre-fix22 (`build.sh.before-fix22`, 23,647 lines): {RESULTS["build_diff"]}
- verify22.py: {RESULTS["verify22"]}
- Audit #69 (final; #68 re-run preceded it): {RESULTS["audit68"]}
- Dry-run #37 (re-re-run, final): {RESULTS["dryrun37"]}
- Sweep #30c (final, incl. weaving-coherence pass): {RESULTS["sweep30b"]}
- Weaving-coherence: {RESULTS["weaving"]}
- /demo (a) callable: {RESULTS["demo_callable"]}
- /demo (b) never automatic: {RESULTS["demo_not_auto"]}
- /demo (c) contract intact: {RESULTS["demo_contract"]}
- Banned terms in the built tree: {RESULTS["banned"]}
- Counts (skills/agents/rules/commands/hooks; trigger keys): {RESULTS["counts"]}

## 1. The 144-item disposition table — zero unaccounted

The table below is copied verbatim from `fix22/disposition-merged.md` (built from the six source dispositions after the post-fix22 rebuild; status vocabulary: **new** = did not exist, **partial** = mechanism existed, the rule/value/wording is new, **covered** = already existed, no new text, **pointer** = points at an existing home, does no restating). Line numbers in the Placement column are as of the Audit #67 build (build.sh 23,732 lines); the §13–§17 inserts + the demogate edits shift later line numbers — sweep #30c's independent per-row check found ~51–64 rows drifted, content verified present in every case — so the anchor tokens (`_F22`) are the stable locators, not the line numbers. **144 items, zero unaccounted:** every item is placed, already-covered, deduped, or dropped with a parent-grade reason in its source disposition file (`fix22/disposition-A.md` … `disposition-G.md`, `disposition-merged.md`).

{table}

## 2. Process / asset additions recorded separately (§8–§17)

These are NOT part of the 144-item table; they are process/asset additions recorded here.

### §8 — H1 color accents + H2 accentuation accents
- H1: one accent colour, used for action/emphasis only; accent sprawl is a polish-pass flag (`ACCENT_F22` in ui-ux-pro-max + slop checklist).
- H2: every screen declares an accent hierarchy (what draws the eye first/second/third); the hierarchy is a D19-recorded decision (`ACCENTUATION_F22` in orchestrate + ui-ux-pro-max + slop checklist).

### §9 — Mobbin as pattern research
- Pattern research before generating direction (orchestrate `MOBBIN_RESEARCH_F22`); pattern reference while building (Taste + ui-ux-pro-max `MOBBIN_PATTERN_F22`); QA convention check in polish-pass (`MOBBIN_QA_F22`). Free tier only, never blocked on Mobbin, never a Mobbin URL as a source (anti-derivative rule stands).

### §10 — Direct-don't-describe
- Directives with exact values, not prose descriptions (`DIRECTIVES_F22` in orchestrate, Taste, ui-ux-pro-max, GAN planner/generator/evaluator, polish-pass). Prose-only FAILS the handoff check.

### §11 — 4 asset libraries
- Lenis (`lenis@1.3.27`, MIT, smooth scroll, never on Taste landing pages); GSAP (`gsap@3.15.1`, GreenSock Standard "no charge" — NOT MIT — deviation D1; `--domain gsap` + 17 presets + ScrollTrigger); Vanta (`three@0.134.0` scoped pin, reduced-motion + mobile-fallback + scrim 4.5:1); React Bits (pinned commit `9d9c687d…`, MIT + Commons Clause — deviation D2, React/Next only). Three.js scoped pins: Vanta 0.134.0 / general 0.185.1 / Bang 0.161.0. Running total after §11: 4.

### §12 — Bang Motion port into pitch-deck-video (/demo)
- Anti-slide checks, one-world/camera/persistent-subject architecture, 10 style directions + 19 opener concepts as menus, kinetic typography as §10 directives, 6 explainer styles. Pin SHA `c1aa65e921c970d858705fcb4a53a8294d1a4131`; repo quiet since Sep 15, 2026; SKILL.md in Indonesian, ported in English; distilled. GSAP converged on 3.15.1 (Bang's 3.12.5 recorded as Bang's version only). /demo still films the REAL app locally; F1–F6, voice rules, $10 cap, local-only filming, under 2:10 / max 2:30 unchanged.

### §13 — 3D / depth
- Depth strategy named per surface (flat / layered / deep-3D / parallax / Vanta scene / 3D-transform hero / camera-through-world), with exact values per §10, recorded in `docs/design-tokens.md`; a flat surface is an explicit `flat by choice — <reason>`. Depth as the SEVENTH D19 dimension via an extension line immediately after the existing `D19_RULE` block in both canonical homes (orchestrate, Taste) + a mirror in ui-ux-pro-max — `D19_RULE` itself is byte-identical (verify19 asserts it as a substring). Depth tokens in motion-foundations (`depthTokens`: perspective 1000, parallax near 0.5 / mid 0.25 / far 0.1, tilt.max 6°, elevation raised 8 / floating 16 / modal 24); parallax + 3D-transform hero patterns in motion-patterns; depth rules in ui-ux-pro-max; depth check (D1–D6) in the polish-pass slop checklist; texture/depth overlap note in less-flat-ui (Soft Shadow #23 is BOTH). Theme-matched; scrim 4.5:1; reduced-motion + mobile fallback. No existing depth-as-design-axis rule existed before this (verified: 3 "Depth" hits in build.sh are redesign-depth levels; 24 lowercase hits are unrelated; built-tree mentions are a principle, a shadow note, and a redesign note).

### §14 — Thinking Orbs
- Jakub Antalik's thinking-orbs (`thinking-orbs@0.3.2`, MIT, React >= 18). NINE verified states — working, searching, solving, listening, connecting, weaving, composing, breathing, shaping — and NO state named "thinking" (the SPEC's "thinking = reasoning" mapping draft is corrected: reasoning maps to working/solving; the breathing state's aria-label reads "Thinking…" but breathing is idle/waiting only). State-matched, never decorative, never a general spinner; menu not defaults; monochrome theme ink; two tuned sizes (64 chat-avatar, 20 inline-text); 2D canvas, 60fps, offscreen/hidden pause, DPR capped at 2, reduced-motion renders a frozen one-frame orb. React Native exists in-repo only (not on npm, not run on a device); SwiftUI planned only. Cursor gravity is optional, off by default, verify-first. **RareFormLabs connection unresolved — asset verified independently** (no link between RareFormLabs and these orbs found; never invent one).

### §15 — 4 more libraries (cindie.zhu reel)
- react-three-fiber (`@react-three/fiber@9.8.2` React 19 / `@8.18.0` React 18, MIT; peer `three@0.185.1` + `@types/three@0.185.1`) — THE 3D implementation layer for React; STRICT pairing v8↔React 18, v9↔React 19. Ecosystem: drei, Rapier, postprocessing, XR.
- liquid-glass-js (dashersw, MIT, commit `78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a`) — Apple-style liquid glass, real refraction via WebGL 2.0; NO npm package — copy `container.js`, `button.js`, `glass.css`; html2canvas@1.4.1 for page sampling (perf note recorded). Namesake ozcanyldzhn/liquid-glass.js is a DIFFERENT library (npm package, SVG displacement) — never confuse them.
- ShaderGradient (`@shadergradient/react@2.4.20`, ESM-only; MIT declared in package.json + README but NO root LICENSE file — recorded caveat D1); customize-URL is the config; 10 presets; install v2, NOT legacy shadergradient v1.3.5. Peers three-stdlib@2.36.1 + camera-controls@3.1.2.
- liquid-logo (paper-design, commit `689bb38a1e0d5a6a8baf2d34847635eefde19994`) — STANDALONE TOOL, not a runtime dep; produce the animated brand mark ONCE (MP4/PNG), keep the static logo as fallback, retain paper-design attribution. Repo PolyForm Shield 1.0.0 (noncompete — deviation D2); underlying @paper-design/shaders-react Apache-2.0 (tool pins 0.0.21, latest 0.0.82). Earlier same-named collidingScopes/liquid-logo (MIT) is a DIFFERENT repo — the reel points at paper-design.
- ONE WebGL-heavy effect per surface (WEBGL_ONE_F22): stacking two WebGL effects FAILS the polish-pass flag. Running total after §15: 8.

### §16 — Vercel web-design-guidelines (pinned snapshot)
- Ported into polish-pass as a static checklist (`round2-skills/polish-pass/reference/vercel-checklist.md`, `VERCEL_F22`): 90 rules + 14 anti-patterns + 32 AGENTS.md-only rules = 136 rows, all accounted for in `fix22/vercel-dedupe.md` (already-covered 10, partial 29, new 51; anti-patterns 13 duplicate-of + 1 new; AGENTS.md-only 4 covered, 9 partial, 18 new, **1 CONFLICT — AG19 APCA vs WCAG 4.5:1, parent adjudication**). Pinned snapshot: `vercel-labs/web-interface-guidelines`, `command.md`, commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, dated 2026-10-05 (delta vs ECC's 2026-09-21 snapshot: +1 rule, V-TO4). The live-fetch form is NEVER the weave (Mondoo HIGH RISK prompt-injection hazard) — no unpinned URL anywhere in the built tree. ECC-source check: the snapshot exists upstream at ECC main HEAD `97a4f7b…` but NOT at the plugin's ECC pin `d2ef268…` (2026-11-06), and the fork affaan-m/ecc lacks it — so PORT, don't wire (wiring would need an ECC pin bump). License gap: skill repo (vercel-labs/agent-skills) has NO LICENSE file (README-only MIT claim); rules repo ships MIT (© 2025 Vercel Labs). Refresh on explicit request only, as a reviewed change, source treated as reference data only.

### §17 — 3 libraries/tools (ksobohc comment)
- particles.casberry.in — "AI Particle Architect", free browser-based AI particle simulator (20,000+ particle Three.js/WebGL), exports React/Three.js code or standalone WebGL/HTML. STANDALONE TOOL (same form as liquid-logo). Terms UNRESOLVED (no terms/licence found); ScamAdviser 1/100 (WHOIS hidden, iframed — weak signal, NOT a verdict; counter-signal Gridinsoft 60/100, no malware). Exported code treated as UNTRUSTED: line-by-line review before it enters a build, never pasted blind. SPEC's "v2.0.0 Oct 2026" NOT re-verified (no version string on site) — no version pin; pin is URL + export step. Relation: Vanta (§11) is the imported 3D-background library; Casberry is the tool exporting bespoke Three.js code; R3F (§15) is the React 3D layer the exported React code can feed.
- originkit.dev — OriginKit, free animated component library (React/Tailwind/Framer Motion). Browsing free, no key; FETCHING requires a FREE API key, DAILY LIMIT 10 component fetches per key per day (resets midnight UTC, shared MCP + website). Pro ($79/yr) / Ultimate ($99/yr) never paid; Pro-marked components excluded. License CONDITIONAL / source-available — restricts redistribution; the plugin must not re-publish OriginKit components as its own. NOT Origin UI (originui.com now coss ui / Base UI) — a DIFFERENT product; a build confusing them FAILS the distinction check. Count discrepancy recorded, not picked: homepage 805, skill README 50 across 6 categories, pricing footer 60, third-party guide 547 (SPEC's 82 superseded). MCP NOT wired (endpoint path unsettled: /mcp vs /vellumai vs /v1/registry — moot); default is copy-paste; key env-only, never in a file. Dedupe vs React Bits (§11): React Bits is the importable MIT library; OriginKit is the browsable catalog for animated flourishes.
- daisyui.com — daisyUI 5 (`daisyui@5.7.50`, MIT, repo saadeghi/daisyui ~42.5k stars), Tailwind CSS v4 plugin (`@plugin "daisyui"`), 68 components, 0 JS, 0 dependencies, framework-agnostic. daisyUI 5.x + Tailwind v4 ONLY. FIT-CHECK (binding): a build shipping its default theme unexamined FAILS (generic look — the Home Run lesson); components are a MENU, re-themed through the brand/theme deal. Dedupe vs shadcn (already pinned @4.23.0): daisyUI is the Tailwind-native library (semantic classes, zero JS, any framework); shadcn is the React copy-paste set. Paid extras OUT (Blueprint MCP $22/mo not wired; Dashboard/Charts/Figma/templates paid).
- Running total of asset libraries/tools in fix #22: §11's 4 + §15's 4 + §17's 3 = **11**, in three integration forms (npm plugin dependency; browsable library copy-paste/MCP capped; standalone tool exporting code).

## 3. Placement map

| Addition | Home skill(s) | Anchor token | Mechanism |
|---|---|---|---|
| A/B principles, laws, tokens, rules | motion-foundations, motion-patterns, motion-advanced, make-interfaces-feel-better, ui-ux-pro-max | PRINCIPLES_F22, LAWS_F22, ANIM_TOKENS_F22, ANIM_RULES_F22, ANIM_ADV_F22 | fix22.py runtime block |
| C slop indicators | polish-pass slop-checklist + wiring | SLOP_F22 | staged |
| D unslop fixes | polish-pass unslop-fixes + wiring | UNSLOP_F22 | staged |
| E trends | Taste + 15 Hallmark theme files | TRENDS_F22 | staged |
| F backgrounds | less-flat-ui (verification-only) | — | — |
| G design terms | Taste glossary + owning-skill pointers | GLOSSARY_F22 | staged + runtime |
| H1/H2 accents | ui-ux-pro-max, orchestrate, polish-pass | ACCENT_F22, ACCENTUATION_F22 | runtime + staged |
| §9 Mobbin | orchestrate, Taste, ui-ux-pro-max, polish-pass | MOBBIN_RESEARCH_F22, MOBBIN_PATTERN_F22, MOBBIN_QA_F22 | staged + runtime |
| §10 directives | orchestrate, Taste, ui-ux-pro-max, GAN agents, polish-pass | DIRECTIVES_F22 | staged + runtime |
| §11 libraries | motion-foundations, motion-patterns, ui-ux-pro-max, Taste | LENIS_F22, GSAP_F22, SCROLLTRIGGER_F22, VANTA_F22, REACTBITS_F22 | runtime + staged |
| §12 Bang | pitch-deck-video (staged source) | BANG_ANTISLIDE_F22, BANG_ONEWORLD_F22, BANG_STYLES_F22, BANG_OPENERS_F22, BANG_KINETIC_F22, BANG_EXPLAINER_F22 | staged |
| §13 depth | orchestrate, Taste, ui-ux-pro-max, motion-foundations, motion-patterns, polish-pass, less-flat-ui | DEPTH_F22 | staged (DEPTH-01–08) + runtime (DEPTH-09–13) |
| §14 orbs | motion-patterns, motion-foundations, ui-ux-pro-max, orchestrate, polish-pass | ORBS_F22 | runtime (ORB-MP/MF/UIPRO) + staged (ORB-ORCH/PP1/PP2) |
| §15 libraries | motion-foundations, motion-patterns, ui-ux-pro-max, Taste, less-flat-ui, polish-pass | R3F_F22, LIQGLASS_F22, SHADERGRAD_F22, LIQLOGO_F22, WEBGL_ONE_F22 | runtime (L15-01–04, L15-06) + staged (L15-05, L15-07, L15-08) |
| §16 Vercel | polish-pass (new checklist file), ui-ux-pro-max quick-reference, motion-foundations | VERCEL_F22 | new file + runtime (VERCEL-02–07) |
| §17 libraries | motion-foundations, motion-patterns, ui-ux-pro-max, design-system, Taste, polish-pass | CASBERRY_F22, ORIGINKIT_F22, DAISYUI_F22 | runtime (L17-01–04) + staged (L17-05–07) |

## 4. Adjudication notes (carried + new)

Carried from wave 1 (parent adjudicates; applied exactly as specified, flags in the text):
- B3: 30ms stagger token vs Rule 5 0.05s floor (CONFLICT FLAG in the token comment).
- B15: 0.8x exit factor vs quick-reference ~60–70% (CONFLICT FLAG in the token comment).
- B4: 0.97 press scale vs `scale.press` 0.95 (observation, not resolved by editing).
- C13 vs Impeccable eyebrow tension (eyebrows are a slop flag; the Impeccable craft floor also governs them — the slop check and the craft floor agree the eyebrow is flagged; the tension is which rule a build cites first).
- Hallmark count correction: 16 Range lines in 15 theme files (Blueprint carries E3+E17), not 15/14.
- Three.js scoped pins (Vanta 0.134.0 / general 0.185.1 / Bang 0.161.0) — NOT a single version.
- Bang pin SHA `c1aa65e9…` + repo staleness (quiet since Sep 15, 2026) + SKILL.md in Indonesian (ported in English).
- GSAP license deviation D1 (GreenSock Standard "no charge", NOT MIT); React Bits deviation D2 (MIT + Commons Clause); Vanta staleness D3.

New in §13–§17 (parent adjudicates; applied as specified):
- §13 depth token values (DEPTH-09): perspective 1000, parallax {{near 0.5, mid 0.25, far 0.1}}, tilt.max 6°, elevation blur {{8, 16, 24}} — the §13 agent's values, no SPEC source. Same pattern as the AB-03 conflict flags.
- §13 "six dimensions" staleness: the extension line makes the count seven, but existing texts still say "six" (Taste trend line, `D19_APP`, X1, `DIRECTIVES_F22`, wave-1 D19 bullets). DECISION (coordinator, recorded): leave the frozen fix #19 texts byte-identical (they are asserted verbatim by prior verifiers) and let the extension line stand as the amending record. Do NOT sweep "six" → "seven" without a parent decision.
- §14 orbs mapping correction: "thinking = reasoning" is WRONG (no thinking state); reasoning → working/solving. No D19-reason clearance for a mismatched or decorative orb (stricter than §4a). Pin 0.3.2 (published) vs repo 0.3.1 (repo package.json). Gravity as a requirement needs verification against pinned 0.3.2 (documented in the Libraries.dev skill reference, NOT in the standalone repo's component). Repo-migration note: npm 0.3.2's repository field points at the Libraries.dev monorepo `packages/thinking-orbs`; standalone repo commit de85557, 4,014 stars.
- §15 deviations D1–D7 (see `fix22/libraries15-patches.md` §6): D1 ShaderGradient missing root LICENSE; D2 liquid-logo PolyForm Shield noncompete; D3 liquid-glass-js single-commit pin (no tags/releases); D5 three.js pins coexist three-ways (Vanta 0.134.0 / general 0.185.1 / Bang 0.161.0); D7 §13 Depth D19 dimension not pre-empted (the §15 texts cite §13 depth rules that land in the same program — order §13 before §15 in application). SPEC wording flag: paper-design (2025-02-18) predates collidingScopes (2025-03-03), so calling collidingScopes "earlier" is wrong; resolution (reel = paper-design) unchanged.
- §15 liquid-glass-design dangling reference — resolved as option (b), corrected: the dangling skill-text references were already corrected by the audit20a Fix 2a/2b deletions; the only surviving build.sh hit is the pi-core governance list (`build.sh:18731`, expected-unshipped by design, must NOT be edited). Built-tree skill text has 0 hits. The liquid-glass-js integration is NEW implementation, NOT a gap-fill; no skill named `liquid-glass-design` is created.
- §16 Vercel AG19 CONFLICT: AGENTS.md rule AG19 (APCA contrast) vs the plugin's WCAG 4.5:1 craft floor — parent adjudication. (Dedupe: `fix22/vercel-dedupe.md`, 136 rows, zero unaccounted.)
- §16 Vercel license gap: skill repo has NO LICENSE file (README-only MIT claim); rules repo ships MIT. Recorded, not assumed away.
- §17 Casberry terms unresolved — consider a harder line (bar exports from shipped builds until terms confirmed). OriginKit terms not re-read from the site (recorded per the Design Atlas review). MCP endpoint path unsettled (/mcp vs /vellumai vs /v1/registry) — moot, no MCP wiring. Casberry version unre-verified (SPEC's "v2.0.0 Oct 2026" not recorded as a pin).
- §17 token-sharing note: LIQLOGO_F22 occurs twice in ui-ux-pro-max (L15-03 + L15-04) and VERCEL_F22 twice in polish-pass SKILL.md (VERCEL-02 + VERCEL-03) — both are pointer mentions of the same anchor token in one file, not orphaned anchors; the sweep's "exactly once per file" convention is about the anchor LABEL (one home per token), and the home files are the checklist (VERCEL_F22) and Taste step 4a (LIQLOGO_F22). Sweep #30c verified: 57 _F22 tokens total (37 pre-demogate + 20 DEMOGATE), every anchor resolves, no orphans. (Sweep #30b's "38" was a miscount in that report, not a lost token — corrected by the #30c re-count.)
- §16 Vercel checklist hit-area wording (sweep #30b Finding 2, fixed): the three parentheticals citing "(40x40px, ideally 44x44px — Group A A14 / G8)" were wrong — the live rule is 44x44px minimum — and now read "44x44px minimum, the plugin floor" (vercel-checklist.md V-FO6 + vercel-dedupe.md V-FO6/AG1).

## 5. Apply-time decisions (coordinator, Nov 12–13)

- **Tuple format resolved:** `fix22.py` PATCHES are 6-tuples `(id, rel, old, new, mode, token)` (verified by reading `fix22.py:1044-1141` + `preflight()`); the GENERATED build.sh subs are 5-tuples (token dropped). Audit #67's "5-element" claim was about the generated subs, not the PATCHES list. All §13–§17 patches were applied as 6-tuples.
- **D-A1 ('after' blank-line normalization):** the wave-1 convention is that an 'after' insert starts with a paragraph break (`\\n\\n`, cf. AB01). The §13/§14 spec fences lacked it (their 'after' texts started directly with content), so the applier prepended `\\n\\n` to DEPTH-01/02/03/04/05/07/08/11/12/13 and replaced the leading single space of ORB-ORCH/ORB-PP2 with `\\n\\n`. §15/§17 'after' texts already started with a blank line; Vercel tuples are verbatim Python literals (VERCEL-02/03's leading space is a deliberate mid-sentence continuation). Whitespace only — no content changed.
- **D-A2 (L15-06 edit point):** L15-06 was specified as an edit to the shared global Cursor skill (`~/workspace/cursor-skills/less-flat-ui/SKILL.md`). CONVERTED to a runtime-block patch on the built copy (`skills/less-flat-ui/SKILL.md`, before `### 3. Thermal gradients`). The fix22 block runs after the `build.sh:263` copy of the global source, so a runtime patch survives rebuilds; editing the global source would leak a plugin-scoped note into Anish's general Cursor skill. Precedent: DEPTH-13 + Batch E (`build.sh:20972-21004`). The global source was NOT edited.
- **D-A3:** DEPTH-03's new text is IDENTICAL to DEPTH-02's (per the spec).
- **D-A4:** L17-06 is a staged direct edit (per the spec's ordering note); it carries no new `_F22` token (its text only adds "a Casberry particle export" to L15-08's list).
- **D-A5 (ORB-PP1 anchor correction):** ORB-PP1's anchor carried a spurious 2-space indent on its first line ("  Colors: ..." — the file's line is "  decision record; Colors: ..."). Corrected to DEPTH-08's anchor (same two lines, no leading indent). The §14 agent's count==1 claim for that anchor was wrong; the applier's validation caught it.
- **verify21 question — RESOLVED:** verify21 = 96/102. The 6 FAILs are exactly the frozen post-fix21 build.sh fingerprint + 5 cascade lines. Each prior verifier was run directly: each fails ONLY on its own frozen fingerprint check. So verify21 passes on substance; the 6 fails are fingerprint/cascade artifacts of the legitimate build.sh change, not real regressions. verify22 §22 encodes this allowance. **Counts after §13–§17 (changed from the Audit #67 baseline):** fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76, fix20 164/169 (fix15/17/19 each lost one more check — the less-flat-ui diff check, "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks" — because the diff is now **6 hunks, not 4**: the 4 Batch E hunks intact + 2 fix22 runtime hunks, DEPTH-13 and L15-06. That is the EXPECTED consequence of the correct D-A2 scoping decision (plugin-scoped notes must not leak into the shared global Cursor skill), not a regression. verify22 §22 `_allowed_fail` allows that exact check line too, with the 4→6 reason recorded. The prior verifiers themselves were NOT edited.
- **§13 Depth-hits check — CONFIRMED, no existing depth rule:** "Depth" case-sensitive in build.sh = 3 lines, all redesign-depth levels; 24 lowercase hits, none a design-axis rule; built-tree mentions are a principle (A11), a shadow note, and a redesign note. §13 is genuinely new.
- **§14 state list — VERIFIED LIVE (9 states, no "thinking"):** working, searching, solving, listening, connecting, weaving, composing, breathing, shaping. The phantom tenth comes from the breathing state's aria-label "Thinking…".
- **Glossary home justification:** Group G terms live in the Taste glossary (`skills/design-taste-frontend/references/design-glossary.md`, `GLOSSARY_F22`) because Taste is the skill that defines the design vocabulary for the whole package; owning skills point at it (G-P1/P-G2/P-G3) and never restate definitions.

## 6. Weaving-coherence + /demo gates

- Weaving-coherence pass (sweep #30c, final): every §1–§17 item reachable from the design-package flow at its SPEC'd placement, pointers resolve, not duplicated elsewhere. Result: {RESULTS["weaving"]} (see `fix22/sweep30c-report.md`, per-section table with current line numbers).
- /demo (a) callable: {RESULTS["demo_callable"]} — the /demo command exists, is wired, invokes pitch-deck-video; the dry-run fixture exercises invoking /demo on a sample app and shows it reaches the filming pipeline (shots.json → Remotion → film → narrate). Live-vs-not-executed, stated explicitly: the dry-run re-re-run served the sample app (200s), ran `npm install` (exit 0) and `tts.mjs` (exit 0, estimated durations), and proved the Remotion `-p` invocation resolves live and the render bundles and begins — but NO live film/render/stills were produced in this environment (no Playwright browser binary; `record.mjs` fails at `chromium.launch()`; Playwright's CDN closes at ~90%). No film is claimed on wiring alone.
- /demo (b) never automatic: {RESULTS["demo_not_auto"]} — grep-verified + full-context reads (sweep #30c, Audit #69): no orchestrate step, hook, post-build trigger, finish-report step, or other command invokes /demo or pitch-deck-video automatically. **The removal, and the behavior change (recorded here as required):** Audit #68 confirmed /demo WAS auto-invoked at 6 sites — orchestrate step 5d (B-1), orch-build-mvp skill+command step 8 (B-2), orch-change-feature skill+command step 5 (B-3), hackathon-mode §7 "filmed by default… required deliverable", commands/demo.md dispatch note, orchestrate/references/dispatch-prompt.md Environment field. ALL were removed (17 staged edits + 14 runtime patches via `fix22/demogate-apply.py`, + follow-ups O-9/H-2/H-3/B2S6/B2S7 and the §7 narration-key conditional H-4a/b; 20 DEMOGATE tokens, each exactly once). The standing first-build contract CHANGES: from deploy → demo video → commit → README (demo a required deliverable, filmed by default) to **deploy → commit → README, demo no longer a required deliverable** — /demo runs ONLY when the user invokes it explicitly (or the request explicitly asks for a demo video). The B-3 decision: the orch-change-feature re-film was REMOVED, not carved out as an exception (the parent's rule is absolute); the removal's done-condition for the video is now "the demo video reflects the removal, or is flagged as stale" (re-film with `/demo --rebuild` on request). The parent spot-checks this before anything is reported to Anish. **Applier bug found and fixed during the removal (recorded):** `demogate-apply.py` read `olines` (orchestrate) during validation, then the O-4 full-line step wrote that PRE-edit snapshot back, clobbering the other 12 orchestrate staged edits (O-1, O-2a–d, O-3, O-5, O-6, O-7a/b, O-8a/b) — only O-4 itself survived. The coordinator caught it by grepping the built tree, re-applied the 12 edits via `fix22/demogate-fix-o.py`, and then found three more stale sequence mentions the first pass missed (orchestrate step 6 Order sentence + README video-path input, hackathon-mode :12 sequence + :61 timing, orch-build-mvp step 9 timing) and fixed them (O-9/H-2/H-3/B2S6) plus the §7 paragraph (H-4a/b) and the orch-build-mvp :32 paragraph (B2S7). The final Audit #69 (ZERO) and sweep #30c (CLEAN) verified the removal on the final build.
- /demo (c) contract intact: {RESULTS["demo_contract"]} — §12 port did not change /demo's contract: still films the REAL app locally, F1 feature coverage, F2 stack labels, F3 Edge at position 3, F4 theme pull + gorgeousness checks, F5 blocking A/V table + 10s mix listen, F6 measured runtime under 2:10 / max 2:30, voice rules, $10 budget cap, local-only filming. The §15 liquid-logo brand-mark step produces the animated mark ONCE, outside the video pipeline (never a runtime import). **Remotion invocation fix (recorded, two rounds):** dry-run #37 found `template/scripts/qa.mjs:42` calling `npx remotion@4.0.542 still` — the `remotion` package carries NO executable bin (verified: installed `node_modules/remotion/package.json` bin is null; the CLI lives in `@remotion/cli`) and 4.0.542 was unpinned vs the template's 4.0.526 pin; `build.mjs:335` had the same broken render call. First fix (`npx @remotion/cli@4.0.526`) was text-correct but STILL failed live: `@remotion/cli` carries THREE bins (remotion/remotionb/remotiond), so bare `npx <package>` cannot determine the executable ("could not determine executable to run", verified live twice). Final fix (proven live): `npx -p @remotion/cli@4.0.526 remotion <cmd>` at both call sites — `remotion --help`, `render --help`, and the local bin all exit 0; `qa.mjs`'s `-p` invocation resolves past npx, Remotion auto-downloads its headless shell, bundles the composition, and begins rendering. **The one check not met in this environment (recorded honestly, not claimed):** `node scripts/qa.mjs` still exits 1 — NOT on the invocation, but on the template's runtime Google Fonts fetch: `src/fonts.ts` loads Hanken Grotesk / Instrument Serif / JetBrains Mono via `@remotion/google-fonts`, and Chrome in this sandbox cannot reach `fonts.gstatic.com` (`ERR_SSL_PROTOCOL_ERROR` / `net_error -107`; the same URL returns 200 via `curl`; a direct headless-Chrome fetch hung >2 min; a proxy-wrapper probe failed identically — Chrome egress is blocked here while Node/npm egress works). So the literal key check "`qa.mjs` exits 0" is NOT proven in this environment and is OWED to the live smoke test on a normal network. **Observation carried (not a verdict driver):** the template fetches its fonts live at render time, while the plugin's standing font rule (fix #19/#21) is self-hosted static fonts — a render depending on a live Google Fonts fetch fails in any restricted network. Whether the template should self-host its fonts (or the skill should record the network requirement) is the parent's call.

## 7. How to re-verify

- `cd ~/workspace/hackathon-plugin && python3 fix22/verify22.py` (must print 100% + exit 0; it also runs verify15/17/18/19/20/21 with the fingerprint allowance).
- `grep -riE "claude|codex|anthropic|opus|sonnet|haiku|composer-2.5" hackathon-ecc/skills hackathon-ecc/agents hackathon-ecc/commands hackathon-ecc/rules hackathon-ecc/hooks --exclude-dir=node_modules` (must be empty).
- `bash build.sh` (exit 0) then re-check `md5sum build.sh` / `wc -l build.sh` against the Results above.
- Patch specs: `fix22/depth-patches.md`, `fix22/orbs-patches.md`, `fix22/libraries15-patches.md`, `fix22/vercel-patches.md` (+ `fix22/vercel-dedupe.md`), `fix22/libraries17-patches.md`. Applier: `fix22/apply22.py` (re-runnable dry-run: `python3 fix22/apply22.py`; the staged files + fix22.py are already applied — do NOT re-run `--apply` blindly). Demogate applier + follow-up fix scripts: `fix22/demogate-apply.py` (17 staged edits + 14 runtime patches; contains the O-4 clobber bug documented in §6 — do NOT re-run `--apply`), `fix22/demogate-fix-o.py` (re-applied the 12 clobbered orchestrate edits), `fix22/demogate-fix-o2.py` (O-9/H-2/H-3), `fix22/demogate-add-b2s6.py` + `fix22/demogate-add-b2s7.py` (runtime patches), `fix22/demogate-fix-o3.py` (M-1/H-4a/b/REMO-2a/b).
- Reports (final round): `fix22/sweep30c-report.md` (CLEAN), `fix22/audit69-report.md` (ZERO), `fix22/dryrun37-rerun2-report.md` (+ `fix22/dryrun37-rerun2/`, 42/42 fixtures + 58/59 demo checks, 1 environmental FAIL). Earlier rounds: `fix22/sweep30b-report.md` + `fix22/sweep30b-rerun-report.md`, `fix22/audit68-report.md` + `fix22/audit68-rerun-report.md`, `fix22/dryrun37-report.md` (+ `fix22/dryrun37/`) + `fix22/dryrun37-rerun-report.md` (+ `fix22/dryrun37-rerun/`).

## 8. Carried forward

- Parent spot-check still owed before reporting the close to Anish.
- No bundle, commit, or push made (b2444de predates fixes #14–#21 — do NOT push it; a fresh bundle is needed before any push).
- Queued after the fix #22 close + spot-check: make a render of Home Run following the design skill (Anish, Nov 12, 18:54).
- OWED to the live smoke test (Anish's Cursor, the standing gate before GitHub publish): full live `qa.mjs` exit-0 on a normal network (the `-p` invocation is proven to resolve + bundle + begin rendering in this sandbox; the exit-0 itself is blocked here only by Chrome's lack of egress to fonts.gstatic.com) AND a live film (no Playwright browser binary in this sandbox; `record.mjs` fails at `chromium.launch()`).
- Open adjudications for the parent (see §4): B3/B15/B4 token conflicts; §13 depth token values + "six dimensions" staleness; §14 orbs gravity verification; §16 AG19 APCA vs WCAG 4.5:1; §17 Casberry harder line (bar exports until terms confirmed); template live-Google-Fonts dependency vs the self-hosted-fonts rule (self-host the template fonts, or record the network requirement?).
"""

out = BODY
open(os.path.join(FIX22, "MANIFEST.md"), "w", encoding="utf-8").write(out)
print("MANIFEST.md written.")
print("Disposition table rows embedded:", len(rows))
