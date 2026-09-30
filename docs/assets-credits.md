# 外部素材の記録（出典・規約・クレジット）

無料で商用利用できる素材を使うときの記録です（`CLAUDE.md` 1-1 の例外の運用）。素材を1つ使うごとに、下の表に1行足します。

## 記録のしかた
- 素材名・入手元（URL）・入手日・使った場所（ファイルや画面）
- 利用規約の要点（商用利用、加工・改変、クレジット、再配布、ゲームへの組み込み）。読んだ規約のURLも書く
- クレジット表記が必要か（必要なら、ゲーム内クレジットまたは README に書いたか）
- 規約が読めない・不明な素材は、使わない

## 使用中の素材

| 素材名 | 入手元 | 入手日 | 使った場所 | 規約の要点 | クレジット |
|---|---|---|---|---|---|
| ぴぽや「フィールドマップセット１」「同 追加パーツ」（`pipo-map001.zip`・`pipo-map001plus.zip`） | https://pipoya.net/sozai/assets/map-chip_tileset32/ | 2026-09-30 | 取得・規約確認済み、元ファイルは `assets-src/pipoya/`。**ゲームに反映済み（2026-09-30）**: 地形テクスチャ5点（草A・草B・土の道・水面・深い森。128×128）に、自動タイルの中央の1枚を並べ、色を24色に減らして使用（`tools/pixel-art/import-pipoya.mjs` → `pipoya-terrain.json` → `export-game-data.mjs` → `src/game/art/sprite-data.generated.ts`）。建物・城・山などの他の絵は未使用 | 無料素材利用規約（https://pipoya.net/sozai/terms-of-use/ ）と同梱の readme を確認。商用利用可、加工可、無償の再配布可（規約とともに）、ゲームへの組み込み・販売可。禁止は素材としての販売（転売）。要点は `assets-src/pipoya/LICENSE-pipoya.md` | 不要（お礼として README・ゲーム内クレジットに「ぴぽや https://pipoya.net/」と書く予定） |
| ぴぽや「RPGキャラ基本セット」から9枚（若者女・老人男・王・魔物・魔物ボス・勇者男・勇者女・魔法使い女・僧侶男）と「シンプルエネミーシンボル32×32キャラチップ」から1枚、計10枚 | https://pipoya.net/sozai/assets/charachip/character-chip-1/ | 2026-09-30 | 元ファイルは `assets-src/pipoya/charachip/`・`assets-src/pipoya/simpleenemy/`（同梱の readme も一緒に保存）。**まだゲームには反映していない**（32×32のキャラチップのため、マップのキャラの大きさを人間が決めてから、縮小・色数の調整をして使うか、描き方の参考にする） | 無料素材利用規約（https://pipoya.net/sozai/terms-of-use/ 、2026-09-30 再確認。AIについての記述なし）と同梱の readme を確認。商用利用可、加工可、無償の再配布可（規約とともに）、ゲームへの組み込み・販売可。禁止は素材としての販売（転売）。敵の一枚絵（絵画調でドット絵ではない）と有料のモンスターセットは使わない | 不要（お礼として README・ゲーム内クレジットに「ぴぽや https://pipoya.net/」と書く予定） |
| ドット絵ライブラリ500枚（ぴぽや倉庫 233枚＝RPGキャラ基本セット・キャラチップ32出力素材・シンボルエネミー・ハロウィン・その他キャラチップ・飛空艇・ウディタ２用マップセット・フィールドマップセット１で組み立てたマップ見本／OpenGameArt の CC0 素材 252枚／Kenney の CC0 素材 15枚。配布元の素材セットは148種類） | 1枚ずつのURL・作者は `assets-src/pixel-library/MANIFEST.md` と `manifest.csv`。主な入手元: https://pipoya.net/sozai/ ・ https://opengameart.org/ ・ https://kenney.nl/assets | 2026-09-30 | 元ファイルは `assets-src/pixel-library/`（キャラクター・モンスター・ボス・フィールド・マップ・ダンジョン・町と屋内・小物の8分類）。**まだゲームには反映していない** | CC0 は各ページのライセンス欄（2026-09-30 に全ページを読み直し）と Kenney の License.txt で確認。ぴぽやは無料素材利用規約と同梱の readme（写しは `assets-src/pixel-library/LICENSES/`）で確認: 商用利用可・加工可・ゲームへの組み込み可・無償の再配布可（規約とともに）、素材としての販売は禁止。既存作品に寄せたと書かれたもの・作者の公開済みゲームで使われた絵・AIを使ったと書かれたもの・ドット絵でないもの・文字入りは外した（`assets-src/pixel-library/README.md`） | 不要（CC0 もぴぽやも不要。お礼として README・ゲーム内クレジットに「ぴぽや https://pipoya.net/」「Kenney」「OpenGameArt の各作者」を書く予定） |
| FluidR3 Mono GM サウンドフォント（`FluidR3Mono_GM.sf3`。npm `@librescore/sf3` 0.8.0 に同梱） | https://www.npmjs.com/package/@librescore/sf3 （原典: Frank Wen「Fluid (R3) GM」、Michael Cowgill による Mono 版） | 2026-09-30 | BGMの録音音源。ゲームで使う楽器（GMの17種＋ドラム6セット）だけを `tools/soundfont/trim-soundfont.mjs` で切り出し、`src/audio/soundfont/game.sf3`（約3.3MB）としてゲームに同梱。元ファイルは `assets-src/soundfont/` | MITライセンス（`assets-src/soundfont/LICENSE-FluidR3.md`）。商用利用・改変・再配布・ゲームへの組み込みは可。**著作権表示と許諾文を配布物に含める条件**あり（`public/licenses/FluidR3-GM-MIT.txt` をゲームに同梱、README にも表記）。同梱のサンプルは、パブリックドメインの素材と作者本人の録音、Ethan Winer 氏・Michael Schorsch 氏の提供分 | 必要（README・ゲーム内クレジットに「Fluid (R3) GM SoundFont © Frank Wen / Mono版 © Michael Cowgill（MIT）」と書く） |
| spessasynth_lib / spessasynth_core（サウンドフォント再生ライブラリ。npm） | https://github.com/spessasus/spessasynth_lib | 2026-09-30 | BGMの再生（`src/audio/sampled-engine.ts`） | Apache-2.0。商用利用・改変・再配布は可。ライセンス文を同梱する条件あり（`public/licenses/spessasynth-Apache-2.0.txt`） | 必要（README に表記） |
| Neural Amp Modeler Core（WASM版 `@opendaw/nam-wasm`。npm） | https://github.com/sdatkinson/NeuralAmpModelerCore （WASM版: https://www.npmjs.com/package/@opendaw/nam-wasm ） | 2026-09-30 | 作曲ソフトのアンプシミュレーター（`src/audio/nam/`）。作曲ソフト（`tools/composer/`）にだけ埋め込み、ゲーム本体には入れない | MITライセンス（© 2023 Steven Atkinson）。商用利用・改変・再配布は可。著作権表示と許諾文を含める条件あり。.namモデルは同梱していない。利用者が読み込むモデルは、モデルごとに配布元の規約（商用利用・再配布）を確認する。ゲームにはモデルを入れない | 必要（README に表記） |
| NAMの見本モデル3つ（NeuralAmpModelerCore の `example_models/` の `A2.nam`・`my_model.nam`・`wavenet.nam`） | https://github.com/sdatkinson/NeuralAmpModelerCore （コミット 0b3d3c9） | 2026-09-30 | 作曲ソフトの同梱アンプ（ハイゲインアンプA・B、ベース用プリアンプ）。元ファイルは `assets-src/nam-models/`。ゲーム本体には入れない | リポジトリ全体が MITライセンス（© 2023 Steven Atkinson）で、`example_models/` に別の規約はない。商用利用・改変・再配布は可。著作権表示と許諾文を含める（`assets-src/nam-models/LICENSE-NeuralAmpModelerCore.txt`、`public/licenses/NeuralAmpModelerCore-MIT.txt`）。モデル内の機材メーカー名は画面に出さない | 必要（README に表記） |
| Electron（デスクトップ版の土台）・Anthropic TypeScript SDK（AI作曲の通信）・Model Context Protocol SDK（コネクタ。開発用） | https://www.electronjs.org/ ・ https://github.com/anthropics/anthropic-sdk-typescript ・ https://github.com/modelcontextprotocol/typescript-sdk | 2026-09-30 | デスクトップ版（`desktop/`）とコネクタ（`tools/mcp/`）。ゲーム本体には入れない | すべて MIT（Electron に同梱の Chromium は、各部品のライセンスが `LICENSES.chromium.html` として配布物に入る）。商用利用・再配布は可。ライセンス文を配布物に含める（`desktop/copy-licenses.mjs` が `licenses/` にそろえる） | 必要（デスクトップ版の「ヘルプ」→「ライセンス」） |
| LAME（lamejs、npm `@breezystack/lamejs` 1.2.7）・文字フォント Orbitron と JetBrains Mono（npm `@fontsource`） | https://lame.sourceforge.net/ ・ https://github.com/shijinyu/lamejs ・ https://fonts.google.com/specimen/Orbitron ・ https://www.jetbrains.com/lp/mono/ | 2026-09-30 | デスクトップ版だけ（MP3 の書き出し・画面の英数字の文字）。ゲーム本体には入れない | LAME: LGPL-3.0。商用可。条件（部品の説明による）: 本体と別ファイルで使う・LAME を使っていることと入手先を示す・改変したら公開する（改変していない）。LGPL/GPL の本文と表示を `licenses/` に同梱。フォント: SIL OFL 1.1（商用・同梱可。フォント単体の販売は不可。ライセンス文を同梱） | 必要（「ヘルプ」→「ライセンス」） |

## 素材の置き場
- 元ファイル: `assets-src/`（規約の写しも一緒に置く）
- ゲームに読み込む形（色番号のRLEなど）に変換したもの: `src/game/art/`

## メモ
- 2026-09-30: BGMを録音音源で鳴らすため、サウンドフォントを探した。**GeneralUser GS**（ライセンスは商用利用可だが、作者自身が「サンプルの出どころは100%確認できていない」と明記）は、出どころが不明確なため使わなかった。**MuseScore General**（MIT・一部CC0/PD、出どころが明記）は40MBで大きすぎたため見送り。**FluidR3 Mono GM**（MIT、出どころの明記あり）を採用した。より高品質にしたくなったら、MuseScore General Lite（約40MB）への差し替えを検討する（容量予算は人間が拡大を許可済み）。
- 2026-09-29: 人間から「ぴぽや倉庫（https://pipoya.net/sozai/ ）の無料素材を使う、または参考にする」との指示があった。ただし、この作業環境のネットワークからはpipoya.netに接続できず、素材の取得も規約の確認もできなかった。人間が素材をダウンロードして `assets-src/pipoya/` に置いた時点で、規約（素材に付属のreadmeなど）を確認し、上の表に記録する。
- 2026-09-30: パソコンのClaude Code＋Chrome拡張で、ぴぽや倉庫の規約ページと素材ページを確認し、上の2点を取得した（ダウンロード・展開とも人間の承認済み）。
- 2026-09-30: ぴぽや素材の、生成AI・AI学習・AIが作った作品での利用についての記述を確認した。**結果: 記述なし**（禁止も制限も、許可の明記もない）。
  - 確認した範囲: (1) 素材利用規約 https://pipoya.net/sozai/terms-of-use/ の本文全体（冒頭の「素材利用規約」から末尾の「素材利用許諾者・許諾作品」の表記例まで。無料素材・有料素材・支援サイト限定素材の各規約と特殊事項を含む。約1.1万字）。(2) `assets-src/pipoya/pipo-map001/readme.txt`、`assets-src/pipoya/pipo-map001plus/readme.txt`
  - 確認の方法: Chromeで全文を読んだうえで、本文を取得して「AI」「ＡＩ」「人工知能」「生成」「学習」「機械」「データセット」「ディープ」「深層」「NFT」などの語を検索した
  - 検索に当たったのは「学習」の2か所だけで、どちらも有料素材・支援サイト限定素材の「Scratchでの利用について」にある、購入者自身の学習目的でローカル環境で使うことの話。AIとは関係ない
  - 規約には「予告なく追加変更する場合がある」とあるため、素材を追加で使うときや公開前には、あらためて確認する

## 使わないと決めた素材（2026-09-30 確認）
人間から紹介された Seliel the Shaper（Mana Seed）の素材。Chromeで価格と Mana Seed User License（https://selieltheshaper.weebly.com/user-license.html ）を確認した。

| 素材名 | URL | 価格 | 判断 |
|---|---|---|---|
| Iconic Homestead | https://seliel-the-shaper.itch.io/iconic-homestead | 有料（19.99ドル〜） | 使わない |
| Muddy Cave | https://seliel-the-shaper.itch.io/muddy-cave | 有料（19.99ドル〜） | 使わない |
| Gentle Forest | https://seliel-the-shaper.itch.io/gentle-forest | 無料（0ドル〜。払うと色違いが増える） | 使わない |

理由: 規約の「No GenAI」条項が、AIが作った絵・文章・コードなどと同じ作品で使うことを、例外なく禁じている。このゲームはAI（Claude）がコード・文章・絵を作っているため、無料・有料を問わず条件を満たせない。また Gentle Forest の無料版の色は、既存作品（聖剣伝説3）の各ステージを参考にしたと明記されており、CLAUDE.md 1-1 の点でも避ける。作者の意向を尊重し、技法の参考にもしない（人間の了承済み）。

## 使わないと決めた素材（2026-09-30、ドット絵ライブラリ500枚を選ぶときに外したもの）
既存作品のまね（CLAUDE.md 1-1）や規約・品質の理由で外した主なもの。どれも CC0 だが使わない。

| 素材 | URL | 外した理由 |
|---|---|---|
| 12 Public Domain Boss Sprites | https://opengameart.org/content/12-public-domain-boss-sprites | 画像変換AI（DeepStyle）を使ったと書かれている |
| Versatile 255 tile pixel art pack | https://opengameart.org/content/versatile-255-tile-pixel-art-pack | 既存の有名RPGから着想したと書かれている |
| RPG Town Pixel Art Assets | https://opengameart.org/content/rpg-town-pixel-art-assets | 既存の有名RPGに強く影響を受けたと書かれている |
| 16x16 Overworld Tiles | https://opengameart.org/content/16x16-overworld-tiles-0 | 既存のゲームに着想を得たと書かれている |
| isaiah658's Pixel Pack #1 | https://opengameart.org/content/isaiah658s-pixel-pack-1 | 既存のゲームに着想を得たと書かれている |
| Eyeball boss / Gosoythoth mimic / Walking ice golem | https://opengameart.org/content/eyeball-boss ほか | 既存のゲームや特定の絵を元にしたと書かれている |
| Spring monster pack | https://opengameart.org/content/spring-monster-pack | ツクールの標準素材を含む |
| 2D Retro Baddie Sprites / Knight Enemy / Top Down Adventure Assets / RPG Art Pack | https://opengameart.org/content/2d-retro-baddie-sprites ほか | 作者の公開済みゲームで使われた絵（1-1 を厳しめに解釈） |
| Stalagmite monster | https://opengameart.org/content/stalagmite-monster | 既存のTRPGの魔物を元にしたと書かれている |
| Dungeon Crawl の32×32タイル | https://opengameart.org/content/dungeon-crawl-32x32-tiles-supplemental ほか | 既存のゲームの絵そのもの |
| RotMG Enemy | https://opengameart.org/content/rotmg-enemy | 既存のゲームの絵 |

## 使わないと決めた素材（2026-09-30、BGM）

| 素材 | URL | 外した理由 |
|---|---|---|
| Shade さんの無料曲「RoughEdge20240822」 | https://booth.pm/en/items/6038821 | 規約が「常識の範囲内でお楽しみください」だけで、ゲームへの使用・再配布・学習に使ってよいかが不明 |
| Shade BGM 素材集 VOL1・VOL2 | https://booth.pm/ja/items/1185169 ・ https://booth.pm/ja/items/1185182 | 有料（人間の承認が必要）。再配布の可否は同梱の規約を読まないと分からない。調べた内容は `docs/sound/reference-shade-bgm.md` |
