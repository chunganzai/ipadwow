# iPad 自動重簽（防止 7 天過期）

免費 Apple ID 簽的 App 7 天就會失效。這裡的工具會每小時檢查一次，快到期時自動用 iloader 重簽，不行就跳桌面通知提醒。

## 怎麼運作
- `systemd --user` 的 `ipad-resign.timer` 每小時執行一次 `resign.py`（開機 5 分鐘後也會跑一次）
- `expiry.py` 用 `ideviceprovision` 讀 iPad 上每個 App 的簽名到期日，結果快取在 `~/.local/state/ipad-resign/last.json`
- 剩 **2 天內**到期時：
  - **iPad 有接上：** 自動操作 iloader 視窗（「匯入 IPA」→ 選 `apps.conf` 裡的 IPA），重簽後再讀一次到期日確認成功，然後跳「重簽完成」通知
  - **iPad 沒接上：** 每 6 小時跳一次提醒；剩不到半天時每小時提醒
- 重簽是覆蓋安裝，App 的資料（遊戲檔、StikDebug 配對檔、Config.wtf）都會保留

## 自動重簽的條件（不符合會跳通知說明原因）
- 電腦螢幕沒有鎖定
- iloader 已開啟，而且已用 iPad 的 Apple ID 登入。沒開的話會自動開，但登入要自己按
- iloader 視窗會被最大化（按鈕位置依 1920x1008 的版面）
- 重簽時 iPad 上的 Tolkara 會被關掉，不要在遊戲中途接上電腦

## 指令
```bash
~/ipadwow/resign/resign.py --status   # 看到期日（iPad 沒接時顯示上次紀錄）
~/ipadwow/resign/resign.py            # 照規則檢查一次
~/ipadwow/resign/resign.py --force    # 現在全部重簽
journalctl --user -u ipad-resign -n 20   # 看排程紀錄；另有 ~/.local/state/ipad-resign/resign.log
systemctl --user disable --now ipad-resign.timer   # 停用
```

## 檔案
| 檔案 | 用途 |
|------|------|
| `apps.conf` | 要重簽的 App 和 IPA 路徑；換新版 IPA 時改這裡 |
| `expiry.py` | 讀 iPad 的到期日 |
| `resign.py` | 判斷、提醒、操作 iloader |
| `xctl.py` | X11 截圖、點擊、打字的小工具 |
| `systemd/` | `ipad-resign.service`、`ipad-resign.timer` 的副本（實際在 `~/.config/systemd/user/`） |

## 之後可以改進
- iloader 沒有指令列模式，所以現在是操作視窗。若改用它底層的 Rust 函式庫 `isideload` 寫成指令列工具，就不需要螢幕解鎖或 iloader 開著。這需要安裝 Rust（`rustup`），自動模式擋下了由 Claude 下載執行安裝程式，要使用者自己同意或執行
