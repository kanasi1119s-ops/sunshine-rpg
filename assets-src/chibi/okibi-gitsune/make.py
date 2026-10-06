"""燠火狐（おきびぎつね。2頭身の歩くモンスター・4本足）を、3つの型で作って見比べる。
2026-10-07、人間の指示「このパターン記録しよう。ほかのモンスターでもやってみて」。
型は .claude/skills/make-art/prompt-chibi-from-reference.md の「モンスターの歩く絵の3つの型」（立たせない）:
- v16x16/ … 16×16 だけ
- mix/    … 下・上は 16×32（見下ろしで体が奥へのびる）、横は 32×16（低く長い横姿）
- v16x32/ … 16×32 だけ（横は 16×16 の横姿を下にそろえて置く）
イメージ画像は ref.png（Stable Diffusion 1.5）。残した特ちょう: 灰色の体／燃えるような橙の頭と、しっぽの橙の帯／
黒い耳の先と黒い足先／白いほおと口もと。
使い方: python3 make.py → 各フォルダに walker.json・sheet*.txt/json（エディタ用）・sheet*.png・sheet*_x8.png・walk.gif"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import monster_walk as mw  # noqa: E402
from monster_walk import mirror, put_leg, sway, finish, save, ORDER  # noqa: E402

HERE = pathlib.Path(__file__).parent
PAL = {
    "A": "#1c1418",  # 縁取り
    "a": "#3a2e30",  # 中の縁取り
    "B": "#4a4a52",  # 灰の暗
    "C": "#76767e",  # 灰の地
    "D": "#a4a4ae",  # 灰の明
    "P": "#a8380e",  # 橙の暗
    "Q": "#ec5a18",  # 橙の地
    "R": "#ff9c4a",  # 橙の明
    "W": "#f4ece4",  # 白（ほお・口もと）
    "V": "#c4b8b0",  # 白の影
    "K": "#161214",  # 黒（耳の先・足先）
    "J": "#2a1a0a",  # 目
    "E": "#f0b030",  # 目の光（こはく色）
    "N": "#0c0a0a",  # 鼻
    "S": "#ff8c8c",  # ほおの桃色
}
mw.LEG_L = ["AA.", "DCC", "CBB", "KKA"]          # 灰色の足に黒い足先
mw.LEG_R = [".AA", "BCB", "BBB", "AKK"]

# かわいくする（2026-10-07、人間の指示「狐もっとかわいくして」）: 頭をもっと大きく、体を短く、
# 目を2×3の大きな黒目に白い光、耳の内側を明るい橙、ほおに桃色、口もとは小さく、しっぽは丸くふくらませる。

# ---- 16×32 下向き（頭が手前、体としっぽが奥へのびる） ----
L_DOWN = mirror([
    "....AAAA",   # 0  しっぽの先（灰。丸くふくらむ）
    "...ADDDC",
    "..ADDCCC",
    "..ADCCCC",
    "..AQRQQQ",   # 4  しっぽの橙の帯
    "..AQQQQQ",
    "...APQQQ",
    "....ABCC",   # 7  しっぽの付け根
    "...ABCDC",   # 8  背中（短く）
    "..ABCCDC",
    "..ABCCCC",
    "...ABCCC",
    ".AA.ABCC",   # 12 耳の先（黒）
    "AKKAAACC",
    "AKRKAAAA",
    "AQRRQAQQ",   # 15 耳の内側（明るい橙）
    "AQRRQQQQ",
    "AQQQQQQQ",   # 17 頭（大きく丸く）
    "AQRQQQQQ",
    "AQQQQQQQ",
    "AQQWJQQQ",   # 20 目（大きな黒目に白い光）
    "AQQJJQQQ",
    "AQQJJQQQ",
    "AQSSQWWW",   # 23 ほおの桃色・白い口もと
    ".AQQWWWN",   # 24 鼻
    ".AQQWWWW",
    "..AQQWWV",
    "...AAVVV",
    "....ACCC",   # 28 胸
    "....ABCC",
    ".....AAA",
])
# ---- 16×32 上向き（頭が奥、しっぽが手前） ----
L_UP = mirror([
    ".AA.....",   # 0  耳の先
    "AKKA....",
    "AKQKA...",
    "AQQQQA..",
    "AQQQQQAA",
    "AQRQQQQQ",   # 5  頭の後ろ（大きく丸く）
    "AQQQQQQQ",
    "AQQQQQQQ",
    "APQQQQQQ",
    ".APQQQQQ",
    "..APPQQQ",
    "....ABCC",   # 11 首
    "...ABCDC",   # 12 背中（短く）
    "..ABCCDC",
    "..ABCCCC",
    "...ABCCC",
    "....ABCC",   # 16 しっぽの付け根
    "...ACCCC",
    "..ACCCCC",
    "..AQQRQQ",   # 19 橙の帯
    "..AQQQQQ",
    "..APQQQQ",
    "..ACCCCC",
    "..ADCCCC",   # 23 しっぽの先（丸く）
    "...ADDDC",
    "....AAAA",
])


def long_frames():
    fr = {}
    for f in range(3):
        g = list(L_DOWN) + ["." * 16]
        a, b = {0: (26, 26), 1: (27, 25), 2: (25, 27)}[f]   # 前足（頭の左右）
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (9, 9), 1: (8, 10), 2: (10, 8)}[f]       # 後ろ足
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(0, 4), -1 if f == 1 else 1)       # しっぽの先がゆれる
        fr[f"down{f}"] = g
        g = list(L_UP) + ["." * 16] * 6
        a, b = {0: (9, 9), 1: (8, 10), 2: (10, 8)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (14, 14), 1: (15, 13), 2: (13, 15)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(22, 26), -1 if f == 1 else 1)
        fr[f"up{f}"] = [ "." * 16] * 5 + g[:27]              # 下をそろえる
    return fr


# ---- 32×16 横向き（左向き。頭が左、しっぽが右上へ） ----
W_TOP = [
    "......AA........................",   # 0  耳（手前の耳が大きく、奥の耳は小さく）
    "..AA.AKKA............AAAAA......",
    ".AKKAAKRKA..........ADDDDCA.....",   # 2  耳の内側・しっぽの先（丸くふくらむ）
    "AQRRQQRRQQA........ADDCCCCCA....",
    "AQQQQQQQQQQA.......ACCCCCCCA....",
    "AQRQQQQQQQQQA......AQQRQQQQA....",   # 5  しっぽの橙の帯
    "AQQWJQQQQQQQAAAAAAAQQQQQQQA.....",   # 6  目（大きな黒目に白い光）
    "AQQJJQQQQQQQACDDDCCCAQQQQBA.....",
    "NWQJJSQQQQQAACCCCCCCCAPPBA......",   # 8  鼻・ほおの桃色
    "AWWQQSQQQQQACCCCCCCCCCAAA.......",
    ".AWWWQQQQQACCCCCCCCCCBA.........",
    "..AVWWQQQACBCCCCCCCBBA..........",
    "...AAAAAAABBBBBBBBBBA...........",
]
W_LEGS = {
    0: ["........ACCA....ACCA............", "........ACCA....ACCA............", ".......AKKKA...AKKKA............"],
    1: [".......ACCA......ABBA...........", "......ACCA........ABBA..........", ".....AKKKA........AKKKA........."],
    2: [".........ABBA..ACCA.............", "..........ABBAACCA..............", ".........AKKKAKKKA.............."],
}


def wide_frames():
    return {f"left{f}": W_TOP + [r[:32] for r in W_LEGS[f]] for f in range(3)}


# ---- 16×16 ----
S_DOWN = mirror([
    ".AA.....",   # 0  耳
    "AKKA....",
    "AKRKA...",
    "AQRRQAAA",
    "AQQQQQQQ",   # 4  頭（ほとんど頭だけ）
    "AQRQQQQQ",
    "AQQWJQQQ",   # 6  目
    "AQQJJQQQ",
    "AQSSQWWW",   # 8  ほお・口もと
    ".AQQWWWN",   # 9  鼻
    "..AQWWWV",
    "...AAVVV",
    "....ACCC",   # 12 胸
    ".....AAA",
])
S_UP = mirror([
    ".AA.....",
    "AKKA....",
    "AKQKA...",
    "AQQQQAAA",
    "AQQQQQQQ",
    "AQRQQQQQ",
    "APQQQQQQ",
    ".APPQQQQ",
    "...ABCCC",   # 8  背中
    "...ABCDC",
    "....AQQR",   # 10 しっぽの橙の帯
    "...AQQQQ",
    "...ACCCC",
    "....ADDC",
    ".....AAA",
])
S_SIDE = [
    "....A...........",   # 0  耳（横から見ても分かるよう、手前の耳を橙の三角で高く立て、奥の耳は小さく離す。人間の指示「横から見たとき耳がわからない」）
    ".A.AKA.....AAA..",
    "AKAQRQA...ADDDA.",   # 2  しっぽの先（丸く）
    "..AQRRQQA.ACCCDA",   # 3  おでこを2ドット下げて、口もとを前へ突き出す（人間の指示「口元の白いの増やして。口を突き出す感じ」「もう少し突き出していいかな」）
    "..AQQQQQAAAQRQQA",   # 4  しっぽの橙の帯
    "..AQWJQQQAAQQQQA",   # 5  目（前側の黒い点はなし）
    ".AWQJJSQQACAQQBA",   # 6  口もとの上（白）
    "NWWWQQQQACCCAPA.",   # 7  鼻の頭と、白い口もと
    "AWWWWQQACCCCCBA.",   # 8  下あご（白く前へ）
    ".AVWWWACCCCCBA..",
    "..AAAACCCCCBA...",
    "....ABBBBBBA....",
]
S_LEGS = {0: ["....ACA.ACA.....", "...AKKAAKKA.....", "................", "................"],
          1: ["...ACA...ABA....", "..AKKA...AKKA...", "................", "................"],
          2: [".....ABAACA.....", ".....AKKKKA.....", "................", "................"]}


def small_frames():
    fr = {}
    for f in range(3):
        g = list(S_DOWN) + ["." * 16]
        a, b = {0: (10, 10), 1: (11, 9), 2: (9, 11)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        fr[f"down{f}"] = g
        g = list(S_UP) + ["." * 16]
        # 後ろから見た足（人間の指示「後ろから見たとき足が前しか見えない」）: 前足は体の左右に小さく、後ろ足はしっぽの左右に。前と後ろは逆に出す
        BL, BR = ["ACB", "ACB", "KKA"], ["BCA", "BCA", "AKK"]
        a, b = {0: (7, 7), 1: (6, 8), 2: (8, 6)}[f]          # 前足（奥）
        put_leg(g, a, True, BL, 1); put_leg(g, b, False, BR, 12)
        a, b = {0: (12, 12), 1: (13, 11), 2: (11, 13)}[f]    # 後ろ足（手前）
        put_leg(g, a, True, BL, 1); put_leg(g, b, False, BR, 12)
        if f:
            sway(g, range(11, 15), -1 if f == 1 else 1)
        fr[f"up{f}"] = g
        fr[f"left{f}"] = S_SIDE + S_LEGS[f]
    return fr


def main():
    long = finish(long_frames(), 16, 32)
    small = finish(small_frames(), 16, 16)
    wide = finish(wide_frames(), 32, 16)
    du = {k: v for k, v in long.items() if k[:-1] in ("down", "up")}
    tall_side = {k: ["." * 16] * 16 + v for k, v in small.items() if k[:-1] in ("left", "right")}
    save(HERE, "v16x32", [("all", {**du, **tall_side}, 16, 32, ORDER)], PAL)
    save(HERE, "v16x16", [("all", small, 16, 16, ORDER)], PAL)
    save(HERE, "mix", [("down-up", du, 16, 32, ["down", "up"]), ("side", wide, 32, 16, ["left", "right"])], PAL)


if __name__ == "__main__":
    main()
