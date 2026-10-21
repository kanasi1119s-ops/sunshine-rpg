# ラウドロック・ラウドメタル25曲の設計表（2026-10-21 人間の指示。曲調を全部変える。キーボードをバイオリン・チェロにした曲もある）
# 使い方: python3 loud25.py <出力フォルダ> [番号...]   → <出力フォルダ>/loud25-01-xxx.json …
#   書き出し: node tools/composer/song.mjs build <json> --wav --drums muldjord --bass pick [--piano salamander] --master-preset rock-clean
# 曲どうしで変えたもの: テンポ（76〜220）・拍子（4/4・3/4・6/8・7/4）・調と旋法・チューニング（ドロップA〜E）・ノリ（ドラムの型）・
#   刻みとリードの音色・足す楽器（ピアノ・バイオリンとチェロ・シンセ・合唱・加工ギター・なし）・入り方・終わり方・ベースの動機・技（スウィープ・タッピング・ソロ）
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from loud25_arrange import build

def form(bpm, beats, layout, target=272, unit=2):
    """layout: (id, kind, 重み, 進行)。曲の長さが target 秒前後になるように小節数を決める"""
    total = target * bpm / 60 / beats
    W = sum(w for _, _, w, _ in layout)
    out = []
    for sid, kind, w, prog in layout:
        n = max(unit, int(round(w * total / W / unit)) * unit)
        out.append((sid, kind, n, prog))
    return out

def std(beats_steps, feel):
    """ドラムの型（1文字＝16分。steps は 1小節の文字数）。feel ごとにセクションの型を返す"""
    n = beats_steps
    z = "." * n
    def at(pos, ch="X"):
        r = ["."] * n
        for p in pos: r[p % n] = ch
        return "".join(r)
    q = n // 4 if n % 4 == 0 else None
    if feel == "metalcore":
        return {
            "intro": {"k": "X..X..X...X.X...", "s": "....X.......X...", "c": "n.......r.r.r.r.", "fill": "tom"},
            "verse": {"k": "sync", "s": ["....X..o.o..X..o", "....X..o....X.XX"], "h": "x.x.x.x.x.x.x.x.", "fill": "snare"},
            "pre": {"k": ["X.......X.......", "X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X."], "s": ["........X.......", "........X.......", "....X.......X...", "....X...X...X.X."], "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": ["X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X..x..x.", "X..x..X.X...XXXX"], "s": "....X.......X...", "c": ["r.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.n.", "r.r.r.r.r.r.r.r."], "fill": "tom"},
            "inter": {"k": "sync", "s": "........X.......", "c": "n...n...n...n...", "fill": "snare"},
            "bridge": {"k": ["X...............", "........X......."], "s": ["................", "............o.o."], "c": ["r...r...r...r...", "r...r...r...r..."], "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "kick"},
            "solo": {"k": ["X..x..X.X..x..x.", "X..x..X.X..xXXXX"], "s": "....X.......X...", "c": ["r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.r."], "fill": "tom"},
            "outro": {"k": ["X...............", z], "s": z, "c": ["c...............", z], "crash": False, "nofill": True},
        }
    if feel == "djent":
        return {
            "intro": {"k": "sync", "s": "........X.......", "c": "r...r...r...r...", "fill": "snare"},
            "verse": {"k": "sync", "s": "........X.......", "c": ["r...r...r...r...", "r...r...r...n..."], "fill": "kick"},
            "pre": {"k": "sync", "s": ["....X.......X...", "....X...X...X.X."], "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": "sync", "s": "....X.......X...", "c": ["n.r.r.r.n.r.r.r.", "r.r.r.r.n.r.r.r."], "fill": "tom"},
            "inter": {"k": "sync", "s": "........X.......", "c": "u...u...u...u...", "fill": "snare"},
            "bridge": {"k": ["X...............", z], "s": [z, "........o......."], "c": "r.......r.......", "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "kick"},
            "solo": {"k": "sync", "s": "....X.......X...", "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "outro": {"k": ["X...............", z], "s": z, "c": ["c...............", z], "crash": False, "nofill": True},
        }
    if feel == "nu":
        return {
            "intro": {"k": "X..X..X.X......X", "s": "....X..o....X.o.", "h": "x.xxx.x.x.xxx.x.", "fill": "snare"},
            "verse": {"k": ["X..X..X.X......X", "X..X..X.X..X...."], "s": ["....X..o.o..X.o.", "....X..o....X..o"], "h": "x.xxx.x.x.xxx.x.", "fill": "snare"},
            "pre": {"k": "X.....X.X.......", "s": "....X.......X...", "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": ["X..X..X.X..X..X.", "X..X..X.X...X.X."], "s": "....X.......X...", "c": ["r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.r."], "fill": "tom"},
            "inter": {"k": "X.....X...X.....", "s": "....X.......X...", "h": "x.xxx.x.x.xxx.x.", "fill": "snare"},
            "bridge": {"k": ["X.......X.......", z], "s": ["....o.......o...", "....o.......o..."], "h": "x...x...x...x...", "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n...n...n...n...", "fill": "kick"},
            "solo": {"k": "X..X..X.X......X", "s": "....X..o....X.o.", "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "outro": {"k": ["X...............", z], "s": z, "c": ["c...............", z], "crash": False, "nofill": True},
        }
    if feel == "drive":   # 疾走（8分の推進。ツーバスは山場だけ）
        return {
            "intro": {"k": "X...X...X...X...", "s": "....X.......X...", "c": "c.r.r.r.r.r.r.r.", "fill": "snare"},
            "verse": {"k": ["X.x...X.X.x...x.", "X.x...X.X.x....."], "s": "....X.......X...", "h": "x.x.x.x.x.x.x.x.", "fill": "snare"},
            "pre": {"k": ["X...X...X...X...", "X.X.X.X.X.X.X.X."], "s": ["....X.......X...", "....X...X...X.X."], "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": ["X.x.X.x.X.x.X.x.", "X.x.X.x.X.x.X.x.", "X.x.X.x.X.x.X.x.", "X.x.X.x.X...XXXX"], "s": "....X.......X...", "c": ["c.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.r.", "n.r.r.r.r.r.r.r.", "r.r.r.r.r.r.r.n."], "fill": "tom"},
            "inter": {"k": "X..X..X.X..X..X.", "s": "....X.......X...", "c": "n...r...r...r...", "fill": "snare"},
            "bridge": {"k": ["X.......X.......", "X..............."], "s": ["................", "....o.......o..."], "h": "x...x...x...x...", "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "kick"},
            "solo": {"k": ["X.x.X.x.X.x.X.x.", "X.X.X.X.X.X.X.X."], "s": ["....X.......X...", ".X.X.X.X.X.X.X.X"], "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "outro": {"k": ["X...............", z], "s": z, "c": ["c...............", z], "crash": False, "nofill": True},
        }
    if feel == "industrial":
        return {
            "intro": {"k": "X...X...X...X...", "h": "..x...x...x...x.", "fill": "snare"},
            "verse": {"k": "X...X...X...X...", "s": "....X.......X...", "h": "..x...x...x...x.", "fill": "snare"},
            "pre": {"k": "X...X...X...X...", "s": ["....X.......X...", "....X...X.X.XXXX"], "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": ["X...X...X...X...", "X...X...X...X..X"], "s": "....X.......X...", "c": "r.r.r.r.r.r.r.r.", "fill": "snare"},
            "inter": {"k": "sync", "s": "........X.......", "c": "n...n...n...n...", "fill": "snare"},
            "bridge": {"k": "X.......X.......", "h": "..x...x...x...x.", "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "kick"},
            "solo": {"k": "X...X...X...X...", "s": "....X.......X...", "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "outro": {"k": ["X...X...X...X...", "X..............."], "s": z, "h": "..x...x...x...x.", "crash": False, "nofill": True},
        }
    if feel == "halftime":
        return {
            "intro": {"k": "X.......X.......", "s": "........X.......", "c": "r...r...r...r...", "fill": "snare"},
            "verse": {"k": ["X.....X.X.......", "X.....X.....X..."], "s": "........X.......", "h": "x...x...x...x...", "fill": "snare"},
            "pre": {"k": "X.......X.......", "s": ["........X.......", "....X.......X..."], "h": "x.x.x.x.x.x.x.x.", "fill": "stop"},
            "chorus": {"k": ["X..x..X.X..x....", "X..x..X.X...X.X."], "s": "....X.......X...", "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "inter": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "snare"},
            "bridge": {"k": ["X...............", z], "s": [z, "........o......."], "c": "r.......r.......", "crash": False, "fill": "snare"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.......n.......", "fill": "kick"},
            "solo": {"k": "X..x..X.X..x..x.", "s": "....X.......X...", "c": "r.r.r.r.r.r.r.r.", "fill": "tom"},
            "outro": {"k": ["X...............", z], "s": z, "c": ["c...............", z], "crash": False, "nofill": True},
        }
    raise ValueError(feel)

def generic(n, beat_len, groups, feel):
    """4/4 以外（3/4・6/8・7/4）のドラムの型。groups はまとまりの拍数（例 [2,2,3]）。beat_len は1拍の文字数"""
    z = "." * n
    starts = []; p = 0
    for g in groups:
        starts.append(p); p += g * beat_len
    def put(pos, ch="X", base=None):
        r = list(base or z)
        for x in pos: r[x % n] = ch
        return "".join(r)
    kick = put(starts)
    back = put([s + beat_len * (1 if g >= 2 else 0) for s, g in zip(starts, groups) if g >= 2])
    eighths = put(range(0, n, max(1, beat_len // 2)), "x")
    ride = put(range(0, n, max(1, beat_len // 2)), "r")
    chorus_k = put(starts + [s + beat_len // 2 for s in starts])
    return {
        "intro": {"k": kick, "s": z, "c": put(starts, "r"), "fill": "snare"},
        "verse": {"k": "sync", "s": back, "h": eighths, "fill": "snare"},
        "pre": {"k": kick, "s": back, "h": eighths, "fill": "stop"},
        "chorus": {"k": [chorus_k, chorus_k[:-4] + "XXXX" if n >= 8 else chorus_k], "s": back, "c": [ride, put([0], "n", ride)], "fill": "tom"},
        "inter": {"k": "sync", "s": back, "c": put(starts, "n"), "fill": "snare"},
        "bridge": {"k": [put([0]), z], "s": z, "c": put(starts, "r"), "crash": False, "fill": "snare"},
        "break": {"k": "sync", "s": put([starts[len(starts) // 2]]), "c": put(starts, "n"), "fill": "kick"},
        "solo": {"k": chorus_k, "s": back, "c": ride, "fill": "tom"},
        "outro": {"k": [put([0]), z], "s": z, "c": [put([0], "c"), z], "crash": False, "nofill": True},
    }

def L(*bars):  # 旋律のリズム（1小節ずつ）
    return [list(b) for b in bars]

SPECS = []
def song(**k): SPECS.append(k)

# ════════ 1. 天穹アンカー（メタルコア・疾走・ピアノ）════════
song(no=1, slug="tenkyu-anchor", title="天穹アンカー", seed=101, bpm=176, key="E", mode="aeolian", tuning="E2",
     desc="空へ錨を投げるような疾走メタルコア。Eマイナー・標準チューニング・ピアノ",
     form=form(176, 4, [("intro", "intro", 8, "1m 6 3 7"), ("verse1", "verse", 16, "1m 1m 6 6 4m 4m 5m 7"), ("pre1", "pre", 8, "6 7 1m 3"),
                        ("chorus1", "chorus", 16, "3 7 1m 6 3 7 4m 5"), ("inter", "interlude", 8, "1m 6"), ("verse2", "verse", 16, "1m 1m 6 6 4m 4m 5m 7"),
                        ("pre2", "pre", 8, "6 7 1m 3"), ("chorus2", "chorus", 16, "3 7 1m 6 3 7 4m 5"), ("bridge", "bridge", 12, "6maj7 7 3 4m7"),
                        ("break", "break", 8, "1m"), ("solo", "solo", 12, "1m 6 3 7"), ("chorus3", "chorus", 16, "3 7 1m 6 3 7 4m 5"), ("outro", "outro", 6, "1m")]),
     rhythm={"tone": "loud-mid", "pm": ["verse"], "intro": ["X-x-X-x-XXo-X---", "X-x-X-x-X-3-5---"], "verse": ["mmmm-mm-mmmm-mm-", "mmm-mmm-mm-mmmmm"],
             "pre": "X===x===X===x===", "chorus": ["X=====x=x=x=X===", "X=====x=x=x=x=x="], "inter": "X--X--X-X--X--3-",
             "bridge": "-", "break": ["X--X--X-X--X--X-", "X--X--X---XX-X--"], "solo": "x-x-x-x-x-x-x-x-", "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "B4", "hi": "B5", "rhythm": L([1.5, 0.5, 1, 1], [1, 1, 2], [0.5, 0.5, 1, 1, 1], [3, 1]), "peak": 5},
                                              "inter": {"lo": "E5", "hi": "E6", "rhythm": L([0.5] * 8, [1, 1, 1, 1], [0.5] * 8, [4])}}},
     tech={"solo": "mmsmmmtt", "inter": "--ss"},
     bass={"intro": ["R:0.5! -:0.5 R:0.5 -:0.5 R:0.5! 8:0.5' R:0.5 5:0.5", "R:0.5! -:0.5 R:0.5 -:0.5 R:0.5 3:0.5 5:0.5 b:0.5"],
           "verse": ["R:0.25! R:0.25' R:0.25' R:0.25' -:0.25 R:0.25' R:0.5 R:0.25! R:0.25' 8:0.5! 5:0.5 3:0.5", "R:0.75! R:0.25' R:0.5 5:0.5 8:0.5! 7:0.5 5:0.5 b:0.5"],
           "pre": ["R:1! 5:0.5 8:0.5 7:1 5:1", "3:0.5 5:0.5 8:1! 9:0.5 8:0.5 7:0.5 b:0.5"],
           "chorus": ["R:1.5! R:0.5 5:0.5 8:0.5! 7:0.5 5:0.5", "3:0.5 R:0.5 5:1! 8:0.5 7:0.5 5:0.5 b:0.5"],
           "chorus_end": "R:0.5! R:0.5 5:0.5 8:0.5 9:0.25 8:0.25 7:0.25 5:0.25 3:0.25 4:0.25 5:0.25 b:0.25",
           "inter": "R:0.5! -:0.5 R:0.5 -:0.25 R:0.25 R:0.5 -:0.5 R:0.5 3:0.5", "bridge": ["8:1.5! 7:0.5 5:1 3:1", "4:1 5:1 7:1.5 b:0.5"],
           "break": ["R:0.75! -:0.5 R:0.75 -:0.5 R:0.5 -:0.75 R:0.25", "R:0.75! -:0.5 R:0.75 -:0.5 R:0.5 5:0.5 b:0.5"], "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5! R:0.5 7:0.5 b:0.5",
           "outro": ["R:4!", "-:4"]},
     drums=std(16, "metalcore"),
     extras={"piano": {"arp": "intro,bridge,outro", "chords": "chorus", "soft": "verse,pre", "chordRhythm": [1.5, 1, 1.5]}},
     modulate=1)

# ════════ 2. 鉄紺のパルス（ジェント・8弦の低いF#・シンセの空気）════════
song(no=2, slug="tekkon-pulse", title="鉄紺のパルス", seed=202, bpm=132, key="F#", mode="phrygian", tuning="F#1",
     desc="8弦の低いF#で刻む、拍がずれていくジェント。フリジアン・シンセの空気",
     form=form(132, 4, [("intro", "intro", 8, "1m 1m"), ("verse1", "verse", 16, "1m 1m 2 1m"), ("pre1", "pre", 8, "6 7 6 7"),
                        ("chorus1", "chorus", 16, "6maj7 3 7 1m"), ("verse2", "verse", 16, "1m 1m 2 1m"), ("chorus2", "chorus", 16, "6maj7 3 7 1m"),
                        ("bridge", "bridge", 12, "4m7 6maj7"), ("break", "break", 12, "1m 2"), ("chorus3", "chorus", 16, "6maj7 3 7 1m"), ("outro", "outro", 6, "1m")]),
     rhythm={"tone": "djent-8", "noPower": True, "intro": ["X--x-x--X--x-x--", "X--x-x--X-x-x---"], "verse": ["X--x-x--X--x-x-b", "X--xx-x--X-x-xx-"],
             "pre": "X==-X==-X==-X===", "chorus": ["X=====x=X=====x=", "X===x===X=x=x==="], "bridge": "-", "break": ["X---x---x--x--x-", "X--x--x--x--x-bX"],
             "outro": "X==============="},
     lead={"tone": "warm-lead-a", "sections": {"chorus1,chorus2,chorus3": {"lo": "C#5", "hi": "C#6", "rhythm": L([2, 1, 1], [1, 1, 2], [1.5, 0.5, 2], [4]), "peak": 4},
                                               "bridge": {"lo": "A4", "hi": "A5", "rhythm": L([3, 1], [2, 2], [3, 1], [4])}}},
     bass={"intro": ["R:0.75! -:0.25 R:0.25' R:0.5 -:0.25 R:0.75! -:0.25 R:0.25' R:0.5 -:0.25", "R:0.75! -:0.25 R:0.25' R:0.5 -:0.25 R:0.5! -:0.25 R:0.5 -:0.75"],
           "verse": ["R:0.75! -:0.25 R:0.25' R:0.5 -:0.25 R:0.75! -:0.25 R:0.25' R:0.5 9:0.25", "R:0.75! -:0.25 R:0.25' R:0.5 -:0.25 8:0.5! 7:0.5 5:0.5 b:0.5"],
           "pre": ["R:0.75! R:0.75 R:0.5 R:0.75 R:0.75 R:0.5", "R:1! 5:1 8:1 7:1"], "chorus": ["R:2! 5:1 8:1", "7:1 5:1 3:1 b:1"], "bridge": ["8:2! 7:1 5:1", "3:2 5:1 b:1"],
           "break": ["R:1! -:1 R:0.75 R:0.5 R:0.75", "R:0.75! -:0.25 R:0.75 -:0.25 R:0.75 -:0.25 9:0.5 R:0.5"], "outro": ["R:4!", "-:4"]},
     drums=std(16, "djent"),
     extras={"synth": {"wall": "intro,chorus,bridge", "pluck": ""}}, riserTo=["chorus", "break"])

# ════════ 3. 錆色ジャンクション（ニューメタル・跳ねるノリ・加工ギター）════════
song(no=3, slug="sabiiro-junction", title="錆色ジャンクション", seed=303, bpm=98, key="C", mode="dorian", tuning="C2",
     desc="跳ねるニューメタル。Cドリアン・ドロップC・加工ギターとチェロ",
     form=form(98, 4, [("intro", "intro", 6, "1m"), ("verse1", "verse", 16, "1m 1m 4 4"), ("pre1", "pre", 6, "7 7 4 5m"),
                       ("chorus1", "chorus", 12, "1m 3 4 7"), ("verse2", "verse", 12, "1m 1m 4 4"), ("chorus2", "chorus", 12, "1m 3 4 7"),
                       ("bridge", "bridge", 10, "b6 7 1m 1m"), ("break", "break", 8, "1m"), ("chorus3", "chorus", 12, "1m 3 4 7"), ("outro", "outro", 4, "1m")], unit=2),
     rhythm={"tone": "nu-metal-wall", "intro": "X--X--X-X---x-x-", "verse": ["X--X--X-X------b", "X--X--X-X--X-3-5"], "pre": "X=======X==-X===",
             "chorus": ["X=====x=X=====x=", "X=====x=x=x=X==="], "bridge": "-", "break": ["X--X--X-X---X---", "X--X--X-X-X-X-XX"], "outro": "X==============="},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "G4", "hi": "G5", "rhythm": L([1, 0.5, 0.5, 1, 1], [0.5, 0.5, 1, 2], [1, 1, 1, 1], [3, 1])}}},
     bass={"intro": "R:0.75! R:0.75' R:0.5 R:0.5! -:0.5 8:0.25' R:0.25, -:0.5", "verse": ["R:0.75! R:0.75' R:0.5 R:0.5 -:0.5 8:0.25' R:0.25, 5:0.5", "R:0.75! R:0.75' R:0.5 R:0.5 3:0.5 4:0.5 b:0.5"],
           "pre": ["R:2! 5:1 8:1", "7:1 5:1 4:1 b:1"], "chorus": ["R:1.5! R:0.5 8:0.5' R:0.5 5:0.5 3:0.5", "R:1! 5:0.5 8:0.5 7:0.5 5:0.5 4:0.5 b:0.5"],
           "bridge": ["8:1.5! 7:0.5 5:1 4:1", "3:1 4:1 5:1.5 b:0.5"], "break": ["R:0.75! R:0.75 R:0.5 R:2", "R:0.75! R:0.75 R:0.5 R:0.5 R:0.5 5:0.5 b:0.5"], "outro": "R:4!"},
     drums=std(16, "nu"),
     extras={"gated": "verse,break", "strings": {"cello": "bridge,chorus", "celloMotif": ["R:2 5:2", "3:2 b:2"]}}, trigger="punch")

# ════════ 4. 白夜のガロップ（ギャロップ・和声的短音階・バイオリン）════════
song(no=4, slug="byakuya-gallop", title="白夜のガロップ", seed=404, bpm=186, key="A", mode="harmonic", tuning="A1",
     desc="白夜を駆けるギャロップのラウドメタル。Aの和声的短音階・ドロップA・バイオリンが歌う",
     form=form(186, 4, [("intro", "intro", 8, "1m 1m 5 5"), ("verse1", "verse", 16, "1m 6 4m 5"), ("pre1", "pre", 8, "4m 5 6 5"),
                        ("chorus1", "chorus", 16, "1m 3aug 6 5"), ("inter", "interlude", 8, "1m 5"), ("verse2", "verse", 16, "1m 6 4m 5"),
                        ("chorus2", "chorus", 16, "1m 3aug 6 5"), ("bridge", "bridge", 16, "6 7dim 1m 5"), ("solo", "solo", 16, "1m 6 4m 5"),
                        ("chorus3", "chorus", 16, "1m 3aug 6 5"), ("outro", "outro", 8, "1m 5 1m")]),
     rhythm={"tone": "loud-high", "pm": ["verse"], "intro": "X-xxX-xxX-xxX-xx", "verse": ["m-mmm-mmm-mmm-mm", "m-mmm-mmm-mmX==="], "pre": "X===X===X=x=X===",
             "chorus": ["X-xxX-xxX-xxX-xx", "X-xxX-xxX===X==="], "inter": "X-xxX-xx5-xx5-xx", "bridge": "-", "solo": "X-xxX-xxX-xxX-xx", "outro": "X==============="},
     lead={"tone": "warm-lead-b", "sections": {"inter": {"lo": "E5", "hi": "E6", "rhythm": L([0.5] * 8, [0.5, 0.5, 1, 2])},
                                               "chorus1,chorus2,chorus3": {"inst": "violin", "lo": "A4", "hi": "C6", "rhythm": L([1.5, 0.5, 1, 1], [2, 1, 1], [1, 1, 1, 1], [4]), "peak": 6},
                                               "bridge": {"inst": "violin", "lo": "E4", "hi": "E5", "rhythm": L([2, 2], [3, 1], [2, 1, 1], [4])}}},
     tech={"solo": "mmmmssmmmmtttt--"},
     bass={"intro": "R:0.5! R:0.25 R:0.25 R:0.5 R:0.25 R:0.25 R:0.5 R:0.25 R:0.25 5:0.5 3:0.25 b:0.25", "verse": ["R:0.5! R:0.25' R:0.25' R:0.5 R:0.25' R:0.25' R:0.5 R:0.25' R:0.25' 8:0.5! 5:0.25 3:0.25", "R:0.5! R:0.25' R:0.25' 3:0.5 5:0.5 8:1! 7:0.5 b:0.5"],
           "pre": ["R:1! 5:1 8:1 5:1", "7:1 8:1 9:1 b:1"], "chorus": ["R:0.5! R:0.25 R:0.25 R:0.5 R:0.25 R:0.25 5:0.5 R:0.25 R:0.25 8:0.5 7:0.5", "R:0.5! 3:0.5 5:0.5 8:0.5 7:0.5 5:0.5 3:0.5 b:0.5"],
           "inter": "R:0.5! R:0.25 R:0.25 5:0.5 R:0.25 R:0.25 8:0.5 R:0.25 R:0.25 7:0.5 b:0.5", "bridge": ["R:2! 5:2", "3:2 b:2"], "solo": "R:0.5! R:0.25 R:0.25 R:0.5 R:0.25 R:0.25 R:0.5 8:0.5 5:0.5 b:0.5",
           "outro": ["R:4!", "5:4", "R:4!", "-:4"]},
     drums={**std(16, "drive"), "verse": {"k": "sync", "s": "....X.......X...", "h": "x.x.x.x.x.x.x.x.", "fill": "snare"}},
     extras={"strings": {"cello": "bridge", "celloMotif": ["R:2 5:2", "8:2 7:2"], "pad": "chorus,bridge"}}, modulate=2)

# ════════ 5. 群青ハーフタイム（ハーフタイムの重さ・合唱）════════
song(no=5, slug="gunjo-halftime", title="群青ハーフタイム", seed=505, bpm=140, key="B", mode="aeolian", tuning="B1",
     desc="ゆったり重いハーフタイムのメタルコア。Bマイナー・ドロップB・合唱の厚み",
     form=form(140, 4, [("intro", "intro", 8, "1m 6 4m 5m"), ("verse1", "verse", 16, "1m 1m 7 6"), ("pre1", "pre", 8, "4m 4m 6 7"),
                        ("chorus1", "chorus", 16, "6 7 1m 3"), ("verse2", "verse", 16, "1m 1m 7 6"), ("pre2", "pre", 8, "4m 4m 6 7"),
                        ("chorus2", "chorus", 16, "6 7 1m 3"), ("bridge", "bridge", 12, "3maj7 6maj7"), ("break", "break", 12, "1m b2 1m 7"),
                        ("chorus3", "chorus", 16, "6 7 1m 3"), ("outro", "outro", 8, "1m 6 1m")]),
     rhythm={"tone": "modern-metalcore", "pm": ["verse"], "intro": ["X=======X===x===", "X=======x===X==="], "verse": ["m-m--m-mm---m-m-", "m-m--m-mm-m-mmmm"],
             "pre": "X===X===X===X===", "chorus": ["X=======x===x===", "X=======X===x=x="], "bridge": "-", "break": ["X--X--X-----X---", "X--X--X---b-X-b-"], "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "D5", "hi": "D6", "rhythm": L([2, 1, 1], [3, 1], [1, 1, 1, 1], [4]), "peak": 5}}},
     bass={"intro": ["R:2! 5:1 8:1", "7:2 5:1 b:1"], "verse": ["R:0.5! -:0.5 R:0.25 -:0.5 R:0.25' R:0.5 -:1 R:0.25 R:0.25", "R:0.5! -:0.5 R:0.25 -:0.5 R:0.25' 8:1! 7:0.5 b:0.5"],
           "verse_b": ["R:0.5! -:0.5 R:0.25 -:0.5 R:0.25' R:0.5 3:0.5 5:0.5 8:0.5", "8:1! 7:0.5 5:0.5 3:1 b:1"], "pre": ["R:1! R:1 5:1 8:1", "7:1 8:1 9:1 b:1"],
           "chorus": ["R:2! 8:1 5:1", "3:1.5 5:0.5 8:1 b:1"], "bridge": ["8:3! 7:1", "5:2 3:1 b:1"], "break": ["R:0.75! -:0.25 R:0.5 R:0.75 -:1.25 R:0.5", "R:0.75! -:0.25 R:0.5 R:0.75 -:0.75 9:0.5 b:0.5"],
           "outro": ["R:4!", "-:4"]},
     drums=std(16, "halftime"), extras={"choir": "chorus,bridge"}, riserTo=["chorus", "break"])

# ════════ 6. 六つ拍子の灯台（6/8・バイオリンとチェロ）════════
song(no=6, slug="mutsubyoshi-toudai", title="六つ拍子の灯台", seed=606, bpm=168, beats=6, res=0.5, key="D", mode="aeolian", tuning="D2",
     desc="6/8 で揺れる重いバラード調のラウドメタル。Dマイナー・ドロップD・チェロとバイオリン",
     form=form(168, 6, [("intro", "intro", 6, "1m 6 3 7"), ("verse1", "verse", 12, "1m 7 6 7"), ("pre1", "pre", 6, "4m 5m 6 7"),
                        ("chorus1", "chorus", 12, "3 7 1m 6"), ("verse2", "verse", 12, "1m 7 6 7"), ("chorus2", "chorus", 12, "3 7 1m 6"),
                        ("bridge", "bridge", 10, "6maj7 4m7"), ("solo", "solo", 8, "1m 6 4m 5"), ("chorus3", "chorus", 12, "3 7 1m 6"), ("outro", "outro", 6, "1m")]),
     rhythm={"tone": "marshall-mid", "intro": "-", "verse": ["X==x==X==x-x", "X==x==X=xX=="], "pre": "X=====X=====", "chorus": ["X=====X==x==", "X==x==X====="],
             "bridge": "-", "solo": "X==x==X==x==", "outro": "X==========="},
     lead={"tone": "warm-lead-b", "sections": {"chorus1,chorus2,chorus3": {"inst": "violin", "lo": "A4", "hi": "D6", "rhythm": L([3, 1, 2], [2, 1, 3], [1, 1, 1, 3], [6]), "peak": 5},
                                               "intro": {"inst": "violin", "lo": "D5", "hi": "A5", "rhythm": L([3, 3], [2, 1, 3], [3, 3], [6])},
                                               "verse2": {"lo": "D5", "hi": "D6", "rhythm": L([6], [3, 3], [6], [6])}}},
     tech={"solo": "mmmmmm--"},
     bass={"intro": "-:6", "verse": ["R:3! 5:2 8:1", "7:3 5:2 b:1"], "verse_b": ["R:2! 3:1 5:2 8:1", "9:1 8:1 7:1 5:2 b:1"], "pre": ["R:3! 5:3", "8:2 7:1 b:3"],
           "chorus": ["R:1.5! R:0.5 5:1 8:2 7:1", "3:2 5:1 b:3"], "bridge": ["8:4! 7:2", "5:3 b:3"], "solo": "R:2! 5:1 8:2 b:1", "outro": "R:6!"},
     drums=generic(12, 2, [3, 3], "six"),
     extras={"strings": {"cello": "intro,verse,bridge,outro", "celloMotif": ["R:3 5:3", "8:2 7:1 5:3"], "pad": "chorus,bridge"}}, riserTo=["chorus"])

# ════════ 7. 七拍目の雷鳴（7/4・フリジアン・ドミナント・タッピングで始まる）════════
song(no=7, slug="nanahakume-raimei", title="七拍目の雷鳴", seed=707, bpm=150, beats=7, key="E", mode="phrygdom", tuning="E2", grouping=[2, 2, 3],
     desc="2+2+3 の7拍子で進むプログレッシブ・メタル。Eフリジアン・ドミナント・タッピングで幕開け",
     form=form(150, 7, [("intro", "intro", 6, "1 2"), ("verse1", "verse", 10, "1 1 2 1"), ("pre1", "pre", 4, "4m 2"), ("chorus1", "chorus", 8, "6 7m 1 1"),
                        ("inter", "interlude", 6, "1 2"), ("verse2", "verse", 10, "1 1 2 1"), ("chorus2", "chorus", 8, "6 7m 1 1"), ("solo", "solo", 10, "1 4m 2 1"),
                        ("break", "break", 6, "1 2"), ("chorus3", "chorus", 8, "6 7m 1 1"), ("outro", "outro", 4, "1")]),
     rhythm={"tone": "electro-rock", "intro": "-", "verse": ["X--x--X--x--X--x-x-X-b-X----", "X--x--X--x--X-x-x-X--b-X-b--"], "pre": "X=======X=======X===========",
             "chorus": ["X=======X=======X===x===x===", "X=======X=======X=====x=x=x="], "inter": "X--x--X--x--X--x-x-X-2-3-5--",
             "solo": "X-x-X-x-X-x-X-x-X-x-X-x-x-x-", "break": ["X--X--X-X--X--X-X--X--X-X---", "X--X--X-X--X--X-X--X--XbXbXb"], "outro": "X==========================="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "B4", "hi": "B5", "rhythm": L([2, 2, 3], [1, 1, 2, 3], [2, 2, 1, 2], [7]), "peak": 3}}},
     tech={"intro": "tttttt", "inter": "ttssss", "solo": "mmmmssmmtt"},
     bass={"intro": "-:7", "verse": ["R:0.75! -:0.25 R:0.5 -:0.5 R:0.75! -:0.25 R:0.5 -:0.5 R:0.5 R:0.5 5:0.5 8:1! b:0.5", "R:0.75! -:0.25 R:0.5 -:0.5 R:0.75 -:0.25 3:0.5 4:0.5 5:1! 7:0.5 8:0.5 b:1"],
           "pre": "R:2! 5:2 8:1.5 b:1.5", "chorus": ["R:2! 8:2 7:1.5 5:1.5", "3:2 5:2 8:1 7:1 b:1"], "inter": "R:0.75! -:0.25 R:0.5 -:0.5 R:0.75 -:0.25 R:0.5 -:0.5 R:0.5 3:0.5 5:0.5 8:0.5 b:1",
           "solo": "R:1! 5:1 8:1 5:1 R:1 7:1 b:1", "break": ["R:0.75! -:0.25 R:0.75 -:0.25 R:0.5 R:0.75 -:0.25 R:0.75 -:0.25 R:0.5 R:0.75 -:0.25 R:1", "R:0.75! -:0.25 R:0.75 -:0.25 R:0.5 R:0.75 -:0.25 R:0.75 -:0.25 R:0.5 b:0.5 R:0.5 b:1"],
           "outro": "R:7!"},
     drums=generic(28, 4, [2, 2, 3], "seven"), extras={"synth": {"pluck": "verse,chorus", "pluckPatch": "glassPluck"}})

# ════════ 8. ネオン血統（インダストリアル・4つ打ち・加工ギターとシンセ）════════
song(no=8, slug="neon-kettou", title="ネオン血統", seed=808, bpm=128, key="F#", mode="phrygian", tuning="F#1",
     desc="4つ打ちで押し進むインダストリアル・メタル。F#フリジアン・低いF#・加工ギターとシンセの壁",
     form=form(128, 4, [("intro", "intro", 8, "1m"), ("verse1", "verse", 16, "1m 1m 2 1m"), ("pre1", "pre", 8, "6 6 7 7"), ("chorus1", "chorus", 16, "1m 6 3 7"),
                        ("verse2", "verse", 16, "1m 1m 2 1m"), ("chorus2", "chorus", 16, "1m 6 3 7"), ("bridge", "bridge", 12, "6maj7 3"), ("break", "break", 8, "1m 2"),
                        ("chorus3", "chorus", 16, "1m 6 3 7"), ("outro", "outro", 8, "1m")]),
     rhythm={"tone": "electro-rock", "intro": "-", "verse": ["X---x-x-X---x-x-", "X---x-x-X-x-x-bx"], "pre": "X=======X=======", "chorus": ["X===x===X===x===", "X===x===X=x=x=x="],
             "bridge": "-", "break": ["X--X--X---X--X--", "X--X--X---XbXbXb"], "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"inst": "synth", "lo": "C#5", "hi": "C#6", "rhythm": L([1, 1, 1, 1], [1.5, 0.5, 2], [1, 1, 1, 1], [4])},
                                             "bridge": {"lo": "F#4", "hi": "F#5", "rhythm": L([2, 2], [4], [2, 2], [4])}}},
     bass={"intro": ["R:0.5! -:0.5 R:0.5 -:0.5 R:0.5 -:0.5 R:0.5 -:0.5"], "verse": ["R:0.5! R:0.5 -:0.5 R:0.5 R:0.5 -:0.5 8:0.5' R:0.5", "R:0.5! R:0.5 -:0.5 R:0.5 3:0.5 5:0.5 9:0.5 b:0.5"],
           "pre": ["R:2! 5:2", "8:2 b:2"], "chorus": ["R:0.5! R:0.5 8:0.5 R:0.5 R:0.5 8:0.5 R:0.5 5:0.5", "R:0.5! 3:0.5 5:0.5 8:0.5 7:0.5 5:0.5 3:0.5 b:0.5"],
           "bridge": ["8:2! 7:2", "5:2 b:2"], "break": ["R:0.75! -:0.25 R:0.5 -:0.5 R:0.5 R:0.75 -:0.25 R:0.5", "R:0.75! -:0.25 R:0.5 -:0.5 b:0.5 R:0.5 b:0.5 R:0.5"], "outro": ["R:0.5! -:0.5 R:0.5 -:0.5 R:0.5 -:0.5 R:0.5 -:0.5", "R:4!"]},
     drums=std(16, "industrial"), extras={"gated": "intro,verse,outro", "synth": {"wall": "chorus,bridge"}}, riserTo=["chorus", "break"])

# ════════ 9. 朱夏ブレイクビーツ（ポストハードコア・長調・ピアノ）════════
song(no=9, slug="shuka-breakbeats", title="朱夏ブレイクビーツ", seed=909, bpm=190, key="G", mode="ionian", tuning="E2",
     desc="明るい長調で駆けるポストハードコア。Gメジャー・標準チューニング・ピアノ",
     form=form(190, 4, [("intro", "intro", 8, "1 5 6m 4"), ("verse1", "verse", 16, "1 3m 4 5"), ("pre1", "pre", 8, "2m 3m 4 5"), ("chorus1", "chorus", 16, "4 5 3m 6m"),
                        ("inter", "interlude", 8, "1 5"), ("verse2", "verse", 16, "1 3m 4 5"), ("pre2", "pre", 8, "2m 3m 4 5"), ("chorus2", "chorus", 16, "4 5 3m 6m"),
                        ("bridge", "bridge", 16, "6m 5 4 4"), ("chorus3", "chorus", 16, "4 5 3m 6m"), ("outro", "outro", 8, "1 5 1")]),
     rhythm={"tone": "loud-mid-hs", "intro": ["X===X===X=x=X===", "X===X===x=x=x=x="], "verse": ["X-x-x-x-X-x-x-x-", "X-x-x-x-X-x-x-3-"], "pre": "X=x=X=x=X=x=X=x=",
             "chorus": ["X=====x=x=x=X===", "X=====x=x=x=x=x="], "inter": "X-x-x-x-5-x-x-x-", "bridge": "-", "outro": "X==============="},
     lead={"tone": "warm-lead-a", "sections": {"chorus1,chorus2,chorus3": {"lo": "B4", "hi": "C6", "rhythm": L([1, 0.5, 0.5, 1, 1], [1, 1, 2], [0.5, 0.5, 0.5, 0.5, 1, 1], [3, 1]), "peak": 5},
                                               "inter": {"lo": "D5", "hi": "D6", "rhythm": L([0.5] * 8, [2, 2])}}},
     bass={"intro": "R:0.5! R:0.5 8:0.5 R:0.5 R:0.5 5:0.5 3:0.5 b:0.5", "verse": ["R:0.5! R:0.5 R:0.5 8:0.5' R:0.5 R:0.5 5:0.5 R:0.5", "R:0.5! R:0.5 3:0.5 5:0.5 8:0.5 5:0.5 3:0.5 b:0.5"],
           "verse_b": ["R:0.5! 8:0.5' R:0.5 8:0.5' 5:0.5 R:0.5 3:0.5 R:0.5", "9:0.5 8:0.5 7:0.5 5:0.5 3:0.5 4:0.5 5:0.5 b:0.5"],
           "pre": ["R:0.5! R:0.5 R:0.5 R:0.5 3:0.5 3:0.5 5:0.5 5:0.5", "8:1! 7:1 5:1 b:1"], "chorus": ["R:1! 5:0.5 8:0.5 7:0.5 8:0.5 5:0.5 3:0.5", "R:0.5! 3:0.5 5:1 8:1 b:1"],
           "inter": "R:0.5! 8:0.5' R:0.5 8:0.5' 5:0.5 8:0.5' 7:0.5 b:0.5", "bridge": ["R:4!", "5:4", "3:2 5:2", "8:2 b:2"], "outro": ["R:4!", "5:4", "R:4!", "-:4"]},
     drums=std(16, "drive"), extras={"piano": {"arp": "intro,bridge", "chords": "chorus,pre", "soft": "verse", "chordRhythm": [1, 1, 1, 1]}}, modulate=2)

# ════════ 10. 凍土のレクイエム（遅く重い・合唱と弦の合奏）════════
song(no=10, slug="todo-requiem", title="凍土のレクイエム", seed=1010, bpm=88, key="C#", mode="phrygian", tuning="C#2",
     desc="凍った大地をゆっくり踏みしめる重いラウドメタル。C#フリジアン・ドロップC#・合唱と弦の合奏",
     form=form(88, 4, [("intro", "intro", 6, "1m 2"), ("verse1", "verse", 12, "1m 1m 2 1m"), ("pre1", "pre", 4, "6 7"), ("chorus1", "chorus", 10, "6 3 7 1m"),
                       ("verse2", "verse", 10, "1m 1m 2 1m"), ("chorus2", "chorus", 10, "6 3 7 1m"), ("bridge", "bridge", 8, "4m 6"), ("solo", "solo", 8, "1m 6 7 1m"),
                       ("chorus3", "chorus", 10, "6 3 7 1m"), ("outro", "outro", 4, "1m")]),
     rhythm={"tone": "loud-high", "intro": "-", "verse": ["X=======X===x=x=", "X=======b=======", "X=======X===x===", "X===2===X===b==="], "pre": "X===============",
             "chorus": ["X=======X=======", "X=======X===x=x="], "bridge": "-", "solo": "X===x=x=X===x=x=", "outro": "X==============="},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "G#4", "hi": "G#5", "rhythm": L([2, 2], [3, 1], [1, 1, 2], [4]), "peak": 3}}},
     tech={"solo": "mmmmmmmm"},
     bass={"intro": "-:4", "verse": ["R:2! R:1 5:1", "b:2 R:2", "R:2! 8:1 7:1", "9:2 b:2"], "pre": ["R:4!", "5:2 b:2"], "chorus": ["R:2! 8:2", "7:2 5:1 b:1"],
           "bridge": ["8:4!", "7:2 b:2"], "solo": "R:1! 5:1 8:1 b:1", "outro": "R:4!"},
     drums={**std(16, "halftime"), "verse": {"k": ["X.......X.X.....", "X.....X.X......."], "s": "........X.......", "c": "r...r...r...r...", "fill": "tom"}},
     extras={"choir": "intro,chorus,outro", "strings": {"pad": "intro,bridge,chorus", "cello": "bridge", "celloMotif": ["R:4", "5:2 b:2"]}}, riserTo=["chorus"])

# ════════ 11. 逆光アクセル（Jロック寄りの疾走・長調・旋律が先に来る）════════
song(no=11, slug="gyakko-accel", title="逆光アクセル", seed=1111, bpm=200, key="A", mode="ionian", tuning="E2",
     desc="逆光の中を加速する、歌うような長調のラウドロック。Aメジャー・標準チューニング・ピアノ",
     form=form(200, 4, [("intro", "intro", 8, "4 5 3m 6m"), ("verse1", "verse", 16, "1 5 6m 3m 4 1 2m 5"), ("pre1", "pre", 8, "4 5 6m 6m"),
                        ("chorus1", "chorus", 16, "4 5 3m 6m 2m 5 1 1"), ("inter", "interlude", 8, "1 5 6m 4"), ("verse2", "verse", 16, "1 5 6m 3m 4 1 2m 5"),
                        ("pre2", "pre", 8, "4 5 6m 6m"), ("chorus2", "chorus", 16, "4 5 3m 6m 2m 5 1 1"), ("bridge", "bridge", 16, "6m 3m 4 5"),
                        ("solo", "solo", 16, "1 5 6m 4"), ("chorus3", "chorus", 16, "4 5 3m 6m 2m 5 1 1"), ("outro", "outro", 8, "4 5 1")]),
     rhythm={"tone": "jpop-rock-drive", "intro": "X=x=x=x=X=x=x=x=", "verse": ["X-x-x-x-x-x-x-x-", "X-x-x-x-X===x-x-"], "pre": "X=x=X=x=X=x=X=x=", "chorus": ["X=====x=x=x=X===", "X===x===x=x=x=x="],
             "inter": "X=x=x=x=X=x=x=x=", "bridge": "-", "solo": "X-x-x-x-X-x-x-x-", "outro": "X==============="},
     lead={"tone": "warm-lead-a", "sections": {"intro": {"lo": "C#5", "hi": "C#6", "rhythm": L([1, 0.5, 0.5, 1, 1], [2, 2])},
                                               "chorus1,chorus2,chorus3": {"lo": "C#5", "hi": "D6", "rhythm": L([0.5, 0.5, 1, 1, 1], [1.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2], [3, 1]), "peak": 5},
                                               "inter": {"lo": "E5", "hi": "E6", "rhythm": L([0.5] * 8, [1, 1, 2])}}},
     tech={"solo": "mmmmsmmmmmmmmm--"},
     bass={"intro": "R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 5:0.5 b:0.5", "verse": ["R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5", "R:0.5! R:0.5 R:0.5 8:0.5' R:0.5 5:0.5 3:0.5 b:0.5"],
           "verse_b": ["R:0.5! 8:0.5' R:0.5 8:0.5' R:0.5 5:0.5 R:0.5 3:0.5", "R:0.5! 3:0.5 5:0.5 8:0.5 9:0.5 8:0.5 7:0.5 b:0.5"], "pre": ["R:0.5! R:0.5 R:0.5 R:0.5 5:0.5 5:0.5 8:0.5 8:0.5", "8:1! 7:1 5:1 b:1"],
           "chorus": ["R:1! R:0.5 5:0.5 8:0.5 7:0.5 5:0.5 3:0.5", "R:0.5! R:0.5 3:0.5 5:0.5 8:1 b:1"], "inter": "R:0.5! 8:0.5' R:0.5 8:0.5' 5:0.5 8:0.5' 3:0.5 b:0.5",
           "bridge": ["R:2! 5:2", "3:2 b:2"], "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 3:0.5 b:0.5", "outro": ["R:4!", "R:4", "R:4!"]},
     drums=std(16, "drive"), extras={"piano": {"arp": "intro,bridge,outro", "chords": "chorus,inter", "soft": "verse,pre", "chordRhythm": [0.5, 1, 0.5, 1, 1]}}, modulate=1)

# ════════ 12. 深海エンジン（ジェント・5つずつ回るリフ・ガラスのシンセ）════════
song(no=12, slug="shinkai-engine", title="深海エンジン", seed=1212, bpm=120, key="D", mode="phrygian", tuning="D2",
     desc="5つずつ回るリフが4拍子の上でずれていく深海のジェント。Dフリジアン・ドロップD・ガラスのシンセ",
     form=form(120, 4, [("intro", "intro", 8, "1m"), ("verse1", "verse", 16, "1m 1m 2 2"), ("chorus1", "chorus", 12, "6 7 4m 1m"), ("inter", "interlude", 8, "1m 2"),
                        ("verse2", "verse", 16, "1m 1m 2 2"), ("chorus2", "chorus", 12, "6 7 4m 1m"), ("bridge", "bridge", 12, "6maj7 7"), ("break", "break", 12, "1m 2"),
                        ("chorus3", "chorus", 12, "6 7 4m 1m"), ("outro", "outro", 6, "1m")]),
     rhythm={"tone": "djent-8", "noPower": True, "intro": "-", "verse": ["X-x-xX-x-xX-x-xX", "-x-xX-x-xX-x-xX-", "x-xX-x-xX-x-xX-x", "-xX-x-xX-x-xX-x-"], "chorus": ["X=====x=X=====x=", "X===x===X===x=x="],
             "inter": ["X-x-xX-x-xX-x-xX", "-x-xX-x-xX-x-x2-"], "bridge": "-", "break": ["X--x--x-X--x--x-", "X-x-x-X-x-xX--X-"], "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "A4", "hi": "A5", "rhythm": L([3, 1], [2, 1, 1], [2, 2], [4])},
                                             "bridge": {"lo": "D5", "hi": "D6", "rhythm": L([4], [2, 2], [3, 1], [4])}}},
     tech={"inter": "tttttttt"},
     bass={"intro": ["R:4!", "-:4"], "verse": ["R:0.5! -:0.25 R:0.25 -:0.25 R:0.5! -:0.25 R:0.25 -:0.25 R:0.5! -:0.25 R:0.25 -:0.25 R:0.25", "-:0.25 R:0.25 -:0.25 R:0.5! -:0.25 R:0.25 -:0.25 R:0.5! -:0.25 R:0.25 -:0.25 9:0.5 b:0.25"],
           "chorus": ["R:3! 5:1", "8:2 7:1 b:1"], "inter": "R:1! 5:0.5 8:0.5 R:1 9:0.5 b:0.5", "bridge": ["8:4!", "7:2 5:1 b:1"],
           "break": ["R:0.75! -:0.5 R:0.75 R:0.75 -:0.5 R:0.75", "R:0.5! -:0.5 R:0.5 R:0.5 -:0.5 R:0.75 -:0.25 b:0.5"], "outro": ["R:4!", "-:4"]},
     drums={**std(16, "djent"), "verse": {"k": "sync", "s": "........X.......", "c": ["u...u...u...u...", "u...u...u...n..."], "fill": "kick"}},
     extras={"synth": {"pluck": "intro,bridge,outro", "pluckPatch": "glassPluck", "wall": "chorus"}}, riserTo=["chorus", "break"])

# ════════ 13. 紅蓮スタンピード（スラッシュ寄りの速さ・楽器はバンドだけ）════════
song(no=13, slug="guren-stampede", title="紅蓮スタンピード", seed=1313, bpm=210, key="E", mode="aeolian", tuning="E2",
     desc="燃える群れが駆け抜ける、いちばん速いスラッシュ寄りのラウドメタル。Eマイナー・標準・バンドだけ",
     form=form(210, 4, [("intro", "intro", 8, "1m 1m b2 1m"), ("verse1", "verse", 16, "1m 1m 6 7"), ("pre1", "pre", 8, "4m 4m 5m 5m"), ("chorus1", "chorus", 16, "6 7 1m 1m"),
                        ("verse2", "verse", 16, "1m 1m 6 7"), ("chorus2", "chorus", 16, "6 7 1m 1m"), ("solo", "solo", 24, "1m 6 7 1m"), ("break", "break", 12, "1m b2"),
                        ("chorus3", "chorus", 16, "6 7 1m 1m"), ("outro", "outro", 8, "1m b2 1m")]),
     rhythm={"tone": "loud-high", "pm": ["verse"], "intro": ["xxxxxxxxX===X===", "xxxxxxxxX=b=X==="], "verse": ["mmmmmmmmmmmmmmmm", "mmmmmmmmm-m-X==="], "pre": "X=x=X=x=X=x=X=x=",
             "chorus": ["X=x=x=x=X=x=x=x=", "X=x=x=x=X=======",], "solo": "x-x-x-x-x-x-x-x-", "break": ["X---X---X-X-X---", "X---X---XbXbXbX-"], "outro": ["X===X===X===X===", "X==============="]},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "B4", "hi": "C6", "rhythm": L([1, 1, 1, 1], [2, 2], [1, 0.5, 0.5, 2], [4]), "peak": 2}}},
     tech={"solo": "mmmmmmmmsssmmmmmtttt----"},
     bass={"intro": "R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:1! R:1", "verse": ["R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25", "R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.5 3:0.5 5:0.5 b:0.5"],
           "pre": ["R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5", "5:0.5 5:0.5 8:0.5 8:0.5 7:0.5 7:0.5 b:0.5 b:0.5"], "chorus": ["R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 8:0.5 R:0.5 5:0.5", "R:0.5! 3:0.5 5:0.5 8:0.5 7:1 b:1"],
           "solo": "R:0.5! R:0.5 R:0.5 8:0.5' R:0.5 R:0.5 5:0.5 b:0.5", "break": ["R:1! R:1 R:0.5 R:0.5 R:1", "R:1! R:1 b:0.5 R:0.5 b:1"], "outro": ["R:1! R:1 R:1 R:1", "R:4!"]},
     drums={**std(16, "drive"), "verse": {"k": "X.x.X.x.X.x.X.x.", "s": ["....X.......X...", "....X.......X..."], "h": "x.x.x.x.x.x.x.x.", "fill": "snare"},
            "chorus": {"k": ["X.x.X.x.X.x.X.x.", "X.x.X.x.X.x.X.x.", "X.X.X.X.X.X.X.X.", "X.x.X.x.X...XXXX"], "s": ["..X...X...X...X.", "..X...X...X...X.", ".X.X.X.X.X.X.X.X", "....X.......X..."], "c": "r.r.r.r.r.r.r.r.", "fill": "tom"}}, riser=False)

# ════════ 14. 月影ワルツ（3/4・和声的短音階・バイオリンが主役）════════
song(no=14, slug="tsukikage-waltz", title="月影ワルツ", seed=1414, bpm=180, beats=3, key="D", mode="harmonic", tuning="D2",
     desc="月の影で踊る3拍子のラウドメタル。Dの和声的短音階・ドロップD・バイオリンが主役",
     form=form(180, 3, [("intro", "intro", 8, "1m 1m 5 5"), ("verse1", "verse", 16, "1m 6 4m 5"), ("pre1", "pre", 8, "4m 4m 5 5"), ("chorus1", "chorus", 16, "1m 3aug 6 5"),
                        ("inter", "interlude", 8, "1m 5"), ("verse2", "verse", 16, "1m 6 4m 5"), ("chorus2", "chorus", 16, "1m 3aug 6 5"), ("bridge", "bridge", 16, "6 2m 5 1m"),
                        ("solo", "solo", 16, "1m 6 4m 5"), ("chorus3", "chorus", 16, "1m 3aug 6 5"), ("outro", "outro", 8, "1m 5 1m")], unit=4),
     rhythm={"tone": "marshall-mid", "pm": ["verse"], "intro": "-", "verse": ["m-m-m-X=====", "m-m-m-X===x="], "pre": "X=====X=====", "chorus": ["X===x=x=x=x=", "X===========",],
             "inter": "X===x=x=5=x=", "bridge": "-", "solo": "X-x-x-X-x-x-", "outro": "X==========="},
     lead={"tone": "warm-lead-b", "sections": {"intro": {"inst": "violin", "lo": "D5", "hi": "A5", "rhythm": L([2, 1], [1, 1, 1], [2, 1], [3])},
                                               "chorus1,chorus2,chorus3": {"inst": "violin", "lo": "A4", "hi": "D6", "rhythm": L([1.5, 0.5, 1], [2, 1], [1, 1, 1], [3]), "peak": 5},
                                               "inter": {"lo": "D5", "hi": "D6", "rhythm": L([0.5] * 6, [1, 1, 1], [0.5] * 6, [3])},
                                               "bridge": {"inst": "violin", "lo": "F4", "hi": "F5", "rhythm": L([3], [2, 1], [3], [3])}}},
     tech={"solo": "mmmmmmmmssssmmmm"},
     bass={"intro": ["R:3!", "5:3"], "verse": ["R:1! 5:1 8:1", "R:1! 3:1 5:1", "R:1! 5:1 8:1", "7:1 5:1 b:1"], "pre": ["R:2! 5:1", "8:2 b:1"], "chorus": ["R:1! 5:0.5 8:0.5 7:1", "3:1 5:1 b:1"],
           "inter": "R:1! 3:0.5 5:0.5 8:0.5 b:0.5", "bridge": ["8:3!", "7:2 5:1", "3:3", "b:3"], "solo": "R:1! 5:1 8:0.5 b:0.5", "outro": ["R:3!", "5:3", "R:3!", "-:3"]},
     drums=generic(12, 4, [3], "waltz"), extras={"strings": {"cello": "intro,bridge,verse", "celloMotif": ["R:3", "5:2 b:1"], "pad": "chorus,bridge"}}, modulate=1)

# ════════ 15. 硝子の飛行機雲（明るいリディアン・ピアノとシンセを少し）════════
song(no=15, slug="garasu-hikokigumo", title="硝子の飛行機雲", seed=1515, bpm=165, key="E", mode="lydian", tuning="E2",
     desc="ガラスのように透ける空と飛行機雲。浮き上がる響きのEリディアン・標準・ピアノとシンセ",
     form=form(165, 4, [("intro", "intro", 8, "1 2 1 2"), ("verse1", "verse", 16, "1 2 6m 7m"), ("pre1", "pre", 8, "5 6m 2 2"),
                        ("chorus1", "chorus", 16, "6m 5 2 1"), ("inter", "interlude", 8, "1 2"), ("verse2", "verse", 16, "1 2 6m 7m"), ("chorus2", "chorus", 16, "6m 5 2 1"),
                        ("bridge", "bridge", 16, "3m 6m 2 2"), ("solo", "solo", 12, "1 2 6m 5"), ("chorus3", "chorus", 16, "6m 5 2 1"), ("outro", "outro", 8, "1 2 1")]),
     rhythm={"tone": "electro-rock", "intro": "-", "verse": ["X===x-x-X===x-x-", "X===x-x-X-x-x-x-"], "pre": "X===X===X===X===", "chorus": ["X=====x=x=x=X===", "X=====x=X=====x="],
             "inter": "X===x-x-X===x-4-", "bridge": "-", "solo": "X-x-x-x-X-x-x-x-", "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "B4", "hi": "C#6", "rhythm": L([2, 1, 1], [1.5, 0.5, 2], [1, 1, 1, 1], [4]), "peak": 4},
                                             "inter": {"lo": "E5", "hi": "E6", "rhythm": L([1, 1, 1, 1], [4])}}},
     tech={"solo": "mmmmsmmmttt-"},
     bass={"intro": ["R:4!", "R:4"], "verse": ["R:1! R:0.5 5:0.5 8:1 7:0.5 5:0.5", "R:0.5! R:0.5 3:0.5 5:0.5 8:1 b:1"], "verse_b": ["R:1! 8:0.5 7:0.5 5:1 3:0.5 b:0.5", "R:0.5! 9:0.5 3:0.5 5:0.5 8:0.5 7:0.5 5:0.5 b:0.5"],
           "pre": ["R:1! 5:1 8:1 9:1", "8:1 7:1 5:1 b:1"], "chorus": ["R:1.5! 5:0.5 8:1 7:1", "5:1 3:1 9:1 b:1"], "inter": "R:1! 5:0.5 8:0.5 9:1 b:1", "bridge": ["8:2! 7:2", "5:2 b:2"],
           "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 3:0.5 b:0.5", "outro": ["R:4!", "R:4", "R:4!"]},
     drums=std(16, "metalcore"), extras={"piano": {"arp": "intro,verse,bridge,outro", "chords": "", "arpRate": 0.5}, "synth": {"wall": "chorus"}})

# ════════ 16. 黒鉄の行進（グルーヴ・ドリアン・バンドだけ・ベースから始まる）════════
song(no=16, slug="kurogane-koushin", title="黒鉄の行進", seed=1616, bpm=104, key="F#", mode="dorian", tuning="F#1",
     desc="重い鉄の足どりで進むグルーヴ・メタル。F#ドリアン・低いF#・ベースから始まる",
     form=form(104, 4, [("intro", "intro", 8, "1m"), ("verse1", "verse", 16, "1m 1m 4 4"), ("pre1", "pre", 6, "3 4"), ("chorus1", "chorus", 12, "1m 7 4 4"),
                        ("verse2", "verse", 12, "1m 1m 4 4"), ("chorus2", "chorus", 12, "1m 7 4 4"), ("break", "break", 10, "1m"), ("solo", "solo", 12, "1m 4 7 1m"),
                        ("chorus3", "chorus", 12, "1m 7 4 4"), ("outro", "outro", 4, "1m")]),
     rhythm={"tone": "nu-metal-wall", "intro": ["-", "-", "X-x--x-xX--3-x--", "X-x--x-xX--3-5-4"], "verse": ["X-x--x-xX--3-x--", "X-x--x-xX--3-5-4"], "pre": "X=======X=======",
             "chorus": ["X===x=x=X=====x=", "X===x=x=X===x=x="], "break": ["X--X--X-X--X----", "X--X--X-X--Xb-X-"], "solo": "X-x--x-xX--3-x--", "outro": "X==============="},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "A4", "hi": "A5", "rhythm": L([1, 1, 2], [0.5, 0.5, 1, 2], [1, 1, 1, 1], [3, 1])}}},
     tech={"solo": "mmmmmmmmmmmm"},
     bass={"intro": ["R:0.5! 8:0.25' R:0.25, -:0.5 R:0.5 -:0.25 3:0.25 4:0.5 5:0.5 b:0.5", "R:0.5! 8:0.25' R:0.25, -:0.5 R:0.5 7:0.5 5:0.5 4:0.5 3:0.5"],
           "verse": ["R:0.5! 8:0.25' R:0.25, -:0.5 R:0.5 -:0.25 3:0.25 4:0.5 5:0.5 b:0.5", "R:0.5! 8:0.25' R:0.25, -:0.5 R:0.5 7:0.5 5:0.5 4:0.5 3:0.5"],
           "pre": ["R:2! 5:2", "8:2 b:2"], "chorus": ["R:1.5! R:0.5 8:0.5 7:0.5 5:1", "3:0.5 4:0.5 5:1 7:1 b:1"], "break": ["R:0.75! -:0.25 R:0.5 R:0.75 -:0.25 R:0.5 -:1", "R:0.75! -:0.25 R:0.5 R:0.75 -:0.25 R:0.5 b:0.5 R:0.5"],
           "solo": "R:0.5! 8:0.25' R:0.25, 5:0.5 R:0.5 7:0.5 5:0.5 3:0.5 b:0.5", "outro": "R:4!"},
     drums={**std(16, "nu"), "intro": {"k": ["................", "................", "X..X..X.X......X", "X..X..X.X..X...."], "s": ["................", "................", "....X..o....X.o.", "....X..o....X.XX"], "h": ["x...x...x...x...", "x...x...x...x...", "x.xxx.x.x.xxx.x.", "x.xxx.x.x.xxx.x."], "crash": False, "fill": "snare"}}, riser=False)

# ════════ 17. 雷鳥コーリング（メタルコア・全弦開放のG#で始まる・合唱）════════
song(no=17, slug="raicho-calling", title="雷鳥コーリング", seed=1717, bpm=150, key="G#", mode="aeolian", tuning="G#1",
     desc="雷鳥が呼ぶ山の頂のメタルコア。G#マイナー・低いG#・全弦開放の響きで始まり、合唱が広がる",
     form=form(150, 4, [("open", "intro", 4, "1m"), ("intro", "intro", 6, "1m 6"), ("verse1", "verse", 16, "1m 1m 7 6"), ("pre1", "pre", 8, "4m 5m 6 7"),
                        ("chorus1", "chorus", 16, "6 3 7 1m"), ("verse2", "verse", 16, "1m 1m 7 6"), ("pre2", "pre", 8, "4m 5m 6 7"), ("chorus2", "chorus", 16, "6 3 7 1m"),
                        ("break", "break", 16, "1m 2dim 1m 7"), ("chorus3", "chorus", 16, "6 3 7 1m"), ("outro", "outro", 6, "1m")]),
     rhythm={"tone": "modern-metalcore", "pm": ["verse"], "open": "-", "intro": "X=====x=X=====x=", "verse": ["mm-mm-m-mm-mm-m-", "mm-mm-m-m-m-X==="], "pre": "X===X===X=x=X===",
             "chorus": ["X=======x=x=X===", "X=======X=x=x=x="], "break": ["X--X--X-X--X--X-", "X--X--X---X-X-X-", "X--X--X-X--X--X-", "XXX-XXX-XX-XXX--"], "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"chorus1,chorus2,chorus3": {"lo": "D#5", "hi": "D#6", "rhythm": L([1.5, 0.5, 2], [1, 1, 1, 1], [3, 1], [4]), "peak": 4}}},
     bass={"open": "-:4", "intro": ["R:2! 8:1 7:1", "5:2 b:2"], "verse": ["R:0.25! R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 R:0.5 R:0.25 R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 8:0.5", "R:0.25! R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 R:0.5 3:0.5 5:0.5 8:1"],
           "verse_b": ["R:0.25! R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 R:0.5 5:0.5 8:0.5 9:0.5 8:0.5", "8:1! 7:0.5 5:0.5 3:1 b:1"], "pre": ["R:1! 5:1 8:1 5:1", "8:1 9:1 8:1 b:1"],
           "chorus": ["R:2! 5:1 8:1", "9:1 8:1 7:1 b:1"], "break": ["R:0.75! -:0.5 R:0.75 -:0.5 R:0.5 -:0.5 R:0.5", "R:0.75! -:0.5 R:0.75 -:0.25 b:0.25 R:0.5 b:0.5 R:0.5"], "outro": ["R:4!", "-:4"]},
     drums={**std(16, "metalcore"), "open": {"k": ["X...............", "................"], "c": ["c...............", "................"], "crash": False, "nofill": True}},
     extras={"choir": "chorus,outro", "open": ["G#1", "D#2", "G#2", "C#3", "F3", "A#3"]}, riserTo=["intro", "chorus", "break"])

# ════════ 18. 蒼いネガフィルム（オルタナ寄り・ハーフタイム・チェロが歌う）════════
song(no=18, slug="aoi-negafilm", title="蒼いネガフィルム", seed=1818, bpm=110, key="C#", mode="dorian", tuning="C#2",
     desc="色の反転した記憶を歩く、オルタナ寄りのラウドロック。C#ドリアン・ドロップC#・チェロが歌う",
     form=form(110, 4, [("intro", "intro", 6, "1m 4"), ("verse1", "verse", 12, "1m 4 1m 4"), ("pre1", "pre", 6, "3 7"), ("chorus1", "chorus", 12, "2m 3 7 4"),
                        ("verse2", "verse", 12, "1m 4 1m 4"), ("chorus2", "chorus", 12, "2m 3 7 4"), ("bridge", "bridge", 12, "4 4 1m 1m"), ("chorus3", "chorus", 12, "2m 3 7 4"), ("outro", "outro", 6, "1m 4")]),
     rhythm={"tone": "loud-mid-noise", "intro": "-", "verse": ["X=======--------", "X===x===--------"], "pre": "X===x=x=X===x=x=", "chorus": ["X=======X=======", "X===x===X===x=x="],
             "bridge": ["-", "-", "-", "-", "X===============", "X===============", "X===x===X===x===", "X=x=X=x=X=x=X=x="], "outro": ["X===============", "-"]},
     lead={"tone": "warm-lead-a", "sections": {"intro,verse1,verse2": {"inst": "cello", "lo": "C#3", "hi": "E4", "rhythm": L([1.5, 0.5, 2], [2, 1, 1], [3, 1], [4])},
                                               "chorus1,chorus2,chorus3": {"lo": "G#4", "hi": "G#5", "rhythm": L([1, 1, 2], [2, 2], [1, 0.5, 0.5, 2], [4]), "peak": 3}}},
     bass={"intro": ["-:4", "-:4", "R:4!", "5:2 b:2"], "verse": ["R:1.5! 5:0.5 8:1 7:1", "5:1 4:1 3:1 b:1"], "pre": ["R:1! 5:1 8:1 9:1", "8:1 7:1 5:1 b:1"],
           "chorus": ["R:1! R:1 8:1 5:1", "9:1 8:1 5:1 b:1"], "bridge": ["8:3! 7:1", "5:3 b:1"], "outro": ["R:4!", "-:4"]},
     drums={**std(16, "halftime"), "bridge": {"k": ["X...............", "................", "X...............", "........X.......", "X.......X.......", "X.......X.......", "X...X...X...X...", "X.X.X.X.X.X.X.X."],
                                             "s": ["................", "................", "................", "............o.o.", "........X.......", "........X.......", "....X.......X...", "....X...X.X.XXXX"], "c": "r...r...r...r...", "crash": False, "fill": "snare"}},
     extras={"strings": {"cello": "bridge,outro", "celloMotif": ["R:2 5:1 8:1", "7:2 5:1 b:1", "3:2 5:2", "8:1 7:1 5:1 b:1"], "pad": "chorus"}}, riserTo=["chorus"])

# ════════ 19. 電脳カーニバル（エレクトロ・メタル・お祭り・シンセが旋律）════════
song(no=19, slug="denno-carnival", title="電脳カーニバル", seed=1919, bpm=140, key="A", mode="dorian", tuning="A1",
     desc="電子の街のお祭り騒ぎ。跳ねるエレクトロ・メタル。Aドリアン・ドロップA・シンセが旋律、加工ギター",
     form=form(140, 4, [("intro", "intro", 8, "1m 4 1m 4"), ("verse1", "verse", 16, "1m 1m 4 7"), ("pre1", "pre", 8, "3 4 5m 4"), ("chorus1", "chorus", 16, "1m 7 3 4"),
                        ("inter", "interlude", 8, "1m 4"), ("verse2", "verse", 16, "1m 1m 4 7"), ("chorus2", "chorus", 16, "1m 7 3 4"), ("break", "break", 12, "1m 7"),
                        ("chorus3", "chorus", 16, "1m 7 3 4"), ("outro", "outro", 8, "1m 4 1m")]),
     rhythm={"tone": "electro-rock", "intro": "-", "verse": ["X--x--X-X--x-4-5", "X--x--X-X-x-x---"], "pre": "X=x=X=x=X=x=X=x=", "chorus": ["X===x=x=X===x=x=", "X===x=x=X=x=x=x="],
             "inter": "X--x--X-X--x-4-5", "break": ["X--X--X-----X---", "X--X--X---XbXbXb"], "outro": ["X===============", "-"]},
     lead={"tone": "bmth-lead", "sections": {"intro,inter": {"inst": "synth", "lo": "E5", "hi": "E6", "rhythm": L([0.5, 0.5, 0.5, 0.5, 1, 1], [0.5] * 8, [1, 0.5, 0.5, 2], [4])},
                                             "chorus1,chorus2,chorus3": {"inst": "synth", "lo": "C5", "hi": "D6", "rhythm": L([1, 0.5, 0.5, 1, 1], [0.5, 0.5, 1, 2], [1, 1, 1, 1], [3, 1]), "peak": 5}}},
     bass={"intro": ["R:0.5! -:0.5 8:0.5 -:0.5 R:0.5 -:0.5 8:0.5 -:0.5"], "verse": ["R:0.5! -:0.5 8:0.5' R:0.5 -:0.5 R:0.5 8:0.5' 5:0.5", "R:0.5! -:0.5 8:0.5' R:0.5 3:0.5 4:0.5 5:0.5 b:0.5"],
           "verse_b": ["R:0.5! 8:0.5' R:0.5 8:0.5' 7:0.5 8:0.5' 5:0.5 8:0.5'", "R:0.5! 9:0.5 3:0.5 4:0.5 5:0.5 7:0.5 8:0.5 b:0.5"], "pre": ["R:1! 5:1 8:1 5:1", "7:1 8:1 9:1 b:1"],
           "chorus": ["R:0.5! 8:0.5 R:0.5 8:0.5 R:0.5 8:0.5 7:0.5 5:0.5", "R:0.5! 8:0.5 R:0.5 8:0.5 3:0.5 4:0.5 5:0.5 b:0.5"], "inter": "R:0.5! -:0.5 8:0.5' R:0.5 -:0.5 R:0.5 8:0.5' b:0.5",
           "break": ["R:0.75! -:0.25 R:0.5 -:0.5 R:2", "R:0.75! -:0.25 R:0.5 -:0.5 b:0.5 R:0.5 b:0.5 R:0.5"], "outro": ["R:0.5! -:0.5 8:0.5 -:0.5 R:0.5 -:0.5 8:0.5 -:0.5", "R:4!", "-:4"]},
     drums={**std(16, "industrial"), "chorus": {"k": ["X...X...X...X...", "X...X...X...X..X"], "s": "....X.......X...", "h": "..x...x...x...x.", "c": ["c...............", "................"], "fill": "snare"}},
     extras={"gated": "verse,break", "synth": {"wall": "chorus,pre", "pluck": "intro,verse,outro", "pluckPatch": "glassPluck"}}, riserTo=["chorus", "break"])

# ════════ 20. 砂嵐の預言者（フリジアン・ドミナント・バイオリンの異国の旋律）════════
song(no=20, slug="sunaarashi-yogensha", title="砂嵐の預言者", seed=2020, bpm=160, key="E", mode="phrygdom", tuning="E2",
     desc="砂嵐の向こうで告げる預言者。異国の音階（Eフリジアン・ドミナント）のラウドメタル。バイオリンが旋律",
     form=form(160, 4, [("intro", "intro", 8, "1 1 2 1"), ("verse1", "verse", 16, "1 1 2 1"), ("pre1", "pre", 8, "4m 4m 2 2"), ("chorus1", "chorus", 16, "4m 2 1 1"),
                        ("inter", "interlude", 8, "1 2"), ("verse2", "verse", 16, "1 1 2 1"), ("chorus2", "chorus", 16, "4m 2 1 1"), ("bridge", "bridge", 12, "6 7m"),
                        ("solo", "solo", 16, "1 2 4m 1"), ("chorus3", "chorus", 16, "4m 2 1 1"), ("outro", "outro", 8, "1 2 1")]),
     rhythm={"tone": "loud-high", "pm": ["verse"], "intro": "-", "verse": ["m-mm-mbm-mm-m3m-", "m-mm-mbm-mm-X==="], "pre": "X===x=x=X===x=x=", "chorus": ["X=====x=X=====x=", "X===x===X=x=b=X="],
             "inter": "X-xbX-x3X-xbX-5-", "bridge": "-", "solo": "X-xbX-x-X-xbX-x-", "outro": "X==============="},
     lead={"tone": "bmth-lead", "sections": {"intro,inter": {"inst": "violin", "lo": "E5", "hi": "E6", "rhythm": L([1, 0.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2], [1, 1, 2], [4])},
                                             "chorus1,chorus2,chorus3": {"inst": "violin", "lo": "G#4", "hi": "B5", "rhythm": L([1.5, 0.5, 1, 1], [2, 2], [1, 0.5, 0.5, 2], [4]), "peak": 5},
                                             "bridge": {"lo": "E5", "hi": "E6", "rhythm": L([4], [2, 2], [3, 1], [4])}}},
     tech={"solo": "mmmmmmssmmmmtttt"},
     bass={"intro": ["R:4!", "R:2 b:2"], "verse": ["R:0.5! -:0.5 R:0.25 R:0.25 -:0.5 R:0.5 -:0.5 R:0.5 3:0.5", "R:0.5! -:0.5 R:0.25 R:0.25 -:0.5 4:0.5 5:0.5 3:0.5 b:0.5"],
           "verse_b": ["R:0.5! 3:0.5 4:0.5 5:0.5 R:0.5 3:0.5 9:0.5 R:0.5", "8:1! 7:0.5 5:0.5 4:0.5 3:0.5 9:0.5 b:0.5"], "pre": ["R:1! R:1 5:1 8:1", "9:1 8:1 7:1 b:1"],
           "chorus": ["R:1.5! 5:0.5 8:1 7:1", "3:1 4:1 5:1 b:1"], "inter": "R:0.5! 9:0.5 R:0.5 3:0.5 R:0.5 9:0.5 R:0.5 b:0.5", "bridge": ["8:2! 7:2", "5:2 b:2"],
           "solo": "R:0.5! R:0.5 9:0.5 R:0.5 3:0.5 R:0.5 5:0.5 b:0.5", "outro": ["R:4!", "R:2 b:2", "R:4!"]},
     drums=std(16, "metalcore"), extras={"strings": {"cello": "intro,bridge", "celloMotif": ["R:2 9:2", "3:2 b:2"], "pad": "chorus"}})

# ════════ 21. メテオ・スプリント（いちばん速い・ブラストとハーフタイムの切りかえ）════════
song(no=21, slug="meteor-sprint", title="メテオ・スプリント", seed=2121, bpm=220, key="C", mode="aeolian", tuning="C2",
     desc="流星のように駆け抜ける。ブラストビートとハーフタイムが入れかわるラウドメタル。Cマイナー・ドロップC",
     form=form(220, 4, [("intro", "intro", 8, "1m b2 1m b2"), ("verse1", "verse", 16, "1m 1m 6 7"), ("chorus1", "chorus", 16, "6 7 3 5"), ("verse2", "verse", 16, "1m 1m 6 7"),
                        ("chorus2", "chorus", 16, "6 7 3 5"), ("break", "break", 16, "1m b2"), ("solo", "solo", 24, "1m 6 3 7"), ("chorus3", "chorus", 16, "6 7 3 5"), ("outro", "outro", 8, "1m b2 1m")]),
     rhythm={"tone": "loud-high", "intro": ["XXXXXXXXX===X===", "XXXXXXXXX=b=X==="], "verse": ["X-x-x-x-X-x-x-x-", "X-x-x-x-b-x-b-x-"], "chorus": ["X=======X=======", "X===x===X===x==="],
             "break": ["X---------X-----", "X-----X---X-b-X-"], "solo": "x-x-x-x-x-x-x-x-", "outro": ["X===X===X===X===", "X==============="]},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "C5", "hi": "D6", "rhythm": L([2, 2], [3, 1], [2, 1, 1], [4]), "peak": 2}}},
     tech={"solo": "mmmmmmmmssssmmmmtttttt--"},
     bass={"intro": "R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:0.25 R:1! R:1", "verse": ["R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5", "R:0.5! R:0.5 R:0.5 R:0.5 b:0.5 R:0.5 b:0.5 R:0.5"],
           "chorus": ["R:2! 5:2", "8:1 7:1 5:1 b:1"], "break": ["R:2.5! R:1.5", "R:1.5! R:1 R:0.5 b:0.5 R:0.5"], "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 7:0.5 b:0.5", "outro": ["R:1! R:1 R:1 R:1", "R:4!"]},
     drums={**std(16, "drive"), "verse": {"k": "X.X.X.X.X.X.X.X.", "s": ".X.X.X.X.X.X.X.X", "c": "r.r.r.r.r.r.r.r.", "fill": "snare"},
            "chorus": {"k": ["X.......X.......", "X.....X.X......."], "s": "........X.......", "c": "c.......r.......", "fill": "tom"},
            "break": {"k": "sync", "s": "........X.......", "c": "n.........n.....", "fill": "kick"}}, riser=False)

# ════════ 22. 夕凪ディストーション（6/8・長調のバラード・ピアノと弦）════════
song(no=22, slug="yunagi-distortion", title="夕凪ディストーション", seed=2222, bpm=132, beats=6, res=0.5, key="B", mode="ionian", tuning="B1",
     desc="風の止まった夕方の、6/8 で揺れる長調のロック・バラード。Bメジャー・ドロップB・ピアノと弦",
     form=form(132, 6, [("intro", "intro", 4, "1 4"), ("verse1", "verse", 8, "1 5 6m 4"), ("pre1", "pre", 4, "2m 3m 4 5"), ("chorus1", "chorus", 8, "4 5 3m 6m"),
                        ("verse2", "verse", 8, "1 5 6m 4"), ("chorus2", "chorus", 8, "4 5 3m 6m"), ("bridge", "bridge", 6, "6m 4 1 5"), ("solo", "solo", 6, "1 5 6m 4"),
                        ("chorus3", "chorus", 8, "4 5 3m 6m"), ("outro", "outro", 4, "4 1")]),
     rhythm={"tone": "loud-mid", "intro": "-", "verse": ["X=====------", "X=====x=x==="], "pre": "X=====X=====", "chorus": ["X=====X==x==", "X==x==X====="], "bridge": "-", "solo": "X==x==X==x==", "outro": ["X===========", "-"]},
     lead={"tone": "warm-lead-b", "sections": {"chorus1,chorus2,chorus3": {"lo": "D#5", "hi": "E6", "rhythm": L([3, 1, 2], [2, 1, 3], [1, 1, 1, 3], [6]), "peak": 5},
                                               "solo": {"lo": "F#5", "hi": "E6", "rhythm": L([1, 1, 1, 1, 1, 1], [3, 3], [1, 1, 1, 1, 2], [6])}}},
     bass={"intro": "-:6", "verse": ["R:3! 5:2 8:1", "3:3 b:3"], "pre": ["R:2! 5:2 8:2", "7:3 b:3"], "chorus": ["R:2! 5:1 8:2 7:1", "3:2 5:1 b:3"], "bridge": ["8:4! 7:2", "5:3 b:3"],
           "solo": "R:2! 5:1 8:2 b:1", "outro": ["R:6!", "R:6"]},
     drums=generic(12, 2, [3, 3], "six"),
     extras={"piano": {"arp": "intro,verse,bridge,outro", "chords": "", "arpRate": 0.5, "arpLo": "B4"}, "strings": {"pad": "chorus,bridge", "cello": "verse,bridge", "celloMotif": ["R:3 5:3", "8:3 b:3"]}}, riserTo=["chorus"])

# ════════ 23. 九龍シンジケート（ラップメタル寄りの跳ね・ドリアン・ベースが主役）════════
song(no=23, slug="kowloon-syndicate", title="九龍シンジケート", seed=2323, bpm=100, key="E", mode="dorian", tuning="E2",
     desc="迷路の街を跳ね回る、ラップメタル寄りのファンキーなラウドロック。Eドリアン・標準・ベースが主役",
     form=form(100, 4, [("intro", "intro", 8, "1m 4"), ("verse1", "verse", 16, "1m 4 1m 4"), ("pre1", "pre", 6, "3 4 5m 5m"), ("chorus1", "chorus", 12, "1m 3 4 4"),
                        ("verse2", "verse", 12, "1m 4 1m 4"), ("chorus2", "chorus", 12, "1m 3 4 4"), ("bridge", "bridge", 10, "2m 4"), ("chorus3", "chorus", 12, "1m 3 4 4"),
                        ("outro", "outro", 6, "1m 4 1m")]),
     rhythm={"tone": "nu-metal-wall", "intro": ["-", "-", "X--x--x-X---x---", "X--x--x-X-x-x---"], "verse": ["X---x---X--x--x-", "-x--X---x-xX----"], "pre": "X=======X=======",
             "chorus": ["X===x=x=X===x=x=", "X===x===X=x=x=x="], "bridge": "-", "outro": "X==============="},
     lead={"tone": "marshall-mid", "sections": {"chorus1,chorus2,chorus3": {"lo": "G4", "hi": "G5", "rhythm": L([0.5, 0.5, 1, 1, 1], [0.5, 0.5, 0.5, 0.5, 2], [1, 1, 1, 1], [3, 1])}}},
     bass={"drive": 0.5,
           "intro": ["R:0.25! R:0.25' 8:0.25' R:0.25, -:0.25 R:0.25' 5:0.25' 7:0.25 8:0.5! 7:0.25' 5:0.25' 3:0.5 4:0.25 b:0.25", "R:0.25! R:0.25' 8:0.25' R:0.25, -:0.25 R:0.25' 5:0.25' 7:0.25 8:0.25' 9:0.25' 8:0.25' 7:0.25' 5:0.5 3:0.25 b:0.25"],
           "verse": ["R:0.25! R:0.25' 8:0.25' R:0.25, -:0.25 R:0.25' 5:0.25' 7:0.25 8:0.5! 7:0.25' 5:0.25' 3:0.5 4:0.25 b:0.25", "R:0.25! R:0.25' 8:0.25' R:0.25, -:0.25 R:0.25' 5:0.25' 7:0.25 8:0.25' 9:0.25' 8:0.25' 7:0.25' 5:0.5 3:0.25 b:0.25"],
           "verse_b": ["R:0.5! 8:0.25' R:0.25, 7:0.5 8:0.25' 5:0.25' R:0.5 3:0.25' 4:0.25' 5:0.5 b:0.5", "R:0.25! 8:0.25' R:0.25' 8:0.25' 7:0.25' 8:0.25' 5:0.25' 7:0.25' 3:0.5 4:0.5 5:0.5 b:0.5"],
           "pre": ["R:1! 5:1 8:1 7:1", "5:1 4:1 3:1 b:1"], "chorus": ["R:1! 8:0.5' R:0.5 5:0.5 7:0.5 8:0.5 b:0.5", "R:0.5! 3:0.5 4:0.5 5:0.5 7:0.5 8:0.5 9:0.5 b:0.5"],
           "bridge": ["8:0.5! 7:0.25' 5:0.25' 3:0.5 5:0.5 8:1 7:0.5 b:0.5", "R:0.5! 3:0.5 5:0.5 7:0.5 9:1 b:1"], "outro": ["R:0.25! R:0.25' 8:0.25' R:0.25, -:0.25 R:0.25' 5:0.25' 7:0.25 8:0.5! 7:0.25' 5:0.25' 3:0.5 4:0.25 b:0.25", "R:4!", "-:4"]},
     drums={**std(16, "nu"), "intro": {"k": ["................", "................", "X..X..X.X......X", "X..X..X.X..X...."], "s": ["................", "................", "....X..o....X.o.", "....X..o....X.XX"], "h": ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "x.xxx.x.x.xxx.x.", "x.xxx.x.x.xxx.x."], "crash": False, "fill": "snare"}},
     extras={"gated": "chorus"}, riser=False)

# ════════ 24. 星屑ハイウェイ（メロディックなパンク・メタル・長調の疾走）════════
song(no=24, slug="hoshikuzu-highway", title="星屑ハイウェイ", seed=2424, bpm=205, key="D", mode="mixolydian", tuning="D2",
     desc="星屑の高速道路を飛ばす、メロディックなパンク寄りのラウドロック。Dミクソリディアン・ドロップD",
     form=form(205, 4, [("intro", "intro", 8, "1 7 4 1"), ("verse1", "verse", 16, "1 7 4 1"), ("pre1", "pre", 8, "2m 4 5m 7"), ("chorus1", "chorus", 16, "4 1 7 1"),
                        ("verse2", "verse", 16, "1 7 4 1"), ("pre2", "pre", 8, "2m 4 5m 7"), ("chorus2", "chorus", 16, "4 1 7 1"), ("bridge", "bridge", 12, "6m 7 4 4"),
                        ("solo", "solo", 16, "1 7 4 1"), ("chorus3", "chorus", 16, "4 1 7 1"), ("outro", "outro", 8, "4 7 1")]),
     rhythm={"tone": "melodic-punk", "intro": "X=x=x=x=X=x=x=x=", "verse": ["X-x-x-x-X-x-x-x-", "X-x-x-x-x-x-x-x-"], "pre": "X=x=X=x=X=x=X=x=", "chorus": ["X=x=x=x=X=x=x=x=", "X=======X=x=x=x="],
             "bridge": "-", "solo": "X-x-x-x-X-x-x-x-", "outro": "X==============="},
     lead={"tone": "warm-lead-a", "sections": {"chorus1,chorus2,chorus3": {"lo": "A4", "hi": "B5", "rhythm": L([1, 1, 1, 1], [1.5, 0.5, 2], [0.5, 0.5, 1, 1, 1], [4]), "peak": 4},
                                               "intro": {"lo": "D5", "hi": "D6", "rhythm": L([1, 0.5, 0.5, 1, 1], [2, 2])}}},
     tech={"solo": "mmmmmmmmmmmmmm--"},
     bass={"intro": "R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 R:0.5", "verse": ["R:0.5! R:0.5 R:0.5 R:0.5 R:0.5 R:0.5 5:0.5 R:0.5", "R:0.5! R:0.5 R:0.5 R:0.5 3:0.5 5:0.5 8:0.5 b:0.5"],
           "verse_b": ["R:0.5! 8:0.5 R:0.5 8:0.5 R:0.5 8:0.5 5:0.5 3:0.5", "R:0.5! 3:0.5 5:0.5 3:0.5 R:0.5 7:0.5 5:0.5 b:0.5"], "pre": ["R:0.5! R:0.5 R:0.5 R:0.5 5:0.5 5:0.5 8:0.5 8:0.5", "7:1! 5:1 3:1 b:1"],
           "chorus": ["R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 3:0.5 R:0.5", "R:0.5! R:0.5 3:0.5 5:0.5 8:1 b:1"], "bridge": ["R:2! 5:2", "3:2 b:2"], "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 3:0.5 b:0.5",
           "outro": ["R:4!", "R:4", "R:4!"]},
     drums={**std(16, "drive"), "verse": {"k": "X...X.x.X...X.x.", "s": "....X.......X...", "h": "x.x.x.x.x.x.x.x.", "fill": "snare"}},
     extras={"piano": {"chords": "chorus", "soft": "bridge", "chordRhythm": [1, 1, 1, 1], "arp": ""}}, modulate=1)

# ════════ 25. 終焉のオーロラ（壮大なしめくくり・和声的短音階・弦と合唱・全弦開放）════════
song(no=25, slug="shuen-aurora", title="終焉のオーロラ", seed=2525, bpm=145, key="F#", mode="harmonic", tuning="F#1",
     desc="世界の終わりに空を覆うオーロラ。壮大なしめくくりのシンフォニック・メタル。F#の和声的短音階・弦と合唱",
     form=form(145, 4, [("open", "intro", 4, "1m"), ("intro", "intro", 8, "1m 6 4m 5"), ("verse1", "verse", 16, "1m 6 4m 5"), ("pre1", "pre", 8, "6 7dim 1m 5"),
                        ("chorus1", "chorus", 16, "1m 3aug 6 5"), ("verse2", "verse", 16, "1m 6 4m 5"), ("chorus2", "chorus", 16, "1m 3aug 6 5"), ("bridge", "bridge", 12, "6 2dim 5 5"),
                        ("solo", "solo", 16, "1m 6 4m 5"), ("chorus3", "chorus", 16, "1m 3aug 6 5"), ("outro", "outro", 8, "1m 6 1m")]),
     rhythm={"tone": "modern-metalcore", "pm": ["verse"], "open": "-", "intro": "X=======X=======", "verse": ["mm-m-mm-mm-m-m-m", "mm-m-mm-X===X==="], "pre": "X===X===X=x=X===",
             "chorus": ["X=======X===x=x=", "X===x===X=x=x=x="], "bridge": "-", "solo": "X-x-x-x-X-x-x-x-", "outro": ["X===============", "X===============", "-"]},
     lead={"tone": "bmth-lead", "sections": {"intro": {"inst": "violin", "lo": "C#5", "hi": "C#6", "rhythm": L([2, 1, 1], [3, 1], [2, 2], [4])},
                                             "chorus1,chorus2,chorus3": {"lo": "C#5", "hi": "D6", "rhythm": L([1.5, 0.5, 2], [1, 1, 1, 1], [2, 1, 1], [4]), "peak": 5},
                                             "bridge": {"inst": "violin", "lo": "F#4", "hi": "F#5", "rhythm": L([4], [3, 1], [2, 2], [4])}}},
     tech={"solo": "mmmmssmmmmttttmm"},
     bass={"open": "-:4", "intro": ["R:2! 5:2", "8:2 b:2"], "verse": ["R:0.25! R:0.25 -:0.25 R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 R:0.25 -:0.25 R:0.25 5:0.5", "R:0.25! R:0.25 -:0.25 R:0.25 -:0.25 R:0.25 R:0.25 -:0.25 8:1! 7:0.5 b:0.5"],
           "verse_b": ["R:0.25! R:0.25 -:0.25 R:0.25 -:0.25 R:0.25 3:0.5 5:0.5 8:0.5 7:0.5 5:0.5", "3:1! 4:0.5 5:0.5 7:1 b:1"], "pre": ["R:1! 5:1 8:1 5:1", "7:1 8:1 9:1 b:1"],
           "chorus": ["R:1.5! 5:0.5 8:1 7:1", "3:1 5:1 8:1 b:1"], "bridge": ["8:4!", "7:2 b:2"], "solo": "R:0.5! R:0.5 8:0.5 R:0.5 5:0.5 R:0.5 7:0.5 b:0.5", "outro": ["R:4!", "5:4", "R:4!", "-:4"]},
     drums={**std(16, "metalcore"), "open": {"k": ["X...............", "................"], "c": ["c...............", "................"], "crash": False, "nofill": True}},
     extras={"choir": "chorus,bridge,outro", "strings": {"pad": "intro,chorus,bridge,outro", "cello": "verse,bridge", "celloMotif": ["R:2 5:2", "8:2 7:1 b:1"]}, "open": ["F#1", "C#2", "F#2", "B2", "D#3", "G#3"]},
     riserTo=["intro", "chorus", "solo"], modulate=1)
