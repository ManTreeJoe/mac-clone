# My next Mac

A local repository for choosing and documenting a repeatable Mac setup.

Your checked choices in [CHECKLIST.md](CHECKLIST.md) are prepared for installation. The full original inventory remains for reference; unchecked software is excluded from the install plan.

## One command on a new Mac

Open Terminal and paste:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/ManTreeJoe/mac-clone/master/bootstrap.sh)"
```

The bootstrap downloads this public repo, installs Homebrew and required Apple command-line tools if missing, and installs your selected Homebrew apps, Git tools, direct developer downloads, and Magnet through the Mac App Store. It adds Homebrew to `~/.zprofile` without replacing your existing settings. It saves each setup snapshot under `~/Library/Application Support/mac-clone/` and prints the remaining manual tasks. Run as your normal account; respond to macOS password, installer, and permission prompts when requested.

You can rerun the same command after a failure. Already installed Homebrew packages are retained without upgrading them, and unrelated apps are not removed. An existing app installed outside Homebrew can require manual resolution if Homebrew reports a conflict.

### All selected apps are included

The installer covers all 18 selected app bundles, plus the selected Codex CLI and Git tools. Ardia, ArtCraft Launcher, and Grok Bot use Homebrew. Card Hopper, Isocast, and UGREEN NAS use official, version-pinned downloads with SHA-256 and bundle-ID checks. Magnet uses the Mac App Store through `mas` (installed as a helper). See [SOURCES.md](SOURCES.md) for every source.

This setup requires **Apple silicon and macOS 14 or later**. Card Hopper and Isocast currently publish Apple-silicon builds; the bootstrap refuses incompatible Macs before installing.

**Before running, sign into the Mac App Store with the Apple Account that owns Magnet.** If you do not own it, purchase it in the App Store first. Setup attempts its installation but does not purchase paid apps. A missing purchase, sign-in, or failed download produces an error; rerun the same command once resolved.

### What still needs you

Respond to admin and installer prompts. Complete app sign-ins, license activation, first-launch permissions, browser sync, backups, and FileVault. Isocast can request a codec download on first launch. The script lists these tasks at the end.

Specific shell settings, fonts, editor apps, and extensions were not individually selected and are not added. No app binaries, private settings, or credentials are stored here. `codex` installs the CLI, not the desktop app.

Homebrew resolves current package versions. Direct downloads are pinned in `manifests/direct-apps.json`; changing their versions requires checking the official release, checksum, app layout, and bundle ID again. UGREEN's pinned official API record supplies a fresh expiring CDN link on each run. Existing direct-installed apps with the expected bundle ID are kept unchanged. Unavailable releases or mismatched downloads stop that app and produce a failure rather than silently substituting another source.

If using a coding assistant, give it this repo URL and ask it to read `AGENTS.md`, run the bootstrap, and help complete account and first-launch steps.

## Updating your choices

Edit the checkboxes in `CHECKLIST.md`, run `python3 scripts/prepare.py`, review the generated files, and commit/push the changes. Do not run the installer on the old Mac just to publish this repo.

## Files

- `CHECKLIST.md`: your choices.
- `Brewfile.selected`: selected automated installs.
- `MANUAL-INSTALL.md`: account and first-launch tasks.
- `SOURCES.md`: official downloads and installation routes.
- `manifests/direct-apps.json`: pinned developer releases.
- `manifests/direct-selected.tsv`: generated direct-download selections.
- `AGENTS.md`: instructions for the assistant setting up the next Mac.
- `inventory/selected.json`: machine-readable choices.
- `inventory/machine.json`: original software and settings-location inventory.
- `inventory/install-sources.json`: checked Homebrew cask metadata from https://formulae.brew.sh/api/.
- `scripts/prepare.py`: regenerate the plan without installing.
- `bootstrap.sh`: fresh-Mac entry point; installs prerequisites and runs the installer.
- `scripts/install.sh`: run Homebrew, Mac App Store, and direct installs.
- `scripts/install-direct.sh`: verify and install direct developer downloads.
- `scripts/scan.py`: refresh installation metadata without changing your checklist.

## Refresh inventory

With Python 3 available, run from this directory:

```sh
python3 scripts/scan.py
```

The scanner uses local installation metadata. It does not open personal documents, shell histories, browser profiles, config contents, SSH files, or credential stores. Some app names and extension names can still be private; inspect the repo before publishing it. Missing commands or unreadable locations may be omitted. This is not a complete backup, a system security audit, or an exhaustive inventory of Apple system apps, nested runtimes, Python/Ruby packages, browser extensions, app plugins, and system extensions.

This repository is public by the owner’s choice. Do not commit credentials or private configuration contents.
