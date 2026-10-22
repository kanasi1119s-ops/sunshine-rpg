# Groove MIDI Dataset（GMD・Google Magenta・CC BY 4.0）の MIDI から、4/4 の8小節のまとまりを取り出し、
# 作曲ソフトの16分の格子（1小節16マス）に直して phrases.json（と fills.json）を作る（2026-10-22）。
# 使い方: python3 -I extract_gmd.py <groove フォルダ（info.csv のある所）> <出力フォルダ>
#   必要: pip install --break-system-packages mido
# 書き方（1小節 = {k,s,h,t,c}、どれも16文字）:
#   k キック / s スネア: X 強・x ふつう・o ゴースト・. 休み
#   h ハイハット: X x o（閉じ）・O（開き）・.
#   t タム: 1 ハイ（C4）・2 ミッド（A3）・3 ロー（F3）・4 フロア（D3）。強く打った音は A B C D（同じ順）
#   c シンバル: c クラッシュ1（C2）・g クラッシュ2（G2）・r ライド（D2）・u ライドのベル（F2）・n チャイナ（B2）・s スプラッシュ（A2）。
#               大文字（C G R U N S）は強く（!）
import csv, json, sys, os, collections, statistics, mido

STEP = 0.25   # 16分＝0.25拍
# GMD（Roland TD-11）の鍵盤 → 楽器（ページの対応表どおり。左右の打面・縁も同じ楽器にまとめる）
KIT = {36: "k", 38: "s", 40: "s", 37: "s",
       48: "t1", 50: "t1", 45: "t2", 47: "t2", 43: "t4", 58: "t4",
       42: "h", 22: "h", 44: "hp", 46: "ho", 26: "ho",
       49: "c", 55: "c", 57: "g", 52: "g", 51: "r", 59: "r", 53: "u"}
# 強さ（ベロシティ 0〜127）の段の閾値（楽器ごと。GMD の分布〔スネアの中央値 45・キック 53・閉じたハット 43〜85〕から決めた）
GHOST = {"k": 30, "s": 50, "h": 40, "hp": 999, "t": 0}      # これより弱い → o（ゴースト）
ACCENT = {"k": 100, "s": 110, "h": 100, "hp": 999, "t": 110, "cym": 110}   # これ以上 → X（強）
CRASH_MIN = 30   # これより弱いクラッシュは、手で止めた音・まちがいの触れとみなして捨てる
OPEN_MIN = 50    # これより弱い「開き」は、ほとんど閉じた音なので閉じたハットに

def read_notes(path):
    m = mido.MidiFile(path); tpb = m.ticks_per_beat; t = 0; out = []
    tempo = 500000
    for msg in mido.merge_tracks(m.tracks):
        t += msg.time
        if msg.type == "set_tempo": tempo = msg.tempo
        if msg.type == "note_on" and msg.velocity > 0 and msg.note in KIT:
            out.append((t / tpb, KIT[msg.note], msg.velocity, msg.note))
    return out, tempo

def grid_of(notes, b0, nbars, shuffle):
    """notes のうち [b0, b0+nbars) 小節を格子にする。返り値: bars, 寄せの記録"""
    cells = [dict(k={}, s={}, h={}, t={}, c={}) for _ in range(nbars)]
    moved, offs, merged, trip = 0, [], 0, 0
    tb = collections.Counter()
    lo, hi = b0 * 4 - 0.125, (b0 + nbars) * 4 - 0.125
    for pos, ins, v, note in notes:
        if not (lo <= pos < hi): continue
        rel = pos - b0 * 4
        beat = int((rel + 0.125) // 1); f = rel - beat
        # 16分の格子と、8分3連の格子のどちらに近いか
        q16 = round(f * 4) / 4; q3 = round(f * 3) / 3
        if abs(f - q3) + 0.02 < abs(f - q16) and abs(f - q3) < 0.06 and q3 not in (0.0, 1.0):
            trip += 1
            if not shuffle: tb[int((rel + 0.125) // 4)] += 1
            # シャッフルなら 3連の3つ目＝8分の裏、そうでなければ 16分の近い方へ
            if shuffle: q = 0.5 if abs(q3 - 2 / 3) < 0.01 else 0.25
            else: q = 0.25 if abs(q3 - 1 / 3) < 0.01 else 0.75
        else:
            q = q16
            if shuffle and abs(f - 0.75) < 0.1 and f > 0.6: q = 0.5   # 跳ねた裏（0.62〜0.7）が16分の「a」に寄るのを8分の裏へ
        off = (f - q) * 4; offs.append(abs(off))
        if abs(off) > 0.25: moved += 1
        step = int(round((beat + q) * 4))
        if step < 0: step = 0
        bar, st = divmod(step, 16)
        if bar >= nbars: continue
        C = cells[bar]
        if ins == "k" or ins == "s":
            ch = "o" if v < GHOST[ins] else ("X" if (v >= ACCENT[ins] or (note == 40 and v >= 100)) else "x")
            key = ins
        elif ins == "h":
            ch = "o" if v < GHOST["h"] else ("X" if v >= ACCENT["h"] else "x"); key = "h"
        elif ins == "hp":
            ch = "o"; key = "h"
        elif ins == "ho":
            ch = "O" if v >= OPEN_MIN else ("x" if v >= GHOST["h"] else "o"); key = "h"
        elif ins.startswith("t"):
            n = ins[1]; ch = "ABCD"["1234".index(n)] if v >= ACCENT["t"] else n; key = "t"
        else:
            if ins in ("c", "g") and v < CRASH_MIN: continue
            ch = ins.upper() if v >= ACCENT["cym"] else ins; key = "c"
        if st in C[key]:
            merged += 1
            C[key][st] = pick(C[key][st], ch)
        else: C[key][st] = ch
    bars = []
    for C in cells:
        bars.append({k: "".join(C[k].get(i, ".") for i in range(16)) for k in "kshtc"})
    return bars, dict(trip_bars=sorted(b for b, c in tb.items() if c >= 3 and b < nbars), moved=moved, n=len(offs), mean_off=round(statistics.mean(offs), 3) if offs else 0, merged=merged, triplet=trip)

RANK = {".": 0, "o": 1, "x": 2, "1": 2, "2": 2, "3": 2, "4": 2, "r": 2, "u": 3, "c": 3, "g": 3, "n": 3, "s": 3, "O": 4,
        "X": 5, "A": 5, "B": 5, "C": 5, "D": 5, "R": 5, "U": 5, "G": 5, "N": 5, "S": 5}
def pick(a, b):
    """同じマスに2つ寄ったとき: 強い方・開きを優先"""
    return a if RANK.get(a, 2) >= RANK.get(b, 2) else b

def swing_of(notes, b0, nbars):
    """8分の裏の位置（拍の中の 0.4〜0.8）の平均。0.5＝まっすぐ、0.667＝3連のシャッフル"""
    lo, hi = b0 * 4, (b0 + nbars) * 4; fs = []
    for pos, ins, v, note in notes:
        if lo <= pos < hi and ins in ("h", "ho", "r", "s", "k"):
            f = pos % 1
            if 0.4 <= f <= 0.8: fs.append(f)
    # 16分の「a」（0.75）とまざるので、0.56〜0.72 の山の大きさで見る
    if len(fs) < 8: return 0.5, 0
    mid = [f for f in fs if 0.58 <= f <= 0.72]; straight = [f for f in fs if f < 0.56]; late = [f for f in fs if f > 0.72]
    share = len(mid) / len(fs)
    return (round(statistics.mean(mid), 3) if mid else 0.5), round(share, 2)

def timing_of(notes, b0, nbars, bpm):
    """スネアの2・4拍（バックビート）と、キック1拍目のずれ（ms。＋＝遅い）"""
    lo, hi = b0 * 4 - 0.2, (b0 + nbars) * 4 - 0.2; ms = 60000 / bpm
    sn, kk = [], []
    for pos, ins, v, note in notes:
        if not (lo <= pos < hi): continue
        b = round(pos); d = (pos - b) * ms
        if abs(pos - b) > 0.12: continue
        if ins == "s" and v >= 60 and int(b) % 2 == 1: sn.append(d)
        if ins == "k" and int(b) % 4 == 0: kk.append(d)
    return (round(statistics.mean(sn), 1) if len(sn) > 3 else None), (round(statistics.mean(kk), 1) if len(kk) > 3 else None)

if __name__ == "__main__":
    root, outdir = sys.argv[1], sys.argv[2]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import classify
    rows = list(csv.DictReader(open(os.path.join(root, "info.csv"))))
    phrases, fills, seen = [], [], set()
    for r in rows:
        if r["time_signature"] != "4-4": continue
        notes, _ = read_notes(os.path.join(root, r["midi_filename"]))
        if not notes: continue
        bpm = int(r["bpm"]); style, sub = (r["style"].split("/") + [""])[:2]
        nbar = int(max(p for p, *_ in notes) // 4) + 1
        base = dict(style=style, sub=sub, bpm=bpm, drummer=r["drummer"])
        if r["beat_type"] == "beat":
            for b0 in range(0, nbar - 7, 8):
                sw, share = swing_of(notes, b0, 8)
                shuffle = share >= 0.35 and sw >= 0.6
                bars, q = grid_of(notes, b0, 8, shuffle)
                key = json.dumps(bars)
                if key in seen: continue
                empty = sum(1 for b in bars if not any(c != "." for v in b.values() for c in v))
                if empty > 2: continue
                seen.add(key)
                sl, kl = timing_of(notes, b0, 8, bpm)
                ph = dict(id=f"gmd:{r['id']}:b{b0 + 1}", source="GMD", **base, bars=bars, trip_bars=q.pop("trip_bars"),
                          swing=sw if shuffle else 0.5, quant=q, snare_lag_ms=sl, kick_lag_ms=kl)
                phrases.append(classify.classify(ph))
        else:   # フィル（1〜2小節が多い）は別の表に
            nb = min(nbar, 4)
            sw, share = swing_of(notes, 0, nb); shuffle = share >= 0.35 and sw >= 0.6
            bars, q = grid_of(notes, 0, nb, shuffle)
            ph = dict(id=f"gmd:{r['id']}", source="GMD", **base, bars=bars, trip_bars=q.pop("trip_bars"), swing=sw if shuffle else 0.5, quant=q)
            fills.append(classify.classify(ph))
    os.makedirs(outdir, exist_ok=True)
    print("phrases", len(phrases), "fills", len(fills))
    json.dump(phrases, open(os.path.join(outdir, "gmd_phrases.tmp.json"), "w"), ensure_ascii=False)
    json.dump(fills, open(os.path.join(outdir, "gmd_fills.tmp.json"), "w"), ensure_ascii=False)
