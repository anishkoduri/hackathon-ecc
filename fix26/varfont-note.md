# Fix #26 §4 — Variable-font scoped exception (VARFONT_F26)

## Decision (parent decision at the fix #25 close, recorded here)

The pitch-deck-video template's Hanken Grotesk + JetBrains Mono variable
woff2 files are a SCOPED EXCEPTION to the static-only font rule
(fix #19/#21; pitch-deck-video SKILL.md: "keep fonts self-hosted and
static"). App UI fonts stay static-only.

## Scope (video template only)

- `new-skills/pitch-deck-video/template/public/fonts/HankenGrotesk.woff2`
  — 34,704 B, variable, wght 100–900 (template `src/fonts.ts:11–12`,
  weight `'100 900'`).
- `new-skills/pitch-deck-video/template/public/fonts/JetBrainsMono.woff2`
  — 30,376 B, variable, wght 400–500 (template `src/fonts.ts:14–15`,
  weight `'400 500'`).
- NOT excepted: `InstrumentSerif.woff2` — 21,032 B, static, weight 400
  only (`src/fonts.ts:13`, weight `'400'`).

File sizes verified against the staged files this session; the variable /
static split is the template's own recorded fact (`src/fonts.ts:11–15`)
and the fix #25 manifest §4(b) row.

## Reason

The video renders in a single controlled Chromium and the output is a
fixed video file, so the cross-platform variance the static-only rule
guards against does not apply. The rule's purpose is identical rendering
of app UI on iPhone and web; a fixed video file has no second platform
to diverge on.

## Where recorded

- `new-skills/orchestrate/references/design-inventory.md` §11 (new
  "Scoped exceptions" section, lines 162–166) — placed there because no
  existing inventory section fits: the font entries in §1/§2 are
  catalogs of pairings, and §9's Bang Motion row covers /demo video
  styles, not template fonts. A dedicated exceptions section keeps the
  narrowing visible instead of burying it in an unrelated table.
- This note (`fix26/varfont-note.md`).

## No code change

Recording only. No font file, loader, or rule text was changed.
