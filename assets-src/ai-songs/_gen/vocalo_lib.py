# vocalo_lib.py — 今のボカロ曲らしさを作る部品（2026-11-15。人間「ボカロ曲の作り方徹底的に学んで、必要な要素を作曲ソフトに入れようか」）
# 調べた内容は docs/sound/vocaloid-study.md。ここには、曲の台本（vt3_NN_*.py）から呼ぶ部品を置く。
#   ① 16分のマスで書くリズム（steps / mel16）: 16分の早口・「16分＋16分休符＋4分」の決め・シンコペーションを、型のくり返しなしで1小節ずつ書ける
#   ② 丸サ進行（Just the Two of Us 進行）と、サビでの転調（marusa / up）
#   ③ リリースカットピアノ（relcut）: 和音を短く切って、すき間を空けて刻む
#   ④ 切り貼り（stutter）: 同じ音を細かくくり返す。歌のチョップ用の文字列も作れる
#   ⑤ 16ビートの4つ打ち・半分の速さ・キメ（全員で同じリズム）のドラムの型
from vt25_lib import *


def steps(pat, pitches, step=0.25, short=None):
    """16分のマスで書いたリズムを、音の並びにする。pat: 'x'＝音の頭、'-'＝のばす、'.'＝休み（1文字＝16分）。
    pitches: 音名のリスト（足りなければ最後の音をくり返す）。short: 音の長さの上限（リリースカット＝0.25 など。残りは休みになる）"""
    out, i, k = [], 0, 0
    pat = pat.replace(" ", "")
    while i < len(pat):
        c = pat[i]; j = i + 1
        if c == "x":
            while j < len(pat) and pat[j] == "-": j += 1
            L = (j - i) * step; p = pitches[min(k, len(pitches) - 1)]; k += 1
            if short and L > short: out.append(f"{p}:{short:g}"); out.append(f"R:{L - short:g}")
            else: out.append(f"{p}:{L:g}")
        else:
            while j < len(pat) and pat[j] == ".": j += 1
            out.append(f"R:{(j - i) * step:g}")
        i = j
    return " ".join(out)


def onsets(pat): return pat.count("x")


def mel16(pat, degs):
    """歌の1小節を16分のマスで書く。degs: 音階の度数（"5" "1'" "#7" など）を音の頭の数だけ。返すのは Key.mel に渡す文字列"""
    assert onsets(pat) == len(degs), (pat, degs)
    return steps(pat, [str(d) for d in degs])


MARUSA_C = ["Fmaj7", "E7", "Am7", "C7"]          # 丸サ進行（ハ長調／イ短調での形: IV△7 → III7 → VIm7 → I7）


def marusa(semi=0, last=None):
    """丸サ進行を semi 半音だけ移す。last: 4小節目を別の和音にする（例: 次の調の V7）"""
    ch = [tr_chord(c, semi) for c in MARUSA_C]
    if last: ch[3] = last
    return ch


def relcut(tracks, chord, pat, center=64, short=0.25):
    """リリースカットピアノ: 和音（3声）を pat のリズムで短く切って鳴らす。返すのは各声の文字列のリスト"""
    v = sorted(voice(chord.split("|")[0].split("/")[0], center, len(tracks)))
    return [steps(pat, [nm(m)], short=short) for m in v]


def stutter_chop(note, kana, n=4, step=0.25, tail=None):
    """歌の切り貼り: 同じ音・同じ文字を n 回、細かくくり返す（例: ぴ・ぴ・ぴ・ぴ）。chops() に渡す文字列。tail: 最後につける (音, 長さ, 文字)"""
    s = " ".join(f"{note}:{step:g}:{kana}" for _ in range(n))
    if tail: s += f" {tail[0]}:{tail[1]:g}:{tail[2]}"
    return s


# ドラムの型（16マス）: (キック, スネア, ハイハット)
BEAT16 = ("X...X...X...X...", "....X.......X...", "x.xxx.xxx.xxx.xx")        # 16ビートの4つ打ち（ハイハットは閉じた16分。裏のオープンは使わない）
BEAT16B = ("X...X...X...X.x.", "....X.......X..x", "xxx.xxx.xxx.xxx.")
HALF = ("X.........x.....", "........X.......", "x.x.x.x.x.x.x.x.")           # 半分の速さ
KIME8 = ("X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "................")           # キメ: 8分で全員いっしょ
KIME_END = ("X..X..X.X.X.....", "X..X..X.X.X.....", "................")        # キメ: 3・3・2 で止まる
