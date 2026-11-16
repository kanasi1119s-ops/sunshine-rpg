# 17「放課後タッピング」v3（放課後のセッション・フュージョン）。仮。
# 人間（2026-11-16 22:30）:「16.17もう一度作り直そう」→ 方向は「まったく新しい方向で」。G（マスロック）・H（ガレージ）・I（ポストロック）・v2（マスロック 138）のどれとも違う曲調にする。
# 曲を決める表:
#   形 … 工程表の決まり「リフが主役。歌は2回だけ、あとは楽器が話を進める」。机をたたくリズムで始まる → タッピングのテーマ → 歌1 → キメ → ベースの番 → エレピの番 → ギターの番 → キメ → 静かな所 → 歌2 → 全員でテーマ → キメで止まる
#   強さ … 机 2 → テーマ 6 → 歌1 5 → キメ 8 → ベース 4 → エレピ 5 → ギター 7→8 → キメ 8 → 静か 2 → 歌2 7 → テーマ（全員）10
#   旋律の性格 … 歌は短い（8小節＋4小節）。16分で食って、長い音はウラから。主役はタッピングのテーマと、楽器の「番」
#   その曲だけの音 … 机をたたく手びょうしのリズム、全員が同じリズムで動くキメ、楽器が順番に前へ出る「番」
# 学んだ弾き方: タッピング（tap3: たたく→はなす→左手でたたく の3つ組。つなげる）／単音のギター（1拍に約1.6音・句は8分のウラから・2割は休む・しゃくりは長い音だけ・ビブラートは山場の1音だけ）
#   ベースは歩く（根音は6割まで）／歌は休みを多く・ビブラート深め／ドラムはテンポ112 なので16分の刻みでよい（1秒に 7〜10打）
# 使い方: VB_VOCAL=1 python3 vt3_17f_tapping.py <出力.json>
from vocalo_lib import *
import random as _r, re as _re

S = Song("17", "tapping", "放課後タッピング（仮）", "After School Tapping", 112, 4, "B", "minor", "フュージョン")
S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.1"
K = Key("B", "minor"); SC = {11, 1, 2, 4, 6, 7, 9}
T_CH = ["Bm7", "E7", "Amaj7", "F#m7", "Gmaj7", "A", "Em7", "F#7"]
V_CH = ["Gmaj7", "A", "F#m7", "Bm7", "Gmaj7", "A", "Em7", "F#7", "Gmaj7", "A", "Bm7", "Bm7"]
VAMP = ["Bm7", "Bm7", "E7", "E7"]
S.scene("机のリズム", 2, "intro", ["Bm7", "Bm7"])
S.scene("テーマ", 8, "intro", T_CH)
S.scene("歌1", 12, "chorus", V_CH)
S.scene("キメ", 2, "break", ["Bm7", "Bm7"])
S.scene("ベースの番", 4, "solo", VAMP)
S.scene("エレピの番", 4, "solo", VAMP)
S.scene("ギターの番", 8, "solo", T_CH)
S.scene("キメ2", 2, "break", ["Bm7", "Bm7"])
S.scene("静かな所", 4, "bridge", ["Gmaj7", "A", "Em7", "F#7"])
S.scene("歌2", 12, "chorus", V_CH)
S.scene("テーマ（全員）", 8, "outro", T_CH)
S.scene("キメ3", 2, "outro", ["Bm7", "Bm7"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1703)

# ================= 歌（2回だけ）=================
SP = ["..x.x-xx-x--x-x-", ".x------x-----..", "x.x--x-x.x--x---", ".x------........", "..xx-x-x.x-x--x-", "x--x--.x---.....", "x-xx.x-x--x-x---", ".x----------....",
      "x--x--x-.x-x----", ".x------x-----..", "x--x.x-x-x--x---", ".x----------...."]
SD = ["5, 5, 7, 1 7, 5, 7,", "7, 2", "2 2 1 7, 1 2", "3", "3 3 2 3 4 3 2", "2 4 4", "4 4 3 4 5 4 3", "2", "3 3 4 3 1", "2 4", "5 4 3 4 3 1", "1"]
V1 = ["ゆうやけのじっけんだ", "ろくほんのかわ", "ゆびさきではねるたび", "なまえのないとり", "だれもしらない", "ここでうまれた"]
V2 = ["ちゃいむがなってもまだ", "かえりたくない", "まどのそとへとどけと", "とりがいまとんだ", "あしたもここで", "つづきをやろう"]


def put(name, pats, degs, phrases, o=4):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("歌1", SP, SD, V1); put("歌2", SP, SD, V2)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw): gtr_strum(tracks, S, b, pat, halves(b)[0], RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SC))


def shift(s, n):
    """音の並びを n 半音ずらす（キメを、楽器ごとに高さを変えて重ねるため）"""
    return " ".join(x if x.startswith("R") else _re.sub(r"^[A-G][#b]?\d", lambda m: nm(midi(m.group(0)) + n), x) for x in s.split())


def comp(b, pat):
    v = sorted(voice(halves(b)[0], 62, 3))
    for j in range(3): EP[j].bar(b, steps(pat, [N(v[j])]))


CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 1}, {"type": "room", "mix": 0.1}]
TAP = S.track("タッピングのギター（クリーン）", "distGuitar", volume=0.13, pan=-0.25, fx=GFX + [{"type": "pingpong", "beats": 0.75, "mix": 0.14, "feedback": 0.25}], legato=True, **CLEAN)
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.12, 0.2))
GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.065, pan=0.55, fx=GFX, **CLEAN) for i in range(6)]
EP = [S.track(f"エレピ{i + 1}", "keys", patch="kfbGlassEp", volume=0.07, pan=(-0.45, -0.3, -0.15)[i], reverb=0.2, sustain=0.9) for i in range(3)]
EPL = S.track("エレピ（旋律）", "keys", patch="kfbGlassEp", volume=0.12, pan=-0.2, reverb=0.25, sustain=1.0)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.26))
CLAP = S.track("机をたたく音", "guitar", patch="kawaiiFx", volume=0.08, pan=0.05, reverb=0.12, modulate=False)

DESK = ["B4:0.5 B4:0.25 B4:0.25 R:0.5 B4:0.5 B4:0.25 B4:0.25 B4:0.5 R:1", "B4:0.5 B4:0.25 B4:0.25 R:0.5 B4:0.5 B4:0.25 B4:0.25 B4:0.25 B4:0.25 B4:0.5 R:0.5"]      # 机をたたくリズム（3＋3＋2）
THEME = ["R:0.5 B4:0.5 D5:0.5 F#5:0.75 E5:0.25 D5:0.5 B4:1", "R:0.5 G#4:0.5 B4:0.5 D5:0.5 E5:1 D5:0.5 B4:0.5", "C#5:0.75 E5:0.75 G#5:0.5 A5:1 G#5:0.5 E5:0.5", None,
         "R:0.5 B4:0.5 D5:0.5 F#5:0.75 G5:0.25 F#5:0.5 D5:1", "R:0.5 C#5:0.5 E5:0.5 A5:1 G5:0.5 E5:1", "G5:0.75 F#5:0.75 E5:0.5 D5:0.5 B4:0.5 D5:1", None]      # None の小節はタッピングの3つ組
KIME = ["B1:0.5 R:0.25 D2:0.5 R:0.25 E2:0.5 R:0.5 F#2:0.5 A2:0.5 B2:0.5", "D3:0.5 B2:0.5 R:0.25 A2:0.5 R:0.25 F#2:1 R:1"]      # 全員が同じリズムで動く
KIME_D = [("X.....X.....X...", "...X......X...X.", "................"), ("X....X..........", "..X.....X.......", "................")]
B_SOLO = ["B1:0.5 R:0.25 B1:0.25 D2:0.5 E2:0.5 F#2:0.75 A2:0.25 B2:1", "R:0.5 D3:0.5 B2:0.5 A2:0.5 F#2:0.5 E2:0.5 D2:0.5 B1:0.5", "E2:0.75 E2:0.25 G#2:0.5 B2:0.5 D3:1 B2:0.5 G#2:0.5", "R:0.5 E2:0.5 F#2:0.5 G#2:0.5 A2:0.5 A#2:0.5 B2:1"]
E_SOLO = ["R:0.5 D5:0.5 F#5:0.5 A5:0.5 B5:1 A5:0.5 F#5:0.5", "E5:0.75 D5:0.75 B4:0.5 R:1 B4:0.5 D5:0.5", "E5:0.5 G#5:0.5 B5:0.5 D6:1 B5:0.5 G#5:1", "R:0.5 F#5:0.5 G#5:0.5 A5:0.5 B5:0.5 C#6:0.5 D6:1"]
G_SOLO = ["R:0.5 F#5:0.5_ A5:0.5 B5:1/ A5:0.5_ F#5:1", "R:1 E5:0.5 G#5:0.5_ B5:0.5 B5:0.5 A5:0.5_ G#5:0.5", "A5:1.5/ G#5:0.25_ E5:0.25 C#5:1 R:1", "R:0.5 C#5:0.5 E5:0.5_ F#5:0.5 A5:0.5 F#5:0.5_ E5:0.5 C#5:0.5",
          "D5:0.75 D5:0.75 F#5:0.5_ G5:0.5 B5:1.5/", "R:0.5 A5:0.5_ B5:0.25_ C#6:0.25 E6:1/ C#6:0.5_ B5:0.5 A5:0.5", "G5:0.5 G5:0.5 E5:0.5_ D5:0.5 B4:0.5 D5:0.5_ E5:1", "R:0.5 A#5:0.5 C#6:1/ E6:2~"]
WB = [("x-.x..x-x-.xx-x-", "11355wd"), ("x-..x.x-..x-x-x-", "1875wd"), ("x-x-..x-.xx-x-x-", "12355wd"), ("x-.x-.x-x-x-x-x-", "1123123"), ("x-..x.x-x-.xx-x-", "18755wd"), ("x-x-x-..x-.xx-x-", "12345wd"), ("x-.x..x-.xx-x-x-", "11345wa"), ("x-x-..x-x-x-x-x-", "1231234")]
VB_ = [("x--x..x-..x-x-x-", "113wda"), ("x-..x-x-..x.x-x-", "1535wd"), ("x--x..x-x-..x-x-", "11235d"), ("x-.x..x-x-x-x-x-", "1151123")]
KICKS = ["X..x...xX.x.....", "X.....x.X..x....", "X..x...xX.x.....", "X.....x.X.x....."]


def kime(b, i, crash_it=True):
    BASS.bar(b, KIME[i]); TAP.bar(b, shift(KIME[i], 36)); EPL.bar(b, shift(KIME[i], 24)); D.set(b, *KIME_D[i])
    if i == 0 and crash_it: crash(D, b, "C2", 4)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "机のリズム":
        CLAP.bar(b, DESK[i])
        if i == 1: D.set(b, "................", "............ooXX", "..x...x...x....."); BASS.bar(b, "R:3 F#2:0.5 A2:0.5")
    elif n in ("テーマ", "テーマ（全員）"):
        allp = n == "テーマ（全員）"
        if THEME[i]: TAP.bar(b, THEME[i])
        else: TAP.bar(b, tap3(halves(b)[0], "xxxxxxxxxxxx...." if i == 3 else "xxxxxxxxx-......", order="TPH", start=1 if i == 3 else 2))
        if allp and THEME[i]: EPL.bar(b, shift(THEME[i], -12))                        # 最後は、エレピも同じテーマを1オクターブ下で
        bass(b, *WB[i % 8]); comp(b, ["x-----x---x-----", "..x---x-----x---", "x-----x-x-------", "x---x-----......"][i % 4] if not allp else ["x--x--x-x--x--x-", "x-x---x--x--x---"][i % 2])
        if allp or i >= 4: strum(GR, b, ["x-xxx-x-xxx-x-xx", "x-x-xxx-x-xxx-x-"][i % 2], drive=False)
        feel(D, b, "funk16", k=KICKS[i % 4]); CLAP.bar(b, DESK[i % 2]) if i < 2 and not allp else None
        if i == 0: crash(D, b, "C2", 4)
        if i in (3, 7): fill_cresc(D, b, 1 if i == 3 else 2)
    elif n in ("歌1", "歌2"):
        two = n == "歌2"; stop = i == 7                                               # 8小節目の後ろ2拍は伴奏が休む
        if stop: bass(b, "x-.x..x-........", "115"); comp(b, "x-----x-........"); D.set(b, "X..x...x........", "....X...........", "x.x.x.x........."); fill_cresc(D, b, 2); continue
        bass(b, *(VB_[i % 4] if not two else WB[(i + 3) % 8])); comp(b, ["x-----x---x-----", "..x---x-----x---", "x-----x-x-------", "x---x-----x-x---"][i % 4])
        if two or i >= 8: strum(GR, b, ["x-------x-x-----", "x-----x---x-x---"][i % 2], drive=False)
        if SP[i].startswith(".x") and i not in (3,): TAP.bar(b, "R:1.5 " + tap3(halves(b)[0], "xxxxxx", order="TPH", start=(i // 2) % 3) + " R:1")      # 歌が伸ばしている小節で、タッピングが少し答える
        feel(D, b, "soul8" if not two else "funk16", k=["X.......x.X.....", "X..x....X.......", "X.......x.X.....", "X.....x.X..x...."][i % 4] if not two else KICKS[i % 4])
        if i in (0, 8): crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 2)
    elif n in ("キメ", "キメ2", "キメ3"):
        kime(b, i)
        if n == "キメ3" and i == 1: comp(b, "x-x..x..x-------")
    elif n == "ベースの番":                                                         # ベースが歌う。エレピは小さく押さえ、ドラムはすき間を空ける
        BASS.bar(b, B_SOLO[i]); comp(b, "x---------------" if not odd else "......x---------"); feel(D, b, "space" if not odd else "break")
        if last: fill_cresc(D, b, 1)
    elif n == "エレピの番":
        EPL.bar(b, E_SOLO[i]); bass(b, *VB_[i % 4]); comp(b, "x-----x---------" if not odd else "..x-------x-----"); feel(D, b, "soul8", k=["X.......x.X.....", "X..x....X......."][i % 2]); strum(GR, b, "x---------------", drive=False) if odd else None
        if i == 0: crash(D, b, "C2", 4)
        if last: fill_cresc(D, b, 1)
    elif n == "ギターの番":                                                         # ギターが歌う。後半でだんだん大きく
        LEAD.bar(b, G_SOLO[i]); bass(b, *WB[(i + 2) % 8]); comp(b, ["x-----x---x-----", "..x---x-----x---"][i % 2])
        if i >= 4: strum(GR, b, ["x-xxx-x-xxx-x-xx", "x-x-xxx-x-xxx-x-"][i % 2], drive=False)
        feel(D, b, "funk16", k=KICKS[i % 4])
        if i in (0, 4): crash(D, b, "C2", 4)
        if i == 3: fill_cresc(D, b, 1)
        if last: fill_cresc(D, b, 2)
    elif n == "静かな所":                                                           # エレピとベースと、机をたたく音だけ
        comp(b, "x---------------" if not odd else "x-------x-------"); bass(b, "x-------x---x-x-" if not last else "x---x---........", "115d" if not last else "15"); CLAP.bar(b, DESK[i % 2]) if i >= 2 else None
        if i == 1: TAP.bar(b, "R:2 " + tap3(halves(b)[0], "xxxxxx", order="TPH", start=0) + " R:0.5")
        if last: D.set(b, "................", "........ooxxXXXX", "................")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の17「放課後タッピング」v3（放課後のセッション・フュージョン・112・ロ短調）。机をたたくリズムで始まり、タッピングのテーマ、"
          "ベース・エレピ・ギターが順番に前へ出て、全員が同じリズムで動くキメで止まる。歌は2回だけ。自作")
finish(S, LY, V, 0, special={"静かな所": -0.5, "テーマ（全員）": 0.5, "机のリズム": 0.2})

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=88, down=10, up=10, seed=17)
js = load(path); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"歌1": 22, "歌2": 26}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("歌2", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"歌1": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"机のリズム": 7.0, "テーマ": 1.5, "キメ": 0.6, "ギターの番": -0.5, "キメ2": 0.6, "歌2": 0.5, "テーマ（全員）": 1.5, "キメ3": 1.5})   # v3: 机のリズムの出だしが小さかった・最後のテーマがギターの番より小さかった
