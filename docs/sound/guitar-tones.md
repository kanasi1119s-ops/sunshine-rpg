# ギターの音色プリセット（guitarTone）

人間が聞き比べて「いい」と言ったギターの音を、名前で使い回すための一覧。中身は `src/audio/guitar-tones.ts`。
AIソング形式のパートに `"guitarTone": "<名前>"` と書くと、アンプ・歪み・高音・キャビネット・残響・ディレイがまとめて入る。
パートに同じ項目（`amp`・`reverb` など）を書けば、そちらが優先。プリセットを使った曲は、自動のしゃくり（`autoScoop`）も止まる。

| 名前 | 音 | 中身 | 決めた日・曲 |
|---|---|---|---|
| `warm-lead-a` | 響く温かいリード。浅い歪みで中域（1〜2kHz）が太く、2〜4kHz を丸める | `amp: lead`・drive 1.0・tone -3・残響 0.32・ディレイ 0.75拍（mix 0.18・feedback 0.35）＋プレート 0.16 | 2026-10-15『ネオンハートビート』聞き比べ A |
| `warm-lead-b` | こもった軽い歪みのリード。中域（500Hz〜2kHz）が厚く丸い | `amp: overdrive`・drive 1.2・tone -4・録音キャビネット `dfc-ampmix`・残響とディレイは A と同じ | 2026-10-15『ネオンハートビート』聞き比べ B（曲の標準） |

- どちらも、ビブラート（`~`）・チョーキング（`^`）・自動のしゃくりなし（banned-sounds 17）。旋律やソロの `leadGuitar`・`guitar` 向け。
- `warm-lead-b` は録音キャビネット（David Fau Casquel、CC BY 3.0）を通す。この音をゲームに入れるときはクレジットが必要（docs/assets-credits.md）。キャビネットIRは作曲ソフトだけにあるので、ゲーム本体で鳴らすとキャビネットなしの音になる。
- 足すとき: 聞き比べで人間が選んだ音だけを、`GUITAR_TONES` に名前・説明・決めた経緯と一緒に足し、この表にも書く。

例:
```json
{ "instrument": "leadGuitar", "role": "旋律", "volume": 0.16, "pan": 0.08, "gainDb": 3, "guitarTone": "warm-lead-b", "notes": "..." }
```
