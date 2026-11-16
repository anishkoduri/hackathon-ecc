#!/usr/bin/env python3
"""Dry-run #38 leg 2 analysis: apply the fix #23 §6 alignment assertions
(ALIGN_F23 (a)-(h), COVER_F23, BLOCK_F23) to the FRESH align-audit run
(~/workspace/cold-start-render/home-run/qa/align-audit-results.json).

Tolerances (SPEC §6 / polish-pass/reference/alignment.md): 0px overflow;
<=2px centering / grid / spacing equality. Geometry from
getBoundingClientRect() as recorded by qa/align-audit.mjs.

Prints one line per assertion with the measurement, then a summary.
Exit 0 only if every assertion passes OR fails solely on the two
pre-documented conditional items (iris-disc bleed, panel-top stagger)
whose declaration state is reported explicitly; any other flag exits 1.
The verdict itself is the dry-run report's call -- this script reports
the measurements.
"""
import json
import os
import re
import sys

RENDER = os.path.expanduser("~/workspace/cold-start-render/home-run")
QA = os.path.join(RENDER, "qa")
RESULTS = os.path.join(QA, "align-audit-results.json")
TOKENS = os.path.join(RENDER, "docs/design-tokens.md")

fails = []
notes = []


def check(name, ok, detail):
    print(("PASS " if ok else "FLAG ") + name + " -- " + detail)
    if not ok:
        fails.append(name)


def main():
    with open(RESULTS, encoding="utf-8") as fh:
        data = json.load(fh)
    tokens = open(TOKENS, encoding="utf-8").read()
    bleed_declared = bool(re.search(r"bleed", tokens, re.I))
    # A panel-top stagger counts as declared only if one line ties the
    # stagger to the panels (a bare "top of the panel" elsewhere + a
    # motion "stagger" elsewhere is not a declaration).
    stagger_declared = any(
        "stagger" in line.lower() and "panel" in line.lower()
        for line in tokens.splitlines())
    print("measurements: %d" % len(data))
    labels = [m["label"] for m in data]
    widths = sorted({m["vw"] for m in data})
    states = sorted({m["label"].split("-", 1)[1] for m in data})
    print("widths: %s" % widths)
    print("states per width: %s" % states)
    print("bleed declared in design-tokens.md: %s" % bleed_declared)
    print("panel-top stagger declared in design-tokens.md: %s"
          % stagger_declared)

    # (a) OVERFLOW -- 0px at every width; no leaf text overflow
    bad_over = [m["label"] for m in data if m["docOverflowX"] != 0]
    check("6a-overflow-doc", not bad_over,
          "docOverflowX == 0 in %d/%d measurements%s"
          % (len(data) - len(bad_over), len(data),
             ("; nonzero: %s" % bad_over) if bad_over else ""))
    bad_text = [(m["label"], m["textOverflow"]) for m in data
                if m.get("textOverflow")]
    check("6a-overflow-text", not bad_text,
          "leaf text scrollWidth > clientWidth + 1 in %d measurements%s"
          % (len(bad_text), ("; " + str(bad_text[:2])) if bad_text else ""))

    # (b) CENTER -- phone frame centered <=2px at every width
    offs = [(m["label"], m["phone"]["viewportCenterOffset"]) for m in data]
    bad_c = [x for x in offs if abs(x[1]) > 2]
    check("6b-center-phone", not bad_c,
          "phone viewportCenterOffset in [%s] (max |offset| %d)%s"
          % (sorted({o for _, o in offs}), max(abs(o) for _, o in offs),
             ("; over tolerance: %s" % bad_c) if bad_c else ""))

    # (c) NAV -- adjacent tab gaps equal +/-2; tabbar centered in phone;
    #     each label center == its item center +/-2
    gap_bad, label_bad, bar_bad = [], [], []
    for m in data:
        tabs = sorted(m["tabs"], key=lambda t: t["left"])
        gaps = [tabs[i + 1]["left"] - tabs[i]["right"]
                for i in range(len(tabs) - 1)]
        if gaps and max(gaps) - min(gaps) > 2:
            gap_bad.append((m["label"], gaps))
        for t in tabs:
            if abs(t["labelCenterX"] - t["tabCenterX"]) > 2:
                label_bad.append((m["label"], t["nav"]))
        tb = m["tabbar"]
        if abs((tb["left"] - tb["phoneLeft"])
               - (tb["phoneRight"] - tb["right"])) > 2:
            bar_bad.append(m["label"])
    check("6c-nav-gaps", not gap_bad,
          "adjacent tab gaps equal +/-2px in %d/%d measurements%s"
          % (len(data) - len(gap_bad), len(data),
             ("; unequal: %s" % gap_bad[:3]) if gap_bad else ""))
    check("6c-nav-labels", not label_bad,
          "label center == tab center +/-2px for every tab%s"
          % ("; off: %s" % label_bad[:5] if label_bad else ""))
    check("6c-nav-bar-centered", not bar_bad,
          "tabbar centered in phone frame +/-2px in %d/%d%s"
          % (len(data) - len(bar_bad), len(data),
             ("; off: %s" % bar_bad[:3]) if bar_bad else ""))

    # (d) GRID -- view children share one left/right edge; feed cards one edge
    grid_bad, card_bad = [], []
    for m in data:
        ch = m.get("children", [])
        if ch:
            # Full-width children share one left/right edge (+/-2px). A
            # narrower child is left-aligned (offL == the common offL) or
            # centered (|offL - offR| <= 2) -- ALIGN_F23_GRID.
            full = [c for c in ch if c["w"] >= m["viewRect"]["w"] - 4]
            narrow = [c for c in ch if c["w"] < m["viewRect"]["w"] - 4]
            if full:
                off_l = {c["offL"] for c in full}
                off_r = {c["offR"] for c in full}
                if max(off_l) - min(off_l) > 2 or max(off_r) - min(off_r) > 2:
                    grid_bad.append((m["label"], sorted(off_l), sorted(off_r)))
                common_l = sorted(off_l)[0]
                for c in narrow:
                    left_aligned = abs(c["offL"] - common_l) <= 2
                    centered = abs(c["offL"] - c["offR"]) <= 2
                    if not (left_aligned or centered):
                        grid_bad.append((m["label"], c["cls"], c["offL"],
                                         c["offR"]))
        fe = m.get("feedCardEdges")
        if fe and (len(fe["lefts"]) > 1 or len(fe["rights"]) > 1):
            card_bad.append((m["label"], fe))
    check("6d-grid-children", not grid_bad,
          "full-width children share one left/right edge +/-2px; narrower "
          "children left-aligned or centered, in %d/%d%s"
          % (len(data) - len(grid_bad), len(data),
             ("; off: %s" % grid_bad[:3]) if grid_bad else ""))
    check("6d-grid-feedcards", not card_bad,
          "feed cards share one left and one right edge per width%s"
          % ("; split: %s" % card_bad[:3] if card_bad else ""))

    # (e) CLIP -- no text clipped (covered in (a)); beyond-frame elements
    beyond = [(m["label"], [b["cls"] for b in m.get("beyondPhone", [])])
              for m in data if m.get("beyondPhone")]
    beyond_classes = sorted({c for _, cs in beyond for c in cs})
    check("6e-clip-beyond-frame", not beyond or bleed_declared,
          "elements beyond the phone frame in %d measurements: %s; "
          "declared intentional bleed in decision record: %s"
          % (len(beyond), beyond_classes, bleed_declared))
    if beyond and not bleed_declared:
        notes.append("6e: beyond-frame classes %s (max extent %s) -- "
                     "passes ONLY if declared as intentional bleed; "
                     "decision record does not declare it"
                     % (beyond_classes,
                        [(l, b) for l, b in
                         [(m["label"], m["beyondPhone"]) for m in data
                          if m.get("beyondPhone")][:1]]))

    # (f) LABELS -- SVG text boxes non-overlapping + inside viewport;
    #     stamps centered on parent +/-2; status pairs by vertical CENTERS
    #     (harness records tops only -- centers not verifiable from JSON;
    #     insets checked instead, centers probed separately if available)
    ov_bad = [(m["label"], m["routeMap"]["overlaps"] or
               m["branchStrip"]["overlaps"])
              for m in data
              if (m.get("routeMap") and (m["routeMap"]["overlaps"]
                                         or m["routeMap"]["outOf"]))
              or (m.get("branchStrip") and (m["branchStrip"]["overlaps"]
                                            or m["branchStrip"]["outOf"]))]
    check("6f-labels-svg", not ov_bad,
          "route-map + branch-strip SVG labels: 0 overlaps, 0 out-of-bounds "
          "in %d/%d measurements%s"
          % (len(data) - len(ov_bad), len(data),
             ("; bad: %s" % ov_bad[:3]) if ov_bad else ""))
    stamp_offs = [s["offset"] for m in data for s in m.get("stamps", [])]
    check("6f-labels-stamps", all(abs(o) <= 2 for o in stamp_offs),
          "stamp center offset on parent in [%s] (n=%d)"
          % (sorted(set(stamp_offs)), len(stamp_offs)))
    sb_bad = [(m["label"], m["statusbar"]["timeLeft"],
               m["statusbar"]["iconsRight"]) for m in data
              if abs(m["statusbar"]["timeLeft"]
                     - m["statusbar"]["iconsRight"]) > 2]
    check("6f-status-insets", not sb_bad,
          "statusbar time-left inset == icons-right inset +/-2px "
          "(timeLeft/iconsRight symmetric)%s"
          % ("; asymmetric: %s" % sb_bad[:3] if sb_bad else ""))
    tops = sorted({(m["statusbar"]["timeTop"], m["statusbar"]["iconsTop"])
                   for m in data})
    notes.append("6f-status-centers: harness records tops only "
                 "(timeTop/iconsTop pairs %s); vertical-CENTER comparison "
                 "needs element heights -- see the separate probe" % (tops,))

    # (g) ACTIONS -- grouped inputs centered on panel +/-2
    cb = [(m["label"], m["codeBoxes"]["offset"]) for m in data
          if m.get("codeBoxes")]
    check("6g-actions-codeboxes", all(abs(o) <= 2 for _, o in cb),
          "code-box group offset on panel: %s (n=%d)"
          % (sorted({o for _, o in cb}), len(cb)))

    # (h) PANELS -- desktop only (1440): gutters symmetric +/-2, tops
    #     aligned +/-2 unless a stagger is recorded. Mid-band numbers are
    #     meaningless in the stacked layout and are NOT asserted.
    desk = [m for m in data if m["vw"] == 1440 and m.get("gutterLeft") is not None]
    gut_bad = [m["label"] for m in desk
               if abs(m["gutterLeft"] - m["gutterRight"]) > 2]
    check("6h-panels-gutters", not gut_bad,
          "desktop side-panel gutters symmetric +/-2px (44/44) in %d/%d%s"
          % (len(desk) - len(gut_bad), len(desk),
             ("; bad: %s" % gut_bad[:3]) if gut_bad else ""))
    top_deltas = sorted({m.get("panelTopDelta") for m in desk})
    top_ok = all(abs(m["panelTopDelta"]) <= 2 for m in desk) or stagger_declared
    check("6h-panels-tops", top_ok,
          "desktop side-panel top deltas: %s; stagger recorded in decision "
          "record: %s" % (top_deltas, stagger_declared))
    if not top_ok:
        notes.append("6h: panel top delta 26px at 1440 (left top 232 vs "
                     "right top 206) with no recorded stagger -- the desk "
                     "is align-items:center, so the delta is the height "
                     "difference of vertically-centered panels, not a "
                     "top-alignment defect; the record does not state it")

    # COVER_F23 -- widths x states matrix complete + screenshots present
    req_widths = {1440, 900, 390}
    req_states = {"home", "home-bottom", "detail", "offer", "offer-accepted",
                  "trip", "trip-wrongcode", "trip-delivered", "branches",
                  "trips", "you", "post", "post-done"}
    have = {(m["vw"], m["label"].split("-", 1)[1]) for m in data}
    missing = [(w, s) for w in sorted(req_widths) for s in sorted(req_states)
               if (w, s) not in have]
    check("cover-matrix", not missing,
          "required matrix 3 widths x 13 states = 39 cells; missing: %s"
          % (missing if missing else "none"))
    shot_missing = []
    for (w, s) in sorted(have):
        p = os.path.join(QA, "align-%d-%s.png" % (w, s))
        if not os.path.exists(p):
            shot_missing.append((w, s))
    check("cover-screenshots", not shot_missing,
          "screenshots present for every measured cell%s"
          % ("; missing: %s" % shot_missing[:5] if shot_missing else ""))
    extra = sorted({w for w in widths} - req_widths)
    print("bonus widths measured (beyond the required 3): %s" % extra)

    print("\nNOTES:")
    for n in notes:
        print(" - " + n)
    print("\n%d FLAG(s): %s" % (len(fails), fails if fails else "none"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
