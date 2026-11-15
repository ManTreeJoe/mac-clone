#!/bin/bash
# Install only the explicitly selected Homebrew packages.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if ! command -v brew >/dev/null 2>&1; then
  echo 'Homebrew is required. Install it using https://brew.sh, then rerun this script.'
  exit 1
fi
brew bundle --file="$ROOT/Brewfile.selected"
echo 'Homebrew selections installed. Continue with MANUAL-INSTALL.md.'
