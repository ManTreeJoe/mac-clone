# Official sources for the last seven apps

Verified against developer pages, release metadata, and installed app identities on November 14, 2026. No third-party mirror downloads are used.

| Selected app | Official source | Installation route |
| --- | --- | --- |
| Ardia | [ardia.dev](https://ardia.dev/), [developer releases](https://github.com/ardia-browser/ardia/releases) | Homebrew `ardia`, the current stable release. The original Mac had a nightly build. |
| ArtCraft Launcher | [ArtCraft's apps page](https://getartcraft.com/apps), [storytold/craft-launcher](https://github.com/storytold/craft-launcher/releases) | Homebrew `artcraft-launcher`; this is the launcher, not the separate ArtCraft studio app. |
| Card Hopper | [ManTreeJoe/cardHopper v1.3.4](https://github.com/ManTreeJoe/cardHopper/releases/tag/v1.3.4) | Official arm64 ZIP, SHA-256 pinned; expected app ID `com.cardhopper.app`. The installed updater explicitly identifies this repository as its publisher. |
| Grok Bot | [developer setup guide](https://docs.x.ai/grok-bot/get-started), [x.ai/bot](https://x.ai/bot) | Homebrew `grok-bot`, whose official download is hosted on `downloads.cursor.com`; matches the original `com.anysphere.sand` app. |
| Isocast | [anomalyco/isocast releases](https://github.com/anomalyco/isocast/releases/tag/v0.0.10) | Official 0.0.10 arm64 DMG, SHA-256 pinned; expected app ID `dev.isocast.release`. The older installed app used the project's earlier `R44VC0RP/isocast` release feed. |
| Magnet | [developer site](https://magnetmac.com/), [Mac App Store](https://apps.apple.com/us/app/magnet/id441258766?mt=12) | Homebrew Bundle's `mas` entry for ID `441258766`. Requires the signed-in Apple Account's existing purchase; does not purchase paid apps. |
| UGREEN NAS | [official download center](https://ai.ugreen.com/pages/downloads) | Vendor's Apple-silicon desktop client 1.21.0.80330, SHA-256 pinned; expected app ID `com.ugreen.pro.client`. Uses the desktop DMG, not the iOS App Store app. |

## Direct-download integrity

The Card Hopper and Isocast SHA-256 values come from the official GitHub release assets' digest fields. UGREEN's download center calls `https://api-us.ugnas.com/api/system/v3/sa/apk`; its Apple-silicon Mac record is ID 423 (`clientBit: 3`). The installer resolves that fixed record through the official `ua/temp/link` endpoint with a cache-busting timestamp and accepts only its `https://dl-us.ugreennas.com/` CDN link.

The downloaded UGREEN DMG was checked against the vendor record's MD5 `cc71c3ce09264b1e6224683c478bc003`; its stronger SHA-256 is pinned in the manifest for installation. Signed CDN query strings expire and are deliberately not committed. Each direct download must match its SHA-256 before extraction, and its extracted app must match the expected bundle ID before copying. Failed downloads, changed contents, or mismatched app identities are reported as failures. Gatekeeper checks and macOS permissions are not disabled.

Homebrew cask metadata: [Ardia](https://formulae.brew.sh/cask/ardia), [ArtCraft Launcher](https://formulae.brew.sh/cask/artcraft-launcher), [Grok Bot](https://formulae.brew.sh/cask/grok-bot). [Homebrew Bundle](https://docs.brew.sh/Brew-Bundle-and-Brewfile) supports Mac App Store entries; [mas](https://github.com/mas-cli/mas) documents account and purchase requirements.
