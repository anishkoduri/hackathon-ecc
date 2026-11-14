#!/usr/bin/env python3
"""Fix program #17: back-port ALL Campus Eats render feedback into the
package so a re-render looks like the final version (v5, 61 elements
literal), not the first (v1, 25).

Rules (SPEC-DRAFT.md sections A, as corrected by PARENT-GUIDANCE.md):
  U1  unique page-only elements, at least three per build
  T1  type fills its bubble (60% fill ratio, 25% dead-space band)
  F1  every font decision cites the type system (extends C1-C3)
  M1-M6  motion / interactivity density (scroll entrances with 1500ms
        fail-safe, hover micros, life in existing pieces, >=1 interactive
        bit per page, reduced motion respected)
  E1  creative freedom, strengthened to an ACTIVE PUSH to be trailblazing
        (Anish, Nov 11: "more creative and push boundaries, just not in a
        dumb way and in a trailblazing way")
  Sticker exceptions (parent decision 1): hand-drawn ink marks and scroll
        rise-and-settle entrances as SCOPED, NAMED exceptions in sticker.md
  R3 widening: a theme-matched handmade surface treatment (tape,
        perforation, washi, hand-drawn ink mark) counts as a treatment kind

Decisions recorded here (parent guidance overrides SPEC-DRAFT.md where
they differ):
  - Re-trace target is 59-63 (final artifact 61 literal +/-2), NOT the
    SPEC draft's 30-34 band (built on the mistaken 32-as-final premise).
    The re-trace is an independent recount of the final artifact under
    BASELINE.md's literal rule, plus a coverage mapping; see MANIFEST.md.
  - M1 scope is Option B (keep the Taste landing-page scroll ban in
    references/motion.md); scroll entrances on Sticker builds are licensed
    by the sticker.md exception B, not by M1.
  - No new inventory: tape/perforation are covered by the R3 widening, NOT
    by new less-flat-ui catalogue entries (treatments stay 1..23).

Applies the rules to the plugin's staged sources, and appends a build.sh
patch block (LAST, before STEP 5, after the fix16 block) for the upstream
files that have no staged source (ui-ux-pro-max, make-interfaces-feel-better,
motion-foundations/patterns/advanced, orch-build-mvp).

Staged-source edits (direct, build.sh copies them verbatim):
  new-skills/design-taste-frontend/SKILL.md ......... U1, T1, F1, E1 (step 4a);
                                                    fix17 static checks (step 6)
  new-skills/design-taste-frontend/references/hallmark/references/themes/sticker.md
                                                    exceptions A + B, Motion pointer
  new-skills/orchestrate/SKILL.md ................... E1 (design-package rule),
                                                    fix17 static checks (Verify 5a)
  round2-skills/polish-pass/SKILL.md ................ F1 + T1 (harmony check)
  round2-skills/polish-pass/reference/lenses/typeset.md .. T1 (Rules + Verify)
  ~/workspace/cursor-skills/less-flat-ui/SKILL.md ... U1 (record), R3 widening
Build.sh patch block (upstream, no staged source):
  skills/ui-ux-pro-max/SKILL.md ..................... U1 (app), E1 (app), T1, F1
  skills/make-interfaces-feel-better/SKILL.md ....... M3-M5 (+ default motion set)
  skills/motion-foundations/SKILL.md ................ M1, M2, M6
  skills/motion-patterns/SKILL.md ................... M1, M2 (rule 9/10 + example)
  skills/motion-advanced/SKILL.md ................... M2 (useScrollReveal fail-safe)
  skills/orch-build-mvp/SKILL.md .................... E1 (step 4),
                                                    fix17 static checks (step 6)

Every substitution asserts count==1. A preflight pass checks every anchor
before any file is written, so a bad anchor aborts before touching anything.
"""
import os
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
STICKER = os.path.join(PLUGIN, "new-skills/design-taste-frontend/references/hallmark/references/themes/sticker.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
POLISH = os.path.join(PLUGIN, "round2-skills/polish-pass/SKILL.md")
TYPESET = os.path.join(PLUGIN, "round2-skills/polish-pass/reference/lenses/typeset.md")
LESSFLAT = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")

# --- rule texts ------------------------------------------------------------

U1_RULE = """**Unique page-only elements — at least three per build (fix #17 U1).** Every build invents at least THREE unique, one-of-a-kind elements and records them in the 'Unique elements' list in `docs/design-tokens.md`. 'Unique' means ALL FOUR: (1) page-only — the element occurs on exactly one page of this build and is not repeated on any other page or surface of the same build (a repeated instance is one element used twice, not two unique elements — and a repeated element is a pattern, not unique); (2) not a reusable pattern — it is not built from a sections-library recipe, a ui-ux-pro-max pattern, a dealt moment, a Range pattern element, a less-flat-ui treatment, a hero spec, or any other catalogue item in any skill; (3) not in any skill's catalogue — no skill file names it, depicts it, or prescribes it as an option; (4) invented for that page through the skills — generated from the dealt theme's material world (its material, tokens, palette balance, and do-nots) to serve one section's job. Each list entry names the element, its surface, its kind (BASELINE.md counting rule), the section job it serves, the theme material it draws on, and why it is not a catalogue item. At least one of the three must sit on the primary page. A build whose Unique list has fewer than three complete entries is incomplete — a static check item in step 6, never a screen verdict. Each unique element counts once under the BASELINE.md counting rule, as its kind."""

T1_RULE = """**Type fills its bubble (fix #17 T1).** For every display, figure, or label type set inside a bounded container — a tile, card, bubble, chip, tag, badge, stat fill, or price-ladder cell — the size is chosen so the type fills its container: the rendered glyph bounding box must span at least 60% of the container's inner width where the layout fills horizontally, or at least 60% of its inner height where it fills vertically, measured in-page (glyph box vs container box) and recorded per surface in `docs/design-tokens.md`'s Type list as surface → face/size → container inner size → fill ratio. Bounded by no-overflow (no text clipped or spilling its container at 1440 or 390) and no-crowding (type never touches the container edge — the inset is at least the theme's own padding/rhythm token — and adjacent type runs never collide; the existing check.mjs collision/overflow findings govern). The step-6 screenshot check includes a dead-space item: a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding, fed to the fix batch like other checks. Flowing body copy is not a bubble — the C3 body-measure rule (65–75ch) governs there, not this rule."""

F1_RULE = """**Every font decision cites the type system (fix #17 F1 — extends fix #15 C1–C3, does not replace them).** Every face, weight, size, and tracking value on the page is an explicit value from the skills' type system — the dealt pairing (Taste step 4a / ui-ux-pro-max type scale), the theme file's type voice, or the `system.md` Type scale step. No face, weight, size, or tracking on the page is a browser or framework default, and no value is chosen flat (unstated, inherited, 'whatever it came with'). The Type list in `docs/design-tokens.md` gains two columns — weight and tracking — and every row gains a Source cell naming the exact skill text the choice comes from (pairing line, theme-file line, or scale step). A row with an empty Source cell, a Source of 'default', or a value that traces to no recorded pairing/scale/theme line is an incomplete build — a static check item in step 6, never a screen verdict. The polish-pass harmony check verifies the Type list including the Source cells (consistency only — a surface whose type does not trace to the recorded pairing/scale is a harmony divergence, recorded as candidate evidence, never a verdict). App surfaces record theirs the same way in `design-system/<project-slug>/MASTER.md`, conforming to the tokens file."""

E1_RULE = """**Push boundaries — be trailblazing, not dumb (fix #17 E1).** The design-lead MUST push boundaries and aim to be trailblazing: invent original, first-of-its-kind elements for the page — the unique elements of U1 are the normal case, and a build with no element a template would not produce has not pushed far enough. 'Trailblazing' means original, first-of-its-kind decisions, not safe or derivative ones. 'Not in a dumb way' means EVERY boundary push must still: (1) serve the section's job, named in the Unique-list entry; (2) fit the theme's material world — material, tokens, palette balance, do-nots; (3) obey the type/space rules — the C3 Type list, the T1 fill rule, measure and contrast checks; (4) be theme-matched (fix #15 rule A); (5) pass the craft floor; (6) pass the Hallmark floor; (7) use no violet; (8) be anti-derivative — never based on a searched reference, and the entry names the theme material it draws on, never a URL; (9) stand or fall on browser-qa's verdict on the rendered screen, which is the final word on whether the invented element reads as distinct rather than generic or template. NOT within reason: a new theme (re-deal instead, Taste step 4); a new palette (the Tokens block is the page's `:root` — re-deal once if it clashes); a template pattern (a sections-library recipe reused as-is is a catalogue item, not an invention — it fails U1's not-a-catalogue test); breaking a floor or a ban (craft-floor bans are absolute; the Hallmark floor binds). Each invented element's Unique-list entry carries the nine-point bound checklist, one line per bound; a missing or failed bound is a static-check finding, and a floor/ban break blocks. Distinctiveness itself is browser-qa's verdict alone."""

M1_RULE = """**M1 — Scroll entrances on motion-governed surfaces (fix #17).** On surfaces governed by the motion-* skills (React/Next.js app surfaces), each content section enters on scroll: `whileInView` with `viewport={{ once: true }}` (motion-patterns rule 7), using motion-foundations tokens. Each entrance is recorded per surface in `docs/design-tokens.md`'s Motion list (surface → entrance → tokens used). A section with no entrance and no recorded reason is an incomplete build — a static check item in step 6, never a screen verdict. SCOPE: the design-taste-frontend page system keeps its standing rule (`references/motion.md`: 'Scrolling moves nothing but the dealt moment') — scroll entrances do NOT apply to Taste landing pages under this rule. A theme file may record a scoped, named exception permitting scroll entrances as that theme's own motion (see sticker.md, fix #17 exception B) — the exception is the theme's decision, not this rule's."""

M2_RULE = """**M2 — 1500ms fail-safe: content can never stay hidden (fix #17).** Every scroll-entrance element becomes fully visible within 1500ms of entering the viewport even if its observer never fires: a timed fail-safe (a timer or CSS fallback that forces the visible state — opacity 1, transform none — 1500ms after mount/entry) is a required part of every entrance implementation, and its presence is recorded in the Motion list (surface → entrance → fail-safe mechanism). The step-6 check scrolls to each section, waits 1500ms, and confirms in the screenshot that no content is still hidden (no element left at opacity 0 or off-screen). A section still hidden after the wait is a finding, fed to the fix batch. Under `prefers-reduced-motion: reduce` the content is visible at rest, with no entrance to fail — reduced-motion renders are exempt from the entrance itself but never from visibility."""

M3_RULE = """**M3 — Hover micro-interactions on every interactive element (fix #17).** Every link, button, linked card, and linked photograph has a visible hover state per the hover layer (`references/motion.md`, hover-layer table) and the motion defaults (enter: opacity + small translateY; press: scale 0.97; transitions scoped to the changed properties, never `transition: all`). A hover may also warm a name's colour on a fill (never pink text on the paper ground), lift-and-pop a card or photograph on tap, or wiggle a sticker — each distinct hover behaviour is its own authored motion, recorded in `docs/design-tokens.md`'s Motion list. The step-6 check shoots a hovered card and a hovered photograph at 1440 (the existing Taste rule) and records hovered shots per interactive surface; an interactive element with no visible hover change is a finding, fed to the fix batch like other checks."""

M4_RULE = """**M4 — Life in existing pieces (fix #17).** Every authored motion element already on the page — hero entrance, dealt hero loop (fix #15 R4), dealt moment, count, diagram pulse, effect/scene loop — must actually move in the rendered page. Ambient loops on existing pieces (a card's bob, a seal's breathe, a flag's sway, a heart's beat, a marquee's pause-on-hover) are authored motion too, each recorded in the Motion list with its trigger (on load / on scroll / on hover / timed loop / count). The D1 screenshot pass (and browser-qa's visual loop) confirms each one moves; a piece that should move and does not is a finding."""

M5_RULE = """**M5 — At least one small interactive bit per page, where the page has one (fix #17).** Each page that carries an interactive surface — a stepper, toggle, tab, filter, counter, peek-list, or live total — must have at least one working interactive bit recorded in `docs/design-tokens.md` (name, surface, what it does, what state it shows). A page with an interactive surface and no recorded bit is incomplete — a static check item in step 6, never a screen verdict. A page with no interactive surface is exempt, and the exemption is recorded ('no interactive surface — none'). The bit is small: one control and its feedback, not a feature."""

M6_RULE = """**M6 — Reduced motion respected in CSS and JS (fix #17).** Every motion rule in this section is gated on `prefers-reduced-motion: reduce`, in both layers: CSS via the `@media (prefers-reduced-motion: reduce)` block that disables all transforms and limits opacity transitions to ≤ 0.2s (motion-foundations), and JS via `useSafeMotion` / `motionConfig.shouldAnimate` (motion-foundations) or the Taste motion layer's reduced-motion rest. Checkable: the built page contains the reduced-motion CSS block and the JS guard, and the step-6 record notes the reduced-motion render (or records that it did not run — never claim a render pass that did not run). Content under reduced motion is readable at rest, without script."""

STATIC_CHECKS = """**Fix #17 static checks (all static checks, never screen verdicts).** (U1) The 'Unique elements' list in `docs/design-tokens.md` has at least three complete entries — element, surface, kind, section job, theme material, why-not-a-catalogue-item — with at least one on the primary page; fewer is an incomplete build. (F1) The Type list gains weight and tracking columns and a Source cell per row naming the exact skill text; a row with an empty or 'default' Source is an incomplete build. (T1) Each Type-list row records the fill ratio (glyph box / container box, minimum 0.60), and the screenshot check includes the dead-space item (a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding). (M1–M6) The Motion list records, per surface: each scroll entrance with its tokens and fail-safe mechanism (M1/M2, motion-governed surfaces only — landing pages keep the Taste scroll ban except where a theme file records a scoped exception); hovered shots per interactive surface and each distinct hover behaviour (M3); each authored motion piece with its trigger, confirmed moving in the D1 pass (M4); one working interactive bit per page with an interactive surface, or the recorded exemption 'no interactive surface — none' (M5); the reduced-motion render noted, or recorded as not run (M6). (E1) Each Unique-list entry carries the nine-point bound checklist, all passing, or the failure recorded as a finding; a floor/ban break blocks."""

# --- app-surface mirrors (same rules, app homes) ---------------------------

U1_APP = """**Unique page-only elements (fix #17 U1, app surfaces).** Each primary app surface carries at least 1 page-only element (invented through this skill's styles/palettes/pairings, never a searched reference), recorded in the 'Unique elements' list in `docs/design-tokens.md` (or MASTER.md) with its kind, the job it serves, and why it is not a catalogue item; a surface with none records `none — <reason>`. The full U1 rule (at least three per build, four-part uniqueness test) lives in `design-taste-frontend` step 4a."""

# --- sticker.md scoped exceptions (parent decision 1) ---------------------

STICKER_EXCEPTIONS = """## Scoped exceptions (decided, not drift)

- **Hand-drawn ink marks (fix #17, exception A).** A hand-drawn ink scribble underline, doodle trail, or drawn seal/emblem (e.g. a Taco Compass) is permitted as a one-off ink-on-paper element in theme colours — it is ink on the theme's paper, not a mascot or a drawn-sticker character. The 'Never a drawn sticker, mascot or doodle' do-not stays intact for everything else. Added at Anish's direction in the Campus Eats cold-start render, Nov 11, 2026.
- **Scroll rise-and-settle entrances (fix #17, exception B).** Content sections may enter on scroll with a staggered rise-and-settle entrance (with the 1500ms fail-safe, fix #17 M2) as sticker motion. The 'nothing on scroll' motion rule stays intact beyond that motion. Added at Anish's direction in the Campus Eats cold-start render, Nov 11, 2026."""

# --- less-flat-ui: R3 widening + U1 record --------------------------------

R3_WIDEN = """ A theme-matched handmade surface treatment — tape, perforation, washi, a hand-drawn ink mark — counts as a treatment kind (fix #17): the kind is the treatment application on one surface, not the catalogue entry; the 23-entry catalogue is the vocabulary, not the limit."""

U1_LF = """ Per screen, record the page-only elements alongside the treatments (surface → page-only elements, kind, theme-fit); a screen with none records `none — <reason>` (fix #17 U1, app/dashboard count). Handmade surface treatments (tape, perforation, washi, hand-drawn ink marks) record the same way and count toward the two-distinct-kinds check."""

# --- polish-pass: F1 + T1 verification (harmony) ---------------------------

POLISH_F1_T1 = """ The harmony check also verifies the Type list's weight and tracking columns and Source cells (fix #17 F1): a row with an empty or 'default' Source, or a value tracing to no recorded pairing/scale/theme line, is a harmony divergence, recorded as candidate evidence, never a verdict. It also verifies the T1 fill ratios recorded per Type-list row (glyph box ≥ 60% of the container's inner size) — consistency only, never a verdict."""

# --- typeset lens: T1 -------------------------------------------------------

TYPESET_RULE = """
- [ ] Display, figure and label type fills its bubble (glyph box ≥ 60% of the container's inner size); no dead space, no overflow, no crowding (fix #17 T1)."""

TYPESET_VERIFY = """
- Fill (fix #17 T1): display, figure and label type inside a bounded container fills it (glyph box ≥ 60% of the container's inner size along the fill axis); a bubble, card, or tile whose largest empty band exceeds 25% of its minor dimension is a finding, fed to the fix batch like other checks."""

# --- make-interfaces-feel-better: default motion set + M3-M5 --------------

MIFE_MOTION = """

**Default motion set (fix #17, v4-level).** Every page carries the default motion set — scroll entrances with a 1500ms fail-safe (M1/M2, on motion-governed surfaces; landing pages keep the Taste scroll ban except where a theme file records a scoped exception), hover micro-interactions on every interactive element (M3), life in existing pieces (M4), and at least one small interactive bit per page where the page has one (M5) — decided here for feel/timing, implemented with the motion-* skills. Reduced motion is respected in CSS and JS (M6). Each item is recorded in `docs/design-tokens.md`'s Motion list (surface → item → trigger/tokens/fail-safe).

""" + M3_RULE + """

""" + M4_RULE + """

""" + M5_RULE

MIFE_CHECKLIST = """
- Every interactive element has a visible hover state, with hovered shots recorded per interactive surface (fix #17 M3).
- Every authored motion element actually moves in the rendered page; each recorded in the Motion list with its trigger (fix #17 M4).
- Each page with an interactive surface has at least one working interactive bit recorded, or the exemption noted (fix #17 M5)."""

# --- motion skills: M1/M2 rules, fail-safe, M6 ------------------------------

M6_ACCESS = """ Under reduced motion the fail-safe still reveals (opacity-only ≤ 0.2s) — content is visible at rest with no entrance to fail (fix #17 M2/M6). Every motion rule in this section is gated on `prefers-reduced-motion: reduce`, in both layers: the CSS block above and the JS guard (`useSafeMotion` / `motionConfig.shouldAnimate`); the built page must contain both, and the step-6 record notes the reduced-motion render (or records that it did not run — never claim a render pass that did not run) (fix #17 M6)."""

PATTERNS_FAILSAFE_NOTE = """

**1500ms fail-safe (fix #17 M2).** If the reveal has not fired within 1500ms of the element entering the viewport, the content is shown anyway — nothing ever stays hidden because an observer never fired. Implement with a timer or CSS fallback that forces the visible state (opacity 1, transform none) 1500ms after mount/entry; record the mechanism in the Motion list. See `motion-advanced` `useScrollRevealSafe` for the shared implementation."""

ADVANCED_FAILSAFE = """

// 1500ms fail-safe (fix #17 M2): if the reveal has not completed within
// 1500ms of mount, force the visible state — content can never stay hidden
// because an observer never fired. Record the mechanism in the Motion list.
export function useScrollRevealSafe() {
  const { ref, style } = useScrollReveal()
  const [revealed, setRevealed] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setRevealed(true), 1500)
    return () => clearTimeout(t)
  }, [])
  return { ref, style: revealed ? { opacity: 1, y: 0 } : style }
}
"""

# --- staged-source appends: (path, old-anchor, addition) -------------------
# Addition is appended directly after the anchor (anchor kept verbatim).
STAGED_SUBS = [
    # -- Taste (design-taste-frontend): step 4a gets U1 + T1 + F1 + E1 as
    #    four new bold lines after the step-4a paragraph (conflict C1: do
    #    NOT keep appending into the giant :246 line).
    (TASTE,
     "that element is recorded as its own type moment in `docs/design-tokens.md`, distinct from the surface carrying it.",
     "\n\n" + U1_RULE + "\n\n" + T1_RULE + "\n\n" + F1_RULE + "\n\n" + E1_RULE),
    # -- Taste step 6: consolidated fix17 static checks, new paragraph after
    #    the step-6 paragraph (conflict C2: one consolidated list, not four
    #    separate sentences).
    (TASTE,
     "for overflow, collide and tap-size, and runs copy-lint, whose FAILs block like the checker's:",
     "\n\n   " + STATIC_CHECKS),
    # -- orchestrate: E1 after the canonical block in the design-package rule.
    (ORCH,
     "Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit).",
     "\n\n" + E1_RULE),
    # -- orchestrate Verify 5a: consolidated fix17 static checks (engine-side).
    (ORCH,
     "a dealt moment with neither is an incomplete build (fix #15 R1).",
     " " + STATIC_CHECKS),
    # -- polish-pass harmony: F1 + T1 verification (consistency only).
    (POLISH,
     "recorded as candidate evidence, never a verdict (fix #15 C3 — consistency only).",
     POLISH_F1_T1),
    # -- typeset lens: T1 rule checkbox + Verify bullet.
    (TYPESET,
     "- [ ] Text zooms to 200% without clipping or overlap.",
     TYPESET_RULE),
    (TYPESET,
     "- Typography should rise with no overflow regressions.",
     TYPESET_VERIFY),
    # -- less-flat-ui (standalone source of truth): R3 widening + U1 record.
    (LESSFLAT,
     "The second kind must be theme-matched (rule A governs the choice) — do not hard-code which kind, only that a second distinct kind is required.",
     R3_WIDEN),
    (LESSFLAT,
     "treatments are recorded under it, not instead of it.",
     U1_LF),
    # -- sticker.md: scoped exceptions A + B after the last do-not.
    (STICKER,
     "without the product's own pictures, the fills carry the page.",
     "\n\n" + STICKER_EXCEPTIONS),
]

# Prepend-style replacements (old -> new, full text).
REPLACEMENTS = [
    # sticker.md Motion line: pointer to the scoped exception (do-not stays).
    (STICKER,
     "nothing on scroll.",
     "nothing on scroll, except the scoped exception in 'Scoped exceptions' below (scroll rise-and-settle entrances as sticker motion)."),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, addition) ------
# All are appends: new = old + addition.
BUILD_SUBS = [
    # ui-ux-pro-max: U1 (app) + E1 (app) after the anti-generic bar.
    ("skills/ui-ux-pro-max/SKILL.md",
     "Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether a screen fails any of these — this skill never states a screen pass/fail.",
     "\n\n" + U1_APP + "\n\n" + E1_RULE),
    # ui-ux-pro-max: T1 + F1 after the C1 sentence in the type-scale step.
    ("skills/ui-ux-pro-max/SKILL.md",
     "The dealt pairing / type scale is the ONLY permitted faces on the build — no other face is introduced; record the pairing + its source in `docs/design-tokens.md` (fix #15 C1).",
     " " + T1_RULE + " " + F1_RULE),
    # motion-patterns: rule 9 = M1, rule 10 = M2, after rule 8.
    ("skills/motion-patterns/SKILL.md",
     "8. **All token values are imported from `motion-foundations`.** No inline numbers.",
     "\n9. " + M1_RULE + "\n10. " + M2_RULE),
    # motion-patterns: fail-safe note after the scroll-reveal code block.
    ("skills/motion-patterns/SKILL.md",
     "  transition={{ duration: motionTokens.duration.slow, ease: motionTokens.easing.smooth }}\n/>\n```",
     PATTERNS_FAILSAFE_NOTE),
    # motion-foundations: rule 9 = M1, rule 10 = M2, after rule 8.
    ("skills/motion-foundations/SKILL.md",
     "8. **Never read `window` or `navigator` at module level.** Always guard with `typeof window !== \"undefined\"`.",
     "\n9. " + M1_RULE + "\n10. " + M2_RULE),
    # motion-foundations: M6 note in Accessibility, after the degrade-gracefully
    # sentence.
    ("skills/motion-foundations/SKILL.md",
     "Motion must degrade gracefully. It must never disappear abruptly in a way\nthat causes layout shift or confuses orientation.",
     M6_ACCESS),
    # motion-advanced: fail-safe hook variant after the useScrollReveal Usage.
    ("skills/motion-advanced/SKILL.md",
     "<motion.section ref={ref} style={style} />\n```",
     ADVANCED_FAILSAFE),
    # make-interfaces-feel-better: default motion set + M3-M5 in Motion section.
    ("skills/make-interfaces-feel-better/SKILL.md",
     "- Icon swaps: cross-fade with opacity, scale, and blur instead of instant\n  visibility toggles.",
     MIFE_MOTION),
    # make-interfaces-feel-better: M3-M5 checklist items.
    ("skills/make-interfaces-feel-better/SKILL.md",
     "- Small controls still have usable hit areas.",
     MIFE_CHECKLIST),
    # orch-build-mvp: E1 after the GAN-evaluator sentence (step 4).
    ("skills/orch-build-mvp/SKILL.md",
     "The GAN evaluator does NOT judge screen distinctiveness: its Design Quality / Originality rows defer to browser-qa (see `gan-style-harness`).",
     "\n\n" + E1_RULE),
    # orch-build-mvp: consolidated fix17 static checks (step 6, engine-side).
    ("skills/orch-build-mvp/SKILL.md",
     "a dealt moment with neither is an incomplete build (fix #15 R1).",
     " " + STATIC_CHECKS),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]


def build_sh_block():
    """The fix17 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix17: back-port ALL Campus Eats render feedback (U1/T1/F1/M1-M6/E1, sticker exceptions A+B, R3 widening) ---")
    lines.append("# (skills/ui-ux-pro-max, make-interfaces-feel-better, the motion-* skills and orch-build-mvp are upstream;")
    lines.append("#  they have no staged source and are patched here. The staged-source halves -- design-taste-frontend,")
    lines.append("#  sticker.md, orchestrate, polish-pass, typeset lens, less-flat-ui -- are applied by fix17/fix17.py to their")
    lines.append("#  sources. All anchors were verified count==1 against the post-fix16 built tree by fix17.py's preflight;")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly on mismatch.)")
    lines.append("# Placement: LAST, just before STEP 5 (after the fix16 block).")
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
    lines.append("    assert n == 1, f\"fix17 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    open(p, \"w\").write(t.replace(old, old + add))")
    lines.append("print(\"fix17 upstream block applied\")")
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
    # Build-sh patch anchors against the current built tree.
    for rel, old, add in BUILD_SUBS:
        p = os.path.join(BUILT, rel)
        text = open(p, encoding="utf-8").read()
        n = text.count(old)
        assert n == 1, f"PREFLIGHT built {rel}: anchor count={n}: {old[:70]!r}"
    # Build.sh insertion anchor.
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fix17 upstream block applied" not in btext, "PREFLIGHT build.sh: fix17 block already present"
    # No banned terms (fix #16 scrub) in any addition or in the block itself.
    additions = [add for _, _, add in STAGED_SUBS]
    additions += [new for _, _, new in REPLACEMENTS]
    additions += [add for _, _, add in BUILD_SUBS]
    block = build_sh_block()
    for blob in additions + [block]:
        low = blob.lower()
        for term in BANNED:
            assert term not in low, f"PREFLIGHT banned term {term!r} in a fix17 addition"
    print(f"preflight OK: {sum(len(v) for v in grouped.values())} staged anchors + "
          f"{len(BUILD_SUBS)} built-tree anchors + build.sh insertion anchor + banned-term scan clean")


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

    # 2. Backup build.sh (keep the first pre-fix17 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix17")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix17")
    else:
        print("build.sh.before-fix17 already exists, kept")

    # 3. Append the fix17 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print(f"build.sh: fix17 block appended ({len(BUILD_SUBS)} upstream subs, "
          f"{len(block.splitlines())} lines)")


if __name__ == "__main__":
    main()
