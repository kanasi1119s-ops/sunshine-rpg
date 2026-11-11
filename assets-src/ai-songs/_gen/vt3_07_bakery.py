# vt3 07「焼きたてのオーブン」Fresh Out of the Oven（仮）— ボサノバ・ハウス。122・4/4。A長調（転調なし）。
# 第3弾（0時〜24時の街）の 6時。表は docs/sound/vt3-plan.md。
# 物語: 町のパン屋の朝。まだ暗い店で、ゆうべ寝かせた生地がふくらんでいる。エプロンをしめた「わたし」は、
#   となりのラジオから流れる小さな鼻歌（1時の節）をまねしながら生地をこねる。オーブンの「チン」。いちばん最初のパンが焼ける。
#   学校へ行く子が窓をのぞいて手をふる。シャッターを開けると、光といっしょに、今日のはじまりを手わたす。
# 場面と強さ: タイマー（チン）→ イントロ（ナイロンギターのボサノバ・弱）→ Aメロ1（ささやく）→ Bメロ1 → サビ1（4つ打ちのハウスに入れかわる・中強）
#   → 間奏（フルート・節）→ Aメロ2 → Bメロ2 → サビ2 → 寝かせる（ギターと小鳥だけ・とても静か）→ 間奏2（ハウスのピアノとフルート）
#   → 最後のサビ（いちばん厚い）→ ドアベル
# 旋律の性格: ボサノバのささやく歌いまわし（句の頭を少し遅らせる）。サビはハウスの上で、1' からのくり返しでなめらかに上がる。A3〜F#5。
# この曲だけの音: Aメロはボサノバ（ナイロン弦とクロススティック）、サビで4つ打ちのハウスに入れかわる。オーブンの「チン」で始まり、ドアベルで終わる。
#   合いことばの節（3・5・6・5・2）は、間奏のフルートに1回（C#・E・F#・E・B）。
from vt25_lib import *

S = Song("07", "bakery", "焼きたてのオーブン（仮）", "Fresh Out of the Oven", 122, 4, "A", "major", "ボサノバ・ハウス（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
K = Key("A", "major")          # oct 3 で 1 = A3

INTRO = ["Amaj7", "Dmaj7", "Amaj7", "Dmaj7"]
A_CH = ["Amaj7", "C#m7", "Dmaj7", "Dm6", "Amaj7", "F#m9", "Bm7", "E7b9"]
B_CH = ["Dmaj7", "C#m7", "F#m9", "Bm7", "Dmaj7", "C#m7", "Bm7", "E7sus4"]
C_CH = ["F#m9", "Dmaj9", "Amaj9", "E9", "F#m9", "Dmaj9", "Bm9", "E7sus4"]

S.scene("タイマー", 2, "intro", ["Amaj7", "Amaj7"])
S.scene("イントロ", 8, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", INTRO)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("寝かせる", 8, "bridge", ["Dmaj7", "C#m7", "Bm7", "Amaj7", "Dmaj7", "C#m7", "Bm7", "E7sus4"])
S.scene("間奏2", 8, "solo", C_CH)
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("ドアベル", 4, "outro", ["F#m9", "Dmaj9", "Amaj9", "Amaj9"])

V = Voice(S, vol=0.2, delay=0.75, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
NYL = [S.track(f"ナイロンギター{i + 1}", "guitar", patch="nylonGuitar", amp="crystal", volume=0.07, pan=-0.35, reverb=0.25, chorus=0, sustain=1.0) for i in range(4)]
PN = [S.track(f"ハウスのピアノ{i + 1}", "piano", volume=0.07, pan=0.3, reverb=0.25, fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 400, "high": 0}]) for i in range(3)]
FL = S.track("電子のサックス（旋律）", "lead", patch="kfbFutureSax", volume=0.085, pan=0.1, reverb=0.3, mono=True)   # v2: フルートの音は使わない（人間・2026-11-11）→ 電子のリードに
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("fbChord", vol=0.014, pan=-0.5 + 0.5 * i, duck=0.4, sustain=1.5)) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.22))
BELL = S.track("オーブンとドアベル", "glockenspiel", volume=0.06, pan=0.3, reverb=0.4)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.75 2:0.25 3:1 5:1", "4:1.5 3:0.5 2:1 R:1", "R:0.5 2:0.5 2:0.75 1:0.25 2:1 4:1", "3:1.5 2:0.5 1:1 R:1",
      "R:0.5 5:0.5 5:0.75 4:0.25 5:1 1':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 4:0.5 3:0.5 2:0.5 3:1 2:1", "2:2 R:2"]
A1 = ("まだくらいみせで/こむぎこのにおい/ゆうべのきじがね/ふくらんでる/"
      "おーぶんのまえで/えぷろんしめたら/はりがろくじへと/あとすこしね")
A2 = "となりのらじおが/けさもながれてる/ちいさなはなうた/まねてこねる"
VB = ["R:0.5 6:0.5 6:0.5 5:0.5 6:1 1':1", "7:1 6:1 5:1 R:1", "R:0.5 5:0.5 5:0.5 4:0.5 5:1 7:1", "6:1 5:1 4:1 R:1",
      "R:0.5 4:0.5 5:0.5 6:0.5 1':1 2':1", "3':2 2':1 R:1", "R:0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 7:0.5", "2':3 R:1"]
B1 = "いちばんさいしょの/ぱんがやけるまで/まだねむるまち/においでおこそう"
B2 = "がっこうへいくこが/まどをのぞいてく/てをふってくれた/それだけでわらう"
VC = ["R:0.5 1':0.5 1':0.5 1':0.5 3':1 2':1", "1':1.5 6:0.5 6:1 R:1", "R:0.5 6:0.5 6:0.5 6:0.5 1':1 7:1", "5:2 R:2",
      "R:0.5 1':0.5 1':0.5 1':0.5 4':1 3':1", "2':1.5 1':0.5 2':1 R:1", "R:0.5 7:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "1':2 R:2",
      "R:0.5 3':0.5 3':0.5 4':0.5 5':1 4':1", "3':1.5 1':0.5 1':1 R:1", "R:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "2':2 R:2",
      "R:0.5 1':0.5 3':0.5 5':0.5 6':1 5':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 2':0.5 3':0.5 2':0.5 1':1 7:0.5 1':0.5", "1':3 R:1"]
C1 = ("やきたてのあさを/どうぞどうぞ/ふわっとあまいゆげ/まちにひろがれ/"
      "しゃったーをあけたら/ひかりのかご/きょうのはじまりを/てわたすんだよ")
C2 = ("やきたてのあさを/ひとつどうぞ/ちいさなてのひら/ぬくもりのせて/"
      "いつものことばを/いってらっしゃいね/きょうのはじまりを/てわたすんだよ")
C3 = ("やきたてのあさを/どうぞどうぞ/はなうたまぜこみ/ふっくらやけたよ/"
      "しゃったーをあけたら/ひかりのかご/きょうのはじまりを/てわたすんだよ")
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC, C3)

# ================= ギター・ピアノ・パッド =================
def bossa(b, ch):
    """ボサノバの刻み（親指は根音と5度、ほかの指は少し前に食う和音）"""
    v = voice(ch, 62, 3); r = low(ch, "E2")
    NYL[0].bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:1 {nm(r)}:1.5")
    # v2: 毎小節同じ型をやめ、2小節でひとまとまりのボサノバの型にする（2小節目は裏から入る）
    for j in range(3): NYL[j + 1].bar(b, f"{nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.75 {nm(v[j])}:0.75 R:0.5 {nm(v[j])}:1" if b % 2 == 0 else f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.75 R:0.25 {nm(v[j])}:0.5 {nm(v[j])}:1")


def house_piano(b, ch):
    # v2: ハウスの区間が 6.0〜6.4（ピアノ4声の細かい刻み＋パッド＋ボサノバのギターが同時に鳴り、高い音も強すぎた）
    #     → ピアノは3声で刻みを少なく、高い音を持ち上げない
    v = voice(ch, 64, 3)
    for j in range(3): PN[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1 R:0.5 {nm(v[j])}:0.5 R:0.5")


def pad(b, ch, c=62):
    v = voice(ch, c, 3)
    for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")


MOTIF = "R:1 C#5:0.5 E5:0.5 F#5:1 E5:0.5 B4:0.5"     # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "タイマー":
        if i == 1: bossa(b, ch)
    elif n in ("イントロ", "Aメロ1", "Aメロ2", "Bメロ1", "Bメロ2"):
        bossa(b, ch)
        if n in ("Bメロ1", "Bメロ2"): pad(b, ch)
        if n == "イントロ" and i >= 4: FL.bar(b, ["R:1 E5:1 C#5:1 B4:1", "A4:3 R:1", "R:1 F#5:1 E5:1 C#5:1", "B4:3 R:1"][i - 4])
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"):
        house_piano(b, ch)
        if n == "最後のサビ" and i >= 8: pad(b, ch, 64); bossa(b, ch)      # v2: パッドとギターは最後のサビの後半だけ
        if n == "間奏2":
            SOLO = ["R:0.5 A5:0.5 F#5:0.5 E5:0.5 C#5:1 E5:1", "F#5:2 E5:1 R:1", "R:0.5 B5:0.5 A5:0.5 F#5:0.5 E5:1 C#5:1", "B4:3 R:1",
                    "R:0.5 C#6:0.5 B5:0.5 A5:0.5 F#5:1 E5:1", "D5:2 F#5:1 R:1", "R:0.5 E5:0.5 F#5:0.5 G#5:0.5 A5:1 B5:1", "B5:3 R:1"]
            FL.bar(b, SOLO[i])
    elif n == "間奏":
        bossa(b, ch)
        FL.bar(b, [MOTIF, "C#5:3 R:1", "R:1 E5:1 F#5:1 A5:1", "G#5:3 R:1", "R:1 F#5:1 E5:1 C#5:1", "B4:2 C#5:2", "R:1 E5:0.5 D5:0.5 C#5:1 B4:1", "A4:3 R:1"][i])
    elif n == "寝かせる":
        bossa(b, ch) if i % 2 == 0 else None
        if i >= 4: pad(b, ch, 60)
    elif n == "ドアベル":
        if i < 3: house_piano(b, ch); pad(b, ch, 64); bossa(b, ch)
        else:
            v = voice(ch, 62, 3)
            for j in range(3): NYL[j + 1].bar(b, f"{nm(v[j])}:3 R:1")

BELL.bar(S.sc("タイマー")[0], "E7:0.5 R:3.5")            # オーブンの「チン」
BELL.bar(S.sc("ドアベル")[3], "R:1 B6:0.5 G#6:0.5 E6:1 R:1")   # 店のドアベル
season(S, S.sc("寝かせる")[0], "小鳥", beats=32, vol=0.05, every=8)

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("Aメロ1", "Aメロ2", "Bメロ1", "Bメロ2", "間奏") or (n == "イントロ" and i >= 4):
        BASS.bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:0.5 {nm(r + 7)}:1.5 {nm(r)}:0.5")
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"):      # v3: 裏のオクターブ跳び（house）をやめ、根音と5度で歩く
        BASS.bar(b, f"{nm(r)}:1 {nm(r)}:0.5 {nm(r + 7)}:1 {nm(r + 7)}:0.5 {nm(r + 12 if i % 2 else r)}:1")
    elif n == "寝かせる" and i >= 4: BASS.bar(b, f"{nm(r)}:4")
    elif n == "ドアベル" and i < 3: BASS.bar(b, f"{nm(r)}:4")

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 4, "C4")
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4")

# ================= ドラム（ボサノバ → ハウス）=================
BK, BS, BH = "X..X....X..X....", "..x..x....x..x..", "x.x.x.x.x.x.x.x."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("イントロ", "Aメロ1", "Aメロ2", "Bメロ1", "Bメロ2", "間奏"):
        if n == "イントロ" and i < 4: continue
        vgroove(D, b, "beat8", ghosts=0.1, seed=b, k=BK, s=BS, h=BH)      # クロススティック風の軽いスネア
        if n in ("Bメロ1", "Bメロ2") and i == 6: put_fill(D, b, "build")
        if n in ("Bメロ1", "Bメロ2") and last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"):
        # v3: ピアノを薄くしても 6.3 のまま → 生ドラムでの4つ打ち＋裏のオープンハイハットが固く聞こえていた。
        #     キックは4つ打ちのまま、スネアは軽いクロススティック、ハイハットは閉じた8分（ボサノバの手ざわりを残す）
        vgroove(D, b, "beat8", ghosts=0.1, seed=b, k="X...X...X...X...", s="....x.......x..x", h="x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last and n not in ("最後のサビ",): put_fill(D, b, "snare16" if n != "間奏2" else "lift")
    elif n == "寝かせる":
        if i >= 6: vgroove(D, b, "beat8", ghosts=0.1, seed=b, k=BK, s=BS, h=BH)
        if last: put_fill(D, b, "build")
    elif n == "ドアベル":
        if i < 2: vgroove(D, b, "four", ghosts=0.2, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        if i == 2: crash(D, b, "C2", 8)

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の07（6時）。ボサノバ・ハウス。A長調・122。町のパン屋の朝、いちばん最初のパンが焼ける。"
          "Aメロはナイロンギターのボサノバ、サビは4つ打ちのハウスとピアノ。合いことばの節は間奏のフルート。オーブンの「チン」で始まり、ドアベルで終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.3}, special={"寝かせる": -0.6, "最後のサビ": 0.35, "ドアベル": -0.2})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午前6時・パン屋のオーブン・ボサノバ・ハウス）で直すこと:
#   電子の音: フルートの旋律を電子のサックス（kfbFutureSax）に、パッドをキックで凹むうねる和音（fbChord）に。最後のサビだけ、4小節ごとに短い矩形波のプラックが駆け下りる
#            （01 の駆け上がりとは逆向き・1オクターブ下から）。サビ2 から、低い所に丸いサブベース
#   ギター: ナイロンギターのボサノバの型を、2小節でひとまとまりに（2小節目は裏から入る）。強さを1音ずつ少し揺らす
#   歌: Aメロはウィスパー（まだ暗い店・小声）、Bメロはクリア、サビはキュート（焼きたて・明るい）、寝かせる（ブリッジ）はウィスパー。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
import random as _rnd
path = sys.argv[1]
run, sub = {}, {}
for q, b in enumerate(S.sc("最後のサビ")):
    ch = S.chords[b].split("|")[0].split("/")[0]; t = tones(ch, "E4", "A5")
    if q % 4 == 3 and len(t) >= 5: run[b] = "R:2 " + " ".join(f"{nm(t[-1 - (z % len(t))])}:0.25" for z in (0, 1, 2, 3, 2, 3, 4, 5))
for name in ("サビ2", "最後のサビ"):
    for b in S.sc(name): sub[b] = f"{nm(low(S.chords[b].split('|')[0], 'C1'))}:3.5 R:0.5"
parts = [pad_part(S, "プラック（駆け下りる）", "kfbSquarePluck", run, 0.045, pan=-0.3, reverb=0.25, fx=[{"type": "pingpong", "beats": 0.5, "mix": 0.18, "feedback": 0.3}]),
         pad_part(S, "サブベース", "kfbSub", sub, 0.028, instrument="bass", reverb=0, duck=0.5)]
add_parts(path, parts)
js = load(path); rr = _rnd.Random(6)        # ナイロンギター: 強さを1音ずつ揺らす（指で弾く人の、音ごとの強さのちがい）
for p in js["parts"]:
    if p.get("role", "").startswith("ナイロンギター"):
        p["notes"] = " ".join(t if t.startswith("R") or "%" in t else f"{t}%{int(84 + rr.uniform(-12, 10))}" for t in p["notes"].split())
save(path, js)
set_parts(path, "ベース（指", sustain=1.15)
# 測ると、サビ1 が Aメロと同じ大きさ、2番の Aメロ・Bメロが サビ2 と同じ、最後のサビがいちばん小さかった。出だしのタイマーは −30dB → 仕上げで場面ごとに直す
final_gain(path, {"タイマー": 8, "イントロ": 2, "サビ1": 1.0, "間奏": -0.5, "Aメロ2": -1.2, "Bメロ2": -0.8, "サビ2": 0.6, "最後のサビ": 2.0})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 20, "最後のサビ": 24, "bridge": 6, "outro": 0}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.6)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "cute", "bridge": "whisper"}, default="clear")
