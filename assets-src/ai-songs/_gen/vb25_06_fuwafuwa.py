# vb25 06「ふわふわ現象論」Fluffy Phenomenon Theory（仮）— ダンス（フューチャーベース）。B長調（サビ・ドロップは G#短調）・150・4/4
# 物語: ある朝、町じゅうの雲が綿あめになっていた。ためしに一歩ふみ出すと、ふわっと体が浮く。ランドセルをしょって、雲から雲へ歩いて学校へ。
#   鳥と並んで歩き、ドロップで雲のいちばん上へ。途中で雲が切れて、はるか下に自分の町が見えて、足がすくむ。もう一度上を向いて、最後は全部の雲の上へ。
# 場面と強さ: 短いサビ（ドロップの先取り）→ 綿あめの朝（Aメロ・歌の役と声のチョップの掛け合い）→ 足元ふわふわ（Bメロ・フィルターが閉じていく）
#   → 雲の上へ（1サビ＝ドロップ・4つ打ち・強）→ 鳥と並んで（間奏・ベルの主旋律）→ 雲の通学路（2番。前半はベルが歌を受け取る）→ Bメロ2
#   → 2サビ（Half feel のハーフ）→ 1拍の完全な無音 → 雲が切れて（静けさ・下が見える）→ 落ちサビ（ベルと歌だけ）
#   → もう一度上へ（フィルターが開いていく）→ 最後のドロップ（最大）→ 風の音だけ残す
# 旋律の性格: 歌の役が2拍歌うと、声のチョップが2拍で答える掛け合い。Aメロは16分の早口、ドロップは同じ音の3連打と6度の跳躍。最高音 C#6
# 派手な展開: サビごとのリズムの入れかえ（1サビはドロップの4つ打ち・2サビはハーフ）・Half feel・フィルターの開閉（Bメロで閉じ、最後の前で開く）・1拍の完全な無音
from vb25_lib import *

S = Song("06", "fuwafuwa", "ふわふわ現象論（仮）", "Fluffy Phenomenon Theory", 150, 4, "B", "major", "ダンス（フューチャーベース・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # B 長調（Aメロ・Bメロ）
KM = Key("G#", "minor")      # サビ・ドロップ（G# 短調）


def chk(*lists):
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


A_CH = ["Bmaj7", "D#m7", "Emaj7", "F#", "Bmaj7", "D#7", "G#m7", "F#sus4"]          # D#7＝vi（G#m）への副属和音
B_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "D#m7", "Emaj7", "F#"]
D_CH = ["Emaj7", "F#6", "D#m7", "G#m9", "Emaj7", "F#", "D#7", "G#m"]               # D#7＝G# 短調の V（長調の V）
GAP = ["Emaj9", "Emaj9", "C#m9", "C#m9", "Emaj9", "Emaj9", "C#m9", "D#7sus4"]
UP_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "D#m7", "Baug", "D#7"]             # Baug＝増三和音

S.scene("短いサビ", 8, "intro", D_CH)
S.scene("綿あめの朝", 16, "verse", A_CH)
S.scene("足元ふわふわ", 8, "pre", B_CH)
S.scene("雲の上へ", 16, "chorus", D_CH)
S.scene("鳥と並んで", 8, "interlude", D_CH)
S.scene("雲の通学路", 16, "verse", A_CH)
S.scene("足元ふわふわ2", 8, "pre", B_CH)
S.scene("ハーフのサビ", 16, "chorus", D_CH)
S.scene("雲が切れて", 8, "break", GAP)
S.scene("落ちサビ", 8, "bridge", D_CH)
S.scene("もう一度上へ", 8, "build", UP_CH)
S.scene("最後のドロップ", 32, "chorus", D_CH)
S.scene("風", 8, "outro", ["Emaj9", "Emaj9", "G#m9", "G#m9", "G#m9", "G#m9", "G#m9", "G#m9"])

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75)
CHOP = S.track("声のチョップ風シンセ", "lead", patch="chiff", volume=0.12, pan=0.12, reverb=0.2, mono=True, gainDb=1,
               fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "eq", "low": 0, "mid": 5, "midHz": 520, "high": 0},
                   {"type": "eq", "low": 0, "mid": 3.5, "midHz": 1150, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.7},
                   {"type": "pingpong", "beats": 0.5, "mix": 0.16, "feedback": 0.25}])
BELL = S.track("ベル（主旋律の受け渡し・きらめき）", "fmBell", volume=0.1, pan=-0.2, reverb=0.45, sustain=1.0)
SAW = [S.track(f"スーパーソウ{i + 1}", "pad", **pad_spec("supersawPad", vol=0.055, pan=0.0, duck=0.6, sustain=0.8)) for i in range(4)]
SAWC = [S.track(f"閉じたスーパーソウ{i + 1}（800Hz）", "pad", patch="supersawPad", volume=0.06, pan=0.0, reverb=0.35, sustain=0.8, duck=0.4,
                fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}]) for i in range(3)]
SAWH = [S.track(f"半分ひらいたスーパーソウ{i + 1}（2kHz）", "pad", patch="supersawPad", volume=0.058, pan=0.0, reverb=0.35, sustain=0.8, duck=0.5,
                fx=[{"type": "filter", "kind": "lowpass", "freq": 2000, "q": 0.9}]) for i in range(3)]
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.24, duck=0.35))
ARP = S.track("プラックのアルペジオ", "pad", **pluck_spec("pluckSynth", vol=0.075, pan=0.35, delay=0.75, sustain=0.5))
PAD = [S.track(f"雲のパッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.07, pan=0.0, duck=0.0, sustain=2.5)) for i in range(3)]
FX = S.track("効果音（風のノイズ・ライザー）", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.4)
CYM = S.track("シンバルの効果音（風のロール）", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役 =================
# Aメロ（B長調の度数。oct=3 で 1 = B3。B3 は使わず、1' = B4 を主音にする）: 前半は歌が2拍半、チョップが1拍で答える
A1 = ["R:0.25 5:0.25 5:0.25 6:0.25 1':0.25 1':0.25 7:0.25 6:0.25 5:0.5 3:0.5 R:1",
      "R:0.25 3:0.25 3:0.25 5:0.25 7:0.25 7:0.25 6:0.25 5:0.25 3:0.5 2:0.5 R:1",
      "R:0.25 4:0.25 4:0.25 6:0.25 1':0.25 1':0.25 2':0.25 1':0.25 7:0.25 6:0.25 4:0.5 R:1",
      "5:0.25 6:0.25 7:0.25 2':0.25 R:0.25 2':0.25 1':0.25 7:0.25 5:1 R:1",
      "R:0.25 1':0.25 1':0.25 2':0.25 3':0.25 3':0.25 2':0.25 1':0.25 7:0.5 5:0.5 R:1",
      "R:0.25 #5:0.25 #5:0.25 7:0.25 2':0.25 2':0.25 1':0.25 7:0.25 #5:0.5 3:0.5 R:1",
      "R:0.25 6:0.25 6:0.25 1':0.25 3':0.25 3':0.25 2':0.25 1':0.25 6:0.25 5:0.25 3:0.5 R:1",
      "5:0.5 4:0.5 2:0.5 4:0.5 5:2"]
# 後半: 歌が切れ目なく16分で（2度・6度・7度の跳びを混ぜる。歌いにくい所）
A1b = ["R:0.25 5:0.25 1':0.25 5:0.25 3':0.25 2':0.25 1':0.25 5:0.25 R:0.25 6:0.25 1':0.25 6:0.25 2':0.5 1':0.5",
       "R:0.25 3:0.25 7:0.25 3:0.25 2':0.25 1':0.25 7:0.25 3:0.25 R:0.25 5:0.25 7:0.25 5:0.25 1':0.5 7:0.5",
       "R:0.25 4:0.25 1':0.25 4:0.25 3':0.25 2':0.25 1':0.25 6:0.25 R:0.25 4:0.25 6:0.25 1':0.25 3':0.5 2':0.5",
       "1':0.5 7:0.25 6:0.25 5:0.5 2:0.5 R:0.25 2:0.25 5:0.25 6:0.25 7:1",
       "R:0.25 1':0.25 1':0.25 1':0.25 7:0.25 1':0.25 2':0.25 3':0.25 R:0.25 2':0.25 1':0.25 7:0.25 5:0.5 6:0.5",
       "R:0.25 #5:0.25 #5:0.25 #5:0.25 7:0.25 #5:0.25 3:0.25 #5:0.25 R:0.25 7:0.25 2':0.25 3':0.25 2':0.5 7:0.5",
       "6:0.25 7:0.25 1':0.25 3':0.25 2':0.5 1':0.5 6:0.25 5:0.25 3:0.25 5:0.25 6:1",
       "5:2 R:2"]
# 2番（雲の通学路）の後半: 1番より1段高く、短い句を詰める
A2b = ["R:0.25 3':0.25 3':0.25 2':0.25 1':0.25 7:0.25 1':0.25 2':0.25 R:0.25 3':0.25 2':0.25 1':0.25 5:0.5 1':0.5",
       "R:0.25 2':0.25 2':0.25 1':0.25 7:0.25 5:0.25 7:0.25 1':0.25 R:0.25 2':0.25 1':0.25 7:0.25 3:0.5 7:0.5",
       "R:0.25 1':0.25 1':0.25 7:0.25 6:0.25 4:0.25 6:0.25 7:0.25 R:0.25 1':0.25 2':0.25 3':0.25 4':0.5 3':0.5",
       "2':0.5 1':0.25 7:0.25 5:0.5 7:0.5 2':1 R:1",
       A1b[4], A1b[5], A1b[6],
       "5:1 7:1 2':1 R:1"]
# Bメロ（B長調）: 8分で上がる。最後の2小節でフィルターが閉じる
BM = ["4:0.5 6:0.5 1':0.5 3':0.5 3':1 2':1", "5:0.5 7:0.5 2':0.5 3':0.5 2':1 7:1", "3:0.5 5:0.5 7:0.5 2':0.5 3':1.5 2':0.5", "1':2 R:0.5 6:0.5 1':0.5 3':0.5",
      "2':1 3':0.5 4':0.5 6':1 4':1", "5':1 4':0.5 3':0.5 5':1 3':1", "4':1 5':0.5 6':0.5 1'':1.5 R:0.5", "7':3 R:1"]
BM2 = BM[:6] + ["4':0.5 5':0.5 6':0.5 7':0.5 1'':1 6':1", "7':2 5':1 R:1"]
# ドロップ（G# 短調の度数。oct=4 で 1 = G#4）: 歌が2拍、チョップが2拍で答える（前半）→ 歌が切れ目なく（後半）
DR = ["R:0.5 3':0.5 3':0.5 3':0.5 R:2", "R:0.5 2':0.5 2':0.5 2':0.5 4':1 7:1",
      "R:0.5 1':0.5 1':0.5 1':0.5 R:2", "R:0.5 3:0.5 1':0.5 3':0.5 2':2",
      "R:0.5 3':0.5 3':0.5 3':0.5 R:2", "R:0.5 2':0.5 2':0.5 2':0.5 4':1 7:1",
      "R:0.5 5:0.5 #7:0.5 2':0.5 4':1.5 2':0.5", "1':3 R:1",
      "R:0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':0.5 5:1", "R:0.5 2':0.5 2':0.5 2':0.5 1':0.5 7:0.5 2:1",
      "R:0.5 5:0.5 3':0.5 2':0.5 1':1 7:1", "1':0.5 7:0.5 3:0.5 1':0.5 5:2",
      "R:0.5 4':0.5 4':0.5 4':0.5 3':1 5:1", "R:0.5 2':0.5 2':0.5 2':0.5 4':1 2':1",
      "R:0.5 5:0.5 #7:0.5 2':0.5 4':1.5 2':0.5", "1':2 3:1 1':1"]
# 声のチョップの答え（ドロップの前半）: 16分の切れた声
CHR = ["R:2 3':0.25 3':0.25 R:0.25 1':0.25 7:0.25 1':0.25 3':0.5", "R:2.5 4':0.25 2':0.25 7:0.25 2':0.25 R:0.5",
       "R:2 1':0.25 1':0.25 R:0.25 5:0.25 7:0.25 5:0.25 1':0.5", "R:3 2':0.25 1':0.25 7:0.25 5:0.25",
       "R:2 3':0.25 3':0.25 R:0.25 4':0.25 3':0.25 1':0.25 5:0.5", "R:2.5 2':0.25 1':0.25 7:0.25 4:0.25 R:0.5",
       "R:3.5 #7:0.25 2':0.25", "R:3 5:0.25 7:0.25 1':0.25 3':0.25"]
# 最後のドロップの後ろ16小節: 歌とチョップが同時に、いちばん高い C#6 を何度も
LASTX = ["R:0.5 4':0.5 4':0.5 4':0.5 3':0.5 2':0.5 1':1", "R:0.5 4':0.5 4':0.5 4':0.5 2':1 7:1",
         "R:0.5 3':0.5 3':0.5 3':0.5 1':0.5 5:0.5 1':1", "3':1 5:1 1':2",
         "R:0.5 4':0.5 4':0.5 4':0.5 3':0.5 2':0.5 1':1", "R:0.5 4':0.5 4':0.5 4':0.5 2':1 4':1",
         "R:0.5 5:0.5 #7:0.5 2':0.5 4':2", "4':2 3':1 1':1"]
# 雲が切れて（静けさ）・落ちサビ: 長い音で（重ねなし）
GP = ["R:4", "R:2 3':1 2':1", "1':3 R:1", "R:2 5:1 7:1", "1':2 3':2", "2':3 R:1", "R:1 7:1 5:1 3:1", "5:4"]
chk(A1, A1b, A2b, BM, BM2, DR, CHR, LASTX, GP)

for i, b in enumerate(S.sc("綿あめの朝")): V.bar(b, K.mel((A1 + A1b)[i], oct=3))
for i, b in enumerate(S.sc("雲の通学路")):
    if i < 8: BELL.bar(b, K.mel(A1[i], oct=4))                          # 2番の前半は、ベルが歌を受け取る（1オクターブ上）
    else: V.bar(b, K.mel(A2b[i - 8], oct=3))
for i, b in enumerate(S.sc("足元ふわふわ")): V.bar(b, K.mel(BM[i], oct=3))
for i, b in enumerate(S.sc("足元ふわふわ2")): V.bar(b, K.mel(BM2[i], oct=3))
for name in ("雲の上へ", "ハーフのサビ"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KM.mel(DR[i], oct=4))
for i, b in enumerate(S.sc("短いサビ")): V.bar(b, KM.mel(DR[8 + i], oct=4))     # 始まりは、ドロップの後半を先取り
for i, b in enumerate(S.sc("雲が切れて")): V.bar(b, KM.mel(GP[i], oct=4), low=False)
for i, b in enumerate(S.sc("落ちサビ")): V.bar(b, KM.mel(DR[i], oct=4), low=False)
UPL = ["R:0.5 3:0.5 5:0.5 7:0.5 1':2", "R:0.5 2:0.5 4:0.5 6:0.5 7:2", "R:0.5 5:0.5 7:0.5 2':0.5 3':2", "R:0.5 1':0.5 3':0.5 5':0.5 4':2",
       "R:0.25 2:0.25 4:0.25 6:0.25 1':0.5 6:0.5 R:0.25 4:0.25 6:0.25 1':0.25 2':0.5 1':0.5",
       "R:0.25 3:0.25 5:0.25 7:0.25 2':0.5 7:0.5 R:0.25 5:0.25 7:0.25 2':0.25 3':0.5 2':0.5",
       "R:0.25 3:0.25 #5:0.25 1':0.25 3':0.5 1':0.5 R:0.25 #5:0.25 1':0.25 3':0.25 #5':0.5 3':0.5", "7':3 R:1"]
chk(UPL)
for i, b in enumerate(S.sc("もう一度上へ")): V.bar(b, K.mel(UPL[i], oct=3))
for i, b in enumerate(S.sc("最後のドロップ")): V.bar(b, KM.mel((DR + LASTX + DR[8:])[i], oct=4))

# ================= 声のチョップ =================
for name in ("雲の上へ", "最後のドロップ", "短いサビ"):
    for i, b in enumerate(S.sc(name)):
        if name == "短いサビ": CHOP.bar(b, KM.mel(CHR[i % 8], oct=4)); continue
        if i < 8 or (name == "最後のドロップ" and 16 <= i < 24): CHOP.bar(b, KM.mel(CHR[i % 8], oct=4))
for i, b in enumerate(S.sc("ハーフのサビ")):
    if i < 8: CHOP.bar(b, KM.mel(CHR[i % 8], oct=3))                     # ハーフでは1オクターブ下で答える
# Aメロ前半: 歌の休む最後の1拍に、チョップが答える
ANS = ["R:3 5:0.25 1':0.25 R:0.25 1':0.25", "R:3 3:0.25 7:0.25 R:0.25 7:0.25", "R:3 4:0.25 1':0.25 R:0.25 2':0.25", "R:3 5:0.25 7:0.25 2':0.25 R:0.25"]
for name in ("綿あめの朝",):
    for i, b in enumerate(S.sc(name)):
        if i < 7: CHOP.bar(b, K.mel(ANS[i % 4], oct=3))
# 間奏（鳥と並んで）: ベルの主旋律とチョップの掛け合い
BIRD = ["5':0.5 3':0.5 1':0.5 3':0.5 5':1 4':1", "3':0.5 2':0.5 1':0.5 7:0.5 2':2", "1':0.5 3':0.5 5':0.5 7':0.5 5':1 3':1", "4':1 3':0.5 2':0.5 #7:2"]
chk(BIRD)
for i, b in enumerate(S.sc("鳥と並んで")):
    BELL.bar(b, KM.mel(BIRD[i % 4], oct=4))
    CHOP.bar(b, KM.mel(["R:3 3':0.25 1':0.25 5:0.5", "R:3 2':0.25 7:0.25 4:0.5"][i % 2], oct=4))
# 落ちサビ: ベルが和音をゆっくり
for i, b in enumerate(S.sc("落ちサビ")):
    t = tones(S.chords[b], "G#4", "G#6"); BELL.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 3)))
for i, b in enumerate(S.sc("雲が切れて")):
    if i % 2 == 0: BELL.bar(b, KM.mel("5':1 3':1 1':2", oct=4))

# ================= 伴奏 =================
FB = "X:0.75 X:0.75 X:0.5 X:0.75 X:0.75 X:0.5"           # フューチャーベースの和音のノリ（3・3・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 4)
    drop = n in ("雲の上へ", "最後のドロップ", "短いサビ")
    if drop:
        for j in range(4): SAW[j].bar(b, FB.replace("X", nm(v[j])))
    elif n == "ハーフのサビ":
        for j in range(4): SAW[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:1.5 {nm(v[j])}:0.5")
    elif n.startswith("足元ふわふわ"):
        if i >= 6:
            for j in range(3): SAWC[j].bar(b, FB.replace("X", nm(v[j])))       # フィルターが閉じる（800Hz）
        elif i >= 4:
            for j in range(3): SAWH[j].bar(b, FB.replace("X", nm(v[j])))       # 半分閉じる（2kHz）
    elif n == "もう一度上へ":
        if i < 4:
            for j in range(3): SAWC[j].bar(b, FB.replace("X", nm(v[j])))       # 閉じた所から
        else:
            for j in range(3): SAWH[j].bar(b, FB.replace("X", nm(v[j])))       # 開いていく → ドロップの頭で全部ひらく
    # 雲のパッド
    if n in ("綿あめの朝", "雲の通学路") or n in ("雲が切れて", "落ちサビ", "風") or (n.startswith("足元") and i < 4):
        if not (n == "風" and i >= 6):
            vv = voice(ch, 60, 3)
            for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
    # プラックのアルペジオ（Aメロ・Bメロ）
    if n in ("綿あめの朝", "雲の通学路") and i >= 4 or n.startswith("足元"):
        t = tones(ch, "B3", "B5"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    if drop and i % 4 == 3:
        t = tones(ch, "G#3", "G#5"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0)))
    # ベース
    if drop: BASS.bar(b, bass_line(S, b, "oct8") if i % 2 == 0 else bass_line(S, b, "push"))
    elif n == "ハーフのサビ": BASS.bar(b, bass_line(S, b, "half"))
    elif n in ("綿あめの朝", "雲の通学路"): BASS.bar(b, bass_line(S, b, "long" if i < 8 else "root8"))
    elif n.startswith("足元"): BASS.bar(b, bass_line(S, b, "root8") if i < 6 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "鳥と並んで": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "落ちサビ": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4" if i >= 4 else "R:4")
    elif n == "もう一度上へ": BASS.bar(b, bass_line(S, b, "root8" if i < 6 else "pulse"))

# 風の音（シンバルのロールとノイズで）・ライザー
riser(FX, S.sc("雲の上へ")[0], 8, "D4"); riser(FX, S.sc("ハーフのサビ")[0], 4, "C4"); riser(FX, S.sc("最後のドロップ")[0], 8, "D4")
FX.bar(S.sc("雲が切れて")[0], "G4:4")                                    # サブドロップ（下が見える）
FX.bar(S.sc("雲が切れて")[2], "A4:2 R:2"); FX.bar(S.sc("雲が切れて")[5], "A4:2 R:2")     # 風の「シュッ」
CYM.bar(S.sc("風")[0], "E4:8")                                          # 風がふくらむ（スウェル）
CYM.bar(S.sc("風")[2], "B4:24")                                         # ロールのディミヌエンドで、風だけが残る
FX.bar(S.sc("風")[5], "A4:3 R:1"); FX.bar(S.sc("風")[7], "A4:4")
cym_swell(CYM, S.sc("鳥と並んで")[0], 2, "C4")

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "短いサビ":
        vgroove(D, b, "four", seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("綿あめの朝", "雲の通学路"):
        if i < 8: vgroove(D, b, "twostep" if n == "綿あめの朝" else "trap", ghosts=0.25, seed=b)
        else: vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("足元ふわふわ"):
        vgroove(D, b, "four" if i < 4 else "four16", seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "....x...x.x.XXXX", "." * 16)
    elif n == "雲の上へ" or (n == "最後のドロップ" and i < 16):
        vgroove(D, b, "four", seed=b)                                        # 1サビ＝ドロップ（4つ打ち）
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
    elif n == "ハーフのサビ" or (n == "最後のドロップ" and i >= 16):
        vgroove(D, b, "half" if n == "ハーフのサビ" else "halfdrive", ghosts=0.3, seed=b)   # 2サビ＝ハーフ（Half feel）
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomtrip")
        if last and n == "最後のドロップ": D.set(b, "X.......X.......", "....X.......X...", "." * 16)
    elif n == "鳥と並んで":
        vgroove(D, b, "twostep", seed=b)
        D.cym(b, ("C2:0.5 " if i == 0 else "F2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if last: put_fill(D, b, "small")
    elif n == "雲が切れて":
        D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "落ちサビ":
        D.set(b, "." * 16, "." * 16, "x...x...x...x..." if i >= 4 else "." * 16)
        if last: put_fill(D, b, "build")
    elif n == "もう一度上へ":
        vgroove(D, b, "four", seed=b, s="............X..." if i < 4 else None)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "XXXXXXXXXXXXXXXX", "." * 16)
    elif n == "風":
        if i == 0: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)

SIL.add(S.sc("ハーフのサビ")[-1], 3, 4)            # 雲が切れる直前の1拍は、完全な無音
SIL.add(S.sc("足元ふわふわ2")[-1], 3.5, 4)          # ハーフに入る前の短いブレイク（半拍）
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の06。ダンス（フューチャーベース）。B長調（サビ・ドロップは G#短調）・150。"
          "雲が綿あめになった日、空を歩いて学校へ行く。短いサビで始まり、歌の役と声のチョップの掛け合いの Aメロ、フィルターが閉じる Bメロ、"
          "4つ打ちのドロップ（1サビ）、ベルの間奏、Half feel のハーフ（2サビ）、1拍の無音から雲が切れる静けさ、ベルと歌だけの落ちサビ、"
          "フィルターが開いていく所から最後のドロップ、風の音だけ残して終わる。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
