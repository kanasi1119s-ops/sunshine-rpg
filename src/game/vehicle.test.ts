import { describe, expect, it } from "vitest";
import { WORLD_MAPS } from "./world/world";
import { WORLD_CHANNEL, WORLD_SHIP_DOCK, WORLD_SHIP_START, WORLD_TOWER, WORLD_AIRSHIP_START, WORLD_ISLETS } from "./map/world/world-map.generated";
import { buildVehicleCollision, canLandOn, groundIdAt } from "./vehicle";
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
  it("船は、海を進み、海に接する陸には上がれる。塔を囲んでいた渦の輪はなくなり、海になった", () => {
    const c = buildVehicleCollision(world, "ship");
    expect(c[WORLD_SHIP_START.y * W + WORLD_SHIP_START.x]).toBe(0);
    expect(c[WORLD_SHIP_DOCK.y * W + WORLD_SHIP_DOCK.x]).toBe(0);
    expect(world.layers[0].data.some((id) => id === 13 || id === 14)).toBe(false);
    for (const [x, y] of WORLD_CHANNEL) expect(world.layers[0].data[y * W + x]).toBe(1);
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

  it("芯環塔には近寄れない: 船でも飛空艇でも、塔のまわり（大滝・陥没）へは行けない", () => {
    const ship = reach(buildVehicleCollision(world, "ship"), WORLD_SHIP_START);
    // 大滝のふち（半径8.4マス）の内がわへは入れない。その外は海（船で滝のそばまでは行ける）
    for (let dy = -9; dy <= 9; dy++) for (let dx = -9; dx <= 9; dx++) if (Math.hypot(dx, dy) <= 8.4) expect(ship.has((WORLD_TOWER.y + dy) * W + WORLD_TOWER.x + dx)).toBe(false);
    expect(ship.has((WORLD_TOWER.y + 10) * W + WORLD_TOWER.x)).toBe(true);
    for (let dy = -6; dy <= 6; dy++) for (let dx = -6; dx <= 6; dx++) expect(world.collision![(WORLD_TOWER.y + dy) * W + WORLD_TOWER.x + dx]).toBe(1);
    expect(isBasinCauseway(WORLD_TOWER.x, WORLD_TOWER.y + 2)).toBe(false);
    const air = reach(buildVehicleCollision(world, "air"), WORLD_AIRSHIP_START);
    for (let dy = -6; dy <= 6; dy++) for (let dx = -6; dx <= 6; dx++) if (Math.hypot(dx, dy) <= 6.6) expect(air.has((WORLD_TOWER.y + dy) * W + WORLD_TOWER.x + dx)).toBe(false);
  });

  it("飛空艇は、山や海の上も飛べるが、塔のまわりの大滝（嵐）は越えられない。着陸は歩ける地形だけ", () => {
    const c = buildVehicleCollision(world, "air");
    expect(c[(WORLD_AIRSHIP_START.y) * W + WORLD_AIRSHIP_START.x]).toBe(0);
    expect(c[(WORLD_TOWER.y + 7) * W + WORLD_TOWER.x]).toBe(1);
    expect(canLandOn(2)).toBe(true);
    expect(canLandOn(1)).toBe(false);
    expect(canLandOn(4)).toBe(false);
    expect(groundIdAt(world, 0, 0)).toBe(1);
  });
});

describe("芯環塔の上の積乱雲の下: 船は雲のうしろを進め、飛空艇は入れない", () => {
  it("雲の下の海は、船は通れて、飛空艇は通れない", () => {
    const ship = buildVehicleCollision(world, "ship");
    const air = buildVehicleCollision(world, "air");
    const at = (c: number[], dx: number, dy: number): number => c[(WORLD_TOWER.y + dy) * W + WORLD_TOWER.x + dx];
    expect(groundIdAt(world, WORLD_TOWER.x, WORLD_TOWER.y - 10)).toBe(1);
    expect(at(ship, 0, -10)).toBe(0);
    expect(at(air, 0, -10)).toBe(1);
    expect(at(ship, -9, -9)).toBe(0);
    // 雲より上（北）の海は、これまでどおり通れる
    expect(groundIdAt(world, WORLD_TOWER.x, WORLD_TOWER.y - 19)).toBe(1);
    expect(at(ship, 0, -19)).toBe(0);
  });
});
