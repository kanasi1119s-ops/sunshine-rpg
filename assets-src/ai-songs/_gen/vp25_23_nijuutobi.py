# vp25 23「二重とび」Double Dutch Days（仮）— K-POP。E長調（最後のサビで F#長調）・124⇄150（場面でビートが切り替わる）・4/4。主役の楽器: ロートタム
# 物語: 体育の授業の縄跳びテスト。ふつう跳びは余裕。二重とびもできた。三重とびに挑戦して…縄が足に引っかかる（しん）。
#   もう一度立ち上がって、跳ぶ。成功！ みんなの拍手の中で着地。
# 形: ふつう跳び→二重とび→ふつう跳び→二重とび→三重とびで引っかかる→立ち上がる→成功（ダンスブレイク）→最後のサビ→着地
# 場面と強さ: 二重とびで上がる（テンポも 150 のトラップへ）／引っかかる＝急な無音（2小節）／成功＝最大のダンスブレイク／着地でぴたりと止まる
# 旋律の性格: 縄が地面を打つリズムの、跳ねる2音のフック（ロートタムが音程で弾く）。高く伸びるプリコーラス（リード）
# 崩す所: フックをドラム（音程のあるロートタム）に任せる
from vp25_lib import *

S = Song("23", "nijuutobi", "二重とび（仮）", "Double Dutch Days", 124, 4, "E", "major", "K-POP")
K = S.key
VERSE = ["C#m7", "F#m7", "Amaj7", "B7sus4"]
PRE = ["Amaj7", "B/A", "G#m7", "C#7", "F#m7", "G#7", "Amaj7", "B7sus4"]
DROP = ["C#m7", "A", "F#m7", "G#7"]
BRIDGE = ["Amaj7", "G#m7", "F#m7", "E/G#", "Amaj7", "B", "C#m7", "B"]
S.scene("ふつう跳び", 24, "verse", VERSE)
S.scene("プリ", 8, "pre", PRE)
S.scene("二重とび", 16, "chorus", DROP)
S.scene("ふつう跳び2", 24, "verse", VERSE)
S.scene("プリ2", 8, "pre", PRE)
S.scene("二重とび2", 16, "chorus", DROP)
S.scene("三重とび", 8, "pre", ["A", "B", "C#m7", "D"] * 2)
S.scene("引っかかる", 2, "break", ["D", "D"])
S.scene("立ち上がる", 12, "bridge", BRIDGE + BRIDGE[:4])
S.scene("成功", 16, "solo", DROP)
F_ = [tr_chord(c, 2) for c in DROP]
S.scene("最後のサビ", 24, "chorus", F_)
S.scene("着地", 2, "outro", ["F#", "F#"])
T150 = [S.sc(n)[0] for n in ("二重とび", "二重とび2", "成功")]
T124 = [S.sc(n)[0] for n in ("ふつう跳び2", "三重とび")]
S.tempo = sorted([{"bar": b + 1, "bpm": 150} for b in T150] + [{"bar": b + 1, "bpm": 124} for b in T124], key=lambda e: e["bar"])
KF = K.up(2)
S.drum_gain = {"kick": {"gainDb": -6}}

RT = S.track("主役: ロートタム（縄のフック）", "rotoTom", patch="rotoTom", volume=0.26, pan=0.0, gainDb=5, reverb=0.15)
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.18, pan=0.0, delay=0.5))
PL = S.track("プラック", "pad", **pluck_spec("pluckSynth", vol=0.09, pan=0.4, delay=0.75, sustain=0.5))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.05, pan=[-0.6, 0.6, 0][i], duck=0.4, sustain=1.0)) for i in range(3)]
SUB = S.track("808", "sub808", **sub_spec(0.22))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass2", vol=0.18, duck=0.3))
EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.09, pan=[-0.35, 0.35, 0][i], reverb=0.2) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- ロートタムのフック（縄が地面を打つ: 跳ねる2音） ----------
def rope(ch, dens):
    r = low(ch, "A2")              # 太鼓の高さ（A2〜G#3 あたり）
    hi = r + 7 if r + 7 <= midi("B3") else r - 5
    pat = {1: f"{nm(r)}:1! R:1 {nm(r)}:1! R:1",
           2: f"{nm(r)}:0.75! {nm(hi)}:0.25 R:1 {nm(r)}:0.75! {nm(hi)}:0.25 R:1",
           3: f"{nm(r)}:0.5! {nm(hi)}:0.25 {nm(hi)}:0.25 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5! {nm(hi)}:0.25 {nm(hi)}:0.25 {nm(r)}:0.5 {nm(hi)}:0.5",
           4: f"{nm(r)}:0.25! {nm(hi)}:0.25 {nm(r)}:0.25 {nm(hi)}:0.25 R:0.5 {nm(r)}:0.25! {nm(hi)}:0.25 {nm(r)}:0.5 {nm(hi)}:0.25 {nm(r)}:0.25 R:0.5 {nm(hi)}:0.25 {nm(hi)}:0.25"}[dens]
    return pat


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n in ("ふつう跳び", "ふつう跳び2"): RT.bar(b, rope(ch, 1 if i < 8 else 2))
    elif n in ("プリ", "プリ2"): RT.bar(b, rope(ch, 1) if i < 6 else "R:4")
    elif n in ("二重とび", "二重とび2", "最後のサビ"): RT.bar(b, rope(ch, 3))
    elif n == "三重とび": RT.bar(b, rope(ch, 4))
    elif n == "成功": RT.bar(b, rope(ch, 4) if i % 4 != 3 else rope(ch, 3))
    elif n == "立ち上がる" and i >= 8: RT.bar(b, rope(ch, 1))
RT.bar(S.sc("引っかかる")[0], "A2:0.25! R:3.75")          # 縄が引っかかる

# ---------- 歌の役 ----------
VM = ["R:0.5 3:0.5 3:0.5 5:0.5 3:1 2:1", "R:0.5 6,:0.5 1:0.5 3:0.5 4:1 3:1", "R:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:1", "1:2 R:2",
      "R:0.5 5:0.5 5:0.5 6:0.5 5:1 3:1", "R:0.5 4:0.5 6:0.5 1':0.5 7:1 6:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':0.5 7:0.5 5:1", "6:2 R:2"]
PRM = ["1':2 2':2", "3':3 2':1", "5':4", "4':2 3':2", "2':2 3':2", "#1':2 7:2", "1':2 2':2", "3':4"]
DM = ["R:4", "5:0.5 6:0.5 R:3", "R:4", "1':0.5 7:0.5 R:3"]          # ドロップは短い合いの手だけ（フックはロートタム）
for sc_ in ("ふつう跳び", "ふつう跳び2"):
    for i, b in enumerate(S.sc(sc_)):
        if i >= 8 or sc_ == "ふつう跳び2": LEAD.bar(b, K.mel(VM[i % 8], oct=4 if sc_ == "ふつう跳び" else 5))
for sc_ in ("プリ", "プリ2"):
    for i, b in enumerate(S.sc(sc_)): LEAD.bar(b, K.mel(PRM[i], oct=4))
for sc_ in ("二重とび", "二重とび2"):
    for i, b in enumerate(S.sc(sc_)): LEAD.bar(b, K.mel(DM[i % 4], oct=5))
for i, b in enumerate(S.sc("立ち上がる")):
    LEAD.bar(b, K.mel(["3:4", "2:2 1:2", "6,:3 1:1", "7,:4", "1:2 3:2", "2:2 4:2", "3:4", "2:4", "5:2 6:2", "7:2 1':2", "2':2 3':2", "5':4"][i], oct=4))
for i, b in enumerate(S.sc("最後のサビ")):
    LEAD.bar(b, KF.mel(PRM[i % 8], oct=4) if i < 16 else KF.mel(["1'':4", "7':2 5':2", "6':4", "5':4", "4':2 5':2", "6':2 7':2", "1'':4", "1'':4"][i - 16], oct=4))

# ---------- 伴奏（場面ごとにジャンルが入れかわる） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("ふつう跳び", "ふつう跳び2"):
        v = voice(ch, 64, 3)
        for j in range(3): EP[j].bar(b, ("R:0.75 X:0.75 R:0.5 X:0.75 R:0.75 X:0.5" if n == "ふつう跳び" else "X:0.5 R:0.5 X:0.5 R:1 X:0.5 R:1").replace("X", nm(v[j])))
        BASS.bar(b, f"{nm(r)}:0.75 R:0.25 {nm(r)}:0.5 {nm(r + 12)}:0.5 R:1 {nm(r + 7)}:0.5 {nm(r)}:0.5" if i >= 4 else "R:4")
    if n in ("プリ", "プリ2", "立ち上がる"):
        v = voice(ch, 64, 3)
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
        BASS.bar(b, f"{nm(r)}:2 {nm(r)}:2")
    if n in ("二重とび", "二重とび2", "成功", "最後のサビ"):
        SUB.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r + 12)}:0.5 {nm(r)}:1")
        v = voice(ch, 66, 3)
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5")
        t = tones(ch, "E5", "E7")
        PL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in [0, 2, 1, 3, 2, 4, 3, 5, 4, 2, 3, 1, 2, 0, 1, 3]))
    if n == "三重とび":
        SUB.bar(b, f"{nm(r)}:4")
        t = tones(ch, "E5", "E7")
        PL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in range(16)))
for sc_ in ("二重とび", "二重とび2", "成功"): riser(FX, S.sc(sc_)[0], 4, "C4"); cym_swell(CYM, S.sc(sc_)[0], 2, "C4")
riser(FX, S.sc("最後のサビ")[0], 8, "D4")
FX.bar(S.sc("引っかかる")[0], "R:1 G4:3")

# ---------- ドラム（場面ごとにビートの型が入れかわる） ----------
REGGAETON = ("X...X...X...X...", "...X..X....X..X.", "x.x.x.x.x.x.x.x.")
AFRO = ("X......X..X.....", "....x.....X.....", "x.xxx.x.x.xxx.xx")
TRAP = ("X.....X...X.....", "........X.......", "x.x.x.x.xxxxx.x.")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ふつう跳び":
        if i >= 8: put_groove(D, b, REGGAETON, seed=b, hat_vary=False)
    elif n == "ふつう跳び2": put_groove(D, b, AFRO, ghosts=0.3, seed=b, hat_vary=False)
    elif n in ("プリ", "プリ2"):
        D.set(b, "X.......X.......", "....X.......X..." if i < 6 else ("x.x.x.x.x.x.x.x." if i == 6 else "xxxxxxxxXXXXXXXX"), "x.x.x.x.x.x.x.x." if i < 6 else "." * 16)
    elif n in ("二重とび", "二重とび2", "最後のサビ"):
        put_groove(D, b, TRAP, ghosts=0.2, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3: D.H[b] = "x.x.x.x.xxxxxxxx"
    elif n == "三重とび":
        D.set(b, "X...X...X...X...", "x.x.x.x.x.x.x.x." if i < 4 else "xxxxxxxxxxxxxxxx", "." * 16)
        if last: D.set(b, "X...X...X.......", "xxxxxxxxXXXX....", "." * 16)
    elif n == "立ち上がる":
        if i >= 8: D.set(b, "X.......X.......", "....X.......X...", "..x...x...x...x.")
    elif n == "成功":
        D.set(b, "X.X...X.X.X...X.", "....X..X..X.X...", "x.xxx.xxx.xxx.xx")
        if i % 4 == 0: crash(D, b, "C2" if i % 8 == 0 else "B2")
    elif n == "着地":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2")
    if n in ("ふつう跳び", "ふつう跳び2") and i % 8 == 7 and i >= 8: put_fill(D, b, "small")
RT.bar(S.sc("着地")[0], "F#2:1! R:3")

S.desc = ("仮: ボカロ曲のインスト25曲の23。K-POP。E長調（最後のサビで F#長調）。テンポは場面で 124 と 150 が入れかわる。主役の楽器はロートタム（音程のある太鼓）。"
          "体育の縄跳びテスト。縄が地面を打つリズムの跳ねる2音のフックをロートタムが弾く。ふつう跳び（レゲトン→アフロビート）→プリコーラス→二重とび（150 のトラップ）"
          "→三重とびに挑戦して引っかかる（2小節の無音）→立ち上がる→成功のダンスブレイク（最大）→最後のサビ→ぴたりと着地。自作")
S.write()
