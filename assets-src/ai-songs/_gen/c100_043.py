# ケルト・フルート100曲「銀の笛と百の夜」043 塔の鐘守 The Bell-Keeper of the Tower — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 石の輪の先に、古い塔が立っている。塔のてっぺんには鐘があり、年老いた鐘守がひとりで住んでいる。
#   鐘守は若い日の祖父を知っていた。エイラが笛で問いかけると、鐘守は低い声（チェロ）で、ゆっくりと昔の話を返す。
#   ふたりの話は、ときに重なり、最後に鐘守が鐘をひとつ鳴らす。その余韻の中で、エイラは祖父の秘密の入口を知る。
# 調べ: 悲しみ。形: 対話（笛とチェロ＝鐘守の声。4小節ずつ交互に話し、回想ではチェロが長く語り、最後は3度で寄りそう）。
# 拍子・速さ: 6/8・付点4分＝46（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: A エオリア。
# 主役は笛（エイラの笛）。伴奏の主役: チェロ（人の声として旋律で答える）。脇: 遠い鐘（始まりと終わりの1音ずつ）と、ごく小さいコントラバスの持続。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 100曲の中で、笛以外が旋律を歌うのは、この曲のチェロだけ。
# 始まり: 遠い鐘の1音 → 終わり: 鐘の余韻。
# 山: 前半に1つ（対話1の終わり）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 46
S = Song("C100", "043-the-bell-keeper", "塔の鐘守", "The Bell-Keeper of the Tower", BPM, 2, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
K = Key("A", "minor", 4); KL = Key("A", "minor", 3)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CH8 = ["Am", "Em", "F", "C", "Dm", "Am", "E", "Am"]
SC = [("鐘", 2, "intro", ["Am", "Am"]), ("対話1", 32, "chorus", CH8 * 4), ("対話2", 32, "verse", CH8 * 4), ("回想", 16, "verse", CH8 * 2),
      ("寄りそう", 16, "verse", CH8 * 2), ("鐘の余韻", 4, "outro", ["Am"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("鐘", 0, 0.66), ("対話1", 0, 0.72), ("対話1", 24, 0.84), ("対話1", 31, 0.78), ("対話2", 0, 0.72), ("回想", 0, 0.68), ("寄りそう", 0, 0.72),
          ("鐘の余韻", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="鐘", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: チェロ（0.025・gainDb 2）は笛と同じくらい（声として丁度よい）。鐘は打った所で笛より少し小さく、長く減衰する
VC = S.track("チェロ（鐘守の声）", "strings", patch="cello", volume=0.025, gainDb=2, pan=-0.2, reverb=0.6, release=0.4, barGain=[round(x * 1.4, 3) for x in G])
BELL = S.track("遠い鐘", "bell", volume=0.12, pan=0.3, reverb=0.9, barGain=[1.2] * c.NB)
CB = S.track("コントラバス（ごく小さい持続）", "strings", patch="contrabass", volume=0.02, pan=0.05, reverb=0.6, release=0.6, barGain=G)

F = [["5:3 4:2 3:1", "2:3 1:3", "3:2 4:1 5:2 6:1", "5:6"], ["1':3 7:2 6:1", "5:3 3:3", "4:2 3:1 2:2 1:1", "2:6"],
     ["3:2 5:1 1':3", "7:2 6:1 5:3", "6:2 5:1 4:2 2:1", "3:6"], ["5:2 4:1 3:2 2:1", "1:3 7,:3", "1:2 2:1 3:2 4:1", "1:6"]]
C = [["1:3 2:2 3:1", "4:3 3:3", "2:2 1:1 7,:2 6,:1", "7,:6"], ["3:3 4:2 5:1", "6:3 5:3", "4:2 3:1 2:3", "1:6"],
     ["5:2 4:1 3:3", "2:2 3:1 4:3", "3:2 2:1 1:2 7,:1", "1:6"], ["6:3 5:3", "4:2 3:1 2:3", "3:2 4:1 2:2 7,:1", "1:6"]]
def say(track, bars, b0, key, oct_, dens, seed, mk=""):
    ev = []
    for j, s_ in enumerate(e2b(bars)):
        ev += mel_events(key, s_, oct_, (b0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    if track is c.FLUTE: play(track, ornament(ev, key, BPM, "air", B, density=dens, seed=seed))
    else: play(track, [(t, L, m, mk) for t, L, m in ev])

# 対話1・2：笛4小節 → チェロ4小節（チェロの答えは、笛の最後の小節に半分重なって入る）
for sc, d in (("対話1", 0.3), ("対話2", 0.2)):
    s0 = c.s0[sc]
    for q in range(4):
        say(c.FLUTE, F[(q + (sc == "対話2")) % 4], s0 + 8 * q, K, 4, d, 4300 + q + len(sc))
        say(VC, C[(q + (sc == "対話2")) % 4], s0 + 8 * q + 4, KL, 3, 0, 0)
# 回想：鐘守（チェロ）が長く語り、笛は長い音で聞く
s0 = c.s0["回想"]
say(VC, C[1] + C[2] + C[3] + C[0], s0, KL, 3, 0, 0)
say(c.FLUTE, ["5:6", "4:6", "3:6", "2:6", "1:6", "7,:6", "1:6", "3:6", "4:6", "3:6", "2:6", "1:6", "2:6", "3:6", "2:6", "1:6"], s0, K, 4, 0.0, 4310)
# 寄りそう：同じ節を、笛とチェロが3度（10度）で一緒に
s0 = c.s0["寄りそう"]
for q in range(2):
    say(c.FLUTE, F[3] + F[0], s0 + 8 * q, K, 4, 0.2, 4320 + q)
    ev = []
    for j, s_ in enumerate(e2b(F[3] + F[0])):
        ev += mel_events(K, s_, 4, (s0 + 8 * q + j) * B)
    play(VC, [(round(t, 4), L, (m - 15 if m - 15 >= 45 else m - 3), "") for t, L, m in ev])     # 10度下（チェロの声で）
# 鐘：始まりと終わりに1音ずつ（遠く、長い余韻）
BELL.at(0.0, "A4:4"); BELL.at(c.s0["鐘の余韻"] * B, "A4:8")
# コントラバス：ごく小さく、A と E（2小節ずつ）
for b in range(2, c.s0["鐘の余韻"], 2):
    CB.at(b * B, f"{'A1' if S.chords[b] in ('Am', 'F', 'Dm') else 'E2'}:4,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の043（第3版）。古い塔の鐘守と、エイラの対話。6/8・付点4分＝46、A エオリア。エイラの笛が問いかけ、鐘守はチェロの低い声で、ゆっくりと若い日の祖父の話を返す（100曲の中で、笛以外が旋律を歌うのはこの曲のチェロだけ）。回想ではチェロが長く語り、最後は笛とチェロが同じ節で寄りそう。始まりと終わりは、遠い鐘の1音と、その余韻。",
       harm_scenes=None, tail_scene="鐘の余韻", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.32, "lp": 2600, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air043.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
