#!/usr/bin/env python3
"""曲の形をサイコロで決める（2026-11-23 人間「決め事というより、ランダムにした方が同じにならないんじゃないかな」）。
使い方: python3 tools/vt3/form_dice.py [種の数字] [曲の長さ（秒）] [テンポ]
  種を書かなければ、毎回ちがう形が出る。出た形は「決まり」ではなく出発点。物語に合わない所だけ人が直す。
  場面の並び・長さ・調・速さの感じ・始まり方・終わり方・旋律の句の形を、全部くじで引く。
2026-11-25 人間「ランダムだけど合わない部分は合うように引き直すようにしようか。あとリズムの取り方も変えれるようにしよう」
  ・合わない所だけを引き直す（全体は引き直さない）。何を・なぜ引き直したかを最後に書く。前と同じ結果がほしい時は --no-fit
  ・リズムの取り方（グルーブ）も引く: 型は tools/vt3/grooves.json。テンポに合う型の中から「主」と「静かな場面用」を1つずつ。--not-groove 型の名前 で、前の曲と同じ型をさける"""
import random, sys, time

SK = "--skeleton" in sys.argv      # 骨組みだけ: 始まり方・場面の並び・長さ・旋律の句・終わり方をくじで決める（調・速さ・ドラム・厚みは人が物語に合わせて決める）
NOFIT = "--no-fit" in sys.argv
sys.argv = [a for a in sys.argv if a not in ("--skeleton", "--no-fit")]
_pos = []; _skip = False
for _a in sys.argv[1:]:
    if _skip: _skip = False; continue
    if _a in ("--min-chorus", "--not-start", "--not-groove", "--grooves"): _skip = True; continue
    _pos.append(_a)
_opts = sys.argv[1:]; sys.argv = sys.argv[:1] + _pos + ["--"] + _opts
seed = int(_pos[0]) if len(_pos) > 0 else int(time.time() * 1000) % 100000
sec = float(_pos[1]) if len(_pos) > 1 else 270
bpm = int(_pos[2]) if len(_pos) > 2 else None
MINCH = 0; EXS = []; EXG = []; ONLYG = None                                                              # --min-chorus N: サビが N 回より少ない形は引き直す ／ --not-start 言葉: その言葉が入る始まり方は引き直す（直前の曲と同じ始まり方をさける）
for _i, _a in enumerate(list(sys.argv)):
    if _a == "--min-chorus": MINCH = int(sys.argv[_i + 1])
    if _a == "--not-start": EXS.append(sys.argv[_i + 1])
    if _a == "--not-groove": EXG.append(sys.argv[_i + 1])
    if _a == "--grooves": ONLYG = sys.argv[_i + 1].split(",")                      # --grooves a,b,c: そのジャンルに合う型だけから引く
_bpm_arg = bpm
while True:
    bpm = _bpm_arg
    R = random.Random(seed)
    bpm = bpm or R.choice(range(96, 200, 4))
    bars_total = round(sec * bpm / 240)

    STARTS = ["いきなり歌（伴奏なしで1句）", "いきなり全員でサビ", "ドラムだけ", "ベースだけ", "歌なしのフックを全員で", "和音を1回鳴らしてすぐ歌", "効果音ひとつ → すぐAメロ", "曲のいちばん静かな場面から",
              "最後のサビの旋律を別の楽器で先に聞かせる", "リードギター（またはシンセ）のソロから", "手びょうしと声の切れはしだけ", "立ち上げ（上がっていく音）から始めて、いきなり落とす"]
    ENDS = ["歌の最後の音で、後奏なしに終わる", "始まりと同じ音にもどって終わる", "全員で1打して止まる", "だんだん楽器が抜けて、1つだけ残る", "フックをくり返しながら消えていく", "サビの途中でぷつっと終わる", "テンポを落として終わる", "新しい旋律を最後に1回だけ歌って終わる"]
    PARTS = ["A", "B", "サビ", "歌なしのフック", "ドロップ", "新しい歌の場面", "語り・早口の場面", "静かな場面", "立ち上げ", "にせの立ち上げ（静かな場面へ落とす）", "楽器のソロ", "止まる（1〜2小節）", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）"]
    W = [10, 5, 10, 6, 5, 7, 4, 6, 5, 4, 4, 3, 4, 3, 3]
    LENS = [4, 6, 8, 8, 8, 10, 12, 12, 16, 16] if SK else [2, 4, 4, 6, 8, 8, 8, 10, 12, 16]
    KEYMOVE = ["同じ調", "同じ調", "同じ調", "短3度上", "短3度下", "半音上", "全音上", "長3度上", "同じ主音の短調（長調）へ", "4度上"]
    FEEL = ["ふつう", "ふつう", "ふつう", "半分の速さに感じる", "倍の速さに感じる", "はねる", "3つ割り（6つで数える）", "テンポを上げる（+6〜12）", "テンポを落とす（−6〜12）"]
    DRUM = ["4つ打ち", "ハイハットの16ビート", "半分の速さ", "タム中心", "キックなし", "ブレイクビート風", "頭だけ打って止まる", "ライドで刻む", "ドラムなし", "2拍3連の形"]
    PHRASE = ["2小節の句", "3小節の句", "1小節の短い句をたたみかける", "5小節の句", "4小節のばす長い句", "1拍早く食って入る", "小節のまん中から入る", "休みから入って最後をのばす", "同じ音を連打してから跳ぶ", "高い音から下りてくる", "低い音から6度以上跳ぶ"]
    DENS = ["うすい（2〜3パート）", "ふつう", "厚い（全員）", "歌と1つの楽器だけ", "低い音なし", "高い音なし"]

    n_sc = R.randint(9, 15)
    form = []; prev = None; used = 0
    while used < bars_total - 4:
        p = R.choices(PARTS, W)[0]
        if p == prev and R.random() < 0.8: continue                     # 同じ場面を続けるのはまれに
        L = R.choice(LENS if p not in ("止まる（1〜2小節）",) else [1, 2])
        if p.startswith("サビ") and L < 8: L = 8
        L = min(L, bars_total - used)
        form.append((p, L, R.choice(KEYMOVE), R.choice(FEEL), R.choice(DRUM), R.choice(DENS), R.choice(PHRASE), R.randint(1, 10))); used += L; prev = p
    _start = R.choice(STARTS)                                              # くじの順番は前と同じ（前に使った種が、同じ結果を出すように）
    if sum(1 for x in form if x[0].startswith("サビ")) >= MINCH and not any(w in _start for w in EXS): break
    seed += 1
_end = None; FIXED = []
SUNG = ("A", "B", "サビ", "新しい歌の場面", "語り・早口の場面", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）", "静かな場面")
if not NOFIT:
    # ---- 合わない所だけ引き直す。くじは別のさいころ（R2）で引くので、元のくじの順番は変わらない ----
    R2 = random.Random(seed * 7919 + 13); form = [list(x) for x in form]
    INST = ("歌なしのフック", "ドロップ", "楽器のソロ", "立ち上げ", "にせの立ち上げ（静かな場面へ落とす）", "止まる（1〜2小節）")
    STOP, UP, FAKE = "止まる（1〜2小節）", "立ち上げ", "にせの立ち上げ（静かな場面へ落とす）"

    def why_part(i):
        """場面 i が合わない理由（合っていれば None）"""
        p, L = form[i][0], form[i][1]; nx = form[i + 1][0] if i + 1 < len(form) else None; pv = form[i - 1][0] if i else None
        if p == STOP and i in (0, len(form) - 1): return "「止まる」が曲の最初か最後にある（止まる前・あとの場面がない）"
        if p == STOP and (pv == STOP or sum(1 for x in form[:i] if x[0] == STOP) >= 2): return "「止まる」が続く、または3回め（止まりすぎると流れが切れる）"
        if p == UP and (nx is None or nx in ("静かな場面", STOP, UP, FAKE, "B", "A", "語り・早口の場面")): return f"「立ち上げ」の次が「{nx}」（上げたのに山へ行かない。落とすのは「にせの立ち上げ」の役目）"
        if p == FAKE and nx in ("サビ", "ドロップ", "歌なしのフック", "サビ（別の和音）", UP, None): return f"「にせの立ち上げ」の次が「{nx}」（落とす先の静かな場面がない）"
        if p == "A（倍の速さ）" and bpm >= 150: return f"テンポ {bpm} で「A（倍の速さ）」は、人が歌えない速さになる"
        if p == "サビ（半分の速さ）" and bpm <= 110: return f"テンポ {bpm} で「サビ（半分の速さ）」は、遅すぎて間がもたない"
        if p in INST and pv in INST and (form[i - 2][0] in INST if i >= 2 else False): return "歌のない場面が3つ続く（歌が長く出てこない）"
        if p == pv and p not in ("サビ",): return f"「{p}」が2回続く"
        if p.startswith("サビ") and pv and pv.startswith("サビ") and i >= 2 and form[i - 2][0].startswith("サビ"): return "サビが3つ続く（山ばかりで、山に聞こえなくなる）"
        if p.startswith("サビ") and sum(1 for x in form[:i] if x[0].startswith("サビ")) >= 5: return "サビが6回め（多すぎて、山に聞こえなくなる）"
        return None

    def why_len(i):
        p, L = form[i][0], form[i][1]
        if p in (UP, FAKE) and L > 8: return f"「{p}」が {L}小節は長い（上がっていくだけの時間が長すぎる）"
        if p in SUNG and L < 4: return f"歌の場面が {L}小節は短い（1句も歌いきれない）"
        if p in ("楽器のソロ", "ドロップ", "歌なしのフック") and L > 12: return f"歌のない「{p}」が {L}小節は長い"
        return None

    def why_phrase(i):
        p, L, ph = form[i][0], form[i][1], form[i][6]
        if p not in SUNG: return None
        if ph == "5小節の句" and L % 5 and L < 10: return f"{L}小節の場面に「5小節の句」は入らない"
        if ph == "3小節の句" and L % 3 and L < 9 and L != 8: return f"{L}小節の場面に「3小節の句」は半端が出る"
        if ph == "4小節のばす長い句" and L < 8: return f"{L}小節の場面に「4小節のばす長い句」は1回しか入らない"
        if ph == "1小節の短い句をたたみかける" and L >= 12: return f"{L}小節ずっと「1小節の短い句」は単調になる"
        if i and form[i - 1][0] in SUNG and form[i - 1][6] == ph: return f"前の場面と同じ句の形（{ph}）"
        return None

    def fit_pass():
        # 引き直しでサビを増やしすぎない（サビがもう4回あれば、引き直しではサビを引かない。引き直しが次の引き直しを呼ばないように）
        for _pass in range(40):
            hit = False
            for i in range(len(form)):
                for kind, why, draw in (("場面", why_part, lambda: R2.choices(PARTS, [0 if (q.startswith("サビ") and sum(1 for x in form if x[0].startswith("サビ")) >= 4) else w_ for q, w_ in zip(PARTS, W)])[0]), ("長さ", why_len, lambda: R2.choice(LENS)), ("句", why_phrase, lambda: R2.choice(PHRASE))):
                    w = why(i)
                    if not w: continue
                    col = {"場面": 0, "長さ": 1, "句": 6}[kind]; old = form[i][col]
                    for _try in range(60):
                        form[i][col] = draw()
                        if kind == "場面" and form[i][0] == STOP and form[i][1] > 2: form[i][1] = R2.choice([1, 2])
                        if kind == "場面" and form[i][0] != STOP and form[i][1] < 4: form[i][1] = R2.choice(LENS)
                        if kind == "場面" and form[i][0].startswith("サビ") and form[i][1] < 8: form[i][1] = 8
                        if form[i][col] != old and not why(i): break
                    FIXED.append(f"{i + 1}番め の{kind}: 「{old}」→「{form[i][col]}」 ／ 理由: {w}"); hit = True
            if not hit: break

    fit_pass()
    for _grow in range(12):                                                # 引き直しで短くなって、長さが足りなくなった時は、場面を引き足す（最後の場面の前に入れる）
        if sum(x[1] for x in form) >= bars_total - 6: break
        p_ = R2.choices(PARTS, W)[0]; L_ = R2.choice(LENS if p_ != STOP else [1, 2])
        if p_.startswith("サビ") and L_ < 8: L_ = 8
        L_ = min(L_, bars_total - sum(x[1] for x in form))
        if L_ < 4 and p_ != STOP: continue
        form.insert(len(form) - 1, [p_, L_, R2.choice(KEYMOVE), R2.choice(FEEL), R2.choice(DRUM), R2.choice(DENS), R2.choice(PHRASE), R2.randint(1, 10)])
        FIXED.append(f"{len(form) - 1}番め に場面を足した: 「{p_}」{L_}小節 ／ 理由: 引き直しで短くなり、曲の長さが足りない"); fit_pass()
    used = sum(x[1] for x in form); form = [tuple(x) for x in form]
    first, lastp = form[0][0], form[-1][0]
    def why_start(st):
        if "いきなり歌" in st and first not in SUNG: return f"最初の場面が「{first}」（歌がない）のに、歌から始める"
        if "いきなり全員でサビ" in st and first in (STOP, "静かな場面", FAKE): return f"最初の場面が「{first}」なのに、全員のサビから始める"
        if "立ち上げ" in st and first in (UP, FAKE): return "始まり方も最初の場面も「立ち上げ」で、同じことが続く"
        if "いちばん静かな場面" in st and first in ("ドロップ", "サビ", "歌なしのフック"): return f"最初の場面が「{first}」（大きい）のに、いちばん静かな場面から始める"
        return None
    def why_end(en):
        if ("歌の最後の音" in en or "新しい旋律を最後に" in en) and lastp not in SUNG: return f"最後の場面が「{lastp}」（歌がない）のに、歌で終わる"
        if "サビの途中" in en and not lastp.startswith("サビ"): return f"最後の場面が「{lastp}」なのに、サビの途中で終わる"
        if "フックをくり返し" in en and not any(x[0] == "歌なしのフック" for x in form): return "フックの場面がないのに、フックをくり返して終わる"
        return None
    _end0 = _end = R.choice(ENDS); _st0 = _start                              # 終わり方は、元のくじと同じ順番で引く
    while why_start(_start) or any(w in _start for w in EXS): _start = R2.choice(STARTS)
    if _start != _st0: FIXED.append(f"始まり方: 「{_st0}」→「{_start}」 ／ 理由: {why_start(_st0)}")
    while why_end(_end): _end = R2.choice(ENDS)
    if _end != _end0: FIXED.append(f"終わり方: 「{_end0}」→「{_end}」 ／ 理由: {why_end(_end0)}")
print(f"■ 形のくじ（種 {seed}）: テンポ {bpm}・{used}小節・約{used * 240 / bpm:.0f}秒")
print(f"始まり方: {_start}")
print("| 番 | 場面 | 小節 | 調（前の場面から） | 速さの感じ | ドラム | 厚み | 旋律の句 | 強さ(1-10) |\n|---|---|---|---|---|---|---|---|---|")
if SK:
    print("（骨組みだけ）"); [print(f"  {i}. {p} {L}小節" + (f" ／ 句: {ph}" if p in ("A", "B", "サビ", "新しい歌の場面", "語り・早口の場面", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）", "静かな場面") else "")) for i, (p, L, k, f, d, de, ph, e) in enumerate(form, 1)]
for i, (p, L, k, f, d, de, ph, e) in enumerate(form if not SK else [], 1):
    voc = p in ("A", "B", "サビ", "新しい歌の場面", "語り・早口の場面", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）", "静かな場面")
    print(f"| {i} | {p} | {L} | {k} | {f} | {d} | {de} | {ph if voc else '—'} | {e} |")
print(f"終わり方: {_end or R.choice(ENDS)}")
# ---- リズムの取り方（グルーブ）のくじ ----
import json, os
_G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grooves.json"), encoding="utf-8")); R3 = random.Random(seed * 104729 + 7)
_ok = [k for k, v in _G.items() if not k.startswith("_") and v["bpm"][0] <= bpm <= v["bpm"][1] and k not in EXG and (ONLYG is None or k in ONLYG)]
if _ok:
    g1 = R3.choice(_ok); _rest = [k for k in _ok if k != g1 and (_G[k]["swing16"] > 0) == (_G[g1]["swing16"] > 0)] or [k for k in _ok if k != g1] or [g1]; g2 = R3.choice(_rest)   # 静かな場面用は、はね方が同じ型から（1曲の中で、はねる・はねないを混ぜない）
    print(f"リズムの取り方（主）: {g1}「{_G[g1]['name']}」 ／ はね {_G[g1]['swing16']}・ノリ {_G[g1]['feel']}")
    print(f"リズムの取り方（静かな場面・Aメロなど）: {g2}「{_G[g2]['name']}」")
    print(f"  （テンポ {bpm} に合う型: {'・'.join(_ok)}。合わなければ --not-groove {g1} で引き直す）")
if FIXED:
    print(f"■ 合わないので引き直した所（{len(FIXED)}か所。ほかは最初のくじのまま）"); [print("  ・" + x) for x in FIXED]
elif not NOFIT: print("■ 引き直した所: なし（最初のくじで全部合っていた）")
cnt = sum(1 for x in form if x[0].startswith("サビ")); print(f"（サビ {cnt} 回。0 回なら「サビのない曲」としてそのまま作ってもよいし、引き直してもよい）")
