#!/bin/bash
# One-command entry point. Requires only tools included with macOS.
set -euo pipefail
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'This setup is for macOS only.' >&2
  exit 1
fi
if [[ "$EUID" -eq 0 ]]; then
  echo 'Run as your normal Mac account, without sudo.' >&2
  exit 1
fi
# The selected Ardia, Card Hopper, and Isocast builds require Apple silicon.
if [[ "$(uname -m)" != arm64 || "$(sw_vers -productVersion | cut -d. -f1)" -lt 14 ]]; then
  echo 'This selected setup requires Apple silicon and macOS 14 or later.' >&2
  exit 1
fi
WORK="$(mktemp -d "${TMPDIR:-/tmp}/mac-clone.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Fetch a complete snapshot so the Brewfile and installer always agree.
echo 'Downloading your selected Mac setup…'
curl --fail --show-error --silent --location --retry 3 \
  https://codeload.github.com/ManTreeJoe/mac-clone/tar.gz/refs/heads/master \
  --output "$WORK/setup.tar.gz"
mkdir "$WORK/source"
tar -xzf "$WORK/setup.tar.gz" -C "$WORK/source" --strip-components=1
# Preserve each run for troubleshooting and the remaining manual steps.
SETUP_BASE="$HOME/Library/Application Support/mac-clone"
mkdir -p "$SETUP_BASE"
SETUP_DIR="$(mktemp -d "$SETUP_BASE/setup.XXXXXX")"
cp -R "$WORK/source/." "$SETUP_DIR/"
echo "Setup files saved to: $SETUP_DIR"

# The official Homebrew installer handles Command Line Tools on a fresh Mac.
# Do not suppress its password prompt or confirmation.
BREW=''
if [[ -x /opt/homebrew/bin/brew ]]; then
  BREW=/opt/homebrew/bin/brew
elif [[ -x /usr/local/bin/brew ]]; then
  BREW=/usr/local/bin/brew
elif command -v brew >/dev/null 2>&1; then
  BREW="$(command -v brew)"
fi
if [[ -z "$BREW" ]]; then
  echo 'Installing Homebrew and required Apple developer tools…'
  curl --fail --show-error --silent --location --retry 3 \
    https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh \
    --output "$WORK/homebrew-install.sh"
  /bin/bash "$WORK/homebrew-install.sh"
  if [[ -x /opt/homebrew/bin/brew ]]; then
    BREW=/opt/homebrew/bin/brew
  elif [[ -x /usr/local/bin/brew ]]; then
    BREW=/usr/local/bin/brew
  else
    echo 'Homebrew did not finish. Resolve the message above and rerun the command.' >&2
    exit 1
  fi
fi
eval "$("$BREW" shellenv)"
# Make brew discoverable in future zsh sessions without replacing existing settings.
BREW_INIT="eval \"\$(\"$BREW\" shellenv)\""
if ! /usr/bin/grep -Fqx "$BREW_INIT" "$HOME/.zprofile" 2>/dev/null; then
  printf '\n# Homebrew (mac-clone setup)\n%s\n' "$BREW_INIT" >> "$HOME/.zprofile"
fi
/bin/bash "$SETUP_DIR/scripts/install.sh"
