# vb25 13「まばたきプリズム」Blink Prism（仮）— エレクトロニカ（グリッチポップ）。F#長調（Aメロは平行調の D#短調で）・148・4/4。転調なし
# 2026-10-25 作り直し: 物語を人の気持ちの話に（けんかした友だちに謝りに行く）、歌を人が歌える旋律（8分と4分）に、音を Surge の音に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を D長調から 8半音下げて F#長調にした（書くのは D長調の度数のまま、書き出しの前に下げる）。
# 物語: 雨上がりの帰り道。きのうのけんかで、ごめんねの一言が言えない。水たまりの虹をのぞいてまばたきすると、別の街に君が見える気がする。
#   会いたいけれどこわい。鏡の中の自分に背中を押されて、虹の橋をこえて謝りに行く。最後は仲直りの虹。
# 場面と強さ: しずく（ガラスの音だけ）→ 水たまり（ハープとしずく）→ 帰り道（Aメロ）→ 言えない（Bメロ・溜め・止め）→ まばたき（サビ）
#   → まばたき（間奏・グリッチ）→ 別の街（2番。BGM はハープが歌を受け取る）→ Bメロ2 → サビ2（2ステップ・止め）→ しずくの音（静けさ）
#   → 逆さまの街（Cメロ・Half feel）→ 鏡の街（逆再生・溜め）→ 1拍の無音 → 全部の虹（最後のサビ）→ 水面が戻る → しずく1つ
# 旋律の性格: 光が散るような5度・6度の跳躍と、短い句のくり返し。Bメロは「ごめんね」を言いかけては止まる下がる句。最高音 F#5。
# ほかの曲とちがう所: ハープとガラスの音のきらめき、グリッチ、逆再生。転調なし。
from vb25_lib import *

S = Song("13", "blinkprism", "まばたきプリズム（仮）", "Blink Prism", 148, 4, "D", "major", "グリッチポップ（ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
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

V = Voice(S, vol=0.22, delay=0.75, patch="popLeadClear", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
GLASS = S.track("ガラスの音（しずく・きらめき）", "pad", patch="surgeChordXyloChill", volume=0.08, pan=0.45, sustain=1.2, reverb=0.5,
                fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.35}])
HARP = S.track("ハープ", "harp", volume=0.13, pan=-0.35, reverb=0.35, sustain=1.6)
HARPM = S.track("ハープ（歌の受け渡し）", "harp", volume=0.18, pan=-0.35, reverb=0.35, sustain=1.6)
GLT = S.track("グリッチ（ビットクラッシュの刻み）", "lead", patch="surgeMixedFeelings", volume=0.07, pan=0.2, sustain=0.4, reverb=0.15,
              fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "bitcrusher", "bits": 6, "mix": 0.45}])
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadBellPad", vol=0.055, pan=0.0, duck=0.35, sustain=1.8)) for i in range(3)]
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassCatBass", vol=0.22, duck=0.25))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音（逆再生）", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（D長調の度数。oct=4 で 1 = D4。書き出しの前に全体を 8半音下げる） =================
VERSE = ["R:1 6:0.5 6:0.5 5:0.5 3':0.5 1':1", "6:2 R:2",
         "R:1 5:0.5 5:0.5 2':1 7:1", "5:2 R:2",
         "R:1 6:0.5 1':0.5 3':0.5 1':0.5 6:1", "5:2 R:2",
         "R:1 5:0.5 5:0.5 2':0.5 1':0.5 7:1", "#5:2 R:2",
         "R:1 1':0.5 1':0.5 7:0.5 6:0.5 3':1", "2':1 1':1.5 R:1.5",
         "R:1 7:0.5 7:0.5 1':0.5 2':0.5 3':1", "7:2 R:2",
         "R:1 6:0.5 6:0.5 3':0.5 2':0.5 1':1", "6:2 R:2",
         "R:1 5:0.5 4:0.5 2':1 7:1", "#5:2 R:2"]
V1 = "あめあがりの/かえりみち/みずたまりに/にじがうつる/きのうのけんか/むねにのこる/ごめんねすら/いえなくて"
V2 = "まばたきして/みずのなか/べつのまちが/ゆらゆらゆれ/きみもいまごろ/おなじそらを/みあげてたら/いいのにな"
BM = ["3':0.5 2':0.5 1':1 3':0.5 2':0.5 1':1", "3':0.5 2':0.5 7:1 3':0.5 2':0.5 7:0.5 R:0.5", "3':0.5 2':0.5 3':1 5':1 3':1", "1':2 R:1 1':0.5 2':0.5",
      "5':0.5 4':0.5 2':1 5':0.5 4':0.5 2':1", "#5':0.5 3':0.5 7:1 2':1 R:1", "6':1 3':1 2':2", "5':2 R:2"]
P1 = "ごめんねのひとことだけが/とおくにある/にじのはしをわたれたらね/いけるよ"
P2 = "あいたいけれどこわくてさ/あしがとまる/それでもにじのむこうがわ/いきたい"
CH1 = ["R:0.5 1':0.5 5':1 4':0.5 3':0.5 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "R:0.5 7:0.5 5':1 3':0.5 2':0.5 7:1", "1':1.5 7:0.5 6:2",
       "R:0.5 1':0.5 5':1 4':0.5 3':0.5 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 1'':1 6':1", "5':1 4':0.5 2':0.5 5':1 4':1", "2':3 R:1"]
CH1b = [CH1[0], "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1", "R:0.5 7:0.5 5':1 6':0.5 5':0.5 3':1", "4':1 3':1 1':2",
        "R:0.5 b6':0.5 b6':0.5 b6':0.5 4':1 2':1", "3':1 1':1 5:1.5 R:0.5", "2':0.5 #4':0.5 6':1 #4':1 2':1", "5':2 4':1 R:1"]
CH2 = CH1[:6] + ["5':1 6':0.5 5':0.5 4':1 2':1", "7:3 R:1"]
CH2b = CH1b[:6] + ["2':1 #4':1 6':1 1'':1", "7':2 5':2"]
TAGL = ["R:0.5 1':0.5 5':1 6':0.5 5':0.5 3':1", "R:0.5 3':0.5 3':0.5 3':0.5 7':1 5':1", "5':1 3':1 7:1 3':1", "1'':2 6':2",
        "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "5':1 7':1 6':1 5':1", "3':4", "R:4"]
C1 = "まばたきを/ぷりずむの/ひかりがくだける/まばたきを/きみのいるまちがみえた"
C1b = "にじいろの/はしをこえ/あやまりにいくよ/あめのあとのそら/にじがかかるよ"
C2 = "まばたきを/ぷりずむの/ひかりがくだける/まばたきを/きみもおなじそらみてた"
C2b = "にじいろの/はしをこえ/あやまりにいくよ/あめのあとのそら/かけだしてく"
CL = C1 + "/" + C1b + "/ありがとう/なかなおりのにじがでた/ぷりずむのそらのした"
UP = ["2':2 1':1 6:1", "3':3 R:1", "6:1 1':1 3':1 5':1", "7':3 R:1", "6':2 5':1 3':1", "5':3 R:1",
      "2':1 3':1 5':1 3':1", "#5':2 3':1 R:1", "2':1 4':1 6':2", "b6':2 4':1 R:1", "3':1 5':1 1'':2", "5':2 R:2"]
UPV = "さかさま/みずのまち/きみがね/わらっていたの/ほんとうは/あいたい"
MI = ["1':2 3':2", "2':2 7:2", "3':1 5':1 3':2", "1':3 R:1", "2':1 5':1 2':2", "3':2 #5':2", "6':2 3':2", "5':2 R:2"]
MIV = "かがみのなかのね/せなかをおしてる"
BACK = ["3':2 2':1 1':1", "6:3 R:1", "5:2 1':2", "7:3 R:1", "3':2 5':1 3':1", "2':4", "R:4", "R:4"]
LY = Lyrics(S)
def put(name, lines, text, low=True):
    bars = S.sc(name); mel = [K.mel(x, oct=4) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars, mel, text, name)
put("のぞきこむ", VERSE, V1)
if VOCAL: put("別の街", VERSE, V2)
else:
    for i, b in enumerate(S.sc("別の街")):
        line = K.mel(VERSE[i], oct=4)
        if i < 8: HARPM.bar(b, shift_oct(line, 1))                  # BGM: 別の街の前半は、ハープが歌を受け取る
        else: V.bar(b, line)
put("虹が見える", BM, P1); put("虹が見える2", BM, P2)
put("虹がつながる", CH1 + CH1b, C1 + "/" + C1b); put("虹がつながる2", CH2 + CH2b, C2 + "/" + C2b)
put("全部の虹", CH1 + CH1b + TAGL, CL)
put("逆さまの街", UP, UPV, low=lambda i: i >= 4)
put("鏡の街", MI, MIV, low=lambda i: i >= 4)
put("水面が戻る", BACK, "かえろう/ふたり/あおぞら", low=False)


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
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の13。グリッチポップ。F#長調（Aメロは D#短調）・148・転調なし。"
          "けんかした友だちに「ごめんね」を言いに行く雨上がり。ガラスのしずくで始まり、跳ねる Aメロ、言いかけては止まる Bメロ、光が散るような跳躍のサビ、グリッチの間奏、"
          "2ステップの2サビ、逆さまの街の Cメロ、鏡の街の逆再生と1拍の無音、仲直りの最後のサビ、しずく1つで終わる。ハープと Surge の音。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "雨", S.beats * 6, vol=0.08)
season(S, S.nb - 6, "小鳥", S.beats * 6, vol=0.06)
S.flags += " --space sky --space-wet 0.16"
teto(S, LY, V, transpose=-8, special={"全部の虹": 0.55, "逆さまの街": -0.5, "鏡の街": -0.15, "水面が戻る": -0.45})
