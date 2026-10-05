import { describe, expect, it } from "vitest";
import { createTileMap } from "./map/tile-map";
import type { TileMapData } from "./map/types";
import { isOpenSpot, rescueTile } from "./player-rescue";

function mapOf(rows: string[]): ReturnType<typeof createTileMap> {
  const h = rows.length, w = rows[0].length;
  const data: TileMapData = {
    id: "t", width: w, height: h, tileWidth: 16, tileHeight: 16,
    layers: [{ name: "ground", data: new Array(w * h).fill(1) }],
    tileColors: { 1: "#444" },
    collision: rows.join("").split("").map((c) => (c === "#" ? 1 : 0)),
  } as TileMapData;
  return createTileMap(data);
}

describe("動けなくなったときの救出", () => {
  const rows = [
    "####################",
    "#..................#",
    "#..................#",
    "#........#.........#",
    "#.......#X#........#",
    "#........#.........#",
    "#..................#",
    "####################",
  ];
  const map = mapOf(rows);
  it("四方を囲まれたマスは、動ける場所ではない", () => {
    expect(isOpenSpot(map, 9, 4)).toBe(false);
  });
  it("囲まれていたら、近くの広い場所へ移す", () => {
    const r = rescueTile(map, 9, 4);
    expect(r).not.toBeNull();
    expect(isOpenSpot(map, r!.x, r!.y)).toBe(true);
    expect(Math.abs(r!.x - 9) + Math.abs(r!.y - 4)).toBeLessThanOrEqual(4);
  });
  it("ふさがったマスの上に立っていても、移す", () => {
    expect(rescueTile(map, 8, 4)).not.toBeNull();
  });
  it("ふつうの場所では何もしない", () => {
    expect(rescueTile(map, 3, 3)).toBeNull();
  });
});
