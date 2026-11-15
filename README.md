# My next Mac

A local repository for choosing and documenting a repeatable Mac setup.

Your checked choices in [CHECKLIST.md](CHECKLIST.md) are prepared for installation. The full original inventory remains for reference; unchecked software is excluded from the install plan.

## One command on a new Mac

Open Terminal and paste:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/ManTreeJoe/mac-clone/master/bootstrap.sh)"
```

The bootstrap downloads this public repo, installs Homebrew and required Apple command-line tools if missing, and installs your selected Homebrew apps and Git tools. It adds Homebrew to `~/.zprofile` without replacing your existing settings. It saves each setup snapshot under `~/Library/Application Support/mac-clone/` and prints the remaining manual tasks. Run as your normal account; respond to macOS password, installer, and permission prompts when requested.

You can rerun the same command after a failure. Already installed Homebrew packages are retained without upgrading them, and unrelated apps are not removed. An existing app installed outside Homebrew can require manual resolution if Homebrew reports a conflict.

### What still needs you

This command installs the automated selections, including Notchy through the developer’s documented Homebrew tap. Seven selected apps still need a verified installer or purchase history: Ardia, ArtCraft Launcher, Card Hopper, Grok Bot, Isocast, Magnet, and UGREEN NAS. See [MANUAL-INSTALL.md](MANUAL-INSTALL.md). Those are not reported as automatically installed.

Account sign-ins, purchased licenses, permissions, browser sync, backups, and FileVault still require your involvement. Shell preferences, font, and editor were selected as broad goals, but no specific settings files, font, editor, or extensions were individually chosen. No app binaries, private settings, or credentials are in this repo.

The `codex` selection installs the Codex CLI, not the desktop app. Versions are resolved at installation time.

If using a coding assistant, give it this repo URL and ask it to read `AGENTS.md`, run the bootstrap, and help complete every remaining manual step.

Sources: [Homebrew installation](https://brew.sh/), [Notchy developer’s Homebrew instructions](https://notchy.dev/help/install-with-homebrew/).

## Updating your choices

Edit the checkboxes in `CHECKLIST.md`, run `python3 scripts/prepare.py`, review the generated files, and commit/push the changes. Do not run the installer on the old Mac just to publish this repo.

## Files

- `CHECKLIST.md`: your choices.
- `Brewfile.selected`: selected automated installs.
- `MANUAL-INSTALL.md`: selected apps and setup tasks requiring extra steps.
- `AGENTS.md`: instructions for the assistant setting up the next Mac.
- `inventory/selected.json`: machine-readable choices.
- `inventory/machine.json`: original software and settings-location inventory.
- `inventory/install-sources.json`: checked Homebrew cask metadata from https://formulae.brew.sh/api/.
- `scripts/prepare.py`: regenerate the plan without installing.
- `bootstrap.sh`: fresh-Mac entry point; installs prerequisites and runs the installer.
- `scripts/install.sh`: install selected Homebrew packages.
- `scripts/scan.py`: refresh installation metadata without changing your checklist.

## Refresh inventory

With Python 3 available, run from this directory:

```sh
python3 scripts/scan.py
```

The scanner uses local installation metadata. It does not open personal documents, shell histories, browser profiles, config contents, SSH files, or credential stores. Some app names and extension names can still be private; inspect the repo before publishing it. Missing commands or unreadable locations may be omitted. This is not a complete backup, a system security audit, or an exhaustive inventory of Apple system apps, nested runtimes, Python/Ruby packages, browser extensions, app plugins, and system extensions.

This repository is public by the owner’s choice. Do not commit credentials or private configuration contents.
