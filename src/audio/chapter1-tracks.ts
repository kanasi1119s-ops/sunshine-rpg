import type { Score } from "./score";

/**
 * 第1章（麦香野）のBGM。`docs/sound/tracks.md`の方針
 * （16bit風チップチューン×現代的な音づくり。全パートの合計拍数が
 * 揃うように作り、ループのつなぎ目で不自然に途切れないようにしている）
 * に沿ってオリジナルで作曲した。既存曲のメロディ・コード進行は使っていない。
 */

/**
 * 麦香野の村（BGM）。
 * 現代的な工夫: F→Bb→C→Fの進行に、9th・7thのテンション音を別パートで重ねる
 * （灯里の町テーマと同じ手法）。灯里が港町の明るさなのに対し、こちらは
 * 田畑と水車のある農村の、のどかで少し素朴な響きにしている。
 */
export const CHAPTER1_VILLAGE_THEME: Score = {
  tempoBpm: 104,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.24,
      notes: [
        { note: "F4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "C5", durationBeats: 1 },
        { note: "Bb4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "F4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "Bb4", durationBeats: 1 },
        { note: "D5", durationBeats: 1 },
        { note: "F5", durationBeats: 1 },
        { note: "D5", durationBeats: 1 },
        { note: "C5", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 2 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.16,
      notes: [
        { note: "F3", durationBeats: 4 },
        { note: "Bb3", durationBeats: 4 },
        { note: "C3", durationBeats: 4 },
        { note: "F3", durationBeats: 4 },
      ],
    },
    {
      // Fmaj9→Bbmaj7→C9→Fmaj9 のテンションだけを重ねる。
      waveform: "sine",
      volume: 0.1,
      notes: [
        { note: "G4", durationBeats: 4 },
        { note: "A4", durationBeats: 4 },
        { note: "D5", durationBeats: 4 },
        { note: "G4", durationBeats: 4 },
      ],
    },
    {
      waveform: "sine",
      volume: 0.05,
      notes: [{ note: "F2", durationBeats: 16 }],
    },
  ],
};

/**
 * 麦香野の水源（BGM）。掘り返された採掘跡がある、涸れた水源。
 * 現代的な工夫: 低音ドローン（E2）に対してBb3・B3のトライトーン／半音の
 * ぶつかりを重ね、「涸れる・歪む」という異様さを静かに滲ませている
 * （roles.md 3-7の不協和音を、町外れのテーマよりもさらに静かな場面向けに応用）。
 */
export const CHAPTER1_WATER_SOURCE_THEME: Score = {
  tempoBpm: 78,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.2,
      notes: [
        { note: "E4", durationBeats: 1 },
        { note: "R", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "F4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 1 },
        { note: "R", durationBeats: 2 },
        { note: "E4", durationBeats: 1 },
        { note: "G4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 2 },
      ],
    },
    {
      waveform: "sine",
      volume: 0.09,
      notes: [{ note: "E2", durationBeats: 16 }],
    },
    {
      // ドローン（E2）と半音・トライトーンでぶつかる音を重ねる。
      waveform: "sawtooth",
      volume: 0.06,
      notes: [
        { note: "Bb3", durationBeats: 8 },
        { note: "F4", durationBeats: 8 },
      ],
    },
  ],
};

/**
 * ボス戦「水涸れの歪み」（BGM）。
 * 現代的な工夫: 通常戦闘よりも前のめりにしつつ、水源テーマと同じ
 * E～Bbのトライトーンを軸に、二つ目のフレーズでF～Bのトライトーンへ
 * 半音上げてずらすことで、序章ボス戦とは違う「乾き切っていく」不安定さを出している。
 */
export const CHAPTER1_BOSS_THEME: Score = {
  tempoBpm: 158,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.3,
      notes: [
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.22,
      notes: [
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "F2", durationBeats: 0.5 },
        { note: "B2", durationBeats: 0.5 },
        { note: "F2", durationBeats: 0.5 },
        { note: "B2", durationBeats: 0.5 },
        { note: "F2", durationBeats: 0.5 },
        { note: "B2", durationBeats: 0.5 },
        { note: "F2", durationBeats: 0.5 },
        { note: "B2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 1 },
        { note: "Bb2", durationBeats: 1 },
        { note: "E2", durationBeats: 2 },
      ],
    },
    {
      waveform: "sawtooth",
      volume: 0.09,
      notes: [
        { note: "E3", durationBeats: 8 },
        { note: "Bb3", durationBeats: 8 },
      ],
    },
  ],
};
