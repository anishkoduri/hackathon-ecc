---
name: projects
description: List known projects and their instinct statistics
command: true
---

# Projects Command

List project registry entries and per-project instinct/observation counts for continuous-learning-v2.

## Implementation

Run the instinct CLI using the plugin root path:

```bash
ECC_ROOT="$(node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)")" &&
python3 "$ECC_ROOT/skills/continuous-learning-v2/scripts/instinct-cli.py" projects
```

Or, relative to the plugin root (manual installation, `ECC_PLUGIN_ROOT` not set):

```bash
python3 skills/continuous-learning-v2/scripts/instinct-cli.py projects
```

## Usage

```bash
/projects
```

## What to Do

1. Read `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/projects.json`

   Legacy homunculus data is not read (the migration script was removed in fix #16).
2. For each project, display:
   - Project name, id, root, remote
   - Personal and inherited instinct counts
   - Observation event count
   - Last seen timestamp
3. Also display global instinct totals
