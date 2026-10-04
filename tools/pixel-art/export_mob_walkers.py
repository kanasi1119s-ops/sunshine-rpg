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

out = {}
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
    out[key] = {"palette": pal, "roles": roles, "shade": shade, "frames": frames}

ts = (
    "// 自動生成: tools/pixel-art/export_mob_walkers.py（手で編集しない）。町の人（モブ）の2頭身の素体4種\n"
    "export interface MobTemplate {\n  palette: string[];\n  roles: string[];\n  shade: number[];\n  frames: Record<string, string[]>;\n}\n\n"
    "export const MOB_TEMPLATES: Record<string, MobTemplate> = " + json.dumps(out, ensure_ascii=False) + ";\n"
)
(ROOT / "src/game/sprite/mob-walker-data.generated.ts").write_text(ts, encoding="utf-8")
print("書き出し:", ", ".join(out), len(ts) // 1024, "KB")
