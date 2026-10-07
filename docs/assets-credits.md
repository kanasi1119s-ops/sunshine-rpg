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
| GeneralUser GS 2.0.3（`GeneralUser-GS.sf2`、約32MB。作曲ソフト用の音源の候補） | https://github.com/mrbumpy409/generaluser-gs （作者: S. Christian Collins、https://www.schristiancollins.com/generaluser） | 2026-10-07 | 作曲ソフトの録音音源の聴き比べ用。`assets-src/soundfont/` に置いた。作曲ソフトだけ `COMPOSER_SOUNDFONT=assets-src/soundfont/GeneralUser-GS.sf2 node tools/composer/build.mjs` で差し替えて使う。**ゲーム（`game.sf3`）には入れていない** | 独自の許諾（`assets-src/soundfont/LICENSE-GeneralUserGS.txt`）。商用の音楽制作・ソフトへの組み込み・改変・再配布は可。ただし作者自身が「含まれるサンプルの出どころを100%は保証できない（市販のサウンドフォントやサンプルCDからのものはない）」と書いている。**ゲームに入れて配布するなら、このリスクを人間（旭さん）が了承してから** | 不要（入れるなら感謝の表記が望ましい） |
| 使わない／保留: VSCO 2 Community Edition（CC0、オーケストラ。約3GB、SFZ形式） | https://versilian-studios.com/vsco-community/ | 2026-10-07 | 規約はCC0で問題なし。ただしSFZ形式で大きく、今のエンジン（SoundFont）では鳴らせないため保留。SF2へ変換して小さく切り出せれば弦・管の質を上げる候補 | CC0（表記不要） | 不要 |
| 使わない／保留: Salamander Grand Piano V3（CC BY 3.0） | https://github.com/sfzinstruments/SalamanderGrandPiano | 2026-10-07 | SFZ形式（48kHz/24bit）。ピアノの質を上げる候補。SF2への変換と容量の確認が必要 | CC BY 3.0。商用・改変可。**作者 Alexander Holm のクレジット表記が必要** | 必要 |
