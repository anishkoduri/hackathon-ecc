---
name: instinct-import
description: Import instincts from file or URL into project/global scope
command: true
---

# Instinct Import Command

## Implementation

Run the instinct CLI using the plugin root path:

```bash
ECC_ROOT="$(node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)")" &&
python3 "$ECC_ROOT/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7] [--scope project|global]
```

Or, relative to the plugin root (manual installation, `ECC_PLUGIN_ROOT` not set):

```bash
python3 skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url>
```

Import instincts from local file paths or HTTP(S) URLs.

## Usage

```
/instinct-import team-instincts.yaml
/instinct-import https://github.com/org/repo/instincts.yaml
/instinct-import team-instincts.yaml --dry-run
/instinct-import team-instincts.yaml --scope global --force
```

## What to Do

1. Fetch the instinct file (local path or URL)
2. Parse and validate the format
3. Check for duplicates with existing instincts
4. Merge or add new instincts
5. Save to inherited instincts directory:
   - Project scope: `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/projects/<project-id>/instincts/inherited/`
   - Global scope: `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/instincts/inherited/`
   - Legacy homunculus data is not read (the migration script was removed in fix #16).

## Import Process

```
 Importing instincts from: team-instincts.yaml
================================================

Found 12 instincts to import.

Analyzing conflicts...

## New Instincts (8)
These will be added:
  ✓ use-zod-validation (confidence: 0.7)
  ✓ prefer-named-exports (confidence: 0.65)
  ✓ test-async-functions (confidence: 0.8)
  ...

## Duplicate Instincts (3)
Already have similar instincts:
  WARNING: prefer-functional-style
     Local: 0.8 confidence, 12 observations
     Import: 0.7 confidence
     → Keep local (higher confidence)

  WARNING: test-first-workflow
     Local: 0.75 confidence
     Import: 0.9 confidence
     → Update to import (higher confidence)

Import 8 new, update 1?
```

## Merge Behavior

When importing an instinct with an existing ID:
- Higher-confidence import becomes an update candidate
- Equal/lower-confidence import is skipped
- User confirms unless `--force` is used

## Source Tracking

Imported instincts are marked with:
```yaml
source: inherited
scope: project
imported_from: "team-instincts.yaml"
project_id: "a1b2c3d4e5f6"
project_name: "my-project"
```

## Flags

- `--dry-run`: Preview without importing
- `--force`: Skip confirmation prompt
- `--min-confidence <n>`: Only import instincts above threshold
- `--scope <project|global>`: Select target scope (default: `project`)

## Output

After import:
```
PASS: Import complete!

Added: 8 instincts
Updated: 1 instinct
Skipped: 3 instincts (equal/higher confidence already exists)

New instincts saved to: ${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/instincts/inherited/

Run /instinct-status to see all instincts.
```
