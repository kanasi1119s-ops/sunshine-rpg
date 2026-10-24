# vp25 11「遠足のしおり」The Field Trip Itinerary（仮）— ロック（ポップパンク寄り）。B長調・182・4/4。主役の楽器: オカリナ
# 物語: 小学校の遠足。しおりの時刻表のとおり、8時に集合（点呼）、バスで出発、車内でみんなの歌、山道を登って、山頂でお弁当。
#   帰りのバスでは、はしゃぎ疲れてだんだん眠くなり、みんな寝てしまう。
# 形: しおりの時刻表のとおり: 集合→バス→バスの中の歌→山道→山頂でお弁当→帰りのバス→眠る
# 場面と強さ: 集合＝ざわざわ（オカリナの点呼に、みんなが答える）／バス＝一定の走り／山頂＝最大の開放／帰り＝だんだん眠く小さく、フェードアウト
# 旋律の性格: 点呼のような短い呼びかけと答え。帰りは同じ呼びかけが子守歌に変わる（音が長く、低く）
# 崩す所: 最後の4分の1は、速さを落とさずに音だけ小さくする（眠気。テンポは走ったまま、楽器が1つずつ寝ていく）
from vp25_lib import *

S = Song("11", "ensoku", "遠足のしおり（仮）", "The Field Trip Itinerary", 182, 4, "B", "major", "ロック（ポップパンク）")
S.kit = "naked"
K = S.key
GATHER = ["B", "E", "F#", "B"]
BUS = ["B", "D#m", "E", "F#", "G#m", "E", "C#m7", "F#sus4"]
SONG = ["E", "F#", "D#m", "G#m", "C#m", "F#", "B", "B"]
TRAIL = ["G#m", "F#", "E", "D#7"]
TOP = ["B", "B/A", "E/G#", "Em/G", "B/F#", "G#m7", "C#m7", "F#7"]
HOME = ["B", "G#m", "E", "F#"]
SLEEP = ["E", "B/D#", "C#m7", "F#sus4"]
S.scene("集合", 16, "intro", GATHER)
S.scene("バス", 32, "verse", BUS)
S.scene("バスの歌", 24, "pre", SONG)
S.scene("山道", 24, "bridge", TRAIL)
S.scene("山頂", 40, "chorus", TOP)
S.scene("帰りのバス", 32, "verse", HOME)
S.scene("眠る", 24, "outro", SLEEP)
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud " + S.flags

# 帰り道の眠気: 小節ごとの音量（帰りのバスの後半から、だんだん小さく）
SLEEPY = []
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = 1.0
    if n == "帰りのバス": v = 1.0 - 0.35 * max(0, i - 8) / 24
    if n == "眠る": v = 0.65 - 0.45 * i / L
    SLEEPY.append(round(v, 3))

OC = S.track("主役: オカリナ（点呼）", "ocarina", volume=0.25, pan=-0.05, reverb=0.3, gainDb=5, phrase=4, mono=True,
             fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2000, "high": 0}])
LEAD = S.track("リード（歌の役・みんなの答え）", "lead", **lead_spec("squareLead", vol=0.18, pan=0.08, delay=0.5))
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.1, 0.0), barGain=SLEEPY) for i in range(3)]
CL = [S.track(f"クリーンのギター{i + 1}", "guitar", **clean_gtr_spec(0.09, [0.45, 0.55][i]), barGain=SLEEPY) for i in range(2)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2), barGain=SLEEPY)
GLK = S.track("鉄琴（お弁当のきらめき）", "glockenspiel", patch="glockenspiel", volume=0.1, pan=0.4, reverb=0.35, sustain=1.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
S.drum_gain = {k: {"barGain": SLEEPY} for k in ("kick", "snare", "hihat", "tom", "crash")}

# ---------- 点呼（呼びかけと答え） ----------
CALL = ["1:0.5 1:0.5 3:1 R:2", "R:4", "5:0.5 5:0.5 1':1 R:2", "R:4"]          # オカリナ「はーい、そろった？」
ANSW = ["R:4", "R:1 3:0.5 3:0.5 5:1 R:1", "R:4", "R:1 5:0.5 6:0.5 1':1 R:1"]  # みんな「はーい！」
for i, b in enumerate(S.sc("集合")):
    OC.bar(b, K.mel(CALL[i % 4] if i < 12 else ["1':0.5 1':0.5 3':1 R:2", "R:4", "5':0.5 5':0.5 1'':1 R:2", "R:4"][i % 4], oct=4))
    if i >= 4: LEAD.bar(b, K.mel(ANSW[i % 4], oct=4))
# バス: 歌の役が一定の走りの旋律、オカリナは4小節ごとに「点呼」の断片
BM = ["5:1 5:0.5 6:0.5 5:1 3:1", "4:1 4:0.5 5:0.5 4:1 2:1", "3:1 3:0.5 4:0.5 3:1 1:0.5 2:0.5", "3:3 R:1",
      "6:1 6:0.5 7:0.5 1':1 6:1", "5:1 5:0.5 6:0.5 5:1 3:1", "4:1 6:0.5 5:0.5 4:1 3:1", "2:3 R:1"]
BM2 = ["1':1 1':0.5 2':0.5 1':1 5:1", "6:1 6:0.5 7:0.5 1':1 3':1", "2':1 2':0.5 3':0.5 2':1 7:1", "1':3 R:1",
       "3':1 3':0.5 2':0.5 1':1 6:1", "1':1 7:0.5 6:0.5 5:1 3:1", "4:1 5:0.5 6:0.5 7:1 2':1", "#4':2 R:2"]
for i, b in enumerate(S.sc("バス")):
    if i < 4: continue
    LEAD.bar(b, K.mel((BM if (i - 4) % 16 < 8 else BM2)[(i - 4) % 8], oct=4))
    if i % 8 == 3: OC.bar(b, K.mel("R:2 1':0.5 1':0.5 3':1", oct=4))
# バスの中の歌: オカリナが主役で歌う（みんなは手拍子）
SG = ["3:1 5:1 6:1 5:1", "4:2 3:2", "2:1 4:1 6:1 5:1", "4:4", "3:1 5:1 1':1 7:1", "6:2 5:2", "4:1 3:1 2:1 3:1", "1:4"]
for i, b in enumerate(S.sc("バスの歌")): OC.bar(b, K.mel(SG[i % 8] if i < 16 else seq_up(SG[i % 8], K, 2), oct=4 if i < 8 else 5))
# 山道: 一歩ずつ（リード、低めから上る）
TM = ["1:2 2:2", "3:2 4:2", "5:3 4:1", "3:4", "2:2 3:2", "4:2 5:2", "6:3 5:1", "#4:4"]
for i, b in enumerate(S.sc("山道")): LEAD.bar(b, K.mel(TM[i % 8], oct=4 if i < 16 else 5))
# 山頂: いちばん開放（リード＋オカリナの重ね）
TP = ["5':2 4':1 3':1", "4':3 R:1", "3':1 4':1 5':1 6':1", "5':4", "4':2 3':1 2':1", "3':2 1':2", "2':1 3':1 4':1 2':1", "1':3 R:1",
      "5':2 6':1 7':1", "1'':3 7':1", "6':1 5':1 4':1 3':1", "4':4", "5':1 4':1 3':1 4':1", "5':2 1':2", "2':1 4':1 6':1 7':1", "1'':4"]
for i, b in enumerate(S.sc("山頂")):
    if i < 8: OC.bar(b, K.mel(TP[i], oct=4)); continue
    LEAD.bar(b, K.mel(TP[i % 16], oct=4))
    if i >= 24: OC.bar(b, K.mel(TP[i % 16], oct=3))
# 帰りのバス: 行きのバスの旋律を、音を長く
for i, b in enumerate(S.sc("帰りのバス")):
    if i < 16: LEAD.bar(b, K.mel(BM[i % 8], oct=4))
    elif i < 24: OC.bar(b, K.mel(["5:2 3:2", "4:2 2:2", "3:2 1:2", "3:4", "6:2 1':2", "5:2 3:2", "4:2 3:2", "2:4"][i - 16], oct=4))
# 眠る: 点呼の子守歌（長く、低く）
LULL = ["1:2 1:2", "3:4", "5:2 5:2", "1':4", "6:2 5:2", "4:4", "3:2 2:2", "1:4"]
for i, b in enumerate(S.sc("眠る")):
    if i < 16: OC.bar(b, K.mel(LULL[i % 8], oct=4))
    elif i == 16: OC.bar(b, K.mel("1:4", oct=4))

# ---------- ギター ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    pw = power(S.chords[b], "E2")
    if n == "集合":
        if i < 4: continue
        pat = "X:0.5! R:1.5 X:0.5! R:1.5" if i < 12 else " ".join("X:0.5" for _ in range(8))
    elif n in ("バス", "山頂"): pat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
    elif n == "バスの歌": pat = "X:1! X:1 X:1! X:1"
    elif n == "山道": pat = "X:2! X:1.5 X:0.5"
    elif n == "帰りのバス": pat = " ".join("X:0.5" for _ in range(8)) if i < 16 else "X:2 X:2"
    else: continue
    for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))
for b in S.sc("バスの歌") + S.sc("帰りのバス")[16:] + S.sc("眠る")[:20]:
    v = voice(S.chords[b], 64, 2)
    for j in range(2): CL[j].bar(b, f"{nm(v[j])}:1 {nm(v[1 - j])}:1 {nm(v[j])}:1 {nm(v[1 - j])}:1")
# お弁当のきらめき
for i, b in enumerate(S.sc("山頂")):
    if i % 4 == 0: GLK.bar(b, " ".join(f"{nm(m)}:0.5" for m in tones(S.chords[b], "B5", "B6")[:4]) + " R:2")

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n == "集合": BASS.bar(b, "R:4" if i < 4 else (f"{nm(r)}:0.5! R:1.5 {nm(r)}:0.5 R:1.5" if i < 12 else bass_line(S, b, "root8"))); continue
    if n in ("バス", "山頂"): BASS.bar(b, bass_line(S, b, "root8")); continue
    if n == "バスの歌": BASS.bar(b, bass_line(S, b, "walk")); continue
    if n == "山道": BASS.bar(b, bass_line(S, b, "half")); continue
    if n == "帰りのバス": BASS.bar(b, bass_line(S, b, "root8") if i < 16 else f"{nm(r)}:2 {nm(r + 7)}:2"); continue
    if n == "眠る" and i < 20: BASS.bar(b, f"{nm(r)}:4")

cym_swell(CYM, S.sc("山頂")[0], 2, "C4"); cym_swell(CYM, S.sc("バス")[0], 1, "C4")

# ---------- ドラム ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "集合":
        if i < 4: continue
        if i < 12: D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        else: put_groove(D, b, "drive", ghosts=0.3, seed=b, hat_vary=False)
        if last: put_fill(D, b, "snare16")
        continue
    if n == "バス":
        put_groove(D, b, ("X.....X.X.....X.", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        if i in (0, 16): crash(D, b)
        if i % 8 == 7: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        continue
    if n == "バスの歌":
        # 手拍子のような2・4拍（スネアの軽い音）とライド
        D.set(b, "X.......X.......", "....X.......X...", "." * 16)
        D.cym(b, "D2:1 D2:1 D2:1 D2:1")
        if i % 8 == 7: put_fill(D, b, "small")
        continue
    if n == "山道":
        put_groove(D, b, "half", ghosts=0.4, seed=b, hat_vary=False)
        D.cym(b, ("C2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "build")
        continue
    if n == "山頂":
        # ポップパンクの速い2ビート（キック表・スネア裏）と8ビートを交互に
        if (i // 8) % 2 == 1: D.set(b, "X...X...X...X...", "..X...X...X...X.", "X.x.X.x.X.x.X.x.")
        else: put_groove(D, b, "drive", ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        continue
    if n == "帰りのバス":
        put_groove(D, b, ("X.....X.X.....X.", "....X.......X...", "X.x.X.x.X.x.X.x.") if i < 16 else ("X.......X.......", "....X.......X...", "x...x...x...x..."), seed=b, hat_vary=False)
        if i == 0: crash(D, b, "D2")
        continue
    if n == "眠る" and i < 12:
        D.set(b, "X.......X......." if i < 8 else "X...............", "." * 16, "x...x...x...x...")

S.fade_out = 10
S.desc = ("仮: ボカロ曲のインスト25曲の11。ポップパンク寄りのロック。B長調・182。主役の楽器はオカリナ。小学校の遠足を、しおりの時刻表のとおりに。"
          "集合（オカリナの点呼にみんなが答える）→バス→バスの中の歌→山道→山頂でお弁当（いちばん開放、2ビート）→帰りのバス→眠る。"
          "最後の4分の1は、テンポを落とさずに音だけだんだん小さくなり、点呼の旋律が子守歌に変わる。自作")
S.write()
