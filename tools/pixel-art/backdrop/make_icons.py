"""仲間6人の顔アイコン（assets-src/characters/party-dot/<名前>/アイコン_512x512.png）を、会話欄用（64×64。拡大も縮小もせず1対1で描く＝ぼやけない。輪郭を強めに強調）に縮める。
使い方: python3 tools/pixel-art/backdrop/make_icons.py　出力: src/assets/portraits/<romaji>.png"""
from pathlib import Path
from PIL import Image, ImageFilter

SRC = Path("assets-src/characters/party-dot")
DST = Path("src/assets/portraits")
SIZE = 64
NAMES = {"ユーリ": "yuri", "レト": "reto", "ミナ": "mina", "ガイド": "guide", "オルカ": "orca", "アヤメ": "ayame"}
DST.mkdir(parents=True, exist_ok=True)
for jp, name in NAMES.items():
    im = Image.open(SRC / jp / "アイコン_512x512.png").convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=170, threshold=0))
    im.save(DST / f"{name}.png", optimize=True)
    print(name, (DST / f"{name}.png").stat().st_size)
