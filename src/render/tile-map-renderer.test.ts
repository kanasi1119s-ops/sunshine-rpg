import { describe, expect, it } from "vitest";
import { createTileMap } from "../game/map/tile-map";
import type { TileMapData } from "../game/map/types";
import { createCamera } from "./camera";
import { renderTileMap } from "./tile-map-renderer";

class FakeContext {
  fillStyle = "";
  calls: { color: string; x: number; y: number; w: number; h: number }[] = [];

  fillRect(x: number, y: number, w: number, h: number): void {
    this.calls.push({ color: this.fillStyle, x, y, w, h });
  }
}

function makeMapData(): TileMapData {
  return {
    width: 4,
    height: 4,
    tileWidth: 10,
    tileHeight: 10,
    layers: [{ name: "ground", data: new Array(16).fill(1) }],
    tileColors: { 1: "#ff0000" },
  };
}

describe("renderTileMap", () => {
  it("0番のタイルは描画しない", () => {
    const data = makeMapData();
    data.layers[0].data[0] = 0;
    const map = createTileMap(data);
    const camera = createCamera(40, 40);
    const ctx = new FakeContext();

    renderTileMap(ctx as unknown as CanvasRenderingContext2D, map, camera);

    expect(ctx.calls.some((c) => c.x === 0 && c.y === 0)).toBe(false);
  });

  it("カメラに映る範囲のタイルをワールド座標からカメラ分ずらして描画する", () => {
    const map = createTileMap(makeMapData());
    const camera = createCamera(20, 20);
    camera.x = 10;
    camera.y = 10;
    const ctx = new FakeContext();

    renderTileMap(ctx as unknown as CanvasRenderingContext2D, map, camera);

    // タイル(1,1)はワールド座標(10,10)。カメラが(10,10)にいるので画面上は(0,0)。
    expect(ctx.calls.some((c) => c.x === 0 && c.y === 0 && c.color === "#ff0000")).toBe(
      true,
    );
  });
});
