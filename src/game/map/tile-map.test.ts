import { describe, expect, it } from "vitest";
import { createTileMap, findExitAt, getTileId, isWalkable } from "./tile-map";
import type { TileMapData } from "./types";

function makeMapData(): TileMapData {
  // 3x2 のマップ。中央下(1,1)だけ通行不可にする。
  return {
    width: 3,
    height: 2,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: [1, 1, 1, 1, 1, 1] }],
    tileColors: { 1: "#4caf50" },
    collision: [0, 0, 0, 0, 1, 0],
  };
}

describe("createTileMap", () => {
  it("ピクセル単位の大きさを計算する", () => {
    const map = createTileMap(makeMapData());
    expect(map.widthPx).toBe(48);
    expect(map.heightPx).toBe(32);
  });
});

describe("getTileId", () => {
  it("指定した座標のタイルIDを返す", () => {
    const map = createTileMap(makeMapData());
    expect(getTileId(map, 0, 1, 0)).toBe(1);
  });

  it("マップ外は0を返す", () => {
    const map = createTileMap(makeMapData());
    expect(getTileId(map, 0, -1, 0)).toBe(0);
    expect(getTileId(map, 0, 10, 10)).toBe(0);
  });
});

describe("isWalkable", () => {
  it("通行判定レイヤーで1のタイルは通れない", () => {
    const map = createTileMap(makeMapData());
    expect(isWalkable(map, 1, 1)).toBe(false);
  });

  it("通行判定レイヤーで0のタイルは通れる", () => {
    const map = createTileMap(makeMapData());
    expect(isWalkable(map, 0, 0)).toBe(true);
  });

  it("マップ外は通れない", () => {
    const map = createTileMap(makeMapData());
    expect(isWalkable(map, -1, 0)).toBe(false);
    expect(isWalkable(map, 3, 0)).toBe(false);
  });
});

describe("findExitAt", () => {
  it("出入り口が置かれたタイルでは対応する出口情報を返す", () => {
    const data = makeMapData();
    data.exits = [{ tileX: 0, tileY: 0, targetMapId: "room", targetTileX: 2, targetTileY: 2 }];
    const map = createTileMap(data);
    expect(findExitAt(map, 0, 0)).toEqual(data.exits[0]);
  });

  it("出入り口が無いタイルではundefined", () => {
    const map = createTileMap(makeMapData());
    expect(findExitAt(map, 0, 0)).toBeUndefined();
  });
});
