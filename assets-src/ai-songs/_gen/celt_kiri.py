# ケルトの小品「霧の湖の灯り」Lantern on the Misty Lake（仮）— 2026-10-25 人間「ケルトは音全体に強弱と余韻をつけて。スケールの大きさと幻想的な感じで。
#   ちょっと軽い曲。空間も意識して。頭の中を全て支配するような感じで」。サウンドセット celtic-fantasy と、空間 dome（とても大きくやわらかい）で鳴らす。
# 物語: 夜の霧の湖。ひとつの灯りがともり、舟で湖を渡ると、霧の向こうから光の柱が立ちのぼる。光が消えたあと、湖はまた静かになる。
# 強さ: 霧（pp）→ 灯り（p）→ 湖を渡る（mp→mf）→ 光の柱（f→ff。いちばん大きい）→ 1拍の無音 → 静けさ（pp）→ 帰り道（f。+2 の転調）→ 消える（pp。長い余韻）
# 音域: チェロ・コントラバスの C2 から、笛の D6・ベルの C7 まで（5オクターブ）
import sys
from vb25_lib import *

S = Song("C1", "kiri", "霧の湖の灯り（仮）", "Lantern on the Misty Lake", 88, 4, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("霧", 8, "intro", ["Dm", "Dm", "C/D", "Dm", "Bbmaj7", "C", "Dm", "Dm"])
S.scene("灯り", 8, "verse", ["Dm", "C", "Bb", "F", "Gm", "C", "Dm", "A"])
S.scene("湖を渡る", 8, "verse", ["Dm", "C", "Bb", "F", "Gm", "Bb", "C", "A7"])
S.scene("光の柱", 8, "chorus", ["Bb", "C", "Am", "Dm", "Gm", "C", "F", "A"])
S.scene("静けさ", 4, "break", ["Dm", "Bbmaj7", "Gm6", "A"])
S.scene("帰り道", 8, "chorus", ["C", "D", "Bm", "Em", "Am", "D", "G", "B"])   # +2（E ドリアン側へ）
S.scene("消える", 6, "outro", ["Em", "Cmaj7", "D", "Em", "Em", "Em"])
K = S.key; KE = Key("E", "dorian")
NB = S.nb

def curve(points):
    """場面ごとの強さ（0〜1）の点を、小節ごとの値にする（直線でつなぐ）"""
    out = []
    pts = sorted(points)
    for b in range(NB):
        for (b0, v0), (b1, v1) in zip(pts, pts[1:]):
            if b0 <= b <= b1:
                out.append(round(v0 + (v1 - v0) * (b - b0) / max(1, b1 - b0), 3)); break
        else: out.append(pts[-1][1])
    return out
s0 = {n: S.sc(n)[0] for n in ("霧", "灯り", "湖を渡る", "光の柱", "静けさ", "帰り道", "消える")}
# 曲全体の強さの曲線（全員にかける）。ff の所を 1.0
DYN = curve([(0, 0.35), (s0["灯り"], 0.5), (s0["湖を渡る"], 0.62), (s0["光の柱"] - 1, 0.8), (s0["光の柱"] + 4, 1.0), (s0["静けさ"] - 1, 0.95),
             (s0["静けさ"], 0.4), (s0["帰り道"] - 1, 0.55), (s0["帰り道"] + 3, 0.92), (s0["消える"], 0.7), (NB - 1, 0.25)])
def g(extra=None):
    return [round(d * (extra[b] if extra else 1), 3) for b, d in enumerate(DYN)]

HARP = S.track("ハープ", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.15, pan=-0.1, reverb=0.45, barGain=g())
HARP2 = S.track("ハープ（高い響き）", "harp", patch="folkHarp", volume=0.08, pan=0.4, reverb=0.6, barGain=g())
WH = S.track("笛", "lead", patch="tinWhistle", recipe="celtic-whistle", volume=0.12, pan=-0.05, reverb=0.5, barGain=g())
FID = S.track("フィドル", "strings", patch="violin", recipe="celtic-fiddle", volume=0.1, pan=0.2, reverb=0.5, barGain=g())
STR = [S.track(f"弦の持続{i}", "strings", patch="slowStrings", recipe="celtic-strings", volume=0.07, pan=[-0.7, 0.7, 0][i], reverb=0.55, barGain=g()) for i in range(3)]
LOW = S.track("チェロ", "strings", patch="cello", recipe="celtic-low", volume=0.1, pan=-0.15, reverb=0.35, barGain=g())
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.08, pan=0.15, reverb=0.35, barGain=g())
HORN = S.track("ホルン", "brass", patch="horn", volume=0.08, pan=0.3, reverb=0.55, barGain=g())
CHOIR = [S.track(f"合唱のような空気{i}", "pad", patch="modernPad", recipe="celtic-pad", volume=0.05, pan=[-0.6, 0.6][i], reverb=0.6, barGain=g()) for i in range(2)]
BELL = S.track("ベル（光）", "bell", patch="glockenspiel", volume=0.06, pan=0.35, reverb=0.7, barGain=g())
TIMP = S.track("ティンパニ", "strings", patch="timpani", volume=0.09, pan=0, reverb=0.45, barGain=g())
FD = S.track("枠太鼓", "harp", patch="frameDrum", volume=0.06, pan=-0.2, reverb=0.4, barGain=g())
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
SIL = Silence(S)

# ---------- 旋律（D ドリアン。笛とフィドルの掛け合い） ----------
A = ["5:1.5 4:0.5 3:1 1:1", "2:1 4:1 5:2", "6:1 5:0.5 4:0.5 3:1 2:1", "1:3 R:1",
     "5:1 6:0.5 7:0.5 1':1 7:1", "6:1.5 5:0.5 4:2", "3:1 4:0.5 5:0.5 2:1 7,:1", "#3:3 R:1"]
B = ["1':1 7:0.5 6:0.5 5:1 6:1", "7:1 1':0.5 2':0.5 3':2", "2':1 1':0.5 7:0.5 6:1 4:1", "5:3 R:1",
     "4:1 5:0.5 6:0.5 7:1 2':1", "1':1.5 7:0.5 6:1 5:1", "4:1 5:1 6:1 7:1", "#3':4"]
C = ["4':2 3':1 2':1", "3':1.5 2':0.5 1':2", "1':1 2':1 3':1 5':1", "5':3 4':0.5 3':0.5",
     "2':1.5 1':0.5 7:1 6:1", "7:1 1':1 2':1 3':1", "4':2 3':1 1':1", "#3':4"]
for i, b in enumerate(S.sc("灯り")): WH.bar(b, K.mel(A[i], oct=5))
for i, b in enumerate(S.sc("湖を渡る")):
    if i % 2 == 0: FID.bar(b, K.mel(B[i], oct=4))
    else: WH.bar(b, K.mel(B[i], oct=5))
for i, b in enumerate(S.sc("光の柱")):
    WH.bar(b, K.mel(C[i], oct=4)); FID.bar(b, K.mel(C[i], oct=4))         # 笛とフィドルを同じ旋律で（笛はオクターブ上の響き）
for i, b in enumerate(S.sc("静けさ")):
    if i >= 1: FID.bar(b, K.mel(["R:4", "5:2 4:1 3:1", "2:3 R:1", "#3:4"][i], oct=4))
for i, b in enumerate(S.sc("帰り道")):
    WH.bar(b, KE.mel(C[i], oct=4)); FID.bar(b, KE.mel(A[i], oct=4))
for i, b in enumerate(S.sc("消える")):
    if i < 4: WH.bar(b, KE.mel(["5:2 3:2", "1:4", "2:2 4:2", "1:4"][i], oct=5))

# ---------- 伴奏 ----------
for b in range(NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2")
    # ハープ: 霧はゆっくり高い響きだけ、灯りから8分の分散和音（上へ下へ）
    t = tones(ch, "D3", "D6")
    if n == "霧":
        HARP2.bar(b, " ".join(f"{nm(x)}:1" for x in [t[-1], t[-3], t[-2], t[-4]]))
        if i >= 4: HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
    elif n in ("静けさ",):
        HARP.bar(b, " ".join(f"{nm(t[q])}:1" for q in (0, 2, 4, 3)) if i < 3 else f"{nm(t[0])}:4")
    elif n == "消える":
        if i < 5: HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 5, 3, 2, 1)) if i < 3 else " ".join(f"{nm(t[q])}:1" for q in (0, 2, 4, 6)))
        else: HARP2.bar(b, f"{nm(t[-1])}:4")
    else:
        HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 6, 7, 6, 4, 2)))
        if n in ("光の柱", "帰り道"): HARP2.bar(b, " ".join(f"{nm(x)}:0.5" for x in [t[-1], t[-2], t[-3], t[-2]] * 2))
    # 低い支え
    if n not in ("霧",) or i >= 4:
        LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
    if n in ("光の柱", "帰り道") or (n == "湖を渡る" and i >= 4): CB.bar(b, f"{nm(lo)}:4")
    # 弦の持続（湖を渡るの後半から）と合唱のような空気（霧と光の柱）
    v = voice(ch, 62, 3, spread=True)
    if n in ("光の柱", "帰り道") or (n == "湖を渡る" and i >= 2) or (n == "消える" and i < 4):
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    if n in ("霧", "光の柱", "帰り道", "消える"):
        w = voice(ch, 69, 2)
        for j in range(2): CHOIR[j].bar(b, f"{nm(w[j])}:4")
    if n in ("光の柱", "帰り道") and i % 2 == 0:
        h = voice(ch, 58, 1)[0]; HORN.bar(b, f"{nm(h)}:3 R:1")
    # ベル: 光の場面だけ、きらめき
    if n in ("霧", "光の柱", "帰り道") and i % 2 == 1:
        BELL.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C6", "C7")[:4]))
    # 打楽器: 枠太鼓（湖を渡るから）・ティンパニ（光の柱の頭とロール）
    if n in ("湖を渡る", "光の柱", "帰り道"):
        FD.bar(b, "C3:1 R:0.5 D3:0.5 C#3:1 D3:0.5 D3:0.5" if n != "湖を渡る" else "C3:1 R:1 C#3:1 R:1")
    if n in ("光の柱", "帰り道") and i % 4 == 0: TIMP.bar(b, f"{nm(low(ch, 'D2'))}:2 R:2")
    if n == "湖を渡る" and i == 7: TIMP.bar(b, " ".join([f"{nm(low('A', 'D2'))}:0.25"] * 16))     # ロールで光の柱へ
cym_swell(CYM, s0["光の柱"] - 1, 4, "E4"); cym_swell(CYM, s0["帰り道"] - 1, 2, "C4")
CYM.bar(NB - 3, "B4:12")            # 最後はシンバルのロールのディミヌエンドで余韻
SIL.add(s0["静けさ"] - 1, 3, 4)     # 光の柱のあとの1拍の完全な無音
SIL.apply()
season(S, 0, "そよ風", 32, vol=0.07)
season(S, NB - 6, "そよ風", 24, vol=0.06)
S.fade_out = 0
S.flags = "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0"
S.desc = ("仮: ケルトの小品。D ドリアン（帰り道で E ドリアン）・88。夜の霧の湖にひとつの灯り、舟で渡ると光の柱が立つ。"
          "霧(pp)→灯り(p)→湖を渡る→光の柱(ff)→1拍の無音→静けさ(pp)→帰り道(+2・f)→消える(pp・長い余韻)。空間は大きな dome。自作")
vwrite(S)
