# MANIFEST-A — Fix program #13, fixer A (ORCHESTRATION CORE)

Patch script: `~/workspace/hackathon-plugin/fix13/fix13-orchestrate.py` (run; idempotent — a second run reports all 21 hunks ALREADY and exits 0).
No rebuild done. No zip/upload. `build.sh`, `~/workspace/hackathon-plugin-repo/`, and the bundle untouched. No fixer-B file touched (polish-pass, ui-ux-pro-max, design-taste-frontend, less-flat-ui, motion skills, design-system, inherit-legacy-style — read-only for anchor verification).

## 0. Anchors verified before patching (all matched exactly once)

- Orchestrate row-10 carve-out: `new-skills/orchestrate/SKILL.md:85` — "A mechanical, fully-specified UI component slice whose design is already fixed by the design system does NOT match this row…" — confirmed present, now removed (post-patch grep count 0).
- Team table: `:24–27`; step 3 integration-in-brief: `:55`; step 4 TDD-in-brief: `:56`; design-system handoff: `:140`; fallback pins: `:145`; blind reviewer: `:175–178`; visual loop: `:182`; Hallmark audit "(landing/company pages only)": `:184`.
- dispatch-prompt.md skeleton item 5: `:19–21` ("ONLY when the custom roster injected a skill…").
- feature-expansion `:145` UI rule ("Name the skill in the brief"), `:60` Lens D, `:189` reference-table UI row.
- hackathon-scope `:43` wow test; grill-me step 5 `:38` (decision-record finalisation).
- design-taste-frontend `:234` theme deal, `:240` log `--entry`, `:242` tokens writer, `:53` captivating-hero bar (read-only; fixer B owns the file).
- ui-ux-pro-max `:14` captivating bar, `:89` anti-generic bar (read-only; fixer B owns the file — referenced by name only).
- sloplint: `--scope app` exists (usage line, `sloplint.mjs:27` area); `APP_SKIP` at `:798–799` includes `32`; `:905` `if ((opts.scope === 'app' || APPSCREEN) && appSkip(g)) return;`; gates.md §1 line 14: gate 32 is "Ledger. Bookkeeping about repetition (32). Reports at NOTE, never counts toward the verdict." **Therefore sloplint app scope cannot carry the distinctiveness check — the check lives in the visual loop + blind reviewer instead (see A9b/A8/A10b). This is stated in the patched text, not papered over.**

## 1. Changes (staged file:line, post-patch)

### `new-skills/orchestrate/SKILL.md`
- **:28 (A1)** — Team table: new `design-lead` row, model `grok-4.7-high`.
- **:56 (A2)** — Step 3 Slice: "Design package in every UI slice brief" — names components per surface (landing: Taste + dealt Hallmark theme + ui-ux-pro-max + Impeccable via polish-pass + Harmony; app/dashboard/components: ui-ux-pro-max + Impeccable via polish-pass + Harmony + less-flat-ui where dull/flat; motion: + make-interfaces-feel-better; new design-system: + design-system; legacy drift: + inherit-legacy-style); direction recorded BEFORE UI is built; a UI brief with no named components and no recorded direction is not ready to dispatch.
- **:57 (A3)** — Step 4 Build: "Design package in every UI brief" beside the TDD-in-every-brief sentence.
- **:57 (A4)** — Step 4 Build, wave order: **Grok 4.7 High picker instruction** (see §2).
- **:86 (A5a)** — Row 10: carve-out CLOSED. Relevance is by SURFACE TYPE, never by size; every UI touch matches row 10 (landing, dashboard/app, single component, small UI fix, redesign, one-prompt change rebuilding a surface). "Already fixed" only changes which design work is left (minimum: ui-ux-pro-max direction check + Harmony check); the only non-match is non-UI mechanical work (pure backend/logic, no visual surface).
- **:86 (A5b)** — Row 10 route cell: design skill leads on model `grok-4.7-high` (slug form only).
- **:88 (A5c)** — New "Design-package rule (row 10)" paragraph: full per-surface component map, direction recorded in `docs/design-tokens.md` before building (landing: dealt Hallmark theme slug + Tokens; app: ui-ux-pro-max direction — theme/axes/mood, named, never "modern clean"); small changes, one-prompt changes, redesigns, UI fixes, and removal flows that rebuild a surface are UI slices under this rule and record direction in the decision record / run ledger (lightest-weight record that exists for that flow).
- **:143 (A6)** — Design-system handoff: "Direction recorded before building" — every UI brief records its `Design direction:` line + components before any UI is built.
- **:148 (A7)** — Fallback pins: design-lead tier `grok-4.7-high` (slug form only — never bracket syntax, never `effort=xhigh`; Grok 4.7 takes per-vendor `reasoning_effort=xhigh`, which Cursor does not expose in a pin, so the pin is the slug alone).
- **:181 (A8)** — Verify step 2 blind reviewer: design-distinctiveness scope on UI diffs (finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as default template; routes to the capped fix loop).
- **:185 (A9a/A9b)** — Verify step 5 visual loop: enumerates the app's key screens/routes (every primary route, not just "key pages") and applies the **distinctiveness bar that can FAIL** — captivating/wow test (hackathon-scope wow test, feature-expansion Lens D, Taste captivating-hero bar) + anti-generic bar; bar = "a named direction is recorded AND visibly applied (tokens, type, colour, spacing decisions trace to it)" — **no numeric score**. FAIL = finding, minor at least, routed to the fix loop within existing caps (max 3 rounds, 2 fix rounds per problem list).
- **:187 (A10a/A10b)** — Verify step 6 retitled "Hallmark audit (landing/company pages) + app-screen design audit": new "App screens (every build, landing or not)" paragraph — runs sloplint `--scope app` on the primary screens, fixes every `FAIL`, fixes/waives every `REFLEX`, `--json` counts into the Verify fix list; states explicitly that app scope does NOT carry distinctiveness (APP_SKIP skips gate 32, NOTE-only) and the distinctiveness check lives in step 5 + step 2 instead. On a no-landing build this IS the step-6 design audit; on a landing build both run.
- **:277 (A11)** — Final report: new "Design direction applied" bullet (named direction, components per surface, Verify distinctiveness outcome).

### `new-skills/orchestrate/references/dispatch-prompt.md`
- **:24 (B1)** — Skeleton item **5a**: "Design package — named by default on every UI dispatch (not custom-roster-only)" — same per-surface component map + direction restated inline from `docs/design-tokens.md`, never "see the design system". A UI dispatch with no named design skill is incomplete.
- **:177–182 (B2)** — Blind-reviewer template: `[UI diff:]` constraints block with the distinctiveness bar.

### `new-skills/grill-me/SKILL.md`
- **:38 (C1)** — Step 5 finalisation: the decision record carries one `Design direction:` line (theme/axes/mood, named from the brief's mood/domain); if the user said nothing about look/feel, record the stated default as an assumption (marked assumed, not user-stated) — never leave the line blank.

### `rewritten-skills/hackathon-scope/SKILL.md`
- **:48 (D1)** — `docs/scope.md` contents: design direction copied from the record's `Design direction:` line; if missing, record the stated default as an assumption in `docs/scope.md`, never blank.

### `new-skills/feature-expansion/SKILL.md`
- **:145 (E1)** — UI rule extended to the full design package (ui-ux-pro-max + less-flat-ui + Impeccable via polish-pass + Harmony; landing: design-taste-frontend leads with the dealt Hallmark theme, ui-ux-pro-max + Impeccable + Harmony still apply); brief names components and records direction BEFORE UI is built, "however small".
- **:189 (E2)** — Reference-table UI row updated to match.

## 2. Grok pin + picker instruction locations

Pin `grok-4.7-high` (slug form only, NO bracket syntax anywhere — verified: `grep -rn "grok-4.7\[" new-skills/ rewritten-skills/` returns nothing):
- `new-skills/orchestrate/SKILL.md:28` — team table, design-lead row.
- `new-skills/orchestrate/SKILL.md:86` — row-10 route cell ("design skill leads on model `grok-4.7-high`").
- `new-skills/orchestrate/SKILL.md:148` — fallback pins, design-lead tier (+ the `reasoning_effort=xhigh` / no-`effort=xhigh` note).
- Picker instruction: `new-skills/orchestrate/SKILL.md:57` (step 4, wave order — where the design role is first invoked in the first build): "Select **Grok 4.7 High** in Cursor's model picker before the first build, or the design pin may silently fall back to another model… File-level pin only — the live smoke test decides whether the pin holds; do not claim it is verified working." It is a pre-build setup note, not a mid-build ask; it never pauses the build and adds no user question or approval gate.
- Cost note (not a blocker): "High" is a reasoning effort, not a price tier — higher effort burns the Cursor weekly usage pool faster.

**Not claimed as verified working.** No frontmatter/agent-definition pin was added: there is no design-lead agent definition file in the staged tree, and per bounds no new agent was created — the design-lead is a roster row + fallback pin, dispatched as a general subagent with the dispatch-prompt role preamble (the existing fallback mechanism). The live smoke test decides whether the pin holds.

## 3. Exclusion-note draft (for the coordinator to place if it belongs in a file fixer A doesn't own)

> **Design-adjacent skills deliberately NOT wired into the UI design package.** `gan-style-harness` — Claude Code only: it drives the `claude` CLI and does not run in Cursor, so it cannot lead design in a Cursor first build. `frontend-design-direction` — production UI outside hackathons; its own description forbids hackathon use. Direction lenses + `live` / `generate` — decided out Nov 10. `loop-design-check` and `api-design` — not UI design (`loop-design-check` is a loop/process check; `api-design` is API design), so neither belongs in the UI design package. If any of these is later wanted, that is a new decision, not an oversight in this fix.

## 4. Held back, with reasons

- **orch-build-mvp standalone flow + orch-change-feature + orch-pipeline Verify extension (task §4d/§6): NOT patched in staged files — no staged sources exist.** These three skills come from upstream ECC (`$ECC_SRC`) and are patched only via `build.sh`-embedded `audit_patch`/`qc_patch` blocks (build.sh:5983–6029, 6029–6075, 6127–6234, 9594–9622, 9622–9654, 9688–9794). I did not touch build.sh. Exact coordinator patch text is in §5 below — append LAST before STEP 5, after verifying each anchor against the built tree. Note: `qc_patch` reverts the `ecc-` agent prefixes to plain names (`security-reviewer`, `code-reviewer`), so the §5 anchors use the **post-qc** (plain) text.
- **sloplint `--scope app` as the distinctiveness carrier: HELD BACK — it cannot do it.** `--scope app` exists, but `APP_SKIP` (sloplint.mjs:798–799, applied at :905) skips gate 32 and other page gates in app scope, and gate 32 is NOTE-only bookkeeping anyway (gates.md §1: "never counts toward the verdict"). The distinctiveness check is therefore placed in the visual loop + blind reviewer, and the patched step-6 text says so explicitly. Do not claim a sloplint app-scope pass proves distinctiveness.
- **No numeric distinctiveness score** — per task; the bar is recorded-direction-AND-visibly-applied, a finding (minor at least) on failure.
- **No new skills/agents/rules/commands** — no gap needed one; design-lead is a roster row + fallback pin (see §2).
- **No new approval gates, wait points, or user questions** — the picker instruction is a pre-build setup note; §7 auto-approval, the deferred-six §3/§7 carve-out, auto-expansion/auto-approval, CBM phrasing, direction lenses/live-generate, and frontend-slides untouched. No supply-chain pins or SSML truth touched.
- **`commands/orchestrate.md` unchanged** — thin wrapper, no pins or routing of its own; all routing lives in the skill.

## 5. Coordinator patch block (exact text — append LAST before STEP 5 in build.sh)

Anchors verified against build.sh audit_patch/qc_patch pairs (post-qc built-tree text). Coordinator: verify each anchor against the built tree before applying; if an anchor doesn't match, stop that hunk and report it.

```python
# Fix program #13, fixer A — design package + Grok pin for the orch-* pipelines
# (orch-build-mvp / orch-change-feature / orch-pipeline have no staged sources;
#  they are upstream ECC patched here). Placement: LAST, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import sys
base = sys.argv[1]
subs = [
  # orch-build-mvp: design package + Grok pin on every UI slice (step 5).
  ("skills/orch-build-mvp/SKILL.md",
   r'''3. Stop at **Gate 1** (slice plan) and **Gate 2** (pre-commit). Commit the
   scaffold and each slice as separate `feat:` commits.
4. Add `security-reviewer` for any slice touching a security trigger.''',
   r'''3. Stop at **Gate 1** (slice plan) and **Gate 2** (pre-commit). Commit the
   scaffold and each slice as separate `feat:` commits.
4. Add `security-reviewer` for any slice touching a security trigger.
5. **Design package on every UI slice (relevance by surface type, never by size).** Every slice that touches a UI surface names its design components in its brief and records its direction in `docs/design-tokens.md` before building UI (landing: `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony; app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; motion: + `make-interfaces-feel-better`; new design-system work: + `design-system`; legacy drift: + `inherit-legacy-style`). The design role runs on model `grok-4.7-high` (slug form only — never bracket syntax; select Grok 4.7 High in Cursor's model picker before the first build, or the pin may silently fall back — file-level pin only, the live smoke test decides). Small changes, one-prompt changes, redesigns, and UI fixes are UI slices under this rule. Verify the built app's primary screens against the distinctiveness bar — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template — within the existing fix caps.'''),
  # orch-change-feature: UI change / rebuild-a-surface rule (step 5).
  ("skills/orch-change-feature/SKILL.md",
   r'''1. Run the `orch-pipeline` engine with the settings above.
2. Keep the plan light — only `standard`+ size warrants the full planning pass.
3. Stop at **Gate 1** (plan / changed-test approval) and **Gate 2** (pre-commit).
4. Add `security-reviewer` if the change touches a security trigger.''',
   r'''1. Run the `orch-pipeline` engine with the settings above.
2. Keep the plan light — only `standard`+ size warrants the full planning pass.
3. Stop at **Gate 1** (plan / changed-test approval) and **Gate 2** (pre-commit).
4. Add `security-reviewer` if the change touches a security trigger.
5. **UI change / rebuild-a-surface rule.** If the change touches UI — including a one-prompt change, a redesign, or a removal that rebuilds a surface — it is a UI slice under the design-package rule (orchestrate SKILL.md row 10): name the applicable design components in the brief (app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing: `design-taste-frontend` + dealt Hallmark theme; motion: + `make-interfaces-feel-better`), record the direction in the decision record / run ledger (the lightest-weight record that exists for this flow — one line, a stated default from the brief's mood/domain if silent, marked assumed) and in `docs/design-tokens.md` where the flow keeps one, and run the applicable package components before the change lands. The design role runs on model `grok-4.7-high` (slug form only). Verify the rebuilt surface against the distinctiveness bar (named direction recorded AND visibly applied; a finding, minor at least, when it carries no named direction, no applied theme/tokens, or reads as a default template) within the existing fix caps. Pure backend/logic changes with no visual surface are exempt.'''),
  # orch-pipeline step 5 Review: distinctiveness scope on UI diffs.
  ("skills/orch-pipeline/SKILL.md",
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below).''',
   r'''- **5. Review** — `code-reviewer` agent / `/code-review`. Add `security-reviewer`
  whenever the diff touches a security trigger (below). On any diff that touches a UI surface, the reviewer ALSO judges the built screens against the distinctiveness bar (orchestrate SKILL.md Verify step 5): a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it) — a finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template.'''),
  # orch-pipeline Verification: UI / design-package / distinctiveness line.
  ("skills/orch-pipeline/SKILL.md",
   r'''- `security-reviewer` ran iff a security trigger was touched''',
   r'''- `security-reviewer` ran iff a security trigger was touched
- UI work (if any): the design package was named in the brief, the direction is recorded, and the distinctiveness bar passed or its findings were fixed within the caps (finding, minor at least, when screens carry no named direction, no applied theme/tokens, or read as a default template)'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    assert t.count(old) == 1, f"anchor mismatch (x{t.count(old)}) in {rel}"
    open(p, "w").write(t.replace(old, new, 1))
print("fix13-A orch-pipeline block applied")
PYEOF
```

## 6. Verification greps run

- `python3 fix13/fix13-orchestrate.py` → first run 20/21 (B1 anchor mismatch — see §7), fixed, re-run 21/21; third run 21/21 ALREADY (idempotent, exit 0).
- Marker-count check (each hunk's added text counted in its file): **ALL SINGLE — 21 markers ×1**.
- `grep -rn "grok-4.7-high" new-skills/orchestrate/ new-skills/grill-me/ new-skills/feature-expansion/ rewritten-skills/hackathon-scope/` → 4 hits, all in `new-skills/orchestrate/SKILL.md` (:28, :57, :86, :148).
- `grep -c "no design decision is left, so design leadership is not the question" new-skills/orchestrate/SKILL.md` → **0** (old carve-out gone); the only remaining "does NOT match this row" is the new non-UI-mechanical sentence (:86).
- `grep -rn "grok-4.7\[" new-skills/ rewritten-skills/` → none (no bracket syntax).
- `grep -n "Design direction:" new-skills/grill-me/SKILL.md rewritten-skills/hackathon-scope/SKILL.md` → grill-me :38, hackathon-scope :48.
- `grep -n "full design package" new-skills/feature-expansion/SKILL.md` → :145, :189.
- `grep -n "5a. **Design package" new-skills/orchestrate/references/dispatch-prompt.md` → :24; `[UI diff:]` → :177.
- build.sh untouched (never written; md5 `215270e157c4a0e3e4985e45c185460c`, mtime predates this fix). No rebuild, no zip/upload, repo/bundle untouched.

## 7. Incidents during this fix (for the record)

- **B1 anchor transposition (first run: 20/21).** The B1 old-anchor had the closing `"` and backtick transposed after `SKILL.md` (anchor `md"\`` vs file ``md`"``). Fixed the two occurrences in the script (old + new text of B1) by code-point comparison; B1 then applied. No guessing: the hunk was skipped, not forced.
- **Double application on re-run (second run).** Append-style hunks re-applied because their old anchor survives inside the new text. 12 doubles were collapsed back to singles with a dedupe pass (B1 had only ever applied once, so 12 is the correct count). The script's idempotency check now tests for the NEW text first (the only safe check for append-style hunks); a third run reports all 21 ALREADY and the marker-count check confirms ALL SINGLE.
