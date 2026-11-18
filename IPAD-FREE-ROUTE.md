# iPad 執行步驟規劃：免費 Apple ID 加 External JIT（不用 Mac）

> 📜 **原始規劃**（2026-11-17）。實際做法有些不同（沒用 SideStore、GetMoreRam），以 [README.md](README.md) 為準。


整理日期：2026-11-17。對象：iPad mini 8（A20 Pro、約 12GB RAM、256GB、iPadOS 27）加這台 Linux 電腦。
依據：
- jklock/wolkaraforever issue #67：iPhone 16 Pro Max、iOS 27.0、免費 Apple ID，**2026-11-14 成功進入遊戲世界**。
- 官方 BUILDING.md、release.yml、StikDebug 和 GetMoreRam 的官方說明。
- 原文備份在 `reference/upstream/`。

> ⚠️ 這是**實驗性路線**。成功案例是 iPhone，iPad 上幾乎沒人實測；官方 BUILDING.md 寫「External JIT 尚未在實機跑過」，那句話已經過時（#67 已證實可行）。
> 封號風險和官方路線相同：「風險是真實的，而且完全由你承擔」。

---

## 🛠 實作紀錄（2026-11-18，實際做法和下面規劃不同的地方）

| 項目 | 實際情況 / 改法 |
|------|----------------|
| GitHub | 帳號 <GITHUB_USER>，fork：https://github.com/<GITHUB_USER>/wolkaraforever |
| 官方 release.yml 的 bug | IPA 產生在 `build/platform/`，上傳步驟卻在根目錄找 → 失敗。修法：新增標籤 **`v1.0.17-ipa`**（改 `wolkaraforever/tools/package_ipa.sh`，編完把 IPA 複製到根目錄），用這個標籤跑 Actions。不改 workflow 檔（那需要 gh 的 workflow 權限） |
| GitHub Actions | `macos-26` 雲端 Mac 常排不到（"job was not acquired… capacity constraints"），要一直 rerun。不要改成 macos-15：編譯會讀取主機的 macOS 框架 |
| SideStore 0.7.0 | **iPad 上登入失敗**：On-Device Anisette 出 -45063；jkcoxson / StikStore 伺服器都是 `Apple PTM/TK endpoint returned HTTP 401`（同一個 Apple ID 在 iloader 可登入）。→ **已刪除 SideStore，改用電腦上的 iloader 安裝所有 App** |
| iloader | **v2.4.1 安裝任何 IPA 都會自動加上 increased-memory-limit** → **不需要 GetMoreRam**。Anisette 選 Jkcoxson。iPad 用的 Apple ID：<IPAD_APPLE_ID>（Team <TEAM_ID>） |
| StikDebug 3.2.2 | 用 iloader「匯入 IPA」安裝（bundle `com.stik.stikdebug.<TEAM_ID>`）。iloader 沒放好配對檔 → 手動把 SideStore 資料夾裡的配對檔複製成 StikDebug Documents 的 `pairingFile.plist`，StikDebug 開啟無錯誤 |
| 每週更新簽名 | 因為沒有 SideStore：**每 7 天把 iPad 接電腦，用 iloader 對同一個 IPA 再「匯入 IPA」一次**（覆蓋安裝，資料保留） |
| App 名額 | StikDebug + WolkaraForever = 2/3（LocalDevVPN 是 App Store 版，不算） |
| IPA 存放 | `~/ipadwow/ipa/`，另複製一份到 `~/下載/` |

---

## 一、前置軟體清單

### 這台 Linux 電腦（只在一開始用到）

| 軟體 | 用途 | 狀態 |
|------|------|------|
| **iloader**（`~/.local/bin/iloader`，v2.3.9） | 第一次把 SideStore 裝到 iPad，並放入配對檔 | ✅ 已有（iPhone 時用過）；動工前檢查有沒有新版 |
| `ifuse`、`libimobiledevice` | 從電腦讀 iPad 上 App 的 Documents（查記憶體 log） | ✅ 已有（iPhone 時用過） |
| idevice_pair（jkcoxson） | **備案**：產生 iOS 26 以上用的 **rppairing** 配對檔 | 需要時再裝：https://github.com/jkcoxson/idevice_pair/releases/latest |
| **GitHub 帳號** | Fork 專案並用 GitHub 雲端 Mac 編譯 IPA | ❓ 使用者要提供，或新建一個 |
| USB-C 傳輸線 | iPad 第一次接電腦 | 準備 |

### iPad 上要裝的 App

| # | App | 來源 | 佔免費帳號名額？ | 用途 |
|---|-----|------|------------------|------|
| 1 | **LocalDevVPN** | App Store（免費） | 否 | 讓 iPad 自己連到自己的開發者服務；SideStore 重新簽名和 StikDebug 開 JIT 都靠它 |
| 2 | **SideStore** | 用 iloader 從電腦安裝 | ✅ 第 1 個 | 用免費 Apple ID 簽名、安裝、每 7 天重新整理 |
| 3 | **StikDebug 3.2.2 以上** | SideStore 安裝 `StikDebug-3.2.2.ipa`（https://github.com/StikDebug/StikDebug/releases） | ✅ 第 2 個 | 開 JIT（iOS 27 支援；3.2.0 起能在裝置上產生配對檔） |
| 4 | **WolkaraForever**（`Tolkara-unsigned.ipa`，External JIT 版） | 自己 Fork 後用 GitHub Actions 編譯，再用 SideStore 安裝 | ✅ 第 3 個 | 遊戲啟動器：下載、更新、執行永恆 |
| 5 | **GetMoreRam** | SideStore 安裝（https://github.com/hugeBlack/GetMoreRam） | ✅ **暫時**用到第 4 個名額 | 幫 WolkaraForever 的 App ID 開啟「增加記憶體上限」權限，用完就刪 |
| — | 檔案 App | 內建 | — | 查看 log |

> **免費 Apple ID 規則：** 同一台裝置同時最多 **3 個**側載 App；每個帳號每 7 天最多註冊 **10 個 App ID**；簽名 **7 天**到期，要重新整理。
> 剛好放得下 SideStore、StikDebug、WolkaraForever 三個。GetMoreRam 要暫時停用 StikDebug 騰出名額，用完再換回來。

### Apple ID 的選擇（動工前決定）
- **選項 A：和 iPhone 共用同一個免費 Apple ID**（team <IPHONE_TEAM_ID>）
  - 每週 10 個 App ID 的額度和 iPhone 共用，iPhone 那邊的 SideStore、LiveContainer、Dopamine 也在用。
- **選項 B：iPad 另外開一個免費 Apple ID（建議）**
  - 額度獨立，出問題也不會影響 iPhone。
- 無論哪個都要開**雙重認證**。

---

## 二、執行步驟

### 階段 1｜電腦：在 GitHub 雲端編譯 WolkaraForever IPA

1. 登入 GitHub → 打開 https://github.com/jklock/wolkaraforever → **Fork**。
2. 在自己的 fork：**Actions** 分頁 → 啟用 workflows → 選 **Experimental IPA (manual)** → **Run workflow**，tag 填當時最新的標籤（目前是 `v1.0.17`）。
   - 它在 GitHub 的 macos-26 雲端機器上執行 `wolkaraforever/tools/package_ipa.sh`。
   - 產出 `Tolkara-unsigned.ipa`：External JIT 預設模式，含 WolkaraForever 啟動器和下載器。
   - 公開 repo 使用 GitHub Actions 免費。
3. 完成後，到自己 fork 的 **Releases** → 對應的標籤 → 下載或複製 `Tolkara-unsigned.ipa` 的網址。
4. ⚠️ **根憑證問題（待確認）**：
   - 官方 workflow 用 `TOLKARA_SYSTEM_ROOTS=NO`，刻意不放 macOS 的系統根憑證。官方 README 說「讀取系統根憑證的程式會找不到憑證」。
   - #67 成功的使用者是用 **`TOLKARA_SYSTEM_ROOTS=YES`** 自己在 GitHub Actions 編譯的。
   - 建議：先用官方設定 `NO` 試。如果遊戲登入時出現連線、憑證錯誤，再把自己 fork 裡 `release.yml` 那行改成 `YES` 重新編譯。
   - 改成 YES 時，最好把產物改成 Actions artifact，不要公開 release。
   - Claude 可以協助改這個檔案。

### 階段 2｜電腦加 iPad：安裝 SideStore、開啟開發者模式

1. iPad 用 USB-C 接到 Linux 電腦 → iPad 上按「信任」。
2. 執行 `~/.local/bin/iloader` → 登入要用的 Apple ID → 選 iPad → 安裝 **SideStore**，並讓它放入配對檔。
   - anisette 設定沿用 iPhone 上可用的那組：伺服器 `https://mac-ani.jkcoxson.com`，詳細見 memory `iphone-sideload-setup`。
3. iPad：設定 → 隱私權與安全性 → **開發者模式** → 開啟 → 重開機 → 確認開啟。
   - 裝過開發用簽名的 App（SideStore）之後，這個選項才會出現。
4. iPad：設定 → 一般 → **VPN 與裝置管理** → 信任你的 Apple ID 開發者描述檔。
5. App Store 安裝 **LocalDevVPN** → 開啟並連線，允許加入 VPN 設定。
6. 打開 SideStore → 確認能「Refresh All」成功（代表簽名、配對、VPN 都正常）。

### 階段 3｜iPad：安裝 StikDebug 並設定 JIT

1. SideStore 安裝 StikDebug：
   - 在 Safari 打開 `sidestore://install?url=https://github.com/StikDebug/StikDebug/releases/download/3.2.2/StikDebug-3.2.2.ipa`（版本以當時最新為準）。
   - 或先下載 IPA，再從 SideStore 的「＋」匯入。
2. 開 StikDebug → 照提示**在裝置上產生配對檔**（3.2.0 起的功能）。
   - iOS 26 以上要的是 **rppairing**（RemotePairing）配對檔，不是舊式的 lockdown 配對檔。
   - 如果裝置上產生失敗，在 Linux 用 idevice_pair 產生後匯入。
3. LocalDevVPN 保持連線 → 在 StikDebug 測試連線，確認看得到裝置。

### 階段 4｜iPad：安裝 WolkaraForever

1. Safari 打開 `sidestore://install?url=<你 fork 的 Tolkara-unsigned.ipa 網址>` → SideStore 簽名安裝。
2. 記下 SideStore 給它的 **bundle ID**（App 詳細資料裡看得到）。之後重裝都必須是同一個，不然遊戲資料會在新的空容器裡。
3. **先不要下載遊戲**，先處理記憶體權限（階段 5）。

### 階段 5｜iPad：開啟「增加記憶體上限」權限（關鍵）

沒有這個權限，App 只有約 3.3GB 可用，進入遊戲世界時會閃退（#67 實測）。

1. SideStore → 停用 **StikDebug**，騰出名額（停用不是刪除）。
2. SideStore 安裝 **GetMoreRam**。
3. GetMoreRam → Settings → 登入**同一個 Apple ID** → **App IDs** → **Refresh** → 點 WolkaraForever 的 App ID → **Add Increased Memory Limit**。
   - 如果有 Extended Virtual Addressing 的選項也一併加上（官方說 IPA 宣告了這兩項權限）。
4. 回 SideStore → **重新安裝** WolkaraForever：用同一個 IPA 覆蓋安裝，**不是只按 Refresh**，也**不要先刪除**。
   - 這樣它才會拿到含新權限的描述檔。
5. SideStore：刪除 GetMoreRam → 重新啟用 StikDebug。
6. **驗證**：
   - 用 StikDebug 開一次 WolkaraForever（見階段 6 的 1–3）→ 關掉。
   - 讀 App Documents 裡的 `external-jit-diagnostics.log`，看第一行 `process-start … budget=` 的數字。
     - 約 `3,539,000,000`：權限**沒生效**，回第 3 步，或改試「疑難排解」的備案。
     - 約 `6,000,000,000` 以上：✅ 成功。iPad mini 8 的 RAM 比 iPhone 多，數字可能更高。
   - 怎麼讀 log：iPad「檔案」App → 我的 iPad → WolkaraForever；或接上 Linux 用 `ifuse --documents <bundle ID> <掛載點>`。

### 階段 6｜第一次開遊戲

1. 開 **LocalDevVPN**，確認已連線。
2. 開 **StikDebug** → 選 WolkaraForever → 由 StikDebug **啟動**它並開啟 JIT。
   - ⚠️ 一定要從 StikDebug 啟動，**不要先自己點開 App**（StikDebug 開發者在 issue #476 的說明）。
   - iOS 26 以上，StikDebug 對每個 App 要用對應的腳本。#67 用的是 **universal.js**；選腳本時選它，以當時 StikDebug 的提示為準。
   - 沒開 JIT 的話，App 會直接說明，不會啟動遊戲。
3. WolkaraForever 主畫面 → 選 **Forever**、**地區**、**遊戲語言** → 下載（約 70GB）。
   - iPad 接電源、用 Wi-Fi、保持螢幕亮著。中斷可以續傳，不要刪 App。
4. 顯示**就緒**後才按 **Play**。
5. 第一次進遊戲：
   - WolkaraForever 的畫面設定先選 **Performance**（#67 用 956×440 成功）。
   - 進遊戲後到 系統 → 圖形 全部調最低，穩定後再慢慢調高。
6. 登入問題：
   - **BLZ51914440**（被斷線）：看 issue #47 的「網頁登入交接」機制有沒有合併進新版。
   - **BLZ51900003**（帳密錯誤）：可能是地區選錯。台灣帳號試 TW 或 KR 相關地區。

### 階段 7｜日常使用與維護

- **每次玩**：LocalDevVPN 連線 → StikDebug → 啟動 WolkaraForever。
- **每 7 天**：SideStore 的 Refresh All。可以照 iPhone 的做法設捷徑自動化：LocalDevVPN 連線，然後 SideStore Refresh All。
  - 過期的話 App 打不開，但資料還在，重新整理後就恢復。
- **遊戲更新**：在 WolkaraForever 裡更新，不需要電腦。
- **App 升級**：在 GitHub 重跑 workflow 產生新 IPA → SideStore **覆蓋安裝**（同一個 bundle ID）。重裝後要再確認一次 `budget=`。

---

## 三、疑難排解與備案

| 問題 | 處理 |
|------|------|
| `budget=` 一直是 3.3GB | ① 確認是「重新安裝」不是 Refresh ② SideStore 裡停用再啟用 WolkaraForever ③ 備案：改用 AltStore 2.2 以上（它會自動開這個權限；#67 用 Windows 上的 AltStore Classic 2.3.3 成功，**這台是 Linux，需要另外找 Windows 電腦或 AltServer-Linux**）④ 備案：查新版 iloader 能不能直接簽 IPA 並保留權限 |
| StikDebug 連不上（E96、BrokenPipe、NotConnected） | 確認 LocalDevVPN 已連線、App 由 StikDebug 啟動、配對檔是 rppairing、StikDebug ≥ 3.2.2 |
| 進遊戲世界時閃退回主畫面 | 看 `external-jit-diagnostics.log` 有沒有 memory-warning 以及 budget 數字 → 降解析度（Performance）→ 回報到 #67 那類 issue |
| 遊戲登入時出現憑證或連線錯誤 | 用 `TOLKARA_SYSTEM_ROOTS=YES` 重新編譯（階段 1 第 4 步） |
| 安裝時 bundle ID 變了 | **停止**，不要繼續用新的；回去用原本的 ID 覆蓋安裝，不然 70GB 資料會在舊容器裡 |
| 超過 3 個 App 的名額 | 在 SideStore 停用暫時不用的 App；GetMoreRam 用完就刪 |

---

## 四、動工前待確認事項

- [ ] 使用者的 GitHub 帳號（要拿來 Fork 和跑 Actions）
- [ ] iPad 用哪個 Apple ID（建議另開一個）
- [ ] iloader 有沒有新版、是否支援 iPadOS 27
- [ ] SideStore 目前版本在 iPadOS 27 的狀態，以及它重新安裝時會不會保留 increased-memory-limit
- [ ] 動工當天重看：WolkaraForever 最新 release、issue #47（登入）、#67 後續、StikDebug 最新版
- [ ] 地區和語言：台灣帳號在 App 裡要選哪個地區（見 README〈地區與語言〉）

---

## 來源

- WolkaraForever：https://github.com/jklock/wolkaraforever （#67、#47、#82、`platform/docs/BUILDING.md`、`.github/workflows/release.yml`）
- StikDebug：https://github.com/StikDebug/StikDebug/releases 、https://stikdebug.org/ 、issue #476、#446
- GetMoreRam：https://github.com/hugeBlack/GetMoreRam
- idevice_pair：https://github.com/jkcoxson/idevice_pair/releases/latest
- LiveContainer 與 SideStore 說明：https://livecontainer.github.io/docs/installation/lc_sidestore
