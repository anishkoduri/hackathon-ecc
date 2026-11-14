# Fix #22 §17 patch specs — 3 more libraries/tools from the ksobohc comment

**Status:** patch specs for the coordinator + report. Do NOT edit `build.sh`
from this file alone — apply each build.sh-embedded spec as a patch in the
existing build.sh fix22 patch block (same convention as `fix22/fix22.py`,
which the coordinator extends), and apply the staged-source specs directly
to their staged files (same convention as `fix22/libraries-patches.md`
LIB-05 and `fix22/libraries15-patches.md` L15-05/L15-07/L15-08). Do NOT
edit `hackathon-ecc/` directly. Do NOT run `bash build.sh` as part of
applying (the coordinator rebuilds once). Do NOT run `fix11/fix11-stage.py`.
Do NOT edit `fix22.py` or `verify22.py` from this file.

**Patch format — 6-tuples, VERIFIED against the real file:** `fix22.py`'s
`PATCHES` list is 6-tuples `(id, rel, old, new, mode, token)`, NOT
5-tuples (verified by reading `fix22/fix22.py:1044-1141` and the
`build_sh_block()` / `preflight()` code at lines 1154-1330). The 6th
element is the idempotency token: `preflight()` fails loudly with
`TOKEN-ALREADY-PRESENT` if the token is already in the ORIGINAL built
file, and `self_checks()` asserts the token is present in the build.sh
block. The token for every patch below is the `_F22` anchor string named
in its `new_text` (for multi-token patches, the first token listed in the
summary table — any one token string present in `new_text` satisfies the
machinery, since the token only needs to be absent originally and present
after). Staged edits (L17-05, L17-06, L17-07) carry a token the same way
for `verify22.py`, following the L15 convention; they are NOT `fix22.py`
`PATCHES` entries.

**Anchor convention (same as ab-patches.md / libraries-patches.md /
libraries15-patches.md):** every anchor below was verified to occur
EXACTLY ONCE in its target file in the current built tree / staged source
(counts recorded per patch, checked 2026-11-13). Apply in fix17 style:
assert the anchor count is 1, fail loudly on mismatch, never guess.
Insert AFTER the anchor unless the entry says BEFORE. Anchors are copied
VERBATIM from the target file (including line wrapping — the built tree
wraps long paragraphs; a one-line anchor that spans a wrap in the file
does NOT match).

**Anchor-collision check (2026-11-13):** no anchor below collides with
any anchor in `fix22/ab-patches.md` (AB-01–AB-14),
`fix22/process-patches.md` (P1–P5), `fix22/libraries-patches.md`
(LIB-01–LIB-08), or `fix22/libraries15-patches.md` (L15-01–L15-08),
except the DELIBERATE shared/chained anchors listed under Ordering
dependencies below (L17-01 shares the A11 anchor with L15-01; L17-02
shares the `## End-to-End Example` anchor with LIB-07 and L15-02;
L17-03 chains on L15-03's inserted text; L17-05 shares the
`One object never carries the page` anchor with L15-05; L17-06 and
L17-07 chain on L15-08's inserted text). Shared `before`/`after`
anchors are safe under `fix22.py`'s list-order simulation (the anchor
text itself is never consumed by an insert); chained anchors REQUIRE
the list/staged order in §Ordering dependencies.

**Anchor tokens for cross-reference / verify22.py:** `CASBERRY_F22`
(L17-01, L17-02, L17-03, L17-05, L17-07), `ORIGINKIT_F22` (L17-02,
L17-03, L17-05), `DAISYUI_F22` (L17-03, L17-04, L17-05). All three
tokens were 0 in build.sh and 0 in the built tree before this fix
(checked 2026-11-13 — see Report §10). Each token occurs exactly once
per file it is placed in (never repeated within a file): patch texts
therefore NEVER repeat a token already placed in the same file by an
earlier patch — cross-references to Vanta / R3F / ShaderGradient /
liquid glass / liquid-logo / the one-WebGL rule inside a patch text use
the plain name (§11 / §15), never the `_F22` token, where that token
already lives in the file.

**Pinned versions (all verified live 2026-11-13 — see Report §2 for
sources):**
- daisyUI: `daisyui@5.7.50` (exact), MIT; pair: Tailwind CSS v4 ONLY.
- OriginKit: NO version to pin (browsable library, no npm package, no
  repo pin) — the binding constraint is the 10/day fetch cap + the
  env-only key, not a version.
- Casberry: NO version to pin (hosted tool, no npm package, no repo) —
  the pin is the tool URL + the export step; the SPEC's "v2.0.0 Oct
  2026" was NOT re-verified live in this session and is NOT recorded
  as a pin (see Report §2).

**Bundled vs install-on-demand (per item, following the plugin's
existing convention — see Report §6):** daisyUI install-on-demand per
project (exact pin in the project's package.json + lockfile);
OriginKit copy-paste fetch, no install (MCP NOT wired); Casberry
standalone tool, no install (output is code/asset only).

Banned terms check: none of the new texts below contains any of the
seven banned terms (case-insensitive: claude, codex, anthropic, opus,
sonnet, haiku, composer-2.5). Note: the Casberry site's own prompt text
names two LLM providers — that wording is NOT quoted anywhere in the
patch texts below (the tool is described as "a general-purpose LLM").
The word "AI" appears in the patch texts (in "AI Particle Architect",
the tool's own name) — "AI" is NOT banned.

---

## Summary table

| Patch | File (edit point) | Mode | Anchor (short form) | Token |
|-------|-------------------|------|---------------------|-------|
| L17-01 | `skills/motion-foundations/SKILL.md` (build.sh fix22 block) | after | A11 Solid drawing in 3D block | `CASBERRY_F22` |
| L17-02 | `skills/motion-patterns/SKILL.md` (build.sh fix22 block) | before | `## End-to-End Example` | `ORIGINKIT_F22` (also `CASBERRY_F22`) |
| L17-03 | `skills/ui-ux-pro-max/SKILL.md` (build.sh fix22 block) | after | L15-03 caveat tail (chained on L15-03) | `DAISYUI_F22` (also `CASBERRY_F22`, `ORIGINKIT_F22`) |
| L17-04 | `skills/design-system/SKILL.md` (build.sh fix22 block) | after | Mode 1 Output line | `DAISYUI_F22` |
| L17-05 | `new-skills/design-taste-frontend/SKILL.md` (STAGED source, direct edit) | before | `- **One object never carries the page.**` line | `CASBERRY_F22` (also `ORIGINKIT_F22`, `DAISYUI_F22`) |
| L17-06 | `round2-skills/polish-pass/reference/slop-checklist.md` (STAGED source, direct edit) | replace | L15-08 flag-list fragment (chained on L15-08) | `CASBERRY_F22` is in L17-07, not here — token for this tuple is the replaced fragment's file token `WEBGL_ONE_F22` (already present; see note) |
| L17-07 | `round2-skills/polish-pass/reference/slop-checklist.md` (STAGED source, direct edit) | after | L15-08 section tail (chained on L15-08) | `CASBERRY_F22` |

**L17-06 token note (flagged for the coordinator):** L17-06 is a
`replace` on L15-08's inserted text, and its `new_text` adds NO new
`_F22` token — it only adds the words "a Casberry particle export" to
the existing counted-effects list. The `CASBERRY_F22` token for the
checklist file is carried by L17-07 alone (exactly once in the file).
If the coordinator folds L17-06 into `fix22.py`'s `PATCHES` (rather
than applying it as a staged direct edit), the 6th tuple element must
be a string absent from the original file and present after — use
`"a Casberry particle export"` as the token, NOT `WEBGL_ONE_F22`
(which is already present in the file post-L15-08 and would trip
`TOKEN-ALREADY-PRESENT`). As written here (staged direct edit, same as
L15-08), no `fix22.py` token machinery applies.

## Ordering dependencies (coordinator MUST respect — list/staged order)

1. **L15-01 before L17-01.** Both insert AFTER the same A11 anchor.
   List order L15-01 → L17-01 gives final stacking: A11 block,
   L17-01 (Casberry), L15-01 (R3F). Either order satisfies the anchors;
   this order keeps the tool rule before the implementation-layer rule.
2. **LIB-07, then L15-02, then L17-02.** All three insert BEFORE
   `## End-to-End Example`. `before` inserts stack in list order, so
   the final order is: LIB-07 (React Bits), L15-02 (R3F scene), L17-02
   (OriginKit + Casberry pattern), then the heading.
3. **L15-03 before L17-03 (HARD).** L17-03's anchor is the tail of the
   text L15-03 inserts (the ShaderGradient licence-caveat paragraph).
   The anchor does not exist until L15-03 is applied; `preflight()`
   would fail `ANCHOR-COUNT=0` otherwise.
4. **L15-05 before L17-05.** Both insert BEFORE the
   `One object never carries the page` line in the staged Taste file.
   Staged apply order L15-05 → L17-05 gives final stacking: L15-05
   bullets, L17-05 bullets, then the "One object" bullet.
5. **L15-08 before L17-06 and L17-07 (HARD).** Both anchors are text
   L15-08 inserts into the staged slop-checklist. Staged apply order
   L15-08 → L17-06 → L17-07. L17-06 and L17-07 are staged direct edits
   (NOT `fix22.py` patches) precisely so they do not depend on a
   rebuild-then-preflight round-trip: the coordinator applies L15-08,
   then applies these two against the updated staged file.

---

## L17-01 — motion-foundations, Casberry particle scenes (standalone tool) (CASBERRY_F22)

- **Target:** `skills/motion-foundations/SKILL.md`, Principles section
  (A11 Solid drawing in 3D — a particle scene is a 3D depth moment).
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-01/LIB-02/L15-01).
- **Built-tree location:** the A11 principle block, lines 87–89.
- **Anchor (count==1, insert AFTER):**

  ```
  - **A11 Solid drawing in 3D** — an object keeps believable volume, weight, and depth
    while it moves. In UI: a card that flips or expands keeps its shadow, edge, and
    layering consistent through the move; it never flattens into a texture or shears.
  ```

- **Insert (full text):**

```md

### Particle backgrounds — Casberry, a standalone tool (fix #22 §17, CASBERRY_F22)

Where a build needs a bespoke particle scene — a hero or dealt moment the
libraries do not have (Vanta's named effects, a hand-built React Three
Fiber scene) — the approved production method is Casberry
(particles.casberry.in, "AI Particle Architect", free, no sign-up, no
install): a hosted tool that generates a live 20,000+ particle Three.js /
WebGL simulation from a prompt and exports React / Three.js code or a
standalone WebGL / HTML file, which is then dropped into the project.
Casberry is a STANDALONE TOOL, not a library to import and not a runtime
dependency — the plugin never imports it; it records the tool + the
export step (same form as liquid-logo, §15). Directed per §10: the agent
writes the prompt / spec with exact values (particle count, form, motion,
colours from the theme's own tokens, controls) and the tool generates;
the generated effect is reviewed against the theme and D19 before use.
The export is the surface's one WebGL-heavy effect (see the
`polish-pass` slop checklist, one-WebGL rule): a Casberry export never
shares a surface with a Vanta scene, a React Three Fiber scene, a
ShaderGradient, liquid glass, or liquid metal. Constraints, all binding:
theme-matched (particle colours are the theme's own tokens); a static
fallback (the theme's gradient or image ground) on mobile/low-power and
whenever WebGL is unavailable; the scene MUST disable under
`prefers-reduced-motion: reduce` (the finished still shows instead);
never behind text without a scrim and a 4.5:1 contrast check. TRUST FLAG
+ EXPORT REVIEW (binding): the domain carries a very low automated trust
score (ScamAdviser 1/100, WHOIS hidden, iframed — a weak automated
signal, NOT a verdict; a second checker rates it 60/100 with no malware
detected) and its terms / licence are UNRESOLVED (no terms or licence
statement found on the site as of Nov 13, 2026 — exported effects are
NOT assumed free for commercial use). Every exported snippet is
therefore treated as UNTRUSTED code: review every line before it enters
a build (same bar as the plugin's security re-scan — no document /
window / fetch / eval / network access, no obfuscated payloads), never
paste it blind; a Casberry export pasted without review FAILS the
security check (see the `polish-pass` slop checklist, export-review
check). Which 3D path to reach for: Vanta (§11) is the imported
3D-background LIBRARY for a known effect; Casberry is the TOOL that
exports Three.js code for a bespoke particle scene; React Three Fiber
(§15) is the React 3D layer the exported React code can feed and the
layer for hand-built React scenes. Theme-match precondition: a particle
scene is applied only when it matches the dealt theme; a clash is not
applied, with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the particle motion is the dealt moment's motion, with
exact values in the directing prompt; Theme: the scene is the dealt
theme's depth, never a stock particle demo; Texture: the particle field
is the surface's texture / depth layer; Visuals: the scene is the hero's
visual anchor, never behind unreadable text (4.5:1 scrim / contrast
check where text overlaps it); Techniques: standalone tool at
particles.casberry.in, exported code reviewed line by line before it
enters the build, no runtime dependency; Colors: none — the particle
colours are the theme's own tokens.)
```

## L17-02 — motion-patterns, OriginKit animated components + Casberry pattern (ORIGINKIT_F22 / CASBERRY_F22)

- **Target:** `skills/motion-patterns/SKILL.md`, `## Code Examples`
  section, after the last example (R3F scene, L15-02), before the
  End-to-End Example.
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-02/LIB-07/L15-02).
- **Built-tree location:** `## End-to-End Example` heading (count==1).
- **Anchor (count==1, insert BEFORE):**

  ```
  ## End-to-End Example
  ```

- **Insert (full text):**

```md
### OriginKit — animated components, React/Next only (fix #22 §17, ORIGINKIT_F22)

OriginKit (originkit.dev) is a browsable catalog of animated React
components — backgrounds, cursor treatments, text effects, buttons,
loaders, image galleries — fetched by copy-paste from the site or
through its MCP server. The catalog is organised in 6 categories
(interactive elements, image galleries, text effects, animations,
background animations, buttons). COUNT NOTE (binding): the site's own
numbers disagree — the homepage says "Discover 805 Components" (Nov 13,
2026), the skill README says 50 across the 6 categories, the pricing
page says 60 components — the categories matter more than the exact
number; never cite a component count as exact. Stack: React, Tailwind
CSS, Framer Motion; usable in Framer, React, Next.js, Vite. SCOPE —
React/Next.js builds ONLY: on a non-React stack the PATTERN is
implemented with the stack's own tools (recorded-gap style: name the
closest equivalent — a CSS / GSAP / vanilla implementation of the same
effect — never force OriginKit outside React). Each component is used as
a §10 directive (component name + exact props, as listed for that
component on originkit.dev — the directive records the prop values, it
never says "a fluid-trail effect") with its fix #19 D19 reason, recorded
in `docs/design-tokens.md`. ACCESS + CAP (binding): browsing is free, no
API key. FETCHING component source requires a FREE API key
(originkit.dev > Settings > API Integration). DAILY LIMIT: 10 component
fetches per key per day, resets midnight UTC, shared between MCP and
website copies. A build needing more than 10 OriginKit fetches in a day
hits the cap: proceed from the skills alone, record the gap, never pay
for Pro ($79/yr) or Ultimate ($99/yr) — same form as Mobbin §9.
Pro-marked components are excluded on the free tier. API KEY HANDLING
(binding): the free key is an env var only, never written to any file
(same rule as the ElevenLabs narration key). NO MCP WIRING in the plugin:
the default is copy-paste from the site; the MCP server
(https://mcp.originkit.dev/mcp) is NOT wired in unless reachability +
env-only key flow are verified — that verification has NOT been done, so
copy-paste is the only wired path. LICENSE (binding): CONDITIONAL /
source-available — NOT a clean open-source licence. The terms restrict
redistribution of components and templates: components are for use in
your own project, not for redistribution, and the plugin must not
re-publish OriginKit components as its own. DISTINCTION CHECK (binding):
OriginKit (originkit.dev — animated flourishes) is NOT Origin UI
(originui.com, now coss ui / Base UI — solid form / layout primitives:
button, input, nav, card shells). A build citing Origin UI when it
means OriginKit (or vice versa) FAILS the distinction check. DEDUPE vs
React Bits (§11): React Bits is the importable MIT library (copy-paste
source at a pinned commit); OriginKit is the browsable catalog for
animated flourishes fetched by copy-paste or MCP. Reach for React Bits
when the build wants a pinned, importable bit; reach for OriginKit when
the build wants to browse a catalog for a flourish (background, cursor
treatment, text effect, button, loader) and fetch it. OriginKit
components are IMPLEMENTATIONS of motion patterns — the pattern stays
the authority, the component is the menu item. Components that animate
respect `prefers-reduced-motion: reduce` (static final state) — a
component with no reduced-motion handling is not used. OriginKit is a
menu, never a default: a component is used only when the dealt theme
calls for that exact effect. Theme-match precondition: every component
must still match the dealt theme; a clash is not applied, with the
reason recorded in `docs/design-tokens.md`.

(D19 — Motion: the component's animation is the motion decision, with
exact props as the values; Theme: the component is theme-matched or not
used; Texture: none — a component adds motion, not a surface treatment
(background components excepted: those ARE the surface's texture,
theme-matched); Visuals: the component's effect is visible and anchored,
never decoration that obscures content; Techniques: copy-paste fetch at
the 10/day cap, env-only key, no MCP wiring; Colors: none — the
component's colours are the theme's own tokens.)

### Particle background — Casberry export (fix #22 §17, CASBERRY_F22)

A bespoke particle background on any stack is produced with Casberry
(particles.casberry.in) — see `motion-foundations` for the full rule:
the agent directs the prompt with exact values, exports React /
Three.js code or a standalone WebGL / HTML file, and drops it into the
project. The export is the surface's one WebGL-heavy effect and is
reviewed as untrusted code before it enters the build (same bar as the
plugin's security re-scan) — never pasted blind. Under
`prefers-reduced-motion: reduce` the scene does not run — a static
image / poster of the finished scene renders in its place. Theme-match
precondition: the particle scene must still match the dealt theme; a
clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the particle motion is the dealt moment's motion, exact
in the directing prompt; Theme: the scene is the dealt theme's depth
moment, never a stock particle demo; Texture: the particle field is the
surface's texture / depth layer; Visuals: the scene is the hero's visual
anchor, never behind unreadable text; Techniques: standalone tool,
exported code reviewed line by line, no runtime dependency; Colors:
none — the particle colours are the theme's own tokens.)

```

## L17-03 — ui-ux-pro-max, §17 libraries stack scope (CASBERRY_F22 / ORIGINKIT_F22 / DAISYUI_F22)

- **Target:** `skills/ui-ux-pro-max/SKILL.md`, `### Step 4: Stack
  Guidelines`, immediately after the §15 libraries scope paragraph
  (L15-03).
- **Edit point:** build.sh fix22 patch block (no staged source exists for
  this skill — same as LIB-03/LIB-04/LIB-06/LIB-08/L15-03/L15-04).
- **Built-tree location:** the tail of the L15-03 insert (the
  ShaderGradient licence-caveat paragraph). CHAINED anchor: this patch
  MUST run after L15-03 in `PATCHES` list order (same chaining pattern
  as AB-03b on AB-03a and L15-03 on LIB-03).
- **Anchor (count==1 post-L15-03, insert AFTER):**

  ```
  The Figma plugin's paid Pro
  tier is out of scope — the npm library is the integration, and it is free.
  ```

- **Insert (full text):**

```md

**§17 design asset libraries — stack scope (fix #22 §17, CASBERRY_F22 /
ORIGINKIT_F22 / DAISYUI_F22).** Three more free libraries / tools are
approved menu items, never defaults — each is chosen through the
skills, theme-matched, with a D19 reason, and directed per §10 (library
+ effect name + exact parameters). The three arrive in three different
integration forms: **daisyUI** (`daisyui@5.7.50`, MIT) is an npm plugin
dependency; **OriginKit** (originkit.dev; conditional / source-available
licence — see `motion-patterns`) is a browsable library fetched by
copy-paste (MCP not wired — see below); **Casberry**
(particles.casberry.in; terms unresolved — see
`motion-foundations`) is a standalone tool that exports code. Stack
scope: **daisyUI** is Tailwind builds ONLY (any framework, since it is
CSS) — daisyUI 5.x pairs with Tailwind CSS v4 ONLY (`@plugin "daisyui"`
in CSS; v4 class names changed from earlier versions — never mix
v4-era snippets with v5); **OriginKit** is React/Next.js ONLY
(Framer / React / Vite); **Casberry** exports are stack-independent
(the exported React code feeds the React 3D layer on React builds; the
standalone HTML file drops into any stack). Install (exact pins, per
project, install-on-demand): `npm i -D daisyui@5.7.50`, then `@import
"tailwindcss";` + `@plugin "daisyui";` in CSS. Caps + paid exclusions
(binding): OriginKit free tier — 10 component fetches per key per day
(resets midnight UTC, shared MCP + website copies), Pro-marked
components excluded, Pro ($79/yr) / Ultimate ($99/yr) never paid;
daisyUI free (MIT) — the Blueprint MCP server ($22/mo, paid licence
key) is NOT wired, and the paid Dashboard / Charts skills, Figma
library, and templates are out of scope; Casberry free, no sign-up —
terms unresolved, exports reviewed as untrusted code. Running total of
asset libraries / tools in fix #22: §11's 4 + §15's 4 + §17's 3 = 11.
Every library effect respects `prefers-reduced-motion: reduce` (static
fallback or off) — no library exempts the rule. Unpinned versions
("latest") FAIL the pin check. The pinned versions live here and in the
owning skills; a build that needs a newer version re-pins deliberately
and records the new pin + its verification, never floats. Theme-match
precondition: a library effect is applied only when it matches the
dealt theme; a clash is not applied, with the reason recorded in
`docs/design-tokens.md`.

(D19 — Motion: the libraries are the component / flourish / particle
mechanisms, chosen per build; Theme: every effect is theme-matched or
not applied; Texture: Casberry particle fields ARE texture / surface
treatments chosen through the theme; Visuals: scope keeps effects on
the surfaces where they read (daisyUI components on Tailwind builds,
OriginKit flourishes on React, particle scenes on heroes); Techniques:
exact pins + stack scope + caps, install-on-demand per project
(OriginKit copy-paste fetch, Casberry standalone tool — see
`fix22/libraries17-patches.md` §6 in the manifest record); Colors: none
— the libraries choose no colours (daisyUI themes are re-themed to the
brand deal; OriginKit and Casberry colours are the theme's own tokens).)
```

## L17-04 — design-system, daisyUI component-library menu + shadcn dedupe (DAISYUI_F22)

- **Target:** `skills/design-system/SKILL.md`, Mode 1 (Generate Design
  System) — the component-library menu a generated system may draw
  from. The primitives in this skill stay the authority; daisyUI is
  the menu item.
- **Edit point:** build.sh fix22 patch block (no staged source exists
  for this skill — ECC upstream, `origin: ECC` in the frontmatter;
  same convention as ui-ux-pro-max / motion-*).
- **Built-tree location:** after the Mode 1 Output line (file is 82
  lines; anchor is the Output line).
- **Anchor (count==1, insert AFTER):**

  ```
  Output: `DESIGN.md` + `design-tokens.json` + `design-preview.html`
  ```

- **Insert (full text):**

```md

### Component library menu — daisyUI (fix #22 §17, DAISYUI_F22)

On Tailwind builds, daisyUI (`daisyui@5.7.50`, MIT) is an approved menu
item for prebuilt components: semantic class names (`btn`, `card`,
`modal`, `toggle`, ...) on top of Tailwind utilities, plus built-in
themes; 68 components; 0 JavaScript shipped, 0 dependencies;
framework-agnostic (any framework, since it is CSS). Install (exact pin,
per project, install-on-demand): `npm i -D daisyui@5.7.50`, then
`@import "tailwindcss";` + `@plugin "daisyui";` in CSS. Version pairing
is PINNED: daisyUI 5.x + Tailwind CSS v4 ONLY — v4 class names changed
from earlier versions; never mix v4-era snippets with v5, and never
install daisyUI 4 against Tailwind v4. FIT-CHECK (binding): daisyUI has
a strong default look. Its components are a MENU of implementations,
re-themed through the brand / theme deal — the design package chooses
the direction; daisyUI supplies prebuilt components that get re-themed.
A build shipping daisyUI's default theme unexamined FAILS (generic look
— the Home Run lesson). DEDUPE vs shadcn: the plugin already pins
shadcn (`shadcn@4.23.0`, build.sh pin) as its React copy-paste
component set. Reach for daisyUI when the build is Tailwind-native and
wants semantic-class components with zero JS on any framework; reach
for shadcn when the build is React and wants the copy-paste component
set. The component primitives in this skill stay the authority — daisyUI
is the menu item, never the source of the primitives. Paid extras OUT
of scope: the Blueprint MCP server ($22/mo, paid licence key) is NOT
wired; Dashboard / Charts skills, the Figma library, and templates are
paid — out of scope. Theme-match precondition: a daisyUI component is
applied only when it matches the dealt theme; a clash is not applied,
with the reason recorded in `docs/design-tokens.md`.

(D19 — Motion: none — daisyUI adds components, not motion (an animated
component on top of daisyUI is a motion-patterns decision); Theme: the
components are re-themed to the brand deal, never shipped in the
default theme; Texture: none — daisyUI adds component structure, not a
surface treatment; Visuals: semantic classes keep the markup readable
and the components consistent across the build; Techniques: exact pin +
Tailwind v4 pairing, install-on-demand per project; Colors: the theme
colours ARE the re-theme — the default theme's colours are never
shipped unexamined.)
```

---

## L17-05 — design-taste-frontend, §17 libraries on landing pages (CASBERRY_F22 / ORIGINKIT_F22 / DAISYUI_F22) — STAGED EDIT

- **Target (staged source):** `new-skills/design-taste-frontend/SKILL.md`,
  section 2 (Tech bullet area, after the §15 bullets at staged lines
  ~127–129 once L15-05 is applied).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  LIB-05 / L15-05 / L15-07). The staged file is the source of truth for
  this skill; build.sh installs it — do NOT also patch it through the
  build.sh fix22 block.
- **Staged location:** insert BEFORE the `- **One object never carries the
  page.**` line (staged line 127; count==1).
- **Anchor (count==1, insert BEFORE):**

  ```
  - **One object never carries the page.** The product or hero object whole leads the hero and **two more sections at
  ```

  (Anchor is the first line of that bullet as wrapped in the staged file;
  the insert goes before the whole bullet.)

- **Insert (full text):**

```md
- **Bespoke particle hero backgrounds come from Casberry (fix #22 §17, CASBERRY_F22).** Where the deal calls for the one effect as a bespoke particle scene — a hero the libraries do not have — the approved production method is Casberry (particles.casberry.in, free, no sign-up): direct the prompt with exact values, export React / Three.js code or a standalone WebGL / HTML file, drop it into the build. STANDALONE TOOL, not a dependency (same form as liquid-logo, §15). The export is the surface's one WebGL-heavy effect; it is reviewed as untrusted code before it enters the build (very low automated trust score on the domain; terms unresolved — see `motion-foundations`). Constraints, all binding: theme-matched (particle colours are the theme's own tokens); a static fallback on mobile/low-power and whenever WebGL is unavailable; the scene MUST disable under `prefers-reduced-motion: reduce` (the finished still shows instead); never behind text without a scrim and a 4.5:1 contrast check. (D19 — Motion: the particle motion is the dealt moment's motion; Theme: theme-matched, the scene is the theme's own depth; Texture: the particle field is the page's texture layer; Visuals: the scene is the hero's visual anchor, never behind unreadable text; Techniques: standalone tool, exported code reviewed line by line, no runtime dependency; Colors: the particle colours are the theme's own tokens.)
- **Animated flourishes on React come from OriginKit (fix #22 §17, ORIGINKIT_F22).** Where the deal calls for an animated flourish — a background, a cursor treatment, a text effect, a button, a loader — on a React build, the approved browsable catalog is OriginKit (originkit.dev; React, Tailwind CSS, Framer Motion). Fetch by copy-paste from the site (default — the MCP server is NOT wired in the plugin). Cap (binding): 10 component fetches per key per day (resets midnight UTC); a build needing more proceeds from the skills alone and records the gap, never pays for Pro ($79/yr) or Ultimate ($99/yr). Pro-marked components are excluded on the free tier. Licence is conditional / source-available — components are for use in your own project, not for redistribution; the plugin never re-publishes OriginKit components as its own. NOT Origin UI (originui.com, now coss ui / Base UI — solid form / layout primitives): a build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check. Each component is used as a §10 directive (component name + exact props) with its fix #19 D19 reason. (D19 — Motion: the component's animation is the dealt moment's motion; Theme: theme-matched, the flourish is the theme's own motion; Texture: none — a flourish adds motion, not a surface treatment (background flourishes excepted: those ARE the page's texture layer); Visuals: the flourish is the hero's visual anchor, never decoration that obscures content; Techniques: copy-paste fetch at the 10/day cap, env-only key, no MCP wiring; Colors: the component's colours are the theme's own tokens.)
- **Prebuilt components on Tailwind landing builds come from daisyUI (fix #22 §17, DAISYUI_F22).** Where the build is Tailwind and needs prebuilt components — buttons, cards, modals, toggles — the approved library is daisyUI (`daisyui@5.7.50`, MIT; `@plugin "daisyui"` in CSS; daisyUI 5.x + Tailwind CSS v4 ONLY). Components are a MENU of implementations, re-themed through the brand / theme deal: a build shipping daisyUI's default theme unexamined FAILS (generic look — the Home Run lesson). The design package chooses the direction; daisyUI supplies prebuilt components that get re-themed. (D19 — Motion: none — daisyUI adds components, not motion; Theme: the components are re-themed to the brand deal, never shipped in the default theme; Texture: none — daisyUI adds component structure, not a surface treatment; Visuals: the components are consistent across the page, never the default look; Techniques: exact pin + Tailwind v4 pairing, install-on-demand per project; Colors: the theme colours ARE the re-theme.)
```

## L17-06 — polish-pass slop checklist, one-WebGL rule extended to Casberry exports (replace) — STAGED EDIT

- **Target (staged source):**
  `round2-skills/polish-pass/reference/slop-checklist.md`, the
  one-WebGL-heavy-effect-per-surface section (L15-08).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  L15-08). Do NOT patch through the build.sh fix22 block — see the
  L17-06 token note in the summary table. CHAINED on L15-08: apply
  AFTER L15-08.
- **Staged location:** the "What counts as a flag" bullet of the
  `WEBGL_ONE_F22` section (L15-08 insert, spec lines 497–504).
- **Anchor (count==1 post-L15-08, REPLACE):**

  ```
    WebGL-heavy library effects at once — any two of: an R3F scene
    (R3F_F22), a Vanta scene (VANTA_F22), a ShaderGradient
    (SHADERGRAD_F22), liquid glass (LIQGLASS_F22), liquid metal
    (LIQLOGO_F22).
  ```

  (Anchor is the tail of the flag bullet, lines 498–501 of
  `libraries15-patches.md` as applied — 2-space continuation indent,
  em dash before "any two of". The bullet's opening line and the rest
  of the bullet are untouched by this replace.)

- **New text (replaces the anchor verbatim):**

  ```
    WebGL-heavy library effects at once — any two of: an R3F scene
    (R3F_F22), a Vanta scene (VANTA_F22), a ShaderGradient
    (SHADERGRAD_F22), liquid glass (LIQGLASS_F22), liquid metal
    (LIQLOGO_F22), a Casberry particle export.
  ```

## L17-07 — polish-pass slop checklist, Casberry export-review check (CASBERRY_F22) — STAGED EDIT

- **Target (staged source):**
  `round2-skills/polish-pass/reference/slop-checklist.md`, appended
  after the one-WebGL-heavy-effect-per-surface section (L15-08).
- **Edit point:** STAGED source, direct edit by the coordinator (same as
  L15-08). Do NOT patch through the build.sh fix22 block. CHAINED on
  L15-08: apply AFTER L15-08 (and after L17-06; order between L17-06
  and L17-07 does not matter — different anchors).
- **Staged location:** end of the `WEBGL_ONE_F22` section (L15-08
  insert, spec lines 528–530).
- **Anchor (count==1 post-L15-08, insert AFTER):**

  ```
    effects per surface in the static check; Colors: none — the check counts
    effects, it chooses no colours.
  ```

  (The closing lines of the WEBGL_ONE_F22 D19 block, verified
  count==1 in the L15-08 insert text.)

- **Insert (full text):**

```md

## Exported code is reviewed before it enters the build — Casberry (CASBERRY_F22, fix #22 §17)

- **What counts as a flag:** a Casberry particle export (or any
  hosted-tool export) pasted into the build without a line-by-line
  review — the exported snippet is UNTRUSTED code (very low automated
  trust score on the domain, ScamAdviser 1/100; terms unresolved). A
  build pasting exported code blind FAILS the security check.
- **Justified use:** the exported snippet reviewed line by line
  against the theme and D19, with no network / DOM / storage access,
  no obfuscated payloads, and no code outside the particle function —
  then the reviewed snippet enters the build as the surface's one
  WebGL-heavy effect, with its static fallback and reduced-motion
  handling recorded.
- **Clearance:** the review is recorded (what was checked + the
  reviewer's note) in the decision record; an unreviewed export has no
  clearance — fix, do not clear, by reviewing it or removing it.
- **Standing:** a static check producing candidate evidence for
  `browser-qa`, never a verdict — same standing as every check in this
  file (fix #13e screen-verdicts rule).
- **Cross-references, do not duplicate:** the Casberry rule lives in
  `motion-foundations`; the one-WebGL-heavy-effect-per-surface check
  above counts the export as the surface's one effect. This check only
  reviews the exported code; it never restates the tool's install or
  parameters.
- **D19 —** Motion: the review keeps the effect's motion to what the
  directive specified; Theme: the reviewed effect must fit the dealt
  theme; Texture: the particle scene is the surface's texture / depth
  layer; Visuals: the reviewed scene reads as a deliberate anchor;
  Techniques: line-by-line review against the security bar, recorded
  in the decision record; Colors: none — the check reviews code, it
  chooses no colours.
```

---

## Integrator checklist (after applying)

1. Apply L17-01–L17-04 in the build.sh fix22 patch block (extend
   `fix22.py`'s `PATCHES` with the 6th token element — see the format
   note at the top), L17-05 directly to
   `new-skills/design-taste-frontend/SKILL.md`, L17-06 + L17-07
   directly to `round2-skills/polish-pass/reference/slop-checklist.md`.
   Respect the Ordering dependencies (§ above): L15-01 → L17-01;
   LIB-07 → L15-02 → L17-02; L15-03 → L17-03; L15-05 → L17-05;
   L15-08 → L17-06 → L17-07. Rebuild (`bash build.sh`, exit 0) and
   confirm the built tree contains every anchor token exactly once per
   file: `CASBERRY_F22` in `skills/motion-foundations/SKILL.md`,
   `skills/motion-patterns/SKILL.md`, `skills/ui-ux-pro-max/SKILL.md`,
   `skills/design-taste-frontend/SKILL.md`,
   `skills/polish-pass/reference/slop-checklist.md`; `ORIGINKIT_F22` in
   `skills/motion-patterns/SKILL.md`, `skills/ui-ux-pro-max/SKILL.md`,
   `skills/design-taste-frontend/SKILL.md`; `DAISYUI_F22` in
   `skills/ui-ux-pro-max/SKILL.md`, `skills/design-system/SKILL.md`,
   `skills/design-taste-frontend/SKILL.md`.
2. Confirm counts: no new skill, no new command, no new trigger key
   from this patch spec (rules and pointers only).
3. Confirm the staged Taste edit (L17-05) and the staged polish-pass
   edits (L17-06, L17-07) survive the rebuild unchanged, and that the
   wave-1 / §11 / §15 texts in those files (TRENDS_F22, DIRECTIVES_F22,
   MOBBIN_PATTERN_F22, VANTA_F22, R3F_F22, LIQGLASS_F22, SHADERGRAD_F22,
   LIQLOGO_F22, WEBGL_ONE_F22) are untouched.
4. Confirm banned terms are 0 in the built tree (case-insensitive)
   after the rebuild.
5. Confirm the fix #19/#20/#21 font rules, the screen-verdicts rule,
   and the model pins are untouched by this spec (no entry touches
   them).
6. Confirm the one-WebGL rule now counts Casberry exports (L17-06
   replace visible in the built slop-checklist) and the export-review
   check exists (L17-07 section).
7. verify22.py additions (for the coordinator): each of the three
   recorded in its placements with pinned versions/terms; Casberry's
   terms status recorded (explicitly unresolved) + the trust flag
   recorded + the export-review step present; OriginKit's 10/day cap +
   Pro-marked exclusion + the Origin UI distinction recorded; daisyUI
   5.x + Tailwind v4 pairing pinned; dedupe vs React Bits (§11) and vs
   shadcn recorded; the one-WebGL rule extended to Casberry exports.
   Dry-run fixtures (SPEC §17): (a)–(f) — the exact check phrases are
   in Report §9.

---

# Report — fix #22 §17 (3 more libraries/tools)

## 1. Deliverable

`fix22/libraries17-patches.md` (this file): patch specs L17-01–L17-07 +
this report. No plugin file was edited, `build.sh` was not run, `fix22.py`
and `verify22.py` were not edited.

## 2. Live-verified versions + licences + terms + caps (all checked 2026-11-13, do not take the SPEC's expectations as verified)

| Item | Site / repo | Pinned / recorded | Licence / terms (verified live) | Source of verification |
|------|------------|-------------------|--------------------------------|------------------------|
| Casberry (particles.casberry.in) | https://particles.casberry.in/ | **No version pin** — hosted tool, no npm package, no repo. Pin = tool URL + export step. SPEC's "v2.0.0 Oct 2026" NOT re-verified (no version string surfaced on the site in this session) and is NOT recorded as a pin. | **Terms UNRESOLVED** — no terms or licence statement found on the site (homepage crawl 2026-11-13) or via search. Exported effects are NOT assumed free for commercial use. **Trust flag CONFIRMED:** ScamAdviser trust score **1/100** (WHOIS hidden, iframed, "may be a scam", last update 7 months ago). Counter-signal recorded: Gridinsoft 60/100, no major malware/phishing detections. The flag is a weak automated signal, NOT a verdict — but the export-review step stands regardless. Mitigating fact (from the site's own prompt text, crawled): the tool's validator REJECTS generated code containing `document`, `window`, `fetch`, `XMLHttpRequest`, `eval`, `Function(`, `import(`, `localStorage`, `setTimeout`, etc., and dry-runs it before accepting — that lowers the risk of a hostile export but does NOT replace the plugin-side review. | Site homepage crawl (2026-11-13 00:56 UTC): "AI Particle Simulator", 20,000+ particle swarm, single-snippet JS function body, `target`/`color` write-only API, `addControl` sliders; search: ScamAdviser check page (score 1, WHOIS hidden, iframed), Gridinsoft review (60/100, no malware), Reddit r/threejs post (export to HTML, "use anywhere else"), novitckii guide ("Export production-ready React or Three.js code in seconds", "100% Free, No sign-up required"). |
| OriginKit (originkit.dev) | https://www.originkit.dev/ | **No version pin** — browsable library, no npm package. Binding constraint = 10/day cap + env-only key. | **CONDITIONAL / source-available — NOT a clean open-source licence.** Terms restrict redistribution of components and templates (Design Atlas review, 2026-09-27: "Conditional licence, source available… The terms restrict redistribution of components and templates; check their current conditions before reuse"). No terms page surfaced on originkit.dev itself in this session — the restriction is recorded per the Atlas review of the terms, not per a fresh read of the terms page (see §8 A2). | Site homepage crawl (2026-11-13 00:56 UTC): hero "Discover **805 Components**". Pricing page (crawled 4 days ago): Pro $144 struck → **$79/year**, Component Copy Limit 25/Day; Ultimate **$99/year**, no limit (fair use); footer "60 components, 2,671 examples". vellum-ai/originkit README + SKILL.md: "Daily limit: **10 component fetches per key, resets at midnight UTC**", shared between MCP and website copies; key from originkit.dev > Settings > API Integration (`cmp_live_...`); MCP server `https://mcp.originkit.dev/mcp` (JSON-RPC, bearer auth). Skill README: "50 animated components across 6 categories: interactive elements, image galleries, text effects, animations, background animations, buttons". Logiaweb toolkit guide: 547 in the gallery (backgrounds 190, interactive 80). |
| daisyUI (daisyui.com) | https://github.com/saadeghi/daisyui | **`daisyui@5.7.50` (exact)**; pair: Tailwind CSS v4 ONLY. | **MIT** (jsDelivr "Version 5.7.50 License MIT"; GitHub Releases; daisyui.com comparison pages "MIT License Open source"). Repo ~42.8k stars. | GitHub Releases (crawled 4 days ago): **v5.7.50 Latest**, released Oct 13 2026 (`bf3bac3`), `npm i -D daisyui@5.7.50`. jsDelivr npm/daisyui page: "Version 5.7.50 License MIT", updated 2026-10-13. Homepage crawl (2026-11-13): "68 components", "Pure CSS. Framework agnostic. Works everywhere", install `npm i -D daisyui@latest` + `@import "tailwindcss"; @plugin "daisyui";`, "Create a custom theme for yourself using daisyUI theme generator". Install skill: "You must use Tailwind CSS 4 with daisyUI 5". Blueprint MCP: paid ($22/mo, licence key + email per SPEC + pacyfist.dev — NOT wired). |

### Count discrepancy — OriginKit (resolved as SPEC directed: record, don't pick)

Four different counts surfaced live, all newer than or equal to the
SPEC's three: homepage hero **805** (Nov 13, 2026 crawl — the freshest
site fact), skill README **50 across 6 categories** (vellum-ai/originkit
— the count the agent-facing docs still carry), pricing-page footer
**60 components, 2,671 examples**, and a third-party guide's **547 in
the gallery**. The patch texts record the spread verbatim (L17-02) and
forbid citing any count as exact — the 6 categories are the stable
fact, the count is not. The SPEC's "82 (July 2026)" did not resurface
in this session and is superseded by the four above.

### Casberry version note

The SPEC's "v2.0.0 Oct 2026 (v1.0.0 Feb 2026)" could not be re-verified:
the homepage crawl shows no version string, and no changelog/releases
page surfaced. Since Casberry is a hosted tool with no installable
artifact, there is nothing to pin a version TO — the pin is the tool
URL + the export step, and the version claim is left out of the patch
texts entirely (neither asserted nor denied).

### Origin UI distinction — verified independently

originui.com **301-redirects to https://coss.com/ui** (coss ui, built
on Base UI `@base-ui/react`); it is a solid form/layout-primitives
library (button, input, nav, card shells, ~55 component families).
OriginKit (originkit.dev) is a DIFFERENT product (animated flourishes).
Two independent sources confirm the split and explicitly warn not to
confuse them (ai-design-lab SOURCES.md: "https://www.originkit.dev/ is
a *different* product (Originkit — animated flourishes). Do not confuse
them."; site-director registry-catalog.md, live finding 2026-07-15).
The distinction check is in L17-02 and L17-05 with the exact FAIL
phrase (Report §9, fixture (e)).

### MCP endpoint note — OriginKit

The Vellum plugin docs give the MCP server as
`https://mcp.originkit.dev/mcp` (matching the SPEC); the same repo's
README also mentions `https://mcp.originkit.dev/vellumai`, and a
third-party guide lists a REST registry at
`https://mcp.originkit.dev/v1/registry`. Which path is canonical is
UNRESOLVED — and moot for the plugin, because the default is
copy-paste and no MCP wiring is done (L17-02 states this). Flagged for
the coordinator (see §8 A3); do not wire MCP until the endpoint + the
env-only key flow are verified live.

## 3. Edit points (with file:line evidence)

| Patch | File | Edit point | Evidence |
|-------|------|-----------|----------|
| L17-01 | `skills/motion-foundations/SKILL.md` | build.sh fix22 patch block (no staged source; same as LIB-01/L15-01) | Built tree `hackathon-ecc/skills/motion-foundations/SKILL.md:87-89` — A11 block verbatim (anchor verified count==1). |
| L17-02 | `skills/motion-patterns/SKILL.md` | build.sh fix22 patch block (no staged source; same as LIB-02/LIB-07/L15-02) | Built tree `hackathon-ecc/skills/motion-patterns/SKILL.md` — `## End-to-End Example` count==1 (`grep -c` = 1). |
| L17-03 | `skills/ui-ux-pro-max/SKILL.md` | build.sh fix22 patch block (no staged source; same as LIB-03/L15-03) | Chained anchor = L15-03's inserted caveat tail (`libraries15-patches.md:303-307`: "…the plugin records the caveat and proceeds / on the declared MIT. Install … The Figma plugin's paid Pro / tier is out of scope — the npm library is the integration, and it is free."). The LIB-03 paragraph tail it chains from is count==1 in the built tree (`grep -c "library effect is applied only when it matches the dealt theme"` = 1). |
| L17-04 | `skills/design-system/SKILL.md` | build.sh fix22 patch block (no staged source; ECC upstream — frontmatter `origin: ECC`; same convention as ui-ux-pro-max / motion-*) | Built tree `hackathon-ecc/skills/design-system/SKILL.md` (82 lines) — Output line `Output: \`DESIGN.md\` + \`design-tokens.json\` + \`design-preview.html\`` count==1. Build.sh embeds the skill via patch lists (e.g. `build.sh:22426`, `22634`, `22679`, `23380`) and assembles it in STEP 2; the fix22 runtime block patches the built tree, so the built-tree anchor is the correct one (same as the LIB patches). |
| L17-05 | `new-skills/design-taste-frontend/SKILL.md` | STAGED source, direct edit (same as LIB-05 / L15-05 / L15-07) | Staged file line 127: `- **One object never carries the page.** …` count==1; Vanta bullet already applied at staged line 126 (`VANTA_F22`). |
| L17-06 | `round2-skills/polish-pass/reference/slop-checklist.md` | STAGED source, direct edit (same as L15-08) | Chained anchor = L15-08's flag-list fragment (`libraries15-patches.md:497-501`, 2-space continuation indent, em dash before "any two of"). Staged file is currently 484 lines with no `WEBGL_ONE_F22` yet (L15-08 not yet applied). |
| L17-07 | `round2-skills/polish-pass/reference/slop-checklist.md` | STAGED source, direct edit (same as L15-08) | Chained anchor = L15-08's section tail (`libraries15-patches.md:528-530`: "…effects per surface in the static check; Colors: none — the check counts / effects, it chooses no colours."). |

## 4. Dedupe notes (one concept, one home)

| Pair | Resolution (recorded in the patches) |
|------|--------------------------------------|
| Casberry vs Vanta (§11) vs React Three Fiber (§15) | Vanta = the imported 3D-background LIBRARY for a known effect; Casberry = the TOOL that exports Three.js code for a bespoke particle scene; React Three Fiber = the React 3D layer the exported React code can feed + the layer for hand-built React scenes. Recorded in L17-01 (primary home: `motion-foundations`). |
| OriginKit vs React Bits (§11) | React Bits = the importable MIT library (copy-paste source at a pinned commit); OriginKit = the browsable catalog for animated flourishes (backgrounds, cursor treatments, text effects, buttons, loaders) fetched by copy-paste or MCP. Reach for React Bits for a pinned, importable bit; for OriginKit to browse a catalog for a flourish. Recorded in L17-02 (primary home: `motion-patterns`). OriginKit components are IMPLEMENTATIONS of motion patterns — the pattern stays the authority. |
| daisyUI vs shadcn | shadcn (`shadcn@4.23.0`, pin at `build.sh:21712`) = the React copy-paste component set; daisyUI = the Tailwind-native component library (semantic classes, zero JS, any framework). Reach for daisyUI on Tailwind-native builds wanting semantic-class components; for shadcn on React builds wanting the copy-paste set. Recorded in L17-04 (primary home: `design-system`). |
| daisyUI vs design-system primitives | The primitives in `design-system` stay the authority; daisyUI is the menu item, never the source of the primitives. Recorded in L17-04. |
| OriginKit vs Origin UI | DIFFERENT products (see §2). OriginKit = animated flourishes (originkit.dev); Origin UI = solid form/layout primitives (originui.com → coss ui / Base UI). The distinction check is in L17-02 + L17-05. |
| Casberry vs liquid-logo (§15) | Same integration FORM (standalone tool, export step, never a runtime dependency) — different output (particle scene vs animated brand mark). L17-01 cites liquid-logo as the form precedent, without duplicating its rule. |

## 5. One-WebGL-heavy-effect-per-surface rule — extended to Casberry

The §15 rule (L15-08, `WEBGL_ONE_F22` in the polish-pass slop
checklist) counts R3F scenes, Vanta scenes, ShaderGradients, liquid
glass, and liquid metal. L17-06 extends the counted list with "a
Casberry particle export" by a `replace` on the flag bullet, so a
surface carrying a Casberry export + any other WebGL-heavy effect
FAILS the check, and a surface with one theme-matched Casberry export
+ static fallback PASSES. L17-01 / L17-02 / L17-05 state the same
extension in the per-library rules (by name, without repeating the
`WEBGL_ONE_F22` token — it already lives in those files via L15).
No clearance exists for two effects on one surface (same as §15).

## 6. Bundled vs install-on-demand (per item)

Existing convention followed (same as `fix22/libraries-report.md` §4
and `fix22/libraries15-patches.md` §6: plugin-script deps are
exact-pinned in the repo-root `package.json` + `package-lock.json` and
installed with `npm ci`; clone sources are pinned to SHAs; CBM binary
is NOT bundled; `puppeteer-core` is install-only at a pinned version):

| Item | Decision | Reason |
|------|----------|--------|
| daisyUI (`daisyui@5.7.50`) | **Install-on-demand, per project** (exact pin in the project's package.json + lockfile; `npm i -D daisyui@5.7.50`) | A build's CSS dependency, not a plugin-script dependency. The plugin never loads daisyUI itself. Versioned CDN (`https://cdn.jsdelivr.net/npm/daisyui@5.7.50`) is the non-npm alternative — same exact pin, never `@5` floating. |
| OriginKit | **Copy-paste fetch, no install** (default path; MCP NOT wired) | No package exists to install. The fetch is capped (10/day) and key-gated; the plugin records the cap + the env-only key rule instead of a version. |
| Casberry | **Standalone tool, no install** (run the hosted tool, output is exported code only) | No package, no repo. The plugin never imports it; the build ships the reviewed export + the static fallback. |

**Security note (how checked):** daisyUI's pin is a standard
supply-chain pin (npm package, MIT, exact version verified live on
GitHub Releases + jsDelivr). OriginKit's key is env-only (same rule as
the ElevenLabs narration key — verified to exist in the plugin at
`hackathon-ecc/skills/orch-build-mvp/SKILL.md:32`: "the key is an env
var only and is never written to any file"). Casberry exports are
reviewed as untrusted code (trust flag + unresolved terms recorded in
L17-01 and enforced by the L17-07 checklist section).

## 7. Decisions made

1. **Patch format is 6-tuples** `(id, rel, old, new, mode, token)` —
   verified by reading `fix22.py` (the task's "5-tuples" description
   does not match the file; the L15 spec flagged the same discrepancy
   and the coordinator maps the 6th element the same way). Token =
   the `_F22` anchor string in `new_text`.
2. **L17-06 / L17-07 are staged direct edits, not `fix22.py`
   patches** — because their anchors are L15-08's inserted text,
   which does not exist in the current built tree (L15-08 not yet
   applied). Routing them through `fix22.py` would need a
   rebuild-then-preflight round-trip; the staged route (same as
   L15-08 itself) keeps the dependency inside the staged file, where
   the coordinator applies L15-08 first. If the coordinator prefers
   the `fix22.py` route, L17-06's token must be `"a Casberry particle
   export"` (see the summary-table note) — never `WEBGL_ONE_F22`.
3. **Casberry version is NOT pinned or asserted.** The SPEC's "v2.0.0
   Oct 2026" did not resurface live; a hosted tool has no installable
   artifact to pin. The pin is the URL + the export step.
4. **OriginKit count is recorded as a spread, never as one number**
   (805 / 50 / 60 / 547 — see §2). Patch texts forbid citing a count
   as exact.
5. **No MCP wiring for OriginKit.** The endpoint path is not settled
   (§2) and the env-only key flow is unverified; copy-paste is the
   only wired path. Wiring MCP is a future deliberate decision, not
   part of this fix.
6. **No new skill / command / trigger key.** All seven patches are
   rules, pointers, and checklist sections in existing skills.
7. **D19 + theme-match on every patch text** (each insert carries its
   D19 block and theme-match precondition, per PARENT-GUIDANCE.md).
   The §13 seventh D19 dimension (Depth) is NOT restated in these
   patch texts — the §13 work is a separate subagent's scope; the
   D19 blocks here use the standing six-dimension form, with Depth
   covered where it applies inside Motion/Visuals (particle scenes
   are depth moments). Flagged, not silently changed (see §8 A4).

## 8. Items needing coordinator / parent adjudication

- **A1 — Casberry terms unresolved.** No terms/licence statement was
  found on the site or via search as of Nov 13, 2026. The patches
  record "terms unresolved" and forbid assuming commercial use is
  free. If the parent wants a harder line (e.g. Casberry exports
  barred from commercial/shipped builds until terms are confirmed),
  that is a one-line change to L17-01/L17-07 — say so; the current
  text permits use after review, with the unresolved status recorded.
- **A2 — OriginKit terms not re-read from the site.** The
  redistribution restriction is recorded per the Design Atlas review
  (2026-09-27) of the terms, because no terms page surfaced on
  originkit.dev in this session. If the coordinator can reach the
  terms page directly, confirm the restriction verbatim and update
  the manifest; the patch texts do not quote terms language, so no
  patch change is needed either way.
- **A3 — OriginKit MCP endpoint path unsettled** (`/mcp` vs
  `/vellumai` vs `/v1/registry`). No action needed now (copy-paste
  is the default); resolve only if MCP wiring is ever proposed.
- **A4 — D19 Depth dimension (§13).** These patch texts use the
  standing six-dimension D19 form. If the §13 coordinator lands the
  seventh Depth dimension before these patches apply, the D19 blocks
  in L17-01/L17-02/L17-05 (particle scenes are depth moments) should
  gain an explicit Depth line — a mechanical follow-up, flagged here
  rather than pre-empted.
- **A5 — Casberry v2.0.0 not re-verified.** If the coordinator finds
  a version string on the site, record it in the manifest; no patch
  text needs it (no installable artifact).

## 9. Dry-run fixture check phrases (SPEC §17 verification — exact phrases the fixtures judge against)

| Fixture | Expected | Exact check phrase(s) in the patch texts |
|---------|----------|------------------------------------------|
| (a) Casberry export, one-WebGL rule + review | PASS | "The export is the surface's one WebGL-heavy effect" (L17-01, L17-02) + "reviewed as untrusted code before it enters the build" (L17-02) + "the exported snippet reviewed line by line" (L17-07). A surface with one theme-matched Casberry export + static fallback PASSES (L17-06 list + L17-07 "Justified use"). |
| (b) Build needing >10 OriginKit fetches/day | Hits cap gracefully | "DAILY LIMIT: 10 component fetches per key per day, resets midnight UTC" + "proceed from the skills alone, record the gap, never pay for Pro ($79/yr) or Ultimate ($99/yr)" (L17-02, L17-03, L17-05). |
| (c) daisyUI component, default theme unexamined | FAIL | "A build shipping daisyUI's default theme unexamined FAILS" (L17-04, L17-05). |
| (d) daisyUI component re-themed to the brand deal | PASS | "re-themed through the brand / theme deal" (L17-04, L17-05) + "The design package chooses the direction; daisyUI supplies prebuilt components that get re-themed" (L17-04, L17-05). |
| (e) Origin UI confused with OriginKit | FAIL | "A build citing Origin UI when it means OriginKit (or vice versa) FAILS the distinction check" (L17-02, L17-05). |
| (f) Casberry export pasted without review | FAIL | "a Casberry export pasted without review FAILS the security check" (L17-01) + "A build pasting exported code blind FAILS the security check" (L17-07). |

## 10. Coverage re-verification (word-boundary greps over build.sh, 2026-11-13)

| Term | Count in build.sh | Note |
|------|-------------------|------|
| `daisyui` | 0 | New. |
| `daisyUI` | 0 | New. |
| `daisy` | 0 | New (substring check; no false positives to clear). |
| `originkit` | 0 | New. |
| `OriginKit` | 0 | New. |
| `origin-kit` | 0 | New. |
| `casberry` | 0 | New. |
| `particles` (word-boundary, `-w`) | 0 | New — per the substring-grep lesson, `-w` was used ("particles" as a generic word appears nowhere even so). |
| `Particles` | 0 | New. |
| `CASBERRY_F22` / `ORIGINKIT_F22` / `DAISYUI_F22` | 0 in build.sh, 0 in the built tree, 0 in `new-skills/` and `round2-skills/` | All three tokens new (checked across `hackathon-ecc/`, `build.sh`, `new-skills/`, `round2-skills/`). |

Related pins confirmed in place (not touched by this spec):
`shadcn@4.23.0` at `build.sh:21712`. LIB tokens already in build.sh
(LENIS_F22: 3, GSAP_F22: 2, SCROLLTRIGGER_F22: 3, VANTA_F22: 2,
REACTBITS_F22: 3 — §11 applied). L15 tokens still 0 everywhere
(R3F_F22, LIQGLASS_F22, SHADERGRAD_F22, LIQLOGO_F22, WEBGL_ONE_F22 —
§15 patches not yet applied; the Ordering dependencies in this file
assume they land first where chained).
