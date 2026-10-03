import { describe, expect, it } from "vitest";
import { WORLD_MAPS, WORLD_NPCS } from "../world/world";
import { MAP_PROPS, propFootprintTiles, propOverhangTiles } from "./map-props";
import { createTileMap, isWalkable } from "./tile-map";

describe("マップの飾り（木・家）", () => {
  it("飾りのある地図は、データに props が入り、足元のマスが通れない", () => {
    for (const [mapId, props] of Object.entries(MAP_PROPS)) {
      const data = WORLD_MAPS[mapId];
      expect(data, mapId).toBeDefined();
      expect(data.props?.length, mapId).toBe(props.length);
      const map = createTileMap(data);
      for (const prop of props) {
        for (const { x, y } of propFootprintTiles(prop)) {
          expect(isWalkable(map, x, y), `${mapId} (${x},${y})`).toBe(false);
        }
      }
    }
  });

  it("足元・足元の覆うマスは、地図の中に収まり、NPC・出入り口と重ならない", () => {
    for (const [mapId, props] of Object.entries(MAP_PROPS)) {
      const data = WORLD_MAPS[mapId];
      const npcs = WORLD_NPCS[mapId] ?? [];
      for (const prop of props) {
        const overhang = propOverhangTiles(prop.kind, data.tileHeight);
        const tiles = propFootprintTiles(prop);
        for (const { x, y } of tiles) {
          expect(x >= 0 && x < data.width && y >= 0 && y < data.height, `${mapId} ${prop.kind} (${x},${y}) が範囲外`).toBe(true);
        }
        // 絵がはみ出す上のマスにも、NPC・出入り口を置かない（絵の奥に隠れてしまう）
        const top = Math.min(...tiles.map((t) => t.y)) - overhang;
        const xs = tiles.map((t) => t.x);
        const area = (x: number, y: number): boolean => x >= Math.min(...xs) - (prop.kind === "tree" ? 1 : 0) && x <= Math.max(...xs) + (prop.kind === "tree" ? 1 : 0) && y >= top && y <= prop.tileY;
        for (const npc of npcs) {
          expect(area(npc.tileX, npc.tileY), `${mapId} の ${npc.id} が ${prop.kind}(${prop.tileX},${prop.tileY}) と重なる`).toBe(false);
        }
        for (const exit of data.exits ?? []) {
          expect(area(exit.tileX, exit.tileY), `${mapId} の出入り口(${exit.tileX},${exit.tileY}) が ${prop.kind} と重なる`).toBe(false);
        }
      }
    }
  });

  it("木は、地図の上から3マス以内に置かない（絵が画面の外に切れる）", () => {
    for (const [mapId, props] of Object.entries(MAP_PROPS)) {
      for (const prop of props.filter((p) => p.kind === "tree")) {
        expect(prop.tileY, `${mapId} の木 (${prop.tileX},${prop.tileY})`).toBeGreaterThanOrEqual(3);
      }
    }
  });
});
