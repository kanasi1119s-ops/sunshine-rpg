# カフェでゆったり聞けるジャズ 25曲（2026-10-19、人間の依頼「カフェでゆったり聞けるjazzソングを25曲作ってください。空間を包み込むような感じで、
#   集中力が高まるようにお願いします。時間は4〜5分で。曲調はすべて変えてください」）。
#
# 作りの考え方:
#  - 集中できる音: テンポは最後まで一定、同じノリ（グルーブ）がずっと続く。音量が急に変わらない（強弱はなめらかに、ソロも大きくしない）。
#    旋律は歌える形（短い動機をくり返して変える）。速いフレーズを詰めこまない（ソロも「息つぎ」をはさむ）。
#  - 空間を包む音: うしろに薄い弦（またはパッド）を長くのばし、左右に広げる。ピアノ・ギターの和音は左右に置き、真ん中は旋律とベース。
#    書き出しで部屋の残響（--space）を足す。
#  - ジャズの形: イントロ → テーマ（A A' B A''、各8小節）→ ソロ（同じ進行の上で、旋律の楽器・2つ目の楽器が順に）→ テーマ → 終わり（ゆっくりにして伸ばす）。
#    ピアノの和音は「根音を省いた」形（3度・7度・9度・13度）で、となりの和音へ近い音でつなぐ。ベースは曲の型（ウォーキング・2ビート・ボサノバ・トゥンバオ…）。
#  - 25曲で、リズムの型・拍子・テンポ・調・和音の進み方・旋律の楽器・和音の楽器をすべて変える。
#  - 既存の曲の旋律・進行は使わない（CLAUDE.md 1-1）。進行はこの曲集のために書き、旋律は曲ごとに決まった乱数で、この曲のために作る。
# 使い方: python3 cafe_jazz.py <番号か id か all> [出力フォルダ]   環境変数 JAZZ_TUNE（JSON）で曲ごとの調整を試す
import sys, os, re, json, math, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import nm, fmt

TPB = 12                       # 1拍 = 12 刻み（8分・16分・3連符を全部表せる）
TARGET = (262.0, 292.0)        # 曲の長さ（秒）

PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pcof(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else -1 if len(s) > 1 and s[1] == "b" else 0)) % 12

# ================================================================ 和音
# 種類 → (和音の音, 根音を省いた4声, 旋律に使う音階)。数字は根音からの半音
IONIAN = [0, 2, 4, 5, 7, 9, 11]; DORIAN = [0, 2, 3, 5, 7, 9, 10]; MIXO = [0, 2, 4, 5, 7, 9, 10]
Q = {
    "maj7": ([0, 4, 7, 11], [4, 7, 11, 14], IONIAN),
    "maj7#11": ([0, 4, 7, 11], [4, 6, 11, 14], [0, 2, 4, 6, 7, 9, 11]),
    "6": ([0, 4, 7, 9], [4, 7, 9, 14], IONIAN),
    "maj": ([0, 4, 7], [4, 7, 12, 14], IONIAN),
    "m7": ([0, 3, 7, 10], [3, 7, 10, 14], DORIAN),
    "m6": ([0, 3, 7, 9], [3, 7, 9, 14], DORIAN),
    "m11": ([0, 3, 7, 10], [3, 10, 14, 17], DORIAN),
    "mM7": ([0, 3, 7, 11], [3, 7, 11, 14], [0, 2, 3, 5, 7, 9, 11]),
    "m": ([0, 3, 7], [3, 7, 12, 14], [0, 2, 3, 5, 7, 8, 10]),
    "7": ([0, 4, 7, 10], [4, 9, 10, 14], MIXO),
    "7b9": ([0, 4, 7, 10], [4, 7, 10, 13], [0, 1, 4, 5, 7, 8, 10]),
    "7alt": ([0, 4, 10], [4, 10, 15, 20], [0, 1, 3, 4, 6, 8, 10]),
    "7#11": ([0, 4, 7, 10], [4, 6, 10, 14], [0, 2, 4, 6, 7, 9, 10]),
    "7sus4": ([0, 5, 7, 10], [5, 10, 14, 19], [0, 2, 5, 7, 9, 10]),
    "m7b5": ([0, 3, 6, 10], [3, 6, 10, 14], [0, 2, 3, 5, 6, 8, 10]),
    "dim7": ([0, 3, 6, 9], [3, 6, 9, 12], [0, 2, 3, 5, 6, 8, 9, 11]),
}
ALIAS = [("maj9", "maj7"), ("maj7#11", "maj7#11"), ("maj7", "maj7"), ("69", "6"), ("6", "6"), ("m7b5", "m7b5"), ("dim7", "dim7"), ("mM7", "mM7"),
         ("m11", "m11"), ("m9", "m7"), ("m7", "m7"), ("m6", "m6"), ("9sus4", "7sus4"), ("7sus4", "7sus4"), ("sus4", "7sus4"),
         ("7b9", "7b9"), ("7#9", "7alt"), ("7alt", "7alt"), ("7#11", "7#11"), ("13", "7"), ("9", "7"), ("7", "7"), ("m", "m"), ("", "maj")]

def chord(name):
    """和音名 → dict(r=根音, q=種類, tones, voice, scale, bass)"""
    head, _, bass = name.partition("/")
    m = re.match(r"^([A-G][#b]?)(.*)$", head); r = pcof(m.group(1)); rest = m.group(2)
    q = dict(ALIAS)[rest]
    tones, voice, scale = Q[q]
    return dict(r=r, q=q, name=name, tones=[(r + i) % 12 for i in tones], voice=[r + i for i in voice],
                scale=sorted({(r + i) % 12 for i in scale}), bass=pcof(bass) if bass else r, third=(r + (3 if q in ("m7", "m6", "m11", "mM7", "m", "m7b5", "dim7") else 5 if q == "7sus4" else 4)) % 12)

def voicing(pcs, prev, lo, hi):
    """根音を省いた4声。前の和音から動きがいちばん小さい形（4声が lo〜hi に入る）"""
    want = list(dict.fromkeys(p % 12 for p in pcs))[:4]
    while len(want) < 4: want.append(want[0])
    best = None
    for perm in set(itertools.permutations(want)):
        cand = []
        for i, p in enumerate(perm):
            ref = prev[i] if prev else lo + 2 + i * 4
            cand.append(min((x for x in range(lo, hi + 1) if x % 12 == p), key=lambda x: abs(x - ref)))
        if len(set(cand)) < 4: continue
        if max(cand) - min(cand) > 14: continue            # 手の幅
        cost = sum(abs(a - b) for a, b in zip(cand, prev)) if prev else sum(abs(x - (lo + 4 + i * 4)) for i, x in enumerate(cand))
        if best is None or cost < best[0]: best = (cost, cand)
    if best is None:
        base = lo; out = []
        for p in want:
            x = min(x for x in range(base, base + 13) if x % 12 == p)
            while x in out: x += 12
            out.append(x)
        return out
    return best[1]

# ================================================================ 楽器
def P(**k): return k
INST = {
    # 旋律
    "piano": (P(instrument="piano", volume=0.2, reverb=0.26, sustain=1.7, bright=-0.25), (57, 89)),
    "flute": (P(instrument="panflute", patch="flute", volume=0.2, reverb=0.38, breath=True, attack=0.06, release=0.45, bright=-0.2, fx=[{"type": "plate", "mix": 0.12}]), (62, 86)),
    "clarinet": (P(instrument="panflute", patch="clarinet", volume=0.21, reverb=0.35, breath=True, attack=0.06, release=0.45, fx=[{"type": "plate", "mix": 0.1}]), (55, 79)),
    "clarinetLow": (P(instrument="panflute", patch="clarinet", volume=0.22, reverb=0.4, breath=True, attack=0.08, release=0.5, bright=-0.25, fx=[{"type": "plate", "mix": 0.14}]), (52, 72)),
    "trumpet": (P(instrument="brass", patch="trumpet", volume=0.15, reverb=0.4, breath=True, attack=0.06, release=0.4, bright=-0.55, fx=[{"type": "eq", "low": 0, "mid": -2, "midHz": 3000, "high": -5}, {"type": "plate", "mix": 0.12}]), (58, 79)),
    "trombone": (P(instrument="brass", patch="trombone", volume=0.18, reverb=0.38, breath=True, attack=0.07, release=0.45, bright=-0.35, fx=[{"type": "plate", "mix": 0.1}]), (46, 70)),
    "horn": (P(instrument="brass", patch="horn", volume=0.18, reverb=0.42, breath=True, attack=0.08, release=0.5, bright=-0.3, fx=[{"type": "plate", "mix": 0.12}]), (53, 74)),
    "oboe": (P(instrument="panflute", patch="oboe", volume=0.18, reverb=0.38, breath=True, attack=0.06, release=0.45, bright=-0.2, fx=[{"type": "plate", "mix": 0.1}]), (60, 82)),
    "violin": (P(instrument="fiddle", patch="violin", volume=0.17, reverb=0.42, gainDb=1, bright=-0.3, attack=0.08, release=0.5), (62, 86)),
    "viola": (P(instrument="strings", patch="viola", volume=0.19, reverb=0.42, attack=0.1, release=0.5), (55, 79)),
    "cello": (P(instrument="strings", patch="cello", volume=0.2, reverb=0.4, attack=0.1, release=0.5), (45, 69)),
    "jazzGuitar": (P(instrument="leadGuitar", patch="jazzGuitar", amp="jazz", volume=0.2, reverb=0.28, sustain=1.2, chorus=0, autoScoop=False, humanPitch=0, bright=-0.2), (55, 81)),
    # 2026-10-19 人間「電子音系はなるべく使わず、実際の楽器音を」→ エレピ・オルガン・シンセのパッドをやめ、録音の楽器（VCSL ほか）にする
    "vibes": (P(instrument="harp", patch="vibraphone", volume=0.2, reverb=0.42, sustain=1.8, bright=-0.2, fx=[{"type": "plate", "mix": 0.12}]), (57, 89)),
    "tenorSax": (P(instrument="brass", patch="tenorSax", volume=0.18, reverb=0.4, breath=True, attack=0.05, release=0.5, bright=-0.3, fx=[{"type": "plate", "mix": 0.12}]), (46, 75)),
    "marimba": (P(instrument="harp", patch="marimba", volume=0.2, reverb=0.35, sustain=1.4), (57, 84)),
    "kalimba": (P(instrument="harp", patch="kalimbaReal", volume=0.2, reverb=0.4, sustain=1.8, bright=-0.2), (60, 88)),
    "accordion": (P(instrument="accordion", volume=0.15, reverb=0.35, attack=0.05, release=0.35), (57, 81)),
    "nylon": (P(instrument="leadGuitar", patch="nylonGuitar", amp="clean", volume=0.19, reverb=0.32, sustain=1.3, bright=-0.3, chorus=0, autoScoop=False, humanPitch=0), (55, 81)),
}
COMP = {   # 和音の楽器（4声）。(設定, 下, 上, パン)
    "piano": (P(instrument="piano", volume=0.085, reverb=0.38, sustain=1.5, bright=-0.35), 50, 72, -0.4),
    "vibes": (P(instrument="harp", patch="vibraphone", volume=0.09, reverb=0.4, sustain=1.5, bright=-0.25), 53, 74, 0.4),
    "nylon": (P(instrument="guitar", patch="nylonGuitar", amp="clean", volume=0.085, reverb=0.28, sustain=1.0, bright=-0.35, chorus=0, autoScoop=False, humanPitch=0), 50, 70, -0.45),
    "jazzGuitar": (P(instrument="guitar", patch="jazzGuitar", amp="jazz", volume=0.08, reverb=0.25, sustain=0.9, bright=-0.3, chorus=0, autoScoop=False, humanPitch=0), 50, 69, 0.45),
    "marimba": (P(instrument="harp", patch="marimba", volume=0.09, reverb=0.32, sustain=1.0), 55, 74, -0.4),
    "pizz": (P(instrument="strings", patch="pizzicato", volume=0.1, reverb=0.35), 52, 74, -0.45),
    "accordion": (P(instrument="accordion", volume=0.06, reverb=0.3, attack=0.03, release=0.25), 55, 72, -0.4),
}
PADS = {   # うしろの長い和音（空間）
    "strings": P(instrument="strings", patch="slowStrings", volume=0.045, reverb=0.5, attack=0.6, release=1.0),
    "ensemble": P(instrument="strings", patch="stringEnsemble", volume=0.04, reverb=0.5, attack=0.6, release=1.0),
}

# ================================================================ 25曲の設計
def S(id, title, en, image, meter, bpm, swing, key, A, B, drums, bass, comp, cstyle, lead, solo2, pad, desc, **kw):
    return dict(id=id, title=title, en=en, image=image, meter=meter, bpm=bpm, swing=swing, key=key, A=A, B=B, drums=drums, bass=bass,
                comp=comp, cstyle=cstyle, lead=lead, solo2=solo2, pad=pad, desc=desc, **kw)

SONGS = [
    S("morning-espresso", "朝のエスプレッソ", "Morning Espresso", "開店したばかりのカフェ。一杯目のエスプレッソの香り", "4/4", 116, 0.62, "F",
      "Fmaj7 | Em7b5 A7b9 | Dm9 | Cm7 F7 | Bbmaj7 | Bbm7 Eb7 | Am7 D7b9 | Gm7 C7",
      "Bbmaj7 | Bm7b5 E7b9 | Am9 | Abm7 Db7 | Gm9 | Gm7 C7sus4 | Fmaj7 D7 | Gm7 C7",
      "swing", "walk", "piano", "swing", "piano", "piano", "strings", "ピアノトリオのミディアム・スウィング。ブラシのようにやさしいライド。"),
    S("rainy-bossa", "雨の窓辺のボサノバ", "Bossa by the Rainy Window", "窓をつたう雨つぶ。ガラスの向こうの、にじんだ街", "4/4", 126, 0.0, "D",
      "Dm9 | Dm9 | Gm9 | Gm9 | Em7b5 | A7b9 | Dm9 | Bbmaj7 A7alt",
      "Fmaj7 | Bbmaj7 | Em7b5 | A7b9 | Dm9 | G7#11 | Gm9 | A7alt",
      "bossa", "bossa", "nylon", "bossa", "flute", "piano", "strings", "ナイロン弦のギターがボサノバのリズム。旋律はフルート。"),
    S("afternoon-waltz", "午後のワルツ", "Afternoon Waltz", "午後のひざしが、テーブルにゆっくり動いていく", "3/4", 132, 0.6, "Bb",
      "Bbmaj7 | Gm9 | Cm9 | F7 | Dm7 | G7b9 | Cm9 | F7sus4",
      "Ebmaj7 | Ebm6 | Dm7 | G7 | Cm9 | F7 | Bbmaj7 | Cm7 F7",
      "waltz", "waltz", "piano", "waltz", "clarinet", "piano", "strings", "ジャズワルツ。旋律はクラリネット、ソロはクラリネットとピアノ。"),
    S("midnight-ballad", "真夜中のバラード", "Midnight Ballad", "閉店まぎわ。灯りを少し落とした店で、静かに流れる", "4/4", 62, 0.7, "Eb",
      "Ebmaj7 | Cm9 | Fm9 | Bb7 | Gm7 C7b9 | Fm7 Bb7 | Ebmaj7 Abmaj7 | Fm7 Bb7sus4",
      "Abmaj7 | Abm6 | Gm7 | C7alt | Fm9 | Bb7 | Ebmaj7 | Fm7 Bb7",
      "ballad", "ballad", "piano", "ballad", "tenorSax", "piano", "strings", "バラード。息まじりのテナーサックスとピアノ、うしろに弦。"),
    S("library-five", "本棚の五拍子", "Five Beats on the Bookshelf", "本を一冊ぬき出して、ページをゆっくりめくる", "5/4", 132, 0.55, "C",
      "Cm9 | Cm9 | Abmaj7#11 | Abmaj7#11 | Fm9 | Bb7sus4 | Ebmaj7 | G7alt",
      "Abmaj7 | Gm7 | Fm9 | Bbm7 Eb7 | Abmaj7 | Dm7b5 G7b9 | Cm9 | G7sus4",
      "five", "five", "piano", "five", "vibes", "piano", "strings", "5拍子（3＋2）のクール・ジャズ。ビブラフォンの旋律。"),
    S("lamp-mode", "ランプの灯るモード", "Modal Lamplight", "ランプの灯りが、木のテーブルにまるく落ちている", "4/4", 108, 0.6, "D",
      "Dm11 | Dm11 | Dm11 | Dm11 | Ebmaj7#11 | Ebmaj7#11 | Dm11 | Dm11",
      "Em11 | Em11 | Fmaj7#11 | Fmaj7#11 | Em11 | Em11 | Ebmaj7#11 | A7alt",
      "swing2", "walk", "piano", "modal", "jazzGuitar", "vibes", "strings", "ドリアンのモード・ジャズ。ピアノの和音、ジャズギターとビブラフォン。"),
    S("neosoul-sunlight", "ネオソウルの陽だまり", "Neo-Soul Sunlight", "窓ぎわのソファ。日だまりの中で、少しうとうと", "4/4", 80, 0.32, "Ab",
      "Abmaj9 | Dbmaj9 | Cm9 | Fm9 | Bbm9 | Eb9sus4 | Abmaj9 | Gm7 C7alt",
      "Dbmaj9 | Dbm6 | Cm9 | F13 | Bbm9 | Eb13 | Abmaj9 | Eb9sus4",
      "neosoul", "neosoul", "piano", "neosoul", "horn", "tenorSax", "strings", "ゆるく跳ねるネオソウル。ピアノの和音と、やわらかいホルンとテナーサックス。"),
    S("harbor-samba", "港のサンバ", "Harbor Samba", "港の見えるテラス。潮風がテーブルクロスをゆらす", "4/4", 104, 0.0, "G",
      "Gmaj7 | Gmaj7 | Am9 | D7 | Bm7 | E7b9 | Am9 | D7sus4",
      "Cmaj7 | Cm6 | Bm7 | E7 | Am9 | D7 | Gmaj7 E7b9 | Am7 D7",
      "samba", "samba", "nylon", "samba", "marimba", "piano", "strings", "ゆったりしたサンバ。マリンバの旋律と、ナイロン弦のギター。"),
    S("blue-monday", "ブルーな月曜日", "Blue Monday Blues", "雨の月曜日。カウンターで、ゆっくりコーヒーを飲む", "4/4", 84, 0.66, "F",
      "F7 | Bb7 | F7 | Cm7 F7 | Bb7 | Bdim7 | F7 | Am7b5 D7b9",
      "Gm7 | C7 | F7 D7b9 | Gm7 C7 | F7 | Bb7 | F7 | Gm7 C7",
      "shuffle", "walk", "piano", "swing", "jazzGuitar", "tenorSax", "strings", "スロー・ブルース。ピアノとテナーサックスが歌う。"),
    S("moonlit-bolero", "月夜のボレロ", "Moonlit Bolero", "月の光がさしこむ、古いレンガの店", "4/4", 92, 0.0, "E",
      "Em9 | Em9 | Am9 | Am9 | F#m7b5 | B7b9 | Em9 | Cmaj7 B7",
      "Gmaj7 | Gmaj7 | Am9 | D7 | Gmaj7 | Cmaj7 | F#m7b5 | B7alt",
      "bolero", "bolero", "nylon", "bolero", "violin", "nylon", "strings", "ラテンのボレロ。バイオリンの旋律と、ナイロン弦のギター。"),
    S("snow-window", "雪の窓", "Snow at the Window", "窓の外に、音もなく雪がふりつもる", "4/4", 96, 0.0, "A",
      "Amaj7 | B/A | Amaj7 | B/A | F#m9 | Dmaj7#11 | Amaj7 | E7sus4",
      "Dmaj7#11 | C#m7 | Bm9 | E7sus4 | Fmaj7#11 | Dmaj7 | C#m7 | E7sus4",
      "straight", "straight", "piano", "ecm", "viola", "piano", "strings", "まっすぐな8分の、北のジャズ。ピアノの広い和音とビオラ。"),
    S("afro-sixeight", "木もれ日の6/8", "Dappled Six-Eight", "大きな木の下のテラス。木もれ日が、ゆらゆら", "12/8", 72, 0.0, "G",
      "Gm9 | Gm9 | Cm9 | Cm9 | Ebmaj7 | D7alt | Gm9 | D7sus4",
      "Ebmaj7 | Ebmaj7 | Cm9 | Cm9 | Am7b5 | D7b9 | Gm9 | D7alt",
      "afro", "afro", "piano", "afro", "flute", "piano", "strings", "アフロ・キューバンの6/8（12/8）。ピアノのくり返しと、フルート。"),
    S("cobblestone-swing", "石畳のスウィング", "Cobblestone Swing", "石畳の路地。古い映画館のとなりのカフェ", "4/4", 132, 0.55, "A",
      "Am6 | Am6 | E7 | E7 | E7 | E7 | Am6 | Am6",
      "Dm6 | Dm6 | Am6 | Am6 | B7 | E7 | Am6 | E7",
      "pompe", "pompe", "jazzGuitar", "pompe", "accordion", "jazzGuitar", "none", "マヌーシュ・スウィング。ギターの刻み（ラ・ポンプ）と、アコーディオン。"),
    S("coffee-chacha", "コーヒー豆のチャチャ", "Coffee Bean Cha-Cha", "焙煎機の音。カップの中でゆれる、こげ茶色", "4/4", 112, 0.0, "C",
      "Cmaj7 | Am9 | Dm9 | G7 | Em7 | A7b9 | Dm9 | G7sus4",
      "Fmaj7 | Fm6 | Em7 | A7 | Dm9 | G7 | Cmaj7 A7b9 | Dm7 G7",
      "chacha", "tumbao", "piano", "montuno", "trombone", "piano", "strings", "チャチャチャ。ピアノのモントゥーノとトロンボーン。"),
    S("dusk-hardbop", "夕暮れのハードバップ", "Hard Bop at Dusk", "夕方のにぎわい。オレンジ色のランプがつく", "4/4", 126, 0.58, "F",
      "Fm9 | Fm9 | Bbm9 | Eb7 | Abmaj7 | Dbmaj7 | Gm7b5 | C7b9",
      "Abmaj7 | Am7 D7 | Gm7b5 | C7alt | Fm9 | Bbm7 Eb7 | Abmaj7 | G7alt C7b9",
      "swing3", "walk", "piano", "swing", "trumpet", "trombone", "none", "短調のハードバップ。トランペットとトロンボーンの2管でテーマ。", horns=True),
    S("nordic-lake", "北の湖", "Nordic Lake", "しんとした湖。水面に、白い空がうつる", "4/4", 70, 0.0, "B",
      "Bm9 | Gmaj7#11 | Em9 | F#7sus4 | Bm9 | Dmaj7 | Gmaj7#11 | F#7sus4",
      "Gmaj7 | A6 | Em9 | Bm9 | Gmaj7#11 | Em9 | Cmaj7#11 | F#7sus4",
      "brushballad", "ballad", "piano", "ecm", "piano", "cello", "strings", "北欧のジャズ・バラード。ピアノとチェロ、うしろに弦。"),
    S("guitar-trio", "窓ぎわのギター・トリオ", "Guitar Trio by the Window", "窓ぎわの席。ノートを開いて、ペンを走らせる", "4/4", 140, 0.55, "Bb",
      "Bbmaj7 | G7b9 | Cm9 | F7 | Dm7 | Db7 | Cm9 | F7",
      "Ebmaj7 | Ab7 | Dm7 | G7b9 | Cm9 | F7 | Bbmaj7 G7b9 | Cm7 F7",
      "brushes", "walk", "jazzGuitar", "swing", "jazzGuitar", "jazzGuitar", "strings", "ギター・トリオ。ブラシのドラムと、ジャズギターの旋律。"),
    S("stride-cafe", "古い喫茶店のピアノ", "Old Café Piano", "古い喫茶店の、すみに置かれたアップライト・ピアノ", "4/4", 100, 0.62, "C",
      "C6 | A7 | Dm7 | G7 | C6 | C7 | F6 | Fm6",
      "Em7 | A7 | Dm7 | G7 | C6 | A7b9 | Dm7 | G7",
      "stride", "stride", "piano", "stride", "piano", "piano", "strings", "ストライド風のソロ・ピアノに、ブラシとベースを少し。"),
    S("chamber-rain", "雨あがりの室内楽", "Chamber Jazz After the Rain", "雨があがって、木の床が少しひんやり", "4/4", 112, 0.58, "D",
      "Dmaj7 | Bm9 | Em9 | A7 | F#m7 | B7b9 | Em9 | A7sus4",
      "Gmaj7 | Gm6 | F#m7 | B7 | Em9 | A7 | Dmaj7 B7b9 | Em7 A7",
      "swing", "two", "pizz", "pizz", "oboe", "piano", "ensemble", "室内楽のジャズ。弦のピチカートが和音、オーボエの旋律。"),
    S("noir-fog", "霧の夜の探偵", "Foggy Noir", "霧の夜。窓の外を、帽子の人が通りすぎる", "4/4", 72, 0.7, "C",
      "Cm9 | Abmaj7 | Fm9 | G7alt | Cm9 | Dm7b5 G7b9 | Cm9 | Dm7b5 G7alt",
      "Ebmaj7 | Am7b5 D7b9 | Gm7 | C7b9 | Fm9 | Bb7 | Ebmaj7 | Dm7b5 G7alt",
      "ballad", "two", "piano", "ballad", "tenorSax", "clarinetLow", "strings", "フィルム・ノワール風のスロー・スウィング。テナーサックスと低いクラリネット。"),
    S("sunny-calypso", "日だまりのカリプソ", "Sunny Calypso", "日だまりのテラス。冷たいアイスコーヒー", "4/4", 116, 0.0, "G",
      "Gmaj7 | Em7 | Am7 | D7 | Gmaj7 | G7 | Cmaj7 | D7",
      "Cmaj7 | C#dim7 | Gmaj7 | E7 | Am7 | D7 | Gmaj7 | D7sus4",
      "calypso", "calypso", "piano", "calypso", "kalimba", "piano", "strings", "明るいカリプソ。カリンバの旋律と、はずむピアノ。"),
    S("mellow-funk", "夜ふけのメロウ・ファンク", "Mellow Late-Night Funk", "夜ふけのカフェ。デスクライトの下で、もう少しだけ", "4/4", 94, 0.0, "E",
      "Em9 | A13 | Em9 | A13 | Cmaj7 | B7alt | Em9 | A13",
      "Cmaj7 | Bm7 | Am9 | D9 | Gmaj7 | Cmaj7 | F#m7b5 | B7alt",
      "funk", "funk", "piano", "funk", "flute", "vibes", "strings", "メロウなジャズ・ファンク。ピアノの刻み、フルートとビブラフォン。"),
    S("duo-cello", "ふたりのデュオ", "Duo for Two", "向かいあった二人。言葉のかわりに、音で話す", "4/4", 76, 0.62, "D",
      "Dmaj7 | Em9 | F#m7 | B7b9 | Em9 | A7 | Dmaj7 | A7sus4",
      "Gmaj7 | Gm6 | F#m7 | B7alt | Em9 | A7 | F#m7 B7 | Em7 A7",
      "none", "none", "piano", "duo", "cello", "piano", "none", "ピアノとチェロのデュオ。ドラムとベースなしで、ピアノの左手が低音。"),
    S("gospel-sunday", "日曜日のゴスペル", "Sunday Gospel", "日曜日の朝。窓から教会の鐘が聞こえる", "12/8", 64, 0.0, "Ab",
      "Abmaj7 | Db/Ab | Abmaj7 | Fm9 | Bbm9 | Eb7sus4 | Abmaj7 | Eb7",
      "Dbmaj7 | Dbm6 | Cm7 | F7 | Bbm9 | Eb7 | Ab Fm7 | Bbm7 Eb7",
      "gospel", "gospel", "piano", "gospel", "piano", "tenorSax", "ensemble", "12/8 のゴスペル・バラード。ピアノとテナーサックス、うしろに弦の合奏。"),
    S("dawn-baiao", "夜明けのバイヨン", "Baião at Dawn", "夜明けの市場。パンの焼けるにおい", "4/4", 108, 0.0, "D",
      "D7 | D7 | C/D | C/D | D7 | G/D | A7sus4 | D7",
      "G | G | D | D | Em7 | A7 | D | A7sus4",
      "baiao", "baiao", "piano", "baiao", "accordion", "flute", "strings", "ブラジルのバイヨン。アコーディオンの旋律（ミクソリディアン）と、フルート。"),
]

# 2026-10-19 点数の試し: ナイロンギター（7.39→7.79）・エレピ・ギターの和音は点数を下げる（音源の質）。和音はピアノを基本にする（オルガンの2曲は残す）
COMP_OVERRIDE = {"rainy-bossa": "piano", "lamp-mode": "piano", "neosoul-sunlight": "piano", "moonlit-bolero": "piano", "cobblestone-swing": "piano",
                 "guitar-trio": "piano", "chamber-rain": "piano", "mellow-funk": "piano"}
for _s in SONGS:
    if _s["id"] in COMP_OVERRIDE: _s["comp"] = COMP_OVERRIDE[_s["id"]]

# ================================================================ 拍子
METER = {"4/4": dict(beats=4, sub=4, split=[2, 2]), "3/4": dict(beats=3, sub=4, split=[2, 1]), "5/4": dict(beats=5, sub=4, split=[3, 2]),
         "12/8": dict(beats=4, sub=3, split=[2, 2])}

# ================================================================ リズムの型（旋律）。1文字＝8分（12/8 は 3連の8分）。x 音の頭・- のばす・. 休み
CELLS = {
    "swing": ["x--x--x-", "x-------", "..x-x-x-", "x-x---x-", "x---x--x", ".x-x-x--", "x--x-x--", "x---..x-", "x-xx----", "..xx-x--"],
    "ballad": ["x---x---", "x-----x-", "..x-x---", "x-xxx---", "x-------", "...x---x", "x---..xx", "x-----.."],
    "bossa": ["x--x---x", "--x--x--", "x---x--x", "x-x---x-", "-x--x---", "x-------", "x--x--x-"],
    "latin": ["x-x-x-x-", "x--x--x-", ".x-x-x-x", "x-xx-x--", "x-------", "x--x-x--", "..x-x-x-"],
    "waltz": ["x--x-x", "x-----", "..x-x-", "x-x-x-", "x---x-", ".x-x--"],
    "five": ["x--x--x-x-", "x-----x---", "..x-x-x---", "x---x-x-x-", "x---------", "x--x--x---"],
    "afro": ["x--x--x--x--", "x-----x-----", "..x..x..x---", "x--x-x--x---", "x-----------", "x-x--x--x-x-"],
}
SOLO = {
    "4": ["xxxxxxxx", ".xxxxxx-", "x-xxxx-.", "xxxx-x..", "..xxxxxx", "x.xxx-x-", "xx-xxx--", "x---xxxx", "x-x-xxx-"],
    "3": ["xxxxxx", ".xxxx-", "x-xxx-", "xxxx--", "x-x-x-"],
    "5": ["xxxxxxxx--", "x-xxxx-xx-", ".xxxxxx---", "x-x-xxxx--"],
    "12": ["xxxxxx--x---", "x--xxxxxx---", "xxx--xxx--x-", "x-xx-xx-x---"],
    "ballad": ["x-xxx-x-", "xxxx----", ".x-xxx-x", "x---xx-x", "xx-x-x--"],
}
END = {"4": "x-------", "3": "x-----", "5": "x---------", "12": "x-----------"}

# ================================================================ 和音の楽器のリズム。1文字＝16分（12/8 は 3連の8分）。X 強く・x・o 弱く・- のばす・. 休み
COMPPAT = {
    "swing": [("x-----x-........", 3), ("......x-------..", 2), ("x---....x---....", 2), ("..x-------......", 1), ("x-------........", 2),
              ("....x-----..x---", 1), ("............x---", 1), ("x-----------....", 1)],
    "bossa": [("x-.x-.x-..x-.x-.", 1), ("..x-.x-.x-.x-.x-", 1)],
    "waltz": [("....x---x---", 3), ("x-------....", 1), ("....x-----x-", 2), ("......x-x---", 1)],
    "ballad": [("x---------------", 3), ("x-------x-------", 2), ("x-----------x---", 1)],
    "five": [("x-----x-....x---....", 2), ("......x-----x-------", 1), ("x-------....x-------", 1)],
    "modal": [("x-------........", 2), ("......x-------..", 2), ("..x-----........", 1), ("............x---", 1), ("x---------------", 1)],
    "neosoul": [("x-------.x------", 2), ("x-----x-.....x--", 1), ("x---------x-----", 2)],
    "samba": [("x-.x-.x-.x-.x-..", 1), (".x-.x-.x-.x-.x-.", 1)],
    "organ": [("x---------------", 2), ("x-------....x---", 1), ("......x---------", 1)],
    "bolero": [("x---..x-x---x---", 1)],
    "ecm": [("x---------------", 2), ("x-------x-------", 1)],
    "afro": [("x-.x-.x-.x-.", 1), ("x--x-.x--x-.", 1)],
    "pompe": [("o.-.X.-.o.-.X.-.", 1)],
    "montuno": [("x-.x-.x-..x-x-..", 1), (".x-.x-..x-.x-.x-", 1)],
    "calypso": [("x-.x-.x-x-.x-.x-", 1)],
    "funk": [("..x...x.x.....x.", 1), ("x.....x...x.x...", 1)],
    "duo": [("x-------x-------", 2), ("x---------------", 1), ("....x-------x---", 1)],
    "gospel": [("x--x--x--x--", 1), ("x-----x--x-x", 1)],
    "baiao": [("x--x--x-x--x--x-", 1)],
    "stride": [("....x---....x---", 1)],
    "pizz": [("x...x.......x...", 1), ("x.......x...x...", 1)],
}

# ================================================================ ドラムの型（1文字＝16分。12/8 は 3連の8分）
DR = {
    "swing": dict(ride="x...X.x.x...X.x.", hat="....x.......x...", kick="", snare="", ghost=0.22, bomb=0.06),
    "swing2": dict(ride="x...X.x.x...X.x.", hat="....x.......x...", kick="", snare="", ghost=0.12, bomb=0.03),
    "swing3": dict(ride="x...X.x.x...X.x.", hat="....x.......x...", kick="", snare="", ghost=0.32, bomb=0.12),
    "brushes": dict(ride="", hat="....x.......x...", kick="", snare="o.o.X.o.o.o.X.o.", ghost=0.0, bomb=0.03),
    "ballad": dict(ride="x.......x.......", hat="....x.......x...", kick="", snare="o...o.o.o...o.o.", ghost=0.0, bomb=0.0),
    "brushballad": dict(ride="", hat="....x.......x...", kick="o...............", snare="o.o.x.o.o.o.x.o.", ghost=0.0, bomb=0.0),
    "waltz": dict(ride="x...X.x.x...", hat="....x...x...", kick="o...........", snare="", ghost=0.18, bomb=0.0),
    "five": dict(ride="x...X.x.x...X...X.x.", hat="........x.......x...", kick="o...........o.......", snare="", ghost=0.15, bomb=0.0),
    "bossa": dict(ride="", hat="o.o.o.o.o.o.o.o.", kick="x.....x.x.....x.", snare=["x.....x.....x...", "....x.....x....."], ghost=0.0, bomb=0.0),
    "neosoul": dict(ride="", hat="o.x.o.x.o.x.o.x.", kick="X.....o...X..o..", snare="....X..o....X...", ghost=0.0, bomb=0.0),
    "samba": dict(ride="", hat="xoooxoooxoooxooo", kick="o.......x.......", snare="..o.x..o.o.x..o.", ghost=0.0, bomb=0.0),
    "shuffle": dict(ride="", hat="x.x.x.x.x.x.x.x.", kick="x.......x.......", snare="....X.......X...", ghost=0.1, bomb=0.0),
    "bolero": dict(ride="", hat="o.x.o.x.o.x.o.x.", kick="x.......x.......", snare="....x..x....x...", ghost=0.0, bomb=0.0),
    "straight": dict(ride="x.x.x.x.x.x.x.x.", hat="........x.......", kick="x.......o.......", snare="", ghost=0.08, bomb=0.0),
    "afro": dict(bell="x.x.xx.x.x.x", hat="...x.....x..", kick="x.....x.....", snare="", ghost=0.15, bomb=0.0),
    "pompe": dict(ride="", hat="....x.......x...", kick="", snare="....x.......x...", ghost=0.0, bomb=0.0),
    "chacha": dict(bell="x...x...x...x...", hat="x.x.x.x.x.x.x.x.", kick="x.......x.......", snare="............x.x.", ghost=0.0, bomb=0.0),
    "calypso": dict(ride="", hat="x.x.x.x.x.x.x.x.", kick="x.....x.x.......", snare="....x.......x...", ghost=0.0, bomb=0.0),
    "funk": dict(ride="", hat="xoxoxoxoxoxoxoxo", kick="X......x..X.....", snare="....X..o.o..X..o", ghost=0.0, bomb=0.0),
    "gospel": dict(ride="", hat="xooxooxooxoo", kick="x.....x.....", snare="...X.....X..", ghost=0.0, bomb=0.0),
    "baiao": dict(ride="", hat="xoxoxoxoxoxoxoxo", kick="x..x....x..x....", snare="....o.......o...", ghost=0.0, bomb=0.0),
    "stride": dict(ride="", hat="....x.......x...", kick="", snare="o.o.x.o.o.o.x.o.", ghost=0.0, bomb=0.0),
    "none": None,
}
DRUMMIX = {"kick": {"level": 0.55}, "snare": {"level": 0.6, "reverb": 0.12, "tune": 1}, "hat": {"level": 0.6, "pan": 0.25},
           "tom": {"spread": 0.5, "tune": -2}, "crash": {"level": 0.6, "pan": -0.25, "reverb": 0.22}}


# ================================================================ 組み立て
class Part:
    def __init__(self, base, role):
        self.base = dict(base); self.role = role; self.ev = []   # (開始の刻み, 長さの刻み, 音（数）か記号, 印)
    def add(self, s, d, m, mk=""):
        if d > 0: self.ev.append((int(s), int(d), m, mk))


def build(song, out):
    rng = random.Random("cafe-jazz-" + song["id"] + str(song.get("seed", "")))
    M = METER[song["meter"]]; beats, sub = M["beats"], M["sub"]; BT = beats * TPB; bpm = song["bpm"]
    bar_s = beats * 60 / bpm
    key = pcof(song["key"])
    triplet = sub == 3
    E8 = TPB // 3 if triplet else TPB // 2          # 旋律の1文字（8分）の刻み
    G = TPB // sub                                    # 和音・ドラムの1文字の刻み

    def parse_sec(txt):
        bars = []
        for b in txt.split("|"):
            chs = b.split(); spans = []
            if len(chs) == 1: spans = [(chord(chs[0]), 0, BT)]
            else:
                cut = M["split"][0] * TPB
                spans = [(chord(chs[0]), 0, cut), (chord(chs[1]), cut, BT - cut)]
            bars.append(spans)
        return bars
    A = parse_sec(song["A"]); B = parse_sec(song["B"])
    tonic = A[0][0][0]

    # ---- 形を決める（長さが 4分半前後になるように）
    def total_s(n_solo, out_bars): return (4 + 32 + n_solo * 8 + out_bars + 4) * bar_s + bar_s * 0.6
    best = None
    for out_bars in (32, 16):
        for n_solo in range(0, 21):
            t = total_s(n_solo, out_bars)
            score = abs(t - sum(TARGET) / 2) + (0 if TARGET[0] <= t <= TARGET[1] else 100) + (0 if n_solo >= 2 else 8)
            if best is None or score < best[0]: best = (score, n_solo, out_bars)
    _, n_solo, out_bars = best
    form = [("intro", A[4:8], None)]
    form += [("A", A, "head"), ("A2", A, "head"), ("B", B, "head"), ("A3", A, "head")]
    order = ["A", "A", "B", "A"]
    soloists = ["lead", "solo2"] if song["solo2"] != "none" else ["lead"]
    s2_left = song.get("s2blocks", 99)   # 2つ目の楽器がソロをとる区間（8小節）の数の上限
    for i in range(n_solo):
        sec = order[i % 4]; who = soloists[(i // 2) % len(soloists)] if n_solo > 2 else "lead"
        if who == "solo2":
            if s2_left <= 0: who = "lead"
            else: s2_left -= 1
        form.append(("S" + sec, A if sec == "A" else B, who))
    if out_bars == 32: form += [("A", A, "head"), ("A2", A, "head"), ("B", B, "head"), ("A3", A, "head")]
    else: form += [("B", B, "head"), ("A3", A, "head")]
    tonic_name = song["A"].split("|")[0].split()[0]
    out_spans = [[(chord(tonic_name), 0, BT)] for _ in range(4)]
    form.append(("outro", out_spans, "outro"))

    bars = []; bar_info = []   # 小節ごとの (区間の名前, 誰が旋律か, 区間の中の小節番号)
    for name, sec, who in form:
        L = len(sec) if name != "intro" else 4
        for i in range(L):
            bars.append(sec[i]); bar_info.append((name, who, i))
    NB = len(bars); TU = NB * BT

    def ch_at(t):
        b = min(NB - 1, max(0, t // BT)); r = t - b * BT
        for c, s0, d in bars[b]:
            if s0 <= r < s0 + d: return c
        return bars[b][-1][0]

    # ---- 楽器
    lb, (llo, lhi) = INST[song["lead"]]
    if song.get("oldfeel") and song["lead"] == "piano": lb = dict(lb, reverb=0.3, sustain=1.3); llo, lhi = 60, 86
    P = {"lead": Part(lb, f"旋律（{song['lead']}）")}
    comp_name = song["comp"]; cb, clo, chi, cpan = COMP[comp_name]
    if song.get("oldfeel") and comp_name == "piano": cb = dict(cb, reverb=0.3, sustain=1.0)
    P["comp"] = [Part(cb, f"和音（{comp_name}・{i + 1}）") for i in range(4)]
    s2 = song["solo2"]
    if s2 != "none" and s2 != song["lead"]:
        b2, (lo2, hi2) = INST[s2]
        P["solo2"] = Part(b2, f"ソロ（{s2}）")
    else: lo2, hi2 = llo, lhi
    if song["pad"] != "none":
        pb = dict(PADS[song["pad"]])
        if not song.get("oldpad"): pb.update(reverb=0.72, attack=max(pb.get("attack", 0.6), 0.9), release=1.8)
        P["pad"] = [Part(pb, f"うしろの和音（{song['pad']}・{i + 1}）") for i in range(5)]   # 2026-10-19 人間「奥行き・スケール・余韻」
    if song["bass"] != "none":
        if song["bass"] == "stride": P["bass"] = Part(dict(INST["piano"][0], volume=0.12, bright=-0.4), "左手の低音（ピアノ）")
        else: P["bass"] = Part(dict(instrument="bass", amp="jazz", volume=0.22, reverb=0.03, release=0.15, bright=-0.45, attack=0.01, duck=0.3,
                                     fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -6}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.02, "release": 0.2}]), "ベース")
            # 2026-10-19 点数の試し（『朝のエスプレッソ』）: ベースの出だしをやわらかく 7.88→7.89、書き出しを --bass finger（指弾きの録音）に 8.11（いちばん効いた）
    if song["cstyle"] == "duo": P["bass"] = Part(dict(INST["piano"][0], volume=0.11, bright=-0.45), "左手の低音（ピアノ）")
    if song.get("horns"): P["harm"] = Part(INST["trombone"][0], "テーマの2声目（トロンボーン）")

    # ================= 旋律
    def colors(c):
        r = c["r"]; q = c["q"]; out = [c["third"], c["tones"][2] if len(c["tones"]) > 2 else (r + 7) % 12]
        if len(c["tones"]) > 3: out.append(c["tones"][3])
        if q in ("7b9",): out.append((r + 1) % 12)
        elif q == "7alt": out += [(r + 3) % 12, (r + 8) % 12]
        elif q != "dim7": out.append((r + 2) % 12)
        if q in ("6", "m6"): out.append((r + 9) % 12)
        return list(dict.fromkeys(out))

    def onsets_of(cellstr, t0):
        res = []; cur = None
        for i, ch in enumerate(cellstr):
            t = t0 + i * E8
            if ch == "x":
                if cur: res.append(cur)
                cur = [t, E8]
            elif ch == "-" and cur: cur[1] += E8
            else:
                if cur: res.append(cur); cur = None
        if cur: res.append(cur)
        return res

    def pick(c_at_t, strong, prev, goal, lo, hi, r2, last_iv):
        c = c_at_t
        pool = colors(c) if strong else c["scale"]
        cand = [x for x in range(lo, hi + 1) if x % 12 in pool]
        def cost(x):
            iv = x - prev
            k = abs(iv) * (0.9 if strong else 1.3) + abs(x - goal) * 0.35 + r2.random() * 2.2
            if iv == 0: k += 2.5
            if abs(last_iv) > 4 and iv * last_iv > 0: k += 3      # 跳んだあとは反対向きへ
            if abs(iv) > 7: k += 6
            if x % 12 == c["r"] and strong and c["q"] not in ("6", "m6", "maj"): k += 1.2   # 根音より 3度・7度・9度
            return k
        return min(cand, key=cost)

    def anticip(t, d):
        # 小節の最後の8分から次の小節へのびる音は、次の和音で選ぶ
        r = t % BT
        return ch_at(t + d) if (r >= BT - E8 and d > E8) else ch_at(t)

    def line(onsets, lo, hi, center, r2, arch=5, end_tonic=False):
        notes = []; prev = center; last_iv = 0; n = len(onsets)
        for i, (t, d) in enumerate(onsets):
            c = anticip(t, d)
            strong = t % (2 * TPB) == 0 or d >= TPB or i == 0
            goal = center + arch * math.sin(math.pi * (i + 0.5) / max(1, n))
            m = pick(c, strong, prev, goal, lo, hi, r2, last_iv)
            if end_tonic and i == n - 1:
                tc = [x for x in range(lo, hi + 1) if x % 12 in (c["r"], c["third"], (c["r"] + 7) % 12)]
                m = min(tc, key=lambda x: abs(x - prev))
            notes.append((t, d, m)); last_iv = m - prev; prev = m
        return notes

    def snap(x, c, strong, lo, hi):
        pool = colors(c) if strong else c["scale"]
        cand = [y for y in range(lo - 2, hi + 3) if y % 12 in pool]
        y = min(cand, key=lambda y: (abs(y - x), y))
        while y > hi: y -= 12
        while y < lo: y += 12
        return y

    bpb = len(END["12" if triplet else str(beats)])
    feel = song["cstyle"]
    vocab = CELLS["ballad" if feel in ("ballad", "ecm", "duo", "gospel") and not triplet else
                  "afro" if triplet else "waltz" if beats == 3 else "five" if beats == 5 else
                  "bossa" if feel in ("bossa", "neosoul") else "latin" if feel in ("samba", "montuno", "calypso", "baiao", "bolero", "funk", "afro") else "swing"]
    endc = END["12" if triplet else str(beats)]

    def head_section(sec_bars_start, lo, hi, center, seed, kind):
        """8小節の旋律。kind: A（動機→くり返し→展開）・A2（A の最後2小節を変える）・B（新しい形、少し高く）"""
        r2 = random.Random(song["id"] + str(song.get("seed", "")) + seed)
        if kind == "B": center += (3 if song.get("oldfeel") else 5)
        c1, c2 = r2.choice(vocab), r2.choice(vocab)
        c5, c6, c7 = r2.choice(vocab), r2.choice(vocab), r2.choice(vocab)
        if c2.endswith("-") or c2.endswith("x"): c2 = c2[:-2] + ".."      # 4小節目の終わりは息つぎ
        cells = [c1, c2, c1, c2, c5, c6, c7, endc]
        t0 = sec_bars_start * BT
        on12 = onsets_of(c1 + c2, t0)
        n12 = line(on12, lo, hi, center, r2)
        # 3〜4小節目: 1〜2小節目の動機を、新しい和音へ移す（形はそのまま）
        n34 = []
        if n12:
            first = n12[0]; c = anticip(first[0] + 2 * BT, first[1])
            shift = snap(first[2], c, True, lo, hi) - first[2]
            for (t, d, m) in n12:
                c = anticip(t + 2 * BT, d); strong = (t % (2 * TPB) == 0) or d >= TPB
                n34.append((t + 2 * BT, d, snap(m + shift, c, strong, lo, hi)))
        on58 = onsets_of(c5 + c6 + c7 + endc, t0 + 4 * BT)
        n58 = line(on58, lo, hi, center + 2, r2, arch=6, end_tonic=True)
        return n12 + n34 + n58

    def solo_section(sec_bars_start, lo, hi, center, seed):
        r2 = random.Random(song["id"] + str(song.get("seed", "")) + "solo" + seed)
        sv = SOLO["ballad" if feel in ("ballad", "ecm", "duo") and not triplet else "12" if triplet else str(beats)]
        if song.get("calm_solo"):   # ソロも、テーマのようにゆったり（細かい音を減らす）
            sv = vocab
        cells = []
        for b in range(8):
            c = r2.choice(sv)
            if b % 2 == 1: c = c[:-2] + ".."             # 2小節ごとに息つぎ
            if b == 7: c = endc[:len(endc) // 2] + "." * (len(endc) - len(endc) // 2)
            cells.append(c)
        on = onsets_of("".join(cells), sec_bars_start * BT)
        # 旋律の線は2小節ずつ、中心を少しずつ動かす
        out = []; prev_c = center
        for k in range(4):
            seg = [o for o in on if (sec_bars_start + 2 * k) * BT <= o[0] < (sec_bars_start + 2 * k + 2) * BT]
            cen = center + [0, 3, 5, 1][k] + r2.randint(-2, 2)
            out += line(seg, lo, hi, cen, r2, arch=4)
        return out

    lmid = (llo + lhi) // 2
    # 後テーマの始まりの小節
    out_head_start = None; bb = 0; seen_head = 0
    for (nm_, sc_, w_) in form:
        if w_ == "head" and nm_ == "A":
            seen_head += 1
            if seen_head == 2: out_head_start = bb
        bb += 4 if nm_ == "intro" else len(sc_)
    LEAD = []; S2 = []
    b0 = 0; cache = {}
    for name, sec, who in form:
        L = 4 if name == "intro" else len(sec)
        if who == "head":
            kind = {"A": "A", "A2": "A2", "B": "B", "A3": "A3"}[name]
            key_ = "B" if kind == "B" else "A"
            if key_ not in cache: cache[key_] = (b0, head_section(b0, llo, lhi, lmid, key_, key_))
            sb, notes = cache[key_]
            mv = [(t + (b0 - sb) * BT, d, m) for (t, d, m) in notes]
            if kind in ("A2", "A3"):
                r3 = random.Random(song["id"] + str(song.get("seed", "")) + kind)
                keep = [x for x in mv if x[0] < (b0 + 6) * BT]
                tail = onsets_of(r3.choice(vocab) + endc, (b0 + 6) * BT)
                prevm = keep[-1][2] if keep else lmid
                tl = line(tail, llo, lhi, prevm, r3, arch=2, end_tonic=True)
                mv = keep + tl
            # 後テーマの最初の A は、2つ目の楽器が吹く（同じ旋律を同じ音でくり返さない）
            if out_head_start is not None and b0 == out_head_start and song["solo2"] not in ("none", song["lead"]) and song.get("s2head", True):
                mv2 = []
                for (t, d, m) in mv:
                    while m > hi2: m -= 12
                    while m < lo2: m += 12
                    mv2.append((t, d, m))
                S2 += mv2
            else:
                LEAD += mv
        elif who in ("lead", "solo2"):
            lo, hi = (llo, lhi) if who == "lead" else (lo2, hi2)
            sn = solo_section(b0, lo, hi, (lo + hi) // 2, f"{b0}")
            (LEAD if who == "lead" else S2).extend(sn)
        elif who == "outro":
            r4 = random.Random(song["id"] + str(song.get("seed", "")) + "outro")
            tag = onsets_of(r4.choice(vocab) + endc[:2] + "-" * (len(endc) - 2) + endc.replace("x", "-"), b0 * BT)
            prevm = LEAD[-1][2] if LEAD else lmid
            tg = line(tag, llo, lhi, prevm, r4, arch=2, end_tonic=True)
            if tg:   # 最後の音は、終わりまでのばす
                t, d, m = tg[-1]; tg[-1] = (t, TU - t, m)
            LEAD += tg
        b0 += L
    for (t, d, m) in LEAD: P["lead"].add(t, d, m, "~." if d >= 2 * TPB and song["lead"] not in ("jazzGuitar", "piano", "marimba", "kalimba", "vibes") else "")
    if song.get("double") and song["lead"] != "piano":   # 旋律をピアノで小さく重ねる（音の芯）
        P["dbl"] = Part(dict(INST["piano"][0], volume=0.2), "旋律の重ね（ピアノ）")
        for (t, d, m) in LEAD:
            mm = m
            while mm > 84: mm -= 12
            while mm < 60: mm += 12
            P["dbl"].add(t, d, mm)
    tgt2 = P.get("solo2")
    s2_is_comp = (s2 == comp_name) or (s2 == "piano" and comp_name == "piano")
    solo2_bars = set()
    if S2:
        for (t, d, m) in S2:
            solo2_bars.add(t // BT)
            if tgt2: tgt2.add(t, d, m)
            else: P["lead"].add(t, d, m)   # 同じ楽器なら同じパートで
        if not tgt2 and s2_is_comp and song["lead"] != s2:
            pass
    # ピアノがソロをとるとき、和音はピアノの「左手」だけ（2声・低め）
    piano_solo_bars = set(); 
    if s2 == "piano" and comp_name == "piano": piano_solo_bars = solo2_bars
    if song["lead"] == "piano" and comp_name == "piano":
        piano_solo_bars = {t // BT for (t, d, m) in LEAD}

    # テーマの2声目（2管）
    if "harm" in P:
        for (t, d, m) in LEAD:
            bi = t // BT
            if bar_info[bi][1] != "head": continue
            c = anticip(t, d)
            cand = [x for x in range(46, 71) if x % 12 in colors(c) and 3 <= m - x <= 9]
            if cand: P["harm"].add(t, d, max(cand))

    # ================= 和音
    pats = COMPPAT[feel]
    prev = None; prevpad = None
    for bi in range(NB):
        name, who, i = bar_info[bi]
        if name == "outro" and i >= 1:
            if i == 1:
                c = bars[bi][0][0]; v = voicing([x for x in c["voice"]], prev, clo, chi)
                for k in range(4): P["comp"][k].add(bi * BT, TU - bi * BT, v[k])
            continue
        # パターンを選ぶ（2小節で1組のものは、小節の偶奇で）
        if len(pats) == 2 and all(w == 1 for _, w in pats): pat = pats[bi % 2][0]
        else: pat = rng.choices([p for p, _ in pats], weights=[w for _, w in pats])[0]
        cur = None; evs = []
        for j, chx in enumerate(pat):
            t = bi * BT + j * G
            if chx in "xXo":
                if cur: evs.append(cur)
                cur = [t, G, chx]
            elif chx == "-" and cur: cur[1] += G
            else:
                if cur: evs.append(cur); cur = None
        if cur: evs.append(cur)
        for (t, d, chx) in evs:
            c = ch_at(t + d - 1) if (t % BT) >= BT - TPB // 2 and d > TPB // 2 else ch_at(t)
            v = voicing(c["voice"], prev, clo, chi); prev = v
            mk = "!" if chx == "X" else "," if chx == "o" else ""
            lh = bi in piano_solo_bars
            for k in range(4):
                if lh and k >= 2: continue
                m = v[k] - (5 if lh and v[k] > 60 else 0)
                if lh: m = snap(m, c, True, 48, 62)
                P["comp"][k].add(t, d, m, mk)
        # うしろの和音: 小節の頭から、和音ごとにのばす
        if "pad" in P and not (song.get("oldfeel") and name == "intro"):
            for (c, s0, d) in bars[bi]:
                pcs = [c["third"], c["tones"][3] if len(c["tones"]) > 3 else (c["r"] + 7) % 12, (c["r"] + 2) % 12 if c["q"] not in ("7b9", "dim7", "7alt") else c["tones"][2]]
                want = list(dict.fromkeys(pcs))
                while len(want) < 3: want.append(c["tones"][1 if len(want) == 1 else 2])
                best = None
                for perm in itertools.permutations(want[:3]):
                    cand = []
                    for k, p in enumerate(perm):
                        ref = prevpad[k] if prevpad else 64 + k * 4
                        cand.append(min((x for x in range(60, 80) if x % 12 == p), key=lambda x: abs(x - ref)))
                    if len(set(cand)) < 3: continue
                    cost = sum(abs(a - b) for a, b in zip(cand, prevpad)) if prevpad else 0
                    if best is None or cost < best[0]: best = (cost, cand)
                pv = best[1] if best else [64, 67, 71]; prevpad = pv
                dd = d if name != "outro" else TU - (bi * BT + s0)
                for k in range(3): P["pad"][k].add(bi * BT + s0, dd, pv[k])
                # 低い声（根音・5度、C2〜E3）と高い声（9度か5度、E5〜C6）で、上下に広げる
                lowp = c["bass"] if (bi + s0) % 2 == 0 else c["r"]
                if song.get("oldpad"): continue
                P["pad"][3].add(bi * BT + s0, dd, min((x for x in range(40, 53) if x % 12 == lowp), key=lambda x: abs(x - 45)))
                hp = (c["r"] + 2) % 12 if c["q"] not in ("7b9", "dim7", "7alt", "m7b5") else c["tones"][2]
                P["pad"][4].add(bi * BT + s0, dd, min((x for x in range(76, 89) if x % 12 == hp), key=lambda x: abs(x - 81)))

    # ================= ベース
    bstyle = song["bass"] if song["cstyle"] != "duo" else "duo"
    BLO, BHI = (28, 50) if bstyle not in ("stride", "duo") else (36, 55)
    def bnote(pc_, ref):
        return min((x for x in range(BLO, BHI + 1) if x % 12 == pc_), key=lambda x: abs(x - ref))
    BPAT = {   # (拍, 長さ, 何の音) R=根音 5=5度 3=3度 7=7度 O=オクターブ上 A=次の根音への半音
        "bossa": [(0, 1.5, "R"), (1.5, 0.5, "5"), (2, 1.5, "5"), (3.5, 0.5, "R")],
        "samba": [(0, 0.75, "R"), (1.5, 0.5, "5"), (2, 0.75, "R"), (3.5, 0.5, "5")],
        "bolero": [(0, 2, "R"), (2, 1, "5"), (3.5, 0.5, "5")],
        "straight": [(0, 2, "R"), (2, 2, "5")],
        "neosoul": [(0, 1.25, "R"), (1.5, 1, "5"), (2.75, 0.75, "7"), (3.5, 0.5, "A")],
        "tumbao": [(1.5, 1.5, "R"), (3, 1, "5")],
        "calypso": [(0, 1, "R"), (1.5, 0.5, "R"), (2, 1, "5"), (3, 0.5, "3"), (3.5, 0.5, "5")],
        "funk": [(0, 0.5, "R"), (0.75, 0.25, "R"), (1.5, 0.25, "7"), (2, 0.5, "R"), (2.75, 0.5, "5"), (3.5, 0.25, "O"), (3.75, 0.25, "A")],
        "baiao": [(0, 0.75, "R"), (0.75, 1.25, "5"), (2, 0.75, "R"), (2.75, 1.25, "5")],
        "stride": [(0, 1, "R"), (2, 1, "5")],
        "duo": [(0, 2, "R"), (2, 2, "5")],
        "pompe": [(0, 1, "R"), (2, 1, "5")],
        "two": [(0, 2, "R"), (2, 2, "5")],
        "ballad": [(0, 2, "R"), (2, 1.5, "5"), (3.5, 0.5, "A")],
        "afro": [(0, 2 / 3, "R"), (4 / 3, 2 / 3, "5"), (2, 1, "R"), (10 / 3, 2 / 3, "5")],
        "gospel": [(0, 2, "R"), (2, 1, "3"), (3, 2 / 3, "5"), (11 / 3, 1 / 3, "A")],
        "five": [(0, 1.5, "R"), (1.5, 1.5, "5"), (3, 1, "R"), (4, 1, "A")],
        "waltz": [(0, 3, "R")],
    }
    if "bass" in P:
        prevb = 36 if BLO < 36 else 43
        for bi in range(NB):
            name, who, i = bar_info[bi]
            if name == "outro" and i >= 1:
                if i == 1: P["bass"].add(bi * BT, TU - bi * BT, bnote(tonic["r"], prevb))
                continue
            soloing = who in ("lead", "solo2")
            walk = bstyle == "walk" or (bstyle in ("two", "pompe", "waltz") and soloing)
            nxt = ch_at((bi + 1) * BT) if bi + 1 < NB else tonic
            if walk:
                n = beats
                for k in range(n):
                    t = bi * BT + k * TPB; c = ch_at(t)
                    chord_change_next = ch_at(t + TPB)["name"] != c["name"] or k == n - 1
                    tgt_next = ch_at(t + TPB) if k < n - 1 else nxt
                    if k == 0 or ch_at(t - 1)["name"] != c["name"]:
                        m = bnote(c["bass"], prevb)
                    elif chord_change_next:
                        rt = bnote(tgt_next["bass"], prevb)
                        m = rt + rng.choice([-1, 1, -1]) if rng.random() < 0.7 else bnote((tgt_next["r"] + 7) % 12, rt)
                        m = max(BLO, min(BHI, m))
                    else:
                        pool = [x for x in range(BLO, BHI + 1) if x % 12 in c["tones"] or (x % 12 in c["scale"] and rng.random() < 0.3)]
                        cand = sorted(pool, key=lambda x: abs(x - prevb) + (3 if x == prevb else 0) + rng.random() * 3)
                        m = cand[0]
                    P["bass"].add(t, TPB, m, "" if k % 2 == 0 else ","); prevb = m
            else:
                pat = BPAT.get(bstyle, BPAT["two"])
                if beats == 3 and bstyle != "waltz": pat = BPAT["waltz"]
                for (bt, dl, what) in pat:
                    t = bi * BT + int(round(bt * TPB)); d = int(round(dl * TPB))
                    if bt >= beats: continue
                    d = min(d, (bi + 1) * BT - t)
                    c = ch_at(t)
                    if what == "R": pc_ = c["bass"]
                    elif what == "5": pc_ = (c["r"] + 7) % 12 if c["q"] not in ("m7b5", "dim7") else (c["r"] + 6) % 12
                    elif what == "3": pc_ = c["third"]
                    elif what == "7": pc_ = c["tones"][3] if len(c["tones"]) > 3 else c["r"]
                    elif what == "O": pc_ = c["r"]
                    else:
                        pc_ = (nxt["bass"] + rng.choice([-1, 1])) % 12
                    m = bnote(pc_, prevb if what != "O" else prevb + 12)
                    P["bass"].add(t, d, m); prevb = m

    # ================= ドラム
    dsty = DR.get(song["drums"])
    D = {}
    if dsty:
        dvol = song.get("dvol", 1.0)
        D["kick"] = Part(dict(instrument="kick", volume=round(0.08 * dvol, 3)), "キック")   # 2026-10-19 試し: キックを半分＋ベースを凹ませると +0.14（ベースとキックのぶつかり）
        D["snare"] = Part(dict(instrument="snare", volume=round(0.12 * dvol, 3)), "スネア（ブラシのつもり）")
        D["hat"] = Part(dict(instrument="hihat", volume=round(0.07 * dvol, 3)), "ハイハット")
        D["ride"] = Part(dict(instrument="crash", volume=round(0.055 * dvol, 3)), "ライド")
        D["crash"] = Part(dict(instrument="crash", volume=round(0.045 * dvol, 3)), "シンバル（区切り）")
        D["tom"] = Part(dict(instrument="tom", volume=round(0.1 * dvol, 3), reverb=0.2), "タム・フロアタム（フィル）")
        has_ride = bool(dsty.get("ride"))
        BRUSH_SN = ("o.o.x.o.o.o.x.o." + "o.o.x.o.")[:BT // G] if not triplet else "o.ox.oo.ox.o"
        # 単調にしない（2026-10-19 人間「単調な感じはなるべく少なく」）: はじめのテーマの A は軽く（ライドの曲はブラシ、
        #   ほかの曲はスネアなし）→ A2 から本来の型へ。区間の終わりのフィルは、タム（高→低のフロアタム）とスネアを交互に
        sec_count = [0]
        for bi in range(NB):
            name, who, i = bar_info[bi]
            if bi == 4 + 32 and who in ("lead", "solo2"): D["crash"].add(bi * BT, 2 * BT, "x", "")   # ソロの入り
            if name == "outro" and i >= 1:
                if i == 1: D["crash"].add(bi * BT, 3 * BT, "x", ",")
                continue
            t0 = bi * BT; L = BT // G
            if name == "intro" and i < 2 and song.get("quietintro"):
                if i == 1: D["crash"].add(t0 + BT - TPB, TPB, "x", ",")
                continue
            last_of_sec = (i == 7) and name != "intro"
            intro_light = name == "intro"
            first_A = bi < 4 + 32 and name == "A" and not song.get("nobrushA")
            if first_A and has_ride:   # はじめの A: ライドを休み、ブラシの円とハイハット
                dsty_b = dict(dsty, ride="", snare=BRUSH_SN, ghost=0.0)
            elif first_A and song.get("thinA"): dsty_b = dict(dsty, snare="", ghost=0.0)
            else: dsty_b = dsty
            if song.get("hat2ride") and not first_A:   # ハイハットの刻みをライドに（点数の試しでライドが効く。2026-10-19）
                hp_ = dsty_b.get("hat", "")
                if isinstance(hp_, str) and hp_:
                    rp_ = "".join("x" if ch in "xX" else ("x" if ch in "oO" and k_ % 2 == 0 else ".") for k_, ch in enumerate(hp_))
                    dsty_b = dict(dsty_b, ride=rp_, hat=("....x.......x..." if len(hp_) == 16 else ""))
            def grid(pat, inst, tok="x"):
                if not pat: return
                if isinstance(pat, list): pat = pat[bi % len(pat)]
                for j, ch in enumerate(pat[:L]):
                    if ch in "xXoO":
                        # ライドは次に叩くまで鳴らしつづける（2026-10-19、人間「ライドの鳴りをもう少し伸ばして鋭く」）
                        if inst == "ride": D["ride"].add(t0 + j * G, 4 * TPB, "D#3", "!" if ch == "X" else "," if ch == "o" else "")
                        elif inst == "bell": D["ride"].add(t0 + j * G, 4 * TPB, "F3", "!" if ch == "X" else "," if ch == "o" else "")
                        else: D[inst].add(t0 + j * G, G, ch.lower() if ch != "O" else "O", "!" if ch == "X" else "," if ch == "o" else "")
            grid(dsty_b.get("ride", ""), "ride"); grid(dsty_b.get("bell", ""), "bell"); grid(dsty_b.get("hat", ""), "hat")
            grid(dsty_b.get("kick", ""), "kick")
            sn = dsty_b.get("snare", "")
            if last_of_sec and not intro_light:   # 区間の終わりに、小さなフィル
                base = (sn[bi % len(sn)] if isinstance(sn, list) else sn) or "." * L
                nfill = sec_count[0] % 3; sec_count[0] += 1
                per = L // beats
                if nfill == 0:   # スネアの1拍
                    fill = "o" * per if not triplet else "oox"; sn = base[:L - len(fill)] + fill
                else:            # タム → フロアタム（1拍、ときどき2拍）
                    nb_ = 2 if (nfill == 2 and beats >= 4) else 1
                    sn = base[:L - per * nb_] + "." * (per * nb_)
                    pitches = ["C4", "A3", "F3", "D3", "C4", "B3", "G3", "A2"] if nb_ == 2 else ["B3", "G3", "D3", "A2"]
                    step = (per * nb_) // len(pitches) or 1
                    for q_, pn in enumerate(pitches[:per * nb_]):
                        D["tom"].add(t0 + (L - per * nb_ + q_ * step) * G, step * G, pn, "!" if q_ == len(pitches) - 1 else "")
            grid(sn, "snare")
            for j in range(L):   # ゴースト（合いの手）と、まれなキック
                if j % (2 if triplet else 2) == (0 if triplet else 2 % 2) and j % (sub) != 0 and rng.random() < dsty.get("ghost", 0):
                    D["snare"].add(t0 + j * G, G, "o", ",")
            if rng.random() < dsty.get("bomb", 0): D["kick"].add(t0 + (L - 2) * G, G, "x", ",")
            # ときどきアクセント（2026-10-19 人間「ドラムはたまにアクセントも」）: 裏拍にスネアとキックを強く＋シンバルを短く鳴らす。
            #   はじめの A・イントロ・終わりでは入れず、テーマの B・後テーマ・ソロの盛り上がりで、4小節に1回くらい
            if not song.get("noaccent") and not first_A and name not in ("intro", "outro") and not last_of_sec and rng.random() < (0.3 if name in ("B", "SB") else 0.18):
                per = L // beats; spot = rng.choice([b_ for b_ in range(1, beats)])
                j_ = spot * per - (per // 2 if not triplet else 1)   # 拍の前の裏
                D["snare"].add(t0 + j_ * G, G, "x", "!"); D["kick"].add(t0 + j_ * G, G, "x", "")
                D["crash"].add(t0 + j_ * G, 2 * TPB, "x", "")
            if i == 0 and who == "head" and bi > 4: D["crash"].add(t0, 2 * BT, "x", ",")

    # ================= ブレイク（はじめのテーマの最後の小節は、全員が1拍目で止まり、旋律だけが残る → ソロへ）と、
    #   ソロのはじめの8小節は、うしろの弦が抜ける（楽器の出入り）
    def cut_bar(parts_, b, keep=TPB):
        lo, hi = b * BT, (b + 1) * BT
        for p_ in parts_:
            nev = []
            for (s_, d_, m_, mk_) in p_.ev:
                if lo < s_ < hi: continue
                if s_ == lo and d_ > keep and p_ is not D.get("crash"): d_ = keep
                if s_ < lo < s_ + d_ and p_ is not D.get("crash"): d_ = lo - s_
                nev.append((s_, d_, m_, mk_))
            p_.ev = nev
    if NB > 4 + 32 + 8 and bar_info[4 + 32][1] in ("lead", "solo2") and not song.get("nobreak"):
        brk = 4 + 32 - 1
        cut_bar(list(P["comp"]) + ([P["bass"]] if "bass" in P else []) + [D[k] for k in D], brk)
        if D: D["crash"].add(brk * BT, 2 * TPB, "x", ",")
        if "pad" in P and n_solo >= 3 and not song.get("nopadout"):
            for b in range(4 + 32, 4 + 32 + 8): cut_bar(P["pad"], b, keep=0)
            for p_ in P["pad"]: p_.ev = [e for e in p_.ev if not (e[1] <= 0)]

    # ================= 強弱（小節ごと）: 曲全体で大きな山を作る（2026-10-19 人間「強弱を」）
    #   イントロ（小さく始めて上げる）→ テーマ A（控えめ）→ B（盛り上げる）→ ソロ（少しずつ上げる）→ 後テーマの B が頂点 → 終わり（静かに消える）
    lvl = []; n_s = sum(1 for (_, w_, _) in bar_info if w_ in ("lead", "solo2")); k_s = 0; heads_seen_ = 0
    for (name, who, i) in bar_info:
        if name == "intro": g = 0.8 + 0.03 * i   # 試し（2026-10-19）: 静かすぎるイントロは点数が下がる（0.6→0.8）
        elif name == "outro": g = 0.82 - 0.08 * i
        elif who in ("lead", "solo2"):
            g = 0.84 + 0.14 * (k_s / max(1, n_s - 1)); k_s += 1
        elif name == "B": g = 0.92 + 0.012 * i + (0.06 if k_s > 0 else 0)
        elif name == "A3": g = 0.96 - 0.012 * i if k_s > 0 else 0.86
        elif name == "A2": g = 0.84
        else: g = 0.8 if k_s == 0 else 0.9
        lvl.append(g)
    if song.get("arc", 1.0) != 1.0:   # 強弱の幅（1＝そのまま、0.5＝半分）
        lvl = [round(0.92 + song["arc"] * (g - 0.92), 3) for g in lvl]
    gain = [round(sum(lvl[max(0, k - 1):k + 2]) / len(lvl[max(0, k - 1):k + 2]), 3) for k in range(NB)]
    gain_pad = [round(min(1.15, 0.55 + 0.6 * (g - 0.55)), 3) for g in gain]          # うしろの弦は、ソロで引き、盛り上がりでふくらむ
    gain_pad = [round(gp * (0.82 if bar_info[k][1] in ("lead", "solo2") else 1.0), 3) for k, gp in enumerate(gain_pad)]
    gain_dr = [round(max(0.3, 1.0 + 1.6 * (g - 0.9)), 3) for g in gain]               # ドラムは差を大きく

    # ================= 書き出し
    parts = []
    def rest(u):
        out = []
        while u > 0:
            d = min(u, 8 * TPB); out.append(f"R:{fmt(d / TPB)}"); u -= d
        return out
    def emit(p, drum=False):
        ev = sorted(p.ev, key=lambda e: (e[0], -e[1])); toks = []; t = 0
        if not ev: return
        for k, (s, d, m, mk) in enumerate(ev):
            if s < t: continue
            nx = next((e[0] for e in ev[k + 1:] if e[0] > s), None)
            if nx is not None and s + d > nx: d = nx - s
            if d <= 0: continue
            if s > t: toks += rest(s - t)
            name_ = m if isinstance(m, str) else nm(m)
            toks.append(f"{name_}:{fmt(d / TPB)}{mk}")
            t = s + d
        if t < TU: toks += rest(TU - t)
        q = dict(p.base); q["role"] = p.role; q.setdefault("pan", 0); q["notes"] = " ".join(toks)
        q["barGain"] = gain_pad if p.role.startswith("うしろの和音") else gain_dr if drum else gain
        parts.append(q)
    P["lead"].base.update(pan=0.05, phrase=8)
    for k, p in enumerate(P["comp"]): p.base["pan"] = cpan
    if "solo2" in P: P["solo2"].base.update(pan=0.25 if cpan < 0 else -0.25, phrase=8)
    if "pad" in P:
        for k, p in enumerate(P["pad"]): p.base["pan"] = [-0.8, 0.8, -0.35, 0.0, 0.45][k]
    if "harm" in P: P["harm"].base.update(pan=-0.2, phrase=8, volume=0.14)
    if "bass" in P: P["bass"].base["pan"] = 0.05
    emit(P["lead"])
    if "dbl" in P: P["dbl"].base.update(pan=-0.1, phrase=8); emit(P["dbl"])
    if "solo2" in P: emit(P["solo2"])
    if "harm" in P: emit(P["harm"])
    for p in P["comp"]: emit(p)
    if "pad" in P:
        for p in P["pad"]: emit(p)
    if "bass" in P: emit(P["bass"])
    for k in ("kick", "snare", "hat", "ride", "crash", "tom"):
        if k in D: emit(D[k], drum=True)
    # 楽器ごとの大きさをそろえる（2026-10-19。楽器の音源ごとに、同じ volume でも大きさが 20dB 近くちがう。
    #   cafe_jazz_cal.json＝同じ音形を鳴らして測った、旋律のピアノとの差 dB）。旋律はピアノと同じ、ソロは -1、和音は -6.5、うしろの和音は -12 に
    CAL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cafe_jazz_cal.json")))
    def cal_db(key, target):
        if key not in CAL: return 0.0
        return round(max(-8.0, min(10.0, target - CAL[key])), 1)
    for q in parts:
        r = q["role"]
        if r.startswith("旋律（"): q["gainDb"] = q.get("gainDb", 0) + cal_db("L:" + song["lead"], 0.0)
        elif r.startswith("ソロ（"): q["gainDb"] = q.get("gainDb", 0) + cal_db("L:" + song["solo2"], -1.0)
        elif r.startswith("旋律の重ね"): q["gainDb"] = q.get("gainDb", 0) + float(song.get("double_db", -6.0))
        elif r.startswith("テーマの2声目"): q["gainDb"] = q.get("gainDb", 0) + cal_db("L:trombone", -3.0)
        elif r.startswith("和音（"): q["gainDb"] = q.get("gainDb", 0) + cal_db("C:" + comp_name, song.get("comp_t", -8.5))
        elif r.startswith("うしろの和音（"): q["gainDb"] = q.get("gainDb", 0) + cal_db("P:" + song["pad"], song.get("pad_t", -15.0))
        elif r.startswith("左手の低音"): q["gainDb"] = q.get("gainDb", 0)
    tune = song.get("tune", {})
    for q in parts:
        for k2, v in tune.items():
            if q["role"].startswith(k2): q.update(v)

    tempo = [{"bar": NB - 3, "bpm": round(bpm * 0.72), "ramp": 3}]
    secs = (NB - 3) * bar_s + 3 * bar_s / 0.88
    def safe(n):   # 作曲ソフトの和音の欄が読める書き方へ（表示と点検用。音はパートで書いている）
        for a, b in (("maj7#11", "maj7"), ("7b9", "7"), ("7alt", "7"), ("7#9", "7"), ("7#11", "7"), ("9sus4", "7sus4"), ("m11", "m9"), ("mM7", "m"), ("13", "7")):
            n = n.replace(a, b)
        return n
    bar_ch = [safe(b[0][0]["name"]) for b in bars]
    j = {"title": song["title"] + "（仮）", "titleEn": song["en"],
         "description": f"（仮）カフェ用のジャズ。{song['image']}。{song['meter']}・BPM{bpm}・{song['key']}、約{int(secs // 60)}分{int(secs % 60):02d}秒。"
                        f"形: イントロ4・テーマ32・ソロ{n_solo * 8}・テーマ{out_bars}・終わり4。{song['desc']}",
         "bpm": bpm, "beats": beats, "chords": " ".join(bar_ch), "barsPerChord": 1, "repeats": 1, "tone": "rock", "feel": "rock",
         "swing": song["swing"], "human": 0.2, "dynamics": song.get("dyn", False), "autoAccompaniment": False, "autoScoop": False, "guitarWobble": False,
         "drumMix": DRUMMIX, "parts": parts, "tempo": tempo, "instrumentCheck": False}
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    json.dump(j, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return secs, NB, n_solo, out_bars


# 曲ごとの決めた調整（2026-10-19、点数の試しで選んだもの）。L2＝旋律をピアノにして元の楽器はソロと後テーマへ、C＝ソロもゆったり・2つ目の楽器は後テーマだけ
def _L2(s): return {"lead": "piano", "solo2": s["lead"]}
_C = dict(s2blocks=0, s2head=True, calm_solo=True)
FINAL = {}
for _n, _s in enumerate(SONGS, 1):
    k = f"{_n:02d}"
    if _n in (2, 9, 10, 19, 22, 25, 6, 8): FINAL[k] = _L2(_s)
    if _n in (2, 22, 25, 6): FINAL[k]["seed"] = 1
    if _n in (3, 5, 7, 11, 13, 12, 17): FINAL[k] = dict(_L2(_s), seed={3: 1, 5: 1, 7: 1, 11: 1, 13: 2, 12: 2, 17: 1}[_n], **_C)
    # 2026-10-19 テナーサックス（VCSL の録音）を入れたので、4・20 はサックスが旋律
    if _n == 4: FINAL[k] = dict(seed=1, drums="swing2", cstyle="swing", bass="two", **_C)
    if _n == 20: FINAL[k] = dict(seed=1, drums="swing2", cstyle="swing", bass="two", **_C)
    if _n == 9: FINAL[k] = {"lead": "piano", "solo2": "tenorSax"}
    if _n == 16: FINAL[k] = dict(seed=1, drums="straight", **_C)
    if _n == 24: FINAL[k] = {"seed": 1}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "assets-src/ai-songs"
    tune = json.loads(os.environ["JAZZ_TUNE"]) if "JAZZ_TUNE" in os.environ else FINAL
    for n, s in enumerate(SONGS, 1):
        if which not in ("all", str(n), s["id"]): continue
        if f"{n:02d}" in tune: s = dict(s, **tune[f"{n:02d}"])
        if "JAZZ_EXTRA" in os.environ: s = dict(s, **json.loads(os.environ["JAZZ_EXTRA"]))
        out = os.path.join(outdir, os.environ.get("JAZZ_PRE", "") + f"cafe25-{n:02d}-{s['id']}.json")
        t, nb, ns, ob = build(s, out)
        print(f"{n:02d} {s['id']} {t:.0f}秒 {nb}小節 ソロ{ns * 8} 後テーマ{ob}")
