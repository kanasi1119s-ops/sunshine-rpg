import { describe, expect, it } from "vitest";
import { createTileMap, getTileId, isWalkable } from "./tile-map";
import { createPlayer, updatePlayer } from "../player";

function map(wrap: boolean) {
  const w = 4, h = 3;
  return createTileMap({
    width: w, height: h, tileWidth: 16, tileHeight: 16,
    layers: [{ name: "g", data: Array.from({ length: w * h }, (_, i) => i + 1) }],
    tileColors: {}, collision: new Array(w * h).fill(0), wrap,
  } as never);
}

describe("上下左右がつながる地図", () => {
  it("端の外側のマスも、反対側のマスとして読める", () => {
    const m = map(true);
    expect(getTileId(m, 0, -1, 0)).toBe(getTileId(m, 0, 3, 0));
    expect(getTileId(m, 0, 0, 3)).toBe(getTileId(m, 0, 0, 0));
    expect(isWalkable(m, -1, -1)).toBe(true);
  });
  it("つながらない地図は、外が通れない", () => {
    expect(isWalkable(map(false), -1, 0)).toBe(false);
  });
  it("左の端から出ると右の端に出て、上の端から出ると下の端に出る", () => {
    const m = map(true);
    const l = updatePlayer({ ...createPlayer(0, 16), }, "left", 500, m);
    expect(l.x).toBeGreaterThan(m.widthPx - 40);
    const u = updatePlayer({ ...createPlayer(16, 0) }, "up", 500, m);
    expect(u.y).toBeGreaterThan(m.heightPx - 40);
    const r = updatePlayer(createPlayer(m.widthPx - 13, 16), "right", 500, m);
    expect(r.x).toBeLessThan(40);
  });
});
