# Fix #25 SPEC — One more turn of iterations and improvements, then verify everything is called, weaved, and works

## §0 Origin

Anish, Nov 13, 00:50 CST: "Now do another turn of iterations and
improvements to turn this plugin up a notch, and then check to make sure
everything is called and weaved and works."

Fix #24 made the plugin coherent and Cursor-native. This fix raises the
bar one notch — real improvements, not more text — and then proves the
whole thing is CALLED (every part is actually invoked), WEAVED (the
weaving holds end-to-end), and WORKS (the loops pass, including a
call-graph leg).

## §1 Called — the call map

- Build the call map: every skill, agent, rule, command, hook, and
  trigger key, and where it is invoked from. The map lives as a durable
  file (next to the inventory, e.g. `references/call-map.md` in
  orchestrate, staged + built) and is kept current by the same change
  that adds or removes an element — same currency rule as the inventory.
- Every entry must be reachable from the flow (grill → design package →
  build → verify → polish → deploy → commit → README → final report, or
  an explicit on-request path like /demo). Anything uncalled is either
  WIRED IN (a real dispatch path is added) or recorded as intentionally
  dormant WITH its reason. No orphaned skills. No dead dispatch paths.
- The map's counts must agree with the tree (166 skills / 72 agents /
  123 rules / 87 commands / 15 hooks / 64 trigger keys, or the manifest
  justifies a change).

## §2 Weaved — the weaving holds end-to-end

- Re-verify the fix #24 coherence as the baseline and tighten what the
  call map exposes: every decision routes through a named skill; the
  design package runs on every UI surface; the inventory is read BEFORE
  deciding; no off-skill improvisation path exists in the built tree.
- The design-package flow reads as one story (fix #24 §1c). Any step
  the call map shows as bypassable gets its bypass closed or its reason
  recorded.

## §3 Works — the loops, plus a call-graph leg

- Full loop: Audit (ZERO) → sweep (CLEAN, weaving CLEAN) → dry-run
  (PASS) → verify25.py (exit 0) → manifest.
- Dry-run gains a **call-graph leg (Leg 5)**: fixtures that exercise
  each dispatch path in the call map — every command, every on-request
  skill, every hook that can fire statically — and report any path that
  does not execute. A path that cannot execute in the sandbox is
  recorded as OWED to the live smoke test, never claimed.
- The persistent environmental /demo FAIL (Leg 3, sandbox Chrome can't
  reach fonts.gstatic.com) is addressed by §4(b). If the self-host clears
  it, the dry-run goes 59/59; if it cannot be cleared in the sandbox,
  record honestly what remains owed.

## §4 Improvements — up a notch

- (a) **Authorized verifier updates (parent-authorized at the fix #24
  close — the exception to "prior verifiers are NOT edited", only these
  two):** S1 — styles.csv header 80 → 89 (csv is the source) with the
  verify23 assertion updated in the same change; verify13h M3
  expectations updated for the F-04 rename (the two checks at :57,63).
  Record both in the manifest with the before/after tails.
- (b) **Template-fonts self-host (decided at the fix #22 close,
  follow-up fix):** the pitch-deck-video template stops fetching Google
  Fonts live at render time (@remotion/google-fonts) and self-hosts its
  fonts, like the rest of the plugin. Must not break the /demo contract
  (runtime under 2:10 hard / 2:30 absolute, local-only filming, $10
  budget cap, voice fallback chain). If the self-host clears the Leg 3
  environmental FAIL, say so with the evidence.
- (c) **Coordinator's highest-leverage improvements** from the call/weave
  audit: the weakest surfaces the Home Run lessons exposed, tightened
  where the call map shows a gap. Bounded: no new skill unless the
  manifest justifies it; no re-litigation of fixes #14–#24 adjudications;
  THE CORE, "more, not bolder", the frozen texts, and the /demo gates
  stand.
- (d) **Design bar: beat Campus Eats v5.** The design package must now
  generate designs BETTER than the previous Campus Eats iteration (v5:
  61 elements literal, Sticker theme, hero deal `centred`, letters-
  assemble + iris-opens moments, motion/interactivity +10–15% over v4;
  record at `~/workspace/cold-start-render/campus-eats/`). "Better" is
  measured on the recorded dimensions — element count AND variety,
  hero strength, motion, dynamic interface, functionality, alignment —
  not count alone. Raise the floor: a build that would have scored like
  v5 is now BELOW the bar. The dry-run's design leg benchmarks against
  the v5 record and the re-traced design must beat it on those
  dimensions, or the gap is recorded as owed.
- (e) **Technical depth: hard ideas get hard builds.** The build engine
  must code technically impressive and challenging projects from just an
  idea the user states. Strengthen the scope/expansion/implementer
  briefs and verification for technical substance: real architecture,
  real algorithms and data structures, system design, performance
  budgets, edge cases — not a thin demo that happens to run. A hard idea
  must not be quietly re-scoped down to an easy one; if scope is cut,
  the decision record says what was cut and why.
- (f) **Intelligent, adaptive, creative — in design AND substance.**
  The orchestrator and design-lead adapt to the idea (its domain, its
  constraints, how much the user specified — a vague one-liner gets
  reasoning and gap-filling, a big prompt gets execution), and the
  expansion proposes substantively creative features and technical
  approaches, not just more UI. Creativity applies to what the product
  DOES, not only how it looks. The decision record shows the reasoning:
  what was inferred, what was chosen, what was rejected.

## §5 Verification criteria

- Audit #72 (or next number): ZERO blocking, ZERO minor.
- Sweep (next number): CLEAN, weaving-coherence CLEAN for the whole tree.
- Dry-run (next number): PASS — Leg 1 fixtures, Leg 2 render re-run
  (incl. the Campus Eats v5 benchmark from §4(d): the re-traced design
  must beat v5 on the recorded dimensions), Leg 3 /demo, Leg 4
  Cursor-readiness, Leg 5 call-graph (incl. a technical-depth check from
  §4(e): a hard-idea fixture whose build must show real architecture and
  algorithmic substance).
- verify25.py: checks for every placement, exit 0. It also codifies the
  prior-verifier tails after §4(a): fix22 366/369 (unchanged), fix23's
  tail as re-measured after the S1 assertion update (record the new
  codified tail — the S1 fix may move it back toward 212).
- Prior verifiers: re-run; fails must be only the codified tails
  (frozen fingerprint + less-flat-ui hunks + cascades + the §4(a)
  updates). No regressions.
- Banned terms: 0 in the built tree. Counts and pins unchanged unless
  the manifest justifies a change.
- Manifest: fix25/MANIFEST.md, written by a script, with the disposition
  table, the call-map location, the anchor tokens, the open parent
  adjudications, and the dry-run caveat if any check is
  environment-limited.

## §6 Non-goals

- Do not re-litigate fixes #14–#24 adjudications (slop = flags, trends =
  menu, /demo gates, Casberry bar, APCA informational, THE CORE, the
  inventory, C2/C3 scope splits, FILM_F1/F5/F6).
- Do not rewrite frozen verifier-asserted texts — except the two
  authorized §4(a) updates, and only those.
- Do not pre-decide the smoke test's live questions. Make the plugin
  robust + clear, and let the smoke test decide.
- No bundle, no commit, no push.
