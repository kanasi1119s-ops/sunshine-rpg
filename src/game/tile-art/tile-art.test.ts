import { describe, expect, it } from "vitest";
import { buildTileArtCells, TILE_ART, TILE_ART_SIZE, TILE_VARIANTS, type TileArtSpec } from "./tile-art";

describe("buildTileArtCells", () => {
  it("すべてのパターンで、有効な#rrggbb形式の色だけを返す", () => {
    for (const spec of Object.values(TILE_ART)) {
      for (const cell of buildTileArtCells(spec)) {
        expect(cell.color).toMatch(/^#[0-9a-f]{6}$/i);
        expect(cell.row).toBeGreaterThanOrEqual(0);
        expect(cell.row).toBeLessThan(TILE_ART_SIZE);
        expect(cell.col).toBeGreaterThanOrEqual(0);
        expect(cell.col).toBeLessThan(TILE_ART_SIZE);
      }
    }
  });

  it("同じ仕様なら毎回同じ結果になる（時刻・乱数に依存しない）", () => {
    for (const spec of Object.values(TILE_ART)) {
      expect(buildTileArtCells(spec)).toEqual(buildTileArtCells(spec));
    }
  });

  it("木の樹冠は円形で、四隅は描かない（矩形べた塗りにならない）", () => {
    const cells = buildTileArtCells(TILE_ART.treeCanopy);
    const hasCorner = cells.some((c) => (c.row === 0 || c.row === TILE_ART_SIZE - 1) && (c.col === 0 || c.col === TILE_ART_SIZE - 1));
    expect(hasCorner).toBe(false);
    expect(cells.length).toBeGreaterThan(0);
  });

  it("草・水・道は、タイル全体を埋める（隙間なく描ける地形）", () => {
    const totalCells = TILE_ART_SIZE * TILE_ART_SIZE;
    for (const key of ["grass", "water", "path"] as const) {
      expect(buildTileArtCells(TILE_ART[key])).toHaveLength(totalCells);
    }
  });

  it("複数の色を使う（単色べた塗りにならない）", () => {
    for (const spec of Object.values(TILE_ART)) {
      const colors = new Set(buildTileArtCells(spec).map((c) => c.color));
      expect(colors.size).toBeGreaterThan(1);
    }
  });

  it("未知のパターン名を渡しても例外にならない（防御的）", () => {
    const spec = { base: "#123456", accentLight: "#234567", accentDark: "#012345", pattern: "grass" } as TileArtSpec;
    expect(() => buildTileArtCells(spec)).not.toThrow();
  });
});

describe("見た目の揺らぎ（variant）", () => {
  it("草・水・道は、揺らぎごとに違う模様になり、並べても単調にならない", () => {
    for (const key of ["grass", "water", "path"] as const) {
      const patterns = new Set<string>();
      for (let variant = 0; variant < TILE_VARIANTS; variant++) {
        patterns.add(JSON.stringify(buildTileArtCells(TILE_ART[key], variant)));
      }
      expect(patterns.size, `${key} の揺らぎが同じ`).toBeGreaterThan(1);
    }
  });

  it("草・水は5階調前後の色を使う（SFC後期風の陰影）", () => {
    for (const key of ["grass", "water"] as const) {
      const colors = new Set(buildTileArtCells(TILE_ART[key]).map((c) => c.color));
      expect(colors.size, `${key} の色数`).toBeGreaterThanOrEqual(4);
    }
  });
});

