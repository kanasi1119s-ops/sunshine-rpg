# vtp 07「ハニー・サワー」（仮）— 重音テト・K-POP 風の明るいボカロ曲。122・4/4。E長調（Aメロは C#m の色）→ 最後のサビは +1（F）。
# 2026-11-07 人間「KPOPで1曲ボカロ曲を作りましょう。ハチミツ、甘い、懐かしい、恋、酸っぱい、パワフル、元気をイメージして明るい曲に」
# 物語: 子どものころの夏、おばあちゃんが作ってくれたはちみつレモン。あまくてすっぱいあの味のような恋を、今年こそ一気に飲みほす（告白する）。
# K-POP のお約束（調べたこと）: サビのあとの掛け声の「ポストサビ」／2番でリズムの型を替える（ビートスイッチ）／歌のないダンスブレイク／
#   ブリッジで落として最後のサビで転調／電子のドラム・808・金管のキメ・声を切り刻んだようなシンセ／ハモリと声の重ね。
# コード進行: 王道・カノン・丸サは使わない。G#7（Ⅲ7）・Cmaj7（♭Ⅵ）・Am6（Ⅳm6）・D/E（♭Ⅶ の上の音を E の上で）・Dmaj7 で「甘い・酸っぱい・懐かしい」。
# この曲だけの音: 炭酸のびんを開ける「プシュッ」で始まり、「プシュッ」で終わる。
import sys, os, json, re
from vt25_lib import *

S = Song("07", "honeysour", "ハニー・サワー（仮）", "Honey Sour", 122, 4, "E", "major", "K-POP（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
K = Key("E", "major")
KL = Key("F", "major")

INTRO = ["E", "D/E"] * 4
VCH = ["C#m7", "F#m9", "Amaj7", "G#7"] * 2
PRE = ["F#m7", "G#m7", "Amaj7", "Bsus4", "Dmaj7", "E/G#", "Amaj7", "B7sus4"]
CH = ["Emaj7", "G#7", "C#m7", "Cmaj7", "Amaj7", "Am6", "B7sus4", "E"]
POST = ["E", "D/E"] * 4
DB = ["C#m7", "C#m7", "Amaj7", "B7"] * 2
BR = ["Amaj7", "G#m7", "F#m7", "E/G#", "Amaj7", "Am6", "Bsus4", "C7"]
S.scene("前奏", 8, "intro", INTRO)
S.scene("Aメロ1", 8, "verse", VCH)
S.scene("Bメロ1", 8, "pre", PRE)
S.scene("サビ1", 8, "chorus", CH)
S.scene("ポストサビ1", 8, "chorus", POST)
S.scene("Aメロ2", 8, "verse", VCH)
S.scene("Bメロ2", 8, "pre", PRE)
S.scene("サビ2", 8, "chorus", CH)
S.scene("ポストサビ2", 8, "chorus", POST)
S.scene("ダンスブレイク", 8, "solo", DB)
S.scene("ブリッジ", 8, "bridge", BR)
S.scene("最後のサビ", 8, "chorus", [tr_chord(c, 1) for c in CH])
S.scene("最後のポストサビ", 8, "chorus", [tr_chord(c, 1) for c in POST])
S.scene("後奏", 4, "outro", ["F", "Eb/F", "F", "F"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.2, patch="brightLead", low=False)
LY = Lyrics(S)

# ================= 歌（E長調・oct 4: 1＝E4、6,＝C#4、1'＝E5、2'＝F#5） =================
VA = ["R:0.5 6,:0.25 6,:0.25 1:0.5 6,:0.25 1:0.25 3:0.5 3:0.5 2:0.5 1:0.5", "6,:0.5 1:0.5 6,:1 R:2",
      "R:0.5 3:0.25 3:0.25 4:0.5 3:0.25 4:0.25 6:0.5 6:0.5 5:0.5 4:0.5", "3:0.5 2:0.5 7,:0.5 3:1 R:1.5",
      "R:0.5 5:0.25 5:0.25 6:0.5 5:0.5 3:0.5 3:0.5 1:0.5 R:0.5", "2:0.5 3:0.5 4:0.5 3:1 R:1.5",
      "R:0.5 3:0.25 4:0.25 6:0.5 6:0.25 5:0.25 4:0.5 3:0.5 4:1", "3:0.5 2:0.5 #5:1 R:2"]
VP = ["R:1 2:0.5 3:0.5 4:1 6:1", "5:1 4:1 R:2", "R:1 3:0.5 4:0.5 6:1 1':1", "1':1 6:1 5:1 R:1",
      "R:0.5 2:0.5 4:0.5 6:0.5 b7:1 6:1", "5:1 6:1 1':1 R:1", "R:1 1':0.5 2':0.5 1':1 6:1", "5:2 R:2"]
VC = ["1':0.5 1':0.5 5:0.5 1':0.5 2':1 1':1", "R:4",
      "R:0.5 6:0.5 6:0.25 5:0.25 6:0.5 1':0.5 2':0.5 1':0.5 6:0.5", "5:0.5 1':0.5 5:1 b3:1 R:1",
      "1':0.5 1':0.5 5:0.5 1':0.5 2':1 1':1", "R:4",
      "R:0.5 5:0.25 5:0.25 6:0.5 5:0.5 4:0.5 4:0.25 5:0.25 6:0.5 1':0.5", "2':0.5 1':0.5 5:0.5 1':2.5"]
VPO = ["1':0.25 1':0.25 1':0.5 5:0.5 1':0.5 2':1 R:1", "R:4",
       "R:0.5 6:0.5 5:0.5 3:0.5 5:0.5 6:0.5 R:1", "R:4",
       "1':0.25 1':0.25 1':0.5 5:0.5 1':0.5 2':1 R:1", "R:4",
       "R:0.5 3:0.25 3:0.25 5:0.5 6:0.5 1':1 2':0.5 R:0.5", "R:4"]
VBR = ["R:1 3:0.5 3:0.5 4:0.5 6:0.5 5:0.5 4:0.5", "3:0.5 3:0.5 2:0.5 3:0.5 5:0.5 3:0.5 R:1",
       "R:0.5 2:0.25 2:0.25 4:0.5 6:0.5 6:0.5 5:0.5 4:0.5 4:0.5", "3:0.5 4:0.5 5:0.5 6:0.5 5:1 R:1",
       "R:1 6:0.5 6:0.5 1':1 2':1", "2':1 1':0.5 b6:0.5 4:1 R:1",
       "R:1 1':0.5 1':0.5 2':1 1':1", "1':1 b6:1 b3:1 R:1"]

A1 = "がらすのびんにしまったなつ/はちみつみたいにとろけてる/きみのとなりはすっぱくて/ことばがのどにひっかかる"
A2 = "ふるいあるばむのすみっこで/わらうふたりはおなじかおで/いまもかわらずすきなの/あまいだけじゃつまらない"
P1 = "すこしすっぱい/そのきもちごと/まぜてのみほして/さあいくよ"
P2 = "あわがはじけ/なつのにおいが/いまならいえるよ/きいてよね"
CHL = "はにはにさわ/あまくてすっぱいこのこいを/はにはにさわ/いっきにのみほしてはじけたい"
POL = "はにはにはに/すっぱいさわ/はにはにはに/もっとちょうだい"
BRL = "おばあちゃんのいれてくれた/はちみつれもんのあじがする/あまいだけじゃない/それがこいでしょ"


def put(name, key, lines, text, o=4, bars=None):
    bars = bars or S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("前奏", K, ["R:2 1':0.5 1':0.5 5:0.5 2':0.5"], "はにさわ", bars=[S.sc("前奏")[7]])
put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VP, P1)
put("サビ1", K, VC, CHL)
put("ポストサビ1", K, VPO, POL)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VP, P2)
put("サビ2", K, VC, CHL)
put("ポストサビ2", K, VPO, POL)
put("ブリッジ", K, VBR, BRL)
put("最後のサビ", KL, VC, CHL)
put("最後のポストサビ", KL, VPO, POL)

# ================= 楽器 =================
CHOP = S.track("声のようなシンセ（合いことば）", "lead", patch="vocalChop", volume=0.085, pan=0.0, reverb=0.18, mono=True)
ARP = S.track("きらきらのアルペジオ", "lead", patch="kawaiiArp", volume=0.045, pan=0.35, reverb=0.25)
BELL = S.track("ベルの合いの手", "lead", patch="popBell", volume=0.04, pan=-0.35, reverb=0.3)
PLK = [S.track(f"はじくシンセの和音{j + 1}", "lead", patch="surgePopcorn", volume=0.045, pan=-0.25 + 0.25 * j, reverb=0.15) for j in range(3)]
SAW = [S.track(f"厚いシンセの和音{j + 1}", "lead", patch="modernSupersaw", volume=0.032, pan=-0.5 + 0.5 * j, reverb=0.2) for j in range(3)]
BRS = [S.track(f"金管のキメ{j + 1}", "brass", patch="brassSection", volume=0.06, pan=-0.3 + 0.3 * j, reverb=0.15) for j in range(3)]
SUB = S.track("808", "sub808", volume=0.17, pan=0)
SB = S.track("はずむシンセベース", "bass", patch="surgeBassPop", volume=0.15, pan=0)
PNL = S.track("ピアノ（左手）", "piano", volume=0.085, pan=-0.15, reverb=0.3)
PNR = [S.track(f"ピアノ（右手{j + 1}）", "piano", volume=0.055, pan=-0.05, reverb=0.3) for j in range(3)]
STR = [S.track(f"ストリングス{j + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=-0.4 + 0.4 * j, reverb=0.35, sustain=1.4) for j in range(3)]
GLK = S.track("オルゴールのような鉄琴", "glockenspiel", volume=0.06, pan=0.25, reverb=0.4)
SNAP = S.track("指パッチン", "lead", patch="seasonFx", volume=0.05, pan=0.15, modulate=False)
CLAP = S.track("手拍子", "lead", patch="seasonFx", volume=0.06, pan=-0.1, modulate=False)
FX = S.track("炭酸の音・ライザー・ドロップ", "lead", patch="fxRiser", volume=0.055, pan=0, reverb=0.25)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()


def root(ch, lo="E1"):
    bs = ch.split("/")[1] if "/" in ch else re.match(r"[A-G][#b]?", ch).group(0)
    return low(bs, lo)


HOOK = ["E5:0.5 E5:0.5 B4:0.5 E5:0.5 F#5:1 E5:1", "R:0.5 B4:0.5 C#5:0.5 B4:0.5 G#4:1 E4:1"]   # 合いことばの節（声のようなシンセ）
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    up = 1 if n.startswith("最後") or n == "後奏" else 0
    hook = [" ".join((lambda m: nm(midi(m.group(1)) + up) + m.group(2))(re.match(r"([A-G]#?\d)(.*)", t)) if not t.startswith("R") else t for t in h.split()) for h in HOOK]
    v3 = voice(ch.split("/")[0], 67 + up, 3, prev); prev = v3
    t = tones(ch.split("/")[0], "E4", "E6")
    r = root(ch)
    if n == "前奏":
        if i == 0: FX.bar(b, "A4:2")                                    # びんを開ける「プシュッ」（白い雑音のシュッ）
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 1, 3, 5, 3)))
        if i >= 2: CHOP.bar(b, hook[i % 2])
        if i >= 4:
            SUB.bar(b, f"{nm(r)}:2 {nm(r)}:1.5 {nm(r + 12)}:0.5")
            [SAW[j].bar(b, f"{nm(v3[j])}:4") for j in range(3)]
            D.set(b, "X.......X..x....", "....X.......X...", "x.x.x.x.x.x.x.x.")
        if i == 3: FX.at(S.bar_beat(b + 1) - 4, "C4:4")
        if i == 7: D.set(b, "X.......X.......", "....X...........", "x.x.x.x........."); [BRS[j].bar(b, f"{nm(v3[j])}:0.5 R:1 {nm(v3[j])}:0.5 R:2") for j in range(3)]
    elif n in ("Aメロ1", "Aメロ2"):
        SB.bar(b, f"{nm(r)}:0.25 R:0.5 {nm(r)}:0.25 R:0.5 {nm(r + 7)}:0.25 R:0.25 {nm(r)}:0.5 R:0.5 {nm(r)}:0.25 R:0.75")
        [PLK[j].bar(b, f"R:0.5 {nm(v3[j])}:0.25 R:1.25 {nm(v3[j])}:0.25 R:0.75 {nm(v3[j])}:0.25 R:0.75") for j in range(3)]
        if n == "Aメロ1":
            D.set(b, "X......xX.......", "................", "..x...x...x...x.")
            SNAP.bar(b, "R:1 C#5:1 R:1 C#5:1")
        else:                                                           # 2番: ラテン系の跳ねる型（デンボウ）にビートスイッチ
            D.set(b, "X...X...X...X...", "...x..x....x..x.", "x.x.x.x.x.x.x.x.")
            BELL.bar(b, "R:3 " + f"{nm(t[-2])}:0.5 {nm(t[-3])}:0.5" if i % 2 == 1 else "R:4")
        if i == 7: CYM.at(S.bar_beat(b + 1) - 2, "C4:2")
    elif n in ("Bメロ1", "Bメロ2"):
        SB.bar(b, f"{nm(r)}:1 {nm(r)}:1 {nm(r)}:1 {nm(r)}:1" if i < 7 else f"{nm(r)}:1 R:3")
        [SAW[j].bar(b, f"{nm(v3[j])}:4" if i < 7 else f"{nm(v3[j])}:2 R:2") for j in range(3)]
        if i < 4: D.set(b, "X.......X.......", "....X.......X...", "xxxxxxxxxxxxxxxx" if i >= 2 else "x.x.x.x.x.x.x.x.")
        elif i < 7: D.set(b, "X...X...X...X...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x."); CLAP.bar(b, "B4:0.5 B4:0.5 B4:0.5 B4:0.5 B4:0.5 B4:0.5 B4:0.5 B4:0.5")
        else: D.set(b, "X...X...........", "xxxxXXXX........", "................")   # 最後の2拍は全部止まる（ため）
        if i == 5: FX.at(S.bar_beat(b), "D4:8")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        if i == 0: D.cym(b, "C2:4"); FX.bar(b, "G4:2")
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r)}:1 {nm(r + 12)}:0.5")
        [SAW[j].bar(b, f"{nm(v3[j])}:1.5 {nm(v3[j])}:1 {nm(v3[j])}:1.5") for j in range(3)]
        [BRS[j].bar(b, f"R:1.5 {nm(v3[j] + 12)}:0.5 R:1.5 {nm(v3[j] + 12)}:0.5" if i % 2 == 0 else f"{nm(v3[j] + 12)}:0.25 R:3.75") for j in range(3)]
        D.set(b, "X...X...X...X...", "....X.......X...", "..O...O...O...O.")
        CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i in (1, 5): CHOP.bar(b, hook[(i // 4) % 2])                  # 歌の休みの小節に合いことばで答える
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)] + 12)}:0.25" for q in (0, 1, 2, 1) * 4) if i % 2 == 1 else "R:4")
        if i == 7: D.set(b, "X...X...X...X...", "....X...X.X.XXXX", "..O...O........."); D.tom(b, "R:3 C4:0.25 A3:0.25 F3:0.25 F3:0.25")
    elif n in ("ポストサビ1", "ポストサビ2", "最後のポストサビ"):
        if i == 0: D.cym(b, "C2:4")
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r)}:1.5")
        if i % 2 == 1: CHOP.bar(b, hook[(i // 2) % 2])
        [BRS[j].bar(b, f"{nm(v3[j])}:0.5 R:1 {nm(v3[j])}:0.5 R:2" if i % 2 == 1 else "R:4") for j in range(3)]
        D.set(b, "X.....X...X.....", "........X.......", "x.x.xxx.x.x.xxxx")
        CLAP.bar(b, "R:2 B4:2")
        if i == 7 and n == "ポストサビ1": CYM.at(S.bar_beat(b + 1) - 2, "C4:2"); D.set(b, "X.....X...X.....", "........X...XXXX", "x.x.xxx.........")
        if i == 7 and n == "ポストサビ2": D.set(b, "X.....X...X.....", "........X.X.XXXX", "x.x.xxx.........")
    elif n == "ダンスブレイク":                                         # 跳ねるキック（ジャージークラブ風）と金管のリフ
        if i == 0: D.cym(b, "C2:4"); FX.bar(b, "G4:2")
        D.set(b, "X..X..X.X..X..X.", "....X.......X...", "x.x.x.x.x.x.x.x.")
        SUB.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5 {nm(r + 12)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5")
        rf = ["C#5:0.5 R:0.25 C#5:0.25 E5:0.5 F#5:0.5 R:0.5 E5:0.5 C#5:1", "B4:0.5 R:0.25 B4:0.25 C#5:0.5 E5:0.5 R:0.5 C#5:0.5 B4:1",
              "A4:0.5 R:0.25 A4:0.25 C#5:0.5 E5:0.5 R:0.5 G#5:0.5 F#5:1", "F#5:0.75 E5:0.75 D#5:0.5 B4:1 F#4:1"][i % 4]
        BRS[0].bar(b, rf)
        BRS[1].bar(b, " ".join((nm(midi(x.split(':')[0]) - 4) + ':' + x.split(':', 1)[1]) if not x.startswith("R") else x for x in rf.split()))
        CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 7: D.set(b, "X..X..X.X.......", "....X...XXXXXXXX", "x.x.x.x........."); FX.at(S.bar_beat(b + 1) - 1, "E4:2")
    elif n == "ブリッジ":                                              # 懐かしい: ピアノ・弦・鉄琴。後半から少しずつドラム
        PNL.bar(b, f"{nm(root(ch, 'E2'))}:2 {nm(root(ch, 'E2') + 7)}:2")
        [PNR[j].bar(b, f"R:0.5 {nm(v3[j])}:1.5 R:0.5 {nm(v3[j])}:1.5") for j in range(3)]
        [STR[j].bar(b, f"{nm(v3[j] - 12)}:4") for j in range(3)] if i >= 2 else None
        GLK.bar(b, " ".join(f"{nm(t[q % len(t)] + 12)}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)) if i < 4 else "R:4")
        SB.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4")
        if i >= 4: D.set(b, "X.......X.......", "....x.......x...", "x...x...x...x...")
        if i == 7: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", "x.x.x.x.x.x.x.x."); CYM.at(S.bar_beat(b + 1) - 4, "E4:4"); FX.at(S.bar_beat(b + 1) - 4, "C4:4")
    elif n == "後奏":
        if i < 3:
            D.set(b, "X.......X.......", "X.......X.......", "................"); D.cym(b, "C2:2 C2:2")
            [BRS[j].bar(b, f"{nm(v3[j] + 12)}:0.5 R:1.5 {nm(v3[j] + 12)}:0.5 R:1.5") for j in range(3)]
            SUB.bar(b, f"{nm(r)}:2 {nm(r)}:2")
        else:
            D.set(b, "X...............", "X...............", "................"); D.cym(b, "C2:4")
            [BRS[j].bar(b, f"{nm(v3[j] + 12)}:1 R:3") for j in range(3)]
            FX.at(S.bar_beat(b) + 2, "A4:2")                           # 最後にまた「プシュッ」

S.fade_out = 0
S.desc = ("仮: K-POP 風のボカロ曲（重音テト）。ハニー・サワー。E・122、最後のサビは +1（F）。炭酸の「プシュッ」で始まり終わる。"
          "ポストサビの掛け声・2番のビートスイッチ・ダンスブレイク・懐かしいブリッジ。王道・カノン・丸サを使わない進行。自作")
finish(S, LY, V, 0, hi=80, double=[("サビ1", 0.3), ("サビ2", 0.35), ("最後のサビ", 0.5), ("最後のポストサビ", 0.4)],
       level={"verse": -0.15}, special={"最後のサビ": 0.35, "ブリッジ": -0.3})

if VOCAL:   # 歌のノイズ対策（白い息のリテイクで決めたもの）と、サビの3度上のハモリ（明るい K-POP の重ね）
    path = sys.argv[1]; js = json.load(open(path))
    main = js["vocals"][0]; main.update(hiClean=0.8, breathy=0.0, declick=1.0)
    rng = []
    for nm_ in ("サビ1", "サビ2", "最後のサビ", "ポストサビ1", "ポストサビ2", "最後のポストサビ"):
        bs = S.sc(nm_); rng.append((bs[0] * S.beats, (bs[-1] + 1) * S.beats, KL if nm_.startswith("最後") else K))
    SC = {id(kk): sorted({(midi(kk.mel(f"{d}:1", oct=4).split(":")[0]) % 12) for d in range(1, 8)}) for kk in (K, KL)}
    out = []; t = 0.0
    for tok in main["notes"].split():
        m = re.match(r"^([A-G][b#]?-?\d)([^:]*):([0-9.]+):(.+)$", tok)
        L_ = float(tok.split(":")[1])
        hit = [x for x in rng if x[0] - 1e-6 <= t < x[1]] if m else []
        if m and hit:
            pcs = SC[id(hit[0][2])]; q = midi(m.group(1)); steps = 0
            while steps < 2:
                q -= 1
                if q % 12 in pcs: steps += 1
            out.append(f"{nm(q)}{m.group(2).replace('/', '').replace('!', '')}:{m.group(3)}:{m.group(4)}")
        else:
            out.append(f"R:{L_:g}")
        t += L_
    harm = dict(main); harm.update({"notes": " ".join(out), "volume": 0.4, "pan": 0, "vibrato": 20, "vibratoRate": 5.9, "vibratoMap": [],
                                    "blend": {"voice": "teto-soft", "amount": 0.45}, "reverb": 0.24, "dynamics": [], "consonant": 1.2})
    js["vocals"].append(harm)
    json.dump(js, open(path, "w"), ensure_ascii=False)
    print("  サビとポストサビに3度下のハモリを入れた")
