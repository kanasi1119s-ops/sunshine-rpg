#!/usr/bin/env python3
"""ギターの「単音まじりの弾き方」（リード・リフ・和音と単音をまぜた弾き方）の型を、3つのデータから取り出す。
使い方: python3 -I tools/guitar/phrase_patterns.py <GuitarSet の .jams フォルダ> <EGSet12 の .jams フォルダ> <Guitar-TECHS の .mid フォルダ> <出力.json> [--max 120]
取り出すもの（＝手の動き）: 2小節の中で、いつ・単音か和音か・何本・どれだけのばすか（切るか、次の音につなぐか）・どの弦のあたりか・
  前の音から上がるか下がるか（向きと、となりの音か／とんだ音か、の3段階だけ）・強さ（記録がある物だけ）。
取り出さないもの: 音の高さそのもの・音程の数・和音（元の演奏の旋律は再現できない形にする。CLAUDE.md 1-1）。音声は使わない。
出典（どれも CC BY 4.0）:
  GuitarSet … Q. Xi ほか, ISMIR 2018. https://zenodo.org/records/3371780 （ソロの演奏 180本）
  EGSet12 … twelve real & original solo electric guitar performances. https://zenodo.org/records/11406378 （プロが作曲して弾いたエレキのオリジナル 12曲）
  Guitar-TECHS … H. Pedroza, W. Abreu, R. M. Corey, I. R. Roman, ICASSP 2025. https://zenodo.org/records/14963133 （P3 のオリジナルのソロ 12本。弦ごとの MIDI・強さつき）"""
import json, os, sys, collections, bisect
gs, eg, gt, out = sys.argv[1:5]; MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 120
STYLE = {"BN": "ボサノバ", "Funk": "ファンク", "Jazz": "ジャズ", "Rock": "ロック", "SS": "弾き語り風"}


def jams_notes(path):
    j = json.load(open(path)); notes = []; beats = []; tempo = None
    for a in j["annotations"]:
        if a["namespace"] == "note_midi":
            s = int(a["annotation_metadata"]["data_source"])
            for d in a["data"]: notes.append((d["time"], d["duration"], s, d["value"], None))
        elif a["namespace"] == "beat_position":
            beats = [d["time"] for d in a["data"]]
        elif a["namespace"] == "tempo": tempo = a["data"][0]["value"]
    return sorted(notes), sorted(beats), tempo


def midi_notes(path):
    import mido
    m = mido.MidiFile(path); notes = []; tempo = 120.0
    for tr in m.tracks:
        t = 0; on = {}
        for e in tr:
            t += e.time
            if e.type == "set_tempo": tempo = mido.tempo2bpm(e.tempo)
            elif e.type == "note_on" and e.velocity > 0: on[(e.channel, e.note)] = (t, e.velocity)
            elif e.type in ("note_off", "note_on") and (e.channel, e.note) in on:
                t0, v = on.pop((e.channel, e.note)); notes.append((t0, t - t0, e.channel, e.note, v))
    spt = 60.0 / tempo / m.ticks_per_beat
    return sorted((a * spt, b * spt, 5 - c if c <= 5 else 0, d, v) for a, b, c, d, v in notes), [], tempo      # Guitar-TECHS は ch0＝1弦（高い）なので、0＝6弦（低い）に直す


def windows(notes, beats, tempo):
    if not notes: return []
    if beats and len(beats) > 8: bt = beats
    else: spb0 = 60.0 / tempo; bt = [i * spb0 for i in range(int(notes[-1][0] / spb0) + 3)]
    spb = (bt[-1] - bt[0]) / (len(bt) - 1)
    def pos(t):
        i = max(0, min(len(bt) - 2, bisect.bisect_right(bt, t) - 1)); return i + (t - bt[i]) / (bt[i + 1] - bt[i])
    groups = []; cur = []
    for n in notes:
        if cur and (n[0] - cur[-1][0] > 0.05 or n[2] in [x[2] for x in cur]): groups.append(cur); cur = []
        cur.append(n)
    if cur: groups.append(cur)
    used = sorted({n[2] for n in notes}); lo, hi = used[0], used[-1]; wins = collections.defaultdict(list); prev = None
    for gi, g in enumerate(groups):
        st = [x[2] for x in g]; t0 = g[0][0]; p = pos(t0); top = max(x[3] for x in g)
        if len(g) == 1: d = "s"
        else:
            up = sum(1 for a, b in zip(st, st[1:]) if b < a); d = "d" if (len(st) - 1 - up) >= up else "u"
        dur = sorted(x[1] for x in g)[len(g) // 2]; nxt = groups[gi + 1][0][0] - t0 if gi + 1 < len(groups) else dur + 1
        art = "つなぐ" if dur >= nxt * 0.92 else "切る" if dur < nxt * 0.55 else "ふつう"
        mv = 0 if prev is None else (top - prev); move = "0" if round(mv) == 0 else ("+" if mv > 0 else "-") + ("1" if abs(mv) <= 2.5 else "2" if abs(mv) <= 4.5 else "3"); prev = top
        vel = [x[4] for x in g if x[4] is not None]
        w = int(p // 8); q = p - w * 8; slot = round(q * 4)
        if slot >= 32: w += 1; slot = 0; q -= 8
        e = {"slot": slot, "off": round((q - slot / 4) * spb * 1000, 1), "dir": d, "n": len(st), "lo": round((st[0] - lo) / max(1, hi - lo), 2), "hi": round((max(st) - lo) / max(1, hi - lo), 2),
             "spread": round((g[-1][0] - t0) * 1000, 1), "len": round(dur / spb, 3), "art": art, "move": move}
        if vel: e["vel"] = int(sum(vel) / len(vel))
        wins[w].append(e)
    return [sk for w, sk in sorted(wins.items()) if 5 <= len(sk) <= 40]


lib = []; seen = set()
def add(src_name, title, style, tempo, sk_list, per=2):
    got = 0
    for sk in sorted(sk_list, key=lambda sk: -len(sk)):
        key = tuple((s["slot"], s["dir"] == "s", s["move"][0]) for s in sk)
        if key in seen: continue
        seen.add(key); single = sum(1 for s in sk if s["dir"] == "s")
        lib.append({"id": "", "データ": src_name, "様式": style, "テンポ": int(round(tempo)), "元の演奏": title, "打数": len(sk), "単音": single, "和音": len(sk) - single, "16分のウラ": sum(1 for s in sk if s["slot"] % 2),
                    "つなぐ": sum(1 for s in sk if s["art"] == "つなぐ"), "切る": sum(1 for s in sk if s["art"] == "切る"), "強さあり": "vel" in sk[0], "strokes": sk})
        got += 1
        if got >= per: break


for fn in sorted(os.listdir(gt)):
    if fn.endswith(".mid"):
        n, b, t = midi_notes(os.path.join(gt, fn)); add("Guitar-TECHS", "P3_" + fn[:-4], "エレキのソロ", t, windows(n, b, t), per=4)
for fn in sorted(os.listdir(eg)):
    if fn.endswith(".jams"):
        n, b, t = jams_notes(os.path.join(eg, fn)); add("EGSet12", fn[:-5], "エレキ（和音と単音）", t, windows(n, b, t), per=3)
for fn in sorted(os.listdir(gs)):
    if fn.endswith("_solo.jams"):
        n, b, t = jams_notes(os.path.join(gs, fn)); rest = fn.split("_")[1]; sty = "".join(c for c in rest.split("-")[0] if c.isalpha())
        add("GuitarSet", fn[:-5], STYLE.get(sty, sty) + "のソロ", float(rest.split("-")[1]), windows(n, b, t), per=1)
by = collections.defaultdict(list)
for e in lib: by[e["データ"] + e["様式"]].append(e)
pick = []
while len(pick) < MAX and any(by.values()):
    for k in sorted(by):
        if by[k] and len(pick) < MAX: pick.append(by[k].pop(0))
for i, e in enumerate(pick): e["id"] = f"ph-{i + 1:03d}"
json.dump({"_説明": "ギターの単音まじりの弾き方の型（2小節・16分で32マス）。slot＝マス、off＝マスからのずれ（ミリ秒）、dir＝s 単音・d ダウンの和音・u アップの和音、n＝弦の本数、lo〜hi＝使った弦の中での位置（0＝低い弦）、len＝のばす拍、art＝つなぐ・ふつう・切る、move＝前の音からの動き（0＝同じ、+／-＝上がる／下がる、1＝となり・2＝1つとばし・3＝とぶ）、vel＝強さ（記録がある物だけ）。音の高さは入れていない",
           "_出典": "GuitarSet（Xi ほか, ISMIR 2018, zenodo 3371780）・EGSet12（zenodo 11406378）・Guitar-TECHS（Pedroza ほか, ICASSP 2025, zenodo 14963133）。どれも CC BY 4.0。型への変換: tools/guitar/phrase_patterns.py",
           "patterns": pick}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("型", len(lib), "種類 →", len(pick), "種類を保存:", dict(collections.Counter(e["データ"] + "・" + e["様式"] for e in pick)))
