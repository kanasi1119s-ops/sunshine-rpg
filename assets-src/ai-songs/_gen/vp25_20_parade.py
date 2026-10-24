# vp25 20「パレードが通る」Here Comes the Parade（仮）— J-POP（マーチ）。D長調（山車で G長調）・150・4/4。主役の楽器: ピッコロ
# 物語: 町のお祭りの日。沿道で待っていると、遠く左の方から楽隊の音が聞こえてくる。近づいて、目の前を楽隊が通り、山車、子ども会の行列が続く。
#   やがて右の方へ遠ざかり、静けさが戻る。
# 形: 遠くからパレードが近づき、目の前を通り、遠ざかる
# 場面と強さ: 強さは「距離」だけで決める。遠い＝小さくこもって左／目の前＝最大でまん中／遠ざかる＝右へ小さくこもる／去ったあとの静けさ
# 旋律の性格: 付点のマーチのリズムの明るい旋律（ピッコロ）
# 崩す所: 強さを曲の構成ではなく「距離」だけで決める（同じ旋律でも、遠いと小さく、こもって、左右に寄る）
from vp25_lib import *

S = Song("20", "parade", "パレードが通る（仮）", "Here Comes the Parade", 150, 4, "D", "major", "J-POP（マーチ）")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
MARCH = ["D", "G/D", "A7", "D", "Bm", "E7", "A", "A7"]
MARCH2 = ["D", "D/F#", "G", "Gm6", "D/A", "B7", "Em7", "A7"]
FLOAT = ["G", "C", "D7", "G", "Em", "A7", "D7", "G"]
KIDS = ["D", "Bm", "G", "A"]
S.scene("遠くの音", 16, "intro", MARCH)
S.scene("近づく", 24, "verse", MARCH + MARCH2 + MARCH)
S.scene("目の前の楽隊", 32, "chorus", MARCH + MARCH2 + MARCH + MARCH2)
S.scene("山車", 24, "bridge", FLOAT)
S.scene("子ども会", 24, "verse", KIDS)
S.scene("遠ざかる", 24, "outro", MARCH + MARCH2 + MARCH)
S.scene("静けさ", 8, "outro", ["D"] * 8)
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
KG = Key("G", "major")

# 距離（0＝遠い〜1＝目の前）と、左右の位置（-1 左〜1 右）
DIST, POS = [], []
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    d, p = {"遠くの音": (0.1 + 0.15 * i / L, -1.0), "近づく": (0.25 + 0.6 * i / L, -1.0 + 0.8 * i / L), "目の前の楽隊": (1.0, -0.2 + 0.4 * i / L),
            "山車": (0.95, 0.2), "子ども会": (0.9 - 0.1 * i / L, 0.2 + 0.2 * i / L), "遠ざかる": (0.8 - 0.65 * i / L, 0.4 + 0.6 * i / L), "静けさ": (0.0, 1.0)}[n]
    DIST.append(round(d, 3)); POS.append(round(p, 3))
# 左・まん中・右の3つの写しを、位置で入れかえる（遠いほど、こもった写し）
WL = [round(max(0, -p) * (1 - d) + 0.02, 3) for d, p in zip(DIST, POS)]
WR = [round(max(0, p) * (1 - d) + 0.02, 3) for d, p in zip(DIST, POS)]
WC = [round(min(1.0, d * 1.1), 3) for d in DIST]
FAR = [{"type": "filter", "kind": "lowpass", "freq": 2200, "q": 0.7}, {"type": "reverb", "mix": 0.35}]
PIC = {"L": S.track("主役: ピッコロ（遠く左）", "panflute", patch="piccolo", volume=0.24, pan=-0.85, gainDb=5, phrase=4, mono=True, barGain=WL, fx=FAR, reverb=0.5),
       "C": S.track("主役: ピッコロ（目の前）", "panflute", patch="piccolo", volume=0.24, pan=0.0, gainDb=5, phrase=4, mono=True, barGain=WC, reverb=0.25,
                    fx=[{"type": "eq", "low": -4, "mid": 1.5, "midHz": 2200, "high": 0}]),
       "R": S.track("主役: ピッコロ（遠く右）", "panflute", patch="piccolo", volume=0.24, pan=0.85, gainDb=5, phrase=4, mono=True, barGain=WR, fx=FAR, reverb=0.5)}
BR = {"L": [S.track(f"楽隊の金管（左{i}）", "brass", patch="trombone", volume=0.13, pan=-0.8, barGain=WL, fx=FAR, reverb=0.5) for i in range(2)],
      "C": [S.track(f"楽隊の金管（まん中{i}）", "brass", patch="trombone", volume=0.13, pan=[-0.15, 0.15][i], barGain=WC, reverb=0.25) for i in range(2)],
      "R": [S.track(f"楽隊の金管（右{i}）", "brass", patch="trombone", volume=0.13, pan=0.8, barGain=WR, fx=FAR, reverb=0.5) for i in range(2)]}
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.18, pan=0.0, delay=0.5), barGain=WC)
BASS = S.track("ベース", "bass", **rock_bass_spec(0.19), barGain=[round(0.2 + 0.8 * d, 3) for d in DIST])
GLK = S.track("鉄琴（山車）", "glockenspiel", patch="glockenspiel", volume=0.12, pan=0.25, reverb=0.35, sustain=1.5, barGain=WC)
D = S.drumkit()
S.drum_gain = {k: {"barGain": [round(0.15 + 0.85 * d, 3) for d in DIST]} for k in ("kick", "snare", "hihat", "tom", "crash")}


def put3(trs, b, s):
    for side in ("L", "C", "R"):
        t = trs[side]
        if isinstance(t, list): continue
        t.bar(b, s)


# ---------- ピッコロ（付点のマーチ） ----------
MA = ["1':0.75 2':0.25 3':0.5 1':0.5 5:1 R:1", "4:0.75 5:0.25 6:0.5 4:0.5 2:1 R:1", "5:0.75 6:0.25 7:0.5 5:0.5 2':0.75 1':0.25 7:0.5 6:0.5", "5:2 R:2",
      "6:0.75 7:0.25 1':0.5 6:0.5 3':1 2':1", "#1':0.75 2':0.25 3':0.5 #4':0.5 #5':1 R:1", "3':0.75 2':0.25 1':0.5 7:0.5 6:0.5 5:0.5 #4:0.5 6:0.5", "5:3 R:1"]
MA2 = ["3':0.75 2':0.25 1':0.5 3':0.5 5':1 R:1", "4':0.75 3':0.25 2':0.5 4':0.5 6':1 R:1", "5':0.75 4':0.25 3':0.5 5':0.5 1'':1 7':0.5 6':0.5", "5':2 R:2",
       "5':0.75 #4':0.25 5':0.5 3':0.5 1':1 2':1", "3':0.75 #4':0.25 5':0.5 3':0.5 b7':1 6':1", "5':0.5 4':0.5 3':0.5 2':0.5 1':0.5 3':0.5 2':0.5 7:0.5", "1':3 R:1"]
for name in ("遠くの音", "近づく", "目の前の楽隊", "遠ざかる"):
    for i, b in enumerate(S.sc(name)):
        put3(PIC, b, K.mel((MA if (i // 8) % 2 == 0 else MA2)[i % 8], oct=4))
# 山車（G長調）: 鉄琴と金管のお囃子のような跳ねる句。ピッコロは高い合いの手
FL = ["5:0.5 5:0.5 1':0.5 5:0.5 3':1 2':1", "1':0.5 6:0.5 5:0.5 3:0.5 2:1 R:1", "4:0.5 5:0.5 6:0.5 4:0.5 2':1 1':1", "7:1 5:1 1':2"]
for i, b in enumerate(S.sc("山車")):
    GLK.bar(b, KG.mel(FL[i % 4], oct=5))
    if i % 2 == 1: put3(PIC, b, KG.mel("R:2 5':0.5 6':0.5 1'':1", oct=4))
    if i >= 8: LEAD.bar(b, KG.mel(["3':4", "2':2 1':2", "6:3 R:1", "7:4", "1':2 3':2", "#1':2 3':2", "#4':2 2':2", "3':4"][i % 8], oct=4))
# 子ども会: やさしい高い旋律（ピッコロだけ）
KD = ["5':1 3':1 5':1 3':1", "6':2 5':2", "4':1 2':1 4':1 2':1", "5':4", "3':1 5':1 1'':1 7':1", "6':2 5':2", "4':1 3':1 2':1 4':1", "3':4"]
for i, b in enumerate(S.sc("子ども会")): put3(PIC, b, K.mel(KD[i % 8], oct=4 if i < 16 else 3))
# 目の前: 歌の役が楽隊に重なる
for i, b in enumerate(S.sc("目の前の楽隊")):
    if i >= 8: LEAD.bar(b, K.mel(["3':2 2':1 1':1", "5':4", "4':2 3':1 2':1", "6:4", "3':2 #4':1 5':1", "6':2 #5':2", "5':2 4':1 2':1", "1':4"][i % 8], oct=4))

# ---------- 金管（後打ちの和音: 2拍目と4拍目） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "静けさ": continue
    v = voice(S.chords[b], 57, 2)
    pat = "R:1 X:1 R:1 X:1" if n != "山車" else "X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:1"
    for side in ("L", "C", "R"):
        for j in range(2): BR[side][j].bar(b, pat.replace("X", nm(v[j])))

# ---------- ベース（マーチの2拍: 根音と5度） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "静けさ": continue
    r = low(S.chords[b], "E1")
    BASS.bar(b, f"{nm(r)}:1! R:1 {nm(r + 7)}:1 R:1" if n != "山車" else bass_line(S, b, "walk"))

# ---------- ドラム（マーチ: スネアの連打とバスドラム） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "静けさ": continue
    D.set(b, "X.......X.......", "....X..xx...X.xx" if i % 2 == 0 else "....X..xX.x.Xxxx", "x...x...x...x...")
    if n == "目の前の楽隊" and i % 8 == 0: crash(D, b, "C2")
    if n == "山車": D.set(b, "X.....X.X.......", "....X.......X.x.", "x.x.x.x.x.x.x.x.")
    if i % 8 == 7: D.S[b] = "x.x.x.x.xxxxXXXX"

S.desc = ("仮: ボカロ曲のインスト25曲の20。マーチの J-POP。D長調（山車で G長調）・150。主役の楽器はピッコロ。お祭りのパレード。"
          "遠く左から楽隊が近づき、目の前を通り、山車（お囃子のような跳ねる句と鉄琴）、子ども会の行列が続いて、右へ遠ざかる。"
          "強さは距離だけで決める（左・まん中・右の写しを入れかえ、遠いほど小さく、こもる）。付点のマーチの旋律。自作")
S.write()
