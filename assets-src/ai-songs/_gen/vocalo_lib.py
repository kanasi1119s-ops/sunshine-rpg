# vocalo_lib.py — 今のボカロ曲らしさを作る部品（2026-11-15。人間「ボカロ曲の作り方徹底的に学んで、必要な要素を作曲ソフトに入れようか」）
# 調べた内容は docs/sound/vocaloid-study.md。ここには、曲の台本（vt3_NN_*.py）から呼ぶ部品を置く。
#   ① 16分のマスで書くリズム（steps / mel16）: 16分の早口・「16分＋16分休符＋4分」の決め・シンコペーションを、型のくり返しなしで1小節ずつ書ける
#   ② 丸サ進行（Just the Two of Us 進行）と、サビでの転調（marusa / up）
#   ③ リリースカットピアノ（relcut）: 和音を短く切って、すき間を空けて刻む
#   ④ 切り貼り（stutter）: 同じ音を細かくくり返す。歌のチョップ用の文字列も作れる
#   ⑤ 16ビートの4つ打ち・半分の速さ・キメ（全員で同じリズム）のドラムの型
from vt25_lib import *


def steps(pat, pitches, step=0.25, short=None):
    """16分のマスで書いたリズムを、音の並びにする。pat: 'x'＝音の頭、'-'＝のばす、'.'＝休み（1文字＝16分）。
    pitches: 音名のリスト（足りなければ最後の音をくり返す）。short: 音の長さの上限（リリースカット＝0.25 など。残りは休みになる）"""
    out, i, k = [], 0, 0
    pat = pat.replace(" ", "")
    while i < len(pat):
        c = pat[i]; j = i + 1
        if c == "x":
            while j < len(pat) and pat[j] == "-": j += 1
            L = (j - i) * step; p = pitches[min(k, len(pitches) - 1)]; k += 1
            if short and L > short: out.append(f"{p}:{short:g}"); out.append(f"R:{L - short:g}")
            else: out.append(f"{p}:{L:g}")
        else:
            while j < len(pat) and pat[j] == ".": j += 1
            out.append(f"R:{(j - i) * step:g}")
        i = j
    return " ".join(out)


def onsets(pat): return pat.count("x")


def mel16(pat, degs):
    """歌の1小節を16分のマスで書く。degs: 音階の度数（"5" "1'" "#7" など）を音の頭の数だけ。返すのは Key.mel に渡す文字列"""
    assert onsets(pat) == len(degs), (pat, degs)
    return steps(pat, [str(d) for d in degs])


MARUSA_C = ["Fmaj7", "E7", "Am7", "C7"]          # 丸サ進行（ハ長調／イ短調での形: IV△7 → III7 → VIm7 → I7）


def marusa(semi=0, last=None):
    """丸サ進行を semi 半音だけ移す。last: 4小節目を別の和音にする（例: 次の調の V7）"""
    ch = [tr_chord(c, semi) for c in MARUSA_C]
    if last: ch[3] = last
    return ch


def relcut(tracks, chord, pat, center=64, short=0.25):
    """リリースカットピアノ: 和音（3声）を pat のリズムで短く切って鳴らす。返すのは各声の文字列のリスト"""
    v = sorted(voice(chord.split("|")[0].split("/")[0], center, len(tracks)))
    return [steps(pat, [nm(m)], short=short) for m in v]


def stutter_chop(note, kana, n=4, step=0.25, tail=None):
    """歌の切り貼り: 同じ音・同じ文字を n 回、細かくくり返す（例: ぴ・ぴ・ぴ・ぴ）。chops() に渡す文字列。tail: 最後につける (音, 長さ, 文字)"""
    s = " ".join(f"{note}:{step:g}:{kana}" for _ in range(n))
    if tail: s += f" {tail[0]}:{tail[1]:g}:{tail[2]}"
    return s


# ドラムの型（16マス）: (キック, スネア, ハイハット)
BEAT16 = ("X...X...X...X...", "....X.......X...", "x.xxx.xxx.xxx.xx")        # 16ビートの4つ打ち（ハイハットは閉じた16分。裏のオープンは使わない）
BEAT16B = ("X...X...X...X.x.", "....X.......X..x", "xxx.xxx.xxx.xxx.")
HALF = ("X.........x.....", "........X.......", "x.x.x.x.x.x.x.x.")           # 半分の速さ
KIME8 = ("X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "................")           # キメ: 8分で全員いっしょ
KIME_END = ("X..X..X.X.X.....", "X..X..X.X.X.....", "................")        # キメ: 3・3・2 で止まる


# ===================== 2026-11-15 追加（人間「今の作り方に足りていないもの全て足して。音の作り方も学んでプロ仕様に」）=====================
# 調べた音作り（docs/sound/vocaloid-study.md の「プロの音作り」）:
#   ・スーパーソウの和音は、7th・9th を入れて、根音を低く、上の音を高く広げる。150〜200Hz より下を切る。2〜3kHz のきつさを少し抑える。キックで凹ませる
#   ・サブベースは真ん中（モノラル）で根音だけ。和音の音はサブに入れない（低音がにごる）
#   ・広がりは高い音ほど広く。低い音は真ん中
#   ・すき間を空ける（全部を埋めない）。うねりは、和音を変えるのでなく、音量とフィルターの動きで作る

def wide9(ch, lo=60, n=5):
    """フューチャーベースの和音の積み方: 根音を下に、5度・7度・9度・その上に3度（n 声。返すのは MIDI 番号）。
    lead の楽器は C4 より下が鳴らないので、根音は C4 以上に置く（2026-11-15: 低い声が鳴っていなかったのを直した）"""
    name = ch.split("|")[0].split("/")[0]
    r = low(name, "C1")
    while r < max(lo, 60): r += 12
    pcs = sorted({(m - r) % 12 for m in tones(name, nm(r), nm(r + 12))})
    third = next((x for x in pcs if x in (3, 4)), 4); sev = next((x for x in pcs if x in (10, 11)), 10)
    return [r, r + 7, r + sev, r + 14, r + 12 + third][:n]


def arp16(ch, pat, order, lo="A4", hi="A6", short=None):
    """16分のアルペジオ: 和音の音を order の順（番号）に、pat のリズムで鳴らす"""
    tn = tones(ch.split("|")[0].split("/")[0], lo, hi)
    return steps(pat, [nm(tn[q % len(tn)]) for q in order], short=short)


def glitch(pitch, beats=4, shape=(4, 8, 16)):
    """グリッチ（くり返しがだんだん細かくなる）: 16分 → 32分 → 64分。shape: それぞれの個数。残りは休み"""
    out, t = [], 0.0
    for n, L in zip(shape, (0.25, 0.125, 0.0625)):
        for _ in range(n):
            if t + L <= beats + 1e-9: out.append(f"{pitch}:{L:g}"); t += L
    if beats - t > 1e-6: out.append(f"R:{beats - t:g}")
    return " ".join(out)


def tape_stop(pitch, beats=2, down=12):
    """テープストップ（回転が止まるように音が落ちる）: 同じ長さの中で down 半音下へすべる"""
    return f"{pitch}:{beats:g}>{nm(midi(pitch) - down)}"


# かわいい効果音（kawaiiFx の鍵盤）: 場面の変わり目に置く「上がる音・下がる音・インパクト」
KFX = {"awa": "C4", "drop": "C#4", "kira": "D4", "kira2": "D#4", "kyu": "E4", "pyon": "F4", "up": "F#4", "down": "G4", "rev": "G#4",
       "clap": "B4", "snap": "C5", "impact": "G5", "sub": "G#5", "laser": "A5", "glitch": "D#6"}


def fx_bar(*hits, beats=4):
    """効果音の1小節。hits: (拍の位置, 名前, 長さ) を並べる。例 fx_bar((0, "impact", 1), (2, "kira", 0.5))"""
    out, t = [], 0.0
    for at, name, L in sorted(hits):
        if at - t > 1e-6: out.append(f"R:{at - t:g}")
        out.append(f"{KFX[name]}:{L:g}"); t = at + L
    if beats - t > 1e-6: out.append(f"R:{beats - t:g}")
    return " ".join(out)


# 音作りのまとまり（エフェクターの並び）。曲ごとに選んで使う（全曲に同じものを入れる決まりではない）
def rack_supersaw(hp=180, lp=7000, pump_ms=None, wide=0.35):
    """スーパーソウの和音: 低い所を切る → 150Hz 付近と 2.5kHz を少し抑える → 上を丸める →（うねるフィルター）→ 広げる → プレートの残響"""
    r = [{"type": "filter", "kind": "highpass", "freq": hp, "q": 0.7}, {"type": "eq", "low": -2, "mid": -2, "midHz": 2600, "high": 1.5},
         {"type": "filter", "kind": "lowpass", "freq": lp, "q": 0.6}]
    if pump_ms: r.append({"type": "syncfilter", "ms": pump_ms, "freq": 3200, "depth": 0.55, "q": 0.9, "mix": 0.6})
    return r + [{"type": "widen", "mix": wide}, {"type": "plate", "mix": 0.14}]


def rack_bass():
    """FM のベース: 低い所は真ん中のまま、コンプでつぶをそろえ、700Hz 付近を少し出して小さいスピーカーでも聞こえるように"""
    return [{"type": "compressor", "threshold": -20, "ratio": 4, "attack": 0.008, "release": 0.12}, {"type": "eq", "low": 1, "mid": 2, "midHz": 750, "high": -1}]


def rack_pluck(beats=0.75):
    """プラック: 低い所を切って、ピンポンディレイで左右にこだまを返す"""
    return [{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "pingpong", "beats": beats, "mix": 0.2, "feedback": 0.32}, {"type": "plate", "mix": 0.1}]


def rack_piano():
    """リリースカットピアノ: 低い所を切り、コンプで頭をそろえ、明るさを少し足す（切れ味）"""
    return [{"type": "filter", "kind": "highpass", "freq": 160, "q": 0.7}, {"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.004, "release": 0.09},
            {"type": "eq", "low": -2, "mid": 1, "midHz": 1800, "high": 2.5}]


def rack_lead():
    """電子のリード: ダブラーで太くして、付点8分のディレイ"""
    return [{"type": "doubler", "ms": 14, "depth": 0.4, "mix": 0.3}, {"type": "delay", "beats": 0.75, "mix": 0.16, "feedback": 0.28}, {"type": "plate", "mix": 0.12}]


def kero(js, idx):
    """ケロケロ声（音程を階段のように動かす調声）: 音の移りを一気に・しゃくりなし・ビブラートなし・自動の歌い回しなし。js["vocals"][idx] に効く"""
    js["vocals"][idx].update(glide=0.12, auto=0, scoop=0, slashScoop=0, vibratoMap=[], vibrato=0)


def drum_punch(js, mix=0.3, room=0.06):
    """ドラムのパラレルコンプ（つぶした音を元の音に混ぜて、太さと前に出る感じを足す）。キックとスネアだけ。スネアには短い部屋の残響も"""
    n = 0
    for p in js["parts"]:
        if p.get("instrument") in ("kick", "snare"):
            fx = [{"type": "pcomp", "threshold": -30, "ratio": 12, "attack": 0.004, "release": 0.2, "mix": mix}]
            if p["instrument"] == "snare" and room: fx.append({"type": "room", "mix": room})
            p["fx"] = fx; n += 1
    print(f"  ドラムのパラレルコンプ: {n} パート")


# ===================== 2026-11-15 ドラムの「感じ」とアクセント（人間「もうちょいドラムの感じ勉強してみて。色々アクセントとかも勉強して。」）=====================
# プロのドラマーの演奏（Groove MIDI）を測って分かったこと（docs/sound/reference-drum-accent.md）を、型にしたもの。X＝強く・x＝ふつう・o＝弱く（ゴースト）・O＝オープンハイハット
#   ・刻みは同じ強さで叩かない。ロックは拍の頭が8分ウラの 1.3倍、ポップスは 2倍。ジャズはほぼ同じ。ニューオーリンズ・アフロビートはウラの方が強い
#   ・スネアの2・4拍目はほぼ最大の強さ。ゴーストはその4分の1の強さで、入る場所は「1拍目の16分ウラ・2拍目の最後の16分・3拍目の16分ウラ・4拍目の最後の16分」
#   ・キックは 1拍目・3拍目・3拍目のウラ。ファンクは16分でずらす
#   ・オープンハイハットは、ファンクなら3拍目のウラ、ソウルなら8分のウラ全部
#   ・クラッシュは小節の頭。ときどき4拍目のウラ（次の小節へ食う）
#   ・フィルは16分が中心。スネア4割・タム3割・キック1割。後半を前半の 1.16倍に強く。クラッシュはフィルの中でなく、次の小節の頭
FEEL = {
    "rock8":    ("X.......X.x.....", "....X..o.o..X..o", "X.x.X.x.X.x.X.x."),      # ロックの8分: 頭を強く、ゴーストは少なめ
    "rock8b":   ("X.....x.X.......", "....X....o..X...", "X.x.X.x.X.x.X.O."),      # 4拍目のウラでハイハットを開く
    "pop8":     ("X.....x.X.x.....", "....X.......X..o", "X.o.X.o.X.o.X.o."),      # ポップスの8分: 頭とウラの差を大きく（2倍）
    "upbeat8":  ("X.......X.......", "....X.......X...", "x.X.x.X.x.X.x.X."),      # ウラを強く（前へはねる）
    "funk16":   ("X..x...xX.x.....", "....X..o.o..X.oo", "X.xxX.xxX.OxX.xx"),      # ファンクの16分: キックを16分でずらす・3拍目のウラで開く・ゴースト多め
    "soul8":    ("X.......x.X.....", "....X..o.o..X..o", "x.x.x.x.x.x.x.x."),      # ソウル: 刻みは平らに、ゴーストで歌う
    "half":     ("X.........x.....", "........X..o...o", "X.x.X.x.X.x.X.x."),      # 半分の速さ
    "halfopen": ("X.....x...x.....", "........X.......", "X.x.X.x.X.x.X.O."),
    "quarter":  ("X.......X.......", "....X.......X...", "X...x...X...x..."),      # 速い曲: 4分で大きく（1・3拍目を強く）
    "four":     ("X...X...X...X...", "....X.......X...", "x.X.x.X.x.X.x.X."),      # 4つ打ち: ハイハットはウラ
    "break":    ("X.........X..x..", "....X..o.o..X..o", "X.x.X.x.X.xxX.x."),      # ブレイクビート風（1小節目）
    "break2":   ("X..x......X.....", "....X..o.oX...X.", "X.x.X.xxX.x.X.x."),      # ブレイクビート風（2小節目: スネアを1つ前へずらす）
    "space":    ("X...............", "........X.......", "................"),      # キック1発とスネア1発だけ
}


def feel(D, b, name, k=None, s=None, h=None):
    """ドラムの感じ（FEEL）を1小節に置く。k・s・h で、その小節だけ差しかえられる"""
    a, c, e = FEEL[name]; D.set(b, k or a, s or c, h or e)


def fill_cresc(D, b, beats=2, toms=True):
    """フィル: 16分で、だんだん強く（弱 → ふつう → 強）。beats 拍ぶん、小節の終わりに置く。スネアからタムへ下りる。クラッシュは次の小節の頭に自分で置く"""
    n = int(beats * 4); pat = ("o" * (n // 4) + "x" * (n // 2) + "X" * (n - n // 4 - n // 2))
    s = D.S[b]; D.S[b] = s[:16 - n] + (pat if not toms else pat[:n // 2] + "." * (n - n // 2))
    D.H[b] = D.H[b][:16 - n] + "." * n; D.K[b] = D.K[b][:16 - n] + "." * (n - 1) + ("X" if False else ".")
    if toms:
        h = n - n // 2; names = ["C4", "A3", "F3", "D3"]       # 高いタム → 低いタム
        D.tom(b, f"R:{(16 - h) / 4:g} " + " ".join(f"{names[min(3, q * 4 // h)]}:0.25{'!' if q >= h // 2 else ''}" for q in range(h)))


def hat_roll(track, b, beats=1, key="C#5"):
    """ハイハットのロール（16分 → 32分）を小節の終わりに。track は kawaiiFx のパート（C#5・D5 がハイハット）"""
    n32 = int(beats * 8); track.bar(b, f"R:{4 - beats:g} " + " ".join(f"{key}:0.125" for _ in range(n32)))


# ===================== 2026-11-15 ギターの和音の弾き方（人間「ギターは和音の弾き方を学んだ方がいい。」）=====================
# プロのギタリストの伴奏（GuitarSet・弦ごとの記録）を測って分かったこと（docs/sound/reference-guitar-chords.md）:
#   ・ロックの和音の形は「根音・5度・オクターブ・その上に3度」（0 7 12 16）と「根音・5度・オクターブ」（0 7 12）が中心。根音のすぐ上に3度を置く形（0 4 7）は 2.5% しかない
#   ・1回に鳴らす弦の数は毎回ちがう（1本 21%・2本 23%・3本 19%・4本 22%・5本 10%・6本 5%）
#   ・ロックとファンクは、拍の頭も8分のウラもダウン（上から下へ）。アップは16分のウラだけ
#   ・弦から弦へのずれは1本あたり約8ミリ秒（最初から最後まで 16〜33ミリ秒）
#   ・音は次のストロークまで鳴らしつづける（97%）。切らない
import random as _vr


def gtr_shape(ch):
    """ギターの押さえ方に近い和音の形（低い弦から。MIDI 番号）。根音が6弦にあれば6本、5弦にあれば5本"""
    name = ch.split("|")[0].split("/")[0]; r = low(name, "E2")
    while r > 51: r -= 12
    pcs = {(m - r) % 12 for m in tones(name, nm(r), nm(r + 12))}
    third = 5 if (5 in pcs and 3 not in pcs and 4 not in pcs) else (2 if (2 in pcs and 3 not in pcs and 4 not in pcs) else (3 if 3 in pcs else 4))
    sev = 10 if 10 in pcs else (11 if 11 in pcs else None)
    if r <= 45:      # 6弦が根音（Eの形）: 根音・5度・（7度かオクターブ）・3度・5度・根音
        return [r, r + 7, r + (sev if sev else 12), r + 12 + third, r + 19, r + 24]
    return [r, r + 7, r + (sev if sev else 12), r + 12 + third, r + 19]      # 5弦が根音（Aの形）


def gtr_strum(tracks, S, b, pat, ch, rng, drive=True, lag_ms=8, bpm=None, strings=None):
    """ギターの和音を、人が弾くようにかき鳴らす。tracks は同じ設定のパートを6本（弦1本ずつ）。pat は16分のマス（x＝ストローク、-＝のばす、.＝休み）
    ・拍の頭: ダウン。低い弦から 4〜6本（たまに低い2〜3本だけ）・強く    ・8分のウラ: ダウン。いちばん低い弦は飛ばして 3〜4本・少し弱く
    ・16分のウラ: アップ。高い弦から 2〜3本・弱く                       ・音は次のストロークまで鳴らす"""
    v = gtr_shape(ch)[:strings] if strings else gtr_shape(ch); n = len(v); lag = lag_ms / 1000 * (bpm or S.bpm) / 60; pat = pat.replace(" ", ""); hits = [i for i, c in enumerate(pat) if c == "x"]
    for hi, i in enumerate(hits):
        e = i + 1
        while e < len(pat) and pat[e] == "-": e += 1
        L = (e - i) * 0.25; q = i % 4
        if q == 0:
            k = min(n, rng.choice([n, n, max(4, n - 1), 4, 3] if drive else [n, 4, 4, 3])); idx = list(range(0, k)); mark = "!"
        elif q == 2:
            k = rng.choice([4, 3, 3, 4]); idx = list(range(1, min(n, 1 + k))); mark = ""
        else:
            k = min(n, rng.choice([3, 2, 2])); idx = list(range(n - 1, n - 1 - k, -1)); mark = ","
        for order, j in enumerate(idx):
            d = order * lag; tracks[j].at(S.bar_beat(b) + i * 0.25 + d, f"{nm(v[j])}:{max(0.12, L - d):.3f}{mark}")


def gtr_velocity(js, match, seed=3, strong=(94, 106), mid=(76, 88), weak=(56, 68)):
    """gtr_strum で書いたギターのパートに、1音ずつの強さを付ける（! ＝強い＝拍の頭、印なし＝8分のウラ、, ＝弱い＝16分のアップ）。js は曲の JSON、match は役の名前の一部"""
    rng = _vr.Random(seed); n = 0
    for p in js["parts"]:
        if match not in p.get("role", ""): continue
        out = []
        for t in p["notes"].split():
            if t.startswith("R") or "%" in t: out.append(t); continue
            lo, hi = strong if t.endswith("!") else (weak if t.endswith(",") else mid)
            out.append(f"{t.rstrip('!,')}%{int(rng.uniform(lo, hi))}"); n += 1
        p["notes"] = " ".join(out)
    print(f"  ギターの強さを付けた（{match}）: {n} 音")


# ===== 2026-11-16: 分析ソフト（段2）で分かった弱い所を直す部品 =====
# お手本とくらべて: ベースが根音ばかり（78%）で音が少なく、4度5度で跳ぶ → 歩くベース。歌のリズムが2小節の型のくり返し → 小節ごとに型と言葉を書く。
_SMALL = "ゃゅょぁぃぅぇぉっャュョァィゥェォッ"
def mora(s): return sum(1 for c in s if c not in _SMALL and c not in " 　")


def song_lines(spec):
    """歌を1小節ずつ書く。spec: (16分の型, 度数の並び, その小節の言葉) のリスト。音の頭の数・度数の数・言葉の音の数が合っているか確かめる。
    返すのは (Key.mel に渡す行のリスト, Lyrics.flow に渡す文字)。小節の終わりに休み（8分以上）が無ければ、句は次の小節へつづく。型を小節ごとに変えて書くためのもの（同じ型の2小節くり返しをやめる）"""
    lines, words = [], []
    for i, (pat, degs, txt) in enumerate(spec):
        d = degs.split(); assert onsets(pat) == len(d) == mora(txt), (i, pat, onsets(pat), len(d), txt, mora(txt))
        lines.append(steps(pat, d)); nx = spec[i + 1][0] if i + 1 < len(spec) else "...."
        gap = (len(pat) - len(pat.rstrip("."))) + (len(nx) - len(nx.lstrip(".")))      # 次の小節の頭までの休み（16分の数）。2つ以上あれば句の切れ目
        words.append(txt + ("/" if gap >= 2 else ""))
    return lines, "".join(words)


def _root_pc(ch): return {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[ch[0]] + (1 if ch[1:2] == "#" else -1 if ch[1:2] == "b" else 0)
def _is_minor(ch): q = ch[2:] if ch[1:2] in ("#", "b") else ch[1:]; return q.startswith("m") and not q.startswith("maj")


def walk_bass(pat, kinds, c1, c2, nxt, scale_pcs, lo=28):
    """歩くベースの1小節。pat: 16分の型。kinds: 音の頭ごとに1文字。
    1〜8＝その和音の音階の何番目か（長い和音はミクソリディアン、短い和音はドリアン。1＝根音、3＝3度、5＝5度、7＝7度、8＝オクターブ）、l＝根音の1つ下、
    d＝次の和音の根音のとなりの音（調の音階で）、w＝そのもう1つ手前、a＝次の根音の半音となり。小節の後半で和音が変わるときは、後半の音は後ろの和音で数える。
    返すのは、音名の並び（steps の結果）"""
    def root(ch):
        r = _root_pc(ch) % 12 + 24
        while r < lo: r += 12
        return r
    r1, r2 = root(c1), root(c2); rn = root(nxt); cur = r2
    rn = min((rn - 12, rn, rn + 12), key=lambda x: (abs(x - cur), x)) if rn - 12 >= lo - 2 else min((rn, rn + 12), key=lambda x: abs(x - cur))
    up = rn > cur; sc = sorted(p for p in range(lo - 12, lo + 40) if p % 12 in scale_pcs)
    side = [p for p in sc if (p < rn if up else p > rn)]; side = side[::-1] if up else side      # 次の根音に近い順
    if rn == cur: side = [p for p in sc if p < rn][::-1]
    out = []; pos = [i for i, c in enumerate(pat.replace(" ", "")) if c == "x"]; assert len(pos) == len(kinds), (pat, kinds)
    for p, k in zip(pos, kinds):
        ch, r = (c2, r2) if p >= 8 else (c1, r1); iv = [0, 2, 3, 5, 7, 9, 10, 12] if _is_minor(ch) else [0, 2, 4, 5, 7, 9, 10, 12]
        if k in "12345678": n = r + iv[int(k) - 1]
        elif k == "l": n = r - 2
        elif k == "d": n = side[0]
        elif k == "w": n = side[1]
        elif k == "a": n = rn - 1 if up or rn == cur else rn + 1
        else: raise ValueError(k)
        out.append(nm(n))
    return steps(pat, out)


def split_mora(text, counts):
    """ひとつづきの言葉を、小節ごとの音の数（counts）で切り分ける（小さい「ゃ」「っ」などは前の字につける）"""
    units = []
    for c in text:
        if c in _SMALL and units: units[-1] += c
        elif c not in " 　": units.append(c)
    assert len(units) == sum(counts), (text, len(units), counts); out = []; k = 0
    for n in counts: out.append("".join(units[k:k + n])); k += n
    return out


def song_phrases(pats, degs, phrases):
    """歌を「句」で書く。pats・degs は小節ごと、phrases は句ごとの言葉（句は、小節の終わりに8分以上の休みがある所で切れる）。song_lines に渡す形にして返す"""
    spec = []; k = 0
    for ph in phrases:
        j = k
        while True:
            nx = pats[j + 1] if j + 1 < len(pats) else "...."
            if (len(pats[j]) - len(pats[j].rstrip("."))) + (len(nx) - len(nx.lstrip("."))) >= 2: break
            j += 1
        for p, d, w in zip(pats[k:j + 1], degs[k:j + 1], split_mora(ph, [onsets(p) for p in pats[k:j + 1]])): spec.append((p, d, w))
        k = j + 1
    assert k == len(pats), (k, len(pats)); return song_lines(spec)


# ===== 2026-11-16: タッピング（両手で指板をたたいてつなぐ弾き方）=====
# 学んだこと（docs/sound/reference-lead-guitar.md）: たたく（T）→ はなして左手の音を鳴らす（P）→ 左手でたたく（H）の3つでひと組。3つ組が4拍子の上をずれていく。
# 左手の2音は近く（2〜5半音）、右手の音は遠く（7半音以上）。どの音も同じ大きさ。クリーンの音で、和音（9度入り）を分けて弾く。弦を変えるのは組の変わり目。
def tap3(ch, pat, lo="E4", order="TPH", start=0, add9=True, step=1):
    """タッピングの1小節。pat: 16分の型（x の数だけ音を出す）。order: 3つ組の順（T＝右手でたたく高い音、P＝左手の低い音、H＝左手のもう1つの音）。
    start: どの高さの組から始めるか。step: 組が変わるたびに何段上（下）へ移るか。返すのは steps に渡せる音名の並び（パートには legato=True を付ける）"""
    c = ch.split("|")[0]; pcs = set(chord_pcs(c))
    if add9: pcs.add((_root_pc(c) + 2) % 12)
    lo_m = midi(lo); t = [m for m in range(lo_m, lo_m + 29) if m % 12 in pcs]; n = onsets(pat); out = []
    for i in range(n):
        g = start + (i // len(order)) * step; a = t[g % max(1, len(t) - 6)]; b = next(m for m in t if m > a + 1); T = next(m for m in t if m >= a + 7)
        out.append(nm({"T": T, "P": a, "H": b}[order[i % len(order)]]))
    return steps(pat, out)
