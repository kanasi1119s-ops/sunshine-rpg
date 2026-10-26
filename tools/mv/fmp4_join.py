#!/usr/bin/env python3
"""断片化した MP4（frag_keyframe+empty_moov で作ったもの）を、1曲ずつ書き足して1本にする。
パソコンの連結フォルダは書きこみが遅く、ffmpeg で 1.9GB を一度に作ると時間切れになるため、曲ごとに少しずつ足せるこの形にした（2026-10-26）。
曲 N の断片の時刻（tfdt）に、それまでの曲の長さ（映像と音の長いほう）を足し、moof の番号を通し番号にして、初めの頭（ftyp+moov）だけを残す。
使い方:
  python3 fmp4_join.py start <出力> <曲1.mp4>          … 出力を新しく作る（頭＋曲1）。状態は <出力>.state.json
  python3 fmp4_join.py add <出力> <曲N.mp4>            … 曲Nの断片を、時刻をずらして書き足す
"""
import sys, struct, json, os
def boxes(b, s=0, e=None):
    e = len(b) if e is None else e; i = s
    while i < e:
        sz, t = struct.unpack(">I4s", b[i:i + 8]); hdr = 8
        if sz == 1: sz = struct.unpack(">Q", b[i + 8:i + 16])[0]; hdr = 16
        yield t.decode("latin1"), i, sz, hdr; i += sz
def child(b, i, sz, hdr, name):
    for t, j, s2, h2 in boxes(b, i + hdr, i + sz):
        if t == name: yield j, s2, h2
def info(b):
    """moov から、トラックごとの時間の単位（timescale）と、trex の既定の長さ"""
    ts, dd = {}, {}
    for t, i, sz, h in boxes(b):
        if t != "moov": continue
        for j, s2, h2 in child(b, i, sz, h, "trak"):
            tid = None
            for k, s3, h3 in child(b, j, s2, h2, "tkhd"):
                v = b[k + h3]; tid = struct.unpack(">I", b[k + h3 + (20 if v == 1 else 12):][:4])[0]
            for k, s3, h3 in child(b, j, s2, h2, "mdia"):
                for m, s4, h4 in child(b, k, s3, h3, "mdhd"):
                    v = b[m + h4]; ts[tid] = struct.unpack(">I", b[m + h4 + (20 if v == 1 else 12):][:4])[0]
        for j, s2, h2 in child(b, i, sz, h, "mvex"):
            for k, s3, h3 in child(b, j, s2, h2, "trex"):
                tid, _, dur = struct.unpack(">III", b[k + h3 + 4:k + h3 + 16]); dd[tid] = dur
    return ts, dd
def frags(b, ts, dd, off_s, seq0):
    """断片を書きかえる（tfdt += off、mfhd の番号を通しに）。返り値: 書きかえた断片・曲の長さ（秒）・次の番号"""
    out = bytearray(); end = {}; seq = seq0; first = None
    for t, i, sz, h in boxes(b):
        if t == "moof" and first is None: first = i
        if first is None: continue
        if t == "mfra": continue   # 曲ごとの目次は入れない（入れると、再生ソフトが1曲目の終わりで動画が終わると読んでしまう。2026-10-27）
        chunk = bytearray(b[i:i + sz])
        if t == "moof":
            for t2, j, s2, h2 in boxes(chunk, h, sz):
                if t2 == "mfhd": struct.pack_into(">I", chunk, j + h2 + 4, seq); seq += 1
                if t2 == "traf":
                    tid = None; ddur = None; base = None
                    for t3, k, s3, h3 in boxes(chunk, j + h2, j + s2):
                        if t3 == "tfhd":
                            fl = int.from_bytes(chunk[k + h3 + 1:k + h3 + 4], "big"); tid = struct.unpack(">I", chunk[k + h3 + 4:k + h3 + 8])[0]
                            p = k + h3 + 8 + (8 if fl & 1 else 0) + (4 if fl & 2 else 0)
                            ddur = struct.unpack(">I", chunk[p:p + 4])[0] if fl & 8 else dd.get(tid, 0)
                        if t3 == "tfdt":
                            v = chunk[k + h3]
                            add = int(round(off_s * ts[tid]))
                            if v == 1:
                                base = struct.unpack(">Q", chunk[k + h3 + 4:k + h3 + 12])[0]; struct.pack_into(">Q", chunk, k + h3 + 4, base + add)
                            else:
                                base = struct.unpack(">I", chunk[k + h3 + 4:k + h3 + 8])[0]
                                if base + add >= 2 ** 32: raise SystemExit("tfdt が 32bit をこえる（version 1 にしてください）")
                                struct.pack_into(">I", chunk, k + h3 + 4, base + add)
                        if t3 == "trun":
                            fl = int.from_bytes(chunk[k + h3 + 1:k + h3 + 4], "big"); n = struct.unpack(">I", chunk[k + h3 + 4:k + h3 + 8])[0]
                            p = k + h3 + 8 + (4 if fl & 1 else 0) + (4 if fl & 4 else 0)
                            per = (4 if fl & 0x100 else 0) + (4 if fl & 0x200 else 0) + (4 if fl & 0x400 else 0) + (4 if fl & 0x800 else 0)
                            tot = 0
                            for q in range(n):
                                tot += struct.unpack(">I", chunk[p + q * per:p + q * per + 4])[0] if fl & 0x100 else ddur
                            end[tid] = max(end.get(tid, 0), (base + tot) / ts[tid])
        out += chunk
    return bytes(out), max(end.values()), seq
cmd, OUT, SRC = sys.argv[1:4]
b = open(SRC, "rb").read(); ts, dd = info(b)
st_path = OUT + ".state.json"
if cmd == "start":
    head = b[:next(i for t, i, sz, h in boxes(b) if t == "moof")]
    fr, dur, seq = frags(b, ts, dd, 0.0, 1)
    open(OUT, "wb").write(head + fr); json.dump({"off": dur, "seq": seq}, open(st_path, "w"))
else:
    st = json.load(open(st_path))
    fr, dur, seq = frags(b, ts, dd, st["off"], st["seq"])
    with open(OUT, "ab") as f: f.write(fr)
    json.dump({"off": st["off"] + dur, "seq": seq}, open(st_path, "w"))
print("ok", OUT, "ここまでの長さ", round(json.load(open(st_path))["off"], 3))
