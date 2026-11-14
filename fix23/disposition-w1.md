# Fix #23 W1 disposition — §1 Ambition + §2 Motion + THE INVENTORY + orchestrate design-package backbone

Worker W1. Scope: SPEC §1, §2, the inventory mechanism, and the orchestrate
design-package backbone. §3/§4/§5/§6 belong to W2/W3/W4; their lines are
inserted later by integration at the anchor left in orchestrate SKILL.md
(see below). No bundle, no commit, no push. `build.sh` NOT run, NOT edited
(md5 still `4799a819791b9c3ec4c19136ad698397`, 23,774 lines). The built tree
was read-only for counting/anchor verification. `fix11/fix11-stage.py` not
re-run. Prior verifiers not edited. `~/workspace/cursor-skills/less-flat-ui`
not edited (read-only; D-A2). No /demo or DEMOGATE token touched.

## Files changed / created by W1

| File | Change |
|---|---|
| `new-skills/orchestrate/SKILL.md` | 2 insertions (design-package step block; F6-primary-gate extension) + integration anchor comment |
| `new-skills/orchestrate/references/design-inventory.md` | NEW — the inventory catalog (INVENTORY_F23) |
| `new-skills/orchestrate/references/dispatch-prompt.md` | 1 insertion (§5a — the design-lead prompt names the inventory) |
| `fix23/apply-w1.py` | NEW — inserts the W1 runtime-patch block into build.sh before `# STEP 5 — Counts` (integration runs it; W1 did NOT run it) |
| `fix23/disposition-w1.md` | This file |

## Where the design-lead prompt lives (finding)

There is no standalone "design-lead prompt" file. The design-lead is a role
in orchestrate (team table, row 10) whose operating prompt is the UI
dispatch template: `new-skills/orchestrate/references/dispatch-prompt.md`
§5a ("Design package — named by default on every UI dispatch"), which is
what the design-lead executor actually receives, plus the design-package
rule in `new-skills/orchestrate/SKILL.md` (row 10 + step 3). The inventory
is therefore referenced from BOTH: orchestrate SKILL.md step 3
(INVENTORY_F23) AND dispatch-prompt.md §5a (INVENTORY_F23). The inventory
file itself ships with orchestrate: `build.sh:224` copies
`new-skills/orchestrate/SKILL.md` + `references/` verbatim, so
`new-skills/orchestrate/references/design-inventory.md` lands in the built
tree as `skills/orchestrate/references/design-inventory.md` with no
`build.sh` edit.

## Integration anchor (for W2/W3/W4 lines)

`new-skills/orchestrate/SKILL.md:72` (after the W1 step-3 block):

`<!-- F23-ORCHESTRATE-EXTENSIONS: integration inserts §3/§4/§5/§6 lines here -->`

## Per-item placement table

Status: new = W1 wrote new text; covered = already present, cited as pointer; pointer = inventory entry pointing at the owning skill's own text.

### §1 Ambition

| SPEC item | Placement (file + anchor token) | Status |
|---|---|---|
| Design package records USED vs CONSIDERED-AND-REJECTED with D19 reasons | `new-skills/orchestrate/SKILL.md` step 3, `AMBITION_F23` | new |
| "Considered and rejected" must be specific, never a blanket line | Same block, `AMBITION_F23` ("a line like 'we considered everything' is not a reason and fails the bar") | new |
| Small-slice use without recorded specific reasons FAILS the ambition bar | Same block, `AMBITION_F23` | new |
| Design usable without the package (none of the inventoried elements beyond the bare minimum) fails | Same block, `AMBITION_F23` | new |
| Ambition = MORE elements, MORE motion, MORE decisions — not louder; "more, not bolder" stands | Same block, `AMBITION_F23` | new |
| F6 is the PRIMARY gate: browser-qa judges impressive AND ambitious, not just rule-correct | `new-skills/orchestrate/SKILL.md` step 3 `AMBITION_F23` + F6 section extension, `AMBITION_F23` (after "the bar governs, the bans bind") | new |
| THE INVENTORY — one catalog file, read BEFORE deciding | `new-skills/orchestrate/references/design-inventory.md`, `INVENTORY_F23`; referenced from orchestrate SKILL.md step 3 (`INVENTORY_F23`) and dispatch-prompt.md §5a (`INVENTORY_F23`) | new |
| Inventory kept current — future fixes update it in the same change | Inventory file, Currency rule (`INVENTORY_F23`); orchestrate step-3 block (`INVENTORY_F23`) | new |

### THE INVENTORY — coverage (all counts verified by reading the actual files, Nov 12, 2026)

| Coverage item (SPEC §1) | Inventory § | Verified count / source | Status |
|---|---|---|---|
| ui-ux-pro-max styles | §1 | 89 rows in `data/styles.csv` (skill header describes 80 searchable, 51 active — both numbers given, csv is the source) | new |
| ui-ux-pro-max palettes | §1 | 192 rows in `data/colors.csv` | new |
| ui-ux-pro-max font pairings | §1 | 74 rows in `data/typography.csv` | new |
| ui-ux-pro-max UX guidelines | §1 | 120 rows in `data/ux-guidelines.csv` | new |
| ui-ux-pro-max icons | §1 | 105 rows in `data/icons.csv` | new |
| ui-ux-pro-max GSAP presets | §1 | 17 rows in `data/motion.csv` (+ `--domain gsap`) | new |
| ui-ux-pro-max chart types | §1 | 25 rows in `data/charts.csv` | new |
| ui-ux-pro-max stacks | §1 | 22 csv files in `data/stacks/` | new |
| Taste hero + dealt moments, finish gate | §2 | 18 moments in `assets/moments/index.json`, 13 dealt (transition 4, text 4, hover 1, scroll 7, liquid 2); 5 retired; gate in `references/gate.md` | new |
| Hallmark 50-theme catalog, sloplint, hero/finish reviews | §3 | 50 themes in `references/hallmark/references/themes/index.json` (50 `.md` files); sloplint scripts; review-hero / review-finish | new |
| Impeccable detector rules, craft floor | §4 | 62 rules in `impeccable-detector-rules.json`; craft floor in `craft-floor.md` | new |
| less-flat-ui, all 23 treatments | §5 | 23 `###` headings #1–#23 in the global skill (read-only; D-A2 — not edited) | pointer |
| motion-foundations principles + laws, motion-patterns tokens, motion-advanced examples | §6 | A1–A12 principles, A13–A20 laws, B1–B20 tokens/rules, 17 motion-advanced code examples | new |
| polish-pass slop checklist, unslop fixes, Vercel checklist, accent checks | §7 | 20 checks C1–C20; 20 fixes D1–D20; Vercel 16 groups / 104 rule bullets; ACCENT_F22 / ACCENTUATION_F22 / WEBGL_ONE_F22 / ORBS_F22 / DEPTH_F22 | new |
| design-system | §8 | Modes 1–3 + daisyUI component menu | new |
| make-interfaces-feel-better | §8 | 9 core principles; default motion set M1–M6 | new |
| Fix #22 glossary terms | §9 | 20 terms G1–G20 in `design-glossary.md` | new |
| Fix #22 H1/H2 accents | §9 | ACCENT_F22 / ACCENTUATION_F22 | new |
| Fix #22 Mobbin pattern research | §9 | MOBBIN_RESEARCH_F22, category-level, free tier only | new |
| Fix #22 direct-don't-describe | §9 | DIRECTIVES_F22 | new |
| Fix #22 11 asset libraries/tools | §9 | 4 (§11) + 4 (§15) + 3 (§17) = 11; pins carried from fix22/MANIFEST.md (Lenis 1.3.27, GSAP 3.15.1, Vanta 0.5.24, React Bits 9d9c687…, R3F 9.8.2/8.18.0, liquid-glass-js 78cb6cc…, ShaderGradient 2.4.20, liquid-logo 689bb38…, Casberry BARRED until terms confirmed, OriginKit 10 fetches/day, daisyUI 5.7.50) | new |
| Fix #22 Bang Motion layer | §9 | 10 style directions + 19 opener concepts in pitch-deck-video | new |
| Fix #22 Depth tokens | §9 | perspective 1000, parallax 0.5/0.25/0.1, tilt max 6°, elevation 8/16/24 | new |
| Fix #22 Thinking Orb states | §9 | 9 states, sizes 64/20, `thinking-orbs@0.3.2`, no "thinking" state | new |
| Skill-bundled reference inventories | §10 | Taste palettes 64 / type 39 (json); ui-ux-pro-max data catalogs; Hallmark 50; Impeccable 62 | new |

### §2 Motion

| SPEC item | Placement (file + anchor token) | Status |
|---|---|---|
| Deliberate motion is the default on every build (entrances, staggers, dealt moments, micro-interactions, state transitions) | Orchestrate SKILL.md step 3, `MOTION_F23`; runtime subs MOTION-01–05 (see below) | new |
| Motion routed through fix #22 tokens (Group A + Group B, e.g. stagger 30ms, press 0.97, dropdowns 150–250ms) | Orchestrate step 3 `MOTION_F23`; MOTION-01/02/05 add-texts (`MOTION_F23`) | new |
| A build that feels static fails even if every static rule passes | Orchestrate step 3 `MOTION_F23`; MOTION-01–05 add-texts | new |
| Motion recorded with D19 reason (Motion dimension) + token values, directed per §10 | Orchestrate step 3 `MOTION_F23`; MOTION-01–05 add-texts | new |
| `prefers-reduced-motion` respected everywhere, complete static fallback (not broken) | Orchestrate step 3 `MOTION_F23`; MOTION-01–05 add-texts | new |
| Scope guard: Taste landing pages keep the scroll ban (hero entrance + dealt moments + micro-interactions only) | MOTION-01 add-text + `apply-w1.py` block header comment | new |

### Runtime patches (`fix23/apply-w1.py` → build.sh block before `# STEP 5 — Counts`)

Each sub is (id, rel-path, old-anchor, add-text, mode). All anchors verified
count==1 against the CURRENT built tree by grep before the script was
written; the block re-asserts count==1 at build time and fails loudly.
Idempotency guard: the script refuses if its marker comment
(`# --- fix23 W1: motion default (fix #23 §2, MOTION_F23) ---`) is already
in build.sh. The script was NOT run (integration runs it). `py_compile`
passed; the block's inner Python compiles; marker absent from build.sh;
`# STEP 5 — Counts` count==1.

| Sub | Target (built tree) | Anchor (count==1) | Mode | Token |
|---|---|---|---|---|
| MOTION-01 | `skills/motion-foundations/SKILL.md` | `## Rules` | after | MOTION_F23 |
| MOTION-02 | `skills/motion-patterns/SKILL.md` | `## Rules` | after | MOTION_F23 |
| MOTION-03 | `skills/motion-advanced/SKILL.md` | `## Rules` | after | MOTION_F23 |
| MOTION-04 | `skills/make-interfaces-feel-better/SKILL.md` | `### Motion` | after | MOTION_F23 |
| MOTION-05 | `skills/ui-ux-pro-max/SKILL.md` | `## Before Delivering App UI` | after | MOTION_F23 |

Anchors that did NOT resolve count==1: none. Every anchor above resolved
count==1 (also re-checked by extracting the subs from `apply-w1.py` and
counting against the built tree after writing).

## Verification done by W1

- Baseline re-checked: `build.sh` 23,774 lines, md5
  `4799a819791b9c3ec4c19136ad698397` — unchanged after W1's work.
- Banned terms (claude/codex/anthropic/opus/sonnet/haiku/composer-2.5,
  case-insensitive): 0 in the inventory file, orchestrate SKILL.md,
  dispatch-prompt.md, and the `apply-w1.py` BLOCK.
- Grok pins: no bare `grok-4.6-high-fast` in any W1 text (W1 wrote no model
  pins; the only model mentions are the pre-existing ones).
- `apply-w1.py`: `py_compile` OK; embedded build.sh block's inner Python
  compiles OK; preconditions hold (marker absent, STEP 5 count==1).
- D19 seven dimensions stand (W1 touched no D19 text); "more, not bolder"
  and anti-derivative restated in the new blocks; browser-qa remains the
  sole verdict executor (F6 extension says the verdict stays browser-qa's
  alone, never a static check).

## What W1 could NOT verify / open items for integration

- `apply-w1.py` was NOT run per instructions, so the block's insertion into
  `build.sh` and the resulting built tree are unverified until integration
  runs it (the block's own asserts are the check).
- `daisyUI 68 components` (the plugin's recorded count — design-system
  skill + fix22/MANIFEST.md agree) and the 11 library pins are carried from
  fix22/MANIFEST.md, not re-counted from the libraries themselves in this
  pass (the manifest is the recorded source; the inventory cites it as such
  for daisyUI's component count). 65 was the §17 research count; 68 is the
  corrected figure.
- The `styles.csv` 89-row count vs the skill header's "80 searchable styles
  (51 active)" disagree; the inventory records both and treats the csv as
  the source. If the header is the intended count, the inventory's styles
  line needs a correction — flagged, not silently resolved.
- Open token conflicts carried verbatim from fix #22 (B3 30ms vs Rule 5
  0.05s floor; B15 0.8x vs quick-reference ~60–70%; B4 0.97 vs
  `scale.press` 0.95): recorded as flags in the inventory (§6) and in the
  `apply-w1.py` block header. This block changes no token value; the parent
  still adjudicates.
- Sibling workers (W2/W3/W4) have files in `fix23/` already
  (`apply-w2.py`, `apply-w3.py`, `apply-w4.py`, `disposition-w4.md`,
  `orch-lines-w2.py`, etc.). W1 did not read or touch them.
