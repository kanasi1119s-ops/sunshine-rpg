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
| ドット絵ライブラリ2 500枚（1回目とは別の絵。ぴぽや倉庫 168枚＝RPGキャラ基本セットの色違い・グラフィック合成器用パーツの見本キャラ・猫にん・シンボルエネミー・ハロウィン・クリスマス・光モノ・爆弾と風船・本・ウディタ２用マップセット・フィールドマップセット１で組み立てたマップ見本8枚／OpenGameArt の CC0 素材 329枚（186ページ）／Kenney の CC0 素材 3枚） | 1枚ずつのURL・作者は `assets-src/pixel-library-2/MANIFEST.md` と `manifest.csv`。主な入手元: https://pipoya.net/sozai/ ・ https://opengameart.org/ ・ https://kenney.nl/assets | 2026-09-30 | 元ファイルは `assets-src/pixel-library-2/`（8分類）。**まだゲームには反映していない** | CC0 は186ページすべてを 2026-09-30 に読み直して確認、Kenney は License.txt。ぴぽやは無料素材利用規約と各 readme（写しは `assets-src/pixel-library-2/LICENSES/`）: 商用利用可・加工可・ゲームへの組み込み可・無償の再配布可（規約とともに）、素材としての販売は禁止。説明文の全文を読み、既存のゲームの絵・既存のゲームのために作られた絵・既存作品に似せた絵・有名作品の生き物に似たモンスター集・由来があいまいな絵・AIや3D由来の絵を外した（`assets-src/pixel-library-2/README.md`） | 不要（お礼として README・ゲーム内クレジットに「ぴぽや https://pipoya.net/」「Kenney」「OpenGameArt の各作者」を書く予定） |
| ドット絵の参考素材630点（1000点を用意し、作るのに手間がかからないもの370点を削除。ぴぽや倉庫 249点／OpenGameArt の CC0 素材 381点。アイコン・部品など1点ずつの小さな絵を多く含む） | 1点ずつのURL・作者は `assets-src/pixel-reference/MANIFEST.md` と `manifest.csv`。主な入手元: https://pipoya.net/sozai/ ・ https://opengameart.org/ | 2026-09-30 | 元ファイルは `assets-src/pixel-reference/`（描き方の参考・キャラを組み立てる部品）。**ゲームには反映していない** | CC0 は 199 ページすべてを 2026-09-30 に読み直して確認。ぴぽやは無料素材利用規約と各 readme（写しは `assets-src/pixel-reference/LICENSES/`）: 商用利用可・加工可・ゲームへの組み込み可・無償の再配布可（規約とともに）、素材としての販売は禁止。説明文の全文を読み、既存のゲームの絵・既存のゲームのために作られた絵・既存作品に似せた絵・由来があいまいな絵・AIや3D由来の絵を外した。全年齢に合わない絵（下着・水着など）も外した（`assets-src/pixel-reference/README.md`） | 不要（使う場合は、お礼として README・ゲーム内クレジットに書く） |
| FluidR3 Mono GM サウンドフォント（`FluidR3Mono_GM.sf3`。npm `@librescore/sf3` 0.8.0 に同梱） | https://www.npmjs.com/package/@librescore/sf3 （原典: Frank Wen「Fluid (R3) GM」、Michael Cowgill による Mono 版） | 2026-09-30 | BGMの録音音源。ゲームで使う楽器（GMの約60種＋ドラム7セット。2026-10-02に民族楽器を追加）だけを `tools/soundfont/trim-soundfont.mjs` で切り出し、`src/audio/soundfont/game.sf3`（約3.3MB）としてゲームに同梱。元ファイルは `assets-src/soundfont/` | MITライセンス（`assets-src/soundfont/LICENSE-FluidR3.md`）。商用利用・改変・再配布・ゲームへの組み込みは可。**著作権表示と許諾文を配布物に含める条件**あり（`public/licenses/FluidR3-GM-MIT.txt` をゲームに同梱、README にも表記）。同梱のサンプルは、パブリックドメインの素材と作者本人の録音、Ethan Winer 氏・Michael Schorsch 氏の提供分 | 必要（README・ゲーム内クレジットに「Fluid (R3) GM SoundFont © Frank Wen / Mono版 © Michael Cowgill（MIT）」と書く） |
| spessasynth_lib / spessasynth_core（サウンドフォント再生ライブラリ。npm） | https://github.com/spessasus/spessasynth_lib | 2026-09-30 | BGMの再生（`src/audio/sampled-engine.ts`） | Apache-2.0。商用利用・改変・再配布は可。ライセンス文を同梱する条件あり（`public/licenses/spessasynth-Apache-2.0.txt`） | 必要（README に表記） |
| Neural Amp Modeler Core（WASM版 `@opendaw/nam-wasm`。npm） | https://github.com/sdatkinson/NeuralAmpModelerCore （WASM版: https://www.npmjs.com/package/@opendaw/nam-wasm ） | 2026-09-30 | 作曲ソフトのアンプシミュレーター（`src/audio/nam/`）。作曲ソフト（`tools/composer/`）にだけ埋め込み、ゲーム本体には入れない | MITライセンス（© 2023 Steven Atkinson）。商用利用・改変・再配布は可。著作権表示と許諾文を含める条件あり。.namモデルは同梱していない。利用者が読み込むモデルは、モデルごとに配布元の規約（商用利用・再配布）を確認する。ゲームにはモデルを入れない | 必要（README に表記） |
| NAMの見本モデル3つ（NeuralAmpModelerCore の `example_models/` の `A2.nam`・`my_model.nam`・`wavenet.nam`） | https://github.com/sdatkinson/NeuralAmpModelerCore （コミット 0b3d3c9） | 2026-09-30 | 作曲ソフトの同梱アンプ（ハイゲインアンプA・B、ベース用プリアンプ）。元ファイルは `assets-src/nam-models/`。ゲーム本体には入れない | リポジトリ全体が MITライセンス（© 2023 Steven Atkinson）で、`example_models/` に別の規約はない。商用利用・改変・再配布は可。著作権表示と許諾文を含める（`assets-src/nam-models/LICENSE-NeuralAmpModelerCore.txt`、`public/licenses/NeuralAmpModelerCore-MIT.txt`）。モデル内の機材メーカー名は画面に出さない | 必要（README に表記） |
| Electron（デスクトップ版の土台）・Anthropic TypeScript SDK（AI作曲の通信）・Model Context Protocol SDK（コネクタ。開発用） | https://www.electronjs.org/ ・ https://github.com/anthropics/anthropic-sdk-typescript ・ https://github.com/modelcontextprotocol/typescript-sdk | 2026-09-30 | デスクトップ版（`desktop/`）とコネクタ（`tools/mcp/`）。ゲーム本体には入れない | すべて MIT（Electron に同梱の Chromium は、各部品のライセンスが `LICENSES.chromium.html` として配布物に入る）。商用利用・再配布は可。ライセンス文を配布物に含める（`desktop/copy-licenses.mjs` が `licenses/` にそろえる） | 必要（デスクトップ版の「ヘルプ」→「ライセンス」） |
| LAME（lamejs、npm `@breezystack/lamejs` 1.2.7）・文字フォント Orbitron と JetBrains Mono（npm `@fontsource`） | https://lame.sourceforge.net/ ・ https://github.com/shijinyu/lamejs ・ https://fonts.google.com/specimen/Orbitron ・ https://www.jetbrains.com/lp/mono/ | 2026-09-30 | デスクトップ版だけ（MP3 の書き出し・画面の英数字の文字）。ゲーム本体には入れない | LAME: LGPL-3.0。商用可。条件（部品の説明による）: 本体と別ファイルで使う・LAME を使っていることと入手先を示す・改変したら公開する（改変していない）。LGPL/GPL の本文と表示を `licenses/` に同梱。フォント: SIL OFL 1.1（商用・同梱可。フォント単体の販売は不可。ライセンス文を同梱） | 必要（「ヘルプ」→「ライセンス」） |

## 条件つきで使える素材（元の画像はリポジトリに置かない）

| 素材名 | 入手元 | 確認日 | 置き場 | 規約の要点 | クレジット |
|---|---|---|---|---|---|
| ドット絵世界（Pixel Art World）のタイルセット・キャラ素材（ツクール用の表記がないもの） | http://yms.main.jp （規約: https://yms.main.jp/page-s1/terms.html ） | 2026-09-30 | **リポジトリには元の画像を置かない**（公開リポジトリに置くと「そのままの素材を配る」ことになるため）。素材の一覧・URL・判定は `docs/design/yms-dotworld-catalog.md`。**まだゲームには反映していない** | 編集可、商用可、二次配布は禁止。ツクール用の表記がある素材はツクールでの制作専用なので使えない。サンプルマップは使用NG。作者さんへの問い合わせの答え（2026-09-30、旭さん経由）: ツクールの素材以外は使ってよい、商用のゲームとして配るのは「配る」に含まれない、ダメなのは素材をそのままの形で配ること。→ 使うときは作者のサイトから取得し、加工したものだけをゲームに組み込む | **必要**（配布するときはスタッフロールなど1か所に「ドット絵世界 http://yms.main.jp」） |

## モンスター・悪魔・天使・神・神話・聖書の絵（2026-10-01、合計10,253枚）

| 素材 | 置き場 | 規約の要点 | クレジット |
|---|---|---|---|
| ぴぽや「ポップモンスターイラスト素材（Pipoya RPG Monster Pack）」274枚 | `assets-src/monster-illustrations/01-pipoya/`（同梱の説明は `LICENSES/`） | ぴぽや無料素材利用規約: 商用可・加工可・無償の再配布は条件つきで可・素材としての販売は不可 | 不要 |
| OpenGameArt の絵 315枚（115ページ） | `assets-src/monster-illustrations/02-opengameart/` | CC0／CC-BY 3.0・4.0／OGA-BY 3.0（2026-10-01 に全ページを読み直し）。AI・既存ゲーム由来・3D・ドット絵は除外 | CC-BY・OGA-BY の140枚は必要（`assets-src/monster-illustrations/CREDITS.md`） |
| 美術館のパブリックドメイン作品 9,664枚（メトロポリタン 5,680・NGA 1,638・SMK 1,341・クリーブランド 1,005。聖書・神話・悪魔・天使など） | `assets-src/monster-illustrations/03-museum-art/` | 画像は各館が CC0 で公開。昔の作品そのもので、聖書・宗教の主題を含むので、ゲームにそのまま出すかは人間が判断 | 不要 |

**まだゲームには反映していない。** 1枚ずつの入手元は `assets-src/monster-illustrations/manifest.csv`。

## 使わないと決めた素材（2026-10-01、モンスターの絵）

| 素材 | URL | 外した理由 |
|---|---|---|
| 素材屋『氏』のモンスター素材 | https://uzi-material.com/ （規約: https://uzi-material.com/service/ ） | 二次配布禁止（公開リポジトリに置けない）、AI学習等への使用禁止。ゲームでの利用自体は可（自作ゲーム・商用可、課金要素の強いゲームは不可、商用ならなるべく「氏家まさら／素材屋『氏』」と表記）。使うなら、AIで開発しているゲームへの組み込みと公開リポジトリへの配置を作者に確認してから |
| Free 30 Enemy characters pack（cogabushi） | https://cogabushi.itch.io/free-30-enemy-characters-pack | 再配布禁止（加工・トレースしたものも含む）、使えるのはダウンロードした本人だけ、作者がAIで作った画像と明記 |
| シカゴ美術館の画像 | https://www.artic.edu/ | 画像の自動取得に確認画面（Cloudflare）が出たので、回避せずに取得をやめた |

## AIで作った絵（2026-10-03、試作）

| もの | 置き場 | 使ったモデル（ライセンス） | 状態 |
|---|---|---|---|
| ドット絵の試作7体（スライム・ゴースト・ゴーレム・竜の子・コウモリの悪魔・スケルトン騎士・小悪魔） | `assets-src/ai-generated/trial-2026-10-03/` | PublicPrompts/All-In-One-Pixel-Model（CreativeML OpenRAIL-M）＋ latent-consistency/lcm-lora-sdv1-5（openrail++） | **ゲームには入れていない**。入れる前に、既存作品に似ていないかの確認と人間の確認が要る。1体（キノコ）は有名なキャラを連想させたので外した |
| RPGの戦闘の敵らしいドット絵の試作12体（牙オオカミ・よろいトカゲ兵・フードの亡霊・水晶ゴーレム・紫の怪鳥・亡者の王・呪われた騎士・大ダコ・赤衣の魔術師・翼の魔像・黒い大グモ・沼の獣。64×64・16色） | `assets-src/ai-generated/trial-2026-10-03-rpg/` | 同上。背景の切り抜きに rembg（MIT）＋ isnet-general-use（Apache-2.0）を使用 | **ゲームには入れていない**。入れる前に、既存作品に似ていないかの確認と人間の確認が要る。3枚（火のサラマンダー2枚・角のある緑の怪物1枚）は有名なキャラを連想させるおそれがあるので外した |
| `/make-art` の見本（フィールド用キャラ5人・登場人物の全身の絵3人） | `assets-src/ai-generated/2026-10-03-make-art-examples/` | 全身の絵: stable-diffusion-v1-5（CreativeML OpenRAIL-M）＋ LCM-LoRA（openrail++）、切り抜きに rembg（MIT）＋ isnet-general-use（Apache-2.0）。フィールド用キャラは手描きの型に色を当てはめたもの（AIはデザイン画の色の参考だけ） | **ゲームには入れていない**（見本）。名前は仮 |
| 2026-10-04 | 敵の絵（雑魚・ボス、`assets-src/monsters/`。名簿 `tools/pixel-art/ai-gen/monster-roster.json`） | Stable Diffusion 1.5（CreativeML OpenRAIL-M）の下絵 → sfcize.py → 手直し → ドット絵エディタ | 既存作品に似ていないかを1体ずつ目で確認。顔は右向き |

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
| 日本一フリーBGM の曲（約1万2千曲） | https://nihonichi-bgm.com/ （規約: https://nihonichi-bgm.com/terms/ 、2026-09-30 確認） | **学習（音の作りを数値で測る）だけに使い、ゲームには入れない。** 規約上はゲームへの組み込み・商用利用は可、再配布・販売と誹謗中傷を含む利用は禁止。ただし全曲が生成AI（Suno AI）製で、サイト自身が権利の保証をせず、既存曲と似る可能性を認めているため、オリジナル曲の方針（`roles.md` 3-7）と 1-1 から使わない。mp3 はリポジトリに置かない（二次配布になるため）。測った数値と学んだことは `docs/sound/reference-nihonichi-bgm.md` |

## 使わないと決めた素材（2026-09-30、ドット絵ライブラリ2を選ぶときに外したもの・1回目から差し替えたもの）
説明文の全文を読み直して外した主なもの。どれも CC0 だが使わない。

| 素材 | URL | 外した理由 |
|---|---|---|
| Gnomes / Skeletons Rework / Barrels (Mage City Arcanos remix) / Cave Entrance / Mushroom Houses | https://opengameart.org/content/gnomes ほか | 既存のゲーム（Stendhal）のために作られた絵。1回目の500枚から3枚を差し替えた |
| Eye of Sender / Eye of Sender Animated | https://opengameart.org/content/eye-of-sender ほか | 既存のゲームの品物の名前のもじり。1回目から1枚を差し替えた |
| 8bit NES Big Slime Monster / Slime (Radomir Dopieralski) | https://opengameart.org/content/slime-4 ほか | 元の作者でない人が上げた絵を元にしていて、元の規約が確かめられない。1回目から1枚を差し替えた |
| Main art from Monster RPG 2 / Frogatto / The Battle for Wesnoth 関連 / FLARE 用の絵 / Glitch の絵 | https://opengameart.org/content/main-art-from-monster-rpg-2 ほか | 既存のゲームの絵、または既存のゲームのために作られた絵 |
| 50+ Monsters Pack 2D | https://opengameart.org/content/50-monsters-pack-2d | 見た目が有名な作品の生き物に似ている（同じ作者の別のパックに、その作品に似せたと書かれている） |
| Dragon Maniac & Friends | https://opengameart.org/content/dragon-maniac-friends | 竜がディズニーのキャラクターに似ていると作者が書いている |
| Gothicvania 各パック / Crypt of Dracula NES / Tiny Zelder clone / Legend of Faune / TinyRPG Stranger Forest | https://opengameart.org/content/gothicvania-town ほか | 既存の作品に似せた・寄せたと書かれている |
| Animated Bird Characters / Blue Lizard / Christmas Village / Helgi / Wacky EGA portraits / Kica's Enemy Pack / Witchy Bizness | https://opengameart.org/content/animated-bird-characters ほか | 作者の公開済みゲーム・ゲームジャム作品・制作中のゲームで使われた絵 |
| Tasen soldier / Bird-like RPG character / Trolls (Wesnoth 準拠) | https://opengameart.org/content/tasen-soldier-for-rpg-maker-mv ほか | 既存のゲームの種族・絵柄・規格に合わせた絵 |
| 12 Public Domain Boss Sprites / 25 Portrait pixel art pack / Ogre / 4 summoning circles | https://opengameart.org/content/12-public-domain-boss-sprites ほか | 画像変換AI・人物生成AI・3D描画から作った絵、またはドット絵でない |

## 使わないと決めた素材（2026-09-30、参考素材1000点を選ぶときに外したもの）

| 素材 | URL | 外した理由 |
|---|---|---|
| Assets for Tuxemon | https://opengameart.org/content/assets-for-tuxemon | 既存のゲーム（Tuxemon）の絵 |
| CC0 herb icons / Chick / CC0 leggings icons / Explosion animations | https://opengameart.org/content/cc0-herb-icons ほか | 既存のゲーム（Stendhal・FLARE・Frogatto）のための絵、またはそこから取った絵 |
| 16x16 echinoderms / Chain insect / Jump and run tileset 24x24 | https://opengameart.org/content/16x16-echinoderms ほか | Minecraft 用に作った絵、または Minecraft に似せた絵 |
| Brackeys game jam pack / Gude Jump n Run / Pink Knight / Horde Corp ほか | https://opengameart.org/content/brackeys-game-jam-20221-pack ほか | 公開済みゲーム・ゲームジャム作品・既存作品に着想を得たと書かれたゲームの絵 |
| Slime (slime-4) | https://opengameart.org/content/slime-4 | 元の作者でない人が上げた絵で、元の規約が確かめられない |
| Procedural sword/potion icons / Planet surface skyboxes | https://opengameart.org/content/procedural-sword-icons ほか | 手で描いた絵ではなく、プログラムで生成した絵 |

## ドット絵の練習で見た参考素材（2026-10-03）
練習（模写・なぞり）で見た絵は、すべて `assets-src/pixel-reference/` の無料素材（CC0・ぴぽや）。**練習の成果（`assets-src/pixel-practice/` の模写・なぞり）はゲームに入れていない**。ゲームに入れた雑魚の敵8体（`tools/pixel-art/mobs.mjs`）は一から描いた自作で、参考素材の絵は写していない。
| GeneralUser GS 2.0.3（`GeneralUser-GS.sf2`、約32MB。作曲ソフト用の音源の候補） | https://github.com/mrbumpy409/generaluser-gs （作者: S. Christian Collins、https://www.schristiancollins.com/generaluser） | 2026-10-07 | 作曲ソフトの録音音源の聴き比べ用。`assets-src/soundfont/` に置いた。作曲ソフトに2つとも埋め込み、画面の「録音音源」で切りかえて使う（書き出しは `node tools/composer/song.mjs build … --wav --soundfont gu`）。**ゲーム（`game.sf3`）には入れていない**（作曲ソフトの画面でだけ選べる） | 独自の許諾（`assets-src/soundfont/LICENSE-GeneralUserGS.txt`）。商用の音楽制作・ソフトへの組み込み・改変・再配布は可。ただし作者自身が「含まれるサンプルの出どころを100%は保証できない（市販のサウンドフォントやサンプルCDからのものはない）」と書いている。**ゲームに入れて配布するなら、このリスクを人間（旭さん）が了承してから** | 不要（入れるなら感謝の表記が望ましい） |
| VSCO 2 Community Edition（Versilian Studios。オーケストラ。作曲ソフト用の音源 `orchestra.sf3`） | https://versilian-studios.com/vsco-community/ （GitHub: sgossner/VSCO-2-CE、LICENSE 確認 2026-10-13） | 2026-10-13 | 伸ばす音（弦の独奏・合奏、ホルン・トランペット・トロンボーン・チューバ、フルート・オーボエ・クラリネット・ファゴット・ピッコロ、オルガン）と、ハープ・ティンパニ・マリンバ・グロッケンの録音を、`tools/soundfont/build-orchestra.mjs` で選んで SoundFont に変換（約18MB。元の約870MBは `assets-src` に入れない。環境変数 VSCO で場所を渡す）。作曲ソフト専用で、ゲーム本体（`game.sf3`）には入れていない | CC0（商用・加工・再配布 可）。クレジットは求められているが義務ではない | 任せる（README に「VSCO 2 Community Edition by Versilian Studios」と記載） |
| Salamander Grand Piano V3（作曲ソフト用のピアノ音源 `piano-salamander.sf3`） | https://github.com/sfzinstruments/SalamanderGrandPiano （作者: Alexander Holm。LICENSE 確認 2026-10-13） | 2026-10-13 | 全88鍵のうち3半音ごとの録音を、強さ6（弱）・13（強）の2層だけ使い、モノラル・約7秒に切って変換（約3.4MB）。作曲ソフト専用で、ゲーム本体には入れていない | CC BY 3.0（商用・改変可）。**作者 Alexander Holm のクレジット表記が必要** | **必要** |
| FreePats「Clean Electric Bass YR」（指弾き・ピック弾き。作曲ソフト用のベース音源） | https://freepats.zenvoid.org/ElectricGuitar/clean-electric-bass.html （GitHub: freepats/electric-bass-YR。録音: Andrea Biasior、Yamaha RBX） | 2026-10-07 | 元のSFZを `tools/soundfont/build-bass.mjs` で小さなSF3（約0.6MB。2026-10-08に鍵域を21〜84へ拡張し、A2より上の音も鳴るよう直した）に変換し、GMのエレキベース（33・34）を入れかえる。元は `assets-src/soundfont/extra/src/electric-bass-yr/`、変換後は `assets-src/soundfont/extra/bass-*.sf3`。作曲ソフトの画面「ベース音源」で選ぶ。**ゲームには入れていない** | CC0 1.0（パブリックドメイン）。商用・改変・再配布・ゲームへの組み込みは可。表記は不要 | 不要 |
| Muldjord Kit（生ドラム。作曲ソフト用のドラム音源） | https://github.com/sfzinstruments/DrumGizmo.MuldjordKit （原典: Lars Muldjord / DrumGizmo、SFZ化: sfzinstruments） | 2026-10-07 | 16本のマイク録音を `tools/soundfont/build-drums.mjs` で「近接マイク＋オーバーヘッド＋部屋」のステレオにまぜ、強さ4〜5層・必要な長さだけ切り出して、SF3（約3.1MB）にした。GMドラムの 0・8・16・32 のキットで、鳴らすキーだけ入れかえる。設定ファイルは `assets-src/soundfont/extra/src/muldjord/Data/`、録音（約340MB）はgitに入れず、変換結果は `assets-src/soundfont/extra/drums-muldjord.sf3`。作曲ソフトの画面「ドラム音源」で選ぶ。**ゲームには入れていない** | CC BY 4.0（`assets-src/soundfont/extra/src/muldjord/LICENSE`）。商用・改変・再配布は可。**作者 Lars Muldjord のクレジット表記が必要**（加工したことも書く）。ゲームに入れるときは、ゲーム内クレジットと README に「Muldjord Kit © Lars Muldjord (CC BY 4.0)。ミックス・切り出しの加工あり」と書くこと | 必要（ゲームに入れる場合） |
| 使わない: Meatbass（Karoryfer、ウッドベース） | https://www.kvraudio.com/product/meatbass-by-karoryfer/details | 2026-10-07 | GPL 3 のため、ゲームに入れる素材としては避ける | — | — |
| Sneakybass（Karoryfer、ウッドベース。作曲ソフトの「ジャズ」ベース） | https://github.com/sfzinstruments/karoryfer.sneakybass | 2026-10-07 | リポジトリのライセンス表記が CC0 と確認できたので、`tools/soundfont/build-bass.mjs jazz` でSF3（約1.2MB）にした。`assets-src/soundfont/extra/bass-jazz.sf3`。**ゲームには入れていない** | CC0（クレジット不要） | 不要 |
| Black And Green Guitars（Karoryfer Samples。Gretsch Anniversary〔緑〕と Hofner Club〔黒〕の生ギター。作曲ソフトの「ギター音源」） | https://github.com/sfzinstruments/karoryfer.black-and-green-guitars （コミット b3b3249） | 2026-10-11 | リポジトリの LICENSE が CC0 1.0、readme に「Royalty-free for all commercial and non-commercial use」と確認できたので、`tools/soundfont/build-guitar.mjs` で twang の録音（ラウンドロビン1番目・強さ3段・mono・Vorbis圧縮）を SF3（Gretsch 5.6MB・Hofner 3.7MB）にした。GMのジャズギター(26)・クリーンギター(27)を入れかえる。`assets-src/soundfont/extra/guitar-gretsch.sf3`・`guitar-hofner.sf3`。ライセンス文と readme の写しも同じ場所。**ゲームには入れていない** | CC0（クレジット不要。録音・写真は Brian Wood） | 不要 |
| Virtuosity Drums（ジャズ用の生ドラム。作曲ソフトの「ジャズ」ドラム） | https://github.com/sfzinstruments/virtuosity_drums | 2026-10-07 | CC0。`tools/soundfont/build-drums-jazz.mjs` でマイクをまぜ、SF3（約2.9MB）にした。`assets-src/soundfont/extra/drums-jazz.sf3`。**ゲームには入れていない** | CC0（クレジット不要） | 不要 |
| ジャンル別のベース・ドラム（ロック／メタル／J-POP） | 上の FreePats ベース（ピック・指弾き）と Muldjord Kit | 2026-10-07 | 同じ録音に、音量バランスとEQを変えただけのもの（`build-bass.mjs`・`build-drums.mjs` の PROFILES）。`bass-rock/metal/jpop.sf3`、`drums-rock/metal/jpop.sf3` | ベースは CC0。ドラムは Muldjord Kit と同じ CC BY 4.0 | ドラムは必要（ゲームに入れる場合） |
| ドラム「スープラ」（乾いた金属スネア寄せ。作曲ソフトの「ドラム音源」） | 上の Muldjord Kit | 2026-10-08 | 同じ録音に、スネアだけ別のEQ（400Hz付近を引き、5.5kHzを持ち上げ）・短い余韻・部屋の鳴りを減らす設定をかけたもの（`build-drums.mjs` の PROFILES の supra）。`drums-supra.sf3`（約2.6MB）。特定の実機の録音ではなく、あくまで音色を寄せた近似。**ゲームには入れていない** | Muldjord Kit と同じ CC BY 4.0 | 必要（ゲームに入れる場合） |
| タム（ロートタム・キャノンタム・インチ違い。作曲ソフトの「オーケストラ音源」の GM 117〜119） | 上の Muldjord Kit の録音のタム（Tom1〜4） | 2026-10-13 | `tools/soundfont/toms-real.mjs`。録音を音程の測定→鍵盤の高さに合わせて音程をずらし、キャノン＝余韻短縮・高域を丸め、ロート＝打った直後の音程の動きを加えた。`orchestra.sf3` に収録。**ゲームには入れていない** | Muldjord Kit と同じ CC BY 4.0 | 必要（ゲームに入れる場合） |
| バスドラのトリガー・インパクト（`orchestra.sf3` の GM 120・121） | 計算で作った音（`tools/soundfont/toms-synth.mjs`。録音素材なし） | 2026-10-13 | 素材の権利なし | 自作 | 不要 |
| 使わない: Salamander Drumkit（CC BY-SA 3.0）、Big Rusty Drums（CC0、2.3GB） | https://github.com/endolith/Salamander-Drumkit | 2026-10-07 | 前者は改変したサンプルを同じ条件（SA）で公開する義務があり、扱いにくい。後者は容量が大きく、クセの強い古い機材のため見送り | — | — |



## シンセ音色の音源（作曲ソフト専用）
- `assets-src/soundfont/extra/synths.sf3`: FluidR3（MIT。記録済み）から、シンセ系の音色（GM 38・39・50・51・80〜103の一部）だけを切り出したもの。作曲ソフトの書き出しだけで使い、ゲームには入れていない。

## 使わないと決めた素材（2026-10-11、アンプシミュレーターのモデル）

| 素材 | URL | 外した理由 |
|---|---|---|
| TONE3000 のアンプ・ペダルのキャプチャ（`.nam`）の多く（ライセンス表記「T3K」） | https://www.tone3000.com/ | 「再アップロード・再配布は作者の許可が必要」。作曲ソフトに埋め込んで配る形になるので使えない。ダウンロードにもログインが必要な可能性が高い（アカウント作成は人間の判断） |
| pelennor2170/NAM_models（コミュニティのキャプチャ集） | https://github.com/pelennor2170/NAM_models | ライセンスが GNU GPL v3。作曲ソフトへの埋め込みは、ソフト全体への GPL の適用が必要になるおそれがあるので、人間の判断を待つ（今は使わない） |

## 作曲ソフト用の追加音源（2026-10-14、Suno との差を調べたときに足したもの。作曲ソフト専用で、ゲーム本体 `dist/` には入れていない）
調べと変換の詳細は `docs/sound/band-ensemble/suno-gap-and-sources.md`。変換後の SF3 は `assets-src/soundfont/extra/`、規約の本文・README の写しは `assets-src/soundfont/extra/src/licenses/`。**どれも耳での確認は未実施（数値で無音でないこと・音程のみ確認）。**

| 素材 | URL | 入手日 | 使い方 | 規約 | クレジット |
|---|---|---|---|---|---|
| FSBS Electric Guitar（Fender 基本機種の直接録音。direct・clean bridge small・jazz bridge small） | https://freepats.zenvoid.org/ElectricGuitar/clean-electric-guitar.html | 2026-10-14 | `tools/soundfont/build-fsbs.mjs` で SF3 に変換。`guitar-fsbs-direct.sf3`・`guitar-fsbs-clean-small.sf3`・`guitar-fsbs-jazz-small.sf3`（GM 27・27・26 を入れかえる）。direct はアンプ（NAM）に通す前提 | CC0 1.0（各版の README とライセンス文で確認） | 不要 |
| FSBS Electric Guitar の歪み版（dist2） | 同上 | 2026-10-14 | `guitar-fsbs-dist2.sf3`（GM 30）。禁止音（「みんなで」の曲の歪みギター）には使わない | 同じシリーズが CC0。この版の README の写しは保存できていない（元の入手元で再確認すること） | 不要 |
| Emilyguitar（Karoryfer Samples、D. Smolken。Epiphone Emily the Strange の直接録音） | https://github.com/sfzinstruments/karoryfer.emilyguitar | 2026-10-14 | `tools/soundfont/sfz-to-sf3.mjs` で `guitar-emily.sf3`（GM 27） | CC0 1.0（LICENSE 本文を確認） | 不要 |
| Shinyguitar（Karoryfer Samples、D. Smolken。アーチトップの電気ギター。ピックアップ録音〔electric_one〕を使用。4層×ラウンドロビン） | https://github.com/sfzinstruments/karoryfer.shinyguitar | 2026-10-15 | `tools/soundfont/sfz-to-sf3.mjs`（--rr 2 --q 6）で `guitar-shiny.sf3`（GM 27）。作曲ソフトの `--guitar shiny`。マイク録音〔acoustic_one〕は `guitar-shiny-acoustic.sf3`（`--guitar shiny-acoustic`。アコギ代わり。2026-10-15） | CC0 1.0（LICENSE 本文を確認。readme に「royalty-free for all commercial and non-commercial use」。写しは `assets-src/soundfont/extra/LICENSE-karoryfer-shinyguitar-CC0.txt`） | 不要 |
| David Fau Casquel's Impulse Responses（ギターのキャビネット／アンプのインパルス応答6つ。作者本人が作成） | https://archive.org/details/ImpulseResponses （musical-artifacts.com/artifacts/156） | 2026-10-15 | 元ファイルは `assets-src/ir/david-fau-casquel/`。`tools/soundfont/build-cab-irs.py` で約93ミリ秒に切って `tools/composer/cab-irs.ts`（作曲ソフト専用。ゲーム本体には入れない）。fx の `{"type":"cabir","ir":"dfc-bestplugins"}` などで使う | CC BY 3.0（archive.org の licenseurl で確認） | **必要**: 「Impulse Responses by David Fau Casquel (CC BY 3.0)」。この IR を通した曲をゲームに入れるときは、ゲーム内クレジット（または README）に書く |
| 使わない: Bestplugins AMPS IR Pack 2 ほか同作者の「バンド名・アンプ名」のIR集 | https://archive.org/details/BestpluginsAmpsIRPack2 | 2026-10-15 | 規約は CC BY 3.0 だが、有名アンプ・バンドの音に寄せたもので、他人の録音から作った可能性があり出どころが不明確なため使わない | — | — |
| Growlybass（Karoryfer Samples。Squier Jazz Bass） | https://github.com/sfzinstruments/karoryfer.growlybass | 2026-10-14 | `sfz-to-sf3.mjs --shift -12` で `bass-growly.sf3`（GM 33） | CC0 1.0（LICENSE 本文を確認） | 不要 |
| VSCO 2 Community Edition の独奏コントラバス・ピチカート（Versilian Studios） | https://github.com/sgossner/VSCO-2-CE （Strings/Solo Contrabass/Pizz） | 2026-10-20 | 出だしの大きさをそろえた SFZ（`assets-src/soundfont/src/upright-vsco/upright.sfz`）から `sfz-to-sf3.mjs --program 33` で `bass-upright.sf3`（作曲ソフトの `--bass upright`＝ウッドベース） | CC0 1.0（LICENSE 本文を確認） | 不要 |
| VCSL（Versilian Community Sample Library）の小物打楽器（クラップ、タンバリン、カウベル、アゴゴ、カバサ、ギロ、クラベス、ウッドブロック、トライアングル、シェイカー、スレイベル、ベルツリー） | https://github.com/sgossner/VCSL | 2026-10-14 | `tools/soundfont/build-aux-percussion.mjs` で既存のドラム SF3 に足し、`drums-{rock,muldjord,jpop,metal,jazz,supra}-aux.sf3` にした | CC0 1.0（LICENSE を確認） | 不要（任意） |
| FreePats World Percussion（ボンゴ、コンガ、マラカス、カスタネット） | https://freepats.zenvoid.org/ | 2026-10-14 | 同上（`drums-*-aux.sf3` に組み込み） | CC0（LICENSE.txt を確認）。付属の picture.jpg だけ CC BY 4.0 だが使っていない | 不要 |
| Greg Sullivan E-Pianos（Wurlitzer EP200、Yamaha CP80、Hohner Pianet T。マッピング: kinwie） | https://github.com/sfzinstruments/GregSullivan.E-Pianos （作者: http://www.sullivang.net/） | 2026-10-14 | `sfz-to-sf3.mjs` で `epiano-wurlitzer-ep200.sf3`・`epiano-cp80.sf3`・`epiano-pianet-t.sf3` | **CC BY 3.0**（LICENSE 本文を確認。作者がクレジットを求めている） | **必要（ゲームに入れる場合）。案: 「Electric piano samples by Greg Sullivan (CC BY 3.0)」** |
| FreePats Upright piano KW（Kawai アップライト。small と bright） | http://freepats.zenvoid.org/Piano/acoustic-grand-piano.html#UprightKW | 2026-10-14 | `tools/soundfont/sf2-to-sf3.mjs` で `piano-upright-kw.sf3`・`piano-upright-kw-bright.sf3` | CC0（cc0.txt を確認） | 不要 |
| FreePats Spanish classical guitar（ナイロン弦） | http://freepats.zenvoid.org/Guitar/acoustic-guitar.html | 2026-10-14 | `guitar-nylon-spanish.sf3`（GM 24） | CC0（cc0.txt を確認） | 不要 |
| FreePats Drawbar / Percussive / Rock / Church organ emulation（setBfree・Aeolus の録音） | http://freepats.zenvoid.org/Organ/ | 2026-10-14 | `organ-drawbar.sf3`・`organ-percussive.sf3`・`organ-rock.sf3`・`organ-church.sf3`（GM 16〜19） | CC0（README に明記）。GPL のソフトで鳴らした録音だが、音そのものには及ばないという一般的な理解。法的な最終判断は人間 | 不要 |
| FreePats Synth pads（New age、Sweep、Bowed、Choir。ZynAddSubFX / Yoshimi で作成） | http://freepats.zenvoid.org/ | 2026-10-14 | `synth-pad-newage.sf3`（GM 88）・`synth-pad-choir.sf3`（91）・`synth-pad-bowed.sf3`（92）・`synth-pad-sweep.sf3`（95） | CC0（README に明記）。上のオルガンと同じ注意 | 不要 |
| FreePats Synth Lead（Square・Calliope・Fifths・Bass & Lead）。Zyn/Yoshimi・Hexter・Surge で作成（作者: Roberto、快乐爱的小精灵） | https://freepats.zenvoid.org/Synthesizer/synth-lead.html | 2026-10-14 | `tools/soundfont/sf2-to-sf3.mjs` で `synth-lead-square.sf3`（GM 80）・`synth-lead-calliope.sf3`（82）・`synth-lead-fifths.sf3`（86）・`synth-lead-bass.sf3`（87） | CC0（各 README に明記。写しは `src/licenses/README-freepats-synth-lead-*.txt`） | 不要 |
| FreePats Synth Bass（Synth Bass 1・Synth Bass 2＝DX7 BASS 1・Lately Bass＝TX81Z） / Synth Brass（Brass 1・Brass 2＝DX7 BRASS 7） / Synth Strings（1・2） | https://freepats.zenvoid.org/Synthesizer/ （synth-bass.html・synth-brass.html・synth-strings.html） | 2026-10-14 | `sf2-to-sf3.mjs` で `synth-bass-zyn.sf3`・`synth-bass-lately.sf3`（GM 38）、`synth-bass-dx7.sf3`（39）、`synth-brass-zyn.sf3`（62）、`synth-brass-dx7.sf3`（63）、`synth-strings-1.sf3`（50）、`synth-strings-2.sf3`（51） | CC0（各 README に明記。DX7 の音は Hexter／Dexed という自由ソフトで鳴らした録音） | 不要 |
| FreePats FM Piano 1・FM Piano 2（DX7 の電子ピアノ風。Hexter の録音） | https://freepats.zenvoid.org/ElectricPiano/synthesized-piano.html | 2026-10-14 | `sf2-to-sf3.mjs --first-only` で `epiano-fm-dx7.sf3`・`epiano-fm-bright.sf3`（GM 4） | CC0（README に明記） | 不要 |
| FreePats Piano FB（Francis Bacon の自動演奏ピアノ。ホンキートンク。small 版） | https://freepats.zenvoid.org/Piano/honky-tonk-piano.html | 2026-10-14 | `sf2-to-sf3.mjs` で `piano-honkytonk.sf3`（GM 3） | CC0（README に明記） | 不要 |
| FreePats Button Accordion HN（Hohner。録音: Jeff Stauffer、整形: michael02022） | https://freepats.zenvoid.org/Organ/accordion.html | 2026-10-14 | `sfz-to-sf3.mjs --loop` で `accordion-hohner.sf3`（GM 21）。リリース用の録音は読み捨て、ループの終点をファイル末尾の手前に直した SFZ（作業用）から変換 | CC0（README・LICENSE に明記） | 不要 |
| FreePats Glass（水のグラスを叩いた録音。Roberto） | https://freepats.zenvoid.org/ChromaticPercussion/glass.html | 2026-10-14 | `sf2-to-sf3.mjs` で `glass-water.sf3`（GM 8。セレスタの代わり。範囲は A4〜G6 だけ） | CC0（readme・cc0.txt を確認） | 不要 |
| **FreePats YDP Grand Piano（Zenph Studios の Yamaha Disklavier Pro の録音を元に Roberto が SoundFont 化）** | https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html （YDP-GrandPiano-SF2-20160804） | 2026-10-14 | `sf2-to-sf3.mjs --q 3 --first-only` で `piano-ydp-grand.sf3`（GM 0。9.96MB） | **CC BY 3.0**（同梱 txt の本文を確認: 元の「Zenph Studios Yamaha Disklavier Pro Piano Multisamples for OLPC」は CC BY、FreePats の加工も CC BY 3.0） | **必要（ゲームに入れる場合）。案: 「Grand piano samples: Zenph Studios (Yamaha Disklavier Pro, OLPC sound library) / SoundFont by Roberto, FreePats (CC BY 3.0)」** |
| VCSL（Versilian Community Sample Library）の TX81Z（Clavisynth・FM Piano・Piano 1）。ヤマハ TX81Z 実機の FM 音を Samplit で録音 | https://github.com/sgossner/VCSL | 2026-10-14 | WAV から作った SFZ を `sfz-to-sf3.mjs` で `keys-clavi-tx81z.sf3`（GM 7）・`epiano-tx81z-fm.sf3`・`epiano-tx81z-piano1.sf3`（GM 4）。ファイル名の音名がオクターブずれているため、実測（倍音検査）で +24 / 0 / +12 のずれを直してある | CC0 1.0（リポジトリの LICENSE 本文を確認） | 不要（任意で感謝） |
| VCSL のグロッケンシュピール・ビブラフォン（ハードマレット）・マリンバ・シロフォン（ミディアム）・ハンドチャイム・チェンバロ（フランス型 Harpsi2、イタリア型 Harpsichord_stop1） | https://github.com/sgossner/VCSL | 2026-10-14 | 同上で `glockenspiel-vcsl.sf3`（GM 9）・`vibraphone-vcsl.sf3`（11）・`marimba-vcsl.sf3`（12）・`xylophone-vcsl.sf3`（13）・`chimes-vcsl.sf3`（8）・`harpsichord-french.sf3`・`harpsichord-italian.sf3`（6）。VCSL の音名は 1 オクターブ低く書かれていたため、実測で +12 している。マリンバは録音レベルが低い（-15〜-68dB）ので、サンプルごとに音量をそろえた | CC0 1.0（同上） | 不要（任意で感謝） |
| VCSL のテナーサックス（Non-Vibrato）・カリンバ（Tanzania）・カホン | https://github.com/sgossner/VCSL | 2026-10-19 | `gen-vcsl-sfz.py`／手書きの SFZ（`assets-src/soundfont/src/cajon-vcsl/cajon.sfz`）を `sfz-to-sf3.mjs` で `sax-tenor-vcsl.sf3`（GM 66）・`kalimba-vcsl.sf3`（GM 108）・`cajon-vcsl.sf3`（GM 115。C3 付近＝低音・D3＝トーン・E3〜＝スラップ、強さ3層×2回ずつ）。作曲ソフト専用（ゲーム本体には入れない） | CC0 1.0（リポジトリの LICENSE 本文を確認） | 不要（任意で感謝） |
| **自作のシンセ音（アナログ風）**: ソーリード・スーパーソー・アルペジオ向けの短い音・ジュピター系ポリシンセ・シンセブラス・ストリングスマシン・ムーグ系ベース・アシッドベース | 外部の素材なし。`tools/soundfont/build-analog-synths.mjs` が、ソー波・パルス波（polyBLEP）→ ラダーフィルター → アンサンブルコーラスで合成 | 2026-10-14 | `synth-lead-saw.sf3`・`synth-lead-supersaw.sf3`・`synth-lead-arp.sf3`（GM 81）、`synth-poly-analog.sf3`（90）、`synth-brass-analog.sf3`（62）、`synth-strings-machine.sf3`（50）、`synth-bass-moog.sf3`（38）、`synth-bass-acid.sf3`（39） | 外部の著作物を含まない（このプロジェクトで書いたプログラムが作った波形）。実在のシンセの録音・プリセット・サンプルは使っていない | 不要 |

## 作曲ソフト用の追加素材（2026-10-20、人間「現代のロック・ラウドロックに必要なものを全部やって」「ジャズ、ケルト音楽、電子音楽、テクノポップ、ダンスミュージック、ボカロ向けの音源も追加して」。作曲ソフト専用で、ゲーム本体 `dist/` には入れていない）
規約は配布元のページと同梱のライセンス文で確認した。変換後の SF3 は `assets-src/soundfont/extra/`、IR は `assets-src/ir/`、NAM は `assets-src/nam-models/`。

| 素材 | URL | 入手日 | 使い方 | 規約 | クレジット |
|---|---|---|---|---|---|
| Dark Days のハイゲインアンプの NAM（トランジスタアンプ・ゲイン最大。アンプのみの `DI.nam`） | https://darkdays.net （直接配布の zip） | 2026-10-20 | `assets-src/nam-models/darkdays-ss-highgain-di.nam`。AIソングの amp `namDD`（キャビネットIRを通す前提）。画面では機材名を出さない | CC BY 4.0（同梱の LICENSE.txt。商用・改変・再配布可。作者名とリンク、変更したことの表示が条件） | **必要**: 「Amp capture by Dark Days — https://darkdays.net (CC BY 4.0)」。この NAM で書き出した曲を公開するときは、概要欄・ゲーム内クレジットに書く |
| マーシャルの中くらいの歪みの NAM（この作曲ソフトで学習。`assets-src/nam-models/marshall-jvm-g4.nam`、amp `namJVM`） | 学習データ: Marshall JVM 410H Dataset（Š. Miklánek, A. Wright, V. Välimäki, J. Schimmel）https://zenodo.org/records/7970723 （doi:10.5281/zenodo.7970723） | 2026-10-21 | OD1 チャンネル・ゲイン4・ベース/ミドル/トレブル5 の入力と出力（スピーカー出力をロードボックスで録ったもの＝アンプだけ）を 48kHz にして、neural-amp-modeler 0.13（MIT）で学習（WaveNet、30周目、検証の誤差 ESR 0.050）。キャビネットIR を通す前提 | データは CC BY 4.0（Zenodo の記録）。学習したモデルは改変物として同じく表記する | **必要**: 「Amp model trained on the Marshall JVM 410H Dataset by Š. Miklánek, A. Wright, V. Välimäki, J. Schimmel (CC BY 4.0), doi:10.5281/zenodo.7970723」。**注意**: データの入力のギター演奏は IDMT のデータセット（CC BY-NC-ND 4.0）から取られている（論文に記載）。モデルに元の演奏そのものは入らないが、権利の扱いは灰色。人間の判断（2026-10-21「使うかは使ってみて判断する」）で試用中 |
| Dark Days のキャビネットIR（2x12・V30。cap/cone/edge・ミックス3種のうち7つ） | 同上 | 2026-10-20 | `assets-src/ir/darkdays/` → `tools/composer/cab-irs.ts`（名前 `dd-v30-2x12-…`） | CC BY 4.0（同梱の LICENSE.txt） | **必要**: 「Cabinet IRs by Dark Days — https://darkdays.net (CC BY 4.0)」 |
| Jester's Brutal Pack 1.0・Emerald Pack 1.0（4x12 のキャビネットIR。作者 Bastian Karschewski が自分で録音） | https://www.jester-dyne-productions.com/brutal-ir-pack/ ・ https://www.jester-dyne-productions.com/emerald-ir-pack/ | 2026-10-20 | `assets-src/ir/jester-dyne/`（元の名前は下品なものがあるので `brutal-4x12-01〜15`・`greenback-4x12-01〜06` に付け直した）→ `cab-irs.ts`（名前 `jd-…`） | CC0（同梱の手引き PDF「LICENSED 2022 UNDER: CC0」） | 不要 |
| Weresax（Karoryfer。アルトサックス） | https://github.com/sfzinstruments/karoryfer.weresax | 2026-10-20 | `sax-alto-weresax.sf3`（GM 65、patch `altoSax`） | CC0 1.0（LICENSE） | 不要 |
| Bear Sax（Karoryfer。1926年のバリトンサックス） | https://github.com/sfzinstruments/karoryfer.bear-sax | 2026-10-20 | `sax-bari-bear.sf3`（GM 67、patch `bariSax`。抜けていた C4 は B3 の録音で埋めた） | CC0 1.0（LICENSE） | 不要 |
| D. Smolken's double bass（1958年 Otto Rubner のコントラバスのピチカート） | https://github.com/sfzinstruments/dsmolken.double-bass | 2026-10-20 | `bass-upright-rubner.sf3`（GM 33。書き出しの `--bass rubner`）。雑音の録音は除いた | CC0 1.0（LICENSE、readme「Royalty-free for all commercial and non-commercial use」） | 不要 |
| VSCO 2 CE のトランペット（ハーマンミュート） | https://github.com/sgossner/VSCO-2-CE | 2026-10-20 | `trumpet-harmon-vsco.sf3`（GM 59、patch `mutedTrumpet`） | CC0（既存の VSCO 2 CE と同じ） | 不要 |
| VCSL の Folk Harp・Baroque Soprano Recorder・Frame Drum | https://github.com/sgossner/VCSL | 2026-10-20 | `harp-folk-vcsl.sf3`（GM 111、`folkHarp`）・`whistle-recorder-vcsl.sf3`（GM 78、`tinWhistle`。ティンホイッスルの代わり）・`framedrum-vcsl.sf3`（GM 116、`frameDrum`。バウロンの代わり） | CC0 1.0（LICENSE） | 不要 |
| FreePats Bagpipe（2026-08-06版。G のバグパイプの録音とドローン） | https://freepats.zenvoid.org/Ethnic/bagpipe.html | 2026-10-20 | `bagpipe-freepats.sf3`（GM 109。instrument `bagpipe` を使う曲で重なる） | CC0（README・LICENSE.txt） | 不要 |
| FreePats Synthesizer Percussion（2022-07-18版。アナログのドラムマシン風の音を Yoshimi・Geonkick で作ったもの） | https://freepats.zenvoid.org/Percussion/electric-percussion.html | 2026-10-20 | `drums-electro.sf3`（ドラムのバンク 128。書き出しの `--drums electro`）。GM の鍵盤に並べ直し、ダンス向けのキック（36）はこのソフトで合成した音 | CC0（readme・LICENSE） | 不要 |
| このソフトで合成した音（外部の録音なし） | `tools/soundfont/build-analog-synths.mjs`・効果音は Python で合成 | 2026-10-20 | `synth-pluck-edm.sf3`（GM 85、`pluckSynth`）・`synth-chip-pulse25/12.sf3`（GM 124・125）・`synth-bass-reese.sf3`（GM 34、`reeseBass`）・`fx-electro.sf3`（GM 126、`fxRiser`。ライザー・ダウンリフター・逆再生シンバル・サブドロップ・シュッ） | 自作（CC0 扱い） | 不要 |

### 使わないと決めた素材（2026-10-20）
| 素材 | URL | 理由 |
|---|---|---|
| Kay 703 NAM Profiles（以前 `kay703-g3〜g10.nam` として同梱） | https://www.tone3000.com/tones/kay-703-6302 | ページの表記は CC0 だが、TONE3000 の利用規約（2025-03-12 発効、https://www.tone3000.com/terms ）が「サイトから入手したトーンの再配布」と「作者と TONE3000 の書面の許可のない商用配布」を禁じている。人間の判断（2026-10-20「他の物で代用しましょう」）で外した。`namKay3〜10` は blues・crunch・lead・loudrock に置きかえ |
| TONE3000 のほかの CC0／CC BY のキャプチャ | https://www.tone3000.com/ | 同じ利用規約のため。使うなら作者の別の配布元か書面の許可が必要 |
| Origin Effects・Celestion・OwnHammer・God's Cab ほかの市販系キャビネットIR | 各社 | 改変・再配布の禁止、有料、または規約が読めない |
| CrocellKit・Aasimonster（DrumGizmo。メタル向けドラム、CC BY 4.0） | https://drumgizmo.org/ | 使えるが、数GB と大きく、今回は見送り（候補） |
| Cowsynth・Caveman Cosmonaut（Karoryfer、CC0） | https://github.com/sfzinstruments | 使えるが、プラックやシンセらしさは SFZ のフィルター・エンベロープ頼みで、録音だけを SF3 にするとバグパイプやオルガンの持続音になるため見送り。プラックは自作の合成にした |
| smpldsnds/supersaw・Hydrogen のドラムキット・FreePats の古い SF2 | GitHub ほか | GPL（作曲ソフト全体に影響するおそれ） |
| Michael Fischer の TR-808 サンプルほか「無料」とだけあるドラムマシンの音 | — | 再配布の許可が書かれていない |

## 使わないと決めた素材（2026-10-14、音源の調査で外したもの）

| 素材 | URL | 外した理由 |
|---|---|---|
| Voxengo の無料インパルス応答 | https://www.voxengo.com/impulses/ | 「売ったり、配布で直接・間接の利益を得てはならない」とあり、ゲームでの扱いが排除できない |
| EchoThief / MIT IR Survey / OpenAIR | https://www.echothief.com/ ・ https://mcdermottlab.mit.edu/Reverb/IR_Survey.html ・ https://www.openair.hosted.york.ac.uk/ | 読めたページに規約の記載がない（OpenAIR は応答が空）。規約が読めない素材は使わない |
| Rickenbacker 4001（Project 16） / jRhodes3c・jRhodes3d / MF Tin Whistle | https://sfzinstruments.github.io/ | 非商用（CC BY-NC 系） |
| Kay 5-String Banjo | https://sfzinstruments.github.io/ | GPL-3.0-or-later |
| Sonatina Symphonic Orchestra / G-Town Church Sampling Project | https://sfzinstruments.github.io/ | CC Sampling Plus 1.0（宣伝・広告目的の利用を禁じる条項があり、ゲームでの扱いが不明） |
| Sam's Sonor / LivingRoom Upright Micro / BJDNielPercussions | https://sfzinstruments.github.io/ | CC BY-SA 4.0（ShareAlike の扱いがむずかしい） |
| Unreal Instruments の各種 / Standard Bass / Estate Grand LE / Piano in 162 / Church Steinway / Maestro Concert Grand / Terkelsen's Marimba ほか、規約が Custom または空欄のもの | https://sfzinstruments.github.io/ | 規約の本文を読めていない |
| Karoryfer の有料品（Baconwulf、Beefowulf ほか） / SFZ 一覧で Commercial のもの | https://sfzinstruments.github.io/ | 有料（人間の承認が必要） |
| Meatbass（Karoryfer） | https://shop.karoryfer.com/pages/free-meatbass | **記録のくいちがい**: 上の記録（2026-10-07）は GPL 3、SFZ 一覧は CC0-1.0。LICENSE を直接読んで確かめるまで使わない |
| Sforzatron（Plogue。Taijiguy の無料メロトロン） | https://sfzinstruments.github.io/keyboards/sforzatron/ | SFZ 一覧のライセンス欄が空で、配布元の規約も確かめられていない（2026-10-14）。規約が読めないので使わない |
| Pianobook の各サンプルパック | https://www.pianobook.co.uk/faq/ | FAQ は「作曲・制作に商用でも使ってよい。ただしこれらを商用のサンプルライブラリにしないこと」。パックごとに作者の規約が違い、SoundFont をソフトに同梱して配る形が認められるか不明。個別のパックの規約を読むまで使わない |

### 規約は使える（CC0 / CC BY）が、まだ変換していない候補（2026-10-14）
Naked Drums（Wilkinson Audio、CC BY 4.0、1.3GB）、DRS Kit（CC BY 4.0）、SM Drums（Public Domain）、Swirly Drums・Unruly Drums・Frankensnare・Gogodze Phu Vol I/II（CC0）、Fashionbass・Pastabass・Black and Blue Basses・Swagbass・Ergo EUB（CC0）、Shinyguitar（CC0）、Headroom Piano（CC BY 4.0）、VCSL Keys（CC0）、MTG Solo Sax（CC BY 4.0）、Bear Sax・Weresax・War Tuba（CC0）、Minifreak Pads・Wavestate Pads（SHLD Music、CC0）。根拠は SFZ Instruments の一覧（https://sfzinstruments.github.io/ 、2026-10-14 確認）。**使う前に各リポジトリの LICENSE 本文を読んでから、この表に移すこと。**

### 2026-10-14 人間の判断（旭さん）
- 作曲ソフトへの追加音源の組み込みを許可（「入れて良いです」）。組み込み先は作曲ソフト（tools/composer/entry.ts）のみで、ゲーム本体の `dist/` には入れていない。ゲームに入れる場合は別途、容量予算とクレジット（Greg Sullivan のエレピ3種は CC BY 3.0 で表記必須）を確認する。
- 書き出しの仕上げは「B」（-13.5 LUFS・左右の広げなし）を標準にした（rock-clean・rock-clear・jpop-band）。

### 歌声の音源（2026-10-18、人間の指示「作曲ソフトに歌う機能を追加しよう」）
| 素材 | 入手元 | 規約の要点 | 扱い |
|---|---|---|---|
| 重音テト UTAU 音源（通常 単独音＋連続音 TETO-tougou-110401・弱音源 TETO-jakuongen210725・滑らか音源 TETO-namerakaongen211125） | https://kasaneteto.jp/utau/ （規約: https://kasaneteto.jp/guidelines/voice.html ） | 個人が歌わせた曲を動画サイトに投稿・広告収入を得る・同人で販売・配信するのは許諾不要（公式は「今のところ商用利用に当たらない」）。**音源そのものの配布・販売は、改変の有無を問わず禁止**。企業の商用利用・規約の範囲を超える利用は別途許諾（窓口: クリプトン・フューチャー・メディア）。犯罪・自殺系など問題のある作品、第三者を傷つける作品には使わない。「重音テト」の表記は必須ではない | **リポジトリに入れない**（再配布になるため）。各自が公式から入手して `assets-src/voicebanks/teto/`（gitignore 済み）か `~/voicebanks/teto/`、または環境変数 `SUNSHINE_VOICEBANKS` の場所に置く。歌声エンジン（`tools/singer/sing.py`）は書き出しのときにだけ読む。**ゲーム本体（dist/）には入れない**。ゲームの販売に歌声を使う場合は、別途の許諾が必要か窓口に確認してから（人間の承認が必要） |
