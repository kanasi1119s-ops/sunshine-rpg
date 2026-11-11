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
