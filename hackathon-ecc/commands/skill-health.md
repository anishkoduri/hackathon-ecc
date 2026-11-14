---
name: skill-health
description: Show skill portfolio health dashboard with charts and analytics. Use for the quantitative usage/success-rate dashboard; for a qualitative compliance or quality audit use the skill-stocktake skill.
command: true
---

# Skill Health Dashboard

Shows a comprehensive health dashboard for all skills in the portfolio with success rate sparklines, failure pattern clustering, pending amendments, and version history.

## Implementation

Run the skill health CLI in dashboard mode:

```bash
ECC_ROOT="$(node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)")" &&
node "$ECC_ROOT/scripts/skills-health.js" --dashboard
```

For a specific panel only:

```bash
ECC_ROOT="$(node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)")" &&
node "$ECC_ROOT/scripts/skills-health.js" --dashboard --panel failures
```

For machine-readable output:

```bash
ECC_ROOT="$(node -e "var r=(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})();console.log(r)")" &&
node "$ECC_ROOT/scripts/skills-health.js" --dashboard --json
```

## Usage

```
/skill-health                    # Full dashboard view
/skill-health --panel failures   # Only failure clustering panel
/skill-health --json             # Machine-readable JSON output
```

## What to Do

1. Run the skills-health.js script with --dashboard flag
2. Display the output to the user
3. If any skills are declining, highlight them and suggest running /evolve
4. If there are pending amendments, suggest reviewing them

## Panels

- **Success Rate (30d)** — Sparkline charts showing daily success rates per skill
- **Failure Patterns** — Clustered failure reasons with horizontal bar chart
- **Pending Amendments** — Amendment proposals awaiting review
- **Version History** — Timeline of version snapshots per skill

## Snapshot storage

Snapshot creation and rollback require writable storage with hardlink support. The versioning API checks that capability before creating or changing version history and refuses unsupported storage without a copy fallback. Use a hardlink-capable location for new snapshots. Reading existing health and version history does not require creating hard links.
