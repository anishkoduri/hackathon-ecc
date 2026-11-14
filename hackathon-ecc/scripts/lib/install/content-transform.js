'use strict';

// fix #16 (D10/D14): the installer is Cursor-only. All host-specific content
// transforms (Cursor manual-plugin namespace, Qwen/Antigravity/Copilot
// frontmatter, OpenCode hook disabling) are removed with their host adapters.
// No Cursor plan names a transform, so this is a passthrough that fails
// loudly on any named transform instead of silently passing it through.
function transformInstallContent(operation, content) {
  if (!operation.contentTransform) {
    return content;
  }
  throw new Error(`Unknown install content transform: ${operation.contentTransform}`);
}

module.exports = { transformInstallContent };
