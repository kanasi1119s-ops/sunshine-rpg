import { REST, type NoteEvent, type Score } from "./score";

/**
 * 第5章（霧断崖）のBGM。`docs/sound/tracks.md`の方針に沿ってオリジナルで作曲した。
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
 * 霧断崖の町（BGM）。霧に包まれた古い宗教都市の静けさ。
 * 現代的な工夫: ゆったりしたテンポで、旋律をE・G・A・B・D（ペンタトニック）だけで組み、
 * 音と音のあいだに間を残した。高音の鐘のような音を、霧の向こうから響くようにまばらに重ねた。
 */
export const CHAPTER5_TOWN_THEME: Score = {
  tempoBpm: 84,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes(
        "E5:2 G5:1 B5:1 A5:2 G5:2 " +
          "E5:2 D5:1 E5:1 G5:4 " +
          "A5:2 B5:1 D6:1 B5:2 A5:2 " +
          "G5:2 E5:2 E5:4",
      ),
    },
    {
      waveform: "sine",
      volume: 0.17,
      notes: notes("E3:4 E3:4 C3:4 C3:4 D3:4 D3:4 E3:4 B2:4"),
    },
    {
      // 霧の向こうの鐘のような高音
      waveform: "sine",
      volume: 0.08,
      notes: notes("R:6 B6:0.5 R:1.5 R:8 E6:0.5 R:7.5 R:8"),
    },
  ],
};

/**
 * 記録の間（BGM）。岩壁を掘った古文書庫の、ひんやりした静寂。
 * 現代的な工夫: とてもゆっくりしたテンポで、低い持続音の上に、長い音を1つずつ置いた。
 * ときおり紙をめくるような小さな高音が鳴り、「誰かに見られている」ような落ち着かなさを出した。
 */
export const CHAPTER5_ARCHIVE_THEME: Score = {
  tempoBpm: 60,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes("A2:16 F2:16"),
    },
    {
      waveform: "sine",
      volume: 0.13,
      notes: notes(
        "A4:2 C5:2 E5:4 D5:2 C5:2 B4:4 " +
          "A4:2 C5:2 F5:4 E5:2 D5:2 A4:4",
      ),
    },
    {
      waveform: "square",
      volume: 0.04,
      notes: notes("R:5 A6:0.25 R:10.75 R:8 E6:0.25 R:7.75"),
    },
  ],
};

/**
 * ボス戦「予言の歪み」（BGM）。
 * 現代的な工夫: ノコギリ波の旋律を、同じ音の連打から一気に跳ね上げる形にして、
 * 文字が霧の中から浮かび上がって襲いかかる勢いを出した。低音は8分音符で休まず刻み、
 * 4小節ごとに根音を上げて追い立てる。
 */
export const CHAPTER5_BOSS_THEME: Score = {
  tempoBpm: 152,
  loop: true,
  tracks: [
    {
      waveform: "sawtooth",
      volume: 0.16,
      notes: notes(
        "E5:0.5 E5:0.5 G5:0.5 E5:0.5 B5:1 A5:1 " +
          "G5:0.5 G5:0.5 B5:0.5 G5:0.5 D6:1 B5:1 " +
          "A5:0.5 A5:0.5 C6:0.5 A5:0.5 E6:1 C6:1 " +
          "B5:1 A5:1 G5:1 F#5:1",
      ),
    },
    {
      waveform: "square",
      volume: 0.12,
      notes: notes("E2:0.5 E2:0.5 B2:0.5 E2:0.5 E2:0.5 E2:0.5 B2:0.5 E2:0.5 G2:0.5 G2:0.5 D3:0.5 G2:0.5 G2:0.5 G2:0.5 D3:0.5 G2:0.5 A2:0.5 A2:0.5 E3:0.5 A2:0.5 A2:0.5 A2:0.5 E3:0.5 A2:0.5 B2:0.5 B2:0.5 F#3:0.5 B2:0.5 B2:0.5 B2:0.5 F#3:0.5 B2:0.5"),
    },
    {
      waveform: "triangle",
      volume: 0.14,
      notes: notes("E3:4 G3:4 A3:4 B3:4"),
    },
  ],
};
