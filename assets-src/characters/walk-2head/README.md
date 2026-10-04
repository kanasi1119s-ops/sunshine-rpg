# 2頭身の歩くキャラ（仲間6人、16×32・4方向×3コマ）

2026-10-04 に作った新しい2頭身の絵（`/make-art` のフィールド用キャラ）。人間の指示「2頭身のドットキャラ新しいのあるからそっちを使って」で、エフェクトの見本の動画（`tools/pixel-art/fx/fx_preview.py --party`）の味方に使う。
形式: `{"palette": [...], "frames": {"down0".."right2": [32行×16文字]}}`（記号 A=palette[0]、B=palette[1]…、"." は透明）。
ゲームの中（`src/game/sprite/walker-data.generated.ts`）は、まだ前の絵のまま。入れかえるときは `docs/decisions.md` に書く。
