#!/usr/bin/env python3
"""Dry-run #35 fixture runner (fix #21, SPEC section 6 items 4-8).

Applies the STATIC21 / F4_TIGHT / F7 logic to small fixtures, using the
real rule constants imported from fix21.py (never retyped from memory).
Each fixture prints an explicit PASS or FAIL from the script itself.

Model
-----
A Type list is a list of tokens: {"element", "role", "face", "decision"}
  role: "main" (main visible text: heading, display, hero, prominent
        label, price, name, call to action), "long-body" (running
        paragraphs of reading prose), or "small" (ordinary small labels:
        captions, meta rows, table heads, form labels, chips, small nav
        links).
  face: the face the token points at. The BODY_FACE is the face serving
        as body/reading text on that build: "Fraunces (stand-in for
        Tiempos)" (or Tiempos itself).
  decision: None, or a dict {face, why, job, theme_fit} -- the recorded
        artistic font design decision for that element, or a class
        decision {"class": <name>, ...} shared by a genuinely uniform
        class. A blanket class named "all text" is NOT a class decision
        (STATIC21: "a blanket 'all text' class line is not a class
        decision").

Checks (from STATIC21, verbatim logic)
---------------------------------------
F4_TIGHT: no token for main visible text points at the body face; the
  body face serves long-length body text and small incidental text only.
F7: every text element in the Type list -- or every genuinely uniform
  text class -- carries its recorded artistic font decision (face + why
  + job + theme/brand fit); a text element with no recorded decision is
  an incomplete build; a main visible text element set in the body face
  is an incomplete build; a blanket 'all text' class line is not a
  class decision.

Read-only: touches no plugin file, no built-tree file, no artifact.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix21 import F4_TIGHT, F7, STATIC21  # noqa: E402

BODY_FACE = "Fraunces (stand-in for Tiempos)"
DISPLAY_FACE = "Bowlby One SC"  # the dealt display face in the repair
MAIN_ROLES = {"main"}
DECISION_FIELDS = ("face", "why", "job", "theme_fit")

results = []


def record(name, passed, detail):
    results.append((name, passed))
    print(("PASS " if passed else "FAIL ") + name)
    print("     " + detail)


def decision_complete(dec):
    """A recorded artistic font decision needs face + why + job + theme/brand fit."""
    if not isinstance(dec, dict):
        return False
    return all(dec.get(f) for f in DECISION_FIELDS)


def is_blanket(dec):
    """A blanket 'all text' class line masquerading as a class decision."""
    if not isinstance(dec, dict):
        return False
    cls = str(dec.get("class", "")).strip().lower()
    return cls == "all text"


def check_f4_tight(tokens):
    """Returns (ok, [violations]). F4_TIGHT: body face never for main text."""
    bad = [t for t in tokens
           if t["role"] in MAIN_ROLES and t["face"] == BODY_FACE]
    if bad:
        return False, ["main visible token %r points at body face %r"
                       % (t["element"], t["face"]) for t in bad]
    return True, ["no main visible token points at the body face; body face "
                  "serves long body / small text only"]


def check_f7(tokens):
    """Returns (ok, [violations]). F7: every element/class has a decision;
    no blanket 'all text' class; no main visible text in the body face."""
    bad = []
    for t in tokens:
        dec = t.get("decision")
        if dec is None:
            bad.append("element %r has NO recorded artistic font decision"
                       % t["element"])
        elif is_blanket(dec):
            bad.append("element %r is covered only by a blanket 'all text' "
                       "class line -- not a class decision" % t["element"])
        elif not decision_complete(dec):
            missing = [f for f in DECISION_FIELDS if not dec.get(f)]
            bad.append("element %r has an incomplete decision (missing: %s)"
                       % (t["element"], ", ".join(missing)))
        if t["role"] in MAIN_ROLES and t["face"] == BODY_FACE:
            bad.append("main visible token %r set in the body face"
                       % t["element"])
    if bad:
        return False, bad
    return True, ["every text element carries its recorded artistic font "
                  "decision (face + why + job + theme/brand fit); no "
                  "blanket class; no main visible text in the body face"]


def full_decision(face, why, job, theme_fit, cls=None):
    d = {"face": face, "why": why, "job": job, "theme_fit": theme_fit}
    if cls:
        d["class"] = cls
    return d


# --- Item 4: default leak -----------------------------------------------
# A price token pointing at the body face with NO recorded decision.
item4 = [{"element": "price", "role": "main", "face": BODY_FACE,
          "decision": None}]
ok, why = check_f7(item4)
record("item4 F7: price token in Fraunces, no recorded decision -> FAIL",
       not ok, "; ".join(why))

# --- Item 5: missing decision --------------------------------------------
# 5a: a button with no font-decision line.
item5a = [{"element": "button (.btn)", "role": "main",
           "face": DISPLAY_FACE, "decision": None}]
ok, why = check_f7(item5a)
record("item5a F7: button with no font-decision line -> FAIL",
       not ok, "; ".join(why))
# 5b: the same record WITH the decision (face + why + job + theme/brand fit).
item5b = [{"element": "button (.btn)", "role": "main",
           "face": DISPLAY_FACE,
           "decision": full_decision(
               DISPLAY_FACE,
               "the dealt display face carries the call to action so it "
               "reads as the one loud moment on the card",
               "make the CTA the visual anchor and the click target",
               "matches the sticker theme's loud display type and the "
               "brand's bold, playful voice")}]
ok, why = check_f7(item5b)
record("item5b F7: same button WITH its decision -> PASS",
       ok, "; ".join(why))

# --- Item 6: body face for main text --------------------------------------
# 6a: a heading token pointing at Fraunces.
item6a = [{"element": "heading (h1)", "role": "main", "face": BODY_FACE,
           "decision": full_decision(
               BODY_FACE, "it was the default", "heading",
               "no theme fit recorded")}]
ok, why = check_f4_tight(item6a)
record("item6a F4_TIGHT: heading token in Fraunces -> FAIL",
       not ok, "; ".join(why))
# 6b: the same heading in the display face.
item6b = [{"element": "heading (h1)", "role": "main", "face": DISPLAY_FACE,
           "decision": full_decision(
               DISPLAY_FACE,
               "the dealt display face is the unique important font for "
               "main visible text (fix #20 F5)",
               "carry the page's main statement at hero scale",
               "matches the theme's display type and the brand's loud "
               "identity")}]
ok, why = check_f4_tight(item6b)
record("item6b F4_TIGHT: same heading in the display face -> PASS",
       ok, "; ".join(why))
# F7 on 6b as well (the heading now also has its decision recorded).
ok, why = check_f7(item6b)
record("item6b F7: same heading, decision recorded -> PASS",
       ok, "; ".join(why))

# --- Item 7: permitted uses ----------------------------------------------
# 7a: a long body paragraph in Fraunces.
item7a = [{"element": "body paragraph (long)", "role": "long-body",
           "face": BODY_FACE,
           "decision": full_decision(
               BODY_FACE,
               "the body face is the reading face; its 1.55 line-height "
               "carries long prose",
               "carry running paragraphs of reading prose",
               "matches the theme's warm reading voice and the brand's "
               "editorial tone")}]
ok, why = check_f4_tight(item7a)
record("item7a F4_TIGHT: long body paragraph in Fraunces -> PASS",
       ok, "; ".join(why))
ok, why = check_f7(item7a)
record("item7a F7: long body paragraph, decision recorded -> PASS",
       ok, "; ".join(why))
# 7b: a small caption / meta row in Fraunces with a recorded class decision
# (class "captions/meta rows" is genuinely uniform: same face, same size
# step, same job across its members).
class_dec = full_decision(
    BODY_FACE,
    "small incidental text is the second permitted home of the body face "
    "(fix #20 F5 small-labels permission, fix #21 F7 condition)",
    "label photos and carry meta rows at a step smaller, sentence case, "
    "untracked",
    "matches the theme's quiet secondary voice; keeps the display face "
    "for the loud moments",
    cls="captions/meta rows")
item7b = [{"element": "caption", "role": "small", "face": BODY_FACE,
           "decision": class_dec},
          {"element": "meta row", "role": "small", "face": BODY_FACE,
           "decision": class_dec}]
ok, why = check_f4_tight(item7b)
record("item7b F4_TIGHT: caption/meta row in Fraunces (small text) -> PASS",
       ok, "; ".join(why))
ok, why = check_f7(item7b)
record("item7b F7: caption/meta row, uniform class decision recorded -> PASS",
       ok, "; ".join(why))

# --- Item 8: blanket class abused -----------------------------------------
# One blanket class decision "all text: Fraunces".
blanket = full_decision(
    BODY_FACE, "it is the default for everything", "all text",
    "no per-element theme fit recorded", cls="all text")
item8 = [{"element": "heading (h1)", "role": "main", "face": BODY_FACE,
          "decision": blanket},
         {"element": "price", "role": "main", "face": BODY_FACE,
          "decision": blanket},
         {"element": "body paragraph (long)", "role": "long-body",
          "face": BODY_FACE, "decision": blanket}]
ok, why = check_f7(item8)
record("item8 F7: blanket 'all text: Fraunces' class line -> FAIL",
       not ok, "; ".join(why))

# --- Item 3 (supporting): the recorded .btn / .roll-btn leaks -------------
# Recorded fix #20 finding (fix20/SPEC.md section 11): the read-only
# Campus Eats artifact's CTA buttons .btn (index.html:193) and .roll-btn
# (:679) are set in Fraunces, the body face -- a genuine F5 leak. Under
# fix #21 they are also F7 failures: no recorded artistic font decision
# for those buttons. Modelled here as the recorded finding (no artifact
# file was read by this worker).
item3 = [{"element": ".btn CTA", "role": "main", "face": BODY_FACE,
          "decision": None},
         {"element": ".roll-btn CTA", "role": "main", "face": BODY_FACE,
          "decision": None}]
ok, why = check_f7(item3)
record("item3 F7: recorded .btn/.roll-btn Fraunces CTAs, no decision -> FAIL",
       not ok, "; ".join(why))
ok, why = check_f4_tight(item3)
record("item3 F4_TIGHT: recorded .btn/.roll-btn Fraunces CTAs -> FAIL",
       not ok, "; ".join(why))

# --- Sanity: the imported rule constants are the real ones -----------------
assert "LONG-LENGTH body text and SMALL incidental text only" in F4_TIGHT
assert "a blanket 'all text' line is not a class decision" in F7
assert "no token for main visible text points at the body face" in STATIC21
print("sanity: F4_TIGHT / F7 / STATIC21 imported from fix21.py (not retyped)")

failed = [n for n, ok in results if not ok]
print("\n%d/%d fixture expectations met" % (len(results) - len(failed),
                                            len(results)))
sys.exit(1 if failed else 0)
