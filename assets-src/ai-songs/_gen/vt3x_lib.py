import copy
# HUMMING RELAY（vt3）の作り直しで使う部品（2026-11-11）。決まりは docs/sound/vt3-remake-plan.md。
# 人間「全部完成度高めて。同じ感じにならないように。音の深み、スケール、空間、しゃくり、ビブラート。細部まで細かく。
#   特にギターは音の作り方も演奏の仕方もプロ仕様に」「電子系音源は Kawaii future bass 系に」
# どれも「使う曲だけ・曲ごとに値を決めて」呼ぶ（全曲に同じ処理をかけない）。台本の finish() のあとで、書き出した JSON を書きかえる。
import sys, os, json, re, copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools/composer'))
from vb25_lib import midi, nm, voice, chord_pcs
from strum_groove import Groove, Lanes

TAKES = {   # GuitarSet（本物のギタリストの伴奏の録音データ）。ジャンルごとに、テンポの近い演奏から揺れ方を借りる
    "funk": ["00_Funk2-119-G_comp", "01_Funk2-119-G_comp", "02_Funk2-119-G_comp", "03_Funk2-119-G_comp", "00_Funk1-114-Ab_comp", "01_Funk1-114-Ab_comp",
             "04_Funk2-119-G_comp", "05_Funk2-119-G_comp", "02_Funk1-114-Ab_comp", "03_Funk3-112-C#_comp", "00_Funk3-112-C#_comp"],
    "funk_slow": ["00_Funk1-97-C_comp", "01_Funk1-97-C_comp", "02_Funk1-97-C_comp", "00_Funk3-98-A_comp", "01_Funk3-98-A_comp", "00_Funk2-108-Eb_comp", "01_Funk2-108-Eb_comp"],
}


def rests(r):
    """長い休みは 16 拍ずつに分ける（1つの休みは 16 拍まで）"""
    out = []
    while r > 16 + 1e-6: out.append("R:16"); r -= 16
    if r > 1e-4: out.append(f"R:{r:.4f}")
    return out


def load(path): return json.load(open(path))
def save(path, js): json.dump(js, open(path, "w"), ensure_ascii=False)


# ---------------------------------------------------------------- 歌
def vocal_polish(path, S, vib, scoop=0.6, slash=0.9, vib_min_beats=1.0, vib_start=0.42, auto=0.6, breaths=0.5, head_fade=0.05, **more):
    """歌の細かい歌い方を、曲ごとに決めた値にする。
    vib: {場面の名前 か 種類: ビブラートの深さ（セント）}。場面の中は同じ深さ（場面の境目でだけ変わる）。
    scoop: 句の頭のしゃくり（半音）。slash: 「/」をつけた音のしゃくり（半音）。プロの目安 0.5〜1.0。
    vib_min_beats: ビブラートをかける音の最短の長さ（拍）。vib_start: 音の長さの何割からかけ始めるか。"""
    js = load(path); main = js["vocals"][0]
    spb = 60.0 / S.bpm
    vm = []
    for n_, b0, L_, k_ in S.scenes:
        v = vib.get(n_, vib.get(k_, 24))
        vm += [[b0 * S.beats, v], [(b0 + L_) * S.beats - 0.01, v]]
    main.update(vibratoMap=vm, scoop=scoop, slashScoop=slash, vibMinSec=round(vib_min_beats * spb * 0.98, 3), vibStart=vib_start, auto=auto,
                breaths=breaths, hiClean=0.8, breathy=0.0, declick=1.0, headFade=head_fade)
    main.update(more)
    save(path, js)
    print(f"  歌い方: しゃくり {scoop}/{slash} 半音・ビブラートは {vib_min_beats} 拍以上の音の後ろ {round((1 - vib_start) * 100)}%・深さ {sorted(set(v for _, v in vm))} セント")


def remark(path, S, fn):
    """歌の1音ずつの印（/ しゃくり・~ ビブラート・! 強く・? 弱く・\\ フォール）を、曲ごとの決まり fn で付け直す。
    fn(info) → 印の文字列（None なら今のまま）。info: {"scene","kind","bar","pos"（小節の中の拍）,"len"（拍）,"midi","kana","head","tail","prev","mark"}"""
    js = load(path); main = js["vocals"][0]; B = S.beats
    sec = {}
    for n_, b0, L_, k_ in S.scenes:
        for bb in range(b0, b0 + L_): sec[bb] = (n_, k_)
    toks = main["notes"].split(); ev = []; t = 0.0
    for i, tok in enumerate(toks):
        L = float(tok.split(":")[1]); m = re.match(r"^([A-G][b#]?-?\d)([^:]*):([0-9.]+):(.+)$", tok)
        ev.append((i, t, L, m)); t += L
    notes = [e for e in ev if e[3]]
    n = 0
    for j, (i, t, L, m) in enumerate(notes):
        prev = notes[j - 1] if j else None; nxt = notes[j + 1] if j + 1 < len(notes) else None
        head = prev is None or t - (prev[1] + prev[2]) > 0.4
        tail = nxt is None or nxt[1] - (t + L) > 0.4
        bar = min(int(t // B + 1e-6), S.nb - 1); sc = sec.get(bar, ("", ""))
        info = {"scene": sc[0], "kind": sc[1], "bar": bar, "pos": t - bar * B, "len": L, "midi": midi(m.group(1)), "kana": m.group(4), "head": head, "tail": tail,
                "prev": midi(prev[3].group(1)) if (prev and not head) else None, "mark": m.group(2)}
        mk = fn(info)
        if mk is not None and mk != m.group(2):
            toks[i] = f"{m.group(1)}{mk}:{m.group(3)}:{m.group(4)}"; n += 1
    main["notes"] = " ".join(toks); save(path, js)
    print(f"  歌の印を付け直した: {n} 音")


def harmony(path, S, spans, steps=2, vol=0.4, lowest=55, shift=0, **more):
    """サビなどに、下のハモリ（音階で steps 段下。2＝3度下）を足す。spans: [(場面の名前, 始まりの小節（場面の中）, 終わりの小節, Key)]
    ビブラートの深さと速さを本線と変え、やわらかい声を多めに混ぜる（2つの声が溶けすぎない）"""
    js = load(path); main = js["vocals"][0]; rng = []
    for name, a, b, key in spans:
        bs = S.sc(name); b = len(bs) if b is None else b
        pcs = sorted({(midi(key.mel(f"{d}:1", oct=4).split(":")[0]) + shift) % 12 for d in range(1, 8)})   # shift: 書き出しで全体を移す半音（歌の音はもう移っている）
        rng.append(((bs[0] + a) * S.beats, (bs[0] + b) * S.beats, pcs))
    out = []; t = 0.0; cnt = 0
    for tok in main["notes"].split():
        m = re.match(r"^([A-G][b#]?-?\d)([^:]*):([0-9.]+):(.+)$", tok); L_ = float(tok.split(":")[1])
        hit = [x for x in rng if x[0] - 1e-6 <= t < x[1]] if m else []
        if m and hit:
            q = midi(m.group(1)); k = 0
            while k < steps:
                q -= 1
                if q % 12 in hit[0][2]: k += 1
            mk = m.group(2).replace("/", "").replace("!", "")
            if q >= lowest: out.append(f"{nm(q)}{mk}:{m.group(3)}:{m.group(4)}"); cnt += 1
            else: out.append(f"R:{m.group(3)}")
        else: out.append(f"R:{L_:g}")
        t += L_
    harm = dict(main)
    harm.update({"notes": " ".join(out), "volume": vol, "pan": 0, "vibrato": 20, "vibratoRate": 5.9, "vibratoMap": [], "blend": {"voice": "teto-soft", "amount": 0.45},
                 "reverb": 0.26, "dynamics": [], "consonant": 1.2, "breaths": 0.0})
    harm.update(more)
    js["vocals"].append(harm); save(path, js)
    print(f"  ハモリ（{steps} 段下）: {cnt} 音")


# ---------------------------------------------------------------- テトの声の種類（2026-11-11 人間「テトボイス5種類ぐらい用意して欲しい」）
# 曲や場面に合わせて選ぶ。teto_voice(path, "smooth") で、その曲の歌（とハモリ）の声を切りかえる。数字は細かく直してよい（出発点）。
_EQ_CLEAR = [["peak", 220, 0.8, 3], ["peak", 1600, 1.2, 2], ["peak", 2000, 2.0, 9], ["hshelf", 6500, 0.7, 10]]
TETO_VOICES = {
    # 1 クリア: これまでの標準。透き通って少しアニメ声寄り・一字一字はっきり。ポップス・ロック全般
    "clear": {"voice": "teto", "blend": {"voice": "teto-soft", "amount": 0.22}, "formant": 1.075, "breathy": 0.0, "consonant": 1.6, "air": 4.0, "eq": _EQ_CLEAR, "deess": -3.0,
              "vibratoRate": 5.3, "glide": 1.0, "legato": 0.0},
    # 2 なめらか: 滑らか音源。音と音がつながる・子音はやわらかめ。バラード・シティポップ・R&B
    "smooth": {"voice": "teto-smooth", "blend": {"voice": "teto-soft", "amount": 0.15}, "formant": 1.05, "breathy": 0.05, "consonant": 1.25, "air": 3.5,
               "eq": [["peak", 220, 0.8, 2], ["peak", 1600, 1.2, 2], ["peak", 2000, 2.0, 6], ["hshelf", 6500, 0.7, 8]], "deess": -3.0, "vibratoRate": 5.0, "glide": 1.5, "legato": 0.03},
    # 3 ウィスパー: 弱音源を多く・息まじり・近くでそっと歌う。静かな Aメロ・夜の曲・チル
    "whisper": {"voice": "teto", "blend": {"voice": "teto-soft", "amount": 0.75}, "formant": 1.04, "breathy": 0.35, "consonant": 1.2, "air": 5.0,
                "eq": [["peak", 220, 0.8, 1], ["peak", 2000, 2.0, 5], ["hshelf", 6500, 0.7, 9]], "deess": -4.0, "vibratoRate": 4.9, "glide": 1.3, "legato": 0.02},
    # 4 キュート: 幼く明るい・子音くっきり・揺れは浅く速い。カワイイ・フューチャーベース、アイドルポップ、元気な曲
    "cute": {"voice": "teto", "blend": {"voice": "teto-soft", "amount": 0.12}, "formant": 1.13, "breathy": 0.0, "consonant": 1.85, "air": 4.5,
             "eq": [["peak", 220, 0.8, 1], ["peak", 1600, 1.2, 2], ["peak", 2600, 2.0, 8], ["hshelf", 6500, 0.7, 10]], "deess": -3.0, "vibratoRate": 6.0, "glide": 0.9, "legato": 0.0},
    # 5 クール: 少し大人っぽく落ち着いた声・滑らか音源を半分・高い成分は控えめ。ジャズ、トリップホップ、ロックの低い Aメロ
    "cool": {"voice": "teto", "blend": {"voice": "teto-smooth", "amount": 0.5}, "formant": 0.975, "breathy": 0.08, "consonant": 1.35, "air": 2.5,
             "eq": [["peak", 250, 0.8, 3], ["peak", 1400, 1.2, 2], ["peak", 2000, 2.0, 5], ["hshelf", 6500, 0.7, 6]], "deess": -3.0, "vibratoRate": 5.0, "glide": 1.2, "legato": 0.015},
}
TETO_VOICE_NAMES = {"clear": "クリア", "smooth": "なめらか", "whisper": "ウィスパー", "cute": "キュート", "cool": "クール"}


def teto_voice(path, name, which=None, **more):
    """曲の歌の声を、TETO_VOICES の種類に切りかえる。which: 何番目の歌か（None＝全部。0＝本線だけ）。more で個別に上書き"""
    js = load(path)
    for i, v in enumerate(js.get("vocals", [])):
        if which is not None and i != which: continue
        v.update(copy.deepcopy(TETO_VOICES[name])); v.update(more)
    save(path, js); print(f"  テトの声: {TETO_VOICE_NAMES[name]}")


def voice_by_scene(path, S, plan, default="clear", which=0, tweak=None):
    """場面ごとにテトの声の種類を変える（2026-11-11 人間「1.3.4 を主体に曲に反映しましょう」＝クリア・ウィスパー・キュートを主体に）。
    plan: {場面の名前 か 種類(verse/pre/chorus…): 声の名前}。歌を声の種類ごとの歌に分け、ほかの場面は休みにする（声ごとに別々に合成される）。
    tweak: {声の名前: {上書きする設定}}。ハモリ・チョップ（2番目より後ろの歌）はそのまま"""
    js = load(path); main = js["vocals"][which]; per = {}
    t = 0.0
    for tok in main["notes"].split():
        L_ = float(tok.split(":")[1]); b = min(S.nb - 1, int((t + 1e-6) // S.beats)); n, i, L, k = S.scene_of(b)
        name = plan.get(n, plan.get(k, default))
        for nm_ in set(list(per.keys()) + [name]): per.setdefault(nm_, [])
        for nm_, lst in per.items():
            while sum(x[1] for x in lst) < t - 1e-6: lst.append(("R", t - sum(x[1] for x in lst)))     # あとから出てきた声は、そこまで休み
            lst.append((tok, L_) if nm_ == name or tok.startswith("R:") else ("R", L_))
        t += L_
    outs = []
    for nm_, lst in per.items():
        toks = []; acc = 0.0
        for tok, L_ in lst:
            if tok == "R" or tok.startswith("R:"): acc += L_; continue
            if acc > 1e-6: toks.extend(rests(acc)); acc = 0.0
            toks.append(tok)
        if acc > 1e-6: toks.extend(rests(acc))
        v = copy.deepcopy(main); v.update(copy.deepcopy(TETO_VOICES[nm_])); v.update((tweak or {}).get(nm_, {})); v["notes"] = " ".join(toks); outs.append(v)
        print(f"  テトの声 {TETO_VOICE_NAMES[nm_]}: {sum(1 for x in lst if x[0] != 'R' and not x[0].startswith('R:'))} 音")
    js["vocals"] = js["vocals"][:which] + outs + js["vocals"][which + 1:]; save(path, js)


def chops(path, S, bars, vol=0.3, pan=0.25, shift=0, **more):
    """ボーカルチョップ（2026-11-11 人間が調べた「ブルーアーカイブの曲でよく使われる要素」）: テトの声で、短い音を切って音程をつけて鳴らす（歌詞の意味はない「や・は・あ・ら」など）。
    bars: {小節の番号: "E4:0.5:や R:0.25 E4:0.25:や ..."}（その小節の拍の合計ぶん書く。足りないぶんは休み）。音源は配らないので、音源（SF3）にはせず歌の声としてその場で合成する。
    揺らさない・息つぎなし・子音を強め。shift: 書き出しで全体を移す半音"""
    js = load(path); main = js["vocals"][0]; out = []; cnt = 0
    for b in range(S.nb):
        t = 0.0
        for tok in bars.get(b, "").split():
            q = tok.split(":"); L_ = float(q[1]); t += L_
            if q[0] == "R": out.append(f"R:{L_:g}")
            else: out.append(f"{nm(midi(q[0]) + shift)}:{L_:g}:{q[2]}"); cnt += 1
        if S.beats - t > 1e-6: out.extend(rests(S.beats - t))
    ch = dict(main)
    ch.update({"notes": " ".join(out), "volume": vol, "pan": pan, "vibrato": 0, "vibratoMap": [], "reverb": 0.3, "dynamics": [], "consonant": 1.3, "breaths": 0.0, "auto": 0, "scoop": 0})
    ch.update(more); js["vocals"].append(ch); save(path, js)
    print(f"  ボーカルチョップ: {cnt} 音")


# ---------------------------------------------------------------- ギター
GT_BASE = {"instrument": "distGuitar", "di": "emily", "sustain": 1.3, "release": 0.12, "chorus": 0, "humanPitch": 0, "noScoop": True, "stringNoise": True,
           "humanTiming": 0, "double": False, "powerChord": False}
RIGS = {
    # ファンクのカッティング（ストラトの中間の位置の音をねらう）: コンプで粒をそろえる → クリーンのアンプ（歪ませない）→ 低い所を切り、
    #   2.4kHz のはじく音を少し出し、7kHz から丸める → 小さな部屋。コーラスなし
    "funk_cut": {"amp": "funk", "ampDrive": 0.12, "fx": [
        {"type": "compressor", "threshold": -22, "ratio": 4, "attack": 0.008, "release": 0.12},
        {"type": "filter", "kind": "highpass", "freq": 190, "q": 0.7},
        {"type": "eq", "low": -2, "mid": 2.0, "midHz": 2400, "high": 0},
        {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6},
        {"type": "room", "mix": 0.1}]},
    # ファンクの単音（「チキチキ」と歩く1本の線）: 少しだけ太く、やまびこなし
    # シティポップ・ネオソウルのカッティング（セミアコ寄りの丸いクリーン）: ゆるいコンプ → J-POP のクリーン → 6.5kHz から丸める → 部屋と短い板の残響
    "city_cut": {"di": "gretsch", "amp": "jpopClean", "ampDrive": 0.1, "fx": [
        {"type": "compressor", "threshold": -20, "ratio": 3, "attack": 0.012, "release": 0.15},
        {"type": "filter", "kind": "highpass", "freq": 170, "q": 0.7},
        {"type": "eq", "low": -1.5, "mid": 1.5, "midHz": 2000, "high": 0},
        {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.6},
        {"type": "room", "mix": 0.12}]},
    # クリーンのアルペジオ（音を伸ばして重ねる）: コンプは弱く、明るさを少し残し、板の残響を長めに
    "clean_arp": {"di": "shiny", "amp": "jpopClean", "ampDrive": 0.06, "sustain": 1.8, "release": 0.3, "fx": [
        {"type": "compressor", "threshold": -18, "ratio": 2.5, "attack": 0.02, "release": 0.2},
        {"type": "filter", "kind": "highpass", "freq": 150, "q": 0.7},
        {"type": "eq", "low": -1, "mid": 0, "midHz": 1200, "high": 1.5},
        {"type": "filter", "kind": "lowpass", "freq": 8000, "q": 0.6},
        {"type": "plate", "mix": 0.18}]},
    "funk_line": {"amp": "funk", "ampDrive": 0.18, "fx": [
        {"type": "compressor", "threshold": -24, "ratio": 5, "attack": 0.006, "release": 0.1},
        {"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7},
        {"type": "eq", "low": -2, "mid": 2.5, "midHz": 1500, "high": -1},
        {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.6},
        {"type": "room", "mix": 0.08}]},
}


class GuitarRig:
    """1本のギター。弦ごとの線（Lanes）にためて、最後に DI ギターのパート（弦ごと）にする"""
    def __init__(self, S, role, rig, pan, vol, style="funk", seed=1, amount=0.85, **over):
        self.S = S; self.role = role; self.pan = pan; self.vol = vol; self.lanes = Lanes()
        self.g = Groove(seed=seed, amount=amount, takes=TAKES[style]); self.spec = dict(RIGS[rig]); self.spec.update(over)

    def bar(self, b, pat, vo, vo_next=None, vel=1.0):
        S = self.S
        self.lanes.add(self.g.bar(b, pat, vo, vo_next or vo, S.bpm, vel), chord_change=(b == 0 or S.chords[b] != S.chords[b - 1]))

    def stop(self, b): self.lanes.stop_at(b * self.S.beats)

    def parts(self):
        total = self.S.nb * self.S.beats; self.lanes.stop_at(total); out = []
        for st, n_ in enumerate(self.lanes.notes(total)):
            if not n_: continue
            p = copy.deepcopy(GT_BASE); p.update(self.spec); p.update(role=f"{self.role}・弦{st + 1}", pan=self.pan, volume=self.vol, notes=n_); out.append(p)
        return out


def top4(ch, center=64, prev=None):
    """高い4本の弦（4〜1弦）で押さえる和音。低い2本は弾かない（ファンク・シティポップのカッティングの押さえ方）"""
    v = sorted(voice(ch.split("|")[0].split("/")[0], center, 4, prev))
    return [None, None] + [nm(x) for x in v]


def line_part(S, role, rig, pan, vol, bars, shift=0, seed=5, jitter=0.01, **over):
    """DI ギターで弾く1本の線（アルペジオ・単音のリフ・リード）。bars: {小節の番号: "A3:0.5 C4:0.5 R:1 ..."}（その小節ぶん。足りなければ休み）。
    出だしを少し揺らし（jitter 拍）、強さも少し揺らす。音名のうしろに %強さ を書けばそれを使う"""
    import random as _r
    rr = _r.Random(seed); toks = []; cur = 0.0
    for b in sorted(bars):
        t = b * S.beats
        for tok in bars[b].split():
            q = tok.split(":"); L_ = float(q[1].split("%")[0])
            if q[0] != "R":
                st = max(cur, t + rr.uniform(-jitter, jitter)); vel = int(q[1].split("%")[1]) if "%" in q[1] else int(86 + rr.uniform(-8, 8))
                if st > cur + 1e-4: toks.extend(rests(st - cur))
                d = max(0.08, t + L_ - st); toks.append(f"{nm(midi(q[0]) + shift)}:{d:.4f}%{vel}"); cur = st + d
            t += L_
    tot = S.nb * S.beats
    if tot > cur + 1e-4: toks.extend(rests(tot - cur))
    p = copy.deepcopy(GT_BASE); p.update(RIGS[rig]); p.update(over); p.update(role=role, pan=pan, volume=vol, notes=" ".join(toks)); return p


def std_mark(scoop_kinds=("chorus",), jump=5, minlen=0.75, plain=()):
    """歌の印の決まり（remark に渡す）。scoop_kinds の場面では、2小節ごとの句の頭と、大きく跳んで伸ばす音を下からすくう。plain の場面は揺らさない"""
    def fn(x):
        mk = x["mark"].replace("/", "")
        if x["kind"] in scoop_kinds or x["scene"] in scoop_kinds:
            if x["head"] and x["pos"] < 1.01 and x["bar"] % 2 == 0: mk += "/"
            elif x["prev"] is not None and x["midi"] - x["prev"] >= jump and x["len"] >= minlen: mk += "/"
        elif x["prev"] is not None and x["midi"] - x["prev"] >= jump + 2 and x["len"] >= 1.0: mk += "/"
        if x["scene"] in plain or x["kind"] in plain: mk = mk.replace("~", "").replace("/", "")
        return mk
    return fn


def set_parts(path, match, **kw):
    """役の名前に match を含むパートの設定を書きかえる（例: ベースに sustain=1.15）"""
    js = load(path); n = 0
    for p in js["parts"]:
        if match in p.get("role", ""): p.update(kw); n += 1
    save(path, js); print(f"  設定を変えた（{match}）: {n}")


def add_parts(path, parts, drop=None):
    js = load(path)
    if drop: js["parts"] = [p for p in js["parts"] if not drop(p)]
    js["parts"] += parts; save(path, js)
    print(f"  パートを足した: {len(parts)}")


def scene_gain(path, S, gains, only=None):
    """場面ごとの大きさ（サビがいちばん大きく聞こえるように、測ってから決める）。only: パートを選ぶ関数"""
    js = load(path)
    for p in js["parts"]:
        if only and not only(p): continue
        g = p.get("barGain", [1] * S.nb)
        g = list(g) + [1] * (S.nb - len(g))
        for b in range(S.nb): g[b] = round(min(2.0, g[b] * gains.get(S.scene_of(b)[0], 1.0)), 4)
        p["barGain"] = g
    save(path, js)
