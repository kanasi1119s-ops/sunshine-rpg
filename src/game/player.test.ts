import { describe, expect, it } from "vitest";
import { createPlayer, updatePlayer } from "./player";
import { createTileMap } from "./map/tile-map";
import type { TileMapData } from "./map/types";

function makeOpenMap(): ReturnType<typeof createTileMap> {
  const data: TileMapData = {
    width: 10,
    height: 10,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: new Array(100).fill(1) }],
    tileColors: { 1: "#000" },
    collision: new Array(100).fill(0),
  };
  return createTileMap(data);
}

function makeWalledMap(): ReturnType<typeof createTileMap> {
  const map = makeOpenMap();
  // (5, 5) を壁にする。
  map.data.collision![5 * 10 + 5] = 1;
  return map;
}

describe("updatePlayer", () => {
  it("方向入力がなければ動かず、moving は false になる", () => {
    const player = createPlayer(80, 80);
    const map = makeOpenMap();
    const result = updatePlayer(player, null, 100, map);
    expect(result.x).toBe(80);
    expect(result.y).toBe(80);
    expect(result.moving).toBe(false);
  });

  it("開けた場所では方向に向かって移動する", () => {
    const player = createPlayer(80, 80);
    const map = makeOpenMap();
    const result = updatePlayer(player, "right", 1000, map);
    expect(result.x).toBeGreaterThan(80);
    expect(result.y).toBe(80);
    expect(result.direction).toBe("right");
    expect(result.moving).toBe(true);
  });

  it("壁にぶつかる方向には移動しないが、向きは変える", () => {
    // プレイヤーの右端がちょうどタイル(5,5)の壁の境界に接する位置に置く。
    const player = createPlayer(5 * 16 - 12, 5 * 16);
    const map = makeWalledMap();
    const result = updatePlayer(player, "right", 100, map);
    expect(result.x).toBe(player.x);
    expect(result.y).toBe(player.y);
    expect(result.direction).toBe("right");
    expect(result.moving).toBe(false);
  });
});
