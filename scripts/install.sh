#!/bin/bash
# Install only the explicitly selected Homebrew packages.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v brew >/dev/null 2>&1; then
  echo 'Homebrew is required. Use the one-command bootstrap in README.md.' >&2
  exit 1
fi
STATUS=0
# Do not upgrade already-installed packages or remove unrelated software.
if ! brew bundle --no-upgrade --file="$ROOT/Brewfile.selected"; then
  STATUS=1
  echo 'Some automatic installs failed. Review the errors above, then rerun to retry.' >&2
fi
if ! /bin/bash "$ROOT/scripts/install-direct.sh"; then
  STATUS=1
fi
printf '\nAccount and first-launch setup:\n\n'
cat "$ROOT/MANUAL-INSTALL.md"
printf '\nSaved instructions: %s/MANUAL-INSTALL.md\n' "$ROOT"
if [[ "$STATUS" -eq 0 ]]; then
  echo 'All selected app installation steps finished. Complete the account and first-launch tasks above.'
fi
exit "$STATUS"
