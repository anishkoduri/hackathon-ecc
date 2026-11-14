#!/usr/bin/env python3
"""Dry-run #36 fixture runner (fix #22, SPEC sections 6.3, 8, 9, 10, 11, 12).

Follows the Dry-run #35 method (fix21/dryrun35-report.md + dryrun35-fixtures.py):
re-run the verifier, grep the built tree for the rule anchors, then apply the
check logic from the built skill texts to small fixture inputs. Each fixture
prints an explicit PASS/FAIL from the script itself: PASS means the observed
outcome matched the SPEC's expected outcome.

Rule grounding: the ANCHORS below are asserted verbatim against the built
tree at run time (read, never retyped from memory). The check functions
implement the logic those anchor texts state. No plugin file is touched.

Proxies (recorded explicitly, per the task):
- Bang fixtures (section 12) are COMPOSITION MANIFESTS judged by static
  review against the pitch-deck-video anti-slide checks. There is no live
  browser here, so no footage was filmed in this dry-run; fixture 12e
  (film-the-real-app) is judged on the composition manifest's beat plan
  (filmed beats vs generated-graphics beats), the closest executable proxy.
- All other fixtures are decision-record / token / handoff inputs judged
  against the static checks the skills state. Slop flags are static checks
  producing candidate evidence, never screen verdicts (fix #13e); the
  runner models the FLAG/CLEAR outcome of the static check, not a verdict.

Models
------
Slop instance: {"check", "use", "deliberate", "d19", "theme_fit",
  "source_cell", "f5_key_label", "repeated", "whole_identity"}
  use: "default" (unconsidered default usage) or "justified" (deliberate
  use through the named skill path).
  deliberate/d19/theme_fit: booleans. source_cell: True when the C3
  clearance names the skill text the font choice comes from. f5_key_label:
  True when a C13 clearance is also recorded as a fix #20 F5 key label.
  repeated: True for an eyebrow above every section heading.
  whole_identity: True when a treatment IS the whole visual identity.

Token set: {"dropdown_ms", "stagger_ms", "popover_scale", "layout_id_reuse"}
Trend use: {"trend", "theme_reason", "d19"}
Screen: {"accents": [{"rank", "means", "d19"}...], "accent_hues": [...],
  "accent_on_non_action": bool, "accent_in_brand_tokens": bool, "d19": bool}
Mobbin build: {"source": "taste"|"mobbin-url"|"mobbin-screen-copy",
  "categories_consulted": [...], "unreachable": bool, "gap_recorded": bool}
Handoff: {"values": bool, "d19": bool}  (values = exact tokens/values/copy)
Implementer: {"action": "execute"|"reinterpret"|"recorded-gap"}
Library use: {"library", "stack", "version", "theme_reason": bool,
  "reduced_motion": bool, "effect_name": bool, "exact_params": bool}
Composition: {"beats": [{"kind": "slide-fade"|"world-move"|"filmed"|"generated",
  "min_text_px": int, "text_levels": int}...], "camera_moves": bool,
  "persistent_subject": bool, "style_direction": str|None,
  "style_theme_reason": bool, "av_table_rows": [...]}
"""
import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
SLOP = os.path.join(BUILT, "skills/polish-pass/reference/slop-checklist.md")
TASTE = os.path.join(BUILT, "skills/design-taste-frontend/SKILL.md")
UIPRO = os.path.join(BUILT, "skills/ui-ux-pro-max/SKILL.md")
ORCH = os.path.join(BUILT, "skills/orchestrate/SKILL.md")
POLISH = os.path.join(BUILT, "skills/polish-pass/SKILL.md")
MP = os.path.join(BUILT, "skills/motion-patterns/SKILL.md")
PDV = os.path.join(BUILT, "skills/pitch-deck-video/SKILL.md")

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


# --- Anchor assertions: rule texts exist verbatim in the built tree -------
def anchors():
    slop = read(SLOP)
    assert "flags **unconsidered default usage**, never deliberate use" in slop
    assert "cleared by a recorded D19 reason + theme-fit" in slop
    assert "a gradient wash as the default background or brand look" in slop
    assert "dithering IS the whole visual identity" in slop
    assert "ASCII art / ASCII imagery as the default visual" in slop
    assert "the squircle as the default container shape with no reason" in slop
    assert "Instrument Serif used as a display or body face with no recorded" in slop
    assert "repeated eyebrow above every section heading stays a craft-floor ban" in slop
    assert "accent sprawl is a flag, slop-adjacent" in slop
    taste = read(TASTE)
    assert "A trend used with no theme-match reason is an incomplete build" in taste
    assert "gates.md 2a bans purple-to-blue" in taste
    uipro = read(UIPRO)
    assert "Accent sprawl" in uipro and "is a `polish-pass` flag" in uipro
    assert "One accent colour (fix #22 H1, ACCENT_F22)" in uipro
    orch = read(ORCH)
    assert "A screen with no deliberate accentuation" in orch
    assert "A build that cites a Mobbin screen as its design source FAILS" in orch
    assert "the build is NEVER blocked on Mobbin" in orch
    assert "A description" in orch and "FAILS the handoff check" in orch
    assert "Implementers do not re-interpret directives" in orch
    mp = read(MP)
    assert "Reuse the same layoutId" in mp
    assert "dropdowns animate at 150" in mp and "250ms" in mp
    assert "stagger the details in 30ms steps" in mp
    assert "React Bits is React-only" in mp
    pdv = read(PDV)
    assert "one continuous world, a moving camera, a persistent subject" in pdv
    assert "No text under 30px on a 1080-wide stage" in pdv
    assert "A composition that uses a style direction with no theme/brand reason FAILS" in pdv
    polish = read(POLISH)
    assert "MOBBIN_QA_F22" in polish
    print("anchors: all rule texts present verbatim in the built tree")


# --- Section 6.3: slop flags ----------------------------------------------
def check_slop(inst):
    """Returns (cleared, [reasons]). A flag clears only on deliberate use
    + recorded D19 reason + theme-fit (checklist header + per-check
    Clearance lines). C13 additionally needs the F5 key-label record and
    covers one deliberate label only; a repeated eyebrow never clears.
    C3 additionally needs the Source cell naming the skill text."""
    reasons = []
    if inst.get("repeated") and inst["check"] == "C13":
        return False, ["repeated eyebrow above every section heading stays "
                       "a craft-floor ban regardless of any reason recorded"]
    if inst["use"] == "default":
        return False, ["%s used as an unconsidered default (no deliberate "
                       "use through the skills)" % inst["check"]]
    if not inst.get("d19") or not inst.get("theme_fit"):
        missing = [k for k in ("d19", "theme_fit") if not inst.get(k)]
        return False, ["deliberate use but no recorded %s -- flag stays"
                       % " + ".join(missing)]
    if inst["check"] == "C3" and not inst.get("source_cell"):
        return False, ["Instrument Serif choice with no Source cell naming "
                       "the skill text -- clearance requires it"]
    if inst["check"] == "C13" and not inst.get("f5_key_label"):
        return False, ["eyebrow clearance requires the fix #20 F5 key-label "
                       "record as well as the D19 reason"]
    if inst.get("whole_identity"):
        return False, ["treatment IS the whole visual identity -- flag stays"]
    return True, ["deliberate use through the named skill path with recorded "
                  "D19 reason + theme-fit -- flag cleared"]


def check_tokens(tok):
    """Group B token check: dropdown 150-250ms, row stagger 30ms, popover
    start 0.95, layoutId reuse present (motion-patterns B2/B3/B10/B20)."""
    bad = []
    if not (150 <= tok.get("dropdown_ms", 0) <= 250):
        bad.append("dropdown %sms outside the 150-250ms band"
                   % tok.get("dropdown_ms"))
    if tok.get("stagger_ms") != 30:
        bad.append("row stagger %sms, not 30ms" % tok.get("stagger_ms"))
    if tok.get("popover_scale") != 0.95:
        bad.append("popover start scale %s, not 0.95"
                   % tok.get("popover_scale"))
    if not tok.get("layout_id_reuse"):
        bad.append("no shared layoutId -- the object is replaced, not expanded")
    return (not bad), bad or ["dropdown in 150-250ms band, 30ms stagger, "
                              "popover 0.95, layoutId reused"]


def check_trend(use):
    """Trend theme-match check (Taste TRENDS_F22): a trend used with no
    theme-match reason is an incomplete build."""
    if not use.get("theme_reason") or not use.get("d19"):
        return False, ["trend %r used with no theme-match reason -- "
                       "incomplete build" % use["trend"]]
    return True, ["trend %r recorded with theme-match reason + D19"
                  % use["trend"]]


# --- Section 8: H1 / H2 ----------------------------------------------------
def check_accent_hierarchy(screen):
    """H2 (orchestrate ACCENTUATION_F22): every screen declares first /
    second / third + means + D19 reason for each accent. No deliberate
    accentuation fails."""
    accents = screen.get("accents", [])
    if not accents:
        return False, ["no deliberate accentuation -- everything the same "
                       "weight, nothing draws the eye"]
    ranks = [a["rank"] for a in accents]
    if ranks != [1, 2, 3]:
        return False, ["hierarchy %s does not declare first/second/third"
                       % ranks]
    for a in accents:
        if not a.get("means") or not a.get("d19"):
            return False, ["accent rank %s has no means and/or no D19 reason"
                           % a["rank"]]
    return True, ["hierarchy declared first/second/third with means + D19 "
                  "reason for each accent"]


def check_accent_sprawl(screen):
    """H1 (polish-pass ACCENT_F22): two or more competing accent hues, or
    accent on non-action elements, is a flag. One accent, action-only,
    recorded in the brand tokens with a D19 reason, passes."""
    hues = screen.get("accent_hues", [])
    if len(set(hues)) >= 2:
        return False, ["%d competing accent hues %s -- accent sprawl"
                       % (len(set(hues)), sorted(set(hues)))]
    if screen.get("accent_on_non_action"):
        return False, ["accent used on non-action elements (decorative "
                       "fills / body text / backgrounds) -- sprawl"]
    if not screen.get("accent_in_brand_tokens") or not screen.get("d19"):
        return False, ["single accent but not recorded in the brand tokens "
                       "with a D19 reason -- incomplete"]
    return True, ["one accent colour, action/emphasis only, recorded in the "
                  "brand identity tokens with a D19 reason"]


# --- Section 9: Mobbin ------------------------------------------------------
def check_mobbin(build):
    """Mobbin boundary (orchestrate MOBBIN_RESEARCH_F22 / Taste
    MOBBIN_PATTERN_F22): the generating skill is always the recorded
    source, never a Mobbin URL; a specific screen is never cited as the
    source of a decision; copying a specific screen's layout fails the
    anti-derivative check; unreachable + recorded gap never blocks."""
    if build.get("source") == "mobbin-url":
        return False, ["decision record cites a Mobbin URL as its design "
                       "source -- FAILS the check"]
    if build.get("source") == "mobbin-screen-copy":
        return False, ["layout copied from a specific Mobbin screen -- "
                       "FAILS the anti-derivative check"]
    if build.get("unreachable"):
        if build.get("gap_recorded"):
            return True, ["Mobbin unreachable, gap recorded, design "
                          "proceeds from the skills alone -- never blocked"]
        return False, ["Mobbin unreachable and no gap recorded"]
    if build.get("categories_consulted") and build.get("source") == "taste":
        return True, ["Mobbin categories consulted (%s); direction generated "
                      "through Taste, the recorded source"
                      % ", ".join(build["categories_consulted"])]
    return False, ["no category consultation and no generating skill recorded"]


# --- Section 10: directives -------------------------------------------------
def check_handoff(handoff):
    """Directive handoff (orchestrate DIRECTIVES_F22): a description
    without exact values is not a deliverable and FAILS the handoff check;
    a directive without its D19 reason is incomplete."""
    if not handoff.get("values"):
        return False, ["prose-only handoff, no exact values -- FAILS the "
                       "handoff check"]
    if not handoff.get("d19"):
        return False, ["directive with exact values but no D19 reason -- "
                       "incomplete"]
    return True, ["directive with exact tokens/values/copy + D19 reason"]


def check_implementer(impl):
    """Implementers do not re-interpret directives: ambiguous/unbuildable/
    conflicting directives surface as a recorded gap; improvising around
    a directive is off-skill improvisation and fails the audit."""
    if impl["action"] == "reinterpret":
        return False, ["implementer re-interpreted the directive instead of "
                       "executing it or flagging a recorded gap -- FAILS"]
    if impl["action"] == "recorded-gap":
        return True, ["ambiguous directive surfaced as a recorded gap, not "
                      "improvised around"]
    return True, ["directive executed verbatim"]


# --- Section 11: libraries --------------------------------------------------
PINNED = {"lenis": "lenis@1.3.27", "gsap": "gsap@3.15.1",
          "vanta": "vanta@0.5.24", "three-vanta": "three@0.134.0",
          "react-bits": "9d9c687dc4f55b23539aa5417b703078047efa74"}


def check_library(use):
    """Library rules (ui-ux-pro-max stack scope + VANTA_F22 + REACTBITS_F22
    + GSAP rule): Vanta needs a reduced-motion fallback; React Bits is
    React/Next only; a GSAP effect is directed by name + exact parameters;
    every effect needs a theme reason; unpinned ('latest') versions fail
    the pin check."""
    lib = use["library"]
    if lib == "vanta" and not use.get("reduced_motion"):
        return False, ["Vanta background with no reduced-motion fallback -- "
                       "incomplete build"]
    if lib == "react-bits" and use.get("stack") not in ("react", "nextjs"):
        return False, ["React Bits on a %s stack -- FAILS the scope check "
                       "(React/Next only)" % use.get("stack")]
    if lib == "gsap":
        if not (use.get("effect_name") and use.get("exact_params")):
            return False, ["GSAP effect described in prose without exact "
                           "parameters -- incomplete, FAILS the handoff check"]
    if use.get("version") in ("latest", None):
        return False, ["unpinned version %r -- FAILS the pin check"
                       % use.get("version")]
    if use.get("version") != PINNED.get(lib):
        return False, ["version %r is not the pinned %s"
                       % (use.get("version"), PINNED.get(lib))]
    if not use.get("theme_reason"):
        return False, ["library effect with no theme reason -- not applied"]
    return True, ["%s at pinned %s, theme-matched, reduced-motion handled"
                  % (lib, use.get("version"))]


# --- Section 12: Bang Motion -------------------------------------------------
def check_bang(comp):
    """Anti-slide checks (pitch-deck-video BANG_ANTISLIDE_F22) + style
    menu + film-the-real-app + A/V table. Proxy: the composition manifest
    is judged by static review; no footage was filmed in this dry-run."""
    bad = []
    beats = comp.get("beats", [])
    if any(b["kind"] == "slide-fade" for b in beats):
        bad.append("composition built as slides with fades")
    if not comp.get("camera_moves"):
        bad.append("no camera that actually moves")
    if not comp.get("persistent_subject"):
        bad.append("no subject that persists across scenes")
    for b in beats:
        if b.get("min_text_px", 30) < 30:
            bad.append("text %spx on a 1080-wide stage (under 30px)"
                       % b.get("min_text_px"))
        if b.get("text_levels", 1) > 2:
            bad.append("more than two text levels in one frame")
    if comp.get("style_direction") and not comp.get("style_theme_reason"):
        bad.append("style direction %r with no theme/brand reason"
                   % comp.get("style_direction"))
    if comp.get("replaces_filmed_footage"):
        bad.append("generated motion graphics replace filmed app footage "
                   "-- film-the-real-app rule")
    if bad:
        return False, bad
    return True, ["one continuous world, moving camera, persistent subject, "
                  "text >= 30px, style direction theme-matched, filmed "
                  "footage kept"]


def check_av_table(comp):
    """F5 A/V table (pitch-deck-video): kinetic type and camera moves go
    IN the table as rows of their own."""
    rows = comp.get("av_table_rows", [])
    kinds = {r.get("kind") for r in rows}
    if "kinetic-type" not in kinds or "camera-move" not in kinds:
        return False, ["A/V table missing rows: %s" % sorted(kinds)]
    return True, ["kinetic type and camera moves are rows in the A/V table"]


# --- Fixtures ----------------------------------------------------------------
def main():
    anchors()

    # -- SPEC 6.3 (a): unconsidered defaults FAIL the polish check ---------
    multi_default = [
        {"check": "C1", "use": "default"},
        {"check": "C19", "use": "default"},
        {"check": "C6", "use": "default"},
    ]
    flags = [check_slop(i) for i in multi_default]
    record("6.3a slop defaults: pills + gradient wash + divider soup, "
           "no reasons -> FLAG",
           False, all(ok for ok, _ in flags),
           "; ".join(r[0] for _, r in flags))

    # -- SPEC 6.3 (b): same items with D19 reason + theme-fit PASS ---------
    multi_reasoned = [
        {"check": "C1", "use": "justified", "d19": True, "theme_fit": True},
        {"check": "C19", "use": "justified", "d19": True, "theme_fit": True},
        {"check": "C6", "use": "justified", "d19": True, "theme_fit": True},
    ]
    clears = [check_slop(i) for i in multi_reasoned]
    record("6.3b same slop items with recorded D19 reason + theme-fit "
           "-> CLEAR",
           True, all(ok for ok, _ in clears),
           "; ".join(r[0] for _, r in clears))

    # -- SPEC 6.3 (c): default purple gradient wash FAILS -------------------
    ok, why = check_slop({"check": "C19", "use": "default"})
    record("6.3c default purple gradient wash -> FLAG",
           False, ok, "; ".join(why))
    ok, why = check_slop({"check": "C19", "use": "justified", "d19": True,
                          "theme_fit": True})
    record("6.3c-control theme-matched gradient treatment (#3/#9) + D19 "
           "-> CLEAR",
           True, ok, "; ".join(why))

    # -- SPEC 6.3 (d): theme-matched dithering with D19 PASSES --------------
    ok, why = check_slop({"check": "C14", "use": "justified", "d19": True,
                          "theme_fit": True})
    record("6.3d theme-matched dithering (less-flat-ui #11) + D19 -> CLEAR",
           True, ok, "; ".join(why))
    ok, why = check_slop({"check": "C14", "use": "default",
                          "whole_identity": True})
    record("6.3d-control dithering as the whole visual identity, no reason "
           "-> FLAG",
           False, ok, "; ".join(why))

    # -- SPEC 6.3 (e): layoutId reuse / shared-element transition PASSES ----
    ok, why = check_tokens({"dropdown_ms": 200, "stagger_ms": 30,
                            "popover_scale": 0.95, "layout_id_reuse": True})
    record("6.3e layoutId reuse (shared-element transition, B20/G20) "
           "-> PASS",
           True, ok, "; ".join(why))

    # -- SPEC 6.3 (f): dropdown 150-250ms + 30ms stagger PASS --------------
    ok, why = check_tokens({"dropdown_ms": 200, "stagger_ms": 30,
                            "popover_scale": 0.95, "layout_id_reuse": True})
    record("6.3f dropdown 200ms + 30ms row stagger -> PASS token check",
           True, ok, "; ".join(why))
    ok, why = check_tokens({"dropdown_ms": 600, "stagger_ms": 30,
                            "popover_scale": 0.95, "layout_id_reuse": True})
    record("6.3f-control dropdown at 600ms -> FAIL token check",
           False, ok, "; ".join(why))

    # -- SPEC 6.3 (g): trend with no theme reason FAILS ----------------------
    ok, why = check_trend({"trend": "E7 dark gradient heroes",
                           "theme_reason": False, "d19": False})
    record("6.3g trend (dark gradient heroes) with no theme reason -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_trend({"trend": "E7 dark gradient heroes",
                           "theme_reason": True, "d19": True})
    record("6.3g-control same trend with theme-match reason + D19 -> PASS",
           True, ok, "; ".join(why))

    # -- SPEC 6.3 (h): eyebrow with no D19 FAILS; with one PASSES -----------
    ok, why = check_slop({"check": "C13", "use": "default"})
    record("6.3h eyebrow label with no D19 reason -> FLAG",
           False, ok, "; ".join(why))
    ok, why = check_slop({"check": "C13", "use": "justified", "d19": True,
                          "theme_fit": True, "f5_key_label": True})
    record("6.3h single deliberate key label + D19 + F5 record -> CLEAR",
           True, ok, "; ".join(why))
    ok, why = check_slop({"check": "C13", "use": "justified", "d19": True,
                          "theme_fit": True, "f5_key_label": True,
                          "repeated": True})
    record("6.3h-extra repeated eyebrow above every heading, even with a "
           "reason -> FLAG (stricter rule wins)",
           False, ok, "; ".join(why))

    # -- Family coverage: ASCII pair ----------------------------------------
    ok, why = check_slop({"check": "C15", "use": "default",
                          "whole_identity": True})
    record("family ASCII: ASCII as the default visual, no reason -> FLAG",
           False, ok, "; ".join(why))
    ok, why = check_slop({"check": "C15", "use": "justified", "d19": True,
                          "theme_fit": True})
    record("family ASCII: theme-matched ASCII (less-flat-ui #22) + D19 "
           "-> CLEAR",
           True, ok, "; ".join(why))

    # -- Family coverage: Instrument Serif pair ------------------------------
    ok, why = check_slop({"check": "C3", "use": "default"})
    record("family Instrument Serif: defaulted-to face, no recorded choice "
           "-> FLAG",
           False, ok, "; ".join(why))
    ok, why = check_slop({"check": "C3", "use": "justified", "d19": True,
                          "theme_fit": True, "source_cell": True})
    record("family Instrument Serif: chosen through the skills + D19 + "
           "Source cell -> CLEAR",
           True, ok, "; ".join(why))

    # -- Family coverage: squircle pair --------------------------------------
    ok, why = check_slop({"check": "C16", "use": "default"})
    record("family squircle: default container shape, no reason -> FLAG",
           False, ok, "; ".join(why))
    ok, why = check_slop({"check": "C16", "use": "justified", "d19": True,
                          "theme_fit": True})
    record("family squircle: theme-matched squircle + D19 -> CLEAR",
           True, ok, "; ".join(why))

    # -- Section 8: H1 / H2 --------------------------------------------------
    ok, why = check_accent_hierarchy({"accents": []})
    record("8-H2a screen with no deliberate accentuation -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_accent_hierarchy({"accents": [
        {"rank": 1, "means": "size + H1 accent colour", "d19": True},
        {"rank": 2, "means": "weight", "d19": True},
        {"rank": 3, "means": "spacing", "d19": True}]})
    record("8-H2b declared first/second/third + means + D19 reasons -> PASS",
           True, ok, "; ".join(why))
    ok, why = check_accent_sprawl({"accent_hues": ["#7C3AED", "#F59E0B",
                                                   "#06B6D4"],
                                   "accent_on_non_action": True,
                                   "accent_in_brand_tokens": False,
                                   "d19": False})
    record("8-H1a three competing accent colours -> FAIL sprawl check",
           False, ok, "; ".join(why))
    ok, why = check_accent_sprawl({"accent_hues": ["#7C3AED"],
                                   "accent_on_non_action": False,
                                   "accent_in_brand_tokens": True,
                                   "d19": True})
    record("8-H1b single consistent accent colour, action-only -> PASS",
           True, ok, "; ".join(why))

    # -- Section 9: Mobbin ----------------------------------------------------
    ok, why = check_mobbin({"source": "mobbin-url",
                            "categories_consulted": []})
    record("9a decision record cites a Mobbin URL as design source -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_mobbin({"source": "taste",
                            "categories_consulted": ["onboarding",
                                                     "paywall"]})
    record("9b consulted Mobbin categories, direction generated through "
           "Taste -> PASS",
           True, ok, "; ".join(why))
    ok, why = check_mobbin({"source": "taste", "unreachable": True,
                            "gap_recorded": True})
    record("9c Mobbin unreachable, gap recorded -> PASS (never blocked)",
           True, ok, "; ".join(why))
    ok, why = check_mobbin({"source": "mobbin-screen-copy",
                            "categories_consulted": []})
    record("9d copies a specific Mobbin screen's layout -> FAIL "
           "anti-derivative",
           False, ok, "; ".join(why))

    # -- Section 10: directives ----------------------------------------------
    ok, why = check_handoff({"values": False, "d19": False})
    record("10a prose-only handoff (no exact values) -> FAIL handoff check",
           False, ok, "; ".join(why))
    ok, why = check_handoff({"values": True, "d19": True})
    record("10b handoff with exact tokens/values/copy + D19 -> PASS",
           True, ok, "; ".join(why))
    ok, why = check_implementer({"action": "reinterpret"})
    record("10c implementer re-interprets a directive -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_handoff({"values": True, "d19": False})
    record("10d directive with values but no D19 reason -> FAIL "
           "(incomplete)",
           False, ok, "; ".join(why))
    ok, why = check_handoff({"values": True, "d19": True})
    record("10e directive with values + D19 reason -> PASS",
           True, ok, "; ".join(why))
    ok, why = check_implementer({"action": "recorded-gap"})
    record("10c-control ambiguous directive surfaced as a recorded gap "
           "-> PASS",
           True, ok, "; ".join(why))

    # -- Section 11: libraries -------------------------------------------------
    ok, why = check_library({"library": "vanta",
                             "version": "vanta@0.5.24",
                             "reduced_motion": False, "theme_reason": True})
    record("11a Vanta background with no reduced-motion fallback -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_library({"library": "react-bits",
                             "stack": "html-tailwind",
                             "version": "9d9c687dc4f55b23539aa5417b703078047efa74",
                             "theme_reason": True})
    record("11b React Bits on a non-React stack -> FAIL scope check",
           False, ok, "; ".join(why))
    ok, why = check_library({"library": "gsap", "version": "gsap@3.15.1",
                             "effect_name": True, "exact_params": True,
                             "theme_reason": True})
    record("11c GSAP effect by name + exact parameters -> PASS",
           True, ok, "; ".join(why))
    ok, why = check_library({"library": "gsap", "version": "gsap@3.15.1",
                             "effect_name": True, "exact_params": True,
                             "theme_reason": False})
    record("11d library effect with no theme reason -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_library({"library": "gsap", "version": "latest",
                             "effect_name": True, "exact_params": True,
                             "theme_reason": True})
    record("11e unpinned ('latest') library version -> FAIL pin check",
           False, ok, "; ".join(why))
    ok, why = check_library({"library": "vanta",
                             "version": "vanta@0.5.24",
                             "reduced_motion": True, "theme_reason": True})
    record("11a-control Vanta pinned + reduced-motion fallback + theme "
           "reason -> PASS",
           True, ok, "; ".join(why))

    # -- Section 12: Bang Motion (proxy: static composition review) -----------
    ok, why = check_bang({"beats": [
        {"kind": "slide-fade", "min_text_px": 48, "text_levels": 2},
        {"kind": "slide-fade", "min_text_px": 48, "text_levels": 2}],
        "camera_moves": False, "persistent_subject": False,
        "style_direction": None, "style_theme_reason": False,
        "replaces_filmed_footage": False})
    record("12a /demo composition built as slides with fades -> FAIL "
           "anti-slide",
           False, ok, "; ".join(why))
    ok, why = check_bang({"beats": [
        {"kind": "world-move", "min_text_px": 48, "text_levels": 2},
        {"kind": "filmed", "min_text_px": 48, "text_levels": 1},
        {"kind": "world-move", "min_text_px": 36, "text_levels": 2}],
        "camera_moves": True, "persistent_subject": True,
        "style_direction": "cinematic dark", "style_theme_reason": True,
        "replaces_filmed_footage": False})
    record("12b one continuous world + moving camera + persistent subject "
           "-> PASS",
           True, ok, "; ".join(why))
    ok, why = check_bang({"beats": [
        {"kind": "world-move", "min_text_px": 22, "text_levels": 2}],
        "camera_moves": True, "persistent_subject": True,
        "style_direction": None, "style_theme_reason": False,
        "replaces_filmed_footage": False})
    record("12c text 22px on a 1080-wide stage -> FAIL (under 30px)",
           False, ok, "; ".join(why))
    ok, why = check_bang({"beats": [
        {"kind": "world-move", "min_text_px": 48, "text_levels": 2}],
        "camera_moves": True, "persistent_subject": True,
        "style_direction": "brutalist mono", "style_theme_reason": False,
        "replaces_filmed_footage": False})
    record("12d Bang style direction with no theme/brand reason -> FAIL",
           False, ok, "; ".join(why))
    ok, why = check_bang({"beats": [
        {"kind": "generated", "min_text_px": 48, "text_levels": 2},
        {"kind": "generated", "min_text_px": 48, "text_levels": 2}],
        "camera_moves": True, "persistent_subject": True,
        "style_direction": None, "style_theme_reason": False,
        "replaces_filmed_footage": True})
    record("12e generated motion graphics replace filmed app footage "
           "-> FAIL (film-the-real-app)",
           False, ok, "; ".join(why))
    ok, why = check_av_table({"av_table_rows": [
        {"kind": "kinetic-type", "claim": "title slams in on the beat"},
        {"kind": "camera-move", "claim": "camera pushes through the hero"},
        {"kind": "say", "claim": "the app syncs in real time"}]})
    record("12f kinetic type + camera moves in the A/V table -> PASS",
           True, ok, "; ".join(why))

    failed = [n for n, ok in results if not ok]
    print("\n%d/%d fixture expectations met"
          % (len(results) - len(failed), len(results)))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
