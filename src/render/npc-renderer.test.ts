import { describe, expect, it } from "vitest";
import { npcFeetY, renderNpcs } from "./npc-renderer";
import { npcLook, spriteSpecForNpc } from "../game/sprite/character-specs";
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
  it("spriteNameが登録済みのNPCも、名前の無いNPCも、16×32のドット絵として描く", () => {
    for (const npc of [
      { id: "touri-kasen", tileX: 1, tileY: 1, color: "#7a8fa6", spriteName: "カセン", commands: [] },
      { id: "touri-fisherman", tileX: 1, tileY: 1, color: "#e0a458", commands: [] },
    ] as Npc[]) {
      const ctx = new FakeContext();
      renderNpcs(ctx as unknown as CanvasRenderingContext2D, [npc], makeMap(), createCamera(64, 64));
      expect(ctx.rectCalls.length).toBeGreaterThan(20);
      expect(Math.max(...ctx.rectCalls.map((r) => r.y))).toBeLessThanOrEqual(33); // 足元は、そのマスの下端まで（影が下に2行）
    }
  });

  it("台・扉・宝箱・壁画・敵のNPCは、人ではなく、小さな箱・結晶として描く（人のドット絵より、描く回数が少ない）", () => {
    const person = new FakeContext();
    renderNpcs(person as unknown as CanvasRenderingContext2D, [{ id: "town-villager", tileX: 1, tileY: 1, color: "#7a8fa6", commands: [] }], makeMap(), createCamera(64, 64));
    for (const id of ["deep1-pedestal-a", "tower1-chest", "kyotoukyu-mural-left", "god-1-altar", "chapter0-yugami", "deep4-boss", "tower2-guard"]) {
      const ctx = new FakeContext();
      renderNpcs(ctx as unknown as CanvasRenderingContext2D, [{ id, tileX: 1, tileY: 1, color: "#7a8fa6", commands: [] }], makeMap(), createCamera(64, 64));
      expect(ctx.rectCalls.length, id).toBeGreaterThan(0);
      expect(ctx.rectCalls.length, id).toBeLessThan(person.rectCalls.length);
    }
  });

  it("npcLook: 人・物・敵を分ける。衛兵（toushin-guard）は人。サブストーリーの調べる場所は、最初に話す人がいれば人", () => {
    const say = (speaker?: string) => [{ type: "message" as const, text: "あ", speaker }];
    expect(npcLook({ id: "toushin-guard", commands: [] })).toBe("person");
    expect(npcLook({ id: "tower2-guard", commands: [] })).toBe("monster");
    expect(npcLook({ id: "god-3-boss", commands: [] })).toBe("monster");
    expect(npcLook({ id: "deep1-gate", commands: [] })).toBe("object");
    expect(npcLook({ id: "side-s001-step1", commands: say(undefined) })).toBe("object");
    expect(npcLook({ id: "side-s004-step1", commands: say("井戸端の少年") })).toBe("person");
    expect(npcLook({ id: "side-s001-giver", commands: say(undefined) })).toBe("person");
  });

  it("同じNPCはいつも同じ見た目（色）。別のNPCは、見た目が変わる", () => {
    const draw = (id: string) => {
      const ctx = new FakeContext();
      renderNpcs(ctx as unknown as CanvasRenderingContext2D, [{ id, tileX: 1, tileY: 1, color: "#7a8fa6", commands: [] }], makeMap(), createCamera(64, 64));
      return JSON.stringify(ctx.rectCalls);
    };
    expect(draw("a-1")).toBe(draw("a-1"));
    const looks = new Set(["a-1", "b-2", "c-3", "d-4", "e-5", "f-6"].map((id) => JSON.stringify(spriteSpecForNpc({ id, color: "#7a8fa6" }))));
    expect(looks.size).toBeGreaterThan(3);
  });

  it("filterで、描くNPCを絞れる（プレイヤーより奥・手前に分けて描くため）", () => {
    const npcs: Npc[] = [
      { id: "n-a", tileX: 0, tileY: 0, color: "#7a8fa6", commands: [] },
      { id: "n-b", tileX: 2, tileY: 3, color: "#a08050", commands: [] },
    ];
    const ctx = new FakeContext();
    renderNpcs(ctx as unknown as CanvasRenderingContext2D, npcs, makeMap(), createCamera(64, 64), (n) => n.id === "n-b");
    const all = new FakeContext();
    renderNpcs(all as unknown as CanvasRenderingContext2D, npcs, makeMap(), createCamera(64, 64));
    expect(ctx.rectCalls.length).toBeGreaterThan(20);
    expect(ctx.rectCalls.length).toBeLessThan(all.rectCalls.length);
    expect(npcFeetY(npcs[1], 16)).toBe(64);
  });
});
