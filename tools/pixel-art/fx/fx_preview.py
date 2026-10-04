"""雷の術のエフェクトを、本物の戦闘画面に重ねて、コマの長さどおりの動画にする（見本）。

使い方: python3 fx_preview.py 背景.png 名前とHPの入った背景.png エフェクトのフォルダ ボスのanim.json 出力.mp4 [--slow 4] [--party 2頭身の歩く絵のフォルダ] [--set fire] [--bg 背景.png] [--ui 文字と窓.png]
  --set: lightning（雷の術、ふだん）か fire（炎の術）
  --party: 味方を新しい2頭身の絵（assets-src/characters/walk-2head/）で立たせる。背景は味方の絵のないもの（ruins-noparty.png）を使う
  背景.png: 戦闘画面（論理 400×225）から敵を抜いたもの。ゲームの描画（battle-renderer.ts）で作る
  ボスの anim.json: boss_rig.py の出力（両手を振り上げるコマを「となえる姿」に使う）
画面のつくり（battle-renderer.ts と同じ）: ボスは左（x=16, y=2, 132×132）、味方は右の地面。戦闘の場は上の169。
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FIELD_H = 169
SCALE = 3
BOSS_X, BOSS_Y, BOSS_SIZE = 16, 2, 132
CAST_POINT = (87, 10)                       # 両手を振り上げた手の上（ボスの絵 256 の (3, 137) あたり）
PARTY_FEET = [(368, 165), (354, 147), (338, 165), (324, 147)]   # 4人の足元のまん中
PARTY_MID = (346, 160)


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def rows_rgba(rows, pal):
    H, W = len(rows), len(rows[0])
    a = np.zeros((H, W, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != "." and c in pal:
                a[y, x, :3] = hex_rgb(pal[c]); a[y, x, 3] = 255
    return a


def main():
    args = sys.argv[1:]
    bg_none, bg_boss, fxdir, animp, out = args[:5]
    slow = float(args[args.index("--slow") + 1]) if "--slow" in args else 0
    base = np.array(Image.open(bg_none).convert("RGB"))
    named = np.array(Image.open(bg_boss).convert("RGB"))
    base[134:162, 0:170] = named[134:162, 0:170]          # ボスの名前とHP
    # --bg 絵.png: 戦闘の場（上の400×169）の背景をこの絵にする。--ui 文字と窓.png: ゲームと同じ細かさ（1200×675）の
    # 文字と窓（battle-ui-layer.mjs で作る）を、拡大したあとに重ねる（論理の大きさの文字を拡大すると、つぶれて読みにくかった）
    ui = None
    if "--bg" in args:
        bgimg = np.array(Image.open(args[args.index("--bg") + 1]).convert("RGB").resize((400, FIELD_H), Image.NEAREST))
        base = np.zeros((225, 400, 3), np.uint8); base[:] = (20, 14, 36); base[:FIELD_H] = bgimg
    if "--ui" in args:
        ui = Image.open(args[args.index("--ui") + 1]).convert("RGBA").resize((400 * SCALE, 225 * SCALE), Image.LANCZOS)
    # --party フォルダ: 新しい2頭身の歩く絵（16×32）を、ゲームと同じ位置に立たせる。
    # "left0"（敵の方を向いた絵）。雷に当たると flash_left（白）→ shock_left（しびれ）⇄ hurt_left（ひるむ）になり、2ドット後ろへ飛ばされる
    party = []
    if "--party" in args:
        pdir = args[args.index("--party") + 1]
        S = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        for idx, nm in enumerate(["ユーリ", "レト", "ミナ", "ガイド"]):
            d = json.load(open(f"{pdir}/{nm}.json"))
            pal = {S[i]: c for i, c in enumerate(d["palette"])}
            imgs = {k: Image.fromarray(rows_rgba(d["frames"][k], pal), "RGBA") for k in ("left0", "hurt_left", "shock_left", "flash_left", "burn_left") if k in d["frames"]}
            row, col = idx % 2, idx // 2
            party.append((imgs, 400 - 40 - col * 30 - row * 14, 225 - 56 - 4 - row * 18))
    BOLT_STATE = {3: "flash_left", 4: "shock_left", 5: "hurt_left", 6: "shock_left", 7: "hurt_left", 8: "shock_left"}
    STORM_ORDER = [4, 0, 2, 5, 1, 3]          # lightning.py の make_storm と同じ（0〜3 が味方4人）

    def party_state(effs):
        """そのコマでの、味方それぞれの（絵, 後ろへのずれ）"""
        st = [("left0", 0)] * len(party)
        for name, i, _ in effs:
            for m, key, dx in fx[name]["frames"][i].get("party", []):   # エフェクトのコマに書いてある、当たった味方の絵（炎の術など）
                if m < len(st): st[m] = (key, dx)
            if name == "bolt" and party:
                if i in BOLT_STATE: st[0] = (BOLT_STATE[i], 2)
                elif 9 <= i: st[0] = ("hurt_left", 1)
            if name == "storm":
                for k in range(min(4, len(party))):
                    sidx = i - (2 + 2 * STORM_ORDER.index(k))
                    if sidx == 1: st[k] = ("flash_left", 2)
                    elif sidx in (2, 4): st[k] = ("shock_left", 2)
                    elif sidx in (3, 5): st[k] = ("hurt_left", 2)
                    elif sidx >= 6: st[k] = ("hurt_left", 1)
        return st

    def draw_party(img, states, glowing):
        for (imgs, x, feet), (key, dx) in zip(party, states):
            if (key in ("flash_left", "shock_left", "burn_left")) != glowing:
                continue
            spr = imgs.get(key, imgs["left0"])
            if not glowing:
                sh = Image.new("RGBA", (14, 3), (0, 0, 0, 71))
                img.paste(sh, (x + 1 + dx, feet - 2), sh)
            img.paste(spr, (x + dx, feet - 29), spr)
    anim = json.load(open(animp)); apal = anim["palette"]
    boss_cache = {}

    def boss_img(key, i):
        if (key, i) not in boss_cache:
            a = rows_rgba(anim[key][i], apal)
            boss_cache[(key, i)] = Image.fromarray(a, "RGBA").resize((BOSS_SIZE, BOSS_SIZE), Image.LANCZOS)
        return boss_cache[(key, i)]

    # --set lightning（雷）/ fire（炎）: 1人用・全体用のエフェクトの名前と、画面のどこに合わせるか、字幕
    kind = args[args.index("--set") + 1] if "--set" in args else "lightning"
    SETS = {
        "lightning": ("bolt", [PARTY_FEET[0]], "storm", [PARTY_MID], "雷の術", "落雷・1人", "雷の嵐・全体"),
        "fire": ("fireball", [(0, 0)], "pillars", [PARTY_MID], "炎の術", "火球・1人", "火柱・全体"),
    }
    single, s_anchor, allfx, a_anchor, label, l1, l2 = SETS[kind]
    fx = {n: json.load(open(f"{fxdir}/{n}.json")) for n in ("charge", single, allfx, "aura") if os.path.exists(f"{fxdir}/{n}.json")}
    fx_cache = {}

    def fx_img(n, i, key="rows"):
        if (n, i, key) not in fx_cache:
            f = fx[n]["frames"][i]
            fx_cache[(n, i, key)] = Image.fromarray(rows_rgba(f[key], fx[n]["palette"]), "RGBA")
        return fx_cache[(n, i, key)]

    # 1コマ = (ボスの絵, [(エフェクト名, コマ番号, 画面の基準点)], ミリ秒, 字幕)
    REST = ("flat_attack3", 13)
    seq = []

    def idle(ms, cap):
        seq.append((REST, [], ms, cap))

    def cast(cap):
        for i in range(5):
            seq.append((("flat_attack3", i), [], anim["attack3_ms"][i], cap))
        for i, f in enumerate(fx["charge"]["frames"]):
            effs = [("charge", i, CAST_POINT)]
            if "aura" in fx and i < len(fx["aura"]["frames"]):
                effs.append(("aura", i, (BOSS_X, BOSS_Y)))
            seq.append((("flat_attack3", 5), effs, f["ms"], cap))

    def play(name, anchors, cap):
        frs = fx[name]["frames"]
        back = [11, 12, 13]
        for i, f in enumerate(frs):
            pose = ("flat_attack3", back[min(i // 2, 2)]) if i < 6 else REST
            effs = [(name, i, a) for a in anchors]
            na = len(fx["charge"]["frames"]) + i       # 発動のエフェクトの、消えていく残り
            if "aura" in fx and na < len(fx["aura"]["frames"]):
                effs.append(("aura", na, (BOSS_X, BOSS_Y)))
            seq.append((pose, effs, f["ms"], cap))

    caps = [f"{label}（発動・ため → {l1}）", f"{label}（発動・ため → {l2}）"]
    idle(700, caps[0]); cast(caps[0]); play(single, s_anchor, caps[0]); idle(900, caps[0])
    cast(caps[1]); play(allfx, a_anchor, caps[1]); idle(1000, caps[1])
    if slow:
        fx_names = None
        c = f"ゆっくり（{int(slow)}倍おそく）: 発動 → {l1}"
        seq += [(p, e, ms * slow, c) for p, e, ms, _ in [s for s in seq if s[1] and s[3] == caps[0]]]
        idle(500, c)
        c = f"ゆっくり（{int(slow)}倍おそく）: 発動 → {l2}"
        seq += [(p, e, ms * slow, c) for p, e, ms, _ in [s for s in seq if s[1] and s[3] == caps[1]]]
        idle(800, c)

    font = ImageFont.truetype(FONT, 30)
    tmp = tempfile.mkdtemp()
    lines = []
    for k, (pose, effs, ms, cap) in enumerate(seq):
        f0 = fx[effs[0][0]]["frames"][effs[0][1]] if effs else {"dim": 0, "flash": 0, "shake": 0}
        dk = f0["dim"] * 0.72
        pst = party_state(effs)
        img = Image.fromarray(base.copy())
        draw_party(img, pst, False)                 # ふつう・ひるむ姿は、画面といっしょに暗くする
        a = np.array(img).astype(float)
        a[:FIELD_H] = a[:FIELD_H] * (1 - dk) + np.array([18, 8, 40]) * dk
        img = Image.fromarray(a.astype(np.uint8))
        # 発動のエフェクトの奥の半分（ボスのうしろ）
        for name, i, (sx, sy) in effs:
            f = fx[name]["frames"][i]
            if "back" in f:
                ax, ay = fx[name]["anchor"]; im = fx_img(name, i, "back")
                img.paste(im, (sx - ax + f["bx"], sy - ay + f["by"]), im)
        b = np.array(boss_img(*pose)).astype(float)
        b[..., :3] = b[..., :3] * (1 - dk) + np.array([18, 8, 40]) * dk
        bi = Image.fromarray(b.astype(np.uint8), "RGBA")
        img.paste(bi, (BOSS_X, BOSS_Y), bi)
        for name, i, (sx, sy) in effs:
            f = fx[name]["frames"][i]; ax, ay = fx[name]["anchor"]
            if "at" in f:          # コマごとに画面の置き場所がある（飛んでいく火の玉など）
                sx, sy = f["at"]
            im = fx_img(name, i)
            ox, oy = sx - ax + f["x"], sy - ay + f["y"]
            # 戦闘の場（上の169）の中だけに描く
            crop_h = max(0, min(im.height, FIELD_H - oy))
            if crop_h > 0:
                part = im.crop((0, 0, im.width, crop_h))
                img.paste(part, (ox, oy), part)
        # 白・しびれ・燃える姿は、光っているので暗くせず、稲妻・炎より手前に描く（稲妻にかくれて、ダメージの絵が見えなかった）
        draw_party(img, pst, True)
        a = np.array(img).astype(float)
        if f0["flash"]:
            fc = np.array(hex_rgb(f0.get("flash_color", "#ffffff")))
            a[:FIELD_H] = a[:FIELD_H] * (1 - f0["flash"] * 0.6) + fc * f0["flash"] * 0.6
        if f0["shake"]:
            s = f0["shake"] * (1 if k % 2 else -1)
            a[:FIELD_H] = np.roll(a[:FIELD_H], s, axis=1)
        img = Image.fromarray(a.astype(np.uint8)).resize((400 * SCALE, 225 * SCALE), Image.NEAREST)
        if ui is not None:
            img = img.convert("RGBA"); img.alpha_composite(ui); img = img.convert("RGB")
        card = Image.new("RGB", (400 * SCALE, 225 * SCALE + 55), (24, 18, 40))
        card.paste(img, (0, 0))
        ImageDraw.Draw(card).text((16, 225 * SCALE + 10), cap, font=font, fill=(242, 193, 78))
        p = f"{tmp}/{k:04d}.png"; card.save(p)
        lines.append(f"file '{p}'\nduration {ms / 1000:.3f}")
    lines.append(f"file '{tmp}/{len(seq) - 1:04d}.png'")
    # 効果音を合わせるための「いつ・どのエフェクトの・何コマ目」（出力.timeline.json）。ゆっくりの所は slow に倍率
    tl, t = [], 0.0
    for pose, effs, ms, cap in seq:
        tl.append({"t": round(t, 3), "effs": [[n, i] for n, i, _ in effs], "slow": ("ゆっくり" in cap) and slow or 1})
        t += ms / 1000
    json.dump(tl, open(os.path.splitext(out)[0] + ".timeline.json", "w"), ensure_ascii=False)
    open(f"{tmp}/list.txt", "w").write("\n".join(lines))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
                    "-vf", "fps=60,format=yuv420p", "-c:v", "libx264", "-crf", "20", out], check=True)
    print("動画:", out, tmp, round(sum(s[2] for s in seq) / 1000, 1), "秒", len(seq), "枚")


if __name__ == "__main__":
    main()
