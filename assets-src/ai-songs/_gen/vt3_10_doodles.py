# vt3 10「教科書の落書きたち」Doodles in the Textbook（仮）— ブルーグラス。160・4/4。G長調（転調なし）。
# 第3弾（0時〜24時の街）の 9時。表は docs/sound/vt3-plan.md。
# 物語: 9時の算数の授業。ねむくなって、教科書のすみに描いた落書き（棒人間・ロケット・小さなねこ）。ぱらぱらめくると、動き出した。
#   棒人間が口笛でふくのは、聞きおぼえのある節（けさ街に流れていた鼻歌）。数字もいっしょに踊り出し、教室の外までパレード。
#   先生がふりむいた瞬間、ぴたりと止まる。チャイムが鳴るまで、ちいさな仲間たちはページのすみで待っている。
# 場面と強さ: バンジョー（ロールだけ）→ イントロ（フィドルの節・中）→ Aメロ1（はずむ・中）→ Bメロ1（せんせいは黒板へ・止め）
#   → サビ1（落書きの行進・強）→ ソロ回し1（バンジョー → フィドル）→ Aメロ2 → Bメロ2 → サビ2 → 先生がふりむく（全員止まる・無音に近い）
#   → ソロ回し2（ギター → フィドルとバンジョーのかけ合い）→ 最後のサビ（いちばん強い）→ チャイム
# 旋律の性格: はねるカントリーの8分、サビはヨーデルのようにオクターブを行き来する（D4 ↔ D5）。A3〜F#5。
# この曲だけの音: 楽器ごとのソロ回し（バンジョー・フィドル・ギター）と、「先生がふりむく」所の全員の止め。
#   合いことばの節（3・5・6・5・2）は、ソロ回し1でフィドルが弾く（B・D・E・D・A）。
from vt25_lib import *

S = Song("10", "doodles", "教科書の落書きたち（仮）", "Doodles in the Textbook", 160, 4, "G", "major", "ブルーグラス（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass rubner " + S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.8
K = Key("G", "major")          # oct 3 で 1 = G3（歌は D4〜F#5）

A_CH = ["G", "G", "C", "G", "G", "Em", "D", "D"]
B_CH = ["Em", "C", "G", "D", "Em", "C", "Am7", "D"]
C_CH = ["C", "G", "D", "G", "C", "G", "Am7", "D", "C", "G", "Em", "C", "G", "D", "G", "G"]
TUNE = ["G", "C", "G", "D", "G", "C", "D", "G"]

S.scene("バンジョー", 4, "intro", ["G", "G", "C", "D"])
S.scene("イントロ", 8, "intro", TUNE)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("ソロ回し1", 16, "solo", TUNE)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("先生がふりむく", 4, "bridge", ["Em", "C", "Am7", "D"])
S.scene("ソロ回し2", 16, "solo", TUNE)
S.scene("最後のサビ", 24, "chorus", C_CH + C_CH[:8])
S.scene("チャイム", 8, "outro", ["C", "G", "D", "G", "C", "D", "G", "G"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="oboe", low=False)
BJ = S.track("バンジョー（ロール）", "banjo", volume=0.1, pan=0.3, reverb=0.2)
FID = S.track("フィドル", "fiddle", volume=0.12, pan=-0.2, reverb=0.3)
GT = [S.track(f"ナイロンギター{i + 1}", "guitar", patch="nylonGuitar", amp="crystal", volume=0.07, pan=-0.45, reverb=0.2, chorus=0, sustain=0.6) for i in range(4)]
GTS = S.track("ギター（ソロ）", "guitar", patch="nylonGuitar", amp="crystal", volume=0.11, pan=-0.2, reverb=0.25, chorus=0, sustain=0.6)
BASS = S.track("ウッドベース", "bass", **finger_bass_spec(vol=0.23))
CHIME = S.track("チャイム（グロッケン）", "glockenspiel", volume=0.06, pan=0, reverb=0.5)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:0.5 6:0.5 1':0.5 2':0.5 3':1", "2':0.5 1':0.5 2':1 R:2", "R:1 3':0.5 3':0.5 5':0.5 3':0.5 2':1", "1':2 R:2",
      "R:1 5:0.5 6:0.5 1':0.5 2':0.5 3':1", "5':0.5 3':0.5 5':1 R:2", "R:1 6':0.5 5':0.5 3':0.5 2':0.5 1':1", "2':2 R:2"]
A1 = ("くじのさんすうは/ねむくなるね/きょうかしょのすみに/らくがきした/"
      "ぼうにんげんとね/ちいさなねこ/ぱらぱらめくると/うごきだした")
A2 = ("ぼうにんげんがね/くちぶえふく/ききおぼえのふし/ねこもおどる/"
      "けいせんのうえで/つなわたりだ/すうじのいちまで/たちあがったよ")
VB = ["R:1 6':1 6':0.5 5':0.5 6':1", "5':2 R:2", "R:1 5':1 5':0.5 3':0.5 5':1", "6':2 R:2",
      "R:1 6':1 6':0.5 5':0.5 6':1", "5':2 3':1 R:1", "R:0.5 3':0.5 2':0.5 1':0.5 6:0.5 5:0.5 6:1", "R:4"]
B1 = "せんせいは/こくばんへ/いまのうちに/みんなでほら"
B2 = "ろけっとから/けむりでて/ぺーじのそら/とんでいくよ"
VC = ["5:0.5 5':0.5 5:0.5 5':0.5 6':1 5':1", "3':1.5 2':0.5 1':1 R:1", "4:0.5 4':0.5 4:0.5 4':0.5 5':1 4':1", "3':2 R:2",
      "5:0.5 5':0.5 5:0.5 5':0.5 6':1 5':1", "3':1 2':0.5 1':0.5 2':1 R:1", "R:0.5 6:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5 6:0.5", "1':2 R:2",
      "6:0.5 6':0.5 6:0.5 6':0.5 7':1 6':1", "5':1.5 3':0.5 2':1 R:1", "4:0.5 4':0.5 4:0.5 4':0.5 3':1 2':1", "1':2 R:2",
      "5:0.5 5':0.5 5:0.5 5':0.5 6':1 7':1", "6':1 5':0.5 3':0.5 5':1 R:1", "R:0.5 2':0.5 3':0.5 2':0.5 1':0.5 6:0.5 5:0.5 6:0.5", "1':3 R:1"]
C1 = ("らくがきこうしんだ/ぺーじをこえて/すうじもいっしょにおどる/いちにさんしごー/"
      "らくがきこうしんだ/とまらないんだ/きょうしつのそとまでね/ぱれーどしてるよ")
C2 = ("らくがきこうしんだ/ぺーじをこえて/くちぶえのあのふしで/みんなでうたうよ/"
      "らくがきこうしんだ/まだまだつづく/せんせいがふりむいた/ぴたりととまったよ")
C3 = ("らくがきこうしんだ/またうごきだす/ちゃいむがなるまでずっと/ちいさななかまだ/"
      "らくがきこうしんだ/ぺーじとじても/あしたのじゅぎょうでまた/あおうねきっとだよ/"
      "らくがきこうしんだ/またあしただよ/きょうかしょのすみっこでね/まっていてくれるよ")
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA + VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC + VC[:8], C3)

# ================= バンジョー・ギター・フィドル =================
def roll(b, ch):
    """バンジョーの3本指のロール（16分ではなく8分。160 なので細かすぎない）"""
    t = tones(ch, "G3", "G5")
    seq = [t[q % len(t)] for q in (2, 1, 0, 3, 1, 0, 2, 4)]
    BJ.bar(b, " ".join(f"{nm(x)}:0.5" for x in seq))


def boomchuck(b, ch):
    """ギターのブン・チャッ（1・3拍は低音、2・4拍は和音）"""
    r = low(ch, "E2"); v = voice(ch, 60, 3)
    GT[0].bar(b, f"{nm(r)}:1 R:1 {nm(r + 7)}:1 R:1")
    for j in range(3): GT[j + 1].bar(b, f"R:1 {nm(v[j])}:0.5 R:0.5 R:1 {nm(v[j])}:0.5 R:0.5")


FTUNE = ["D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:1 E5:1", "G5:1 E5:0.5 D5:0.5 C5:1 E5:1", "D5:0.5 B4:0.5 A4:0.5 G4:0.5 B4:1 D5:1", "A4:2 F#4:1 R:1",
         "D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:1 E5:1", "G5:1 E5:0.5 D5:0.5 C5:1 E5:1", "D5:0.5 C5:0.5 B4:0.5 A4:0.5 F#4:1 A4:1", "G4:3 R:1"]
MOTIF = ["R:1 B4:0.5 D5:0.5 E5:1 D5:0.5 A4:0.5", "G4:3 R:1"]     # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "バンジョー": roll(b, ch)
    elif n == "イントロ":
        roll(b, ch); boomchuck(b, ch); FID.bar(b, FTUNE[i])
    elif n in ("Aメロ1", "Aメロ2"):
        boomchuck(b, ch)
        if n == "Aメロ2" or i >= 8: roll(b, ch)
        if i % 4 == 3: FID.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "D5", "D6")[:4]))
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: boomchuck(b, ch); roll(b, ch)
        if i < 7: FID.bar(b, f"{nm(voice(ch, 72, 1)[0])}:4")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        boomchuck(b, ch); roll(b, ch)
        if i % 4 == 3: FID.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "D5", "D6")[:4]))
    elif n == "ソロ回し1":
        boomchuck(b, ch)
        if i < 8:   # バンジョーのソロ
            t = tones(ch, "G4", "G6"); BJ.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 2, 1, 3, 5, 3)))
        else:       # フィドルのソロ（最初の2小節が節）
            FID.bar(b, MOTIF[i - 8] if i < 10 else FTUNE[i - 8]); roll(b, ch)
    elif n == "先生がふりむく":
        if i == 3: FID.bar(b, "R:3 D5:1")
    elif n == "ソロ回し2":
        boomchuck(b, ch) if i >= 8 else None
        if i < 8:   # ギターのソロ
            GTS.bar(b, ["G4:0.5 A4:0.5 B4:0.5 D5:0.5 E5:1 D5:1", "C5:1 E5:1 G5:2", "D5:0.5 B4:0.5 G4:0.5 B4:0.5 D5:2", "A4:1 B4:0.5 A4:0.5 F#4:2",
                        "G4:0.5 B4:0.5 D5:0.5 G5:0.5 E5:1 D5:1", "C5:0.5 D5:0.5 E5:0.5 G5:0.5 E5:2", "D5:1 C5:0.5 B4:0.5 A4:1 F#4:1", "G4:3 R:1"][i])
            r = low(ch, "E2"); GT[0].bar(b, f"{nm(r)}:1 R:1 {nm(r + 7)}:1 R:1")
        else:       # フィドルとバンジョーのかけ合い（1小節ずつ）
            if i % 2 == 0: FID.bar(b, FTUNE[i - 8])
            else: t = tones(ch, "G4", "G6"); BJ.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (4, 3, 2, 1, 0, 1, 2, 3)))
    elif n == "チャイム":
        if i < 6: boomchuck(b, ch); roll(b, ch)
        if i < 4: FID.bar(b, FTUNE[i + 4])
        if i == 6:
            v = voice(ch, 62, 3)
            for j in range(3): GT[j + 1].bar(b, f"{nm(v[j])}:4")

CHIME.bar(S.sc("チャイム")[6], "D6:1 B5:1 G5:2"); CHIME.bar(S.sc("チャイム")[7], "A5:1 D6:3")    # 授業の終わりのチャイム（3つの音の自作）

# ================= ウッドベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("先生がふりむく",): continue
    if n == "Bメロ1" or n == "Bメロ2":
        if i < 7: BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    elif n == "チャイム":
        if i < 7: BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i < 6 else f"{nm(r)}:4")
    elif n != "バンジョー" or i >= 2:
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i % 4 != 3 else bass_line(S, b, "walk", lo="E1"))

# ================= ドラム（ブラシのような軽い2ビート）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("バンジョー", "先生がふりむく"): continue
    if n == "イントロ" and i < 4: continue
    if n in ("Bメロ1", "Bメロ2") and i == 7: continue
    if n == "チャイム" and i >= 6:
        if i == 6: crash(D, b, "C2", 6)
        continue
    hh = "x.x.x.x.x.x.x.x." if n in ("サビ1", "サビ2", "最後のサビ") else "x...x...x...x..."
    vgroove(D, b, "beat8", ghosts=0.15, seed=b, k="X.......X.......", s="....x.......x...", h=hh)
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 0: crash(D, b)
    if n in ("Bメロ1", "Bメロ2") and i == 6: put_fill(D, b, "small")

SIL.add(S.sc("Bメロ1")[-1], 0, 4); SIL.add(S.sc("Bメロ2")[-1], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の10（9時）。ブルーグラス。G長調・160。算数の授業中、教科書の落書きが動き出して行進する。"
          "バンジョーのロール・フィドル・ナイロンギターのブン・チャッ・ウッドベース、楽器ごとのソロ回し。先生がふりむくと全員止まる。"
          "合いことばの節はソロ回し1のフィドル。授業の終わりのチャイムで終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"先生がふりむく": -0.8, "最後のサビ": 0.35})
