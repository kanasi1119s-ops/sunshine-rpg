"""ダンス 1000コマ（24コマ/秒・約41.7秒）。テンポ120（1拍＝12コマ）。
  0〜95    その場でリズム（ひざでのる・ゆれる）
  96〜287  左右のステップ（ステップ・タッチ）
  288〜479 手拍子（2拍に1回 → 毎拍）
  480〜527 くるっと回る（2拍で1回転 × 2）
  528〜719 ステップしながら手拍子（タッチで手をたたく）
  720〜767 くるっと回る（2回）
  768〜959 速い手拍子（半拍ごと）と小さなステップ
  960〜999 最後に1回転して、正面で手を合わせて止まる"""
import sys, math; sys.path.insert(0, '/tmp/px5')
import rig
B = 12
def ease(u): return 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, u)))
def bounce(t, depth=2):            # 拍の頭で しずむ（ひざでのる）
    u = (t % B) / B; return round(depth * math.sin(math.pi * u) ** 2) if u < 0.5 else round(depth * (1 - ease((u - 0.5) * 2)) * 0)
def pose(t):
    p = dict(bx=0, by=0, hy=0, ua=(0, 0), fa=(0, 0), liftL=0, liftR=0, legdx=(0, 0), spin=None, clap=None)
    beat = t / B; ib = int(beat); u = beat - ib
    def bob(d=2): return round(d * math.sin(math.pi * u))         # 拍ごとに しずんで もどる
    def step(t0, span=2, dist=5):
        """ステップ・タッチ: 2拍で 右へ dist（右足から）→ 次の2拍で左へ。戻り値 bx, liftL, liftR"""
        k = (t - t0) / B; cyc = int(k // span); v = (k % span) / span; dirn = 1 if cyc % 2 == 0 else -1
        start = 0 if dirn == 1 else dist
        if v < 0.5:                                               # 1拍め: 進む方の足を上げて運ぶ
            w = ease(v * 2); bx = start + dirn * dist * w * 0.7
            lift = round(4 * math.sin(math.pi * v * 2))
            return round(bx), (lift if dirn == -1 else 0), (lift if dirn == 1 else 0)
        w = ease((v - 0.5) * 2); bx = start + dirn * dist * (0.7 + 0.3 * w)       # 2拍め: もう一方の足を寄せる（タッチ）
        lift = round(3 * math.sin(math.pi * (v - 0.5) * 2))
        return round(bx), (lift if dirn == 1 else 0), (lift if dirn == -1 else 0)
    if t < 96:                                                    # その場でリズム
        p["by"] = bob(2); p["hy"] = -1 if 0.15 < u < 0.4 else 0
        p["bx"] = round(1.5 * math.sin(2 * math.pi * beat / 4))
    elif t < 288:                                                 # 左右のステップ
        p["bx"], p["liftL"], p["liftR"] = step(96); p["by"] = bob(1); p["hy"] = -1 if 0.15 < u < 0.4 else 0
        p["bx"] -= 2
    elif t < 480:                                                 # 手拍子: はじめの8拍は2拍に1回、あとは毎拍
        every = 2 if t < 384 else 1
        k = (t - 288) / B; v = (k % every) / every
        p["clap"] = 0 if v < 0.12 else min(1, ease((v - 0.12) / 0.35)) if v < 0.5 else 1 - ease((v - 0.5) / 0.5) if every == 1 else (1 if v < 0.75 else 1 - ease((v - 0.75) / 0.25))
        p["by"] = bob(2); p["hy"] = -1 if 0.15 < u < 0.4 else 0
    elif t < 528 or 720 <= t < 768:                               # くるっと回る（2拍で1回転）
        t0 = 480 if t < 528 else 720; k = (t - t0) / (2 * B)
        p["spin"] = 360 * ease(k - math.floor(k)); p["by"] = -round(2 * math.sin(math.pi * (k - math.floor(k))))
    elif t < 720:                                                 # ステップしながら手拍子（タッチの拍で手をたたく）
        p["bx"], p["liftL"], p["liftR"] = step(528); p["bx"] -= 2; p["by"] = bob(1)
        k = (t - 528) / B; v = (k % 2) / 2
        p["clap"] = 1 if v < 0.45 else (1 - ease((v - 0.45) / 0.1) if v < 0.55 else ease((v - 0.6) / 0.4) if v >= 0.6 else 0)
    elif t < 960:                                                 # 速い手拍子（半拍ごと）と、小さなゆれ
        k = (t - 768) / (B / 2); v = k - math.floor(k)
        p["clap"] = 0 if v < 0.15 else (ease((v - 0.15) / 0.35) if v < 0.5 else 1 - ease((v - 0.5) / 0.5))
        p["bx"] = round(3 * math.sin(2 * math.pi * beat / 4)); p["by"] = bob(1)
        p["liftL"] = 2 if (ib % 4 == 1 and u < 0.5) else 0; p["liftR"] = 2 if (ib % 4 == 3 and u < 0.5) else 0
    else:                                                         # 最後: 1回転して、正面で手を合わせて止まる
        k = (t - 960) / 24
        if k < 1: p["spin"] = 360 * ease(k); p["by"] = -round(2 * math.sin(math.pi * k))
        else: p["clap"] = 0; p["by"] = 1 if t < 990 else 0
    return p
FRAMES = [rig.grid(rig.render(pose(t))) for t in range(1000)]
if __name__ == "__main__":
    import json
    json.dump(FRAMES, open('/tmp/px5/frames.json', 'w'))
    sel = list(range(96, 144, 3)) + list(range(288, 312, 3)) + list(range(480, 504, 3))
    rig.png([FRAMES[i] for i in sel], '/tmp/px5/dance_pick.png', z=2, cols=16)
    print(len(FRAMES), "コマ", len(set(map(tuple, FRAMES))), "種類")
