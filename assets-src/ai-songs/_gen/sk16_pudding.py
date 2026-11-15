# 16「おやつ宣戦布告」のスケッチ（サビだけ30秒を、まったく違う3方向で）。仮。
# 人間（2026-11-15）:「とりあえず4で」＝ 30秒のスケッチを3案作って聞いてもらい、選ばれた方向だけを1曲に仕上げる。
# 使い方: SK=A|B|C VB_VOCAL=1 python3 sk16_pudding.py <出力.json>
#   A「止めて、叫んで、伸ばす」… 176・D短調。全員で2発打って黙る → その無音で歌が早口 → 次の小節で歌が食って伸ばし、下でバンドが走る。ギター2本のロック
#   B「足ぶみと手びょうし」… 104・D長調（♭VII の C を借りる）。キック2発と手びょうしだけの上で、みんなで大きく歌う。ピアノとベース。4拍目はいつも休み
#   C「かけぬける明るいパンク」… 200・F長調（IV → IVm）。伴奏は止まらず走りつづけ、歌は長い音で上をすべる。8小節目だけ全員が止まって歌がひとり残る。シンセのきらきら
# 3つとも、docs/sound/reference-pop909.md の「休符」「和音（sus・3和音）」「音の伸ばし方（句の最後を伸ばす・ウラから食って入る）」を、それぞれ違う形で使う。
# v2（2026-11-15）人間「歌詞が直接すぎるものが多いので重要な所は隠語にしたりして。」→ 大事な言葉を言いかえた:
#   プリン＝金色の月（つき・満月）／けんか＝三時の乱世／スプーン＝銀のつるぎ／兄＝となりの王さま／じゃんけん＝グー・チョキ・パーのうらない／
#   あいこ＝かがみ合わせのにらめっこ／半分こ＝満月を割る／母＝女神の手／なかなおり＝雪どけ。「プリン」「兄」「けんか」とは一度も言わない。
from vocalo_lib import *
SK = os.environ.get("SK", "A"); DR = os.environ.get("DR", "0")     # DR: スケッチ C のドラムの案（0＝もとの8分、1＝4分で大きく、2＝4ビート、3＝半分の速さ、4＝4つ打ちと手びょうし）
def M(pat, degs): return mel16(pat, degs.split())


if SK == "A":
    S = Song("16", "sk-a", "おやつ宣戦布告 スケッチA（仮）", "Snack War sketch A", 176, 4, "D", "minor", "ロック（止めて叫ぶ・スケッチ）")
    S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
    K = Key("D", "minor")
    CH = ["Dm", "Dsus4", "Bb", "Csus4", "Dm", "F", "Gm", "Asus4", "Bb", "C", "Dm", "Dsus4", "Gm", "Bb", "Asus4", "Dm"]
    S.scene("リフ", 4, "intro", ["Dm", "Dm", "Bb", "C"]); S.scene("サビ", 16, "chorus", CH); S.scene("おわり", 1, "outro", ["Dm"])
    CALL = "....xxxx.xx.x-.."; HOLD = "x-x-x-.x--------"
    C_ = ["5 5 5 7 1' 1' 7", "3' 3' 2' 1' 7 1' 2'", "5 5 5 7 1' 1' 2'", "1' 1' 2' 3' 3' 2' 1'", "1' 1' 1' 2' 3' 3' 2'", "5 5 7 1' 2' 2' 1'", "3' 3' 2' 1' 2' 2' 1'", "5 5 5 7 1' 2' 3'"]
    H_ = ["7 1' 2' 3'", "1' 7 5 5", "3' 2' 1' 2'", "2' 1' 7 1'", "1' 1' 2' 2'", "7 1' 2' 1'", "1' 2' 3' 3'", "3' 2' 1' 1'"]
    VC = [x for c, h in zip(C_, H_) for x in (M(CALL, c), M(HOLD, h))]
    TXT = "さんじのらんせ/まくあけ/つきはひとつぶ/きんいろ/ぎんのつるぎが/きらめく/ぐーちょきぱーの/うらない/かがみあわせの/にらめっこ/まんげつをわる/なんてね/めがみのてから/ふたつめ/さんじのらんせ/ゆきどけ"
elif SK == "B":
    S = Song("16", "sk-b", "おやつ宣戦布告 スケッチB（仮）", "Snack War sketch B", 104, 4, "D", "major", "ロック（足ぶみと手びょうし・スケッチ）")
    S.kit = "naked-x"; S.flags = S.flags + " --piano salamander --space room --space-wet 0.12 --bass bnb-loud"
    K = Key("D", "major")
    CH = ["D", "D", "C", "G", "D", "D", "C", "G", "Bm", "G", "Asus4", "A"]
    S.scene("サビ", 12, "chorus", CH); S.scene("おわり", 1, "outro", ["D"])
    PA = "x---x-x-..x-x---"; PB = "x-------....x-x-"; PE = "x-----------...."
    VC = [M(PA, "1 3 5 5 6"), M(PB, "5 5 6"), M(PA, "1' b7 5 4 5"), M(PB, "6 5 6"), M(PA, "1' 1' 2' 1' 6"), M(PB, "5 6 1'"),
          M(PA, "2' 1' b7 5 b7"), M(PB, "1' 1' 2'"), M(PA, "3' 3' 2' 1' 6"), M(PB, "1' 6 1'"), M(PA, "2' 2' 1' 2' 3'"), M(PE, "2'")]
    TXT = "さんじのかね/きんのつきひとつ/となりのおうさま/ゆずれぬおうかん/ぎんのつるぎぬき/さんじのらんせだ"
else:
    S = Song("16", "sk-c", "おやつ宣戦布告 スケッチC（仮）", "Snack War sketch C", 200, 4, "F", "major", "パンク（かけぬける・スケッチ）")
    S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
    K = Key("F", "major")
    CH = ["F", "Am", "Bb", "Bbm", "F", "Dm", "Gm", "Csus4", "F", "Am", "Bb", "Bbm", "F", "Dm", "Gm", "C"]
    S.scene("リフ", 4, "intro", ["F", "Am", "Bb", "Bbm"]); S.scene("サビ", 16, "chorus", CH); S.scene("おわり", 3, "outro", ["F", "Bbm", "F"])
    P1 = "x---x---x-x-x---"; P2 = "x-----x-------.."
    A_ = ["3 3 5 3 1", "4 4 5 6 1'", "5 5 6 5 3", "6 6 5 4 2", "1' 1' 6 5 6", "6 6 1' 6 4", "5 6 1' 1' 6", "2 4 6 1' 6"]
    B_ = ["2 3", "6 b6", "5 6", "4 5", "6 5", "5 4", "6 1'", "5 5"]
    VC = [x for a, b in zip(A_, B_) for x in (M(P1, a), M(P2, b))]
    TXT = "さんじのらんせ/つきはひとつぶ/ぎんのつるぎが/ぐーちょきぱーの/かがみあわせの/まんげつをわる/めがみのてから/ふたつめのつき"
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.4; S.keepers = {}
if SK == "C" and DR != "0": S.slug = f"sk-c-d{DR}"

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S)
bars = S.sc("サビ"); mel = [K.mel(x, oct=4) for x in VC]
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, TXT, "サビ")
N = lambda m: nm(m)

if SK == "A":
    GL = [S.track(f"Lギター{i + 1}", "distGuitar", **rock_gtr_spec(0.055, -0.6, drive=0.45)) for i in range(3)]
    GR = [S.track(f"Rギター{i + 1}", "distGuitar", **rock_gtr_spec(0.052, 0.6, drive=0.45)) for i in range(3)]
    BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.25))

    def gt(b, pat, short=None):
        ch = S.chords[b]; pw = power(ch, "D2"); r = low(ch, "C3"); up = tones(ch, nm(r + 1), nm(r + 12))[:2]
        while len(up) < 2: up.append(r + 12)
        for j in range(3): GL[j].bar(b, steps(pat, [N(pw[j])], short=short)); GR[j].bar(b, steps(pat, [N(([r] + up)[j])], short=short))
        BASS.bar(b, steps(pat, [N(low(ch, "D1"))], short=short))
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b)
        if n == "リフ":
            gt(b, ["x-.x-...x-.x-...", "x-.x-...x-x-x-..", "x-.x-...x-.x-...", "x-x-x-x-........"][i])        # 全員で打って、休む
            D.set(b, ["X..X....X..X....", "X..X....X.X.X...", "X..X....X..X....", "X.X.X.X........."][i], ["X..X....X..X....", "X..X....X.X.X...", "X..X....X..X....", "X.X.X.X........."][i], "................")
        elif n == "サビ":
            if i % 2 == 0:      # 2発打って黙る → 歌だけが早口
                gt(b, "x-.x-...........", short=0.5); D.set(b, "X..X............", "X..X............", "................")
                if i % 8 == 0: crash(D, b, "C2", 2)
            else:               # 歌が伸ばす下で、バンドが走る（最後の8分は休み。15小節目は全部打ち切り）
                gt(b, "x-x-x-x-x-x-x-..") if i != 15 else gt(b, "x-x-x-x-x-x-x---")
                D.set(b, "X...X.X...X.X...", "....X.......X.X.", "x.x.x.x.x.x.x...")
        else:
            gt(b, "x---............"); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
elif SK == "B":
    PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.12, pan=-0.2 + 0.2 * i, reverb=0.2, sustain=1.2, fx=rack_piano()) for i in range(3)]
    PL = S.track("ピアノ（左手のオクターブ）", "piano", volume=0.13, pan=-0.1, reverb=0.15, sustain=1.0)
    BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
    CLAP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.085, pan=0.05, reverb=0.25, modulate=False)
    TAMB = S.track("タンバリン", "guitar", patch="kawaiiFx", volume=0.04, pan=0.4, reverb=0.2, modulate=False)
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b); ch = S.chords[b]; r = low(ch, "D1")
        if n == "サビ":
            v = sorted(voice(ch, 64, 3))
            # 足ぶみ2発（1拍目・2拍目）→ 手びょうし（3拍目）→ 4拍目は全員休み。ピアノは足ぶみといっしょに2発だけ
            pat = "x---x---........" if i % 4 != 3 else "x---x---..x-x-.."
            for j in range(3): PN[j].bar(b, steps(pat, [N(v[j])], short=0.75))
            PL.bar(b, steps("x---x---........", [N(r + 24), N(r + 12)], short=0.75))
            BASS.bar(b, steps("x---x---........" if i % 2 == 0 else "x---x-....x-x-..", [N(r), N(r), N(r + 7), N(r + 12)], short=0.75))
            D.set(b, "X...X...........", "................", "................"); CLAP.bar(b, "R:2 B4:1 R:1"); TAMB.bar(b, "R:2 B5:0.5 B5:0.5 R:1")
            if i == 8: crash(D, b, "C2", 4)
            if i == 11: D.set(b, "X...X...X.X.X...", "........X.X.X...", "................")     # 最後だけ、4拍目の手前まで打つ
        else:
            v = sorted(voice(ch, 64, 3))
            for j in range(3): PN[j].bar(b, steps("x-----------....", [N(v[j])]))
            PL.bar(b, steps("x-----------....", [N(r + 24)])); BASS.bar(b, steps("x-----------....", [N(r)])); D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
else:
    GL = [S.track(f"Lギター{i + 1}", "distGuitar", **rock_gtr_spec(0.045, -0.6, drive=0.4)) for i in range(3)]
    GR = [S.track(f"Rギター{i + 1}", "distGuitar", **rock_gtr_spec(0.043, 0.6, drive=0.4)) for i in range(3)]
    BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
    PLK = S.track("きらきらのプラック", "lead", patch="kfbSquarePluck", volume=0.06, pan=0.3, reverb=0.2, fx=rack_pluck())
    CLAP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.085, pan=0.05, reverb=0.2, modulate=False)
    if DR == "2": S.keepers = {"サビ": "ride"}
    SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.022, pan=(0, 0.2, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.5, fx=rack_supersaw()) for i in range(5)]

    def gt(b, pat):
        ch = S.chords[b]; pw = power(ch, "F2"); r = low(ch, "C3"); up = tones(ch, nm(r + 1), nm(r + 12))[:2]
        while len(up) < 2: up.append(r + 12)
        for j in range(3): GL[j].bar(b, steps(pat, [N(pw[j])])); GR[j].bar(b, steps(pat, [N(([r] + up)[j])]))
        BASS.bar(b, steps(pat, [N(low(ch, "F1"))]))
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b); ch = S.chords[b]
        if n == "リフ":
            PLK.bar(b, arp16(ch, "x.xxx.xxx.xxx.xx", (0, 2, 4, 3, 5, 4, 6, 5, 7, 6, 4, 2), lo="F4", hi="F6", short=0.25))
            if i >= 2: gt(b, "x-x-x-x-x-x-x-x-"); D.set(b, "X...X...X...X...", "................" if i == 2 else "....X...X.X.XXXX", "x.x.x.x.x.x.x.x.")
        elif n == "サビ":
            if i == 7:      # 8小節目: 頭の1発だけで全員止まり、歌の長い音がひとり残る
                gt(b, "x-.............."); D.set(b, "X...............", "X...............", "................")
            elif DR == "0":
                gt(b, "x-x-x-x-x-x-x-x-"); D.set(b, "X...X.X.X...X.X." if i % 2 == 0 else "X...X.X.X..XX.X.", "....X.......X...", "x.x.x.x.x.x.x.x.")
            elif DR == "1":      # 4分で大きく: キックは1・3拍目、スネアは2・4拍目、刻みは4分
                gt(b, "x-x-x-x-x-x-x-x-"); D.set(b, "X.......X......." if i % 2 == 0 else "X.....X...X.....", "....X.......X...", "x...x...x...x...")
            elif DR == "2":      # 4ビート: ライドを4分で刻み、スネアは軽く2・4拍目。ベースは4分で歩く。ギターは2・4拍目に短く
                r = low(ch, "F1"); t = tones(ch, nm(r + 1), nm(r + 12)); nx = low(S.chords[b + 1], "F1") if b + 1 < S.nb else r
                BASS.bar(b, steps("x---x---x---x---", [N(r), N(t[0]), N(t[1] if len(t) > 1 else r + 7), N(nx - 1 if nx > r else nx + 1)]))
                rr = low(ch, "C3"); up = tones(ch, nm(rr + 1), nm(rr + 12))[:2]
                for j in range(3): GR[j].bar(b, steps("....x-......x-..", [N(([rr] + up + [rr + 12])[j])], short=0.5))
                D.set(b, "X..............." if i % 4 == 0 else "................", "....x.......x...", "x...x...x...x..." if i % 2 == 0 else "x...x.x.x...x.x.")
            elif DR == "3":      # 半分の速さ: キックは1拍目（と3拍目のウラ）、スネアは3拍目だけ
                gt(b, "x-x-x-x-x-x-x-x-"); D.set(b, "X.........X....." if i % 2 == 0 else "X.....X.........", "........X.......", "x...x...x...x...")
            else:                # 4つ打ちと手びょうし: キックを4分で踏み、スネアのかわりに手びょうし。シンバルなし
                gt(b, "x-x-x-x-x-x-x-x-"); D.set(b, "X...X...X...X...", "................", "................"); CLAP.bar(b, "R:1 B4:1 R:1 B4:1")
                v = wide9(ch); [SAW[j].bar(b, steps("x-------------..", [N(v[j])])) for j in range(5)]
                if i % 2 == 1: PLK.bar(b, "R:2 " + arp16(ch, "xxxxxxxx", (0, 1, 2, 3, 4, 5, 6, 7), lo="F5", hi="F7"))      # 歌が伸ばしている後ろで「ピロピロピロピーン」
            if i % 8 == 0: crash(D, b, "C2", 4)
            if i == 15: put_fill(D, b, "snare16")
        else:
            if i == 0: gt(b, "x---------------"); crash(D, b, "C2", 4); D.set(b, "X...............", "X...............", "................")
            if i == 1: PLK.bar(b, arp16(ch, "x.x.x.x.x.x.x-..", (7, 6, 5, 4, 3, 2, 1), lo="F4", hi="F6"))
            if i == 2: gt(b, "x-----------...."); D.set(b, "X...............", "X...............", "................")

S.fade_out = 0
S.desc = f"仮: 16「おやつ宣戦布告」のサビのスケッチ{SK}（30秒）。3方向から1つを選んでもらうためのもの。自作"
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"chorus": 18}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ", 8 if SK != "B" else 0, None, K)], vol=0.36)
    if SK == "B": harmony(path, S, [("サビ", 0, None, K)], steps=7, vol=0.26, lowest=45)     # みんなで歌う感じ: 3度下と1オクターブ下
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
