# 『なつぞら、かけだせ』（仮）の伴奏（重音テトの歌つきボカロ曲。歌は OpenUtau で）。BPM150・ニ長調・120小節（約3分12秒）。
# 歌の旋律と歌詞は teto-natsu-vocal.py。伴奏は歌とぶつからないよう控えめ: 歌のある所はリードギター・ベルを鳴らさない。
# 環境変数 GUIDE=1 で、歌の旋律をピアノで鳴らす「ガイド版」にする（確認用）。
# 使い方: python3 teto-natsu.py <出力.json>
# 書き出し: --drums jpop --bass finger --piano salamander --orchestra vsco --guitar gretsch --master-preset jpop-band（伴奏の PQ 8.04。ベース jpop だと 7.92）
# 歌声ソフト用: python3 tools/vocal/vocal-export.py assets-src/ai-songs/_gen/teto-natsu-vocal.py --out <フォルダ> --name なつぞら、かけだせ --bpm 150 --key 2 --wave <伴奏.wav>
import json, re, sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import drumkit

def fmt(x): return ("%.4f" % x).rstrip("0").rstrip(".")
N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pcof(s):
    r = PCN[s[0]]
    if len(s) > 1 and s[1] == "#": r += 1
    if len(s) > 1 and s[1] == "b": r -= 1
    return r % 12
def midi(n):
    i = 2 if len(n) > 2 and n[1] in "#b" else 1
    return pcof(n[:i]) + 12 * (int(n[i:]) + 1)
def tr(tok, k):
    if tok.startswith("R:") or k == 0: return tok
    n, rest = tok.split(":", 1)
    return nm(midi(n) + k) + ":" + rest
def fold(tok, hi=88):  # リードギターの音域（〜E6）を超える音は1オクターブ下げる
    if tok.startswith("R:"): return tok
    n_, rest_ = tok.split(":", 1); m = midi(n_)
    return nm(m - 12 if m > hi else m) + ":" + rest_
def seq(lst, k=0, f=lambda x: x): return " ".join(f(tr(x, k)) for x in " ".join(lst).split())
def up(chs, k):  # コード名を k 半音上げる（フラット表記）
    F = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    out = []
    for c in chs:
        parts = []
        for x in c.split("/"):
            m = re.match(r"^([A-G][#b]?)(.*)$", x); parts.append(F[(pcof(m.group(1)) + k) % 12] + m.group(2))
        out.append("/".join(parts))
    return out

import guitarcut, drumkit, importlib.util
_spec = importlib.util.spec_from_file_location("vocal", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "teto-natsu-vocal.py"))
vocal = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(vocal)
GUIDE = _os.environ.get("GUIDE") == "1"
# ---------------- コード（8小節ずつ。vocal.ORDER と同じ並び） ----------------
CH = {"intro": "G A F#m Bm G A D D", "A1": "D A/C# Bm G D A G A", "A2": "D A/C# Bm G Em F#m G A", "B": "Em F#m G A Em F#m G A",
      "C1": "G A F#m Bm G A D D", "C2": "G A F#m Bm Em A D D"}
SEC = [("intro", CH["intro"].split(), 0, 0),
       ("verse", CH["A1"].split(), 0, 0), ("verse", CH["A2"].split(), 0, 1), ("pre", CH["B"].split(), 0, 0),
       ("chorus", CH["C1"].split(), 0, 0), ("chorus", CH["C2"].split(), 0, 1),
       ("inter", CH["intro"].split(), 0, 0),
       ("verse", CH["A1"].split(), 0, 2), ("pre", CH["B"].split(), 0, 1),
       ("chorus", CH["C1"].split(), 0, 0), ("chorus", CH["C2"].split(), 0, 1),
       ("otosabi", CH["C1"].split(), 0, 0),
       ("chorus", CH["C1"].split(), 0, 2), ("chorus", CH["C2"].split(), 0, 3),
       ("outro", CH["intro"].split(), 0, 0)]
assert len(SEC) == len(vocal.ORDER)
chords = [c for _, pr, _, _ in SEC for c in pr]
GAIN = {"intro": .85, "verse": .8, "pre": .88, "chorus": 1.0, "inter": .92, "otosabi": .7, "outro": .88}
ARC = []
for si, (s, pr, k, n) in enumerate(SEC):
    g = GAIN[s] + (0.03 if si >= 7 and s != "otosabi" else 0)
    ARC += [round(min(1.05, g + (0.06 * i / len(pr) if s in ("pre",) else 0)), 3) for i in range(len(pr))]

def barsum(toks):
    t = 0
    for x in toks:
        if x.startswith("g:"): assert len(x) == 18, x; t += 4; continue
        d = x.split(":")[1]; t += float("".join(c for c in d if c.isdigit() or c == "."))
    return t
def cat(secs, name):
    out = []
    for (s, pr, _, _), toks in zip(SEC, secs):
        if isinstance(toks, str): toks = toks.split()
        assert abs(barsum(toks) - 4 * len(pr)) < 1e-6, (name, s, barsum(toks), 4 * len(pr))
        out += toks
    return " ".join(out)
def per(fn): return [fn(si, s, pr, k, n) for si, (s, pr, k, n) in enumerate(SEC)]
def rest(pr): return f"R:{fmt(4 * len(pr))}"

def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch.split("/")[0]); r = pcof(m.group(1)); q = m.group(2)
    minor = q.startswith("m") and not q.startswith("maj")
    pcs = [r, (r + (3 if minor else 4)) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    return pcs
def bass_pc(ch): return pcof(re.match(r"^([A-G][#b]?)", ch.split("/")[1]).group(1)) if "/" in ch else chord_pcs(ch)[0]
def tones_from(ch, lo):
    pcs = chord_pcs(ch); r = pcs[0]; base = lo + ((r - lo) % 12)
    return sorted(base + o + ((p - r) % 12) for o in (0, 12) for p in pcs)
def voicing(ch, center):
    pcs = chord_pcs(ch)[:3]; best = None
    for inv in range(3):
        o = pcs[inv:] + pcs[:inv]; cur = center - 7; v = []
        for p in o:
            x = cur + ((p - cur) % 12); v.append(x); cur = x + 1
        sc = abs(sum(v) / 3 - center)
        if best is None or sc < best[0]: best = (sc, v)
    return best[1]

# ---------------- リードギターのリフ（歌のない所だけ） ----------------
RIFF = ["B5:0.5 A5:0.5 G5:0.5 D5:0.5 G5:0.5 A5:0.5 B5:1", "C#6:0.5 B5:0.5 A5:0.5 E5:0.5 A5:0.5 B5:0.5 C#6:1",
        "C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:1 E6:1", "D6:2 B5:1 F#5:1",
        "B5:0.5 D6:0.5 B5:0.5 G5:0.5 B5:1 D6:1", "C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 E5:1 C#6:1",
        "D6:0.5 A5:0.5 F#5:0.5 A5:0.5 D6:2", "D6:3 R:1"]
def f_lead(si, s, pr, k, n):
    if s in ("intro", "inter"): return " ".join(RIFF)
    if s == "outro": return " ".join(RIFF[:6] + ["D6:4", "R:4"])
    return rest(pr)
# ---------------- 歌のガイド（GUIDE=1 のときだけ） ----------------
def f_guide(si, s, pr, k, n):
    bars = vocal.bars()[si * 8:(si + 1) * 8]
    out = []
    for bar in bars:
        for tok in bar.split():
            if tok.startswith("R:"): out.append(tok)
            else:
                kana, p, d = tok.split(":"); out.append(f"{p}:{d}")
    return " ".join(out)
# ---------------- ピアノ（分散和音） ----------------
P8 = [0, 2, 4, 2, 1, 3, 4, 3]
def f_piano(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        t = tones_from(ch, 50); last = i == len(pr) - 1
        if s == "otosabi": out += [f"{nm(t[j % len(t)])}:1" for j in (0, 2, 4, 2)]
        elif s == "pre" and last: out += [f"{nm(t[0])}:1", f"{nm(t[2])}:1", "R:2"]
        elif s == "outro" and i >= 6: out += [f"{nm(t[0])}:4"] if i == 6 else ["R:4"]
        else: out += [f"{nm(t[j % len(t)])}:0.5" for j in P8]
    return " ".join(out)
# ---------------- 弦（2声） ----------------
def strings(center, which):
    def f(si, s, pr, k, n):
        out = []
        for i, ch in enumerate(pr):
            v = nm(voicing(ch, center)[which])
            on = s in ("pre", "chorus", "otosabi") or (s == "verse" and n == 1 and i >= 4) or (s == "outro" and i >= 4)
            if not on: out.append("R:4")
            elif s == "pre" and i == len(pr) - 1: out += [f"{v}:2", "R:2"]
            else: out.append(f"{v}:4")
        return " ".join(out)
    return f
# ---------------- ベース ----------------
def f_bass(si, s, pr, k, n):
    out = []
    for i, ch in enumerate(pr):
        r = 28 + ((bass_pc(ch) - 28) % 12); a, o, f5 = nm(r), nm(r + 12 if r + 12 <= 50 else r + 7), nm(r + 7)
        nx = pr[i + 1] if i + 1 < len(pr) else ch; rn = 28 + ((bass_pc(nx) - 28) % 12)
        ap = nm(rn - 1 if rn > r else rn + 1) if rn != r else f5
        last = i == len(pr) - 1
        if s == "otosabi": out += [f"{a}:4"] if i < 6 else [a + ":1", a + ":1", o + ":1", ap + ":1"]
        elif s == "pre" and last: out += [f"{a}:1", "R:3"]
        elif s == "outro" and i >= 6: out += [f"{a}:4"] if i == 6 else ["R:4"]
        elif s in ("chorus", "intro", "inter"): out += [a + ":0.5"] * 3 + [o + ":0.5"] + [a + ":0.5"] * 2 + [f5 + ":0.5", ap + ":0.5"]
        else: out += [a + ":1", a + ":0.5", o + ":0.5", a + ":1", ap + ":1"]
    return " ".join(out)
# ---------------- カッティング（1本。控えめ） ----------------
def cut_pat(s, n, b):
    last = b == 7
    if s == "verse" and n >= 1: return "--D.--D.--D.--D." if not last else "--D.--D.D.------"
    if s == "pre": return "D.......--------" if last else "D.xUD.xUD.xUD.xU"
    if s == "chorus": return "D.xU.UxUD.xU.UxU" if not last else "D.xU.UxUD.------"
    if s in ("intro", "inter"): return "D.xUD.xUD.xUD.xU" if not last else "D.xUD.xUD.------"
    if s == "outro": return "D.xUD.xUD.xUD.xU" if b < 6 else ("D..............." if b == 6 else None)
    return None
CUT = guitarcut.cut_parts(SEC, chord_pcs, nm, cut_pat)
# ---------------- ドラム（drumkit.py） ----------------
Z = drumkit.Z
def groove(s, n, b, L):
    crash = b == 0 and s not in ("otosabi",)
    if s in ("intro", "inter", "chorus"):
        kk = ["X...X.x.X...X...", "X...X.x.X.x.X..."][b % 2]; hh = "X.O.X.O.X.O.X.O." if s == "chorus" else "X.x.X.x.X.x.X.x."
        return kk, "....X......oX...", hh, False, crash
    if s == "verse": return ["X.....x...x.....", "X.....x.X......."][b % 2], "....X......oX..o", ("X.x.X.x.X.x.X.x." if n != 1 else "X.xoX.xoX.xoX.xo"), False, crash and n != 1
    if s == "pre": return "X.....x.X.x.....", "....X..o....X..o", ("X.x.X.x.X.x.X.x." if b < 4 else "XxxxXxxxXxxxXxxx"), False, crash
    if s == "otosabi":
        if b < 6: return Z, Z, Z, False, False
        return "X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.x.x.", False, False
    if s == "outro":
        if b < 6: return "X...X.x.X...X...", "....X......oX...", "X.x.X.x.X.x.X.x.", False, b == 0
        if b == 6: return "X...............", Z, Z, False, True   # 最後の和音にクラッシュを1つ。あとは伸ばして静かに
        return Z, Z, Z, False, False
    return Z, Z, Z, False, False
KICK, SNARE, HAT, CRASH, TOM, RIDE = drumkit.build(SEC, groove, fills_off={"outro"})
DG = drumkit.drum_gain(SEC, {"intro": (0.85, 0.9), "verse": (0.78, 0.88), "pre": (0.85, 1.02), "chorus": (0.95, 1.0), "inter": (0.9, 0.95),
                             "otosabi": (0.6, 0.95), "outro": (0.9, 0.75)})

PARTS = []
def add(inst, role, vol, pan, secs, **kw):
    d = {"instrument": inst, "role": role, "volume": vol, "pan": pan, "notes": cat(secs, role)}; d.update(kw); PARTS.append(d)
A = ARC
DR = -6
if GUIDE: add("piano", "歌のガイド（ピアノ）", 0.24, 0, per(f_guide), barGain=A, reverb=0.15, gainDb=3)
add("leadGuitar", "リフ（リードギター・歌のない所だけ）", 0.16, 0.1, per(f_lead), barGain=A, gainDb=5, guitarTone="warm-lead-b")
add("piano", "ピアノ（分散和音）", 0.13, -0.3, per(f_piano), barGain=A, reverb=0.15)
for _i, _name in enumerate(["低", "中低", "中高", "高"]):
    add("guitar", f"カッティング（{_name}い弦）", 0.065, 0.6, CUT[_i], barGain=A, amp="jpopClean", chorus=0, reverb=0.12, humanPitch=0, push=round(0.008 * _i, 3))
add("strings", "弦（上）", 0.08, 0.5, per(strings(69, 2)), barGain=A, reverb=0.26)
add("strings", "弦（下）", 0.07, -0.5, per(strings(55, 0)), barGain=A, reverb=0.26)
add("bass", "ベース", 0.3, 0, per(f_bass), barGain=A)
add("kick", "キック", 0.3, 0, KICK, barGain=DG, gainDb=DR)
add("snare", "スネア", 0.26, 0, SNARE, barGain=DG, push=0.015, gainDb=DR)
add("hihat", "ハイハット", 0.08, 0, HAT, barGain=DG, push=-0.008, gainDb=DR)
add("crash", "クラッシュ", 0.1, 0, CRASH, barGain=DG, gainDb=DR)
add("crash", "ライド", 0.07, 0.2, RIDE, barGain=DG, gainDb=DR)
add("tom", "タム", 0.16, 0, TOM, barGain=DG, reverb=0, gainDb=DR)

song = {"title": "なつぞら、かけだせ（仮）" + ("・ガイド版" if GUIDE else "・伴奏"),
        "description": "（仮）重音テトの歌つきボカロ曲の伴奏（歌は OpenUtau で入れる）。BPM150・ニ長調。歌のある所はリードギター・ベルなし、落ちサビはピアノと弦だけ。入り方: 3（リフで始める）。終わり方: 最後の和音を伸ばして静かに。",
        "bpm": 150, "beats": 4, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
        "tone": "pop", "feel": "pop", "human": 0.25, "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False,
        "parts": PARTS}
json.dump({"guitarWobble": False, **song}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("ok", len(PARTS), "parts", len(chords), "bars", round(len(chords) * 4 * 60 / 150), "sec")
