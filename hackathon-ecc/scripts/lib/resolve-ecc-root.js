'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');


const CURRENT_PLUGIN_SLUG = 'ecc';
const CURRENT_PLUGIN_HANDLE = `${CURRENT_PLUGIN_SLUG}@${CURRENT_PLUGIN_SLUG}`;
const PLUGIN_ROOT_SEGMENTS = [
  [CURRENT_PLUGIN_SLUG],
  [CURRENT_PLUGIN_HANDLE],
  ['marketplaces', CURRENT_PLUGIN_SLUG],
];

// Artifacts that identify a COMPLETE ECC root when the caller gives no explicit
// probe. A real ECC root ships both the script tree AND ECC's skills; a partial
// install (scripts copied, skills not) must not qualify for skill-resolving
// callers, which build `skills/...` paths against the resolved root (#2544).
// Checking "skills/ exists" is not enough — a user's own agent data directory's skills/ can
// be present with none of ECC's skills — so we probe for a sentinel skill that
// ships in every ECC root and is exactly what the failing skill commands need.
// If that skill is ever renamed, move this sentinel with it.
const DEFAULT_SCRIPT_PROBE = path.join('scripts', 'lib', 'utils.js');
const DEFAULT_SKILL_PROBE = path.join('skills', 'continuous-learning-v2');

/**
 * Resolve the ECC source root directory.
 *
 * Tries, in order:
 *   1. ECC_PLUGIN_ROOT env var (set by the host for hooks, or by user)
 *   2. Cursor plugin install — scans ~/.cursor/plugins/ (local install
 *      first, then any two-level marketplace layout) for a directory
 *      passing the resolver's probe
 *   3. Host-agnostic fallback — the plugin root relative to this file
 *      (this module lives at <plugin-root>/scripts/lib/resolve-ecc-root.js,
 *      so two levels up is the plugin root)
 *
 * @param {object} [options]
 * @param {string} [options.homeDir]  Override home directory (for testing)
 * @param {string} [options.envRoot]  Override ECC_PLUGIN_ROOT (for testing)
 * @param {string} [options.probe]    Relative path used to verify a candidate
 *                                    root contains what the caller needs. When
 *                                    given, it is honored exactly (script
 *                                    consumers pass their own script path). When
 *                                    omitted, a candidate must contain BOTH the
 *                                    ECC script tree and a sentinel ECC skill,
 *                                    so a partial install (scripts without
 *                                    skills) is rejected for skill consumers.
 * @returns {string} Resolved ECC root path
 */
function resolveEccRoot(options = {}) {
  const envRoot = options.envRoot !== undefined
    ? options.envRoot
    : (process.env.ECC_PLUGIN_ROOT || '');

  if (envRoot && envRoot.trim()) {
    return envRoot.trim();
  }

  const homeDir = options.homeDir || os.homedir();

  // Decide whether a candidate directory is a usable ECC root. An explicit
  // caller probe is honored exactly (script consumers know the artifact they
  // need). With the default probe the caller is a skill consumer, so a
  // candidate must contain both ECC's scripts and a sentinel ECC skill —
  // otherwise a scripts-only agent-data short-circuits and every skill path
  // resolves to a location that does not exist (#2544).
  const isRoot = options.probe
    ? (dir) => fs.existsSync(path.join(dir, options.probe))
    : (dir) => fs.existsSync(path.join(dir, DEFAULT_SCRIPT_PROBE))
            && fs.existsSync(path.join(dir, DEFAULT_SKILL_PROBE));


  // Cursor plugin install (Audit #8): mirror the ~/.cursor/plugins scan
  // from buildInlineResolve() here, so direct JS callers of
  // resolveEccRoot() find a Cursor install too. Local install first,
  // then any two-level marketplace layout. Candidates are validated
  // with the same probe as every other candidate.
  const cursorPluginsDir = path.join(homeDir, '.cursor', 'plugins');
  const localCursorRoot = path.join(cursorPluginsDir, 'local', 'hackathon-ecc');
  if (isRoot(localCursorRoot)) {
    return localCursorRoot;
  }
  for (const topEntry of directories(cursorPluginsDir)) {
    if (!topEntry.isDirectory()) continue;
    const topPath = path.join(cursorPluginsDir, topEntry.name);
    for (const subEntry of directories(topPath)) {
      if (!subEntry.isDirectory()) continue;
      const candidate = path.join(topPath, subEntry.name);
      if (isRoot(candidate)) {
        return candidate;
      }
    }
  }

  // Host-agnostic fallback (Audit #4): this module lives at
  // <plugin-root>/scripts/lib/resolve-ecc-root.js in every host, so the
  // plugin root is two levels up from __dirname. In a Cursor install there
  // is no agent data home and no ECC_PLUGIN_ROOT, so all the probing above
  // fails; resolving relative to this file still finds the plugin. The
  // candidate is validated with the same probe as every other candidate,
  // so a bare scripts-only copy does not qualify.
  const selfRoot = path.resolve(__dirname, '..', '..');
  if (isRoot(selfRoot)) {
    return selfRoot;
  }

  return selfRoot;
}

function normalizePluginRootForPlatform(rootDir, platform = process.platform) {
  if (platform !== 'win32' || typeof rootDir !== 'string') return rootDir;

  const match = rootDir.match(/^\/([a-zA-Z])(?:\/(.*))?$/);
  if (!match) return rootDir;

  const [, driveLetter, rest = ''] = match;
  return `${driveLetter.toUpperCase()}:/${rest}`;
}

/**
 * Compact inline locator for embedding in hooks.json and command .md code blocks.
 *
 * This minified form contains no spread, no nested array literals, and no
 * escaped double quotes, so it survives `node -e "..."` quoting on every shell.
 * When ECC_PLUGIN_ROOT is set (as the host does for plugin hooks and
 * commands) it is used directly. Otherwise the inline scans
 * ~/.cursor/plugins (local install first, then any two-level marketplace
 * layout) for a directory passing the resolver's probe, so it finds the
 * plugin in a Cursor install. Only then does it fall back to the local
 * install path. The inline runs under `node -e` with no __dirname, so it
 * cannot use the selfRoot fallback in resolveEccRoot() directly.
 *
 * Usage in commands:
 *   const _r = <paste INLINE_RESOLVE>;
 *   const sm = require(_r + '/scripts/lib/session-manager');
 */

function buildInlineResolve(options = {}) {
  let probeArg = '';
  if (options && options.probe) {
    const segments = String(options.probe).split(/[\\/]/).filter(Boolean);
    for (const seg of segments) {
      if (!/^[\w.-]+$/.test(seg)) {
        throw new Error(`Invalid probe segment: ${seg}`);
      }
    }
    probeArg = `{probe:p.join(${segments.map((s) => `'${s}'`).join(',')})}`;
  }
  // Cursor-only: the inline runs under `node -e` with no __dirname, so it
  // cannot use the selfRoot fallback in resolveEccRoot() directly; instead
  // it scans ~/.cursor/plugins (the documented local install at
  // plugins/local/hackathon-ecc first, then any two-level marketplace
  // layout) for a directory passing the same probe the shared resolver
  // uses. L() delegates to the shared resolver when a candidate loads.
  return `(function(){var p=require('path'),f=require('fs'),o=require('os');var e=process.env.ECC_PLUGIN_ROOT;if(e&&e.trim())return e.trim();function L(x){try{return require(p.join(x,'scripts','lib','resolve-ecc-root')).resolveEccRoot()}catch(_){return null}}function D(x){try{return f.readdirSync(x,{withFileTypes:true}).filter(function(z){return z.isDirectory()}).map(function(z){return z.name})}catch(e){if(e.code==='ENOENT')return [];throw e}}var h=o.homedir();var cp=p.join(h,'.cursor','plugins');var q=p.join(cp,'local','hackathon-ecc');var r=L(q);if(r)return r;var A=D(cp);for(var a=0;a<A.length;a++){var B=D(p.join(cp,A[a]));for(var b=0;b<B.length;b++){r=L(p.join(cp,A[a],B[b]));if(r)return r}}return q})()`;
}

const INLINE_RESOLVE = buildInlineResolve();

module.exports = {
  resolveEccRoot,
  normalizePluginRootForPlatform,
  INLINE_RESOLVE,
  buildInlineResolve,
};
