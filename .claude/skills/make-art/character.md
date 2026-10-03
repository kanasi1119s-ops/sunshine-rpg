# キャラクター（登場人物の全身の絵）の作り方

目標: 戦闘・会話・立ち絵に使う、陰影の重い全身のドット絵（128×128・24色）。ゲームの登場人物の枠は256×256（`roles.md` の大きさの基準）なので、128で作って2倍で表示する（1ドット＝2×2）。256で直接作ると、顔の手直しの量が4倍になり、エディタの画面にも入りきらない。作り方はモンスターと同じ流れ（`monster.md`）で、人物ならではの注意を足したもの。特定の漫画家・イラストレーターの絵柄に寄せない（CLAUDE.md 1-1）。

## 1. 何を描くか決める

`docs/story/characters.md` の設定（年齢・役割・髪・服・持ち物）から、英語で1文にする。
- 例: `a young traveling swordswoman with short red hair, green hooded cloak, brown leather armor and a long sword`
- 例: `an old wandering mage with a long gray beard, deep blue robe with silver trim and a wooden staff`
- 例: `a broad-shouldered knight captain with short brown hair, steel plate armor, a crimson cape and a big round shield`
- 髪の色・服の色・目印の1色は、フィールド用キャラ（`field-character.md`）と**同じ色**にする（同じ人物だと分かるように）。
- 避ける: "anime"・"manga"・"chibi"・特定の作家名や作品名。

## 2. 下絵を描く

```sh
python3 tools/pixel-art/ai-gen/make_jobs.py character jobs.json "swordswoman:a young traveling swordswoman with ..." --seeds 2
MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5 VARIANT=fp16 STYLE=painterly python3 tools/pixel-art/ai-gen/generate.py jobs.json
```
- **縦長（512×768）で描かせる**（雛形の既定）。正方形（512×512）だと、頭か足が切れることが多かった（4人中3人で頭が切れた）。
- 縦長は1枚2分ほどかかる（メモリ節約のため、注意を1つずつ計算している）。
- 頭・足が切れた絵、2人描かれた絵、顔が崩れた絵は捨てる。

## 3. ドット絵にする

```sh
python3 tools/pixel-art/ai-gen/sfcize.py raw/swordswoman_0.png out/swordswoman 128 24
```

## 4. 手直し（人物は顔がいちばん大事）

128×128 では顔が10〜14ドットほどになり、そのままでは目鼻がつぶれる。`edits.py` で直す。
1. **目**: 左右に2×1か2×2ドットの暗い目＋1ドットの明るい光。眉を暗い1ドットの線で。
2. **口**: 暗い1〜2ドット。表情を出したいときだけ。
3. **髪**: 髪の流れに沿って、明るい1ドットの線を2〜3本（つやの筋）。
4. **手・武器の先**: 縮小で欠けやすい。剣の刃は、明るい色の1ドットの線を通す。
5. **服の目印**: フィールド用キャラと同じ色の帯・襟・マントを、はっきりした色で。
6. 外周の黒一色の線・孤立点・背景の取り残しが無いか。**似ていないかの確認**（SKILL.md の1）。

## 5. エディタで描いて確かめる

```sh
EDITOR=<保存したエディタのindex.html> node tools/pixel-practice/editor-draw.mjs out/swordswoman_fix.txt out/swordswoman_fix.json out/swordswoman-editor.png --zoom 6
```
「食い違い 0 マス」を確かめる。128×128 は `--zoom 6`（キャンバスが画面に入る倍率）で描く。
- 256×256 など大きな絵は、マウスで1マスずつ塗ると30分以上かかる。`--import --wide` を付けると、エディタの「貼り付けて読み込む」で読み込み（20秒ほど）、同じように「食い違い 0 マス」を確かめられる。128×128 も `--import` で速くなる。

## 5-2. 顔のアイコン（512×512、人間の指示 2026-10-04）

イメージ画像の「顔のアップ」から作る。**顔・頭が切れないこと**（頭のてっぺん〜あご、髪飾り・帽子まで入れ、上に少し余白）。
1. **顔の大きさをそろえる**（人間の指示 2026-10-04）: `tools/pixel-art/ai-gen/icon_frame.py` で、両目・あご先・顔の幅を指定して構図を決める（足りない所は描き足す）。√(目〜あご × 顔の幅) が全員同じになる。目〜あごだけでそろえると、顔の細い大人の男性が小さく見えた。
2. rembg の `isnet-anime` で切り抜き、いちばん大きなかたまりだけ残す（街灯などの背景の取り残しは、色や範囲を指定して消す）。
3. `icon512.py 切り抜き.png 出力名 512 32 --crop x,y,一辺`（正方形の構図のまま減色・縁取り。胸の下の切れ目は縁取りしない）。
   **構図は顔に寄せる**（人間の指示 2026-10-04）: 頭のてっぺんの上に少し余白、あごの下に首元が少し入る大きさ。顔の幅が画面の約6割。横に流れる長い髪やリボンの端は切れてもよい。128×128 も同じ構図で `... 128 24 --crop ...`。
4. エディタで描き（512 は `--import --wide --zoom 4`、128 は `--import --zoom 6`）、「食い違い 0 マス」を確かめる。
5. 頼み方の見本は `prompt-icon.md`。

## 6. 記録・ゲームへ

SKILL.md の4・5。会話の顔は、立ち絵の頭の部分を切り出して使う（`docs/decisions.md` 2026-09-29 の大きな絵の取り込み方と同じ）。
