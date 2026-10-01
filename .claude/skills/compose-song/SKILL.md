---
name: compose-song
description: サンシャイン作曲ソフトの形式で、Claude Code 自身がオリジナルの曲（BGM）を書き、確かめ、MIDI・WAV・作曲ソフトのプロジェクトに書き出す（必要ならゲームの曲として登録する）。「曲を作って」「BGMを作曲して」「この曲を直して」と頼まれたときに使う。APIキーはいらない。
---

# 曲を作る（Claude Code から作曲ソフトを使う）

APIキーは使わない。曲は、あなた（Claude Code）が「AIソング形式」のJSONで書き、`tools/composer/song.mjs` で確かめて書き出す。

## 手順

1. **形式を読む**: `node tools/composer/song.mjs guide` を実行し、書き方・楽器の一覧・よい曲にするコツを読む。見本は `assets-src/ai-songs/harbor-night.json`。
2. **依頼を整理する**: 場面・雰囲気・テンポ・長さ（指定がなければ60〜90秒）・使いたい楽器。あいまいなら、RPGの場面に合わせて自分で決めてよい。
3. **曲を書く**: `assets-src/ai-songs/<英小文字の名前>.json` に書く。
   - **完全なオリジナルにする**（CLAUDE.md 1-1）。既存曲のメロディ・特徴的なコード進行を写さない。「〜風」はジャンルと雰囲気だけを参考にする。
   - メロディは曲全体ぶん書き、Aメロ・Bメロ・サビのように変化をつける。ドラムやリフは1〜2小節の型を書けば、くり返して埋まる。
   - 各パートの拍の合計を、コードの数 × barsPerChord × repeats × beats にそろえる（足りない分はくり返し、はみ出た分は切られて注意が出る）。
4. **確かめて書き出す**: `node tools/composer/song.mjs build assets-src/ai-songs/<名前>.json --wav`
   - `×` が出たら、書かれた場所（`parts[0]（メロディ）: 音名が読めません「H4:1」` など）を直して、もう一度 build する。
   - 出力は `dist-songs/`（gitには入れない）: 作曲ソフトで開けるプロジェクト（`.sunshine-song.json`）・MIDI・WAV。
   - `--edition real|ps2|modern` でサウンドの版を選べる（既定は real＝実楽器）。
   - WAV は Playwright と Chromium が必要。なければ、作曲ソフト（`node tools/composer/build.mjs` で作る `dist-composer/index.html`）でプロジェクトを開き、「WAVで書き出す」を押すよう案内する。
4b. **仕上がりを数値で検査する**: `python3 tools/audio-check/producer-check.py dist-songs/<名前>.wav --genre normal|loud|soft`（numpy と ffmpeg が必要）。ピーク・頭打ち・直流成分・低音のモノラル・ループのつなぎ目・耳に痛い帯域は必須（×なら直す）。音量・ピークと平均の差・左右・残響の尾・音の起伏は目安（△は理由を考える）。ジャンルは、ラウド（メタル・ロック・ダンス）なら loud、繊細・アンビエントなら soft。音作りの定石は `docs/sound/guitar-bass-drums-sound-design.md` と `docs/sound/sound-design-study-2.md`、ドラムの型は `docs/sound/drum-patterns.md`。
5. **聴いてもらう**: WAV（またはプロジェクト）を利用者に渡す。自分では音を聴けないので、「こう作った」（調・テンポ・構成・楽器）を説明し、感想をもらって直す。直すときは同じJSONを書きかえて、もう一度 build する。
6. **ゲームに入れるとき**（頼まれたときだけ）: `--register <曲ID> --scene "<場面>"` をつけて build する。`src/audio/songs/<曲ID>.sunshine-song.json` ができ、ゲームの曲一覧とBGMプレイヤーに入る。鳴らす場面は、ゲーム側の `bgmId` に曲IDを書いて決める。既存の曲を差しかえるときは `docs/decisions.md` に理由を書く（CLAUDE.md 1-7）。

## 注意
- 仮の曲は、`description` と `docs/progress.md` に「仮」と書く（CLAUDE.md 1-4）。
- 言語はすべて日本語（曲名・説明・報告）。
