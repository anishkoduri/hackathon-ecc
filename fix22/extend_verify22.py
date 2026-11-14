#!/usr/bin/env python3
"""Insert the §13-§17 check sections into fix22/verify22.py.

Run once by the coordinator. Inserts new sections 13-17 before the
existing "# 13. Dedupe" comment, renumbers existing sections 13-17 to
18-22, and updates the docstring's numbered list. Idempotent: refuses
to run twice (checks for the §13 marker first).
"""
import os
import sys

FIX22 = os.path.expanduser("~/workspace/hackathon-plugin/fix22")
PATH = os.path.join(FIX22, "verify22.py")
text = open(PATH, encoding="utf-8").read()

if "# 13. Depth (§13)" in text:
    print("verify22.py already has the §13-§17 sections; nothing to do.")
    sys.exit(0)

NEW = '''
# 13. Depth (§13) — the z-axis as a seventh D19 dimension.
ds = read("skills/design-system/SKILL.md")
vercel = read("skills/polish-pass/reference/vercel-checklist.md")
orbs_report = open(os.path.join(PLUGIN, "fix22/orbs-patches.md"),
                   encoding="utf-8").read()
dedupe_vercel = open(os.path.join(PLUGIN, "fix22/vercel-dedupe.md"),
                     encoding="utf-8").read()
lib15_report = open(os.path.join(PLUGIN, "fix22/libraries15-patches.md"),
                    encoding="utf-8").read()
check("depth strategy in every UI slice brief (DEPTH-01, DEPTH_F22)",
      "Depth strategy in every UI slice brief (fix #22 §13, DEPTH_F22)" in orch)
check("flat by choice recorded as an explicit depth strategy",
      "flat by choice — <reason>" in orch)
check("D19 seventh-dimension extension line in orchestrate + Taste (DEPTH-02/03)",
      "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in orch
      and "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in taste)
check("D19 rule text itself unchanged (tail sentence still verbatim)",
      "The check verifies the reasoning is PRESENT and addresses the dimensions" in orch
      and "The check verifies the reasoning is PRESENT and addresses the dimensions" in taste)
check("depth as a dealt moment in Taste (DEPTH-04)",
      "Depth as a dealt moment / theme element (fix #22 §13, DEPTH_F22)" in taste)
check("depth strategy recorded with the direction (DEPTH-05/06)",
      "Depth strategy recorded with the direction (fix #22 §13, DEPTH_F22)" in orch
      and "depth strategy per surface (fix #22 §13, DEPTH_F22)" in orch)
check("depth check wired into polish-pass step 5 (DEPTH-07)",
      "Then run the depth check" in polish)
check("depth check section in the slop checklist (DEPTH-08, D1-D6)",
      "## Depth check — the z-axis (fix #22 §13, DEPTH_F22)" in slop
      and "D1 — A depth strategy is named for every surface" in slop
      and "D6 — The Depth dimension is recorded" in slop)
check("depth tokens in motion-foundations (DEPTH-09, DEPTH_F22)",
      "### Depth tokens — 3D motion values (fix #22 §13, DEPTH_F22)" in mf
      and "perspective: 1000" in mf
      and "parallax: { near: 0.5, mid: 0.25, far: 0.1 }" in mf
      and "tilt: { max: 6 }" in mf
      and "elevation: { raised: 8, floating: 16, modal: 24 }" in mf)
check("parallax layers + 3D-transform hero in motion-patterns (DEPTH-10)",
      "### Parallax layers and 3D-transform hero (fix #22 §13, DEPTH_F22)" in mp)
check("depth rules in ui-ux-pro-max (DEPTH-11, DEPTH_F22)",
      "**Depth rules — the z-axis on app surfaces (fix #22 §13, DEPTH_F22).**" in uipro
      and "Elevation system" in uipro
      and "scrim and a 4.5:1 contrast check" in uipro)
check("D19 seventh-dimension mirror in ui-ux-pro-max (DEPTH-12)",
      "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in uipro)
check("texture/depth overlap note in less-flat-ui (DEPTH-13)",
      "**Depth and texture are different axes (fix #22 §13, DEPTH_F22).**" in lessflat
      and "Soft Shadow #23 is BOTH" in lessflat)
check("DEPTH_F22 token in build.sh (fix22 block)",
      "DEPTH_F22" in build)

# 14. Thinking Orbs (§14) — state-matched loading indicator.
for _st in ("working", "searching", "solving", "listening", "connecting",
            "weaving", "composing", "breathing", "shaping"):
    check(f"orb state `{_st}` in the motion-patterns state table",
          f"| `{_st}` |" in mp)
check("orb pattern in motion-patterns (ORB-MP, ORBS_F22)",
      "### Thinking Orb — the loading indicator for AI/agent waiting states (fix #22 §14, ORBS_F22)" in mp)
check("no state named thinking (SPEC mapping corrected)",
      "There is no `thinking` state in the library" in mp)
check("generic spinner FAILS for an AI/agent wait (fixture a)",
      "a generic spinner" in mp and "FAILS" in mp)
check("orb tokens in motion-foundations (ORB-MF, ORBS_F22)",
      "### Thinking Orb tokens (fix #22 §14, ORBS_F22)" in mf
      and "ONE static representative" in mf
      and "DPR is capped at 2" in mf)
check("orb component in ui-ux-pro-max (ORB-UIPRO, ORBS_F22)",
      "**Thinking Orb — the loading indicator component for AI/agent waiting states (fix #22 §14, ORBS_F22).**" in uipro)
check("orb pin thinking-orbs@0.3.2 + MIT + React >= 18",
      "thinking-orbs@0.3.2" in uipro and "License MIT" in uipro
      and "React >= 18" in uipro)
check("orb stack scope: React Native install-from-repo-gated, SwiftUI planned only",
      "NOT published on npm" in uipro and "SwiftUI: PLANNED only" in uipro)
check("waiting states in the design package (ORB-ORCH, ORBS_F22)",
      "Waiting states in every UI slice brief (fix #22 §14, ORBS_F22)" in orch)
check("orb check in the slop checklist (ORB-PP1, ORBS_F22)",
      "## Thinking Orb check — ORBS_F22 (fix #22 §14, polish-pass portion)" in slop
      and "a mismatched orb state" in slop)
check("orb as the D19 loading-state implementation (ORB-PP2, ORBS_F22)",
      "the approved implementation of this fix is the" in unslop
      and "Thinking Orb (`motion-patterns`, ORBS_F22)" in unslop)
check("ORBS_F22 token in build.sh (fix22 block)",
      "ORBS_F22" in build)
check("rareformlabs connection unresolved — recorded, not invented",
      "rareformlabs connection unresolved — asset verified independently" in orbs_report)

# 15. Libraries §15 — R3F / liquid-glass-js / ShaderGradient / liquid-logo.
check("R3F in motion-foundations + motion-patterns + ui-ux-pro-max + Taste (R3F_F22)",
      "R3F_F22" in mf and "R3F_F22" in mp and "R3F_F22" in uipro
      and "R3F_F22" in taste)
check("R3F pins @9.8.2 (React 19) / @8.18.0 (React 18), MIT",
      "@react-three/fiber@9.8.2" in mf and "@react-three/fiber@8.18.0" in mf
      and "MIT" in mf)
check("R3F strict version pairing: React 18 + v9 FAILS, React 19 + v8 FAILS",
      "React 18 + R3F v9 FAILS the pairing check" in mf
      and "React 19 + R3F v8 FAILS the pairing check" in mf)
check("liquid-glass-js in ui-ux-pro-max + Taste + less-flat-ui (LIQGLASS_F22)",
      "LIQGLASS_F22" in uipro and "LIQGLASS_F22" in taste
      and "LIQGLASS_F22" in lessflat)
check("liquid-glass-js pin commit 78cb6ccb + MIT + no npm package (copy files)",
      "78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a" in uipro
      and "NO npm package" in uipro
      and "container.js" in lessflat and "button.js" in lessflat
      and "glass.css" in lessflat)
check("liquid-glass-js html2canvas perf note + frosted-blur fallback",
      "html2canvas@1.4.1" in lessflat and "frosted blur" in lessflat)
check("ShaderGradient in ui-ux-pro-max + Taste (SHADERGRAD_F22)",
      "SHADERGRAD_F22" in uipro and "SHADERGRAD_F22" in taste)
check("ShaderGradient @2.4.20 ESM-only + MIT-declared-no-LICENSE caveat",
      "@shadergradient/react@2.4.20" in uipro
      and "NO root LICENSE file" in uipro)
check("ShaderGradient v2, NOT legacy v1.3.5",
      "NOT legacy" in uipro and "v1.3.5" in uipro)
check("liquid-logo in ui-ux-pro-max + Taste (LIQLOGO_F22)",
      "LIQLOGO_F22" in uipro and "LIQLOGO_F22" in taste)
check("liquid-logo pin commit 689bb38a + PolyForm Shield + standalone tool",
      "689bb38a1e0d5a6a8baf2d34847635eefde19994" in uipro
      and "PolyForm Shield 1.0.0" in uipro
      and "STANDALONE TOOL" in uipro)
check("liquid-logo static fallback + paper-design attribution",
      "static logo" in uipro and "paper-design attribution" in taste)
check("one-WebGL-heavy-effect-per-surface rule (WEBGL_ONE_F22)",
      "One WebGL-heavy effect per surface (WEBGL_ONE_F22)" in uipro
      and "## One WebGL-heavy effect per surface — WEBGL_ONE_F22 (fix #22 §15)" in slop)
check("liquid-glass-design dangling reference resolved (option b): 0 in built skill text",
      "liquid-glass-design" not in subprocess.run(
          ["grep", "-r", "liquid-glass-design", "skills", "--exclude-dir=node_modules"],
          cwd=BASE, capture_output=True, text=True).stdout
      and "liquid-glass-design" in lib15_report
      and "option (b), corrected" in lib15_report)
check("§15 tokens in build.sh (fix22 block)",
      "R3F_F22" in build and "LIQGLASS_F22" in build
      and "SHADERGRAD_F22" in build and "LIQLOGO_F22" in build
      and "WEBGL_ONE_F22" in build)

# 16. Vercel web-design-guidelines (§16) — pinned snapshot, never live fetch.
check("Vercel checklist file exists in the built tree (VERCEL_F22)",
      os.path.isfile(os.path.join(BASE, "skills/polish-pass/reference/vercel-checklist.md"))
      and "VERCEL_F22" in vercel)
check("Vercel pinned snapshot: commit 4ecfb9fb + date 2026-10-05",
      "4ecfb9fb8d1d3b7009674869b3aaee2f904042e1" in vercel
      and "2026-10-05" in vercel)
check("Vercel checklist wired into polish-pass (VERCEL-02/03)",
      "Also read the Vercel checklist" in polish
      and "Then run the Vercel checklist" in polish)
check("Vercel pointers in quick-reference + motion-foundations (VERCEL-04..07)",
      "vercel-a11y-check" in qr and "vercel-touch-check" in qr
      and "vercel-type-check" in qr
      and "pinned Vercel checklist (VERCEL_F22)" in mf)
check("live-fetch instruction ABSENT: no raw.githubusercontent URL in the checklist",
      "raw.githubusercontent.com" not in vercel)
check("live-fetch ABSENT from the built tree (no unpinned Vercel fetch URL)",
      "raw.githubusercontent.com/vercel-labs" not in subprocess.run(
          ["grep", "-r", "raw.githubusercontent.com/vercel-labs",
           "skills", "agents", "commands", "rules", "hooks",
           "--exclude-dir=node_modules"],
          cwd=BASE, capture_output=True, text=True).stdout)
check("Vercel license gap recorded (rules MIT, skill repo NO LICENSE)",
      "MIT (© 2025 Vercel Labs" in vercel and "has NO LICENSE" in vercel)
check("ECC-source check recorded (snapshot NOT in-source at the plugin pin)",
      "does NOT carry the skill" in vercel)
check("Vercel dedupe table accounts for all 136 rows, zero unaccounted",
      "136 rows accounted for, zero" in dedupe_vercel)
check("Vercel AG19 conflict recorded (APCA vs WCAG 4.5:1, parent adjudication)",
      "AG19" in dedupe_vercel)
check("VERCEL_F22 token in build.sh (fix22 block)",
      "VERCEL_F22" in build)

# 17. Libraries §17 — Casberry / OriginKit / daisyUI.
check("Casberry in motion-foundations + motion-patterns + ui-ux-pro-max + Taste + slop (CASBERRY_F22)",
      "CASBERRY_F22" in mf and "CASBERRY_F22" in mp
      and "CASBERRY_F22" in uipro and "CASBERRY_F22" in taste
      and "CASBERRY_F22" in slop)
check("Casberry standalone tool + terms unresolved + trust flag + export review",
      "STANDALONE TOOL" in mf and "terms / licence are UNRESOLVED" in mf
      and "ScamAdviser 1/100" in mf and "UNTRUSTED code" in mf)
check("Casberry export-review check in the slop checklist (L17-07)",
      "## Exported code is reviewed before it enters the build — Casberry (CASBERRY_F22, fix #22 §17)" in slop)
check("one-WebGL rule extended to Casberry exports (L17-06 replace)",
      "a Casberry particle export" in slop)
check("OriginKit in motion-patterns + ui-ux-pro-max + Taste (ORIGINKIT_F22)",
      "ORIGINKIT_F22" in mp and "ORIGINKIT_F22" in uipro
      and "ORIGINKIT_F22" in taste)
check("OriginKit 10/day cap + Pro exclusion + conditional licence",
      "10 component fetches per key per day" in mp
      and "never pays for Pro" in mp and "CONDITIONAL" in mp)
check("OriginKit is NOT Origin UI (distinction check)",
      "is NOT Origin UI" in mp)
check("OriginKit deduped vs React Bits (catalog vs importable library)",
      "Reach for React Bits" in mp)
check("daisyUI in ui-ux-pro-max + design-system + Taste (DAISYUI_F22)",
      "DAISYUI_F22" in uipro and "DAISYUI_F22" in ds
      and "DAISYUI_F22" in taste)
check("daisyUI pin 5.7.50 + MIT + Tailwind v4 pairing",
      "daisyui@5.7.50" in ds and "MIT" in ds
      and "Tailwind CSS v4" in ds)
check("daisyUI default theme unexamined FAILS + shadcn dedupe",
      "default theme unexamined FAILS" in ds and "shadcn" in ds)
check("running total of asset libraries/tools in fix #22 is 11",
      "§11's 4 + §15's 4 + §17's 3 = 11" in uipro)
check("§17 tokens in build.sh (fix22 block)",
      "CASBERRY_F22" in build and "ORIGINKIT_F22" in build
      and "DAISYUI_F22" in build)

'''

# Insert before the existing "# 13. Dedupe" section.
marker = "# 13. Dedupe (§5) — one concept, one primary home."
assert text.count(marker) == 1, "dedupe marker not found exactly once"
text = text.replace(marker, NEW + marker, 1)

# Renumber the existing sections 13-17 -> 18-22.
for old, new in (("# 13. Dedupe", "# 18. Dedupe"),
                 ("# 14. Counts", "# 19. Counts"),
                 ("# 15. No banned terms", "# 20. No banned terms"),
                 ("# 16. build.sh", "# 21. build.sh"),
                 ("# 17. Previous verifiers", "# 22. Previous verifiers")):
    assert text.count(old) == 1, "section marker %r not found once" % old
    text = text.replace(old, new, 1)

# Docstring: insert the new items after item 12 (Bang) and renumber.
old_doc = """ 13. Dedupe (§5): the pairs resolve to a single primary home.
 14. Every placed item is named in its target skill in the built tree AND
     in build.sh (fix22 block).
 15. Counts unchanged post-fix21: 166/72/123/87/15; trigger keys 64.
 16. No banned terms in the built tree (excl. node_modules).
 17. build.sh is the post-fix22 file (fix22 block + BANG_PIN + all earlier
     markers; more lines than post-fix21, 23,647).
 18. verify15/17/18/19/20/21 still pass (subprocesses, exit 0 required)."""
new_doc = """ 13. Depth (§13): depth strategy per surface, Depth as the seventh D19
     dimension (extension line, D19_RULE untouched), depth tokens, depth
     rules, depth check; DEPTH_F22 in every placement + build.sh.
 14. Thinking Orbs (§14): nine verified states (no "thinking" state),
     orb tokens + component + pin 0.3.2 + MIT, waiting states, orb check;
     rareformlabs connection unresolved, recorded not invented.
 15. Libraries (§15): R3F + liquid-glass-js + ShaderGradient + liquid-logo
     named in their placements with pins + licenses + stack scope; R3F
     pairing rule; ShaderGradient v2 not v1; liquid-logo standalone +
     fallback + attribution; one-WebGL rule; liquid-glass-design resolved
     (option b, corrected).
 16. Vercel (§16): pinned snapshot in polish-pass (commit + date), wired
     into the pass + pointers; live-fetch instruction ABSENT (grep);
     ECC-source check + license gap recorded; dedupe 136 rows, AG19
     conflict recorded.
 17. Libraries (§17): Casberry + OriginKit + daisyUI named in their
     placements with pins/terms/caps; Casberry terms unresolved + trust
     flag + export review; OriginKit 10/day cap + Origin UI distinction;
     daisyUI 5.7.50 + Tailwind v4 + default-theme FAIL; running total 11.
 18. Dedupe (§5): the pairs resolve to a single primary home.
 19. Every placed item is named in its target skill in the built tree AND
     in build.sh (fix22 block).
 20. Counts unchanged post-fix21: 166/72/123/87/15; trigger keys 64.
 21. No banned terms in the built tree (excl. node_modules).
 22. build.sh is the post-fix22 file (fix22 block + BANG_PIN + all earlier
     markers; more lines than post-fix21, 23,647).
 23. verify15/17/18/19/20/21 still pass (subprocesses, exit 0 required)."""
assert text.count(old_doc) == 1, "docstring block not found exactly once"
text = text.replace(old_doc, new_doc, 1)

open(PATH, "w", encoding="utf-8").write(text)
print("verify22.py extended: §13-§17 sections inserted, old sections "
      "renumbered 13-17 -> 18-22, docstring updated.")
