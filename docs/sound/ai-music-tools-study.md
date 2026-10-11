# 他社のAI作曲ソフトは、どう曲を作っているか（2026-10-11 調査）

調べた先: [Amplify「SunoのAIモデルのつくり方」](https://amplifypartners.com/barrchives/how-suno-builds-ai-models-for-musicians) /
[VI-Control「SunoとUdioの技術」](https://vi-control.net/community/threads/how-exactly-do-suno-ai-and-udio-com-work-technical-view.151041/) /
[AssemblyAI（MusicLM の紹介）](https://plushcap.com/analysis/assemblyai/what-ai-music-generators-can-do-and-how-they-do-it) /
[Hostman「AI音楽生成の比較」](https://hostman.com/blog/ai-music-generation-complete-guide-and-comparison) /
[Stable Audio の論文](https://arxiv.org/html/2402.04825v3)
※ Suno・Udio は非公開なので、外から推測された部分を含む。

## 1. 作り方は大きく2種類
| 方式 | 中身 | 代表 | 長所 | 短所 |
|---|---|---|---|---|
| 音そのものを作る（オーディオ生成） | 音を細かい数字の列（トークン）に変換し、次の数字を予想して並べる（言語モデルと同じ）。または拡散モデルで音を作る | Suno（Transformer・順番に生成）、Udio、MusicLM、MusicGen、Stable Audio（拡散・長さを指定できる） | 歌・実音がそのまま出る。仕上がりが一気に完成品 | 後から1音だけ直せない。MIDIが出ない。長い曲で構成が崩れやすい |
| 楽譜（MIDI）を作る（シンボリック生成） | 音符・コード・楽器の指定を作り、音源で鳴らす | AIVA、（うち） | MIDIで書き出せる。直せる。調・テンポ・楽器を指定できる | 音は音源しだい。歌は苦手 |
| 部品を組み合わせる（ループ／ステム） | 用意した音の部品を、ムード・長さに合わせて並べる | Soundraw、Mubert | 速い。長さを指定できる | 個性が出にくい |

## 2. 音のAIの仕組み（Suno・Udio・MusicLM 系）
- 音を圧縮して数字のトークンにする（コーデック。EnCodec など）。Transformer が、文章の説明（タグ・BPM・歌詞）に合わせてトークンの続きを予想し、最後に音へ戻す。
- 学習では、曲に「説明・タグ・BPM」を付けてペアにする。だからプロンプトの言葉（ジャンル、気分、楽器）が音に反映される。
- Suno は拡散より、順番に作る方式を選んだと言われる（「一歩ずつ作るほうが、おもしろい曲になりやすい」）。
- 長さの指定は、始まりの時刻と全体の長さを数字で入力する（Stable Audio／MusicLM）。セクションごとに様式を指定できるモデルもある。
- 利用者の選び方（どちらを気に入ったか）を学習の手がかりにする。
- 弱点: 長い曲の一貫した構成、声の正確さ、1音ずつの編集、歌詞の正確さ。

## 3. 他社の道具が利用者に出している操作
| 道具 | 操作 | 書き出し |
|---|---|---|
| Suno | 文章（スタイル）・歌詞・曲の長さ・参考音声・編集 | MP3／WAV／ステム（有料） |
| AIVA | スタイル・コード進行・MIDI・参考曲で作る。テンポ、キー、長さ、楽器 | MIDI／WAV／MP3 |
| Soundraw | ジャンル・ムード・長さ・テンポをボタンで選ぶ。曲の山を後から編集 | MP3／WAV／ステム |
| Mubert | ジャンル・ムード・長さ（5秒〜25分）。無限に流せる | MP3 |
| MusicGen | 文章か音声から短い曲 | WAV |

## 4. うちとの違いと、取り入れるもの
- うちは**楽譜を作る方式**（AIソング形式のJSON）。曲を後から1音単位で直せるのが強み。歌は作らない。
- 取り入れる:
  1. **「説明（タグ）→音」の対応を学ぶ**: 分析した録音の数字（帯域・重心・左右・コードの傾向）を、サウンドセットの名前と説明に結びつける（実装済み: `sound-sets.ts`）。
  2. **セクション単位の指定**: 「Aメロは静か、サビは全部」と言葉で決められるように、手引きに編曲の表を入れた（実装済み）。
  3. **長さの指定**: 「◯分◯秒」で曲の長さを決められる（`song.mjs` の長さ表示で確認）。
  4. **選んで学ぶ**: 聴いた人の好き嫌いを記録して、次の曲に反映する（`docs/sound/banned-sounds.md`）。
  5. **ステム書き出し**: パートごとの WAV を出す（実装済み: build の `--wav` とパート単位の確認）。
  6. 作ったあとに**自分で聴いて評価する自動チェック**（`song-check.ts`、`analyze.py`）。
- 取り入れない: 他人の曲を学習した音のコピー（著作権）。
