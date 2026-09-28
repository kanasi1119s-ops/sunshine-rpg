import type { Score } from "./score";

/**
 * 序章（灯里）のBGM。`docs/sound/tracks.md`の方針
 * （16bit風チップチューン×現代的な音づくり。全パートの合計拍数が
 * 揃うように作り、ループのつなぎ目で不自然に途切れないようにしている）
 * に沿ってオリジナルで作曲した。既存曲のメロディ・コード進行は使っていない。
 */

/**
 * タイトル・灯りのテーマ（ライトモチーフ）。
 * 現代的な工夫: 単旋律のパートを複数重ね、9th・7thの色づけの音（テンション）と
 * 低音のドローンを別パートとして重ねることで、和音がなくても厚みのある響きにしている。
 */
export const CHAPTER0_TITLE_THEME: Score = {
  tempoBpm: 92,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.25,
      notes: [
        { note: "E4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "D4", durationBeats: 1 },
        { note: "C4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "F4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "C5", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "D4", durationBeats: 2 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.16,
      notes: [
        { note: "C3", durationBeats: 4 },
        { note: "F3", durationBeats: 4 },
        { note: "G3", durationBeats: 4 },
        { note: "C3", durationBeats: 4 },
      ],
    },
    {
      // 9th・7th のテンションだけを別パートで持たせる（Cmaj9→Fmaj7→G9→Cmaj9）。
      waveform: "sine",
      volume: 0.1,
      notes: [
        { note: "D4", durationBeats: 4 },
        { note: "E4", durationBeats: 4 },
        { note: "A4", durationBeats: 4 },
        { note: "D4", durationBeats: 4 },
      ],
    },
    {
      // 広がりを出すための低いドローン。
      waveform: "sine",
      volume: 0.05,
      notes: [{ note: "C2", durationBeats: 16 }],
    },
  ],
};

/**
 * 灯里の町（明るい港町）。
 * 現代的な工夫: タイトルテーマの旋律の動き（E→G→A→G…の跳躍の形）を
 * 調とリズムを変えて再利用し、ライトモチーフの変奏になるようにしている。
 */
export const CHAPTER0_TOWN_THEME: Score = {
  tempoBpm: 118,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.26,
      notes: [
        { note: "G4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 1 },
        { note: "D5", durationBeats: 1 },
        { note: "B4", durationBeats: 1 },
        { note: "A4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "D4", durationBeats: 1 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 1 },
        { note: "E5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "D4", durationBeats: 1 },
        { note: "G3", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.15,
      notes: [
        { note: "G3", durationBeats: 4 },
        { note: "C3", durationBeats: 4 },
        { note: "D3", durationBeats: 4 },
        { note: "G3", durationBeats: 4 },
      ],
    },
    {
      // Gmaj9→Cmaj7→D9→Gmaj9 のテンションだけを重ねる。
      waveform: "sine",
      volume: 0.1,
      notes: [
        { note: "A4", durationBeats: 4 },
        { note: "B4", durationBeats: 4 },
        { note: "E5", durationBeats: 4 },
        { note: "A4", durationBeats: 4 },
      ],
    },
    {
      waveform: "sine",
      volume: 0.06,
      notes: [{ note: "G2", durationBeats: 16 }],
    },
  ],
};

/**
 * 町外れ・歪みの発生地点（調査・緊張のテーマ）。
 * 現代的な工夫: ドローンに対してトライトーン（三全音）でぶつかる音を
 * 重ね、静かながら落ち着かない響きにしている（roles.md 3-7の
 * 「不安定な響きの和音・音のぶつかり」を静かな場面向けに弱めに適用）。
 */
export const CHAPTER0_OUTSKIRTS_THEME: Score = {
  tempoBpm: 84,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.22,
      notes: [
        { note: "D4", durationBeats: 1 },
        { note: "R", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "E4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "C4", durationBeats: 1 },
        { note: "R", durationBeats: 2 },
        { note: "D4", durationBeats: 1 },
        { note: "F4", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "F4", durationBeats: 1 },
        { note: "D4", durationBeats: 2 },
      ],
    },
    {
      waveform: "sine",
      volume: 0.1,
      notes: [{ note: "D2", durationBeats: 16 }],
    },
    {
      // ドローン（D2）とトライトーンでぶつかるAbを重ねる。
      waveform: "sawtooth",
      volume: 0.07,
      notes: [
        { note: "Ab3", durationBeats: 8 },
        { note: "A3", durationBeats: 8 },
      ],
    },
  ],
};

/**
 * 通常戦闘（疾走感重視）。
 * 現代的な工夫というよりも、方針どおり「速いテンポ・細かい刻み・
 * 前のめりなリズム」を徹底したチップチューン然としたアップテンポ曲。
 */
export const CHAPTER0_BATTLE_THEME: Score = {
  tempoBpm: 168,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.28,
      notes: [
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 1 },
        { note: "B4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.2,
      notes: [
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "C2", durationBeats: 1 },
        { note: "C2", durationBeats: 1 },
        { note: "C2", durationBeats: 1 },
        { note: "C2", durationBeats: 1 },
        { note: "D2", durationBeats: 1 },
        { note: "D2", durationBeats: 1 },
        { note: "D2", durationBeats: 1 },
        { note: "D2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
        { note: "E2", durationBeats: 1 },
      ],
    },
    {
      waveform: "sawtooth",
      volume: 0.12,
      notes: [
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "C3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "C3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "C3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "C3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
      ],
    },
  ],
};

/**
 * ボス戦「灯里の歪み」。
 * 現代的な工夫: 通常戦闘よりもさらに前のめりにしつつ、根音とトライトーンの
 * 低音を交互に鳴らして不安定さ（歪みの異様さ）を強めている
 * （roles.md 3-7の「不協和音」を戦闘の緊迫感の演出に応用）。
 */
export const CHAPTER0_BOSS_THEME: Score = {
  tempoBpm: 150,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.3,
      notes: [
        { note: "D4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "C4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "A4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 1 },
        { note: "D4", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.22,
      notes: [
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "E2", durationBeats: 0.5 },
        { note: "Bb2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D2", durationBeats: 1 },
        { note: "Ab2", durationBeats: 1 },
        { note: "D2", durationBeats: 2 },
      ],
    },
    {
      waveform: "sawtooth",
      volume: 0.09,
      notes: [
        { note: "D3", durationBeats: 8 },
        { note: "Ab3", durationBeats: 8 },
      ],
    },
  ],
};
