# シンセサイザーの音づくり（作曲ソフト用ガイド）

作曲ソフトのシンセ音色は、パートの `patch` で選ぶ。録音音源（FluidR3 の GM シンセ音色、MIT）を使うので、つまみ（フィルター・ADSR・LFO）を自由に回す本物のシンセではない。以下は「どの音色を、どう書けば、そのシンセらしくなるか」の対応表。

## 基本のしくみ（学んだこと）
- 波形: サイン（丸い・基音のみ）／三角（やわらかい）／矩形（芯があり中空・8bit寄り）／ノコギリ（明るくぎらつく・倍音が多い）。ノコギリを削って（ローパスフィルター）音色をつくるのが「引き算合成」。
- ADSR: 立ち上がり（アタック）・減衰・保持・余韻。パッドはアタック1.5秒以上、プラックはサステイン0で減衰を200〜700ミリ秒。
- LFO: 約2Hzの揺れでビブラート。譜面では `~` が近い。
- スーパーソー: ノコギリ7本を少しずつずらして重ね、低音を削って広いリバーブ。厚いサビ・トランス・ボカロ系のコード刻み。
- リーゼベース: ノコギリ2本のずれがうなりを作る太い低音。

## patch 一覧
| 種類 | patch | 使いどころ |
|---|---|---|
| リード | squareLead / sawLead / calliope / chiff / charang / fifths / bassLead | 旋律。sawLead はサビ、squareLead は8bit寄り、charang は攻め、fifths は力強く |
| ベース | synthBass1 / synthBass2 | 1＝太く丸い、2＝硬く尖る。根音を低く |
| パッド | warmPad / newAge / halo / sweep / metalPad / bowedGlass | `sustain` 2〜3 の長い音 |
| 刻み | polysynth / synthStrings1 / synthStrings2 | 和音の刻み・厚み |
| 飾り | crystal / iceRain / brightness / starTheme / atmosphere / goblin / echoDrops / soundtrack | ここぞの場面だけ |

声に聞こえる音（GM 85・91）は入れていない。

## 書き方の定石
- パッド: `sustain` 2〜3、低め〜中音域、`volume` は控えめ。
- プラック: `polysynth` か `crystal` に `sustain` 0.4。
- リード: `~` と `phrase` で歌わせる。
- ベース: 旋律と音域を重ねない。
- 1曲に使える音色の種類は約14まで（MIDIのチャンネル数）。

## 見本
`assets-src/ai-songs/synth-patch-tour-1.json`（リードとベース）、`synth-patch-tour-2.json`（パッドと飾り）。同じ短いフレーズを音色ごとに順に鳴らす聞き比べ。

## 出典
- [Basicwavez: Fundamentals of audio synthesis](https://basicwavez.com/fundamentals-of-audio-synthesis/)
- [Produce Like A Pro: Supersaw](https://producelikeapro.com/blog/supersaw-synth-explained/)
- [emastered: シンセパッド](https://emastered.com/ja/blog/synth-pad)
- Splice / LANDR の合成方式の解説
