# 現代ラウドロック／メタルコア／ポストハードコアの音作り（2015〜2026）調査まとめ

調査日: 2026-10-22。目的は、既存曲の音をまねることではなく、**一般的な制作手法**を集めて、Web Audio で作っている作曲ソフトの設定値に置きかえること。

## 読み方

- **【出典】** は記事やインタビューに書かれていた内容（数値は原文どおり）
- **【実装値】** は、出典の数値と一般的な信号処理の知識をもとに、Web Audio（BiquadFilter / WaveShaper / DynamicsCompressor / ConvolverNode / DelayNode / GainNode / StereoPanner）で使えるように決めた**出発点の値**。最後は耳で決める。
- 出典が数値を出していないところは「数値なし」と書き、実装値は一般的な目安で補った（その場合は「目安」と書いた）。

### 調べてわかった全体の傾向（先に結論）

1. **ゲインは思っているより少なく、ブースター（TS系）で低域を締める**のが定番。TS系はドライブ 0〜2、レベル 8〜10。
2. **ギターの低域は思い切って切る**（HPF 80〜150Hz、低いチューニングでも 100Hz 前後から）。低域はベースとキックに任せる。
3. **歪んだギターにはふつうのコンプを掛けない**。かわりに 100〜400Hz だけを押さえるマルチバンドかダイナミック EQ を使い、ブリッジミュートの「ボワッ」だけを抑える。
4. **ベースは「クリーンの低域」と「歪んだ中高域」に分けて並列で鳴らす**のが標準。分け目は 100〜300Hz（クランク成分は 700Hz〜2kHz）。
5. **キックは生音とサンプル（トリガー）を混ぜる**。サンプルはアタック（3.5〜5kHz）担当、生音（またはサブ層）は重さ（50〜80Hz）担当。生マイクは 450Hz 以下を切ってサンプルと位相がぶつからないようにする例もある。
6. **サイドチェインでキックの瞬間だけベースを 3〜6dB、ギターを 3dB 以下下げる**と、キックが前に出る。
7. **ドラムバスは SSL 型コンプ（アタック 30ms・比率 4:1・3〜4dB）**、パラレルは 10:1〜20:1 で 10〜20dB 潰して下に混ぜる。
8. 市販のメタルのマスターは **-7〜-5 LUFS**（とても大きい）。ただしこのソフトの標準は人間の指示どおり **-13.5 LUFS（B 設定）** のままでよい。配信では -14 LUFS 付近に下げられるので、大きくしても得がない。
9. **シンセがなくても現代的に聞こえる**のは、ギターのアンビエント層（スウェル・E-Bow 的な持続音・トレモロ・リバーブだらけのリード）、逆再生シンバル、ブレイク前のリバーブ投げ、テープストップ、セクションごとの自動化（音量・フィルター・広がり）による。

---

## 1. リズムギター

### 1-1. チューニング（最低音の基本周波数）

| チューニング | 最低音 | 基本周波数 | ベース（1オクターブ下） |
|---|---|---|---|
| 標準 E（参考） | E2 | 82.4Hz | E1 41.2Hz |
| ドロップ D | D2 | 73.4Hz | D1 36.7Hz |
| ドロップ C（メタルコアの定番） | C2 | 65.4Hz | C1 32.7Hz |
| ドロップ B / 7弦標準 B | B1 | 61.7Hz | B0 30.9Hz |
| ドロップ A（7弦、ラウド系で多い） | A1 | 55.0Hz | A0 27.5Hz |
| 8弦標準 F# | F#1 | 46.2Hz | （5弦/6弦ベースや同音） |
| ドロップ E（8弦） | E1 | 41.2Hz | — |

- 【出典】標準 E の基本は約 82Hz、ギターの力の中心は 100〜250Hz。ドロップ F# の基本は約 46Hz（Nail The Mix「How to Mix Low Tuned Guitars」）。
- 【出典】Jens Bogren: 下げたチューニングの質感は「砂ではなく砂利のよう」。低域カットは約 100Hz、12〜18dB/oct（Gearspace インタビュー）。
- 【出典】ベースは強く弾くとシャープしやすいので、10〜15 セント低めに合わせることもある（Nail The Mix「Different Types of Bass」）。
- 【実装値】
  - 曲ごとに `tuning: 'dropC' | 'dropA7' | 'f#8'` などを選べるようにし、最低音を上の表の周波数にする。
  - **低いチューニングほどギターの HPF を上げてよい**（基本周波数より上で切ってもよい。倍音が音程を伝えるため）。ドロップ C で 90〜110Hz、ドロップ A で 100〜130Hz、8弦で 110〜150Hz。
  - 弦の太さの感じ（低い弦ほど「ゴリッ」とした粒の粗さ）を出すため、低いチューニングでは歪みの前の 1.5〜3kHz を +1〜2dB。

### 1-2. ゲイン（歪みの量）は意外と少なめ

- 【出典】ゲインは「和音の一音一音が聞こえるところまで下げる」。大きさは1本を歪ませるのではなく、2本・4本重ねで作る（Nail The Mix「Guitar Mixing FAQs」）。
- 【出典】歪みはそれ自体が圧縮なので、歪みが多いほどコンプは少なく（Jens Bogren / Leprous の記事）。
- 【出典】Jens Bogren は重いリズムギターに録音でもミックスでもコンプを使わない（Gearspace）。
- 【実装値】
  - WaveShaper の曲線は `tanh(k·x)` 系で、**k（入力ゲイン）を 8〜20 程度**から始める（現在の値が 30 以上なら下げる）。高すぎると「割れ」「ピー」という高域が出る（人間が嫌った歪みギターの原因の一つ）。
  - 歪みは**2段に分ける**（プリアンプ的に k=3〜5 → 間にフィルター → k=4〜8）。1段で大きく歪ませるより、音の芯が残る。
  - 2段の間に HPF 100〜150Hz（12dB/oct）を入れると、低域がつぶれず締まる（ブースターと同じ考え）。
  - 4× オーバーサンプリング（`WaveShaperNode.oversample = '4x'`）を必ず使う。折り返しノイズが「ピー」「シャリシャリ」の原因になる。

### 1-3. ブースター（TS系オーバードライブ）でタイトにする

- 【出典】ブースター用途の TS 系は「ドライブはほぼ 0、レベル高め（2時以降）」。低域を切って中域を前に出し、アンプの入力を押す（Violet Recording「What Is a Tube Screamer?」）。
- 【出典】Spiritbox のプラグインの前段オーバードライブ: ドライブ約 1〜2、レベル約 8〜9。低域を締め、中域を集める（Nail The Mix「Spiritbox Plugin」）。
- 【出典】Jens Bogren（BTBAM）: 左右で別のブースターを使う（左 TS 改造、右 OD808）。Leprous では「ブーストあり」と「ブーストなし」の層を混ぜ、ブーストありが主役、静かな部分ではブーストなしを上げる。
- 【実装値】（TS の回路はゲイン段に約 720Hz の一次ハイパスがあり、700Hz〜1kHz 付近が持ち上がる「中域の山」が特徴として広く知られている。ドライブ 0 では元の音も混ざるため、実効的には「低域を下げて中域を少し持ち上げ、音量を上げる」になる）
  - 歪みの**前**に: Highpass 150Hz（Q 0.7）→ Peaking 800Hz +4dB（Q 0.8）→ Lowpass 6kHz（Q 0.5）→ Gain +6〜+10dB
  - 「ブーストなし」の層（4本重ねの内側ペア用）は Highpass 80Hz、Peaking なし、Gain +0dB。

### 1-4. キャビネット（IR）とマイク

- 【出典】SM57 はスピーカーの「ダストキャップとコーンの境目、約 1 インチ（2.5cm）」から始める。キャップ寄りは明るくアタック強め、エッジ寄りは暗く太い。SM57 の特性は 4〜6kHz の山と緩い低域落ち（Nail The Mix「SM57」）。
- 【出典】SM57 + MD421（低中域の太さ）、SM57 + Royer R-121（リボン、低域の重さと滑らかな高域）の組み合わせ。Andy Sneap 系は 57 と 421 を並べる。
- 【出典】キャビネットはメサの 4×12（Celestion Vintage 30）が定番。Jens Bogren は 4本重ねの内側ペアに別のキャビを使い、低域と位相を整える。
- 【実装値】（IR 音源がない場合のキャビ近似。今のソフトに IR がある場合はそれを優先）
  - Highpass 70〜90Hz（Q 0.7、キャビの低域の限界）
  - Peaking 110〜130Hz +2〜3dB（Q 1.0、密閉キャビの「ドスッ」）
  - Peaking 400Hz −3dB（Q 1.2、箱鳴り）
  - Peaking 2.5kHz +3dB（Q 1.0、V30 の中高域）
  - Peaking 4.5kHz +2dB（Q 1.5、SM57 の山）
  - Lowpass 5.5〜7kHz（12dB/oct を 2 段 = 24dB/oct。スピーカーは 5kHz より上がほぼ出ない。ここが甘いと「ピー」が出る）
  - 「57 + 421」風にするなら、上の鎖のコピーで Peaking 2.5k/4.5k を下げ、200Hz を +2dB したものを 30% 混ぜる。
  - 「Fredman（2本の 57、片方 45 度）」風: 片方の鎖で 2〜3kHz に浅い谷（−3dB）を作り混ぜると、えぐれた広い音になる。

### 1-5. EQ（ハイパス・ローパス・不要な帯域）

- 【出典】HPF は「細く聞こえ始めるところまで上げて、少し戻す」。だいたい 80〜120Hz（Zakk Cervini の記事）、100〜120Hz かそれ以上（Guitar Mixing FAQs）、100〜150Hz、ときにそれ以上（Quad Tracking）、ギターバスで 150Hz（Jens Bogren / Leprous）、BTBAM の各トラックは約 50Hz（あとでバスで調整）。
- 【出典】LPF は 10〜12kHz から下げていく（FAQ）、8〜10kHz（Andy Sneap 系）、8〜12kHz（Spiritbox）。
- 【出典】こもり・箱鳴りは 250〜500Hz の一番ひどいところを**狭い Q で**下げる（広く削らない）。耳に痛い「ジリジリ」は 4〜8kHz を狭い Q で（Zakk Cervini）。
- 【出典】Dan Lancaster（BMTH）: SSL チャンネルで 2.5kHz・4.3kHz・8kHz を +6dB、そのあと EQ を何個も使って問題の周波数を狭く削る（Sound On Sound）。
- 【出典】中域を全部えぐらない（Riffhard）。プレゼンスは 2〜5kHz を広く少し上げる（Spiritbox）。
- 【実装値】（ギター1本ずつ → ギターバスの順）
  - 1本ずつ: Highpass 100Hz（12dB/oct）、Lowpass 9kHz（12dB/oct）
  - Peaking 350Hz −3dB（Q 2.0）※曲ごとに 250〜500Hz で一番こもる所
  - Peaking 5.5kHz −3dB（Q 4.0）※耳に痛い所（4〜8kHz）。複数あれば 2〜3 個
  - Peaking 2.5kHz +1.5dB（Q 0.7）※前に出したいとき
  - ギターバス: Highpass 120Hz（ドロップ A なら 130Hz）、Highshelf 10kHz +1dB（空気感、なくてもよい）
  - ボーカル（歌）がある部分は、ギターバス 1〜3kHz を −1〜2dB（後述のサイドチェインで自動化してもよい）

### 1-6. 重ね録り（ダブル／4本）と左右の振り方

- 【出典】4本重ねの振り方: 1本目 L100%、2本目 R100%、3本目 L70〜80%、4本目 R70〜80%（Nail The Mix「Quad Tracking」）。
- 【出典】内側ペアは音色を変える: ピックアップを変える、ゲインを少し下げる、ブースターを変える、IR を変えて中域の性格を変える。まず外側2本がぴったり合ってから足す。
- 【出典】ギターは同じ演奏の複製（コピー）ではなく、別テイク。BTBAM では左右のチャンネルに別の「SSL のランダムなチャンネル」を割り当てて、わずかな違いで広がりを出す。
- 【出典】ギターのアンビエンスは部屋マイクより、テンポに合ったディレイの方が芯がぼけない（Jens Bogren）。
- 【実装値】
  - **同じ音を左右に置くだけでは広がらない**（真ん中に集まる）。左右で次をずらす:
    - 発音タイミング: ±3〜12ms のランダム（1音ごと）
    - ピッチ: ±3〜6 セントのランダム（1音ごと）、左右でオフセット（L −2 セント、R +2 セント）
    - ベロシティ（強さ）: ±8%
    - EQ: 左右で Peaking 位置を少し変える（L 2.3kHz / R 2.8kHz など）
  - 外側ペア: pan −1.0 / +1.0、ブーストあり、ゲイン k=14 など
  - 内側ペア: pan −0.75 / +0.75、ブーストなし（または別キャビ近似）、ゲイン k を外側の 70%、音量は外側より −4〜−6dB
  - 静かな部分（ヴァース・クリーン寄り）は外側ペアだけ、サビ・ブレイクで内側ペアを足す（自動化）。
  - Haas 効果（片側だけ 10〜20ms 遅らせて広げる）は**使わない**。モノラルにしたとき音が薄くなり、位相が乱れる。

### 1-7. ゲート

- 【出典】ゲートのアタック 0.1〜1ms（先読みがあれば 0ms）、ホールド 10〜50ms（速い刻みは 5〜20ms）、レンジは完全に消す（−∞）か、自然にしたいなら −12〜−20dB、キー信号は 2〜5kHz を通してピックの当たりで反応させる。歪みの前（DI）の信号で歪み後をゲートすると正確（Nail The Mix「Noise Gate for Metal Guitars」）。
- 【実装値】（このソフトは打ち込みなので、ノイズを消すためよりも「止めの鋭さ」の調整として）
  - 刻みの止め: 音符の終わりから 5〜15ms でリリース（指数カーブ、−40dB まで）。
  - **ただし人間の好みとして「すぐミュートする」「ブリッジミュートの刻みだらけ」は嫌われている**。止めるのは速い刻みのブレイク部分だけにし、和音を伸ばす部分・リード・クリーンには掛けない。伸ばす和音は 300ms〜1.5s かけて自然に減衰させる。
  - レンジは −20dB（完全に消さない）を標準に。完全に消すのは刻みが速いところ（16分以上）のみ。

### 1-8. 低域の暴れ（ブリッジミュートの「ボワッ」）を抑える

- 【出典】マルチバンドで 100〜250Hz だけを押さえる（FAQ）、150〜400Hz を速いアタック・速いリリースで、一番大きいミュート音だけに数 dB（Andy Sneap 系）、150〜200Hz 以下を速く強く（Low Tuned）。BTBAM ではギターバスの 100〜150Hz をタムの音でサイドチェインして下げる。
- 【出典】ギターバスは軽く 1〜2dB（FAQ）、SSL 型 アタック 約 30ms・リリース速め・1〜3dB（Spiritbox）。
- 【実装値】
  - Web Audio にマルチバンドはないので、**帯域分割**で作る: 入力 → (Lowpass 200Hz ×2 段) → DynamicsCompressor（threshold −24dB, ratio 4, attack 0.003s, release 0.08s, knee 6）→ 合流。もう一方は (Highpass 200Hz ×2 段)。※Linkwitz-Riley に近づけるため Q=0.707 を 2 段。
  - または「ミュートの音符だけ 120〜250Hz を −3dB」をノート側で行う（簡単で確実）。
  - ギターバス全体: DynamicsCompressor threshold −12dB, ratio 2, attack 0.03s, release 0.1s, 目標 1〜2dB。

---

## 2. リードギター

- 【出典】リードはリズムと別のアンプ・別のキャビにして抜けをよくする（Jens Bogren）。Jens は Amon Amarth のリードにコンプを使わなかった（歪みで十分圧縮されている）。
- 【出典】Spiritbox 系はリード用チャンネルを「なめらかで、より歪んだ」音にする。
- 【出典】ディレイはセンド（AUX）で使い、プラグイン側は 100% ウェット、送り量で混ぜる。左右で拍を変える: 片方 4分、もう片方 付点8分 か 8分。ピンポンの単調さを避ける。フィードバックは「中くらい」から、速いフレーズでは下げ、最後の伸ばしやチョーキングで上げる（自動化）。ディレイ音に HPF 200〜300Hz、LPF 3〜5kHz（Nail The Mix「Delay」）。
- 【出典】リードのディレイは 4分音符、フィードバック約 25%、ミックス 30〜40%（Music Guy Mixing）。
- 【出典】付点8分の計算は 45000 ÷ BPM（ms）。168BPM なら 268ms（bonedo）。
- 【出典】Dan Lancaster はリバーブ用 AUX とディレイ用 AUX を複数用意。Jordan Fish は「リバーブより ディレイが好き」。
- 【実装値】
  - 歪み: リズムより k を 1.3〜1.6 倍（サステインを出す）。ただし前段 HPF は 200〜250Hz と高めにして、低域の濁りをなくす。
  - EQ: Highpass 180Hz、Peaking 1.2kHz +2dB（Q 0.8、歌うような中域）、Peaking 3kHz +1.5dB、Lowpass 7.5kHz（24dB/oct）。
  - **人間の好み**: 標準の crunch アンプ（「ピロピロ」）は使わない。ビブラートは「ゴムが伸びる」感じになるので深さを控えめ（±15〜25 セント、4.5〜5.5Hz、0.25〜0.4s 遅れて始めて徐々に深く）。チョーキングは 1/2〜1 音を 60〜150ms で上げる。
  - ディレイ（センド）: L = 4分音符、R = 付点8分、フィードバック 20〜30%、ディレイ内に HPF 250Hz と LPF 4kHz、送り量はドライに対して −12〜−9dB（ミックスで 25〜35% 相当）。長い伸ばしの音の終わりだけ送り量を +3〜6dB 上げる（「ディレイ投げ」）。
  - リバーブ: プレートかホール、減衰 1.8〜2.8s、プリディレイ 20〜40ms、HPF 300Hz、LPF 6kHz、送り −16〜−12dB。
  - **ディレイとリバーブをリードの音でダッキング**（弾いている間は小さく、止まると広がる）: 送り先のゲインを、リードの音量に合わせて −4〜−6dB 下げる（アタック 10ms、リリース 250〜400ms）。
  - 置き方: ソロ1本なら中央かやや片寄り（±0.15）。2本ならハモりを L/R ±0.4〜0.6。
  - ハモり: 3度上（スケール内）が基本、5度・6度も使う。オクターブ重ね（1オクターブ下を −6dB）で太くする。ハモりの側は音量 −3dB、タイミング +5〜10ms。

---

## 3. ベース

### 3-1. 歪みとクリーンの並列（帯域を分ける）

- 【出典】クリーンの低域トラックは 200〜300Hz より上を切る、歪みトラックは 200〜250Hz より下を切る。クランク・ザラつきは約 800Hz〜2kHz（Nail The Mix「Different Types of Bass」）。
- 【出典】DI を 2本に分けて約 150Hz で分ける。下は強く圧縮、上は歪ませて好みで混ぜる（Breakdowns 記事）。
- 【出典】クリーン（サブ）トラックは LPF 150〜200Hz → 圧縮、ザラつきトラックはその上から HPF → 歪み（Low Tuned 記事）。
- 【出典】「カランとした」金属的なベース: 歪み側の HPF を 500Hz〜2kHz（出発点 700Hz）にして、クリーンの低域と混ぜる（Joel ＝ Nail The Mix「Clanky Bass」）。
- 【出典】Jens Bogren: クリーンアンプ＋歪み（SansAmp 系）＋ 5kHz で HPF した DI（弦の細かさ）を混ぜる。ベースをドラムのパラレルコンプに送ることもある。
- 【出典】Dan Lancaster（BMTH）: DI に API 550 で 2.5kHz +12dB、1.5kHz 付近も上げてから 1176 系で圧縮。アンプ側は SansAmp で歪ませ、圧縮と歪みのあとで 30Hz を持ち上げる。
- 【出典】Sylosis のベース: 1176 系で約 5dB、さらにリミッター 3〜4dB。60Hz を上げ、100Hz を深く狭く削り、300Hz を削り、600Hz〜1kHz は残し、1〜2kHz の「ヒュー」という耳障りを削る。アナライザーで低域と高中域が同じくらいの高さになるのが目安。
- 【実装値】（人間の好み: ラウドのベースは**明るくゴリッと**、**こもった音はだめ**、**指弾き**がよい）
  - **低域（クリーン）層**: Lowpass 160Hz（24dB/oct）→ DynamicsCompressor（threshold −28dB, ratio 6, attack 0.01s, release 0.12s）→ 音量 0dB 基準
  - **中域（歪み）層**: Highpass 160Hz（24dB/oct）→ 前段 Peaking 800Hz +3dB → WaveShaper（k=6〜12、4x）→ Peaking 300Hz −3dB（Q 1.5、こもり取り）→ Peaking 1.2kHz +3dB（Q 0.8、ゴリッ）→ Peaking 1.8kHz −2dB（Q 3、ヒュー音）→ Lowpass 4.5kHz → 音量 −3〜0dB（明るくしたいときは上げる）
  - **弦の粒（クランク）層（任意）**: Highpass 2.5kHz → 軽い歪み k=3 → Lowpass 8kHz → 音量 −12〜−9dB。指弾きの「パチッ」とした当たり（1〜3ms の短いアタック成分）を残す。
  - 全体（ベースバス）: Peaking 60Hz +2dB（Q 1.0）、Peaking 100Hz −2dB（Q 4、キックの居場所）、DynamicsCompressor（threshold −18dB, ratio 4, attack 0.02s, release 0.1s、約 5dB）→ 最後に軽いリミット（threshold −6dB, ratio 20, attack 0.001s）。
  - **指弾き**の音作り: アタックの立ち上がり 4〜8ms（ピックは 1〜2ms）、指の当たりの成分を 700Hz〜1.5kHz に少し、2.5kHz 以上の「カチッ」は控えめ。音符の長さはギターより少し長め（レガート）にして「ブン」と鳴らす。
  - ジャズ的なグルーヴのベースは歪み層 0 にし、クリーン層の LPF を 2.5kHz に上げ、1音ごとのアタックをはっきり（立ち上がり 5ms、減衰を 0.3〜0.6s）。

### 3-2. ギター・キックとのすみ分け

- 【出典】キックとベースの重なりは 60〜100Hz。勝ち筋は「キックにサブ、ベースに低中域の倍音」（Volumes 記事）。
- 【出典】キックを 60Hz で上げたらベースを 60Hz で少し狭く削る。ベースが 120Hz に力があるならキックの 120Hz を少し削る（Kick Drum EQ）。
- 【出典】別の方法: キックの重さを 80〜100Hz に置き、ギターとベースのバスの同じところを緩やかに削る（Low Tuned 記事「High Kick」）。
- 【実装値】
  - 周波数の役割分担（目安）:
    - 30〜60Hz: キックのサブ（とベースのクリーン層の最低部）
    - 60〜100Hz: ベースの基音（キックと交互に。サイドチェインで解決）
    - 100〜250Hz: ベースの低中域、ギターはここから上
    - 250〜500Hz: 削る場所（全員）
    - 500Hz〜2kHz: ベースの歪み層・ギターの中域・スネアの胴
    - 2〜5kHz: ギターのプレゼンス・キックのアタック・スネアの「パン」・歌
    - 5〜10kHz: シンバル、ギターは控えめ
  - ベースはギターより 1 オクターブ下を基本に、ベースのメロディがある曲は丁寧に（人間の好み）。

---

## 4. ドラム

### 4-1. キック（トリガーのサンプル＋生音、重いキック）

- 【出典】キックは生音と強く加工したサンプルを混ぜ、鋭いアタックとサブを出す（Zakk Cervini）。
- 【出典】Wage War のキック: サンプルと生のルームマイクを同じバスにまとめる。サンプルの位相を反転すると「サブの太さ」が増えた（同位相だと低中域のパンチ）。バスに歪みを並列で約 14%。R-Bass で 80Hz を強調（強さ +13）。トランジェント強調。サンプル側は 16kHz 付近を広く上げてクリック、400〜500Hz を削る。**生のキックマイクは 450Hz 以下をほぼ全部切り**、3.5kHz を上げてビーターの当たりだけ使う（サンプルとの位相の衝突を避けるため）。最後にリミッター（Nail The Mix「Wage War」）。
- 【出典】キック EQ: HPF 30〜40Hz（それ以上は切らない）、250〜600Hz の箱鳴りを 3〜6dB 削る、50〜80Hz を 2〜4dB 広く上げる、アタックは 2〜4kHz（「バシッ」）か 5〜8kHz（現代メタルの「カチッ」）。生音は 70Hz を上げ、サンプルは 4kHz を上げて低域を大胆に切る（Kick Drum EQ）。
- 【出典】Joey Sturgis の帯域: サブ 20〜80Hz、パンチ 80〜250Hz、温かさ 400Hz〜1.5kHz、クリック 4〜12kHz、こもり 100〜300Hz、段ボール 500〜800Hz。例では 60Hz を中くらいの Q で上げる。
- 【出典】Dan Lancaster（BMTH）: 生キックで 1kHz を上げ、500Hz を削り、63Hz を持ち上げる。トランジェント処理で余韻を減らしてゲートのように使う。サンプルは近いマイクとルームの2種を混ぜる。
- 【出典】低いチューニングでは、キックに合わせて 40〜60Hz のサイン波（サブ）を鳴らす方法もある（Low Tuned）。ただし「とても低いサブは一般のスピーカーで聞こえない」（Wage War）、Jordan Fish も「音圧を追うと本当の低いサブは削られがち」と言う。
- 【実装値】（人間の指示: ラウドロックのバスドラは**トリガー**と、それとは別の**重みのあるバスドラ**の両方を入れる）
  - **トリガー層（アタック担当）**: 短いクリック（ノイズ 2ms + 高めの音 4ms）→ Highpass 1.5kHz → Peaking 4kHz +4dB（Q 1.2）→ Peaking 7kHz +2dB → 長さ 25〜40ms。音量はキック全体の −6〜−3dB。ベロシティに関係なく**ほぼ一定**（トリガーの性質。差は ±1.5dB 以内）。
  - **重み層（ボディ担当）**: サイン波を 150Hz → 50Hz（ドロップ A の曲なら 45Hz、ドロップ C なら 55Hz、曲のキーの根音近く）へ 40〜60ms で下げる。音量の減衰は 250〜400ms（速い2バスは 120〜180ms）。WaveShaper で軽く歪ませ（k=1.5〜2.5）倍音 100〜200Hz を足す。Peaking 60Hz +3dB、Peaking 350Hz −4dB（Q 1.5）、Highpass 30Hz。
  - **生音層（あれば。サンプル音源の生キック）**: Highpass 450Hz → Peaking 3.5kHz +3dB。音量 −8dB。
  - 3層をキックバスにまとめ: 並列歪み 14%（WaveShaper k=4 を 14% 混ぜる）→ DynamicsCompressor（threshold −10dB, ratio 4, attack 0.005s, release 0.06s）→ リミット（threshold −3dB, ratio 20, attack 0.001s, release 0.05s）。
  - 位相: 重み層の開始位相をトリガー層の立ち上がりと揃える（重み層の開始を 0〜1ms 遅らせて合わせる）。合わないと低域が消える。
  - 速い2バス（16分以上）: 重み層の減衰を短く（120ms）、音量 −2dB。各打の強さに ±1dB の揺れ。最初の一打だけ +1dB（Wage War の「フレーズの最初の一打が強く反応する」考え方）。

### 4-2. スネア

- 【出典】スネア: 胴 150〜250Hz を上げる、「パン」は 2〜5kHz を広く、空気 8〜12kHz を慎重に、HPF 80〜100Hz。1176 系で 6〜10dB 速いアタック・速いリリース。サンプルは音量 0 から上げて生音を支える程度（Drum Mixing FAQs）。
- 【出典】生スネア＋強く圧縮したサンプル（5kHz 付近にアタック）を下に混ぜる。ルーム系のサンプルで大きさを足す（Zakk Cervini）。
- 【出典】Dan Lancaster: サンプル2種と生スネアを重ねる。500Hz と 1kHz を少し上げる。歪みで鳴りを出し元の音と混ぜる。スネア裏はアタック遅め・4:1・約 3dB。
- 【出典】ブレイクダウン: スネアを AUX で速いアタック・速いリリース、10〜20dB 潰して下に混ぜる。サビで手拍子（クラップ）を1打おきに重ねて広がりとアタックを足す（Machine）。
- 【実装値】
  - 胴（トーン）: 三角波 180〜220Hz（チューニング）、減衰 120〜200ms
  - 響き線（ノイズ）: ホワイトノイズ → Bandpass 4kHz（Q 0.6）+ Highpass 1.5kHz、減衰 150〜250ms
  - EQ: Highpass 90Hz、Peaking 200Hz +2dB、Peaking 900Hz −2dB（Q 1.5）、Peaking 3.5kHz +3dB（Q 0.8）、Highshelf 9kHz +1.5dB
  - コンプ: threshold −20dB, ratio 4, attack 0.003s, release 0.08s（6〜8dB）
  - スネアのリバーブ（プレート）: 減衰 1.2〜1.8s、プリディレイ 15〜25ms、HPF 400Hz、LPF 8kHz、送り −14dB。ブレイクの直前の最後の一打だけ送り +6dB で「投げる」。
  - ゴーストノート: 強さ 15〜30%、音量 −18〜−12dB（グルーヴのため。単調さをなくす）

### 4-3. シンバル（人間の好み: たたいたら鳴りを伸ばす、ライドは伸びて鋭く）

- 【出典】シンバルの耳に痛い所は 6〜10kHz（例 8kHz）。動的 EQ で耳に痛いときだけ下げる（Drum Mixing FAQs）。
- 【出典】Jason Richardson / Luke Holland の録音: オーバーヘッドで 300Hz を削り、391Hz 以下を棚で下げ、1.5kHz からの広い高域棚で空気感。コンプは軽く、アタック遅めでスティックの当たりを通す。ハイハット・ライド・スタックは別マイクで、ライドは忙しい部分で上げる。
- 【出典】Andy Sneap: シンバルはいちばん難しい要素の一つ。
- 【出典】ブレイクダウンの刻みの間はシンバルを 2〜3dB 下げる。最初のクラッシュだけ長く暗いプレートを送る（Breakdowns）。
- 【実装値】
  - クラッシュ: 減衰 2.5〜4s（**途中で止めない**。次のクラッシュが来ても前の余韻は 200ms かけて自然に下げるだけ）。Highpass 350Hz、Lowshelf 400Hz −3dB、Highshelf 1.5kHz +1.5dB、Peaking 8kHz −2dB（Q 2）。
  - チャイナ: 減衰 1.5〜2.5s、Bandpass 寄り（Peaking 3kHz +2dB）、左右どちらかに ±0.5。
  - ライド: 打ち（ピン）は Peaking 4〜5kHz +3dB（Q 2）で鋭く、減衰（ウォッシュ）3〜5s。ベル打ちは 1.2〜2kHz を +3dB、減衰 2s。サビや速い部分で +1.5dB。
  - ハイハット: Highpass 500Hz、Peaking 10kHz +1dB。開きは 300〜800ms、閉じは 40〜80ms、半開きを入れて変化を出す。
  - スタック（重ねたシンバル）: 減衰 150〜300ms、Peaking 2.5kHz +2dB。
  - シンバルは**オーバーヘッドバス**にまとめてコンプ（threshold −14dB, ratio 2.5, attack 0.03s, release 0.3s, 2dB 以下）。速い release だと余韻が「吸い込まれる」ので遅めに。

### 4-4. タム

- 【出典】Andy Sneap 系: タムとスネアのマイクはゲートでシンバルのかぶりを消し、強く圧縮してフィルを均一に。BTBAM ではタムの音でギターバスの 100〜150Hz を下げる（タムの低域を通すため）。
- 【実装値】
  - ハイタム 160〜200Hz、ミッドタム 120〜150Hz、フロア 80〜100Hz（音程を 30〜50ms で少し下げる）。減衰 400〜900ms（フロアは長め）。
  - Peaking 4kHz +2dB（アタック）、Peaking 400Hz −3dB。
  - パンは左（ハイ）→右（フロア）にドラマー視点で ±0.5 程度。
  - タムが鳴る瞬間だけギターバスの 100〜150Hz を −2〜−3dB（サイドチェイン）。

### 4-5. ルーム（部屋鳴り）とパラレルコンプ

- 【出典】Jens Bogren: 部屋マイクは常に鳴らすとアタックがぼける。テンポに合ったディレイの方を好む。ドラムは近いマイクを主にして、トリガーは支えるだけ。部屋マイクは 3m 先のブルームライン、モノラル、広い AB など。
- 【出典】Architects: ルームマイクなしで録ったドラムに、胴（シェル）だけを大きなホールリバーブに送って大きさを出す。アタックはドライのまま。
- 【出典】Dan Lancaster: ルームはテープ系の飽和を明るい設定でかけてザラつきを足す。
- 【出典】パラレルコンプ: 比率 8:1〜20:1（∞ でも）、1176 系で 10〜20dB。圧縮前に 100〜150Hz 以下を切ってキックでポンピングしないように。圧縮後に 5〜10kHz と 200〜400Hz を上げ、400〜600Hz を削る。音量 0 から上げて下に敷く（Parallel Compression）。
- 【出典】ドラムバス（SSL 型）: アタック 30ms（最も遅い）、リリース 100ms かオート、4:1、大きい打で 3〜4dB（Zakk Cervini）。ブレイクダウンだけドラムバスの飽和を 20〜30% 上げる。
- 【実装値】
  - **ルーム**: キック以外（スネア・タム・シンバル）を ConvolverNode（部屋の IR、0.6〜1.2s）へ送り、出口で DynamicsCompressor（threshold −30dB, ratio 10, attack 0.01s, release 0.15s）で強く潰し、Highpass 200Hz、Lowpass 9kHz。音量はドライに対して −14〜−10dB（静かな部分は −16dB、サビは −10dB）。
  - **胴だけの大きなリバーブ**: スネアとタムだけ、ホール 2〜3s、プリディレイ 30ms、HPF 300Hz、送り −18dB。
  - **パラレルコンプ**: ドラムバスのコピー → Highpass 120Hz → DynamicsCompressor（threshold −35dB, ratio 20, attack 0.001s, release 0.1s）→ Peaking 300Hz +2dB → Peaking 500Hz −3dB → Highshelf 7kHz +2dB → 音量 −12dB から上げる（目安 −9dB）。
  - **ドラムバス**: DynamicsCompressor（threshold −14dB, ratio 4, attack 0.03s, release 0.1s, knee 3）、3〜4dB。

---

## 5. 全体（帯域のすみ分け・サイドチェイン・音圧・マスター・広がり）

### 5-1. 帯域のすみ分け・置き場所

- 【出典】前景（歌）・中景（リズムギターとスネア）・背景（E-Bow、パッド、テクスチャー）の 3 層で考える（BMTH の記事）。
- 【出典】ミックスは一番うるさいところ（最後のサビ）から作る。まずドラム → ベース・ギター・歌の芯 → 飾りは最後（Dan Lancaster）。
- 【実装値】
  - 中央に置くもの: キック・スネア・ベース・歌・ソロ。左右に開くもの: リズムギター（±1.0 / ±0.75）、ハモり（±0.5）、アンビエント層（±0.6〜0.9、ステレオのリバーブ）。
  - 奥行き: 前に出すものはリバーブを少なく・高域を残す。奥に置くものは Lowpass 5〜7kHz、リバーブ多め、プリディレイ短め、音量 −6〜−12dB。

### 5-2. サイドチェイン（ダッキング）

- 【出典】キックでベースを下げる: 3〜6dB、比率 4:1、アタック最速（0.1ms）、リリース約 50ms から（Sidechain 記事）。ギターは 3dB 以下、パーカッション類は 1〜2dB。キックの信号は部屋鳴りのない直接の音を使う。スネアでベースとギターを下げるときはアタックを遅めにして、余韻の部分だけ下げる（Volumes）。
- 【出典】歌でリズムギターを下げる: 2:1、1〜2dB、500Hz〜3kHz だけでもよい。
- 【出典】Zakk Cervini 系: ボーカルのディレイを歌でダッキングし、歌っていない間に響かせる。
- 【実装値】（Web Audio の DynamicsCompressor はサイドチェイン入力がないので、**ノートの時刻からゲインのエンベロープを作る**のが確実）
  - キック → ベースバス: 打った瞬間 −4dB、1ms で下げ、50〜70ms で戻す（指数カーブ）。
  - キック → ギターバス: −2dB、1ms で下げ、40〜60ms で戻す。低域だけ下げたいときは、ギターバスを 250Hz で上下に分けて下側だけ −3dB。
  - スネア → ギターバス: −1dB、10ms で下げ、120ms で戻す（余韻の部分）。
  - 歌・リード → ギターバスの 1〜3kHz: −1.5dB（音が鳴っている間）。
  - リード → ディレイ/リバーブの送り: −4〜−6dB（2 章参照）。
  - 人間の過去の指示: パートごとに数値で整え、最後に全体を整える。ダッキングは「ぐじゃぐじゃ感」を減らすのに効く。

### 5-3. 音圧（LUFS）とマスター

- 【出典】配信向けのメタルは −7〜−5 LUFS（積分）が多い。配信は約 −14 LUFS に下げられる。リミッターの上限 −0.3〜−1.0dBTP。リミッターの前にクリッパーで 1〜2dB。サイド成分（左右の差）に 120〜150Hz の HPF をかけて低域をモノラルにする。80〜200Hz のダイナミック EQ で一番大きいミュートだけ下げる（Mastering FAQs）。
- 【出典】Dan Lancaster のマスター: SSL バスコンプ 3〜5dB、アタック 30ms、リリース速め、4:1。API で 8kHz と 16kHz を上げて明るく。最後の音圧用リミッターは確認用で、マスタリングに出す前に外した。
- 【出典】Jens Bogren: クリップ（AD かデジタル）をリミッターより好む。出力の上限は約 −0.2dB（配信向けは約 −1dB）。
- 【出典】Jordan Fish: 音圧を追うと低いサブが削られる。ミックスバスに 1176 系を「ラップのように」軽く。
- 【実装値】（このソフトの標準「B」= **−13.5 LUFS・widen 1.0** を守る）
  - マスターの順番: 
    1. Highpass 25Hz（24dB/oct、聞こえない低域を消す）
    2. 低域のモノラル化: M/S に分け、S（左右の差）に Highpass 140Hz
    3. 80〜200Hz の動的な抑え（帯域分割 + DynamicsCompressor threshold −20dB, ratio 3, attack 0.005s, release 0.1s、2dB 以内）
    4. バスコンプ: threshold −10dB, ratio 4（強すぎるなら 2）, attack 0.03s, release 0.1s, 2〜3dB
    5. EQ: Highshelf 8kHz +1dB、Peaking 16kHz +0.5dB（明るさ）、Peaking 300Hz −0.5〜−1dB（濁りの最後の掃除）
    6. ソフトクリップ（WaveShaper のなめらかな曲線、4x）で 1〜1.5dB
    7. リミッター（先読みつきの自作が望ましい）上限 −1.0dBTP
    8. 音量を −13.5 LUFS に合わせる
  - −13.5 LUFS なら強いリミットは不要。**リミッターでの圧縮は 2dB 以内**にして、キックとスネアの当たりを残す（大きい市販曲より「強弱」が残るのがこのソフトの強み）。
  - ステム（パートごとの書き出し）を確認用に出す。

### 5-4. 広がり

- 【出典】強い HPF/LPF は左右の広がりを狭く感じさせることがあるので、全体で確認（Jens Bogren / Leprous）。広がりはギターの別テイク（4本重ね）と左右の微妙な違いで作る。ブレイクの前の小節で狭め、頭で広げる自動化（Breakdowns）。
- 【実装値】
  - マスターで左右を人工的に広げない（widen 1.0）。広がりはギター4本の配置・左右で違うディレイ（4分 / 付点8分）・ステレオのリバーブで作る。
  - ブレイクの1小節前にギターの pan を ±1.0 → ±0.6 に寄せ、頭の一拍で ±1.0 に戻す（200ms かけて）。

---

## 6. シンセを使わなくても「現代的」に聞こえる工夫

- 【出典】BMTH: E-Bow のドローン（持続音）、クリーンや E-Bow の質感、和音のレイク（かき鳴らし）、トレモロのギターで動きを出す。背景に置く。
- 【出典】Architects: アンビエントのリードは、ギターに揺れのあるリバーブなどを大量にかけたもので、パッドの役割をする。ミックスの最初の 1 時間でリバーブとディレイを作る。
- 【出典】ギターのアンビエント技（bonedo）: (1) ボリューム奏法のパッド — ボリューム → ディレイ → リバーブの順（ボリュームの後ろに置いて余韻を切らない）、ゆっくり上げて素早く下げる、(2) バイオリン風のスウェル、(3) 付点8分ディレイを原音と同じ大きさで1回だけ、(5) バリトン・トレモロ、(6) 2度や開放弦を混ぜた和音や広い三和音、(7) E-Bow。
- 【出典】ブレイクダウンの演出: 直前 1〜2 小節でマスターを約 1.5dB 下げ、頭で 0dB か +1dB に。キック・スネア・ギターを 1〜2dB 上げる。盛り上げ中にローパスを閉じ、頭で開く。ギターとベースのハイパスを徐々に上げて薄くする。逆再生シンバルで溜め、頭で切る。直前の最後のスネアに大きく暗いリバーブを投げ、ぴたりと切る。最初の一打の下に根音のサイン波のサブドロップ（速いピッチの下がり）（Breakdowns）。
- 【出典】Machine: 逆再生シンバル（チャイナなど）は山が「その瞬間の直前」に来るように置く。爆発音・サブドロップはバンドが戻る「1拍目」に、まず HPF 148Hz で小さなスピーカーで合わせてから低域を戻す。サビで歓声を短く。
- 【出典】テープストップ: 再生速度が下がる＝音程と速さが同時に落ちる。4 小節の終わりにドラムバスで止める、など（Attack Magazine）。
- 【実装値】
  - **ボリューム・スウェル**: クリーンか軽い歪み。音量 0 → 最大を 250〜600ms（曲線は指数の逆、ゆっくり始めて速く上がる）、ディレイ 付点8分・フィードバック 40〜55%・ミックス 35%、リバーブ 4〜8s、プリディレイ 0〜20ms、HPF 300Hz、LPF 5kHz。ディレイとリバーブはスウェルの**後ろ**につなぐ。
  - **E-Bow 風の持続音**: 歪み軽め（k=3〜5）、立ち上がり 400〜800ms、サステイン無限、音の終わり 1〜2s。倍音を少し揺らす（1.2kHz 付近の Peaking を 0.2Hz で ±1dB）。**コーラスは掛けない**（人間が嫌う「きゅいんきゅいん」）。ビブラートも深くしない（±10 セント以下）。
  - **トレモロ・ピッキングの層**: 16分か32分で同じ音、背景に −10dB、リバーブ多め。
  - **シマー風（オクターブ上のリバーブ）**: リバーブの戻りの一部をオクターブ上にピッチシフト（Web Audio では、リバーブ IR をオクターブ上の倍音を強めた IR にするか、再生速度 2 倍の IR を混ぜる）、戻り −18dB、減衰 6〜10s。
  - **逆再生**: クラッシュやギター和音の余韻を AudioBuffer で反転し、山の位置を目的の拍の 20〜50ms 前に置く。長さ 1〜2 拍。音量は −6dB から。
  - **テープストップ**: AudioBufferSourceNode の `playbackRate` を 1.0 → 0.05 へ 300〜800ms（1/2〜1 拍）で指数的に下げる（音程も一緒に下がる）。最後の 30ms で音量を 0 に。使う場所はブレイク直前・曲の終わりなど 1 曲に 1〜2 回まで。
  - **フィードバック（ハウリングの持続音）**: 伸ばしている和音の最後に、根音の 2 倍か 3 倍（オクターブか 5 度上）のサイン波＋軽い歪みを 1〜2s かけて −30dB → −12dB に上げる。わずかなピッチの揺れ（±5 セント、0.3Hz）。
  - **ハーモナイザー／ワーミー風（ピッチを上下）**: 1 オクターブ上の音を 100〜300ms で滑らせる（`detune` を自動化）。オクターブ下を重ねて太くする（−6dB）。
  - **リバーブ投げ・ディレイ投げ**: 区切りの最後の一音だけ送りを +6〜+10dB、次の頭で 50ms かけて 0 に戻す（余韻は自然に消える）。
  - **ブレイク前の「間」**: 1/8〜1 拍の無音（ただしシンバルの余韻と投げたリバーブは残す。人間の好みでも「すぐミュート」はあり得ない）。
  - **フィルターの自動化**: 盛り上げで ギター・ベースのバスに Highpass 100Hz → 600Hz（2〜4 小節）、頭で 100Hz に戻す。イントロでバンド全体を Lowpass 800Hz（「隣の部屋で鳴っている」感じ）から開く。
  - **最初の一打の強調**: 爆発・インパクト系は手元にないので、キック重み層を −12 半音分さらに下げたサブドロップ（50Hz → 30Hz を 0.8〜1.5s）と、逆再生シンバル、クラッシュ＋チャイナ同時打ちで代用。
  - **2本のギターでの「質感の対比」**: 片方は歪み、片方は同じ和音のクリーンのアルペジオ（リバーブ多め、コーラスなし）を背景で重ねる。

---

## 7. このソフトに入れるときのチェック項目（人間の好みとの対応）

- ギターの「割れ」「ピー」: ゲイン k を下げる・4x オーバーサンプリング・キャビ LPF を 24dB/oct で 5.5〜7kHz・4〜8kHz の狭い削り。
- 曲の頭をブリッジミュートの刻みにしない。刻みとブリッジミュートの多用を避け、伸ばす和音・アンビエント層・リードで頭を作る。
- 音をすぐ止めない（シンバル 2.5〜5s、和音の余韻 300ms〜1.5s）。
- クリーンにコーラスを掛けない。リードの crunch（ピロピロ）は使わない。ビブラートは浅く。
- ラウドのベースは明るくゴリッと（歪み層の 1.2kHz を上げ、300Hz を削る）、指弾き。
- キックはトリガー層＋重み層の 2 層以上。
- ドラムは単調にしない（ゴーストノート、ライド・タム・フロア、ハーフタイム、間）。
- 書き出しは −13.5 LUFS・widen 1.0（B）。

---

## 出典 URL 一覧

### 記事・インタビュー（本文を読んだもの）
1. Sound On Sound「Inside Track: Architects & Bring Me The Horizon（Jordan Fish）」 https://www.soundonsound.com/techniques/inside-track-architects-bring-me-horizon
2. Sound On Sound（Dan Lancaster / Bring Me The Horizon『That's The Spirit』のミックス） https://www.soundonsound.com/node/4912271
3. Gearspace「Interview: Jens Bogren」 https://gearspace.com/board/interviews/1414494-interview-jens-bogren.html?nojs=1
4. Mix（mixonline）「Getting Heavy with Will Putney」 https://www.mixonline.com/recording/getting-heavy-with-will-putney
5. Nail The Mix「How Zakk Cervini Crafts Modern Metal's Polished Aggression」 https://www.nailthemix.com/?p=11587
6. Nail The Mix「Jens Bogren's BTBAM Rhythm Guitar Tone and Mixing Tricks」 https://www.nailthemix.com/?p=9186
7. Nail The Mix「Jens Bogren: boosted vs unboosted layers (Leprous)」 https://nailthemix.com/jens-bogren-leprous-rhythm-guitar-mix
8. Nail The Mix「Guitar Mixing FAQs」 https://www.nailthemix.com/guitar-mixing-faqs
9. Nail The Mix「How To Quad Track Guitars」 https://www.nailthemix.com/quad-tracking-guitars
10. Nail The Mix「Noise Gate For Metal Guitars」 https://nailthemix.com/noise-gate-for-metal-guitars
11. Nail The Mix「How to Mix Low Tuned Guitars」 https://www.nailthemix.com/?p=11399
12. Nail The Mix「Spiritbox Plugin: How Mike Stringer Gets His Guitar Tone」 https://nailthemix.com/spiritbox-plugin
13. Nail The Mix「The Andy Sneap Sound」 https://www.nailthemix.com/?p=11586
14. Nail The Mix「SM57 Microphone」 https://www.nailthemix.com/sm57-microphone
15. Nail The Mix「How to Use Delay on Metal Guitars」 https://www.nailthemix.com/how-to-use-delay-on-guitars
16. Nail The Mix「How To Get That Clanky Metal Bass Tone」 https://nailthemix.com/how-to-get-that-clanky-metal-bass-tone
17. Nail The Mix「Handling Different Types of Bass in Your Metal Mix」 https://www.nailthemix.com/different-types-of-bass
18. Nail The Mix「How To EQ Metal Bass Guitar (Sylosis)」 https://nailthemix.com/sylosis-bass-scoop-metal-mix-clar
19. Nail The Mix「Kick Drum EQ for Modern Metal Mixes」 https://www.nailthemix.com/kick-drum-eq
20. Nail The Mix「Crafting a Modern Metalcore Kick Drum Sound (Wage War)」 https://nailthemix.com/wage-war-andrew-wade-metalcore-kick
21. Nail The Mix「How To EQ Metal Kick Drums w/ Joey Sturgis」 https://nailthemix.com/how-to-eq-metal-kick-drums-w-joey-sturgis
22. Nail The Mix「Metal Drum Mixing FAQs」 https://www.nailthemix.com/drum-mixing-faqs
23. Nail The Mix「Mixing World-Class Drum Cymbals (Luke Holland & Jason Richardson)」 https://nailthemix.com/jason-richardson-drums-taylor-tactics
24. Nail The Mix「Parallel Compression」 https://nailthemix.com/parallel-compression
25. Nail The Mix「Sidechain Compression for Insanely Punchy Metal Mixes」 https://nailthemix.com/sidechain
26. Nail The Mix「Sidechain Everything to the Kick (Volumes)」 https://www.nailthemix.com/volumes-kicks-hold-up-sidechain-fixes
27. Nail The Mix「Mastering FAQs」 https://www.nailthemix.com/mastering-faqs
28. Nail The Mix「How to Mix Metal Breakdowns That Hit Harder」 https://www.nailthemix.com/?p=12455
29. Nail The Mix「Machine's Post-Production FX: Explosions, Reverses & Sub Drops」 https://www.nailthemix.com/?p=10170
30. Nail The Mix「Balancing heavy guitars with electronic layers and Ebow drones (BMTH)」 https://www.nailthemix.com/?p=9498
31. Nail The Mix「Building reverb and delay from scratch (Architects)」 https://www.nailthemix.com/?p=9488
32. Nail The Mix「Start Mixing From the Loudest Section (BMTH / Dan Lancaster)」 https://nailthemix.com/bmth-drums-lancaster-core-strategy
33. Riffhard「How to Get a Metalcore Guitar Tone」 https://www.riffhard.com/how-to-get-a-metalcore-guitar-tone/
34. Violet Recording「What Is a Tube Screamer?」 https://violetrecording.com/what-is-a-tube-screamer/
35. Music Guy Mixing「Delay Settings For Lead Guitar」 https://www.musicguymixing.com/delay-settings-for-lead-guitar/
36. bonedo「Die 7 besten Ambient- und Atmo-Soundtricks für Gitarre」 https://www.bonedo.de/artikel/die-7-besten-ambient-und-atmo-soundtricks-fuer-gitarre
37. Attack Magazine「Creative tape stop effects」 https://www.attackmagazine.com/technique/tutorials/creative-tape-stop-effects/
38. Metal Injection「Toontrack Metal Month: Exclusive Interview with Andy Sneap」 https://metalinjection.net/interviews/toontrack-metal-month-exclusive-interview-with-andy-sneap

### 見つけたが本文が読めなかった・内容が薄かったもの
- Tape Op「Will Putney」（有料部分のため技術の話は読めず） https://tapeop.com/interviews/154/will-putney
- Toontrack「Producer Profile: Will Putney / Drew Fulk（WZRD BLD）」（記事一覧のみで技術情報なし） https://toontrack.com/news/producer-profile-will-putney/page/37 ・ https://www.toontrack.com/news/producer-profile-drew-fulk/page/3
- URM Academy「Podcast EP302 Zakk Cervini」「EP190 Dan Lancaster」（音声のため未読） https://urm.academy/urmpc302-zakk-cervini ・ https://urm.academy/ep190-dan-lancaster
- ElectroSmash の Tube Screamer 回路解析はツールの制限で取得できず（TS の約 720Hz の値は一般に知られている回路の値として記載）。

### 注意
- Joel Wanasek と WZRD BLD（Drew Fulk）は、本人の数値つきの解説を本文で確認できなかった（Joel の名前は Nail The Mix の「Clanky Bass」記事の手順に出てくる）。
- 出典の多くは Nail The Mix（教育サイト）の要約記事。実際の名プロデューサーの発言として確実なのは Sound On Sound（Jordan Fish、Dan Lancaster）、Gearspace（Jens Bogren）、Mix（Will Putney）。
