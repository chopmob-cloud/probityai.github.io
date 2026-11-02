"""F3 Missing is not clean: a record with one passage missing (verdict from probity-verify).

"Record" is probity-verify's own word for the stored report it checks against the source capture
(adapters/source_coverage.py: a selected span found in the source and not in the record returns
contradicted, selected_span_missing_from_record). The picture separates the two readers' vantages, one
panel each, divided by a thin rule:

Top panel: what a reader that trusts the record has in front of it. The record alone, its six passages packed
in a plain frame with a tab on its top edge that prints report.txt. Nothing in it is marked: a reader of the
record alone has nothing to flag. The eye stands to its right in the trusting reader's own ink (self), and a
thought cloud in the same ink holds a check: it believes the record is fine.
Bottom panel: what probity-verify has in front of it. The same six passages, now standing over the source
passages they came from, so the fifth place in the record is empty; nothing is drawn in it. Under it the
source capture, all seven passages, with a tab hanging from its foot that prints source.html. One straight
accent rung pairs each source passage with its record passage; the fifth rung, in loss ink, rises to the
record's foot like the others, with nothing above it: the source has the passage, the record has none to pair with.
A brace gathers both rows into the lens, which prints a receipt with a cross in the same loss ink:
contradicted, with the packet's reason line under it. The two readers stand at the same x, one per panel.
The only words are what the readers print and the two file paths the packet binds.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import figkit as fk

HERE = Path(__file__).resolve().parent
NAME = "f3-missing-not-clean"
REV = 3
CASE = tomllib.loads((HERE / "data/source-coverage.toml").read_text())
N, HOLE = 7, 4
FINE = "fine"  # what a reader that trusts the record concludes
TITLE = "A passage missing from the record is not a clean record"
DESC = (
    "Top: a reader that trusts the record has only the record in front of it, six passages with nothing to flag, "
    "and thinks it fine. Bottom: the same record over the source capture it came from, seven passages. "
    "probity-verify pairs each source passage with its passage in the record, finds the fifth has none, and "
    f"returns {CASE['decision']}, reason {CASE['reason']}."
)


def _tab(f: fk.Fig, cx, edge, name, below) -> float:
    """A file-name tab centred on cx on a frame's edge at y=edge: standing on top of the frame, or hanging
    from its foot when below. It carries the path the packet binds (product text). Returns its far edge."""
    sz = f.text_size
    cap = fk.cap_height(sz, "mono", 500)
    w = fk.text_width(name, sz, "mono", 500) + 24
    h = cap + 16
    y = edge if below else edge - h
    f.rect(cx - w / 2, y, w, h, fill="tile", stroke="rule", rx=5, sw=2.5)
    f.text(cx, y + h / 2 + cap / 2, name, "fg", "mono", 500, anchor="middle")
    return y + h if below else y


def _frame(f: fk.Fig, xs, y, sw_, sh_, tab, below) -> float:
    """A plain framed row round the pages at xs, top y, with a file-name tab; returns the tab's far edge."""
    fw = xs[-1] + sw_ - xs[0] + 20
    f.rect(xs[0] - 10, y - 10, fw, sh_ + 20, stroke="rule", rx=8, sw=2.5)
    edge = y + sh_ + 10 if below else y - 10
    return _tab(f, xs[0] - 10 + fw / 2, edge, tab, below=below)


def _draw(f: fk.Fig, geo, sgap, top, gsize, reason_below, lr) -> float:
    """Draw both panels with the top panel's record at top; returns the bottom of the last thing drawn."""
    sz = f.text_size
    sw_, sh_ = fk.sheet_size(*geo)
    rw = round(gsize * 1.9 * 0.74, 1)  # the receipt's width
    word_w = max(fk.text_width(w, sz, "sans", 600) for w in (FINE, CASE["decision"]))
    col_w = lr * 2.5 + 30 + rw + 16 + word_w
    gx = f.width - fk.PAD - col_w + lr * 1.25  # the readers' glyph column, the same in both panels
    mx = gx + lr * 1.25 + 30  # the verdicts' left edge
    tx = mx + rw + 16
    cap = fk.cap_height(sz, "sans", 600)
    x0 = fk.PAD + 10
    xs = [x0 + i * (sw_ + sgap) for i in range(N)]
    # top panel: the record alone, its six passages packed, and the eye that trusts it
    yr = top
    _frame(f, xs[: N - 1], yr, sw_, sh_, CASE["record_path"], below=False)
    for x in xs[: N - 1]:
        fk.sheet(f, x, yr, *geo)
    ey = yr + sh_ / 2
    er = lr * 1.25
    # the eye stands right beside the record it reads, so what it has in front of it is the record alone
    ex = xs[N - 2] + sw_ + 10 + 24 + er
    fk.eye(f, ex, ey, er, ink="self")
    # the thought cloud stands up and right of the eye, clear of it, with the check inside; fine beside it
    cw, ch = rw + 30, gsize * 1.6
    ccx, ccy = ex + er + 34 + cw / 2, ey - ch * 0.3
    fk.thought(f, ccx, ccy, cw, ch, (ex + er * 0.8, ey - er * 0.6), ink="self")
    g = ch * 0.5
    f.glyph("check", ccx - g / 2, ccy - g / 2, g, "self", sw=max(3.0, g * 0.13))
    fx = ccx + cw / 2 + ch * 0.3 + 12
    assert fx + fk.text_width(FINE, sz, "sans", 600) <= f.width - fk.PAD, "fine runs off the frame"
    f.text(fx, ccy + cap / 2, FINE, "fg", "sans", 600)
    rule_y = yr + sh_ + 10 + max(28, ch * 0.4)
    # bottom panel: the same six passages over the source passages they came from; the fifth place is empty
    tab_h = cap + 16
    yb = rule_y + 26 + tab_h + 10
    # no divider between the panels: one dashed tie runs from the top record's foot to the bottom record's
    # tab, so the two report.txt rows read as one file seen twice
    t1 = (xs[0] - 10 + xs[N - 2] + sw_ + 10) / 2
    t2 = (xs[0] - 10 + xs[N - 1] + sw_ + 10) / 2
    y0, y2 = yr + sh_ + 10, yb - 10 - tab_h
    jy = (y0 + y2) / 2
    f.path(f"M{t1:.1f} {y0:.1f} L{t1:.1f} {jy:.1f} L{t2:.1f} {jy:.1f} L{t2:.1f} {y2:.1f}", stroke="rule", sw=2.5, dash="8 6")
    _frame(f, xs, yb, sw_, sh_, CASE["record_path"], below=False)
    for i, x in enumerate(xs):
        if i != HOLE:
            fk.sheet(f, x, yb, *geo)
    under = yb + sh_ + 10  # the record frame's foot
    ys = under + 2 * (lr + 30) + 10  # the source's top
    src_foot = _frame(f, xs, ys, sw_, sh_, CASE["source_path"], below=True)
    for x in xs:
        fk.sheet(f, x, ys, *geo)
    # probity-verify pairs each source passage with its record passage, one straight rung per pair; the fifth
    # rung, in loss ink, rises to the record's foot like the other six and has nothing above it: absence shown by
    # absence. Every mark drawn inside the empty place was read as a seventh page or a marker.
    for i, x in enumerate(xs):
        mx_ = x + sw_ / 2
        if i == HOLE:
            f.line(mx_, ys - 12, mx_, under + 2, "loss", sw=4)
        else:
            f.line(mx_, ys - 12, mx_, under + 2, "accent", sw=3)
    # a brace gathers both rows into the lens: it reads the two rows side by side
    rx1 = xs[-1] + sw_ + 10
    bx = rx1 + 18
    bt_, bb_ = yb - 10, ys + sh_ + 10
    bm = (bt_ + bb_) / 2
    f.path(
        f"M{bx:.1f} {bt_:.1f} Q{bx + 12:.1f} {bt_:.1f} {bx + 12:.1f} {bt_ + 14:.1f} L{bx + 12:.1f} {bm - 14:.1f} "
        f"Q{bx + 12:.1f} {bm:.1f} {bx + 24:.1f} {bm:.1f} Q{bx + 12:.1f} {bm:.1f} {bx + 12:.1f} {bm + 14:.1f} "
        f"L{bx + 12:.1f} {bb_ - 14:.1f} Q{bx + 12:.1f} {bb_:.1f} {bx:.1f} {bb_:.1f}",
        stroke="accent",
        sw=3,
    )
    assert bx + 40 <= gx - lr, "the rows run into the readers' column"
    yv = bm
    f.line(bx + 26, yv, gx - lr - 12, yv, "accent", sw=3)
    fk.arrow(f, gx - lr - 4, yv, size=7)
    fk.lens(f, gx, yv, lr)
    f.line(gx + lr + 2, yv, mx - 12, yv, "accent", sw=3)
    fk.arrow(f, mx - 4, yv, size=7)
    fk.slip(f, mx, yv, gsize * 1.9, CASE["glyph"], "loss")
    f.text(tx, yv + cap / 2, CASE["decision"], "fg", "sans", 600)
    if reason_below:
        ry = src_foot + 14 + sz
        f.text(fk.PAD - 1.5, ry, CASE["reason"], "muted", "mono", 500)
        return ry + sz * 0.6
    ry = yv + gsize * 0.95 + 14 + sz
    rx = f.width - fk.PAD - fk.text_width(CASE["reason"], sz, "mono", 500)
    assert rx > rx1 + 16, "the reason runs into the source row"
    f.text(rx, ry, CASE["reason"], "muted", "mono", 500)
    return max(ry + sz * 0.4, src_foot)


def wide() -> fk.Fig:
    f = fk.Fig(NAME, "wide", 1280, 0, TITLE, DESC)
    f.height = round(_draw(f, (3, 3, 12, 5, 11), 34, 76, 34, False, 18) + 26)
    return f


def narrow() -> fk.Fig:
    f = fk.Fig(NAME, "narrow", 720, 0, TITLE, DESC)
    # one cell column per page: seven portrait pages leave room for the verdict column in 720 units
    f.height = round(_draw(f, (1, 3, 12, 4, 7), 10, 86, 40, True, 20) + 30)
    return f


FIGS = (wide, narrow)
