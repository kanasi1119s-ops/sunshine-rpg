# vb25 01「既読メトロノーム」Read Receipt Metronome（仮）— テクノポップ（ボカロ曲のインスト）。164・4/4
# Aメロ・Bメロは C#m → サビは平行調の E → 最後のサビは +1（F）。
# 2026-10-25 人間「まだゲームの作り方に引っ張られてるでしょ？」→ 作曲ソフトをふつうの曲が既定の形に変え、01 を物語から作り直した。
#   前の「無限階エレベーター」（階＝ステージ・チャイム＝合図）はゲームの発想だったのでやめた。
# 物語: 夜中に勇気を出して送ったメッセージに「既読」がついたのに、返事が来ない。その数分間、胸の音がメトロノームのように速くなる。
#   迷い、後悔、それでも待つ。最後に「ごめん、寝てた。明日会おう」が届く。
# 作り方: 歌から作る。頭の中でつけた歌詞の言葉のリズム（拍の数・息つぎ）で旋律を決め、伴奏はフレーズごとに弾き方を変える（1小節の型で埋めない）。
#   頭の中の歌詞（旋律の下書き。曲には入らない）:
#     Aメロ「既読がついた　まだ返事はない　砂時計の砂が　落ちてく」「心の音が　うるさくなる　何度も画面を　見てしまう」
#     Bメロ「消したい言葉　でも本当の言葉　送らなきゃよかった？　ちがう」
#     サビ「それでも待ってる　それでも待ってる　君からの一言を」「眠れない夜を　数えてる　この胸の　メトロノーム」
# 心を動かす所: サビは同じ言葉を2回くり返して3回目でオクターブ上へ跳ぶ／サビの終わりに借りてきた短調の和音（Am6）と倚音／
#   Bメロの最後は息を止めるように切る／最後のサビの前は1拍の完全な無音のあと、通知の2音と転調で全員が入る。
# この曲だけの形: 始まりは胸の音（木のメトロノームの刻み）がだんだん速くなる。終わりは刻みがだんだん遅くなって止まる。
from vb25_lib import *

S = Song("01", "metronome", "既読メトロノーム（仮）", "Read Receipt Metronome", 164, 4, "C#", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander"
S.no_depth = True
S.keep_old_synth = True
K = S.key                    # C# の短調
KE = Key("E", "major")       # サビ（平行調）
KF = Key("F", "major")       # 最後のサビ（+1）

VER = ["C#m", "A", "B", "G#m7", "C#m", "A", "F#m7", "G#7"]
PRE = ["A", "B", "G#m7", "C#m", "F#m7", "G#7", "A", "B"]
CHO = ["A", "B", "G#m7", "C#m", "F#m7", "B", "E", "E/G#", "A", "B", "G#m7", "C#m7", "F#m7", "Am6", "E/G#", "B"]
CHO_F = ["Bb", "C", "Am7", "Dm", "Gm7", "C", "F", "F/A", "Bb", "C", "Am7", "Dm7", "Gm7", "Bbm6", "F/A", "C"]
CMELO = ["A", "G#m7", "F#m7", "E", "A", "B", "C#m", "C#m/B", "A", "G#m7", "F#m7", "E/G#", "A", "B", "Csus4", "C"]
INTER = ["C#m", "A", "B", "G#m7"]

S.scene("送信", 8, "intro", INTER * 2)
S.scene("既読", 16, "verse", VER * 2)
S.scene("消したい言葉", 8, "pre", PRE)
S.scene("それでも待ってる", 16, "chorus", CHO)
S.scene("画面を見る", 8, "interlude", INTER * 2)
S.scene("時計の針", 16, "verse", VER * 2)
S.scene("消したい言葉2", 8, "pre", PRE)
S.scene("待つのがこわい", 16, "chorus", CHO)
S.scene("ピアノの間", 8, "interlude", ["A", "B", "G#m7", "C#m", "F#m7", "G#7", "A", "B"])
S.scene("眠れない夜", 16, "bridge", CMELO)
S.scene("それでも", 8, "break", CHO[:8])
S.scene("明日会おう", 32, "chorus", CHO_F + CHO_F)
S.scene("胸の音が止まる", 8, "outro", ["Bb", "C", "Am7", "Dm7", "Bb", "C", "F", "F"])

# ---------------- パート ----------------
V = Voice(S, vol=0.22, delay=0.75, bright=1.5, patch="surgeFormantPulse", low=True)   # 歌の役＋1オクターブ下の重ね
V.main.spec["fx"].insert(2, {"type": "eq", "low": -1, "mid": 0, "midHz": 1000, "high": 3})
TICK = S.track("胸の音（木のメトロノーム）", "pad", patch="surgeWoody", volume=0.12, pan=0.25, reverb=0.25, sustain=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.25}])
PN = S.track("ピアノ（右手）", "piano", volume=0.13, pan=-0.15, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PN2 = S.track("ピアノ（右手の和音の上）", "piano", volume=0.13, pan=-0.15, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PNL = S.track("ピアノ（左手）", "piano", volume=0.13, pan=-0.15, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PNM = S.track("ピアノ（歌を受け取る）", "piano", volume=0.17, pan=-0.15, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassAnalogBassImaged", vol=0.25, duck=0.3))
CSPEC = dict(patch="surgeChordHappyOldVibe", volume=0.055, pan=0.0, reverb=0.25, sustain=0.9, duck=0.35,
             fx=[{"type": "filter", "kind": "highpass", "freq": 230, "q": 0.7}, {"type": "eq", "low": 0, "mid": -3, "midHz": 420, "high": 2}])
CHD = [S.track(f"サビの和音{i + 1}", "pad", **dict(CSPEC)) for i in range(3)]
GSPEC = dict(patch="surgePadSparkly", volume=0.045, pan=0.0, reverb=0.4, sustain=2.0, fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}])
GLOW = [S.track(f"きらめくパッド{i + 1}", "pad", **dict(GSPEC)) for i in range(3)]
BSPEC = dict(patch="surgePadBowed", volume=0.06, pan=0.0, reverb=0.45, sustain=2.5)
BOW = [S.track(f"弓のパッド{i + 1}", "pad", **dict(BSPEC)) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", **dict(volume=0.065, pan=0.0, reverb=0.4, sustain=1.6)) for i in range(2)]
BELL = S.track("きらめき（ベル）", "pad", patch="surgeFantasyBell", volume=0.06, pan=0.4, reverb=0.4, sustain=1.0,
               fx=[{"type": "filter", "kind": "highpass", "freq": 600, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.3}])
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ---------------- 歌の役 ----------------
VA = ["R:0.5 5,:0.25 1:0.25 1:0.25 2:0.25 3:0.5 R:0.25 2:0.25 1:0.5 R:1",             # 既読がついた
      "R:0.25 1:0.25 1:0.25 3:0.25 4:0.25 4:0.25 3:0.25 1:0.25 3:1 R:1",               # まだ返事はない
      "R:0.5 2:0.25 2:0.25 4:0.25 5:0.5 4:0.25 2:0.5 R:0.5 7,:0.25 1:0.25 2:0.5",      # 砂時計の砂が
      "2:1 1:0.5 7,:0.5 5,:1.5 R:0.5",                                                 # 落ちてく
      "R:0.5 3:0.25 3:0.25 3:0.25 4:0.25 5:0.5 R:0.25 4:0.25 3:0.5 R:1",               # 心の音が
      "R:0.25 3:0.25 3:0.25 5:0.25 6:0.5 5:0.25 3:0.25 5:1 R:1",                       # うるさくなる
      "R:0.5 6:0.25 6:0.25 5:0.25 4:0.5 3:0.25 4:0.5 R:0.5 3:0.25 2:0.25 1:0.5",       # 何度も画面を
      "#7,:1.5 2:0.5 5:2"]                                                              # 見てしまう
VA_END = VA[:7] + ["5:1 #7:1 2':2"]
VERSE = VA + VA_END
BM = ["3:1 4:0.5 3:0.5 6:1.5 R:0.5", "4:1 5:0.5 4:0.5 7:1.5 R:0.5", "5:1 7:0.5 1':0.5 2':1 1':1", "1':2 R:1 5:0.5 6:0.5",
      "6:1 1':0.5 6:0.5 3':1.5 R:0.5", "#7:1 2':0.5 #7:0.5 4':1.5 R:0.5", "3':1 2':0.5 1':0.5 3':1 4':1", "5':2 R:2"]
# サビ（E 長調の度数）
CH = ["R:0.5 6:0.25 6:0.25 6:0.5 1':0.5 6:0.5 5:0.5 R:1",          # それでも待ってる
      "R:0.5 5:0.25 5:0.25 5:0.5 7:0.5 5:0.5 4:0.5 R:1",           # それでも待ってる
      "R:0.5 3:0.25 3:0.25 3:0.5 3':1.5 2':0.5 R:0.5",             # 君からの（3回目でオクターブ上へ）
      "1':0.5 7:0.5 6:0.5 5:0.5 6:1.5 R:0.5",                      # 一言を
      "R:0.5 6:0.25 6:0.25 6:0.5 1':0.5 2':0.5 1':0.5 6:1",        # 眠れない夜を
      "R:0.5 5:0.25 5:0.25 5:0.5 7:0.5 1':0.5 2':1 R:0.5",         # 数えてる
      "3':1 2':0.5 1':0.5 2':1.5 1':0.5",                          # この胸の
      "1':2 R:1 5:0.5 6:0.5",                                      # （息つぎ）
      "R:0.5 6:0.25 6:0.25 6:0.5 1':0.5 6:0.5 5:0.5 R:1",
      "R:0.5 5:0.25 5:0.25 5:0.5 7:0.5 5:0.5 4:0.5 R:1",
      "R:0.5 3:0.25 3:0.25 3:0.5 3':1.5 2':0.5 R:0.5",
      "1':1 7:1 6:2",
      "R:0.5 3':0.25 3':0.25 3':0.5 2':0.5 1':0.5 6:0.5 1':1",     # メトロノーム（高い所で同じ音の連打）
      "1':1.5 6:0.5 b6:1 4:1",                                     # 借りてきた短調の和音（Am6）の上で、切なく下がる
      "4:1 3:1 R:1 1:0.5 3:0.5",                                   # 倚音（A → G#）
      "5:3 R:1"]
CH_END = CH[:12] + ["R:0.5 3':0.25 3':0.25 3':0.5 2':0.5 1':0.5 6:0.5 1':1", "2':1 3':1 5':2", "5':2 4':1 3':1", "3':4~"]
CM = ["3':4", "2':2 1':2", "1':2 6:2", "5:4", "3':4", "4':2 2':2", "3':3 R:1", "R:4",
      "R:1 6:0.5 1':0.5 3':2", "R:1 5:0.5 7:0.5 2':2", "R:1 4:0.5 6:0.5 1':2", "R:1 3:0.5 5:0.5 1':2",
      "R:0.5 1':0.5 3':0.5 4':0.5 6':2", "R:0.5 2':0.5 4':0.5 5':0.5 7':2", "1'':4", "R:4"]

for name in ("既読", "時計の針"):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(VERSE[i], oct=4)
        if name == "時計の針" and i < 8: PNM.bar(b, shift_oct(line, 1))       # 2番の前半は、ピアノが歌を受け取る
        else: V.bar(b, line)
for name in ("消したい言葉", "消したい言葉2"):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(BM[i], oct=4))
for name in ("それでも待ってる", "待つのがこわい"):
    for i, b in enumerate(S.sc(name)): V.bar(b, KE.mel(CH[i], oct=4))
for i, b in enumerate(S.sc("眠れない夜")):
    if i >= 2: V.bar(b, K.mel(CM[i], oct=4) if i < 8 else KE.mel(CM[i], oct=3), low=False)
for i, b in enumerate(S.sc("それでも")): V.bar(b, KE.mel(CH[i], oct=4), low=False)
for i, b in enumerate(S.sc("明日会おう")): V.bar(b, KF.mel((CH + CH_END)[i], oct=4))

# ---------------- 胸の音（木のメトロノーム） ----------------
def ticks(note, per_beat, beats=4):
    if per_beat == 3:                     # 3連（端数が残らないように 0.3333・0.3333・0.3334）
        return " ".join(f"{note}:0.3333 {note}:0.3333 {note}:0.3334" for _ in range(int(beats)))
    step = 1 / per_beat
    return " ".join(f"{note}:{step:g}" for _ in range(int(beats * per_beat)))


# 送信: 4分 → 8分 → 3連 → 16分と、だんだん速くなる
for i, b in enumerate(S.sc("送信")): TICK.bar(b, ticks("C#5", [1, 1, 2, 2, 3, 3, 4, 4][i]))
# Aメロ・Bメロ: 小さく、歌のすき間でだけ鳴る（落ち着かない気持ち）
for name in ("既読", "時計の針"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: TICK.bar(b, "R:2 " + ticks("C#5", 4, 2))
# Bメロの最後: 刻みだけが残って、息を止めるように切れる
for name in ("消したい言葉", "消したい言葉2"):
    b = S.sc(name)[-1]; TICK.bar(b, ticks("B4", 4, 2) + " R:2")
# 眠れない夜: 胸の音がゆっくりになる（2分 → 4分）
for i, b in enumerate(S.sc("眠れない夜")): TICK.bar(b, ticks("C#5", 0.5 if i < 8 else 1))
# 終わり: 16分 → 8分 → 4分 → 2分 → 止まる
for i, b in enumerate(S.sc("胸の音が止まる")):
    if i < 7: TICK.bar(b, ticks("C5", [4, 4, 2, 2, 1, 1, 0.5][i]))
    else: TICK.bar(b, "C5:4")

# ---------------- ピアノ（フレーズごとに弾き方を変える） ----------------
COMP = [  # Aメロの右手の和音の刻み（4種類を順に。同じ型をくり返さない）
    lambda v: f"R:0.5 {v[1]}:0.5 R:1 {v[1]}:0.75 R:0.25 {v[2]}:1",
    lambda v: f"{v[0]}:1.5 R:0.5 {v[1]}:0.5 R:0.5 {v[2]}:1",
    lambda v: f"R:1 {v[1]}:0.5 {v[2]}:0.5 R:0.5 {v[1]}:1.5",
    lambda v: f"{v[2]}:0.75 R:0.25 {v[1]}:0.75 R:0.25 {v[0]}:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = [nm(x) for x in voice(ch, 66, 3)]
    if n in ("既読", "時計の針") and not (n == "時計の針" and i < 8):
        f = COMP[(i // 2 + (b % 3)) % 4]
        PN.bar(b, f(v)); PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:1 {nm(low(ch, 'C2') + 7)}:1" if i % 4 != 3 else f"{nm(low(ch, 'C2'))}:4")
    if n == "時計の針" and i < 8:
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:1.5 {nm(low(ch, 'C2') + 12)}:2.5")
    if n.startswith("消したい言葉"):
        if i < 7: PN.bar(b, " ".join(f"{v[q % 3]}:0.5" for q in (0, 1, 2, 1, 0, 1, 2, 1))); PNL.bar(b, piano_left8(ch, "C2"))
    if n in ("それでも待ってる", "待つのがこわい", "明日会おう"):
        if i % 8 < 6: PN.bar(b, piano_arp16(ch, "E4", "E6", pat=(0, 1, 2, 3, 2, 1, 2, 3) if i % 2 == 0 else (0, 2, 1, 3, 2, 3, 1, 2)))
        else:                                                         # フレーズの終わりは、和音を強く2回（歌の息つぎを支える）
            PN.bar(b, f"{v[0]}:1.5! {v[0]}:0.5 R:0.5 {v[0]}:1.5"); PN2.bar(b, f"{v[2]}:1.5 {v[2]}:0.5 R:0.5 {v[2]}:1.5")
        PNL.bar(b, piano_left8(ch, "C2") if i % 4 != 3 else f"{nm(low(ch, 'C2'))}:1 {nm(low(ch, 'C2') + 12)}:1 {nm(low(ch, 'C2') + 7)}:1 {nm(low(ch, 'C2') + 5)}:1")
    if n == "ピアノの間":                                             # 間奏: ピアノが前に出て、サビの言葉を崩した句を弾く
        PNM.bar(b, KE.mel(["R:0.5 6:0.25 6:0.25 6:0.5 1':0.5 3':1 2':0.5 1':0.5", "7:1 5:0.5 7:0.5 2':2",
                            "R:0.5 3':0.25 3':0.25 3':0.5 5':1 4':0.5 3':0.5", "1':3 R:1",
                            "6:0.5 1':0.5 3':0.5 6':0.5 5':1 3':1", "#5:0.5 #7:0.5 2':0.5 #4':0.5 5':2",
                            "4':0.5 3':0.5 2':0.5 1':0.5 3':1 2':1", "#4':2 R:2"][i], oct=4))
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2")
    if n == "それでも":
        PN.bar(b, f"{v[0]}:1 {v[1]}:1 {v[2]}:1 {v[1]}:1"); PNL.bar(b, f"{nm(low(ch, 'C2'))}:4")
    if n == "眠れない夜" and i >= 8:
        PN.bar(b, " ".join(f"{v[q % 3]}:1" for q in (0, 2, 1, 2)))

# ---------------- ベース（2小節ごとに形を変え、句の終わりに次の根音へ向かう） ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "送信": BASS.bar(b, "R:4" if i < 4 else bass_line(S, b, "long" if i < 6 else "root8"))
    elif n in ("既読", "時計の針"): BASS.bar(b, bass_line(S, b, ["root8", "push", "root8", "walk"][i % 4]))
    elif n.startswith("消したい言葉"): BASS.bar(b, bass_line(S, b, "push" if i < 7 else "long"))
    elif n == "それでも待ってる" or n == "明日会おう": BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "walk"))
    elif n == "待つのがこわい": BASS.bar(b, bass_line(S, b, "half" if i < 8 else "oct8"))
    elif n in ("画面を見る", "ピアノの間"): BASS.bar(b, bass_line(S, b, "house" if n == "画面を見る" else "root8"))
    elif n == "眠れない夜": BASS.bar(b, bass_line(S, b, "long") if i >= 4 else "R:4")
    elif n == "胸の音が止まる": BASS.bar(b, bass_line(S, b, "long") if i < 7 else f"{nm(low(ch, 'E1'))}:4")

# ---------------- 和音・パッド・弦・きらめき ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 3)
    if n in ("それでも待ってる", "明日会おう"):
        r = "R:0.5 {0}:1 R:0.5 {0}:1 R:0.5 {0}:0.5" if i % 4 != 3 else "{0}:1.5 {0}:1 R:1.5"
        for j in range(3): CHD[j].bar(b, r.format(nm(v[j])))
    if n == "待つのがこわい":                                        # 2番のサビは重いリズムに（和音は長く、裏で1回だけ）
        for j in range(3): CHD[j].bar(b, f"{nm(v[j])}:2.5 R:0.5 {nm(v[j])}:1")
    if n in ("それでも待ってる", "待つのがこわい", "明日会おう", "画面を見る"):
        w = voice(ch, 72, 3)
        for j in range(3): GLOW[j].bar(b, f"{nm(w[j])}:4")
    if n == "眠れない夜" or (n == "送信" and i >= 4):
        for j in range(3): BOW[j].bar(b, f"{nm(v[j])}:4")
    if n == "明日会おう" and i >= 8:
        w = voice(ch, 74, 2)
        for j in range(2): STR[j].bar(b, f"{nm(w[j])}:4")
    # きらめき（ベル）: サビの長い音のときだけ、上で小さく答える（毎回少しちがう形）
    if n in ("それでも待ってる", "待つのがこわい", "明日会おう") and i % 4 == 3:
        t = tones(ch, "E6", "E7")
        BELL.bar(b, ["R:2 {0}:0.5 {1}:0.5 {2}:1", "R:2.5 {2}:0.5 {1}:0.5 {0}:0.5", "R:2 {1}:0.25 {2}:0.25 {1}:0.5 {0}:1", "R:3 {2}:1"][(i // 4) % 4].format(*[nm(x) for x in t[:3]]))

# 通知が届く（最後のサビの直前）: 1拍の完全な無音のあと、明るいベルの2音（物語の大事な一瞬。1回だけ）
nb = S.sc("明日会おう")[0]
BELL.bar(nb - 1, KF.mel("R:3.5 5':0.25 1'':0.25", oct=4))
cym_swell(CYM, S.sc("それでも待ってる")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("待つのがこわい")[0] - 1, 2, "C4")

# ---------------- ドラム ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "送信":
        hb = "X..X............" if i < 4 else ("X..X....X..X...." if i < 6 else "X..X..X.X..X..X.")   # 胸の音（ドクッ、ドクッ）がつまっていく
        D.set(b, hb, "." * 16, "." * 16 if i < 6 else "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "build")
    elif n in ("既読", "時計の針"):
        vgroove(D, b, "vrock2" if (i // 4) % 2 == 0 else "beat8", ghosts=0.35, seed=b)
        if n == "時計の針" and i >= 8: ride(D, b, "x.x.x.x." if i % 2 == 0 else "x.xxx.x.")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small" if i < 8 else "snare16")
    elif n.startswith("消したい言葉"):
        vgroove(D, b, "half" if i < 4 else "four16", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)
    elif n in ("それでも待ってる", "明日会おう"):
        vgroove(D, b, "vrock", ghosts=0.3, seed=b, h=None if i % 8 < 4 else "XxOxXxxxXxOxXxxx")
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, ["snare16", "tomdown", "small", "tomtrip"][(i // 8) % 4])
    elif n == "待つのがこわい":
        vgroove(D, b, "halfdrive" if i < 12 else "vrock", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b)
        if last: put_fill(D, b, "tomdown")
    elif n == "画面を見る":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "ピアノの間":
        vgroove(D, b, "beat8", ghosts=0.4, seed=b)
        ride(D, b, "x.x.x.x.")
        if last: put_fill(D, b, "lift")
    elif n == "眠れない夜":
        if i < 8: D.set(b, "X..X............" if i % 2 == 0 else "." * 16, "." * 16, "." * 16)   # 胸の音だけが、ゆっくり
        else: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n == "それでも":
        D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "胸の音が止まる":
        D.set(b, ["X..X....X..X....", "X..X....X..X....", "X..X............", "X..X............", "X...............", "X...............", "X...............", "................"][i], "." * 16, "." * 16)
        if i == 0: crash(D, b)

# 止めと無音: Bメロの最後の2拍（刻みだけ残す）は伴奏が止まる／最後のサビの直前は1拍の完全な無音（通知の音だけ）
for name in ("消したい言葉", "消したい言葉2"):
    SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(nb - 1, 2.5, 3.5)
SIL.apply()
# Bメロの最後に残す刻みは、無音を入れた後で戻す（ここだけは鳴らす）
for name in ("消したい言葉", "消したい言葉2"):
    b = S.sc(name)[-1]; TICK.bar(b, "R:2 " + ticks("B4", 4, 2))

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の01。テクノポップ・164。C#m の Aメロ・Bメロから、サビは平行調の E、最後のサビは +1（F）。"
          "夜中に送ったメッセージに既読がついたのに返事が来ない。胸の音がメトロノームのように速くなる。迷い、後悔、それでも待つ。最後に「ごめん、寝てた。明日会おう」。"
          "木のメトロノームの刻みがだんだん速くなる始まり、言葉のリズムで書いた Aメロ、同じ言葉を2回くり返し3回目で跳ぶサビ、借りてきた短調の和音と倚音、"
          "2番はピアノが歌を受け取り、2番のサビは重いリズム、ピアノの間奏、胸の音だけがゆっくりになる Cメロ、ピアノと歌の落ちサビ、1拍の無音と通知の2音から +1 の最後のサビ、刻みが遅くなって止まる終わり。歌の役は声のようなシンセ。自作")
S.flags += " --space sky --space-wet 0.18"
vwrite(S)
