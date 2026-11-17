# Sweep #41 — fix #31 — INDEPENDENT SWEEP REPORT

**Verdict: SWEEP #41: CLEAN** — 0 blocking, 0 minor. The run-1 built
tree passes every check in the sweep scope: the 5 new skills are woven
into every canonical package/palette list, the stale-count sweep is
clean, the new skill dirs match the MANIFEST exactly, every inventory
§12 path exists, all 6 key URLs resolve live, no TODO/FIXME/XXX or
model-pin text sits in the new/edited files, `fix31.py` matches its
template byte-for-byte, the README and trigger coverage read 72/49 as
stated, and the GetLayers weight language is present at all six sites
the MANIFEST claims. Audit #97 (A/B) and dry-run #46 are parallel
round-1 work; their verdicts are not re-verified here.

**Scope.** Sweep of the run-1 built tree (`hackathon-ecc/`, built from
fix #30 commit cfb15f9 + fix #31 changes) + staged sources
(`new-skills/`, `new-rules/`), per the task brief: (a) weaving check,
(b) stale-count sweep, (c) orphan/consistency sweep incl. live URL
checks, (d) regression sweep, (e) GetLayers weight check. Read-only
except this report. I did not trust the coordinator's, the patch log's,
or `verify31.py`'s run-1 claims: every item below was verified by my
own greps, file reads, and counters. `verify31.py` was re-run by me
(380/380, exit 0 — see §(i)). No live-browser or Cursor-session check
beyond fetching the 6 cited URLs as page text was performed.
`build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing
was committed, pushed, or messaged. Date: Mon 2026-11-16 (Nov 17, 2026
~04:15 UTC).

---

## BLOCKING findings

None. (Numbered 41-Ax: none issued.)

---

## MINOR findings

None. (Numbered 41-Bx: none issued.)

---

## Checks table

| # | Check | Result |
|---|---|---|
| (a) | Weaving: 5 new skills in every canonical package/palette list | PASS — DESIGNPKG-AUTO (both files), palette-first, orchestrate :70, inventory §12 all include all 5; see (a) for the surface shorthands that omit them with a recorded reason |
| (b) | Stale counts: "67 skills" / frozen GetLayers counts / GSAP 3.15.0 / Hairline UI as in-scope | PASS — 0 / 0 / 0 / 0 in-scope (3 Hairline UI hits are all explicit out-of-scope disclaimers) |
| (c) | Orphan/consistency: new skill dir contents, inventory §12 paths, live URLs | PASS — dirs match MANIFEST exactly; all §12 paths exist; all 6 URLs resolve live |
| (d) | Regression: TODO/FIXME/XXX, model pins, fix31.py template, README + triggers | PASS — 0 TODO/FIXME/XXX and 0 model-pin hits in new/edited files; fix31.py == template (md5 `37577dddaebf75224b5e0b4e35ab80ef`); README 72 in all 4 lines + fix31 note; trigger coverage 72/49 |
| (e) | GetLayers weight at all 6 claimed sites | PASS — present at DESIGNPKG-AUTO (both files), design-taste-frontend :224, orchestrate :70, inventory §12, getlayers skill |
| (f) | Independent counts | PASS — 72 skills / 45 agents / 48 rules / 55 commands / 15 hooks / 49 trigger keys, reproduced by my own counts |
| (g) | Verifier re-run | PASS — `verify31.py` re-run by me: 380/380, exit 0 |
| (h) | Post-build drift | PASS — no built-tree file newer than `fix31/build-log-run1.txt` |

---

## Notes / observations (checked and cleared)

### (a) Weaving — PASS, with the surface shorthands recorded

**Canonical lists — all 5 present, verified by my own reads:**

- **DESIGNPKG-AUTO**, `skills/orchestrate/SKILL.md:35` and
  `rules/hackathon-mode.mdc:44`: package list names
  `design-taste-frontend / ui-ux-pro-max / less-flat-ui / polish-pass /
  motion-foundations / motion-patterns / motion-advanced /
  make-interfaces-feel-better / design-system / motionsites-web-builder /
  getlayers / gsap / react-bits / hairline-create / hairline-adopt`,
  with a gloss line per new resource (`GETLAYERS_F31`, `GSAP_F31`,
  `REACTBITS_F31`, `HAIRLINE_F31`), the GetLayers-consulted-FIRST
  sentence, and the USED/CONSIDERED-AND-REJECTED citation sentence.
  The palette list inside the same block puts `getlayers` first.
  The two lines are byte-identical once the leading `- ` list marker
  on the hackathon-mode line is stripped (same md5
  `6f74770f3e897b3115caecd6177ed90d`; raw lengths 3463 vs 3465) — the
  same prefix convention as the earlier fixes, not a divergence.
  `verify31.py` passes its byte-identical check on the stripped form.
- **Palette-first**, `skills/design-taste-frontend/SKILL.md:224`:
  `getlayers` FIRST ("the first-class foundation the direction leans
  on — consult its prompts before the other palette sources"), then
  `motionsites-web-builder`, the design package (`ui-ux-pro-max`,
  `less-flat-ui`, `motion-foundations`, `motion-patterns`,
  `motion-advanced`, `make-interfaces-feel-better`, `design-system`,
  `gsap`, `react-bits`, `hairline-create`, `hairline-adopt`), and the
  dealt Hallmark theme; citation sentence present (USED or
  CONSIDERED-AND-REJECTED with D19; a direction naming no GetLayers
  layer at all is a finding).
- **Orchestrate inventory paragraph**, `skills/orchestrate/SKILL.md:70`:
  "the fix #31 additions (GetLayers prompt-first layers — consulted
  FIRST in the palette inventory, the first-class foundation — GSAP
  animation, React Bits components, Hairline illustrations — see §12
  of the inventory)".
- **Design inventory §12**,
  `skills/orchestrate/references/design-inventory.md:168–186`: new
  section for the four resources, GetLayers row leads with
  "Consulted FIRST"; §1 GSAP presets row (:34) and §9 row (:146)
  point at the new usage skill (`skills/gsap/SKILL.md`, `gsap@3.15.1`).
- **Staged vs built weave lines:** the palette-first line and the
  orchestrate :70 line are byte-identical between staged and built;
  the DESIGNPKG-AUTO lines differ only by the designed pin rename
  (`grok-4.7-high` staged → `grok-4.7-extra-high` built, OWED-30-1
  class). The other staged-vs-built diffs in these three files are
  pre-existing drift of the same class (e.g. `code-reviewer` vs
  `code-reviewer` agent with path, design-taste-frontend scope
  wording), not fix #31 changes.

**Sites that still omit the 5 — listed, with the reason each is not a
finding.** These are surface-conditional shorthands, not canonical
package/palette lists; every one of them also omits
`motionsites-web-builder` (fix #27), i.e. the omission predates fix
#31 and is not a fix #31 regression; each delegates to the canonical
list or the inventory:

- `skills/orchestrate/SKILL.md:66` (step 3 slice briefs) and `:139`
  (routing-table row 10, the design-package rule): per-surface
  subsets — landing (`design-taste-frontend` + theme + `ui-ux-pro-max`
  + polish-pass + Harmony), app/dashboard (`ui-ux-pro-max` +
  polish-pass + Harmony + `less-flat-ui` where dull/flat), motion
  (+ `make-interfaces-feel-better`), design-system (+
  `design-system`). No GSAP/React Bits/GetLayers/Hairline row, and
  no motionsites row either.
- `skills/feature-expansion/SKILL.md:156` (UI rule) and `:200`
  (reference table): "full design package: `ui-ux-pro-max` +
  `less-flat-ui` + Impeccable via `polish-pass` + Harmony" with the
  same surface conditionals. The wording "full design package" is
  loose — the list is a surface subset, and it omits motionsites too —
  but the same sentence continues "UI decisions route through the
  design inventory — read it before deciding", which is where the
  fix #31 additions live. Pre-existing wording, not a fix #31
  regression; I record it as an observation, not a finding.
- `skills/orchestrate/references/dispatch-prompt.md:23` (5a): same
  per-surface subsets, delegated to "the design-package rule
  (orchestrate SKILL.md row 10)".
- `skills/integration/SKILL.md:107` (UI rule) and `:122`
  (attribution/composition list): app-UI shorthand (`ui-ux-pro-max`
  + `less-flat-ui`); the :122 list is the skills this skill composes,
  not a design-package enumeration.
- `skills/polish-pass/SKILL.md:15` and `:34`: redirect naming
  `ui-ux-pro-max` / `less-flat-ui` / `design-taste-frontend` as the
  skills that own design direction — a redirect, not an enumeration.
- `skills/orchestrate/references/call-map.md`: no rows for the 5 new
  skills. This is OWED-31-3 (generator-owned map, not regenerated;
  leaf resources, no new orchestration edges; sidecar still says 67
  skills) — recorded, not re-filed. Note the map's own header states
  the currency rule ("kept current by the same change that adds or
  removes an element"), which the OWED entry explicitly overrides for
  this fix; the conditional in OWED-31-3 (regenerate if the audit
  finds DESIGNPKG-AUTO additions are dispatch edges) is the audit's
  call, not this sweep's.
- `skills/design-taste-frontend/SKILL.md:224` carries no `_F31`
  tokens (0 hits in the file) — the skill names are all present and
  the tokens appear in 9 other tree files (`rules/hackathon-mode.mdc`,
  the 5 new skills, `skills/orchestrate/SKILL.md`,
  `skills/orchestrate/references/design-inventory.md`, `README.md`).
  Token-per-file is a convention, not a requirement; not a finding.

### (b) Stale-count sweep — CLEAN (own greps, excl. `node_modules`)

| String | Occurrences | Files |
|---|---|---|
| `67 skills` | **0** | 0 |
| `50 templates` | **0** | 0 |
| `114 WebGL` | **0** | 0 |
| `276 backgrounds` | **0** | 0 |
| `10 animated sections` | **0** | 0 |
| `GSAP 3.15.0` / `gsap@3.15.0` | **0** | 0 |
| `Hairline UI` | **3** | 3 — all explicit out-of-scope disclaimers, not in-scope presentation |

The 3 Hairline UI hits, read in full:
`skills/hairline-create/SKILL.md:7` ("This is Hairline illustrations
— NOT Hairline UI (hairlineui.com), a different product that is not in
scope."), `skills/hairline-adopt/SKILL.md:7` (same disclaimer),
`skills/orchestrate/references/design-inventory.md:185` ("NOT Hairline
UI (hairlineui.com) — a different product, not in scope"). All three
are the required disambiguation, matching SPEC/MANIFEST.

Beyond the brief's list, also checked: the drifted Nov 17 counts
(`62 templates`, `222 3D`, `54 sections`, `530 backgrounds`, `1,088`)
appear **0** times in the built tree — the skill correctly carries no
counts and points at the live `llms.txt`; `200` (React Bits count)
appears **0** times in the react-bits skill and the inventory. The
GSAP pin is `3.15.1` everywhere it appears (gsap skill :6/:24,
design-inventory :146/:183, `ui-ux-pro-max/SKILL.md:326/:350/:426`,
`motion-patterns/SKILL.md:563/:747`, `pitch-deck-video/SKILL.md:308`
"GSAP 3.15.1"), consistent with the inventory's pre-existing pin and
the SPEC correction (DECISION-31-2).

### (c) Orphan/consistency sweep — CLEAN

**New skill dirs — contents match the MANIFEST exactly** (own
`find`, staged `diff -r` silent for all five):

- `skills/getlayers/` — `SKILL.md` only.
- `skills/gsap/` — `SKILL.md` only.
- `skills/react-bits/` — `SKILL.md` only.
- `skills/hairline-create/` — `SKILL.md` + `LICENSE` + `kernel.js`
  (engine), `bench.html` (page), `build.mjs` + `validate.mjs` (check
  scripts), `examples/riffle.js` + `examples/terrain.js`, plus the
  supporting `concepts.md`, `look.md`, `look.mjs`, `read.mjs`,
  `rules.md`, `source.md` — the MANIFEST's "engine/checks/examples"
  set, as vendored.
- `skills/hairline-adopt/` — `SKILL.md` + `LICENSE` only.
- Both LICENSE files are MIT, Lucas Marques, copyright 2026, md5
  `d97393bd90aec1925bdf7413a6e0cc06` for both.
- No vendored GetLayers content, no React Bits `.tsx`/`.jsx`/`.css`
  source, no vendored GSAP source (`gsap.js` / `gsap.min.js` /
  `gsap.ts`: 0 hits outside `node_modules`) — confirmed by my own
  `find`, not only by verify31.

**Inventory §12 paths exist on disk:** `skills/getlayers/SKILL.md`,
`skills/gsap/SKILL.md`, `skills/react-bits/SKILL.md`,
`skills/hairline-create/SKILL.md`, `skills/hairline-adopt/SKILL.md`
all present; §1's `skills/ui-ux-pro-max/data/motion.csv` exists with
header + 17 data rows (rows 1–17, GSAP presets); §9's
`skills/gsap/SKILL.md` usage-skill pointer resolves.

**URLs — all 6 key URLs resolve to live pages** (fetched as page text
Nov 17, 2026 ~04:15 UTC):

- `https://getlayers.ai/llms.txt` — live; counts still read 62
  templates / 222 3D scenes / 54 sections / 530 backgrounds / 1,088
  gradients, exactly as the MANIFEST's Nov 17 reading — no further
  drift since the fix was written. Also confirms the MCP is a Full
  Stack benefit and every layer carries a commercial licence.
- `https://gsap.com/standard-license` — live; Webflow "Standard no
  charge" licence, IP stays with Webflow, bans competing no-code
  visual animation builders, termination at discretion; FAQ confirms
  all former Club plugins free for commercial use.
- `https://reactbits.dev/get-started/installation` — live; CLI form
  `npx shadcn@latest add @react-bits/SplitText-TS-TW` matches the
  skill verbatim, including the JS/TS + CSS/TW variant rule.
- `https://hairline.lucasmarkes.com` — live; "Thirty-three isometric
  figures", MIT and free — matches the skill/inventory's 33.
- `https://github.com/greensock/gsap-skills` — live, public, MIT;
  8 skills (`gsap-core`, `gsap-timeline`, `gsap-scrolltrigger`,
  `gsap-plugins`, `gsap-utils`, `gsap-react`, `gsap-performance`,
  `gsap-frameworks`) — matches the skill's reference table.
- `https://github.com/lucasmarkes/hairline` — live, public, MIT;
  "Thirty-three isometric line figures", install
  `npm i @lucasmarkes/hairline`, shadcn registry URL matches the
  skill; `hairline-create` / `hairline-adopt` both documented there.

### (d) Regression sweep — CLEAN

- **TODO/FIXME/XXX in the new/edited files: 0.** Own grep over
  `skills/getlayers`, `skills/gsap`, `skills/react-bits`,
  `skills/hairline-create`, `skills/hairline-adopt`,
  `skills/orchestrate/SKILL.md`, `rules/hackathon-mode.mdc`,
  `skills/design-taste-frontend/SKILL.md`,
  `skills/orchestrate/references/design-inventory.md`, `README.md`.
  (The whole-tree count is 53, all pre-existing: template
  placeholders, review-checklist wording, and binary-image
  false positives in `design-taste-frontend` PNG assets — none in
  fix #31 files.)
- **Model-pin text in the 5 new skills: 0.** Own case-insensitive
  grep for `grok-4.7`, `grok-4.6`, `Grok 4.7`, `Grok 4.6`,
  `deepseek`, `qwen`, `claude`, `gpt-4`, `sonnet` over the 5 new
  skill dirs returns nothing.
- **`fix31.py` == `fix31.py.template`:** md5
  `37577dddaebf75224b5e0b4e35ab80ef` for both.
- **README:** 72 skills in all 4 count lines (:13, :37, :39, :41);
  fix #31 provenance note present at :29 ("Fix #31 design libraries
  (Nov 17, 2026) — GetLayers (free set only), GSAP, React Bits, and
  Hairline illustrations added to the palette-first inventory. Skills
  are now 72." with all four `_F31` tokens). Zero `67 skills`
  tree-wide (see (b)).
- **Trigger coverage:** `manifests/context-packs/skill-triggers@1.json`
  — `coverage {'skills': 72, 'withTriggers': 49}`, 49 trigger keys
  under `triggers`. `build.sh:222` lists all 5 new skills in the
  new-skills loop; the fix31 hook sits at :24136–24146, after fix30
  and before STEP 5, as the MANIFEST states.
- **Patch log:** `fix31/fix31-patch-log.md` records 0 errors, 11
  changes; its DECISION-31-1…31-7 and OWED-31-1…31-4 match the
  MANIFEST. Build log run 1 ends "build complete", exit 0, counts
  72/45/48/55/15.

### (e) GetLayers weight — CONFIRMED at all 6 claimed sites

| Site | Weight language present |
|---|---|
| DESIGNPKG-AUTO, `skills/orchestrate/SKILL.md:35` | "GetLayers prompts are consulted FIRST in the palette inventory — the first-class foundation the direction leans on" + citation sentence (USED/CONSIDERED-AND-REJECTED, D19; naming no layer is a finding) |
| DESIGNPKG-AUTO, `rules/hackathon-mode.mdc:44` | Same text (stripped byte-identical to :35) |
| Palette-first, `skills/design-taste-frontend/SKILL.md:224` | "`getlayers` FIRST (prompt-first cinematic layers; the first-class foundation the direction leans on — consult its prompts before the other palette sources)" + citation sentence |
| Orchestrate inventory paragraph, `skills/orchestrate/SKILL.md:70` | "GetLayers prompt-first layers — consulted FIRST in the palette inventory, the first-class foundation" |
| Inventory §12, `design-inventory.md:176` | "GetLayers prompts carry the most weight in the palette-first flow — they are consulted FIRST, before the other palette sources, and the direction leans on them heavily as its foundation" + GetLayers row leads with "Consulted FIRST" |
| GetLayers skill, `skills/getlayers/SKILL.md` | Framing header ("consulted FIRST, before the other palette sources… direction leans on GetLayers layers heavily as its foundation… names the layers USED or CONSIDERED-AND-REJECTED, each with a D19 reason") + a dedicated "Priority in the palette-first flow" section with the `not considered — <reason>` escape |

Ordering is also as claimed: `getlayers` is first in every palette
list (DESIGNPKG-AUTO palette list, design-taste-frontend :224).

### (f) Independent counts — reproduced

Own counts on disk: skills 72, agents 45, rules 48, commands 55,
hooks 15 (`hooks/hooks.json`, 15 entries), trigger keys 49
(`skill-triggers@1.json`, `triggers` dict of 49, coverage 72/49).
Build log run 1 agrees (skills 72, agents 45, rules 48, commands 55,
hooks 15). The call-map sidecar still reads 67/45/48/55/49 at :9–14 —
OWED-31-3, recorded, not re-filed (see (a)).

### (g) Carried items — still standing as recorded, not re-filed

- **OWED-31-1:** live behaviour of the four resources unverified
  until real project use; live smoke test still skipped since Nov 15.
  Nothing in this sweep changes that.
- **OWED-31-2:** GetLayers MCP unwired ($199 Full Stack) — the skill
  states it, no MCP wiring found in the tree.
- **OWED-31-4:** vendored `hairline-create/SKILL.md:11` says "The
  six figures of @lucasmarkes/hairline are the bar" — upstream's
  original-six text; the library now ships 33. Present as recorded;
  the live repo's own README still carries the same "six figures"
  image caption, confirming it is upstream text, not a fix #31 edit.
- **OWED-30-6** (allow-listed verify30 check-9b smuggled name) and
  the dry-run epic/`/prune` error: not re-filed per the brief. The 7
  epic commands ship in `hackathon-ecc/commands/`; `/prune` absent —
  re-confirmed, not filed.
- **F35 fragility, F-O scope note, check-12b transient** (carried
  from sweep #40): not re-probed in this sweep's scope; nothing in
  the fix #31 diff touches those mechanisms.

### (h) SPEC conformance — scope MET

SPEC `fix31/SPEC.md`: four resources, free-tier only, no paid plans;
one skill (or inventory entry) per resource, following the
MotionSites/Animaster pattern; weave into palette-first + the single
inventory catalog; verifier checks incl. licence checks; do not change
model pins / adaptability routing / debloat / design package /
grill-me; do not purchase any paid plan. All met as shipped: 5 skills
(Hairline is two, per SPEC), palette-first + DESIGNPKG-AUTO + inventory
§12 weave, verify31 §14 checks, no pin/routing/debloom change (pin
census holds: 49 ID + 22 prose extra-high, 70 fast-worker, 0 old pin —
asserted by fix31.py and re-confirmed by verify31's pass). The two
SPEC corrections are honoured: GSAP pinned at 3.15.1, not 3.15.0;
GetLayers counts not frozen anywhere. The SPEC's Verification section
requires the audit loop + sweep + dry-run with honest verdicts and a
design leg using ≥1 item from each source: the audit loop (audit #97
A/B) and dry-run #46 are parallel round-1 work whose reports were
still landing as this sweep ran — their verdicts are outside this
sweep's scope to confirm, and this sweep is CLEAN on its own scope.

### (i) Verifier runs — my own re-run

- **`verify31.py`, re-run by me: 380/380 checks pass, exit 0.**
  (Tail: "PASS no vendored GSAP source file…", "PASS README fix31
  provenance note present with the four _F31 tokens", "PASS
  fix31/fix31-patch-log.md exists with 0 errors, trigger 67 -> 72,
  README note added", "380/380 checks pass".) Run took ~29 s. The
  380 total is the verifier's own count; I report the run's own
  "380/380", not a recount of call sites.

### Other

- No file was edited, created, or deleted except this report.
  `build.sh` was not run; `fix11/fix11-stage.py` was not run; nothing
  was committed, pushed, or messaged.
