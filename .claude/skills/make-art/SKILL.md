---
name: make-art
description: サンシャインRPGの絵（戦闘の敵・ボス、登場人物の全身の絵、フィールド用の歩くキャラ 16×32）を、画像生成AIの下絵とドット絵エディタで作る。「モンスターを作って」「敵の絵を作って」「キャラクターの絵を作って」「フィールドのキャラを作って」と頼まれたとき、また /rpg-cycle のアート担当がこれらを作るときに使う。
---

# 絵を作る（モンスター・キャラクター・フィールド用キャラ）

3種類あります。まず種類を決めて、そのファイルを読んでから始める。

| 種類 | 何に使う | 大きさ | 読むファイル |
|---|---|---|---|
| **モンスター**（ザコ・ボス） | 戦闘の敵 | ザコ 96×96・20色／ボス **256×256・40色**（2026-10-04 人間の指示。以前は128で作って2倍） | `monster.md` |
| **キャラクター** | 登場人物の全身の絵（戦闘・会話・立ち絵） | 128×128・24色 | `character.md`（顔アイコン 512・128 の頼み方の見本は `prompt-icon.md`） |
| **フィールド用キャラ** | マップを歩く人（主人公・仲間・町の人） | 16×32・4方向×3コマ・20色以内 | `field-character.md`（頼み方の見本は `prompt-field-character.md`） |

## どの種類でも守ること

1. **既存作品のまねをしない（CLAUDE.md 1-1）。** AIへの指示文に、作品名・ゲーム名・作者名・既存のキャラやモンスターの名前を書かない（`make_jobs.py` が一部の言葉を止める）。生き物・人物の種類に、色・体の特徴・持ち物を自分で決めて足す。できた絵は必ず目で見て、有名な作品のキャラ・モンスターを連想させたら使わない（例: 赤と黄色の二足で立つ小さなトカゲ、赤いきのこの帽子の子ども、黒いとがった髪に赤いはちまき）。外した理由も記録する。
2. **ドット絵エディタで描く**（`roles.md` 3-8）。仕上げた文字グリッドを `tools/pixel-practice/editor-draw.mjs` でエディタに1ドットずつ描き、「食い違い0マス」を確かめる。エディタは `tools/pixel-editor/index.html`（Artifact「ドット絵エディタ」 https://claude.ai/artifact/Xo7VKZU9cHJk15BnvVmxdp と同じもの。レイヤー・フレーム対応のAseprite風。使い方は同じフォルダの README.md）で、`editor-draw.mjs` は `EDITOR` を指定しなければこれを使う。**`--zoom` は6以上**（5以下だとマウスの位置がずれて食い違いが出た）。
3. **敵・ボスは全身を入れる**（人間の指示、2026-10-04）。下絵は置き場所の下書き（`layouts.py`）から描き、`fullbody.py` の全身チェックが「全身OK」のものだけ使う。顔は右向き（戦闘では敵が左側）。手順は `monster.md` の2。
4. **メモリに注意**: 絵の生成（generate.py）と、背景の切り抜き（rembg）・エディタ（ブラウザ）を**同時に動かさない**（メモリ7GBほどの環境で生成が止まった）。生成 → 終わってから変換・エディタ、の順にする。
5. **記録する**: AIで作った絵は、`assets-src/ai-generated/<日付>-<内容>/` に、仕上げた絵・下絵・README（指示文・乱数の種・モデル・外したものと理由）を置く。`docs/assets-credits.md` の「AIで作った絵」の表に1行足す。
6. **ゲームに入れるとき**（人間の指示、2026-10-03）: 入れてよい。ただし、ゲーム内の絵のデータの近くと `docs/progress.md` に「AIの下絵から作った」と書き、実行レポートの「人間に確認してほしいこと」に、並べた画像（見本）とともに挙げる。人間が差し戻したら外す。
7. **無料素材の利用**: クレジット表記が必要な無料素材（CC-BY・OGA-BY など）も、規約を守れば参考・部品に使ってよい（人間の指示、2026-10-03）。使うときは `docs/assets-credits.md` に記録し、ゲーム内のクレジットに表記する。表記が必要な素材がどれかは各フォルダの `CREDITS.md`・`manifest.csv` で分かる。

## ゲームの敵ぜんぶを作るとき（2026-10-04〜）

`monster_batch.py`（名簿 `monster-roster.json`・ボス24体と雑魚200種）で、4体ずつ進める。`next`→（名簿の prompt に英語の指示文を書く）→`draft`→見比べて `pick`（左向きなら `--mirror`）→手直し→エディタ→`final.txt/json`→`done`→`export`→`node tools/pixel-art/export-game-data.mjs`。顔は右向き。雑魚は 96×96・20色（`enemy:<id>`）、ボスは 128×128・24色を2倍で 256（`boss:<id>`）。

## 道具（`tools/pixel-art/ai-gen/`）

| 道具 | すること |
|---|---|
| `prompts.json` | 種類ごとの指示文の雛形（後ろにつく共通の文・避けるもの・大きさ） |
| `make_jobs.py` | 種類と短い説明から、生成の指示ファイルを作る |
| `generate.py` | 下絵を描く（CPUで1枚50〜80秒） |
| `sfcize.py` | 絵画風の下絵 → 重厚なドット絵（モンスター・キャラクター） |
| `edits.py` | 文字グリッドに点を打ち直す（目・顔・牙などの手直し） |
| `field_sprite.py` ＋ `field_templates.py` | フィールド用キャラ（型＋色＋飾り） |
| `pixelize.py` | 背景の切り抜き（`--rembg`）、素朴な小さいドット絵 |

準備（はじめての環境で一度だけ）: `pip install --break-system-packages torch diffusers transformers accelerate safetensors peft rembg onnxruntime scikit-learn scikit-image`（torch は CPU 版で可）。モデルは初回に自動で取得される（Stable Diffusion 1.5 は約2GB、rembg のモデルは約180MB）。

## 手引き

- 敵の絵の考え方・失敗例: `docs/design/heavy-enemy-workflow.md`
- マップのキャラの決まり（大きさ・4方向・歩き・色数）: `docs/design/pixel-character-guide.md`
- AIでドット絵を描くときの一般的な注意: `docs/design/pixel-art-ai-workflow-notes.md`
