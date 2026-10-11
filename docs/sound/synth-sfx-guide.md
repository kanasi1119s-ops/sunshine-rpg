# シンセの音色づくりと、ゲームの効果音づくり（2026-10-11 調査）

シンセの音色（リード・パッド・ベース・プラック・弦・金管・ベル・オルガン・ノイズ・シネマティック）の作り方と、ゲームの効果音（SE）の作り方を、ネットの解説 37 件（文末）から調べ、うちの作曲ソフトで使える数字（Hz・秒・dB・割合）にまとめた。**文章は写さず、数字と考え方だけを借り、言葉は自分で書き直している**。既存ゲームの効果音は再現しない。ここにあるのは、どのゲームにも通じる「一般的な作り方」だけである。

**既存文書との分担**: 波形・フィルター・ADSR・ユニゾンの基本表は `sound-design-basics.md` §4 に、patch の一覧は `synth-guide.md` に、帯域とミックスは `mixing-guide.md` にある。この文書は **それらに無い部分**（音色の種類別の設計表、FM・ウェーブシェーパー・ビットクラッシュの数字、ゲーム SE 58 種のレシピ、SE と BGM の共存、Web Audio API での書き方、実装提案）を足す。重なる所は参照だけにした。

**数字の読み方**: 「出」は記事に書かれていた数字。「補」は記事に数字が無く、複数の記事の傾向と一般的な慣例から置いた**出発点**（SE レシピの数字は大半が補）。**どの数字も最後は耳と A/B で決める**。なお、記事の多くは数字が少なく（図の中にだけある、質的な説明のみ、など）、数字が取れたものを「出」にした。

## 1. 要点
1. **音色は「波形（素材）× フィルターの時間変化（明るさ）× 音量の時間変化（ADSR）」で決まる**。プラックは「明るく始まりすぐ暗くなる」、パッドは「ゆっくり開いてゆっくり閉じる」、ブラスは「音量より少し遅れて明るくなる」（出 [12]）。
2. **効果音は短く、立ち上がりを速く**。UI の「ピッ」は 100ms 前後、決定は 100〜250ms、エラーは 150〜300ms、衝撃は 200〜500ms、報酬・レベルアップは 1〜2 秒（出 [26][28]）。先頭の無音は削る。
3. **音の向きで意味を伝える**。上がる＝成功・回復・開く、下がる＝失敗・閉じる・ダメージ。成功は 3 度（または 5 度）の 2 音で上がり、失敗は下がるか不協和（短 2 度）にする（出 [28]）。
4. **効果音は「層」で作る**。①打撃（低い、短い）②本体（ノイズ・トーン）③飾り（高い、きらめき）の 3 層が基本。層ごとに周波数の席を分ける。
5. **同じ音を連続で鳴らすと疲れる**。足音・文字送りは、ピッチを ±3〜8%、音量を ±1dB ずらして毎回変える。連打の間隔の下限は 60〜200ms（出 [28]。数字は記事間で 100 と 200 に割れた）。
6. **警告音は「基音 150〜1000Hz ＋ 4 本以上の倍音が 300〜4000Hz」、緊急度はパルスの数と速さで表す**（出 [30]。高＝速い 10 連、中＝やや遅い 3 連、低＝1〜2 連）。
7. **Web Audio API では、音量の立ち上がりは直線、減衰は指数で描き、指数カーブの終点は 0 にできない（0.0001 など小さな正の値にする）**（出 [1][7]）。
8. **BGM との共存は「帯域をずらす」と「音量で優先順位をつける」の 2 本立て**。SE は BGM の 1〜4kHz（旋律・歪みギター）と重なりやすい。うちでは `applyGameDuck`（1〜4kHz のパートを 2.5dB 下げる）が既にある。
9. **うちの `SYNTH_PATCHES` は録音（GM）音源で、つまみ式のシンセではない**。音色の「波形・フィルター・ADSR」は、近い patch の選択と `sustain`・`bright` で近似する（§3 の最右列）。**本物の合成は `voices.ts`（Web Audio）と `se-library.ts` の合成フォールバックだけ**にある。

## 2. 今のうちの合成まわり（読んだ結果）
| 場所 | 中身 | この文書との関係 |
|---|---|---|
| `src/audio/ai-song.ts` `SYNTH_PATCHES`（37 個） | ギター 5（nylonGuitar 24〜mutedGuitar 28）、ベース 5（acousticBass 32・fretlessBass 35・slapBass 36・synthBass1 38・synthBass2 39）、弦 2（synthStrings1 50・2 51）、リード 7（squareLead 80・sawLead 81・calliope 82・chiff 83・charang 84・fifths 86・bassLead 87）、パッド・FX 18（newAge 88〜starTheme 103）。声に聞こえる音（85・91）は入れていない | §3 の最右列は、この名前で書いた |
| `src/audio/voices.ts`（741 行、Web Audio の合成） | `strings`＝ノコギリ 2 本（±9 セント）＋三角、LP 2300Hz。`pad`＝サイン＋三角（+11 セント）＋サイン 1 オクターブ上、LP 1400Hz。`bass`＝三角＋矩形（LP 720Hz）＋サイン（1 オクターブ下）。`sfxUp/Down`＝指数グライド（上は ×2.6、下は ×0.3）。`impact`＝LP が下がるノイズ＋サインの落下。`swoosh`＝BP（Q1.2）が f→6f。`wind`・`pierce`・`chime`・`bell`・`sub808`・`cowbell` ほか | 合成 SE の部品がすでにある。新しく足すのは FM・ピンクノイズ・クラッシュ・ユニゾン |
| `src/audio/audio-engine.ts` | `scheduleNote`: 加算はサイン系は 1 本、`rich`（BGM）はデチューン ±6 セントの 2 本、アタック 5ms（BGM 12ms）、リリース最大 50〜120ms。`playSe`: `gm` 付きは録音、無ければ合成。`seBus`・`seGain` | SE の包絡は固定で、細かい ADSR は持てない |
| `src/audio/se-library.ts`（53 種、各 2〜3.6 秒、240BPM） | 録音音源（GM）＋合成ノイズの重ね。長い余韻は 3 拍（0.75 秒）で切る。勝利・レベルアップは独自の楽句 | 本書 §5 は「録音を使わない純合成の SE」のレシピで、フォールバックと置き換え候補 |
| `docs/sound/synth-guide.md` | patch の使いどころ、書き方の定石 | 変更なし |

## 3. 音色の設計表（種類 × 波形 × フィルター × エンベロープ × LFO × エフェクト × うちの近似）
A/D/S/R は秒（S は 0〜1 の割合）。フィルターは LP＝ローパス。「出」は記事の数字、「補」は目安。
| 種類 | 波形 | フィルター | エンベロープ A / D / S / R（秒） | LFO | エフェクト | うちの patch での近似 |
|---|---|---|---|---|---|---|
| **リード（ノコギリ）** | ノコギリ 2 本（±5〜10 セント）。迷ったらこれ（出 [13]） | LP 2〜4kHz、レゾナンス少し高め（抜けを出す、出 [13]）。キー追従 70〜100% | 0.005 / 0.1 / 0.8〜1 / 0.1（補） | ビブラート 5〜6Hz・深さ 20〜30 セント・0.3〜0.8 秒遅れて開始（補。ブラスは 5Hz・ごく浅く・AR で遅らせ、出 [12]） | 軽いディレイ（付点 1/8）、リバーブ少し | `sawLead`（サビ）、`charang`（攻め）。旋律に `~` と `phrase` |
| **リード（矩形・ちいさな芯）** | 矩形、デューティ 12.5/25/50%（NES 系は 4 段階：12.5・25・50・75%、出 [32]）。細いほど鼻にかかる | LP は開き気味（6kHz 以上）か無し | 0.001 / 0.05 / 0.7 / 0.05 | ビブラート 6Hz・浅め | ビットクラッシュ 8bit（§6-4）で味付け | `squareLead`、`calliope` |
| **リード（やわらかいソロ）** | 三角＋サイン（1 オクターブ上を少し） | LP 1.5〜3kHz | 0.03 / 0.2 / 0.7 / 0.3 | 5Hz・25 セント | ホールリバーブ | `chiff`、`bowedGlass`、`fifths`（力強く） |
| **パッド** | ノコギリ 2〜3 本（±10〜15 セント）＋サイン。ウェーブテーブルなら位置を LFO でゆっくり動かす | LP 800〜2kHz、レゾナンス低〜中（目立たせない、出 [13]）。遅いフィルター包絡で少しずつ開く | 1.5〜2.5 / 長い / 0.65〜1 / 2〜5（`sound-design-basics.md` §4-3 の出） | 0.5〜2Hz でフィルターか音量をゆっくり揺らす（出） | 長いリバーブ（2〜4 秒）、コーラス。低域は 100〜150Hz でハイパス | `warmPad`、`newAge`、`halo`、`sweep`、`metalPad`。`sustain` 2〜3、`volume` 控えめ、`duck` 0.2〜0.4 |
| **ベース（サブ）** | サイン（または LP で丸めたノコギリ） | サイン：無し。ノコギリ：24dB LP を低く置き、音程が聞こえるまで上げ、レゾナンスで重い低域を少し間引く（出 [34]） | 0.003 / 0.2 / 0.9 / 0.05〜0.1（リリース 50〜100ms でクリックを防ぐ、出 [33]） | なし | 軽い歪み（2 次・3 次の倍音を足して小さなスピーカーでも聞こえるように、出 [33]）。80〜100Hz 以下はモノ | `synthBass1`（丸い）。根音を低く、旋律と音域を重ねない |
| **ベース（リース／ノコギリ 2 本）** | ノコギリ 2 本、ずれ 5〜15 セント（3〜20 の範囲、出 [33]）。うなりが太さになる | LP 800Hz〜2kHz、遅い LFO（0.5〜2Hz）でカットオフを揺らす（出 [33]） | 0.01 / 0.3 / 0.8 / 0.1 | 0.5〜2Hz（フィルター） | 少し歪ませる | `synthBass2`（硬く尖る）、`bassLead` |
| **ベース（アシッド）** | ノコギリか矩形 | LP、レゾナンスは自己発振の手前まで高く（出 [33]）。フィルター包絡は速く鋭く | 0 / 0.15 / 0.2 / 0.05 | なし | ディストーション | `synthBass2` ＋ `bright` を下げ気味、短い音（`'`） |
| **プラック** | ノコギリか矩形（デューティ細め） | LP が閉じ気味から始まり、フィルター包絡の量を大きく取る。包絡のアタックは 0（出 [13]） | 0 / 0.1〜0.3 / 0〜0.3 / 0.05〜0.3（補は basics §4-3 の出） | なし（または浅いビブラート） | 短いディレイ、軽いリバーブ | `polysynth`、`crystal` に `sustain` 0.4。`pluck-arp`（`PART_RECIPES`） |
| **アルペジエーター** | プラックの音色を使う | 開き気味（4〜6kHz）。フィルター包絡は短く | 0 / 0.12 / 0.15 / 0.08。**ゲート（音の長さ）は歩幅の 50〜80%**（出 [17]：既定は歩幅の半分、小さいほどスタッカート） | なし | ディレイ（付点 1/8）、ステレオに振る | 16 分音符で刻み、`polysynth` を `sustain` 0.4。音域は 1〜2 オクターブ（出 [17]：幅は 0〜5 オクターブ） |
| **ストリングス風（弦楽合奏機）** | ノコギリ＋パルス幅変調（デューティ 50%↔約 5% を三角波で動かす、出 [14]）。または細いパルス（5〜20%）を 2 本、片方は 1 オクターブ上（出 [15]） | LP 約 6kHz・HP 約 200Hz で帯域を狭める（出 [15]）。キー追従は中くらい | 0.2〜0.6 / 短い / 1 / 0.5〜1.5（補。台形の音量、長い尾、出 [14]）。ベロシティは効かせない（昔の機械は無反応、出 [14]） | 低い LFO＋ランダム（サンプル＆ホールド）で自然な揺れ（出 [14]） | **コーラスを 2 段直列（3 タップ）**（出 [15]） | `synthStrings1`（太い）、`synthStrings2`（明るい）。`chorus` 0.3、`reverb` 0.3 |
| **ブラス風** | ノコギリ（またはトランペット様の波形） | LP が音量より**少し遅れて**開く（高い倍音は立ち上がりが遅い、出 [12]）。レゾナンスは強く吹くほど上げる（出 [12]） | 0.02〜0.06（強いほど短く）/ 0.1 / 0.7 / 0.05〜0.1（出 [12]：リリースはごく短く） | ビブラート約 5Hz をごく浅く、AR で遅らせる。**頭の約 50ms だけ約 80Hz の三角波でフィルターを揺らして「ガッ」とした唸り**（出 [12]。ピッチは揺らさない） | 小さなノイズを下に混ぜる（出 [12]）。リバーブ中 | `charang`、`sawLead` ＋ `bright` を少し下げる。短い打ち込みは `staccato` |
| **ベル（FM）** | キャリア 1：モジュレーター 3.5 の**非整数比**（出 [9]）。または 1.41・2.76 の比（出 basics §4-1）。または非整数比のサイン 6 本の足し算（出 [11]） | なし（FM の強さ＝インデックスで明るさを決める）。インデックスを時間とともに下げる（出 [8]） | キャリア 0.002 / 2〜4 / 0 / 長い。モジュレーター 0.1〜0.15 / 0（出 [9]） | 同じ高さに近い 2 つの部分音をわずかにずらして「ワンワン」（うなり、出 [11]） | 長いリバーブ | `crystal`、`bowedGlass`、`iceRain`、`starTheme`、`bell-accent`（`PART_RECIPES`） |
| **エレピ（FM）** | キャリア 1：モジュレーター 14（出 [9]）。モジュレーターの強さ 0.55→0.30 | なし | モジュレーター 0 / 0.25〜0.40 / 0 / —（頭だけ明るい）。キャリア 0 / 0.5 / 低い / 0.3（出 [9]） | 浅いトレモロ 4〜5Hz | コーラス、軽い歪み | `polysynth` を `sustain` 0.5（近似）。録音の GM エレピを使うほうがよい |
| **オルガン** | ドローバー＝倍音 1・3・2・4・6・8・10・12・16 番目を加える足し算（出 [16]）。「88 8000 000」が基本の太い音色。矩形の近似は「00 8030 200」（出 [16]） | LP は開いて使う。キークリックはフィルターの速い包絡で（出 [16]） | **四角い包絡**：音量は 0 / 0 / 1 / 0.01〜0.03（押したら全開、離したら止まる、出 [16]） | ロータリー（レスリー）風のビブラート 6〜7Hz は別のエフェクトで（補） | コーラス、軽い歪み | patch に純オルガンは無い。`sawLead` ＋ `bright` を下げて近づける。`voices.ts` に足し算音源を足す案（§10 提案 7） |
| **ノイズ系（風・ライザー・スネア的）** | 白色ノイズ（平ら）、ピンク（−3dB/オクターブ）、ブラウン（−12dB/オクターブ）（出 [4]） | BP か LP。ライザーは 150Hz→10kHz を 4〜8 小節で（出 [23]）、レゾナンス 15〜20% | 風：0.3 / — / 1 / 0.5。ライザー：直線のゆっくりした立ち上がり | 風：0.2Hz・深さ 500Hz でカットオフを揺らす（出 [5]） | リバーブ 2〜6 秒、付点 1/8 ディレイ（出 [23]） | `sweep`、`atmosphere`、`goblin`（飾り）。実際の風・ライザーは `voices.ts` の `wind`・`swoosh` |
| **シネマティック（ドローン・ヒット・ライザー）** | ドローン：低いサイン／ノコギリ 3 本（0・+12・−12 半音、出 [23]）に 5〜7 ボイスのユニゾン 10〜15 セント（出 [23]） | LP でゆっくり開閉 | ドローン：3〜6 / — / 1 / 4〜8。ヒット：0 / 0.1 / 0 / 1.5〜3 | ピッチの揺れ ±2 半音の LFO（出 [23]）＋±50 セントの微かなずれで不穏に | 長いリバーブ（2〜6 秒）、リバース・リバーブ（反転して残響をつけ、もう一度反転すると手前に膨らむ、出 [35]） | `soundtrack`、`atmosphere`、`halo`、`warmPad` の低音域。`sustain` 3 |

## 4. 波形・フィルター・包絡・LFO の設定の目安（早見）
| 要素 | 値の目安 | 意味・注意 |
|---|---|---|
| 波形 | サイン＝丸い基音のみ／三角＝やわらかい／矩形＝中空で芯／ノコギリ＝倍音が多く明るい（出 [2]） | 引き算合成の素材。迷ったらノコギリ |
| パルス幅 | 50%＝矩形、25%・12.5%＝細く鼻にかかる（出 [32]）。PWM は 5〜50% の間を動かす（出 [14]） | 動かすと弦・パッドの厚み |
| LP カットオフ | ベース 40% 開き、リード 2〜4kHz、パッド 0.8〜2kHz、プラックは閉じ気味から開く | 暗い〜明るい |
| レゾナンス | 15〜35% で性格づけ。最大近くは自己発振＝サイン音（出 [20]：レーザー音はこれで作る） | 山を作る |
| フィルター包絡 | プラック＝速いアタック・短いディケイ。ブラス＝音量より遅れる（出 [12]） | 時間による明るさ |
| 音量包絡 | 立ち上がりは直線、減衰・余韻は指数（出 [1][7]） | 自然な減り方 |
| LFO ゆるい揺れ | 0.5〜2Hz（出 basics §4-2） | パッド、フィルター |
| LFO ビブラート | 5〜8Hz、10〜30 セント、0.3〜1 秒遅れて開始（出 [12][21]） | リード、弦 |
| LFO トレモロ | 2〜4Hz（出 [21]） | 浮遊感 |
| LFO ワブル・AM | 20〜40Hz の矩形で音量を刻むと「パルス音」（出 [2]：880Hz のサイン × 30Hz） | 警報、麻痺、扉のきしみ |
| ポルタメント／グライド | 指数グライド 30〜500ms | ジャンプ、レーザー、ワープ |
| キー追従 | 70〜100% | 高い音がこもらない |
| 音の長さ | UI 50〜250ms、衝撃 200〜500ms、魔法 0.5〜1.5 秒、ファンファーレ 1〜4 秒 | §5 |

## 5. 効果音のレシピ集（58 種）
### 5-0. 書き方の約束
- 層を `T`（OscillatorNode）、`N`（ノイズ）、`FM`（2 オペレーター）で書く。**`f 880→1320 (.05)`＝周波数が 880Hz から 1320Hz へ、0.05 秒で指数的に動く**。1 つだけなら固定。
- **`[a/d/s/r]`＝ A/D/S/R（秒、s は割合）**。`@0.12` は鳴らし始める時刻（秒）。`-6dB` は、その SE でいちばん大きい層に対する相対音量。
- フィルターは `LP`・`HP`・`BP` ＋ 周波数（`→` で掃引）＋ `Q`。
- 長さは音が実質消えるまで（余韻込み）。**SE 全体の山（ピーク）は −6〜−3dBFS を目標**に、層の合計を調整する。
- ピッチは「ゲームの BGM の調」に合わせられるものは `※調` とした（§8）。
- 有名な効果音と同じ 2 音・同じ形にならないよう、音程の組は独自に選んだ（例：コインは 5 度、決定は上行 5 度）。
- 数字は**出発点（補）**。

### 5-1. メニュー・画面（14 種）
| # | 名前 | 構成（層・周波数・包絡・音量） | 長さ |
|---|---|---|---|
| 1 | カーソル移動 | T triangle 1320 [.001/.03/0/.01] 0dB + T sine 2640 [.001/.02/0/.01] −12dB。毎回ピッチ ±2% | 0.05 秒 |
| 2 | 決定 ※調 | T triangle 880 [.003/.06/.3/.04] @0 → T triangle 1319 [.003/.12/.2/.08] @0.06（上行 5 度）+ T sine 2638 [.002/.1/0/.05] @0.06 −10dB | 0.25 秒 |
| 3 | キャンセル | T triangle 659 [.003/.05/.3/.03] @0 → T triangle 440 [.003/.1/.1/.07] @0.06（下行）。LP 3kHz | 0.2 秒 |
| 4 | ブブー（使えない） | T square 150 と T square 157（うなり）を 2 回 @0・@0.16、各 [.005/.1/.6/.02]、LP 1.2kHz | 0.35 秒 |
| 5 | メニューを開く | T triangle 523・659・784 を @0・.04・.08、各 [.002/.05/.2/.05]。N white BP 2k→5k Q1 [.01/.1/0/.05] −18dB | 0.25 秒 |
| 6 | メニューを閉じる | 5 を逆順（784・659・523）、N は BP 5k→2k | 0.22 秒 |
| 7 | 文字送り | T square 900（毎回 ±5%）[.001/.012/0/.005] −14dB。**60ms 未満の再発音は間引く** | 0.02 秒 |
| 8 | ページめくり | N white BP 3k→1.5k Q0.7 [.01/.1/0/.03] | 0.15 秒 |
| 9 | ボタンクリック | N white HP 2k [.001/.008/0/.005] + T sine 1800→1200 (.02) [.001/.025/0/.01] −3dB | 0.04 秒 |
| 10 | スイッチ ON | T square(25%) 700→1000 (.04) [.002/.05/0/.03] | 0.08 秒 |
| 11 | スイッチ OFF | T square(25%) 1000→650 (.05) [.002/.05/0/.03] | 0.08 秒 |
| 12 | セーブ ※調 | T triangle 523・659・784・1047 を @0・.07・.14・.21、各 [.003/.15/.2/.2] + FM(carrier 1568, ratio 3.5, index 3→0 (.4)) [.002/.5/0/.6] @0.21 −10dB | 0.9 秒 |
| 13 | 買い物（お金） | T square 1175 [.002/.04/0/.02] @0 → T square 1760 [.002/.25/0/.2] @0.05（上行 5 度。有名な 2 音と別の組）+ T sine 3520 −14dB @0.05 | 0.35 秒 |
| 14 | 装備する | T sine 180→90 (.08) [.001/.1/0/.03] + FM(carrier 2400, ratio 3.5, index 2→0 (.06)) [.001/.06/0/.04] −6dB @0.03 + N white HP 3k [.001/.01/0/.01] −8dB | 0.2 秒 |

### 5-2. フィールド（15 種）
| # | 名前 | 構成 | 長さ |
|---|---|---|---|
| 15 | 足音（草） | N white BP 1200 Q0.8（毎回 ±15%）[.003/.05/0/.02] 0dB + T sine 110→70 (.04) [.001/.04/0/.01] −10dB | 0.08 秒 |
| 16 | 足音（石） | N white HP 1.5k + BP 3k Q2 [.001/.03/0/.01] + T sine 160→90 (.03) [.001/.04/0/.01] −12dB | 0.06 秒 |
| 17 | 足音（木の床） | T sine 220→110 (.06) [.001/.07/0/.02] + N white BP 700 Q3 [.001/.05/0/.02] −6dB（空洞の響き） | 0.1 秒 |
| 18 | 扉を開ける（きしみ） | T sawtooth 180→260 (.4) →210 (.3)、LP 900〜1500（BP Q8 を 400→900 で掃引）、音量を 35Hz の矩形で刻む（深さ 60%、出 [31]：きしみは速度に比例して増える短いパルスの連なり）[.05/.5/.5/.2] + N pink LP 400 −20dB | 0.8 秒 |
| 19 | 扉を閉める | N brown LP 300→120 (.15) [.001/.15/0/.05] + T sine 90→50 (.15) [.001/.15/0/.05] −3dB + N white HP 2k [.001/.01/0/.005] −10dB | 0.3 秒 |
| 20 | 鍵がかかっている | T sine 160→100 (.04) [.001/.05/0/.02] を @0・@0.12 + N white BP 1.5k [.001/.02/0/.01] −6dB + ガタつき：N BP 2.5k Q5 を 40Hz の AM [.002/.1/0/.05] @0.28 −10dB | 0.5 秒 |
| 21 | 宝箱を開ける | 留め金：N white HP 3k [.001/.01/0/.005]。きしみ：18 と同じで 150→300 (.3) LP 1.2k −6dB @0.05。きらめき：T sine/triangle 1319・1760・2349・2794・3136 を @0.4 から 0.05 間隔、各 [.003/.4/0/.4] −8dB。FM(carrier 2093, ratio 3.5) [.002/.8/0/.8] @0.6 −12dB | 1.5 秒 |
| 22 | アイテム入手 ※調 | T triangle 1047 [.003/.07/.2/.05] @0 → T triangle 1568 [.003/.3/.2/.2] @0.07 + T sine 3136 [.002/.2/0/.1] @0.07 −12dB | 0.5 秒 |
| 23 | 階段 | 足音 16 を 4 回 @0・.18・.36・.54、フィルター中心を 1 回ごとに ×1.08 ずつ上げる、音量 −3dB ずつ小さく | 0.8 秒 |
| 24 | ワープ | T sawtooth ×3（±12 セント）200→2000 (.8) [.1/.6/.6/.2]、LP 400→6k Q2 + N white BP 500→5k Q1.5 [.2/.6/.3/.2] −8dB + FM(carrier 2637, ratio 2.76, index 4→0 (.5)) @0.8 [.002/.7/0/.7] −10dB | 1.6 秒 |
| 25 | ジャンプ | T pulse(25%) 330→660 (.1) [.002/.12/0/.04] | 0.15 秒 |
| 26 | 水しぶき | N white BP 2.5k Q0.7 [.005/.25/0/.15] + 泡：T sine 400→1200 (.05) を 4〜6 個、時刻は 0〜0.3 秒からランダム、各 [.002/.06/0/.02] −10dB | 0.5 秒 |
| 27 | 警報（警告） | T square 660 + T square 1320（−6dB）+ T square 1980（−10dB）を 3 パルス（各 0.12 秒、間 0.08 秒）、[.003/.1/.8/.01]。出 [30]：中程度の緊急度は「やや遅い 3 連」。周期 1.2 秒で繰り返す | 1.0 秒（周期） |
| 28 | 地響き | N brown LP 90 Q1 [.2/—/1/.6] + T sine 40→30 (1.5) −3dB + 全体を 8Hz・深さ 40% の AM | 1.6 秒 |
| 29 | 壁にぶつかる | T sine 130→70 (.08) [.001/.1/0/.03] + N white BP 400 Q1 [.001/.05/0/.02] −6dB | 0.12 秒 |

### 5-3. 戦闘（8 種）
| # | 名前 | 構成 | 長さ |
|---|---|---|---|
| 30 | 敵と遭遇 | T sawtooth 1200→200 (.35) [.002/.3/.1/.1]、LP 3k + N white HP 4k [.001/.25/0/.1] −8dB + T square 110 [.005/.2/.4/.15] @0.3 −6dB | 0.6 秒 |
| 31 | 斬撃 | N white BP 1.5k→6k Q1.2 (.12) [.01/.1/0/.03]（風切り）+ @0.1 N white HP 3k [.001/.04/0/.02] −3dB + T sine 200→90 (.08) [.001/.08/0/.03] −4dB @0.1 | 0.3 秒 |
| 32 | 打撃・ダメージ | T sine 180→50 (.12) [.001/.12/0/.04] + N white LP 3k→300 (.1) [.001/.1/0/.03] −3dB + クリック N HP 2k [.001/.01/0/.005] −8dB | 0.25 秒 |
| 33 | 会心の一撃 | 31 + T sawtooth 400→1600 (.15) [.002/.15/0/.05] −8dB + FM(carrier 2200, ratio 2.76, index 5→0 (.3)) [.001/.4/0/.3] −10dB @0.1 + 重い低音：T sine 100→40 (.4) [.001/.4/0/.1] @0.1 | 0.7 秒 |
| 34 | ミス（かわされた） | N white BP 800→2.5k Q1 (.15) [.02/.1/0/.05] −6dB | 0.2 秒 |
| 35 | 防御 | N white BP 2k Q4 [.001/.02/0/.01] + FM(carrier 1200, ratio 3.5, index 3→0 (.1)) [.001/.15/0/.1] −3dB + T sine 150→100 (.05) [.001/.08/0/.03] −6dB | 0.25 秒 |
| 36 | 味方がダメージを受ける | T sawtooth 300→90 (.2) [.002/.2/0/.08]、LP 1.5k + N white LP 2k→400 (.15) [.001/.15/0/.05] −4dB + T sine 120→60 (.1) −4dB。2 音目に半音上（短 2 度）を足すと痛い | 0.35 秒 |
| 37 | 敵を倒した | T sawtooth 600→60 (.5) [.002/.5/0/.1]、LP 3k→300 + N white LP 6k→300 (.5) [.001/.5/0/.1] −3dB。全体を 20Hz・深さ 30% の AM（崩れる感じ） | 0.7 秒 |

### 5-4. 魔法・状態（14 種）
| # | 名前 | 構成 | 長さ |
|---|---|---|---|
| 38 | 詠唱・チャージ | T sawtooth ×5（±10 セント）220→880 (1.0) [.8/—/1/.1]、LP 500→5k Q2 + T sine 1760 に 6Hz のトレモロ −12dB。徐々に大きく | 1.2 秒 |
| 39 | 炎 | N pink BP 600→2.5k Q0.8 [.05/.5/.3/.3]（ごうっ）+ パチパチ：N HP 2k の 3ms バースト、毎秒 20〜40 回のランダム −10dB + T sine 80→50 (.5) [.01/.5/0/.2] −4dB | 0.9 秒 |
| 40 | 氷 | FM(carrier 2637, ratio 2.76, index 4→0 (.5)) [.001/.5/0/.5] + きらめき：T sine 3000〜6000 をランダム 5 個、各 [.001/.2/0/.2] −10dB + N white HP 6k [.001/.1/0/.1] −18dB | 0.8 秒 |
| 41 | 雷 | 割れ：N white HP 3k [0/.03/0/.02] 0dB → T sawtooth 3000→200 (.08) [.001/.08/0/.02] −6dB（ジグザグに）→ ゴロゴロ：N brown LP 200 [.05/.6/.2/.5] −2dB @0.05 + T sawtooth 60 LP 150 [.05/.6/.2/.5] −6dB | 1.1 秒 |
| 42 | 風 | N pink BP 400→1200→600 (全体 .8) Q1.2、0.5〜2Hz でカットオフを ±30% 揺らす [.2/—/1/.3]（出 [5]：0.2Hz・深さ 500Hz のゆるい掃引） | 0.9 秒 |
| 43 | 光 ※調 | T sine 1319・1760・2349・3136 を 0.06 間隔で上行 [.003/.3/0/.3] + 3 本の T triangle 2093/2100/2087（うなり）[.1/.4/.3/.5] −8dB + FM(carrier 3136, ratio 3.5) [.001/.8/0/.8] −12dB。HP 500 | 1.2 秒 |
| 44 | 闇 | T sawtooth ×3（±25 セント）110→55 (.6) [.05/.5/.3/.4]、LP 600→200 + T sine 55 −3dB + N brown LP 150 [.3/.4/0/.3] −6dB + 短 2 度の T sine 117 | 1.2 秒 |
| 45 | 回復 ※調 | T triangle 523・659・784・1047・1319 を 0.07 間隔で上行 [.003/.5/0/.3] + T sine 1047＋1319（和音）[.2/.4/.3/.5] −8dB + HP 400 | 1.0 秒 |
| 46 | 能力アップ | T square 440・554・659・880 を 0.05 間隔 [.002/.05/0/.03] + T sine 880→1760 (.3) [.01/.3/0/.1] −8dB | 0.4 秒 |
| 47 | 能力ダウン | 46 を逆順（880・659・554・440）、LP 2k、音量 −3dB | 0.4 秒 |
| 48 | 毒 | 泡：T sine 150→250 (.08) を毎秒 4〜6 回、各 [.002/.08/0/.03] + T sawtooth 98 と 103（うなり）LP 400 [.1/—/.6/.2] −6dB + N white BP 500 Q2 −14dB | 0.7 秒 |
| 49 | 眠り | T sine 523 → 440 → 349 を 0.25 間隔（下行）、4Hz のトレモロ、LP 1.2k、各 [.02/.3/.3/.3] + N pink LP 500 [.3/—/1/.4] −20dB | 1.0 秒 |
| 50 | 麻痺 | T sawtooth 120 を 50Hz の AM、BP 1k Q3 [.01/.3/.5/.1] + N white BP 3k Q4 をランダムに切る（ゲート 10〜30ms）−6dB | 0.45 秒 |
| 51 | 復活 ※調 | T sawtooth ×3（根音・3 度・5 度）LP 1.5k [.4/—/.8/.5] → @0.6 T sine 1047＋2093 [.002/.8/0/.8] + きらめき 3〜5 個 −10dB | 1.6 秒 |

### 5-5. ファンファーレ・節目（7 種）
旋律は**独自に作る**（既存の勝利曲に似せない。同じ音の連打で始めて短い下降で受ける型を避ける、`se-library.ts` の注記と同じ方針）。
| # | 名前 | 構成 | 長さ |
|---|---|---|---|
| 52 | レベルアップ ※調 | ブラス風：T sawtooth LP（フィルター包絡 800→3k、A.01 D.15）を 5 音上行（0.09 秒間隔）→ 最後の音と和音を 0.5 秒保つ [.01/.1/.7/.2]。T sine（1 オクターブ上）−8dB、きらめき FM(carrier 2093) −12dB | 1.4 秒 |
| 53 | 勝利 | ロール：N white BP 1.5k のスネア 8 打、間隔 0.1→0.04 秒で加速 → ブラス風 3 音上行 → 長い和音 1.2 秒 + ティンパニ T sine 100→55 (.3) [.002/.3/0/.2] + シンバル N white HP 6k [.003/1.2/0/.8] −6dB | 3 秒 |
| 54 | ゲームオーバー | T sawtooth + 三角のパッド、下行 3 音（A3→F3→D3）+ 保持、LP 3k→400 (2.5)、リバーブ尾 2 秒 [.1/—/.8/2] | 3.5 秒 |
| 55 | 重要アイテム（小ファンファーレ） ※調 | ブラス風 4 音（0.1 秒間隔）、最後 0.4 秒保持、T sine 1 オクターブ上 −8dB | 1.2 秒 |
| 56 | 経験値・お金のカウント | T square 1200 の 40ms チック、25Hz（0.04 秒間隔）、1 チックごとに +2% 上げる [.001/.03/0/.01] −10dB | 任意 |
| 57 | ボス登場（シネマティック・ヒット） | サブ：T sine 60→30 (1.5) [.005/1.5/0/.5] + N brown LP 200 [.01/1.2/0/.8] −3dB + T sawtooth 3 本の低い和音 LP 500 [.05/1/0/1] −8dB + 逆再生風の N white HP 1k の膨らみを手前 0.8 秒（リバース・リバーブ、出 [35]）−10dB | 3 秒 |
| 58 | 場面転換（スウッシュ） | N white BP 200→8k (1.0) Q1.5 [.8/—/1/.05]（150Hz→10kHz をライザーの目安、出 [23]）+ T sine 100→800 (1.0) −12dB | 1.1 秒 |

## 6. 技法の補足（ユニゾン・FM・ウェーブシェーパー・ビットクラッシュ）
| 技法 | 数字 | Web Audio での書き方 |
|---|---|---|
| ユニゾン／デチューン | 5〜7 ボイス、ずれ 10〜15 セント（出 [23]）。ベースは 5〜15 セント（出 [33]）。音量は各 1/√ボイス数 | `detune = (i-(n-1)/2) * 2*spread/(n-1)`、パンも同様に振る。低域（〜150Hz）はモノにする |
| FM | 比が整数＝音程がある、非整数（1.41・2.76・3.5）＝金属・ベル（出 [8][9]）。インデックスが大きいほど明るい。モジュレーターに短い包絡を付けると「頭だけ明るい」 | モジュレーター OscillatorNode → GainNode(`index × 周波数 f`) → キャリア `osc.frequency`。インデックスの包絡はこの GainNode で |
| ウェーブシェーパー | `tanh(x·drive)` で軟らかい歪み。`drive` 1〜10。入力は −1〜1 に収め、範囲外は端に張りつく（出 [3]）。`oversample = "4x"` | `new Float32Array(1024)`、`curve[i] = Math.tanh(drive * x)`。うちの `distortionCurve`・`ceilingCurve` がある |
| ビットクラッシュ | 8bit 以下でレトロ、4bit 以下で荒れた音（出 [19]）。ドライとのパラレルで原音を残す | 階段状のカーブ：`levels = 2**bits`、`curve[i] = Math.round(x*levels/2)/(levels/2)`。サンプルレート落としは AudioWorklet か、`ScriptProcessor`、またはオフライン描画で |
| AM（刻み） | 20〜40Hz の矩形で音量を刻む（出 [2]） | LFO OscillatorNode → GainNode の `gain` に接続 |
| ピンク／ブラウンノイズ | ピンク −3dB/oct、ブラウン −12dB/oct（出 [4]） | 白色ノイズをバッファに作り、ピンクは Kellet 法の係数つきフィルター、ブラウンは「前の値を 0.98 倍＋小さなランダムを足す」積分器（出 [4]） |
| Karplus–Strong（撥弦） | ディレイ長＝ 1÷周波数、帰還 0.9〜0.99（補）、ループ内の LP で高域から消える（補。出 [18]：その機材では帰還のつまみが減衰＝音の消え方に効く） | `DelayNode` + `GainNode`（帰還）+ `BiquadFilter`（LP）にノイズ 1〜5ms を流す。`harp`・`kalimba` がすでに近い |

## 7. Web Audio API での実現（実装できる形）
```ts
const FLOOR = 0.0001; // 指数カーブの終点は 0 にできない（出 [1][7]）

/** 音量の形。a/d/r は秒、s は 0〜1（peak に対する割合）、hold は保つ秒。終わる時刻を返す。 */
function adsr(p: AudioParam, t: number, peak: number, a: number, d: number, s: number, hold: number, r: number): number {
  p.cancelScheduledValues(t);
  p.setValueAtTime(0, t);
  p.linearRampToValueAtTime(peak, t + Math.max(a, 0.002));      // 立ち上がりは直線（0.002 秒未満はクリックの元）
  const sus = Math.max(peak * s, FLOOR);
  p.exponentialRampToValueAtTime(sus, t + a + d);                // 減衰は指数
  const off = t + a + d + hold;
  p.setValueAtTime(sus, off);
  p.exponentialRampToValueAtTime(FLOOR, off + r);                // 余韻も指数
  return off + r;
}

/** T 層。f1/glide を付けると指数グライド。 */
function tone(ctx: BaseAudioContext, dest: AudioNode, o: {
  type: OscillatorType | PeriodicWave; f0: number; f1?: number; glide?: number; at: number; peak: number;
  a: number; d: number; s: number; hold: number; r: number; detune?: number; lp?: [number, number?, number?];
}): void {
  const osc = ctx.createOscillator();
  if (typeof o.type === "string") osc.type = o.type; else osc.setPeriodicWave(o.type);
  osc.detune.value = o.detune ?? 0;
  osc.frequency.setValueAtTime(o.f0, o.at);
  if (o.f1) osc.frequency.exponentialRampToValueAtTime(o.f1, o.at + (o.glide ?? 0.1));
  const g = ctx.createGain();
  let node: AudioNode = osc;
  if (o.lp) { const f = ctx.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = o.lp[0]; f.Q.value = o.lp[2] ?? 0.7; osc.connect(f); node = f; }
  node.connect(g).connect(dest);
  const end = adsr(g.gain, o.at, o.peak, o.a, o.d, o.s, o.hold, o.r);
  osc.start(o.at); osc.stop(end + 0.02);
}

/** デューティ比つきの矩形（パルス）。位相は聞こえないので cos だけで作る。 */
function pulseWave(ctx: BaseAudioContext, duty: number, n = 64): PeriodicWave {
  const real = new Float32Array(n + 1), imag = new Float32Array(n + 1);
  for (let k = 1; k <= n; k++) real[k] = (2 / (k * Math.PI)) * Math.sin(k * Math.PI * duty);
  return ctx.createPeriodicWave(real, imag);
}

/** N 層。noise は 2 秒の白色ノイズバッファ（使い回す）。BP/LP/HP を掃引できる。 */
function noiseLayer(ctx: BaseAudioContext, dest: AudioNode, buf: AudioBuffer, o: {
  filter: BiquadFilterType; f0: number; f1?: number; sweep?: number; q?: number; at: number; peak: number;
  a: number; d: number; s: number; hold: number; r: number;
}): void {
  const src = ctx.createBufferSource(); src.buffer = buf; src.loop = true;
  const f = ctx.createBiquadFilter(); f.type = o.filter; f.Q.value = o.q ?? 0.7;
  f.frequency.setValueAtTime(o.f0, o.at);
  if (o.f1) f.frequency.exponentialRampToValueAtTime(o.f1, o.at + (o.sweep ?? 0.2));
  const g = ctx.createGain();
  src.connect(f).connect(g).connect(dest);
  const end = adsr(g.gain, o.at, o.peak, o.a, o.d, o.s, o.hold, o.r);
  src.start(o.at); src.stop(end + 0.02);
}

/** FM 層（ベル・エレピ・金属音）。ratio は非整数なら金属的。index はキャリア周波数に対する倍率。 */
function fmLayer(ctx: BaseAudioContext, dest: AudioNode, o: { fc: number; ratio: number; index0: number; index1: number; sweep: number;
  at: number; peak: number; a: number; d: number; s: number; hold: number; r: number }): void {
  const car = ctx.createOscillator(), mod = ctx.createOscillator(), mg = ctx.createGain(), g = ctx.createGain();
  car.frequency.value = o.fc; mod.frequency.value = o.fc * o.ratio;
  mg.gain.setValueAtTime(o.index0 * o.fc, o.at);
  mg.gain.exponentialRampToValueAtTime(Math.max(o.index1 * o.fc, FLOOR), o.at + o.sweep); // インデックスを下げる＝暗くなる（出 [8]）
  mod.connect(mg).connect(car.frequency);
  car.connect(g).connect(dest);
  const end = adsr(g.gain, o.at, o.peak, o.a, o.d, o.s, o.hold, o.r);
  car.start(o.at); mod.start(o.at); car.stop(end + 0.02); mod.stop(end + 0.02);
}
```
- **データで書く**: 1 つの SE を `Layer[]`（上の `tone`・`noiseLayer`・`fmLayer` の引数）の配列にして、§5 の表をそのまま JSON に起こせる。
- **ランダム変化**: 発音のたびに `f0 *= 1 + (Math.random()-0.5)*0.06`、`peak *= 10 ** ((Math.random()-0.5)*2/20)`（±1dB）。
- **連打を間引く**: `lastPlayed[id]` を覚えて、60〜200ms 以内の再発音を捨てる（出 [28]）。
- **スケジューリング**: 発音時刻は `ctx.currentTime + 秒` で正確に予約する。先読みのタイマーは 25ms ごと・0.1 秒先まで（出 [2]）。
- **クリック（プチッ）対策**: 立ち上がりは 2ms 以上、`stop` は包絡が 0 になってから。`cancelScheduledValues` は予約済みの包絡も消すので、使う位置に注意（出 [7]）。
- **長さの短い SE の山**: 層を足した合計が 1.0 を超えないよう、`peak` の合計を 0.7 以内にする（出口にリミッターはあるが、割れの原因を作らない）。

## 8. BGM との共存
### 8-1. 周波数の席
| SE の種類 | 主な帯域 | BGM 側で空ける帯域 | 備考 |
|---|---|---|---|
| UI（カーソル・決定） | 1〜4kHz（明るい 2〜3 音） | 旋律・歪みギターの 1〜4kHz（出 `mixing-guide.md`：BGM を 2〜3dB） | 短いので BGM を下げなくてもよい |
| 打撃・衝撃 | 低音 60〜200Hz ＋ ノイズ 2〜6kHz | キック・ベースと重なる。BGM のキックと同時に鳴るとぶつかる | 衝撃の低音は 100Hz 以上にして、BGM のサブ（〜80Hz）と分ける |
| 魔法・きらめき | 2〜8kHz | シンバル・ハイハット・ベル系 | 高域が重なるのでベル系の BGM は `volume` を下げる |
| 警報・警告 | 基音 150〜1000Hz ＋ 倍音 300〜4000Hz（出 [30]） | パッド・弦の中域 | 目立たせたいので BGM を短く 3〜6dB 下げてよい |
| 風・環境ノイズ | 200Hz〜2kHz | パッド・弦 | 常時鳴らさない。BGM とぶつかるなら −20dB 以下 |
| ファンファーレ | 全域 | BGM と同時に鳴らさない | BGM を止めるか 6〜10dB 下げる |

### 8-2. 音量の優先順位（BGM に対する目安・補）
| 種類 | 目安 | 根拠 |
|---|---|---|
| 警告・重要通知 | +3dB | 出 [28]：警告 +3、通知 0、フィードバック −6、環境 −12（相対） |
| 通知・アイテム入手 | 0dB | 同上 |
| UI のフィードバック（カーソル・クリック） | −6dB | 同上 |
| 足音・環境 | −12dB 以下 | 同上 |
| 同時に鳴る SE | 優先度の低いものを −3〜−6dB | 出 [29]：声が優先 → ほかは下がる |
- **書き出しの山**: SE は約 −1dB（出 [28]）。うちでは −6〜−3dBFS を目標にし、BGM（ゲーム用 −16.5〜−14.5 LUFS、`bgm-loudness.json`）と合わせる。
- **ダッキング**: BGM が SE の間だけ下がる設計。すばやく下げてゆっくり戻す。目安は「アタック 0〜10ms／リリース 50〜100ms／比 3:1〜4:1」（透明なダッキング、出 [33]）または、声のように目立たせたいなら「アタック 100ms／リリース 600ms」（出 [36]）。ファンファーレなら −6〜−10dB を 1.5〜3 秒。
- **うちでの手段**: `applyGameDuck(score, db)`（既定 2.5dB）が BGM 側の「常時の余白」。SE が鳴るときだけ下げる動的なダッキングは `audio-engine.ts` の BGM バスに `setTargetAtTime` を足す案（提案 6）。

## 9. チェックリスト
**音色づくり**
- [ ] 目的の音は「波形（素材）」「フィルターの時間変化」「音量の ADSR」のどれで決まるか、先に決めたか
- [ ] パッド：アタック 1.5 秒以上・リリース 2 秒以上、低域は 100〜150Hz でハイパスしたか
- [ ] プラック：サステイン 0〜0.3、ディケイ 0.1〜0.3 秒、フィルター包絡が速いか
- [ ] ベース：リリース 50〜100ms でクリックを防ぎ、軽い歪みで小さなスピーカーでも聞こえるか
- [ ] ブラス：フィルターが音量より少し遅れて開くか。ビブラートは遅らせたか
- [ ] 弦：帯域を狭め（200Hz〜6kHz）、コーラスを重ねたか
- [ ] ベル：非整数比か、インデックスは時間とともに下げたか
- [ ] ユニゾン：ずれは 15 セント以内か。低域はモノか

**効果音**
- [ ] 目的別の長さに収まっているか（UI 〜250ms、衝撃 〜500ms、報酬 1〜2 秒）
- [ ] 先頭に無音が無いか。立ち上がりは 2ms 以上か（クリック防止）
- [ ] 上行＝成功、下行＝失敗の向きが合っているか
- [ ] 3 層（打撃・本体・飾り）に分け、帯域が重なりすぎていないか
- [ ] 連続して鳴る音は、ピッチ ±3〜8%・音量 ±1dB の変化と、60〜200ms の間引きがあるか
- [ ] 山が −6〜−3dBFS 以内で、層を足して割れていないか
- [ ] BGM の調と合う音（決定・回復・光・ファンファーレ）は調に合わせたか
- [ ] 既存ゲームの効果音・名曲の2音／旋律に似ていないか

**BGM との共存**
- [ ] SE の主な帯域と、BGM の旋律・歪みギターの 1〜4kHz がぶつからないか（`applyGameDuck` を適用）
- [ ] 警告・ファンファーレのとき、BGM を下げたか（−3〜−10dB、ゆっくり戻す）
- [ ] 優先順位（警告 > 通知 > UI > 環境）で音量差がついているか

## 10. 取り入れる提案（実装可能な単位）
どれも**実装前に実験で確かめる**もの。コードは編集していない（提案のみ）。
1. **SE ジェネレーター `sfx-synth.ts`（純合成の SE）**: §7 の `tone`・`noiseLayer`・`fmLayer`・`pulseWave` と、§5 の 58 種を `Layer[]` のデータで持つ。`SfxRecipe = { id; group; name; lengthSec; layers: Layer[] }`。`audio-engine.ts` に `playSfx(id, ctx, dest)` を足し、`playSe` の録音が未準備のときの代わりにする。テスト：オフライン描画（`offline-render.ts`）で全レシピが「長さ ≦ 想定、山 ≦ 0.7、NaN なし」を満たす。
2. **SE の聞き比べコマンド `song.mjs sfx <id> [--wav]`**: 1 のレシピを WAV に書き出し、山・RMS・長さ・スペクトル重心（Hz）を表示。`se-library.ts` の録音版と並べて聞き比べる。
3. **SE の検査 `checkSe(entry)`**: 長さの上限（UI 0.4 秒、衝撃 0.8 秒、魔法 1.6 秒、ファンファーレ 4 秒）、山 −3dBFS 以下、先頭 10ms 以内に立ち上がるか、DC 成分が無いか、主な帯域（1〜4kHz のエネルギーの割合）を計り、警告を出す。`se-library.test.ts` に組み込む。
4. **変化づけ `varySe(recipe, rng)`**: 足音・文字送り・クリックに、ピッチ ±3〜8%、音量 ±1dB、フィルター中心 ±15% をかける。3〜5 個の変種を回す（ラウンドロビン）。再発音を 60〜200ms で間引く。純関数にして乱数を差し替え可能にする。
5. **調に合わせる `tuneSe(recipe, keyRoot)`**: ※調 の付いたレシピ（決定・セーブ・アイテム・光・回復・復活・ファンファーレ）の周波数を、BGM の調の最も近い音階音へ寄せる。最大でも ±2 半音。曲ごとの調は `score` から取れるか確認。
6. **動的ダッキング `duckBgmForSe(level)`**: `audio-engine.ts` の BGM バスの `gain` に `setTargetAtTime`。UI＝なし、通知＝−2dB、警告＝−4dB、ファンファーレ＝−8dB。アタック 10ms／戻り 400〜600ms。SE の `priority` を `SeEntry` に足す。
7. **音源の追加（`voices.ts`）**: ① `fmBell`・`fmEpiano`（§3 の FM 数字）、② `drawbarOrgan`（倍音 1・3・2・4・6・8 を足し算、四角い包絡）、③ `pink` / `brown` ノイズ（`noise()` に種類を追加し、風・地響き・雷を自然に）、④ `unisonSaw`（ボイス数と spread を引数に）。`Instrument` 型に足す。
8. **`PART_RECIPES` の拡充（`sound-sets.ts`）**: 既存の `soft-pad`・`pluck-arp`・`bell-accent` に、§3 から `strings-ensemble`（chorus 0.3・reverb 0.3・duck 0.3）、`brass-swell`（bright −0.1・スタッカート）、`organ-hold`、`cinematic-drone`（sustain 3・reverb 0.5・低音域）、`chip-lead`（`squareLead`・reverb 0）を足す。名前は音の特徴にする。
9. **ビットクラッシュ／ウェーブシェーパーの小さなエフェクト**: `bitcrush(bits)` の階段カーブと `shaper(drive)` を `voices.ts` に足し、レトロ風の場面（チップ風 SE、タイトル画面）で選べるようにする。デフォルトは無し。
10. **聞き比べページ**: 作曲ソフトの画面に、§5 の 58 種を一覧で鳴らす「SE ラボ」を足す（スライダーで周波数・長さ・ADSR を変えられ、JSON を書き出せる）。レシピ調整の道具として、1・2 の後に。

### 実装状況（2026-10-11 第2ラウンド）

| # | 提案 | 状態 | 内容 |
|---|---|---|---|
| 1 | SE ジェネレーター | **入れた** | `src/audio/synth-dsp.ts`（PolyBLEP の波形・ノイズ・双二次フィルター・FFT・WAV）、`sfx-synth.ts`（`renderSfx`・残響・山の正規化・`playSfx`）、`sfx-recipes.ts`（**58 種**）。純 JS なので Node・ブラウザで同じ音。ゲーム本体の `AudioEngine.playSfx(recipe)` から鳴らす。**既存の `se-library.ts`（録音版）は置き換えていない**（並べて聞き比べるため） |
| 2 | 聞き比べコマンド | **入れた** | `node tools/composer/song.mjs sfx [<id>] [--wav] [--key 2:aeolian]`（山・RMS・長さ・立ち上がり・重心。id なしは全件の検査） |
| 3 | SE の検査 `checkSe` | **入れた** | 山 −3dBFS 以下・長さ・立ち上がり 10ms・直流・UI の 1〜4kHz。長さの上限は ui 0.4・impact 0.8・magic 1.6・fanfare 4 に、**`notice` 1.0 秒を足した**（セーブ・購入・エラーなどの通知）。ゆっくりが正しい SE（詠唱・ライザー・勝利の盛り上げ）は `soft: true` で立ち上がりの検査を免除 |
| 4 | 変化づけ | **入れた** | `varySe`・`makeVariants`（4 変種）・`SeThrottle`（間引き）・`RoundRobin`。種が同じなら同じ音 |
| 5 | 調に合わせる | **入れた** | `tuneSe(recipe, tonic, scale)`（※調の層だけ、最大 ±2 半音）。`AudioEngine.setSfxKey` で BGM の調を渡す |
| 6 | ダッキング | **入れた** | `duckBgmForSe`（通知 −2・警告 −4・ファンファーレ −8dB、アタック 10ms／戻り 約 0.5 秒）。`AudioEngine` に BGM と出力の間の `bgmDuck` を足し、`playSfx` が自動でかける |
| 7 | 音源の追加 | 一部 | `fmBell`・`fmEpiano`・`drawbarOrgan`・`unisonSaw` を `Instrument` に追加（`synth-voices.ts` に数字、`voices.ts` に Web Audio の鳴らし方、`gm-map.ts` に GM 番号 14・4・16・81）。**pink／brown ノイズは SE 側（`synth-dsp.ts`）だけ**で、`voices.ts` の風・雨・雷は白色ノイズのまま（既存の音が変わるため） |
| 8 | `PART_RECIPES` の拡充 | **入れた** | `strings-ensemble`・`brass-swell`・`organ-hold`・`cinematic-drone`・`chip-lead`。PartMix に入らないもの（sustain・スタッカート・音域・patch）は `hint` に書いた |
| 9 | ビットクラッシュ／シェーパー | 一部 | 階段カーブ `bitcrushCurve(bits)` と `shaperCurve(drive)` を純関数で用意しテストした。**音源として選べるようにはしていない**（デフォルトは無し） |
| 10 | SE ラボ | **入れた** | `node tools/composer/build.mjs` が `dist-composer/sfx-lab.html`（1 ファイル）も作る。58 種の一覧・鳴らす・高さ／長さ／立ち上がり／余韻／山のスライダー・調に合わせる・変種・WAV と JSON の書き出し・検査の表示 |

**注意**: 数字（周波数・包絡）は本文の表の出発点のままで、**耳での調整はまだ**。音程の組は独自に選び、既存ゲームの効果音と同じ形にしていない。`drawbarOrgan`（GM16）・`unisonSaw`（GM81）は作曲ソフト（GeneralUser）には入っているが、ゲーム用の `game.sf3` にはまだ無い（作り直すときに `USED_GM_PROGRAMS` へ入れる）。

## 11. 参考URL（調べた先。順不同）
**Web Audio API・実装**
1. [MDN: exponentialRampToValueAtTime](https://developer.mozilla.org/en-US/docs/Web/API/AudioParam/exponentialRampToValueAtTime)
2. [MDN: Advanced techniques — Creating and sequencing audio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques)
3. [MDN: WaveShaperNode curve](https://developer.mozilla.org/en-US/docs/Web/API/WaveShaperNode/curve)
4. [react-native-audio-api: Noise generation](https://docs.swmansion.com/react-native-audio-api/docs/guides/noise-generation)
5. [DEV: Procedural audio textures in the browser](https://dev.to/hexshift/how-to-generate-procedural-audio-textures-in-the-browser-no-samples-needed-332l)
6. [Medium: Tips and techniques for the Web Audio API](https://medium.com/@danielmckemie/tips-and-techniques-for-using-the-web-audio-api-89b8beda6cf2)
7. [oxxostudio: AudioParam と GainNode](https://www.oxxostudio.tw/articles/201509/web-audio-api-audioparam-gainnode.html)

**FM・音色**
8. [Cycling '74: Synthesis Tutorial 5 — FM](https://docs.cycling74.com/api/latest/max8/tutorials/06_synthesischapter05)
9. [DecentSampler: How to use FM synthesis](https://decentsampler-developers-guide.readthedocs.io/en/1.21.1/topic-how-to-use-fm-synthesis.html)
10. [Attack Magazine: FM electric piano](https://www.attackmagazine.com/technique/tutorials/fm-electric-piano/)
11. [Sound On Sound: Synthesizing bells](https://www.soundonsound.com/techniques/synthesizing-bells)
12. [Sound On Sound: Synthesizing brass instruments](https://www.soundonsound.com/techniques/synthesizing-brass-instruments)
13. [Sound On Sound: Synth School part 2](https://www.soundonsound.com/techniques/synth-school-part-2)
14. [Sound On Sound: Synthesizing strings and string machines](https://soundonsound.com/techniques/synthesizing-strings-string-machines)
15. [MusicRadar: Recreate the Solina String Ensemble](https://www.musicradar.com/how-to/synth-string-synth-choir)
16. [Sound On Sound: Synthesizing tonewheel organs part 1](https://www.soundonsound.com/techniques/synthesizing-tonewheel-organs-part-1)
17. [DeepMind parameter guide: Arpeggiator](https://cdn.jsdelivr.net/npm/patchwork-deepmind@0.3.0/skills/deepmind-parameter-guide/sections/arp-sequencer.md)
18. [Bela: Virtual string synthesis (Karplus–Strong)](https://learn.bela.io/tutorials/pure-data/audio/virtual-string-synthesis)
19. [Soundtrap: Bitcrusher](https://blog.soundtrap.com/how-to-use-bitcrusher-like-a-pro/)
33. [Beat Kitchen: Bass design and the low end](https://beatkitchen.io/guides/electronic-music/04-bass-design/)
34. [Syntorial: Sub bass](https://www.syntorial.com/tutorials/synth-quickie-sub-bass/)

**効果音・ゲーム**
20. [Soundfly: Laser sounds with a synth](https://flypaper.soundfly.com/produce/pew-pew-how-to-make-laser-sounds-with-a-synth/)
21. [Soundcy: How to write laser sounds](https://soundcy.com/article/how-to-write-laser-sounds)
22. [Cycling '74 forum: Create thunder sound](https://cycling74.com/forums/create-thunder-sound)
23. [Unison: How to create risers](https://unison.audio/how-to-create-risers/)
24. [MusicRadar: Synth sweep FX](https://musicradar.com/how-to/synth-sweep-fx)
25. [jsfxr のパラメーター解説](https://renickbell.net/doku.php?id=jsfxr)
26. [Morphic: How to make sound effects for games](https://morphic.com/resources/how-to/how-to-make-sound-effects-for-games)
27. [Giant Bomb: Reward sound](https://giantbomb.com/wiki/Concepts/Reward_Sound)
28. [UX sound design（長さ・音量階層・音程の向き）](https://claudeskills.info/skills/guia-matthieu/clawfu-skills/ux-sound-design/)
29. [Game Audio Principles（カテゴリと優先度）](https://skills.sh/vudovn/antigravity-kit/game-audio)
30. [警報音の規格 IEC 60601-1-8 の解説](https://mspindy.com/technical-articles/using-audible-alarms-in-medical-equipment-iec-60601-1-8/)
31. [Designing Sound in SuperCollider: Creaking door](https://en.wikibooks.org/wiki/Designing_Sound_in_SuperCollider/Creaking_door)
32. [NESdev: APU basics](https://nesdev.org/wiki/APU_basics)
35. [iZotope: 8 creative reverb effects](https://www.izotope.com/en/learn/8-creative-reverb-effects-for-sound-design)
36. [OBS: Compressor filter（ダッキング設定）](https://obsproject.com/kb/compressor-filter)
37. [Giant Bomb／OpenGameArt などの素材ページ（回復・炎の音。作り方の数字はほぼ無く、参考のみ）](https://opengameart.org/content/magic-words-healing-sound-effect)

**調査上の注意**: 次のページは本文を読めなかった／数字が無かったため数字には使っていない — Violet Recording（UI サウンド・足音。機械的に取得を拒否）、A Sound Effect の魔法 SE（動画のみ）、OpenGameArt の炎（説明なし）。魔法の種類別（炎・氷・雷・光・闇）のレシピは、記事に数字が無いため**補**（ノイズの色とフィルターの動き、FM の非整数比、音の向きなど、複数の記事の一般論から組み立てた）。耳で確かめて調整すること。
