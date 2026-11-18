# ipadwow — 在 iPad 上原生執行《魔獸世界：永恆》

> 📜 **歷史研究紀錄**（2026-11-15 ～ 11-17）。當時結論是「需要 Mac 和付費帳號」，**已經過時**：2026-11-18 起免費路線已實際跑通。現況和安裝方式看 [README.md](README.md)。


建立：2026-11-15（同日補上開發機 iPad mini 8 的評估）
狀態：⏸ 資料蒐集完成。2026-11-17 發現**可能不用 Mac** 的免費路線（見〈2026-11-17 更新〉）；官方路線的 Mac 安裝步驟見 [INSTALL-MAC.md](INSTALL-MAC.md)。
目的：讓 Claude 或使用者日後讀這份文件就能接續。

---

## 一句話結論

用非官方專案 **WolkaraForever**（建立在 **Tolkara** 之上）可以在 iPad 上**原生**跑 WoW 永恆。
支援的做法需要三樣東西：
- Apple 晶片的 Mac
- 付費 Apple Developer 會員（US$99/年）
- iPad 開啟開發者模式

只有 Linux 電腦加免費 Apple ID 時，目前沒有確定可行的路（理由見〈為什麼現在做不了〉）。

---

## 🆕 2026-11-17 更新（重要，先讀這段）

### 專案進度
- 最新正式版仍是 **v1.0.17**（2026-11-14）。之後 main 還有修正（至 2026-11-17 `db5470a`）：
  - 手把語音輸入（#92、#95）、插件 CurseForge 金鑰管理（#96、#97）、文件全面重寫（#85）。
- 版本歷程：v1.0.10 Duo 控制與版面、v1.0.11 聊天輸入、v1.0.12 重裝後保留授權、v1.0.13 手把、v1.0.14 觸控控制器、v1.0.15 鍵盤與聽寫、v1.0.16 插件中心、v1.0.17 建置修正。

### ✅ 閃退問題（補充③）其實早就修好了
- jklock 在 #22 說明：原因是新安裝寫出的 `.build.info` 缺 `CDN Servers`，**v1.0.2（#24）起已自動寫入並修復**。
- 官方路線不用再手動改 `.build.info`；補充③只在用很舊的版本時才需要。

### ⚠️ 新的登入問題（未解）
- **#47**：登入畫面被斷線 **BLZ51914440**（iPhone Duo、iOS 27.3）。
  - 有人說是 Blizzard 越來越要求「經啟動器登入」。
  - gus-schissler 參考 Waypoint 做了「battle.net 網頁登入再交給遊戲」的機制，iPad 和 iPhone 實測可用，正在開 PR。
  - 動工時看這個機制有沒有合併。
- **#82**：BLZ51900003（帳密錯誤）可能是**地區設定**造成的，不一定是密碼錯。台灣帳號要特別注意地區。

### 🔥 可能不需要 Mac 和付費帳號的路線（#67 實測成功）

**案例：**
- 環境：iPhone 16 Pro Max（A18 Pro）、iOS 27.0、**免費 Apple ID**、External JIT。
- 2026-11-14 成功進入遊戲世界。

**關鍵是記憶體上限（increased-memory-limit 權限）：**

| 簽名工具 | 權限 | 記憶體上限 | 結果 |
|----------|------|------------|------|
| Sideloadly | 被丟掉 | 3.3GB | 進世界時閃退 |
| **AltStore Classic 2.3.3** | 保留 | **6GB** | 成功進入遊戲 |

- 維護者 jklock 說明：**免費 Apple ID 也拿得到 increased-memory-limit**，是部分簽名工具在重簽時把它丟了。
- 這推翻了先前「免費帳號拿不到」的判斷。先前依據的是 Tolkara README 和 pookee 文件的說法。
- 保留權限的方法：
  1. **GetMoreRam**（https://github.com/hugeBlack/GetMoreRam）
     - 一個側載的小 App。登入同一個 Apple ID → App IDs → 對目標 App 按「Add Increased Memory Limit」。
     - 之後再從 SideStore 或 AltStore 重裝，就會帶上這個權限。
  2. **AltStore 2.2 以上**：會自動開啟這個權限。
  3. 有 Mac 的話，Xcode 加免費 Personal Team 也可以。
- 驗證方式：開一次 App 再關掉，看 `external-jit-diagnostics.log` 第一行的 `budget=`。
  - 約 3,539,000,000 代表權限沒生效；約 6,000,000,000 以上代表成功。
- ⚠️ 重裝時**不要刪 App**，而且 **bundle ID 不能變**（AltStore 要關掉「Randomize Bundle IDs」），否則 70GB 遊戲資料會不見。

**IPA 從哪來（不用自己的 Mac）：**
- 官方 repo 有 GitHub Actions 工作流程 `.github/workflows/release.yml`（「Experimental IPA (manual)」）。
  - 在 GitHub 的 **macos-26 雲端機器**上，從指定標籤建置 `Tolkara-unsigned.ipa`，模式是 External JIT。
  - 只能手動觸發，不會自動公開發布。
- 作法：**Fork jklock/wolkaraforever 到自己的 GitHub → Actions → 手動執行 → 從自己的 Release 下載 IPA**。
  - 原始碼公開、在自己的帳號裡建置，比下載陌生人的 IPA 安全。
  - #67 的使用者就是這樣做的（「Build: GitHub Actions, TOLKARA_SYSTEM_ROOTS=YES」）。
- 這版 IPA 會自己下載遊戲（WolkaraForever 啟動器），不需要 Mac 上的遊戲副本。

**其餘需求：**
- iPad 開發者模式（iPad 上就能開，不一定要 Mac）。
- JIT 啟用工具 **StikDebug** 加 **LocalDevVPN**，以及配對檔。使用者 iPhone 上已有 LocalDevVPN 和配對檔的經驗，見 memory `iphone-sideload-setup`。
- iPad 要裝 SideStore（或在 Windows 用 AltStore Classic）。

**免費帳號的限制：**
- 每 7 天要重新整理簽名（SideStore 可以自動）。
- 同時只能有 3 個側載 App（SideStore、StikDebug、WolkaraForever；GetMoreRam 用完可以刪）。
- 每 7 天最多註冊 10 個 App ID。

**風險和未知：**
- External JIT 在 **iPad** 上的實測仍少，成功案例是 iPhone。
- iPad mini 8 約 12GB RAM，拿到權限後的上限應該 ≥ 6GB，比 iPhone 16 Pro Max 寬裕，**但要實測**。
- 每次開遊戲都要先用 StikDebug 開 JIT，比官方路線麻煩。
- 封號風險和官方路線一樣。

➡️ **iPad 端完整執行步驟與前置軟體：[IPAD-FREE-ROUTE.md](IPAD-FREE-ROUTE.md)**

**結論：** 這條路值得**在借到 Mac 前先試**。失敗了也只是花時間，不花錢。成功的話就不用付 US$99 年費。

## 專案與來源

| 專案 | 角色 | 連結 |
|------|------|------|
| Tolkara | 底層：在 iPadOS 上載入**未修改的 arm64 macOS 程式**並轉譯 API | https://github.com/tolkara/tolkara |
| WolkaraForever（jklock，上游） | WoW 永恆專用：在 iPad 上**自己下載、驗證、更新**遊戲，含觸控、鍵盤、觸控板操作 | https://github.com/jklock/wolkaraforever |
| WolkaraForever（pookee fork） | 針對 iPhone 調整 | https://github.com/pookee/wolkaraforever |
| Wolkara（Jose10Espinoza） | WoW 版 Tolkara fork，用 Xcode 建置 | https://github.com/Jose10Espinoza/wolkara |
| 安裝說明 | 主要依據 | https://github.com/jklock/wolkaraforever/blob/main/docs/INSTALLATION.md |
| AltStore IPA 流程 PR | 本機打包 IPA 的工作流程（可參考） | https://github.com/jklock/wolkaraforever/pull/3 |
| 影片教學 | Tolkara 安裝 WoW 永恆 | https://www.youtube.com/watch?v=2bV4raILFp4 |
| 原始 Reddit 文章 | 使用者提供（Claude 無法讀取 reddit） | https://www.reddit.com/r/classicwow/comments/1wuyw0p/you_can_play_forever_natively_on_ipad/ |

其他 fork（未細看）：robinebers、akauper、Morv、post-ai、zippyy、andrewfblack 的 wolkaraforever。
相容性文件：https://github.com/jklock/wolkaraforever/blob/main/COMPATIBILITY.md 、 https://github.com/tolkara/tolkara/blob/main/COMPATIBILITY.md
Release 列表：https://github.com/jklock/wolkaraforever/releases

### 現成 IPA（目前**不建議**使用）

- **Tolkara 官方 `Tolkara-unsigned.ipa`**
  - 由 v0.2.1 的 GitHub Actions 建置：https://github.com/tolkara/tolkara/releases/tag/v0.2.1
  - 走「External JIT」模式，用 SideStore 或 LiveContainer 自行簽名。
  - 官方 README 寫明 External JIT「尚未在實機跑過」。
  - 官方版**不會自己下載遊戲**：要你提供 macOS 版 WoW，而且要先在 Mac 上開過一次（存好地區），再複製過去。
- **個人 fork 的「iPad Experimental Build」**
  - 來源：https://github.com/jameslewislee123-pixel/wolkaraforever/releases/tag/v0.0.1-ipad-test
  - 個人帳號發布，沒有 SHA-256 檢查碼，內容無法驗證。
  - 在裡面輸入 Battle.net 帳密有被盜的風險，**不要用**。

---

## 需求清單（依 WolkaraForever 文件）

- [ ] **Apple 晶片 Mac**（M1 以上），裝好最新 Xcode、Xcode Command Line Tools、XcodeGen、Python 3
- [ ] **付費 Apple Developer Program 會員**
  - 免費帳號（Personal Team）拿不到 tunnel 與記憶體相關權限：increased-memory-limit、extended-virtual-addressing
- [ ] **iPad**：開發者模式已開、已信任該 Mac、可用空間 ≥ 70GB
  - 官方實測機是 iPad Pro (M5) 加 iPadOS 27
  - 文件沒寫最低晶片或 RAM，越新越好
- [ ] **自己的 WoW 帳號**，要有永恆的遊玩資格（使用者已有，台灣區帳號）
- [ ] 穩定 Wi-Fi：「開發者服務」模式在行動網路下需要文件中的恢復步驟

### 待確認事項

- [x] 開發用 iPad：**iPad mini 8（2026）**，評估見〈開發機：iPad mini 8〉
- [x] iPad mini 8 容量：**256GB** ✅（使用者 2026-11-15 確認）
- [x] iPad mini 8 系統：**iPadOS 27** ✅（使用者確認，與官方實測版本相同）
- [ ] 語言與地區：WolkaraForever 文件只列英、西、德三種遊戲語言，**沒有繁中（zhTW）**；地區選 Blizzard CDN 區域。
  - 使用者帳號是台灣區（Linux 端裝的是 zhTW，CDN 為 kr），要確認能否選台灣或亞洲區。
- [ ] 動工時重新看各 repo 最新版：專案更新很快，fork 很多

---

## 開發機：iPad mini 8（2026）

2026-11-15 查詢。來源：MacRumors、AppleInsider、Tom's Guide、Mark Ellis Reviews。

| 項目 | 規格 | 對本專案的影響 |
|------|------|----------------|
| 晶片 | **A20 Pro**（2nm，與 iPhone 18 Pro 同款），5 核 CPU、7 核 GPU（128/256GB 款） | arm64，可以跑 macOS arm64 程式，架構沒問題 |
| RAM | 約 **12GB**（媒體報導，Apple 不公布） | 和實測的 iPad Pro M5 同一級距；需要付費帳號提供的 increased-memory-limit 權限 |
| 螢幕 | 8.5 吋 OLED，2316×1512，60Hz（無 ProMotion） | 介面偏小，可能需要調 UI 縮放 |
| 其他 | Wi-Fi 7、IP67、建議售價 US$699 | Wi-Fi 7 對「開發者服務」模式的連線有利 |
| 容量 | **256GB**（使用者確認） | 足夠放永恆（約 49–70GB） |
| iPadOS | **27**（使用者確認） | 和官方實測（iPad Pro M5 + iPadOS 27）同一版 ✅ |

### 相容性評估

- ✅ **架構**：A 系列和 M 系列都是 Apple 晶片 arm64，Tolkara 原理一樣能用。
- ⚠️ **沒有實測紀錄**：WolkaraForever 和 Tolkara 文件都**沒提到 iPad mini**。
  - 也沒有 A17、A18、A19、A20 的測試結果。
  - 實機測過的只有 iPad Pro (M5)、iPhone 16 Pro Max、iPhone 15 Plus (A16)，以及 WolkaraForever 的 iPhone Duo。
  - 所以使用者這台會是首批 A20 Pro iPad 的測試者。
- ⚠️ **BC 壓縮貼圖**：macOS 版遊戲用 BC（DXT）貼圖，只有部分 iOS GPU 能直接讀取。
  - A16 不支援，要改存成未壓縮格式，佔用 2 到 8 倍的貼圖記憶體。
  - 一般認為 A17 Pro 以後的 GPU（Apple GPU family 9）支援 BC，**未經文件證實**，要實機確認。
  - 如果被迫走未壓縮格式，12GB RAM 會很吃緊。
- ✅ **儲存空間**：使用者的 iPad 是 **256GB**，夠用。
  - 目標版本**只有魔獸世界永恆**，不裝正式服或經典版。Linux 端實際安裝是 49GB（`_forever_`，1.60.1）。
  - WolkaraForever 文件建議預留約 70GB，含 macOS 版本體、更新暫存和快取。
  - 開工前先清出 **≥ 70GB 可用空間**，比較保險。
- ⚠️ **未解問題（iPad Pro M5 也有）**：Tolkara 記錄「開發者服務」模式在 iPad 上跑 6 到 8 分鐘後會沒有任何錯誤報告就結束，**調查中**。動工前先看這個問題修好沒。
- ℹ️ **小螢幕操作**：
  - v1.0.14 起觸控控制器是正式功能，但只在 iPad Pro 13 吋模擬器上驗證過。
  - 8.5 吋可能要調 UI 縮放，或改接藍牙鍵盤和觸控板。
  - Tolkara 曾記錄角色選擇畫面的頂部選單過大、位置跑掉（iPad Pro M5 跑 WoW 經典版時）。
- ℹ️ **介面模式**：v1.0.10 有 Automatic、iPadOS、iOS、iOS on Duo 四種，iPad mini 應該會自動選 iPadOS。

### 專案最新狀態（2026-11-15 查）

- WolkaraForever 最新版 **v1.0.17**（2026-11-14，「Integration build repair」，官方說要裝 v1.0.17 不要裝 v1.0.16）。
- 近期版本：
  - v1.0.16：Add-on Hub（插件中心）
  - v1.0.14：觸控控制器
  - v1.0.0：2026-10-22
- 更新非常頻繁，動工時要重新看 release notes。
- 語言：已有英、西、德、法。**仍然沒有 zhTW 或台灣、亞洲地區的資訊**，動工時要確認。

## 補充研究（2026-11-15 第二輪）

### ① 借 Mac 的硬性條件（Xcode 27）

- **一定要 Apple 晶片的 Mac**（M1 以上）。Xcode 27「只能在 Apple 晶片 Mac 上安裝執行」，Intel Mac 不行。
- **macOS Tahoe 26.6 以上**（Xcode 27 的最低需求）。借之前先確認那台 Mac 能升到 26.6。
- iPadOS 27 要用 **Xcode 27**（附 iPadOS 27 SDK）建置部署。
  - 目前最新是 Xcode 27.1（2026-10-15，build 27A9275）。
  - Xcode 本體加 iOS 平台元件大約要 **30–40GB 空間**，借的 Mac 要留夠（此數字為估計）。
- **Xcode 26 行不行？**（2026-11-16 查）
  - 官方版本表：Xcode 26 只支援到 iOS/iPadOS 26，Xcode 27 支援到 27。
  - Apple DTS 在論壇說「用 Xcode 26 在 27 系統上執行 App 不受支援」，但有開發者回報可以跑。
  - 專案沒有指定 Xcode 版本（「current Xcode」）。
    - Tolkara 主程式的 deploymentTarget 是 iOS 17.0，ProcessProbe 是 26.2，Swift 5.0。
    - install_prerequisites.sh 只檢查 xcodebuild 與 devicectl 存不存在，不檢查版本。
  - 結論：**用 Xcode 27**。所有 M 系列 Mac 都能升到 Tahoe 26.6，升級後就能裝。只有借來的 Mac 無法升級時，才試 Xcode 26 加 iPadOS 27（不受支援，devicectl 和裝置配對最可能出問題）。
  - 來源：https://developer.apple.com/support/xcode/ 、 https://developer.apple.com/forums/thread/836048
- 不用一直借著：建置完成後，App 在 iPad 上可用 1 年（付費帳號描述檔效期），到期再借 Mac 重簽即可。
  - 但專案更新很頻繁，想升級新版也需要 Mac。

### ② Apple Developer Program（台灣個人申請）

➡️ **完整申請步驟見 [APPLE-DEVELOPER-ENROLL.md](APPLE-DEVELOPER-ENROLL.md)**


- 年費 **US$99**。Apple 以當地貨幣計價，台灣約 NT$3,200 上下，以官網結帳金額為準。
- 條件：
  - Apple 帳號已開**雙重認證**、已成年。
  - 個人申請以**法定姓名**登記（會顯示為 App 銷售者），姓名填錯會延誤審核。
- **信用卡要開通海外、網路刷卡**：台灣卡常因此付款失敗。
- 審核：第三方經驗是約一週內（非官方承諾）。可以**在借到 Mac 前先申請**，申請不需要 Mac，用 iPhone 的 Apple Developer App 或網頁就能辦。
- 官方說明：https://developer.apple.com/tw/help/account/membership/program-enrollment 、 https://developer.apple.com/tw/support/enrollment/

### ③ 已知問題：永恆一啟動就閃退（Forever CTD）— ✅ v1.0.2 起已修好（見 2026-11-17 更新）

- 回報：https://github.com/fJavierLasso/wolkara/issues/13 （**仍開啟，維護者沒回應**；jklock/wolkaraforever#22 也是同一問題）
  - 原始回報：iPad Pro M5、**iPadOS 27.2**，用「開發者服務」模式。
  - iPhone Duo（iOS 27.2/27.3）也有人重現。
- 症狀：第一個畫面出現前就崩潰（libsystem_pthread 空指標）。Tact.log 在崩潰前會出現 `Server: 4294967295`，代表沒選到 CDN 伺服器。
- **社群解法（已有人確認有效）**：手動編輯遊戲資料夾裡的 `.build.info`。
  1. 在欄位標頭 `CDN Hosts!STRING:0` 後面加上 `CDN Servers!STRING:0` 欄位。
  2. 填入該地區的 CDN 伺服器清單，來源是 `http://us.patch.battle.net:1119/wowf/cdns`。
  - 有人用美區（client 1.60.1.70862）照這樣改之後，記憶體準備完成並進到登入畫面。
- 參考檔案已存在 `reference/`：
  - `linux-forever-build.info`：Linux 這邊 Battle.net 產生的正確 `.build.info`，**已經含 CDN Servers 欄位**（台灣帳號走 `kr` CDN），格式可以直接照抄。
  - `wowf-cdns.txt`：Blizzard 官方的 wowf CDN 清單，有 us、eu、cn、kr、**tw** 五區。
  - `wowf-versions.txt`：各區版本號。2026-11-15 **全部都是 1.60.1.70938**，遊戲資料各區相同。

### ④ 地區與語言（台灣帳號）

- Blizzard 的 wowf 有 **`tw` 區**，CDN 和美區相同（level3、us.cdn）。
  - Linux 這邊 Battle.net 幫台灣帳號選的是 `kr` CDN，`.build.info` 的 Tags 是 `zhTW`、`acct-TWN`。
- WolkaraForever 文件說首次啟動要選「Forever、地區、遊戲語言」。
  - 語言目前只看到英、西、德、法。
  - **沒有任何文件提到 tw、kr 地區或 zhTW**；FEATURES.md 已 404，無法確認地區清單。
- 推測（未驗證）：
  - 遊戲資料各區相同，所以下載選哪一區都可以。
  - 真正影響的是登入入口（portal）：台灣帳號要連 TW/KR 的伺服器（Linux 紀錄是 realm 94-2-2、subRegion 94-2-89）。
  - 如果 App 只能選美區或歐區，可能要像 CTD 解法那樣**手動改 `.build.info` 和 Config.wtf 的 `portal` 設定**，讓它連亞洲區。
- 中文顯示：
  - Linux 版遊戲是 zhTW 介面。macOS 版用 zhTW 語言包應該也行，但 App 沒提供這個選項。
  - 最差情況：英文介面加台灣伺服器，實際能不能這樣登入要動工時確認。

### ⑤ iPadOS 27 記憶體

- 有使用者在 iPadOS 27 beta 回報：16GB 的 iPad Pro M4，App 可用記憶體只剩約 5.33GB，懷疑 increased-memory-limit 權限沒生效（未獲回覆）。
  - 來源：https://forum.nomadsculpt.com/t/ipados-27-beta-available-memory-drops-to-5-33-gb-on-m4-ipad-pro-1tb-16-gb-ram/24862
- Apple 論壇也有 Xcode 27 加 iOS 27 記憶體用量偏高的回報。
- 對 iPad mini 8（約 12GB）的意義：
  - 正式版 iPadOS 27 實際能給 App 多少記憶體，要用付費帳號簽了 increased-memory-limit 之後**實機量測**。
  - 這是最大的未知數。WoW 永恆在 Linux 這邊跑時，常駐記憶體約 3.7GB（實測 RSS）。

### ⑥ 其他實機紀錄（jklock/wolkaraforever）

- v1.0.3：下載中斷自動重試（#36 修正 iPad 首次安裝時 CDN 逾時）。
- PR #48：在 iPad Pro 12.9 吋（第 5 代，M1）上，啟動器到了「Ready to play」，沒有新的崩潰。**M1 iPad 也能走到這步，對 A20 Pro 是好消息。**
- PR #41、PR #11：早期版本在實體 iPad 上啟動就 SIGABRT 或第一個指令崩潰，後續版本已處理。

## 動工步驟（借到 Mac 後）

0. **借 Mac 前就能做**：申請 Apple Developer Program（見補充②）；確認信用卡已開通海外刷卡；iPad 清出 ≥ 70GB。
1. **確認借到的 Mac**：Apple 晶片，macOS ≥ Tahoe 26.6，可用空間 ≥ 60GB（Xcode 27 加 iOS 平台元件，估計值）。
2. **Mac 準備**：
   ```bash
   xcode-select --install
   # 從 App Store 裝 Xcode，開一次並同意授權
   brew install xcodegen python3
   ```
3. **iPad 準備**：設定 → 隱私權與安全性 → 開發者模式 → 開啟，重開機。用 USB 接上 Mac 並按「信任」。
4. **取得原始碼**：
   ```bash
   git clone https://github.com/jklock/wolkaraforever.git
   cd wolkaraforever
   ```
   先讀 `docs/INSTALLATION.md` 的最新版。以下腳本名稱來自文件，以 repo 實際內容為準。
5. **依文件執行**：`install_prerequisites.sh` → `device_variables.sh`（填 Team ID、裝置 UDID）→ `preflight.sh` → `install.sh`
   - 在 Xcode 的 Signing 選付費 Team。
6. **在 iPad 上**：開 WolkaraForever → 選 Forever、CDN 區域、語言 → 讓它下載約 70GB → 用自己的 Battle.net 帳號登入。
   - 一啟動就閃退時，照補充③修 `.build.info`。
   - 連不到台灣伺服器時，看補充④。
7. **簽名效期**：付費帳號的描述檔一年有效，到期要重新在 Mac 上簽；免費帳號是 7 天。

---

## 日後更新：什麼時候需要 Mac

| 情況 | 需要 Mac？ | 說明 |
|------|-----------|------|
| 遊戲一般更新、修正檔 | ❌ 不用 | WolkaraForever 會在 iPad 上直接向 Blizzard CDN「下載、驗證、更新」遊戲 |
| WolkaraForever / Tolkara 升級新版 | ✅ 要 | 只有原始碼，每版都要在 Mac 上用 Xcode 重新建置安裝；更新很頻繁，但不用每版都裝 |
| 遊戲大改版，新版用到專案還不支援的功能 | ✅ 要（等作者修好後） | 更新完可能打不開，要等新版 App 再用 Mac 重裝 |
| 簽名到期（付費帳號一年） | ✅ 要 | 到期前接 Mac 重簽，否則 App 打不開 |

預期模式：平常 iPad 自己更新自己玩；遇到大改版打不開，或者滿一年，就借一次 Mac（約一到兩小時）。

## 為什麼現在做不了（2026-11-15 評估）

1. 建置和安裝腳本都在 macOS 上跑，沒有 Linux 或 CI 的建置途徑。
2. 免費 Apple ID 會失去大記憶體權限，WoW 這種大型程式很可能放不進去。
3. 不用 Mac 的 External JIT 加官方 IPA 這條路，官方自己說尚未實機驗證，而且遊戲本體仍然要從 Mac 複製。

---

## 風險（務必先知道）

- Tolkara 官方原文：**「使用線上帳號時，被停權或封號的風險是真實的，而且完全由你承擔。」**
- WolkaraForever：「Blizzard 不支援也不認可本專案，能執行不代表帳號安全。」
- 遊戲裡不要搭配任何外掛、腳本或自動化工具；專案政策也明確拒絕反作弊繞過。

---

## 備案：串流（現在就能做，免費）

這台 Linux 電腦已經能跑 WoW 永恆，見 `~/WOW-BNET-CHANGELOG.md`。
- 電腦端裝 **Sunshine**，UHD 620 用 VAAPI 硬體編碼。
- iPad 端從 App Store 裝 **Moonlight**。
- 優點：有繁中，沒有封號風險，不需要 Mac。
- 缺點：電腦要開著，順暢度跟電腦一樣。

使用者目前選擇等 Mac 走原生路線；串流是隨時可以啟用的備案。

---

## 相關背景

- 使用者的 iPhone 側載環境（SideStore、LiveContainer、Dopamine，免費 Apple ID team <IPHONE_TEAM_ID>）：見 Claude memory `iphone-sideload-setup`。
  - 免費帳號有 3 個 App 的上限，不能直接套用到這個專案。
- Linux 端的 WoW 設定與除錯紀錄：`~/WOW-BNET-CHANGELOG.md`。
