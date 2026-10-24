# vp25 22「海沿いの国道、夕方五時」Coast Road, 5 PM（仮）— J-POP（シティポップ寄り）。E♭長調・112・4/4。主役の楽器: アルトサックス
# 物語: 夏の終わりの夕方。車の窓を開けて、海沿いの国道を走る。信号待ち、坂を上って、トンネル。抜けた瞬間、目の前いっぱいの海。
#   夕日が沈むまで走って、最後は波の音だけ。
# 形: 窓を開ける→海岸通り→信号待ち→坂の上→トンネル→海が見える→夕日が沈むまで→波
# 場面と強さ: 窓を開けた瞬間＝いきなり全員／トンネル＝こもって小さい（高い音を全部削る）／出た瞬間の海＝最大の開放／夕日＝だんだん減り、波の音だけ
# 旋律の性格: メジャー7th のシンコペーション、長い音を後ろに引っ張る（サックスは後ろにもたれて歌う）
# 崩す所: トンネルの間は、全部の楽器の高い音を削る（こもった別の音で弾く）
from vp25_lib import *

S = Song("22", "kokudou", "海沿いの国道、夕方五時（仮）", "Coast Road, 5 PM", 112, 4, "Eb", "major", "J-POP（シティポップ）")
S.kit = "jpop"   # 2026-10-25: 切り抜きで naked 6.83 → jpop 7.07
K = S.key
COAST = ["Abmaj7", "G7", "Cm7", "Bbm7", "Eb7", "Abmaj7", "Db9", "Ebmaj7"]
SIGNAL = ["Abmaj7", "Abmaj7", "Gm7", "Gm7", "Fm7", "Fm7", "Bb7sus4", "Bb7sus4"]
HILL = ["Fm7", "Gm7", "Abmaj7", "Bb7sus4"]
TUNNEL = ["Cm7", "Abmaj7", "Fm7", "G7"]
SEA = ["Ebmaj7", "G7", "Cm7", "Bbm7", "Abmaj7", "Db9", "Fm7", "Bb7sus4"]
DUSK = ["Abmaj7", "Gm7", "Fm7", "Ebmaj7"]
S.scene("窓を開ける", 8, "intro", SEA)
S.scene("海岸通り", 20, "verse", COAST + COAST + COAST[:4])
S.scene("信号待ち", 8, "break", SIGNAL)
S.scene("坂の上", 16, "pre", HILL)
S.scene("トンネル", 16, "bridge", TUNNEL)
S.scene("海が見える", 32, "chorus", SEA)
S.scene("夕日", 24, "solo", DUSK)
S.scene("波", 8, "outro", ["Ebmaj7"] * 8)
S.extra.update({"tone": "rock", "diGuitar": "emily", "swing16": 0.12})
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags   # 2026-10-25: 参考の音で 7.07 → 7.62（09 の切り抜き）
TUN = set(S.sc("トンネル"))
MUFF = [{"type": "filter", "kind": "lowpass", "freq": 700, "q": 0.8}, {"type": "reverb", "mix": 0.3}]

SAX = S.track("主役: アルトサックス", "brass", patch="altoSax", volume=0.25, pan=0.08, reverb=0.3, gainDb=7, phrase=8, mono=True,
              fx=[{"type": "eq", "low": -3, "mid": 2.5, "midHz": 1800, "high": 1}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3200, "high": 0}])
SAXT = S.track("サックス（トンネルの中）", "brass", patch="altoSax", volume=0.2, pan=0.08, gainDb=5, mono=True, fx=MUFF)
EP = [S.track(f"エレピ{i + 1}", "keys", volume=0.11, pan=[-0.35, 0.35, 0.0, -0.15][i], reverb=0.2, sustain=1.0) for i in range(4)]
EPT = [S.track(f"エレピ（トンネル{i + 1}）", "keys", volume=0.1, pan=0, fx=MUFF) for i in range(2)]
CUT = [S.track(f"ギターのカッティング{i + 1}", "guitar", **clean_gtr_spec(0.08, [0.55, -0.55][i])) for i in range(2)]
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("chiff", vol=0.16, pan=-0.08, delay=0.75, extra_fx=[{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}]))
BASS = S.track("ベース", "bass", **rock_bass_spec(0.21))
STR = [S.track(f"弦{i + 1}", "strings", patch="slowStrings", **strings_spec(0.07, [-0.55, 0.55][i])) for i in range(2)]
WAVE = S.track("波の音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.45, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- サックス（後ろにもたれたシンコペ） ----------
HOOK = ["R:0.5 5:0.5 7:0.75 1':0.25 2':1 7:1", "1':1.5 6:0.5 5:2", "R:0.5 3:0.5 5:0.75 6:0.25 b7:1 5:1", "4:3 R:1",
        "R:0.5 3':0.5 2':0.75 1':0.25 7:1 6:1", "5:1.5 b7:0.5 1':2", "R:0.5 6:0.5 1':0.75 2':0.25 3':1 1':1", "2':3 R:1"]
VERSE = ["R:1 3:0.75 5:0.25 7:1 6:1", "5:1.5 4:0.5 2:2", "R:1 5:0.75 6:0.25 1':1 b7:1", "6:2 R:2", "R:1 5:0.75 6:0.25 7:1 2':1", "1':1.5 6:0.5 4:2",
         "R:1 4:0.75 6:0.25 b2':1 1':1", "7:2 R:2"]
for i, b in enumerate(S.sc("窓を開ける")): SAX.bar(b, K.mel(HOOK[i], oct=4))
for i, b in enumerate(S.sc("海岸通り")):
    if i < 8: SAX.bar(b, K.mel(VERSE[i], oct=4))
    else: LEAD.bar(b, K.mel(VERSE[i % 8], oct=4 if i < 16 else 5)); SAX.bar(b, K.mel("R:3 5':0.5 3':0.5", oct=4) if i % 2 == 1 else "R:4")
for i, b in enumerate(S.sc("信号待ち")):
    if i in (1, 3, 5): SAX.bar(b, K.mel(["R:2 3':1 2':1", "R:2 1':1 7:1", "R:2 6:1 5:1"][(i - 1) // 2], oct=4))
for i, b in enumerate(S.sc("坂の上")):
    LEAD.bar(b, K.mel(["4:1 5:1 6:1 1':1", "7:3 R:1", "1':1 2':1 3':1 4':1", "5':4"][i % 4], oct=4 if i < 8 else 4))
    if i >= 8: SAX.bar(b, K.mel(["4:1 5:1 6:1 1':1", "7:3 R:1", "1':1 2':1 3':1 4':1", "5':4"][i % 4], oct=3))
for i, b in enumerate(S.sc("トンネル")):
    SAXT.bar(b, K.mel(["b3':2 2':1 1':1", "1':4", "6:2 5:1 4:1", "7:4"][i % 4], oct=4) if i % 2 == 0 or True else "R:4")
for i, b in enumerate(S.sc("海が見える")):
    SAX.bar(b, K.mel(HOOK[i % 8], oct=4 if i < 16 else 5))
    if i < 16: LEAD.bar(b, K.mel(["3':4", "2':2 1':2", "5:3 R:1", "6:4", "1':4", "b7:2 6:2", "1':3 2':1", "3':4"][i % 8], oct=4))
# 夕日: サックスのソロ（だんだん音が少なく）
SOLO = ["5':0.5 4':0.5 3':0.5 1':0.5 7:1 5:1", "6:1.5 1':0.5 3':2", "4':0.75 3':0.25 2':0.5 1':0.5 7:1 6:1", "5:4",
        "3':1 2':0.5 1':0.5 6:2", "5:3 R:1", "4:1 5:1 6:2", "5:4"]
for i, b in enumerate(S.sc("夕日")):
    SAX.bar(b, K.mel(SOLO[i % 8], oct=4) if i < 16 else K.mel(["3':4", "R:4", "2':4", "R:4", "1':4", "R:4", "R:4", "R:4"][i - 16], oct=4))
SAX.bar(S.sc("波")[4], K.mel("5:8", oct=4))       # 波の音の中のサックスの1音

# ---------- 伴奏 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 63, 4)
    if n == "波": continue
    if b in TUN:
        for j in range(2): EPT[j].bar(b, f"{nm(v[j], True)}:4")
    else:
        pat = "R:0.5 X:1 R:0.5 X:0.75 X:1.25" if n not in ("信号待ち", "夕日") else "X:4"
        if n == "夕日" and i >= 16: pat = "X:4" if i % 4 == 0 else "R:4"
        for j in range(4): EP[j].bar(b, pat.replace("X", nm(v[j], True)))
    if n in ("窓を開ける", "海岸通り", "海が見える", "坂の上"):
        g = voice(S.chords[b], 67, 2)
        for j in range(2): CUT[j].bar(b, f"R:0.5 {nm(g[j], True)}:0.75 R:0.75 {nm(g[j], True)}:0.5 R:0.5 {nm(g[j], True)}:0.75 R:0.25")
    if n in ("海が見える", "坂の上") and not (n == "坂の上" and i < 8):
        sv = voice(S.chords[b], 72, 2)
        for j in range(2): STR[j].bar(b, f"{nm(sv[j], True)}:4")
    r = low(S.chords[b], "E1")
    if n == "信号待ち": BASS.bar(b, f"{nm(r, True)}:4" if i % 2 == 0 else "R:4"); continue
    if n == "トンネル": BASS.bar(b, f"{nm(r, True)}:2 {nm(r + 7, True)}:2"); continue
    if n == "夕日" and i >= 16: BASS.bar(b, f"{nm(r, True)}:4" if i % 4 == 0 else "R:4"); continue
    BASS.bar(b, f"{nm(r, True)}:0.75 {nm(r, True)}:0.25 R:0.5 {nm(r + 12, True)}:0.5 R:0.5 {nm(r + 10, True)}:0.5 {nm(r + 7, True)}:0.5 {nm(r + 12, True)}:0.5")

# 波の音（ホワイトノイズのシュッを長く）
for i, b in enumerate(S.sc("波")):
    if i % 2 == 0: WAVE.bar(b, "A4:4")
for i, b in enumerate(S.sc("夕日")[16:]):
    if i % 4 == 2: WAVE.bar(b, "A4:4")
cym_swell(CYM, S.sc("海が見える")[0], 4, "E4")
cym_swell(CYM, S.sc("窓を開ける")[0] + 1, 1, "C4") if False else None

# ---------- ドラム（16ビートのはね。トンネルはこもったキックとスネアだけ） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("窓を開ける", "海岸通り", "海が見える", "坂の上"):
        put_groove(D, b, ("X.....x...X.....", "....X......oX..o", "XoxoXoxoXoxoXoxo" if n != "海岸通り" else "X.xoX.xoX.xoX.xo"), ghosts=0.6, seed=b, hat_vary=False)
        if i == 0 or (n == "海が見える" and i % 8 == 0): crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "small" if not last else "tomdown")
    elif n == "信号待ち":
        D.set(b, "." * 16, "." * 16, "x...x...x...x..." if i >= 4 else "." * 16)
    elif n == "トンネル":
        D.set(b, "X.........X.....", "....X.......X...", "." * 16)
        if last: D.set(b, "X.......X.......", "....X...xxXXXXXX", "." * 16)
    elif n == "夕日":
        if i < 16: put_groove(D, b, ("X.....x...X.....", "....X.......X...", "." * 16), ghosts=0.5, seed=b, hat_vary=False); D.cym(b, "D2:1 D2:1 D2:1 D2:1")
        elif i < 20: D.set(b, "X...............", "." * 16, "." * 16)

S.desc = ("仮: ボカロ曲のインスト25曲の22。シティポップ寄りの J-POP。E♭長調・112。主役の楽器はアルトサックス。夏の終わりの夕方、海沿いの国道を車で走る。"
          "窓を開けた瞬間に全員（サックスのフック）→海岸通り→信号待ち→坂の上→トンネル（全部の楽器の高い音を削った、こもった音）→抜けた瞬間の海（最大）→"
          "夕日（サックスのソロが、だんだん少なく）→波の音とサックスの1音。メジャー7th のシンコペーション。自作")
S.write()
