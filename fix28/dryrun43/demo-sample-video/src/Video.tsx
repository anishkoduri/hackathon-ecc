import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, interpolate } from 'remotion';
import { FPS, SCENES, TOTAL, TOTAL_FRAMES, APP_END, MUSIC } from './timeline';
import voDurations from './vo-durations.json';
import { Screen } from './parts/Screen';
import { Captions } from './parts/Captions';
import { Hook } from './scenes/Hook';
import { Arch } from './scenes/Arch';
import { Close } from './scenes/Close';
import { C } from './theme';
import './fonts';

const f = (s: number) => Math.round(s * FPS);

// Audio guards — the video is a required deliverable and must NEVER abort
// on a missing audio file. `src/vo-durations.json` is the manifest tts.mjs
// writes: `narration` is 'none' when no voice provider existed (estimated
// beat lengths, no wav files on disk), 'partial' when some lines failed at
// runtime, and each shot carries `hasAudio`. `musicBed` is true only when
// public/music/bed.wav exists (set by build.mjs after the music step).
// This manifest — not a filesystem check — is the guard, because during a
// Remotion render components run server-side, where `getStaticFiles()` and
// `fs` are unavailable. A scene with no audio simply renders silent; a
// missing bed simply renders without music.
// Fail CLOSED on an unknown shot id or a missing flag: `?.hasAudio === true`
// is false for undefined, so a scene with no entry in the manifest never
// renders an <Audio> for a wav file that does not exist. (The music guard
// below, `VO.musicBed === true`, is fail-closed the same way.)
const VO = voDurations as { narration?: string; musicBed?: boolean; shots?: { id: string; hasAudio?: boolean }[] };
const HAS_NARRATION = VO.narration !== 'none';
const hasVo = (id: string): boolean =>
  HAS_NARRATION && VO.shots?.find((s) => s.id === id)?.hasAudio === true;
const HAS_MUSIC_BED = Boolean(MUSIC) && VO.musicBed === true;

// Card scenes are keyed by shot id, so adding a card in shots.json is one entry
// here and nothing else.
const CARDS: Record<string, React.FC<{ dur: number }>> = { hook: Hook, arch: Arch, close: Close };

const Progress: React.FC = () => {
  const p = useCurrentFrame() / TOTAL_FRAMES;
  return <div style={{ position: 'absolute', left: 0, bottom: 0, height: 4, width: `${p * 100}%`, background: C.accent, opacity: 0.85 }} />;
};

export const CompanionVideo: React.FC = () => (
  <AbsoluteFill style={{ background: C.bgDeep }}>
    {/* Footage sits underneath and reads absolute time; see parts/Screen.tsx. */}
    <Screen />

    {SCENES.filter((s) => CARDS[s.id]).map((s) => {
      const Card = CARDS[s.id];
      const isLast = s.id === SCENES.at(-1)?.id;
      const dur = isLast ? TOTAL - s.start : s.dur;
      return (
        <Sequence key={s.id} from={f(s.start - 0.35)} durationInFrames={f(dur + 0.35)} name={s.id}>
          <AbsoluteFill style={{ opacity: 1 }}>
            <Card dur={dur} />
          </AbsoluteFill>
        </Sequence>
      );
    })}

    {/* Narration: only for scenes whose wav file exists (see hasVo above).
        A scene with no voice renders silent on its estimated length. */}
    {SCENES.filter((s) => hasVo(s.id)).map((s) => (
      <Sequence key={`a-${s.id}`} from={f(s.start)} name={`vo:${s.id}`}>
        <Audio src={staticFile(`vo/${s.id}.wav`)} />
      </Sequence>
    ))}

    {/* Music bed: ducked under the voice, lifted for the open and the close.
        Levels live in shots.json -> music.gain. Delete that block to go without.
        Rendered only when a bed was actually fetched (HAS_MUSIC_BED); if the
        music step failed, the video renders without a bed rather than
        aborting on a missing file. */}
    {HAS_MUSIC_BED ? (
      <Audio
        src={staticFile('music/bed.wav')}
        volume={(fr) => {
          const t = fr / FPS;
          const g = MUSIC!.gain;
          return interpolate(
            t,
            [0, 2.2, 4.2, APP_END - 0.3, APP_END + 1.2, TOTAL - 1.2, TOTAL],
            [0, g.open, g.under, g.under, g.close, g.close, 0],
            { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
          );
        }}
      />
    ) : null}

    <Captions />
    <Progress />
  </AbsoluteFill>
);
