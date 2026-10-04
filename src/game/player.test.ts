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

  it("動いている間、歩行アニメーション用の経過時間が進む", () => {
    const player = createPlayer(80, 80);
    const map = makeOpenMap();
    const first = updatePlayer(player, "right", 100, map);
    expect(first.animationMs).toBe(100);
    const second = updatePlayer(first, "right", 50, map);
    expect(second.animationMs).toBe(150);
  });

  it("止まると、歩行アニメーション用の経過時間が0に戻る", () => {
    const player = { ...createPlayer(80, 80), animationMs: 200 };
    const map = makeOpenMap();
    const result = updatePlayer(player, null, 100, map);
    expect(result.animationMs).toBe(0);
  });

  it("壁にぶつかって止まったときも、経過時間が0に戻る", () => {
    const player = { ...createPlayer(5 * 16 - 12, 5 * 16), animationMs: 200 };
    const map = makeWalledMap();
    const result = updatePlayer(player, "right", 100, map);
    expect(result.animationMs).toBe(0);
  });
});

describe("出口・角のすべり補助とNPCの通せんぼ", () => {
  /** 上の壁の列に、1マス（x=5）だけ出口が開いている地図。 */
  function makeGateMap(): ReturnType<typeof createTileMap> {
    const map = makeOpenMap();
    for (let x = 0; x < 10; x++) {
      if (x !== 5) map.data.collision![2 * 10 + x] = 1;
    }
    return map;
  }

  it("出口の幅より少しずれていても、上へ進むだけで出口へ横にすべって通れる", () => {
    const map = makeGateMap();
    // 出口(x=5: 80〜96px)に対し、プレイヤー（幅12）の左端が 85px。右端が 97px で壁にかかる。
    let player = createPlayer(85, 60);
    for (let i = 0; i < 60; i++) player = updatePlayer(player, "up", 16, map);
    expect(player.y).toBeLessThan(32);
  });

  it("遠く離れた壁の前では、すべらずに止まる", () => {
    const map = makeGateMap();
    let player = createPlayer(20, 60);
    for (let i = 0; i < 60; i++) player = updatePlayer(player, "up", 16, map);
    expect(player.y).toBeGreaterThanOrEqual(32);
    expect(player.x).toBe(20);
  });

  it("NPCのいるマスには入れない", () => {
    const map = makeOpenMap();
    let player = createPlayer(80, 80);
    for (let i = 0; i < 40; i++) player = updatePlayer(player, "right", 16, map, [{ tileX: 7, tileY: 5 }]);
    // NPC（x=112〜）の手前で止まる。プレイヤーの右端 = x + 12 <= 112
    expect(player.x + player.width).toBeLessThanOrEqual(112);
  });

  it("NPCと重なってしまったときは、離れる向きに動ける", () => {
    const map = makeOpenMap();
    const player = createPlayer(80, 80);
    const result = updatePlayer(player, "left", 100, map, [{ tileX: 5, tileY: 5 }]);
    expect(result.x).toBeLessThan(80);
  });
});
