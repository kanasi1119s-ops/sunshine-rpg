#!/usr/bin/env python3
"""書き出した曲（WAV）の「仕上がり」を、数値で合否判定する検査（2026-10-02）。

使い方:
    python3 tools/audio-check/producer-check.py 曲.wav [--genre normal|loud|soft] [--json]
終了コード: 1つでも「×」（必須の項目）があれば 1。

何を見るか（人の耳の代わりではない。耳で聴く前に、はっきりした欠点を機械で落とす）:
  必須（×だと書き出し失敗）
    peak      ピークが -1.0dBTP 以下（圧縮して配信しても割れない）
    clip      頭打ち（±0.999 以上）のサンプルが 0 個
    dc        直流成分（波形の偏り）がない
    lowmono   120Hz より下が左右でそろっている（相関 0.95 以上＝低音が真ん中）
    start     曲の頭に無音が 0.3秒以上ない／頭の1サンプルが大きくない（ループでプチッと鳴らない）
    seam      ループのつなぎ目: 曲の終わり（残響の尾を除く）と頭の音量差が 9dB 以内
    harsh     4〜8kHz（耳に痛い帯域）が、全体に対して -13dB より大きくない
  目安（△は注意。ジャンルで基準が違う）
    lufs      音量（ジャンルごとの範囲）
    crest     ピークと平均の差（詰めすぎると疲れる）
    corr      左右の相関（真ん中に寄りすぎ／逆相に近い）
    tail      残響の尾が 4秒以内
    lra       曲の中の音量の幅（起伏）
ジャンル: normal＝ふつう（BGM全般）、loud＝ラウドメタル・ロック・ダンス（大きく詰めてよい）、soft＝繊細・アンビエント（小さく静か）
"""
import json
import sys

import numpy as np

import analyze as A

GENRES = {
    "normal": dict(lufs=(-17.0, -9.0), crest=12.0, corr=(0.35, 0.92)),
    "loud": dict(lufs=(-12.0, -5.0), crest=9.0, corr=(0.35, 0.97)),
    "soft": dict(lufs=(-23.0, -12.0), crest=13.0, corr=(0.2, 0.9)),
}


def db(x):
    return 20 * np.log10(max(float(x), 1e-12))


def lowpass_fft(x, cutoff):
    spec = np.fft.rfft(x)
    freq = np.fft.rfftfreq(len(x), 1 / A.SR)
    spec[freq > cutoff] = 0
    return np.fft.irfft(spec, len(x))


def check(path, genre="normal"):
    g = GENRES[genre]
    x = A.load(path)
    r = A.analyze(path)
    mid = x.mean(1)
    res = []  # (id, must, ok, 値の説明)
    add = lambda i, must, ok, text: res.append((i, must, bool(ok), text))

    add("peak", True, r["TP"] <= -0.95, f"TP {r['TP']:.1f}dBTP（-1.0 以下）")
    clipped = int((np.abs(x) >= 0.999).sum())
    add("clip", True, clipped == 0, f"頭打ち {clipped} 個")
    dc = float(abs(mid.mean()))
    add("dc", True, dc < 0.005, f"直流成分 {dc:.4f}")

    n = min(len(x), A.SR * 120)  # 低音の相関は先頭2分で見る（計算を軽くする）
    lo_l, lo_r = lowpass_fft(x[:n, 0], 120), lowpass_fft(x[:n, 1], 120)
    denom = np.sqrt((lo_l ** 2).sum() * (lo_r ** 2).sum()) + 1e-12
    low_corr = float((lo_l * lo_r).sum() / denom)
    add("lowmono", True, low_corr >= 0.95, f"120Hz 未満の左右の相関 {low_corr:.3f}（0.95 以上）")

    env = np.abs(mid)
    lead = int(np.argmax(env > 10 ** (-60 / 20)))
    add("start", True, lead < 0.3 * A.SR and abs(float(mid[lead])) < 0.05, f"頭の無音 {lead / A.SR:.2f}秒、最初の音 {abs(float(mid[lead])):.3f}")

    # 曲の終わり: -60dB より大きい最後の場所まで（残響の尾の無音を除く）。尾の途中は小さいので、終わりの手前2秒と頭2秒の音量を比べる
    last = len(mid) - int(np.argmax(env[::-1] > 10 ** (-45 / 20)))
    w = 2 * A.SR
    head = db(np.sqrt(np.mean(mid[lead:lead + w] ** 2)))
    body_end = db(np.sqrt(np.mean(mid[max(0, last - w - A.SR):max(w, last - A.SR)] ** 2)))
    add("seam", True, abs(head - body_end) <= 9.0, f"頭 {head:.1f}dB／終わり {body_end:.1f}dB（差 {abs(head - body_end):.1f}dB。9 以内）")

    harsh = r["band_dB"]["presence"]
    add("harsh", True, harsh <= -13.0, f"4〜8kHz の量 {harsh:.1f}dB（-13 以下）")

    lo, hi = g["lufs"]
    add("lufs", False, lo <= r["I"] <= hi, f"音量 {r['I']:.1f}LUFS（{genre}: {lo}〜{hi}）")
    add("crest", False, r["crest_dB"] >= g["crest"], f"ピークと平均の差 {r['crest_dB']:.1f}dB（{g['crest']} 以上）")
    add("corr", False, g["corr"][0] <= r["corr"] <= g["corr"][1], f"左右の相関 {r['corr']:.2f}（{g['corr'][0]}〜{g['corr'][1]}）")
    tail = r.get("tail_s")
    add("tail", False, tail is None or tail <= 4.0, f"残響の尾 {tail}秒（4 以内）")
    add("lra", False, r["LRA"] >= 2.0, f"音量の幅 {r['LRA']:.1f}LU（2 以上）")
    return res, r


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    genre = "normal"
    if "--genre" in sys.argv:
        genre = sys.argv[sys.argv.index("--genre") + 1]
        args = [a for a in args if a != genre]
    failed = False
    out = {}
    for f in args:
        res, r = check(f, genre)
        out[f] = [dict(id=i, must=m, ok=o, text=t) for i, m, o, t in res]
        if "--json" not in sys.argv:
            print(f"\n■ {f}（ジャンル: {genre}）")
            for i, must, ok, text in res:
                mark = "○" if ok else ("×" if must else "△")
                print(f"  {mark} {i:8s} {text}")
        failed |= any(m and not o for _, m, o, _ in res)
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    sys.exit(1 if failed else 0)
