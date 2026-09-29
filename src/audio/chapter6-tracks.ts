import { REST, type NoteEvent, type Score } from "./score";

/**
 * 第6章（霜原）のBGM。`docs/sound/tracks.md`の方針に沿ってオリジナルで作曲した。
 * 既存曲のメロディ・コード進行は使っていない。全パートの合計拍数を揃えてある。
 */

/** "音名:拍数" の並びから音符列を作る小さな補助（"R:1" は休符）。 */
function notes(spec: string): NoteEvent[] {
  return spec.split(" ").map((token) => {
    const [name, beats] = token.split(":");
    return { note: name === "R" ? REST : name, durationBeats: Number(beats) };
  });
}

/**
 * 霜原の町（BGM）。雪に閉ざされた戦跡の町の、澄んだ冷たさとかすかなぬくもり。
 * 現代的な工夫: 旋律をD・F・G・A・Cの音だけで組み、高い鈴のような音を雪の粒のようにまばらに散らした。
 * 低音は2小節ごとにゆっくり動き、暖炉のような三角波の和音を重ねた。
 */
export const CHAPTER6_TOWN_THEME: Score = {
  tempoBpm: 76,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes(
        "D5:2 F5:1 A5:1 G5:2 F5:2 " +
          "D5:2 C5:1 D5:1 F5:4 " +
          "G5:2 A5:1 C6:1 A5:2 G5:2 " +
          "F5:2 D5:2 D5:4",
      ),
    },
    {
      waveform: "sine",
      volume: 0.16,
      notes: notes("D3:4 D3:4 Bb2:4 Bb2:4 C3:4 C3:4 D3:4 A2:4"),
    },
    {
      // 雪の粒のような高音
      waveform: "sine",
      volume: 0.07,
      notes: notes("R:3 A6:0.5 R:4.5 R:4 D7:0.5 R:3.5 R:2 F6:0.5 R:5.5 R:8"),
    },
  ],
};

/**
 * 戦跡の施設（BGM）。雪の下に眠る古い装置の、機械的な不気味さ。
 * 現代的な工夫: 低い持続音の上で、四角波の短い音が規則正しく脈打つ（止まりかけの機械の鼓動）。
 * 旋律は半音でわずかにずれた音を含め、「まだ動いている何か」の不安を出した。
 */
export const CHAPTER6_FACILITY_THEME: Score = {
  tempoBpm: 68,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes("D2:16 Bb1:16"),
    },
    {
      waveform: "square",
      volume: 0.05,
      notes: notes("A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 A3:0.5 R:1.5 " +
        "F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5 F3:0.5 R:1.5"),
    },
    {
      waveform: "sine",
      volume: 0.12,
      notes: notes(
        "D5:4 E5:2 F5:2 A4:4 C#5:4 " +
          "Bb4:4 C5:2 D5:2 F4:4 A4:4",
      ),
    },
  ],
};

/**
 * ボス戦「試作機の歪み」（BGM）。
 * 現代的な工夫: 四角波の旋律を、2音ずつ「ガシャン」と噛み合う歯車のように刻み、
 * 低音は休まず16分音符で回し続けた。4小節ごとに根音が下がり、重い機械が押しつぶしてくる圧力を出した。
 */
export const CHAPTER6_BOSS_THEME: Score = {
  tempoBpm: 148,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.13,
      notes: notes(
        "D5:0.5 D5:0.5 A5:1 F5:0.5 F5:0.5 C6:1 " +
          "D5:0.5 D5:0.5 A5:1 G5:1 F5:1 " +
          "Bb4:0.5 Bb4:0.5 F5:1 D5:0.5 D5:0.5 A5:1 " +
          "Bb4:0.5 Bb4:0.5 F5:1 E5:1 D5:1",
      ),
    },
    {
      waveform: "sawtooth",
      volume: 0.1,
      notes: notes(
        "D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 " +
          "D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 D2:0.25 D2:0.25 D3:0.25 D2:0.25 " +
          "Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 " +
          "Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25 Bb1:0.25 Bb1:0.25 Bb2:0.25 Bb1:0.25",
      ),
    },
    {
      waveform: "triangle",
      volume: 0.14,
      notes: notes("D3:4 D3:4 Bb2:4 Bb2:4"),
    },
  ],
};
