# vtp 07「ハニー・サワー」（仮）— 重音テト・K-POP 風の明るいボカロ曲。122・4/4。E長調（Aメロは C#m の色）→ 最後のサビは +1（F）。
# 2026-11-07 人間「KPOPで1曲ボカロ曲を作りましょう。ハチミツ、甘い、懐かしい、恋、酸っぱい、パワフル、元気をイメージして明るい曲に」
# 物語: 子どものころの夏、おばあちゃんが作ってくれたはちみつレモン。あまくてすっぱいあの味のような恋を、今年こそ一気に飲みほす（告白する）。
# K-POP のお約束（調べたこと）: サビのあとの掛け声の「ポストサビ」／2番でリズムの型を替える（ビートスイッチ）／歌のないダンスブレイク／
#   ブリッジで落として最後のサビで転調／電子のドラム・808・金管のキメ・声を切り刻んだようなシンセ／ハモリと声の重ね。
# コード進行: 王道・カノン・丸サは使わない。G#7（Ⅲ7）・Cmaj7（♭Ⅵ）・Am6（Ⅳm6）・D/E（♭Ⅶ の上の音を E の上で）・Dmaj7 で「甘い・酸っぱい・懐かしい」。
# この曲だけの音: 炭酸のびんを開ける「プシュッ」で始まり、「プシュッ」で終わる。
import sys, os, json, re
import numpy as np
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

# ================= 楽器（2026-11-07 人間「Kawaii_future_bass系の音源を主体で使って」）=================
# カワイイ・フューチャーベースの音を主役に: うねる和音（fbChord・キックに合わせて凹む＋音の頭を下からすくい上げる）、
#   声を切り刻んだようなシンセ（vocalChop）、きらきらのアルペジオ（kawaiiArp）、ベル（popBell）、ファミコン風の小さなパルス（chipPulse25）、
#   はじけるプラック（surgePopcorn）、808。金管は使わない。
# MIDI のチャンネルは（ドラム以外）15まで: 同じ楽器の和音のパートは pan・reverb をそろえて1つのチャンネルを共有させる（v1 は足りずに、
#   ブリッジのピアノや弦などが別の楽器の音で鳴っていた）
CHOP = S.track("声のようなシンセ（合いことば）", "lead", patch="vocalChop", volume=0.09, pan=0.0, reverb=0.2, mono=True)
ARP = S.track("きらきらのアルペジオ", "lead", patch="kawaiiArp", volume=0.045, pan=0.3, reverb=0.25)
BELL = S.track("ベル（合いの手・オルゴール）", "lead", patch="popBell", volume=0.045, pan=-0.3, reverb=0.3)
FB = [S.track(f"うねる和音{j + 1}", "lead", patch="fbChord", volume=0.036, pan=0.0, reverb=0.22, duck=0.55) for j in range(3)]
PLK = [S.track(f"はじくプラックの和音{j + 1}", "lead", patch="surgePopcorn", volume=0.045, pan=0.0, reverb=0.15) for j in range(3)]
CHIP = S.track("小さなパルス（ファミコン風）", "lead", patch="chipPulse25", volume=0.03, pan=0.2, reverb=0.2, mono=True)
SUB = S.track("808", "sub808", volume=0.17, pan=0)
SB = S.track("はずむシンセベース", "bass", patch="surgeBassPop", volume=0.15, pan=0)
PN = [S.track(f"ピアノ{j + 1}", "piano", volume=0.06, pan=-0.1, reverb=0.3) for j in range(4)]
STR = [S.track(f"ストリングス{j + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=0.0, reverb=0.35, sustain=1.4) for j in range(3)]
PERC = S.track("手拍子・指パッチン", "lead", patch="seasonFx", volume=0.055, pan=0.0, reverb=0.12, modulate=False)
FX = S.track("炭酸の音・ライザー・ドロップ", "lead", patch="fxRiser", volume=0.055, pan=0, reverb=0.25)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()


def root(ch, lo="E1"):
    bs = ch.split("/")[1] if "/" in ch else re.match(r"[A-G][#b]?", ch).group(0)
    return low(bs, lo)


HOOK = ["E5:0.5 E5:0.5 B4:0.5 E5:0.5 F#5:1 E5:1", "R:0.5 B4:0.5 C#5:0.5 B4:0.5 G#4:1 E4:1"]   # 合いことばの節
DROP = ["E5:0.25 E5:0.25 R:0.25 B4:0.25 E5:0.5 F#5:0.25 E5:0.25 R:0.5 G#5:0.5 F#5:0.5 E5:0.5",
        "C#5:0.25 C#5:0.25 R:0.25 B4:0.25 C#5:0.5 E5:0.25 C#5:0.25 R:0.5 B4:0.5 G#4:0.5 B4:0.5"]   # ドロップの声のシンセ（切り刻んだ節）
def shift(line, up):
    return " ".join((lambda m: nm(midi(m.group(1)) + up) + m.group(2))(re.match(r"([A-G]#?\d)(.*)", t)) if not t.startswith("R") else t for t in line.split())
def fbw(b, v3, pat):
    """うねる和音: 音の頭を下からすくい上げ（/）、キックに合わせて凹ませる"""
    for j in range(3): FB[j].bar(b, " ".join((f"{nm(v3[j])}:{d}/" if k == 0 else f"{nm(v3[j])}:{d}") if d > 0 else f"R:{-d}" for k, d in enumerate(pat)))
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    up = 1 if n.startswith("最後") or n == "後奏" else 0
    hook = [shift(h, up) for h in HOOK]; drop = [shift(h, up) for h in DROP]
    v3 = voice(ch.split("/")[0], 67 + up, 3, prev); prev = v3
    t = tones(ch.split("/")[0], "E4", "E6")
    r = root(ch)
    arp16 = " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 1, 3, 5, 3))
    if n == "前奏":
        # 2026-11-08 人間「前奏の演奏変えよう。ピロピロ始まり聞き飽きた」: きらきらのアルペジオで始めるのをやめた。
        #   びんの「プシュッ」→ 古いピアノの和音（はちみつの懐かしさ）だけ → 2小節目からうねる和音が下から立ち上がり、指パッチンと808のすべり
        #   → 4小節目の頭で止めて、5小節目からキックの跳ねる型と、声のシンセの合いことば。アルペジオは前奏では鳴らさない
        if i == 0: FX.bar(b, "A4:2")                                    # びんを開ける「プシュッ」
        if i < 4:
            PN[0].bar(b, f"{nm(root(ch, 'E2'))}:1.5 {nm(root(ch, 'E2') + 12)}:2.5")
            [PN[j + 1].bar(b, f"{nm(v3[j])}:1.5 R:0.5 {nm(v3[j])}:0.5 {nm(v3[j])}:1.5") for j in range(3)]
        if 1 <= i < 4:
            fbw(b, v3, [4] if i < 3 else [2, 1, -1])                   # うねる和音を長くのばして、少しずつ立ち上がる
            PERC.bar(b, "R:1 C#5:1 R:1 C#5:1")
        if i == 2: SUB.bar(b, f"R:2 {nm(r + 12)}:1 {nm(r)}:1/")       # 808 が下にすべり込む
        if i == 3: FX.at(S.bar_beat(b), "C4:3"); D.set(b, "................", "........X.X.XXXX", "................")
        if i >= 4:
            SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 R:1 {nm(r + 12)}:0.5")
            fbw(b, v3, [0.75, 0.75, 0.5, -0.5, 0.75, 0.75])
            CHOP.bar(b, hook[i % 2])
            BELL.bar(b, "R:2 " + f"{nm(t[-1])}:1 {nm(t[-2])}:1" if i % 2 == 1 else "R:4")
            D.set(b, "X..X......X.....", "....X.......X...", "x...x.x.x...x.x.")
        if i == 4: D.cym(b, "C2:4")
        if i == 7: D.set(b, "X..X......X.....", "....X...X.X.XXXX", "x...x.x........."); CHIP.bar(b, "E6:0.25 R:0.25 B5:0.25 R:0.25 E6:0.5 R:2.5")
    elif n in ("Aメロ1", "Aメロ2"):
        SB.bar(b, f"{nm(r)}:0.25 R:0.5 {nm(r)}:0.25 R:0.5 {nm(r + 7)}:0.25 R:0.25 {nm(r)}:0.5 R:0.5 {nm(r)}:0.25 R:0.75")
        [PLK[j].bar(b, f"R:0.5 {nm(v3[j])}:0.25 R:1.25 {nm(v3[j])}:0.25 R:0.75 {nm(v3[j])}:0.25 R:0.75") for j in range(3)]
        if n == "Aメロ1":
            D.set(b, "X......xX.......", "................", "..x...x...x...x.")
            PERC.bar(b, "R:1 C#5:1 R:1 C#5:1")                         # 指パッチン
        else:                                                           # 2番: ラテン系の跳ねる型（デンボウ）にビートスイッチ
            D.set(b, "X...X...X...X...", "...x..x....x..x.", "x.x.x.x.x.x.x.x.")
            BELL.bar(b, "R:3 " + f"{nm(t[-2])}:0.5 {nm(t[-3])}:0.5" if i % 2 == 1 else "R:4")
        if i == 7: CYM.at(S.bar_beat(b + 1) - 2, "C4:2")
    elif n in ("Bメロ1", "Bメロ2"):
        SB.bar(b, f"{nm(r)}:1 {nm(r)}:1 {nm(r)}:1 {nm(r)}:1" if i < 7 else f"{nm(r)}:1 R:3")
        fbw(b, v3, [2, 2] if i < 4 else ([1, 1, 1, 1] if i < 6 else ([0.5] * 8 if i == 6 else [1, -3])))
        ARP.bar(b, arp16 if i >= 4 and i < 7 else "R:4")
        if i < 4: D.set(b, "X.......X.......", "....X.......X...", "xxxxxxxxxxxxxxxx" if i >= 2 else "x.x.x.x.x.x.x.x.")
        elif i < 7: D.set(b, "X...X...X...X...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x."); PERC.bar(b, "B4:0.5 " * 8)
        else: D.set(b, "X...X...........", "xxxxXXXX........", "................")   # 最後の2拍は全部止まる（ため）
        if i == 5: FX.at(S.bar_beat(b), "D4:8")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        if i == 0: D.cym(b, "C2:4"); FX.bar(b, "G4:2")
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r)}:1 {nm(r + 12)}:0.5")
        fbw(b, v3, [1.5, 1, 1, 0.5])
        D.set(b, "X.....X...X.....", "....X.......X...", "x.x.x.x.x.x.xxxx")
        PERC.bar(b, "R:1 B4:1 R:1 B4:1")
        if i in (1, 5): CHOP.bar(b, hook[(i // 4) % 2]); CHIP.bar(b, shift(hook[(i // 4) % 2], 12))   # 歌の休みに合いことばで答える
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)] + 12)}:0.25" for q in (0, 1, 2, 1) * 4))
        if i == 7: D.set(b, "X.....X...X.....", "....X...X.X.XXXX", "x.x.x.x........."); D.tom(b, "R:3 C4:0.25 A3:0.25 F3:0.25 F3:0.25")
    elif n in ("ポストサビ1", "ポストサビ2", "最後のポストサビ"):     # ドロップ: 声のシンセが主役、和音は8分でうねる
        if i == 0: D.cym(b, "C2:4")
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r)}:1.5")
        fbw(b, v3, [0.75, 0.75, 0.5, 0.75, 0.75, 0.5])
        if i % 2 == 1: CHOP.bar(b, drop[(i // 2) % 2])
        D.set(b, "X.....X...X.....", "........X.......", "x.x.xxx.x.x.xxxx")
        PERC.bar(b, "R:2 B4:2")
        BELL.bar(b, "R:2 " + f"{nm(t[-1])}:0.5 {nm(t[-2])}:0.5 {nm(t[-3])}:1" if i % 2 == 0 else "R:4")
        if i == 7 and n == "ポストサビ1": CYM.at(S.bar_beat(b + 1) - 2, "C4:2"); D.set(b, "X.....X...X.....", "........X...XXXX", "x.x.xxx.........")
        if i == 7 and n == "ポストサビ2": D.set(b, "X.....X...X.....", "........X.X.XXXX", "x.x.xxx.........")
    elif n == "ダンスブレイク":                                         # 2つ目のドロップ: 声のシンセのリフと、16分でうねる和音
        if i == 0: D.cym(b, "C2:4"); FX.bar(b, "G4:2")
        D.set(b, "X..X..X.X..X..X.", "....X.......X...", "x.x.x.x.x.x.x.x.")
        SUB.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5 {nm(r + 12)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5")
        fbw(b, v3, [0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.5, 0.5, 0.5])
        CHOP.bar(b, drop[i % 2]); CHIP.bar(b, shift(drop[i % 2], 12) if i >= 4 else "R:4")
        PERC.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 7: D.set(b, "X..X..X.X.......", "....X...XXXXXXXX", "x.x.x.x........."); FX.at(S.bar_beat(b + 1) - 1, "E4:2")
    elif n == "ブリッジ":                                              # 懐かしい: ピアノ・弦・オルゴールのようなベル。後半から少しずつドラム
        PN[0].bar(b, f"{nm(root(ch, 'E2'))}:2 {nm(root(ch, 'E2') + 7)}:2")
        [PN[j + 1].bar(b, f"R:0.5 {nm(v3[j])}:1.5 R:0.5 {nm(v3[j])}:1.5") for j in range(3)]
        if i >= 2: [STR[j].bar(b, f"{nm(v3[j] - 12)}:4") for j in range(3)]
        BELL.bar(b, " ".join(f"{nm(t[q % len(t)] + 12)}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)) if i < 4 else "R:4")
        SB.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4")
        if i >= 4: D.set(b, "X.......X.......", "....x.......x...", "x...x...x...x...")
        if i == 7: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", "x.x.x.x.x.x.x.x."); CYM.at(S.bar_beat(b + 1) - 4, "E4:4"); FX.at(S.bar_beat(b + 1) - 4, "C4:4")
    elif n == "後奏":
        if i < 3:
            D.set(b, "X.......X.......", "X.......X.......", "................"); D.cym(b, "C2:2 C2:2")
            fbw(b, v3, [0.5, -1.5, 0.5, -1.5]); SUB.bar(b, f"{nm(r)}:2 {nm(r)}:2")
            CHOP.bar(b, drop[i % 2])
        else:
            D.set(b, "X...............", "X...............", "................"); D.cym(b, "C2:4")
            fbw(b, v3, [1, -3])
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

    # ===== 2026-11-08 人間「テトの声ももっと抑揚と、コーラスをつけよ。あと男性っぽい声のテトも入れてデュエットしよう」 =====
    # 男声のテト: 同じテトの音源を1オクターブ下げ、のどの響き（フォルマント）を 0.84 に下げて、太く低い男の人の声にする。
    # デュエットの分け方（句ごと。句のまん中の時刻で決める）:
    #   前奏の「はにさわ」… ふたり ／ Aメロ … テト（女声）／ Bメロ … 男声 ／ サビ … ふたり（オクターブのユニゾン）
    #   ポストサビ … 掛け合い（テト→男声→テト→ふたり）／ ブリッジ … 男声→テト→ふたり
    BT = S.beats
    def sec(nm_): bs = S.sc(nm_); return bs[0] * BT, (bs[-1] + 1) * BT
    toks = main["notes"].split(); tt = []; t = 0.0
    for tok in toks: tt.append(t); t += float(tok.split(":")[1])
    phr = []; cur = []
    for i, tok in enumerate(toks):
        if tok.startswith("R:"):
            if cur: phr.append(cur); cur = []
        else: cur.append(i)
    if cur: phr.append(cur)
    def who(i0, i1, k):
        mid = (tt[i0] + tt[i1] + float(toks[i1].split(":")[1])) / 2
        for nm_ in [x[0] for x in S.scenes]:
            a0, a1 = sec(nm_)
            if a0 <= mid < a1: break
        else: return "both"
        r = (mid - a0) / (a1 - a0)
        # 2026-11-08 人間「Aメロは女性、Bメロ男性、サビ2人にしよう」
        if nm_ == "前奏": return "both"
        if nm_.startswith("Aメロ"): return "teto"
        if nm_.startswith("Bメロ"): return "man"
        if "サビ" in nm_ and "ポスト" not in nm_: return "both"
        if nm_.startswith("ポストサビ") or nm_ == "最後のポストサビ":
            return ["teto", "man", "teto", "both"][min(3, int(r * 4))]
        if nm_ == "ブリッジ": return ["man", "teto", "both", "both"][min(3, int(r * 4))]
        return "both"
    role = {}
    for k, ph in enumerate(phr):
        w = who(ph[0], ph[-1], k)
        for i in ph: role[i] = w
    def rest_of(tok): return "R:" + tok.split(":")[1]
    t_notes = [tok if tok.startswith("R:") or role.get(i) in ("teto", "both") else rest_of(tok) for i, tok in enumerate(toks)]
    m_notes = [rest_of(tok) if tok.startswith("R:") or role.get(i) not in ("man", "both") else tok for i, tok in enumerate(toks)]
    hm = harm["notes"].split()
    harm["notes"] = " ".join(h if (h.startswith("R:") or role.get(i) in ("teto", "both")) else rest_of(h) for i, h in enumerate(hm)) if len(hm) == len(toks) else harm["notes"]

    # 抑揚: 句ごとに「入りは少し抑えて、まん中から高い音・長い音に向かってふくらみ、句の終わりで力を抜く」山を、場面の強さに足す。
    #   強い拍の高い音には「!」（強く）、裏の短い音には「?」（弱く）。サビの入り・ブリッジの最後の句は大きく。
    base = {"verse": -0.3, "pre": 0.0, "chorus": 0.45, "intro": 0.2, "bridge": -0.25, "solo": 0.3, "outro": 0.1}
    kind = {x[0]: x[3] for x in S.scenes}
    dyn = []
    def accent(tok, i, top):
        mm = re.match(r"^([A-G][b#]?-?\d)([^:]*):([0-9.]+):(.+)$", tok)
        if not mm or "!" in mm.group(2) or "?" in mm.group(2): return tok
        on = abs((tt[i] * 2) % 2) < 1e-6 and abs(tt[i] % 1) < 1e-6; L_ = float(mm.group(3))
        if on and midi(mm.group(1)) >= top - 1 and L_ >= 0.5: return f"{mm.group(1)}!{mm.group(2)}:{mm.group(3)}:{mm.group(4)}"
        if not on and L_ <= 0.25 and midi(mm.group(1)) < top - 3: return f"{mm.group(1)}?{mm.group(2)}:{mm.group(3)}:{mm.group(4)}"
        return tok
    for ph in phr:
        t0 = tt[ph[0]]; t1 = tt[ph[-1]] + float(toks[ph[-1]].split(":")[1])
        nm_ = next((x for x in [y[0] for y in S.scenes] if sec(x)[0] <= (t0 + t1) / 2 < sec(x)[1]), S.scenes[-1][0])
        b0 = base.get(kind.get(nm_, "verse"), 0.0) + (0.12 if nm_.startswith("最後") else 0.0)
        ms_ = [midi(re.match(r"([A-G][b#]?-?\d)", toks[i]).group(1)) for i in ph if re.match(r"[A-G]", toks[i])]
        top = max(ms_) if ms_ else 0
        ipk = max(ph, key=lambda i: (midi(re.match(r"([A-G][b#]?-?\d)", toks[i]).group(1)) if re.match(r"[A-G]", toks[i]) else 0) + float(toks[i].split(":")[1]))
        tp = tt[ipk]
        dyn += [[round(t0, 3), round(b0 - 0.15, 3)], [round(tp, 3), round(b0 + 0.22, 3)], [round(max(tp + 0.01, t1 - 0.3), 3), round(b0 + 0.05, 3)], [round(t1, 3), round(b0 - 0.2, 3)]]
        for i in ph: t_notes[i] = accent(t_notes[i], i, top) if not t_notes[i].startswith("R:") else t_notes[i]; m_notes[i] = accent(m_notes[i], i, top) if not m_notes[i].startswith("R:") else m_notes[i]
    dyn = [[float(a_), float(np.clip(b_, -0.6, 0.75))] for a_, b_ in sorted(dyn)]
    main.update(notes=" ".join(t_notes), dynamics=dyn, auto=0.7, scoop=0.75, vibrato=38, legato=0.012)
    man = dict(main); man.update({"notes": " ".join(m_notes), "transpose": -12, "formant": 0.84, "volume": 0.95, "pan": 0.0,
                                  "blend": {"voice": "teto-soft", "amount": 0.12}, "vibrato": 26, "vibratoRate": 5.0, "scoop": 0.6, "air": 2.0,
                                  "eq": [["peak", 160, 0.8, 2], ["peak", 350, 1.0, -2.5], ["peak", 1800, 1.4, 3], ["peak", 3200, 2.0, 4], ["hshelf", 6500, 0.7, 5]],
                                  "reverb": 0.17})
    # ふたりで歌う所は、男声を少し下げて（オクターブのユニゾンが太く聞こえすぎないように）、句ごとに音量を変える
    js["vocals"].append(man)

    # コーラス（バックの声）: サビ・最後のサビで、和音の音を「あー」で長くのばす2声（左右）。ポストサビは掛け声「へい」を16分の裏で。
    bk = [[], []]
    def pad(L, rest=True): return f"R:{L:g}"
    t = 0.0
    for b in range(S.nb):
        n_, i_, _, _ = S.scene_of(b)
        if n_ in ("サビ1", "サビ2", "最後のサビ"):
            ch = S.chords[b].split("/")[0]; v = voice(ch, 67 + (1 if n_.startswith("最後") else 0), 3)
            for j in range(2): bk[j].append(f"{nm(v[j + 1])}:3.5:あ R:0.5")
        elif n_ in ("ポストサビ2", "最後のポストサビ") and i_ % 2 == 1:
            bk[0].append(f"R:3 {nm(76 + (1 if n_.startswith('最後') else 0))}!:0.5:へ {nm(73 + (1 if n_.startswith('最後') else 0))}:0.5:ー"); bk[1].append("R:4")
        else:
            for j in range(2): bk[j].append("R:4")
    for j, pn in enumerate((-0.55, 0.55)):
        c = dict(harm); c.update({"notes": " ".join(bk[j]), "volume": 0.22, "pan": pn, "reverb": 0.34, "vibrato": 12, "dynamics": [],
                                  "blend": {"voice": "teto-soft", "amount": 0.6}, "auto": 0.0, "formant": 1.05 if j == 0 else 0.9})
        js["vocals"].append(c)
    json.dump(js, open(path, "w"), ensure_ascii=False)
    print("  デュエット（男声のテト）・抑揚・バックのコーラスを入れた: 歌", len(js["vocals"]), "本")
