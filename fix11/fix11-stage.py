#!/usr/bin/env python3
"""Fix program #11 — stage the Hallmark + Impeccable scoped additions.

Copies verified upstream files into the staged skill dirs (build.sh copies
those dirs verbatim into the built plugin). No build.sh patch anchors are
touched here; the SKILL.md wiring edits are applied separately by hand, and
the ui-ux-pro-max runtime patch lives in build.sh (placed LAST, before STEP 5).

Pins (all verified before writing):
- Hallmark: Nutlope/hallmark, MIT, v2.0.0, HEAD
  7e213cb6feb4ef82733bd66a0600b2e54ca0994c (2026-11-10 18:01 UTC).
  No GitHub releases/tags — the SHA is the pin.
- Impeccable: pbakaus/impeccable, Apache-2.0, skill release skill-v4.8.0
  (universal.zip, 18,116,588 bytes, 2026-10-26), npm impeccable@4.8.0
  (tarball shasum f344aaa43511ea0ccadce1a42c860f5990953430), engine v0.1.18.
  npm latest is 4.8.2 (2026-11-09) — 4.8.0 is pinned deliberately because
  the skill-v4.8.0 release is the verified one.
- puppeteer-core: pinned at 25.17.0 (npm view) wherever the Hallmark render
  tier is invoked (install instruction only — the plugin never auto-installs).

What is staged (text only, no binaries, no images):
- Hallmark: 50 theme .md + index.json + themes/README.md; theme.mjs,
  sloplint.mjs, sloplint-render.mjs, photos.json; gates.md, review-hero.md,
  review-finish.md, redesign.md; + a condensed hallmark-floor.md written
  for this plugin (16 Floor rules, verbatim-ish from SKILL.md) and a
  PROVENANCE.md. NOT staged: SKILL.md (no separate skill), the 50 .jpg
  pictures (text-only staging — the visual pick degrades to header/material
  description; the .jpgs are 5.0 MB total and remain available upstream),
  layout/anatomy/craft/direction/imagery/patterns/flow/genres/
  macrostructures (Taste owns the build playbook), capture.mjs/picture.mjs
  (covered by polish-pass capture.mjs + browser-qa), install*.mjs /
  lint-hook.mjs (no Cursor edit-time hook upstream; plugin has its own
  hooks), imagegen.mjs (no Together image generation — never wired),
  refcheck.mjs (upstream CI only), photos library images (photos.json holds
  URLs only, no bytes — staged).
- Impeccable: craft-floor.md, critique.md, onboard.md, extract.md
  (verbatim, attribution header prepended), detector-rules.json (the 62-rule
  list extracted from the --list-rules --json golden file at tag
  skill-v4.8.0), + an impeccable-PROVENANCE.md. NOT staged: the 24-command
  SKILL.md (no separate skill; commands mapped in the gap table), the
  direction lenses (bolder/quieter/colorize/decolorize/delight/overdrive —
  flagged, not added), live/generate (interactive live-variant mode —
  flagged, not added), the engine binary (downloads once from the pinned
  release, SHA-verified against engine-checksums.txt), the .cursor/hooks.json
  hook (POSIX-only as shipped — likely broken on Windows/PowerShell; the
  detector is wired as a named step instead, hook = live-smoke-test item).
"""
import json
import os
import shutil
import sys

PLUGIN_ROOT = os.path.expanduser("~/workspace/hackathon-plugin")
HALLMARK_SRC = os.path.expanduser("~/workspace/tmp-hallmark-research/skills/hallmark")
IMPECCABLE_SRC = "/tmp/impeccable-480/extracted/.cursor/skills/impeccable"

TASTE_HALLMARK = os.path.join(
    PLUGIN_ROOT, "new-skills/design-taste-frontend/references/hallmark")
POLISH_REF = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/reference")

HALLMARK_SHA = "7e213cb6feb4ef82733bd66a0600b2e54ca0994c"
IMPECCABLE_VERSION = "4.8.0"
IMPECCABLE_ENGINE = "0.1.18"
IMPECCABLE_WIN_SHA = ("8f61e96b0c97001546a824d79b44f46b423b560f3eb1a0cc44a8695a1b395d9f")


def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")


def copy_with_header(src, dst, header):
    """Verbatim upstream file with an attribution header prepended."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    body = open(src, encoding="utf-8").read()
    open(dst, "w", encoding="utf-8").write(header + body)
    print(f"copied+header {src} -> {dst}")


def main():
    # --- sanity: sources exist ---
    assert os.path.isdir(HALLMARK_SRC), f"missing {HALLMARK_SRC}"
    assert os.path.isdir(IMPECCABLE_SRC), f"missing {IMPECCABLE_SRC}"
    # Verify the Hallmark checkout is at the pinned SHA.
    import subprocess
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=os.path.expanduser(
            "~/workspace/tmp-hallmark-research"),
        capture_output=True, text=True, check=True).stdout.strip()
    assert head == HALLMARK_SHA, f"Hallmark HEAD {head} != pinned {HALLMARK_SHA}"
    print(f"Hallmark HEAD verified: {head}")

    # ============ HALLMARK ============
    # scripts (verbatim, upstream layout preserved so relative paths resolve:
    # theme.mjs reads ../references/themes/index.json; photos.json sits next
    # to the scripts, as upstream)
    for name in ("theme.mjs", "sloplint.mjs", "sloplint-render.mjs",
                 "photos.json"):
        copy_file(os.path.join(HALLMARK_SRC, "scripts", name),
                  os.path.join(TASTE_HALLMARK, "scripts", name))
    # references (verbatim)
    for name in ("gates.md", "review-hero.md", "review-finish.md",
                 "redesign.md"):
        copy_file(os.path.join(HALLMARK_SRC, "references", name),
                  os.path.join(TASTE_HALLMARK, "references", name))
    # theme catalog: 50 .md + index.json + README.md, TEXT ONLY (no .jpg)
    themes_src = os.path.join(HALLMARK_SRC, "references", "themes")
    themes_dst = os.path.join(TASTE_HALLMARK, "references", "themes")
    os.makedirs(themes_dst, exist_ok=True)
    md_files = sorted(f for f in os.listdir(themes_src)
                      if f.endswith(".md") and f != "README.md")
    assert len(md_files) == 50, f"expected 50 theme .md, found {len(md_files)}"
    for f in md_files:
        copy_file(os.path.join(themes_src, f), os.path.join(themes_dst, f))
    copy_file(os.path.join(themes_src, "index.json"),
              os.path.join(themes_dst, "index.json"))
    copy_file(os.path.join(themes_src, "README.md"),
              os.path.join(themes_dst, "README.md"))
    jpg = [f for f in os.listdir(themes_src) if f.endswith(".jpg")]
    assert len(jpg) == 50, f"expected 50 theme .jpg upstream, found {len(jpg)}"
    assert not any(f.endswith(".jpg") for f in os.listdir(themes_dst)), \
        "no .jpg may be staged (text-only catalog)"
    print("theme catalog: 50 .md + index.json + README.md staged, 0 .jpg")

    # condensed Hallmark floor (written for this plugin; rules condensed
    # from skills/hallmark/SKILL.md "The Floor", gate numbers kept)
    floor = """<!-- Hallmark floor, condensed for this plugin.
Source: Nutlope/hallmark, MIT, v2.0.0, HEAD 7e213cb6feb4ef82733bd66a0600b2e54ca0994c.
Upstream: skills/hallmark/SKILL.md "The Floor" (16 non-waivable rules) +
references/gates.md §1-§2 (tiers). Condensed here so the landing slice can
read the Floor without loading Hallmark's whole build playbook (Taste owns
the build). Gate numbers are Hallmark's; where a rule duplicates this
plugin's own craft floor, the stricter ban wins. -->

# Hallmark floor (condensed)

These 16 rules bind every Hallmark-dealt landing page. None is waivable,
even when nothing else is read. Above the Floor, a **Reflex** gate is a
default a model falls into, waivable on the record with a real reason, and
a **Finish** check is craft detail, answered, never blocking
(`references/gates.md` §1-§2). The full gate list is 90 clauses across 71
numbers (14 retired, never reused) + 26 Finish checks F1-F26 — see
`references/gates.md` §4-§5. (Note: older write-ups say "57 gates"; that
count does not match v2.0.0.)

1. Every colour and every font goes through a token declared at `:root`
   (or a declared theme block). No literal colour or `font-family` past
   the token block. (48)
2. Never `transition: all`. Never animate `width`, `height`, `top` or
   `left`. (10a)
3. Never one italic word inside a roman heading. (38i)
4. `overflow-x: clip` on both `html` and `body`. Never `hidden`, never
   `100vw`. (34)
5. Image-bearing grid tracks use `minmax(0, 1fr)`; display heads carry
   `overflow-wrap: break-word; min-width: 0`. (50)
6. Every interactive element has `:focus-visible`, appearing instantly.
   (26a, 15)
7. Every animation has a `prefers-reduced-motion: reduce` fallback, and
   content is visible with scripting off. (27, 62)
8. Never an invented metric, testimonial, logo wall or case-study count.
   (46a)
9. Never an eyebrow, and never a label in tracked capitals or small caps:
   labels, captions, table heads, tags and nav links are the body face
   (or the theme's label face), a step smaller, sentence or lower case,
   untracked. (54, 67)
10. Never middle-dot-joined meta strings, arrows glued to link text, or
    decorative status dots. (63)
11. Never a purple-to-blue gradient, a card inside a card, an emoji as an
    icon, or a hand-drawn browser or OS window. (2a, 4, 30a, 47a)
12. The hero's headline, one sentence and primary action are all visible
    at 1280 x 800 without scrolling. (44b)
13. About 80 words on any one screen; the hero's text is the headline,
    one sentence and its actions. (58)
14. The container is capped and centred: at 1920 the gutters grow, the
    measure and the grids do not. (44d)
15. The first non-empty line of the CSS source is the Hallmark stamp,
    then the critique line, then any waivers. (20) — applies to files
    the landing slice writes on a Hallmark-dealt page, not to the whole
    codebase.
16. If Node is available, run `node <skill>/references/hallmark/scripts/sloplint.mjs <output> --render`
    before handing back. Fix every `FAIL`; fix or waive every `REFLEX`.
    (The render tier needs `puppeteer-core@25.17.0` + Chrome; without
    them run the static tier only and record that the render tier did
    not run.)

## The 6-axis pre-emit self-critique (gates.md §3)

Before the sweep, score the planned page 1-5 on six axes; anything under 3
triggers a revision first. Stamp line:
`/* Hallmark · pre-emit critique: P5 H4 E5 S3 R5 V4 · weakest: S, <fix> */`
— name the weakest axis + the fix taken; straight 5s name what was cut.

- **P**hilosophy — 3: has a tone; 5: has an argument a reader could
  disagree with.
- **H**ierarchy — 3: needs a second look; 5: survives the squint test.
- **E**xecution — 3: two or three loose details; 5: would pass the gates
  first time.
- **S**pecificity — 3: fits the category; 5: could belong to no other
  product.
- **R**estraint — 3: keeps one decoration too many; 5: lost something
  you liked.
- **V**ariety — 3: differs from the log on three of six structural axes;
  5: shares almost nothing with the last three runs.
"""
    floor_path = os.path.join(TASTE_HALLMARK, "references",
                              "hallmark-floor.md")
    os.makedirs(os.path.dirname(floor_path), exist_ok=True)
    open(floor_path, "w", encoding="utf-8").write(floor)
    print(f"wrote {floor_path}")

    provenance_h = f"""# Hallmark — provenance (staged, scoped)

Source: **Nutlope/hallmark**, by Hassan El Mghari (nutlope) / Together AI,
MIT license. Version **2.0.0**, pinned HEAD commit
`{HALLMARK_SHA}` (2026-11-10 18:01 UTC; verified by `git rev-parse HEAD`
on the sparse checkout before staging). The repo has **no GitHub
releases and no tags** — the SHA is the pin.

## What was staged (text only, no binaries, no images)

- `references/themes/` — the 50-theme material catalog: 50 `.md` files +
  `index.json` + `README.md` (~424 KB text). The 50 `.jpg` pictures were
  NOT staged: the deal/pick step degrades to header + material
  description (the theme file's `material` line + feel paragraph) instead
  of the picture. The `.jpg`s total 5.0 MB and remain available upstream.
- `scripts/theme.mjs` — `deal` (3 themes, pick 1), `draw`, `photos`,
  `log`, `index`, `validate`, `check`, `scaffold`. Only `deal` (+ `log`,
  `photos`, `check`, `index`, `validate`) is wired in this plugin; `draw`
  and `scaffold` are NOT used — Taste owns shape + scaffold.
- `scripts/sloplint.mjs` — the mechanical gate checker (zero dependencies,
  Node 18+). `scripts/sloplint-render.mjs` — the render tier (needs
  `puppeteer-core@25.17.0` + Chrome; static tier runs without them).
- `scripts/photos.json` — 755 Wikimedia photo URLs + metadata only, no
  image bytes (needed by `theme.mjs photos`).
- `references/gates.md` — the full gate list: 90 clauses, 71 numbers
  (14 retired), tiers 39 Floor / 50 Reflex / 1 Ledger, + 26 Finish
  checks F1-F26. (Older write-ups say "57 gates" — that count does not
  match v2.0.0.)
- `references/review-hero.md`, `references/review-finish.md` — the
  fresh-context reviewer prompts (hero review, finish review).
- `references/redesign.md` — the redesign flow (keeps content + wiring).
- `references/hallmark-floor.md` — condensed Floor + 6-axis critique,
  written for this plugin from upstream SKILL.md + gates.md §3.

## What was NOT staged (and why)

- `skills/hallmark/SKILL.md` — Hallmark is NOT a separate skill in this
  plugin and has no `/hallmark` command; Taste leads landing builds and
  deals from this catalog. No `study` verb exists in v2.0.0 (verbs are
  build / redesign / audit only).
- The 50 `.jpg` theme pictures (see above).
- `references/layout.md`, `anatomy.md`, `craft.md`, `direction.md`,
  `imagery.md`, `patterns.md`, `flow.md`, `genres/`, `macrostructures/`,
  `texture.md`, etc. — Hallmark's build playbook; Taste owns the build.
- `scripts/capture.mjs`, `scripts/picture.mjs` — covered by polish-pass
  `capture.mjs` + browser-qa.
- `scripts/install.mjs`, `scripts/install-hook.mjs`,
  `scripts/lint-hook.mjs` — no Cursor edit-time hook exists upstream;
  this plugin has its own hooks.
- `scripts/imagegen.mjs` — Together AI FLUX image generation (needs
  `TOGETHER_API_KEY`). Never wired; the plugin never generates images.
- `scripts/refcheck.mjs` — upstream CI consistency gate, not runtime.
- `site/` (usehallmark.com demo pages, ~228 MB repo bulk) and `eval/` —
  never checked out.

## Windows notes (primary platform)

- `sloplint-render.mjs` resolves Chrome via `CHROME_PATH` first, then a
  hardcoded list that includes only the 64-bit path
  `C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe` (32-bit and
  per-user `%LOCALAPPDATA%` installs are NOT listed). If Chrome is not
  found, set `CHROME_PATH` (PowerShell:
  `$env:CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'`;
  Git Bash: `CHROME_PATH='C:/Program Files/Google/Chrome/Application/chrome.exe'`).
- All skill shell commands are `node <script> …` (shell-agnostic); no
  `.sh`/`.bat`/`.ps1`, no curl/wget/pipe-to-shell, no chmod.
- `theme.mjs log --entry '<json>'` examples use single quotes (Git Bash
  syntax); in PowerShell use double quotes with inner-quote escaping.
- Render tier needs `puppeteer-core@25.17.0` (pinned; `npm i -g
  puppeteer-core@25.17.0` when it is missing). It cannot reuse the
  plugin's Playwright 1.65.0 as a drop-in: `sloplint-render.mjs` is written
  directly against the Puppeteer API. The browser binary itself is shared
  (system Chrome), so no second browser download.
"""
    prov_path = os.path.join(TASTE_HALLMARK, "PROVENANCE.md")
    open(prov_path, "w", encoding="utf-8").write(provenance_h)
    print(f"wrote {prov_path}")

    # ============ IMPECCABLE ============
    imp_header = f"""<!--
Impeccable reference, staged verbatim (this header added by the plugin).
Source: pbakaus/impeccable, Apache License 2.0, skill release skill-v4.8.0
(universal.zip, 2026-10-26), engine v{IMPECCABLE_ENGINE}. npm package
impeccable@{IMPECCABLE_VERSION} (tarball shasum
f344aaa43511ea0ccadce1a42c860f5990953430). npm latest is 4.8.2 — 4.8.0 is
pinned deliberately (the skill-v4.8.0 release is the verified one).
See impeccable-PROVENANCE.md in this directory for the full gap table.
-->
"""
    for name, staged in (("craft-floor.md", "impeccable-craft-floor.md"),
                         ("critique.md", "impeccable-critique.md"),
                         ("onboard.md", "impeccable-onboard.md"),
                         ("extract.md", "impeccable-extract.md")):
        copy_with_header(
            os.path.join(IMPECCABLE_SRC, "reference", name),
            os.path.join(POLISH_REF, staged), imp_header)

    # detector rules: extract the 62-rule list from the --list-rules --json
    # golden file (the file on disk is a test-runner wrapper; stdout holds
    # the real JSON list).
    golden = json.load(open("/tmp/impeccable-480/detect-list-rules-json.json",
                            encoding="utf-8"))
    rules = json.loads(golden["stdout"])
    assert isinstance(rules, list) and len(rules) == 62, \
        f"expected 62 detector rules, got {len(rules)}"
    cats = {}
    for r in rules:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    assert cats == {"slop": 31, "quality": 31}, f"category split {cats}"
    rules_path = os.path.join(POLISH_REF, "impeccable-detector-rules.json")
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {rules_path} (62 rules: 31 slop + 31 quality)")

    prov_i = f"""# Impeccable — provenance (staged, scoped — gap analysis)

Source: **pbakaus/impeccable**, by Paul Bakaus, Apache License 2.0.
Skill release **skill-v4.8.0** (`universal.zip`, 18,116,588 bytes,
2026-10-26), engine **v{IMPECCABLE_ENGINE}**. npm package
`impeccable@{IMPECCABLE_VERSION}` (tarball shasum
`f344aaa43511ea0ccadce1a42c860f5990953430`, `engines: node >=18.19.0`).
npm latest is 4.8.2 (2026-11-09) — 4.8.0 is pinned deliberately because
the skill-v4.8.0 release is the verified one. Repo HEAD at staging time:
`c1e0e5492fbb524f5df84d635ecfae7dc438ec45` (2,825 commits, 107,702 stars).
Engine SHA-256 (from upstream `engine-checksums.txt`):
`impeccable-windows-x64.exe {IMPECCABLE_WIN_SHA}`
(linux-x64 `736ed785…f71f648`, darwin-arm64 `543ee2f7…c8a9e1`).

## What was staged (in this directory)

- `impeccable-craft-floor.md` — verbatim `reference/craft-floor.md`
  (44 lines): read before any UI edit; bans are absolute.
- `impeccable-critique.md` — verbatim `reference/critique.md`
  (819 lines): scored UX review (heuristics, persona testing,
  anti-pattern detection, ranked fixes).
- `impeccable-onboard.md` — verbatim `reference/onboard.md`
  (234 lines): first-run flows, empty states, activation / aha moment.
- `impeccable-extract.md` — verbatim `reference/extract.md`
  (69 lines): consolidate repeated patterns/tokens/components into the
  design system.
- `impeccable-detector-rules.json` — the 62 deterministic detector rules
  (31 slop + 31 quality; 44 warning, 16 advisory, 2 error), extracted
  from the `--list-rules --json` golden file at tag skill-v4.8.0. The
  rule registry itself lives in the engine (Rust); the skill ships no
  rule list, so this file is the plugin's lookup copy.

## Detector wiring

Invoke as `npx impeccable@{IMPECCABLE_VERSION} detect <paths>` (pinned;
no API key, no LLM). The engine binary is NOT bundled: on first run it
downloads from the pinned release and is SHA-256-verified against the
checksums file (fails closed on mismatch). Source scans use pattern rules
only; rendered-page rules (contrast, line-length, occlusion) need a URL
or dev server + installed Chrome/Edge. On Windows run it from Git Bash
or PowerShell (`npx` is cross-platform); the engine cache is
`%USERPROFILE%\\.impeccable\\bin\\0.1.18\\`. The shipped
`.cursor/hooks.json` detector hook is POSIX-only and likely broken on
Windows (Cursor runs hook commands through PowerShell) — it is NOT wired;
the detector runs as a named step in polish-pass instead, and the hook is
a live-smoke-test item.

## DESIGN.md mapping (no new state files)

Impeccable's `PRODUCT.md`/`DESIGN.md` are NOT introduced as parallel
state: `PRODUCT.md` maps to this plugin's `docs/decision-record.md` +
`docs/scope.md`; `DESIGN.md` maps to `docs/design-tokens.md` +
`design-system/<project-slug>/MASTER.md`. The detector's
`design-system-*` rules (font/color/radius/font-size drift) read the
project's token file (`docs/design-tokens.md`) instead of DESIGN.md.

## Gap table (24 commands + the rest)

- COVERED, not staged: `polish` (= polish-pass), `distill`, `harden`,
  `clarify`, `adapt`, `optimize`, `typeset`, `layout` (all have a
  polish-pass lens of the same name); `animate` (polish-pass animate
  lens + ui-ux-pro-max motion implementation — `data/motion.csv`, 17
  GSAP presets, `--motion` dial tiers Subtle/Standard/Complex,
  quick-reference.md §7 spring-physics/easing/exit-faster-than-enter —
  + `make-interfaces-feel-better` owns feel/timing decisions and the
  motion-* skills own implementation; no framer-motion content anywhere,
  GSAP only).
- MAPPED, not staged: `init` → grill-me decision record;
  `document` → design-tokens.md/MASTER.md; `shape` → grill-me +
  hackathon-scope + Taste deal (visual probes covered by Taste);
  `audit` → adversarial audit + browser-qa (covered-in-part);
  `craft` → deprecated alias upstream, skipped.
- ADDED (this round): `extract`, `critique`, `onboard` references above;
  the detector (62 rules); the craft floor.
- FLAGGED, not added (decision items for Anish — see the coordinator's
  final report): direction lenses `bolder`, `quieter`, `colorize`,
  `decolorize`, `delight`, `overdrive` (their job is to CHANGE a design's
  direction, which clashes with the standing rule that polish-pass never
  restyles; note `overdrive`'s spring-physics content is partly covered
  by ui-ux-pro-max quick-reference.md §7, and the GSAP Complex tier
  covers pin/Flip/SplitText scroll choreography — the missing part is the
  direction change itself); `live` + `generate` (live browser variant
  iteration — genuinely missing, but interactive, needs a running dev
  server + the 553 KB live-browser.js engine scripts, and cannot run in
  the unattended first build).
"""
    prov_i_path = os.path.join(POLISH_REF, "impeccable-PROVENANCE.md")
    open(prov_i_path, "w", encoding="utf-8").write(prov_i)
    print(f"wrote {prov_i_path}")

    print("STAGING DONE")


if __name__ == "__main__":
    main()
