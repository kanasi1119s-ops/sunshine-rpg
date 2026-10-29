# ケルト・フルート100曲「銀の笛と百の夜」010 出航 Setting Sail — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第1章の終わり。朝の港で、エイラは船に乗る。綱を引く人たちの行進（マーチ）、帆が上がって船が動きだす（ジグ）、
#   帆が風をつかんで沖へ走りだす（リール）。曲が変わるたびに調が一段上がり、船が速くなる。
# 調べ: 喜び。形: マーチ → ジグ → リール（3つの踊りの曲をつないだ「セット」。だんだん速くなる）。
# 拍子・速さ: マーチ 2/4・♩=96（4/4 の小節に2小節ずつ書く）→ ジグ 6/8・付点4分＝112（1拍＝付点4分。4拍の小節にジグ2小節）→ リール 4/4・♩=112。
# 調: マーチ D イオニア → ジグ E ミクソリディア → リール A イオニア（一段ずつ上がる）。
# 主役は笛: 装飾多め（カット・ロール）。ジグの2回目から2本目の笛が3度下で入り、リールは2本で。
# 伴奏の主役: ボーラン（枠太鼓）。脇: ナイロン弦ギターのストローク、コントラバス。竪琴・ピアノ・弦の和音・パッドは使わない。
# この曲だけ: 曲が変わるたびに調が一つ上がり、速くなる（帆が風をつかむ）。つなぎの1小節はボーランだけが次の拍子を打って導く。
# 始まり: ボーランの連打（だんだん強く）→ 終わり: 全員で1拍だけ鳴らして切る。
# 山: 階段（曲が変わるたびに一段）。
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "010-setting-sail", "出航", "Setting Sail", 96, 4, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
MAC, MBC = ["D", "D", "G", "A", "D", "D", "A", "D"], ["D", "A", "D", "A", "D", "G", "A", "D"]
JAC, JBC = ["E", "D", "E", "A", "E", "D", "A", "E"], ["E", "A", "D", "E", "A", "A", "D", "E"]   # ジグは1小節（4拍）にジグ2小節：和音はその2小節で1つ
RAC, RBC = ["A", "D", "A", "E", "A", "D", "E", "A"], ["A", "E", "D", "E", "A", "E", "E", "A"]
S.scene("帆を張る", 2, "intro", ["D", "D"])
S.scene("マーチ", 24, "verse", MAC + MBC + MAC)
S.scene("つなぎ1", 1, "break", ["E"])
S.scene("ジグ", 32, "chorus", (JAC[:4] + JAC[4:] + JBC[:4] + JBC[4:]) * 2)
S.scene("つなぎ2", 1, "break", ["A"])
S.scene("リール", 48, "chorus", RAC + RAC + RBC + RBC + RAC + RBC)
NAMES = ["帆を張る", "マーチ", "つなぎ1", "ジグ", "つなぎ2", "リール"]
J0 = 1 + 2 + 24 + 1; R0 = J0 + 32 + 1
S.tempo = [{"bar": 1, "bpm": 96}, {"bar": J0, "bpm": 112}, {"bar": R0, "bpm": 112}]
c = make(S, NAMES,
         [("帆を張る", 0, 0.66), ("マーチ", 0, 0.7), ("マーチ", 23, 0.75), ("つなぎ1", 0, 0.76), ("ジグ", 0, 0.8), ("ジグ", 31, 0.85),
          ("つなぎ2", 0, 0.86), ("リール", 0, 0.88), ("リール", 40, 0.94), ("リール", 47, 0.96)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="帆を張る", passing=True, tension=False)
B = S.beats
DR = S.track("ボーラン", "guitar", patch="frameDrum", volume=0.35, gainDb=18,   # 0.1 では全体の中でほとんど聞こえなかった（前奏 -61dB）
             pan=-0.12, reverb=0.3, modulate=False,
             barGain=[round(x * (2.2 if c.scene_of_bar[b] == "帆を張る" else 1.0), 3) for b, x in enumerate(c.g())])
DR2 = S.track("ボーラン（交互）", "guitar", patch="frameDrum", volume=0.35, gainDb=18,   # 枠太鼓の録音はとても小さい（vol 0.3 で笛より 37dB 小さかった）。gainDb の上限 +18 まで
              pan=-0.12, reverb=0.3, modulate=False, barGain=DR.spec["barGain"])
_hn = [0]
def hit(t, note, mk="", L=0.75):
    """枠太鼓の1打。短い音（1回目の 0.25〜0.33 拍）は鳴らなかったので、2つのパートに交互に置いて、1打を長めにする"""
    tr = (DR, DR2)[_hn[0] % 2]; _hn[0] += 1
    tr.at(round(t, 4), f"{note}:{L}{mk}")
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)   # ギターの最低音を E2 以上に（1回目は D2 が出て音域の外）
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.055, pan=0.3 + 0.05 * i, reverb=0.3, barGain=c.g()) for i in range(5)]
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.08, pan=0.0, reverb=0.3, barGain=c.g())
F2 = S.track("2本目の笛", "panflute", patch="flute", volume=0.26, bright=-0.8, pan=0.3, reverb=0.5, breath=False,
             noRestrike=True, mono=True, sustain=1.05, phrase=16, barGain=c.g())

# ---------- マーチ（D イオニア。4/4 の1小節＝マーチ2小節） ----------
KD, KE, KA = Key("D", "major", 4), Key("E", "mixolydian", 4), Key("A", "major", 4)
MA = ["1:1 3:0.75 2:0.25 1:1 5,:1", "1:0.5 2:0.5 3:0.5 4:0.5 5:2", "6:1 5:0.75 4:0.25 3:1 1:1", "2:1.5 3:0.5 2:2",
      "1:1 3:0.75 2:0.25 1:1 5,:1", "1:0.5 2:0.5 3:0.5 4:0.5 5:1 1':1", "7:1 6:0.75 5:0.25 4:1 2:1", "1:2 R:2"]
MB = ["5:1 1':0.75 7:0.25 1':1 3':1", "2':1 1':0.5 7:0.5 6:2", "5:1 6:0.75 7:0.25 1':1 5:1", "4:0.5 5:0.5 6:0.5 7:0.5 1':2",
      "3':1 2':0.75 1':0.25 7:1 5:1", "6:1 1':0.5 7:0.5 6:1 4:1", "5:1 3:0.75 2:0.25 1:1 7,:1", "1:2 R:2"]
play_melody(c, "マーチ", MA + MB + MA[:7] + ["1:2 5:1 7,:1"], 4, "march", key=KD, density=0.6, seed=1001)
play_melody(c, "つなぎ1", ["1:4"], 4, "air", key=KD, density=0.0)

# ---------- ジグ（E ミクソリディア。1拍＝付点4分、8分＝1/3拍） ----------
def jig(bars8):
    """8分を1とした6/8の小節（2つで4拍の小節1つ）を、1拍＝付点4分の長さに直す"""
    out = []
    for a, b in zip(bars8[0::2], bars8[1::2]):
        toks = []
        for s in (a, b):
            for t in s.split():
                n, L = t.split(":"); toks.append(f"{n}:{round(float(L) / 3, 4)}")
        out.append(" ".join(toks))
    return out
JA = ["1:2 3:1 5:2 3:1", "6:2 5:1 3:2 2:1", "1:2 3:1 5:2 1':1", "7:3 5:3",
      "1:2 3:1 5:2 3:1", "6:2 5:1 6:2 1':1", "7:2 5:1 4:2 2:1", "1:3 R:3"]
JB = ["5:2 1':1 2':2 1':1", "3':2 2':1 1':2 7:1", "6:2 1':1 2':2 1':1", "7:3 5:3",
      "5:2 1':1 2':2 3':1", "4':2 3':1 2':2 1':1", "7:2 5:1 4:2 2:1", "1:3 R:3"]
jl = jig(JA) + jig(JA) + jig(JB) + jig(JB)
n1 = play_melody(c, "ジグ", jl + jl, 4, "march", key=KE, density=0.8, seed=1002)
j2 = c.s0["ジグ"] * B + 16 * B                 # 2回目から2本目の笛（3度下）
for st, L, m, mk in n1:
    if st >= j2 and L >= 0.3:
        h = m - 3 if (m - 3 - KE.t) % 12 in [x % 12 for x in KE.steps] else m - 4
        F2.at(round(st + 0.015, 4), f"{nm(h)}:{round(L, 4)}")
play_melody(c, "つなぎ2", ["5:4"], 4, "air", key=KE, density=0.0)

# ---------- リール（A イオニア） ----------
RA = ["1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 2:0.5",
      "1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 1:0.5", "2:0.5 7,:0.5 5,:0.5 7,:0.5 2:1 1:0.5 7,:0.5",
      "1:0.5 3:0.5 5:0.5 3:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "6:0.5 1':0.5 6:0.5 4:0.5 5:0.5 3:0.5 2:0.5 1:0.5",
      "2:0.5 4:0.5 6:0.5 4:0.5 5:0.5 3:0.5 2:0.5 7,:0.5", "1:1 3:0.5 2:0.5 1:2"]
RB = ["1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5", "7:0.5 5:0.5 3:0.5 5:0.5 7:1 6:0.5 5:0.5",
      "6:0.5 4:0.5 2:0.5 4:0.5 6:0.5 1':0.5 2':0.5 1':0.5", "7:0.5 6:0.5 5:0.5 3:0.5 2:1 5:1",
      "1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5", "7:0.5 5:0.5 3:0.5 5:0.5 6:0.5 4:0.5 2:0.5 4:0.5",
      "5:0.5 3:0.5 1:0.5 3:0.5 2:0.5 4:0.5 7,:0.5 2:0.5", "1:1 3:0.5 2:0.5 1:2"]
RB_END = RB[:7] + ["1':1 R:3"]                  # 最後：全員で1拍だけ鳴らして切る
nr = play_melody(c, "リール", RA + RA + RB + RB + RA + RB_END, 4, "reel", key=KA, density=0.9, seed=1003)
for st, L, m, mk in nr:                          # リールは2本で（3度下。速い装飾音は重ねない）
    if L >= 0.4:
        h = m - 3 if (m - 3 - KA.t) % 12 in [x % 12 for x in KA.steps] else m - 4
        F2.at(round(st + 0.015, 4), f"{nm(h)}:{round(L, 4)}")

# ---------- 伴奏 ----------
def rt(ch, lo=40):
    r = PC[re.match(r"^([A-G][#b]?)", ch).group(1)]
    return lo + (r - lo) % 12
T3 = 1 / 3
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = rt(ch)
    if n == "帆を張る":       # ボーランの連打。16分で、だんだん強く
        for q in range(16 if i == 0 else 12):
            hit(b * B + q * 0.25, 'D3' if q % 4 == 0 else 'A3', ',' if (i == 0 and q < 8) else '')
        if i == 1: hit(b * B + 3, "D3", "!", 1)
        continue
    if n in ("つなぎ1", "つなぎ2"):   # つなぎ：ボーランだけが次の拍子を打つ（ジグは3つずつ、リールは2つずつ）
        if n == "つなぎ1":
            for q in range(12): hit(b * B + q * T3, 'D3' if q % 3 == 0 else 'A3', '!' if q % 3 == 0 else ',')
        else:
            for q in range(8): DR.at(b * B + q * 0.5, f"{'D3' if q % 2 == 0 else 'A3'}:0.5{'!' if q % 4 == 0 else ','}")
        CB.at(b * B, f"{nm(r)}:4,")
        continue
    if n == "マーチ":
        DR.bar(b, "D3:1! A3:1, D3:1 A3:0.5, A3:0.5,")
        strum(GT, b, B, ch, [(0, 1, "d", "!"), (1, 1, "d", ","), (2, 1, "d", ""), (3, 1, "d", ",")])
        CB.bar(b, f"{nm(r)}:1 R:1 {nm(r + 7 - (12 if r + 7 > 50 else 0))}:1 R:1")
    elif n == "ジグ":         # 1拍＝付点4分。ジグの1小節：下・上・上・下・上・上
        for half in (0, 2):
            for q, (nn, mk) in enumerate([("D3", "!"), ("A3", ","), ("A3", ","), ("D3", ""), ("A3", ","), ("A3", ",")]):
                hit(b * B + half + q * T3, nn, mk)
            strum(GT, b, B, ch, [(half, 1, "d", "!"), (half + 1, 2 * T3, "d", ""), (half + 1 + 2 * T3, T3, "u", ",")])
            CB.at(b * B + half, f"{nm(r)}:1"); CB.at(b * B + half + 1, f"{nm(r + 7 - (12 if r + 7 > 50 else 0))}:1,")
    elif n == "リール":
        if i == 47:            # 最後：全員で1拍だけ
            DR.at(b * B, "D3:1!"); strum(GT, b, B, ch, [(0, 1, "d", "!")]); CB.at(b * B, f"{nm(r)}:1!")
            continue
        bodhran(DR, b, B, "reel", var=1 if i % 8 == 7 else 0)
        strum(GT, b, B, ch, [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")])
        CB.bar(b, f"{nm(r)}:1 {nm(r + 7 - (12 if r + 7 > 50 else 0))}:1, {nm(r)}:1 {nm(r + 7 - (12 if r + 7 > 50 else 0))}:1,")

# 枠太鼓の音：D3（手のひら）はとても小さく、A3 は鳴らない（2026-10-30 に試しの書き出しで測った）。低い打ち＝C3、高い打ち＝E3 に
for _tr in (DR, DR2):
    _tr.ev = [(st, L, x.replace("D3:", "C3:", 1) if x.startswith("D3:") else x.replace("A3:", "E3:", 1) if x.startswith("A3:") else x) for st, L, x in _tr.ev]
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の010（第3版）。第1章の終わり、朝の港から船出する。マーチ（D）→ ジグ（E ミクソリディア）→ リール（A）の3つの踊りの曲をつないだセットで、曲が変わるたびに調が一段上がり、速くなる（帆が風をつかむ）。伴奏の主役はボーラン、脇にギターのストロークとコントラバス。ジグの2回目から2本目の笛。ボーランの連打で始まり、最後は全員で1拍だけ鳴らして切る。",
       harm_scenes=None, tail_scene="リール", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "1046", "db": -44, "hp": 110, "lp": 5000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.16, "lp": 3000, "rt": 2.0}}}
json.dump(air, open("/tmp/cel/w/air010.json", "w"), ensure_ascii=False)
# 1/3 拍の位置を丸めると「R:0」ができて書き出しが止まる（1回目）。長さ0の休みを取りのぞく
_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
