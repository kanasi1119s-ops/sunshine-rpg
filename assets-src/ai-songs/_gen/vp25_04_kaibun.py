# vp25 04「回文」Palindrome（仮）— テクノポップ。B♭長調・124・4/4。主役の楽器: 鉄琴（グロッケンシュピール）
# 物語: 「たけやぶやけた」のような、前から読んでも後ろから読んでも同じ一日。朝に出かけた道を、夕方に逆の順で帰ってくる。
# 形: 前半 A→B→C→D、まん中で完全な無音、後半は D'→C'→B'→A'。後半は、旋律も和音もドラムも小節の順と音の順を逆にした「鏡」
# 場面と強さ: 左右対称の山。A（静か）→B→C→D（1つ目の山）／まん中＝完全な無音（2小節）／D'（2つ目の山）→C'→B'→A'（静か）
# 旋律の性格: 4音の動機（1・2・4・3）と、その逆行形（3・4・2・1）。後半はすべてが逆から聞こえる
# 崩す所: 後半は和音の進行も逆にする（V→I の解決が I→V になり、終わったようで終わらない）。シンバルは後半だけ逆再生の音
from vp25_lib import *

S = Song("04", "kaibun", "回文（仮）", "Palindrome", 124, 4, "Bb", "major", "テクノポップ")
K = S.key
CH = {"A": ["Bbmaj7", "Dm7", "Ebmaj7", "Ebm6"] * 3,
      "B": ["Gm7", "Cm7", "Ebmaj7", "F", "Gm7", "Cm7", "Abmaj7", "F"] * 2,
      "C": ["Ebmaj7", "F/Eb", "Dm7", "Gm7", "Cm7", "Dm7", "Ebmaj7", "F7sus4"] * 2,
      "D": ["Bb", "Dm7", "Ebmaj7", "Cm7", "Gm7", "F/A", "Bbmaj7", "Ebmaj7/F"] * 3}
LEN = {"A": 12, "B": 16, "C": 16, "D": 24}
KIND = {"A": "intro", "B": "verse", "C": "pre", "D": "chorus"}
for x in "ABCD": S.scene(x, LEN[x], KIND[x], CH[x])
S.scene("まん中", 2, "break", ["Ebmaj7/F", "Ebmaj7/F"])
for x in "DCBA": S.scene(x + "'", LEN[x], {"D": "chorus", "C": "bridge", "B": "verse", "A": "outro"}[x], list(reversed(CH[x])))

GL = S.track("主役: 鉄琴", "glockenspiel", patch="glockenspiel", volume=0.24, pan=0.15, reverb=0.35, sustain=1.6, gainDb=4)
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("chiff", vol=0.2, pan=-0.05, delay=0.75))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.21, duck=0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.5, 0.5, 0][i], duck=0.15)) for i in range(3)]
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=[-0.6, 0.6, 0][i], duck=0.35, sustain=1.0)) for i in range(3)]
ARP = S.track("ガラスのアルペジオ", "pad", **pluck_spec("glassPluck", vol=0.08, pan=-0.4, delay=0.75, sustain=0.9))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 前半の材料（小節ごと）。後半はこれを鏡にする ----------
MOT = "1:0.5 2:0.5 4:0.5 3:0.5"          # 動機（1・2・4・3）
MEL = {}
MEL["A"] = ["R:4"] * 4 + ["R:2 1':0.5 2':0.5 4':0.5 3':0.5", "2':4", "R:2 6:0.5 7:0.5 2':0.5 1':0.5", "1':4",
                         "R:2 1':0.5 2':0.5 4':0.5 3':0.5", "5':3 4':1", "3':2 2':1 1':1", "1':4"]
MEL["B"] = ["5,:0.5 6,:0.5 1:0.5 7,:0.5 6,:1 R:1", "4,:0.5 5,:0.5 b7,:0.5 6,:0.5 5,:1 R:1", "3,:0.5 4,:0.5 6,:0.5 5,:0.5 5,:1 6,:0.5 7,:0.5", "1:3 R:1",
            "5,:0.5 6,:0.5 1:0.5 7,:0.5 2:1 1:1", "6,:0.5 7,:0.5 2:0.5 1:0.5 6,:1 R:1", "1:0.5 2:0.5 4:0.5 3:0.5 b7,:1 1:1", "2:3 R:1",
            "5:0.5 6:0.5 1':0.5 7:0.5 6:1 5:1", "4:0.5 5:0.5 b7:0.5 6:0.5 5:1 4:1", "3:0.5 4:0.5 6:0.5 5:0.5 5:2", "4:2 3:1 2:1",
            "1:0.5 2:0.5 4:0.5 3:0.5 2:1 1:1", "6,:0.5 7,:0.5 2:0.5 1:0.5 6,:2", "b7,:0.5 1:0.5 3:0.5 2:0.5 1:1 b7,:1", "1:2 R:2"]
MEL["C"] = ["5:2 4:1 3:1", "4:2 5:2", "6:3 5:1", "5:2 4:1 2:1", "3:2 2:1 1:1", "2:2 3:2", "5:3 6:1", "5:4",
            "1':2 7:1 6:1", "7:2 1':2", "2':3 1':1", "7:2 6:1 5:1", "6:2 5:1 4:1", "5:2 6:2", "7:2 1':1 2':1", "1':4"]
HOOKD = ["1':0.5 2':0.5 4':0.5 3':0.5 2':1 1':1", "6:0.5 7:0.5 2':0.5 1':0.5 6:2", "5:0.5 6:0.5 1':0.5 7:0.5 6:1 5:1", "4:2 5:1 6:1",
         "2':0.5 3':0.5 5':0.5 4':0.5 3':1 2':1", "1':0.5 2':0.5 3':0.5 2':0.5 1':2", "1':0.5 2':0.5 4':0.5 3':0.5 2':1 3':1", "4':3 R:1"]
MEL["D"] = HOOKD + [seq_up(x, K, 0) for x in HOOKD[:4]] + ["5':0.5 6':0.5 1'':0.5 7':0.5 6':1 5':1", "4':0.5 5':0.5 6':0.5 5':0.5 4':2",
                                                         "3':0.5 4':0.5 6':0.5 5':0.5 4':1 3':1", "4':3 R:1"] + HOOKD


def mirror_bar(s):
    """1小節の音を逆の順に（音の長さもそのまま逆）"""
    return " ".join(reversed(s.split()))


for x in "ABCD":
    for i, b in enumerate(S.sc(x)): LEAD.bar(b, K.mel(MEL[x][i], oct=4))
    for i, b in enumerate(S.sc(x + "'")): LEAD.bar(b, K.mel(mirror_bar(MEL[x][LEN[x] - 1 - i]), oct=4))

# 鉄琴: A は動機の点描、C はリードの後ろで動機、D は歌の頭の4音を重ねる（1オクターブ上）
GLM = {"A": [MOT + " R:2", "R:4", "R:2 " + MOT, "R:4"] * 3, "B": ["R:4"] * 16,
       "C": ["R:2 " + MOT, "R:4", "R:2 " + seq_up(MOT, K, 1), "R:4", "R:2 " + seq_up(MOT, K, 2), "R:4", "R:2 " + seq_up(MOT, K, 3), "R:4"] * 2,
       "D": [" ".join(h.split()[:4]) + " R:2" if "R:" not in h.split()[0] else "R:4" for h in MEL["D"]]}
GLM["B"] = ["R:4"] * 8 + ["R:2 " + MOT, "R:4", "R:2 " + seq_up(MOT, K, -1), "R:4", "R:2 " + MOT, "R:4", "R:2 " + seq_up(MOT, K, 1), "R:4"]
for x in "ABCD":
    o = 5 if x == "D" else 6
    for i, b in enumerate(S.sc(x)): GL.bar(b, K.mel(GLM[x][i], oct=o))
    for i, b in enumerate(S.sc(x + "'")): GL.bar(b, K.mel(mirror_bar(GLM[x][LEN[x] - 1 - i]), oct=o))
# まん中の2小節目の最後に鉄琴の1音（鏡の折り目）だけ…は置かない（完全な無音）

# ---------- ベース・和音・アルペジオ（前半を作ってから鏡） ----------
BASSM, PADM, SAWM, ARPM = {}, {}, {}, {}
for x in "ABCD":
    bs, ps, ss, ar = [], [], [], []
    for i, b in enumerate(S.sc(x)):
        ch = S.chords[b]; r = nm(low(ch))
        r8 = nm(low(ch) + 12); f5 = nm(low(ch) + 7)
        if x == "A": bs.append("R:4" if i < 8 else f"{r}:4")
        elif x == "B": bs.append(f"{r}:1.5 {r}:0.5 R:1 {f5}:0.5 {r}:0.5")
        elif x == "C": bs.append(f"{r}:0.5 {r}:0.5 {r8}:0.5 {r}:0.5 R:0.5 {r}:0.5 {r8}:0.5 {f5}:0.5")
        else: bs.append(" ".join(f"{r if j % 2 == 0 else r8}:0.5" for j in range(8)))
        v = voice(ch, 58, 3)
        ps.append([f"{nm(m)}:4" for m in v] if x in ("A", "B", "C") else ["R:4"] * 3)
        sv = voice(ch, 65, 3)
        ss.append([f"{nm(m)}:1.5 {nm(m)}:1 {nm(m)}:1.5" for m in sv] if x == "D" else ["R:4"] * 3)
        t = tones(ch, "F4", "F6")
        ar.append(" ".join(f"{nm(t[k % len(t)])}:0.25" for k in [0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 5, 4, 2, 3, 1, 2]) if x in ("C", "D") and not (x == "C" and i < 8) else "R:4")
    BASSM[x], PADM[x], SAWM[x], ARPM[x] = bs, ps, ss, ar
for x in "ABCD":
    for i, b in enumerate(S.sc(x)):
        BASS.bar(b, BASSM[x][i]); ARP.bar(b, ARPM[x][i])
        for j in range(3): PAD[j].bar(b, PADM[x][i][j]); SAW[j].bar(b, SAWM[x][i][j])
    for i, b in enumerate(S.sc(x + "'")):
        k = LEN[x] - 1 - i
        BASS.bar(b, mirror_bar(BASSM[x][k])); ARP.bar(b, mirror_bar(ARPM[x][k]))
        for j in range(3): PAD[j].bar(b, mirror_bar(PADM[x][k][j])); SAW[j].bar(b, mirror_bar(SAWM[x][k][j]))

# ---------- ドラム（前半を作り、後半はグリッドを左右反転。クラッシュは逆再生のシンバルに） ----------
for x in "ABCD":
    for i, b in enumerate(S.sc(x)):
        last = i == LEN[x] - 1
        if x == "A":
            if i >= 8: D.set(b, h="x...x...x...x...")
            continue
        if x == "B":
            put_groove(D, b, "half", ghosts=0.3, seed=b, hat_vary=False); D.H[b] = "x.x.x.x.x.x.x.x."
            if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
            if i == 0: crash(D, b, "D2")
        elif x == "C":
            put_groove(D, b, "pop8", ghosts=0.4, seed=b, hat_vary=False)
            if i == 0: crash(D, b)
            if i % 8 == 7: put_fill(D, b, "tomdown" if last else "small")
        else:
            put_groove(D, b, "four", ghosts=0.3, seed=b, hat_vary=False); D.H[b] = "x.O.x.O.x.O.x.O."
            if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
            if i % 8 == 7: put_fill(D, b, "snare16" if i != 23 else "build")
MIR = {}
for x in "ABCD":
    for i, b in enumerate(S.sc(x + "'")):
        src = S.sc(x)[LEN[x] - 1 - i]; MIR[src] = b
        D.set(b, D.K[src][::-1], D.S[src][::-1], D.H[src][::-1])
# タムのフィルも鏡に（小節の終わりのフィルは、鏡の小節の頭に来る）
for t0, L, x_ in list(D.T.ev):
    src = int(t0 // 4)
    if src in MIR:
        off = 4 - ((t0 - src * 4) + L)
        D.T.ev.append((MIR[src] * 4 + off, L, x_))
# 鏡のシンバル: 前半のクラッシュ（区間の頭）は、後半では「区間の終わりに向かってふくらむ逆再生」になる
for x in "BCD":
    for i, b in enumerate(S.sc(x)):
        if i == 0 or (x == "D" and i % 8 == 0):
            mb = S.sc(x + "'")[LEN[x] - 1 - i] + 1          # 鏡の位置の小節の終わり
            cym_swell(CYM, mb, 2, "C4")

S.flags += " --space hall --space-wet 0.14"
S.desc = ("仮: ボカロ曲のインスト25曲の04。テクノポップ。B♭長調・124。主役の楽器は鉄琴。前から読んでも後ろから読んでも同じ一日。"
          "A→B→C→D、まん中に2小節の完全な無音、後半は D'→C'→B'→A' と、旋律・和音・ベース・ドラムの小節の順と音の順をすべて逆にした鏡。"
          "動機は 1・2・4・3 と、その逆行形。後半のシンバルは逆再生の音で、区間の終わりに向かってふくらむ。自作")
S.write()
