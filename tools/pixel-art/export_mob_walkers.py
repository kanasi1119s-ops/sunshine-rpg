"""町の人（モブ）の歩く絵の素体を、主要キャラと同じ2頭身の絵（assets-src/characters/walk-2head/*.json）から作る。
使い方: python3 tools/pixel-art/export_mob_walkers.py
出力: src/game/sprite/mob-walker-data.generated.ts（手で編集しない）

どの色を「髪・肌・服・飾り」として塗り替えるかは、ROLES に、色の記号（palette の何番目か）で書く。
書いていない色（縁取り・目・白・金具・革など）は、そのまま使う。塗り替えるときは、同じ役割の色の明るさの差（影・地・明）を保つ。"""
import json, colorsys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "assets-src/characters/walk-2head"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# 素体の名前 → (元の人物, {役割: 色の記号})
TEMPLATES = {
    "reto": ("レト", {"hair": "BCD", "skin": "EGHI", "accent": "JK", "top": "LMO", "bottom": "PQRSVW"}),
    "yuri": ("ユーリ", {"hair": "BCD", "skin": "GIJK", "accent": "EF", "top": "LMO", "bottom": "QRSTUW"}),
    "mina": ("ミナ", {"hair": "BCE", "skin": "GKLM", "accent": "DI", "top": "NOPQSTUVWX"}),
    "guide": ("ガイド", {"hair": "BCDX", "skin": "HJKM", "accent": "ION", "top": "PQRSUWY"}),
}

def lum(hexv):
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)[1]

def strip(key, frames):
    """モブには、武器（弓・杖）・ぶら下げた灯り・髪や額の飾りは付けない（2026-10-04、人間の指示）。
    持ち物の色の画素を消し、まわりの縁取りが残らないようにする。髪の飾りは、髪の色にぬりかえる。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        H, W = len(g), len(g[0])
        def at(x, y):
            return g[y][x] if 0 <= x < W and 0 <= y < H else "."
        for y in range(H):
            for x in range(W):
                c = g[y][x]
                if c == ".":
                    continue
                if key == "reto" and ((c in "TU" and y >= 20) or (c == "N" and y >= 24)):
                    g[y][x] = "."                       # ぶら下げた灯り
                elif key == "yuri":
                    if (c in "VP" and y >= 20) or (c == "N" and y >= 24):
                        g[y][x] = "."                   # ぶら下げた灯り
                    elif c in "EF" and y <= 12:
                        g[y][x] = "C"                   # はちまき → 髪
                elif key == "mina":
                    if c in "EFHJ":
                        g[y][x] = "."                   # 髪かざりと杖
                elif key == "guide":
                    if y <= 3:
                        g[y][x] = "."                   # 頭の上のまげ（飾り）
                    elif c in "EFGNX" and 8 <= y <= 10:
                        g[y][x] = "B"                   # 額・髪の飾り・髪どめ → 髪
                    elif c in "LTV":
                        g[y][x] = "."                   # 弓
                    elif fk.startswith("up") and y >= 11 and 6 <= x <= 9:
                        g[y][x] = "B" if y <= 15 else "S"   # 背中の矢筒 → 髪・服の色
        # 持ち物を消したあとに、ひとりぼっちになった縁取りを消す
        for _ in range(3):
            for y in range(H):
                for x in range(W):
                    if g[y][x] != "A":
                        continue
                    if not any(at(x + dx, y + dy) not in (".", "A") for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                        g[y][x] = "."
        out[fk] = ["".join(r) for r in g]
    return out

def symmetrize(frames):
    """前向き・後ろ向きの絵の、頭から腰まで（上の23段）を、左右対称にする。持ち物を消したあとの欠けを、
    絵の残っているほうの半分を反転して埋める。脚（下の段）は歩きの動きがあるので、そのまま。"""
    out = {}
    for fk, rows in frames.items():
        if not (fk.startswith("down") or fk.startswith("up")):
            out[fk] = rows
            continue
        rows = list(rows)
        upper = rows[:23]
        left = sum(1 for r in upper for ch in r[:8] if ch != ".")
        right = sum(1 for r in upper for ch in r[8:] if ch != ".")
        new = []
        for r in upper:
            half = r[8:] if right >= left else r[:8]
            full = (half[::-1] + half) if right >= left else (half + half[::-1])
            new.append(full)
        out[fk] = new + rows[23:]
    return out

built = {}
for key, (name, groups) in TEMPLATES.items():
    d = json.load(open(SRC / f"{name}.json"))
    pal = d["palette"]
    roles = ["fixed"] * len(pal)
    shade = [0.0] * len(pal)
    for role, letters in groups.items():
        idx = [LETTERS.index(c) for c in letters]
        ls = sorted(lum(pal[i]) for i in idx)
        med = ls[len(ls) // 2]
        for i in idx:
            roles[i] = role
            shade[i] = round(max(-0.6, min(0.6, (lum(pal[i]) - med) * 1.25)), 3)
    frames = {k: v for k, v in d["frames"].items() if k[:-1] in ("down", "up", "left", "right") and k[-1] in "012"}
    frames = symmetrize(strip(key, frames))
    built[key] = {"palette": pal, "roles": roles, "shade": shade, "frames": frames}

# 男の人の2種め: レトの頭（ふさふさの髪）に、ユーリの服。ユーリの髪はとげとげなので、モブには使わない（2026-10-04、人間の指示）
def compose(head_key, body_key, split_y):
    h, b = built[head_key], built[body_key]
    table, order = {}, []
    def letter(pal, i, src):
        k = (src["palette"][i], src["roles"][i], src["shade"][i])
        if k not in table:
            table[k] = LETTERS[len(order)]
            order.append(k)
        return table[k]
    frames = {}
    for fk in h["frames"]:
        rows = []
        for y in range(len(h["frames"][fk])):
            src = h if y < split_y else b
            row = src["frames"][fk][y]
            rows.append("".join("." if ch == "." else letter(None, LETTERS.index(ch), src) for ch in row))
        frames[fk] = rows
    return {"palette": [k[0] for k in order], "roles": [k[1] for k in order], "shade": [k[2] for k in order], "frames": frames}

out = {
    "reto": built["reto"],
    "man2": compose("reto", "yuri", 14),
    "mina": built["mina"],
    "guide": built["guide"],
    # 女の人の増やした2種: ミナの頭にガイドの服、ガイドの頭にミナの服
    "woman3": compose("mina", "guide", 14),
    "woman4": compose("guide", "mina", 14),
}

ts = (
    "// 自動生成: tools/pixel-art/export_mob_walkers.py（手で編集しない）。町の人（モブ）の2頭身の素体4種\n"
    "export interface MobTemplate {\n  palette: string[];\n  roles: string[];\n  shade: number[];\n  frames: Record<string, string[]>;\n}\n\n"
    "export const MOB_TEMPLATES: Record<string, MobTemplate> = " + json.dumps(out, ensure_ascii=False) + ";\n"
)
(ROOT / "src/game/sprite/mob-walker-data.generated.ts").write_text(ts, encoding="utf-8")
print("書き出し:", ", ".join(out), len(ts) // 1024, "KB")
