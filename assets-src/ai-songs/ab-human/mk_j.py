# 聞き比べJ: L＝かき鳴らし（人の演奏データ）、R＝リフ、真ん中＝リード。2026-11-07
# 人間「音悪くないけど、リードとリフ、LRわかりやすくして欲しい」「聞にくい」
# 見つけた不具合: 弦ごとのパートに powerChord:false が無く、1音ごとに5度と1オクターブ上が足されていた（和音が18音になり、汚い歪みの原因）
import json, copy, random, re, sys
sys.path.insert(0, '/home/claude/wt-mix/tools/composer')
from gset_to_parts import string_parts
random.seed(7)
NODR = '--nodrums' in sys.argv
s = json.load(open('/tmp/ab/i1_nodr.json' if NODR else '/tmp/ab/gd.json'))
src = json.load(open('/tmp/ab/i1_nodr.json'))
gt = [p for p in src['parts'] if p['instrument'] == 'distGuitar']
tmpl = {k: v for k, v in gt[0].items() if k not in ('notes', 'role', 'pan', 'volume', 'double')}
tmpl['double'] = False  # 音色の既定の「左右2本どり」を切る（L と R を分けるため）
base = [p for p in s['parts'] if p['instrument'] != 'distGuitar']
chords = 'F#m D E C#m F#m D E C#m D E C#m F#m Bm E A A'.split()
LO = {"F#m": ["F#2", "C#3", "F#3", "A3", "C#4", "F#4"], "D": [None, "A2", "D3", "A3", "D4", "F#4"], "E": ["E2", "B2", "E3", "G#3", "B3", "E4"],
      "C#m": [None, "C#3", "G#3", "C#4", "E4", "G#4"], "Bm": [None, "B2", "F#3", "B3", "D4", "F#4"], "A": [None, "A2", "E3", "A3", "C#4", "E4"]}
parts = list(base)
# --- L: かき鳴らし（Aメロは控えめ、サビは厚く）
a = string_parts([('01_Rock3-117-Bb_comp', 0, 8), (None, 0, 8)], chords, LO, 140, vel_scale=0.85)
b = string_parts([(None, 0, 8), ('00_Rock3-117-Bb_comp', 8, 8)], chords, LO, 140, vel_scale=1.0)
for i in range(6):
    for tag, n in (('A', a[i]), ('S', b[i])):
        if all(t.startswith('R:') for t in n.split()): continue
        p = copy.deepcopy(tmpl); p.update(role=f'Lギター（かき鳴らし）{tag}・弦{i+1}', pan=-0.8, volume=0.047, notes=n, powerChord=False)
        parts.append(p)

def human(seq, jit=0.012, bpm=140, base_vel=100, acc=None):
    """(音名, 拍, 記号) の並びを、ずれ（秒）と強さのゆれつきの notes にする。"""
    sp = 60 / bpm; out = []; t = 0.0; ev = []
    for name, d, mark in seq:
        if name == 'R': t += d; continue
        on = t + (random.gauss(0, jit) / sp if t > 0 else 0)
        beatpos = t % 1
        v = base_vel + (12 if beatpos < 0.01 else -8 if abs(beatpos - 0.5) > 0.01 else 0) + random.gauss(0, 5)
        ev.append([max(0, on), t + d, name, mark, int(max(55, min(125, v)))]); t += d
    cur = 0.0
    for i, (on, end, name, mark, v) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else end
        ln = max(0.06, min(end, nxt) - on - 0.01)
        if on > cur + 1e-4: out.append(f'R:{on - cur:.4f}')
        out.append(f'{name}:{ln:.4f}{mark}%{v}'); cur = on + ln
    if t > cur + 1e-4: out.append(f'R:{t - cur:.4f}')
    return ' '.join(out)

def P(txt):
    r = []
    for tok in txt.split():
        m = re.match(r'([A-G][#b]?\d|R):([\d.]+)(.*)', tok); r.append((m[1], float(m[2]), m[3]))
    return r

# --- R: リフ（Aメロ＝コードの音を動くリフ、サビ＝オクターブ奏法の旋律）。高めの明るい箱で L と色を分ける
rA1 = 'F#3:0.75 C#4:0.25 F#4:0.5 E4:0.5 C#4:0.75 A3:0.25 B3:0.5 C#4:0.5 D3:0.75 A3:0.25 D4:0.5 C#4:0.5 A3:0.75 F#3:0.25 A3:1 E3:0.75 B3:0.25 E4:0.5 F#4:0.5 G#4:0.75 E4:0.25 B3:1 C#4:0.75 G#3:0.25 E4:0.5 C#4:0.5 B3:0.5 G#3:0.5 E3:0.5 G#3:0.5'
rA2 = 'F#3:0.75 C#4:0.25 F#4:0.5 E4:0.5 C#4:0.75 A3:0.25 B3:0.5 C#4:0.5 D3:0.75 A3:0.25 D4:0.5 C#4:0.5 A3:0.75 F#3:0.25 A3:1 E3:0.75 B3:0.25 E4:0.5 F#4:0.5 G#4:0.75 E4:0.25 B3:1 C#4:0.75 E4:0.25 G#4:0.5 E4:0.5 C#4:0.5 B3:0.5 G#3:0.5 A3:0.5'
oct = 'F#3:1 E3:0.5 F#3:0.5 A3:1.5 F#3:0.5 G#3:1 F#3:0.5 G#3:0.5 B3:1.5 G#3:0.5 E3:1 G#3:0.5 B3:0.5 C#4:2 C#4:1 B3:0.5 A3:0.5 F#3:2 D3:1 F#3:0.5 B3:0.5 D4:1.5 C#4:0.5 B3:1 G#3:0.5 E3:0.5 G#3:2 A3:1.5 C#4:0.5 E4:2 C#4:1 B3:1 A3:2'
def up12(seq):
    N = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    o = []
    for n, d, m in seq:
        if n == 'R': o.append((n, d, m)); continue
        g = re.match(r'([A-G]#?)(\d)', n); o.append((g[1] + str(int(g[2]) + 1), d, m))
    return o
random.seed(11); rlow = human(P(rA1) + P(rA2) + P(oct), base_vel=98)
random.seed(11); rhigh = human([('R', 32, '')] + up12(P(oct)), base_vel=88)
rt = copy.deepcopy(tmpl); rt.update(amp='namJVM', ampDrive=0.5, ampCabIr='jd-greenback-4x12-01', release=0.12)
for role, n, v in (('Rギター（リフ）', rlow, 0.087), ('Rギター（リフ・オクターブ上）', rhigh, 0.067)):
    p = copy.deepcopy(rt); p.update(role=role, pan=0.8, volume=v, notes=n, powerChord=False); parts.append(p)

# --- リード（真ん中）: Aメロは句の終わりの合いの手だけ、サビはのばす音とチョーキングのオブリ
lead = ('R:4 R:2 C#5:0.5 B4:0.25_ A4:0.25 B4:1^^ R:4 R:2 E4:0.5 F#4:0.5 G#4:1^ '
        'R:4 R:2 A4:0.5 B4:0.5 C#5:1~. R:4 R:1 C#5:0.5 E5:0.5 F#5:1 E5:0.5 C#5:0.5 '
        'F#5:2!/ E5:1 C#5:1 B4:3^^@0.25 R:1 R:1 G#4:0.5 B4:0.5 C#5:2~. A4:1 B4:1 C#5:2 '
        'D5:2! C#5:1 B4:1 G#4:2>B4 R:2 A4:1 C#5:1 E5:2~. R:4')
parts.append({"instrument": "leadGuitar", "role": "リードギター", "guitarTone": "warm-lead-a", "pan": 0.1, "volume": 0.107, "notes": lead, "humanTiming": 0.3})
s['parts'] = parts; s['title'] = 'ギター聞き比べJ'; s['description'] = 'L＝かき鳴らし・R＝リフ・真ん中＝リード'
out = '/tmp/ab/j_nodr.json' if NODR else '/tmp/ab/j.json'
json.dump(s, open(out, 'w'), ensure_ascii=False); print(out, len(parts))
