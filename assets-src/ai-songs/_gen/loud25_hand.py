# ラウド25曲を「手で書く」ための共通部品（2026-10-22。1曲目「逆光プリズム」の作り方を部品にしたもの）
# 使い方: 曲ごとのファイル（loud25_NN_*.py）で、SPEC（設計）と手書きの旋律を書き、build() で組み立ててから、ここの部品で仕上げる。
# 決まりごと（人間の感想から。docs/sound/loud-rock-patterns.md）
# - リードは「2 マーシャル系」（namJVM）。標準の lead アンプは使わない
# - キーボード・シンセ・ライザーは入れない（電子音感が強すぎる）
# - バスドラはトリガー（punch）＋重みの層（録音のキックの低音だけ）
# - ブリッジミュートの刻みは使わない。長い休み（R:8 より長い）は4拍ずつに分ける
import re, json, copy
from loud25_lib import midi, name, at_least

LEAD_TONE = dict(humanPitch=0, noScoop=True, di="emily", double=False, chorus=0,
                 amp="namJVM", ampDrive=0.7, ampGate=10, ampTight=0.6, ampTightHz=150, ampCabIr="jd-greenback-4x12-01", reverb=0.12,
                 fx=[{"type": "eq", "low": -2, "mid": 2.5, "midHz": 1000, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 7500, "q": 0.7},
                     {"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.18}])
ARP_TONE = dict(LEAD_TONE, ampDrive=0.35, fx=[{"type": "eq", "low": -3, "mid": 1.5, "midHz": 1000, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.7},
                                              {"type": "delay", "beats": 0.75, "mix": 0.22, "feedback": 0.35}, {"type": "plate", "mix": 0.24}])

TOK = re.compile(r"^(.*):([\d.]+)([^\d.]*)$")

def toks(notes):
    out, t = [], 0.0
    for tk in notes.split():
        m = TOK.match(tk); out.append([t, float(m.group(2)), m.group(1), m.group(3)]); t += float(m.group(2))
    return out

def total(notes):
    if notes.startswith("g:"): return (len(notes) - 2) / 4
    return sum(d for _, d, _, _ in toks(notes))

def put(p, a, b, new=""):
    """パート p の [a, b) 拍を new（音の並び。空なら休み）で置きかえる。ドラムの g: 形式は new に16分の文字列も使える"""
    n = p["notes"]
    if n.startswith("g:"):
        g = list(n[2:])
        for i in range(int(round(a * 4)), int(round(b * 4))): g[i] = "."
        for j, ch in enumerate(new): g[int(round(a * 4)) + j] = ch
        p["notes"] = "g:" + "".join(g); return
    out = []
    for t, d, h, suf in toks(n):
        e = t + d
        if e <= a + 1e-9 or t >= b - 1e-9: out.append(f"{h}:{d:g}{suf}"); continue
        if t < a - 1e-9: out.append(f"{h}:{a - t:g}{suf}")
        if t <= a + 1e-9 or t < a: out.append(new if new else f"R:{b - a:g}")
        if e > b + 1e-9: out.append(f"R:{e - b:g}")
    p["notes"] = " ".join(x for x in out if x)

def split_rests(n):
    if n.startswith("g:"): return n
    out = []
    for tk in n.split():
        m = re.match(r"^R:([\d.]+)$", tk)
        if m and float(m.group(1)) > 4:
            d = float(m.group(1))
            while d > 4 + 1e-9: out.append("R:4"); d -= 4
            out.append(f"R:{d:g}")
        else: out.append(tk)
    return " ".join(out)

def starts(form, beats=4):
    """区間の名前 → (始まりの拍, 小節数)"""
    st, pos = {}, 0
    for sid, kind, n, prog in form: st[sid] = (pos * beats, n); pos += n
    return st

def cell_riff(cell, roots, low, step=0.5, start=0, accent_every=None, end_root=True, per_bar=None):
    """かたまり cell（根音からの半音の数。None は休み）を step 拍ずつ並べる。roots は小節ごとの根音（0〜11）。
    かたまりの頭に強弱。最後の音は根音にもどす（end_root）。per_bar＝1小節の拍数（既定 4）"""
    per_bar = per_bar or 4
    n = int(round(len(roots) * per_bar / step)); toks_ = []
    for j in range(n):
        root = at_least(roots[int(j * step // per_bar)], low)
        idx = (j + start) % len(cell)
        iv = cell[idx]
        if j == n - 1 and end_root: iv = 0
        if iv is None: toks_.append(f"R:{step:g}"); continue
        acc = "!" if (idx == 0 or (j == n - 1 and end_root)) else ""
        toks_.append(f"{name(root + iv)}:{step:g}{acc}")
    return " ".join(toks_)

def retone_leads(parts, tone=LEAD_TONE, skip=("リードギター（分散和音）",)):
    for p in parts:
        if p["instrument"] == "leadGuitar" and p["role"] not in skip:
            p.pop("guitarTone", None); p.update(json.loads(json.dumps(tone)))

def add_heavy_kick(parts, volume=0.2):
    k = [p for p in parts if p["instrument"] == "kick"][0]
    heavy = {kk: vv for kk, vv in k.items() if kk not in ("trigger", "triggerVolume")}
    heavy.update({"role": "キック（重み）", "volume": volume, "gainDb": -3,
                  "fx": [{"type": "eq", "low": 6, "mid": -4, "midHz": 400, "high": -8}, {"type": "filter", "kind": "lowpass", "freq": 180, "q": 0.9}]})
    parts.insert(parts.index(k) + 1, heavy)
    return heavy

def split_lead(parts, st, quiet_sids, volume=0.105, role="リード（Aメロ・ブリッジ）"):
    """quiet_sids の区間の旋律を、同じ音色で小さめの別パートに移す"""
    lead = [p for p in parts if p["role"] == "リード（旋律）"][0]
    quiet = json.loads(json.dumps(lead)); quiet["role"] = role; quiet["volume"] = volume
    full = total(lead["notes"])
    keep = [st[s] for s in quiet_sids if s in st]
    for a, n in keep: put(lead, a, a + n * 4)
    edges = sorted(set([0, full] + [a for a, n in keep] + [a + n * 4 for a, n in keep]))
    inside = lambda x: any(a <= x < a + n * 4 for a, n in keep)
    for x0, x1 in zip(edges, edges[1:]):
        if x1 > x0 and not inside(x0): put(quiet, x0, x1)
    parts.insert(parts.index(lead) + 1, quiet)
    return lead, quiet

def part(parts, role_prefix=None, inst=None):
    for p in parts:
        if (role_prefix and p["role"].startswith(role_prefix)) or (inst and p["instrument"] == inst): return p
    return None

def finish(song, parts, title):
    for p in parts: p["notes"] = split_rests(p["notes"])
    lens = {p["role"]: total(p["notes"]) for p in parts}
    assert len(set(lens.values())) == 1, lens
    song["parts"] = parts; song["title"] = title
    return song
