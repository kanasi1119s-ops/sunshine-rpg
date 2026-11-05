# 断片化MP4の長さを直す: mfra→free、mvhd/tkhd/mdhd に全体の長さを書く（映像と音には手をつけない）
import struct, os, sys
f = sys.argv[1]; vdur = float(sys.argv[2]); adur = float(sys.argv[3])
fd = open(f, "r+b"); L = os.path.getsize(f); pos = 0; n = 0
while pos < L:
    fd.seek(pos); h = fd.read(16); sz, t = struct.unpack(">I4s", h[:8])
    if sz == 1: sz = struct.unpack(">Q", h[8:16])[0]
    if t == b"mfra": fd.seek(pos + 4); fd.write(b"free"); n += 1
    pos += sz
fd.seek(0); head = bytearray(fd.read(4000))
def boxes(b, s, e):
    i = s
    while i < e:
        sz, t = struct.unpack(">I4s", b[i:i+8]); yield t.decode(), i, sz; i += sz
mi = head.find(b"moov") - 4; msz = struct.unpack(">I", head[mi:mi+4])[0]
mvts = None; writes = []
for t, i, sz in boxes(head, mi + 8, mi + msz):
    if t == "mvhd":
        assert head[i+8] == 0; mvts = struct.unpack(">I", head[i+20:i+24])[0]
        writes.append((i + 24, round(max(vdur, adur) * mvts)))
for t, i, sz in boxes(head, mi + 8, mi + msz):
    if t != "trak": continue
    kind = None; tk = None; md = None
    for t2, j, s2 in boxes(head, i + 8, i + sz):
        if t2 == "tkhd": assert head[j+8] == 0; tk = j
        if t2 == "mdia":
            for t3, k, s3 in boxes(head, j + 8, j + s2):
                if t3 == "mdhd": assert head[k+8] == 0; md = k
                if t3 == "hdlr": kind = head[k+16:k+20].decode()
    d = vdur if kind == "vide" else adur
    mts = struct.unpack(">I", head[md+20:md+24])[0]
    writes.append((tk + 28, round(d * mvts))); writes.append((md + 24, round(d * mts)))
    print(kind, "timescale", mts)
for off, v in writes: fd.seek(off); fd.write(struct.pack(">I", v))
fd.close(); print("mfra→free", n, "書きこみ", writes)
