# 試作「前夜祭」（歌なし・D→E・152）2026-11-07
# 人間「ギターコードをジャンジャン弾くような感じで曲を作って」
#   主役＝左右の和音のかき鳴らし（左＝低い押さえ方・右＝高い押さえ方。人の演奏データ GuitarSet）、リード＝サビの主旋律、ドラム＝人の演奏データ（Groove MIDI）
# 物語: 文化祭の前の夜、軽音部の3人が体育館で最後の通し練習をする。
import json, copy, random, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools/composer'))
from gset_to_parts import string_parts
from gmd_to_parts import parts_from_gmd

BPM = 152
SEC = [
    ('カウント', 'D'),
    ('前奏', 'D D Bm G D A G A'),
    ('Aメロ', 'D F#m G Gm D F#m Em A'),
    ('Aメロ2', 'D F#m G Gm D F#m Em A'),
    ('Bメロ', 'Bm G D A Bm G Em A'),
    ('サビ', 'G A F#m Bm G A D D G A F#m Bm Em G A A'),
    ('間奏', 'D C G D D C G A'),
    ('落ちサビ', 'G A F#m Bm G A D B'),
    ('最後のサビ', 'A B G#m C#m A B E E A B G#m C#m F#m A B B'),
    ('終わり', 'E'),
]
chords = ' '.join(c for _, c in SEC).split(); NB = len(chords); TOTAL = NB * 4
start = {}; b = 0
for n, c in SEC: start[n] = b; b += len(c.split())
def sec_of(bi): return [n for n, _ in SEC if start[n] <= bi][-1]

LO = {"D": [None, "A2", "D3", "A3", "D4", "F#4"], "F#m": ["F#2", "C#3", "F#3", "A3", "C#4", "F#4"], "G": ["G2", "B2", "D3", "G3", "B3", "G4"],
      "Gm": ["G2", "D3", "G3", "A#3", "D4", "G4"], "Bm": [None, "B2", "F#3", "B3", "D4", "F#4"], "A": [None, "A2", "E3", "A3", "C#4", "E4"],
      "Em": ["E2", "B2", "E3", "G3", "B3", "E4"], "C": [None, "C3", "E3", "G3", "C4", "E4"], "B": [None, "B2", "F#3", "B3", "D#4", "F#4"],
      "E": ["E2", "B2", "E3", "G#3", "B3", "E4"], "G#m": ["G#2", "D#3", "G#3", "B3", "D#4", "G#4"], "C#m": [None, "C#3", "G#3", "C#4", "E4", "G#4"]}
HI4 = {"D": "A3 D4 F#4 A4", "F#m": "A3 C#4 F#4 A4", "G": "B3 D4 G4 B4", "Gm": "A#3 D4 G4 A#4", "Bm": "B3 D4 F#4 B4", "A": "A3 C#4 E4 A4",
       "Em": "B3 E4 G4 B4", "C": "C4 E4 G4 C5", "B": "B3 D#4 F#4 B4", "E": "B3 E4 G#4 B4", "G#m": "B3 D#4 G#4 B4", "C#m": "C#4 E4 G#4 C#5"}
HI = {k: [None, None] + v.split() for k, v in HI4.items()}

base = json.load(open('/tmp/ab/i1_nodr.json'))
gt = [p for p in base['parts'] if p['instrument'] == 'distGuitar'][0]
gtmpl = {k: v for k, v in gt.items() if k not in ('notes', 'role', 'pan', 'volume', 'double')}
gtmpl['double'] = False; gtmpl['powerChord'] = False
bass_t = [p for p in base['parts'] if p['instrument'] == 'bass'][0]
drum_ref = {p['instrument']: p for p in json.load(open('/tmp/ab/gd.json'))['parts'] if p['instrument'] in ('kick', 'snare', 'hihat', 'tom', 'crash')}
parts = []

def num(tok): return float(re.match(r'[\d.]+', tok.split(':', 1)[1]).group())
def to_events(n):
    ev = []; t = 0.0
    for tok in n.split():
        nm = tok.split(':', 1)[0]
        if nm != 'R': ev.append([t, num(tok), tok])
        t += num(tok)
    return ev
def rests(d):
    o = []
    while d > 16 + 1e-6: o.append('R:16'); d -= 16
    if d > 1e-4: o.append(f'R:{d:.4f}')
    return o
def merge(evs, total):
    evs = sorted(evs, key=lambda e: e[0]); out = []; cur = 0.0
    for i, (t, d, tok) in enumerate(evs):
        if t < cur - 1e-6: continue
        nxt = evs[i + 1][0] if i + 1 < len(evs) else total
        d = min(d, max(0.04, nxt - t - 0.01))
        name, rest = tok.split(':', 1)
        tail = re.sub(r'^[\d.]+', '', rest)
        if t > cur + 1e-4: out += rests(t - cur)
        out.append(f'{name}:{d:.4f}{tail}'); cur = t + d
    if total > cur + 1e-4: out += rests(total - cur)
    return ' '.join(out)

# ---------------- かき鳴らしの部品
def gset(voic, segs_by_bar, vel):
    """segs_by_bar: [(曲の小節, 源のファイル, 源の小節, 何小節)] → 弦ごとの事件の並び"""
    per = [[] for _ in range(6)]
    for bar, src, b0, n in segs_by_bar:
        full = ([(None, 0, bar)] if bar else []) + [(src, b0, n)] + ([(None, 0, NB - bar - n)] if NB - bar - n else [])
        ss = string_parts(full, chords, voic, BPM, vel_scale=vel)
        for i in range(6): per[i] += to_events(ss[i])
    return per
def hits(voic, bar, pos, vel=100, up=False, ring=None, spread=0.016):
    """そろえて弾く打ち（キメ・のばす和音）。pos: [(小節内の拍, 長さ, 強さ倍)]"""
    per = [[] for _ in range(6)]; sp = 60 / BPM
    vo = voic[chords[bar]]
    strs = [i for i in range(6) if vo[i] is not None]
    if up: strs = strs[::-1]
    for (bt, d, vm) in pos:
        for k, st in enumerate(strs):
            t = bar * 4 + bt + k * spread / sp
            v = int(max(40, min(140, vel * vm * (0.92 if up else 1.0))))
            per[st].append([t, d - k * spread / sp, f'{vo[st]}:{d:.4f}%{v}'])
    return per
def addp(a, b):
    for i in range(6): a[i] += b[i]

L = [[] for _ in range(6)]; R = [[] for _ in range(6)]
S = start
# 前奏: 頭2小節は「ジャーーン」をのばす → かき鳴らし
addp(L, hits(LO, S['前奏'], [(0, 7.9, 1.25)])); addp(R, hits(HI, S['前奏'], [(0.02, 7.9, 1.2)]))
addp(L, gset(LO, [(S['前奏'] + 2, '00_Rock3-148-C_comp', 2, 6)], 1.0))
addp(R, gset(HI, [(S['前奏'] + 2, '00_Rock3-117-Bb_comp', 0, 6)], 0.9))
# Aメロ: 左ひとり → Aメロ2 で右が重なる
addp(L, gset(LO, [(S['Aメロ'], '01_Rock3-117-Bb_comp', 0, 8)], 0.9))
addp(L, gset(LO, [(S['Aメロ2'], '01_Rock3-117-Bb_comp', 8, 8)], 0.95))
addp(R, gset(HI, [(S['Aメロ2'], '00_Rock3-148-C_comp', 8, 8)], 0.8))
# Bメロ: 前半4小節はキメ（1拍目・2拍目の裏・4拍目）、後半はダウンを詰め、最後は16分で加速
KIME = [(0, 0.45, 1.2), (1.5, 0.45, 1.1), (3, 0.9, 1.15)]
for k in range(4):
    addp(L, hits(LO, S['Bメロ'] + k, KIME)); addp(R, hits(HI, S['Bメロ'] + k, [(p + 0.01, d, v) for p, d, v in KIME]))
addp(L, gset(LO, [(S['Bメロ'] + 4, '00_Rock3-117-Bb_comp', 4, 3)], 0.95))  # 同じ打ちの並べ方は機械的になるので、人の演奏データに
addp(R, gset(HI, [(S['Bメロ'] + 4, '00_Rock3-148-C_comp', 4, 3)], 0.95))
last = S['Bメロ'] + 7
# 最後の小節: 16分で全部の弦をそろえてかき鳴らす加速は、うるさく機械的（サビ頭の点数 6.4）。人の演奏の詰まった小節にして、強さだけ上げる
addp(L, gset(LO, [(last, '00_Rock3-148-C_comp', 7, 1)], 1.1))
addp(R, gset(HI, [(last, '00_Rock3-117-Bb_comp', 7, 1)], 1.05))
# サビ: 全開（左右で違う人の演奏）
addp(L, gset(LO, [(S['サビ'], '00_Rock3-117-Bb_comp', 0, 16)], 1.05))
addp(R, gset(HI, [(S['サビ'], '04_Rock3-148-C_comp', 0, 16)], 1.0))  # 右は左と違うノリの人（打ちが少なめで、左の詰まった刻みとぶつからない）
# 間奏: 前半は左とバスドラだけ（見回りで一瞬止まる＝2小節目の3拍目から休み）、後半は全員
addp(L, gset(LO, [(S['間奏'], '04_Rock3-148-C_comp', 0, 1)], 0.85))
addp(L, hits(LO, S['間奏'] + 1, [(0, 1.9, 0.9)]))
addp(L, gset(LO, [(S['間奏'] + 2, '04_Rock3-148-C_comp', 2, 2), (S['間奏'] + 4, '00_Rock3-117-Bb_comp', 8, 4)], 0.95))
addp(R, gset(HI, [(S['間奏'] + 4, '00_Rock3-148-C_comp', 12, 4)], 0.95))
# 落ちサビ: 1小節に1回のばす（最後の小節は転調の入口 B を強めに）
for k in range(8): addp(L, hits(LO, S['落ちサビ'] + k, [(0, 3.9, 0.8 if k < 7 else 1.0)]))
# 最後のサビ（E）: 最強
addp(L, gset(LO, [(S['最後のサビ'], '00_Rock3-117-Bb_comp', 0, 16)], 1.12))
addp(R, gset(HI, [(S['最後のサビ'], '00_Rock3-148-C_comp', 0, 16)], 1.08))
# 終わり: ジャン・ジャン・ジャン
END = [(0, 0.4, 1.25), (1, 0.4, 1.25), (2, 1.2, 1.35)]
addp(L, hits(LO, S['終わり'], END)); addp(R, hits(HI, S['終わり'], [(p + 0.01, d, v) for p, d, v in END]))

for side, per, pan, vol, amp_over in (('L', L, -0.8, 0.05, {}), ('R', R, 0.8, 0.0535, {'ampCabIr': 'jd-greenback-4x12-01'})):
    for i in range(6):
        if not per[i]: continue
        p = copy.deepcopy(gtmpl); p.update(role=f'{side}ギター（かき鳴らし）・弦{i + 1}', pan=pan, volume=vol, notes=merge(per[i], TOTAL), **amp_over)
        parts.append(p)

# ---------------- ドラム
G = '/tmp/gmd/groove/'
R14 = G + 'drummer5/session2/14_rock_140_beat_4-4.mid'; R13 = G + 'drummer5/session2/13_rock_140_beat_4-4.mid'
PK = G + 'drummer1/session2/32_punk_140_beat_4-4.mid'; HT = G + 'drummer1/session1/202_rock-halftime_140_beat_4-4.mid'
dn = {k: [] for k in ('kick', 'snare', 'hihat', 'tom', 'crash')}
def dseg(f, b0, n):
    r = parts_from_gmd(f, b0, n)
    for k in dn: dn[k].append(r.get(k) or f'R:{n * 4}')
def dcustom(n, **kw):
    for k in dn: dn[k].append(kw.get(k, f'R:{n * 4}'))
dcustom(1, hihat='x:1%45 x:1%50 x:1%55 x:1%62')                      # カウント（ハイハットを踏む音）
dcustom(2, kick='x:8%125', crash='C2:8%128', tom='R:6 C4:0.25%90 C4:0.25%95 A3:0.25%100 A3:0.25%105 F3:0.5%112 F3:0.5%118')
dseg(R14, 2, 6)                                                       # 前奏
dseg(R13, 0, 8)                                                       # Aメロ
dseg(PK, 4, 8)                                                        # Aメロ2
k4 = 'x:1.5%120 x:1.5%110 x:1%118 '; s4 = 'R:3 x:1%115 '               # Bメロのキメ（ギターと同じ所）
# クラッシュを毎回たたくとうるさい（点数 6.2）ので、2小節に1回。ほかの打ちはスネアとハイハットのオープンでそろえる
dcustom(4, kick=k4 * 4, crash='C2:8%115 ' * 2, snare=('R:1.5 x:1.5%105 x:1%112 ') * 4, hihat=('R:1.5 x:1.5*%90 R:1 ') * 4)
dseg(PK, 20, 3)
dcustom(1, kick='x:1%110 x:1%110 x:1%115 x:1%120', snare=' '.join(f'x:0.5%{int(70 + 55 * i / 7)}' for i in range(8)))
dseg(R14, 40, 8); dseg(R14, 32, 8)                                    # サビ
dcustom(1, kick='x:1%105 x:1%100 x:1%105 x:1%100')                    # 間奏: バスドラだけ
dcustom(1, kick='x:1%100 x:1%95 R:2')                                 # 見回りで止まる
dcustom(2, kick='x:1%100 x:1%100 x:1%100 x:1%100 x:1%100 x:1%105 x:1%110 x:0.5%115 x:0.5%120')
dseg(PK, 53, 4)                                                       # ライド
dseg(HT, 1, 8)                                                        # 落ちサビ（半分の速さのノリ・最後にフィル）
dseg(R14, 24, 8); dseg(R14, 40, 8)                                    # 最後のサビ
dcustom(1, kick='x:1%125 x:1%125 x:2%130', crash='C2:1%125 C2:1%125 C2:2%132', snare='x:1%120 x:1%120 x:2%125')
for k, lst in dn.items():
    p = copy.deepcopy(drum_ref[k]); p['notes'] = ' '.join(lst); p['volume'] = round(p['volume'] * 0.89, 4); parts.append(p)

# ---------------- リード（前奏の顔・サビ・落ちサビ・最後のサビ）
def tr(txt, semi):
    N = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    def f(m):
        n = N.index(m[1]) + (int(m[2]) + 1) * 12 + semi; return f'{N[n % 12]}{n // 12 - 1}'
    return re.sub(r'\b([A-G]#?)(\d)(?=:)', f, txt.replace('Db', 'C#'))
HOOK = 'F#5:1 D5:0.5 B4:0.5 D5:1 F#5:1 G5:1.5 F#5:0.5 D5:2 A4:0.5 D5:0.5 F#5:1 E5:1 D5:1 C#5:2 E5:2 B4:1 D5:1 G5:1 F#5:1 E5:4~. '
CH = ('B4:1 A4:0.5 B4:0.5 D5:1.5 B4:0.5 C#5:1 E5:1 A4:2 A4:0.5 C#5:0.5 F#5:1.5 E5:0.5 C#5:1 D5:3~. R:1 '
      'B4:0.5 D5:0.5 G5:1.5 F#5:0.5 D5:1 E5:1 F#5:0.5 E5:0.5 C#5:2 D5:1.5 A4:0.5 F#4:1 A4:1 D5:4~. '
      'B4:1 A4:0.5 B4:0.5 D5:1.5 B4:0.5 C#5:1 E5:1 F#5:2 F#5:1 E5:0.5 C#5:0.5 A4:2 B4:1 D5:1 F#5:2 '
      'G5:2! F#5:1 E5:1 D5:1.5 B4:0.5 G4:2 A4:1 B4:1 C#5:1 E5:1 E5:2^^@0.3 C#5:2 ')
OCHI = ('B4:1 A4:0.5 B4:0.5 D5:1.5 B4:0.5 C#5:1 E5:1 A4:2 A4:0.5 C#5:0.5 F#5:1.5 E5:0.5 C#5:1 D5:3~. R:1 '
        'B4:0.5 D5:0.5 G5:1.5 F#5:0.5 D5:1 E5:1 F#5:0.5 E5:0.5 C#5:2 D5:1.5 A4:0.5 F#4:1 A4:1 D5:2 D#5:2 ')
lead = ('R:4 R:8 ' + HOOK + 'R:16 R:16 R:16 R:16 R:16 R:16 ' + CH + 'R:16 R:16 ' + OCHI + tr(CH, 2) + 'R:4')
tot = sum(num(t) for t in lead.split()); assert abs(tot - TOTAL) < 1e-6, (tot, TOTAL)
# 2026-11-07 人間「ギターを和音で弾いて欲しいかな」: 旋律も単音ではなく和音で弾く（旋律をいちばん上に、そのコードの音を下に2つ重ねる）
NN = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
def mid(n): g = re.match(r'([A-G]#?)(-?\d)', n); return NN.index(g[1]) + (int(g[2]) + 1) * 12
def nm(m): return f'{NN[m % 12]}{m // 12 - 1}'
QUAL = {'m': [0, 3, 7], '': [0, 4, 7]}
def tones(ch):
    r = re.match(r'([A-G]#?)(m?)', ch); return {(NN.index(r[1]) + i) % 12 for i in QUAL[r[2]]}
voices = [[], [], []]; t = 0.0
for tok in lead.split():
    n, rest = tok.split(':', 1); d = num(tok)
    if n == 'R':
        for v in voices: v.append(f'R:{d:g}')
    else:
        marks = re.sub(r'^[\d.]+', '', rest)
        keep = re.sub(r'\^+(@[\d.]+)?', '', marks)            # 和音でチョーキングはしない
        slide = ''
        if '>' in keep: keep, slide = keep.split('>', 1); slide = '>' + slide
        m = mid(n); tc = tones(chords[min(NB - 1, int(t // 4))])
        lows = []; x = m - 1
        while len(lows) < 2:
            if x % 12 in tc: lows.append(x)
            x -= 1
        voices[0].append(f'{n}:{d:g}{keep}{slide}')
        for k, lm in enumerate(lows):
            sl = ''
            if slide:
                tm = mid(slide[1:]) - m; sl = '>' + nm(lm + tm)
            voices[k + 1].append(f'{nm(lm)}:{d:g}{keep.replace("~.", "").replace("~", "")}{sl}')
    t += d
rt = copy.deepcopy(gtmpl); rt.update(release=0.15)
# 3音だとサビで左右のかき鳴らしとぶつかって濁る（点数 6.2〜6.5）ので、旋律＋下の1音（2音の和音）にする
for k, (role, v) in enumerate((('旋律の和音・上（旋律）', 0.062), ('旋律の和音・下', 0.042))):
    # かき鳴らしと同じ音色だと埋もれて濁るので、旋律の和音はリードの音色（浅い歪み・中域が太い）で弾く
    parts.append({"instrument": "leadGuitar", "role": role, "guitarTone": "warm-lead-a", "pan": 0.05, "volume": round(v * 1.15, 4), "notes": ' '.join(voices[k]), "humanTiming": 0.2})
# 落ちサビだけ、リードをやさしく（別パートにして音量を下げる）は今回はしない（同じパートで弾く）

# ---------------- ベース
ROOT = {"D": "D2", "F#m": "F#1", "G": "G1", "Gm": "G1", "Bm": "B1", "A": "A1", "Em": "E2", "C": "C2", "B": "B1", "E": "E2", "G#m": "G#1", "C#m": "C#2"}
def up(n): g = re.match(r'([A-G]#?)(\d)', n); return g[1] + str(int(g[2]) + 1)
rnd = random.Random(4); bt = []
for bi, c in enumerate(chords):
    r = ROOT[c]; s = sec_of(bi); k = bi - start[s]
    if s == 'カウント': bt.append('R:4'); continue
    if s == '前奏' and k < 2: bt.append(f'{r}:8' if k == 0 else ''); continue
    if s == 'Aメロ': pat = f'{r}:1.5 {r}:0.5 R:0.5 {r}:1 {r}:0.5'
    elif s == 'Bメロ' and k < 4: pat = f'{r}:1.5 {r}:1.5 {r}:1'
    elif s == '間奏' and k < 4: pat = (f'{r}:1 {r}:1 {r}:2' if k != 1 else f'{r}:2 R:2')
    elif s == '落ちサビ': pat = f'{r}:4'
    elif s == '終わり': pat = f'{r}:1 {r}:1 {r}:2'
    else: pat = ' '.join([f'{r}:0.5'] * 7) + (f' {up(r)}:0.5' if k % 2 else f' {r}:0.5')
    toks = []
    for tkn in pat.split():
        nm, d = tkn.split(':')
        toks.append(tkn if nm == 'R' else f'{nm}:{d}%{int(max(60, min(120, rnd.gauss(96, 6))))}')
    bt.append(' '.join(toks))
pb = copy.deepcopy(bass_t); pb['notes'] = ' '.join(x for x in bt if x); parts.append(pb)

song = {k: v for k, v in base.items() if k != 'parts'}
song.update(title='前夜祭（試作）', description='試作・歌なし。主役＝左右の和音のかき鳴らし（人の演奏データ）・サビの主旋律＝リード・ドラム＝人の演奏データ。仮の曲',
            bpm=BPM, chords=' '.join(chords), parts=parts, dynamics=False)
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ab/zenyasai.json'
json.dump(song, open(out, 'w'), ensure_ascii=False); print(out, NB, 'bars', len(parts), 'parts')
