# 文章から4〜5分の曲を作る（Suno式の自動作曲）

スタイル指定の文章（と、あれば歌詞・テンポ・調）から、**4〜5分の曲**を自動で組み立てて、プロジェクト・MIDI・（WAV）に書き出すコマンドです。
APIキーも有料サービスもいりません。同じ文章・同じ種からは、いつも同じ曲ができます。

## 使い方

```bash
# 1曲（種を変えた3つのバージョンを作って、聴いて選ぶ）
node tools/composer/make.mjs one --title "炎の行進" --prompt "melodic metal, twin guitars, 160 BPM, E minor" --variations 3 --wav

# songs.json の全曲をまとめて（毎日10曲用）
node tools/composer/make.mjs batch songs.json --wav
node tools/composer/make.mjs batch songs.json --only 3 5        # 3曲目と5曲目だけ
```

- `songs.json`（形式は `assets-src/songs-example.json`）: `[{"title","prompt","lyrics","bpm","key_scale","time_signature","audio_duration"}, ...]`。`title` と `prompt` だけでも動く。
- 出力（`--out`、既定は `dist-songs/<日付>/`）: 曲ごとに `.sunshine-song.json`（作曲ソフトで開ける）・`.mid`・`.lyrics.txt`・`.report.json`（何を決めたか・構成・長さ・注意）、全体の `index.md`。
- `--wav` は Playwright と Chromium が必要（`npm i -D playwright && npx playwright install chromium`）。WAVを作れなくても、プロジェクトとMIDIは出る（警告つき）。作曲ソフトで開いて「WAVで書き出す」でも作れる。
- 長さは `audio_duration`（秒、既定270）に近づく。構成は「イントロ → A → A → B → サビ → …（くり返し）→ 間奏 → サビ → サビ → アウトロ」。結果が4:00〜5:00から外れると警告が出る。

## 文章から読み取るもの（`src/audio/style-prompt.ts`）

日本語・英語のキーワードから、曲調・味つけ・テンポ・調を決める。`songs.json` の `bpm`・`key_scale`・`time_signature` があれば、そちらを優先する。決まらない項目は曲調ごとの標準値。

| 言葉の例 | 曲調（Style） | 味つけ（flavor） |
|---|---|---|
| metal / メタル | metal | |
| death metal / デスメタル | deathmetal | |
| hardcore / ハードコア | hardcore | |
| prog metal / プログレ / 変拍子 | progmetal（7拍子） | |
| loud metal / ラウドメタル | metal | loud |
| loud rock / ラウドロック | rock | loud |
| dance rock / ダンス×ロック | dancerock | |
| phonk / フォンク | phonk | |
| rock x orchestra / ロック×オーケストラ | rock | orchestra |
| rock x wagakki / ロック×和楽器 | rock | wagakki |
| jazz / R&B / soul / funk / EDM / pop / folk / ambient など | jazz・rnb・electro・jpop・folk・space など | |

- **loud**: リズムギターを同じ刻みで2本に倍にして左右いっぱい（-0.9／0.9）に振り、`loudmetal`（メタル系）または `loudrock`（ロック系）のアンプを通す。1本ずつの音量は 0.1 以下に抑える。
- **orchestra**: 弦3声・ブラス・合唱・ティンパニを足す（サビでブラスとティンパニが入る）。
- **wagakki**: 琴の分散和音・三味線の刻み・尺八の長い音・太鼓（タム）を足す。
- orchestra・wagakki は4拍子の曲だけ（7拍子のプログレには付かない。警告が出る）。

## 何ができて、何ができないか（正直なところ）

- できる: 4〜5分の長さ・構成、10ジャンルの作り分け、歌詞ファイルの保存、10曲の一括生成、結果の自動確認（長さ・構成・警告）。
- **歌声**: 曲に `lyrics_kana`（ひらがなの歌詞）を書くと、歌のメロディと歌声用の楽譜も作る。声にするのは PC 側の VOICEVOX（女声・波音リツが既定）。詳しくは `docs/sound/vocal.md`。`lyrics_kana` がない曲は歌わない。グロウル・シャウトはできない。
- 旋律は規則（コードの音を軸に音階を歩く）から作る。Sunoのような学習済みモデルの音楽とは別物で、**同じ曲調でも似た雰囲気になりやすい**。Aメロは3種類、B・間奏は2種類の旋律をまわして単調さを減らしているが、サビは同じ旋律のくり返し。
- 音の良し悪しは**耳で確かめる**。この文書の数値（長さ・構成）は、曲が聴ける状態かどうかを保証しない。
- 既存の曲のメロディ・コード進行は使わない（CLAUDE.md 1-1）。文章に実在のアーティスト名・曲名を書かない。

## 関連

- 曲の書き方（手書きの曲）: `.claude/skills/compose-song/SKILL.md`、`node tools/composer/song.mjs guide`
- 自動作曲の中身: `src/audio/songwriter.ts`（`SongSpec.targetSec` が90秒を超えると長尺モード、`SongSpec.flavor` で味つけ）
- テスト: `src/audio/songwriter-long.test.ts`、`src/audio/style-prompt.test.ts`、`src/audio/vocal-score.test.ts`
- 歌声: `docs/sound/vocal.md`
