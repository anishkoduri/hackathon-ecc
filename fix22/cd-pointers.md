# Fix #22 Groups C+D — pointer specs (cd-pointers.md)

Patch specs for the integrator. These pointers live in skills that are
**build.sh-embedded** — do NOT edit the built tree (`hackathon-ecc/`) directly
and do NOT edit `build.sh` by hand in this file's scope; the integrator applies
each spec to the embedded copy in `build.sh` (the built-tree path is given so
the anchor can be found and verified, and the anchor text below is copied
verbatim from the built tree, which mirrors `build.sh`).

Each spec gives: target file (built-tree path), the exact anchor text copied
verbatim with enough context to be unique (verified: each anchor occurs exactly
once in its file), the full new pointer text, and where it goes relative to the
anchor. The `ui-ux-pro-max` H1 concept pointer (`ACCENT_F22`) and the
orchestrate / `ui-ux-pro-max` H2 hierarchy rules belong to the Groups A+B agent
— they are NOT in this file.

## P1 — D9 specific headlines → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 110.
- **Anchor (verbatim, unique):**
  `- \`visual-hierarchy\` - Establish hierarchy via size, spacing, contrast — not color alone`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`headline-specific\` - Headlines name the specific outcome or value (what it does, for whom, to what end), not a generic claim; a vague headline is fixed in polish-pass (UNSLOP_F22 D9 — Make headlines specific), never by restyling here (fix #22)`
- **Why here:** `visual-hierarchy` is the closest owning rule (headlines carry
  hierarchy); the headline-specificity wording itself lives in polish-pass
  `UNSLOP_F22` D9 — this pointer routes to it, it does not duplicate it.

## P2 — D10 CTA emphasis → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 91.
- **Anchor (verbatim, unique):**
  `- \`primary-action\` - Each screen should have only one primary CTA; secondary actions visually subordinate (Apple HIG)`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`cta-emphasis\` - The one primary CTA is emphasized by size, weight, fill, and the accent (H1, ACCENT_F22); secondary actions stay subordinate. Emphasis detail lives in polish-pass (UNSLOP_F22 D10 — Emphasize the CTA) (fix #22)`
- **Why here:** `primary-action` already states one primary CTA; the emphasis
  means live in polish-pass D10 — this pointer routes to them.

## P3 — D15 contrast pointer → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 9.
- **Anchor (verbatim, unique):**
  `- \`color-contrast\` - Minimum 4.5:1 ratio for normal text (large text 3:1); Material Design`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`color-contrast-polish\` - Text-contrast failures found in a polish pass are fixed against the polish-pass craft floor (Contrast ≥4.5:1, ≥3:1 large text, in light AND dark, in every state) — see UNSLOP_F22 D15 (fix #22); this rule states the ratio, the craft floor is the check`
- **Why here:** the ratio already exists here and in the craft floor / less-flat-ui;
  D15 points at it and does not restate it.

## P4 — D16 headline wrapping → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 131.
- **Anchor (verbatim, unique):**
  `- \`heading-line-balance\` - Use balanced wrapping on short headings as a progressive, user-agent-controlled heuristic; keep natural wrapping readable and never force final words together with blanket nonbreaking spaces`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`headline-wrap-polish\` - Headline wrapping is fixed in a polish pass against the craft floor (headings use \`text-wrap: balance\`, no orphans, no mid-phrase breaks) — see UNSLOP_F22 D16 (fix #22)`
- **Why here:** `heading-line-balance` already owns headline wrapping; D16
  points at it (plus the craft-floor `text-wrap: balance` rule) and does not
  restate it.

## P5 — D18 tabular nums → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 129.
- **Anchor (verbatim, unique):**
  `- \`number-tabular\` - Use tabular/monospaced figures for data columns, prices, and timers to prevent layout shift`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`tabular-polish\` - Tabular figures are applied in a polish pass wherever digits change or align (counters, prices, tables) — see UNSLOP_F22 D18 (fix #22); the same value also lives in make-interfaces-feel-better (tabular-nums rule)`
- **Why here:** SPEC §5 primary home is `ui-ux-pro-max` type rules + glossary G3;
  `number-tabular` is that rule. Note for the integrator: the same value also
  exists in make-interfaces-feel-better (SKILL.md tabular-nums rule + table) —
  that is a cross-reference, not a second primary home.

## P6 — D8 group with spacing → ui-ux-pro-max

- **Target:** `skills/ui-ux-pro-max/references/quick-reference.md`, line 130.
- **Anchor (verbatim, unique):**
  `- \`whitespace-balance\` - Use whitespace intentionally to group related items and separate sections; avoid visual clutter (Apple HIG)`
- **Insert:** the following new line immediately AFTER the anchor line:
  `- \`spacing-group-polish\` - Grouping with spacing is applied in a polish pass (related items tight, distinct groups at least 2 spacing steps apart; spacing, not dividers or borders, does the grouping) — see UNSLOP_F22 D8 (fix #22); this skill owns the spacing scale (\`spacing-scale\`)`
- **Why here:** `ui-ux-pro-max` owns spacing (SPEC §2 partial); D8 points at it
  and the craft-floor spacing rules and does not restate them.

## P7 — D20 animate useful feedback → motion-patterns + motion-foundations

Two insertion points, one spec (one family: D20 ~ A10 ~ B8; the A10/B8 items
themselves belong to the Groups A+B agent).

### P7a — motion-patterns, "Button feedback" example

- **Target:** `skills/motion-patterns/SKILL.md`, line 103.
- **Anchor (verbatim, unique):**
  ```
  ### Button feedback

  ```tsx
  "use client"
  import { motion } from "motion/react"
  import { springs, motionTokens } from "@/lib/motion-tokens"

  <motion.button
    whileHover={{ scale: motionTokens.scale.pop }}
    whileTap={{ scale: motionTokens.scale.press }}
    transition={springs.snappy}
  />
  ```
  ```
- **Insert:** the following paragraph immediately AFTER the closing fence of that
  code block:
  `Animate useful feedback only (UNSLOP_F22 D20, fix #22): press feedback, a success pulse, a state change — motion that tells the user something happened. No decorative motion. This is one family with motion-foundations Principle A10 (Exaggerated feedback) and motion-patterns B8 (Pulse to confirm success); the A10/B8 items live in the motion skills (Groups A+B), this fix points at them.`
- **Why here:** the Button feedback example is the concrete home of feedback
  animation; D20 points at it and at the A10/B8 family.

### P7b — motion-foundations, duration tokens table

- **Target:** `skills/motion-foundations/SKILL.md`, line 72.
- **Anchor (verbatim, unique):**
  `| \`fast\` | Button feedback, icon swap, chip toggle |`
- **Insert:** the following line immediately AFTER the tokens table (after the
  `| \`crawl\` | Deliberate storytelling; use sparingly |` row):
  `Feedback animation (UNSLOP_F22 D20) uses the \`fast\` token for button feedback; see motion-patterns "Button feedback" and Principle A10 / B8 (fix #22).`
- **Why here:** the `fast` token is the value D20's feedback animation uses;
  the pointer routes the fix to the token without duplicating it.
