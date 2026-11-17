#!/usr/bin/env python3
"""Fix #31 re-weave: GetLayers prompts carry MORE WEIGHT (direction update
from Anish, Nov 16, 2026 ~10:02 PM CT — before the audit loop).

GetLayers is a first-class, high-priority source in the palette-first
flow, not a minor or optional entry: the design-lead consults the
GetLayers prompts FIRST — alongside or ahead of the other palette
sources — and the direction leans on GetLayers layers heavily as its
foundation. The weight is visible three ways: ordering (GetLayers
consulted first in the flow), explicit priority language in the skill,
and a check that the design direction cites the GetLayers layers USED
or CONSIDERED-AND-REJECTED with a D19 reason (same as every inventory
entry).

Constraints that STAND (unchanged): free set only; no vendored
GetLayers content (reference only — licence bars
scraping/redistribution/resale); a layer is a foundation, not a
finished brand (restyle, never ship trial layers unchanged).

Edits (staged sources only; they flow through the STEP 2 copy):
  R1. new-skills/orchestrate/SKILL.md + new-rules/hackathon-mode.mdc
      (DESIGNPKG-AUTO, byte-identical — the identical insertions keep
      them byte-identical): getlayers moves to the FRONT of the palette
      source list; a priority sentence follows the getlayers gloss; a
      citation sentence follows the palette-attribution audit sentence.
  R2. new-skills/design-taste-frontend/SKILL.md (palette-first
      paragraph): getlayers is named FIRST among the sources, with
      priority language; getlayers leaves the design-package
      parenthetical (it is named before it); the same citation sentence
      follows the audit sentence.
  R3. new-skills/orchestrate/SKILL.md (inventory paragraph): the fix
      #31 additions mention carries the consulted-FIRST weight.
  R4. new-skills/orchestrate/references/design-inventory.md (§12):
      the GetLayers row's Reach-for-it cell leads with "Consulted
      FIRST" + the citation rule; the §12 intro names GetLayers'
      first-class weight.
  R5. new-skills/getlayers/SKILL.md: priority language in the framing
      header + a "Priority in the palette-first flow" section.
      (Applied by the coordinator with an edit, not here — the skill
      file is short and the edit is exact.)

Every substitution asserts its anchor occurs EXACTLY once and the
script writes nothing on any failure.
"""
import os
import sys

ROOT = os.path.expanduser("~/workspace/hackathon-plugin")
ERRORS = []
CHANGES = []


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sub_once(text, old, new, where):
    n = text.count(old)
    if n != 1:
        ERRORS.append(f"{where}: anchor occurs {n} times, expected 1 :: {old[:70]!r}")
        return text
    CHANGES.append(f"{where}: substituted :: {old[:50]!r} ...")
    return text.replace(old, new)


PRIORITY_SENTENCE = (
    " GetLayers prompts are consulted FIRST in the palette inventory — the "
    "first-class foundation the direction leans on: the design-lead reads "
    "the live GetLayers library before the other palette sources, and the "
    "direction names the GetLayers layers used or considered-and-rejected, "
    "each with a fix #19 D19 reason.")
CITATION_SENTENCE = (
    " GetLayers layers are cited the same way as every inventory entry — "
    "USED or CONSIDERED-AND-REJECTED, each with a D19 reason; a direction "
    "that names no GetLayers layer at all (neither used nor "
    "considered-and-rejected, nor `not considered — <reason>`) is a finding.")

# ---------------------------------------------------------------- R1 (both DESIGNPKG-AUTO files, identical)
for rel in ("new-skills/orchestrate/SKILL.md", "new-rules/hackathon-mode.mdc"):
    t = read(rel)
    t = sub_once(
        t,
        "(`motionsites-web-builder`, `getlayers`, `gsap`, `react-bits`, "
        "`hairline-create`, `hairline-adopt`, `ui-ux-pro-max`, `less-flat-ui`, "
        "`motion-foundations`, `motion-patterns`, `motion-advanced`, "
        "`make-interfaces-feel-better`, `design-system`, the dealt Hallmark theme)",
        "(`getlayers`, `motionsites-web-builder`, `gsap`, `react-bits`, "
        "`hairline-create`, `hairline-adopt`, `ui-ux-pro-max`, `less-flat-ui`, "
        "`motion-foundations`, `motion-patterns`, `motion-advanced`, "
        "`make-interfaces-feel-better`, `design-system`, the dealt Hallmark theme)",
        rel + " R1 palette order")
    t = sub_once(
        t,
        "restyled, never shipped unchanged) (fix #31, GETLAYERS_F31).",
        "restyled, never shipped unchanged) (fix #31, GETLAYERS_F31)." +
        PRIORITY_SENTENCE,
        rel + " R1 priority sentence")
    t = sub_once(
        t,
        "The audit checks the design-direction record names the palette "
        "components used (sources + components + tailoring); a direction "
        "with no palette attribution is a finding.",
        "The audit checks the design-direction record names the palette "
        "components used (sources + components + tailoring); a direction "
        "with no palette attribution is a finding." + CITATION_SENTENCE,
        rel + " R1 citation sentence")
    if not ERRORS:
        write(rel, t)

# ---------------------------------------------------------------- R2
rel = "new-skills/design-taste-frontend/SKILL.md"
t = read(rel)
t = sub_once(
    t,
    "read the available component/design sources — `motionsites-web-builder` "
    "(cinematic components, motion patterns, hero treatments, media; free "
    "sample only, fetched from upstream at use time; consulted, never a "
    "template), the design package (`ui-ux-pro-max`, `less-flat-ui`, "
    "`motion-foundations`, `motion-patterns`, `motion-advanced`, "
    "`make-interfaces-feel-better`, `design-system`, `getlayers`, `gsap`, "
    "`react-bits`, `hairline-create`, `hairline-adopt`), and the dealt "
    "Hallmark theme (the starting point, not a cage)",
    "read the available component/design sources — `getlayers` FIRST "
    "(prompt-first cinematic layers; the first-class foundation the direction "
    "leans on — consult its prompts before the other palette sources), then "
    "`motionsites-web-builder` (cinematic components, motion patterns, hero "
    "treatments, media; free sample only, fetched from upstream at use time; "
    "consulted, never a template), the design package (`ui-ux-pro-max`, "
    "`less-flat-ui`, `motion-foundations`, `motion-patterns`, `motion-advanced`, "
    "`make-interfaces-feel-better`, `design-system`, `gsap`, `react-bits`, "
    "`hairline-create`, `hairline-adopt`), and the dealt Hallmark theme "
    "(the starting point, not a cage)",
    rel + " R2 palette order")
t = sub_once(
    t,
    "The audit checks the design-direction record names the palette "
    "components used (sources + components + tailoring); a direction "
    "with no palette attribution is a finding.",
    "The audit checks the design-direction record names the palette "
    "components used (sources + components + tailoring); a direction "
    "with no palette attribution is a finding." + CITATION_SENTENCE,
    rel + " R2 citation sentence")
if not ERRORS:
    write(rel, t)

# ---------------------------------------------------------------- R3
rel = "new-skills/orchestrate/SKILL.md"
t = read(rel)
t = sub_once(
    t,
    "the fix #31 additions (GetLayers prompt-first layers, GSAP animation, "
    "React Bits components, Hairline illustrations — see §12 of the inventory)",
    "the fix #31 additions (GetLayers prompt-first layers — consulted FIRST "
    "in the palette inventory, the first-class foundation — GSAP animation, "
    "React Bits components, Hairline illustrations — see §12 of the inventory)",
    rel + " R3 inventory paragraph weight")
if not ERRORS:
    write(rel, t)

# ---------------------------------------------------------------- R4
rel = "new-skills/orchestrate/references/design-inventory.md"
t = read(rel)
t = sub_once(
    t,
    "All four resources are free-tier only; no paid plan is purchased for any of\n"
    "them. Counts for GetLayers and React Bits drift weekly — this file freezes\n"
    "no count for either; read the live library when you need the current numbers.",
    "All four resources are free-tier only; no paid plan is purchased for any of\n"
    "them. Counts for GetLayers and React Bits drift weekly — this file freezes\n"
    "no count for either; read the live library when you need the current numbers.\n"
    "GetLayers prompts carry the most weight in the palette-first flow — they are\n"
    "consulted FIRST, before the other palette sources, and the direction leans on\n"
    "them heavily as its foundation (see the skill).",
    rel + " R4 §12 intro weight")
t = sub_once(
    t,
    "A cinematic hero, animated ground, real-time 3D scene, or gradient ground on a marketing surface; a section whose motion is already designed. Never app UI; never a mismatched layer forced onto a surface",
    "Consulted FIRST in the palette inventory — the first-class foundation the direction leans on. A cinematic hero, animated ground, real-time 3D scene, or gradient ground on a marketing surface; a section whose motion is already designed. Never app UI; never a mismatched layer forced onto a surface. The direction cites the layers USED or CONSIDERED-AND-REJECTED, each with a D19 reason",
    rel + " R4 §12 GetLayers row weight")
if not ERRORS:
    write(rel, t)

if ERRORS:
    print("RE-WEAVE FAILED — nothing was written for the failed files:")
    for e in ERRORS:
        print("  ERROR: " + e)
    sys.exit(1)
print("RE-WEAVE OK:")
for c in CHANGES:
    print("  " + c)
