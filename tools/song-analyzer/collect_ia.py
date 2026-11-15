#!/usr/bin/env python3
"""お手本集め: Internet Archive のネットレーベル（レーベル本人が自由なライセンスで出している作品）から1曲ずつ取ってきて分析し、カルテ（数字）だけを残す。
使い方: python3 tools/song-analyzer/collect_ia.py <出力フォルダ> ジャンル:識別子 [ジャンル:識別子 …]
決まり: ライセンスが CC BY・CC BY-SA・CC0 のどれかで、ネットレーベルの集まり（collection: netlabels）に入っている作品だけ。それ以外は取らずに飛ばす。
        音のファイルは分析したら消す。出どころ（作者・レーベル・ライセンス・URL）をカルテに書く。"""
import sys, os, json, subprocess, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A
OK = ("creativecommons.org/licenses/by/", "creativecommons.org/licenses/by-sa/", "creativecommons.org/publicdomain/zero/")
out = sys.argv[1]; os.makedirs(out, exist_ok=True); tmp = "/tmp/sa/ref"; os.makedirs(tmp, exist_ok=True)
def secs(x):
    try:
        if ":" in str(x): p = [float(q) for q in str(x).split(":")]; return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
        return float(x)
    except Exception: return 0
for spec in sys.argv[2:]:
    genre, ident = spec.split(":", 1)
    try:
        d = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}", timeout=60)); m = d["metadata"]; lic = str(m.get("licenseurl", "")); col = m.get("collection", []); col = [col] if isinstance(col, str) else col
        if not any(o in lic for o in OK) or "netlabels" not in col: print(f"× {ident}: 条件に合わない（{lic}・{col[:3]}）"); continue
        cands = [f for f in d["files"] if f["name"].lower().endswith(".mp3") and "_64kb" not in f["name"] and 110 <= secs(f.get("length", 0)) <= 400]
        if not cands: print(f"× {ident}: ちょうどよい長さの曲がない"); continue
        f = cands[min(1, len(cands) - 1)] if len(cands) > 2 else cands[0]      # アルバムの2曲目（1曲目は前奏だけのことがある）
        path = os.path.join(tmp, ident + ".mp3"); urllib.request.urlretrieve(f"https://archive.org/download/{ident}/" + urllib.parse.quote(f["name"]), path)
        name = f"ref-{genre}-{ident}"; r = A.analyze(path, None, name, None)
        r["source"] = dict(genre=genre, title=str(f.get("title") or f["name"]), creator=str(f.get("creator") or m.get("creator")), release=str(m.get("title")), label=[c for c in col if c not in ("netlabels", "audio") and not c.startswith("fav-")][:1],
                           license=lic, url=f"https://archive.org/details/{ident}", uploader_note="ネットレーベルの集まりに入っている作品")
        json.dump(r, open(os.path.join(out, name + ".karte.json"), "w"), ensure_ascii=False); A.chart(r, os.path.join("/tmp/sa", name + ".karte.png")); os.remove(path)
        print(f"○ {genre} {ident}: {r['source']['creator']}「{r['source']['title']}」 {lic.split('org/')[-1]}  テンポ {r['tempo']}・{r['seconds']}秒"); sys.stdout.flush()
    except Exception as e: print(f"× {ident}: {type(e).__name__} {e}"); sys.stdout.flush()
