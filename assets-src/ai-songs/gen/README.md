# 3分ループ曲の生成スクリプト（2026-10-02）
8小節ごとの構成（導入・Aメロ・サビ・間奏・ソロ・最後は導入に戻る）から、AIソング形式のJSONを作る。
実行（リポジトリの直下で）: `python3 assets-src/ai-songs/gen/song1.py`（song2・song3 も同様）。各パートの長さが32拍でないとエラーになる。
作った曲: boss-crimson-gate（ラウドメタル）、caravan-hijaz（民族音楽）、neon-circuit（ダンス）。ゲームの曲には登録していない。
