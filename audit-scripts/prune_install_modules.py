#!/usr/bin/env python3
"""Audit #6 (Fixer A), Defect 2: prune manifests/install-modules.json to the shipped subset.

Removes every `paths` entry that does not exist under the plugin root, drops
modules left with zero paths, and prunes `dependencies` / `optionalDependencies`
entries that name a dropped module (they would otherwise dangle).

Usage: run from the plugin root (paths in the manifest are plugin-relative):
    cd ~/workspace/hackathon-plugin/hackathon-ecc
    python3 ../audit-scripts/prune_install_modules.py

Writes a JSON summary to stdout and to install-modules.prune-report.json
next to this script (audit-scripts/, for the record — NOT inside the plugin).
The manifest itself is rewritten in place with json.dump(indent=2) + trailing
newline, preserving key order.
"""
import json
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.abspath(__file__))
# Script lives in <plugin-repo>/audit-scripts/, plugin root is hackathon-ecc/.
# Resolve robustly: prefer cwd if it contains manifests/install-modules.json.
if os.path.exists(os.path.join(os.getcwd(), "manifests", "install-modules.json")):
    PLUGIN_ROOT = os.getcwd()
else:
    PLUGIN_ROOT = os.path.join(os.path.dirname(PLUGIN_ROOT), "hackathon-ecc")

MANIFEST = os.path.join(PLUGIN_ROOT, "manifests", "install-modules.json")
REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "install-modules.prune-report.json")


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        data = json.load(f)
    modules = data["modules"]
    total_paths_before = sum(len(m.get("paths", [])) for m in modules)

    removed_paths = []          # (module_id, path)
    removed_modules = []        # module ids dropped for having zero paths
    pruned_dependencies = []    # (module_id, field, dep_id)
    kept = []
    for m in modules:
        kept_paths = []
        for p in m.get("paths", []):
            if os.path.exists(os.path.join(PLUGIN_ROOT, p)):
                kept_paths.append(p)
            else:
                removed_paths.append((m["id"], p))
        if not kept_paths:
            removed_modules.append(m["id"])
            continue
        m["paths"] = kept_paths
        kept.append(m)

    dropped = set(removed_modules)
    for m in kept:
        for field in ("dependencies", "optionalDependencies"):
            deps = m.get(field)
            if not deps:
                continue
            kept_deps = [d for d in deps if d not in dropped]
            for d in deps:
                if d in dropped:
                    pruned_dependencies.append((m["id"], field, d))
            if kept_deps:
                m[field] = kept_deps
            else:
                m.pop(field, None)

    data["modules"] = kept
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    total_paths_after = sum(len(m.get("paths", [])) for m in kept)
    report = {
        "total_path_entries_before": total_paths_before,
        "total_path_entries_after": total_paths_after,
        "removed_path_entries": len(removed_paths),
        "modules_before": len(modules),
        "modules_after": len(kept),
        "removed_modules": removed_modules,
        "removed_paths": [{"module": mid, "path": p} for mid, p in removed_paths],
        "pruned_dependencies": [
            {"module": mid, "field": field, "dependency": dep}
            for mid, field, dep in pruned_dependencies
        ],
    }
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")

    print(f"modules: {len(modules)} -> {len(kept)} (removed {len(removed_modules)}: {removed_modules})")
    print(f"path entries: {total_paths_before} -> {total_paths_after} (removed {len(removed_paths)})")
    print(f"pruned dangling dependencies: {len(pruned_dependencies)}: {pruned_dependencies}")
    print(f"report: {REPORT}")


if __name__ == "__main__":
    main()
