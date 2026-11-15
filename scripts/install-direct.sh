#!/bin/bash
# Install checksum-pinned official releases not distributed through Homebrew.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${MAC_CLONE_APP_DIR:-/Applications}"
MANIFEST="${MAC_CLONE_DIRECT_MANIFEST:-$ROOT/manifests/direct-selected.tsv}"
install_app() (
  set -euo pipefail
  NAME="$1"; BUNDLE="$2"; VERSION="$3"; TYPE="$4"; URL="$5"; SHA="$6"; ARCH="$7"
  TARGET="$DEST/$NAME.app"
  if [[ -e "$TARGET" || -L "$TARGET" ]]; then
    EXISTING="$(plutil -extract CFBundleIdentifier raw -o - "$TARGET/Contents/Info.plist" 2>/dev/null || true)"
    if [[ "$EXISTING" == "$BUNDLE" ]]; then
      echo "Already installed: $NAME"
      exit 0
    fi
    echo "Cannot install $NAME: another app occupies $TARGET" >&2
    exit 1
  fi
  if [[ "$ARCH" != any && "$(uname -m)" != "$ARCH" ]]; then
    echo "$NAME requires $ARCH; this Mac is $(uname -m)." >&2
    exit 1
  fi
  WORK="$(mktemp -d "${TMPDIR:-/tmp}/mac-clone-app.XXXXXX")"
  MOUNT=''
  cleanup() {
    if [[ -n "$MOUNT" ]]; then hdiutil detach "$MOUNT" -quiet || true; fi
    rm -rf "$WORK"
  }
  trap cleanup EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  if [[ "$TYPE" == ugreen-dmg ]]; then
    # The vendor issues expiring links. Resolve a fresh one for this pinned release.
    curl -fsSL --retry 3 "$URL&_=$(date +%s)" -o "$WORK/link.json"
    URL="$(plutil -extract data.linkData.tempUrl raw -o - "$WORK/link.json")"
    case "$URL" in
      https://dl-us.ugreennas.com/*) ;;
      *) echo 'UGREEN returned no valid official download link. See SOURCES.md.' >&2; exit 1 ;;
    esac
  fi
  echo "Downloading $NAME ${VERSION}..."
  curl -fSL --retry 3 "$URL" -o "$WORK/download"
  ACTUAL="$(shasum -a 256 "$WORK/download")"; ACTUAL="${ACTUAL%% *}"
  if [[ "$ACTUAL" != "$SHA" ]]; then
    echo "Checksum mismatch for $NAME; refusing to install." >&2
    exit 1
  fi
  if [[ "$TYPE" == zip ]]; then
    mkdir "$WORK/unpacked"
    ditto -x -k "$WORK/download" "$WORK/unpacked"
    SOURCE="$WORK/unpacked/$NAME.app"
  else
    mkdir "$WORK/mount"
    hdiutil attach "$WORK/download" -readonly -nobrowse -mountpoint "$WORK/mount" -quiet
    MOUNT="$WORK/mount"
    SOURCE="$MOUNT/$NAME.app"
  fi
  ACTUAL_BUNDLE="$(plutil -extract CFBundleIdentifier raw -o - "$SOURCE/Contents/Info.plist")"
  if [[ "$ACTUAL_BUNDLE" != "$BUNDLE" ]]; then
    echo "Bundle identity mismatch for $NAME; refusing to install." >&2
    exit 1
  fi
  # A staging folder prevents an interrupted copy from looking installed on retry.
  mkdir -p "$DEST"
  if [[ -w "$DEST" ]]; then
    STAGE="$(mktemp -d "$DEST/.mac-clone.XXXXXX")"
    if ! ditto "$SOURCE" "$STAGE/$NAME.app"; then rm -rf "$STAGE"; exit 1; fi
    mv "$STAGE/$NAME.app" "$TARGET"
    rmdir "$STAGE"
  else
    # Copy privately before elevation; credentials stay in the system prompt.
    ditto "$SOURCE" "$WORK/$NAME.app"
    STAGE="$(sudo /usr/bin/mktemp -d "$DEST/.mac-clone.XXXXXX")"
    if ! sudo /usr/bin/ditto "$WORK/$NAME.app" "$STAGE/$NAME.app"; then
      sudo /bin/rm -rf "$STAGE"
      exit 1
    fi
    sudo /bin/mv "$STAGE/$NAME.app" "$TARGET"
    sudo /bin/rmdir "$STAGE"
  fi
  echo "Installed: $NAME"
)
STATUS=0
while IFS=$'\t' read -r NAME BUNDLE VERSION TYPE URL SHA ARCH <&3; do
  [[ -z "$NAME" || "$NAME" == \#* ]] && continue
  # Run each app independently so one unavailable download does not skip the rest.
  # Do not put the function in an if/! context (that would disable errexit inside).
  set +e
  install_app "$NAME" "$BUNDLE" "$VERSION" "$TYPE" "$URL" "$SHA" "$ARCH"
  RESULT=$?
  set -e
  if [[ "$RESULT" -ne 0 ]]; then
    echo "FAILED: $NAME (rerun after resolving the error above)." >&2
    STATUS=1
  fi
done 3< "$MANIFEST"
exit "$STATUS"
