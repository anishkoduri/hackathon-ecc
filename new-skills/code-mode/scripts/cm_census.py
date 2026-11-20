"""cm_census — token census for the code-mode helper library.

The E3 estimator is this plugin's canonical estimator (a
regex-piece algorithm): split text into word runs / number runs
/ single symbols (1 each), plus +1 per 4 chars beyond 8 for long
alpha pieces. Every census figure this plugin reports uses it, so a
script's distilled return is measured with the same ruler as the
skill censuses. Stdlib only.

Contract: e3(text) -> int; census_file(path) -> one record;
census_tree(root, suffixes) -> per-file records + totals. Records
are plain dicts so cm_report can digest them without imports
crossing the other way.
"""
from __future__ import annotations

import os
import re
from typing import Iterable, TypedDict

_PIECE = re.compile(r"[A-Za-z]+|[0-9]+|[^\sA-Za-z0-9]")


class CensusRecord(TypedDict):
    path: str
    e3: int
    bytes: int
    lines: int


def e3(text: str) -> int:
    """Estimated tokens (E3) of a text — the plugin's ruler."""
    n = 0
    for m in _PIECE.finditer(text):
        s = m.group(0)
        n += 1
        if s.isalpha() and len(s) > 8:
            n += (len(s) - 8 + 3) // 4
    return n


def census_file(path: str) -> CensusRecord:
    """Census one file: E3, byte size, line count."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return {
        "path": path,
        "e3": e3(text),
        "bytes": len(text.encode("utf-8")),
        "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
    }


def census_tree(root: str, suffixes: Iterable[str] = (".md",)) -> dict:
    """Census every file under root whose name ends in a suffix.

    Returns {"files": [CensusRecord, ...] sorted by path,
    "totals": {"files": n, "e3": sum, "bytes": sum}}. The full
    record list is raw output — write it to a file and return a
    cm_report digest to the model, never the list itself.
    """
    wanted = tuple(suffixes)
    records: list[CensusRecord] = []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            if name.endswith(wanted):
                records.append(census_file(os.path.join(dirpath, name)))
    records.sort(key=lambda r: r["path"])
    return {
        "files": records,
        "totals": {
            "files": len(records),
            "e3": sum(r["e3"] for r in records),
            "bytes": sum(r["bytes"] for r in records),
        },
    }
