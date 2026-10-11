# ミックスのパターン集（2026-10-11 調査）

テーマ: **バラバラの楽器を、一つの曲として聞こえるようにまとめる**。ネットの解説（文末の54件。本文を読めたもの。要約経由が多い）から、「まとめる」ための型を集め、うちの作曲ソフトで実際に設定できる数字に落とした。

関係する文書（重ねて書かない）: `mixing-guide.md`（EQ・コンプ・残響の一般値、実験記録）、`layering-guide.md`（音域・リズムの重ね方）、`sound-design-basics.md`（つまみの対応表）、`punk-guide.md`（パンクの録音分析）、`guitar-tone-basics.md`（ギターの音）、`sound-sets.md`（セットの仕組み）。本書は**「型（レシピ）」の一覧**と**症状からの逆引き**が中心。

**数字の読み方（先に必ず）**
- 出どころは3種類。**(出)** 記事に書かれていた数値／**(う)** うちの既存文書・コードで確かめ済みの値／**(推)** 記事の方針をうちの道具に読み替えた私の推定。どれも**出発点**で、最後は耳と `analyze.py --bands` で決める。
- パートの `volume` は、`clear-guitar-rock`（キック .09・スネア .065・ベース .095・リード .09・ギター .2 …）の目盛りに合わせた。ドラムの音源（`--drums rock` など）を替えると基準が変わる（`punk-run` はキック .03）ので、**比率で使い、合計を 0.9 以下に**そろえる（0.9 を超えるとサウンドセットは自動で縮める。本書の数字は合計 0.35〜0.8）。
- 書き方: `楽器 音量 p=左右 r=reverb c=chorus b=bright d=duck`。`p-.6` は左、`b-.2` は丸く、`d.25` はキックで25%凹む。
- 書き出しの引数は、`song.mjs build 曲.json --wav` に足す。**書き出しの WAV にだけ効く**（ゲーム中の再生は変わらない）。

## 1. 要点

1. 「まとまる」とは、**全部の音が同じ一つの部屋・同じ一つの音量の物差し・同じ一つの接着剤の中にいる**こと。そのために、**4つの席**を各パートに割り当てる: **周波数（どの帯域）／左右／前後（ドライ〜ウェット）／時間（いつ鳴るか）**。
2. うちの道具では、EQ・コンプ（パートごと）が無いので、**編曲（音域・休符・音量）で席を作り、仕上げは「書き出しの3つ」（`--master` 軽い圧縮＋音量そろえ、`--space` 共通の部屋、`--widen` 幅）で接着**する。
3. 接着（バスコンプ）は**軽く**。記事は共通して「2:1前後・1〜2dB」(出)。うちの `natural` の曲は 2.2:1 のやさしい圧縮、それ以外は 4:1 の強い圧縮なので、**起伏を残したい曲は `natural`**。
4. **低域は中央・モノ、広がりは中高域**に。`--widen` は全帯域に効く（ffmpeg の extrastereo）ので、ベース・キックを中央に置き、低音が重い曲は 1.5 以下に。
5. 共通の残響（`--space`）は**接着剤**、パートごとの `reverb` は**遠近の差**。両方を使い、キックとベースには残響を足さない。
6. 主役と脇役の差は**階層で決める**（主役1／準主役.6／脇役.35／空気.2）。全部を同じ大きさにしない。
7. ゲームの曲は**効果音と1〜4kHz を分け合う**。BGM は 2〜3dB 控えめにし、場面で下げる（出: 数dB下げて、前後0.5秒ほどで戻す）。
8. 症状は**帯域**で考える: こもり=200〜500Hz、痛い=2〜8kHz、濁り=60〜250Hz、スカスカ=80〜250Hz。直す順は「音量→音域→左右→残響→書き出し」。
9. 測って確かめる: `analyze.py --bands`（帯域）、`third-octave.py`（1/3オクターブ）、相関 0.4〜0.88、crest 10dB 以上、LRA 4 以上。
10. **ミックスの型は「選ぶもの」**。曲の種類（ジャンル・場面）から型を1つ選び、その数字を出発点にして、1回に1か所だけ動かす。

## 2. まとめる10の原則（根拠つき）

| # | 原則 | 根拠 | うちでの形 |
|---|---|---|---|
| 1 | **足す前に引く**。濁ったら新しい音を足さず、今ある音を減らす | EQで一度に3dB以上削る必要があるなら音源を見直す(出32,33)。トラックを加える前に不要なものを外す | 重なる脇役の `volume` を20〜30%下げる／音域を上げる／休符 |
| 2 | **低域は少数精鋭で中央・モノ** | キック・ベースは中央、100〜200Hz以下はセンター(出7,12,5)。低域を広げると位相と濁りが出る(出31) | kick・bass・sub808 は `pan` 0。低音のパートは3つまで |
| 3 | **キックとベースは交代する** | サイドチェイン: キック→ベースで 5:1・アタック4ms・リリース60ms 程度(出15)、またはキックをHPF/ベースを削る | `duck` .2〜.35、ベースは短く（sustain .6〜.8）、音域は 80〜120Hz 以上 |
| 4 | **遠近は音量・明るさ・残響で作る** | 乾いた音は近く、湿った音は遠い。前は短い残響・後ろは長い(出11,22,4) | 主役 `reverb` .1〜.2／脇役 .25〜.35／背景 .45〜.6、`bright` を奥ほど下げる |
| 5 | **共通の残響で空間をそろえる** | 複数トラックを共通の残響に送ると同じ空間に聞こえる。ただし全部に同じだと平らになる(出4,11) | `--space room\|plate\|hall` ＋パートごとの `reverb` の差 |
| 6 | **接着は軽く** | バスコンプ 2:1・1〜2dB・自動リリースかテンポに合う(出1,10,18)。ジャズは 1.1:1(出13) | `natural` の内蔵圧縮に任せ、`--master` を下げすぎない |
| 7 | **階層で音量を決める** | 重要なものから上げる。ロック/メタルはキック・スネア→歌→ベース→リズムギター(出14)。ポップは歌が基準(出34) | 主役1／準主役.6／脇役.35／空気.2（§5） |
| 8 | **ゲインステージング** | 各トラック平均 -18dBFS、バスは -10 より下、マスターは -6 を超えない(出54,8)。ヘッドルームは後で上げる方が安全 | `volume` の合計 0.9 以下（本書のパターンは 0.35〜0.8）。小さく書いて `--master` で大きさをそろえる |
| 9 | **帯域・位置・時間の席取り** | 同じ帯域・同じ位置に主役を2つ置かない。EQは最後の手段(出33,21) | 役割ごとに音域を分け、リズムを噛み合わせる（`layering-guide.md`） |
| 10 | **参照して測る** | 参照曲は2〜3曲、音量をそろえてから、同じ区間（サビ同士）を比べる。1回に1要素(出47,48) | `analyze.py --bands --compare`、モノ確認、3つの再生環境 |

## 3. ミックスのパターン集

凡例の追加: **drumMix** は `楽器 L=level p=pan r=reverb sp=spread t=tune`。**帯域**は `analyze.py` の帯域名（sub 20〜60／bass 60〜250／lowmid 250〜1k／mid 1〜4k／presence 4〜8k／air 8k〜）で、「低」=bass、「中低」=lowmid、「中」=mid、「張り」=presence。dBは全体に対する値で、**§3.0 の表から選んで目標にする**（推）。

### 3.0 帯域の目標の目安（家族別・推）

参考37曲の平均は 低 -3.3／中低 -5.9／中 -11.5／張り -22.9（`mixing-guide.md` §8）。パンクの録音は 中 -5.7／張り -14.5（`punk-guide.md` §7）。これらと記事の傾向から、家族ごとにずらした。**全帯域の合計は 0dB（=100%）を超えない**ように、足し引きして選ぶ。

| 家族 | 低(60-250) | 中低(250-1k) | 中(1-4k) | 張り(4-8k) | 1/3oct 傾き（1kHz基準、1オクターブごと） |
|---|---|---|---|---|---|
| ロック/ポップ/アニソン | -4 | -6 | -8.5 | -17 | -1.5 dB/oct |
| パンク/メタル（ギターの壁） | -5.5 | -5 | -6.5 | -15 | -1 dB/oct（中が主役） |
| EDM/ベースミュージック | -2 | -8 | -12 | -20 | -2 dB/oct（低が主役） |
| ヒップホップ/R&B | -2.5 | -7 | -11 | -22 | -2 dB/oct |
| ジャズ/アコースティック | -4 | -5.5 | -9 | -20 | -1.5 dB/oct |
| ローファイ/バラード | -3.5 | -5 | -13 | -28 | -2.5 dB/oct（暗い） |
| アンビエント/映画/オーケストラ | -5 | -4.5 | -9 | -20 | -1.5 dB/oct |
| ゲーム戦闘/ボス | -4 | -6 | -8 | -16 | -1.25 dB/oct |

1/3オクターブ曲線の作り方（推）: `third-octave.py` の読み出しは定Q（1/3オクターブ幅）なので、ピンクノイズが平ら。傾き s dB/oct なら、1kHz を 0 として **周波数 f の目標 = s × log2(f/1000)**（例: s=-1.5 なら 125Hz=+4.5、250Hz=+3、2kHz=-1.5、4kHz=-3、8kHz=-4.5）。この形の JSON を作って `third-octave.py 書き出し.wav 目標.json` の第2引数に渡す。ギター単体の目標は `data/guitar-curve-5tracks.json`（済）。

### 3.1 「まとめる」技術の型（A群）

#### M01 やさしい接着（natural）
- 向く曲: バラード、ジャズ、映画、ゲームのフィールド。起伏を残したい曲全般。
- パート: 変更なし。合計を 0.9 以下にそろえる（0.7〜0.8 が安全）。
- 書き出し: 曲に `dynamics:"natural"` ＋ `--master -14`。内蔵の圧縮は 2.2:1・しきい値 .2・アタック8ms・リリース140ms(う)で、記事の「2:1・1〜2dB・アタック3〜30ms」(出1,10,18)の範囲。
- 帯域: 全体。LRA 4 以上、crest 11 以上を保つ。
- 注意: `--master` を -10 より上げると、リミッターが先に効いて起伏が減る。

#### M02 パンチ型の接着（4:1）
- 向く曲: ロック、パンク、メタル、EDM、戦闘。`natural` でない曲。
- パート: 変更なし。ドラム（キック・スネア）を相対的に1段上に。
- 書き出し: `natural` を付けず `--master -10`。内蔵は 4:1・しきい値 .12・アタック4ms・リリース90ms(う)。ドラムバスのような攻めた圧縮に近い(出)。
- 帯域: 低〜中を厚く。
- 注意: crest が 9dB を切ったら、`volume` の合計を下げるか `natural` に。ポンピング（リリース90msが拍に合わない）が出たら BPM を確認（1拍=60000÷BPM、速い曲ほど合う）。

#### M03 ゴースト層（パラレル圧縮の代用・推）
- 向く曲: スネア・キックが細い曲、ロック、ポップ。
- パート: 主役のスネアはそのまま、同じ音符の複製パートを足す: `snare .065; snare .016 r.4 b-.25`（複製は主役の約25%＝記事のパラレルは「聞こえ始めたところから1〜2dB戻す」(出2,3)、ここでは-12dB）。
- drumMix: `snare L1.05 r.2`
- 書き出し: `--master -11`
- 帯域: 中低（スネアの胴 200〜250Hz）と残響の尾。
- 注意: エンジンにパラレル圧縮は無い。**似せるだけ**。複製が同時に鳴ると位相が重なって太くなる効果があるので、`push` は 0。聞いて薄くなるなら外す。

#### M04 共通の部屋（room）
- 向く曲: 速いテンポ（BPM 130 以上）、ロック、パンク、ドラムが主役の曲。
- パート: 全パートの `reverb` を .10〜.18 にそろえ、**kick・bass は 0**。主役 .10、脇役 .18。
- 書き出し: `--space room --space-wet 0.15`（room は rt60 0.7秒・プリディレイ8ms・明るい(う)。記事の「リズム楽器は 0.4〜0.8秒の短い残響」(出4)に合う）。
- 帯域: 中低〜中。200〜500Hz が増えたら wet を下げる。
- 注意: 共通の IR はキックとベースにも乗る。濁る（低が +1.5dB 以上増える）なら wet を .08 に。

#### M05 共通の部屋（plate）
- 向く曲: リード（歌相当）が主役のポップ、アニソン、ボカロ風。
- パート: lead `r.18`、伴奏 `r.12`、drumMix snare `r.2`。
- 書き出し: `--space plate --space-wet 0.12`（plate は rt60 1.3秒・プリディレイ4ms・高域が明るい(う)。リードとスネアにプレートが定番(出11,50)）。
- 帯域: 中〜張り。
- 注意: プリディレイが4msと短く、リードが奥に引く。前に出したいなら、リードの `reverb` を .1 に。

#### M06 共通の部屋（hall）
- 向く曲: 遅い曲（BPM 90 以下）、バラード、映画、タイトル、アンビエント。
- パート: 弦・パッド `r.45`、ピアノ `r.25`、リード `r.25`、bass・kick は `r0〜.05`。
- 書き出し: `--space hall --space-wet 0.12〜0.25`（hall は rt60 1.9秒・プリディレイ22ms(う)。記事の 2〜4秒の映画向け(出4)よりは短い）。
- 帯域: 低中〜中低。速い曲では濁る(出)。
- 注意: テンポが速い曲、細かい16分の曲では使わない。

#### M07 奥行き3層（手前・中・奥）
- 向く曲: 編成が6パート以上の曲すべて。
- パート（例）: 手前 `lead .10 r.12 b0`／中 `piano .10 r.25 b-.1; guitar .14 r.25`／奥 `strings .06 r.5 b-.25; bell .04 r.6 b-.3; pad .05 r.55 b-.3`。キックとベースは `r0`。
- 書き出し: `--space room --space-wet 0.12`
- 帯域: 奥のパートは 張り(4k〜)を丸める（`bright` で代用）。
- 注意: 記事の「近い音はドライ・プリディレイなし／遠い音は深い残響と高域減」(出22)の読み替え。`bright` は下げる方向が中心(う)。

#### M08 キックとベースの交代（サイドチェイン代用）
- 向く曲: ロック、ポップ、EDM、ヒップホップ、全般。
- パート: `kick .09; bass .085 b+.15 d.3`（sustain .6〜.8、短く切る）。`duck` はキックの位置で凹み、約0.45拍で戻る(う)。BPM 174 なら約155ms、BPM 70 なら約385ms。
- 書き出し: `--master -11`
- 帯域: 低（60〜120Hz）。キックが埋もれたら `d` を +.05。
- 注意: `d` .4 以上はポンピングが目立つ（そのためのジャンル以外では .15〜.3）。パッドは `d.25`。

#### M09 周波数の席取り（4つの席）
- 向く曲: 7パート以上で濁る曲。
- 配分: 低(60-150Hz)=kick・bass／体(200-500Hz)=**1つだけ**（piano か guitar か strings のどれか）／輪郭(1-4kHz)=lead と、歪みギターのどちらかが主、もう一方は `b-.15` ＋ `volume`×.8／空気(5kHz〜)=hat・bell。
- パート: 体の楽器以外は音域を C4（中央のド）以上に上げる。パッドは C3 以上。
- 書き出し: そのまま。
- 帯域: 中低が目標より +2dB 以上なら席が重なっている。
- 注意: 記事はEQで削る(出21,25)が、うちは**音域の移動と音量**で代用。

#### M10 低モノ・高ワイド
- 向く曲: EDM、ポップ、ゲーム全般。
- パート: kick・snare・bass・sub808・lead は `p0`。パッド・弦・アルペジオは `p±.4〜.8`、`c.2〜.3`。
- 書き出し: `--widen 1.4`（全帯域に効く(う)ので、低音が中央の曲だけ。1.5 を超えない）。
- 帯域: 低は変えず、中〜張りの左右差が増える。
- 注意: 記事は低域の 100〜200Hz 以下をモノにする(出7,12)。`--widen` は低域も広げるため、**低域のパートが中央ならサイド成分がほぼ無く、実害は小さい**(推)。相関が 0.3 を下回ったら下げる。

#### M11 LCR（中央・左端・右端の3か所）
- 向く曲: ロック、パンク、メタル、迷いたくないとき。
- パート: 中央=kick・snare・bass・lead／左=リズムギターA・鍵盤／右=リズムギターB・ストリングス。`p-.85 / 0 / .85`。
- 書き出し: `--widen 1.2`
- 帯域: 変わらない。
- 注意: 同じ側に似た帯域を積まない(出)。真ん中を詰めすぎない（kick・snare・bass・lead の4つまで）。

#### M12 ダブルの壁
- 向く曲: パンク、メタル、シューゲイザー。
- パート: 同じリフを2パート、`distGuitar .12 p-.85` と `distGuitar .12 p.85`。片方を5度なし／1オクターブ違いにすると広がる（`punk-guide.md`）。`push` .02 でわずかにずらす。
- 書き出し: `--widen 1.2`（もう壁が広いので控えめ）。
- 帯域: 中（1〜4kHz）が主役の帯域になる。
- 注意: 記事では「ダブルは別々の演奏を左右に」(出5)。ここは同音符なので、コーラス .3 で揺らぎを足すと近づく。

#### M13 ダイナミクス階層（4段）
- 向く曲: すべて。
- 配分: **主役 1／準主役 .6／脇役 .35／空気 .2**（volume の比）。主役=リード、準主役=リズム楽器の核（ドラム・ベース・ギター）、脇役=ハーモニー、空気=ベル・シンバル・残響。
- 書き出し: そのまま。
- 帯域: 張り(4k〜)は「空気」の段のみ。
- 注意: 同じ段に3つ以上置かない（団子の元）。比は §5 の表。

#### M14 ゲインステージング（合計と出口）
- 向く曲: すべて。
- パート: 合計 `volume` = 0.9 以下（本書のパターンは 0.35〜0.8。0.7〜0.8 が安全）。0.9 超は自動で縮む(う)。曲全体を小さく書いて、大きさは `--master` に任せる。
- 書き出し: `--master -12`（ゲームは -14〜-10 の範囲で揃える。`mixing-guide.md`）。
- 帯域: —
- 注意: 合計を0.4倍・0.6倍にして max_volume が上がるなら、リミッターがかかっている（`punk-guide.md` §8）。

#### M15 参照曲との並べ方（手順の型）
- 向く曲: 仕上げ。
- 手順: 近いジャンルの2〜3曲を選ぶ(出47)／LUFS を ±0.5dB で揃える／同じ区間（サビ同士）(出47)／帯域→音量バランス→幅→ダイナミクスの順に1要素ずつ(出48)／モノで確認。
- 書き出し: `analyze.py --bands --compare`（参考37曲）。
- 注意: 音の質ではなく**数字の傾き**を見る。同じ傾きの曲をそろえる。

#### M16 引き算ミックス
- 向く曲: 濁った曲、パート数の多い曲。
- 手順: 最も目立つ脇役から順に `volume` を ×.8 にし、聞き比べる／消しても主役が変わらないパートは削る／最後に主役を +10%。
- 書き出し: そのまま。
- 注意: 「新しいトラックを足す前に、要らないものを外す」(出32)。

### 3.2 ジャンル・編成のパターン（B群）

#### M17 ロックバンド（4人: ドラム・ベース・ギター2・リード）
- 向く曲: ギターロック、バンド編成のゲーム曲。
- パート: kick .09; snare .065 r.15; hihat .03; crash .032; tom .05; bass .09 b+.2 d.25; crunch .13 p-.8 r.1; crunch .13 p.8 r.1; leadGuitar .10 r.2
- drumMix: hat L.7 p-.3 r.08; snare r.15; tom sp.6 r.12; crash L.9 p.3 r.2
- 書き出し: `--master -10 --widen 1.4 --space room --space-wet 0.12`
- 帯域: 低 -4／中低 -6／中 -9／張り -17。
- 注意: リードとリズムギターが 1〜4kHz で重なる。crunch は音域を E2〜E4、`b-.1`。リードは中央・ギター2本の0.77倍。

#### M18 ロックバンド（5人: ＋キーボード）
- 向く曲: ポップロック、アニソン風バンド。
- パート: kick .085; snare .06 r.15; hihat .028; crash .03; tom .045; bass .085 d.25; crunch .11 p-.8; crunch .11 p.8; leadGuitar .10 r.2; piano .07 p.35 r.25 b-.15
- drumMix: hat L.65 p-.3; snare r.15; tom sp.6; crash L.85 p.3 r.2
- 書き出し: `--master -10 --widen 1.4 --space room --space-wet 0.14`
- 帯域: 低 -4／中低 -6／中 -8.5。
- 注意: 鍵盤は右に寄せ、ギターが休む所でコードを埋める。体の席(200〜500Hz)は鍵盤かギターのどちらかに。

#### M19 疾走パンク
- 向く曲: 2ビートの速い曲（BPM 160〜210）。
- パート: `--sound punk-run` に準拠: kick .03; snare .054; hihat .045; crash .055; tom .033; bass .026 b+.5 d.15; distGuitar .12 p-.55; crunch .12 p.55; leadGuitar .09 r.2; echoGuitar .06 r.2
- drumMix: hat L1.05 p-.3 r.05; snare L1.15 r.15; tom sp.6 r.12 t-3; crash L1.0 p.3 r.25
- 書き出し: `--sound punk-run`（master -10 が入る）。`--space room --space-wet 0.1` を足してもよい。
- 帯域: 低 -5.5／中低 -5／中 -6.5／張り -15（`punk-guide.md` §7, §9）。
- 注意: ギターは1〜4kHz が主役の帯域。ギターが痩せたら `volume` を上げる前にベースを下げる。この行はドラム音源 rock の目盛り。

#### M20 ガレージ/ローファイロック
- 向く曲: 荒い録音風、インディー、ゲームの酒場。
- パート: kick .08 b-.3; snare .06 b-.3 r.2; hihat .022 b-.4; bass .09 b-.2 d.15; crunch .15 p-.4 b-.2; crunch .1 p.5 b-.2 c.15; leadGuitar .08 b-.25 r.25
- drumMix: hat L.5 p-.35 r.1; snare r.25; tom sp.5
- 書き出し: `--master -12 --space room --space-wet 0.22`（widen なし）。
- 帯域: 低 -3.5／中低 -5／中 -10／張り -24。
- 注意: 全パートの `bright` を下げ、高域を丸める（`bright` は下げ方向が効く(う)）。

#### M21 メタル（タイトな低域・ギターの壁）
- 向く曲: ボス戦、ヘビーな戦闘。`tone:"metal"`。
- パート: kick .10 b+.3; snare .06; tom .05; hihat .026; crash .03; bass .085 b+.4 d.35; distGuitar .12 p-.9; distGuitar .12 p.9; leadGuitar .10 r.2
- drumMix: kick L1.1; snare L1.05 r.1; hat L.6 p-.25 r.04; crash L.8 p.3 r.2; tom sp.8 r.1
- 書き出し: `--master -9 --widen 1.2`（hall は使わない）。
- 帯域: 低 -4.5／中低 -7／中 -7.5。
- 注意: 200〜500Hz を作りやすいので、ギターの音域は D2 より下を使わない。ベースは `bright` で上の倍音を出して歪みギターの下で聞こえさせる。記事の優先順は「キック・スネア→歌→ベース→ギター」(出14)。

#### M22 ドゥーム/スラッジ（遅くて重い）
- 向く曲: BPM 70 以下の重い曲、ラスボス前。
- パート: kick .09 r.1; snare .06 r.25; tom .06 sp.7; bass .11 b+.1 d.1; distGuitar .12 p-.7; distGuitar .12 p.7; leadGuitar .08 r.3
- drumMix: kick L1.0; snare L1.0 r.3; crash L.7 p.3 r.3
- 書き出し: `--master -11 --space hall --space-wet 0.1`（遅いので hall が使える）。
- 帯域: 低 -3／中低 -6／中 -9。
- 注意: 低が3つ（kick・bass・ギター低弦）あるので、`duck` は弱め(.1)、ギターを少し高い音域に。

#### M23 ポップ（歌=リード主役）
- 向く曲: ポップス、エンディング、イベント。
- パート: leadGuitar .12 r.2 c.1; piano .10 p-.3 r.2; guitar .14 p.4 r.15; strings .05 p-.3 r.35; bell .04 p.5 r.4; bass .085 d.25; kick .08; snare .06 r.2; hihat .028 p.3; crash .03
- drumMix: hat L.6 p.3 r.08; snare r.2; tom sp.5; crash L.8 p-.3
- 書き出し: `--master -11 --widen 1.5 --space plate --space-wet 0.12`
- 帯域: 低 -4／中低 -6／中 -8／張り -16。
- 注意: 歌の席（1〜4kHz）を空けるため、伴奏の1〜4kHz を `b-.1`。ドラムは歌の邪魔にならない小さめ。ミックスの順は「歌→ドラム・ベース→他」(出23,34)。

#### M24 J-POP / アニソン
- 向く曲: ゲームのオープニング、イベント、明るい街、キャラのテーマ。
- パート: leadGuitar .12 r.22 b+.1; guitar .12 p-.5 r.15; crunch .09 p.7 r.1; strings .05 p-.3 r.4; piano .07 p.3 r.25; bass .085 b+.25 d.2; kick .08; snare .06 r.2; hihat .028; crash .03; tom .04; bell .04 p.6 r.35
- drumMix: hat L.65 p-.3; snare r.2; crash L.85 p.3 r.2
- 書き出し: `--master -10 --widen 1.6 --space plate --space-wet 0.14`
- 帯域: 低 -4／中低 -6.5／中 -8／張り -15（明るめ）。
- 注意: 歌（リード）が最大で、サビで全員が上がる。ストリングスは高い音域で歌の隙間を埋める。日本のミックスは歌が前に出る傾向（推。記事の直接の数値は無い）。

#### M25 ボカロ風（高速・リード最大）
- 向く曲: BPM 150〜190 の速い曲、ハイテンポの戦闘。
- パート: leadGuitar .14 b+.2 r.15; piano .08 p-.3 r.15; distGuitar .08 p-.8; distGuitar .08 p.8; lead .05 p.6 c.3 r.2; bass .09 b+.3 d.3; kick .09 b+.2; snare .07 r.15; hihat .035 p-.3; crash .035; strings .05 r.3
- drumMix: kick L1.1; snare L1.1 r.12; hat L.8 p-.3; crash L.9 p.3
- 書き出し: `--master -9 --widen 1.6 --space room --space-wet 0.1`
- 帯域: 低 -4.5／中低 -6.5／中 -7.5／張り -14。
- 注意: 速いので hall は不可。キックの `duck` はリリース0.45拍が速さに追いつくか確認（BPM 180 なら約150ms）。

#### M26 バラード（ピアノ＋弦）
- 向く曲: 悲しい場面、エンディング、静かなイベント。
- パート: piano .16 p-.2 r.25 b-.1; strings .08 p.3 r.45 b-.2 c.2 d.25; leadGuitar .09 r.25; bass .06 b-.1 d.1; kick .05 r.2; snare .03 r.3; hihat .012
- drumMix: kick L.7; snare L.7 r.3; hat L.45 r.1
- 書き出し: `natural` ＋ `--master -15 --widen 1.2 --space hall --space-wet 0.2`
- 帯域: 低 -3.5／中低 -5／中 -12／張り -28。
- 注意: ピアノと弦が 200〜500Hz で重なりやすい。弦は C3 以上、ピアノの左手と離す。弦の `duck` はピアノの打鍵（キックの位置）ではなく、ドラムを入れた曲だけ効く。

#### M27 ジャズトリオ（ピアノ・ベース・ドラム）
- 向く曲: 酒場、大人の街、夜のイベント。
- パート: piano .16 p-.3 r.12; bass .13 p.2 b-.1 r.04; kick .05; snare .04 r.1; hihat .025 p-.2; crash .02 p.3 r.15
- drumMix: kick L.7; snare L.8 r.1; hat L.6 p-.25; crash L.7 p.3 r.15; tom sp.7
- 書き出し: `natural` ＋ `--master -16 --space room --space-wet 0.15`（widen なし）。
- 帯域: 低 -4／中低 -5.5／中 -9／張り -20。
- 注意: ベースをわずかに右、ピアノを左(出6,13)。圧縮はごく軽く（バス 1.1:1 の例(出13)）。残響は短い部屋(出6,9)。ドラムが大きすぎるとジャズらしさが消える（ライドを小さく）。

#### M28 ジャズクインテット（＋ホーン2）
- 向く曲: ビッグな街、パーティ。
- パート: piano .12 p-.4 r.12; bass .11 p.25; brass .10 p-.2 r.15; lead .10 p.2 r.15; kick .045; snare .04 r.1; hihat .025 p-.2; crash .02 p.3 r.15
- drumMix: 上と同じ。
- 書き出し: `natural` ＋ `--master -15 --space room --space-wet 0.18`
- 帯域: 低 -4.5／中低 -5／中 -8.5。
- 注意: ホーンの専用の残響を足す(出9)つもりで `r.15`。ソロ時は伴奏を少し下げる（曲のパート数を減らす）。

#### M29 ファンク
- 向く曲: 明るい街、ダンスの場面。
- パート: bass .13 b+.3 d.15; guitar .12 p-.6 b+.2 r.05; keys .09 p.5; brass .09 p.2 r.1; kick .085; snare .07 r.1; hihat .035 p-.3
- drumMix: kick L1.0; snare L1.05 r.1; hat L.75 p-.3; tom sp.5
- 書き出し: `--master -11 --widen 1.2`
- 帯域: 低 -3／中低 -6／中 -8（ベースが主役）。
- 注意: ベースが主役なので、キックよりベースが大きい（.13 対 .085）。ベースは短く、キックと音の頭をそろえる。ギターは細かい16分で高域に置く（500Hz〜）。ベースを鍵盤で重ねる案は記事あり(出51)。

#### M30 R&B / ネオソウル
- 向く曲: 夜の街、恋愛イベント。
- パート: piano .11 p-.3 c.25 r.25 b-.1; pad .05 p.4 c.3 r.4 b-.2; leadGuitar .11 r.25; choir .06 p.6 r.4; sub808 .10 d.3; kick .08; snare .06 r.25; hihat .02 p.3
- drumMix: hat L.55 p.3 r.1; snare L.95 r.25; kick L.9
- 書き出し: `--master -13 --widen 1.5 --space plate --space-wet 0.15`
- 帯域: 低 -2.5／中低 -7／中 -11／張り -22。
- 注意: 記事は歌の残響 1.8〜3秒・プリディレイ30〜60ms、ハーモニーは広く左右へ(出50)。うちはプレート（rt60 1.3秒）で近づけ、コーラスのパートを `p±.6`。

#### M31 ヒップホップ（ブーンバップ）
- 向く曲: 街の裏路地、闇市。
- パート: piano .10 p-.2 b-.35 c.15; bass .11 b-.2 d.2; kick .10 b0; snare .08 r.12; hihat .02 p.35; bell .04 p.4 r.3
- drumMix: kick L1.1; snare L1.1 r.12; hat L.6 p.35 r.05
- 書き出し: `--master -12 --space room --space-wet 0.12`（widen なし）。
- 帯域: 低 -2.5／中低 -6.5／中 -11。
- 注意: ハットは中央から30〜50%ずらす(出46)。キックとベースの住み分け: キックの音程を下げ、ベースは上の倍音を出す(出38)。

#### M32 トラップ（808）
- 向く曲: 現代的な戦闘、夜の街。
- パート: sub808 .12 d.2; kick .06 b+.3; snare .07 r.2; hihat .03 p-.4; hihat .02 p.4; bell .07 p.3 r.3; pad .04 b-.3 r.5
- drumMix: kick L.9; snare L1.0 r.2; hat L.7 p±.4
- 書き出し: `--master -9 --widen 1.3`
- 帯域: sub〜低 -1.5（808）／中低 -8／中 -12。
- 注意: 808 は根音か5度に合わせる(出26)。キックの低域を削り、アタックだけを残す。808 は `p0`、上の倍音は `bright` で出して小スピーカーでも聞こえるように(出39)。

#### M33 ハウス
- 向く曲: 明るい街、ダンスの場面、カジノ風（賭け要素は作らない）。
- パート: kick .10 b+.2; bass .08 d.4 b+.15; snare .06 r.18; hihat .028 p.3; crash .02 p-.3 r.15; pad .05 p-.3 c.4 d.4 r.35 b-.2; keys .07 p.4 d.3; lead .07 p.2 r.2
- drumMix: kick L1.2; snare L.8 r.18; hat L.6 p.3
- 書き出し: `--master -9 --widen 1.6 --space plate --space-wet 0.1`
- 帯域: 低 -2／中低 -8／中 -11.5。
- 注意: キックがローエンドを取り、ベースは100Hz 以上で性格を出す(出43)。ドラムは「キック0dB、クラップ -3〜-6、ハット -10〜-14」(出44, `mixing-guide.md`)なので hihat は kick の約1/3。

#### M34 ドラムンベース（174）
- 向く曲: 高速の追跡、緊迫したダンジョン。
- パート: sub808 .10; bass .06 b+.1; kick .09; snare .08; hihat .03 p.3; pad .05 d.25 r.4; lead .07 r.25
- drumMix: kick L1.0; snare L1.1 r.12; hat L.65 p.3
- 書き出し: `--master -9 --widen 1.4`
- 帯域: sub〜低 -2／中低 -8／中 -10。
- 注意: サブは 80Hz 以下・モノ・キックに合わせて凹ませる(出27)。BPM 174 の `duck` 0.45拍≒155ms。ミッドベース(bass)で幅を作り、sub は中央。

#### M35 ダブステップ/ベースミュージック（ハーフタイム）
- 向く曲: 重いボス戦、機械の敵。
- パート: sub808 .11; bass .08 b+.2 d.2; bass .04 p-.6 c.3; kick .09; snare .09 r.25; hihat .02; lead .06 r.3
- drumMix: snare L1.15 r.25; kick L1.1; hat L.5
- 書き出し: `--master -9 --widen 1.4`
- 帯域: 低 -2／中低 -7／中 -10。
- 注意: 幅は中域（500Hz 以上）のベースだけに持たせ、sub808 は `p0`(出28,27)。スネアは3拍目。

#### M36 シンセウェーブ
- 向く曲: 夜のネオン街、レトロ未来のステージ。`synth:true`。
- パート: kick .08; snare .08 r.35; tom .06 sp.8 r.3; bass .09 b+.2; pad .07 p-.5 c.4 r.45; lead .09 c.2 r.3; keys .06 p.6 r.25 c.2
- drumMix: kick L1.0; snare L1.1 r.35; tom sp.8 r.3
- 書き出し: `--master -10 --widen 1.6 --space plate --space-wet 0.18`
- 帯域: 低 -3.5／中低 -6.5／中 -9。
- 注意: 80年代のドラムのゲートリバーブは、プリディレイ0・短く切る(出20)。うちは snare の `reverb` で近似し、尾の長さは変えられない（提案5）。

#### M37 ローファイ（チル）
- 向く曲: 休憩所、宿屋、夜の静かな場面。
- パート: piano .13 p-.3 b-.45 r.3 c.25; bass .09 b-.35 d.25; kick .08 b-.3; snare .05 b-.4 r.15; hihat .018 b-.4 p.35; guitar .07 b-.3 p.4 r.2
- drumMix: kick L.9; snare L.8 r.15; hat L.5 p.35 r.05
- 書き出し: `--master -14 --space room --space-wet 0.22`（widen なし）。
- 帯域: 低 -3.5／中低 -5／中 -13／張り -30。
- 注意: 記事の「LPFで高域を落とし、サチュレーションと揺れ」(出16,40,41)を、`bright` -.3〜-.45 と `chorus`（揺れ）で近似。サチュレーションは無い。キックでベースを凹ませる(出16,40)。

#### M38 アンビエント
- 向く曲: 森、洞窟の入口、神秘的な場面、メニュー画面。
- パート: pad .10 p-.4 c.35 r.55 b-.2; pad .08 p.4 c.3 r.55; strings .06 r.5; bell .04 p.5 r.6; leadGuitar .05 r.5; bass .06 b-.2
- drumMix: —（ドラムなし）
- 書き出し: `natural` ＋ `--master -18 --widen 1.8 --space hall --space-wet 0.3`
- 帯域: 低 -5／中低 -4.5／中 -10／張り -22。
- 注意: パッドは低域を空け（C3 以上）、動きは音のオン・オフで作る(出17,36)。2つのパッドを左右反対に(出35)。静かな曲ほど `--master` を下げ、起伏を残す。

#### M39 オーケストラ/映画音楽
- 向く曲: 王城、戦争の序章、感動の場面。
- パート: strings .08 p-.4 r.25; strings .08 p.4 r.25; bass .07 p0 b-.2 r.2; brass .09 p.2 r.4 b-.1; choir .07 r.4; harp .05 p.5 r.35; tom .05 r.5 b-.1 L.9; kick .05 r.45
- drumMix: kick L.8 r.45; tom sp.7 r.4; crash L.7 r.4
- 書き出し: `natural` ＋ `--master -16 --widen 1.3 --space hall --space-wet 0.22`
- 帯域: 低 -5／中低 -4.5／中 -9／張り -20。
- 注意: 配置は、第1バイオリン左・チェロ右・コントラバス中央(出37)。奥行きは弦=手前（`r.25`）、管=その後ろ（`r.4`）、打楽器=最後方（`r.5`）(出18,37)。バランスは「弦→木管→金管→打楽器」(出18)。バス圧縮は 2:1・1〜2dB 以内(出18)。

#### M40 シューゲイザー
- 向く曲: 夢の中、記憶の場面、幻想の戦闘。
- パート: distGuitar .09 p-.7 c.35 r.5; distGuitar .09 p.7 c.35 r.5; guitar .08 p-.3 r.5; guitar .06 p.3 r.5; bass .10 d.1; kick .08; snare .065 r.4; hihat .02 b-.3; leadGuitar .07 r.5 b-.2
- drumMix: snare L1.0 r.4; hat L.5 p.3 r.2; crash L.8 p-.3 r.4
- 書き出し: `--master -12 --widen 1.6 --space hall --space-wet 0.25`
- 帯域: 低 -4.5／中低 -5／中 -9。
- 注意: 記事はリバーブとディレイでミックスを飽和させ、ギターの層を色の違いで分ける(出29,30)。濁りの管理が難しい(出30)ので、ベースとキックは中央・残響0〜.05、ギターの音域は E2 以上。

#### M41 アコースティック弾き語り風
- 向く曲: 宿屋、回想、焚き火の場面。
- パート: lead .12 r.2; guitar .20 p-.25 r.15; echoGuitar .08 p.3 r.2; strings .04 r.4; bass .04
- drumMix: —
- 書き出し: `natural` ＋ `--master -15 --space room --space-wet 0.12`
- 帯域: 低 -4／中低 -5／中 -9。
- 注意: 歌（lead）の席（2〜4kHz）をギターと分ける。ギターは右手のかき鳴らしで 100Hz 以下を持つ→ 低域は薄く（ベースは極小）。

#### M42 ミニマル（反復）
- 向く曲: 緊張が続く探索、時間が止まる場面。
- パート: bell .09 p.3 r.2; bell .07 p-.3 r.25; bass .08 d.2; kick .08; hihat .025 p.4; pad .04 r.4
- drumMix: kick L.9; hat L.6 p.4
- 書き出し: `natural` ＋ `--master -13 --widen 1.3`
- 帯域: 低 -3／中低 -6／中 -10。
- 注意: 少ないパートで、**1つのパートを 1〜2dB ずつ動かす**だけで進行する。パートを増やさない。

#### M43 ピアノソロ
- 向く曲: 回想、静かな日常。
- パート: piano .30 p0 r.2; piano .05 p.5 r.45 b-.3（1オクターブ上の薄い複製）
- 書き出し: `natural` ＋ `--master -17 --widen 1.3 --space hall --space-wet 0.18`
- 帯域: 低 -4／中低 -4.5／中 -10。
- 注意: 1パートだけの曲は `volume` の合計が小さくなるので、1パートを .3 まで上げてよい。

### 3.3 ゲーム音楽のパターン（C群）

#### M44 フィールド（探索）
- パート: leadGuitar .11 r.25; guitar .14 p-.4 r.2; strings .07 p.3 r.4; bass .07 d.15; kick .05; snare .04 r.15; hihat .018; bell .04 p.5 r.4
- drumMix: kick L.8; snare L.8 r.15; hat L.55 p.3
- 書き出し: `natural` ＋ `--master -13 --widen 1.4 --space hall --space-wet 0.12`
- 帯域: 低 -4／中低 -5.5／中 -9。
- 注意: 長く聞く曲なので耳が疲れない: 張り(4k〜)を控えめ。ループの継ぎ目の尾(出: `mixing-guide.md` §4)。

#### M45 戦闘
- パート: kick .09; snare .075 r.12; hihat .035; crash .035; tom .055; bass .09 b+.3 d.3; distGuitar .11 p-.75 b-.1; distGuitar .11 p.75 b-.1; leadGuitar .10 r.15; strings .06 r.25
- drumMix: kick L1.1; snare L1.1 r.12; hat L.7 p-.3; crash L.85 p.3 r.2; tom sp.6
- 書き出し: `--master -10 --widen 1.3 --space room --space-wet 0.1`
- 帯域: 低 -4／中低 -6／中 -8／張り -16。
- 注意: 効果音（斬撃・魔法）が 1〜4kHz を使う。ギターを `b-.1`、合計を控えめに。ゲーム側で場面のダッキングを足す案（提案8）。

#### M46 ボス戦
- パート: kick .10 b+.2; snare .075 r.15; tom .07 sp.6 r.2; crash .035; bass .10 b+.3 d.3; distGuitar .11 p-.8; distGuitar .11 p.8; brass .09 p.2 r.25; choir .06 r.4; strings .06 r.3
- drumMix: kick L1.15; snare L1.1 r.15; tom sp.6 r.2; crash L.85 p.3 r.25
- 書き出し: `--master -9.5 --widen 1.4 --space hall --space-wet 0.1`
- 帯域: 低 -3.5／中低 -6.5／中 -8.5／張り -16。
- 注意: 層は多いが、合計は 0.9 内に。合唱と金管は同じ席（500〜2kHz）なので、片方を休符で抜く。戦闘より一段厚い（+1段）。

#### M47 町
- パート: guitar .18 p-.35 r.15; lead .10 r.25; harp .07 p.4 r.3; strings .04 r.4; bass .06 d.1; kick .03; hihat .012 p.3
- drumMix: kick L.6; hat L.4 p.3
- 書き出し: `natural` ＋ `--master -15 --widen 1.2 --space room --space-wet 0.15`
- 帯域: 低 -4／中低 -5.5／中 -9／張り -20。
- 注意: 人の声（会話や市場の効果音）が重なるので、1〜4kHz を控えめに、低い楽器は少なく。

#### M48 ダンジョン
- パート: pad .09 p-.3 b-.35 r.5 c.1; strings .07 p.3 b-.3 r.5; bass .08 b-.2; bell .035 p.6 r.6; tom .05 r.5 b-.2; wind .03 r.4
- drumMix: tom sp.6 r.5; kick L.6 r.5
- 書き出し: `natural` ＋ `--master -16 --widen 1.4 --space hall --space-wet 0.3`
- 帯域: 低 -4／中低 -4.5／中 -11／張り -24。
- 注意: 足音・水滴などの効果音が聞こえるよう、2〜4kHz を空ける。ベルは疎らに。

#### M49 タイトル画面
- パート: strings .10 p-.3 r.35; strings .06 p.3 r.35; brass .08 r.3; piano .09 p-.2 r.25; leadGuitar .10 r.3; harp .05 p.5 r.35; tom .06 r.35; choir .05 r.4
- drumMix: tom sp.7 r.35; kick L.7 r.4
- 書き出し: `natural` ＋ `--master -13 --widen 1.5 --space hall --space-wet 0.2`
- 帯域: 低 -4.5／中低 -5／中 -9。
- 注意: ループしない場合は終わりに自然な尾を残す。ゲームの顔なので幅（widen）を広めに。

#### M50 和風・民族
- パート: koto .12 p-.4 r.3; shamisen .09 p.4 b+.1 r.2; shakuhachi .10 r.35 b-.1; tom .07 sp.6 r.3 L.9; kick .05 r.3; bass .05 b-.2; chime .035 p.6 r.5
- drumMix: tom L.9 sp.6 r.3 t-3; kick L.7 r.3
- 書き出し: `natural` ＋ `--master -15 --widen 1.2 --space room --space-wet 0.18`
- 帯域: 低 -5／中低 -5／中 -9／張り -19。
- 注意: 撥弦は頭が鋭く、尾が短いので、残響で余韻を補う。尺八は中央で息の成分（4kHz 付近）を残す。太鼓は低めに（`tune` -3）。

#### M51 チップチューン/レトロ風
- 向く曲: レトロな場面、ミニゲーム。
- パート: lead .10 b0; lead .08 p.4; bass .09; kick .07; snare .05; hihat .02
- drumMix: —（残響 0）。
- 書き出し: `--master -11`（`--space` なし、widen 1.0）。
- 帯域: 低 -4／中低 -6／中 -8。
- 注意: 乾きが音色。残響を付けない。`CLAUDE.md` に、レトロな音は「場面に合うときに選ぶ曲調の一つ」とある。

#### M52 効果音と共存（汎用の席空け）
- 向く曲: 戦闘・町・ダンジョンなど効果音が多い場面すべて。
- パート: 1〜4kHz を担うパート（lead・distGuitar・crunch・bell）に `volume` ×.8、伴奏に `b-.15〜-.25`。ベース・パッド・弦は変えない。
- 書き出し: `--master -14`（ゲームでは曲どうしの音量差を `bgm-trim` で補正）。
- 帯域: 中が目標より -2dB 低く。
- 注意: 出典では、固定のカットなら Q 0.7〜1 で -2〜-3dB(出 `mixing-guide.md` §2)。場面で一時的に下げる設計も（提案8）。「音楽は数dB下げて、前後0.5秒ほどのフェードで戻す」(出42)、ナレーション中は一律 -9dB・降下0.5秒・復帰1秒の例(出19)。

#### M53 ループ BGM（継ぎ目）
- パート: 終わりの小節に、パッド・弦のロングトーンを置き、先頭にも同じ音の頭を入れる。
- 書き出し: `--space room --space-wet 0.1`（残響が短い方が継ぎ目が目立たない）。hall は避ける。
- 注意: 残響の尾を先頭に重ねる工夫は書き出しの後処理が要る（提案9）。

#### M54 ビルド → ドロップ（セクションの型）
- 向く曲: EDM、ボス戦の第2形態。
- 手順: ブレイク=kick・bass を休符、パッドとリードのみ、`r` 多め／ビルド=スネアのロール、リードを上げ、パート数 4→6／ドロップ直前の1拍=全休符／ドロップ=全パート復帰、ドライ寄り。
- 数字: ブレイクの `volume` 合計は本編の約60%（出: ブレイクとビルドを小さくするとドロップが大きく聞こえる、`mixing-guide.md` §5）。
- 注意: 書き出しの `--widen` は曲全体なので、幅の変化は**パートの出入り**で作る（M55）。

#### M55 サビだけ広げる（幅の変化）
- 手順: ヴァース=広がりのパートは1つだけ（`p±.4`）。サビ=ダブルのギターを追加（`p±.85`）、`chorus` .3 のパッド、ストリングスを追加。
- 書き出し: `--widen 1.4`（固定）。
- 注意: 記事では幅を自動で変える(出12)が、うちはパートの出入りで代用。

#### M56 ドラム単体のバランス（ロック標準）
- drumMix: kick L1.0; snare L1.05 r.15; hat L.65 p-.3 r.08; tom L.9 sp.6 r.12; crash L.85 p.3 r.2
- パート: ドラムの `volume` はキックを基準に、スネア ×.72、ハット ×.33、クラッシュ ×.36、タム ×.55。
- 書き出し: —
- 帯域: キック 60〜100Hz、スネア 150〜250Hz と 2〜5kHz、ハット 6kHz〜。
- 注意: タムは高→低を左→右へ（`sp`）、ハットは30%左(出5,46)。シンバルがうるさい時は `crash L` を下げ、`r` を足す。

## 4. 症状別の直し方

| # | 症状 | 帯域・原因 | 直し方（うちの手段） |
|---|---|---|---|
| 1 | こもる | 200〜500Hz。持続音（弦・パッド・ピアノ・歪みギター）が重なる。残響が濃い(出31,32) | 体の楽器を1つに決め、他を C4 以上へ。脇役 `volume` ×.8。`--space-wet` を -.05。主役の `bright` を 0 に。 |
| 2 | きんきん・刺さる | 2〜5kHz（広くは2.5〜8k）。リード・歪みギター・ベルが同帯域(出45) | 脇役 `b-.2〜-.3`、歪みギター ×.85、ベル `r` を上げ `volume` を下げる。ハットは `drumMix.hat.L` を -.1。 |
| 3 | スカスカ | 80〜250Hz、または音数不足。モノで位相が打ち消される場合も(出7) | bass +10%。ピアノの左手・低いパッドを足す。ベースを1オクターブ重ねる。相関 <0.3 なら `--widen`/`chorus` を下げる。 |
| 4 | もたつく | キック・ベースの長さ、ドラムの残響の尾 | bass の `sustain` .6〜.8、`d.25`。ドラムの `r` を -.1。リリースの目安は1拍=60000÷BPM の50〜90%(出 `mixing-guide.md`)。 |
| 5 | うるさい（疲れる） | 全体の大きさ、2〜5kHz、PLR低 | `--master` を -2。`natural` に。全体の `bright` -.1。ハット・クラッシュ -10%。 |
| 6 | ステレオが狭い | 全部が中央、側成分が無い | 脇役を `p±.4〜.8`、`c.2〜.3`、`--widen 1.4〜1.8`。相関 0.4〜0.88 に(出7,12)。 |
| 7 | 主役が埋もれる | 1〜4kHz、同じ席の脇役が大きい | 主役 +10〜20%。脇役 `b-.2` ×.8。左右に逃がす。主役の `reverb` -.1。階層(§5)。 |
| 8 | 低音が濁る | 60〜250Hz、特に200〜350Hz。キック・ベース・ギターの重なり(出31,33) | bass ×.85〜.9。`d.25〜.35`。sustain を短く。ベースを `p0`。低音パートを3つまでに。 |
| 9 | シンバルがうるさい | 6〜10kHz、「アイスピック」は8〜10k(出52)。 | `crash L` を .85→.7、`hat L` を .6。`reverb` で丸める。パンを外へ（p±.3）。 |
| 10 | リードが前に出ない | 1〜4kHz、残響が多い、同帯域の伴奏 | リード `r.1〜.2`、`volume` +15%、伴奏 ×.85。サイドチェイン代用でパッド `d.25`。 |
| 11 | 音が割れる | 全体。合計 >0.9、amp が深い | 合計 0.75。amp の drive を下げる。crest 10dB 以上(う)。 |
| 12 | 平坦で迫力がない | LRA <4、全部同じ大きさ | `natural`。セクションごとにパート数を変える（ヴァース3〜4、サビ5〜7）。 |
| 13 | ペラペラ・小さく聞こえる | 全体のPSR低。圧縮のしすぎ(`mixing-guide.md` §6) | `--master` を -2。非natural → natural。低域の薄いパートを足す。 |
| 14 | ブーミー（低音出すぎ） | 60〜120Hz。参考の 低 -3.3 より +2 以上 | bass ×.85（実験で最も効いた(う)）。kick の `b` を上げて高域のアタック側へ。 |
| 15 | 小さいスピーカーで低音が消える | 40〜120Hz の基音だけ | bass に 1オクターブ上の層を足す。`b+.3`。sub808 の上の倍音。 |
| 16 | 鼻づまり | 1〜3kHz のリード楽器が集中(出21) | 該当パートの音域を上げる。`b-.15`。ハーモニーのパートを減らす。 |
| 17 | 耳が疲れる | 3〜8kHz。合計が大きい、シンバルが多い | 全体 `b-.1`。ハット・クラッシュ -10%。休憩して耳をリセット(出46)。 |
| 18 | 残響で濁る | 200〜500Hz。hall が速い曲に、bass・kick へ | 曲が速ければ room か plate に。bass・kick は `r0`。パート `r` ≤ .2。 |
| 19 | 奥行きがない（ペタッ） | 全パートが同じ乾き具合 | 3層(M07)。奥のパートに `r.5` と `b-.3`。 |
| 20 | 中央に穴が空く | 全員を端に振りすぎ | lead・bass・kick・snare を `p0`。`--widen` を下げる(出5)。 |
| 21 | モノにすると薄くなる | 位相の打ち消し。chorus・ダブル＋widen | 相関 <0.3 なら `--widen` と `chorus` を下げる。重ね `push` を .02→0。 |
| 22 | ドラムがバラバラ | tom・hat・crash の位置が不統一 | `drumMix` の `pan` を一方向にそろえる（hat 左・crash 右・tom 高左→低右）。 |
| 23 | キックが埋もれる | 60〜100Hz と 2〜4kHz。bass が大きい | kick `L` +.1、`b` +。bass `d` +.05、bass ×.9。 |
| 24 | スネアが埋もれる | 150〜250Hz と 2〜5kHz。ギターと同帯域 | snare `L` 1.15、`r.15`。ギター ×.9。 |
| 25 | ハットがガチャガチャ | 6〜10kHz。hat が大きい | hat `L` .5〜.6、`p±.3`、`r.05`(出46)。 |
| 26 | ポンピングが目立つ | `duck` が深すぎ、BPMと不一致 | `d` を .15〜.25。BPM で 0.45拍の長さを確認。 |
| 27 | 曲の頭と終わりで大きさが違う | 書き出しの大きさ、尾 | `trimDb` で補正。`--space-wet` を下げる。 |
| 28 | 効果音に埋もれる | 1〜4kHz の衝突 | M52。BGM を 2〜3dB 下げ、場面で一時的に下げる。 |
| 29 | パンチがない | キックの頭（2〜4kHz）、アタックの丸さ | kick `b+.2`、snare `L` +.1。natural でなく 4:1(M02)。 |
| 30 | ギターが痩せる | 1〜4kHz が少ない(`punk-guide.md` §7, §9) | ギター `volume` を上げる前にベースを下げる。amp を punk/crunch に。 |
| 31 | 歌（リード）が前に出すぎ・浮く | 残響が少なすぎ、明るすぎ | `r.15〜.22`、`b-.1`、伴奏を +5%。 |
| 32 | 奥のパートが聞こえない | 残響多すぎ + volume小さすぎ | `volume` +20%、`r` -.1、`b` 0 に。 |

## 5. パートの音量比の早見表

`volume` の比。**リード（主役）=1**（各パターンの値から逆算。ハウスはリード、ファンクはベース、ジャズトリオはピアノ、オーケストラは金管を1にした）。`clear-guitar-rock` の基準目盛り（std ドラム音源）。ドラム音源が rock（`punk-run`）なら、ドラム列に ×0.35〜0.5。合計は 0.9 以下に収める。

| 編成 | kick | snare | hihat | crash | tom | bass | リズムGt(1本) | 鍵盤/ピアノ | 弦/パッド | ベル/空気 | リード |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ロック4人（M17） | 0.9 | 0.65 | 0.3 | 0.32 | 0.5 | 0.9 | 1.3 | — | — | — | 1 |
| ロック5人（M18） | 0.85 | 0.6 | 0.28 | 0.3 | 0.45 | 0.85 | 1.1 | 0.7 | — | — | 1 |
| ポップ（M23） | 0.67 | 0.5 | 0.23 | 0.25 | — | 0.71 | 1.17 | 0.83 | 0.42 | 0.33 | 1 |
| J-POP（M24） | 0.67 | 0.5 | 0.23 | 0.25 | 0.33 | 0.71 | 1.0 | 0.58 | 0.42 | 0.33 | 1 |
| メタル（M21） | 1.0 | 0.6 | 0.26 | 0.3 | 0.5 | 0.85 | 1.2 | — | — | — | 1 |
| バラード（M26） | 0.55 | 0.33 | 0.13 | — | — | 0.67 | — | 1.78 | 0.89 | — | 1 |
| ジャズトリオ（M27） | 0.31 | 0.25 | 0.16 | 0.12 | — | 0.81 | — | 1.0 | — | — | (ピアノ=1) |
| ファンク（M29） | 0.65 | 0.54 | 0.27 | — | — | 1.0 | 0.92 | 0.69（keys） | 0.69（brass） | — | (ベース=1) |
| ハウス（M33） | 1.43 | 0.86 | 0.4 | 0.29 | — | 1.14 | — | 1.0（keys） | 0.71（pad） | — | 1（lead .07 = 1） |
| ゲーム戦闘（M45） | 0.9 | 0.75 | 0.35 | 0.35 | 0.55 | 0.9 | 1.1 | — | 0.6 | — | 1 |
| ゲーム町（M47） | 0.3 | — | 0.12 | — | — | 0.6 | 1.8（nylon） | — | 0.4（弦）／0.7（harp） | — | 1 |
| ゲームフィールド（M44） | 0.45 | 0.36 | 0.16 | — | — | 0.64 | 1.27 | — | 0.64 | 0.36 | 1 |
| オーケストラ（M39） | 0.56 | — | — | — | 0.56 | 0.78 | — | — | 0.89（弦2本） | 0.56（harp） | 1（brass .09=1） |

読み方の目安（dB）: 比 0.9 =-1dB／0.7 =-3dB／0.5 =-6dB／0.35 =-9dB／0.25 =-12dB／0.2 =-14dB／0.125 =-18dB。EDM は「キック 0dB・クラップ -3〜-6・ハット -10〜-14・リード=キックのすぐ下・パッド -6〜-9」(出44, `mixing-guide.md` §5)。

## 6. ミックスのチェックリスト

1. パートの `volume` の合計は 0.9 以下か（0.7〜0.8 が安全）。主役が最大か。
2. 同じ席に主役級が2つ以上いないか（周波数・左右・時間）。
3. kick・bass・sub808・lead・snare は `pan` 0か。
4. 低域を担うパートは3つ以内か。ベースは短く、`duck` .15〜.35 か。
5. 200〜500Hz で持続音が重なっていないか（体の楽器は1つ）。
6. 奥行き: 主役が乾き、背景が湿っているか。kick・bass の `reverb` は 0〜.05 か。
7. `--space` は曲のテンポに合っているか（速いなら room/plate）。wet は帯域診断で低が +1.5dB 以上増えていないか。
8. `analyze.py --bands` で 帯域が §3.0 の家族の値から ±2dB か。参考37曲の範囲内か。
9. 相関 0.4〜0.88、LRA 4 以上、crest 10dB 以上、PLR 9 以上。
10. モノで聞いて、低音が消えない・リードが消えないか。
11. ヘッドホン・スピーカー・スマホの3つで聞いたか。
12. ゲーム内で効果音と一緒に聞いたか（1〜4kHz の衝突）。
13. 音量を ±0.5LUFS で揃えて、参照曲（2〜3曲）と A/B したか。
14. 曲頭・曲末の大きさ、ループの継ぎ目に不自然さがないか。
15. 1回の調整で動かしたのは1か所か（やりすぎ防止）。

## 7. 取り入れる提案（実装できる単位）

1. **ミックスのパターンをサウンドセットに追加**。本書の M17〜M50 から代表12種（rock-4, pop-lead, jpop-bright, ballad-piano-strings, jazz-trio, funk-bass, house-duck, ambient-wide, orchestra-depth, game-battle, game-town, game-dungeon）を `SOUND_SETS` に足す。`parts` と `drumMix` は本書の数字、`master` は `{lufs, widen}`。名前は音の特徴にする（バンド名にしない）。
2. **`SoundSet.master` に `space` と `spaceWet` を足す**（今は `lufs` と `widen`）。`song-lib.mjs` の `build` が `set.master.space` を読んで `--space` を自動にする（`master`/`widen` と同じ仕組み）。引数は後勝ち。
3. **帯域診断の目標を家族別 JSON に**。`docs/sound/data/mix-targets.json` に §3.0 の家族ごとの `{bass,lowmid,mid,presence,tilt}` を置き、`analyze.py --bands --family rock` で、参考37曲ではなく家族の目標との差を表示する。
4. **1/3オクターブ目標曲線の自動生成**。`third-octave.py --tilt -1.5` で、傾き s から目標 JSON を作って比べる（§3.0 の式）。家族名でも指定できるように。
5. **役割から初期値を出す「ミックス下書き」**。`suggestMix(score, patternId)` が、トラックの `instrument` から `volume`・`pan`・`reverb`・`bright`・`duck` を出す（`applySoundSet` の親戚）。手で変えた値は上書きしない。役割は §3.1 M09 と §5 の比を使う。
6. **ミックスの検査を `score-check.mjs` に追加**。合計 `volume` が 0.9 超、主役（最大の volume）が 2 つ以上同じ値、低域のパート（bass・sub808・kick）が `pan` 非0、kick・bass の `reverb` > .1、同じ側に3パート以上、などを警告する。
7. **`--widen` を高域だけに効かせる**。`song-lib.mjs` で 150Hz で2つに分け（`lowpass`/`highpass`）、高域側だけ extrastereo をかけて足し戻す。低域のモノが保証でき、`widen` を 2 まで安全に上げられる。
8. **ゲームの BGM バスに「効果音ダッキング」**。`createBgmBus` に、イベント（会話・大技・宝箱）で BGM を -3〜-9dB にし、0.5秒で下げ、1秒で戻す API。BGM 側の 1〜4kHz だけ下げる版（バンドパス）は第2段。
9. **ループ用の尾の重ね書き出し**。`--loop-tail` で、書き出しの WAV の末尾の残響を先頭に足す（テールラップ）。`--space` の尾（rt60 の1.15倍）が収まる長さに。
10. **参照曲の A/B 自動レポート**。`analyze.py --compare 参照1 参照2 参照3` が、LUFS を揃えてから、帯域・LRA・相関・左右の広がりの差を1枚の表にする（サビ同士を自動で選ぶ）。
11. **ゴースト層の自動生成**。M03 の「複製パート」をボタン1つで作る（スネアまたはキックを複製、`volume` ×.25、`reverb` +.25、`bright` -.25）。聞いて決めるための試作として。
12. **場面のプリセット（ゲームの場面 → 型）**。作曲ソフトで場面（フィールド・戦闘・ボス・町・ダンジョン・タイトル）を選ぶと、M44〜M49 のパートの初期値と書き出しの引数が入る。

## 8. 調べていないこと・限界

- 本文を読めたのは WebFetch の要約経由で、数値の出どころは各記事の要約。robots 制限などで読めなかったページ（例: violetrecording の一部、nailthemix の一部）は使っていない。
- **(推)** の付く数値（家族別の帯域目標、`--space-wet` の量、`widen` の上限、ゴースト層の比）は、うちの道具で**測って確かめていない**。採用する前に、`analyze.py --bands` と耳で確かめる。
- うちのエンジンに無いもの: パートごとのEQ・コンプ、サチュレーション、ダイナミックEQ、パラレル、プリディレイの変更。本書はそれらを音量・音域・`bright`・`duck`・`reverb` で近似した。
- 日本語ジャンル（J-POP/アニソン/ボカロ）の記事は、数値の載るものが見つからず、**(推)** が多い。

## 9. 参考URL（読めたもの。番号は本文の (出N) と対応）

1. https://www.musicguymixing.com/bus-compression/
2. https://www.musicguymixing.com/parallel-compression-settings/
3. https://www.musicguymixing.com/parallel-compression-on-drums/
4. https://www.soundbridge.io/reverb-and-delay-tips-for-cleaner-deeper-mixes
5. https://www.nailthemix.com/panning
6. https://emastered.com/blog/mixing-jazz
7. https://www.edmprod.com/mono-vs-stereo
8. https://output.com/blog/gain-staging-101-how-to-supercharge-your-mix
9. https://www.izotope.com/community/blog/9-tips-for-mixing-jazz
10. https://mastering.com/6-mix-bus-compression-mistakes-will-destroy-mixes/
11. https://loststoriesacademy.com/blogs-and-tutorials/how-to-create-depth-and-dimension-with-reverb-and-delay
12. https://audient.com/ko/tutorial/5-tips-for-taking-control-of-stereo-width/
13. https://www.soundonsound.com/techniques/mix-rescue-jazz-trio
14. https://www.nailthemix.com/what-is-mixing-in-music
15. https://edmprod.com/sidechain-compression
16. https://www.antarestech.com/blog/the-complete-guide-to-mixing-lo-fi-music
17. https://www.izotope.com/en/learn/5-tips-for-mixing-pads
18. https://beatkitchen.io/guides/orchestral/11-orchestral-mixing/
19. https://www.gamedeveloper.com/audio/game-audio-theory-ducking
20. https://musictech.com/tutorials/tips/how-to-create-authentic-vintage-drum-gated-reverb-for-synthwave-chillwave-music-styles
21. https://www.soundhouse.co.jp/contents//index?post=3112
22. https://www.tetsu7017.com/blog/dtm-mixing-guide-beginners/
23. https://emastered.com/blog/pop-mixing
24. https://www.riffhard.com/how-to-mix-punk-guitar/
25. https://www.audio-issues.com/music-mixing/eq-tips-for-punk-rock/
26. https://www.masteringthemix.com/blogs/learn/how-to-mix-808s-that-bang
27. https://www.beatportal.com/articles/818379-step-by-step-guide-to-producing-drum-and-bass-like-sub-focus-a-m-c-and-delta-heavy
28. https://musicradar.com/how-to/8-ways-to-improve-your-bass-mixing-skills
29. https://www.riffhard.com/how-to-get-a-shoegaze-guitar-tone/
30. https://homerecording.com/bbs/threads/thoughts-on-how-to-mix-and-record-shoegaze-style-music-my-bloody-valentine-etc.255956/
31. https://www.masteringthemix.com/blogs/learn/how-to-fix-muddiness-when-mastering-music
32. https://emastered.com/ja/blog/avoiding-muddy-sound
33. https://emastered.com/ja/blog/frequency-masking
34. https://www.sweetwater.com/insync/quickie-guide-mixing-part-4/
35. https://www.soundonsound.com/techniques/mix-rescue-ambient-dance-track
36. https://www.musicradar.com/tuition/tech/27-essential-ambient-production-tips-166772
37. https://www.loopmasters.com/articles/2361-Realistic-Orchestral-Panning-Instrument-Placement-In-The-Stereo-Field
38. https://www.songchecks.com/blog/how-mix-bass-and-kick-in-hip-hop
39. https://waves.com/mix-808-and-kick-like-a-pro
40. https://ujam.com/blog/top-5-production-mixing-tips-for-lofi
41. https://www.masteringthemix.com/blogs/learn/how-to-make-lo-fi-hip-hop
42. https://morphic.com/resources/how-to/how-to-mix-sound-effects-with-music
43. https://www.izotope.com/en/learn/9-tips-for-producing-and-mixing-house-music
44. https://www.loopcloud.com/articles/2718-Mixing-Electronic-Music-A-Few-Quick-And-Easy-Guidelines
45. https://www.musicguymixing.com/harsh-mix/
46. https://www.izotope.com/en/learn/how-to-mix-hi-hats
47. https://www.masteringthemix.com/pages/how-to-use-reference-tracks
48. https://www.waves.com/science-mix-referencing-5-step-method
49. https://www.izotope.com/en/learn/what-is-audio-saturation
50. https://rysupaudio.com/blogs/news/how-to-mix-rnb-vocals
51. https://producelikeapro.com/blog/three-steps-to-funky-bass/amp/
52. https://www.nailthemix.com/deesser
53. https://unison.audio/audio-ducking/
54. https://www.loststoriesacademy.com/blogs-and-tutorials/what-is-gain-staging-and-why-it-matters-in-mixing

うち側の根拠（本書で参照した既存のファイル・コード）: `src/audio/sound-sets.ts`（`PartMix`・`applySoundSet`・音量の目盛り）、`src/audio/score.ts`（`drumMix`）、`tools/composer/song-lib.mjs`（`--master`/`--widen`/`--space`/`--space-wet` の仕組み）、`tools/composer/space-ir.mjs`（`SPACES`: room/hall/plate）、`tools/audio-check/analyze.py`・`third-octave.py`、`docs/sound/mixing-guide.md`・`punk-guide.md`・`layering-guide.md`・`sound-design-basics.md`・`sound-sets.md`。

## 10. 実装状況（2026-10-11）

§7 の提案 12 個のうち、書き出し・サウンドセット・診断に関わるものを実装した。コードは `src/audio/sound-sets.ts`・`src/audio/mix-tools.ts`、診断は `tools/audio-check/`、書き出しは `tools/composer/`。テスト: `npx vitest run src/audio/sound-sets src/audio/mix-tools`（26 件）と `node --test tools/composer/*.test.mjs`。

| # | 提案 | 状態 | 内容・測った数字 |
|---|---|---|---|
| 1 | ミックスの型をサウンドセットに | **入れた（13 個）** | 提案の 12 個（rock-4・pop-lead・jpop-bright・ballad-piano-strings・jazz-trio・funk-bass・house-duck・ambient-wide・orchestra-depth・game-battle・game-town・game-dungeon）＋ game-boss。数字は各 M の値。`punk-run`・`clear-guitar-rock` は変えていない（テストで固定）。**M の番号で入れたもの**: M17・M23・M24・M26・M27・M29・M33・M38・M39・M45・M46・M47・M48。ベース／キック／808 は中央のまま（M27 の「ベースをわずかに右」は、低域モノ化・診断と食い違うので中央にした） |
| 2 | `master` に space・spaceWet・preset | **入れた** | `SoundSet.master = {lufs, widen?, preset?, space?, spaceWet?}`。`build` が読み、`--master-preset`・`--space`・`--space-wet`・`--master`・`--widen` を書けばそちらが優先 |
| 3 | 帯域診断の家族別 JSON | **入れた** | `docs/sound/data/mix-targets.json`（§3.0 の 8 家族＋別名。数字だけ）。`analyze.py --bands 結果.json --family rock` |
| 4 | 1/3 オクターブ目標の自動生成 | **入れた** | `third-octave.py 曲.wav --tilt -1.5` または `--family rock`（1kHz 基準の傾き × log2(f/1kHz)）。`match-eq.py` も同じ式 |
| 5 | 役割から初期値（ミックス下書き） | 一部 | `ROLE_DEFAULTS`／`suggestPartDefaults(role, side)`（旋律 .1／低音 .09／和音 .06／飾り .035／空気 .02）。`suggestMix(score, patternId)` は作らず、型を当てるのは `applySoundSet`（セット）に任せた |
| 6 | ミックスの検査 | **入れた**（`score-check.mjs` には足さず build の警告へ） | `checkMixRoles(score)`: 合計 volume > 0.9／kick・bass・sub808 が中央でない／低音パートの reverb > .1／低域パートが 4 つ以上／違う楽器の主役が同じ音量／同じ側に 3 パート以上。`song.mjs build` の注意に出る。楽譜から音域・重心を出す `analyze.py --roles 曲.sunshine-song.json`（200〜500Hz に持続音が複数＝体の席の重なり、ベースの重心がキックに近い、1〜4kHz の席、低域の中央・残響） |
| 7 | `--widen` を高域だけに | **入れた** | 書き出しの M/S ワイド（サイド HPF）＋低域モノ化で実現（`mastering-guide.md` §11）。`widen` を 2 まで上げても低音のサイドは増えない |
| 8 | ゲームの BGM バスの効果音ダッキング | **入れなかった** | ゲーム内の再生（`createBgmBus`）側の作業で担当外。代わりに書き出し側の `applyGameDuck(score, db)`（1〜4kHz のパートを下げ、伴奏の bright を -0.1）を用意（sound-design-basics 提案 7） |
| 9 | ループ用の尾の重ね書き出し | **入れた** | `--loop-tail`、継ぎ目の検査つき |
| 10 | 参照曲の A/B 自動レポート | **入れなかった** | `analyze.py --compare` はある。LUFS をそろえてサビ同士を自動で選ぶ処理は、参照曲の置き方を決めてから |
| 11 | ゴースト層の自動生成 | **入れた（関数のみ）** | `addGhostLayer(score, instrument)`: volume ×.25・reverb +.25・bright -.25 の複製。作曲ソフトのボタンは未 |
| 12 | 場面のプリセット | **入れた（表のみ）** | `SCENE_SETS`（field・town・battle・boss・dungeon・title → セットと書き出しプリセット）。画面の選択欄は未 |

追加: サイドチェイン風 duck の推奨値 `recommendDuck(role, genre, bpm)`（役割別の基本値 × ジャンルの掛け率、EDM 以外は .4 まで、戻りは約 0.45 拍 `duckRecoverMs(bpm)`、速い／遅いテンポの注意つき）、BPM 同期のディレイ秒数 `syncDelaySeconds(bpm)`（`song.mjs delays 128` で表示）。

### 書き出して測った数字（見本曲に型と仕上げを当てた）
| 曲 | 当てたもの | I | TP | LRA | PLR | PSR | 相関 | crest | width |
|---|---|---|---|---|---|---|---|---|---|
| loud-rock-demo | `--master-preset game-battle --space room --space-wet 0.1 --loop-tail` | -14.7 | -1.5 | 7.8 | 13.2 | 10.4 | 0.95 | 15.4 | 0.15 |
| delicate-demo | `--sound ballad-piano-strings`（preset solo・hall .2・-15） | -15.0 | -2.3 | 2.3 | 12.7 | 11.5 | 0.37 | 14.5 | 0.68 |
| delicate-demo | `--sound jazz-trio`（preset jazz・room .15・-16） | -16.0 | -1.7 | 2.1 | 14.3 | 13.3 | 0.49 | 15.2 | 0.59 |
| hiphop-demo | `--master-preset hiphop --match-eq hiphop --lowmono 120 --tp -1.2 --clip 1` | -10.1 | -1.2 | 1.8 | 8.9 | 7.9 | 0.92 | 12.0 | 0.21 |

（見本曲は音の良し悪しを聴いて作ったものではないので、数字は「新しい仕上げが目標の大きさと天井に収まり、つぶしすぎない」ことの確認。曲の頭と終わりが違う見本曲では、継ぎ目の検査が「要直し」になる＝検査が働いている。）

### 入れなかった M のパターン
M01・M02・M04〜M16 は「型」というより手順・書き出しの引数の組み合わせなので、セットの `master`（M04〜M06 の space と wet、M10・M11 の widen）と、検査（M09・M13・M14）、関数（M03 ゴースト層、M08 の duck、M52 の席空け）に分けて入れた。M18〜M22・M25・M28・M30〜M32・M34〜M37・M40〜M43・M49〜M51・M54〜M56 は、**同じ書式で足せる**がセットとしては入れていない（数が多く、聴いて選ぶ段階に入っていないため）。M53 は `--loop-tail`、M56 のドラムのバランスは各セットの `drumMix` に入っている。
