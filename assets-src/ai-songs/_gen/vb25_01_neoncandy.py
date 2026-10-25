# vb25 01「ネオンキャンディ・バグ」Neon Candy Bug（仮）— テクノポップ（高速）。F#m（サビは平行調の A）・188・4/4。最後のサビは +1（Gm／B♭）
# 物語: 古いゲーム機の中のキャラクターが、画面のすみのバグの穴を見つけて、外の世界へ飛び出す。
# 場面と強さ: 起動（チップのリフ・中）→ ゲームの中の毎日（Aメロ・語る）→ 穴を見つける（Bメロ・溜め）→ 決心のサビ（強）
#   → 2周目（ピアノが歌を受け取る）→ 穴に落ちる（1拍の完全な無音 → Half feel・こもった音）→ 外の世界（4つ打ちで明るく開く）
#   → チップのソロ → 落ちサビ（ピアノと歌だけ）→ 最後のサビ（+1・最大）→ 電源が切れる（急停止）
# 旋律の性格: Aメロは16分の早口で同じ音を連打して語る。サビは同じ音の3連打のフックと、オクターブの跳躍。最高音 C#6（最後は D6）
from vb25_lib import *

S = Song("01", "neoncandy", "ネオンキャンディ・バグ（仮）", "Neon Candy Bug", 188, 4, "F#", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # F# の短調
KA = Key("A", "major")       # サビ（平行調）
KG = Key("G", "minor")       # 最後のサビの短調側（+1）
KB = Key("Bb", "major")      # 最後のサビ（+1）

RIFF_CH = ["F#m", "D", "E", "F#m"]
A_CH = ["F#m", "D", "E", "F#m"]
B_CH = ["D", "E", "C#m", "F#m", "D", "E", "Bm7", "C#7"]
C_CH = ["F#m", "D", "E", "A", "F#m", "D", "E", "E/G#"]
C_CH2 = ["F#m", "D", "E", "A", "F#m", "D", "Bm7", "C#7"]
HOLE = ["Bm7", "C#7", "F#m", "F#m/E", "Dmaj7", "C#7sus4", "C#7", "C#7"]
OUT = ["A", "E/G#", "F#m", "D", "A/C#", "D", "E", "E"]
LAST = ["Gm", "Eb", "F", "Bb", "Gm", "Eb", "F", "F/A"]
LAST2 = ["Gm", "Eb", "F", "Bb", "Gm", "Eb", "Cm7", "D7"]

S.scene("起動", 8, "intro", RIFF_CH)
S.scene("ゲームの中の毎日", 16, "verse", A_CH)
S.scene("穴を見つける", 8, "pre", B_CH)
S.scene("決心", 16, "chorus", C_CH + C_CH2)
S.scene("ステージ2", 8, "interlude", RIFF_CH)
S.scene("2周目", 16, "verse", A_CH)
S.scene("穴を見つける2", 8, "pre", B_CH)
S.scene("決心2", 16, "chorus", C_CH + C_CH2)
S.scene("穴に落ちる", 16, "bridge", HOLE)
S.scene("外の世界", 16, "chorus", OUT)
S.scene("ボーナスステージ", 16, "interlude", RIFF_CH)
S.scene("落ちサビ", 8, "break", C_CH)
S.scene("最後の決心", 24, "chorus", LAST + LAST2 + LAST)
S.scene("ゲームの外", 12, "outro", ["Gm", "Eb", "F", "Gm"])
S.scene("電源オフ", 2, "outro", ["Gm", "Gm"])

V = Voice(S, vol=0.22, delay=0.75)
CHIP = S.track("チップのリフ（矩形波 25%）", "lead", patch="chipPulse25", volume=0.13, pan=-0.2, reverb=0.12, mono=True, gainDb=1,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 7500, "q": 0.7},
                   {"type": "pingpong", "beats": 0.75, "mix": 0.12, "feedback": 0.2}])
CHIP2 = CHIP   # 合いの手もチップのリフのパートで（チャンネルの数を節約）
PN = S.track("ピアノ（右手）", "piano", volume=0.13, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
PNL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
PNM = S.track("ピアノ（歌の受け渡し）", "piano", volume=0.17, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass2", vol=0.21, duck=0.25))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.055, pan=[-0.6, 0.6, 0][i], duck=0.45, sustain=0.9)) for i in range(3)]
PAD = [S.track(f"こもったパッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.07, pan=[-0.5, 0.5][i], duck=0.2),) for i in range(2)]
for p in PAD: p.spec["fx"] = [{"type": "filter", "kind": "lowpass", "freq": 900, "q": 0.8}, {"type": "reverb", "mix": 0.35}]
ARP = S.track("プラックのアルペジオ", "pad", **pluck_spec("pluckSynth", vol=0.075, pan=0.4, delay=0.75, sustain=0.5))
BELL = S.track("FMベル（きらめき）", "fmBell", volume=0.1, pan=0.3, reverb=0.4, sustain=1.2, gainDb=1)
WOB = S.track("ワブルベース（一瞬）", "bass", patch="reeseBass", volume=0.12, pan=0, gainDb=1,
              fx=[{"type": "syncfilter", "beats": 0.5, "depth": 0.8, "freq": 900}, {"type": "filter", "kind": "highpass", "freq": 45, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.08, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律 =================
# Aメロ（F#m の度数）: 16分の早口。同じ音の連打で語り、4小節目で上へ抜ける
A1 = ["R:0.25 5,:0.25 1:0.25 1:0.25 1:0.5 3:0.25 1:0.25 R:0.25 5,:0.25 1:0.25 3:0.25 4:0.5 3:0.5",
      "R:0.25 3:0.25 3:0.25 3:0.25 4:0.25 3:0.25 1:0.5 R:0.25 6,:0.25 1:0.25 3:0.25 1:1",
      "R:0.25 2:0.25 2:0.25 2:0.25 4:0.25 5:0.25 4:0.25 2:0.25 R:0.25 7,:0.25 2:0.25 4:0.25 5:0.5 4:0.5",
      "3:0.5 1:0.25 5,:0.25 R:0.5 1:0.25 3:0.25 5:1.5 R:0.5"]
A1b = A1[:3] + ["3:0.5 4:0.25 5:0.25 R:0.25 5:0.25 7:0.5 1':2"]
A2 = ["R:0.25 1':0.25 1':0.25 1':0.25 7:0.25 5:0.25 4:0.5 R:0.25 3:0.25 4:0.25 5:0.25 7:0.5 5:0.5",
      "R:0.25 6:0.25 6:0.25 6:0.25 5:0.25 4:0.25 3:0.5 R:0.25 1:0.25 3:0.25 4:0.25 3:1",
      "R:0.25 7:0.25 7:0.25 7:0.25 5:0.25 4:0.25 2:0.25 4:0.25 5:0.5 7:0.5 1':0.5 2':0.5",
      "1':0.75 7:0.25 5:0.5 4:0.5 3:1 R:1"]
VERSE = A1 + A1b + A2 + A1b
# Bメロ: 少しずつ上げて溜める。最後の小節は止め
BM = ["1:1 3:0.5 4:0.5 5:1 4:0.5 3:0.5", "2:1 4:0.5 5:0.5 7:1.5 5:0.5", "5:1 2:0.5 5:0.5 1':1 7:0.5 5:0.5", "1':2 7:1 1':1",
      "3':1 2':0.5 1':0.5 3':1 2':0.5 1':0.5", "2':1 1':0.5 7:0.5 2':2", "4':1 3':0.5 2':0.5 1':1 2':1", "5:1 #7:1 R:2"]
# サビ（A長調の度数）: 同じ音の3連打のフック → オクターブの跳躍 → 最高音 C#6
CH1 = ["R:0.5 3:0.5 3:0.5 3:0.5 5:1 3:1", "2:0.5 1:0.5 2:0.5 3:0.5 6:1.5 R:0.5", "R:0.5 5,:0.5 5:0.5 5:0.5 1':1 7:0.5 5:0.5", "3:1 2:0.5 1:0.5 1:2",
       "R:0.5 3:0.5 3:0.5 3:0.5 5:1 3:1", "2:0.5 1:0.5 2:0.5 3:0.5 6:0.5 1':0.5 2':1", "3':1.5 2':0.5 1':0.5 7:0.5 5:1", "7:1 5:1 7:2"]
CH2 = CH1[:6] + ["3':1 2':1 1':1 2':1", "#5:1 3:1 #5:1 7:1"]
CHORUS = CH1 + CH2

for name in ("ゲームの中の毎日", "2周目"):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(VERSE[i], oct=4)
        if name == "2周目" and i < 8:
            PNM.bar(b, shift_oct(line, 1))                 # 2周目の前半は、ピアノが歌を受け取る
        else:
            V.bar(b, line)
for name in ("穴を見つける", "穴を見つける2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BM[i], oct=4))
for name in ("決心", "決心2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KA.mel(CHORUS[i], oct=4))
# 穴に落ちる: Half feel。長い音でゆっくり落ちていく歌（高い所から）
HL = ["5':2 4':1 3':1", "#7:3 R:1", "1':2 7:1 5:1", "4:3 R:1", "6:2 5:1 3:1", "4:1.5 5:0.5 7:2", "R:1 #7:1 2':1 4':1", "#7':4"]
for i, b in enumerate(S.sc("穴に落ちる")):
    if i >= 8: V.bar(b, K.mel(HL[i - 8], oct=4))
# 外の世界: ピアノが主旋律（受け渡し）、歌は後半で重なる
OW = ["3:0.5 5:0.5 1':1 7:0.5 5:0.5 3:1", "2:0.5 3:0.5 5:1 3:0.5 2:0.5 7,:1", "1:0.5 3:0.5 6:1 5:0.5 3:0.5 1:1", "2:0.5 4:0.5 6:1 1':0.5 2':0.5 3':1",
      "5':1 3':0.5 1':0.5 3':1 2':1", "1':0.5 2':0.5 3':1 2':0.5 1':0.5 6:1", "5:0.5 6:0.5 7:1 1':0.5 2':0.5 5:1", "5:2 #4:1 5:1"]
for i, b in enumerate(S.sc("外の世界")):
    PNM.bar(b, KA.mel(OW[i % 8], oct=4))
    if i >= 8: V.bar(b, KA.mel(["3:2 5:2", "7,:2 3:2", "6,:2 1:2", "2:2 4:2", "5:2 3:2", "6:2 3:2", "2:2 5:2", "5:4"][i - 8], oct=4))
# 落ちサビ: ピアノと歌だけ。歌は1オクターブ下で、ささやくように（重ねなし）
for i, b in enumerate(S.sc("落ちサビ")): V.bar(b, KA.mel(CH1[i], oct=4), low=False)
# 最後のサビ（B♭長調）: +1。最後の8小節は最高音 D6 へ
LAST_L = CH1 + CH2 + CH1[:6] + ["3':1 4':1 5':2", "3':4"]
for i, b in enumerate(S.sc("最後の決心")): V.bar(b, KB.mel(LAST_L[i], oct=4))
for i, b in enumerate(S.sc("ゲームの外")): V.bar(b, KG.mel(["5:2 3:2", "1:4", "2:2 5,:2", "1:4"][i % 4], oct=4) if i < 8 else KG.mel("R:4", oct=5))

# ================= チップのリフ・ソロ =================
RIFF = ["1:0.25 1':0.25 5:0.25 3:0.25 1:0.25 1':0.25 7:0.25 5:0.25 1:0.25 1':0.25 5:0.25 3:0.25 4:0.25 3:0.25 2:0.25 7,:0.25",
        "6,:0.25 6:0.25 3:0.25 1:0.25 6,:0.25 6:0.25 4:0.25 3:0.25 6,:0.25 6:0.25 3:0.25 1:0.25 3:0.25 4:0.25 6:0.25 1':0.25",
        "7,:0.25 7:0.25 4:0.25 2:0.25 7,:0.25 7:0.25 5:0.25 4:0.25 7,:0.25 7:0.25 4:0.25 2:0.25 4:0.25 5:0.25 7:0.25 2':0.25",
        "1':0.5 7:0.25 5:0.25 3:0.5 1:0.25 3:0.25 5:1 R:1"]
for name in ("起動", "ステージ2"):
    for i, b in enumerate(S.sc(name)): CHIP.bar(b, K.mel(RIFF[i % 4], oct=4))
# ボーナスステージ: チップのソロ（4小節ずつ、上へ）。最後の2小節はスタッター（同じ音の32分の連打）
SOLO = [RIFF[0], RIFF[1], RIFF[2], "1':0.25 2':0.25 3':0.25 5':0.25 3':0.25 2':0.25 1':0.25 7:0.25 5:0.5 3:0.5 1:1",
        "3:0.25 5:0.25 1':0.25 3':0.25 " * 2 + "4:0.25 6:0.25 1':0.25 4':0.25 " * 2,
        "2:0.25 4:0.25 6:0.25 2':0.25 " * 2 + "2:0.25 5:0.25 7:0.25 2':0.25 " * 2,
        "1':0.25 3':0.25 5':0.25 1'':0.25 5':0.25 3':0.25 1':0.25 5:0.25 1':0.25 3':0.25 5':0.25 1'':0.25 7':0.5 5':0.5",
        "5':1 4':0.5 3':0.5 2':1 1':1"]
for i, b in enumerate(S.sc("ボーナスステージ")):
    if i < 14: CHIP.bar(b, K.mel(SOLO[i % 8].strip(), oct=4))
    elif i == 14: CHIP.bar(b, K.mel(" ".join(["1':0.125"] * 16 + ["5:0.125"] * 16), oct=4))
    else: CHIP.bar(b, K.mel(" ".join(["7:0.125"] * 8 + ["#7:0.125"] * 8) + " R:2", oct=4))
# 合いの手（歌のすき間に、高いチップの短い句）
for name in ("ゲームの中の毎日", "2周目"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: CHIP2.bar(b, K.mel("R:3 5':0.25 4':0.25 3':0.25 1':0.25", oct=4))
for name in ("決心", "決心2", "最後の決心"):
    kk = KB if name == "最後の決心" else KA
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: BELL.bar(b, kk.mel("R:2 5':0.5 3':0.5 1':1", oct=4))

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "電源オフ": continue
    v = voice(ch, 64, 3)
    # ベース
    if n in ("起動", "ステージ2", "ボーナスステージ"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("ゲームの中の毎日", "2周目"): BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "oct8"))
    elif n.startswith("穴を見つける"): BASS.bar(b, bass_line(S, b, "push" if i < 7 else "long"))
    elif n.startswith("決心") or n == "最後の決心": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "穴に落ちる": BASS.bar(b, bass_line(S, b, "long") if i >= 2 else "R:4")
    elif n == "外の世界": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "ゲームの外": BASS.bar(b, bass_line(S, b, "half"))
    # 厚い和音（サビだけ）
    if n.startswith("決心") or n == "最後の決心" or (n == "外の世界" and i >= 8):
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5")
    # ピアノ（右手16分の分散和音・左手8分のオクターブ）
    if n.startswith("穴を見つける") or n.startswith("決心") or n == "最後の決心" or n == "落ちサビ":
        if n == "落ちサビ":
            PN.bar(b, " ".join(f"{nm(x)}:4" for x in [v[1]])); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
        else:
            PN.bar(b, piano_arp16(ch, "C#4", "C#6")); PNL.bar(b, piano_left8(ch, "C2"))
    if n in ("ゲームの中の毎日", "2周目") and i >= 8:
        PN.bar(b, " ".join(f"{nm(x)}:0.5" for x in [v[0], v[2], v[1], v[2]] * 2))
    # こもったパッド（穴の中）
    if n == "穴に落ちる":
        for j in range(2): PAD[j].bar(b, f"{nm(v[j])}:4")
    # プラックのアルペジオ（Aメロの後半・外の世界）
    if (n in ("ゲームの中の毎日", "2周目") and i >= 8) or n == "外の世界":
        t = tones(ch, "A4", "A6"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)))

# ワブルベース（一瞬だけ。2回目のサビの終わりの2小節）
for b in S.sc("決心2")[-2:]: WOB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:4")
# 効果音
riser(FX, S.sc("決心")[0] - 2, 8, "C4"); riser(FX, S.sc("決心2")[0] - 2, 8, "C4"); riser(FX, S.sc("最後の決心")[0] - 4, 16, "D4")
cym_swell(CYM, S.sc("外の世界")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("最後の決心")[0] - 1, 2, "C4")
FX.bar(S.sc("電源オフ")[0], "E4:4 R:4")                 # 電源が切れる（ダウンリフター）

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "起動":
        vgroove(D, b, "vrock" if i >= 4 else "none", seed=b)
        if i < 4: D.set(b, "X...X...X...X...", "................", "................")
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("ゲームの中の毎日", "2周目"):
        vgroove(D, b, "vrock2" if i < 8 else "vrock", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("穴を見つける"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)                               # 止め（後ろ2拍は全員休み）
    elif n.startswith("決心") or n == "最後の決心":
        # 2回目のサビの前半は Half feel（サビごとにリズムを入れかえる）
        name = "halfdrive" if (n == "決心2" and i < 8) else "vrock"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n != "最後の決心": put_fill(D, b, "tomdown")
    elif n == "ステージ2":
        vgroove(D, b, "four16", seed=b)
        if last: put_fill(D, b, "small")
    elif n == "穴に落ちる":
        if i < 2: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n == "外の世界":
        vgroove(D, b, "four", seed=b)
        if i == 0: crash(D, b)
        if i == 8: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "ボーナスステージ":
        vgroove(D, b, "vrock", ghosts=0.4, seed=b)
        if i % 4 == 0: crash(D, b, "B2" if i % 8 == 4 else "C2")
        if i >= 14: D.set(b, "X.X.X.X.X.X.X.X.", "....X.......XXXX", "x.x.x.x.x.x.x.x.")
    elif n == "落ちサビ":
        D.set(b, "." * 16, "." * 16, "." * 16)
        if last: put_fill(D, b, "build")
    elif n == "ゲームの外":
        vgroove(D, b, "half", seed=b)
        if i == 0: crash(D, b)
    elif n == "電源オフ":
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)
        if i == 0: crash(D, b, "C2", 2)

# 1拍の完全な無音（穴に落ちる直前）と、Bメロの最後の止め
SIL.add(S.sc("穴に落ちる")[0] - 1, 3, 4)
for name in ("穴を見つける", "穴を見つける2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("電源オフ")[0], 1, 8)       # 電源が切れたら、何も鳴らない
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の01。テクノポップ。F#m（サビは A）・188。古いゲーム機のキャラが、バグの穴から外の世界へ飛び出す。"
          "チップのリフで始まり、16分の早口の Aメロ、同じ音の3連打のサビ、1拍の無音から Half feel の穴の中、4つ打ちの外の世界、"
          "チップのソロとスタッター、ピアノと歌だけの落ちサビ、+1 の最後のサビ、電源が切れて急停止。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
