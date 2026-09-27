/**
 * シード指定できる擬似乱数生成器（mulberry32）。
 * 同じシードなら同じ結果になるため、戦闘の自動シミュレーションや
 * 自動テストで結果を再現できる（不具合の再現にも使う）。
 */
export function createRng(seed: number): () => number {
  let state = seed >>> 0;
  return function random(): number {
    state |= 0;
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
