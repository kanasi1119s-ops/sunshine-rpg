"""「ハニー・サワー」の試作MV（2026-11-08 人間「ハニーサワーのMVこの動画で作れるかな？」→「とりあえず作ってみて」）。
人間が作った10秒の動画（Gemini）だけで、曲（約3分32秒）に合わせてつなぐ。
  python3 tools/mv/honeysour_mv.py <元の動画.mp4> <曲.mp3> <出力.mp4>
元の動画の場面（秒）:
  A びん（0〜0.96）／B 窓辺と映る分身（1.0〜3.5。分身が歌い返すのは 2.0〜）／C ステージ全身（3.55〜4.95）
  D レモンのアップ（5.0〜6.15）／E ステージ全身2（6.25〜7.2）／F 台所のはちみつ紅茶（7.35〜8.3）／G 夕焼けのはちみつの塔（8.35〜10.0）
つなぎ方:
  ・切りかえは、曲の小節・拍の頭（122 BPM）にそろえる
  ・長くのばす所は、スロー（前のコマと次のコマを混ぜてなめらかに）＋行って戻る（ブーメラン）で、止まって見えないようにする
  ・同じ場面でも、寄り（ズーム）・ゆっくり横に動く・色味を変えて、くり返しに見えにくくする
  ・前奏は逆再生（びんに吸い込まれる）、8小節目はテープが止まるように遅くして止める（曲の前奏と同じ）
  ・元の動画についていた音は使わず、曲の音にする
"""
import sys, os, subprocess, tempfile

SRC, AUD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ASS = sys.argv[4] if len(sys.argv) > 4 else None   # 歌詞の字幕（tools/mv/honeysour_lyrics.py で作る）
BPM = 122.0; BEAT = 60 / BPM; BAR = 4 * BEAT
W, H, FPS = 720, 1280, 24
SC = {"A": (0.0, 0.96), "B": (1.0, 3.5), "Bt": (1.0, 2.0), "Br": (2.0, 3.5), "C": (3.55, 4.95), "D": (5.0, 6.15),
      "E": (6.25, 7.2), "F": (7.35, 8.3), "G": (8.35, 10.0), "Gend": (9.2, 10.0)}
TMP = tempfile.mkdtemp(prefix="hsmv_")
segs = []   # (長さ秒, 場面, 速さ, 逆再生, 寄り, 横の動き(-1〜1), 左右反転, 色)


def add(dur, sc, speed=1.0, rev=False, zoom=1.0, pan=0.0, flip=False, col=None, freeze_end=False):
    # 左右反転は使わない（腕の「04」の数字が鏡文字になる。試作1で見つけた）
    segs.append(dict(dur=dur, sc=sc, speed=speed, rev=rev, zoom=zoom, pan=pan, flip=False, col=col, freeze=freeze_end))


def beats(n): return n * BEAT
def bars(n): return n * BAR


# ---------------- 前奏（8小節）----------------
# 2026-11-08 人間「ゆっくりしすぎてぼやけてみえる」: 前は、びんの1秒を8倍のスローにして、コマを混ぜてつないでいたので、ぼやけて見えた。
#   → 4小節で、ほかの場面が1小節ずつ逆再生で巻きもどり、最後にびんへ吸い込まれる（どれも 0.8〜1倍。ぼかしもやめた）
for sc, z in (("G", 1.0), ("C", 1.05), ("Bt", 1.1), ("A", 1.0)):
    add(bars(1), sc, speed=0.85 if sc != "A" else 0.6, rev=True, zoom=z, col="dream")
for k, (sc, z, f) in enumerate([("C", 1.0, False), ("D", 1.1, False), ("E", 1.0, True), ("D", 1.25, True), ("C", 1.2, False), ("E", 1.15, False)]):
    add(beats(2), sc, speed=1.0, zoom=z, flip=f)                           # ドロップ: 2拍ごとに切りかえ
add(beats(2), "C", speed=0.35, zoom=1.05, freeze_end=True, col="stop")    # テープストップ: 遅くなって止まる
add(beats(2), "D", speed=0.6, zoom=1.3)                                   # 声だけの「はにさわ」（にっこり）
# ---------------- Aメロ1（テト）8小節 ----------------
for k in range(4): add(bars(2), "Bt", speed=0.35, zoom=[1.0, 1.2, 1.1, 1.35][k], pan=[0, 0.4, -0.4, 0.2][k])
# ---------------- Bメロ1（男性ボイス＝ガラスの分身）8小節 ----------------
for k in range(4): add(bars(2), "Br", speed=0.45, zoom=[1.15, 1.35, 1.25, 1.5][k], pan=[0.6, 0.8, 0.5, 0.7][k], col="cool" if k % 2 else None)
# ---------------- サビ（ふたり）----------------
def chorus(flipbase=False):
    plan = [("C", 1.0, 0), ("E", 1.05, 0), ("D", 1.15, 0), ("C", 1.2, 0.3), ("E", 1.0, 0), ("G", 1.0, 0), ("D", 1.3, 0), ("C", 1.1, -0.3)]
    for k, (sc, z, p) in enumerate(plan):
        add(beats(2), sc, speed=0.8, zoom=z, pan=p, flip=(k % 2 == 1) ^ flipbase)
        add(beats(2), sc, speed=0.8, zoom=z * 1.12, pan=-p, flip=(k % 2 == 1) ^ flipbase)
def post():
    for k in range(8):
        if k % 2 == 0:
            for j in range(4): add(beats(1), "D", speed=1.0, zoom=[1.0, 1.15, 1.3, 1.15][j], flip=j % 2 == 1)   # 拍ごとに寄る（「はにはにはに」）
        else:
            add(beats(2), "C" if k % 4 == 1 else "E", speed=1.0, zoom=1.1)
            add(beats(2), "D", speed=0.7, zoom=1.4, pan=0.2)
chorus(); post()
# ---------------- Aメロ2（男性ボイス）・Bメロ2（テト）----------------
for k in range(4): add(bars(2), "Br", speed=0.4, zoom=[1.2, 1.4, 1.3, 1.5][k], pan=[0.7, 0.5, 0.8, 0.6][k], flip=True, col="cool")
for k in range(4): add(bars(2), "Bt", speed=0.4, zoom=[1.1, 1.25, 1.4, 1.6][k], pan=[-0.3, 0.3, 0, 0][k], flip=True)
chorus(True); post()
# ---------------- ダンスブレイク ----------------
for k in range(8):
    if k < 6:
        add(beats(2), "C" if k % 2 == 0 else "E", speed=1.15, zoom=1.0, flip=k % 4 >= 2)
        add(beats(2), "E" if k % 2 == 0 else "C", speed=1.15, zoom=1.2, flip=k % 4 < 2)
    else:
        for j in range(4): add(beats(1), ["C", "E", "D", "E"][j], speed=1.3, zoom=1.0 + 0.1 * j, flip=j % 2 == 1)
# ---------------- ブリッジ（懐かしい）----------------
for k in range(3): add(bars(2), "F", speed=0.3, zoom=[1.0, 1.2, 1.35][k], pan=[0, -0.3, 0.3][k], col="sepia")
add(bars(1), "F", speed=0.5, zoom=1.5, col="sepia"); add(bars(1), "G", speed=0.6, zoom=1.2)
# ---------------- 最後のサビ・最後のポストサビ ----------------
plan = [("G", 1.0), ("C", 1.0), ("G", 1.2), ("E", 1.1), ("D", 1.2), ("G", 1.0), ("C", 1.15), ("G", 1.3)]
for k, (sc, z) in enumerate(plan):
    add(beats(2), sc, speed=0.7, zoom=z, flip=k % 2 == 1); add(beats(2), sc, speed=0.7, zoom=z * 1.1, flip=k % 2 == 0)
post()
# ---------------- 後奏 ----------------
add(bars(3), "G", speed=0.45, zoom=1.0, pan=0)
add(None, "Gend", speed=0.5, zoom=1.15, freeze_end=True)                  # ウインクして止まる（曲の最後まで）

COL = {None: "", "dream": ",eq=brightness=0.04:saturation=1.2",
       "stop": ",eq=saturation=0.7", "cool": ",colorbalance=bs=0.12:rs=-0.06",
       "sepia": ",eq=saturation=0.55:brightness=0.02,colorbalance=rs=0.08:gs=0.03:bs=-0.08:rm=0.06:bm=-0.05"}


def dur_total():
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUD]))
    return d


T = dur_total(); used = sum(s["dur"] for s in segs if s["dur"])
for s in segs:
    if s["dur"] is None: s["dur"] = T - used
files = []
for i, s in enumerate(segs):
    a, b = SC[s["sc"]]; L = b - a
    # スローは 0.6 倍まで（それより遅いと、コマがとびとびに見えるか、混ぜるとぼやける）。足りない長さは行って戻る（ブーメラン）でうめる
    sp = max(0.6, s["speed"])
    z = s["zoom"]; cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
    px = f"({W}-{cw})/2*(1+{s['pan']}*(t/{s['dur']:.3f}*2-1)*0.9)" if s["pan"] else f"({W}-{cw})/2"
    base = f"trim={a}:{b},setpts=PTS-STARTPTS"
    slow = f",setpts=PTS/{sp},fps={FPS}" if abs(sp - 1) > 1e-3 else f",fps={FPS}"   # コマは混ぜない（ぼやけるため）
    one = L / sp
    fwd = base + slow
    # ブーメラン: 行って戻るをくり返して長さを満たす（止めて終わる所は、最後のコマで止める）
    reps = max(1, int(s["dur"] / one) + 1)
    if s["freeze"]:
        chain = f"[0:v]{fwd}{',reverse' if s['rev'] else ''},tpad=stop_mode=clone:stop_duration={max(0, s['dur'] - one) + 0.1:.3f}[c]"
    else:
        parts = []; ch_ = f"[0:v]{fwd},split=2[f0][r0];[r0]reverse[rv];"
        seq = []
        for k in range(reps):
            seq.append("f" if (k % 2 == 0) != s["rev"] else "r")
        nf = seq.count("f"); nr = seq.count("r")
        ch_ += f"[f0]split={max(1, nf)}" + "".join(f"[f{k}x]" for k in range(max(1, nf))) + ";"
        ch_ += f"[rv]split={max(1, nr)}" + "".join(f"[r{k}x]" for k in range(max(1, nr))) + ";"
        fi = ri = 0; labels = []
        for q in seq:
            if q == "f": labels.append(f"[f{fi}x]"); fi += 1
            else: labels.append(f"[r{ri}x]"); ri += 1
        unused = [f"[f{k}x]" for k in range(fi, max(1, nf))] + [f"[r{k}x]" for k in range(ri, max(1, nr))]
        for u in unused: ch_ += f"{u}nullsink;"
        ch_ += "".join(labels) + f"concat=n={len(labels)}:v=1:a=0[c]"
        chain = ch_
    vf = (chain + f";[c]scale={W}:{H},crop={cw}:{ch}:'{px}':'({H}-{ch})/2',scale={W}:{H}:flags=lanczos"
          + ("," + "hflip" if s["flip"] else "") + COL[s["col"]] + f",trim=duration={s['dur']:.4f},setpts=PTS-STARTPTS,format=yuv420p[v]")
    out = os.path.join(TMP, f"s{i:03d}.mp4"); files.append(out)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", vf, "-map", "[v]", "-r", str(FPS),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], capture_output=True, text=True)
    if r.returncode: print(i, s, r.stderr[-800:]); sys.exit(1)
lst = os.path.join(TMP, "list.txt")
open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", AUD, "-map", "0:v", "-map", "1:a"]
               + (["-vf", f"subtitles={ASS}"] if ASS else []) + [
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac", "-b:a", "256k", "-shortest",
                "-movflags", "+faststart", OUT], check=True)
print(f"できた: {OUT}（{len(segs)} カット・{T:.1f}秒）")
