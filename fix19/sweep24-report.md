# Sweep #24 — fix program #19 fix-up round (hackathon-ecc), built-tree re-verification

**Verdict: CLEAN — 0 blocking / 0 minor.** Every re-derived number matches
the fix-up manifest. Sweep #23 MINOR-1 is CLOSED: all 51 Hallmark theme
files now carry named faces only on every `--font-*` declaration line (90
lines checked, 0 tails). The fix-up's other claims also verify: `build.sh`
byte-identical (23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`),
banned terms 0 in the built tree, Grok pins unchanged, all four fix19 rules
identical across their full-rule placements with md5s matching sweep #23,
STATIC19 identical ×3, canonical block verbatim ×1 in all 11 files, counts
unchanged, `system-ui` total still 161 with the same class breakdown, and
all four verifiers re-run green by this sweep. One observation (OBS-1, not
a finding): a live-run artifact file, `.taste-skill/history.json`, sits in
the built tree outside the 25 fix-up files — runtime state from the
fix-up's live `start.mjs` verification, not a plugin file.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`,
`node_modules/` excluded everywhere; plus `build.sh` and the staged sources
`new-skills/`, `rewritten-skills/`, `round2-skills/`, `new-rules/`,
`~/workspace/cursor-skills/less-flat-ui/SKILL.md`. SPEC read first:
`~/workspace/hackathon-plugin/fix19/SPEC.md`; MANIFEST, inventory, and
fix-up engine read: `fix19/MANIFEST.md`, `fix19/inventory.md`,
`fix19/fix19_fixup.py`. Every number below was re-derived by running the
greps/commands shown; nothing was copied from the fix-up report without
re-running. This sweep made no plugin change (read-only); its only write
is this report.

**Given state (verified):** `build.sh` md5
`a8d3d3c6f6d32344d0168c5323d9364b`, 23,314 lines (matches the task brief);
`fix19/verify19.py` re-run by this sweep: **75/75 checks pass**.

---

## 1. Banned terms — 0 in the built tree — PASS, with two staged-source deviations (not findings)

Built tree (from `hackathon-ecc/`):
```
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
```
Result: **0 hits** (empty output). Re-derived independently in
`/tmp/sweep24.py` (walk of the whole built tree excl. `node_modules`):
**0 banned-term lines**.

Staged sources (same counts as sweep #23 — the fix-up touched none of
these files):

| Source | Banned-term lines | Disposition |
|---|---:|---|
| `new-skills/` | **0** | — |
| `round2-skills/` | **0** | — |
| `~/workspace/cursor-skills/less-flat-ui/SKILL.md` | **0** | — |
| `new-rules/` | **1** | `new-rules/hackathon-mode.mdc:38` — the upstream `` `claude -p` `` wording. Pre-existing fix16 staged/built drift, documented in sweep22 §5; the built side is scrubbed by `fix16.py` (build.sh:23204–23211 runs it as the last build step). Not a fix19 defect. |
| `rewritten-skills/` | **17** (all `claude`, 0 of any other term) | All in `rewritten-skills/app-scaffold/`: `SKILL.md` ×6, `reference/workflow.md` ×9, `reference/best-practices.md` ×1, `templates/package-scripts.json` ×1 — upstream "Claude Code" prose in the restored original skill. Same fix16 mechanism: `fix16/fix16.py` `generic_pass()` replaces `Claude Code`/`Claude-Code`/word-boundary `Claude` → `Cursor` tree-wide on the built tree. Verified: built `skills/app-scaffold/` grep = **0**. Not a fix19 defect; no staged source was touched by fix19 here. |

No fix19 addition contains a banned term: every fix19 constant in
`fix19/fix19.py` (`F2_RULE`, `F3_RULE`, `F4_RULE`, `D19_RULE`, `STATIC19`,
`C2_NEW`, `D19_ROUTING`, `D19_REVIEWER`, `POLISH_F19`, `TYPESET_F19`,
`TYPESET_CHECKBOX_NEW`, `LF_D19`, `F2_APP`, `F3_APP`, `F4_APP`, `D19_APP`,
`C1_APP_NOTE`, `START_MJS_NEW`, `THEME_MJS_NEW`, `SHOTS_SANS_NEW`) scans
0 for `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5`
(case-insensitive). The F4 rewording is confirmed in the placed text: the
title reads "**Plain/body text uses Tiempos (fix #19 F4).**" and the body
reads "Body and plain text use Tiempos (Klim, paid, NOT bundleable). The
canonical free stand-in is Fraunces, set at a 1.55 reading line-height."
— no "Anthropic", no "Claude", all functional facts kept (Tiempos, Klim,
paid, NOT bundleable, Fraunces stand-in, 1.55).

## 2. Grok pins unchanged — PASS (match fix16 MANIFEST exactly)

| String | Occurrences | Lines |
|---|---:|---:|
| `grok-4.7-high` | 52 | 45 |
| `cursor-grok-4.6-high-fast` | 100 | 99 |

Commands (from `hackathon-ecc/`):
```
grep -ro 'grok-4.7-high' --exclude-dir=node_modules . | wc -l              # 52
grep -r 'grok-4.7-high' --exclude-dir=node_modules . | wc -l               # 45
grep -ro 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l  # 100
grep -r 'cursor-grok-4.6-high-fast' --exclude-dir=node_modules . | wc -l   # 99
grep -rP '(?<!cursor-)grok-4\.6-high-fast' --exclude-dir=node_modules . | wc -l  # 0
grep -r 'grok-4\.7\[' --exclude-dir=node_modules . | wc -l                 # 0
grep -r 'grok-4\.6\[' --exclude-dir=node_modules . | wc -l                 # 0
grep -r 'effort=' --exclude-dir=node_modules . | wc -l                     # 0
grep -ro 'reasoning_effort' --exclude-dir=node_modules . | wc -l           # 2
grep -rn 'Grok 4.7 High \[0-9\]\|Grok 4.6 High Fast \[0-9\]' --exclude-dir=node_modules . | wc -l  # 0
```

`reasoning_effort` (2 occ / 2 lines): `rules/common-performance.mdc` and
`skills/orchestrate/SKILL.md:160`-region — the same two lines as sweep #22
and sweep #23. No pin drift.

## 3. Fix #19 rule-text identity — PASS (md5s match sweep #23 exactly)

Constants imported from `fix19/fix19.py`; counts are `text.count(constant)`
in the built files; md5s are of the constant text. The fix-up did NOT
change F2's text (its F2 change is the procedural instancing step, not the
rule), and all four md5s match sweep #23.

| Rule | md5 | Taste | Orchestrate | ui-ux-pro-max | orch-build-mvp |
|---|---|---:|---:|---:|---:|
| F2_RULE (1845 chars) | `5ca43e60866aa11f6eca80647c455280` | 1 | 1 | — | — |
| F3_RULE (872 chars) | `1e7d03034ed4c57f9ce4d0536f73ec50` | 1 | 1 | — | — |
| F4_RULE (1002 chars) | `9468eba62050011de12d882475ce6411` | 1 | 1 | — | — |
| D19_RULE (2090 chars) | `f97c569f4ce53fd9a5d351cc0bed52dd` | 1 | 1 | — | — |
| STATIC19 (1162 chars) | `130a988e85e82ad1b75d1bec74fb3bb6` | 1 | 1 | — | 1 |
| F2_APP | `3babd65b4f368dbb0aebc2c81cff62a4` | — | — | 1 | — |
| F3_APP | `13538e3754bc6c28ade62de3fe121623` | — | — | 1 | — |
| F4_APP | `b1425eda6050bb6425e141ff3175f9fb` | — | — | 1 | — |
| D19_APP | `3ab424b65bd3dfbc4b62d00d85f3d961` | — | — | 1 | 1 |

App mirrors are intentionally different from the full rules (MASTER.md home
instead of `docs/design-tokens.md`, plus the pointer "The full F2/F3/F4/D19
rule lives in `design-taste-frontend` step 4a") — recorded as specified, not
as drift. D19_APP is identical across its two placements (ui-ux-pro-max and
orch-build-mvp, same md5).

Other fix19 placements (all count 1, all in the expected file):
- `C2_NEW` in Taste step 4a (line 246); the old C2 sentence is gone:
  `body faces name their source (self-hosted or link) and fallback stack`
  tree-wide **0**.
- `C1_APP_NOTE` in ui-ux-pro-max: 1.
- `D19_ROUTING` in orchestrate (:100 region): 1; `D19_REVIEWER` in
  orchestrate (:195 region): 1. (The old routing/reviewer sentences remain
  as the prefix the extensions append to — expected.)
- `POLISH_F19` in polish-pass harmony: 1.
- `TYPESET_F19` in `polish-pass/reference/lenses/typeset.md`: 1;
  `TYPESET_CHECKBOX_NEW`: 1. The replaced sentence is gone:
  `legitimate default with` tree-wide **0**; the old checkbox
  `variable fonts use \`font-optical-sizing: auto\`` tree-wide **0**.
- `LF_D19` in standalone `less-flat-ui/SKILL.md`: 1; in the built copy: 1.

Fix-up additions (all count 1, all in the expected file — the fix-up's
new text, verified present, not just claimed):
- `INSTANCE_STEP` ("Instance the dealt faces to static files before
  shipping (fix #19 F2 — the instancing step)") in Taste built: 1.
- Taste `:root` carve-out ("Keep the `:root` block as printed, except the
  font delivery") in Taste built: 1.
- `start.mjs` header carve-out ("except the font delivery") staged: 1.
- `layout-v4.md` carve-outs staged: "except the font delivery" 1, "only
  as the generation source (fix #19 F2)" 1.

## 4. No fix19 residues — PASS

- `may invent` tree-wide: **0**.
- "Anthropic" / "Claude" in any fix19 rule text (constants + placed text): **0**
  (§1). The rewording dropped both tokens; no staged or built file reintroduces
  them in fix19 text.
- Stale C2 sentence: **0** (§3). Old system-ui-legitimising sentence: **0** (§3).
- `Tiempos` tree-wide: 22 occurrences, all inside fix19 rule text (F4, STATIC19,
  C1_APP_NOTE) — no catalogue entries added, per SPEC §9 (Fraunces/Tiempos are
  named in rule text only). Same count as sweep #23.

## 5. Theme tail-strip verification — PASS (sweep #23 MINOR-1 CLOSED)

Re-derived from scratch over all 51 theme files in the built tree
(`skills/design-taste-frontend/references/hallmark/references/themes/*.md`),
checking every `--font-*` declaration line against the fix-up's
`THEME_TAILS` list (`', system-ui'`, `', ui-sans-serif'`, `', ui-serif'`,
`', ui-monospace'`, `', ui-rounded'`, `', sans-serif'`, `', serif'`,
`', monospace'`):

| Check | Result |
|---|---:|
| Theme files | 51 |
| `--font-*` declaration lines | 90 |
| Lines still carrying a generic/system tail | **0** |
| Any `--font-` line with a tail (incl. non-declaration) | **0** |
| `system-ui` in theme files | **0** |
| Empty `--font-` declarations (face lost by the strip) | **0** |

Spot check of the sweep #23 MINOR-1 exemplar: `darkroom.md:27` now reads
`--font-display: "Sofia Sans Extra Condensed"; --font-body: "Barlow";`
— the `ui-sans-serif, sans-serif` tails are gone, the named faces kept.
The 20 files the fix19 strip never touched (arcade, blueprint, broadside,
darkroom, dose, editorial, formwork, halftone, hum, newsprint, overprint,
pasteup, piste, riso, solstice, sport, terminal, terrazzo, vellum,
wayfind — the exact 20 named in `fix19_fixup.py:EXPECTED_UNSTRIPPED`) all
verify clean, as do the 30 originally stripped files. The strip also
removed the non-`system-ui` tails from the originally stripped files
(e.g. `sticker.md:28–29`, unchanged from sweep #23). No declaration lost
its face: every line still names a face (or a `var()`).

MINOR-1 is therefore closed with no residual: the Tokens blocks of all 51
themes now satisfy the placed F2 rule (no bare generic / `ui-*` fallback
as a live path).

## 6. Canonical block identical ×1 in all 11 files — PASS

`CANONICAL` imported from `fix15/fix15.py`: md5
`673ab869558822a8592886716a8fdac7`, 692 chars. `text.count(CANONICAL) == 1`
in all 11: `design-taste-frontend/SKILL.md`, `ui-ux-pro-max/SKILL.md`,
`polish-pass/SKILL.md`,
`design-taste-frontend/references/hallmark/references/hallmark-floor.md`,
`make-interfaces-feel-better/SKILL.md`, `motion-foundations/SKILL.md`,
`motion-patterns/SKILL.md`, `motion-advanced/SKILL.md`,
`orchestrate/SKILL.md`, `orch-build-mvp/SKILL.md`, and standalone
`less-flat-ui/SKILL.md`.

Fix #17 anchors intact (re-derived): E1_RULE md5
`e9d2102572611fe7a6ba507b961013b2` (matches the fix17 baseline md5), count 1
in each of the four placements (Taste, orchestrate, orch-build-mvp,
ui-ux-pro-max). Sticker exceptions A+B present (`sticker.md:90–91`).
less-flat-ui treatments still exactly 1..23 (headings `### 1.` through
`### 23. Soft shadow`, in both the standalone file and the built copy).

## 7. `system-ui` inventory — PASS (161 remaining, classes match the manifest)

Fresh totals, built tree excl. `node_modules`:

| Class | Occurrences | How counted |
|---|---:|---|
| `skills/design-taste-frontend/assets/` demo HTML/CSS | 129 | `grep -ro system-ui skills/design-taste-frontend/assets` |
| Dev/QA tooling pages | 12 | Per-file: `fx-gallery.template.html` 2, `fx-lab.template.html` 1, `moments.mjs` 3, `sloplint-render.mjs` 1, `control-plane-view-ui.js` 2, `proximity-viz.js` 2, `ui.js` 1 |
| Detectors (must keep) | 3 | `sloplint.mjs` 2, `consistency.mjs` 1 |
| Reference data | 3 | `skills/ui-ux-pro-max/data/styles.csv` 3 |
| `*.md` rule-text mentions (the fix19 rules naming the ban) | 14 | Taste 5, orchestrate 4, typeset lens 2, orch-build-mvp 1, polish-pass 1, ui-ux-pro-max 1 |
| **Total** | **161** | `grep -ro system-ui` tree-wide = 161; 129+12+3+3+14 = 161 ✓ |

Theme files: `system-ui` **0** (all 51 theme files). Shipping templates:
`start.mjs`, `theme.mjs`, `shots.json`, `shots.example.json` — **0** each.
The fix-up did not move the total, as claimed: it removed generic tails,
not `system-ui` — the only literal `system-ui` the fix-up could have added
would be in new text, and the new INSTANCE_STEP / carve-out texts contain
none (verified: the `*.md` mention count is still exactly 14).

## 8. build.sh exception inventory re-derived — delta 0 vs sweep #23 — PASS

- `md5sum build.sh` → `a8d3d3c6f6d32344d0168c5323d9364b`, **23,314 lines**
  (was 23,276; +38 = the fix19 block, lines 23267–23304, marker
  `# --- fix19: font identity, forced font choice, Tiempos body font,
  thought-out decisions (F2/F3/F4/D19) ---` at :23267). The fix-up did
  not edit build.sh: md5 and line count are unchanged from sweep #23.
- Fresh banned-term line count: `grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh` → **798 lines**.
- Re-derivation: parsed the 798-row inventory table in
  `fix16/sweep18-report.md` (§Check 16) and cross-checked its line-number
  set against a fresh `grep -in` of `build.sh`. The two sets are
  **identical — no missing, no extra lines** (798 rows, line range
  150–23204, no duplicate line numbers).
- Category counts from the table's class column: **(a) OLD-side 389, (b)
  comment 52, (c1) NEW-side transient 355, (c2) heredoc 0, (c3) build-time
  `.claude/skills/` paths 2** (`:265`, `:298` — the two `cp -r …/.claude/skills/…`
  lines) — identical to the sweep #18 baseline and to sweep #23.
- Per-term line counts (fresh grep): `claude` 701, `codex` 103, `anthropic` 5,
  `opus` 22, `sonnet` 23, `haiku` 13, `composer-2.5` 0 — identical to the
  sweep22/sweep23 baseline. Per-term occurrence counts: `claude` 930,
  `codex` 126, `anthropic` 8, `opus` 26, `sonnet` 24, `haiku` 13.
- **Delta vs sweep #23: 0.** The fix19 block contains **zero** banned-term
  lines (max banned line is 23204, the fix16 block header — the fix19 block
  at 23267–23304 sits after every banned line, so no line numbers shifted).
  build.sh still contains the fix15 and fix17 block markers (verify19
  checks 10/11 assert this; fix18 has no build.sh block, per MANIFEST §3
  deviation 6).

## 9. Counts — PASS

| Inventory | Count | Command |
|---|---:|---|
| skills | **166** | `ls skills \| wc -l` |
| agents | **72** | `ls agents \| wc -l` |
| rules | **123** | `ls rules \| wc -l` |
| commands | **87** | `ls commands \| wc -l` |
| hooks | **15** | `python3 -c "len(json.load(open('hooks/hooks.json'))['hooks'])"` |

## 10. Verifiers re-run by this sweep — all green

| Verifier | Result |
|---|---:|
| `fix15/verify15.py` | **43/43 checks pass** |
| `fix17/verify17.py` | **59/59 checks pass** |
| `fix18/verify18.py` | **72/72 checks pass** |
| `fix19/verify19.py` | **75/75 checks pass** |

## 11. Staged-vs-built diffs and the fix-up's 25-file claim — PASS, with one observation

`diff -q` staged → built for the nine fix19/fix-up staged files:

| File | Result |
|---|---|
| `new-skills/orchestrate/SKILL.md` | IDENTICAL |
| `round2-skills/polish-pass/reference/lenses/typeset.md` | IDENTICAL |
| `new-skills/design-taste-frontend/scripts/start.mjs` | IDENTICAL |
| `new-skills/design-taste-frontend/references/hallmark/scripts/theme.mjs` | IDENTICAL |
| `new-skills/pitch-deck-video/template/shots.json` | IDENTICAL |
| `new-skills/pitch-deck-video/template/shots.example.json` | IDENTICAL |
| `new-skills/design-taste-frontend/references/layout-v4.md` | IDENTICAL |
| `new-skills/design-taste-frontend/SKILL.md` | DIFFERS — 1 hunk only (lines 9–13, frontmatter description) |
| `round2-skills/polish-pass/SKILL.md` | DIFFERS — 4 hunks only (lines 3, 15, 24, 31) |

Both diffs are the same pre-existing build.sh patch blocks as sweep #23,
not fix19/fix-up: the Taste hunk is the `replace_text("design-taste-frontend", …)`
"Use ONLY for a full company or landing-page build from scratch…"
description replacement at `build.sh:606–614`; the polish-pass hunks are
block "(f) polish-pass: the new-look rule also names Taste" at
`build.sh:~759`. Both built-side strings are present in
`build.sh.before-fix19` (grep count 1 each), so they predate fix19. The
built side is the intended side; the fix19-relevant regions match
(§3 counts). Same class as sweep22 §5's `hackathon-mode.mdc` deviation.
Theme files staged-vs-built: **0 mismatches** across all 51 files.

**Fix-up 25-file claim — verified for plugin files.** Regenerated the
tree manifest (`cd hackathon-ecc && find . -type f -not -path
'./node_modules/*' | sort | xargs sha256sum`) and diffed it against the
pre-fix-up `fix19/manifest1.txt` (2665 lines). Exactly **25 files
changed** (old hash + new hash each): Taste `SKILL.md`,
`layout-v4.md`, `start.mjs`, `shots.json`, `shots.example.json`, and the
20 theme files — precisely the fix-up's claimed set. No other plugin
file moved.

**OBS-1 (observation, not a finding):** the manifest diff shows one
additional path present only in the current tree:
`skills/design-taste-frontend/.taste-skill/history.json` (292 bytes,
created Nov 12 02:26–02:27). It is runtime state written by a live
`start.mjs` run — its contents (`"palettes": ["white-link-blue" ×6]`,
`"types": ["fraunces" ×4, "instrument" ×2]`, `"dealt": []`) match the
fix-up's live verification ("`types` over all 6 pages"), not a plugin
source. It is absent from both `fix19/manifest1.txt` and
`fix19/manifest2.txt`, and `build.sh` does not produce it, so it is not
one of the 25 fix-up files and not a plugin change. It is harmless, but
it means the built tree now contains one file the build does not
reproduce; the next full rebuild (or a `rm` of the `.taste-skill/`
directory) clears it. Not counted as a finding because it is not a
plugin defect, a pin, a count, or rule-text drift.

**Fix-up MINOR-2 (audit #60) spot-verified in the built tree:**
`start.mjs` — `axisVal`/`axisOrder`/`isLower` all 0, `e.variable` 0,
`expandWeights` present (2 refs), zero `'..'`/`".."` literals in the
`fontLink` function body, mono system tails (`ui-monospace`,
`SFMono-Regular`, `Menlo`) all 0, mono stack now
`` `"${monoOf(t).family}"` `` alone. `shots.json` and
`shots.example.json` (JSON re-validated by this sweep): fonts
`sans: "Hanken Grotesk"`, `serif: "Instrument Serif"`,
`mono: "JetBrains Mono"` — named bundled faces only, in both files.

## Commands used (full list)

```
md5sum build.sh ; wc -l build.sh
python3 fix19/verify19.py ; python3 fix15/verify15.py ; python3 fix17/verify17.py ; python3 fix18/verify18.py
python3 /tmp/sweep24.py  (banned-term walk built tree + staged sources + fix19 constants; grok pin counts; F2/F3/F4/D19/STATIC19/app-mirror counts + md5s from fix19.py; CANONICAL counts + md5 from fix15.py; E1 md5/counts from fix17.py; theme decl-line tail check over all 51 files; system-ui class breakdown; counts; fix-up claim checks; staged-vs-built diffs)
grep -rn 'may invent' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rn 'body faces name their source (self-hosted or link) and fallback stack' / 'legitimate default with' / 'variable fonts use `font-optical-sizing: auto`' --exclude-dir=node_modules hackathon-ecc
grep -c 'system-ui' hackathon-ecc/skills/design-taste-frontend/scripts/start.mjs hackathon-ecc/skills/design-taste-frontend/references/hallmark/scripts/theme.mjs hackathon-ecc/skills/pitch-deck-video/template/shots.json hackathon-ecc/skills/pitch-deck-video/template/shots.example.json
grep -n 'fix19:' build.sh
diff new-skills/design-taste-frontend/SKILL.md hackathon-ecc/skills/design-taste-frontend/SKILL.md ; diff round2-skills/polish-pass/SKILL.md hackathon-ecc/skills/polish-pass/SKILL.md
(cd hackathon-ecc && find . -type f -not -path './node_modules/*' | sort | xargs sha256sum > /tmp/sweep24-manifest-now.txt) ; diff fix19/manifest1.txt /tmp/sweep24-manifest-now.txt
python3 (sweep18 table parse: 798 rows, classes a389/b52/c1 355/c3 2; fresh grep -in line-set comparison → identical; per-term line + occurrence counts)
grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh ; per-term grep counts
grep -c '^### [0-9]' hackathon-ecc/skills/less-flat-ui/SKILL.md ; grep '^### 23\.' hackathon-ecc/skills/less-flat-ui/SKILL.md
ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l ; python3 -c "import json; print(len(json.load(open('hooks/hooks.json'))['hooks']))"
```
