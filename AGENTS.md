# New Mac installation instructions

The owner has chosen software in CHECKLIST.md. Checked boxes are the selection authority. Do not install unchecked items from the full inventory.

1. Read README.md, CHECKLIST.md, Brewfile.selected, and MANUAL-INSTALL.md.
2. This is an installation request for a new Mac only when the owner asks to set up that Mac. Do not install packages merely when editing this repo.
3. On an authorized target Mac, check for Xcode command-line tools and Homebrew. If absent, use their official installation instructions. Let the owner handle admin dialogs and account sign-ins.
4. Run `bash bootstrap.sh` for a fresh-Mac setup, or `bash scripts/install.sh` when Homebrew is already available. Do not use `brew bundle cleanup` or uninstall unrelated software.
5. All selected apps have routes in Brewfile.selected and manifests/direct-selected.tsv. Read SOURCES.md. Direct installs verify SHA-256 and bundle IDs; never bypass a mismatch. Magnet requires an App Store sign-in and existing purchase. Do not purchase anything automatically. The selected setup requires Apple silicon and macOS 14 or later.
6. Ask the owner to complete account sign-ins, licenses, sync, backup, and FileVault tasks. No credentials are stored here. Never solicit passwords in chat.
7. No editor, extensions, configuration files, or specific font were individually selected. Clarify those broad goals before adding software or changing settings.
8. Verify installed selections and report remaining manual tasks accurately. Checked selection boxes do not prove installation succeeded.

After selection edits, run `python3 scripts/prepare.py` and review its diff before installation. This updates the Brewfile and manual plan; it does not install anything.

Validate changes with `python3 -m unittest discover -s tests -v`, `bash -n bootstrap.sh scripts/install.sh scripts/install-direct.sh`, and `git diff --check`. Tests copy fixture apps only into temporary directories; do not run the real setup on the original Mac merely to test it.
