#!/usr/bin/env python3
"""本物のシンバルの効果音（逆再生シンバル・スウェル・長い一打）の素材を作る前処理。合成音（シンセのライザーなど）は使わない。

使い方: python3 -I tools/soundfont/cymbal-fx-prep.py <作業フォルダ> --oslo <オスロ大学のシンバル録音の WAV フォルダ>
  → <作業フォルダ>/out/*.wav（44.1kHz・ステレオ・32bit 浮動小数）と list.json を書く。SF3 にするのは build-cymbal-fx.mjs。

元の録音（どちらも CC BY 4.0・クレジット必要）:
 - CrocellKit（DrumGizmo）: クラッシュ2枚・チャイナ2枚の強い一打を、ファイルの最後まで（8〜10秒）zip から Range で取り出し、
   OH 左右・OH 真ん中・部屋 左右 をまぜてステレオにする（dg-extract.py の道具を使う）
 - Cymbal percussion（オスロ大学 fourMs Lab、2011。https://zenodo.org/records/21710617 の WAV.zip）: サスペンデッドシンバル。
   マレットのロールのクレッシェンド（18秒）・ディミヌエンド（21秒）・ふちの強打
作るもの:
 - 逆再生（クラッシュ・チャイナ）: 一打を逆にし、「山（打った瞬間）」が音の最後に来るようにする。長さ 0.25〜4秒の 9 段（√2 倍ずつ）。
   頭は 25% かけてなめらかに入り、山のあと 8ms で止める（すぐあとに本物の一打を重ねる前提）。
 - スウェル（ロールのクレッシェンド）: クレッシェンドの録音の「いちばん大きい所」で終わるよう、その手前の長さぶんを切る。0.25〜8秒の 11 段。
 - 一打（長い）: クラッシュ・チャイナ・サスペンデッドのふちの強打・ロールのディミヌエンド。余韻は切らない（最後の 1 秒だけなめらかに消す）。
"""
import importlib.util, json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

args = sys.argv[1:]
work = args[0]
oslo = args[args.index("--oslo") + 1]
os.makedirs(os.path.join(work, "out"), exist_ok=True)
spec = importlib.util.spec_from_file_location("dgx", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dg-extract.py"))
dgx = importlib.util.module_from_spec(spec); spec.loader.exec_module(dgx)
KIT = dgx.KITS["crocell"]
SR = 44100
LENS = [0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0, 5.6, 8.0]


def crocell_hit(inst, idx):
    """CrocellKit の1打を最後まで取り出し、OH・部屋のマイクをまぜたステレオ（44.1kHz）にする。"""
    cache = os.path.join(work, f"{inst}-{idx}.npy")
    if os.path.exists(cache):
        return np.load(cache)
    import xml.etree.ElementTree as ET
    cd = dgx.central_directory(KIT["url"])
    xml = ET.fromstring(dgx.head_of(KIT["url"], cd[f"{KIT['prefix']}{inst}/{inst}.xml"], 10 ** 7))
    smp = next(s for s in xml.iter("sample") if s.get("name") == f"{inst}-{idx}")
    ch = {a.get("channel"): int(a.get("filechannel")) - 1 for a in smp.iter("audiofile")}
    file = next(a.get("file") for a in smp.iter("audiofile"))
    entry = cd[f"{KIT['prefix']}{inst}/{file}"]
    fmt, raw = dgx.parse_wav(dgx.head_of(KIT["url"], entry, entry[2]))
    tag, nch, sr, bits = fmt
    x = np.frombuffer(raw[: len(raw) - len(raw) % (nch * 4)], dtype="<f4").reshape(-1, nch).astype(np.float64)
    L = x[:, ch["OHLeft"]] + 0.4 * x[:, ch["AmbLeft"]] + 0.35 * x[:, ch["OHCenter"]]
    R = x[:, ch["OHRight"]] + 0.4 * x[:, ch["AmbRight"]] + 0.35 * x[:, ch["OHCenter"]]
    st = np.stack([resample_poly(L, 147, 160), resample_poly(R, 147, 160)], 1)
    np.save(cache, st)
    return st


def mono_file(name):
    x, sr = sf.read(os.path.join(oslo, name), dtype="float64")
    if x.ndim > 1:
        x = x.mean(1)
    if sr != SR:
        x = resample_poly(x, SR, sr)
    return np.stack([x, x], 1)


def fade_in(y, frac):
    n = max(1, int(len(y) * frac)); y[:n] *= (np.linspace(0, 1, n) ** 2)[:, None]; return y


def fade_out(y, sec):
    n = min(len(y), int(sec * SR)); y[-n:] *= (np.linspace(1, 0, n) ** 2)[:, None]; return y


def onset(y):
    e = np.abs(y).max(1); return int(np.argmax(e > e.max() * 0.3))


items = []


def put(name, y, kind, length=None):
    y = y / max(1e-9, np.abs(y).max()) * 0.7  # 山を約 -3dB にそろえる
    sf.write(os.path.join(work, "out", name + ".wav"), y.astype("float32"), SR, subtype="FLOAT")
    items.append({"name": name, "kind": kind, "len": length, "sec": round(len(y) / SR, 3)})


# 逆再生
for fam, inst, idx in [("revcrash", "CrashL", 24), ("revchina", "ChinaR", 24)]:
    hit = crocell_hit(inst, idx)
    on = onset(hit)
    body = hit[max(0, on - int(0.004 * SR)):]
    for L in LENS[:9]:
        seg = body[: int(L * SR)][::-1].copy()  # 打った瞬間が最後に来る
        seg = fade_in(seg, 0.25)
        seg = np.concatenate([seg, body[int(0.004 * SR): int(0.012 * SR)][: int(0.008 * SR)] * np.linspace(1, 0, int(0.008 * SR))[:, None]])
        put(f"{fam}-{L}", seg, fam, L)
# スウェル（ロールのクレッシェンド。いちばん大きい所で終わる）
roll = mono_file("suspeso_tremolo_cresc_soft2strong0001_video2.wav")
env = np.convolve(np.abs(roll[:, 0]), np.ones(2205) / 2205, mode="same")
peak = int(np.argmax(env))
for L in LENS:
    a = max(0, peak - int(L * SR))
    seg = fade_in(roll[a:peak].copy(), 0.15)
    put(f"swell-{L}", seg, "swell", L)
# 一打（長い）
for name, inst, idx in [("hit-crash", "CrashL", 24), ("hit-crash2", "CrashR", 20), ("hit-china", "ChinaR", 24), ("hit-china2", "ChinaL", 15)]:
    h = crocell_hit(inst, idx); h = h[max(0, onset(h) - int(0.003 * SR)):]
    put(name, fade_out(h.copy(), 1.0), "hit")
put("hit-susp", fade_out(mono_file("suspeso_attack_kant_strong0001_video2.wav")[: 12 * SR].copy(), 1.0), "hit")
put("roll-dim", fade_out(mono_file("suspeso_tremolo_diminuendo0001_video2.wav").copy(), 1.5), "hit")
json.dump({"lens": LENS, "items": items}, open(os.path.join(work, "out", "list.json"), "w"), ensure_ascii=False, indent=1)
print("書き出し:", len(items), "個。通信:", f"{dgx.fetched[0] / 1e6:.0f}MB")
