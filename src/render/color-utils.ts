/** #rrggbb形式の色を、指定した割合だけ明るく（正）／暗く（負）する。 */
export function shadeColor(hex: string, amount: number): string {
  const match = /^#([0-9a-fA-F]{6})$/.exec(hex);
  if (!match) {
    return hex;
  }
  const value = parseInt(match[1], 16);
  const channel = (shift: number): number => {
    const c = (value >> shift) & 0xff;
    const adjusted = amount >= 0 ? c + (255 - c) * amount : c + c * amount;
    return Math.max(0, Math.min(255, Math.round(adjusted)));
  };
  const r = channel(16);
  const g = channel(8);
  const b = channel(0);
  return `#${((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1)}`;
}

/**
 * (x, y)から決まる整数の疑似乱数。フレームをまたいでも同じ結果になるよう、
 * 時刻やMath.random()は使わない（毎回同じ模様になるようにするため）。
 */
export function hashCell(x: number, y: number): number {
  let h = (x * 374761393 + y * 668265263) | 0;
  h = (h ^ (h >>> 13)) * 1274126177;
  h = h ^ (h >>> 16);
  return h >>> 0;
}
