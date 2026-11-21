# vt3 11「洗濯日和のステップ」Laundry-Day Step（仮）— ケルトのジグ（8分の6）。8分＝260（付点4分＝87。作曲ソフトの上限）。D長調 → 最後のくり返しは E。
# 第3弾（0時〜24時の街）の 10時。表は docs/sound/vt3-plan.md。
#
# v2（2026-11-15）: ゼロから作り直し。人間の指示（2026-11-15）:「ボカロ系の曲は、ロック、テクノポップ、ファンク、KPOP、ダンス、ケルトで作り直そう」
#   「曲の構成も11から既存の作り方とは違う構成にしてみて」→ この曲はケルト。v1 はスパニッシュギターのレゲトンだった。
#
# 構成（今までの「前奏 → Aメロ → Bメロ → サビ → 間奏 → …」をやめる。ケルトの歌の形）:
#   歌（同じ節で3番まで）と、みんなで歌う「くり返し」と、フィドルのジグ（踊りの曲）が交互に進む。Bメロもブリッジもない。
#   ハープ → ジグ1（曲A）→ 歌1 → くり返し1 → ジグ2（曲A・アコーディオン）→ 歌2 → くり返し2 → ジグ3（曲B → 曲A。2つの曲をつなげる）
#   → 歌3（ハープと声だけ）→ くり返し3 → くり返し4（E に上がる・いちばん大きい）→ 曲A で終わり、洗濯ばさみの「パチン」
#
# 物語: 晴れた10時のベランダ。白いシーツを広げると、風が背中を押して、からだが勝手にゆれ出す。おとなりさんの手拍子、踊り出すシャツとタオル、空へとんでいくくつした。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: へった分だけ軽くなる、しわは笑ったあと ──「まあいいか」。
#
# 曲を決める表:
#   旋律: 歌＝ジグの「長・短」（4分と8分）にのる7音の行を8行。くり返し＝「まあ・いいか」（5音）と3音の返事を2回 → 長い1行（13音）
#   和音: 歌 I・IV・vi・ii・V。くり返しは IV から入る（IV → I → V → vi）
#   ベース: 付点4分の根音（1小節に2つ）。ジグ3 と最後だけ、8分で5度へ動く
#   この曲だけ: ①8分の6のジグ ②歌とジグが交互（踊りの曲を2つつなげる）③同じ節の歌が3番まで ④バウロン（わく太鼓）の役の低い太鼓
#   音色: フィドル（節）・アコーディオン（持続音と節）・ハープ（分散和音）・低い太鼓・ベース。歌のない版の旋律は電子の音（笛の音は指定がない限り使わない）
#
# ケルトの作り方（docs/sound/composer-preferences.md のケルトの決まり・ケルト100曲で調べたこと）: ジグは 8分の6 で「タータ・タータ」。
#   旋律の楽器（フィドル・アコーディオン）は同じ節をいっしょに弾く（ユニゾン）。伴奏は持続音と分散和音で、和音を厚くしすぎない。
#   2つ以上の曲をつなげて弾く（セット）。音に強弱と余韻をつける。
from vt25_lib import *

S = Song("11", "laundry", "洗濯日和のステップ（仮）", "Laundry-Day Step", 260, 6, "D", "major", "ケルトのジグ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space hall --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.4
S.keepers = {}
K = Key("D", "major")          # oct 4 で 1 = D4
KE = Key("E", "major")

TA = ["D", "D", "G", "A", "D", "Bm", "A", "D"]
TB = ["Bm", "G", "D", "A", "Bm", "G", "A", "D"]
V_CH = ["D", "D", "G", "D", "D", "Bm", "Em", "A", "D", "D", "G", "D", "Bm", "G", "A", "D"]
R_CH = ["G", "D", "A", "Bm", "G", "D", "A", "A", "G", "D", "A", "Bm", "G", "A", "D", "D"]

S.scene("ハープ", 4, "intro", ["D", "D", "G", "A"])
S.scene("ジグ1", 16, "intro", TA + TA)
S.scene("歌1", 16, "verse", V_CH)
S.scene("くり返し1", 16, "chorus", R_CH)
S.scene("ジグ2", 16, "break", TA + TA)
S.scene("歌2", 16, "verse", V_CH)
S.scene("くり返し2", 16, "chorus", R_CH)
S.scene("ジグ3", 32, "solo", TB + TB + TA + TA)
S.scene("歌3", 16, "bridge", V_CH)
S.scene("くり返し3", 16, "chorus", R_CH)
S.scene("くり返し4", 16, "chorus", [tr_chord(c, 2) for c in R_CH])
S.scene("おわり", 10, "outro", [tr_chord(c, 2) for c in TA] + ["E", "E"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead", low=False)
# v9（2026-11-21）: 人間「16までの曲達オーケストラ系の楽器全部変更」→ フィドル・ハープ2本・弦・マリンバを、アコギ・アコギの分散和音・シンセのパッド・木のようなシンセに（音の並びはそのまま。アコーディオンはそのまま）
FID = S.track("フィドル（アコギの節）", "guitar", patch="nylonGuitar", amp="clean", volume=0.2, pan=-0.2, reverb=0.3, chorus=0, fx=[{"type": "boost", "gain": 8}])
ACC = S.track("アコーディオン（節）", "accordion", volume=0.1, pan=0.25, reverb=0.25)
ACL = [S.track(f"アコーディオン（持続音{i + 1}）", "accordion", volume=0.04, pan=0.35 - 0.2 * i, reverb=0.3) for i in range(2)]
HARP = S.track("ハープ（エレピの分散和音）", "keys", volume=0.2, pan=-0.35, reverb=0.35, sustain=1.6, fx=[{"type": "boost", "gain": 3}])
HARP2 = S.track("ハープ（エレピの上の線）", "keys", volume=0.2, pan=0.3, reverb=0.4, sustain=1.6)
BOD = S.track("低い太鼓（バウロンの役）", "inchTom", volume=0.14, pan=0.05, reverb=0.2)
STR = [S.track(f"シンセのパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.08, pan=-0.4 + 0.8 * i, reverb=0.45, sustain=1.5) for i in range(2)]
BASS = S.track("ベース（指弾き・丸い音）", "bass", sustain=1.0, **dict(finger_bass_spec(vol=0.2), fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 1200, "q": 0.6}]))
PIN = S.track("洗濯ばさみのパチン（木のようなシンセ）", "lead", patch="surgeWoody", volume=0.1, pan=0.4, reverb=0.15)
D = S.drumkit()

# ================= 歌（拍は8分。1小節＝6。4分＝2、8分＝1）=================
VV = ["1:2 1:1 3:2 5:1", "5:2 6:1 5:2 R:1", "6:3 6:1 5:1 3:1", "3:1 2:2 1:2 R:1",
      "1:2 3:1 5:2 1':1", "1':2 7:1 6:2 R:1", "4:3 4:1 6:1 4:1", "5:1 7,:2 2:2 R:1",
      "1:2 1:1 3:2 5:1", "6:2 5:1 6:2 R:1", "1':3 1':1 6:1 5:1", "5:1 3:2 5:2 R:1",
      "6:3 6:1 1':1 6:1", "6:1 5:2 4:2 R:1", "5:2 5:1 7:2 2':1", "1':3 R:3"]
V1 = "はれたじゅうじの/べらんだにでて/しろいしーつを/ひろげてみたら/かぜがせなかを/ぽんとおしたよ/からだがかってに/ゆれだした"
V2 = "おとなりさんが/てびょうしくれて/しゃつもたおるも/おどりだしたよ/くつしたひとつ/そらへとんでく/おいかけないで/てをふるよ"
V3 = "せんたくきがね/うたいおえたら/そらのまんなか/おひさまひとつ/しわもよごれも/えがおのあとさ/ぱちんととめて/できあがり"
# くり返し: 「まあ・いいか」（5音）→ 3音の返事、を2回 → 長い1行
HOOK1 = "6:2 6:1 5:1 4:1 6:1"
HOOK2 = "5:2 5:1 4:1 2:1 5:1"
VR = [HOOK1, "R:1 5:1 3:1 5:2 R:1", HOOK2, "R:1 3:1 5:1 6:2 R:1", "4:2 6:1 1':2 6:1", "5:2 3:1 5:2 1':1", "2':2 1':1 7:2 5:1", "5:3 R:3",
      HOOK1, "R:1 5:1 3:1 5:2 R:1", HOOK2, "R:1 3:1 5:1 6:2 R:1", "4:2 6:1 1':2 2':1", "2':2 1':1 7:2 R:1", "1':2 1':1 7:1 6:1 1':1", "R:6"]
R1 = "まあいいか/そらは/まあいいか/あおい/かぜにふかれてゆれていよう/まあいいか/ぬれて/まあいいか/いても/あとはおひさま/まあいいか"
R2 = "まあいいか/ひとつ/まあいいか/へれば/へったぶんだけかるくなるよね/まあいいか/しわも/まあいいか/あじさ/わらったあとだよ/まあいいか"
R3 = "まあいいか/きょうも/まあいいか/あすも/まっさらにあらってほしていこう/まあいいか/うたう/まあいいか/おどる/はだしのままで/まあいいか"
R4 = "まあいいか/そらは/まあいいか/あおい/かぜにふかれてゆれていよう/まあいいか/きょうは/まあいいか/いいひ/せんたくびより/まあいいか"
LY = Lyrics(S)


def put(name, lines, text, key=K, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("歌1", VV, V1); put("くり返し1", VR, R1)
put("歌2", VV, V2); put("くり返し2", VR, R2)
put("歌3", VV, V3); put("くり返し3", VR, R3)
put("くり返し4", VR, R4, key=KE)

# ================= ジグ（踊りの曲）=================
TUNE_A = ["D5:1 F#5:1 A5:1 F#5:1 D5:1 F#5:1", "A5:2 B5:1 A5:1 F#5:1 D5:1", "G5:1 B5:1 D6:1 B5:1 G5:1 B5:1", "A5:1 C#6:1 E6:1 C#6:2 A5:1",
          "D6:2 A5:1 F#5:1 A5:1 D6:1", "B5:1 D6:1 B5:1 F#5:2 B5:1", "A5:1 C#6:1 A5:1 E5:1 G5:1 E5:1", "D5:3 D5:2 R:1"]
TUNE_B = ["B4:1 D5:1 F#5:1 B5:2 F#5:1", "G5:1 B5:1 G5:1 D5:1 G5:1 B5:1", "A5:2 F#5:1 D5:1 F#5:1 A5:1", "E5:1 A5:1 C#6:1 E6:2 C#6:1",
          "D6:1 B5:1 F#5:1 B5:1 D6:1 B5:1", "G5:2 B5:1 D6:2 B5:1", "C#6:1 A5:1 E5:1 A5:1 C#6:1 E6:1", "D6:3 D5:2 R:1"]
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


def harp(b, order=(0, 2, 3, 4, 3, 2), lo="D3", hi="D5", tr=None):
    tn = tones(root(b), lo, hi); (tr or HARP).bar(b, " ".join(f"{nm(tn[q % len(tn)])}:1" for q in order))


def drone(b, c=62):
    """v7: アコーディオンの持続音はやめた。場面ごとに採点すると、持続音のある場面だけ低かった（歌1 7.30・歌2 7.00・くり返し 7.25。持続音のない ジグ2 は 7.87、歌3 は 7.90）。
    かわりに、くり返しとジグ3 では弦ののばす音を使う"""
    if S.scene_of(b)[0].startswith("くり返し") or S.scene_of(b)[0] in ("ジグ3", "おわり"): strs(b, c + 5)


def strs(b, c=69):
    v = sorted(voice(root(b), c, 3)); STR[0].bar(b, f"{nm(v[0])}:6"); STR[1].bar(b, f"{nm(v[2])}:6")


LOB, HIB = "F1", "A1"
BOD_A = f"{LOB}:2 {HIB}:1 {LOB}:1 {HIB}:1 {HIB}:1"          # ドン・タ ド・タ・タ
BOD_B = f"{LOB}:1 {HIB}:1 {HIB}:1 {LOB}:2 {HIB}:1"
BOD_S = f"{LOB}:3 {LOB}:2 {HIB}:1"                           # 静かな型
BOD_F = f"{LOB}:1 {HIB}:1 {HIB}:1 {LOB}:1 {LOB}:1 {LOB}:1"   # 場面の変わり目
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ハープ":
        harp(b)
        if i == 2: HARP2.bar(b, "F#5:1 A5:1 B5:2 A5:1 E5:1")              # 合いことばの節（3・5・6・5・2）
        if i == 3: HARP2.bar(b, "A5:2 C#6:1 E6:3")
    elif n == "ジグ1":                                                    # 前半: フィドルとハープだけ → 後半: 持続音・太鼓・ベース
        FID.bar(b, TUNE_A[i % 8]); harp(b)
        if i >= 8: drone(b); BOD.bar(b, BOD_F if last else (BOD_A if i % 2 == 0 else BOD_B))
    elif n == "ジグ2":                                                    # 前半: アコーディオンが節 → 後半: フィドルもいっしょに（ユニゾン）
        ACC.bar(b, TUNE_A[i % 8]); harp(b, (0, 3, 2, 4, 2, 3)); BOD.bar(b, BOD_F if last else (BOD_A if i % 2 == 0 else BOD_B))
        if i >= 8: FID.bar(b, TUNE_A[i % 8]); strs(b, 66)
    elif n == "ジグ3":                                                    # 曲B を2回（フィドル → 2人）→ 曲A を2回（全員・2回目は弦も）
        tune = TUNE_B if i < 16 else TUNE_A
        FID.bar(b, tune[i % 8]); harp(b, (0, 2, 3, 4, 3, 2) if i % 2 == 0 else (0, 3, 2, 4, 2, 3)); drone(b)
        if i % 16 >= 8 or i >= 16: ACC.bar(b, tune[i % 8])
        if i >= 24: strs(b, 69)
        BOD.bar(b, BOD_F if i % 8 == 7 else (BOD_A if i % 2 == 0 else BOD_B))
    elif n in ("歌1", "歌2"):
        harp(b, (0, 2, 3, 4, 3, 2) if i % 2 == 0 else (0, 3, 2, 4, 2, 3))
        drone(b); BOD.bar(b, BOD_F if last else BOD_S)       # v8: 歌1 の頭で 4.6dB 下がっていた → 1番の頭から低い太鼓とベース
        # フィドルは行の終わり（偶数の小節の後ろ半分）で答える。2番はアコーディオンも交代で
        if i % 4 == 3 and i < 15:
            tn = tones(root(b), "D5", "D6"); (FID if (n == "歌1" or i % 8 == 3) else ACC).bar(b, f"R:3 {nm(tn[1])}:1 {nm(tn[2])}:1 {nm(tn[1])}:1")
    elif n == "歌3":                                                      # ハープと声だけ（後半に弦がそっと）
        harp(b, (0, 2, 3, 4, 3, 2)); HARP2.bar(b, f"R:3 {nm(tones(root(b), 'D5', 'D6')[1])}:3") if i % 2 == 1 else None
        if i >= 8: strs(b, 66)
        if i >= 14: BOD.bar(b, BOD_S if i == 14 else BOD_F)
    elif n.startswith("くり返し"):
        big = n == "くり返し4"; semi = 2 if big else 0
        harp(b, (0, 2, 3, 4, 3, 2) if i % 2 == 0 else (0, 3, 2, 4, 2, 3)); drone(b, 64 if big else 62)
        BOD.bar(b, BOD_F if (i % 8 == 7 and not (big and last)) else (BOD_A if i % 2 == 0 else BOD_B))
        if n != "くり返し1" or i >= 8: strs(b, 71 if big else 69)
        # フィドル: 歌が休む所（返事のあと・8小節目・16小節目）で答える。最後はずっと上で歌う
        if i in (7, 15): FID.bar(b, tr_line(TUNE_A[6] if i == 7 else TUNE_A[7], semi)); ACC.bar(b, tr_line(TUNE_A[6] if i == 7 else TUNE_A[7], semi)) if n != "くり返し1" else None
        elif big or n == "くり返し3":
            v = sorted(voice(root(b), 76, 3)); FID.bar(b, f"{nm(v[1])}:3 {nm(v[2])}:3" if i % 2 == 0 else f"{nm(v[2])}:6")
        elif i in (1, 3, 9, 11):
            tn = tones(root(b), "D5", "D6"); FID.bar(b, f"R:4 {nm(tn[2])}:1 {nm(tn[1])}:1")
    elif n == "おわり":
        if i < 8:
            ln = tr_line(TUNE_A[i], 2); FID.bar(b, ln); ACC.bar(b, ln); harp(b); drone(b, 64); strs(b, 71); BOD.bar(b, BOD_F if i == 7 else (BOD_A if i % 2 == 0 else BOD_B))
        elif i == 8:
            harp(b, (0, 1, 2, 3, 4, 5), "E3", "E6"); drone(b, 64); strs(b, 71); BOD.bar(b, f"{LOB}:6"); FID.bar(b, "E5:6"); PIN.bar(b, "R:3 E7:0.5 B7:2.5")     # 洗濯ばさみの「パチン」
        else: drone(b, 64); strs(b, 71)

# ================= ベース（付点4分の根音。共通の部品 bass_line は使わない）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    ap = t5 if rn == r else (rn - 2 if rn > r else rn + 2)
    two = f"{nm(r)}:3 {nm(t5)}:2 {nm(r)}:1"; lilt = f"{nm(r)}:2 {nm(r)}:1 {nm(t5)}:2 {nm(ap)}:1"; run = f"{nm(r)}:2 {nm(t3)}:1 {nm(t5)}:1 {nm(t3)}:1 {nm(ap)}:1"; long_ = f"{nm(r)}:4 {nm(t5)}:2"
    if n == "ジグ1" and i >= 8: BASS.bar(b, two)
    elif n == "ジグ2": BASS.bar(b, lilt if i % 4 == 3 else two)
    elif n == "ジグ3": BASS.bar(b, run if i % 4 == 3 else (lilt if i % 2 == 0 else two))
    elif n == "歌1": BASS.bar(b, long_)
    elif n == "歌2": BASS.bar(b, two if i % 4 != 3 else lilt)
    elif n == "歌3" and i >= 8: BASS.bar(b, long_)
    elif n.startswith("くり返し"): BASS.bar(b, run if i % 8 == 7 else (lilt if (i % 2 == 0 and n != "くり返し1") else two))
    elif n == "おわり": BASS.bar(b, (lilt if i % 2 == 0 else two) if i < 8 else long_) if i < 9 else None

# ================= ドラム（主役にしない。低い太鼓が運ぶ。くり返しとジグ3 だけ、キックと軽いスネア）=================
def g6(s): return s.replace(" ", "")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ジグ3" or n in ("くり返し2", "くり返し3", "くり返し4") or (n == "くり返し1" and i >= 8) or (n == "おわり" and i < 8):
        D.set(b, g6("X... .... .... X... .... ....") if i % 2 == 0 else g6("X... .... .... X... .... x..."), "." * 24, "." * 24)       # v6: ハイハットはなし（低い太鼓が刻む）
        if i % 8 == 0: crash(D, b, "C2", 6)
    elif n == "おわり" and i == 8: D.set(b, g6("X... .... .... .... .... ...."), "." * 24, "." * 24); crash(D, b, "C2", 6)

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。ケルトのジグ（8分の6）。D→E。晴れた日のベランダで洗濯物を干していると、からだが勝手にゆれ出す。"
          "歌（3番まで）と、みんなで歌う「まあいいか」のくり返しと、フィドルのジグが交互に進む。フィドル・アコーディオン・ハープ・低い太鼓。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"歌3": -0.4, "くり返し4": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ハープ", mid=82, down=10, up=8, seed=3); humanize(path, "フィドル", mid=86, down=8, up=8, seed=5); humanize(path, "アコーディオン（節", mid=86, down=8, up=8, seed=7); humanize(path, "低い太鼓", mid=88, down=10, up=10, seed=9)
# v5 を測ると、ハープ −32・ジグ1 −25・歌1 −22（くり返し −14〜−16）で、前半が小さすぎた。場面ごとの採点は 歌2 が 6.91（低い太鼓が細かく鳴りっぱなし）。
#   → フィドルとハープを大きく、低い太鼓は小さく・歌の間は静かな型だけ、ハイハットはなし。前半3つの場面は同じ大きさで持ち上げる（途中で主役が小さくならないように）
scene_gain(path, S, {"ハープ": 1.6, "ジグ1": 1.6, "歌1": 1.6})
final_gain(path, {"歌1": -1.0, "くり返し1": 1.0, "くり返し4": 1.0})   # v8 を測ると 歌1（−14.7）が くり返し1（−15.2）より大きかった
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 8, "chorus": 20, "くり返し4": 24, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=3.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("くり返し2", 8, None, K), ("くり返し3", 0, None, K), ("くり返し4", 0, None, KE)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.3
    save(path, js)
