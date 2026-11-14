# Sweep #23 — fix program #19 (hackathon-ecc), built-tree re-verification

**Verdict: NOT CLEAN — 0 blocking / 1 minor.** Every re-derived number matches
the implementation report except one residue the fix19 scope did not cover:
20 Hallmark theme files (31 `--font-*` declaration lines in their Tokens
blocks) still carry bare-generic / `ui-*` tails — pre-existing, byte-identical
to the pre-fix15 copy, but now in direct tension with the placed F2 rule text,
which bans bare generic fallbacks as a live path in exactly those Tokens
blocks. Finding MINOR-1 below, with file:line evidence and the one-line fix
(extend the existing tail strip to those 20 files). Everything else passes:
banned terms 0 in the built tree, Grok pins unchanged, all four fix19 rules
identical across their full-rule placements, STATIC19 identical ×3, canonical
block verbatim ×1 in all 11 files, counts unchanged, all four verifiers
re-run green by this sweep.

**Scope:** built tree `~/workspace/hackathon-plugin/hackathon-ecc/`,
`node_modules/` excluded everywhere; plus `build.sh` and the staged sources
`new-skills/`, `rewritten-skills/`, `round2-skills/`, `new-rules/`,
`~/workspace/cursor-skills/less-flat-ui/SKILL.md`. SPEC read first:
`~/workspace/hackathon-plugin/fix19/SPEC.md`; MANIFEST and inventory read:
`fix19/MANIFEST.md`, `fix19/inventory.md`. Every number below was re-derived
by running the greps/commands shown; nothing was copied from the fix19
implementation report without re-running. This sweep made no plugin change
(read-only); its only write is this report.

**Given state (verified):** `build.sh` md5
`a8d3d3c6f6d32344d0168c5323d9364b`, 23,314 lines (matches the task brief);
`fix19/verify19.py` re-run by this sweep: **75/75 checks pass**.

---

## 1. Banned terms — 0 in the built tree — PASS, with two staged-source deviations (not findings)

Built tree (from `hackathon-ecc/`):
```
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md
```
Result: **0 hits** (empty output).

Staged sources:

| Source | Banned-term lines | Disposition |
|---|---:|---|
| `new-skills/` | **0** | — |
| `round2-skills/` | **0** | — |
| `~/workspace/cursor-skills/less-flat-ui/SKILL.md` | **0** | — |
| `new-rules/` | **1** | `new-rules/hackathon-mode.mdc:38` — the upstream `` `claude -p` `` wording. Pre-existing fix16 staged/built drift, documented in sweep22 §5; the built side is scrubbed by `fix16.py` (build.sh:23204–23211 runs it as the last build step). Not a fix19 defect. |
| `rewritten-skills/` | **17** (all `claude`, 0 of any other term) | All in `rewritten-skills/app-scaffold/`: `SKILL.md` ×6, `reference/workflow.md` ×9, `reference/best-practices.md` ×1, `templates/package-scripts.json` ×1 — upstream "Claude Code" prose in the restored original skill. Same fix16 mechanism: `fix16/fix16.py` `generic_pass()` (lines ~1230–1270) replaces `Claude Code`/`Claude-Code`/word-boundary `Claude` → `Cursor` tree-wide on the built tree. Verified: built `skills/app-scaffold/` grep = **0**, and the staged-vs-built diffs of all four files are exactly those substitutions (e.g. "Recommended Claude Code workflow" → "Recommended Cursor workflow", "have Claude write it" → "have Cursor write it"). Not a fix19 defect; no staged source was touched by fix19 here. |

No fix19 addition contains a banned term: every fix19 constant in
`fix19/fix19.py` (`F2_RULE`, `F3_RULE`, `F4_RULE`, `D19_RULE`, `STATIC19`,
`C2_NEW`, `D19_ROUTING`, `D19_REVIEWER`, `POLISH_F19`, `TYPESET_F19`,
`TYPESET_CHECKBOX_NEW`, `LF_D19`, `F2_APP`, `F3_APP`, `F4_APP`, `D19_APP`,
`C1_APP_NOTE`, `START_MJS_NEW`, `THEME_MJS_NEW`, `SHOTS_SANS_NEW`) scans
0 for `claude|codex|anthropic|opus|sonnet|haiku|composer-2.5` (case-insensitive).
The F4 rewording is confirmed in the placed text: the title reads
"**Plain/body text uses Tiempos (fix #19 F4).**" and the body reads
"Body and plain text use Tiempos (Klim, paid, NOT bundleable). The canonical
free stand-in is Fraunces, set at a 1.55 reading line-height." — no
"Anthropic", no "Claude", all functional facts kept (Tiempos, Klim, paid,
NOT bundleable, Fraunces stand-in, 1.55).

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
`skills/orchestrate/SKILL.md:160`-region — the same two lines as sweep #22.

## 3. Fix #19 rule-text identity — PASS

Constants imported from `fix19/fix19.py`; counts are `text.count(constant)`
in the built files; md5s are of the constant text.

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
- `LF_D19` in standalone `less-flat-ui/SKILL.md`: 1.

## 4. No fix19 residues — PASS

- `may invent` tree-wide: **0**.
- "Anthropic" / "Claude" in any fix19 rule text (constants + placed text): **0**
  (§1). The rewording dropped both tokens; no staged or built file reintroduces
  them in fix19 text.
- Stale C2 sentence: **0** (§3). Old system-ui-legitimising sentence: **0** (§3).
- `Tiempos` tree-wide: 22 occurrences, all inside fix19 rule text (F4, STATIC19,
  C1_APP_NOTE) — no catalogue entries added, per SPEC §9 (Fraunces/Tiempos are
  named in rule text only).

## 5. Theme tail-strip verification — MINOR-1 (see finding)

Re-derived from scratch, including against the pre-fix19 copy
`~/workspace/hackathon-plugin-repo/` (build.sh 23,160 lines, pre-fix15 vintage;
its theme files carry exactly the fix19 preflight numbers: 30 files with
`system-ui`, 39 occurrences).

**The 30 stripped files — PASS.** All 30 files that contained `system-ui`
pre-fix19 now carry named faces only on every `--font-*` declaration line:
57 declaration lines checked, **0 with a generic tail**. Proof by replay:
applying `fix19.py:strip_theme_tails` to the repo copy reproduces the current
file byte-identically for 29 of the 30; the 30th, `sticker.md`, differs only
by the pre-existing fix17 exceptions A+B (lines 90–91 plus the Motion-line
pointer, added Nov 11 by fix #17 — not fix19). The strip also removed the
non-`system-ui` tails from those files: e.g. `sticker.md:28–29` went from
`--font-display: "Bowlby One SC", "Arial Black", sans-serif; --font-body:
"Sofia Sans", ui-sans-serif, system-ui, sans-serif;` to `--font-display:
"Bowlby One SC", "Arial Black"; --font-body: "Sofia Sans";`.

**The 21 unstripped files — MINOR-1.** `fix19.py:main()` step 2 skips any
theme file with no `system-ui` (`if not before: continue`), so 21 files were
never touched — verified byte-identical to the pre-fix19 repo copy. Of those,
README.md has no `--font-*` declarations, but the other **20 files still
carry generic tails on 31 `--font-*` declaration lines** in their Tokens
blocks (the `:root` CSS fence, e.g. `darkroom.md:27` — see finding). The 83
non-declaration `--font-` lines across all theme files are all `var(--font-*)`
usages (`font-family: var(--font-display)` etc.) and carry no stacks — clean.

### MINOR-1 — 20 theme Tokens blocks still ship bare-generic / `ui-*` font tails

20 files, 31 `--font-*` declaration lines (Tokens block = the page's
`:root` per Taste step 4), each a named face followed by a generic tail
(`ui-sans-serif` / `ui-serif` / `ui-monospace` / `ui-rounded` plus bare
`sans-serif` / `serif` / `monospace`):

| File | Lines | Example |
|---|---|---|
| `arcade.md` | :29 | `--font-display: "Bungee", "Impact", sans-serif; --font-body: "Chivo", ui-sans-serif, sans-serif; --font-outlier: "Silkscreen", monospace;` |
| `blueprint.md` | :28–29 | `"Chakra Petch", ui-sans-serif, sans-serif` / `"IBM Plex Mono", ui-monospace, monospace` |
| `broadside.md` | :27–28 | `"Six Caps", "Impact", sans-serif` / `"Bevan", Georgia, serif` |
| `darkroom.md` | :27 | `"Sofia Sans Extra Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif;` |
| `dose.md` | :31–32 | `"Schibsted Grotesk", ui-sans-serif, sans-serif` / `"DM Mono", ui-monospace, monospace` |
| `editorial.md` | :27 | `"Bricolage Grotesque", ui-sans-serif, sans-serif; --font-body: "Source Serif 4", ui-serif, Georgia, serif;` |
| `formwork.md` | :30–31 | `"Oswald", ui-sans-serif, sans-serif` / `"Archivo Narrow", ui-sans-serif, sans-serif` |
| `halftone.md` | :28 | `"Ultra", ui-serif, Georgia, serif; --font-body: "Chivo", ui-sans-serif, sans-serif;` |
| `hum.md` | :32–33 | `"Chillax", ui-rounded, ui-sans-serif, sans-serif` / `"Geist Mono", ui-monospace, monospace` |
| `newsprint.md` | :27–28 | `"Zilla Slab", ui-serif, Georgia, serif` / `"Libre Franklin", ui-sans-serif, sans-serif` |
| `overprint.md` | :30–31 | `"Anybody", ui-sans-serif, sans-serif` / `"Archivo Narrow", ui-sans-serif, sans-serif` |
| `pasteup.md` | :27 | `"League Gothic", Impact, sans-serif; --font-body: "Newsreader", Georgia, serif;` |
| `piste.md` | :28 | `"Barlow Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif;` |
| `riso.md` | :27 | `"Cabinet Grotesk", ui-sans-serif, sans-serif; --font-body: "Literata", ui-serif, Georgia, serif;` |
| `solstice.md` | :28–29 | `"Yeseva One", ui-serif, Georgia, serif` / `"Archivo Narrow", ui-sans-serif, sans-serif` |
| `sport.md` | :28–29 | `"Saira Condensed", sans-serif` / `"JetBrains Mono", ui-monospace, monospace` |
| `terminal.md` | :30 | `"Martian Mono", ui-monospace, monospace` |
| `terrazzo.md` | :28–29 | `"Syne", ui-sans-serif, sans-serif` / `"JetBrains Mono", ui-monospace, monospace` |
| `vellum.md` | :28–29 | `"Grenze Gotisch", ui-serif, Georgia, serif` / `"Grenze", ui-serif, Georgia, serif` |
| `wayfind.md` | :27 | `"Chivo Mono", ui-monospace, monospace` |

Why minor, not blocking: the residue is pre-existing (all 20 files are
byte-identical to the pre-fix15 copy — fix19 introduced none of it), and
fix19's implemented scope was the 30 `system-ui` files, as documented in
`fix19/MANIFEST.md` §3/§4 and `fix19/inventory.md` (which inventoried
`system-ui` only). But it is a real residue, not bookkeeping: MANIFEST §3
deviation 5 puts "Theme Tokens blocks … in scope under SPEC §5 (they ship
into built pages — the Tokens block is the page's `:root`)", the placed
F2_RULE bans "no bare generic `sans-serif`/`serif` as a live path", and F2
binds the delivery format even for a theme body face kept under exception
("A theme body face delivered as a variable file or with a system fallback
is a bug to fix, not an exception to record"). A build dealing one of these
20 themes ships a `:root` that violates the rule the package just placed.
`verify19.py` does not assert on non-`system-ui` generic tails, which is why
it passes 75/75 despite this. **Fix:** run the existing
`strip_theme_tails` (same `THEME_TAILS` list, same function) over the
remaining 20 files — no new logic needed; then re-sweep. No `system-ui`
is involved in any of the 20 (theme-file `system-ui` is 0, §7), so the
fix19 `system-ui` inventory is unaffected.

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
less-flat-ui treatments still exactly 1..23.

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
Pre-fix19 baseline re-derived from the repo copy: 191 occurrences in 121
files (SPEC §1's "139" is wrong, as MANIFEST §3 deviation 1 states); 191 −
44 fixed (40 `*.md` + 4 shipping templates) = 147, + 14 new rule-text
mentions = 161 ✓.

## 8. build.sh exception inventory re-derived — delta 0 — PASS

- `md5sum build.sh` → `a8d3d3c6f6d32344d0168c5323d9364b`, **23,314 lines**
  (was 23,276; +38 = the fix19 block, lines 23267–23304, marker
  `# --- fix19: font identity, forced font choice, Tiempos body font,
  thought-out decisions (F2/F3/F4/D19) ---` at :23267).
- Fresh banned-term line count: `grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh` → **798 lines**.
- Re-derivation: parsed the 798-row inventory table in
  `fix16/sweep18-report.md` (§Check 16) and cross-checked its line-number
  set against a fresh `grep -in` of `build.sh`. The two sets are
  **identical — no missing, no extra lines**. (First parse attempt returned
  734 rows because the table's term column can be multi-term, e.g.
  `claude,codex`; re-parsing with a comma-tolerant column pattern yields
  all 798.)
- Category counts from the table's class column: **(a) OLD-side 389, (b)
  comment 52, (c1) NEW-side transient 355, (c2) heredoc 0, (c3) build-time
  `.claude/skills/` paths 2** (`:265`, `:298` — the two `cp -r …/.claude/skills/…`
  lines) — identical to the sweep #18 baseline (389/52/355/0/2).
- Per-term line counts (fresh grep): `claude` 701, `codex` 103, `anthropic` 5,
  `opus` 22, `sonnet` 23, `haiku` 13, `composer-2.5` 0 — identical to the
  sweep22 baseline.
- **Delta vs sweep #22: 0.** The fix19 block contains **zero** banned-term
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

## 11. Staged-vs-built diffs — PASS, with two noted deviations (not findings)

`diff -q` staged → built for the eight fix19 staged files:

| File | Result |
|---|---|
| `new-skills/orchestrate/SKILL.md` | IDENTICAL |
| `round2-skills/polish-pass/reference/lenses/typeset.md` | IDENTICAL |
| `new-skills/design-taste-frontend/scripts/start.mjs` | IDENTICAL |
| `new-skills/design-taste-frontend/references/hallmark/scripts/theme.mjs` | IDENTICAL |
| `new-skills/pitch-deck-video/template/shots.json` | IDENTICAL |
| `new-skills/pitch-deck-video/template/shots.example.json` | IDENTICAL |
| `new-skills/design-taste-frontend/SKILL.md` | DIFFERS — 1 hunk only (lines 9–13, frontmatter description) |
| `round2-skills/polish-pass/SKILL.md` | DIFFERS — 4 hunks only (lines 3, 15, 24, 31) |

Both diffs are pre-existing build.sh patch blocks, not fix19: the Taste
hunk is the `replace_text("design-taste-frontend", …)` "Use ONLY for a full
company or landing-page build from scratch…" description replacement at
`build.sh:606–614`; the polish-pass hunks are block "(f) polish-pass: the
new-look rule also names Taste" at `build.sh:~759`. Both built-side strings
are present in `build.sh.before-fix19` (grep count 1 each), so they predate
fix19. The built side is the intended side; the fix19-relevant regions match
(§3 counts). Same class as sweep22 §5's `hackathon-mode.mdc` deviation.
Theme files staged-vs-built: **0 mismatches** across all 51 files.

## Commands used (full list)

```
md5sum build.sh ; wc -l build.sh
python3 fix19/verify19.py ; python3 fix15/verify15.py ; python3 fix17/verify17.py ; python3 fix18/verify18.py
grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules skills agents commands rules hooks README.md  (in hackathon-ecc)
for d in new-skills rewritten-skills round2-skills new-rules; do grep -rniE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' --exclude-dir=node_modules "$d"; done
grep -niE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' ~/workspace/cursor-skills/less-flat-ui/SKILL.md
grep -ro 'grok-4.7-high' / grep -r 'grok-4.7-high' / grep -ro 'cursor-grok-4.6-high-fast' / grep -r 'cursor-grok-4.6-high-fast' / grep -rP '(?<!cursor-)grok-4\.6-high-fast' / grep -r 'grok-4\.7\[' / grep -r 'grok-4\.6\[' / grep -r 'effort=' / grep -ro 'reasoning_effort' (all --exclude-dir=node_modules, in hackathon-ecc)
grep -rn 'Grok 4.7 High \[0-9\]\|Grok 4.6 High Fast \[0-9\]' --exclude-dir=node_modules .
python3 /tmp/sweep23.py  (F2/F3/F4/D19/STATIC19/app-mirror counts + md5s from fix19.py; CANONICAL counts + md5 from fix15.py; theme decl-line tail check; staged-vs-built diffs; system-ui class breakdown)
grep -rn 'may invent' --exclude-dir=node_modules hackathon-ecc | wc -l
grep -rn 'body faces name their source (self-hosted or link) and fallback stack' / 'legitimate default with' / 'variable fonts use `font-optical-sizing: auto`' --exclude-dir=node_modules hackathon-ecc
grep -c 'system-ui' hackathon-ecc/skills/design-taste-frontend/scripts/start.mjs hackathon-ecc/skills/design-taste-frontend/references/hallmark/scripts/theme.mjs hackathon-ecc/skills/pitch-deck-video/template/shots.json hackathon-ecc/skills/pitch-deck-video/template/shots.example.json
grep -n 'fix19:' build.sh ; grep -n 'fix19 upstream block applied' build.sh
python3 (strip replay: fix19.strip_theme_tails on ~/workspace/hackathon-plugin-repo theme copy vs current staged themes; 29/30 byte-identical, sticker.md = strip + fix17 exceptions; 21 unstripped byte-identical)
python3 (E1 md5/counts from fix17.py; less-flat-ui treatment numbers; sticker exceptions A+B; theme decl-line split stripped 57/0 vs unstripped 33/31; non-decl --font- lines audit)
diff -q (8 fix19 staged files) ; diff new-skills/design-taste-frontend/SKILL.md hackathon-ecc/skills/design-taste-frontend/SKILL.md ; diff round2-skills/polish-pass/SKILL.md hackathon-ecc/skills/polish-pass/SKILL.md
grep -c 'Use ONLY for a full company or landing-page build from scratch' / 'less-flat-ui, and design-taste-frontend, not this skill' build.sh build.sh.before-fix19
python3 (sweep18 table parse with comma-tolerant term column → 798 rows, classes a389/b52/c1 355/c2 0/c3 2; fresh grep -in line-set comparison → identical; per-term line counts)
grep -c -iE 'claude|codex|anthropic|opus|sonnet|haiku|composer-2\.5' build.sh ; per-term grep -ci loop
ls skills|wc -l ; ls agents|wc -l ; ls rules|wc -l ; ls commands|wc -l ; python3 -c "import json; print(len(json.load(open('hooks/hooks.json'))['hooks']))"
```
