"""第4版: 2048×1152（元の 512 ドットの 4 倍。ドットの形をくずさない）・毎秒30コマ。鯨は毎秒30画素＝1コマ1画素で進む（ちょうど割り切れるので、進み方にむらがない）。
背景のくり返しアニメに、鯨とクラゲを重ねて動かす（毎秒30コマ・1画素きざみで動かすので、かくかくしない）。
  鯨: 海より上の空を、右から左へゆったり泳いで画面の外へ出ていき、しばらくすると、ちがう高さでまた右から現れる。
  クラゲ: 水の中を、ゆっくりした大きな波（周期のちがう2つのゆれ）で自由にただよう。傘が閉じるとふわっと上がる（泳ぎのコマと合わせる）。
使い方: python3 compose.py <背景GIF> <出力.mp4> [秒数] [音（なければ無音）]   環境変数 CRF / BITRATE"""
import json, math, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
bgf, out = sys.argv[1], sys.argv[2]
dur = float(sys.argv[3]) if len(sys.argv) > 3 else 60
audio = sys.argv[4] if len(sys.argv) > 4 else None
I = json.load(open(D + "/sprites/info.json"))
SPF = 15   # 泳ぎのコマ（60コマで1周＝4秒）
WP = 240.0   # (2048+1155+20)/20＝約161秒で横切り、残りは画面の外（4分でひと回り）  # 鯨が1回横切る周期（秒）。約80秒で横切り、16秒は画面の外

def wave(terms):   # [(振幅, 周期, 位相)] → ffmpeg の式
    return "+".join(f"{A}*sin(2*PI*t/{T}+{p})" for A, T, p in terms)

ww, wh = I["whale"]["w"], I["whale"]["h"]
v = 20.0   # ゆったり（3コマで2画素。決まった並びでむらなく進む）
wx = f"2048+10-{v:.4f}*mod(t,{WP})"   # (2048+1266+20)/30＝約111秒で横切り、約9秒は画面の外
wy = "-40+" + wave([(30, 48, 0.0), (10, 16, 1.1)])   # 鯨の下が海にかからない高さ（体の上の尾の先は、ときどき画面の上に出る）   # 大きくなった鯨の下が海にかからない高さ
# クラゲ（2026-10-18、人間の指示「クラゲも向きを変えたりいろいろ試して」）: 進む向きに傘を向ける（横に動くほど体をかたむける。±35°まで）。
#   3匹で傘を動かす速さを変える（シアン 4秒・金 3.2秒・青 5秒）。傘が閉じるたび、傘の向いている方へ、ふわっと進む。
JP = {"jcyan": 0.0, "jgold": 2.2, "jblue": 4.1}
JR = {"jcyan": 15, "jgold": 18.75, "jblue": 12}          # 泳ぎのコマの速さ（60コマ）→ 1かき＝60/速さ 秒
JM = {  # 中心のx, xのゆれ, 上のy, yのゆれ, 向きのゆらぎ（ラジアン, 周期, 位相）
    # 周期はどれも 240 秒を割り切る値（240 秒ごとに全部の動きがちょうど元にもどる → 4分ぶんを作って、くり返してつなげられる）
    "jcyan": (1152, [(112, 60, 0.0), (48, 20, 1.3)], 960, [(45, 40, 0.5), (13, 12, 2.0)], (0.18, 24, 0.4)),
    "jgold": (1328, [(176, 80, 2.0), (48, 16, 0.2)], 989, [(58, 48, 1.7), (13, 15, 0.9)], (0.25, 20, 2.2)),
    "jblue": (1744, [(240, 120, 4.0), (64, 30, 2.5)], 957, [(51, 40, 3.1), (13, 10, 1.4)], (0.30, 30, 1.0)),
}
inputs = ["-framerate", "30", "-stream_loop", "-1", "-i", D + "/bgframes/bg_%03d.png",       # 背景 300コマ・30コマ/秒
          "-framerate", "30", "-stream_loop", "-1", "-i", D + "/sprites/whale_%03d.png"]   # 鯨は 180コマ・30コマ/秒
for k in JM: inputs += ["-framerate", str(JR[k]), "-stream_loop", "-1", "-i", D + f"/sprites/{k}_%02d.png"]
nin = 2 + 3
inputs += ["-loop", "1", "-i", D + "/islandmask.png", "-framerate", "30", "-stream_loop", "-1", "-i", D + "/smoke/sm_%03d.png"]
fc = "[0:v]scale=2048:1152:flags=neighbor,format=rgba,split[b0][bI];"
fc += f"[{nin}:v]format=gray[im];[bI][im]alphamerge[isl];"                         # 島（家・木）だけを切り出した層
fc += f"[{nin + 1}:v]scale=2048:1152:flags=neighbor,format=rgba[smk];"
cur = "b0"
for i, k in enumerate(JM, start=2):
    cx, xs, cy, ys, (ta, tt, tph) = JM[k]
    w, h = I[k]["w"], I[k]["h"]; Dg = int(math.ceil(math.hypot(w, h))) + 2
    per = 60 / JR[k]
    vx = "+".join(f"{A * 2 * math.pi / T:.4f}*cos(2*PI*t/{T}+{p})" for A, T, p in xs)
    ang = f"(clip(0.9*atan(({vx})/19),-0.6,0.6)+{ta}*sin(2*PI*t/{tt}+{tph}))"
    bob = f"10*cos(2*PI*t/{per:.4f}+{JP[k]})"
    jx = f"{cx - Dg / 2:.1f}+" + wave(xs) + f"-{bob}*sin({ang})"
    jy = f"{cy + h / 2 - Dg / 2:.1f}+" + wave(ys) + f"+{bob}*cos({ang})"
    fc += (f"[{i}:v]fps=30,format=rgba,rotate=a='{ang}':c=none:ow={Dg}:oh={Dg}[s{i}];"
           f"[{cur}][s{i}]overlay=x='{jx}':y='{jy}':eval=frame:format=auto[b{i}];")
    cur = f"b{i}"
fc += (f"[1:v]fps=30,format=rgba[sw];[{cur}][sw]overlay=x='{wx}':y='{wy}':eval=frame:format=auto[w1];"
       f"[w1][isl]overlay=0:0:format=auto[w2];[w2][smk]overlay=0:0:format=auto,format=yuv420p[v]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
if audio: cmd += ["-i", audio]
cmd += ["-filter_complex", fc, "-map", "[v]"]
if audio: cmd += ["-map", f"{len(JM) + 4}:a", "-c:a", "aac", "-b:a", "192k"]
cmd += ["-t", f"{dur:.2f}", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-crf", os.environ.get("CRF", "18"), "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("ok", out, os.path.getsize(out) // 1000000, "MB")
