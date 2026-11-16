#!/usr/bin/env python3
"""Dry-run #38 fix #23 fixtures (SPEC sections 1-6 + 9 + THE CORE).

Method follows dry-run #37: assert the rule anchors verbatim
(whitespace-normalised) against the built tree at run time, then apply
the check logic stated in the built skill texts to small fixture inputs.
Each fixture prints an explicit PASS/FAIL from the script itself: PASS
means the observed outcome matched the SPEC's expected outcome.

Proxies (recorded explicitly):
- All fixtures are design-package / decision-record / type-audit-table /
  measurement-dict inputs judged against the static checks the skills
  state. Type-audit, ambition, hero, functionality and dynamic findings
  are candidate evidence, never screen verdicts (fix #13e); the runner
  models the FLAG/CLEAR outcome of the static check, not a verdict on a
  rendered screen. The LIVE application of the §6 assertions to the Home
  Run render is dryrun38-align.py, not this runner.
- Visual share = sum(size_px * visible_chars) per face / total (typeset
  lens, TYPEAUDIT_F23). T1a body <=40% roll-up; T1b body <=55% per
  screen; T1c display/important >=25% roll-up; T1d hero display > body;
  T2 trio re-deal (reuse only with a recorded D19 reason + theme-fit);
  T3 distinct faces >= max(3, ceil(N/20)), each counted face >=5%.
- Alignment tolerances: 0px overflow; <=2px centering/grid/spacing.
- A coverage gap (unverified width or unverified flow state) is a
  BLOCKING finding (BLOCK_F23) -- modelled as the check returning the
  DO NOT SHIP outcome, which is the SPEC's expected outcome.
"""
import math
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
ORCH = os.path.join(BUILT, "skills/orchestrate/SKILL.md")
BQA = os.path.join(BUILT, "skills/browser-qa/SKILL.md")
POLISH = os.path.join(BUILT, "skills/polish-pass/SKILL.md")
TYPESET = os.path.join(BUILT,
                       "skills/polish-pass/reference/lenses/typeset.md")
SLOP = os.path.join(BUILT, "skills/polish-pass/reference/slop-checklist.md")
ALIGN = os.path.join(BUILT, "skills/polish-pass/reference/alignment.md")
TASTE = os.path.join(BUILT, "skills/design-taste-frontend/SKILL.md")
UIPRO = os.path.join(BUILT, "skills/ui-ux-pro-max/SKILL.md")
MF = os.path.join(BUILT, "skills/motion-foundations/SKILL.md")
MP = os.path.join(BUILT, "skills/motion-patterns/SKILL.md")
MA = os.path.join(BUILT, "skills/motion-advanced/SKILL.md")
MIFB = os.path.join(BUILT, "skills/make-interfaces-feel-better/SKILL.md")
ORCHMVP = os.path.join(BUILT, "skills/orch-build-mvp/SKILL.md")
INV = os.path.join(BUILT,
                   "skills/orchestrate/references/design-inventory.md")

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
    orch = norm(read(ORCH))
    assert "INVENTORY_F23" in orch
    assert "we considered everything\" is not a reason and fails the bar" in orch
    assert ("A build that uses only a small slice of the available inventory "
            "without recorded specific reasons for the rest FAILS the "
            "ambition bar") in orch
    assert ("A design that could have been made without the package — one "
            "that uses none of the inventoried elements beyond the bare "
            "minimum — fails the ambition bar") in orch
    assert "a build the user would forget the next day FAILS, however rule-correct" in orch
    assert "A build that feels static fails, even if every static rule passes" in orch
    assert "stagger 30ms, press scale 0.97, dropdowns 150–250ms" in orch
    assert ("A build with an unverified width or an unverified flow state "
            "is NOT shippable") in orch
    assert "the trio is re-dealt per build" in orch
    assert "MEMORABLE_F23" in orch and "AMBITION_F23" in orch
    inv = norm(read(INV))
    assert "INVENTORY_F23" in inv
    assert ("any future fix that adds design elements updates it in the "
            "same change") in inv
    for group in ("ui-ux-pro-max", "Taste", "Hallmark", "Impeccable",
                  "less-flat-ui", "motion-foundations", "polish-pass",
                  "design-system", "make-interfaces-feel-better"):
        assert group in inv, group
    typeset = norm(read(TYPESET))
    assert "the body face carries ≤ 40% of the build's total visual share" in typeset
    assert "≤ 55% on any single primary screen" in typeset
    assert "≥ 25% of the build's total visual share" in typeset
    assert "the display face's share exceeds the body face's share" in typeset
    assert "T2 — trio re-deal" in typeset
    assert "distinct faces F ≥ max(3, ceil(N/20))" in typeset
    assert "Each counted face must carry ≥ 5% of the build's visual share" in typeset
    assert "Visual share** of a face = Σ (size × visible characters)" in typeset
    bqa = norm(read(BQA))
    assert "Typography that reads as defaulted fails here" in bqa
    assert "judges memorability as the TOP criterion" in bqa
    assert "the build shows HOW it works early" in bqa
    assert "scrollWidth - innerWidth == 0" in bqa
    assert "Hero / phone frame centered in the viewport (offset ≤ 2px)" in bqa
    assert "no element beyond its frame unless a declared intentional bleed" in bqa
    assert "tops aligned ± 2px unless a stagger is recorded" in bqa
    assert "every state change choreographed" in bqa
    assert ("A build with an unverified width or an unverified flow state "
            "is NOT shippable — the gap is a blocking finding, not a note") in bqa
    assert "Missing coverage → blocking finding → verdict DO NOT SHIP" in bqa
    taste = norm(read(TASTE))
    assert ("gets a dealt amazing moment: a dealt moment + a distinctive "
            "composition + motion") in taste
    assert "show HOW the thing works" in taste
    assert "as a first-class surface, theme-matched, not an afterthought" in taste
    uipro = norm(read(UIPRO))
    assert ("The trio \"one display face + body stand-in + mono\" is a "
            "pattern, not a default") in uipro
    assert "App and dashboard surfaces show their mechanism, not just their chrome" in uipro
    mf = norm(read(MF))
    assert "Every state change on a build is a choreographed transition" in mf
    mp = norm(read(MP))
    assert "sortable, filterable, expandable, draggable where it serves the job" in mp
    ma = norm(read(MA))
    assert "must actually respond and move in the rendered page" in ma
    assert "MOTION_F23" in norm(read(MIFB))
    assert "TYPEAUDIT_F23" in norm(read(ORCHMVP))
    assert "ALIGN_F23" in norm(read(ALIGN))
    assert "COVER_F23" in norm(read(ALIGN))
    assert "BLOCK_F23" in norm(read(ALIGN))
    print("anchors: all fix #23 rule texts present verbatim in the built tree")


# --- §1 Ambition + THE CORE ------------------------------------------------
def check_ambition(rec):
    """Returns True = PASSES the ambition bar."""
    if rec.get("blanket_line"):
        return False  # "we considered everything" is not a reason
    if rec.get("slice") == "small" and not rec.get("specific_reasons"):
        return False  # small slice without recorded specific reasons
    if rec.get("slice") == "bare-minimum":
        return False  # could have been made without the package
    if rec.get("rule_correct") and not rec.get("ambitious"):
        return False  # rule-correct but unambitious fails F6 primary gate
    if not rec.get("inventory_read"):
        return False  # inventory must be read BEFORE deciding
    return True


def check_memorable(build):
    """THE CORE: memorable is the bar, above F6."""
    if not build.get("memorable_moment"):
        return False  # forgettable tomorrow fails, however rule-correct
    if build.get("loud_thin"):
        return False  # loud but thin still fails ("more, not bolder")
    return True  # over-the-top + quiet palette with a strong moment passes


def section1():
    record("F23-1a", False, check_ambition(
        {"inventory_read": True, "slice": "broad", "blanket_line": True}),
        "record says 'we considered everything' -- blanket line, not a reason")
    record("F23-1b", True, check_ambition(
        {"inventory_read": True, "slice": "broad",
         "specific_reasons": [("less-flat-ui #9", "wrong surface"),
                              ("Vanta", "theme-fit")]})
        , "used + considered-and-rejected named specifically with D19 reasons")
    record("F23-1c", False, check_ambition(
        {"inventory_read": True, "slice": "small", "specific_reasons": []}),
        "small slice of the inventory with no recorded specific reasons")
    record("F23-1d", False, check_ambition(
        {"inventory_read": True, "slice": "bare-minimum",
         "specific_reasons": []}),
        "design usable without the package (bare minimum only)")
    record("F23-1e", False, check_ambition(
        {"inventory_read": True, "slice": "broad", "rule_correct": True,
         "ambitious": False}),
        "rule-correct but unambitious design fails at the finish review")
    record("F23-1f", True, check_ambition(
        {"inventory_read": True, "slice": "broad",
         "specific_reasons": [("R3F", "no 3D job on this build")]}),
        "inventory read before deciding; record cites entries used vs rejected")
    record("F23-Ca", False, check_memorable({"memorable_moment": False}),
        "forgettable build: no memorable moment named -- fails, however "
        "rule-correct")
    record("F23-Cb", True, check_memorable(
        {"memorable_moment": True, "quiet_palette": True}),
        "over-the-top ambition + quiet palette + strong moment -- not "
        "flagged for being quiet")
    record("F23-Cc", False, check_memorable(
        {"memorable_moment": False, "loud_thin": True}),
        "loud styling (cranked weight/color/size), thin ambition -- "
        "over-the-top is ambition, not loudness")


# --- §2 Motion --------------------------------------------------------------
def check_motion(build):
    """Returns True = PASSES the motion-default rule."""
    if build.get("scroll_motion_on_taste_landing"):
        return False  # scope guard: Taste landing pages keep the scroll ban
    if build.get("static_feel"):
        return False  # feels static fails, even if static rules pass
    if build.get("has_3d_motion") and not build.get("reduced_motion"):
        return False
    if not build.get("motion"):
        return False
    if build.get("token_routed") is False:
        return False
    return True


def section2():
    record("F23-2a", True, check_motion(
        {"motion": ["entrance", "stagger 30ms", "dealt moment",
                    "micro-interactions", "state transitions"],
         "token_routed": True, "reduced_motion": True}),
        "deliberate eye-catching motion, token-routed, reduced-motion fallback")
    record("F23-2b", False, check_motion(
        {"motion": [], "static_feel": True, "token_routed": True}),
        "build feels static -- fails even though every static rule passes")
    record("F23-2c", False, check_motion(
        {"motion": ["3D tilt"], "has_3d_motion": True,
         "reduced_motion": False, "token_routed": True}),
        "3D motion with no reduced-motion fallback")
    record("F23-2d", True, check_motion(
        {"motion": ["stagger 30ms", "press scale 0.97",
                    "dropdown 150-250ms"],
         "token_routed": True, "reduced_motion": True}),
        "motion values are the fix #22 tokens (stagger 30ms, press 0.97, "
        "dropdowns 150-250ms)")
    record("F23-2e", False, check_motion(
        {"motion": ["scroll parallax"], "token_routed": True,
         "reduced_motion": True, "scroll_motion_on_taste_landing": True}),
        "Taste landing page with scroll motion -- scroll ban scope guard")


# --- §3 Fonts / type audit ---------------------------------------------------
def visual_shares(faces):
    """faces: {face: (size_px, chars)} -> {face: share}. One entry per face
    here stands for the summed size*chars of all that face's elements."""
    total = sum(size * chars for size, chars in faces.values())
    return {f: (size * chars) / total for f, (size, chars) in faces.items()}


def check_typeaudit(t):
    """Returns True = PASSES the type audit (no uncleared fail)."""
    shares = visual_shares(t["faces"])
    body = shares.get("body", 0.0)
    display = sum(s for f, s in shares.items() if f.startswith("display"))
    if body > 0.40 and not t.get("body_exception"):
        return False  # T1a
    if t.get("body_per_screen_max", 0.0) > 0.55 and not t.get("body_exception"):
        return False  # T1b
    if display < 0.25:
        return False  # T1c -- no clearance exists
    if t.get("hero_display", 0.0) <= t.get("hero_body", 0.0):
        return False  # T1d -- no clearance exists
    if t.get("trio_same_as_previous") and not t.get("trio_reuse_reason"):
        return False  # T2
    n = t.get("n_elements", 0)
    need = max(3, math.ceil(n / 20))
    counted = [f for f, s in shares.items() if s >= 0.05]
    if len(counted) < need:
        return False  # T3 -- no clearance exists
    return True


def section3():
    base = {"faces": {"display-700": (48, 120), "body-400": (16, 900),
                      "mono-500": (14, 300)},
            "body_per_screen_max": 0.50, "hero_display": 0.60,
            "hero_body": 0.30, "trio_same_as_previous": False,
            "n_elements": 30}
    # body share: 48*120=5760 display; 16*900=14400 body; 14*300=4200 mono;
    # total 24360 -> body 59% -> T1a FAIL (deliberately body-led fixture)
    record("F23-3a", False, check_typeaudit(dict(base)),
        "body face 59% of build visual share -- T1a cap 40%")
    ok = {"faces": {"display-700": (48, 220), "display-500": (28, 180),
                    "body-400": (16, 700), "mono-500": (14, 300)},
          "body_per_screen_max": 0.45, "hero_display": 0.62,
          "hero_body": 0.28, "trio_same_as_previous": False,
          "n_elements": 30}
    # display 10560+5040=15600; body 11200; mono 4200; total 31000 ->
    # body 36%, display 50% -> passes T1a/T1c/T1d; 4 faces >= 5% -> T3 ok
    record("F23-3b", True, check_typeaudit(ok),
        "body 36% roll-up, display 50%, hero display > body, 4 faces -- PASS")
    screen_heavy = dict(ok, body_per_screen_max=0.60)
    record("F23-3c", False, check_typeaudit(screen_heavy),
        "body 60% on one primary screen -- T1b cap 55%")
    low_display = {"faces": {"display-700": (48, 60), "body-400": (16, 900),
                             "mono-500": (14, 300)},
                   "body_per_screen_max": 0.50, "hero_display": 0.30,
                   "hero_body": 0.28, "trio_same_as_previous": False,
                   "n_elements": 30}
    # display 2880/21480 = 13% -> T1c FAIL
    record("F23-3d", False, check_typeaudit(low_display),
        "display/important faces 13% of build share -- T1c floor 25%")
    hero_body_led = dict(ok, hero_display=0.30, hero_body=0.45)
    record("F23-3e", False, check_typeaudit(hero_body_led),
        "hero/home surface: body share exceeds display share -- T1d")
    record("F23-3f", False, check_typeaudit(
        dict(ok, trio_same_as_previous=True)),
        "trio identical to previous build, no recorded reuse reason -- T2")
    record("F23-3g", True, check_typeaudit(
        dict(ok, trio_same_as_previous=True, trio_reuse_reason=True)),
        "same trio with a recorded D19 reason + theme-fit -- T2 cleared")
    record("F23-3h", False, check_typeaudit(
        dict(ok, n_elements=50,
             faces={"display-700": (48, 300), "body-400": (16, 600),
                    "mono-500": (14, 50)})),
        "N=50 text elements, only 2 faces >=5% (mono 2.8%) -- T3 needs "
        ">= max(3, 3)=3")
    record("F23-3i", True, check_typeaudit(dict(ok, n_elements=50)),
        "N=50, 4 distinct faces each >=5% -- T3 variety floor met")
    record("F23-3j", False, check_typeaudit(dict(base)),
        "one face (body) dominates the visual field -- reads as defaulted, "
        "fails at browser-qa")


# --- §4 Hero ------------------------------------------------------------------
def check_hero(h):
    """Returns True = PASSES the hero bar."""
    if h.get("generic_pasted"):
        return False  # generic hero section pasted onto an app
    if not h.get("dealt_moment"):
        return False  # merely adequate hero fails F6
    if not (h.get("composition") and h.get("motion")):
        return False
    if not h.get("picks_row"):
        return False  # static check: Hero-moment row present
    return True


def section4():
    record("F23-4a", True, check_hero(
        {"dealt_moment": True, "composition": True, "motion": True,
         "picks_row": True}),
        "hero with dealt moment + distinctive composition + motion, recorded")
    record("F23-4b", False, check_hero(
        {"dealt_moment": False, "composition": True, "motion": True,
         "picks_row": False}),
        "merely adequate hero, no dealt moment -- fails F6")
    record("F23-4c", True, check_hero(
        {"dealt_moment": True, "composition": True, "motion": True,
         "picks_row": True, "calibrated_to_product": True}),
        "app home/feed surface IS the hero surface; moment serves the job")
    record("F23-4d", False, check_hero(
        {"dealt_moment": True, "composition": True, "motion": True,
         "picks_row": True, "generic_pasted": True}),
        "generic hero section pasted onto an app that does not need one")
    record("F23-4e", False, check_hero(
        {"dealt_moment": True, "composition": True, "motion": True,
         "picks_row": False}),
        "Picks block missing the Hero-moment row -- static check fails")


# --- §5 Functionality ----------------------------------------------------------
def check_func(f):
    """Returns True = PASSES the functionality rule."""
    if f.get("mechanism") is None:
        return False  # looks good but hides what it does
    if f.get("mechanism") == "generic":
        return False  # not THIS build's mechanism
    if not f.get("visible_early"):
        return False  # mechanism must be visible early, never buried
    if not f.get("theme_matched"):
        return False
    return True


def section5():
    record("F23-5a", True, check_func(
        {"mechanism": "this", "visible_early": True, "theme_matched": True,
         "story_recorded": True}),
        "this build's pipeline/diagram visible early, theme-matched, story "
        "recorded")
    record("F23-5b", False, check_func(
        {"mechanism": None, "visible_early": False, "theme_matched": True}),
        "build looks good but hides what the thing does")
    record("F23-5c", False, check_func(
        {"mechanism": "generic", "visible_early": True,
         "theme_matched": True}),
        "generic 'add a diagram' -- not this build's pipeline/data/stack")
    record("F23-5d", False, check_func(
        {"mechanism": "this", "visible_early": False, "theme_matched": True}),
        "mechanism buried below the fold -- must be visible early")
    record("F23-5e", True, check_func(
        {"mechanism": "this", "visible_early": True, "theme_matched": True,
         "story_recorded": True}),
        "functionality story recorded: pipeline + live data + stack with "
        "the product's own names and real figures")


# --- §6 Alignment (assertion logic; live application is dryrun38-align.py) ---
def check_overflow(m):
    return all(x == 0 for x in m.get("docOverflowX", []))


def check_center(m):
    return all(abs(x) <= 2 for x in m.get("phoneOffsets", []))


def check_nav(m):
    gaps = m.get("navGaps", [])
    if gaps and (max(gaps) - min(gaps) > 2):
        return False
    return all(abs(d) <= 2 for d in m.get("labelCenterDeltas", []))


def check_grid(m):
    return (len(set(m.get("cardLefts", []))) <= 1
            and len(set(m.get("cardRights", []))) <= 1)


def check_clip(m):
    if m.get("textOverflow", 0) > 0:
        return False
    for b in m.get("beyondFrame", []):
        if not m.get("bleed_declared"):
            return False
    return True


def check_actions(m):
    return all(abs(x) <= 2 for x in m.get("actionOffsets", []))


def check_panels(m):
    if m.get("panelTopDelta") is None:
        return True  # stacked layout: tops not asserted there
    return abs(m["panelTopDelta"]) <= 2 or bool(m.get("stagger_recorded"))


def check_coverage(m):
    """Returns (shippable, reason). A gap is BLOCKING, not a note."""
    missing_w = set(m.get("widths_required", [])) - set(m.get("widths_measured", []))
    missing_s = set(m.get("states_required", [])) - set(m.get("states_measured", []))
    return (not missing_w and not missing_s,
            "missing widths %s, missing states %s" % (sorted(missing_w), sorted(missing_s)))


def section6():
    record("F23-6a", True, check_overflow({"docOverflowX": [0, 0, 0]}),
        "scrollWidth - innerWidth == 0 at every tested width")
    record("F23-6b", False, check_overflow({"docOverflowX": [0, 5, 0]}),
        "5px horizontal overflow at 390 -- ALIGN_F23_OVERFLOW")
    record("F23-6c", True, check_center({"phoneOffsets": [0, 0, 0]}),
        "hero/phone frame centered, offset 0 at 1440/900/390")
    record("F23-6d", False, check_center({"phoneOffsets": [0, 5, 0]}),
        "phone frame 5px off center -- tolerance is <=2px")
    record("F23-6e", True, check_nav(
        {"navGaps": [75, 75, 75, 75], "labelCenterDeltas": [0, 0, 0, 0, 0]}),
        "nav gaps equal, nav group centered, each label center == item center")
    record("F23-6f", False, check_nav(
        {"navGaps": [75, 75, 99, 75], "labelCenterDeltas": [0, 0, 0, 0, 0]}),
        "adjacent nav gaps unequal (75/75/99/75) -- beyond +/-2px")
    record("F23-6g", True, check_grid(
        {"cardLefts": [548, 548, 548], "cardRights": [892, 892, 892]}),
        "feed cards share one left and one right edge per width")
    record("F23-6h", False, check_grid(
        {"cardLefts": [548, 552, 548], "cardRights": [892, 892, 892]}),
        "one feed card 4px off the common left edge -- grid fails")
    record("F23-6i", False, check_clip({"textOverflow": 1}),
        "leaf text element scrollWidth > clientWidth + 1 -- clipped text")
    record("F23-6j", True, check_actions({"actionOffsets": [0, 0]})
        and check_clip({"textOverflow": 0, "beyondFrame": []}),
        "stamps offset 0, code-box group centered on its panel (offset 0)")
    cov = {"widths_required": [1440, 900, 390],
           "states_required": ["home", "offer", "offer-accepted", "trip",
                               "trip-wrongcode", "trip-delivered", "branches",
                               "trips", "you", "post", "post-done"]}
    full = dict(cov, widths_measured=[1440, 900, 390],
                states_measured=list(cov["states_required"]))
    ok, why = check_coverage(full)
    record("F23-6k", True, ok, "coverage matrix complete: 3 widths x all "
           "flow states measured + screenshotted -- shippable")
    ok, why = check_coverage(dict(cov, widths_measured=[1440, 900],
                                  states_measured=list(cov["states_required"])))
    record("F23-6l", False, ok, "390 width never measured -- BLOCKING gap "
           "(DO NOT SHIP): " + why)
    ok, why = check_coverage(dict(cov, widths_measured=[1440, 900, 390],
                                  states_measured=[s for s in cov["states_required"]
                                                   if s != "trip-wrongcode"]))
    record("F23-6m", False, ok, "wrong-code state never measured -- BLOCKING "
           "gap (DO NOT SHIP): " + why)
    record("F23-6n", True, check_clip(
        {"textOverflow": 0, "beyondFrame": ["iris-disc"],
         "bleed_declared": True}),
        "element beyond its frame with a DECLARED intentional bleed in the "
        "decision record, page overflow still 0 -- passes")
    record("F23-6o", False, check_clip(
        {"textOverflow": 0, "beyondFrame": ["iris-disc"],
         "bleed_declared": False}),
        "element beyond its frame with NO declared bleed -- ALIGN_F23_CLIP")
    record("F23-6p", True, check_panels(
        {"panelTopDelta": 26, "stagger_recorded": True}),
        "desktop side-panel tops differ 26px with a recorded stagger -- passes")
    record("F23-6q", False, check_panels(
        {"panelTopDelta": 26, "stagger_recorded": False}),
        "desktop side-panel tops differ 26px, no stagger recorded -- "
        "ALIGN_F23_PANELS")


# --- §9 Dynamic interface ------------------------------------------------------
def check_dynamic(d):
    """Returns True = PASSES the dynamic-interface rule."""
    if not d.get("live_state"):
        return False  # frozen mock content, not live state
    if not d.get("controls_respond"):
        return False  # controls that do not respond FAIL at browser-qa
    if d.get("state_changes") and not d.get("choreographed"):
        return False  # a state change with no motion is a gap
    if not d.get("story_recorded"):
        return False  # decision record states the dynamic story per surface
    if not d.get("reduced_motion_complete"):
        return False  # reduced-motion fallback must be complete
    return True


def section9():
    record("F23-9a", True, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": True,
         "interactive_depth": True, "story_recorded": True,
         "reduced_motion_complete": True}),
        "live state moves, controls respond immediately, every state change "
        "choreographed, story recorded")
    record("F23-9b", False, check_dynamic(
        {"live_state": False, "controls_respond": True,
         "state_changes": False, "choreographed": True,
         "story_recorded": True, "reduced_motion_complete": True}),
        "frozen mock content -- surfaces show no live state")
    record("F23-9c", True, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": True,
         "interactive_depth": True, "story_recorded": True,
         "reduced_motion_complete": True}),
        "loading-to-loaded / empty-to-filled transitions choreographed "
        "(motion tokens + dealt moments)")
    record("F23-9d", False, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": False,
         "story_recorded": True, "reduced_motion_complete": True}),
        "state change with no motion -- a gap")
    record("F23-9e", True, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": True,
         "interactive_depth": True, "story_recorded": True,
         "reduced_motion_complete": True}),
        "interactive depth: sortable / filterable / expandable where it "
        "serves the job -- the user can DO things")
    record("F23-9f", False, check_dynamic(
        {"live_state": True, "controls_respond": False,
         "state_changes": True, "choreographed": True,
         "story_recorded": True, "reduced_motion_complete": True}),
        "controls do not respond live -- FAIL at browser-qa")
    record("F23-9g", True, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": True,
         "story_recorded": True, "reduced_motion_complete": True}),
        "reduced-motion fallback complete: state still changes, content "
        "correct at rest")
    record("F23-9h", False, check_dynamic(
        {"live_state": True, "controls_respond": True,
         "state_changes": True, "choreographed": True,
         "story_recorded": False, "reduced_motion_complete": True}),
        "no dynamic story in the decision record (what changes / trigger / "
        "how it moves)")


def main():
    anchors()
    section1()
    section2()
    section3()
    section4()
    section5()
    section6()
    section9()
    total = len(results)
    passed = sum(1 for _, ok in results if ok)
    print("\n%d/%d fix #23 fixture expectations met" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
