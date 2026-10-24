# vp25 16「縁側と昼寝の猫」The Cat Napping on the Veranda（仮）— ヒップホップ（ブーンバップ）。E♭長調・88（はねる）・4/4。主役の楽器: クラリネット
# 物語: 夏の昼下がり、縁側で猫が昼寝。のびをして、毛づくろい。急に何かを見つけて走り出す（ほんの数秒）。戻ってきてまた丸くなり、
#   魚の夢を見る。あくびをひとつして、また眠る。
# 形: 猫の気まぐれ: 寝る→伸び→毛づくろい→急に走り出す→戻る→夢→あくび→また寝る
# 場面と強さ: 寝る＝キックとベースだけで小さい／走り出す＝一瞬だけ倍の速さで最大（8小節）／夢＝ふわっと／最後はいびき（ベースの長い音）
# 旋律の性格: 後ろにもたれた3連と休符、ため息のような下降（クラリネット）
# 崩す所: ブーンバップの途中で一瞬だけ倍速のトラップになる
from vp25_lib import *

S = Song("16", "hirune", "縁側と昼寝の猫（仮）", "The Cat Napping on the Veranda", 88, 4, "Eb", "major", "ヒップホップ（ブーンバップ）")
S.kit = "naked"
K = S.key
LOOP = ["Abmaj7", "Gm7", "Cm7", "F9"]
LOOP2 = ["Abmaj7", "Bb/Ab", "Gm7", "C7"]
RUN = ["Fm7", "Bb7", "Ebmaj7", "C7"]
DREAM = ["Bmaj7", "Bbm7", "Ebm7", "Abmaj7"]
S.scene("寝る", 12, "intro", LOOP)
S.scene("伸び", 12, "verse", LOOP)
S.scene("毛づくろい", 16, "verse", LOOP2)
S.scene("走り出す", 8, "chorus", RUN)
S.scene("戻る", 12, "pre", LOOP)
S.scene("夢", 16, "bridge", DREAM)
S.scene("あくび", 8, "verse", LOOP2)
S.scene("また寝る", 12, "outro", LOOP)
S.extra.update({"swing": 0.42})
S.flags = "--bass rubner " + S.flags
T3, T3b = "0.3333", "0.3334"

CL = S.track("主役: クラリネット", "panflute", patch="clarinet", volume=0.25, pan=-0.05, reverb=0.3, gainDb=6, phrase=4, mono=True,
             fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 1}])
EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.11, pan=[-0.35, 0.35, 0.0, 0.15][i], reverb=0.2, sustain=1.2,
              fx=[{"type": "tremolo", "rate": 4, "depth": 0.15}]) for i in range(4)]
BASS = S.track("ウッドベース", "bass", volume=0.22, pan=0, duck=0.0)
SUB = S.track("808（走る所だけ）", "sub808", **sub_spec(0.22))
VIB = S.track("夢のベル", "fmBell", volume=0.1, pan=0.4, reverb=0.45, sustain=2.0)
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("chiff", vol=0.15, pan=0.1, delay=0.75))
D = S.drumkit()

# ---------- クラリネット（ため息の下降、もたれた3連） ----------
SIGH = ["5':1.5 4':0.5 3':1 2':1", "1':2 R:2", f"R:1 6:{T3} 5:{T3} 3:{T3b} 2:1.5", "R:4"]
STRETCH = ["R:0.5 1:0.5 3:0.5 5:0.5 1':2", "7:1 6:0.5 5:0.5 3:2", "R:0.5 2:0.5 4:0.5 6:0.5 1':1 7:1", f"6:1 5:{T3} 4:{T3} 3:{T3b} 2:2",
           "R:0.5 3:0.5 5:0.5 7:0.5 2':2", "1':1 7:0.5 6:0.5 5:2", f"R:1 3':{T3} 2':{T3} 1':{T3b} b7:1 6:1", "5:4"]
GROOM = [f"3':0.5 2':0.25 1':0.25 7:0.5 1':0.5 R:2", f"R:2 5:{T3} 6:{T3} 7:{T3b} 1':1", "2':0.5 1':0.25 7:0.25 6:0.5 7:0.5 R:2", f"R:2 4:{T3} 5:{T3} 6:{T3b} b7:1",
         "1':0.75 7:0.25 6:0.5 5:0.5 3:1 R:1", "R:1 2:0.5 3:0.5 5:1 6:1", "5:0.5 3:0.5 2:0.5 1:0.5 b7,:1 R:1", "R:4"]
for i, b in enumerate(S.sc("寝る")):
    if i < 4: CL.bar(b, K.mel(SIGH[i], oct=4))
    elif i >= 8: CL.bar(b, K.mel(SIGH[i % 4], oct=4))
for i, b in enumerate(S.sc("伸び")): CL.bar(b, K.mel(STRETCH[i % 8], oct=4))
for i, b in enumerate(S.sc("毛づくろい")): CL.bar(b, K.mel(GROOM[i % 8], oct=4 if i < 8 else 5))
# 走り出す: リードの速い16分
RUNM = ["5:0.25 6:0.25 1':0.25 2':0.25 3':0.5 2':0.25 1':0.25 6:0.5 5:0.5 3:0.5 5:0.5", "4:0.25 5:0.25 6:0.25 1':0.25 2':0.5 1':0.25 6:0.25 5:1 R:1",
        "3:0.25 5:0.25 6:0.25 1':0.25 3':0.5 2':0.25 1':0.25 7:0.5 6:0.5 5:0.5 3:0.5", "#4:0.25 5:0.25 6:0.25 7:0.25 1':1 R:2"]
for i, b in enumerate(S.sc("走り出す")): LEAD.bar(b, K.mel(RUNM[i % 4], oct=4 if i < 4 else 5))
for i, b in enumerate(S.sc("戻る")): CL.bar(b, K.mel(SIGH[i % 4] if i < 4 else STRETCH[(i - 4) % 8], oct=4))
# 夢: 魚の夢（ベルとクラリネットの長い音、調が変わる）
DR = ["F#5:2 D#5:2", "Db5:4", "Gb5:2 F5:2", "Bb4:4", "C5:2 Eb5:2", "C5:3 R:1", "D#5:2 C#5:1 B4:1", "Bb4:4"]
for i, b in enumerate(S.sc("夢")):
    if i < 8: VIB.bar(b, " ".join(f"{nm(m)}:1" for m in tones(S.chords[b], "Eb5", "Eb6")[:4]))
    else: CL.bar(b, DR[i - 8])
for i, b in enumerate(S.sc("あくび")): CL.bar(b, K.mel(["5':3 1':1", "R:4", "6:2 5:1 3:1", "2:4", "5':2 3':2", "2':4", "1':2 6:2", "5:4"][i], oct=4))
for i, b in enumerate(S.sc("また寝る")):
    if i < 4: CL.bar(b, K.mel(SIGH[i], oct=4))

# ---------- エレピ（2小節のループ。7th の和音を、後ろにもたれて） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("寝る",) and i < 4: continue
    v = voice(S.chords[b], 62, 4)
    if n == "走り出す": pat = "X:0.5 R:0.25 X:0.25 R:0.5 X:0.5 R:1 X:0.5 R:0.5"
    elif n == "夢": pat = "X:4"
    elif n == "また寝る" and i >= 8: pat = "X:4" if i == 8 else "R:4"
    else: pat = "R:0.25 X:1.25 R:0.5 X:0.75 X:1.25" if i % 2 == 0 else "X:1.5 R:0.5 X:2"
    for j in range(4): EP[j].bar(b, pat.replace("X", nm(v[j], True)))

# ---------- ベース（丸いウッドベース。走る所だけ 808） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n == "走り出す":
        SUB.bar(b, f"{nm(r, True)}:1.5 {nm(r, True)}:0.5 R:0.5 {nm(r + 12, True)}:0.5 {nm(r, True)}:1"); continue
    if n == "また寝る" and i >= 8:
        if i == 8: BASS.bar(b, "Eb1:16")      # いびき（長い音）
        continue
    if n == "寝る" and i < 4: continue
    nx = low(S.chords[b + 1], "E1") if b + 1 < S.nb else r
    ap = nx - 1 if nx > r else nx + 1
    BASS.bar(b, f"{nm(r, True)}:1.25 R:0.25 {nm(r, True)}:0.5 R:1 {nm(r + 7, True)}:0.5 {nm(ap, True)}:0.5" if n != "夢" else f"{nm(r, True)}:2 {nm(r + 7, True)}:2")

# ---------- ドラム（ブーンバップ。走る所は倍速のトラップ） ----------
BBK = ["X.........X..x..", "X......x..X.....", "X.........X.x...", "X..x......X....."]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "寝る":
        if i >= 4: D.set(b, BBK[i % 4], "." * 16 if i < 8 else "....X.......X...", "x.x.x.x.x.x.x.x." if i >= 8 else "." * 16)
        continue
    if n in ("伸び", "毛づくろい", "戻る", "あくび"):
        put_groove(D, b, (BBK[i % 4], "....X.......X...", "x.x.x.x.x.x.x.xO" if i % 4 == 3 else "x.x.x.x.x.x.x.x."), ghosts=0.6, seed=b, hat_vary=False)
        if i % 8 == 7: put_fill(D, b, "small")
        if n == "毛づくろい" and last: D.set(b, "X.......X.......", "....X...X.X.XXXX", "x.x.x.x.........")
        continue
    if n == "走り出す":
        # 倍速のトラップ: キックが2拍ごと、スネアが2拍目と4拍目＋32分のハット
        D.set(b, "X.....X.X.....X.", "....X.......X...", "xxxxxxxxxxxxxxxx" if i % 2 else "x.xxx.xxx.xxxxxx")
        if i == 0: crash(D, b, "C2")
        if last: D.set(b, "X...............", "X...............", "." * 16)
        continue
    if n == "夢":
        if i >= 8: D.set(b, "X.........X.....", "." * 16, "." * 16); D.cym(b, "D2:1 D2:1 D2:1 D2:1")
        continue
    if n == "また寝る" and i < 8:
        D.set(b, BBK[i % 4], "....X.......X..." if i < 4 else "." * 16, "x...x...x...x..." if i < 6 else "." * 16)

S.desc = ("仮: ボカロ曲のインスト25曲の16。ブーンバップのヒップホップ。E♭長調・88（はねる）。主役の楽器はクラリネット。夏の昼下がり、縁側で昼寝する猫の気まぐれ。"
          "寝る→伸び→毛づくろい→急に走り出す（8小節だけ倍速のトラップ）→戻る→魚の夢（調が変わる）→あくび→また寝る（いびきのベースの長い音）。"
          "クラリネットは後ろにもたれた3連と、ため息のような下降。自作")
S.write()
