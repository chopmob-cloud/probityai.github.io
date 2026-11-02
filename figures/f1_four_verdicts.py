"""F1 Four verdicts: one sealed archive, checked four ways, and what the verifier prints each time.

Two panels, one above the other, divided by a thin rule.
Panel 1 (arms 1 to 3 of demo/four-arms.sh): the archive, a box of three files sealed by one closed padlock, fans
into three rows. Each row reads left to right: the archive as the verifier gets it, the verifier's lens (blue)
and the receipt it prints with the verdict glyph, then the verdict word and exit code. The padlock is the same in
every row; what happened to the archive is drawn on its files. Row 2: a pencil in loss ink rests its point on one
byte of the middle file, that one byte in the same ink: someone changed one byte. The receipt's cross takes the
same ink. Row 3: where the middle file stood there is only a dashed footprint: a required file is missing, so
not-established never reads as failed.
Panel 2 (arm 4) uses the same grammar: the same archive fans into two readings, the upper by the version 1 lens,
the lower by the version 2 lens (the same instrument made stronger and larger, as the stricter verifier is),
each with the verifier id its record carries under it. Both routes run into one open file folder and both
receipts stand in it, whole: kept together. The verdict both print sits beside the folder.
Words and exit codes come from data/four-arms.toml; the row captions are the alt text, not words on the picture.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import figkit as fk

HERE = Path(__file__).resolve().parent
NAME = "f1-four-verdicts"
REV = 3
ARMS = tomllib.loads((HERE / "data/four-arms.toml").read_text())["arm"]
TITLE = "Four verdicts from one evidence archive"
# the alt text: each row's caption with what the verifier prints for it, from data/four-arms.toml
DESC = " ".join(
    ["One sealed archive of three files, checked four ways."]
    + [f"{a['caption']}: {a['verdict']}, exit {a['exit']}." for a in ARMS[:3]]
    + [
        f"Below: the same archive is read by verifier {ARMS[3]['verifier_ids'][0]} and by the changed verifier "
        f"{ARMS[3]['verifier_ids'][1]}. Both print {ARMS[3]['verdict']}, exit {ARMS[3]['exit']}, and both "
        "receipts are kept in one folder."
    ]
)
INK = {
    "check": "fg",
    "cross": "loss",
    "query": "fg",
}  # the cross takes the pencil's ink: that changed byte is why the verifier refused
STATE = (
    {},
    {"mark": (1, (1, 0))},
    {"missing": 1},
)
LR, SH = 20, 62  # lens radius, receipt height


def _verdict(f: fk.Fig, arm, x, cy, stacked: bool) -> float:
    """The verdict word and exit code as the verifier prints them, from x, centred on cy. Returns the right edge."""
    sz = f.text_size
    cap = fk.cap_height(sz, "mono", 500)
    ex = f"exit {arm['exit']}"
    if stacked:
        f.text(x, cy - sz * 0.2, arm["verdict"], "fg", "mono", 500)
        f.text(x, cy - sz * 0.2 + sz * 1.2, ex, "muted", "mono", 500)
        return x + fk.text_width(arm["verdict"], sz, "mono", 500)
    f.text(x, cy + cap / 2, arm["verdict"], "fg", "mono", 500)
    ex_x = x + fk.text_width(arm["verdict"] + " ", sz, "mono", 500)
    f.text(ex_x, cy + cap / 2, ex, "muted", "mono", 500)
    return ex_x + fk.text_width(ex, sz, "mono", 500)


def _read(f: fk.Fig, x, cy, bars, lr=LR, version=0) -> float:
    """The route from an archive's right edge x through a lens with `bars` glass to a receipt's arrow tip.
    Returns the x where the receipt's left edge goes."""
    lx = x + 30 + lr
    sx = lx + lr * 1.6 + 24
    f.line(x + 6, cy, lx - lr * (1.3 if version > 1 else 1.0) - 2, cy, "accent", sw=3)
    rim = lr * (1.3 if version > 1 else 1.0)  # a later version is drawn larger (fk.lens_version)
    if version:
        fk.lens_version(f, lx, cy, lr, version)
    else:
        fk.lens(f, lx, cy, lr, bars=bars)
    f.line(lx + rim + 2, cy, sx - 12, cy, "accent", sw=3)
    fk.arrow(f, sx - 4, cy, size=7)
    return sx


def _row(f: fk.Fig, k, bx, cy, geo, sgap, stacked, lr=LR, sh=SH) -> float:
    """Panel 1: one archive at bx centred on cy, read by the verifier, which prints a receipt. Returns the right edge."""
    arm = ARMS[k]
    bw, bh = fk.box_size(3, geo, sgap)
    fk.box(f, bx, cy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=lr * 0.8, **STATE[k])
    sx = _read(f, bx + bw, cy, 0, lr, version=1)
    fk.slip(f, sx, cy, sh, arm["glyph"], INK[arm["glyph"]])
    return _verdict(f, arm, sx + round(sh * 0.74, 1) + 26, cy, stacked)


def _pair(f: fk.Fig, x0, cy, geo, sgap, pitch, lr=LR, fan=96, narrow=False) -> float:
    """Panel 2: one archive at x0 centred on cy fans, as in panel 1, into two readings: the version 1 lens on
    the upper route, the version 2 lens (the same instrument made stronger) on the lower. The verifier id each
    reading's record carries (product text from data/four-arms.toml) sits under its own lens. Both routes run
    into one open file folder and both receipts stand in it, whole; the verdict both print sits beside it
    (under it in the narrow layout). Returns the lowest y drawn."""
    arm = ARMS[3]
    bw, bh = fk.box_size(3, geo, sgap)
    fk.box(f, x0, cy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=lr * 0.8)
    rows = (cy - pitch / 2, cy + pitch / 2)
    rx = x0 + bw + fan
    fx = x0 + bw + 10
    for ry in rows:
        f.path(
            f"M{fx:.1f} {cy:.1f} C{fx + 50:.1f} {cy:.1f} {rx - 70:.1f} {ry:.1f} {rx - 16:.1f} {ry:.1f}",
            stroke="rule",
            sw=2.5,
        )
        fk.arrow(f, rx - 6, ry, "rule", size=7)
    ends = []
    for k, ry in enumerate(rows):
        f.line(rx - 4, ry, rx + 6, ry, "accent", sw=3)
        ends.append(_read(f, rx, ry, 0, lr, version=k + 1))
    # the verifier id each reading's record carries, under its own lens
    sz = f.text_size
    cap = fk.cap_height(sz, "mono", 500)
    v1, v2 = arm["verifier_ids"]
    lx = rx + 30 + lr  # the lens centre (see _read)
    low_text = 0.0
    for k, (vid, ry, rim) in enumerate(zip((v1, v2), rows, (lr, lr * 1.4))):
        # under its lens; in the narrow layout the upper id sits over its lens, clear of the routes below it
        ty = ry - rim - 12 if narrow and k == 0 else ry + rim * 1.5 + 8 + cap
        # under its lens; where the column is too narrow it ends at the frame's right margin, still under it
        tx = min(lx - lr, f.width - fk.PAD - fk.text_width(vid, sz, "mono", 500))
        if narrow and k == 0:  # over its lens, ending at the lens's right rim, clear of the verdict to its right
            tx = lx + lr - fk.text_width(vid, sz, "mono", 500)
        assert tx <= lx, vid
        f.text(tx, ty, vid, "fg", "mono", 500)
        low_text = max(low_text, ty + sz * 0.3)
    # the receipts' place: one open folder; both routes run into it and both receipts stand in it, whole
    sh2 = SH + 10
    rw = round(sh2 * 0.74, 1)
    g = 14
    fw = 2 * rw + 3 * g
    # the folder stands clear of the longer id, so the ids read as the lenses' names, not the folder's
    px = max(max(ends) + 40, lx - lr + fk.text_width(v2, sz, "mono", 500) + 30)
    if narrow:
        px = f.width - fk.PAD - fw - 6
    top = cy - sh2 / 2 - 14
    fh = sh2 + 34
    for e, ry, ty in zip(ends, rows, (cy - 12, cy + 12)):
        x1 = px - 12
        f.path(
            f"M{e - 12:.1f} {ry:.1f} C{(e + x1) / 2:.1f} {ry:.1f} {(e + x1) / 2:.1f} {ty:.1f} {x1:.1f} {ty:.1f}",
            stroke="accent",
            sw=3,
        )
        fk.arrow(f, px - 4, ty, size=7)
    fk.folder_back(f, px, top, fw, fh)
    for k in range(2):
        fk.slip(f, px + g + k * (rw + g), cy - 10, sh2, "check", "fg")
    # the folder's slanted front pocket, the back's own width, over the receipts' torn feet only
    fk.folder_front(f, px, top, fw, fh, 30)
    if narrow:
        # over the folder's right end, clear of its tab and of the upper id
        vx = f.width - fk.PAD - fk.text_width(arm["verdict"], sz, "mono", 500)
        vy = top - 20 - 14 - sz * 1.2 + sz * 0.2
        _verdict(f, arm, vx, vy, True)
        return low_text + 20
    right = _verdict(f, arm, px + fw + 26, cy, False)
    assert right <= f.width - fk.PAD, right
    return max(low_text, top + fh) + 20


def wide() -> fk.Fig:
    W, pad = 1280, fk.PAD
    geo, sgap = (3, 3, 11, 4, 10), 10
    bw, bh = fk.box_size(3, geo, sgap)
    f = fk.Fig(NAME, "wide", W, 0, TITLE, DESC)
    pitch = bh + 40
    c0 = 30 + bh / 2
    centres = [c0, c0 + pitch, c0 + 2 * pitch]
    sy = centres[1]
    fk.box(f, pad, sy - bh / 2 + 6, geo=geo, sgap=sgap, lock_r=16)
    rx = pad + bw + 96
    fx = pad + bw + 10
    for cy in centres:
        f.path(
            f"M{fx:.1f} {sy:.1f} C{fx + 50:.1f} {sy:.1f} {rx - 70:.1f} {cy:.1f} {rx - 16:.1f} {cy:.1f}",
            stroke="rule",
            sw=2.5,
        )
        fk.arrow(f, rx - 6, cy, "rule", size=7)
    for k, cy in enumerate(centres):
        right = _row(f, k, rx, cy, geo, sgap, False)
        assert right <= W - pad, (k, right)
    rule_y = centres[-1] + bh / 2 + 30
    f.line(pad, rule_y, W - pad, rule_y, "rule", sw=1.5)
    pitch2 = SH + 40
    c2 = rule_y + 30 + pitch2 / 2 + SH / 2 + 14
    pitch2 = max(pitch2, bh + 30)
    low = _pair(f, pad, c2, geo, sgap, pitch2, fan=96)
    f.height = round(low + 24)
    return f


def narrow() -> fk.Fig:
    W, pad = 720, fk.PAD
    geo, sgap = (3, 3, 9, 4, 8), 8
    bw, bh = fk.box_size(3, geo, sgap)
    f = fk.Fig(NAME, "narrow", W, 0, TITLE, DESC)
    pitch = max(bh, 2 * f.text_size * 1.3) + 46
    c0 = 30 + bh / 2
    centres = [c0, c0 + pitch, c0 + 2 * pitch]
    for k, cy in enumerate(centres):
        right = _row(f, k, pad, cy, geo, sgap, True, 18, 58)
        assert right <= W - pad, (k, right)
    rule_y = centres[-1] + bh / 2 + 30
    f.line(pad, rule_y, W - pad, rule_y, "rule", sw=1.5)
    # panel 2: the same archive fans into the version 1 and version 2 readings, one folder keeps both
    pitch2 = bh + 2 * f.text_size + 40
    c2 = rule_y + 30 + f.text_size + 18 + 18 * 1.3 + pitch2 / 2
    low = _pair(f, pad, c2, geo, sgap, pitch2, 18, fan=70, narrow=True)
    f.height = round(low + 24)
    return f


FIGS = (wide, narrow)
