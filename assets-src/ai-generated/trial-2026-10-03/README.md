# AIで作ったドット絵の試作（2026-10-03）

**AIで作った画像です（試作）。ゲームにはまだ入れていない。** 道具と使い方は `tools/pixel-art/ai-gen/`。

- モデル: PublicPrompts/All-In-One-Pixel-Model（CreativeML OpenRAIL-M）＋ LCM-LoRA（openrail++）
- 設定: 512×512、6ステップ、CFG 1.5
- 仕上げ: `pixelize.py`（長い辺48px・12色以内・背景透過）
- `〇〇.png` が仕上げたドット絵、`〇〇_raw.png` が元の下絵、`_compare.png` が並べた比べ（上が下絵、下が仕上げを4倍に拡大）。

| ファイル | 指示文の中身（共通部分: `full body, front view, rpg game enemy, in pixelsprite style, simple flat colors, black outline, centered, plain white background`） | 乱数の種 | 色数 |
|---|---|---|---|
| slime.png | a round blue slime monster with big eyes | 7 | 11 |
| ghost.png | a floating purple ghost with a lantern | 8 | 11 |
| golem.png | a stone golem with glowing cracks | 9 | 11 |
| whelp.png | a small red dragon whelp with wings | 10 | 12 |
| bat.png | a giant bat demon with spread wings | 11 | 9 |
| skel.png | a skeleton knight with a rusty sword and shield | 13 | 12 |
| imp.png | a small horned imp demon holding a trident | 14 | 12 |

**外したもの**: 「a walking mushroom monster with a spotted cap」（乱数の種12）。赤いキノコの帽子と青い服の子どもの姿になり、有名なゲームのキャラを連想させたため（CLAUDE.md 1-1）。

**気づいたこと**:
- 形は分かるが、描き込みは少なく素朴。スライム・ゴーストは指示より単純になった。
- 背景は単色ではなく色付きになったが、四すみの色で消せた。
- コウモリの悪魔・小悪魔・スケルトン騎士は、敵として使えそうな形。
