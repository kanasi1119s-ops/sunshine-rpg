#!/usr/bin/env python3
"""お手本のカルテから「学んだ型の引き出し」を作る（2026-11-16）。曲を作る前に読む用。
使い方: python3 tools/song-analyzer/library.py <カルテのフォルダ> --md <出力.md> --json <出力.json>
ジャンルごとに、数字の幅（まん中の半分＝25%〜75%）と、型をまとめる:
  ・ドラム: 位置ごとの打つ割合から「よく打つ場所」を1小節の絵にする（1曲ずつの型は聞き取りのゆれが大きいので、割合の平均を使う）
  ・ベース: 1小節の音の数、根音の割合、動き方、音を出す場所の多い型
  ・和音: 変わる速さ、根音の動き方、短いコード進行（何曲に出てきたか）
  ・歌: 音の長さ、句の長さ、跳ぶ割合、くり返し方
  ・音色: キック・スネアの高さと長さ、歌のビブラート、広がり
1曲ぶんの進行や旋律は入れない（カルテにも入っていない）。"""
import sys, os, json, glob, collections
import numpy as np

GJ = {"pop": "ポップ", "rock": "ロック", "metal": "メタル", "funk": "ファンク", "dance": "ダンス", "electronic": "エレクトロニクス", "vocaloid": "ボカロ", "jpop": "J-POP", "kpop": "K-POP", "other": "そのほか"}
kd = sys.argv[1]; md = sys.argv[sys.argv.index("--md") + 1] if "--md" in sys.argv else None; jp = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
G = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(kd, "ref-*.karte.json"))):
    k = json.load(open(f)); g = GJ.get((k.get("source") or {}).get("genre", "other"), "そのほか"); G[g].append(k); G["ぜんぶ"].append(k)


def rng(vals, nd=1):
    v = [x for x in vals if x is not None]
    if len(v) < 2: return None
    return [round(float(np.percentile(v, 25)), nd), round(float(np.median(v)), nd), round(float(np.percentile(v, 75)), nd)]


def get(k, *path):
    for p in path:
        if not isinstance(k, dict) or p not in k: return None
        k = k[p]
    return k


def picture(p, hi=0.5, lo=0.25): return "".join("X" if x >= hi else "x" if x >= lo else "." for x in p)


def merge(dicts):
    c = collections.defaultdict(list)
    for d in dicts:
        for a, b in (d or {}).items(): c[a].append(b)
    n = max(1, len([d for d in dicts if d])); return {a: round(sum(b) / n, 3) for a, b in sorted(c.items(), key=lambda kv: -sum(kv[1]))}


LIB = {}
for g, ks in G.items():
    s2 = [k.get("stage2") or {} for k in ks]; s3 = [k.get("stage3") or {} for k in ks]; L = {"曲の数": len(ks), "テンポ": rng([k["tempo"] for k in ks], 0)}
    # ドラム
    pk = [get(s, "ドラム", "位置ごとの割合", "キック") for s in s2]; ps = [get(s, "ドラム", "位置ごとの割合", "スネア") for s in s2]; ph = [get(s, "ドラム", "位置ごとの割合", "刻み") for s in s2]
    # 小節の頭の当て方が曲ごとに1〜3拍ずれることがあるので、平均する前に「スネアが2・4拍目に来る向き」に拍の単位で回してそろえる（スネアが毎拍ある曲は、そのまま）
    for i in range(len(ks)):
        if not (pk[i] and ps[i] and len(pk[i]) == 16 and len(ps[i]) == 16): continue
        sc = lambda r: ps[i][(4 + r) % 16] + ps[i][(12 + r) % 16] - ps[i][r % 16] - ps[i][(8 + r) % 16] + 0.5 * pk[i][r % 16]
        r = max((0, 4, 8, 12), key=sc)
        if r and sc(r) > sc(0) + 0.15: pk[i] = pk[i][r:] + pk[i][:r]; ps[i] = ps[i][r:] + ps[i][:r]; ph[i] = (ph[i][r:] + ph[i][:r]) if ph[i] and len(ph[i]) == 16 else ph[i]
    def avg(ps_):
        v = [p for p in ps_ if p and len(p) == 16]; return [round(float(x), 2) for x in np.mean(v, 0)] if v else None
    d = {"曲の数": len([p for p in pk if p])}
    for nm, p in (("キック", avg(pk)), ("スネア", avg(ps)), ("刻み", avg(ph))):
        if p: d[nm + "をよく打つ場所（X＝半分以上の小節・x＝4回に1回以上）"] = picture(p); d[nm + "の位置ごとの割合"] = p
    d["刻みの細かさ（1小節の打数）"] = rng([get(s, "ドラム", "刻みの細かさ（1小節の打数・中央値）") for s in s2]); d["フィルらしい小節（8小節あたり）"] = rng([get(s, "ドラム", "フィルらしい小節の数（8小節あたり）") for s in s2], 2)
    d["前か2小節前との似かた（キックとスネア）"] = rng([get(s, "ドラム", "前か2小節前との似かた（キックとスネア・8分にまとめて）") for s in s2], 2); d["スネアの弱い打の割合"] = rng([get(s, "ドラム", "スネアの弱い打（ゴースト）の割合") for s in s2], 2)
    L["ドラム"] = d
    # ベース
    b = {"1小節の音の数": rng([get(s, "ベース", "1小節の音の数（中央値）") for s in s2]), "根音を弾いている割合": rng([get(s, "ベース", "和音の根音との関係", "根音") for s in s2], 2), "音域（半音）": rng([get(s, "ベース", "音域（半音）") for s in s2], 0),
         "動き方（平均）": merge([get(s, "ベース", "動き方") for s in s2]), "根音いがいで弾く音（平均）": merge([get(s, "ベース", "和音の根音との関係") for s in s2]), "前か2小節前との似かた": rng([get(s, "ベース", "前か2小節前との似かた（音を出す場所・8分にまとめて）") for s in s2], 2)}
    pc = collections.Counter(); ns = collections.Counter()
    for s in s2:
        for e in get(s, "ベース", "型のくり返し", "多い型") or []: pc[e["型"]] += e["割合"]; ns[e["型"]] += 1
    b["音を出す場所の多い型（8分。x＝音の頭、-＝のばす、.＝休み）"] = [{"型": p, "曲数": ns[p]} for p, _ in sorted(pc.items(), key=lambda kv: (-ns[kv[0]], -kv[1]))[:8]]; L["ベース"] = b
    # 和音
    c = {"和音が変わる回数（1小節あたり）": rng([get(s, "和音", "和音が変わる回数（1小節あたり）") for s in s2], 2), "根音が変わる回数（1小節あたり）": rng([get(s, "和音", "根音が変わる回数（1小節あたり）") for s in s2], 2),
         "使っている根音の数": rng([get(s, "和音", "使っている根音の数（全体の3%以上）") for s in s2], 0), "小節の途中で変わる小節の割合": rng([get(s, "和音", "小節の途中で変わる小節の割合") for s in s2], 2),
         "根音の動き方（平均）": merge([get(s, "和音", "根音の動き方の割合") for s in s2]), "和音の種類（平均）": merge([get(s, "和音", "和音の種類の割合") for s in s2])}
    fr = {}
    for s in s2:
        for n, lst in (get(s, "和音", "短いコード進行（多い順）") or {}).items():
            for e in lst: fr.setdefault(n, {}).setdefault(e["進行"], []).append(e["回数"])
    # 調の当て方がずれると度数もずれる（短調の曲で、5番目の音を主音とまちがえやすい）。だから、はじめの和音をドにそろえた形でも数える（調の当て方によらない）
    DEG = {"I": 0, "♭II": 1, "II": 2, "♭III": 3, "III": 4, "IV": 5, "♭V": 6, "V": 7, "♭VI": 8, "VI": 9, "♭VII": 10, "VII": 11}; NM = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
    def keyfree(prog):
        out = []; base = None
        for x in prog.split(" → "):
            q = "m" if x.endswith("m") else ""; d = DEG.get(x[:-1] if q else x)
            if d is None: return None
            base = d if base is None else base; out.append(NM[(d - base) % 12] + q)
        return " → ".join(out)
    kf = {}
    for i, s in enumerate(s2):
        for n, lst in (get(s, "和音", "短いコード進行（多い順）") or {}).items():
            for e in lst:
                kk = keyfree(e["進行"])
                if kk: kf.setdefault(n, {}).setdefault(kk, {}).setdefault(i, 0); kf[n][kk][i] += e["回数"]
    c["短いコード進行（はじめの和音をドにそろえた形・何曲に出てきたか）"] = {n: [{"進行": p, "曲数": len(v), "回数": sum(v.values())} for p, v in sorted(d_.items(), key=lambda kv: (-len(kv[1]), -sum(kv[1].values())))[:14]] for n, d_ in sorted(kf.items())}
    c["短いコード進行（何曲に出てきたか）"] = {n: [{"進行": p, "曲数": len(v), "回数": sum(v)} for p, v in sorted(d_.items(), key=lambda kv: (-len(kv[1]), -sum(kv[1])))[:12]] for n, d_ in sorted(fr.items())}; L["和音"] = c
    # 歌
    spb = [60 / k["tempo"] for k in ks]; vs = [get(s, "歌の旋律の形") for s in s2]
    def vv(key, mul=None, nd=2): return rng([(v[key] * (mul[i] if mul else 1)) for i, v in enumerate(vs) if v and v.get(key) is not None], nd)
    L["歌"] = {"曲の数": len([v for v in vs if v and "句の数" in v]), "音の長さ（秒）": vv("音の長さの中央値（拍）", spb), "句の長さ（秒）": vv("句の長さ（拍・中央値）", spb), "句の最後の音の長さ（秒）": vv("句の最後の音の長さ（拍）", spb), "16分以下の短い音の割合": vv("16分以下の音の数の割合"),
              "2拍以上の長い音の割合": vv("2拍以上の音の数の割合"), "長い音が拍のウラで始まる割合": vv("長い音が拍のウラ（食って入る）で始まる割合"), "跳ぶ動き（5半音以上）の割合": vv("跳ぶ動き（5半音以上）の割合"), "音域（半音）": vv("音域（半音）", None, 0),
              "前か2小節前との似かた（リズム）": vv("前か2小節前との似かた（音を出す場所・8分にまとめて）"), "句の形（平均）": merge([v.get("句の形の割合") for v in vs if v])}
    # 音色
    t = {}
    for nm, path in (("キックの高さ（Hz）", ("ドラムの音", "キック", "いちばん強い高さ（Hz）")), ("キックの長さ（ミリ秒）", ("ドラムの音", "キック", "長さ（ミリ秒・−20dB まで）")), ("スネアの胴の高さ（Hz）", ("ドラムの音", "スネア", "胴の高さ（Hz）")),
                     ("スネアの余韻（ミリ秒）", ("ドラムの音", "スネア", "余韻（ミリ秒・−20dB まで）")), ("ベースの音の重心（Hz）", ("ベース", "音の重心（Hz）")), ("ベースの倍音の下がり方（dB／オクターブ）", ("ベース", "倍音の形", "倍音の下がり方（dB／オクターブ）")),
                     ("ベースの大きさのゆれ幅（dB）", ("ベース", "大きさのゆれ幅（dB・鳴っている所）")), ("和音の楽器の音の重心（Hz）", ("和音の楽器", "音の重心（Hz）")), ("和音の楽器の左右の広がり（中）", ("和音の楽器", "左右の広がり（中 250Hz〜2kHz）")),
                     ("和音の楽器の大きさのゆれ幅（dB）", ("和音の楽器", "大きさのゆれ幅（dB・鳴っている所）")), ("和音の楽器のへこみの深さ（dB）", ("和音の楽器", "拍に合わせたへこみ", "へこみの深さ（dB）")), ("歌の音の重心（Hz）", ("歌", "音の重心（Hz）")),
                     ("歌のビブラートの深さ（セント）", ("歌", "ビブラート", "ビブラートの深さ（セント・片側）")), ("歌のビブラートの速さ（Hz）", ("歌", "ビブラート", "ビブラートの速さ（Hz）")), ("歌のビブラートがある割合", ("歌", "ビブラート", "そのうちビブラートがある割合"))):
        t[nm] = rng([get(s, *path) for s in s3], 2 if "割合" in nm or "広がり" in nm else 1)
    wf = collections.Counter(get(s, "ベース", "倍音の形", "波の形（たぶん）") for s in s3); wf.pop(None, None); t["ベースの波の形（曲数）"] = dict(wf.most_common()); L["音色"] = t
    # 全体
    L["全体"] = {"伴奏が休んでいる時間（%）": rng([k["rests"]["accomp"] * 100 for k in ks if "rests" in k and "accomp" in k["rests"]]) if all("rests" in k for k in ks) else None}
    LIB[g] = L

if jp: json.dump(LIB, open(jp, "w"), ensure_ascii=False, indent=1)
R = lambda r, u="": "—" if not r else f"{r[1]}{u}（{r[0]}〜{r[2]}）"
order = ["ぜんぶ"] + [g for g in GJ.values() if g in LIB]
T = ["# 学んだ型の引き出し（お手本のカルテから）", "", f"お手本 {LIB['ぜんぶ']['曲の数']}曲（" + "・".join(f"{g} {LIB[g]['曲の数']}" for g in order[1:]) + "）。ネットレーベルの、自由なライセンス（CC BY・CC BY-SA・CC0）の曲だけ。",
     "数字は「まん中の値（25%〜75%の幅）」。機械の聞き取りなので、目安。1曲ぶんの進行や旋律は入っていない。", "", "**信用しにくい所**: ①根音が半音で動く進行（C → B、C → D♭ など）は、聞き取りのゆれで多めに出る（自分の曲でも、書いていないのに 1〜29% と出た）。②ドラムの絵は、テンポや小節の頭の当てまちがいでぼやける。③歌の数字は、歌の少ない曲（ダンス・エレクトロニクス）では声の切れはしを測っている。", "", "## 使い方", "", "- 曲を作る前に、そのジャンルの行を見て、幅から外れすぎていないかを確かめる（外すなら、わざと外す）。",
     "- ドラムの絵は「その場所を打つ小節の割合」。X の場所を骨組みにして、x の場所を小節ごとに入れたり抜いたりする。", "- 短いコード進行は、度数（I＝その調の1番目）。そのまま並べるのではなく、つなぎ方の材料にする。", ""]
T += ["## ジャンルごとの数字", "", "| 項目 | " + " | ".join(order) + " |", "|---|" + "---|" * len(order)]
rows = [("テンポ", lambda L: R(L["テンポ"])), ("ドラム: 刻みの細かさ（1小節の打数）", lambda L: R(L["ドラム"]["刻みの細かさ（1小節の打数）"])), ("ドラム: フィル（8小節あたり）", lambda L: R(L["ドラム"]["フィルらしい小節（8小節あたり）"])),
        ("ドラム: 前か2小節前との似かた", lambda L: R(L["ドラム"]["前か2小節前との似かた（キックとスネア）"])), ("ベース: 1小節の音の数", lambda L: R(L["ベース"]["1小節の音の数"])), ("ベース: 根音を弾く割合", lambda L: R(L["ベース"]["根音を弾いている割合"])),
        ("ベース: となりの音へ動く割合", lambda L: str(L["ベース"]["動き方（平均）"].get("となりの音へ（1〜2半音）", "—"))), ("ベース: 4度・5度で跳ぶ割合", lambda L: str(L["ベース"]["動き方（平均）"].get("5度・4度（5〜7半音）", "—"))),
        ("和音: 根音が変わる回数（1小節）", lambda L: R(L["和音"]["根音が変わる回数（1小節あたり）"])), ("和音: 使う根音の数", lambda L: R(L["和音"]["使っている根音の数"])), ("和音: 小節の途中で変わる割合", lambda L: R(L["和音"]["小節の途中で変わる小節の割合"])),
        ("歌: 音の長さ（秒）", lambda L: R(L["歌"]["音の長さ（秒）"])), ("歌: 句の長さ（秒）", lambda L: R(L["歌"]["句の長さ（秒）"])), ("歌: 句の最後の音（秒）", lambda L: R(L["歌"]["句の最後の音の長さ（秒）"])), ("歌: 跳ぶ動きの割合", lambda L: R(L["歌"]["跳ぶ動き（5半音以上）の割合"])),
        ("歌: リズムの似かた", lambda L: R(L["歌"]["前か2小節前との似かた（リズム）"])), ("歌: ビブラートの深さ（セント）", lambda L: R(L["音色"]["歌のビブラートの深さ（セント）"])), ("キックの高さ（Hz）", lambda L: R(L["音色"]["キックの高さ（Hz）"])),
        ("キックの長さ（ミリ秒）", lambda L: R(L["音色"]["キックの長さ（ミリ秒）"])), ("スネアの胴の高さ（Hz）", lambda L: R(L["音色"]["スネアの胴の高さ（Hz）"])), ("スネアの余韻（ミリ秒）", lambda L: R(L["音色"]["スネアの余韻（ミリ秒）"])),
        ("ベースの大きさのゆれ幅（dB）", lambda L: R(L["音色"]["ベースの大きさのゆれ幅（dB）"])), ("和音の楽器の左右の広がり", lambda L: R(L["音色"]["和音の楽器の左右の広がり（中）"])), ("和音の楽器のへこみの深さ（dB）", lambda L: R(L["音色"]["和音の楽器のへこみの深さ（dB）"]))]
for nm, fn in rows: T.append(f"| {nm} | " + " | ".join(fn(LIB[g]) for g in order) + " |")
T += ["", "## ドラム: よく打つ場所（1小節を16に分けた絵）", "", "X＝半分以上の小節で打つ、x＝4回に1回以上、.＝あまり打たない。小節の頭の当て方が曲ごとにずれるので、スネアが2・4拍目に来る向きにそろえてから平均した。テンポを半分や倍に聞きまちがえた曲もまざるので、絵はぼやける。目安。", ""]
for g in order:
    d = LIB[g]["ドラム"]; T.append(f"**{g}**（{d['曲の数']}曲）"); T.append("```")
    for nm in ("キック", "スネア", "刻み"):
        key = nm + "をよく打つ場所（X＝半分以上の小節・x＝4回に1回以上）"
        if key in d: T.append(f"{nm:　<4} {d[key][:4]} {d[key][4:8]} {d[key][8:12]} {d[key][12:]}")
    T += ["```", ""]
T += ["## ベース: 音を出す場所の多い型（8分。x＝音の頭、-＝のばす、.＝休み）", ""]
for g in order: T.append(f"- **{g}**: " + "／".join(f"`{e['型']}`（{e['曲数']}曲）" for e in LIB[g]["ベース"]["音を出す場所の多い型（8分。x＝音の頭、-＝のばす、.＝休み）"][:6]))
T += ["", "## 和音: 根音の動き方（平均の割合）", ""]
for g in order: T.append(f"- **{g}**: " + "／".join(f"{a} {int(b * 100)}%" for a, b in list(LIB[g]["和音"]["根音の動き方（平均）"].items())[:6]))
T += ["", "## 短いコード進行（はじめの和音をドにそろえた形。何曲に出てきたか）", "", "調の当て方によらない数え方。「C → A♭」は「長い和音から、長3度下の長い和音へ」の意味で、どの調でも同じ動きを1つに数える。", ""]
for g in order:
    T.append(f"- **{g}**")
    for n, lst in LIB[g]["和音"]["短いコード進行（はじめの和音をドにそろえた形・何曲に出てきたか）"].items():
        top = [e for e in lst if e["曲数"] >= 2][:10] or lst[:3]; T.append(f"  - 和音{n}つ: " + "／".join(f"{e['進行']}（{e['曲数']}曲）" for e in top))
T += ["", "## 短いコード進行（度数。調の当て方がずれていると、度数もずれる。目安）", ""]
for g in order:
    T.append(f"### {g}"); T.append("")
    for n, lst in LIB[g]["和音"]["短いコード進行（何曲に出てきたか）"].items():
        top = [e for e in lst if e["曲数"] >= (2 if g != "ぜんぶ" else 3)][:10] or lst[:4]; T.append(f"- 和音{n}つ: " + "／".join(f"{e['進行']}（{e['曲数']}曲）" for e in top))
    T.append("")
txt = "\n".join(T)
if md: open(md, "w").write(txt + "\n")
print(txt)
