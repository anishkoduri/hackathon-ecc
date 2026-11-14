# Sweep #30 — fix program #22 (hackathon-ecc), built-tree re-verification

**Verdict: SWEEP #30: NOT CLEAN — 2 minor findings, 0 blocking.** Both findings
are consistency defects in fix #22 working documents, not missing rule text:
three anchor tokens named in the patch spec / disposition (`ANIM_TOKENS_F22`,
`ANIM_RULES_F22`, `ANIM_ADV_F22`) never appear in the built tree or build.sh,
and SPEC §6.1 still says the disposition table covers "all 142 items" when it
covers 144. Every fix #22 rule text is present where the merged disposition
claims it; the build.sh diff is exactly the 80-line fix22 block + the 5
BANG_PIN lines; banned-term set is 0 in the built tree; counts are unchanged;
verify22 re-run by this sweep: **291/291 checks pass, exit 0**.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`,
`node_modules/` excluded everywhere; plus `build.sh`, the staged sources
`new-skills/` and `round2-skills/`, and the fix22 working files. SPEC read
first: `~/workspace/hackathon-plugin/fix22/SPEC.md`. Method: the Sweep #29
report (`~/workspace/hackathon-plugin/fix21/sweep29-report.md`) followed for
format and bar — anchor/count identity checks, staged-vs-built diffs,
build.sh hygiene, banned-term grep, leftover-marker grep, counts, verifier
re-run — adapted to fix #22's checklist (anchor orphans, stale counts,
duplication, disposition-citation resolution, process rows, leftovers).
Every number below was re-derived by running the greps/commands shown;
nothing was copied from the fix22 implementation report, Audit #67, or
Dry-run #36 without re-running. This sweep made no plugin change
(read-only); its only write is this report. `fix22/MANIFEST.md` still does
not exist (see §8, open item, not a finding).

**Given state (verified):** `build.sh` 23,732 lines, md5
`891fca7b5f34aa74db95cb04501345a0` (matches the task brief);
`fix22/verify22.py` re-run by this sweep: **291/291, exit 0**. Audit #67:
ZERO ERRORS. Dry-run #36: PASS 46/46.

---

## Findings

### Finding 1 (minor) — Three fix #22 anchor tokens never appear in the built tree or build.sh

`ANIM_TOKENS_F22`, `ANIM_RULES_F22`, `ANIM_ADV_F22` are named as anchor
tokens in the fix #22 working documents but resolve to nothing in the plugin:

| Token | Claimed as anchor in | Built-tree hits | build.sh lines | fix22.py hits |
|---|---|---:|---:|---:|
| `ANIM_TOKENS_F22` | `fix22/ab-patches.md:23`, `:230` (AB-03), `:795–797` (integrator checklist item 1); `fix22/disposition-B.md:10` | **0** | **0** | **0** |
| `ANIM_RULES_F22` | `fix22/ab-patches.md:23–24`, `:323` (AB-04), `:353` (AB-05), `:423` (AB-06), `:474` (AB-07), `:517` (AB-08), `:795–797`; `fix22/disposition-B.md:11` | **0** | **0** | **0** |
| `ANIM_ADV_F22` | `fix22/ab-patches.md:24`, `:544` (AB-09), `:584` (AB-10), `:795–797`; `fix22/disposition-B.md:12` | **0** | **0** | **0** |

The checklist item 1 in `fix22/ab-patches.md:795–797` says: "Rebuild
(`bash build.sh`, exit 0) and confirm the built tree contains every anchor
token: PRINCIPLES_F22, LAWS_F22, ANIM_TOKENS_F22, ANIM_RULES_F22,
ANIM_ADV_F22, ACCENT_F22, ACCENTUATION_F22" — three of the seven listed
tokens fail that check. `fix22/disposition-B.md:10–12` likewise calls them
"Anchor tokens: ANIM_TOKENS_F22 (motion-foundations token values, AB-03),
ANIM_RULES_F22 (motion-patterns rules/examples, AB-04–AB-08), ANIM_ADV_F22
(motion-advanced choreography, AB-09–AB-10)."

**What is present instead (why this is minor, not blocking):** the rule
content the three tokens were meant to anchor IS in the built tree, verified
independently in §3 below — the AB-03 token values (`dropdown: 0.2`,
`staggerRow: 0.03`, `smooth` B1 annotation, `inOut`, `popover: 0.95`,
`stretch: 1.12`, `exitFactor: 0.8`) at
`hackathon-ecc/skills/motion-foundations/SKILL.md:306–333`; the AB-04–AB-08
rules and examples in `motion-patterns/SKILL.md:57–93` and following
examples; the AB-09–AB-10 rules and examples in
`motion-advanced/SKILL.md:61–66` and following examples. The inserted text
carries per-item `(fix #22)` markers and B-numbers, not the group anchor
strings. `fix22/verify22.py` asserts the per-item content, not these three
group tokens, so no verifier depends on them. No other file in the plugin
references these three tokens, so there is no dangling pointer inside the
built tree — the orphan is confined to the two working documents claiming
anchors that do not exist.

**What it should say / fix options (coordinator's call):** either (a) insert
the three anchor strings at their group locations (the AB-03 token group in
motion-foundations, the AB-04–AB-08 rules/examples in motion-patterns, the
AB-09–AB-10 rules/examples in motion-advanced) so the checklist's "built
tree contains every anchor token" holds literally; or (b) correct
`fix22/ab-patches.md` (§ header, AB-03–AB-10 headings, checklist item 1)
and `fix22/disposition-B.md:10–12` to demote the three names from "anchor
tokens" to patch-group labels. Option (b) needs no rebuild; option (a) needs
a rebuild + verifier re-run.

### Finding 2 (minor) — SPEC §6.1 still says the disposition table covers "all 142 items"

`fix22/SPEC.md:255` (§6.1): "Disposition table (in fix22/MANIFEST.md): all
142 items accounted for". The table covers **144** items (142 reels + H1 +
H2) — `fix22/disposition-merged.md` header ("Merged disposition (144
items)") and 144 rows verified in §3, and SPEC §8 itself ("Disposition
table covers 144 items (142 + H1 + H2)"). §6.1 was never updated when §8
added H1/H2. The live record (`disposition-merged.md`) is correct; only the
§6.1 sentence is stale.

**What it should say:** "all 144 items accounted for" (or "all 142 reel
items + H1 + H2"). One-line doc correction in the parent SPEC; no plugin
change. Related lines checked and cleared, not findings: `SPEC.md:5` ("142
items total") is the reel inventory itself and is accurate for the reels;
`SPEC.md:178` ("Group F, all 22 (+ #23 Soft Shadow)") is accurate;
`build.sh:23643` and `fix22/fix22.py:2,1120` ("(142 items) + H1/H2
accents + …") enumerate components, so the total is implied 144, not
claimed as 142.

---

## 1. Anchor tokens — 23 of 26 resolve; 3 orphaned (Finding 1) — otherwise PASS

Occurrences in the built tree (`hackathon-ecc/`, excl. `node_modules`) and
in `build.sh`. "Home" = the file carrying the rule text; other files are
pointers/cross-references, which is the established pattern.

| Anchor | Built-tree hits (files) | build.sh lines | Home rule text present |
|---|---:|---:|---|
| `PRINCIPLES_F22` | 4 (4) | 3 | Yes — motion-foundations Principles, ×1 in home file |
| `LAWS_F22` | 4 (4) | 3 | Yes — motion-foundations Decision Guidance laws, ×1 in home file |
| `ANIM_TOKENS_F22` | **0** | **0** | **No — Finding 1** (content present, token absent) |
| `ANIM_RULES_F22` | **0** | **0** | **No — Finding 1** (content present, token absent) |
| `ANIM_ADV_F22` | **0** | **0** | **No — Finding 1** (content present, token absent) |
| `SLOP_F22` | 22 (10) | 8 | Yes — slop checklist, 3 occurrences in home file |
| `UNSLOP_F22` | 16 (8) | 8 | Yes — unslop fixes, 2 occurrences in home file |
| `TRENDS_F22` | 38 (16) | 0 | Yes — Taste SKILL.md 23 occurrences (20 entries + intro ×2 + finish-gate pointer), 16 Hallmark Range lines in 15 theme files |
| `GLOSSARY_F22` | 4 (4) | 3 | Yes — glossary, ×1 in home file |
| `ACCENT_F22` | 11 (6) | 2 | Yes — ui-ux-pro-max H1 + sprawl check |
| `ACCENTUATION_F22` | 6 (5) | 1 | Yes — orchestrate design-package step + hierarchy rules/check |
| `MOBBIN_RESEARCH_F22` | 1 (1) | 0 | Yes — orchestrate `:62` |
| `MOBBIN_PATTERN_F22` | 2 (2) | 1 | Yes — Taste `:445`, ui-ux-pro-max `:167` |
| `MOBBIN_QA_F22` | 1 (1) | 0 | Yes — polish-pass `:104` |
| `DIRECTIVES_F22` | 8 (7) | 4 | Yes — all 8 required locations (§3 process rows) |
| `LENIS_F22` | 4 (3) | 3 | Yes — motion-foundations `:178` |
| `GSAP_F22` | 2 (1) | 2 | Yes — ui-ux-pro-max `:274–285` |
| `SCROLLTRIGGER_F22` | 4 (3) | 3 | Yes — motion-patterns `:429` |
| `VANTA_F22` | 5 (2) | 2 | Yes — Taste `:127` |
| `REACTBITS_F22` | 5 (2) | 3 | Yes — motion-patterns `:552` |
| `BANG_ANTISLIDE_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:247` |
| `BANG_ONEWORLD_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:281` |
| `BANG_STYLES_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:304` |
| `BANG_OPENERS_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:337` |
| `BANG_KINETIC_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:373` |
| `BANG_EXPLAINER_F22` | 1 (1) | 0 | Yes — pitch-deck-video `:409` |

Notes: 0 lines in build.sh for `TRENDS_F22`, `MOBBIN_RESEARCH_F22`,
`MOBBIN_QA_F22`, and all six `BANG_*` tokens is expected — those texts live
in staged sources (orchestrate, design-taste-frontend, polish-pass,
pitch-deck-video), installed by build.sh's install steps, not in the fix22
patch block. The fix22 block in build.sh is the patch half only (motion-*,
make-interfaces-feel-better, ui-ux-pro-max, GAN agents, ui-ux-pro-max data
files), per the block header at `build.sh:23643–23650`. No duplicate anchor
definitions: each home file carries its anchor ×1 (PRINCIPLES ×1, LAWS ×1,
GLOSSARY ×1 in home files); multi-file counts are the intended pointers.

## 2. Stale counts — PASS (with Finding 2 in SPEC §6.1)

| Stale string | Built tree | build.sh | Disposition |
|---|---:|---:|---|
| "142 items" | **0** | 1 line (`:23643`, block header — component list, cleared, see Finding 2 notes) | 0 in disposition-merged |
| "22 treatments" | **0** | 0 | — |
| "23,647" (pre-fix22 line count) | **0** | 0 | — |
| Old md5 `8dfacb47…` | **0** | 0 | — |
| "ScrollTrigger: 0" | **0** | — | — |
| "40x40px" | **0** | 1 line (`:22082`, old side of a pre-fix22 W2-C4 replace tuple — build machinery, not live text; see below) | — |
| "3.12.2" (stale GSAP pin) | **0** | 1 line (`:23706`, old side of the fix22 CSV-GSAP replace tuple — the match string, not a pin claim; built `threejs.csv` row 35 is `gsap/3.15.1`) | — |
| "GSAP 3.12.5" | **2**, both Bang-reference-only in `skills/pitch-deck-video/SKILL.md:219, :245`, each next to the plugin pin 3.15.1 | — | As specified (§12) |
| "LIB-05" | **0** | 0 | — |

Checked-and-cleared in fix22 working files (all explicitly framed as
pre-fix22 baseline / history / verification, not current state):
"23,647" / old md5 in `PARENT-GUIDANCE.md:8` (starting state),
`disposition-E.md:10,124`, `libraries-report.md:72,209`,
`verify22.py:55,574,595,599` (baseline + allowed fingerprint exception);
"3.12.2" in `libraries-report.md:180,183` (the stale pin, described as
fixed), `fix22.py:21,1003,1101` (CSV_GSAP_OLD match string),
`verify22.py:497–504` (assertion it is absent from the built tree);
"40x40px" in `SPEC.md:179,193,242` (baseline description of the old rule),
`disposition-A.md:26` (quotes the old rule as pre-existing state),
`fix22.py:72` (glossary-fix note), `verify22.py:28,331–332` (assertion it
is gone from the glossary); "22 treatments" in `SPEC.md:178` and
`f-report.md:7` (both "22 + #23 Soft Shadow", accurate); "142 items" in
`SPEC.md:5` (reel inventory, accurate), `PARENT-GUIDANCE.md:4` (reel
inventory), `fix22.py:2,1120` (component list with "+ H1/H2", accurate).
Less-flat-ui states its count correctly in the built tree:
`skills/less-flat-ui/SKILL.md:103` ("## The 23 treatments") and `:8`
(source note: 22 reel backgrounds + Soft Shadow).

## 3. Disposition citations + process rows — PASS (142/142 items, 26/26 process)

Script-checked every `file:line` citation in
`fix22/disposition-merged.md`: for each row, the cited line ±3 lines in the
rebuilt tree must contain the item id or its distinctive name.

| Group | Rows | Failures |
|---|---:|---:|
| A (A1–A20) | 20 | 0 |
| B (B1–B20) | 20 | 0 |
| C (C1–C20) | 20 | 0 |
| D (D1–D20) | 20 | 0 |
| E (E1–E20) | 20 | 0 |
| F (F1–F22) | 22 | 0 |
| G (G1–G20) | 20 | 0 |
| H1, H2 | 2 | 0 |
| **Total item rows** | **144** | **0** |

One documented exception, already explained by Audit #67 §1.1 and not a
finding: B18 is cited at `make-interfaces-feel-better/SKILL.md:120`, whose
line reads "Icon swaps: cross-fade with opacity, scale, and blur instead of
instant…" — the pre-existing B18 rule text, carrying no "B18" token because
no new text was written for a covered item; the name is carried in the
motion-patterns AB-05 note, which verify22 asserts. My window check passed
it on the distinctive name ("cross-fade").

Process rows (all 26 re-checked, window ±3 lines must contain the anchor
token): Mobbin 4/4 (orchestrate `:62`, Taste `:445`, ui-ux-pro-max `:167`,
polish-pass `:104`); Directives 8/8 (orchestrate `:64`, Taste `:391` ×2,
ui-ux-pro-max `:219`, GAN planner `:46`, generator `:32`, evaluator `:134`,
polish-pass `:100`); Libraries 4/4 (Lenis motion-foundations `:178`, GSAP
ScrollTrigger motion-patterns `:429`, Vanta Taste `:127`, React Bits
motion-patterns `:552`); Bang 6/6 (pitch-deck-video `:247, :281, :304, :337,
:373, :409`); H1 2/2 (ui-ux-pro-max `:122`, sprawl check slop-checklist
`:419`); H2 3/3 (orchestrate `:62`, ui-ux-pro-max `:16`, slop-checklist
`:450`). **0 failures.**

## 4. Duplication — PASS

- fix22 block in build.sh appears exactly once: header
  `# --- fix22: weave 7 @charles.unemployed reels (142 items) + H1/H2
  accents + Mobbin + directives + 4 libraries + Bang Motion port ---` at
  `:23643`; `fix22 upstream block applied` ×1; block spans `:23641–23720`
  (80 lines, before STEP 5, after the fix21 block). `diff
  build.sh.before-fix22 build.sh` = **exactly 2 hunks, +85 / −0 lines**:
  the 5 BANG_PIN lines at `:42–46` and the 80-line fix22 block at
  `:23641–23720`. No other line in build.sh changed.
- No patch text duplicated in the built tree: every home anchor is ×1 in
  its home file (§1); no duplicate anchor definitions.
- No new skill / command / trigger key from fix #22: counts §7 unchanged;
  trigger keys 64, all resolving to real skill dirs (§7).

## 5. Banned-term set + model pins — PASS

| Scope | Banned-term-set lines | How counted |
|---|---:|---|
| Built tree (skills, agents, commands, rules, hooks, README.md, excl. `node_modules`) | **0** | case-insensitive grep over the seven banned strings — no file with a nonzero count |
| Staged sources (`new-skills/`, `round2-skills/`) | **0** | same grep — no file with a nonzero count |
| fix22 block in build.sh (`:23641–23720`) | **0** | same grep over the block lines |

The banned-term set appears in `fix22/fix22.py` on 2 lines only — the
scrub-list definition in the fix script itself, not rule text (same
standing as fix21's scrub list, per Sweep #29 §1). Model pins, full built
tree excl. `node_modules`: `grok-4.7-high` **54**, `cursor-grok-4.6-high-fast`
**102**, bare `grok-4.6-high-fast` (without the `cursor-` prefix) **0** —
exactly Audit #67's counts. The only non-Grok model string in the touched
files is the pre-existing stack-label example in
`skills/pitch-deck-video/SKILL.md:98` (an example stack label naming a
frontier model, present in `build.sh.before-fix22` — 10 hits there — so not
introduced by this fix).

## 6. Leftovers — PASS

- Word-boundary `TODO|FIXME|XXX|HACK` in all 33 files carrying fix #22
  anchors (3 GAN agents, Taste + glossary + 15 Hallmark themes,
  make-interfaces-feel-better, motion-foundations, motion-patterns,
  orchestrate, pitch-deck-video, polish-pass + craft-floor + vibe-code-tells
  + polish + slop-checklist + unslop-fixes, ui-ux-pro-max + quick-reference):
  **0 hits**. (The broad 618-hit count over the whole built tree is
  substring noise — "hackathon", "hack" inside ordinary words.)
- `LIB-05`: **0 hits** in the built tree and build.sh; in the working
  files it is referenced only as applied
  (`libraries-patches.md:3,31,301,473`, `libraries-report.md:4,140,149,155,200`,
  `fix22.py:19` — "already applied to the staged Taste source"). Nothing
  references it as pending. The staged edit survives: VANTA_F22 present in
  built Taste `:127` (staged `:126`, one-line frontmatter shift).
- No orphaned fix22 scratch contradicting the final state: `fix22/` holds
  the patch specs, dispositions, reports, logs, and verifier runs; the only
  marker hits in fix22 working files are in captured logs/dumps
  (`baseline-greps.txt`, `build1.log`, `build2.log` — a quoted pre-existing
  skill line captured by the build log), which are historical records,
  exempt.

## 7. Counts — PASS

| Inventory | Count | Command |
|---|---:|---|
| skills | **166** | `ls skills \| wc -l` |
| agents | **72** | `ls agents \| wc -l` |
| rules | **123** | `ls rules \| wc -l` |
| commands | **87** | `ls commands \| wc -l` |
| hooks | **15** | `len(json.load(open('hooks/hooks.json'))['hooks'])` |
| trigger keys | **64** | `skill-triggers@1.json`: `withTriggers == len(triggers) == 64`; every key resolves to a real skill dir (0 unresolvable) |

Unchanged post-fix21, per SPEC §6.6 (166/72/123/87/15, 64 trigger keys).
The glossary, slop checklist, and unslop fixes are reference files, not
skills. Marketplace manifests contain no F22 / fix22 markers (0 hits in
`hackathon-ecc/manifests/`).

## 8. Staged-vs-built diffs — PASS, pre-existing hunks only

| Staged file | Built counterpart | Result |
|---|---|---|
| `new-skills/orchestrate/SKILL.md` | `skills/orchestrate/SKILL.md` | IDENTICAL |
| `new-skills/design-taste-frontend/SKILL.md` | `skills/design-taste-frontend/SKILL.md` | DIFFERS — frontmatter description hunk only (the pre-existing build.sh description replacement documented in Sweep #29 §6) |
| `new-skills/design-taste-frontend/references/design-glossary.md` | `skills/design-taste-frontend/references/design-glossary.md` | IDENTICAL |
| Hallmark theme files (51 files) | `skills/design-taste-frontend/references/hallmark/references/themes/` | IDENTICAL, 51/51 |
| `round2-skills/polish-pass/SKILL.md` | `skills/polish-pass/SKILL.md` | DIFFERS — pre-existing hunks only (frontmatter description + "never redesigns" paragraphs, the build.sh block "(f)" patch documented in Sweep #29 §6) |
| `round2-skills/polish-pass/reference/slop-checklist.md` | `skills/polish-pass/reference/slop-checklist.md` | IDENTICAL |
| `round2-skills/polish-pass/reference/unslop-fixes.md` | `skills/polish-pass/reference/unslop-fixes.md` | IDENTICAL |
| `new-skills/pitch-deck-video/SKILL.md` | `skills/pitch-deck-video/SKILL.md` | IDENTICAL |

All fix #22-relevant regions match exactly (§1, §3). The two differing
files differ only where build.sh's pre-existing patch blocks rewrite text
that is present in `build.sh.before-fix21` — not fix #22 edits.

## 9. Pins — PASS (confirmed arrangement)

- GSAP converges on **3.15.1** in the built tree; "3.12.2" appears nowhere
  in the built tree; "GSAP 3.12.5" ×2, both Bang-reference-only
  (pitch-deck-video `:219, :245`); "GSAP 3.13" is the licence-history
  reference, not a pin.
- three.js is scoped as specified: `three@0.134.0` ×5 occurrences (Vanta
  scope), `three@0.185.1` ×7 occurrences (general scope, incl. threejs.csv),
  Bang's `0.161.0` ×3 occurrences across 2 lines, both inside the Bang
  section of pitch-deck-video as Bang's version only.
- BANG_PIN `c1aa65e9…` ×1 in build.sh (`:42`, full SHA
  `c1aa65e921c970d858705fcb4a53a8294d1a4131`), in pitch-deck-video, and in
  `fix22/bang-report.md`.

## 10. Verifiers re-run by this sweep

| Verifier | Result |
|---|---:|
| `fix22/verify22.py` | **291/291 checks pass, exit 0** (re-run by this sweep) |

Prior verifiers were not re-run by this sweep; Audit #67 §7 and Dry-run #36
§1 record `fix21/verify21.py` at 96/102, failing only the frozen post-fix21
build.sh fingerprint plus its 5 cascade lines — legitimately superseded by
fix #22 (23,732 lines / md5 `891fca7b…`), and allowed by verify22 §17.

## 11. Open items (not findings — coordinator steps before the fix closes)

1. **`fix22/MANIFEST.md` not yet written.** SPEC §6.8 requires it before
   close (disposition, placement as built, adjudication notes,
   glossary-home justification, counts, verifier/audit/dry-run/sweep
   results). Recorded as open by Audit #67 §8 item 1 as well; still open.
2. **Parent adjudications still open:** the three token conflicts (B3 30ms
   vs Rule 5 0.05s floor; B15 0.8× vs quick-reference ~60–70%; B4 0.97 vs
   `scale.press` 0.95) and the C13 vs Impeccable eyebrow tension — all
   carried as recorded flags in the built text, none silently resolved.
3. **Findings 1–2 above** are the coordinator's fix loop: add the three
   ANIM anchor strings or demote them in the working docs; correct SPEC
   §6.1's "142" to 144.

## Commands used (full list)

```
md5sum build.sh ; wc -l build.sh
python3 fix22/verify22.py
diff build.sh.before-fix22 build.sh ; diff build.sh.before-fix22 build.sh | grep -c '^>' / '^<'
python3 /tmp/sweep30.py  (anchor-token counts in built tree + build.sh; banned-term grep built tree + staged sources; stale-string greps built tree + build.sh + fix22/; counts; fix22-block lines; model-name greps in the 33 F22-anchor files; marketplace-manifest F22 grep)
grep -rn "ANIM_TOKENS_F22|ANIM_RULES_F22|ANIM_ADV_F22" fix22/ build.sh new-skills/ round2-skills/ hackathon-ecc/ --exclude-dir=node_modules --exclude-dir=__pycache__
grep -n "142 items|3.12.2|40x40px" build.sh ; sed -n '38,48p;23641,23655p;22060,22100p' build.sh
grep -rn "GPT" hackathon-ecc/skills/pitch-deck-video/SKILL.md ; grep -c "GPT" build.sh.before-fix22
python3 (word-boundary TODO/FIXME/XXX/HACK over all 33 F22-anchor files; disposition-merged 144-row + 26-process-row citation check; trigger-key resolution)
grep -ro "TRENDS_F22|SLOP_F22|UNSLOP_F22|GLOSSARY_F22|PRINCIPLES_F22|LAWS_F22|three@0.185.1|three@0.134.0|0.161.0" hackathon-ecc/ --exclude-dir=node_modules | wc -l (per pattern)
grep -ro "grok-4.7-high|cursor-grok-4.6-high-fast" hackathon-ecc/ --exclude-dir=node_modules | wc -l ; grep -rP '(?<!cursor-)grok-4\.6-high-fast' hackathon-ecc/ --exclude-dir=node_modules | wc -l
diff (staged vs built: orchestrate, Taste, glossary, 51 Hallmark themes, polish-pass SKILL + slop-checklist + unslop-fixes, pitch-deck-video)
grep -rn "LIB-05" fix22/ build.sh new-skills/ round2-skills/ hackathon-ecc/ --exclude-dir=node_modules --exclude-dir=__pycache__
grep -rn "144 items|144-item" hackathon-ecc/ --exclude-dir=node_modules ; grep -rn "23 treatments" hackathon-ecc/ --exclude-dir=node_modules
grep -rciE <banned-term set> --exclude-dir=node_modules hackathon-ecc/skills hackathon-ecc/agents hackathon-ecc/commands hackathon-ecc/rules hackathon-ecc/hooks hackathon-ecc/README.md ; same for new-skills round2-skills
ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l ; python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"
```
