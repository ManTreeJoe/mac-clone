# New Mac installation instructions

The owner has chosen software in CHECKLIST.md. Checked boxes are the selection authority. Do not install unchecked items from the full inventory.

1. Read README.md, CHECKLIST.md, Brewfile.selected, and MANUAL-INSTALL.md.
2. This is an installation request for a new Mac only when the owner asks to set up that Mac. Do not install packages merely when editing this repo.
3. On an authorized target Mac, check for Xcode command-line tools and Homebrew. If absent, use their official installation instructions. Let the owner handle admin dialogs and account sign-ins.
4. Run `bash scripts/install.sh` to install the selected Homebrew apps and Git tools. Do not use `brew bundle cleanup` or uninstall unrelated software.
5. Handle every app in MANUAL-INSTALL.md through a verified official source or purchase history. Ambiguous apps require source confirmation; never silently omit them or substitute namesakes.
6. Ask the owner to complete account sign-ins, licenses, sync, backup, and FileVault tasks. No credentials are stored here. Never solicit passwords in chat.
7. No editor, extensions, configuration files, or specific font were individually selected. Clarify those broad goals before adding software or changing settings.
8. Verify installed selections and report remaining manual tasks accurately. Checked selection boxes do not prove installation succeeded.

After selection edits, run `python3 scripts/prepare.py` and review its diff before installation. This updates the Brewfile and manual plan; it does not install anything.
