#!/bin/bash
# Diagnostic-only wrapper (dry-run #37 rerun2): launch the real
# chrome-headless-shell with the sandbox egress proxy so Chrome can reach
# fonts.gstatic.com. Reads the proxy from the environment at run time;
# no credential is written in this file. Used ONLY for the still-render
# diagnostic probe; the as-shipped qa.mjs run does not use it.
exec "/home/hatch/workspace/hackathon-plugin/fix22/dryrun37-rerun2/demo-sample-video/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell" --proxy-server="$https_proxy" --ignore-certificate-errors "$@"
