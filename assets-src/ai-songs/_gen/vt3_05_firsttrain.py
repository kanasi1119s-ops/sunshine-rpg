# vt3 05「始発までのベンチ」Bench Before the First Train（仮）— シューゲイザー。92・4/4。D長調（転調なし）。
# 第3弾（0時〜24時の街）の 4時。表は docs/sound/vt3-plan.md。
# 物語: 終電をのがして、駅のベンチで朝を待つ「わたし」。ホームはしんとしていて、星がひとつだけ。
#   眠い目をこすると、東の空がすこしずつ白くなっていく。遠くで鳥の声。ふと、どこかで聞いた鼻歌（1時のラジオの節）を口ずさむ。
#   始発の電車が光をつれてやってくる。「おはよう」と言うために、家に帰ろう。
# 場面と強さ: チャイム（駅の2つの音）→ イントロ（逆再生のふくらみ・アルペジオ）→ 1番（声とアルペジオだけ・弱）
#   → サビ1（音の壁が半分）→ 間奏 → 2番（バンドが入る）→ サビ2 → 間奏2（音の壁）→ ブリッジ（鼻歌・とても弱い）
#   → 最後のサビ（音の壁がいちばん厚い・空が明るくなる）→ アウトロ（始発が入ってくる低い音と光）
# 旋律の性格: 遠くでつぶやくような、のばす音の多い旋律（A3〜F#5）。サビは 5 → 1' と上がって、長く浮かぶ。
# この曲だけの音: 明るく歪ませたギターを左右に何本も重ねた「音の壁」（シューゲイザー）。空の明るさに合わせて、だんだん厚くなる。
#   合いことばの節（3・5・6・5・2）は、ブリッジでテトが「らららら」と口ずさむ（BGM はエコーのギター）。
from vt25_lib import *

S = Song("05", "firsttrain", "始発までのベンチ（仮）", "Bench Before the First Train", 92, 4, "D", "major", "シューゲイザー（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space hall --space-wet 0.22"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
S.keepers = {"Aメロ2": "closed", "サビ2": "ride", "最後のサビ": "wash"}
K = Key("D", "major")          # oct 4 で 1 = D4

A_CH = ["Dmaj7", "Aadd9", "Bm7", "Gmaj7#11"]
B_CH = ["Em7", "F#m7", "Gmaj7", "Asus4"]
C_CH = ["Gmaj7", "Aadd9", "F#m7", "Bm7", "Gmaj7", "Aadd9", "Dmaj7", "Dmaj7"]

S.scene("チャイム", 2, "intro", ["Dmaj7", "Dmaj7"])
S.scene("イントロ", 12, "intro", ["Dmaj7", "Gmaj7#11"])
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 4, "break", ["Dmaj7", "Gmaj7#11"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("間奏2", 8, "solo", ["Dmaj7", "Gmaj7#11", "Bm7", "Aadd9"])
S.scene("ブリッジ", 4, "bridge", ["Em9", "Gmaj7", "Em9", "Asus4"])
S.scene("最後のサビ", 16, "chorus", C_CH + C_CH)
S.scene("アウトロ", 6, "outro", ["Dmaj7", "Gmaj7#11", "Dmaj7", "Gmaj7#11", "Dmaj7", "Dmaj7"])

V = Voice(S, vol=0.2, delay=0.75, bright=-0.2, patch="chiff", low=False)
WL = [S.track(f"音の壁 L{i + 1}", "distGuitar", amp="shoegaze", volume=0.032, pan=-0.75, reverb=0.6, chorus=0, sustain=0.9) for i in range(3)]
WR = [S.track(f"音の壁 R{i + 1}", "distGuitar", amp="shoegaze", volume=0.03, pan=0.75, reverb=0.6, chorus=0, sustain=0.9) for i in range(3)]
ARP = S.track("エコーのギター（アルペジオ）", "echoGuitar", amp="crystal", volume=0.07, pan=0.25, reverb=0.5, chorus=0, sustain=1.0,
              fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.35}])
SWL = [S.track(f"逆再生のふくらみ{i + 1}", "pad", **pad_spec("surgePadNeverending", vol=0.04, pan=-0.4 + 0.4 * i, duck=0.0, sustain=2.5)) for i in range(3)]
PAD = [S.track(f"響くパッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.035, pan=-0.5 + 0.5 * i, duck=0.2, sustain=2.0)) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.2))
CHIME = S.track("駅のチャイム（グロッケン）", "glockenspiel", volume=0.06, pan=0.0, reverb=0.6)
TRAIN = S.track("始発の音（低い一撃）", "impactHit", volume=0.08, pan=0, reverb=0.4)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.4)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 3:1 3:1 2:1", "1:3 R:1", "R:1 3:1 5:1 4:1", "3:3 R:1", "R:1 6:1 5:1 3:1", "2:3 R:1", "R:1 2:1 3:1 5:1", "5:2 6:1 R:1"]
A1 = "しゅうでん/のがした/べんちで/あさをまつ"
A2 = "まだよる/けれども/ひがしの/そらしろむ"
VB = ["R:1 5:1 6:1 1':1", "7:3 R:1", "R:1 6:1 7:1 2':1", "1':2 7:1 R:1"]
B1 = "ねむいめ/こすってみた"
B2 = "とおくで/とりのこえ"
VC = ["R:0.5 5:0.5 1':1 1':1 7:1", "6:2 5:1 R:1", "R:0.5 5:0.5 1':1 2':1 1':1", "3':3 R:1",
      "R:0.5 6:0.5 6:1 5:1 3:1", "5:2 6:1 R:1", "R:0.5 2:0.5 3:1 2:1 1:1", "1:3 R:1"]
C1 = "しらんでゆく/まちのそら/ひとりきりの/よるがとけ"
C2 = "しらんでゆく/わたしのめ/なきそうなの/まぶしくて"
C3 = "しらんでゆく/あおいそら/しはつがくる/ひかりつれ/しらんでゆく/ねむるまち/おはようとね/かえろうか"
HUM = ["R:2 3:0.5 5:0.5 6:1", "5:0.5 2:1.5 R:2", "R:2 3:0.5 5:0.5 6:1", "5:0.5 2:3.5"]   # 合いことばの節
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC + VC, C3)
if VOCAL: put("ブリッジ", HUM, "ららららら/ららららら")
else:
    for b, l in zip(S.sc("ブリッジ"), HUM): ARP.bar(b, K.mel(l, oct=5))

# ================= ギター・パッド =================
def wall(b, ch, amount):
    """音の壁: 左は根音・5度・オクターブ、右は中の和音（C3〜B4）。8分で弾き続ける（ジャジャジャジャ）。amount 1〜3 で本数を増やす"""
    pw = power(ch, "E2")
    r = low(ch, "C3"); up = [x for x in tones(ch, nm(r + 1), nm(r + 12))][:2]
    while len(up) < 2: up.append(r + 12)
    rv = [r] + up
    for j in range(amount):
        WL[j].bar(b, " ".join(f"{nm(pw[j])}:0.5" for _ in range(8)))
        WR[j].bar(b, " ".join(f"{nm(rv[j])}:0.5" for _ in range(8)))


def arp(b, ch, lo="D4", hi="D6"):
    t = tones(ch, lo, hi)
    seq = [t[q % len(t)] for q in (0, 2, 1, 3, 2, 4, 3, 5)]
    ARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in seq))


def pad(b, ch, tr=PAD, c=62):
    v = voice(ch, c, 3)
    for j in range(3): tr[j].bar(b, f"{nm(v[j])}:4")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "チャイム":
        CHIME.bar(b, "A5:1.5 F#5:2.5" if i == 0 else "A5:1.5 D5:2.5")
    elif n == "イントロ":
        pad(b, ch, SWL, 64)
        if i >= 4: arp(b, ch)
        if i >= 8: wall(b, ch, 1)
    elif n in ("Aメロ1", "Bメロ1"):
        arp(b, ch)
        if n == "Bメロ1": pad(b, ch)
    elif n == "サビ1":
        arp(b, ch, "D5", "D6"); wall(b, ch, 2); pad(b, ch)
    elif n == "間奏":
        arp(b, ch); pad(b, ch, SWL, 64); wall(b, ch, 1)
    elif n in ("Aメロ2", "Bメロ2"):
        arp(b, ch); wall(b, ch, 1 if n == "Aメロ2" else 2)
        if n == "Bメロ2": pad(b, ch)
    elif n == "サビ2":
        arp(b, ch, "D5", "D6"); wall(b, ch, 3); pad(b, ch)
    elif n == "間奏2":
        wall(b, ch, 3); pad(b, ch, SWL, 66)
        SOLO = ["R:1 F#5:1 A5:2", "G5:2 F#5:1 E5:1", "D5:3 R:1", "E5:1 F#5:1 A5:2", "B5:2 A5:1 F#5:1", "G5:3 R:1", "F#5:1 E5:1 D5:1 B4:1", "C#5:3 R:1"]
        ARP.bar(b, SOLO[i])
    elif n == "ブリッジ":
        pad(b, ch, SWL, 62)
    elif n == "最後のサビ":
        arp(b, ch, "D5", "D6"); wall(b, ch, 3); pad(b, ch, PAD, 64)
        if i >= 8: pad(b, ch, SWL, 69)
    elif n == "アウトロ":
        if i < 4: wall(b, ch, 3 - i // 2); pad(b, ch, SWL, 66); arp(b, ch, "D5", "D6")
        else: pad(b, ch, SWL, 66)

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("サビ1", "サビ2", "最後のサビ", "間奏2"): BASS.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(8)))
    elif n in ("Aメロ2", "Bメロ2", "間奏", "Bメロ1"): BASS.bar(b, f"{nm(r)}:2 {nm(r)}:1 {nm(r + 7)}:1")
    elif n == "イントロ" and i >= 8: BASS.bar(b, f"{nm(r)}:4")
    elif n == "アウトロ" and i < 5: BASS.bar(b, f"{nm(r)}:4")

# ================= 効果音（逆再生のシンバル・始発）=================
for name in ("サビ1", "サビ2", "最後のサビ", "間奏"): cym_swell(CYM, S.sc(name)[0], 4, "C4")
FX.bar(S.sc("アウトロ")[0], "D4:8")                 # 始発が近づく
TRAIN.bar(S.sc("アウトロ")[2], "A1:4")              # 電車がホームに入る低い音

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "イントロ":
        if i >= 8: D.set(b, "X.......X.......", "................", "x...x...x...x...")
        if i == 11: put_fill(D, b, "small")
    elif n == "Aメロ1":
        pass                                           # 声とアルペジオだけ
    elif n == "Bメロ1":
        D.set(b, "X.......X.......", "................", "x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.25, seed=b, k="X.......X.X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown")
        if last and n != "最後のサビ": put_fill(D, b, "small")
    elif n in ("間奏", "Aメロ2", "Bメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.......X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if n == "間奏" and i == 0: crash(D, b)
        if last and n == "Bメロ2": put_fill(D, b, "snare16")
        elif last: put_fill(D, b, "small")
    elif n == "間奏2":
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.......X.X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "C2", 6)
        if last: halt(D, b, 1)
    elif n == "アウトロ":
        if i < 4: vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.......X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "C2", 6)
        if i == 4: crash(D, b, "C2", 8)

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の05（4時）。シューゲイザー。D長調・92。終電をのがし、駅のベンチで始発を待つ。"
          "明るく歪ませたギターを左右に重ねた音の壁が、空の明るさに合わせて厚くなる。合いことばの節はブリッジの鼻歌。始発の低い音で終わる。自作")
finish(S, LY, V, 0,
       fx=[{"type": "width", "scenes": ["サビ2", "最後のサビ", "間奏2"], "mode": "wide", "amount": 0.4}],
       level={"verse": -0.3}, special={"Aメロ1": -0.5, "ブリッジ": -0.6, "最後のサビ": 0.4, "アウトロ": -0.2})
