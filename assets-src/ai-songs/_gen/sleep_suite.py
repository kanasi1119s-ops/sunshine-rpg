# 睡眠用の「不思議な空間」の曲 25曲（2026-10-18、人間の依頼「睡眠用BGMを25曲作ってください。不思議な空間、ゆったり、静か眠れる曲です。
#   頭の中で音がゆっくり流れるように、ほかのことが考えられなくなるような曲にしてください。時間は4分から5分で。曲調は全部変えてください」）。
#
# 作りの考え方（眠りにさそう音）:
#  - 同じ形の「くり返し」（オスティナート）を最初から最後まで、ゆっくり流しつづける。和音が変わると高さだけが変わる。→ 頭の中を音が流れつづけ、ほかのことを考えにくくする。
#  - 旋律は少なく、長い音で。同じ旋律を何度もくり返す（覚えやすい形を、ぼんやり追える）。B の旋律は少し高く。
#  - 土台は、のばす和音（パッドや弦）と、低い根音（ドローン）。和音は、となりの和音へ近い音でつなぐ（声部の動きを小さく）。
#  - テンポは 44〜60（ゆっくりの呼吸にそろえる）。太鼓は入れない。4小節ごとに、息をするように音量が少しふくらんで引く。
#  - 曲ごとに、拍子・テンポ・調と旋法・和音の進み方・くり返しの形・楽器の組み合わせ・旋律の楽器を全部変える。
#  - 既存の曲のメロディ・進行は使わない（CLAUDE.md 1-1）。旋律は曲ごとに決まった乱数で、この曲のために書く。
# 使い方: python3 sleep_suite.py <番号か id か all> [出力フォルダ（省略は assets-src/ai-songs）]   環境変数 SLEEP_TUNE（JSON）で曲ごとの調整を試す
import sys, os, re, json, math, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import nm, fmt

TARGET = 272.0   # くり返しの部分の長さの目安（秒）。終わりの部分を足して 4分半前後

PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else -1 if len(s) > 1 and s[1] == "b" else 0)) % 12

def chord(ch):
    """和音名 → (根音, 和音の音（根音から上へ）, 低音)。maj7・m7・7・6・m6・add9・maj9・m9・sus2・sus4・m7b5・/低音 を読む"""
    head, _, bass = ch.partition("/")
    m = re.match(r"^([A-G][#b]?)(.*)$", head); r = pc(m.group(1)); q = m.group(2)
    minor = q.startswith("m") and not q.startswith("maj")
    t = 5 if "sus4" in q else 2 if "sus2" in q else 3 if minor else 4
    f = 6 if "b5" in q else 8 if "aug" in q else 7
    iv = [0, t, f]
    if "maj7" in q or "maj9" in q: iv.append(11)
    elif "7" in q or ("9" in q and "add9" not in q and "maj9" not in q and "69" not in q): iv.append(10)
    if "6" in q: iv.append(9)
    if "9" in q: iv.append(14)
    return r, [(r + i) % 12 for i in iv], (pc(bass) if bass else r)

MODES = {"ionian": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "mixolydian": [0, 2, 4, 5, 7, 9, 10], "aeolian": [0, 2, 3, 5, 7, 8, 10],
         "lydian": [0, 2, 4, 6, 7, 9, 11], "phrygian": [0, 1, 3, 5, 7, 8, 10], "harmonic": [0, 2, 3, 5, 7, 8, 11], "minpent": [0, 3, 5, 7, 10],
         "majpent": [0, 2, 4, 7, 9], "whole": [0, 2, 4, 6, 8, 10]}
METER = {"4/4": (4, 2), "3/4": (3, 2), "6/8": (2, 3), "9/8": (3, 3), "12/8": (4, 3), "5/4": (5, 2), "2/2": (2, 4)}   # (作曲ソフトの beats, 1拍の細かい単位)

# ================================================================ 楽器（役目ごと）。音域は (下, 上)
CH = lambda **k: [{"type": "chorus", "mix": k.get("mix", 0.2)}]
PAD = {   # のばす和音
    "warmPad": dict(instrument="pad", patch="warmPad", volume=0.075, reverb=0.6, sustain=2.5, attack=0.6, release=0.9, fx=CH()),
    "halo": dict(instrument="pad", patch="halo", volume=0.07, reverb=0.6, sustain=2.5, attack=0.6, release=0.9, fx=CH()),
    "newAge": dict(instrument="pad", patch="newAge", volume=0.065, reverb=0.6, sustain=2.5, attack=0.5, release=0.9, fx=CH()),
    "sweep": dict(instrument="pad", patch="sweep", volume=0.065, reverb=0.6, sustain=2.5, attack=0.6, release=0.9, fx=CH()),
    "bowedGlass": dict(instrument="pad", patch="bowedGlass", volume=0.07, reverb=0.6, sustain=2.5, attack=0.6, release=0.9, fx=CH()),
    "atmosphere": dict(instrument="pad", patch="atmosphere", volume=0.065, reverb=0.6, sustain=2.5, attack=0.5, release=0.9, fx=CH()),
    "metalPad": dict(instrument="pad", patch="metalPad", volume=0.06, reverb=0.6, sustain=2.5, attack=0.7, release=0.9, fx=CH()),
    "strings": dict(instrument="strings", patch="slowStrings", volume=0.075, reverb=0.45, release=0.8, attack=0.4),
    "ensemble": dict(instrument="strings", patch="stringEnsemble", volume=0.07, reverb=0.45, release=0.8, attack=0.4),
    "organ": dict(instrument="pad", patch="reedOrgan", volume=0.055, reverb=0.5, release=0.8, attack=0.4),
}
DRONE = {   # 低い根音
    "contrabass": (dict(instrument="strings", patch="contrabass", volume=0.12, reverb=0.35, release=0.8, attack=0.3), (28, 43)),
    "cello": (dict(instrument="strings", patch="cello", volume=0.11, reverb=0.38, release=0.8, attack=0.3, gainDb=-3), (36, 50)),
    "fretless": (dict(instrument="bass", patch="fretlessBass", volume=0.15, reverb=0.25, release=0.6), (28, 43)),
    "lowpad": (dict(instrument="pad", patch="warmPad", volume=0.09, reverb=0.4, sustain=2.5, attack=0.8, release=1.0), (36, 48)),
}
OST = {   # ゆっくり流れつづけるくり返し。(設定, いちばん下の音)
    "harp": (dict(instrument="harp", volume=0.11, reverb=0.45, bright=-0.4, sustain=3, release=0.8, fx=[{"type": "pingpong", "beats": 1.0, "mix": 0.12, "feedback": 0.25}]), 57),
    "piano": (dict(instrument="piano", volume=0.1, reverb=0.36, sustain=2.2, fx=[{"type": "plate", "mix": 0.16}]), 57),
    "kalimba": (dict(instrument="kalimba", volume=0.1, reverb=0.45, sustain=2.2, fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.14, "feedback": 0.3}]), 62),
    "fmBell": (dict(instrument="fmBell", volume=0.055, reverb=0.5, sustain=3, release=1.0, bright=-0.3), 62),
    "fmEpiano": (dict(instrument="fmEpiano", volume=0.09, reverb=0.4, sustain=2, fx=[{"type": "chorus", "mix": 0.25}]), 55),
    "glock": (dict(instrument="glockenspiel", volume=0.055, reverb=0.5, sustain=4, release=0.8, fx=[{"type": "pingpong", "beats": 1.0, "mix": 0.18, "feedback": 0.3}]), 81),
    "marimba": (dict(instrument="harp", patch="marimba", volume=0.1, reverb=0.42, sustain=1.6), 55),
    "nylon": (dict(instrument="guitar", patch="nylonGuitar", amp="clean", volume=0.1, reverb=0.36, sustain=1.8, bright=-0.35, chorus=0, autoScoop=False, humanPitch=0), 52),
    "crystal": (dict(instrument="lead", patch="crystal", volume=0.05, reverb=0.55, sustain=1.4, fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.2, "feedback": 0.3}]), 64),
    "koto": (dict(instrument="koto", volume=0.1, reverb=0.42, sustain=2), 55),
    "pizz": (dict(instrument="strings", patch="pizzicato", volume=0.11, reverb=0.42), 55),
}
MEL = {   # 長い音の旋律。(設定, 音域)
    "flute": (dict(instrument="panflute", patch="flute", volume=0.15, reverb=0.48, breath=True, attack=0.3, release=0.7, fx=[{"type": "delay", "beats": 1.5, "mix": 0.1, "feedback": 0.25}]), (62, 86)),
    "clarinet": (dict(instrument="panflute", patch="clarinet", volume=0.16, reverb=0.45, breath=True, attack=0.3, release=0.7, fx=[{"type": "plate", "mix": 0.12}]), (52, 79)),
    "oboe": (dict(instrument="panflute", patch="oboe", volume=0.14, reverb=0.45, breath=True, attack=0.3, release=0.7, fx=[{"type": "plate", "mix": 0.12}]), (60, 82)),
    "cello": (dict(instrument="strings", patch="cello", volume=0.15, reverb=0.42, attack=0.35, release=0.8), (45, 69)),
    "viola": (dict(instrument="strings", patch="viola", volume=0.14, reverb=0.45, attack=0.35, release=0.8), (52, 76)),
    "horn": (dict(instrument="brass", patch="horn", volume=0.13, reverb=0.45, breath=True, attack=0.35, release=0.7, fx=[{"type": "reverb", "mix": 0.15}]), (50, 72)),
    "piano": (dict(instrument="piano", volume=0.13, reverb=0.38, sustain=2.4, fx=[{"type": "plate", "mix": 0.16}]), (62, 88)),
    "ocarina": (dict(instrument="ocarina", volume=0.15, reverb=0.48, breath=True, fx=[{"type": "delay", "beats": 1.5, "mix": 0.1, "feedback": 0.25}]), (64, 86)),
    "shakuhachi": (dict(instrument="shakuhachi", volume=0.15, reverb=0.5, breath=True), (62, 84)),
    "calliope": (dict(instrument="lead", patch="calliope", volume=0.11, reverb=0.5, attack=0.3, release=0.8, fx=[{"type": "delay", "beats": 1.5, "mix": 0.14, "feedback": 0.3}]), (60, 84)),
    "fiddle": (dict(instrument="fiddle", patch="violin", volume=0.15, reverb=0.5, gainDb=2, bright=-0.2, attack=0.4, release=0.8, doubleDetune={"cents": 5, "spread": 0.3}), (60, 86)),
    "kalimba": (dict(instrument="kalimba", volume=0.13, reverb=0.48, sustain=2.4), (64, 88)),
}
SPARK = {   # ときどき高く光る音
    "glock": (dict(instrument="glockenspiel", volume=0.05, reverb=0.55, sustain=4, release=0.8, fx=[{"type": "pingpong", "beats": 1.0, "mix": 0.22, "feedback": 0.35}]), (81, 100)),
    "fmBell": (dict(instrument="fmBell", volume=0.045, reverb=0.55, sustain=3, release=1.0, bright=-0.3), (72, 91)),
    "crystal": (dict(instrument="lead", patch="crystal", volume=0.04, reverb=0.6, sustain=1.6, fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.22, "feedback": 0.35}]), (76, 93)),
    "kalimba": (dict(instrument="kalimba", volume=0.07, reverb=0.55, sustain=2.4), (72, 91)),
    "harp": (dict(instrument="harp", volume=0.07, reverb=0.55, bright=-0.3, sustain=3, release=0.8), (72, 93)),
}
TEX = {   # 1回のくり返しに1つ、遠くでただよう音
    "iceRain": dict(instrument="lead", patch="iceRain", volume=0.035, reverb=0.65, sustain=3, release=1.2),
    "echoDrops": dict(instrument="lead", patch="echoDrops", volume=0.035, reverb=0.65, sustain=3, release=1.2),
    "atmosphere": dict(instrument="lead", patch="atmosphere", volume=0.04, reverb=0.65, sustain=3, release=1.2),
    "soundtrack": dict(instrument="lead", patch="soundtrack", volume=0.035, reverb=0.65, sustain=3, release=1.2),
    "starTheme": dict(instrument="lead", patch="starTheme", volume=0.03, reverb=0.65, sustain=3, release=1.2),
}

# ================================================================ 25曲の設計
def Z(id, title, en, image, meter, bpm, key, mode, A, B, pad, drone, ost, opat, mel, mel2=None, spark=None, tex=None, desc="", **kw):
    """A・B: 4つの和音（1つの和音が cb 小節）。opat: くり返しの形（数字＝和音の音の低いほうからの番号、. 休み、- のばす。1文字＝step 単位）"""
    return dict(id=id, title=title, en=en, image=image, meter=meter, bpm=bpm, key=key, mode=mode, A=A.split(), B=B.split(), pad=pad, drone=drone,
                ost=ost, opat=opat, mel=mel, mel2=mel2 or mel, spark=spark, tex=tex, desc=desc, **kw)

SONGS = [
    Z("deep-sea", "深海のゆりかご", "Cradle of the Deep Sea", "光のとどかない深い海の底。ゆっくりゆれる水の中で、遠くのくじらの声を聞く", "4/4", 50, "D", "dorian",
      "Dm9 Bbmaj7 Fmaj7/A Gsus2", "Bbmaj7 C/Bb Am7 Dm9", "warmPad", "contrabass", "harp", "0-2-4-3-1-3-2-4-", "clarinet", "cello", None, "atmosphere",
      "ドリアン。ハープが4分音符で寄せては返す波。旋律はクラリネット、Bはチェロ。"),
    Z("star-sea", "星の海をただよう", "Drifting on a Sea of Stars", "まわりが一面の星。体が軽くなって、星の海をどこまでもただよう", "4/4", 54, "E", "lydian",
      "Emaj7 F#/E G#m7 Cmaj7", "Amaj7 F#/A# G#m7 C#m9", "halo", "fretless", "fmBell", "0.2.4..3.1.2..4.", "flute", None, "glock", "iceRain",
      "リディアン（F# のコード）と ♭VI の Cmaj7。ベルの音が星のまたたき。"),
    Z("moon-library", "月の図書館", "Library of the Moon", "月の上にある、しずかな図書館。ページをめくる音だけが、ゆっくり聞こえる", "3/4", 58, "A", "aeolian",
      "Am9 Fmaj7 Dm9 E7sus4", "Cmaj7 Bbmaj7 Fmaj7/A E7sus4", "strings", "cello", "piano", "024232", "oboe", "viola", "kalimba", None,
      "3拍子。ピアノの分散和音がページのように流れる。ナポリの Bbmaj7。"),
    Z("cloud-cradle", "雲の上のゆりかご", "Cradle Above the Clouds", "やわらかな雲のベッド。風にゆられて、ゆっくり空を流れていく", "6/8", 46, "F", "ionian",
      "Fmaj7 Am7/E Dm9 Bbadd9", "Gm9 Bbmaj7 Csus4 Dbmaj7", "newAge", "lowpad", "harp", "024-3-", "ocarina", "clarinet", "glock", None,
      "6/8 のゆりかご。♭VI の Dbmaj7 で雲の切れ間。"),
    Z("old-clocks", "古時計の眠る部屋", "Room of Sleeping Clocks", "古い時計がたくさん並ぶ部屋。どの時計も、ゆっくり、ゆっくり時をきざむ", "4/4", 60, "C#", "aeolian",
      "C#m9 Amaj7 F#m9 G#7sus4", "Emaj7 B/D# Dmaj7 G#sus4", "ensemble", "contrabass", "marimba", "0.3.1.3.2.3.1.4.", "oboe", "horn", "fmBell", None,
      "マリンバが時計のふりこ。ナポリの Dmaj7。"),
    Z("sand-mirage", "砂の夜の蜃気楼", "Mirage on a Night of Sand", "月の砂漠に、ぼんやり浮かぶ幻の街。近づいても、近づいても遠い", "9/8", 46, "E", "phrygian",
      "Em Fmaj7/E Em7 Dm6/E", "Cmaj7 Fmaj7 Bm7b5 Em", "sweep", "fretless", "nylon", "0--2-13-2", "calliope", None, "crystal", "atmosphere",
      "フリジアン（F のコード）。9/8 のゆらぎ。ドローンは主音のまま。", drone_mode="pedal"),
    Z("forest-spring", "森の奥の泉", "Spring Deep in the Forest", "苔むした森の奥、こんこんとわく泉。水の輪がゆっくり広がる", "4/4", 56, "G", "ionian",
      "Gmaj9 C/G Em9 Cm6", "Am9 Bm7 Cmaj7 D/C", "warmPad", "cello", "kalimba", "0.1.3.2.4.2.3.1.", "flute", "clarinet", "harp", "echoDrops",
      "カリンバが水の輪。短調の Cm6、リディアンの D/C。"),
    Z("ice-cave", "氷の洞窟", "The Ice Cave", "青くすきとおる氷の洞窟。しずくが落ちて、長く長くひびく", "4/4", 48, "B", "aeolian",
      "Bm9 Gmaj7 Em9 F#sus4", "Gmaj7 Dmaj7/F# Cmaj7 F#sus4", "bowedGlass", "contrabass", "crystal", "0..2..1.3..2..4.", "piano", None, "glock", "iceRain",
      "ガラスのような弦と、しずくの音。ナポリの Cmaj7。"),
    Z("dream-carousel", "夢の回転木馬", "Carousel in a Dream", "だれもいない夜の遊園地。回転木馬だけが、ゆっくり回りつづける", "3/4", 56, "Ab", "lydian",
      "Abmaj7 Bb/Ab Cm7 Fm9", "Dbmaj7 Bb/D Cm7 Ebsus4", "strings", "lowpad", "glock", "042-3-", "clarinet", "fiddle", "fmBell", None,
      "オルゴールのような鉄琴のワルツ。リディアン（Bb のコード）。"),
    Z("attic-rain", "雨音の屋根裏", "Attic in the Rain", "屋根をたたく、やさしい雨。屋根裏の小さなベッドで毛布にくるまる", "4/4", 52, "Bb", "mixolydian",
      "Bbadd9 Ab/Bb Ebmaj7/Bb Bbsus2", "Gm9 Abmaj7 Fsus4 F", "warmPad", "fretless", "fmEpiano", "0-1-2-3-2-1-2-4-", "cello", "piano", None, "echoDrops",
      "ミクソリディアン（Ab のコード）。エレピの雨だれ。"),
    Z("lighthouse-night", "灯台のある夜の海", "Night Sea by the Lighthouse", "夜の海を、灯台の光がゆっくりなでていく。波の音が遠くでくり返す", "6/8", 50, "D", "ionian",
      "Dmaj7 Gmaj7/D Bm9 Gm6", "Em9 F#m7 Gmaj7 Asus4", "ensemble", "contrabass", "harp", "013431", "horn", "flute", "glock", None,
      "6/8 の波。短調の Gm6。遠くのホルン。"),
    Z("space-garden", "宇宙の果ての庭", "Garden at the Edge of Space", "宇宙のいちばん果てに、ひっそりと咲く光の花の庭", "4/4", 50, "F#", "lydian",
      "F#maj7 G#/F# D#m9 Bmaj7", "Dmaj7 Emaj7 F#maj7 G#/F#", "sweep", "lowpad", "fmBell", "0..1..3..2..4..2", "calliope", None, "crystal", "starTheme",
      "リディアン。♭VI の Dmaj7 と ♭VII の Emaj7 で、どこまでも浮かぶ。"),
    Z("sunken-bells", "湖に沈んだ鐘", "Bells Beneath the Lake", "湖の底に沈んだ古い鐘。ときどき水の中で、ゆっくり鳴る", "4/4", 46, "C", "dorian",
      "Cm9 F/C Cm9 Abmaj7", "Ebmaj7 Bb/D Abmaj7 Gsus4", "organ", "contrabass", "piano", "0---2---1---3---", "flute", "viola", "fmBell", "atmosphere",
      "オルガンの和音。ピアノは2拍ずつの大きな波。ドリアン（F のコード）。"),
    Z("mist-path", "霧の中の小径", "Path in the Mist", "白い霧の中、足もとの小径だけが見える。どこへ続くのかは分からない", "5/4", 54, "Eb", "aeolian",
      "Ebm9 Cbmaj7 Abm9 Bbsus4", "Gbmaj7 Db/F Cbmaj7 Bbsus4", "strings", "cello", "piano", "0-2-14-3-2-", "clarinet", None, "kalimba", None,
      "5拍子（3+2）。数えられない長さで、霧の中を歩く。"),
    Z("bamboo-moon", "竹林と月", "Moon over the Bamboo Grove", "風のない夜の竹林。竹のすきまから、まるい月がのぞく", "4/4", 52, "D", "minpent",
      "Dm7 Csus2/D Dm7 Am7/D", "Fadd9 Csus2 Gsus2 Am7", "warmPad", "cello", "koto", "0.2.1.3.2.4.3.1.", "shakuhachi", None, None, "atmosphere",
      "尺八（D F G A C）と琴。和音はドローンの上に浮かぶ。", drone_mode="pedal", instrumentCheck=False),
    Z("night-musicbox", "夜空のオルゴール", "Music Box of the Night Sky", "夜空に置かれた大きなオルゴール。星をひとつずつはじいて、ゆっくり鳴る", "3/4", 52, "G", "lydian",
      "Gmaj7 A/G Bm7 Em9", "Cmaj7 D/C Bm7 Ebmaj7", "halo", "lowpad", "kalimba", "0-3-2-", "piano", "flute", "glock", None,
      "3拍子。リディアン（A のコード）と ♭VI の Ebmaj7。"),
    Z("falling-snow", "雪の降る音", "The Sound of Falling Snow", "音のない雪の夜。耳をすますと、雪がつもる音が聞こえる", "4/4", 46, "E", "ionian",
      "Emaj9 C#m9 Amaj7 Am6", "F#m9 G#m7 Amaj7 Bsus4", "strings", "contrabass", "glock", "0...2...1...3...", "piano", "clarinet", None, "iceRain",
      "鉄琴の雪がゆっくり落ちる。短調の Am6。"),
    Z("moss-cave", "光る苔の洞窟", "Cave of Glowing Moss", "洞窟の壁に、緑に光る苔。ほのかな光の中で、時間が止まる", "4/4", 52, "G#", "dorian",
      "G#m9 C#/G# G#m9 Emaj7", "Bmaj7 F#/A# Emaj7 D#sus4", "atmosphere", "fretless", "kalimba", "0.2.1.2.3.2.1.4.", "fiddle", None, "crystal", "echoDrops",
      "ドリアン（C# のコード）。カリンバの光の粒。"),
    Z("stopped-station", "時の止まった駅", "The Station Where Time Stopped", "最終列車が行ったあとの、小さな駅。ベンチで、来ない列車を待つ", "4/4", 58, "A", "mixolydian",
      "Aadd9 G/A Dmaj7/A Asus2", "F#m9 Gmaj7 Dmaj7 Esus4", "organ", "contrabass", "nylon", "0.2.3.1.2.4.3.2.", "oboe", None, "fmBell", None,
      "ミクソリディアン（G のコード）。ナイロン弦のギター。"),
    Z("hanging-garden", "空中庭園の夜", "Night in the Hanging Garden", "空にうかぶ庭園。夜の花のあいだを、ゆっくり風がとおる", "3/4", 50, "Bb", "lydian",
      "Bbmaj7 C/Bb Dm9 Gm9", "Ebmaj7 F/Eb Dm7 Fsus4", "halo", "cello", "harp", "024342", "horn", "fiddle", "kalimba", None,
      "3拍子のハープ。リディアン（C のコード）。"),
    Z("deep-sleep-waves", "深い眠りの波", "Waves of Deep Sleep", "大きな波が、ゆっくり、ゆっくり、寄せては返す。だんだん体が重くなる", "4/4", 44, "C", "lydian",
      "Cmaj9 D/C Em9 Am9", "Fmaj7 G/F Em7 D/F#", "ensemble", "lowpad", "piano", "0---1---2---4---3---2---1---2---", "cello", None, "harp", "atmosphere",
      "いちばん遅い曲。ピアノは2拍ごとに1音（呼吸に合わせる）。", cb=2),
    Z("greenhouse", "夢見る温室", "The Dreaming Greenhouse", "ガラスの温室に、見たことのない植物。夜になると、ほのかに光る", "4/4", 56, "F", "lydian",
      "Fmaj9 G/F Am9 Dm9", "Bbmaj7 Cmaj7 Dbmaj7 Ebmaj7", "newAge", "fretless", "marimba", "0.1.2.4.3.1.2.3.", "flute", "oboe", "crystal", None,
      "B は長7の和音が全音ずつ上がる（♭VI・♭VII）。マリンバの葉ずれ。"),
    Z("star-threads", "星座をつなぐ糸", "Threads Between Constellations", "星と星を細い光の糸がつなぎ、ゆっくり星座になっていく", "12/8", 44, "Db", "ionian",
      "Dbmaj7 Bbm9 Gbmaj7 Ebm9", "Gbmaj7 Abm7 Fm7 Bbm9", "warmPad", "contrabass", "harp", "024-35-31-24", "clarinet", "flute", "glock", "starTheme",
      "12/8 のゆったりした流れ。ハープが糸をたぐる。"),
    Z("wander-woods", "迷いの森の灯り", "Lights in the Wandering Woods", "深い森の中に、ぽつりと浮かぶ灯り。ついていくと、また次の灯りが浮かぶ", "6/8", 48, "F", "harmonic",
      "Fm9 Dbmaj7 Bbm9 C7sus4", "Abmaj7 Gb Dbmaj7 C7sus4", "sweep", "cello", "pizz", "0.2.1.", "ocarina", "viola", "fmBell", "soundtrack",
      "ヘ短調（和声的）。ピチカートが足音。ナポリの Gb。"),
    Z("before-dawn", "夜明けの手前で", "Just Before Dawn", "夜明けの少し前、空がうっすら明るくなる。もう少しだけ、眠っていよう", "4/4", 50, "G", "lydian",
      "Gmaj9 A/G Em9 Cmaj7", "Am9 Bm7 Cmaj9 D/C", "strings", "cello", "fmEpiano", "0-2-1-3-2-4-3-2-", "piano", "horn", "glock", "iceRain",
      "最後の曲。リディアン（A のコード）。夜明けの前の、やさしい光。"),
]

# 点数（Audiobox の PQ）で決めた曲ごとの調整
FINAL = {}


# ================================================================ 音を書く
class Part:
    def __init__(self, base, role):
        self.base = dict(base); self.role = role; self.ev = []   # (開始の単位, 長さの単位, 音 or None, 記号)
    def add(self, s, d, m, mark=""): self.ev.append((s, d, m, mark))


def voicing(pcs, prev, lo=45, hi=69):
    """4声の和音。前の和音から動きがいちばん小さい形"""
    want = list(dict.fromkeys(pcs))[:4]
    if len(want) < 4: want = want + [want[0]] * (4 - len(want))
    best = None
    for perm in set(itertools.permutations(want)):
        cand = []; m0 = lo
        ok = True
        for i, p in enumerate(perm):
            ref = prev[i] if prev else lo + 3 + i * 5
            opts = [x for x in range(lo, hi + 1) if x % 12 == p]
            x = min(opts, key=lambda x: abs(x - ref))
            cand.append(x)
        if len(set(cand)) < 4: continue
        cost = sum(abs(a - b) for a, b in zip(cand, prev)) if prev else sum(abs(x - (lo + 3 + i * 5)) for i, x in enumerate(cand))
        if best is None or cost < best[0]: best = (cost, cand)
    if best: return best[1]
    # 4つの音が重なってしまうときは、下から順に積む（同じ音は1オクターブ上へ）
    out = []
    for p in want:
        x = min(x for x in range(lo, hi + 13) if x % 12 == p)
        while x in out: x += 12
        out.append(x)
    return sorted(out)


def scale_for(scale, cpcs):
    s = set(cpcs)
    for x in scale:
        if all((x - c) % 12 not in (1, 11) for c in cpcs): s.add(x)
    return sorted(s)


def build(song, out):
    rng = random.Random(song["id"] + str(song.get("seed", "")))
    beats, sub = METER[song["meter"]]; BU = beats * sub; bpm = song["bpm"]
    bar_s = beats * 60 / bpm; cb = song.get("cb", 2 if bar_s < 5 else 1)
    key = pc(song["key"]); scale = [(key + i) % 12 for i in MODES[song["mode"]]]
    loop_bars = 4 * cb; loop_s = loop_bars * bar_s
    n = max(6, round(TARGET / loop_s))
    # くり返しごとの設計: (和音 A/B, 鳴らすもの, 旋律 A/B/なし, 強さ)
    core = [("A", "pod", "A", 0.8), ("B", "podsx", "B", 0.9), ("A", "podx", "A", 0.88), ("B", "potx", None, 0.72),
            ("B", "pods", "B", 0.95), ("A", "podx", "A", 0.85)]
    plan = [("A", "po", None, 0.6)]
    k = 0
    while len(plan) < n - 1: plan.append(core[k % len(core)]); k += 1
    plan.append(("A", "pot", None, 0.62))
    plan = song.get("plan", plan)
    total_bars = len(plan) * loop_bars + 3
    TU = total_bars * BU
    P = {}
    padb = dict(PAD[song["pad"]]); P["pad"] = [Part(padb, f"パッド（{song['pad']}・{i + 1}）") for i in range(4)]
    db, (dlo, dhi) = DRONE[song["drone"]]; P["drone"] = Part(db, f"低音（{song['drone']}）")
    ob, olo = OST[song["ost"]]; P["ost"] = Part(ob, f"くり返し（{song['ost']}）")
    mb, (mlo, mhi) = MEL[song["mel"]]; P["mel"] = Part(mb, f"旋律（{song['mel']}）")
    if song["mel2"] != song["mel"]:
        mb2, (mlo2, mhi2) = MEL[song["mel2"]]; P["mel2"] = Part(mb2, f"旋律B（{song['mel2']}）")
    if song.get("spark"): sb, (slo, shi) = SPARK[song["spark"]]; P["spark"] = Part(sb, f"きらめき（{song['spark']}）")
    if song.get("tex"): P["tex"] = Part(TEX[song["tex"]], f"遠くの音（{song['tex']}）")
    tune = song.get("tune", {})
    for k2, v in tune.items():   # 例: {"pad": {"volume": 0.09}}
        tgt = P.get(k2)
        if tgt is None: continue
        for p in (tgt if isinstance(tgt, list) else [tgt]): p.base.update(v)

    # 和音の並び（小節ごと）
    bar_ch = []
    for (ab, _, _, _) in plan:
        for ch in song[ab]: bar_ch += [ch] * cb
    tonic = song.get("end_chord") or (song["key"] + ("m9" if song["mode"] in ("aeolian", "dorian", "phrygian", "harmonic", "minpent") else "maj9"))
    bar_ch += [tonic] * 3

    # パッド・低音
    prev = None; b = 0
    while b < total_bars:
        ch = bar_ch[b]; L = 1
        while b + L < total_bars and bar_ch[b + L] == ch and L < (3 if b >= total_bars - 3 else cb): L += 1
        r, cpcs, bass = chord(ch)
        v = voicing(cpcs, prev); prev = v
        for i, m in enumerate(v): P["pad"][i].add(b * BU, L * BU, m)
        dp = key if song.get("drone_mode") == "pedal" else bass
        dm = dlo + ((dp - dlo) % 12)
        P["drone"].add(b * BU, L * BU, dm)
        b += L

    # くり返し（オスティナート）: 曲の頭から最後まで、形をくり返す（和音が変わると高さだけ変わる）
    pat = song["opat"]; step = song.get("ostep", 1)
    u = 0; j = 0; cur = None
    while u < TU - BU:   # 最後の小節は、のばした音だけ
        c = pat[j % len(pat)]; ch = bar_ch[u // BU]
        if c.isdigit():
            r, cpcs, _ = chord(ch)
            tones = [x for x in range(olo, olo + 30) if x % 12 in cpcs]
            m = tones[min(int(c), len(tones) - 1)]
            cur = [u, step, m]; P["ost"].ev.append(cur)
        elif c == "-" and cur is not None and cur[0] + cur[1] == u: cur[1] += step
        else: cur = None
        u += step; j += 1
    P["ost"].ev = [tuple(e) + ("",) for e in P["ost"].ev]
    lastr, lpcs, _ = chord(tonic)
    lt = [x for x in range(olo, olo + 30) if x % 12 in lpcs]
    P["ost"].add(TU - BU, BU, lt[0])

    # 旋律: A と B を1回ずつ書き、同じ旋律をくり返す（2回目以降は最後の和音の所だけ少し変える）
    def phrase(chs, lo, hi, center, seed):
        r2 = random.Random(song["id"] + seed); blk = cb * BU; notes = []
        vals = [sub * 1, sub * 2, sub * 2, sub * 3, sub * 4] + ([sub + sub // 2] if sub == 2 else [])
        prevm = center
        bump = [0, 2, 4, -1]
        for bi, ch in enumerate(chs):
            r, cpcs, _ = chord(ch); sc = scale_for(scale, cpcs)
            for _ in range(300):
                rhythm = []; rem = blk
                while rem > 0:
                    if rem <= sub * 4 and rem >= sub * 2 and (rhythm or cb == 1) and r2.random() < 0.6: rhythm.append(rem); break
                    opts = [v for v in vals if v <= rem] or [rem]
                    d = r2.choice([v for v in opts if rem - v >= sub * 2] or opts); rhythm.append(d); rem -= d
                if (2 if cb > 1 else 1) <= len(rhythm) <= (4 if cb > 1 else 3) and rhythm[-1] >= sub * 2: break
            if r2.random() < 0.35 and rhythm[-1] >= sub * 3: rhythm[-1] -= sub; rhythm.append(-sub)
            t = bi * blk
            goal = center + bump[bi] * (1 if cb > 1 else 0.6)
            for k3, d in enumerate(rhythm):
                if d < 0: t += -d; continue
                pool = [x for x in range(lo, hi + 1) if x % 12 in sc]
                if k3 == 0 or d >= sub * 2:
                    pool = [x for x in range(lo, hi + 1) if x % 12 in cpcs or (x - r) % 12 == 2]
                cand = sorted(pool, key=lambda x: abs(x - prevm) * 1.0 + abs(x - goal) * 0.5 + r2.random() * 2.5)
                m = cand[0] if abs(cand[0] - prevm) > 0 or len(cand) < 2 else cand[1 if r2.random() < 0.7 else 0]
                if k3 == len(rhythm) - 1 and bi == 3: m = min([x for x in range(lo, hi + 1) if x % 12 in cpcs], key=lambda x: abs(x - prevm))
                notes.append((t, d, m)); prevm = m; t += d
        return notes
    mid = (mlo + mhi) // 2
    melA = phrase(song["A"], mlo, mhi, mid - 2, "A")
    if "mel2" in P: mlo2_, mhi2_ = MEL[song["mel2"]][1]
    else: mlo2_, mhi2_ = mlo, mhi
    melB = phrase(song["B"], mlo2_, mhi2_, (mlo2_ + mhi2_) // 2 + 2, "B")
    melA2 = melA[:]; tail = phrase(song["A"], mlo, mhi, mid, "A2")
    melA2 = [x for x in melA if x[0] < 3 * cb * BU] + [x for x in tail if x[0] >= 3 * cb * BU]
    seenA = 0
    for li, (ab, lay, mk, lvl) in enumerate(plan):
        s0 = li * loop_bars * BU
        if mk == "A":
            src = melA if seenA % 2 == 0 else melA2; seenA += 1
            for (t, d, m) in src: P["mel"].add(s0 + t, d, m, "~" if d >= 3 * sub else "")
        elif mk == "B":
            tgt = P.get("mel2", P["mel"])
            for (t, d, m) in melB: tgt.add(s0 + t, d, m, "~" if d >= 3 * sub else "")
        if "s" in lay and "spark" in P:
            for bb in range(0, loop_bars, 2):
                if rng.random() < 0.75:
                    ch = bar_ch[li * loop_bars + bb]; r, cpcs, _ = chord(ch)
                    pool = [x for x in range(slo, shi + 1) if x % 12 in cpcs]
                    off = rng.choice([0, sub, 2 * sub, BU // 2]) if BU > 2 * sub else 0
                    P["spark"].add(s0 + bb * BU + off, 2 * BU - off, rng.choice(pool))
        if "t" in lay and "tex" in P:
            ch = bar_ch[li * loop_bars]; r, cpcs, _ = chord(ch)
            m = 60 + ((cpcs[min(2, len(cpcs) - 1)] - 60) % 12) + 12
            P["tex"].add(s0 + BU, max(sub, min(int(9 * bpm / 60) * sub, (loop_bars - 2) * BU)), m)   # 9 秒まで（息の長さ）

    # 音量: くり返しごとの強さ（なめらかに）×4小節ごとの呼吸×最初と最後のフェード
    lv = []
    for (_, _, _, l) in plan: lv += [l] * loop_bars
    lv += [0.55, 0.45, 0.35]
    sm = [sum(lv[max(0, i - 2):i + 3]) / len(lv[max(0, i - 2):i + 3]) for i in range(total_bars)]
    gain = []
    for i in range(total_bars):
        g = sm[i] * (1 + 0.07 * math.sin(2 * math.pi * (i - 1) / 4))
        if i < 2: g *= 0.75 + 0.125 * i
        gain.append(round(min(1.0, g), 3))

    # パートを、作曲ソフトの書式に
    parts = []
    def rest(units):   # 長い休みは 8 拍ずつに分ける（作曲ソフトが読める長さ）
        out = []
        while units > 0:
            d = min(units, 8 * sub); out.append(f"R:{fmt(d / sub)}"); units -= d
        return out
    def emit(p, legato=False, onlay=None):
        ev = sorted(p.ev); toks = []; t = 0
        for i, (s, d, m, mk) in enumerate(ev):
            if s < t: continue
            if i + 1 < len(ev) and s + d > ev[i + 1][0]: d = ev[i + 1][0] - s
            if d <= 0: continue
            if s > t: toks += rest(s - t)
            toks.append(f"{nm(m)}:{fmt(d / sub)}{mk}")
            t = s + d
        if t < TU: toks += rest(TU - t)
        if not ev: return
        q = dict(p.base); q["role"] = p.role; q.setdefault("pan", 0); q["barGain"] = gain; q["notes"] = " ".join(toks)
        parts.append(q)
    # くり返しの層をはずす所（"o" がない所）は音を消す
    def mute(p, letter):
        keep = []
        for e in p.ev:
            li = e[0] // (loop_bars * BU)
            if li >= len(plan) or letter in plan[li][1]: keep.append(e)
        p.ev = keep
    mute(P["ost"], "o"); mute(P["drone"], "d")
    pans = song.get("pans", {})
    for i, p in enumerate(P["pad"]): p.base["pan"] = pans.get("pad", -0.45 if song["pad"] in ("strings", "ensemble") else 0)
    P["drone"].base["pan"] = 0
    P["ost"].base["pan"] = pans.get("ost", -0.35)
    P["mel"].base["pan"] = pans.get("mel", 0.1)
    if "mel2" in P: P["mel2"].base["pan"] = pans.get("mel2", -0.12)
    if "spark" in P: P["spark"].base["pan"] = pans.get("spark", 0.55)
    if "tex" in P: P["tex"].base["pan"] = pans.get("tex", -0.5)
    for p in P["pad"]: emit(p)
    for k2 in ("drone", "ost", "mel", "mel2", "spark", "tex"):
        if k2 in P: emit(P[k2])
    if song.get("mel_db"):
        for q in parts:
            if q["role"].startswith("旋律"): q["gainDb"] = q.get("gainDb", 0) + song["mel_db"]

    tempo = [{"bar": total_bars - 2, "bpm": round(bpm * 0.86), "ramp": 3}]
    secs = sum(bar_s for _ in range(total_bars - 3)) + 3 * bar_s / 0.93
    mmss = f"{int(secs // 60)}分{int(secs % 60):02d}秒"
    md_ = {"ionian": "長調", "aeolian": "短調", "dorian": "ドリアン", "lydian": "リディアン", "mixolydian": "ミクソリディアン", "phrygian": "フリジアン",
           "harmonic": "和声的短音階", "minpent": "短調の五音音階", "majpent": "長調の五音音階", "whole": "全音音階"}[song["mode"]]
    j = {"title": song["title"] + "（仮）",
         "description": f"（仮）睡眠用。{song['image']}。{song['meter']}・BPM{bpm}・{song['key']}の{md_}、約{mmss}。くり返し: {song['ost']}、和音: {song['pad']}、低音: {song['drone']}、旋律: {song['mel']}"
                        + (f"・{song['mel2']}" if song['mel2'] != song['mel'] else "") + f"。{song['desc']}",
         "bpm": bpm, "beats": beats, "chords": " ".join(bar_ch), "barsPerChord": 1, "repeats": 1, "tone": "rock", "feel": "rock", "human": 0.15,
         "dynamics": "natural", "autoAccompaniment": False, "autoScoop": False, "guitarWobble": False, "parts": parts, "tempo": tempo, "titleEn": song["en"]}
    if song.get("instrumentCheck") is False: j["instrumentCheck"] = False
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump(j, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return secs


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "assets-src/ai-songs"
    tune = json.loads(os.environ["SLEEP_TUNE"]) if "SLEEP_TUNE" in os.environ else FINAL
    for n, s in enumerate(SONGS, 1):
        if which not in ("all", str(n), s["id"]): continue
        if f"{n:02d}" in tune: s = dict(s, **tune[f"{n:02d}"])
        out = os.path.join(outdir, f"sleep25-{n:02d}-{s['id']}.json")
        t = build(s, out)
        print(f"{n:02d} {s['id']} {t:.0f}秒")
