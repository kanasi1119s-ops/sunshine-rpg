# SF2/SF3 のプリセット番号（GM の楽器番号）を書きかえた写しを作る。
# 2026-10-20 ラウドロック: 歪みギター（GM 30）を、歪ませる前の録音（DI）で鳴らすため。
# 使い方: python3 represet.py <元.sf3> <出力.sf3> <新しい番号> [新しい名前]
import struct, sys
src, dst, num = sys.argv[1], sys.argv[2], int(sys.argv[3])
name = sys.argv[4] if len(sys.argv) > 4 else None
d = bytearray(open(src, "rb").read())
i = d.find(b"phdr"); n = struct.unpack("<I", d[i + 4:i + 8])[0]; base = i + 8
for j in range(0, n - 38, 38):   # 最後の EOP は書きかえない
    o = base + j
    struct.pack_into("<H", d, o + 20, num)
    if name:
        d[o:o + 20] = name.encode("ascii")[:19].ljust(20, b"\0")
open(dst, "wb").write(d)
print(dst, "preset", num)
