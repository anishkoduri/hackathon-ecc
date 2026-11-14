// One command: narration -> music -> recording -> frames -> render.
//
//   node scripts/build.mjs            full rebuild (starts the app if needed)
//   node scripts/build.mjs --no-record reuse the last take (script-only changes)
//   node scripts/build.mjs --render    render only
//
// TTS is cached per line, so a frontend-only change re-uses every clip and the
// cost is the recording plus the render. The music bed is fetched right after
// narration (it needs the measured lengths); if the fetch fails the video
// renders without a bed rather than aborting — see the music step below.
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';

let cfg;
try {
  cfg = JSON.parse(fs.readFileSync('shots.json', 'utf8'));
} catch (e) {
  console.error(`shots.json is not valid JSON: ${String(e).split('\n')[0]}`);
  process.exit(1);
}
const args = process.argv.slice(2);
const only = (f) => args.includes(f);
const t0 = Date.now();
const lap = (label, from) => console.log(`\n── ${label} ${((Date.now() - from) / 1000).toFixed(1)}s\n`);

const run = (cmd, a) => {
  const r = spawnSync(cmd, a, { stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status ?? 1);
};

// A bed is valid only when the file is non-empty AND ffprobe can read a
// finite duration from it. Existence alone is not enough: a failed re-cut
// can leave a truncated bed.wav behind, and that must never be flagged true.
const isValidAudio = (file) => {
  try {
    if (!fs.existsSync(file) || fs.statSync(file).size === 0) return false;
    const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', file], { encoding: 'utf8' });
    const dur = Number((r.stdout ?? '').trim());
    return r.status === 0 && Number.isFinite(dur) && dur > 0;
  } catch {
    return false;
  }
};

// Reconcile the `musicBed` flag Video.tsx renders from with what this run
// actually wants: true only when shots.json has a music block AND
// public/music/bed.wav exists on disk AND probes as a valid (non-empty,
// finite-duration) audio file. The flag lives in
// src/vo-durations.json, which tts.mjs just wrote (default false). Called
// after the music step, and again right before rendering (so --render runs,
// which skip the music step, reconcile it too) — removing the music block
// while a bed.wav from an earlier run still sits on disk must NOT render
// a stale bed.
const setMusicBedFlag = () => {
  try {
    const p = path.resolve('src/vo-durations.json');
    if (!fs.existsSync(p)) return;
    const vo = JSON.parse(fs.readFileSync(p, 'utf8'));
    vo.musicBed = Boolean(cfg.music) && isValidAudio(path.resolve('public/music/bed.wav'));
    fs.writeFileSync(p, JSON.stringify(vo, null, 2));
  } catch {
    /* flag is advisory; Video.tsx treats a missing flag as "no bed" */
  }
};

const KNOWN_ACTIONS = new Set([
  'goto', 'wait', 'waitFor', 'click', 'hover', 'type', 'scroll', 'scrollIn', 'focus', 'settle', 'cut',
]);

// Cheap checks that would otherwise surface as a confusing video two minutes
// from now rather than as an error two seconds from now. These run BEFORE
// any server is started, so a bad shots.json fails fast with this list
// instead of crashing at portOf() with a stack trace.
const problems = [];
const ids = new Set();
for (const [i, shot] of (cfg.shots ?? []).entries()) {
  const where = `shots[${i}]${shot?.id ? ` (${shot.id})` : ''}`;
  if (!shot?.id) problems.push(`${where}: missing id`);
  else if (ids.has(shot.id)) problems.push(`${where}: duplicate id`);
  else ids.add(shot.id);
  if (!shot?.say?.trim()) problems.push(`${where}: missing say`);
  if (!['app', 'card'].includes(shot?.kind)) problems.push(`${where}: kind must be "app" or "card"`);
  if (shot?.kind === 'card' && shot.do) problems.push(`${where}: card shots cannot have a do list`);
  for (const step of shot?.do ?? []) {
    const name = Object.keys(step ?? {})[0];
    if (!KNOWN_ACTIONS.has(name)) problems.push(`${where}: unknown action "${name}"`);
  }
}
if (!cfg.app?.url) problems.push('app.url: missing');
else {
  try { new URL(cfg.app.url); }
  catch { problems.push(`app.url: not a valid URL (${cfg.app.url})`); }
}
if (!cfg.shots?.length) problems.push('shots is empty');
if (problems.length) {
  console.error(`shots.json has ${problems.length} problem(s):\n  ${problems.join('\n  ')}`);
  process.exit(1);
}

// Default port for a URL with no explicit port: https → 443, http → 80
// (the old default of 80 for everything sent https checks to the wrong port).
const portOf = (url) => {
  const u = new URL(url);
  return Number(u.port || (u.protocol === 'https:' ? 443 : 80));
};
// Reachability of the URL's own host. Bounded by a timeout: a
// firewalled/blackholed host must read as "down" instead of hanging the
// build on the OS TCP timeout. (app.url is always a localhost URL — see
// the local-only note below — so this is a localhost check in practice.)
const isUp = (host, port, timeoutMs = 5000) =>
  new Promise((res) => {
    let settled = false;
    const s = net.connect(port, host);
    const done = (v) => {
      if (settled) return;
      settled = true;
      s.destroy();
      res(v);
    };
    s.setTimeout(timeoutMs);
    s.on('connect', () => done(true));
    s.on('timeout', () => done(false));
    s.on('error', () => done(false));
  });

const appUrl = new URL(cfg.app.url);
const appHost = appUrl.hostname;
const isLocalHost = ['localhost', '127.0.0.1', '::1', '[::1]'].includes(appHost);

// The demo video is made from the CODE, not a live link: /demo always films
// the local app from the project dir, so app.url is ALWAYS a localhost URL
// for the app being filmed. There is no deployed-URL filming path.
if (!isLocalHost) {
  console.error(
    `app.url must be a localhost URL — the demo video is filmed from the local app, not a deployed link (${cfg.app.url}).\n` +
      `Set app.url to the local dev URL (e.g. http://localhost:3000) and re-run.`
  );
  process.exit(1);
}
const port = portOf(cfg.app.url);

// How to start the app. `app.devCommand` wins; otherwise read the app's own
// `dev` script and work out how it takes a port, because every framework
// spells that differently. Never assume Vite — and NEVER fall through to a
// stray `npx vite`: when package.json exists but has no `dev` script (or
// there is no package.json at all), exit 1 immediately with a pointer
// instead of spawning a server for an app that cannot start that way.
const devCommandFor = (dir, port) => {
  if (cfg.app.devCommand) return cfg.app.devCommand.replace(/\{port\}/g, String(port));

  let pkg = null;
  try {
    pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
  } catch {
    /* no package.json — handled by the guard below */
  }
  const dev = pkg?.scripts?.dev ?? '';

  if (!pkg || !dev.trim()) {
    console.error(
      `Cannot auto-start the app in ${dir}: ${!pkg ? 'no package.json there' : 'package.json has no "dev" script'}.\n` +
        `Start the app there yourself, set APP_DIR to the directory that holds the app, or set app.devCommand in shots.json (e.g. "npm run dev -- --port {port}").`
    );
    process.exit(1);
  }

  if (/\bnext\b/.test(dev)) return `npm run dev -- --port ${port}`;
  if (/\bvite\b/.test(dev)) return `npm run dev -- --port ${port} --strictPort`;
  if (/\b(react-scripts|remix|nuxt|astro|svelte-kit|vue-cli-service)\b/.test(dev)) return `npm run dev -- --port ${port}`;
  return `npm run dev`; // most others honour PORT from the environment
};

// Start the app's dev server from `dir` on `port` and wait for it to answer.
// Exits 1 immediately — instead of spawning a stray `npx vite` and waiting
// 40 s — when there is no app to start here: no app.devCommand and no
// package.json in `dir` means there is no app to start, so do not run a
// stray `npx vite`. This guard applies whether APP_DIR is set or not.
const startDevServer = async (dir, port) => {
  if (!cfg.app.devCommand) {
    try {
      fs.readFileSync(path.join(dir, 'package.json'), 'utf8');
    } catch {
      console.error(
        `Nothing is serving ${cfg.app.url}, and there is no app to auto-start here (${dir} has no package.json).\n` +
          `Start the app there, or set APP_DIR=/path/to/the/app and re-run.\n` +
          `If its dev server needs a specific command, set app.devCommand in shots.json.`
      );
      process.exit(1);
    }
  }

  const cmd = devCommandFor(dir, port);
  console.log(`starting the app from ${dir}:  ${cmd}`);
  const server = spawn(cmd, {
    cwd: dir,
    shell: true,
    stdio: ['ignore', 'ignore', 'inherit'],
    detached: true,
    env: { ...process.env, PORT: String(port), BROWSER: 'none' },
  });

  // Next and friends can take a while on a cold start; 160 * 250ms = 40s.
  // Bail early if the dev command itself exits (e.g. the port is taken and
  // --strictPort refused it) — otherwise the wait loop would see the other
  // app on that port, call it up, and film the wrong thing.
  for (let i = 0; i < 160 && !(await isUp('localhost', port)); i++) {
    if (server.exitCode !== null) break;
    await new Promise((r) => setTimeout(r, 250));
  }
  if (server.exitCode !== null) {
    console.error(`the dev command exited without the app coming up on :${port}. Try running \`${cmd}\` in ${dir} yourself.`);
    process.exit(1);
  }
  if (!(await isUp('localhost', port))) {
    console.error(`the app did not come up on :${port}. Try running \`${cmd}\` in ${dir} yourself.`);
    process.exit(1);
  }
  return server;
};

let devServer = null;
const willRecord = !only('--render') && !only('--no-record');
if (!(await isUp(appHost, port))) {
  if (!willRecord) {
    // --render / --no-record needs no app at all: NEVER auto-start a dev
    // server and NEVER exit 1 for a down app — render from cached footage.
    console.log(`! app is not up at ${cfg.app.url} — continuing without it (this run does not record; rendering from cached footage). Note it in the final report.`);
  } else {
    // APP_DIR unset: fall back to auto-starting the dev server from the
    // project directory (the video project lives in the app repo) — the same
    // auto-start as APP_DIR. Note the fallback in the final report.
    const dir = process.env.APP_DIR ?? process.cwd();
    if (!process.env.APP_DIR) {
      console.log(`! APP_DIR is unset — auto-starting the dev server from the project directory (${dir}); note it in the final report.`);
    }
    devServer = await startDevServer(dir, port);
  }
}

// --render runs skip tts.mjs, so the manifest can go stale: a wav deleted
// since the last build would still be flagged hasAudio, and Video.tsx would
// render an <Audio> for a file that does not exist. Reconcile hasAudio from
// file existence (the same check tts.mjs does on a full rebuild) and drop
// any non-finite cached duration to an estimated silent beat, before
// rendering. The reconcile runs BOTH directions: a line whose wav is gone
// goes silent, AND a line flagged silent whose wav is still on disk (e.g.
// the first build's ElevenLabs narration, in a keyless removal re-film)
// is RESTORED with its probed duration — a wav on disk is never ignored.
// Runs on every build; on a full rebuild it is a no-op.
const reconcileNarration = () => {
  try {
    const p = path.resolve('src/vo-durations.json');
    if (!fs.existsSync(p)) return;
    const vo = JSON.parse(fs.readFileSync(p, 'utf8'));
    let changed = false;
    let silent = 0;
    let restored = 0;
    for (const s of vo.shots ?? []) {
      const hasFile = fs.existsSync(path.resolve(`public/vo/${s.id}.wav`));
      if (s.hasAudio && !hasFile) { s.hasAudio = false; changed = true; }
      if (!Number.isFinite(Number(s.dur))) {
        const words = String(s.say ?? '').trim().split(/\s+/).filter(Boolean).length;
        s.dur = Number(Math.max(2, words / 2.5).toFixed(3));
        s.hasAudio = false;
        changed = true;
      }
      if (!s.hasAudio && hasFile) {
        // Restore: a wav rendered in an earlier run is still on disk — the
        // line keeps its original voice instead of going silent. Only when
        // the file probes as valid audio with a finite duration; a bad
        // probe keeps it silent.
        try {
          const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', path.resolve(`public/vo/${s.id}.wav`)], { encoding: 'utf8' });
          const d = Number((r.stdout ?? '').trim());
          if (r.status === 0 && Number.isFinite(d) && d > 0) { s.hasAudio = true; s.dur = Number(d.toFixed(3)); changed = true; restored += 1; }
        } catch { /* stays silent */ }
      }
      if (!s.hasAudio) silent += 1;
    }
    if (changed) {
      const total = (vo.shots ?? []).length;
      vo.narration = silent === 0 ? 'full' : silent === total ? 'none' : 'partial';
      fs.writeFileSync(p, JSON.stringify(vo, null, 2));
      console.log(`! narration manifest reconciled before render: ${silent} of ${total} shot(s) silent (missing wav or bad duration)${restored > 0 ? `, ${restored} restored from wavs on disk` : ''}. Note it in the final report.`);
    }
  } catch {
    /* manifest is advisory; Video.tsx fail-closes on missing flags */
  }
};

try {
  if (!only('--render')) {
    let s = Date.now();
    run('node', ['scripts/tts.mjs']);
    lap('narration', s);

    // Music bed, fetched once the measured lengths exist. This step NEVER
    // aborts the run: a failed fetch (no yt-dlp, no network, bad URL) just
    // means the video renders without a bed — Video.tsx skips the <Audio>
    // element when no bed.wav exists. Note it in the final report.
    if (cfg.music) {
      s = Date.now();
      const musicRun = spawnSync('node', ['scripts/music.mjs'], { stdio: 'inherit' });
      if (musicRun.status !== 0) {
        console.log('! music bed could not be fetched — rendering WITHOUT a music bed. Note it in the final report; re-run `node scripts/music.mjs` once the track is reachable.');
      } else {
        lap('music', s);
      }
    }
    setMusicBedFlag();

    if (!only('--no-record')) {
      s = Date.now();
      run('node', ['scripts/record.mjs']);
      lap('recording', s);

      s = Date.now();
      run('node', ['scripts/frames.mjs']);
      lap('frames', s);
    }
  }

  // Reconcile the music-bed flag from disk before rendering, so --render
  // runs (which skip the music step above) do not render a stale bed.
  setMusicBedFlag();

  // Reconcile narration against the wav files on disk (see above): a
  // --render run skips tts.mjs, so a stale manifest would render audio
  // for files that no longer exist.
  reconcileNarration();

  const s = Date.now();
  run('npx', ['@remotion/cli@4.0.526', 'render', 'src/index.ts', 'Demo', 'out/demo.mp4',
    '--concurrency=8', '--jpeg-quality=92', '--crf=19', '--log=error']);
  lap('render', s);
} finally {
  if (devServer) process.kill(-devServer.pid);
}

// Master the audio to roughly what YouTube and Devpost normalise to, so the
// video is not noticeably quieter than everything around it. Video is copied.
// Warning-only: out/demo.mp4 already exists at this point, so a failed
// loudnorm master or small variant must NOT fail the run — the rendered
// video is still usable as-is.
const runWarn = (label, cmd, a) => {
  const r = spawnSync(cmd, a, { stdio: 'inherit' });
  if (r.status !== 0) console.log(`! ${label} failed — out/demo.mp4 is still usable as rendered. Note it in the final report.`);
  return r.status === 0;
};

if (runWarn('audio mastering (loudnorm)', 'ffmpeg', ['-y', '-v', 'error', '-i', 'out/demo.mp4', '-c:v', 'copy',
  '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', 'out/.mastered.mp4'])) {
  fs.renameSync('out/.mastered.mp4', 'out/demo.mp4');
}

// A smaller copy for upload limits that cap at 50–100 MB.
runWarn('small variant (demo-small.mp4)', 'ffmpeg', ['-y', '-v', 'error', '-i', 'out/demo.mp4', '-vcodec', 'libx264', '-crf', '26',
  '-preset', 'veryfast', '-acodec', 'aac', '-b:a', '128k', 'out/demo-small.mp4']);

console.log(`\ntotal ${((Date.now() - t0) / 1000).toFixed(1)}s -> out/demo.mp4`);
