# PUNK 01「終電バイバイ」Last Train, Bye-Bye（仮）— ポップパンク（ボカロ）。4分の4・176・ニ長調。176小節・約4分。
#
# 2026-11-25 人間「パンクロックの曲作ろうか」→ 聞いて決めたこと: タイプ＝ポップパンク／長さ＝約4分／物語＝終電を見送る夜。
# ジャンルの決まりごと（docs/sound/punk-guide.md・melocore-study.md・この日に調べ直したこと）から使ったもの:
#   ギターは左右2本で和音をかき鳴らす（8分・ダウン中心）／ベースは8分の根音でキックとそろえる／場面の頭にクラッシュ、4・8小節の切れ目にフィル／サビは全員の声を重ねる／リードは短く歌える旋律。
#   なぞらなかったもの: 進行は I–V–vi–IV にしない（サビは I → III7 → IV → iv、終わりは ♭VI → ♭VII）。サビの3回は「半分の速さ」（くじ）。ブリッジミュートの刻みは入れない（人間が聞きにくいと言った音）。
# 形: くじ（tools/vt3/form_dice.py --skeleton 74443 240 176 --min-chorus 3 --not-start 立ち上げ --not-start 手びょうし --grooves drive,twobeat,pogo,laid,tresillo）。
#   始まり＝リードギターのソロ／終わり＝全員で1打して止まる／リズムの取り方＝主「pogo（4分キックのたてノリ）」・Aメロ「drive（前のめりの8ビート）」。合わない10か所は引き直し。
#   人が決めた所: サビの出だしの形（3 3 5 6 5）と最後の1行（よるはこんなにひろい）は、3種類の入り方でも毎回同じ（C で分かったこと: サビには1つの顔が要る）。
#   この曲だけのもの: 発車メロディのようなリードギターの旋律（自作。最初と最後と、ベルの場面）と、線路の「ガタン・ゴトン」のタム。
# 物語: 残業帰り。階段の上で足が止まり、走れば間に合う終電をわざと見送る。だれもいないホームから、線路ぞいを走って帰る。夜はこんなに広い。朝が来れば同じ電車に乗るけれど、降りた足あとは消えない。
# 歌詞: 曲名の言葉（しゅうでん・ばいばい）は歌わない。声: 1種類。歌をなぞるリードは入れない。シンセ・オーケストラの楽器は使わない（バンドだけ）。
from vocalo_lib import *
import gtr2_lib as G2
from groove_lib import Groove
import re as _re, os

S = Song("33", "lasttrain", "終電バイバイ（仮）", "Last Train, Bye-Bye", 176, 4, "D", "major", "ポップパンク（ボカロ）")
# v4（2026-11-26）人間「今回はドラムの音、トライデントにしよう」: 音源は v1 から crocell-punch（TRiDENT を目標に作った音源）だったが、Kawaii future bass の曲から持ちこんだ3つの設定で、その音から離れていた
#   → 部屋の響き（--space room）をやめる／ドラムを真ん中に寄せる処理（narrow）をやめる／開いたハイハットを 0.3 倍 → 0.55 倍（TRiDENT の音で作ったバンド曲 vb25 と同じ）
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags
KD = Key("D", "major")
CHH = ["D", "D", "F#7", "F#7", "G", "G", "Gm", "Gm", "D", "D", "F#7", "F#7", "G", "A", "Bb", "C"]          # サビ（半分の速さ・16小節）
CHN = ["D", "F#7", "G", "Gm", "D", "F#7", "Bb", "C"]                                                      # サビ（ふつうの速さ・8小節）
SC = []


def scene(name, n, kind, chs):
    assert len(chs) == n, (name, n, len(chs)); SC.append(name); S.scene(name, n, kind, chs)


scene("ソロ1", 4, "intro", ["D", "F#7", "G", "Gm"])
scene("A1", 12, "verse", ["D", "D", "Bm", "Bm", "G", "G", "A", "A", "Em", "G", "A", "A"])
scene("止まる", 1, "bridge", ["A"])
scene("ベル", 6, "pre", ["G", "G", "A", "A", "Bm", "Bm"])
scene("A2", 16, "verse", ["D", "D", "Bm", "Bm", "G", "G", "A", "A", "D", "D", "Bm", "Bm", "Em", "G", "A", "A"])
scene("B", 8, "pre", ["Em", "Em", "G", "G", "Bb", "Bb", "A", "A7"])
scene("ホーム", 6, "bridge", ["Bm", "Bm", "G", "G", "Em", "A"])
scene("サビ1", 16, "chorus", CHH)
scene("タクシー", 8, "pre", ["G", "G", "A", "A", "Bb", "C", "D", "D"])
scene("A3", 6, "verse", ["D", "Bm", "G", "A", "Em", "A"])
scene("走る", 8, "chorus", CHN)
scene("ソロ2", 12, "break", ["Bm", "Bm", "G", "G", "D", "D", "A", "A", "Bm", "G", "A", "A"])
scene("サビ2", 16, "chorus", CHH)
scene("ドロップ", 6, "break", ["D", "D", "C", "C", "G", "A"])
scene("サビ3", 16, "chorus", CHH)
scene("A4", 8, "verse", ["D", "D", "Bm", "Bm", "G", "Gm", "A", "A"])
scene("立ち上げ", 4, "pre", ["G", "A", "Bb", "C"])
scene("最後", 15, "chorus", ["D", "F#7", "G", "Gm"] * 2 + ["D", "F#7", "G", "A", "Bb", "C", "D"])
scene("フック", 8, "outro", ["D", "F#7", "G", "Gm", "D", "F#7", "C", "D"])
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.55

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
BSPEC = rock_bass_spec(0.17); BSPEC["ampDrive"] = 0.3
BSPEC["fx"] = [{"type": "eq", "low": 0, "mid": 4, "midHz": 900, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 2200, "high": 1}]
BASS = S.track("指弾きのベース", "bass", **BSPEC)
GT = os.environ.get("GT", "cur")                                                     # ギターの音の聞きくらべ（2026-11-26 人間「ギターの音違うかなー」）: cur＝v4／tri＝TRiDENT の音の標準（jpop-rock-drive・右は三和音）／tri5＝同じ音で左右とも根音と5度／mar5＝マーシャルで左右とも根音と5度
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.09, -0.6, tone="marshall-mid", drive=float(os.environ.get("LD", "0.35")))) for i in range(6)]
# v3: サビだけ切り出して（tools/vt3/excerpt_vocal.py）くらべた。v2 のサビ「走る」= 6.9。ギターを全部ぬくと 7.8、右ギターだけぬくと 7.47 ＝ 歌と同じ高さで歪んだ三和音をかき鳴らす右ギターが元。
#   右を「B で OK が出た音」（アンプの型なし・浅い歪み・高い所の三和音）にして 7.43、サビの上げ幅を小さくして 7.47、左の入力を 0.5 → 0.35 にして 7.66。r1＝左右とも根音と5度（7.08）、r2＝右の入力を下げる（7.05）は効かなかった
RV = os.environ.get("RV", {"cur": "r3", "tri": "r0", "tri5": "r1", "mar5": "r1"}[GT])                                                      # 右ギターの試し（サビの点数が低い元を探した。記録は docs/sound/punk-guide.md §10）
GSPB = lambda v, p: {**{k: x for k, x in rock_gtr_spec(v, p).items() if k != "guitarTone"}, "release": 0.9}
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **(GSPB(0.12, 0.6) if RV == "r3" else rock_gtr_spec(0.085, 0.6, tone="marshall-mid", drive=0.25 if RV == "r2" else 0.45))) for i in range(6)]
if GT != "cur":
    _sp = (lambda v, pn: rock_gtr_spec(v, pn)) if GT in ("tri", "tri5") else (lambda v, pn: rock_gtr_spec(v, pn, tone="marshall-mid", drive=0.5))
    for i_ in range(6): GL[i_].spec.clear(); GL[i_].spec.update(_sp(0.085, -0.6)); GR[i_].spec.clear(); GR[i_].spec.update(_sp(0.08, 0.6))
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.1, 0.1))                 # v2: 0.14 → 0.1（リードのある場面だけ 3〜4dB 大きかった）
SL, SR = G2.Strummer(GL, S, 33), G2.Strummer(GR, S, 71); SL.gap = SR.gap = 0.0
# ギターの弾き方の聞きくらべ（2026-11-26 人間「ギターの弾き方も違和感あるんよな」）。調べ直したこと（docs/sound/punk-guide.md §11）:
#   根音と5度は「1本の太い弦」のように同時に弾く／8分は全部ダウンで、形を変えない／Aメロは頭だけ開いてあとはミュート、サビは開いて弾く／2本のギターは同じことをせず、片方はオクターブなど
#   cur＝v4（歌の所で手を抜く・右は分散和音やアップダウン）／p1＝左右とも8分のダウンをまっすぐ（Aメロは左だけ、右はのばす）／p2＝p1＋Aメロの左は「頭だけ開いて、あとはやわらかいミュート」／p3＝p1＋右はオクターブ奏法
GP = os.environ.get("GP", "cur")
if GP != "cur": SL.tight = SR.tight = 5
PML = [S.track(f"Lギター（やわらかいミュート）{i + 1}", "distGuitar", **{**dict(GL[0].spec), "palmMute": "light"}) for i in range(2)] if GP == "p2" else None
P8 = ("D-d-d-d-D-d-d-d-", "D-d-d-d-D-d-d-d-", "D-d-d-d-D-d-d-d-", "D-d-d-d-D-d-D-d-")           # 8分のダウンをまっすぐ（強いのは1拍めと3拍め。4小節めだけ4拍めも強く）
import random as _rnd
_PR = _rnd.Random(5)


def r_oct(b):
    """右ギターのオクターブ奏法: 和音の3度（3度のない和音は根音）を、8分で"""
    root, third, fifth, sev, _ = G2.chord_info(simple(S.chords[b])); pc = third if third is not None else root; m = 52 + (pc - 52) % 12
    G2.octaves(SR, 2, 4, S, b, " ".join(f"{nm(m)}:0.5" + ("!" if k % 4 == 0 else "") for k in range(8)))


def strum2(b, i, L, R, space):
    c = simple(S.chords[b]); low = G2.low_shape(c, with_third=False); verse = space and S.scene_of(b)[0].startswith("A")
    if L:
        if GP == "p2" and verse: SL.bar(b, "D---............", low, feel="down"); G2.palm(PML, S, b, "....m.m.M.m.m.m.", low, _PR)
        else: SL.bar(b, P8[i % 4], low, feel="down")
    if R:
        if verse: SR.bar(b, "D---------------", low, feel="down")
        elif GP == "p3": r_oct(b)
        else: SR.bar(b, P8[i % 4], low, feel="down")

D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)
mel = lambda s, up=0: KD.mel(s, oct=4 + up)                                          # 1＝D4。歌は 5,（A3）〜 2'（E5）

# ================= 歌 =================
BAD = []


def put(name, bars_s, segs, pre=0):
    """bars_s: 小節を | で区切った旋律。segs: 句ごとの歌詞。pre: 前の場面の最後の小節から歌い始める数（食って入る句）"""
    b0 = S.sc(name)[0] - pre; lines = [x.strip() for x in bars_s.split("|")]; bars = list(range(b0, b0 + len(lines)))
    assert len(lines) == len(S.sc(name)) + pre, (name, len(lines))
    for x in lines: assert abs(sum(float(y.split(":")[1]) for y in x.split()) - 4) < 1e-6, (name, x)
    nn = sum(1 for x in " ".join(lines).split() if not x.startswith("R")); mm = sum(mora(t) for t in segs)
    if nn != mm: BAD.append((name, nn, mm, [mora(t) for t in segs]))
    ml = [x if x == "R:4" else mel(x) for x in lines]
    for b, m in zip(bars, ml):
        if m != "R:4": V.bar(b, m)
    LY.flow(bars, ml, "/".join(segs), name)


R8 = lambda d: " ".join(f"{d}:0.5" for _ in range(4))                                # 同じ音を8分で4つ
# リズムの形: 4分を並べるだけにしない（8分早く食う・付点でのばす）。パンクの歌は拍の前へつっこむ
HEAD = "R:1 3:1 3:0.5 5:1.5 | 6:2.5 5:1.5"                                           # サビの顔: 休みから入って「3 3 5 6 5」
LAST = "R:1 1':1 7:0.5 6:1.5 | 5:1.5 6:1 7:1.5 | 1':1.5 1':1.5 b7:1 | 2':3 R:1"      # サビの最後の1行（♭VI → ♭VII の上で、いちばん高い音へ）

put("A1", "5,:0.5 5,:0.5 3:1.5 3:0.5 2:1 | 1:0.5 2:1 3:2.5 | R:1.5 3:0.5 2:1 1:1 | 6,:2.5 R:1.5 | 5,:0.5 5,:0.5 4:1.5 4:0.5 3:1 | 2:0.5 3:1 4:2.5 | R:1.5 5:0.5 4:1 3:1 | 2:2.5 R:1.5 | "
          "6,:0.5 6,:0.5 5:1.5 5:0.5 4:1 | 3:0.5 4:1 5:2.5 | R:1.5 5:0.5 6:1 7:1 | 7:3 R:1",
    ["きょうもさいごのひとりだね", "あかりをけしてかぎしめて", "いつものえきへいそぐあし"])                                       # 低い音から6度以上跳ぶ。最後は導音で止まる（足が止まる）
put("A2", f"{R8(3)} 6:1.5 5:0.5 | 3:1.5 R:2.5 | {R8(1)} 5:1.5 3:0.5 | 1:1.5 R:2.5 | {R8(1)} 6:1.5 5:0.5 | 4:1.5 R:2.5 | {R8(2)} 7:1.5 6:0.5 | 5:1.5 R:2.5 | "
          f"{R8(3)} 6:1.5 5:0.5 | 3:1.5 R:2.5 | {R8(1)} 5:1.5 3:0.5 | 1:1.5 R:2.5 | {R8(2)} 5:1.5 4:0.5 | 3:0.5 4:1 5:2.5 | 6:1.5 5:1.5 7:1 | R:4",
    ["かいだんのうえ", "あしをとめたよ", "まにあうけれど", "はしらないまま", "とびらがとじて", "あかりがにげる", "こどうだけがやけにひびく"])   # 同じ音を連打してから跳ぶ
put("B", "R:0.5 2:1 4:1 6:1.5 | 5:1.5 4:1.5 2:1 | R:0.5 4:1 6:1 1':1.5 | 1':1.5 6:1.5 5:1 | R:0.5 4:1 b6:1 1':1.5 | b7:1.5 b6:1.5 4:1 | R:0.5 5:1 7:1 2':1.5 | 2':3 R:1",
    ["あさのかいぎ", "なるめざまし", "ぜんぶこんや", "わすれる"])                                                                  # 2小節の句
put("ホーム", "3:0.5 3:1 1:1.5 R:1 | 1:0.5 1:1 6,:1.5 R:1 | 4:0.5 4:1 2:1.5 R:1 | 3:0.5 3:1 1:1.5 R:1 | 4:0.5 4:1 5:1.5 R:1 | 6:0.5 7:1 2':2.5",
    ["だれも", "いない", "ほおむ", "くつの", "おとが", "ひとつ"])                                                                  # 1小節の短い句をたたみかける
put("サビ1", HEAD + " | R:1 5:0.5 #5:1 7:1.5 | 7:3 R:1 | R:1 1':1 7:0.5 6:1.5 | 5:2.5 4:1.5 | R:1 4:0.5 5:1 b6:1.5 | 5:3 R:1 | " + HEAD + " | R:1 5:0.5 #5:1 7:1.5 | 7:3 R:1 | " + LAST,
    ["こんやだけ", "ぬけだす", "きめられた", "みちから", "かえりみち", "なくして", "よるはこんなにひろい"])                          # 休みから入って最後をのばす
put("A3", "R:2.5 3:0.5 5:1 | 6:0.5 5:1 3:2.5 | R:2.5 2:0.5 4:1 | 5:0.5 4:1 2:2.5 | R:2.5 4:0.5 6:1 | 7:2.5 R:1.5", ["こんびにの", "ひかりまで", "はしる"])   # 小節のまん中から入る
put("走る", "3:0.5 3:1 5:1 6:1.5 | #5:0.5 7:1 7:1.5 R:1 | 1':0.5 7:1 6:1 5:1.5 | 4:0.5 5:1 b6:1.5 R:1 | 3:0.5 3:1 5:1 6:1.5 | #5:0.5 7:1 7:1.5 R:1 | 1':0.5 1':1 b7:1 1':1.5 | 2':3 R:1",
    ["はしりだせいま", "かぜをきるおと", "だれもしらない", "ぼくのよる"])                                                          # 2小節の句（サビの顔を、ふつうの速さで）
put("サビ2", HEAD + " | 7:4 | 7:2.5 R:1.5 | 1':4 | 1':2.5 R:1.5 | R:1 4:0.5 5:1 b6:1.5 | 5:3 R:1 | " + HEAD + " | 7:4 | 7:2.5 R:1.5 | " + LAST,
    ["あしおとがほら", "いま", "ひびいた", "ひとりきりでも", "よるはこんなにひろい"])                                              # 4小節のばす長い句
put("サビ3", "R:3 3:1 | 3:0.5 5:1.5 6:2 | 5:2 R:1 5:1 | #5:0.5 7:1.5 7:2 | R:3 1':1 | 7:0.5 6:1.5 5:2 | 4:2 R:1 4:1 | 5:0.5 b6:1.5 5:2 | R:3 3:1 | "
            "3:0.5 5:1.5 6:2 | 5:2 R:1 5:1 | #5:0.5 7:1.5 7:2 | R:3 1':1 | 7:0.5 6:1.5 5:2 | 6:0.5 7:1.5 1':2 | 1':2.5 b7:1.5 | 2':3 R:1",
    ["あさがくる", "まえまで", "このあしで", "どこまで", "いけるかな", "ためそう", "よるはこんなにひろい"], pre=1)                   # 1拍早く食って入る
put("A4", "3:1.5 2:0.5 1:1 2:1 | 3:2.5 R:1.5 | 3:1.5 2:0.5 1:1 6,:1 | 1:2.5 R:1.5 | 4:1.5 3:0.5 2:1 3:1 | 4:2.5 R:1.5 | 5:1.5 6:0.5 7:1 6:1 | 5:2.5 R:1.5", ["ひがしから", "あさのいろ", "とおくから", "はしるおと"])   # 2小節の句
put("最後", "3:0.5 3:0.5 3:1 6:2 | #5:0.5 7:1 7:1.5 R:1 | 1':0.5 7:1 6:1 5:1.5 | 4:0.5 5:1 b6:1.5 R:1 | 3:0.5 3:0.5 3:1 6:2 | #5:0.5 7:1 7:1.5 R:1 | 1':0.5 7:1 6:1 5:1.5 | 5:0.5 b6:1 5:1.5 R:1 | "
            "3:0.5 3:1 5:1 6:1.5 | 7:3 R:1 | " + LAST + " | R:4",
    ["あしたもおなじ", "でんしゃにのるよ", "それでもこんや", "おりたあしあと", "きえないよ", "よるはこんなにひろい"])                # 同じ音を連打してから跳ぶ
assert not BAD, BAD


# ================= 伴奏 =================
def bass(b, pat="r-r-r-r-r-r-r-r-"):
    r = low(S.chords[b], "E1"); out = []; i = 0
    while i < 16:
        L = 1
        while i + L < 16 and pat[i + L] == "-": L += 1
        out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N(r + {'r': 0, '5': 7, '7': 10, 'R': 12}[pat[i]])}:{L * 0.25:g}" + ("!" if i % 8 == 0 else "")); i += L
    BASS.bar(b, " ".join(out))


def simple(ch):
    m = _re.match(r"([A-G][#b]?)(.*)", ch.split("/")[0]); root, rest = m[1], m[2]
    return root + ("sus4" if "sus4" in rest else "m" if (rest.startswith("m") and not rest.startswith("maj")) else "")


TR = [None]
DN = ("D-d-d-d-D-d-d-d-", "D-d-d-D-d-d-D-d-", "D-d-d-d-D-d-D-d-", "D-d-D-d-d-d-D-D-")           # 8分のダウン（強い所が小節ごとに動く）
UD = ("D-U-D-U-D-U-D-U-", "D---D-U---U-D-U-", "D-U-D-U---U-D-U-", "D---D-U-D-U-D-U-")           # ダウンとアップ
HALF = ("D-------D-d-d-d-", "D-----d-D-------", "D-------D-d-D-d-", "D---d---D-d-d-d-")         # 半分の速さ: のばしてから刻む
ARP = ("0---1---2---1---", "0---2---1---2---", "0-1-2---1---2---", "2---1---0---1---")


def strum(b, i, L=DN, R=UD, space=False):
    """ギター左右: 左は根音と5度（低い側・ダウン）、右は三和音（まん中の弦）。space: 歌が鳴っている所では少し引く"""
    if GP != "cur": return strum2(b, i, L, R, space)
    c = simple(S.chords[b]); sung = G2.sung_slots(V, S, b) if space else None
    if L: p = L[i % 4]; SL.bar(b, G2.with_space(p, sung, keep=(0, 8)) if sung else p, G2.low_shape(c, with_third=False), feel="down")
    if R:
        p = R[i % 4]; TR[0] = G2.triad(c, TR[0], top_lo=64, top_hi=71, groups=((2, 3, 4), (3, 4, 5))) if RV == "r3" else G2.triad(c, TR[0])
        SR.bar(b, G2.with_space(p, sung, keep=(0, 8)) if sung else p, G2.low_shape(c, with_third=False) if RV == "r1" else TR[0], feel="down" if R is DN or R is HALF else 8)


def arp_r(b, i):
    if GP != "cur": return SR.bar(b, "D---------------", G2.low_shape(simple(S.chords[b]), with_third=False), feel="down") if GP != "p3" else r_oct(b)
    TR[0] = G2.triad(simple(S.chords[b]), TR[0]); G2.arp(SR, b, ARP[i % 4], TR[0])


def ring(b, both=True):
    """和音を1回鳴らしてのばす"""
    c = simple(S.chords[b]); SL.bar(b, "D---------------", G2.low_shape(c, with_third=False), feel="down")
    if both: TR[0] = G2.triad(c, TR[0]); SR.bar(b, "D---------------", TR[0], feel="down")


def lead(b, line, up=0): LEAD.bar(b, mel(line, up))


BELL = ("5:0.5 1':0.5 3':0.5 1':0.5 2':1 1':1", "#5:0.5 7:0.5 3':0.5 7:0.5 2':1 7:1", "6:0.5 1':0.5 4':0.5 1':0.5 3':1 2':1", "b6:0.5 1':0.5 4':0.5 1':0.5 2':1 1':1")   # 発車メロディのような旋律（自作）
SOLO = ("6,:0.5 1:0.5 3:1 3:0.5 2:0.5 1:1", "3:1.5 5:0.5 3:2", "4:0.5 6:0.5 1':1 1':0.5 7:0.5 6:1", "5:1.5 6:0.5 5:2", "3:0.5 5:0.5 1':0.5 5:0.5 3:0.5 5:0.5 1':0.5 2':0.5", "3':3 R:1",
        "2':0.5 1':0.5 7:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5", "2':2 7:1 5:1", "6:1 1':1 3':1 2':1", "1':1 7:0.5 6:0.5 5:2", "5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 2':0.5 3':0.5", "2':3 R:1")
GM, GQ = Groove("pogo"), Groove("drive")                                             # リズムの取り方: 主＝4分キックのたてノリ／Aメロ＝前のめりの8ビート（くじ）
NO = "................"
HK = ("X.....X.X.......", "X.....X.X.....X.", "X.....X.X.......", "X...X.X.X.......")              # 半分の速さ: スネアは3拍めだけ
HS = ("........X.......", "........X.....o.", "........X.......", "........X..o....")
HH = ("O...O...O...O...", "O...O...O...O.x.", "O...O...O...O...", "O...x...O...O...")
HB = ("r-r-r-r-r-r-r-r-", "r-r-r-r-r-r-R-5-", "r-r-r-r-r-r-r-r-", "r-r-r-R-r-r-5-r-")
TRAIN = "F3:0.5! F3:0.5 R:1 D3:0.5! D3:0.5 R:1"                                       # 線路の「ガタン・ゴトン」


def fill(b, kind):
    if kind == 0: fill_cresc(D, b, 2, True)
    elif kind == 1: fill_cresc(D, b, 1, False)
    elif kind == 2: D.S[b] = D.S[b][:8] + "X.X..X.."; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:3 C4:0.25 A3:0.25! F3:0.5!")
    elif kind == 3: D.S[b] = D.S[b][:8] + "XX......"; D.H[b] = D.H[b][:8] + "........"; D.tom(b, "R:2.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25! F3:0.25! D3:0.25!")
    elif kind == 4: D.S[b] = D.S[b][:12] + "x.xX"; D.H[b] = D.H[b][:12] + "...."
    elif kind == 5: D.S[b] = D.S[b][:8] + "X..X..X."; D.H[b] = D.H[b][:8] + "........"; D.K[b] = D.K[b][:8] + ".X..X..X"          # スネアとキックのかけ合い


def band(b, i, G=GM, k=0, space=False, L=DN, R=UD):
    """全員: ドラム（型）・キックと同じ所で打つベース・ギター左右"""
    G.drums(D, b, i + k); bass(b, G.B[(i + k) % 4]); strum(b, i + k, L, R, space)


def half(b, i, k=0):
    """サビ（半分の速さ）: スネアは3拍め、開いたハイハットを4分で、ベースは8分、ギターはのばしてから刻む"""
    D.set(b, HK[(i + k) % 4], HS[(i + k) % 4], HH[(i + k) % 4]); bass(b, HB[(i + k) % 4]); strum(b, i + k, HALF, DN)


CB = {}                                                                              # かけ声（テトの声の切れはし）
for b in range(S.nb):
    n, i, Ln, kind = S.scene_of(b); last = i == Ln - 1
    if n == "ソロ1":                                                     # リードギターのソロから。2小節は1人、3小節めで全員
        lead(b, BELL[i])
        if i >= 2: band(b, i, GM); (i == 2 and crash(D, b, "C2", 4))
        if last: fill(b, 3)
    elif n == "A1":                                                      # A: 前のめりの8ビート。左ギターは刻み、右は分散和音（後ろ4小節は右もかき鳴らす）
        GQ.drums(D, b, i); bass(b, GQ.B[i % 4]); strum(b, i, DN, None, space=True)
        if i < 8: arp_r(b, i)
        else: strum(b, i, None, UD, space=True)
        if i == 0: crash(D, b, "C2", 4)
        if i in (3, 7): fill(b, 4)
        if last: fill(b, 5)
    elif n == "止まる":                                                  # 足が止まる: 1小節、だれも鳴らさない（前の音の残りだけ）
        pass
    elif n == "ベル":                                                    # 発車ベル（リードギター）。4小節上がって、2小節落とす（走らない）
        if i < 4:
            lead(b, BELL[i], 0); bass(b, ("r---r---r---r---", "r-r-r-r-r-r-r-r-")[i // 2]); ring(b, both=i >= 2)
            D.set(b, "X...X...X...X...", NO if i < 2 else ("x...x...x...x..." if i == 2 else "x.x.x.x.xxxxXXXX"), NO)
        else:
            arp_r(b, i); bass(b, "r---------------"); D.tom(b, TRAIN)
    elif n == "A2":                                                      # A: 前半は軽く、9小節めから右ギターもかき鳴らす
        GQ.drums(D, b, i); bass(b, GQ.B[i % 4]); strum(b, i, DN, None, space=True)
        if i < 8: arp_r(b, i + 1)
        else: strum(b, i, None, UD, space=True)
        if i in (0, 8): crash(D, b, "C2", 4)
        if i in (7, 11): fill(b, 4 if i == 11 else 2)
        if last: fill(b, 0)
    elif n == "B":                                                       # B: たてノリ。♭VI の所で全員が1回止まる
        if i in (4, 5): ring(b); bass(b, "r---------------" if i == 4 else "r-------r---r-r-"); D.set(b, "X...............", NO, NO) if i == 4 else D.set(b, "X.......X...X.X.", "........x...x.xX", NO); (i == 4 and crash(D, b, "C2", 4))
        else: band(b, i, GM, space=True)
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: fill(b, 4)
        if last: fill(b, 3)
    elif n == "ホーム":                                                  # だれもいないホーム: 右ギターの分散和音とベースと「ガタン・ゴトン」
        arp_r(b, i); bass(b, "r-------r-------"); c_ = simple(S.chords[b]); SL.bar(b, "D---------------", G2.low_shape(c_, with_third=False), feel="down")   # v2: 左ギターも和音を1回鳴らしてのばす（v1 は -31dB まで落ちて、急に小さくなりすぎた）
        if i >= 2: D.tom(b, TRAIN)
        if last: D.set(b, NO, NO, NO); fill_cresc(D, b, 2, True)
    elif n in ("サビ1", "サビ2", "サビ3"):
        half(b, i, k={"サビ1": 0, "サビ2": 1, "サビ3": 2}[n])
        if i in (0, 8): crash(D, b, "C2", 4)
        if i in (4, 12): crash(D, b, "C2", 4)
        if i == 7: fill(b, 2 if n != "サビ2" else 5)
        if i >= 12 and n == "サビ3": D.set(b, GM.K[i % 4], GM.S[i % 4], GM.H[i % 4])            # 3回めの最後の1行は、ふつうの速さで走る
        if last: fill(b, 0 if n != "サビ2" else 3)
    elif n == "タクシー":                                                # にせの立ち上げ: 6小節上がって、2小節落とす
        if i < 6:
            band(b, i, GM, L=DN, R=DN); lead(b, BELL[i % 4] if i < 4 else ("1':1 2':1 1':1 2':1", "3':3 R:1")[i - 4])
            if i == 0: crash(D, b, "C2", 4)
            if i == 5: D.set(b, "X...X...X...X...", "x.x.x.x.xxxxXXXX", NO)
        else:
            arp_r(b, i); bass(b, "r---------------"); D.tom(b, TRAIN)
            if i == 6: crash(D, b, "C2", 4)
    elif n == "A3":                                                      # コンビニの光まで: ベースとドラムと分散和音 → 最後の2小節で全員
        GQ.drums(D, b, i); bass(b, GQ.B[i % 4])
        if i < 4: arp_r(b, i)
        else: strum(b, i, DN, UD, space=True)
        if last: fill(b, 0)
    elif n in ("走る", "最後"):                                          # サビ（ふつうの速さ）: たてノリで全員
        band(b, i, GM, k=1 if n == "最後" else 0, L=DN, R=DN if n == "最後" else UD)
        if i % 4 == 0: crash(D, b, "C2", 4)
        if n == "走る" and i == 3: fill(b, 4)
        if n == "最後" and i in (3, 7): fill(b, 4 if i == 3 else 2)
        if n == "最後" and i == 9: fill(b, 5)
        if n == "最後" and last: D.set(b, "X...............", NO, NO); crash(D, b, "C2", 4); ring(b); bass(b, "r---------------"); D.tom(b, "R:2 C4:0.25 C4:0.25 A3:0.25 A3:0.25 F3:0.25! F3:0.25! D3:0.25! D3:0.25!")   # 15小節め: 1打してタムだけ → フックへ
        elif last: fill(b, 3)
    elif n == "ソロ2":                                                   # リードギターのソロ: 前半は前のめりの8ビート、後半はたてノリ
        band(b, i, GQ if i < 8 else GM, L=DN, R=UD); lead(b, SOLO[i])
        if i in (0, 4, 8): crash(D, b, "C2", 4)
        if i == 7: fill(b, 2)
        if last: fill(b, 0)
    elif n == "ドロップ":                                                # ドロップ: I → ♭VII → IV。全員で刻んで、かけ声
        band(b, i, GM, L=DN, R=DN)
        if i % 2 == 0: crash(D, b, "C2", 4)
        CB[b] = "R:3 A4:0.5:へ A4:0.5:い" if i % 2 == 0 else "R:1 A4:0.5:へ A4:0.5:い R:2"
        if last: fill(b, 2); CB.pop(b)                                              # 最後の小節は、歌が食って入るので、かけ声なし
    elif n == "A4":                                                      # 朝: 分散和音とベース、線路の音。後ろ4小節でドラムが小さくもどる
        arp_r(b, i); bass(b, "r-------r-------" if i < 4 else GQ.B[i % 4])
        if i < 4: D.tom(b, TRAIN)
        else: GQ.drums(D, b, i, snare="........X.......")
        if last: fill(b, 1)
    elif n == "立ち上げ":                                                # 4小節で上がる
        ring(b) if i < 2 else strum(b, i, DN, DN); bass(b, ("r---r---r---r---", "r---r---r---r---", "r-r-r-r-r-r-r-r-", "r-r-r-r-r-r-r-r-")[i])
        D.set(b, "X...X...X...X...", ("....x.......x...", "x...x...x...x...", "x.x.x.x.x.x.x.x.", "xxxxxxxxXXXXXXXX")[i], NO)
        if i == 0: crash(D, b, "C2", 4)
    elif n == "フック":                                                  # 最初のギターの旋律にもどる → 全員で1打して止まる
        if last:
            D.set(b, "X...............", "X...............", NO); crash(D, b, "C2", 4); ring(b); bass(b, "r---------------"); lead(b, "1':4")
            continue
        band(b, i, GM, k=2, L=DN, R=UD); lead(b, BELL[i % 4] if i < 6 else "b7:1 1':1 2':1 3':1")
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i % 2 == 1: CB[b] = "R:3 A4:0.5:へ A4:0.5:い"
        if i == 3: fill(b, 4)
        if i == 6: fill(b, 0)

SL.end(S.nb); SR.end(S.nb)
S.fade_out = 0
S.desc = ("仮: 重音テトのポップパンク（176・ニ長調・約4分）。残業帰りに、走れば間に合う終電をわざと見送り、線路ぞいを走って帰る夜の歌。"
          "場面の並び・長さ・旋律の句の形・始まり方・終わり方・リズムの取り方は、くじ（form_dice.py・種 74443。合わない所は引き直し）で決めた。リードギターのソロで始まり、全員で1打して止まる。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "リードギター", mid=98, down=10, up=12, seed=33)
js = load(path); print("  ギターの強さ:", SL.velocity(js) + SR.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    remark(path, S, lambda x: x["mark"].replace("!", "").replace("?", ""))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 16, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ1", 8, None, KD), ("サビ2", 8, None, KD), ("サビ3", 0, None, KD), ("最後", 0, None, KD)], vol=0.2)          # サビは声を重ねる（全員で歌う感じ）
    chops(path, S, CB, vol=0.3, pan=0.25)
    voice_by_scene(path, S, {}, default="clear")
    sing_ends(path, S, human=0.3)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path)
QUIET = {"ホーム": 0.95, "A4": 0.95}                                                 # v2: 静かな場面は、鳴らす楽器を減らすだけで十分静か（v1 はさらに下げて -31dB・-23dB まで落ちた）
LK = float(os.environ.get("LK", "0.85"))
LOUD = {"サビ1": 1.35 * LK, "サビ2": 1.35 * LK, "サビ3": 1.35 * LK, "走る": 1.25 * LK, "最後": 1.3 * LK, "A1": 0.92, "A2": 0.9, "ドロップ": 1.2}   # v2: v1 はサビ（-19dB）が A（-17〜-18dB）より小さかった → サビを上げ、A を少し下げる
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in QUIET.items():
        for j, b in enumerate(S.sc(name)): g[b] = round(min(g[b], 1.0) * k, 4)
    for name, k in LOUD.items():
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    for name in ("ベル", "タクシー"):
        for b in S.sc(name)[-2:]: g[b] = round(min(g[b], 1.0) * 0.85, 4)
    p_["barGain"] = g[:S.nb]
js["diGuitar"] = "emily"; js["guitarWobble"] = False
GM.apply(js)                                                                         # ノリ: ぴったり（パンクは正確さ）。キックとベースは同じだけずらす
for p_ in list(js["parts"]):
    if p_.get("patch") == "kfbSineLead":
        if VOCAL: js["parts"].remove(p_); print("  歌をなぞるリードを消した")
        else:                                                                        # BGM の版: 歌の旋律は、シンセでなくリードギターが弾く（バンドだけの曲なので）
            keep = {k: p_[k] for k in ("role", "notes", "barGain") if k in p_}; p_.clear(); p_.update({"instrument": "distGuitar", **lead_gtr_spec(0.13, 0.0), **keep, "role": "歌の旋律（リードギター）"}); print("  BGM: 歌の旋律をリードギターに")
save(path, js)
