import { describe, expect, it } from "vitest";
import { WORLD_MAPS, WORLD_NPCS } from "./world";
import { CHAPTER0_START } from "./chapter0-world";
import { createTileMap, isWalkable } from "../map/tile-map";
import type { EventCommand } from "../event/types";

/**
 * 到達可能性のチェック: どの地図でも、NPC（人・調べる場所・仕掛け）のすぐ隣に、
 * 「入ってくる場所（出入り口の行き先・警告の行き先・開始地点）」から歩いてたどり着ける。
 * 通せんぼをするNPC（封印の扉など）は、フラグで通れるようになる仕掛けなので、NPCの位置は通れるものとして数える。
 */
function collectWarps(commands: EventCommand[], out: { mapId: string; tileX: number; tileY: number }[]): void {
  for (const c of commands) {
    if (c.type === "warp") {
      out.push({ mapId: c.mapId, tileX: c.tileX, tileY: c.tileY });
    } else if (c.type === "choice") {
      c.options.forEach((o) => collectWarps(o.commands, out));
    } else if (c.type === "if") {
      collectWarps(c.then, out);
      collectWarps(c.else ?? [], out);
    }
  }
}

describe("到達可能性", () => {
  const seeds: Record<string, { x: number; y: number }[]> = {};
  const addSeed = (mapId: string, x: number, y: number) => {
    (seeds[mapId] ??= []).push({ x, y });
  };
  addSeed(CHAPTER0_START.mapId, CHAPTER0_START.tileX, CHAPTER0_START.tileY);
  for (const data of Object.values(WORLD_MAPS)) {
    for (const exit of data.exits ?? []) {
      addSeed(exit.targetMapId, exit.targetTileX, exit.targetTileY);
    }
  }
  const warps: { mapId: string; tileX: number; tileY: number }[] = [];
  for (const npcs of Object.values(WORLD_NPCS)) {
    for (const npc of npcs) {
      collectWarps(npc.commands, warps);
    }
  }
  for (const w of warps) {
    addSeed(w.mapId, w.tileX, w.tileY);
  }

  function reachable(mapId: string): Set<string> {
    const map = createTileMap(WORLD_MAPS[mapId]);
    const npcTiles = new Set((WORLD_NPCS[mapId] ?? []).map((n) => `${n.tileX},${n.tileY}`));
    const passable = (x: number, y: number) => isWalkable(map, x, y) || npcTiles.has(`${x},${y}`);
    const seen = new Set<string>();
    const queue: { x: number; y: number }[] = [...(seeds[mapId] ?? [])];
    for (const s of queue) {
      seen.add(`${s.x},${s.y}`);
    }
    while (queue.length > 0) {
      const { x, y } = queue.shift()!;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = x + dx;
        const ny = y + dy;
        if (passable(nx, ny) && !seen.has(`${nx},${ny}`)) {
          seen.add(`${nx},${ny}`);
          queue.push({ x: nx, y: ny });
        }
      }
    }
    return seen;
  }

  it("すべての地図に、入ってくる場所がある（どこからも入れない地図がない）", () => {
    const orphans = Object.keys(WORLD_MAPS).filter((mapId) => !(seeds[mapId]?.length));
    expect(orphans).toEqual([]);
  });

  it("すべてのNPCは、歩ける場所にあり、出入り口・到着地点の上に立っていない", () => {
    const bad: string[] = [];
    for (const [mapId, npcs] of Object.entries(WORLD_NPCS)) {
      const data = WORLD_MAPS[mapId];
      const map = createTileMap(data);
      const arrivals = Object.values(WORLD_MAPS).flatMap((m) => m.exits ?? []).filter((e) => e.targetMapId === mapId);
      for (const npc of npcs) {
        if (!isWalkable(map, npc.tileX, npc.tileY)) {
          bad.push(`${mapId} の ${npc.id} が通行不可タイル`);
        }
        if ((data.exits ?? []).some((e) => e.tileX === npc.tileX && e.tileY === npc.tileY)) {
          bad.push(`${mapId} の ${npc.id} が出入り口の上`);
        }
        if (arrivals.some((e) => e.targetTileX === npc.tileX && e.targetTileY === npc.tileY)) {
          bad.push(`${mapId} の ${npc.id} が到着地点の上`);
        }
      }
    }
    expect(bad).toEqual([]);
  });

  it("すべてのNPCの隣に、歩いてたどり着ける", () => {
    const bad: string[] = [];
    for (const [mapId, npcs] of Object.entries(WORLD_NPCS)) {
      const seen = reachable(mapId);
      const map = createTileMap(WORLD_MAPS[mapId]);
      for (const npc of npcs) {
        const neighbors = [[1, 0], [-1, 0], [0, 1], [0, -1]].map(([dx, dy]) => [npc.tileX + dx, npc.tileY + dy]);
        const ok = neighbors.some(([x, y]) => isWalkable(map, x, y) && seen.has(`${x},${y}`));
        if (!ok) {
          bad.push(`${mapId} の ${npc.id}（${npc.tileX},${npc.tileY}）にたどり着けない`);
        }
      }
    }
    expect(bad).toEqual([]);
  });

  it("すべての出入り口の隣に、歩いてたどり着ける（地図の出口が閉じ込められていない）", () => {
    const bad: string[] = [];
    for (const [mapId, data] of Object.entries(WORLD_MAPS)) {
      const seen = reachable(mapId);
      for (const exit of data.exits ?? []) {
        const map = createTileMap(data);
        const ok = [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]].some(([dx, dy]) => {
          const x = exit.tileX + dx;
          const y = exit.tileY + dy;
          return (isWalkable(map, x, y) || (x === exit.tileX && y === exit.tileY)) && seen.has(`${x},${y}`);
        });
        if (!ok) {
          bad.push(`${mapId} の出入り口（${exit.tileX},${exit.tileY}）にたどり着けない`);
        }
      }
    }
    expect(bad).toEqual([]);
  });
});
