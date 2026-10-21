# ラウド25曲の1曲目（作り直し）「逆光プリズム」
# 2026-10-22 人間「この曲没で旋律から作り直して」「既存の物にとらわれないでラウドロックの曲作って。旋律とか既存でよく聞くもの過ぎてつまらない」
#   「単調になりやすい傾向あるから注意して」「リードは 2（マーシャル系）」「電子音感が強すぎる」「トリガーとは別に重みのあるバスドラ」
#
# 方針（定番から外す）
# - 調: D。Aメロは暗いフリジアン（レ・ミ♭…）、サビで同じ D のまま明るいリディアン（ソ#が光る）に切りかわる＝「逆光」
# - リフ: 7つの8分音符のかたまりを 4/4 の上でくり返す（ずれていき、区切りで戻る）。開放の D を鳴らしたまま、♭2 と ♯4 を混ぜる
# - 和音: 短3度ずつ上がる D→F→A♭→B（Bメロ・ブリッジ）、サビは D→E→C#m7→B♭maj7 のように機能和声から外す
# - 旋律: 手書き。7度・3全音の跳躍、裏拍から入る、休みも旋律の一部、サビの終わりは ♯4（ソ#）で解決させない
# - 単調にしない: 区間ごとにドラム・編成・音域を変える（1回目と2回目のAメロ、3回目のサビも変える）
import sys, json, copy, re
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from loud25_lib import midi, name, at_least, NAMES
from loud25_arrange import build

LEAD_TONE = dict(humanPitch=0, noScoop=True, di="emily", double=False, chorus=0,   # 人間が選んだ「2 マーシャル系」（f3-t2-jvm）
                 amp="namJVM", ampDrive=0.7, ampGate=10, ampTight=0.6, ampTightHz=150, ampCabIr="jd-greenback-4x12-01", reverb=0.12,
                 fx=[{"type": "eq", "low": -2, "mid": 2.5, "midHz": 1000, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 7500, "q": 0.7},
                     {"type": "delay", "beats": 0.75, "mix": 0.18, "feedback": 0.3}, {"type": "plate", "mix": 0.18}])
ARP_TONE = dict(LEAD_TONE, ampDrive=0.35, fx=[{"type": "eq", "low": -3, "mid": 1.5, "midHz": 1000, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.7},
                                              {"type": "delay", "beats": 0.75, "mix": 0.22, "feedback": 0.35}, {"type": "plate", "mix": 0.24}])

# ── 旋律（1小節＝4拍。手で書いた音） ──
VERSE_A = [
    "R:0.5 D4:0.5 C5:1! R:0.5 A4:0.5 D#4:1",     # Dm  レ→ド（7度）跳んで、ミ♭（♭2）へ落ちる
    "G4:1.5 A#4:0.5 D5:1 R:1",                   # E♭
    "R:0.5 D4:0.5 C5:1! R:0.5 F5:0.5 D#5:1",     # Dm
    "D5:2 A#4:1 R:1",                            # E♭
    "R:0.5 G4:0.5 F5:1! D5:1 A#4:1",             # Gm  ソ→ファ（7度）
    "C5:1 D#5:1 G5:1.5 R:0.5",                   # E♭
    "A4:1 D5:0.5 A4:0.5 G#4:2",                  # Dm  ソ#（♯4）をちらっと見せる＝サビの予告
    "G#4:3 R:1",                                 # A♭
]
VERSE_B = VERSE_A[:4] + [
    "R:0.5 G4:0.5 F5:1! A#5:1 G5:1",
    "D#5:1 G5:1 A#5:1.5 R:0.5",
    "A5:1 D5:0.5 A4:0.5 G#4:1 A4:1",
    "C5:2 D#5:1 G#5:1",
]
VERSE2_A = [   # 2回目のAメロは1オクターブ近く上で、リズムを詰める（1回目と同じにしない）
    "R:0.5 D5:0.5 C6:0.5! R:0.5 A5:0.5 R:0.5 D#5:1",
    "G5:1 A#5:0.5 D6:0.5 R:0.5 A#5:0.5 G5:1",
    "R:0.5 D5:0.5 C6:0.5! R:0.5 F6:0.5 R:0.5 D#6:1",
    "D6:1.5 A#5:0.5 G5:1 R:1",
] + VERSE_B[4:]
PRE = [
    "F#4:3 A4:1", "D5:4",            # D（短調から急に長3度＝明るさの気配）
    "A4:3 C5:1", "F5:4",             # F
    "C5:3 D#5:1", "G#5:4",           # A♭
    "D#5:2 F#5:2", "B5:2 A5:1 C#6:1",  # B
]
CHORUS = [
    "R:0.5 A5:0.5 E6:1.5! G#5:1.5",  # D     ラ→ミ（上へ5度）→ソ#（♯4）。裏拍から入る
    "G#5:2 F#5:1 B5:1",              # E
    "E5:1.5 G#5:0.5 C#6:2!",         # C#m7
    "D6:2 A5:1 F5:1",                # B♭maj7（明るさが一瞬陰る）
    "R:0.5 A5:0.5 E6:1.5! G#5:1.5",  # D
    "B5:1 D#6:1 E6:2",               # E
    "C#6:1.5 A5:0.5 F#5:2",          # F#m
    "G#5:1 C6:1 D#6:2",              # A♭（3全音はなれた和音へ）
    "D6:1.5 A5:0.5 F5:1 A5:1",       # B♭maj7
    "G5:1 C6:1 E6:2!",               # C
    "R:0.5 A5:0.5 E6:1.5! G#5:1.5",  # D
    "G#5:2 B5:1 E6:1",               # E
    "E6:1 C#6:1 G#5:1 B5:1",         # C#m7
    "A5:2 D6:2",                     # B♭maj7
    "G#5:4", "G#5:2 R:2",            # E E   ソ#で止める（解決しない）
]
INTER = ["R:4"] * 4 + [
    "R:0.5 D#5:0.5 A#5:1 R:0.5 G5:0.5 D5:1", "D#5:2 R:2",
    "R:0.5 G#4:0.5 D#5:1 R:0.5 C5:0.5 G4:1", "G#4:3 R:1",
]
BRIDGE = [   # 半音・全音が交互の音階（レ・ミ♭・ファ・ファ#・ソ#・ラ・シ・ド）で、ゆっくり
    "D5:3 D#5:1", "F#5:4", "F5:3 G#5:1", "A5:4", "G#5:3 B5:1", "C6:4", "B5:3 C6:1", "D6:2 D#6:2",
    "R:4", "R:4", "R:4", "R:4",      # ギターの分散和音だけにして、すき間を作る
    "G#5:1 B5:1 D6:2", "C6:2 D#6:2", "D#6:2 D6:2", "C6:1 A5:1 F#5:1 D#5:1",
]
INTRO = ["R:4"] * 8
OUTRO = ["R:4"] * 6 + ["R:0.5 A5:0.5 E6:1.5! G#5:1.5", "G#5:1 R:3"]

FORM = [
    ("intro", "intro", 8, "1m"),
    ("verse1", "verse", 16, "1m 2 1m 2 4m 2 1m b5"),
    ("pre1", "pre", 8, "1 1 3 3 b5 b5 #6 #6"),
    ("chorus1", "chorus", 16, "1add9 #2 #7m7 6maj7 1add9 #2 #3m b5 6maj7 7 1add9 #2 #7m7 6maj7 #2 #2"),
    ("inter", "interlude", 8, "1m 1m 1m 1m 2 2 b5 b5"),
    ("verse2", "verse", 16, "1m 2 1m 2 4m 2 1m b5"),
    ("pre2", "pre", 8, "1 1 3 3 b5 b5 #6 #6"),
    ("chorus2", "chorus", 16, "1add9 #2 #7m7 6maj7 1add9 #2 #3m b5 6maj7 7 1add9 #2 #7m7 6maj7 #2 #2"),
    ("bridge", "bridge", 16, "1 1 3 3 b5 b5 #6 #6"),
    ("solo", "solo", 16, "1m 2 1m 2 4m 2 7 7"),
    ("chorus3", "chorus", 16, "1add9 #2 #7m7 6maj7 1add9 #2 #3m b5 6maj7 7 1add9 #2 #7m7 6maj7 #2 #2"),
    ("outro", "outro", 8, "1m 1m 1m 1m 2 2 1 1"),
]

SPEC = {
    "no": 1, "slug": "gyakkou-prism", "title": "逆光プリズム", "seed": 7101, "motifSeed": 7101,
    "bpm": 150, "key": "D", "mode": "phrygian", "tuning": "D2",
    "desc": "暗いフリジアンのAメロから、同じ D のままサビで明るいリディアンに切りかわる。7つの8分音符のリフが 4/4 の上でずれていく",
    "form": [list(f) for f in FORM],
    "rhythm": {
        "tone": "loud-mid", "pm": [], "verse_keep": True,
        "intro": "-", "inter": "-", "bridge": "-", "outro": "-",
        "verse": ["X=====x=====X===", "X=======x===x==="],
        "pre": "X===============",
        "chorus": ["X=====x=====x===", "X=====x=====X==="],
        "solo": ["X=======x=======", "X=====x=====x==="],
    },
    "lead": {"tone": "bmth-lead", "sections": {
        "intro": {"notes": INTRO},
        "verse1": {"notes": VERSE_A + VERSE_B},
        "verse2": {"notes": VERSE2_A + VERSE_B},
        "pre1,pre2": {"notes": PRE},
        "chorus1,chorus2,chorus3": {"notes": CHORUS},
        "inter": {"notes": INTER},
        "bridge": {"notes": BRIDGE},
        "outro": {"notes": OUTRO},
    }},
    "tech": {"solo": "mmsmmmtt"},
    "bass": {
        # Aメロ: すき間の多い、跳ねるベース（前半はギターなし）
        "verse": ["R:0.75! -:0.25 R:0.5 8:0.5 -:0.5 R:0.5 b:0.5 5:0.5", "R:1! -:0.5 5:0.5 8:0.75 7:0.25 5:0.5 -:0.5"],
        "pre": ["R:2! 5:2", "8:1! 5:1 3:1 5:1"],
        "chorus": ["R:1.5! R:0.5 5:1 8:1", "R:1! 3:1 5:1.5 9:0.5"],
        "bridge": ["R:4!", "5:2 3:2"],
        "solo": ["R:0.5! R:0.5 8:0.5 R:0.5 5:0.5! R:0.5 7:0.5 b:0.5", "R:1! 5:0.5 8:0.5 R:1 b:1"],
        "intro": "R:4", "inter": "R:4", "outro": "R:4",
    },
    "drums": {
        "intro": {"k": ["................"] * 4 + ["X...............", "X.........X.....", "X...............", "X.....X...X....."],
                  "s": ["................"] * 4 + ["........X.......", "........X.......", "........X.......", "........X...X..."],
                  "c": ["................"] * 4 + ["n...............", "r...r...r...r...", "n...............", "r...r...r...r..."], "fill": "tom", "crash": False},
        "verse1": {"k": "sync", "s": ["....X..o.o..X..o", "....X..o....X.o."], "h": ["x.x.x.xox.x.x.x.", "x.x.x.x.x.xox.x."], "fill": "snare", "crash": False},
        "verse2": {"k": ["X..X....X.X.....", "X..X..X...X..X.."], "s": ["....X.......X..o", "....X..o....X..."], "c": "r.r.r.r.r.r.r.r.", "fill": "snare"},
        "pre": {"k": ["X.......X.......", "X.......X.......", "X...X...X...X...", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "XXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXX"],
                "s": ["........X.......", "........X.......", "....X.......X...", "....X.......X...", "....X.......X...", "....X...X...X...", "....X.X.X.X.XXXX", "XXXXXXXXXXXXXXXX"],
                "h": ["x...x...x...x...", "x...x...x...x...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "................", "................", "................", "................"],
                "c": ["................"] * 4 + ["r.r.r.r.r.r.r.r."] * 2 + ["................"] * 2, "fill": "stop", "crash": False},
        "chorus1": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X...XXXX"], "s": "....X.......X...",
                    "c": ["r.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.n.", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus2": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "X..x..X.X...XXXX"], "s": "....X.......X...",
                    "c": ["n.r.r.r.n.r.r.r.", "r.r.r.r.r.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus3": {"k": ["X...............", "X.........X.....", "X...............", "X.....X...X.....", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX"],
                    "s": ["........X.......", "........X.......", "........X.......", "........X...X...", "....X.......X...", "....X.......X...", "....X.......X...", "....X.......X..."],
                    "c": ["n.......n.......", "r...r...r...r...", "n.......n.......", "r...r...r...r...", "n.r.r.r.r.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r.", "n...n...n...n..."], "fill": "tom"},
        "inter": {"k": "X.X.X.X.X.X.X.X.", "s": ["....X.......X...", "....X.......X..o"], "c": "n...n...n...n...", "fill": "kick"},
        "bridge": {"k": ["X...............", "................", "X.........X.....", "................"], "s": ["................", "........o.......", "................", "........o...o.o."],
                   "t": ["........3.......", "4.......4.......", "........3...3...", "4.......4...4.4."], "c": ["r...r...r...r..."], "crash": False, "fill": "snare"},
        "solo": {"k": ["X..x..X.X..x..x.", "XXXXXXXXX..x..x."], "s": "....X.......X...", "c": ["r.r.r.r.r.r.r.r.", "n.r.r.r.n.r.r.r."], "fill": "tom"},
        "outro": {"k": ["X.X.X.X.X.X.X.X."] * 6 + ["X...............", "................"], "s": ["....X.......X..."] * 6 + ["................"] * 2,
                  "c": ["n...n...n...n..."] * 6 + ["c...............", "................"], "crash": False, "nofill": True},
    },
    "extras": {"piano": {"arp": "bridge", "arpGuitar": ARP_TONE, "noChords": True}},
}

# ── 7つの8分音符のリフ（4/4 の上でずれていく） ──
CELL = [0, 0, 12, 1, 0, 7, 6]   # 開放の D・D・1オクターブ上・♭2・D・5度・♯4
def poly_riff(bar_chords, low, start_cell=0):
    """bar_chords: 小節ごとの根音（音名の数 0〜11）。8分音符を順に並べ、かたまりの頭に強弱をつける。最後の8分は根音で戻す"""
    toks = []; n = len(bar_chords) * 8
    for j in range(n):
        root = at_least(bar_chords[j // 8], low)
        idx = (j + start_cell) % 7
        m = root + CELL[idx] if j < n - 1 else root
        toks.append(f"{name(m)}:0.5" + ("!" if idx == 0 or j == n - 1 else ""))
    return " ".join(toks)

TOK = re.compile(r"^(.*):([\d.]+)([^\d.]*)$")
def toks(notes):
    out, t = [], 0.0
    for tk in notes.split():
        m = TOK.match(tk); out.append([t, float(m.group(2)), m.group(1), m.group(3)]); t += float(m.group(2))
    return out
def put(p, a, b, new=""):
    """パート p の [a, b) 拍を new（音の並び。空なら休み）で置きかえる"""
    n = p["notes"]
    if n.startswith("g:"):
        g = list(n[2:])
        for i in range(int(a * 4), int(b * 4)): g[i] = "."
        p["notes"] = "g:" + "".join(g); return
    out = []
    for t, d, h, suf in toks(n):
        e = t + d
        if e <= a + 1e-9 or t >= b - 1e-9: out.append(f"{h}:{d:g}{suf}"); continue
        if t < a - 1e-9: out.append(f"{h}:{a - t:g}{suf}")
        if t <= a + 1e-9 or t < a: out.append(new if new else f"R:{b - a:g}")
        if e > b + 1e-9: out.append(f"R:{e - b:g}")
    p["notes"] = " ".join(x for x in out if x)

def make(path):
    song, S = build(copy.deepcopy(SPEC))
    beats = 4
    start = {}; pos = 0
    for sid, kind, n, prog in FORM: start[sid] = (pos * beats, n); pos += n
    roots = [S.bars[i][2].root for i in range(S.NB)]
    parts = []
    for p in song["parts"]:
        if p["role"] in ("ライザー",): continue
        if p["instrument"] == "leadGuitar" and p["role"] != "リードギター（分散和音）":
            for k in ("guitarTone",): p.pop(k, None)
            p.update(json.loads(json.dumps(LEAD_TONE)))
        parts.append(p)
    # リード: Aメロ・ブリッジは小さめの別パート（同じ音色）、サビ・Bメロは前へ
    lead = [p for p in parts if p["role"] == "リード（旋律）"][0]
    quiet = json.loads(json.dumps(lead)); quiet["role"] = "リード（Aメロ・ブリッジ）"; quiet["volume"] = 0.105
    for sid in ("verse1", "verse2", "bridge"):
        a, n = start[sid]; put(lead, a, a + n * beats)
    keep = [start[s] for s in ("verse1", "verse2", "bridge")]
    full = sum(n for _, _, n, _ in FORM) * beats
    edges = sorted([0] + [a for a, n in keep] + [a + n * beats for a, n in keep] + [full])
    inside = lambda x: any(a <= x < a + n * beats for a, n in keep)
    for x0, x1 in zip(edges, edges[1:]):
        if x1 > x0 and not inside(x0): put(quiet, x0, x1)
    parts.insert(parts.index(lead) + 1, quiet)
    # Aメロの前半8小節はギター（刻み）を抜く（ベース・ドラム・旋律だけ）
    rhythm = [p for p in parts if p["role"].startswith("刻み")][0]
    for sid in ("verse1", "verse2"):
        a, n = start[sid]; put(rhythm, a, a + 8 * beats)
    # 7つの8分のリフ（前奏・間奏・後奏の前半）: ギター（単音）とベース（1オクターブ下）で同じ形
    riff = {"instrument": "distGuitar", "role": "リフ（7つの8分）", "volume": 0.1, "pan": 0, "guitarTone": "loud-mid", "gainDb": -4, "powerChord": False, "notes": f"R:{full}"}
    bass = [p for p in parts if p["instrument"] == "bass"][0]
    for sid, nb, cell0 in (("intro", 8, 0), ("inter", 8, 3), ("outro", 6, 5)):
        a, _ = start[sid]
        rr = roots[a // beats: a // beats + nb]
        put(riff, a, a + nb * beats, poly_riff(rr, midi("D3"), cell0))
        put(bass, a, a + nb * beats, poly_riff(rr, midi("D1"), cell0).replace("!", "!") )
    parts.insert(parts.index(rhythm) + 1, riff)
    # 後奏の最後2小節: 全員で D（長調の和音＝サビの明るさ）を1回鳴らして、ぱっと終わる
    a, _ = start["outro"]
    put(rhythm, a + 24, a + 32, "D2:4! R:4")
    # 重みのあるバスドラ（トリガーとは別。録音のキックの低音だけ）
    k = [p for p in parts if p["instrument"] == "kick"][0]
    heavy = {kk: vv for kk, vv in k.items() if kk not in ("trigger", "triggerVolume")}
    heavy.update({"role": "キック（重み）", "volume": 0.2, "gainDb": -3,
                  "fx": [{"type": "eq", "low": 6, "mid": -4, "midHz": 400, "high": -8}, {"type": "filter", "kind": "lowpass", "freq": 180, "q": 0.9}]})
    parts.insert(parts.index(k) + 1, heavy)
    # ベースは bassSplit（サビの抜粋で点が高かった）＋少し明るく
    bass.update({"amp": "bassSplit", "ampDrive": 0.6, "fx": [{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}]})
    song["parts"] = parts
    song["title"] = SPEC["title"]
    json.dump(song, open(path, "w"), ensure_ascii=False)
    return song

if __name__ == "__main__":
    s = make(sys.argv[1] if len(sys.argv) > 1 else "/tmp/lr/opt/full/n1-gyakkou.json")
    for p in s["parts"]: print(p["role"], p["instrument"], p["notes"][:90])
