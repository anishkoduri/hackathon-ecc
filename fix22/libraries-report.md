# Fix #22 §11 report — 4 free GitHub design asset libraries

**Implementation agent report, 2026-11-12.** Companion files:
`fix22/libraries-patches.md` (LIB-01–LIB-08 patch specs + LIB-05 applied staged
edit), `fix22/SPEC.md` §11. The 144-item disposition table stands unchanged —
the libraries are a process/asset addition recorded here, no rows added to any
disposition file.

## 1. Deliverables

| # | What | Location |
|---|------|----------|
| 1 | Staged edit (APPLIED): Vanta in design-taste-frontend | `new-skills/design-taste-frontend/SKILL.md:126` — `VANTA_F22` occurs exactly once (file 607 lines, was 606). No wave-1 text touched (TRENDS_F22, DIRECTIVES_F22, MOBBIN_PATTERN_F22 intact). |
| 2 | Patch specs LIB-01–LIB-04, LIB-06–LIB-08 | `fix22/libraries-patches.md` |
| 3 | This report | `fix22/libraries-report.md` |

## 2. Live-verified versions + licences (all checked 2026-11-12, do not take the SPEC's expectations as verified)

| Library | Repo | Pinned version | Licence (verified live) | Source of verification |
|---------|------|---------------|------------------------|------------------------|
| Lenis | https://github.com/darkroomengineering/lenis | `lenis@1.3.27` (npm latest; gitHead `1f60fb9199a823f10fb23f7df55011defbb2747a`) | **MIT** | npm registry `registry.npmjs.org/lenis/latest` — `"license":"MIT"`, `"version":"1.3.27"` (crawled 2026-11-12 23:10 UTC). Corroborated by the Lenis guide stating MIT. |
| GSAP | https://github.com/greensock/GSAP | `gsap@3.15.1` (npm latest — note: 3.15.1, not 3.15.0 as some guides say) | **GreenSock Standard "no charge" licence — NOT MIT** (see deviation D1) | npm registry `registry.npmjs.org/gsap/latest` — `"license":"Standard 'no charge' license: https://gsap.com/standard-license."`, `"version":"3.15.1"`. Free incl. all plugins since 3.13 (Webflow acquisition) corroborated by gsap.com Installation docs and GreenSock's own statements. |
| Vanta | https://github.com/tengbao/vanta | `vanta@0.5.24` (npm latest; gitHead `b09bdb4a9000a63f907320d79654da9d0023a4f7`) + `three@0.134.0` (see §5 D3–D4) | **MIT** | npm registry `registry.npmjs.org/vanta/latest` — `"license":"MIT"`, `"version":"0.5.24"`; repo `package.json` on master — `"license": "MIT"`, `"version": "0.5.24"`. |
| React Bits | https://github.com/DavidHDev/react-bits | **No npm package** — pinned repo commit `9d9c687dc4f55b23539aa5417b703078047efa74` (2026-11-10, "Tool performance improvements") | **MIT + Commons Clause v1.0 — NOT pure MIT** (see deviation D2) | GitHub API `api.github.com/repos/DavidHDev/react-bits/commits?per_page=1` (latest commit above); repo `LICENSE.md` on main, read verbatim — "MIT + Commons Clause License Condition v1.0", Copyright (c) 2026 David Haz. |
| three.js (Vanta dependency) | https://github.com/mrdoob/three.js | `three@0.134.0` for Vanta scenes (r134); latest upstream is 0.187.0; plugin's general pin is 0.185.1 (see §5 D3) | **MIT** | npm registry `registry.npmjs.org/three/latest` — `"license":"MIT"`, `"version":"0.187.0"`. Vanta README (master, read verbatim) documents three.js **r134** in its script-tag example (`cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js`) and states effects are rendered by three.js or p5.js, with the host supplying THREE (global or passed in). Vanta's `package.json` declares **no** three.js dependency or peerDependency at all. |

## 3. GSAP integration verification — INTACT (with one correction to the parent baseline)

**Finding: the existing `--domain gsap` integration is intact and complete.**
Evidence (built tree, Audit #66 state):

- `skills/ui-ux-pro-max/SKILL.md:3` (frontmatter) and `:8` — "17 GSAP presets"
  in the searchable-data counts.
- `skills/ui-ux-pro-max/SKILL.md:164` — the `--motion` bullet: "`--motion`
  attaches a ready-to-use GSAP snippet (with framework notes, Do/Don't, and
  performance notes) pulled from `--domain gsap`, matched to the resolved tier
  (Subtle/Standard/Complex)."
- `skills/ui-ux-pro-max/SKILL.md:191` — domain table row: "GSAP animation
  presets | `gsap` | `"scroll reveal stagger" --domain gsap`".
- `skills/ui-ux-pro-max/data/motion.csv` — 18 lines = header + **17 data rows**
  (rows 1–17), each a GSAP preset with snippet, framework notes, Do/Don't, and
  performance notes, tiered Subtle/Standard/Complex. Every row's framework
  notes already carry the reduced-motion handling.
- `skills/ui-ux-pro-max/data/data-provenance.json:1131,1144,1148` — GSAP scope
  ("No 1-17; GSAP API identifiers…") with refs to `gsap.com/docs/v3/GSAP/`
  and `gsap.com/docs/v3/Plugins/ScrollTrigger/`.

**Correction to the parent baseline ("ScrollTrigger: 0 mentions"):** that count
was over **build.sh only** (verified: `grep -cw ScrollTrigger build.sh` = 0,
re-checked 2026-11-12). In the **built tree** ScrollTrigger already appears —
in the upstream skill's data files, not in skill prose:

- `motion.csv` rows 4, 5, 6 (Scroll Reveal) and 13, 14 (Parallax Scroll) —
  snippets with `scrollTrigger` configs (5 lines total).
- `data/stacks/threejs.csv` rows 35–36 — "Load GSAP Before Scene Script" and
  "Register ScrollTrigger Before Use" (incl. the `gsap.registerPlugin(
  ScrollTrigger)` requirement).
- `skills/design-taste-frontend/references/motion.md:202` — "GSAP ScrollTrigger
  scoped to that section without its pin (tech only)".

So the GSAP extension (LIB-04) does NOT introduce ScrollTrigger from zero: it
**names ScrollTrigger in skill prose** (where it was previously data-only) and
ties it to the Group B token values. LIB-02 does the same routing in
motion-patterns. The 17 presets are NOT re-verified row-by-row for snippet
correctness (that is the upstream skill's data, unchanged by this fix); the
verification here is that the integration exists, is referenced from SKILL.md,
and the preset count is 17 as claimed.

**Also verified:** baseline re-check over build.sh (2026-11-12, word-boundary
greps): Lenis 0, Vanta 0, React Bits 0, ScrollTrigger 0, "smooth scroll" 0,
"threejs" 4, GSAP 8 — matching the parent baseline exactly. build.sh md5
`8dfacb47a2a6698d47e4b4a5f8d9126c`, 23,647 lines — unchanged starting state.

## 4. Bundled vs install-on-demand (per library)

Existing convention followed (found in build.sh): plugin-script deps are exact-
pinned in the repo-root `package.json` + `package-lock.json` and installed with
`npm ci` (build.sh:13735–13737; current deps: `@iarna/toml@2.2.5`,
`ajv@8.20.0`, `js-yaml@4.3.2`, `sql.js@1.14.2`); clone sources are pinned to
SHAs via `pin_checkout()` (build.sh:46–51; six pins: ECC, UIPRO, MARKETPLACE,
CHWEZI, FLECTO, AGENTSKILLS); CBM binary is NOT bundled; `puppeteer-core` is
install-only at a pinned version (`puppeteer-core@25.17.0`).

| Library | Decision | Reason |
|---------|----------|--------|
| Lenis | **Install-on-demand, per project** (`npm i lenis@1.3.27`, exact pin in the project's package.json + lockfile) | A build's runtime dependency, not a plugin-script dependency. The plugin's node_modules ships only what the plugin's own scripts need; a generated project's deps belong to the project. Small (~3 kB gzipped), no install scripts. |
| GSAP | **Install-on-demand, per project** (`npm i gsap@3.15.1`, exact pin in the project's package.json + lockfile) | Same as Lenis. The plugin only *references* GSAP (presets/snippets); it never loads GSAP itself. |
| Vanta | **Install-on-demand, per project** (`npm i vanta@0.5.24 three@0.134.0`, exact pins in the project's package.json + lockfile) | Same as Lenis/GSAP, plus its three.js dependency is installed alongside it as the paired pin (Vanta declares no three.js dependency of its own — §5 D4). ~120 kB min+gzip incl. three.js per the README. |
| three.js | **Install-on-demand, per project** — two pins coexist: general `three@0.185.1` (existing, `data/stacks/threejs.csv` row 1) and Vanta-scoped `three@0.134.0` | The general pin governs hand-written three.js scenes; the Vanta-scoped pin governs Vanta scenes only. See §5 D3 for why they differ. |
| React Bits | **Copy-paste vendored source at the pinned commit** (no npm package exists; `npx shadcn@latest add @react-bits/<Bit>-TS-TW` or `npx jsrepo add github/DavidHDev/react-bits/<path>`) | The library's own distribution model: components land as source files the project owns. No runtime dependency to pin; the pin is the repo commit SHA. Optional peer deps (GSAP/three.js) resolve through the already-pinned versions above. |

**Security note (how checked):** each repo/licence/version was verified live
from the authoritative source (npm registry + GitHub raw/API, §2). All five
packages are well-known public libraries (Lenis ~14k stars, GSAP the industry
standard, Vanta long-standing, React Bits 51.5k stars, three.js the standard
WebGL library). No install scripts were run by this agent, and the plugin
itself never installs these libraries — they are installed by the build's own
package-manager step, or copied as source via the standard shadcn/jsrepo CLIs.
The standing re-scan bar (0 malicious) applies at audit time over the new pins;
nothing here exempts it.

## 5. SPEC deviations proposed / flags for the coordinator

**D1 — GSAP licence is NOT MIT (SPEC §11 expected MIT for all four).** The npm
registry licence field is `Standard 'no charge' license:
https://gsap.com/standard-license` — GreenSock's own licence, free for all uses
including commercial since GSAP 3.13 (Webflow acquisition, all former Club
plugins now public). The **free-only rule still holds** (no payment, no
account, no key); only the licence *name* differs. Recorded in LIB-03/LIB-04
as the GreenSock Standard "no charge" licence. No action needed beyond the
record — but verify22.py must assert that licence string, not "MIT", for GSAP.
(One third-party page claimed "MIT License, Copyright (c) 2026 GreenSock" —
that text belongs to GreenSock's separate gsap-skills repo, not to GSAP itself;
the registry field is authoritative and was used.)

**D2 — React Bits licence is MIT + Commons Clause, NOT pure MIT.** Verified
from the repo's LICENSE.md (read verbatim): free for personal and commercial
use *inside an application, website, or product*, but the components
themselves may not be sold, sublicensed, or redistributed — alone, in a
bundle, or as a port. That restriction does not block the plugin's use (builds
ship apps, not the library), but it is a real restriction the manifest must
record, and the "free" claim must carry the Commons Clause qualifier.
Additional notes: (a) React Bits has a paid **Pro** tier (complete pages,
templates, Agent Kit — "pay once") — the free library stays free forever per
the README, and Pro is NOT approved or used by this weave; (b) official
**Vue and Svelte ports exist** (vue-bits.dev, sveltebits.xyz) — out of scope
per SPEC (React-only); not woven in, noted here only; (c) there is **no npm
package and no semver** — the pin is a commit SHA by necessity, not by choice.

**D3 — Vanta is stale, and its three.js pin is deliberately old.** npm latest
is `vanta@0.5.24`; the repo has **no GitHub releases at all**
(`api.github.com/repos/tengbao/vanta/releases/latest` → 404) and the version
has not moved in years. Its README documents **three.js r134** (= `three@
0.134.0`). The plugin's general three.js pin is `0.185.1` (threejs.csv row 1)
and latest upstream is `0.187.0` — **neither is verified compatible with Vanta
0.5.24**, and three.js has removed APIs across the r134→r187 span, so the
newer pins were NOT substituted. Decision: Vanta scenes pin the
README-documented pair (`vanta@0.5.24` + `three@0.134.0`); the general
`0.185.1` pin continues to govern hand-written three.js scenes. The two pins
coexisting is intentional and stated in LIB-03/LIB-05/LIB-06. Proposed
follow-up for the coordinator/audit: smoke-test a Vanta scene with
three@0.134.0 before relying on it, and record Vanta's staleness in the
manifest (same treatment as Bang Motion §12: pin + record staleness; the
library is a pinned asset, not a live dependency needing upstream updates).

**D4 — Vanta declares no three.js dependency.** Vanta's `package.json`
(master) has no `dependencies` and no `peerDependencies` — the host must
supply THREE (global script tag or passed in as the `THREE:` option). Handled
explicitly by the paired pin in LIB-03/LIB-05/LIB-06 (the build installs both
packages and passes THREE in). A build that installs `vanta` alone gets a
runtime failure — the patch texts say so by pinning the pair together.

**D5 — p5.js-backed Vanta effects excluded.** Vanta effects are rendered by
three.js **or** p5.js (README); TRUNK (and any other p5-backed effect) needs
p5.js, for which there is no pin and no verification. LIB-05/LIB-06 state
p5-backed effects are not covered (recorded-gap if a build wants one). This
narrows the SPEC's "waves, birds, net, fog, etc." (all three.js-backed) by
excluding the p5 subset — flagged, not silently dropped.

**D6 — Lenis values live in the directed init, not in `motionTokens`.**
LIB-01 states `lerp: 0.1` in the rule text rather than adding a token entry,
because AB-03 owns the `motionTokens` block and a token edit would collide
with its anchors. The SPEC's "smooth-scroll rule/token" is satisfied as a rule
with exact values (§10-directive form); a future token pass may move the
values into `motionTokens`. Flagged for the coordinator.

**D7 — Taste landing pages keep the no-smooth-scroll-library rule (no
`references/motion.md` change).** Staged
`new-skills/design-taste-frontend/references/motion.md:203` says "No
smooth-scroll library (Lenis, Locomotive, ScrollSmoother) on any page". The
Lenis weave is scoped to motion-governed **app surfaces** only (LIB-01/LIB-02
state the carve-out explicitly, mirroring the fix #17 M1 carve-out already in
motion-foundations Rule 9 / motion-patterns Rule 9). No change to motion.md is
proposed — this is a deliberate scope boundary, not an oversight. If the
coordinator wants Lenis on Taste landing pages, that is a separate parent
decision.

**D8 — Observation (not a patch): stale GSAP CDN pin in threejs.csv.**
`data/stacks/threejs.csv` row 35 (line 36) shows a CDN example loading
`gsap@3.12.2`, while the new pin is `gsap@3.15.1`. That data file is upstream
clone content, outside this fix's patch scope; left untouched. Coordinator
decides whether to align it (and whether the 3.12.x CDN example stays valid
under the free-since-3.13 licence change — 3.12.2 predates the all-plugins-free
change, so its SplitText-era licence note differs).

**D9 — AB-03 conflict flags are cited, not resolved.** LIB-02 and LIB-04 cite
the AB-03 flags where a routed value is under one (30ms stagger vs Rule 5's
0.05s floor; exit 0.8× vs quick-reference ~60–70%; press scale 0.95 vs polish
0.97 — LIB-04 does not set a press value). The parent adjudicates; this fix
changes none of those values.

## 6. Per-library placement (as built / as specified)

| Library | Placement | File:line (anchor token) |
|---------|-----------|--------------------------|
| Lenis | motion-foundations smooth-scroll rule | `skills/motion-foundations/SKILL.md`, after the "When to disable animation entirely" list (LIB-01, LENIS_F22) |
| Lenis | motion-patterns scroll routing (reveal + progress bar) | `skills/motion-patterns/SKILL.md`, after the Scroll progress bar example (LIB-02, LENIS_F22 / SCROLLTRIGGER_F22) |
| Lenis | ui-ux-pro-max stack scope | `skills/ui-ux-pro-max/SKILL.md:204` Available stacks line (LIB-03) |
| GSAP | ui-ux-pro-max ScrollTrigger + Group B numbers through tweens | `skills/ui-ux-pro-max/SKILL.md:164` `--motion` bullet (LIB-04, GSAP_F22 / SCROLLTRIGGER_F22); verified intact: SKILL.md:3, :8, :164, :191; `data/motion.csv` rows 1–17 |
| Vanta | design-taste-frontend shader scenes / hero backgrounds | `new-skills/design-taste-frontend/SKILL.md:126` — **APPLIED** (LIB-05, VANTA_F22) |
| Vanta | ui-ux-pro-max background options (app surfaces) | `skills/ui-ux-pro-max/SKILL.md`, after the Anti-generic bar paragraph (LIB-06, VANTA_F22) |
| React Bits | motion-patterns (primary home) | `skills/motion-patterns/SKILL.md`, before `## End-to-End Example` (LIB-07, REACTBITS_F22) |
| React Bits | ui-ux-pro-max scope pointer | `skills/ui-ux-pro-max/SKILL.md`, after the "Domain is auto-detected" paragraph (LIB-08, REACTBITS_F22) |

## 7. Self-verification performed

- Re-ran all baseline greps over build.sh (Lenis 0, Vanta 0, React Bits 0,
  ScrollTrigger 0, smooth scroll 0, threejs 4, GSAP 8) and confirmed build.sh
  md5 `8dfacb47a2a6698d47e4b4a5f8d9126c` / 23,647 lines — starting state intact
  (build.sh was never edited).
- Verified every LIB-01–LIB-08 anchor occurs exactly once in its target file
  in the Audit #66 built tree (counts recorded in `libraries-patches.md`
  header); checked no anchor collides with ab-patches.md AB-01–AB-14 or
  process-patches.md P1–P5.
- Verified the 17 GSAP presets: `motion.csv` = 18 lines (header + rows 1–17);
  `scrollTrigger` in rows 4–6 and 13–14 (5 lines).
- Verified the staged Taste edit by re-grep: `VANTA_F22` exactly once, line
  126; file 607 lines; wave-1 texts untouched.
- Verified the five anchor tokens (LENIS_F22, GSAP_F22, SCROLLTRIGGER_F22,
  VANTA_F22, REACTBITS_F22) were 0 in build.sh and 0 in the built tree before
  this fix.
- Banned-term scan (case-insensitive) over `fix22/libraries-patches.md`,
  `fix22/libraries-report.md`, and the staged Taste edit: **0 hits** for any
  of the seven banned terms.
- No new skill created; no font rules, screen-verdicts rule, model pins,
  marketplace manifest, or Audit #4 backup touched; `hackathon-ecc/` never
  edited; `bash build.sh` never run; `fix11/fix11-stage.py` never run.
- No file outside `~/workspace/hackathon-plugin/fix22/` and the single staged
  Taste SKILL.md edit was written.

## 8. Open items for the coordinator / integrator

1. Apply LIB-01–LIB-04, LIB-06–LIB-08 in the build.sh patch blocks, rebuild,
   and run the LIB checklist in `libraries-patches.md` (incl. the staged
   Taste edit surviving the rebuild).
2. Adjudicate / record deviations D1–D9 in the manifest (esp. D1 GSAP licence
   string, D2 Commons Clause qualifier, D3 Vanta staleness + three.js 0.134.0
   pair, D7 Taste scope boundary).
3. verify22.py additions listed in the `libraries-patches.md` integrator
   checklist §7 — note the GSAP licence assertion must expect the GreenSock
   Standard "no charge" licence, not MIT, and React Bits must expect
   "MIT + Commons Clause".
4. Dry-run fixtures per SPEC §11: (a) Vanta background with no reduced-motion
   fallback FAILS; (b) React Bits on a non-React stack FAILS the scope check;
   (c) a GSAP effect directed by name + exact parameters PASSES; (d) a library
   effect with no theme reason FAILS; (e) an unpinned ("latest") library
   version FAILS the pin check.
