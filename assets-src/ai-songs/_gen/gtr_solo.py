# ギター1本だけの曲（仮）。人間（2026-11-15）:「ギター単体の曲頂戴」
# 96・G長調・16小節＋終わり（45秒）。ドラム・ベース・歌なし。ギターは1本（弦1本ずつ6つのパートに分けて書くが、同じ設定なので1本のギターとして鳴る）。
#   1〜4小節: 指でつまびく（1拍目に低い弦、あとは高い弦を順に。音は鳴らしたまま）
#   5〜12小節: かき鳴らし（学んだ弾き方: 押さえ方の形・毎回ちがう弦の数・8分はダウン・16分ウラだけアップ）。8小節目と12小節目は、和音のあいだを単音でつなぐ
#   13〜16小節: 1拍目だけ鳴らして、つまびきに戻る → 最後は G をゆっくり下ろして鳴らしっぱなし
# 使い方: GT=clean|crunch python3 gtr_solo.py <出力.json>
from vocalo_lib import *
import random as _r
GT = os.environ.get("GT", "clean")
S = Song("96", f"gtr-solo-{GT}", f"ギター1本の曲（{'クリーン' if GT == 'clean' else '浅い歪み'}・仮）", "solo guitar", 96, 4, "G", "major", "ギター1本")
S.kit = "naked-x"; S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
CH = ["G", "Em7", "C", "Dsus4|D", "G", "D", "Em", "C", "G", "D", "C", "Dsus4|D", "Em", "C", "G", "D"]
S.scene("曲", 16, "verse", CH); S.scene("おわり", 2, "outro", ["G", "G"])
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
BASE = dict(sustain=1.6, release=0.25, chorus=0, humanPitch=0, noScoop=True, powerChord=False, di="emily", stringNoise=True)
SPEC = dict(BASE, amp="jpopClean", ampDrive=0.1) if GT == "clean" else dict(BASE, amp="namJVM2", ampDrive=0.45, ampGate=10, ampTight=0.3, ampTightHz=110, ampCabIr="dd-v30-2x12-mix-balanced")
FX = [{"type": "filter", "kind": "highpass", "freq": 80, "q": 0.7}, {"type": "eq", "low": 0, "mid": -1.5, "midHz": 300, "high": 0.5}, {"type": "room", "mix": 0.14}, {"type": "plate", "mix": 0.08}]
G6 = [S.track(f"ギター{i + 1}弦め", "distGuitar", volume=0.1, pan=0, fx=FX, **SPEC) for i in range(6)]
rr = _r.Random(11); N = lambda m: nm(m)


def pick(b, ch, order, at=0.0, step=0.5, ring=2.0, mark=""):
    """つまびき: order の順に、弦を1本ずつ鳴らす（鳴らしたまま。同じ弦を次に弾くまで）"""
    v = gtr_shape(ch); t = at
    for k, j in enumerate(order):
        j = min(j, len(v) - 1); nxt = next((q for q in range(k + 1, len(order)) if min(order[q], len(v) - 1) == j), None)
        L = (nxt - k) * step if nxt is not None else ring
        G6[j].at(S.bar_beat(b) + t, f"{N(v[j])}:{L:g}{'!' if k == 0 else mark}"); t += step


def run(b, notes, at, step=0.5):
    """単音でつなぐ（低い弦で）"""
    for k, n in enumerate(notes): G6[1].at(S.bar_beat(b) + at + k * step, f"{n}:{step:g}")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); c = S.chords[b].split("|")
    if n == "おわり":
        if i == 0: gtr_strum(G6, S, b, "x---------------", "G", rr, lag_ms=38)      # ゆっくり下ろす
        continue
    if i < 4:
        if len(c) == 1: pick(b, c[0], [0, 2, 3, 4, 5, 4, 3, 2])
        else: pick(b, c[0], [0, 2, 3, 4], ring=1.0); pick(b, c[1], [0, 3, 4, 3], at=2.0)
    elif i < 12:
        j = i - 4; pats = ["x---x-.xx-x-x-.x", "x-.xx-x-x-.xx-x-", "x---x-.xx-x-.xx-", "x-.xx-x-x-x-...."]
        if len(c) == 1:
            gtr_strum(G6, S, b, pats[j % 4], c[0], rr, drive=False)
            if j % 4 == 3: run(b, [N(low(c[0], "E2") + 2), N(low(c[0], "E2") + 4)] if j == 3 else ["B2", "A2"], 3.0)      # 和音のあいだを単音でつなぐ
        else:
            gtr_strum(G6, S, b, "x---x-.x........", c[0], rr, drive=False); gtr_strum(G6, S, b, "........x-x-x---", c[1], rr, drive=False)
    else:
        gtr_strum(G6, S, b, "x-------........", c[0], rr, drive=False, lag_ms=16); pick(b, c[0], [3, 4, 5, 4], at=2.0, ring=1.0, mark=",")
S.fade_out = 0; S.desc = "仮: ギター1本だけの曲（45秒）。和音の弾き方の聞きくらべ用"
finish(S, LY, V, 0)
from vt3x_lib import *
path = sys.argv[1]; js = load(path); gtr_velocity(js, "ギター", 5, strong=(90, 102), mid=(72, 84), weak=(56, 68)); save(path, js)
