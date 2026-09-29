import type { Score } from "./score";

/** 拍子。num=1小節の中の数（1〜32）、den=何分音符を1つと数えるか（1・2・4・8・16・32）。 */
export interface TimeSignature {
  num: number;
  den: number;
}

export const DENOMINATORS = [1, 2, 4, 8, 16, 32];

export function timeSignatureOf(score: Pick<Score, "timeSig">): TimeSignature {
  const t = score.timeSig;
  if (!t || !(t.num >= 1 && t.num <= 32) || !DENOMINATORS.includes(t.den)) return { num: 4, den: 4 };
  return { num: Math.round(t.num), den: t.den };
}

/** 1小節の長さ（4分音符を1拍とした拍の数）。例: 4/4→4、3/4→3、7/8→3.5、6/8→3。 */
export function barBeats(sig: TimeSignature): number {
  return (sig.num * 4) / sig.den;
}

/** 拍子の1つ分の長さ（4分音符を1拍とした拍の数）。例: 7/8→0.5。 */
export function unitBeats(sig: TimeSignature): number {
  return 4 / sig.den;
}

/** "7/8" のような文字を拍子にする。読めなければ null。 */
export function parseTimeSignature(text: string): TimeSignature | null {
  const m = /^\s*(\d{1,2})\s*\/\s*(\d{1,2})\s*$/.exec(text);
  if (!m) return null;
  const sig = { num: Number(m[1]), den: Number(m[2]) };
  return sig.num >= 1 && sig.num <= 32 && DENOMINATORS.includes(sig.den) ? sig : null;
}
