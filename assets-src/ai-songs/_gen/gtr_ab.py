# ギターの音の聞きくらべ（同じ8小節・同じ和音を、音の作り方と弾き方だけ変えて鳴らす）。仮。歌なし。
# 人間（2026-11-15）:「あとギターの音毎回思うけどどうにかならないかな。」→ どこが嫌かをしぼるための聞きくらべ。
# 使い方: GV=A|B|C|D python3 gtr_ab.py <出力.json>
#   A: 今の 16 と同じ（ハイゲインアンプのモデルを浅く・3本の弦を同時に鳴らす・全部同じ強さ）
#   B: マーシャルを学習したモデル（浅めの歪み）＋ かき鳴らし（弦を低い方から少しずつずらす・ウラは上から・1音ずつ強さを変える）
#   C: B と同じ弾き方で、歪みを深く（サビの壁向き）
#   D: クリーン寄り（J-POP のクリーン）で、同じかき鳴らし
from vocalo_lib import *
import random as _r
GV = os.environ.get("GV", "A")
S = Song("95", f"gtr-{GV.lower()}", f"ギターの聞きくらべ{GV}（仮）", f"guitar test {GV}", 200, 4, "F", "major", "ギターの聞きくらべ")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}
CH = ["F", "Am", "Bb", "Bbm", "F", "Dm", "Gm", "C"]
S.scene("サビ", 8, "chorus", CH); S.scene("おわり", 1, "outro", ["F"])
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False); LY = Lyrics(S)
BASE = {"sustain": 1.3, "release": 0.12, "chorus": 0, "humanPitch": 0, "noScoop": True, "powerChord": False}
SPEC = {"A": None,
        "B": dict(BASE, di="emily", stringNoise=True, amp="namJVM2", ampDrive=0.55, ampGate=12, ampTight=0.4, ampTightHz=120, ampCabIr="dd-v30-2x12-mix-balanced"),
        "C": dict(BASE, di="emily", stringNoise=True, amp="namJVM", ampDrive=0.8, ampGate=14, ampTight=0.5, ampTightHz=130, ampCabIr="dd-v30-2x12-mix-balanced"),
        "D": dict(BASE, di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12)}[GV]
FX = [{"type": "filter", "kind": "highpass", "freq": 90, "q": 0.7}, {"type": "eq", "low": 0, "mid": -2, "midHz": 300, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 1500, "high": 0.5}, {"type": "room", "mix": 0.08}]
def mk(name, vol, pan, i):
    if GV == "A": return S.track(f"{name}{i + 1}", "distGuitar", **rock_gtr_spec(vol, pan, drive=0.4))
    return S.track(f"{name}{i + 1}", "distGuitar", volume=vol, pan=pan, fx=FX, **SPEC)
GL = [mk("Lギター", 0.05, -0.6, i) for i in range(4)]; GR = [mk("Rギター", 0.047, 0.6, i) for i in range(4)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.22)); D = S.drumkit(); N = lambda m: nm(m); rr = _r.Random(7)
LAG = 0.014 * 200 / 60        # 弦から弦へ 14ミリ秒（拍に直す）


def strum(tracks, b, pat, notes):
    """かき鳴らし: pat の x ごとに、表（8分の頭）は低い弦から、ウラは高い弦から、少しずつずらして鳴らす。強さは表を強く・1音ずつゆらす"""
    n = len(notes)
    for j in range(n):
        out = []; t = 0.0; k = 0; i = 0; p = pat
        while i < len(p):
            c = p[i]; e = i + 1
            while e < len(p) and p[e] == ("-" if c == "x" else "."): e += 1
            L = (e - i) * 0.25
            if c == "x":
                down = (i % 4) == 0 or (i % 4) == 3; order = j if down else (n - 1 - j)
                if GV == "A": out.append((i * 0.25, L, f"{notes[j]}:{L:g}"))
                else:
                    out.append((i * 0.25 + order * LAG, max(0.1, L - order * LAG), f"{notes[j]}:{max(0.1, L - order * LAG):.3f}{'!' if i % 4 == 0 else ''}"))
            i = e
        for st, L, tok in out: tracks[j].at(S.bar_beat(b) + st, tok)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]; pw = power(ch, "F2"); r = low(ch, "C3"); up = tones(ch, nm(r + 1), nm(r + 16))[:3]
    lv = [N(x) for x in (pw + [pw[0] + 12])[:4]]; rv = [N(x) for x in ([r] + up)[:4]]
    if n == "サビ":
        strum(GL, b, "x-x-x-x-x-x-x-x-" if i % 2 == 0 else "x-x-x-x---x-x-x-", lv)
        strum(GR, b, "x-.x-.x-x-.x-.x-" if i % 2 == 0 else "x-.x-.x---x-.x-.", rv)
        BASS.bar(b, steps("x-x-x-x-x-x-x-x-", [N(low(ch, "F1"))]))
        feel(D, b, "quarter", k="X.......X......." if i % 2 == 0 else "X.....X...X.....")
        if i == 0: crash(D, b, "C2", 4)
        if i == 7: fill_cresc(D, b, 1, toms=False)
    else:
        strum(GL, b, "x---------------", lv); strum(GR, b, "x---------------", rv); BASS.bar(b, steps("x-----------....", [N(low(ch, "F1"))])); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
S.fade_out = 0; S.desc = f"仮: ギターの音の聞きくらべ{GV}"
finish(S, LY, V, 0)
from vt3x_lib import *
path = sys.argv[1]
if GV != "A": humanize(path, "Lギター", mid=86, down=12, up=8, seed=3); humanize(path, "Rギター", mid=82, down=14, up=10, seed=4)      # 1音ずつ強さをゆらす
js = load(path); drum_punch(js); save(path, js)
