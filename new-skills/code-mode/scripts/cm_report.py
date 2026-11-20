"""cm_report — distilled returns for code-mode scripts.

The return discipline of SCRIPT-FIRST_F34, enforced mechanically:
a script's model-facing output is at most CAP_E3 (500) estimated
tokens. Raw output goes to a file on disk; the model reads the
digest and re-reads the raw file selectively only when a digest
line needs evidence.

Why 500: a full work return runs to ~2,000 tokens (status,
files changed, decisions); a script return is a mechanical
digest — status, counts, exceptions, pointers — a strict
subset, so a quarter of that is generous. It also sits
under the ~600-token research-brief cap (RESEARCHBRIEF_F34), a
richer artifact consumed inline by two pipeline steps. A digest
that cannot fit in 500 E3 is not a digest; it is the firehose
wearing a summary's clothes, and distill() truncates it with a
pointer rather than letting it overflow.

Stdlib only; the E3 ruler is cm_census.e3 (same directory — the
script adds this directory to sys.path and imports what it needs).
"""
from __future__ import annotations

import os

from cm_census import e3

CAP_E3 = 500


def distill(headline: str, counts: dict[str, int],
            exceptions: list[str], raw_pointer: str,
            cap: int = CAP_E3) -> str:
    """Build a model-facing digest of at most `cap` E3.

    Shape: one headline line, one counts line, then exception lines
    (the findings the model must see), then the raw-output pointer.
    The cap is met structurally, in this order: exceptions are kept
    while they fit and the rest are dropped behind a "+N more" line
    naming the raw file — never silently; if the digest still
    overflows (a pathological headline), the headline is truncated
    by halving until it fits; only for an absurd input whose counts
    line alone overflows is the counts line truncated the same way.
    The "+N more" line and the raw pointer are never dropped.
    """
    head = f"OK {headline}" if not exceptions else f"DONE {headline}"
    counts_line = "counts: " + ", ".join(
        f"{k}={v}" for k, v in counts.items())
    raw_line = f"raw: {raw_pointer}"

    def more_line(dropped: int) -> str:
        return f"! +{dropped} more exceptions in {raw_pointer}"

    kept: list[str] = []
    for exc in exceptions:
        rest = len(exceptions) - len(kept) - 1
        trial = [head, counts_line] + kept + [f"! {exc}"]
        if rest:
            trial.append(more_line(rest))
        trial.append(raw_line)
        if e3("\n".join(trial)) > cap:
            break
        kept.append(f"! {exc}")
    dropped = len(exceptions) - len(kept)
    parts = [head, counts_line] + kept
    if dropped:
        parts.append(more_line(dropped))
    parts.append(raw_line)
    out = "\n".join(parts)
    if e3(out) > cap:
        # Pathological inputs only: shrink by halving — strictly
        # decreasing, so this always terminates (a fixed-step shrink
        # can map a short line to itself and spin). Headline first;
        # the counts line only for an absurd input. The "+N more"
        # and raw-pointer lines are never touched — the raw file
        # holds everything the digest abbreviates.
        for idx in (0, 1):
            while e3(out) > cap and len(parts[idx]) > 4:
                parts[idx] = parts[idx][: max(4, len(parts[idx]) // 2)]
                out = "\n".join(parts)
            if e3(out) <= cap:
                break
    return out


def finish(raw_text: str, raw_path: str, headline: str,
           counts: dict[str, int], exceptions: list[str],
           cap: int = CAP_E3) -> str:
    """Write the raw output to raw_path and return the digest.

    This is the last call of a code-mode script: everything the
    script gathered goes into the file; only the digest (<= cap E3)
    is printed for the model.
    """
    os.makedirs(os.path.dirname(os.path.abspath(raw_path)), exist_ok=True)
    with open(raw_path, "w", encoding="utf-8") as fh:
        fh.write(raw_text)
    return distill(headline, counts, exceptions, raw_path, cap)
