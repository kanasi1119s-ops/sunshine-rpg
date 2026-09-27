/** 文字送り：経過時間から、いま何文字目まで表示するかを計算する。 */
export function computeVisibleChars(
  text: string,
  elapsedMs: number,
  charsPerSecond = 30,
): number {
  const chars = Math.floor((elapsedMs / 1000) * charsPerSecond);
  return Math.min(text.length, Math.max(0, chars));
}
