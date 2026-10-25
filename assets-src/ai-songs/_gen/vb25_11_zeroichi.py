# vb25 11「ゼロイチ・ワンダーランド」Zero-One Wonderland（仮）— エレクトロニカ（デジタルの世界）。E短調（サビは平行調の G長調）・154・4/4。最後のサビは +2（F#短調／A長調）
# 2026-10-25 人間「デジタルな感じの世界の曲も欲しいかも」→「25曲の中に入れる」「ふつうの曲」。前の 11（図書館の迷路）と入れかえた。
# 物語: 夜中、電源を入れたパソコンの中へ吸いこまれ、0と1の光の粒になって電子の街を旅する。データの川、ファイアウォールの壁、ネットの空、
#   キャッシュの迷路、バグの嵐をこえて、光回線の上を全速力で走り、朝にログアウトする。
# 場面と強さ: 起動（ベル1つ・小）→ ログイン（アルペジオとキック・中）→ データの川（Aメロ・語る）→ ファイアウォール（Bメロ・溜め・止め）
#   → ネットの空（サビ・強・4つ打ち）→ キャッシュの迷路（2番の前半はボーカルチョップ風が歌を受け取る）→ ファイアウォール2 → ネットの空2（ジャージークラブ）
#   → バグの嵐（グリッチ・スタッター・1拍の完全な無音）→ 再起動（Half feel・こもり）→ サーバーの夜景（アルペジオのソロ）→ 光回線（最後のサビ +2・最大）→ ログアウト
# 旋律の性格: 2進数のように同じ音の連打と、1オクターブの跳び（0と1）。Aメロは16分の早口、サビは高い所で短い句をくり返す。最高音 D6
from vb25_lib import *

S = Song("11", "zeroichi", "ゼロイチ・ワンダーランド（仮）", "Zero-One Wonderland", 154, 4, "E", "minor", "エレクトロニカ（ボカロ・デジタルの世界）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
K = S.key                    # E短調
KG = Key("G", "major")       # サビ
KA = Key("A", "major")       # 最後のサビ（+2）
KF = Key("F#", "minor")

A_CH = ["Em", "Em/D", "Cmaj7", "B7", "Em", "Em/D", "Am7", "B7sus4"]
B_CH = ["Cmaj7", "D", "Bm7", "Em", "Am7", "D", "A#dim", "B7"]                # A#dim＝♯iv°（次の Em への準備）
C_CH = ["Cmaj7", "D", "Bm7", "Em", "Cmaj7", "D", "G", "B/D#"]                # B/D#＝vi への副属和音
C_CH2 = ["Cmaj7", "D", "Bm7", "Em", "Am7", "D", "Gmaj7", "Gmaj7"]
BUG = ["Em", "F", "Em", "F", "Em", "F", "B7", "B7"]                           # F＝♭II（ナポリ。グリッチの不安定さ）
NIGHT = ["Am7", "Bm7", "Cmaj7", "D", "Am7", "Bm7", "Cmaj7", "D/F#"]
LAST = ["Dmaj7", "E", "C#m7", "F#m", "Dmaj7", "E", "A", "C#/F"]
LAST2 = ["Dmaj7", "E", "C#m7", "F#m", "Bm7", "E", "Amaj7", "Amaj7"]

S.scene("起動", 4, "intro", ["Em", "Em", "Cmaj7", "B7sus4"])
S.scene("ログイン", 8, "intro", A_CH)
S.scene("データの川", 16, "verse", A_CH)
S.scene("ファイアウォール", 8, "pre", B_CH)
S.scene("ネットの空", 16, "chorus", C_CH + C_CH2)
S.scene("キャッシュの迷路", 16, "verse", A_CH)
S.scene("ファイアウォール2", 8, "pre", B_CH)
S.scene("ネットの空2", 16, "chorus", C_CH + C_CH2)
S.scene("バグの嵐", 8, "break", BUG)
S.scene("再起動", 8, "bridge", NIGHT)
S.scene("サーバーの夜景", 16, "solo", NIGHT)
S.scene("光回線", 24, "chorus", LAST + LAST2 + LAST)
S.scene("ログアウト", 8, "outro", ["Amaj7", "E", "F#m", "D", "Amaj7", "E", "Amaj7", "Amaj7"])

V = Voice(S, vol=0.22, delay=0.75, patch="picoLeadRound")   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
ARP = S.track("デジタルのアルペジオ", "pad", patch="kawaiiArp", volume=0.075, pan=0.35, reverb=0.25,
              fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.3}])
ARP2 = S.track("アルペジオ（ソロ）", "lead", patch="modernPluck", volume=0.13, pan=-0.1, reverb=0.25, mono=True,
               fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
CHOP = S.track("ボーカルチョップ風", "pad", patch="vocalChop", volume=0.11, pan=-0.25, reverb=0.3)
FB = [S.track(f"フューチャーベースの和音{i + 1}", "pad", patch="fbChord", volume=0.055, pan=[-0.6, 0.6, 0][i], reverb=0.3, duck=0.5) for i in range(3)]
SAW = [S.track(f"厚い和音{i + 1}", "pad", patch="modernSupersaw", volume=0.045, pan=[-0.7, 0.7][i], reverb=0.3, duck=0.45) for i in range(2)]
PAD = [S.track(f"こもったパッド{i + 1}", "pad", patch="modernPad", volume=0.06, pan=[-0.5, 0.5][i], reverb=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 900, "q": 0.8}]) for i in range(2)]
BELL = S.track("ポップなベル（データの粒）", "bell", patch="popBell", volume=0.08, pan=0.25, reverb=0.45)
GLITCH = S.track("グリッチ（ビットの崩れ）", "lead", patch="chipPulse12", volume=0.07, pan=0.0, mono=True,
                 fx=[{"type": "bitcrusher", "bits": 6, "mix": 0.8}, {"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("modernBass", vol=0.21, duck=0.25))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律 =================
# Aメロ（E短調の度数）: 0と1のように、同じ音の連打とオクターブの跳び。16分の早口
AV = ["R:0.25 1:0.25 1:0.25 1':0.25 1:0.25 1:0.25 1':0.25 7:0.25 6:0.5 5:0.5 3:0.5 5:0.5",
      "R:0.25 4:0.25 4:0.25 4:0.25 5:0.25 4:0.25 3:0.5 R:0.25 1:0.25 2:0.25 3:0.25 2:1",
      "R:0.25 3:0.25 3:0.25 3':0.25 3:0.25 3:0.25 3':0.25 2':0.25 1':0.5 7:0.5 5:0.5 7:0.5",
      "#7:0.75 6:0.25 5:0.5 #4:0.5 #7,:1.5 R:0.5",
      "R:0.25 1:0.25 1:0.25 1':0.25 1:0.25 1:0.25 1':0.25 7:0.25 6:0.5 1':0.5 3':0.5 1':0.5",
      "R:0.25 2':0.25 2':0.25 2':0.25 1':0.25 7:0.25 6:0.5 R:0.25 5:0.25 6:0.25 7:0.25 1':1",
      "R:0.25 6:0.25 6:0.25 1':0.25 6:0.25 6:0.25 1':0.25 3':0.25 2':0.5 1':0.5 6:0.5 4:0.5",
      "4:0.5 5:0.5 #7:1 4:1 R:1"]
AV2 = AV[:6] + ["R:0.25 3':0.25 3':0.25 3':0.25 2':0.25 1':0.25 7:0.25 6:0.25 5:0.5 3:0.5 5:0.5 6:0.5", "#7:1.5 2':0.5 #7:1 R:1"]
VERSE = AV + AV2
# Bメロ: 壁に向かって少しずつ上がる。最後の小節は止め
BV = ["3:1 3:0.5 4:0.5 5:1 6:0.5 5:0.5", "6:1 6:0.5 7:0.5 1':1 2':1", "2':1 1':0.5 7:0.5 6:1 5:1", "5:1.5 6:0.5 7:2",
      "1':1 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "2':1 2':0.5 3':0.5 4':2", "#4':1 3':1 2':1 1':1", "#7:2 R:2"]
# サビ（G長調）: 高い所で短い句をくり返す（データの粒が空に散る）
CV = ["R:0.5 5:0.5 1':0.5 5:0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 6:0.5 3':2", "R:0.5 6:0.5 1':0.5 6:0.5 3':1 2':1", "1':0.5 7:0.5 6:0.5 7:0.5 5:2",
      "R:0.5 5:0.5 1':0.5 5:0.5 2':1 3':1", "4':1 3':0.5 2':0.5 1':1 2':1", "3':1 5':1 4':0.5 3':0.5 2':1", "#2':3 R:1"]
CV2 = CV[:6] + ["3':1 2':0.5 1':0.5 2':1 7:1", "1':4"]
CHORUS = CV + CV2
for name in ("データの川", "キャッシュの迷路"):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(VERSE[i], oct=4)
        if name == "キャッシュの迷路" and i < 8: CHOP.bar(b, line)         # 2番の前半はボーカルチョップ風が歌を受け取る
        else: V.bar(b, line)
for name in ("ファイアウォール", "ファイアウォール2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BV[i], oct=4))
for name in ("ネットの空", "ネットの空2"):
    for i, b in enumerate(S.sc(name)):
        V.bar(b, KG.mel(CHORUS[i], oct=4))
        if i % 4 == 3: CHOP.bar(b, KG.mel("R:2 5':0.25 R:0.25 5':0.25 3':0.25 1':1", oct=4))     # 合いの手
# 再起動: Half feel。長い音で、もう一度立ち上がる歌（こもり）
RV = ["3:2 5:2", "6:3 R:1", "1':2 7:1 6:1", "5:4", "3:2 5:2", "6:2 1':2", "2':2 3':2", "#4':4"]
for i, b in enumerate(S.sc("再起動")): V.bar(b, K.mel(RV[i], oct=4))
# 光回線（A長調。+2）: いちばん高い D6 へ
LV = CV + CV2[:6] + ["3':1 4':1 5':2", "3':4"] + CV[:6] + ["4':1 3':1 2':1 1':1", "1':4"]
for i, b in enumerate(S.sc("光回線")): V.bar(b, KA.mel(LV[i], oct=4))
for i, b in enumerate(S.sc("ログアウト")):
    if i < 4: V.bar(b, KA.mel(["5:2 3:2", "2:2 5,:2", "3:2 1:2", "1:4"][i], oct=5))

# ================= ソロ・グリッチ =================
SOLO = ["1:0.25 3:0.25 5:0.25 1':0.25 " * 2 + "2:0.25 4:0.25 6:0.25 2':0.25 " * 2,
        "3:0.25 5:0.25 7:0.25 3':0.25 " * 2 + "4:0.25 6:0.25 1':0.25 4':0.25 " * 2,
        "1':0.25 7:0.25 6:0.25 5:0.25 4:0.25 3:0.25 2:0.25 1:0.25 2:0.25 3:0.25 4:0.25 5:0.25 6:0.5 5:0.5",
        "3:1 R:0.5 5:0.25 6:0.25 7:1 1':1"]
for i, b in enumerate(S.sc("サーバーの夜景")):
    s_ = SOLO[i % 4].strip() if i < 12 else ["5':0.25 3':0.25 1':0.25 5:0.25 " * 4, "6':0.25 4':0.25 1':0.25 6:0.25 " * 4,
                                             "7':0.5 5':0.5 2':0.5 7:0.5 5:0.5 2:0.5 7,:1", "#4:4"][i - 12].strip()
    ARP2.bar(b, K.mel(s_, oct=4))
for i, b in enumerate(S.sc("バグの嵐")):
    if i % 2 == 0: GLITCH.bar(b, K.mel(" ".join(["1':0.125"] * 8 + ["b2':0.125"] * 8) + " R:2", oct=4))
    else: GLITCH.bar(b, K.mel("R:2 " + " ".join(["5:0.125", "1':0.125"] * 8), oct=4))
for name in ("ログイン", "データの川"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 7: GLITCH.bar(b, K.mel("R:3 " + " ".join(["1'':0.0625"] * 8) + " R:0.5", oct=4))   # 1拍だけのビットの崩れ

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 64, 3)
    t = tones(ch, "B4", "B6")
    # デジタルのアルペジオ（起動からずっと。バグの嵐と再起動では止まる）
    if n not in ("バグの嵐", "再起動", "サーバーの夜景") and not (n == "起動" and i < 2):
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 1, 3, 2, 4, 3, 1) * 2))
    # ベース
    if n in ("ログイン", "データの川", "キャッシュの迷路"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "oct8"))
    elif n.startswith("ファイアウォール"): BASS.bar(b, bass_line(S, b, "push" if i < 7 else "long"))
    elif n.startswith("ネットの空") or n == "光回線": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "バグの嵐": BASS.bar(b, bass_line(S, b, "half"))
    elif n in ("再起動", "サーバーの夜景"): BASS.bar(b, bass_line(S, b, "long" if n == "再起動" else "house"))
    elif n == "ログアウト" and i < 6: BASS.bar(b, bass_line(S, b, "half"))
    # フューチャーベースの和音（サビ）・厚い和音（光回線）
    if n.startswith("ネットの空") or n == "光回線":
        for j in range(3): FB[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5")
    if n == "光回線" or (n == "ネットの空2" and i >= 8):
        w = voice(ch, 60, 2, spread=True)
        for j in range(2): SAW[j].bar(b, f"{nm(w[j])}:4")
    # こもったパッド（起動・再起動・ログアウト）
    if n in ("起動", "再起動", "ログアウト", "サーバーの夜景"):
        w = voice(ch, 60, 2)
        for j in range(2): PAD[j].bar(b, f"{nm(w[j])}:4")
    # ベル（データの粒）
    if n in ("起動", "ネットの空", "ネットの空2", "光回線") and i % 2 == 1:
        BELL.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "B5", "B6")[:4]) + " R:2")
BELL.bar(0, "R:2 B5:2")
FX.bar(S.sc("ログイン")[0] - 1, "A4:4")
riser(FX, S.sc("ネットの空")[0] - 2, 8, "C4"); riser(FX, S.sc("ネットの空2")[0] - 2, 8, "C4"); riser(FX, S.sc("光回線")[0] - 4, 16, "D4")
cym_swell(CYM, S.sc("ネットの空")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("光回線")[0] - 1, 2, "C4")
FX.bar(S.sc("ログアウト")[-1], "E4:4")                  # 電源が落ちる（ダウンリフター）

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "起動":
        D.set(b, "................", "................", "................" if i < 2 else "x.x.x.x.x.x.x.x.")
    elif n == "ログイン":
        vgroove(D, b, "four", seed=b, s="................" if i < 4 else None)
        if last: put_fill(D, b, "snare16")
    elif n in ("データの川", "キャッシュの迷路"):
        vgroove(D, b, "twostep" if i < 8 else "four", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("ファイアウォール"):
        vgroove(D, b, "half" if i < 4 else "four16", ghosts=0.2, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n.startswith("ネットの空") or n == "光回線":
        name = "jersey" if (n == "ネットの空2" and i < 8) else "four16"
        vgroove(D, b, name, ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n != "光回線": put_fill(D, b, "tomdown")
    elif n == "バグの嵐":
        D.set(b, "X..X..X.X..X....", "....X.......X...", "xxxx....xxxx....")
        if i % 2 == 1: D.S[b] = "....X...xxxxXXXX"
    elif n == "再起動":
        vgroove(D, b, "half", seed=b, h="x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n == "サーバーの夜景":
        vgroove(D, b, "four", seed=b)
        if i == 0: crash(D, b)
        if i % 4 == 3: ride(D, b, "x.x.x.x.")
        if last: put_fill(D, b, "lift")
    elif n == "ログアウト":
        vgroove(D, b, "half", seed=b) if i < 6 else D.set(b, "X" + "." * 15, "." * 16, "." * 16)
        if i == 0: crash(D, b)

# こもり（再起動の場面は、ベルとアルペジオがないので、歌の役と和音だけ。光回線の前4小節）
muffle(S, [ARP2, BASS], S.sc("サーバーの夜景")[-4:], 800)
# 止めと1拍の完全な無音
for name in ("ファイアウォール", "ファイアウォール2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("バグの嵐")[-1], 3, 4)
SIL.apply()
S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の11。エレクトロニカ（デジタルの世界）。E短調（サビは G長調）・154、最後のサビは +2。"
          "夜中にパソコンの中へ吸いこまれ、0と1の光の粒になって電子の街を旅する。データの川・ファイアウォール・ネットの空・キャッシュの迷路・バグの嵐・"
          "再起動・サーバーの夜景・光回線をこえて、朝にログアウト。旋律は同じ音の連打とオクターブの跳び（0と1）。歌の役はクリアなポップのリード。自作")
vwrite(S)
