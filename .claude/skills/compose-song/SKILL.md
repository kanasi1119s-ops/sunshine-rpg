---
name: compose-song
description: サンシャイン作曲ソフトの形式で、Claude Code 自身がオリジナルの曲（BGM）を書き、確かめ、MIDI・WAV・作曲ソフトのプロジェクトに書き出す（必要ならゲームの曲として登録する）。「曲を作って」「BGMを作曲して」「この曲を直して」と頼まれたときに使う。APIキーはいらない。
---

# 曲を作る（Claude Code から作曲ソフトを使う）

APIキーは使わない。曲は、あなた（Claude Code）が「AIソング形式」のJSONで書き、`tools/composer/song.mjs` で確かめて書き出す。

## 手順

1. **形式を読む**: `node tools/composer/song.mjs guide` を実行し、書き方・楽器の一覧・よい曲にするコツを読む。見本は `assets-src/ai-songs/harbor-night.json`。
2. **依頼を整理する**: 場面・雰囲気・テンポ・長さ（指定がなければ60〜90秒）・使いたい楽器。あいまいなら、RPGの場面に合わせて自分で決めてよい。
2.5. **設計図と進行を先に決める**（曲の個性が決まる所。docs/sound/ai-composition-workflow.md の 2・3 節）: `node tools/composer/chord-pick.mjs --scene <場面> --avoid-last 3` で直近の曲と違う進行の候補を出し、`node tools/composer/song.mjs plan-template` の雛形から `assets-src/ai-songs/<名前>.plan.json`（属性カードとセクション表）を書いて、`node tools/composer/song.mjs plan-check <plan.json>` で直す。description に「入り方: 5。終わり方: …。動機: E4:1 G4:1 A4:2」を書く。コードごとの長さ `Am*2`・セクション別の進行 `sectionChords`・転調 `modulate`・ループの継ぎ目 `loopTail` が使える（`song.mjs guide`）。
3. **曲を書く**: `assets-src/ai-songs/<英小文字の名前>.json` に書く。
   - **完全なオリジナルにする**（CLAUDE.md 1-1）。既存曲のメロディ・特徴的なコード進行を写さない。「〜風」はジャンルと雰囲気だけを参考にする。
   - メロディは曲全体ぶん書き、Aメロ・Bメロ・サビのように変化をつける。ドラムやリフは1〜2小節の型を書けば、くり返して埋まる。
   - 各パートの拍の合計を、コードの数 × barsPerChord × repeats × beats にそろえる（足りない分はくり返し、はみ出た分は切られて注意が出る）。
4. **確かめて書き出す**: `node tools/composer/song.mjs build assets-src/ai-songs/<名前>.json --wav`
   - `×` が出たら、書かれた場所（`parts[0]（メロディ）: 音名が読めません「H4:1」` など）を直して、もう一度 build する。
   - `注意:` は自動チェックのヒント（低音のにごり・同じ音域のぶつかり・単調さ。`--wav` のときは音割れ・低音の多すぎ・強弱の平らさ・途中の無音も）。直すと良くなるので、出たら曲を直して build し直す。直さないなら、理由を報告に書く。
   - 出力は `dist-songs/`（gitには入れない）: 作曲ソフトで開けるプロジェクト（`.sunshine-song.json`）・MIDI・WAV。
   - **段階ビルド**: 一度に全部を書かず、「設計図 → 進行 → 旋律 → ベース・ドラム → 和音 → 飾り」の各段階で `build`（WAVなし）を回し、`×` と `注意:` を読んでから次の段階に進む。注意と `node tools/audio-check/score-check.mjs <曲.json> --facts`（小節番号つきの事実の一覧）を貼って、**1つずつ**直す。
   - 書き出し後: `node tools/composer/song.mjs gate <WAV> --save <曲ID>` で合否表（○／要直し）を出し、直したら同じ測定をもう一度回して `song.mjs log <曲ID> --before .. --change .. --after .. --ear ..` で1行残す。直前の曲との重なりは `song.mjs novelty <曲.json>`。
   - `--edition real|ps2|modern` でサウンドの版を選べる（既定は real＝実楽器）。
   - WAV は Playwright と Chromium が必要。なければ、作曲ソフト（`node tools/composer/build.mjs` で作る `dist-composer/index.html`）でプロジェクトを開き、「WAVで書き出す」を押すよう案内する。
5. **聴いてもらう**: WAV（またはプロジェクト）を利用者に渡す。自分では音を聴けないので、「こう作った」（調・テンポ・構成・楽器）を説明し、感想をもらって直す。直すときは同じJSONを書きかえて、もう一度 build する。
6. **ゲームに入れるとき**（頼まれたときだけ）: `--register <曲ID> --scene "<場面>"` をつけて build する。`src/audio/songs/<曲ID>.sunshine-song.json` ができ、ゲームの曲一覧とBGMプレイヤーに入る。鳴らす場面は、ゲーム側の `bgmId` に曲IDを書いて決める。既存の曲を差しかえるときは `docs/decisions.md` に理由を書く（CLAUDE.md 1-7）。

## 注意
- 仮の曲は、`description` と `docs/progress.md` に「仮」と書く（CLAUDE.md 1-4）。
- 言語はすべて日本語（曲名・説明・報告）。
