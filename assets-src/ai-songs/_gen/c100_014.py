# ケルト・フルート100曲「銀の笛と百の夜」014 迷い羊 The Stray Lamb — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 放牧小屋の朝のあと、1匹の子羊が群れからはぐれる。エイラが笛で追いかけると、子羊は右へ左へ跳ねて逃げる。
#   森に入って見失い、また見つけて追いかけ、最後に子羊が立ち止まって、笛と同じ足どりで並んで帰る。
# 調べ: あいだ（明るくも暗くもない、いたずらっぽい）。形: 追いかけっこ（笛が追うと旋律が逃げる）。
# 拍子・速さ: 6/8・付点4分＝96。子羊（ピチカート）は 3+3 で跳ね、追う笛は 2+2+2（3拍子の感じ）で走る＝拍がずれる。
#   見つけた瞬間から、笛も 3+3 になって拍がそろう。旋法: F♯ エオリア。
# 主役は笛（追う笛。子羊の句を半小節おくれて追う）。伴奏の主役: ピチカート（子羊。左・中・右と跳ぶ場所が変わる）。
#   脇: コントラバスとチェロのピチカート（地面）。竪琴・ギター・ピアノ・パッド・打楽器・長い弦の和音は使わない。
# この曲だけ: 逃げる旋律と追う笛がずれた拍子で動き、見つけた瞬間に拍がそろう。
# 始まり: ピチカートだけ（子羊の足あと）→ 終わり: 見つけて全員がそろい、同じ足どりで1拍。
# 山: 終盤に1つ（見つけた）。最初が大きく、だんだん小さくなる形にはしない。
# 書き方: 1拍＝付点4分（♩.=96）、1小節＝2拍。旋律は8分＝1で書き、e2b で 1/3 拍に直す（011 と同じ）。
import sys, json, re
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2

BPM = 96
S = Song("C100", "014-the-stray-lamb", "迷い羊", "The Stray Lamb", BPM, 2, "F#", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("F#", "minor", 4)
T3 = 1 / 3
def e2b(s_):
    return " ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split())

CA = ["F#m", "E", "D", "F#m"]; CB = ["D", "E", "C#m", "F#m"]
LEN = {"足あと": 8, "追いかけ": 48, "森の中": 32, "また見つけた": 56, "並んだ": 40, "帰り道": 8}
for n, L in LEN.items():
    S.scene(n, L, {"並んだ": "chorus", "足あと": "intro", "帰り道": "outro"}.get(n, "verse"), ((CA + CB) * 20)[:L])
NAMES = list(LEN)
c = make(S, NAMES,
         [("足あと", 0, 0.62), ("追いかけ", 0, 0.68), ("追いかけ", 47, 0.78), ("森の中", 0, 0.62), ("森の中", 31, 0.68),
          ("また見つけた", 0, 0.74), ("また見つけた", 55, 0.84), ("並んだ", 0, 0.9), ("並んだ", 39, 0.94), ("帰り道", 0, 0.82), ("帰り道", 7, 0.74)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足あと", passing=True, tension=False)
B = S.beats

# 子羊（ピチカート）：左・中・右の3か所。句ごとに跳ぶ場所を変える
# 1回目（7.53）: 試し書き出しでピチカートは笛より約10dB小さく、子羊だけの足あとが -45dB に沈んだ → gainDb 6、足あとはさらに ×1.6。2回目（7.59）も足あとが -34dB と本編より 12dB 小さかったので ×2.5
LAMB = [S.track(f"子羊（ピチカート・{nm_}）", "strings", patch="pizzicato", volume=0.12, gainDb=6, pan=p, reverb=0.35,
                barGain=[round(x * (2.5 if b < 8 else 1.0), 3) for b, x in enumerate(c.g())])
        for nm_, p in (("左", -0.6), ("中", 0.05), ("右", 0.6))]
CBP = S.track("コントラバス（ピチカート）", "strings", patch="contrabass", volume=0.08, gainDb=4, pan=0.0, reverb=0.3, sustain=0.5, barGain=c.g())
VCP = S.track("チェロ（ピチカート）", "strings", patch="pizzicato", volume=0.1, pan=-0.15, reverb=0.35, barGain=c.g())

# ---------- 子羊の旋律（3+3 で跳ねる。8分＝1、1小節＝6） ----------
SA = ["1:2 3:1 5:2 4:1", "3:1 4:1 5:1 7:3", "6:2 5:1 4:2 3:1", "2:1 3:1 4:1 1:3"]
SB = ["5:1 6:1 7:1 1':2 7:1", "6:2 4:1 5:3", "3:1 5:1 7:1 6:2 5:1", "4:1 2:1 7,:1 1:3"]
SC = ["3:1 R:1 3:1 5:1 R:1 5:1", "7:2 R:1 6:2 R:1", "4:1 5:1 6:1 5:1 4:1 3:1", "2:3 R:3"]       # 跳ねて止まる（振り返る）
LAMB_PH = [SA, SB, SA, SC]

# ---------- 追う笛（2+2+2 で走る。2小節＝12） ----------
FL = ["1:2 3:2 5:2 4:2 3:2 2:2", "5:2 6:2 7:2 1':2 7:2 5:2", "4:2 5:2 6:2 5:2 4:2 3:2", "2:2 3:2 4:2 3:2 2:4",
      "3:2 5:2 7:2 6:2 5:2 4:2", "1':4 7:2 6:2 5:4", "6:2 4:2 2:2 3:2 4:2 5:2", "4:2 3:2 2:2 7,:2 1:4"]
FOREST = ["1:8 2:2 3:2", "5:8 4:2 3:2", "2:8 7,:2 1:2", "3:12",                         # 1回目は句の中の休みで -53dB まで沈んだ → 休みをのばす音に                         # 森：見失って、低く長く呼ぶ
          "5:4 4:2 3:6", "6:6 5:2 4:4", "3:4 2:4 1:4", "7,:10 1:2"]

def put(track, s_, oct_, start_beat, key=K, orn=None):
    ev = mel_events(key, e2b(s_), oct_, start_beat)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    if orn is not None:
        ev = _v2.ornament(ev, key, BPM, "march", B, density=orn[0], seed=orn[1])
    else:
        ev = [(t, L, m, "") for t, L, m in ev]
    play(track, ev)

def lamb_phrase(b0, ph, oct_, hop, dens=None):
    """子羊の4小節。1小節ごとに左右へ跳ぶ（hop=跳び始めの場所）"""
    for j, s_ in enumerate(ph):
        put(LAMB[(hop + j) % 3], s_, oct_, (b0 + j) * B)

# 足あと：子羊だけ（左→中→右と跳ぶ）
s0 = c.s0["足あと"]
lamb_phrase(s0, SA, 5, 0); lamb_phrase(s0 + 4, SC, 5, 2)

# 追いかけ：子羊は高い所で 3+3。笛は半小節おくれて 2+2+2 で追う（拍がずれる）
s0 = c.s0["追いかけ"]
for q in range(12):
    lamb_phrase(s0 + 4 * q, LAMB_PH[q % 4], 5, q)
for q in range(24):
    st = (s0 + 2 * q) * B + 1          # 半小節（付点4分1つ）おくれて
    if st + 4 > (s0 + LEN["追いかけ"]) * B: break
    put(c.FLUTE, FL[q % 8], 4, st, orn=(0.25 + 0.3 * q / 24, 1400 + q))

# 森の中：子羊は時々、遠くで1〜2音だけ（見失う）。笛は低く長く呼ぶ
s0 = c.s0["森の中"]
for q in range(8):
    # 2回目まで、句（2小節）を4小節ごとに置いていたので2小節ずつ笛が消えて -50dB に沈んだ → 長さを倍にして4小節を埋める（低く長く呼ぶ）
    slow = " ".join(f"{t.split(':')[0]}:{float(t.split(':')[1]) * 2:g}" for t in FOREST[q].split())
    put(c.FLUTE, slow, 4, (s0 + 4 * q) * B, orn=(0.35, 1500 + q))
    b = s0 + 4 * q + 2
    put(LAMB[(q * 2) % 3], ["R:3 5:1 R:2", "R:1 3:1 R:4", "R:4 7:1 R:1", "R:2 1':1 R:3"][q % 4], 5, b * B)

# また見つけた：子羊は低い所へ逃げる。笛は高い所から、もっと近く（1拍＝付点4分の半分＝8分3つおくれ）で追う
s0 = c.s0["また見つけた"]
for q in range(14):
    lamb_phrase(s0 + 4 * q, LAMB_PH[(q + 1) % 4], 4, 2 * q)
for q in range(28):
    st = (s0 + 2 * q) * B + 0.5 + (0.5 if q < 14 else 0)           # 後半は差が詰まる（追いつきそう）
    if st + 4 > (s0 + LEN["また見つけた"]) * B: break
    put(c.FLUTE, FL[(q + 3) % 8], 5 if q % 8 < 4 else 4, st, orn=(0.45 + 0.3 * q / 28, 1600 + q))

# 並んだ（山）：見つけた瞬間、笛も 3+3 になり、子羊と同じ旋律を1オクターブ上で、同じ拍で
s0 = c.s0["並んだ"]
for q in range(10):
    ph = [SA, SB, SA, SB, SA, SB, SC, SB, SA, SB][q]
    for j, s_ in enumerate(ph):
        for i in range(3):                                           # 子羊は真ん中に来る（3か所そろって鳴る）
            if i == 1 or q >= 2: put(LAMB[i], s_, 4, (s0 + 4 * q + j) * B)
    for j, s_ in enumerate(ph):
        put(c.FLUTE, s_, 5, (s0 + 4 * q + j) * B, orn=(0.6, 1700 + 4 * q + j))

# 帰り道：同じ足どりで、ゆっくり主音へ
s0 = c.s0["帰り道"]
for j, s_ in enumerate(["5:2 4:1 3:2 2:1", "1:3 3:3", "5:6", "1:6", "R:6", "R:6", "R:6", "R:6"]):
    put(c.FLUTE, s_, 5, (s0 + j) * B)
for j, s_ in enumerate(["5:2 4:1 3:2 2:1", "1:3 3:3", "5:3 R:3", "1:3 R:3"]):
    put(LAMB[1], s_, 4, (s0 + j) * B)

# ---------- 地面：コントラバスとチェロのピチカート（1拍目と2拍目に根音と5度） ----------
ROOT = {"F#m": 42, "E": 40, "D": 38, "C#m": 37}
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    if n == "足あと": continue
    if n == "森の中":
        if i % 2 == 0: CBP.bar(b, f"{nm(r)}:{round(2 * T3, 4)} R:{round(4 * T3, 4)}")
        continue
    if n == "帰り道":
        if i < 4: CBP.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1")
        elif i == 4: CBP.bar(b, f"{nm(42)}:2")
        continue
    CBP.bar(b, f"{nm(r)}:{round(2 * T3, 4)} R:{round(T3, 4)} {nm(r + 7)}:{round(2 * T3, 4)} R:{round(T3, 4)}")
    if n == "並んだ" or (n == "また見つけた" and i >= 28):
        VCP.bar(b, f"{nm(r + 12)}:{round(T3, 4)} R:{round(2 * T3, 4)} {nm(r + 19)}:{round(T3, 4)} R:{round(2 * T3, 4)}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の014（第3版）。群れからはぐれた子羊を、エイラの笛が追いかける。6/8・付点4分＝96、F♯ エオリア。子羊（ピチカート）は 3+3 で左右に跳ねて逃げ、追う笛は 2+2+2 で半小節おくれて走るので、拍がずれたまま進む。森で見失い、また見つけて追い、最後に笛も 3+3 になって子羊と同じ旋律を同じ拍で弾き、並んで帰る。",
       harm_scenes=None, tail_scene="帰り道", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.5, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.22, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air014.json", "w"), ensure_ascii=False)

# 1/3 拍を丸めてできる「R:0」を取りのぞく（010・011 と同じ）
_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
