# Fix program #11 — Hallmark + Impeccable scoped addition

**Date:** Nov 10–11, 2026 (finished ~00:05 CST Nov 11)
**Status:** DONE — staged, wired, rebuilt twice (exit 0, diff 0), verified in the built plugin.
**Backups:** `build.sh.before-fix11` (in `~/workspace/hackathon-plugin/`).
**Patch scripts:** `fix11/fix11-stage.py`, `fix11/fix11-wire.py` (in `~/workspace/hackathon-plugin/fix11/`).

## Build results

- Builds 3 + 4 (after README size update + index.json strip): exit 0, md5 manifests identical (diff = 0).
- Counts unchanged: **169 skills / 72 agents / 123 rules / 96 commands, hooks 15** (no new skills, agents, rules, commands, or hook events — this round adds references + wiring only).
- build.sh: 21,934 → **21,957 lines** (fix11 runtime patch block, 23 lines, placed LAST before STEP 5).
- Plugin size: 55 MB → **57,584 KB (~56.2 MB, du reports 57M)**; staged addition ≈ 1.5 MB (Hallmark 1,368 KB + Impeccable ~96 KB). README "55 MB" → "56 MB" (2 lines, built README verified: "56 MB" ×2, "55 MB" ×0). The byte-cap comment at build.sh:16992 also updated 55 → 56 MB.

## Pins and SHAs (all re-verified before staging)

| Item | Pin | Verified by |
|---|---|---|
| Hallmark repo | HEAD SHA `7e213cb6feb4ef82733bd66a0600b2e54ca0994c` (last commit 2026-11-10 18:01 UTC), v2.0.0, MIT | `git ls-remote https://github.com/Nutlope/hallmark` |
| Hallmark | NO GitHub releases/tags — the SHA is the pin | GitHub releases page / ls-remote |
| Impeccable skill release | `skill-v4.8.0` (universal.zip 18,116,588 bytes, 2026-10-26) | GitHub release tag, verified download |
| Impeccable npm | `impeccable@4.8.0`, tarball shasum `f344aaa43511ea0ccadce1a42c860f5990953430`, engines node >=18.19.0 | `npm view impeccable@4.8.0` |
| Impeccable engine | v0.1.18; Windows x64 SHA-256 `8f61e96b0c97001546a824d79b44f46b423b560f3eb1a0cc44a8695a1b395d9f` | `impeccable --list-rules --json` golden file at tag skill-v4.8.0; engine release |
| puppeteer-core | `puppeteer-core@25.17.0` (install instruction only — plugin never auto-installs) | `npm view puppeteer-core@25.17.0` |

**Note for next audit:** npm latest for `impeccable` is **4.8.2** (2026-11-09). 4.8.0 is pinned deliberately — it is the verified skill release. Do not "fix" this to latest without re-verifying the skill release.

## Corrections to the brief's premises (found by research)

- Hallmark has **NO "57 gates"** — it is **90 clauses across 71 numbers** (14 retired, never reused), tiers 39 Floor / 50 Reflex / 1 Ledger, + 26 Finish checks F1–F26 (`gates.md`).
- Hallmark has **NO "study" verb** — verbs are **build / redesign / audit only**.
- Impeccable's shipped Cursor hook (`.cursor/hooks.json`, 268 bytes) is a single POSIX sh command; Cursor on Windows runs hook commands through PowerShell, so it is **likely broken on Windows** — NOT wired. Detector runs as a named step instead; hook = live-smoke-test item.
- `impeccable.cmd` is untested on real Windows by upstream's own admission; no windows-arm64 npm package (falls back to x64 exe).

## Hallmark — what was staged and where it lives

Staged under `new-skills/design-taste-frontend/references/hallmark/` (built: `skills/design-taste-frontend/references/hallmark/`), 1,368 KB:

- `scripts/theme.mjs` (deal/scaffold/index), `scripts/sloplint.mjs` (231 KB, zero-dep, Node 18+), `scripts/sloplint-render.mjs` (Puppeteer render tier), `scripts/photos.json` (755 Wikimedia URLs + metadata only, no bytes)
- `references/gates.md` (90 clauses), `references/review-hero.md`, `references/review-finish.md`, `references/redesign.md`
- `references/themes/` — **50.md + index.json + README.md, 0.jpg** (text only; the 50.jpgs, 5.0 MB total, NOT staged — the visual pick degrades to header/material description)
- `references/hallmark-floor.md` (condensed 16 Floor rules + 6-axis critique, written for this plugin)
- `PROVENANCE.md` (SHA, version, what was/wasn't staged, Windows notes)

**NOT staged:** `skills/hallmark/SKILL.md` (no separate skill); layout/anatomy/craft/direction/imagery/patterns/flow/genres/macrostructures (Taste owns the build playbook); capture.mjs/picture.mjs (covered by polish-pass capture.mjs + browser-qa); install*.mjs/lint-hook.mjs (no Cursor edit-time hook upstream; plugin has its own hooks); imagegen.mjs (Together FLUX, never wired); refcheck.mjs (upstream CI only); `site/` + `eval/` (never checked out).

**index.json tweak (this round, not upstream):** the staged `index.json` had all 50 `picture` keys stripped (they pointed at the unstaged .jpgs); `pictured` (text description of the picture's content) kept. Verified: `theme.mjs deal` still works and no longer references any .jpg path. If `theme.mjs index` is ever re-run it regenerates `picture` only for .jpgs that exist, so regeneration stays consistent.

## Hallmark — wiring (built file:line)

| Wiring | Built location |
|---|---|
| Theme deal (Taste step 4: deal 3 themes, pick 1 by material) | `skills/design-taste-frontend/SKILL.md:234` |
| Craft-floor read (Taste step 4a) | `skills/design-taste-frontend/SKILL.md:242` |
| Redesign paragraph (before step 5; `sloplint --before` / `--kept`) | `skills/design-taste-frontend/SKILL.md:244` |
| sloplint + hero review (Taste step 6) | `skills/design-taste-frontend/SKILL.md:306`, `:314` |
| Hallmark audit (orchestrate Verify item 6: sloplint + 6-axis critique + finish review) | `skills/orchestrate/SKILL.md:182` |
| README credit | `README.md:22` |

Design: the 50-theme catalog is the theme vocabulary UNDER Taste (Taste stays the landing lead). sloplint + reviewer wire into Verify as a named check — NOT a second builder, NOT an approval gate (auto-approval after grill-me stands; reviewer is a sub-agent pass, never a wait). Audit verb = the sloplint run in Verify. No separate `/hallmark` command, no separate skill.

**Render-tier decision:** `sloplint-render.mjs` is written directly against the Puppeteer API (`page.evaluate`, `page.screenshot`, `page.keyboard.press`) — it cannot reuse the plugin's Playwright 1.65.0 or chrome-devtools MCP as a drop-in. Decision: pin `puppeteer-core@25.17.0` (install instruction only); static tier runs without it and the handoff must say the render tier did not run. Chrome discovery: `CHROME_PATH` first, then a hardcoded list with only the 64-bit Windows path (`C:\Program Files\Google\Chrome\Application\chrome.exe`) — 32-bit and per-user `%LOCALAPPDATA%` installs NOT listed; `CHROME_PATH` is the workaround.

## Impeccable — gap table (24 commands + rest)

### ADDED this round

Staged under `round2-skills/polish-pass/reference/` (built: `skills/polish-pass/reference/`), ~96 KB:

| Component | Staged as | Wired into (built file:line) |
|---|---|---|
| **Detector** — 62 rules (31 slop + 31 quality; 44 warning, 16 advisory, 2 error; rule registry lives in the engine only, so the 62-rule list was extracted and staged as JSON) | `impeccable-detector-rules.json` (62 rules verified by parse) | polish-pass SKILL.md:89 (non-negotiable #5), polish.md:18 (Step 2 baseline) + :46 (Step 5 re-run); invoked as `npx impeccable@4.8.0 detect` |
| **Craft floor** (44 lines, read before any UI edit) | `impeccable-craft-floor.md` | polish-pass SKILL.md:88 (non-negotiable #4), Taste SKILL.md:242 (step 4a), ui-ux-pro-max SKILL.md:87 (Step 2) — via build.sh runtime patch (ui-ux-pro-max is fetched fresh from upstream each build via `pin_clone`, so it cannot be a staged edit; patch block at build.sh:21945) |
| **`critique`** reference (819 lines — scored UX review) | `impeccable-critique.md` | polish.md:19 (Step 2, when a Dimension scores below 6) |
| **`onboard`** reference (234 lines — first-run/empty states/activation) | `impeccable-onboard.md` | polish.md:37 (Step 4, when harden runs on a first-run surface) |
| **`extract`** reference (69 lines — consolidate repeated patterns into the design system) | `impeccable-extract.md` | polish.md:37 (Step 4, when consistency finds 3+ repeats) |
| Provenance + full gap table | `impeccable-PROVENANCE.md` | Attribution at polish-pass SKILL.md:107; Hallmark credit at :109; DESIGN.md/PRODUCT.md mapping at :75 |

### COVERED, not staged

| Component | Covered by |
|---|---|
| `polish` | = polish-pass itself |
| `distill`, `harden`, `clarify`, `adapt`, `optimize`, `typeset`, `layout` | polish-pass has a lens of the same name for each |
| `animate` | Covered THREE ways: polish-pass animate lens (fix-only) + ui-ux-pro-max motion implementation (motion.csv, 17 GSAP presets, `--motion` dial 1–10 with Subtle / Standard scroll-stagger / Complex choreography incl. pin, Flip, SplitText; SKILL.md:124/:130/:133; Animation row 7 of the quality table, MEDIUM weight, SKILL.md:30; quick-reference.md §7 spring-physics + easing + exit-faster-than-enter) + `make-interfaces-feel-better` owns feel/timing decisions (SKILL.md:133 — `--motion` only sets intensity). GSAP only; no framer-motion anywhere. |
| `craft` | Deprecated alias upstream, skipped |

### MAPPED, not staged (no new state files)

- `init` → grill-me decision record (`docs/decision-record.md`)
- `document` → `docs/design-tokens.md` / MASTER.md
- `shape` → grill-me + hackathon-scope + Taste deal
- `audit` → adversarial audit + browser-qa (covered-in-part)
- PRODUCT.md → `docs/decision-record.md` + `docs/scope.md`; DESIGN.md → `docs/design-tokens.md` + MASTER.md. The detector's `design-system-*` rules read `docs/design-tokens.md` instead of DESIGN.md.

### FLAGGED, not added (decision items for Anish)

1. **Direction lenses — `bolder`, `quieter`, `colorize`, `decolorize`, `delight`, `overdrive`.** Their job is to CHANGE a design's direction, clashing with the standing rule that polish-pass never restyles. Nuance: `overdrive`'s spring-physics content is partly covered by ui-ux-pro-max quick-reference.md §7, and the GSAP Complex tier covers pin/Flip/SplitText scroll choreography — the missing part is the direction change itself. **Recommendation: keep flagged; revisit only if Anish wants an interactive on-demand mode.**
2. **`live` + `generate`** (live browser variant iteration). Genuinely missing, but interactive, needs a running dev server + the 553 KB live-browser.js engine scripts, and cannot run in the unattended first build. **Recommendation: keep flagged; same revisit condition.**

## Verification (all in the BUILT plugin)

- Builds 1–2: exit 0, diff 0, counts 169/72/123/96, hooks 15. Builds 3–4 (after README + index.json changes): exit 0, diff 0, same counts.
- All staged files present in built tree; all 14 wiring edits present (grep counts match; line numbers in the tables above).
- `node --check` passes on all 3 staged Hallmark scripts (theme/sloplint/sloplint-render).
- **Functional test — `theme.mjs deal`:** ran from /tmp against the built tree, dealt 3 themes (Manifesto, Brutal, Garden) for "Campus Eats dining hall app", exit 0. After the index.json strip, output no longer references any .jpg path.
- **Functional test — `sloplint.mjs` static tier:** ran on a minimal test HTML page, exit 0, correctly reported 3 FAIL / 1 REFLEX / 2 WARN.
- Detector rules JSON parses: 62 rules, 31 slop / 31 quality.
- Pins: `impeccable@4.8.0` everywhere it is invoked (0 unpinned `npx impeccable`); `puppeteer-core@25.17.0` everywhere it is referenced as an install (the 1 remaining bare `puppeteer-core` mention is upstream code in sloplint-render.mjs:102 — a module-resolution loop `['puppeteer-core', 'puppeteer']`, not an install instruction).
- Frontmatter: 0 bad in audit scope (460 blocks in SKILL.md/commands/agents/rules); GATE phrase 21× (unchanged); SSML intact (pitch-deck-video SKILL.md:339–340, :542 — "v3/v4 models do NOT support `<break>` tags").
- README credit line present (README.md:22); fix11 patch printed in build log.

## Notes for the next audit

- **terminal.md YAML quirk (NOT a defect):** `skills/design-taste-frontend/references/hallmark/references/themes/terminal.md` has a `material:` header value containing ": " ("in the page's own glyphs: a photograph rendered…"), which fails strict YAML parsing. Hallmark theme headers are NOT YAML frontmatter — `theme.mjs` `parseHeader` splits each line on the FIRST `key: ` and keeps the rest, so the value is intact and the deal ran over all 50 themes. Do not "fix" by quoting the value — quoting would put literal quotes into the material string. The audit's frontmatter scope is SKILL.md/commands/agents/rules files, where this file does not belong.
- The deal output's static `next:` line still says "look at the pictures" (upstream hint text); the Taste wiring overrides it ("pick by the material description, not the picture"). No .jpg file paths remain in deal output.
- The Impeccable hook (`.cursor/hooks.json`) was NOT staged or wired — Windows/PowerShell incompatibility. Live-smoke-test item only.
- Pip pinning NOT done (separate decision, pending). No zip/upload. `~/workspace/hackathon-plugin-repo/` untouched.

## Smoke-test items appended

`LIVE_SMOKE_TEST.md` §13 (before Results): detector first run via npx on Windows (Git Bash + PowerShell, engine download + SHA check, `%USERPROFILE%\.impeccable\bin\0.1.18\`), Cursor hook on Windows (expected unknown — record whether it fires), Hallmark render tier (puppeteer-core@25.17.0 + Chrome, `CHROME_PATH` workaround), Hallmark theme deal (theme name + material in the report).
