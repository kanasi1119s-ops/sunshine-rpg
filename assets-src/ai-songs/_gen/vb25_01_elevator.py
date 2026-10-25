# vb25 01「無限階エレベーター」Infinite Floor Elevator（仮）— テクノポップ（ボカロ曲のインスト）。178・4/4
# Aメロ・Bメロは Bm（短調の循環）→ サビは平行調の D に開く → 最後のサビは +2（E）。
# 2026-10-25 v1 は人間「つまらない曲。却下」「ボカロ曲のインストだよ。もっと完成度上げて」→ 作り直し（v2）。
#   v1 の原因: 一音ずつ上がるだけの旋律（フックがない）・音階を並べただけのリフ・順に上がるだけの和音・物語の仕掛けを音楽より優先した。
#   v2 は docs/sound/vocaloid-study.md の決まり（3章）で作る: Aメロの細かいリズムと食い・サビは同じ音の連打のフックを2回くり返し3回目で跳ぶ・
#   短調の循環→平行調・♭II と副属和音・ピアノの16分の分散和音・主旋律の受け渡し・サビ直前の「ベースとシンセだけ」・止めと1拍の無音・
#   2番のサビはジャージークラブにリズムを入れかえ・半音ずつ下がる Half feel・最後のサビの前のこもり→開く。
# 物語（演出として残す）: 雨の日曜日、デパートのエレベーターのボタンに「屋上」より上の階が増えている。押すたびにありえない階へ。
#   途中でエレベーターが止まって（Cメロ: 和音が半音ずつ下がる）、また動きだし、最後は空の階で扉が開く。
#   耳を引く音: 階に着くチャイム・止まるときのダウンリフター・逆再生のシンバル。
from vb25_lib import *

S = Song("01", "elevator", "無限階エレベーター（仮）", "Infinite Floor Elevator", 178, 4, "B", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander"
S.no_depth = True
S.keep_old_synth = True
K = S.key                     # B の短調
KD = Key("D", "major")        # サビ（平行調）
KE = Key("E", "major")        # 最後のサビ（+2）
KC = Key("C#", "minor")       # 最後のサビの短調側

INTRO = ["Bm", "G", "A", "F#m"]
VERSE = ["Bm", "G", "A", "F#m"]
PRE = ["G", "A", "F#m", "Bm", "Em", "F#7", "G", "A"]
CHO = ["Bm", "G", "A", "D", "Bm", "G", "Em", "A/C#", "Bm", "G", "A", "D", "G", "A/G", "F#m", "Bm"]
CMELO = ["Bm", "A#", "A", "G#", "G", "F#", "Em", "F#7", "Em", "F#m", "G", "A", "Bm", "C", "C#", "F#7"]   # ガタン: 半音ずつ下がって止まり、また上がる（C は ♭II）
SOLO = ["Bm", "G", "A", "D", "Bm", "G", "Em", "A/C#"]
LAST = ["C#m", "A", "B", "E", "C#m", "A", "F#m", "B/D#", "C#m", "A", "B", "E", "A", "B/A", "G#m", "C#m"]
LAST2 = ["C#m", "A", "B", "E", "C#m", "A", "F#m", "B/D#", "C#m", "A", "B", "E", "A", "B", "C#m", "C#m"]

S.scene("前奏", 12, "intro", INTRO * 3)
S.scene("Aメロ", 16, "verse", VERSE * 4)
S.scene("Bメロ", 8, "pre", PRE)
S.scene("サビ", 16, "chorus", CHO)
S.scene("間奏", 8, "interlude", INTRO * 2)
S.scene("Aメロ2", 16, "verse", VERSE * 4)
S.scene("Bメロ2", 8, "pre", PRE)
S.scene("サビ2", 16, "chorus", CHO)
S.scene("止まる", 16, "bridge", CMELO)
S.scene("ソロ", 16, "interlude", SOLO * 2)
S.scene("落ちサビ", 8, "break", CHO[:8])
S.scene("上昇", 4, "pre", ["G", "A", "B", "B"])
S.scene("最後のサビ", 32, "chorus", LAST + LAST2)
S.scene("終わり", 8, "outro", ["C#m", "A", "B", "C#m", "A", "B", "C#m", "C#m"])

# ---------------- パート ----------------
V = Voice(S, vol=0.22, delay=0.75, bright=1.5, patch="surgeFormantPulse", low=True)      # 歌の役＋1オクターブ下のこもった重ね（くじらさんの方法）
# 2026-10-25 人間「全体的にこもるように聞こえる。煌めきを」→ 歌の役の高い所を持ち上げる
V.main.spec["fx"].insert(2, {"type": "eq", "low": -1, "mid": 0, "midHz": 1000, "high": 3})
RIFF = S.track("リフ（ポップなシンセ）", "lead", patch="surgeDnaSeq", volume=0.12, pan=-0.2, reverb=0.12, mono=True,
               fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
ANS = S.track("合いの手（明るいリード）", "lead", patch="surgeTropics", volume=0.09, pan=0.35, reverb=0.25, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "pingpong", "beats": 0.5, "mix": 0.25, "feedback": 0.3}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassPasty", vol=0.25, duck=0.3))
PN = S.track("ピアノ（右手）", "piano", volume=0.12, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PNL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PNM = S.track("ピアノ（主旋律の受け渡し）", "piano", volume=0.16, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
CSPEC = dict(patch="surgeChordUnisonMinority", volume=0.055, pan=0.0, reverb=0.25, sustain=0.9, duck=0.4,
             fx=[{"type": "filter", "kind": "highpass", "freq": 230, "q": 0.7}, {"type": "eq", "low": 0, "mid": -3, "midHz": 420, "high": 2}])
CHD = [S.track(f"厚い和音{i + 1}", "pad", **dict(CSPEC)) for i in range(3)]
DSPEC = dict(patch="surgePadNewtonWasEvil", volume=0.06, pan=0.0, reverb=0.4, sustain=2.0)
DARK = [S.track(f"暗いパッド{i + 1}", "pad", **dict(DSPEC)) for i in range(3)]
KSPEC = dict(patch="surgePadNeverending", volume=0.05, pan=0.0, reverb=0.45, sustain=2.5, fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}])
SKY = [S.track(f"空のパッド{i + 1}", "pad", **dict(KSPEC)) for i in range(3)]
SPK = S.track("きらめき（高い16分）", "pad", patch="surgePopcorn", volume=0.05, pan=0.45, reverb=0.35, sustain=0.6,
              fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.3, "feedback": 0.35}])
CHIME = S.track("階に着くチャイム", "bell", patch="surgeBell1", volume=0.1, pan=0.2, reverb=0.4)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.08, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ---------------- 旋律（歌の役） ----------------
# Aメロ（Bm の度数）: 16分の細かい句に休みを入れる（16分は6割ほど。速すぎて聴きにくくしない）。拍の前からの食いを各小節に1か所
A1 = ["R:0.25 1:0.25 1:0.25 2:0.25 3:0.5 1:0.25 R:0.25 5:0.5 4:0.25 3:0.25 2:0.5 1:0.5",
      "R:0.25 3:0.25 3:0.25 4:0.25 5:0.5 3:0.5 6:0.75 5:0.25 3:0.5 R:0.5",
      "R:0.25 4:0.25 4:0.25 5:0.25 6:0.5 5:0.25 4:0.25 3:0.5 2:0.5 3:0.5 R:0.5",
      "5,:0.5 7,:0.5 2:1.5 R:1 1:0.25 2:0.25"]
A2 = ["R:0.25 3:0.25 3:0.25 4:0.25 5:0.5 3:0.25 R:0.25 1':0.5 7:0.25 5:0.25 4:0.5 3:0.5",
      "R:0.25 5:0.25 5:0.25 6:0.25 1':0.5 7:0.5 6:0.75 5:0.25 3:0.5 R:0.5",
      "R:0.25 4:0.25 5:0.25 6:0.25 7:0.5 6:0.25 5:0.25 4:0.5 2:0.5 4:0.5 5:0.5",
      "5:1.5 R:0.5 R:1 R:0.5 5:0.25 4:0.25"]
A3 = A1[:3] + ["5:1 7:1 2':2"]
VLINE = A1 + A2 + A1 + A3
# Bメロ: 8分と付点で広く、上へ溜める。最後の小節は「ベースとシンセだけ」で止める
BM = ["3:1 4:0.5 5:1 3:0.5 6:1", "5:1.5 4:0.5 3:1 2:1", "3:0.5 4:0.5 5:1 7:1.5 5:0.5", "1':3 R:1",
      "R:0.5 5:0.5 6:0.5 7:0.5 1':1 7:1", "#7:1 1':0.5 2':1.5 1':1", "3':1 2':0.5 1':1 2':1.5", "4':2 R:2"]
# サビ（D 長調の度数）: 同じ音の3連打の短い句を2回 → 3回目で6度上へ跳ぶ。後半は高い所（A5）で同じ形をくり返して締める
CH = ["R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 R:0.5 3:0.25 3:0.25 3:0.5 6:0.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 1':1.5 7:0.5 R:0.5",
      "6:0.5 5:0.5 3:0.5 2:0.5 3:1 R:0.5 2:0.25 1:0.25",
      "2:1 1:1 R:1 5,:0.25 6,:0.25 7,:0.25 1:0.25",
      "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 R:0.5 3:0.25 3:0.25 3:0.5 6:0.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 6:0.5 1':0.5 2':1",
      "3':1 2':0.5 1':0.5 2':1 1':0.5 7:0.5",
      "6:1.5 5:0.5 3:0.5 5:1.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 R:0.5 3:0.25 3:0.25 3:0.5 6:0.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 1':1.5 7:0.5 R:0.5",
      "6:0.5 5:0.5 3:0.5 2:0.5 3:1 5:0.5 6:0.5",
      "1':2 R:1 3':0.5 4':0.5",
      "R:0.5 5':0.25 5':0.25 5':0.5 3':0.5 R:0.5 3':0.25 3':0.25 3':0.5 1':0.5",
      "2':1 1':0.5 7:0.5 1':1 2':1",
      "3':1.5 2':0.5 1':1 7:1",
      "7:1 6:2 R:1"]
CH_LAST = CH[:15] + ["6:2 R:2"]
CH_END = CH[:12] + ["R:0.5 5':0.25 5':0.25 5':0.5 3':0.5 R:0.5 3':0.25 3':0.25 3':0.5 1':0.5", "2':1 3':1 5':1 6':1", "5':2 3':1 2':1", "1':3 R:1"]
# Cメロ（止まる）: 半音ずつ下がる和音の上を、長い音でゆっくり落ちる → 後半は動きだして上がる
CM = ["5:4", "5:4", "5:4", "5:4", "5:2 4:2", "#4:4", "5:2 4:1 3:1", "#4:2 #7,:2",
      "R:1 5,:0.5 7,:0.5 2:2", "R:1 6,:0.5 1:0.5 3:2", "R:1 7,:0.5 2:0.5 4:2", "R:1 1:0.5 3:0.5 5:2",
      "R:0.5 3:0.5 5:0.5 1':0.5 2':2", "R:0.5 3:0.5 5:0.5 1':0.5 b2':2", "R:0.5 3:0.5 #4:0.5 5:0.5 #5:2", "#7:2 2':1 #4':1"]

for name in ("Aメロ", "Aメロ2"):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(VLINE[i], oct=4)
        if name == "Aメロ2" and i < 8: PNM.bar(b, shift_oct(line, 1))          # 2番の前半は、ピアノが主旋律を受け取る
        else: V.bar(b, line)
for name in ("Bメロ", "Bメロ2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BM[i], oct=4))
for name in ("サビ", "サビ2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KD.mel((CH if name == "サビ" else CH_LAST)[i], oct=4))
for i, b in enumerate(S.sc("止まる")):
    if i >= 4: V.bar(b, K.mel(CM[i], oct=4), low=(i >= 8))
for i, b in enumerate(S.sc("落ちサビ")): V.bar(b, KD.mel(CH[i], oct=4), low=False)
for i, b in enumerate(S.sc("最後のサビ")): V.bar(b, KE.mel((CH + CH_END)[i], oct=4))
for i, b in enumerate(S.sc("終わり")):
    if i < 4: V.bar(b, KC.mel(["3:2 1:2", "R:4", "3:1 5:1 7:2", "1':4"][i], oct=4))

# ---------------- リフ ----------------
def riff_bar(ch, var=0):
    """この曲のリフ（1小節）: 根音 → 1オクターブ上 → 6度の跳び → 3つの下り、を16分の食いで。var=1 は後半を上へ返す"""
    t = tones(ch, "B3", "B5")
    r = t[0]; o = r + 12
    up = [x for x in t if x > o] or [o + 7]
    six = r + 9 if (r + 9) % 12 in [x % 12 for x in t] or True else r + 7
    mid = [x for x in t if r < x < o]
    a, b = (mid + [r + 7, r + 4])[:2]
    tail = f"{nm(up[0])}:0.25 {nm(o)}:0.25 {nm(b)}:0.25 {nm(a)}:0.25" if var else f"{nm(a)}:0.25 {nm(b)}:0.25 {nm(r)}:0.25 R:0.25"
    return f"{nm(r)}:0.25 R:0.25 {nm(o)}:0.25 R:0.25 {nm(a + 0)}:0.5 {nm(b)}:0.25 {nm(r)}:0.25 R:0.25 {nm(a)}:0.25 {nm(o)}:0.25 R:0.5 " + tail


for name in ("前奏", "間奏"):
    for i, b in enumerate(S.sc(name)): RIFF.bar(b, riff_bar(S.chords[b], i % 4 == 3))
for i, b in enumerate(S.sc("終わり")): RIFF.bar(b, riff_bar(S.chords[b], i % 2))
for name in ("サビ", "サビ2", "最後のサビ"):                     # サビ: リフの断片を歌のすき間（小節の後ろ1拍）に
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: RIFF.bar(b, "R:3 " + " ".join(f"{nm(x)}:0.25" for x in tones(S.chords[b], "D5", "D6")[:4]))
# ソロ（リフのシンセ）: 前半はリフを崩して、後半は16分の上り下り。最後の2小節は同じ音の連打で溜める
SOLO_L = ["1':0.25 R:0.25 1'':0.25 R:0.25 6':0.5 5':0.25 3':0.25 R:0.25 5':0.25 1'':0.25 R:0.5 7':0.25 6':0.25 5':0.5",
          "3':0.5 5':0.5 6':0.75 5':0.25 3':0.5 2':0.5 1':1",
          "2':0.25 3':0.25 5':0.25 6':0.25 5':0.25 3':0.25 2':0.25 1':0.25 2':0.5 3':0.5 5':1",
          "1'':1.5 7':0.5 6':0.5 5':0.5 3':1",
          "6:0.25 1':0.25 3':0.25 6':0.25 5':0.25 3':0.25 1':0.25 6:0.25 5:0.25 6:0.25 1':0.25 3':0.25 5':0.5 6':0.5",
          "5':0.25 6':0.25 1'':0.25 2'':0.25 1'':0.25 6':0.25 5':0.25 3':0.25 2':0.5 3':0.5 5':1",
          "3':0.25 3':0.25 3':0.25 3':0.25 2':0.25 2':0.25 2':0.25 2':0.25 1':0.25 1':0.25 1':0.25 1':0.25 7:0.5 1':0.5",
          "7:0.25 1':0.25 2':0.25 3':0.25 4':0.25 #4':0.25 5':0.25 #5':0.25 6':2"]
for i, b in enumerate(S.sc("ソロ")): RIFF.bar(b, KD.mel(SOLO_L[i % 8], oct=4))
# 合いの手（明るいリード）: 2番のサビと最後のサビの、歌の長い音の上に短く答える
for name in ("サビ2", "最後のサビ"):
    kk = KD if name == "サビ2" else KE
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 3: ANS.bar(b, kk.mel("R:2 5':0.5 6':0.5 1'':1", oct=4))
        if i % 8 == 7: ANS.bar(b, kk.mel("R:2.5 3':0.5 2':0.5 1':0.5", oct=4))

# ---------------- 伴奏 ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 3)
    # ベース
    if n == "前奏": BASS.bar(b, bass_line(S, b, "long") if i < 4 else bass_line(S, b, "oct8"))
    elif n in ("Aメロ", "Aメロ2"): BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "push"))
    elif n.startswith("Bメロ"): BASS.bar(b, bass_line(S, b, "push" if i < 7 else "long"))
    elif n == "サビ" or n == "最後のサビ": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "サビ2": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "間奏" or n == "ソロ": BASS.bar(b, bass_line(S, b, "pulse" if n == "間奏" else "oct8"))
    elif n == "止まる": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "push"))
    elif n == "上昇": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "終わり": BASS.bar(b, bass_line(S, b, "oct8") if i < 7 else f"{nm(low(ch, 'E1'))}:1 R:3")
    # ピアノ: Aメロは裏の和音、Bメロ・サビは右手16分の分散和音と左手8分のオクターブ、落ちサビはピアノだけ
    if n in ("Aメロ", "Aメロ2") and not (n == "Aメロ2" and i < 8):
        PN.bar(b, " ".join(f"R:0.5 {nm(v[(q % 3)])}:0.5" for q in range(4)))
    if n.startswith("Bメロ") and i < 7 or n in ("サビ", "サビ2", "最後のサビ", "ソロ"):
        PN.bar(b, piano_arp16(ch, "D4", "D6")); PNL.bar(b, piano_left8(ch, "C2"))
    if n == "落ちサビ":
        PN.bar(b, " ".join(f"{nm(x)}:1" for x in [v[0], v[1], v[2], v[1]])); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
    if n == "Aメロ2" and i < 8: PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2")
    # 厚い和音（サビ・ソロ・最後のサビ）: 裏で刻む
    if n in ("サビ", "サビ2", "最後のサビ", "ソロ"):
        rhythm = "R:0.5 {0}:1 R:0.5 {0}:1 R:0.5 {0}:0.5" if n != "サビ2" else "{0}:0.75 R:0.25 {0}:0.5 R:0.5 {0}:0.75 R:0.25 {0}:1"
        for j in range(3): CHD[j].bar(b, rhythm.format(nm(v[j])))
    if n == "前奏" and i >= 4:
        for j in range(3): CHD[j].bar(b, f"{nm(v[j])}:4")
    # 止まる: 暗いパッド（半音ずつ下がる和音）
    if n == "止まる":
        for j in range(3): DARK[j].bar(b, f"{nm(v[j])}:4")
    # 最後のサビ: 空のパッドを下に広げる
    if n == "最後のサビ" or n == "上昇":
        w = voice(ch, 58, 3)
        for j in range(3): SKY[j].bar(b, f"{nm(w[j])}:4")


# きらめき（2026-10-25 人間「煌めきがあるような音に」）: サビは高い所で16分の分散和音（2拍ずつ上がって下がる）、
#   Aメロは歌のすき間に高い3音の「くすっ」とする合いの手（遊び。毎回少しちがう形）
_play = ["R:3 {0}:0.25 {1}:0.25 {2}:0.5", "R:3.25 {2}:0.25 {1}:0.25 {0}:0.25", "R:2.5 {0}:0.25 R:0.25 {1}:0.25 R:0.25 {2}:0.5", "R:3 {2}:0.5 {2}:0.25 {1}:0.25"]
for name in ("サビ", "サビ2", "最後のサビ"):
    for i, b in enumerate(S.sc(name)):
        t = tones(S.chords[b], "C6", "C7")
        SPK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 2, 1, 2, 3)) + " R:2" if i % 2 == 0 else "R:2 " + " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (3, 2, 1, 0, 1, 2, 1, 0)))
for name in ("Aメロ", "Aメロ2"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 1:
            t = tones(S.chords[b], "E5", "E6")
            SPK.bar(b, _play[(i // 2) % 4].format(*[nm(x) for x in t[:3]]))
# Bメロの最後の小節（ベースとシンセだけ）: 厚い和音が16分の裏で食う（次に何が来るか読めないリズムで、サビへの期待を作る）
for name in ("Bメロ", "Bメロ2"):
    b = S.sc(name)[-1]; v = voice(S.chords[b], 64, 3)
    for j in range(3): CHD[j].bar(b, f"R:0.75 {nm(v[j])}:0.25 R:0.5 {nm(v[j])}:0.5 R:0.25 {nm(v[j])}:0.25 R:0.5 {nm(v[j])}:0.25 R:0.75")

# 階に着くチャイム（場面の頭）: 高い2音
for step, name in enumerate(("Aメロ", "サビ", "Aメロ2", "サビ2", "最後のサビ")):
    b = S.sc(name)[0]; kk = {"サビ": KD, "サビ2": KD, "最後のサビ": KE}.get(name, KD)
    hi = ["3'", "4'", "5'", "6'", "1''"][step]                      # 階が上がるたびにチャイムも1段ずつ高く（くすっとする遊び）
    CHIME.bar(b, kk.mel(f"{hi}:0.5 3':1.5", oct=4) + " R:2")
CHIME.bar(S.sc("終わり")[-1], KE.mel("R:1 5':0.5 3':2.5", oct=4))
# 効果音: サビの前のライザー・逆再生シンバル、止まるときのダウンリフター
riser(FX, S.sc("サビ")[0] - 2, 8, "C4"); riser(FX, S.sc("サビ2")[0] - 2, 8, "C4"); riser(FX, S.sc("最後のサビ")[0] - 4, 16, "D4")
cym_swell(CYM, S.sc("サビ")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("ソロ")[0] - 1, 2, "C4")
FX.bar(S.sc("止まる")[0], "E4:4")

# ---------------- ドラム ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "前奏":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "four16", seed=b)
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("Aメロ", "Aメロ2"):
        vgroove(D, b, "vrock2" if n == "Aメロ" else "beat8", ghosts=0.35, seed=b)
        if n == "Aメロ2" and i >= 8: ride(D, b, "x.x.x.x.")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("Bメロ"):
        vgroove(D, b, "half" if i < 4 else "four16", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 0)                                   # サビ直前の1小節: ベースとシンセだけ
    elif n in ("サビ", "最後のサビ"):
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n == "サビ": put_fill(D, b, "tomdown")
    elif n == "サビ2":
        vgroove(D, b, "jersey", ghosts=0.2, seed=b)                # 2番のサビはジャージークラブに入れかえ（和音はそのまま）
        if i % 8 == 0: crash(D, b)
        if i == 15: put_fill(D, b, "tomtrip")
    elif n == "間奏":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "止まる":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.25, seed=b, h="x...x...x...x...")
        if i == 8: crash(D, b, "G2")
        if last: put_fill(D, b, "build")
    elif n == "ソロ":
        vgroove(D, b, "vrock", ghosts=0.35, seed=b)
        if i % 4 == 0: crash(D, b, "B2" if i % 8 == 4 else "C2")
        if i == 15: put_fill(D, b, "lift")
    elif n == "落ちサビ":
        D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "上昇":
        vgroove(D, b, "four16", seed=b)
        if i >= 2: put_fill(D, b, "build")
    elif n == "終わり":
        if i < 7: vgroove(D, b, "four16", seed=b)
        else: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 2)

# 最後のサビの前の「こもり」: 上昇の4小節は、リフ以外を 800Hz のこもった写しへ → サビの頭で開く
muffle(S, [BASS, CHD[0], CHD[1], CHD[2], PN, PNL], S.sc("上昇"), freq=800)
# 止めと無音: Bメロ2 の最後の1拍は完全な無音（1回）・止まるの頭は1拍止まる・終わりはテンションの短い和音で切る
SIL.add(S.sc("Bメロ2")[-1], 3, 4)
SIL.add(S.sc("上昇")[-1], 3, 4)
SIL.add(S.sc("止まる")[0], 1, 2)
SIL.add(S.sc("終わり")[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の01。テクノポップ・178。Bm の短調の循環から、サビは平行調の D に開き、最後のサビは +2（E）。"
          "雨の日曜日、デパートのエレベーターに屋上より上の階が増えていて、押すたびにありえない階へ。途中で止まり（和音が半音ずつ下がる Half feel）、"
          "また動きだして、最後は空の階で扉が開く。いきなりリフで始まり、16分の Aメロ、同じ音の連打を2回くり返して3回目で跳ぶサビ、"
          "2番はピアノが主旋律を受け取り、2番のサビはジャージークラブ、シンセのソロ、ピアノと歌の落ちサビ、こもり→開く最後のサビ、短い和音で切る。歌の役は声のようなシンセ。自作")
S.flags += " --space sky --space-wet 0.2"   # 2026-10-25 人間「空間を支配しよう」「煌めきがある音に」→ 明るく広い空間
vwrite(S)
