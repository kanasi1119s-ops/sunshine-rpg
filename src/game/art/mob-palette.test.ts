import { describe, expect, it } from "vitest";
import { hueOfHex, mobPalette } from "./mob-palette";
import { SPRITE_DATA } from "./sprite-data.generated";
import { decodeSprite } from "./sprite";

describe("雑魚の敵の色づけ", () => {
  it("パレットは13色で、すべて #rrggbb", () => {
    const palette = mobPalette(150);
    expect(palette).toHaveLength(13);
    for (const hex of palette) {
      expect(hex).toMatch(/^#[0-9a-f]{6}$/);
    }
  });

  it("本体の階調は暗→明の順に明るくなる", () => {
    const lightness = (hex: string): number => {
      const v = parseInt(hex.slice(1), 16);
      return (((v >> 16) & 255) + ((v >> 8) & 255) + (v & 255)) / 3;
    };
    const body = mobPalette(200).slice(1, 6).map(lightness);
    expect([...body].sort((a, b) => a - b)).toEqual(body);
  });

  it("色相を取り出せる（色の輪の上で近い値）", () => {
    expect(hueOfHex("#ff0000")).toBe(0);
    expect(hueOfHex("#00ff00")).toBe(120);
    expect(hueOfHex("#0000ff")).toBe(240);
    expect(hueOfHex("#808080")).toBe(0);
  });

  it("8つの形の絵は、色番号がどれも13色の範囲内", () => {
    for (const key of ["mob:bat", "mob:beetle", "mob:shard", "mob:drop", "mob:ghost", "mob:rat", "mob:scorpion", "mob:eye"]) {
      const cells = decodeSprite(SPRITE_DATA[key]);
      expect(Math.max(...Array.from(cells)), key).toBeLessThan(13);
    }
  });
});
