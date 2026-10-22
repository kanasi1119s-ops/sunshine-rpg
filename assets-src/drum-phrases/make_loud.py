# ラウドロック・メタルコア・メタル向けの8小節フレーズを、一般的な型から自作する（2026-10-22）。
# GMD（プロのドラマーの演奏）にはツーバス・ハーフタイムのブレイクダウン・ブラスト・チャイナのアクセントがほとんど無いため、
# ドラムの教本・レッスンで一般に教えられている型（特定の曲の写しではない）を組み合わせて足す。
# 8小節の中の変化は docs/sound/modern-loud-rock/arrangement-detail.md 5-2 の「変化の予定表」に従う:
#   1 小節目 クラッシュ／2・6 ゴーストの位置を変える／3 キックを1つ足す／4 小さいフィル（最後の1拍）／
#   5 2枚目のシンバル／7 ハットを開く・ライドのベル／8 大きいフィル（最後の2拍か1小節。前と違う種類）
# 使い方: python3 -I make_loud.py <出力 json>
import json, sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify

E16 = "." * 16
def bar(k=E16, s=E16, h=E16, t=E16, c=E16):
    for v in (k, s, h, t, c): assert len(v) == 16, (k, s, h, t, c)
    return dict(k=k, s=s, h=h, t=t, c=c)

def rep(x, n=16): return (x * 16)[:n]

# ── グルーヴの型（1小節。top は刻むシンバルの種類）──
# (名前, 区分, bpm の範囲, キック, スネア, 刻み, 刻みの楽器, 説明)
GROOVES = [
    ("rock8", "loudrock", (110, 150), "X.......X.x.....", "....X.......X...", "x.x.x.x.x.x.x.x.", "hat", "8ビート（ラウドロックのAメロ）"),
    ("rock8sync", "loudrock", (120, 160), "X..X..X...X.....", "....X.......X...", "x.x.x.x.x.x.x.x.", "hat", "キックがギターのアクセントに沿う 3+3+2 の8ビート"),
    ("mcverse", "metalcore", (130, 170), "X..X..X.X...X...", "....X.......X...", "x.x.x.x.x.x.x.x.", "ride", "メタルコアのAメロ（ライド8分・キックはリフに沿う）"),
    ("open8", "loudrock", (120, 160), "X.......X.x.....", "....X.......X...", "x.O.x.O.x.O.x.O.", "hat", "裏拍でハットを開く（サビ）"),
    ("crash8", "loudrock", (130, 170), "X...X.x.X...X.x.", "....X.......X...", "c.c.c.c.c.c.c.c.", "crash", "クラッシュの8分（サビの壁）"),
    ("twobass16", "metal", (140, 190), "XxXxXxXxXxXxXxXx", "....X.......X...", "x.x.x.x.x.x.x.x.", "ride", "ツーバス16分（スネア2・4）"),
    ("twobass16half", "metalcore", (140, 180), "XxXxXxXxXxXxXxXx", "........X.......", "n...n...n...n...", "china", "ツーバス16分＋ハーフのスネア＋チャイナ4分"),
    ("twobass8", "metal", (160, 210), "x.x.x.x.x.x.x.x.", "....X.......X...", "x...x...x...x...", "crash", "ツーバス8分（速いテンポで16分の代わり）"),
    ("gallop", "metal", (140, 190), "X.xxX.xxX.xxX.xx", "....X.......X...", "x.x.x.x.x.x.x.x.", "hat", "ギャロップ（8分＋16分2つ）"),
    ("revgallop", "metal", (140, 180), "XxX.XxX.XxX.XxX.", "....X.......X...", "x.x.x.x.x.x.x.x.", "ride", "逆ギャロップ（16分2つ＋8分）"),
    ("dbeat", "punk", (160, 200), "X.....x.X.....x.", "....X.......X...", "c.c.c.c.c.c.c.c.", "crash", "Dビート寄り（キック・スネア・キックキック・スネア）"),
    ("skank", "punk", (170, 210), "x...x...x...x...", "..x...x...x...x.", "x...x...x...x...", "ride", "スカンク（2ビート。キックとスネアが8分で交互）"),
    ("blastalt", "metal", (180, 230), "x.x.x.x.x.x.x.x.", ".x.x.x.x.x.x.x.x", "x.x.x.x.x.x.x.x.", "crash", "ブラスト寄り（交互。強さは控えめ）"),
    ("blasthammer", "metal", (170, 220), "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "ride", "ブラスト寄り（ハンマー。キックとスネアが同時に8分）"),
    ("halfbd", "metalcore", (120, 160), "X.......X.x...x.", "........X.......", "n...n...n...n...", "china", "ハーフタイムのブレイクダウン（チャイナ4分）"),
    ("chugbd", "metalcore", (110, 150), "X..X..X...X.X...", "........X.......", "n...n...n...n...", "china", "ギターの刻みにキックが沿うブレイクダウン"),
    ("halfslow", "metalcore", (100, 140), "X.........X.....", "........X.......", "n.......n.......", "china", "2分音符のチャイナで重く遅いブレイクダウン"),
    ("djent332", "metalcore", (110, 150), "X..X..X.X..X..X.", "........X.......", "x...x...x...x...", "ride", "3+3+2 の引っかけ（ハーフのスネア・ライド4分）"),
    ("fourfloor", "loudrock", (120, 140), "X...X...X...X...", "....X.......X...", "..O...O...O...O.", "hat", "4つ打ち＋裏のオープンハット（ダンスロック寄り）"),
    ("bellgroove", "metalcore", (120, 160), "X.....X.X..X....", "....X.......X...", "u.r.u.r.u.r.u.r.", "bell", "ライドのベル（カップ）とライド本体を交互"),
    ("tomgroove", "loudrock", (100, 140), "X.......X.......", "....x.......x...", "4.44.4.44.4.44.4", "tom", "フロアタムで刻むブリッジ（トライバル）"),
    ("halfride", "loudrock", (130, 170), "X.......x.x.....", "........X.......", "x.x.x.x.x.x.x.x.", "ride", "ハーフタイム（スネア3拍目・ライド8分）"),
    # 繊細な場面（2026-10-22 人間「激しすぎ・音が強すぎ→繊細さも」）
    ("softverse", "ballad", (70, 110), "x.......x.......", "....x.......x...", "o.o.o.o.o.o.o.o.", "hat", "静かなAメロ（弱いハット8分・スネアは軽く）"),
    ("softride", "ballad", (70, 110), "x.........x.....", "........x.......", "r.r.r.r.r.r.r.r.", "ride", "ライドだけの静かな刻み（ハーフ）"),
    ("ghostgroove", "loudrock", (90, 120), "X.....x...x.....", "..o.X..o.o..X..o", "x.x.x.x.x.x.x.x.", "hat", "ゴースト入りの軽い16分の揺れ"),
    ("pulse", "ballad", (70, 120), "x.......x.......", E16, E16, "none", "キックだけの鼓動（イントロ・間）"),
]

# 刻みの文字列 → (h, c, t) の格子に
def top_to(tp, kind):
    h = c = t = E16
    if kind in ("hat",): h = tp
    elif kind == "tom": t = tp
    elif kind == "none": pass
    else:
        m = {"ride": "r", "crash": "c", "china": "n", "bell": None}
        c = "".join("." if ch == "." else (ch if kind == "bell" else m[kind]) for ch in tp)
        if kind in ("ride", "bell"):  # ライドの下で左足のハイハット（2・4拍）
            h = "....o.......o..."
    return h, c, t

# ── 小さいフィル（最後の1拍＝4マス）: (s, k, t, c)
SMALL = [
    ("..xX", None, None, None, "スネア"), (None, None, "1234", None, "タム下り"), ("xxxX", None, None, None, "スネア連打"),
    (None, "X...", "2.44", None, "タム下り"), ("o.oX", None, None, None, "ゴースト"), (None, "..XX", None, None, "キック連打"),
    ("X...", "X...", None, "s...", "一撃"), ("....", "....", None, None, "間"),
]
# ── 大きいフィル（最後の2拍＝8マス、"bar" は1小節＝16マス）: (s, k, t, c, 種類)
BIG = [
    ("........", "x...x...", "11223344", "........", "タム下り"),
    ("xxxx....", "x.....xx", "....2244", "........", "タム下り"),
    ("X..X..X.", "X..X..X.", "........", "n..n..n.", "一撃"),
    ("X.......", "X.......", "........", "c.......", "間"),
    ("X...X...", "XXXXXXXX", "........", "........", "キック連打"),
    ("x.x.xxXX", "x.......", "........", "........", "スネア連打"),
    ("x..x..x.", ".x..x..x", "..1..2..", "........", "リニア"),
    ("X.......", "....x...", "....D...", "........", "フラム風の4分"),
    ("..xxxxXX", "x.......", "........", "........", "スネア連打"),
    ("x.......", "..x...x.", ".1..2.4.", "........", "タム下り"),
    ("o.o.ooxX", "x.....x.", "........", "........", "ゴースト"),
    ("........", "......XX", "1.2.3.4.", "........", "タム下り"),
    ("bar", "x.x.x.x.xxxxXXXX", "x...x...x...x...", E16, E16, "スネア連打"),
    ("bar", "xxxx....xxxx....", "x.......x.......", "....1122....3344", E16, "タム下り"),
    ("bar", E16, "X...............", E16, "C...............", "間"),
    ("bar", "X.....X.....X...", "X.....X.....X...", E16, "N.....N.....N...", "一撃"),
]

def put(row, a, seg):
    return row[:a] + seg + row[a + len(seg):]

def make(g, variant, seed, dyn, top_alt=None, fill_order=None):
    rnd = random.Random(seed)
    name, style, (b0, b1), K, S, T, kind, desc = g
    if top_alt: T, kind = top_alt
    h0, c0, t0 = top_to(T, kind)
    bars = []
    fills_order = fill_order or rnd.sample(range(len(BIG)), len(BIG))
    small = rnd.sample(range(len(SMALL)), 2)
    for bi in range(8):
        k, s, h, c, t = K, S, h0, c0, t0
        # 強さ（soft は全体を一段弱く、hard はバックビートとシンバルを強く）
        if dyn == "soft":
            k = k.replace("X", "x"); s = s.replace("X", "x"); h = h.replace("X", "x").replace("x", "o") if kind == "hat" else h
        elif dyn == "hard":
            s = "".join("X" if ch == "x" and i in (4, 8, 12) else ch for i, ch in enumerate(s))
        # ハイハットの強弱（1拍目＞3拍目＞2・4拍目＞裏拍）
        if kind == "hat" and dyn != "soft":
            h = "".join(("X" if i == 0 else ("x" if i % 4 == 0 else ("o" if i % 2 else "x"))) if ch == "x" else ch for i, ch in enumerate(h))
        j = bi
        if j in (0, 4) and K[0] != ".":
            cym = "c" if j == 0 else rnd.choice(["g", "n", "s"]) if style != "ballad" else "g"
            if dyn == "soft": cym = "g" if j == 4 else "c"
            c = put(c, 0, cym.upper() if dyn == "hard" else cym); h = put(h, 0, ".")
        if j in (1, 5) and dyn != "soft" and kind != "none":   # ゴーストの位置を変える
            pos = 7 if j == 1 else rnd.choice([11, 15, 3])
            if s[pos] == "." and s[pos - 1] == "." and (pos + 1 > 15 or s[pos + 1] == "."): s = put(s, pos, "o")
        if j == 2 and k[14] == "." and k[12] == ".": k = put(k, 14, "x")
        if j == 6:
            if kind == "hat" and h[14] != ".": h = put(h, 14, "O")
            elif kind in ("ride", "bell") and dyn != "soft": c = put(c, 0, "u"); c = put(c, 8, "u")
        if j == 3:
            sn, kc, tm, cy, _ = SMALL[small[0]]
            s, h = put(s, 12, sn or "...."), put(h, 12, "....")
            if kind != "hat": c = put(c, 12, cy or "....")
            elif cy: c = put(c, 12, cy)
            if kc: k = put(k, 12, kc)
            if tm: t = put(t, 12, tm)
        if j == 7:
            f = BIG[fills_order[variant % len(BIG)]]
            if f[0] == "bar":
                _, s, k, t, c, _ = f; h = E16
                if dyn == "soft": s = s.replace("X", "x"); k = k.replace("X", "x"); t = t.translate(str.maketrans("ABCD", "1234"))
            else:
                sn, kc, tm, cy, _ = f
                s, k, t = put(s, 8, sn), put(k, 8, kc), put(t, 8, tm); h = put(h, 8, "." * 8); c = put(c, 8, cy)
                if dyn == "soft": s = s.replace("X", "x"); k = k.replace("X", "x"); c = c.lower()
        # 手は2本まで: シンバル・タムと重なる閉じたハットは消す（ペダルの o は残す）
        h = "".join("." if (c[i] != "." or t[i] != ".") and h[i] != "o" else h[i] for i in range(16))
        bars.append(bar(k, s, h, t, c))
    bpm = rnd.randrange(b0, b1 + 1, 5)
    return dict(id=f"loud:{name}-{variant + 1:02d}{dyn[0]}", source="自作（一般的な型）", style=style, sub=name, bpm=bpm,
                drummer="", desc=desc, bars=bars, swing=0.5)

def build():
    out = []; seen = set(); n = 0
    alt_tops = {"rock8": [("x.x.x.x.x.x.x.x.", "ride"), ("u...u...u...u...", "bell")],
                "twobass16": [("c...c...c...c...", "crash"), ("n...n...n...n...", "china")],
                "gallop": [("c...c...c...c...", "crash")], "halfbd": [("c...c...c...c...", "crash")],
                "mcverse": [("x.x.x.x.x.x.x.x.", "hat")], "dbeat": [("x.x.x.x.x.x.x.x.", "ride")]}
    for gi, g in enumerate(GROOVES):
        soft_ok = g[1] in ("ballad", "loudrock") or g[0] in ("halfride", "mcverse", "djent332", "bellgroove")
        dyns = ["soft", "mid"] if g[1] == "ballad" else (["mid", "hard"] + (["soft"] if soft_ok else []))
        tops = [None] + alt_tops.get(g[0], [])
        for v in range(3 if g[1] != "ballad" else 3):
            for dyn in dyns:
                ta = tops[v % len(tops)]
                ph = make(g, v + gi, seed=1000 + gi * 37 + v * 7 + len(dyn), dyn=dyn, top_alt=ta)
                key = json.dumps(ph["bars"])
                if key in seen: continue
                seen.add(key); out.append(classify.classify(ph))
    return out

if __name__ == "__main__":
    P = build()
    json.dump(P, open(sys.argv[1], "w"), ensure_ascii=False)
    print("自作フレーズ", len(P))
