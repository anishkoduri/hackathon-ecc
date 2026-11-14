# Sweep #30b — fix #22 confirmation sweep (hackathon-ecc)

**Verdict: SWEEP #30b: FINDINGS — 1 blocking-class + 1 minor.** The weaving-coherence
pass is CLEAN (every §1–§17 item is reachable from the design-package flow at its
SPEC'd placement), all 38 anchor tokens resolve, verify22 re-run by this sweep is
**368/368, exit 0**, and the Sweep #30 findings are both fixed. The two findings are:
**(1)** /demo is auto-invoked by the autonomous first-build pipeline at four sites,
against Anish's Nov 12 18:52 "callable on demand and NEVER run automatically"
instruction and the addendum §3(b) blocking rule (the addendum's own preliminary
note already flagged this; this sweep confirms it with full-context reads — Audit #68
must confirm and the coordinator/parent must decide the removal); **(2)** the §16
files cite the plugin hit-area rule with the superseded "40x40px, ideally 44x44px"
wording in three places, while the live rule is 44x44px minimum.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/` (`node_modules/`
excluded everywhere), `build.sh`, staged sources (`new-skills/`, `round2-skills/`),
and the fix22 working files. SPEC read first (`fix22/SPEC.md` §§1–17). Method: the
Sweep #30 report followed for format and bar, extended with the parent's §30b
checklist (full anchor re-derivation with occurrence counts, disposition re-check
against the current tree, less-flat-ui diff, token-sharing adjudication, the
mandatory weaving-coherence pass, the §13 D19-extension form, the Vercel live-fetch
absence, and the /demo callable/never-automatic gates). Every number below was
re-derived by running the greps/commands shown; nothing was copied from Audit #67,
Dry-run #36/#37, or the coordinator's reports without re-running. This sweep made
no plugin change (read-only); its only write is this report. No `bash build.sh` run,
no bundle/commit/push, no message sent.

**Given state (measured by this sweep):** `build.sh` **23,758 lines, md5
`306dd648ab9dc4bee0e019a896e26f64`**; pre-fix22 baseline `build.sh.before-fix22`
23,647 lines, md5 `8dfacb47a2a6698d47e4b4a5f8d9126c` — diff **+111/−0, exactly 2
hunks** (see §4). Counts 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks;
64 trigger keys, all resolving. `fix22/verify22.py` re-run by this sweep: **368/368,
exit 0**.

---

## Findings

### Finding 1 (blocking-class, per addendum §3b) — /demo IS auto-invoked by the autonomous first-build pipeline

Anish's instruction (Nov 12, ~18:52 CST, recorded in `fix22/parent-addendum-nov12.md`
§3): "/demo must be callable on demand and NEVER run automatically." The addendum's
rule (b) is explicit: "no orchestrate step, no hook, no post-build trigger, no
finish-report step, and no other command invokes /demo or pitch-deck-video
automatically. It runs ONLY when the user invokes /demo explicitly. Any
auto-invocation found is a BLOCKING audit finding — remove it, re-run the sweep
and the audit." The addendum §5 already recorded this as PRELIMINARY ("needs Audit
#68 confirmation"); this sweep did the full-context reads and confirms it. Four
auto-invocation sites in the built tree:

| Site | Text (built tree) |
|---|---|
| `hackathon-ecc/skills/orchestrate/SKILL.md:80` | Step 5d: "**5d. Demo** — `/demo` (`pitch-deck-video`). `/demo` films the LOCAL app from the project dir only…" — step 5 is "Verify → polish → deploy → demo, in that order" inside the autonomous first build (step 6 notes "Gate 2 auto-approves in a first build"). |
| `hackathon-ecc/skills/orch-build-mvp/SKILL.md:83` | Step 8: "**Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.**" |
| `hackathon-ecc/commands/orch-build-mvp.md:36` | Step 8: "Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — the demo video is a required deliverable…" |
| `hackathon-ecc/rules/hackathon-mode.mdc:68` | "The first build films `/demo` (`pitch-deck-video`) after deploy: the demo video is a required deliverable, filmed by default (film the real app) — then the README is written…" |

Checked and cleared (mentions, not invocations): `hackathon-ecc/skills/hackathon-pitch/SKILL.md`
(pitch storyboard, not the video pipeline), `deploy-fast/SKILL.md:21` (live-demo vs
filmed-video distinction), `orch-change-feature/SKILL.md:54` (`/demo` vs
`/demo --rebuild` semantics), `manifests/context-packs/skill-triggers@1.json` and
`manifests/install-modules.json` (registry mentions). Hooks: **0** "demo" hits in
`hackathon-ecc/hooks/` (`.json` + all `.js`). Callable (a) is confirmed:
`hackathon-ecc/commands/demo.md` exists, frontmatter "Generate a narrated product
demo video, under 2:10… Use when the user wants a demo video…", args `/demo`,
`/demo <path>`, `--rebuild/--script/--render/--montage/--explainer`; Dry-run #37's
/demo output records 35/35 contract checks met (see §10). Contract (c) is therefore
not in dispute — only (b).

**What it should be / fix options (coordinator + Audit #68 + parent's call):** remove
the four auto-invocations so /demo runs only on explicit user invocation, re-run
sweep + audit — OR the parent adjudicates that the standing first-build contract
(deploy → demo → commit → README, demo as a required deliverable of a user-requested
first build) stands and amends the "never automatic" rule. Either way the
`fix22/MANIFEST.md` MUST record the decision explicitly, including the behavior
change if the steps are removed (addendum §5 tension note). This sweep does not
remove anything (read-only).

### Finding 2 (minor) — §16 files cite the plugin hit-area rule with superseded wording

The live plugin hit-area rule is **44x44px minimum**: `skills/make-interfaces-feel-better/SKILL.md:149`
("Interactive controls must have at least a 44x44px hit area (the plugin floor…)"),
`skills/motion-foundations/SKILL.md:322` (same), glossary G8
(`skills/design-taste-frontend/references/design-glossary.md:27`, "44x44px minimum
on the plugin's craft floor"). The string "40x40px" occurs nowhere else in the
built tree. But three §16 locations cite the rule as "(40x40px, ideally 44x44px —
Group A A14 / G8)" — the pre-fix22 wording (SPEC §2 quotes the old rule that way):

| Location | Text |
|---|---|
| `hackathon-ecc/skills/polish-pass/reference/vercel-checklist.md:175–176` | V-FO6: "Covered in part by: plugin hit-area rule (40x40px, ideally 44x44px — Group A A14 / G8)." |
| `fix22/vercel-dedupe.md:67` | V-FO6 row: "Plugin hit-area rule already exists (40x40px, ideally 44x44px — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp)…" |
| `fix22/vercel-dedupe.md:244` | AG1 row: "already-covered — plugin rule is stricter (40x40px, ideally 44x44px — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp)." |

The dedupe's own quick-reference citation (44x44pt / 48x48dp) is correct, so the
error is confined to the parenthetical restatement of the plugin rule. **Fix:** change
the three parentheticals to the live rule ("44x44px minimum (the plugin floor) —
Group A A14 / G8"). No plugin rule text changes; the checklist/dedupe citations do.
Same defect class as Sweep #30 Finding 2 (stale wording in a fix22 document).

---

## 1. Sweep #30 findings — both verified FIXED

| Sweep #30 finding | Re-check by this sweep |
|---|---|
| Finding 1 — `ANIM_TOKENS_F22` / `ANIM_RULES_F22` / `ANIM_ADV_F22` never inserted (0 hits in built tree and build.sh) | **FIXED.** Inserted as group-anchor labels via AB-03g/AB-05g/AB-09g: `build.sh:23707–23709` (the three tuples, in the fix22 block); built tree 1× each in its home file — `ANIM_TOKENS_F22` in `skills/motion-foundations/SKILL.md`, `ANIM_RULES_F22` in `skills/motion-patterns/SKILL.md`, `ANIM_ADV_F22` in `skills/motion-advanced/SKILL.md` (see §2). `fix22.py:67–69,709–717,1875–1883` records the repair; verify22 §ANIM checks pass (368/368). |
| Finding 2 — SPEC §6.1 said "all 142 items" | **FIXED.** `fix22/SPEC.md:255` (§6.1) now reads "all 144 items accounted for". The other "142" occurrences are accurate: `SPEC.md:5` (reel inventory, 142 items total), `:275` ("Item count is now 144 (142 + 2)"), `:284` ("covers 144 items (142 + H1 + H2)"). |

## 2. Anchor table — all 38 tokens resolve (occurrence counts)

Counts are substring occurrences in the built tree (excl. `node_modules`) and in
`build.sh`. "Home" = the file carrying the rule text; other files are pointers /
cross-references, the established pattern. Zero-token rows: none.

| Anchor | Built occ. (files) | build.sh occ. | Home |
|---|---:|---:|---|
| `PRINCIPLES_F22` | 5 (5) | 3 | motion-foundations Principles ×1 |
| `LAWS_F22` | 4 (4) | 3 | motion-foundations Decision Guidance laws ×1 |
| `ANIM_TOKENS_F22` | 1 (1) | 1 | motion-foundations (AB-03g group label) |
| `ANIM_RULES_F22` | 1 (1) | 1 | motion-patterns (AB-05g group label) |
| `ANIM_ADV_F22` | 1 (1) | 1 | motion-advanced (AB-09g group label) |
| `SLOP_F22` | 28 (11) | 12 | slop-checklist anchor `:1–3`, 20 indicators |
| `UNSLOP_F22` | 16 (8) | 10 | unslop-fixes anchor `:1–3`, 20 fixes |
| `TRENDS_F22` | 53 (16) | 0 | Taste SKILL.md ×23 (20 entries + intro ×2 + finish-gate pointer); 15 Hallmark theme files ×30 (Blueprint carries E3+E17, ×4) |
| `GLOSSARY_F22` | 5 (5) | 3 | design-glossary.md ×1, 20 terms |
| `ACCENT_F22` | 11 (6) | 2 | ui-ux-pro-max H1 + sprawl check |
| `ACCENTUATION_F22` | 6 (5) | 1 | orchestrate design-package step + hierarchy rules/check |
| `MOBBIN_RESEARCH_F22` | 1 (1) | 0 | orchestrate `:64` (mega-line) |
| `MOBBIN_PATTERN_F22` | 2 (2) | 1 | Taste `:445`, ui-ux-pro-max `:167` |
| `MOBBIN_QA_F22` | 1 (1) | 0 | polish-pass `:104` |
| `DIRECTIVES_F22` | 8 (7) | 4 | All 8 required locations (§10) |
| `LENIS_F22` | 4 (3) | 4 | motion-foundations `:178` |
| `GSAP_F22` | 2 (1) | 2 | ui-ux-pro-max `:274–285` |
| `SCROLLTRIGGER_F22` | 4 (3) | 4 | motion-patterns `:429` |
| `VANTA_F22` | 10 (3) | 5 | Taste `:127` (+ pointers) |
| `REACTBITS_F22` | 5 (2) | 5 | motion-patterns `:552` |
| `BANG_ANTISLIDE_F22` | 1 (1) | 0 | pitch-deck-video `:247` |
| `BANG_ONEWORLD_F22` | 1 (1) | 0 | pitch-deck-video `:281` |
| `BANG_STYLES_F22` | 1 (1) | 0 | pitch-deck-video `:304` |
| `BANG_OPENERS_F22` | 1 (1) | 0 | pitch-deck-video `:337` |
| `BANG_KINETIC_F22` | 1 (1) | 0 | pitch-deck-video `:373` |
| `BANG_EXPLAINER_F22` | 1 (1) | 0 | pitch-deck-video `:409` |
| `DEPTH_F22` | 35 (8) | 14 | orchestrate design-package + extension lines |
| `ORBS_F22` | 24 (6) | 12 | motion-patterns orb pattern + tokens + checks |
| `R3F_F22` | 11 (5) | 7 | Taste `:135` / motion-foundations / motion-patterns |
| `LIQGLASS_F22` | 6 (4) | 2 | less-flat-ui liquid-glass block + Taste `:136` |
| `SHADERGRAD_F22` | 7 (3) | 3 | Taste `:134`, ui-ux-pro-max `:447` |
| `LIQLOGO_F22` | 6 (3) | 4 | Taste step 4a `:435` (label home) — see §9 |
| `WEBGL_ONE_F22` | 9 (6) | 5 | one-WebGL-per-surface rule, all homes |
| `VERCEL_F22` | 8 (4) | 6 | vercel-checklist.md `:1–3` (label home) — see §9 |
| `CASBERRY_F22` | 5 (5) | 3 | motion-foundations `:90` + Taste `:138` |
| `ORIGINKIT_F22` | 3 (3) | 2 | Taste `:139`, motion-patterns, ui-ux-pro-max |
| `DAISYUI_F22` | 3 (3) | 2 | design-system `:35`, Taste, ui-ux-pro-max |

Notes: 0 in build.sh for `TRENDS_F22`, `MOBBIN_RESEARCH_F22`, `MOBBIN_QA_F22`,
and all six `BANG_*` tokens is expected — those texts live in staged sources,
installed by build.sh's install steps, not in the fix22 patch block. No duplicate
anchor definitions: each home file carries its anchor ×1 (PRINCIPLES, LAWS,
GLOSSARY, ANIM_* ×1 in home files); multi-file counts are the intended pointers.
Counts grew vs Sweep #30 exactly where §§13–17 added pointers (SLOP 22→28,
VANTA 5→10, DEPTH/ORBS/R3F/LIQGLASS/SHADERGRAD/LIQLOGO/WEBGL/VERCEL/CASBERRY/
ORIGINKIT/DAISYUI all new) — no token lost, none orphaned.

## 3. SPEC lines + library total — PASS

- SPEC §6.1: "all 144 items accounted for" (`SPEC.md:255`) — Finding 2 of Sweep #30 fixed (§1).
- §8: "Item count is now 144 (142 + 2)" (`:275`); "Disposition table covers 144 items
  (142 + H1 + H2)" (`:284`). §9/§10/§11/§12/§13/§14/§15/§16/§17 each state the
  144-item table stands (process/asset additions, recorded separately).
- Asset libraries/tools running total = **11**: §11's 4 + §15's 4 + §17's 3
  (`SPEC.md:571`: "**Running total of asset libraries/tools in fix #22: §11's 4 +
  §15's 4 + §17's 3 = 11.**"). §15 intermediate total 8 (`:501`) is consistent.
  All 11 named in their target skills with pins/licenses/stack scope (spot-verified
  in §10: Lenis `lenis@1.3.27` MIT; GSAP `gsap@3.15.1` GreenSock Standard "no
  charge", NOT MIT; Vanta `vanta@0.5.24` MIT + `three@0.134.0`; React Bits commit
  `9d9c687d…` MIT + Commons Clause; R3F `@react-three/fiber@9.8.2` (React 19) /
  `@8.18.0` (React 18) MIT; liquid-glass-js commit `78cb6ccb…` MIT, no npm package;
  ShaderGradient `@shadergradient/react@2.4.20` v2 (NOT legacy v1.3.5); liquid-logo
  commit `689bb38a…` PolyForm Shield + `@paper-design/shaders-react` Apache 2.0;
  thinking-orbs `thinking-orbs@0.3.2` MIT; Casberry standalone tool, terms
  unresolved + trust flag + export review; OriginKit 10/day cap + conditional
  licence + Origin UI distinction; daisyUI `daisyui@5.7.50` MIT + Tailwind v4).

## 4. build.sh diff + duplication — PASS

- `diff build.sh.before-fix22 build.sh` = **+111 / −0, exactly 2 hunks**:
  `41a42,46` (5 BANG_PIN lines; `BANG_PIN="c1aa65e921c970d858705fcb4a53a8294d1a4131"`
  at `build.sh:42`) and `23635a23641,23746` (the 106-line fix22 block,
  `build.sh:23641–23746`; header at `:23643`, `print("fix22 upstream block applied")`
  at `:23746`). No other line changed. (Sweep #30's build was +85: the extra 26
  lines since are the AB-03g/05g/09g inserts + the §13–§17 patches.)
- The fix22 block's patch ids (in order): AB-01–AB-14 (incl. AB-03a–f, AB-03g,
  AB-05g, AB-09g), CD-P1–P6, G-P-G1/G-P-G2/G-P-G3, PROC-P1–P5, LIB-01–04,
  LIB-06–08 (LIB-05 was the already-applied staged Vanta edit, not a runtime patch
  — same as Sweep #30 §6), CSV-GSAP, DEPTH-09–13, ORB-MP/ORB-MF/ORB-UIPRO,
  L15-01–04 + L15-06, VERCEL-02–07, L17-01–04. The block contains all 11 §13–17
  anchor tokens (DEPTH/ORBS/R3F/LIQGLASS/SHADERGRAD/LIQLOGO/WEBGL_ONE/VERCEL/
  CASBERRY/ORIGINKIT/DAISYUI). It appears exactly once.
- No duplicated rules: every home anchor is ×1 in its home file (§2); dedupe pairs
  honored — B4 (0.97 press, make-interfaces-feel-better, no duplication),
  A14/G8 (44x44px floor, glossary G8 + A14 naming, one rule), D5 (covered-by-
  architecture, one line), D8 (spacing pointer, not restated), D15 (4.5:1 pointer,
  not restated), G4/G13 (glossary definitions pointing at existing QA flag /
  pro-rules reference), C13 (eyebrow flag + D19 clearance, not a ban). §16 Vercel
  dedupe: 136 rows, 0 unaccounted — see §5.
- No new skill / command / trigger key from fix #22 (counts §7 unchanged).

## 5. Disposition citations + Vercel dedupe — PASS (content), with a record-freshness note

**144-item disposition** (`fix22/disposition-merged.md`): every item is named in its
cited target skill in the current built tree — **144/144 by content** (item id, or
its distinctive name where the entry carries no id, e.g. Group F verification-only
entries and the covered B18). Line-exactness (±3 lines of the cited line) holds for
**83/144**; **61 cited lines drifted** but the content is present at a nearby line
(Taste E1–E20 ×20, less-flat-ui F1–F22 ×22, motion-foundations A12–A20/B1/B2/B3/B5/
B9/B10/B15 ×16, make-interfaces-feel-better B4/B18 ×2, unslop-fixes D20 ×1). The
drift is mechanical: inserts since the Audit #67 build moved lines down (e.g. F8
"Halftone" cited `:220`, now `less-flat-ui/SKILL.md:259`; F14 "Cloud sky" cited
`:310`, now `:349` — both +39 from the LIQGLASS_F22 block insert). The two rows my
first scripted pass flagged as "missing" (F8, F14) are present by name; the flag was
the checker's id-matching, not a plugin gap. **Not a finding:** the task brief states
the disposition's line numbers are as of the Audit #67 build, and its header is
frozen at that build (`build.sh` 23,732 lines, md5 `891fca7b…`). The coordinator's
still-unwritten `fix22/MANIFEST.md` (SPEC §6.8) is where current-build placements
must be recorded — see §11 open items. Process rows (26): all present — Mobbin 4/4,
Directives 8/8, Libraries 4/4 (+ ScrollTrigger), Bang 6/6 (see §2 table).

**Vercel dedupe** (`fix22/vercel-dedupe.md`, 292 lines): header states "136 rows
accounted for, zero unaccounted: 90 `command.md` rules + 14 anti-patterns + 32 rules
found only in the same repo's `AGENTS.md`". Independently re-derived: 154
`|`-starting lines = 18 table header rows + 136 rule rows (two rule rows carry bold
dispositions — V-AP1 "**new**", `:215`, and AG19 "**conflict — parent adjudication**",
`:262`); dispositions already-covered 14, partial 38, new 70, duplicate-of 13,
conflict 1 (AG19) = 136.
§4 totals reconcile exactly: command.md 90 (10 + 29 + 51), anti-patterns 14 (13 +
1), AGENTS.md-only 32 (4 + 9 + 18 + 1). **Zero unaccounted.** The single conflict,
AG19 (APCA vs WCAG 4.5:1), is recorded for parent adjudication (`vercel-dedupe.md:262,280,289`);
V-P6 (font preload) vs self-hosted fonts is recorded as resolved (preload compatible
with self-hosted fonts). One citation inside the dedupe is stale — Finding 2
(V-FO6 `:67`, AG1 `:244`).

## 6. verify22 re-run — 368/368, exit 0 (by this sweep)

```
cd ~/workspace/hackathon-plugin && python3 fix22/verify22.py
→ 368/368 checks pass (exit 0)
```

Including: ANIM group anchors in home files + build.sh (Sweep #30 Finding 1
repair); counts 166/72/123/87/15; trigger keys 64, all resolving; banned terms 0;
fix22 block + BANG_PIN present in build.sh; build.sh lines + md5 measured for the
MANIFEST (23,758 / `306dd648…`); prior verifiers still passing except their stale
post-fix21 build.sh fingerprint (fix15 42/44, fix17 58/60, fix18 69/72, fix19 71/76,
fix20 164/169, fix21 96/102 — the fingerprint + cascade lines only, legitimately
superseded by fix #22). The verifier itself notes `fix22/MANIFEST.md` not yet written.

## 7. Leftovers + standing rules — PASS

| Check | Result |
|---|---|
| Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5, case-insensitive, built tree excl. `node_modules`) | **0** in every file |
| Model pins (`grep -ro`, Audit #67 method) | `grok-4.7-high` **54**, `cursor-grok-4.6-high-fast` **102**, bare `grok-4.6-high-fast` **0** — exactly Audit #67's counts |
| Font rules | F4 tightened scope ("long body and small text only", "(F4 tight)") present in Taste step 4a + orch-build-mvp; F7 (every text element gets an artistic font decision) present in Taste `:441` + orch-build-mvp; static instances only (fix #19 F2 instancing step, Taste `:417`, `:246`) present. Clarification, not a finding: the literal token `F4_TIGHT` exists only in `fix21/SPEC.md` (the fix #21 spec's constant name); the built tree carries the rule as "(F4 tight)" / "F4 tightened" prose. Same for `D19_RULE` — it is a `fix19` Python-module constant, not built-tree text; see §11. |
| Screen-verdicts rule | Intact: slop checklist, unslop fixes, Vercel checklist, and depth check are all STATIC checks / candidate evidence, never verdicts (vercel-checklist.md `:6–9` states it explicitly: "CANDIDATE EVIDENCE for `browser-qa`, NEVER a pass/fail verdict on a rendered screen (fix #13e screen-verdicts rule — `browser-qa` alone issues verdicts on rendered screens)"). |
| No new skill/command/trigger key | Counts §7 unchanged; `ls commands` = 87 |
| Leftovers (word-boundary TODO/FIXME/XXX/HACK in the 19 F22-anchor files) | **0** |
| `LIB-05` in built tree / build.sh | **0** (referenced only as applied in fix22 working files) |
| Stale strings in built tree | "142 items" 0, "23,647" 0, old md5 `8dfacb47` 0, superseded md5 `891fca7b` 0, "ScrollTrigger: 0" 0, "3.12.2" 0, "LIB-05" 0. "40x40px": **1 file** — vercel-checklist.md (Finding 2). "GSAP 3.12.5" ×2, both Bang-reference-only in pitch-deck-video (as specified, §12); "3.12.2" absent from the built tree. |
| `liquid-glass-design` dangling reference | **0** in the built tree (resolved — liquid-glass-js fills the gap per SPEC §15 option (a)). The 4 hits in `build.sh` (`:18731`, `:19412`, `:19449`, `:19458`) are unchanged from `build.sh.before-fix22` (4 hits there too): a governance/regression list noting the skill does not exist, not a live pointer. |

## 8. Counts — PASS

| Inventory | Count | How measured |
|---|---:|---|
| skills | **166** | `ls hackathon-ecc/skills \| wc -l` |
| agents | **72** | `ls hackathon-ecc/agents \| wc -l` |
| rules | **123** | `ls hackathon-ecc/rules \| wc -l` |
| commands | **87** | `ls hackathon-ecc/commands \| wc -l` |
| hooks | **15** | `len(json.load(open('hooks/hooks.json'))['hooks'])` (`ls hooks/` = 17 entries incl. `hooks.json` + 16 `.js` files) |
| trigger keys | **64** | `skill-triggers@1.json`: 64 keys; after stripping the `skill:` prefix every key resolves to a real skill dir (0 unresolvable) |

Unchanged post-fix21, per SPEC §6.6. Less-flat-ui: **23 treatments**
(`skills/less-flat-ui/SKILL.md:103` "## The 23 treatments"; #23 Soft Shadow at
`:568`); L15-06 is a patch label for the liquid-glass note, not a 24th treatment.

## 9. Less-flat-ui diff + token-sharing adjudication — PASS

**Less-flat-ui diff** (global `~/workspace/cursor-skills/less-flat-ui/SKILL.md`,
534 lines, vs built `hackathon-ecc/skills/less-flat-ui/SKILL.md`, 579 lines):
**exactly 6 non-equal hunks** (difflib), as required:

| Hunk | Content |
|---|---|
| 1. replace, global L14 → built L14–15 | Design-decision pointer (weave20 pointer: F2/F3/F4/F5/F6/D19/B1/X1 → Taste step 4a / orchestrate) — Batch E |
| 2. insert, built L35 | "Texture in service of the wow moment, not decoration" — Batch E wow-moment rule |
| 3. replace, global L75 → built L77 | "Record every treatment applied…" (design-tokens record line) — Batch E |
| 4. insert, built L104–105 | "Re-tint every example below to the project's dealt palette…" (re-tint warning) — Batch E |
| 5. insert, built L144–182 (39 lines) | "Liquid glass — real refraction (fix #22 §15, LIQGLASS_F22)…" — fix22 runtime hunk (L15-06). Note: the inserted text carries the anchor `LIQGLASS_F22`, not the literal patch label "L15-06" (0 hits for "L15-06" in the built file) — the label lives in `fix22.py` / the fix22 block, not in the skill text. |
| 6. replace, global L523 → built L566–568 | "**Depth and texture are different axes (fix #22 §13, DEPTH_F22).** This skill owns texture — the 23 treatments. The z-axis is owned by the depth rules…" — fix22 runtime hunk (DEPTH-13) |

The 4 Batch E hunks are intact as specified. No other difference.

**Token-sharing adjudication** (both confirmed as pointer mentions of one anchor
label per home file, not duplicate definitions):

- `LIQLOGO_F22` in `ui-ux-pro-max/SKILL.md`: **4 occurrences** (not 2 as the task
  brief's shorthand said) — `:238` + `:248` (the two §15 placements, L15-03
  wordmark animation + L15-04 app-surface use), `:441` (the §15 four-libraries
  list line), `:457` (pointer: "see `design-taste-frontend` step 4a,
  LIQLOGO_F22"). The anchor LABEL (the standalone-tool definition, pin, licences,
  static-fallback rule, attribution) lives **once**, in Taste step 4a
  (`design-taste-frontend/SKILL.md:435`). The other two files carrying the token
  (`polish-pass/reference/slop-checklist.md` ×1, Taste ×1) are pointers/checks.
  **Adjudication: PASS** — pointer mentions, one label home.
- `VERCEL_F22` in `polish-pass/SKILL.md`: **2 occurrences** (`:98`, `:99`) — both
  are pointers to `reference/vercel-checklist.md` ("Also read the Vercel checklist
  … and apply its fix guidance on every pass" / "Then run the Vercel checklist …
  same standing: candidate evidence for `browser-qa`, never a verdict"). The
  anchor LABEL lives **once**, in `polish-pass/reference/vercel-checklist.md:1–3`
  ("# Vercel checklist — VERCEL_F22" / "**Anchor: `VERCEL_F22`.** … pinned
  snapshot…"). The other files (`motion-foundations` ×1, quick-reference ×3) are
  pointers. **Adjudication: PASS** — pointer mentions, one label home.

## 10. Weaving-coherence pass — CLEAN (per §1–§17)

For every §1–§17 item I verified: (i) it is reachable from the design-package flow
at its SPEC'd placement — orchestrate step 3 design-package-in-every-UI-slice-brief
(`skills/orchestrate/SKILL.md:62`, mega-line) → Taste step 4a / ui-ux-pro-max /
motion-* / less-flat-ui / polish-pass — with its D19 reason and its §10 directive
form intact; (ii) its pointers resolve (bidirectional where the SPEC requires);
(iii) it is not duplicated elsewhere. No item is only appended. Result by section:

| Section | Flow entry point (SPEC'd placement) | Reachability / pointers | Result |
|---|---|---|---|
| §1–§3 A (A1–A20) | orchestrate `:62` "Motion principles in every UI slice brief (PRINCIPLES_F22 / LAWS_F22)" → motion-foundations Principles `:52–90` + Decision Guidance `:217–281` | make-interfaces-feel-better + ui-ux-pro-max point back to the laws; A7→B7, A8→B6, A2→B5/B19 cross-refs present | PASS |
| B (B1–B20) | Same brief line → motion-foundations tokens (`dropdown: 0.2`, `staggerRow: 0.03`, `stretch: 1.12`, `inOut`, `popover: 0.95`, `exitFactor: 0.8`) + motion-patterns Rules 11–19 + motion-advanced Rules 9–11/examples | Group anchors AB-03g/05g/09g resolve (§1); B4/B18 covered-evidence intact; B3/B15/B4 conflict flags carried, not resolved | PASS |
| C (C1–C20) | orchestrate Verify step → polish-pass SKILL.md `:98–99` ("read the slop checklist … on every pass") → slop-checklist anchor `:1–3`, all 20 indicators as flags with D19-reason + theme-fit clearance | Taste finish gate + Impeccable detector context point at the checklist; each fix pairs to unslop-fixes | PASS |
| D (D1–D20) | Same polish-pass step → unslop-fixes anchor `:1–3`, all 20 fixes; CD-P1–P7 pointers in quick-reference + motion-* | D11→H1, D20→A10/B8 family, D5/D8/D15 pointers (not restated) — §4 | PASS |
| E (E1–E20) | Taste step 4a trend menu (`TRENDS_F22` ×23 in Taste) — the design package MAY draw on it; 16 Hallmark Range lines in 15 theme files | E12/E14/E16 menu-only: no theme file carries an eyebrow, sparkle, or three-icon-cards line (the only "eyebrow" hit in the theme dir is `themes/README.md:54`, the validator prohibition itself); E6 points at less-flat-ui #21, no duplication | PASS |
| F (F1–F22) | less-flat-ui catalogue, reached via orchestrate `:62` ("`less-flat-ui` where dull/flat") + Taste step 4a + R3 (≥2 distinct treatment kinds) | Verification-only: no text copied; all 22 + #23 Soft Shadow present (§5) | PASS |
| G (G1–G20) | One glossary file, reached from every owning skill: ui-ux-pro-max `:69`, motion-foundations `:710` (G18), motion-patterns `:999` (G10/G14/G20) — each "Design vocabulary — the definitions … live in `design-glossary.md` (`GLOSSARY_F22`)" | Glossary carries the owning-skill column per term (e.g. G8 → ui-ux-pro-max, 44x44px floor); bidirectional. Note: the disposition's "P-G1/P-G2/P-G3" labels appear in build.sh as patch ids `G-P-G1/2/3`; the built text uses the "Design vocabulary" pointer form. Same pointers, label-form difference only. | PASS |
| H1 | orchestrate `:62` (accent colour via H2 means) → ui-ux-pro-max `:122` concept + slop-checklist `:419` sprawl check; D11 points at it | H1 is the concept, D11 the fix — not duplicated | PASS |
| H2 | orchestrate `:62` "Accent hierarchy in every UI slice brief (ACCENTUATION_F22)" → ui-ux-pro-max `:16` hierarchy rules → slop-checklist `:450` hierarchy check | F5/dealt-moments/H1 recorded as accentuation means under H2, cross-referenced not duplicated | PASS |
| §9 Mobbin | orchestrate `:64` (same mega-line family; `MOBBIN_RESEARCH_F22` at `:64`) category-level research step + record requirement + no-copy boundary + free-tier + never-blocked → Taste `:445` + ui-ux-pro-max `:167` pattern reference → polish-pass `:104` QA convention check | No Mobbin URL as a design source anywhere (grep-verified by the addendum's dry-run fixture 9a, which FAILS a record citing one); recorded-gap fallback for unreachable/paywalled | PASS |
| §10 Directives | orchestrate `:72` "Directives, not descriptions (DIRECTIVES_F22)" in every implementer brief → Taste step 4a (×2) + ui-ux-pro-max `:219` + GAN planner `:46` / generator `:32` / evaluator `:134` + polish-pass `:100` | Every §10 rule carries its D19 parenthetical (orchestrate `:72` ends "(D19 — Motion: …; Theme: …; Texture: …; Visuals: …; Techniques: …; Colors: …)"); prose-only FAILS the handoff check; ambiguity → recorded gap | PASS |
| §11 Libraries | Lenis → motion-foundations `:178` (+ motion-patterns + ui-ux-pro-max); GSAP → ui-ux-pro-max `:274–285` (`--domain gsap`, 17 presets intact) + ScrollTrigger motion-patterns `:429`; Vanta → Taste `:127` (+ ui-ux-pro-max); React Bits → motion-patterns `:552` (React-only) | Pins/licences/scopes in §3; reduced-motion + mobile fallback + scrim stated for Vanta; unpinned "latest" FAILS the pin check | PASS |
| §12 Bang | pitch-deck-video staged source `new-skills/pitch-deck-video/SKILL.md` **identical** to built (830 lines, BANG_* at `:247/:281/:304/:337/:373/:409` in both); /demo command loads the skill | Anti-slide as structural checks; one-world/camera/persistent-subject architecture; 10 style directions + 19 openers as menus (look from brand/theme deal); kinetic type as directives; explainer styles inform How beats. /demo still films the LOCAL app; no second toolchain. Dry-run #37 /demo output: 35/35 contract checks met (F1–F6, voice, $10 cap, local-only, 84.1s runtime, Bang rows in the A/V table). | PASS (contract); (b) never-automatic is Finding 1, not a weaving defect |
| §13 Depth | orchestrate `:66` "Depth strategy in every UI slice brief (DEPTH_F22)" + `:108` "Depth strategy recorded with the direction" → ui-ux-pro-max depth rules → motion-foundations/patterns 3D motion → Taste dealt moments → polish-pass depth check (`:101`, slop-checklist depth section) | Seventh-dimension extension line sits immediately after the frozen D19 line in both homes (§11); `flat by choice — <reason>` satisfies the dimension; depth/texture overlap recorded (less-flat-ui hunk 6) | PASS |
| §14 Orbs | orchestrate `:64` "Waiting states in every UI slice brief (ORBS_F22)" → motion-patterns orb pattern (9 repo-verified states, NO "thinking" state — correction to the SPEC draft recorded in the skill) → motion-foundations tokens (sizes 64/20, monochrome, reduced-motion frozen frame, offscreen/hidden pause, DPR ≤2) → ui-ux-pro-max `:122` component rules → polish-pass check | State-matched, never decorative; generic spinner FAILS; `thinking-orbs@0.3.2` MIT pinned. RareFormLabs note: recorded as unresolved in `fix22/orbs-patches.md:520–525` ("rareformlabs connection unresolved — asset verified independently"); SPEC §14 requires the note in the MANIFEST — still open with the MANIFEST itself (§11). Never invented a link. | PASS |
| §15 Libraries | R3F → Taste `:135` + motion-foundations `:160–161` (pairing rule) + motion-patterns; liquid-glass-js → Taste `:136` + less-flat-ui hunk 5 + ui-ux-pro-max; ShaderGradient → Taste `:134` + ui-ux-pro-max `:447` (v2, NOT legacy v1.3.5); liquid-logo → Taste step 4a `:435` (label home) + ui-ux-pro-max `:238/:248` | One-WebGL-per-surface rule (`WEBGL_ONE_F22`, 9 occ., 6 files) incl. Casberry extension; R3F v8↔React 18 / v9↔React 19 pairing enforced; ShaderGradient customize-URL is the config; liquid-logo standalone tool + static fallback + attribution | PASS |
| §16 Vercel | polish-pass SKILL.md `:98–99` ("read the Vercel checklist … on every pass", candidate evidence only) → vercel-checklist.md (454 lines, pinned commit `4ecfb9fb8d1d3b7009674869b3aaee2f904042e1`, 2026-10-05, ECC pinned-snapshot form, refresh on explicit request only) → pointers in ui-ux-pro-max quick-reference (×3) + motion-foundations `:212` | Dedupe 136/0 (§5); license gap recorded (skill repo NO LICENSE file; rules repo MIT); ECC-source check recorded (vercel-checklist `:20–27`); live-fetch absent (§12). One stale citation — Finding 2. | PASS (modulo Finding 2) |
| §17 Libraries | Casberry → motion-foundations `:90` + Taste `:138` + motion-patterns + ui-ux-pro-max; OriginKit → Taste `:139` + motion-patterns + ui-ux-pro-max; daisyUI → design-system `:35` + Taste + ui-ux-pro-max | Casberry: standalone tool, export reviewed as untrusted code, terms unresolved, one-WebGL rule covers exports; OriginKit: 10/day cap, Pro-marked excluded, Origin UI distinction, env-only key, no MCP wiring; daisyUI: 5.x + Tailwind v4 pinned, default-theme-unexamined FAILS | PASS |

**Weaving-coherence verdict: CLEAN.** No §1–§17 item is only appended; every item
is encountered at its SPEC'd step with its D19 reason and §10 directive form
intact (spot-verified in the §13–§17 rule texts, each carrying a full
"(D19 — Motion: …; Theme: …; Texture: …; Visuals: …; Techniques: …; Colors: …)"
parenthetical), pointers resolve bidirectionally where required, and nothing is
duplicated elsewhere. Dry-run #37's raw outputs corroborate the weaving
(42/42 fixture expectations met, §13–§17 + §8–§12 fixtures; see §10).

## 11. §13 D19-extension form + Vercel live-fetch absence — PASS

**D19 extension form:** the frozen fix #19 D19 rule line is **byte-identical** in
orchestrate and Taste — `orchestrate/SKILL.md:120` == `design-taste-frontend/SKILL.md:423`
(2,090 chars each, verified by exact string comparison). The seventh-dimension
extension line sits **immediately after it in both homes** — `orchestrate:122` ==
Taste `:425` (923 chars each, exact): "**Depth — the seventh dimension (fix #22
§13, DEPTH_F22).** The six dimensions above are unchanged — the fix #19 D19 rule
text is verbatim and stays byte-identical (verify19 asserts it as a substring).
This line EXTENDS it: every UI decision's recorded reason now addresses SEVEN
dimensions…" (ui-ux-pro-max carries the app-surface mirror at `:228`). No "six
dimensions" text was rewritten: the 9 "six dimensions" hits in the built tree are
the two extension lines themselves (which say the six are unchanged), the frozen
D19 lines' own wording, and the frozen fix #19 "## D19 reason … (fix #19 D19 —
six dimensions)" headings in slop-checklist/unslop-fixes/vercel-checklist (the
vercel-checklist one uses the same frozen heading form; the seventh dimension is
recorded by the extension lines and the checklist's depth content, not by editing
the heading). "six dimensions" occurs 4× in `build.sh.before-fix22` — the phrase
pre-dates fix #22. `D19_RULE` as a literal string does not occur in the built tree
because it is the `fix19` Python-module constant name; verify19 asserts the rule
text as a substring, and verify22 reports fix19 at 71/76 (fails only the stale
fingerprint cascade).

**Vercel live-fetch absence:** **0** `raw.githubusercontent.com/vercel-labs` URLs
anywhere in the built tree, and no unpinned Vercel fetch instruction. The only
two `raw.githubusercontent.com` hits in the built tree are pre-existing,
version-pinned install URLs in `skills/codebase-memory/SKILL.md:51,70`
(`DeusData/codebase-memory-mcp/v0.12.1`) — not Vercel, not a guidelines fetch.
The checklist states the hazard explicitly (vercel-checklist `:24–26`: the
unpinned URL "is a flagged prompt-injection hazard and is NEVER the weave") and
records the pinned snapshot + ECC refresh discipline.

## 12. Verifiers / dry-runs observed (not re-run by this sweep, except verify22)

| Check | Result as observed |
|---|---|
| `fix22/verify22.py` (re-run by this sweep) | **368/368, exit 0** (§6) |
| Audit #67 | ZERO ERRORS (report `fix22/audit67-report.md`; build state then 23,732 lines / md5 `891fca7b…` — superseded by the §13–17 + AB-03g rebuild, now 23,758 / `306dd648…`) |
| Dry-run #36 | PASS 46/46 (per Audit #67 / sweep #30; §1–§12 fixtures) |
| Dry-run #37 (raw outputs, `fix22/dryrun37/`) | **42/42 fixture expectations met** (`dryrun37-output.txt`: §13a–g, §14a–e, §15a–i, §16a–e, §17a–f, 8-H1a, 8-H2b, 9a–b, 10a–b, 11a/c, 12a–b) and **35/35 /demo contract checks met** (`dryrun37-demo-output.txt`: pipeline files, local-only, F1–F6, voice, $10 cap, Bang rows). No formal `dryrun37-report.md` exists yet; the "FAIL" strings in the output files are the expected-outcome labels ("expected FLAG/FAIL"), not failures. The demo-sample-video fixture app ships a `node_modules/` tree under `fix22/dryrun37/` (fixture scaffolding, not plugin code). |
| Audit #68 | **Not yet run** — no `fix22/audit68-report.md` exists. It must confirm Finding 1 (addendum §3b) and the /demo gates. |
| `fix22/MANIFEST.md` | **Not yet written** (SPEC §6.8). `fix22/build_manifest.py` exists (a builder script, not the manifest). verify22 notes the absence. Open item, not a finding (same as Sweep #30 §11). |

## 13. Open items (not findings — coordinator / parent steps before the fix closes)

1. **Finding 1** — /demo auto-invocation: coordinator + Audit #68 confirm, then
   remove the four sites or the parent adjudicates the standing first-build
   contract; the MANIFEST must record the decision/behavior change explicitly.
2. **Finding 2** — correct the three stale hit-area parentheticals (vercel-checklist
   `:175–176`; vercel-dedupe `:67`, `:244`) to "44x44px minimum (the plugin floor)".
3. **`fix22/MANIFEST.md` still not written** (SPEC §6.8): disposition as built,
   placement map, adjudication notes (§4a/§4b pairs, B3/B15/B4 token conflicts,
   C13 vs Impeccable eyebrow tension, AG19 APCA vs WCAG 4.5:1), glossary-home
   justification, counts before/after, verifier + audit + dry-run + sweep results,
   the rareformlabs-unresolved note, and the current-build (23,758 / `306dd648…`)
   disposition line numbers superseding the Audit #67-as-of record (§5 note).
4. **Audit #68** not yet run; **dry-run #37** has raw outputs (42/42 + 35/35) but no
   formal report. Both are close criteria per the amended addendum §4, plus
   weaving-coherence CLEAN (this sweep) and the /demo gates.
5. **Parent adjudications still open** (carried as recorded flags, none silently
   resolved): B3 30ms vs Rule 5 0.05s floor; B15 0.8× vs quick-reference ~60–70%;
   B4 0.97 vs `scale.press` 0.95; C13 vs Impeccable eyebrow tension; AG19 APCA vs
   WCAG 4.5:1. No new conflicts found by this sweep.

## Commands used (full list)

```
md5sum build.sh build.sh.before-fix22 ; wc -l build.sh build.sh.before-fix22
python3 fix22/verify22.py
diff build.sh.before-fix22 build.sh
python3 /tmp/sweep30b.py   (anchor line-counts, AB-03g/05g/09g, counts, trigger-key resolution, banned terms, grok pins, font/screen-verdicts greps, Vercel live-fetch, D19_RULE/six-dimensions, token-sharing, SPEC/dedupe lines, less-flat-ui difflib)
python3 /tmp/sweep30b2.py  (anchor occurrence counts, grok occurrence counts, trigger keys stripped, build.sh diff hunks + BANG_PIN, D19 full-line equality, 'six dimensions' in before-fix22, liquid-glass-design, vercel-dedupe row parse, less-flat-ui 6-hunk diff)
python3 /tmp/sweep30b3.py  (grok grep -ro replication, D19 equality, screen-verdicts/font greps, disposition ±3-line check, dedupe pairs, stale strings, leftovers, SPEC '142', /demo greps, rareformlabs, §15/§17 specifics, §16 specifics)
python3 /tmp/sweep30b4.py  (hit-area rule text, V-FO6/AG1 rows, dryrun37 listing, disposition presence check, process rows, orchestrate L62 inventory, step 5d, staged-vs-built pitch-deck-video)
grep -rn (targeted: F8/F14 in less-flat-ui; MOBBIN/ACCENTUATION/DEPTH/ORBS lines in orchestrate; VERCEL_F22 context in polish-pass :98–99; glossary pointers; pitch-deck-video mentions incl. hackathon-mode.mdc:68, orch-build-mvp skill :83 + command :36; hooks demo grep; dry-run #37 outputs)
ls hackathon-ecc/skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l ; python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"
```
