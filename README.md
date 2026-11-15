# My next Mac

A local repository for choosing and documenting a repeatable Mac setup.

Your checked choices in [CHECKLIST.md](CHECKLIST.md) are prepared for installation. The full original inventory remains for reference; unchecked software is excluded from the install plan.

## Use on a new Mac

Tell your coding assistant:

> Set up this Mac using this repository. Read AGENTS.md and install my selected software. Complete the Homebrew installs, help with each manual app, and report anything that still requires my sign-in, license, or a confirmed download source. Do not install unchecked inventory items.

Clone the repository on the new Mac, then point the assistant at that checkout. A private GitHub repository requires signing in first.

`Brewfile.selected` installs the verified Homebrew selections with `bash scripts/install.sh`. `MANUAL-INSTALL.md` preserves every selected app that needs a separate installer or App Store purchase. The repository contains manifests and instructions, not app binaries or licenses. Package versions are resolved at installation time.

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
- `scripts/install.sh`: install selected Homebrew packages.
- `scripts/scan.py`: refresh installation metadata without changing your checklist.

## Refresh inventory

With Python 3 available, run from this directory:

```sh
python3 scripts/scan.py
```

The scanner uses local installation metadata. It does not open personal documents, shell histories, browser profiles, config contents, SSH files, or credential stores. Some app names and extension names can still be private; inspect the repo before publishing it. Missing commands or unreadable locations may be omitted. This is not a complete backup, a system security audit, or an exhaustive inventory of Apple system apps, nested runtimes, Python/Ruby packages, browser extensions, app plugins, and system extensions.

The GitHub remote, once configured, is shown by `git remote -v`. Keep this repository private unless you deliberately choose otherwise.
