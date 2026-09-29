/** 作曲ソフトの和音入力: 根音から、和音の構成音（半音の数）を作る。 */
export const CHORD_SHAPES: [string, string, number[]][] = [
  ["none", "単音", [0]],
  ["major", "メジャー（明るい）", [0, 4, 7]],
  ["minor", "マイナー（暗い）", [0, 3, 7]],
  ["power", "パワーコード（5度）", [0, 7, 12]],
  ["sus4", "サスフォー", [0, 5, 7]],
  ["seventh", "セブンス", [0, 4, 7, 10]],
  ["minor7", "マイナーセブンス", [0, 3, 7, 10]],
  ["major7", "メジャーセブンス", [0, 4, 7, 11]],
  ["dim", "ディミニッシュ", [0, 3, 6]],
  ["add9", "アドナインス", [0, 4, 7, 14]],
];

export function chordIntervals(shape: string): number[] {
  return CHORD_SHAPES.find(([k]) => k === shape)?.[2] ?? [0];
}
