# ケルト・フルート100曲「銀の笛と百の夜」019 夕べの笛吹き The Evening Pipers — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夕方、エイラが丘のふもとで笛を吹くと、谷の向こうの丘から、知らない笛吹きが同じ節を吹き返してくる。
#   二人は顔も見えないまま、句を受け渡して、日が沈むまで吹き続ける。最後に遠い方の笛だけが、暗くなった谷に残る。
# 調べ: 喜び。形: ブルターニュの「受け渡し」（二人の歌い手が、相手の句をくり返して受け継ぐ。句のしっぽは二人で重ねて、途切れさせない）。
# 拍子・速さ: 4/4・♩=108。旋法: A ドリア。
# 主役は笛（近い笛＝エイラ。中音域）。脇: 遠い丘の笛（2本目の笛。少し小さく、響きが多く、右に）。
# 伴奏の主役: ボーラン（ケリー式。低く柔らかく、C3 が中心）。竪琴・ギター・ピアノ・弦・パッドは使わない。
# この曲だけ: 二人の笛吹きが、句のしっぽ（最後の1小節）を重ねて、途切れずに受け渡す。
# 始まり: 近い笛ひとり → 終わり: しっぽが重なったまま、遠い笛だけが残る。
# 山: 波（受け渡し2で一度、受け渡し3でもう一度。丘のこだまで一度静かになる）。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "019-the-evening-pipers", "夕べの笛吹き", "The Evening Pipers", 108, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("A", "dorian", 4)
CH = ["Am", "G", "Am", "Em"]
SC = [("近い笛", 8, "intro"), ("受け渡し1", 32, "verse"), ("受け渡し2", 32, "chorus"), ("丘のこだま", 16, "verse"),
      ("受け渡し3", 24, "chorus"), ("しっぽ", 8, "outro")]
for n, L, kd in SC: S.scene(n, L, kd, (CH * 8)[:L])
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("近い笛", 0, 0.66), ("受け渡し1", 0, 0.7), ("受け渡し1", 31, 0.76), ("受け渡し2", 0, 0.8), ("受け渡し2", 20, 0.88),
          ("受け渡し2", 31, 0.8), ("丘のこだま", 0, 0.68), ("受け渡し3", 0, 0.78), ("受け渡し3", 20, 0.9), ("しっぽ", 0, 0.78), ("しっぽ", 7, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="近い笛", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 遠い笛（volume 0.2）は近い笛とほぼ同じ大きさ → 0.15（遠く）。ボーランは笛より約 8〜10dB 小さい（柔らかい打ちとして丁度よい）
FAR = S.track("遠い丘の笛", "panflute", patch="flute", volume=0.15, bright=-0.6, pan=0.45, reverb=0.75, breath=False, barGain=G)
DR = [S.track(f"ボーラン{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.12 + 0.08 * j, reverb=0.3, barGain=G)
      for j in range(2)]

# ---------- 句（A ドリア。1=A4。4小節） ----------
P = [["1:1 3:0.5 4:0.5 5:1 4:1", "3:1 1:1 2:1 7,:1", "1:0.5 2:0.5 3:1 4:1 6:1", "5:2 3:2"],
     ["5:1 6:0.5 5:0.5 4:1 3:1", "4:1 2:1 3:1 1:1", "2:0.5 3:0.5 4:1 5:1 3:1", "1:2 7,:2"],
     ["3:1 5:1 1':1 7:0.5 6:0.5", "5:1 6:1 4:2", "3:1 4:0.5 3:0.5 2:1 7,:1", "1:4"],
     ["6:1 5:1 4:1 3:1", "4:0.5 5:0.5 6:1 5:2", "4:1 3:0.5 2:0.5 1:1 2:1", "3:2 1:2"]]

def sing(track, bars, b0, oct_=4, dens=0.25, seed=1):
    ev = []
    for j, s_ in enumerate(bars):
        ev += mel_events(K, s_, oct_, (b0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(track, ornament(ev, K, 108, "march", B, density=dens, seed=seed))

# 近い笛ひとり（8小節）
s0 = c.s0["近い笛"]
sing(c.FLUTE, P[0], s0, dens=0.2, seed=1900); sing(c.FLUTE, P[1], s0 + 4, dens=0.2, seed=1901)

def exchange(scene, plen, order, dens, seed):
    """受け渡し：歌い手が交代で、相手の句をくり返して受け継ぐ。次の歌い手は、前の句の最後の小節から重ねて入る"""
    s0 = c.s0[scene]; L = c.sc_len[scene]
    turn = 0
    while turn * plen < L:
        who = (c.FLUTE, FAR)[turn % 2]; other = (FAR, c.FLUTE)[turn % 2]
        ph = order[(turn // 2) % len(order)]
        if plen == 2: ph = ph[:2] if (turn // 2) % 2 == 0 else ph[2:]
        b0 = s0 + turn * plen
        if b0 + plen > s0 + L: break
        sing(who, ph, b0, dens=dens, seed=seed + turn)
        if b0 + plen < s0 + L or scene != "受け渡し3":                       # しっぽ：次の人が最後の1小節を重ねて吹く
            sing(other, ph[-1:], b0 + plen - 1, dens=dens * 0.5, seed=seed + 50 + turn)
        turn += 1
# 受け渡し1：4小節ずつ。エイラが吹いた句を、遠い笛がくり返す（遠い笛から始める＝近い笛ひとりの句を受け継ぐ）
s0 = c.s0["受け渡し1"]
sing(FAR, P[1][-1:], s0 - 1, dens=0.1, seed=1909)              # 近い笛ひとりの最後の小節に、遠い笛が重なって入ってくる
exchange("受け渡し1", 4, [P[1], P[2], P[3], P[0]], 0.25, 1910)
# 受け渡し2：2小節ずつ（受け渡しが速くなる）
exchange("受け渡し2", 2, [P[2], P[3], P[0], P[1]], 0.35, 1950)
# 丘のこだま：遠い笛がひとりで長く吹き、近い笛は低い長い音で支える
s0 = c.s0["丘のこだま"]
sing(FAR, P[3], s0, dens=0.3, seed=1990); sing(FAR, P[2], s0 + 4, dens=0.3, seed=1991)
sing(FAR, P[0], s0 + 8, dens=0.3, seed=1992); sing(FAR, P[1], s0 + 12, dens=0.3, seed=1993)
for j, s_ in enumerate(["1:4", "7,:4", "1:4", "5,:4", "3:4", "2:4", "1:4", "7,:4", "6,:4", "7,:4", "1:4", "3:4", "4:4", "3:4", "2:4", "1:4"]):
    sing(c.FLUTE, [s_.replace("5,", "5")], s0 + j, dens=0.0, seed=2000 + j)
# 受け渡し3：また4小節ずつ。最後の2周は二人がいっしょに（山）
exchange("受け渡し3", 4, [P[0], P[2], P[1], P[3]], 0.35, 2010)
s0 = c.s0["受け渡し3"]
for q in (4, 5):                                                   # 最後の2周（同じ句 P[1] のくり返し）は、もう一人が3度下でいっしょに
    ev = []
    for j, s_ in enumerate(P[1]):
        ev += mel_events(K, s_, 4, (s0 + 4 * q + j) * B)
    play((FAR, c.FLUTE)[q % 2], [(round(t, 4), L, _dia(K, m, -2), ",") for t, L, m in ev])
# しっぽ：近い笛と遠い笛が重なったまま、近い笛が先に止まり、遠い笛だけが残る
s0 = c.s0["しっぽ"]
sing(c.FLUTE, ["5:2 3:2", "1:4"], s0, dens=0.1, seed=2040)
sing(FAR, ["5:2 3:2", "1:4", "R:1 3:1 2:1 7,:1", "1:4", "1:4", "R:4", "R:4", "R:4"], s0, dens=0.1, seed=2041)

# ---------- ボーラン（ケリー式。低く柔らかく。2つのパートに交互に） ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); tr = DR[b % 2]
    if n == "近い笛" or (n == "受け渡し1" and i < 8): continue
    if n == "受け渡し1":
        tr.bar(b, "C3:1! R:0.5 C3:0.5, C3:1 E3:0.5, C3:0.5,")
    elif n in ("受け渡し2", "受け渡し3"):
        bodhran(tr, b, B, "reel", var=(i % 4 == 3), soft=True)
    elif n == "丘のこだま":
        if i % 2 == 0: tr.bar(b, "C3:2, R:2")
    elif n == "しっぽ" and i < 2:
        tr.bar(b, "C3:1, R:3")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の019（第3版）。夕方、谷の向こうの丘から、知らない笛吹きが同じ節を吹き返してくる。ブルターニュの受け渡し（4/4・♩=108、A ドリア）。近い笛（エイラ）と遠い丘の笛が、相手の句をくり返して受け継ぎ、句のしっぽの1小節は二人で重ねて途切れさせない。伴奏は低く柔らかいボーラン。最後は遠い笛だけが暗くなった谷に残る。",
       harm_scenes=None, tail_scene="しっぽ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air019.json", "w"), ensure_ascii=False)
