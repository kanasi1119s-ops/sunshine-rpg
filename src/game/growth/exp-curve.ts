/** レベルNに到達するために必要な累計経験値。 */
export function expRequiredForLevel(level: number): number {
  return Math.floor(20 * Math.pow(level, 2.5));
}

/** 累計経験値から、今何レベルかを求める。 */
export function levelForExp(exp: number): number {
  let level = 1;
  while (expRequiredForLevel(level + 1) <= exp) {
    level++;
  }
  return level;
}

/** 次のレベルまでに、あと何経験値必要か。 */
export function expToNextLevel(exp: number): number {
  const level = levelForExp(exp);
  return expRequiredForLevel(level + 1) - exp;
}
