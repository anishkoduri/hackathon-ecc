# Dry-run #36 — Fix #22 weave (reels, H1/H2, Mobbin, directives, libraries, Bang Motion)

- **Date:** 2026-11-12, evening CST. Worker: dry-run agent (fix #22), check-only.
- **Scope kept:** read-only against the plugin tree and the built tree. Two files written, both inside `fix22/dryrun36/`: the fixture runner `dryrun36-fixtures.py` and its captured output `dryrun36-output.txt`. This report is the third file, at `fix22/dryrun36-report.md`. No staged source, `build.sh`, built-tree file, or verifier edited; no commit, no bundle, no GitHub touch, no message to Anish.
- **Verdict: DRY-RUN #36: PASS.** All 46 fixture expectations met (see the table). No findings.

## 0. Method — Dry-run #35 followed

This dry-run follows the Dry-run #35 method (`fix21/dryrun35-report.md` + `fix21/dryrun35-fixtures.py`):

1. Re-run the fix verifier this session (`fix22/verify22.py`).
2. Grep the built tree for the rule anchors the fixtures judge against; the fixture runner asserts those anchor phrases verbatim against the built tree at run time (read, never retyped from memory) before running any fixture.
3. Apply the check logic stated in the built skill texts to small fixture inputs. Each fixture prints an explicit PASS/FAIL from the script itself: PASS means the observed outcome matched the SPEC's expected outcome.
4. A fixture is a finding ONLY if the observed outcome differs from the SPEC's expected outcome.

Starting state confirmed this session: `build.sh` = 23,732 lines, md5 `891fca7b5f34aa74db95cb04501345a0` (matches the task's stated gate numbers); built tree 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys.

## 1. Rule presence — verify22.py re-run by this worker: PASS (291/291, exit 0)

Re-ran `python3 fix22/verify22.py` from `~/workspace/hackathon-plugin/` this session. Final line: **291/291 checks pass**. The run's tail also records the older verifiers as passing except for their stale post-fix21 `build.sh` fingerprints (fix19 72/76, fix20 164/169, fix21 96/102 on that leg) — expected after a new fix changes `build.sh`, and recorded as PASS lines by verify22 itself, not as failures. This dry-run does not re-litigate those fingerprint checks; verify22 is the governing verifier for fix #22 and it passes 291/291.

Anchor phrases asserted verbatim by the fixture runner (all present in the built tree — the runner prints `anchors: all rule texts present verbatim in the built tree`):

- `SLOP_F22` header: "flags **unconsidered default usage**, never deliberate use" + "cleared by a recorded D19 reason + theme-fit" (`skills/polish-pass/reference/slop-checklist.md:15-18`); C3/C13/C14/C15/C16/C19 flag lines; "accent sprawl is a flag, slop-adjacent" (`:419-425`).
- Trend rule: "A trend used with no theme-match reason is an incomplete build" (`skills/design-taste-frontend/SKILL.md:246`).
- H1: "One accent colour (fix #22 H1, ACCENT_F22)" (`skills/ui-ux-pro-max/SKILL.md:122`); H2: "A screen with no deliberate accentuation" (`skills/orchestrate/SKILL.md:62`, ACCENTUATION_F22).
- Mobbin: "A build that cites a Mobbin screen as its design source FAILS" + "the build is NEVER blocked on Mobbin" (`skills/orchestrate/SKILL.md:62`); `MOBBIN_QA_F22` (`skills/polish-pass/SKILL.md:104`).
- Directives: "FAILS the handoff check" + "Implementers do not re-interpret directives" (`skills/orchestrate/SKILL.md:64`).
- Tokens: "Reuse the same layoutId" (`skills/motion-patterns/SKILL.md:87`); "dropdowns animate at 150–250ms" (`:214`); "stagger the details in 30ms steps" (`:231`); "React Bits is React-only" (`:552`).
- Bang: "one continuous world, a moving camera, a persistent subject" + "No text under 30px on a 1080-wide stage" + "A composition that uses a style direction with no theme/brand reason FAILS" (`skills/pitch-deck-video/SKILL.md:199-200, 247-270, 324`).

## 2. Proxies — recorded explicitly

- **§12 Bang fixtures are composition manifests judged by static review** against the pitch-deck-video anti-slide checks. There is no live browser in this dry-run, so no footage was filmed; fixture 12e (film-the-real-app) is judged on the composition manifest's beat plan (filmed beats vs generated-graphics beats), the closest executable proxy. No fixture is marked PASS on the basis of reading the skill text alone — every §12 fixture is an input manifest the `check_bang` / `check_av_table` logic runs over.
- **Slop flags are static checks producing candidate evidence, never screen verdicts** (fix #13e). The runner models the FLAG/CLEAR outcome of the static check, not a verdict on a rendered screen.
- **One runner bug, fixed in the runner, not the plugin:** the first run returned 45/46 because fixture 6.3a passed an inverted boolean (`all(not ok ...)` where the check's "cleared" value was meant). The check logic was correct; the fixture's expectation wiring was wrong. Fixed in `dryrun36-fixtures.py`, re-run twice: **46/46, exit 0** both times.

## 3. Per-fixture table

Judging skill/check column gives the built-tree anchor (file:line). "Observed" is the script's output for that fixture, quoted or paraphrased from `fix22/dryrun36/dryrun36-output.txt`.

### §6.3 Slop flags (SPEC items a–h) + legitimate-technique family pairs

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 6.3a | Pills + gradient wash + divider soup, no reasons, as unconsidered defaults | `polish-pass/reference/slop-checklist.md:15-18` (SLOP_F22 header: flags unconsidered default usage) | FLAG on all three (C1, C19, C6) | FLAG | PASS |
| 6.3b | Same three items, each with recorded D19 reason + theme-fit | `slop-checklist.md:15-18` (cleared by recorded D19 reason + theme-fit) | CLEAR on all three | CLEAR | PASS |
| 6.3c | Default purple gradient wash | `slop-checklist.md:385` (C19) + `design-taste-frontend/SKILL.md:290` (E7: purple-to-blue wash FAILS the polish check) | FLAG | FLAG | PASS |
| 6.3c-control | Theme-matched gradient treatment (less-flat-ui #3/#9) + D19 | `slop-checklist.md:385` (C19 justified use) | CLEAR | CLEAR | PASS |
| 6.3d | Theme-matched dithering (less-flat-ui #11) + D19 reason | `slop-checklist.md:300` (C14 justified use) | CLEAR | CLEAR | PASS |
| 6.3d-control | Dithering as the whole visual identity, no reason | `slop-checklist.md:300` (C14 flag) | FLAG | FLAG | PASS |
| 6.3e | Shared-element transition reusing the same layoutId | `motion-patterns/SKILL.md:87` (B20 layoutId reuse) | PASS | PASS | PASS |
| 6.3f | Dropdown 200ms + 30ms row stagger (+ popover 0.95) | `motion-patterns/SKILL.md:214, 231` (B2/B3/B6 token values) | PASS token check | PASS | PASS |
| 6.3f-control | Dropdown at 600ms, stagger 30ms | `motion-patterns/SKILL.md:214` (150–250ms band) | FAIL token check (600ms outside band) | FAIL | PASS |
| 6.3g | Trend E7 dark gradient heroes, no theme reason | `design-taste-frontend/SKILL.md:246` (TRENDS_F22: no theme-match reason = incomplete build) | FAIL (incomplete build) | FAIL | PASS |
| 6.3g-control | Same trend with theme-match reason + D19 | `design-taste-frontend/SKILL.md:246` | PASS | PASS | PASS |
| 6.3h | Eyebrow label, no D19 reason | `slop-checklist.md:271` (C13 flag) | FLAG | FLAG | PASS |
| 6.3h | Single deliberate key label + D19 + theme-fit + fix #20 F5 key-label record | `slop-checklist.md:271` (C13 clearance) | CLEAR | CLEAR | PASS |
| 6.3h-extra | Repeated eyebrow above every section heading, even with a reason + F5 record | `slop-checklist.md:271` (repeated eyebrow stays a craft-floor ban regardless of any reason recorded) | FLAG | FLAG | PASS |
| Family ASCII | ASCII art as the default visual, no reason | `slop-checklist.md:318` (C15 flag) | FLAG | FLAG | PASS |
| Family ASCII | Theme-matched ASCII (less-flat-ui #22) + D19 | `slop-checklist.md:318` (C15 justified use) | CLEAR | CLEAR | PASS |
| Family Instrument Serif | Instrument Serif defaulted to as display/body face, no recorded choice | `slop-checklist.md:104` (C3 flag: defaulting to it IS the tell) | FLAG | FLAG | PASS |
| Family Instrument Serif | Face chosen through the skills + D19 + Source cell naming the skill text | `slop-checklist.md:104` (C3 clearance) | CLEAR | CLEAR | PASS |
| Family squircle | Squircle as the default container shape, no reason | `slop-checklist.md:334` (C16 flag) | FLAG | FLAG | PASS |
| Family squircle | Theme-matched squircle + D19 | `slop-checklist.md:334` (C16 justified use) | CLEAR | CLEAR | PASS |

Family coverage: all six legitimate-technique families the task names are covered as FLAG/CLEAR pairs — dithering (6.3d), ASCII, gradient backgrounds (6.3c), Instrument Serif, eyebrows (6.3h), squircles. In every pair the same use with no reason flags and the same use with a recorded D19 reason + theme-fit clears.

### §8 H1/H2 accents

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 8-H2a | Screen with no declared accents (everything same weight) | `orchestrate/SKILL.md:62` (ACCENTUATION_F22: no deliberate accentuation fails the check) | FAIL | FAIL | PASS |
| 8-H2b | Declared first/second/third + means (size + H1 colour / weight / spacing) + D19 reason each | `orchestrate/SKILL.md:62` + `ui-ux-pro-max/SKILL.md:15-19` (H2 hierarchy rules) | PASS | PASS | PASS |
| 8-H1a | Three competing accent hues (#7C3AED, #F59E0B, #06B6D4), accent also on non-action elements | `slop-checklist.md:419` (ACCENT_F22 sprawl flag) + `ui-ux-pro-max/SKILL.md:122` (H1) | FAIL sprawl check | FAIL | PASS |
| 8-H1b | Single accent hue (#7C3AED), action/emphasis only, recorded in brand tokens with D19 | `slop-checklist.md:419` (ACCENT_F22 justified use) | PASS | PASS | PASS |

### §9 Mobbin

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 9a | Decision record cites a Mobbin URL as the design source | `orchestrate/SKILL.md:62` (MOBBIN_RESEARCH_F22: cites a Mobbin screen as source FAILS) | FAIL | FAIL | PASS |
| 9b | Mobbin categories consulted (onboarding, paywall); direction generated through Taste, Taste recorded as source | `orchestrate/SKILL.md:62` + `design-taste-frontend/SKILL.md:445` (MOBBIN_PATTERN_F22) | PASS | PASS | PASS |
| 9c | Mobbin unreachable; gap recorded; design proceeds from the skills alone | `orchestrate/SKILL.md:62` (never blocked on Mobbin; recorded-gap fallback) | PASS (never blocked) | PASS | PASS |
| 9d | Layout copied from a specific Mobbin screen | `orchestrate/SKILL.md:62` + `design-taste-frontend/SKILL.md:445` (no-copy boundary; anti-derivative rule) | FAIL anti-derivative | FAIL | PASS |

### §10 Directives

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 10a | Handoff is prose-only ("make it warm and premium"), no exact values | `orchestrate/SKILL.md:64` (DIRECTIVES_F22: description without exact values FAILS the handoff check) | FAIL handoff check | FAIL | PASS |
| 10b | Handoff with exact tokens/values/copy + D19 reason | `orchestrate/SKILL.md:64` | PASS | PASS | PASS |
| 10c | Implementer re-interprets a directive instead of executing it or flagging a recorded gap | `orchestrate/SKILL.md:64` (implementers do not re-interpret; improvising fails the audit) | FAIL | FAIL | PASS |
| 10d | Directive with exact values but no D19 reason | `orchestrate/SKILL.md:64` (a directive without its D19 reason is incomplete) | FAIL (incomplete) | FAIL | PASS |
| 10e | Directive with exact values + D19 reason | `orchestrate/SKILL.md:64` | PASS | PASS | PASS |
| 10c-control | Ambiguous directive surfaced as a recorded gap, not improvised around | `orchestrate/SKILL.md:64` (recorded-gap fallback) | PASS | PASS | PASS |

### §11 Libraries

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 11a | Vanta background (`vanta@0.5.24`), no reduced-motion fallback | `design-taste-frontend/SKILL.md:127` (VANTA_F22: MUST disable under `prefers-reduced-motion`) | FAIL (incomplete build) | FAIL | PASS |
| 11b | React Bits on an `html-tailwind` (non-React) stack | `motion-patterns/SKILL.md:552` (REACTBITS_F22: React/Next only) | FAIL scope check | FAIL | PASS |
| 11c | GSAP effect directed by name + exact parameters, pinned `gsap@3.15.1`, theme-matched | `ui-ux-pro-max/SKILL.md:279` (GSAP rule: effect name + exact parameters) | PASS | PASS | PASS |
| 11d | Same GSAP effect with no theme reason | `ui-ux-pro-max/SKILL.md:279, 379` (theme-match precondition) | FAIL (not applied) | FAIL | PASS |
| 11e | GSAP effect at version `latest` | `ui-ux-pro-max/SKILL.md:379` ("latest" FAILS the pin check) | FAIL pin check | FAIL | PASS |
| 11a-control | Vanta pinned + reduced-motion fallback + theme reason | `design-taste-frontend/SKILL.md:127` | PASS | PASS | PASS |

### §12 Bang Motion (proxy: static composition review — see §2)

| Fixture | Input | Judging skill/check | Observed outcome | Expected outcome | Result |
|---|---|---|---|---|---|
| 12a | Composition manifest: two slide-fade beats, static camera, no persistent subject | `pitch-deck-video/SKILL.md:247` (BANG_ANTISLIDE_F22 checks 1–3) | FAIL anti-slide | FAIL | PASS |
| 12b | Composition manifest: one continuous world, camera moves, persistent subject, text ≥30px, style direction theme-matched, filmed beats kept | `pitch-deck-video/SKILL.md:247, 252-270` + `:211` (BANG_ONEWORLD_F22) | PASS | PASS | PASS |
| 12c | Composition with 22px text on a 1080-wide stage | `pitch-deck-video/SKILL.md:269` (check 7: no text under 30px) | FAIL (under 30px) | FAIL | PASS |
| 12d | Composition using style direction "brutalist mono" with no theme/brand reason | `pitch-deck-video/SKILL.md:324` (BANG_STYLES_F22: no theme/brand reason FAILS QA) | FAIL | FAIL | PASS |
| 12e | Composition whose How/features beats are generated motion graphics, not filmed footage | `pitch-deck-video/SKILL.md:211` (filmed How/features beats stay filmed) + fix #18 redirect | FAIL (film-the-real-app) | FAIL | PASS |
| 12f | A/V table rows include kinetic-type and camera-move claims | `pitch-deck-video/SKILL.md:199` (F5: kinetic type and camera moves go IN the table) | PASS | PASS | PASS |

## 4. Verdict summary

| Section | Fixtures | Result |
|---|---|---|
| §6.3 slop flags + family pairs | 20 | PASS (20/20) |
| §8 H1/H2 accents | 4 | PASS (4/4) |
| §9 Mobbin | 4 | PASS (4/4) |
| §10 directives | 6 | PASS (6/6) |
| §11 libraries | 6 | PASS (6/6) |
| §12 Bang Motion | 6 | PASS (6/6) |
| **Total** | **46** | **PASS (46/46, exit 0, confirmed on re-run)** |

**DRY-RUN #36: PASS**

## 5. Notes for the coordinator / parent (not findings)

1. **C13 eyebrow tension, recorded in the checklist itself.** `slop-checklist.md:271` (C13) records a flagged-for-parent conflict: the SPEC §4a allowance (a single deliberate theme-matched key label with a D19 reason is justified) points one way and the Impeccable craft floor's absolute ban on a kicker/eyebrow above a heading points the other; the check applies the stricter rule, so clearance requires the D19 reason + theme-fit + the fix #20 F5 key-label record, and covers one deliberate key label only, never a repeated pattern. Fixture 6.3h follows the checklist's own stated clearance path and passes; fixture 6.3h-extra confirms the repeated pattern still flags even with a reason. The underlying conflict is the checklist author's flag for the parent, not a dry-run finding — the built text behaves exactly as it states.
2. **Older verifiers' stale fingerprints.** verify22's regression leg notes fix19/fix20/fix21 pass except for their stale post-fix21 `build.sh` fingerprints (expected: `build.sh` changed under fix #22). verify22 itself is 291/291. If the audit wants the older verifiers green in isolation, their fingerprint expectations need updating to the post-fix22 build — that is coordinator work, not a fix #22 rule defect.
3. **Runner bug, not a plugin defect (§2).** First run was 45/46 on a wiring error in the runner's 6.3a fixture (inverted boolean); fixed in the runner and re-run twice at 46/46.
4. **§12 proxy stands.** The Bang fixtures were judged on composition manifests by static review; no footage was filmed in this dry-run (no live browser). A live /demo run remains the only end-to-end confirmation that filmed beats stay filmed in a real composition.

## Files / evidence used (read-only, except the files written)

- `~/workspace/hackathon-plugin/fix22/SPEC.md` (§6.3, §8, §9, §10, §11, §12 — fixture definitions and expected outcomes)
- `~/workspace/hackathon-plugin/fix21/dryrun35-report.md` + `fix21/dryrun35-fixtures.py` (method followed)
- `~/workspace/hackathon-plugin/fix22/verify22.py` (re-run this session: **291/291**, exit 0)
- `~/workspace/hackathon-plugin/fix22/dryrun36/dryrun36-fixtures.py` (written this session; run: **46/46 fixture expectations met**, exit 0, confirmed on re-run)
- `~/workspace/hackathon-plugin/fix22/dryrun36/dryrun36-output.txt` (captured script output)
- Built tree (read-only greps + runner anchor assertions this session): `hackathon-ecc/skills/polish-pass/reference/slop-checklist.md` (SLOP_F22, C1/C3/C6/C13/C14/C15/C16/C19, ACCENT_F22 :419, ACCENTUATION_F22 :450); `design-taste-frontend/SKILL.md:127, 246, 445`; `ui-ux-pro-max/SKILL.md:15-19, 122, 167, 279, 379`; `orchestrate/SKILL.md:62, 64`; `polish-pass/SKILL.md:98-99, 104`; `motion-patterns/SKILL.md:87, 214, 231, 428, 552`; `motion-foundations/SKILL.md:178`; `pitch-deck-video/SKILL.md:199-200, 211, 247-270, 324, 373`
- `build.sh` measured this session: 23,732 lines, md5 `891fca7b5f34aa74db95cb04501345a0`
