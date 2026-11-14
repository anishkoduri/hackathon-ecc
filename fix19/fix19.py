#!/usr/bin/env python3
"""Fix program #19: font identity, forced font choice, the Tiempos body
font (free stand-in Fraunces), and thought-out decisions across the FULL
experience (fix #19 F2/F3/F4/D19).

Back-ports the Campus Eats font repair (Nov 11 evening) and Anish's two
follow-up directives into the package as enforceable rules, so a future
build cannot ship fonts that render differently per platform, cannot fall
back to a system font, cannot pick a generic font, cannot set body text
in anything but the Tiempos font (or its recorded stand-in), and cannot
make a UI decision without a thought-out, full-experience reason recorded
for it.

Rules (SPEC.md section 2):
  F2  fonts render identically on iPhone and web — static bundled files
      only (extends fix #15 C2)
  F3  font choice is unique and interesting — forced, never a default
      (extends fix #15 C1, fix #17 F1)
  F4  plain/body text uses Tiempos (free stand-in Fraunces at 1.55
      line-height)
  D19 every UI decision carries a thought-out reason across the FULL
      experience (Motion / Theme / Texture / Visuals / Techniques /
      Colors, one line each)

BANNED-TERM REWORDING (fix #16 scrub; see MANIFEST.md):
  The SPEC's F4 texts name the company "Anthropic" and the assistant
  "Claude" — BOTH tokens are banned in the built tree (fix #16 scrub:
  claude/codex/anthropic/opus/sonnet/haiku/composer-2.5, case-insensitive).
  The parent task's suggested rewording ("the font Claude's reading text
  is set in") still contains the banned token "claude", so it was NOT
  used. Instead F4_RULE / F4_APP are reworded token-free: the title names
  Tiempos directly, and the body drops the attribution clause while
  keeping every functional fact (Tiempos, Klim, paid, NOT bundleable,
  Fraunces stand-in, 1.55 line-height). SPEC intent preserved; neither
  token appears in any addition (preflight asserts this).

Staged-source edits (direct, build.sh copies them verbatim):
  new-skills/design-taste-frontend/SKILL.md ......... C2 replacement,
                                                    F2/F3/F4/D19 (step 4a),
                                                    STATIC19 (step 6)
  new-skills/design-taste-frontend/references/hallmark/references/themes/*.md
                                                    theme Tokens blocks:
                                                    system-ui + bare-generic
                                                    tails stripped from the
                                                    --font-* lines (30 files,
                                                    39 occurrences; the
                                                    named faces stay)
  new-skills/design-taste-frontend/scripts/start.mjs .. stack() fallback
                                                    (built-page CSS stacks)
  new-skills/design-taste-frontend/references/hallmark/scripts/theme.mjs
                                                    CUSTOM_TOKENS font lines
  new-skills/pitch-deck-video/template/shots.json
  new-skills/pitch-deck-video/template/shots.example.json
                                                    "sans" stack -> bundled
                                                    face alone
  new-skills/orchestrate/SKILL.md ................... F2/F3/F4/D19
                                                    (design-package rule),
                                                    D19_ROUTING (:100),
                                                    D19_REVIEWER (:195),
                                                    STATIC19 (Verify 5a)
  round2-skills/polish-pass/SKILL.md ................ POLISH_F19 (harmony)
  round2-skills/polish-pass/reference/lenses/typeset.md .. TYPESET_F19
                                                    (system-ui sentence
                                                    replaced) + checkbox
  ~/workspace/cursor-skills/less-flat-ui/SKILL.md ... LF_D19 (record)
Build.sh patch block (upstream, no staged source):
  skills/ui-ux-pro-max/SKILL.md ..................... F2/F3/F4/D19 app
                                                    mirrors + C1-sentence
                                                    extension
  skills/orch-build-mvp/SKILL.md .................... D19_APP (step 4),
                                                    STATIC19 (step 6)

Every substitution asserts count==1. A preflight pass checks every anchor
before any file is written, so a bad anchor aborts before touching anything.
"""
import glob
import os
import re
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
POLISH = os.path.join(PLUGIN, "round2-skills/polish-pass/SKILL.md")
TYPESET = os.path.join(PLUGIN, "round2-skills/polish-pass/reference/lenses/typeset.md")
LESSFLAT = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")
START_MJS = os.path.join(PLUGIN, "new-skills/design-taste-frontend/scripts/start.mjs")
THEME_MJS = os.path.join(PLUGIN, "new-skills/design-taste-frontend/references/hallmark/scripts/theme.mjs")
SHOTS = os.path.join(PLUGIN, "new-skills/pitch-deck-video/template/shots.json")
SHOTS_EX = os.path.join(PLUGIN, "new-skills/pitch-deck-video/template/shots.example.json")
THEMES_DIR = os.path.join(PLUGIN, "new-skills/design-taste-frontend/references/hallmark/references/themes")

# --- rule texts (SPEC section 2; F4 reworded token-free, see docstring) ---

F2_RULE = """**Fonts render identically on iPhone and web — static bundled files only (fix #19 F2 — extends fix #15 C2).** The shipped font files are STATIC instances — one file per weight (e.g. 400/500/600/700/800), generated from a variable font with fontTools instancer/subsetter where the source is variable, with the optical size baked in (opsz) and no fvar table. A variable font file is NEVER the shipped delivery format: its interpolated weights render differently under iOS vs Windows, which is exactly the bug this rule fixes — a variable font may be the generation source, never a shipped file. NO system-ui / system fallback anywhere as a live path: no `system-ui` in any font stack, no bare generic `sans-serif`/`serif` as a live path — the stack names bundled faces only, and a bundled face that fails to load is a visible failure (a finding), never silently papered over by a system font. `font-synthesis: none` (no browser-synthesised bold/italic — the synthesised weights are the ones that diverge) and `text-size-adjust: 100%` (no platform text scaling). Preload the first-paint faces. The D1 screenshot QA (desktop + mobile) confirms the SAME faces render on both widths — compare the rendered faces, not just layout; a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding, the way the v1 audit caught Bowlby falling back to a plain sans. Where the stack's default font loading serves a variable font (e.g. next/font), the build instances it to static files before shipping. Recorded in `docs/design-tokens.md`'s Type list: each face → its static files (weight → file), source, and preloads. A Type-list row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build — a static check item in step 6, never a screen verdict."""

F3_RULE = """**Font choice is unique and interesting — forced, never a default (fix #19 F3 — extends fix #15 C1, fix #17 F1).** No generic/system font as a display or body face. The pairing must be distinctive: a one-off display face with character plus a characterful body face — the pairing itself is a design decision, made THROUGH the design skills (the dealt pairing in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with a Source cell naming the exact skill text (fix #17 F1), never inherited from a framework default, a browser default, or a template. A pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build — a static check item in step 6, never a screen verdict. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2); the body face likewise."""

# REWORDED (see module docstring): SPEC title "uses the Anthropic font"
# and body "the font Claude's reading text is set in ... set at Claude's
# 1.55 reading line-height" both contain banned tokens (anthropic /
# claude). Title now names Tiempos directly; the body drops the
# attribution clause and keeps every functional fact.
F4_RULE = """**Plain/body text uses Tiempos (fix #19 F4).** Body and plain text use Tiempos (Klim, paid, NOT bundleable). The canonical free stand-in is Fraunces, set at a 1.55 reading line-height. Wherever the stand-in is used, record it explicitly as the stand-in in the Type list (face → 'Fraunces (stand-in for Tiempos)') — never present Fraunces as Tiempos. Tiempos itself is never shipped from this plugin (no paid licence); if the project holds a Tiempos licence, the licensed files replace the stand-in and the record says so. A dealt theme that names a different body face keeps it ONLY as a scoped, recorded exception in `docs/design-tokens.md` with a fix #19 D19 reason (job / considered-and-rejected / theme-fit across the six full-experience dimensions) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback). A theme body face delivered as a variable file or with a system fallback is a bug to fix, not an exception to record."""

D19_RULE = """**Every UI decision carries a thought-out reason across the FULL experience (fix #19 D19).** No silent defaults, no arbitrary picks. Each UI decision run through the skills — font, color, layout, element, treatment, motion, component, spacing — carries an explicit recorded reason in the decision record (`docs/design-tokens.md` / the decision record / `design-system/<project-slug>/MASTER.md` on app surfaces; the run ledger for the smallest flows): (1) what job it serves, (2) what was considered and rejected, (3) how it matches the theme. The reasoning must consider the FULL experience, not just the UI: every decision's recorded reason addresses SIX dimensions, one line each — **Motion** (what moves, what entrance/hover/loop it carries, or `none — <reason>`); **Theme** (how it fits the dealt theme — material, tokens, palette balance, do-nots); **Texture** (the not-flat-UI texture layer — what less-flat-ui treatment it carries, or `none — <reason>`); **Visuals** (imagery, iconography, visual treatment, what it looks like); **Techniques** (the other design techniques brought to bear — element kinds and skill techniques beyond the decision's own kind, e.g. a dealt moment, a diagram, an effect, a type moment, a craft-floor rule); **Colors** (palette tokens used, balance, contrast). A dimension that genuinely does not apply records `none — <reason>` — an explicit none, never a missing line. A decision whose recorded reasoning covers only layout/structure — the UI alone — does NOT satisfy this rule. A UI decision with no recorded reason, a missing dimension, or a layout-only reason is an incomplete build — a static check item in step 6, never a screen verdict. The audit/dry-run loop CHECKS the reasoning is present: the static checks verify every decision-record entry carries all six dimension lines, and the blind reviewer on UI diffs flags a missing dimension as a finding (minor at least). The check verifies the reasoning is PRESENT and addresses the dimensions — the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check."""

STATIC19 = """**Fix #19 static checks (all static checks, never screen verdicts).** (F2) The Type list names, per face, its static files (weight → file) with source and preloads; a row naming a variable file, a `system-ui` fallback, a bare generic fallback, or no preload is an incomplete build. (F3) The pairing is recorded with a Source cell naming the exact skill text; a pairing that is a framework default, a system stack, or a template's stock pairing is an incomplete build. (F4) Body/plain text is Tiempos or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. (D1 face check) The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths — a rendered face that is not a declared bundled face (a system font, a synthesised weight, a fallback sans) is a finding. (D19) Every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; an entry missing a dimension, or a reason covering only layout/structure, is an incomplete build."""

# --- C2 replacement (Taste step 4a, F2 folded into C2's home) --------------

C2_NEW = """Display faces are self-hosted as STATIC instances (one bundled woff2 file per weight + `@font-face` in the built page) whenever the face's character matters — a variable font file is never the shipped format, and the closest installed font is a failure, not a fallback; body faces are likewise static instances, and name their source (self-hosted static files + preloads) in `docs/design-tokens.md` (fix #19 F2, extending fix #15 C2). No `system-ui` or bare generic fallback anywhere as a live path; `font-synthesis: none` and `text-size-adjust: 100%`."""

C2_OLD = """Display faces are self-hosted (bundled woff2 + `@font-face` in the built page) whenever the face's character matters — the closest installed font is a failure, not a fallback; body faces name their source (self-hosted or link) and fallback stack in `docs/design-tokens.md` (fix #15 C2)."""

# --- orchestrate routing / reviewer extensions ------------------------------

D19_ROUTING = """ Each decision carries its fix #19 D19 reason — job served, considered-and-rejected, theme-fit — across all six full-experience dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), recorded in the decision record; Verify checks the record exists, matches what was built, AND that every decision carries all six dimension lines."""

D19_REVIEWER = """ The reviewer also checks each UI decision's recorded reason covers all six fix #19 D19 dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors) — a missing dimension, or a reason covering only layout/structure, is a finding, minor at least."""

ROUTING_OLD = """Record each decision (direction, components used, tokens) in `docs/design-tokens.md` / the decision record, and Verify checks the record exists and matches what was built."""

REVIEWER_OLD = """a missing record is a finding, minor at least."""

# --- polish-pass harmony + typeset lens + less-flat-ui ----------------------

POLISH_F19 = """ The harmony check also verifies the Type list's font-identity fields (fix #19 F2): each face names its static files (weight → file) with source and preloads, and no row names a variable file, a `system-ui` fallback, or a bare generic fallback — a row that does is a harmony divergence, recorded as candidate evidence, never a verdict. It also verifies the decision-record reasons (fix #19 D19): every decision-record entry carries all six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>` — consistency only, never a verdict."""

TYPESET_OLD = """The system font stack (`system-ui`) is a legitimate default with good optical sizing, provided weights, tracking, and scale are still deliberately tuned (check 4 applies); a custom face needs a reason (brand voice, a job system fonts can't do). Set `font-optical-sizing: auto` on variable fonts."""

TYPESET_F19 = """The system font stack (`system-ui`) is NOT a legitimate live path for a built page (fix #19 F2): a system font is a failure, not a fallback — the stack names bundled static faces only. A custom face needs a reason (brand voice, a job system fonts can't do); shipped files are static instances (one per weight, opsz baked in) — a variable font is the generation source only, never a shipped file. Set `font-optical-sizing: auto` on the static instances where the face ships an opsz axis."""

TYPESET_CHECKBOX_OLD = """- [ ] A custom typeface has a stated reason; variable fonts use `font-optical-sizing: auto`."""

TYPESET_CHECKBOX_NEW = """- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2)."""

LF_D19 = """ Treatment choices are UI decisions under fix #19 D19: each recorded treatment carries the six dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; a treatment recorded with only a layout/structure reason does not satisfy the rule."""

# --- app-surface mirrors (same rules, app homes) ---------------------------

F2_APP = """**Fonts render identically on iPhone and web — static bundled files only (fix #19 F2, app surfaces).** App surfaces ship static font instances only (one file per weight); a variable font file is never the shipped format; no `system-ui` or bare generic fallback as a live path; `font-synthesis: none`, `text-size-adjust: 100%`; preload the first-paint faces. The D1 screenshot pass (desktop + mobile) confirms the same faces render on both widths. Recorded in `design-system/<project-slug>/MASTER.md` (face → static files, source, preloads). The full F2 rule lives in `design-taste-frontend` step 4a."""

F3_APP = """**Font choice is unique and interesting — forced (fix #19 F3, app surfaces).** No generic/system font as a display or body face on app surfaces; the pairing is distinctive, made through this skill's type scale, and recorded in MASTER.md with a Source cell. A framework-default, system-stack, or template-stock pairing is an incomplete build. The full F3 rule lives in `design-taste-frontend` step 4a."""

# REWORDED title (see module docstring): SPEC title "uses the Anthropic
# font" contains the banned token; title now names Tiempos directly.
F4_APP = """**Plain/body text uses Tiempos (fix #19 F4, app surfaces).** Body and plain text use Tiempos, or the recorded stand-in 'Fraunces (stand-in for Tiempos)' at 1.55 line-height; a theme body face kept without a scoped, recorded exception is an incomplete build. The full F4 rule lives in `design-taste-frontend` step 4a."""

D19_APP = """**Every UI decision carries a thought-out reason across the FULL experience (fix #19 D19, app surfaces).** Each app-surface UI decision carries its recorded reason in MASTER.md — job served, considered-and-rejected, theme-fit — across all six dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), each a reason or an explicit `none — <reason>`; a layout-only reason does not satisfy the rule. The full D19 rule lives in `design-taste-frontend` step 4a."""

# C1-sentence extension (ui-ux-pro-max type-scale step). The SPEC names
# this slot ("extend the C1 sentence with the F2/F3/F4 app note") but
# gives no constant for it; this pointer sentence is the note.
C1_APP_NOTE = """ On app surfaces, the font-identity rules apply as in fix #19 F2/F3/F4 (static bundled instances only, no system fallback; a distinctive pairing recorded with its Source cell; body text Tiempos or the recorded Fraunces stand-in) — see the F2/F3/F4 app mirrors in this skill."""

# --- shipping-template replacements (start.mjs / theme.mjs / shots.json) ---

START_MJS_OLD = """const stack = (f, serif) => `"${f.family}", ${serif ? 'Georgia, serif' : 'system-ui, sans-serif'}`;"""
START_MJS_NEW = """const stack = (f, serif) => `"${f.family}"${serif ? ', Georgia' : ''}`;"""

THEME_MJS_OLD = """  --font-display: "FILL ME", ui-serif, serif; --font-body: "FILL ME", ui-sans-serif, system-ui, sans-serif; --font-outlier: var(--font-body);"""
THEME_MJS_NEW = """  --font-display: "FILL ME"; --font-body: "FILL ME"; --font-outlier: var(--font-body);"""

SHOTS_SANS_OLD = '''"sans": "\\"Hanken Grotesk\\", system-ui, sans-serif"'''
SHOTS_SANS_NEW = '''"sans": "\\"Hanken Grotesk\\""'''

# --- theme Tokens-block tail strip ------------------------------------------
# Generic/system fallback tails stripped from --font-* lines only (named
# faces — the theme's type voice, cf. SPEC section 5's Sofia precedent —
# are retained). Order matters: longest tails first.
THEME_TAILS = [", system-ui", ", ui-sans-serif", ", ui-serif",
               ", ui-monospace", ", ui-rounded", ", sans-serif",
               ", serif", ", monospace"]

E1_END = "Distinctiveness itself is browser-qa's verdict alone."
STATIC_END = "or the failure recorded as a finding; a floor/ban break blocks."

# --- staged-source appends: (path, old-anchor, addition) -------------------
STAGED_SUBS = [
    # Taste step 4a: F2 + F3 + F4 + D19 as four new bold lines after E1.
    (TASTE, E1_END,
     "\n\n" + F2_RULE + "\n\n" + F3_RULE + "\n\n" + F4_RULE + "\n\n" + D19_RULE),
    # Taste step 6: STATIC19 as a new paragraph after the fix17 checks.
    (TASTE, STATIC_END,
     "\n\n   " + STATIC19),
    # Orchestrate design-package rule: F2 + F3 + F4 + D19 after E1.
    (ORCH, E1_END,
     "\n\n" + F2_RULE + "\n\n" + F3_RULE + "\n\n" + F4_RULE + "\n\n" + D19_RULE),
    # Orchestrate Verify 5a: STATIC19 inline after the fix17 paragraph.
    # (Anchor is the 5a paragraph's final sentence; the two-line anchor
    # "…blocks.\n   - **5b. Final polish**" would inject STATIC19 AFTER
    # the 5b lead-in, mid-bullet — preflight asserts the 5b bullet still
    # immediately follows the 5a paragraph after the edit instead.)
    (ORCH, STATIC_END,
     " " + STATIC19),
    # Polish-pass harmony: font-identity fields + decision-record reasons.
    (POLISH,
     "It also verifies the T1 fill ratios recorded per Type-list row (glyph box ≥ 60% of the container's inner size) — consistency only, never a verdict.",
     POLISH_F19),
    # Less-flat-ui record section: treatments are D19 decisions.
    (LESSFLAT,
     "Handmade surface treatments (tape, perforation, washi, hand-drawn ink marks) record the same way and count toward the two-distinct-kinds check.",
     LF_D19),
]

# Prepend-style replacements (old -> new, full text).
REPLACEMENTS = [
    (TASTE, C2_OLD, C2_NEW),
    (ORCH, ROUTING_OLD, ROUTING_OLD + D19_ROUTING),
    (ORCH, REVIEWER_OLD, REVIEWER_OLD + D19_REVIEWER),
    (TYPESET, TYPESET_OLD, TYPESET_F19),
    (TYPESET, TYPESET_CHECKBOX_OLD, TYPESET_CHECKBOX_NEW),
    (START_MJS, START_MJS_OLD, START_MJS_NEW),
    (THEME_MJS, THEME_MJS_OLD, THEME_MJS_NEW),
    (SHOTS, SHOTS_SANS_OLD, SHOTS_SANS_NEW),
    (SHOTS_EX, SHOTS_SANS_OLD, SHOTS_SANS_NEW),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, addition) -----
BUILD_SUBS = [
    # ui-ux-pro-max: F2/F3/F4/D19 app mirrors after the anti-generic bar.
    ("skills/ui-ux-pro-max/SKILL.md",
     "Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail.",
     "\n\n" + F2_APP + "\n\n" + F3_APP + "\n\n" + F4_APP + "\n\n" + D19_APP),
    # ui-ux-pro-max: C1-sentence extension in the type-scale step.
    ("skills/ui-ux-pro-max/SKILL.md",
     "The dealt pairing / type scale is the ONLY permitted faces on the build — no other face is introduced; record the pairing + its source in `docs/design-tokens.md` (fix #15 C1).",
     C1_APP_NOTE),
    # orch-build-mvp: D19_APP after the E1 rule in step 4.
    ("skills/orch-build-mvp/SKILL.md",
     E1_END,
     "\n\n" + D19_APP),
    # orch-build-mvp: STATIC19 as a new paragraph after the fix17 checks.
    ("skills/orch-build-mvp/SKILL.md",
     STATIC_END,
     "\n\n" + STATIC19),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def theme_files():
    return sorted(glob.glob(os.path.join(THEMES_DIR, "*.md")))


def strip_theme_tails(text):
    """Strip generic/system fallback tails from --font-* lines only."""
    out = []
    for line in text.splitlines(keepends=True):
        if "--font-" in line:
            for tail in THEME_TAILS:
                line = line.replace(tail, "")
        out.append(line)
    return "".join(out)


def check_theme_declarations(text, path):
    """Every --font-* declaration must still name a face (or a var())."""
    for m in re.finditer(r"--font-[a-z]+:\s*([^;]*);", text):
        v = m.group(1).strip()
        assert v, f"PREFLIGHT {path}: emptied font declaration: {m.group(0)!r}"
        assert ('"' in v or "var(" in v), \
            f"PREFLIGHT {path}: font declaration left with no named face: {m.group(0)!r}"


def build_sh_block():
    """The fix19 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix19: font identity, forced font choice, Tiempos body font, thought-out decisions (F2/F3/F4/D19) ---")
    lines.append("# (skills/ui-ux-pro-max and orch-build-mvp are upstream; they have no")
    lines.append("#  staged source and are patched here. The staged-source halves --")
    lines.append("#  design-taste-frontend (incl. theme Tokens blocks, start.mjs, theme.mjs),")
    lines.append("#  pitch-deck-video template shots.json, orchestrate, polish-pass, typeset")
    lines.append("#  lens, less-flat-ui -- are applied by fix19/fix19.py to their sources.")
    lines.append("#  All anchors were verified count==1 against the post-fix18 built tree")
    lines.append("#  by fix19.py's preflight; the asserts below re-verify at build time")
    lines.append("#  and fail the build loudly on mismatch.)")
    lines.append("# Placement: LAST, just before STEP 5 (after the fix17 block; fix18 made")
    lines.append("#  no build.sh block — it edited staged sources only).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("subs = [")
    for rel, old, add in BUILD_SUBS:
        lines.append("  (%s," % repr(rel))
        lines.append("   %s," % repr(old))
        lines.append("   %s)," % repr(add))
    lines.append("]")
    lines.append("for rel, old, add in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix19 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    open(p, \"w\").write(t.replace(old, old + add))")
    lines.append("print(\"fix19 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def preflight():
    """Check every anchor count==1 before writing anything."""
    # Staged-source anchors.
    grouped = {}
    for path, old, add in STAGED_SUBS:
        grouped.setdefault(path, []).append(old)
    for path, old, new in REPLACEMENTS:
        grouped.setdefault(path, []).append(old)
    for path, olds in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old in olds:
            n = text.count(old)
            assert n == 1, f"PREFLIGHT {path}: anchor count={n}: {old[:70]!r}"
    # Orchestrate 5b bullet must immediately follow the 5a paragraph
    # (the two-line anchor from the SPEC is a locator, not an append point:
    # appending after it would inject STATIC19 after the 5b lead-in).
    orch = open(ORCH, encoding="utf-8").read()
    assert orch.count(STATIC_END + "\n   - **5b. Final polish**") == 1, \
        "PREFLIGHT orchestrate: 5a paragraph / 5b bullet adjacency"
    # Taste step-4a E1 ending vs step-6 STATIC_CHECKS ending are distinct:
    # the step-6 ending is followed by the gate code block, not by E1 text.
    taste = open(TASTE, encoding="utf-8").read()
    assert taste.count(STATIC_END + "\n\n   ```bash") == 1, \
        "PREFLIGHT taste: step-6 static-checks paragraph ending"
    # Theme Tokens blocks: simulate the tail strip; every file that has
    # system-ui must end at zero, with all font declarations intact.
    n_themes_with_system_ui = 0
    n_system_ui_removed = 0
    for path in theme_files():
        text = open(path, encoding="utf-8").read()
        before = text.count("system-ui")
        if before:
            n_themes_with_system_ui += 1
            n_system_ui_removed += before
        stripped = strip_theme_tails(text)
        assert stripped.count("system-ui") == 0, \
            f"PREFLIGHT {path}: system-ui survives the tail strip"
        check_theme_declarations(stripped, path)
    assert n_themes_with_system_ui == 30, \
        f"PREFLIGHT themes: expected 30 files with system-ui, got {n_themes_with_system_ui}"
    assert n_system_ui_removed == 39, \
        f"PREFLIGHT themes: expected 39 system-ui removed, got {n_system_ui_removed}"
    # Build-sh patch anchors against the current built tree.
    for rel, old, add in BUILD_SUBS:
        p = os.path.join(BUILT, rel)
        text = open(p, encoding="utf-8").read()
        n = text.count(old)
        assert n == 1, f"PREFLIGHT built {rel}: anchor count={n}: {old[:70]!r}"
    # Build.sh insertion anchor.
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fix19 upstream block applied" not in btext, "PREFLIGHT build.sh: fix19 block already present"
    # No banned terms (fix #16 scrub) in any addition or in the block itself.
    additions = [add for _, _, add in STAGED_SUBS]
    additions += [new for _, _, new in REPLACEMENTS]
    additions += [add for _, _, add in BUILD_SUBS]
    block = build_sh_block()
    for blob in additions + [block]:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fix19 addition"
    print(f"preflight OK: {sum(len(v) for v in grouped.values())} staged anchors + "
          f"{len(BUILD_SUBS)} built-tree anchors + build.sh insertion anchor + "
          f"theme strip (30 files, 39 system-ui) + banned-term scan clean")


def main():
    preflight()

    # 1. Staged-source edits (replacements first, then appends).
    for path, old, new in REPLACEMENTS:
        text = open(path, encoding="utf-8").read()
        assert text.count(old) == 1, f"{path}: replacement anchor not found exactly once: {old[:70]!r}"
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
        print(f"{os.path.relpath(path, PLUGIN) if path.startswith(PLUGIN) else path}: replacement applied")
    by_path = {}
    for path, old, add in STAGED_SUBS:
        by_path.setdefault(path, []).append((old, add))
    for path, subs in by_path.items():
        text = open(path, encoding="utf-8").read()
        for old, add in subs:
            assert text.count(old) == 1, f"{path}: anchor not found exactly once: {old[:70]!r}"
            text = text.replace(old, old + add)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN) if path.startswith(PLUGIN) else path}: {len(subs)} substitutions applied")

    # 2. Theme Tokens-block tail strip (30 staged theme files).
    n_files = 0
    n_removed = 0
    for path in theme_files():
        text = open(path, encoding="utf-8").read()
        before = text.count("system-ui")
        if not before:
            continue
        stripped = strip_theme_tails(text)
        assert stripped.count("system-ui") == 0, f"{path}: system-ui survives the tail strip"
        check_theme_declarations(stripped, path)
        open(path, "w", encoding="utf-8").write(stripped)
        n_files += 1
        n_removed += before
    print(f"themes: tail strip applied to {n_files} files, {n_removed} system-ui removed")

    # 3. Backup build.sh (keep the first pre-fix19 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix19")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix19")
    else:
        print("build.sh.before-fix19 already exists, kept")

    # 4. Append the fix19 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print(f"build.sh: fix19 block appended ({len(BUILD_SUBS)} upstream subs, "
          f"{len(block.splitlines())} lines)")


if __name__ == "__main__":
    main()
