import { describe, expect, it } from "vitest";
import { findNpcAt, getFacingTile, type Npc } from "./npc";
import { createPlayer } from "./player";

describe("getFacingTile", () => {
  it("下を向いているとき、1つ下のタイルを返す", () => {
    const player = createPlayer(16, 16);
    player.direction = "down";
    expect(getFacingTile(player, 16, 16)).toEqual({ tileX: 1, tileY: 2 });
  });

  it("左を向いているとき、1つ左のタイルを返す", () => {
    const player = createPlayer(32, 16);
    player.direction = "left";
    expect(getFacingTile(player, 16, 16)).toEqual({ tileX: 1, tileY: 1 });
  });
});

describe("findNpcAt", () => {
  it("指定タイルにいるNPCを返す", () => {
    const npcs: Npc[] = [{ id: "a", tileX: 2, tileY: 3, color: "#fff", commands: [] }];
    expect(findNpcAt(npcs, 2, 3)?.id).toBe("a");
  });

  it("誰もいなければundefined", () => {
    const npcs: Npc[] = [{ id: "a", tileX: 2, tileY: 3, color: "#fff", commands: [] }];
    expect(findNpcAt(npcs, 0, 0)).toBeUndefined();
  });
});
