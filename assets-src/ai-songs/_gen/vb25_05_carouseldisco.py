# vb25 05「回転木馬ディスコティック」Carousel Discotheque（仮）— ダンス（ディスコ・生のバンド）。D ドリアン（サビは F長調）・124・4/4。
#   閉園のアナウンスの間だけ 93。最後のサビは +1（F#長調）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（前は木馬たちが踊る話）、歌を人が歌える旋律（付点で跳ねる8分と4分）に、テトの歌の版を足した。
# 物語: 遊園地のメリーゴーランド係のアルバイト、最後の夜。閉園して明かりが落ちると、仲間がこっそり手招きする。ミラーボールの代わりの月の下で、
#   止まった木馬のまわりをみんなで踊る。明日からはばらばらの道。本当はこの店も、みんなも好きだったと言えないまま、夜明けまで回り続ける。
# 場面と強さ: 閉園（4つ打ちのキックだけ → カリオペ）→ 最後のシフト（Aメロ・語る）→ 明日から（Bメロ・溜め → キメの止め）
#   → まわれまわれ（サビ1）→ ミラーボールの月（間奏・ブラス）→ 夜の庭（2番。BGM はブラスが歌を受け取る）→ Bメロ2（キメ）→ サビ2
#   → 閉園のアナウンス（テンポ ×0.75・ストリングスが歌い、後半は歌が静かに）→ 夜明けまで（こもった音 → 1拍の完全な無音）
#   → 最後のサビ（+1・いちばん大きい）→ 木馬が止まる（カリオペ）
# 旋律の性格: 付点（0.75＋0.25）で跳ねる中音域（C#4〜F#5）。サビは「まわれまわれよ」の同じ音を3つずつ置くフック。
# ほかの曲とちがう所: 生のスラップベース・ブラス・カッティングのギター・オルガン・ストリングスのディスコ。テンポが途中で遅くなる。
from vb25_lib import *

S = Song("05", "carouseldisco", "回転木馬ディスコティック（仮）", "Carousel Discotheque", 124, 4, "D", "dorian", "ダンス（ディスコ・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key                    # D ドリアン（Aメロ）
KDm = Key("D", "minor")      # 間奏の旋律（B♭ を含む）
KF = Key("F", "major")       # サビ（平行調）
KG = Key("F#", "major")      # 最後のサビ（+1）


def chk(*lists):
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


A_CH = ["Dm7", "G7", "Dm7", "G7", "Bbmaj7", "A7", "Dm7", "Dm7"]
B_CH = ["Gm7", "C7", "Fmaj7", "Dm7", "Gm7", "C7", "Bbmaj7", "A7"]
C_CH = ["Bbmaj7", "C7", "Am7", "Dm7", "Gm7", "C7", "Fmaj7", "D7",
        "Gm7", "A7", "Dm7", "Dm7/C", "Bbmaj7", "Bbm6", "Am7", "A7"]             # D7＝ii（Gm）への副属和音、Bbm6＝同主短調から借りた iv
ANN = ["Dm9", "Gm9", "Cmaj7", "Fmaj7", "Bbmaj7", "Em7b5", "A7sus4", "A7"]
DAWN = ["Gm7", "A7", "Dm7", "Dm7/C", "Bbmaj7", "C7", "Bbmaj7", "C#7"]            # C#7＝次の調（F#長調）の V

S.scene("閉園", 8, "intro", ["Dm7", "Dm7", "Dm7", "Dm7", "Dm7", "G7", "Dm7", "A7"])
S.scene("木馬が目を覚ます", 16, "verse", A_CH)
S.scene("たてがみを揺らして", 8, "pre", B_CH)
S.scene("回れ回れ", 16, "chorus", C_CH)
S.scene("ミラーボールの月", 8, "interlude", A_CH)
S.scene("2周目", 16, "verse", A_CH)
S.scene("たてがみを揺らして2", 8, "pre", B_CH)
S.scene("回れ回れ2", 16, "chorus", C_CH)
S.scene("閉園のアナウンス", 16, "bridge", ANN)
S.scene("夜明けまで", 8, "build", DAWN)
S.scene("全部の木馬", 24, "chorus", [tr_chord(c, 1) for c in C_CH + C_CH[:8]])
S.scene("木馬が止まる", 5, "outro", [tr_chord(c, 1) for c in ["Bbmaj7", "C7", "Fmaj7", "Fmaj7", "Fmaj7"]])
S.tempo = [{"bar": S.sc("閉園のアナウンス")[0] + 1, "bpm": 93}, {"bar": S.sc("夜明けまで")[0] + 1, "bpm": 124}]

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, patch="altoSax", low=True)
V.main.spec["fx"].insert(1, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.7})   # 2026-10-26 人間「０５もリードの歪ちょっと抑えよう」   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
SLAP = S.track("スラップベース", "slap", volume=0.2, pan=0.0, duck=0.15,
               fx=[{"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 2200, "high": 1.5}])
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=0.0, reverb=0.25, gainDb=2,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 1}]) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.09, pan=0.25, reverb=0.35, sustain=1.5) for i in range(4)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.07, pan=-0.25, reverb=0.2) for i in range(3)]
MUF = [S.track(f"こもったオルガン{i + 1}（夜明けまで）", "drawbarOrgan", volume=0.08, pan=-0.25, reverb=0.3,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}]) for i in range(3)]
GTR = [S.track(f"カッティングのギター{i + 1}", "guitar", **clean_gtr_spec(0.085, 0.4)) for i in range(2)]
for g_ in GTR: g_.spec["sustain"] = 0.4
CAL = S.track("回転木馬のカリオペ", "lead", patch="calliope", volume=0.1, pan=0.15, reverb=0.3, mono=True, breath=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "eq", "low": 0, "mid": 2, "midHz": 1200, "high": -2}, {"type": "eq", "low": 0, "mid": -2.5, "midHz": 3200, "high": 0},
                  {"type": "filter", "kind": "lowpass", "freq": 5500, "q": 0.7}])
CHIME = S.track("アナウンスのチャイム・きらめき", "glockenspiel", volume=0.08, pan=0.2, reverb=0.45, sustain=1.2)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（Aメロは D ドリアン oct=4＝D4、Bメロ・サビは F長調 oct=4＝F4） =================
VERSE = ["R:0.5 1:0.75 3:0.25 4:0.5 5:0.5 3:1 R:0.5", "4:0.75 3:0.25 1:2 R:1",
         "R:0.5 5:0.75 4:0.25 3:0.5 1:1 R:1", "2:2 R:2",
         "R:0.5 4:0.75 4:0.25 5:0.5 3:0.5 4:0.5 5:0.5 R:0.5", "5:1 #7,:1 R:2",
         "R:0.5 1:0.75 3:0.25 5:0.5 7:0.5 5:1 R:0.5", "4:0.75 3:0.25 1:2 R:1",
         "R:0.5 5:0.75 5:0.25 5:0.5 7:0.5 1':1 R:0.5", "7:0.75 6:0.25 5:2 R:1",
         "R:0.5 6:0.75 6:0.25 5:0.5 4:0.5 2:1 R:0.5", "4:0.75 6:0.25 5:2 R:1",
         "R:0.5 4:0.75 4:0.25 3:0.5 4:0.5 5:1 R:0.5", "5:1 #7,:2 R:1",
         "R:0.5 1':0.75 7:0.25 5:0.5 4:0.5 3:1 R:0.5", "1:2 R:2"]
V1 = "さいごのしふとが/おわるころ/めりーごーらんど/あかりがきえてく/なかまのひとりが/てまねきをしてる/ないしょだよねと/わらいながら"
V2 = "だれもいなくなる/よるのにわ/かいてんもくばが/ひかりはじめてく/みらーぼーるがね/つきのかわりにね/くるくるまわる/ぼくらのよる"
BM = ["R:0.5 2:0.75 2:0.25 4:0.5 5:0.5 6:1 R:0.5", "5:0.75 4:0.25 3:1 R:2",
      "R:0.5 3:0.75 3:0.25 5:0.5 6:0.5 1':1 R:0.5", "6:0.75 5:0.25 R:3",
      "R:0.5 4:0.75 4:0.25 6:0.5 1':0.5 1':1 R:0.5", "7:0.75 6:0.25 R:3",
      "R:0.5 4:0.5 6:0.5 1':0.5 1':2", "7:0.5 R:0.5 #5:0.5 R:2.5"]
P1 = "あしたからはもう/ばらばらになる/それでもいまは/おどろうよね"
P2 = "ほんとうはいつも/このみせがすき/みんながすきで/いえないまま"
CH = ["R:0.5 1':0.75 1':0.25 1':0.5 6:0.75 6:0.25 6:0.5 R:0.5", "5:2 R:2",
      "R:0.5 3:0.75 3:0.25 5:0.5 7:0.5 5:1 R:0.5", "5:1 6:2 R:1",
      "R:0.5 2:0.75 2:0.25 4:0.5 6:0.5 5:0.5 4:0.5 R:0.5", "3:1 5:1.5 R:1.5",
      "R:0.5 1:0.75 3:0.25 5:0.5 7:1 R:1", "#4:1 6:1.5 R:1.5",
      "R:0.5 1':0.75 1':0.25 1':0.5 6:0.75 6:0.25 6:0.5 R:0.5", "#5:2 R:2",
      "R:0.5 6:0.75 6:0.25 5:0.5 3:0.5 2:1 R:0.5", "3:1 6:1.5 R:1.5",
      "R:0.5 4:0.75 4:0.25 5:0.5 6:0.5 1':1 R:0.5", "b6:1 1':1.5 R:1.5",
      "R:0.5 7:0.75 6:0.25 5:0.5 3:2", "#5:2 R:2"]
C1 = "まわれまわれよ/かいてんもくば/こよいはさいごの/でぃすこのよる/まわれまわれよ/わすれないよう/ひかりのなかで/いつまでも"
C2 = "まわれまわれよ/えぷろんぬいで/いつものみんなと/わらいあうの/まわれまわれよ/あしたのことは/いまはわすれて/おどろうよ"
LASTX = ["R:0.5 1':0.75 1':0.25 1':0.5 6:0.75 6:0.25 6:0.5 R:0.5", "5:2 R:2",
         "R:0.5 3:0.75 3:0.25 5:0.5 7:0.5 5:1 R:0.5", "6:2 5:2",
         "R:0.5 2:0.75 4:0.25 6:0.5 1':0.5 6:1 R:0.5", "5:0.75 4:0.25 3:2 R:1",
         "1':1 7:1 6:1 5:1", "6:2 5:2"]
LASTV = "まわれまわれよ/このよるのこと/ありがとうみんな/またあおうね"
SM = ["5:2/ 3:1 1:1", "4:3/ 6:1", "7:2/ 5:1 2:1", "3:3/ R:1", "6:2/ 1':1 3':1", "4:2 6:1 1':1", "1':2/ 7:1 5:1", "#7:4~"]
VN = ["R:1 3:1 5:1 1':1", "7:3 6:1", "5:2 7:1 2':1", "5:3 R:1", "R:1 4:1 6:1 1':1", "6:2 4:2", "4:1 5:1 1':1 5:1", "#7:3 R:1"]
VNV = "それぞれのみちへと/わかれてゆくけれどね"
DW = ["R:0.5 2:0.5 4:0.5 6:0.5 1':1 6:1", "#5:0.75 7:0.25 6:0.5 #5:0.5 7:2", "R:0.5 6:0.5 1':0.5 6:0.5 5:1.5 3:0.5", "4:1 3:0.5 1:0.5 5:2",
      "4:1 6:1 1':1 3':1", "5:1 7:1 2':1 4':1", "6:1 1':1 3':1 4':1"]
DWV = "よあけまでもうすこし/このままでいさせて"
chk(VERSE, BM, CH, LASTX, SM, VN, DW)
LY = Lyrics(S)
def put(name, key, lines, text, low=True, rng=None):
    bars = S.sc(name)[rng] if rng else S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("木馬が目を覚ます", K, VERSE, V1)
if VOCAL: put("2周目", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("2周目")):
        if i < 8: BR[0].bar(b, K.mel(VERSE[i], oct=4))                 # BGM: 2番の前半は、ブラスが歌を受け取る
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("たてがみを揺らして", KF, BM, P1); put("たてがみを揺らして2", KF, BM, P2)
put("回れ回れ", KF, CH, C1); put("回れ回れ2", KF, CH, C2)
for i, b in enumerate(S.sc("閉園のアナウンス")[:8]): STR[3].bar(b, KDm.mel(SM[i], oct=4))
put("閉園のアナウンス", KDm, VN, VNV, low=False, rng=slice(8, 16))
put("夜明けまで", KF, DW[:4], DWV, rng=slice(0, 4))
for i, b in enumerate(S.sc("夜明けまで")[4:]):
    if i < 3: V.low.bar(b, KF.mel(DW[4 + i], oct=4))                  # こもった声（重ねのパートだけ・元の高さ）
    else: V.low.bar(b, KG.mel("5:1 7:1 2':1 R:1", oct=4))             # C#7（F#長調の V）
put("全部の木馬", KG, CH + LASTX, C1 + "/" + LASTV)


# ================= 回転木馬のカリオペ（イントロ・終わり） =================
CAR = ["1':0.75 3':0.25 5':0.5 3':0.5 1':1 5:1", "6:0.75 1':0.25 2':0.5 1':0.5 6:1 4:1", "1':0.75 3':0.25 5':0.5 6':0.5 5':1 3':1", "#7:1 2':1 4':1 #7:1"]
chk(CAR)
for i, b in enumerate(S.sc("閉園")):
    if i >= 4: CAL.bar(b, KDm.mel(CAR[i - 4], oct=4))
for i, b in enumerate(S.sc("木馬が止まる")):
    CAL.bar(b, KG.mel(["5:1.5 4:0.5 3:1 1:1", "2:1.5 3:0.5 4:1 5:1", "1':2 7:1 5:1", "3:4", "R:4", "R:4"][i], oct=4))

# ================= ブラス（合いの手・間奏の主旋律） =================
MIR = ["5':0.5 R:0.25 5':0.25 4':0.5 3':0.5 1':1 R:1", "4':0.5 R:0.25 4':0.25 3':0.5 2':0.5 6:1 R:1",
       "3':0.5 R:0.25 3':0.25 4':0.5 5':0.5 6':0.75 5':0.25 3':0.5 1':0.5", "#5:0.5 7:0.5 2':0.5 3':0.5 #5':1 R:1"]
chk(MIR)
for i, b in enumerate(S.sc("ミラーボールの月")): BR[0].bar(b, KF.mel(MIR[i % 4], oct=3) if i < 7 else KF.mel("3':1 2':1 #5:1 3':1", oct=3))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 62, 3)
    stab = None
    if n in ("回れ回れ", "回れ回れ2", "全部の木馬") and i % 2 == 1: stab = "R:3.5 X:0.5"           # 4拍目の裏から次の頭へ「パッ」
    if n in ("回れ回れ", "回れ回れ2", "全部の木馬") and i % 4 == 0: stab = "X:0.5! R:3.5"
    if n.startswith("たてがみ") and i == 7: stab = "X:0.5! R:0.5 X:0.5! R:2.5"               # キメ
    if n == "木馬が目を覚ます" and i % 4 == 3: stab = "R:2.5 X:0.25 X:0.25 X:0.5' R:0.5"
    if stab:
        for j in range(3):
            if n == "2周目" and j == 0: continue
            BR[j].bar(b, stab.replace("X", nm(v[j])))
# 間奏の後ろ2本（ハモり）
for i, b in enumerate(S.sc("ミラーボールの月")):
    v = voice(S.chords[b], 57, 3)
    for j in (1, 2): BR[j].bar(b, f"{nm(v[j - 1])}:2 {nm(v[j - 1])}:2")

# ================= 伴奏 =================
def slap_line(b, style):
    """スラップベースの音域（E1〜G3）に収まらない型は、8分の根音にする"""
    s_ = bass_line(S, b, style)
    if any(midi(x.split(":")[0]) > midi("G3") for x in s_.split() if not x.startswith("R")): s_ = bass_line(S, b, "root8")
    return s_


def cut16(b, ch):
    """カッティング: 16分の刻み（弾く音＝和音の2音、消す音＝休み）"""
    v = voice(ch, 64, 2)
    pat = "x.xx.x.x.xx.x.xx" if b % 2 else ".x.xx.x..x.xx.x."
    for j in range(2):
        GTR[j].bar(b, " ".join((f"{nm(v[j])}:0.25" + ("," if c == "x" else "") if c != "." else "R:0.25") for c in pat))

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    chorus = n in ("回れ回れ", "回れ回れ2", "全部の木馬")
    verse = n in ("木馬が目を覚ます", "2周目")
    # スラップベース
    if n == "閉園": SLAP.bar(b, slap_line(b, "disco")) if i >= 4 else None
    elif verse: SLAP.bar(b, slap_line(b, "disco" if i % 2 == 0 else "oct8"))
    elif n.startswith("たてがみ"): SLAP.bar(b, slap_line(b, "push") if i < 7 else f"{nm(low(ch, 'E1'))}:0.5! R:0.5 {nm(low(ch, 'E1'))}:0.5! R:2.5")
    elif chorus or n == "ミラーボールの月": SLAP.bar(b, slap_line(b, "disco"))
    elif n == "閉園のアナウンス": SLAP.bar(b, f"{nm(low(ch, 'E1'))}:2 {nm(low(ch, 'E1') + 7)}:2" if i >= 4 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "夜明けまで": SLAP.bar(b, slap_line(b, "oct8") if i < 4 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "木馬が止まる" and i < 4: SLAP.bar(b, slap_line(b, "half"))
    # オルガン: Aメロは裏の刻み、アナウンスでは伸ばし
    if verse or n == "閉園" and i >= 4:
        for j in range(3): ORG[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    elif n == "閉園のアナウンス" or n == "木馬が止まる":
        for j in range(3): ORG[j].bar(b, f"{nm(v[j])}:4")
    elif chorus:
        for j in range(3): ORG[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:2.5")
    elif n == "夜明けまで" and i >= 4:
        for j in range(3): MUF[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    # ストリングス: サビと Bメロで伸ばし、サビの頭で「しゃくり」上げる
    if chorus or n.startswith("たてがみ") and i < 7 or n == "閉園のアナウンス":
        vs = voice(ch, 69, 3)
        for j in range(3): STR[j].bar(b, f"{nm(vs[j])}:4" + ("/" if (chorus and i % 4 == 0) else ""))
    # カッティング
    if (verse and i >= 8) or chorus or n == "ミラーボールの月":
        cut16(b, ch)
# ストリングスの「しゃくり」の合いの手（サビの4小節目ごとに、下から駆け上がる）
for name, kk in (("回れ回れ", KF), ("回れ回れ2", KF), ("全部の木馬", KG)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: STR[3].bar(b, kk.mel("R:2 1':0.25 2':0.25 3':0.25 5':0.25 6':1/", oct=3))

# アナウンスのチャイム（4つの音）ときらめき
CHIME.bar(S.sc("閉園のアナウンス")[0], KDm.mel("5':1 3':1 1':1 5:1", oct=4))
CHIME.bar(S.sc("閉園のアナウンス")[8], KDm.mel("5:1 1':1 3':1 5':1", oct=4))
for i, b in enumerate(S.sc("全部の木馬")):
    if i % 8 == 6: CHIME.bar(b, KG.mel("R:2 5':0.5 3':0.5 1':1", oct=4))
riser(FX, S.sc("回れ回れ")[0], 4, "C4"); riser(FX, S.sc("回れ回れ2")[0], 4, "C4")
FX.bar(S.sc("閉園のアナウンス")[0], "E4:4")                              # ダウンリフター（テンポが落ちる）
riser(FX, S.sc("全部の木馬")[0] - 0.25, 8, "D4")
cym_swell(CYM, S.sc("ミラーボールの月")[0], 2, "C4"); cym_swell(CYM, S.sc("2周目")[0], 2, "E4")

# ================= ドラム（電子のドラム・ディスコ） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "閉園":
        if i < 4: D.set(b, "X...X...X...X...", "." * 16, "." * 16)               # 4つ打ちのキックだけ
        else: vgroove(D, b, "disco", seed=b, s="............X...")
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("木馬が目を覚ます", "2周目"):
        vgroove(D, b, "disco" if i < 8 else "four16", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if n == "2周目" and i < 8: D.cym(b, ("F2:0.5 " if i % 4 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("たてがみ"):
        vgroove(D, b, "half" if i < 4 else "disco", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16); crash(D, b, "G2", 4)   # キメ（全員の止め）
    elif n == "回れ回れ":
        vgroove(D, b, "disco", seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "tomdown")
    elif n == "回れ回れ2":
        vgroove(D, b, "twostep" if i < 8 else "four16", ghosts=0.3, seed=b)   # 2回目は2ステップから入れかえ
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if not last else "build")
    elif n == "ミラーボールの月":
        vgroove(D, b, "disco", seed=b)
        D.cym(b, ("C2:0.5 " if i == 0 else "F2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if last: put_fill(D, b, "tomtrip")
    elif n == "閉園のアナウンス":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if i == 4: crash(D, b, "C2", 8)
        if last: put_fill(D, b, "build")
    elif n == "夜明けまで":
        if i < 4: vgroove(D, b, "four16", seed=b)
        else: D.set(b, "X...X...X...X...", "." * 16, "." * 16)
        if i == 0: crash(D, b, "G2")
        if last: D.set(b, "X...X...X.X.X...", "....X...XXX.....", "." * 16)
    elif n == "全部の木馬":
        vgroove(D, b, "disco" if i < 16 else "four16", seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last: put_fill(D, b, "tomdown")
    elif n == "木馬が止まる":
        if i < 2: vgroove(D, b, "disco", seed=b)
        elif i < 4: D.set(b, "X...X...X...X...", "." * 16, "..x...x...x...x.")
        if i == 0: crash(D, b, "C2", 8)

SIL.add(S.sc("たてがみを揺らして")[-1], 2, 4)      # キメの止め（1回目）
SIL.add(S.sc("たてがみを揺らして2")[-1], 2, 4)     # キメの止め（2回目）
SIL.add(S.sc("夜明けまで")[-1], 3, 4)              # 最後のサビの前の1拍は、完全な無音
SIL.apply()

S.fade_out = 12
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の05。ダンス（ディスコ・生のバンド）。D ドリアン（サビは F）・124、閉園のアナウンスの間だけ 93。最後のサビは +1（F#）。"
          "遊園地のアルバイト最後の夜、閉園後に仲間と踊る別れの歌。キックとカリオペで始まり、付点で跳ねる Aメロ、キメの止め、「まわれまわれよ」のサビ、ブラスの間奏、"
          "テンポが遅くなるアナウンスの場面、こもった夜明け前と1拍の無音、+1 の最後のサビ、カリオペで木馬が止まる。スラップベース・ブラス・ギター・オルガン・ストリングス。自作")
S.no_depth = True
S.flags += " --space hall --space-wet 0.16"
teto(S, LY, V, special={"全部の木馬": 0.55, "閉園のアナウンス": -0.5, "夜明けまで": 0.05})
