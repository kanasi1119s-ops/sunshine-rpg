#!/usr/bin/env python3
"""Naked Drums（Wilkinson Audio。SFZ 化 kinwie。CC BY 4.0）と Frankensnare（Karoryfer。CC0）から、
必要な打音と強さの層だけを取り出し、build-drums.mjs が読める形（sfzinstruments 版 Muldjord Kit と同じ並び）に直す前処理。

使い方（Windows でも動く。git と ffmpeg が必要）:
  git clone --filter=blob:none --no-checkout https://github.com/sfzinstruments/WilkinsonAudio.NakedDrums <naked の置き場>
  git clone --filter=blob:none --no-checkout https://github.com/sfzinstruments/karoryfer.frankensnare <frankensnare の置き場>
  python3 -I tools/soundfont/naked-extract.py --naked <naked の置き場> --fs <frankensnare の置き場> --samples <出力: 録音の置き場> [--rr 2]

- 「--filter=blob:none」で clone すると、録音（全部で数GB）は落とさない。このスクリプトが、使う打音のファイルだけを git checkout で取り寄せる。
- 出力:
  - <samples>/<楽器>/<番号>-<楽器>-<マイク>.flac（24bit・モノラル。OH・部屋のステレオは OHL/OHR・AmbL/AmbR に分ける）
  - assets-src/soundfont/extra/src/naked/Data/macro.txt（強さの層の範囲）・region/<楽器>.txt（<region> 行）・trim.json（元の SFZ の音量の補正 dB）
  - assets-src/soundfont/extra/src/naked/extract-list.txt（取り出した元のファイルの一覧）
元の録音（取り出した FLAC）はリポジトリに入れない。設定（Data/）だけを assets-src に置く。
"""
import argparse, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "assets-src" / "soundfont" / "extra" / "src" / "naked"
ND = Path("Wilkinson Audio") / "Naked Drums"

# Naked Drums の楽器: key＝元の keymap.txt のキーの名前、vol＝group_volume の名前（同じキーに複数あるとき）、
# mics＝{ここでのマイク名: 元のグループのファイル}（OH・CR は部屋／上のマイク）、sec＝取り出す長さ（秒）
OHCR = lambda p: {"OH": f"{p}_oh", "CR": f"{p}_cr"}
NAKED = {
    "Kick":        {"key": "KEY_KICK", "mics": {"KickIn": "kick_in", "KickSub": "kick_sub", **OHCR("kick")}, "sec": 1.2},
    "Snare":       {"key": "KEY_SNR1", "mics": {"SnareTop1": "snare_top1", "SnareTop2": "snare_top2", "SnareBot": "snare_bot", **OHCR("snare")}, "sec": 1.3},
    "Snare2":      {"key": "KEY_SNR2", "mics": {"SnareTop1": "snare_top1", "SnareTop2": "snare_top2", "SnareBot": "snare_bot", **OHCR("snare")}, "sec": 1.3},
    "SideStick":   {"key": "KEY_SIDE", "mics": {"SnareTop1": "snare_top1", "SnareTop2": "snare_top2", "SnareBot": "snare_bot", **OHCR("snare")}, "sec": 0.6},
    "HihatClosed": {"key": "KEY_HH_CLS", "mics": {"Hats": "hats_di", **OHCR("hats")}, "sec": 0.8},
    "HihatTight":  {"key": "KEY_HH_TGH", "mics": {"Hats": "hats_di", **OHCR("hats")}, "sec": 0.6},
    "HihatPedal":  {"key": "KEY_HH_PDL", "mics": {"Hats": "hats_di", **OHCR("hats")}, "sec": 0.6},
    "HihatHalf":   {"key": "KEY_HH_HLF", "mics": {"Hats": "hats_di", **OHCR("hats")}, "sec": 1.8},
    "HihatOpen":   {"key": "KEY_HH_OPN", "mics": {"Hats": "hats_di", **OHCR("hats")}, "sec": 3.2},
    **{f"Tom{i}": {"key": f"KEY_TOM{i}", "mics": {"Tom": f"tom{i}_di", **OHCR(f"tom{i}")}, "sec": 2.2} for i in range(1, 6)},
    "Ride":        {"key": "KEY_RD_BOW", "mics": {"Ride": "ride_di", **OHCR("ride")}, "sec": 4.0},
    "RideBell":    {"key": "KEY_RD_BEL", "mics": {"Ride": "ride_di", **OHCR("ride")}, "sec": 4.0},
    "Crash1":      {"key": "KEY_CRS1_EDG", "vol": "TRIM_CRS1_EDG", "mics": OHCR("crash1"), "sec": 5.0},
    "Crash2":      {"key": "KEY_CRS2_EDG", "vol": "TRIM_CRS2_EDG", "mics": OHCR("crash2"), "sec": 5.0},
    "Crash1Bell":  {"key": "KEY_CRS1_BEL", "mics": OHCR("crash1"), "sec": 4.0},
    "Crash1Choke": {"key": "KEY_CRS1_EDG", "vol": "TRIM_CRS1_CHK", "mics": OHCR("crash1"), "sec": 1.2},
    "Crash2Choke": {"key": "KEY_CRS2_EDG", "vol": "TRIM_CRS2_CHK", "mics": OHCR("crash2"), "sec": 1.2},
    "Splash1":     {"key": "KEY_SPL1", "mics": OHCR("splash1"), "sec": 4.0},
    "Splash2":     {"key": "KEY_SPL2", "mics": OHCR("splash2"), "sec": 4.0},
    "China1":      {"key": "KEY_CHN1", "mics": OHCR("china1"), "sec": 5.0},
    "China2":      {"key": "KEY_CHN2", "mics": OHCR("china2"), "sec": 5.0},
}
# Frankensnare のスネア: set＝Samples/ の下の組、layers＝使う強さの層（1始まり。元の層の番号）
FS = {
    "FsAlu":    {"set": "14a_basic", "layers": [2, 4, 6, 8, 10, 11], "sec": 1.3},   # 14x8 アルミ・センター
    "FsAluRim": {"set": "14a_rims", "layers": [1, 2, 3], "sec": 1.3},              # 14x8 アルミ・リムショット
    "FsMaple":  {"set": "14p_basic", "layers": [2, 4, 6, 8, 10, 11], "sec": 1.3},  # 14x6.5 メイプル・センター
}
FS_MICS = {"FsTop": "top", "FsBtm": "btm", "OH": "oh"}
RR_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def defines(text):
    """#define $NAME 値 を辞書に（1行に2つあることもある）"""
    return {m[0]: m[1] for m in re.findall(r"#define \$(\w+)\s+(\S+)", text)}


def git_checkout(repo, paths):
    for i in range(0, len(paths), 80):
        subprocess.run(["git", "-C", str(repo), "checkout", "HEAD", "--", *[p.as_posix() for p in paths[i:i + 80]]], check=True)


def channels(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=channels", "-of", "csv=p=0", str(f)], capture_output=True, text=True, check=True)
    return int(out.stdout.strip().splitlines()[0])


def cut(src, dst, sec, ch=None):
    """src の頭から sec 秒を 24bit モノラル FLAC に（ch＝ステレオのどちらか。None はモノラルのまま）"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    af = ["-af", f"pan=mono|c0=c{ch}"] if ch is not None else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", str(sec), *af, "-ac", "1", "-c:a", "flac", "-sample_fmt", "s32", "-bits_per_raw_sample", "24", str(dst)], check=True)


def put(src, outdir, inst, idx, mic, sec):
    """マイクの録音を書き出す。OH・CR（部屋）はステレオを左右に分ける（モノラルなら左右に同じものを置く）"""
    name = {"OH": ("OHL", "OHR"), "CR": ("AmbL", "AmbR")}.get(mic)
    if name is None:
        cut(src, outdir / inst / f"{idx}-{inst}-{mic}.flac", sec)
        return
    n = channels(src)
    for c, nm in enumerate(name):
        cut(src, outdir / inst / f"{idx}-{inst}-{nm}.flac", sec, c if n == 2 else None)


def naked_jobs(repo, rr):
    data = repo / ND / "Data"
    macro = defines((data / "macro.txt").read_text())
    jobs, regions, trims = [], {}, {}
    for inst, cfg in NAKED.items():
        layers_out = None
        for mic, gfile in cfg["mics"].items():
            text = (data / "group" / f"{gfile}.txt").read_text()
            local = defines(text)
            master = re.search(r"master_volume=\$(\w+)", text)
            master_db = float(macro.get(master[1], 0)) if master else 0.0
            block = None
            for b in text.split("<group>")[1:]:
                if f"key=${cfg['key']}\n" in b + "\n" and (not cfg.get("vol") or f"group_volume=${cfg['vol']}" in b):
                    block = b
                    break
            if block is None:
                raise SystemExit(f"見つからない: {inst} {mic} {cfg['key']}")
            gv = re.search(r"group_volume=\$(\w+)", block)
            trims.setdefault(inst, {})[mic] = master_db + (float(local.get(gv[1], macro.get(gv[1], 0))) if gv else 0.0)
            code = re.search(r'file/(\w+)\.txt', block)[1]
            vtype = int(re.search(r'region/v(\d)\.txt', block)[1])
            f = defines((data / "file" / f"{code}.txt").read_text())
            layers = []
            for layer in range(1, vtype + 1):
                for r in range(1, rr + 1):
                    n = (r - 1) * vtype + layer
                    sample = f"{f['MIC']}_{f['ART']}_{f[f'VEL{layer}']}_{RR_WORDS[r - 1]}-{f[f'CODE_{n:02d}']}.flac"
                    layers.append((layer, r, sample))
            lo_hi = [(int(macro[f"V{vtype}{l}L"]), int(macro[f"V{vtype}{l}H"])) for l in range(1, vtype + 1)]
            if layers_out is None:
                layers_out = (vtype, lo_hi)
                regions[inst] = layers_out
            for layer, r, sample in layers:
                idx = layer * 10 + r
                jobs.append((repo / ND / "Samples" / sample, inst, idx, mic, cfg["sec"]))
    return jobs, regions, trims


def fs_jobs(repo, rr):
    jobs, regions = [], {}
    for inst, cfg in FS.items():
        groups = None
        for mic, sub in FS_MICS.items():
            text = (repo / "Programs" / "mappings" / f"{cfg['set']}_{sub}.sfz").read_text()
            gs = []
            for g in text.split("<group>")[1:]:
                lo = int((re.search(r"lovel=(\d+)", g) or [0, 1])[1])
                hi = int((re.search(r"hivel=(\d+)", g) or [0, 127])[1])
                samples = re.findall(r"sample=\.\./(\S+)", g)
                gs.append((lo, hi, samples))
            groups = gs
            for j, layer in enumerate(cfg["layers"]):
                for r in range(1, rr + 1):
                    jobs.append((repo / gs[layer - 1][2][r - 1], inst, layer * 10 + r, mic, cfg["sec"]))
        # 選んだ層の強さの範囲: 選ばなかった層は、その上の選んだ層がうけもつ
        ranges, prev = [], 0
        for layer in cfg["layers"]:
            hi = groups[layer - 1][1] if layer != cfg["layers"][-1] else 127
            ranges.append((prev + 1, hi))
            prev = hi
        regions[inst] = (len(cfg["layers"]), ranges, cfg["layers"])
    return jobs, regions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--naked", required=True)
    ap.add_argument("--fs", required=True)
    ap.add_argument("--samples", required=True)
    ap.add_argument("--rr", type=int, default=2)
    a = ap.parse_args()
    naked, fs, out = Path(a.naked), Path(a.fs), Path(a.samples)
    nj, nreg, trims = naked_jobs(naked, a.rr)
    fj, freg = fs_jobs(fs, a.rr)
    for repo, jobs in ((naked, nj), (fs, fj)):
        need = sorted({j[0].relative_to(repo) for j in jobs if not j[0].exists()})
        if need:
            print("取り寄せ:", repo, len(need), "ファイル")
            git_checkout(repo, need)
    for src, inst, idx, mic, sec in nj + fj:
        put(src, out, inst, idx, mic, sec)
    # 設定（Data/）を書く
    (DATA / "Data" / "region").mkdir(parents=True, exist_ok=True)
    macro_lines, base = [], 100
    for inst, (vtype, lo_hi) in nreg.items():
        lines = [f"#define $instr {inst}", "group_label=$instr", ""]
        for l, (lo, hi) in enumerate(lo_hi, 1):
            v = base + l
            macro_lines.append(f"#define $v{v}l {lo}\n#define $v{v}h {hi}")
            for r in range(1, a.rr + 1):
                lines.append(f"<region> lovel=$v{v}l hivel=$v{v}h sample=$instr/{l * 10 + r}-$instr-$mic.$ext seq_position={r}")
        (DATA / "Data" / "region" / f"{inst}.txt").write_text("\n".join(lines) + "\n")
        base += 10
    for inst, (n, ranges, layers) in freg.items():
        lines = [f"#define $instr {inst}", "group_label=$instr", ""]
        for (lo, hi), layer in zip(ranges, layers):
            v = base + layer
            macro_lines.append(f"#define $v{v}l {lo}\n#define $v{v}h {hi}")
            for r in range(1, a.rr + 1):
                lines.append(f"<region> lovel=$v{v}l hivel=$v{v}h sample=$instr/{layer * 10 + r}-$instr-$mic.$ext seq_position={r}")
        (DATA / "Data" / "region" / f"{inst}.txt").write_text("\n".join(lines) + "\n")
        base += 20
    (DATA / "Data" / "macro.txt").write_text("// 強さの層の範囲（naked-extract.py が書く）\n" + "\n".join(macro_lines) + "\n")
    (DATA / "Data" / "trim.json").write_text(json.dumps(trims, ensure_ascii=False, indent=1) + "\n")
    listing = [f"{src.relative_to(naked if src.is_relative_to(naked) else fs).as_posix()}\t{inst}\t{idx}\t{mic}\t{sec}s" for src, inst, idx, mic, sec in nj + fj]
    (DATA / "extract-list.txt").write_text("# 元のファイル\t楽器\t番号\tマイク\t長さ（naked-extract.py が書く）\n" + "\n".join(listing) + "\n")
    print("楽器:", len(nreg) + len(freg), "打音のファイル:", len(nj) + len(fj))


if __name__ == "__main__":
    main()
