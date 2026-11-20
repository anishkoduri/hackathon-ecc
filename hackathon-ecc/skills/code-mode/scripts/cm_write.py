"""cm_write — guarded writes for code-mode scripts.

The write side of the library, deliberately narrow (SCRIPT-GATE_F34
enforced in code, not just in prose):

- Every target path is resolved and must stay INSIDE the declared
  project root — a script that tries to write outside its scope
  raises GuardError instead of writing.
- Writes are serialized by construction: one call writes one file;
  there is no batch or parallel write API.
- Overwriting an existing file requires overwrite=True, stated in
  the script where the gate review can see it.
- There is NO delete operation in this library at all. A script
  that needs to remove a file cannot do it through the helpers —
  that work stays with the orchestrator's direct, approved calls.

Stdlib only. Contract: write_text(path, text, root, overwrite) ->
record; append_line(path, line, root) -> record.
"""
from __future__ import annotations

import os
from typing import TypedDict


class GuardError(Exception):
    """A guarded write refused: out of scope, or an unflagged overwrite."""


class WriteRecord(TypedDict):
    path: str
    bytes: int
    action: str  # "created" | "overwritten" | "appended"


def _in_scope(path: str, root: str) -> str:
    """Resolve path against root; refuse anything that escapes it."""
    root_abs = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root_abs, path)
                              if not os.path.isabs(path) else path)
    if target != root_abs and not target.startswith(root_abs + os.sep):
        raise GuardError(f"out of scope: {path!r} resolves to {target!r}, "
                         f"outside the declared root {root_abs!r}")
    return target


def write_text(path: str, text: str, root: str,
               overwrite: bool = False) -> WriteRecord:
    """Write one file inside root. Refuses an existing file unless
    overwrite=True. Creates parent directories inside the scope."""
    target = _in_scope(path, root)
    existed = os.path.exists(target)
    if existed and not overwrite:
        raise GuardError(f"refusing to overwrite {path!r} without "
                         f"overwrite=True (SCRIPT-GATE_F34 item 3)")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(text)
    return {"path": path, "bytes": len(text.encode("utf-8")),
            "action": "overwritten" if existed else "created"}


def append_line(path: str, line: str, root: str) -> WriteRecord:
    """Append one line to a file inside root (ledger-style appends:
    the file is never rewritten in place, only extended)."""
    target = _in_scope(path, root)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "a", encoding="utf-8") as fh:
        fh.write(line.rstrip("\n") + "\n")
    return {"path": path, "bytes": len(line.encode("utf-8")) + 1,
            "action": "appended"}
