# vt25 23「テールランプ・ホームタウン」Taillight Hometown（仮）— シンセウェイブ。108・4/4。A の短調（夜）→ 最後のサビと終わりは C 長調の明るい和音（朝）。
# 物語: 夜行バスの窓。街の灯りが遠ざかって、赤いテールランプが並ぶ夜道。上京して5年、がんばってきた、たぶんね。
#   眠れない夜に、イヤホンの歌を何度も聞く。窓の外に海のにおい、ふるさとが近づいてくる。トンネルを抜けたら、夜が明けていく。
#   朝の光が海を染めて、駅で待ってる母に「ただいま」。
# 場面と強さ: 夜の高速（8分のシンセのアルペジオ）→ Aメロ1 → Bメロ1 → サビ1 → 間奏 → Aメロ2 → Bメロ2 → サビ2
#   → サックスのソロ → トンネル（静か・パッドと歌だけ）→ 夜明け（パッドがふくらむ・小鳥）→ 最後のサビ（C 長調の明るい和音・いちばん強い）
#   → 終わり（朝・ベルと小鳥。「ただいま」）
# 旋律の性格: Aメロは8分で、窓の外をながめるように。サビは「3 → 5 → 6 → 1'」と上がって、最後は 5'（E5）まで。
# ほかの曲とちがう所: 80年代風のシンセ（のこぎり波のアルペジオ・8分のシンセベース・サックスのソロ）。夜の短調から、朝の長調の和音へ。
from vt25_lib import *

S = Song("23", "taillamp", "テールランプ・ホームタウン（仮）", "Taillight Hometown", 108, 4, "A", "minor", "シンセウェイブ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --space hall --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.drum_scale = 0.9
K = Key("A", "minor")           # oct 3 で 1 = A3（歌うのは A3〜E5）

A_CH = ["Am", "Fmaj7", "C", "G", "Am", "Fmaj7", "Em7", "G"]
B_CH = ["Dm7", "Em7", "Fmaj7", "G", "Dm7", "Em7", "Fmaj7", "Gsus4"]
C_CH = ["Fmaj7", "G", "Em7", "Am", "Dm7", "G", "Am", "Am"]
CM_CH = ["F", "G", "C", "Am", "F", "G", "C", "C"]               # 朝の和音（C 長調）
T_CH = ["Fmaj7", "Em7", "Dm7", "Am"]

S.scene("夜の高速", 8, "intro", A_CH)
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("サックスのソロ", 8, "solo", C_CH)
S.scene("トンネル", 8, "bridge", T_CH * 2)
S.scene("夜明け", 4, "break", ["Fmaj7", "G", "Gsus4", "G"])
S.scene("最後のサビ", 16, "chorus", CM_CH * 2)
S.scene("終わり", 12, "outro", ["C", "G/B", "Am", "F", "C", "G", "F", "C", "Fmaj7", "G", "Cmaj7", "Cmaj7"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
ARP = S.track("アルペジオ（のこぎり波）", "pad", patch="surgeRetroWave", volume=0.065, pan=-0.25, sustain=0.35, reverb=0.25,
              fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.045, pan=-0.4 + 0.4 * i, duck=0.3, sustain=1.8)) for i in range(3)]
SB = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.2, duck=0.3))
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.06, pan=0.2, reverb=0.35, sustain=1.0) for i in range(3)]
SAX = S.track("サックス", "brass", patch="altoSax", volume=0.14, pan=0.15, reverb=0.4, breath=True, attack=0.05, release=0.5, bright=-0.3,
              fx=[{"type": "plate", "mix": 0.15}])
BELL = S.track("ベル（朝）", "pad", patch="surgeFantasyBell", volume=0.05, pan=0.35, reverb=0.5, sustain=1.0)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.5) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 1':0.5 1':0.5 7:0.5 1':1 5:1", "5:1.5 4:0.5 3:1 R:1", "R:0.5 3:0.5 3:0.5 2:0.5 3:1 5:1", "4:1.5 3:0.5 2:1 R:1",
      "R:0.5 1':0.5 1':0.5 7:0.5 1':1 5:1", "6:1.5 5:0.5 3:1 R:1", "R:0.5 5:0.5 5:0.5 4:0.5 5:1 7:1", "7:2 R:2"]
A1 = "やこうばすのまど/まちがとおざかる/てーるらんぷがね/ならぶよみち"
A2 = "ねむれないよるに/いやほんのうたを/なんどもきいてる/ふるさとへと"
VB = ["R:1 4:0.5 4:0.5 4:0.5 3:0.5 4:1", "5:2 R:2", "R:1 6:0.5 6:0.5 6:0.5 5:0.5 6:1", "7:2 R:2",
      "R:1 1':0.5 1':0.5 1':0.5 7:0.5 1':1", "7:1 5:1 R:2", "R:1 6:1 1':1 3':1", "2':3 R:1"]
B1 = "じょうきょうして/もうごねんだ/がんばってきたよ/たぶんね"
B2 = "まどのそとに/うみのにおい/ちかづいてくる/ふるさと"
VC = ["R:0.5 3:0.5 5:0.5 6:0.5 1':1 7:1", "7:1.5 5:0.5 4:1 R:1", "R:0.5 5:0.5 7:0.5 1':0.5 2':1 7:1", "1':1.5 7:0.5 5:1 R:1",
      "R:0.5 4:0.5 6:0.5 1':0.5 3':1 2':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 5':1 3':1", "1':2 R:2"]
VCL = VC[:7] + ["3':2 R:2"]
C1 = "ひかりをおいかけ/よるをこえてゆく/ねむるまちのそら/かえるばしょへ"
C2 = "とおくなるまちも/ちかくなるまちも/どちらもわたしの/だいじなまち"
CL = C1 + "/あさのひかりがね/うみをそめてゆく/えきでまってるはは/ただいまだよ"
VT = ["R:1 3:0.5 3:0.5 4:0.5 4:0.5 5:1", "5:1.5 4:0.5 5:1 R:1", "R:1 4:0.5 4:0.5 3:0.5 3:0.5 2:1", "1:3 R:1"]
X1 = "とんねるぬけたら/よがあけてく/まぶしいひかりが/ほほをなでる"
VE = ["R:4", "R:4", "R:4", "R:4", "R:4", "R:4", "R:4", "R:4", "R:1 3':1 2':1 1':1", "7:4", "R:4", "R:4"]
E1 = "ただいま"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel):
        if m != "R:4": V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA, A1)
put("Bメロ1", VB, B1); put("Bメロ2", VB, B2)
put("サビ1", VC, C1); put("サビ2", VC, C2)
put("トンネル", VT * 2, X1)
put("最後のサビ", VC + VCL, CL)
put("終わり", VE, E1)
if VOCAL: put("Aメロ2", VA, A2)
else:                                           # 歌なしの版: 2番の Aメロはサックスが歌う
    for b, l in zip(S.sc("Aメロ2"), VA): SAX.bar(b, K.mel(l, oct=4))

# ================= サックスのソロ（サビの和音の上） =================
SOLO = ["R:0.5 E5:0.5 G5:0.5 A5:0.5 C6:1 B5:1", "G5:2 E5:1 D5:1", "R:0.5 E5:0.5 G5:0.5 B5:0.5 D6:1.5 B5:0.5", "C6:1 B5:0.5 A5:0.5 E5:2",
        "R:0.5 D5:0.5 F5:0.5 A5:0.5 C6:1 A5:1", "B5:1.5 A5:0.5 G5:1 D5:1", "E5:0.5 G5:0.5 A5:0.5 C6:0.5 E6:1 D6:1", "C6:1 B5:1 A5:2"]
for b, l in zip(S.sc("サックスのソロ"), SOLO): SAX.bar(b, l)

# ================= 伴奏 =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b].split("/")[0]; v = voice(ch, 64, 3, prev=prev); prev = v; pv = voice(ch, 57, 3); r = low(ch, "E1")
    t = tones(ch, "A3", "A5")
    # パッド（夜の空気）
    if n != "夜の高速" or i >= 4:
        if not (n == "終わり" and i >= 11):
            for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4" if not (n == "終わり" and i == 10) else f"{nm(pv[j])}:8")
    if n == "トンネル":                                      # 静か: パッドと、エレピの和音だけ
        for j in range(3): EP[j].bar(b, f"{nm(v[j])}:4")
        if i >= 4: SB.bar(b, f"{nm(r)}:4")
        continue
    if n == "夜明け":
        FX.bar(b, "C4:4") if i == 0 else None
        if i == 0: season(S, b, "小鳥", beats=16, vol=0.05, pan=0.4)
        SB.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(8)) if i >= 2 else f"{nm(r)}:4")
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 4, 3, 2, 1) * 2) if i >= 2 else "R:4")
        continue
    if n == "終わり":
        if i < 10:
            for j in range(3): EP[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
            if i < 8: ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
            SB.bar(b, f"{nm(r)}:4")
        elif i == 10:
            for j in range(3): EP[j].bar(b, f"{nm(v[j])}:8")
            SB.bar(b, f"{nm(r)}:8")
        if i % 4 == 0 and i < 9: BELL.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]) + " R:2")
        if i == 0: season(S, b, "小鳥", beats=32, vol=0.05, pan=0.4)
        continue
    # のこぎり波の 16分のアルペジオ（夜の高速の流れる灯り）
    ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 4, 3, 2, 1) * 2))
    if n == "夜の高速" and i < 4: continue
    # シンセベース: 8分の連打（シンセウェイブの走るベース）。最後の拍で次へ
    SB.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(6)) + f" {nm(r + 12)}:0.5 {nm(r)}:0.5")
    if n.startswith(("サビ", "最後")) or n == "サックスのソロ":
        for j in range(3): EP[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5")
    if n in ("サビ2", "最後のサビ", "サックスのソロ"):
        sv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n == "最後のサビ" and i % 4 == 3:
        BELL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]))
for name in ("サビ1", "最後のサビ"):
    cym_swell(CYM, S.sc(name)[0], 2, "E4")

# ================= ドラム（80年代: 大きなスネアの 2・4拍、8分のハット） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "夜の高速":
        if i >= 4: vgroove(D, b, "beat8", ghosts=0, seed=b, k="X.......X.......", s="................", h="x.x.x.x.x.x.x.x.")
        if i == 7: put_fill(D, b, "build")
        continue
    if n in ("トンネル", "夜明け"):
        if n == "夜明け" and i >= 2: vgroove(D, b, "four", ghosts=0, seed=b, s="................", h="x.x.x.x.x.x.x.x.")
        if n == "夜明け" and last: put_fill(D, b, "build")
        continue
    if n == "終わり":
        if i < 8: vgroove(D, b, "half", ghosts=0, seed=b, h="x.x.x.x.x.x.x.x.")
        elif i == 8: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)
        continue
    chorus = n.startswith(("サビ", "最後")) or n == "サックスのソロ"
    if n.startswith("Aメロ"):
        vgroove(D, b, "beat8", ghosts=0.1, seed=b, k="X.......X.X.....", h="x.x.x.x.x.x.x.x.")
    elif n.startswith("Bメロ"):
        vgroove(D, b, "beat8", ghosts=0.1, seed=b, k="X...X...X...X...", h="x.x.x.x.x.x.x.x.")
    else:
        vgroove(D, b, "four" if chorus else "beat8", ghosts=0.15, seed=b, s="....X.......X...", h="x.xxx.xxx.xxx.xx" if chorus else None)
    if i == 0 or (chorus and i % 8 == 0): crash(D, b, "C2", 4)
    if last: put_fill(D, b, "snare16")
    elif chorus and i % 4 == 3: put_fill(D, b, "small")

SIL.add(S.sc("トンネル")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の23。シンセウェイブ。A の短調・108、最後のサビと終わりは C 長調の明るい和音。"
          "夜行バスでふるさとへ帰る夜から、朝の「ただいま」まで。のこぎり波の 16分のアルペジオ、走る8分のシンセベース、サックスのソロ、"
          "トンネルを抜けて夜が明ける（小鳥とパッド）。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"トンネル": -0.5, "夜明け": -0.3, "最後のサビ": 0.5})
