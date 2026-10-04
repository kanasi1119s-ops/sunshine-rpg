import { describe, expect, it } from "vitest";
import { carveLayers } from "./carve-map";
import { serpentineLayout } from "./serpentine";

/** 入り口から出口まで、歩いてたどり着けるか（4方向）。 */
function reachable(layout: ReturnType<typeof serpentineLayout>): { ok: boolean; steps: number } {
  const { ground, collision } = carveLayers(layout.spec);
  void ground;
  const w = layout.width;
  const start = layout.landmarks.south;
  const goal = layout.landmarks.north;
  const dist = new Map<number, number>([[start.y * w + start.x, 0]]);
  const queue = [start];
  while (queue.length > 0) {
    const cur = queue.shift()!;
    const d = dist.get(cur.y * w + cur.x)!;
    if (cur.x === goal.x && cur.y === goal.y) return { ok: true, steps: d };
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = cur.x + dx;
      const ny = cur.y + dy;
      if (nx < 0 || ny < 0 || nx >= w || ny >= layout.height) continue;
      if (collision[ny * w + nx] === 1 || dist.has(ny * w + nx)) continue;
      dist.set(ny * w + nx, d + 1);
      queue.push({ x: nx, y: ny });
    }
  }
  return { ok: false, steps: -1 };
}

describe("長いダンジョンの形", () => {
  it("入り口から出口まで歩いてたどり着け、道のりは長い（フィールドを歩くように）", () => {
    for (const seed of [1, 7, 23]) {
      const layout = serpentineLayout({ lanes: 5, wall: 4, floor: 1, path: 2, seed });
      const r = reachable(layout);
      expect(r.ok).toBe(true);
      expect(r.steps).toBeGreaterThan(150);
    }
  });

  it("小部屋（寄り道）がいくつもあり、宝箱や仕掛けを置ける", () => {
    const layout = serpentineLayout({ lanes: 5, wall: 4, floor: 1, seed: 3 });
    expect(layout.landmarks.alcoves.length).toBeGreaterThanOrEqual(5);
  });

  it("同じ数字からは、毎回同じ形になる", () => {
    const a = serpentineLayout({ lanes: 5, wall: 4, floor: 1, seed: 9 });
    const b = serpentineLayout({ lanes: 5, wall: 4, floor: 1, seed: 9 });
    expect(carveLayers(a.spec).collision).toEqual(carveLayers(b.spec).collision);
  });
});

import { mazeLayout } from "./serpentine";

describe("迷路のダンジョン", () => {
  function steps(layout: ReturnType<typeof mazeLayout>): number {
    const { collision } = carveLayers(layout.spec);
    const w = layout.width;
    const start = layout.landmarks.south;
    const goal = layout.landmarks.north;
    const dist = new Map<number, number>([[start.y * w + start.x, 0]]);
    const queue = [start];
    while (queue.length > 0) {
      const cur = queue.shift()!;
      const d = dist.get(cur.y * w + cur.x)!;
      if (cur.x === goal.x && cur.y === goal.y) return d;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = cur.x + dx;
        const ny = cur.y + dy;
        if (nx < 0 || ny < 0 || nx >= w || ny >= layout.height || collision[ny * w + nx] === 1 || dist.has(ny * w + nx)) continue;
        dist.set(ny * w + nx, d + 1);
        queue.push({ x: nx, y: ny });
      }
    }
    return -1;
  }

  it("入り口から出口まで歩いてたどり着け、ほとんどの道は行き止まり（迷う）", () => {
    for (const seed of [1, 7, 23, 41, 99]) {
      const layout = mazeLayout({ wall: 4, floor: 1, seed });
      expect(steps(layout)).toBeGreaterThan(100);
      expect(layout.landmarks.alcoves.length).toBeGreaterThanOrEqual(8);
    }
  });

  it("行き止まりの小部屋は、宝箱を置くために歩いてたどり着ける", () => {
    const layout = mazeLayout({ wall: 4, floor: 1, seed: 5 });
    const { collision } = carveLayers(layout.spec);
    for (const a of layout.landmarks.alcoves) expect(collision[a.tileY * layout.width + a.tileX]).toBe(0);
  });
});
