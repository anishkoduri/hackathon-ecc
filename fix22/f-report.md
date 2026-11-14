# Fix #22 — Group F verification report (backgrounds, verification only)

Scope: SPEC §3, Group F — verify only, no new plugin text. Method: word-boundary greps; every hit inspected (hyphen-joined compounds do not count). All file:line references are against the current tree on Nov 12, 2026. Baseline confirmed: `build.sh` = 23,647 lines (verify15 re-ran 44/44 PASS during this check, including the R3 assertion).

## Verdicts

- (a) less-flat-ui contents check — **PASS**: all 22 treatments + #23 Soft Shadow present.
- (b) Plugin references to less-flat-ui — **PASS**: every reference points at the skill and its 23 treatments; no stale count, no wrong path.
- (c) Fix #15 R3 enforcement — **PASS with one observation**: the rule text is live and build-time-checked (verify15 PASS); see §c for the exact enforcement chain and the observation.

## (a) less-flat-ui contents check

Skill file (standalone global skill, outside the plugin): `~/workspace/cursor-skills/less-flat-ui/SKILL.md`.
Per-item locations are in `fix22/disposition-F.md` (one row per item, 23/23 verified). Summary:

- Frontmatter `SKILL.md:3` states "23 textured treatments"; source line `:8` states "Source of the 23 treatments" (22 from the @charles.unemployed reel + Soft Shadow from the @lnunesdesigns reel).
- Catalogue heading `## The 23 treatments` at `SKILL.md:101` (global) / `hackathon-ecc/skills/less-flat-ui/SKILL.md:104` (built).
- Headings `### 1.`–`### 23.` present in order in both the global file (lines 103–484) and the built copy (lines 107–488; +4 offset from the two patch insertions at the top of the file).
- Built copy vs global file: `diff` shows exactly the 4 documented patch hunks (weave20 design-decision pointer, wow-moment rule, design-tokens record line, re-tint warning). `fix15/verify15.py` patch checks 1–4 all PASS, and its "treatments still number 1..23 exactly" check PASSes.
- No treatment text was copied into the plugin for Group F. Nothing to duplicate; the catalogue lives only in the skill.

## (b) Plugin references to less-flat-ui

Full grep saved at `fix22/grep-lessflatui-F.txt` (87 hits across `build.sh`, `new-skills/`, `round2-skills/`, `hackathon-ecc/`). Every hit was inspected. All references name the skill `less-flat-ui` as the texture layer; none states a treatment count other than 23, and none points at a wrong path. Stale-count scan: zero hits for "22 treatments" / "22-entry" / "22 backgrounds" / "twenty-two" in the live tree (`build.sh`, staged sources, `hackathon-ecc/`). The only "22" in the live tree is the reel title itself ("22 Backgrounds to Make Designs Less Flat"), which is correct — the reel had 22, Soft Shadow is the 23rd. ("22 treatments" does appear in frozen historical backup/audit dirs, e.g. `hackathon-plugin-fixed-backup-audit4/`, `audit9-quality/` — pre-#23 snapshots, not live plugin files; not pointer fixes.)

Key references (design-package routing — the ones that matter for Group F):

| Location | What it says | Verdict |
|---|---|---|
| `build.sh:17` | Header comment: `less-flat-ui ............ ~/workspace/cursor-skills/less-flat-ui` | correct path |
| `build.sh:112` | Plugin description lists `less-flat-ui` among UI skills | correct |
| `build.sh:256-258` | Comment + `cp -r "$HOME/workspace/cursor-skills/less-flat-ui" "$PLUGIN_DIR/skills/less-flat-ui"` — the copy step that puts the skill into the built tree | correct; this is how the 23 treatments reach the built tree |
| `build.sh:22193` | Orchestrate design-package rule (row 10): app/dashboard/components get `less-flat-ui` where dull/flat; landing gets Taste + `ui-ux-pro-max` | correct |
| `build.sh:22204, 22272-22273, 22681, 22686, 22692` | UI-change / rebuild-a-surface rules in orch-* skills: same design-package routing with `less-flat-ui` where dull/flat | correct |
| `build.sh:20967-20999` | Batch E patch: "texture in service of the wow moment" applied to `skills/less-flat-ui/SKILL.md` | correct |
| `build.sh:22062, 22066` | W2-G9 patches touching `skills/less-flat-ui/SKILL.md` (re-tint warning, record line) | correct |
| `build.sh:22127` | Trigger keys: `"skill:less-flat-ui": ["add texture to the ui", "less flat ui", "depth and texture"]` | correct |
| `build.sh:23399-23400` | Weave20 A10: design-decision pointer inserted into `skills/less-flat-ui/SKILL.md` after "Never skip the check because a surface is small." | correct |
| `build.sh:23152, 23217, 23274` | Fix-program comments naming less-flat-ui as a fix15/fix17/fix19 target | correct |
| `build.sh:758-771, 10086, 16921, 18344` | polish-pass scope routing ("a new look belongs to ui-ux-pro-max and less-flat-ui"), install-modules list (`skills/less-flat-ui`), README text (texture layer on non-landing UI) | correct |
| `new-skills/orchestrate/SKILL.md:62, 96, 98, 110, 128` | Slice-brief design package, routing table row 10, design-package rule, D19 Texture dimension, anti-derivative rule — all name `less-flat-ui` as the texture layer | correct |
| `new-skills/orchestrate/references/dispatch-prompt.md:24` | Dispatch design package names `less-flat-ui` where dull/flat | correct |
| `new-skills/design-taste-frontend/SKILL.md:81-84, 248, 264` | Texture boundary: `less-flat-ui` applies only where the Taste page system leaves a surface unstyled; U1/D19 mentions | correct |
| `new-skills/feature-expansion/SKILL.md:148, 192` | UI rule: full design package = `ui-ux-pro-max` + `less-flat-ui` + Impeccable via polish-pass + Harmony | correct |
| `new-skills/integration/SKILL.md:107, 122` | Integration UI goes through `ui-ux-pro-max` + `less-flat-ui` together | correct |
| `round2-skills/polish-pass/SKILL.md:3, 15, 32` | Scope: a new look belongs to `ui-ux-pro-max` and `less-flat-ui`, not polish-pass | correct |
| `hackathon-ecc/skills/orchestrate/SKILL.md:62, 96, 98, 110, 128` | Built-tree copies of the staged orchestrate references above | correct |
| `hackathon-ecc/skills/polish-pass/SKILL.md:3, 15, 25, 32` | Built-tree polish-pass scope routing | correct |
| `hackathon-ecc/skills/design-taste-frontend/SKILL.md:82, 84, 249` | Built-tree texture boundary + U1 | correct |
| `hackathon-ecc/skills/orch-add-feature/SKILL.md:33`, `orch-build-mvp/SKILL.md:41`, `orch-change-feature/SKILL.md:36`, `orch-fix-defect/SKILL.md:36`, `orch-refine-code/SKILL.md:35`, `feature-expansion/SKILL.md:148, 192`, `integration/SKILL.md:107, 122` | Built-tree UI-change / UI-rule routing, all naming `less-flat-ui` where dull/flat | correct |
| `hackathon-ecc/rules/hackathon-mode.mdc:18, 31, 34, 35, 49` | §5 routing: non-landing UI uses `ui-ux-pro-max` + `less-flat-ui` together; Taste builds use the texture layer only on unstyled surfaces; "`less-flat-ui` owns the lightweight texture layer for any surface." | correct |
| `hackathon-ecc/rules/ponytail.mdc:13` | UI direction set by `ui-ux-pro-max` + `less-flat-ui` pairing (or Taste on landing pages) | correct |
| `hackathon-ecc/.cursor-plugin/plugin.json:4`, `hackathon-ecc/README.md:20`, `hackathon-ecc/manifests/install-modules.json:410`, `hackathon-ecc/manifests/context-packs/skill-triggers@1.json:256`, `hackathon-ecc/skills/less-flat-ui/SKILL.md:2` | Plugin description, README texture-layer line, install list, trigger keys, skill frontmatter `name: less-flat-ui` | correct |

No reference is missing where the design-package routing should name the texture layer: orchestrate row 10, the design-package rule, the dispatch prompt, the UI-change rules in all five orch-* skills, feature-expansion, integration, hackathon-mode §5, and the README all name it.

## (c) Fix #15 R3 enforcement

Rule text (exact wording, as it stands in the skill):

> "On app/dashboard surfaces, at least TWO DISTINCT treatment kinds must be recorded per screen, or "none — <reason>" per untreated surface (fix #15 R3 — baseline: 2 treatment applications, both Soft Shadow, one kind). The second kind must be theme-matched (rule A governs the choice) — do not hard-code which kind, only that a second distinct kind is required. A theme-matched handmade surface treatment — tape, perforation, washi, a hand-drawn ink mark — counts as a treatment kind (fix #17): the kind is the treatment application on one surface, not the catalogue entry; the 23-entry catalogue is the vocabulary, not the limit."

Locations of the rule text:

- `~/workspace/cursor-skills/less-flat-ui/SKILL.md:14` (standalone global skill, "Check every surface" paragraph).
- `~/workspace/hackathon-plugin/hackathon-ecc/skills/less-flat-ui/SKILL.md:15` (built copy; same paragraph, preceded on the same line by the weave20 design-decision pointer insertion).
- Rule source: `~/workspace/hackathon-plugin/fix15/fix15.py:118-121` — the fix #15 R3 patch, applied to the standalone global skill file (fix15.py header line 19: `less-flat-ui/SKILL.md ... A, R3 (surface check)`). It is NOT in `build.sh` text and NOT in any staged source under `new-skills/` or `round2-skills/` — the rule reaches the built tree via the `build.sh:256-258` copy of the global skill, not via an embedded patch. That is the intended mechanism (the global skill is the source of truth for less-flat-ui).

The check — live, not a comment:

1. **Build-time verifier, executed during this check:** `fix15/verify15.py:141-142` asserts `"at least TWO DISTINCT treatment kinds must be recorded per screen" in lessflat` for the built skill. Ran `python3 fix15/verify15.py` (read-only): **PASS** — "PASS R3: two distinct treatment kinds per app screen (less-flat-ui)", 44/44 checks pass overall, including "less-flat-ui treatments still number 1..23 exactly" and "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks".
2. **Runtime record:** `less-flat-ui/SKILL.md:527` (global) / `hackathon-ecc/skills/less-flat-ui/SKILL.md:531` (built) — "Record what you applied": every treatment applied is recorded per surface in `docs/design-tokens.md` as a Treatments list (surface → treatments applied, or "none — <Do NOT reason>"), "so the polish-pass harmony check can verify the texture layer against the recorded direction"; handmade treatments "count toward the two-distinct-kinds check"; each recorded treatment carries the six D19 dimension lines.
3. **D19 cross-check:** the harmony rule verifies every decision-record entry carries all six D19 dimension lines including Texture (what less-flat-ui treatment it carries, or `none — <reason>`) — `round2-skills/polish-pass/SKILL.md:22`, and the D19 rule in `new-skills/orchestrate/SKILL.md:110` / `new-skills/design-taste-frontend/SKILL.md:264` (built copies at the same lines in `hackathon-ecc/`).

Observation (not a pointer fix — for the coordinator to adjudicate): the polish-pass harmony rule text (`round2-skills/polish-pass/SKILL.md:22`) verifies tokens/type/color/radii/spacing, the Type list, D19 reasons, font scope, and brand identity, but it does not name the Treatments list or the two-distinct-kinds count explicitly. The R3 count is therefore enforced by (1) the skill's own mandatory recording instruction, (2) the D19 Texture-dimension check on the record, and (3) the build-time verify15 assertion — not by a step-6 check sentence that counts kinds per screen. No "fix #15 R3" string exists anywhere in the plugin outside the less-flat-ui skill itself (word-boundary grep for `R3` in `build.sh` finds only a fix17 comment at `build.sh:23214` about "R3 widening"; in the built tree, only `hackathon-ecc/skills/less-flat-ui/SKILL.md:15`). If the coordinator wants the count named in the harmony rule, that is new rule text, not a pointer fix, and is out of Group F scope — flagging it here only.

## Pointer fixes needed

**None.** No reference is missing, stale, or mis-pointed. No file needs a pointer change for Group F.

## Files delivered

- `~/workspace/hackathon-plugin/fix22/disposition-F.md` — 23 rows (F1–F22 + #23), each with global + built-tree file:line, all verified.
- `~/workspace/hackathon-plugin/fix22/f-report.md` — this report.
- Intermediate (kept in fix22/, not /tmp): `~/workspace/hackathon-plugin/fix22/grep-lessflatui-F.txt` — full 87-hit grep of `less-flat-ui` across `build.sh`, `new-skills/`, `round2-skills/`, `hackathon-ecc/`.
