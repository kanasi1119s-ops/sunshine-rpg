# vp25 02「ロボット掃除機の大冒険」The Great Voyage of a Robot Vacuum（仮）— テクノポップ。D長調（ベランダで E長調）・132・4/4。主役の楽器: チェンバロ
# 物語: 留守番中のロボット掃除機が、台所・居間・ソファの下（迷子）をへて、日の当たるベランダへ。電池が減って、ゆっくり充電台へ帰る。
# 形: 部屋めぐり。壁にぶつかるたびに向きが変わる（旋律の2音の動機が上下反転する）
# 場面と強さ: 起動＝リズムの型だけ／台所＝小刻みで中くらい／居間＝広がる／ソファの下＝暗くこもって小さい（迷子）／脱出＝せり上がる／
#   ベランダの日なた＝最大／電池が少ない＝テンポが落ちて細くなる／充電台＝電子音1つ
# 旋律の性格: 角ばった2音の動機（6度の跳躍＋1歩）。壁に当たるたびに上下が反転する。チェンバロは包丁のような16分の刻み
# 崩す所: ソファの下は、7つの16分でひと回りする型（4/4 の上で拍がずれる＝迷子）
from vp25_lib import *

S = Song("02", "roboclean", "ロボット掃除機の大冒険（仮）", "The Great Voyage of a Robot Vacuum", 132, 4, "D", "major", "テクノポップ")
K = S.key
KE = Key("E", "major")
KITCHEN = ["Dadd9", "F#m7", "Gmaj7", "E7", "Dadd9", "F#m7", "Bm7", "A7sus4"]
LIVING = ["Em7", "A7", "Dmaj7", "Bm7", "Em7", "F#7", "Bm7", "Bbmaj7"]
SOFA = ["Bm", "Bm/A", "Gmaj7", "F#7"]
ESCAPE = ["G", "A", "Bm", "C", "G", "A", "C", "B7"]
VERANDA = ["E", "G#7", "C#m7", "E7", "Amaj7", "Am6", "E/B", "B7"]
BATTERY = ["E", "C#m7", "Amaj7", "B7sus4"]

S.scene("起動", 8, "intro", ["D"] * 8)
S.scene("台所", 24, "verse", KITCHEN)
S.scene("壁1", 4, "break", ["Bbmaj7", "Bbmaj7", "A7sus4", "A7"])
S.scene("居間", 24, "pre", LIVING)
S.scene("壁2", 4, "break", ["Bbmaj7", "Bbmaj7", "F#7", "F#7"])
S.scene("ソファの下", 16, "bridge", SOFA)
S.scene("脱出", 8, "pre", ESCAPE)
S.scene("ベランダ", 32, "chorus", VERANDA)
S.scene("電池が少ない", 16, "outro", BATTERY)
S.scene("充電台", 6, "outro", ["E"] * 6)
S.tempo = [{"bar": S.sc("電池が少ない")[0] + 1, "bpm": 132}, {"bar": S.sc("電池が少ない")[4] + 1, "bpm": 112, "ramp": 12}]

HAR = S.track("主役: チェンバロ（刻み）", "harpsichord", volume=0.24, pan=-0.18, reverb=0.22, sustain=0.6, gainDb=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1}])
HAR2 = S.track("チェンバロ（対旋律）", "harpsichord", volume=0.2, pan=0.3, reverb=0.25, sustain=0.8, gainDb=3,
               fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2800, "high": 1}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.19, pan=0.0, delay=0.5))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.22, duck=0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.5, 0.5, 0][i], duck=0.2)) for i in range(3)]
BLIP = S.track("電子音（センサー）", "pad", **pluck_spec("pluckSynth", vol=0.07, pan=0.45, delay=0.75, sustain=0.4))
SSAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=[-0.6, 0.6, 0][i], duck=0.35, sustain=1.0)) for i in range(3)]
FX = S.track("効果音（ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 歌の役: 2音の動機（6度上へ跳んで1歩戻る）。壁のたびに上下反転 ----------
UPM = ["1:0.5 6:0.5 5:1 R:0.5 3:0.5 2:0.5 3:0.5", "R:0.5 2:0.5 7:0.5 6:1 R:0.5 5:0.5 3:0.5", "4:0.5 2':0.5 1':1 R:0.5 6:0.5 5:0.5 6:0.5", "#5:1.5 2':0.5 1':1 R:1",
       "1:0.5 6:0.5 5:1 R:0.5 3:0.5 2:0.5 3:0.5", "R:0.5 3:0.5 1':0.5 7:1 R:0.5 5:0.5 3:0.5", "4:0.5 2':0.5 1':0.5 7:0.5 6:1 5:0.5 4:0.5", "5:3 R:1"]
DNM = ["5:0.5 7,:0.5 1:1 R:0.5 3:0.5 4:0.5 3:0.5", "R:0.5 6:0.5 1:0.5 2:1 R:0.5 3:0.5 5:0.5", "3:0.5 5,:0.5 6,:1 R:0.5 1:0.5 2:0.5 1:0.5", "2:1.5 #5,:0.5 6,:1 R:1",
       "5:0.5 7,:0.5 1:1 R:0.5 3:0.5 4:0.5 3:0.5", "R:0.5 6:0.5 1:0.5 2:1 R:0.5 3:0.5 5:0.5", "6:0.5 1:0.5 2:0.5 3:0.5 4:1 3:0.5 2:0.5", "1:3 R:1"]
for i, b in enumerate(S.sc("台所")):
    if i < 8: continue                       # 最初の8小節はチェンバロだけで台所の様子
    LEAD.bar(b, K.mel(UPM[i % 8]))
# 居間: 反転した動機（下へ跳ぶ）で、長めの音
for i, b in enumerate(S.sc("居間")):
    m = DNM[i % 8]
    if i >= 16: m = seq_up(m, K, 2) if i % 8 < 6 else m
    LEAD.bar(b, K.mel(m, oct=4 if i < 16 else 5))
# 壁: 一撃と、動機の2音だけ（向きを変える合図）
for sc_, mel in (("壁1", ["1':0.5 6:0.5 R:3", "R:4", "6:0.5 1':0.5 R:3", "R:4"]), ("壁2", ["1':0.5 6:0.5 R:3", "R:4", "1:0.5 #4:0.5 R:3", "R:4"])):
    for i, b in enumerate(S.sc(sc_)): LEAD.bar(b, K.mel(mel[i]))
# ベランダ（E長調）: 動機は上向きに戻り、長く伸びやかに
VER = ["1:0.5 6:0.5 5:2 3:0.5 5:0.5", "#5:1 4':1 3':1 2':1", "R:0.5 3:0.5 1':0.5 7:0.5 6:1.5 5:0.5", "5:1 4:1 3:1 b7:1",
       "R:0.5 6:0.5 3':0.5 2':0.5 1':2", "b6:1 1':1 b3':1 2':1", "1':1.5 7:0.5 6:1 5:1", "4:1 5:1 6:1 7:1",
       "1':0.5 6':0.5 5':2 3':0.5 5':0.5", "#5':1 4'':1 3'':1 2'':1", "R:0.5 3':0.5 1'':0.5 7':0.5 6':1.5 5':0.5", "5':1 4':1 3':1 b7':1",
       "R:0.5 6:0.5 3':0.5 2':0.5 1':2", "b6:1 1':1 b3':1 2':1", "3':1.5 2':0.5 1':1 7:1", "1':3 R:1"]
for i, b in enumerate(S.sc("ベランダ")):
    m = VER[i % 16]
    if i < 16 and i % 16 in (8, 9, 10, 11): m = VER[i % 8]          # 1回目は高い所へ行かない（2回目にとっておく）
    LEAD.bar(b, KE.mel(m))
# 電池: 動機の断片だけ、だんだん間があく
BAT = ["1':0.5 6:0.5 5:3", "R:4", "3':0.5 1':0.5 7:3", "R:4", "1':0.5 6:0.5 5:3", "R:4", "6:0.5 4:0.5 3:3", "R:4",
       "1':0.5 6:3.5", "R:4", "R:4", "5:4", "R:4", "R:4", "R:4", "R:4"]
for i, b in enumerate(S.sc("電池が少ない")): LEAD.bar(b, KE.mel(BAT[i]))

# ---------- チェンバロ ----------
def chop(b, lo="D4", hi="D6", pat="0102010301020104", acc=(0, 4, 8, 12)):
    t = tones(S.chords[b], lo, hi)
    return " ".join(f"{nm(t[int(c) % len(t)])}:0.25{'!' if i in acc else (',' if i % 2 else '')}" for i, c in enumerate(pat))


CHOP_PATS = ["0102010301020104", "0120012001200124", "0213021302130243", "0102030401020304"]
for i, b in enumerate(S.sc("台所")):
    # 包丁の刻み（4小節ごとに型を変える）。歌が入る8小節目からは、歌の間（休み）だけ刻む
    pat = CHOP_PATS[(i // 4) % 4]
    if i < 8: HAR.bar(b, chop(b, "D4", "A5", pat))
    else: HAR.bar(b, chop(b, "A3", "F#5", pat, acc=(0, 6, 10)))
for i, b in enumerate(S.sc("居間")):
    # 居間はアルベルティ（下・上・中・上）の8分で、ゆったり
    t = tones(S.chords[b], "A3", "D5")
    HAR.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.5" for k in [0, 3, 1, 3, 0, 3, 1, 3]))
    if i >= 8:
        # 対旋律: 歌の長い音の所で、上から下りる8分
        tt = tones(S.chords[b], "D5", "D6")
        HAR2.bar(b, "R:2 " + " ".join(f"{nm(tt[-1 - k % len(tt)])}:0.5" for k in range(4)))
for sc_ in ("壁1", "壁2"):
    for i, b in enumerate(S.sc(sc_)):
        if i % 2 == 0:
            t = tones(S.chords[b], "D3", "D5")
            HAR.bar(b, " ".join(f"{nm(x)}:0.0625" for x in t[:6]) + f" {nm(t[-1])}:{4 - 0.0625 * 6:g}")   # ジャラン（ぶつかった音）

# ソファの下: 7つの16分でひと回りする型（迷子）。低く、暗く
sofa = S.sc("ソファの下")
CYC = "X..x.x."          # 7つの16分
pos = 0
seqn = [0, 2, 1, 2, 3, 2, 1]
k = 0
for i, b in enumerate(sofa):
    t = tones(S.chords[b], "B2", "B4")
    toks = []
    for j in range(16):
        c = CYC[pos % 7]; pos += 1
        if c == ".": toks.append("R:0.25")
        else: toks.append(f"{nm(t[seqn[k % 7] % len(t)])}:0.25{'!' if c == 'X' else ','}"); k += 1
    HAR.bar(b, merge_rests(" ".join(toks)))
# 脱出: 16分の上行（せり上がる）
for i, b in enumerate(S.sc("脱出")):
    t = tones(S.chords[b], "D4", "D6")
    HAR.bar(b, " ".join(f"{nm(t[(k + i) % len(t)])}:0.25" for k in range(16)))
# ベランダ: 歌の後ろで16分の明るい刻み（E長調）、後半は対旋律（2本目）
for i, b in enumerate(S.sc("ベランダ")):
    HAR.bar(b, chop(b, "E4", "E6", CHOP_PATS[(i // 2) % 4], acc=(0, 3, 6, 10, 12)))
    if i >= 16:
        tt = tones(S.chords[b], "E5", "E6")
        HAR2.bar(b, " ".join(f"{nm(tt[k % len(tt)])}:0.5" for k in [2, 1, 0, 1, 2, 3, 2, 1]))
for i, b in enumerate(S.sc("電池が少ない")):
    if i < 8: HAR.bar(b, chop(b, "E4", "E5", "0.0.1.0.2.0.1.0.".replace(".", "0")[:16], acc=(0, 8)) if i % 2 == 0 else "R:4")
    elif i in (8, 11): t = tones(S.chords[b], "E4", "E5"); HAR.bar(b, f"{nm(t[0])}:1 {nm(t[1])}:1 {nm(t[2])}:2")

# ---------- 起動・センサーの電子音 ----------
BOOT = ["D6:0.25 R:3.75", "D6:0.25 A6:0.25 R:3.5", "D6:0.25 A6:0.25 D7:0.25 R:3.25", "R:4",
        "D6:0.25 R:0.25 D6:0.25 R:0.25 A6:0.25 R:0.75 D6:0.25 R:1.75", "D6:0.25 R:0.25 D6:0.25 R:0.25 A6:0.25 R:0.75 F#6:0.25 R:1.75",
        "D6:0.25 R:0.25 D6:0.25 R:0.25 A6:0.25 R:0.75 D6:0.25 R:1.75", "A6:0.25 R:0.25 A6:0.25 R:0.25 E6:0.5 R:2.5"]
for i, b in enumerate(S.sc("起動")): BLIP.bar(b, BOOT[i])
for b in S.sc("居間")[::4] + S.sc("ベランダ")[2::8]: BLIP.bar(b, "R:3 A6:0.25 R:0.25 E7:0.25 R:0.25")
fin = S.sc("充電台")
BLIP.bar(fin[2], "E6:0.5 B6:0.5 E7:1.5 R:1.5")       # 充電台の「ピッ」

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    if n == "起動": BASS.bar(b, "R:4" if i < 4 else "D1:0.25! R:0.75 D1:0.25 R:0.75 D2:0.25 R:0.75 D1:0.25 R:0.75"); continue
    if n == "台所": BASS.bar(b, bass_line(S, b, "push" if i >= 8 else "half")); continue
    if n in ("壁1", "壁2"): BASS.bar(b, f"{nm(low(S.chords[b]))}:1! R:3" if i % 2 == 0 else "R:4"); continue
    if n == "居間": BASS.bar(b, bass_line(S, b, "oct8" if i >= 8 else "root8")); continue
    if n == "ソファの下": BASS.bar(b, f"{nm(low(S.chords[b], 'B0'))}:4" if i % 2 == 0 else f"{nm(low(S.chords[b], 'B0'))}:2 R:2"); continue
    if n == "脱出": BASS.bar(b, bass_line(S, b, "root8")); continue
    if n == "ベランダ": BASS.bar(b, bass_line(S, b, "oct8") if i % 4 != 3 else bass_line(S, b, "push")); continue
    if n == "電池が少ない": BASS.bar(b, bass_line(S, b, "half") if i < 8 else (f"{nm(low(S.chords[b]))}:4" if i % 4 == 0 else "R:4")); continue

# ---------- 和音（パッド・厚い和音） ----------
pv = chord_voices(S, range(S.nb), center=60, n=3)
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    if n in ("居間", "ソファの下", "電池が少ない") or (n == "台所" and i >= 16):
        if n == "電池が少ない" and i >= 12: continue
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")
    if n == "ベランダ" or n == "脱出" and i >= 4:
        sv = voice(S.chords[b], 66, 3)
        pat = "X:0.75 X:0.75 X:0.5 R:0.5 X:0.75 X:0.75" if n == "ベランダ" else "X:4"
        for j in range(3): SSAW[j].bar(b, pat.replace("X", nm(sv[j])))
    if n == "充電台" and i < 5:
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")

riser(FX, S.sc("ベランダ")[0], 8, "D4"); cym_swell(CYM, S.sc("ベランダ")[0], 2, "C4")
cym_swell(CYM, S.sc("居間")[0], 1, "C4"); cym_swell(CYM, S.sc("ベランダ")[16], 2, "C4")

# ---------- ドラム ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    last = i == L - 1
    if n == "起動":
        if i >= 4: D.set(b, h="x.x.x.x.x.x.x.x.")
        continue
    if n == "台所":
        put_groove(D, b, ("X.....x...X.....", "....X.......X..." if i >= 8 else "................", "xxoxxxoxxxoxxxox"), ghosts=0.4, seed=b)
        if i == 8: crash(D, b, "A2", 2)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
        continue
    if n in ("壁1", "壁2"):
        if i % 2 == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "B2", 4)
        elif i == 3: D.set(b, "................", "........x.x.XXXX", "................")
        continue
    if n == "居間":
        put_groove(D, b, "four", ghosts=0.3, seed=b)
        D.H[b] = "..x...x...x...x." if i < 8 else "x.x.x.x.x.x.x.x."      # 2026-10-25: 居間の PQ が 7.3 と低いので、開いたハットをやめる
        if i in (0, 8, 16): crash(D, b)
        if i % 8 == 7: put_fill(D, b, "tomdown" if last else "small")
        continue
    if n == "ソファの下":
        # キックは7つの16分の型（ハットは4/4 のまま、弱く）
        kk = "".join("X" if CYC[(16 * i + j) % 7] == "X" else "." for j in range(16))
        D.set(b, kk, "................", "..o...o...o...o.")
        continue
    if n == "脱出":
        put_groove(D, b, ("X...X...X...X...", "....X.......X..." if i < 4 else "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x."), seed=b)
        if i >= 6: D.S[b] = "xxxxxxxxXXXXXXXX" if i == 7 else "x.x.x.x.xxxxxxxx"
        continue
    if n == "ベランダ":
        put_groove(D, b, "fourOpen", ghosts=0.4, seed=b)
        D.S[b] = "....X......oX..o"
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        elif i % 4 == 3: put_fill(D, b, "small")
        continue
    if n == "電池が少ない":
        if i < 8: put_groove(D, b, "half", seed=b); D.H[b] = "x...x...x...x..."
        elif i < 12: D.set(b, "X...............", "................", "x.......x.......")
        if i == 0: crash(D, b, "D2")
        continue

S.flags += " --space room --space-wet 0.12"
S.fade_out = 6
S.desc = ("仮: ボカロ曲のインスト25曲の02。テクノポップ。D長調→ベランダで E長調・132（電池が減ると112へ）。主役の楽器はチェンバロ。"
          "ロボット掃除機が台所（包丁のような16分の刻み）・居間（アルベルティ）・ソファの下（7つの16分でひと回りする型で迷子）をへて、日の当たるベランダへ。"
          "壁にぶつかるたびに歌の役の2音の動機が上下反転する。最後は充電台の電子音1つ。自作")
S.write()
