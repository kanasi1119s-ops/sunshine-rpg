# vb25 13「まばたきプリズム」Blink Prism（仮）— エレクトロニカ（グリッチポップ）。D長調（Aメロは平行調の B短調で）・148・4/4。転調なし
# 物語: 雨上がりの帰り道。水たまりにできた虹をのぞくと、まばたきするたびに、別の街が映る。最後は虹が全部つながって、2つの街が1つの空になる。
# 場面と強さ: しずく（ガラスの音だけ・極小）→ 水たまり（ハープとしずく・小→中）→ のぞきこむ（Aメロ・語る）→ 虹が見える（Bメロ・溜め・止め）
#   → 虹がつながる（サビ・強）→ まばたき（間奏・グリッチ）→ 別の街（Aメロ2・ハープが歌を受け取る）→ 虹が見える2 → 虹がつながる2（2ステップにリズムを入れかえ・止め）
#   → しずくの音（静けさ）→ 逆さまの街（Cメロ・Half feel）→ 鏡の街（逆再生のシンバルとガラス・溜め）→ 1拍の完全な無音 → 全部の虹（最後のサビ・最大）
#   → 水面が戻る → しずく1つ
# 旋律の性格: 光が散るような高い跳躍（5度・短6度・オクターブ）と、短い句のくり返し。最高音 D6
# 派手な展開: 1拍の完全な無音・逆再生（シンバルと、ガラスの音の逆行形）・止め2回・Half feel・サビごとのリズムの入れかえ（4つ打ち→2ステップ）・転調なし
from vb25_lib import *

S = Song("13", "blinkprism", "まばたきプリズム（仮）", "Blink Prism", 148, 4, "D", "major", "グリッチポップ（ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
K = S.key

A_CH = ["Bm", "G", "A", "F#m", "Bm", "G", "Em7", "F#7"]                    # i–♭VI–♭VII–v（B短調で）と長調の V（F#7）
B_CH = ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "F#7", "Gmaj7", "A7sus4"]      # F#7＝vi への副属和音
C_CH = ["G", "D", "A", "Bm", "G", "D/F#", "Em7", "A"]                       # IV–I–V–vi
C_CH2 = ["G", "D", "A", "Bm", "Gm6", "D/F#", "E7", "A7"]                    # Gm6＝同主調から借りた iv・E7＝V への副属和音
UPSIDE = ["Em7", "F#m7", "Gmaj7", "A", "Bm7", "Bm7/A", "Gmaj7", "F#7", "Em7", "Gm6", "D/F#", "A7sus4"]
MIRROR = ["Gmaj7", "A", "F#m7", "Bm7", "Em7", "F#7", "Gmaj7", "A7sus4"]
TAG = ["G", "A", "F#m7", "Bm7", "Gmaj7", "A", "Dmaj7", "Dmaj7"]
POOL = ["Dmaj7", "Bm7", "Gmaj7", "A7sus4"]

S.scene("しずく", 2, "intro", ["Dmaj7", "Dmaj7"])
S.scene("水たまり", 8, "intro", POOL * 2)
S.scene("のぞきこむ", 16, "verse", A_CH)
S.scene("虹が見える", 8, "pre", B_CH)
S.scene("虹がつながる", 16, "chorus", C_CH + C_CH2)
S.scene("まばたき", 8, "interlude", POOL * 2)
S.scene("別の街", 16, "verse", A_CH)
S.scene("虹が見える2", 8, "pre", B_CH)
S.scene("虹がつながる2", 16, "chorus", C_CH + C_CH2)
S.scene("しずくの音", 4, "break", ["Dmaj7"] * 4)
S.scene("逆さまの街", 12, "bridge", UPSIDE)
S.scene("鏡の街", 8, "build", MIRROR)
S.scene("全部の虹", 24, "chorus", C_CH + C_CH2 + TAG)
S.scene("水面が戻る", 8, "outro", POOL * 2)
S.scene("しずく1つ", 2, "outro", ["Dmaj7", "Dmaj7"])

V = Voice(S, vol=0.22, delay=0.75)
GLASS = S.track("ガラスの音（しずく・きらめき）", "bell", patch="glassPluck", volume=0.09, pan=0.45, sustain=1.2, reverb=0.5,
                fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.35}])
HARP = S.track("ハープ", "harp", volume=0.13, pan=-0.35, reverb=0.35, sustain=1.6)
HARPM = S.track("ハープ（歌の受け渡し）", "harp", volume=0.18, pan=-0.35, reverb=0.35, sustain=1.6)
GLT = S.track("グリッチ（ビットクラッシュの刻み）", "lead", patch="pluckSynth", volume=0.08, pan=0.2, sustain=0.4, reverb=0.15,
              fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "bitcrusher", "bits": 6, "mix": 0.45}])
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=0.0, duck=0.35, sustain=1.8)) for i in range(3)]
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.22, duck=0.25))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音（逆再生）", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の役 =================
A1 = ["R:0.25 6:0.25 6:0.25 5:0.25 3:0.25 5:0.25 6:0.5 R:0.25 6:0.25 1':0.25 6:0.25 5:0.5 3:0.5",
      "R:0.25 5:0.25 5:0.25 4:0.25 2:0.25 4:0.25 5:0.5 R:0.25 5:0.25 1':0.25 5:0.25 4:0.5 2:0.5",
      "R:0.25 3:0.25 3:0.25 5:0.25 1':0.25 7:0.25 5:0.25 3:0.25 R:0.25 2:0.25 3:0.25 5:0.25 7:1",
      "7:0.5 6:0.25 5:0.25 R:0.5 3:0.25 5:0.25 3:1.5 R:0.5",
      "R:0.25 6:0.25 1':0.25 3':0.25 1':0.25 6:0.25 5:0.25 6:0.25 R:0.25 3:0.25 4:0.25 5:0.25 6:0.5 1':0.5",
      "R:0.25 2':0.25 1':0.25 6:0.25 5:0.25 4:0.25 2:0.5 R:0.25 4:0.25 5:0.25 6:0.25 5:1",
      "R:0.25 2:0.25 4:0.25 5:0.25 2':0.5 1':0.5 R:0.25 5:0.25 6:0.25 1':0.25 2':0.5 1':0.5",
      "3:0.5 #5:0.5 7:0.5 2':0.5 3':1 R:1"]
A1b = ["R:0.25 6:0.25 6:0.25 5:0.25 3:0.25 5:0.25 6:0.5 R:0.25 1':0.25 3':0.25 1':0.25 6:0.5 5:0.5",
       "R:0.25 5:0.25 5:0.25 4:0.25 2:0.25 4:0.25 5:0.5 R:0.25 2':0.25 1':0.25 6:0.25 5:0.5 4:0.5",
       "R:0.25 7:0.25 7:0.25 5:0.25 3:0.25 5:0.25 7:0.5 R:0.25 5:0.25 7:0.25 2':0.25 7:1",
       "3:0.5 5:0.25 7:0.25 R:0.5 7:0.25 5:0.25 3:1.5 R:0.5",
       A1[4],
       "R:0.25 4:0.25 5:0.25 6:0.25 1':0.25 2':0.25 3':0.5 R:0.25 2':0.25 1':0.25 6:0.25 5:1",
       "R:0.25 5:0.25 2':0.25 5:0.25 1':0.25 5:0.25 6:0.25 5:0.25 4:0.5 5:0.5 2':1",
       "#5:0.5 7:0.5 3':1 R:2"]
A2b = ["R:0.25 1':0.25 1':0.25 6:0.25 5:0.25 6:0.25 1':0.5 R:0.25 3':0.25 2':0.25 1':0.25 6:0.5 3:0.5",
       "R:0.25 4:0.25 6:0.25 1':0.25 2':0.25 1':0.25 6:0.5 R:0.25 5:0.25 4:0.25 2:0.25 4:1",
       "R:0.25 5:0.25 7:0.25 2':0.25 3':0.25 2':0.25 7:0.5 R:0.25 5:0.25 3:0.25 5:0.25 7:1",
       "3':0.5 2':0.25 7:0.25 R:0.5 3:0.25 7:0.25 5:1.5 R:0.5",
       "R:0.25 6:0.25 6:0.25 1':0.25 3':0.25 1':0.25 6:0.25 1':0.25 R:0.25 5':0.25 3':0.25 1':0.25 6:0.5 5:0.5",
       "R:0.25 2':0.25 2':0.25 1':0.25 6:0.25 5:0.25 4:0.5 R:0.25 6:0.25 1':0.25 3':0.25 2':1",
       "R:0.25 2:0.25 5:0.25 1':0.25 2':0.25 1':0.25 5:0.25 2:0.25 4:0.5 5:0.5 1':0.5 2':0.5",
       "3':1 #5:1 R:2"]
BM = ["3':0.5 2':0.5 1':1 3':0.5 2':0.5 1':1", "3':0.5 2':0.5 7:1 3':0.5 2':0.5 7:1", "3':0.5 2':0.5 3':1 5':1 3':1", "1':2 R:1 1':0.5 2':0.5",
      "5':0.5 4':0.5 2':1 5':0.5 4':0.5 2':1", "#5':0.5 3':0.5 7:1 2':1 3':1", "6':1 3':1 2':2", "5':2 R:2"]
BM2 = BM[:4] + ["5':0.5 4':0.5 2':0.5 1':0.5 2':1 5':1", "3':0.5 #5':0.5 3':1 7:1 3':1", "6':2 5':1 3':1", "5':1 R:3"]
CH1 = ["R:0.5 1':0.5 5':1 4':0.5 3':0.5 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "R:0.5 7:0.5 5':1 3':0.5 2':0.5 7:1", "1':1.5 7:0.5 6:2",
       "R:0.5 1':0.5 5':1 4':0.5 3':0.5 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 1'':1 6':1", "5':1 4':0.5 2':0.5 5':1 4':1", "2':3 R:1"]
CH1b = [CH1[0], "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1", "R:0.5 7:0.5 5':1 6':0.5 5':0.5 3':1", "4':1 3':1 1':2",
        "R:0.5 b6':0.5 b6':0.5 b6':0.5 4':1 2':1", "3':1 1':1 5:1 1':1", "2':0.5 #4':0.5 6':1 #4':1 2':1", "5':2 4':1 R:1"]
CH2 = CH1[:6] + ["5':1 6':0.5 5':0.5 4':1 2':1", "7:3 R:1"]
CH2b = CH1b[:6] + ["2':1 #4':1 6':1 1'':1", "7':2 5':2"]
TAGL = ["R:0.5 1':0.5 5':1 6':0.5 5':0.5 3':1", "R:0.5 3':0.5 3':0.5 3':0.5 7':1 5':1", "5':1 3':1 7:1 3':1", "1'':2 6':2",
        "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "5':1 7':1 6':1 5':1", "3':4", "R:4"]

for name, lines in (("のぞきこむ", A1 + A1b), ("別の街", A1 + A2b)):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(lines[i], oct=4)
        if name == "別の街" and i < 8: HARPM.bar(b, line)          # 別の街の前半は、ハープが歌を受け取る
        else: V.bar(b, line)
for name, lines in (("虹が見える", BM), ("虹が見える2", BM2)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
for name, lines in (("虹がつながる", CH1 + CH1b), ("虹がつながる2", CH2 + CH2b), ("全部の虹", CH1 + CH1b + TAGL)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
UP = ["2':2 1':1 6:1", "3':3 R:1", "6:1 1':1 3':1 5':1", "7':3 R:1", "6':2 5':1 3':1", "5':3 R:1",
      "2':1 3':1 5':1 3':1", "#5':2 3':2", "2':1 4':1 6':2", "b6':2 4':2", "3':1 5':1 1'':2", "5':2 R:2"]
for i, b in enumerate(S.sc("逆さまの街")): V.bar(b, K.mel(UP[i], oct=4), low=(i >= 4))
MI = ["1':2 3':2", "2':2 7:2", "3':1 5':1 3':2", "1':4", "2':1 5':1 2':2", "3':2 #5':2", "6':2 3':2", "5':2 R:2"]
for i, b in enumerate(S.sc("鏡の街")): V.bar(b, K.mel(MI[i], oct=4), low=(i >= 4))
for i, b in enumerate(S.sc("水面が戻る")):
    if i < 6: V.bar(b, K.mel(["3':2 2':1 1':1", "6:4", "5:2 1':2", "7:4", "3':2 5':1 3':1", "2':4"][i], oct=4), low=False)

# ================= ハープ・ガラス・グリッチ =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    # ハープの分散和音（8分。水面のゆれ）
    if n in ("水たまり", "水面が戻る") or (n in ("のぞきこむ", "別の街") and i >= 8) or n.startswith("虹が見える") or n == "逆さまの街":
        if not (n == "別の街" and i < 8):
            t = tones(ch, "D3", "D5")
            HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 1, 3, 5, 4)))
    elif n in ("虹がつながる", "虹がつながる2", "全部の虹"):
        t = tones(ch, "D4", "D6")
        HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 3)))
# しずく（ガラスの音）: まばらに、左右のディレイで散る
DROPS = ["R:1 5':0.5 R:2.5", "R:2.5 3'':0.5 R:1", "R:0.5 1'':0.5 R:1.5 6':0.5 R:1", "R:3 2'':0.5 R:0.5"]
for name in ("しずく", "水たまり", "しずくの音", "水面が戻る"):
    for i, b in enumerate(S.sc(name)): GLASS.bar(b, K.mel(DROPS[(b + i) % 4], oct=4))
for name in ("のぞきこむ", "別の街"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3 and not (name == "別の街" and i < 8): GLASS.bar(b, K.mel("R:2.5 5':0.25 3':0.25 1'':0.5 5':0.5", oct=4))
for name in ("虹がつながる", "虹がつながる2", "全部の虹"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: GLASS.bar(b, K.mel("R:3 1'':0.25 6':0.25 5':0.25 3':0.25", oct=4))
# まばたき（間奏）: グリッチの刻みが主旋律（同じ音の32分のスタッター）と、ガラスの音の掛け合い
BLINK = ["1':0.25 1':0.25 5':0.5 3':0.25 3':0.25 1'':0.5 5':1 3':1", "6:0.25 6:0.25 3':0.5 1':0.25 1':0.25 6':0.5 5':1 3':1",
         "5:0.25 5:0.25 2':0.5 7:0.25 7:0.25 5':0.5 3':1 2':1", " ".join(["5':0.125"] * 8) + " " + " ".join(["4':0.125"] * 8) + " 3':1 2':1"]
for i, b in enumerate(S.sc("まばたき")):
    if i % 2 == 0: GLT.bar(b, K.mel(BLINK[(i // 2) % 4], oct=4))
    else: GLASS.bar(b, K.mel(retro(BLINK[(i // 2) % 4]) if i < 7 else "5':2 R:2", oct=4))
# 鏡の街: サビの句の逆行形（逆さまに映る旋律）をガラスで
for i, b in enumerate(S.sc("鏡の街")):
    if i % 2 == 1: GLASS.bar(b, K.mel(retro(CH1[i % 8]), oct=4))
# グリッチの刻み（Bメロの最後・サビの変わり目にスタッター）
for name in ("虹が見える", "虹が見える2"):
    b = S.sc(name)[-2]; GLT.bar(b, K.mel("R:2 " + " ".join(["5':0.125"] * 8) + " " + " ".join(["#5':0.125"] * 4) + " R:0.5", oct=4))

# ================= パッド・ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    r = low(ch, "E1")
    if n in ("水たまり", "虹が見える", "虹が見える2", "虹がつながる", "虹がつながる2", "全部の虹", "逆さまの街", "鏡の街", "水面が戻る") \
            and not (n.startswith("虹が見える") and i == L - 1):
        for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")
    if n == "水たまり": BASS.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4")
    elif n in ("のぞきこむ", "別の街"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "root8"))
    elif n.startswith("虹が見える"): BASS.bar(b, bass_line(S, b, "house") if i < L - 1 else f"{nm(r)}:2 R:2")
    elif n in ("虹がつながる", "全部の虹"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n == "虹がつながる2": BASS.bar(b, bass_line(S, b, "push"))
    elif n == "まばたき": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "逆さまの街": BASS.bar(b, bass_line(S, b, "half"))
    elif n == "鏡の街": BASS.bar(b, bass_line(S, b, "long") if i < 4 else bass_line(S, b, "root8"))
    elif n == "水面が戻る": BASS.bar(b, bass_line(S, b, "half") if i < 6 else "R:4")

# 逆再生（逆再生のクラッシュ・逆再生チャイナ）と、ライザー
for b in S.sc("鏡の街")[1::2]: cym_swell(CYM, b + 1, 2, "C4" if b % 4 == 1 else "D4")
cym_swell(CYM, S.sc("虹がつながる")[0], 2, "C4"); cym_swell(CYM, S.sc("まばたき")[0], 1, "D4"); cym_swell(CYM, S.sc("逆さまの街")[0], 4, "E4")
riser(FX, S.sc("虹がつながる2")[0], 4, "C4"); riser(FX, S.sc("全部の虹")[0], 8, "D4")
FX.bar(S.sc("しずくの音")[0], "E4:4")                  # ダウンリフター（静けさへ落ちる）
# しずく1つ（最後の1音）
GLASS.bar(S.sc("しずく1つ")[0], K.mel("R:1 5':3", oct=4))

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("しずく", "しずくの音", "しずく1つ"): D.set(b, "." * 16, "." * 16, "." * 16)
    elif n in ("水たまり", "水面が戻る"):
        if i < 4: D.set(b, "X.........X.....", "." * 16, "..x...x...x...x.")
        else: vgroove(D, b, "twostep", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if n == "水面が戻る" and i >= 6: D.set(b, "." * 16, "." * 16, "." * 16)
        if last and n == "水たまり": put_fill(D, b, "snare16")
    elif n in ("のぞきこむ", "別の街"):
        vgroove(D, b, "twostep" if i < 8 else "four16", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("虹が見える"):
        vgroove(D, b, "half" if i < 4 else "four", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2); D.cym(b, "A2:2")
    elif n == "虹がつながる":                      # 1回目: 4つ打ち
        vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if i == 7 else "tomdown")
    elif n == "虹がつながる2":                     # 2回目: 2ステップ（リズムの入れかえ）
        vgroove(D, b, "twostep", ghosts=0.45, seed=b)
        if 4 <= i < 12: D.cym(b, ("C2:1 " if i == 4 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "B2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomtrip")
        if last: halt(D, b, 1); D.cym(b, "C2:4")
    elif n == "まばたき":
        vgroove(D, b, "four" if i % 2 == 0 else "twostep", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i == 3 or i == 7: put_fill(D, b, "small" if i == 3 else "snare16")
    elif n == "逆さまの街":
        vgroove(D, b, "half", ghosts=0.45, seed=b, h="x...x...x...x...")
        if not last: D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "鏡の街":
        D.set(b, "X...X...X...X...", "." * 16, "." * 16 if i < 4 else "..x...x...x...x.")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)
    elif n == "全部の虹":
        vgroove(D, b, "four16" if i < 16 else "jersey", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); D.cym(b, "C2:4")

# 止め2回・1拍の完全な無音
SIL.add(S.sc("虹が見える")[-1], 2, 4)
SIL.add(S.sc("虹がつながる2")[-1], 1, 4)
SIL.add(S.sc("鏡の街")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の13。グリッチポップ。D長調（Aメロは B短調で）・148・転調なし。雨上がり、水たまりの虹をのぞくと別の街が映る。"
          "ガラスのしずくで始まり、ハープの水面、16分で語る Aメロ、短い句をくり返して止める Bメロ、5度・短6度・オクターブで光が散るサビ（Gm6・E7）。"
          "まばたきの間奏はグリッチのスタッターとガラスの逆行形の掛け合い、2番はハープが歌を受け取り、2回目のサビは2ステップ。しずくの音だけの静けさ、"
          "Half feel の逆さまの街、逆再生のシンバルで溜める鏡の街、1拍の無音のあと全部の虹。最後はしずく1つで終わる。歌の役は声のように聞こえるシンセ。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "雨", S.beats * 6, vol=0.08)
season(S, S.nb - 6, "小鳥", S.beats * 6, vol=0.06)
vwrite(S)
