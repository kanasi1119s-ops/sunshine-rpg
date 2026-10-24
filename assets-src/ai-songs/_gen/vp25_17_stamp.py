# vp25 17「商店街スタンプラリー」The Shopping Street Stamp Rally（仮）— ヒップホップ（トラップ寄り）。F#長調・140（半分の速さで感じる）・4/4。主役の楽器: 三味線
# 物語: 夏祭りの日の商店街スタンプラリー。八百屋・パン屋・駄菓子屋・魚屋・花屋・本屋と、店を一軒ずつ回ってスタンプを押す（ポン！）。
#   全部そろったら福引。ガラガラと回して、玉がころころ…大当たり！
# 形: 店を一軒ずつ回る。店ごとにビートが変わり、スタンプの「ポン」で区切る。最後は福引
# 場面と強さ: 店ごとに違う（八百屋＝元気、パン屋＝ふんわり、駄菓子屋＝にぎやか、魚屋＝威勢がいい、花屋＝やさしい、本屋＝静か）／
#   福引の玉が転がる間＝ほぼ無音の緊張／大当たり＝最大（それまでの店の動機が全部重なる）
# 旋律の性格: ラップのような同じ音の16分のシンコペを、リードが言葉のように弾く。三味線は店ごとの動機
# 崩す所: 店が変わるたびにビートの型を丸ごと替える（ループ感をなくす）
from vp25_lib import *

S = Song("17", "stamp", "商店街スタンプラリー（仮）", "The Shopping Street Stamp Rally", 140, 4, "F#", "major", "ヒップホップ（トラップ）")
K = S.key
SHOPS = [("八百屋", ["F#", "D#m7", "B", "C#"]), ("パン屋", ["Bmaj7", "A#m7", "G#m7", "C#7sus4"]), ("駄菓子屋", ["F#", "G#7", "B", "C#"]),
         ("魚屋", ["D#m", "C#", "B", "A#7"]), ("花屋", ["G#m7", "C#7", "F#maj7", "D#m7"]), ("本屋", ["Bmaj7", "C#7sus4"])]
S.scene("ガラガラ", 4, "intro", ["C#7sus4"] * 4)
for name, ch in SHOPS: S.scene(name, 20 if name != "本屋" else 16, "verse" if name != "駄菓子屋" else "chorus", ch)
S.scene("福引", 12, "break", ["C#7sus4"] * 12)
S.scene("大当たり", 32, "chorus", ["F#", "A#7", "D#m", "F#7", "B", "Bm", "F#/C#", "C#7"])
S.scene("余韻", 4, "outro", ["F#"] * 4)
S.drum_gain = {"kick": {"gainDb": -6}}

SH = S.track("主役: 三味線", "shamisen", volume=0.27, pan=-0.12, reverb=0.2, gainDb=6,
             fx=[{"type": "eq", "low": -4, "mid": 3, "midHz": 2500, "high": 1}, {"type": "room", "mix": 0.15}])
SH2 = S.track("三味線（合いの手）", "shamisen", volume=0.18, pan=0.4, reverb=0.25, gainDb=3,
              fx=[{"type": "eq", "low": -4, "mid": 3, "midHz": 2800, "high": 1}])
RAP = S.track("リード（ラップのように）", "lead", **lead_spec("pluckSynth", vol=0.17, pan=0.05, delay=0.5))
SUB = S.track("808", "sub808", **sub_spec(0.22))
EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.1, pan=[-0.4, 0.4, 0.0][i], reverb=0.2, sustain=1.0) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.5, 0.5][i], duck=0.3)) for i in range(2)]
BELL = S.track("鐘（大当たり）", "bell", volume=0.15, pan=0.0, reverb=0.45, sustain=3.0)
POP = S.track("スタンプ（ポン）", "impactHit", volume=0.1, pan=0.0, reverb=0.2)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
D = S.drumkit()

# ---------- 店ごとの動機（三味線）と、ラップの句（リード） ----------
MOT = {"八百屋": "1':0.5 1':0.25 5:0.25 R:0.5 6:0.5 1':0.5 5:0.5 R:1", "パン屋": "3':1 2':0.5 1':0.5 5:2",
       "駄菓子屋": "5:0.25 6:0.25 1':0.25 6:0.25 5:0.25 3:0.25 5:0.5 R:0.5 1':0.5 2':0.5 3':0.5",
       "魚屋": "1':0.75 1':0.25 1':0.5 b7:0.5 1':1 R:1", "花屋": "3:1 5:1 6:0.5 5:0.5 3:1", "本屋": "5:2 3:2"}
RAPS = {"八百屋": ["3:0.25 3:0.25 3:0.25 R:0.25 3:0.25 3:0.25 5:0.5 R:0.5 3:0.25 3:0.25 2:0.5 1:0.5", "R:0.5 1:0.25 1:0.25 1:0.25 R:0.25 2:0.5 3:0.25 3:0.25 3:0.25 R:0.25 2:0.5 R:0.5"],
        "駄菓子屋": ["5:0.25 5:0.25 R:0.25 5:0.25 5:0.25 5:0.25 6:0.5 5:0.25 5:0.25 R:0.25 3:0.25 2:0.5 3:0.5", "R:0.25 6:0.25 6:0.25 6:0.25 5:0.5 3:0.5 R:0.25 5:0.25 5:0.25 5:0.25 6:0.5 1':0.5"],
        "魚屋": ["1':0.5 1':0.25 1':0.25 R:0.5 b7:0.25 b7:0.25 1':0.5 R:0.5 5:0.5 R:0.5", "R:0.5 5:0.25 5:0.25 6:0.5 1':0.25 1':0.25 R:0.5 1':0.25 b7:0.25 5:0.5 R:0.5"]}
for name, ch in SHOPS:
    bars = S.sc(name)
    for i, b in enumerate(bars):
        last = i == len(bars) - 1
        if last: continue
        m = MOT[name]
        # 動機を2小節ごとに、1回目はそのまま・2回目は高さを変えて
        SH.bar(b, K.mel(m if (i // 2) % 2 == 0 else seq_up(m, K, 2), oct=4) if i % 2 == 0 else "R:4")
        if name in RAPS and i >= 4: RAP.bar(b, K.mel(RAPS[name][i % 2], oct=4))
        if name == "パン屋" and i >= 4: SH2.bar(b, K.mel(["5:4", "4:2 3:2", "2:4", "1:2 R:2"][i % 4], oct=4))
        if name == "花屋" and i >= 4: SH2.bar(b, K.mel(seq_up(m, K, 4), oct=4) if i % 2 == 1 else "R:4")
        if name == "本屋": SH2.bar(b, "R:4")
    # 店の終わり: スタンプのポン
    POP.bar(bars[-1], "C3:1 R:3")
    SH.bar(bars[-1], K.mel("R:1 1':0.25 5:0.25 1:0.5 R:2", oct=4))
# ガラガラ（福引の音: 三味線の撥の速い連打）と福引
for i, b in enumerate(S.sc("ガラガラ")):
    SH.bar(b, " ".join(f"{nm(midi('C#5') + (q % 3) * 2)}:0.125," for q in range(16)) + " R:2")
for i, b in enumerate(S.sc("福引")):
    if i < 4: SH.bar(b, " ".join(f"{nm(midi('C#5') + (q % 3) * 2)}:0.125," for q in range(16)) + " R:2")
    elif i < 10: SH.bar(b, f"C#5:{[1, 1.5, 2, 2.5, 3, 4][i - 4]}, R:{4 - [1, 1.5, 2, 2.5, 3, 4][i - 4]}".replace(" R:0", "")) if i < 9 else SH.bar(b, "C#5:4,")
# 大当たり: 全部の店の動機が重なる
ORDER = ["八百屋", "駄菓子屋", "魚屋", "花屋"]
for i, b in enumerate(S.sc("大当たり")):
    SH.bar(b, K.mel(MOT[ORDER[(i // 2) % 4]], oct=4) if i % 2 == 0 else K.mel(MOT["駄菓子屋"], oct=5) if i >= 16 else "R:4")
    if i >= 8: RAP.bar(b, K.mel(RAPS[["八百屋", "駄菓子屋", "魚屋"][(i // 4) % 3]][i % 2], oct=5 if i >= 24 else 4))
    if i >= 16: SH2.bar(b, K.mel(MOT["花屋"], oct=5) if i % 2 == 1 else "R:4")
BELL.bar(S.sc("大当たり")[0], "F#5:2 C#6:2 F#6:4")
BELL.bar(S.sc("余韻")[0], "F#6:16")

# ---------- 店ごとのビート（丸ごと替える） ----------
BEATS = {
    "八百屋": ("X.....X...X.....", "........X.......", "x.x.x.x.x.x.x.x."),         # 元気: トラップの基本
    "パン屋": ("X.........X.....", "........X.......", "x...x...x...x..."),         # ふんわり: 少ない
    "駄菓子屋": ("X.X...X.X.X...X.", "....X.......X...", "xxxxxxxxxxxxxxxx"),       # にぎやか: 倍の細かさ
    "魚屋": ("X..X..X...X..X..", "........X.....X.", "x.x.xxx.x.x.xxx."),         # 威勢: 3+3+2
    "花屋": ("X.......X.......", "........X.......", "..x...x...x...x."),         # やさしい
    "本屋": ("X...............", "................", "x.......x......."),         # 静か
}
for name, ch in SHOPS:
    for i, b in enumerate(S.sc(name)):
        last = i == len(S.sc(name)) - 1
        if name in ("八百屋", "パン屋", "花屋", "本屋") and i < 2 and name != "八百屋": D.set(b, "X" + "." * 15, "." * 16, "." * 16); continue
        put_groove(D, b, BEATS[name], ghosts=0.3 if name in ("八百屋", "魚屋") else 0.0, seed=b, hat_vary=False)
        if name == "八百屋" and i % 4 == 3: D.H[b] = "x.x.x.x.x.xxxxxx"
        if name == "駄菓子屋" and i % 4 == 3: D.S[b] = "....X.......XxXX"
        if i == 2: D.cym(b, "A2:2 R:2")
        if last: D.set(b, "X" + "." * 15, "." * 16, "." * 16)
for i, b in enumerate(S.sc("大当たり")):
    put_groove(D, b, BEATS[["八百屋", "駄菓子屋", "魚屋", "八百屋"][(i // 8) % 4]], ghosts=0.3, seed=b, hat_vary=False)
    if i % 8 == 0: crash(D, b, "C2")
    if i % 8 == 7: D.S[b] = "........X.x.XXXX"
D.set(S.sc("余韻")[0], "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, S.sc("余韻")[0], "C2")
# 福引: ほぼ無音の緊張（ハットだけ、だんだん間があく）
for i, b in enumerate(S.sc("福引")):
    if i >= 4: D.set(b, h=["x.x.x.x.x.x.x.x.", "x...x...x...x...", "x.......x.......", "x...............", "x...............", "................", "................", "................"][i - 4])

# ---------- 808・エレピ・パッド ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in dict(SHOPS) or n == "大当たり":
        if i == L - 1 and n != "大当たり": continue
        pat = {"八百屋": "X:2.5 X:1.5", "パン屋": "X:4", "駄菓子屋": "X:1 R:0.5 X:0.5 X:1 X:1", "魚屋": "X:0.75 X:0.75 X:2.5", "花屋": "X:4", "本屋": "R:4", "大当たり": "X:1.5 X:1 X:1.5"}[n]
        SUB.bar(b, pat.replace("X", nm(r)))
        v = voice(S.chords[b], 62, 3)
        ep = {"パン屋": "X:4", "花屋": "X:2 X:2", "本屋": "X:4", "大当たり": "R:0.5 X:0.5 R:1 R:0.5 X:0.5 R:1"}.get(n, "R:0.75 X:0.25 R:1 R:0.75 X:0.25 R:1")
        for j in range(3): EP[j].bar(b, ep.replace("X", nm(v[j])))
        if n in ("パン屋", "花屋", "本屋"):
            pv = voice(S.chords[b], 56, 2)
            for j in range(2): PAD[j].bar(b, f"{nm(pv[j])}:4")
riser(FX, S.sc("大当たり")[0], 8, "D4")

S.desc = ("仮: ボカロ曲のインスト25曲の17。トラップ寄りのヒップホップ。F#長調・140（半分の速さで感じる）。主役の楽器は三味線。夏祭りの日の商店街スタンプラリー。"
          "八百屋・パン屋・駄菓子屋・魚屋・花屋・本屋と、店ごとにビートを丸ごと替え、スタンプの「ポン」で区切る。リードはラップのような同じ音の16分のシンコペ。"
          "福引の玉が転がる間はほぼ無音、大当たりで全部の店の動機が重なる。自作")
S.write()
