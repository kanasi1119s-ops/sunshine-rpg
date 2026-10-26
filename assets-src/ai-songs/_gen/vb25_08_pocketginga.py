# vb25 08「からっぽのポケットに銀河」Galaxy in an Empty Pocket（仮）— ロック（疾走ギターロック・生のバンド）。D長調・172・4/4（Bメロは 6/8 に聞こえる3連）。転調なし
# 2026-10-25 作り直し: 物語を人の気持ちの話に（夏休みを何もせずに終えた後悔と、となりの友だち）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を G長調から 5半音下げて D長調にした（書くのは G長調の度数のまま、書き出しの前に下げる）。虫の声はゲームっぽいパルス波をやめて録音の鈴虫に。
# 物語: 夏休みの最後の夜。何もしないまま夏が終わる。財布もからっぽ、宿題も残っている。空き地の草に寝ころんで、となりの君と星を数えていたら、
#   からっぽのポケットに星が降ってくるみたいだった。何もない夏でも、君と並んでいたことが光っている。流れ星に「この夏を忘れないで」と願う。
# 場面と強さ: 空き地（ギターのコード1つ・虫の声）→ 自転車で（前奏）→ 星を数える（Aメロ）→ 夜風（Bメロ 6/8）→ 銀河（サビ）→ 寄り道（間奏）
#   → 2番（BGM はリードギターが歌を受け取る）→ 夜風2 → 銀河2 → 花火の燃えかす（Cメロ・虫の声 → Half feel）→ ギターソロ
#   → 流れ星を待つ（こもった音）→ 1拍の完全な無音 → 流れ星（最後のサビ）→ 帰り道 → 虫の声と1音
# 旋律の性格: Aメロは8分で数えるように語る。Bメロは3連で揺れる。サビは同じ音を3つ置いてから高く跳んで長くのばす。最高音 F#5。
# ほかの曲とちがう所: 左右に分かれた生のギター2本とアコギ、6/8 に揺れる Bメロ、虫の声。
from vb25_lib import *

S = Song("08", "pocketginga", "からっぽのポケットに銀河（仮）", "Galaxy in an Empty Pocket", 172, 4, "G", "major", "疾走ギターロック（ボカロ）")
S.kit = "crocell-punch-heavy"   # 2026-10-26 人間「トリガーの音がバスドラの重さを掻き消しちゃってる。トリガー無くさなくていい」
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
S.extra.update({"tone": "rock"})
K = S.key

RIFF_CH = ["Gadd9", "D/F#", "Em7", "Cadd9"]
A_CH = ["G", "D/F#", "Em7", "Cadd9", "Am7", "G/B", "C", "D"]
B_CH = ["Cmaj7", "D", "Bm7", "Em7", "Am7", "B7", "Cmaj7", "D"]          # B7＝vi への副属和音（定番以外）
C_CH = ["C", "D", "Bm7", "Em", "C", "D", "G", "G/B"]
C_CH2 = ["C", "D", "B7", "Em7", "Am7", "D7", "G", "G"]                   # B7（副属和音）
EMBER = ["Em7", "Cmaj7", "G/B", "Am7", "Em7", "Cmaj7", "Am7", "D7sus4",
         "C", "B7/D#", "Em7", "Em7/D", "Cmaj7", "G/B", "Am7", "D"]
WAIT = ["Cmaj7", "D", "Bm7", "Em7", "Am7", "Bm7", "Cmaj7", "D7sus4"]
STAR3 = ["Am7", "D/F#", "G/B", "C", "Cm6", "G/D", "D7sus4", "G"]         # Cm6＝同主調から借りた iv
OUT = ["Gadd9", "D/F#", "Em7", "Cadd9"]

S.scene("空き地", 2, "intro", ["Gadd9", "Gadd9"])
S.scene("自転車で", 8, "intro", RIFF_CH)
S.scene("星を数える", 16, "verse", A_CH)
S.scene("夜風", 8, "pre", B_CH)
S.scene("銀河", 16, "chorus", C_CH + C_CH2)
S.scene("寄り道", 8, "interlude", RIFF_CH)
S.scene("星を数える2", 16, "verse", A_CH)
S.scene("夜風2", 8, "pre", B_CH)
S.scene("銀河2", 16, "chorus", C_CH + C_CH2)
S.scene("花火の燃えかす", 16, "bridge", EMBER)
S.scene("ギターソロ", 16, "solo", RIFF_CH)
S.scene("流れ星を待つ", 8, "build", WAIT)
S.scene("流れ星", 24, "chorus", C_CH + C_CH2 + STAR3)
S.scene("帰り道", 12, "outro", OUT)
S.scene("虫の声と1音", 4, "outro", ["Gadd9"] * 4)

V = Voice(S, vol=0.22, delay=0.75, patch="flute", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
NY = [S.track(f"アコギ（ナイロン弦）{i + 1}", "guitar", patch="nylonGuitar", volume=0.12, pan=0.35, amp="clean", chorus=0, reverb=0.25,
              humanPitch=0, sustain=1.6, fx=[{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": 0, "mid": -2, "midHz": 3200, "high": -2}])
      for i in range(4)]
GL = [S.track(f"ギター左（{['根音', '5度'][i]}）", "distGuitar", **rock_gtr_spec(0.085, -0.6, drive=0.26)) for i in range(2)]
GR = [S.track(f"ギター右（{['根音', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.085, 0.6, drive=0.26)) for i in range(2)]
# 2026-10-26 人間「08のギターの高い方の音少し、ほんの少し優しくてもいいかも」: 歪みギターの 3.5〜8kHz を少しだけ丸める（下の SOFT を各ギターの fx の最後に足す）
SOFT = [{"type": "eq", "low": 0, "mid": -2, "midHz": 4200, "high": -2.5}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.7}]
LG2 = S.track("リフのギター（サビの下で回る・小さめ）", "distGuitar", **{**lead_gtr_spec(0.085, 0.3), "ampDrive": 0.6})
LG = S.track("リードギター（リフ・ソロ・歌の受け渡し）", "distGuitar", **{**lead_gtr_spec(0.14, -0.08), "ampDrive": 0.75})   # 2026-10-26 人間「08のギターの音少しだけ歪み抑えよう」: バッキング 0.35→0.26、リード 1.0→0.75
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.21))
GLK = S.track("グロッケン（星）", "glockenspiel", volume=0.1, pan=0.3, reverb=0.45, sustain=1.6)
STR = [S.track(f"ストリングス{i + 1}", "strings", **strings_spec(0.085, -0.3)) for i in range(3)]
# 虫の声: 高いパルス波を細かく震わせる（トレモロ 15Hz）
BUG = S.track("虫の声（録音の鈴虫）", "pad", patch="seasonFx", volume=0.08, pan=0.5, reverb=0.3, modulate=False)
CHIRP = "D4:4"
CHIRP2 = "D4:4"
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
# 流れ星を待つ: こもった音（ローパス 800Hz の写しに入れかえる）
LPF = {"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.8}
GM = [S.track(f"こもったギター{i + 1}", "distGuitar", **{**rock_gtr_spec(0.085, 0.0, drive=0.26), "fx": rock_gtr_spec()["fx"] + [LPF]}) for i in range(2)]
STM = [S.track(f"こもったストリングス{i + 1}", "strings", **{**strings_spec(0.09, 0.3), "fx": [LPF]}) for i in range(3)]
D = S.drumkit()
for _t in GL + GR + GM + [LG, LG2]: _t.spec["fx"] = list(_t.spec.get("fx", [])) + SOFT
SIL = Silence(S)

# ================= 歌の旋律と歌詞（G長調の度数。oct=4 で 1 = G4。書き出しの前に全体を 5半音下げる） =================
VERSE = ["R:1 3:0.5 3:0.5 2:0.5 1:0.5 2:1", "3:1 2:1.5 R:1.5",
         "R:1 3:0.5 5:0.5 5:0.5 6:0.5 5:1", "3:2 R:2",
         "R:1 1:0.5 1:0.5 2:0.5 3:0.5 4:1", "3:1 2:1.5 R:1.5",
         "R:1 3:0.5 4:0.5 5:0.5 6:0.5 5:1", "7,:1 5,:1.5 R:1.5",
         "R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "2:1 7,:1.5 R:1.5",
         "R:1 5:0.5 6:0.5 1':0.5 7:0.5 6:1", "5:2 R:2",
         "R:1 6:0.5 6:0.5 5:0.5 3:0.5 1:1", "2:1 3:1.5 R:1.5",
         "R:1 1:0.5 2:0.5 3:0.5 4:0.5 5:1", "5:2 R:2"]
V1 = "なつやすみのね/さいごのよる/さいふのなかは/かぜのすみかで/あきちのくさに/ねころんだら/ほしをかぞえる/いちにいさん"
V2 = "まっしろなままで/なつがおわる/しゅくだいもまだ/おわらないまま/となりのきみが/わらいだした/ほしのかずなら/まけないよと"
BM = ["3:0.6667 4:0.3333 5:1 5:0.6667 6:0.3333 5:1", "6:0.6667 5:0.3333 #4:1 5:1 R:1",
      "7:1 6:0.6667 5:0.3333 3:1 5:0.6667 6:0.3333", "7:2 R:2",
      "2':0.6667 1':0.3333 7:1 1':0.6667 7:0.3333 6:1", "#5:0.6667 6:0.3333 7:1 2':1 R:1",
      "1':1 3':1 2':0.6667 1':0.3333 7:0.6667 6:0.3333", "5:1 7:1 R:2"]
P1 = "よかぜがつめたくなる/なつのおわりね/ぬけがらのひびがまた/ひとつおちてゆく"
P2 = "ほしをかぞえていたら/ほしがふってくる/ほしこづかいあふれて/ぎんがみたいだね"
CH1 = ["R:0.5 5:0.5 5:0.5 5:0.5 1':2", "7:0.5 1':0.5 2':1 7:1 5:1", "R:0.5 5:0.5 5:0.5 5:0.5 3':2", "2':1 1':0.5 7:0.5 1':2",
       "R:0.5 3':0.5 3':0.5 3':0.5 2':1 3':1", "2':0.5 3':0.5 2':1 7:1.5 R:0.5", "5:1 1':1 2':1 3':1", "2':3 R:1"]
CH1b = ["R:0.5 5:0.5 5:0.5 5:0.5 1':2", "7:0.5 1':0.5 2':1 3':1 2':1", "R:0.5 #5:0.5 #5:0.5 #5:0.5 3':2", "2':1 1':1 7:1 5:1",
        "R:0.5 5:0.5 1':0.5 2':0.5 3':2", "3':1 2':1 1':1.5 R:0.5", "3':2 1':1 5:1", "1':4"]
CH2 = CH1[:6] + ["5:1 6:1 1':1 2':1", "3':2 2':1 1':1"]
CH2b = CH1b[:6] + ["3':1 2':0.5 1':0.5 2':2", "1':2 R:2"]
CHL_b = CH1b[:4] + ["R:0.5 5:0.5 1':0.5 2':0.5 3':2", "3':1 2':1 1':1.5 R:0.5", "3':2 2':1 1':1", "1':3 R:1"]
CHL_c = ["R:0.5 3':0.5 3':0.5 3':0.5 2':1 1':1", "7:0.5 1':0.5 2':1 5:2", "R:0.5 5:0.5 1':0.5 2':0.5 3':2", "3':2 2':1 R:1",
         "2':2 1':1 b6:1", "5:1 7:1 1':2", "2':4", "1':4"]
C1 = "からっぽのぽけっとにね/ほしをつめこんで/なにもないなつだって/かがやくよ/きみとならんでいた/それがたからもの/ほしのまんなか/ふたりで"
C2 = "からっぽのぽけっとにね/ほしがふってくるよ/なつのおわりのよる/ぎんがになったよ/きみとならんでいた/それがたからもの/ほしのまんなか/ほしのなか"
CL = "からっぽのぽけっとにね/ほしをつめこんで/なにもないなつだって/かがやくよ/きみとならんでいた/それがたからもの/ながれぼしがね/きらめく/ねがいごとはひとつ/このなつをね/わすれないでいて"
EM = ["3:2 2:1 1:1", "5,:3 R:1", "1:1 2:1 3:1 5:1", "4:3 R:1",
      "5:2 6:1 5:1", "#5:3 R:1", "3:1 5:1 1':2", "7:3 R:1", "1':2 7:1 6:1", "5:2 3:1 R:1", "6:1 1':1 2':1 3':1", "3':2 2':2"]
EMV = "もえかす/てのひらに/あつかった/なつのひ/ほんとうは/いいたかったよ"
WT = ["3:2 5:2", "6:2 5:1 #4:1", "5:2 3:1 R:1", "5:1 6:1 7:1 1':1", "1':2 7:1 6:1", "7:2 5:1 R:1", "1':1 2':1 3':1 2':1", "2':3 R:1"]
WTV = "ながれぼしまつ/そらのしたでいのる/あとすこし"
OUTL = ["5:2 3:2", "2:3 R:1", "3:2 5:1 6:1", "5:3 R:1", "1':2 7:1 5:1", "6:3 R:1", "5:1 3:1 2:1 7,:1", "1:4"]
OUTV = "またね/あしたも/あえるよ/ほしのした"
LY = Lyrics(S)
def put(name, lines, text, low=True, rng=None):
    bars = S.sc(name)[rng] if rng else S.sc(name); mel = [K.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("星を数える", VERSE, V1)
if VOCAL: put("星を数える2", VERSE, V2)
else:
    for i, b in enumerate(S.sc("星を数える2")):
        if i < 8: LG.bar(b, K.mel(VERSE[i], oct=4))              # BGM: 2番の前半は、リードギターが歌を受け取る
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("夜風", BM, P1); put("夜風2", BM, P2)
put("銀河", CH1 + CH1b, C1); put("銀河2", CH2 + CH2b, C2)
put("流れ星", CH1 + CHL_b + CHL_c, CL)
put("花火の燃えかす", EM[:4], "/".join(EMV.split("/")[:2]), low=False, rng=slice(4, 8))
put("花火の燃えかす", EM[4:], "/".join(EMV.split("/")[2:]), rng=slice(8, 16))
bars = S.sc("流れ星を待つ"); mel = [K.mel(x, oct=4) for x in WT]
for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=(i >= 4))
LY.flow(bars, mel, WTV, "流れ星を待つ")
put("帰り道", OUTL, OUTV, rng=slice(0, 8))


# ================= リードギター（リフ・合いの手・ソロ） =================
RIFF = ["1':0.5 5:0.5 2':0.5 5:0.5 3':0.75 2':0.25 1':0.5 5:0.5", "7:0.5 5:0.5 2':0.5 5:0.5 3':0.75 2':0.25 7:1",
        "6:0.5 5:0.5 3':0.5 5:0.5 5':0.75 3':0.25 2':0.5 1':0.5", "4:0.5 5:0.5 6:0.5 1':0.5 2':1.5 R:0.5"]
for name in ("自転車で", "寄り道", "帰り道"):
    for i, b in enumerate(S.sc(name)):
        if name == "帰り道" and i >= 8: break
        if name == "帰り道" and i < 8 and i % 4 != 3: continue      # 帰り道はリフの終わりだけ
        LG.bar(b, K.mel(RIFF[i % 4] if not (name == "寄り道" and i >= 4) else seq_up(RIFF[i % 4], K, 2), oct=3))
SOLO = ["5:1 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "7:1.5 1':0.5 2':2", "3':0.5 5':0.5 3':0.5 2':0.5 1':1 7:1", "1':3 R:1",
        "5':0.5 4':0.5 3':0.5 5':0.5 1'':1 7':1", "6':1 5':1 #4':1 5':1", "3':0.25 4':0.25 5':0.25 6':0.25 7':0.5 6':0.5 5':1 3':1", "4':2 3':1 2':1",
        "1'':0.75 7':0.25 5':0.5 3':0.5 1'':0.75 7':0.25 5':1", "7':0.75 6':0.25 5':0.5 2':0.5 7':0.75 6':0.25 5':1",
        "5':0.75 3':0.25 2':0.5 7:0.5 5':0.75 3':0.25 2':1", "1':2 3':1 5':1",
        "5':0.5 6':0.25 5':0.25 6':0.5 1'':0.5 5':1 3':1", "2':1 3':1 5':1 6':1", "1'':2 7':1 5':1", "5':4"]
# 2026-10-26 人間（08）「2分55秒〜56秒のギターの音は聞きにくい」: ソロ13小節目の 32分の連打（トレモロ・1音 44ms）が機関銃のように
#   同じ音の頭を打ち直して聞きにくかった → 16分と8分の、歌えるフレーズ（5→6 の行き来から 1'' へ上がって下りる）に書きかえ
for i, b in enumerate(S.sc("ギターソロ")): LG.bar(b, K.mel(SOLO[i], oct=3))
# 2026-10-26 人間「ギターのリフも入れた方が08いいかも」: 前奏のリフの形（8分で上下して、3度で跳ねる）を和音に合わせて動かし、
#   サビの下（歌より低い G3〜E4 あたり）と、流れ星を待つ後半・帰り道で回す
def riff_on(ch, last=False):
    r = low(ch, "F#3"); third = 3 if ("m" in ch.split("/")[0].replace("maj", "")) else 4
    off = [0, -5, 2, -5, third, 2, 0, -5]
    ln = [0.5, 0.5, 0.5, 0.5, 0.75, 0.25, 0.5, 0.5]
    if last: return f"{nm(r)}:0.5 {nm(r - 5)}:0.5 {nm(r + 2)}:0.5 {nm(r - 5)}:0.5 {nm(r + third)}:2"
    return " ".join(f"{nm(r + o)}:{d}" for o, d in zip(off, ln))
for name in ("銀河", "銀河2", "流れ星"):
    for i, b in enumerate(S.sc(name)): LG2.bar(b, riff_on(S.chords[b], last=(i % 8 == 7)))
for i, b in enumerate(S.sc("流れ星を待つ")):
    if i >= 4: LG2.bar(b, riff_on(S.chords[b]))
for i, b in enumerate(S.sc("帰り道")):
    if i < 8 and i % 4 != 3: LG.bar(b, riff_on(S.chords[b]))
# 合いの手（Aメロの4小節ごと・サビの8小節ごと）
for name in ("星を数える", "星を数える2"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3 and not (name == "星を数える2" and i < 8): LG.bar(b, K.mel("R:2.5 5:0.25 6:0.25 1':0.5 2':0.5", oct=3))

# ================= グロッケン（星のきらめき） =================
for name in ("自転車で", "銀河", "銀河2", "流れ星", "寄り道"):
    for i, b in enumerate(S.sc(name)):
        if name in ("自転車で", "寄り道"):
            if i % 2 == 1: GLK.bar(b, K.mel("R:2 5:0.5 3:0.5 1':1", oct=5))
        elif i % 4 == 3: GLK.bar(b, K.mel("R:3 5:0.25 3:0.25 2:0.25 5:0.25", oct=5))
        elif i % 4 == 0 and name == "流れ星": GLK.bar(b, K.mel("1':2 5:2", oct=5))

# ================= 伴奏 =================
def strum(b, ch, pat, lo="G3", hi="G4"):
    """アコギのコード（4本に分けて少しずつずらす）。pat は長さの並び（! で強く）"""
    t = tones(ch, lo, hi)[:4]
    while len(t) < 4: t.append(t[-1] + 12)
    for j in range(4):
        NY[j].bar(b, " ".join(f"{nm(t[j])}:{x}" for x in pat.split()), off=0.025 * j)


def mbass(b, style):
    """歌うベース（E1〜D3）。r＝根音、c1・c2＝根音の上の和音の音、o＝オクターブ、a＝次の根音へ寄る音（半音か全音）"""
    ch = S.chords[b]; r = low(ch, "E1")
    nx = low(S.chords[b + 1], "E1") if b + 1 < S.nb else r
    if nx - r > 6: nx -= 12
    if r - nx > 6: nx += 12
    up = [t for t in tones(ch, nm(r + 1), nm(r + 12))]
    c1 = up[0] if up else r + 4; c2 = up[1] if len(up) > 1 else r + 7
    o = r + 12 if r + 12 <= 50 else r
    a = nx - 1 if nx > r else (nx + 1 if nx < r else nx + 2)
    w = nx - 2 if nx > r else nx + 2
    P_ = {"walk": [(r, 1, "!"), (c2, 0.5, ""), (o, 0.5, ""), (c1 + 12 if c1 + 12 <= 50 else c1, 1, ""), (w, 0.5, ""), (a, 0.5, "")],
          "climb": [(r, 0.5, "!"), (r, 0.5, ""), (c1, 0.5, ""), (c2, 0.5, ""), (o, 1, "!"), (c2, 0.5, ""), (a, 0.5, "")],
          "drive": [(r, 0.5, "!"), (r, 0.5, ""), (o, 0.5, ""), (r, 0.5, ""), (c2, 0.5, "!"), (o, 0.5, ""), (c1 + 12 if c1 + 12 <= 50 else c2, 0.5, ""), (a, 0.5, "")],
          "run": [(r, 0.5, "!"), (c1, 0.5, ""), (c2, 0.5, ""), (o, 0.5, ""), (c2 + 0, 0.5, ""), (c1, 0.5, ""), (w, 0.5, ""), (a, 0.5, "")],
          "ride": [(r, 1.5, "!"), (c2, 0.5, ""), (o, 1, ""), (a, 1, "")]}[style]
    fix = lambda m: m + 12 if m < 28 else (m - 12 if m > 50 else m)   # E1〜D3 に収める
    return " ".join(f"{nm(fix(m))}:{d}{acc}" for m, d, acc in P_)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    pw = power(ch, "E2")
    v = voice(ch, 62, 3)
    # アコギ
    if n == "空き地":
        if i == 0: strum(b, ch, "8", "D3", "D4")
    elif n in ("星を数える", "星を数える2"):
        tt = tones(ch, "G3", "D5")
        NY[0].bar(b, " ".join(f"{nm(tt[q % len(tt)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    elif n.startswith("夜風"):
        tt = tones(ch, "G3", "D5")
        NY[0].bar(b, " ".join(f"{nm(tt[q % len(tt)])}:0.3333" for q in (0, 1, 2, 3, 2, 1, 0, 2, 3, 4, 3, 2)))
    elif n == "花火の燃えかす" and i < 8:
        strum(b, ch, "4", "E3", "E4")
    elif n in ("銀河", "銀河2", "流れ星") and i % 2 == 0:
        strum(b, ch, "1.5 1 1.5")
    elif n == "帰り道": strum(b, ch, "2.5 1.5")
    elif n == "虫の声と1音" and i == 0: strum(b, ch, "8", "D3", "D4")
    # 歪みのギター（パワーコード）
    gpat = None
    if n in ("自転車で", "寄り道"): gpat = "X:1.5! X:1 X:1.5"
    elif n in ("星を数える", "星を数える2"):
        gpat = None if i < 4 else ("X:2! X:2" if i < 8 else "X:1.5! X:0.5 X:1 X:1")
    elif n.startswith("夜風"): gpat = "X:2! X:2" if i < 7 else "X:2! R:2"
    elif n in ("銀河", "銀河2", "流れ星"):
        gpat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8))
        if n == "銀河2" and i == L - 1: gpat = "X:2! R:2"
    elif n == "花火の燃えかす" and i >= 8: gpat = "X:4!" if i % 2 == 0 else "X:2! X:2"
    elif n == "ギターソロ": gpat = "X:1.5! X:1 X:1.5" if i % 4 != 3 else "X:0.5! X:0.5 X:0.5 X:0.5 X:2"
    elif n == "帰り道": gpat = "X:4!" if i < 8 else None
    if gpat:
        for j in range(2):
            GL[j].bar(b, gpat.replace("X", nm(pw[j])))
            GR[j].bar(b, gpat.replace("X", nm([pw[0], pw[2]][j])))
    if n == "流れ星を待つ":
        for j in range(2): GM[j].bar(b, ("X:2! X:2" if i < 6 else "X:1! X:1 X:1 X:1").replace("X", nm(pw[j])))
    # ストリングス
    if n.startswith("夜風") or n in ("銀河", "銀河2", "流れ星") or (n == "花火の燃えかす" and i >= 8) or (n == "帰り道" and i < 8):
        vv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(vv[j])}:4")
    if n == "流れ星を待つ":
        vv = voice(ch, 67, 3)
        for j in range(3): STM[j].bar(b, f"{nm(vv[j])}:4")
    # ベース（2026-10-26 人間「08はベースにメロディ入れようか」: 根音から和音の音をたどって、次の和音の根音へ半音・全音で寄っていく歌うベース）
    if n == "自転車で": BASS.bar(b, mbass(b, "ride") if i >= 4 else f"{nm(low(ch, 'E1'))}:4")
    elif n in ("星を数える", "星を数える2"): BASS.bar(b, mbass(b, "walk" if i < 8 else "climb"))
    elif n.startswith("夜風"):
        r = low(ch, "E1")
        BASS.bar(b, f"{nm(r)}:1 {nm(r)}:0.6667 {nm(r + 7)}:0.3333 {nm(r)}:1 {nm(r + 12)}:0.6667 {nm(r + 7)}:0.3333" if i < 7 else f"{nm(r)}:2 R:2")
    elif n in ("銀河", "銀河2", "流れ星"): BASS.bar(b, mbass(b, "drive" if i % 4 != 3 else "run"))
    elif n == "寄り道": BASS.bar(b, mbass(b, "run" if i % 2 else "ride"))
    elif n == "花火の燃えかす": BASS.bar(b, bass_line(S, b, "long") if i >= 4 and i < 8 else (bass_line(S, b, "half") if i >= 8 else "R:4"))
    elif n == "ギターソロ": BASS.bar(b, mbass(b, "drive" if i % 2 == 0 else "climb"))
    elif n == "流れ星を待つ": BASS.bar(b, bass_line(S, b, "long" if i < 6 else "root8"))
    elif n == "帰り道": BASS.bar(b, mbass(b, "walk") if i < 8 else (f"{nm(low(ch, 'E1'))}:4" if i == 8 else "R:4"))

# 虫の声（空き地・花火の燃えかすの頭・最後）
for b in S.sc("空き地"): BUG.bar(b, CHIRP)
for j, b in enumerate(S.sc("花火の燃えかす")[:6]): BUG.bar(b, CHIRP if j % 2 == 0 else CHIRP2)
for j, b in enumerate(S.sc("帰り道")[8:] + S.sc("虫の声と1音")): BUG.bar(b, CHIRP if j % 2 == 0 else CHIRP2)
GLK.bar(S.sc("虫の声と1音")[1], K.mel("5:4", oct=5))           # 最後の1音（星がひとつ）
# 効果音
riser(FX, S.sc("銀河")[0], 4, "C4"); riser(FX, S.sc("銀河2")[0], 4, "C4"); riser(FX, S.sc("流れ星")[0], 16, "D4")
cym_swell(CYM, S.sc("自転車で")[0], 2, "C4"); cym_swell(CYM, S.sc("ギターソロ")[0], 4, "E4")

# ================= ドラム =================
TRIP = {}   # 6/8 に聞こえる小節（3連のグリッド）: 小節 → (キック, スネア, ハイハット)


def ride8(b, first="C2"):
    D.cym(b, f"{first}:0.5 " + "D2:0.5 " * 7); D.H[b] = "." * 16


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "空き地":
        D.set(b, "." * 16, "." * 16, "." * 16)
        if i == 1: D.set(b, "." * 16, "........oxxxXXXX", "." * 16)
    elif n in ("自転車で", "寄り道"):
        vgroove(D, b, "beat8" if i % 4 != 3 else "vrock2", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if i == 4 and n == "寄り道": ride8(b, "C2")
        elif i > 4 and n == "寄り道": ride8(b, "D2")
        if last: put_fill(D, b, "tomdown")
    elif n in ("星を数える", "星を数える2"):
        if i < 4: vgroove(D, b, "beat8", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        if i >= 8 and n == "星を数える2": ride8(b, "C2" if i == 8 else "D2")
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "tomtrip")       # 次の 6/8 へ、3連のタムで入る
    elif n.startswith("夜風"):
        D.set(b, "." * 16, "." * 16, "." * 16)
        if i < 7:
            TRIP[b] = ("X....xX....x" if i % 2 == 0 else "X.....X..x..", "...X.o...X.o" if i < 6 else "...X.o..oXXX", (".oxOoxXoxOox" if i in (0, 4) else "XoxOoxXoxOox"))
            if i == 0: D.cym(b, "C2:4")
            if i == 4: D.cym(b, "G2:4")
        else:
            halt(D, b, 2); D.cym(b, "C2:2")          # 止め（後ろ2拍は全員休み）
    elif n in ("銀河", "銀河2", "流れ星"):
        vgroove(D, b, "vrock2" if not (n == "流れ星" and i >= 16) else "vrock", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if 8 <= i < 16 and n == "銀河2": ride8(b, "C2" if i == 8 else "D2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last and n == "銀河": put_fill(D, b, "tomdown")
        if last and n == "銀河2": halt(D, b, 2)
        if last and n == "流れ星": put_fill(D, b, "tomtrip")
    elif n == "花火の燃えかす":
        if i < 8: D.set(b, "." * 16, "." * 16, "." * 16)
        else:
            vgroove(D, b, "half", ghosts=0.45, seed=b, h="x...x...x...x...")
            if i < 15: D.cym(b, ("B2:1 " if i == 8 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if i == 7: D.set(b, "." * 16, "........oooxxxXX", "." * 16)
        if i == 15: put_fill(D, b, "lift")
    elif n == "ギターソロ":
        vgroove(D, b, "punk" if i < 8 else "vrock", ghosts=0.35, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "B2")
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "tomdown")
    elif n == "流れ星を待つ":
        D.set(b, "X.......X.......", "." * 16, "x.x.x.x.x.x.x.x." if i >= 4 else "." * 16)
        if i == 6: D.set(b, "X...X...X...X...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.")
        if i == 7: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)
    elif n == "帰り道":
        if i < 8: vgroove(D, b, "beat8", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b)
        if i == 7: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); D.cym(b, "C2:4")
        if i >= 8: D.set(b, "." * 16, "." * 16, "." * 16)

# 1拍の完全な無音（流れ星の直前）・止め
SIL.add(S.sc("流れ星を待つ")[-1], 3, 4)
SIL.add(S.sc("夜風")[-1], 2, 4); SIL.add(S.sc("夜風2")[-1], 2, 4); SIL.add(S.sc("銀河2")[-1], 2, 4)
SIL.apply()

# 6/8 の小節のドラム（3連のグリッドのパートを足す）
_tj = S.to_json


def _to_json():
    js = _tj()
    kk, ss, hh = [], [], []
    for b in range(S.nb):
        x = TRIP.get(b, ("." * 12,) * 3)
        kk.append(x[0]); ss.append(x[1]); hh.append(x[2])
    sp = lambda inst: {kk_: vv for kk_, vv in NAKED[inst].items() if kk_ != "human"}
    js["parts"] += [{"role": "キック（6/8）", "instrument": "kick", "notes": "t:" + "".join(kk), **sp("kick")},
                    {"role": "スネア（6/8）", "instrument": "snare", "notes": "t:" + "".join(ss), **sp("snare")},
                    {"role": "ハイハット（6/8）", "instrument": "hihat", "notes": "t:" + "".join(hh), **sp("hihat")}]
    return js


S.to_json = _to_json
S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の08。疾走ギターロック。D長調・172・転調なし。夏休みを何もせずに終えた最後の夜、となりの君と星を数える。"
          "ギターのコード1つと虫の声で始まり、8分で数える Aメロ、6/8 に揺れる Bメロ、高く跳んでのばすサビ、Half feel の Cメロ、ギターソロ、こもった待ち時間と1拍の無音、"
          "最後のサビ、虫の声と1音で終わる。左右のギター2本・アコギ・ベース・ドラム・グロッケン・ストリングス。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "鈴虫", S.beats * 8, vol=0.08)
season(S, S.nb - 8, "コオロギ", S.beats * 8, vol=0.08)
S.no_depth = True   # 2026-10-25: 深いパッドを足すと MIDI のチャンネルがあふれるので、空間だけ
S.flags += " --space hall --space-wet 0.15"
S.no_depth = True
teto(S, LY, V, transpose=-5, special={"流れ星": 0.55, "花火の燃えかす": -0.5, "流れ星を待つ": -0.2, "帰り道": -0.4})
