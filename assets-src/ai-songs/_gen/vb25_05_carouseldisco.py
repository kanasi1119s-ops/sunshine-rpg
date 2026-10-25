# vb25 05「回転木馬ディスコティック」Carousel Discotheque（仮）— ダンス（ディスコ）。D ドリアン／D短調（サビは平行調の F長調）・128・4/4。
#   間奏だけ ×0.75（96）。最後のサビは +1（D#短調／F#長調）
# 物語: 閉園後の遊園地。最後のお客さんが帰って明かりが落ちると、メリーゴーランドの木馬たちがそっと目を覚まし、ミラーボールの月の下で夜通しディスコを踊る。
#   閉園のアナウンスがもう一度流れて、みんなが一瞬かたまる。でも夜明けまではまだ時間がある。最後は全部の木馬がそろって回り、朝が来ると元の場所で止まる。
# 場面と強さ: 閉園（4つ打ちのキックだけ → 回転木馬のカリオペ）→ 木馬が目を覚ます（Aメロ・語る）→ たてがみを揺らして（Bメロ・溜め → キメの止め）
#   → 回れ回れ（サビ1・強）→ ミラーボールの月（間奏・ブラス）→ 2周目（2番。前半はブラスが歌を受け取る）→ Bメロ2（キメ）→ サビ2（ノリを入れかえ）
#   → 閉園のアナウンス（静けさ・テンポ ×0.75・ストリングスのしゃくりが主旋律）→ 夜明けまで（こもった音・ローパス → 1拍の完全な無音）
#   → 全部の木馬がそろって回る最後のサビ（+1・最大）→ 木馬が止まる（フェードアウト）
# 旋律の性格: 付点（0.75＋0.25）で跳ねる、グルーヴに乗る中音域（D4〜D5）。Aメロは16分の細かい言葉、サビは同じ音を付点で3回打つフック。最高音 C6〜D6
# 派手な展開: テンポの変化（間奏だけ ×0.75）・全員の止め（キメ2回）・最後のサビ前のフィルター・1拍の完全な無音・最後のサビ +1・サビごとのリズムの入れかえ
from vb25_lib import *

S = Song("05", "carouseldisco", "回転木馬ディスコティック（仮）", "Carousel Discotheque", 128, 4, "D", "dorian", "ダンス（ディスコ・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # D ドリアン（Aメロ）
KDm = Key("D", "minor")      # 間奏の旋律（B♭ を含む）
KF = Key("F", "major")       # サビ（平行調）
KG = Key("F#", "major")      # 最後のサビ（+1）


def chk(*lists):
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


A_CH = ["Dm7", "G7", "Dm7", "G7", "Bbmaj7", "A7", "Dm7", "Dm7"]
B_CH = ["Gm7", "C7", "Fmaj7", "Dm7", "Gm7", "C7", "Bbmaj7", "A7"]
C_CH = ["Bbmaj7", "C7", "Am7", "Dm7", "Gm7", "C7", "Fmaj7", "D7",
        "Gm7", "A7", "Dm7", "Dm7/C", "Bbmaj7", "Bbm6", "Am7", "A7"]             # D7＝ii（Gm）への副属和音、Bbm6＝同主短調から借りた iv
ANN = ["Dm9", "Gm9", "Cmaj7", "Fmaj7", "Bbmaj7", "Em7b5", "A7sus4", "A7"]
DAWN = ["Gm7", "A7", "Dm7", "Dm7/C", "Bbmaj7", "C7", "Bbmaj7", "C#7"]            # C#7＝次の調（F#長調）の V

S.scene("閉園", 8, "intro", ["Dm7", "Dm7", "Dm7", "Dm7", "Dm7", "G7", "Dm7", "A7"])
S.scene("木馬が目を覚ます", 16, "verse", A_CH)
S.scene("たてがみを揺らして", 8, "pre", B_CH)
S.scene("回れ回れ", 16, "chorus", C_CH)
S.scene("ミラーボールの月", 8, "interlude", A_CH)
S.scene("2周目", 16, "verse", A_CH)
S.scene("たてがみを揺らして2", 8, "pre", B_CH)
S.scene("回れ回れ2", 16, "chorus", C_CH)
S.scene("閉園のアナウンス", 16, "bridge", ANN)
S.scene("夜明けまで", 8, "build", DAWN)
S.scene("全部の木馬", 24, "chorus", [tr_chord(c, 1) for c in C_CH + C_CH[:8]])
S.scene("木馬が止まる", 6, "outro", [tr_chord(c, 1) for c in ["Bbmaj7", "C7", "Fmaj7", "Fmaj7", "Fmaj7", "Fmaj7"]])
S.tempo = [{"bar": S.sc("閉園のアナウンス")[0] + 1, "bpm": 96}, {"bar": S.sc("夜明けまで")[0] + 1, "bpm": 128}]

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, patch="popLeadClear")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
SLAP = S.track("スラップベース", "slap", volume=0.2, pan=0.0, duck=0.15,
               fx=[{"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 2200, "high": 1.5}])
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=0.0, reverb=0.25, gainDb=2,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 1}]) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.09, pan=0.25, reverb=0.35, sustain=1.5) for i in range(4)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.07, pan=-0.25, reverb=0.2) for i in range(3)]
MUF = [S.track(f"こもったオルガン{i + 1}（夜明けまで）", "drawbarOrgan", volume=0.08, pan=-0.25, reverb=0.3,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}]) for i in range(3)]
GTR = [S.track(f"カッティングのギター{i + 1}", "guitar", **clean_gtr_spec(0.085, 0.4)) for i in range(2)]
for g_ in GTR: g_.spec["sustain"] = 0.4
CAL = S.track("回転木馬のカリオペ", "lead", patch="calliope", volume=0.1, pan=0.15, reverb=0.3, mono=True, breath=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "eq", "low": 0, "mid": 2, "midHz": 1200, "high": -2}])
CHIME = S.track("アナウンスのチャイム・きらめき", "fmBell", volume=0.09, pan=0.2, reverb=0.45, sustain=1.2)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役 =================
# Aメロ（D ドリアンの度数。oct=4 で 1 = D4）: 付点で跳ねつつ、16分の細かい言葉で語る
A1 = ["R:0.25 1:0.25 3:0.25 1:0.25 4:0.75 3:0.25 R:0.25 1:0.25 3:0.25 4:0.25 5:0.5 3:0.5",
      "R:0.25 2:0.25 4:0.25 2:0.25 6:0.75 4:0.25 R:0.25 2:0.25 4:0.25 6:0.25 7:0.5 6:0.5",
      "1:0.25 1:0.25 3:0.25 5:0.25 3:0.25 1:0.25 R:0.5 5:0.75 4:0.25 3:0.5 1:0.5",
      "R:0.25 4:0.25 4:0.25 4:0.25 6:0.25 4:0.25 2:0.5 R:0.25 7,:0.25 2:0.25 4:0.25 6:1",
      "R:0.25 b6:0.25 5:0.25 4:0.25 5:0.75 3:0.25 R:0.25 b6:0.25 5:0.25 4:0.25 3:0.5 1:0.5",
      "R:0.25 5:0.25 4:0.25 2:0.25 #7,:0.75 2:0.25 R:0.25 4:0.25 5:0.25 7:0.25 #7:1",
      "1':0.75 7:0.25 5:0.5 4:0.25 3:0.25 1:0.5 R:0.5 3:0.25 4:0.25 5:0.5",
      "4:0.75 3:0.25 1:1 R:2"]
A1b = ["R:0.25 5:0.25 5:0.25 4:0.25 5:0.25 7:0.25 5:0.25 4:0.25 R:0.25 3:0.25 4:0.25 5:0.25 1':0.5 7:0.5",
       "R:0.25 6:0.25 6:0.25 5:0.25 6:0.25 1':0.25 6:0.25 5:0.25 R:0.25 4:0.25 5:0.25 6:0.25 2':0.5 1':0.5",
       "R:0.25 1':0.25 7:0.25 5:0.25 3:0.25 5:0.25 7:0.25 1':0.25 3':0.75 1':0.25 7:0.5 5:0.5",
       "6:0.75 5:0.25 4:0.5 2:0.5 R:0.25 4:0.25 6:0.25 1':0.25 7:1",
       "R:0.25 4:0.25 b6:0.25 1':0.25 R:0.25 4:0.25 b6:0.25 1':0.25 3':0.5 1':0.25 b6:0.25 5:0.5 4:0.5",
       "R:0.25 5:0.25 #7:0.25 2':0.25 R:0.25 5:0.25 #7:0.25 4':0.25 2':0.5 #7:0.25 5:0.25 4:0.5 2:0.5",
       "1:0.25 3:0.25 5:0.25 1':0.25 5:0.5 3:0.5 R:0.25 4:0.25 3:0.25 1:0.25 3:1",
       "1:2 R:2"]
A2b = ["R:0.25 1':0.25 1':0.25 7:0.25 5:0.25 4:0.25 5:0.25 7:0.25 R:0.25 1':0.25 2':0.25 3':0.25 2':0.5 1':0.5",
       "R:0.25 6:0.25 6:0.25 5:0.25 4:0.25 2:0.25 4:0.25 6:0.25 R:0.25 7:0.25 1':0.25 2':0.25 1':0.5 6:0.5",
       "5:0.75 4:0.25 3:0.25 4:0.25 5:0.25 7:0.25 1':0.75 7:0.25 5:0.5 3:0.5",
       "4:0.75 2:0.25 7,:0.5 2:0.5 4:0.25 6:0.25 1':0.25 2':0.25 1':1",
       "R:0.25 b6:0.25 b6:0.25 b6:0.25 5:0.25 4:0.25 3:0.25 4:0.25 5:0.75 b6:0.25 1':1",
       "R:0.25 #7:0.25 #7:0.25 #7:0.25 2':0.25 #7:0.25 5:0.25 4:0.25 2:0.75 4:0.25 5:1",
       "1':0.25 5:0.25 3:0.25 1:0.25 3:0.25 5:0.25 1':0.25 3':0.25 2':0.75 1':0.25 7:0.5 5:0.5",   # D5→D4→F5 を16分で（歌いにくい所）
       "4:0.75 3:0.25 1:1 R:2"]
# Bメロ（F長調の度数。oct=4 で 1 = F4）: 付点で一段ずつ上がる。最後はキメで止める
BM = ["2:0.75 4:0.25 5:0.5 4:0.5 6:1 5:1", "3:0.75 5:0.25 4:0.5 5:0.5 1':1 7:1", "1':0.75 3':0.25 2':0.5 1':0.5 5:1 3':1", "2':1.5 1':0.5 6:2",
      "2':0.75 4':0.25 2':0.5 1':0.5 6:1 4:1", "1':0.75 3':0.25 1':0.5 4:0.5 5:1 3:1", "4:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "3':0.5 R:0.5 3':0.5 R:2.5"]
BM2 = BM[:4] + ["4':0.75 3':0.25 2':0.5 1':0.5 6:1 2':1", "3':0.75 1':0.25 7:0.5 5:0.5 3:1 5:1", "6:0.5 1':0.5 3':0.5 4':0.5 5':1 4':1", "3':0.5 R:0.5 #5:0.5 R:2.5"]
# サビ（F長調）: 同じ音を付点で3回打つフック（0.75＋0.25＋0.5）
CH = ["R:0.5 3':0.75 3':0.25 3':0.5 5':0.5 4':1 1':0.5", "R:0.5 2':0.75 2':0.25 2':0.5 4':0.5 3':1 5:0.5",
      "R:0.5 1':0.75 3':0.25 5':1 3':0.5 1':0.5 6:0.5", "R:0.5 6:0.5 1':0.5 2':0.5 3':2",
      "R:0.5 4':0.75 4':0.25 4':0.5 2':0.5 6:1 2':0.5", "R:0.5 3':0.75 3':0.25 3':0.5 4:0.5 5:1 3':0.5",
      "1':0.75 3':0.25 5':1 3':0.75 1':0.25 5:1", "R:0.5 #1':0.5 3':0.5 6':0.5 5':1 3':1",
      "R:0.5 2':0.75 2':0.25 2':0.5 6:0.5 2':1 4':0.5", "R:0.5 3':0.75 2':0.25 3':0.5 #5:0.5 7:1 2':0.5",
      "R:0.5 3':0.75 3':0.25 3':0.5 2':0.5 1':0.75 6:0.25 6:0.5", "5:0.5 6:0.5 1':0.5 3':0.5 5':2",
      "R:0.5 4':0.75 3':0.25 4':0.5 5':0.5 4':1 1':0.5", "R:0.5 2':0.75 1':0.25 b6:0.5 1':0.5 4':1 2':0.5",
      "3':0.75 1':0.25 5:0.5 1':0.5 3':1 6:1", "#5:1 7:1 2':1 3':1"]
# 最後のサビの後ろ8小節（全部の木馬がそろう）: 長くのばして回る
LASTX = ["R:0.5 5':0.75 5':0.25 5':0.5 4':0.5 3':1 1':0.5", "R:0.5 4':0.75 4':0.25 4':0.5 3':0.5 2':1 5:0.5",
         "R:0.5 3':0.75 3':0.25 3':0.5 5':0.5 3':1 1':0.5", "2':2 3':2",
         "R:0.5 5':0.75 5':0.25 5':0.5 4':0.5 3':1 1':0.5", "R:0.5 4':0.75 4':0.25 4':0.5 2':0.5 5:1 2':0.5",
         "3':1 5':1 4':1 2':1", "1':4"]
# 閉園のアナウンス（96）: ストリングスがしゃくりで歌い（D短調の度数）、後半は歌の役が静かに戻る
SM = ["5:2/ 3:1 1:1", "4:3/ 6:1", "7:2/ 5:1 2:1", "3:3/ R:1", "6:2/ 1':1 3':1", "4:2 6:1 1':1", "1':2/ 7:1 5:1", "#7:4~"]
VN = ["R:1 3:1 5:1 1':1", "7:3 6:1", "5:2 7:1 2':1", "5:3 R:1", "R:1 4:1 6:1 1':1", "6:2 4:2", "4:1 5:1 1':1 5:1", "#7:3 R:1"]
# 夜明けまで（F長調）: 前半は8分で上がり、後半はこもった声で
DW = ["R:0.5 2:0.5 4:0.5 6:0.5 1':1 6:1", "#5:0.75 7:0.25 2':0.5 7:0.5 3':1 2':1", "R:0.5 6:0.5 1':0.5 3':0.5 5':1.5 3':0.5", "4':1 3':0.5 1':0.5 5:2",
      "4:1 6:1 1':1 3':1", "5:1 7:1 2':1 4':1", "6:1 1':1 3':1 4':1"]
chk(A1, A1b, A2b, BM, BM2, CH, LASTX, SM, VN, DW)

for i, b in enumerate(S.sc("木馬が目を覚ます")): V.bar(b, K.mel((A1 + A1b)[i], oct=4))
for i, b in enumerate(S.sc("2周目")):
    if i < 8: BR[0].bar(b, K.mel(A1[i], oct=4))                         # 2番の前半は、ブラスが歌を受け取る
    else: V.bar(b, K.mel(A2b[i - 8], oct=4))
for i, b in enumerate(S.sc("たてがみを揺らして")): V.bar(b, KF.mel(BM[i], oct=4))
for i, b in enumerate(S.sc("たてがみを揺らして2")): V.bar(b, KF.mel(BM2[i], oct=4))
for name in ("回れ回れ", "回れ回れ2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KF.mel(CH[i], oct=4))
for i, b in enumerate(S.sc("閉園のアナウンス")):
    if i < 8: STR[3].bar(b, KDm.mel(SM[i], oct=4))
    else: V.bar(b, KDm.mel(VN[i - 8], oct=4), low=False)
for i, b in enumerate(S.sc("夜明けまで")):
    if i < 4: V.bar(b, KF.mel(DW[i], oct=4))
    elif i < 7: V.low.bar(b, KF.mel(DW[i], oct=4))                      # こもった声（重ねのパートだけ・元の高さ）
    else: V.low.bar(b, KG.mel("5:1 7:1 2':1 R:1", oct=4))             # C#7（F#長調の V）
LAST_L = [l.replace("6':", "5':") for l in CH + LASTX]
for i, b in enumerate(S.sc("全部の木馬")): V.bar(b, KG.mel(LAST_L[i], oct=4))

# ================= 回転木馬のカリオペ（イントロ・終わり） =================
CAR = ["1':0.75 3':0.25 5':0.5 3':0.5 1':1 5:1", "6:0.75 1':0.25 2':0.5 1':0.5 6:1 4:1", "1':0.75 3':0.25 5':0.5 6':0.5 5':1 3':1", "#7:1 2':1 4':1 #7:1"]
chk(CAR)
for i, b in enumerate(S.sc("閉園")):
    if i >= 4: CAL.bar(b, KDm.mel(CAR[i - 4], oct=4))
for i, b in enumerate(S.sc("木馬が止まる")):
    CAL.bar(b, KG.mel(["5:1.5 4:0.5 3:1 1:1", "2:1.5 3:0.5 4:1 5:1", "1':2 7:1 5:1", "3:4", "R:4", "R:4"][i], oct=4))

# ================= ブラス（合いの手・間奏の主旋律） =================
MIR = ["5':0.5 R:0.25 5':0.25 4':0.5 3':0.5 1':1 R:1", "4':0.5 R:0.25 4':0.25 3':0.5 2':0.5 6:1 R:1",
       "3':0.5 R:0.25 3':0.25 4':0.5 5':0.5 6':0.75 5':0.25 3':0.5 1':0.5", "#5:0.5 7:0.5 2':0.5 3':0.5 #5':1 R:1"]
chk(MIR)
for i, b in enumerate(S.sc("ミラーボールの月")): BR[0].bar(b, KF.mel(MIR[i % 4], oct=3) if i < 7 else KF.mel("3':1 2':1 #5:1 3':1", oct=3))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 62, 3)
    stab = None
    if n in ("回れ回れ", "回れ回れ2", "全部の木馬") and i % 2 == 1: stab = "R:3.5 X:0.5"           # 4拍目の裏から次の頭へ「パッ」
    if n in ("回れ回れ", "回れ回れ2", "全部の木馬") and i % 4 == 0: stab = "X:0.5! R:3.5"
    if n.startswith("たてがみ") and i == 7: stab = "X:0.5! R:0.5 X:0.5! R:2.5"               # キメ
    if n == "木馬が目を覚ます" and i % 4 == 3: stab = "R:2.5 X:0.25 X:0.25 X:0.5' R:0.5"
    if stab:
        for j in range(3):
            if n == "2周目" and j == 0: continue
            BR[j].bar(b, stab.replace("X", nm(v[j])))
# 間奏の後ろ2本（ハモり）
for i, b in enumerate(S.sc("ミラーボールの月")):
    v = voice(S.chords[b], 57, 3)
    for j in (1, 2): BR[j].bar(b, f"{nm(v[j - 1])}:2 {nm(v[j - 1])}:2")

# ================= 伴奏 =================
def slap_line(b, style):
    """スラップベースの音域（E1〜G3）に収まらない型は、8分の根音にする"""
    s_ = bass_line(S, b, style)
    if any(midi(x.split(":")[0]) > midi("G3") for x in s_.split() if not x.startswith("R")): s_ = bass_line(S, b, "root8")
    return s_


def cut16(b, ch):
    """カッティング: 16分の刻み（弾く音＝和音の2音、消す音＝休み）"""
    v = voice(ch, 64, 2)
    pat = "x.xx.x.x.xx.x.xx" if b % 2 else ".x.xx.x..x.xx.x."
    for j in range(2):
        GTR[j].bar(b, " ".join((f"{nm(v[j])}:0.25" + ("," if c == "x" else "") if c != "." else "R:0.25") for c in pat))

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    chorus = n in ("回れ回れ", "回れ回れ2", "全部の木馬")
    verse = n in ("木馬が目を覚ます", "2周目")
    # スラップベース
    if n == "閉園": SLAP.bar(b, slap_line(b, "disco")) if i >= 4 else None
    elif verse: SLAP.bar(b, slap_line(b, "disco" if i % 2 == 0 else "oct8"))
    elif n.startswith("たてがみ"): SLAP.bar(b, slap_line(b, "push") if i < 7 else f"{nm(low(ch, 'E1'))}:0.5! R:0.5 {nm(low(ch, 'E1'))}:0.5! R:2.5")
    elif chorus or n == "ミラーボールの月": SLAP.bar(b, slap_line(b, "disco"))
    elif n == "閉園のアナウンス": SLAP.bar(b, f"{nm(low(ch, 'E1'))}:2 {nm(low(ch, 'E1') + 7)}:2" if i >= 4 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "夜明けまで": SLAP.bar(b, slap_line(b, "oct8") if i < 4 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "木馬が止まる" and i < 4: SLAP.bar(b, slap_line(b, "half"))
    # オルガン: Aメロは裏の刻み、アナウンスでは伸ばし
    if verse or n == "閉園" and i >= 4:
        for j in range(3): ORG[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    elif n == "閉園のアナウンス" or n == "木馬が止まる":
        for j in range(3): ORG[j].bar(b, f"{nm(v[j])}:4")
    elif chorus:
        for j in range(3): ORG[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:2.5")
    elif n == "夜明けまで" and i >= 4:
        for j in range(3): MUF[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    # ストリングス: サビと Bメロで伸ばし、サビの頭で「しゃくり」上げる
    if chorus or n.startswith("たてがみ") and i < 7 or n == "閉園のアナウンス":
        vs = voice(ch, 69, 3)
        for j in range(3): STR[j].bar(b, f"{nm(vs[j])}:4" + ("/" if (chorus and i % 4 == 0) else ""))
    # カッティング
    if (verse and i >= 8) or chorus or n == "ミラーボールの月":
        cut16(b, ch)
# ストリングスの「しゃくり」の合いの手（サビの4小節目ごとに、下から駆け上がる）
for name, kk in (("回れ回れ", KF), ("回れ回れ2", KF), ("全部の木馬", KG)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: STR[3].bar(b, kk.mel("R:2 1':0.25 2':0.25 3':0.25 5':0.25 6':1/", oct=3))

# アナウンスのチャイム（4つの音）ときらめき
CHIME.bar(S.sc("閉園のアナウンス")[0], KDm.mel("5':1 3':1 1':1 5:1", oct=4))
CHIME.bar(S.sc("閉園のアナウンス")[8], KDm.mel("5:1 1':1 3':1 5':1", oct=4))
for i, b in enumerate(S.sc("全部の木馬")):
    if i % 8 == 6: CHIME.bar(b, KG.mel("R:2 5':0.5 3':0.5 1':1", oct=4))
riser(FX, S.sc("回れ回れ")[0], 4, "C4"); riser(FX, S.sc("回れ回れ2")[0], 4, "C4")
FX.bar(S.sc("閉園のアナウンス")[0], "E4:4")                              # ダウンリフター（テンポが落ちる）
riser(FX, S.sc("全部の木馬")[0] - 0.25, 8, "D4")
cym_swell(CYM, S.sc("ミラーボールの月")[0], 2, "C4"); cym_swell(CYM, S.sc("2周目")[0], 2, "E4")

# ================= ドラム（電子のドラム・ディスコ） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "閉園":
        if i < 4: D.set(b, "X...X...X...X...", "." * 16, "." * 16)               # 4つ打ちのキックだけ
        else: vgroove(D, b, "disco", seed=b, s="............X...")
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("木馬が目を覚ます", "2周目"):
        vgroove(D, b, "disco" if i < 8 else "four16", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if n == "2周目" and i < 8: D.cym(b, ("F2:0.5 " if i % 4 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("たてがみ"):
        vgroove(D, b, "half" if i < 4 else "disco", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16); crash(D, b, "G2", 4)   # キメ（全員の止め）
    elif n == "回れ回れ":
        vgroove(D, b, "disco", seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "tomdown")
    elif n == "回れ回れ2":
        vgroove(D, b, "twostep" if i < 8 else "four16", ghosts=0.3, seed=b)   # 2回目は2ステップから入れかえ
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "build")
    elif n == "ミラーボールの月":
        vgroove(D, b, "disco", seed=b)
        D.cym(b, ("C2:0.5 " if i == 0 else "F2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if last: put_fill(D, b, "tomtrip")
    elif n == "閉園のアナウンス":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if i == 4: crash(D, b, "C2", 8)
        if last: put_fill(D, b, "build")
    elif n == "夜明けまで":
        if i < 4: vgroove(D, b, "four16", seed=b)
        else: D.set(b, "X...X...X...X...", "." * 16, "." * 16)
        if i == 0: crash(D, b, "G2")
        if last: D.set(b, "X...X...X.X.X...", "....X...XXX.....", "." * 16)
    elif n == "全部の木馬":
        vgroove(D, b, "disco" if i < 16 else "four16", seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last: put_fill(D, b, "tomdown")
    elif n == "木馬が止まる":
        if i < 2: vgroove(D, b, "disco", seed=b)
        elif i < 4: D.set(b, "X...X...X...X...", "." * 16, "..x...x...x...x.")
        if i == 0: crash(D, b, "C2", 8)

SIL.add(S.sc("たてがみを揺らして")[-1], 2, 4)      # キメの止め（1回目）
SIL.add(S.sc("たてがみを揺らして2")[-1], 2, 4)     # キメの止め（2回目）
SIL.add(S.sc("夜明けまで")[-1], 3, 4)              # 最後のサビの前の1拍は、完全な無音
SIL.apply()

S.fade_out = 12
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の05。ダンス（ディスコ）。D ドリアン／D短調（サビは F）・128、閉園のアナウンスの間だけ 96。最後のサビは +1（F#）。"
          "閉園後の遊園地で、メリーゴーランドの木馬たちが夜通しディスコを踊る。4つ打ちのキックだけで始まり、回転木馬のカリオペ、付点で跳ねる Aメロ、"
          "付点の3連打のサビ、スラップベース・ブラス・オルガン・カッティング、キメの止め2回、テンポが落ちるアナウンスの間（ストリングスのしゃくり）、"
          "こもった夜明け前と1拍の無音、+1 の最後のサビ、木馬が止まってフェードアウト。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
