# My next Mac

A local repository for choosing and documenting a repeatable Mac setup.

Start with [CHECKLIST.md](CHECKLIST.md). Check the things you want on a new Mac and add notes at the bottom. Nothing is selected yet, and there is no installer that changes your Mac.

The scan was taken November 14, 2026 on an Apple Silicon Mac running macOS 26.5.1. It records installed software, configuration locations, font filenames, user launch-agent filenames, and a small allowlist of macOS preferences. The inventory is a snapshot of what is present, not proof of what is used or essential.

## Files

- `CHECKLIST.md`: editable selections and manual migration reminders.
- `inventory/machine.json`: detailed installation metadata, including all Homebrew dependencies and font filenames.
- `scripts/scan.py`: read-only local rescan; writes only `inventory/machine.json` and preserves your checklist choices.
- `Brewfile.selected`: empty starting point for the packages you eventually choose.

## Choose, then build the setup

1. Check wanted items in `CHECKLIST.md`. Avoid duplicates between applications and Homebrew casks.
2. Put selected Homebrew identifiers in `Brewfile.selected` using the commented examples there. Prefer top-level tools; Homebrew installs their dependencies.
3. Review each selected configuration locally. Remove credentials, account identifiers, private URLs, and machine-specific paths before deliberately adding sanitized files to this repo.
4. Keep accounts, passwords, SSH private keys, licenses, personal files, databases, and virtual machines in a separate private/encrypted migration process.
5. On the new Mac, install Homebrew from its official instructions, clone this repository, inspect the selected Brewfile, and run `brew bundle --file=Brewfile.selected` when ready. Homebrew resolves current versions; this is not a version-locked clone.
6. Restore selected sanitized settings and complete the manual checklist. Verify the result before retiring the old Mac.

## Refresh inventory

With Python 3 available, run from this directory:

```sh
python3 scripts/scan.py
```

The scanner uses local installation metadata. It does not open personal documents, shell histories, browser profiles, config contents, SSH files, or credential stores. Some app names and extension names can still be private; inspect the repo before publishing it. Missing commands or unreadable locations may be omitted. This is not a complete backup, a system security audit, or an exhaustive inventory of Apple system apps, nested runtimes, Python/Ruby packages, browser extensions, app plugins, and system extensions.

This repo is local only. No GitHub repository has been created or uploaded.
