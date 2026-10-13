# 音のクオリティを上げる6つの道筋（Suno に近づけるための実際の手当て）

作曲ソフト（`tools/composer/`）で、AIソングJSON から録音音源で鳴らすときに使える手当てを、道筋ごとにまとめる。数字は出発点で、耳で直す。

| 道筋 | 何をするか | どこにあるか |
|---|---|---|
| 1 音源の質 | 録音音源を増やす。**ベース**（FreePats・Sneakybass）、**ドラム**（Muldjord・各ジャンル用）、**ギター**（Karoryfer）、**オーケストラ**（VSCO 2 CE。弦・金管・木管・ティンパニ・ハープ・マリンバ・オルガン）、**グランドピアノ**（Salamander） | `assets-src/soundfont/extra/*.sf3`、`tools/soundfont/build-*.mjs`、規約は `docs/assets-credits.md` |
| 2 ドラムの本物らしさ | ジャンル別の drumMix・ドラム音源・ゴーストノート・フィル・位置ずらし（push） | `docs/sound/drum-genre-guide.md`、`drum-fills.md`、`--genre` |
| 3 アンプ・エフェクト・空間 | 22種のエフェクト（fx）、NAMアンプ、リバーブ（room／plate／hall の IR） | `docs/sound/effects.md`、`amp-sim-guide.md`、`--space` |
| 4 マスタリング | ジャンル別の仕上げ（大きさ・EQ・圧縮・広がり）。`rock-open` など | `tools/composer/master.mjs`、`--master-preset`、`docs/sound/mastering-guide.md` |
| 5 編曲の厚み | 同じ旋律を1オクターブ上に重ねる、左右に振る、合奏と独奏を重ねる、gainDb で前に出す | `docs/sound/layering-guide.md`、`arrangement-guide.md`、パートの `gainDb` |
| 6 人間らしさ | human（タイミング・強さ・音程のゆれ）、swing、pushMs、dynamics: natural | AI ソングの `human`・`swing`・`dynamics` |

## ジャンル別の出発点（サウンドセット `--sound` に入れてある）

| 場面 | サウンドセット | 音源 | 仕上げ（`--master-preset`） | 厚みの足し方 |
|---|---|---|---|---|
| バラード | `ballad-piano-strings` | ピアノ＝Salamander、弦＝VSCO、ベース指弾き、ジャズドラム | `pop` か `solo` | 弦の合奏に violin／cello の独奏を重ねる。ピアノは左手を低く、右手に8分のアルペジオ |
| オーケストラ・ボス | `orchestra-depth` | VSCO（弦・金管・ティンパニ）、Salamander | `orch` | horn／trombone で和音の壁、timpani で拍の頭、trumpet の合図。合唱（choir）は別パート |
| 町・村 | `game-town` | VSCO（flute・clarinet・harp）、Salamander | `game-field` | 木管の旋律に harp の分散和音。ドラムなし |
| ダンジョン | `game-dungeon` | VSCO（cello・contrabass・低い弦） | `game-dungeon` | 余韻の長いパッド＋低い弦の持続音。音数は少なく |
| ジャズ | `jazz-trio` | Salamander、ウッドベース、ジャズドラム | `jazz` | swing・7thコード、trumpet のテーマ |
| アンビエント | `ambient-wide` | VSCO の弦・Salamander | `ambient` | 長い音、左右に広げる、リバーブ大きめ |
| ロック・パンク・メタル | `punk-run`・`rock-4`・`game-boss` ほか | ギター／ベース／ドラムのジャンル別 | `rock-open`・`punk`・`metal` | 旋律の1オクターブ上の重ね、gainDb で前へ |

## オーケストラ音源の使い方（要点）

- パートの `patch` に violin・viola・cello・contrabass・pizzicato・stringEnsemble・slowStrings・trumpet・trombone・tuba・horn・brassSection・oboe・bassoon・clarinet・piccolo・flute・timpani・glockenspiel・marimba・churchOrgan・reedOrgan を書くと、書き出しで自動的にオーケストラ音源が選ばれる。
- 音源は強弱を2層（弱・強）持つ。velocity（音の強さ）が上がるほど明るく強い録音に切りかわる。
- 伸ばす音は中ほどをくり返す（ループ）ので、長い音符でも途切れない。短い音（ハープ・ピチカート・ティンパニ・マリンバ）は録音の自然な減衰で鳴る。
- 本物の独奏楽器は音の数が少ないほど映える。1パートに和音を詰めず、旋律は1音ずつ。
- 見本: `assets-src/ai-songs/orchestra-showcase.json`（仮）。

## できないこと・正直な限界

- 歌（ボーカル）は入れない方針。
- 録音を増やしても、Suno のような「生成モデルの一体感」には届かない。耳で聴いて音量・EQ・空間を整える作業は残る。
- 音源の変換は、強弱2層・一部の音だけ（音の間は高さをずらして補う）。足りない音が気になったら層や音を増やす（`build-orchestra.mjs`）。
