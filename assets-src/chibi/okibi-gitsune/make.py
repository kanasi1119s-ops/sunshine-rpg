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
}
mw.LEG_L = ["AA.", "DCC", "CBB", "KKA"]          # 灰色の足に黒い足先
mw.LEG_R = [".AA", "BCB", "BBB", "AKK"]

# ---- 16×32 下向き（頭が手前、体としっぽが奥へのびる） ----
L_DOWN = mirror([
    ".....AAA",   # 0  しっぽの先（灰。ふさふさと太く）
    "....ADDC",
    "...ADCCC",
    "...ACCCC",
    "...AQRQQ",   # 4  しっぽの橙の帯
    "...AQQQQ",
    "....APQQ",
    "....ABCC",   # 7  しっぽの付け根
    "...ABCCC",
    "...ABCDC",   # 9  背中
    "..ABCCDC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "...ABCCC",
    "..AA.ABC",   # 16 耳の先（黒）
    "..AKA.AC",
    "..AKQAQQ",
    "..AQRQQQ",
    ".AQRQQQQ",   # 20 頭（橙）
    ".AQQQQQQ",
    ".AQQQQQQ",
    ".AQQJEQQ",   # 23 目
    ".AWQQQQQ",   # 24 白いほお
    ".AWWQQQQ",
    "..AWWWQQ",
    "..AVWWWN",   # 27 鼻
    "...AVWWW",
    "....AAVW",
    "......AA",
])
# ---- 16×32 上向き（頭が奥、しっぽが手前） ----
L_UP = mirror([
    "..AA....",   # 0  耳の先
    "..AKA...",
    "..AKQA..",
    "..AQQQAA",
    ".AQRQQQQ",   # 4  頭の後ろ（橙）
    ".AQQQQQQ",
    ".AQQQQQQ",
    ".APQQQQQ",
    "..APQQQQ",
    "...APPQQ",
    "....ABCC",   # 10 首
    "...ABCDC",
    "..ABCCDC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "..ABCCCC",
    "...ABCCC",
    "....ABCC",
    "....ABCC",   # 22 しっぽ（手前へ。ふさふさと太く）
    "...ABCCC",
    "...AQQRQ",   # 24 橙の帯
    "...AQQQQ",
    "...APQQQ",
    "...ACCCC",
    "...ADCCC",
    "....ADDC",
    ".....AAA",
])


def long_frames():
    fr = {}
    for f in range(3):
        g = list(L_DOWN) + ["." * 16]
        a, b = {0: (27, 27), 1: (28, 26), 2: (26, 28)}[f]   # 前足（頭の左右）
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (13, 13), 1: (12, 14), 2: (14, 12)}[f]   # 後ろ足
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(0, 4), -1 if f == 1 else 1)       # しっぽの先がゆれる
        fr[f"down{f}"] = g
        g = list(L_UP) + ["." * 16]
        a, b = {0: (9, 9), 1: (8, 10), 2: (10, 8)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        a, b = {0: (19, 19), 1: (20, 18), 2: (18, 20)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        if f:
            sway(g, range(27, 31), -1 if f == 1 else 1)
        fr[f"up{f}"] = g
    return fr


# ---- 32×16 横向き（左向き。頭が左、しっぽが右上へ） ----
W_TOP = [
    "...A.A..........................",   # 0  耳の先
    "..AKAKA.................AAA.....",
    "..AKQKQA...............ACDDA....",   # 2  しっぽの先（灰）
    ".AQRQQQQA.............ACCCDA....",
    ".AQRQQQQQA...AAAAAAA..ACCQQCA...",
    "AQRQEJQQQQAAACDDDDDCAACCQRQCA...",   # 5  目・背中・しっぽの橙の帯
    "AQQQQQQQPQACCDCCCCCCCCCQRQQBA...",
    "AWWQQQQPPACCCCCCCCCCCCBQQQBA....",
    "NWWWQQPPACCCCCCCCCCCCBCBQBBA....",   # 8  鼻
    "AVWWWPPACCCCCCCCCCCCCBCBBBA.....",
    ".AVVWWACBCCCCCCCCCCCBBBAAA......",
    "..AAAABBCCBBBBBBBBBBBBA.........",
    "......ABBBAAAAAAAAABBBA.........",
]
W_LEGS = {
    0: ["......ACCA.........ACCA.........", "......ACCA.........ACCA.........", ".....AKKKA........AKKKA........."],
    1: [".....ACCA..........ABBA.........", "....ACCA............ABBA........", "...AKKKA............AKKKA......."],
    2: ["......ABBA........ACCA..........", ".......ABBA......ACCA...........", ".......AKKKA....AKKKA............"],
}


def wide_frames():
    return {f"left{f}": W_TOP + [r[:32] for r in W_LEGS[f]] for f in range(3)}


# ---- 16×16 ----
S_DOWN = mirror([
    "..A.....",   # 0  耳
    ".AKA....",
    ".AKQA...",
    ".AQQQAAA",
    "AQRQQQQQ",   # 4  頭
    "AQQQQQQQ",
    "AQQJEQQQ",   # 6  目
    "AWQQQQQQ",
    "AWWQQQQQ",
    ".AWWWWQN",   # 9  鼻
    "..AVWWWW",
    "...AAVVV",
    "....ACCC",   # 12 胸
    "....ABCC",
    ".....AAA",
])
S_UP = mirror([
    "..A.....",
    ".AKA....",
    ".AKQA...",
    ".AQQQAAA",
    "AQRQQQQQ",
    "AQQQQQQQ",
    ".APQQQQQ",
    "..APPQQQ",
    "...ABCCC",   # 8  背中
    "...ABCDC",
    "...ABCCC",
    "....AQQR",   # 11 しっぽの橙の帯
    "....AQQQ",
    "....ACDC",
    ".....AAA",
])
S_SIDE = [
    "..A.A...........",   # 0  耳
    ".AKAKA......AA..",
    ".AKQKQA....ACDA.",   # 2  しっぽの先
    "AQRQQQQA..ACCQA.",
    "AQEJQQQAAAAQRQA.",   # 4  目・しっぽの橙
    "AQQQQQQACCCAQQA.",
    "NWWQQPACCCCCCBA.",   # 6  鼻
    "AVWWPACCCCCCCBA.",
    ".AVWACCCCCCCBA..",
    "..AABCCCCCBBA...",
    "...ABBBBBBBA....",
]
S_LEGS = {0: ["...ACCA.ACCA....", "...ACCA.ACCA....", "..AKKKAAKKKA....", "................"],
          1: ["..ACCA...ABBA...", ".ACCA.....ABBA..", "AKKKA.....AKKKA.", "................"],
          2: ["....ABBAACCA....", ".....ABBACCA....", ".....AKKKKKKA...", "................"]}


def small_frames():
    fr = {}
    for f in range(3):
        g = list(S_DOWN) + ["." * 16]
        a, b = {0: (11, 11), 1: (12, 10), 2: (10, 12)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
        fr[f"down{f}"] = g
        g = list(S_UP) + ["." * 16]
        a, b = {0: (8, 8), 1: (9, 7), 2: (7, 9)}[f]
        put_leg(g, a, True); put_leg(g, b, False)
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
