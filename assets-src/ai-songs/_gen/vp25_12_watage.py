# vp25 12「たんぽぽの綿毛飛行」A Dandelion Seed's Flight（仮）— ロック（6/8）。D長調（2周目は E長調）・付点4分＝84（8分＝252）・6/8。主役の楽器: バイオリン
# 物語: 春の終わり、たんぽぽの綿毛がひとつ、風に乗って飛び立つ。空の旅、突風、凪。遠くの野原に着地して、季節がめぐり、
#   次の春に花が咲く。そこからまた綿毛が飛び立つ（2周目は、前とちがう場所へ＝転調）。
# 形: 飛ぶ→着地→春に花→また飛ぶ（2周目は着地点が違う＝転調）
# 場面と強さ: 風の強さそのまま。突風で最大、凪で無音（4小節）。着地は小さく、春は少しずつ、2周目の飛行が山
# 旋律の性格: 6/8 の付点で浮かぶ跳躍、上がって漂う（バイオリンは柔らかく、力強く、透き通るように）
# 崩す所: ロックを3拍子系（6/8）で書く
from vp25_lib import *

S = Song("12", "watage", "たんぽぽの綿毛飛行（仮）", "A Dandelion Seed's Flight", 252, 6, "D", "major", "ロック（6/8）")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
WIND = ["D", "Bm/D", "G/D", "D"]
SKY = ["D", "F#m", "G", "A", "Bm", "F#m/A", "G", "A7sus4"]
GUST = ["Bb", "C", "D", "D"]
LAND = ["Bm", "G", "Em", "F#"]
SPRING = ["G", "A", "F#m", "Bm", "Em7", "A", "D", "D"]
SKY2 = [tr_chord(c, 2) for c in SKY]
S.scene("風", 8, "intro", WIND)
S.scene("飛び立つ", 24, "verse", SKY)
S.scene("空の旅", 40, "chorus", SKY)
S.scene("突風", 8, "break", GUST)
S.scene("凪", 4, "break", ["D", "D", "D", "D"])
S.scene("着地", 16, "verse", LAND)
S.scene("春", 24, "pre", SPRING)
S.scene("もう一度", 40, "chorus", SKY2)
S.scene("凪の終わり", 12, "outro", ["E", "E", "A/E", "E", "E", "E", "E", "E", "E", "E", "E", "E"])
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
K2 = K.up(2)
B = 6

VN = S.track("主役: バイオリン", "strings", patch="violin", volume=0.24, pan=0.0, reverb=0.38, gainDb=5, phrase=6, mono=True,
             fx=[{"type": "eq", "low": -4, "mid": 1.5, "midHz": 2200, "high": 1.5}, {"type": "eq", "low": 0, "mid": -1.5, "midHz": 450, "high": 0}])
VN2 = S.track("バイオリン（下の声）", "strings", patch="violin", volume=0.15, pan=-0.3, reverb=0.4, gainDb=2, mono=True)
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.14, pan=0.25, reverb=0.35)
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.1, 0.0)) for i in range(3)]
CL = S.track("クリーンのギター（分散和音）", "guitar", **clean_gtr_spec(0.1, 0.45))
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.5, 0.5, 0][i])) for i in range(3)]
FX = S.track("効果音（風）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.35)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# 拍は8分。旋律は付点（3拍＝付点4分）で浮かぶ
FLY = ["1:2 3:1 5:3", "6:2 5:1 3:3", "4:2 6:1 1':3", "7:3 5:3", "6:2 1':1 3':3", "2':2 1':1 6:3", "5:2 4:1 2:2 4:1", "5:6"]
FLY2 = ["3':2 2':1 1':3", "1':2 7:1 5:3", "6:2 1':1 2':3", "1':3 7:2 5:1", "6:2 7:1 1':2 3':1", "5':3 3':3", "4':2 3':1 2':2 1':1", "2':6"]
SKYM = FLY + FLY2
for i, b in enumerate(S.sc("風")):
    if i >= 4: VN.bar(b, K.mel(["5:6", "6:3 5:3", "3:6", "2:3 R:3"][i - 4], oct=4))
for i, b in enumerate(S.sc("飛び立つ")): VN.bar(b, K.mel(FLY[i % 8], oct=4 if i < 16 else 5))
for i, b in enumerate(S.sc("空の旅")):
    VN.bar(b, K.mel(SKYM[i % 16], oct=4 if i < 16 else 5) if i < 32 else K.mel(["5':6", "4':3 3':3", "2':6", "1':3 R:3", "3':6", "2':3 1':3", "7:6", "R:6"][i - 32], oct=4))
    if 16 <= i < 32: VN2.bar(b, K.mel(seq_up(SKYM[i % 16], K, -2), oct=4))
GU = ["4':1 5':1 6':1 1'':3", "7':1 1'':1 2'':1 3'':3", "#4':2 5':1 6':3", "5':6"]
for i, b in enumerate(S.sc("突風")):
    kk = Key("D", "major")
    VN.bar(b, kk.mel(["b6:1 b7:1 1':1 2':3", "b7:1 1':1 2':1 3':3", "#4':2 5':1 6':3", "5':6"][i % 4], oct=4) if i < 4 else
           kk.mel(["b6':1 b7':1 1'':1 2'':3", "b7':1 1'':1 2'':1 3'':3", "#4'':2 5'':1 6'':3", "5'':6"][i % 4], oct=3))
# 着地: 低く、長く
for i, b in enumerate(S.sc("着地")): VN.bar(b, K.mel(["6,:6", "5,:3 4,:3", "5,:6", "#4,:6", "6,:3 1:3", "2:3 1:3", "7,:6", "#1:6"][i % 8], oct=5) if i >= 4 else "R:6")
# 春: 花が開くように上る
SP = ["2:2 3:1 5:3", "4:2 3:1 #1:3", "3:2 5:1 6:3", "4:3 2:3", "5:2 6:1 1':3", "#1':2 2':1 3':3", "2':6", "1':3 R:3"]
for i, b in enumerate(S.sc("春")): VN.bar(b, K.mel(SP[i % 8], oct=4 if i < 16 else 5))
for i, b in enumerate(S.sc("もう一度")):
    VN.bar(b, K2.mel(SKYM[i % 16], oct=5 if i >= 8 else 4) if i < 32 else K2.mel(["5':6", "6':3 5':3", "3':6", "2':3 1':3", "1':6", "R:6", "R:6", "R:6"][i - 32], oct=4))
    if 8 <= i < 32: VN2.bar(b, K2.mel(seq_up(SKYM[i % 16], K2, -2), oct=5))
for i, b in enumerate(S.sc("凪の終わり")):
    if i == 10: VN.bar(b, K2.mel("5:6", oct=5))          # 凪の無音のあと、1音

# ---------- 伴奏 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; pw = power(ch, "E2"); r = low(ch, "E1")
    if n in ("空の旅", "もう一度", "突風") or (n == "飛び立つ" and i >= 8):
        pat = "X:3! X:2 X:1" if n != "突風" else "X:1! X:1 X:1 X:1! X:1 X:1"
        if n == "飛び立つ": pat = "X:6!"
        for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))
    if n in ("飛び立つ", "着地", "春", "空の旅") and not (n == "空の旅" and i >= 32):
        t = tones(ch, "D3", "D5")
        CL.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in [0, 2, 4, 3, 2, 1]))
    if n in ("風", "着地", "凪の終わり") or (n == "春" and i < 8):
        v = voice(ch, 57, 3)
        if not (n == "凪の終わり" and i >= 4):
            for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:6")
    # ベース（付点4分の歩み）
    if n in ("空の旅", "もう一度"): BASS.bar(b, f"{nm(r)}:2! {nm(r)}:1 {nm(r + 7)}:2 {nm(r + 12)}:1")
    elif n == "突風": BASS.bar(b, " ".join(f"{nm(r)}:1{'!' if q % 3 == 0 else ''}" for q in range(6)))
    elif n in ("飛び立つ", "春") and i >= 8: BASS.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3")
    elif n == "着地" and i >= 4: BASS.bar(b, f"{nm(r)}:6")
    if n in ("空の旅", "もう一度", "春"):
        CELLO.bar(b, f"{nm(low(ch, 'C3'))}:6" if i % 2 == 0 else f"{nm(low(ch, 'C3'))}:3 {nm(low(ch, 'C3') + 7)}:3")

FX.bar(S.sc("風")[0], "D4:6 R:6")
FX.bar(S.sc("凪")[0], "A4:6 R:18")
cym_swell(CYM, S.sc("空の旅")[0], 3, "C4"); cym_swell(CYM, S.sc("突風")[0], 6, "E4"); cym_swell(CYM, S.sc("もう一度")[0], 3, "C4")

# ---------- ドラム（6/8: 1拍目キック・4拍目スネア、8分のハット。グリッドは24文字＝8分×6） ----------
def g6(s): return s.replace(" ", "")
SIX_K = g6("X... .... .... .... .... x...")
SIX_S = g6(".... .... .... X... .... ....")
SIX_H = g6("x... x... x... x... x... x...")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "飛び立つ" and i >= 8:
        D.set(b, SIX_K, SIX_S if i >= 16 else "." * 24, SIX_H)
        if i == 8: crash(D, b, "D2", 6)
        continue
    if n in ("空の旅", "もう一度"):
        kk = SIX_K if i % 4 != 3 else g6("X... .... x... .... X... x...")
        D.set(b, kk, g6(".... .... ..o. X... .... ..o."), SIX_H)
        if i % 8 == 0: D.cym(b, f"{'C2' if i % 16 == 0 else 'G2'}:6"); D.H[b] = "." + D.H[b][1:]
        if i % 8 == 7:
            D.S[b] = g6(".... .... .... X... x.x. XXXX"); D.H[b] = g6("x... x... x... ........ ....")[:24].ljust(24, ".")
            D.tom(b, "R:4 C4:0.5 A3:0.5 F3:0.5 D3:0.5" if i % 16 == 15 else "R:6")
        continue
    if n == "突風":
        D.set(b, g6("X... X... X... X... X... X..."), g6(".... .... .... X... .... X..."), "." * 24)
        D.cym(b, "C2:6" if i % 4 == 0 else "D2:1 D2:1 D2:1 D2:1 D2:1 D2:1")
        if last: D.set(b, "X" + "." * 23, "X" + "." * 23, "." * 24)
        continue
    if n == "春" and i >= 8:
        D.set(b, SIX_K, SIX_S if i >= 16 else "." * 24, g6("x... .... x... .... x... ...."))
        if last: D.S[b] = g6(".... .... .... X... xxxx XXXX")
        continue
    if n == "着地" and i >= 8:
        D.set(b, g6("X... .... .... .... .... ...."), "." * 24, g6(".... .... x... .... .... x..."))

S.desc = ("仮: ボカロ曲のインスト25曲の12。6/8 のロック。D長調（2周目は E長調）。付点4分＝84。主役の楽器はバイオリン（柔らかく、力強く、透き通るように）。"
          "たんぽぽの綿毛の旅。風（ドローン）→飛び立つ→空の旅→突風（最大）→凪（4小節の無音）→野原に着地→次の春に花→また飛び立つ（転調）→凪のあとのバイオリンの1音。自作")
S.write()
