# `/make-art` の見本（2026-10-03）

スキル `/make-art`（`.claude/skills/make-art/`）の手順を確かめたときの見本です。**ゲームには入れていません。** 名前はすべて仮のものです。

## フィールド用キャラ（`field/`）

16×32・4方向×3コマ。`field_sprite.py` の型（`field_templates.py`。手描き）に色を当てはめたもの。`〇〇.png` は12コマの一覧（横: コマ0〜2、縦: 下・上・左・右、8倍）、`〇〇.walker.json` はゲームの形式（WalkerData）、`〇〇.colors.json` は使った6色。どれもドット絵エディタで描いて「食い違い0マス」を確かめた（`--zoom 7`）。

| 見本 | 組み合わせ | 色の出どころ |
|---|---|---|
| boy（村の少年） | spiky＋tunic＋band | AIのデザイン画から取り出し、髪と目印の色を手で変えた（黒いとがった髪＋赤いはちまきは、有名なキャラを思わせるので避けた） |
| fighter（旅の戦士） | short＋tunic＋cape,backsword | AIのデザイン画を見て、6色を手で決めた（自動の取り出しでは肌が緑になった） |
| knight（騎士） | short＋tunic＋helmet,sword,shield,cape | 手で決めた（デザイン画なし） |
| mage（老魔法使い） | hood＋robe＋beard＋staff | AIのデザイン画を見て、手で決めた（自動では肌が青になった） |
| priestess（巫女） | long＋dress＋cape | AIのデザイン画を見て、手で決めた（自動では髪が肌色になった） |

## 登場人物の全身の絵（`character/`）

128×128・24色。`make_jobs.py character`（縦長512×768）→ `generate.py` → `sfcize.py`。`〇〇_raw.jpg` が下絵、`〇〇.png` が仕上げ。どれもエディタで描いて「食い違い0マス」を確かめた（`--zoom 6`）。

| 見本 | 指示文の中身 | 乱数の種 | 手直し |
|---|---|---|---|
| swordswoman | a young traveling swordswoman with short red hair, green hooded cloak, brown leather armor and a long sword | 1500 | 目・眉・口（`swordswoman-edits.json`） |
| oldmage | an old wandering mage with a long gray beard, deep blue robe with silver trim and a wooden staff | 1531 | なし |
| merchant | a cheerful round merchant woman with an orange headscarf, yellow apron and a large backpack | 1593 | なし |

- 正方形（512×512）で描かせたときは、4人中3人の頭が切れた。縦長では8枚中6枚で全身が入った（騎士2枚は頭が切れたので外した。1枚にはサインのような文字も入っていた）。
- モデル: stable-diffusion-v1-5/stable-diffusion-v1-5（CreativeML OpenRAIL-M）＋ LCM-LoRA（openrail++）。背景の切り抜きは rembg（MIT）＋ isnet-general-use（Apache-2.0）。
