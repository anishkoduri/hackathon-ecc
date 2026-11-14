#!/usr/bin/env python3
"""Fix #22 §13-§17 applier (coordinator tool).

Parses the five patch-spec files (depth, orbs, libraries15, vercel,
libraries17), validates every anchor (count==1, in application order,
simulated per target file), then applies:
  - staged-source patches directly to their staged files,
  - runtime-block patches by appending constants + 6-tuples to fix22.py
    PATCHES (fix22.py itself is then run by the coordinator; its
    preflight re-validates everything against the built tree),
  - VERCEL-01 as a new file round2-skills/polish-pass/reference/vercel-checklist.md.

Usage: python3 apply22.py            # dry-run: parse + validate only
       python3 apply22.py --apply    # apply (writes files)

Apply-time decisions recorded here (see also fix22/MANIFEST.md):
  D-A1  'after' texts are normalised to the wave-1 convention: an 'after'
        insert must start with a paragraph break. Fence-extracted 'after'
        texts that start with a non-whitespace character get "\\n\\n"
        prepended; a leading single space (ORB-ORCH) is replaced by
        "\\n\\n". Vercel tuples are Python literals and are applied
        verbatim (VERCEL-02/03's leading space is a deliberate
        mid-sentence continuation).
  D-A2  L15-06 is CONVERTED from a global-source edit to a runtime-block
        patch on skills/less-flat-ui/SKILL.md (mode before, anchor
        "### 3. Thermal gradients"). The fix22 block runs after the
        build.sh:263 copy of the global source, so a runtime patch
        survives rebuilds; editing the shared global Cursor skill would
        leak a plugin-scoped note into Anish's general Cursor skill.
        Precedent: DEPTH-13 + Batch E (build.sh:20972-21004).
  D-A3  DEPTH-03's new text is IDENTICAL to DEPTH-02's (per the spec).
  D-A4  L17-06 is a staged direct edit (per the spec's ordering note);
        it carries no new _F22 token.
"""
import ast
import os
import re
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
FIX22 = os.path.join(PLUGIN, "fix22")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BANNED = ("claude", "codex", "anthropic", "opus", "sonnet", "haiku",
          "composer-2.5")
APPLY = "--apply" in sys.argv

# ---------------------------------------------------------------- helpers


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def lines_of(path):
    return read(path).split("\n")


def is_fence(line):
    # Fences may be indented (lib15/lib17 anchor fences sit inside list
    # items, "  ```"). The content they wrap is indented by the same
    # amount and must be dedented to match the target file.
    return line.strip() in ("```", "```md")


def fence_indent(line):
    return len(line) - len(line.lstrip(" "))


def dedent_by(lines, n):
    out = []
    for line in lines:
        if n and line.startswith(" " * n):
            out.append(line[n:])
        else:
            out.append(line)
    return out


def find_fence(lines, start, label):
    """Return (open_idx, close_idx, indent) of the first fenced block
    at/after `start`. Used for ANCHOR blocks (no inner fences)."""
    i = start
    while i < len(lines) and not is_fence(lines[i]):
        i += 1
    if i >= len(lines):
        raise ValueError("no opening fence after %s (from line %d)"
                         % (label, start))
    indent = fence_indent(lines[i])
    j = i + 1
    while j < len(lines) and not is_fence(lines[j]):
        j += 1
    if j >= len(lines):
        raise ValueError("no closing fence after %s (from line %d)"
                         % (label, start))
    return i, j, indent


def find_text_fence(lines, start, end, label):
    """Return (open_idx, close_idx) of a NEW-TEXT fenced block: the open
    is the first fence at/after `start`; the close is the LAST fence line
    before `end` (new text may contain inner ```ts/```tsx blocks whose
    closing lines are plain ``` lines)."""
    i = start
    while i < end and not is_fence(lines[i]):
        i += 1
    if i >= end:
        raise ValueError("no opening fence for %s" % label)
    closes = [k for k in range(i + 1, end) if is_fence(lines[k])]
    if not closes:
        raise ValueError("no closing fence for %s" % label)
    return i, closes[-1]


def block_text(lines, open_idx, close_idx):
    return "\n".join(lines[open_idx + 1:close_idx])


def apply_patch(text, old, new, mode):
    if mode == "after":
        return text.replace(old, old + new)
    if mode == "before":
        return text.replace(old, new.rstrip("\n") + "\n\n" + old)
    return text.replace(old, new)  # replace


def norm_after(pid, new):
    """Wave-1 'after' convention: the insert starts with a paragraph
    break. Returns (new_text, note-or-None)."""
    if new.startswith("\n"):
        return new, None
    if new.startswith(" "):
        return "\n\n" + new.lstrip(" "), "leading-space replaced by blank line"
    if new:
        return "\n\n" + new, "prepended blank line"
    return new, None


def first_backtick(line):
    m = re.search(r"`([^`]+)`", line)
    return m.group(1) if m else None


# ---------------------------------------------------------------- patches
# A patch is a dict: id, kind ('staged'|'runtime'|'newfile'), file
# (plugin-relative path; for runtime, built-tree rel path), anchor, new,
# mode, token (None for L17-06), spec, norm_note.

PATCHES = []


def add_patch(pid, kind, file, anchor, new, mode, token, spec):
    PATCHES.append({"id": pid, "kind": kind, "file": file, "anchor": anchor,
                    "new": new, "mode": mode, "token": token, "spec": spec,
                    "norm_note": None})


def kind_for(path):
    if path.startswith(("new-skills/", "round2-skills/")):
        return "staged"
    return "runtime"


def split_sections(lines, header_re):
    """Split `lines` into (header_match, start_idx, end_idx) sections
    for every line matching header_re."""
    starts = [(i, header_re.match(lines[i]))
              for i in range(len(lines))]
    starts = [(i, m) for i, m in starts if m]
    out = []
    for n, (i, m) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        out.append((m, i, end))
    return out


# ---------------------------------------------------------------- §13 depth
def parse_depth():
    lines = lines_of(os.path.join(FIX22, "depth-patches.md"))
    # Group S section: "## Group S" .. "## Group R"; Group R: .. "## Report"
    gs = next(i for i, l in enumerate(lines) if l.startswith("## Group S"))
    gr = next(i for i, l in enumerate(lines) if l.startswith("## Group R"))
    rep = next(i for i, l in enumerate(lines) if l.startswith("## Report"))
    hdr = re.compile(r"^### (DEPTH-\d+) — ")
    texts = {}
    for m, i, end in split_sections(lines, hdr):
        pid = m.group(1)
        group = "S" if i < gr else "R"
        # File
        fl = next(k for k in range(i, end)
                  if lines[k].startswith("- **File:**"))
        file = first_backtick(lines[fl])
        # Anchor
        al = next(k for k in range(i, end)
                  if "Anchor" in lines[k] and lines[k].startswith("- **"))
        o, c, ind = find_fence(lines, al, pid + " anchor")
        anchor = "\n".join(dedent_by(lines[o + 1:c], ind))
        # Mode / Token
        ml = next(k for k in range(i, end)
                  if lines[k].startswith("- **Mode:**"))
        mode = first_backtick(lines[ml])
        tl = next(k for k in range(i, end)
                  if lines[k].startswith("- **Token:**"))
        token = first_backtick(lines[tl])
        # New text
        nl = next(k for k in range(i, end)
                  if lines[k].startswith("- **New text:**"))
        if "IDENTICAL" in lines[nl]:
            ref = re.search(r"DEPTH-\d+", lines[nl]).group(0)
            new = texts[ref]
        else:
            o2, c2 = find_text_fence(lines, nl, end, pid + " new text")
            new = block_text(lines, o2, c2)
        texts[pid] = new
        kind = "staged" if group == "S" else "runtime"
        if kind == "staged" and not kind_for(file) == "staged":
            raise ValueError("%s: Group S file %s is not staged" % (pid, file))
        add_patch(pid, kind, file, anchor, new, mode, token, "depth")


# ---------------------------------------------------------------- §14 orbs
def parse_orbs():
    lines = lines_of(os.path.join(FIX22, "orbs-patches.md"))
    hdr = re.compile(r"^### (ORB-[A-Z0-9]+) — ")
    for m, i, end in split_sections(lines, hdr):
        pid = m.group(1)
        if pid not in ("ORB-MP", "ORB-MF", "ORB-UIPRO", "ORB-ORCH",
                       "ORB-PP1", "ORB-PP2"):
            continue  # report subsections, not patches
        fl = next(k for k in range(i, end)
                  if lines[k].startswith("- **file:**"))
        file = first_backtick(lines[fl])
        al = next(k for k in range(i, end)
                  if lines[k].startswith("- **anchor"))
        o, c, ind = find_fence(lines, al, pid + " anchor")
        anchor = "\n".join(dedent_by(lines[o + 1:c], ind))
        ml = next(k for k in range(i, end)
                  if lines[k].startswith("- **mode:**"))
        mode = first_backtick(lines[ml])
        nl = next(k for k in range(i, end)
                  if lines[k].startswith("- **new_text:**"))
        o2, c2 = find_text_fence(lines, nl, end, pid + " new text")
        new = block_text(lines, o2, c2)
        add_patch(pid, kind_for(file), file, anchor, new, mode,
                  "ORBS_F22", "orbs")


# ------------------------------------------------------- §15/§17 libraries
def parse_summary_table(lines, prefix):
    """Return {pid: (file, mode, token)} from the Summary table."""
    out = {}
    for line in lines:
        m = re.match(r"^\| (L1[57]-\d+) \| `([^`]+)`[^|]*\| (\w+) \|[^|]*\| (.*) \|$",
                     line)
        if m and m.group(1).startswith(prefix):
            toks = re.findall(r"`([A-Z0-9_]+_F22)`", m.group(4))
            out[m.group(1)] = (m.group(2), m.group(3),
                               toks[0] if toks else None)
    return out


def parse_libraries(spec_file, prefix):
    lines = lines_of(os.path.join(FIX22, spec_file))
    table = parse_summary_table(lines, prefix)
    hdr = re.compile(r"^## (%s-\d+) — " % prefix)
    for m, i, end in split_sections(lines, hdr):
        pid = m.group(1)
        file, mode_tbl, token = table[pid]
        # Anchor label line + fence
        al = next(k for k in range(i, end)
                  if lines[k].startswith("- **Anchor"))
        if "BEFORE" in lines[al]:
            mode_sec = "before"
        elif "AFTER" in lines[al]:
            mode_sec = "after"
        elif "REPLACE" in lines[al]:
            mode_sec = "replace"
        else:
            raise ValueError("%s: mode not in anchor line" % pid)
        if mode_sec != mode_tbl:
            raise ValueError("%s: table mode %s != section mode %s"
                             % (pid, mode_tbl, mode_sec))
        o, c, ind = find_fence(lines, al, pid + " anchor")
        anchor = "\n".join(dedent_by(lines[o + 1:c], ind))
        # Insert / New text fence
        nl = next(k for k in range(i, end)
                  if lines[k].startswith("- **Insert (full text):")
                  or lines[k].startswith("- **New text (replaces"))
        o2, c2 = find_text_fence(lines, nl, end, pid + " insert")
        new = block_text(lines, o2, c2)
        add_patch(pid, kind_for(file), file, anchor, new, mode_tbl,
                  token, spec_file.replace("-patches.md", ""))


# ---------------------------------------------------------------- §16 vercel
def parse_vercel():
    lines = lines_of(os.path.join(FIX22, "vercel-patches.md"))
    # Tuples: the ```python fence in §1 — exec the assignments, eval the
    # tuple expressions via AST so no string is retyped.
    py_open = next(i for i, l in enumerate(lines) if l == "```python")
    py_close = next(i for i in range(py_open + 1, len(lines))
                    if lines[i] == "```")
    src = "\n".join(lines[py_open + 1:py_close])
    tree = ast.parse(src)
    ns = {}
    tuples = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            ns[node.targets[0].id] = ast.literal_eval(node.value)
        elif isinstance(node, ast.Expr):
            v = eval(compile(ast.Expression(node.value),
                             "<vercel>", "eval"), dict(ns))
            # The fence writes each tuple with a trailing comma, so at
            # module level it parses as a 1-tuple holding the 6-tuple.
            if len(v) == 1 and isinstance(v[0], tuple):
                v = v[0]
            tuples.append(v)
    for t in tuples:
        pid, file, anchor, new, mode, token = t
        add_patch(pid, "runtime", file, anchor, new, mode, token,
                  "vercel")
    # VERCEL-01 new file: lines 93..546 (1-indexed) — the ```markdown
    # fence content (see the fence at line 92, close at line 547).
    md_open = next(i for i, l in enumerate(lines) if l == "```markdown")
    # close: the ``` line immediately before "## 3. Report"
    rep3 = next(i for i, l in enumerate(lines)
                if l.startswith("## 3. Report"))
    md_close = max(i for i in range(md_open + 1, rep3) if lines[i] == "```")
    content = "\n".join(lines[md_open + 1:md_close])
    PATCHES.append({"id": "VERCEL-01", "kind": "newfile",
                    "file": "round2-skills/polish-pass/reference/vercel-checklist.md",
                    "anchor": None, "new": content, "mode": None,
                    "token": "VERCEL_F22", "spec": "vercel",
                    "norm_note": None})


# ---------------------------------------------------------------- build list
def build_patch_list():
    parse_depth()
    parse_orbs()
    parse_libraries("libraries15-patches.md", "L15")
    parse_vercel()
    parse_libraries("libraries17-patches.md", "L17")
    # D-A2: L15-06 conversion — global-source edit -> runtime-block patch.
    for p in PATCHES:
        if p["id"] == "L15-06":
            p["kind"] = "runtime"
            p["file"] = "skills/less-flat-ui/SKILL.md"
            p["norm_note"] = ("CONVERTED to runtime block on the built copy "
                              "(see D-A2); global source NOT edited")
    # L17-06 carries no new _F22 token (its new text only adds the words
    # "a Casberry particle export" to L15-08's list; CASBERRY_F22 for the
    # checklist file is carried by L17-07 alone — see the spec's token
    # note). The summary-table regex grabs CASBERRY_F22 from the note;
    # override it to None so the token check is skipped.
    for p in PATCHES:
        if p["id"] == "L17-06":
            p["token"] = None
    # first line ("  Colors: ..." — the file's line is
    # "  decision record; Colors: ..."). The correct anchor is
    # DEPTH-08's (same two lines, no leading indent); the §14 agent
    # copied the continuation indent as if "Colors:" started the line.
    for p in PATCHES:
        if p["id"] == "ORB-PP1":
            p["anchor"] = ("Colors: color (H1) is one accentuation means, "
                           "used for\n  action/emphasis only.")
            p["norm_note"] = ("anchor corrected (D-A5): dropped spurious "
                              "2-space indent on first line; now identical "
                              "to DEPTH-08's anchor")
    # Normalise 'after' texts (fence-extracted only, not vercel tuples).
    for p in PATCHES:
        if p["kind"] in ("staged", "runtime") and p["mode"] == "after" \
                and p["spec"] != "vercel":
            p["new"], note = norm_after(p["id"], p["new"])
            if note:
                p["norm_note"] = (p["norm_note"] + "; " if p["norm_note"]
                                  else "") + "after-norm: " + note

# ---------------------------------------------------------------- validate
FILE_CONST = {
    "skills/motion-foundations/SKILL.md": "MF",
    "skills/motion-patterns/SKILL.md": "MP",
    "skills/ui-ux-pro-max/SKILL.md": "UIPRO",
    "skills/less-flat-ui/SKILL.md": "LFUI",
    "skills/design-system/SKILL.md": "DS",
    "skills/polish-pass/SKILL.md": "PP",
    "skills/ui-ux-pro-max/references/quick-reference.md": "UIPRO_QR",
}
NEW_CONSTS = {"LFUI": "skills/less-flat-ui/SKILL.md",
              "DS": "skills/design-system/SKILL.md",
              "PP": "skills/polish-pass/SKILL.md"}


def const_name(pid):
    return pid.replace("-", "")


def validate():
    """Simulate every patch in order; fail loudly on any problem.
    Returns (sim_staged, sim_built, notes) where the sims map
    plugin-relative path -> simulated content."""
    sim_staged, sim_built = {}, {}
    orig_staged, orig_built = {}, {}
    notes = []
    for p in PATCHES:
        pid = p["id"]
        if p["kind"] == "newfile":
            dest = os.path.join(PLUGIN, p["file"])
            if os.path.exists(dest):
                raise ValueError("%s: new file already exists: %s"
                                 % (pid, p["file"]))
            if "VERCEL_F22" not in p["new"]:
                raise ValueError("%s: new file lacks its token" % pid)
            notes.append("%s new file %s (%d lines, token present)"
                         % (pid, p["file"], p["new"].count("\n") + 1))
            continue
        # Load the target's original + simulated text.
        if p["kind"] == "staged":
            store, orig = sim_staged, orig_staged
            path = os.path.join(PLUGIN, p["file"])
        else:
            store, orig = sim_built, orig_built
            path = os.path.join(BUILT, p["file"])
        if p["file"] not in store:
            store[p["file"]] = read(path)
            orig[p["file"]] = store[p["file"]]
        new = p["new"]
        # Banned terms + triple-quote safety (runtime constants only).
        low = new.lower()
        for term in BANNED:
            if term in low:
                raise ValueError("%s: banned term %r in new text" % (pid, term))
        if p["kind"] == "runtime" and '"""' in new:
            raise ValueError("%s: new text contains triple-quote" % pid)
        # Token: absent from the ORIGINAL file, present in the new text.
        tok = p["token"]
        if tok is not None:
            if tok in orig[p["file"]]:
                raise ValueError("%s: token %s already in original %s"
                                 % (pid, tok, p["file"]))
            if tok not in new:
                raise ValueError("%s: new text lacks its token %s"
                                 % (pid, tok))
        # Anchor count==1 in the simulated text; apply.
        n = store[p["file"]].count(p["anchor"])
        if n != 1:
            raise ValueError("%s: anchor count=%d in %s (expected 1); "
                             "anchor head: %r"
                             % (pid, n, p["file"], p["anchor"][:100]))
        store[p["file"]] = apply_patch(store[p["file"]], p["anchor"],
                                       new, p["mode"])
        note = "%s %s %s mode=%s anchor=%d chars new=%d chars" % (
            pid, p["kind"], p["file"], p["mode"], len(p["anchor"]),
            len(new))
        if p["norm_note"]:
            note += "  [%s]" % p["norm_note"]
        notes.append(note)
    return sim_staged, sim_built, notes


# ---------------------------------------------------------------- apply
def apply_all(sim_staged, sim_built):
    # 1. Staged files.
    for rel, text in sim_staged.items():
        dest = os.path.join(PLUGIN, rel)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote staged %s (%d lines)" % (rel, text.count("\n") + 1))
    # 2. New vercel checklist file.
    for p in PATCHES:
        if p["kind"] == "newfile":
            dest = os.path.join(PLUGIN, p["file"])
            with open(dest, "w", encoding="utf-8") as f:
                f.write(p["new"])
            print("wrote new file %s (%d lines)"
                  % (p["file"], p["new"].count("\n") + 1))
    # 3. fix22.py: new file constants + new-text constants + tuples.
    f22 = os.path.join(FIX22, "fix22.py")
    text = read(f22)
    # 3a. File constants after GAN_EVALUATOR.
    anchor_const = 'GAN_EVALUATOR = "agents/ecc-gan-evaluator.md"\n'
    assert text.count(anchor_const) == 1
    add = "".join('%s = "%s"\n' % (k, v) for k, v in NEW_CONSTS.items())
    text = text.replace(anchor_const, anchor_const + add, 1)
    # 3b. New-text constants before PATCHES.
    const_defs = ["\n# --- fix #22 §13-§17 additions (apply22.py) ---\n"]
    tuples = []
    for p in PATCHES:
        if p["kind"] != "runtime":
            continue
        if p["spec"] == "vercel":
            # Verbatim tuples from the spec (they use PP/UIPRO_QR/MF).
            tuples.append("    (%r, %s, %r, %r, %r, %r),"
                          % (p["id"], FILE_CONST[p["file"]], p["anchor"],
                             p["new"], p["mode"], p["token"]))
            continue
        name = const_name(p["id"])
        new = p["new"]
        if '"""' in new or new.endswith('"') or "\\" in new:
            const_defs.append("%s = %r\n" % (name, new))
        else:
            const_defs.append('%s = """%s"""\n' % (name, new))
        tuples.append("    (%r, %s, %r, %s, %r, %r),"
                      % (p["id"], FILE_CONST[p["file"]], p["anchor"],
                         name, p["mode"], p["token"]))
    marker = "PATCHES = [\n"
    assert text.count(marker) == 1
    text = text.replace(marker, "".join(const_defs) + "\n" + marker, 1)
    # 3c. Tuples before the closing ] of PATCHES.
    idx = text.index(marker)
    close = text.index("\n]\n", idx)
    text = text[:close] + "\n" + "\n".join(tuples) + text[close:]
    with open(f22, "w", encoding="utf-8") as f:
        f.write(text)
    print("fix22.py: added %d file constants, %d new-text constants, "
          "%d runtime tuples" % (len(NEW_CONSTS), len(const_defs) - 1,
                                 len(tuples)))


def main():
    build_patch_list()
    print("parsed %d patches (%d staged, %d runtime, %d newfile)"
          % (len(PATCHES),
             sum(1 for p in PATCHES if p["kind"] == "staged"),
             sum(1 for p in PATCHES if p["kind"] == "runtime"),
             sum(1 for p in PATCHES if p["kind"] == "newfile")))
    sim_staged, sim_built, notes = validate()
    print("VALIDATION OK — %d patches" % len(PATCHES))
    for n in notes:
        print("  " + n)
    if not APPLY:
        print("dry-run only (no files written). Re-run with --apply.")
        return
    apply_all(sim_staged, sim_built)
    print("APPLIED.")


if __name__ == "__main__":
    main()
