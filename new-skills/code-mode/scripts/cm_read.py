"""cm_read — file reading and searching for code-mode scripts.

Read-side helpers only: nothing in this module writes. grep returns
match RECORDS (path, line number, the matched line trimmed) so the
script can count, filter, and digest them in code — the model sees
the digest (via cm_report), not the raw match dump. Stdlib only.

Contract: read_text(path) -> str; list_files(root, suffixes) ->
sorted relative paths; grep(root, pattern, suffixes) -> records.
"""
from __future__ import annotations

import os
import re
from typing import Iterable, TypedDict


class Match(TypedDict):
    path: str
    line: int
    text: str


def read_text(path: str) -> str:
    """Read one file as UTF-8 text."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def list_files(root: str, suffixes: Iterable[str] = (".md",)) -> list[str]:
    """All files under root ending in a suffix, sorted, relative."""
    wanted = tuple(suffixes)
    out: list[str] = []
    for dirpath, _dirs, names in os.walk(root):
        for name in names:
            if name.endswith(wanted):
                out.append(os.path.relpath(os.path.join(dirpath, name), root))
    return sorted(out)


def grep(root: str, pattern: str, suffixes: Iterable[str] = (".md",),
         max_per_file: int = 1000) -> list[Match]:
    """Regex-search every matching file under root.

    Returns one record per matching line (line text trimmed to 200
    chars — records are for counting and digesting, not for quoting
    whole files). max_per_file bounds a runaway match set per file.
    """
    rx = re.compile(pattern)
    matches: list[Match] = []
    for rel in list_files(root, suffixes):
        full = os.path.join(root, rel)
        try:
            text = read_text(full)
        except (OSError, UnicodeDecodeError):
            continue
        per_file = 0
        for i, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                matches.append({"path": rel, "line": i,
                                "text": line.strip()[:200]})
                per_file += 1
                if per_file >= max_per_file:
                    break
    return matches
