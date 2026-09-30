import { describe, expect, it } from "vitest";
import { MAP_TILE_ART } from "./map-tile-art";
import { buildTileArtCells, TILE_ART, TILE_ART_SIZE, TILE_VARIANTS, tintedSpec, type TilePatternKind } from "./tile-art";
import { WORLD_MAPS } from "../world/world";

const NEW_PATTERNS: TilePatternKind[] = ["flagstone", "brick", "sand", "snow", "plank", "cloud", "roof", "crate", "pillar", "machine", "pipe", "carpet", "crystal", "void"];

describe("タイルの模様（石畳・壁・砂・雪・板張り・雲）", () => {
  it("どの模様も、16×16のタイルを埋め、色数は5階調以内で、揺らぎの種類ごとに絵が違う", () => {
    for (const pattern of NEW_PATTERNS) {
      const spec = tintedSpec(pattern, "#8a8578");
      const variants = Array.from({ length: TILE_VARIANTS }, (_, v) => buildTileArtCells(spec, v));
      for (const cells of variants) {
        expect(cells.length, pattern).toBe(TILE_ART_SIZE * TILE_ART_SIZE);
        expect(new Set(cells.map((c) => c.color)).size, pattern).toBeLessThanOrEqual(5);
      }
      const json = variants.map((c) => JSON.stringify(c));
      expect(new Set(json).size, `${pattern} の揺らぎが同じ`).toBeGreaterThan(1);
    }
  });

  it("模様の指定は、実在する地図の、実在するタイルIDに対するもの。指定の種類は、登録済みの模様かtint", () => {
    for (const [mapId, art] of Object.entries(MAP_TILE_ART)) {
      const data = WORLD_MAPS[mapId];
      expect(data, `${mapId} の地図が無い`).toBeDefined();
      for (const [id, kind] of Object.entries(art)) {
        expect(data.tileColors[Number(id)], `${mapId} のタイル${id}が無い`).toBeDefined();
        if (kind.startsWith("tint:")) {
          expect(NEW_PATTERNS).toContain(kind.slice(5));
        } else {
          expect(TILE_ART[kind], `${mapId} の ${kind}`).toBeDefined();
        }
      }
    }
  });

  it("地図に、模様の指定が反映されている", () => {
    expect(WORLD_MAPS["kiri-town"].tileArt?.[1]).toBe("tint:flagstone");
    expect(WORLD_MAPS["deep-1"].tileArt?.[2]).toBe("tint:brick");
  });
});
