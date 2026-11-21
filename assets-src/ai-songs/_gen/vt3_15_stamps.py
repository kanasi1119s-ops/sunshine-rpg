# vt3 15「おばあちゃんのスタンプ」Grandma's Stamps（仮）— 今のボカロ曲の作り方で作る1曲目。テクノポップ（Kawaii future bass の音＋リリースカットピアノ）。172・4/4。
#   Aメロは A短調、サビは短3度上の C短調（サビで転調）、最後のサビはさらに半音上（C♯短調）。2分53秒。
# 第3弾（0時〜24時の街）の 14時。表は docs/sound/vt3-plan.md。
#
# v6（2026-11-15）: 人間「今の作り方に足りていないもの全て足して。音の作り方も学んでプロ仕様に」→ 5声に広げたスーパーソウ（9度入り・うねるフィルター）、
#   音作りのまとまり（rack_*）、上がる音・インパクト・サブドロップ、グリッチ、テープストップ、16分のアルペジオ、ケロケロ声（語り）、1オクターブ下のハモリ。前奏を厚く、最後のサビを一番強く。
# v4（2026-11-15）: ゼロから作り直し。人間（2026-11-15）:「曲の作り方単調なんだよね」「現代的な感じのボカロっぽさないよね。ボカロ曲の作り方徹底的に学んで、必要な要素を作曲ソフトに入れようか」
#   調べたこと（docs/sound/vocaloid-study.md）を、部品（vocalo_lib.py）にして、この曲で初めて使う:
#   ① 速いテンポ（172）と、16分の早口の歌 ② 跳ぶ旋律（5度の行き来・6度上がる）③ 丸サ進行（IV△7 → III7 → VIm7 → I7）とサビでの転調（短3度上）
#   ④ リリースカットピアノ（短く切ってすき間を空けて刻む。小節ごとにリズムを変える）⑤ 16ビートの4つ打ち・半分の速さ・キメ・1小節の止め
#   ⑥ 切り貼り（歌の「ぴ・ぴ・ぴ・ぴ」）⑦ 短い曲（3分以内）で、4〜8小節ごとに場面が変わる。前奏は2小節だけで、すぐサビ
#
# 構成: ぴこん（2小節）→ 頭のサビ（8）→ リフ（4）→ Aメロ（8・最後はキメと止め）→ Aメロ'（8）→ Bメロ（8・半分の速さ → 止めと切り貼り）→ サビ1（16）
#       → リフ（4）→ 語り（8・ばあちゃんの音声メッセージ。半分の速さ・キュートの声）→ Bメロ'（4）→ サビ2（16）→ ソロ（8・電子のリード）
#       → 落ちサビ（8・ピアノと声だけ。鼻歌＝合いことばの節）→ 最後のサビ（16・半音上）→ しめ（4）→ ぴこん（2）
#
# 物語: 山のむこうに住むおばあちゃんの、はじめてのメッセージ「げんきですか」。たった6文字に、何分かけたのかな。返事をしたら、すぐスタンプ。
#   おじぎするねこ、花のくま、ハートが3つ。電車でも、寝る前も、ぴこん、ぴこん。届いた音声メッセージには、ばあちゃんの鼻歌。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: はなれて暮らすさびしさが、「ぴこん」の音で、言葉よりずっとたくさんの「だいすき」に変わる。
from vocalo_lib import *

S = Song("15", "stamps", "おばあちゃんのスタンプ（仮）", "Grandma's Stamps", 172, 4, "A", "minor", "テクノポップ（今のボカロ曲の作り方・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.keepers = {}
KA = Key("A", "minor")         # Aメロ・Bメロ・語り（oct 3 で 1 = A3）
KC = Key("C", "minor")         # サビ（oct 4 で 1 = C4）
KD = Key("C#", "minor")        # 最後のサビ

MA, MC, MD = marusa(0), marusa(3), marusa(4)
A_CH = ["Am7", "Am7", "Am7", "Am7", "Fmaj7", "E7", "Am7", "E7"]
S.scene("ぴこん", 2, "intro", ["Cm7", "Cm7"])
S.scene("頭のサビ", 8, "chorus", MC + marusa(3, last="E7"))
S.scene("リフ", 4, "break", MA)
S.scene("Aメロ", 8, "verse", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ", 8, "pre", ["Dm7", "E7", "Am7", "A7", "Dm7", "G7", "G7", "G7"])
S.scene("サビ1", 16, "chorus", MC * 4)
S.scene("リフ2", 4, "break", MA)
S.scene("語り", 8, "bridge", MA + MA)
S.scene("Bメロ2", 4, "pre", ["Dm7", "G7", "G7", "G7"])
S.scene("サビ2", 16, "chorus", MC * 4)
S.scene("ソロ", 8, "solo", MA + marusa(0, last="G7"))
S.scene("落ちサビ", 8, "bridge", MC + marusa(3, last="G#7"))
S.scene("最後のサビ", 16, "chorus", MD * 4)
S.scene("しめ", 4, "chorus", MD)
S.scene("おわり", 2, "outro", ["C#m7", "C#m7"])

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
PN = [S.track(f"リリースカットピアノ{i + 1}", "piano", volume=0.11, pan=-0.25 + 0.1 * i, reverb=0.12, sustain=0.25, fx=rack_piano()) for i in range(3)]
PNL = [S.track(f"ピアノ（のばす{i + 1}）", "piano", volume=0.1, pan=-0.15, reverb=0.3, sustain=1.6) for i in range(3)]
FMB = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.095, pan=0, duck=0.25, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.036, pan=0, duck=0.4)
# スーパーソウの和音は5声（根音・5度は真ん中寄り、3度・7度・9度は高く広く）。2拍で1往復するフィルターでうねらせ、キックで凹ませる
SAW = [S.track(f"スーパーソウの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.026, pan=(0, 0.15, -0.45, 0.45, -0.2)[i], reverb=0.2, duck=0.6,
               fx=rack_supersaw(hp=180 if i < 2 else 260, pump_ms=round(60000 / 172 * 2), wide=0.2 if i < 2 else 0.4)) for i in range(5)]
PLK = S.track("プラックのリフ", "lead", patch="kfbSquarePluck", volume=0.062, pan=0.3, reverb=0.2, fx=rack_pluck())
LEAD = S.track("電子のリード（ソロ）", "lead", patch="kfbSineLead", volume=0.085, pan=-0.1, reverb=0.25, fx=rack_lead())
PAD = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.032, pan=-0.4 + 0.4 * i, reverb=0.45) for i in range(3)]
PIK = S.track("通知の音（ぴこん）", "lead", patch="kfbGlocken", volume=0.09, pan=0.3, reverb=0.3)
KDR = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
FXT = S.track("かわいい効果音（上がる音・インパクト）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.2, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌（16分のマスで書く。x＝音の頭、-＝のばす、.＝休み）=================
def M(pat, degs): return mel16(pat, degs.split())


HOOK = "x-xx..x-xx..x-x-"            # ぴ・こん　ぴ・こん　＋2音（長・短短 の形を2回）
RUN = "xxxx..xxxx..x-x-"             # 16分4つ・休み・16分4つ・8分2つ（早口）
END3 = "x-.x-.x-------.."            # v10: 句の最後を、拍のウラから食って入って2拍のばす（プロの編曲では句の最後の4割が2拍以上・長い音の半分ほどはウラから入る）
VC = [M(HOOK, "3' 1' 1' 3' 1' 1' 5 1'"), M("x-x-..x-------..", "2' #7 5"),
      M(RUN, "5 5 1' 1' 5 5 3' 3' 2' 1'"), M(END3, "7 5 3"),
      M(HOOK, "3' 1' 1' 3' 1' 1' 7 2'"), M("x-x-..x-------..", "4' 2' #7"),
      M(RUN, "3 3 5 5 7 7 1' 1' 3' 1'"), M(END3, "7 1' 7"),
      M(HOOK, "3' 1' 1' 3' 1' 1' 5 1'"), M("x-x-..x-------..", "2' #7 5"),
      M(RUN, "1' 1' 5 5 1' 1' 3' 3' 4' 3'"), M(END3, "1' 7 5"),
      M(HOOK, "3' 1' 1' 3' 1' 1' 7 2'"), M("x-x-..x-------..", "4' 2' #7"),
      M("x-x-x-x-x-x-x---", "5 7 1' 3' 2' 1' 7"), M("x-----------....", "1'")]
C1 = ("ぴこんぴこんとどいたよ/おじぎのねこにはなのくまね/ぴこんぴこんまたきたよ/はーとがみっつもならんでるよ/"
      "ぴこんぴこんやまこえて/ことばよりもずっとたくさんの/ぴこんぴこんおやゆびで/だいすきがとどく")
C0 = "ぴこんぴこんとどいたよ/おじぎのねこにはなのくまね/ぴこんぴこんまたきたよ/はーとがみっつもならんでるよ"
C2 = ("ぴこんぴこんでんしゃでも/となりのひとまでわらってるよ/ぴこんぴこんねるまえも/おやすみのくまがてをふるよ/"
      "ぴこんぴこんおしえたの/わたしなのにまけそうだよね/ぴこんぴこんおやゆびで/あいにいくからね")
C3 = ("ぴこんぴこんとどいたよ/こんどはほんものとどけるね/ぴこんぴこんまっていてね/すたんぷよりもつよくぎゅっとね/"
      "ぴこんぴこんやまこえて/ことばよりもずっとたくさんの/ぴこんぴこんおやゆびで/だいすきがとどく")
PAT = "..xxxxx.xxxxx-.."            # Aメロ: 半拍おいて、16分5つ・16分5つ（早口で語る）
VA = [M(PAT, "5 5 5 7 1' 1' 7 5 5 3"), M(END3, "3 5 5"), M(PAT, "5 5 7 7 1' 2' 1' 7 7 5"), M(END3, "7 1' 7"),
      M(PAT, "3 3 5 5 1' 1' 5 5 3 3"), M(END3, "2' #7 5"), M("x-x-x-x-x-x-x-x-", "1' 1' 7 5 7 1' 2' 3'"), "R:4"]
A1 = "やまのむこうのばあちゃんから/はじめてのめっせーじがきたよ/げんきですかのむもじだけで/なんぷんかけたの"
A2 = "へんじをしたらすぐすたんぷ/おじぎするねこがとんできた/おしえたのはまごのわたしで/こんなにおすとは"
VB = [M("x---x---x-x-x---", "4 6 1' 6 1'"), M("x-------x---....", "2' #7"), M("x---x---x-x-x---", "5 1' 3' 1' 3'"), M("x-------x---....", "2' #3'"),
      M("x-x-x-x-x---x---", "4 6 1' 2' 4' 2'"), M("x-x-x-x-x-------", "2' 4' 2' 7 2'"), "R:4", "R:4"]
B1 = "ゆびいっぽんでね/うってくれたんだ/めがねずらしてのぞいて"
B2 = "ことばにできないきもち"
VT = [M("x-x-x-x-x-x-x-x-", "3 3 5 5 3 3 1 3"), M("x-x-----........", "5 #7"), M("x-x-x-x-x-x-x-x-", "5 5 7 7 5 5 3 5"), M("x-x-----........", "7 5"),
      M("x-x-x-x-x-x-x-x-", "3 5 5 1' 1' 5 5 3"), M("x-x-----........", "2' #7"), M("x-x-x-x-x-x-x-x-", "1' 1' 7 7 5 5 7 1'"), M("x-x-----........", "7 3'")]
TT = "もしもしきこえるかい/こちらはげんきですよ/すたんぷたのしいねえ/またすぐおくるからね"
VO = [M("........x-x-x---", "5 7 1'"), M("x-x-----........", "7 4"), M("x-x-x-x-x-x-x---", "3 3 5 5 7 5 3"), M("x-------........", "5"),
      M("........x-x-x---", "5 7 1'"), M("x-x-----........", "7 4"), M("x-x-x-x-x-x-x---", "5 5 7 7 1' 7 5"), M("x-------........", "1'")]
OT = "ららららら/ばあちゃんのうただ/ららららら/あいにいくからね"
VG = [VC[0], VC[1], M("x-x-x-x-x-x-....", "1' 7 5 7 1' 1'"), "R:4"]
GT = "ぴこんぴこんとどいたよ/げんきですよ"
LY = Lyrics(S)


def put(name, key, lines, text, o):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("頭のサビ", KC, VC[:8], C0, 4)
put("Aメロ", KA, VA, A1, 3)
put("Aメロ2", KA, VA, A2, 3)
put("Bメロ", KA, VB, B1, 3)
put("サビ1", KC, VC, C1, 4)
put("語り", KA, VT, TT, 3)
put("Bメロ2", KA, VB[4:], B2, 3)
put("サビ2", KC, VC, C2, 4)
put("落ちサビ", KC, VO, OT, 4)
put("最後のサビ", KD, VC, C3, 4)
put("しめ", KD, VG, GT, 4)

# ================= 伴奏（小節ごとにリズムを変える。同じ型を続けない）=================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
RC_V = ["x..x..x.x..x.x..", "x.x..x..x.x..x.x", "x..x..x.x..x..x.", "..x.x..x..x.x..x"]       # Aメロのリリースカットピアノ（4小節で1まわり・毎小節ちがう）
RC_C = ["x.xx.x.xx.x.x.x.", "x..x.xx.x..x.xx.", "x.xx.x.xx.x.xx.x", "x.x..x.x.x..x..."]       # サビ
RC_R = ["x.xx..x.xx..x.x.", "x..x..x..x..x.x.", "x.xx..x.xx..x.x.", "x.x.x.x.xxxxxxxx"]       # リフ


def rc(b, pat, c=64, short=0.25):
    for tr, line in zip(PN, relcut(PN, S.chords[b], pat, c, short)): tr.bar(b, line)


def long3(tracks, b, c=64, pat="x---------------"):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): tracks[j].bar(b, steps(pat, [nm(v[j])]))


def bass(b, style):
    ch = S.chords[b]; r = low(ch, "F1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "F1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); o = r + 12
    ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1); N = nm
    FMB.bar(b, {"v1": steps("x..x..x...x.x...", [N(r), N(r), N(o), N(r), N(t5)]),
                "v2": steps("x.x...x..x..x.x.", [N(r), N(o), N(r), N(t5), N(o), N(ap)]),
                "c1": steps("x.x.x.x.x.x.x.x.", [N(r), N(o), N(r), N(o), N(r), N(o), N(t5), N(ap)]),
                "c2": steps("x.xxx.x.x.xxx.x.", [N(r), N(r), N(o), N(r), N(o), N(r), N(r), N(o), N(t5), N(ap)]),
                "half": steps("x-------..x-x---", [N(r), N(t5), N(o)]),
                "kime8": steps("x.x.x.x.x.x.x.x.", [N(r)] * 8), "hit": steps("x---............", [N(r)]), "long": steps("x-------------..", [N(r)])}[style])


def saw(b, pat, c=53):
    v = wide9(S.chords[b], c, 5)
    for j in range(5): SAW[j].bar(b, steps(pat, [nm(v[j])]))


def plk(b, pat, order, lo="A4", hi="A6"):
    tn = tones(root(b), lo, hi); PLK.bar(b, steps(pat, [nm(tn[q % len(tn)]) for q in order]))


def pik(b, hi="C7", lo_="G6", at="..........x-x---"): PIK.bar(b, steps(at, [lo_, hi]))



def bp(b, pat, kinds, short=None):
    """ベースを16分のマスで書く。kinds: r＝根音・o＝1オクターブ上・5＝5度・a＝次の和音へ近づく音"""
    ch = S.chords[b]; r = low(ch, "F1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "F1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1); mp = {"r": r, "o": r + 12, "5": t5, "a": ap}
    FMB.bar(b, steps(pat, [nm(mp[c]) for c in kinds], short=short))


def stab(b, pat, c=53):
    v = wide9(S.chords[b], c, 5)
    for j in range(5): SAW[j].bar(b, steps(pat, [nm(v[j])]))


# v10（2026-11-15）人間「音の伸ばし方とかを勉強するといいかも。」→ docs/sound/reference-pop909.md の「音の伸ばし方」。句の最後を2拍のばす・ウラから食って入る。
# v7（2026-11-15）人間「曲調が今までと変わってないなー。休符とかもしっかり使ってみて。」
#   今までの曲は、どの場面も全員が鳴りっぱなしだった。この版は「鳴らさない所」を先に決める:
#   ・Aメロ: 歌っている小節は、頭のベース1発と指パッチンだけ。歌が休む半小節に、ピアノが答える（かけ合い）
#   ・サビ1・サビ2: 半分の速さ。和音は短い「ジャッ・ジャッ」だけで、間は空ける。4小節ごとに最後の1拍を全員休む
#   ・リフ: 全員が同じリズムで打って、2拍まるごと休む
#   ・最後のサビだけ、4つ打ちで全員が鳴りつづける（ここまで空けてきたぶん、いちばん大きく聞こえる）
RIFF = [("x.xx....x.xx....", (2, 0, 2, 3, 2, 4)), ("x.xx....x.x.x-..", (3, 1, 3, 4, 5, 4)),
        ("x.xx....x.xx....", (2, 0, 2, 4, 3, 5)), ("x-x-x-x-........", (4, 3, 2, 0))]
SOLO = ["x-xxx-x-xx......|C6 A5 C6 E6 C6 A5 G5", "........x-x-xxxx|B5 D6 E6 D6 B5 E6", "xxxx.xxx........|A5 C6 E6 A6 G6 E6 C6", "....x-x-x-..x-x-|G6 E6 C6 E6 G6",
        "x-xxx-x-xx......|F6 C6 F6 A6 F6 C6 A5", "........xx.xx.xx|E6 B5 E6 G#5 B5 D6", "x---x-x-........|A6 E6 C6", "xxxxxxxxxxxx....|G5 B5 D6 F6 G6 F6 D6 B5 D6 F6 G6 B6"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ぴこん":
        pik(b, at="x-x-....x-x-....")
        long3(PNL, b, 67, "x-------........"); long3(PAD, b, 72); stab(b, "x-------........", 51); bp(b, "x-------........", "r")
        if i == 1: PLK.bar(b, "R:2 " + glitch("G5", 1, (4,)) + " R:1"); FXT.bar(b, fx_bar((0, "kira", 1), (2, "up", 1)))   # 最後の1拍は全員休み → サビ
    elif n in ("頭のサビ", "サビ1", "サビ2", "ソロ"):
        j = i % 8; first = n == "頭のサビ"; odd = j % 2 == 1
        # 和音は短く打って、間を空ける。歌が休む後半（奇数の小節）に答える
        if not odd: stab(b, "x-.....x-......." if j % 4 == 0 else "x-....x-..x-....")
        else: stab(b, "........x-.x-..." if j != 7 else "........x-......")
        if not odd: bp(b, "x-....x-....x...", "rr5", short=0.5)
        else: bp(b, "x-......x..x.x..", "rroa", short=0.5) if j != 7 else bp(b, "x-......x-......", "ro", short=0.5)
        if not first: SUB.bar(b, steps("x-------........", [nm(low(S.chords[b], "F1"))]))
        if odd and n != "ソロ": pik(b, at="..........x-x-.." if j != 7 else "........x-x-....")
        if n == "サビ2" and not odd: rc(b, "..x...x...x.x...", 67)                                  # 2回目は、ピアノがすき間に少し入る
        if n == "サビ2" and j in (3,): plk(b, "........xxxxxx..", (2, 3, 4, 5, 6, 7))
        if n == "ソロ": pat, nts = SOLO[i].split("|"); LEAD.bar(b, steps(pat, nts.split()))
        if n == "ソロ" and odd is False and i > 0: rc(b, "........x.xx.x..", 64)                       # リードが休む後半に、ピアノが答える
        if i == 0 and not first: FXT.bar(b, fx_bar((0, "impact", 2)))
    elif n in ("最後のサビ", "しめ"):
        j = i % 8
        rc(b, ["x.xx.x.xx.x.x.x.", "x..x.xx.x..x.xx.", "x.xx.x.xx.x.xx.x", "x.x..x.x.x..x..."][(i + (i // 4)) % 4], 68)
        bp(b, "x.x.x.x.x.x.x.x.", "rororo5a") if j % 2 == 0 else bp(b, "x.xxx.x.x.xxx.x.", "rroroorr5a"[:10])
        stab(b, "x-----x-----x---" if j % 2 == 0 else "x---x-----x-----", 51); SUB.bar(b, steps("x-------x-------", [nm(low(S.chords[b], "F1"))] * 2))
        if j % 2 == 1 and n != "しめ": pik(b, "C#7", "G#6")
        if n != "しめ" and j % 2 == 0: PLK.bar(b, arp16(S.chords[b], "x.xxx.xxx.xxx.xx", (0, 2, 4, 3, 5, 4, 6, 5, 7, 6, 4, 2), short=0.25))
        long3(PAD, b, 72)
        if i == 0: FXT.bar(b, fx_bar((0, "impact", 2), (0, "sub", 2)) if n != "しめ" else fx_bar((0, "impact", 2)))
    elif n in ("リフ", "リフ2"):
        pat, order = RIFF[i]
        rc(b, pat, 64, short=0.25); bp(b, pat, "rrorro"[:onsets(pat)] if i < 3 else "ro5a", short=0.5 if i == 3 else 0.25); plk(b, pat, order)
        if n == "リフ2" and i == 3: FXT.bar(b, fx_bar((2, "down", 2)))
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"
        if i < 6 and i % 2 == 0:                                                     # 歌っている小節: ほとんど鳴らさない
            bp(b, "x-.............." if not two else "x-....x-........", "r" if not two else "rr", short=0.5)
        elif i < 6:                                                                  # 歌が休む後半に、ピアノ（2番はプラックも）が答える
            rc(b, ["........x.xx.x..", "........xx.x.x..", "........x..x.xx."][i // 2], 64); bp(b, "x-......x..x....", "rr5", short=0.5)
            if two: plk(b, "..........x.xx-.", (3, 4, 2))
        elif i == 6: rc(b, "x.x.x.x.x.x.x.x.", 67); bp(b, "x.x.x.x.x.x.x.x.", "rrrrrrrr")   # キメ: 8分で全員いっしょ
        else: rc(b, "x...............", 69); bp(b, "x---............", "r")                # 1拍だけ鳴らして止める
    elif n in ("Bメロ", "Bメロ2"):
        q = i if n == "Bメロ" else i + 4
        if q < 6:
            long3(PNL, b, 62 + q, "x-----------...."); long3(PAD, b, 66 + q); bp(b, "x-------..x-x---", "r5o")
            if q >= 4: stab(b, "x-----------....", 50)
        elif q == 6: stab(b, "x-x-x-x-x-x-x-x-", 52); bp(b, "x.x.x.x.x.x.x.x.", "rrrrrrrr")
        else: FXT.bar(b, fx_bar((0, "rev", 3)) if n == "Bメロ" else fx_bar((0, "up", 2), (2, "glitch", 1)))   # 全員休み（歌の切り貼りだけ）。最後の1拍は無音
    elif n == "語り":
        long3(PNL, b, 64, "x-----------...." if i % 2 == 0 else "....x-------...."); bp(b, "x-------........", "r")
        if i % 2 == 1: pik(b, "E7", "B6", "............x-x-")
        if i >= 4: long3(PAD, b, 69)
    elif n == "落ちサビ":
        long3(PNL, b, 64, "x-------x-----.." if i % 2 == 0 else "x-----------....")
        if i >= 4: long3(PAD, b, 69)
        if i == 0: FXT.bar(b, fx_bar((0, "down", 2), (2, "kira2", 1)))
        if i == 7: stab(b, "x-------........", 52); FXT.bar(b, fx_bar((0, "rev", 2), (2, "up", 1)))        # 最後の1拍は無音 → 最後のサビ
    elif n == "おわり":
        if i == 0: pik(b, "C#7", "G#6", "x-x-............"); long3(PNL, b, 68)

# ================= ドラム（半分の速さとすき間 → 最後だけ4つ打ち）=================
SNAP = "R:1 C5:1 R:1 C5:1"       # 指パッチン（2拍目と4拍目）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("頭のサビ", "サビ1", "サビ2", "ソロ"):
        j = i % 8
        if j == 7: D.set(b, "X..X....X.......", "........X.X.....", "x.x.x.x.x.x.....")            # 最後の1拍は休み
        elif j == 3: D.set(b, "X..X......X.....", "........X.....XX", "x.x.x.x.x.x.x...")
        elif j % 2 == 0: D.set(b, "X.........X.X...", "........X.......", "x.x.x.xxx.x.x.x." if n != "頭のサビ" else "x...x...x...x...")
        else: D.set(b, "X..X......X.....", "........X.......", "x.x.x.x.....x.x.")
        KDR.bar(b, "R:2 B4:1 R:1")
        if i % 8 == 0: crash(D, b, "C2", 4)
    elif n in ("最後のサビ", "しめ"):
        kk, ss, hh = BEAT16 if i % 4 != 3 else BEAT16B
        vgroove(D, b, "beat8", ghosts=0.15, seed=b, k=kk, s=ss, h=hh, vary=False)
        KDR.bar(b, "R:1 B4:1 R:1 B4:1")
        if i % 8 == 0: crash(D, b, "C2", 6)
        if last and n == "しめ": D.set(b, *KIME_END)
        elif i % 8 == 7: put_fill(D, b, "small")
    elif n in ("リフ", "リフ2"):
        if i < 3: D.set(b, "X..X....X..X....", "....X.......X...", "................")
        else: D.set(b, "X.X.X.X.........", "X.X.X.X.........", "................")
    elif n in ("Aメロ", "Aメロ2"):
        two = n == "Aメロ2"
        if i < 6 and i % 2 == 0: D.set(b, "X..............." if not two else "X.....X.........", "................", "................" if not two else "..x...x...x...x."); KDR.bar(b, SNAP)
        elif i < 6: D.set(b, "X.......X..X....", "............X...", "................" if not two else "..x...x.x.x.x.x."); KDR.bar(b, "R:1 C5:1 R:2")
        elif i == 6: D.set(b, *KIME8)
        else: D.set(b, "X...............", "X...............", "................")
    elif n in ("Bメロ", "Bメロ2"):
        q = i if n == "Bメロ" else i + 4
        if q < 6: D.set(b, *HALF)
        elif q == 6: D.set(b, "X...X...X...X...", "X.X.X.X.XXXXXXXX", "................")
    elif n == "語り":
        D.set(b, "X.........x.....", "........x.......", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.....")
    elif n == "落ちサビ":
        if i == 7: D.set(b, "X...X...X.X.....", "....X...X.X.....", "................")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の15（14時）。今のボカロ曲の作り方で作る1曲目。テクノポップ・172。Aメロは A短調、サビは短3度上の C短調、最後は半音上。"
          "16分の早口の歌、跳ぶ旋律、丸サ進行、リリースカットピアノ、16ビートの4つ打ち、キメと止め、歌の切り貼り。2分53秒。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"落ちサビ": -0.5, "語り": -0.3, "最後のサビ": 0.5})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "リリースカットピアノ", mid=84, down=12, up=10, seed=3); humanize(path, "プラックのリフ", mid=82, down=10, up=8, seed=5)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 4, "pre": 12, "chorus": 18, "最後のサビ": 22, "bridge": 6}, scoop=0.25, slash=0.6, vib_min_beats=2.0, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, KC), ("サビ2", 0, None, KC), ("最後のサビ", 0, None, KD), ("しめ", 0, None, KD)], vol=0.36)
    # 歌の切り貼り: ぴこん の場面・Aメロの止め・Bメロの最後の小節（サビへ「ぴ・ぴ・ぴ・ぴ」とかけ上がる）
    cb = {S.sc("ぴこん")[1]: "R:2 " + stutter_chop("G4", "ぴ", 4, 0.25) + " " + stutter_chop("C5", "ぴ", 4, 0.25)}
    for nme in ("Aメロ", "Aメロ2"): cb[S.sc(nme)[7]] = "R:2 " + stutter_chop("E4", "ぴ", 2, 0.25) + " " + stutter_chop("A4", "ぴ", 2, 0.25) + " " + stutter_chop("E5", "ぴ", 4, 0.125) + " R:0.5"
    for nme in ("Bメロ", "Bメロ2"): cb[S.sc(nme)[-1]] = stutter_chop("G4", "ぴ", 4, 0.5) + " " + stutter_chop("B4", "ぴ", 4, 0.25) + " " + stutter_chop("D5", "ぴ", 8, 0.125)
    chops(path, S, cb, vol=0.34, pan=-0.15)
    harmony(path, S, [("最後のサビ", 0, None, KD)], steps=7, vol=0.2, lowest=50)      # 最後のサビだけ: 1オクターブ下も重ねて厚く
    # ダブリング（同じ旋律を、左右に、ほんの少し高さをずらして重ねる）: サビ2 と最後のサビだけ。歌ごとに合成のゆらぎが変わるので、ぴったり同じ音にはならない
    for sgn in (-1, 1): harmony(path, S, [("サビ2", 0, None, KC), ("最後のサビ", 0, None, KD), ("しめ", 0, None, KD)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    voice_by_scene(path, S, {"語り": "cute"}, default="clear")
    js = load(path)
    kero(js, 1)                                                                      # 語り（ばあちゃんの音声メッセージ）だけ、ケロケロ声
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"ぴこん": 1.5, "頭のサビ": 0.5, "リフ": 1.2, "Aメロ": 1.2, "Aメロ2": 0.6, "最後のサビ": 0.9, "しめ": 0.7})      # v11（2026-11-21）: 人間「前奏で急に音小さくなるのやめて」。頭のサビ → リフ → Aメロ で 4.6dB ずつ下がっていた → リフと Aメロを持ち上げ、出だしの +3 を +1.5 に
