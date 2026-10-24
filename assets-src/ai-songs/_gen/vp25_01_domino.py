# vp25 01「ドミノ倒しの午後」Dominoes on a Slow Afternoon（仮）— テクノポップ。E♭長調・128・4/4。主役の楽器: 木琴
# 物語: 日曜の午後、居間の床いっぱいにドミノを並べる。最初の1枚が倒れ、連鎖は曲がり角を曲がり、階段を下り、二手に分かれて、
#   最後の大仕掛けへ。最後の1枚だけが、なぜか倒れずに残る。
# 形: 1枚が次の1枚を倒す連鎖。楽器が1つずつ「倒れて」加わる。木琴の8分の音型は、1小節ごとに1音ずつずれていく（ドミノのずれ）
# 場面と強さ: 一枚目＝コトンと小さい／並べる・倒れはじめ＝少しずつ／加速＝中くらい／曲がり角・階段＝場面が変わる／
#   分かれ道＝静か（ドラムなし→木琴2本の輪唱）／大仕掛け＝最大／最後の1枚の前に1拍の無音→全員→木琴の1音だけが残る
# 旋律の性格: 8分の同じ音型を1音ずつずらす（跳ばない）。サビは同じ4音の形が1段ずつ下がるゼクエンツ。最後だけ1オクターブ跳ぶ
# 崩す所: 4つ打ちのキックを入れない（ドミノの音を主役にするため）。キックは「ドミノが床に当たる音」として、まばらにだけ
from vp25_lib import *

S = Song("01", "domino", "ドミノ倒しの午後（仮）", "Dominoes on a Slow Afternoon", 128, 4, "Eb", "major", "テクノポップ")
K = S.key
VERSE = K.prog("1maj7 2m/1 3m7 4maj7 2m7 3m7 4maj7 5sus4")
HOOK = ["Ebmaj7", "Db/Eb", "Abmaj7/Eb", "Ebmaj7", "Cm7", "F7", "Fm7", "Bb7sus4"]
HOOK_END = ["Ebmaj7", "Db/Eb", "Abmaj7/Eb", "Ebmaj7", "Cm7", "F7", "Fm7", "Bb7"]
CORNER = ["Bmaj7", "Db", "Bbm7", "Ebm7", "Bmaj7", "Db", "Gb", "Bbsus4"]                  # 同じ主音の短調から借りる（曲がり角で景色が変わる）
STAIRS = ["Eb", "Bb/D", "Eb7/Db", "Cm", "Abm/B", "Bb", "Ab/C", "Bbsus4"]               # 1段ずつ下りるベース
SPLIT = ["Abmaj7", "Gm7", "Fm7", "Ebmaj7"]

S.scene("一枚目", 8, "intro", ["Eb"] * 8)
S.scene("並べる", 8, "intro", VERSE)
S.scene("倒れはじめ", 16, "verse", VERSE)
S.scene("加速", 16, "chorus", HOOK + HOOK_END)
S.scene("曲がり角", 8, "bridge", CORNER)
S.scene("階段", 8, "pre", STAIRS)
S.scene("倒れはじめ2", 16, "verse", VERSE)
S.scene("加速2", 16, "chorus", HOOK + HOOK_END)
S.scene("分かれ道", 16, "break", SPLIT)
up = 2   # 大仕掛けは全音上（F 長調）
BIG = [tr_chord(c, up) for c in HOOK + HOOK_END + HOOK + HOOK_END][:24]
S.scene("大仕掛け", 24, "chorus", BIG)
S.scene("最後の一枚", 8, "outro", ["F"] * 8)
K2 = K.up(up)

# ---------- パート ----------
XY = S.track("主役: 木琴（ドミノ）", "xylophone", volume=0.26, pan=-0.12, reverb=0.3, sustain=1.0, gainDb=4)
XY2 = S.track("木琴（分かれ道の2本目）", "xylophone", volume=0.2, pan=0.55, reverb=0.4, sustain=1.0, gainDb=3)
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.2, pan=0.05, delay=0.75))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass2", vol=0.2, duck=0.0))
STAB = [S.track(f"和音の刻み{i + 1}", "pad", **pluck_spec("polysynth", vol=0.06, pan=[-0.4, 0.4, 0][i], delay=0.75, sustain=0.35)) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.55, 0.55, 0][i])) for i in range(3)]
ARP = S.track("ガラスのアルペジオ", "pad", **pluck_spec("glassPluck", vol=0.08, pan=0.35, delay=0.5, sustain=0.8))
FX = S.track("効果音（ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 木琴のドミノ（8分の音型を1小節ごとに1音ずつずらす） ----------
SC = sorted({(K.t + s) % 12 for s in K.steps})


def scale_up(m, k):
    """音階の上で k 段動かす"""
    pcs = SC if not getattr(scale_up, "k2", False) else sorted({(K2.t + s) % 12 for s in K2.steps})
    step = 1 if k > 0 else -1
    for _ in range(abs(k)):
        m += step
        while m % 12 not in pcs: m += step
    return m


CELL = [0, 1, 2, 1, 3, 2, 4, 3]     # 段の動き（跳ばない）


def domino_bar(b, shift, start_lo="Eb5", dens=8):
    ch = S.chords[b]
    r = [m for m in range(midi(start_lo), midi(start_lo) + 12) if m % 12 == bass_pc(ch) or m % 12 == PC[ch_root(ch)] % 12][0]
    cell = CELL[shift % 8:] + CELL[:shift % 8]
    toks = []
    for j, c in enumerate(cell):
        if j >= dens: toks.append("R:0.5"); continue
        toks.append(f"{nm(scale_up(r, c), K.flat)}:0.5{'!' if j == 0 else ''}")
    return " ".join(toks)


# 一枚目: コトン（1音）→ 2音 → … と、ドミノが1枚ずつ並ぶ
for i, b in enumerate(S.sc("一枚目")):
    n = [1, 0, 2, 0, 3, 4, 6, 8][i]
    if n == 0: continue
    XY.bar(b, domino_bar(b, 0, dens=n))
for i, b in enumerate(S.sc("並べる") + S.sc("倒れはじめ")):
    XY.bar(b, domino_bar(b, i // 2 if b in S.sc("並べる") else i))
for i, b in enumerate(S.sc("倒れはじめ2")):
    XY.bar(b, domino_bar(b, i + 3, start_lo="Bb4"))
# 曲がり角・階段: 木琴は階段（1段ずつ下がる4音）
for i, b in enumerate(S.sc("曲がり角")):
    XY.bar(b, domino_bar(b, 7 - i, start_lo="Bb4"))
for i, b in enumerate(S.sc("階段")):
    ch = S.chords[b]; top = tones(ch, "C5", "C6")[-1]
    XY.bar(b, " ".join(f"{nm(scale_up(top, -j), K.flat)}:0.5" for j in range(8)))

# ---------- 歌の役（リード）: 倒れはじめ（Aメロ） ----------
VA = ["R:0.5 5,:0.5 6,:0.5 7,:0.5 1:1 7,:0.5 1:0.5", "2:1.5 1:0.5 7,:1 R:1", "R:0.5 6,:0.5 7,:0.5 1:0.5 2:1 1:0.5 2:0.5", "3:2 2:1 1:1",
      "R:0.5 4:0.5 3:0.5 4:0.5 6:1 4:0.5 3:0.5", "2:1.5 3:0.5 5:1 R:1", "R:0.5 6:0.5 5:0.5 4:0.5 3:1 2:0.5 3:0.5", "4:3 R:1",
      "R:0.5 5:0.5 6:0.5 7:0.5 1':1 7:0.5 1':0.5", "2':1.5 1':0.5 6:1 R:1", "R:0.5 6:0.5 7:0.5 1':0.5 2':1 1':0.5 7:0.5", "1':2 7:1 6:1",
      "R:0.5 6:0.5 5:0.5 6:0.5 1':1 6:0.5 5:0.5", "5:1.5 4:0.5 2:1 R:1", "R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:0.5 3:0.5", "2:2 R:2"]
# 2回目の Aメロ: 同じ形を1段上で始め、後半は木琴と掛け合い（リードが休む所で木琴が答える）
VA2 = [seq_up(x, K, 2) if i in (0, 1, 3) else x for i, x in enumerate(VA[:8])]
VA2[2] = "R:0.5 1:0.5 2:0.5 3:0.5 5:1 3:0.5 2:0.5"
VA2 = VA2 + VA[8:12] + ["R:4", "5:1.5 4:0.5 2:1 R:1", "R:4", "2:2 R:2"]
# サビ: 4音の形が1段ずつ下がる（ドミノが順に倒れる）
HK = ["5:0.5 6:0.5 5:0.5 3:0.5 5:1.5 R:0.5", "4:0.5 5:0.5 4:0.5 2:0.5 4:1.5 R:0.5", "3:0.5 4:0.5 3:0.5 1:0.5 3:1.5 R:0.5", "2:0.5 3:0.5 2:0.5 7,:0.5 1:2",
      "R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:1", "6:1 1':0.5 6:0.5 #4:1 R:1", "4:0.5 6:0.5 1':1 6:0.5 4:0.5 3:1", "4:3 R:1",
      "5:0.5 6:0.5 5:0.5 3:0.5 5:1.5 R:0.5", "4:0.5 5:0.5 4:0.5 2:0.5 4:1.5 R:0.5", "3:0.5 4:0.5 3:0.5 1:0.5 3:1.5 R:0.5", "2:0.5 3:0.5 2:0.5 7,:0.5 1:2",
      "R:0.5 5:0.5 6:0.5 7:0.5 1':1 7:0.5 6:0.5", "6:1 1':0.5 6:0.5 #4:1 6:1", "4:0.5 6:0.5 1':1 2':1 1':1", "7:2 2':2"]
# サビの後半の頭（9〜12小節目）は、同じゼクエンツを高い所から（同じ4小節が続かないように）
HK[8:12] = ["1':0.5 2':0.5 1':0.5 6:0.5 1':1.5 R:0.5", "b7:0.5 1':0.5 b7:0.5 5:0.5 b7:1.5 R:0.5", "6:0.5 5:0.5 6:0.5 4:0.5 6:1.5 R:0.5", "5:0.5 6:0.5 5:0.5 3:0.5 5:2"]
for i, b in enumerate(S.sc("倒れはじめ")): LEAD.bar(b, K.mel(VA[i]))
for i, b in enumerate(S.sc("倒れはじめ2")): LEAD.bar(b, K.mel(VA2[i]))
for sc in ("加速", "加速2"):
    for i, b in enumerate(S.sc(sc)): LEAD.bar(b, K.mel(HK[i]))
# 木琴はサビで、リードの伸ばす所（2拍目の裏から）にだけ合いの手（同じ4音を1オクターブ上で）
for sc in ("加速", "加速2"):
    for i, b in enumerate(S.sc(sc)):
        if i % 8 < 4: XY.bar(b, K.mel(" ".join(HK[i].split()[:4]) + " R:2", oct=6), off=2)
        else: XY.bar(b, domino_bar(b, i, start_lo="Bb5", dens=4), off=0)

# 曲がり角: リードは長い音（景色が変わる）
CORN = ["#4:3 3:1", "4:2 5:2", "4:3 R:1", "b3:2 4:1 5:1", "#4:3 5:1", "#6:2 #4:2", "b3:4", "4:2 R:2"]
for i, b in enumerate(S.sc("曲がり角")):
    ch = S.chords[b]
    LEAD.bar(b, " ".join(f"{nm(m, K.flat)}:{L}" for m, L in zip(tones(ch, "Bb4", "Bb5")[1:3], (2, 2))) if i % 2 == 0 else
             f"{nm(tones(ch, 'Bb4', 'Bb5')[-1], K.flat)}:3 R:1")

# 分かれ道: 2本の木琴の輪唱（同じ旋律を、右の木琴が1拍遅れで）。前半はドラムなし
ROUND = ["5:0.5 6:0.5 5:0.5 3:0.5 2:1 3:1", "4:0.5 3:0.5 2:0.5 1:0.5 7,:1 5,:1", "1:0.5 2:0.5 3:0.5 5:0.5 6:1 5:1", "3:1.5 2:0.5 1:2"]
for i, b in enumerate(S.sc("分かれ道")):
    XY.bar(b, K.mel(ROUND[i % 4]))
    if i < 15: XY2.bar(b, K.mel(ROUND[i % 4], oct=6), off=1)
    else: XY2.bar(b, K.mel(" ".join(ROUND[i % 4].split()[:4]), oct=6), off=1)
# 後半の8小節でリードが戻る（ささやくように、輪唱の上で長い音）
for i, b in enumerate(S.sc("分かれ道")[8:]):
    LEAD.bar(b, K.mel(["3':4", "2':4", "1':3 7:1", "1':2 R:2"][i % 4]))

# 大仕掛け: サビを全音上で2回＋最後の8小節は大きく。最後だけ1オクターブ跳ぶ
for i, b in enumerate(S.sc("大仕掛け")):
    if i < 16: LEAD.bar(b, K2.mel(HK[i]))
    else:
        LEAD.bar(b, K2.mel(["5:0.5 6:0.5 5:0.5 3:0.5 5:1.5 R:0.5", "4:0.5 5:0.5 4:0.5 2:0.5 4:1.5 R:0.5", "3:0.5 4:0.5 3:0.5 1:0.5 3:1.5 R:0.5",
                            "2:0.5 3:0.5 2:0.5 7,:0.5 1:2", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 7:0.5 6:0.5", "6:1 1':0.5 6:0.5 #4:1 6:1",
                            "4:0.5 6:0.5 1':1 2':1 1':1", "1:1 1':3"][i - 16]))
    scale_up.k2 = True
    XY.bar(b, domino_bar(b, i, start_lo="C5" if i < 16 else "F5"))
scale_up.k2 = True
# 最後の一枚: 1小節目の4拍目が無音 → 2小節目の頭に全員 → 木琴の1音だけ残る
fin = S.sc("最後の一枚")
XY.bar(fin[0], K2.mel("1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 R:1", oct=5))
XY.bar(fin[1], "F6:4!")
XY.bar(fin[4], "R:2 C6:6")      # 最後の1枚（倒れずに残る）: 5度の音で終わる（解決しない）

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    if n == "一枚目": continue
    if n == "並べる": BASS.bar(b, bass_line(S, b, "long") if i < 4 else bass_line(S, b, "half")); continue
    if n in ("倒れはじめ", "倒れはじめ2"): BASS.bar(b, bass_line(S, b, "push")); continue
    if n in ("加速", "加速2") or (n == "大仕掛け"): BASS.bar(b, bass_line(S, b, "oct8") if i % 8 != 7 else bass_line(S, b, "root8")); continue
    if n == "曲がり角": BASS.bar(b, bass_line(S, b, "half")); continue
    if n == "階段": BASS.bar(b, bass_line(S, b, "root8")); continue
    if n == "分かれ道": BASS.bar(b, bass_line(S, b, "long") if i >= 8 else "R:4"); continue
    if n == "最後の一枚":
        if i == 0: BASS.bar(b, "F1:3 R:1")
        elif i == 1: BASS.bar(b, "F1:4!")

# ---------- 和音: 刻み（裏拍）とパッド ----------
cv = chord_voices(S, range(S.nb), center=62, n=3)
pv = chord_voices(S, range(S.nb), center=58, n=3)
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    v = cv[b]
    if n in ("加速", "加速2", "大仕掛け", "倒れはじめ2") or (n == "倒れはじmeta"):
        pat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.25 X:0.25 X:0.5" if n != "倒れはじめ2" else "R:0.5 X:0.5 R:1 R:0.5 X:0.5 R:1"
        for j in range(3): STAB[j].bar(b, pat.replace("X", nm(v[j])))
    if n in ("並べる", "曲がり角", "分かれ道", "加速", "加速2", "大仕掛け", "最後の一枚") and not (n == "最後の一枚" and i > 1):
        if n == "最後の一枚" and i == 0: continue
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")

# ガラスのアルペジオ（加速と大仕掛けの後半で、16分の分散和音）
for b in S.sc("加速2") + S.sc("大仕掛け"):
    n, i, L, kind = S.scene_of(b)
    if n == "加速2" and i < 8: continue
    t = tones(S.chords[b], "Bb4", "Bb6")
    ARP.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.25" for k in [0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 3, 4, 2, 3, 1]))

# 効果音: 場面の変わり目の前に
for b in (S.sc("加速")[0], S.sc("加速2")[0], S.sc("大仕掛け")[0]):
    riser(FX, b, 4, "C4"); cym_swell(CYM, b, 2, "C4")
cym_swell(CYM, S.sc("最後の一枚")[1], 2, "E4")

# ---------- ドラム（4つ打ちなし。キックはドミノが床に当たる音として、まばらに） ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    last = i == L - 1
    if n == "一枚目":
        if i >= 4: D.set(b, h="....x.......x...")
        continue
    if n == "並べる":
        put_groove(D, b, ("X...........x...", "................", "x.x.x.x.x.x.x.x." if i >= 4 else "....x.......x..."), seed=1)
        if last: put_fill(D, b, "small")
        continue
    if n in ("倒れはじめ", "倒れはじめ2"):
        put_groove(D, b, ("X.........x.....", "....X.......X...", "x.xxx.x.x.xxx.x."), ghosts=0.5, seed=b)
        if i % 8 == 7: put_fill(D, b, "snare16" if last else "small")
        if i == 0: crash(D, b)
        continue
    if n in ("加速", "加速2"):
        put_groove(D, b, ("X.....X...x.....", "....X.......X...", "xxxxxxxxxxxxxxxx".replace("x", "x", 1)), ghosts=0.4, seed=b)
        D.H[b] = "XoxoXoxoXoxoXoxo"
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomdown")
        continue
    if n == "曲がり角":
        put_groove(D, b, "half", ghosts=0.3, seed=b)
        D.H[b] = "x.x.x.x.x.x.x.x."
        if i == 0: crash(D, b, "D2")
        if last: put_fill(D, b, "tomtrip")
        continue
    if n == "階段":
        # 1段ずつ下りる: タムを1拍ごとに1段ずつ下げる
        D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        D.tom(b, ["C4:1", "A3:1", "F3:1", "D3:1", "A2:1", "C4:0.5 A3:0.5", "F3:0.5 D3:0.5", "A2:0.25 A2:0.25 A2:0.25 A2:0.25"][i] + (" R:3" if i < 5 else " R:3"))
        if last: put_fill(D, b, "build")
        continue
    if n == "分かれ道":
        if i < 8: continue
        put_groove(D, b, ("................", "....x.......x...", "x.x.x.x.x.x.x.x."), seed=b)
        if i == 8: D.cym(b, "D2:4")
        if last: put_fill(D, b, "lift")
        continue
    if n == "大仕掛け":
        put_groove(D, b, ("X.....X...x...x.", "....X.......X...", "XoxoXoxoXoxoXoxo"), ghosts=0.5, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if i != 23 else "snare16")
        elif i % 4 == 3: put_fill(D, b, "small")
        continue
    if n == "最後の一枚":
        if i == 0:
            D.set(b, "X.....X.X.......", "....X.......X...", "XoxoXoxoXoxo....")   # 4拍目は無音（最後の1枚の前の間）
        elif i == 1:
            D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2"); D.cym(b, "G2:4")

# ドラムのタムの小節の長さを合わせる（階段の型は 4拍を超える所があるので、ここで切る）
S.flags += " --space hall --space-wet 0.12"
S.fade_out = 0
S.desc = ("仮: ボカロ曲のインスト25曲の01。テクノポップ。E♭長調・128。主役の楽器は木琴。日曜の午後のドミノ倒し。木琴の8分の音型が1小節ごとに1音ずつずれ、"
          "楽器が1つずつ倒れるように加わる。曲がり角（同じ主音の短調から借りた和音）、階段（1段ずつ下りるベースとタム）、分かれ道（木琴2本の輪唱）をへて、"
          "全音上の大仕掛けへ。最後の1枚の前に1拍の無音、全員の一撃、木琴の5度の1音だけが残る。4つ打ちのキックは使わない。自作")
S.write()
