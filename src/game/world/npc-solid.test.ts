import { describe, expect, it } from "vitest";
import { WORLD_MAPS, WORLD_NPCS } from "./world";

/** 床のつながりを数える（入れた「障害物」のマスは通れない）。 */
function components(w: number, h: number, blocked: boolean[]): number[] {
  const comp = new Array<number>(w * h).fill(-1);
  let n = 0;
  for (let s = 0; s < w * h; s++) {
    if (blocked[s] || comp[s] !== -1) continue;
    const stack = [s];
    comp[s] = n;
    while (stack.length) {
      const c = stack.pop()!;
      const x = c % w;
      const y = Math.floor(c / w);
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        const i = ny * w + nx;
        if (!blocked[i] && comp[i] === -1) {
          comp[i] = n;
          stack.push(i);
        }
      }
    }
    n++;
  }
  return comp;
}

describe("物（NPC・宝箱）も通れなくしたとき", () => {
  it("物のせいで、歩ける場所どうしが分断されない（ふさがれた通路がない）", () => {
    const problems: string[] = [];
    for (const [mapId, map] of Object.entries(WORLD_MAPS)) {
      const npcs = WORLD_NPCS[mapId] ?? [];
      if (npcs.length === 0 || !map.collision) continue;
      const base = map.collision.map((v) => v === 1);
      const withNpc = base.slice();
      for (const npc of npcs) withNpc[npc.tileY * map.width + npc.tileX] = true;
      const before = components(map.width, map.height, base);
      const after = components(map.width, map.height, withNpc);
      // 物なしでつながっていた出入り口どうしが、物ありでは分断されていないか
      const exitIdx = (map.exits ?? []).map((e) => e.tileY * map.width + e.tileX).filter((i) => !withNpc[i]);
      for (const i of exitIdx) {
        for (const j of exitIdx) {
          if (before[i] === before[j] && after[i] !== after[j]) problems.push(`${mapId} (${i % map.width},${Math.floor(i / map.width)})→(${j % map.width},${Math.floor(j / map.width)})`);
        }
      }
    }
    expect(problems).toEqual([]);
  });
});
