# vt25 15「ガラスの靴は履かない」I Won't Wear Glass Slippers（仮）— K-POP（ガールクラッシュ・ビッグビート×EDM）。128・4/4。F# の短調 → 最後のサビは +1（G の短調）。
#   （表では トラップ 102・808・弦のスタッカートだったが、第1弾の 15「フライパン・オーケストラ」（トラップ 104・808・ピッツィカート・C の短調）と
#     ほとんど同じになるので、ビッグビート×EDM の 128 にして、うなるリースベースと、ドロップの「押しつぶしたシンセ」（OTT のかわり）にした）
# 物語: 待っているだけのお姫さまは、もうやめた。魔法がとけるまで待つなんて、ごめんね。かぼちゃの馬車よりも、自分の足で行く。
#   12時の鐘なんて気にしない。ガラスの靴は履かないって決めた。靴ひもをしめて、かけだす。鏡よ鏡、答えはいらない。いちばんきれいかは、わたしが決める。
#   おとぎばなしなら、わたしが書く。最後のページはまだ白い。ハッピーエンドは、自分の手で。最後にガラスが割れる音。
# 場面と強さ: 一撃（インパクトと一言「まちません」）→ Aメロ1（低く強い語り）→ Bメロ1 → サビ1（強）→ ドロップ1（押しつぶしたシンセ・いちばん激しい音）
#   → Aメロ2（鏡よ鏡）→ Bメロ2 → サビ2 → ドロップ2 → 鏡の前（ひとり・とても弱い）→ 最後のサビ（+1）→ ガラスが割れる音で切る
# 旋律の性格: Aメロは低く強い語り（A3〜F#4 の同音の連打）。サビで高く張る（F#4 → A4 → C#5 → E5）。
# ほかの曲とちがう所（この曲だけの音）: ドロップで、シンセを音域ごとに強く押しつぶす（OTT のかわり）。うなるリースベース。終わりにガラスが割れる。
from vt25_lib import *

S = Song("15", "glassshoe", "ガラスの靴は履かない（仮）", "I Won't Wear Glass Slippers", 128, 4, "F#", "minor", "K-POP（ガールクラッシュ・ビッグビート×EDM・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.55
K = Key("F#", "minor")          # oct 3 で 1 = F#3。歌うのは A3〜E5
KL = Key("G", "minor")          # 最後のサビ（+1）

A_CH = ["F#m", "Dmaj7", "Bm7", "C#7"]
B_CH = ["Dmaj7", "E", "C#m7", "F#m", "Dmaj7", "E", "Bm7", "C#7"]
C_CH = ["Dmaj7", "E", "F#m", "F#m", "Dmaj7", "E", "C#m7", "F#m"]
DROP = ["F#m", "F#m", "Dmaj7", "E", "F#m", "F#m", "Bm7", "C#7"]
LAST = [tr_chord(c, 1) for c in C_CH * 2]

S.scene("一撃", 4, "intro", ["F#m", "F#m", "Dmaj7", "C#7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH * 2)
S.scene("ドロップ1", 8, "solo", DROP)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH * 2)
S.scene("ドロップ2", 12, "solo", DROP + ["F#m", "Dmaj7", "E", "C#7"])
S.scene("鏡の前", 8, "bridge", ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "D7"])     # 最後の小節は +1 への入り口
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("ガラス", 4, "outro", ["Gm", "Gm", "Gm", "Gm"])

V = Voice(S, vol=0.22, delay=0.75, bright=0.8, patch="sawLead", low=True)
REESE = S.track("うなるリースベース", "bass", **synth_bass_spec("reeseBass", vol=0.2, duck=0.35))
SUB = S.track("808", "sub808", volume=0.17, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}])
STAC = [S.track(f"弦のスタッカート{i + 1}", "strings", patch="stringEnsemble", volume=0.065, pan=-0.35 + 0.35 * i, reverb=0.3, sustain=0.3) for i in range(3)]
BRS = [S.track(f"ブラスの一撃{i + 1}", "brass", patch="brassSection", volume=0.07, pan=-0.25 + 0.25 * i, reverb=0.3, sustain=0.5) for i in range(3)]
SAW = [S.track(f"ドロップのシンセ{i + 1}", "pad", **pad_spec("surgeHappySaws", vol=0.05, pan=-0.45 + 0.45 * i, duck=0.5, sustain=0.6)) for i in range(3)]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.1, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 2.5}]) for i in range(3)]
GLS = S.track("ガラス（グロッケン）", "glockenspiel", patch="glockenspiel", volume=0.06, pan=0.4, reverb=0.45)
HIT = S.track("インパクト", "impactHit", volume=0.1, pan=0, reverb=0.3)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 3:0.5 1':1", "7:0.5 5:0.5 3:1 R:2", "R:0.5 4:0.5 4:0.5 4:0.5 6:0.5 4:0.5 2':1", "5:0.5 #7:0.5 5:1 R:2"]
A1 = ("まっているだけのひめ/そんなのもうやめた/まほうがとけるまで/まつなんてごめんね/"
      "かぼちゃのばしゃよりも/じぶんのあしでいく/じゅうにじのかねなど/わたしはきにしない")
A2 = "かがみよかがみさん/こたえはいらないの/いちばんきれいかは/わたしがきめるから/どくのりんごなんて/かじらないのわたし/ねむるのはまだあと/ゆめはじぶんでみる"
VB = ["R:0.5 5:0.5 5:0.5 6:0.5 7:1 5:1", "6:1.5 5:0.5 4:1 R:1", "R:0.5 5:0.5 5:0.5 6:0.5 1':1 7:1", "7:1.5 5:0.5 3:1 R:1",
      "R:0.5 1':0.5 1':0.5 2':0.5 3':1 1':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "#7:2 R:2"]
B1 = "かぼちゃはいらない/どれすもいらない/くつのひもをしめ/かけだすのよ"
B2 = "おとぎばなしなら/わたしがかくから/さいごのぺーじは/まだしろいの"
VC = ["R:0.5 1':0.5 1':0.5 3':0.5 5':1 3':1", "4':1 2':1 1':1 R:1", "R:0.5 1':0.5 1':0.5 3':0.5 5':1 7':1", "5':2 R:2",
      "R:0.5 3':0.5 3':0.5 5':0.5 7':1 6':1", "5':1 4':1 2':1 R:1", "R:0.5 3':0.5 4':0.5 5':0.5 7':1 5':1", "1':2 R:2"]
C1 = "がらすのくつはね/はかないもん/じぶんのあしでね/はしるんだよ/おうじさまなんか/またないから/じゅうにじすぎても/とまらないの"
C2 = "がらすのくつはね/われていいよ/はだしのままでも/いけるからね/まほうのかわりに/えらぶのはね/たいせつなものを/このてでとる"
CL = "がらすのくつはね/はかないもん/じぶんのあしでね/はしるんだよ/このものがたりは/わたしがかく/はっぴーえんどはね/じぶんのてで"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("一撃", K, ["R:4", "R:1 5:0.5 5:0.5 1':0.5 3':0.5 1':1", "R:4", "R:4"], "まちません")
put("Aメロ1", K, VA * 4, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC, C1); put("サビ2", K, VC + VC, C2)
put("最後のサビ", KL, VC + VC, CL)
if VOCAL: put("Aメロ2", K, VA * 4, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA * 4)):
        if i < 8: BRS[0].bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 伴奏 =================
DROPM = ["F#5:0.5 F#5:0.25 A5:0.25 R:0.5 C#6:0.5 R:0.5 A5:0.5 E5:1", "F#5:0.75 A5:0.75 C#6:0.5 E6:1 C#6:1",
         "F#5:0.5 F#5:0.25 A5:0.25 R:0.5 D6:0.5 R:0.5 C#6:0.5 A5:1", "G#5:1 B5:1 E6:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 64, 3); r = low(ch, "E1"); bv = voice(ch, 67, 3)
    if n == "一撃":
        if i in (0, 2): HIT.bar(b, f"{nm(r + 12)}:4")
        for j in range(3): STAC[j].bar(b, f"{nm(v[j])}:0.25! R:3.75" if i % 2 == 0 else "R:4")
        continue
    if n in ("Aメロ1", "Aメロ2"):
        REESE.bar(b, f"{nm(r)}:1.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.5 R:0.5")
        for j in range(3): STAC[j].bar(b, f"{nm(v[j])}:0.25 R:0.75 {nm(v[j])}:0.25 R:0.5 {nm(v[j])}:0.25 R:2" if i % 2 == 0 else f"R:2 {nm(v[j])}:0.25 R:0.25 {nm(v[j])}:0.25 R:1.25")
        if i % 4 == 3 and not (n == "Aメロ2" and not VOCAL):
            for j in range(3): BRS[j].bar(b, f"R:3 {nm(bv[j])}:0.5! R:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        REESE.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(8)))
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1")
        if i == 7:
            for j in range(3): STAC[j].bar(b, " ".join(f"{nm(v[j])}:0.25" for _ in range(16)))
    elif n.startswith(("サビ", "最後")):
        REESE.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r + 12)}:0.5 {nm(r)}:1 {nm(r + 7)}:1")
        SUB.bar(b, f"{nm(r + 12 if r < 30 else r)}:2 {nm(r + 12 if r < 30 else r)}:2")
        for j in range(3): STAC[j].bar(b, " ".join(f"{nm(v[j])}:0.25" if q % 2 == 0 else "R:0.25" for q in range(16)))
        for j in range(3): BRS[j].bar(b, f"{nm(bv[j])}:0.5! R:1.5 {nm(bv[j])}:0.25 R:0.25 {nm(bv[j])}:0.5 R:1" if i % 2 == 0 else "R:4")
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
    elif n in ("ドロップ1", "ドロップ2"):
        REESE.bar(b, f"{nm(r)}:0.5 R:0.25 {nm(r)}:0.25 {nm(r + 12)}:0.5 R:0.5 {nm(r)}:0.75 {nm(r + 10)}:0.25 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5")
        SUB.bar(b, f"{nm(r + 12 if r < 30 else r)}:4")
        sv = voice(ch, 66, 3)
        for j in range(3): SAW[j].bar(b, " ".join(f"{nm(sv[j])}:0.25" if q % 4 != 2 else "R:0.25" for q in range(16)))
        GLS.bar(b, DROPM[i % 4])
    elif n == "鏡の前":
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:4")
        if i % 2 == 0: GLS.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]) + " R:2")
    elif n == "ガラス":
        if i == 0:
            HIT.bar(b, "G2:4")
            GLS.bar(b, " ".join(f"{nm(x)}:0.0625" for x in range(96, 80, -1)) + " R:3")       # ガラスが割れる（高い音が一気に落ちる）
            CYM.bar(b, "F4:4")
riser(FX, S.sc("ドロップ1")[0], 4, "C4"); riser(FX, S.sc("ドロップ2")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 8, "D4")
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "一撃":
        if i in (0, 2): D.set(b, "X" + "." * 15, "." * 16, "." * 16)
        if i == 3: put_fill(D, b, "snare16")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "bigbeat", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X.......X.......", "........XXXXXXXX", "................")
    elif n.startswith(("サビ", "最後")):
        vgroove(D, b, "four16", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown")
    elif n in ("ドロップ1", "ドロップ2"):
        vgroove(D, b, "four", ghosts=0.2, seed=b, s="....X..X....X...", h="..O...O...O...O.")
        if i % 4 == 0: crash(D, b)
    elif n == "鏡の前":
        if last: put_fill(D, b, "build")
    elif n == "ガラス" and i == 0:
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)

SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の15。K-POP（ガールクラッシュ・ビッグビート×EDM）。F# の短調・128、最後のサビは +1（G の短調）。"
          "待っているだけはやめた。自分の足で走ると決める。インパクトの一撃と「まちません」で始まり、低く強い語りの Aメロ、高く張るサビ、"
          "シンセを音域ごとに押しつぶすドロップ、うなるリースベース、鏡の前のひとり、最後はガラスが割れる音で切る。自作")
finish(S, LY, V, 0, fx=[{"type": "ott", "scenes": ["ドロップ1", "ドロップ2"], "depth": 0.45}, {"type": "ott", "scenes": ["最後のサビ"], "depth": 0.2}],
       level={"verse": -0.15}, special={"鏡の前": -0.6, "最後のサビ": 0.5, "一撃": 0.1})
