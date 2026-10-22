# ラウド25曲の1曲目「逆光プリズム」（第3版。型B「現代ラウドロックの設計図」で作り直し）
# 2026-10-22 人間「曲としてレベルが低い」「聴きたいかと言われたら聞きたくはない」「もっと現代のラウドロックの勉強してきて」
# 設計図: docs/sound/loud-rock-patterns.md の型B、調査は docs/sound/modern-loud-rock/*.md
#
# 骨組み（定番を守る）: D マイナー・140・ドロップD・約3分30秒・124小節。最初のサビは 0:55
#   イントロ8 → Aメロ16 → Bメロ8 → サビ16 → 看板リフ8 → Aメロ2 8 → Bメロ2 8 → サビ2 16 → ブリッジ8 → ブレイクダウン8 → ラストサビ16 → アウトロ4
# 意外性（4か所だけ）:
#   1. サビ3小節目に借用の長三和音 G（ドリアの IV）。旋律もファ#に上がる＝「逆光」が差す瞬間
#   2. Aメロの4小節目に E♭（フリジアの ♭II）を一瞬
#   3. ブリッジの3小節目に E♭maj7
#   4. ラストサビの頭4小節は、リードとクリーンの分散和音とキックだけに抜く
import sys, json, copy
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from loud25_lib import midi, name, at_least
from loud25_arrange import build
from loud25_hand import (LEAD_TONE, ARP_TONE, put, starts, retone_leads, plain_guitars, drum_detail, add_heavy_kick, split_lead, part, finish, toks, total)

# ── 旋律（歌の代わりのリード。1小節＝4拍） ──
# 2026-10-22 人間「このリードのギターフレーズ変えよう」→ arrangement-detail.md 4章の決まりで書き直し（第6版）
#   1フレーズ＝2小節（4〜9音＋2拍以上の休み）、8小節＝A・A'・B・A''、奇数番目は和音にない音で止める（問い）・偶数番目は和音の音（答え）、
#   半分以上は裏拍から入る、同じ音の16分の連打（リズムで語る）＋上への跳躍の動機を全区間で使う、チョーキングは1フレーズに1回まで
CELL = "R:0.5 {n}:0.25 {n}:0.25 R:0.25 {n}:0.25"     # 動機の頭（裏から入って同じ音を3つ）＝2拍
def cell(n, rest): return CELL.format(n=n) + " " + rest
VERSE_B = [  # 中心はラ4〜ド5。主音（レ）は避ける
    cell("A4", "C5:0.5 E5:1 C5:0.5 A4:0.5"),   # Dm   A（ミ＝9度の色）
    "G4:1.5 R:2.5",                            # E♭   問い（息つぎ）
    cell("A4", "C5:0.5 F5:1! E5:0.5 C5:0.5"),  # Dm   A'（上へのばす）
    "D5:1.5 R:2.5",                            # C    9度で止める
    "R:1 F4:0.5 A#4:0.5 D5:1 F5:1",            # B♭   B（拍から入り、和音をのぼる）
    "E5:1 G5:0.5 E5:0.5 C5:1 R:1",             # C
    cell("D5", "A#4:0.5 G4:1 A4:1"),           # Gm   A''（動機を高い所から）
    "C#5:2 R:2",                               # A    答え（Bメロへ）
]
VERSE = VERSE_B[:4]
PRE = [  # 動機を長くした形（同じ音を3つ→上へ）を、和音ごとに上へ移す
    "R:1 D5:0.5 D5:0.5 D5:1 F5:1",             # Gm
    "G5:2 R:2",                                # Gm
    "R:1 F5:0.5 F5:0.5 F5:1 A5:1",             # B♭
    "A#5:2 R:2",                               # B♭
    "R:1 G5:0.5 G5:0.5 G5:1 E5:1",             # C
    "E5:2 R:2",                                # C
    "R:0.5 F5:0.5 G5:0.5 A5:0.5 G5:1 F5:1",    # Csus4
    "E5:3 R:1",                                # C    最後の1拍は全員休み
]
CHORUS = [
    cell("D5", "F5:0.5 A5:1.5! G5:0.5"),       # B♭add9  A: 同じ音を3つ→ラへ跳ぶ（ラ＝maj7 の色）
    "G5:1.5 R:2.5",                            #          問い（6度で止める）
    cell("C5", "F5:0.5 A5:1.5! F5:0.5"),       # F       A': 同じ形を1つ下から
    "F5:1.5 R:2.5",                            #          答え（根音）
    "R:1 B5:0.5 A5:0.5 B5:1 D6:1!",            # G       B: シ（借用の長三和音の3度）で光が差す
    "D6:2!^^ B5:1 R:1",                        #          レからミへチョーキング（問い）
    cell("A5", "G5:0.5 E5:1.5 D5:0.5"),        # Asus4   A'': 高い所から下りる
    "C#5:2.5! R:1.5",                          # A       答え（導音で次へ）
    cell("D5", "F5:0.5 A5:1.5! G5:0.5"),       # B♭add9  A
    "G5:1.5 R:2.5",
    cell("C5", "F5:0.5 C6:1.5!/ A5:0.5"),      # F       A'（ドまで跳ぶ。スライドで入る）
    "G5:1 F5:0.5 E5:0.5 R:2",                  #          問い（maj7 で止める）
    "R:1 E5:0.5 G5:0.5 C6:1 D6:1!^^",          # C       B: いちばん高いミ6はチョーキングで1回だけ
    "E6:2 D6:1 R:1",
    cell("A5", "G5:0.5 F5:1 E5:1"),            # Dm(add9) A''
    "D5:3! R:1",                               #          やっと主音で言い切る
]
BRIDGE = ["D5:4", "F5:4", "G5:4", "E5:2 R:2", "D5:4", "F5:2 A5:2", "G5:4", "E5:4"]
INTRO = ["R:4", "R:4", cell("D5", "F5:0.5 A5:1.5! G5:0.5"), "G5:1.5 R:2.5"] + ["R:4"] * 4   # サビのフックの先出し

CH = "6add9 6add9 3 3 4 4 5sus4 5 6add9 6add9 3 3 7 7 1madd9 1madd9"
FORM = [
    ("intro", "intro", 8, "1madd9 1madd9 6add9 6add9 1m 1m 1m 1m"),
    ("verse1", "verse", 16, "1m b2 1m 7 6 7 1m 1m 1m b2 1m 7 6 7 4m 5"),
    ("pre1", "pre", 8, "4m 4m 6 6 7 7 7sus4 7"),
    ("chorus1", "chorus", 16, CH),
    ("inter1", "interlude", 8, "1m"),
    ("verse2", "verse", 8, "1m b2 1m 7 6 7 4m 5"),
    ("pre2", "pre", 8, "4m 4m 6 6 7 7 7sus4 7"),
    ("chorus2", "chorus", 16, CH),
    ("bridge", "bridge", 8, "6maj7 4m7 b2maj7 5sus4 6maj7 4m7 b2maj7 5"),
    ("break", "break", 8, "1m"),
    ("chorus3", "chorus", 16, CH),
    ("outro", "outro", 4, "1m"),
]

FORM_D = [(f[0], f[3]) for f in FORM]

SPEC = {
    "no": 1, "slug": "gyakkou-prism", "title": "逆光プリズム", "seed": 7101, "motifSeed": 7101,
    "bpm": 140, "key": "D", "mode": "aeolian", "tuning": "D2",
    "desc": "暗い D マイナーのAメロから、サビ3小節目の借用の長三和音で光が差す。型B（現代ラウドロックの設計図）",
    "form": [list(f) for f in FORM],
    "rhythm": {
        "tone": "loud-mid", "pm": [], "verse_keep": True,
        "intro": "-", "inter1": "-", "bridge": "-", "break": "-", "outro": "-",
        "verse": ["X=====x=====X===", "X=======x===x==="],
        "pre": ["X===============", "X=======X======="],
        "chorus": ["X===============", "X=======x======="],
    },
    "lead": {"tone": "bmth-lead", "sections": {
        "intro": {"notes": INTRO},
        "verse1": {"notes": VERSE + ["R:4"] * 4 + VERSE_B},   # 5〜8小節は息つぎ（分散和音だけ）
        "verse2": {"notes": ["R:4"] * 4 + VERSE_B[4:]},            # 2回目は前半をバンドだけに（1回目と変える）
        "pre1,pre2": {"notes": PRE},
        "chorus1,chorus2,chorus3": {"notes": CHORUS},
        "bridge": {"notes": BRIDGE},
        "inter1": {"notes": ["R:4"] * 8}, "break": {"notes": ["R:4"] * 8}, "outro": {"notes": ["R:4"] * 4},
    }},
    "tech": {},
    "bass": {
        "verse": ["R:1.5! R:0.5 5:1 R:1", "R:1! 5:0.5 8:0.5 7:1 5:1"],
        "pre": "R:4", "chorus": ["R:1! R:0.5 R:0.5 R:1 R:1", "R:1! R:1 5:1 8:1"],
        "intro": "R:4", "inter": "R:4", "bridge": ["R:4!"], "break": "R:4", "outro": "R:4",
    },
    "drums": {
        "intro": {"k": ["................", "................", "................", "................", "X.....X...X.....", "X.....X...X...X.", "X.....X...X.....", "X.....X...X.X.X."],
                  "s": ["................"] * 4 + ["....X.......X...", "....X.......X...", "....X.......X...", "....X.......X..."],
                  "c": ["................"] * 4 + ["c...r...r...r...", "r...r...r...r...", "n...r...r...r...", "r...r...r...r..."], "fill": "tom", "crash": False},
        "verse1": {"k": "sync", "s": ["....X..o....X...", "....X......oX..o"], "h": ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.xo"], "fill": "snare", "crash": False},
        "verse2": {"k": "sync", "s": ["....X..o....X..o", "....X..o.o..X..."], "c": "r.r.r.r.r.r.r.r.", "fill": "snare"},
        "pre1": {"k": ["X.......X......."] * 2 + ["X...X...X...X..."] * 2 + ["X.X.X.X.X.X.X.X."] * 3 + ["X.X.X.X.X.X....."],
                 "s": ["........X......."] * 2 + ["....X.......X..."] * 2 + ["....X.......X...", "....X.......X...", "....X...X...X...", "....X.X.X.X....."],
                 "h": ["x...x...x...x..."] * 4 + ["................"] * 4, "c": ["................"] * 4 + ["r.r.r.r.r.r.r.r."] * 3 + ["r.r.r.r.r.r....."], "fill": "stop", "crash": False},
        "pre2": {"k": ["X...X...X...X..."] * 4 + ["XXXXXXXXXXXXXXXX"] * 3 + ["X.X.X.X.X.X....."],
                 "s": ["....X.......X..."] * 4 + ["....X.......X...", "....X.......X...", "....X.X.X.X.X.X.", "XXXXXXXXXXXX...."],
                 "c": ["r.r.r.r.r.r.r.r."] * 4 + ["n...n...n...n..."] * 3 + ["................"], "fill": "stop", "crash": False},
        "chorus1": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X...XXXX"], "s": "....X.......X...",
                    "c": ["c.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus2": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "XXXXXXXXXXXX.XXX"], "s": "....X.......X...",
                    "c": ["c.r.r.r.n.r.r.r.", "r.r.r.r.r.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r."], "fill": "tom"},
        "chorus3": {"k": ["X...X...X...X..."] * 4 + ["X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX", "X..x..X.X..x..x.", "XXXXXXXXXXXXXXXX"],
                    "s": ["................"] * 4 + ["....X.......X..."] * 4,
                    "c": ["................"] * 4 + ["c.r.r.r.n.r.r.r.", "n...n...n...n...", "r.r.r.r.r.r.r.r.", "n...n...n...n..."], "fill": "tom", "crash": False},
        "inter1": {"k": ["X.....X...X.....", "X.....X...X.X.X."], "s": "........X.......", "c": ["n...r...r...r...", "r...r...r...r..."], "fill": "snare"},
        "bridge": {"k": ["X...............", "................", "X.........X.....", "................"], "s": ["................"],
                   "t": ["........4.......", "4.......4.......", "........3...4...", "4.......4...3.4."], "c": ["r.......r......."], "crash": False, "fill": "stop"},
        "break": {"k": ["X..X..X...X.X...", "X..X..X...X.....", "X..X..X...X.X...", "X..X..X.........", "X..X..X...X.X...", "X..X..X...X.....", "X..X..X.........", "X..............."],
                  "s": ["........X......."] * 7 + ["................"], "c": ["n...n...n...n...", "n...n...n.......", "n...n...n...n...", "n...n...n.......", "c...n...n...n...", "n...n...n.......", "c...n...n...n...", "n..............."], "crash": False, "nofill": True},
        "outro": {"k": ["X.....X...X.....", "X.....X...X.X.X.", "X...............", "................"], "s": ["....X.......X...", "....X.......X...", "................", "................"],
                  "c": ["n...r...r...r...", "r...r...r...r...", "c...............", "................"], "crash": False, "nofill": True},
    },
    "extras": {"piano": {"arp": "intro,verse1,bridge,chorus3", "arpGuitar": ARP_TONE, "noChords": True}},
}

# 看板リフ: 低い開放の D と高い弦の旋律を交互に（ペダルトーン奏法）＋最後に伸ばす。刻みではない
SIG_A = "D2:0.5! D3:0.5 D2:0.5 F3:0.5 D2:0.5 G3:0.5 D2:0.5 A3:0.5"
SIG_B = "D2:0.5! A#3:0.5 D2:0.5 A3:0.5 D2:0.5 F3:0.5 G3:1!"
SIG_C = "D2:0.5! D3:0.5 D2:0.5 F3:0.5 D2:0.5 G3:0.5 A3:0.5 C4:0.5"
SIG_D = "D4:2! A3:1 R:1"
def sig(n):  # n 小節
    seq = [SIG_A, SIG_B, SIG_A, SIG_B, SIG_C, SIG_B, SIG_C, SIG_D]
    return " ".join(seq[i % 8] for i in range(n))
# ブレイクダウン: 伸ばす和音の一撃と休み（ブリッジミュートの刻みは使わない）。キックと同じ位置。7小節目で間を広げ、8小節目は3〜4拍目を休んでから最後の一撃へ
BD_A = "D2:0.75! D2:0.75! D2:1! D2:0.5! D2:1!"          # 0・3・6・10・12（キックと同じ）
BD_B = "D2:0.75! D2:0.75! D2:1! D2:1.5!"                 # 0・3・6・10
BD_C = "D2:0.75! D2:0.75! D2:2.5!"                       # 0・3・6 で伸ばす
BD_END = "D2:0.75! R:3.25"                               # 1拍目の一撃だけ（あとは休み）

# ── 歌（2026-10-22 人間「1・2・3だね」→ 1曲目は歌入りのバンドの曲。旋律は歌が運び、リードギターは前奏と間奏だけ）──
# 歌詞はオリジナル。テーマ: 閉じこもった部屋に差しこむ一筋の光が、プリズムで色に分かれる（逆光）
# 旋律は歌える高さへ1オクターブ下げる（Aメロ ラ3〜、サビ レ4〜ミ5。テトは B3〜E5 が楽）
LYRICS = {
    "verse1": ["とじこめたへやで", "かぞえたためいき", "ことばをなくして", "ゆびさきこごえる", "すきまにさしこむ", "ひとすじのいろ"],
    "verse2": ["ふるえるてのひら", "かざしたまぶた"],
    "pre": ["いまはまだ", "とおくても", "このむねの", "おくでひかる"],
    "chorus": ["ひかりきりさく", "うしろのひかり", "まだとおくへ", "ぷりずむになれ", "なみだもひかる", "くだけたいろあつめ", "そらへはなて", "ぼくらのいろで"],
    "bridge": ["かげごとだきしめて"],
}
SMALL = set("ゃゅょぁぃぅぇぉ")
def morae(line):
    out = []
    for ch in line:
        if ch in SMALL and out: out[-1] += ch
        else: out.append(ch)
    return out

def vocal_notes(lead_notes, st, sids_lyrics, full):
    """リードの音（同じ場所）を1オクターブ下げ、歌詞を1音ずつ付けた "vocals" の notes を作る"""
    out = []; pos = 0.0
    def rest(d):
        nonlocal pos
        while d > 1e-9:
            x = min(4, d); out.append(f"R:{x:g}"); d -= x; pos += x
    events = toks(lead_notes)
    for sid, lines in sids_lyrics:
        a, n = st[sid]; b = a + n * 4
        seq = [m for line in lines for m in morae(line)]
        notes = [(t, d, h, suf) for t, d, h, suf in events if a - 1e-9 <= t < b - 1e-9 and not h.startswith("R")]
        assert len(seq) == len(notes), (sid, len(seq), len(notes), [h for _, _, h, _ in notes])
        for (t, d, h, suf), syl in zip(notes, seq):
            if t > pos + 1e-9: rest(t - pos)
            nm = name(midi(h) - 12); bang = "!" if "!" in suf else ""
            bend = suf.count("^")
            if bend and d > 0.5:
                out.append(f"{nm}{bang}:0.5:{syl}"); out.append(f"{name(midi(h) - 12 + bend)}:{d - 0.5:g}:ー")
            else:
                out.append(f"{nm}{bang}:{d:g}:{syl}")
            pos = t + d
    if full > pos: rest(full - pos)
    return " ".join(out)

def harmony(notes, t0, S, above=True):
    """各音に、その小節の和音の音のうち 3〜4 半音上（above）か下の音を合わせる"""
    out = []
    for t, d, h, suf in toks(notes):
        if h.startswith("R"): out.append(f"{h}:{d:g}{suf}"); continue
        m = midi(h); pcs = S.bars[int((t0 + t) // 4)][2].pcs()
        rng = range(2, 10)
        cands = [m + k for k in rng if (m + k) % 12 in pcs] if above else [m - k for k in rng if (m - k) % 12 in pcs]
        pick = next((c for c in cands if 3 <= abs(c - m) <= 4), cands[0] if cands else (m + 3 if above else m - 3))
        out.append(f"{name(pick)}:{d:g}{suf}")
    return " ".join(out)

def seg(p, a, b):
    return " ".join(f"{h}:{d:g}{suf}" for t, d, h, suf in toks(p["notes"]) if a - 1e-9 <= t < b - 1e-9)

def make(path, vocal=True):
    song, S = build(copy.deepcopy(SPEC))
    st = starts(FORM)
    full = st["outro"][0] + 4 * 4
    parts = [p for p in song["parts"] if p["role"] != "ライザー"]
    retone_leads(parts)
    lead = part(parts, "リード（旋律）")
    lead["fx"] = [{"type": "eq", "low": -2, "mid": 2.5, "midHz": 1200, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 7500, "q": 0.7},
                  {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.25}, {"type": "plate", "mix": 0.16}]
    lead["phrase"] = 8
    lead, quiet = split_lead(parts, st, ("verse1", "verse2", "bridge", "intro"), volume=0.1, role="リード（Aメロ・ブリッジ）")
    rhythm = part(parts, "刻み")
    bass = part(parts, inst="bass")
    arp = part(parts, "リードギター（分散和音）")
    # Aメロ1の前半8小節はリズムギターを抜き、クリーンの分散和音だけ。後半からリズムギター
    a, n = st["verse1"]; put(rhythm, a, a + 8 * 4); put(arp, a + 8 * 4, a + n * 4)
    # ラストサビの頭4小節: リズムギター・ベースを抜く（リードと分散和音とキックだけ）。分散和音はその4小節だけ
    a, n = st["chorus3"]; put(rhythm, a, a + 16); put(bass, a, a + 16); put(arp, a + 16, a + n * 4)
    # イントロ: 1〜4小節は分散和音とリード（サビの先出し）。4小節目の4拍目は全員休み。5〜8小節は看板リフ
    a, _ = st["intro"]; put(arp, a + 16, a + 32); put(arp, a + 15, a + 16); put(bass, a, a + 16)
    riff = {"instrument": "distGuitar", "role": "看板リフ", "volume": 0.11, "pan": 0, "guitarTone": "loud-mid", "gainDb": -3, "powerChord": False, "notes": f"R:{full}"}
    for sid, frm, nb in (("intro", 4, 4), ("inter1", 0, 8), ("outro", 0, 2)):
        a, _ = st[sid]; put(riff, a + frm * 4, a + (frm + nb) * 4, sig(nb))
    # ベース: 看板リフの下は D のペダル（4分）。Bメロも D のペダル（8分）。ブレイクダウンは和音の一撃とそろえる
    for sid, frm, nb in (("intro", 4, 4), ("inter1", 0, 8), ("outro", 0, 2)):
        a, _ = st[sid]; put(bass, a + frm * 4, a + (frm + nb) * 4, " ".join(["D2:1! D2:1 D2:1 D2:1"] * nb))
    for sid in ("pre1", "pre2"):
        a, n = st[sid]; put(bass, a, a + (n - 1) * 4, " ".join(["D2:0.5! D2:0.5 D2:0.5 D2:0.5 D2:0.5! D2:0.5 D2:0.5 D2:0.5"] * (n - 1))); put(bass, a + (n - 1) * 4, a + n * 4, "D2:3! R:1")
    bd = " ".join([BD_A, BD_B, BD_A, BD_C, BD_A, BD_B, BD_C, BD_END])
    a, _ = st["break"]
    put(riff, a, a + 32, bd); put(bass, a, a + 32, bd)
    a, _ = st["outro"]; put(rhythm, a + 8, a + 16, "D2:8!"); put(bass, a + 8, a + 16, "D2:8!"); put(riff, a + 8, a + 16, "R:8")
    parts.insert(parts.index(rhythm) + 1, riff)
    # 4本重ね: 内側の2本（ブーストなし・−5dB・±0.75）はサビとブレイクダウンだけ
    inner = json.loads(json.dumps(rhythm)); inner["role"] = "リズム（内側の2本）"; inner["gainDb"] = rhythm.get("gainDb", -5) - 5; inner["guitarTone"] = "loud-mid-hs"; inner["pan"] = 0
    inner["notes"] = f"R:{full}"
    for sid in ("chorus1", "chorus2"):
        a, n = st[sid]; put(inner, a, a + n * 4, seg(rhythm, a, a + n * 4))
    a, n = st["chorus3"]; put(inner, a + 16, a + n * 4, seg(rhythm, a + 16, a + n * 4))
    parts.insert(parts.index(riff) + 1, inner)
    # ハモり: サビ2は長い音だけ3度上、ラストサビ（5小節目から）は3度上＋オクターブ下
    harm = json.loads(json.dumps(lead)); harm["role"] = "リード（ハモり）"; harm["volume"] = 0.08; harm["pan"] = 0.35; harm["notes"] = f"R:{full}"
    a, n = st["chorus2"]
    s2 = " ".join((f"{h}:{d:g}{suf}" if d >= 1.5 or h.startswith("R") else f"R:{d:g}") for t, d, h, suf in toks(seg(lead, a, a + n * 4)))
    put(harm, a, a + n * 4, harmony(s2, a, S))
    a, n = st["chorus3"]; put(harm, a + 16, a + n * 4, harmony(seg(lead, a + 16, a + n * 4), a + 16, S))
    octv = json.loads(json.dumps(lead)); octv["role"] = "リード（オクターブ下）"; octv["volume"] = 0.07; octv["pan"] = -0.3; octv["notes"] = f"R:{full}"
    low = " ".join((f"{name(midi(h) - 12)}:{d:g}{suf}" if not h.startswith("R") else f"{h}:{d:g}{suf}") for t, d, h, suf in toks(seg(lead, a + 16, a + n * 4)))
    put(octv, a + 16, a + n * 4, low)
    lead["pan"] = -0.05
    parts.insert(parts.index(quiet) + 1, harm); parts.insert(parts.index(harm) + 1, octv)
    # ブリッジのリードはゆっくり立ち上がる（ボリューム奏法の代わりに attack）
    quiet["attack"] = 0.25
    # ── 作り込み（docs/sound/modern-loud-rock/arrangement-detail.md）──
    drum_detail(parts, st, FORM, ("verse1", "verse2", "chorus1", "chorus2", "chorus3", "inter1"))
    # サビ2 → ブリッジ: 1拍目に全員の一撃、残りはたたかずに鳴らし切る（いちばん大きな落差）
    a, n = st["chorus2"]; lb = a + (n - 1) * 4
    for p in parts:
        if p["instrument"] in ("kick", "snare"): put(p, lb, lb + 4, "X")
        if p["instrument"] == "hihat": put(p, lb, lb + 4)
    put(part(parts, inst="tom"), lb, lb + 4); put(part(parts, inst="crash"), lb, lb + 4, "C2:4!")
    # 看板リフを育てる: 看板リフの区間の後半4小節は1オクターブ上（変えるのは高さだけ）
    a, _ = st["inter1"]
    up = " ".join((f"{name(midi(h) + 12)}:{d:g}{suf}" if not h.startswith("R") else f"{h}:{d:g}{suf}") for t, d, h, suf in toks(seg(riff, a + 16, a + 32)))
    put(riff, a + 16, a + 32, up)
    # ブリッジの後半4小節: 看板リフの頭3音だけを、長さ2倍・分散和音のギターで（切り詰め＋引きのばし）
    a, n = st["bridge"]
    put(arp, a + 16, a + 32, " ".join(["D4:1! D5:1 D4:1 F5:1"] * 2 + ["D4:1! D5:1 D4:1 G5:1", "D4:1! A4:1 D5:2"]))
    # 伸ばす高い層（E-Bow 風。サビ2とラストサビの5小節目から）: 和音の3度か9度を2小節ずつ、ゆっくり立ち上げる
    pad = {"instrument": "distGuitar", "role": "伸ばす高い層", "volume": 0.05, "pan": 0.45, "powerChord": False, "double": False, "di": "emily", "autoScoop": False,
           "attack": 0.4, "reverb": 0.4, **{k: v for k, v in LEAD_TONE.items() if k in ("amp", "ampCabIr", "ampGate", "humanPitch", "noScoop")}, "ampDrive": 0.4,
           "fx": [{"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}, {"type": "delay", "beats": 0.75, "mix": 0.25, "feedback": 0.35}, {"type": "plate", "mix": 0.3}],
           "notes": f"R:{full}"}
    PADN = {"6": "D6", "6add9": "C6", "3": "A5", "4": "B5", "5sus4": "D6", "5": "C#6", "7": "E5", "1madd9": "E5"}
    for sid, frm in (("chorus2", 0), ("chorus3", 4)):
        a, n = st[sid]; chs = dict(FORM_D)[sid].split()
        for b in range(frm, n, 2):
            put(pad, a + b * 4, a + (b + 2) * 4, f"{PADN.get(chs[b], 'A5')}:8")
    parts.insert(parts.index(arp), pad)
    # 耳のごちそう: リードが休んでいる拍にハーモニクス（12フレット相当の高い音、余韻長め）。4小節目と8小節目の後半
    harmo = {"instrument": "distGuitar", "role": "ハーモニクス（飾り）", "volume": 0.05, "pan": -0.5, "powerChord": False, "double": False, "di": "emily", "autoScoop": False,
             "amp": "clean", "reverb": 0.55, "fx": [{"type": "delay", "beats": 0.75, "mix": 0.3, "feedback": 0.4}], "notes": f"R:{full}"}
    for sid in ("verse1", "verse2", "chorus1", "chorus2", "chorus3", "pre1"):
        a, n = st[sid]
        for b in range(3, n, 4):
            pos = a + b * 4 + 3
            busy = any(not h.startswith("R") and t0 < pos + 1 and t0 + d > pos for t0, d, h, suf in toks(lead["notes"]) + toks(quiet["notes"]))
            if not busy:
                put(harmo, pos, pos + 1, ["D6:1!", "A5:1!", "F#6:1!", "E6:1!"][(b // 4) % 4] if sid.startswith("chorus") else ["D6:1!", "A5:1!"][(b // 4) % 2])
    parts.insert(parts.index(arp), harmo)
    # ベースのスライド: Bメロの最後の伸ばす根音の終わりを下へ滑らせる（サビの頭へ）
    for sid in ("pre1", "pre2"):
        a, n = st[sid]; put(bass, a + (n - 1) * 4, a + n * 4, "D2:3!\\ R:1")
    song["human"] = 0.3
    add_heavy_kick(parts)
    bass.update({"amp": "bassSplit", "ampDrive": 0.6, "duck": 0.25, "fx": [{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}]})
    plain_guitars(parts)
    if vocal:
        # 歌の旋律（リード2本を合わせた音）→ 歌に。リードギターは前奏の先出しだけ残し、ハモり・オクターブ下は歌に任せて外す
        merged = {"notes": f"R:{full}"}
        for p_ in (quiet, lead):
            for t, d, h, suf in toks(p_["notes"]):
                if not h.startswith("R"): put(merged, t, t + d, f"{h}:{d:g}{suf}")
        L = LYRICS
        sids = [("verse1", L["verse1"]), ("pre1", L["pre"]), ("chorus1", L["chorus"]), ("verse2", L["verse2"]), ("pre2", L["pre"]),
                ("chorus2", L["chorus"]), ("bridge", L["bridge"]), ("chorus3", L["chorus"])]
        vn = vocal_notes(merged["notes"], st, sids, full)
        song["vocals"] = [{"voice": "teto", "notes": vn, "volume": 1.0, "pan": 0, "reverb": 0.2}]
        song["vocalLevel"] = 1.0
        for sid, _ in sids:
            a, n = st[sid]; put(lead, a, a + n * 4); put(quiet, a, a + n * 4)
        parts[:] = [p_ for p_ in parts if p_["role"] not in ("リード（ハモり）", "リード（オクターブ下）")]
    song["dynamics"] = "natural"
    finish(song, parts, SPEC["title"])
    json.dump(song, open(path, "w"), ensure_ascii=False)
    return song, st

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lr/opt/full/n7-gyakkou.json"
    s, st = make(out)
    inst = json.loads(json.dumps(s)); inst.pop("vocals", None); inst.pop("vocalLevel", None)
    json.dump(inst, open(out.replace(".json", "-inst.json"), "w"), ensure_ascii=False)   # 伴奏だけ（パソコンで書き出す）
    for p in s["parts"]: print(p["role"], p["notes"][:90])
    print("小節", sum(f[2] for f in FORM), "秒", round(sum(f[2] for f in FORM) * 4 * 60 / SPEC["bpm"]), "最初のサビ", round(st["chorus1"][0] * 60 / SPEC["bpm"]), "秒")
