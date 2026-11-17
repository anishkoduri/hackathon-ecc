// Audio first. Render one narration clip per shot, measure it, and write the
// measured durations. Everything downstream (the recorder's dwell times, the
// scene lengths, the captions) is derived from these numbers, so changing a
// line in shots.json is the only edit a script change needs.
//
// Clips are cached by a hash of the voice settings and the text, so re-running
// after a frontend change costs nothing and only edited lines are re-rendered.
import { execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

let cfg;
try {
  cfg = JSON.parse(fs.readFileSync('shots.json', 'utf8'));
} catch (e) {
  console.error(`shots.json is not valid JSON: ${String(e).split('\n')[0]}`);
  process.exit(1);
}
const tts = cfg.tts ?? { provider: 'say', fallback: { voice: 'Samantha', rate: 178 } };
const VO = path.resolve('public/vo');
fs.mkdirSync(VO, { recursive: true });

// --- credentials -----------------------------------------------------------
// Read straight out of the other project's env file rather than copying the
// key in here. Override the path with MINIMAX_ENV_FILE, or just export
// MINIMAX_API_KEY / MINIMAX_GROUP_ID and the file is not needed at all.
const readEnvFile = (file) => {
  if (!file || !fs.existsSync(file)) return {};
  const out = {};
  for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m) out[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
  return out;
};

const fileEnv = readEnvFile(process.env.MINIMAX_ENV_FILE ?? tts.envFile);
const creds = {
  // The subscription key is preferred where it exists; same endpoint either way.
  key: process.env.MINIMAX_API_KEY || fileEnv.MINIMAX_SUBSCRIPTION_API_KEY || fileEnv.MINIMAX_API_KEY,
  group: process.env.MINIMAX_GROUP_ID || fileEnv.MINIMAX_GROUP_ID,
  // ElevenLabs key comes ONLY from the environment. Never read it from a
  // file, never hardcode it, never write it into shots.json.
  eleven: process.env.ELEVENLABS_API_KEY,
};

// --- providers -------------------------------------------------------------
const sayTo = async (text, mp3) => {
  const v = tts.fallback ?? { voice: 'Samantha', rate: 178 };
  const aiff = mp3.replace(/\.\w+$/, '.aiff');
  execFileSync('say', ['-v', v.voice, '-r', String(v.rate), '-o', aiff, text]);
  fs.renameSync(aiff, mp3);
};

const minimaxTo = async (text, mp3) => {
  if (!creds.key || !creds.group) throw new Error('no MiniMax credentials');
  const res = await fetch(`https://api.minimaxi.com/v1/t2a_v2?GroupId=${creds.group}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${creds.key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: tts.model ?? 'speech-2.8-hd',
      text,
      stream: false,
      language_boost: tts.languageBoost ?? 'English',
      voice_setting: { voice_id: tts.voice, speed: tts.speed ?? 1, vol: 1, pitch: 0, text_normalization: true },
      audio_setting: { sample_rate: 44100, bitrate: 128000, format: 'mp3', channel: 1 },
    }),
    signal: AbortSignal.timeout(180_000),
  });
  if (!res.ok) throw new Error(`MiniMax HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const body = await res.json();
  if (body.base_resp?.status_code) throw new Error(`MiniMax ${body.base_resp.status_code}: ${body.base_resp.status_msg}`);
  if (!body.data?.audio) throw new Error('MiniMax returned no audio');
  fs.writeFileSync(mp3, Buffer.from(body.data.audio, 'hex'));
};

const probe = (f) =>
  Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', f]).toString().trim());

// --- ElevenLabs (REST, free tier) + Piper (local, zero keys) ----------------
// ElevenLabs free tier: 10,000 chars/month (~10 min audio), REST only,
// non-commercial, attribution in the title of anything published from it.
// Endpoint and shape mirror OpenMontage's tools/audio/elevenlabs_tts.py:
// POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id} with the
// `xi-api-key` header and { text, model_id, voice_settings } in the body.
// Default model eleven_multilingual_v2; eleven_flash_v2_5 is the fast one.
// SSML <break> tags work on the v2 family — eleven_multilingual_v2 (the
// default), eleven_flash_v2, and eleven_flash_v2_5 — up to 3s per break.
// eleven_turbo_v2_5 also takes breaks but is deprecated: never select it.
// v3/v4 models do NOT support <break> tags. Voice ids are
// opaque strings, e.g. Rachel is 21m00Tcm4TlvDq8ikWAM.
const elevenlabsTo = async (text, mp3) => {
  if (!creds.eleven) throw new Error('no ELEVENLABS_API_KEY set');
  const voiceId = tts.voice ?? '21m00Tcm4TlvDq8ikWAM'; // Rachel, the ElevenLabs default
  const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`, {
    method: 'POST',
    headers: { 'xi-api-key': creds.eleven, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
    body: JSON.stringify({
      text,
      model_id: tts.model ?? 'eleven_multilingual_v2',
      voice_settings: {
        stability: tts.stability ?? 0.5,
        similarity_boost: tts.similarityBoost ?? 0.75,
        style: tts.style ?? 0.0,
        speed: tts.speed ?? 1.0,
        use_speaker_boost: true,
      },
    }),
    signal: AbortSignal.timeout(180_000),
  });
  if (!res.ok) throw new Error(`ElevenLabs HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  fs.writeFileSync(mp3, Buffer.from(await res.arrayBuffer()));
};

// Free-tier quota, tracked locally so a second video in the same month does
// not silently burn the rest of the allowance. Only characters actually
// synthesised count; cached lines and failed calls cost nothing.
const ELEVENLABS_MONTHLY_CHARS = 10_000;
const usagePath = path.resolve('src/elevenlabs-usage.json');
const currentMonth = () => new Date().toISOString().slice(0, 7);
const readUsage = () => {
  try {
    const u = JSON.parse(fs.readFileSync(usagePath, 'utf8'));
    return u.month === currentMonth() ? u : { month: currentMonth(), charsUsed: 0 };
  } catch { return { month: currentMonth(), charsUsed: 0 }; }
};
const recordUsage = (chars) => {
  const u = readUsage();
  u.charsUsed += chars;
  fs.writeFileSync(usagePath, JSON.stringify(u, null, 2));
};

// Piper: local binary, zero keys, offline. Install with `pip install piper-tts==1.8.0`
// (Windows PowerShell: `py -m pip install piper-tts==1.8.0`), then download a voice model (default en_US-lessac-medium,
// voices live in ~/.piper/models). This is the no-key fallback on Windows,
// where macOS `say` does not exist. Piper writes a WAV even though the
// scratch path ends in .raw; ffmpeg below probes content, not extension.
const hasPiper = (() => {
  let cached;
  return () => {
    if (cached === undefined) {
      try { execFileSync('piper', ['--version'], { stdio: 'ignore' }); cached = true; }
      catch { cached = false; }
    }
    return cached;
  };
})();

// `say` exists on macOS only. `say -v '?'` lists voices and exits 0 there;
// anywhere else the binary is missing and the spawn throws.
const hasSay = (() => {
  let cached;
  return () => {
    if (cached === undefined) {
      try { execFileSync('say', ['-v', '?'], { stdio: 'ignore' }); cached = true; }
      catch { cached = false; }
    }
    return cached;
  };
})();

// --- voice preflight -------------------------------------------------------
// Check which voice providers exist BEFORE synthesising anything, so a
// missing voice is a known, reported condition — not a crash on the first
// line (the old Windows failure: no key, no Piper, no `say`). Checks, in
// order: ELEVENLABS_API_KEY in the environment, MiniMax credentials,
// the `piper` binary, macOS `say`.
const preflightVoice = () => {
  const available = [];
  if (creds.eleven) available.push('elevenlabs');
  if (creds.key && creds.group) available.push('minimax');
  if (hasPiper()) available.push('piper');
  if (hasSay()) available.push('say');
  console.log(`voice preflight: available providers: ${available.length ? available.join(', ') : 'none (no ELEVENLABS_API_KEY, no MiniMax credentials, no Piper, no say)'}`);
  return available;
};

const piperTo = async (text, mp3) => {
  if (!hasPiper()) throw new Error('piper binary not found — install with: pip install piper-tts (Windows PowerShell: py -m pip install piper-tts), then download a voice model');
  const args = ['--model', tts.piperModel ?? 'en_US-lessac-medium'];
  const dataDir = path.join(process.env.HOME ?? process.env.USERPROFILE ?? '.', '.piper', 'models');
  if (fs.existsSync(dataDir)) args.push('--data-dir', dataDir);
  args.push('--output_file', mp3);
  execFileSync('piper', args, { input: text, encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
};

const cachePath = path.join(VO, '.cache.json');
// A corrupt cache file must not abort tts.mjs with a stack trace: ignore it
// and re-render the clips (the wav files on disk are still reused only when
// their cache entry is intact, so a corrupt cache costs re-synthesis, not a
// failed run).
const cache = (() => {
  if (!fs.existsSync(cachePath)) return {};
  try {
    return JSON.parse(fs.readFileSync(cachePath, 'utf8'));
  } catch (e) {
    console.log(`! public/vo/.cache.json is corrupt (${String(e).split('\n')[0]}) — ignoring it; clips will be re-rendered`);
    return {};
  }
})();

const availableProviders = preflightVoice();

// Resolve the configured provider to one that actually exists, before
// deciding narration is impossible. Chains, in order:
//   ElevenLabs → Piper → say;  MiniMax → Piper → say;  Piper → say;  say → Piper → ElevenLabs.
// If the chain is exhausted, fall through to any other usable voice
// (ElevenLabs → Piper → say → MiniMax) before skipping narration — narration is
// skipped only when no usable voice exists at all. MiniMax sits last in that
// universal fallback: a MiniMax voice id is not an ElevenLabs voice id, so a
// MiniMax attempt with another provider's voice id fails at the API and the
// line degrades through the chain instead — it never aborts the run.
const CHAINS = {
  elevenlabs: ['elevenlabs', 'piper', 'say'],
  minimax: ['minimax', 'piper', 'say'],
  piper: ['piper', 'say'],
  say: ['say', 'piper', 'elevenlabs'],
};
const configuredProvider = tts.provider ?? 'say';
const chain = CHAINS[configuredProvider] ?? [configuredProvider, 'piper', 'say'];
let provider = chain.find((p) => availableProviders.includes(p))
  ?? ['elevenlabs', 'piper', 'say', 'minimax'].find((p) => availableProviders.includes(p))
  ?? null;
if (provider && provider !== configuredProvider) {
  console.log(`! provider "${configuredProvider}" is unavailable — using ${provider} instead`);
}

// No usable voice provider at all: NEVER abort the video. Skip every narration
// line and write estimated beat lengths (word-count based, ~150 wpm, min
// 2s per beat) so the scenes keep a sensible length and the video still
// renders music-only/silent. The caller must note the missing narration in
// the final report; re-running `npm run script` with a key or Piper
// installed produces the narrated cut.
const skipNarration = provider === null;
if (skipNarration) {
  // provider === null here means availableProviders is empty: the universal
  // fallback above covers every known provider, so a non-empty available
  // list always resolves to one.
  console.log('! no voice provider available — building WITHOUT narration (music-only/silent). Install Piper or set ELEVENLABS_API_KEY and re-run `npm run script` for a narrated cut. Note the missing narration in the final report.');
  const out = cfg.shots.map((s) => {
    const words = s.say.trim().split(/\s+/).filter(Boolean).length;
    const est = Number(Math.max(2, words / 2.5).toFixed(3));
    // Narration-cache reuse: a keyless re-run (e.g. a one-prompt removal
    // re-film in a new session, no key) still has the first build's wavs
    // on disk. If this line's cached clip was rendered with the
    // CONFIGURED provider (cache key + stored provider both match) and
    // the wav is still there with a finite duration, reuse it in its
    // original voice instead of going silent — the video keeps its
    // narration. A clip rendered by a fallback voice never matches here
    // (its stored provider differs from the configured one), so it is
    // never reused as the configured voice.
    const wav = path.join(VO, `${s.id}.wav`);
    const key = crypto
      .createHash('sha1')
      .update(`${configuredProvider}|${tts.voice}|${tts.model}|${tts.speed}|${tts.stability}|${tts.similarityBoost}|${tts.style}|${tts.piperModel}|${JSON.stringify(tts.fallback)}|${s.say}`)
      .digest('hex');
    const entry = cache[s.id];
    if (entry?.key === key && entry.provider === configuredProvider && fs.existsSync(wav)) {
      let d = entry.dur;
      if (!Number.isFinite(d)) { try { d = Number(probe(wav).toFixed(3)); } catch { d = NaN; } }
      if (Number.isFinite(d)) return { id: s.id, kind: s.kind, say: s.say, dur: d, hasAudio: true };
    }
    return { id: s.id, kind: s.kind, say: s.say, dur: est, hasAudio: false };
  });
  const total = out.reduce((n, s) => n + s.dur + cfg.gapMs / 1000, 0);
  const reused = out.filter((s) => s.hasAudio).length;
  const narration = reused === 0 ? 'none' : reused === out.length ? 'full' : 'partial';
  fs.mkdirSync('src', { recursive: true });
  fs.writeFileSync('src/vo-durations.json', JSON.stringify({ gapMs: cfg.gapMs, narration, musicBed: false, shots: out }, null, 2));
  console.log(`\nvoice: none — narration skipped, estimated beat lengths used${reused > 0 ? ` (${reused} of ${out.length} line(s) reused from the narration cache in their original voice)` : ''}`);
  console.log(`narration total (with gaps, estimated): ${total.toFixed(1)}s`);
  process.exit(0);
}

const out = [];
let total = 0;
let built = 0;
let failedLines = 0;

for (const s of cfg.shots) {
  const wav = path.join(VO, `${s.id}.wav`);
  // Cache key is keyed on the CONFIGURED provider, not the resolved one:
  // a keyless re-run (removal re-film, new session, no key) resolves to
  // piper/say, but the first build's ElevenLabs wavs are still on disk
  // and must be reused in their original voice, not re-synthesised in a
  // fallback voice or dropped. The stored provider on the cache entry
  // guards the other direction: a clip rendered by a fallback voice is
  // never reused as the configured voice — if the entry's provider
  // differs from the configured one, the line re-renders (see the
  // cache-hit guard below). The provider that actually produced the clip
  // is stored on the cache entry.
  const key = crypto
    .createHash('sha1')
    .update(`${configuredProvider}|${tts.voice}|${tts.model}|${tts.speed}|${tts.stability}|${tts.similarityBoost}|${tts.style}|${tts.piperModel}|${JSON.stringify(tts.fallback)}|${s.say}`)
    .digest('hex');

  if (cache[s.id]?.key !== key || !fs.existsSync(wav) || (cache[s.id]?.provider && cache[s.id].provider !== configuredProvider)) {
    const raw = path.join(VO, `${s.id}.raw`);
    // One unified fallback chain per line: walk the resolved provider's
    // chain in order (the same CHAINS used at resolution — say → Piper →
    // ElevenLabs; MiniMax → Piper → say; ElevenLabs → Piper → say;
    // Piper → say), skipping voices the preflight found unavailable, and
    // then the UNIVERSAL list (ElevenLabs → Piper → say → MiniMax) on
    // chain exhaustion, so a usable voice never sits unused while a line
    // goes silent. A provider that passed preflight but fails at runtime
    // degrades to the next voice in the chain and says so out loud.
    // ElevenLabs is skipped for a line when the free quota would be
    // exceeded, not failed. A line goes silent only when every voice in
    // the chain fails — the run never reaches here with no voice at all:
    // the preflight above skips narration and the video builds
    // music-only/silent instead of erroring on the first line.
    // The provider that actually produced the clip is stored on the cache
    // entry, since a fallback line keeps the requested provider's key.
    const renderLine = async () => {
      const UNIVERSAL = ['elevenlabs', 'piper', 'say', 'minimax'];
      const lineChain = [...new Set([...(CHAINS[provider] ?? [provider, 'piper', 'say']), ...UNIVERSAL])]
        .filter((p) => availableProviders.includes(p));
      for (const candidate of lineChain) {
        if (candidate === 'elevenlabs') {
          const usage = readUsage();
          if (usage.charsUsed + s.say.length > ELEVENLABS_MONTHLY_CHARS) {
            console.log(`  ! ${s.id}: ElevenLabs free quota would pass ${ELEVENLABS_MONTHLY_CHARS} chars this month (${usage.charsUsed} used) — trying the next voice for this line`);
            continue;
          }
          try {
            await elevenlabsTo(s.say, raw);
            recordUsage(s.say.length);
            return 'elevenlabs';
          } catch (e) {
            console.log(`  ! ${s.id}: ${String(e).split('\n')[0]} — trying the next voice for this line`);
            continue;
          }
        }
        try {
          if (candidate === 'minimax') await minimaxTo(s.say, raw);
          else if (candidate === 'piper') await piperTo(s.say, raw);
          else await sayTo(s.say, raw);
          return candidate;
        } catch (e) {
          console.log(`  ! ${s.id}: ${String(e).split('\n')[0]} — trying the next voice for this line`);
        }
      }
      // Every voice in the chain failed (or the chain was empty). Returning
      // null marks the line silent — the loop below gives it an estimated
      // length and the video still builds. The video NEVER aborts on a
      // voice failure.
      console.log(`  ! ${s.id}: no voice provider could render this line; scene will be silent with an estimated length`);
      return null;
    };
    // Defensive: any unexpected throw inside renderLine degrades to the
    // same silent-line path, never to a failed run.
    let usedProvider = null;
    try {
      usedProvider = await renderLine();
    } catch (e) {
      console.log(`  ! ${s.id}: voice failed (${String(e).split('\n')[0]}) — scene will be silent with an estimated length`);
      usedProvider = null;
    }
    if (usedProvider === null) {
      const words = s.say.trim().split(/\s+/).filter(Boolean).length;
      const est = Number(Math.max(2, words / 2.5).toFixed(3));
      total += est + cfg.gapMs / 1000;
      out.push({ id: s.id, kind: s.kind, say: s.say, dur: est, hasAudio: false });
      failedLines += 1;
      console.log(`${s.id.padEnd(11)} ${est.toFixed(2)}s (estimated, no voice)`);
      continue;
    }
    // Trim the silence the synthesiser leaves at either end, then level every
    // clip identically so no beat sits quieter than its neighbours. Wrapped:
    // a corrupt/empty clip from a runtime-failing provider (ffmpeg or the
    // probe throwing on a bad wav) degrades to a silent line with an
    // estimated length, exactly like a failed provider call — it never
    // aborts the video. A partial wav is removed so a later run does not
    // mistake it for a good clip.
    try {
      execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', raw,
        '-af', 'silenceremove=start_periods=1:start_silence=0.05:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_silence=0.12:start_threshold=-50dB,areverse,loudnorm=I=-18:TP=-2:LRA=11',
        '-ar', '48000', '-ac', '1', wav]);
      const dur = Number(probe(wav).toFixed(3));
      // An all-silence clip trims to nothing and probes as NaN — that is an
      // empty clip, not a measurable one: throw so the catch below degrades
      // the line to a silent estimated length instead of writing NaN into
      // the manifest (which JSON would turn into null and break the timeline).
      if (!Number.isFinite(dur)) throw new Error('probe returned no duration (empty clip after silence trim)');
      cache[s.id] = { key, provider: usedProvider, dur };
      built += 1;
      try { fs.unlinkSync(raw); } catch { /* scratch file; a stale one is re-rendered next run */ }
    } catch (e) {
      console.log(`  ! ${s.id}: audio post-processing failed (${String(e).split('\n')[0]}) — scene will be silent with an estimated length`);
      for (const f of [wav, raw]) { try { fs.unlinkSync(f); } catch { /* already gone */ } }
      const words = s.say.trim().split(/\s+/).filter(Boolean).length;
      const est = Number(Math.max(2, words / 2.5).toFixed(3));
      total += est + cfg.gapMs / 1000;
      out.push({ id: s.id, kind: s.kind, say: s.say, dur: est, hasAudio: false });
      failedLines += 1;
      console.log(`${s.id.padEnd(11)} ${est.toFixed(2)}s (estimated, no voice)`);
      continue;
    }
  }

  // A cached duration must be finite: a corrupt or hand-edited cache entry
  // must not write NaN into the manifest (which JSON turns into null and
  // breaks the timeline). Re-probe the wav that is on disk; if that fails
  // too, degrade to a silent line with an estimated length, exactly like a
  // failed provider call.
  let d = cache[s.id].dur;
  if (!Number.isFinite(d)) {
    try {
      d = Number(probe(wav).toFixed(3));
      if (!Number.isFinite(d)) throw new Error('probe returned no duration');
      cache[s.id].dur = d;
    } catch (e) {
      console.log(`  ! ${s.id}: cached duration is not a number and the clip could not be probed (${String(e).split('\n')[0]}) — scene will be silent with an estimated length`);
      const words = s.say.trim().split(/\s+/).filter(Boolean).length;
      const est = Number(Math.max(2, words / 2.5).toFixed(3));
      total += est + cfg.gapMs / 1000;
      out.push({ id: s.id, kind: s.kind, say: s.say, dur: est, hasAudio: false });
      failedLines += 1;
      console.log(`${s.id.padEnd(11)} ${est.toFixed(2)}s (estimated, no voice)`);
      continue;
    }
  }
  total += d + cfg.gapMs / 1000;
  out.push({ id: s.id, kind: s.kind, say: s.say, dur: d, hasAudio: true });
  console.log(`${s.id.padEnd(11)} ${d.toFixed(2)}s`);
}

fs.writeFileSync(cachePath, JSON.stringify(cache, null, 2));
// `narration` is the manifest Video.tsx renders from: 'full' when every
// line has audio, 'partial' when some lines went silent (voice failed at
// runtime), 'none' when no line has audio. `musicBed` starts false here;
// build.mjs sets it true after the music step if the music block is present
// and public/music/bed.wav exists. Per-shot `hasAudio` lets Video.tsx skip the <Audio> element for
// a silent line instead of referencing a wav file that does not exist.
const narration = failedLines === 0 ? 'full' : failedLines === out.length ? 'none' : 'partial';
fs.writeFileSync('src/vo-durations.json', JSON.stringify({ gapMs: cfg.gapMs, narration, musicBed: false, shots: out }, null, 2));
console.log(`\nvoice: ${provider}${provider === 'minimax' ? ` · ${tts.voice} · ${tts.model}` : ''}${provider === 'elevenlabs' ? ` · ${tts.voice ?? '21m00Tcm4TlvDq8ikWAM'} · ${tts.model ?? 'eleven_multilingual_v2'}` : ''}`);
if (provider === 'elevenlabs') {
  const u = readUsage();
  console.log(`ElevenLabs free quota: ${u.charsUsed}/${ELEVENLABS_MONTHLY_CHARS} chars used in ${u.month}`);
}
console.log(`${built} clip(s) synthesised, ${out.length - built - failedLines} cached${failedLines > 0 ? `, ${failedLines} silent (no voice)` : ''}`);
if (failedLines > 0) {
  console.log(`! ${failedLines} of ${out.length} line(s) could not be voiced — those scenes are silent with estimated lengths. Note the missing narration in the final report; re-running \`npm run script\` with a working voice provider restores them.`);
}
console.log(`narration total (with gaps): ${total.toFixed(1)}s`);
