import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world/world";
import { WORLD_CHANNEL, WORLD_SHIP_DOCK, WORLD_SHIP_START, WORLD_TOWER, WORLD_AIRSHIP_START, WORLD_ISLETS } from "./map/world/world-map.generated";
import { buildVehicleCollision, canLandOn, groundIdAt, openVortexChannel } from "./vehicle";

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
    for (const islet of WORLD_ISLETS) {
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
    let touch = false;
    for (let dy = -4; dy <= 4 && !touch; dy++) for (let dx = -4; dx <= 4; dx++) if (after.has((WORLD_TOWER.y + dy) * W + WORLD_TOWER.x + dx)) { touch = true; break; }
    expect(touch).toBe(true);
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
