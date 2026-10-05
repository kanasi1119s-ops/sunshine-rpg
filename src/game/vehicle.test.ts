import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world/world";
import { WORLD_CHANNEL, WORLD_SHIP_DOCK, WORLD_SHIP_START, WORLD_TOWER, WORLD_AIRSHIP_START, WORLD_ISLETS } from "./map/world/world-map.generated";
import { buildVehicleCollision, canLandOn, closeVortexChannel, groundIdAt, openVortexChannel } from "./vehicle";
import { isBasinCauseway } from "./map/world/world-map";

const world = WORLD_MAPS["world-map"];
const W = world.width;

function reach(collision: number[], from: { x: number; y: number }): Set<number> {
  const seen = new Set<number>([from.y * W + from.x]);
  const st: Array<[number, number]> = [[from.x, from.y]];
  while (st.length) {
    const [x, y] = st.pop()!;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= W || ny >= world.height || collision[ny * W + nx] === 1 || seen.has(ny * W + nx)) continue;
      seen.add(ny * W + nx);
      st.push([nx, ny]);
    }
  }
  return seen;
}

describe("乗り物（船・飛空艇）", () => {
  it("船は、海を進み、海に接する陸には上がれる。山・湖・渦の輪は通れない", () => {
    const c = buildVehicleCollision(world, "ship");
    expect(c[WORLD_SHIP_START.y * W + WORLD_SHIP_START.x]).toBe(0);
    expect(c[WORLD_SHIP_DOCK.y * W + WORLD_SHIP_DOCK.x]).toBe(0);
    for (const [x, y] of WORLD_CHANNEL) {
      expect(c[y * W + x], `渦の切れ目 (${x},${y}) は航路が開く前は通れない`).toBe(1);
    }
  });

  it("船で、4つの大陸すべてと、4つの小島の海岸へ行ける（航路が開く前でも）", () => {
    const c = buildVehicleCollision(world, "ship");
    const seen = reach(c, WORLD_SHIP_START);
    // 3つの大陸（西・北東・南東）の、それぞれの海岸のどこかに着けること
    for (const [name, x0, y0, x1, y1] of [["西の大陸", 6, 60, 115, 160], ["北東の大陸", 120, 8, 225, 75], ["南東の大陸", 135, 108, 232, 186]] as Array<[string, number, number, number, number]>) {
      let found = false;
      for (let y = y0; y <= y1 && !found; y++) for (let x = x0; x <= x1; x++) if (seen.has(y * W + x)) { found = true; break; }
      expect(found, `${name} の海岸へ船で行ける`).toBe(true);
    }
    for (const islet of WORLD_ISLETS.slice(0, 5)) { // 6つ目の火口の迷宮は、灯芯大陸の内陸（歩いて行く）
      let near = false;
      for (let dy = -6; dy <= 6 && !near; dy++) for (let dx = -6; dx <= 6; dx++) if (seen.has((islet.y + dy) * W + islet.x + dx)) { near = true; break; }
      expect(near, `${islet.name} へ船で行ける`).toBe(true);
    }
  });

  it("航路が開くと、渦の切れ目が海になり、船で塔の島へ行ける。開く前は、塔の島へ着けない", () => {
    const before = reach(buildVehicleCollision(world, "ship"), WORLD_SHIP_START);
    expect(before.has((WORLD_TOWER.y + 3) * W + WORLD_TOWER.x)).toBe(false);
    const copy = { ...world, layers: [{ ...world.layers[0], data: [...world.layers[0].data] }] };
    expect(openVortexChannel(copy)).toBe(true);
    const after = reach(buildVehicleCollision(copy, "ship"), WORLD_SHIP_START);
    // 塔は陥没した穴のまんなか（2026-10-05）。船は、穴を渡る岩の細い道の南のはしに着け、そこから歩いて塔の入口へ行く
    let end = WORLD_TOWER.y + 1;
    while (isBasinCauseway(WORLD_TOWER.x, end + 1)) end++;
    expect(after.has(end * W + WORLD_TOWER.x)).toBe(true);
    for (let y = WORLD_TOWER.y + 1; y <= end; y++) expect(world.collision![y * W + WORLD_TOWER.x], `道 ${y}`).toBe(0);
    // 道のほかは、大滝と穴で近づけない
    expect(world.collision![(WORLD_TOWER.y + 3) * W + WORLD_TOWER.x + 3]).toBe(1);
    // 「はじめから」で航路が閉じた状態に戻せる
    expect(closeVortexChannel(copy)).toBe(true);
    expect(closeVortexChannel(copy)).toBe(false);
    expect(copy.layers[0].data).toEqual(world.layers[0].data);
  });

  it("飛空艇は、山や海の上も飛べるが、渦の輪の嵐は越えられない。着陸は歩ける地形だけ", () => {
    const c = buildVehicleCollision(world, "air");
    expect(c[(WORLD_AIRSHIP_START.y) * W + WORLD_AIRSHIP_START.x]).toBe(0);
    for (const [x, y] of WORLD_CHANNEL) expect(c[y * W + x]).toBe(1);
    expect(canLandOn(2)).toBe(true);
    expect(canLandOn(1)).toBe(false);
    expect(canLandOn(4)).toBe(false);
    expect(groundIdAt(world, 0, 0)).toBe(1);
  });
});
