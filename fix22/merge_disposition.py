#!/usr/bin/env python3
"""merge_disposition.py -- build fix22/disposition-merged.md from the
REBUILT tree (hackathon-ecc/) + the six source disposition files.

One row per item (144) with placement = skill + file:line in the built
tree, status, and source disposition. H1/H2 are single merged rows.
Mobbin / directives / libraries / Bang are separate process rows at the end.

Every placement is located by grepping the rebuilt tree for the item's
anchor; a missing or ambiguous anchor fails loudly (exit 1) instead of
emitting a guessed line number.
"""
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
TREE = os.path.join(PLUGIN, "hackathon-ecc")
OUT = os.path.join(PLUGIN, "fix22", "disposition-merged.md")

MF = "skills/motion-foundations/SKILL.md"
MP = "skills/motion-patterns/SKILL.md"
MA = "skills/motion-advanced/SKILL.md"
MIFB = "skills/make-interfaces-feel-better/SKILL.md"
UIPRO = "skills/ui-ux-pro-max/SKILL.md"
QR = "skills/ui-ux-pro-max/references/quick-reference.md"
ORCH = "skills/orchestrate/SKILL.md"
TASTE = "skills/design-taste-frontend/SKILL.md"
POLISH = "skills/polish-pass/SKILL.md"
SLOP = "skills/polish-pass/reference/slop-checklist.md"
UNSLOP = "skills/polish-pass/reference/unslop-fixes.md"
GLOSS = "skills/design-taste-frontend/references/design-glossary.md"
LESSFLAT = "skills/less-flat-ui/SKILL.md"
PITCH = "skills/pitch-deck-video/SKILL.md"


def find(rel, pattern, label):
    path = os.path.join(TREE, rel)
    lines = open(path, encoding="utf-8").read().splitlines()
    hits = [i + 1 for i, l in enumerate(lines) if re.search(pattern, l)]
    if len(hits) != 1:
        print("ANCHOR FAIL %s: %s in %s -> %s hits %s"
              % (label, pattern, rel, len(hits), hits))
        sys.exit(1)
    return hits[0]


def line(rel, n):
    return "`%s:%d`" % (rel, n)


# (id, name, status, rel, regex, secondary-note, source file)
ITEMS = []
# --- Group A: principles A1-A12 + laws A13-A20, motion-foundations.
A_NAMES = {1: "Squash & stretch", 2: "Anticipation wind-up",
           3: "Staging the focus", 4: "Pose to pose", 5: "Follow through",
           6: "Slow in & slow out", 7: "Moving in arcs", 8: "Secondary action",
           9: "Snappy timing", 10: "Exaggerated feedback",
           11: "Solid drawing in 3D", 12: "Overall appeal",
           13: "Fitts's law", 14: "Bigger hit areas", 15: "Hick's law",
           16: "Miller's law", 17: "Doherty threshold", 18: "Postel's law",
           19: "Jakob's law", 20: "Frequency of use"}
for n, name in A_NAMES.items():
    sec = "Principles (PRINCIPLES_F22), AB-01" if n <= 12 \
        else "Decision Guidance laws (LAWS_F22), AB-02"
    note = "motion-foundations %s" % sec
    if n == 14:
        note += "; names the existing 44x44px rule (Fitts's law), no size-rule duplication"
    ITEMS.append(("A%d" % n, name, "partial" if n == 14 else "new",
                  MF, r"\*\*A%d %s" % (n, re.escape(name)), note,
                  "disposition-A.md"))
# --- Group B.
B = [
    ("B1", "Ease-out for entrances", "partial", MF, r"\(fix #22 B1\)",
     "motion-foundations Rules rule 11 (AB-04); token `smooth` annotated B1, :313",
     "disposition-B.md"),
    ("B2", "Dropdowns at 150–250ms", "new", MF, r"// B2 \(fix #22\)",
     "motion-foundations token `dropdown: 0.2`; Dropdown example in motion-patterns (AB-06)",
     "disposition-B.md"),
    ("B3", "Stagger list rows by 30ms", "partial", MF, r"// B3 \(fix #22\)",
     "motion-foundations token `staggerRow: 0.03`; CONFLICT FLAG: 30ms below Rule 5's 0.05s floor, parent adjudicates",
     "disposition-B.md"),
    ("B4", "Scale to 0.97 on press", "covered", MIFB, r"scale\(0\.97\)",
     "make-interfaces-feel-better press default; no new text. OBSERVATION: motion-foundations `scale.press` is 0.95, not the 0.97 default — neither value changed",
     "disposition-B.md"),
    ("B5", "Stretch moving knobs 12%", "new", MF, r"// B5 \(fix #22\)",
     "motion-foundations token `stretch: 1.12`; Stretching knob example in motion-advanced (AB-10)",
     "disposition-B.md"),
    ("B6", "Stagger as details settle", "partial", MP, r"Stagger as details settle \(fix #22 B6\)",
     "motion-patterns note after the Stagger list example (AB-06); cross-ref A8",
     "disposition-B.md"),
    ("B7", "Arcs for object movement", "new", MP, r"\(fix #22 B7",
     "motion-patterns Rules rule 19 (AB-05); primary home, A7 points at it",
     "disposition-B.md"),
    ("B8", "Pulse to confirm success", "partial", MP, r"\(fix #22 B8",
     "motion-patterns Rules rule 17 (AB-05); cross-ref A10",
     "disposition-B.md"),
    ("B9", "Ease-in-out for moves", "new", MF, r"// B9 \(fix #22\)",
     "motion-foundations token `inOut: [0.65, 0, 0.35, 1]`; Rules rule 12 (AB-04)",
     "disposition-B.md"),
    ("B10", "Start popovers at 0.95", "partial", MF, r"// B10 \(fix #22\)",
     "motion-foundations token `popover: 0.95` (separate token, never merge with press); Popover example in motion-patterns (AB-07)",
     "disposition-B.md"),
    ("B11", "Enter from the trigger", "new", MP, r"\(fix #22 B11",
     "motion-patterns Rules rule 11 (AB-05); Dropdown (AB-06) / Popover (AB-07) examples",
     "disposition-B.md"),
    ("B12", "Exit to the trigger", "new", MP, r"\(fix #22 B12",
     "motion-patterns Rules rule 12 (AB-05); Dropdown (AB-06) / Popover (AB-07) examples",
     "disposition-B.md"),
    ("B13", "No bounce on everyday UI", "new", MP, r"\(fix #22 B13",
     "motion-patterns Rules rule 13 (AB-05)",
     "disposition-B.md"),
    ("B14", "Don't tween while held", "new", MP, r"\(fix #22 B14",
     "motion-patterns Rules rule 14 (AB-05); cross-ref G18",
     "disposition-B.md"),
    ("B15", "Make exits 20% shorter", "partial", MF, r"// B15 \(fix #22\)",
     "motion-foundations token `exitFactor: 0.8`; CONFLICT FLAG: quick-reference `exit-faster-than-enter` says ~60–70%, not changed, parent adjudicates; Rules rule 15 (AB-05)",
     "disposition-B.md"),
    ("B16", "Overlap old & new states", "partial", MP, r"16\. \*\*Overlap old & new states \(fix #22 B16\)",
     "motion-patterns Rules rule 16 (AB-05); motion-advanced Rules rule 9 + Overlapping state change example (AB-09/AB-10); scoped vs Rule 3 (`mode=\"wait\"` still governs page transitions)",
     "disposition-B.md"),
    ("B17", "Masks for reveals & colour", "new", MA, r"10\. \*\*Masks for reveals & colour \(fix #22 B17\)",
     "motion-advanced Rules rule 10 (AB-09); Mask reveal example (AB-10)",
     "disposition-B.md"),
    ("B18", "Crossfade icons + blur", "covered", MIFB, r"cross-fade with opacity, scale, and blur",
     "make-interfaces-feel-better Motion defaults; no new text; named in AB-05 insert",
     "disposition-B.md"),
    ("B19", "Rubber band past bounds", "partial", MA, r"11\. \*\*Rubber band past bounds \(fix #22 B19\)",
     "motion-advanced Rules rule 11 (AB-09); cross-ref A2",
     "disposition-B.md"),
    ("B20", "Reuse the same layoutId", "partial", MP, r"18\. \*\*Reuse the same layoutId \(fix #22 B20",
     "motion-patterns Rules rule 18 (AB-05); note AB-08 on the Shared-element crossfade example; dedupe: primary = motion-patterns example + glossary G20",
     "disposition-B.md"),
]
ITEMS.extend(B)
# --- Group C: slop checklist headings.
C_NAMES = {1: "Tags & pills", 2: "Excessive italics", 3: "Instrument Serif",
           4: "Negative kerning", 5: "Over-the-top detailed UI",
           6: "Overusing dividers", 7: "Color shades & opacities",
           8: "Containers with borders", 9: "Overly detailed diagrams",
           10: "Verbose, redundant text", 11: "Code breadcrumbs",
           12: "Section numbering", 13: "Eyebrows", 14: "Dithering",
           15: "ASCII images", 16: "Squircles", 17: "Excessive mono fonts",
           18: "ALL CAPS subtitles", 19: "Gradient backgrounds",
           20: "Periods in titles"}
C_NEW = {2, 3, 5, 11, 20}
for n, name in C_NAMES.items():
    ITEMS.append(("C%d" % n, name, "new" if n in C_NEW else "partial",
                  SLOP, r"### C%d — %s" % (n, re.escape(name)),
                  "polish-pass slop checklist (SLOP_F22); flags, cleared by a recorded D19 reason + theme-fit",
                  "disposition-CD.md"))
# --- Group D: unslop fixes headings.
D_NAMES = {1: "Delete filler badges", 2: "Drop redundant labels",
           3: "Unitalicize random words", 4: "Mono only where needed",
           5: "Use a design system", 6: "Show the actual product",
           7: "Enlarge the main feature", 8: "Group with spacing",
           9: "Make headlines specific", 10: "Emphasize the CTA",
           11: "Add an accent colour", 12: "Keep icons consistent",
           13: "Remove embellishments", 14: "Inner radius = outer – padding",
           15: "Improve text contrast", 16: "Wrap headlines properly",
           17: "Align by eye, not pixels", 18: "Use tabular nums",
           19: "Add loading states", 20: "Animate useful feedback"}
D_COVERED = {5, 14, 15, 18}
D_NEW = {1, 3, 4, 9, 11, 19}
D_PTR = {8: "P6", 9: "P1", 10: "P2", 15: "P3", 16: "P4", 18: "P5", 20: "P7"}
for n, name in D_NAMES.items():
    st = "covered" if n in D_COVERED else ("new" if n in D_NEW else "partial")
    note = "polish-pass unslop fixes (UNSLOP_F22)"
    if n in D_PTR:
        note += "; pointer spec %s (ui-ux-pro-max / motion-patterns)" % D_PTR[n]
    if n == 11:
        note += "; points at H1 (ACCENT_F22), does not duplicate it"
    if n == 5:
        note += "; covered-by-architecture — the plugin IS a design system"
    if n == 14:
        note += "; point, do not restate (craft floor)"
    if n == 15:
        note += "; point, do not restate (4.5:1 rule)"
    if n == 18:
        note += "; primary home is ui-ux-pro-max `number-tabular` (SPEC §5)"
    ITEMS.append(("D%d" % n, name, st, UNSLOP,
                  r"### D%d — %s" % (n, re.escape(name)), note,
                  "disposition-CD.md"))
# --- Group E: trends menu entries.
E_NAMES = {1: "Dithering", 2: "ASCII over video", 3: "Infinite canvases",
           4: "Disco logos", 5: "Renaissance branding", 6: "Monet backgrounds",
           7: "Dark gradient heroes", 8: "Pixel loaders", 9: "Instrument Serif",
           10: "One italic word", 11: "Cream backgrounds",
           12: "All-caps eyebrows", 13: "Pulsing live dots", 14: "Sparkle icons",
           15: "Liquid Glass", 16: "Three icon cards",
           17: "Decorative flowcharts", 18: "Endless marquees",
           19: "Squircles", 20: "Pretext text wrapping"}
E_THEME = {1: "halftone.md", 2: "terminal.md", 3: "blueprint.md",
           4: "carnival.md", 5: "vellum.md", 7: "dusk.md", 8: "arcade.md",
           9: "lumen.md", 10: "spore.md", 11: "hum.md", 13: "wayfind.md",
           15: "dose.md", 17: "blueprint.md", 18: "editorial.md",
           19: "squeeze.md", 20: "newsprint.md"}
for n, name in E_NAMES.items():
    if n == 6:
        st, note = "pointer", ("Taste menu entry points at less-flat-ui #21 "
                               "Impressionist paintings; no theme-file line, does not duplicate the treatment")
    elif n in (12, 14, 16):
        st, note = "new", "menu only — no theme-file line (validator forbids eyebrows / sparkle / three-icon-cards as theme lines)"
    else:
        st, note = "new", ("Hallmark theme Range line in "
                           "references/hallmark/references/themes/%s" % E_THEME[n])
    ITEMS.append(("E%d" % n, name, st, TASTE,
                  r"\*\*E%d %s \(TRENDS_F22\)" % (n, re.escape(name)), note,
                  "disposition-E.md"))
# --- Group F: less-flat-ui treatments (verification-only).
F_NAMES = {1: "Felt texture", 2: "Fluted glass", 3: "Thermal gradients",
           4: "Water ripples", 5: "Speckled graphite",
           6: "Single-hue landscapes", 7: "Blueprint grids", 8: "Halftone",
           9: "Grainy gradients", 10: "Grass texture",
           11: "Dithered images", 12: "Paper texture",
           13: "Contour lines", 14: "Cloud sky", 15: "Pixel mosaics",
           16: "Lens distortion", 17: "Stippled gradients",
           18: "Square-dot grids", 19: "Blurred photos",
           20: "Iridescent shapes", 21: "Impressionist paintings",
           22: "ASCII and pixels"}
# F is F1–F22 (22 reel items). Treatment #23 Soft shadow is NOT a reel
# item — it came from the @lnunesdesigns reel and was already in the
# catalogue; it is verified present (less-flat-ui:488) and recorded in the
# notes section, not as a 145th item row. The 144-item universe is
# A20+B20+C20+D20+E20+F22+G20+H1+H2.
for n, name in F_NAMES.items():
    ITEMS.append(("F%d" % n, name, "verification-only", LESSFLAT,
                  r"### %d\. %s" % (n, re.escape(name)),
                  "less-flat-ui catalogue; no text copied (verification-only)",
                  "disposition-F.md"))
# --- Group G: glossary rows.
G_NAMES = {1: "Kerning", 2: "Optical centre", 3: "Tabular numbers",
           4: "Layout shift", 5: "Tracking", 6: "Optimistic update",
           7: "x-height", 8: "Touch target", 9: "Leading",
           10: "Origin-aware animation", 11: "OKLCH", 12: "Widow",
           13: "Safe area", 14: "Stagger", 15: "Line length",
           16: "Affordance", 17: "Combobox",
           18: "Interruptible animation", 19: "Progressive disclosure",
           20: "Shared element transition"}
G_PTR = {10: "P-G3", 14: "P-G3", 18: "P-G2"}
for n, name in G_NAMES.items():
    ptr = G_PTR.get(n, "P-G1")
    note = "glossary definition; pointer spec %s" % ptr
    if n == 8:
        note += "; owning column: 44x44px minimum (the plugin floor, W2-C4)"
    ITEMS.append(("G%d" % n, name, "new" if n in (1, 2, 12) else "partial",
                  GLOSS, r"\| G%d %s \|" % (n, re.escape(name)), note,
                  "disposition-G.md"))
# --- H1 / H2: single merged rows (B + CD dispositions).
h1 = find(UIPRO, r"One accent colour \(fix #22 H1, ACCENT_F22\)", "H1")
h1s = find(SLOP, r"## Accent sprawl — ACCENT_F22", "H1-sprawl")
ITEMS.append(("H1", "Color accents", "partial", UIPRO, None,
              "ui-ux-pro-max %s; polish-pass accent-sprawl check %s; D11 points at it"
              % (line(UIPRO, h1), line(SLOP, h1s)),
              "disposition-B.md + disposition-CD.md"))
h2 = find(ORCH, r"Accent hierarchy in every UI slice brief \(fix #22 H2, ACCENTUATION_F22\)", "H2")
h2u = find(UIPRO, r"ACCENTUATION_F22\)", "H2-uipro")
h2s = find(SLOP, r"## Accent hierarchy — ACCENTUATION_F22", "H2-slop")
ITEMS.append(("H2", "Accentuation accents", "new", ORCH, None,
              "orchestrate design-package step %s; ui-ux-pro-max hierarchy rules %s; polish-pass hierarchy check %s"
              % (line(ORCH, h2), line(UIPRO, h2u), line(SLOP, h2s)),
              "disposition-B.md + disposition-CD.md"))

rows = []
for item, name, status, rel, pattern, note, src in ITEMS:
    if pattern is not None:
        n = find(rel, pattern, item)
        place = "%s — %s" % (line(rel, n), note)
    else:
        place = note
    rows.append("| %s %s | %s | %s | %s |" % (item, name, place, status, src))

assert len(rows) == 144, "expected 144 rows, got %d" % len(rows)

# --- Process rows (not item rows): verify each placement exists.
def must(rel, pattern, label):
    n = find(rel, pattern, label)
    return line(rel, n)


proc = []
proc.append(("| Mobbin (§9) | "
             "orchestrate %s (MOBBIN_RESEARCH_F22: category-level research step, "
             "record requirement, no-copy boundary, free tier, never blocked); "
             "design-taste-frontend %s (MOBBIN_PATTERN_F22); ui-ux-pro-max %s "
             "(MOBBIN_PATTERN_F22, PROC-P1); polish-pass %s (MOBBIN_QA_F22) | "
             "placed | process-report.md |")
            % (must(ORCH, r"MOBBIN_RESEARCH_F22", "mobbin-orch"),
               must(TASTE, r"MOBBIN_PATTERN_F22", "mobbin-taste"),
               must(UIPRO, r"MOBBIN_PATTERN_F22", "mobbin-uipro"),
               must(POLISH, r"MOBBIN_QA_F22", "mobbin-polish")))
_dir_orch = must(ORCH, r"DIRECTIVES_F22", "dir-orch")
_dir_taste4a = None
for _ln, _t in enumerate(open(os.path.join(TREE, TASTE), encoding="utf-8").read().splitlines(), 1):
    if "DIRECTIVES_F22" in _t and "4a" in _t:
        _dir_taste4a = _ln
assert _dir_taste4a, "Taste step 4a DIRECTIVES_F22 line not found"
_dir_hall = None
for _ln, _t in enumerate(open(os.path.join(TREE, TASTE), encoding="utf-8").read().splitlines(), 1):
    if "DIRECTIVES_F22" in _t and "Hallmark" in _t:
        _dir_hall = _ln
assert _dir_hall, "Taste Hallmark theme-deal DIRECTIVES_F22 pointer not found"
proc.append(("| Directives, not descriptions (§10) | "
             "orchestrate %s (DIRECTIVES_F22, step 4 Build); design-taste-frontend "
             "%s (step 4a) + %s (Hallmark theme-deal pointer); ui-ux-pro-max %s "
             "(PROC-P2); GAN planner %s, generator %s, evaluator %s; polish-pass "
             "%s (DIRECTIVES_F22); prose-only FAILS the handoff check | placed | process-report.md |")
            % (_dir_orch, line(TASTE, _dir_taste4a), line(TASTE, _dir_hall),
               must(UIPRO, r"DIRECTIVES_F22", "dir-uipro"),
               must("agents/ecc-gan-planner.md", r"DIRECTIVES_F22", "dir-planner"),
               must("agents/ecc-gan-generator.md", r"DIRECTIVES_F22", "dir-generator"),
               must("agents/ecc-gan-evaluator.md", r"DIRECTIVES_F22", "dir-evaluator"),
               must(POLISH, r"DIRECTIVES_F22", "dir-polish")))
proc.append(("| Libraries (§11) | "
             "Lenis: motion-foundations %s (LENIS_F22, `lenis@1.3.27`, MIT, smooth-scroll rule); "
             "GSAP: motion-patterns %s (SCROLLTRIGGER_F22; `gsap@3.15.1`, GreenSock Standard \"no charge\", NOT MIT; "
             "`--domain gsap` 17 presets in ui-ux-pro-max %s); Vanta: design-taste-frontend %s "
             "(VANTA_F22, `vanta@0.5.24` MIT + `three@0.134.0`, MUST-disable/static-fallback/mobile/scrim); "
             "React Bits: motion-patterns %s (REACTBITS_F22, commit `9d9c687d…`, MIT + Commons Clause, React-only); "
             "three.js scoped pins: Vanta `three@0.134.0`, general `three@0.185.1`, Bang's 0.161.0 recorded-only; "
             "stale GSAP CDN 3.12.2 in threejs.csv row 35 fixed to 3.15.1 (CSV-GSAP) | placed | libraries-report.md |")
            % (must(MF, r"LENIS_F22", "lib-lenis"),
               must(MP, r"SCROLLTRIGGER_F22", "lib-gsap"),
               must(UIPRO, r"Domain is auto-detected from the query", "lib-domain"),
               must(TASTE, r"VANTA_F22", "lib-vanta"),
               must(MP, r"REACTBITS_F22", "lib-reactbits")))
_bang = [must(PITCH, r"BANG_ANTISLIDE_F22", "bang-anti"),
         must(PITCH, r"BANG_ONEWORLD_F22", "bang-world"),
         must(PITCH, r"BANG_STYLES_F22", "bang-styles"),
         must(PITCH, r"BANG_OPENERS_F22", "bang-openers"),
         must(PITCH, r"BANG_KINETIC_F22", "bang-kinetic"),
         must(PITCH, r"BANG_EXPLAINER_F22", "bang-explainer")]
proc.append(("| Bang Motion port (§12) | "
             "pitch-deck-video %s (anti-slide), %s (one-world), %s (10 style directions, menu), "
             "%s (19 openers, menu), %s (kinetic typography as directives), %s (explainer); "
             "pin SHA `c1aa65e9…` in pitch-deck-video + `build.sh:42` (BANG_PIN) + fix22/bang-report.md; "
             "MIT; GSAP 3.15.1 plugin pin (Bang's 3.12.5 / Three.js 0.161.0 recorded as Bang's only); "
             "repo quiet since Sep 15, 2026, SKILL.md in Indonesian; /demo still films the real app, no second toolchain | placed | bang-report.md |")
            % tuple(_bang))

doc = []
doc.append("# Fix #22 — Merged disposition (144 items)")
doc.append("")
doc.append("Built from the six source dispositions after the post-fix22 rebuild "
           "(`bash build.sh`, exit 0; build.sh 23,732 lines, md5 "
           "`891fca7b5f34aa74db95cb04501345a0`; built tree 166 skills / 72 agents / "
           "123 rules / 87 commands / 15 hooks; 64 trigger keys). Every placement "
           "below is a file:line in the REBUILT tree "
           "(`hackathon-ecc/`), located by anchor grep — not copied from the "
           "pre-build staged line numbers in the source dispositions.")
doc.append("")
doc.append("Status vocabulary: **new** (did not exist), **partial** (mechanism "
           "existed, the rule/value/wording is new), **covered** (already existed, "
           "no new text), **pointer** (points at an existing home, does not restate), "
           "**verification-only** (verified present, no text copied).")
doc.append("")
doc.append("| Item | Placement (built tree) | Status | Source |")
doc.append("|---|---|---|---|")
doc.extend(rows)
doc.append("")
doc.append("## Process rows (not item rows)")
doc.append("")
doc.append("| Process | Placement (built tree) | Status | Source |")
doc.append("|---|---|---|---|")
doc.extend(proc)
doc.append("")
doc.append("## Notes and flags for the coordinator")
doc.append("")
doc.append("- **Three token conflicts applied exactly as specified, flags carried, "
           "NOT resolved** (SPEC §4c): B3 30ms vs Rule 5 0.05s floor; B15 0.8× vs "
           "quick-reference ~60–70%; B4 0.97 vs `scale.press` 0.95 (plus the "
           "B4 observation that the motion-* press scale 0.95 differs from the "
           "polish press default 0.97 — neither value changed). Parent adjudicates.")
doc.append("- **GSAP converges on 3.15.1 everywhere** (GreenSock Standard \"no charge\", "
           "NOT MIT). Three.js is SCOPED, not single-version: Vanta `three@0.134.0`, "
           "general `three@0.185.1`, Bang's 0.161.0 recorded as Bang's version only. "
           "This supersedes the Bang staged note's earlier \"ONE pinned version each\" "
           "alignment flag — SPEC tension (§12 alignment vs §11 deviations D3–D4 in "
           "`fix22/libraries-report.md`).")
doc.append("- **Counts corrected against the source dispositions during verification:** "
           "TRENDS_F22 occurs 23× in Taste SKILL.md (20 entries + intro ×2 + "
           "finish-gate pointer), not 22×; Hallmark carries 16 Range lines in 15 theme "
           "files (Blueprint E3+E17), not 15/14.")
doc.append("- **Group F note:** the less-flat-ui catalogue carries 23 treatments; "
           "F1–F22 are the 22 reel items in this table, and treatment #23 Soft shadow "
           "(`skills/less-flat-ui/SKILL.md:488`) was also verified present — it came "
           "from the @lnunesdesigns reel, not the 22-backgrounds reel, so it is not "
           "a 145th item row.")
doc.append("- **C13 vs Impeccable craft-floor eyebrow tension** (stricter rule wins; "
           "flagged in disposition-CD, not changed).")
doc.append("- **Prior verifiers:** verify15/17/18/19/20/21 each fail ONLY their frozen "
           "post-fix21 build.sh fingerprint check (23,647 lines / md5 8dfacb47…) plus "
           "the resulting cascade lines; all substantive checks still pass. The "
           "fingerprint is legitimately superseded by fix #22 (23,732 lines / md5 "
           "891fca7b…). verify22.py §17 allows exactly those lines.")
doc.append("- **Banned terms:** 0 in the rebuilt tree (case-insensitive grep for "
           "claude|codex|anthropic|opus|sonnet|haiku|composer-2.5, excluding "
           "node_modules).")
doc.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(doc))
print("wrote %s (%d item rows + %d process rows)" % (OUT, len(rows), len(proc)))
