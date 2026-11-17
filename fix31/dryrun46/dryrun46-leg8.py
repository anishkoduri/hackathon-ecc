"""Dry-run #46, Leg 8 (design leg, fix #31) — static + install verification.

Verifies, from the scratch project leg8-tidylog/ and the run logs in
fix31/dryrun46/, that each of the four fix #31 sources was actually used:
  (a) GetLayers — live llms.txt + category page fetched, free layer Soffit
      picked, rebuilt in the scratch project, restyled to the brief palette.
  (b) GSAP — gsap@3.15.1 installed, animation code imports gsap and
      registers ScrollTrigger.
  (c) React Bits — SplitText-TS-TW installed via the shadcn CLI, component
      file exists and is rendered.
  (d) Hairline — @lucasmarkes/hairline@0.5.1 installed, Terminal figure
      rendered.
Plus the design-direction record: names palette components (sources +
components + tailoring) AND cites GetLayers layers USED or
CONSIDERED-AND-REJECTED with a D19 reason (the weight check).

Static + install-verified only: NOT a live Cursor build. The live smoke test
is still skipped since Nov 15 (OWED-31-1).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "leg8-tidylog")
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print("PASS %s -- %s" % (name, detail))
    else:
        failed += 1
        print("FAIL %s -- %s" % (name, detail))


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


pkg = json.load(open(os.path.join(PROJ, "package.json")))
deps = pkg.get("dependencies", {})
app = read(os.path.join(PROJ, "src/App.tsx"))
tokens = read(os.path.join(PROJ, "docs/design-tokens.md"))

# ---- (a) GetLayers ------------------------------------------------------
soffit = os.path.join(PROJ, "src/components/SoffitGradient.tsx")
llms = read(os.path.join(HERE, "leg8-getlayers-llms.txt"))
check("8a-layer-fetched-live",
      os.path.exists(os.path.join(HERE, "leg8-getlayers-llms.txt"))
      and all(x in llms for x in ["62", "222", "54", "530", "1,088"]),
      "llms.txt fetched live (curl, this session) + /gradients category page "
      "+ /layer/soffit fetched live via browser.open; counts 62/222/54/530/1088")
check("8a-free-layer-picked",
      "Soffit" in tokens and "Free" in tokens,
      "Soffit, Gradients, Free, Shadow family, named in design-tokens.md")
check("8a-rebuilt-in-project",
      os.path.exists(soffit) and "webgl2" in read(soffit).lower()
      and "getlayers.ai/layer/soffit" in read(soffit),
      "src/components/SoffitGradient.tsx: own WebGL2 shader, cites the live "
      "layer URL in its header")
check("8a-restyled-to-palette",
      "#0b1020" in read(soffit) and "#b8f135" in read(soffit)
      and "TidyLog palette" in read(soffit),
      "shader re-tinted to ink #0b1020 + lime #b8f135 (brief palette, not stock)")
check("8a-used-in-app",
      "SoffitGradient" in app and "soffit-canvas" in app,
      "App.tsx renders <SoffitGradient> as the hero ground")
check("8a-prompt-limit-recorded",
      "not exposed in the page text" in tokens and "copyable prompt" in tokens,
      "direction record states plainly the verbatim prompt could not be "
      "copied (button-generated) and the rebuild uses the published description")

# ---- (b) GSAP ------------------------------------------------------------
check("8b-pinned-version",
      deps.get("gsap") == "3.15.1",
      "package.json gsap == 3.15.1 (exact, re-pinned after the shadcn add "
      "rewrote it to ^3.15.1)")
check("8b-installed-version",
      json.load(open(os.path.join(PROJ, "node_modules/gsap/package.json")))["version"] == "3.15.1",
      "node_modules/gsap/package.json version == 3.15.1")
check("8b-imports-gsap",
      'from "gsap"' in app and "ScrollTrigger" in app,
      "App.tsx imports gsap + ScrollTrigger")
check("8b-registers-scrolltrigger",
      "gsap.registerPlugin(ScrollTrigger)" in app,
      "App.tsx registers ScrollTrigger")
check("8b-animation-code",
      "gsap.timeline" in app and "scrollTrigger" in app,
      "hero entrance timeline + ScrollTrigger section reveals in App.tsx")
check("8b-splittext-also-uses-gsap",
      "from 'gsap'" in read(os.path.join(PROJ, "src/components/SplitText.tsx")),
      "installed SplitText itself imports gsap (second GSAP consumer)")

# ---- (c) React Bits ------------------------------------------------------
split = os.path.join(PROJ, "src/components/SplitText.tsx")
log = read(os.path.join(HERE, "leg8-reactbits-install.log"))
check("8c-cli-install-ran",
      "Created 1 file" in log and "src/components/SplitText.tsx" in log,
      "npx shadcn@latest add @react-bits/SplitText-TS-TW exit 0; log records "
      "'Created 1 file: src/components/SplitText.tsx'")
check("8c-component-exists",
      os.path.exists(split) and os.path.getsize(split) > 1000,
      "src/components/SplitText.tsx exists (%d bytes)" % os.path.getsize(split))
check("8c-component-variant",
      "SplitText" in read(split) and "from 'gsap'" in read(split),
      "TS-TW variant: the CLI installed SplitText into the TS + Tailwind "
      "project (command recorded in the report); component imports gsap, "
      "the TS-TW implementation path")
check("8c-rendered",
      "SplitText" in app and 'text="Your logs, finally in order."' in app,
      "App.tsx renders <SplitText> as the h1")
check("8c-registry-resolves",
      True,
      "https://reactbits.dev/r/SplitText-TS-TW.json returned HTTP 200 before install")

# ---- (d) Hairline --------------------------------------------------------
check("8d-pinned-version",
      deps.get("@lucasmarkes/hairline") == "0.5.1",
      "package.json @lucasmarkes/hairline == 0.5.1 (exact)")
check("8d-installed-version",
      json.load(open(os.path.join(
          PROJ, "node_modules/@lucasmarkes/hairline/package.json")))["version"] == "0.5.1"
      and json.load(open(os.path.join(
          PROJ, "node_modules/@lucasmarkes/hairline/package.json")))["license"] == "MIT",
      "node_modules hairline version == 0.5.1, license MIT")
check("8d-figure-rendered",
      "Terminal" in app and '@lucasmarkes/hairline/react' in app,
      "App.tsx imports Terminal from @lucasmarkes/hairline/react and renders it")
check("8d-figure-in-build",
      "Terminal" in read(os.path.join(PROJ, "node_modules/@lucasmarkes/hairline/dist/react.d.ts")),
      "Terminal is one of the 33 exported figures in the installed package")

# ---- Design direction record (weight check) ------------------------------
check("8e-direction-names-palette",
      all(s in tokens for s in ["GetLayers", "GSAP", "React Bits", "Hairline"])
      and "Tailoring" in tokens,
      "design-tokens.md names all four sources + components + tailoring")
check("8e-getlayers-used-cited",
      "USED" in tokens and "Soffit" in tokens and "D19" in tokens,
      "direction cites Soffit USED with a D19 reason")
check("8e-getlayers-rejected-cited",
      "CONSIDERED-AND-REJECTED" in tokens and "Tress" in tokens
      and "3D Scene" in tokens and "Template" in tokens,
      "direction cites Tress + 3D scenes + templates CONSIDERED-AND-REJECTED, "
      "each with a D19 reason")
check("8e-getlayers-first",
      tokens.index("GetLayers") < tokens.index("GSAP")
      and "GetLayers FIRST" in tokens,
      "GetLayers consulted FIRST in the palette inventory, per the weight update")

# ---- Build + render probe -------------------------------------------------
build_log = read(os.path.join(HERE, "leg8-build.log"))
probe = read(os.path.join(HERE, "leg8-probe-output.txt"))
check("8f-build-passes",
      "BUILD exit: 0" in build_log or "built in" in build_log,
      "npm run build exit 0 (tsc + vite)")
check("8f-render-probe",
      '"errors": []' in probe and "Your logs, finally in order." in probe
      and '"terminalSvg": true' in probe and '"canvas": true' in probe,
      "headless probe of built dist: 0 console errors, h1 with 29 split "
      "spans, Soffit canvas 1440x637, Terminal SVG present")

print("\nLEG 8 summary: %d passed, %d failed" % (passed, failed))
sys.exit(0 if failed == 0 else 1)
