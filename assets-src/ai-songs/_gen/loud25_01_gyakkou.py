# ラウド25曲の1曲目「逆光プリズム」（第2版）
# 2026-10-22 人間「曲としてレベルが低い」→ 第1版は「定番から外す」ことを優先しすぎて、旋律が跳びすぎ・和音があちこちへ飛ぶ・区間ごとに素材がばらばら、だった。
# 第2版の方針（調べたこと: soundfly「7 Melody Writing and Motivic Development Techniques」、secretsofsongwriting「Melody needs shape」「5 tips」）
# - 4つの音の動機 M（5・6・5・4 度。短・短・長）を、リフ・Aメロ・Bメロ・サビ・ブリッジの全部で使う（まとまり）
# - 同じ形を、Aメロでは暗いフリジアン（ラ・シ♭・ラ・ソ）、サビでは明るいリディアン（ラ・シ・ラ・ソ#）で鳴らす＝「逆光」。意外さはここ1つに絞る
# - 旋律はほぼ順次進行。前の句は不安定な音で終わり、後の句で落ち着く（問いと答え）。山は区間の終わり近くに置く
# - Aメロは低く主音を避け、サビは高く主音（レ）を使う。サビは2小節の短い句のくり返し
# - 意外な和音は1区間に1つまで（サビの B♭、Bメロの E）。それ以外は旋律から和音が分かる流れ
import sys, json, copy
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from loud25_lib import midi, name, at_least
from loud25_arrange import build
from loud25_hand import (LEAD_TONE, ARP_TONE, put, starts, cell_riff, retone_leads, add_heavy_kick, split_lead, part, finish, toks)

# ── 旋律（1小節＝4拍） ──
VERSE = [
    "R:1 A4:0.5 A#4:0.5 A4:1 G4:1",     # Dm  動機 M（ラ・シ♭・ラ・ソ）
    "G4:1.5 F4:0.5 G4:2",               # E♭
    "R:1 A4:0.5 A#4:0.5 A4:1 C5:1",     # Dm  M の終わりを上へのばす
    "C5:1.5 A#4:0.5 A4:2",              # C
    "R:1 D5:0.5 C5:0.5 A#4:1 A4:1",     # B♭  下へ移した形
    "G4:1.5 A4:0.5 C5:2",               # C
    "A4:1 A#4:1 C5:1 D5:1",             # Dm  順に上がって山へ
    "D#5:2 D5:1 R:1",                   # E♭  不安定な音で止める（問い）
]
VERSE_2 = VERSE[:6] + [
    "A4:1 A#4:1 C5:1 D5:0.5 C5:0.5",    # Dm
    "A#4:2 A4:2",                       # E♭  答え（下りて落ち着く）
]
PRE = [
    "D5:0.5 D#5:0.5 D5:1 C5:2",         # B♭  M を上へ移していく
    "E5:0.5 F5:0.5 E5:1 D5:2",          # C
    "F5:0.5 G5:0.5 F5:1 E5:1 D5:1",     # Dm
    "A5:3 R:1",                         # Dm
    "D5:0.5 D#5:0.5 D5:1 C5:2",         # B♭
    "E5:0.5 F5:0.5 E5:1 G5:2",          # C
    "G#5:2 B5:2",                       # E   ここで初めてソ#（明るさの予告）
    "B5:3 R:1",                         # E
]
CHORUS = [
    "A5:1 B5:1 A5:2!",                  # D    M を長くした形（ラ・シ・ラ…）
    "G#5:2 E5:1 F#5:1",                 # E    …ソ#（明るい M）
    "F#5:1 G#5:1 F#5:2",                # Bm   1つ下へ移す
    "E5:3 R:1",                         # A    問い
    "A5:1 B5:1 A5:2!",                  # D
    "G#5:1 B5:1 D6:2",                  # E    上へのばす
    "D6:1.5 C6:0.5 A#5:2",              # B♭   暗い和音が一瞬（Aメロの色を思い出す）
    "C6:2 D6:1 E6:1",                   # C    山へ
    "D6:3 A5:1",                        # D    主音で言い切る
    "B5:1 A5:1 G#5:2",                  # E
    "F#5:1 G#5:1 A5:1 B5:1",            # Bm
    "A5:2 E5:2",                        # A
    "A5:1 B5:1 A5:2!",                  # D
    "G#5:2 B5:1 C#6:1",                 # E
    "D6:2 C6:1 A#5:1",                  # B♭
    "A5:2 C#6:1 E6:1",                  # A    次へ投げる
]
BRIDGE = [
    "D5:2 C5:1 D5:1", "E5:4", "F#5:2 E5:1 F#5:1", "A5:4",
    "D6:2 C6:1 D6:1", "E6:4", "D6:1 B5:1 G#5:2", "B5:4",
    "R:4", "R:4", "R:4", "R:4",         # 分散和音のギターだけ
    "F5:2 A5:2", "G5:2 C6:2", "B5:2 D6:2", "E6:2 R:2",
]
INTER = ["R:4"] * 4 + ["R:1 A#4:0.5 C5:0.5 A#4:1 A4:1", "G4:4", "R:1 A4:0.5 A#4:0.5 A4:1 G4:1", "A4:4"]
OUTRO = ["R:4"] * 6 + ["A5:1 B5:1 A5:2!", "A5:4"]

CH = "1add9 #2 #6m 5 1add9 #2 6 7 1add9 #2 #6m 5 1add9 #2 6 5"
FORM = [
    ("intro", "intro", 8, "1m"),
    ("verse1", "verse", 16, "1m 2 1m 7 6 7 1m 2"),
    ("pre1", "pre", 8, "6 7 1m 1m 6 7 #2 #2"),
    ("chorus1", "chorus", 16, CH),
    ("inter", "interlude", 8, "1m 1m 1m 1m 2 2 1m 1m"),
    ("verse2", "verse", 16, "1m 2 1m 7 6 7 1m 2"),
    ("pre2", "pre", 8, "6 7 1m 1m 6 7 #2 #2"),
    ("chorus2", "chorus", 16, CH),
    ("bridge", "bridge", 16, "6maj7 7 1 1 6maj7 7 #2 #2"),
    ("solo", "solo", 16, "1m 2 1m 7 6 7 1m 2"),
    ("chorus3", "chorus", 16, CH),
    ("outro", "outro", 8, "1m 1m 1m 1m 2 2 1 1"),
]

SPEC = {
    "no": 1, "slug": "gyakkou-prism", "title": "逆光プリズム", "seed": 7101, "motifSeed": 7101,
    "bpm": 150, "key": "D", "mode": "phrygian", "tuning": "D2",
    "desc": "暗いフリジアンのAメロの動機（ラ・シ♭・ラ・ソ）が、サビで同じ形のまま明るいリディアン（ラ・シ・ラ・ソ#）になる",
    "form": [list(f) for f in FORM],
    "rhythm": {
        "tone": "loud-mid", "pm": [], "verse_keep": True,
        "intro": "-", "inter": "-", "bridge": "-", "outro": "-",
        "verse": ["X=====x=====X===", "X=======x===x==="],
        "pre": ["X=======X=======", "X===x===X===x==="],
        "chorus": ["X=======x=======", "X=====x=====x==="],
        "solo": ["X=======x=======", "X=====x=====x==="],
    },
    "lead": {"tone": "bmth-lead", "sections": {
        "verse1,verse2": {"notes": VERSE + VERSE_2},
        "pre1,pre2": {"notes": PRE},
        "chorus1,chorus2,chorus3": {"notes": CHORUS},
        "inter": {"notes": INTER},
        "bridge": {"notes": BRIDGE},
        "outro": {"notes": OUTRO},
        "intro": {"notes": ["R:4"] * 8},
    }},
    "tech": {"solo": "mmsmmmtt"},
    "bass": {
        "verse": ["R:1.5! R:0.5 5:1 R:1", "R:1! 5:0.5 8:0.5 7:1 5:1"],
        "pre": ["R:2! 5:2", "R:1! 5:1 8:1 5:1"],
        "chorus": ["R:1.5! R:0.5 5:1 8:1", "R:1! 3:1 5:1.5 R:0.5"],
        "bridge": ["R:4!", "5:2 3:2"],
        "solo": ["R:0.5! R:0.5 8:0.5 R:0.5 5:0.5! R:0.5 7:0.5 b:0.5", "R:1! 5:0.5 8:0.5 R:1 b:1"],
        "intro": "R:4", "inter": "R:4", "outro": "R:4",
    },
    "drums": {
        "intro": {"k": ["................"] * 4 + ["X.....X...X.....", "X.....X...X...X.", "X.....X...X.....", "X.....X...X.X.X."],
                  "s": ["................"] * 4 + ["........X.......", "........X.......", "........X.......", "........X...X..."],
                  "c": ["................"] * 4 + ["c...r...r...r...", "r...r...r...r...", "n...r...r...r...", "r...r...r...r..."], "fill": "tom", "crash": False},
        "verse1": {"k": "sync", "s": ["....X..o....X...", "....X......oX..o"], "h": ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.xo"], "fill": "snare", "crash": False},
        "verse2": {"k": "sync", "s": ["....X..o....X...", "....X......oX..o"], "c": "r.r.r.r.r.r.r.r.", "fill": "snare"},
        "pre": {"k": ["X.......X.......", "X.......X.......", "X...X...X...X...", "X...X...X...X...", "X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X.", "X.X.X.X.X.X.X.X."],
                "s": ["........X.......", "........X.......", "....X.......X...", "....X.......X...", "....X.......X...", "....X.......X...", "....X...X...X...", "....X.X.X.X.XXXX"],
                "h": ["x...x...x...x...", "x...x...x...x...", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "................", "................", "................", "................"],
                "c": ["................"] * 4 + ["r.r.r.r.r.r.r.r."] * 3 + ["................"], "fill": "stop", "crash": False},
        "chorus1": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X...XXXX"], "s": "....X.......X...",
                    "c": ["r.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.n.", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus2": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "X..x..X.X...XXXX"], "s": "....X.......X...",
                    "c": ["n.r.r.r.n.r.r.r.", "r.r.r.r.r.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus3": {"k": ["X.....X...X.....", "X.....X...X.....", "X.....X...X.....", "X.....X...X.X.X.", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX"],
                    "s": ["........X.......", "........X.......", "........X.......", "........X...X...", "....X.......X...", "....X.......X...", "....X.......X...", "....X.......X..."],
                    "c": ["n.......n.......", "r...r...r...r...", "n.......n.......", "r...r...r...r...", "n.r.r.r.r.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r.", "n...n...n...n..."], "fill": "tom"},
        "inter": {"k": ["X.....X...X.....", "X.....X...X.X.X."], "s": "........X.......", "c": "n...r...r...r...", "fill": "kick"},
        "bridge": {"k": ["X...............", "................", "X.........X.....", "................"], "s": ["................"],
                   "t": ["........3.......", "4.......4.......", "........3...3...", "4.......4...4.4."], "c": ["r...r...r...r..."], "crash": False, "fill": "snare"},
        "solo": {"k": ["X..x..X.X..x..x.", "XXXXXXXXX..x..x."], "s": "....X.......X...", "c": ["r.r.r.r.r.r.r.r.", "n.r.r.r.n.r.r.r."], "fill": "tom"},
        "outro": {"k": ["X.....X...X....."] * 6 + ["X...............", "................"], "s": ["........X......."] * 6 + ["................"] * 2,
                  "c": ["n...r...r...r..."] * 6 + ["c...............", "................"], "crash": False, "nofill": True},
    },
    "extras": {"piano": {"arp": "bridge", "arpGuitar": ARP_TONE, "noChords": True}},
}

# リフ: 動機 M を低い D の上で（1小節目 a・2小節目 b）。8分音符
RIFF_A = [0, 0, 7, 8, 7, 5, 0, 12]       # D D A B♭ A G D D'
RIFF_B = [0, 0, 7, 8, 7, 10, 8, 5]       # D D A B♭ A C B♭ G
def riff_bars(roots, low):
    out = []
    for i, r in enumerate(roots):
        cell = RIFF_A if i % 2 == 0 else RIFF_B
        if i == len(roots) - 1 and len(roots) > 1: cell = RIFF_A[:6] + [0, None]
        out.append(cell_riff(cell, [r], low, 0.5, end_root=False))
    return " ".join(out)

def harmony_below(notes, t0, S):
    """旋律の各音の下に、その小節の和音の音のうち 3〜4 半音下（なければ 2〜9 半音下でいちばん近い音）を置く"""
    out = []
    for t, d, h, suf in toks(notes):
        if h.startswith("R"): out.append(f"{h}:{d:g}{suf}"); continue
        m = midi(h); ch = S.bars[int((t0 + t) // 4)][2]; pcs = ch.pcs()
        cands = [m - k for k in range(2, 10) if (m - k) % 12 in pcs]
        pick = next((c for c in cands if 3 <= m - c <= 4), cands[0] if cands else m - 3)
        out.append(f"{name(pick)}:{d:g}{suf}")
    return " ".join(out)

def make(path):
    song, S = build(copy.deepcopy(SPEC))
    st = starts(FORM)
    roots = [S.bars[i][2].root for i in range(S.NB)]
    parts = [p for p in song["parts"] if p["role"] != "ライザー"]
    retone_leads(parts)
    lead, quiet = split_lead(parts, st, ("verse1", "verse2", "bridge", "inter"))
    rhythm = part(parts, "刻み")
    for sid in ("verse1", "verse2"):                       # Aメロ前半はギターを抜く
        a, n = st[sid]; put(rhythm, a, a + 8 * 4)
    full = st["outro"][0] + 8 * 4
    riff = {"instrument": "distGuitar", "role": "リフ（動機）", "volume": 0.1, "pan": 0, "guitarTone": "loud-mid", "gainDb": -4, "powerChord": False, "notes": f"R:{full}"}
    bass = part(parts, inst="bass")
    for sid, nb in (("intro", 8), ("inter", 8), ("outro", 6)):
        a, _ = st[sid]; rr = roots[a // 4: a // 4 + nb]
        put(riff, a, a + nb * 4, riff_bars(rr, midi("D2")))
        put(bass, a, a + nb * 4, riff_bars(rr, midi("D2")))
    parts.insert(parts.index(rhythm) + 1, riff)
    a, _ = st["outro"]; put(rhythm, a + 24, a + 32, "D2:4! R:4")
    # サビの後半8小節（2回目・3回目は全部）にリードの3度下のハモり
    harm = json.loads(json.dumps(lead)); harm["role"] = "リード（ハモり）"; harm["volume"] = 0.085; harm["pan"] = 0.25
    harm["notes"] = f"R:{full}"
    for sid, frm in (("chorus1", 8), ("chorus2", 0), ("chorus3", 0)):
        a, n = st[sid]; seg = []
        for t, d, h, suf in toks(lead["notes"]):
            if a + frm * 4 - 1e-9 <= t < a + n * 4 - 1e-9: seg.append(f"{h}:{d:g}{suf}")
        put(harm, a + frm * 4, a + n * 4, harmony_below(" ".join(seg), a + frm * 4, S))
    lead["pan"] = -0.1
    parts.insert(parts.index(quiet) + 1, harm)
    add_heavy_kick(parts)
    bass.update({"amp": "bassSplit", "ampDrive": 0.6, "fx": [{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}]})
    finish(song, parts, SPEC["title"])
    json.dump(song, open(path, "w"), ensure_ascii=False)
    return song

if __name__ == "__main__":
    s = make(sys.argv[1] if len(sys.argv) > 1 else "/tmp/lr/opt/full/n1-gyakkou.json")
    for p in s["parts"]: print(p["role"], p["notes"][:100])
