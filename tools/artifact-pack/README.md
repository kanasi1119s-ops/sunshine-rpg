# 大きな1ファイルのHTMLを Artifact に載せる（2026-10-16）

作曲ソフト（約300MB）・BGMプレイヤー（約21MB）は、音源を data:URL で1ファイルに埋め込んでいるので、そのままでは Artifact（ページ16MBまで・1ファイル15MBまで）に載らない。
`split.py` で、大きな埋め込み（約200KB以上）を `sf/NNN.wasm`（音源。Artifact が配れる形の拡張子にしている）・`sf/NNN.js`（ワークレット）に出し、14MB をこえるものは `sf/NNN.pK.wasm` に分ける。
ページの先頭に `shim.html` を入れ、`fetch`（分割したものをつなぐ）と `atob`（作曲ソフトが埋め込みを atob で取り出すところで、`sf/…` のファイルをその場で読む）を差しかえる。

```bash
node tools/composer/build.mjs 出力/full.html          # 作曲ソフト（と sfx-lab.html）
python3 tools/artifact-pack/split.py 出力/full.html 出力/site
node tools/bgm-player/build.mjs 出力/bgm.html
python3 tools/artifact-pack/split.py 出力/bgm.html 出力/bgm-site   # BGMプレイヤーは先頭に <meta charset="utf-8"> を足す
```

公開: 1回の publish は64MBまで（ページも毎回送る）なので、ファイルを45MBずつに分けて、同じ Artifact に何回かに分けて載せる。
- 作曲ソフト: https://claude.ai/artifact/NeHH2jVJnHYiaHM1bjjtZM
- BGMプレイヤー: https://claude.ai/artifact/ExgpkG5gvg9HXf7avEwtnL
- SE ラボ: https://claude.ai/artifact/8fpr6dSbPtfg3hXupXycsj
- ドット絵エディタ: https://claude.ai/artifact/Xo7VKZU9cHJk15BnvVmxdp

Artifact の中では、ファイルの保存（WAV・MIDI・JSON などのダウンロード）と、AI への問い合わせは動かない。
