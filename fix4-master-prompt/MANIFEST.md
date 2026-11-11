# MANIFEST — Master-prompt integration, fix program #4 (upstream ECC only)

Snippets in this dir are build.sh patch blocks in the exact `fix4-patches/E-ui-ux-pro-max.py`
format (comment header + `python3 - "$PLUGIN_DIR" <<'PYEOF'` heredoc, `subs` list,
`assert text.count(old) == 1` per substitution). The coordinator inserts each block
LAST, just before STEP 5, after the GATE / carve-out / Batch E / Batch F /
fix-program-#3 patches — so every anchor below was verified against the CURRENT built
text (post-all-earlier-patches). As with the E-format blocks, each anchor sentence is
preserved inside its replacement, so each block runs exactly once per build.

Tested 2026-11-10: each snippet applied cleanly to a copy of the current built file in
`/tmp/mp-test/` (all asserts passed, `diff` shows pure additions only, no other lines
touched). The built plugin (`hackathon-ecc/`) was NOT modified. `build.sh` was NOT
edited (another step applies these snippets).

## 1. MP-ui-ux-pro-max.py — SNIPPET WRITTEN

- Target (in-build path): `skills/ui-ux-pro-max/SKILL.md`
- Upstream proof: cloned fresh every build from `github.com/nextlevelbuilder/ui-ux-pro-max-skill`
  (`build.sh` :228-230). Not in any staging dir (`new-skills/`, `round2-skills/`,
  `rewritten-skills/`, `new-rules/` — checked, absent).
- Anchor verified against current built file, line 85 (Step 2, "Generate Design System"):
  `This aggregates product/style/color/typography matches, applies reasoning rules from
  ui-reasoning.csv, and returns pattern, style, colors, typography, effects, and
  anti-patterns to avoid.`
  (Post-patch form: build.sh :14861-14862 changed the upstream "landing" wording to this;
  no later patch touches this line. The Batch E captivating bar is elsewhere, :14, no conflict.)
- What was added (inserted after line 85, lands at :87-89 in the test copy):
  - Pre-UI design-system definition checklist: before writing UI code, record in
    `design-system/<project-slug>/MASTER.md` — visual identity; typography + type scale;
    color palette + semantic tokens; spacing/layout system; component hierarchy;
    navigation/IA; responsive behavior; motion/microinteractions; accessibility; loading /
    empty / success / error states for every data surface. Values reused from the
    `--design-system` output and `references/quick-reference.md`. Stated as a pre-UI step,
    not a gate.
  - Anti-generic bar: avoid generic AI-dashboard aesthetics (excessive gradients,
    repetitive same-size cards, decorative clutter); distinction via deliberate typography,
    spacing, alignment, contrast + the captivating-bar anchor.
- ALREADY COVERED (not duplicated — quoted):
  - Design-system generation itself: `### Step 2: Generate Design System (REQUIRED for new
    pages/projects)` (:77) + `--design-system` aggregation (:85).
  - Individual values, scattered but present: type scale — `references/quick-reference.md`
    §6 `` `font-scale` - Consistent type scale (e.g. 12 14 16 18 24 32) `` (:119); semantic
    tokens — priority table row 6 "Semantic color tokens" (SKILL.md :~29) and
    `references/pro-rules.md` "Token-driven theming"; spacing — `--density` spacing scale
    (SKILL.md :127) and quick-reference §5 `` `spacing-scale` ``; hierarchy — quick-reference
    §5 `` `visual-hierarchy` ``; navigation — priority table row 9; responsive — priority
    table row 5; motion — priority table row 7; accessibility — priority table row 1 +
    quick-reference §1; states — quick-reference §2 `` `loading-buttons` `` /
    `` `error-feedback` ``, §3 `` `progressive-loading` `` (skeleton screens), §6
    `` `contrast-feedback` `` (error/success colors), §8 `` `submit-feedback` `` (loading then
    success/error) and `` `empty-data-state` `` (:236).
  - Captivating/memorable bar: Batch E addition, SKILL.md :14 ("**Captivating bar for
    dashboard/app surfaces:** the primary view must have one unmistakable visual anchor…").

## 2. MP-browser-qa.py — SNIPPET WRITTEN

- Target (in-build path): `skills/browser-qa/SKILL.md`
- Upstream proof: copied fresh from the ECC Developer install every build
  (`build.sh` :85 `cp -r "$ECC_SRC/skills/."`). Not in any staging dir (checked, absent).
- Anchor verified against current built file, lines 63-67 (end of Phase 3 + Phase 4 heading):
  ```
  3. Flag layout shifts > 5px, missing elements, overflow
  4. Check dark mode if applicable
  ```

  ### Phase 4: Accessibility
  ```
  (Earlier patches touching this file — Batch F Gap 42b on Phase 1 smoke checks, Batch C on
  the Debugging-order section and the report template, audit_patch on the trailing
  Integration section — touch none of these lines.)
- What was added (new section between Phase 3 and Phase 4, lands at :67-70 in the test copy):
  - Visual iteration loop: run the app (local dev server or staging/preview URL), inspect the
    ACTUAL rendered interface with Playwright (desktop + mobile viewports), never from source
    or description alone; each round judge typography, hierarchy, spacing, alignment, color,
    contrast, responsiveness; list the FIVE most noticeable visual/usability problems; fix
    them; re-inspect. Returns the top-5 problem list each round; the caller caps rounds
    (max 3, then note diminishing returns and move on) — no second cap invented here.
  - "Never claim visual verification without actually inspecting the rendered interface."
- ALREADY COVERED (not duplicated — quoted):
  - Screenshots at 3 breakpoints + baseline comparison: `### Phase 3: Visual Regression`
    (:58-65): "1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)" (:60),
    "— no baseline ⇒ report INCONCLUSIVE, never a silent PASS" (:62).
  - Desktop + mobile screenshots in Phase 1 (:42, "Screenshot above-the-fold on desktop +
    mobile viewport"). These are capture/comparison steps, not the design-judgement +
    top-5 + fix + re-inspect loop — that loop was missing and is what the snippet adds.

## 3. MP-code-reviewer.py — SNIPPET WRITTEN

- Target (in-build path): `agents/ecc-code-reviewer.md` — NOT `skills/code-reviewer/SKILL.md`.
  That skill path does not exist in the plugin: code review lives in the AGENT
  `agents/ecc-code-reviewer.md` (upstream ECC, agents copied from the install at
  `build.sh` :106-111). This snippet targets the agent file instead. No file was created.
- Upstream proof: ECC Developer install copy (build.sh :106-111). Not in any staging dir
  (checked, absent).
- Anchor verified against current built file, line 16:
  `You are a senior code reviewer ensuring high standards of code quality and security.`
  (Earlier patches touching this file — audit2 frontmatter `tools:` removal, audit10
  large-files line and file-size guideline — touch none of this line.)
- What was added (inserted after line 16, lands at :18-21 in the test copy):
  - Adversarial stance: review as a skeptical staff engineer reading someone else's
    implementation; assume every claim is unproven until code, callers, or a test proves it;
    hunt across all checklist categories for incorrect assumptions, functional bugs, security
    vulnerabilities, broken user journeys, race conditions, state-management problems,
    unhandled edge cases, performance bottlenecks, accessibility failures, duplicated /
    unnecessary code, fragile integrations, missing validation, inadequate tests. Fix root
    causes, not symptoms; re-run tests after fixes.
  - CONFIRMED vs SUSPECTED: label every finding CONFIRMED (traced to a concrete failing
    input/state/outcome) or SUSPECTED (plausible risk, name the repro/test that would confirm
    it); never present SUSPECTED as CONFIRMED; SUSPECTED never blocks on its own; the
    Pre-Report Gate still decides whether it is reported at all.
- ALREADY COVERED (not duplicated — quoted):
  - Severity classification: summary table "``| CRITICAL | 0 | pass |``" (:281) and
    "## Approval Criteria" (Approve / Warning / Block by CRITICAL/HIGH) — NOT re-added.
  - Confidence filter: "Only report issues you are confident about (>80% sure it is a real
    problem)" (:26); "Report if you are >80% confident it is a real issue" (:32).
  - Proof bar: "### HIGH / CRITICAL Require Proof" and the four-question Pre-Report Gate.
  - Most hunt areas already in the checklist (security, unvalidated input, state updates in
    render / stale closures, N+1, performance, dead code, missing tests). What was genuinely
    missing: any "skeptical"/"adversarial" framing (zero matches in the file) and explicit
    naming of race conditions and accessibility failures (zero matches in the file) — added
    as stance prose only, no new checklist sections.

## 4. security-reviewer — CHECKED, NO SNIPPET

- The named path `skills/security-reviewer/SKILL.md` does not exist; the real file is the
  upstream ECC agent `agents/ecc-security-reviewer.md` (install copy, build.sh :106-111).
- Checked and deliberately left alone: the adversarial stance belongs in code-reviewer, not
  here — this agent is security-only (OWASP Top 10, secrets, injection, SSRF, unsafe crypto)
  and already carries its own stance: "**Remember**: Security is not optional. One
  vulnerability can cost users real financial losses. Be thorough, be paranoid, be
  proactive." (:116), plus its own severity table in "### 3. Code Pattern Review"
  (CRITICAL / HIGH / MEDIUM). Adding the general-review hunt list here would duplicate
  code-reviewer's scope into a security-only agent.

## Deliberately dropped (conflicting with the goal)

- Any plan-approval gate / "present the plan and wait for approval" step — dropped; none
  of the three snippets adds a gate or wait point. The ui-ux-pro-max addition explicitly
  says "This is a pre-UI step, not an approval gate: define it, then build."
- Any "ask the user" / "confirm with the user" step — dropped; none added. (The
  ui-ux-pro-max `--force` rule requiring explicit user authorization is pre-existing
  upstream text, untouched.)
- Any new agent / skill / file — dropped; all three snippets patch existing upstream files
  only. The `skills/code-reviewer/SKILL.md` and `skills/security-reviewer/SKILL.md` paths
  from the task brief do not exist; the correct upstream targets are the
  `agents/ecc-*.md` files, and only `ecc-code-reviewer.md` got a snippet.
- A second visual-loop round cap in browser-qa — dropped per brief; the procedure states
  the caller (orchestrate) caps rounds at max 3.
- The full master-prompt text — not pasted anywhere; each snippet is a short concrete
  addition in its file's own voice.

## Unanchorable / staged targets

- None. All three anchors were found exactly once in the current built files and all three
  snippets applied cleanly to /tmp copies. No target turned out to live in a staging dir.
