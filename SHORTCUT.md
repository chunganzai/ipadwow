# 主畫面一鍵啟動 Tolkara（免費帳號）

前提：LocalDevVPN 保持連線（設定 → VPN 開著）。StikDebug 裡 Tolkara 已用 Assign Script 指定 universal.js。

## A. 捷徑 App 的 StikDebug 動作（優先）
1. 開「捷徑」App → 右上 **＋** 新增捷徑
2. 搜尋動作 **StikDebug** → 選 **Enable JIT**
3. 點 **App** 參數 → 選 **Tolkara**
4. 頂端名稱改「WoW」→ 分享（或名稱旁選單）→ **加入主畫面** → 可換圖示 → 加入

## B. 網址方式（A 沒有 StikDebug 動作或不能用時）
1. 新增捷徑 → 動作 **打開 URL**
2. 網址填：
   `stikjit://enable-jit?bundle-id=local.tolkara.app.<TEAM_ID>&script-name=universal.js`
3. 加入主畫面，同 A 第 4 步

## 說明
- 網址參數（`enable-jit`、`bundle-id`、`script-name`）和 `EnableJITIntent` 動作是從 StikDebug 3.2.2 的程式內容找到的，2026-11-18 待實測
- 測試成功的判斷：`wolkaraforever.log` 出現 `an arena was reserved at launch`
- 重簽後 bundle ID 不變，捷徑應該不用重做
