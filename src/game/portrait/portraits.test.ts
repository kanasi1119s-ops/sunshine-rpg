import { describe, expect, it } from "vitest";
import {
  buildPortraitRows,
  colorForCell,
  PORTRAIT_GRID_HEIGHT,
  PORTRAIT_GRID_WIDTH,
  PORTRAITS,
  type PortraitSpec,
} from "./portraits";

const VALID_CELLS = new Set([".", "H", "S", "E", "A"]);

describe("buildPortraitRows", () => {
  it("すべての髪型で、行数・列数が固定サイズになる", () => {
    const styles: PortraitSpec["hairStyle"][] = ["short", "long", "twin", "slick"];
    for (const hairStyle of styles) {
      const rows = buildPortraitRows({
        skin: "#000",
        hair: "#000",
        eyes: "#000",
        accent: "#000",
        hairStyle,
        accessory: "none",
      });
      expect(rows).toHaveLength(PORTRAIT_GRID_HEIGHT);
      for (const row of rows) {
        expect(row).toHaveLength(PORTRAIT_GRID_WIDTH);
        for (const cell of row) {
          expect(VALID_CELLS.has(cell), `不明なドット記号: "${cell}"`).toBe(true);
        }
      }
    }
  });

  it("左右対称になる（列cと列(幅-1-c)が同じ記号）", () => {
    const styles: PortraitSpec["hairStyle"][] = ["short", "long", "twin", "slick"];
    const accessories: PortraitSpec["accessory"][] = ["none", "headband", "circlet", "glasses"];
    for (const hairStyle of styles) {
      for (const accessory of accessories) {
        const rows = buildPortraitRows({
          skin: "#000",
          hair: "#000",
          eyes: "#000",
          accent: "#000",
          hairStyle,
          accessory,
        });
        for (const row of rows) {
          for (let col = 0; col < PORTRAIT_GRID_WIDTH; col++) {
            const mirrored = row[PORTRAIT_GRID_WIDTH - 1 - col];
            expect(row[col], `${hairStyle}/${accessory}: "${row}" が左右非対称`).toBe(mirrored);
          }
        }
      }
    }
  });

  it("最低1つは目（E）のドットを含む", () => {
    const rows = buildPortraitRows({
      skin: "#000",
      hair: "#000",
      eyes: "#000",
      accent: "#000",
      hairStyle: "short",
      accessory: "none",
    });
    expect(rows.some((row) => row.includes("E"))).toBe(true);
  });
});

describe("colorForCell", () => {
  const spec: PortraitSpec = {
    skin: "#111",
    hair: "#222",
    eyes: "#333",
    accent: "#444",
    hairStyle: "short",
    accessory: "none",
  };

  it("記号ごとに、そのキャラクターの色を返す", () => {
    expect(colorForCell(spec, "S")).toBe("#111");
    expect(colorForCell(spec, "H")).toBe("#222");
    expect(colorForCell(spec, "E")).toBe("#333");
    expect(colorForCell(spec, "A")).toBe("#444");
  });

  it("'.'は何も描かない（null）", () => {
    expect(colorForCell(spec, ".")).toBeNull();
  });
});

describe("PORTRAITS", () => {
  const NAMED_CAST = ["ユーリ", "レト", "ミナ", "ガイド", "オルカ", "アヤメ", "ドルン", "カセン", "エドレア"];

  it("docs/story/characters.mdの主要キャラクター全員が登録されている", () => {
    for (const name of NAMED_CAST) {
      expect(PORTRAITS[name], `${name}の顔グラフィックが登録されていない`).toBeDefined();
    }
  });

  it("登録されている顔グラフィックは、すべて有効なドットの並びを作れる", () => {
    for (const [name, spec] of Object.entries(PORTRAITS)) {
      const rows = buildPortraitRows(spec);
      expect(rows, name).toHaveLength(PORTRAIT_GRID_HEIGHT);
    }
  });
});
