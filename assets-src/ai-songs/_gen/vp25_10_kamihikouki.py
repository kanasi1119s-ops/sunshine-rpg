# vp25 10「紙ひこうき選手権」The Paper Airplane Championship（仮）— ロック。C長調（優勝機の後半で D長調）・168・4/4。主役の楽器: ドローバーオルガン
# 物語: 町内会の紙ひこうき選手権。号砲とともに開会。1機目はまっすぐ、2機目は宙返り、3機目はくるくる回って落ちる。
#   休憩のあと、最後の1機（優勝機）が風に乗って長く高く飛び、校庭のフェンスを越えて、空の向こうへ。
# 形: 選手が順番に投げる大会。飛び方は一機ずつ違う。優勝機がフェンスを越える（サビという区切りを置かない）
# 場面と強さ: 開会＝いきなり全員／飛行ごとに短い山（だんだん大きく）／着地のたびに一瞬の静けさ（オルガンだけ）／
#   優勝機の飛行だけ長く高い（この曲の山）→フェンスを越えて遠ざかる（フェードアウト）
# 旋律の性格: まっすぐ（同じ音の連打）・宙返り（輪を描くアルペジオ）・くるくる（らせんの下降）と、機体ごとに違う動き。飛ばすのも機体ごとに違う楽器
# 崩す所: サビを置かない（飛行ごとに主役が変わる）
from vp25_lib import *

S = Song("10", "kamihikouki", "紙ひこうき選手権（仮）", "The Paper Airplane Championship", 168, 4, "C", "major", "ロック")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
OPEN = ["C", "F/C", "G/C", "C", "C", "F/C", "G", "G"]
STRAIGHT = ["C", "Em/B", "F/A", "G", "C", "Bb", "F", "G"]
LOOP = ["Dm7", "G7", "Em7", "A7", "Dm7", "G7", "Cmaj7", "C7"]
SPIRAL = ["F", "E7", "Am", "Am/G", "F", "E7", "Am", "G"]
BREAK = ["C7", "C7", "F7", "F7", "C7", "C7", "G7", "G7"]
WIN = ["C", "D/C", "B7/D#", "Em", "F", "G", "Am", "G/B"]
WIN2 = [tr_chord(c, 2) for c in WIN]
S.scene("開会", 8, "intro", OPEN)
S.scene("まっすぐ", 24, "verse", STRAIGHT)
S.scene("着地1", 4, "break", ["F", "F", "G", "G"])
S.scene("宙返り", 28, "verse", LOOP + LOOP + LOOP + ["Dm7", "G7", "Cmaj7", "Cmaj7"])
S.scene("着地2", 4, "break", ["Am", "Am", "G", "G"])
S.scene("くるくる", 24, "pre", SPIRAL)
S.scene("着地3", 4, "break", ["F", "F", "G", "G7"])
S.scene("休憩", 16, "solo", BREAK)
S.scene("優勝機", 56, "chorus", WIN + WIN + WIN + ["F", "G", "A", "A"] + WIN2 + WIN2 + WIN2)
S.scene("空の向こう", 8, "outro", ["D", "G/D", "D", "D", "D", "D", "D", "D"])
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
K2 = K.up(2)

ORG = [S.track(f"主役: オルガン{i + 1}", "drawbarOrgan", volume=0.15, pan=[-0.3, 0.3, 0.0, 0.0][i], reverb=0.2, gainDb=4, sustain=1.0,
               fx=[{"type": "rotary", "mix": 0.6}, {"type": "eq", "low": -3, "mid": 2, "midHz": 1500, "high": 1}]) for i in range(4)]
ORGL = S.track("主役: オルガン（旋律）", "drawbarOrgan", volume=0.2, pan=0.0, reverb=0.2, gainDb=5, phrase=8, mono=True,
               fx=[{"type": "rotary", "mix": 0.5}, {"type": "eq", "low": -4, "mid": 2.5, "midHz": 1800, "high": 1}])
LEAD = S.track("リード（1機目・優勝機）", "lead", **lead_spec("squareLead", vol=0.19, pan=0.05, delay=0.5))
LG = S.track("リードギター（2機目）", "distGuitar", **lead_gtr_spec(0.15, -0.05))
GT = [S.track(f"ギター（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.1, 0.0)) for i in range(3)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.2))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 1機目: まっすぐ（同じ音の連打、高さは変えずにリズムで進む） ----------
STR = ["5:0.5 5:0.5 5:0.5 5:0.25 5:0.25 5:1 5:1", "5:0.5 5:0.5 6:0.5 5:0.5 5:2", "5:0.25 5:0.25 5:0.5 5:0.5 5:0.5 6:1 5:1", "5:4",
       "1':0.5 1':0.5 1':0.5 1':0.25 1':0.25 1':1 b7:1", "1':0.5 1':0.5 1':0.5 2':0.5 1':2", "6:0.5 6:0.5 6:0.25 6:0.25 6:0.5 5:2", "5:4"]
for i, b in enumerate(S.sc("まっすぐ")):
    if i < 4: continue
    m = STR[(i - 4) % 8]
    if i >= 20: m = ["5:1 5:1 5:1 5:1", "5:2 R:2", "3:4", "R:4"][i - 20]       # 着地へ
    LEAD.bar(b, K.mel(m, oct=4 if i < 12 else 5))
# 2機目: 宙返り（輪を描くアルペジオ。リードギター）
def loop_bar(b, i):
    t = tones(S.chords[b], "G3", "G5")
    up_ = [t[q] for q in (0, 1, 2, 3, 4)]
    seq = up_ + list(reversed(up_[1:4]))
    return " ".join(f"{nm(seq[q % len(seq)])}:0.5" for q in range(8))


for i, b in enumerate(S.sc("宙返り")):
    if i < 4: continue
    LG.bar(b, loop_bar(b, i) if i % 4 != 3 else f"{nm(tones(S.chords[b], 'C4', 'C5')[0])}:2 {nm(tones(S.chords[b], 'C5', 'C6')[0])}:2")
# 3機目: くるくる（らせんの下降。オルガンが飛ばす）
SP = ["1'':0.5 6':0.5 7':0.5 5':0.5 6':0.5 4':0.5 5':0.5 3':0.5", "#5':0.5 7':0.5 6':0.5 #4':0.5 #5':0.5 3':0.5 4':0.5 2':0.5",
      "3':0.5 1':0.5 2':0.5 7:0.5 1':0.5 6:0.5 7:0.5 5:0.5", "6:2 R:2",
      "6':0.5 4':0.5 5':0.5 3':0.5 4':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 #5:0.5 6:0.5 #4:0.5 #5:0.5 3:0.5 7:1",
      "1':0.5 6:0.5 7:0.5 5:0.5 6:0.5 3:0.5 4:0.5 2:0.5", "5:4"]
for i, b in enumerate(S.sc("くるくる")): ORGL.bar(b, K.mel(SP[i % 8], oct=4))
# 休憩: オルガンのブルースのソロ
BL = ["5:0.5 b7:0.5 1':1 b7:0.5 5:0.5 4:1", "b3:0.5 3:0.5 5:2 R:1", "1':0.5 b7:0.5 5:0.5 4:0.5 b3:1 1:1", "R:1 5:0.5 6:0.5 b7:1 6:1",
      "5:0.5 1':0.5 b3':1 2':0.5 1':0.5 b7:1", "5:3 R:1", "2':1 1':0.5 b7:0.5 6:1 5:1", "4:0.5 #4:0.5 5:3"]
for i, b in enumerate(S.sc("休憩")): ORGL.bar(b, K.mel(BL[i % 8], oct=4 if i < 8 else 5))
# 優勝機: 長く高く（リード）。オルガンは後半で旋律を重ねる
WM = ["1':2 2':1 3':1", "5':3 4':1", "#4':2 3':1 2':1", "3':4", "4':2 5':1 6':1", "5':2 4':2", "3':1 4':1 5':1 6':1", "5':4",
      "1':1 3':1 5':2", "6':2 5':2", "#5':2 7':1 6':1", "5':4", "6':2 5':1 4':1", "5':2 6':2", "7':2 1'':2", "2'':4"]
for i, b in enumerate(S.sc("優勝機")):
    if i < 24: m = WM[i % 16]; kk = K
    elif i < 28: m = ["4':2 5':2", "6':2 7':2", "#1'':4", "R:4"][i - 24]; kk = K
    else: m = WM[(i - 28) % 16]; kk = K2
    LEAD.bar(b, kk.mel(m, oct=4))
    if i >= 36: ORGL.bar(b, kk.mel(m, oct=4 if i < 44 else 3))
for i, b in enumerate(S.sc("空の向こう")):
    if i < 4: LEAD.bar(b, K2.mel(["1'':4", "R:4", "5':4", "R:4"][i], oct=4))

# ---------- オルガンの和音（主役。着地の静けさではオルガンだけ） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 64, 4)
    if n == "開会":
        pat = "X:1! X:1 X:1.5 X:0.5" if i % 2 == 0 else "X:2! X:2"
        if i < 4:   # 開会のファンファーレはオルガンの旋律（同じ音の連打で始まる）
            ORGL.bar(b, K.mel(["1':0.5 1':0.5 1':0.5 1':0.5 3':1 5':1", "4':2 3':1 2':1", "5:0.5 5:0.5 5:0.5 5:0.5 7:1 2':1", "1':4"][i], oct=4))
    elif n.startswith("着地"): pat = "X:4" if i < 2 else "X:2 X:2"
    elif n in ("まっすぐ", "宙返り", "くるくる"): pat = "R:0.5 X:0.5 R:1 R:0.5 X:0.5 R:1" if n != "宙返り" else "X:1.5 X:2.5"
    elif n == "休憩": pat = "R:0.5 X:0.25 R:0.25 R:1 R:0.5 X:0.25 R:0.25 R:1"
    elif n == "優勝機": pat = "X:4" if i < 24 else "X:2 X:2"
    elif n == "空の向こう": pat = "X:4"
    else: continue
    for j in range(4): ORG[j].bar(b, pat.replace("X", nm(v[j])))

# ---------- ギター ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    pw = power(S.chords[b], "E2")
    if n == "開会": pat = "X:1! X:1 X:1.5! X:0.5" if i < 7 else "X:2! R:2"
    elif n == "まっすぐ": pat = " ".join("X:0.5" + ("!" if j % 4 == 0 else "") for j in range(8)) if i >= 4 else "X:4"
    elif n == "宙返り": pat = "X:1.5! X:1 X:1.5"
    elif n == "くるくる": pat = "X:0.75! X:0.75 X:0.5 X:0.75! X:0.75 X:0.5"
    elif n == "優勝機": pat = " ".join("X:0.5" + ("!" if j % 2 == 0 else "") for j in range(8)) if i >= 8 else "X:2 X:2"
    else: continue
    if n in ("まっすぐ", "宙返り", "くるくる") and i == L - 1: pat = "X:2! R:2"
    for j in range(3): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n.startswith("着地"): BASS.bar(b, f"{nm(r)}:4" if i == 0 else "R:4"); continue
    if n == "開会": BASS.bar(b, f"{nm(r)}:1! {nm(r)}:1 {nm(r)}:1.5 {nm(r)}:0.5" if i < 7 else f"{nm(r)}:2! R:2"); continue
    if n == "宙返り": BASS.bar(b, bass_line(S, b, "walk")); continue
    if n == "休憩": BASS.bar(b, bass_line(S, b, "walk")); continue
    if n == "空の向こう": BASS.bar(b, f"{nm(r)}:4" if i < 4 else "R:4"); continue
    if n in ("まっすぐ", "くるくる", "優勝機"):
        if i == L - 1 and n != "優勝機": BASS.bar(b, f"{nm(r)}:2! R:2"); continue
        BASS.bar(b, bass_line(S, b, "root8" if n != "くるくる" else "push"))

for sc_ in ("まっすぐ", "宙返り", "くるくる"):
    riser(FX, S.sc(sc_)[0], 4, "C4")
cym_swell(CYM, S.sc("優勝機")[0], 2, "C4"); cym_swell(CYM, S.sc("優勝機")[28], 2, "C4")
riser(FX, S.sc("優勝機")[28], 8, "D4")

# ---------- ドラム ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "開会":
        put_groove(D, b, ("X.......X.X.....", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "C2")
        if i == 4: crash(D, b, "G2")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
        continue
    if n.startswith("着地"): continue
    if n == "まっすぐ":
        put_groove(D, b, ("X.......X.......", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        if i == 4: crash(D, b)
        if i % 8 == 3 and i < 20: put_fill(D, b, "small")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
        continue
    if n == "宙返り":
        put_groove(D, b, ("X.....x.X.......", "....X......oX...", "." * 16), ghosts=0.6, seed=b, hat_vary=False)
        D.cym(b, ("C2:1 " if i == 4 else "D2:1 ") + "D2:0.6667 D2:0.3333 D2:1 D2:0.6667 D2:0.3333")
        if i % 8 == 7: put_fill(D, b, "tomtrip")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
        continue
    if n == "くるくる":
        put_groove(D, b, ("X..X..X...X..X..", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.4, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "B2")
        if i % 4 == 3: put_fill(D, b, "tomdown" if i % 8 == 7 else "small")
        if last: D.set(b, "X.......X.......", "X.......X.......", "." * 16)
        continue
    if n == "休憩":
        put_groove(D, b, ("X.......X.......", "....X.......X...", "x..xx..xx..xx..x"), ghosts=0.6, seed=b, hat_vary=False)
        if last: put_fill(D, b, "build")
        continue
    if n == "優勝機":
        if i < 8: put_groove(D, b, ("X.......X.......", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        else: put_groove(D, b, ("X.X...X.X.X...X.", "....X.......X...", "X.x.X.x.X.x.X.x."), ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        elif i % 4 == 3: put_fill(D, b, "small")
        if i == 27: put_fill(D, b, "build")
        continue
    if n == "空の向こう" and i < 2:
        D.set(b, "X" + "." * 15, "." * 16, "." * 16)
        if i == 0: crash(D, b, "C2")

S.fade_out = 14
S.desc = ("仮: ボカロ曲のインスト25曲の10。ロック。C長調（優勝機の後半で D長調）・168。主役の楽器はドローバーオルガン（回るスピーカー）。町内会の紙ひこうき選手権。"
          "号砲で開会（いきなり全員）。1機目はまっすぐ（同じ音の連打、リード）、2機目は宙返り（輪を描くアルペジオ、リードギター）、3機目はくるくる（らせんの下降、オルガン）。"
          "着地のたびにオルガンだけの静けさ。休憩のオルガンのブルースをへて、優勝機が長く高く飛び、フェンスを越えて空の向こうへ（サビは置かない）。自作")
S.write()
