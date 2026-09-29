import type { Instrument, Waveform } from "./score";

/**
 * 楽器の音色 → GM（General MIDI）の楽器番号。録音音源（サウンドフォント）で鳴らすときに使う。
 * ここに書いた番号だけを、`tools/soundfont/trim-soundfont.mjs` が元のサウンドフォントから切り出す（`GM_PROGRAMS`）。
 */
export const GM_PROGRAM: Partial<Record<Instrument, number>> = {
  bass: 33, // フィンガーベース
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
  pad: 89, // ウォームパッド
  bell: 9, // グロッケン
  chime: 11, // ビブラフォン
  lead: 80, // 矩形波リード
  cowbell: 9,
  wind: 122, // 海岸（風・波の音）
  stream: 122,
  rain: 96, // FX 雨
  bird: 123, // 鳥の声
  crickets: 123,
};
export const GM_DEFAULT_BY_WAVE: Record<Waveform, number> = { square: 80, triangle: 4, sawtooth: 80, sine: 89 };

/** 打楽器 → GMドラムのノート番号。 */
export const GM_DRUM_NOTE: Partial<Record<Instrument, number>> = { kick: 36, snare: 38, hihat: 42, crash: 49 };

/** 使うGMの楽器番号の一覧（サウンドフォントを切り出すときの指定に使う）。 */
export const USED_GM_PROGRAMS: number[] = [...new Set([...Object.values(GM_PROGRAM), ...Object.values(GM_DEFAULT_BY_WAVE)])].sort((a, b) => a - b);
