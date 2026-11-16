# 17「放課後タッピング」を作り直すためのスケッチ（サビだけ20〜30秒・3方向）。仮。
# 人間（2026-11-16）:「1と2両方やろう」→ 2＝学んだ型の引き出し（docs/sound/karte/library.md）を使って次の曲を作る。進め方は「スケッチを3方向 → 選んでもらう → 1曲にする」。
# 使い方: SK=G|H|I VB_VOCAL=1 python3 sk17_tapping.py <出力.json>
#   G「タッピングが歌うマスロック」150・E長調 … クリーンのギターが16分で細かく歌い、歌の句の間に答える。ドラムは止めたり食ったりする
#   H「リフ1本のガレージ・ロックンロール」132・A（♭VII・♭III を使う）… 歌は短く叫んで、すぐ休む。あいた所でリフが答える。手びょうし
#   I「静けさから壁になるポストロック」92・D長調 … やまびこのかかったクリーンのギターと長い歌 → 後半で歪んだギターの壁
# 引き出し（ロック9曲）から: ベースは1小節 3〜4音・根音 6割・動くときはとなりの音へ／根音は1小節に 1.0〜1.4回変わる／歌は休みを多く（お手本 23〜70%。自分は 19% だった）／ビブラートを深く（お手本 15〜30セント）
# 歌詞: 中心の言葉を言いかえる（ギターの弦＝六本の川、新しい曲＝名前のない鳥、部室＝夕焼けの実験）
from vocalo_lib import *
import random as _r
SK = os.environ.get("SK", "G")
CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 1}, {"type": "room", "mix": 0.1}]

if SK == "G":
    S = Song("17", "sk-g", "放課後タッピング スケッチG（仮）", "After School Tapping sketch G", 150, 4, "E", "major", "マスロック（スケッチ）")
    S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.1"; K = Key("E", "major"); SC = {4, 6, 8, 9, 11, 1, 3}
    CH = ["A", "B", "G#m7", "C#m", "F#m7", "B", "E", "E|B"]
    S.scene("前奏", 4, "intro", ["E", "E|B", "C#m", "A|B"]); S.scene("サビ", 8, "chorus", CH); S.scene("おわり", 1, "outro", ["E"])
    PT = ["x-x-xx-x--x-x---", "x-----x-------..", "..x-x-x-xx-x--x-", "x---------......", "x--x--x-x-x-x---", "x-x-----x-----..", "xx-x-x--x-x--x--", "x-----------...."]
    DG = ["3 3 5 6 5 3 5", "7 2'", "5 5 7 5 3 5 7", "1'", "1' 1' 6 1' 2' 1'", "7 2' 7", "5 5 1' 5 1' 2' 1'", "1'"]
    PH = ["ゆうやけのじっけんだ", "ろくほんのかわが", "ゆびさきではねてる", "なまえのないとり"]
elif SK == "H":
    S = Song("17", "sk-h", "放課後タッピング スケッチH（仮）", "After School Tapping sketch H", 132, 4, "A", "major", "ガレージ・ロックンロール（スケッチ）")
    S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.1"; K = Key("A", "major"); SC = {9, 11, 1, 2, 4, 6, 7}
    CH = ["A", "A", "G", "D", "A", "A", "C", "D"]
    S.scene("前奏", 4, "intro", ["A", "A", "G", "D"]); S.scene("サビ", 8, "chorus", CH); S.scene("おわり", 1, "outro", ["A"])
    PT = ["x-x-x-x-........", "..x-x-x---......", "x-x-xx-x-x--....", "x---x-------....", "x-x-x-x-........", "..x-x-x---......", "x-xx-x-xx-x-x-..", "x-----------...."]
    DG = ["5 5 5 6", "5 3 1", "2 2 4 2 4 5", "4 6", "5 5 3 5", "5 6 5", "b3 b3 5 b3 b3 5 5 4", "4"]
    PH = ["ほうかご", "つどえ", "ろっぽんのかわ", "なれ", "いまだけ", "きけよ", "なまえのないとり", "よ"]
else:
    S = Song("17", "sk-i", "放課後タッピング スケッチI（仮）", "After School Tapping sketch I", 92, 4, "D", "major", "ポストロック（スケッチ）")
    S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock --space hall --space-wet 0.14 " + S.flags; K = Key("D", "major"); SC = {2, 4, 6, 7, 9, 11, 1}
    CH = ["D", "F#m", "G", "Em7", "Bm7", "A", "G", "G|A"]
    S.scene("前奏", 2, "intro", ["D", "F#m"]); S.scene("サビ", 8, "chorus", CH); S.scene("おわり", 1, "outro", ["D"])
    PT = ["x-------x---x---", "x-----------....", "..x---x---x-x---", "x-------x-----..", "x---x---x-x-x---", "x-----------....", "x-x---x---x---x-", "x-----------...."]
    DG = ["3 5 1'", "5", "6 1' 2' 1'", "2' 1'", "1' 1' 2' 3' 2'", "2'", "1' 2' 3' 2' 1'", "2'"]
    PH = ["ほうかご", "ろっぽんのかわ", "ななしのとり", "いまとびたつ"]
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}; S.fade_out = 0
V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1700 + ord(SK))
lines, text = song_phrases(PT, DG, PH); bars = S.sc("サビ"); mel = [K.mel(x, oct=4) for x in lines]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, text, "サビ")


def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SC))


def tap(b, pat, order, lo, hi, second=False):
    t = [N(m) for m in tones(halves(b)[1 if second else 0], lo, hi)]; TAP.bar(b, steps(pat, [t[q % len(t)] for q in order]))


GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.042, -0.6, drive=0.4)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.07, pan=0.55, fx=GFX, **CLEAN) for i in range(6)] if SK != "H" else [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, 0.6, drive=0.35)) for i in range(6)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))
TAP = S.track("タッピングのギター（クリーン）", "distGuitar", volume=0.12, pan=-0.25, fx=GFX + [{"type": "pingpong", "beats": 0.75, "mix": 0.18 if SK != "I" else 0.32, "feedback": 0.3}], **CLEAN)
CLAP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.075, pan=0.05, reverb=0.15, modulate=False)

for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if SK == "G":
        if n == "おわり": tap(b, "x-x-x-x-x-------", (0, 1, 2, 3, 4), "E4", "E6"); bass(b, "x---------------", "1"); strum(GR, b, "x---------------", drive=False, lag_ms=14); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4); continue
        vocal_long = n == "サビ" and odd                                             # 歌が伸ばしている小節で、タッピングが答える。歌が細かい小節では、タッピングは休む
        if n == "前奏": tap(b, ["x-x-xx-x-x-xx-x-", "x-x-xx-x-x-x-x--", "xx-x-x-xx-x-x-x-", "x-x-x-x-x-x-...."][i], [(0, 2, 1, 3, 2, 4, 3, 5, 4, 2), (0, 2, 1, 3, 2, 4, 3, 2), (5, 4, 3, 4, 2, 3, 1, 2, 0, 1), (0, 1, 2, 3, 4, 5)][i], "E4", "E6", second=i in (1, 3))
        elif vocal_long: tap(b, ["....x-xx-x-xx-x-", "..x-xx-x-x-x-x--", "......xx-x-xx-x-", "....x-x-x-x-...."][i // 2], [(0, 2, 1, 3, 2, 4, 3), (2, 3, 1, 2, 0, 1, 2, 3), (4, 3, 2, 3, 1, 2), (0, 1, 2, 3)][i // 2], "E4", "E6", second=True)
        stop = (n == "前奏" and last) or (n == "サビ" and i == 3)                      # 4小節目の後ろ1拍半は、伴奏が休む
        bass(b, *[("x-----x-x---x-x-", "1135d"), ("x---x-----x-x-x-", "15wda"[:5]), ("x-----x-x-x---x-", "1123d"), ("x---x-x-x-......", "1351")][i % 4] if not stop else ("x---x-x-x-......", "1351"))
        strum(GR, b, ["x-----x---x-----", "x---x-----x-x---", "x-----x-x-------", "x---x---x-......"][i % 4] if not stop else "x---x---x-......", drive=False)
        if n == "サビ" and i >= 4: strum(GL, b, "x---------------" if not odd else "x-------x-------", strings=3)
        feel(D, b, ["break", "upbeat8", "break2", "rock8b"][i % 4], k=["X.....x...X.....", "X..x......x.X...", "X.....x..x......", "X...x.....x....."][i % 4])
        if stop: D.set(b, "X...x.....x.....", "....X....X......", "X.x.X.x.X.......")
        if i == 0: crash(D, b, "C2", 4)
        if n == "サビ" and last: fill_cresc(D, b, 2)
    elif SK == "H":
        RIFF = ["A2:0.5 A2:0.5 C3:0.5 C#3:0.5 E3:1 G3:0.5 E3:0.5", "A2:0.5 A2:0.5 C3:0.5 C#3:0.5 E3:0.5 D3:0.5 C3:0.5 A2:0.5"]      # 低い所で転がるリフ（短3度→長3度のひっかけ）
        if n == "おわり": strum(GL, b, "x---------------", strings=4); strum(GR, b, "x---------------", strings=3, lag_ms=14); bass(b, "x---------------", "1"); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4); continue
        gap = n == "サビ" and PT[i].endswith("........")                             # 歌が半小節で言い切って休む小節 → 後ろ半分でリフが答える
        if n == "前奏": TAP.bar(b, RIFF[i % 2] if i < 2 else "R:4"); strum(GL, b, "x-x-x-x-x-x-x-x-" if i >= 2 else "x---------------", strings=3)
        else:
            strum(GL, b, "x-x-x-x-x-x-x-x-" if not odd else "x-x-x-x-x---x-x-", strings=3); strum(GR, b, "x-------x-------" if not odd else "x-----x---x-----", strings=4)
            if gap: TAP.bar(b, "R:2 " + ["E3:0.5 G3:0.5 A3:0.5 C4:0.25 C#4:0.25", "E3:0.5 D3:0.5 C3:0.5 A2:0.5"][(i // 4) % 2])
        bass(b, *[("x-x-x-x-x-x-x-x-", "11113535"), ("x-x-x-x-x-x-x-x-", "111156wd"), ("x-x-x-x-x-x-x-x-", "11335531"), ("x-x-x-x-x-x-x-x-", "1113wdwa"[:8])][i % 4])
        feel(D, b, "quarter" if n == "前奏" and i < 2 else "rock8", k=["X.....x.X.......", "X.....x.X.x.....", "X.....x.X.......", "X..x..x.X......."][i % 4])
        CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
        if i == 0: crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 2 if n == "サビ" else 1)
    else:
        if n == "おわり": tap(b, "x---x---x-------", (0, 2, 4), "D4", "D6"); bass(b, "x---------------", "1"); strum(GL, b, "x---------------", strings=4); strum(GR, b, "x---------------", drive=False, lag_ms=18); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6); continue
        loud = n == "サビ" and i >= 4                                                 # 後半で、歪んだギターの壁
        tap(b, ["x--x--x--x--x-x-", "x--x--x-x--x--x-"][i % 2], [(0, 2, 4, 2, 3, 1), (0, 2, 3, 4, 2, 1)][i % 2], "D4", "D6")      # 3つずつ進む型（付点8分のやまびこと重なって、細かく聞こえる）
        if n == "サビ": bass(b, *([("x-------x---x-x-", "115d"), ("x-----x-x-----x-", "113d")][i % 2] if not loud else [("x---x-x-x---x-x-", "11235d"), ("x-x---x---x-x-x-", "11875a"[:6])][i % 2]))
        if loud: strum(GL, b, "x-x-x-x-x-x-x-x-", strings=4); strum(GR, b, "x-------x-------", drive=False)
        elif n == "サビ": strum(GR, b, "x---------------", drive=False, lag_ms=16)
        if loud: feel(D, b, "half", h="X.x.X.x.X.x.X.x.", k="X.........x....." if not odd else "X.....x...x....."); 
        elif n == "サビ" and i >= 2: D.set(b, "X.........x.....", "................" if i < 3 else "........ooxxXXXX", "x...x...x...x...")
        if loud and i == 4: crash(D, b, "C2", 6)
        if n == "サビ" and last: fill_cresc(D, b, 2)

S.desc = "仮: 17「放課後タッピング」を作り直すためのスケッチ " + SK + "（サビだけ）。自作"
finish(S, LY, V, 0)
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=17)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"chorus": 24 if SK != "H" else 14}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
