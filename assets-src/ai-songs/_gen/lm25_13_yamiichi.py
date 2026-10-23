# ラウド26曲 13「No Receipts」（仮。もとの仮題「闇市の値札」）。2026-10-24 素材から作り直し
# スタイル: ファンクメタル／ラップメタル（16分の跳ねるうねり・スラップのような切れ）＋バリトンサックス。B♭ 短調のブルース・100・4/4
# 物語: 闇市の値切り。売り手（バリトンサックス）と買い手（リードギター）が言い合う。言い返す間がどんどん短くなり、
#       とうとう同時にどなり合い、にらみ合いの無音。手を打って商談成立（全員の決め）。サックスが去っていく。
# 形: かけ合い（2小節ずつ → 1小節ずつ → 2拍ずつ → 同時）。交代がだんだん短くなる。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   屋台（1）: サックスのうなりだけ
#   売り込み（2）: うねるリフの上で、2小節ずつ言い合う
#   言い返し（2）: 1小節ずつ
#   熱くなる（3）: 2拍ずつ
#   どなり合い（3）: 同時に
#   にらみ合い（0）: 無音
#   商談成立（3）: 全員の決めの一撃
#   去る（1）: サックスのブルース、ドラムはライドだけ
# 旋律の性格: 会話（短い問いと答え）。16分の食い、ブルーノート（E）。語尾を上げる・下げるで問いと答えを分ける
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 100, 4
bar = Bars(BEATS)
R4 = bar.rest()

BL = ["Bbm7", "Bbm7", "Eb7", "Eb7", "Bbm7", "Bbm7", "Gb7", "F7"]
FORM = [("stall", 8), ("pitch", 28), ("counter", 28), ("heat", 16), ("shout", 8), ("stare", 2), ("deal", 4), ("leave", 8)]
CH = {"stall": BL, "pitch": (BL * 4)[:28], "counter": (BL * 4)[:28], "heat": BL * 2, "shout": BL, "stare": ["Bbm7", "Bbm7"],
      "deal": ["Bbm7", "Bbm7", "F7", "Bbm7"], "leave": BL}
song = Song("闇市の値札（仮）",
            "仮: ラウド26曲の13曲目（2026-10-24 素材から作り直し）。ファンクメタル＋バリトンサックス。B♭ 短調のブルース・100。売り手（サックス）と買い手（リード）の値切り。"
            "言い返す間が2小節 → 1小節 → 2拍 → 同時と短くなり、にらみ合いの無音、商談成立の決め。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 闇市の値切り。言い合いの間がどんどん短くなり、どなり合い、にらみ合い、手を打って商談成立、サックスが去っていく。"
song.kinds = {"stall": "intro", "pitch": "verse", "counter": "pre", "heat": "chorus", "shout": "chorus", "stare": "break", "deal": "break", "leave": "outro"}
SECS, NB = song.secs, song.nb
BLUES = scale_pcs("A#", "blues")

# 会話のリズム（問い＝語尾が上がる・答え＝語尾が下がる、は音の歩き方で）
TALK = [[-0.25, 0.25, 0.25, 0.25, 0.5, -0.5, 0.25, 0.25, 0.5, -1], [0.25, 0.25, 0.5, -0.25, 0.25, 0.25, 0.25, 0.5, -1.5],
        [-0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, -1.5], [0.5, -0.25, 0.25, 0.25, 0.25, -0.5, 0.75, 0.25, -1],
        [-1, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, -1], [0.25, 0.5, 0.25, -0.5, 0.25, 0.25, 0.5, 0.5, -1]]
Q = (1, 1, -1, 2, 1)       # 問い: 上がっていく
A = (-1, -1, 1, -2, -1)    # 答え: 下がっていく


def talk(nb, seed, start, end, chords, contour, lo, hi):
    return [bar(x) for x in melody_walk(BLUES, start, end, TALK, seed, chords, contour=contour, lo=lo, hi=hi, long_snap=0.75)]


def half(b_, first):
    """1小節の前半（first=True）か後半だけを残す"""
    out, t = [], 0.0
    for x in b_.split():
        d = tok_beats(x); keep = (t < 2 - 1e-9) if first else (t >= 2 - 1e-9)
        out.append(x if keep else f"R:{d:g}"); t += d
    return bar(" ".join(out))


SAX_LO, SAX_HI, GT_LO, GT_HI = "A#2", "A#3", "A#3", "C#5"
P = {k: [] for k in ["riff", "rhy", "lead", "sax", "bass", "mute"]}
kit = Kit(BEATS)
seq = {}
for name, n in FORM:
    seq[name] = (talk(n, len(name), "F3", "A#2", CH[name], A, SAX_LO, SAX_HI), talk(n, len(name) + 3, "C#4", "F4", CH[name], Q, GT_LO, GT_HI))
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = sax = mute = R4
    s_, g_ = seq[name][0][i], seq[name][1][i]
    r = {"Bbm7": "A#1", "Eb7": "D#2", "Gb7": "F#1", "F7": "F2"}[ch]
    groove = bar(f"{r}:0.25! R:0.25 {r}:0.25 {up(r, 1)}:0.25 R:0.5 {tr(r, 3)}:0.25 {tr(r, 5)}:0.25 {tr(r, 6)}:0.25 {tr(r, 7)}:0.25! R:0.5 {r}:0.25 {tr(r, -2)}:0.25 R:0.5")
    if name == "stall":
        sax = s_ if i % 2 == 0 else R4
        b = R4 if i < 4 else bar(f"{root_note(ch)}:0.5! R:3.5")
    elif name == "pitch":
        riff = groove if i >= 4 else bar(f"{r}:0.25! R:3.75")
        rhy = groove if i >= 8 else R4
        if (i // 2) % 2 == 0: sax = s_
        else: lead = g_
        b = unison_low(groove, -1, "B0")
        mute = bar("R:0.75 A#1:0.25, R:1.75 A#1:0.25,, R:1") if i % 2 else R4
    elif name == "counter":
        riff = rhy = groove
        if i % 2 == 0: sax = s_
        else: lead = g_
        b = unison_low(groove, -1, "B0")
        mute = bar("R:0.75 A#1:0.25, R:0.75 A#1:0.25, R:2") if i % 2 == 0 else R4
    elif name == "heat":
        riff = rhy = groove
        sax = half(s_, True); lead = half(g_, False)
        b = unison_low(groove, -1, "B0")
    elif name == "shout":
        riff = rhy = bar(" ".join(f"{r}:0.25{'!' if j % 4 == 0 else ''}" for j in range(16)))
        sax = s_; lead = g_
        b = unison_low(riff, -1, "B0")
    elif name == "stare":
        b = R4                                                  # にらみ合い: 無音
    elif name == "deal":
        riff = rhy = bar(f"{r}:0.5! R:0.25 {r}:0.25! R:0.5 {r}:0.5! R:2") if i < 3 else bar(f"{r}:1! R:3")
        sax = strip_marks(riff).replace("A#1", "A#2").replace("F2", "F3") if i < 3 else bar("A#2:1! R:3")
        lead = shift_oct(strip_marks(riff), 2) if i < 3 else bar("A#3:1! R:3")
        b = unison_low(riff, -1, "B0")
    else:   # leave
        sax = s_
        b = bass_walk(ch, song.chord_at(min(idx + 1, NB - 1)), BEATS) if i < 6 else R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["sax"].append(sax); P["bass"].append(b); P["mute"].append(mute)
    kit.add("X..x..X...X.....", "....X.......X..o", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("バリトンサックス", "brass", J("sax"), patch="bariSax", volume=0.14, pan=0.15, reverb=0.25, phrase=8, attack=0.02, release=0.3,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 900, "high": 1}, {"type": "plate", "mix": 0.14}]))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "bright-nu-wall"

from lm25_plans import apply_plan
apply_plan(song, "13")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-13-yamiichi.json"
    song.write(out)
    check_clash(song)
