# vp25 09「ペダルを止めるな」Don't Stop Pedaling（仮）— ロック（ボカロロック）。E長調（最後の下り坂で F長調）・140→195・4/4。主役の楽器: ブラスセクション
# 物語: 夏休み、自転車で峠の上の展望台へ。長い上り坂をひと踏みずつ。頂上で一瞬、風だけ。帰りの下り坂は、ペダルを止めずに一気に駆け下りる。
# 形: 坂を上る（遅く重い）→頂上で一瞬止まる→下り坂を一気に（カーブを抜けて、もう一段速い所へ）→ブレーキ
# 場面と強さ: 上り＝ひと踏みごとに拍頭を強く、ためる（だんだん大きく）／頂上＝1小節の完全な無音と風／下り＝最大のまま止まらない／
#   カーブ＝体を傾ける一瞬の溜め（ギターのソロ）／ブレーキ＝全員の1発で着地
# 旋律の性格: 上りは4分の一歩ずつの上行、下りは16分の早口で駆け下りる
# 崩す所: 頂上で1小節の完全な無音（ロックの勢いをあえて切る）
from vp25_lib import *

S = Song("09", "pedal", "ペダルを止めるな（仮）", "Don't Stop Pedaling", 140, 4, "E", "major", "ロック")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
UP1 = ["E", "E/G#", "A", "B", "C#m", "B/D#", "E", "F#m7"]
UP2 = ["A", "B", "C#m", "D", "E", "F#m7", "G#m7", "B7sus4"]
DOWN = ["E", "B/D#", "C#m7", "C#m7/B", "Amaj7", "E/G#", "F#m7", "B7"]
CURVE = ["Cmaj7", "D", "E", "E", "Cmaj7", "D", "B", "B7"]
DOWN2 = [tr_chord(c, 1) for c in DOWN]
S.scene("スタート", 4, "intro", ["E"] * 4)
S.scene("上り坂1", 32, "verse", UP1)
S.scene("上り坂2", 24, "pre", UP2)
S.scene("頂上", 2, "break", ["B7sus4", "B7sus4"])
S.scene("下り坂1", 40, "chorus", DOWN)
S.scene("カーブ", 24, "solo", CURVE)
S.scene("下り坂2", 44, "chorus", DOWN2 + DOWN2 + DOWN2 + DOWN2 + DOWN2[:4])
S.scene("ブレーキ", 6, "outro", ["F", "F", "F", "F", "F", "F"])
b_down = S.sc("下り坂1")[0]
S.tempo = [{"bar": b_down + 1, "bpm": 195}, {"bar": S.sc("ブレーキ")[2] + 1, "bpm": 195}, {"bar": S.sc("ブレーキ")[3] + 1, "bpm": 150, "ramp": 2}]
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
K2 = K.up(1)

BR = [S.track(f"主役: ブラス{i + 1}", "brass", patch="brassSection", volume=0.2, pan=[-0.25, 0.25, 0][i], reverb=0.25, gainDb=4, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 1}]) for i in range(3)]
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.19, pan=0.0, delay=0.5))
LG = S.track("リードギター（カーブのソロ）", "distGuitar", **lead_gtr_spec(0.15, -0.1))
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.1, 0.0)) for i in range(3)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
PIANO = [S.track(f"ピアノ{i + 1}", "piano", **piano_spec(0.12, [-0.3, -0.2, -0.1][i])) for i in range(3)]
FX = S.track("効果音（風）", "pad", patch="fxRiser", volume=0.08, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- ギター（パワーコード） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    pw = power(S.chords[b], "E2")
    if n == "スタート": continue
    if n.startswith("上り坂"):
        # ひと踏みずつ: 1拍目と3拍目を伸ばす（上り坂2は8分を足す）
        pat = "X:2! X:2!" if n == "上り坂1" and i < 16 else ("X:1.5! X:0.5 X:2!" if n == "上り坂1" else "X:1! X:0.5 X:0.5 X:1! X:0.5 X:0.5")
    elif n == "頂上": continue
    elif n.startswith("下り坂"):
        pat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
        if i == L - 1: pat = "X:2! R:2"
    elif n == "カーブ":
        pat = "X:1.5! X:1 X:1.5!" if i % 4 != 3 else "X:0.5! X:0.5 X:0.5 X:0.5 X:2!"
    elif n == "ブレーキ":
        pat = "X:4!" if i < 2 else ("X:0.5! X:0.5 X:0.5 X:0.5 X:0.5 X:0.5 X:1" if i == 2 else ("X:4!" if i == 3 else "R:4"))
    for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ---------- 歌の役 ----------
UPM = ["1:1 2:1 3:1 4:1", "5:3 R:1", "6:1 5:1 4:1 6:1", "5:4", "3:1 4:1 5:1 6:1", "7:2 6:1 5:1", "5:1 6:1 7:1 1':1", "2':3 R:1"]
UPM2 = ["1':1 7:1 1':1 2':1", "3':3 R:1", "2':1 1':1 7:1 2':1", "1':4", "3':1 4':1 5':1 3':1", "4':2 3':1 2':1", "3':1 4':1 5':1 6':1", "7':2 6':2"]
for i, b in enumerate(S.sc("上り坂1")):
    if i >= 8: LEAD.bar(b, K.mel(UPM[i % 8], oct=4))
for i, b in enumerate(S.sc("上り坂2")):
    LEAD.bar(b, K.mel(UPM2[i % 8], oct=4) if i < 16 else K.mel(["1':1 2':1 3':1 4':1", "5':4", "6':2 5':2", "4':2 3':2", "5':4", "R:4", "R:4", "R:4"][i - 16], oct=4))
# 下り坂: 16分の早口で駆け下りる
DM = ["5':0.25 4':0.25 3':0.25 2':0.25 1':0.5 7:0.5 1':1 5:1", "R:0.5 5:0.25 6:0.25 7:0.5 2':0.5 1':0.25 7:0.25 6:0.25 5:0.25 4:1",
      "3':0.25 2':0.25 1':0.25 7:0.25 6:0.5 5:0.5 6:1 3:1", "R:0.5 3:0.25 4:0.25 5:0.5 1':0.5 7:0.25 6:0.25 5:0.25 4:0.25 3:1",
      "6:0.25 5:0.25 4:0.25 3:0.25 2:0.5 3:0.5 4:1 6:1", "5:0.5 4:0.25 3:0.25 2:0.5 1:0.5 3:1 5:1", "4:0.25 5:0.25 6:0.25 4:0.25 2:0.5 4:0.5 6:1 1':1", "7:2 R:1 5:0.5 7:0.5"]
DM2 = ["1'':0.25 7':0.25 6':0.25 5':0.25 3':0.5 2':0.5 3':1 1':1", "R:0.5 7:0.25 1':0.25 2':0.5 5':0.5 4':0.25 3':0.25 2':0.25 1':0.25 7:1",
       "6':0.25 5':0.25 4':0.25 3':0.25 2':0.5 1':0.5 2':1 6:1", "R:0.5 6:0.25 7:0.25 1':0.5 3':0.5 2':0.25 1':0.25 7:0.25 6:0.25 5:1",
       "4':0.25 3':0.25 2':0.25 1':0.25 6:0.5 1':0.5 4':1 6':1", "5':1 4':0.5 3':0.5 1':1 3':1", "2':0.5 3':0.5 4':0.5 6':0.5 5':1 4':1", "#4':2 7':2"]
for i, b in enumerate(S.sc("下り坂1")):
    if i < 8: continue
    LEAD.bar(b, K.mel((DM if (i // 8) % 2 == 1 else DM2)[i % 8], oct=4))
for i, b in enumerate(S.sc("下り坂2")):
    if i >= 40: LEAD.bar(b, K2.mel(["1'':4", "R:4", "5':2 6':2", "1'':4"][i - 40], oct=4)); continue
    LEAD.bar(b, K2.mel((DM2 if (i // 8) % 2 == 0 else DM)[i % 8], oct=4))
LEAD.bar(S.sc("ブレーキ")[0], K2.mel("1':4", oct=5))

# ---------- ブラス（主役）: 上りでは一歩ごとの和音のふくらみ、下りでは合いの手のフック ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 64, 3)
    if n == "上り坂1" and i < 8:
        # 歌が入る前は、ブラスが主役の旋律（一歩ずつ上る）
        m = K.mel(UPM[i], oct=4)
        BR[0].bar(b, m); BR[1].bar(b, transpose(m, -5) if i % 2 else K.mel(seq_up(UPM[i], K, -2), oct=4)); continue
    if n.startswith("上り坂"):
        pat = "X:2 X:2" if n == "上り坂1" else "X:1 R:0.5 X:0.5 X:2"
        for j in range(3): BR[j].bar(b, pat.replace("X", nm(v[j])))
    elif n.startswith("下り坂") or n == "スタート":
        if n == "スタート": continue
        if i < 8:
            # 下り坂の頭の8小節: ブラスがフック（同じ音の連打から跳ね上がる）
            hook = ["5':0.5 5':0.5 5':0.25 5':0.25 6':0.5 5':1 3':1", "4':0.5 4':0.5 4':0.25 4':0.25 5':0.5 4':1 2':1",
                    "3':0.5 3':0.5 3':0.25 3':0.25 4':0.5 3':1 1':1", "2':1 3':1 5':2"][i % 4]
            kk = K if n == "下り坂1" else K2
            BR[0].bar(b, kk.mel(hook, oct=4)); BR[1].bar(b, kk.mel(seq_up(hook, kk, -2), oct=4)); BR[2].bar(b, kk.mel(seq_up(hook, kk, -4), oct=4))
        else:
            # 歌の後ろ: 4拍目の裏から次の頭への「パッ」
            pat = "R:3.5 X:0.5" if i % 2 == 0 else "X:0.5 R:2 X:0.25 X:0.25 X:1"
            for j in range(3): BR[j].bar(b, pat.replace("X", nm(v[j])))
    elif n == "カーブ" and i >= 16:
        for j in range(3): BR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "ブレーキ" and i < 4:
        for j in range(3): BR[j].bar(b, ("X:4" if i in (0, 3) else "R:2 X:2").replace("X", nm(v[j])))

# ---------- カーブのギターソロ（体を傾けて曲がる） ----------
SOLO = ["5:1 6:0.5 7:0.5 1':1 7:0.5 6:0.5", "5:2 3:1 5:1", "6:0.5 7:0.5 1':0.5 2':0.5 3':1 2':1", "1':3 R:1",
        "5:0.5 6:0.5 1':0.5 2':0.5 3':0.5 5':0.5 3':1", "2':1 1':0.5 7:0.5 5:2", "4':0.25 3':0.25 2':0.25 1':0.25 7:0.5 1':0.5 2':2", "#4':4",
        "3':1 2':0.5 1':0.5 2':1 3':1", "4':2 3':2", "5':0.5 4':0.5 3':0.5 2':0.5 1':1 5:1", "6:3 R:1",
        "3':0.5 4':0.5 5':1 4':0.5 3':0.5 2':1", "1':2 5:2", "6:0.5 7:0.5 1':0.5 2':0.5 3':1 #4':1", "5':4"]
for i, b in enumerate(S.sc("カーブ")):
    if i < 16: LG.bar(b, K.mel(SOLO[i], oct=4))

# ---------- ピアノ（上り坂2と下り坂で8分の和音） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("上り坂2", "下り坂1", "下り坂2") and not (n.startswith("下り坂") and i < 8):
        v = voice(S.chords[b], 72, 3)
        pat = " ".join("X:0.5" for _ in range(8)) if n != "上り坂2" else "X:1 X:1 X:1 X:1"
        if i == L - 1 and n.startswith("下り"): pat = "X:2 R:2"
        for j in range(3): PIANO[j].bar(b, pat.replace("X", nm(v[j])))

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n == "スタート": continue
    if n == "上り坂1": BASS.bar(b, f"{nm(r)}:2! {nm(r)}:2!" if i < 16 else bass_line(S, b, "half")); continue
    if n == "上り坂2": BASS.bar(b, bass_line(S, b, "root8")); continue
    if n == "頂上": continue
    if n.startswith("下り坂"): BASS.bar(b, bass_line(S, b, "root8") if i != L - 1 else f"{nm(r)}:2! R:2"); continue
    if n == "カーブ": BASS.bar(b, bass_line(S, b, "push")); continue
    if n == "ブレーキ" and i < 4: BASS.bar(b, f"{nm(r)}:4!" if i in (0, 3) else " ".join(f"{nm(r)}:0.5" for _ in range(8)))

FX.bar(S.sc("頂上")[1], "A4:4")                # 頂上の風
cym_swell(CYM, b_down, 4, "E4")
cym_swell(CYM, S.sc("下り坂2")[0], 2, "C4")

# ---------- ドラム（生ドラム） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "スタート":
        D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        if i == 3: D.set(b, "X.......X.......", "....X...xxXXXXXX", "x.x.x.x.........")
        continue
    if n == "上り坂1":
        if i < 16:
            D.set(b, "X.......X.......", "....X.......X...", "X...x...X...x...")           # ひと踏みずつ（重く）
            if i >= 8: D.cym(b, "D2:1 D2:1 D2:1 D2:1")
        else:
            put_groove(D, b, ("X.......X.x.....", "....X.......X..o", "X.x.X.x.X.x.X.x."), ghosts=0.4, seed=b, hat_vary=False)
        if i in (0, 16): crash(D, b)
        if i % 8 == 7: put_fill(D, b, "tomdown" if i == 15 or last else "small")
        continue
    if n == "上り坂2":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.4, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "build")
        continue
    if n == "頂上": continue
    if n.startswith("下り坂"):
        put_groove(D, b, ("X.X...X.X.X...X." if i % 2 == 0 else "X.X...X.X...X.X.", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        ride = i >= 8 and (i // 8) % 2 == 1
        if ride:
            D.cym(b, ("C2:0.5 " if i % 8 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        elif i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        elif i % 4 == 3: put_fill(D, b, "small")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
        continue
    if n == "カーブ":
        put_groove(D, b, "half", ghosts=0.5, seed=b, hat_vary=False)
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if i % 8 == 7: put_fill(D, b, "tomtrip" if not last else "build")
        continue
    if n == "ブレーキ":
        if i in (0, 3): D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2"); D.cym(b, "G2:4")
        elif i == 2: D.set(b, "X...X...X...X...", "....X...XXXXXXXX", "." * 16)

S.desc = ("仮: ボカロ曲のインスト25曲の09。ボカロロック。E長調（最後の下り坂は F長調）。テンポは上り坂 140、下り坂 195。主役の楽器はブラスセクション。"
          "夏休み、自転車で峠の展望台へ。上り坂はひと踏みずつ（4分の一歩ずつ上る旋律と、1・3拍目の重いギター）、頂上で1小節の完全な無音と風、"
          "下り坂は16分の早口で駆け下りる。カーブでギターのソロ、最後はブレーキと全員の1発で着地。自作")
S.write()
