# 試作曲の音声（聴いて確かめる用）

`assets-src/ai-songs/` の曲を、作曲ソフトと同じ音（real版＝録音音源・アンプ・仕上げ）で書き出したものです（2026-09-30）。**すべてオリジナル曲**で、外部の音源・曲は含みません。ゲームには読み込まれません（ゲームは曲データから鳴らします）。

| ファイル | 曲 | 元のデータ | メモ |
|---|---|---|---|
| `sky-piercing-pulse.mp3` | 天をつらぬく鼓動（仮） | `../sky-piercing-pulse.json` | ダンス×ロック。歪んだギター・シンセのアルペジオ・リードギター・弦・合唱・ブラス |
| `sky-piercing-pulse-clean.mp3` | 天をつらぬく鼓動（きれいな版）（仮） | `../sky-piercing-pulse-clean.json` | 同じメロディ・コードで、ピアノ・エコーギター・弦・鐘・合唱中心。ベースはメロディのように動く |
| `sample-cleandance-auto.mp3` | （見本）自動作曲「きれいなダンス」 | 作曲エンジン `composeSong`（曲調 cleandance・D短調・テンポ150・乱数の種11・長さ110秒を指定） | 作曲ソフトの自動作曲だけで作った見本。手直しなし |
| `sample-dancerock-auto.mp3` | （見本）自動作曲「ダンス×ロック」 | 作曲エンジン `composeSong`（曲調 dancerock・D短調・テンポ150・乱数の種11・長さ110秒を指定） | 同上 |

- 曲データを直したら、`node tools/composer/song.mjs build <曲.json> --wav` で書き出し直し、`ffmpeg -i 〇〇.wav -b:a 256k 〇〇.mp3` で差しかえる。
- 音の仕上げの数値は `python3 tools/audio-check/analyze.py 〇〇.mp3` で測れる（目安は `docs/sound/reference-nihonichi-bgm.md`）。
- 見本の2曲は、作曲エンジンを変えると同じ設定でも音が変わる（2026-09-30 時点の音）。
