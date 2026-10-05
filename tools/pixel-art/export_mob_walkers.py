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
    "guide": ("コハク", {"hair": "BCDX", "skin": "HJKM", "accent": "ION", "top": "PQRSUWY"}),
}

# 目の色の記号（素体ごと）
EYES = {"reto": "F", "yuri": "H", "mina": "I", "guide": "I"}

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

def despeckle(frames, roles):
    """髪の、ひとりぼっちの明るい点・暗い点（上のほうで、頭の先が欠けたように見える）を、まわりの髪の色にそろえる。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        H, W = len(g), len(g[0])
        def role(ch):
            return roles[LETTERS.index(ch)] if ch != "." else None
        for _ in range(2):
            for y in range(1, 22):
                for x in range(W):
                    ch = g[y][x]
                    if role(ch) != "hair":
                        continue
                    nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H]
                    if sum(1 for c in nb if c == ch) >= 2:
                        continue
                    hair_nb = [c for c in nb if role(c) == "hair"]
                    if hair_nb:
                        g[y][x] = max(set(hair_nb), key=hair_nb.count)
        out[fk] = ["".join(r) for r in g]
    return out

def smooth_head(frames):
    """頭（上の18段）のかたちを、なめらかにする。持ち物・飾りを消した跡の、へこみ（欠け）を埋め、とび出たとげ（縁取りのかけら）を消す。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        H, W = len(g), len(g[0])
        def at(x, y):
            return g[y][x] if 0 <= x < W and 0 <= y < H else "."
        for _ in range(3):
            changes = []
            for y in range(1, 21):
                for x in range(W):
                    nb = [at(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                    filled = [c for c in nb if c != "."]
                    if g[y][x] == ".":
                        if len(filled) >= 3:
                            changes.append((x, y, max(set(filled), key=filled.count)))
                    elif len(filled) <= 1:
                        changes.append((x, y, "."))
                    elif sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and at(x + dx, y + dy) != ".") <= 2 and g[y][x] == "A":
                        changes.append((x, y, "."))   # ななめにしかつながっていない縁取りのかけら
            for x, y, c in changes:
                g[y][x] = c
        out[fk] = ["".join(r) for r in g]
    return out

REOUTLINE_MAXY = 99  # スカートの型は、すその下（足先のように見える縁取り）を足さない

def reoutline(frames):
    """縁取りが欠けているところ（絵の外へ、すき間が直接つながっているところ）に、縁取りの色を足す。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        H, W = len(g), len(g[0])
        add = []
        for y in range(min(H, REOUTLINE_MAXY + 1)):
            for x in range(W):
                if g[y][x] != ".":
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and g[ny][nx] not in ".A":
                        add.append((x, y))
                        break
        for x, y in add:
            g[y][x] = "A"
        out[fk] = ["".join(r) for r in g]
    return out

def fill_notches(frames):
    """輪郭の、1ドットぶんの小さなへこみ（髪のおでこのあたりの欠け）を埋める。左右のへりで、短い区間（3段まで）だけ内側にへこんでいるところを、まわりにそろえる。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        H, W = len(g), len(g[0])
        for side in ("L", "R"):
            def edge(y):
                xs = [x for x in range(W) if g[y][x] != "."]
                if not xs:
                    return None
                return min(xs) if side == "L" else max(xs)
            ys = range(5, 23)
            e = {y: edge(y) for y in range(H)}
            y = 5
            while y < 23:
                if e[y] is None or e[y - 1] is None:
                    y += 1
                    continue
                # へこみの区間 [y, y2]: へりが、上の段より1だけ内側
                inward = 1 if side == "L" else -1
                if e[y] == e[y - 1] + inward:
                    y2 = y
                    while y2 + 1 < 23 and e[y2 + 1] == e[y]:
                        y2 += 1
                    if y2 - y + 1 <= 3 and e[y2 + 1] is not None and e[y2 + 1] == e[y - 1]:
                        for yy in range(y, y2 + 1):
                            x_out = e[yy] - inward
                            x_in = e[yy]
                            inner = g[yy][x_in + inward]
                            g[yy][x_out] = g[yy][x_in]      # 縁取りを外へ
                            g[yy][x_in] = inner              # もとの縁取りの位置は、内側の色
                    y = y2 + 1
                else:
                    y += 1
        out[fk] = ["".join(r) for r in g]
    return out

def push_front_hair(frames):
    """横向きの髪の前（おでこの上）を1ドット前に出す。"""
    out = {}
    for fk, rows in frames.items():
        g = [list(r) for r in rows]
        if fk[:-1] in ("left", "right"):
            L = fk.startswith("left")
            for y in range(5, 12):
                xs = [x for x in range(len(g[y])) if g[y][x] != "."]
                if not xs:
                    continue
                x0 = min(xs) if L else max(xs)
                xo = x0 - 1 if L else x0 + 1
                if 0 <= xo < len(g[y]):
                    g[y][xo] = g[y][x0]
                    g[y][x0] = "B"
        out[fk] = ["".join(r) for r in g]
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
    # ミナの髪の左右のふちの濃い色（D）は、頭のところでは「髪」の色にする（飾りの色にすると、横向きで髪が欠けて見える）
    if key == "mina":
        di = LETTERS.index("D")
        hair_idx = [LETTERS.index(c) for c in groups["hair"]]
        med = sorted(lum(pal[i]) for i in hair_idx)[len(hair_idx) // 2]
        newi = len(pal)
        pal = list(pal) + [pal[di]]
        roles = roles + ["hair"]
        shade = shade + [round(max(-0.6, min(0.6, (lum(pal[di]) - med) * 1.25)), 3)]
        newl = LETTERS[newi]
        frames = {fk: ["".join(newl if (ch == "D" and y <= 17) else ch for ch in row) for y, row in enumerate(rows)] for fk, rows in frames.items()}
    REOUTLINE_MAXY = 28 if key in ("mina", "guide") else 99
    frames = symmetrize(strip(key, frames))
    frames = reoutline(fill_notches(reoutline(smooth_head(despeckle(frames, roles)))))
    if key == "mina":
        frames = reoutline(push_front_hair(push_front_hair(frames)))
    if key in ("mina", "guide"):
        # すその線（下から2段）の途切れを、縁取りの色でつなぐ
        for fk, rows in list(frames.items()):
            g = [list(r) for r in rows]
            for y in (29, 30):
                xs = [x for x, ch in enumerate(g[y]) if ch != "."]
                if len(xs) >= 6:
                    for x in range(min(xs), max(xs) + 1):
                        if g[y][x] == ".":
                            g[y][x] = "A"
            frames[fk] = ["".join(r) for r in g]
    # 目は、どの肌の色でも見えやすいよう、黒（ほんのり色つき）にする
    ei = LETTERS.index(EYES[key])
    pal = list(pal); pal[ei] = "#241820"; roles[ei] = "fixed"; shade[ei] = 0.0
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
    # 女の人の増やした2種: ミナの頭にコハクの服、コハクの頭にミナの服
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
