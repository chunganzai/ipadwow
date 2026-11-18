# 借到 Mac 後的完整安裝步驟（官方「開發者服務」路線）

整理日期：2026-11-17。依據 jklock/wolkaraforever 官方文件（docs 驗證版本 `3c33543`，2026-11-13）、
`local.env.example`、本專案蒐集的已知問題。官方文件原文備份在 `reference/upstream/`。
**動工當天先重看官方 INSTALLATION.md 和 Releases**：專案幾乎每天更新，指令可能改。

> 如果決定走「不用 Mac」的新路線（免費 Apple ID 加 External JIT），看 README 的〈2026-11-17 更新〉，不用這份。

---

## 0. 出發前檢查（在家就能做）

- [ ] Apple Developer Program 已通過，記下 **Team ID**（10 碼），見 APPLE-DEVELOPER-ENROLL.md
- [ ] iPad mini 8：iPadOS 27、可用空間 ≥ 70GB、電量充足，帶 **USB-C 傳輸線**
- [ ] 借的 Mac：**Apple 晶片（M1 以上）**、可升級到 **macOS Tahoe 26.6 以上**、可用空間 ≥ 60GB，你有管理員權限
- [ ] 網路穩定（Xcode 約 10GB 以上要下載；遊戲約 70GB 之後在 iPad 上用 Wi-Fi 下載，不經過 Mac）
- [ ] 預留時間：第一次大約 **2–3 小時**（大部分在下載 Xcode）

---

## 1. Mac 端：準備開發環境

1. **更新 macOS**：系統設定 → 一般 → 軟體更新，升到 26.6 以上。
2. **安裝 Xcode 27**：App Store 搜尋 Xcode → 安裝 → 開一次，同意授權並讓它裝完額外元件。
   - 第一次開啟時勾選 **iOS 平台**（iOS 27 SDK）。
3. **安裝命令列工具和 Homebrew**（打開「終端機」）：
   ```sh
   xcode-select --install
   sudo xcodebuild -license accept
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install xcodegen python git
   ```
   - 裝完 Homebrew 後，照畫面提示把 brew 加進 PATH（`eval "$(/opt/homebrew/bin/brew shellenv)"`）。
   - 官方要求 Python 3.9 以上。
4. **Xcode 登入開發者帳號**：Xcode → Settings → Accounts → 「＋」→ Apple ID，登入付費會員的帳號。
   - 確認 Team 顯示你的名字，以及 **(Individual)**，不是 Personal Team。

---

## 2. iPad 端：開啟開發者模式並信任 Mac

1. 用 USB-C 線把 iPad 接上 Mac，iPad 解鎖 → 跳出「要信任這部電腦嗎？」→ **信任**，輸入密碼。
2. 開發者模式：
   - iPad 設定 → **隱私權與安全性** → 最下面 **開發者模式** → 開啟 → 重新開機 → 開機後按「開啟」並輸入密碼。
   - 如果找不到「開發者模式」選項：先在 Mac 上開 Xcode → Window → **Devices and Simulators**，讓 Xcode 認到 iPad 一次，選項就會出現。
3. 在 Xcode 的 Devices and Simulators 裡確認 iPad 顯示為已連線、沒有錯誤（第一次會「準備裝置」幾分鐘）。

---

## 3. 下載原始碼並設定

```sh
cd ~
git clone https://github.com/jklock/wolkaraforever.git
cd wolkaraforever
git checkout v1.0.17      # 或當天最新的 release 標籤；官方說 v1.0.17 不要裝 v1.0.16
cp local.env.example local.env
open -e local.env         # 用文字編輯器打開
```

在 `local.env` 填入：

| 變數 | 要填的值 | 說明 |
|------|----------|------|
| `DEVELOPMENT_TEAM=` | 你的 **Team ID**（10 碼） | Xcode → Settings → Accounts，或 developer.apple.com → Membership |
| `TOLKARA_BUNDLE_ID=` | 例如 `tw.<USER>.wolkaraforever` | **必須全世界唯一**（一個 bundle ID 只能註冊給一個 Team）。**之後永遠不要改**，改了就等於裝一個新 App，遊戲資料要重新下載 |
| `TOLKARA_KEYCHAIN_GROUP=` | 例如 `tw.<USER>.wolkaraforever.authorization` | 選填，但**定了就不要改**：改了要重新做本機授權（enrollment） |
| `TOLKARA_MODE=` | 保持 `developer-service` | 官方整合版只支援這個模式 |
| `DEVICE=` | 先留空 | 下一步的腳本會自動寫入 |

> ⚠️ 把 `local.env` 另外備份一份（例如存到 USB 隨身碟或傳回這台 Linux 的 `~/ipadwow/`）。
> 日後更新或重簽時要用**完全相同**的設定，否則 iPad 上的 App 會被當成新 App。
> 備份裡只有 Team ID 和 bundle ID，不含密碼或憑證。

---

## 4. 檢查、選裝置、預檢

在 `wolkaraforever` 資料夾裡執行（官方文件寫的路徑是 `wolkaraforever/tools/...`；如果提示找不到檔案，改成 `tools/...` 或回上一層執行）：

```sh
wolkaraforever/tools/install_prerequisites.sh --check   # 檢查 Xcode、devicectl、XcodeGen、Python
wolkaraforever/tools/device_variables.sh --write        # 偵測已連接的 iPad，寫入 local.env 的 DEVICE
wolkaraforever/tools/preflight.sh                       # 檢查簽名身分、裝置、開發者模式
```

| 問題 | 處理 |
|------|------|
| prerequisites 檢查失敗 | 照提示安裝缺的工具，再跑一次 `--check` |
| 找不到裝置 | iPad 解鎖 → 重插線 → 確認已信任、開發者模式已開 → 再跑 `device_variables.sh --write` |
| 簽名失敗 | 在 Xcode 修正選到的簽名身分（Team），再跑 `preflight.sh` |

---

## 5. 建置並安裝

```sh
wolkaraforever/tools/install.sh
```

- 它會自動 **建置 → 簽名 → 安裝 → 啟動** App，並做安全檢查。
- 第一次建置要比較久（十幾分鐘級）。
- 如果 iPad 上遊戲正在執行，它會拒絕覆蓋 → 先在 App 裡停止遊戲再重跑。
- 官方警告：**不要用其他方式手動複製 App 或遊戲檔案到 iPad。**
- 如果 iPad 提示「未受信任的開發者」：iPad 設定 → 一般 → **VPN 與裝置管理** → 點你的開發者帳號 → 信任。（官方文件沒寫這步；用付費帳號經 Xcode 安裝通常不會出現，列出來以防萬一。）
- 「開發者服務」模式會用到 App 自己的 VPN 式通道：第一次啟動若跳出「要加入 VPN 設定」→ **允許**。

---

## 6. iPad 上第一次啟動

1. 開 WolkaraForever 主畫面 → 選 **Forever**、**地區**、**遊戲語言**。
   - 地區：先看有沒有台灣 / 亞洲可選（見 README〈地區與語言〉）。目前官方語言只看到英、西、德、法。
2. 按下載（約 70GB，用 Wi-Fi，iPad 保持亮著、接電源）。中斷可以續傳、驗證、修復，**不要刪 App 重來**。
3. 等啟動器顯示**就緒（ready）**才按 **Play**。
4. 第一次會做「記憶體準備」（開發者服務模式每次啟動約每秒 3MB 準備可執行記憶體）——等它跑完。
5. 進遊戲後先到 **系統 → 圖形** 調低（iPad mini 螢幕小、記憶體有限）；必要時 **Launcher Manager → Interface** 選 **iPadOS**（或 Automatic）。
6. 登入：用自己的 Battle.net 帳號。
   - 若出現 **BLZ51914440**（被斷線）：Blizzard 越來越要求透過啟動器登入，issue #47 有人做了「經 battle.net 網頁登入再交給遊戲」的替代機制（PR 進行中），屆時看是否已合併。
   - 若出現 **BLZ51900003**（帳密錯誤）：可能是地區設定不對，不一定是密碼錯。

---

## 7. 安裝完成後（離開 Mac 前）

- [ ] 在 iPad 上確認能進到角色畫面
- [ ] 抄下 `git rev-parse HEAD` 的 commit，記在 README
- [ ] 備份 `local.env`
- [ ] 記下簽名到期日（付費帳號約一年；Xcode → Settings → Accounts → Manage Certificates 可看）
- [ ] **不要刪 App**：刪了會連 70GB 遊戲資料一起刪

---

## 8. 日後更新 App（需要 Mac）

```sh
cd ~/wolkaraforever
git fetch --tags && git checkout <新的版本標籤>
# 放回同一份 local.env
wolkaraforever/tools/install.sh     # 用相同設定重跑即可，會保留遊戲資料與授權
```

遊戲本身的更新在 iPad 上的 App 裡就能做，不需要 Mac（見 README〈日後更新〉）。

---

## 求助時

- iPad App 內 **Settings → Technical details** 記下確切訊息。
- 只在被要求時才分享**去識別化的 log**；不要分享帳密、配對資料、簽名資料、裝置識別碼。
- 回報處：https://github.com/jklock/wolkaraforever/issues
