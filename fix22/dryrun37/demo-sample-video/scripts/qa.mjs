// Renders one still per shot, at a point where that shot has settled, and
// stacks them into contact sheets you can read in one go.
//
//   node scripts/qa.mjs           one still per shot
//   node scripts/qa.mjs 4         four evenly spaced stills per shot
//
// Reviewing a demo video by scrubbing it is slow and you will miss things.
// Reviewing a contact sheet takes seconds and catches the failures that matter:
// a spinner under a caption, a shot on the wrong page, text too small to read.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const FPS = 30;
const LEAD = 0.7;
const perShot = Math.max(1, Number(process.argv[2] ?? 1));

const cfg = JSON.parse(fs.readFileSync('shots.json', 'utf8'));
const vo = JSON.parse(fs.readFileSync('src/vo-durations.json', 'utf8'));
const gap = cfg.gapMs / 1000;

const OUT = path.resolve('out/qa');
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

const picks = [];
let t = LEAD;
for (const s of vo.shots) {
  const dur = s.dur + gap;
  for (let i = 0; i < perShot; i++) {
    // Offset into the shot: one still lands just past the opening, several
    // spread across it. Never frame 0 — that is the crossfade.
    const p = perShot === 1 ? 0.45 : 0.18 + (0.66 * i) / (perShot - 1);
    picks.push({ id: s.id, frame: Math.round((t + dur * p) * FPS) });
  }
  t += dur;
}

console.log(`rendering ${picks.length} stills…`);
for (const p of picks) {
  const file = path.join(OUT, `${String(p.frame).padStart(5, '0')}_${p.id}.png`);
  execFileSync('npx', ['remotion@4.0.542', 'still', 'src/index.ts', 'Demo', file, `--frame=${p.frame}`, '--log=error'], {
    stdio: ['ignore', 'ignore', 'inherit'],
  });
  p.file = file;
}

// Six per sheet: any more and the frames are too small to judge.
const PER = 6;
const sheets = [];
for (let i = 0; i < picks.length; i += PER) {
  const group = picks.slice(i, i + PER);
  const sheet = path.join(OUT, `sheet_${String(sheets.length + 1).padStart(2, '0')}.png`);
  const cols = Math.min(3, group.length);
  const layout = group
    .map((_, n) => {
      const c = n % cols;
      const r = Math.floor(n / cols);
      const x = c === 0 ? '0' : Array.from({ length: c }, (_, k) => `w${k}`).join('+');
      const y = r === 0 ? '0' : `h${(r - 1) * cols}`;
      return `${x}_${y}`;
    })
    .join('|');
  execFileSync('ffmpeg', [
    '-y', '-v', 'error',
    ...group.flatMap((g) => ['-i', g.file]),
    '-filter_complex',
    `${group.map((_, n) => `[${n}]`).join('')}xstack=inputs=${group.length}:layout=${layout},scale=1900:-1`,
    sheet,
  ]);
  sheets.push(sheet);
}

// --- fix #18 QA checks: runtime, coverage, theme, A/V table, mix --------
// Total runtime from MEASURED narration (same derivation as timeline.ts):
// LEAD + sum(dur + gap) + TAIL. Hard rule under 2:10 (130s); absolute
// ceiling 2:30 (150s), never exceeded.
const LEAD_S = 0.7;
const TAIL_S = 1.7;
const totalSec = LEAD_S + (vo.shots ?? []).reduce((n, s) => n + s.dur + gap, 0) + TAIL_S;
const blocking = [];

// Coverage: every must-have feature has a beat or a recorded cut.
const shotById = Object.fromEntries((cfg.shots ?? []).map((s) => [s.id, s]));
let marks = null;
try { marks = JSON.parse(fs.readFileSync('capture/marks.json', 'utf8')); } catch { /* no recording yet */ }
const filmed = new Set((marks?.marks ?? []).map((m) => m.id));
const features = cfg.features ?? null;
const cuts = cfg.cuts ?? [];
const coverageRows = (features ?? []).map((f) => {
  const beat = shotById[f.beat];
  const status = !beat ? 'MISSING BEAT' : beat.kind === 'card' ? 'card — no footage' : !marks ? 'no recording yet' : filmed.has(f.beat) ? 'filmed' : 'NOT FILMED';
  if (!beat || (beat.kind === 'app' && marks && !filmed.has(f.beat))) blocking.push(`coverage: feature "${f.name}" → beat "${f.beat}" ${!beat ? 'missing from shots.json' : 'produced no footage'}`);
  return { name: f.name, beat: f.beat, status };
});
if (features === null) blocking.push('coverage: no features array in shots.json — enumerate the must-haves (step 3)');

// Theme: the seed theme ships only with a recorded source.
const SEED_THEME = { bg: '#0d0a24', accent: '#ffc93c', card: '#161141' };
const colors = cfg.theme?.colors ?? {};
const themeIsSeed = colors.bg === SEED_THEME.bg && colors.accent === SEED_THEME.accent && colors.card === SEED_THEME.card;
if (themeIsSeed && !cfg.theme?.source) blocking.push('theme: shots.json still carries the seed theme with no recorded theme.source');
if (totalSec > 130) blocking.push(`runtime: ${totalSec.toFixed(1)}s over the 2:10 (130s) hard rule — re-cut`);
if (totalSec > 150) blocking.push(`runtime: ${totalSec.toFixed(1)}s over the 2:30 (150s) absolute ceiling — never exceeded`);
const underGain = cfg.music?.gain?.under;

console.log(`\n${sheets.length} contact sheet(s):`);
for (const s of sheets) console.log(`  ${s}`);

console.log('\n--- fix #18 QA (read these before the sheets) ---');
console.log(`Total runtime (measured narration + gaps + lead/tail): ${totalSec.toFixed(1)}s — hard rule under 2:10 (130s), absolute ceiling 2:30 (150s).${totalSec > 130 ? ' BLOCKING: over 2:10 — re-cut.' : ''}`);
console.log('\nCoverage table (feature → beat):');
if (!features) console.log('  (no features array in shots.json — BLOCKING, see below)');
for (const r of coverageRows) console.log(`  ${r.name} → ${r.beat} — ${r.status}`);
console.log('  Cuts (recorded, with reasons):');
for (const c of cuts) console.log(`  ${c.name} — ${c.reason}`);
if (!cuts.length) console.log('  (none)');
console.log(`\nTheme: ${themeIsSeed ? 'identical to the seed theme' : 'pulled from the app tokens'}${cfg.theme?.source ? ` — source recorded: ${cfg.theme.source}` : ' — no theme.source recorded'}`);
console.log(`Vignette: theme.vignette = ${cfg.theme?.vignette ?? '0.3 (default)'}${cfg.theme?.vignette === undefined ? ' — record the choice (0 for light apps)' : ''}`);
if (underGain !== undefined && underGain > 0.20) console.log(`\nWARNING: music.gain.under is ${underGain} (over 0.20) — the bed risks burying the voice. Do the 10-second mix listen from the middle of the video and confirm the narration is intelligible over it.`);
console.log('\nPer-beat A/V table — complete this while reading the sheets (claim → stills support it?):');
for (const s of cfg.shots ?? []) console.log(`  ${s.id} [${s.kind}] "${String(s.say).slice(0, 70)}" — supports it: ___`);
console.log('  Record the completed table in the video project (qa notes). A "no" is BLOCKING: re-film or rewrite the line; the video does not ship with an unmatched claim.');
if (blocking.length) {
  console.log(`\nBLOCKING findings (${blocking.length}):`);
  for (const b of blocking) console.log(`  BLOCKING — ${b}`);
} else {
  console.log('\nNo BLOCKING findings from the automated checks.');
}
console.log('\nRead the sheets as images. Check, in order:');
console.log('  1. capture/marks.json -> warnings is empty, and capture/failures/ is empty');
console.log('  2. every shot is on the page you think it is');
console.log('  3. no spinners, skeletons or empty states');
console.log('  4. every claim in the narration matches what is on screen');
console.log('  5. captions legible, small text legible or zoomed');
console.log('  6. gorgeousness: cards read as the app\'s own palette/fonts (not the seed); footage shows the app\'s best-looking states, never an empty state; vignette matches the app');
console.log('  7. mix: listen to a 10-second sample from the middle of the video and confirm the narration is intelligible over the bed');
if (blocking.length) process.exitCode = 1;

