import { describe, expect, it } from "vitest";
import { renderNpcs } from "./npc-renderer";
import { createTileMap } from "../game/map/tile-map";
import type { TileMapData } from "../game/map/types";
import { createCamera } from "./camera";
import type { Npc } from "../game/npc";

class FakeContext {
  fillStyle = "";
  rectCalls: { x: number; y: number; w: number; h: number }[] = [];

  fillRect(x: number, y: number, w: number, h: number): void {
    this.rectCalls.push({ x, y, w, h });
  }
}

function makeMap(): ReturnType<typeof createTileMap> {
  const data: TileMapData = {
    width: 4,
    height: 4,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: new Array(16).fill(1) }],
    tileColors: { 1: "#5a9a4a" },
  };
  return createTileMap(data);
}

describe("renderNpcs", () => {
  it("spriteNameが登録済みのNPCは、ドット絵として複数のマスを描く", () => {
    const npcs: Npc[] = [{ id: "touri-kasen", tileX: 1, tileY: 1, color: "#7a8fa6", spriteName: "カセン", commands: [] }];
    const ctx = new FakeContext();
    renderNpcs(ctx as unknown as CanvasRenderingContext2D, npcs, makeMap(), createCamera(64, 64));
    expect(ctx.rectCalls.length).toBeGreaterThan(1);
  });

  it("spriteNameが無い、または未登録のNPCは、これまで通り色付き四角1回で描く", () => {
    const npcs: Npc[] = [{ id: "touri-fisherman", tileX: 1, tileY: 1, color: "#e0a458", commands: [] }];
    const ctx = new FakeContext();
    renderNpcs(ctx as unknown as CanvasRenderingContext2D, npcs, makeMap(), createCamera(64, 64));
    expect(ctx.rectCalls.length).toBe(1);
  });
});
