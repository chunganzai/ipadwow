# ipadwow CHANGELOG

在 iPad mini 8（iPadOS 27.0）上，用免費 Apple ID 加 External JIT 跑《魔獸世界永恆》（WoW Forever），透過 WolkaraForever（Tolkara）。
時間為台灣時間（UTC+8）。
文中 `<TEAM_ID>`、`<IPAD_APPLE_ID>`、`<GITHUB_USER>` 等代號的實際值，記在本機的 `PRIVATE.local.md`（不上 git）。

---

## 2026-11-18

### 目前狀態
- ✅ WolkaraForever v1.0.17 已裝到 iPad，名稱顯示為 **Tolkara**，bundle `local.tolkara.app.<TEAM_ID>`
- ✅ 簽名內含 `com.apple.developer.kernel.increased-memory-limit = true` 和 `get-task-allow = true`
- ✅ 從 StikDebug 啟動，JIT 成功。log 顯示 `arena was reserved at launch`，大小 1 GiB
- ✅ 設定：Game Edition = Forever（`wowf`）、Region = **Taiwan（`tw`）**、Language = English（enUS）
- ✅ 遊戲下載完成（16:18，iPad 上約 49GB，檢查 `error=none`）
- ✅ 按 Play 後遊戲能啟動到登入畫面；可用記憶體約 **11.7GB**（遊戲顯示 11.5 GB System Memory），記憶體權限有生效
- ✅ **Battle.net 登入成功**（約 20:00）：含根憑證的 IPA + `portal "KR"` + 手動輸入驗證器代碼
- 🎯 目標達成：iPad 上可以操作登入 Battle.net，已進到角色列表
- ✅ 自動重簽：見下方「自動重簽工具」
- ✅ **繁中介面**（21:22 確認）：zhTW 語言檔下載完成，介面和語音都是中文

### 一鍵啟動捷徑（21:10，待測）
- 需求：從主畫面點一下就開遊戲，不用每次進 StikDebug
- 不需要 JIT 的方式不存在；Tolkara 自己開 JIT 的「Developer service」模式要 Network Extension 權限，只有付費帳號能用
- 免費帳號做法：StikDebug 3.2.2 有捷徑動作 `EnableJITIntent`（Enable JIT，參數 App），也支援網址 `stikjit://enable-jit?bundle-id=…&script-name=…`
- 捷徑檔要在 Mac 上簽名才能匯入，所以要在 iPad 上手動建立，步驟見 `SHORTCUT.md`
- zhTW 下載 20:58 卡住（網路沒有回應），重開後 21:07 從剩下的 3.03GB 接著下載

### 重開遊戲閃退 → 語言被同步成 zhTW（20:11）
- 現象：從 StikDebug 開、按 Play 後約 5 秒遊戲自己結束（`World of Warcraft Forever has closed`），JIT 和記憶體都正常，沒有當機紀錄
- 原因：第一次登入後 `Config.wtf` 的 `textLocale`、`audioLocale` 從 `enUS` 被改成 `zhTW`（推測是同步了帳號在電腦版的設定），但 iPad 只下載了 enUS 語言檔
- 處理：Tolkara 關閉後改回 `enUS`（portal `KR` 不動），原檔備份在 scratchpad

### 文字改繁體中文（20:15–20:18）
- 需求：文字用繁中、語音維持英文
- WolkaraForever 下載和遊戲本身支援 zhTW，但 UI 選單和 `wolkaraforever-config.json` 的驗證只允許 enUS/frFR/esES/deDE
- fork 修改（標籤 **`v1.0.17-zhtw`**，基於 `v1.0.17-roots`，同樣含根憑證）：
  - `WoW/WoWViewController.m`：選單、預設語言、語言名稱清單加入 `zhTW`
  - `Shell/WolkaraForeverConfig.m`：`WoWLocale` 允許 `zhTW`
  - `Shell/{en,fr,de}.lproj/Localizable.strings`：加 `locale.zhTW`
- 雲端編譯一次成功 → `ipa/WolkaraForever-v1.0.17-zhtw-unsigned.ipa`（10,013,229 bytes）；GitHub release 下載後已刪除
- 用 `resign/` 的 iloader 自動化覆蓋安裝，49GB 遊戲檔、portal KR 保留，到期 11/25 20:18
- `resign/apps.conf` 改用 zhtw 版 IPA
- 20:53 iPad 上開始下載 zhTW（驗證總量約 51GB）；`wolkaraforever-config.json` 已是 `WoWLocale: zhTW`
- **決定（20:58）：文字和語音都用中文**，`Config.wtf` 維持 `textLocale/audioLocale "zhTW"`，不改回英文語音
- 21:17 zhTW 下載完成（`error=none`，沿用 47GB、實際讀取約 1.3GB 驗證）
- ✅ 21:22 進遊戲確認介面是繁體中文

### 不透過電腦重簽的可能性（評估，20:10）
| 方式 | 可行性 | 說明 |
|------|--------|------|
| SideStore（iPad 上自己重簽） | ⚠️ 目前不行 | 唯一的「免費帳號 + 不用電腦」正規做法；但 0.7.0 在這台 iPad 登入失敗（-45063 / 401）。可試 iloader 的「SideStore（每夜建置版）」看是否已修好；SideStore 會佔第 3 個 App 名額（剛好 3 個） |
| LiveContainer | ❌ 不建議 | Tolkara 需要自己的記憶體權限和 JIT，49GB 資料也在自己的容器裡，放進 LiveContainer 不適用；而且 LiveContainer 本身仍要重簽 |
| 付費 Apple Developer（US$99/年） | ✅ 可行 | 簽一次可用 1 年，但簽名當下仍需電腦（iloader）；見 `APPLE-DEVELOPER-ENROLL.md` |
| 第三方簽名服務 / 企業憑證 | ❌ 不建議 | 常被撤銷、需交出 Apple ID 或 IPA，也不一定支援 increased-memory-limit |
- 結論：免費帳號下目前仍需電腦，靠 `resign/` 自動重簽 + 提醒；SideStore 修好後可再試

### 自動重簽工具（20:05）
- 新增 `resign/`：每小時（systemd user timer `ipad-resign.timer`）檢查 iPad 上 App 的簽名到期日
  - 剩 2 天內且 iPad 有接 → 自動操作 iloader 視窗匯入 IPA 重簽，並確認新到期日
  - iPad 沒接 → 桌面通知提醒；做不到（螢幕鎖定、iloader 沒登入）也會通知原因
- 實測 `resign.py --force`：StikDebug、Tolkara 都在 1 分鐘內重簽成功，到期日延到 11/25 20:06；配對檔、49GB 遊戲檔、portal KR、記憶體權限都保留
- 原本想用 iloader 底層的 `isideload` 寫指令列工具，但安裝 Rust 被自動模式擋下，先用操作視窗的方式
- 詳見 `resign/README.md`

### 下載完成後到登入（19:30–19:56）
- **第一次 Play 失敗的原因：** 當時的 Tolkara 是從主畫面直接開的，log 裡沒有 `arena was reserved at launch`，等於沒有 JIT
  - 一定要走 LocalDevVPN → StikDebug → Enable JIT → 點 Tolkara；LocalDevVPN 要保持連線
  - 從 StikDebug 開之後 JIT 正常，遊戲進到登入畫面
- **記憶體：** `external-jit-diagnostics.log` 這版沒有 `budget=` 行，改看 `memory checkpoint … available=11779356088`（約 11.7GB）和遊戲 `Logs/gx.log` 的 `11.5 GB System Memory`
- **登入錯誤 BLZ51901016**（`ERROR_NETWORK_MODULE_SOCKET_CLOSED (1016)`）：連上 `TW.actual.battle.net:1119` 後約 0.6 秒被斷線
  - 原因一（推測）：官方 workflow 用 `TOLKARA_SYSTEM_ROOTS=NO` 編，IPA 不含根憑證；上游 `docs/IPHONE.md` 寫 Forever 要用含根憑證的版本才能登入
    - 修法：fork 的 `wolkaraforever/tools/package_ipa.sh` 加 `export TOLKARA_SYSTEM_ROOTS=YES`，標籤 **`v1.0.17-roots`**，雲端編譯一次成功
    - 產物 `ipa/WolkaraForever-v1.0.17-roots-unsigned.ipa`（10,013,075 bytes，內含 `CompatibilityRootCertificates.plist`）
    - 下載後**立刻刪除 GitHub release**，因為這版含 runner 的公開根憑證，不適合公開散布（標籤留著）
    - 用 iloader「匯入 IPA」覆蓋安裝：同 bundle ID，**49GB 遊戲檔保留**，`increased-memory-limit` 仍在
    - 只換這個之後，同樣出現 1016 → 不是唯一原因
  - 原因二：portal 設錯。iPad 的 `_forever_/WTF/Config.wtf` 是 `SET portal "TW"`，但電腦上（Lutris）能登入的 Forever 是 **`SET portal "KR"`**（台灣帳號走 KR 登入伺服器）
    - 修法：Tolkara 完全關閉後，用 ifuse 把那一行改成 `"KR"`，其他設定不動；原檔備份在 scratchpad
    - 上游文件說 beta 用 `portal "test"`，但以本帳號實際可用的值為準
- **portal 改 KR 之後：** 帳號密碼驗證通過（`SRP … ERROR_OK`、`authenticatorRequired=true`）
  - 第 1 次：等手機核准約 1 分鐘逾時 → `Fatal login error (325)`
  - 第 2 次：輸入驗證碼被拒 → `(14400)`，推測代碼錯誤或過期
  - **遊戲登入時手機不會跳出核准通知**，要自己打開 Battle.net 驗證器，把畫面上的代碼（Battle.net 驗證器通常 8 碼）在代碼快更新前輸入 → 成功
- 下載語言只有 enUS，所以 iPad 維持 `textLocale/audioLocale "enUS"`（電腦上是 zhTW）

### 安裝方式（和原規劃不同）
- **SideStore 在 iPad 上無法登入 → 已刪除，改用電腦上的 iloader 安裝全部 App**
  - On-Device Anisette：`ADIProvisioningStart failed (Pending ADI session (-45063))`
  - 遠端 anisette（mac-ani.jkcoxson.com、ani.stikstore.app）：`Apple PTM/TK endpoint returned HTTP 401`
  - 同一個 Apple ID 在 iloader 能登入，所以判斷是 SideStore 0.7.0 的問題。2026-10 起 SideStore GitHub 有大量登入失敗回報（-80045、-80046 等）
  - 曾匯入自訂伺服器清單 `anisette-servers-ipad.json` 到 SideStore Documents，無效
- **iloader v2.4.1**：「匯入 IPA」會自動加上 increased-memory-limit，所以**不需要 GetMoreRam**
  - 舊版二進位備份在 `~/.local/bin/iloader.v2.3.9.bak`。實際上舊檔已自動更新成 2.4.1，兩個檔案內容相同
  - Anisette 伺服器：Jkcoxson；iPad 用 Apple ID：<IPAD_APPLE_ID>（Team `<TEAM_ID>`）

### iPad 上的 App（免費帳號 3 個名額，目前用 2 個）
| App | 來源 | Bundle |
|-----|------|--------|
| LocalDevVPN | App Store，不佔名額 | `com.jkcoxson.LocalDevVPN` |
| StikDebug 3.2.2 | iloader 匯入 IPA | `com.stik.stikdebug.<TEAM_ID>` |
| Tolkara（WolkaraForever v1.0.17） | iloader 匯入 IPA | `local.tolkara.app.<TEAM_ID>` |

### StikDebug 配對檔
- iloader「管理配對檔案 → 放入」後，StikDebug 的 Documents 仍是空的
- 改為手動：把 SideStore Documents 裡 iloader 產生的 `PairingFile_RemoteRP.plist`（同時含 lockdown 和 RP 欄位），用 `ifuse --documents` 複製成 StikDebug 的 `pairingFile.plist`
- 之後 StikDebug 開啟沒有錯誤

### WolkaraForever 使用要點
- 啟動流程：LocalDevVPN 連線 → StikDebug → Enable JIT → 長按 Tolkara 選 Assign Script → **universal.js** → 點 Tolkara 啟動。不要從主畫面直接開
- 下載語言選單只有 enUS、frFR、esES、deDE。程式碼支援 zhTW，但 UI 沒開放
- 地區有 Europe、Americas、Korea、Taiwan 四個
- 第一次的按鈕是 **Install**，下載完會變 **Play**

### 其他
- iPad 內容讀取方式：`ifuse --documents <bundle> <mount>`，App 列表和權限用 `ideviceinstaller -l -o list_user -o xml`
- 電腦螢幕鎖定時，iloader 的 GUI 自動操作會中斷，需要使用者解鎖

---

## 2026-11-17

### GitHub 雲端編譯 IPA
- 登入 `gh`（帳號 <GITHUB_USER>），fork `jklock/wolkaraforever` 到 https://github.com/<GITHUB_USER>/wolkaraforever ，並開啟 Actions
- 官方 workflow「Experimental IPA (manual)」（`release.yml`）有 bug：
  - `package_ipa.sh` 會 `cd build/platform`，IPA 產生在 `build/platform/Tolkara-unsigned.ipa`
  - 但 Publish 步驟在根目錄找 `Tolkara-unsigned.ipa` → `no matches found`
- 修法：不改 workflow，因為那需要 gh token 的 `workflow` scope，而 device-flow 授權逾時了
  - 在 v1.0.17 上加一個 commit，修改 `wolkaraforever/tools/package_ipa.sh`，編完把 IPA 複製回根目錄
  - 打上標籤 **`v1.0.17-ipa`** 並 push
  - 用 `gh workflow run release.yml -f tag=v1.0.17-ipa`
  - 失敗留下的空 release `v1.0.17` 已刪除
- `macos-26` runner 容量不足，好幾次出現 "job was not acquired by Runner … capacity constraints"
  - 用背景迴圈自動 rerun，第 5 次成功
  - 不改用 macos-15，因為編譯會檢查主機的 macOS 框架
- 產物：`Tolkara-unsigned.ipa`（9,894,277 bytes）
  - 本機存成 `ipa/WolkaraForever-v1.0.17-unsigned.ipa`，另外複製到 `~/下載/`
  - 編譯沿用官方 `TOLKARA_SYSTEM_ROOTS=NO`。如果之後登入出現憑證錯誤，改成 YES 重新編譯

### iPad 前置
- App Store 安裝 LocalDevVPN
- 先用 iloader 安裝 SideStore（後來刪除，見 11-18）
- 下載 StikDebug 3.2.2 IPA 到 `ipa/` 和 `~/下載/`

### 文件
- `IPAD-FREE-ROUTE.md`：免費 Apple ID 路線規劃，開頭加上「實作紀錄」
- `README.md`、`INSTALL-MAC.md`、`APPLE-DEVELOPER-ENROLL.md`：Mac 加付費帳號路線，目前用不到，當作備案
