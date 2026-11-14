#!/usr/bin/env python3
"""fix19_fixup.py -- fix-up round for fix #19 (after audit #60 MINOR-1/2
and sweep #23 MINOR-1).

Usage: python3 fix19/fix19_fixup.py     (preflight + apply + self-check)
Exits non-zero if any anchor count differs from expected.

Fix-up items:
  1. MINOR-1 (audit #60 + sweep #23, same finding): 20 Hallmark theme
     files still ship bare-generic / ui-* tails in their Tokens-block
     --font-* lines (31 lines, 92 tail instances). Root cause: fix19.py
     step 2 skips any theme file with no `system-ui`
     (`if not before: continue`), so the strip never ran on them.
     Fix: drop the skip gate — run fix19.strip_theme_tails over ALL 51
     theme files. system-ui total stays 161 (these files contain none).
  2. MINOR-2 (audit #60): start.mjs still emits a Google Fonts
     variable-font <link> into the built page's head.
     (a) fontLink() now requests EXPLICIT weights (static instances)
         instead of variable axis `..` ranges: a weight range is
         expanded to its explicit 100-step weights (plus its end
         weight), and non-weight axes (wdth/opsz/SOFT/WONK) are left
         out of the link — their values are baked in when the build
         instances the face to static files (Taste step 4a).
         axisVal/isLower/axisOrder are deleted (dead after the change).
         Staged source: new-skills/design-taste-frontend/scripts/
         start.mjs (build.sh copies it verbatim; no build.sh patch
         touches it — verified: 0 hits for axisVal/ui-monospace in
         build.sh). build.sh itself is NOT edited by this script.
     (b) The mono stack at start.mjs:301 drops its system tails:
         `"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo,
         Consolas, monospace` -> `"JetBrains Mono"` alone. The loader
         already requests JetBrains Mono at explicit weights 400;500
         (DEFAULT_MONO w [400,500]; type.json mono faces are w
         [400,500] or s [400,500] throughout).
     (c) "Keep the `:root` block as printed" is amended with the F2
         instancing carve-out in Taste SKILL.md (step 4), in
         layout-v4.md ("keep the `:root` block as start.mjs prints
         it"), and in start.mjs's own header comment (line 43, the
         same instruction in the loader itself); the adjacent
         "Load from Google Fonts with `display=swap`" sentence in
         layout-v4.md gets the same carve-out (same paragraph, same
         delivery — leaving it would leave the procedure contradicting
         the rule). The F2 rule text itself is UNCHANGED.
     (d) The instancing METHOD is added as a procedural step in Taste
         step 4a, right after the F2 rule: download the OFL variable
         font -> fontTools instancer per weight -> subsetter -> verify
         no-fvar + correct usWeightClass -> bundle static woff2 +
         @font-face + preloads. The method lives in the procedural
         step, not in F2 (so fix19.py's F2 constant and verify19.py
         are untouched). The new step text contains no literal
         `system-ui` (verify19 asserts the *.md mention count stays
         14 and the total stays 161).
  3. Scoping decision (audit observation): pitch-deck-video
     shots.json serif/mono stacks carry generic tails. DECIDED: F2
     GOVERNS them — the video template is a shipped surface (the
     /demo render; theme.ts passes shots.theme.fonts straight into
     fontFamily in Brand/Captions/Arch/Close, and fonts.ts loads
     Instrument Serif 400 + JetBrains Mono 400/500 explicitly), and
     fix19 already treated shots.json `sans` as in scope on the same
     reasoning (MANIFEST deviation 5). Fixed the same way the `sans`
     stack was: serif -> "Instrument Serif" alone, mono ->
     "JetBrains Mono" alone, in shots.json + shots.example.json.

Each sub: (base, rel, old, new, expected_count). Bases: PLUGIN =
plugin root, TASTE = new-skills/design-taste-frontend, PITCH =
new-skills/pitch-deck-video.
"""
import glob
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix19"))
from fix19 import strip_theme_tails, check_theme_declarations, \
    F2_RULE, THEME_TAILS  # noqa: E402

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILD_SH = os.path.join(PLUGIN, "build.sh")
TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend")
PITCH = os.path.join(PLUGIN, "new-skills/pitch-deck-video")
START_MJS = os.path.join(TASTE, "scripts/start.mjs")
TASTE_SKILL = os.path.join(TASTE, "SKILL.md")
LAYOUT_V4 = os.path.join(TASTE, "references/layout-v4.md")
SHOTS = os.path.join(PITCH, "template/shots.json")
SHOTS_EX = os.path.join(PITCH, "template/shots.example.json")
THEMES_DIR = os.path.join(TASTE, "references/hallmark/references/themes")

OLD_MD5 = "a8d3d3c6f6d32344d0168c5323d9364b"
OLD_LINES = 23314

# The 20 theme files the fix19 strip never ran on (audit #60 / sweep #23).
EXPECTED_UNSTRIPPED = ["arcade.md", "blueprint.md", "broadside.md",
                       "darkroom.md", "dose.md", "editorial.md",
                       "formwork.md", "halftone.md", "hum.md",
                       "newsprint.md", "overprint.md", "pasteup.md",
                       "piste.md", "riso.md", "solstice.md", "sport.md",
                       "terminal.md", "terrazzo.md", "vellum.md",
                       "wayfind.md"]

# --- (d) the instancing method, as a procedural step in Taste step 4a -----
# NOTE: no literal `system-ui` in this text (verify19 asserts the *.md
# mention count stays 14 and the built-tree total stays 161).
INSTANCE_STEP = """**Instance the dealt faces to static files before shipping (fix #19 F2 — the instancing step).** The Google Fonts link `start.mjs` prints requests static instances only (explicit weights, no variable `..` ranges) and is the generation source, never the shipped delivery. Before shipping, instance each dealt face: (1) download the face's OFL variable font (or its static release where one ships); (2) instance it per weight with the fontTools instancer (`fonttools varLib.instancer`, one instance per weight the build uses, e.g. 400/500/600/700/800), with the optical size baked in (opsz) and the other axes (wdth/SOFT/WONK) fixed at their dealt values; (3) subset each instance with the fontTools subsetter (latin + latin-ext); (4) verify each file is static — no fvar table — and its usWeightClass matches the intended weight; (5) bundle the static woff2 files, add one `@font-face` per weight, and preload the first-paint faces. A Type-list row naming a variable file, a system fallback, a bare generic fallback, or no preload is an incomplete build — a static check item in step 6, never a screen verdict."""

# --- (c) the F2 instancing carve-outs (no literal `system-ui` anywhere) ----
TASTE_ROOT_OLD = "Keep the `:root` block as printed."
TASTE_ROOT_NEW = "Keep the `:root` block as printed, except the font delivery: the Google Fonts link the block prints requests static instances only (fix #19 F2) and is the generation source — instance the dealt faces to static files per the step 4a instancing step and ship those files with `@font-face` + preloads, never a CDN link as the delivery."

LAYOUT_ROOT_OLD = "keep the\n  `:root` block as start.mjs prints it."
LAYOUT_ROOT_NEW = "keep the\n  `:root` block as start.mjs prints it, except the font delivery: the printed Google Fonts link is the generation source only — instance the dealt faces to static files per fix #19 F2 (Taste step 4a) and ship those files with `@font-face` + preloads, never a CDN link as the delivery."

LAYOUT_LOAD_OLD = "Load from Google\n  Fonts with `display=swap`; a fallback face never shows (`font-load` warns a family that\n  never loaded)."
LAYOUT_LOAD_NEW = "Load from Google\n  Fonts with `display=swap` only as the generation source (fix #19 F2): the link requests static instances, and the build instances the dealt faces to static files and ships those files — a CDN link is never the shipped delivery. A fallback face never shows (`font-load` warns a family that\n  never loaded)."

START_HEADER_OLD = "Every face is on Google Fonts and every printed value comes from type.json: keep the block as printed."
START_HEADER_NEW = "Every face is on Google Fonts and every printed value comes from type.json: keep the block as printed, except the font delivery — the printed Google Fonts link is the generation source only (fix #19 F2): instance the dealt faces to static files (Taste step 4a) and ship those, never the CDN link."

# --- (a) fontLink(): explicit weights, no variable ranges ------------------
FONTLINK_COMMENT_OLD = "// the Google Fonts CSS2 link: one request, the exact axes, display=swap"
FONTLINK_COMMENT_NEW = "// the Google Fonts CSS2 link: one request, EXPLICIT static weights only (fix #19 F2) — never a variable `..` axis range; display=swap"

AXIS_HELPERS_OLD = """const axisVal = r => (r[0] === r[1] ? String(r[0]) : r[0] + '..' + r[1]);
const isLower = x => x[0] === x[0].toLowerCase();
const axisOrder = (a, b) => (isLower(a) !== isLower(b) ? (isLower(a) ? -1 : 1) : (a < b ? -1 : a > b ? 1 : 0));"""
AXIS_HELPERS_NEW = """// expand a weight range to its explicit static weights: 100-steps from the
// low end up to (not including) the high end, plus both end weights, so
// [400,700] -> 400;500;600;700 and [400,400] -> 400 (fix #19 F2).
const expandWeights = r => {
  const out = new Set([r[0], r[1]]);
  for (let w = Math.ceil(r[0] / 100) * 100; w < r[1]; w += 100) out.add(w);
  return [...out].sort((a, b) => a - b);
};"""

FAM_ENTRY_OLD = "    const e = fam.get(f.family) || { axes: {}, statics: new Set(), variable: false };"
FAM_ENTRY_NEW = "    const e = fam.get(f.family) || { statics: new Set() };"

W_BRANCH_OLD = """    if (f.w) {
      e.variable = true;
      // the letters moment lifts the weight by 200 on a face with a weight axis: load 700 for it
      const w = isDisplay && letters === 'wght' ? [f.w[0], 700] : f.w;
      const put = (k, r) => { const c = e.axes[k]; e.axes[k] = c ? [Math.min(c[0], r[0]), Math.max(c[1], r[1])] : r; };
      put('wght', w);
      for (const k of ['wdth', 'opsz', 'SOFT', 'WONK']) if (f[k]) put(k, f[k]);
    } else if (f.s && f.s.length) f.s.forEach(x => e.statics.add(x));"""
W_BRANCH_NEW = """    if (f.w) {
      // the letters moment lifts the weight by 200 on a face with a weight axis: load 700 for it
      const w = isDisplay && letters === 'wght' ? [f.w[0], 700] : f.w;
      // a weight range is EXPANDED to its explicit 100-step weights (plus its
      // end weight) — the link requests static instances, never a variable
      // range. Any non-weight axis (wdth/opsz/SOFT/WONK) is left out of the
      // link: its value is baked in when the build instances the face to
      // static files (Taste step 4a, instancing step).
      expandWeights(w).forEach(x => e.statics.add(x));
    } else if (f.s && f.s.length) f.s.forEach(x => e.statics.add(x));"""

PARTS_BRANCH_OLD = """    if (e.variable) {
      const keys = Object.keys(e.axes).sort(axisOrder);
      parts.push(`${nm}:${keys.join(',')}@${keys.map(k => axisVal(e.axes[k])).join(',')}`);
    } else if (e.statics.size) parts.push(`${nm}:wght@${[...e.statics].sort().join(';')}`);
    else parts.push(nm);"""
PARTS_BRANCH_NEW = """    if (e.statics.size) parts.push(`${nm}:wght@${[...e.statics].sort((a, b) => a - b).join(';')}`);
    else parts.push(nm);"""

# --- (b) mono stack: bundled face only --------------------------------------
MONO_OLD = """    mono: monoOf(t) ? `"${monoOf(t).family}", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace` : '',"""
MONO_NEW = """    mono: monoOf(t) ? `"${monoOf(t).family}"` : '',"""

# --- (3) shots.json serif/mono stacks (F2 governs: video is a shipped surface)
SHOTS_SERIF_OLD = '      "serif": "\\"Instrument Serif\\", Georgia, serif",'
SHOTS_SERIF_NEW = '      "serif": "\\"Instrument Serif\\"",'
SHOTS_MONO_OLD = '      "mono": "\\"JetBrains Mono\\", ui-monospace, monospace"'
SHOTS_MONO_NEW = '      "mono": "\\"JetBrains Mono\\""'

FIXUP_SUBS = [
    # (a) fontLink(): explicit weights (staged start.mjs).
    (START_MJS, FONTLINK_COMMENT_OLD, FONTLINK_COMMENT_NEW, 1),
    (START_MJS, AXIS_HELPERS_OLD, AXIS_HELPERS_NEW, 1),
    (START_MJS, FAM_ENTRY_OLD, FAM_ENTRY_NEW, 1),
    (START_MJS, W_BRANCH_OLD, W_BRANCH_NEW, 1),
    (START_MJS, PARTS_BRANCH_OLD, PARTS_BRANCH_NEW, 1),
    # (b) mono stack: bundled face only.
    (START_MJS, MONO_OLD, MONO_NEW, 1),
    # (c) "as printed" carve-outs (loader header + Taste + layout-v4).
    (START_MJS, START_HEADER_OLD, START_HEADER_NEW, 1),
    (TASTE_SKILL, TASTE_ROOT_OLD, TASTE_ROOT_NEW, 1),
    (LAYOUT_V4, LAYOUT_ROOT_OLD, LAYOUT_ROOT_NEW, 1),
    (LAYOUT_V4, LAYOUT_LOAD_OLD, LAYOUT_LOAD_NEW, 1),
    # (d) instancing method step in Taste step 4a, after the F2 rule.
    (TASTE_SKILL, F2_RULE, F2_RULE + "\n\n" + INSTANCE_STEP, 1),
    # (3) shots.json serif/mono stacks (both copies).
    (SHOTS, SHOTS_SERIF_OLD, SHOTS_SERIF_NEW, 1),
    (SHOTS, SHOTS_MONO_OLD, SHOTS_MONO_NEW, 1),
    (SHOTS_EX, SHOTS_SERIF_OLD, SHOTS_SERIF_NEW, 1),
    (SHOTS_EX, SHOTS_MONO_OLD, SHOTS_MONO_NEW, 1),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def theme_files():
    return sorted(glob.glob(os.path.join(THEMES_DIR, "*.md")))


def tail_lines(text):
    """--font-* lines still carrying a generic/system tail."""
    bad = []
    for line in text.splitlines():
        if "--font-" in line and any(t in line for t in THEME_TAILS):
            bad.append(line)
    return bad


def preflight():
    # Gate: build.sh is still the post-fix19 file.
    build = read(BUILD_SH)
    assert len(build.splitlines()) == OLD_LINES, \
        f"PREFLIGHT build.sh lines {len(build.splitlines())} != {OLD_LINES}"
    assert hashlib.md5(build.encode("utf-8")).hexdigest() == OLD_MD5, \
        "PREFLIGHT build.sh md5 moved — stop, do not apply the fix-up"
    # No build.sh patch touches the strings this fix-up edits.
    for needle in ("axisVal", "ui-monospace", "Instrument Serif",
                   "Keep the `:root` block as printed"):
        assert needle not in build, \
            f"PREFLIGHT build.sh contains {needle!r} — staged-only edit is unsafe"
    # Every sub anchor count==1 (on the text as left by earlier subs in the
    # same file — none of the subs in one file share an anchor, so a single
    # sequential pass is safe).
    cache = {}
    for path, old, new, want in FIXUP_SUBS:
        if path not in cache:
            cache[path] = read(path)
        n = cache[path].count(old)
        assert n == want, f"PREFLIGHT {path}: anchor count={n} (want {want}): {old[:70]!r}"
        cache[path] = cache[path].replace(old, new)
    # No banned terms in any new text; no new `system-ui` literal in any
    # edited *.md / *.mjs text (verify19 pins the mention count at 14
    # and the built-tree total at 161).
    sys_ui_before = {}
    for path, _, _, _ in FIXUP_SUBS:
        sys_ui_before.setdefault(path, read(path).count("system-ui"))
    for path, old, new, _ in FIXUP_SUBS:
        low = new.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fix-up addition"
        # Only the ADDED text must be system-ui-free: the F2_RULE anchor
        # itself names `system-ui` as the banned token, so an append sub
        # (new startswith old) is checked on its suffix only.
        added = new[len(old):] if new.startswith(old) else new
        assert "system-ui" not in added, \
            f"PREFLIGHT added text for {path} contains literal system-ui"
    for path, text in cache.items():
        assert text.count("system-ui") == sys_ui_before[path], \
            f"PREFLIGHT {path}: system-ui count moved " \
            f"({sys_ui_before[path]} -> {text.count('system-ui')})"
    # Theme strip simulation over ALL 51 files (no skip gate).
    changed, lines_changed, tails_removed = [], 0, 0
    for path in theme_files():
        text = read(path)
        stripped = strip_theme_tails(text)
        assert stripped.count("system-ui") == 0, \
            f"PREFLIGHT {path}: system-ui survives the tail strip"
        check_theme_declarations(stripped, path)
        assert tail_lines(stripped) == [], \
            f"PREFLIGHT {path}: tail lines survive the strip: {tail_lines(stripped)}"
        if stripped != text:
            changed.append(os.path.basename(path))
            lines_changed += sum(1 for a, b in
                                 zip(text.splitlines(), stripped.splitlines())
                                 if a != b)
            tails_removed += sum(text.count(t) - stripped.count(t)
                                 for t in THEME_TAILS)
    assert changed == EXPECTED_UNSTRIPPED, \
        f"PREFLIGHT themes: changed set differs: {changed}"
    assert lines_changed == 31, \
        f"PREFLIGHT themes: expected 31 lines changed, got {lines_changed}"
    assert tails_removed == 92, \
        f"PREFLIGHT themes: expected 92 tails removed, got {tails_removed}"
    # The 30 previously-stripped files are idempotent under re-strip.
    assert len(theme_files()) == 51, \
        f"PREFLIGHT themes: expected 51 files, got {len(theme_files())}"
    # start.mjs still parses (baseline).
    r = subprocess.run(["node", "--check", START_MJS],
                       capture_output=True, text=True)
    assert r.returncode == 0, f"PREFLIGHT node --check failed: {r.stderr}"
    print(f"preflight OK: {len(FIXUP_SUBS)} subs anchored x1 + theme strip "
          f"(20 files, 31 lines, 92 tails) + build.sh {OLD_LINES} lines / "
          f"md5 {OLD_MD5[:8]}… + banned-term + system-ui counts clean")


def main():
    preflight()

    # 1. Text subs (sequential per file, as in fix18_fixup.py).
    cache = {}
    for path, old, new, want in FIXUP_SUBS:
        if path not in cache:
            cache[path] = read(path)
        assert cache[path].count(old) == want, \
            f"{path}: anchor not found exactly once: {old[:70]!r}"
        cache[path] = cache[path].replace(old, new)
        assert new in cache[path], path
    for path, text in cache.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: subs applied")
    # start.mjs must still parse after the edit.
    r = subprocess.run(["node", "--check", START_MJS],
                       capture_output=True, text=True)
    assert r.returncode == 0, f"node --check failed after edit: {r.stderr}"
    print("node --check start.mjs: OK")

    # 2. Theme Tokens-block tail strip over ALL 51 files (no skip gate).
    n_files = 0
    n_lines = 0
    n_tails = 0
    for path in theme_files():
        text = read(path)
        stripped = strip_theme_tails(text)
        if stripped == text:
            continue
        assert stripped.count("system-ui") == 0
        check_theme_declarations(stripped, path)
        assert tail_lines(stripped) == []
        n_lines += sum(1 for a, b in
                       zip(text.splitlines(), stripped.splitlines())
                       if a != b)
        n_tails += sum(text.count(t) - stripped.count(t)
                       for t in THEME_TAILS)
        with open(path, "w", encoding="utf-8") as f:
            f.write(stripped)
        n_files += 1
    print(f"themes: tail strip applied to {n_files} files, {n_lines} lines, "
          f"{n_tails} tails removed")
    assert (n_files, n_lines, n_tails) == (20, 31, 92), \
        f"theme strip mismatch: {(n_files, n_lines, n_tails)}"

    # 3. Self-checks.
    for path, text in cache.items():
        assert "system-ui" not in text or \
            text.count("system-ui") == read(path).count("system-ui")
    start = read(START_MJS)
    assert "axisVal" not in start and "axisOrder" not in start \
        and "isLower" not in start, "variable-axis helpers survive"
    assert "e.variable" not in start, "variable branch survives"
    # `'..'` is legitimate elsewhere in the file (path.join(here, '..',
    # 'library', …)), so scope this to the fontLink function body.
    fn = start[start.find("function fontLink"):start.find("function typeVars")]
    assert "'..'" not in fn and '".."' not in fn, \
        "'..' range literal survives in fontLink"
    assert "ui-monospace" not in start and "SFMono-Regular" not in start \
        and "Menlo" not in start, "mono system tails survive"
    assert "expandWeights" in start, "expandWeights missing"
    assert "Keep the `:root` block as printed, except the font delivery" \
        in read(TASTE_SKILL), "Taste carve-out missing"
    assert "keep the\n  `:root` block as start.mjs prints it, except the " \
        "font delivery" in read(LAYOUT_V4), "layout-v4 carve-out missing"
    assert "only as the generation source (fix #19 F2)" in read(LAYOUT_V4), \
        "layout-v4 Load-from-Google carve-out missing"
    assert "except the font delivery" in start, \
        "start.mjs header carve-out missing"
    assert INSTANCE_STEP in read(TASTE_SKILL), "instancing step missing"
    assert F2_RULE in read(TASTE_SKILL), "F2 rule disturbed in Taste"
    import json
    for p in (SHOTS, SHOTS_EX):
        shots = json.load(open(p, encoding="utf-8"))
        assert shots["theme"]["fonts"] == {
            "sans": '"Hanken Grotesk"',
            "serif": '"Instrument Serif"',
            "mono": '"JetBrains Mono"'}, f"{p}: font stacks wrong: {shots['theme']['fonts']}"
    for p in theme_files():
        assert tail_lines(read(p)) == [], f"{p}: tail lines remain"
        assert read(p).count("system-ui") == 0, f"{p}: system-ui present"
    build = read(BUILD_SH)
    assert len(build.splitlines()) == OLD_LINES, "build.sh line count moved"
    assert hashlib.md5(build.encode("utf-8")).hexdigest() == OLD_MD5, \
        "build.sh md5 moved — this script must not edit build.sh"
    print(f"self-checks pass: build.sh still {OLD_LINES} lines, "
          f"md5 {OLD_MD5} (unedited by this fix-up)")


if __name__ == "__main__":
    main()
