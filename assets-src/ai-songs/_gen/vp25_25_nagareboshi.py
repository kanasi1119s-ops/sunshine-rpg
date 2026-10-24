# vp25 25「流れ星キャッチャー」Shooting Star Catcher（仮）— K-POP。F#長調（つかまえる所で G#長調）・132・4/4。主役の楽器: エコーギター
# 物語: 流星群の夜。虫取り網を持って、流れ星をつかまえに走る。見つけるたびに追いかけて、あと少しの所で消えてしまう。
#   丘の上、仲間とのダンス、最後のチャンス。とうとう一つ、網の中に光が入る。
# 形: 何度も取り逃がす。フック（流れ星の旋律）の断片が、追いかけるたびに1音ずつ長くなって見え、最後にやっと完成した形で一度だけ鳴る
# 場面と強さ: 追いかける＝速く高まる／逃す＝急に空っぽ（1小節の無音）／完成したフック＝最大で長い（全音上げ）
# 旋律の性格: 少しずつ育つフック（2音→3音→…→全部）。エコーギターのやまびこが、流れ星の尾のように残る
# 崩す所: サビ（完成したフック）を最後に一度しか鳴らさない
from vp25_lib import *

S = Song("25", "nagareboshi", "流れ星キャッチャー（仮）", "Shooting Star Catcher", 132, 4, "F#", "major", "K-POP")
K = S.key
CHASE = ["D#m7", "B", "F#/A#", "C#", "D#m7", "B", "G#m7", "C#7sus4"]
HILL = ["Bmaj7", "C#/B", "A#m7", "D#m7", "G#m7", "A#m7", "Bmaj7", "C#7sus4"]
BREAK = ["D#m7", "C#", "B", "C#"]
CATCH = ["E", "B/D#", "C#m7", "F#m7", "G#m7", "A", "B", "B"]          # G#長調の IV から（つかまえる所は明るい方へ）
S.scene("夜空", 4, "intro", ["F#", "F#", "B", "C#"])
S.scene("追いかける1", 20, "verse", CHASE + CHASE + CHASE[:4])
S.scene("逃す1", 1, "break", ["C#7sus4"])
S.scene("追いかける2", 20, "verse", CHASE + CHASE + CHASE[:4])
S.scene("逃す2", 1, "break", ["C#7sus4"])
S.scene("丘の上", 16, "pre", HILL)
S.scene("追いかける3", 20, "verse", CHASE + CHASE + CHASE[:4])
S.scene("逃す3", 1, "break", ["C#7sus4"])
S.scene("ダンスブレイク", 16, "solo", BREAK)
S.scene("最後のチャンス", 8, "pre", ["B", "C#", "D#m", "E", "B", "C#", "D#7", "D#7"])
GS = ["G#", "D#/G", "Fm7", "C#", "Cm7" if False else "A#m7", "C#", "D#7sus4", "D#7"]
S.scene("キャッチ", 24, "chorus", GS + GS + GS)
S.scene("夜空へ", 8, "outro", ["G#"] * 8)
S.drum_gain = {"kick": {"gainDb": -6}}
KG = K.up(2)

EG = S.track("主役: エコーギター（流れ星）", "echoGuitar", volume=0.25, pan=0.0, amp="clean", chorus=0, gainDb=6, reverb=0.35, humanPitch=0, mono=True,
             fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2200, "high": 1.5}, {"type": "pingpong", "beats": 0.75, "mix": 0.3, "feedback": 0.4}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("chiff", vol=0.17, pan=-0.05, delay=0.5))
PL = S.track("プラック", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.4, delay=0.75, sustain=0.5))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=[-0.6, 0.6, 0][i], duck=0.4, sustain=1.0)) for i in range(3)]
SUB = S.track("808", "sub808", **sub_spec(0.2))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.18, duck=0.3))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("halo", vol=0.06, pan=[-0.5, 0.5][i])) for i in range(2)]
STAR = S.track("星の粒", "pad", patch="glassPluck", volume=0.06, pan=-0.5, sustain=1.0, reverb=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 1200, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 流れ星のフック（全部で12音）。断片は最初の n 音 ----------
HOOK = [("5", 0.5), ("1'", 0.5), ("2'", 0.5), ("3'", 1), ("5'", 0.5), ("3'", 0.5), ("2'", 0.5), ("1'", 1.5), ("6", 0.5), ("1'", 0.5), ("2'", 1), ("1'", 2)]


def frag(n, k=K, oct=4, tail=True):
    """フックの最初の n 音（足りない拍は休み）。tail なら最後の音を長く（尾）"""
    toks = [f"{d}:{L:g}" for d, L in HOOK[:n]]
    if tail and n < len(HOOK):
        d, L = HOOK[n - 1]; toks[-1] = f"{d}:{L + 1:g}"
    return k.mel(" ".join(toks), oct=oct)


def put_frag(track, b0, n, k=K, oct=4):
    s = frag(n, k, oct)
    tot = total(s)
    track.at(S.bar_beat(b0), s + (f" R:{(math.ceil(tot / 4) * 4) - tot:g}" if tot % 4 else ""))
    return math.ceil(tot / 4)


put_frag(EG, S.sc("夜空")[0], 2)
for sc_, n in (("追いかける1", 3), ("追いかける2", 5), ("追いかける3", 7)):
    bars = S.sc(sc_)
    put_frag(EG, bars[0], n - 1)                 # 前の断片を思い出して
    put_frag(EG, bars[-4], n)                    # 追いかけの終わりに、1音長くなった断片（そして消える）
put_frag(EG, S.sc("ダンスブレイク")[8], 9)
# キャッチ: やっと完成した形（G#長調）。2回目は1オクターブ上、3回目は全員
for rep, off in ((0, 0), (1, 8), (2, 16)):
    put_frag(EG, S.sc("キャッチ")[off], 12, KG, 4 if rep < 1 else 5)
    EG.bar(S.sc("キャッチ")[off + 4], KG.mel("5':1 3':1 2':1 1':1", oct=4 if rep < 2 else 4))
    EG.bar(S.sc("キャッチ")[off + 5], KG.mel("6':2 5':2", oct=4))
    EG.bar(S.sc("キャッチ")[off + 6], KG.mel("2'':2 1'':1 7':1", oct=4))
    EG.bar(S.sc("キャッチ")[off + 7], KG.mel("1'':4", oct=4))
EG.bar(S.sc("夜空へ")[0], KG.mel("1'':8", oct=4))

# ---------- 歌の役（追いかける）: 走るような8分の句 ----------
RUN = ["R:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:1", "R:0.5 1:0.5 2:0.5 3:0.5 5:1 3:1", "R:0.5 3:0.5 5:0.5 1':0.5 7:0.5 6:0.5 5:1", "4:2 R:2",
       "R:0.5 3:0.5 5:0.5 6:0.5 1':0.5 6:0.5 5:1", "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "R:0.5 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:1", "2:2 R:2"]
for k_, sc_ in enumerate(("追いかける1", "追いかける2", "追いかける3")):
    for i, b in enumerate(S.sc(sc_)):
        if 2 <= i < 16: LEAD.bar(b, K.mel(RUN[i % 8] if k_ != 1 else seq_up(RUN[i % 8], K, 2), oct=4 if k_ < 2 else 5))
HL = ["5':4", "4':2 3':2", "3':4", "2':2 1':2", "7:2 1':2", "2':2 3':2", "4':4", "5':4"]
for i, b in enumerate(S.sc("丘の上")): LEAD.bar(b, K.mel(HL[i % 8], oct=4))
for i, b in enumerate(S.sc("最後のチャンス")): LEAD.bar(b, K.mel(["1':2 2':2", "3':2 4':2", "5':4", "6':4", "5':2 6':2", "7':2 1'':2", "2'':4", "R:4"][i], oct=4))
for i, b in enumerate(S.sc("キャッチ")):
    if i >= 16: LEAD.bar(b, KG.mel([d + ":" + str(L) for d, L in HOOK][0] if False else ["3':4", "2':4", "1':4", "6:4", "1':4", "2':4", "3':2 2':2", "1':4"][i - 16], oct=4))

# ---------- 伴奏 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); v = voice(ch, 64, 3)
    if n.startswith("逃す"): continue
    if n.startswith("追いかける"):
        BASS.bar(b, bass_line(S, b, "root8" if i >= 4 else "long"))
        if i >= 4:
            t = tones(ch, "F#5", "F#7")
            PL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in [0, 2, 1, 3, 2, 4, 3, 1, 0, 2, 1, 3, 2, 4, 3, 5]))
        for j in range(2): PAD[j].bar(b, f"{nm(voice(ch, 58, 2)[j])}:4")
    elif n == "丘の上":
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
    elif n == "ダンスブレイク":
        SUB.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 R:0.5 {nm(r + 12)}:0.5 {nm(r)}:1.5")
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 R:2.5".replace("R:2.5", "R:0.5 " + nm(v[j]) + ":2"))
    elif n == "最後のチャンス":
        BASS.bar(b, bass_line(S, b, "root8"))
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
    elif n == "キャッチ":
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r + 12)}:0.5 {nm(r)}:1")
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5")
        t = tones(ch, "G#5", "G#7")
        PL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in [0, 2, 1, 3, 2, 4, 3, 5, 4, 2, 3, 1, 2, 0, 1, 3]))
    elif n in ("夜空", "夜空へ"):
        for j in range(2): PAD[j].bar(b, f"{nm(voice(ch, 58, 2)[j])}:4")
rnd = random.Random(25)
for b in range(S.nb):
    t = tones(S.chords[b], "C#6", "B7")
    STAR.bar(b, merge_rests(" ".join(f"{nm(rnd.choice(t))}:0.5" if rnd.random() < 0.18 else "R:0.5" for _ in range(8))))
for sc_ in ("ダンスブレイク", "キャッチ"): riser(FX, S.sc(sc_)[0], 8, "D4"); cym_swell(CYM, S.sc(sc_)[0], 2, "C4")
for sc_ in ("逃す1", "逃す2", "逃す3"): FX.bar(S.sc(sc_)[0], "E4:4")       # 消えていく（ダウンリフター）

# ---------- ドラム ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n.startswith("追いかける"):
        if i < 2: continue
        put_groove(D, b, ("X.....X...X.....", "....X.......X...", "x.x.x.x.x.x.x.x." if i < 12 else "xxxxxxxxxxxxxxxx"), ghosts=0.4, seed=b, hat_vary=False)
        if i == 2: crash(D, b, "A2", 2)
        if i % 8 == 7: put_fill(D, b, "small")
        if last: D.set(b, "X...X...X...X...", "....X...xxxxXXXX", "x.x.x.x.........")
    elif n == "丘の上":
        if i >= 8: put_groove(D, b, ("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x."), seed=b, hat_vary=False)
        if last: put_fill(D, b, "build")
    elif n == "ダンスブレイク":
        D.set(b, "X.X...X.X...X.X." if i % 2 == 0 else "X.....X.X.X...X.", "....X..X..X.X...", "x.xxx.xxx.xxx.xx")
        if i % 8 == 0: crash(D, b, "C2")
    elif n == "最後のチャンス":
        D.set(b, "X...X...X...X...", "x.x.x.x.x.x.x.x." if i < 4 else "xxxxxxxxxxxxxxxx", "." * 16)
        if last: D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "キャッチ":
        put_groove(D, b, ("X.....X...X.....", "........X.......", "x.x.x.x.xxxxx.x.") if i < 8 else "four", ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16")
    elif n == "夜空へ" and i == 0:
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2")

S.desc = ("仮: ボカロ曲のインスト25曲の25。K-POP。F#長調（つかまえる所で G#長調）・132。主役の楽器はエコーギター（やまびこが流れ星の尾のように残る）。流星群の夜、流れ星をつかまえに走る。"
          "フック（流れ星の旋律）の断片が、追いかけるたびに 2音→3音→5音→7音→9音と育ち、そのたびに消える（1小節の無音）。"
          "丘の上、ダンスブレイク、最後のチャンスをへて、最後にやっと完成した12音のフックが一度だけ、全音上で鳴る。自作")
S.write()
