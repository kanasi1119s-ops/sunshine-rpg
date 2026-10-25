# vb25 20「おひさまプログラム」Sunshine Program（仮）— J-POP（テクノ×バンド・疾走ピアノ）。B 長調・170・4/4。転調なし
# 物語: 朝日が昇るまでに、町じゅうの目覚まし時計をプログラムして回る小さなロボット。
# 場面と強さ: 起動（シンセのアルペジオだけ・小）→ 夜の町を回る（Aメロ・語る・中）→ 時計をセット（Bメロ・溜め・止め）
#   → 朝のプログラム（サビ・強）→ 屋根づたい（間奏・ギター）→ 2つ目の通り（ピアノが歌を受け取る）→ サビ2（前半 Half feel の入れかえ）
#   → 時計台のギターのソロ → 1拍の完全な無音 → 止まった時計（Half feel・ピアノとベース・弱）→ 夜明け前の暗い2小節（パッドだけ）
#   → こもった音（ローパス 800Hz の写し）でだんだん明るく → 朝日（最後のサビ・最大）→ 朝の鳥と和音
# 旋律の性格: 長調の4つのコードの循環（IV–I/3–V–vi）を回し、旋律と音数で変える。Aメロは16分の「カチコチ」の連打、
#   サビは同じ音の3連打のフックと5度・6度の跳躍。最高音 C#6
# 定番以外の和音: Bメロの D#7（vi への副属和音）→ E（偽終止のように IV へ）、サビの C#7（V への副属和音）、アウトロの Em6（同主短調からの借用）
from vb25_lib import *

S = Song("20", "ohisama", "おひさまプログラム（仮）", "Sunshine Program", 170, 4, "B", "major", "J-POP（テクノ×バンド）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"diGuitar": "emily"})
K = S.key   # B 長調（oct=4 で 1＝B4）


def chk(lines, beats=4):
    for l in lines: assert abs(total(K.mel(l, oct=4)) - beats) < 1e-6, ("拍の数", l, total(K.mel(l, oct=4)))


LOOP = ["E", "B/D#", "F#", "G#m"]
A_CH = LOOP * 3 + ["E", "B/D#", "C#m7", "F#"]
B_CH = ["C#m7", "D#m7", "E", "F#", "G#m", "D#7", "E", "F#sus4"]
C_CH = ["E", "B/D#", "F#", "G#m", "E", "B/D#", "C#7", "F#"]
HF_CH = ["G#m", "E", "B", "F#/A#", "G#m", "E", "C#m7", "D#7"]
SOLO_CH = LOOP * 3 + ["E", "B/D#", "C#7", "F#"]
LAST_CH = C_CH + C_CH + ["E", "B/D#", "C#7", "F#", "E", "Em6", "B", "B"]
OUT_CH = ["E", "Em6", "B/D#", "G#m7", "E", "Em6", "Badd9", "Badd9", "Badd9", "Badd9"]

S.scene("起動", 12, "intro", LOOP)
S.scene("夜の町を回る", 16, "verse", A_CH)
S.scene("時計をセット", 8, "pre", B_CH)
S.scene("朝のプログラム", 16, "chorus", C_CH)
S.scene("屋根づたい", 8, "interlude", LOOP)
S.scene("2つ目の通り", 16, "verse", A_CH)
S.scene("時計をセット2", 8, "pre", B_CH)
S.scene("朝のプログラム2", 16, "chorus", C_CH)
S.scene("時計台", 16, "solo", SOLO_CH)
S.scene("止まった時計", 16, "bridge", HF_CH)
S.scene("夜明け前", 2, "break", ["F#sus4", "F#sus4"])
S.scene("東の空", 8, "build", ["E", "B/D#", "F#", "G#m", "E", "B/D#", "C#m7", "F#"])
S.scene("朝日", 24, "chorus", LAST_CH)
S.scene("朝", 10, "outro", OUT_CH)

V = Voice(S, vol=0.22, delay=0.75)
PIANO_FX = [{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]
PN = S.track("ピアノ（右手）", "piano", volume=0.12, pan=-0.15, reverb=0.22, fx=PIANO_FX)
PNC = [S.track(f"ピアノ（右手の和音{i + 2}）", "piano", volume=0.1, pan=-0.15, reverb=0.22, fx=PIANO_FX) for i in range(2)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=-0.15, reverb=0.22, fx=PIANO_FX)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", volume=0.18, pan=-0.15, reverb=0.22, fx=PIANO_FX)
PNF = S.track("ピアノ（こもった写し）", "piano", volume=0.13, pan=-0.15, reverb=0.3,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}, {"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
ARP = S.track("シンセのアルペジオ（プログラム）", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.4, delay=0.75, sustain=0.5))
ARPF = S.track("シンセのアルペジオ（こもった写し）", "pad", patch="pluckSynth", volume=0.09, pan=0.4, sustain=0.6, reverb=0.3,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}, {"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.3}])
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.09, 0.0)) for i in range(3)]
LG = S.track("リードギター（時計台のソロ・合いの手）", "distGuitar", **lead_gtr_spec(0.15, -0.05))
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.055, pan=0.0, duck=0.2)) for i in range(3)]
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.045, pan=0.0, duck=0.4, sustain=0.9)) for i in range(2)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
BIRD = S.track("朝の鳥（ピッコロ）", "panflute", patch="piccolo", volume=0.1, pan=0.35, reverb=0.45, gainDb=1, mono=True)
RIDE = S.track("ライド", "crash", **{k: v for k, v in NAKED["crash"].items() if k != "human"})
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律 =================
# Aメロ（低め C#4〜D#5）: 16分の「カチコチ」。同じ音の連打と小さな動き。拍の頭の16分前から入る
A1 = ["R:0.25 3,:0.25 4,:0.25 4,:0.25 4,:0.25 6,:0.25 4,:0.5 R:0.25 4,:0.25 6,:0.25 1:0.25 7,:0.5 6,:0.5",
      "R:0.25 3,:0.25 3,:0.25 3,:0.25 5,:0.25 3,:0.25 2,:0.25 3,:0.25 R:0.25 5,:0.25 6,:0.25 5,:0.25 3,:1",
      "R:0.25 2,:0.25 2,:0.25 2,:0.25 3,:0.25 5,:0.25 7,:0.25 5,:0.25 R:0.25 2:0.25 7,:0.25 5,:0.25 6,:0.5 5,:0.5",
      "6,:0.5 1:0.25 6,:0.25 R:0.5 3,:0.25 5,:0.25 6,:1.5 R:0.5",
      "R:0.25 6,:0.25 1:0.25 1:0.25 1:0.25 7,:0.25 6,:0.5 R:0.25 4,:0.25 6,:0.25 1:0.25 3:0.5 2:0.5",
      "R:0.25 2:0.25 2:0.25 2:0.25 1:0.25 7,:0.25 1:0.5 R:0.25 5,:0.25 6,:0.25 7,:0.25 1:1",
      "R:0.25 7,:0.25 7,:0.25 7,:0.25 1:0.25 2:0.25 1:0.25 7,:0.25 5,:0.25 6,:0.25 7,:0.25 2:0.25 3:0.5 2:0.5",
      "1:0.75 7,:0.25 6,:0.5 5,:0.5 6,:1 R:1",
      # 後半: 4度・6度の跳躍を16分で（歌いにくい所）
      "R:0.25 4,:0.25 6,:0.25 1:0.25 4:0.25 3:0.25 1:0.25 6,:0.25 R:0.25 6,:0.25 6,:0.25 6,:0.25 1:0.5 6,:0.5",
      "R:0.25 3,:0.25 5,:0.25 1:0.25 3:0.25 2:0.25 1:0.25 5,:0.25 R:0.25 5,:0.25 6,:0.25 7,:0.25 1:1",
      "R:0.25 2,:0.25 5,:0.25 7,:0.25 2:0.25 7,:0.25 5,:0.25 7,:0.25 2:0.25 3:0.25 2:0.25 7,:0.25 5,:1",
      "6,:0.25 7,:0.25 1:0.25 3:0.25 5:0.5 3:0.5 1:1 R:1",
      "R:0.25 1:0.25 1:0.25 1:0.25 7,:0.25 1:0.25 3:0.5 R:0.25 1:0.25 7,:0.25 6,:0.25 4,:0.5 6,:0.5",
      "R:0.25 3,:0.25 3,:0.25 5,:0.25 1:0.25 7,:0.25 5,:0.5 R:0.25 3,:0.25 5,:0.25 1:0.25 2:1",
      "R:0.25 3:0.25 2:0.25 1:0.25 7,:0.25 6,:0.25 7,:0.25 1:0.25 2:0.25 3:0.25 4:0.25 3:0.25 2:1",
      "2:0.5 1:0.25 7,:0.25 5,:1 R:2"]
# 2番の後半（ピアノから歌が受け取り直す所）: 裏で切って跳ねる、F#5 → A#5 の16分の跳躍
A2b = ["R:0.25 6,:0.25 6,:0.25 1:0.25 R:0.25 1:0.25 3:0.25 1:0.25 4:0.5 3:0.25 1:0.25 6,:1",
       "R:0.25 5,:0.25 5,:0.25 1:0.25 R:0.25 1:0.25 2:0.25 1:0.25 3:0.5 2:0.25 1:0.25 5,:1",
       "R:0.25 7,:0.25 2:0.25 5:0.25 2:0.25 7,:0.25 2:0.25 5:0.25 7:0.5 5:0.5 2:1",
       "1:0.25 7,:0.25 6,:0.5 R:0.5 3,:0.25 5,:0.25 6,:2",
       "R:0.25 1:0.25 1:0.25 3:0.25 1:0.25 7,:0.25 6,:0.5 R:0.25 4,:0.25 6,:0.25 1:0.25 3:0.5 4:0.5"] + A1[13:]
# Bメロ: 少しずつ上げて溜める（G#4 → B5）。最後の小節は後ろ2拍が止め
BM = ["6,:1 7,:0.5 1:0.5 2:1 1:0.5 7,:0.5", "7,:1 1:0.5 2:0.5 3:1.5 2:0.5", "1:1 2:0.5 3:0.5 4:1 3:0.5 1:0.5", "2:2 7,:1 5,:1",
      "3:1 4:0.5 5:0.5 6:1 5:0.5 3:0.5", "#5:1 3:0.5 #5:0.5 7:1.5 6:0.5", "6:1 5:0.5 4:0.5 6:1 1':1", "7:2 R:2"]
# サビ: 同じ音の3連打のフック（F#5×3）→ 4度・5度・6度の跳躍。最高音 C#6
CH1 = ["R:0.5 5:0.5 5:0.5 5:0.5 1':1 6:1", "5:0.5 3:0.5 R:0.5 5,:0.5 3:1.5 R:0.5", "R:0.5 5:0.5 5:0.5 5:0.5 2':1 1':0.5 7:0.5", "6:1.5 2:0.5 1:2",
       "R:0.5 5:0.5 5:0.5 5:0.5 1':1 6:1", "5:0.5 3:0.5 R:0.5 1:0.5 5:0.5 1':0.5 2':1", "#4:1 3:0.5 2:0.5 #4:1 6:1", "5:3 R:1"]
CH2 = ["R:0.5 5:0.5 5:0.5 5:0.5 1':1 6:1", "5:0.5 3:0.5 R:0.5 5,:0.5 3:1.5 R:0.5", "R:0.5 5:0.5 5:0.5 5:0.5 2':1.5 7:0.5", "1':1 6:0.5 5:0.5 1:1 5:1",
       "6:0.5 6:0.5 6:0.5 1':0.5 2':1 1':1", "1':0.5 5:0.5 3:0.5 5:0.5 1':2", "R:0.5 #4:0.5 6:0.5 7:0.5 2':1 1':1", "2':3 R:1"]
CH2b = CH2[:4] + ["6:0.5 6:0.5 6:0.5 1':0.5 2':1.5 1':0.5", "7:0.5 5:0.5 3:0.5 5:0.5 1':1 5:1", "#4:0.5 6:0.5 1':0.5 2':0.5 1':1 7:1", "2':2 R:2"]
# 最後のサビの終わりの8小節: B5 の3連打 → C#6 → Em6 の上で下りる
LAST_T = ["R:0.5 1':0.5 1':0.5 1':0.5 2':1 1':1", "6:0.5 5:0.5 R:0.5 3:0.5 5:1 1':1", "2':1 1':0.5 7:0.5 #4:1 6:1", "7:2 2':2",
          "R:0.5 5:0.5 5:0.5 5:0.5 1':1 6:1", "5:1.5 4:0.5 2:2", "1':4", "R:4"]
# 止まった時計（Half feel）: 長い音でやさしく。前の4小節は歌なし
HF = ["R:4"] * 4 + ["3:2 5:1 3:1", "1:1.5 7,:0.5 6,:2", "6,:1 7,:1 1:1 3:1", "2:2 7,:2",
                    "6:2 5:1 3:1", "4:1.5 3:0.5 1:2", "3:1 5:1 1':1 7:0.5 6:0.5", "7:3 R:1",
                    "1':1 7:0.5 6:0.5 5:1 3:1", "6:2 4:2", "3:1 4:1 5:1 6:1", "#5:2 7:2"]
# 東の空（こもった音の中で、サビのフックを低く小さく → 上がっていく）
FL = ["R:0.5 5,:0.5 5,:0.5 5,:0.5 1:1 6,:1", "5,:0.5 3,:0.5 R:0.5 5,:0.5 3:1.5 R:0.5", "R:0.5 5,:0.5 5,:0.5 5,:0.5 2:1 1:0.5 7,:0.5", "6,:2 R:2",
      "1:1 2:1 3:1 4:1", "5:2 6:2", "7:1 1':1 2':1 7:1", "R:4"]
for L_ in (A1, A2b, BM, CH1, CH2, CH2b, LAST_T, HF, FL): chk(L_)

for i, b in enumerate(S.sc("夜の町を回る")): V.bar(b, K.mel(A1[i], oct=4))
for i, b in enumerate(S.sc("2つ目の通り")):
    if i < 8: PNM.bar(b, shift_oct(K.mel(A1[i], oct=4), 1) if i % 4 != 3 else K.mel(A1[i], oct=5))   # ピアノが歌を受け取る（1オクターブ上で）
    else: V.bar(b, K.mel(A2b[i - 8], oct=4))
for name in ("時計をセット", "時計をセット2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BM[i], oct=4))
for i, b in enumerate(S.sc("朝のプログラム")): V.bar(b, K.mel((CH1 + CH2)[i], oct=4))
for i, b in enumerate(S.sc("朝のプログラム2")): V.bar(b, K.mel((CH1 + CH2b)[i], oct=4))
for i, b in enumerate(S.sc("止まった時計")): V.bar(b, K.mel(HF[i], oct=4), low=i >= 8)
for i, b in enumerate(S.sc("東の空")): V.bar(b, K.mel(FL[i], oct=4), low=False)
for i, b in enumerate(S.sc("朝日")): V.bar(b, K.mel((CH1 + CH2 + LAST_T)[i], oct=4))

# ================= ギターのソロ（時計台）と合いの手 =================
SOLO = ["4:0.5 6:0.5 1':1 7:0.5 6:0.5 4:1", "3:0.5 5:0.5 1':1 2':0.5 1':0.5 5:1", "2':1.5 1':0.25 7:0.25 5:1 2:1", "6:3 R:1",
        "R:0.5 1':0.25 2':0.25 3':0.5 2':0.5 1':0.5 6:0.5 4:1", "5:0.5 1':0.5 3':1 2':0.5 1':0.5 5:1", "2':0.25 3':0.25 2':0.25 1':0.25 7:0.5 5:0.5 2':2", "1':1 7:1 6:2",
        "4':0.25 3':0.25 1':0.25 6:0.25 4':0.25 3':0.25 1':0.25 6:0.25 3':0.5 4':0.5 6':1",
        "5':0.25 3':0.25 1':0.25 5:0.25 5':0.25 3':0.25 1':0.25 5:0.25 3':1 5':1",
        "7':0.25 5':0.25 2':0.25 7:0.25 7':0.25 5':0.25 2':0.25 7:0.25 1'':1 7':1",
        "1'':1.5 6':0.5 5':1 3':1", "4':1 3':0.5 1':0.5 6:1 1':1", "5':2 3':1 5':1", "#4':1 6':1 1'':1 7':0.5 6':0.5", "5':3 R:1"]
for i, b in enumerate(S.sc("時計台")): LG.bar(b, K.mel(SOLO[i], oct=3))
# 屋根づたい: ギターの覚えやすいリフ（D3〜D5。歌の役とぶつからない高さ）
RIFF = ["4:0.5 4:0.25 6:0.25 1':0.5 6:0.5 7:0.5 6:0.5 4:1", "3:0.5 3:0.25 5:0.25 1':0.5 5:0.5 6:0.5 5:0.5 3:1",
        "2:0.5 2:0.25 5:0.25 7:0.5 5:0.5 2':0.5 1':0.5 7:1", "6:0.5 5:0.5 3:0.5 1:0.5 3:1 R:1"]
for i, b in enumerate(S.sc("屋根づたい")): LG.bar(b, K.mel(RIFF[i % 4], oct=3))
# 合いの手: サビの4小節目ごとに、ギターの短い句（歌の役が長い音のすき間）
for name in ("朝のプログラム", "朝のプログラム2", "朝日"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 3: LG.bar(b, K.mel("R:2 5:0.25 6:0.25 1':0.5 2':1", oct=3))
        if i % 8 == 7 and i < 16: LG.bar(b, K.mel("R:3 6:0.25 5:0.25 3:0.25 2:0.25", oct=3))

# ================= 伴奏 =================
def stab(b, ch, pat):
    """ピアノの和音の刻み（右手3音）。pat は '1:1 1:0.5 ...' のような長さの並び（R で休み）"""
    v = voice(ch, 68, 3)
    for j, tr_ in enumerate([PN] + PNC):
        tr_.bar(b, " ".join(("R:" + x.split(":")[1]) if x.startswith("R") else f"{nm(v[j])}:{x.split(':')[1]}" for x in pat.split()))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    # シンセのアルペジオ（プログラムの音）: 起動・Aメロ・サビ
    t = tones(ch, "B3", "B5")
    if n == "起動" or n in ("夜の町を回る",) or n.startswith("朝のプログラム") or n == "朝日" or n == "屋根づたい":
        seq = [t[q % len(t)] for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 6, 4, 3, 1)]
        if n.startswith("朝") or n == "朝日": seq = [x + 12 if x < 64 and x + 12 <= midi("B5") else x for x in seq]
        ARP.bar(b, " ".join(f"{nm(x)}:0.25" for x in seq))
    elif n == "2つ目の通り" and i >= 8:
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 2, 1, 3, 5, 3)))
    elif n == "東の空":
        tf = tones(ch, "B3", "B5")
        ARPF.bar(b, " ".join(f"{nm(tf[q % len(tf)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 6, 4, 3, 1)))
    # ピアノ
    if n == "起動" and i >= 4:
        stab(b, ch, "X:1.5 X:1 X:1.5"); PNL.bar(b, piano_left8(ch, "C2"))
    elif n in ("夜の町を回る", "2つ目の通り"):
        if n == "2つ目の通り" and i < 8: PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2")
        else:
            stab(b, ch, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i < 8 else "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75")
            PNL.bar(b, f"{nm(low(ch, 'C2'))}:1.5 {nm(low(ch, 'C2') + 12)}:1 {nm(low(ch, 'C2'))}:1.5")
    elif n.startswith("時計をセット") or n.startswith("朝のプログラム") or n == "朝日":
        PN.bar(b, piano_arp16(ch, "D#4", "D#6")); PNL.bar(b, piano_left8(ch, "C2"))
        if n.startswith("時計") and i == L - 1: PN.bar(b, f"{nm(v[2] + 12)}:2 R:2")
        for j in range(2):
            if n.startswith("朝") or n == "朝日": PNC[j].bar(b, f"{nm(voice(ch, 64, 2)[j])}:2 {nm(voice(ch, 64, 2)[j])}:2")
    elif n == "止まった時計":
        # 和音を左手と右手で（M7 の色を足す）
        vv = voice(ch, 64, 3)
        for j, tr_ in enumerate([PN] + PNC): tr_.bar(b, f"R:{0.5 * j} {nm(vv[j])}:{4 - 0.5 * j}")
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 7)}:2")
    elif n == "東の空":
        PNF.bar(b, piano_arp16(ch, "D#4", "D#6")); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
    elif n == "朝":
        if i < 6: stab(b, ch, "X:2 X:2"); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
        elif i == 6:
            vv = voice("Badd9", 66, 3)
            for j, tr_ in enumerate([PN] + PNC): tr_.bar(b, f"R:{0.25 * j} {nm(vv[j])}:{16 - 0.25 * j}")
            PNL.bar(b, "B1:16")
    # ベース（根音に沿わせる。サビは8分のオクターブ）
    if n == "起動": BASS.bar(b, bass_line(S, b, "root8") if i >= 4 else "R:4")
    elif n in ("夜の町を回る", "2つ目の通り"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("時計をセット"): BASS.bar(b, bass_line(S, b, "root8") if i < L - 1 else f"{nm(low(ch, 'E1'))}:2 R:2")
    elif n.startswith("朝のプログラム") or n == "朝日" or n == "時計台" or n == "屋根づたい": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "止まった時計": BASS.bar(b, bass_line(S, b, "half"))
    elif n == "東の空": BASS.bar(b, bass_line(S, b, "long" if i < 4 else "root8"))
    elif n == "朝" and i < 7: BASS.bar(b, bass_line(S, b, "half" if i < 6 else "long"))
    # ギター（パワーコード）。曲の頭や Aメロでは刻まない
    pw = power(ch, "E2")
    pat = None
    if (n == "起動" and i >= 8) or n == "屋根づたい": pat = "X:1.5! X:1 X:1.5!"
    elif n.startswith("朝のプログラム") or n == "朝日" or n == "時計台":
        pat = "X:0.5! X:0.5 X:0.5 X:0.5 X:0.5! X:0.5 X:0.5 X:0.5" if i % 8 < 6 else "X:1.5! X:1.5 X:1!"
        if n == "朝のプログラム2" and i < 8: pat = "X:2! X:2"
    elif n.startswith("時計をセット") and i >= 4: pat = "X:1! X:1 X:1! X:1" if i < L - 1 else "X:2! R:2"
    elif n == "朝" and i < 2: pat = "X:4!"
    if pat:
        for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))
    # パッド（ずっと薄く。夜明け前はパッドだけ）
    if n in ("止まった時計", "夜明け前", "東の空", "朝") or n.startswith("時計をセット") or (n in ("夜の町を回る", "2つ目の通り") and i >= 8):
        vv = voice(ch, 60, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4" if not (n == "朝" and i >= 6) else (f"{nm(voice('Badd9', 60, 3)[j])}:16" if i == 6 else ""))
    # 厚い和音（サビだけ）
    if n.startswith("朝のプログラム") or n == "朝日":
        vv = voice(ch, 66, 2)
        for j in range(2): SAW[j].bar(b, f"{nm(vv[j])}:1.5 {nm(vv[j])}:1 {nm(vv[j])}:1.5")

# 夜明け前: 時計の秒針（アルペジオの1音だけ、こもった写しで）
for i, b in enumerate(S.sc("夜明け前")): ARPF.bar(b, "F#4:0.5 R:0.5 F#4:0.5 R:0.5 F#4:0.5 R:0.5 C#5:0.5 R:0.5")
# 効果音
riser(FX, S.sc("朝のプログラム")[0], 4, "C4"); riser(FX, S.sc("朝日")[0], 16, "D4")
cym_swell(CYM, S.sc("朝のプログラム2")[0], 2, "C4"); cym_swell(CYM, S.sc("朝日")[0], 2, "C4"); cym_swell(CYM, S.sc("時計台")[0], 2, "C4")
# 朝の鳥（ピッコロの短いさえずり）
BIRDS = ["R:1 G6:0.125 A6:0.125 G6:0.125 R:0.625 E6:0.25 G6:0.5 R:1.25", "R:2.5 C7:0.125 A6:0.125 C7:0.125 A6:0.125 R:1",
         "R:0.5 E6:0.25 G6:0.25 R:1 G6:0.125 A6:0.125 G6:0.25 R:1.5", "R:3 A6:0.125 G6:0.125 E6:0.25 R:0.5"]
for i, b in enumerate(S.sc("朝")[4:]): BIRD.bar(b, BIRDS[i % 4])

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "起動":
        if i < 4: continue
        vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i == 4: crash(D, b)
        if i == 8: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n in ("夜の町を回る", "2つ目の通り"):
        if i < 8: vgroove(D, b, "beat8", ghosts=0.4, seed=b, h="x.x.x.x.x.x.x.x.")
        else:
            vgroove(D, b, "vrock2", ghosts=0.35, seed=b); D.H[b] = "." * 16
            RIDE.bar(b, " ".join(("D2:0.5!" if q % 2 == 0 else "D2:0.5") for q in range(8)))
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown")
    elif n.startswith("時計をセット"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n.startswith("朝のプログラム") or n == "朝日":
        name = "halfdrive" if (n == "朝のプログラム2" and i < 8) else "vrock"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if n == "朝日" and i == 22: put_fill(D, b, "tomdown")
        if n == "朝日" and i == 23: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2"); RIDE.bar(b, "G2:4")
        elif last: put_fill(D, b, "tomdown")
    elif n == "屋根づたい":
        vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if i == 3: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomtrip")
    elif n == "時計台":
        vgroove(D, b, "vrock" if i < 8 else "vrock2", ghosts=0.35, seed=b)
        if i >= 8:
            D.H[b] = "." * 16; RIDE.bar(b, " ".join(("D2:0.5!" if q % 2 == 0 else "D2:0.5") for q in range(8)))
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "G2")
        if i % 4 == 3 and not last: put_fill(D, b, "small" if i % 8 == 3 else "tomdown")
        if last: put_fill(D, b, "build")
    elif n == "止まった時計":
        if i < 4: continue
        vgroove(D, b, "half", ghosts=0.5, seed=b, h="................")
        RIDE.bar(b, "D2:1! D2:1 D2:1 D2:1")
        if i == 4: crash(D, b, "C2")
        if i == 11: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomtrip")
    elif n == "東の空":
        D.set(b, "X...X...X...X...", "." * 16 if i < 4 else "....x.......x...", "." * 16 if i < 6 else "x.x.x.x.x.x.x.x.")
        if i == 7: put_fill(D, b, "build")
    elif n == "朝":
        if i < 6:
            vgroove(D, b, "half", ghosts=0.2, seed=b)
            if i == 0: crash(D, b)
        elif i == 6: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)

# 1拍の完全な無音（時計台のソロの終わり）と、Bメロの最後の止め
SIL.add(S.sc("時計台")[-1], 3, 4)
for name in ("時計をセット", "時計をセット2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の20。J-POP（テクノ×バンド）。B 長調・170・転調なし。朝日が昇るまでに町じゅうの目覚まし時計をプログラムする小さなロボット。"
          "シンセのアルペジオで起動し、16分の「カチコチ」の Aメロ、F#5 の3連打のフックのサビ、2番はピアノが歌を受け取り、時計台のギターのソロ、"
          "1拍の無音から Half feel の止まった時計、夜明け前の暗い2小節、ローパスの写しで明るくなる東の空、最後のサビ、朝の鳥と Badd9 の和音。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
