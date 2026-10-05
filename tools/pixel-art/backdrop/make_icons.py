"""仲間6人の顔アイコン（assets-src/characters/party-dot/<名前>/アイコン_512x512.png）を、会話欄用（256×256。画面は論理の2〜4倍の細かさで描くので、大きめの絵をなめらかに縮めて描く＝くっきり）に縮める。
使い方: python3 tools/pixel-art/backdrop/make_icons.py　出力: src/assets/portraits/<romaji>.png"""
from pathlib import Path
from PIL import Image, ImageFilter

SRC = Path("assets-src/characters/party-dot")
DST = Path("src/assets/portraits")
SIZE = 256
SMALL = 112  # つよさ画面の一覧用（<romaji>-s.png）
NAMES = {"ユーリ": "yuri", "レト": "reto", "ミナ": "mina", "コハク": "guide", "オルカ": "orca", "アヤメ": "ayame"}
DST.mkdir(parents=True, exist_ok=True)
for jp, name in NAMES.items():
    im = Image.open(SRC / jp / "アイコン_512x512.png").convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
    im.save(DST / f"{name}.png", optimize=True)
    small = Image.open(SRC / jp / "アイコン_512x512.png").convert("RGBA").resize((SMALL, SMALL), Image.LANCZOS)
    small.save(DST / f"{name}-s.png", optimize=True)
    print(name, (DST / f"{name}.png").stat().st_size)
