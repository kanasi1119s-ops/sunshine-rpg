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
