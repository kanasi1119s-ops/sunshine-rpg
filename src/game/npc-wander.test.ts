import { describe, expect, it } from "vitest";
import { createTileMap } from "./map/tile-map";
import type { Npc } from "./npc";
import { faceNpc, opposite, updateWander, wanderStateOf, WANDER_MOVE_MS, WANDER_RADIUS } from "./npc-wander";

function openMap(width = 12, height = 12, blocked: number[] = []) {
  const collision = new Array(width * height).fill(0);
  for (const i of blocked) collision[i] = 1;
  return createTileMap({ width, height, tileWidth: 16, tileHeight: 16, layers: [{ name: "ground", data: new Array(width * height).fill(1) }], tileColors: { 1: "#000" }, collision });
}

function npc(id: string, x: number, y: number, wander = true): Npc {
  return { id, tileX: x, tileY: y, color: "#fff", commands: [], wander };
}

describe("町の人のぶらぶら歩き", () => {
  it("wander でない人は動かない", () => {
    const n = npc("still", 5, 5, false);
    updateWander([n], openMap(), { x: 0, y: 0 }, 20000, false, Math.random);
    expect([n.tileX, n.tileY]).toEqual([5, 5]);
  });

  it("歩き出すと、歩いた先のマスが今の位置になり、歩き終えるまで moving が続く", () => {
    const n = npc("walker-a", 5, 5);
    const map = openMap();
    // 待ち時間が切れるまで進め、向きは「右」（rng=0.8 → 4方向の4番目）
    updateWander([n], map, { x: 0, y: 0 }, 5000, false, () => 0.8);
    expect(n.tileX).toBe(6);
    const s = wanderStateOf("walker-a")!;
    expect(s.moving).toBe(true);
    expect(s.dir).toBe("right");
    expect(s.fromX).toBe(5);
    updateWander([n], map, { x: 0, y: 0 }, WANDER_MOVE_MS + 10, false, () => 0.8);
    expect(wanderStateOf("walker-a")!.moving).toBe(false);
  });

  it("家から離れすぎない（何度歩いても、半径内）", () => {
    const n = npc("walker-b", 6, 6);
    const map = openMap();
    for (let i = 0; i < 400; i++) {
      updateWander([n], map, { x: 0, y: 0 }, 700, false, Math.random);
      expect(Math.abs(n.tileX - 6)).toBeLessThanOrEqual(WANDER_RADIUS);
      expect(Math.abs(n.tileY - 6)).toBeLessThanOrEqual(WANDER_RADIUS);
    }
  });

  it("通れないマス・プレイヤーのいるマス・ほかの人のいるマスには入らない", () => {
    const map = openMap(12, 12, [5 * 12 + 6]);
    const n = npc("walker-c", 5, 5);
    updateWander([n], map, { x: 0, y: 0 }, 5000, false, () => 0.8); // 右(6,5)は壁
    expect(n.tileX).toBe(5);
    const n2 = npc("walker-d", 5, 5);
    updateWander([n2], openMap(), { x: 6, y: 5 }, 5000, false, () => 0.8); // 右にプレイヤー
    expect(n2.tileX).toBe(5);
    const n3 = npc("walker-e", 5, 5);
    updateWander([n3, npc("other", 6, 5, false)], openMap(), { x: 0, y: 0 }, 5000, false, () => 0.8);
    expect(n3.tileX).toBe(5);
  });

  it("会話中（paused）は、新しく歩き出さない。話しかけられたら相手のほうを向く", () => {
    const n = npc("walker-f", 5, 5);
    updateWander([n], openMap(), { x: 0, y: 0 }, 9000, true, () => 0.8);
    expect(n.tileX).toBe(5);
    faceNpc(n, opposite("up"));
    expect(wanderStateOf("walker-f")!.dir).toBe("down");
  });
});
