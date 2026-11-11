# MANIFEST-B — Fixer B, fix program #13: DESIGN-PACKAGE COMPONENTS

Patch script: [fix13/fix13-package.py](sandbox:/workspace/hackathon-plugin/fix13/fix13-package.py)
Run: `python3 fix13/fix13-package.py` — exit 0, **20/20 hunks applied**, 0 skipped.
No rebuild, no zip/upload, no repo/bundle touch, no build.sh edit.

## 0. Anchor verification (done before patching; all confirmed in the files)

- Harmony exists only at `round2-skills/polish-pass/SKILL.md:13` plus a "color harmony"
  cell in `hackathon-ecc/skills/ui-ux-pro-max/data/styles.csv` — parent-verified claim holds.
- ui-ux-pro-max built-tree anchors: captivating bar (`SKILL.md:14`), Step 2 define-before-UI
  (`:87`), anti-generic bar (`:89`), `--motion` feel/timing line (`:133`) — all present;
  ZERO hits for "Hallmark" or "theme" in the skill; quality table (:21–32) breakage-only.
- Taste staged: Hallmark theme deal + `log --entry` + tokens writer (step 4a), sloplint,
  hero review, finish review — all present.
- Impeccable wiring confirmed: detector + craft floor `SKILL.md:88–89`, critique trigger
  `reference/polish.md:19`, onboard/extract `reference/polish.md:40` — all kept.
- polish-pass IS invoked on app screens (orchestrate step 5b `:59`, read-only check).
- Motion skills: `make-interfaces-feel-better` named once in ui-ux-pro-max (`:133`);
  `motion-foundations/patterns/advanced`, `design-system`, `inherit-legacy-style` named
  NOWHERE in ui-ux-pro-max and NOWHERE in staged `new-skills/`, `new-rules/`,
  `round2-skills/`, `rewritten-skills/` — genuine invocation gap, closed below.
- hackathon-mode staged (`new-rules/hackathon-mode.mdc` §2/§5) already pairs
  ui-ux-pro-max + less-flat-ui and routes motion feel→`make-interfaces-feel-better`,
  HOW→motion-* — but hackathon-mode.mdc is fixer A's file; not touched.
- **Correction to the brief:** the less-flat-ui "recording rule (:72)" does NOT exist.
  `~/workspace/cursor-skills/less-flat-ui/SKILL.md` has ZERO hits for "record" /
  "design-tokens" (485 lines). A recording rule was ADDED (L2) instead of edited.
- less-flat-ui staged source located: `~/workspace/cursor-skills/less-flat-ui/SKILL.md`
  (build.sh:258 copies it fresh into the plugin on every build — that file IS the staged source).

## 1. Changes applied (staged file:line, post-patch line numbers)

### 1a. `round2-skills/polish-pass/SKILL.md`
- **H1 — :24.** Generic-template diagnosis is now a FINDING routed to the design skill:
  "record it as a generic-template FINDING in the report … so the orchestrator routes
  it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing
  page) for a redesign within the existing caps; it stays listed under
  'Still short of 10/10' until that redesign lands." (Was: report-only note.)
- **H2 — :20–22.** Harmony rule strengthened in place (no harmony skill invented):
  new "### The harmony check — runs on every pass" subsection. Executed check on every
  pass: read recorded direction (`docs/design-tokens.md` first lines, or
  `design-system/<project-slug>/MASTER.md`; infer + record if neither exists), then per
  primary screen (1) consistency of tokens/type/color/spacing/radii vs the direction,
  (2) direction-application (screen visibly traces to the named direction). Per-screen
  pass/fail recorded in the report under "Harmony check". States explicitly there is no
  standalone harmony skill.
- **H3 — :85.** First-build paragraph: look-that-is-the-problem is now "recorded as a
  generic-template finding for the orchestrator to route back to the design skill (and
  listed under 'Still short of 10/10' until redesigned), not redesigned here."
- **H4a/H4b — :92.** Craft-floor reads required on EVERY pass: "before judging or editing
  on every pass — score-only passes and small fixes included", for both craft floors.
- **H5a/H5b — :93.** Detector runs required on EVERY pass: "on the target's source files
  on every pass — edit passes, score-only passes, and small fixes alike". Fallback KEPT
  (detector cannot run → record and proceed on the other detector's findings, never
  block). New close: "never block, never silently skip" — the only excuse is no source
  available (recorded). The skip path that existed was the score-only row (H6) plus the
  "edited or critiqued" scoping; both are closed.
- **H6 — :33.** Score-only row now requires the harmony check + both detector reads when
  source is available (record it when not).
- **H7 — :96.** New non-negotiable 7: "Run the harmony check" on every pass.
- **Preserved for build.sh patch (f):** all four of its hard-assert anchors are byte-identical
  after patching — description line ("a new look belongs to ui-ux-pro-max and less-flat-ui,
  not this skill."), harmony-rule sentence ("The plugin already has `ui-ux-pro-max` and
  `less-flat-ui` for design direction and surface treatments. Those skills own the look."),
  "If the user asks for a new look outright…" sentence, and the When-to-use table row.
  Verified count==1 each after patching (see §5).

### 1b. `round2-skills/polish-pass/reference/polish.md`
- **P1 — :18.** Step 2 detector step runs on every pass incl. score-only + small fixes.
- **P2 — :24.** New Step 2 item 7: the harmony check as an executed step (read direction,
  per-screen consistency + direction-application, per-screen pass/fail for the report,
  generic-template failure = finding routed to the design skill).
- **P3 — :20.** Generic-template diagnosis (Level 2 template, 3+ vibe-code tells, or
  Persona-fit cap from the generic look) is a FINDING with per-screen evidence.
- **P4 — :35.** Below-Level-6 baseline: finding routed to the design skill within existing
  caps (orchestrator routes); still listed under "Still short of 10/10" until redesigned.
- **P5 — :31.** New Step 3 bullet: systemic drift → **design-system finding** routed to
  the `design-system` skill (tokens to `design-tokens.json`, 10-dimension score) via the
  orchestrator; polish-pass does not run a design-system audit itself.
- **P6 — :76–83.** Report template gains "### Harmony check" table and
  "### Generic-template findings" section (before "### Accepted detector findings").
- **P7 — :7.** Lenses intro: redesign is a routed generic-template finding, not just a note.
- Critique trigger (:19) and onboard/extract (:40) untouched and still wired.
- polish-pass still never restyles: every new routing sentence says the finding goes to
  the design skill and the orchestrator routes it.

### 1c. `round2-skills/polish-pass/reference/scoring.md`
- **S1 — :55.** After the generic-AI-template Persona-fit cap: "A generic-template
  diagnosis is a FINDING routed to the design skill for a redesign (polish.md Step 3),
  not only a score cap — record which screens fail and how." Cap itself unchanged.

### 1d. `new-skills/design-taste-frontend/SKILL.md`
- **T1 — :241 (step 4a motion item).** One-line addition only: motion beyond the page
  system's own entrance/moments (e.g. interactive app-frame widgets in React/Next.js)
  → decide feel/timing with `make-interfaces-feel-better` first, then implement with
  `motion-foundations` / `motion-patterns` / `motion-advanced`.
- **No other Taste change.** Trace showed no gap: theme deal + `log --entry`, tokens
  writer (first two lines = dealt Hallmark theme), sloplint, hero review, finish review
  all verified present. Scope NOT widened to dashboards/apps (frontmatter forbids it).

### 1e. `~/workspace/cursor-skills/less-flat-ui/SKILL.md` (durable source; build copies it)
- **L1 — :14.** "Check every surface, on every UI build or change" — first build,
  one-prompt change, redesign, small component, UI fix, removal flow that rebuilds a
  surface. A fitting treatment is REQUIRED where a surface is dull/flat and text stays
  readable (4.5:1); left flat only for a listed Do NOT case (dense dashboard/form/data
  table, strong brand background, photo-led design, treatment fights content) — stated
  in one line. "Never skip the check because a surface is small."
- **L2 — :482–484.** NEW "## Record what you applied" section (the brief's :72 rule did
  not exist): record every treatment per surface in `docs/design-tokens.md` (Treatments
  list; "none — <Do NOT reason>" for deliberately flat surfaces), so the polish-pass
  harmony check can verify the texture layer. Never rewrite the direction line at the
  top of `docs/design-tokens.md`.

## 2. Runtime patch block — ui-ux-pro-max (EXACT TEXT, for coordinator)

ui-ux-pro-max is fetched fresh from upstream on every build — NO staged copy was edited.
Append this block LAST before STEP 5 (after all existing build.sh patches), so its anchors
match the post-prior-patch text. Every `old` was verified `count == 1` in the CURRENT built
tree (`hackathon-ecc/skills/ui-ux-pro-max/SKILL.md`, re-verified after patching — see §5).
The quality table (:21–32) is untouched, as briefed.

```bash
# --- fix13-B: ui-ux-pro-max — named direction record + enforced anti-generic /
# captivating bars + related-skill routing (motion-*, design-system, legacy) ---
python3 - "$PLUGIN_DIR/skills/ui-ux-pro-max/SKILL.md" <<'PYEOF'
import sys
p = sys.argv[1]
text = open(p, encoding="utf-8").read()
subs = [
  (
    "This is a pre-UI step, not an approval gate: define it, then build.",
    "This is a pre-UI step, not an approval gate: define it, then build. **Name the direction in the record:** the first lines of `design-system/<project-slug>/MASTER.md` — and of `docs/design-tokens.md`, which you write from it when there is no landing slice — must carry the NAMED direction (the theme slug and its axes/mood, or the named style + axes from the `--design-system` output), never a bare \"modern clean\" or an unnamed search result, so any later slice can recover which direction the UI traces to.",
  ),
  (
    "if nothing is memorable, the surface fails even if every other check passes.",
    "if nothing is memorable, the surface fails even if every other check passes. Enforced fail criterion (the brief names the anchor; Verify checks it as pass/fail): after closing the page, a user can describe that one anchor — its form and what it showed — without reopening it. If no anchor can be named, the surface FAILS.",
  ),
  (
    "if a surface looks like a default template, it fails even if every checklist item passes.",
    "if a surface looks like a default template, it fails even if every checklist item passes. Enforced fail criteria (the brief and Verify check these as pass/fail against the recorded named direction): (1) Direction trace — every primary screen visibly traces to the named direction recorded in MASTER.md / `docs/design-tokens.md`; a screen that could belong to any product fails. (2) Memorable anchor — the primary view carries the one unmistakable anchor from the captivating bar above; if no anchor can be named, the surface FAILS. (3) Not a default template — a surface that looks like a default template fails even if every checklist item passes.",
  ),
  (
    "Do not use `--motion` to make a feel/timing decision on its own.",
    "Do not use `--motion` to make a feel/timing decision on its own.\n\n**Related-skill routing.** Motion implementation in React/Next.js goes to the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`) — but only after feel/timing is decided with `make-interfaces-feel-better` (above). New design-system work, or a consistency audit of an existing UI, goes to the `design-system` skill (tokens to `design-tokens.json`, 10-dimension score) — its output becomes the MASTER.md / `docs/design-tokens.md` record, not a second competing system. On a hand-written legacy codebase, run `inherit-legacy-style` before writing UI, so new work follows the codebase's own conventions instead of drifting from them.",
  ),
]
for old, new in subs:
    assert text.count(old) == 1, f"ui-ux-pro-max fix13-B anchor not found exactly once: {old[:60]}"
    text = text.replace(old, new)
open(p, "w", encoding="utf-8").write(text)
print("ui-ux-pro-max patched (fix13-B: named direction + enforced bars + routing)")
PYEOF
```

No other upstream-fetched skill needs a runtime patch block: the motion-*/design-system/
inherit-legacy-style routing is wired through this ui-ux-pro-max block, through Taste T1,
and through the polish-pass design-system finding (P5). Their own descriptions already
route feel→`make-interfaces-feel-better` first (motion-*) / describe their trigger
(design-system, inherit-legacy-style); the gap was that no first-build flow file NAMED them,
which this block closes from the design-skill side. Invocation from orchestrate /
hackathon-mode is fixer A's side (see §4).

## 3. Exclusion-note draft (for the coordinator to place)

Suggested placement: hackathon-mode §5 (UI routing) or the plugin README skill inventory,
as a short "Design skills NOT used" note. Draft text:

> **Design skills NOT used in hackathon builds.** `gan-style-harness` is Claude Code only —
> it drives the `claude` CLI and does not run in Cursor, so it is never invoked here.
> `frontend-design-direction` sets design direction for production UI outside hackathons —
> its own description forbids hackathon use; hackathon UI direction belongs to
> `design-taste-frontend` (full landing/company pages), `ui-ux-pro-max` (dashboards/apps/
> components), and `polish-pass` (fixes to existing UI). Direction lenses and the
> live/generate modes were decided out on Nov 10 — the lenses pick a new visual direction,
> which clashes with `polish-pass`'s never-restyles rule, and live variants need an
> interactive browser session that cannot run in an unattended build. `loop-design-check`
> and `api-design` are not UI design skills and are not wired into any UI flow.

## 4. Held back, with reasons

- **No harmony skill invented.** Harmony is the rule at polish-pass SKILL.md:13, now an
  executed check (H2/P2/H7). No new skill/agent/rule/command was created anywhere.
- **No Taste scope change.** Deal + writers + reviews verified present; frontmatter forbids
  dashboards/apps and app direction belongs to ui-ux-pro-max.
- **Orchestrate row 10 carve-out, hackathon-mode §2/§5, feature-expansion UI rule:**
  fixer A's files — NOT touched. The "force the FULL design package on ANY UI creation"
  pin at the routing layer lives there; my files make the package itself enforceable
  (named direction, pass/fail bars, required texture check, harmony check, detector runs)
  once invoked. If fixer A does not close the row-10 carve-out, mechanical slices can
  still escape ui-ux-pro-max at the router even though the skills now enforce the bars.
- **design-system / inherit-legacy-style invocation from orchestrate/hackathon-mode:**
  left for fixer A; wired from my side only via the ui-ux-pro-max patch block and the
  polish-pass design-system finding (P5).
- **Scoring cap not extended.** The generic-AI-template cap stays Persuade-only (:55);
  only finding-routing was added (S1). Extending the cap to Operate/Read would change
  scoring behaviour beyond the brief.
- **No new approval gates, wait points, or user questions** added anywhere (§7 preserved).
- **fix11/fix11-stage.py NOT re-run;** `reference/impeccable-critique.md` untouched
  (fix-#12 edits preserved). Deferred-six §3/§7 carve-out, auto-expansion/auto-approval,
  CBM phrasing, direction lenses/live-generate, frontend-slides untouched. Supply-chain
  pins and SSML truth untouched.

## 5. Verification greps run (all after patching)

```bash
cd ~/workspace/hackathon-plugin
python3 fix13/fix13-package.py            # exit 0, 20/20 hunks applied
# build.sh patch (f) anchors still count==1 in round2-skills/polish-pass/SKILL.md:
#   f1-desc, f2-harmony, f3-ask, f4-row — all count= 1
grep -n "harmony check\|Harmony check\|generic-template FINDING\|generic-template finding\|Generic-template findings\|Run the harmony check\|score-only passes and small fixes\|never silently skip\|design-system finding\|Record what you applied\|Check every surface" round2-skills/polish-pass/SKILL.md round2-skills/polish-pass/reference/polish.md round2-skills/polish-pass/reference/scoring.md ~/workspace/cursor-skills/less-flat-ui/SKILL.md
grep -n "make-interfaces-feel-better" new-skills/design-taste-frontend/SKILL.md   # :241
grep -n "generic-template diagnosis is a FINDING" round2-skills/polish-pass/reference/scoring.md  # :55
grep -n "impeccable-critique\|impeccable-onboard\|impeccable-extract" round2-skills/polish-pass/reference/polish.md round2-skills/polish-pass/SKILL.md  # critique :19, onboard/extract :40 — still wired
# ui-ux-pro-max patch-block anchors in built tree hackathon-ecc/skills/ui-ux-pro-max/SKILL.md:
#   B1 pre-UI sentence, A3 captivating tail, A2 anti-generic tail, A4 --motion tail — all count= 1
```

Files changed by this fixer (nothing else): `fix13/fix13-package.py` (new),
`round2-skills/polish-pass/SKILL.md`, `round2-skills/polish-pass/reference/polish.md`,
`round2-skills/polish-pass/reference/scoring.md`,
`new-skills/design-taste-frontend/SKILL.md`,
`~/workspace/cursor-skills/less-flat-ui/SKILL.md`. No rebuild, no repo/bundle touch.
