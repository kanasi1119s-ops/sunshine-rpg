# vt3 18「夕焼けの交代式」Changing of the Sunset Guard（仮）— ゴスペル。70・12/8（4拍を3つずつに分けるゆっくりのノリ）。
# E♭長調 → サビ2は E（+1）→ 最後のサビは F（+2）。書き出しは全体を2半音下げる（テトの声に入れるため・D♭ → D → E♭）。
# 第3弾（0時〜24時の街）の 17時。表は docs/sound/vt3-plan.md。
# 物語: 夕方5時。一日じゅう空を照らした太陽が、肩の荷をおろして息をつく。東の空から、眠い目をこすった月が少し遅れてやって来る。
#   「ありがとう、またあす」「任せたよ、夜空を」。光のバトンを手渡すと、町の窓にひとつずつ明かりがともる。
#   聖歌隊が、街に流れていたあの5つの音を、ハミングで歌う。最後は「アーメン」の和音。
# 場面と強さ: オルガン（一音）→ イントロ（オルガンとピアノ）→ Aメロ1（太陽・語る・弱）→ Bメロ1 → サビ1（聖歌隊がこたえる・中強）
#   → 間奏 → Aメロ2（月）→ Bメロ2 → サビ2（+1）→ オルガンだけ（聖歌隊のハミング＝節・とても静か）→ 手拍子（ふくらむ）
#   → 最後のサビ（+2・いちばん強い）→ アーメン
# 旋律の性格: 大きくのびる旋律、3連の小さな飾り（こぶしのような回し）。サビは 1' を何度も伸ばす。
# この曲だけの音: ハモンドオルガン・ゴスペルのピアノ・聖歌隊（声の重ね）。3連のハイハット（ライド）と、2・4拍の手拍子。転調2回。
#   合いことばの節（3・5・6・5・2）は、聖歌隊のハミング。
from vt25_lib import *

S = Song("18", "sunset", "夕焼けの交代式（仮）", "Changing of the Sunset Guard", 70, 4, "Eb", "major", "ゴスペル（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
K = Key("Eb", "major"); K2 = Key("E", "major"); K3 = Key("F", "major")      # oct 4 で 1 = E♭4

A_CH = ["Ebmaj7", "Ab/Eb", "Ebmaj7", "Bb7sus4", "Cm7", "Fm7", "Bb7", "Eb"]
B_CH = ["Ab", "Bb", "Gm7", "C7"]
C_CH = ["Ab", "Eb/G", "Fm7", "Eb", "Ab", "Bb7", "Eb", "Eb"]

S.scene("オルガン", 2, "intro", ["Eb", "Eb"])
S.scene("イントロ", 4, "intro", ["Ab", "Eb/G", "Fm7", "Bb7sus4"])
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", ["Ab", "Bb", "Gm7", "Bb7"])
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 2, "break", ["Ab", "Bb7"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", ["Ab", "Bb", "C#m7", "B7"])                 # 最後は E への入り口
S.scene("サビ2", 8, "chorus", [tr_chord(c, 1) for c in C_CH])
S.scene("オルガンだけ", 4, "bridge", ["A", "E/G#", "F#m7", "B7sus4"])
S.scene("手拍子", 4, "break", ["A", "B", "G#m7", "C7"])                  # 最後は F への入り口
S.scene("最後のサビ", 12, "chorus", [tr_chord(c, 2) for c in C_CH + C_CH[:4]])
S.scene("アーメン", 4, "outro", ["Bb", "F", "Bb", "F"])

V = Voice(S, vol=0.2, delay=0.75, bright=-0.1, patch="surgePadBowed", low=False)
ORG = [S.track(f"ハモンドオルガン{i + 1}", "drawbarOrgan", volume=0.055, pan=-0.35, reverb=0.35, sustain=1.0) for i in range(3)]
PL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=0.15, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": 1}])
PR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.075, pan=0.15, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 2}]) for i in range(3)]
CH = [S.track(f"聖歌隊{i + 1}", "choir", volume=0.07, pan=-0.5 + 0.5 * i, reverb=0.5, sustain=1.5) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.22))
CLAP = S.track("手拍子", "pad", patch="seasonFx", volume=0.07, pan=0, reverb=0.25, modulate=False)
D = S.drumkit()
SIL = Silence(S)

T3 = "0.3333"
# ================= 歌 =================
VA = ["R:1 5:0.6667 6:0.3333 1':1 6:1", "5:2 3:0.6667 2:0.3333 1:1", "R:1 3:0.6667 5:0.3333 6:1 5:1", "3:3 R:1",
      "R:1 5:0.6667 6:0.3333 1':1 2':1", "1':2 6:0.6667 5:0.3333 6:1", "R:1 4:0.6667 3:0.3333 2:1 3:1", "1:3 R:1"]
A1 = "ゆうやけのそらで/たいようが/きょうのしごとおえ/いきをつく"
A2 = "ひがしのそらから/つきがくる/ねむいめをこすって/おくれたね"
VB = ["R:1 4:1 5:1 6:1", "1':2 6:1 R:1", "R:1 5:1 6:1 1':1", "2':3 R:1"]
B1 = "ありがとう/またあす"
B2 = "まかせたよ/よぞらを"
VC = ["1':1.5 6:0.5 5:1 6:1", "1':3 R:1", "2':1.5 1':0.5 6:1 5:1", "6:3 R:1",
      "1':1.5 6:0.5 5:1 3:1", "5:2 6:0.6667 5:0.3333 3:1", "R:1 2:0.6667 3:0.3333 5:1 6:1", "1':3 R:1"]
C1 = "こうたいだ/あかねいろ/ひかりのばとんを/てわたすよ"
C2 = "こうたいだ/あいいろへ/あかりがともるよ/ひとつずつ"
C3 = "こうたいだ/ありがとう/きょうもいちにちを/てらしたね/こうたいだ/おやすみと"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K2, VC, C2)
put("最後のサビ", K3, VC + VC[:4], C3)
if VOCAL: put("アーメン", K3, ["R:2 5:1 5:1", "6:2 5:2", "R:4", "R:4"], "あーめん")

# ================= オルガン・ピアノ・聖歌隊 =================
def organ(b, ch, c=62):
    v = voice(ch, c, 3)
    for j in range(3): ORG[j].bar(b, f"{nm(v[j])}:4")


def gospel_piano(b, ch):
    """左手は根音のオクターブ、右手は3連で和音をゆらす"""
    r = low(ch, "Eb2"); v = voice(ch, 65, 3)
    PL.bar(b, f"{nm(r)}:1 {nm(r + 12)}:0.6667 {nm(r)}:0.3333 {nm(r + 7)}:1 {nm(r + 12)}:1")
    for j in range(3): PR[j].bar(b, f"R:0.3333 {nm(v[j])}:0.3333 {nm(v[j])}:0.3333 R:0.3333 {nm(v[j])}:0.6667 R:0.3333 {nm(v[j])}:0.3333 {nm(v[j])}:0.3333 R:0.3333 {nm(v[j])}:0.6667")


def choir(b, ch, c=67, pat=None):
    v = voice(ch, c, 3)
    for j in range(3): CH[j].bar(b, (pat or "x:4").replace("x", nm(v[j])))


MOTIF = ["R:1 G4:0.6667 Bb4:0.3333 C5:1.5 Bb4:0.5", "F4:3 R:1"]     # 合いことばの節（E♭で 3・5・6・5・2）→ この場面は A なので +6 する
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "オルガン": organ(b, ch)
    elif n == "イントロ": organ(b, ch); gospel_piano(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        organ(b, ch, 60)
        if n == "Aメロ2" or i >= 4: gospel_piano(b, ch)
    elif n in ("Bメロ1", "Bメロ2"):
        organ(b, ch); gospel_piano(b, ch); choir(b, ch, 64)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        organ(b, ch); gospel_piano(b, ch)
        choir(b, ch, 67, "R:2 x:2" if i % 2 == 1 else "x:4")       # 句の終わりに聖歌隊がこたえる
    elif n == "間奏": organ(b, ch); gospel_piano(b, ch)
    elif n == "オルガンだけ":
        organ(b, ch, 60)
        if i < 2:
            m = " ".join(f"{nm(midi(t.split(':')[0]) + 6)}:{t.split(':')[1]}" if not t.startswith("R") else t for t in MOTIF[i].split())
            for j in range(3): CH[j].bar(b, shift_oct(m, 0) if j == 1 else ("R:4" if j == 0 else shift_oct(m, -1)))
    elif n == "手拍子":
        organ(b, ch); gospel_piano(b, ch); choir(b, ch, 64 + i)
    elif n == "アーメン":
        organ(b, ch, 62); choir(b, ch, 67, "x:4" if i < 3 else "x:3 R:1")
        if i < 3: gospel_piano(b, ch)
        else: PL.bar(b, f"{nm(low(ch, 'Eb2'))}:3 R:1")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("オルガン", "オルガンだけ"): continue
    if n == "Aメロ1" and i < 4: BASS.bar(b, f"{nm(r)}:4"); continue
    BASS.bar(b, f"{nm(r)}:1.6667 {nm(r)}:0.3333 {nm(r + 7)}:1 {nm(r + 12)}:0.6667 {nm(r + 10)}:0.3333")

# ================= 手拍子・ドラム（3連のライド）=================
RIDE3 = " ".join(["D2:0.3333"] * 12)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("オルガン", "オルガンだけ"): continue
    if n == "Aメロ1" and i < 4: continue
    if n == "アーメン":
        if i == 0: crash(D, b, "C2", 8); D.set(b, "X...............", "................", "................")
        continue
    D.set(b, "X.........X.....", "....X.......X...", "................")
    D.R.bar(b, RIDE3 if n in ("サビ1", "サビ2", "最後のサビ", "手拍子") else "D2:1 D2:0.6667 D2:0.3333 D2:1 D2:0.6667 D2:0.3333")
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 4 == 0: crash(D, b, "C2", 6)
    if last and n in ("Bメロ1", "Bメロ2", "手拍子", "サビ1", "Aメロ1", "Aメロ2"): put_fill(D, b, "tomtrip")
    if n in ("手拍子", "最後のサビ") or (n in ("サビ1", "サビ2") and i >= 4): CLAP.bar(b, "R:1 B4:1 R:1 B4:1")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の18（17時）。ゴスペル。E♭ → E → F（転調2回）・70の12/8。書き出しは全体を2半音下げる。"
          "太陽と月が空の当番を交代する。ハモンドオルガン・ゴスペルのピアノ・聖歌隊・3連のライドと手拍子。"
          "合いことばの節は聖歌隊のハミング。「アーメン」の和音で終わる。自作")
finish(S, LY, V, -2,
       level={"verse": -0.25}, special={"オルガンだけ": -0.5, "最後のサビ": 0.4, "アーメン": 0.1})
