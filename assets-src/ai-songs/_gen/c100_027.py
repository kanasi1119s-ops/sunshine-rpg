# ケルト・フルート100曲「銀の笛と百の夜」027 鴨の親子 The Duck and Her Ducklings — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 泉からの帰り道、川べりを鴨の親子が一列になって歩いている。親鴨がぴょこぴょこ進むと、すぐうしろの子鴨が
#   1拍おくれて同じ足どりをまねる。池に着くと親子で泳ぎ、また岸に上がって巣へ帰る。最後に子鴨が1羽、ぴよ、と鳴く。
# 調べ: 喜び。形: シングル・ジグ（6/8 の「タ〜タ」でぴょんぴょん跳ねる）。A・B 8小節ずつ。
# 拍子・速さ: 6/8・付点4分＝118。1拍＝付点4分、1小節＝2拍で書き、8分は 1/3 拍（011・014 と同じ）。旋法: F イオニア。
# 主役は笛（親鴨）。脇: ティン・ホイッスル（子鴨。1オクターブ上で、親の句の頭を1拍おくれてまねる）。
# 伴奏の主役: ファゴットの低い「よちよち」（短い音）と、チェロのピチカート。打楽器・竪琴・ギター・ピアノ・パッドは使わない。
# この曲だけ: 子鴨（ホイッスル）が1拍おくれて親のまねをする。池の場面では、まねがおくれて追いつけない。
# 始まり: ピチカートの足どり → 終わり: 子鴨のホイッスルの1音。
# 山: 中盤に1つ（3回目。子鴨のまねがいちばん多い）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 118
S = Song("C100", "027-the-duck-and-her-ducklings", "鴨の親子", "The Duck and Her Ducklings", BPM, 2, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("F", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["F", "Bb", "C", "C", "F", "C", "C", "F"]
CB = ["F", "Bb", "Bb", "F", "Bb", "F", "C", "F"]
AB = CA + CA + CB + CB
SC = [("足どり", 4, "intro", ["F", "C", "F", "C"]), ("1回目", 32, "verse", AB), ("2回目", 32, "verse", AB), ("3回目", 32, "chorus", AB),
      ("池", 24, "verse", (CB + CA + CB)), ("4回目", 32, "verse", AB), ("5回目", 32, "verse", AB), ("6回目", 32, "verse", AB),
      ("帰り", 24, "verse", CA + CB + CA), ("ぴよ", 2, "outro", ["F", "F"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("足どり", 0, 0.64), ("1回目", 0, 0.7), ("2回目", 0, 0.76), ("3回目", 0, 0.84), ("3回目", 31, 0.9), ("池", 0, 0.68),
          ("4回目", 0, 0.78), ("5回目", 0, 0.8), ("6回目", 0, 0.78), ("帰り", 0, 0.7), ("ぴよ", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足どり", passing=True, tension=False)
B = S.beats
G = c.g()
# 試し書き出し: ホイッスル（0.03）でも笛より 5〜8dB 大きい → 0.015。ファゴットは笛より約8dB 小さい → 0.1→0.13。ピチカートは笛と同じくらい
WH = S.track("ティン・ホイッスル（子鴨）", "panflute", patch="tinWhistle", volume=0.015, pan=0.35, reverb=0.4, barGain=G)    # ホイッスルは笛より約10dB 大きい（011）
BS = S.track("ファゴット（よちよち）", "strings", patch="bassoon", volume=0.13, pan=-0.2, reverb=0.35, barGain=G)
VP = S.track("チェロ（ピチカートの足どり）", "strings", patch="pizzicato", volume=0.12, gainDb=6, pan=0.1, reverb=0.35, barGain=G)

# ---------- シングル・ジグ（F イオニア。1=F4。8分＝1、1小節＝6） ----------
A = ["1:2 3:1 5:2 3:1", "4:2 6:1 5:2 3:1", "2:2 4:1 3:2 1:1", "7,:2 2:1 5,:3",
     "1:2 3:1 5:2 1':1", "7:2 5:1 6:2 4:1", "3:2 2:1 4:2 7,:1", "1:3 R:3"]
Bm = ["5:2 6:1 5:2 3:1", "1':2 7:1 6:3", "4:2 5:1 4:2 2:1", "5:2 6:1 5:3",
      "6:2 7:1 1':2 6:1", "5:2 3:1 1:2 3:1", "2:2 3:1 4:2 7,:1", "1:3 R:3"]
POND = ["1:6", "3:3 2:3", "1:3 5,:3", "6,:6", "7,:3 1:3", "2:6", "3:3 4:3", "5:6"] * 3          # 池：ゆったり泳ぐ（長い音）
COPY = {"1回目": 0.4, "2回目": 0.6, "3回目": 1.0, "4回目": 0.5, "5回目": 0.6, "6回目": 0.7, "帰り": 0.3}
for n in ("1回目", "2回目", "3回目", "4回目", "5回目", "6回目"):
    dens = {"3回目": 0.45}.get(n, 0.3)
    notes = play_melody(c, n, e2b(A + A + Bm + Bm), 4, "march", key=K, density=dens, seed=2700 + len(n))
    s0 = c.s0[n]
    # 子鴨のまね：句（4小節）の最初の2小節を、1拍おくれて1オクターブ上で。回によって、まねる句の数が変わる
    for st, L, m, mk in notes:
        bar = int(st // B) - s0; ph = bar // 4
        if bar % 4 < 2 and L >= 0.3 and (ph * 0.37) % 1 < COPY[n]:
            WH.at(round(st + 1.0, 3), f"{nm(m + 12)}:{round(min(L, 0.6), 3)}")
play_melody(c, "池", e2b(POND), 4, "air", key=K, density=0.25, seed=2711)
s0 = c.s0["池"]
for q in range(0, 24, 4):                                                       # 池：子鴨は遠くで、まねがおくれる（2拍おくれ）
    WH.at(round((s0 + q) * B + 2.0, 3), f"{nm(77 + (q % 8) // 4 * 4)}:0.6")
nb = play_melody(c, "帰り", e2b(A + Bm + A), 4, "march", key=K, density=0.25, seed=2712)
s0 = c.s0["ぴよ"]
WH.at(round(s0 * B + 0.5, 3), "F6:0.5")                                         # ぴよ

# ---------- ファゴットのよちよちと、ピチカートの足どり ----------
ROOT = {"F": 41, "Bb": 46, "C": 36}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    th = r + 4; fi = r + 7
    if n == "ぴよ":
        if i == 0: BS.bar(b, f"{nm(41)}:{round(2 * T3, 4)} R:{round(4 * T3, 4)}")
        continue
    VP.bar(b, f"{nm(r + 12)}:{round(T3, 4)} R:{round(2 * T3, 4)} {nm(fi + 12)}:{round(T3, 4)} R:{round(2 * T3, 4)}")
    if n == "足どり": continue
    if n == "池":
        if i % 2 == 0: BS.bar(b, f"{nm(r)}:2,")
        continue
    BS.bar(b, f"{nm(r)}:{round(2 * T3, 4)} R:{round(T3, 4)} {nm(fi if fi <= 50 else fi - 12)}:{round(2 * T3, 4)} R:{round(T3, 4)}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の027（第3版）。川べりを一列に歩く鴨の親子。シングル・ジグ（6/8・付点4分＝118）、F イオニア。親鴨の笛がぴょこぴょこ進むと、子鴨のティン・ホイッスルが1拍おくれて同じ足どりをまねる。伴奏はファゴットの低い「よちよち」とチェロのピチカート。池では親子でゆったり泳ぎ、また岸に上がって帰り、最後に子鴨が1羽「ぴよ」と鳴く。",
       harm_scenes=None, tail_scene="ぴよ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air027.json", "w"), ensure_ascii=False)

# 1/3 拍を丸めてできる「R:0」を取りのぞく
_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
