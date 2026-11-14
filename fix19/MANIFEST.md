# Fix #19 — manifest (font identity, forced font choice, Tiempos body font, thought-out decisions)

- **Status:** CLOSED. Audit #61 CLEAN (0/0), dry-run #30 PASS, sweep #24 CLEAN (0/0). Fix-up round closed the audit #60 / sweep #23 minors (see §7).
- **Engine:** `fix19/fix19.py` (preflight + staged edits + theme tail strip; all anchors count==1) + `fix19/verify19.py`; fix-up engine `fix19/fix19_fixup.py` (see §6).
- **`build.sh`:** 23,314 lines (was 23,276), md5 `a8d3d3c6f6d32344d0168c5323d9364b` — UNCHANGED by the fix-up (the fix-up edited staged sources only; build.sh is byte-identical post-fix-up, verified by md5 after the rebuilds).
- **Backup:** `build.sh.before-fix19` (first pre-fix19 copy, kept).
- **Counts:** 166 skills / 72 agents / 123 rules / 87 commands / 15 hooks — unchanged.
- **Builds:** build 1 exit 0, build 2 exit 0; tree manifests identical (diff 0), sha256 `096b8ca3227c8b7d90db5ddb15b71faf701d83d0457badefe349af8b80090727` (`fix19/manifest1.txt`, `fix19/manifest2.txt`). Fix-up rebuilds: builds 1 + 2 exit 0 with identical logs; a third build (exit 0) produced an identical tree manifest (diff 0) — see §6.
- **Verify:** `fix19/verify19.py` (see §7 below for its check-7 scoping).

build.sh lines: 23314
build.sh md5: a8d3d3c6f6d32344d0168c5323d9364b

## 1. What changed

### Staged sources (edited directly; build.sh copies them verbatim)

| # | File | Change |
|---|---|---|
| 1 | `new-skills/design-taste-frontend/SKILL.md` (step 4a, line 245) | C2 sentence replaced by C2_NEW; F2 + F3 + F4 + D19 appended after the E1 rule |
| 2 | Taste step 6 | STATIC19 appended after the fix17 static-checks paragraph |
| 3 | `new-skills/design-taste-frontend/references/hallmark/references/themes/*.md` (30 files) | Tokens-block tail strip: `system-ui` + bare-generic tails removed from the `--font-*` lines of the 30 files that contained `system-ui` (39 occurrences); named faces retained. (CORRECTED wording — it previously read as if the strip covered all theme files. Fix-up §6 extended the strip to the remaining 20 files: 31 `--font-*` lines, 92 tail instances; all 51 files now carry named faces only.) |
| 4 | `new-skills/design-taste-frontend/scripts/start.mjs:291` | `stack()` fallback: `"Family", system-ui, sans-serif` → `"Family"` (serif branch keeps named `Georgia`) |
| 5 | `.../references/hallmark/scripts/theme.mjs:470` | CUSTOM_TOKENS font lines: system-ui/generic tails stripped |
| 6 | `new-skills/pitch-deck-video/template/shots.json:33` + `shots.example.json:33` | `"sans"` stack → `"Hanken Grotesk"` alone (loaded by `fonts.ts`) |
| 7 | `new-skills/orchestrate/SKILL.md` | F2 + F3 + F4 + D19 after the E1 rule; D19_ROUTING (:100); D19_REVIEWER (:195); STATIC19 in Verify 5a |
| 8 | `round2-skills/polish-pass/SKILL.md` (harmony) | POLISH_F19 appended after the fix17 F1/T1 verification |
| 9 | `round2-skills/polish-pass/reference/lenses/typeset.md` | System-ui sentence (line 55) replaced by TYPESET_F19; checkbox updated |
| 10 | `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (record section) | LF_D19 appended after the fix17 U1 record note |

### build.sh patch block (upstream, no staged source)

| # | File (built) | Change |
|---|---|---|
| 11 | `skills/ui-ux-pro-max/SKILL.md` | F2_APP + F3_APP + F4_APP + D19_APP after the anti-generic bar; C1 sentence extended with C1_APP_NOTE |
| 12 | `skills/orch-build-mvp/SKILL.md` | D19_APP after the E1 rule (step 4); STATIC19 after the fix17 checks (step 6) |

## 2. Banned-term rewording (fix #16 scrub)

The SPEC's F4 texts contain TWO banned tokens: "Anthropic" (title,
"the Anthropic font") and "Claude" ("the font Claude's reading text is
set in", "Claude's 1.55 reading line-height"). The parent task's
suggested rewording ("the font Claude's reading text is set in") still
contains banned token "claude", so it was NOT used. Instead:

- F4_RULE title: "**Plain/body text uses the Anthropic font (fix #19 F4).**"
  → "**Plain/body text uses Tiempos (fix #19 F4).**"
- F4_RULE body: "Body and plain text use Tiempos — the font Claude's
  reading text is set in (Klim, paid, NOT bundleable). The canonical free
  stand-in is Fraunces, set at Claude's 1.55 reading line-height."
  → "Body and plain text use Tiempos (Klim, paid, NOT bundleable). The
  canonical free stand-in is Fraunces, set at a 1.55 reading line-height."
- F4_APP title: same change, with "(fix #19 F4, app surfaces)".

Every functional fact is preserved (Tiempos, Klim, paid, NOT bundleable,
Fraunces stand-in, 1.55 line-height); only the attribution clause was
dropped. No banned term appears in any fix19 addition (asserted by the
engine's preflight scan and by verify19 check 9).

## 3. Deviations from the SPEC (with reasons)

1. **SPEC §1 baseline `system-ui` = 139 is wrong.** Measured baseline is
   **191 occurrences in 121 files** (see `fix19/inventory.md`). The
   verify asserts against the measured numbers.
2. **SPEC §7.7 check 7 ("zero in built-tree `*.md` rule files") cannot
   be literal.** The fix19 rule texts themselves name `system-ui` as the
   banned token (F2_RULE ×3, STATIC19, C2_NEW, POLISH_F19, TYPESET_F19,
   TYPESET checkbox, F2_APP). verify19 therefore asserts zero in `*.md`
   files AFTER subtracting the placed rule texts — any remaining mention
   would be a font-stack occurrence, and the check fails. Theme files
   must be a literal zero (they are, post-strip).
3. **Orchestrate 5a anchor.** The SPEC's two-line anchor
   ("a floor/ban break blocks.\n   - **5b. Final polish**") was used as
   a LOCATOR (preflight asserts the adjacency), not as the append point:
   appending after it would inject STATIC19 after the "**5b. Final
   polish**" lead-in, mid-bullet. STATIC19 is appended after the 5a
   paragraph's final sentence instead, and verify19 asserts it sits
   before the 5b bullet.
4. **C1_APP_NOTE wording is mine.** The SPEC names the slot ("extend
   the C1 sentence with the F2/F3/F4 app note") but gives no constant
   for it; I wrote the pointer sentence in `fix19.py`.
5. **Theme Tokens blocks + `start.mjs` / `theme.mjs` / `shots.json`
   are in scope** under SPEC §5 (they ship into built pages — the
   Tokens block is the page's `:root`; `stack()` emits built-page CSS;
   `sans` is the video render's font stack). Named second faces
   (Georgia, Impact, Arial Black, Futura, Iowan Old Style) were
   RETAINED as the theme's type voice (SPEC §5's Sofia precedent);
   only `system-ui` and bare-generic tails were removed.
6. **`fix18` has no build.sh block** (it edited staged sources only, per
   verify18 check 14), so verify19 check 10 asserts the fix15 + fix17 +
   fix19 markers, not a fix18 marker.
7. **verify19 check 10 reads lines/md5 from this MANIFEST** instead of
   hardcoding them (the numbers only exist after the build).

## 4. `system-ui` inventory (measured pre-fix19; full detail in `fix19/inventory.md`)

- Total 191 → 161 remaining after the fix. The fix-up (§6) did not move the total: the 20 newly stripped theme files contain no `system-ui`, the shots.json serif/mono stacks contain none, and no fix-up text adds a literal `system-ui` (verify19 pins the *.md mention count at 14).
- Fixed: 40 in `*.md` (39 theme Tokens + 1 typeset lens) + 4 shipping
  templates (`start.mjs`, `theme.mjs`, `shots.json` ×2) = 44; fix-up additionally removed 92 bare-generic/ui-* tail instances from 31 `--font-*` lines in 20 theme files and the generic tails from the shots.json serif/mono stacks (no `system-ui` involved in either).
- Remaining 161: 129 demo assets + 12 dev/QA tooling pages + 3
  detectors (sloplint/consistency name the ban — must keep) + 3
  reference data (`styles.csv`) + 14 rule-text mentions (the fix19
  rules themselves naming `system-ui` as the banned token: Taste 5,
  orchestrate 4, typeset lens 2, orch-build-mvp 1, polish-pass 1,
  ui-ux-pro-max 1).

## 5. Open items / limitations (for the audit + dry-run workers)

- `start.mjs` loader gap — CLOSED by the §6 fix-up: `fontLink()` now requests explicit static weights only (no `..` ranges, no non-weight axes), the mono stack names the bundled face only, and the Taste step-4a instancing step tells the build how. The printed Google Fonts link remains the generation source; the shipped delivery is the instanced static files.
- The workspace Campus Eats `design-tokens.md` is still v1-era/stale
  (SPEC §1 caveat); untouched by this fix.
- Open observations for the re-audit (out of this fix-up's scope, recorded not fixed): (i) `start.mjs` still emits `--display-axes` (`font-variation-settings` values, `type.json` fraunces pairing only: `'SOFT' 30, 'WONK' 0`) — a variable-axis CSS var on an otherwise static delivery; the D1 face check would catch a rendered mismatch. (ii) `assets/layout/deal.mjs:128` still says "keep its :root lines as printed" — a demo-asset line about headline weights, not font delivery; left as-is (assets/ are demo-only). (iii) verify19 check-7's name ("system-ui zero in all 30 theme files") is stale — the check itself globs all 51 theme files; the name was not changed (verify19 is updated only when a rule text changes).
- No commit, no bundle, no GitHub touch. Checker results: see §7 (audit #61 CLEAN, dry-run #30 PASS, sweep #24 CLEAN).

## 6. Fix-up round (post-audit #60 / sweep #23, Nov 11 2026)

Engine: `fix19/fix19_fixup.py` (preflight + 15 subs + theme strip over all 51 files + self-checks). The F2 rule text itself is UNCHANGED — the method lives in the procedural step, so `fix19.py`'s F2 constant and `verify19.py` are untouched; verify19 still passes 75/75 with no update.

### What changed (staged sources only; build.sh byte-identical)

| # | File | Change (old → new) |
|---|---|---|
| 1 | `new-skills/design-taste-frontend/references/hallmark/references/themes/*.md` (20 files) | Tail strip extended to all 51 files (skip gate dropped): 31 `--font-*` lines, 92 tail instances removed (e.g. `darkroom.md:27` `--font-display: "Sofia Sans Extra Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif;` → `--font-display: "Sofia Sans Extra Condensed"; --font-body: "Barlow";`). All 51 theme files now carry named faces only; 0 tail lines remain (verified in the built tree). |
| 2 | `new-skills/design-taste-frontend/scripts/start.mjs:257-289` | `fontLink()`: `axisVal`/`isLower`/`axisOrder` deleted; new `expandWeights()` helper (`:261`) expands a weight range to explicit 100-step weights + end weights; the `f.w` branch stores statics instead of setting `e.variable` (`:281`); the URL builder emits `wght@400;500;600;700` only. Non-weight axes (wdth/opsz/SOFT/WONK) are left out of the link — baked in at instancing time. Verified live: `types` over all 6 pages went from 128 `..` ranges to 0; e.g. `family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500`, `family=Instrument+Sans:wght@400;500;600;700` (wdth dropped), `family=Mona+Sans:wght@400;500;600`. |
| 3 | `.../scripts/start.mjs:305` | Mono stack: `"${monoOf(t).family}", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace` → `"${monoOf(t).family}"`. Loader already requests the mono face at explicit weights 400;500 (DEFAULT_MONO `w: [400, 500]`; every `type.json` mono face is `w [400,500]` or `s [400,500]`). Verified live: `css` emits `--font-mono: "Geist Mono";`. |
| 4 | `new-skills/design-taste-frontend/SKILL.md:229` (built :230) | "Keep the `:root` block as printed." → same + "except the font delivery: the Google Fonts link the block prints requests static instances only (fix #19 F2) and is the generation source — instance the dealt faces to static files per the step 4a instancing step and ship those files with `@font-face` + preloads, never a CDN link as the delivery." |
| 5 | `new-skills/design-taste-frontend/SKILL.md:257` (built :258) | New procedural step after the F2 rule: "**Instance the dealt faces to static files before shipping (fix #19 F2 — the instancing step).**" — (1) download the OFL variable font, (2) fontTools instancer per weight with opsz baked in, other axes fixed at dealt values, (3) fontTools subsetter (latin + latin-ext), (4) verify no fvar + correct usWeightClass, (5) bundle static woff2 + `@font-face` + preloads. |
| 6 | `.../references/layout-v4.md:252,254` | Same carve-out on "keep the `:root` block as start.mjs prints it." (verified present at :252) and on the adjacent "Load from Google Fonts with `display=swap`" sentence (same paragraph, same delivery — leaving it would leave the procedure contradicting the rule). |
| 7 | `.../scripts/start.mjs:43` | Same carve-out on the loader's own header comment ("keep the block as printed") — the same instruction in the file under fix. |
| 8 | `new-skills/pitch-deck-video/template/shots.json:34-35` + `shots.example.json:34-35` | Serif/mono stacks narrowed to the bundled faces alone (see shots.json scoping decision below). |

### shots.json scoping decision — F2 GOVERNS the serif/mono stacks (fixed, not left)

The video template IS a shipped surface: `theme.ts` passes `shots.theme.fonts` straight into `fontFamily` in `Brand.tsx`, `Captions.tsx`, `Arch.tsx`, `Close.tsx` (the /demo render is a deliverable), and `fonts.ts` loads exactly the named faces with explicit weights (Instrument Serif 400; JetBrains Mono 400/500) via `@remotion/google-fonts`. Fix19 already treated the `sans` stack as in scope on the same reasoning (deviation 5), so leaving serif/mono with system tails would contradict the `sans` fix. Fixed the same way: `"serif": "\"Instrument Serif\", Georgia, serif"` → `"\"Instrument Serif\""`; `"mono": "\"JetBrains Mono\", ui-monospace, monospace"` → `"\"JetBrains Mono\""` (both files; JSON re-validated).

### Builds + verifiers (post-fix-up)

- Builds 1 + 2: both exit 0; build logs identical; a third build (exit 0) produced an identical tree manifest (diff 0), confirming the two post-fix-up builds are diff 0. Changed files vs the pre-fix-up built tree: exactly the 25 fix-up files (Taste SKILL.md, layout-v4.md, start.mjs, shots.json ×2, 20 theme files) — no other file moved.
- `build.sh` still 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b` (unchanged — the fix-up never edits build.sh).
- Verifiers (re-run post-fix-up): verify19 75/75, verify15 43/43, verify17 59/59, verify18 72/72. Built-tree `system-ui` total still 161; built-theme tail lines 0. Staged-vs-built: identical for start.mjs, layout-v4.md, both shots.json files, and all theme files; Taste differs only by the pre-existing frontmatter hunk.

### Deviations / honest notes on the fix-up run itself

- The fix-up script failed twice mid-run BEFORE its self-checks (after the subs + theme strip had already landed, so the run is one-shot like fix18's): (1) its preflight `system-ui`-in-new-text assert was over-broad — the F2_RULE anchor itself names `system-ui`; scoped to the added text only. (2) its `'..'` self-check assert was over-broad — `'..'` is legitimate in `path.join(here, '..', 'library', …)`; scoped to the `fontLink` function body. Both are fixed in the script as it now stands.
- A real defect the second failure exposed: the script's `SHOTS_SERIF_NEW` dropped the serif line's trailing comma, writing invalid JSON to both shots files (caught by the script's own `json.load` self-check, which is why the check exists). The comma was restored in both staged files and in the script constant; both files re-validated as JSON, and the full self-check suite was then run manually and passed. The script file now in `fix19/` is the corrected version.
- Extra scope beyond the two named ":root" lines, both inside MINOR-2 and reported here (not silent): the layout-v4 "Load from Google Fonts" sentence (#6 above) and the start.mjs:43 header comment (#7 above) carry the same delivery instruction and got the same carve-out.

## 7. Checker results — audit / dry-run / sweep

| Check | Result | Report |
|---|---|---|
| Audit #60 (first round) | **NOT CLEAN — 0 blocking, 2 minor** (MINOR-1: 20 theme files with bare-generic tails; MINOR-2: start.mjs emits a variable-font Google Fonts link + mono system stack) | `fix19/audit60-report.md` |
| Dry-run #30 | **PASS** — all six SPEC §6 items (rule presence 75/75; font criteria 6/6; repair compliance as repair-reported; both negative demonstrations fail as specified; D19 criteria 6/6) | `fix19/dryrun30-report.md` |
| Sweep #23 (post-build 2) | **NOT CLEAN — 0 blocking, 1 minor** (same theme-tails finding as Audit MINOR-1; all numbers re-derived and matching) | `fix19/sweep23-report.md` |
| Audit #61 (re-audit after fix-up) | **CLEAN — 0 blocking, 0 minor** (MINOR-1 fixed: 0 tails in all 51 files; MINOR-2 fixed and verified live — 0 `..` ranges, 225 explicit wght@ lists; shots.json decision agreed sound; left-open items judged documented limitations) | `fix19/audit61-report.md` |
| Sweep #24 (re-sweep after fix-up) | **CLEAN (0/0)** — same measurements re-verified after the fix-up; rule md5s match sweep #23; theme tails 0; system-ui 161 | `fix19/sweep24-report.md` |

Loop closed: the fix-up round (fix19_fixup.py + 3 builds exit 0, diff 0) resolved both audit #60 minors and the sweep #23 minor; re-audit #61 and re-sweep #24 are both clean. Dry-run #30 was NOT re-run after the fix-up (the fix-up changes no dry-run criteria, per the fix17 precedent).

Final state (coordinator-verified after the fix-up): build.sh 23,314 lines, md5 `a8d3d3c6f6d32344d0168c5323d9364b`; verify19 75/75, verify15 43/43, verify17 59/59, verify18 72/72; banned terms 0; counts 166/72/123/87/15; rule md5s F2 5ca43e60…, F3 1e7d0303…, F4 9468eba6…, D19 f97c569f…, STATIC19 130a988e…; canonical block 673ab869… ×1 in all 11 files.

Cleanup note: the fix-up worker's live start.mjs verification left a runtime-state file (`skills/design-taste-frontend/.taste-skill/history.json`, 292 B) in the built tree — not a plugin file, not produced by build.sh. The coordinator deleted it and ran a final full rebuild (exit 0) + verify19 (75/75); the tree is exactly what build.sh produces.

Left open (documented limitations, not findings — audit #61's judgment): (i) start.mjs still emits `--display-axes` (font-variation-settings, fraunces pairing only, inert on the prescribed static delivery); (ii) deal.mjs:128 "keep its :root lines as printed" left as-is (demo asset, headline weights, not delivery); (iii) verify19 check-7's name ("30 theme files") is stale while the check globs all 51 — a doc rename for the next verify19 touch. Live-browser verification (whether a cold-start build actually instances fonts, whether D1 fires) remains open — it needs the live smoke test in Anish's Cursor.
