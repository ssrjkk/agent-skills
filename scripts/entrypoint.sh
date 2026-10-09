#!/bin/sh
set -e

COMMAND="${1:-validate}"
shift 2>/dev/null || true

case "$COMMAND" in
  validate|quality|catalog|stats)
    python -m claude_skills.cli "$COMMAND" "$@"
    ;;
  *)
    echo "Usage: validate|quality|catalog|stats [options]"
    exit 1
    ;;
esac