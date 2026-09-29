import { REST, type NoteEvent, type Score } from "./score";

/**
 * 第4章（砂音）のBGM。`docs/sound/tracks.md`の方針に沿ってオリジナルで作曲した。
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
 * 砂音の町（BGM）。砂漠の隊商都市のにぎわい。
 * 現代的な工夫: 旋律はD音の上で、2度が半音に近づく異国風の音階（D・Eb・F#・G・A・Bb・C）。
 * 低音は「ドン・タタ・ドン」の3拍子のかけ合い（太鼓のような短い低音と休符）で、
 * 隊商が行き交う足取りを表した。
 */
export const CHAPTER4_TOWN_THEME: Score = {
  tempoBpm: 108,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.2,
      notes: notes(
        "D5:1 Eb5:0.5 F#5:0.5 G5:1 F#5:1 Eb5:1 D5:1 " +
          "A4:1 Bb4:0.5 C5:0.5 D5:2 R:1 D5:1 " +
          "Eb5:1 F#5:0.5 G5:0.5 A5:1 G5:1 F#5:1 Eb5:1 " +
          "D5:1 C5:1 Bb4:1 A4:1 D5:4",
      ),
    },
    {
      // 太鼓のような短い低音。「ドン・タタ・ドン」を繰り返す。
      waveform: "triangle",
      volume: 0.19,
      notes: notes(
        "D3:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:0.5 R:0.5 " +
          "D3:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:0.5 R:0.5 " +
          "D3:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:0.5 R:0.5 " +
          "Bb2:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:0.5 R:0.5 " +
          "G2:0.5 R:0.5 D3:0.25 D3:0.25 R:0.5 G2:0.5 R:0.5 " +
          "G2:0.5 R:0.5 D3:0.25 D3:0.25 R:0.5 G2:0.5 R:0.5 " +
          "D3:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:0.5 R:0.5 " +
          "A2:0.5 R:0.5 A2:0.25 A2:0.25 R:0.5 D3:3",
      ),
    },
    {
      // 風のような高音の飾り（間を空けてきらりと鳴る）
      waveform: "sine",
      volume: 0.08,
      notes: notes("R:3 D6:0.5 R:3.5 F#6:0.5 R:1.5 R:3 G6:0.5 R:2.5 R:1 A5:0.5 R:2.5 D6:0.5 R:0.5 R:6"),
    },
  ],
};

/**
 * 隊商の野営地（BGM）。夜の砂漠、たき火のまわり。
 * 現代的な工夫: ゆっくりしたテンポで、低い持続音（ドローン）の上に、
 * 静かなアルペジオを1音ずつ落とす。星空のような、広くて少し心細い響きにした。
 */
export const CHAPTER4_CAMP_THEME: Score = {
  tempoBpm: 72,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: notes("A2:8 G2:8 F2:8 E2:8"),
    },
    {
      waveform: "sine",
      volume: 0.13,
      notes: notes(
        "A4:1 C5:1 E5:1 A5:1 E5:1 C5:1 A4:1 R:1 " +
          "G4:1 B4:1 D5:1 G5:1 D5:1 B4:1 G4:1 R:1 " +
          "F4:1 A4:1 C5:1 F5:1 C5:1 A4:1 F4:1 R:1 " +
          "E4:1 G#4:1 B4:1 E5:1 B4:1 G#4:1 E4:2",
      ),
    },
    {
      // たき火のはぜる音のような、まばらな高い音
      waveform: "square",
      volume: 0.05,
      notes: notes("R:4 E6:0.25 R:3.75 R:3 C6:0.25 R:4.75 R:6 A5:0.25 R:1.75 R:2 B5:0.25 R:5.75"),
    },
  ],
};

/**
 * ボス戦「砂嵐の歪み」（BGM）。
 * 現代的な工夫: ノコギリ波の旋律を、半音ずつ渦を巻くように上下させ、砂嵐が巻き上がる不安定さを出した。
 * 低音は16分音符で細かく揺れ動き、途中で1音ずつ半音上がって緊張を高める。
 */
export const CHAPTER4_BOSS_THEME: Score = {
  tempoBpm: 148,
  loop: true,
  tracks: [
    {
      waveform: "sawtooth",
      volume: 0.16,
      notes: notes(
        "D5:0.5 Eb5:0.5 D5:0.5 C#5:0.5 D5:1 A4:1 " +
          "D5:0.5 Eb5:0.5 F5:0.5 Eb5:0.5 D5:1 G5:1 " +
          "F#5:0.5 G5:0.5 F#5:0.5 F5:0.5 E5:1 Bb4:1 " +
          "A4:0.5 Bb4:0.5 A4:0.5 G#4:0.5 A4:2",
      ),
    },
    {
      waveform: "square",
      volume: 0.12,
      notes: notes(
        "D2:0.25 D2:0.25 A2:0.25 D2:0.25 D2:0.25 D2:0.25 A2:0.25 D2:0.25 D2:0.25 D2:0.25 A2:0.25 D2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 Eb2:0.25 " +
          "D2:0.25 D2:0.25 A2:0.25 D2:0.25 D2:0.25 D2:0.25 A2:0.25 D2:0.25 E2:0.25 E2:0.25 B2:0.25 E2:0.25 F2:0.25 F2:0.25 F2:0.25 F2:0.25 " +
          "F#2:0.25 F#2:0.25 C#3:0.25 F#2:0.25 F#2:0.25 F#2:0.25 C#3:0.25 F#2:0.25 G2:0.25 G2:0.25 D3:0.25 G2:0.25 Ab2:0.25 Ab2:0.25 Ab2:0.25 Ab2:0.25 " +
          "A2:0.25 A2:0.25 E3:0.25 A2:0.25 A2:0.25 A2:0.25 E3:0.25 A2:0.25 Bb2:0.25 Bb2:0.25 Bb2:0.25 Bb2:0.25 A2:0.5 A2:0.5",
      ),
    },
    {
      waveform: "triangle",
      volume: 0.14,
      notes: notes("D3:4 D3:4 F#3:4 A3:4"),
    },
  ],
};
