# 高品質な電子音の作り方（学習）と、作り直し（仮・聴き比べ中）

2026-10-25 記録。人間「電子音ももっとクオリティ高いの欲しいな。作り方学んできて」。
音色のレシピ（波形・重ね方）は `modern-synth-study.md` のまま。今回は「作り方の質」を上げた。作るのは `tools/soundfont/build-hq-synths.py`。
**まだ作曲ソフトの音は差しかえていない（人間が聴き比べて OK を出してから）。**

## 調べたこと（要点）
1. **折り返しのにごり**（[Dubspot](https://blog.dubspot.com/audio-aliasing-guide-music-production)）: 歪み・鋭い波形の高い倍音がナイキストを超えて折り返し、「ガラスのように刺さるザラつき」「音程と関係ない音」になる。非線形の処理は 4 倍以上（明るいシンセは 8〜16 倍）の細かさで。帯域を制限したオシレーターを使う。
2. **動き**（[KVR のアナログのドリフトの議論](https://www.kvraudio.com/forum/viewtopic.php?p=7408514)・[MusicRadar](https://www.musicradar.com/tuition/tech/how-to-add-life-and-depth-to-synths-with-subtle-modulation-effects-632490)）: 本物のシンセは 1本ずつの音程がゆっくり ±5 セントくらいゆれる（低い周波数寄りのノイズ）。変調はごく控えめに（トレモロ 20%・パン 10% など）。「少ないほうがよい」。
3. **重ね方**（[Native Instruments](https://blog.native-instruments.com/how-to-layer-leads/)・[トリケラテクノ](https://note.com/triceratechno/n/n03b202f8fb78)・[Attack Magazine](https://www.attackmagazine.com/technique/synth-secrets/sulta-synths-layered-melodic-leads/)）: 似た音を重ねず役割を分ける（アタック・本体・支え・空気）。アタックは主の層だけ強く。主はモノで真ん中、補助を左右に。200Hz より下はモノ、広がりは中高域。EQ は 200Hz 以下を切り 2〜5kHz を少し。リバーブは高域寄りでプリディレイ。強さのばらつきで人間らしく。
4. **スーパーソウ**（[MazQ](https://www.mazq-music.com/archives/28971377.html)）: 位相をそろえない（リトリガー OFF・位相のばらつき）。Vital なら 16 本・デチューン 20% が「派手」。重ねすぎると位相がずれてアタックがぼやける。
5. **OTT**（[EDMProd](https://www.edmprod.com/ott-plugin/)）: 88Hz・2.5kHz で 3 帯域。強いので混ぜて使う（マスターは 10〜20%）。
6. **サンプルにするとき**（[Audient](https://audient.com/tutorial/how-to-multisample-a-synth/)・[nurykabe](https://nurykabe.com/dump/docs/sampling/)）: 長めに録って後で短く。強さの段は音色が変わる時だけ意味がある。ループはゼロ付近でつなぎ、つなげにくければ長めのクロスフェード。

## 今のシンセを測った結果
| 測ったこと | 結果 |
|---|---|
| 折り返しのにごり（4倍の細かさで作った音とのちがい） | −27〜−38dB（スーパーソウの高い音が最悪 −27dB。ピコピコ −30、ポップリード −33） |
| ループ | 2秒のくり返し。ゆれも動きもない |
| 強さの段 | なし（強さで音色が変わらない） |
| 保存の圧縮（Vorbis q5） | 元の波形との差 −28dB（q10 で −39dB） |

## 作り直した作り方（build-hq-synths.py）
1. 4倍の細かさ（176.4kHz）で作って戻す → 測り直し: ピコピコの 4倍と 8倍の差は −58dB（前は −30dB）。にごりはほぼ消えた。
2. 1本ずつの音程のゆれ（音色ごとに 0.8〜4 セント。クリアな音は少なく）。ループの中で 1〜3 周ちょうど＝つなぎ目の差 0.04%。
3. ループ 2秒 → 3秒。
4. 空気の層（7〜14kHz の薄いノイズ。−30〜−38dB。音の大きさについていく）を伸ばす音にだけ。
5. 180Hz より下の左右の差をなくす。
6. 3帯域の上向きの圧縮を 10〜20% 混ぜる。
7. 保存の圧縮 q7。

## まだやっていないこと
- **強さの段**: 作曲ソフトは、パートの音量を MIDI の強さ（velocity）で表している（`audio-engine.ts`: 強さ＝34＋音量×強さ×430）。このまま強さで音色を変えると、ミックスの音量で音色が変わってしまう。音量（CC7）と強さを分けてから入れる。
- 聴き比べ: `電子音の聴き比べ（前→新）.mp3`（6音色。前→新の順）を人間に送った。OK が出たら `build-hq-synths.py` で SF3 を作って差しかえる。
