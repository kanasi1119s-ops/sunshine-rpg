import { REST, type NoteEvent, type Score } from "./score";

/**
 * 第3章（鉄鏈鉱山）のBGM。`docs/sound/tracks.md`の方針に沿ってオリジナルで作曲した。
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
 * 鉄鏈鉱山の町（BGM）。
 * 現代的な工夫: 低音に「ツルハシを打つような」歯切れのよい2拍刻みのリズム（休符を挟む
 * スタッカート）を置き、働く町の重みを出した。旋律はAマイナーの素朴な民謡風。
 */
export const CHAPTER3_TOWN_THEME: Score = {
  tempoBpm: 96,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.22,
      notes: notes(
        "A4:1 C5:1 E5:1 D5:1 C5:1 B4:1 A4:2 " +
          "G4:1 B4:1 D5:1 C5:1 B4:1 A4:1 E4:2 " +
          "A4:1 C5:1 E5:1 G5:1 F5:1 E5:1 D5:2 " +
          "C5:1 B4:1 A4:1 B4:1 A4:4",
      ),
    },
    {
      // ツルハシのリズム: 打つ→休む、を2拍単位で繰り返す。
      waveform: "triangle",
      volume: 0.18,
      notes: notes(
        "A2:0.5 R:0.5 A2:0.5 R:0.5 A2:0.5 R:0.5 E3:0.5 R:0.5 " +
          "G2:0.5 R:0.5 G2:0.5 R:0.5 E2:0.5 R:0.5 E2:0.5 R:0.5 " +
          "F2:0.5 R:0.5 F2:0.5 R:0.5 C3:0.5 R:0.5 C3:0.5 R:0.5 " +
          "E2:0.5 R:0.5 E2:0.5 R:0.5 A2:2",
      ).concat(
        notes(
          "A2:0.5 R:0.5 A2:0.5 R:0.5 A2:0.5 R:0.5 E3:0.5 R:0.5 " +
            "G2:0.5 R:0.5 G2:0.5 R:0.5 E2:0.5 R:0.5 E2:0.5 R:0.5 " +
            "F2:0.5 R:0.5 F2:0.5 R:0.5 C3:0.5 R:0.5 C3:0.5 R:0.5 " +
            "E2:0.5 R:0.5 E2:0.5 R:0.5 A2:2",
        ),
      ),
    },
    {
      waveform: "sine",
      volume: 0.08,
      notes: notes("A3:8 G3:8 F3:8 E3:8"),
    },
  ],
};

/**
 * 鉄鏈鉱山の坑内（BGM）。
 * 現代的な工夫: 遅いテンポの低い持続音（ドローン）に、間を空けた高音の
 * 「しずく」の音を遠くから響かせ、暗い坑道の反響と緊張感を出した。
 */
export const CHAPTER3_MINE_THEME: Score = {
  tempoBpm: 72,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes("D3:8 Bb2:8 A2:8"),
    },
    {
      // 遠くの反響: 長い休符のあいだに、ぽつりと高い音が落ちる。
      waveform: "sine",
      volume: 0.12,
      notes: notes(
        "R:2 A5:0.5 R:1.5 F5:0.5 R:3.5 " +
          "D5:0.5 R:3.5 R:1 E5:0.5 R:2.5 " +
          "R:2 D5:0.5 R:1.5 A4:1 R:3",
      ),
    },
    {
      waveform: "square",
      volume: 0.09,
      notes: notes("D4:1 F4:1 A4:2 R:4 D4:1 F4:1 E4:2 R:4 Bb3:2 D4:2 C4:2 R:2"),
    },
  ],
};

/**
 * ボス戦「実験の歪み」（BGM）。
 * 現代的な工夫: 機械が回るような16分音符の低音ベースを走らせ、その上で
 * ノコギリ波の旋律が半音でせり上がる。「暴走する装置」の不安定さを出した。
 */
export const CHAPTER3_BOSS_THEME: Score = {
  tempoBpm: 152,
  loop: true,
  tracks: [
    {
      waveform: "sawtooth",
      volume: 0.17,
      notes: notes(
        "E5:1 E5:0.5 F5:0.5 E5:1 B4:1 " +
          "E5:1 E5:0.5 F5:0.5 G5:1 F5:1 " +
          "A5:1 A5:0.5 G5:0.5 F5:1 E5:1 " +
          "D#5:1 E5:1 B4:1 R:1",
      ),
    },
    {
      // 機械のような16分音符の刻み。
      waveform: "square",
      volume: 0.13,
      notes: notes(
        "E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 G2:0.25 G2:0.25 G2:0.25 G2:0.25 " +
          "E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 E2:0.25 F2:0.25 F2:0.25 F2:0.25 F2:0.25 F#2:0.25 F#2:0.25 F#2:0.25 F#2:0.25 " +
          "A2:0.25 A2:0.25 A2:0.25 A2:0.25 A2:0.25 A2:0.25 A2:0.25 A2:0.25 G2:0.25 G2:0.25 G2:0.25 G2:0.25 F2:0.25 F2:0.25 F2:0.25 F2:0.25 " +
          "B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25 B2:0.25",
      ),
    },
    {
      waveform: "triangle",
      volume: 0.14,
      notes: notes("E3:4 E3:4 A3:4 B3:4"),
    },
  ],
};
