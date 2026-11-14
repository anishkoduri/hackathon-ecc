# Fix #22 §12 — Bang Motion port into pitch-deck-video (/demo): implementation report

**Agent:** §12 implementation agent. **Date:** Nov 12, 2026.
**Staged source edited:** `new-skills/pitch-deck-video/SKILL.md` only.
**Built tree untouched.** `build.sh` not run. No bang-motion skill created.
No disposition-table rows added (per task: Bang Motion is a skill-port
addition recorded separately; the 144-item table stands).

## 1. Live verification (Nov 12, 2026)

Source: GitHub repo page (crawled Nov 12, 23:11 UTC) + independent review
(reviewramble.com/bang-motion, answers checked Nov 7, 2026).

| Fact | Verified value |
| --- | --- |
| Repo | `https://github.com/bangtutorial/bang-motion` |
| License | MIT (repo page: "License: MIT License (MIT)"; LICENSE file present) |
| Current commit (HEAD) to pin | `c1aa65e921c970d858705fcb4a53a8294d1a4131` |
| Commits | 3 total, all dated Sep 15, 2026 |
| Created | Sep 5, 2026 |
| Releases / tags | 0 releases, 0 tags — there is NO GitHub release or tag to pin |
| Version | `1.19.0` exists only as a badge / manifest version (landed Sep 15, 2026); do not record it as a release |
| Stars / forks / watchers | 2,093 / 245 / 7 |
| GSAP version (as found upstream) | 3.12.5 (jsDelivr CDN in delivered index.html) |
| Three.js version (as found upstream) | 0.161.0 (jsDelivr CDN in delivered index.html) |
| Upstream output | Single `index.html`, autoplay + loop, `?debug=1` scrub bar, optional frame-by-frame MP4 export (Node + puppeteer + ffmpeg) |
| Open PRs / issues | 1 open PR (Remotion as a second output, unmerged since Sep 23, 2026), 1 open issue |

**Pin for the integrator (build.sh pattern — cf. the 6 clone SHAs at
build.sh lines 29–44, `pin_clone`/`pin_checkout`):**

```
BANG_PIN="c1aa65e921c970d858705fcb4a53a8294d1a4131"
# bangtutorial/bang-motion — MIT, no tags; SHA is the only pin available.
# fetch_repo "bangtutorial/bang-motion" "bang-motion" "$BANG_PIN"
```

Note for the integrator: unlike ECC / ui-ux-pro-max / chwezi-dev-engine,
Bang Motion has no tags at all, so the SHA pin follows the same rule as the
other three tag-less repos in build.sh ("a SHA is the only pin available").
No clone was made into the workspace (a pin is a SHA record, not a copy).
Whether the repo is fetched at build time at all is the integrator's call:
the rules are ported into pitch-deck-video and the repo is not a live
dependency; the pin exists so the port's source is frozen and auditable.

## 2. Explainer-count resolution: SIX is the true count

- Upstream subtitle / manifest: "five explainer styles".
- Upstream README body ("What you can make" table + "6 explainer styles —
  each with its own starter"): **six** — Continuous action, Cartoon collage,
  Visual journalism, White catalog, Vintage sketch, Cartoon stage.
- The independent review confirms six, each with its own starter file, and
  notes the manifest still promises five.
- **Resolution: six.** The port lists six (SKILL.md line 416). The "five" is
  a stale subtitle/manifest upstream; recorded here so the manifest can note
  the mismatch without re-opening it.

## 3. Staleness note (caveat, not a blocker)

Repo created Sep 5, 2026; all 3 commits dated Sep 15, 2026; nothing merged
since. One open PR (Remotion second output, Sep 23, 2026, unmerged — there
is no upstream Remotion output to import) and one open issue. The rules are
ported into pitch-deck-video; the repo is not a live dependency that needs
upstream updates. Pin the SHA above and record the staleness in the manifest.

## 4. Language note

Upstream README is in English. SKILL.md (~39 KB, ~10k tokens), the
changelog, and most reference files are in Indonesian. The port is in
English, distilled from the English README plus the independently verified
rule summaries (anti-slide checks, structural bans, 30px rule). No upstream
file was copied.

## 5. Per-item placement (all in `new-skills/pitch-deck-video/SKILL.md`)

File was 505 lines before; 837 lines after. Every anchor occurs exactly
once (verified by grep after editing). Banned-term grep over the edited
file: 0 hits (case-insensitive: the seven banned terms). No other skill
touched; built tree untouched.

| # | Ported item | Anchor | Placement (file:line) |
| --- | --- | --- | --- |
| 1 | Anti-slide rules (7 checks, verbatim as checks) | `BANG_ANTISLIDE_F22` | SKILL.md:254 (section `### Anti-slide checks`) |
| 2 | QA pointer to the anti-slide checks (BLOCKING) | — (name reference only, anchor kept unique) | SKILL.md:200 (step 6 QA checklist bullet, added) |
| 3 | A/V-table extension: kinetic type + camera moves go IN the table | — (inside F5 bullet + §12 section) | SKILL.md:199 (F5 bullet, sentence added) + SKILL.md:254–286 |
| 4 | One-world / camera / persistent-subject architecture | `BANG_ONEWORLD_F22` | SKILL.md:288 |
| 5 | Style-direction menu, 10 directions | `BANG_STYLES_F22` | SKILL.md:311 (table, 10 rows + header) |
| 6 | Opener concepts, 19 | `BANG_OPENERS_F22` | SKILL.md:344 (numbered list, 19 items — verified count) |
| 7 | Kinetic typography (5 techniques as §10 directives) | `BANG_KINETIC_F22` | SKILL.md:380 |
| 8 | Explainer styles, 6 (resolved count) | `BANG_EXPLAINER_F22` | SKILL.md:416 (table, 6 rows + header) |
| 9 | Section header + source pin + boundary + no-second-toolchain + pinned-versions rules | — | SKILL.md:211–252 |
| 10 | D19 six-dimension reason per rule group | — | 6 blocks: SKILL.md:280, 301, 335, 372, 407, 436 — each verified to name all six dimensions (Motion / Theme / Texture / Visuals / Techniques / Colors), each dimension a reason or an explicit `none — <reason>` |

Style-direction names use the README's full names (Cinematic dark, Poster
color-block, Editorial light, Paper & print, Retro / analog, Brutalist mono,
Pastel playful, Luxury dark, Flat pop with photos, Grainy gradient).
Opener-concept names use the README's table (19, verbatim names).
Kinetic techniques are distilled with exact parameters per §10 (effect +
duration + easing + distance/scale + settle hold): word slam on the beat,
split-text reveal, mask reveal, scale pop, letter stagger (close sentence
only).

Additional upstream details ported into the checks (from the verified rule
summaries): at least two transition types with one in real depth (no flat
block wiping the frame); background layered, never flat; motion every second
(no dead stills).

## 6. Fit-check boundaries stated in the ported text

- **Film stays film** (SKILL.md:223–228): /demo films the LOCAL app via
  Playwright; deployed-URL path stays removed. Bang rules govern the
  motion-graphics layer only (opener, transitions, kinetic title/hero text,
  close). How/features beats stay filmed footage; a composition replacing
  filmed footage with generated motion graphics FAILS QA.
- **No second toolchain** (SKILL.md:230–236): rules implemented in this
  skill's Remotion compositions; no second video pipeline, no bang-motion
  skill. Upstream's Remotion-output PR unmerged since Sep 23, 2026 — no
  upstream Remotion output to import.
- **Pinned versions, never unpinned latest** (SKILL.md:238–246): GSAP
  3.12.5 / Three.js 0.161.0 as found upstream; vendor locally where the
  build is offline-first; fonts stay self-hosted static (fix #19/#21).
- **Existing /demo rules untouched:** F1 (motion graphics never replace
  feature coverage), F2/F3/F4 untouched; F5 extended only by adding kinetic
  type + camera moves as A/V-table rows (SKILL.md:199); F6 stated explicitly
  in the kinetic section — the opener is a beat inside the 130s cap, never
  extra runtime (SKILL.md:403–404). Voice rules, $10 budget cap, local-only
  filming untouched.

## 7. §11 version-alignment flag (do NOT guess — integrator action)

**FLAG:** GSAP 3.12.5 and Three.js 0.161.0 are Bang Motion's versions as
found upstream (recorded in the port). A sibling agent is concurrently
pinning GSAP / three.js versions for §11 (libraries). GSAP and three.js
must converge on **ONE pinned version each across §11 and §12**. This
report does not know §11's pins and does not invent them. The integrator
must reconcile: if §11 pins differ from 3.12.5 / 0.161.0, pick one version
per library, record the choice, and update the §12 text (SKILL.md:214–220
and :238–246) to the converged pins. Until then the §12 text records Bang's
versions as found, flagged as pending convergence.

## 8. Deviations proposed

None. Every §12 item in the SPEC was ported as specified. Two judgement
calls, recorded (not deviations):

1. **Placement:** the whole port lives in one compact section in SKILL.md
   (lines 211–447) plus two one-line pointers in the existing QA checklist
   (lines 199–200), rather than scattering across `references/` — per the
   task's "prefer one compact section; do not scatter". No reference file
   was needed; the content belongs in SKILL.md beside the composition/QA
   rules it extends.
2. **Direction names:** used the README's full direction names (e.g.
   "Poster color-block", "Editorial light") rather than the SPEC's
   shortened forms ("poster block", "editorial") — the README is the
   verified upstream source; the shortened forms are the same ten
   directions.

## 9. Self-verification performed

- Re-read the edited SKILL.md sections after writing; re-ran all greps
  cited above before reporting.
- Anchors: each of the six `BANG_*_F22` anchors occurs exactly once.
- Opener concepts: 19 numbered items counted. Style directions: 10 table
  rows counted (+ header). Explainer styles: 6 table rows.
- D19: 6 reason blocks, each containing all six dimensions (grep counts
  6/6/6/6/6/6 across Motion/Theme/Texture/Visuals/Techniques/Colors).
- Banned terms: 0 hits in the edited file (case-insensitive).
- Upstream facts re-verified live Nov 12 (repo page + independent review);
  commit SHA, license, version-badge-only status, 3-commit history, and
  GSAP/Three.js versions all confirmed from those sources.
- `build.sh` NOT run (integrator rebuilds once). `hackathon-ecc/` untouched.
  `fix11/fix11-stage.py` not run. No other skill edited.
