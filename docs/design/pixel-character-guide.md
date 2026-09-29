# RPGのドットキャラクターの作り方（手引き）

マップを歩くキャラクター（主人公・仲間・町の人）のドット絵を作るための手引きです。2026-09-30、人間の依頼（「RPGでのドットキャラクターの作り方を学んできてください。参考にキャラクターを50人ほど選んでください」）で、ネット上の解説を読み、参考のキャラクター50人を数値と目で分析してまとめました。

- **既存作品の絵・キャラクターは写さない**（CLAUDE.md 1-1）。ここに書くのは、たくさんのキャラクターに共通していた「作り方の型」と数値だけ
- 参考の50人は、**利用条件がはっきりした無料素材（OpenGameArt の CC0＝権利放棄）だけ**から選んだ。1件ずつライセンス欄が CC0 だけであることを確かめ、説明文で既存ゲームの名前や「〜風」を名乗る作品、他人の絵の改変、有料素材、AI での利用を禁じる作者の作品は外した。絵そのものはリポジトリに入れていない（作業用の一時フォルダで分析した）
- 色・陰影・縁取りなどの一般的な技法は `docs/design/pixel-art-notes.md`。この手引きは「キャラクター」に絞る

## 1. うちのマップのキャラクターの現状（2026-09-30）

- マップは16ドットのタイル、画面は400×225ドット
- 主人公・名前のあるNPCは、**12×14ドットの「顔だけ」の絵**（`src/game/portrait/portraits.ts`）。体が無く、向きごとの絵も無い。向きは小さな三角形で示している（`src/render/player-renderer.ts`）
- 歩きは、2コマで1ドット浮かせるだけ
- 名前の無い町の人は、色つきの四角
- 登場人物の256×256の絵（会話・戦闘用）は別にある（`src/game/art/`）

→ 下の型に沿って、**体のある4方向・歩きつきのマップ用キャラクター**に作り直すと、見た目が大きく上がる。

## 2. 大きさと頭身（50人の数値）

| 大きさの帯 | 人数 | 大きさ（中央値） | 頭身（中央値と範囲） | 頭の高さ÷全体 | 色数（中央値） |
|---|---|---|---|---|---|
| 小（高さ17ドット以下） | 21 | 13×15 | **1.9**（1.7〜2.3） | 0.53 | 7 |
| 中（18〜32） | 14 | 14×23 | **2.0**（1.6〜2.9） | 0.49 | 13 |
| 大（33以上） | 15 | 17×41 | **2.8**（1.7〜3.7） | 0.36 | 31 |

- **小さいキャラほど頭が大きい。** 16ドット前後では、頭が全体の半分（2頭身）。頭が小さいと、顔も表情も読めず「棒人間」に見える（解説でも同じ指摘）
- 解説の目安: 16×16は2〜3頭身、24ドットは2.5〜3.5頭身、32ドットは3〜4頭身。**画面を見渡すRPGのマップでは、2〜2.5頭身が主流**（50人の中央値も2.0）
- マップの1マスに対して、**幅は1マス、高さは1〜2マス**が基本。上半分が後ろのマスに重なってよい（奥行きが出る）
- 幅÷高さは、小0.81・中0.66・大0.38。背が高くなっても、幅はあまり増やさない

## 3. 4つの向き

- **描くのは3方向（正面・横・後ろ）。反対の横は、左右反転で作る**（解説・50人とも共通）。ただし、髪の分け目・紋章・片手の武器など**左右で違う物がある場合は、反転せずに描き直す**
- **向きを変えても、高さを変えない。** 正面と横・後ろの高さの差が1ドット以内だったのは40人中37人。足元の線（床）もそろえる
- 横向きの幅は、小さいキャラでは正面より少し細く（0.86倍）、大きいキャラでは腕・足が前後に出るぶん太くなる（1.24倍）
- 正面は顔・胸で読ませる。後ろは後頭部・肩・背中（髪の形と服の色）で読ませる。横は、手前の足を太く、奥の足を細くして前後を出す
- 見下ろしのRPGは、真横・真上ではなく「斜め上から」見る。頭のてっぺんが少し多めに見え、**目は頭の下寄り**に置く

## 4. 歩きのアニメーション

（正面の歩きが1コマしか無い1人を除いた49人）

| コマ数（正面） | 人数 | 使い方 |
|---|---|---|
| 2 | 7 | 足踏みだけ。町の人の待機など |
| **3** | **24** | 左足・立ち・右足を **1→2→3→2** と往復。いちばん多い、古典的な形 |
| **4** | 16 | 立ち・片足・立ち・反対の足。接地の感じが出る。工数の増加は小さい |
| 6・8 | 2 | なめらか。大きいキャラ・走り向き |

- **動かすのは主に足（下半分）。** コマ間で変わるドットは、下半分が上半分より多い（49人中43人）。小さいキャラでは、頭と顔はまったく動かさず（上半分の変化は中央値6%）、足と腕を1〜2ドット動かすだけ
- **足元の線は全コマで同じ高さ。** 1ドットでもずれると、すべって見える。遊んでいる足は、床の足より2ドットほど高く、前後にずらす
- **上下の揺れは0〜1ドット。** 揺れなし22人・1ドット21人・2ドット以上6人。32ドットまでは±1ドット、64ドットでも1〜2ドットまで。足を出したコマで体を1ドット沈める（または、足がそろうコマで1ドット上げる）
- **腕は足と逆に振る**（右足が前なら左手が前）。振り幅は2ドット程度に抑えると、腕だけが目立たない
- **目・顔は歩きの間に変えない。** まばたきは待機のときに別に入れる
- コマの速さ: 1コマ0.1〜0.15秒くらい（3コマ往復なら1周0.4〜0.6秒）。遅いとのろく、速いとせわしない

## 5. 縁取り・色

- **外周の縁取り**: 黒に近い暗い色で1ドットの外周を閉じたのが50人中32人（小さいキャラでは21人中15人）。背景がどの地形でも形が保てる。純黒（#000）より「とても暗い色」の方が、なじみやすい（解説）
- 白い外枠（シール風）は4人。背景から強く浮くが、画面の中でキャラだけ浮きすぎることもある
- **色数**: 小さいキャラは7色前後（最少3色）、中は13色、大は30色前後。解説の目安は、**1つの部分に2〜3色（基本・影・光）、全体で6〜12色**。うちのデータ形式の上限は26色
- 役割（戦士・魔法使い・神官・村人など）は、**色と形（シルエット）で描き分ける**。鎧は金属の灰色、ローブは台形、杖・剣・帽子で形を変える。影絵にしても誰か分かるか確かめる
- 光は上（または左上）から。頭・肩を明るく、頭の下・足を暗く
- 足元に、丸い落ち影を置く（地面に立って見え、当たり判定も伝わる）

## 6. 顔・目（大きさ別）

| 頭の大きさ | 目の描き方 |
|---|---|
| 小（頭8ドット前後） | 目は1×1か1×2ドットの暗い点。表情は髪・色・服で出す |
| 中（頭10〜14ドット） | 2×2ドット（瞳＋光の点1つ）で生き生きする |
| 大（頭16ドット以上） | 瞳・光・まぶた・眉が描ける。瞳の大きさで感情が出る |

- 表情は、目・眉・口だけを変える（嬉しい＝目を閉じて口角を上げる、怒り＝V字の眉、驚き＝目を大きく口を丸く）
- 50人の多くは、小さな顔でも目の位置と数ドットの口だけで表情を出している

## 7. うちのゲームへの当てはめ（提案。まだ決めていない）

**マップ用キャラクターの大きさは、人間の判断が要る。** 絵の大きさの基準（`roles.md` 3-8: 登場人物は256×256）は会話・戦闘の絵のためのもので、16ドットのマスを歩くマップのキャラクターには大きすぎる（画面の高さ225ドットに収まらない）。マップ用は別の大きさにすることを提案する。

| 案 | 大きさ | 頭身 | 良いところ | 気をつけるところ |
|---|---|---|---|---|
| A | **16×24**（幅1マス・高さ1.5マス） | 2〜2.3 | 50人の「中」の中央値に近い。今の画面の広さ・当たり判定（12×14）とつり合う | 顔は小さい（頭10〜12ドット） |
| B | 16×32（幅1マス・高さ2マス） | 2.3〜2.8 | 服・装備を描き込める | 画面の中でキャラが大きく、マップが狭く感じる |
| C | 16×16（今のマスと同じ） | 1.8〜2 | いちばん軽い | 256×256の絵との落差が大きい |

- どの案でも: **4方向×3コマ（1→2→3→2）**を基本に、正面・横・後ろの3方向を描き、横の反対は反転（左右で違う物がある仲間は描き直す）。暗い外周の縁取り、全体で12色以内、足元の線を固定、足を出したコマで1ドット沈む、足元に丸い影
- **256×256の絵と同じ色**（髪・服・目の色）を使い、会話・戦闘の絵と同じ人物だと分かるようにする。仲間どうしは、髪の色と、服の中の鮮やかな1色（目印）で見分ける
- 名前の無い町の人は、同じ体の型（素体）に髪・服の色と帽子などの小物を替えて、数を増やす（素体＋部品の考え方は、解説と、50人の中の素体テンプレートに共通）

## 8. チェックリスト（キャラクターを1人作ったら）

1. 頭身は大きさの帯の目安どおりか（16〜24ドットなら2〜2.5頭身）。影絵にしても誰か分かるか
2. 正面・横・後ろで高さが同じか（差は1ドット以内）。足元の線はそろっているか
3. 反転した横向きで、髪の分け目・武器・紋章が逆になっていないか
4. 歩きで動くのは足と腕だけか。顔は動いていないか。上下の揺れは1ドット以内か
5. 外周は暗い色で閉じているか。色は12色以内（形式の上限26色）か
6. 地形（草・土・水・崖）の上に置いて、すぐ見つかるか。足元に影があるか
7. 256×256の絵と同じ人物に見えるか（髪・服・目の色）
8. 既存作品のキャラクターに似ていないか（1-1）

## 出典

### 読んだ解説（文章・作例の写しは載せていない）
- [Pixelblog 22 - Top Down Character Sprites（SLYNYRD）](https://www.slynyrd.com/blog/2019/10/21/pixelblog-22-top-down-character-sprites)
- [Pixelblog 55 - Top Down Character Animation（SLYNYRD）](https://www.slynyrd.com/blog/2025/3/24/pixelblog-55-top-down-character-animation)
- [ドット絵の歩行アニメーション｜4方向キャラの動かし方（ピクセラボ）](https://pixelartlab.net/tutorials/dot-e-walk-animation)
- [RPG用のドット絵素材の規格とサイズ（ピクセラボ）](https://pixelartlab.net/game-dev/rpg-maker-dot)
- [How to Draw Pixel Art Characters（Pixnote）](https://pixnote.net/en/learn/character/)
- [Pixel art eyes design（Sandro Maglione）](https://www.sandromaglione.com/articles/pixel-art-eyes-techniques-and-styles)
- [Top-down game Pixel art - Design and Animations（Sandro Maglione）](https://www.sandromaglione.com/articles/pixel-art-top-down-game-sprite-design-and-animation)
- [ゲーム風ドット絵キャラクターの描き方（DOT ART PLAY）](https://dotartplay.com/game-characters-dot-summary)（既存ゲームごとの大きさの比べが中心だったため、一般的な数値の範囲だけを参考にした）

> 「The RPG Base's Four Directions」（finalbossblues.com）は、リダイレクトが解決できず本文を読めなかったため、反映していない。

### 参考にしたキャラクター50人（すべて OpenGameArt の CC0。絵はリポジトリに入れていない）

| 作品名 | 作者 | 入手元 | ライセンス | 人数 | 選んだキャラクター |
|---|---|---|---|---|---|
| 16x16 8-bit RPG character set | devurandom | https://opengameart.org/content/16x16-8-bit-rpg-character-set | CC0 | 5 | 戦士・魔法使い・黒装束・神官・村人 |
| 24x32 bases | Cabbit | https://opengameart.org/content/24x32-bases | CC0 | 1 | 素体（24×32） |
| 8bit rpg hero | danbu | https://opengameart.org/content/8bit-rpg-hero | CC0 | 1 | 勇者（紫の帽子） |
| Bushly and Princess Sera | GrafxKid | https://opengameart.org/content/bushly-and-princess-sera | CC0 | 1 | 王女 |
| Character sprite + walk animation | Belohlavek | https://opengameart.org/content/character-sprite-walk-animation | CC0 | 1 | 青年（赤い服） |
| Classic Hero | GrafxKid | https://opengameart.org/content/classic-hero | CC0 | 1 | 勇者（丸頭） |
| Elliot RPG | software_atelier | https://opengameart.org/content/elliot-rpg | CC0 | 1 | 少年（エプロン） |
| Fumiko Complete Charset | skoam | https://opengameart.org/content/fumiko-complete-charset | CC0 | 1 | 女戦士 |
| Hero character sprite sheet | Fry | https://opengameart.org/content/hero-character-sprite-sheet | CC0 | 1 | 主人公（マント） |
| Human RPG Character | Shepardskin | https://opengameart.org/content/human-rpg-character | CC0 | 1 | 人間の子 |
| Mer RPG Character | Shepardskin | https://opengameart.org/content/mer-rpg-character | CC0 | 1 | 人魚 |
| Modern RPG Guy | OVFudj | https://opengameart.org/content/modern-rpg-guy | CC0 | 1 | 現代の青年 |
| Nora World View Sprites | Pixel Scuba | https://opengameart.org/content/nora-world-view-sprites | CC0 | 1 | 少女（白髪） |
| Pixel Art Character | acasas | https://opengameart.org/content/pixel-art-character | CC0 | 1 | 少年（帽子） |
| Puny Characters | Shade | https://opengameart.org/content/puny-characters | CC0 | 3 | 兵士・弓兵・魔導士 |
| RPG Character 'Knight' (NES) | Chasersgaming | https://opengameart.org/content/rpg-character-knight-nes | CC0 | 1 | 騎士（8bit） |
| RPG Character 'Ranger' (NES) | Chasersgaming | https://opengameart.org/content/rpg-character-ranger-nes | CC0 | 1 | 狩人（8bit） |
| RPG character sprites | GrafxKid | https://opengameart.org/content/rpg-character-sprites | CC0 | 2 | 少年（赤髪）・少女（紫の髪） |
| School Girl | diamonddmgirl | https://opengameart.org/content/school-girl | CC0 | 1 | 学生の少女 |
| Snake RPG Character | Shepardskin | https://opengameart.org/content/snake-rpg-character | CC0 | 1 | 蛇の民 |
| Tiny Characters Set | Fleurman | https://opengameart.org/content/tiny-characters-set | CC0 | 4 | 村娘・少女・少年・青年 |
| Tiny RPG CC0 Characters and Portraits | tiopalada | https://opengameart.org/content/tiny-rpg-cc0-characters-and-portraits | CC0 | 3 | 魔法使い（つば広帽子）・狼の獣人・猫頭巾の子 |
| Tiny RPG - Forest | ansimuz | https://opengameart.org/content/tiny-rpg-forest | CC0 | 1 | 弓使い |
| Top Down Adventure Assets | ansimuz | https://opengameart.org/content/top-down-adventure-assets | CC0 | 4 | 少女（村人）・老婆・賢者・鉱夫 |
| Top down player sprite sheet (Julia) | ArlanTR | https://opengameart.org/content/top-down-player-sprite-sheet-julia | CC0 | 1 | 少女（巻き毛） |
| Various Walkcycle (8 characters) | Skab | https://opengameart.org/content/various-walkcycle-8-characters | CC0 | 8 | 紳士（山高帽）・紳士（シルクハット）・青年（紺の上着）・医師（緑の手術着）・看護師（緑の手術着）・白いドレスの女性・白衣の医師・紳士（帽子とめがね） |
| Walking Character Set | ATMANAN | https://opengameart.org/content/walking-character-set | CC0 | 1 | 少年（青い帽子） |
| Woman RPG Character | josepharaoh99 | https://opengameart.org/content/woman-rpg-character | CC0 | 1 | 女性（ワンピース） |
