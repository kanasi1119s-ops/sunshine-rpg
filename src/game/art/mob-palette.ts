/**
 * 雑魚の敵の絵（64×64、`mob:*`）の色づけ。絵は色番号だけを持ち、地方ごとの色相で色を作る。
 * 暗→明の並びは、影を青紫寄り・光を黄寄りへ色相をずらしてある（`docs/design/pixel-art-notes.md` B）。
 * 値は tools/pixel-art/mobs.mjs の `previewPalette` と同じ（色番号: 0縁 1-5本体 6-8差し色 9目の白 10瞳 11影 12照り）。
 */
function hslToHex(h: number, s: number, l: number): string {
  const hue = ((h % 360) + 360) % 360;
  const sat = s / 100;
  const light = l / 100;
  const a = sat * Math.min(light, 1 - light);
  const f = (n: number): number => {
    const k = (n + hue / 30) % 12;
    return light - a * Math.max(-1, Math.min(k - 3, 9 - k, 1));
  };
  return "#" + [f(0), f(8), f(4)].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
}

/** #rrggbb の色相（0〜360）。無彩色は 0。 */
export function hueOfHex(hex: string): number {
  const m = /^#([0-9a-fA-F]{6})$/.exec(hex);
  if (!m) {
    return 0;
  }
  const v = parseInt(m[1], 16);
  const r = ((v >> 16) & 255) / 255;
  const g = ((v >> 8) & 255) / 255;
  const b = (v & 255) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  if (max === min) {
    return 0;
  }
  const d = max - min;
  const h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return Math.round(((h * 60) % 360 + 360) % 360);
}

const BODY: Array<[number, number, number]> = [[-24, 38, 13], [-14, 40, 24], [0, 42, 36], [8, 44, 50], [18, 46, 66]];
const ACCENT: Array<[number, number, number]> = [[-20, 60, 30], [10, 70, 50], [26, 80, 72]];

/** 色相から、雑魚の絵の13色のパレット（色番号順）を作る。 */
export function mobPalette(hue: number): string[] {
  return [
    hslToHex(hue - 30, 40, 6),
    ...BODY.map(([dh, s, l]) => hslToHex(hue + dh, s, l)),
    ...ACCENT.map(([dh, s, l]) => hslToHex(hue + 150 + dh, s, l)),
    "#f4f8ff",
    "#1a1030",
    hslToHex(hue - 30, 30, 10),
    "#ffffff",
  ];
}
