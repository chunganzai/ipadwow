#!/usr/bin/env python3
"""List when each sideloaded app on the iPad expires.

usage: expiry.py            human-readable table
       expiry.py --json     machine-readable (used by watch.sh)

Reads the provisioning profiles on the connected iPad (ideviceprovision) and keeps
only apps that are still installed and listed in apps.conf. Exit code 2 = no iPad.
"""
import json, os, plistlib, re, subprocess, sys, tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def load_apps():
    """apps.conf lines: <bundle prefix> <ipa path>"""
    apps = {}
    with open(os.path.join(HERE, "apps.conf")) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                prefix, ipa = line.split(None, 1)
                apps[prefix] = os.path.expanduser(ipa)
    return apps


def installed_bundles():
    out = subprocess.run(["ideviceinstaller", "-l", "-o", "list_user", "-o", "xml"],
                         capture_output=True, check=True).stdout
    return {a["CFBundleIdentifier"] for a in plistlib.loads(out)}


def profiles():
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ideviceprovision", "copy", d], capture_output=True, check=True)
        for name in os.listdir(d):
            raw = open(os.path.join(d, name), "rb").read()
            m = re.search(rb"<\?xml.*?</plist>", raw, re.S)
            if m:
                yield plistlib.loads(m.group(0))


def main():
    if not subprocess.run(["idevice_id", "-l"], capture_output=True, text=True).stdout.strip():
        print("iPad not connected", file=sys.stderr)
        sys.exit(2)
    apps = load_apps()
    installed = installed_bundles()
    latest = {}
    for p in profiles():
        appid = p["Entitlements"].get("application-identifier", "")
        bundle = appid.split(".", 1)[1] if "." in appid else appid
        if bundle not in installed:
            continue
        prefix = next((k for k in apps if bundle.startswith(k)), None)
        if not prefix:
            continue
        exp = p["ExpirationDate"].replace(tzinfo=timezone.utc)
        if bundle not in latest or exp > latest[bundle]["expires"]:
            latest[bundle] = {"bundle": bundle, "ipa": apps[prefix], "expires": exp}
    now = datetime.now(timezone.utc)
    rows = sorted(latest.values(), key=lambda r: r["expires"])
    for r in rows:
        r["days_left"] = round((r["expires"] - now).total_seconds() / 86400, 2)
    if "--json" in sys.argv:
        print(json.dumps([{**r, "expires": r["expires"].isoformat()} for r in rows]))
    else:
        for r in rows:
            local = r["expires"].astimezone().strftime("%Y-%m-%d %H:%M")
            print(f"{r['bundle']:<40} 到期 {local}  剩 {r['days_left']:.1f} 天")


if __name__ == "__main__":
    main()
