import type { Instrument, Waveform } from "./score";

/**
 * 楽器の音色 → GM（General MIDI）の楽器番号。録音音源（サウンドフォント）で鳴らすときに使う。
 * ここに書いた番号だけを、`tools/soundfont/trim-soundfont.mjs` が元のサウンドフォントから切り出す（`GM_PROGRAMS`）。
 */
export const GM_PROGRAM: Partial<Record<Instrument, number>> = {
  bass: 33, // フィンガーベース
  slap: 36, // スラップベース
  sub808: 38, // シンセベース
  guitar: 27, // クリーンギター
  echoGuitar: 27,
  crunch: 29, // オーバードライブ
  distGuitar: 30, // ディストーション
  leadGuitar: 30,
  keys: 4, // エレピ
  piano: 0,
  harpsichord: 6,
  strings: 48,
  pad: 52, // 合唱（電子的なパッドではなく、生の声に近い響き）
  choir: 52, // 合唱
  brass: 61, // ブラスセクション
  bell: 9, // グロッケン
  chime: 11, // ビブラフォン
  lead: 73, // フルート（電子的なリードではなく、自然な旋律楽器。電子音楽では下のSYNTH_LEADに切り替える）
  cowbell: 9,
  wind: 122, // 海岸（風・波の音）
  stream: 122,
  rain: 96, // FX 雨
  bird: 123, // 鳥の声
  crickets: 123,
};
export const GM_DEFAULT_BY_WAVE: Record<Waveform, number> = { square: 80, triangle: 4, sawtooth: 80, sine: 89 };

/** 効果音（`se-library.ts`）で使うGMの楽器番号。 */
export const SE_GM_PROGRAMS = [8, 9, 11, 12, 14, 33, 44, 45, 46, 47, 48, 52, 53, 55, 56, 61, 89, 91, 98, 100, 101, 115, 116, 119, 120, 122, 126];

/** 重ねて鳴らす楽器（実際の演奏に近づけるため）。例: エレピにピアノを薄く重ねる。 */
export const GM_LAYER: Partial<Record<Instrument, { program: number; gain: number }>> = {
  keys: { program: 0, gain: 0.5 },
  pad: { program: 48, gain: 0.35 },
  bass: { program: 32, gain: 0.3 },
};

/** ドラムセットの選び方（曲調ごと）。GMのドラムキット番号: 0=標準、8=ルーム、16=パワー、24=電子、25=TR-808、32=ジャズ、48=オーケストラ。 */
export const DRUM_KITS = [0, 8, 16, 24, 25, 32, 48];

/** 打楽器 → GMドラムのノート番号。 */
export const GM_DRUM_NOTE: Partial<Record<Instrument, number>> = { kick: 36, snare: 38, hihat: 42, crash: 49, tom: 47 };

/** 使うGMの楽器番号の一覧（サウンドフォントを切り出すときの指定に使う）。 */
/** 電子音楽（エレクトリック・フォンク・プログレッシブなど）では、リードとパッドを電子的な音色にする（楽器番号）。 */
export const SYNTH_LEAD = 80;
export const SYNTH_PAD = 89;
/** メタル調では、リードの声部にオーバードライブのギターを使う。 */
export const METAL_LEAD = 29;

/** 実楽器版で使うGMの楽器番号（バイオリン・チェロ・オーボエ・サックス・アコースティックギターなど）。 */
export const REAL_GM_PROGRAMS = [24, 34, 40, 42, 60, 65, 68, 71, 73];

export const USED_GM_PROGRAMS: number[] = [
  ...new Set([...Object.values(GM_PROGRAM), ...Object.values(GM_DEFAULT_BY_WAVE), ...Object.values(GM_LAYER).map((l) => l.program), ...SE_GM_PROGRAMS, SYNTH_LEAD, SYNTH_PAD, METAL_LEAD, ...REAL_GM_PROGRAMS]),
].sort((a, b) => a - b);
