#!/usr/bin/env python3
"""曲の一部分だけを、パートを段階的に足しながら書き出すための JSON を作る（どのパートを足した時に違和感が出るかを耳で探す）。
使い方: python3 tools/vt3/excerpt_stages.py <曲.json> <始まりの小節(0から)> <小節数> <出力フォルダ> "名前=役の名前に含まれる言葉,言葉|名前2=…"
  例: … 52 8 /tmp/st "1=キック,スネア,ハイハット,タム,シンバル,ベース,ギター（かき鳴らし）|2=+広い和音|3=+*"
  「+言葉」は前の段階に足す。「+*」は残り全部。"""
import json, re, sys, copy
src, b0, nb, out, spec = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
js = json.load(open(src)); beats = js["beats"]; t0, t1 = b0 * beats, (b0 + nb) * beats


def cut(notes):
    if notes.startswith("g:"): return "g:" + notes[2:][b0 * 16:(b0 + nb) * 16]      # ドラムは16分のマス目
    o = []; t = 0.0
    for tok in notes.split():
        m = re.match(r"^(.+?):([0-9.]+)(.*)$", tok); L = float(m[2]); a, b = max(t, t0), min(t + L, t1)
        if b - a > 1e-6:
            if t < t0 and not m[1].startswith("R"): o.append(f"R:{b - a:g}")          # 窓の前から鳴っている音は入れない
            else: o.append(f"{m[1]}:{b - a:g}{m[3]}")
        t += L
        if t >= t1: break
    return " ".join(o) or f"R:{t1 - t0:g}"


base = copy.deepcopy(js); base["chords"] = " ".join(js["chords"].split()[b0:b0 + nb]); base["sections"] = [{"kind": "chorus", "bars": nb}]
for p in base["parts"]:
    p["notes"] = cut(p["notes"]); p.pop("phrase", None)
    if "barGain" in p: p["barGain"] = p["barGain"][b0:b0 + nb]
prev = []
for st in spec.split("|"):
    name, words = st.split("="); add = words.startswith("+"); words = words.lstrip("+").split(",")
    sel = [p for p in base["parts"] if "*" in words or any(w in p["role"] for w in words)]
    if add: sel = prev + [p for p in sel if p not in prev]
    prev = sel; j = dict(base); j["parts"] = sel; j["title"] = f"stage{name}"; json.dump(j, open(f"{out}/stage{name}.json", "w"), ensure_ascii=False)
    print(name, len(sel), "パート")
