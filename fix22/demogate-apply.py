#!/usr/bin/env python3
"""Apply the /demo-gate removal (Audit #68 B-1/B-2/B-3 + Sweep #30b Finding 1/2).

Removes every automatic /demo invocation so /demo runs ONLY when the user
invokes it explicitly (parent addendum §3b, Anish Nov 12 18:52). Two mechanisms:
  (a) STAGED edits — files that are staged sources (orchestrate, hackathon-mode,
      demo.md, dispatch-prompt.md, vercel-checklist): direct edits, verified
      count==1 before writing.
  (b) fix22.py RUNTIME tuples (mode="replace") — ECC-derived files
      (orch-build-mvp, orch-change-feature skill + command): old-text is
      extracted by markers from the CURRENT built tree (post-all-prior-patches),
      so it matches what the fix22 block sees at build time (it runs last).

Also fixes Sweep #30b Finding 2 (stale "40x40px, ideally 44x44px" hit-area
wording in the §16 files -> "44x44px minimum, the plugin floor").

Usage: python3 fix22/demogate-apply.py            # dry-run validation only
       python3 fix22/demogate-apply.py --apply    # apply staged edits + fix22.py
Then:  python3 fix22/fix22.py && bash build.sh && python3 fix22/verify22.py

B-3 decision (coordinator, recorded): the orch-change-feature re-film is
REMOVED, not carved out as an exception. The parent's rule is absolute
("/demo NEVER runs on its own... ONLY when the user invokes /demo
explicitly"), and the parent's addendum says "Any auto-invocation found is
a BLOCKING audit finding — remove it". The removal's done-condition for the
video becomes: flagged as stale (re-film on request) OR re-filmed if the
user asked. The parent spot-checks this before anything is reported to
Anish and may restore the re-film as a documented exception.
"""
import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
FIX22 = os.path.join(PLUGIN, "fix22")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")

BANNED = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5"]

# ---------------------------------------------------------------- staged edits
# Each: (relpath_from_plugin, old_substring, new_substring).
# old must occur exactly once in the staged file. Full-line replacements are
# done by giving the whole line as old (the script reads the line by number
# where noted) -- here every old is a unique substring, so line numbers are
# not needed.
STAGED = [
    # --- orchestrate (new-skills/orchestrate/SKILL.md) ---
    # O-1: :56 summary sequence (narration-key condition + drop demo LOCAL).
    ("new-skills/orchestrate/SKILL.md",
     "(narration-key prompt → scope → expansion Phases 0–3 → slice → build via the routing table incl. row 10 → verify → polish → deploy → demo LOCAL → README → final report)",
     "(narration-key prompt — only when the user asked for a demo video → scope → expansion Phases 0–3 → slice → build via the routing table incl. row 10 → verify → polish → deploy → README → final report). /demo is never part of this sequence — it runs ONLY when the user invokes it explicitly (fix #22 /demo gate)."),
    # O-2a: step 0 — the prompt is conditional on a requested video.
    ("new-skills/orchestrate/SKILL.md",
     "This is the ONE sanctioned user prompt during the first build besides grill-me itself (hackathon-mode §7 schedules it here); it never blocks the build. Send it once, in one message, whether grill-me ran or the user chose the skip path (\"skip the grilling\" / \"just build it\") — it fires at the start of the build either way.",
     "This is the ONE sanctioned user prompt during the first build besides grill-me itself (hackathon-mode §7 schedules it here) — and ONLY when the user asked for a demo video; it never blocks the build. If the user's request explicitly asks for a demo video (or the user invoked `/demo`), send it once, in one message, whether grill-me ran or the user chose the skip path (\"skip the grilling\" / \"just build it\") — it fires at the start of the build either way. If the user did NOT ask for a demo video, do NOT send this prompt — no video is being built, so no key is needed; if the user later asks for a video, `/demo` prompts for the key at the point the video is confirmed (see `commands/demo.md`)."),
    # O-2b: step 0 — "the video will be built either way" is no longer true.
    ("new-skills/orchestrate/SKILL.md",
     "and that the build continues regardless — the video will be built either way, and if the key arrives later a re-run produces the narrated cut.",
     "and that the build continues regardless — if the key arrives later a re-run produces the narrated cut."),
    # O-2c: step 0 — the /demo dispatch is no longer "step 5d".
    ("new-skills/orchestrate/SKILL.md",
     "pass it as the `ELEVENLABS_API_KEY` env var to the `tts` run at /demo time — via the /demo dispatch (step 5d), which carries an explicit env instruction",
     "pass it as the `ELEVENLABS_API_KEY` env var to the `tts` run at /demo time — via the /demo dispatch, which carries an explicit env instruction"),
    # O-2d: step 0 — the re-run is after the USER-invoked /demo.
    ("new-skills/orchestrate/SKILL.md",
     "If the key arrives after /demo already rendered but before the final report,",
     "If the key arrives after the user-invoked /demo already rendered but before the final report,"),
    # O-3: step 5 header — three sub-steps, no demo.
    ("new-skills/orchestrate/SKILL.md",
     "5. **Verify → polish → deploy → demo, in that order** — four sub-steps inside this one step, never reordered (polish runs after verification and before deploy; deploy runs before demo).",
     "5. **Verify → polish → deploy, in that order** — three sub-steps inside this one step, never reordered (polish runs after verification and before deploy)."),
    # O-5: 5c — the 5d demo no longer films/reports the verified tree.
    ("new-skills/orchestrate/SKILL.md",
     "The 5d demo and the step-6 README/final report film and report the verified tree: after a revert that is the pre-redesign verified state, never the held redesign.",
     "The step-6 README/final report reports the verified tree: after a revert that is the pre-redesign verified state, never the held redesign."),
    # O-6: end-of-project checks — no demo in the sequence.
    ("new-skills/orchestrate/SKILL.md",
     "**End-of-project checks (before the final report).** After deploy, demo, commit, and README, run the six deferred checks by name",
     "**End-of-project checks (before the final report).** After deploy, commit, and README, run the six deferred checks by name"),
    # O-7a: :327 — final report after deploy + README (no demo video).
    ("new-skills/orchestrate/SKILL.md",
     "Orchestrate owns the whole-build final report. After deploy, the demo video, and the README, write it to `docs/final-report.md` in the project AND deliver it as the reply",
     "Orchestrate owns the whole-build final report. After deploy and the README, write it to `docs/final-report.md` in the project AND deliver it as the reply"),
    # O-7b: :327 sequence — no demo-video step.
    ("new-skills/orchestrate/SKILL.md",
     "Sequence: verify → polish → deploy → demo video (`/demo` / `pitch-deck-video` films the LOCAL app from the project dir, per orchestrate step 5 above; orchestrate sequences it, it does not film it) → README (`readme-writer`, orchestrate step 6) → final report.",
     "Sequence: verify → polish → deploy → README (`readme-writer`, orchestrate step 6) → final report. (A demo video is filmed only when the user invokes `/demo` explicitly — it is never part of this sequence; if one was filmed, the report carries its handoff below.)"),
    # O-8a: :344 — demo-video handoff is conditional.
    ("new-skills/orchestrate/SKILL.md",
     "- **Demo video handoff** — the video file path (`<app-name>-video/out/demo.mp4`) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\"",
     "- **Demo video handoff (only if a video was filmed)** — the video file path (`<app-name>-video/out/demo.mp4`) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\""),
    # O-8b: :344 — no handoff when no video was filmed.
    ("new-skills/orchestrate/SKILL.md",
     "and the music credit (`public/music/SOURCE.txt`).",
     "and the music credit (`public/music/SOURCE.txt`). If no video was filmed (the user did not invoke `/demo`), this handoff is omitted and the report notes that no demo video was filmed."),
    # --- hackathon-mode (new-rules/hackathon-mode.mdc) ---
    # H-1: :68 — the "required deliverable, filmed by default" mandate.
    ("new-rules/hackathon-mode.mdc",
     "- The first build films `/demo` (`pitch-deck-video`) after deploy: the demo video is a required deliverable, filmed by default (film the real app) — then the README is written and the final report is delivered (deploy → demo → README → final report).",
     "- The first build does NOT film `/demo` automatically (fix #22 /demo gate, DEMOGATE_H1_F22). `/demo` (`pitch-deck-video`) runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video) — never as a pipeline step, never by default. When it runs, it films the LOCAL app (film the real app), never a deployed URL. Then the README is written and the final report is delivered (deploy → README → final report). The demo video is no longer a required deliverable of the first build — the behavior change is recorded in `fix22/MANIFEST.md`."),
    # --- demo.md (new-skills/pitch-deck-video/commands/demo.md) ---
    # D-1: line 13 — the orchestrate-5d / orch-build-mvp-8 dispatch note.
    ("new-skills/pitch-deck-video/commands/demo.md",
     "If this /demo run was dispatched by orchestrate (step 5d) or orch-build-mvp (step 8), do NOT prompt — the prompt was already sent once at the start of the run; the key, if received, arrives via the dispatch's Environment field as an `ELEVENLABS_API_KEY` env instruction — run the `tts` step with that variable set in the process environment.",
     "If this /demo run was invoked with a narration key already provided (via the dispatch's Environment field as an `ELEVENLABS_API_KEY` env instruction), do NOT prompt again — run the `tts` step with that variable set in the process environment."),
    # --- dispatch-prompt.md (new-skills/orchestrate/references/dispatch-prompt.md) ---
    # P-1: Environment field — the "step 0 / step 5d" reference.
    ("new-skills/orchestrate/references/dispatch-prompt.md",
     "(orchestrate step 0 / step 5d) — the executor runs the `tts` step with that",
     "(orchestrate step 0 — only when the user asked for a demo video) — the executor runs the `tts` step with that"),
    # --- Sweep #30b Finding 2: stale hit-area wording in the §16 files ---
    # F2-1: vercel-checklist V-FO6 (staged source). The parenthetical spans a
    # line break ("Group A A14 /" then "G8)" on the next line), so the old
    # text ends at the break.
    ("round2-skills/polish-pass/reference/vercel-checklist.md",
     "40x40px, ideally 44x44px — Group A A14 /",
     "44x44px minimum, the plugin floor — Group A A14 /"),
    # F2-2/F2-3: vercel-dedupe V-FO6 (:67) and AG1 (:244) — same parenthetical,
    # twice in one file, so the applier replaces ALL occurrences here.
    ("fix22/vercel-dedupe.md",
     "(40x40px, ideally 44x44px — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp)",
     "(44x44px minimum, the plugin floor — Group A A14 / G8; quick-reference `touch-target-size` 44x44pt / 48x48dp)"),
]

# O-4 (orchestrate 5d, line 80) is a FULL-LINE replacement (the line is 1,334
# chars; replacing by substring would leave the rest of the auto-invocation).
# Handled separately below by line number.
ORCH_5D_LINE = 80
ORCH_5D_NEW = ("   **Demo — never automatic (fix #22 /demo gate, DEMOGATE_O4_F22).** "
    "`/demo` (`pitch-deck-video`) is NEVER dispatched by this pipeline. It runs "
    "ONLY when the user invokes `/demo` explicitly (or the user's request "
    "explicitly asks for a demo video). When it runs, it films the LOCAL app "
    "from the project dir only (`APP_DIR` to the app dir) — it never films a "
    "deployed URL; do NOT set `shots.json` `app.url` to the deployed URL. If the "
    "user asked for a video, pass the scoped wow moment into the /demo dispatch: "
    "state it explicitly — the wow moment from `docs/scope.md` + "
    "`docs/decision-record.md`, where it lives in the app, and the order it "
    "appears in the demo — so the video features it. If a narration key was "
    "received (step 0, KEY-RECEIPT: yes), the /demo dispatch ALSO carries it "
    "(see the dispatch template's Environment field). If no video was requested, "
    "the final report notes that no demo video was filmed.")

# ---------------------------------------------------------------- runtime patches
# Each: (id, rel_in_built_tree, start_marker, end_marker_or_None, new_text,
#        token). old-text = built_tree[start:end] where end is just past
# end_marker (or start+len when end_marker is None and the whole span is the
# start marker itself). The token must be in new_text and absent from the file.
RUNTIME = [
    # --- orch-build-mvp skill (B-2) ---
    ("DEMOGATE_B2S1", "skills/orch-build-mvp/SKILL.md",
     "8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.**",
     None,
     "8. **Deploy via `deploy-fast`.** **Demo — never automatic (fix #22 /demo gate, DEMOGATE_B2S1_F22).** `/demo` is not filmed here.",
     "DEMOGATE_B2S1_F22"),
    ("DEMOGATE_B2S2", "skills/orch-build-mvp/SKILL.md",
     "then film the LOCAL app from the project dir (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it. The demo video is a required deliverable; its file is `<app-name>-video/out/demo.mp4`.",
     None,
     "Do NOT film via `/demo` here — `/demo` (`pitch-deck-video`) runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video). If the user asked for one, film the LOCAL app from the project dir after deploy (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it; the video file is `<app-name>-video/out/demo.mp4`. If no video was requested, the final report notes that no demo video was filmed. (fix #22 /demo gate, DEMOGATE_B2S2_F22)",
     "DEMOGATE_B2S2_F22"),
    ("DEMOGATE_B2S3", "skills/orch-build-mvp/SKILL.md",
     "`/demo` films the verified tree as it stands after any revert (see 6b) — a held redesign is never in the filmed tree. After filming, invoke `readme-writer` to write/update the README from the built app, before the final report in step 9",
     None,
     "A filmed video shows the verified tree as it stands after any revert (see 6b) — a held redesign is never in the filmed tree. After deploy (and any requested filming), invoke `readme-writer` to write/update the README from the built app, before the final report in step 9 (fix #22 /demo gate, DEMOGATE_B2S3_F22)",
     "DEMOGATE_B2S3_F22"),
    ("DEMOGATE_B2S4", "skills/orch-build-mvp/SKILL.md",
     "and the demo-video handoff: the video file path (`<app-name>-video/out/demo.mp4`) plus the narration record (ElevenLabs usage remaining, narration status per line-set, the provider decision-log entries, and the music credit).",
     None,
     "and, if a video was filmed, the demo-video handoff: the video file path (`<app-name>-video/out/demo.mp4`) plus the narration record (ElevenLabs usage remaining, narration status per line-set, the provider decision-log entries, and the music credit). If no video was filmed, the report notes that instead. (fix #22 /demo gate, DEMOGATE_B2S4_F22)",
     "DEMOGATE_B2S4_F22"),
    ("DEMOGATE_B2S5", "skills/orch-build-mvp/SKILL.md",
     "The report also states the demo video handoff: the video file path (the local filmed video file) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\" — the first build never uploads the video anywhere (it has no YouTube/Devpost account access), so the file path + upload instruction is how the video reaches the submission.",
     None,
     "If a video was filmed, the report also states the demo video handoff: the video file path (the local filmed video file) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\" — the first build never uploads the video anywhere (it has no YouTube/Devpost account access), so the file path + upload instruction is how the video reaches the submission. If no video was filmed, the report notes that no demo video was filmed. (fix #22 /demo gate, DEMOGATE_B2S5_F22)",
     "DEMOGATE_B2S5_F22"),
    # --- orch-build-mvp command (B-2) ---
    ("DEMOGATE_B2C1", "commands/orch-build-mvp.md",
     "8. Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — the demo video is a required deliverable; film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report).",
     None,
     "8. Deploy via `deploy-fast`. Do NOT film via `/demo` here — `/demo` runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video); if the user asked for one, film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report). (fix #22 /demo gate, DEMOGATE_B2C1_F22)",
     "DEMOGATE_B2C1_F22"),
    # --- orch-change-feature skill (B-3) ---
    # B3-S1: the deploy-wait passage. Old = from the "wait for the deploy"
    # sentence through the "film local anyway" sentence (extracted by markers).
    ("DEMOGATE_B3S1", "skills/orch-change-feature/SKILL.md",
     "After the redeploy, wait for the deploy to be ready before re-filming",
     "if the deploy was blocked, film local anyway and note in the final report that the video shows the local app, not the deployed one.",
     "After the redeploy, verify the deploy serves the new version (no removed feature, no dangling references) — UNLESS the deploy was already known-blocked (blocked-deploy handling above: no git-linked deploy, no deploy-fast path, or an unauthenticated deploy CLI): in that case skip the check entirely and note it in the final report. Otherwise take the deployed URL and deploy path from `.hackathon/run-ledger.md` (or `docs/final-report.md` if the ledger is absent), then poll the deployed app until it serves the new version, with a BOUNDED wait — check every ~30s, stop after ~5 minutes. If it never becomes ready in that bound, record the deploy as not-verified in the final report and move on — never wait unboundedly. (The poll verifies the redeploy; it is not a prelude to filming — no re-film happens here.) Then, before any future re-film, update `shots.json` FIRST — remove the feature's shots, selectors, and narration lines — then re-check every remaining shot against the updated demo storyboard in `docs/scope.md` (move the feature to the cut list first, so the storyboard is current): a shot whose feature was removed, or whose narration still promises the removed feature, is removed or rewritten before the re-film. If the user asks for a re-film, re-film via `/demo --rebuild`, which films the LOCAL app from the project dir (`APP_DIR`/project root), never a deployed URL; if the deploy was blocked, film local anyway and note in the final report that the video shows the local app, not the deployed one. (fix #22 /demo gate, DEMOGATE_B3S1_F22)",
     "DEMOGATE_B3S1_F22"),
    # B3-S2: narration continuity is about a REQUESTED re-film.
    ("DEMOGATE_B3S2", "skills/orch-change-feature/SKILL.md",
     "**Narration continuity on the re-film:** narration lines that did not change are served from the per-line cache",
     None,
     "**Narration continuity on a requested re-film (fix #22 /demo gate, DEMOGATE_B3S2_F22):** if the user asks for a re-film, narration lines that did not change are served from the per-line cache",
     "DEMOGATE_B3S2_F22"),
    # B3-S3: the re-upload paragraph lead.
    ("DEMOGATE_B3S3", "skills/orch-change-feature/SKILL.md",
     "After re-filming, IF a hosted video link exists (in the Devpost submission, the README, or the final report) AND the agent has YouTube/Vimeo account access for that host, re-upload the new video",
     None,
     "After a requested re-film, IF a hosted video link exists (in the Devpost submission, the README, or the final report) AND the agent has YouTube/Vimeo account access for that host, re-upload the new video (fix #22 /demo gate, DEMOGATE_B3S3_F22)",
     "DEMOGATE_B3S3_F22"),
    # B3-S4: blocked fallback — satisfied by the stale record, not a re-film.
    ("DEMOGATE_B3S4", "skills/orch-change-feature/SKILL.md",
     "the removal is done-with-blocked-re-upload, satisfied by the re-filmed LOCAL video plus this blocked record, not by a phantom upload",
     None,
     "the removal is done-with-blocked-re-upload, satisfied by the stale-video record (or the re-filmed LOCAL video, if the user asked for a re-film) plus this blocked record, not by a phantom upload (fix #22 /demo gate, DEMOGATE_B3S4_F22)",
     "DEMOGATE_B3S4_F22"),
    # B3-S5: the done-condition.
    ("DEMOGATE_B3S5", "skills/orch-change-feature/SKILL.md",
     "The removal's done-condition (\"the demo video reflects the removal\") is satisfied by the re-filmed LOCAL video + the honest hosting note, not by a phantom upload.",
     None,
     "The removal's done-condition for the video (\"the demo video reflects the removal, or is flagged as stale\") is satisfied by the re-filmed LOCAL video (if the user asked for a re-film) + the honest hosting note, or by the stale-video record when no re-film was requested — never by a phantom upload, never by an automatic re-film. (fix #22 /demo gate, DEMOGATE_B3S5_F22)",
     "DEMOGATE_B3S5_F22"),
    # B3-S6: "none of them may go stale" — the video may be flagged stale.
    ("DEMOGATE_B3S6", "skills/orch-change-feature/SKILL.md",
     "a removal is not done until the deployed app, the demo video, the ledger, and the inventory all reflect it; none of them may go stale.",
     None,
     "a removal is not done until the deployed app, the ledger, and the inventory all reflect it, and the demo video is either re-filmed (on request) or flagged as stale; none of them may go stale silently. (fix #22 /demo gate, DEMOGATE_B3S6_F22)",
     "DEMOGATE_B3S6_F22"),
    # B3-S7: step 6 handoff — stale note when no re-film was requested.
    ("DEMOGATE_B3S7", "skills/orch-change-feature/SKILL.md",
     "the re-uploaded video link if a hosted video existed (or the blocked re-upload record from step 5 if the re-upload was blocked for no account access), else the honest hosting note from step 5 — \"video re-filmed locally at <path>, not yet hosted\"",
     None,
     "the re-uploaded video link if a hosted video existed and a re-film was requested (or the blocked re-upload record from step 5 if the re-upload was blocked for no account access), else the honest hosting note from step 5 — \"video re-filmed locally at <path>, not yet hosted\" if a re-film was requested, or \"demo video STALE — shows the removed feature; re-film with `/demo --rebuild` on request\" if not (fix #22 /demo gate, DEMOGATE_B3S7_F22)",
     "DEMOGATE_B3S7_F22"),
    # --- orch-change-feature command (B-3) ---
    ("DEMOGATE_B3C1", "commands/orch-change-feature.md",
     "update `shots.json` before re-filming, re-film locally via `/demo --rebuild`, re-upload the video and update its link, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal).",
     None,
     "update `shots.json` (remove the feature's shots, selectors, and narration lines) so it is ready for a re-film, note in the final report that the demo video is now stale (re-film with `/demo --rebuild` only when the user asks), re-upload the video and update its link only if a re-film was requested and a hosted link exists, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal). (fix #22 /demo gate, DEMOGATE_B3C1_F22)",
     "DEMOGATE_B3C1_F22"),
]


def extract_old(path, start, end):
    t = open(path, encoding="utf-8").read()
    n = t.count(start)
    assert n == 1, f"{path}: start marker count={n}: {start[:80]!r}"
    i = t.find(start)
    if end is None:
        return t[i:i + len(start)]
    j = t.find(end, i)
    assert j != -1, f"{path}: end marker not found: {end[:80]!r}"
    return t[i:j + len(end)]


def check_banned(text, where):
    low = text.lower()
    for b in BANNED:
        assert b not in low, f"banned term {b!r} in {where}"


def main():
    apply = "--apply" in sys.argv
    failures = []

    # ---- validate staged edits
    staged_cache = {}
    for rel, old, new in STAGED:
        path = os.path.join(PLUGIN, rel)
        if path not in staged_cache:
            staged_cache[path] = open(path, encoding="utf-8").read()
        t = staged_cache[path]
        n = t.count(old)
        if rel == "fix22/vercel-dedupe.md":
            # F2-2/F2-3: the same parenthetical occurs twice; replace both.
            if n != 2:
                failures.append(f"{rel}: expected 2 occurrences, got {n}")
        elif n != 1:
            failures.append(f"{rel}: old count={n}: {old[:80]!r}")
        check_banned(new, f"staged {rel}")
    # O-4 full-line check
    orch = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
    olines = open(orch, encoding="utf-8").read().split("\n")
    line80 = olines[ORCH_5D_LINE - 1]
    if not line80.startswith("   - **5d. Demo**"):
        failures.append(f"orchestrate line {ORCH_5D_LINE} does not start with 5d bullet: {line80[:80]!r}")
    check_banned(ORCH_5D_NEW, "ORCH_5D_NEW")

    # ---- validate runtime patches (old extracted from the CURRENT built tree)
    runtime_old = []
    for pid, rel, start, end, new, token in RUNTIME:
        path = os.path.join(BUILT, rel)
        try:
            old = extract_old(path, start, end)
        except AssertionError as e:
            failures.append(str(e))
            continue
        t = open(path, encoding="utf-8").read()
        if token in t:
            failures.append(f"{pid}: token {token} already in {rel}")
        if token not in new:
            failures.append(f"{pid}: token {token} not in new text")
        try:
            check_banned(new, pid)
        except AssertionError as e:
            failures.append(str(e))
        runtime_old.append((pid, rel, old, new, token))

    if failures:
        print("VALIDATION FAILED:")
        for f in failures:
            print(" -", f)
        sys.exit(1)
    print(f"dry-run validation: OK — {len(STAGED)} staged edits "
          f"(+ O-4 full-line) and {len(RUNTIME)} runtime patches")
    for pid, rel, old, new, token in runtime_old:
        print(f"  {pid}: {rel} old_len={len(old)} new_len={len(new)} token={token}")
    if not apply:
        print("dry-run only (no writes). Re-run with --apply.")
        return

    # ---- apply staged edits
    for rel, old, new in STAGED:
        path = os.path.join(PLUGIN, rel)
        t = open(path, encoding="utf-8").read()
        t = t.replace(old, new)
        open(path, "w", encoding="utf-8").write(t)
        print(f"staged: {rel}")
    # O-4 full-line
    olines[ORCH_5D_LINE - 1] = ORCH_5D_NEW
    open(orch, "w", encoding="utf-8").write("\n".join(olines))
    print(f"staged: new-skills/orchestrate/SKILL.md line {ORCH_5D_LINE} (5d)")

    # ---- append runtime tuples + constants to fix22.py
    f22 = os.path.join(FIX22, "fix22.py")
    src = open(f22, encoding="utf-8").read()
    # New-text constants: append before the PATCHES list.
    consts = []
    for pid, rel, old, new, token in runtime_old:
        consts.append(f'{pid} = """{new}"""')
    anchor = "PATCHES = ["
    assert src.count(anchor) == 1
    src = src.replace(anchor, "\n".join(consts) + "\n\n" + anchor, 1)
    # Tuples: append before the closing "]" of PATCHES. The list ends with a
    # line that is exactly "]" following the last tuple; find it after PATCHES.
    idx = src.find(anchor)
    close = src.find("\n]\n", idx)
    assert close != -1
    tuples = []
    for pid, rel, old, new, token in runtime_old:
        tuples.append(
            f'    ("{pid}", "{rel}", {old!r}, {pid}, "replace", "{token}"),')
    # NOTE: old is embedded as a repr literal; new is the named constant.
    src = src[:close] + "\n" + "\n".join(tuples) + src[close:]
    open(f22, "w", encoding="utf-8").write(src)
    print(f"fix22.py: appended {len(runtime_old)} constants + {len(runtime_old)} runtime tuples")
    print("Next: python3 fix22/fix22.py && bash build.sh && python3 fix22/verify22.py")


if __name__ == "__main__":
    main()
