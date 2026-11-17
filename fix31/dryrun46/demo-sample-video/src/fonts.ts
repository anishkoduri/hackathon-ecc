// Self-hosted fonts (fix #25 §4(b)): the template used to load these three
// families live from Google Fonts via `@remotion/google-fonts`, which fetched
// woff2 files from fonts.gstatic.com at render time — a fetch that fails in
// restricted networks (sandbox Chrome: net::ERR_SSL_PROTOCOL_ERROR), which
// was the long-standing dry-run Leg 3 environmental FAIL. The files now live
// in `public/fonts/` and are loaded from the local Remotion static server;
// nothing in the template contacts Google Fonts at render time.
//
// Same three families the app itself loads, same family names the
// components use via shots.json -> theme.fonts, so no component changes:
//   - Hanken Grotesk: VARIABLE font, wght 100-900 (covers the 400/500/600/
//     700 the template used) — one file, weight range '100 900'.
//   - Instrument Serif: static, 400 only.
//   - JetBrains Mono: VARIABLE font, wght 400-500 (covers the 400/500 the
//     template used) — one file, weight range '400 500'.
// All three are the latin subset only. Source: Google Fonts css2 API
// (fonts.googleapis.com), files fetched from fonts.gstatic.com on
// 2026-11-13; see fix25/template-fonts.md for URLs and checksums.
// `@remotion/fonts` loadFont delays the render until each face loads and
// cancels the render (fail-closed) if a local file cannot be fetched — the
// same fail-closed shape the old google-fonts loader had.
import { loadFont } from '@remotion/fonts';
import { staticFile } from 'remotion';

loadFont({
  family: 'Hanken Grotesk',
  url: staticFile('fonts/HankenGrotesk.woff2'),
  weight: '100 900',
});

loadFont({
  family: 'Instrument Serif',
  url: staticFile('fonts/InstrumentSerif.woff2'),
  weight: '400',
});

loadFont({
  family: 'JetBrains Mono',
  url: staticFile('fonts/JetBrainsMono.woff2'),
  weight: '400 500',
});
