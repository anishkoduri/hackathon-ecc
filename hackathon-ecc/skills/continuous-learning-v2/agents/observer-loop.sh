#!/usr/bin/env bash
# Continuous Learning v2 - Observer background loop
#
# Fix for #521: Added re-entrancy guard, cooldown throttle, and
# tail-based sampling to prevent memory explosion from runaway
# parallel analysis processes.

set +e
SLEEP_PID=""
ACTIVE_ANALYSIS_FILE=""
ACTIVE_PROMPT_FILE=""
ACTIVE_RESULT_FILE=""
RESULT_FDS_OPEN=0
USR1_FIRED=0
PENDING_ANALYSIS=0
ANALYZING=0
LAST_ANALYSIS_EPOCH=0
# Minimum seconds between analyses (prevents rapid re-triggering)
ANALYSIS_COOLDOWN="${ECC_OBSERVER_ANALYSIS_COOLDOWN:-60}"
IDLE_TIMEOUT_SECONDS="${ECC_OBSERVER_IDLE_TIMEOUT_SECONDS:-1800}"
SESSION_LEASE_DIR="${PROJECT_DIR}/.observer-sessions"
ACTIVITY_FILE="${PROJECT_DIR}/.observer-last-activity"

# Resolve this script's own directory so relative helpers
# (../scripts/instinct-cli.py) resolve correctly whether
# this file is executed or sourced. $0 is the *caller* when sourced, so prefer
# ${BASH_SOURCE[0]}, which always points at this file (#2370).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"




cleanup_analysis_resources() {

  if [ "$RESULT_FDS_OPEN" -eq 1 ]; then
    { exec 8>&-; } 2>/dev/null || true
    if [ -n "${LOG_FILE:-}" ]; then
      cat <&9 >> "$LOG_FILE" 2>/dev/null || true
    fi
    { exec 7<&-; } 2>/dev/null || true
    { exec 9<&-; } 2>/dev/null || true
    RESULT_FDS_OPEN=0
  fi
  [ -n "$ACTIVE_ANALYSIS_FILE" ] && rm -f "$ACTIVE_ANALYSIS_FILE"
  [ -n "$ACTIVE_PROMPT_FILE" ] && rm -f "$ACTIVE_PROMPT_FILE"
  [ -n "$ACTIVE_RESULT_FILE" ] && rm -f "$ACTIVE_RESULT_FILE"
  ACTIVE_ANALYSIS_FILE=""
  ACTIVE_PROMPT_FILE=""
  ACTIVE_RESULT_FILE=""
}

cleanup() {
  cleanup_analysis_resources
  [ -n "$SLEEP_PID" ] && kill "$SLEEP_PID" 2>/dev/null
  if [ -f "$PID_FILE" ] && [ "$(cat "$PID_FILE" 2>/dev/null)" = "$$" ]; then
    rm -f "$PID_FILE"
  fi
  exit 0
}
trap cleanup TERM INT

file_mtime_epoch() {
  local file="$1"
  if [ ! -f "$file" ]; then
    printf '0\n'
    return
  fi

  if stat -c %Y "$file" >/dev/null 2>&1; then
    stat -c %Y "$file" 2>/dev/null || printf '0\n'
    return
  fi

  if stat -f %m "$file" >/dev/null 2>&1; then
    stat -f %m "$file" 2>/dev/null || printf '0\n'
    return
  fi

  printf '0\n'
}

has_active_session_leases() {
  if [ ! -d "$SESSION_LEASE_DIR" ]; then
    return 1
  fi

  find "$SESSION_LEASE_DIR" -type f -name '*.json' -print -quit 2>/dev/null | grep -q .
}

latest_activity_epoch() {
  local observations_epoch activity_epoch
  observations_epoch="$(file_mtime_epoch "$OBSERVATIONS_FILE")"
  activity_epoch="$(file_mtime_epoch "$ACTIVITY_FILE")"

  if [ "$activity_epoch" -gt "$observations_epoch" ] 2>/dev/null; then
    printf '%s\n' "$activity_epoch"
  else
    printf '%s\n' "$observations_epoch"
  fi
}

exit_if_idle_without_sessions() {
  if has_active_session_leases; then
    return
  fi

  local last_activity now_epoch idle_for
  last_activity="$(latest_activity_epoch)"
  now_epoch="$(date +%s)"
  idle_for=$(( now_epoch - last_activity ))

  if [ "$last_activity" -eq 0 ] || [ "$idle_for" -ge "$IDLE_TIMEOUT_SECONDS" ]; then
    echo "[$(date)] Observer idle without active session leases for ${idle_for}s; exiting" >> "$LOG_FILE"
    cleanup
  fi
}


analyze_observations() {
  # Background analysis was removed in fix #16: it spawned the
  # a CLI subprocess, which has no Cursor equivalent. Observations are
  # retained (not archived) and the loop keeps its guards, cooldown,
  # and instinct pruning. No reimplementation on Cursor subagents.
  echo "[$(date)] Background analysis disabled (fix #16): observations retained, not analyzed" >> "$LOG_FILE"
}

on_usr1() {
  [ -n "$SLEEP_PID" ] && kill "$SLEEP_PID" 2>/dev/null
  SLEEP_PID=""

  # Re-entrancy guard: defer the nudge so the main loop runs a follow-up
  # analysis immediately after the current analysis finishes.
  if [ "$ANALYZING" -eq 1 ]; then
    PENDING_ANALYSIS=1
    echo "[$(date)] Analysis already in progress, deferring signal" >> "$LOG_FILE"
    return
  fi

  USR1_FIRED=1

  # Cooldown: skip if last analysis was too recent (#521)
  now_epoch=$(date +%s)
  elapsed=$(( now_epoch - LAST_ANALYSIS_EPOCH ))
  if [ "$elapsed" -lt "$ANALYSIS_COOLDOWN" ]; then
    echo "[$(date)] Analysis cooldown active (${elapsed}s < ${ANALYSIS_COOLDOWN}s), skipping" >> "$LOG_FILE"
    return
  fi

  ANALYZING=1
  analyze_observations
  LAST_ANALYSIS_EPOCH=$(date +%s)
  ANALYZING=0
}
trap on_usr1 USR1

# When this file is sourced (e.g. by a caller sourcing it to reuse its
# functions) rather than executed, stop here so callers can invoke individual
# functions such as analyze_observations without starting the observer loop. The only
# production caller (start-observer.sh) executes the script, so $0 equals
# BASH_SOURCE[0] there and this guard is a no-op (#2370).
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
  return 0 2>/dev/null || true
fi

echo "$$" > "$PID_FILE"
echo "[$(date)] Observer started for ${PROJECT_NAME} (PID: $$)" >> "$LOG_FILE"

# Prune expired pending instincts before analysis (SCRIPT_DIR resolved at top
# via ${BASH_SOURCE[0]} so it is correct under both execution and sourcing).
"${CLV2_PYTHON_CMD:-python3}" "${SCRIPT_DIR}/../scripts/instinct-cli.py" prune --quiet >> "$LOG_FILE" 2>&1 || echo "[$(date)] Warning: instinct prune failed (non-fatal)" >> "$LOG_FILE"

while true; do
  exit_if_idle_without_sessions

  if [ "$PENDING_ANALYSIS" -eq 1 ]; then
    PENDING_ANALYSIS=0
    USR1_FIRED=0
    ANALYZING=1
    analyze_observations
    LAST_ANALYSIS_EPOCH=$(date +%s)
    ANALYZING=0
    continue
  fi

  sleep "$OBSERVER_INTERVAL_SECONDS" &
  SLEEP_PID=$!
  wait "$SLEEP_PID" 2>/dev/null
  SLEEP_PID=""

  exit_if_idle_without_sessions
  if [ "$USR1_FIRED" -eq 1 ]; then
    USR1_FIRED=0
  else
    ANALYZING=1
    analyze_observations
    LAST_ANALYSIS_EPOCH=$(date +%s)
    ANALYZING=0
  fi
done
