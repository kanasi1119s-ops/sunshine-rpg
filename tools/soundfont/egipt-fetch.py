#!/usr/bin/env python3
"""EG-IPT（Zenodo、CC BY 4.0。電気ギターの奏法の録音 23.8GB）から、名前が合うファイルだけを HTTP の Range で取り出す。
全部は落とさない。zip の目次だけを読み（dg-extract.py と同じしくみ）、選んだファイルを1つずつ取る。

使い方:
  python3 -I tools/soundfont/egipt-fetch.py <出力フォルダ> <正規表現> [<正規表現> ...] [--max 40] [--list]
例:
  python3 -I tools/soundfont/egipt-fetch.py /tmp/egipt 'HB-bridge/DI/scratch/' 'HB-bridge/DI/palmstrike/'
  python3 -I tools/soundfont/egipt-fetch.py /tmp/egipt 'HB-bridge/(DI|dyn|cond|rib)/ordinario/HB-bridge_ordinario_1[3-8]-(04|12)_'
取り出したファイルは <出力フォルダ>/<元のパスの / を __ にした名前>。元の録音はリポジトリに入れない。
"""
import importlib.util, os, re, sys
from concurrent.futures import ThreadPoolExecutor

URL = "https://zenodo.org/records/15205644/files/EG-IPT.zip?download=1"
spec = importlib.util.spec_from_file_location("dgx", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dg-extract.py"))
dgx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dgx)


def main():
    args = sys.argv[1:]
    mx = int(args[args.index("--max") + 1]) if "--max" in args else 400
    listing = "--list" in args
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--max")]
    out, pats = pos[0], [re.compile(p) for p in pos[1:]]
    os.makedirs(out, exist_ok=True)
    cd = dgx.central_directory(URL)
    names = [n for n in cd if n.lower().endswith(".wav") and "__MACOSX" not in n and any(p.search(n) for p in pats)][:mx]
    print("対象:", len(names), "ファイル", f"{sum(cd[n][2] for n in names) / 1e6:.0f}MB")
    if listing:
        for n in names:
            print(cd[n][2], n)
        return

    def get(n):
        dst = os.path.join(out, n.replace("/", "__"))
        if os.path.exists(dst):
            return
        data = dgx.head_of(URL, cd[n], cd[n][2])
        open(dst, "wb").write(data)

    with ThreadPoolExecutor(6) as ex:
        list(ex.map(get, names))
    print("おわり。通信:", f"{dgx.fetched[0] / 1e6:.0f}MB")


if __name__ == "__main__":
    main()
