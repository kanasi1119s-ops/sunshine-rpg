# ギター・ベース・ドラムの音の作り方（調べたこと）

2026-10-02、人間の指示で調べた。ミキシング解説サイトの一般的な目安をまとめたもので、特定の曲や機材の音を写したものではない。
数値は目安で、最後は耳で決める。作曲ソフトの反映先は `src/audio/amp-rack.ts`（`build`）と `src/audio/amp.ts`。

## 出典
- ギター: [Electric Guitar EQ Guide（Music Guy Mixing）](https://www.musicguymixing.com/electric-guitar-eq/) / [Guitar EQ Cheat Sheet（Producer Hive）](https://producerhive.com/music-production-recording-tips/guitar-eq-cheat-sheet/) / [How to EQ Electric Guitar（Stock Music Musician）](https://www.stockmusicmusician.com/blog/electric-guitar-eq-tips) / [Gearspace: 歪んだギターの帯域](https://gearspace.com/threads/what-frequencies-should-i-watch-when-eqing-a-distorted-guitar.418561/)
- ベース: [Mixing Bass（Sound On Sound）](https://www.soundonsound.com/techniques/mixing-bass) / [Mixing DI Bass Guitar（Sound On Sound）](https://www.soundonsound.com/techniques/mixing-di-bass-guitar) / [Bass DI and Amp Blend Guide](https://www.soundsheavy.com/mixing-techniques/bass-di-and-amp-blend/) / [How to Mix Bass Guitar（Audio Spectra）](https://audiospectra.net/how-to-mix-bass-guitar/)
- ドラム: [Drum EQ Cheat Sheet（Audio Spectra）](https://audiospectra.net/drum-eq-cheat-sheet/) / [How to Mix Drums（Boris FX）](https://borisfx.com/blog/how-to-mix-drums-a-complete-guide-for-mixing-drums/) / [Parallel Compression（Nail The Mix）](https://www.nailthemix.com/parallel-compression) / [Parallel Compression for Weightier Drums（FaderPro）](https://blog.faderpro.com/techniques/parallel-compression-drums/)

## ギター（歪み系）
- **低音を切る**: 80〜150Hz 以下はベース・キックの場所。ここを切ると、歪みが濁らず締まる（メタルは高め＝130Hz 前後）。
- **200〜500Hz は濁りやすい**: 箱鳴り・こもりの元（特に 400〜500Hz）。少し削る。厚みが足りないときは 150〜250Hz の「ふくらみ」を足す。
- **1〜3kHz が輪郭と食いつき**: 前に出る帯域。メタルは 600〜800Hz を削って（ドンシャリ）3kHz 付近で輪郭を出す方向、ロックは 1kHz 前後を厚くする方向。
- **5〜6kHz 以上は「ジャリ」（フィズ）**: 歪んだ音の高域は耳が痛くなる。ローパスで 5〜6kHz（強い歪みは 4.5〜5kHz）に落とす。7kHz 以上はほぼ不要。
- **歪みは2段に分け、段の間で高域を落とす**: 1段で深く歪ませるより、前段で低音を削り、2段で歪ませ、間にローパスを入れるほうがざらつかず、音が締まる（`loudmetal` はこの形）。
- **二重がけに注意**: 録音がすでに歪んだ音に、アンプでさらに歪みをかけると濁る。歪みはどこか1か所でかける。
- 左右に2本（同じ刻み）を振ると壁になる。1本ずつ少しタイミングをずらすと広がるが、揃えたほうが重い（メタル）。

## ベース
- **帯域**: 30Hz 以下は不要（切る）／ 60〜120Hz が重さ ／ 250〜400Hz は濁り（少し削る）／ 400〜800Hz は鼻にかかる ／ 700Hz〜2kHz が音程のはっきりさとうなり ／ 2〜5kHz が弾いた瞬間（ピック・指）の粒。
- **圧縮**: アタックを遅め（20〜30ms）にして、弾き始めを残しつつ音量をそろえる。強くかけてもよいが、アタックとリリースを雑にすると歪む。
- **低音は歪ませない**: 歪みは、低音（約150〜250Hz より下）と分けて、高い側だけにかける（直接の音と、アンプの音を混ぜる「DI＋アンプ」の考え方）。重さはそのまま、輪郭だけ出る。
- キックとぶつかる 60〜100Hz は、どちらかを主役にする（キックが主役ならベースの 60Hz 付近を少し引く）。

## ドラム
- **キック**: 60〜80Hz が重さ、3〜5kHz が「カチッ」（ビーターの音）。その間の 200〜400Hz（こもり・箱鳴り）を削る。圧縮は 4:1・アタック 20〜30ms で、強い打撃に 3〜5dB。
- **スネア**: 500Hz〜1.5kHz の箱鳴りを削り、3〜5kHz で打撃の立ち上がり、8kHz 以上の持ち上げで抜けをよくする。ゴーストノート（弱い音）を挟むと動きが出る。
- **ハイハット**: 200Hz 以下は切る。1〜2kHz が金属的に刺さるなら少し削り、8〜12kHz で「空気」。圧縮はほとんどしない。
- **パラレルコンプ**: 原音に、強く圧縮（比 8:1〜12:1、6〜12dB 圧縮）した音を混ぜる。原音のアタックを残したまま、厚みと密度が出る。メタル・ロックのドラムの「どっしり」の定番。
- **トランジェント**: 打撃の頭（アタック）を少し持ち上げ、伸び（サスティン）を詰めると、締まって前に出る。

## 作曲ソフトへの反映（2026-10-02）
- ベース: 32Hz のハイパス、320Hz の濁りを -2dB、アタック 25ms の軽い圧縮を追加。
- メタルのベース: 約200Hz で2つの道に分け、低い側は歪ませず重く、高い側だけ軽く歪ませる。
- ドラム（ロック・メタル）: 35Hz のハイパスと、強く圧縮した音を混ぜるパラレルコンプを追加。
- ギター: 2段歪み・高域のローパス（`loudmetal`・`loudrock`）は前回までに反映済み。歪みの二重がけを避ける（歪ませるアンプを指定したら元の音色はクリーン）。
