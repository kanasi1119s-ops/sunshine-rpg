"""人間がくれた戦闘背景（assets-src/backgrounds/battle-dot/*.jpg、1024×572）を、ゲーム用（400×169・64色のPNG）に縮める。
使い方: python3 tools/pixel-art/backdrop/make_battle_bg.py
出力: src/assets/battle-bg/<名前>.png（名前の対応は下の NAMES）"""
from pathlib import Path
from PIL import Image

SRC = Path("assets-src/backgrounds/battle-dot")
DST = Path("src/assets/battle-bg")
W, H = 400, 169
NAMES = {
    "草原": "meadow", "高地": "highland", "雪原": "snow1", "雪原２": "snow2",
    "海": "sea1", "海２": "sea2", "海上": "ship1", "海上２": "ship2",
    "洞窟": "cave", "火山": "volcano1", "火山２": "volcano2", "マグマ祠": "magma-shrine",
    "祠": "forest-shrine1", "祠２": "forest-shrine2", "異空間": "void1", "異空間２": "void2",
    "予言の間": "prophecy", "歪の間": "warp1", "歪の間２": "warp2",
}  # 草原没作.jpg は没にした版なので使わない

DST.mkdir(parents=True, exist_ok=True)
for jp, name in NAMES.items():
    im = Image.open(SRC / f"{jp}.jpg").convert("RGB")
    # 横長（400:169）に、中央から切り出す
    ch = round(im.width * H / W)
    top = (im.height - ch) // 2
    im = im.crop((0, top, im.width, top + ch)).resize((W, H), Image.LANCZOS)
    im = im.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE)
    im.save(DST / f"{name}.png", optimize=True)
    print(name, (DST / f"{name}.png").stat().st_size)
