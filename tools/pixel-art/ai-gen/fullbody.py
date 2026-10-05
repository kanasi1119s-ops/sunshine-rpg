"""敵の下絵が「全身が入っているか」を調べる・切れていたら描き足す（2026-10-04、人間の指示「全身が入るようにね」）。

最初に試した神・悪魔・キメラなどの下絵は、体が絵の端で切れていたり、形が崩れていた。そこで、
  1) check: 背景を切り抜き（rembg isnet-general-use）、体が絵の端に触れていないか（上下左右の余白）と、
     体がばらばらになっていないか（いちばん大きなかたまりの割合）を調べる。
  2) extend: 端で切れている下絵を、512の中に小さく置き直し、外側（切れた先）だけを inpainting で描き足す。
使い方（ふつうは monster_batch.py の draft / extend から呼ばれる）:
  python3 fullbody.py check 下絵.png...            → 下絵ごとに <下絵>.check.json と結果の1行
  python3 fullbody.py extend 下絵.png 出力.png "英語の説明"
メモリ7GBほどの環境では、画像生成（generate.py）と同時に動かさない（check も extend も、生成が終わってから）。
"""
import json
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

MARGIN = 0.02     # 体と絵の端のあいだに、最低これだけ（幅の2%＝512で約10ドット）の余白が要る
MAIN_PART = 0.85  # いちばん大きな体のかたまりが、体全体のこれ以上（小さな破片が散らばった下絵をはじく）


_SESSION = None


def body_mask(img):
    """rembg（isnet-general-use。sfcize.py と同じ）で切り抜いた体の形。小さな破片も残して数える"""
    global _SESSION
    from rembg import remove, new_session
    if _SESSION is None:
        _SESSION = new_session("isnet-general-use")
    a = np.asarray(remove(img.convert("RGB"), session=_SESSION))[:, :, 3] >= 128
    return ndimage.binary_opening(a, iterations=2)


def check(path):
    img = Image.open(path)
    m = body_mask(img)
    h, w = m.shape
    res = {"ok": False, "cut": [], "parts": 0.0, "fill": 0.0}
    if m.sum() < 0.01 * w * h:
        res["cut"] = ["体が見つからない"]
        json.dump(res, open(path + ".check.json", "w"), ensure_ascii=False)
        return res
    ys, xs = np.nonzero(m)
    mg = {"上": ys.min() / h, "下": (h - 1 - ys.max()) / h, "左": xs.min() / w, "右": (w - 1 - xs.max()) / w}
    lab, n = ndimage.label(m)
    sizes = np.bincount(lab.ravel())[1:]
    res["parts"] = round(float(sizes.max() / sizes.sum()), 3)
    res["fill"] = round(float(m.sum() / (w * h)), 3)
    res["margin"] = {k: round(float(v), 3) for k, v in mg.items()}
    res["cut"] = [k for k, v in mg.items() if v < MARGIN]
    # 額縁に入った絵・ポスターのように描かれたもの: 体の形が、ほぼ四角（または丸）でぎっしり詰まっている
    bh, bw = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    box_fill = float(m.sum() / (bh * bw))
    res["box_fill"] = round(box_fill, 3)
    # 四すみまで詰まっているか（四角い額縁の絵）。丸い体（苔玉・光の玉）は四すみが空くので額縁としない（2026-10-05）
    y0, x0 = ys.min(), xs.min(); c = max(2, int(min(bh, bw) * 0.12))
    corners = float(np.mean([m[y0:y0 + c, x0:x0 + c].mean(), m[y0:y0 + c, x0 + bw - c:x0 + bw].mean(),
                             m[y0 + bh - c:y0 + bh, x0:x0 + c].mean(), m[y0 + bh - c:y0 + bh, x0 + bw - c:x0 + bw].mean()]))
    res["corners"] = round(corners, 3)
    res["framed"] = bool(box_fill > 0.9) or bool(box_fill > 0.76 and abs(bh - bw) < 0.06 * max(bh, bw) and corners > 0.6)
    res["ok"] = bool(not res["cut"] and res["parts"] >= MAIN_PART and not res["framed"])
    json.dump(res, open(path + ".check.json", "w"), ensure_ascii=False)
    return res


def label(res):
    if res["ok"]:
        return "全身OK"
    msg = []
    if res["cut"]:
        msg.append("切れ:" + "".join(res["cut"]))
    if res.get("parts", 1) < MAIN_PART:
        msg.append("ばらばら")
    if res.get("framed"):
        msg.append("額縁・四角い絵")
    return " ".join(msg)


def pad_if_clear(src, dst, pad=0.08):
    """体が端に「近い」だけで、端そのものは白い背景のとき（はみ出していない）は、白い余白を足すだけで直す（AIを使わない）"""
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    edges = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    if (edges.min(axis=1) > 225).mean() < 0.97:
        return False                      # 端に体がかかっている → 描き足しが要る
    w, h = im.size; p = int(round(max(w, h) * pad))
    bg = tuple(int(v) for v in np.median(edges, axis=0))
    out = Image.new("RGB", (w + 2 * p, h + 2 * p), bg); out.paste(im, (p, p))
    out.resize((w, h), Image.LANCZOS).save(dst)
    return True


def extend(src, dst, desc, scale=0.68, seed=11):
    """切れた下絵を直す。端が白い背景なら余白を足すだけ。体が端にかかっていたら、小さく置き直して外側だけを描き足す（元の部分はそのまま）。"""
    if pad_if_clear(src, dst):
        print("白い余白を足しました（AIは使っていない）")
        return
    import torch
    from diffusers import StableDiffusionInpaintPipeline, LCMScheduler
    torch.set_num_threads(2)
    im = Image.open(src).convert("RGB").resize((512, 512), Image.LANCZOS)
    s = round(512 * scale)
    small = im.resize((s, s), Image.LANCZOS)
    # 切れている側に余白を多く取る（例: 下が切れていれば、絵を上に寄せる）
    # 切れている向きは、保存済みの調べた結果を使う（ここで切り抜きAIを読み込むと、描き足しのAIと合わせてメモリが足りなくなる）
    import os
    cut = json.load(open(src + ".check.json")).get("cut", []) if os.path.exists(src + ".check.json") else check(src).get("cut", [])
    global _SESSION
    _SESSION = None
    import gc; gc.collect()
    def place(lo, hi):   # lo＝左（上）が切れている、hi＝右（下）が切れている
        if hi and not lo:
            return 6                 # 右（下）に描き足す余白を取る
        if lo and not hi:
            return 512 - s - 6       # 左（上）に描き足す余白を取る
        return (512 - s) // 2
    ox, oy = place("左" in cut, "右" in cut), place("上" in cut, "下" in cut)
    # 余白は白い背景にしておく（元の絵をぼかして敷くと、額縁に入った絵のように描かれてしまった）
    canvas = Image.new("RGB", (512, 512), (245, 244, 241))
    canvas.paste(small, (ox, oy))
    m = np.full((512, 512), 255, np.uint8)
    m[oy + 4:oy + s - 4, ox + 4:ox + s - 4] = 0
    mask = Image.fromarray(m).filter(ImageFilter.GaussianBlur(3))
    pipe = StableDiffusionInpaintPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-inpainting", variant="fp16", torch_dtype=torch.float16,
                                                          safety_checker=None, requires_safety_checker=False)
    pipe = pipe.to(torch.float32)
    pipe.enable_attention_slicing(1); pipe.vae.enable_slicing(); pipe.vae.enable_tiling()
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); pipe.fuse_lora()
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    g = torch.Generator().manual_seed(seed)
    out = pipe(prompt=f"full body of {desc}, the rest of the creature body, legs and tail, plain white background, painterly fantasy concept art",
               negative_prompt="cropped, cut off, frame, border, text, second creature, blurry",
               image=canvas, mask_image=mask, num_inference_steps=8, guidance_scale=1.5, generator=g).images[0]
    keep = Image.fromarray(255 - np.asarray(mask))
    Image.composite(canvas, out, keep).save(dst)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "check":
        for p in a[1:]:
            r = check(p)
            print(p, label(r), r.get("margin", ""), "かたまり", r["parts"])
    elif a and a[0] == "extend":
        extend(a[1], a[2], a[3])
        print("描き足し:", a[2])
    else:
        print(__doc__)
