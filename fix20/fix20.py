#!/usr/bin/env python3
"""Fix program #20: Tiempos is body-only, important text gets a unique
important font, impressive is the bar — plus branding (B1) and every
component is an experience (X1), folded into this same program per
Anish's Nov 11 evening follow-up (SPEC.md sections 0-2, updated).

Refines fix #19's font rules so a future build cannot use the body face
for important text, cannot set important text in anything but a unique,
important display face, and cannot be rule-correct yet unimpressive.
Also makes branding required/recorded/checked and requires every
component entry to state the experience it creates.

Rules (SPEC.md section 2; constants verbatim):
  F4_SCOPE  Tiempos / Fraunces stand-in are for BASIC text only
  F5        important text uses a UNIQUE, IMPORTANT font
  F6        the design just has to be impressive (governing bar)
  B1        every build carries a distinct brand identity
  X1        every component is an experience
  STATIC20  fix #20 static checks (incl. B1 + X1 items)
  POLISH_F20 / TYPESET_F20 / TYPESET_CHECKBOX20 (typeset lens)

POLISH_F20 DEVIATION (recorded, not silent): SPEC section 2 prints the
POLISH_F20 text WITHOUT the B1/X1 sentence, while SPEC section 3 row 5,
section 7 check 4, and the parent task all require POLISH_F20 to include
it ("It also verifies the brand identity is recorded (fix #20 B1) and
each component entry states the experience it creates (fix #20 X1) —
consistency only, never a verdict."). The parent task's constants are
authoritative where they differ, so POLISH_F20 below is the SPEC section 2
text PLUS that sentence appended. POLISH_F20_BX1 names the sentence so
verify20 can assert it separately.

OTHER SPEC DEVIATIONS (recorded):
  - SPEC section 3 row 5 claims the POLISH_F19 ending "consistency only,
    never a verdict." has count==1 in polish-pass/SKILL.md. Measured
    count is 2 (the harmony intro uses the same phrase). The engine
    anchors on the full POLISH_F19 constant (count==1) instead.
  - SPEC section 3 row 6 names the TYPESET_F19 tail "font-optical-sizing:
    auto" as the anchor. That phrase sits mid-sentence inside TYPESET_F19
    ("Set `font-optical-sizing: auto` on the static instances ..."), so
    appending after the bare phrase would inject mid-sentence. The engine
    anchors on the full TYPESET_F19 constant (count==1) and appends after
    it — same placement, correct boundary. The "old checkbox" for this
    fix is fix19's TYPESET_CHECKBOX_NEW (count==1, typeset lens line 74).
  - SPEC section 7 check 10 reads build.sh lines + md5 from
    fix20/MANIFEST.md, but the coordinator writes that MANIFEST (not this
    engine). verify20.py therefore asserts the fix20 block marker + the
    fix15/17/19 markers + lines > post-fix19 (23,314) as hard checks, and
    matches lines/md5 against the MANIFEST only when it exists, printing
    the measured values for the coordinator to record.

FIX-UP (Nov 12, 2026 — audit #62 / dry-run #31 / sweep #25):
  fix20/fixup20.py amends five constants in place (F4_SCOPE,
  F5, STATIC20, F4_SCOPE_APP, F5_APP): F4_SCOPE gains a
  role-scoping sentence (the body-only binding attaches to the
  face in its role as the body/reading face; a pairing dealing
  Fraunces as the display face with a different body face is
  governed by F3/F5), F5 defines 'key label', STATIC20 names
  the role reading, and the build.sh block patches
  coverage.skills 169 -> 166 in skill-triggers@1.json. See
  SPEC.md section 11. verify20.py imports these constants, so
  it checks the amended texts automatically.

FIX-UP #2 (Nov 12, 2026 — sweep #26 MINOR-1): fix20/fixup20b.py
drops 'hero eyebrow or kicker' from the F5/F5_APP key-label
examples (Hallmark gate 54 bans eyebrows); the definition
('a label meant to stand out') is unchanged. See SPEC.md
section 11.

Staged-source edits (direct, build.sh copies them verbatim):
  new-skills/design-taste-frontend/SKILL.md ... F4_SCOPE+F5+F6+B1+X1
                                                    (step 4a, after D19),
                                                    STATIC20 (step 6)
  new-skills/orchestrate/SKILL.md ................. F4_SCOPE+F5+F6+B1+X1
                                                    (design-package rule),
                                                    STATIC20 (Verify 5a)
  round2-skills/polish-pass/SKILL.md .............. POLISH_F20 (harmony)
  round2-skills/polish-pass/reference/lenses/typeset.md .. TYPESET_F20
                                                    + checkbox swap
Build.sh patch block (upstream, no staged source):
  skills/ui-ux-pro-max/SKILL.md ................... F4_SCOPE_APP+F5_APP+
                                                    F6_APP+B1_APP+X1_APP
                                                    (after D19_APP)
  skills/orch-build-mvp/SKILL.md .................. same app mirrors
                                                    (step 4, after D19_APP),
                                                    STATIC20 (step 6)

Every substitution asserts count==1. A preflight pass checks every
anchor before any file is written, so a bad anchor aborts before
touching anything. D19_APP occurs TWICE in build.sh (once per patched
file), so the preflight anchors it WITHIN each file's fix19 patch-block
entry, never as a bare build.sh-wide count.
"""
import os
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
POLISH = os.path.join(PLUGIN, "round2-skills/polish-pass/SKILL.md")
TYPESET = os.path.join(PLUGIN, "round2-skills/polish-pass/reference/lenses/typeset.md")

# --- rule texts (SPEC section 2, verbatim) ---

F4_SCOPE = """**Body-only scope for the Tiempos rule (fix #20 — fix #19 F4 is body-only).** Tiempos and the Fraunces stand-in are for BASIC text only — body copy and plain reading text. They are NEVER used for important text. This binds each face in its role as the body/reading face: when Tiempos/Fraunces is the body face, it is never used for important text. A pairing that deals Fraunces (or Tiempos) as the *display* face, with a different face as the body face — for example the `fraunces` pairing in Taste's type catalogue (display Fraunces, Figtree body) — is governed by fix #19 F3 / fix #20 F5, not by this scope rule: on that build the face is the display face, not the body stand-in. Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses the display face (fix #20 F5), never the body face. A build that sets a heading, hero line, call to action, or key label in the body face is an incomplete build — a static check item in step 6, never a screen verdict. Boundary: fix #19 F3 governs the display/important face; fix #19 F4 governs basic text only. A face is either the display face (important text) or the body face (basic text), never both on the same build — except a scoped, recorded exception under this scope rule. Where a dealt theme names the same face for display and body, the design-lead deals a distinct display face and records it in `docs/design-tokens.md`; keeping the collision is a scoped, recorded exception with a fix #19 D19 reason AND the impressive-bar justification (fix #20 F6) — the exception is about the FACE, never about the delivery format (fix #19 F2 still binds: static instances, no system fallback)."""

F5 = """**Important text uses a unique, important font (fix #20 F5).** Anything supposed to be important — headings, display type, hero text, emphasis, key labels, calls to action, anything meant to stand out — uses a UNIQUE, IMPORTANT font: a distinctive display face, chosen through the design skills (the dealt display face in Taste step 4a / the ui-ux-pro-max type scale) and recorded in `docs/design-tokens.md`'s Type list with its fix #19 D19 reason and its impressive-bar justification (fix #20 F6). Not the body face, not a generic/system font. A 'key label' is a label meant to stand out — a featured section label, an emphasis badge or price label. Ordinary small labels — nav links, table heads, captions, chips, form labels, meta rows — follow the Hallmark gates: the body face, a step smaller, sentence case, untracked. The display face is self-hosted (bundled static instances + `@font-face`, fix #19 F2). A build that sets important text in the body face, or in a generic/system font, is an incomplete build — a static check item in step 6, never a screen verdict."""

F6 = """**The design just has to be impressive (fix #20 F6 — the governing bar).** The font rules serve this standard; a font choice that is correct per the rules but leaves the design unimpressive still fails. The finish review judges impressiveness as a verdict — browser-qa's visual verdict on the rendered screens, never a static check — and the decision record must state, for the important font on each surface, why it is the impressive choice for that surface (what makes it stand out, what it beats, why this surface earns it). A decision record that cannot say why the important font is impressive is an incomplete build. This bar connects to, and does not replace, the existing posture: more-not-bolder (fix #13), the E1 creativity push (trailblazing, not dumb), and fix #19 D19 (the six-dimension reason). A design that is rule-correct but unimpressive fails at the finish review; a design that is impressive but breaks a ban still fails — the bar governs, the bans bind."""

B1 = """**Every build carries a distinct brand identity (fix #20 B1).** The build carries the product's own brand — its wordmark, its identity tokens (the name, the mark, the voice, the palette and type that are its own), and its voice — recorded in the decision record (`docs/design-tokens.md` / MASTER.md on app surfaces). The brand is the through-line: every surface, component, and decision expresses it. A build with no recorded brand identity — no wordmark, no identity tokens, no voice on the record — is an incomplete build — a static check item in step 6, never a screen verdict. The brand is generated through the skills (the dealt direction in Taste step 4a / the ui-ux-pro-max identity), never inherited from a template; a build that reads as a generic template has, by definition, no brand. When a project already has a brand (a real product, a real wordmark), the record names it and the build conforms to it; when it does not, the build deals one and records it."""

X1 = """**Every component is an experience (fix #20 X1).** Each component is designed as a moment/interaction, not a static functional block. Every component entry in the decision record states the experience it creates — what it feels like, what moment it is — alongside its six fix #19 D19 dimension lines (Motion / Theme / Texture / Visuals / Techniques / Colors). A component recorded only as a functional block ("a card that shows X", "a list of items") with no experience statement is an incomplete build — a static check item in step 6, never a screen verdict. The experience statement is the component's own: what the user feels using it, what moment it stages, what it does that a static block would not. A component with no interactive or felt quality records that explicitly (`no felt moment — <reason>`, e.g. a legally-required static notice) — an explicit none, never a missing line."""

STATIC20 = """**Fix #20 static checks (all static checks, never screen verdicts).** (F4 scope) The Type list marks the body face as body-only — the body face is the face serving as body/reading text on that build, so a pairing that deals Fraunces as the display face (with a different body face) is checked under F5, not here; no heading, display, hero, call-to-action, or key-label token points at the body face; a dealt theme naming the same face for display and body is either re-dealt with a distinct display face or recorded as a scoped exception with a fix #19 D19 reason and a fix #20 F6 justification. (F5) Every important-text token points at the display face; the display face is recorded with its fix #19 D19 reason and its fix #20 F6 justification; a build setting important text in the body face or a generic/system font is an incomplete build. (F6 record) The decision record states, for the important font on each surface, why it is the impressive choice for that surface; a record that cannot say so is an incomplete build. (F6 verdict) The impressiveness verdict itself is browser-qa's at the finish review, never a static check. (B1) The decision record names the build's brand identity (wordmark, identity tokens, voice); a build with no recorded brand identity is an incomplete build. (X1) Every component entry in the decision record states the experience it creates (what it feels like, what moment it is) alongside the six D19 dimension lines; a component recorded only as a functional block is an incomplete build."""

# --- app-surface mirrors ---

F4_SCOPE_APP = """**Body-only scope for the Tiempos rule (fix #20 — F4 is body-only, app surfaces).** On app surfaces, Tiempos and the Fraunces stand-in are for basic text only — body copy and plain reading text, never important text. Headings, display type, hero text, emphasis, key labels, and calls to action use the display face (fix #20 F5). Role-scoped (fix #20 fix-up): this binds the face as the body face; a pairing that deals Fraunces as the display face, with a different face as body, is governed by F3/F5, not by this scope rule. The full scope rule lives in `design-taste-frontend` step 4a."""

F5_APP = """**Important text uses a unique, important font (fix #20 F5, app surfaces).** On app surfaces, anything supposed to be important uses a unique, important display face, chosen through this skill's type scale and recorded in MASTER.md with its fix #19 D19 reason and its fix #20 F6 justification — never the body face, never a generic/system font. A 'key label' is a label meant to stand out (featured section label, emphasis badge, price label); ordinary small labels follow the Hallmark gates in the body face. The full F5 rule lives in `design-taste-frontend` step 4a."""

F6_APP = """**The design just has to be impressive (fix #20 F6, app surfaces).** On app surfaces, a font choice that is correct per the rules but leaves the design unimpressive still fails; the finish review (browser-qa's visual verdict) judges impressiveness, and MASTER.md states why the important font is the impressive choice for each surface. The full F6 rule lives in `design-taste-frontend` step 4a."""

B1_APP = """**Every build carries a distinct brand identity (fix #20 B1, app surfaces).** On app surfaces, the build carries the product's own brand — wordmark, identity tokens, voice — recorded in MASTER.md; every surface, component, and decision expresses it. A build with no recorded brand identity is an incomplete build. The full B1 rule lives in `design-taste-frontend` step 4a."""

X1_APP = """**Every component is an experience (fix #20 X1, app surfaces).** On app surfaces, each component is designed as a moment/interaction, not a static functional block; every component entry in MASTER.md states the experience it creates (what it feels like, what moment it is) alongside its six fix #19 D19 dimension lines. A component recorded only as a functional block is an incomplete build. The full X1 rule lives in `design-taste-frontend` step 4a."""

# --- typeset lens + polish-pass harmony ---

TYPESET_F20 = """**Body-only scope; important text gets the display face (fix #20).** The body face (Tiempos or the Fraunces stand-in) is for basic text only — a heading, hero line, call to action, or key label set in the body face is a finding. Important text uses the dealt display face; check the Type list for the face's fix #19 D19 reason and its fix #20 F6 justification (why it is the impressive choice for that surface) — a display face with no recorded justification is a finding. The squint test (check 1) is the visual proof: heading and body must read apart at a blur, by face as well as size."""

TYPESET_CHECKBOX_NEW = """- [ ] A custom typeface has a stated reason; shipped font files are static instances (one per weight, opsz baked in) — no variable file is shipped, no `system-ui` fallback (fix #19 F2); the body face is used for basic text only, and important text uses the dealt display face with its recorded impressive-choice justification (fix #20)."""

POLISH_F20_BX1 = """It also verifies the brand identity is recorded (fix #20 B1) and each component entry states the experience it creates (fix #20 X1) — consistency only, never a verdict."""

# SPEC section 2 text PLUS the B1/X1 sentence (see module docstring).
POLISH_F20 = """ The harmony check also verifies the font scope (fix #20): each Type-list body-face row is marked body-only, and no heading, display, hero, call-to-action, or key-label token points at the body face — a token that does is a harmony divergence, recorded as candidate evidence, never a verdict. It also verifies the important font's record (fix #20 F5/F6): the display face is recorded with its fix #19 D19 reason and its fix #20 F6 justification (why it is the impressive choice for that surface) — consistency only, never a verdict. """ + POLISH_F20_BX1

# --- anchors imported from fix19 (verify19 anchors; must stay verbatim) ---
import sys
sys.path.insert(0, os.path.join(PLUGIN, "fix19"))
from fix19 import (D19_RULE, STATIC19, POLISH_F19, TYPESET_F19,  # noqa: E402
                   TYPESET_CHECKBOX_NEW as TYPESET_CHECKBOX_OLD,
                   F4_RULE, F4_APP, D19_APP)

D19_END = "the quality of the reasoning itself is browser-qa's and the reviewer's judgment, not a static check."
STATIC_END = "or the failure recorded as a finding; a floor/ban break blocks."

STEP4A_ADD = ("\n\n" + F4_SCOPE + "\n\n" + F5 + "\n\n" + F6
              + "\n\n" + B1 + "\n\n" + X1)
APP_MIRRORS_ADD = ("\n\n" + F4_SCOPE_APP + "\n\n" + F5_APP + "\n\n" + F6_APP
                   + "\n\n" + B1_APP + "\n\n" + X1_APP)

# --- staged-source appends: (path, old-anchor, addition) -------------------
STAGED_SUBS = [
    # Taste step 4a: F4_SCOPE + F5 + F6 + B1 + X1 after the D19 rule.
    (TASTE, D19_END, STEP4A_ADD),
    # Taste step 6: STATIC20 after STATIC19.
    (TASTE, STATIC19, "\n\n   " + STATIC20),
    # Orchestrate design-package rule: same five rules after D19.
    (ORCH, D19_END, STEP4A_ADD),
    # Orchestrate Verify 5a: STATIC20 inline after STATIC19 (fix19
    # deviation-3 precedent: after the 5a paragraph's final sentence,
    # NOT after the two-line "...5b. Final polish" anchor).
    (ORCH, STATIC19, " " + STATIC20),
    # Polish-pass harmony: POLISH_F20 after POLISH_F19.
    (POLISH, POLISH_F19, POLISH_F20),
    # Typeset lens: TYPESET_F20 after TYPESET_F19.
    (TYPESET, TYPESET_F19, "\n\n" + TYPESET_F20),
]

# Prepend-style replacements (old -> new, full text).
REPLACEMENTS = [
    (TYPESET, TYPESET_CHECKBOX_OLD, TYPESET_CHECKBOX_NEW),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, addition) -----
BUILD_SUBS = [
    # ui-ux-pro-max: app mirrors after D19_APP (anti-generic bar area).
    ("skills/ui-ux-pro-max/SKILL.md", D19_APP, APP_MIRRORS_ADD),
    # orch-build-mvp: app mirrors after D19_APP (step 4).
    ("skills/orch-build-mvp/SKILL.md", D19_APP, APP_MIRRORS_ADD),
    # orch-build-mvp: STATIC20 in step 6 after STATIC19.
    ("skills/orch-build-mvp/SKILL.md", STATIC19, "\n\n" + STATIC20),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def build_sh_block():
    """The fix20 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix20: Tiempos body-only scope, unique important font, impressive bar, brand identity, component-as-experience (F4_SCOPE/F5/F6/B1/X1) ---")
    lines.append("# (skills/ui-ux-pro-max and orch-build-mvp are upstream; they have no")
    lines.append("#  staged source and are patched here. The staged-source halves --")
    lines.append("#  design-taste-frontend (step 4a + step 6), orchestrate (design-package")
    lines.append("#  rule + Verify 5a), polish-pass (harmony), typeset lens -- are applied")
    lines.append("#  by fix20/fix20.py to their sources. All anchors were verified")
    lines.append("#  count==1 against the post-fix19 built tree by fix20.py's preflight;")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly")
    lines.append("#  on mismatch. D19_APP occurs twice in build.sh (once per patched")
    lines.append("#  file) -- the runtime asserts below are per FILE, never build.sh-wide.)")
    lines.append("# Placement: before STEP 5 (after the fix19 block).")
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
    lines.append("    assert n == 1, f\"fix20 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    open(p, \"w\").write(t.replace(old, old + add))")
    lines.append("print(\"fix20 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def fix19_block_region(build_text):
    """The fix19 patch block inside build.sh (for per-entry anchoring)."""
    start = build_text.find("# --- fix19:")
    assert start != -1, "PREFLIGHT build.sh: fix19 block marker not found"
    end = build_text.find("# STEP 5 — Counts", start)
    assert end != -1, "PREFLIGHT build.sh: STEP 5 anchor not found"
    return build_text[start:end]


def entry_slice(region, rel, occurrence=0):
    """Slice of one fix19 subs entry (from its rel line to the next entry)."""
    needle = "(%s," % repr(rel)
    idx = -1
    for _ in range(occurrence + 1):
        idx = region.find(needle, idx + 1)
        assert idx != -1, f"PREFLIGHT build.sh: fix19 entry {occurrence} for {rel} not found"
    nxt = region.find("  (", idx + 1)
    return region[idx:nxt if nxt != -1 else len(region)]


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
    # Fix19 anchors still present verbatim in staged sources (must not
    # have been edited in place by an earlier run).
    taste = open(TASTE, encoding="utf-8").read()
    orch = open(ORCH, encoding="utf-8").read()
    for path, text, rules in ((TASTE, taste, (D19_RULE, F4_RULE, STATIC19)),
                              (ORCH, orch, (D19_RULE, F4_RULE, STATIC19))):
        for rule in rules:
            assert text.count(rule) == 1, \
                f"PREFLIGHT {path}: fix19 anchor missing/changed: {rule[:60]!r}"
    assert open(POLISH, encoding="utf-8").read().count(POLISH_F19) == 1
    assert open(TYPESET, encoding="utf-8").read().count(TYPESET_F19) == 1
    # Orchestrate 5b bullet must still follow the 5a paragraph (STATIC19
    # sits before it); taste step-6 STATIC19 is followed by the gate block.
    assert orch.find(STATIC19) < orch.find("**5b. Final polish**"), \
        "PREFLIGHT orchestrate: STATIC19 must sit before the 5b bullet"
    # No fix20 rule text already present (idempotency guard).
    for path, text in ((TASTE, taste), (ORCH, orch)):
        for rule in (F4_SCOPE, F5, F6, B1, X1, STATIC20):
            assert rule not in text, f"PREFLIGHT {path}: fix20 text already present: {rule[:60]!r}"
    for path in (POLISH, TYPESET):
        text = open(path, encoding="utf-8").read()
        for rule in (POLISH_F20, TYPESET_F20, TYPESET_CHECKBOX_NEW):
            assert rule not in text, f"PREFLIGHT {path}: fix20 text already present: {rule[:60]!r}"
    # Built-tree anchors, per file (never a bare build.sh-wide count).
    uipro = open(os.path.join(BUILT, "skills/ui-ux-pro-max/SKILL.md"), encoding="utf-8").read()
    mvp = open(os.path.join(BUILT, "skills/orch-build-mvp/SKILL.md"), encoding="utf-8").read()
    assert uipro.count(D19_APP) == 1, f"PREFLIGHT built ui-ux-pro-max: D19_APP count={uipro.count(D19_APP)}"
    assert uipro.count(F4_APP) == 1, "PREFLIGHT built ui-ux-pro-max: F4_APP missing"
    assert mvp.count(D19_APP) == 1, f"PREFLIGHT built orch-build-mvp: D19_APP count={mvp.count(D19_APP)}"
    assert mvp.count(STATIC19) == 1, "PREFLIGHT built orch-build-mvp: STATIC19 missing"
    for text, name in ((uipro, "ui-ux-pro-max"), (mvp, "orch-build-mvp")):
        for rule in (F4_SCOPE_APP, F5_APP, F6_APP, B1_APP, X1_APP, STATIC20):
            assert rule not in text, f"PREFLIGHT built {name}: fix20 text already present: {rule[:60]!r}"
    # build.sh: per-entry anchoring inside the fix19 block. D19_APP occurs
    # twice build.sh-wide (once per patched file) — assert count==1 within
    # EACH file's fix19 entry slice, never the bare total.
    btext = open(BUILD_SH, encoding="utf-8").read()
    region = fix19_block_region(btext)
    assert region.count(D19_APP) == 2, \
        f"PREFLIGHT build.sh fix19 block: expected D19_APP x2, got {region.count(D19_APP)}"
    uipro_entry = entry_slice(region, "skills/ui-ux-pro-max/SKILL.md", 0)
    assert uipro_entry.count(D19_APP) == 1, "PREFLIGHT build.sh: D19_APP not exactly once in the ui-ux-pro-max fix19 entry"
    mvp_entry = entry_slice(region, "skills/orch-build-mvp/SKILL.md", 0)
    assert mvp_entry.count(D19_APP) == 1, "PREFLIGHT build.sh: D19_APP not exactly once in the orch-build-mvp fix19 entry"
    mvp_static_entry = entry_slice(region, "skills/orch-build-mvp/SKILL.md", 1)
    assert mvp_static_entry.count(STATIC19) == 1, "PREFLIGHT build.sh: STATIC19 not exactly once in the orch-build-mvp fix19 step-6 entry"
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fix20 upstream block applied" not in btext, "PREFLIGHT build.sh: fix20 block already present"
    # No banned terms (fix #16 scrub) in any addition or in the block itself.
    additions = [add for _, _, add in STAGED_SUBS]
    additions += [new for _, _, new in REPLACEMENTS]
    additions += [add for _, _, add in BUILD_SUBS]
    block = build_sh_block()
    for blob in additions + [block]:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fix20 addition"
    print("preflight OK: %d staged anchors + 3 built-tree anchors + "
          "build.sh per-entry anchors (D19_APP x1 per fix19 entry) + "
          "banned-term scan clean"
          % sum(len(v) for v in grouped.values()))


def self_checks():
    """After the edits: every addition present verbatim, fix19 intact."""
    taste = open(TASTE, encoding="utf-8").read()
    orch = open(ORCH, encoding="utf-8").read()
    polish = open(POLISH, encoding="utf-8").read()
    typeset = open(TYPESET, encoding="utf-8").read()
    for text, name, rules in (
            (taste, "Taste", (F4_SCOPE, F5, F6, B1, X1, STATIC20)),
            (orch, "orchestrate", (F4_SCOPE, F5, F6, B1, X1, STATIC20))):
        for rule in rules:
            assert text.count(rule) == 1, f"SELF-CHECK {name}: missing fix20 text: {rule[:60]!r}"
        for rule in (D19_RULE, F4_RULE, STATIC19):
            assert text.count(rule) == 1, f"SELF-CHECK {name}: fix19 anchor damaged: {rule[:60]!r}"
        assert text.find(STATIC20) > text.find(STATIC19), f"SELF-CHECK {name}: STATIC20 not after STATIC19"
        assert text.find(F4_SCOPE) > text.find(D19_RULE), f"SELF-CHECK {name}: F4_SCOPE not after D19"
    assert polish.count(POLISH_F20) == 1, "SELF-CHECK polish-pass: POLISH_F20 missing"
    assert POLISH_F20_BX1 in polish, "SELF-CHECK polish-pass: B1/X1 sentence missing from POLISH_F20"
    assert polish.count(POLISH_F19) == 1, "SELF-CHECK polish-pass: POLISH_F19 damaged"
    assert typeset.count(TYPESET_F20) == 1, "SELF-CHECK typeset: TYPESET_F20 missing"
    assert typeset.find(TYPESET_F20) > typeset.find(TYPESET_F19), "SELF-CHECK typeset: TYPESET_F20 not after TYPESET_F19"
    assert typeset.count(TYPESET_CHECKBOX_NEW) == 1, "SELF-CHECK typeset: new checkbox missing"
    assert TYPESET_CHECKBOX_OLD not in typeset, "SELF-CHECK typeset: fix19 checkbox still present"
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert "fix20 upstream block applied" in btext, "SELF-CHECK build.sh: fix20 block missing"
    assert btext.count("# STEP 5 — Counts") == 1, "SELF-CHECK build.sh: STEP 5 anchor damaged"
    print("self-checks OK: all fix20 additions present verbatim in staged sources; fix19 anchors intact")


def main():
    preflight()

    # 1. Staged-source edits (replacements first, then appends).
    for path, old, new in REPLACEMENTS:
        text = open(path, encoding="utf-8").read()
        assert text.count(old) == 1, f"{path}: replacement anchor not found exactly once: {old[:70]!r}"
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
        print(f"{os.path.relpath(path, PLUGIN)}: replacement applied")
    by_path = {}
    for path, old, add in STAGED_SUBS:
        by_path.setdefault(path, []).append((old, add))
    for path, subs in by_path.items():
        text = open(path, encoding="utf-8").read()
        for old, add in subs:
            assert text.count(old) == 1, f"{path}: anchor not found exactly once: {old[:70]!r}"
            text = text.replace(old, old + add)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN)}: {len(subs)} substitutions applied")

    # 2. Backup build.sh (keep the first pre-fix20 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix20")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix20")
    else:
        print("build.sh.before-fix20 already exists, kept")

    # 3. Append the fix20 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print(f"build.sh: fix20 block appended ({len(BUILD_SUBS)} upstream subs, "
          f"{len(block.splitlines())} lines)")

    self_checks()


if __name__ == "__main__":
    main()
