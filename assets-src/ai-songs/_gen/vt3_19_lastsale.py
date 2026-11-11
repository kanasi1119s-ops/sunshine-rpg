# vt3 19「商店街ラストセール」Last Sale on Shopping Street（仮）— サンバ。104・4/4（16分の倍のノリ）。C長調 → 最後のサビは +1（D♭）。
# 第3弾（0時〜24時の街）の 18時。表は docs/sound/vt3-plan.md。
# 物語: 夕方6時。60年続いた商店街の店が、今日でぜんぶ閉まる。シャッターには「ありがとう」の張り紙。
#   だから最後はお祭りに。魚屋さんはベルを鳴らし、八百屋さんはかごをたたき、本屋さんは鈴を振る。
#   駄菓子屋の前には、昔のわたしみたいな子どもたち。どこかの店のラジオから流れたあの節を、みんなで歌う。
#   涙はないしょで、手をたたけば笑える。最後のシャッターが下りる音で終わる。
# 場面と強さ: ホイッスル → イントロ（打楽器とブラス・強）→ Aメロ1（はずむ・中）→ Bメロ1（さみしい・止め）→ サビ1（強）
#   → 間奏（ブラスの節）→ Aメロ2 → Bメロ2 → サビ2 → バトゥカーダ（打楽器だけ・いちばん熱い）→ シャッターの前（静か）
#   → 最後のサビ（+1）→ シャッター
# 旋律の性格: 16分で跳ねる明るい句、掛け声。サビは「らすとせーるだよ」で高い所から始まる。
# この曲だけの音: サンバの打楽器（スルド＝低い太鼓・タンボリン・ガンザ・アゴゴ＝カウベル・ホイッスル）とバトゥカーダのソロ。
#   合いことばの節（3・5・6・5・2＝E・G・A・G・D）は、間奏のブラス。
from vt25_lib import *

S = Song("19", "lastsale", "商店街ラストセール（仮）", "Last Sale on Shopping Street", 104, 4, "C", "major", "サンバ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
K = Key("C", "major"); KL = Key("Db", "major")      # oct 4 で 1 = C4

A_CH = ["Cmaj7", "A7", "Dm7", "G7"]
B_CH = ["Am7", "D7", "Dm7", "G7", "Am7", "D7", "Dm7", "G7"]
C_CH = ["F", "G", "Em7", "A7", "Dm7", "G7", "C", "C", "F", "G", "Em7", "A7", "Dm7", "G7", "C", "C"]

S.scene("ホイッスル", 2, "intro", ["C", "C"])
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("バトゥカーダ", 8, "solo", ["C"] * 7 + ["G7"])
S.scene("シャッターの前", 4, "bridge", ["Fmaj7", "Em7", "Dm7", "Ab7"])        # 最後は D♭ への入り口
S.scene("最後のサビ", 16, "chorus", [tr_chord(c, 1) for c in C_CH])
S.scene("シャッター", 2, "outro", ["Db", "Db"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
BRS = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.06, pan=0.25, reverb=0.25, sustain=0.5) for i in range(3)]
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.1, pan=0.1, reverb=0.25)
CAV = [S.track(f"カヴァキーニョのかわり（バンジョー）{i + 1}", "banjo", volume=0.06, pan=-0.4, reverb=0.2) for i in range(3)]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.06, pan=-0.2, reverb=0.25) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.21))
SURDO = S.track("スルド（低い太鼓）", "inchTom", volume=0.13, pan=0, reverb=0.2)
TAMB = S.track("タンボリン（高い太鼓）", "cajon", volume=0.07, pan=0.35, reverb=0.12)
AGO = S.track("アゴゴ（カウベル）", "pad", patch="seasonFx", volume=0.05, pan=-0.3, reverb=0.1, modulate=False)
WHI = S.track("ホイッスル（ピッコロ）", "lead", patch="piccolo", volume=0.07, pan=0.2, reverb=0.2)
SHUT = S.track("シャッター（低い一撃）", "impactHit", volume=0.07, pan=0, reverb=0.3)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 R:0.25 5:0.25 6:0.5 5:0.5 3:0.5 R:1", "R:0.5 2:0.25 3:0.25 R:0.25 4:0.25 3:0.5 2:1 R:1",
      "R:0.5 5:0.25 5:0.25 R:0.25 5:0.25 1':0.5 7:0.5 6:0.5 R:1", "R:0.5 6:0.25 5:0.25 R:0.25 4:0.25 3:0.5 2:1 R:1",
      "R:0.5 5:0.25 5:0.25 R:0.25 5:0.25 6:0.5 5:0.5 3:0.5 R:1", "R:0.5 2:0.25 3:0.25 R:0.25 5:0.25 6:0.5 5:1 R:1",
      "R:0.5 4:0.5 4:0.5 3:0.5 4:0.5 5:0.5 6:0.5 7:0.5", "1':2 R:2"]
A1 = ("ろくじのかね/なるまえに/さかなやさん/べるならす/やおやさんは/かごたたく/ほんやのすずのね/"
      "きょうでさいご/しゃったーには/はりがみがね/ありがとう/ろくじゅうねん/ながいこと/さいごはおまつり")
A2 = "だがしやのこ/あつまるよ/むかしわたし/ここにいた/らじおからは/あのふしが/みんなでうたうよ"
VB = ["R:1 6:1 6:1 5:1", "4:2 3:1 R:1", "R:1 5:1 5:1 4:1", "3:2 2:1 R:1",
      "R:1 6:1 1':1 2':1", "3':2 2':1 R:1", "R:0.5 2':0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:1", "R:4"]
B1 = "さみしいね/でもいいの/わらおうよ/さいごまでね"
B2 = "ねびきだよ/ぜんぶもって/おまけつき/えがおもつけ"
VC = ["1':0.5 1':0.5 1':0.5 2':0.5 3':1 1':1", "2':1.5 1':0.5 6:1 R:1", "7:0.5 7:0.5 7:0.5 1':0.5 2':1 7:1", "1':1.5 6:0.5 5:1 R:1",
      "6:0.5 6:0.5 6:0.5 7:0.5 1':1 6:1", "5:1.5 4:0.5 2:1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 3':1 2':1", "1':3 R:1",
      "3':0.5 3':0.5 3':0.5 4':0.5 3':1 1':1", "2':1.5 1':0.5 6:1 R:1", "2':0.5 2':0.5 2':0.5 3':0.5 2':1 7:1", "1':1.5 6:0.5 5:1 R:1",
      "6:0.5 6:0.5 6:0.5 7:0.5 1':1 6:1", "5:1.5 4:0.5 2:1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 4':1 3':1", "1':3 R:1"]
HOOK = "らすとのせーるだよ"
C1 = f"{HOOK}/まちじゅうでおどろう/まちかどのさんばだ/ならせならせ/{HOOK}/あかりがきえてもね/このよるのたいこは/ひびいてるよ"
C2 = f"{HOOK}/ほいっするをふいてね/おまつりみたいだね/さよならだよ/{HOOK}/なみだはないしょでね/てをたたけばほらね/わらえるでしょ"
C3 = f"{HOOK}/ありがとうこのまち/しゃったーがしまってもね/おぼえてるよ/{HOOK}/またどこかであおう/さいごにしまるおと/ひびくんだよ"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("最後のサビ", KL, VC, C3)

# ================= 和音の楽器 =================
def cav(b, ch):
    """カヴァキーニョの16分のかき鳴らし（サンバのノリ: 2拍目と4拍目の裏を強く）"""
    v = voice(ch, 67, 3)
    for j in range(3): CAV[j].bar(b, f"{nm(v[j])}:0.25 R:0.25 {nm(v[j])}:0.25 {nm(v[j])}:0.25 R:0.25 {nm(v[j])}:0.25! {nm(v[j])}:0.25 R:0.25 "
                                  f"{nm(v[j])}:0.25 R:0.25 {nm(v[j])}:0.25 {nm(v[j])}:0.25 R:0.25 {nm(v[j])}:0.25! {nm(v[j])}:0.25 R:0.25")


def brass(b, ch, pat):
    v = voice(ch, 67, 3)
    for j in range(3): BRS[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def piano(b, ch):
    v = voice(ch, 62, 3)
    for j in range(3): PN[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:1 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")


MOTIF = ["R:1 E5:0.5 G5:0.5 A5:1 G5:0.5 D5:0.5", "C5:3 R:1"]      # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        cav(b, ch); brass(b, ch, "x:0.5! R:0.25 x:0.25 R:1 x:0.5 x:0.5 R:1" if i % 2 == 0 else "R:2 x:0.25 x:0.25 x:0.5 x:1")
        TP.bar(b, ["R:2 G5:0.5 A5:0.5 C6:1", "B5:1 G5:1 E5:2", "R:2 F5:0.5 G5:0.5 A5:1", "G5:3 R:1"][i % 4])
    elif n in ("Aメロ1", "Aメロ2"):
        cav(b, ch)
        if n == "Aメロ2" or i >= 8: piano(b, ch)
        if i % 4 == 3: brass(b, ch, "R:3 x:0.5 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: piano(b, ch); brass(b, ch, "x:4") if i % 2 == 0 else None
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        cav(b, ch); piano(b, ch)
        brass(b, ch, "R:1.5 x:0.5 R:1 x:0.5 x:0.5" if i % 2 == 0 else "R:2.5 x:0.25 x:0.25 x:1")
    elif n == "間奏":
        cav(b, ch)
        TP.bar(b, MOTIF[i] if i < 2 else ["R:1 G5:0.5 A5:0.5 C6:1 A5:1", "G5:2 E5:2", "R:1 F5:0.5 E5:0.5 D5:1 C5:1", "D5:2 G5:2", "R:0.5 E5:0.5 G5:0.5 C6:0.5 B5:1 G5:1", "C6:3 R:1"][i - 2])
        brass(b, ch, "x:0.5! R:3.5" if i % 2 == 0 else "R:4")
    elif n == "シャッターの前":
        v = voice(ch, 62, 3)
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:4")
    elif n == "シャッター":
        if i == 0: brass(b, ch, "x:0.5! R:3.5"); cav(b, ch) if False else None

# ================= 打楽器（スルド・タンボリン・アゴゴ・ホイッスル）=================
def bateria(b, hot=False):
    SURDO.bar(b, "R:1 F1:1 R:1 A1:1" if not hot else "F1:0.5 R:0.5 A1:1 F1:0.5 R:0.25 F1:0.25 A1:1")
    TAMB.bar(b, "E3:0.25 R:0.25 E3:0.25 E3:0.25 R:0.25 E3:0.25 R:0.5 E3:0.25 R:0.25 E3:0.25 E3:0.25 R:0.25 E3:0.25 R:0.5" if not hot
             else " ".join(["E3:0.25"] * 16))
    AGO.bar(b, "C5:0.5 C5:0.25 R:0.25 C5:0.5 R:0.5 C5:0.5 C5:0.25 R:0.25 C5:0.5 R:0.5")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ホイッスル":
        WHI.bar(b, "C7:0.25 R:0.25 C7:0.25 R:0.25 C7:1 R:2" if i == 0 else "C7:0.25 R:0.25 C7:0.25 R:0.25 C7:0.25 R:0.25 C7:0.25 R:0.25 C7:1 R:1")
    elif n == "バトゥカーダ":
        bateria(b, hot=i >= 4)
        if i % 2 == 1: WHI.bar(b, "R:2 C7:0.25 R:0.25 C7:0.25 R:0.25 C7:0.5 R:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: SURDO.bar(b, "R:1 F1:1 R:1 A1:1")
    elif n in ("シャッターの前", "シャッター"):
        pass
    else:
        bateria(b)
        if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 7: WHI.bar(b, "R:2 C7:0.25 R:0.25 C7:0.25 R:0.25 C7:1")
SHUT.bar(S.sc("シャッター")[1], "D1:2 R:2")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("ホイッスル", "バトゥカーダ"): continue
    if n == "シャッターの前": BASS.bar(b, f"{nm(r)}:4"); continue
    if n == "シャッター": BASS.bar(b, f"{nm(r)}:0.5 R:3.5" if i == 0 else "R:4"); continue
    if n in ("Bメロ1", "Bメロ2") and i == 7: continue
    BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.25 {nm(r + 7)}:0.75 {nm(r + 7)}:0.25 {nm(r)}:0.75 {nm(r)}:0.25 {nm(r + 7)}:0.75 {nm(r + 12)}:0.25")

# ================= ドラム（軽い。打楽器が主役）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("ホイッスル", "シャッターの前"):
        if n == "シャッターの前" and i == 3: put_fill(D, b, "build")
        continue
    if n == "シャッター":
        if i == 0: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
        continue
    if n == "バトゥカーダ":
        if i == 7: put_fill(D, b, "snare16")
        continue
    if n in ("Bメロ1", "Bメロ2"):
        if i < 7: D.set(b, "X.......X.......", "....x.......x...", "x.x.x.x.x.x.x.x.")
        continue
    vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X..X....X..X....", s="....X..x....X..x", h="xxxxxxxxxxxxxxxx")
    if n in ("サビ1", "サビ2", "最後のサビ", "イントロ") and i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
    if i % 8 == 7 and not last: put_fill(D, b, "small")

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の19（18時）。サンバ。C長調・104（16分の倍のノリ）、最後のサビは +1。"
          "60年続いた商店街の最後の日を、お祭りにする。スルド・タンボリン・アゴゴ・ホイッスルとバトゥカーダのソロ、ブラス・カヴァキーニョのかわりのバンジョー。"
          "合いことばの節は間奏のトランペット。シャッターが下りる音で終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"シャッターの前": -0.6, "最後のサビ": 0.35, "バトゥカーダ": 0.1})

# ================= v2（2026-11-12 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後6時・商店街のラストセール・サンバ）で直すこと:
#   ホイッスル: フルートの仲間（ピッコロ）をやめ、本物の「玉の入った笛」の録音（toysFx）に（サンバの笛そのもの）。長い音は長い笛、短い音は短い笛
#   カヴァキーニョ（バンジョー）とピアノは、1音ずつ強さを揺らす
#   歌: Aメロ・Bメロはクリア（呼びこみ）、サビはキュート、シャッターの前はウィスパー。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
js = load(path)
for p in js["parts"]:
    if p.get("role", "").startswith("ホイッスル"):
        p["patch"] = "toysFx"; p["modulate"] = False; p["role"] = "ホイッスル（玉の入った笛）"; p["volume"] = 0.05
        p["notes"] = " ".join(t if t.startswith("R") else ("E4:" if float(re.match(r"[0-9.]+", t.split(":")[1]).group(0)) >= 1 else "D#4:") + t.split(":")[1] for t in p["notes"].split())
save(path, js)
humanize(path, "カヴァキーニョ", mid=84, down=12, up=10, seed=3); humanize(path, "ピアノ", mid=82, down=12, up=10, seed=4)
set_parts(path, "ベース（指", sustain=1.12)
final_gain(path, {"ホイッスル": 12, "最後のサビ": 1.8, "シャッター": 3})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "最後のサビ": 22, "bridge": 6, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL)], vol=0.36)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute", "bridge": "whisper"}, default="clear")
