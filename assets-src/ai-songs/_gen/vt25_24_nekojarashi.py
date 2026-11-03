# vt25 24「ねこじゃらしロンド」Foxtail Rondo（仮）— アコースティック・ポップ。112・4/4。G 長調 → 最後の主題は +1（A♭）。
# 物語: 日曜日の午後、日だまりの窓辺で丸くなる猫。わたしはしのび足で、ねこじゃらしを鼻の先でゆらす。耳がぴくり。
#   飛びついた瞬間、するりと逃げた。何度でもくり返そう、同じ遊びを毎日でも。お昼寝した猫は、夢の中でも遊んでる。しっぽがゆれてる。
#   「ねこじゃらし、ゆらゆらり」── 何度も帰ってくる主題（ロンド）。また明日、日だまりで。
# 形（ロンド）: イントロ → 主題1 → 第1の話（Aメロ）→ 主題2 → 第2の話（Aメロ2・Bメロ）→ 主題3（2回・全員）→ 間奏（ベルとギター）
#   → 第3の話（お昼寝・静か）→ 転調 → 主題4（A♭・2回・いちばん強い）→ 終わり（ベルの答えだけが残る）
# 旋律の性格: 主題は「1' 1' 3' 1' 5」と、ねこじゃらしがゆれるように上下する5音の句。話（Aメロ）は8分で語る。
# ほかの曲とちがう所: 歌の句が終わるたびに、ベル（グロッケン）が2つの音で「答える」。同じ主題が何度も帰ってくる（ロンド）。
from vt25_lib import *

S = Song("24", "nekojarashi", "ねこじゃらしロンド（仮）", "Foxtail Rondo", 112, 4, "G", "major", "アコースティック・ポップ（ボカロ）")
S.kit = "jpop"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.16"
K = Key("G", "major")           # oct 3（1 = G3。歌うのは A3〜E5。1 より下と 7' は使わない）
KL = Key("Ab", "major")         # 主題4（oct 3）

R_CH = ["G", "C", "D", "Em", "C", "D", "G", "G"]
E_CH = ["C", "G/B", "Am", "D", "C", "G/B", "Am7", "D"]
B_CH = ["Am7", "Bm7", "C", "D", "Am7", "Bm7", "Cmaj7", "D7"]
X_CH = ["Em", "Bm", "C", "D"]
up = lambda cs: [tr_chord(c, 1) for c in cs]

S.scene("イントロ", 4, "intro", ["G", "C", "D", "G"])
S.scene("主題1", 8, "chorus", R_CH)
S.scene("第1の話", 16, "verse", E_CH * 2)
S.scene("主題2", 8, "chorus", R_CH)
S.scene("第2の話", 8, "verse", E_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("主題3", 16, "chorus", R_CH * 2)
S.scene("間奏", 8, "break", R_CH)
S.scene("第3の話", 12, "bridge", X_CH * 3)
S.scene("転調", 1, "break", ["Eb7"])
S.scene("主題4", 16, "chorus", up(R_CH) * 2)
S.scene("終わり", 12, "outro", ["Db", "Eb", "Ab", "Fm", "Db", "Eb", "Ab", "Ab", "Db", "Eb", "Ab", "Ab"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
GT = [S.track(f"アコースティックギター{i + 1}", "guitar", amp="crystal", volume=0.055, pan=-0.35, reverb=0.25, chorus=0, sustain=0.8) for i in range(4)]
GA = S.track("アコースティックギター（分散和音）", "guitar", amp="crystal", volume=0.075, pan=0.35, reverb=0.3, chorus=0, sustain=1.0)
PNFX = [{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 2.5}]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.075, pan=0.1, reverb=0.25, fx=PNFX) for i in range(3)]
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.19))
GLK = S.track("ベル（答える）", "glockenspiel", patch="glockenspiel", volume=0.07, pan=0.4, reverb=0.45)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.4) for i in range(3)]
PIZZ = S.track("ピチカート（しのび足）", "strings", patch="pizzicato", volume=0.06, pan=-0.2, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VR = ["1':0.5 1':0.5 3':0.5 1':0.5 5:1 R:1", "6:0.5 6:0.5 1':0.5 6:0.5 5:1 R:1", "2':0.5 2':0.5 7:0.5 2':0.5 5':1 R:1",
      "3':0.5 3':0.5 5':0.5 3':0.5 6':1 R:1", "6':0.5 5':0.5 3':0.5 1':0.5 3':1 R:1", "2':0.5 3':0.5 2':0.5 7:0.5 5:1 R:1",
      "1':1 3':1 5':1 3':1", "1':2 R:2"]
R1 = "ねこじゃらし/ゆらゆらり/ひだりみぎ/くるくるり/つかまえた/とおもったら/にげられた"
R2 = "ねこじゃらし/ゆらゆらり/ひだりみぎ/くるくるり/つかまえた/とおもったら/またにげた"
R3 = R1 + "/ねこじゃらし/ゆらゆらり/きみとぼく/くるくるり/おいかけっこ/おわらない/ろんどだよ"
R4 = R1 + "/ねこじゃらし/ゆらゆらり/あしたもね/くるくるり/あそぼうね/ひだまりで/またあした"
VE = ["R:0.5 3':0.5 3':0.5 2':0.5 1':0.5 2':0.5 3':1", "2':1.5 1':0.5 1':1 R:1", "R:0.5 1':0.5 1':0.5 7:0.5 6:0.5 7:0.5 1':1", "2':2 R:2"]
E1 = ("にちようびのごごに/ねこがあくびを/ひだまりのまどべで/まあるくなるの/"
      "わたしはしのびあし/ねこじゃらしをね/はなのさきでゆらす/ぴくりとみみが")
E2 = "とびついたしゅんかん/するりとにげた/ほんきのかおしてる/かわいすぎるよ"
VB = ["R:1 1':0.5 1':0.5 1':0.5 2':0.5 3':1", "2':2 R:2", "R:1 3':0.5 3':0.5 3':0.5 5':0.5 6':1", "5':2 R:2",
      "R:1 1':0.5 1':0.5 1':0.5 2':0.5 3':1", "2':1 3':1 R:2", "R:1 3':0.5 5':0.5 6':0.5 7':0.5 6':1", "5':2 R:2"]
B1 = "なんどでもね/くりかえそう/おなじあそびを/まいにちでも"
VX = ["R:1 3':1 2':1 1':1", "7:3 R:1", "R:1 6:1 7:1 1':1", "2':3 R:1"]
X1 = "おひるね/したねこ/ゆめでも/あそぶの/しっぽがね/ゆれてる"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)
    return bars, mel


ANS = []
for name, key, lines, text in (("主題1", K, VR, R1), ("主題2", K, VR, R2), ("主題3", K, VR * 2, R3), ("主題4", KL, VR * 2, R4)):
    ANS.append((put(name, key, lines, text), key))
put("第1の話", K, VE * 4, E1)
put("Bメロ", K, VB, B1)
put("第3の話", K, VX * 3, X1)
if VOCAL: put("第2の話", K, VE * 2, E2)
else:                                           # 歌なしの版: 第2の話はピアノが歌う
    for b, l in zip(S.sc("第2の話"), VE * 2): PN[0].bar(b, K.mel(l, oct=4))

# ================= ベルの答え（主題の句のあとの休みに、2つの音で） =================
for (bars, mel), key in ANS:
    for b, m in zip(bars, mel):
        toks = m.split()
        if not toks[-1].startswith("R:1") or len(toks) < 3: continue
        last = midi(toks[-2].split(":")[0])
        a = last + 12 if last + 12 <= midi("E6") else last
        GLK.at(S.bar_beat(b) + 3, f"{nm(a)}:0.5")
        GLK.at(S.bar_beat(b) + 3.5, f"{nm(a + (5 if (b % 2) else 7) if a < midi('A5') else a - 5)}:0.5")
for b in S.sc("第1の話") + S.sc("第2の話"):                   # 話の所は、4小節に1回だけ
    if (b - S.sc("第1の話")[0]) % 4 == 3: GLK.at(S.bar_beat(b) + 2.5, "D6:0.5"); GLK.at(S.bar_beat(b) + 3, "G6:1")

# ================= 伴奏 =================
STRUM = [(0, 1), (1, 0.5), (1.5, 0.5), (2.5, 0.5), (3, 0.5), (3.5, 0.5)]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b].split("/")[0]; bass_n = S.chords[b].split("/")[1] if "/" in S.chords[b] else None
    r = midi(bass_n + "2") if bass_n else low(ch, "E1")
    if bass_n and r > midi("D3"): r -= 12
    if r > midi("D2"): r -= 12
    gv = voice(ch, 60, 4); v = voice(ch, 64, 3); t = tones(ch, "D3", "D5")
    if n == "終わり" and i >= 8:
        if i == 8:
            for j in range(4): GT[j].at(S.bar_beat(b) + j * 0.03, f"{nm(gv[j])}:8")
            BASS.bar(b, f"{nm(r)}:8")
        continue
    if n == "転調":
        for j in range(4): GT[j].at(S.bar_beat(b) + j * 0.03, f"{nm(gv[j])}:3.9")
        BASS.bar(b, f"{nm(r)}:4")
        continue
    quiet = n in ("イントロ", "主題1", "第3の話") or n == "第1の話" and i < 8
    if quiet:                                   # 静かな所: ギターの分散和音
        GA.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 2)))
    else:                                       # ギターのストローク（下・下上・上下上）
        for st, Lx in STRUM:
            for j in range(4): GT[j].at(S.bar_beat(b) + st + j * 0.015, f"{nm(gv[j])}:{Lx - 0.03:.3f}")
    if n == "第3の話":
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:4")
        if i >= 4: BASS.bar(b, f"{nm(r)}:4")
        continue
    if n == "イントロ" and i < 2: continue
    BASS.bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:0.5 {nm(r + 12)}:1 {nm(r + 7)}:1" if not quiet else f"{nm(r)}:2 {nm(r + 7)}:2")
    if n.startswith(("主題", "Bメロ", "間奏")) and n != "主題1":
        for j in range(3): PN[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:1 R:0.5 {nm(v[j])}:0.5 R:1")
    if n.startswith(("第1", "第2")) and i % 2 == 0:            # しのび足（ピチカート）
        PIZZ.bar(b, f"{nm(t[0] + 12)}:0.5 R:0.5 {nm(t[1] + 12)}:0.5 R:0.5 {nm(t[2] + 12)}:0.5 R:0.5 {nm(t[1] + 12)}:0.5 R:0.5")
    if n in ("主題3", "主題4") or n == "Bメロ" and i >= 4:
        sv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
# 間奏: ベルが主題を歌い、ギターがかけ合う
for b, l in zip(S.sc("間奏"), VR): GLK.bar(b, K.mel(l, oct=5).replace("R:1", "R:1"))
for b in S.sc("終わり")[:8]:
    if (b - S.sc("終わり")[0]) % 2 == 1: GLK.at(S.bar_beat(b) + 3, "Eb6:0.5"); GLK.at(S.bar_beat(b) + 3.5, "Ab6:0.5")
GLK.at(S.bar_beat(S.sc("終わり")[9]) + 1, "Eb6:0.5"); GLK.at(S.bar_beat(S.sc("終わり")[9]) + 1.5, "C6:0.5"); GLK.at(S.bar_beat(S.sc("終わり")[9]) + 2, "Ab5:2")
cym_swell(CYM, S.sc("主題4")[0], 1, "E4")

# ================= ドラム（軽く: 小さいキック、2・4のスネア、8分のハット） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("イントロ", "主題1") or n == "第3の話" and i < 8:
        if n == "主題1" and last: put_fill(D, b, "small")
        continue
    if n == "転調":
        put_fill(D, b, "build"); continue
    if n == "終わり":
        if i < 8: vgroove(D, b, "beat8", ghosts=0.1, seed=b, h="x.x.x.x.x.x.x.x.")
        elif i == 8: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
        continue
    chorus = n.startswith("主題") or n == "間奏"
    if n == "第3の話":
        vgroove(D, b, "half", ghosts=0, seed=b, h="x...x...x...x...")
    elif n.startswith(("第1", "第2")):
        vgroove(D, b, "beat8", ghosts=0.15, seed=b, k="X.......X.......", h="x.x.x.x.x.x.x.x.")
    else:
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.....X.X......." if chorus else None, h="x.xxx.xxx.xxx.xx" if chorus else None)
    if i == 0 or (chorus and i % 8 == 0): crash(D, b, "C2", 4)
    if last: put_fill(D, b, "snare16" if n in ("Bメロ", "主題3") else "small")

SIL.add(S.sc("主題4")[0] - 2, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の24。アコースティック・ポップ。G 長調・112、最後の主題は +1（A♭）。"
          "日曜の午後、ねこじゃらしで猫と遊ぶ。「ねこじゃらし、ゆらゆらり」の主題が何度も帰ってくるロンドの形。"
          "歌の句が終わるたびにベルが2つの音で答える。アコースティックギター、ピチカートのしのび足、お昼寝の静かな話。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"主題1": -0.25, "第3の話": -0.45, "主題4": 0.5})
