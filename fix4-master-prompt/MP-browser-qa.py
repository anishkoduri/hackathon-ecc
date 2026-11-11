# Master prompt (fix program #4): browser-qa — visual iteration loop
# procedure (run the app, inspect the ACTUAL rendered interface, top-5
# problems, fix, re-inspect).
# Upstream ECC file, copied fresh from the ECC Developer install on every
# build — this fix lives here as a patch block placed LAST — just before
# STEP 5 — after the GATE / carve-out / Batch E / Batch F / fix-program-#3
# patches, whose old-strings the substitution below is anchored on (i.e.
# against the CURRENT built text).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
#
# What it adds, and what it deliberately does NOT duplicate:
# - Phase 3 (:58-65) already screenshots key pages at 3 breakpoints and
#   compares against a baseline, and Phase 1 already screenshots desktop +
#   mobile. What was missing was the ITERATION LOOP itself: judging the
#   rendered UI on design grounds (typography, hierarchy, spacing,
#   alignment, color, contrast, responsiveness), naming the FIVE most
#   noticeable visual/usability problems, fixing them, and re-inspecting —
#   plus the rule never to claim visual verification without actually
#   inspecting the rendered interface. Added here as a new section between
#   Phase 3 and Phase 4.
# - The loop CAP (max 3 rounds, then note diminishing returns and move on)
#   is enforced by the caller (orchestrate) — this procedure states the
#   per-round procedure and that the caller caps rounds; it does not invent
#   a second cap. Interface agreement: the procedure returns the top-5
#   problem list each round.
# - No approval gate, no wait point, no new agent/skill/file.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Master prompt — visual iteration loop: run the app, look at the real
  # rendered UI, fix the five most noticeable problems, re-inspect.
  ("skills/browser-qa/SKILL.md",
   r'''3. Flag layout shifts > 5px, missing elements, overflow
4. Check dark mode if applicable
```

### Phase 4: Accessibility''',
   r'''3. Flag layout shifts > 5px, missing elements, overflow
4. Check dark mode if applicable
```

### Visual iteration loop (run the app, look at the real UI)

Run the app (local dev server, or staging/preview URL) and inspect the ACTUAL rendered interface with Playwright — desktop + mobile viewports — never from source code or a description alone. Each round: capture screenshots, then judge the rendered UI on typography, hierarchy, spacing, alignment, color, contrast, and responsiveness; list the FIVE most noticeable visual/usability problems; fix them; re-inspect. Return the top-5 problem list each round so the caller can decide whether to run another round — the caller caps rounds (max 3, then note diminishing returns and move on). Never claim visual verification without actually inspecting the rendered interface.

### Phase 4: Accessibility'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("master-prompt browser-qa visual iteration loop applied")
PYEOF
