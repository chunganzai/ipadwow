# Apple Developer Program 申請步驟（台灣個人）

> 🗄 **備案文件**：免費 Apple ID 已能取得 increased-memory-limit，不一定要付費。付費的好處是簽名一年有效、可用 Developer service 模式（不需要 StikDebug），見 [README.md](README.md)〈付費帳號能多什麼〉。


整理日期：2026-11-17。依 Apple 官方說明頁整理，來源見文末。
用途：讓 WolkaraForever 能取得 increased-memory-limit、tunnel 等權限，並把 App 簽名效期延長到一年。
**申請不需要 Mac**，用 iPhone 或網頁就能辦，建議借到 Mac 之前先申請好。

---

## 一、事前準備（先檢查，最常卡在這裡）

- [ ] **Apple 帳號已開啟雙重認證**
  - iPhone：設定 → 你的名字 → 登入與安全性 → 雙重認證
- [ ] **已滿 18 歲**（所在地區的法定成年年齡）
- [ ] **帳號資料正確且是最新的**：姓、名、地址、電話、受信任的電話號碼、受信任的裝置
  - 地址**不能是郵政信箱**
- [ ] **法定姓名**
  - 個人申請時，姓名會以「銷售者」名義顯示在 App Store。**不能用暱稱、別名或公司名**，填錯會延誤審核。
  - 建議用**護照上的英文姓名**，並和信用卡持卡人姓名一致。
- [ ] **身分證件**：準備**護照**。Apple 寫「多數地區接受護照」，台灣身分證不一定接受。
- [ ] **付款方式**：信用卡要用**自己名下的卡**
  - 網頁申請時，用別人的卡會被要求補身分證件，延誤審核。
  - **開通海外刷卡和網路交易**，而且要能刷美元（Apple 要求「可用 USD 扣款的信用卡」）。
  - 用 App 申請時，扣款走 Apple 帳號裡的付款方式。**Apple 帳號餘額和禮品卡不能用。**
- [ ] 費用：**US$99／年**，結帳時會以當地貨幣顯示，台灣約 NT$3,200 上下，以結帳畫面為準；另依地區加稅。

---

## 二、方法 A：用 iPhone 上的 Apple Developer App（推薦先試）

> ⚠️ 只有「部分地區」開放用 App 申請，官方說明頁沒列出台灣有沒有開放。
> 如果在 App 裡找不到「立即註冊」(Enroll Now)，就改用方法 B。

**條件：**
- iPhone 或 iPad 已設定 Face ID、Touch ID 或密碼。
- **整個流程都在同一台裝置上完成。**
- 已安裝最新版 Apple Developer App（App Store 免費下載）。
- 這台裝置已登入 iCloud。

**步驟：**
1. 開啟 **Apple Developer** App → 點下方的 **帳號 (Account)** 分頁 → 用你的 Apple 帳號登入。
2. 如果出現 Apple Developer Agreement，看完後點 **同意 (Agree)**。
3. 點 **立即註冊 (Enroll Now)** → 看完權益說明 → **繼續 (Continue)**。
4. 依要求填寫**名字、姓氏、電話**，用護照上的英文拼法。
5. **驗證身分**：用相機拍**護照**照片頁。
   - Apple 會檢查真偽，並讀取姓名和地址。
   - Apple 表示不會保存這張照片。
6. 確認資料 → **繼續** → 選擇 **個人 (Individual)** → 看完 Program License Agreement → **同意**。
7. 確認訂閱內容和價格（會顯示台幣）→ **訂閱 (Subscribe)**，用 Face ID 付款。
8. 完成後會收到確認信。

---

## 三、方法 B：用網頁申請

1. 用電腦或手機瀏覽器打開 https://developer.apple.com/programs/enroll/ → **Start your enrollment**（開始註冊）。
2. 用 Apple 帳號登入，完成雙重認證。
3. 選 **個人 (Individual / Sole Proprietor)**。**不需要 D-U-N-S 編號**，那是公司申請才要的。
4. 填寫個人資料：英文姓名、地址、電話，和護照、信用卡一致。
5. 看完並同意 Program License Agreement。
6. **付款**：用**自己的信用卡**（已開海外和網路刷卡、可刷美元）。
7. 付款後會收到確認信，信裡有 **Enrollment ID**，**請保留**。
8. **24 小時內沒收到會員確認信**，就帶著 Enrollment ID 聯絡 Apple Developer Support：https://developer.apple.com/contact/
   - 經驗上審核時間從幾小時到約一週都有，官方沒有承諾時間。

---

## 四、申請通過後要做的事

- [ ] 登入 https://developer.apple.com/account → **會員資格 (Membership)** → 記下 **Team ID**（10 碼英數）。
  - WolkaraForever 的 `device_variables.sh` 會用到。
- [ ] 確認會員狀態是 Active，到期日大約一年後。
- [ ] 把 Team ID 和到期日填進下面的〈申請紀錄〉。
- 目前**不需要**先建立憑證或描述檔：借到 Mac 後，Xcode 登入同一個 Apple 帳號會自動處理（Signing & Capabilities → Team）。

---

## 五、續約與取消

- 用 App 申請的是**自動續訂**，每年自動扣款，直到你取消。
- 要取消：iPhone 設定 → 你的名字 → 訂閱 → Apple Developer Program。
  - **最晚要在續約日前一天取消**。
  - 當年已付的費用不退，但可以用到到期日。
- 到期後一年內還能重新訂閱。
- ⚠️ 會員到期後，用這個帳號簽的 App（WolkaraForever）也會失效，打不開。

---

## 六、常見延誤或被退件的原因

| 原因 | 避免方法 |
|------|----------|
| 姓名用了暱稱、別名或公司名 | 用護照上的英文法定姓名 |
| Apple 帳號資料過舊，或地址填郵政信箱 | 先更新帳號的姓名、地址、電話 |
| 網頁付款用了別人的信用卡 | 用自己名下的卡（不然會被要求補證件） |
| 信用卡沒開海外或網路刷卡、不能刷美元 | 先打電話給銀行開通 |
| 用 App 申請時中途換了裝置 | 從頭到尾用同一台 iPhone |
| 用 Apple 帳號餘額或禮品卡付款 | 不接受，要用信用卡 |

---

## 申請紀錄（申請後填）

- 申請日期：
- 申請方式：App / 網頁
- Enrollment ID：
- 通過日期：
- Team ID：
- 會員到期日：
- 自動續訂：是 / 否

---

## 來源（Apple 官方）

- 計畫註冊說明（繁中）：https://developer.apple.com/tw/help/account/membership/program-enrollment
- Program enrollment（英文）：https://developer.apple.com/help/account/membership/program-enrollment
- 註冊支援：https://developer.apple.com/tw/support/enrollment/
- 開始註冊：https://developer.apple.com/programs/enroll/
- 用 Apple Developer App 註冊、驗證、續約：https://developer.apple.com/support/app-account/
- App 註冊開放地區：https://support.apple.com/HT204411/
- 聯絡支援：https://developer.apple.com/contact/
