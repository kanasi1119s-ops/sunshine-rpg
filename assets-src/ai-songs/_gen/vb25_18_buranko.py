# vb25 18「ブランコ・リバース」Swing Reverse（仮）— J-POP（3拍子）。A♭長調・144・3/4（Bメロは 6/8 のノリ）。最後のサビは +1（A長調）
# 物語: 夕方の公園。ブランコを思いきりこぐと、ひと振りごとに時間が巻きもどって、子どものころの自分に会える。
#   いちばん高く上がった所で手が届きそうになり、ふっと止まる。思い出の中を歩いて、もう一度こいで、今の自分に戻ってくる。
# 場面と強さ: オルゴール（グロッケンだけ・小）→ 夕方の公園（アコーディオンのワルツ）→ こぎ始め（Aメロ・語る）
#   → 勢いをつける（6/8 の Bメロ・溜め・止め）→ 空へ（サビ・強）→ 風の中（アコーディオンのソロ）→ もう一度こぐ（Aメロ。前半はピアノが歌う）
#   → 勢いをつける2 → いちばん高く（サビ）→ 風を切る（短い合いの手）→ 止まったブランコ（静けさ・1拍の無音）
#   → 子どものころ（Cメロ）→ もっと高く（+1・最大）→ 着地（ブランコのきしみと1音）
# 旋律の性格: ワルツの揺れ。Aメロは低め（C4〜F5）の16分、サビは大きな上下の跳躍（6度・7度）と、いちばん高い所の3連打
# 派手な展開: Bメロ 6/8・最後のサビ +1・1拍の完全な無音・止め2回（Bメロの終わり）・サビ後半の和音のテンポの倍化（2小節に1つ → 1小節に1つ）
# 定番以外のコード: Caug（増三和音）→ Fm7・Ebm7–Ab7（IV への副属和音）・C7（vi への副属和音）・D♭m6（同主短調の iv）・Ddim7・E7（新しい調の V7 で +1 へ）
from vb25_lib import *

S = Song("18", "buranko", "ブランコ・リバース（仮）", "Swing Reverse", 144, 3, "Ab", "major", "J-POP（3拍子・ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"tone": "rock"})
K = S.key                    # A♭長調
KA = Key("A", "major")       # 最後のサビ（+1）
dbl = lambda xs: [x for c in xs for x in (c, c)]

A_CH = dbl(["Abmaj7", "Cm7", "Dbmaj7", "Eb7sus4"])
B_CH = ["Fm7", "Ebm7", "Ab7", "Dbmaj7", "Bbm7", "C7", "Fm7", "Eb7"]
CH = dbl(["Dbmaj7", "Eb", "Cm7", "Fm7"]) + ["Bbm7", "Eb7", "Ab", "Caug", "Fm7", "Dbm6", "Ab/Eb", "Eb7"]
STOP = dbl(["Dbmaj7", "Cm7", "Bbm7", "Ab/C", "Dbmaj7", "Ddim7", "Eb7sus4", "Eb7"])
CHILD = dbl(["Fm", "Fm/Eb", "Dbmaj7", "C7", "Bbm7", "Eb7", "Abmaj7", "E7"])
LAST = [tr_chord(c, 1) for c in CH] + [tr_chord(c, 1) for c in CH[:-1]] + ["A"]

S.scene("オルゴール", 8, "intro", CH[:8])
S.scene("夕方の公園", 8, "interlude", A_CH)
S.scene("こぎ始め", 16, "verse", A_CH)
S.scene("勢いをつける", 8, "pre", B_CH)
S.scene("空へ", 16, "chorus", CH)
S.scene("風の中", 16, "solo", A_CH)
S.scene("もう一度こぐ", 16, "verse", A_CH)
S.scene("勢いをつける2", 8, "pre", B_CH)
S.scene("いちばん高く", 16, "chorus", CH)
S.scene("風を切る", 8, "interlude", ["Dbmaj7", "Eb", "Fm7", "Ab/Eb", "Dbmaj7", "Eb", "Ab", "Ab"])
S.scene("止まったブランコ", 16, "break", STOP)
S.scene("子どものころ", 16, "bridge", CHILD)
S.scene("もっと高く", 32, "chorus", LAST)
S.scene("着地", 12, "outro", ["Dmaj7", "E", "C#m7", "F#m7", "Dmaj7", "E", "A", "A", "A", "A", "A", "A"])

V = Voice(S, vol=0.22, delay=1.0, patch="popLeadClear")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
ACS = dict(volume=0.12, pan=-0.3, reverb=0.28, phrase=6, fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2000, "high": 0.5}])
AC = S.track("アコーディオン（旋律）", "accordion", **ACS)
AC2 = [S.track(f"アコーディオン（和音{i + 1}）", "accordion", **ACS) for i in range(2)]
PNS = piano_spec(0.12, 0.25)
PN = S.track("ピアノ（右手）", "piano", **PNS)
PNL = S.track("ピアノ（左手）", "piano", **PNS)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", **PNS)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", **strings_spec(0.08, 0.5)) for i in range(3)]
MB = S.track("オルゴール風のグロッケン", "glockenspiel", patch="glockenspiel", volume=0.1, pan=0.1, reverb=0.4)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.2))
CREAK = S.track("ブランコのきしみ（弦をこする音）", "guitar", patch="guitarFx", volume=0.06, pan=-0.2, reverb=0.3, modulate=False)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役（3拍＝1小節） =================
VA = ["R:0.25 3,:0.25 5,:0.25 1:0.25 3:0.5 2:0.25 1:0.25 7,:0.25 1:0.25 3:0.5",
      "2:0.25 1:0.25 7,:0.25 5,:0.25 R:0.25 5,:0.25 7,:0.25 1:0.25 3:1",
      "R:0.25 3:0.25 3:0.25 3:0.25 5:0.25 3:0.25 2:0.25 1:0.25 7,:0.5 3:0.5",
      "5:0.25 4:0.25 3:0.25 2:0.25 3:0.5 5,:0.5 7,:1",
      "R:0.25 4,:0.25 6,:0.25 1:0.25 4:0.5 3:0.25 1:0.25 6,:0.25 1:0.25 3:0.5",
      "4:0.25 3:0.25 1:0.25 6,:0.25 R:0.25 6,:0.25 1:0.25 4:0.25 6:1",
      "5:0.25 4:0.25 2:0.25 1:0.25 R:0.25 1:0.25 2:0.25 4:0.25 5:0.5 4:0.5",
      "2:0.5 1:0.25 7,:0.25 5,:1.5 R:0.5",
      "R:0.25 5,:0.25 1:0.25 5:0.25 R:0.25 5:0.25 4:0.25 3:0.25 1:0.5 5:0.5",
      "1':0.25 7:0.25 5:0.25 3:0.25 R:0.25 3:0.25 5:0.25 7:0.25 1':1",
      "R:0.25 7:0.25 7:0.25 5:0.25 3:0.25 5:0.25 7:0.25 5:0.25 3:0.5 2:0.5",
      "3:0.25 2:0.25 1:0.25 7,:0.25 R:0.5 7,:0.25 1:0.25 3:1",
      "R:0.25 1:0.25 1:0.25 1:0.25 4:0.25 1:0.25 6,:0.25 4,:0.25 6,:0.5 1:0.5",
      "4:0.333 5:0.333 6:0.334 1':0.333 6:0.333 4:0.334 3:1",
      "4:0.25 4:0.25 2:0.25 5,:0.25 R:0.25 1:0.25 2:0.25 4:0.25 5:1",
      "4:0.5 2:0.5 5:1 R:1"]
# 2番の後半: 16分の3連のゆらぎと、オクターブ上へのつなぎ
VA2 = ["R:0.25 5,:0.25 1:0.25 3:0.25 5:0.25 1':0.25 5:0.25 3:0.25 1:0.5 5:0.5",
       "1':0.25 2':0.25 1':0.25 7:0.25 5:0.25 3:0.25 R:0.25 3:0.25 5:0.25 7:0.25 1':0.5",
       VA[10], VA[11],
       "R:0.25 1:0.25 4:0.25 6:0.25 1':0.25 6:0.25 4:0.25 1:0.25 6,:0.5 1:0.5",
       "4:0.333 6:0.333 1':0.334 3':0.333 1':0.333 6:0.334 4:1",
       VA[14], VA[15]]
# 6/8 のノリの Bメロ（付点4分＝1.5拍で2つに割る）
VB = ["1:0.5 3:0.5 6:0.5 5:1.5", "5:0.5 b7:0.5 2':0.5 4:1.5", "3:0.5 5:0.5 b7:0.5 1':1.5", "6:1.5 4:0.5 3:0.5 1:0.5",
      "2:0.5 4:0.5 6:0.5 1':1.5", "7:0.5 #5:0.5 3:0.5 2':1.5", "1':1.5 7:0.5 6:0.5 5:0.5", "5:1 R:2"]
VB2 = ["1:0.5 3:0.5 6:0.5 5:1 6:0.5", "5:0.5 b7:0.5 2':0.5 4:1 5:0.5", VB[2], "6:1.5 4:0.5 3:0.5 4:0.5",
       "2:0.5 4:0.5 6:0.5 1':1 2':0.5", VB[5], "1':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5", "5:1 R:2"]
# サビ: いちばん高い所の3連打と、大きな跳躍（6度・7度）
VC = ["R:0.5 1':0.5 1':0.5 1':0.5 3':1", "1':1 6:1 4:1", "R:0.5 2':0.5 2':0.5 2':0.5 5:1", "7:1.5 5:0.5 2':1",
      "R:0.5 3':0.5 3':0.5 3':0.5 7:1", "5:1 3:1 2':1", "1':1.5 7:0.5 6:1", "3:2 R:1",
      "4:0.5 6:0.5 1':0.5 2':0.5 1':0.5 6:0.5", "5:0.5 7:0.5 2':0.5 4':1.5", "3':1.5 1':0.5 5:1", "3:0.5 #5:0.5 1':0.5 3':1.5",
      "1':1 6:0.5 5:0.5 3:1", "b6:1 4:0.5 2:0.5 1:1", "5:0.5 1':0.5 3':0.5 1':0.5 5:1", "2:1 5:1 7:1"]
VC2 = ["R:0.25 5:0.25 1':0.5 1':0.5 1':0.5 3':1", "2':0.5 1':0.5 6:1 4:1"] + VC[2:15] + ["7:1 2':1 R:1"]
VCL = VC + VC[:12] + ["3':1 2':1 1':1", "b6:1 2':1 1':1", "5:0.5 1':0.5 3':0.5 4':0.5 3':1", "1':3"]
VWIND = ["R:0.5 1':0.5 1':0.5 3':1.5", "2':1 7:1 5:1", "R:0.5 1':0.5 1':0.5 6:1.5", "5:1.5 3:1.5",
         "R:0.5 1':0.5 1':0.5 3':1.5", "2':1 7:1 2':1", "1':3", "R:3"]
VSTOP = ["5:3", "4:2 3:1", "7,:3", "R:3", "6:2 1':1", "4:3", "3:1.5 2:1.5", "1:3",
         "6:2 5:1", "4:3", "#4:1.5 6:1.5", "1':3", "1':2 5:1", "4:3", "5:2 7:1", "2':2 R:1"]
VK = ["6,:0.5 1:0.5 3:0.5 6:0.5 1':1", "7:1 6:1 3:1", "5:0.5 6:0.5 1':0.5 3':0.5 2':1", "1':1.5 6:1.5",
      "4:0.5 6:0.5 1':0.5 3':0.5 1':1", "6:3", "3:0.5 #5:0.5 7:0.5 2':0.5 3':1", "2':1.5 7:1.5",
      "2:0.5 4:0.5 6:0.5 1':0.5 2':1", "1':1 6:1 4:1", "5:0.5 7:0.5 2':0.5 4':0.5 2':1", "7:3",
      "1':0.5 3':0.5 5:0.5 1':0.5 3':1", "2':1.5 1':1.5", "#5:1 1':1 #2':1", "#2':1 R:2"]

for i, b in enumerate(S.sc("こぎ始め")): V.bar(b, K.mel(VA[i], oct=4))
for i, b in enumerate(S.sc("もう一度こぐ")):
    if i < 8: PNM.bar(b, K.mel(VA[i], oct=5))             # 前半はピアノが歌を受け取る（1オクターブ上）
    else: V.bar(b, K.mel(VA2[i - 8], oct=4))
for i, b in enumerate(S.sc("勢いをつける")): V.bar(b, K.mel(VB[i], oct=4))
for i, b in enumerate(S.sc("勢いをつける2")): V.bar(b, K.mel(VB2[i], oct=4))
for i, b in enumerate(S.sc("空へ")): V.bar(b, K.mel(VC[i], oct=4))
for i, b in enumerate(S.sc("いちばん高く")): V.bar(b, K.mel(VC2[i], oct=4))
for i, b in enumerate(S.sc("風を切る")): V.bar(b, K.mel(VWIND[i], oct=4))
for i, b in enumerate(S.sc("止まったブランコ")): V.bar(b, K.mel(VSTOP[i], oct=4), low=False)
for i, b in enumerate(S.sc("子どものころ")): V.bar(b, K.mel(VK[i], oct=4))
for i, b in enumerate(S.sc("もっと高く")): V.bar(b, KA.mel(VCL[i], oct=4))
VOUT = ["3':1.5 2':1.5", "1':3", "7:1.5 5:1.5", "6:3", "4:1 6:1 1':1", "2':3", "1':3", "R:3"]
for i, b in enumerate(S.sc("着地")):
    if i < 8: V.bar(b, KA.mel(VOUT[i], oct=4), low=(i < 4))

# ================= オルゴール（グロッケン） =================
for i, b in enumerate(S.sc("オルゴール")): MB.bar(b, K.mel(VC[i], oct=5))
for i, b in enumerate(S.sc("止まったブランコ")):
    if i % 4 == 0: MB.bar(b, K.mel(["5:1 1':1 3':1", "4:1 1':1 4':1", "3:1 5:1 1':1", "6:1 1':1 4':1"][i // 4], oct=5))
MB.bar(S.sc("着地")[9], KA.mel("1':3", oct=5))                # 最後の1音

# ================= アコーディオン（ワルツの和音・風の中のソロ） =================
SOLO = ["5:0.5 3:0.5 1:0.5 3:0.5 5:1", "1':1.5 7:0.5 5:1", "7:0.5 5:0.5 3:0.5 5:0.5 7:1", "2':1.5 1':0.5 7:1",
        "6:0.5 4:0.5 1:0.5 4:0.5 6:1", "1':1 3':1 1':1", "2':0.5 1':0.5 7:0.5 5:0.5 4:1", "5:3",
        "5:0.25 6:0.25 5:0.25 3:0.25 1:0.5 3:0.5 5:1", "1':0.5 2':0.5 1':0.5 7:0.5 5:1", "7:0.25 1':0.25 7:0.25 5:0.25 3:0.5 5:0.5 7:1",
        "3':1.5 2':0.5 1':1", "6:0.25 1':0.25 6:0.25 4:0.25 1:0.5 4:0.5 6:1", "3':1 2':1 1':1", "2':0.5 1':0.5 7:0.5 5:0.5 2':1", "1':1.5 R:1.5"]
for i, b in enumerate(S.sc("風の中")): AC.bar(b, K.mel(SOLO[i], oct=4))
for i, b in enumerate(S.sc("夕方の公園")): AC.bar(b, K.mel(SOLO[i], oct=4) if i < 7 else K.mel("5:1.5 R:1.5", oct=4))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 62, 2)
    if n in ("夕方の公園", "こぎ始め", "風の中", "もう一度こぐ", "子どものころ", "着地") or (n in ("空へ", "いちばん高く", "もっと高く") and i >= 8):
        if n == "着地" and i >= 8: continue
        for j in range(2): AC2[j].bar(b, f"R:1 {nm(v[j])}:1 {nm(v[j])}:1")
    elif n.startswith("勢いを"):
        for j in range(2): AC2[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 {nm(v[j])}:0.5" if i < 7 else f"{nm(v[j])}:1 R:2")

# ================= ピアノ（サビは8分の分散、Aメロは左手の低音） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; t = tones(ch, "Ab3", "Ab5"); r = low(ch, "C2")
    if n in ("空へ", "いちばん高く", "もっと高く", "子どものころ", "風を切る"):
        PN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 2, 1)))
        PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:1.5")
    elif n in ("こぎ始め", "勢いをつける", "勢いをつける2") or (n == "もう一度こぐ" and i >= 8):
        PNL.bar(b, f"{nm(r)}:3")
        if n.startswith("勢いを"): PN.bar(b, f"{nm(t[1 % len(t)])}:1.5 {nm(t[3 % len(t)])}:1.5" if i < 7 else f"{nm(t[1])}:1 R:2")
    elif n == "止まったブランコ":
        if i % 2 == 0: PNL.bar(b, f"{nm(r)}:6")
    elif n == "着地" and i < 8:
        PN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 2, 1)) if i < 4 else f"{nm(t[2])}:3")
        PNL.bar(b, f"{nm(r)}:3")

# ================= ストリングス =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("空へ", "いちばん高く", "もっと高く", "子どものころ", "止まったブランコ", "風の中") or (n == "着地" and i < 8):
        if n == "止まったブランコ" and i < 8: continue
        v = voice(S.chords[b], 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:3")

# ================= ベース（ワルツ: 1拍目、サビは 1拍目と3拍目） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("オルゴール",): continue
    if n == "止まったブランコ":
        if i % 2 == 0: BASS.bar(b, f"{nm(r)}:6")
    elif n.startswith("勢いを"):
        BASS.bar(b, f"{nm(r)}:1.5! {nm(r + 7)}:1.5" if i < 7 else f"{nm(r)}:1! R:2")     # 6/8: 付点4分で2つ
    elif n in ("空へ", "いちばん高く", "もっと高く", "風を切る", "子どものころ"):
        nx = low(S.chords[b + 1], "E1") if b + 1 < S.nb else r
        BASS.bar(b, f"{nm(r)}:1! {nm(r + 12)}:1 {nm(r + 7)}:0.5 {nm(nx - 1 if nx > r else nx + 1)}:0.5")
    elif n == "着地":
        if i < 8: BASS.bar(b, f"{nm(r)}:1! R:1 {nm(r + 7)}:1")
        elif i == 8: BASS.bar(b, f"{nm(r)}:6")
    else:
        BASS.bar(b, f"{nm(r)}:1! R:1 {nm(r + 7)}:1" if i % 2 == 0 else f"{nm(r)}:2 {nm(r + 12)}:1")

# ブランコのきしみ（弦をこする長い音・短い音）
for i, b in enumerate(S.sc("オルゴール")):
    if i % 4 == 3: CREAK.bar(b, "R:1.5 E2:1.5")
for i, b in enumerate(S.sc("止まったブランコ")):
    if i in (0, 6, 12): CREAK.bar(b, "F2:1 R:2")
for i, b in enumerate(S.sc("着地")):
    if i in (8, 10): CREAK.bar(b, "E2:3" if i == 8 else "F2:1.5 R:1.5")

# 効果音
riser(FX, S.sc("空へ")[0], 3, "C4"); riser(FX, S.sc("いちばん高く")[0], 3, "C4"); riser(FX, S.sc("もっと高く")[0], 6, "D4")
cym_swell(CYM, S.sc("風の中")[0], 3, "C4"); cym_swell(CYM, S.sc("子どものころ")[0], 3, "E4")

# ================= ドラム（3拍子: 12文字のグリッド） =================
def tomfill3(b):
    D.S[b] = D.S[b][:6] + "......"; D.H[b] = D.H[b][:6] + "......"; D.K[b] = D.K[b][:6] + "X.....X..."[:6]
    D.tom(b, "R:1.5 C4:0.25 A3:0.25 F3:0.25 D3:0.25 A2:0.5!")


def roll3(b):
    D.S[b] = "....x.xxXXXX"; D.H[b] = "x.x........."


W = {"waltz": ("X...........", "....x...x...", "x.x.x.x.x.x."),
     "waltz2": ("X.......x...", "....X...X...", "x.x.x.x.x.x."),
     "waltzP": ("X...x.......", "....X...Xo..", "XxxxXxxxXxxx"),
     "six8": ("X.....X.....", "......X.....", "X.x.x.X.x.x."),
     "six8b": ("X.x...X.....", "......X...o.", "X.x.x.X.x.x."),
     "halfw": ("X...........", "........X...", "x...x...x...")}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "オルゴール": continue
    if n == "夕方の公園":
        put_groove(D, b, W["waltz"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "G2", 3)
        if last: roll3(b)
    elif n in ("こぎ始め", "もう一度こぐ"):
        put_groove(D, b, W["waltz"] if i < 8 else W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        if n == "もう一度こぐ" and i < 8: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12      # ライド
        if i == 0: crash(D, b, "C2", 3)
        if i == 7: tomfill3(b)
        if last: roll3(b)
    elif n.startswith("勢いを"):
        put_groove(D, b, W["six8"] if i % 2 == 0 else W["six8b"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "B2", 3)
        if i == 6: roll3(b)
        if last: halt(D, b, 1, 3, 12)
    elif n in ("空へ", "いちばん高く", "もっと高く"):
        put_groove(D, b, W["waltzP"] if i >= 8 else W["waltz2"], ghosts=0.35, seed=b, hat_vary=False)
        if n == "もっと高く" and 16 <= i < 24: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12
        if i % 8 == 0 and not (n == "もっと高く" and i == 16): crash(D, b, "C2" if i % 16 == 0 else "G2", 3)
        if i % 8 == 7 and not last: tomfill3(b)
        if last and n != "もっと高く": roll3(b)
    elif n == "風の中":
        put_groove(D, b, W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1"); D.H[b] = "." * 12
        if i % 8 == 7: tomfill3(b)
    elif n == "風を切る":
        put_groove(D, b, W["waltzP"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "G2", 3)
        if i == 6: roll3(b)
        if last: D.set(b, "X...........", "X...........", "." * 12); crash(D, b, "C2", 6)
    elif n == "止まったブランコ":
        if i >= 8: put_groove(D, b, W["halfw"], ghosts=0.2, seed=b, hat_vary=False)
    elif n == "子どものころ":
        put_groove(D, b, W["halfw"] if i < 8 else W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        if i == 8: crash(D, b, "G2", 3)
        if i >= 8: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12
        if i == 14: roll3(b)
        if last: halt(D, b, 1, 3, 12)
    elif n == "着地":
        if i < 8: put_groove(D, b, W["waltz"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "C2", 3)
        if i == 7: D.set(b, "X...........", "X...........", "." * 12); crash(D, b, "C2", 6)

# 止め: 勢いをつけるの最後（1拍だけ）・子どものころの最後（1拍だけ）。1拍の完全な無音: 止まったブランコの最後の拍
for name in ("勢いをつける", "勢いをつける2", "子どものころ"): SIL.add(S.sc(name)[-1], 1, 3)
SIL.add(S.sc("止まったブランコ")[-1], 2, 3)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の18。J-POP（3拍子）。A♭長調・144・3/4（Bメロは 6/8 のノリ）・最後のサビ +1（A）。"
          "公園のブランコを思いきりこぐと、子どものころに戻れる。オルゴール風のグロッケンで始まり、アコーディオンのワルツ、16分の Aメロ、"
          "6/8 のノリで勢いをつける Bメロと止め、大きな跳躍のサビ、アコーディオンのソロ、止まったブランコ（1拍の無音）、子どものころの Cメロ、"
          "+1 のいちばん高いサビ、最後はブランコのきしみと1音。歌の役は声のように聞こえるシンセ。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, S.nb - 6, "夕方の蝉", S.beats * 6, vol=0.07)
vwrite(S)
