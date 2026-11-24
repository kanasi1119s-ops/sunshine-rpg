#!/usr/bin/env python3
"""曲の形をサイコロで決める（2026-11-23 人間「決め事というより、ランダムにした方が同じにならないんじゃないかな」）。
使い方: python3 tools/vt3/form_dice.py [種の数字] [曲の長さ（秒）] [テンポ]
  種を書かなければ、毎回ちがう形が出る。出た形は「決まり」ではなく出発点。物語に合わない所だけ人が直す。
  場面の並び・長さ・調・速さの感じ・始まり方・終わり方・旋律の句の形を、全部くじで引く。"""
import random, sys, time

SK = "--skeleton" in sys.argv      # 骨組みだけ: 始まり方・場面の並び・長さ・旋律の句・終わり方をくじで決める（調・速さ・ドラム・厚みは人が物語に合わせて決める）
sys.argv = [a for a in sys.argv if a != "--skeleton"]
_pos = []; _skip = False
for _a in sys.argv[1:]:
    if _skip: _skip = False; continue
    if _a in ("--min-chorus", "--not-start"): _skip = True; continue
    _pos.append(_a)
_opts = sys.argv[1:]; sys.argv = sys.argv[:1] + _pos + ["--"] + _opts
seed = int(_pos[0]) if len(_pos) > 0 else int(time.time() * 1000) % 100000
sec = float(_pos[1]) if len(_pos) > 1 else 270
bpm = int(_pos[2]) if len(_pos) > 2 else None
MINCH = 0; EXS = []                                                              # --min-chorus N: サビが N 回より少ない形は引き直す ／ --not-start 言葉: その言葉が入る始まり方は引き直す（直前の曲と同じ始まり方をさける）
for _i, _a in enumerate(list(sys.argv)):
    if _a == "--min-chorus": MINCH = int(sys.argv[_i + 1])
    if _a == "--not-start": EXS.append(sys.argv[_i + 1])
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
print(f"■ 形のくじ（種 {seed}）: テンポ {bpm}・{used}小節・約{used * 240 / bpm:.0f}秒")
print(f"始まり方: {_start}")
print("| 番 | 場面 | 小節 | 調（前の場面から） | 速さの感じ | ドラム | 厚み | 旋律の句 | 強さ(1-10) |\n|---|---|---|---|---|---|---|---|---|")
if SK:
    print("（骨組みだけ）"); [print(f"  {i}. {p} {L}小節" + (f" ／ 句: {ph}" if p in ("A", "B", "サビ", "新しい歌の場面", "語り・早口の場面", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）", "静かな場面") else "")) for i, (p, L, k, f, d, de, ph, e) in enumerate(form, 1)]
for i, (p, L, k, f, d, de, ph, e) in enumerate(form if not SK else [], 1):
    voc = p in ("A", "B", "サビ", "新しい歌の場面", "語り・早口の場面", "サビ（別の和音）", "サビ（半分の速さ）", "A（倍の速さ）", "静かな場面")
    print(f"| {i} | {p} | {L} | {k} | {f} | {d} | {de} | {ph if voc else '—'} | {e} |")
print(f"終わり方: {R.choice(ENDS)}")
cnt = sum(1 for x in form if x[0].startswith("サビ")); print(f"（サビ {cnt} 回。0 回なら「サビのない曲」としてそのまま作ってもよいし、引き直してもよい）")
