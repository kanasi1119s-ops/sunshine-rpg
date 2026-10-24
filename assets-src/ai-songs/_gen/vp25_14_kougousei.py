# vp25 14「葉っぱの光合成」A Leaf's Day of Photosynthesis（仮）— エレクトロニカ。C リディアン・8分＝224（付点のない 7/8）・7/8。主役の楽器: フルート
# 物語: 森の葉っぱ1枚の一日。朝露が光り、日が差すと少しずつ光をためて、真昼にいちばん元気に。午後は風にゆれ、夕方、夜は息をひそめる。
#   そしてまた朝露がひとしずく。
# 形: 葉1枚の一日（輪）: 朝露→光をためる→真昼→風→夕方→夜（息を止める）→朝露ふたたび
# 場面と強さ: 真昼＝いちばん大きいが、やわらかい（とがった音を使わない）／夜＝ほぼ無音（約30秒）／朝露＝1音
# 旋律の性格: 泡のように積み上がる7拍のアルペジオ（1小節ごとに1音ずつ増える）。フルートは息の長い旋律
# 崩す所: 夜の場面を、30秒近く無音に近い静けさにする
from vp25_lib import *

S = Song("14", "kougousei", "葉っぱの光合成（仮）", "A Leaf's Day of Photosynthesis", 224, 7, "C", "lydian", "エレクトロニカ（7/8）")
K = S.key
DEW = ["Cmaj7", "D/C", "Cmaj7", "D/C"]
LIGHT = ["Cmaj7", "D/C", "Bm7", "Em7", "Am7", "D", "Gmaj7", "D/F#"]
NOON = ["Cmaj7", "D/C", "Em7", "Bm7", "Cmaj7", "D", "Em7", "D/F#"]
WIND = ["Am7", "Bm7", "Cmaj7", "D"]
DUSK = ["Em7", "Cmaj7", "Am7", "D7sus4"]
S.scene("朝露", 8, "intro", DEW)
S.scene("光をためる", 32, "verse", LIGHT)
S.scene("真昼", 40, "chorus", NOON)
S.scene("風", 16, "bridge", WIND)
S.scene("夕方", 16, "verse", DUSK)
S.scene("夜", 16, "break", ["Cmaj7"] * 16)
S.scene("朝露ふたたび", 12, "outro", DEW * 3)
S.extra["grouping"] = [2, 2, 3]
B = 7

FL = S.track("主役: フルート", "panflute", patch="flute", volume=0.24, pan=0.0, reverb=0.4, gainDb=5, phrase=7, mono=True,
             fx=[{"type": "eq", "low": -4, "mid": 1.5, "midHz": 2000, "high": 1}])
ARP = [S.track(f"泡のアルペジオ{i + 1}", "pad", **pluck_spec(["pluckSynth", "glassPluck"][i], vol=[0.09, 0.07][i], pan=[-0.4, 0.45][i], delay=1.0, sustain=0.7)) for i in range(2)]
BELL = S.track("朝露（ベル）", "fmBell", volume=0.12, pan=0.3, reverb=0.5, sustain=2.0)
BASS = S.track("低音", "bass", **synth_bass_spec("synthBass1", vol=0.2, duck=0.15))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("newAge", vol=0.06, pan=[-0.5, 0.5, 0][i])) for i in range(3)]
DRONE = S.track("朝の空気（ドローン）", "pad", **pad_spec("halo", vol=0.07, pan=0.0, sustain=3.0))
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.15, pan=-0.1, delay=1.5))
D = S.drumkit()

# 光の強さ（小節ごと）
LIGHTV = []
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    LIGHTV.append({"朝露": 0.3, "光をためる": 0.4 + 0.5 * i / L, "真昼": 1.0, "風": 0.9, "夕方": 0.8 - 0.4 * i / L, "夜": 0.15, "朝露ふたたび": 0.3}[n])

# ---------- 泡のアルペジオ: 7拍（8分）。1小節ごとに1音ずつ増える ----------
ORDER = [0, 2, 4, 1, 3, 5, 6]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("夜",) or (n == "朝露ふたたび" and i >= 4) or n == "朝露": continue
    t = tones(S.chords[b], "C5", "C7")
    cnt = {"光をためる": min(7, 1 + i // 2), "真昼": 7, "風": 5, "夕方": max(1, 7 - i // 2)}.get(n, 3)
    toks = []
    for q in range(7):
        idx = ORDER[q]
        toks.append(f"{nm(t[idx % len(t)])}:1" if q < cnt else "R:1")
    ARP[0].bar(b, merge_rests(" ".join(toks)))
    if n == "真昼" or (n == "光をためる" and i >= 24):
        ARP[1].bar(b, " ".join(f"{nm(t[(ORDER[q % 7] + 2) % len(t)])}:0.5" if q % 2 == 0 else "R:0.5" for q in range(14)))

# ---------- フルート（息の長い旋律。2+2+3 の区切りに沿う） ----------
LM = ["3':2 4':2 5':3", "6':4 5':3", "3':2 2':2 7:3", "1':7", "2':2 3':2 4':3", "5':2 6':2 5':3", "3':4 2':3", "3':7"]
LM2 = ["5':2 6':2 7':3", "1'':4 7':3", "6':2 5':2 3':3", "5':7", "6':2 5':2 3':3", "2':2 3':2 4':3", "5':4 3':3", "2':7"]
for i, b in enumerate(S.sc("光をためる")):
    if i >= 8: FL.bar(b, K.mel(LM[i % 8], oct=4))
for i, b in enumerate(S.sc("真昼")):
    FL.bar(b, K.mel((LM2 if (i // 8) % 2 == 0 else LM)[i % 8], oct=4 if i < 24 else 5) if i < 32 else K.mel(["5':7", "3':4 2':3", "1':7", "R:7", "3':7", "4':4 5':3", "3':7", "R:7"][i - 32], oct=4))
    if 16 <= i < 32: LEAD.bar(b, K.mel(["1':7", "7:7", "6:7", "5:7", "6:7", "4:7", "5:7", "5:7"][i % 8], oct=4))
# 風: フルートの細かいゆれ（トリル風の16分）
for i, b in enumerate(S.sc("風")):
    t = tones(S.chords[b], "E5", "E6")
    FL.bar(b, " ".join(f"{nm(t[q % 2])}:0.25" for q in range(8)) + f" {nm(t[2])}:2 {nm(t[1])}:3" if i % 2 == 0 else f"{nm(t[-1])}:4 {nm(t[-2])}:3")
for i, b in enumerate(S.sc("夕方")):
    if i < 12: FL.bar(b, K.mel(["5':4 3':3", "2':7", "1':4 7:3", "6:7"][i % 4], oct=4))
# 朝露（ベル）と、最後の1音
for i, b in enumerate(S.sc("朝露")):
    BELL.bar(b, [f"G6:7", "R:7", f"R:4 E6:3", "R:7", "G6:3 R:4", "D6:7", "R:7", "E6:7"][i])
for i, b in enumerate(S.sc("朝露ふたたび")):
    if i in (0, 4): BELL.bar(b, "G6:7")
    if i == 8: FL.bar(b, K.mel("5':7", oct=4))         # 朝露の1音で輪を閉じる

# ---------- 低音・パッド・ドローン ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("光をためる", "真昼", "風"):
        if n == "光をためる" and i < 8: BASS.bar(b, f"{nm(r)}:7")
        else: BASS.bar(b, f"{nm(r)}:2 {nm(r)}:2 {nm(r + 7)}:3" if n != "風" else f"{nm(r)}:3 R:1 {nm(r + 12)}:1 {nm(r + 7)}:2")
    elif n == "夕方": BASS.bar(b, f"{nm(r)}:7")
    v = voice(S.chords[b], 58, 3)
    if n in ("光をためる", "真昼", "夕方", "風"):
        for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:7")
    if n in ("朝露", "夜", "朝露ふたたび"):
        if n == "夜" and i >= 12: continue
        DRONE.bar(b, "C4:7" if n != "夜" else "G3:7")

# ---------- ドラム（7/8: 2+2+3。キックはまとまりの頭、スネアは3つ目のまとまりの頭） ----------
K7 = "X.......X......." + "............"
S7 = "........" + "........" + "X..........."
H7 = "x...x...x...x...x...x...x..."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "光をためる" and i >= 16:
        D.set(b, "X......." + "........" + "x...........", "." * 28, H7 if i >= 24 else "." * 28)
    elif n == "真昼":
        D.set(b, K7 if i % 4 != 3 else "X.......X.......x.......x...", S7 if i % 8 != 7 else "........" + "....o.o." + "X...x.x.XXXX", H7.replace("x...", "x.o.", 3) if i % 2 else H7)
        if i % 8 == 0: D.cym(b, "D2:7")
    elif n == "風":
        D.set(b, "X......." + "........" + "............", "." * 28, "xoxoxoxoxoxoxoxoxoxoxoxoxoxo")
    elif n == "夕方" and i < 8:
        D.set(b, "X......." + "........" + "............", "." * 28, "x.......x.......x...........")

S.flags += " --space vale --space-wet 0.18"
S.desc = ("仮: ボカロ曲のインスト25曲の14。エレクトロニカ。C リディアン（明るい 4 の音）。7/8（2+2+3、8分＝224）。主役の楽器はフルート。森の葉っぱ1枚の一日。"
          "朝露→光をためる（7拍のアルペジオが1小節ごとに1音ずつ増える）→真昼（いちばん大きいが、やわらかい）→風（細かいゆれ）→夕方→夜（約30秒のほぼ無音）→朝露ふたたび、フルートの1音で輪を閉じる。自作")
S.write()
