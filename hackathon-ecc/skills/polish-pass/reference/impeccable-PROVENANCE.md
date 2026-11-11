# Impeccable — provenance (staged, scoped — gap analysis)

Source: **pbakaus/impeccable**, by Paul Bakaus, Apache License 2.0.
Skill release **skill-v4.8.0** (`universal.zip`, 18,116,588 bytes,
2026-10-26), engine **v0.1.18**. npm package
`impeccable@4.8.0` (tarball shasum
`f344aaa43511ea0ccadce1a42c860f5990953430`, `engines: node >=18.19.0`).
npm latest is 4.8.2 (2026-11-09) — 4.8.0 is pinned deliberately because
the skill-v4.8.0 release is the verified one. Repo HEAD at staging time:
`c1e0e5492fbb524f5df84d635ecfae7dc438ec45` (2,825 commits, 107,702 stars).
Engine SHA-256 (from upstream `engine-checksums.txt`):
`impeccable-windows-x64.exe 8f61e96b0c97001546a824d79b44f46b423b560f3eb1a0cc44a8695a1b395d9f`
(linux-x64 `736ed785…f71f648`, darwin-arm64 `543ee2f7…c8a9e1`).

## What was staged (in this directory)

- `impeccable-craft-floor.md` — verbatim `reference/craft-floor.md`
  (44 lines): read before any UI edit; bans are absolute.
- `impeccable-critique.md` — verbatim `reference/critique.md`
  (819 lines): scored UX review (heuristics, persona testing,
  anti-pattern detection, ranked fixes).
- `impeccable-onboard.md` — verbatim `reference/onboard.md`
  (234 lines): first-run flows, empty states, activation / aha moment.
- `impeccable-extract.md` — verbatim `reference/extract.md`
  (69 lines): consolidate repeated patterns/tokens/components into the
  design system.
- `impeccable-detector-rules.json` — the 62 deterministic detector rules
  (31 slop + 31 quality; 44 warning, 16 advisory, 2 error), extracted
  from the `--list-rules --json` golden file at tag skill-v4.8.0. The
  rule registry itself lives in the engine (Rust); the skill ships no
  rule list, so this file is the plugin's lookup copy.

## Detector wiring

Invoke as `npx impeccable@4.8.0 detect <paths>` (pinned;
no API key, no LLM). The engine binary is NOT bundled: on first run it
downloads from the pinned release and is SHA-256-verified against the
checksums file (fails closed on mismatch). Source scans use pattern rules
only; rendered-page rules (contrast, line-length, occlusion) need a URL
or dev server + installed Chrome/Edge. On Windows run it from Git Bash
or PowerShell (`npx` is cross-platform); the engine cache is
`%USERPROFILE%\.impeccable\bin\0.1.18\`. The shipped
`.cursor/hooks.json` detector hook is POSIX-only and likely broken on
Windows (Cursor runs hook commands through PowerShell) — it is NOT wired;
the detector runs as a named step in polish-pass instead, and the hook is
a live-smoke-test item.

## DESIGN.md mapping (no new state files)

Impeccable's `PRODUCT.md`/`DESIGN.md` are NOT introduced as parallel
state: `PRODUCT.md` maps to this plugin's `docs/decision-record.md` +
`docs/scope.md`; `DESIGN.md` maps to `docs/design-tokens.md` +
`design-system/<project-slug>/MASTER.md`. The detector's
`design-system-*` rules (font/color/radius/font-size drift) read the
project's token file (`docs/design-tokens.md`) instead of DESIGN.md.

## Gap table (24 commands + the rest)

- COVERED, not staged: `polish` (= polish-pass), `distill`, `harden`,
  `clarify`, `adapt`, `optimize`, `typeset`, `layout` (all have a
  polish-pass lens of the same name); `animate` (polish-pass animate
  lens + ui-ux-pro-max motion implementation — `data/motion.csv`, 17
  GSAP presets, `--motion` dial tiers Subtle/Standard/Complex,
  quick-reference.md §7 spring-physics/easing/exit-faster-than-enter —
  + `make-interfaces-feel-better` owns feel/timing decisions and the
  motion-* skills own implementation; no framer-motion content anywhere,
  GSAP only).
- MAPPED, not staged: `init` → grill-me decision record;
  `document` → design-tokens.md/MASTER.md; `shape` → grill-me +
  hackathon-scope + Taste deal (visual probes covered by Taste);
  `audit` → adversarial audit + browser-qa (covered-in-part);
  `craft` → deprecated alias upstream, skipped.
- ADDED (this round): `extract`, `critique`, `onboard` references above;
  the detector (62 rules); the craft floor.
- FLAGGED, not added (decision items for Anish — see the coordinator's
  final report): direction lenses `bolder`, `quieter`, `colorize`,
  `decolorize`, `delight`, `overdrive` (their job is to CHANGE a design's
  direction, which clashes with the standing rule that polish-pass never
  restyles; note `overdrive`'s spring-physics content is partly covered
  by ui-ux-pro-max quick-reference.md §7, and the GSAP Complex tier
  covers pin/Flip/SplitText scroll choreography — the missing part is the
  direction change itself); `live` + `generate` (live browser variant
  iteration — genuinely missing, but interactive, needs a running dev
  server + the 553 KB live-browser.js engine scripts, and cannot run in
  the unattended first build).
