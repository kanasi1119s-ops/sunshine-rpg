# 16「おやつ宣戦布告」を最初から作り直すためのスケッチ（サビだけ30秒・3方向）。仮。
# 人間（2026-11-15 23:52）:「16の曲最初から作り直しましょう。」→ 前の A・B・C とも、v9 とも違う方向を3つ。旋律もリズムも新しく書く。
# 使い方: SK=D|E|F VB_VOCAL=1 python3 sk16b_pudding.py <出力.json>
#   D「はねるファンク・ロック」112・E短調 … 歌は16分で食って短く切り、句の最後だけ伸ばす。クリーンのギターが16分でかき鳴らし（アップ入り）、ベースが動く。ドラムはゴーストノート入り
#   E「ポンプするロック」160・A長調 … 半分の速さ。スーパーソウの和音がキックでへこみ、歪んだギターは長くのばすだけ。歌は大きく、食って伸ばす。ベルが答える
#   F「大げさなバラード」84・C長調 … プリンの取り合いを、わざと壮大に歌い上げる。ピアノと弦で始まり、後半でドラムとギターが入る。III7・IVm で泣かせる
# 必ず守る弾き方（docs/sound/composer-preferences.md の表）を、3つとも守る。歌詞は中心の言葉を言いかえる（プリン＝金色の月、けんか＝三時の乱世、スプーン＝銀のつるぎ、兄＝となりの王）。
from vocalo_lib import *
import random as _r
SK = os.environ.get("SK", "D")
def M(pat, degs): return mel16(pat, degs.split())


if SK == "D":
    S = Song("16", "sk-d", "おやつ宣戦布告 スケッチD（仮）", "Snack War sketch D", 112, 4, "E", "minor", "ファンク・ロック（スケッチ）")
    S.kit = "naked-x"; S.flags = S.flags + " --bass bnb-loud --space room --space-wet 0.08"
    K = Key("E", "minor")
    CH = ["Em7", "A", "Em7", "C|B7", "Em7", "A", "Em7", "C|B7", "Em7", "A", "C|D", "Em"]
    S.scene("サビ", 12, "chorus", CH); S.scene("おわり", 1, "outro", ["Em7"])
    FA = "..xx.xx.x-x-...."; FB = "xx.x--x-------.."
    A_ = ["5 5 7 5 3 5", "1' 1' 7 5 7 1'", "3 3 5 3 1 3", "5 5 7 1' 7 5", "1' 1' 2' 1' 7 1'", "7 7 1' 2' 1' 7"]
    B_ = ["7 7 5 1'", "1' 1' 7 2'", "4 4 5 1'", "7 7 5 5", "2' 2' 1' 1'", "5 5 7 1'"]
    VC = [x for a, b in zip(A_, B_) for x in (M(FA, a), M(FB, b))]
    TXT = "さんじのかね/なりだす/つきはひとつ/きんいろ/となりのおう/にやりと/ぎんのつるぎ/ぬいたら/ゆずれないね/このつき/らんせのまく/あがるよ"
elif SK == "E":
    S = Song("16", "sk-e", "おやつ宣戦布告 スケッチE（仮）", "Snack War sketch E", 160, 4, "A", "major", "ポンプするロック（スケッチ）")
    S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
    K = Key("A", "major")
    CH = ["D", "E", "C#m7", "F#m", "D", "E", "Asus4|A", "A", "D", "E", "C#m7", "F#m", "D", "E", "F#m", "Esus4|E"]
    S.scene("前奏", 4, "intro", ["D", "E", "F#m", "E"]); S.scene("サビ", 16, "chorus", CH); S.scene("おわり", 1, "outro", ["A"])
    EA = "x-x-x-x---x-x---"; EB = "x-----x-------.."
    A_ = ["5, 5, 1 1 3 2", "3 3 5 5 3 2", "4 4 6 6 5 4", "5 5 4 3 2 1", "1 1 3 3 4 6", "5 5 3 3 2 3", "4 4 4 6 5 4", "1 1 3 3 5 6"]
    B_ = ["1 2", "1 3", "4 5", "2 1", "6 5", "2 1", "3 2", "5 5"]
    VC = [x for a, b in zip(A_, B_) for x in (M(EA, a), M(EB, b))]
    TXT = "きんのつきひとつ/となりのおうさま/ゆずれぬおうかん/さんじのらんせだ/ぎんのつるぎぬき/かがみあわせでも/めがみのひとこえ/ふたつめのつきだ"
else:
    S = Song("16", "sk-f", "おやつ宣戦布告 スケッチF（仮）", "Snack War sketch F", 84, 4, "C", "major", "大げさなバラード（スケッチ）")
    S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock --piano salamander --space hall --space-wet 0.14 " + S.flags
    K = Key("C", "major")
    CH = ["C", "E7", "Am", "C7", "F", "Fm", "C|Am", "Dm7|Gsus4"]
    S.scene("サビ", 8, "chorus", CH); S.scene("おわり", 2, "outro", ["C", "C"])
    BA = "x---x-x-x---x---"; BB = "x-----x-------.."
    A_ = ["3 3 2 1 5", "6 6 5 3 1'", "6 6 5 4 1'", "5 5 3 5 1'"]
    B_ = ["6 #5", "1' b7", "1' b6", "2' 1'"]
    VC = [x for a, b in zip(A_, B_) for x in (M(BA, a), M(BB, b))]
    TXT = "さんじのらんせ/つきはひとつぶ/ぎんのつるぎを/そらにかかげて"
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(160)
bars = S.sc("サビ"); mel = [K.mel(x, oct=4) for x in VC]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, TXT, "サビ")


def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def strum(tracks, b, pat, **kw):
    """ギターの和音（学んだ弾き方）。小節の途中で和音が変わるときは、前半と後半で分ける"""
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bassp(tr, b, pat, kinds, short=None):
    c1, c2 = halves(b); r = low(c1, "E1"); r2 = low(c2, "E1"); nx = S.chords[b + 1].split("|")[0] if b + 1 < S.nb else c2; rn = low(nx, "E1")
    mp = {"r": r, "o": r + 12, "5": r + 7, "a": rn - 1 if rn > r2 else rn + 1, "R": r2, "7": r + 10}
    tr.bar(b, steps(pat, [N(mp[c]) for c in kinds], short=short))


CLEAN = dict(di="emily", stringNoise=True, amp="jpopClean", ampDrive=0.12, chorus=0, humanPitch=0, noScoop=True, powerChord=False, sustain=1.3, release=0.5)
GFX = [{"type": "filter", "kind": "highpass", "freq": 110, "q": 0.7}, {"type": "eq", "low": -1, "mid": 1.5, "midHz": 1800, "high": 1}, {"type": "room", "mix": 0.1}]
if SK == "D":
    GR = [S.track(f"Rギター{i + 1}弦め（クリーン）", "distGuitar", volume=0.075, pan=0.5, fx=GFX, **CLEAN) for i in range(6)]
    GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, -0.55, drive=0.3)) for i in range(6)]
    BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))
    STAB = [S.track(f"スーパーソウの合いの手{i + 1}", "lead", patch="kfbSupersawWide", volume=0.024, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.15, fx=rack_supersaw()) for i in range(5)]
    FUNK = ["x-xxx-x-xxx-x-xx", "x-x-xxx-x-xxx-x-", "x-xxx-x-x-xxx-xx", "x-x-xxx-xxx-x---"]
    BP = [("x-..x.x-..x-.xx-", "rrorra"), ("x-.x..x-x-..x.x-", "rr7orr"), ("x-..x.x-..x-.xx-", "rror5a"), ("x-.x-.x-x-x-x-..", "rrRRoa"[:6])]
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b); odd = i % 2 == 1
        if n == "おわり":
            strum(GR, b, "x-----------....", lag_ms=14); strum(GL, b, "x-----------....", strings=3); bassp(BASS, b, "x-----------....", "r"); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4); continue
        strum(GR, b, FUNK[i % 4], drive=False)                                   # クリーン: 16分のかき鳴らし（8分はダウン、16分ウラはアップで高い弦だけ）
        if i % 4 == 0: strum(GL, b, "x-------........", strings=3)                # 歪んだギターは、4小節に1回、頭でのばすだけ
        if i == 11: strum(GL, b, "x---x---x-x-....", strings=3)
        pat, kinds = BP[i % 4]; bassp(BASS, b, pat, kinds, short=None)
        if odd:                                                                  # 歌が伸ばしている後ろで、スーパーソウが「ジャッ・ジャッ」と合いの手
            v = wide9(halves(b)[1])
            for j in range(5): STAB[j].bar(b, steps("..........x-.x-.", [N(v[j])]))
        feel(D, b, "funk16" if i % 4 != 3 else "funk16", k=["X..x...xX.x.....", "X.....x.X..x....", "X..x...xX.x.....", "X.....x.X.x....."][i % 4])
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i in (7, 11): fill_cresc(D, b, 1)
elif SK == "E":
    GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, -0.6, drive=0.4)) for i in range(6)]
    GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.038, 0.6, drive=0.35)) for i in range(6)]
    BASS = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.085, pan=0, duck=0.25, fx=rack_bass())
    SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.038, pan=0, duck=0.4)
    SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.65, fx=rack_supersaw()) for i in range(5)]
    BELL = S.track("ベル", "lead", patch="kfbGlocken", volume=0.085, pan=0.25, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
    KFXT = S.track("クラップ", "guitar", patch="kawaiiFx", volume=0.07, pan=0.05, reverb=0.15, modulate=False)
    HATR = S.track("ハイハットのロール", "guitar", patch="kawaiiFx", volume=0.04, pan=-0.2, reverb=0.1, modulate=False)
    FXT = S.track("効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)
    # ポンプの型（Kawaii future bass の試作1 とベースのリズムが同じだったので、この曲のために書き直した: 2拍目のウラで歌といっしょに食う）
    GATES = ["x---x-x---x-x-x-", "x-x---x-----x-x-", "x---x-x-x-..x---", "x-x---x---x-x-..", "x---x-x---x-x-x-", "x-x---x-----x---", "x-x-x-x---x---x-", "x---x-x-........"]
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b); odd = i % 2 == 1; t = [N(m) for m in tones(halves(b)[0], "C#5", "C#6")]
        if n == "前奏":      # ベルの節と、のびる和音。最後の1拍は全員休み
            v = wide9(halves(b)[0]); [SAW[j].bar(b, steps("x-----------....", [N(v[j])])) for j in range(5)]
            BELL.bar(b, steps(["x-x-x---x-x-x---", "x-x-x---x-------", "x-x-x---x-x-x---", "x-x-x-x-x-x-...."][i], [t[0], t[1], t[-1], t[1], t[0], t[-1]]))
            SUB.bar(b, steps("x-----------....", [N(low(halves(b)[0], "F1"))]))
            if i == 3: FXT.bar(b, fx_bar((0, "up", 3))); D.set(b, "................", "........x.x.XX..", "................")
        elif n == "サビ":
            g = GATES[i % 8]; v = wide9(halves(b)[0]); [SAW[j].bar(b, steps(g, [N(v[j])])) for j in range(5)]      # 和音は小節ごとに型を変えてポンプ
            bassp(BASS, b, g, "rrrrrorr5a"[:onsets(g)]); SUB.bar(b, steps("x-------x-------" if i % 8 != 7 else "x-------........", [N(low(halves(b)[0], "F1"))] * 2))
            strum(GL, b, "x-------x-------" if not odd else "x-----x---------", strings=3); strum(GR, b, "x---------------" if not odd else "x-----x---------", strings=4)     # ギターはのばすだけ（歌が食う所でいっしょに食う）
            if odd: BELL.bar(b, steps("..........x-x-x-", [t[0], t[1], t[-1]]))
            feel(D, b, "half" if i % 4 != 3 else "halfopen", k="X.........x....." if not odd else "X.....x...x....."); KFXT.bar(b, "R:2 B4:1 R:1")
            if i % 8 == 0: crash(D, b, "C2", 4); FXT.bar(b, fx_bar((0, "impact", 2)))
            if i == 7: fill_cresc(D, b, 2)
            if i in (3, 11): hat_roll(HATR, b, 0.5)
            if i == 15: fill_cresc(D, b, 1, toms=False)
        else:
            strum(GL, b, "x-----------....", strings=3); strum(GR, b, "x-----------....", strings=4, lag_ms=14); SUB.bar(b, steps("x-----------....", [N(low(halves(b)[0], "F1"))])); BELL.bar(b, steps("x-x-x-----------", [t[0], t[1], t[-1]]))
            D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
else:
    PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.1, pan=-0.1 + 0.15 * i, reverb=0.3, sustain=1.6) for i in range(3)]
    PL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.2, reverb=0.25, sustain=1.6)
    ST = [S.track(f"弦{i + 1}", "strings", volume=0.05, pan=-0.3 + 0.3 * i, reverb=0.4) for i in range(3)]
    GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.042, -0.6, drive=0.4)) for i in range(6)]
    GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, 0.6, drive=0.35)) for i in range(6)]
    BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b); c1, c2 = halves(b); r = low(c1, "E1")
        v = sorted(voice(c1, 64, 3)); v2 = sorted(voice(c2, 64, 3))
        if n == "おわり":
            if i == 0:
                for j in range(3): PN[j].bar(b, steps("x---------------", [N(v[j])])); ST[j].bar(b, steps("x---------------", [N(v[j] + 12)]))
                PL.bar(b, steps("x---------------", [N(r + 12)])); strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4, lag_ms=20); bassp(BASS, b, "x---------------", "r")
                D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
            continue
        # ピアノ: 左手はオクターブ、右手は8分でわけて弾く（下・中・上・中）
        seq = [v[0], v[1], v[2], v[1], v2[0], v2[1], v2[2], v2[1]]
        PN[0].bar(b, steps("x-x-x-x-x-x-x-x-", [N(m) for m in seq])); PL.bar(b, steps("x-------x-----x-", [N(r + 12), N(low(c2, "E1") + 12), N(low(c2, "E1") + 19)]))
        for j in range(3): ST[j].bar(b, steps("x-------x-------", [N(v[j] + 12), N(v2[j] + 12)]))
        if i >= 4:           # 後半: ドラム・ベース・ギターが入って、大きく
            strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x-----------x---", strings=4); bassp(BASS, b, "x-----x-x-----x-", "rrRa")
            feel(D, b, "half", h="X.x.X.x.X.x.X.x.")
            if i == 4: crash(D, b, "C2", 6)
            if i == 7: fill_cresc(D, b, 2)
        elif i == 3: fill_cresc(D, b, 2)      # 4小節目の後ろ2拍: だんだん強くなるフィルで、後半へ

S.fade_out = 0
S.desc = f"仮: 16「おやつ宣戦布告」を最初から作り直すためのサビのスケッチ{SK}。自作"
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"chorus": 18 if SK != "D" else 10}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ", {"D": 4, "E": 8, "F": 4}[SK], None, K)], vol=0.36)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
