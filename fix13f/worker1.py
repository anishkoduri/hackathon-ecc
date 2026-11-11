#!/usr/bin/env python3
"""Fix round #13f, worker 1: single-executor rewording + render-tier scope guard.

Applies exact-string replacements to STAGED sources only (never the built
tree, never build.sh). Fails loudly if any old string is not found exactly
once. Run once from ~/workspace/hackathon-plugin:
    python3 fix13f/worker1.py
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # ~/workspace/hackathon-plugin

TASTE = BASE / "new-skills/design-taste-frontend"
POLISH = BASE / "round2-skills/polish-pass"

# (path, old, new, label)
EDITS = [
    # --- B1: Taste SKILL.md:52 (built :53) — captivating-hero bar ---
    (TASTE / "SKILL.md",
     "if they cannot, the hero fails even if every other check passes.",
     "if they cannot, the hero falls short of this bar \u2014 record that as candidate evidence for `browser-qa`, whose visual-loop verdict alone decides whether the hero passes the distinctiveness bar, even if every other check passes.",
     "B1 hero bar"),
    # --- Sweep M1: Taste SKILL.md:282 (built :283) — check.mjs findings ---
    (TASTE / "SKILL.md",
     "Every `check.mjs` finding fails the page (no `--no-stress`).",
     "Every `check.mjs` finding fails the page on layout-correctness grounds (no `--no-stress`); a layout finding is not a distinctiveness verdict \u2014 that is `browser-qa`'s alone.",
     "M1 Taste SKILL check.mjs"),
    # --- Sweep M1: layout-v4.md:296 ---
    (TASTE / "references/layout-v4.md",
     "Run it without `--no-stress`; every finding fails the page.",
     "Run it without `--no-stress`; every finding fails the page on layout-correctness grounds, not as a distinctiveness verdict.",
     "M1 layout-v4 check.mjs"),
    # --- Sweep M2: layout-v4.md:182-186 — hero fail list ---
    (TASTE / "references/layout-v4.md",
     "A hero fails with a picture out to one viewport edge, a hero taller than the screen, the visual\nabove the text on a phone, words over the busy part of a picture, a second float card, a slogan, a\ncaption under the picture.",
     "A hero with a picture out to one viewport edge, a hero taller than the screen, the visual above the text on a phone, words over the busy part of a picture, a second float card, a slogan, or a caption under the picture is candidate evidence of a weak hero for `browser-qa` to weigh, not a fail verdict on its own.",
     "M2 layout-v4 hero"),
    # --- B2: gates.md table row gate 8 (:95) ---
    (TASTE / "references/hallmark/references/gates.md",
     "| 8 | Reflex | J | The AI template (hero, three features, call to action, footer), or the same shape as one of the last three logged builds |",
     "| 8 | Reflex | J | The familiar AI shape (hero, three features, call to action, footer), or the same shape as one of the last three logged builds |",
     "B2 gates.md:95 gate 8 row"),
    # --- B2: gates.md table row gate 83 (:117) ---
    (TASTE / "references/hallmark/references/gates.md",
     "so it reads as a stock gallery. Guard:",
     "which is candidate evidence of a stock-gallery look for `browser-qa` to weigh. Guard:",
     "B2 gates.md:117 gate 83 row"),
    # --- B2: gates.md table row gate 85 (:119) ---
    (TASTE / "references/hallmark/references/gates.md",
     "| 85 | Reflex | R | The stock close: the last section before the footer, or the footer, is an email sign-up",
     "| 85 | Reflex | R | The email-sign-up close: the last section before the footer, or the footer, is an email sign-up",
     "B2 gates.md:119 gate 85 row"),
    # --- Sweep M7 (= 6b clause, gates.md:189) ---
    (TASTE / "references/hallmark/references/gates.md",
     "four things stacked on the centre line is a default.",
     "four things stacked on the centre line is candidate evidence of a default composition for `browser-qa` to weigh.",
     "M7 gates.md:189 6b"),
    # --- B2: gates.md:191 gate 8 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "The same composition twice in a row on one page is the template; across pages, a different order or a different lead composition is enough.",
     "The same composition twice in a row on one page is candidate evidence of repetition for `browser-qa` to weigh; across pages, a different order or a different lead composition is enough.",
     "B2 gates.md:191 gate 8"),
    # --- B2: gates.md:193 gate 9 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "A page that climbs the same rung at every seam reads as a template; one that climbs different rungs in different places reads as set.",
     "A page that climbs the same rung at every seam is candidate evidence of a templated rhythm for `browser-qa` to weigh; one that climbs different rungs in different places reads as set.",
     "B2 gates.md:193 gate 9"),
    # --- Sweep M3: gates.md:199 gate 23 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "undeclared sprawl still fails.",
     "undeclared sprawl is still flagged at the craft level (accent footprint above the declared-posture budget), as evidence for `browser-qa` to weigh \u2014 not a template verdict.",
     "M3 gates.md:199 gate 23"),
    # --- B2: gates.md:233 gates 80-82 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "Each reads as generated at a glance.",
     "Each is candidate evidence of a generated look, for `browser-qa` to weigh at a glance.",
     "B2 gates.md:233 gates 80-82"),
    # --- B2: gates.md:235 gate 83 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "The opposite failure: a page that is all photographs, one after another, reads as a stock gallery, and the theme never gets to speak.",
     "The opposite failure: a page that is all photographs, one after another, is candidate evidence of a stock-gallery look for `browser-qa` to weigh, and the theme never gets to speak.",
     "B2 gates.md:235 gate 83"),
    # --- B2: gates.md:239 gate 85 judged clause ---
    (TASTE / "references/hallmark/references/gates.md",
     "and could this exact sequence of sections sit under a different business's name? If it could, the page has no anatomy of its own yet.",
     "and could this exact sequence of sections sit under a different business's name? If it could, that is candidate evidence the page has no anatomy of its own yet, for `browser-qa` to weigh.",
     "B2 gates.md:239 gate 85"),
    # --- Sweep M6: redesign.md:40 ---
    (TASTE / "references/hallmark/references/redesign.md",
     "what reads as generated (the worst tells, by gate)",
     "what suggests a generated look (the strongest candidate evidence, by gate)",
     "M6 redesign.md:40"),
    # --- B3: sloplint-render.mjs header scope note (mirrors sloplint.mjs:2) ---
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "#!/usr/bin/env node\nimport { existsSync, mkdirSync, writeFileSync } from 'node:fs';",
     "#!/usr/bin/env node\n/* sloplint-render: Hallmark's render-tier gate checker (rendered-page checks in a real browser). Its FAIL/REFLEX/WARN grades are render-check grades, not pass/fail verdicts on rendered screens \u2014 screen distinctiveness is judged only by `browser-qa` in the visual loop. Template gates (80, 81, 82, 83, 85) never issue REFLEX verdicts here: on landing pages they emit NOTE candidate evidence for `browser-qa`; on app screens they are skipped (mirroring sloplint.mjs APP_SKIP). */\nimport { existsSync, mkdirSync, writeFileSync } from 'node:fs';",
     "B3 render header note"),
    # --- B3: thread meta.scope into observeSpace at the call site (:201) ---
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "const res = await page.evaluate(observeSpace, w === 1440, heroOnly, meta.heroPostureByFile[file] || '', !!meta.photoShapeByFile[file], meta.jobByFile[file] || '');",
     "const res = await page.evaluate(observeSpace, w === 1440, heroOnly, meta.heroPostureByFile[file] || '', !!meta.photoShapeByFile[file], meta.jobByFile[file] || '', meta.scope);",
     "B3 render call site scope"),
    # --- B3: scope guard inside observeSpace (:739) ---
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "function observeSpace(atLaptop, heroOnly, heroPosture, photoShape, job) {\n  const freeFold = /^(poster|ledge|banner|custom)$/.test(heroPosture || '');",
     "function observeSpace(atLaptop, heroOnly, heroPosture, photoShape, job, scope) {\n  // Template gates (80, 81, 82, 83, 85) never issue REFLEX verdicts here: they\n  // are candidate evidence for browser-qa, not a verdict. On app screens they\n  // are skipped outright (mirroring sloplint.mjs APP_SKIP); on landing pages\n  // they emit a NOTE, which sloplint.mjs counts as a note and never enforces\n  // as FAIL or REFLEX. (The render tier grades no gates 8/9, so there is\n  // nothing further to guard.)\n  const isAppScope = scope === 'app';\n  const templateEvidence = (gate, evidence, fix) => { if (!isAppScope) push(gate, 'NOTE', `${evidence} \u2014 candidate evidence for browser-qa`, fix); };\n  const freeFold = /^(poster|ledge|banner|custom)$/.test(heroPosture || '');",
     "B3 render observeSpace guard"),
    # --- Sweep M3: sloplint-render.mjs:680 gate 23 FAIL evidence (grade kept: craft check) ---
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "push(23, 'FAIL', `accent paints ~${pct.toFixed(1)}% of the 1280x800 viewport (> ${failAt}%)`,",
     "push(23, 'FAIL', `accent paints ~${pct.toFixed(1)}% of the 1280x800 viewport (> ${failAt}%) \u2014 craft-level accent footprint above the declared-posture budget`,",
     "M3 render gate 23 evidence"),
    # --- B3: template gates 80/81/82/83/85: REFLEX -> templateEvidence (NOTE / skip) ---
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "if (drawn.length) push(80, 'REFLEX', ",
     "if (drawn.length) templateEvidence(80, ",
     "B3 render gate 80"),
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "if (empty.length) push(81, 'REFLEX', ",
     "if (empty.length) templateEvidence(81, ",
     "B3 render gate 81"),
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "if (marks.length) push(82, 'REFLEX', ",
     "if (marks.length) templateEvidence(82, ",
     "B3 render gate 82"),
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "if (share > (photoShape ? 0.45 : 0.36) && n >= 3) push(83, 'REFLEX', ",
     "if (share > (photoShape ? 0.45 : 0.36) && n >= 3) templateEvidence(83, ",
     "B3 render gate 83"),
    (TASTE / "references/hallmark/scripts/sloplint-render.mjs",
     "if (hit) push(85, 'REFLEX', ",
     "if (hit) templateEvidence(85, ",
     "B3 render gate 85"),
    # --- B4: impeccable-critique.md:56 Assessment A design-specificity bullet ---
    (POLISH / "reference/impeccable-critique.md",
     "Make this judgment before seeing detector output.",
     "Record this assessment as candidate evidence for `browser-qa` to weigh \u2014 never a verdict \u2014 before seeing detector output.",
     "B4 critique :56"),
    # --- B4: impeccable-critique.md:62 return line ---
    (POLISH / "reference/impeccable-critique.md",
     "Return: design-specificity verdict, heuristic scores,",
     "Return: design-specificity assessment (candidate evidence for `browser-qa`, not a verdict), heuristic scores,",
     "B4 critique :62"),
    # --- B4: impeccable-critique.md:140 heading + framing sentence ---
    (POLISH / "reference/impeccable-critique.md",
     "#### Design Specificity Verdict\n\n**Start here.** Does the result feel authored for this product, or category-interchangeable?",
     "#### Design Specificity Assessment\n\nRecord the outcome as candidate evidence for `browser-qa`'s visual-loop verdict, not as a verdict: the assessment informs the Priority fixes, but only `browser-qa`'s verdict can establish a generic-template finding.\n\n**Start here.** Does the result feel authored for this product, or category-interchangeable?",
     "B4 critique :140"),
    # --- Sweep M4: polish-pass SKILL.md:24 (staged text; built differs only in the trailing clause) ---
    (POLISH / "SKILL.md",
     "If the diagnosis shows the look itself is the problem \u2014 the UI is a generic template, the palette needs re-picking, the structure needs rethinking \u2014 do not restyle it here.",
     "If the evidence suggests the look itself is the problem \u2014 the UI looks like a generic template, the palette needs re-picking, the structure needs rethinking \u2014 do not restyle it here.",
     "M4 polish SKILL.md:24"),
    # --- Sweep M4: polish.md:20 ---
    (POLISH / "reference/polish.md",
     "A generic-template diagnosis (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is appended",
     "A generic-template observation (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is appended",
     "M4 polish.md:20"),
]


def main() -> int:
    failed = []
    for path, old, new, label in EDITS:
        text = path.read_text(encoding="utf-8")
        n = text.count(old)
        if n != 1:
            print(f"FAIL [{label}]: old string found {n}x in {path}")
            failed.append(label)
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        print(f"ok   [{label}]")
    if failed:
        print(f"\n{len(failed)} edit(s) FAILED: {failed}")
        return 1
    print(f"\nAll {len(EDITS)} edits applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
