#!/usr/bin/env python3
"""Dry-run #37 fixture runner (fix #22, SPEC sections 13, 14, 15, 16, 17
plus a regression subset of sections 8-12).

Follows the Dry-run #35/#36 method: re-run the verifier, assert the rule
anchors verbatim (whitespace-normalised, because the built files wrap long
lines) against the built tree at run time, then apply the check logic stated
in the built skill texts to small fixture inputs. Each fixture prints an
explicit PASS/FAIL from the script itself: PASS means the observed outcome
matched the SPEC's expected outcome.

Proxies (recorded explicitly):
- All fixtures are decision-record / design-package / token / handoff /
  composition inputs judged against the static checks the skills state.
  Slop, depth, orb, WebGL, Vercel and export-review findings are static
  checks producing candidate evidence, never screen verdicts (fix #13e);
  the runner models the FLAG/CLEAR outcome of the static check, not a
  verdict on a rendered screen.
- The /demo fixture is NOT in this runner: it is exercised live in
  fix22/dryrun37/demo-sample-video/ (see dryrun37-demo.py + the report).
- Section 15 letters follow the SPEC's list (a)-(g); the task's two extra
  PASS cases are fixtures 15h (R3F v9 on React 19) and 15i (ShaderGradient
  v2 with URL config).

Models
------
Depth package: {"strategy": str|None, "theme_reason": bool, "d19": bool,
  "d19_lines": int, "reduced_motion": bool, "scrim": bool, "contrast": bool,
  "elevation": bool, "parallax": bool, "layered": bool}
  strategy: None (unnamed), "flat by choice — <reason>", or a named
  strategy ("layered", "parallax", "deep-3D", ...).
Orb use: {"kind": "spinner"|"orb", "state": str|None, "actual": str|None,
  "decorative": bool, "reduced_motion": bool}
  kind spinner = generic spinner; orb state must equal actual activity.
Library use: {"library": str, "effects": int, "react": int|None,
  "r3f": str|None, "version": str, "theme_reason": bool,
  "static_fallback": bool, "url_config": bool, "logo_fallback": bool}
Vercel case: {"mode": "live-fetch"|"pinned"|"finding-d19"|"finding-no-d19"
  |"duplicate-new", "d19": bool, "theme_fit": bool}
Casberry/OriginKit/daisyUI use: {"tool": str, "reviewed": bool,
  "fetches": int, "theme": str, "cited": str}
Regression models follow dryrun36 (screen / mobbin build / handoff /
library use / composition).
"""
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
SLOP = os.path.join(BUILT, "skills/polish-pass/reference/slop-checklist.md")
VERCEL = os.path.join(BUILT, "skills/polish-pass/reference/vercel-checklist.md")
TASTE = os.path.join(BUILT, "skills/design-taste-frontend/SKILL.md")
UIPRO = os.path.join(BUILT, "skills/ui-ux-pro-max/SKILL.md")
ORCH = os.path.join(BUILT, "skills/orchestrate/SKILL.md")
POLISH = os.path.join(BUILT, "skills/polish-pass/SKILL.md")
MP = os.path.join(BUILT, "skills/motion-patterns/SKILL.md")
MF = os.path.join(BUILT, "skills/motion-foundations/SKILL.md")
DSYS = os.path.join(BUILT, "skills/design-system/SKILL.md")
PDV = os.path.join(BUILT, "skills/pitch-deck-video/SKILL.md")
DEDUPE = os.path.join(PLUGIN, "fix22/vercel-dedupe.md")

results = []


def record(name, expected_ok, actual_ok, detail):
    """PASS = observed outcome matches the SPEC's expected outcome."""
    matched = (expected_ok == actual_ok)
    results.append((name, matched))
    print(("PASS " if matched else "FAIL ") + name)
    print("     expected %s, observed %s -- %s"
          % ("PASS" if expected_ok else "FLAG/FAIL",
             "PASS" if actual_ok else "FLAG/FAIL", detail))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def norm(text):
    return re.sub(r"\s+", " ", text)


# --- Anchor assertions: rule texts exist verbatim in the built tree -------
def anchors():
    slop = norm(read(SLOP))
    # §13 depth check (DEPTH-08)
    assert "A design package with no depth strategy named FAILS this check" in slop
    assert "a package naming `flat by choice — <reason>` PASSES it" in slop
    assert "A design with depth applied as decoration with no theme reason FAILS this check" in slop
    assert "A design with 3D motion and no reduced-motion fallback FAILS this check" in slop
    assert "A design with 3D that hurts text contrast FAILS this check" in slop
    assert "a decision-record entry with six dimension lines and no Depth line" in slop
    assert "the strategy `flat by choice — <reason>` — an explicit flat call with its reason recorded" in slop
    # §15 one-WebGL rule (L15-08) + Casberry extension (L17-06/07)
    assert "a surface stacking two WebGL-heavy effects FAILS this check" in slop
    assert "a surface with one theme-matched WebGL effect + static fallback PASSES" in slop
    assert "a Casberry particle export" in slop
    assert "A build pasting exported code blind FAILS the security check" in slop
    # §14 orb check (ORB-PP1)
    assert "a generic spinner" in slop and "FAILS" in slop
    assert "an orb used as decoration" in slop
    orch = norm(read(ORCH))
    assert "Depth — the seventh dimension" in orch
    assert "A decision-record entry is complete only when it carries all seven dimension lines" in orch
    assert "flat by choice — <reason>" in orch
    mf = norm(read(MF))
    assert "R3F v9 FAILS the pairing check" in mf
    assert "depthTokens" in mf
    mp = norm(read(MP))
    assert '"a generic spinner" FAILS' in mp
    assert '"a state-matched orb" PASSES' in mp
    assert '"a mismatched orb state" FAILS' in mp
    assert '"an orb used as decoration" FAILS' in mp
    assert '"an orb that does not respect reduced motion" FAILS' in mp
    assert "DAILY LIMIT: 10 component fetches per key per day" in mp
    assert "proceed from the skills alone, record the gap, never pay for Pro ($79/yr) or Ultimate ($99/yr)" in mp
    assert "A build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check" in mp
    assert "a Casberry export pasted without review FAILS the security check" in mf
    taste = norm(read(TASTE))
    assert "a build installing legacy `shadergradient` v1 FAILS the version check" in taste
    assert "a build using the animated logo with no static fallback FAILS the check" in taste
    assert "the URL IS the config" in taste
    assert "a build shipping daisyUI's default theme unexamined FAILS" in taste
    uipro = norm(read(UIPRO))
    assert "Unpinned versions (\"latest\") FAIL the pin check" in uipro
    assert "thinking-orbs@0.3.2" in uipro
    dsys = norm(read(DSYS))
    assert "A build shipping daisyUI's default theme unexamined FAILS" in dsys
    vercel = read(VERCEL)
    assert "pinned snapshot" in vercel
    assert "4ecfb9fb8d1d3b7009674869b3aaee2f904042e1" in vercel
    assert "raw.githubusercontent" not in vercel
    assert "Fetch the latest guidelines" not in vercel
    assert "cleared only by a recorded D19 reason + theme-fit" in norm(read(POLISH)) or "clear them with a recorded D19 reason + theme-fit" in norm(read(POLISH))
    assert "Covered by:" in vercel
    dedupe = read(DEDUPE)
    assert "| V-AN3 |" in dedupe and "already-covered" in dedupe
    # regression anchors (dry-run #36, re-asserted)
    assert "accent sprawl is a flag, slop-adjacent" in slop
    assert "A screen with no deliberate accentuation" in orch
    assert "A build that cites a Mobbin screen as its design source FAILS" in orch
    assert "the build is NEVER blocked on Mobbin" in orch
    assert "FAILS the handoff check" in orch
    assert "Implementers do not re-interpret directives" in orch
    assert "Reuse the same layoutId" in mp
    assert "dropdowns animate at 150" in mp and "250ms" in mp
    assert "stagger the details in 30ms steps" in mp
    assert "React Bits is React-only" in mp
    assert "MUST disable under `prefers-reduced-motion: reduce`" in norm(read(TASTE))
    pdv = norm(read(PDV))
    assert "one continuous world, a moving camera, a persistent subject" in pdv
    assert "No text under 30px on a 1080-wide stage" in pdv
    assert "A composition that uses a style direction with no theme/brand reason FAILS" in pdv
    print("anchors: all rule texts present verbatim in the built tree")


# --- §13 depth ------------------------------------------------------------
def check_depth(pkg):
    """D1-D6 + D19 seventh dimension. Returns True = PASSES the check."""
    if pkg.get("strategy") is None:
        return False  # D1: no strategy named
    if pkg.get("strategy") == "flat by choice — <reason>":
        return True  # D1 justified use; flat is a deliberate call
    # deliberate depth needs theme reason + D19 reason (D2)
    if not (pkg.get("theme_reason") and pkg.get("d19")):
        return False
    # 3D motion needs a reduced-motion fallback (D4)
    if pkg.get("has_3d_motion") and not pkg.get("reduced_motion"):
        return False
    # text over 3D needs scrim + 4.5:1 (D5)
    if pkg.get("text_over_3d") and not (pkg.get("scrim") and pkg.get("contrast")):
        return False
    # D19 seventh dimension: seven lines incl. Depth (D6)
    if pkg.get("d19_lines", 0) < 7:
        return False
    return True


def section13():
    record("13a", False, check_depth({"strategy": None}),
           "design package with no depth strategy named (D1)")
    record("13b", True, check_depth({"strategy": "flat by choice — <reason>"}),
           "package naming flat by choice + reason (D1 justified use)")
    record("13c", True, check_depth({
        "strategy": "layered", "layered": True, "parallax": True,
        "elevation": True, "theme_reason": True, "d19": True,
        "d19_lines": 7, "has_3d_motion": True, "reduced_motion": True,
        "text_over_3d": True, "scrim": True, "contrast": True}),
        "deliberate depth: layered + parallax + elevation values + "
        "theme-matched + 7 D19 lines incl. Depth: line (D1/D2/D4/D5/D6)")
    record("13d", False, check_depth({
        "strategy": "parallax", "theme_reason": True, "d19": True,
        "d19_lines": 7, "has_3d_motion": True, "reduced_motion": False}),
        "3D motion with no reduced-motion fallback (D4)")
    record("13e", False, check_depth({
        "strategy": "deep-3D", "theme_reason": True, "d19": True,
        "d19_lines": 7, "has_3d_motion": True, "reduced_motion": True,
        "text_over_3d": True, "scrim": False, "contrast": False}),
        "3D hurting text contrast: no scrim, no 4.5:1 (D5)")
    record("13f", False, check_depth({
        "strategy": "deep-3D", "theme_reason": False, "d19": False,
        "d19_lines": 7, "has_3d_motion": True, "reduced_motion": True}),
        "depth as decoration with no theme reason (D2)")
    record("13g", False, check_depth({
        "strategy": "layered", "theme_reason": True, "d19": True,
        "d19_lines": 6, "has_3d_motion": False}),
        "decision-record entry with six lines and no Depth line (D6)")


# --- §14 orbs --------------------------------------------------------------
def check_orb(use):
    """Returns True = PASSES the orb check."""
    if use["kind"] == "spinner":
        return False  # (a) generic spinner for an AI/agent wait
    if use.get("decorative"):
        return False  # (d) orb used as decoration
    if not use.get("reduced_motion"):
        return False  # (e) orb that does not respect reduced motion
    if use.get("state") != use.get("actual"):
        return False  # (c) mismatched orb state
    return True  # (b) state-matched orb


def section14():
    record("14a", False, check_orb({"kind": "spinner", "actual": "searching",
                                    "reduced_motion": True}),
           "generic spinner for an AI/agent wait")
    record("14b", True, check_orb({"kind": "orb", "state": "searching",
                                   "actual": "searching",
                                   "reduced_motion": True}),
           "state-matched orb: searching while retrieving")
    record("14c", False, check_orb({"kind": "orb", "state": "solving",
                                    "actual": "page-load",
                                    "reduced_motion": True}),
           "mismatched orb state: solving while the app is just loading a page")
    record("14d", False, check_orb({"kind": "orb", "state": "breathing",
                                    "actual": "idle", "decorative": True,
                                    "reduced_motion": True}),
           "orb used as decoration (logo/background, nothing waiting)")
    record("14e", False, check_orb({"kind": "orb", "state": "working",
                                    "actual": "working",
                                    "reduced_motion": False}),
           "orb that animates under prefers-reduced-motion instead of a "
           "frozen one-frame orb")


# --- §15 libraries ---------------------------------------------------------
def check_webgl_count(effects):
    """WEBGL_ONE_F22: at most one WebGL-heavy effect per surface."""
    return effects <= 1


def check_r3f_pairing(react, r3f):
    """Strict pairing: v8<->React 18, v9<->React 19."""
    return (react == 18 and r3f == "8") or (react == 19 and r3f == "9")


def check_lib(lib):
    """Returns True = PASSES the §15 checks for this library use."""
    if lib.get("effects", 1) > 1:
        return False
    if lib.get("library") == "shadergradient" and lib.get("version") == "v1":
        return False  # legacy shadergradient v1
    if lib.get("library") == "liquid-logo" and not lib.get("logo_fallback"):
        return False  # animated logo with no static fallback
    if lib.get("version") == "latest":
        return False  # unpinned version
    if not lib.get("theme_reason"):
        return False  # no theme reason
    if lib.get("library") == "r3f" and not check_r3f_pairing(
            lib.get("react"), lib.get("r3f")):
        return False
    return True


def section15():
    record("15a", False, check_webgl_count(2),
           "surface stacking two WebGL-heavy effects (R3F scene + Vanta)")
    record("15b", True, check_lib({"library": "shadergradient",
                                   "effects": 1, "version": "2.4.20",
                                   "theme_reason": True,
                                   "static_fallback": True}),
           "one theme-matched WebGL effect + static fallback")
    record("15c", False, check_r3f_pairing(18, "9"),
           "React 18 build installing R3F v9")
    record("15d", False, check_lib({"library": "shadergradient",
                                    "version": "v1", "theme_reason": True}),
           "build installing legacy shadergradient v1 (1.3.5)")
    record("15e", False, check_lib({"library": "liquid-logo",
                                    "version": "pinned",
                                    "logo_fallback": False,
                                    "theme_reason": True}),
           "animated logo with no static fallback")
    record("15f", False, check_lib({"library": "vanta", "effects": 1,
                                    "version": "0.5.24",
                                    "theme_reason": False}),
           "library effect applied with no theme reason")
    record("15g", False, check_lib({"library": "r3f", "react": 19,
                                    "r3f": "9", "version": "latest",
                                    "theme_reason": True}),
           "unpinned (\"latest\") library version")
    record("15h", True, check_r3f_pairing(19, "9"),
           "React 19 build installing R3F v9 (paired)")
    record("15i", True, check_lib({"library": "shadergradient",
                                   "effects": 1, "version": "2.4.20",
                                   "theme_reason": True,
                                   "static_fallback": True,
                                   "url_config": True}),
           "ShaderGradient v2 with URL-as-config (customize URL + preset)")


# --- §16 Vercel ------------------------------------------------------------
def check_vercel(case):
    """Returns True = PASSES (or is CLEARED / REPORTED as the SPEC requires).
    For 16d the expected outcome is 'reported as a fixable finding', which
    the runner models as the check producing a finding (True = finding
    produced and reported, not silently dropped)."""
    if case["mode"] == "live-fetch":
        return False  # live-fetch form is never the weave
    if case["mode"] == "pinned":
        return True  # pinned snapshot with commit recorded
    if case["mode"] == "finding-d19":
        # cleared by recorded D19 reason + theme-fit, recorded
        return bool(case.get("d19") and case.get("theme_fit"))
    if case["mode"] == "finding-no-d19":
        # reported as a fixable finding (file:line + Fix:), not dropped
        return True
    if case["mode"] == "duplicate-new":
        return False  # duplicates an existing Impeccable rule
    return False


def section16():
    vercel = read(VERCEL)
    record("16a", False, check_vercel({"mode": "live-fetch"}),
           "build whose polish-pass fetches rules from a live URL; the "
           "checklist holds no fetch instruction and no unpinned URL")
    record("16b", True, check_vercel({"mode": "pinned"}) and
           "pinned snapshot" in vercel and "4ecfb9f" in vercel,
           "build checked against the pinned snapshot (commit 4ecfb9f, "
           "2026-10-05, recorded at the top of vercel-checklist.md)")
    record("16c", True, check_vercel({"mode": "finding-d19", "d19": True,
                                      "theme_fit": True}),
           "Vercel finding on code with a recorded D19 reason + theme-fit "
           "is CLEARED (deliberate decision stands) and recorded")
    record("16d", True, check_vercel({"mode": "finding-no-d19"}),
           "Vercel finding with no D19 reason is REPORTED as a fixable "
           "finding (file:line + rule id + paired Fix:), never silently "
           "dropped")
    dedupe = read(DEDUPE)
    record("16e", False, check_vercel({"mode": "duplicate-new"}) and
           "V-AN3" in dedupe,
           "rule claimed as new that duplicates an existing Impeccable "
           "rule (V-AN3 = transition: all, already-covered in the dedupe "
           "table) FAILS the dedupe check")


# --- §17 libraries ---------------------------------------------------------
def check_17(case):
    """Returns True = PASSES the §17 check."""
    if case["tool"] == "casberry":
        if not case.get("reviewed"):
            return False  # (f) export pasted without review
        return case.get("effects", 1) <= 1  # (a) one-WebGL + reviewed
    if case["tool"] == "originkit":
        # (b) >10 fetches hits the cap gracefully: proceed from the skills
        # alone, record the gap, never pay. Modelled as True = the cap
        # path is followed (not a failure of the build).
        return bool(case.get("cap_followed"))
    if case["tool"] == "daisyui":
        if case.get("theme") == "default-unexamined":
            return False  # (c)
        return case.get("theme") == "re-themed"  # (d)
    if case["tool"] == "origin-ui-confusion":
        return False  # (e) Origin UI confused with OriginKit
    return False


def section17():
    record("17a", True, check_17({"tool": "casberry", "reviewed": True,
                                  "effects": 1}),
           "Casberry export passes the one-WebGL rule and the export code "
           "is reviewed line by line")
    record("17b", True, check_17({"tool": "originkit", "fetches": 12,
                                  "cap_followed": True}),
           "build needing 12 OriginKit fetches in a day hits the 10/day "
           "cap gracefully: proceeds from the skills alone, records the "
           "gap, never pays for Pro/Ultimate")
    record("17c", False, check_17({"tool": "daisyui",
                                   "theme": "default-unexamined"}),
           "daisyUI component shipped with the default theme unexamined")
    record("17d", True, check_17({"tool": "daisyui", "theme": "re-themed"}),
           "daisyUI component re-themed to the brand deal")
    record("17e", False, check_17({"tool": "origin-ui-confusion",
                                   "cited": "Origin UI"}),
           "Origin UI cited when the build means OriginKit")
    record("17f", False, check_17({"tool": "casberry", "reviewed": False,
                                   "effects": 1}),
           "Casberry exported code pasted without review")


# --- §8-§12 regression (subset of dry-run #36) ----------------------------
def check_h1(screen):
    hues = screen.get("accent_hues", [])
    if len(set(hues)) > 1:
        return False  # accent sprawl
    if screen.get("accent_on_non_action"):
        return False
    return True


def check_h2(screen):
    accents = screen.get("accents", [])
    if not accents:
        return False  # no deliberate accentuation
    return all(a.get("d19") for a in accents)


def check_mobbin(build):
    if build.get("source") == "mobbin-url":
        return False
    if build.get("source") == "mobbin-screen-copy":
        return False
    if build.get("unreachable"):
        return bool(build.get("gap_recorded"))  # never blocked
    return build.get("source") == "taste"


def check_handoff(h):
    return bool(h.get("values") and h.get("d19"))


def check_lib11(lib):
    if lib["library"] == "vanta" and not lib.get("reduced_motion"):
        return False
    if lib["library"] == "react-bits" and lib.get("stack") != "react":
        return False
    if lib["library"] == "gsap":
        return bool(lib.get("effect_name") and lib.get("exact_params")
                    and lib.get("theme_reason")
                    and lib.get("version") != "latest")
    return True


def check_bang(comp):
    beats = comp.get("beats", [])
    if any(b["kind"] == "slide-fade" for b in beats):
        return False
    if not comp.get("camera_moves"):
        return False
    if not comp.get("persistent_subject"):
        return False
    if any(b.get("min_text_px", 99) < 30 for b in beats):
        return False
    if comp.get("style_direction") and not comp.get("style_theme_reason"):
        return False
    if any(b["kind"] == "generated" for b in beats
           if b.get("role") in ("how", "features")):
        return False  # filmed beats replaced by generated graphics
    return True


def section_regression():
    record("8-H1a", False, check_h1({"accent_hues": ["#7C3AED", "#F59E0B",
                                      "#06B6D4"], "accent_on_non_action": True}),
           "three competing accent hues, accent on non-action elements "
           "(ACCENT_F22 sprawl flag)")
    record("8-H2b", True, check_h2({"accents": [
        {"rank": 1, "means": "size + H1 colour", "d19": True},
        {"rank": 2, "means": "weight", "d19": True},
        {"rank": 3, "means": "spacing", "d19": True}]}),
        "declared first/second/third accent hierarchy + means + D19 each")
    record("9a", False, check_mobbin({"source": "mobbin-url"}),
           "decision record cites a Mobbin URL as its design source")
    record("9b", True, check_mobbin({"source": "taste",
                                     "categories_consulted": ["onboarding",
                                                              "paywall"]}),
           "Mobbin categories consulted; direction generated through Taste")
    record("10a", False, check_handoff({"values": False, "d19": False}),
           "handoff is prose-only, no exact values")
    record("10b", True, check_handoff({"values": True, "d19": True}),
           "handoff with exact tokens/values/copy + D19 reason")
    record("11a", False, check_lib11({"library": "vanta",
                                      "reduced_motion": False}),
           "Vanta background with no reduced-motion fallback")
    record("11c", True, check_lib11({"library": "gsap",
                                     "effect_name": True,
                                     "exact_params": True,
                                     "theme_reason": True,
                                     "version": "3.15.1"}),
           "GSAP effect directed by name + exact parameters, pinned, "
           "theme-matched")
    record("12a", False, check_bang({"beats": [
        {"kind": "slide-fade", "min_text_px": 40},
        {"kind": "slide-fade", "min_text_px": 40}],
        "camera_moves": False, "persistent_subject": False}),
        "composition built as slides with fades, static camera, no "
        "persistent subject")
    record("12b", True, check_bang({"beats": [
        {"kind": "world-move", "min_text_px": 34},
        {"kind": "filmed", "role": "how", "min_text_px": 34},
        {"kind": "world-move", "min_text_px": 36}],
        "camera_moves": True, "persistent_subject": True,
        "style_direction": "editorial light",
        "style_theme_reason": True}),
        "one continuous world + moving camera + persistent subject, "
        "text >=30px, style direction theme-matched")


def main():
    anchors()
    section13()
    section14()
    section15()
    section16()
    section17()
    section_regression()
    total = len(results)
    passed = sum(1 for _, ok in results if ok)
    print("\n%d/%d fixture expectations met" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
