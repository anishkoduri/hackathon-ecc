#!/usr/bin/env bash
# =============================================================================
# bootstrap.sh — zero → running Supabase backend (macOS)
# -----------------------------------------------------------------------------
# Idempotent: safe to re-run. Installs prerequisites if missing, initializes
# Supabase, starts the local stack, applies migrations + seed, and generates
# TypeScript types.
#
# Usage:  bash skills/app-scaffold/scripts/bootstrap.sh
# =============================================================================
set -euo pipefail

info()  { printf "\033[1;34m▶ %s\033[0m\n" "$1"; }
ok()    { printf "\033[1;32m✓ %s\033[0m\n" "$1"; }
warn()  { printf "\033[1;33m! %s\033[0m\n" "$1"; }

# --- 1. Homebrew -------------------------------------------------------------
if ! command -v brew >/dev/null 2>&1; then
  warn "Homebrew not found. Install it from https://brew.sh then re-run."
  exit 1
fi

# --- 2. Docker Desktop -------------------------------------------------------
if ! command -v docker >/dev/null 2>&1; then
  info "Installing Docker Desktop..."
  brew install --cask docker
  warn "Open Docker Desktop once to finish setup, then re-run this script."
  open -a Docker || true
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  warn "Docker is installed but not running. Launching it..."
  open -a Docker || true
  info "Waiting for Docker to start..."
  until docker info >/dev/null 2>&1; do sleep 2; done
fi
ok "Docker is running"

# --- 3. Supabase CLI ---------------------------------------------------------
# Pinned to 3.1.0 via npx: Homebrew's tap has no version pin, and a global
# npm install is unsupported. npx caches the pinned version after the first
# run, so later calls are fast. Every CLI call in this script goes through
# $SUPABASE, so the pinned version is what actually runs.
if ! command -v npx >/dev/null 2>&1; then
  warn "npx not found. Install Node.js (https://nodejs.org) then re-run."
  exit 1
fi
SUPABASE=(npx supabase@3.1.0)
ok "Supabase CLI: $("${SUPABASE[@]}" --version)"

# --- 4. Initialize Supabase --------------------------------------------------
if [ ! -f "supabase/config.toml" ]; then
  info "Initializing Supabase project..."
  "${SUPABASE[@]}" init
else
  ok "Supabase already initialized"
fi

# --- 5. Start the local stack ------------------------------------------------
info "Starting local Supabase stack (first run pulls images)..."
"${SUPABASE[@]}" start

# --- 6. Apply migrations + seed ----------------------------------------------
info "Resetting database (runs migrations + seed.sql)..."
"${SUPABASE[@]}" db reset

# --- 7. Generate TypeScript types --------------------------------------------
if [ -d "src/lib" ] || [ -d "src" ]; then
  mkdir -p src/lib
  info "Generating TypeScript types..."
  "${SUPABASE[@]}" gen types typescript --local > src/lib/database.types.ts
  ok "Types written to src/lib/database.types.ts"
fi

echo
ok "Done. Run 'npx supabase@3.1.0 status' to see your local URLs and keys."
info "Studio: http://127.0.0.1:54323   API: http://127.0.0.1:54321"
