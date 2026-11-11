#!/usr/bin/env python3
"""Fix 5 — Audit M2: remove the removed deployed-URL filming design from build.sh.

Defect: build.sh still contains live patch text that writes the REMOVED
deployed-URL filming design (video is made from the code, not a live link —
/demo always films the LOCAL app from the project dir; there is NO
deployed-URL filming path). The built plugin is clean only because later
patches overwrite the early patch's text.

Patch chain (execution order in build.sh), verified byte-for-byte before
writing this script:
  1. Batch F early patch (~line 20012, SKILL.md; ~line 20017,
     commands/orch-build-mvp.md) writes steps with deployed filming:
     "Deploy the working MVP so the demo films the real deployed app" /
     "film the real app by default (set `shots.json` `app.url` to the
     deployed URL...)" / "film the deployed app (or the local dev server...)".
  2. Fix program #3 Batch A skill block (~lines 20132-20143) RENUMBERS the
     skill steps: its old-string contains the early patch's new-strings
     verbatim at numbers 6/7, its new-string repeats them at numbers 7/8.
     Its commands block (~lines 20194-20202) does NOT touch the deployed
     step-5 line, so it needs no change.
  3. Fix program #4 Batch A skill block (~lines 20716-20717) overwrites
     steps 7/8 with the local-only text: its old-string is byte-identical
     to the Fix #3 block's new-string steps 7/8. Its commands block
     (~lines 20790/20801) overwrites step 5 with the local-only text: its
     old-string step 5 is byte-identical to the early patch's step 5.

Fix strategy (unwind, keep the chain consistent — NOT delete-and-re-anchor):
replace the early patch's new-strings with local-only text AND update every
downstream old-string that contains the early text, so each later patch's
old-string still matches the text the earlier patch produces. Step numbers
are preserved throughout (skill Deploy 6 / Film 7 -> renumbered 7 / 8;
command step 5 stays step 5), so no other patch block is affected.
The Fix #4 new-strings are already local-only and are NOT touched.

Substitutions (each asserts its exact occurrence count):
  S1  early SKILL new-string, \\n-joined double-quoted form (:20012)
  S2  early commands new-string, step 5 (:20017)
  S3  Fix #3 skill old-string, steps 6/7 (:20135-20136)
  S4  shared steps 7/8 block — Fix #3 new-string AND Fix #4 old-string
      (:20141-20142 and :20716-20717); count == 2, same replacement, which
      is exactly what keeps the chain link intact
  S5  Fix #4 commands old-string, step 5 (:20790)
  S6  Fix #4 skill-block comment (:20713-20715): it describes the old steps
      7+8 as "(deploy films deployed URL; film sets app.url)" — false once
      S4 lands, since the old steps are already local-only. Comment-only
      change, zero build impact; keeps the file honest.

Usage: python3 fix5-audit-m2.py <path-to-build.sh>
  The coordinator applies this to the real build.sh. Never run build.sh
  itself from here.
"""
import sys

# --- local-only replacement bodies (mirror the already-approved Fix #4
# new-string wording; they state the negation explicitly, never the
# removed design) ---
SKILL_DEPLOY_LOCAL = (
    "Deploy the working MVP; the demo films the LOCAL app from the project "
    "dir, never a deployed URL \u2014 never hard-abort the run for lack of a "
    "deployed URL. If deploy was static-only or blocked, the final report "
    "notes that."
)
SKILL_FILM_LOCAL = (
    "The demo video is a required deliverable \u2014 film the LOCAL app from "
    "the project dir (`APP_DIR` to the app dir); `/demo` never films the "
    "deployed URL, so do NOT set `shots.json` `app.url` to it."
)
CMD_FILM_LOCAL = (
    "film the LOCAL app from the project dir only, never a deployed URL "
    "(if deploy was static-only or blocked, noted in the final report)"
)


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python3 fix5-audit-m2.py <path-to-build.sh>", file=sys.stderr)
        raise SystemExit(2)
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()

    # S1 — Batch F early patch, SKILL.md new-string (:20012). File form is a
    # double-quoted Python string, so the step separator is a literal
    # backslash-n in build.sh (written "\\n" here).
    s1_old = (
        "6. **Deploy via `deploy-fast`.** Deploy the working MVP so the demo "
        "films the real deployed app; if deploy is static-only or blocked, "
        "the demo films the local dev server instead and the final report "
        "notes that \u2014 never hard-abort the run for lack of a deployed URL."
        "\\n7. **Film via `/demo` (`pitch-deck-video`).** "
        + "The demo video is a required deliverable \u2014 film the real app by "
        "default (set `shots.json` `app.url` to the deployed URL, or `APP_DIR` "
        "to the app dir)."
    )
    s1_new = (
        "6. **Deploy via `deploy-fast`.** " + SKILL_DEPLOY_LOCAL
        + "\\n7. **Film via `/demo` (`pitch-deck-video`) \u2014 LOCAL only.** "
        + SKILL_FILM_LOCAL
    )

    # S2 — Batch F early patch, commands new-string (:20017). Anchored with
    # the following "\\n6. Deliver the final report as the reply", which
    # occurs only here (the Fix #4 commands old-string has a real newline
    # and different step-6 wording), so this cannot touch :20790.
    s2_old = (
        "film the deployed app (or the local dev server if deploy was "
        "static-only or blocked, noted in the final report)."
        "\\n6. Deliver the final report as the reply"
    )
    s2_new = (
        CMD_FILM_LOCAL + ".\\n6. Deliver the final report as the reply"
    )

    # S3 — Fix #3 skill old-string, steps 6/7 (:20135-20136), raw
    # triple-quoted form with real newlines in build.sh.
    s3_old = (
        "6. **Deploy via `deploy-fast`.** Deploy the working MVP so the demo "
        "films the real deployed app; if deploy is static-only or blocked, "
        "the demo films the local dev server instead and the final report "
        "notes that \u2014 never hard-abort the run for lack of a deployed URL.\n"
        "7. **Film via `/demo` (`pitch-deck-video`).** "
        "The demo video is a required deliverable \u2014 film the real app by "
        "default (set `shots.json` `app.url` to the deployed URL, or `APP_DIR` "
        "to the app dir)."
    )
    s3_new = (
        "6. **Deploy via `deploy-fast`.** " + SKILL_DEPLOY_LOCAL
        + "\n7. **Film via `/demo` (`pitch-deck-video`) \u2014 LOCAL only.** "
        + SKILL_FILM_LOCAL
    )

    # S4 — shared steps 7/8 block: Fix #3 new-string (:20141-20142) AND
    # Fix #4 old-string (:20716-20717) are byte-identical; both must become
    # the same local-only text or the chain breaks. Count == 2 asserted.
    s4_old = (
        "7. **Deploy via `deploy-fast`.** Deploy the working MVP so the demo "
        "films the real deployed app; if deploy is static-only or blocked, "
        "the demo films the local dev server instead and the final report "
        "notes that \u2014 never hard-abort the run for lack of a deployed URL.\n"
        "8. **Film via `/demo` (`pitch-deck-video`).** "
        "The demo video is a required deliverable \u2014 film the real app by "
        "default (set `shots.json` `app.url` to the deployed URL, or `APP_DIR` "
        "to the app dir)."
    )
    s4_new = (
        "7. **Deploy via `deploy-fast`.** " + SKILL_DEPLOY_LOCAL
        + "\n8. **Film via `/demo` (`pitch-deck-video`) \u2014 LOCAL only.** "
        + SKILL_FILM_LOCAL
    )

    # S5 — Fix #4 commands old-string, step 5 (:20790). Anchored with the
    # following real-newline step 6 ("...the done signal: write it to"),
    # which occurs only here (the early patch at :20017 has a literal
    # backslash-n and "as the reply" wording), so this cannot touch :20017.
    s5_old = (
        "film the deployed app (or the local dev server if deploy was "
        "static-only or blocked, noted in the final report).\n"
        "6. Deliver the final report \u2014 the done signal: write it to "
        "`docs/final-report.md` in the project AND deliver it as the reply"
    )
    s5_new = (
        CMD_FILM_LOCAL + ".\n"
        "6. Deliver the final report \u2014 the done signal: write it to "
        "`docs/final-report.md` in the project AND deliver it as the reply"
    )

    # S6 — Fix #4 skill-block comment (:20713-20715). Comment only; the
    # parenthetical describes the pre-fix old steps and would be false
    # after S4.
    s6_old = (
        "  # Old steps 7+8 (deploy films deployed URL; film sets app.url) become\n"
        "  # step 8 (deploy, then /demo films the LOCAL app only \u2014 video from code,\n"
        "  # never a deployed URL)."
    )
    s6_new = (
        "  # Old steps 7+8 (deploy, then film local-only) become step 8 (deploy,\n"
        "  # then /demo films the LOCAL app only \u2014 video from code, never a\n"
        "  # deployed URL)."
    )

    subs = [
        ("S1", s1_old, s1_new, 1),
        ("S2", s2_old, s2_new, 1),
        ("S3", s3_old, s3_new, 1),
        ("S4", s4_old, s4_new, 2),
        ("S5", s5_old, s5_new, 1),
        ("S6", s6_old, s6_new, 1),
    ]
    for name, old, new, expected in subs:
        found = text.count(old)
        assert found == expected, (
            f"{name}: expected {expected} occurrence(s), found {found}: "
            f"{old[:80]!r}"
        )
        text = text.replace(old, new)

    # Post-checks: no removed-design wording may remain anywhere in build.sh.
    for banned in (
        "films the real deployed app",
        "film the deployed app (or the local dev server",
        "set `shots.json` `app.url` to the deployed URL",
        "film the real app by default",
        "deploy films deployed URL",
    ):
        assert text.count(banned) == 0, f"removed design still present: {banned!r}"

    open(path, "w", encoding="utf-8").write(text)
    print("fix5-audit-m2: deployed-URL filming design removed from build.sh "
          "(S1-S6 applied)")


if __name__ == "__main__":
    main()
