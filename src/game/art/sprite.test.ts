import { describe, expect, it } from "vitest";
import { decodeSprite, type SpriteData } from "./sprite";
import { SPRITE_DATA } from "./sprite-data.generated";

describe("decodeSprite", () => {
  it("色番号（A〜Z）と透明（_）、続く個数（36進数）を正しく読む", () => {
    const data: SpriteData = { size: 2, palette: ["#000000", "#ffffff"], rle: "A_B2" };
    expect(Array.from(decodeSprite(data))).toEqual([0, -1, 1, 1]);
  });

  it("個数が10以上（36進数の小文字を含む）でも正しく読める", () => {
    const data: SpriteData = { size: 4, palette: ["#000000"], rle: "Ag" };   // g = 16
    expect(Array.from(decodeSprite(data)).every((k) => k === 0)).toBe(true);
  });
});

describe("書き出されたドット絵データ（sprite-data.generated.ts）", () => {
  const keys = Object.keys(SPRITE_DATA);

  it("地形・ボス・登場人物が入っている", () => {
    for (const key of ["terrain:grass-a", "terrain:water", "boss:mugikano-yugami", "boss:garasuko-yugami", "boss:tetsukusari-yugami", "boss:sanone-yugami", "boss:kiri-yugami", "boss:shimohara-yugami", "char:ユーリ", "char:オルカ"]) {
      expect(keys, key).toContain(key);
    }
  });

  it("すべて、size×size のマスに読み切れて、使う色番号がパレットの範囲内", () => {
    for (const key of keys) {
      const data = SPRITE_DATA[key];
      const cells = decodeSprite(data);
      expect(cells.length).toBe(data.size * data.size);
      const max = Math.max(...Array.from(cells));
      expect(max, `${key} の色番号`).toBeLessThan(data.palette.length);
      expect(cells.filter((k) => k >= 0).length, `${key} が空`).toBeGreaterThan(data.size * 2);
    }
  });

  it("地形は128×128、ボスと登場人物は256×256", () => {
    for (const key of keys) {
      const expected = key.startsWith("terrain:") ? 128 : 256;
      expect(SPRITE_DATA[key].size, key).toBe(expected);
    }
  });

  it("パレットはすべて #rrggbb 形式", () => {
    for (const key of keys) {
      for (const color of SPRITE_DATA[key].palette) {
        expect(color).toMatch(/^#[0-9a-f]{6}$/i);
      }
    }
  });
});
