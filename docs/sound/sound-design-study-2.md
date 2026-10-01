# 音作りの勉強 その2（2026-10-02）

前回（`guitar-bass-drums-sound-design.md`）の続き。ミキシング解説サイトの一般的な目安をまとめたもの。数値は目安で、最後は耳で決める。特定の曲・機材の音を写したものではない（CLAUDE.md 1-1）。

## 出典
- アンプの歪み: [All the World's a Gain Stage（Premier Guitar）](https://www.premierguitar.com/diy/amp-diy/what-is-gain-on-an-amp) / [Basic Low-Gain and High-Gain Preamp Circuits（Reverb）](https://reverb.com/news/daves-corner-amp-topologies-101-basic-low-gain-and-high-gain-preamp-circuits-explained) / [Tube Screamer Before a High-Gain Amp（Fader & Knob）](https://faderandknob.com/blog/tube-screamer-before-high-gain-amp) / [Impulse Response Explained（MusicStreet）](https://www.musicstreet.co.uk/blogs/blog-post/impulse-response-for-guitarists)
- サイドチェイン: [Sidechain Compression（EDMProd）](https://www.edmprod.com/sidechain-compression/) / [Sidechain Compression（mastering.com）](https://mastering.com/sidechain-compression-guide/) / [Sonarworks](https://www.sonarworks.com/blog/learn/sidechain-compression)
- 残響・ディレイ: [Reverb pre-delay explained（iZotope）](https://www.izotope.com/en/learn/reverb-pre-delay) / [Reverb Send Calculator（CMUSE）](https://www.cmuse.org/reverb-send-calculator) / [How to use a ping-pong delay（startcue）](https://www.startcue.io/learn/delay/ping-pong) / [Delay Types（Unison）](https://unison.audio/delay-types/)
- 周波数のすみ分け・ステレオ: [What is Frequency Masking?（MasteringBox）](https://www.masteringbox.com/learn/frequency-masking) / [Mono vs. Stereo（iZotope）](https://www.izotope.com/community/blog/mono-vs-stereo) / [Mixing in Mono（Composer Deck）](https://composerdeck.com/mixing-in-mono.html)
- ドラムの合成: [Sample-Free Drum Synthesis in Web Audio（DEV）](https://dev.to/sendotltd/sample-free-drum-synthesis-in-web-audio-building-kick-snare-and-hi-hat-from-oscillators-in-60-2c0k) / [808-Style Booms（Attack Magazine）](https://www.attackmagazine.com/technique/synth-secrets/808-style-booms/)
- シンセ: [How to design a supersaw lead（startcue）](https://www.startcue.io/learn/synth-design/supersaw) / [SUPERSAW Synth Tips（Sample Focus）](https://samplefocus.com/blog/supersaw-ableton-live/)
- 音量: [How Loud Should You Master?（Mastering The Mix）](https://www.masteringthemix.com/pages/how-loud-should-you-master) / [LUFS for Metal Mixes（Nail The Mix）](https://www.nailthemix.com/lufs) / [Genre-by-Genre Loudness（Luvlang）](https://luvlang.studio/blog/how-loud-should-my-master-be)
- 民族楽器: [Shakuhachi（Wikipedia）](https://en.wikipedia.org/wiki/Shakuhachi) / [Karplus–Strong string synthesis（Wikipedia）](https://en.wikipedia.org/wiki/Karplus%E2%80%93Strong_string_synthesis)

## 1. 歪みの作り方（アンプの中身）
- ハイゲインのアンプは、**ゲインの段を何段もつないで**（カスケード）、最後に音量を戻す。1段で深くかけるより、段を分けたほうが粒が残り、伸びもよい。
- 歪みの**前**に低音を削り、中域（700〜800Hz 付近）を持ち上げる（ブースターの定石）。低音が歪みに入ると濁るので、先に削って「締める」。
- 最後のキャビネットは「大きなフィルター兼コンプ」。高域を丸め（5〜6kHz 以上）、低域を落とす。ここで刺さりが決まる。
- → 反映済み: `loudmetal`・`metal`（前段ハイパス＋中域ブースト → 2段歪み → 後段で削る → キャビネットのローパス）。

## 2. サイドチェイン（ダンス・ハウスのポンプ感）
- キックが鳴るたびに、ベース・パッド・和音の音量を凹ませ、すぐ戻す。キックが抜け、低音が濁らず、ノリが出る。
- 目安: アタック 0〜10ms（ほぼ即座に凹む）、リリースは 1拍（クォーターノート）に合わせると目立つ（約 100〜200ms なら控えめ）、凹みは 6〜10dB。
- → 反映済み: 曲の `pump: true`。1拍ごとに音量が凹んで戻る（パッド・和音・ベース・リード・鐘・弦に。キックとドラムは凹まない）。

## 3. 残響とディレイ
- 残響は楽器で変える: ボーカルはプレート系 30〜50ms の前の間・1.4〜2.4秒、スネアは 8〜28ms・0.7〜1.6秒、ギターは 15〜40ms・1.0〜2.2秒。発音のはっきりさを守るには、前の間を長めに。
- **残響の戻りは必ず整える**: 250Hz 付近より下を切り（濁り防止）、9〜10kHz より上を落とす（耳が痛くならない）。
- ディレイ（やまびこ）は、戻りの音を暗くする（200〜300Hz より下、5〜8kHz より上を削る）と、元の音の後ろに座る。テンポに合わせた付点8分（ギター・リード向け）や、左右に交互のピンポンは、広がりと動きが出る。
- → 反映済み: 残響の戻りに 250Hz ハイパスと 9kHz ローパス、前の間 30ms。
- 未反映: 楽器ごとに残響の量を変える（S-4 の続き）、テンポ同期のディレイ。

## 4. 周波数のすみ分けとステレオ
- 同じ帯域で重なると互いにかき消し合う（マスキング）。主役でないほうを細く削って、主役の場所を作る（例: キックを立たせたいなら、ベースの 60〜80Hz を少し引く）。
- **低音は真ん中に**: 約 125Hz より下は左右に振らず、モノラルにそろえる（位相の打ち消しが起きやすく、振っても聞こえない）。
- モノラルにして聞くと、パンだけで分けていた重なりが露わになる。左右を足してもきれいに聞こえる作りにする（左右の差だけを足す広がり処理はこれに合う。前回反映済み）。

## 5. ドラムの合成（録音がないときの音）
- キック: サイン波が高い所（約 150Hz）から低い所（約 40〜60Hz）へごく短く下がり、音量は指数的に消える（約 0.4秒）。
- スネア: 約 160〜200Hz の胴（サイン／三角波、約 0.25〜0.35秒）＋ノイズ（高域、短く）。
- ハイハット: 高域のノイズ（または金属的な矩形波の重ね）をハイパスで通し、とても短く切る。閉じは約 0.05秒、開きは 0.3秒以上。
- 現状の `voices.ts` はこの形に近い。録音版（サウンドフォント）が主なので、合成の細かい調整は後回し。

## 6. シンセ（リード・パッド）
- スーパーソウ: ノコギリ波を 5〜7本、少しずつ音程をずらして（detune 約 15〜30セント）重ね、左右に散らす。ずらしすぎる（35 以上）と音程が悪く聞こえ、力も落ちる。
- 厚みの出しすぎを避けるため、低音（約150Hz 未満）は切る。コーラスと残響、サイドチェインと相性がよい。
- 現状の `lead` は 3本（±9セント）で、控えめ。5本に増やす余地あり（未反映）。

## 7. 民族楽器の音色
- 尺八: 基音に、2倍・3倍の倍音（偶数・奇数とも）と息のノイズが混ざるのが音色の核。息の量・倍音の量で、澄んだ音・かすれた音が変わる。→ 反映済み: 息のノイズ（尺八は多め・パンフルート・オカリナは少なめ）。
- 琴・シタール: 撥弦。弦をはじいた直後に明るく、すぐ高域が落ちる。シタールは共鳴弦のうなり（少しずれた弦の重なり）。→ 反映済み（前回）。
- 撥弦は、短いノイズを遅延線でくり返す Karplus–Strong 法でも作れる（未反映）。

## 8. 音量（ラウドネス）
- 配信の基準は -14 LUFS だが、これは再生側の目標で、作る側の決まりではない。実際の市販曲は、ロック -13〜-10、メタル -12〜-9（ラウドメタルはさらに大きく）、EDM -10〜-6 LUFS。
- ピークは -1dBTP 以下（圧縮して配信するときの割れを防ぐ）。
- **ピークと平均の差（crest）が小さすぎると疲れる**: 音量だけ上げて詰めると、リズムの粒が消える。9〜10dB 以上は残したい。
- → 現状の試作曲: メタル -6.4 LUFS（crest 7.3dB）は詰まり気味。下の「次の候補」に入れる。

## 作曲ソフトの次の候補（未反映）
1. ドラムを太鼓ごとの経路に分け、キック・スネア・ハイハットに別々のEQ・圧縮をかける（現状は1つの経路で全体を処理）。
2. 楽器ごとの残響の送り量（弦・パッド・ピアノは多め、ドラム・ベースは少なめ）。
3. テンポ同期のディレイ（付点8分、ピンポン、戻りは暗く）。
4. 125Hz より下をモノラルにそろえる処理。
5. `lead` のスーパーソウ化（5本）。
6. ラウド系の詰まり（crest）を、アンプ段の見直しで戻す。
