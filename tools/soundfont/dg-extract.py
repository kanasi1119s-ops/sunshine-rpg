#!/usr/bin/env python3
"""DrumGizmo 本家の形式のドラムキット（CrocellKit など）から、必要な打音の頭だけを取り出し、
build-drums.mjs が読める形（sfzinstruments 版 Muldjord Kit と同じ並び）に直す前処理。

使い方:
  python3 -I tools/soundfont/dg-extract.py --kit crocell --xml <楽器のXMLの置き場> --samples <出力: 録音の置き場> [--data <出力: Data の置き場>] [--jobs 6]

- 元の zip（5.6GB）は落とさない。zip の目次（最後の数MB）だけを HTTP の Range で読み、
  選んだ打音の WAV について、ファイルの頭から「必要な秒数」ぶんの圧縮データだけを1回の Range 要求で取り、その場で展開する。
- DrumGizmo の楽器の XML（<sample power=...> と、マイクごとの <audiofile channel=... filechannel=...>）から、
  power（打音の強さ）の順に並べて、強さの層を選ぶ（層ごとに RR 個の候補）。
- 出力:
  - <samples>/<楽器>/<番号>-<楽器>-<マイク>.flac（24bit。使うマイクだけ。部屋・OH は AmbL/AmbR/OHL/OHR/OHC に名前をそろえる）
  - <data>/macro.txt（強さの層の範囲 $vNNNl / $vNNNh）と <data>/region/<楽器>.txt（<region> 行）
    → build-drums.mjs の layers() がそのまま読める
元の録音（取り出した FLAC）はリポジトリに入れない（大きい・元の配布物の一部のため）。Data/ だけを assets-src に置く。
"""
import argparse, json, os, re, struct, subprocess, sys, threading, urllib.request, zlib
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

# キットごとの設定。layers＝強さの層の数、rr＝層ごとの候補の数、sec＝取り出す長さ（秒）、close＝残す近接マイク
KITS = {
    "crocell": {
        "url": "https://drumgizmo.org/kits/CrocellKit/CrocellKit1_1.zip",
        "prefix": "CrocellKit/",
        "rename": {"AmbLeft": "AmbL", "AmbRight": "AmbR", "OHLeft": "OHL", "OHRight": "OHR", "OHCenter": "OHC"},
        "inst": {
            "KDrumL": {"layers": 8, "rr": 2, "sec": 1.1, "close": ["KDrumInside", "KDrumOutside"]},
            "KDrumR": {"layers": 8, "rr": 2, "sec": 1.1, "close": ["KDrumInside", "KDrumOutside"]},
            "Snare": {"layers": 8, "rr": 2, "sec": 1.1, "close": ["SnareTop", "SnareBottom"]},
            "SnareRimShot": {"layers": 4, "rr": 1, "sec": 1.1, "close": ["SnareTop", "SnareBottom"]},
            "SnareRim": {"layers": 3, "rr": 1, "sec": 0.6, "close": ["SnareTop", "SnareBottom"]},
            "SnareRest": {"layers": 3, "rr": 1, "sec": 0.7, "close": ["SnareTop", "SnareBottom"]},
            "Tom1": {"layers": 6, "rr": 1, "sec": 1.9, "close": ["Tom1"]},
            "Tom2": {"layers": 6, "rr": 1, "sec": 1.9, "close": ["Tom2"]},
            "FTom1": {"layers": 6, "rr": 1, "sec": 2.1, "close": ["FTom1"]},
            "FTom2": {"layers": 6, "rr": 1, "sec": 2.1, "close": ["FTom2"]},
            "HihatClosed": {"layers": 5, "rr": 2, "sec": 0.7, "close": ["Hihat"]},
            "HihatSemiOpen": {"layers": 4, "rr": 1, "sec": 1.6, "close": ["Hihat"]},
            "HihatOpen": {"layers": 4, "rr": 1, "sec": 2.6, "close": ["Hihat"]},
            "HihatPedal": {"layers": 3, "rr": 1, "sec": 0.6, "close": ["Hihat"]},
            "ChinaL": {"layers": 5, "rr": 1, "sec": 4.6, "close": []},
            "ChinaR": {"layers": 5, "rr": 1, "sec": 4.6, "close": []},
            "SplashL": {"layers": 4, "rr": 1, "sec": 3.2, "close": []},
            "SplashR": {"layers": 4, "rr": 1, "sec": 3.2, "close": []},
            "CrashL": {"layers": 5, "rr": 1, "sec": 5.6, "close": []},
            "CrashR": {"layers": 5, "rr": 1, "sec": 5.6, "close": []},
            "CrashRXtra": {"layers": 4, "rr": 1, "sec": 5.6, "close": []},
            "CrashLStopped": {"layers": 3, "rr": 1, "sec": 1.3, "close": []},
            "CrashRStopped": {"layers": 3, "rr": 1, "sec": 1.3, "close": []},
            "RideR": {"layers": 5, "rr": 2, "sec": 3.6, "close": ["Ride"]},
            "RideRBell": {"layers": 4, "rr": 1, "sec": 3.6, "close": ["Ride"]},
        },
    },
}

fetched = [0]
lock = threading.Lock()


def http_range(url, a, b):
    req = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
    for attempt in range(4):
        try:
            d = urllib.request.urlopen(req, timeout=120).read()
            with lock:
                fetched[0] += len(d)
            return d
        except Exception as e:  # 通信の一時的な失敗はやり直す
            if attempt == 3:
                raise
            print("  やり直し:", e, file=sys.stderr)


def central_directory(url):
    """zip（ZIP64 を含む）の目次を読み、{名前: (ローカルヘッダの位置, 圧縮後の大きさ, 元の大きさ, 圧縮方式)} を返す。"""
    n = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD")).headers["Content-Length"])
    tail = http_range(url, max(0, n - 70000), n - 1)
    i = tail.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    j = tail.rfind(b"PK\x06\x06")  # ZIP64 の終端
    if j >= 0:
        cd_size, cd_off = struct.unpack("<QQ", tail[j + 40:j + 56])
    cd = http_range(url, cd_off, cd_off + cd_size - 1)
    out, p = {}, 0
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        method = struct.unpack("<H", cd[p + 10:p + 12])[0]
        csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
        nl, el, cl = struct.unpack("<HHH", cd[p + 28:p + 34])
        off = struct.unpack("<I", cd[p + 42:p + 46])[0]
        name = cd[p + 46:p + 46 + nl].decode("utf8")
        extra = cd[p + 46 + nl:p + 46 + nl + el]
        q = 0
        while q + 4 <= len(extra):
            hid, hl = struct.unpack("<HH", extra[q:q + 4])
            if hid == 1:
                vals, r = [], q + 4
                for flag in (usize, csize, off):
                    if flag == 0xFFFFFFFF:
                        vals.append(struct.unpack("<Q", extra[r:r + 8])[0]); r += 8
                    else:
                        vals.append(None)
                usize = vals[0] or usize; csize = vals[1] or csize; off = vals[2] or off
            q += 4 + hl
        out[name] = (off, csize, usize, method)
        p += 46 + nl + el + cl
    return out


def head_of(url, entry, nbytes):
    """zip の1つのファイルの、頭の nbytes（展開後）だけを取り出す。"""
    off, csize, usize, method = entry
    lh = http_range(url, off, off + 29)
    nl, el = struct.unpack("<HH", lh[26:30])
    start = off + 30 + nl + el
    want = min(csize, nbytes + 65536) if method == 8 else min(csize, nbytes)
    data = http_range(url, start, start + want - 1)
    if method == 0:
        return data[:nbytes]
    d = zlib.decompressobj(-15)
    return d.decompress(data, nbytes)


def parse_wav(b):
    """多チャンネルの WAV（32bit 浮動小数／24bit／16bit）の頭を読み、(チャンネル数, サンプルレート, 形式, 音のデータ) を返す。"""
    assert b[:4] == b"RIFF" and b[8:12] == b"WAVE"
    p, fmt = 12, None
    while p + 8 <= len(b):
        cid, size = b[p:p + 4], struct.unpack("<I", b[p + 4:p + 8])[0]
        if cid == b"fmt ":
            tag, ch, sr = struct.unpack("<HHI", b[p + 8:p + 16])
            bits = struct.unpack("<H", b[p + 22:p + 24])[0]
            if tag == 0xFFFE:
                tag = struct.unpack("<H", b[p + 32:p + 34])[0]
            fmt = (tag, ch, sr, bits)
        if cid == b"data":
            return fmt, b[p + 8:]
        p += 8 + size + (size & 1)
    raise ValueError("data が見つかりません")


def write_flac(path, raw, fmt, ch_index):
    """多チャンネルの生データから1チャンネルを取り出し、24bit の FLAC に書く（ffmpeg）。"""
    tag, ch, sr, bits = fmt
    codec = {(3, 32): "f32le", (1, 24): "s24le", (1, 16): "s16le", (1, 32): "s32le"}[(tag, bits)]
    frame = ch * bits // 8
    usable = len(raw) - len(raw) % frame
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", codec, "-ar", str(sr), "-ac", str(ch), "-i", "-",
                    "-af", f"pan=mono|c0=c{ch_index}", "-c:a", "flac", "-sample_fmt", "s32", "-bits_per_raw_sample", "24", path],
                   input=raw[:usable], check=True)


def pick_layers(samples, layers, rr):
    """power の順に並べ、強さの層ごとに rr 個の打音を選ぶ。いちばん弱い 1 割は使わない（弱すぎて曲では聞こえないため）。"""
    s = sorted(samples, key=lambda x: x["power"])
    n = len(s)
    lo = int(n * 0.1) if n >= 10 else 0
    pool = s[lo:]
    m = len(pool)
    out = []
    for k in range(layers):
        a = int(m * k / layers)
        b = max(a + 1, int(m * (k + 1) / layers))
        group = pool[a:b]
        # 層の中で強い方から（上の層ほど「その層の代表」になるよう、中央付近から選ぶ）
        mid = len(group) // 2
        order = sorted(range(len(group)), key=lambda i: abs(i - mid))
        out.append([group[i] for i in order[:max(1, min(rr, len(group)))]])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", default="crocell")
    ap.add_argument("--xml", required=True, help="楽器の XML の置き場（<名前>.xml か <キット>__<名前>__<名前>.xml）")
    ap.add_argument("--samples", required=True)
    ap.add_argument("--data", default=None)
    ap.add_argument("--only", default="", help="カンマ区切りで、この楽器だけ")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    kit = KITS[a.kit]
    data_dir = a.data or os.path.join(a.samples, "..", "Data")
    os.makedirs(os.path.join(data_dir, "region"), exist_ok=True)
    print("zip の目次を読みます…")
    cd = central_directory(kit["url"])
    print("ファイル数:", len(cd))
    macro, jobs = [], []
    vnum = 100
    insts = [x for x in kit["inst"] if not a.only or x in a.only.split(",")]
    for inst in insts:
        cfg = kit["inst"][inst]
        cand = [os.path.join(a.xml, f"{inst}.xml"), os.path.join(a.xml, f"{kit['prefix'].strip('/')}__{inst}__{inst}.xml")]
        xml = next(p for p in cand if os.path.exists(p))
        root = ET.parse(xml).getroot()
        samples = []
        for smp in root.iter("sample"):
            files = {af.get("channel"): (af.get("file"), int(af.get("filechannel"))) for af in smp.iter("audiofile")}
            idx = int(re.search(r"(\d+)$", smp.get("name")).group(1))
            samples.append({"idx": idx, "power": float(smp.get("power")), "files": files})
        picked = pick_layers(samples, cfg["layers"], cfg["rr"])
        lines = [f"#define $instr {inst}", f"group_label=$instr", ""]
        L = len(picked)
        base_v = 100 * (list(kit["inst"]).index(inst) + 1)
        for k, group in enumerate(picked):
            vnum = base_v + k
            lo = 1 + round(126 * k / L); hi = round(126 * (k + 1) / L) + (1 if k == L - 1 else 0)
            hi = min(127, max(lo, hi))
            macro.append(f"#define $v{vnum}l {lo}        #define $v{vnum}h {hi}")
            for j, smp in enumerate(group):
                lines.append(f"<region> lovel=$v{vnum}l hivel=$v{vnum}h region_label={smp['idx']} sample=$instr/{smp['idx']}-$instr-$mic.$ext power={smp['power']:.6g} seq_position={j + 1}")
                jobs.append((inst, cfg, smp))
        with open(os.path.join(data_dir, "region", inst + ".txt"), "w") as f:
            f.write("\n".join(lines) + "\n")
        print(inst, "打音", len(samples), "→ 層", L, "× 候補", cfg["rr"])
    if not a.only:
        with open(os.path.join(data_dir, "macro.txt"), "w") as f:
            f.write(f"// dg-extract.py が {a.kit} の XML（power）から作った強さの層\n" + "\n".join(macro) + "\n")
    else:  # 一部だけ作り直すときは、既存の macro.txt に足す
        with open(os.path.join(data_dir, "macro.txt"), "a") as f:
            f.write("\n".join(macro) + "\n")

    keep_base = ["AmbLeft", "AmbRight", "OHLeft", "OHRight", "OHCenter"]

    def work(job):
        inst, cfg, smp = job
        d = os.path.join(a.samples, inst)
        os.makedirs(d, exist_ok=True)
        mics = keep_base + cfg["close"]
        names = {m: kit["rename"].get(m, m) for m in mics}
        if all(os.path.exists(os.path.join(d, f"{smp['idx']}-{inst}-{names[m]}.flac")) for m in mics):
            return
        file = smp["files"][mics[0]][0]
        entry = cd[kit["prefix"] + inst + "/" + file]
        # まず頭 64KB で形式を調べ、必要なバイト数を決める
        fmt, _ = parse_wav(head_of(kit["url"], entry, 65536))
        tag, ch, sr, bits = fmt
        need = 4096 + int(cfg["sec"] * sr) * ch * bits // 8
        fmt, raw = parse_wav(head_of(kit["url"], entry, need))
        for m in mics:
            if m not in smp["files"]:
                continue
            write_flac(os.path.join(d, f"{smp['idx']}-{inst}-{names[m]}.flac"), raw, fmt, smp["files"][m][1] - 1)
        print(f"  {inst} {smp['idx']} ({len(raw) / 1e6:.1f}MB) 通信の合計 {fetched[0] / 1e6:.0f}MB", flush=True)

    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(work, jobs))
    print("おわり。通信の合計:", f"{fetched[0] / 1e6:.0f}MB")


if __name__ == "__main__":
    main()
