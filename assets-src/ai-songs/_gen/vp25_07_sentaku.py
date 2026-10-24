# vp25 07「洗濯物日和」Perfect Laundry Weather（仮）— ダンス（ディスコ）。E ミクソリディアン・118→128（脱水）→100（干す）・4/4。主役の楽器: スラップベース
# 物語: 晴れた日曜。洗濯機のスイッチを入れる。洗う、泡、すすぐ、脱水でぐるぐる回って、ぴたりと止まる。物干しで、洗濯物が風にゆれる。
# 形: 洗う→すすぐ→脱水（だんだん速くなる）→物干しで風に揺れる
# 場面と強さ: スイッチ＝ベースだけ／洗う・すすぐ＝跳ねる中くらい／泡＝ふわっと引く／脱水＝回転が最高速で最大→ぴたりと止まる（無音）／
#   干す＝ゆったりした揺れ（はねるリズム）／風＝パッドとベースの1音
# 旋律の性格: スラップベースの16分のオクターブ跳躍（ベースが旋律を弾く）。歌の役は弦で、しゃくり上げる
# 崩す所: ディスコなのにテンポが上がる（脱水の回転）。干す所で 100 に落とし、はねるリズムに
from vp25_lib import *

S = Song("07", "sentaku", "洗濯物日和（仮）", "Perfect Laundry Weather", 118, 4, "E", "mixolydian", "ダンス（ディスコ）")
K = Key("E", "major")     # 旋律は長調の度数で書く（b7＝D がミクソリディアンの音）
WASH = ["E7", "A9", "E7", "A9", "F#m7", "G#m7", "Amaj7", "B7sus4"]
FOAM = ["Cmaj7", "Dmaj7", "Bm7", "E7sus4"]
RINSE = ["E7", "A9", "G#m7", "C#m7", "F#m7", "B7", "E", "D/E"]
SPIN = ["E", "D/E", "A/E", "B"]
HANG = ["Amaj7", "G#m7", "F#m7", "E/G#", "Amaj7", "B7sus4", "C#m7", "B7sus4"]
S.scene("スイッチ", 4, "intro", ["E7"] * 4)
S.scene("洗う", 24, "verse", WASH)
S.scene("泡", 16, "bridge", FOAM)
S.scene("すすぐ", 24, "verse", RINSE)
S.scene("脱水", 24, "chorus", SPIN)
S.scene("止まる", 2, "break", ["E", "E"])
S.scene("干す", 32, "chorus", HANG)
S.scene("風", 8, "outro", ["Eadd9" if False else "E"] * 8)
b_spin, b_stop, b_hang = S.sc("脱水")[0], S.sc("止まる")[0], S.sc("干す")[0]
S.tempo = [{"bar": b_spin + 1, "bpm": 118}, {"bar": b_spin + 2, "bpm": 128, "ramp": 20}, {"bar": b_hang + 1, "bpm": 100}]

SL = S.track("主役: スラップベース", "slap", volume=0.24, pan=0, gainDb=4, duck=0.1,
             fx=[{"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 3, "midHz": 2400, "high": 2},
                 {"type": "compressor", "threshold": -18, "ratio": 3.5, "attack": 0.003, "release": 0.09}])
STRL = S.track("弦（歌の役）", "strings", patch="stringEnsemble", volume=0.2, pan=0.1, reverb=0.3, gainDb=4, phrase=8, mono=True,
               fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1}])
STRH = [S.track(f"弦の伴奏{i + 1}", "strings", patch="stringEnsemble", **strings_spec(vol=0.08, pan=[-0.55, 0.55][i])) for i in range(2)]
EP = [S.track(f"エレピの刻み{i + 1}", "fmEpiano", volume=0.1, pan=[-0.35, 0.35, 0][i], reverb=0.15, sustain=0.5) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.5, 0.5, 0][i], duck=0.2)) for i in range(3)]
ARP = S.track("回るアルペジオ（脱水）", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.4, delay=0.5, sustain=0.5))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- スラップベース（旋律を弾くベース。親指の低い音と、はじく高い音の跳躍） ----------
def slap_bar(b, style):
    ch = S.chords[b]
    r = low(ch, "E1"); o = r + 12; f5 = r + 7; b7 = r + 10; m3 = r + 3; M3 = r + 4
    nx = S.chords[b + 1] if b + 1 < S.nb else ch
    rn = low(nx, "E1"); ap = rn - 1 if rn != r else r + 7
    N = lambda m, L, mk="": f"{nm(m)}:{L:g}{mk}"
    if style == "riff":       # 洗う: オクターブ跳躍＋短3度→長3度のすべり
        return " ".join([N(r, 0.25, "!"), N(o, 0.25), "R:0.25", N(r, 0.25, ","), N(o, 0.25), N(r, 0.25), N(m3 + 12, 0.25), N(M3 + 12, 0.25),
                         N(r, 0.5, "!"), N(o, 0.25), N(r, 0.25, ","), N(b7, 0.25), N(f5, 0.25), N(o, 0.25), N(ap, 0.25)])
    if style == "riff2":
        return " ".join([N(r, 0.5, "!"), N(o, 0.25), N(r, 0.25, ","), "R:0.25", N(o, 0.25), N(b7 + 12 - 12, 0.25), N(o, 0.25),
                         N(r, 0.25, "!"), N(r, 0.25, ","), N(o, 0.25), N(f5 + 12, 0.25), N(o, 0.5), N(f5, 0.25), N(ap, 0.25)])
    if style == "foam":
        return f"{nm(r)}:1.5 {nm(f5)}:0.5 {nm(o)}:1 {nm(b7)}:1"
    if style == "spin":       # 脱水: 回る（同じ4音がぐるぐる）
        cyc = [r, o, f5 + 12 if f5 + 12 <= midi("G3") else f5, o]
        return " ".join(N(cyc[j % 4], 0.25, "!" if j % 4 == 0 else "") for j in range(16))
    if style == "hang":       # 干す: はねる（付点）
        return " ".join([N(r, 0.75, "!"), N(o, 0.25), N(f5, 0.75), N(r, 0.25, ","), N(M3 + 12 if "m" not in ch[1:3] else m3 + 12, 0.75), N(f5, 0.25), N(o, 0.75), N(ap, 0.25)])
    raise ValueError(style)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "スイッチ": SL.bar(b, slap_bar(b, "riff") if i % 2 == 0 else slap_bar(b, "riff2")); continue
    if n in ("洗う", "すすぐ"): SL.bar(b, slap_bar(b, "riff" if i % 4 < 2 else "riff2") if not (i % 8 == 7) else slap_bar(b, "riff2")); continue
    if n == "泡": SL.bar(b, slap_bar(b, "foam")); continue
    if n == "脱水": SL.bar(b, slap_bar(b, "spin") if i < 22 else ("E2:0.25! E3:0.25 E2:0.25 E3:0.25 " * 4).strip() if i == 22 else "E1:1! R:3"); continue
    if n == "干す": SL.bar(b, slap_bar(b, "hang")); continue
    if n == "風":
        if i == 2: SL.bar(b, "E4:6")     # ベースのハーモニクスの1音（高い所で鳴らす）

# ---------- 歌の役（弦）: しゃくり上げる長い音と、跳ねる句 ----------
WA = ["R:1 5:0.5 6:0.5 1':1/ 6:1", "5:2 R:2", "R:1 5:0.5 6:0.5 2':1/ 1':1", "6:2 R:2", "R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:1", "4:2 5:2", "6:1.5 5:0.5 3:1 2:1", "2:3 R:1",
      "R:1 5:0.5 6:0.5 1':1/ 6:1", "5:2 R:1 3':1/", "2':1.5 1':0.5 b7:1 6:1", "5:2 R:2", "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "1':2 b7:2", "6:1 5:1 3:1 5:1", "4:4"]
RI = ["R:1 1':0.5 2':0.5 3':1/ 1':1", "6:2 R:2", "R:1 1':0.5 2':0.5 5':1/ 3':1", "2':2 R:2", "R:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "2':2 R:2", "1':1.5 7:0.5 5:1 3:1", "b7:3 R:1"]
for i, b in enumerate(S.sc("洗う")):
    if i >= 8: STRL.bar(b, K.mel(WA[i - 8], oct=4))
for i, b in enumerate(S.sc("すすぐ")):
    STRL.bar(b, K.mel((WA[:8] if i < 8 else RI + RI)[i % 16 if i >= 8 else i], oct=4) if i < 8 else K.mel(RI[(i - 8) % 8], oct=4))
FO = ["5':4/", "4':4", "3':3 2':1", "2':4", "1':4/", "2':4", "b7:2 1':2", "2':4"]
for i, b in enumerate(S.sc("泡")):
    if i >= 8: STRL.bar(b, K.mel(FO[i - 8], oct=4))
SPINM = ["1':0.5 2':0.5 3':0.5 5':0.5 3':0.5 2':0.5 1':1", "b7:0.5 1':0.5 2':0.5 4':0.5 2':0.5 1':0.5 b7:1", "6:0.5 b7:0.5 1':0.5 3':0.5 1':0.5 b7:0.5 6:1", "5:2 6:1 7:1"]
for i, b in enumerate(S.sc("脱水")):
    if i < 22: STRL.bar(b, K.mel(SPINM[i % 4], oct=4 if i < 12 else 5))
HA = ["3:1.5 5:0.5 6:2/", "5:1.5 3:0.5 2:2", "1:1.5 2:0.5 3:2", "5,:4", "6,:0.75 1:0.25 3:1 6:1.5 5:0.5", "4:2 2:2", "3:1.5 1:0.5 6,:2", "1:3 R:1"]
for i, b in enumerate(S.sc("干す")):
    if i >= 4: STRL.bar(b, K.mel(HA[(i - 4) % 8] if i < 20 else seq_up(HA[(i - 4) % 8], K, 2), oct=5))

# ---------- 伴奏: 弦の和音・エレピの刻み・パッド ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 64, 3)
    if n in ("洗う", "すすぐ"):
        pat = "R:0.5 X:0.25 R:0.75 X:0.5 R:0.5 X:0.25 R:0.75 X:0.5" if i % 2 == 0 else "R:0.5 X:0.25 R:0.25 X:0.5 R:0.5 X:0.5 R:0.5 X:0.25 X:0.75"
        for j in range(3): EP[j].bar(b, pat.replace("X", nm(v[j])))
    if n == "脱水":
        for j in range(3): EP[j].bar(b, "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5".replace("X", nm(v[j])))
    if n == "干す":
        for j in range(3): EP[j].bar(b, "R:0.75 X:0.25 R:0.75 X:0.25 R:0.75 X:0.25 R:0.75 X:0.25".replace("X", nm(v[j])))
    sv = voice(S.chords[b], 70, 2)
    if n in ("洗う", "すすぐ", "干す") and not (n == "洗う" and i < 8):
        for j in range(2): STRH[j].bar(b, f"{nm(sv[j])}:4")
    if n in ("泡", "風") or (n == "スイッチ" and False):
        pv = voice(S.chords[b], 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
for i, b in enumerate(S.sc("脱水")):
    if i < 22:
        t = tones(S.chords[b], "E5", "E7")
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in [0, 1, 2, 3, 2, 3, 1, 2]) if i >= 8 else "R:4")
riser(FX, b_spin + 20, 8, "D4")
FX.bar(S.sc("風")[0], "A4:2 R:2")
cym_swell(CYM, S.sc("洗う")[0], 2, "C4"); cym_swell(CYM, S.sc("すすぐ")[0], 2, "C4"); cym_swell(CYM, b_spin, 2, "C4")
CYM.bar(S.sc("風")[0], "B4:16")

# ---------- ドラム（ディスコ: 4つ打ち・裏のオープンハット・2・4のスネア） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "スイッチ":
        if i >= 2: D.set(b, h="x.x.x.x.x.x.x.x.")
        continue
    if n in ("洗う", "すすぐ"):
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "x.O.x.O.x.O.x.O." if i >= 8 or n == "すすぐ" else "x.x.x.x.x.x.x.x."), ghosts=0.4, seed=b, hat_vary=False)
        if i in (0, 8, 16): crash(D, b, "C2" if i != 8 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if last else "small")
        continue
    if n == "泡":
        put_groove(D, b, ("X.......X.......", "........X.......", "..x...x...x...x."), seed=b, hat_vary=False)
        if i == 0: D.cym(b, "D2:4")
        if last: put_fill(D, b, "lift")
        continue
    if n == "脱水":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "x.O.x.O.x.O.x.O."), ghosts=0.4, seed=b, hat_vary=False)
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "G2")
        if i % 4 == 3: put_fill(D, b, "snare16" if i < 20 else "build")
        if i == 23: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 1)
        continue
    if n == "止まる": continue
    if n == "干す":
        # はねるリズム（付点）。キックは1・3、スネアは2・4、ハットは付点のはね
        put_groove(D, b, ("X.....x.X.......", "....X.......X..o", "X..xX..xX..xX..x"), ghosts=0.3, seed=b, hat_vary=False)
        if i in (0, 16): crash(D, b, "D2" if i == 0 else "C2")
        if i % 8 == 7: put_fill(D, b, "small" if i != 31 else "tomdown")
        continue
    if n == "風" and i < 2:
        D.set(b, "X..............." if i == 0 else "." * 16, "." * 16, "." * 16)

S.flags += " --space room --space-wet 0.12"
S.desc = ("仮: ボカロ曲のインスト25曲の07。ディスコ。E ミクソリディアン。テンポは 118 から脱水で 128 へ上がり、干す所で 100。主役の楽器はスラップベース（旋律を弾く）。"
          "晴れた日曜の洗濯。洗う・泡・すすぐ・脱水（だんだん速く回る）→ぴたりと止まる（2小節の無音）→物干しで風にゆれる（はねるリズム）。歌の役は弦で、しゃくり上げる。自作")
S.write()
