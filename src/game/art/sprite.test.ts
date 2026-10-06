import { describe, expect, it } from "vitest";
import { decodeSprite, type SpriteData } from "./sprite";
import { SPRITE_DATA } from "./sprite-data.generated";

/** 町・村・お城の印は64×64（2026-10-05、6回目）。 */
const TOWN_ICONS_64 = new Set(["port", "village", "lake", "mine", "castle", "tents", "temple", "snowtown", "sky", "palace", "village-mist", "tents-grass"].map((n) => `prop:icon-${n}`));

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

describe("decodeSprite（色が27色以上の形式）", () => {
  it("「~」で始まる「色番号:続く数」の並びを読める（透明は -1）", () => {
    const data: SpriteData = { size: 2, palette: ["#000000", "#111111"], rle: "~-1:1,30:2,1:1" };
    expect(Array.from(decodeSprite(data))).toEqual([-1, 30, 30, 1]);
  });
});

describe("書き出されたドット絵データ（sprite-data.generated.ts）", () => {
  const keys = Object.keys(SPRITE_DATA);

  it("地形・ボス・登場人物が入っている", () => {
    for (const key of ["terrain:grass-a", "terrain:water", "boss:mugikano-yugami", "boss:garasuko-yugami", "boss:tetsukusari-yugami", "boss:sanone-yugami", "boss:kiri-yugami", "boss:shimohara-yugami", "boss:fushima-yugami", "boss:toushin-yugami", "boss:kyotoukyu-yugami", "boss:god-1", "boss:god-8", "boss:tower2-guard", "boss:tower3-guard", "boss:kanou3-guard", "boss:deep3-yugami", "boss:zenkan", "char:ユーリ", "char:オルカ", "mob:bat", "mob:beetle", "mob:shard", "mob:drop", "mob:ghost", "mob:rat", "mob:scorpion", "mob:eye", "prop:tree", "prop:house", "prop:house-blue", "prop:house-green", "prop:rock", "prop:bush", "prop:manor", "prop:manor-blue", "prop:manor-green"]) {
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

  it("地形は128×128、雑魚の敵は64×64、飾りは48・80（教会は176・中の1枚絵は208）、登場人物は104×104、ボスは256×256、コスモリングライトのユーリは50（砲台は9）", () => {
    for (const key of keys) {
      const expected = key === "cosmo:pod" ? 9 : key.startsWith("cosmo:") ? 50 : key.startsWith("terrain:") ? 128 : key.startsWith("mob:") ? 64 : key.startsWith("prop:manor") ? 80 : key.startsWith("icon:") ? 16 : key.startsWith("prop:house") || key === "prop:jail-bars" ? 64 : key === "prop:icon-spire" ? 112 : key === "prop:icon-core-spire" ? 256 : TOWN_ICONS_64.has(key) ? 64 : key === "prop:church" ? 176 : key === "prop:tree" ? 80 : key === "prop:church-interior" ? 224 : key.startsWith("prop:") ? 48 : key.startsWith("char:") ? 104 : key.startsWith("enemy:") ? 96 : 256;
      expect(SPRITE_DATA[key].size, key).toBe(expected);
    }
  });

  it("パレットはすべて #rrggbb 形式（影などの透ける色は #rrggbbaa）", () => {
    for (const key of keys) {
      for (const color of SPRITE_DATA[key].palette) {
        expect(color).toMatch(/^#[0-9a-f]{6}([0-9a-f]{2})?$/i);
      }
    }
  });
});
