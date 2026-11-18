# ipadwow — Running World of Warcraft: Forever natively on iPad

[繁體中文](README.md) | **English**

This repo runs WoW Forever natively on an iPad with the unofficial **WolkaraForever** project, which is built on **Tolkara**.
**You don't need a Mac or a paid Apple Developer account.** A Linux PC, a free Apple ID and a GitHub Actions cloud build are enough.

- Test device: iPad mini 8 (A20 Pro, ~12 GB RAM, 256 GB, iPadOS 27.0)
- Status (2026-11-18): ✅ installed ✅ JIT ✅ game downloaded ✅ Battle.net login, character list reached ✅ Traditional Chinese UI
- Detailed log and troubleshooting history: [CHANGELOG.md](CHANGELOG.md) (Traditional Chinese)
- `<TEAM_ID>`, `<GITHUB_USER>`, `<IPAD_APPLE_ID>` and similar are placeholders. Replace them with your own values.
- These are personal notes, not official WolkaraForever documentation. This repo does not distribute any IPA.
- Other documents in this repo are in Traditional Chinese.

> ⚠️ Account risk: Tolkara states that "the risk of suspension or ban when using online accounts is real and entirely yours." Blizzard does not support this project. Do not combine it with any add-on automation, bots or cheats.

---

## How it works

| Component | Role | Source |
|-----------|------|--------|
| **WolkaraForever** (app name: Tolkara) | Loads the unmodified macOS arm64 WoW client on iPad. It downloads, verifies and updates the game from Blizzard's CDN by itself | Your own fork, built into an IPA with GitHub Actions |
| **StikDebug** | Enables JIT (executable memory) for Tolkara. You need it every time you launch the game | Official IPA |
| **LocalDevVPN** | An on-device tunnel that lets StikDebug reach the iPad's own developer service. It does not route normal internet traffic | App Store |
| **iloader** (on the Linux PC) | Signs and installs IPAs with a free Apple ID. **It adds `increased-memory-limit` automatically**, so the app gets enough memory | [nab138/iloader](https://github.com/nab138/iloader) (v2.4.1) |
| `resign/` | Checks signing expiry every hour and re-signs with iloader before it expires | This repo |

Free account limits:
- Signatures expire after **7 days**
- At most **3** sideloaded apps at once (StikDebug and Tolkara use 2)
- At most 10 new App IDs per 7 days

---

## Requirements

- A Linux PC with `iloader`, `libimobiledevice`, `ifuse` and `gh`
- A USB-C cable
- An Apple-silicon iPad, ideally on iPadOS 27, with **≥ 70 GB free**. The game is ~49 GB, ~51 GB+ with the Chinese language pack, plus space for update staging
- A free Apple ID (a separate one just for sideloading is recommended)
- A GitHub account
- A Battle.net account with access to Forever, plus the Battle.net Authenticator

---

## Installation (from scratch)

### 1. Build the IPA (GitHub Actions, no Mac needed)
1. Fork `jklock/wolkaraforever` and enable Actions on the fork.
2. Upstream `release.yml` has a bug: the IPA is produced in `build/platform/`, but the upload step looks for it in the repo root.
   - Fix it by adding a commit on the version you want to build that makes `wolkaraforever/tools/package_ipa.sh` copy the IPA back to the root, then tag that commit.
   - The workflow file itself is not changed, because editing it needs the `workflow` scope on the gh token.
3. In the same script add `export TOLKARA_SYSTEM_ROOTS=YES` so the IPA bundles root certificates. **Without them, the Forever login is disconnected (BLZ51901016).**
4. Optional, for a Traditional Chinese UI: allow `zhTW` in the language menu and config validation in `WoW/WoWViewController.m` and `Shell/WolkaraForeverConfig.m`.
5. Start the build with `gh workflow run release.yml -f tag=<tag>`.
   - The `macos-26` runner is often not picked up ("job was not acquired… capacity constraints"). Re-run it.
   - Don't switch to macos-15. The build inspects the host's macOS frameworks.
6. Download the IPA from your release into `ipa/`, **then delete the GitHub release**. An IPA that bundles root certificates should not be shared publicly. The tag can stay.

Tags used on the fork:

| Tag | Contents |
|-----|----------|
| `v1.0.17-ipa` | v1.0.17 + IPA upload path fix |
| `v1.0.17-roots` | + bundled root certificates (`TOLKARA_SYSTEM_ROOTS=YES`) |
| `v1.0.17-zhtw` | + zhTW language option ← **currently used** |

### 2. Prepare the iPad
1. Install **LocalDevVPN** from the App Store.
2. Turn on Developer Mode in Settings → Privacy & Security → Developer Mode, then restart.
3. Connect the iPad by USB and tap **Trust**.

### 3. Install with iloader
1. Open iloader, sign in with the iPad's Apple ID, and choose **Jkcoxson** as the Anisette server.
2. Use **Import IPA** to install **StikDebug** (`ipa/StikDebug-3.2.2.ipa`).
3. Use **Import IPA** to install **WolkaraForever** (`ipa/WolkaraForever-v1.0.17-zhtw-unsigned.ipa`).
4. On the iPad, trust your Apple ID in Settings → General → VPN & Device Management.
5. Check the entitlements with `ideviceinstaller -l -o list_user -o xml`. Tolkara must have `com.apple.developer.kernel.increased-memory-limit = true`.

> SideStore and GetMoreRam are not needed.
> - SideStore 0.7.0 could not sign in on this iPad (-45063, HTTP 401).
> - The SideStore nightly can sign in, but it wants to revoke iloader's signing certificate. That would break the apps iloader installed, so it is not used (see CHANGELOG).

### 4. StikDebug pairing file
iloader's "Manage pairing files → Place" did not put the file into StikDebug, so copy it manually:
1. Generate a pairing file with iloader. iOS 26+ needs `PairingFile_RemoteRP.plist`, the one with the RP fields.
2. Mount StikDebug's Documents with `ifuse --documents com.stik.stikdebug.<TEAM_ID> <mountpoint>`.
3. Copy the file in as `pairingFile.plist`, then unmount.
4. Open StikDebug and make sure it shows no error.

### 5. First launch and game download
1. Connect LocalDevVPN, then in StikDebug:
   1. Tap **Enable JIT**
   2. Long-press Tolkara → **Assign Script** → `universal.js`
   3. Tap Tolkara
2. In Tolkara choose Game Edition **Forever**, Region **Taiwan** and Language **Traditional Chinese** (or English).
3. Tap **Install** and let it download ~49 GB or more. Keep the iPad unlocked with Tolkara in the foreground. When it finishes, the button changes to **Play**.

### 6. Change the login portal (required for Taiwan accounts)
Taiwan accounts log in through the **KR** portal. The app's default `TW` fails with BLZ51901016.
1. **Fully close Tolkara** by swiping it away in the app switcher.
2. Mount it with `ifuse --documents local.tolkara.app.<TEAM_ID> <mountpoint>`.
3. In `World of Warcraft/_forever_/WTF/Config.wtf`, change `SET portal "TW"` to `SET portal "KR"` and leave everything else as it is.
4. Unmount.

### 7. Log in
- Launch Tolkara from StikDebug, tap **Play**, and enter your Battle.net credentials.
- **No approval notification appears on your phone.** Open the Battle.net Authenticator yourself and enter the code it shows (usually 8 digits) before it changes.

---

## Playing

1. Make sure **LocalDevVPN** is connected. You can leave it on, or toggle it in Settings → VPN or in Control Center.
2. Launch Tolkara from StikDebug. **Don't open it from the Home Screen**: it would start without JIT and the game would fail.
3. Tap **Play**.

For one-tap launching, make a Home Screen shortcut with the Shortcuts app. The steps are in [SHORTCUT.md](SHORTCUT.md) (⏳ not yet tested).

To confirm that JIT worked, look for `an arena was reserved at launch` in `wolkaraforever.log`.

---

## Re-signing every 7 days

- `resign/` runs every hour as the systemd user timer `ipad-resign.timer`.
  - If a signature expires within 2 days and the iPad is connected, it drives the iloader window to re-sign.
  - If the iPad isn't connected, it shows a desktop notification instead.
- Re-signing installs over the existing app, so game files, the pairing file and `Config.wtf` are kept.
  - **The bundle ID must stay the same.**
  - **Never delete the app**, or the game data will be lost.
- It needs an unlocked desktop session and iloader signed in.
- Commands: `resign/resign.py --status` and `resign/resign.py --force`. See [resign/README.md](resign/README.md).
- When you switch to a new IPA, update the path in `resign/apps.conf`.

---

## Problems we hit

| Symptom | Cause | Fix |
|---------|-------|-----|
| Play does nothing or fails, and the log has no `arena was reserved` | Opened from the Home Screen, so there was no JIT | Launch through LocalDevVPN → StikDebug |
| Login **BLZ51901016** (disconnected ~0.6 s after connecting) | ① The IPA has no root certificates ② The portal is set to `TW` | ① Build with `TOLKARA_SYSTEM_ROOTS=YES` ② Set `portal "KR"` in `Config.wtf` |
| `Fatal login error (325)` | Timed out waiting for phone approval, which never arrives | Enter the authenticator code manually |
| Login `(14400)` | Wrong or expired authenticator code | Enter the code before it changes |
| After the first login, the game quits ~5 s after launch | Account sync changed the `Config.wtf` locale to `zhTW`, but the zhTW data wasn't downloaded | Download zhTW in Tolkara, or set `textLocale`/`audioLocale` back to a downloaded locale |
| Download progress freezes with no error | The network stopped responding and the app kept waiting | Fully close Tolkara and relaunch from StikDebug. Downloaded data is kept |
| SideStore sign-in fails (-45063, HTTP 401) | SideStore 0.7.0 issue | Use iloader on the PC instead |

---

## Useful commands

```bash
idevice_id -l                                               # is the iPad connected?
ifuse --documents local.tolkara.app.<TEAM_ID> <mountpoint>  # read/write Tolkara's files
fusermount -u <mountpoint>
ideviceinstaller -l -o list_user -o xml                     # apps and entitlements
ideviceinfo -q com.apple.disk_usage                         # free space on the iPad
~/ipadwow/resign/resign.py --status                         # signing expiry
```

Useful files in Tolkara's Documents:
- `wolkaraforever.log`: launcher log (JIT, download progress)
- `external-jit-diagnostics.log`: JIT and memory (`memory checkpoint … available=`)
- `wolkaraforever-config.json`: edition, region, language
- `World of Warcraft/_forever_/WTF/Config.wtf`: game settings (`portal`, `textLocale`, `audioLocale`)
- `.tolkara-updates/`: update staging. Files replace the live install only when the update completes, so a failed update doesn't break the existing install.

---

## What a paid account adds (not required)

A paid Apple Developer membership costs US$99/year and gives you:
- Signatures that last one year instead of 7 days. You still need a computer to sign.
- Tolkara's **Developer service** mode, where Tolkara enables JIT by itself. You don't need StikDebug or LocalDevVPN and can just tap the app icon. This mode needs the Network Extension entitlement, which free accounts cannot sign.

Related (Chinese): [APPLE-DEVELOPER-ENROLL.md](APPLE-DEVELOPER-ENROLL.md), [INSTALL-MAC.md](INSTALL-MAC.md) (official Mac route)

---

## Documents

| File | Contents |
|------|----------|
| [CHANGELOG.md](CHANGELOG.md) | Progress, current state, troubleshooting log |
| [SHORTCUT.md](SHORTCUT.md) | One-tap Home Screen shortcut |
| [resign/README.md](resign/README.md) | Auto re-sign tool |
| [IPAD-FREE-ROUTE.md](IPAD-FREE-ROUTE.md) | Original plan for the free route (2026-11-17) |
| [RESEARCH.md](RESEARCH.md) | Early research; its "Mac required" conclusion is outdated |
| [INSTALL-MAC.md](INSTALL-MAC.md), [APPLE-DEVELOPER-ENROLL.md](APPLE-DEVELOPER-ENROLL.md) | Paid account and Mac route (backup) |
| `reference/` | Copies of upstream docs (MIT, see `reference/upstream/NOTICE.md`), Blizzard CDN and version data |

## Sources

- WolkaraForever: https://github.com/jklock/wolkaraforever (free Apple ID success report: issue #67)
- Tolkara: https://github.com/tolkara/tolkara
- StikDebug: https://github.com/StikDebug/StikDebug
- iloader: https://github.com/nab138/iloader
