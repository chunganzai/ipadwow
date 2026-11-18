"""Tiny X11 helper: screenshot a window, click, type, press keys.

usage:
  xctl.py shot <winid> <out.png>
  xctl.py click <winid> <x> <y>        (window-relative)
  xctl.py type <text>
  xctl.py key <keysym> [modifier keysyms...]
"""
import sys, time
from Xlib import display, X, XK
from Xlib.ext import xtest
from PIL import Image

d = display.Display()
root = d.screen().root


def win(wid):
    return d.create_resource_object('window', int(wid, 16))


def origin(w):
    g = w.get_geometry()
    t = w.translate_coords(root, 0, 0)
    return -t.x, -t.y, g.width, g.height


def grab(wid):
    w = win(wid)
    x, y, wd, ht = origin(w)
    raw = root.get_image(x, y, wd, ht, X.ZPixmap, 0xffffffff)
    return Image.frombytes('RGB', (wd, ht), raw.data, 'raw', 'BGRX')


def shot(wid, out):
    w = win(wid)
    x, y, wd, ht = origin(w)
    raw = root.get_image(x, y, wd, ht, X.ZPixmap, 0xffffffff)
    im = Image.frombytes('RGB', (wd, ht), raw.data, 'raw', 'BGRX')
    im.save(out)
    print(out, wd, ht)


def click(wid, cx, cy):
    w = win(wid)
    x, y, _, _ = origin(w)
    xtest.fake_input(d, X.MotionNotify, x=x + cx, y=y + cy)
    d.sync(); time.sleep(0.1)
    xtest.fake_input(d, X.ButtonPress, 1); d.sync(); time.sleep(0.05)
    xtest.fake_input(d, X.ButtonRelease, 1); d.sync()


def keysym_code(name):
    ks = XK.string_to_keysym(name)
    return d.keysym_to_keycode(ks)


def key(name, mods=()):
    codes = [keysym_code(m) for m in mods]
    for c in codes:
        xtest.fake_input(d, X.KeyPress, c)
    k = keysym_code(name)
    xtest.fake_input(d, X.KeyPress, k); xtest.fake_input(d, X.KeyRelease, k)
    for c in reversed(codes):
        xtest.fake_input(d, X.KeyRelease, c)
    d.sync(); time.sleep(0.03)


SPECIAL = {'/': 'slash', '.': 'period', '-': 'minus', '_': 'underscore', ' ': 'space', ':': 'colon'}


def type_text(s):
    for ch in s:
        name = SPECIAL.get(ch, ch)
        shift = ch.isupper() or ch in '_:'
        key(name.lower() if len(name) == 1 else name, ('Shift_L',) if shift else ())


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'shot':
        shot(sys.argv[2], sys.argv[3])
    elif cmd == 'click':
        click(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == 'type':
        type_text(sys.argv[2])
    elif cmd == 'key':
        key(sys.argv[2], tuple(sys.argv[3:]))
