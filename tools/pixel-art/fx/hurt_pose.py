"""2頭身の歩くキャラ（16×32）に、ダメージを受けたときの絵を足す（2026-10-04、人間の指示
「ダメージを食らった時、ダメージを食らったドット絵になるようにして」）。

使い方: python3 hurt_pose.py assets-src/characters/walk-2head
各キャラの JSON の frames に、次の3コマを足す（どれも左向き＝戦闘で敵の方を向いた絵から作る）:
  hurt_left  ダメージの姿: 身をすくめ（胴を1行ちぢめ、頭を1ドット下げる）、目をぎゅっとつぶり、口をあける
  shock_left しびれ（雷に打たれた瞬間）: hurt_left と同じ形で、ふちを白く、中を青くした色（光る）
  flash_left 当たった瞬間: 体ぜんぶを白く（1コマだけ）
2頭身の型（field_templates.py）では、左向きの目は (14,5)(15,5)、顔の肌は (13,4) の色（ここを変えるのは、ちぢめる前）。
"""
import json
import os
import sys

EYE = [(14, 5), (15, 5)]
CLOSED = [(15, 5), (15, 6)]               # つぶった目（横線）
MOUTH = (17, 6)                           # あけた口


SYMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"   # 色の記号（A=palette[0]…Z の次は小文字）


def lum(h):
    v = int(h[1:], 16)
    return 0.299 * (v >> 16) + 0.587 * ((v >> 8) & 255) + 0.114 * (v & 255)


def shift_rows(g, y0, y1, dx):
    for y in range(y0, y1 + 1):
        r = g[y]
        g[y] = (["."] * dx + r[:16 - dx]) if dx > 0 else (r[-dx:] + ["."] * (-dx))


def make(d):
    pal = d["palette"]
    L = lambda i: SYMS[i]
    sym = {L(i): c for i, c in enumerate(pal)}
    g = [list(r) for r in d["frames"]["left0"]]
    skin = g[13][4]
    ink = "A"                                   # 型の外周の色（いちばん暗い）
    # 顔: 目を閉じる（ぎゅっとつぶった横線）・口をあける
    for y, x in EYE:
        g[y][x] = skin
    for y, x in CLOSED:
        g[y][x] = ink
    g[MOUTH[0]][MOUTH[1]] = ink
    # ひるむ: 胴を1行ちぢめて、頭から上を1ドット下げる（ひざを曲げて身をすくめる）。
    # 頭を横へずらすと、はちまき・髪の先が16ドットの枠で切れたので、横には動かさない（後ろへの飛ばされは、戦闘画面で絵ごと2ドット右へ）
    del g[23]
    g.insert(0, ["."] * 16)
    hurt = ["".join(r) for r in g]
    # しびれ: ふち（いちばん暗い色）を白に、中は明るさで 濃い青・青・水色 にする
    extra = ["#ffffff", "#1d3f9a", "#4d7bff", "#8ee6ff"]
    base = len(pal)
    newpal = pal + [c for c in extra]
    W, DB, BL, CY = (L(base + i) for i in range(4))
    shock = []
    for r in hurt:
        o = ""
        for ch in r:
            if ch == ".":
                o += "."
            elif ch == ink:
                o += W
            else:
                v = lum(sym[ch])
                o += DB if v < 90 else (BL if v < 170 else CY)
        shock.append(o)
    flash = ["".join(W if ch != "." else "." for ch in r) for r in d["frames"]["left0"]]
    d["palette"] = newpal
    d["frames"]["hurt_left"] = hurt
    d["frames"]["shock_left"] = shock
    d["frames"]["flash_left"] = flash
    return d


if __name__ == "__main__":
    folder = sys.argv[1]
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(folder, fn)
        d = json.load(open(p))
        if "hurt_left" in d["frames"]:          # 作りなおすときは、足した色と絵を外してから
            d["palette"] = d["palette"][: len(d["palette"]) - 4]
            for k in ("hurt_left", "shock_left", "flash_left"):
                d["frames"].pop(k)
        d = make(d)
        json.dump(d, open(p, "w"), ensure_ascii=False)
        print(fn, "色", len(d["palette"]), "コマ", len(d["frames"]))
