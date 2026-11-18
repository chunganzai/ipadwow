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
- ⏳ 遊戲下載中，總量約 **50.7GB**，比原估 70GB 小
- ⏳ 待做：按 Play 後讀 `external-jit-diagnostics.log` 的 `budget=`，6GB 以上才算記憶體權限生效；之後登入 Battle.net

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
