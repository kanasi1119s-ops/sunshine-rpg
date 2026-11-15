# ギター1本だけのロック調の曲（仮）。人間（2026-11-15）:「ミュートの効かせ方を少し柔らかくして、ちょっとロック調にして試しにギター単体で作って」
# 126・E短調／G長調・16小節＋終わり（35秒）。ドラム・ベース・歌なし。音はマーシャルを学習したモデルの浅めの歪み。
# ミュートを柔らかくするためにしたこと:
#   ① 音の切れ際を長くした（release 0.25 → 0.55。パッと消えず、すっと引く）
#   ② かき鳴らしの型から「休み」をなくした（音は次のストロークまで鳴らす。止めるのは場面の変わり目だけ）
#   ③ 手のひらのミュート（パームミュート）は「light」（いちばん浅い）にして、音を短くしすぎない（8分いっぱいの9割）。低い弦2本だけ・弱めに弾く
#   ⑤ v2: 歪ませた音で5〜6本の弦をかき鳴らす場面は音質の点数が 6.1〜6.2 と低かった（ミュートのリフの場面は 7.35）。歪みでは弦を3〜4本（根音・5度・オクターブ、ときどき3度）にしぼった
#   ④ ミュートの刻みだけを続けない。開いた和音（鳴らしっぱなし）→ ミュートの刻み → 開いた和音、と交互に置く
from vocalo_lib import *
import random as _r
S = Song("97", "gtr-rock", "ギター1本のロック調の曲（仮）", "solo rock guitar", 126, 4, "E", "minor", "ギター1本（ロック調）")
S.kit = "naked-x"; S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
CH = ["Em", "C", "G", "D", "Em", "C", "G", "Dsus4|D", "C", "D", "Em", "Em", "C", "D", "G", "G"]
S.scene("曲", 16, "verse", CH); S.scene("おわり", 2, "outro", ["Em", "Em"])
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
AMP = dict(di="emily", stringNoise=True, amp="namJVM2", ampDrive=0.6, ampGate=10, ampTight=0.35, ampTightHz=110, ampCabIr="dd-v30-2x12-mix-balanced", chorus=0, humanPitch=0, noScoop=True, powerChord=False)
FX = [{"type": "filter", "kind": "highpass", "freq": 85, "q": 0.7}, {"type": "eq", "low": 0, "mid": -2, "midHz": 300, "high": 0}, {"type": "eq", "low": 0, "mid": 1.5, "midHz": 1500, "high": 0.5}, {"type": "room", "mix": 0.12}]
G6 = [S.track(f"ギター{i + 1}弦め（開いた音）", "distGuitar", volume=0.1, pan=0, fx=FX, sustain=1.6, release=0.55, **AMP) for i in range(6)]
PM = [S.track(f"ギター{i + 1}弦め（やわらかいミュート）", "distGuitar", volume=0.085, pan=0, fx=FX, sustain=0.95, release=0.4, palmMute="light", **AMP) for i in range(2)]
rr = _r.Random(21); N = lambda m: nm(m)


def chug(b, ch, pat):
    """やわらかいミュートの刻み: 低い弦2本（根音と5度）。8分いっぱいの9割の長さ。拍の頭だけ少し強く"""
    v = gtr_shape(ch)[:2]; pat = pat.replace(" ", "")
    for i, c in enumerate(pat):
        if c != "x": continue
        e = i + 1
        while e < len(pat) and pat[e] == "-": e += 1
        L = (e - i) * 0.25 * 0.9
        for j in range(2): PM[j].at(S.bar_beat(b) + i * 0.25 + j * 0.006 * S.bpm / 60, f"{N(v[j])}:{L:.3f}{'' if i % 4 == 0 else ','}")


def run(b, notes, at, step=0.5):
    for k, n in enumerate(notes): G6[1].at(S.bar_beat(b) + at + k * step, f"{n}:{step:g}")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); c = S.chords[b].split("|")
    if n == "おわり":
        if i == 0: gtr_strum(G6, S, b, "x---------------", "Em", rr, lag_ms=30)
        continue
    if i < 4:        # リフ: 開いた和音を1発（2拍鳴らす）→ やわらかいミュートの刻み → 4拍目のウラで開いた和音（次の小節へ食う）
        gtr_strum(G6, S, b, "x-------......x-", c[0], rr, strings=4); chug(b, c[0], "........x-x-x-..")
    elif i < 8:      # かき鳴らし（休みなし。8分はダウン、16分のウラだけアップ）
        pats = ["x-x-x-xxx-x-x-xx", "x-x-xxx-x-x-x-xx", "x-x-x-xxx-xxx-x-", "x-x-x-x-x-x-x---"]
        if len(c) == 1: gtr_strum(G6, S, b, pats[i - 4], c[0], rr, strings=3)
        else: gtr_strum(G6, S, b, "x-x-x-xx........", c[0], rr, strings=3); gtr_strum(G6, S, b, "........x-x-x---", c[1], rr, strings=4)
    elif i < 12:     # だんだん強く: 1拍目だけ開いた和音、あとはやわらかいミュート。4小節目は開いた和音を8分で
        if i < 11: gtr_strum(G6, S, b, "x---............", c[0], rr, strings=4); chug(b, c[0], "....x-x-x-x-x-x-")
        else: gtr_strum(G6, S, b, "x-x-x-x-x-x-x-x-", c[0], rr, strings=4)
    else:            # 大きく鳴らす: 3・3・2 で開いた和音を鳴らしっぱなし。最後の小節は単音で下りる
        if i < 15: gtr_strum(G6, S, b, "x-----x-----x---", c[0], rr, lag_ms=12, strings=4)
        else: gtr_strum(G6, S, b, "x-------........", c[0], rr, strings=4); run(b, ["G3", "F#3", "D3", "B2"], 2.0)
S.fade_out = 0; S.desc = "仮: ギター1本だけのロック調の曲（35秒）。ミュートをやわらかく"
finish(S, LY, V, 0)
from vt3x_lib import *
path = sys.argv[1]; js = load(path); gtr_velocity(js, "開いた音", 5); gtr_velocity(js, "やわらかいミュート", 6, strong=(78, 88), mid=(78, 88), weak=(62, 72)); save(path, js)
