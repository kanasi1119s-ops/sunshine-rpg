# AIで作ったRPGの敵ドット絵の試作（2026-10-03・2回目「RPG風」）

**AIで作った画像です（試作）。ゲームにはまだ入れていない。** 人間の依頼「RPG風に生成して」で、1回目（`../trial-2026-10-03/`）より大きく・描き込みの多い、戦闘画面の敵らしい絵をねらった。

- モデル: PublicPrompts/All-In-One-Pixel-Model（CreativeML OpenRAIL-M）＋ LCM-LoRA（latent-consistency/lcm-lora-sdv1-5、openrail++）
- 設定: 512×512、8ステップ、CFG 2.0。1体につき乱数の種を2つ試し、良いほうを選んだ（32枚の下絵から12体）
- 仕上げ: `tools/pixel-art/ai-gen/pixelize.py --size 64 --colors 16 --rembg`（64×64・16色・背景透過。背景除去は rembg＋isnet-general-use）
- `〇〇.png` が仕上げ（64×64）、`〇〇_raw.png` が元の下絵、`_compare.png` が並べた比べ（上の段が下絵、下の段が仕上げを4倍に拡大）、`_battle-preview.png` が戦闘画面ふうに並べた見本（ゲームの画面ではない）。
- 名前（日本語）は仮のもの。ゲームで使うときに設定に合わせて決める。

指示文の共通部分:
- A: `fantasy rpg battle enemy sprite, 16-bit era game art, front view facing the viewer, detailed shading with highlights, dark outline, vibrant colors, in pixelsprite style, plain white background`
- B: `fantasy rpg battle enemy sprite, 16-bit era game art, single creature, full body, detailed shading with highlights, dark outline, vibrant colors, in pixelsprite style, isolated on plain white background`

| ファイル | 仮の名前 | 指示文の中身 | 共通部分 | 乱数の種 | 色数 |
|---|---|---|---|---|---|
| direwolf.png | 牙オオカミ | a dire wolf beast with glowing yellow eyes and spiky fur | A | 200 | 16 |
| lizardman.png | よろいトカゲ兵 | an armored lizardman warrior with a curved sword and round shield | A | 107 | 16 |
| wraith.png | フードの亡霊 | a hooded wraith mage with a skull face holding a glowing staff | A | 114 | 16 |
| crystal-golem.png | 水晶ゴーレム | a crystal golem made of blue gemstones | A | 121 | 16 |
| harpy.png | 紫の怪鳥 | a harpy with feathered wings and sharp talons | A | 135 | 16 |
| lich.png | 亡者の王（ボス候補） | a lich king boss with a crown, ragged robes and a purple magic orb | A | 249 | 16 |
| cursed-knight.png | 呪われた騎士 | a cursed undead knight in rusted black armor holding a broken greatsword, red glowing eyes | B | 333 | 16 |
| octopus.png | 大ダコ | a purple tentacled sea monster with one big eye rising from the water, many tentacles | B | 422 | 16 |
| sorcerer.png | 赤衣の魔術師（ボス候補） | an old evil sorcerer boss in dark crimson robes casting purple magic, long white beard | B | 355 | 16 |
| gargoyle.png | 翼の魔像 | a three-headed chimera beast with lion body, eagle wings and snake tail | B | 444 | 16 |
| crawler.png | 黒い大グモ | a giant black desert scorpion monster with raised curled stinger tail and big pincers, side view | B | 311 | 16 |
| bog-beast.png | 沼の獣 | a giant carnivorous flower monster with a big toothed mouth, thick green vines and thorny leaves | B | 300 | 16 |

## 外したもの（20枚）

- **似ている心配があるもの（CLAUDE.md 1-1）**: 火のサラマンダー2枚（赤と黄色の、立って歩く小さなトカゲの姿になり、有名なゲームのモンスターを連想させた）。角のある緑の大口の怪物1枚（plant2_1。有名なゲームの悪役の怪獣を連想させるおそれがあるため、念のため外した）。
- **指示どおりの形にならなかったもの**: 食虫植物（赤い丸い頭の人・ただの木）、サソリ（カメのような形・形がくずれた）、海の大蛇（ただの波・青い恐竜）、リッチ1枚（門の絵になった）、ヘビの尾のキメラ1枚（ピンクの獅子。形はよいが色が浮く）。
- **選ばなかったほう**: 同じ指示の2枚のうち、形や描き込みが劣るほう。

## 気づいたこと

- 「白い背景」と指示しても、景色や地面が描かれることが多い。四すみの色で消す方法では地面が残ったので、AIの切り抜き（`--rembg`）を足した。牙オオカミの足元に、地面のかけらが少し残っている（手で消す）。
- 1回目（48px・12色、素朴な形）より、陰影と描き込みが増え、戦闘の敵らしくなった。ただし、細部（顔・手・武器）はつぶれやすく、ゲームに入れる前に手で直す必要がある。
- 下絵の種類の当たり外れが大きい（32枚のうち、使える形は半分ほど）。
- 生き物の名前だけで指示すると、有名作品のデザインに寄ることがある（サラマンダーなど）。指示に色や体の特徴を自分で決めて書くほうが安全。
- 色は16色に収まったが、12体それぞれでパレットが違う。ゲームに入れるときは、共通のパレットに合わせる（工程表の課題）。
