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


# ===================== 2026-11-15 追加（人間「今の作り方に足りていないもの全て足して。音の作り方も学んでプロ仕様に」）=====================
# 調べた音作り（docs/sound/vocaloid-study.md の「プロの音作り」）:
#   ・スーパーソウの和音は、7th・9th を入れて、根音を低く、上の音を高く広げる。150〜200Hz より下を切る。2〜3kHz のきつさを少し抑える。キックで凹ませる
#   ・サブベースは真ん中（モノラル）で根音だけ。和音の音はサブに入れない（低音がにごる）
#   ・広がりは高い音ほど広く。低い音は真ん中
#   ・すき間を空ける（全部を埋めない）。うねりは、和音を変えるのでなく、音量とフィルターの動きで作る

def wide9(ch, lo=53, n=5):
    """フューチャーベースの和音の積み方: 根音を低く、5度、その上に 3度・7度・9度を広げて置く（n 声。返すのは MIDI 番号）"""
    name = ch.split("|")[0].split("/")[0]
    r = low(name, "C1")
    while r < lo: r += 12
    pcs = sorted({(m - r) % 12 for m in tones(name, nm(r), nm(r + 12))})
    third = next((x for x in pcs if x in (3, 4)), 4); sev = next((x for x in pcs if x in (10, 11)), 10)
    v = [r, r + 7, r + 12 + third, r + 12 + sev, r + 26]
    return v[:n]


def arp16(ch, pat, order, lo="A4", hi="A6", short=None):
    """16分のアルペジオ: 和音の音を order の順（番号）に、pat のリズムで鳴らす"""
    tn = tones(ch.split("|")[0].split("/")[0], lo, hi)
    return steps(pat, [nm(tn[q % len(tn)]) for q in order], short=short)


def glitch(pitch, beats=4, shape=(4, 8, 16)):
    """グリッチ（くり返しがだんだん細かくなる）: 16分 → 32分 → 64分。shape: それぞれの個数。残りは休み"""
    out, t = [], 0.0
    for n, L in zip(shape, (0.25, 0.125, 0.0625)):
        for _ in range(n):
            if t + L <= beats + 1e-9: out.append(f"{pitch}:{L:g}"); t += L
    if beats - t > 1e-6: out.append(f"R:{beats - t:g}")
    return " ".join(out)


def tape_stop(pitch, beats=2, down=12):
    """テープストップ（回転が止まるように音が落ちる）: 同じ長さの中で down 半音下へすべる"""
    return f"{pitch}:{beats:g}>{nm(midi(pitch) - down)}"


# かわいい効果音（kawaiiFx の鍵盤）: 場面の変わり目に置く「上がる音・下がる音・インパクト」
KFX = {"awa": "C4", "drop": "C#4", "kira": "D4", "kira2": "D#4", "kyu": "E4", "pyon": "F4", "up": "F#4", "down": "G4", "rev": "G#4",
       "clap": "B4", "snap": "C5", "impact": "G5", "sub": "G#5", "laser": "A5", "glitch": "D#6"}


def fx_bar(*hits, beats=4):
    """効果音の1小節。hits: (拍の位置, 名前, 長さ) を並べる。例 fx_bar((0, "impact", 1), (2, "kira", 0.5))"""
    out, t = [], 0.0
    for at, name, L in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{KFX[name]}:{L:g}"); t = at + L
    if beats - t > 1e-6: out.append(f"R:{beats - t:g}")
    return " ".join(out)


# 音作りのまとまり（エフェクターの並び）。曲ごとに選んで使う（全曲に同じものを入れる決まりではない）
def rack_supersaw(hp=180, lp=7000, pump_ms=None, wide=0.35):
    """スーパーソウの和音: 低い所を切る → 150Hz 付近と 2.5kHz を少し抑える → 上を丸める →（うねるフィルター）→ 広げる → プレートの残響"""
    r = [{"type": "filter", "kind": "highpass", "freq": hp, "q": 0.7}, {"type": "eq", "low": -2, "mid": -2, "midHz": 2600, "high": 1.5},
         {"type": "filter", "kind": "lowpass", "freq": lp, "q": 0.6}]
    if pump_ms: r.append({"type": "syncfilter", "ms": pump_ms, "freq": 3200, "depth": 0.55, "q": 0.9, "mix": 0.6})
    return r + [{"type": "widen", "mix": wide}, {"type": "plate", "mix": 0.14}]


def rack_bass():
    """FM のベース: 低い所は真ん中のまま、コンプでつぶをそろえ、700Hz 付近を少し出して小さいスピーカーでも聞こえるように"""
    return [{"type": "compressor", "threshold": -20, "ratio": 4, "attack": 0.008, "release": 0.12}, {"type": "eq", "low": 1, "mid": 2, "midHz": 750, "high": -1}]


def rack_pluck(beats=0.75):
    """プラック: 低い所を切って、ピンポンディレイで左右にこだまを返す"""
    return [{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "pingpong", "beats": beats, "mix": 0.2, "feedback": 0.32}, {"type": "plate", "mix": 0.1}]


def rack_piano():
    """リリースカットピアノ: 低い所を切り、コンプで頭をそろえ、明るさを少し足す（切れ味）"""
    return [{"type": "filter", "kind": "highpass", "freq": 160, "q": 0.7}, {"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.004, "release": 0.09},
            {"type": "eq", "low": -2, "mid": 1, "midHz": 1800, "high": 2.5}]


def rack_lead():
    """電子のリード: ダブラーで太くして、付点8分のディレイ"""
    return [{"type": "doubler", "ms": 14, "depth": 0.4, "mix": 0.3}, {"type": "delay", "beats": 0.75, "mix": 0.16, "feedback": 0.28}, {"type": "plate", "mix": 0.12}]


def kero(js, idx):
    """ケロケロ声（音程を階段のように動かす調声）: 音の移りを一気に・しゃくりなし・ビブラートなし・自動の歌い回しなし。js["vocals"][idx] に効く"""
    js["vocals"][idx].update(glide=0.12, auto=0, scoop=0, slashScoop=0, vibratoMap=[], vibrato=0)
