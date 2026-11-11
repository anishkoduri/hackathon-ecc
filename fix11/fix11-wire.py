#!/usr/bin/env python3
"""Fix program #11 — wire the Hallmark + Impeccable staged additions into
the staged SKILL.md files (build.sh copies these verbatim into the built
plugin). Every substitution asserts exactly one match in its staged file.
Run once, then rebuild with build.sh.

Does NOT touch: the 4 polish-pass patch-(f) old-strings in build.sh, the
Taste description-replacement old-string, any GATE/carve-out line, or the
fix-#1-#10 mechanisms. The ui-ux-pro-max wiring is a build.sh runtime patch
(upstream file, copied fresh each build) — it lives in build.sh itself,
placed LAST before STEP 5, not here.
"""
import os
import sys

ROOT = os.path.expanduser("~/workspace/hackathon-plugin")


def sub(path, old, new, label):
    p = os.path.join(ROOT, path)
    text = open(p, encoding="utf-8").read()
    n = text.count(old)
    assert n == 1, f"{label}: {path}: pattern found {n}x (want 1): {old[:70]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
    print(f"ok {label}: {path}")


TASTE = "new-skills/design-taste-frontend/SKILL.md"

# --- Taste 1: Hallmark theme deal (step 4, after the palette deal) ---
sub(TASTE,
    "   the comment at the top of `<body>`, and build exactly that (a short page drops what it has no section for: `sections.md` section 4).",
    """   the comment at the top of `<body>`, and build exactly that (a short page drops what it has no section for: `sections.md` section 4).

   **Deal a Hallmark theme for the direction first.** Before the palette deal above, run the Hallmark theme deal — it picks the material world the page lives in, so the direction is dealt, not invented:

   ```bash
   node <skill>/references/hallmark/scripts/theme.mjs deal --genre <genre> --prompt "<the brief>" --log .hallmark/log.json
   ```

   Map the page kind to a Hallmark genre for the deal: tech/dark/atmospheric → `atmospheric`; SaaS/devtool/B2B → `modern-minimal`; playful/fun/kids/games → `playful`; anything else → `editorial` (default). The deal returns 3 themes from the 50-theme catalog (`references/hallmark/references/themes/`, `index.json`); pick the one whose material can carry the brief — read the theme file's header (paper/display/accent/posture), its `material` line, and its feel paragraph. The theme pictures (`.jpg`) are NOT staged in this plugin, so pick by the material description, not the picture. Take the theme's palette balance, type voice, surfaces, and Range (the sections it makes without a photograph); the theme never sets what the page contains or in what order. The theme's Tokens block is the page's `:root` tokens — use it in place of `start.mjs css` for the palette (the hero deal, moments, and nav/footer/close lists above still run). If the dealt theme clashes with the client's own logo or photographs, re-deal once (`--reroll 1`); the client's own colours go through `start.mjs brand` instead. Do NOT use `theme.mjs draw` or `theme.mjs scaffold` — Taste owns shape and scaffold. The Hallmark Floor binds the page: read `references/hallmark/references/hallmark-floor.md` (16 non-waivable rules + the 6-axis pre-emit critique) and follow it; where it and this skill disagree, the stricter ban wins.""",
    "taste-deal")

# --- Taste 2: Impeccable craft floor read (step 4a) ---
sub(TASTE,
    "Anything already fixed by the deal above is named, not re-decided; only the missing pieces (notably the states and the semantic token meanings) are defined here.",
    """Anything already fixed by the deal above is named, not re-decided; only the missing pieces (notably the states and the semantic token meanings) are defined here. Also read the Impeccable craft floor (`skills/polish-pass/reference/impeccable-craft-floor.md` in the plugin) before building any UI: its bans are absolute — a pinned brief never overrides a ban — and where it and this skill disagree, the stricter ban wins.""",
    "taste-4a-floor")

# --- Taste 3: Hallmark redesign flow (before step 5 Build) ---
sub(TASTE,
    "5. **Build.** In `starter.html`: set `<html lang data-type data-radius data-buttons data-motion>`",
    """**Redesign of an existing page (keeping content + wiring).** When the job is a full-page redesign that keeps every fact, link, form, field, handler, route, id, and test hook, follow the Hallmark redesign flow (`references/hallmark/references/redesign.md`): record the before-state (`sloplint --before`, links/fields/handlers/headings + screenshots to `.hallmark/before*`), build, then `sloplint --kept` — anything lost is `FAIL kept` / `WARN kept`. Depths: **full** (system + composition change; default), **restyle** (system only, keep the layout), **polish** (only what a gate names).

5. **Build.** In `starter.html`: set `<html lang data-type data-radius data-buttons data-motion>`""",
    "taste-redesign")

# --- Taste 4: Hallmark sloplint + hero review (step 6, before step 7) ---
sub(TASTE,
    "   (a word inside the client's name, as the logo or the title writes it, is not counted: one WARN).",
    """   (a word inside the client's name, as the logo or the title writes it, is not counted: one WARN).

   **Hallmark sloplint.** Before the report, run the Hallmark gate checker on the built page:

   ```bash
   node <skill>/references/hallmark/scripts/sloplint.mjs index.html --render
   ```

   The static tier always runs. The render tier needs `puppeteer-core` + Chrome: if `puppeteer-core` is missing, install the pinned version (`npm i -g puppeteer-core@25.17.0` — it cannot reuse the plugin's Playwright as a drop-in; the render script is written against the Puppeteer API); if Chrome is not found, set `CHROME_PATH` to the Chrome install (on Windows usually `C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe`). If the render tier cannot run, run the static tier only and record that the render tier did not run — never claim a render pass. Fix every `FAIL`; fix or waive every `REFLEX` (waivers recorded in the CSS stamp, per `references/hallmark/references/gates.md`).

   **Hallmark hero review.** Once the hero is built and shot, run the hero review in a fresh context: a sub-agent if the harness has one (it reads `references/hallmark/references/review-hero.md` and follows it — you do not read the prompt yourself; pass the hero screenshots, the stamp's first two lines, and the Picks Material + Signature rows as file paths); otherwise re-read the prompt yourself and judge from the screenshots alone. Act on its first word (`ship` / `fix`); findings join the fix batch.""",
    "taste-sloplint-hero")

POLISH_SKILL = "round2-skills/polish-pass/SKILL.md"

# --- polish-pass SKILL 1: craft floor (+ Impeccable floor) ---
sub(POLISH_SKILL,
    "4. **Meet the craft floor.** Read [reference/craft-floor.md](reference/craft-floor.md) before any UI edit. Its bans hold unless the project's design notes explicitly record an exception (accessibility and dark-pattern bans never yield), and its **default standard** (WCAG 2.2 AA, evergreen browsers, readable with JS off, reduced motion, LCP < 2.5s on mobile, no new fonts/deps without approval) applies unless the design notes record an exception.",
    "4. **Meet the craft floor.** Read [reference/craft-floor.md](reference/craft-floor.md) before any UI edit. Its bans hold unless the project's design notes explicitly record an exception (accessibility and dark-pattern bans never yield), and its **default standard** (WCAG 2.2 AA, evergreen browsers, readable with JS off, reduced motion, LCP < 2.5s on mobile, no new fonts/deps without approval) applies unless the design notes record an exception. Also read the Impeccable craft floor ([reference/impeccable-craft-floor.md](reference/impeccable-craft-floor.md)) before the first edit: its bans are absolute (a pinned brief never overrides a ban); where the two floors disagree, the stricter ban wins.",
    "polish-floor")

# --- polish-pass SKILL 2: detector (+ Impeccable detector) ---
sub(POLISH_SKILL,
    "5. **Run the detector** on edited or critiqued source files: `node <skill dir>/scripts/detect.mjs <paths>`. Treat findings as evidence to verify, not verdicts. A clean scan does not prove quality.",
    "5. **Run the detector** on edited or critiqued source files: `node <skill dir>/scripts/detect.mjs <paths>`. Treat findings as evidence to verify, not verdicts. A clean scan does not prove quality. Then run the Impeccable detector on the same paths: `npx impeccable@4.8.0 detect <paths>` (pinned; no API key, no LLM — the engine binary downloads once from the pinned release and is SHA-verified). It checks 62 rules ([reference/impeccable-detector-rules.json](reference/impeccable-detector-rules.json)), including rendered-page rules the static scan cannot see — run it against the running app's URL as well as the source when the app is running. Treat its findings the same way: evidence to verify, not verdicts. On Windows run it from Git Bash or PowerShell (`npx` is cross-platform); if a rendered-URL scan cannot find Chrome, set `CHROME_PATH` to the Chrome install.",
    "polish-detector")

# --- polish-pass SKILL 3: DESIGN.md mapping ---
sub(POLISH_SKILL,
    "A brief or explicit user instruction overrides your taste.",
    """A brief or explicit user instruction overrides your taste.

The Impeccable detector's `design-system-*` rules read `DESIGN.md`; in this plugin they read the project's token file instead — `docs/design-tokens.md` when the landing slice wrote it, otherwise the project's token/theme file. `PRODUCT.md` (Impeccable's product record) maps to `docs/decision-record.md` + `docs/scope.md` in this plugin; no `PRODUCT.md` / `DESIGN.md` files are introduced.""",
    "polish-designmd-map")

# --- polish-pass SKILL 4: attribution (round-2 additions + Hallmark) ---
sub(POLISH_SKILL,
    "Provenance note: pristine's lens set mirrors the commands of pbakaus/impeccable without crediting it. That is worth recording: if this skill is ever published or shared, the impeccable lineage should be credited alongside pristine.",
    """Provenance note: pristine's lens set mirrors the commands of pbakaus/impeccable without crediting it. That is worth recording: if this skill is ever published or shared, the impeccable lineage should be credited alongside pristine.

Round 2 additions (Nov 2026, gap analysis vs Impeccable 4.8.0): the Impeccable detector (`npx impeccable@4.8.0 detect`, 62 rules — see `reference/impeccable-detector-rules.json`), the Impeccable craft floor, and the `critique`, `onboard`, and `extract` reference playbooks (see `reference/impeccable-PROVENANCE.md` for the full gap table). The direction lenses (bolder, quieter, colorize, decolorize, delight, overdrive) and the live-variant mode were deliberately left out — the first clash with this skill's never-restyles rule, the second needs an interactive browser session and cannot run in an unattended build.

Hallmark credit: the theme catalog, gate checker, and reviewer prompts wired into `design-taste-frontend` and the Verify stage come from **Hallmark** by Hassan El Mghari (nutlope) / Together AI (MIT, v2.0.0) — see `skills/design-taste-frontend/references/hallmark/PROVENANCE.md`.""",
    "polish-attribution")

POLISH_MD = "round2-skills/polish-pass/reference/polish.md"

# --- polish.md Step 2: Impeccable detector in baseline ---
sub(POLISH_MD,
    "2. Run the detector on the target's source: `node <skill dir>/scripts/detect.mjs <paths>`.",
    "2. Run the detector on the target's source: `node <skill dir>/scripts/detect.mjs <paths>`. Then run the Impeccable detector on the same paths: `npx impeccable@4.8.0 detect <paths> [--json]` (pinned; no API key, no LLM). It checks 62 rules ([reference/impeccable-detector-rules.json](reference/impeccable-detector-rules.json)) including rendered-page rules the static scan cannot see — run it against the running app's URL as well as the source when the app is running. Treat its findings the same way: evidence to verify, not verdicts.",
    "polishmd-step2-detector")

# --- polish.md Step 2: critique playbook trigger ---
sub(POLISH_MD,
    "3. Do a **quick internal score** using the Dimensions and calibration in [scoring.md](scoring.md): score each Dimension, list the gaps. Don't print a full report; keep it short.",
    "3. Do a **quick internal score** using the Dimensions and calibration in [scoring.md](scoring.md): score each Dimension, list the gaps. Don't print a full report; keep it short. If any Dimension scores below 6, run the Impeccable critique playbook ([reference/impeccable-critique.md](reference/impeccable-critique.md)) — a scored review with persona testing and ranked fixes — and fold its Priority fixes into the Lens plan.",
    "polishmd-step2-critique")

# --- polish.md Step 4: Impeccable floor + onboard + extract ---
sub(POLISH_MD,
    "1. Read [craft-floor.md](craft-floor.md) once before the first edit.",
    "1. Read [craft-floor.md](craft-floor.md) once before the first edit, and the Impeccable craft floor ([reference/impeccable-craft-floor.md](reference/impeccable-craft-floor.md)) — its bans are absolute; where the two floors disagree, the stricter ban wins.",
    "polishmd-step4-floor")

sub(POLISH_MD,
    "2. For each planned Lens, read its file in `reference/lenses/` and apply it to the target. When animate runs, build from [patterns/motion-recipes.md](patterns/motion-recipes.md); when harden runs on a data-driven component, test it against [patterns/worst-case-data.md](patterns/worst-case-data.md).",
    "2. For each planned Lens, read its file in `reference/lenses/` and apply it to the target. When animate runs, build from [patterns/motion-recipes.md](patterns/motion-recipes.md); when harden runs on a data-driven component, test it against [patterns/worst-case-data.md](patterns/worst-case-data.md). When harden runs on a first-run, empty-state, or activation surface, also read [reference/impeccable-onboard.md](reference/impeccable-onboard.md) and apply its first-run/empty-state/activation guidance (fix-only: do not invent onboarding copy or product claims). When consistency finds the same pattern or value repeated in three or more places, consolidate it into the shared system following [reference/impeccable-extract.md](reference/impeccable-extract.md) (pull repeated patterns/tokens/components into the design system; never extract a one-off).",
    "polishmd-step4-onboard-extract")

# --- polish.md Step 5: Impeccable detector re-run in Verify ---
sub(POLISH_MD,
    "2. Re-run the detector on edited files. Fix real findings. Accept a flagged item only after you've verified it's safe, and record why in the report (e.g. `outline: none` is fine only when you confirmed a visible `:focus-visible` replacement such as a ring or border, in light and dark).",
    "2. Re-run the detector on edited files. Fix real findings. Accept a flagged item only after you've verified it's safe, and record why in the report (e.g. `outline: none` is fine only when you confirmed a visible `:focus-visible` replacement such as a ring or border, in light and dark). Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`), and fix real findings the same way.",
    "polishmd-step5-detector")

ORCH = "new-skills/orchestrate/SKILL.md"

# --- orchestrate: Hallmark audit as Verification-stage item 6 ---
sub(ORCH,
    "**5. Visual iteration loop (`browser-qa` — after tests pass, before deploy).** Run the app and invoke `browser-qa`'s visual iteration: capture and inspect the ACTUAL rendered interface (desktop + mobile), not a description of it. `browser-qa` returns the top 5 visual/usability problems; fix them, then re-inspect — fixes route by the routing rule (mechanical fix → fast-worker; design flaw → deep-reasoner), and the same capped 2-round fix loop that bounds reviewer defect lists bounds visual-loop fixes too (at most 2 fix rounds per problem list; past that, mark the item blocked with evidence and move on). Cap: **max 3 rounds total** of the inspect → fix → re-inspect loop, then stop, note diminishing returns in the final report, and move on — never an unbounded loop. If the app cannot run, record that as blocked with evidence instead of iterating.",
    """**5. Visual iteration loop (`browser-qa` — after tests pass, before deploy).** Run the app and invoke `browser-qa`'s visual iteration: capture and inspect the ACTUAL rendered interface (desktop + mobile), not a description of it. `browser-qa` returns the top 5 visual/usability problems; fix them, then re-inspect — fixes route by the routing rule (mechanical fix → fast-worker; design flaw → deep-reasoner), and the same capped 2-round fix loop that bounds reviewer defect lists bounds visual-loop fixes too (at most 2 fix rounds per problem list; past that, mark the item blocked with evidence and move on). Cap: **max 3 rounds total** of the inspect → fix → re-inspect loop, then stop, note diminishing returns in the final report, and move on — never an unbounded loop. If the app cannot run, record that as blocked with evidence instead of iterating.

**6. Hallmark audit (landing/company pages only).** After the visual loop, run the Hallmark audit on the built landing page: `node <plugin>/skills/design-taste-frontend/references/hallmark/scripts/sloplint.mjs <built page> --render` (static tier always; render tier needs `puppeteer-core@25.17.0` + Chrome — install the pinned version if it is missing; on Windows set `CHROME_PATH` if Chrome is not found; if the render tier cannot run, run the static tier only and record that the render tier did not run — never claim a render pass). Fix every `FAIL`; fix or waive every `REFLEX` (waivers on the record, in the CSS stamp). Then the 6-axis pre-emit self-critique (`skills/design-taste-frontend/references/hallmark/references/gates.md` §3, condensed in `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md`): score the page 1–5 on Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety; any axis under 3 joins the fix list with the rest of Verify's findings (same capped 2-round fix loop). Then the Hallmark finish review in a fresh context — a sub-agent if the harness has one (it reads `skills/design-taste-frontend/references/hallmark/references/review-finish.md` and follows it; you do not read the prompt yourself — pass the render-tier screenshots, the stamp theme/idea line, the theme file, and the hero review's findings as file paths); otherwise re-read the prompt yourself and judge from the screenshots alone. Act on its first word (`recapture` / `rebuild` / `fix` / `ship`); findings join the fix batch. This is a named check, not a user gate: it never asks the user anything and never blocks the run on anything but the page's own defects.""",
    "orch-verify-hallmark")

print("WIRING DONE")
