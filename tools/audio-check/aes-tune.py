#!/usr/bin/env python3
"""曲の別バージョンをまとめて書き出し、Audiobox Aesthetics の点数（PQ=制作品質）で比べる。
耳の確認ではなく目安。人間の指示（禁止の音・「ドラムを大きく」など）は点数より優先する。

使い方:
  python3 tools/audio-check/aes-tune.py <元の曲.json> <試す案.json> --out <作業フォルダ> [--flags "--drums muldjord --bass pick --master-preset rock-clean"] [-j 2]

試す案.json（配列。1つが1バージョン）:
  [{"name": "a", "db": {"drums": -3, "bass": 2}, "set": {"guitars": {"ampDrive": 0.5, "amp": "hardrock"}},
    "flags": "--guitar fsbs-direct", "drop": ["part:9"]}]
  グループ: drums / bass / guitars / keys / melody / all / part:<番号>（0から） / inst:<楽器名>
  db: gainDb に足す（dB）。set: パートの項目を上書き。flags: --flags に足す（同じ名前は上書き）。drop: パートを消す。top: 曲全体の項目を上書き（drumMix は太鼓ごとに混ぜる）。
結果: <作業フォルダ>/results.csv（名前,PQ,CE,CU,PC,案）と各 mp3。WAV は容量節約のため消す。
必要なもの（初回）: pip install --break-system-packages audiobox_aesthetics、
  torch と torchaudio の CPU 版をそろえる（例: pip install torch==2.11.0 torchaudio==2.11.0 --index-url https://download.pytorch.org/whl/cpu）。
  モデルは HF_HOME=/tmp/hf に落ちる（約1GB）。
"""
import argparse, copy, glob, json, os, shlex, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DRUMS = {"kick", "snare", "hihat", "crash", "ride", "tom", "drums", "perc", "clap", "shaker", "tambourine", "cowbell"}
BASS = {"bass", "slap", "synthBass", "fretless", "acousticBass"}
GUITARS = {"guitar", "distGuitar", "crunch", "leadGuitar", "cleanGuitar", "jazzGuitar", "acousticGuitar", "nylonGuitar"}
KEYS = {"piano", "keys", "organ", "epiano", "rhodes", "pad", "synth"}

def match(group, i, p):
    inst = p.get("instrument", "")
    if group == "all": return True
    if group.startswith("part:"): return i == int(group[5:])
    if group.startswith("inst:"): return inst == group[5:]
    return {"drums": inst in DRUMS, "bass": inst in BASS, "guitars": inst in GUITARS,
            "keys": inst in KEYS, "melody": "メロ" in p.get("role", "") or "lead" in inst.lower()}.get(group, False)

def merge_flags(base, extra):
    out, toks = {}, shlex.split(base) + shlex.split(extra or "")
    order, k = [], None
    for t in toks:
        if t.startswith("--"):
            k = t; order.append(k) if k not in out else None; out[k] = None
        elif k: out[k] = t
    res = []
    for k in order: res += [k] + ([out[k]] if out[k] is not None else [])
    return res

def make(base, v):
    j = copy.deepcopy(base); P = j["parts"]
    for g, d in (v.get("db") or {}).items():
        for i, p in enumerate(P):
            if match(g, i, p): p["gainDb"] = round(p.get("gainDb", 0) + d, 2)
    for g, fields in (v.get("set") or {}).items():
        for i, p in enumerate(P):
            if match(g, i, p): p.update(fields)
    for k, val in (v.get("top") or {}).items():
        if isinstance(val, dict) and isinstance(j.get(k), dict):
            for kk, vv in val.items():
                j[k][kk] = {**j[k].get(kk, {}), **vv} if isinstance(vv, dict) and isinstance(j[k].get(kk), dict) else vv
        else: j[k] = val
    drop = v.get("drop") or []
    j["parts"] = [p for i, p in enumerate(P) if not any(match(g, i, p) for g in drop)]
    return j

def score(wav):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools/audio-check/aes-score.py"), wav], capture_output=True, text=True,
                       env={**os.environ, "HF_HOME": os.environ.get("HF_HOME", "/tmp/hf")}, cwd="/tmp")
    line = [l for l in r.stdout.splitlines() if "{" in l]
    if not line: raise RuntimeError(r.stderr[-400:])
    return json.loads(line[-1][line[-1].index("{"):].replace("'", '"'))

def run(args, base, v):
    name = v["name"]; d = os.path.join(args.out, name); os.makedirs(d, exist_ok=True)
    jp = os.path.join(d, name + ".json")
    json.dump(make(base, v), open(jp, "w"), ensure_ascii=False)
    r = subprocess.run(["node", "tools/composer/song.mjs", "build", jp, "--wav", "--out", d + "/o"] + merge_flags(args.flags, v.get("flags")),
                       cwd=ROOT, capture_output=True, text=True)
    w = glob.glob(d + "/o/*.wav")
    if not w: print(name, "書き出し失敗", r.stdout[-300:], r.stderr[-300:], flush=True); return
    s = score(w[0])
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", w[0], "-b:a", "192k", os.path.join(d, name + ".mp3")])
    os.remove(w[0])
    with open(os.path.join(args.out, "results.csv"), "a") as f:
        f.write(f"{name},{s['PQ']:.2f},{s['CE']:.2f},{s['CU']:.2f},{s['PC']:.2f},{json.dumps(v, ensure_ascii=False)}\n")
    print(name, {k: round(x, 2) for k, x in s.items()}, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("song"); ap.add_argument("variants"); ap.add_argument("--out", required=True)
    ap.add_argument("--flags", default="--drums muldjord --bass pick --master-preset rock-clean")
    ap.add_argument("-j", type=int, default=2)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    base = json.load(open(a.song)); vs = json.load(open(a.variants))
    with ThreadPoolExecutor(a.j) as ex: list(ex.map(lambda v: run(a, base, v), vs))
    rows = [l.split(",", 5) for l in open(os.path.join(a.out, "results.csv"))]
    rows.sort(key=lambda r: -float(r[1]))
    print("\n点数の高い順（PQ=制作品質）:")
    for r in rows[:8]: print(f"  {r[0]}: PQ {r[1]}  楽しさ {r[2]}  {r[5].strip()}")

if __name__ == "__main__":
    main()
