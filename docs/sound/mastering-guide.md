# マスタリングの手引き（2026-10-11 調査）

ネットの解説（文末の40件）と、手元の ffmpeg 6.1.1 での実験をもとに、**書き出し段（`tools/composer/song-lib.mjs` の master 段）をプロ水準に近づける道すじ**をまとめた。文章は写さず、数字と考え方だけを借りている。

**注意**: 本文を読めたページの数字は「出」、検索の要約や一般的な目安は「補」。**どの数字も出発点で、最後は耳（と A/B）で決める**。ffmpeg の例は、実際に短いテスト音で動かして**構文が通ること・数字が動くこと**を確かめたものに「検証済み」、確かめていないものに「未検証」と付けた。テスト音は合成音なので、音質の良し悪しまでは確かめていない。

## 0. 要点（先に結論）

1. マスタリングは「ミックスの直し」ではなく**最後の整え**。濁り・バランス・ぶつかりは直せない（ミックスや編曲に戻す）。動かすのは EQ ±1.5〜3dB、圧縮 GR 1〜2dB、リミッター GR 1〜4dB くらい（出）。
2. 順番は **ゲイン余白 → 掃除（HPF・LPF）→ EQ → 低域モノ化・M/S → 軽い圧縮（接着）→ サチュレーション／クリッパー → リミッター → ラウドネス測定 → ディザ → 書き出し**。幅を変える処理はリミッターの後ろに置かない（出）。
3. **音量の基準は用途で決める**。配信は -14〜-16 LUFS・-1 dBTP。ゲームは据え置き機の全体ミックスで -24、携帯・モバイルで -18 LUFS（出）。AES の「音楽は -16」も使える。**うちのゲームBGMは -16 LUFS を軸**にし、場面で ±2 まで。
4. うちの master 段の弱点は主に 5 つ。①リミッターがオーバーサンプリングなし（真のピークが測られない）②音量合わせが「リミッターの手前」で測られ、仕上がりが目標より小さくなる（`punk-guide.md` §9-3 で目標 -10 が -11.7 になった）③`extrastereo` が低音まで広げる ④ハイパス・ローパス・EQ・ティルトが無い ⑤ディザが無い。**どれも ffmpeg だけで直せる**（§5・§6）。
5. ゲームの容量予算は 128 メガビット（約 16 MB）。**曲をそのまま同梱するのは無理**なので、マスタリングの成果は「書き出し WAV（確認用）」と「ゲーム内の曲ごとの音量補正表・出口バスの設定」の両方に反映する（§7）。
6. 実装は「プリセット `--master-preset`」にまとめると使いやすい（§8 に 11 個の提案）。

## 1. 工程の順番と、それぞれの目的

| # | 工程 | 目的 | 数字（出／補） | ffmpeg |
|---|---|---|---|---|
| 0 | ゲイン余白 | 後ろの処理に余裕を作る | ミックスの山 -6〜-3dBFS、約 5dB の余白（出）。リミッターは外して受け取る | `volume=` |
| 1 | 掃除（HPF／LPF） | 聞こえない超低域・超高域を捨てる | HPF 20〜30Hz（補）、LPF 18〜20kHz（補。ローファイは 8〜12kHz） | `highpass` `lowpass` |
| 2 | 広い EQ | 全体の色合い。**ごく小さく** | ±0.5〜1.5dB が基本、最大 3〜4dB（出）。狭い数 dB はミックスへ戻す | `equalizer` `bass` `treble` `firequalizer` |
| 3 | 低域のモノ化 | クラブ・スマホ・モノ合成で低音が消えない | 100〜150Hz より下をモノ（出。100〜120 と 120〜150 の幅あり） | `acrossover` `pan` |
| 4 | M/S の調整 | 中央は締め、外側は開く | サイド HPF 120〜150Hz、サイド高域シェルフ +1〜4dB／10kHz（出） | `stereotools` |
| 5 | 軽い圧縮（接着） | 曲をまとめる | 2:1〜（最大 4:1）、GR 1〜2dB（出）、アタック遅め（20〜100ms）（出＋補） | `acompressor` `mcompand` |
| 6 | サチュレーション | 倍音で小さなスピーカーでも低音が聞こえる | ごく軽く、2 倍以上のオーバーサンプリング（出） | `asoftclip` `aexciter` |
| 7 | クリッパー | 速い山（キック・スネア）を丸め、リミッターを楽にする | 1〜2dB 分（出）。HPF の後ろ。リミッターの前（出） | `asoftclip` |
| 8 | リミッター（最後） | 天井を決めて音量を上げる | GR 5〜6dB 以下（出）、リリース 50ms 前後、真のピーク -1 dBTP | `alimiter` |
| 9 | 測定 | LUFS・真のピーク・LRA・PLR | 配信 -14、ゲーム -16 前後。PLR 9 未満は潰れ気味（既存文書） | `ebur128=peak=true` |
| 10 | ディザ | 16bit に落とす量子化ノイズを散らす | 三角(TPDF)＋高域寄りの整形が無難（補）。最後に 1 回だけ | `aresample=dither_method=` |
| 11 | 書き出し | 用途別の形式 | 下の §7 | `-c:a` |

順番の考え方（出）: 共鳴の掃除 → 広い音色 → 幅 → 接着の圧縮 → リミッター。圧縮は音色が整った信号に反応させるので EQ の後ろ。クリッパーは EQ の後・リミッターの前。

## 2. ラウドネスの基準

### 2-1 配信・放送・ゲーム
| 先 | 統合ラウドネス | 真のピーク | 出典メモ |
|---|---|---|---|
| Spotify・YouTube・Tidal・Amazon | -14 LUFS | -1 dBTP（Spotify は上げすぎなら -2） | 出 |
| Apple Music | -16 LUFS | -1 dBTP | 出 |
| Deezer | -15 LUFS | -1 dBTP | 出 |
| AES TD1008（配信向けの推奨） | 音楽 -16 LUFS | -1 dBTP | 出 |
| 放送 EBU R128 | -23 LUFS（±0.5） | -1 dBTP | 出 |
| 据え置きゲーム機（PlayStation の資料） | -24 LUFS（±2 LU） | -1 dBTP、LRA 20 以内 | 出 |
| 携帯・モバイルゲーム（同） | -18 LUFS（±2 LU） | -1 dBTP | 出 |
| モバイルの端末スピーカー（解説記事） | 約 -16 LUFS | — | 出 |
| ヘッドホン・静かな部屋（モバイル） | -24 LUFS／うるさい場所で -18 | — | 出 |
| Flight Simulator（全体ミックス） | -24 LKFS（±2） | -2 dBTP | 出 |

- 配信で -14 より大きい曲は**下げられるだけ**で、潰れた音が残る。-14 LUFS・ダイナミックレンジ約 8dB のほうが、-8 LUFS・約 1dB より勝つ、という例がある（出）。
- ゲームは**全体ミックス（音楽＋効果音＋声）で基準を満たす**もの。音楽だけを -24 にするのではない。Wwise の解説は「マスター段は最初は安全用のリミッター（山 -1〜-2 dBFS）として使い、EQ は ±3dB 以内、直すべき大きな問題はミックスで」と述べる（出）。
- 会話は BGM より大きく（既存文書の目安: 声 -12、BGM -16、効果音 -16）。うちは BGM を **-16 LUFS 軸**にしておけば、効果音が重なっても割れにくい。

### 2-2 「潰れ具合」の物差し（PLR）
- ピーク−統合ラウドネス（PLR）や、山と短時間ラウドネスの差（PSR）で見る。**PSR は 8 以上**を目安にする（出）。
- ダイナミックレンジ（ピークとラウドネスの差）の見方（出）: 4 未満＝潰れ／4〜6＝つぶし気味／6〜9＝密／**9〜12＝健全（推奨）**／12 以上＝パンチあり。曲の中でも、静かな所 10〜14、ヴァース 8〜12、サビ・ドロップ 6〜10、ドロップ直前のビルド 6〜8、が目安。
- ジャンル別の目安（出）: クラシック・ジャズ・アコースティック 12〜16／ロック・ポップ 8〜12／EDM・ヒップホップ 6〜10／わざと潰す系（一部のメタル・ハイパーポップ）4〜6。

## 3. ジャンル別マスタリングパターン

**読み方**: LUFS は「配信用に作るとき」の目安（出＋補）。**ゲーム用の書き出しは §3-2 の「ゲーム用に読み替え」を使う**。基本の部品は §5 のレシピ（R1〜R8）に名前を付けてあり、表の ffmpeg 欄は「どのレシピを、どの数字で」を書いた。

### 3-1 ジャンル別（15 パターン）
| # | ジャンル | 目標 LUFS | TP | EQ | コンプ／マルチバンド | 広がり・低域 | ffmpeg の要点 |
|---|---|---|---|---|---|---|---|
| 1 | クリーンギターのロック／ポップロック | -11〜-9（配信）。うちの `clear-guitar-rock` は -10 | -1 | 100Hz 付近を +0.5、300Hz 付近 -1、高域シェルフ +1（補） | 接着 2:1、GR 1〜2、アタック 30ms、リリース 150〜250ms | サイド HPF 150、slev 1.2〜1.3、低域モノ 140 | R1＋R2＋R3(1.25)＋R4(2:1)＋R7 |
| 2 | ハードロック／歪みギター | -10〜-8 | -1 | 箱鳴り 300Hz 付近 -1〜-2、2〜4kHz は +1 まで（出：歪みギターは 1〜3kHz に存在感） | 接着 2:1〜3:1、GR 2、アタック 20〜30ms | ギター 2 本を左右に、低域は中央。slev 1.2 | R4(3:1)＋R6(1dB)＋R7 |
| 3 | メタル | 配信 -9〜-7（出では -7〜-5 まで攻める人もいるが、-14 前後に正規化されるだけなので、うちは -10〜-9 止まりを推奨） | -0.3〜-1（出） | パームミュートの溜まりを 80〜200Hz の動的 EQ で（出）、箱鳴り 250〜400Hz -1〜-2 | マルチバンド（低域だけ）、クリッパーでキック・スネアの山を 1〜2dB 削ってからリミッター（出） | サイド HPF 120〜150（出）、低域モノ 150 | R5(低域のみ)＋R6(1〜2dB)＋R7(GR 3〜5) |
| 4 | パンク／疾走ロック | -10（うちの `punk-run`） | -1〜-1.5 | 4〜8kHz の「空気」が足りない傾向 → 高域シェルフ +1（既存文書: 録音より約 4dB 少なかった） | 浅い（GR 1〜2）。潰すと割れる（`punk-guide.md`） | ギター ±0.9、slev 1.2 | R3＋R4(2:1)＋R6＋R7、仕上がり -10 を閉ループで合わせる(§8-4) |
| 5 | ポップ／J-POP 風 | -12〜-10（出：-12〜-14／-10 前後の幅） | -1 | 200〜400Hz の濁りを -1、主旋律の帯域 2〜4kHz +0.5、10kHz+ に +1（出） | 接着 2:1、GR 1〜2、パラレルで厚み（補） | slev 1.3、低域モノ 120〜140 | R2＋R3(1.3)＋R4＋パラレル(R9) |
| 6 | ジャズ（生楽器の小編成） | -18〜-14（出：-16〜-18） | -1 | 基本は触らない。必要なら 0.5dB 単位。サチュレーションは使わない（出） | ほぼ無し。ピークだけ 2:1（高いしきい値）（出） | 広げない（slev 1.0〜1.1）。低域モノ 100 | R1＋R4(1.5:1、GR≤1)＋R7(GR≤2)。クリッパー無し |
| 7 | クラシック／オーケストラ（映画風） | -20〜-16（出：-18〜-14 の幅。ダイナミクス優先） | -1〜-2 | 300Hz と 3kHz を小さく削る、最高域・最低域をわずかに足す（出）。ティルトは -0.5dB/oct くらいまで | 圧縮は「ごく控えめ」（出）、マルチバンドは各帯が触れる程度（出）。静かな所のボリューム自動化は 3〜5dB 以内（出） | slev 1.0、リバーブの尾を保つ | R1＋R8(ティルト -0.5)＋R4(1.5:1)＋R7(GR 1〜2、最大音の所でちょうど効く程度（出）) |
| 8 | EDM／ダンス | -9〜-6（出：ドロップで -6 前後。-2 は割れる）。配信用は -9〜-8 が無難 | -1 | キックの基音 60〜70Hz、サブは 25〜30Hz 以下を捨てる | クリッパー→リミッター（GR 2〜4）。サイドチェイン感は編曲で | **サブは必ずモノ（〜150Hz）**。高域のサイドを +2〜3dB | R1＋R2(150)＋R3(slev 1.4)＋R6(2dB)＋R7 |
| 9 | ヒップホップ／ビート系 | -10〜-8（出） | -1 | 低域の帯域を 40〜80Hz に集め 200〜400Hz を整理 | 接着 2:1〜4:1、GR 2〜3、アタック遅めでキックの頭を残す | 低域モノ 120〜150 | R2＋R4(3:1、アタック 30ms)＋R6＋R7 |
| 10 | ローファイ／チル | -14〜-12（補） | -1.5 | **LPF を 8〜12kHz に落とす**（出では「高域を落として古いテープ感」）、低中域 200〜400Hz を +1 | 軽い圧縮 1.5:1、サチュレーション多め（出：温かみ） | 広げない（slev 0.9〜1.0）、低域は中央 | R1(LPF 10000)＋R6(軽く)＋R4。ワウ・フラッターは「ピッチのゆれ」（未検証：`aphaser` や `vibrato` で近似） |
| 11 | アンビエント／パッド主体 | -18〜-14（出：-14〜-11 を狙う人も。山は -3dBFS 以下） | -3〜-1.5 | 低域のこもり（200〜300Hz）を -1〜-2、高域をやわらかく | ほぼ無し（出：山の少ない曲を 0dB に近づけない）。ゆるいリミッターのみ | 広め（slev 1.3〜1.5）でも、低域モノ 120 は守る | R1＋R3(1.4)＋R7(GR≤1.5)、LUFS は低め |
| 12 | ゲーム：フィールド・町（穏やか） | **-17〜-16** | -1.5 | 1〜4kHz を -1（効果音・会話の居場所）（既存文書） | 浅い。natural の曲はさらに浅く | slev 1.1〜1.2 | R1＋R2＋R4(1.5:1)＋R7(GR≤2) |
| 13 | ゲーム：戦闘 | **-15〜-14**（場面でいちばん上） | -1.5 | 中域〜低中域（300〜500Hz）と 2〜3kHz を -1〜-2（効果音の技の音と競合）（出） | 接着 2:1〜3:1、GR 2、クリッパー 1dB | slev 1.2、低域モノ 150 | R4(3:1)＋R5(低域)＋R6(1dB)＋R7 |
| 14 | ゲーム：ボス・クライマックス（オーケストラ＋ロック） | **-15〜-14** | -1.5 | 低域の溜まりを動的 EQ、トップ 10kHz+ を +1 | 接着＋低域のみのマルチバンド | slev 1.3、サブはモノ | R5＋R4＋R6＋R7、PLR 10 以上を確認 |
| 15 | ゲーム：ダンジョン・洞窟・不穏 | **-19〜-17** | -2 | 高域を丸く（LPF 14〜16kHz）、200〜300Hz を整理 | 浅い、ダイナミクス優先（LRA が広くてよい） | 広め（残響を活かす）。低域モノ | R1(LPF 15000)＋R3(1.3)＋R7(GR≤1.5) |
| 16 | ゲーム：レトロ風（ファミコン〜スーファミ風の「調」） | -16（場面に合えば -15） | -1.5 | 高域を丸める LPF 10〜14kHz（出：SNES 風はガウス補間＋ローパス）、必要なら 8〜16bit ふうの荒さを足す | 圧縮ほぼ無し（矩形波は元々平ら） | 広げない（ほぼモノ寄り） | R1(LPF)。「荒さ」は `aresample=` の低いレートに落として戻す（未検証） |
| 17 | 和風（和楽器＋弦） | -17〜-15 | -1.5 | 3〜5kHz の撥音のきつさを -1（補）、200Hz 付近を整える | 浅い、クラシックに近い | slev 1.1。琴・笛の定位は編曲で | R1＋R4(1.5:1)＋R7 |
| 18 | ピアノソロ・ギターソロ（静かな曲） | -18〜-16 | -2 | 3kHz 付近のきつさを -1、100〜200Hz を整理 | ほぼ無し | 広げすぎない（slev 1.0〜1.2）、残響は編曲で | R1＋R7(GR≤1) |

### 3-2 ゲーム用に読み替える
- 上の表の LUFS は配信向け。**うちのゲーム用の書き出しは「-16 LUFS を軸に、戦闘・ボスだけ +1〜2、ダンジョン・静かな曲だけ -1〜-3」**にする（表の #12〜#18 の太字）。
- 理由: 現状の全 58 曲は統合ラウドネスが -26.2〜-3.8 LUFS（差 22.4dB、`docs/decisions.md`）で、場面が変わるたびに音量が飛ぶ。マスタリングの数字より前に、**曲どうしを ±2 LU に収める**ほうが体感への効きが大きい。
- LRA（強弱の幅）はゲームでは広くてよいが、ループ曲が 1 曲の中で聞き取れないほど小さくなる所があると、効果音に埋もれる。静かな所の下限は -26 LUFS（短時間）くらいまで（補）。
- 配信のように「大きいほうが勝つ」ことは無い（ゲーム内は固定の音量補正で鳴る）。**音量を稼ぐために潰す理由が無い**。リミッターは安全用の薄いものでよい。

## 4. うちの現状の master 段との差

現状（`song-lib.mjs` 74〜86 行）: `acompressor`（natural: threshold 0.2・ratio 2.2・attack 8・release 140・makeup 1.5／それ以外: threshold 0.12・ratio 4・attack 4・release 90・makeup 2）→ （`--widen` があれば）`extrastereo=m=widen` → LUFS を測る → `volume` で目標へ → `alimiter=limit=0.84:attack=3:release=60:level=false` → 48kHz・16bit・WAV。その前に、`--space` で畳み込みリバーブ（`afir`）を足せる。

| 項目 | 今 | プロの定石 | 差の大きさ・影響 |
|---|---|---|---|
| ハイパス／ローパス | 無し | HPF 20〜30Hz、LPF 18〜20kHz（ジャンルで変える） | 聞こえない超低域がリミッターの余白を食う。小さいが確実に効く |
| EQ／ティルト | 無し（`punk-run` の高域不足は編曲側で補った） | 広い EQ ±0.5〜1.5dB、ティルト ±0.5dB/oct | 帯域の偏りは編曲で直しているが、最後の仕上げの手段が無い |
| 低域のモノ化 | 無し | 100〜150Hz 以下はモノ | `extrastereo` で低音まで広がると、モノ再生で低音が痩せる可能性 |
| 広げ方 | `extrastereo`（全帯域のサイドを倍率） | サイドだけの HPF＋サイド高域を広げる（M/S） | 検証済み: 1kHz のサイドは +3.5dB、同時に 50Hz のサイドも同じ +3.5dB。低音が広がる |
| 圧縮のかけ方 | ratio 4・attack 4ms（natural 以外） | バス接着は 2:1、attack 20〜100ms、GR 1〜2dB | 速いアタックでキックの頭が潰れる。つぶし気味になりやすい |
| マルチバンド | 無し | 低域だけの圧縮など（2〜3 帯域） | 低域の暴れ（メタルのパームミュートなど）を直せない |
| クリッパー／サチュレーション | 無し | 速い山を 1〜2dB 丸めてからリミッター | リミッターが山を直接押さえるので、ドラムの歯切れが落ちやすい |
| リミッター | `alimiter` limit 0.84（約 -1.5dBFS のサンプルピーク）、オーバーサンプリング無し | 真のピーク（-1 dBTP）で止める、オーバーサンプリング | 検証済み（下）。サンプルピークだけでは真のピークが超える場合がある |
| 音量合わせ | 「圧縮後・リミッター前」を測って、目標との差分をゲイン | リミッター後の値で合わせる | リミッターが GR を出すぶん、仕上がりは目標より小さくなる（`punk-guide.md`: 目標 -10 → 実測 -11.7） |
| ディザ | 無し（float → 16bit が丸めだけ） | 16bit に落とす最後に 1 回、三角（TPDF）かノイズシェイプ | 静かな残響の尾・フェードで量子化ひずみが出る可能性。小さい |
| 後ろの確認 | `analyzeMix`（割れ・低音・強弱・無音） | LUFS・TP・PLR・PSR・LRA・モノ互換の合否 | 数字をまとめて見る表が無い（`ai-composition-workflow.md` 提案 4 と同じ） |
| ループの継ぎ目 | 見ていない | 尾を先頭に重ねる／継ぎ目の段差検査 | ゲーム用に必須（§7） |
| `loudness.ts`（TS 側） | LUFS 測定と tanh のソフトクリップ（ceiling 0.97） | — | master 段とは別系統。数字（天井 0.97 と 0.84）が違うので、どちらがどこで使われるかを揃えると混乱が減る |

### 実験で確かめたこと（ffmpeg 6.1.1、合成のテスト音）
1. **サンプルピークが真のピークと一致しない**: 12kHz の正弦波（サンプルは ±0.99 で、真の山は 1.4 になる位相）を作ると、`ebur128=peak=true` は +3.5 dBTP。素の `alimiter`（limit 0.891）を通した後も **+2.1 dBTP のまま**。前後に `aresample=192000` と `aresample=48000` を挟むと **-1.0 dBTP** になった。現状の limit 0.84 は「天井 -1.5dBFS」の余白があるぶん通常は安全だが、リミッター単体では真のピークは保証されない。
2. **`extrastereo` は低音も広げる**（上の表）。`stereotools` で M/S に分け、サイドだけ HPF すれば、50Hz のサイドは約 -17dB まで下がり、1kHz は +1.9dB（slev 1.25）。
3. **`acrossover`（LR4）で 140Hz 以下をモノにする**と、50Hz のサイド成分は約 -35dB、1kHz のサイドと中央は 0.01dB 以内で保たれた。`lowpass`＋`highpass` の足し算（2 次）より、帯域の和が平らで安全。
4. **`asoftclip` の `oversample` を 2 以上にすると、ffmpeg 6.1 では出力が約 6dB 小さくなる**（-12.5 → -18.4 LUFS）。原因は未確認。回避: `oversample=1` のままにして、自分で前後に `aresample=192000`／`aresample=48000` を挟むとレベルは保たれた（検証済み）。
5. `asoftclip=type=tanh` は**しきい値より小さい音にも効く**（しきい値 1 でも -12.5 → -13.1 LUFS）。「山だけ丸める」ではなく穏やかなサチュレーション。山だけ丸めたいなら `type=cubic` など別の型を耳で比べる（未検証）。
6. **`channels=c0`／`c1` は期待どおり動かない**。`stereotools=mode=lr>ms` の後は、**`FL` が Mid、`FR` が Side**（`channels=FR` だけを HPF して確認した）。`c0`・`c1` と書くと両方に効いてしまった。
7. `loudnorm` 単独は「dynamic」で動き、音の動きを変える。`linear=true` の 2 パスは、目標にピークが収まるときだけ線形になる（出）。うちは**自前の測定→ゲイン→リミッター→再測定**のほうが、天井と音量を同時に管理しやすい。

## 5. ffmpeg の具体例（レシピ集）

凡例: **検証済み** = 6.1.1 で実際に通し、数字が動くのを確認。**未検証** = 構文は確認したが効果は聞いていない、または未実行。
シェルの `-af "..."` に書くときの例。Node の `execSync` で書くときは、`,` のエスケープと `\` の扱いに注意（`mcompand` の `args` の中の `,` は `\,` が必要）。

### R1 掃除（HPF・LPF）— 検証済み
```
highpass=f=25:poles=2,lowpass=f=19000:poles=2
```
ローファイは `lowpass=f=10000`。ゲーム全般は 25Hz で十分。

### R2 低域のモノ化（140Hz 以下）— 検証済み（filter_complex）
```
acrossover=split=140:order=4th[lo][hi];
[lo]pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1[lom];
[lom][hi]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo
```
`split` を 100〜150 で動かす。サブを強く守りたい EDM は 150。ジャズは 100。

### R3 M/S で幅を作る（低域は広げない）— 検証済み
```
stereotools=mode=lr>ms,highpass=f=150:poles=2:channels=FR,stereotools=slev=1.25:mode=ms>lr
```
`FR`＝Side を HPF（低域のサイドを捨てる）→ `slev` でサイドを持ち上げる。今の `--widen` の代わりに使う（`slev` ≒ `widen`）。サイド高域だけを足したいときは、`equalizer=f=10000:t=q:w=0.7:g=2:channels=FR` を M/S の中に足す（構文のみ確認、効果は未検証）。

### R4 接着の圧縮（バス）— 構文は検証済み、数字は出発点
```
acompressor=threshold=0.18:ratio=2:attack=30:release=200:knee=4:makeup=1:detection=rms:link=average
```
`threshold` は線形（0.18 ≒ -15dBFS）。GR は 1〜2dB で止める。ジャズ・クラシックは `ratio=1.5:threshold=0.3`。メタル・ヒップホップは `ratio=3:attack=30`。**パラレル**にするときは `acompressor` の `mix=0.35` が使える（`mix` オプションあり）か、`asplit` で分けて `amix` の `weights=1 0.35`（後者は検証済み）。

### R5 マルチバンド（低域だけ、など）— 構文は検証済み
```
mcompand=args='0.02\,0.2 6 -70/-70\,-30/-30\,0/-6 150 | 0.015\,0.15 6 -70/-70\,-30/-30\,0/-5 3000 | 0.005\,0.08 6 -70/-70\,-30/-30\,0/-4 20000'
```
- 各帯域は `アタック,ディケイ（秒） ソフトニー 伝達点（入力dB/出力dB） 上の分割周波数` の並び。上の例は 150Hz／3kHz で 3 分割（0dB 入力で 6/5/4dB 下がる＝効かせすぎ。**まず伝達点を直線に近い `-20/-20,0/-2` から**）。
- 「帯域をなるべく少なく、まず 2〜3」が定石（出）。割る位置は、主旋律の基音・主な倍音と重ならない所（出）。目安: 低域 〜150Hz／中域 150Hz〜3kHz／高域 3kHz〜。接着用の出発点は 2:1・アタック 100ms・リリース 100ms（出）。
- `mcompand` は帯域ごとのレシオやニーを細かく選べず、ソフトニーの値だけ。本格的な動的 EQ は `adynamicequalizer`（6.1 にあり。検証済み＝構文のみ）で代用する。メタルの低域: `adynamicequalizer=threshold=...:dfrequency=120:tfrequency=120:ratio=2:range=4:mode=cut`（数字は未検証）。

### R6 クリッパー（山を丸める）— 検証済み（手動オーバーサンプル版）
```
volume=3dB,aresample=192000,asoftclip=type=tanh:threshold=1:oversample=1,aresample=48000
```
`volume` を上げるぶんだけ山が丸まる。**1〜2dB 分**の強さにとどめ、クリップ後にもう一度音量を測る。`oversample` は 1 のまま（上の実験 4）。

### R7 真のピーク対応のリミッター — 検証済み
```
aresample=192000,alimiter=limit=0.891:attack=5:release=80:level=false,aresample=48000
```
- `limit` は線形。0.891 ≒ -1.0 dBFS、0.841 ≒ -1.5dB、0.794 ≒ -2dB。出力後に `ebur128=peak=true` で TP を見て、超えていたら `limit` を 0.5dB 下げて 1 度やり直す。
- リリースは **50ms 前後**（出：歪みが少なく大きく聞こえる）。ゆっくり（250ms〜）にすると透明、5〜10ms は音量優先だが歪む（出）。`asc=1`（自動の戻り）は未検証。
- 圧縮・クリップで山を先に削り、リミッターの GR は 5〜6dB 以下（出）、ゲームは 3dB 以下を目指す。

### R8 ティルト（明るさの傾き）— 検証済み
```
firequalizer=gain='-0.5*log(max(f\,20)/650)/log(2)':zero_phase=on
```
650Hz を軸に、1 オクターブ上がるごとに -0.5dB（暗く）。符号を逆にすれば明るく。`max(f,20)` を忘れると `log(0)` で失敗する（検証済み）。±1dB/oct を超えない。`zero_phase=on` は位相がずれないが遅延（約 10ms）が付く。

### R9 マッチング EQ（参考の周波数カーブに寄せる）— 検証済み（構文）
```
firequalizer=gain_entry='entry(63,0.4);entry(125,3.0);entry(250,-0.1);entry(1000,2.0);entry(8000,1.5);entry(16000,0)':zero_phase=on:delay=0.05
```
`entry` を、**うちの曲と目標の 1/3 オクターブ差から Python で作って**差し込む（§8-9）。作り方（検証した試作）: ①曲全体を `-ac 1 -ar 48000` で読む ②FFT して 1/3 オクターブ帯ごとの量（全体に対する dB）を出す ③目標の値との差に **amount（30〜50%）**を掛け、**±3dB で切る** ④`entry(中心Hz, dB)` に並べる。

### R10 ディザ（16bit への変換）— 検証済み
```
aresample=osf=s16:dither_method=triangular_hp
```
候補: `triangular`（TPDF）／`triangular_hp`（高域寄りで耳に付きにくい）／`shibata`／`low_shibata`（ノイズシェイプ）。これをフィルターグラフの最後に 1 回だけ入れ、他に `aresample`／`volume` を後ろに置かない。**ループ曲は、ディザの乱数が先頭と末尾で違っても聞こえない程度**（補）。

### R11 全体をつなげた例 — 検証済み（合成音で LUFS -14.2、TP -4.8）
```
# 測る（前段だけ）
[0]highpass=f=25:poles=2,lowpass=f=19000:poles=2,
   acrossover=split=140:order=4th[lo][hi];
   [lo]pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1[lom];[lom][hi]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo,
   stereotools=mode=lr>ms,highpass=f=150:poles=2:channels=FR,stereotools=slev=1.25:mode=ms>lr,
   acompressor=threshold=0.18:ratio=2:attack=30:release=200:knee=4:makeup=1,
   ebur128=peak=true
# 書き出し（測った差分を volume に）
... ,volume=<差分>dB,aresample=192000,asoftclip=type=tanh:threshold=1:oversample=1,
   alimiter=limit=0.891:attack=5:release=80:level=false,aresample=48000,aresample=osf=s16:dither_method=triangular_hp
```
注意: 仕上がり -14.2 は目標 -14.0 より 0.2 小さい（ソフトクリップとリミッターが削るため）。**書き出し後にもう一度測り、±0.3 を超えたら差分を足して 1 回やり直す**（§8-4）。

### その他の ffmpeg フィルターの位置づけ
| フィルター | 使い道 | 判断 |
|---|---|---|
| `loudnorm` | EBU R128 の正規化（dynamic／linear） | 動画向き。**マスタリングの音量合わせには使わない**（動きが変わる）。測定の `print_format=json` は参考になる |
| `dynaudnorm` | 小刻みに音量をそろえる | 音楽には向かない（強弱を壊す）。使わない |
| `speechnorm` | 声の正規化 | 使わない |
| `adeclick`／`adeclip` | クリックやクリップの修復 | **ループ継ぎ目のクリック除去**や、割れた素材の応急（未検証）。マスタリング本体には要らない |
| `crossfeed`／`bs2b` | ヘッドホン用に左右を混ぜる | **聞き比べ用の確認**に使える（書き出しには使わない） |
| `stereowiden`／`haas` | 遅延で広げる | モノ互換が悪い（遅延は櫛形のへこみ）。使わない（M/S を使う） |
| `aexciter`／`asubboost` | 高域の倍音、サブの持ち上げ | 構文のみ確認。効果は未検証。`aexciter` は `freq=6000`・`amount=0.3〜0.5` から、空気（8kHz+）の足しに使えるか耳で |
| `adynamicequalizer` | 動的 EQ（帯域が超えたときだけ削る） | 6.1 にあり。メタル・戦闘曲向け（未検証） |
| `alimiter` の `asc` | 自動の戻り | 未検証 |
| `ebur128=peak=true` | LUFS・LRA・真のピークの測定 | 検証済み（すでに使っている） |
| `astats` | RMS・クレスト・ピーク | 検証済み。PSR は `ebur128` の Short-term の最大値を読む（未実装） |

## 6. 低域・広がり・サチュレーションの数字（まとめ）

- **低域のモノ**: 〜100〜150Hz。100〜120Hz に収めるのが基本（出）、150Hz 近辺までのこともある（出）。サイド HPF は 120〜150Hz（出）。300Hz まで上げて低中域を中央に集める人もいる（出）。
- **サイド高域**: シェルフ +1〜4dB／10kHz 付近（出）。**中央を同時に -1〜-2 すると効きやすい**（補、既存文書）。
- **ハース**（片側を 10〜30ms 遅らせる）はモノで櫛形にへこむ → 使わない。
- **ティルト**: ±0.5dB/oct 程度の緩い傾き。軸 650Hz 前後（補）。
- **ソフトクリップ**: 1〜2dB 分のゲインを足してから丸める（出）。低域を守るため HPF 後か、高域だけにかける。最大 6dB 分の余裕が出るという解説もあるが（出）、うちの合成音の実験では 3dB 分で音は十分変わるので、**1〜2dB から**。
- **リミッターのリリース**: 50ms 付近（出）。GR は 5〜6dB 以下（出）。
- **真のピーク**: 0 dBFS のサンプルが +0.6 dBTP になることがあり、強く潰した曲ではサンプルと真のピークが 1〜2dB 違う（出）。天井は -1 dBTP が配信の共通、Amazon は -2 を勧める（出）。**ゲームは OGG／MP3 に変換するので -1.5〜-2** を使う（補）。
- **ディザ**: 24bit→16bit など**語長を落とす最後の 1 回だけ**。うちは float から 16bit なので、書き出しの最後に R10。

## 7. ゲーム音声としての注意

### 7-1 形式・容量
- **WAV 48kHz 16bit** は確認用の正本。ゲームへの同梱は **OGG Vorbis**（音楽・長い環境音は OGG、短い効果音は WAV）が定石。MP3 は先頭に無音のパディングが付き、**ループの継ぎ目に隙間が出る**ので避ける（出）。MP3→OGG の再変換は劣化が重なるので、元の WAV から作る（出）。
- OGG の品質の目安（`libvorbis -q:a`）: 手元の 12 秒テスト音で、q3＝約 127KB（約 85kbps）、q5＝約 160KB（約 107kbps）、q6＝約 205KB（約 137kbps）。音楽のゲーム同梱は **q5 前後**（ブラウザゲームの例では、重要な音楽に q7、中程度に q5、重要度の低い物に 22.05kHz ＋ q5 などの階段（出））。**1 分の曲で約 1MB に収めたいなら q1 付近（64kbps）か、サンプルレートを下げる**（出）。
- **容量予算は dist/ 全体で 128 メガビット（約 16MB）**（`CLAUDE.md`）。58 曲を q3（約 85kbps）で 3 分ずつにすると 約 110MB で**大幅に超える**。したがって**同梱は「ゲーム内で今のように楽譜から鳴らす」ままが基本**。書き出し WAV は確認と、必要なら数曲だけの OGG 同梱（タイトル曲・ループが重要な曲）に使う。
- 再生は**ストリーミング**（長い曲を丸ごと読み込むと RAM を食う（出））。ブラウザでは Web Audio のデコード済みバッファか `<audio>`。短い効果音は読み込み済みで。
- サンプルレートは**ゲーム全体で 1 種類**（48kHz）にそろえる（再サンプルの劣化を避ける）（出）。

### 7-2 ループ
- 継ぎ目の理想は、**曲そのものが「頭と尾が音楽的に同じ状態」になるように作られていること**（小節の頭で切る、和音・ベース・リズムが同じ状態へ戻る）。つなぎ目の補正は最後の手段（出、議論あり）。
- 残響・シンバルの**尾は、先頭に重ねる**（テールラップ）。ディケイ 3 秒・120BPM なら約 1.5 小節。尾がレンダリングに入っていないと後から作れない（既存文書）。ffmpeg では **同じファイルを 2 つの入力として渡す**と動く: 検証済み
  ```
  ffmpeg -i song.wav -i song.wav -filter_complex \
   "[0]atrim=0:T,asetpts=PTS-STARTPTS[body];[1]atrim=start=T,asetpts=PTS-STARTPTS[tail];[body][tail]amix=inputs=2:normalize=0:duration=longest,atrim=0:T" loop.wav
  ```
  （T＝ループの長さ（秒）＝小節数×1小節の秒数。**1 つの入力を `asplit` で分ける書き方は、出力が 0.02 秒で切れて失敗した**）。重ねた所の音量が上がるので、**尾の始まりを少し絞る**（`afade`）か、重ねた後に再度測る。
- ドラムなど**打楽器は長いクロスフェードで二重に聞こえる**ので、最小の長さ（クリックが消える程度）にとどめる（出）。
- **試し聞き**: 継ぎ目を 3〜4 回つなげて、継ぎ目だけを 1 分以上聞く（6〜10 回の繰り返しで気になる欠点が分かる）（出）。ゲームエンジン上でも確かめる（エディタだけでは分からない）（出）。
- 自動チェック案（§8-10）: 先頭 20ms と末尾 20ms の波形の差（段差）、継ぎ目の前後 100ms の RMS 差、2 周つなげて `ebur128` の Short-term が継ぎ目で急に動かないか。
- OGG／WAV のループ指定: ゲーム側が「ループの始点・終点」を持てるなら、メタデータで（`LOOPSTART`／`LOOPLENGTH` を Vorbis コメントに入れる実装が多い。未検証）。

### 7-3 音量
- 出口のバスと曲ごとの補正で**場面間の音量差を ±2 LU に**（§3-2）。曲ごとの音量補正表（`bgm-loudness` から計算）を入れるのが最優先。
- 戦闘曲は 1〜4kHz を 2〜3dB 引く（既存文書）か、技の効果音が鳴る間だけ動的に引く（`adynamicequalizer` では曲の書き出しの中でしか使えない。ゲーム内の再生では Web Audio 側で）。
- モバイルの端末スピーカーは低音が再生できないので、**100Hz 以下だけで成り立つ低音は聞こえない**。ベースの 2〜4 倍音（200〜800Hz）が大切（補）。小さなスピーカーでの確認は必須。
- 子ども向けは -28 LUFS 前後まで下げ、うるさい場所で -24 に上げる、という例がある（出）。うちの対象は一般向けなので -16 軸でよい。

## 8. 取り入れる提案（実装可能な単位・11個）

優先度順。ほとんどが `song-lib.mjs` の master 段の差し替えと、小さな Python／mjs で済む。**実装前に、短い曲 2〜3 本で A/B（耳）と数字（`analyze.py`）を確かめる**。

1. **プリセット `--master-preset <id>`**: `rock`・`metal`・`punk`・`pop`・`jazz`・`orch`・`edm`・`hiphop`・`lofi`・`ambient`・`game-field`・`game-battle`・`game-boss`・`game-dungeon`・`retro`。中身は表（§3-1）の数字（LUFS、TP 天井、HPF/LPF、低域モノ周波数、slev、接着の ratio／attack、クリップ量、ティルト、マッチング EQ の目標曲線名）を 1 つのオブジェクトにしたもの。`SOUND_SETS` の `master: { lufs, widen }` を `master: { preset?: string, lufs?, ... }` に広げ、個別に上書きできるようにする。
2. **真のピーク対応のリミッター（R7）**: `aresample=192000` の前後挟み＋`limit` を `--tp -1.0`（ゲームは -1.5）から決める。出力を `ebur128=peak=true` で測り、TP が天井を超えたら `limit` を 0.5dB 下げて再実行（最大 3 回）。
3. **低域のモノ化（R2）**: 既定で 140Hz（プリセットで 100〜150）。`--lowmono 0` で切れる。書き出し後に「100Hz 以下の L/R 相関」を測って警告（モノで痩せる曲の発見）。
4. **音量合わせを閉ループにする**: ①前段（HPF・M/S・圧縮・クリップ）だけで LUFS を測る ②ゲイン計算 ③リミッターまで通して書き出す ④書き出した WAV を測り直す ⑤目標との差が ±0.3 を超えたらゲインを補正して 1 回だけやり直す。現状の「仕上がりが目標より 1〜2 小さい」を解く。
5. **M/S ワイド（R3）で `extrastereo` を置き換える**: `--widen` の意味を `slev` に対応づける（1.0＝そのまま、1.3＝広い）。サイド HPF は 150Hz（`--side-hpf` で変更）。
6. **ソフトクリップ段（R6）**: プリセットの `clip: 0〜2`（dB）。手動オーバーサンプル版で。パンク・メタル・EDM・ヒップホップは 1〜2、ジャズ・クラシック・アンビエントは 0。ffmpeg 6.1 の `oversample` の 6dB 低下を避ける注意をコードのコメントに残す。
7. **ディザ（R10）と最後の整形**: float→s16 の最終変換だけ `aresample=osf=s16:dither_method=triangular_hp`。フィルターグラフの最後に置く。ループ曲は継ぎ目の確認後に。
8. **マルチバンドと動的 EQ（R5）**: プリセットの `mb: { lowOnly: true }` など、まず「低域だけ」の 2 帯域（150Hz 分割）から。メタルと戦闘曲に限定。GR 目標 ≤ 2dB。数字が決まるまでは**警告表示なしの任意機能**とし、効果は `analyze.py --bands` とクレストで確かめる。
9. **マッチング EQ（`tools/audio-check/match-eq.py`）**: 既存の `third-octave.py` の測り方（1/3 オクターブ・曲全体）を流用し、目標曲線（ジャンル別の平均。`docs/sound/data/` に数字だけ置く）との差に **amount 0.3〜0.5・±3dB・80Hz〜12kHz** の制限をかけて `firequalizer` の `gain_entry` 文字列を出力。master 段が呼ぶ。**参考録音は数字だけ**（`CLAUDE.md` 1-1）。amount を 1 にしない。
10. **ループの継ぎ目（`--loop` と `loop-check`）**: レンダリング時に尾を余分に出し（小節の整数倍＋尾 N 小節）、先頭に重ねる（§7-2 のレシピ）。書き出し後に自動チェック（先頭・末尾 20ms の差、継ぎ目 ±100ms の RMS 差、2 周つなげた Short-term の跳び）を行い、`warnings` に出す。
11. **ゲーム用の「音量補正表」と合否表**: ①`bgm-loudness.json` から、曲ごとに「-16 LUFS との差（dB）」を計算して `src/audio/` の表に入れ、再生時に掛ける（大きい曲を下げる方向。差が 3dB を超える曲は警告）②`master-report`: 書き出し WAV の I・TP・LRA・PLR・PSR（Short-term の最大との差）・L/R 相関・100Hz 以下の相関・継ぎ目チェックを 1 行で表示して○／要直し（`ai-composition-workflow.md` の提案 4「合否表」と統合）。

### 実装の順番の案
`4 → 2 → 3 → 5 → 7`（音量の正確さと安全）→ `11-①`（ゲーム内の飛びを減らす）→ `1`（プリセット化）→ `6 → 10 → 9 → 8`。

### 実装前に確かめること（未検証）
- 実際の曲（`punk-run`・`clear-guitar-rock`・戦闘曲・静かな曲の 4 種）で、新しい master 段と現状の A/B（同じ LUFS にそろえてから聞く）。
- `asoftclip` の型（tanh／cubic など）の聞こえ方。
- `mcompand` の伝達点の初期値、`adynamicequalizer` の効き。
- `alimiter` の `asc`。リリース 50ms と 80ms の違い。
- OGG ループ点のメタデータの扱い（ゲーム側の再生コード次第）。

## 9. 自動マスタリングの考え方（リファレンス合わせ・マッチング EQ）
- 仕組み（出）: 参考曲の**周波数の平均形**と音量を測り、自分の曲との差の EQ カーブを作って当てる。「quantity of EQ」（amount）と「smoothing」で強さと滑らかさを決め、範囲（アクションリージョン）で低域だけ・高域だけ、のように限定できる。
- 実用の目安（出）: 参考から 20〜30 秒をとる／スムージング約 50%／**amount 30% 以下**（マスターでは弱く）。「少ないほどよい」。ミックスがほぼ仕上がってから使う。
- 比べる前に音量をそろえる（±0.5dB）（既存文書）。聴き比べでは「参考と入れ替える」ボタンのように、すぐ切り替えられる形が良い（出）。
- うちでの使い方: 数字だけ（1/3 オクターブ・曲全体）を目標にし、**曲の真似ではなく、帯域の偏りを見つける道具**にする。効かせすぎないために ±3dB で切る。

## 10. 参考にした資料（本文を読めたもの。URL）
工程・チェーン
1. Mastering The Mix「Where Every Mastering Plugin Sits In The Chain」https://www.masteringthemix.com/blogs/learn/where-every-mastering-plugin-sits-in-the-chain
2. Sage Audio「how to setup your mastering chain」https://www.sageaudio.com/articles/how-to-setup-your-mastering-chain
3. Sage Audio「How to Limit Your Master」https://sageaudio.com/articles/how-to-limit-your-master
4. Mastering The Mix「How To Use A Clipper When Mastering」https://www.masteringthemix.com/blogs/learn/how-to-use-a-clipper-when-mastering
5. iZotope「What Is Soft Clipping?」https://www.izotope.com/en/learn/what-is-soft-clipping.html
6. mastering.com「Clipper vs Limiter」https://mastering.com/clipper-vs-limiter-know-the-difference/
7. Sound On Sound「リミッターのリリース設定」https://www.soundonsound.com/sound-advice/q-what-release-settings-should-use-limiter
8. Sound On Sound「Phoenix Audio Pivot（ティルト EQ）」https://www.soundonsound.com/node/4916156
ラウドネス・真のピーク
9. Fora Soft「LUFS targets per platform 2026」https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026
10. Orphiq「Mastering for Streaming」https://orphiq.com/resources/mastering-for-streaming
11. Signalkey「Inter-sample peaks」https://www.signalkey.io/learn/what-is-true-peak
12. Rae Spoon「Mastering for streaming LUFS guide」https://raespoon.com/dispatches/mastering-for-streaming-lufs-guide/
13. Softube「Dynamic range in mastering」https://www.softube.com/blog/dynamic-range-in-mastering-why-it-matters
14. Phil Speiser「Loud without losing dynamics」https://www.philspeiser.com/blog/loud-without-losing-dynamics
15. Full Compass「Mastering for CD and streaming」https://fullcompass.com/gearcast/mastering-for-cd-and-streaming
ゲーム
16. Audiokinetic「Mastering a Game with Wwise Part 1」https://audiokinetic.com/en/mastering-a-game-with-wwise-part1
17. Audio Media International「Mobile loudness: an adaptive approach」https://audiomediainternational.com/mobile-loudness-an-adaptive-approach/
18. Microsoft Flight Simulator「Audio mixing standards」https://docs.flightsimulator.com/msfs2024/retail/sound/audio-mixing-standards/index.md
19. Defold forum「Optimization of sounds in web games」https://forum.defold.com/t/optimization-of-sounds-in-web-games/81860
20. Bugnet「Which audio file formats should your game use」https://bugnet.io/blog/which-audio-file-formats-should-your-game-use
21. OpenGameArt「Bitcrushing」（レトロ風の作り方）https://opengameart.org/content/bitcrushing
ループ
22. Ardour forum「Exporting seamless loops」https://discourse.ardour.org/t/exporting-seamless-loops/102537
23. DIY AI「Seamless music loops for games」https://diyai.io/ai-tools/audio-generation/ai-music-loops-for-games/
帯域・M/S・マルチバンド
24. iZotope「Multiband Compression Basics」https://www.izotope.com/en/learn/multiband-compression-basics-izotope-mastering-tips
25. MasteringBox「Multiband compression」https://www.masteringbox.com/learn/multiband-compression
26. Future Proof Music School「Preserve mono low end while widening highs」https://futureproofmusicschool.com/blog/how-do-i-preserve-mono-low-end-while-adding-stereo-width-to-highs
27. Future Proof Music School「Cut lows from the sides or the mid」https://futureproofmusicschool.com/blog/should-i-cut-low-frequencies-from-the-sides-or-the-mid-channel
28. Unison「Mid/Side EQ」https://unison.audio/mid-side-eq/
ジャンル別
29. Nail The Mix「Mastering FAQs（メタル）」https://www.nailthemix.com/mastering-faqs
30. Mastering The Mix「Secrets To Making Your Music Stand Out（EDM・DnB のラウドネス）」https://www.masteringthemix.com/blogs/learn/secrets-to-making-your-music-stand-out
31. Cinematic Composing「Mastering Orchestral Mockups」https://learn.cinematiccomposing.com/blog/mastering-orchestral-mockups
32. Home Recording「Tips for mastering acoustic music」https://homerecording.com/bbs/threads/tips-for-mastering-acoustic-music.243223/
33. UJAM「Top 5 production & mixing tips for lo-fi」https://ujam.com/blog/top-5-production-mixing-tips-for-lofi
34. VI-Control「Setting up levels for ambient music」https://vi-control.net/community/threads/setting-up-levels-for-ambient-music-stereo-track.162839/
35. Claude AI music skills「Mastering engineer（ジャンル別の目標LUFS）」https://claudeskills.info/skills/bitwize-music-studio/claude-ai-music-skills/mastering-engineer/
リファレンス・マッチング EQ
36. iZotope「Mix and master with reference tracks in Ozone」https://www.izotope.com/en/learn/mix-and-master-with-reference-tracks-in-ozone.html
37. Music Guy Mixing「Match EQ plugin」https://www.musicguymixing.com/match-eq-plugin/
ffmpeg・ラウドネス測定
38. DEV「ffmpeg loudnorm EBU R128 guide」https://dev.to/javidjamae/ffmpeg-loudnorm-filter-ebu-r128-loudness-normalization-guide-15d4
39. AnimeThemes「Audio normalization（AES -16 LUFS・2 パス）」https://animethemes.moe/wiki/encoding/audio_normalization
40. Google Assistant「Audio loudness（-16 LUFS・ffmpeg の測り方）」https://developers.google.com/assistant/tools/audio-loudness?hl=en

加えて、手元の ffmpeg 6.1.1 の `ffmpeg -h filter=...`（mcompand・alimiter・asoftclip・stereotools・acrossover・acompressor・firequalizer・adynamicequalizer・aresample の dither_method など）で、オプション名・範囲・既定値を確かめた。

## 11. 実装状況（2026-10-11）

§8 の提案 11 個を `tools/composer/master.mjs`・`master-report.mjs`・`song-lib.mjs`・`song.mjs` と `tools/audio-check/` に実装した。テストは `node --test tools/composer/*.test.mjs`（16 件）。**測った数字は合成音と見本曲（`loud-rock-demo` 30 秒、`delicate-demo` 53 秒、`hiphop-demo` 44 秒）のもので、音の良し悪しは耳で確かめていない**。

### 入れたもの
| # | 提案 | 状態 | どこに・どう入れたか | 測った数字 |
|---|---|---|---|---|
| 1 | プリセット `--master-preset` | **入れた** | `MASTER_PRESETS` に 21 個（従来の game・rock・loud・calm の 4 つは**値も出力も変えず**、新しく metal・punk・rock-clean（別名 rock-pop）・pop・jazz・orch・edm・hiphop・lofi・ambient・game-field（別名 game-town）・game-battle・game-boss（別名 game-title）・game-dungeon・retro・wafu・solo の 17）。値は §3-1 の表の数字。`SoundSet.master` に `preset` `space` `spaceWet` を持たせた。個別の上書き引数も追加（下記）。一覧は `song.mjs presets` | 全 21 プリセットを 30 秒の見本曲で通し、1 回の書き出し 5〜14 秒。仕上がりの大きさは目標 ±0.1LU（loud だけ -8.3。リミッターの限界）。従来 4 つの出力は、書き出し前後の WAV の md5 が一致（8 通り） |
| 2 | 真のピーク対応のリミッター | **入れた**（新プリセットのみ `strictTp`） | 192kHz で処理するのは従来どおり。書き出し後に TP を測り、天井を 0.05dB 超えたら超えたぶん `limit` を下げてやり直す（大きさのずれと合わせて最大 3 回）。従来 4 つは今まで通り（出力固定のため） | 12kHz・山 0.95 の合成音で天井 -1.5 のとき TP -1.4 以下。見本曲では全プリセットが天井以内（-1.3〜-7.9 dBTP） |
| 3 | 低域のモノ化 | **入れた** | 従来の 140Hz に加え、プリセットごとの周波数（100〜150）と `--lowmono`。書き出し後の「低域相関」を合否表に。モノ化の前後で低域の割合が 3dB 以上減ると警告 | 逆相の 60Hz を入れた合成音で、100Hz 以下の左右の相関 0.5 未満 → 0.93（pop プリセット） |
| 4 | 音量合わせの閉ループ | 従来どおり（済） | 書き出し後に測り直す仕組みは前から入っていた。TP の補正を足した | 見本曲で目標との差 ±0.1LU |
| 5 | M/S ワイド | **入れた** | `sideHpf` があると `stereotools`（FL=Mid・FR=Side）でサイドだけ HPF してから `slev=widen`。`--side-hpf`。サイドの高域だけを足す `air`（10kHz のシェルフを FR に）も（edm +2・game-boss +1）。`sideHpf` の無いプリセット（従来 4 つ）は extrastereo のまま | 50Hz の逆相（サイドだけ）の合成音で、M/S のサイド残りは extrastereo の 1/5 以下、2kHz のサイドは残る（テストで固定） |
| 6 | ソフトクリップ | **入れた** | `clip`（dB）。`volume=+clip` → `aresample=192000` → `asoftclip=tanh:oversample=1` → `volume=-clip`。`--clip`。コメントに oversample の 6dB 低下を残した | `rock-clean` で clip 0 / 0.5（既定）/ 2 を同じ -10LUFS にそろえると、TP -1.3 / -2.3 / -3.1、PLR 8.7 / 7.7 / 7.0。**強くするほど山は下がるが PLR も下がる**ので 2 より上は使わない。型の比較（+8dB 持ち上げた信号の山をどれだけ下げるか）: tanh -2.1dB・exp -2.1・alg -2.8・cubic -1.2・sin -1.3・quintic -0.6・hard 0。-20dB の小さい信号では tanh・cubic・exp・sin・alg・quintic のどれも音が変わらなかった（atan・erf は音量が変わるので不採用）。**§4 の実験 5「tanh は小さい音にも効く」は、この再実験では確認できなかった** |
| 7 | ディザ | 従来どおり（済） | 変更なし | — |
| 8 | マルチバンド（低域のみ） | **入れた**（metal・game-battle・game-boss） | `mcompand` の 2 帯域（150Hz 分割、上は素通し）。`mb: {split,thr,ratio}` | metal で mb あり/なし: LRA 7.9 / 6.0、PLR 7.1 / 6.8（低域の動きを抑えたぶん、全体を同じ大きさにするとほかが相対的に動く） |
| 9 | マッチング EQ | **入れた** | `tools/audio-check/match-eq.py`（1/3 オクターブ・曲全体・隣と 1:2:1 でならす・各帯域 ±3dB で切ってから amount・上限 0.5・80Hz〜12.5kHz だけ・端は 0）。目標は `docs/sound/data/mix-targets.json`（**数字だけ**＝傾き dB/oct）。`--match-eq <家族> --match-amount` で `firequalizer=gain_entry` に | `rock-clean` に `--match-eq rock`（amount 0.4）で、ロックの傾きとの平均絶対差 5.1 → 4.4dB。当てる量は最大 ±1.2dB |
| 10 | ループの継ぎ目 | **入れた**（一部） | `--loop-tail`（`loopTailWrap`: 曲の長さ T より後ろの尾を先頭に `amix` で重ねて T 秒に切る。入力は同じファイルを 2 つ渡す方式）。`loopCheck`: ①末尾→先頭の段差（末尾 20ms の「となりの音との差」の 8 倍超）②継ぎ目の前後 100ms の大きさの差（6dB 超）③前後 400ms（4dB 超）を警告 | 合成音で、そのまま続く音は通り、フェードアウトで終わる音は警告。`--loop-tail` の合成テストで長さが T ±0.02 秒 |
| 11 | 音量補正表・合否表 | **入れた** | ①`tools/audio-check/bgm-trim-report.py`: `docs/sound/bgm-loudness.json` から -16 LUFS 軸の補正量を計算（上げるときは TP -1 まで、±12 で切る、戦闘・ボス +1.5・ダンジョン -2 の場面補正、差 3dB 超を警告）。②`master-report`（`song.mjs report <wav>` と、書き出しの最後の 1 行）: I・TP・LRA・PLR・PSR・相関・低域相関・継ぎ目を ○／要直し | 58 曲: 補正は -11.0〜0.0dB、-16 から 3dB 以上離れた曲 31、上限で止まる曲 6（ゲームの `bgm-trim.ts` は軸 -15 のまま。表の差し替えは再生音量が変わるので人間の判断待ち） |

追加した引数（`song.mjs` の使い方の説明文にも書いた）: `--tp` `--lowmono` `--side-hpf` `--clip` `--hpf` `--lpf` `--match-eq` `--match-amount` `--loop-tail`、コマンド `report`・`presets`・`delays`。`--space-wet` の既定値はサウンドセットの `spaceWet` があればそれを使う（引数が優先）。

### 合否表の基準（自分で決めた数字）
- 大きさ: 目標 ±0.5LU／TP: 天井 +0.1 以内／左右の相関 0.3 以上／低域相関 0.9 以上（0.5×モノ化周波数以下で測る。低域が全体より 30dB 以上小さい曲は測らない）
- PLR・PSR の下限は目標の大きさで 3 段: -10LUFS 以上 6／4、-13 以上 7.5／5、それより静かなら 9／6.5。§2-2 の「PSR 8 以上」は静かな側の目安で、大きい仕上げにそのまま当てると必ず不合格になるため、見本曲の実測（-10LUFS で PSR 4.3〜6.3）から下げた。

### 入れなかったもの・変えたものと理由
- **動的 EQ（`adynamicequalizer`）**: ffmpeg 6.1 で試したところ、`threshold=0` で効かず `1` 以上で全域が一定に切れ（しきい値を上げても変わらない）、`mode=cutabove` は構文エラー。動的 EQ としては使えないので採用せず、低域だけの `mcompand` で代用した。
- **`aexciter`・`asubboost`・`alimiter` の `asc`・アンチエイリアスの比較**: 効果を聴いて決める作業が要るので未実装（コードのコメントに残してある）。
- **レトロ風の「荒さ」（低いレートに落として戻す）・ローファイのワウ／フラッター**: 音を聴いて決める部分なので、LPF だけ（retro 12kHz・lofi 10kHz）にした。
- **2 周つなげた Short-term の跳び**: 100ms／400ms の窓の RMS 差で代用した（同じ目的で、ffmpeg を 2 周回さずに済む）。
- **OGG のループ点メタデータ・ゲーム内の再生側の変更**: ゲーム側の作業（担当外）。`bgm-trim.ts` の軸（-15）も変えていない。
- **EQ の「ティルト」**: `orch` だけ -0.5dB/oct。ほかは `equalizer`／`treble` の小さい山と棚で足りた。
- 圧縮の位置: §1 の順（EQ → M/S → 圧縮）ではなく、従来の並び（EQ → 圧縮 → 低域モノ・広げる）のままにした。広げる処理がリミッターの前にあることは守っている。出力を変えないための選択。
- プリセットの `rock`: 従来の `rock`（-10LUFS・widen 2.4・normal）の意味を変えない約束なので、§3-1 #1 の「クリーンギターのロック」は `rock-clean`（別名 `rock-pop`）にした。
