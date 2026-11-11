// Fetches the background track named in shots.json and cuts a bed for the
// current edit: trimmed to the video length, faded, and levelled so the mix in
// src/Video.tsx only has to apply gain.
//
// Needs yt-dlp. `node scripts/build.mjs` calls this right after narration
// (the bed length comes from the measured narration), so you only run it by
// hand to re-cut the bed without a full rebuild:
//   node scripts/music.mjs
// A failed fetch never aborts a build: build.mjs logs a warning and the
// video renders without a bed (Video.tsx skips the music <Audio> element
// when no bed.wav exists). On success this also sets `musicBed: true` in
// src/vo-durations.json, the flag Video.tsx renders from; build.mjs
// reconciles that flag from the file on disk after every run.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

let cfg;
try {
  cfg = JSON.parse(fs.readFileSync('shots.json', 'utf8'));
} catch (e) {
  console.error(`shots.json is not valid JSON: ${String(e).split('\n')[0]}`);
  process.exit(1);
}
let vo;
try {
  vo = JSON.parse(fs.readFileSync('src/vo-durations.json', 'utf8'));
} catch (e) {
  console.error(`src/vo-durations.json is not valid JSON (run tts first): ${String(e).split('\n')[0]}`);
  process.exit(1);
}
const music = cfg.music;
if (!music?.url && !music?.file) {
  console.error('shots.json needs music.url (fetched with yt-dlp) or music.file (a local track)');
  process.exit(1);
}

// Same arithmetic as src/timeline.ts: lead + every scene + tail, plus slack.
const LEAD = 0.7, TAIL = 1.7;
const need = LEAD + vo.shots.reduce((n, s) => n + s.dur + cfg.gapMs / 1000, 0) + TAIL + 4;

const DIR = path.resolve('public/music');
fs.mkdirSync(DIR, { recursive: true });
// A local file is simplest and has no licence ambiguity; a URL is fetched once
// and cached.
const local = music.file ? path.resolve(music.file.replace(/^~/, process.env.HOME)) : null;
if (local && !fs.existsSync(local)) {
  console.error(`music.file not found: ${local}`);
  process.exit(1);
}
const src = local ?? path.join(DIR, 'source.webm');

const ytdlp = ['.tools/bin/yt-dlp', 'yt-dlp'].find((p) => { try { execFileSync(p, ['--version'], { stdio: 'ignore' }); return true; } catch { return false; } });

if (!local && !fs.existsSync(src)) {
  if (!ytdlp) { console.error('yt-dlp not found — install it, or drop the track at public/music/source.webm'); process.exit(1); }
  console.log('downloading the track…');
  execFileSync(ytdlp, ['-f', 'bestaudio', '--no-playlist', '-o', path.join(DIR, 'source.%(ext)s'), music.url], { stdio: 'inherit' });
}
fs.writeFileSync(path.join(DIR, 'SOURCE.txt'), `${music.credit ?? ''}\n${music.url ?? local}\n`);

const fadeIn = music.fadeIn ?? 2;
execFileSync('ffmpeg', ['-y', '-v', 'error', '-ss', String(music.start ?? 0), '-t', String(need.toFixed(2)), '-i', src,
  '-af', [
    `afade=t=in:st=0:d=${fadeIn}`,
    `afade=t=out:st=${(need - 3).toFixed(2)}:d=3`,
    'loudnorm=I=-18:TP=-2:LRA=11',
  ].join(','),
  '-ar', '48000', '-ac', '2', path.join(DIR, 'bed.wav')], { stdio: 'inherit' });

// Verify the cut before flagging it: a failed re-cut must not leave a
// truncated bed.wav behind flagged as present. The bed is valid only when
// it is non-empty AND ffprobe reads a finite duration from it. An invalid
// bed is deleted and the step fails (build.mjs treats a failed music step
// as a warning and renders without a bed).
const bedPath = path.join(DIR, 'bed.wav');
let bedValid = false;
try {
  if (fs.statSync(bedPath).size > 0) {
    const dur = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', bedPath], { encoding: 'utf8' }).toString().trim());
    bedValid = Number.isFinite(dur) && dur > 0;
  }
} catch {
  bedValid = false;
}
if (!bedValid) {
  try { fs.unlinkSync(bedPath); } catch { /* already gone */ }
  console.error('music bed cut produced an invalid (empty/unreadable) bed.wav — deleted; rendering without a music bed');
  process.exit(1);
}

// Flag the bed as present for Video.tsx (build.mjs reconciles this from
// disk after every run; this covers a hand-run followed by --render).
try {
  const voPath = path.resolve('src/vo-durations.json');
  if (fs.existsSync(voPath)) {
    const vo = JSON.parse(fs.readFileSync(voPath, 'utf8'));
    vo.musicBed = true;
    fs.writeFileSync(voPath, JSON.stringify(vo, null, 2));
  }
} catch { /* flag is advisory; a missing flag renders as "no bed" */ }

console.log(`bed: ${need.toFixed(1)}s from ${music.credit ?? path.basename(src)}`);
