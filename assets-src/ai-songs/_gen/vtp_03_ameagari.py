# 試作「雨上がりのペダル」（歌なし・E・140）2026-11-07
# 人間「なんか曲を試しに作って。それで聴いて決める」: 聞き比べJの組み方
#   左＝人の演奏データのかき鳴らし（GuitarSet）・右＝リフ・真ん中＝リード・ドラム＝人の演奏データ（Groove MIDI）
# 物語: 雨の中でけんかして別れたあと、雨がやんで自転車で駅へ謝りに行く。
import json, copy, random, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools/composer'))
from gset_to_parts import string_parts
from gmd_to_parts import parts_from_gmd

BPM = 140
SEC = [  # (名前, 小節, コード)
    ('前奏', 'E C#m A B E C#m A B'),
    ('Aメロ', 'E B C#m A E B A B'),
    ('Bメロ', 'F#m G#m A B F#m G#m A B'),
    ('サビ', 'A B G#m C#m F#m B E E'),
    ('間奏', 'E C#m A B E C#m A B'),
    ('Cメロ', 'C#m A E B'),
    ('最後のサビ', 'A B G#m C#m F#m B C D'),
    ('後奏', 'E C#m A E'),
]
chords = ' '.join(c for _, c in SEC).split()
NB = len(chords); TOTAL = NB * 4
start = {}; b = 0
for n, c in SEC: start[n] = b; b += len(c.split())

LO = {"E": ["E2", "B2", "E3", "G#3", "B3", "E4"], "B": [None, "B2", "F#3", "B3", "D#4", "F#4"], "C#m": [None, "C#3", "G#3", "C#4", "E4", "G#4"],
      "A": [None, "A2", "E3", "A3", "C#4", "E4"], "F#m": ["F#2", "C#3", "F#3", "A3", "C#4", "F#4"], "G#m": ["G#2", "D#3", "G#3", "B3", "D#4", "G#4"],
      "C": [None, "C3", "G3", "C4", "E4", "G4"], "D": [None, None, "D3", "A3", "D4", "F#4"]}

base = json.load(open('/tmp/ab/i1_nodr.json'))
gt = [p for p in base['parts'] if p['instrument'] == 'distGuitar'][0]
gtmpl = {k: v for k, v in gt.items() if k not in ('notes', 'role', 'pan', 'volume', 'double')}
gtmpl['double'] = False; gtmpl['powerChord'] = False
bass_t = [p for p in base['parts'] if p['instrument'] == 'bass'][0]
drum_ref = {p['instrument']: p for p in json.load(open('/tmp/ab/gd.json'))['parts'] if p['instrument'] in ('kick', 'snare', 'hihat', 'tom', 'crash')}
parts = []

# ---------------- ドラム（人の演奏データ）
G = '/tmp/gmd/groove/'
R14 = G + 'drummer5/session2/14_rock_140_beat_4-4.mid'; R13 = G + 'drummer5/session2/13_rock_140_beat_4-4.mid'; PK = G + 'drummer1/session2/32_punk_140_beat_4-4.mid'
dseg = [  # (ファイル, 元の小節, 何小節) / None＝休み
    (None, 0, 2), (R14, 2, 6),        # 前奏: 2小節はリフだけ
    (R13, 0, 8),                       # Aメロ
    (PK, 4, 8),                        # Bメロ（飾りの少ない8ビート）
    (R14, 40, 8),                      # サビ（2小節ごとのクラッシュ・最後にフィル）
    (PK, 53, 8),                       # 間奏（ライド・最後にフィル）
    (PK, 74, 4),                       # Cメロ（タムの刻み）
    (R14, 32, 8),                      # 最後のサビ
    (R14, 48, 3), ('END', 0, 1),       # 後奏: 最後の1打
]
dn = {k: [] for k in ('kick', 'snare', 'hihat', 'tom', 'crash')}
for f, b0, n in dseg:
    if f is None:
        for k in dn: dn[k].append(f'R:{n * 4}')
    elif f == 'END':
        dn['kick'].append('x:4%120'); dn['crash'].append('C2:4%125'); dn['snare'].append('R:4'); dn['hihat'].append('R:4'); dn['tom'].append('R:4')
    else:
        r = parts_from_gmd(f, b0, n)
        for k in dn: dn[k].append(r.get(k) or f'R:{n * 4}')
for k, lst in dn.items():
    p = copy.deepcopy(drum_ref[k]); p['notes'] = ' '.join(lst); parts.append(p)

# ---------------- L: かき鳴らし
def sec(n): return start[n]
segL = [(None, 0, 2), ('00_Rock3-148-C_comp', 0, 6),
        ('01_Rock3-117-Bb_comp', 0, 8),
        ('HIT', 92, 2), ('04_Rock3-148-C_comp', 2, 6),
        ('00_Rock3-117-Bb_comp', 0, 8),
        ('00_Rock3-148-C_comp', 8, 8),
        ('HIT', 82, 4),
        ('00_Rock3-148-C_comp', 0, 8),
        ('00_Rock3-117-Bb_comp', 8, 3), ('HIT', 105, 1)]
vel_by_bar = []  # 場面ごとの強さ
VS = {'前奏': 0.95, 'Aメロ': 0.8, 'Bメロ': 0.88, 'サビ': 1.0, '間奏': 0.95, 'Cメロ': 0.85, '最後のサビ': 1.05, '後奏': 1.0}
# string_parts は全体に1つの vel_scale なので、場面ごとに分けて作って重ねる
Lnotes = None
import itertools
def split_by_section(segs):
    out = []; tb = 0
    for s in segs:
        out.append((tb, s)); tb += s[2]
    return out
per = [[] for _ in range(6)]
for tb, sg in split_by_section(segL):
    secname = [n for n, _ in SEC if start[n] <= tb][-1]
    full = [(None, 0, tb)] if tb else []
    full += [sg]
    rest = NB - tb - sg[2]
    if rest: full.append((None, 0, rest))
    ss = string_parts(full, chords, LO, BPM, vel_scale=VS[secname])
    for i in range(6): per[i].append(ss[i])

def merge_notes(lst, total):
    ev = []
    for n in lst:
        t = 0.0
        for tok in n.split():
            nm, d = tok.split(':', 1); dd = float(re.match(r'[\d.]+', d).group())
            if nm != 'R': ev.append((t, tok))
            t += dd
    ev.sort(); out = []; cur = 0.0
    for t, tok in ev:
        if t < cur - 1e-6: continue
        if t > cur + 1e-4: out.append(f'R:{t - cur:.4f}')
        out.append(tok); cur = t + float(re.match(r'[\d.]+', tok.split(':', 1)[1]).group())
    if total > cur + 1e-4: out.append(f'R:{total - cur:.4f}')
    return ' '.join(out)
for i in range(6):
    n = merge_notes(per[i], TOTAL)
    if all(t.startswith('R:') for t in n.split()): continue
    p = copy.deepcopy(gtmpl); p.update(role=f'Lギター（かき鳴らし）・弦{i + 1}', pan=-0.8, volume=0.047, notes=n); parts.append(p)

# ---------------- 人らしい揺れ
def human(seq, jit=0.010, base_vel=100, seed=1):
    rnd = random.Random(seed); sp = 60 / BPM; out = []; t = 0.0; ev = []
    for name, d, mark in seq:
        if name == 'R': t += d; continue
        on = t + (rnd.gauss(0, jit) / sp if t > 0 else 0)
        bp = t % 1
        v = base_vel + (10 if bp < 0.01 else -7 if abs(bp - 0.5) > 0.01 else 0) + rnd.gauss(0, 4)
        ev.append([max(0, on), t + d, name, mark, int(max(55, min(125, v)))]); t += d
    cur = 0.0
    for i, (on, end, name, mark, v) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else end
        ln = max(0.06, min(end, nxt) - on - 0.01)
        if on > cur + 1e-4: out += rests(on - cur)
        mk, sl = (mark.split('>', 1) + [''])[:2] if '>' in mark else (mark, '')
        out.append(f'{name}:{ln:.4f}{mk}%{v}' + (f'>{sl}' if sl else '')); cur = on + ln
    if t > cur + 1e-4: out += rests(t - cur)
    return ' '.join(out), t

def rests(d):
    o = []
    while d > 16 + 1e-6: o.append('R:16'); d -= 16
    if d > 1e-4: o.append(f'R:{d:.4f}')
    return o

def P(txt):
    r = []
    for tok in txt.split():
        m = re.match(r'([A-G][#b]?\d|R):([\d.]+)(.*)$', tok); r.append((m[1], float(m[2]), m[3]))
    return r
def up12(seq):
    o = []
    for n, d, m in seq:
        if n == 'R': o.append((n, d, m)); continue
        g = re.match(r'([A-G][#b]?)(\d)', n); o.append((g[1] + str(int(g[2]) + 1), d, m))
    return o

# ---------------- R: リフ
RIFF = ('E3:0.5 B3:0.5 E4:0.75 D#4:0.25 E4:0.5 B3:0.5 G#3:0.5 B3:0.5 '
        'C#4:0.5 G#3:0.5 E4:0.75 D#4:0.25 E4:0.5 G#3:0.5 C#4:0.5 B3:0.5 '
        'A3:0.5 E4:0.5 C#4:0.75 B3:0.25 C#4:0.5 E4:0.5 F#4:0.5 E4:0.5 '
        'B3:0.5 F#4:0.5 D#4:0.75 C#4:0.25 B3:1 F#3:0.5 A3:0.5 ')
R_A = 'E3:0.5 B3:0.5 G#4:3 B3:0.5 F#4:0.5 D#4:3 C#4:0.5 G#3:0.5 E4:3 A3:0.5 E4:0.5 C#4:3 E3:0.5 B3:0.5 G#4:3 B3:0.5 F#4:0.5 D#4:3 A3:0.5 E4:0.5 C#4:3 B3:0.5 F#4:0.5 A4:1 F#4:1 D#4:1 '
ARP = lambda a: ' '.join(f'{x}:0.5' for x in a.split())
R_B = (ARP('F#3 C#4 F#4 A4 F#4 C#4 A3 C#4') + ' ' + ARP('G#3 D#4 G#4 B4 G#4 D#4 B3 D#4') + ' ' + ARP('A3 E4 A4 C#5 A4 E4 C#4 E4') + ' ' + ARP('B3 F#4 B4 D#5 B4 F#4 D#4 F#4') + ' ' +
       ARP('F#3 C#4 F#4 A4 F#4 C#4 A3 C#4') + ' ' + ARP('G#3 D#4 G#4 B4 G#4 D#4 B3 D#4') + ' ' + ARP('A3 E4 A4 C#5 A4 E4 C#4 E4') + ' B3:1 R:3 ')
CNT = 'E3:2 C#3:2 D#3:2 F#3:2 D#3:4 E3:2 G#3:2 A3:2 F#3:2 F#3:2 D#3:2 E3:4 R:4 '
CNT2 = 'E3:2 C#3:2 D#3:2 F#3:2 D#3:4 E3:2 G#3:2 A3:2 F#3:2 F#3:2 D#3:2 E3:2 G3:2 F#3:2 A3:2 '
R_C = 'R:4 R:4 R:4 R:3 B4:1>B3 '   # Cメロ: 最後の拍で上から滑り落ちる（ブレーキ）
R_O = 'E3:0.5 B3:0.5 E4:0.75 D#4:0.25 E4:0.5 B3:0.5 G#3:0.5 B3:0.5 C#4:0.5 G#3:0.5 E4:0.75 D#4:0.25 E4:0.5 G#3:0.5 C#4:0.5 B3:0.5 A3:0.5 E4:0.5 C#4:0.75 B3:0.25 C#4:0.5 E4:0.5 F#4:0.5 E4:0.5 E3:4 '
rl = P(RIFF + RIFF + R_A + R_B) + [('R', 32, '')] + P(RIFF + RIFF + R_C) + [('R', 32, '')] + P(R_O)
rh = [('R', 32 * 3, '')] + P(CNT) + [('R', 32 + 16, '')] + P(CNT2) + [('R', 16, '')]
rl_low_counter = [('R', 32 * 3, '')] + P(CNT) + [('R', 32 + 16, '')] + P(CNT2) + [('R', 16, '')]
nl, tl = human(rl, base_vel=98, seed=3)
# サビの裏の旋律（低い方は rl の休みの所に入るので、別のパートにする）
nc, tc = human(rl_low_counter, base_vel=92, seed=5)
nh, th = human(up12(rh), base_vel=86, seed=5)
assert abs(tl - TOTAL) < 1e-6 and abs(tc - TOTAL) < 1e-6, (tl, tc, TOTAL)
rt = copy.deepcopy(gtmpl); rt.update(amp='namJVM', ampDrive=0.5, ampCabIr='jd-greenback-4x12-01', release=0.12)
for role, n, v in (('Rギター（リフ）', nl, 0.087), ('Rギター（サビの裏の旋律）', nc, 0.075), ('Rギター（サビの裏の旋律・オクターブ上）', nh, 0.06)):
    p = copy.deepcopy(rt); p.update(role=role, pan=0.8, volume=v, notes=n); parts.append(p)

# ---------------- リード
L_INTRO = 'R:16 R:2 B4:1 G#4:1 C#5:3 B4:1 A4:1 B4:1 C#5:2 D#5:2!~. B4:2 '
L_A = 'R:4 R:2 F#4:0.5 G#4:0.5 B4:1 R:4 R:2 C#5:0.5 B4:0.5 A4:1~. R:4 R:2 D#5:0.5 C#5:0.5 B4:1 R:4 R:1 B4:0.5 C#5:0.5 D#5:1 F#5:1 '
L_B = 'R:32 '
L_CH = 'C#5:1.5 B4:0.5 C#5:1 E5:1 F#5:2! E5:1 D#5:1 D#5:1.5 B4:0.5 G#4:2 R:1 G#4:0.5 B4:0.5 C#5:1 E5:1 F#5:1.5 E5:0.5 C#5:1 A4:1 B4:1 C#5:1 D#5:1 F#5:1 E5:3~. R:1 R:2 B4:0.5 C#5:0.5 E5:1 '
L_SOLO = ('G#4:0.5 B4:0.5 E5:1 D#5:0.5 E5:0.5 F#5:1 E5:2^^@0.3 C#5:1 B4:1 A4:0.25_ B4:0.25_ C#5:0.5 E5:1 C#5:0.5 B4:0.5 A4:1 B4:2>D#5 F#5:2~. '
          'E5:0.5 F#5:0.5 G#5:1 F#5:0.5 E5:0.5 B4:1 C#5:0.25_ D#5:0.25_ E5:0.5 G#5:1 E5:1 C#5:1 E5:2!^^@0.3 C#5:1 A4:1 B4:1 D#5:1 F#5:2~. ')
L_C = 'R:16 '
L_CH2 = 'C#5:1.5 B4:0.5 C#5:1 E5:1 F#5:2! E5:1 D#5:1 D#5:1.5 B4:0.5 G#4:2 R:1 G#4:0.5 B4:0.5 C#5:1 E5:1 F#5:1.5 E5:0.5 C#5:1 A4:1 B4:1 C#5:1 D#5:1 F#5:1 E5:1 D5:1 E5:1 G5:1 F#5:4!~. '
L_OUT = 'B4:4 C#5:4 C#5:2 B4:2 G#4:4~. '
lead_seq = P(L_INTRO + L_A + L_B + L_CH + L_SOLO + L_C + L_CH2 + L_OUT)
assert abs(sum(d for _, d, _ in lead_seq) - TOTAL) < 1e-6, sum(d for _, d, _ in lead_seq)
lead = ' '.join(f'{n}:{d:g}{m}' for n, d, m in lead_seq)
parts.append({"instrument": "leadGuitar", "role": "リードギター", "guitarTone": "warm-lead-a", "pan": 0.1, "volume": 0.107, "notes": lead, "humanTiming": 0.3})

# ---------------- ベース
ROOT = {"E": "E2", "B": "B1", "C#m": "C#2", "A": "A1", "F#m": "F#1", "G#m": "G#1", "C": "C2", "D": "D2"}
def oct_up(n): g = re.match(r'([A-G][#b]?)(\d)', n); return g[1] + str(int(g[2]) + 1)
bseq = []
for bi, c in enumerate(chords):
    r = ROOT[c]; sname = [n for n, _ in SEC if start[n] <= bi][-1]
    if sname == '前奏' and bi < 2: bseq.append(('R', 4, '')); continue
    if sname == 'Aメロ': bseq += P(f'{r}:1.5 {r}:0.5 R:0.5 {r}:1 {r}:0.5')
    elif sname == 'Bメロ':
        bseq += P(f'{r}:1 R:3') if bi == start['Bメロ'] + 7 else P(f'{r}:1 {r}:1 {r}:1 {r}:1')
    elif sname == 'Cメロ': bseq += P(f'{r}:4')
    elif sname == '後奏' and bi == NB - 1: bseq += P(f'{r}:4')
    else:
        pat = ' '.join([f'{r}:0.5'] * 7) + (f' {oct_up(r)}:0.5' if bi % 2 else f' {r}:0.5')
        bseq += P(pat)
nb, tb_ = human(bseq, jit=0.006, base_vel=95, seed=9)
pb = copy.deepcopy(bass_t); pb['notes'] = nb; parts.append(pb)

song = {k: v for k, v in base.items() if k != 'parts'}
song.update(title='雨上がりのペダル（試作）', description='試作・歌なし。左＝人の演奏データのかき鳴らし・右＝リフ・真ん中＝リード・ドラム＝人の演奏データ。仮の曲',
            bpm=BPM, chords=' '.join(chords), parts=parts,
            dynamics=False)  # 自動の強弱（出だしを小さく）は切る。強弱は人の演奏データと場面ごとの強さで付けている
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/ab/ameagari.json'
json.dump(song, open(out, 'w'), ensure_ascii=False); print(out, NB, 'bars', len(parts), 'parts')
