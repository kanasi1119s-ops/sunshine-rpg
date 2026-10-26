# ボカロ曲25曲の品質チェック（2026-10-26 人間「言ったことが一通り終わったら全ての曲の品質チェックを行なって」）
# 使い方: python3 vb25_qc.py <版の名前（vb25-NN-slug-vX）> ...   （BGM と歌の版 vX vo の両方を見る）
# 見ること:
#   歌     … 歌の版に歌が混ざっているか（書き出しの記録）・言葉の途中の息つぎ（句の最後の1音だけ取り残される所）
#   段差   … 前奏の後半のいちばん大きい所と Aメロの頭（3dB 以上で ×）・場面ごとの大きさの段差（静かな場面を除き、前より 4dB 以上小さい所）
#   割れ   … ピーク（0.99 以上が 0.1% を超えたら ×）
#   こもり … 200〜500Hz の割合（全体より −6dB より大きいと「こもり」）
#   低音   … 40〜120Hz が全体より −14dB より小さいと「低音が細い」
#   単調   … 同じ種類の場面が続く所で、4小節ごとの音の色（帯域のバランス）がほとんど変わらない区間
#   点数   … 音質の点数（Audiobox Aesthetics の PQ。8 が目安）
import sys, json, os, re, subprocess
import numpy as np
from scipy.signal import butter, sosfilt

OUT = "/mnt/user-data/outputs/vb25"; Q = "/mnt/user-data/outputs/vbq"; SR = 22050


def load(mp3):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32)


def kw(x):
    return sosfilt(butter(2, 100, "highpass", fs=SR, output="sos"), x) + 0.6 * sosfilt(butter(1, 2000, "highpass", fs=SR, output="sos"), x)


def db(x):
    return 10 * np.log10(np.mean(x.astype(np.float64) ** 2) + 1e-12)


def band(x, lo, hi):
    return sosfilt(butter(4, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def score_of(base):
    try:
        for l in open(f"{OUT}/scores.tsv"):
            p = l.rstrip("\n").split("\t")
            if len(p) >= 5 and p[4] == base: s = p[2]
        return float(s)
    except Exception:
        return None


def check(base):
    mp3 = f"{OUT}/all/{base}.mp3"
    if not os.path.exists(mp3): return {"版": base, "結果": "ファイルなし"}
    x = load(mp3); m = kw(x)
    secs = json.load(open(f"{Q}/{base}.json.secs"))
    res = {"版": base, "点数": score_of(base)}
    probs = []
    # 歌
    if base.endswith("vo"):
        log = f"/tmp/vp25/cl-{base}.log"
        ok = os.path.exists(log) and "歌を混ぜました" in open(log).read()
        res["歌"] = "○" if ok else "？（記録なし）"
        if not ok: probs.append("歌が入っているか確かめられない")
        try:
            v = json.load(open(f"{Q}/{base}.json"))["vocals"][0]["notes"].split()
            gs, cur, rs = [], [], []
            for t in v:
                if t.startswith("R:"):
                    if float(t[2:]) >= 0.45 and cur: gs.append("".join(cur)); rs.append(float(t[2:])); cur = []
                    continue
                cur.append(t.split(":")[-1])
            frag = [f"{gs[i-1]}|{g}" for i, g in enumerate(gs) if i and len(g) <= 1 and len(gs[i - 1]) >= 2 and rs[i - 1] <= 1.0]
            res["息つぎ"] = "○" if not frag else "×" + " ".join(frag[:3])
            if frag: probs.append("言葉の途中の息つぎ")
        except Exception:
            pass
    # 前奏 → Aメロ
    T = next((s["t"] for s in secs if s["kind"] != "intro"), 0)
    if T > 4:
        w = [db(m[int(t * SR):int((t + 2) * SR)]) for t in np.arange(max(0, T - 10), T - 1.9, 0.5)]
        head = db(m[int((T + 0.2) * SR):int((T + 6) * SR)])
        d = max(w) - head
        res["前奏→A"] = f"{d:+.1f}dB"
        if d > 3: probs.append(f"前奏の後半より Aメロが {d:.1f}dB 小さい")
    # 場面の段差
    L = []
    for s, n in zip(secs, secs[1:]):
        seg = m[int((s["t"] + 0.3) * SR):int((n["t"] - 0.3) * SR)]
        if len(seg) < SR: L.append(None); continue
        w = int(0.1 * SR); rr = np.array([np.mean(seg[i:i + w] ** 2) for i in range(0, len(seg) - w, w)])
        rr = rr[rr > rr.max() * 1e-3]
        L.append(10 * np.log10(rr.mean() + 1e-12))
    steps = []
    for i in range(1, len(L)):
        k = secs[i]["kind"]
        if k in ("break", "bridge", "outro", "intro") or L[i] is None or L[i - 1] is None: continue
        if L[i - 1] - L[i] > 4: steps.append(f"{secs[i]['name']}({L[i-1]-L[i]:.1f})")
    res["段差"] = "○" if not steps else "×" + " ".join(steps)
    if steps: probs.append("場面の段差")
    # 割れ
    clip = float(np.mean(np.abs(x) >= 0.99))
    res["割れ"] = "○" if clip < 0.001 else f"×{clip*100:.2f}%"
    if clip >= 0.001: probs.append("割れ")
    # 帯域
    tot = db(x); mud = db(band(x, 200, 500)) - tot; low = db(band(x, 40, 120)) - tot; air = db(band(x, 6000, 10000)) - tot
    res["こもり"] = f"{mud:+.1f}"; res["低音"] = f"{low:+.1f}"; res["高域"] = f"{air:+.1f}"
    if mud > -6: probs.append("こもり（200〜500Hz が多い）")
    if low < -14: probs.append("低音が細い")
    # 単調: 同じ場面の中で、4小節ごとの帯域のバランスの変化が小さい所
    mono = []
    bpm_bar = None
    for s, n in zip(secs, secs[1:]):
        dur = n["t"] - s["t"]; nb = n["bar"] - s["bar"]
        if nb < 12 or s["kind"] in ("intro", "outro"): continue
        bar_s = dur / nb; chunks = []
        for q in range(0, nb - 3, 4):
            seg = x[int((s["t"] + q * bar_s) * SR):int((s["t"] + (q + 4) * bar_s) * SR)]
            spec = [db(band(seg, a, b)) for a, b in ((60, 200), (200, 800), (800, 3000), (3000, 9000))]
            chunks.append(np.array(spec) - np.mean(spec))
        if len(chunks) >= 3:
            ch = max(float(np.max(np.abs(c - chunks[0]))) for c in chunks[1:])
            if ch < 0.6: mono.append(s["name"])
    res["単調"] = "○" if not mono else "△" + "・".join(mono)
    res["問題"] = "、".join(probs) if probs else "なし"
    return res


if __name__ == "__main__":
    rows = []
    for b in sys.argv[1:]:
        for v in (b, b + "vo"):
            r = check(v); rows.append(r); print(json.dumps(r, ensure_ascii=False))
