# vt3 03「夜勤明けのカフェオレ」Café au Lait After the Night Shift（仮）— ネオソウル。84・4/4。D短調（転調なし）。
# 第3弾（0時〜24時の街）の 2時。表は docs/sound/vt3-plan.md。
# 物語: 病院の夜勤。午前2時、ナースコールが鳴りやんだ休けい室。紙コップのカフェオレが「コトン」と落ちる。
#   つけっぱなしのラジオから、さっきの鼻歌（1時のDJの節）がまだ頭の中で回っている。だれかの痛みに手を当ててきた手のひらに、
#   カフェオレのあたたかさが残る。「今日もよくがんばったね」と自分に言って、また廊下へもどる。
# 場面と強さ: 紙コップ（コトン・ローズの和音・弱）→ Aメロ1（ささやく・弱）→ Bメロ1 → サビ1（控えめな山）→ 間奏（ローズ・節が隠れる）
#   → Aメロ2 → Bメロ2 → サビ2 → ブリッジ（ナースコールが鳴りやむ・とても静か）→ 間奏2（ローズのソロ）
#   → 最後のサビ（いちばん厚い・12小節）→ アウトロ（ローズの和音1つ）
# 旋律の性格: もたれるリズム（16分の後ろ寄り）、ため息のように降りる句。D4〜E5。
# この曲だけの音: ネオソウルの「遅れて入る」スネアと、9th・11th の重い和音。紙コップが落ちる「コトン」で始まる。
#   合いことばの節（3・5・6・5・2）は、間奏のローズの右手に1回だけ（F長調として A・C・D・C・G）。
from vt25_lib import *

S = Song("03", "cafeaulait", "夜勤明けのカフェオレ（仮）", "Café au Lait After the Night Shift", 84, 4, "D", "minor", "ネオソウル（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.45
S.keepers = {"Aメロ1": "closed", "サビ2": "ride", "最後のサビ": "ride"}
K = Key("D", "minor")          # oct 4 で 1 = D4

INTRO = ["Dm9", "Bbmaj7", "Gm9", "A7#9"]
A_CH = ["Dm9", "Em7b5", "Fmaj7", "Gm9", "Dm9", "Bbmaj7", "Gm9", "A7#9"]
B_CH = ["Bbmaj7", "C", "Am7", "Dm9"]
C_CH = ["Gm9", "C9", "Fmaj7", "Bbmaj7", "Em7b5", "A7b9", "Dm9", "Dm9"]

S.scene("紙コップ", 4, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 4, "break", INTRO)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("ブリッジ", 8, "bridge", ["Bbmaj7", "Am7", "Gm9", "Fmaj7", "Bbmaj7", "Am7", "Gm9", "A7sus4"])
S.scene("間奏2", 4, "solo", INTRO)
S.scene("最後のサビ", 12, "chorus", C_CH + C_CH[4:8])
S.scene("アウトロ", 6, "outro", ["Dm9", "Bbmaj7", "Gm9", "Bbmaj7", "Dm9", "Dm9"])

V = Voice(S, vol=0.2, delay=0.75, bright=-0.2, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
RH = [S.track(f"ローズ（和音{i + 1}）", "keys", volume=0.075, pan=-0.2, reverb=0.25, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 1, "midHz": 600, "high": -1}]) for i in range(4)]
RL = S.track("ローズ（左手）", "keys", volume=0.08, pan=-0.2, reverb=0.25, sustain=0.9, fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 600, "high": -1}])
RM = S.track("ローズ（右手の節）", "keys", volume=0.1, pan=-0.1, reverb=0.28, sustain=0.8, fx=[{"type": "eq", "low": -3, "mid": 1, "midHz": 800, "high": 0}])
GT = S.track("ギター（オブリ）", "guitar", amp="crystal", volume=0.06, pan=0.5, reverb=0.32, chorus=0, sustain=0.8)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=-0.5 + 0.5 * i, reverb=0.45, sustain=1.6) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.22))
CUP = S.track("紙コップ（カホン）", "cajon", volume=0.08, pan=0.2, reverb=0.15)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.75 5:0.25 5:0.5 4:0.5 3:0.75 4:0.25 3:0.5 1:0.5", "2:1.5 R:2.5",
      "R:0.75 5:0.25 5:0.5 6:0.5 5:0.75 4:0.25 3:0.5 4:0.5", "5:1.5 R:2.5",
      "R:0.75 1':0.25 1':0.5 7:0.5 6:0.75 5:0.25 4:0.5 5:0.5", "6:1 5:0.5 4:1 R:1.5",
      "R:0.5 3:0.5 4:0.5 5:0.5 4:0.5 3:0.5 2:0.5 1:0.5", "2:2 R:2"]
A1 = "かみこっぷがおちる/やきんのきゅうけい/ろうかのあかりひとつ/ちいさなためいき/ねむるいきのおと/しずかにならんで/わたしのあしおとだけ/ろうかにひびくよ"
A2 = "つけっぱなしらじお/さっきのあのふしが/あたまのなかでまわる/くちずさんでみる"
VB = ["R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:1", "4:1.5 3:0.5 4:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 7:1", "6:2 5:1 R:1"]
B1 = "だれかのいたみを/てあてしてきた"
B2 = "よあけまではまだ/すこしとおいね"
VC = ["R:0.5 1':0.5 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 5:0.5", "6:1.5 5:0.5 4:1 R:1",
      "R:0.5 5:0.5 5:0.5 4:0.5 3:0.5 4:0.5 5:0.5 6:0.5", "5:2 R:2",
      "R:0.5 1':0.5 1':0.5 2':0.5 1':0.5 7:0.5 6:0.5 7:0.5", "1':1.5 7:0.5 6:1 R:1",
      "R:0.5 4:0.5 3:0.5 2:0.5 3:1 2:0.5 1:0.5", "1:3 R:1"]
C1 = "かふぇおれのあたたかさ/てのひらにのこる/きょうもよくがんばったね/じぶんにいうの"
C2 = "あまいゆげのむこうで/まちがねむってるの/だれかのあさのために/おきているんだ"
CL = "かふぇおれのあたたかさ/もうすこしだけね/あのふしをくちずさみ/またがんばれる/よあけまであとすこし/さあもどろうか"
VBR = ["R:1 5:1 4:0.5 3:0.5 3:1", "2:2 R:2", "R:1 6:1 5:0.5 4:0.5 4:1", "3:2 R:2",
       "R:1 1':1 7:0.5 6:0.5 6:1", "5:2 R:2", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 2':1", "1':3 R:1"]
CB = "なりやんだ/ろうかには/わたしだけ/ひといきつく"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("ブリッジ", VBR, CB)
put("最後のサビ", VC + VC[4:8], CL)

# ================= ローズ・ギター・弦 =================
def rhodes(b, ch, style):
    v = voice(ch, 62, 4)
    r = low(ch, "D2")
    if style == "long":
        pats = [f"{nm(x)}:4" for x in v]; RL.bar(b, f"{nm(r)}:4")
    elif style == "lay":      # 少し遅れて置く（もたれるノリ）
        pats = [f"R:0.25 {nm(x)}:1.5 R:0.5 {nm(x)}:0.75 R:0.25 {nm(x)}:0.75" for x in v]; RL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    else:                     # 16分の短い合いの手
        pats = [f"{nm(x)}:0.75 R:0.75 {nm(x)}:0.25 R:0.75 {nm(x)}:0.5 R:0.5 {nm(x)}:0.5" for x in v]; RL.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.5 {nm(r + 7)}:1")
    for j in range(4): RH[j].bar(b, pats[j])


def strings(b, ch, c=67):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


MOTIF = "R:1 A4:0.5 C5:0.5 D5:1 C5:0.5 G4:0.5"     # 合いことばの節（F長調で 3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "紙コップ":
        if i >= 1: rhodes(b, ch, "long")
    elif n in ("Aメロ1", "Aメロ2"):
        rhodes(b, ch, "lay")
        if n == "Aメロ2" and i % 2 == 1: GT.bar(b, "R:2.5 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "D4", "D5")[-3:]))
    elif n in ("Bメロ1", "Bメロ2"):
        rhodes(b, ch, "poke"); strings(b, ch, 65)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        rhodes(b, ch, "lay" if i % 2 == 0 else "poke"); strings(b, ch, 69)
        if i % 4 == 3: GT.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "A4", "A5")[:4]))
    elif n == "間奏":
        rhodes(b, ch, "poke")
        RM.bar(b, MOTIF if i == 1 else ("R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C5", "C6")[:4]) if i == 3 else "R:4"))
    elif n == "ブリッジ":
        rhodes(b, ch, "long")
        if i >= 4: strings(b, ch, 64)
    elif n == "間奏2":
        rhodes(b, ch, "lay"); strings(b, ch, 67)
        SOLO = ["R:0.5 A4:0.25 C5:0.25 D5:0.5 F5:0.5 E5:1 C5:1", "D5:1.5 Bb4:0.5 A4:1 R:1",
                "R:0.5 G4:0.25 Bb4:0.25 D5:0.5 F5:0.5 A5:1 G5:0.5 F5:0.5", "E5:1 C#5:1 E5:1 R:1"]
        RM.bar(b, SOLO[i])
    elif n == "アウトロ":
        if i < 5: rhodes(b, ch, "lay" if i < 4 else "long")
        else:
            v = voice(ch, 62, 4)
            for j in range(4): RH[j].bar(b, f"{nm(v[j])}:3 R:1")
            RL.bar(b, f"{nm(low(ch, 'D2'))}:3 R:1")
        if i < 4: strings(b, ch, 65)

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "紙コップ":
        if i >= 2: BASS.bar(b, f"{nm(r)}:3 R:1")
    elif n in ("Aメロ1", "Aメロ2", "間奏", "間奏2"): BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.25 R:0.75 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5")
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "push", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ"): BASS.bar(b, f"{nm(r)}:1 R:0.5 {nm(r)}:0.5 {nm(r + 7)}:0.75 {nm(r + 12)}:0.25 {nm(r + 10)}:0.5 {nm(r + 7)}:0.5")
    elif n == "ブリッジ" and i >= 4: BASS.bar(b, f"{nm(r)}:4")
    elif n == "アウトロ" and i < 5: BASS.bar(b, f"{nm(r)}:4")

# ================= 紙コップ・効果音 =================
CUP.bar(S.sc("紙コップ")[0], "D3:0.5 R:0.25 E3:0.25 R:3")
cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム（もたれるネオソウル）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "紙コップ":
        if i >= 2: D.set(b, "X.........X.....", "................", "x.x.x.x.x.x.x.x.")
    elif n in ("Aメロ1", "Aメロ2", "間奏", "間奏2"):
        vgroove(D, b, "boombap", ghosts=0.55, seed=b, k="X......x..X.....", s="....X.......X..o", h="x.x.x.xxx.x.x.x.")
        if last and n != "間奏2": put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "boombap", ghosts=0.5, seed=b, k="X.........X..x..", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "snare16")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "boombap", ghosts=0.5, seed=b, k="X......x..X..x..", s="....X.......X..o", h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "C2", 6 if n == "最後のサビ" else 4)
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last and n != "最後のサビ": put_fill(D, b, "tomdown")
    elif n == "ブリッジ":
        if i >= 4: D.set(b, "X.........X.....", "................", "x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n == "アウトロ":
        if i < 4: vgroove(D, b, "boombap", ghosts=0.4, seed=b, k="X.........X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.")

SIL.add(S.sc("Bメロ2")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の03（2時）。ネオソウル。D短調・84。病院の夜勤の休けい室で、紙コップのカフェオレを飲む。"
          "ローズのエレピ・指弾きのベース・もたれるドラム・ストリングス。合いことばの節は間奏のローズに1回。自作")
finish(S, LY, V, 0,
       fx=[{"type": "sat", "scenes": "*", "drive": 0.18}],
       level={"verse": -0.2}, special={"ブリッジ": -0.6, "最後のサビ": 0.35, "アウトロ": -0.3})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午前2時・病院の休けい室・ネオソウル）で直すこと:
#   ギター: 右に、ネオソウルの合いの手（2本の弦の重音。下の音から半音・全音すべり上がって入る）。Aメロ1 の前半は弾かない → 後半は2小節に1回 → 2番は毎小節の終わり
#           → サビは裏拍に重音を置く → 最後のサビは句の終わりに駆け下りる。ブリッジとローズのソロは弾かない。DI ギター（丸いフロントの音）・コーラスなし
#   電子の音（少しだけ）: 最後のサビの低い所に丸いサブベース、2小節に1回ガラスのエレピのきらめき。始まりと終わりにレコードのパチパチ（休けい室のラジオ）
#   歌: Aメロとブリッジはウィスパー（ささやく）、Bメロとサビはクリア。揺れは浅く。ハモリは最後のサビだけ
#   ベース: 同じ音を続ける所の穴をなくす
from vt3x_lib import *
path = sys.argv[1]
up_, lo_ = {}, {}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b].split("|")[0].split("/")[0]
    tn = tones(ch, "F4", "A5")
    if len(tn) < 4: continue
    a, c, e = tn[-1], tn[-2], tn[-3]; lowof = lambda x: max([y for y in tones(ch, "C4", "A5") if y < x - 2] or [x - 4])
    def dy(x, d, g=True, v=84):      # 重音1つ: 下からすべり上がって（装飾音）入る
        u = (f"{nm(x - 1)}:0.12%{v - 14} {nm(x)}:{d - 0.12:g}%{v}" if g else f"{nm(x)}:{d:g}%{v}"); l = (f"{nm(lowof(x) - 2)}:0.12%{v - 18} {nm(lowof(x))}:{d - 0.12:g}%{v - 6}" if g else f"{nm(lowof(x))}:{d:g}%{v - 6}")
        return u, l
    def put(seq):
        us, ls = [], []
        for it in seq:
            if isinstance(it, (int, float)): us.append(f"R:{it:g}"); ls.append(f"R:{it:g}")
            else: us.append(it[0]); ls.append(it[1])
        up_[b] = " ".join(us); lo_[b] = " ".join(ls)
    if n == "Aメロ1" and i >= 8 and i % 2 == 1: put([2.5, dy(c, 0.5, v=74), dy(a, 1.0, False, 70)])
    elif n == "Aメロ2": put([2.5, dy(c, 0.5, v=78), dy(a, 1.0, False, 74)] if i % 2 == 1 else [3.0, dy(e, 1.0, v=72)])
    elif n in ("Bメロ1", "Bメロ2"): put([1.5, dy(e, 1.0, v=76), 0.5, dy(c, 1.0, v=80)])
    elif n in ("サビ1", "サビ2"): put([1.5, dy(c, 0.5, v=84), 1.0, dy(a if i % 2 == 0 else e, 1.0, v=86)] if i % 4 != 3 else [2.0, dy(a, 0.5, v=88), dy(c, 0.5, False, 82), dy(e, 1.0, False, 80)])
    elif n == "最後のサビ": put([0.5, dy(e, 0.5, v=84), 0.5, dy(c, 0.5, v=88), 1.0, dy(a, 1.0, v=90)] if i % 4 != 3 else [2.0, dy(a, 0.5, v=92), dy(c, 0.5, False, 86), dy(e, 0.5, False, 82), dy(lowof(e), 0.5, False, 78)])
parts = [line_part(S, "Rギター（合いの手・上）", "soul_clean", 0.5, 0.06, up_, seed=3, jitter=0.015), line_part(S, "Rギター（合いの手・下）", "soul_clean", 0.5, 0.05, lo_, seed=8, jitter=0.015)]
sub, spk = {}, {}
for q, b in enumerate(S.sc("最後のサビ")):
    ch = S.chords[b].split("|")[0]; sub[b] = f"{nm(low(ch, 'C1'))}:3.5 R:0.5"
    if q % 2 == 0: t = tones(ch.split("/")[0], "A5", "A6"); spk[b] = f"{nm(t[-1])}:1 R:0.5 {nm(t[-2])}:0.5 R:2" if len(t) >= 2 else "R:4"
parts += [pad_part(S, "サブベース", "kfbSub", sub, 0.028, instrument="bass", reverb=0),
          pad_part(S, "ガラスのエレピ（きらめき）", "kfbGlassEp", spk, 0.045, pan=0.3, reverb=0.4),
          pad_part(S, "レコードのパチパチ", "kawaiiFx", {S.sc("紙コップ")[0]: "A#5:12 R:4", S.sc("アウトロ")[0]: "A#5:12 A#5:12"}, 0.035, reverb=0.05, modulate=False, instrument="guitar")]
add_parts(path, parts, drop=lambda p: p.get("role", "").startswith("ギター（オブリ）"))
set_parts(path, "ベース", sustain=1.15)
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=4))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 20, "最後のサビ": 24, "bridge": 6, "outro": 0}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.5, auto=0.7, breaths=0.7)
    harmony(path, S, [("最後のサビ", 0, None, K)], vol=0.34)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "bridge": "whisper", "outro": "whisper"}, default="clear")
