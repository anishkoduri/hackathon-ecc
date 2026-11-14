#!/usr/bin/env python3
"""fix18.py -- implement fix #18 (pitch-deck-video: 7 video criteria) in the
STAGED sources; build.sh copies pitch-deck-video verbatim (no runtime
patches), so there is no build.sh block for this fix.

Usage: python3 fix18/fix18.py            (preflight + apply + self-check)
Exits non-zero if any anchor is missing or appears != 1 time.

Edits (SPEC fix18/SPEC.md, rules F1-F6):
  SKILL.md: frontmatter duration, step 3 (features/cuts + best states),
    step 4 (theme.source + arch stack + spoken stack line + F6 caps +
    allocation table), arc (Edge beat, How grows with features),
    pacing, step 6 (coverage / A-V table / gorgeousness / runtime / mix).
  references/shots-reference.md: features/cuts rows + section, arch node
    stack, theme.source + vignette, music under-gain guidance, gapMs note.
  template/shots.example.json + template/shots.json: seed features/cuts,
    stack-labelled arch nodes, Edge shot, seed arch line naming the stack.
  template/src/scenes/Arch.tsx: render the stack label.
  template/scripts/qa.mjs: coverage table + missing-beat flag, theme-vs-seed
    comparison, per-shot A/V table skeleton, under-gain warning, total
    runtime print + BLOCKING check over 2:10 (ceiling 2:30), vignette print.
  commands/demo.md: 1:30-1:50 -> under 2:10 (F6 regime change).
"""
import json
import os
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
STAGED = os.path.join(PLUGIN, "new-skills/pitch-deck-video")

# ---------------------------------------------------------------- constants

STEP3_ADD = """Before storyboarding, enumerate the feature list: every must-have from `docs/scope.md`'s must-have list, plus every route screenshotted above (a route with no must-have feature behind it is not a feature). Write the list into `shots.json` as a `features` array — `[{name, beat}]`, one entry per must-have feature, `beat` being the shot id that shows it — and a `cuts` array — `[{name, reason}]` for any must-have feature deliberately left out of the video. A feature is 'shown' only if it is visible on camera AND named (narration or on-screen caption) in its beat. If the feature count would push the video past the 2:10 cap (step 4), cut the least important features into the `cuts` array with a reason — a feature cut from the video is a reported decision, never a silent omission.

Use the screenshots to pick the best state per beat, not only to verify the wow: for each beat, the shot's state is the best-looking state that shows the claim — populated data, the prettiest route, the wow at its best. Never put an empty state on camera to stand for a full one (the Don't below stays: never describe a screen as full when this account's version of it is empty)."""

STEP4_THEME_ARCH = """Pull the `theme.colors` from the app's own design tokens so the cards and the footage read as one piece, and record the token source (file + values) in `shots.json` as `theme.source` — the QA step fails the video if the theme is still the seed theme with no recorded source. Fill `cards.arch.nodes` with the real architecture — which boxes are model calls and which are deterministic code — and give each node its `stack` label: the concrete framework / model / service / infra that box runs on (e.g. `"Next.js 15"`, `"GPT-5"`, `"Supabase"`), taken from the app's `package.json` + `docs/decision-record.md` / `docs/scope.md`, never invented. That beat is what separates a demo from a wrapper, and judges look for it. Its narration must name the stack in one spoken phrase ("Built on Next.js, GPT-5, and Supabase") — one phrase, not a list read aloud (the 'Never list' rule stays). If the app has no recorded stack, the arch beat says the framework only and notes the gap in the final report."""

CAPS_F6 = """- **12–16 beats; the video is under 2:10 (130 seconds) — hard rule.** The total is computed from the MEASURED narration durations (`src/vo-durations.json`), plus `gapMs` per beat and the card durations — never from estimates. Over 2:10 is a BLOCKING finding in QA: re-cut (shorten lines, drop a low-priority feature beat into the `cuts` array, tighten a beat). Absolute max 2:30 (150 seconds), never exceeded — no approval, no exception, no 'one more beat' may push a video past it; if a storyboard would exceed 2:30 even after cutting, re-cut it (fewer features, shorter lines), never extend it. Leave ~10 seconds of room. Lengths by artefact: the video is under 2:10; the live demo storyboard is 2–4 min; the pitch storyboard is <90s. Do not mix them up — the video cap governs this skill, the longer live-demo storyboard and the shorter pitch storyboard belong to the pitch, not the video."""

ALLOCATION_F6 = """**Write the time budget before writing the lines.** Before writing `shots.json`, write the section budget first, then write lines to fit it — never the reverse (writing lines and discovering the total afterwards). The 130-second budget is divided across the arc by importance, not evenly (times are narration + gaps for that section, in seconds):

| Section | Beats | Seconds | Why |
| --- | --- | --- | --- |
| Problem | 1 | 8–10 | The pain, in the user's words — short, sharp |
| Wow | 1–2 | 14–18 | The opening, the reason to keep watching — deserves time |
| Edge (uniqueness) | 1 | 8–10 | One sentence, the differentiator |
| How / features | 6–9 | 55–65 | The LARGEST share — every feature shown, the program proved |
| Proof (arch + stack) | 1–2 | 12–15 | Credibility beat, stack named aloud |
| Close | 1 | 6–8 | One sentence left on screen |
| Unallocated room | — | ~10 | The existing leave-room rule, kept |

Totals: 113–126s of content + ~10s room ≈ under 2:10. The features' share is the largest because the spare beats go to features (step 3). If a section's lines would exceed its budget, shorten the lines or move a feature to `cuts`; do not borrow from another section's budget without recording it in the final report."""

ARC_F1F3 = """1. **Problem** — one beat, in the user's words, before the product name exists. The pain, not the category.
2. **Wow** — the opening shot above: the product doing the impossible thing, live, with the number said out loud.
3. **Edge** — one beat, one sentence: the one thing no alternative does, in the user's words, with the alternative named or clearly implied ("unlike X, this…"). Shown live where possible — a `focus` on the differentiating element, or the wow footage carrying it. The Edge claim comes from `docs/decision-record.md` / `docs/scope.md` (the wow test: "does this make a judge stop and stare?") or from the user. If none is recorded, ask for one line; never invent a competitor claim — the fallback is stating the wow's distinguishing fact, not a fabricated comparison.
4. **How** — two to four beats along the golden path: one user, one task, each beat one action and one outcome. Never two features in one beat. PLUS one beat per remaining must-have feature from the `features` array (step 3), drawn from the 12–16 beat budget — the budget's spare beats go to features, not to padding the golden path. A feature counts as shown only if it is visible on camera AND named in its beat.
5. **Proof** — the arch card beat: which boxes are model calls and which are deterministic code, each node labelled with its stack, and the stack named aloud in one phrase. This is the credibility beat; judges look for it, and it is what separates a demo from a wrapper.
6. **Close** — one sentence left on screen (the tagline, said out loud)."""

STEP6_QA = """Check: **`capture/marks.json → warnings` is empty** (a missing selector is a warning, not a crash — you still get a video, and a list of what broke). Then read the `qa.mjs` printout and work through it in order:

- **Coverage table complete** — every must-have feature has a beat or a recorded cut (`shots.json` `features` / `cuts`). A feature whose beat id is missing from `shots.json` or whose beat produced no footage is a BLOCKING finding.
- **Per-beat A/V table** — for every shot, the claim in its `say` line against the stills: does the frame support it? Complete the table `qa.mjs` prints while reading the contact sheets and record it in the video project (qa notes). A 'no' is a BLOCKING finding: re-film or rewrite the line; the video does not ship with an unmatched claim.
- **Gorgeousness** — (a) no generic seed look: the cards read as the app's own palette/fonts, not the seed theme; (b) footage shows the app's best-looking states: populated data, the prettiest route, the wow at its best, chosen from the step-3 screenshots — never an empty state on camera; (c) vignette matches the app: `theme.vignette` 0 for light apps, recorded choice either way.
- **Runtime** — `qa.mjs` prints the total from the measured narration; over 2:10 is BLOCKING (re-cut), and 2:30 is the absolute ceiling no version may cross.
- **Mix** — listen to a 10-second sample from the middle of the video (where the music is `under` the voice) and confirm the narration is intelligible over the bed; record the check. `qa.mjs` warns if `music.gain.under` exceeds 0.20 — above that the bed risks burying the voice.
- **Theme pulled, not seeded** — the theme check fails the QA if `shots.json` still carries the seed theme with no recorded `theme.source`.

Then the stills themselves: does each caption land on a frame that supports it? Any blank or white frames? Is small text legible, or does it need a `focus`?"""

FEATURES_CUTS_SECTION = """## features / cuts

From `docs/scope.md`'s must-have list plus every route screenshotted in step 3 (a route with no must-have feature behind it is not a feature).

```json
"features": [{ "name": "Automatic scheduling", "beat": "result" }],
"cuts": [{ "name": "Admin dashboard", "reason": "would push the video past the 2:10 cap; shown in the live demo instead" }]
```

One entry per must-have feature; `beat` is the shot id that shows it. `qa.mjs` prints the coverage table (feature → beat, plus the cuts list) and flags any feature whose beat id is missing from `shots.json` or whose beat produced no footage. If a feature is cut, say so in the final report.

"""

ARCH_NODES_SECTION = """## cards — arch nodes

`cards.arch.nodes[]` is the real architecture: each node is `{label, note, kind}` where `kind` is `in` (input), `llm` (model call), `code` (deterministic code), or `out` (output) — plus an optional `stack` label: the concrete framework / model / service / infra that box runs on (e.g. `"Next.js 15"`, `"GPT-5"`, `"Supabase"`), taken from the app's `package.json` + `docs/decision-record.md` / `docs/scope.md`, never invented. `Arch.tsx` renders the stack label under each node label in mono. The arch beat's narration names the stack in one spoken phrase ("Built on Next.js, GPT-5, and Supabase") — one phrase, not a list read aloud.

"""

SEED_FEATURES_CUTS = """  "features": [
    {
      "name": "Get the booked week back",
      "beat": "result"
    }
  ],
  "cuts": [
    {
      "name": "Example cut — a must-have left out of this video",
      "reason": "would push the video past the 2:10 cap; shown in the live demo instead"
    }
  ],
"""

SEED_EDGE_SHOT = """    {
      "id": "edge",
      "kind": "app",
      "say": "The edge: the one thing no alternative does. Name the alternative, then the difference, in one sentence.",
      "do": [
        {
          "focus": {
            "sel": "text=Result",
            "pad": 300,
            "max": 1.7,
            "ms": 900
          }
        }
      ]
    },
"""

QA_COMPUTE = """// --- fix #18 QA checks: runtime, coverage, theme, A/V table, mix --------
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

"""

QA_TAIL = """console.log(`\\n${sheets.length} contact sheet(s):`);
for (const s of sheets) console.log(`  ${s}`);

console.log('\\n--- fix #18 QA (read these before the sheets) ---');
console.log(`Total runtime (measured narration + gaps + lead/tail): ${totalSec.toFixed(1)}s — hard rule under 2:10 (130s), absolute ceiling 2:30 (150s).${totalSec > 130 ? ' BLOCKING: over 2:10 — re-cut.' : ''}`);
console.log('\\nCoverage table (feature → beat):');
if (!features) console.log('  (no features array in shots.json — BLOCKING, see below)');
for (const r of coverageRows) console.log(`  ${r.name} → ${r.beat} — ${r.status}`);
console.log('  Cuts (recorded, with reasons):');
for (const c of cuts) console.log(`  ${c.name} — ${c.reason}`);
if (!cuts.length) console.log('  (none)');
console.log(`\\nTheme: ${themeIsSeed ? 'identical to the seed theme' : 'pulled from the app tokens'}${cfg.theme?.source ? ` — source recorded: ${cfg.theme.source}` : ' — no theme.source recorded'}`);
console.log(`Vignette: theme.vignette = ${cfg.theme?.vignette ?? '0.3 (default)'}${cfg.theme?.vignette === undefined ? ' — record the choice (0 for light apps)' : ''}`);
if (underGain !== undefined && underGain > 0.20) console.log(`\\nWARNING: music.gain.under is ${underGain} (over 0.20) — the bed risks burying the voice. Do the 10-second mix listen from the middle of the video and confirm the narration is intelligible over it.`);
console.log('\\nPer-beat A/V table — complete this while reading the sheets (claim → stills support it?):');
for (const s of cfg.shots ?? []) console.log(`  ${s.id} [${s.kind}] "${String(s.say).slice(0, 70)}" — supports it: ___`);
console.log('  Record the completed table in the video project (qa notes). A "no" is BLOCKING: re-film or rewrite the line; the video does not ship with an unmatched claim.');
if (blocking.length) {
  console.log(`\\nBLOCKING findings (${blocking.length}):`);
  for (const b of blocking) console.log(`  BLOCKING — ${b}`);
} else {
  console.log('\\nNo BLOCKING findings from the automated checks.');
}
console.log('\\nRead the sheets as images. Check, in order:');
console.log('  1. capture/marks.json -> warnings is empty, and capture/failures/ is empty');
console.log('  2. every shot is on the page you think it is');
console.log('  3. no spinners, skeletons or empty states');
console.log('  4. every claim in the narration matches what is on screen');
console.log('  5. captions legible, small text legible or zoomed');
console.log('  6. gorgeousness: cards read as the app\\'s own palette/fonts (not the seed); footage shows the app\\'s best-looking states, never an empty state; vignette matches the app');
console.log('  7. mix: listen to a 10-second sample from the middle of the video and confirm the narration is intelligible over the bed');
if (blocking.length) process.exitCode = 1;
"""

# ---------------------------------------------------------------- subs
# Each entry: (relative path under STAGED, old text, new text).
# Every old must occur exactly once in its file, or the run aborts.

SKILL = "SKILL.md"
REF = "references/shots-reference.md"
EX = "template/shots.example.json"
SEED = "template/shots.json"
ARCH = "template/src/scenes/Arch.tsx"
QA = "template/scripts/qa.mjs"
DEMO = "commands/demo.md"

SUBS = [
    # --- SKILL.md ---
    (SKILL,
     "Generates a narrated 1:30–1:50 product demo",
     "Generates a narrated product demo, under 2:10,"),
    (SKILL,
     "Do not write narration from the source code.\nYou are writing about what a judge will see, and only the screenshots tell you\nthat.",
     "Do not write narration from the source code.\nYou are writing about what a judge will see, and only the screenshots tell you\nthat.\n\n" + STEP3_ADD),
    (SKILL,
     "Pull the `theme.colors` from the app's own design tokens so the cards and the\nfootage read as one piece. Fill `cards.arch.nodes` with the real architecture —\nwhich boxes are model calls and which are deterministic code. That beat is what\nseparates a demo from a wrapper, and judges look for it.",
     STEP4_THEME_ARCH),
    (SKILL,
     "- **12–16 beats; the video is 1:30–1:50 total.** Under a 2:00 cap, leave 10 seconds of room. Lengths by artefact: the video is 1:30–1:50; the live demo storyboard is 2–4 min; the pitch storyboard is <90s. Do not mix them up — the video cap governs this skill, the longer live-demo storyboard and the shorter pitch storyboard belong to the pitch, not the video.",
     CAPS_F6),
    (SKILL,
     "- **One idea per beat.** The beat ends when the idea does.",
     ALLOCATION_F6 + "\n\n- **One idea per beat.** The beat ends when the idea does."),
    (SKILL,
     "1. **Problem** — one beat, in the user's words, before the product name\n   exists. The pain, not the category.\n2. **Wow** — the opening shot above: the product doing the impossible\n   thing, live, with the number said out loud.\n3. **How** — two to four beats along the golden path: one user, one task,\n   each beat one action and one outcome. Never two features in one beat.\n4. **Proof** — the arch card beat: which boxes are model calls and which\n   are deterministic code. This is the credibility beat; judges look for\n   it, and it is what separates a demo from a wrapper.\n5. **Close** — one sentence left on screen (the tagline, said out loud).",
     ARC_F1F3),
    (SKILL,
     "Pacing: at\n12–16 beats over 90–110 seconds, a beat averages 7–9 seconds;",
     "Pacing: at\n12–16 beats under 2:10, a beat averages 7–9 seconds;"),
    (SKILL,
     "Check: **`capture/marks.json → warnings` is empty** (a missing selector is a\nwarning, not a crash — you still get a video, and a list of what broke). Then:\ndoes each caption land on a frame that supports it? Any blank or white frames?\nIs small text legible, or does it need a `focus`?",
     STEP6_QA),
    # --- shots-reference.md ---
    (REF,
     "| `theme` | `colors` and `fonts` for the cards and captions. Pull from the app's own tokens. |",
     "| `theme` | `colors` and `fonts` for the cards and captions. Pull from the app's own tokens, and record the source (file + values) in `theme.source` — the QA fails the video if the theme is still the seed theme with no recorded source. `theme.vignette` (0–1, default 0.3) darkens the frame edges: set 0 for light apps and record the choice either way. |"),
    (REF,
     "| `gapMs` | Silence added after every line. 200–300 reads well. |",
     "| `gapMs` | Silence added after every line. 200–300 reads well. It counts toward the 2:10 total: measured narration + `gapMs` per beat + card durations + lead/tail — `qa.mjs` prints the total and flags over 2:10 as BLOCKING. |"),
    (REF,
     "| `shots` | The video, in order. |",
     "| `shots` | The video, in order. |\n| `features` | One entry per must-have feature: `{name, beat}` — `beat` is the shot id that shows it. A feature is 'shown' only if it is visible on camera AND named (narration or caption) in its beat. See below. |\n| `cuts` | Must-have features deliberately left out of the video: `{name, reason}`. A cut is a reported decision, never a silent omission — if the feature count would push the video past the 2:10 cap, cut the least important features here. |"),
    (REF,
     "## Actions",
     FEATURES_CUTS_SECTION + "## Actions"),
    (REF,
     "## app",
     ARCH_NODES_SECTION + "## app"),
    (REF,
     "exists (flagged in `src/vo-durations.json`).",
     "exists (flagged in `src/vo-durations.json`). `under` above 0.20 risks burying the voice — `qa.mjs` warns on it, and the step-6 mix check (a 10-second listen from the middle of the video) is the confirmation; keep `under` at or below 0.20 unless the listen says otherwise."),
]

# Seed JSON files: identical subs applied to both (they differ only in tts).
JSON_SUBS = [
    ('  "tagline": "The one sentence you want left on screen at the end.",\n  "theme": {',
     '  "tagline": "The one sentence you want left on screen at the end.",\n' + SEED_FEATURES_CUTS + '  "theme": {'),
    ('        {\n          "label": "Ranker",\n          "note": "candidates scored",\n          "kind": "llm"\n        }',
     '        {\n          "label": "Ranker",\n          "note": "candidates scored",\n          "kind": "llm",\n          "stack": "GPT-5"\n        }'),
    ('        {\n          "label": "Scheduler",\n          "note": "real calendar, real slots",\n          "kind": "code"\n        }',
     '        {\n          "label": "Scheduler",\n          "note": "real calendar, real slots",\n          "kind": "code",\n          "stack": "Next.js 15"\n        }'),
    ('        {\n          "label": "Writer",\n          "note": "the brief",\n          "kind": "llm"\n        }',
     '        {\n          "label": "Writer",\n          "note": "the brief",\n          "kind": "llm",\n          "stack": "GPT-5"\n        }'),
    ('      "say": "What is a model call and what is not. This is the credibility beat."',
     '      "say": "What is a model call and what is not. Built on Next.js and GPT-5 — this is the credibility beat."'),
    ('    },\n    {\n      "id": "arch",',
     '    },\n' + SEED_EDGE_SHOT + '    {\n      "id": "arch",'),
]
for _rel in (EX, SEED):
    for _old, _new in JSON_SUBS:
        SUBS.append((_rel, _old, _new))

SUBS += [
    # --- Arch.tsx ---
    (ARCH,
     "type Node = { label: string; note: string; kind: 'in' | 'llm' | 'code' | 'out' };",
     "type Node = { label: string; note: string; kind: 'in' | 'llm' | 'code' | 'out'; stack?: string };"),
    (ARCH,
     "// The slide judges always ask for: which boxes are model calls and which are\n// not. Nodes come from shots.json -> cards.arch.nodes.",
     "// The slide judges always ask for: which boxes are model calls and which are\n// not. Nodes come from shots.json -> cards.arch.nodes.\n// Each node may carry a `stack` label (the concrete framework / model /\n// service that box runs on), rendered under the node label in mono."),
    (ARCH,
     """                <div style={{ fontFamily: FONT.serif, fontSize: 34, color: C.text, marginTop: 14, lineHeight: 1.05 }}>{n.label}</div>""",
     """                <div style={{ fontFamily: FONT.serif, fontSize: 34, color: C.text, marginTop: 14, lineHeight: 1.05 }}>{n.label}</div>
                {n.stack ? <div style={{ fontFamily: FONT.mono, fontSize: 15, letterSpacing: '0.08em', color: col, marginTop: 8 }}>{n.stack}</div> : null}"""),
    # --- qa.mjs ---
    (QA,
     "console.log(`\\n${sheets.length} contact sheet(s):`);",
     QA_COMPUTE + "console.log(`\\n${sheets.length} contact sheet(s):`);"),
    (QA,
     "console.log(`\\n${sheets.length} contact sheet(s):`);\nfor (const s of sheets) console.log(`  ${s}`);\nconsole.log('\\nRead them as images. Check, in order:');\nconsole.log('  1. capture/marks.json -> warnings is empty, and capture/failures/ is empty');\nconsole.log('  2. every shot is on the page you think it is');\nconsole.log('  3. no spinners, skeletons or empty states');\nconsole.log('  4. every claim in the narration matches what is on screen');\nconsole.log('  5. captions legible, small text legible or zoomed');",
     QA_TAIL),
    # --- demo.md ---
    (DEMO,
     "description: Generate a narrated 1:30–1:50 product demo video of the hackathon project.",
     "description: Generate a narrated product demo video, under 2:10, of the hackathon project."),
    (DEMO,
     "Use the pitch-deck-video skill to generate a narrated 1:30–1:50 product demo video of the app in the current directory, or of the app path given after /demo.",
     "Use the pitch-deck-video skill to generate a narrated product demo video, under 2:10, of the app in the current directory, or of the app path given after /demo."),
]

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
EDITED_FILES = sorted({rel for rel, _, _ in SUBS})


def read(rel):
    with open(os.path.join(STAGED, rel), encoding="utf-8") as f:
        return f.read()


def main():
    # Preflight: every anchor exists exactly once.
    cache = {}
    for rel, old, _new in SUBS:
        if rel not in cache:
            cache[rel] = read(rel)
        n = cache[rel].count(old)
        if n != 1:
            print(f"PREFLIGHT FAIL {rel}: anchor count {n} (want 1): {old[:80]!r}")
            sys.exit(1)
    print(f"preflight OK: {len(SUBS)} anchors, all count==1")

    # Apply.
    for rel, old, new in SUBS:
        text = cache[rel]
        assert text.count(old) == 1, rel
        cache[rel] = text.replace(old, new, 1)
        assert new in cache[rel], rel
    for rel, text in cache.items():
        with open(os.path.join(STAGED, rel), "w", encoding="utf-8") as f:
            f.write(text)
    print(f"applied {len(SUBS)} subs across {len(cache)} files")

    # Self-check: seed JSONs still parse; edge shot present in both.
    for rel in (EX, SEED):
        data = json.loads(read(rel))
        assert data["features"] and data["cuts"], rel
        assert [s["id"] for s in data["shots"]] == ["hook", "setup", "result", "edge", "arch", "close"], rel
        assert [n.get("stack") for n in data["cards"]["arch"]["nodes"]] == [None, "GPT-5", "Next.js 15", "GPT-5", None], rel
        assert "Next.js and GPT-5" in data["shots"][4]["say"], rel
    print("seed JSONs parse: features/cuts present, shot order hook/setup/result/edge/arch/close, stack labels on Ranker/Scheduler/Writer")

    # qa.mjs still parses.
    r = subprocess.run(["node", "--check", os.path.join(STAGED, QA)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("node --check qa.mjs FAILED:\n" + r.stderr)
        sys.exit(1)
    print("node --check qa.mjs OK")

    # No banned terms introduced in the edited files.
    for rel in EDITED_FILES:
        low = read(rel).lower()
        hits = [b for b in BANNED if b in low]
        if hits:
            print(f"BANNED TERM in {rel}: {hits}")
            sys.exit(1)
    print(f"banned-term scan clean across {len(EDITED_FILES)} edited files")

    # Old regime gone from the skill + command (except the 90-second quota
    # examples in the voice sections, which are typical-length figures,
    # not the cap — deliberately untouched, see manifest).
    for rel in (SKILL, DEMO):
        assert "1:30–1:50" not in read(rel), rel
        assert "1:30-1:50" not in read(rel), rel
        assert "2:00 cap" not in read(rel), rel
    assert "90–110 seconds" not in read(SKILL), SKILL
    print("old regime (1:30-1:50 / 2:00 cap / 90-110s) gone from SKILL.md + demo.md")


if __name__ == "__main__":
    main()
