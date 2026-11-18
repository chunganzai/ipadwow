#!/usr/bin/env python3
"""Re-sign the iPad's sideloaded apps before the free Apple ID's 7-day limit.

usage: resign.py            check; re-sign apps within THRESHOLD days if the iPad is
                            connected, otherwise send a desktop reminder
       resign.py --force    re-sign every app in apps.conf now
       resign.py --status   print expiry dates (uses the cache when the iPad is away)

Re-signing drives the iloader window (it has no command line): it must be running,
logged in with the iPad's Apple ID, and the screen must be unlocked. Anything it
cannot do on its own ends in a desktop notification saying what to do.
"""
import json, os, subprocess, sys, time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

THRESHOLD = 2.0          # days left that trigger a re-sign
REMIND_EVERY = 6 * 3600  # seconds between reminders while the iPad is away
STATE = os.path.expanduser("~/.local/state/ipad-resign")
CACHE = os.path.join(STATE, "last.json")
LOG = os.path.join(STATE, "resign.log")
ILOADER = os.path.expanduser("~/.local/bin/iloader")
IMPORT_BTN = (1725, 535)   # 「匯入 IPA」 in the maximized 1920x1008 window
LOGOUT_PX = (100, 340)     # 「登出」 button: red-tinted only while logged in

os.makedirs(STATE, exist_ok=True)
os.environ.setdefault("DISPLAY", ":0")


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def notify(title, body, urgent=False):
    log(f"notify: {title} / {body}")
    subprocess.run(["notify-send", "-a", "iPad 重簽", "-i", "phone",
                    "-u", "critical" if urgent else "normal", title, body])


def read_expiry():
    """Live list from the iPad (and refresh the cache), or None when it is away."""
    r = subprocess.run([sys.executable, os.path.join(HERE, "expiry.py"), "--json"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    rows = json.loads(r.stdout)
    with open(CACHE, "w") as f:
        json.dump({"checked": datetime.now(timezone.utc).isoformat(), "apps": rows}, f)
    return rows


def cached_expiry():
    try:
        rows = json.load(open(CACHE))["apps"]
    except (OSError, ValueError, KeyError):
        return []
    now = datetime.now(timezone.utc)
    for r in rows:
        r["days_left"] = round((datetime.fromisoformat(r["expires"]) - now).total_seconds() / 86400, 2)
    return rows


def describe(rows):
    return "、".join(f"{r['bundle'].split('.')[1]} 剩 {r['days_left']:.1f} 天" for r in rows)


def screen_locked():
    r = subprocess.run(["cinnamon-screensaver-command", "-q"], capture_output=True, text=True,
                       env={**os.environ, "LANG": "C", "LANGUAGE": "C"})
    return "is active" in r.stdout


def iloader_window():
    out = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.rstrip().endswith(" iloader"):
            return line.split()[0]
    return None


def ensure_iloader():
    wid = iloader_window()
    if not wid:
        log("starting iloader")
        subprocess.Popen([ILOADER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
        for _ in range(30):
            time.sleep(1)
            wid = iloader_window()
            if wid:
                time.sleep(5)
                break
    if not wid:
        return None
    subprocess.run(["wmctrl", "-i", "-r", wid, "-b", "add,maximized_vert,maximized_horz"])
    subprocess.run(["wmctrl", "-i", "-a", wid])
    time.sleep(1.5)
    return wid


def resign_with_iloader(due):
    import xctl
    if screen_locked():
        return "電腦螢幕鎖定中，解鎖後執行 ~/ipadwow/resign/resign.py"
    wid = ensure_iloader()
    if not wid:
        return "iloader 沒有開起來"
    img = xctl.grab(wid)
    if img.size != (1920, 1008):
        return f"iloader 視窗大小是 {img.size}，不是預期的 1920x1008"
    r, g, b = img.getpixel(LOGOUT_PX)
    if r - g < 12:
        return "iloader 沒有登入，請在 iloader 點 iPad 用的 Apple ID 登入後再執行一次"
    failed = []
    for app in due:
        log(f"re-signing {app['bundle']} from {app['ipa']}")
        old = app["expires"]
        subprocess.run(["wmctrl", "-i", "-a", wid])
        time.sleep(1)
        xctl.click(wid, *IMPORT_BTN)
        time.sleep(2.5)
        xctl.key("l", ("Control_L",))
        time.sleep(0.8)
        xctl.type_text(app["ipa"])
        time.sleep(0.5)
        xctl.key("Return")
        done = False
        for _ in range(40):            # up to ~5 minutes
            time.sleep(8)
            rows = read_expiry() or []
            cur = next((x for x in rows if x["bundle"] == app["bundle"]), None)
            if cur and cur["expires"] > old:
                log(f"ok {app['bundle']} now expires {cur['expires']}")
                done = True
                break
        time.sleep(4)
        if not done:
            failed.append(app["bundle"].split(".")[1])
    if failed:
        return f"{'、'.join(failed)} 重簽沒有完成，請看 iloader 畫面"
    return None


def main():
    force = "--force" in sys.argv
    live = read_expiry()
    rows = live if live is not None else cached_expiry()

    if "--status" in sys.argv:
        src = "iPad" if live is not None else "上次紀錄（iPad 未連線）"
        for r in rows:
            exp = datetime.fromisoformat(r["expires"]).astimezone()
            print(f"{r['bundle']:<40} 到期 {exp:%m/%d %H:%M}  剩 {r['days_left']:.1f} 天")
        print(f"來源：{src}")
        return

    due = rows if force else [r for r in rows if r["days_left"] <= THRESHOLD]
    if not rows:
        log("no expiry data yet (connect the iPad once)")
        return
    if not due:
        log(f"nothing due: {describe(rows)}")
        return

    if live is None:
        stamp = os.path.join(STATE, "reminded")
        last = os.path.getmtime(stamp) if os.path.exists(stamp) else 0
        soonest = min(r["days_left"] for r in due)
        if time.time() - last >= REMIND_EVERY or soonest < 0.5:
            notify("iPad 的 App 快過期了", f"{describe(due)}。請把 iPad 用線接上這台電腦，會自動重簽。",
                   urgent=soonest < 1)
            open(stamp, "w").close()
        return

    problem = resign_with_iloader(due)
    if problem:
        notify("iPad 自動重簽需要你處理", f"{describe(due)}。{problem}", urgent=True)
    else:
        notify("iPad 重簽完成", describe(read_expiry() or []))


if __name__ == "__main__":
    main()
