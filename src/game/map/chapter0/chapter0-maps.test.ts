import { describe, expect, it } from "vitest";
import { createTouriTownData } from "./touri-town";
import { createTouriBranchData } from "./touri-branch";
import { createTouriOutskirtsData } from "./touri-outskirts";
import type { TileMapData } from "../types";

const MAPS: Record<string, TileMapData> = {
  "touri-town": createTouriTownData(),
  "touri-branch": createTouriBranchData(),
  "touri-outskirts": createTouriOutskirtsData(),
};

describe.each(Object.entries(MAPS))("序章の地図データ: %s", (_id, data) => {
  it("通行判定レイヤーの長さが width*height と一致する", () => {
    expect(data.collision).toHaveLength(data.width * data.height);
  });

  it("地面レイヤーの長さが width*height と一致する", () => {
    expect(data.layers[0]?.data).toHaveLength(data.width * data.height);
  });

  it("使われているすべてのタイルIDに色が定義されている", () => {
    const usedIds = new Set<number>();
    for (const layer of data.layers) {
      for (const id of layer.data) {
        usedIds.add(id);
      }
    }
    for (const id of usedIds) {
      expect(data.tileColors[id], `タイルID ${id} の色が未定義`).toBeDefined();
    }
  });

  it("出入り口はすべて実在するマップを指し、通行可能なタイルに置かれている", () => {
    for (const exit of data.exits ?? []) {
      expect(Object.keys(MAPS), `${exit.targetMapId} という地図が存在しない`).toContain(
        exit.targetMapId,
      );
      const index = exit.tileY * data.width + exit.tileX;
      expect(data.collision?.[index] ?? 0, `出入り口 (${exit.tileX},${exit.tileY}) が通行不可`).toBe(
        0,
      );

      const target = MAPS[exit.targetMapId];
      expect(
        exit.targetTileX >= 0 && exit.targetTileX < target.width,
        `${exit.targetMapId} の移動先タイルXが範囲外`,
      ).toBe(true);
      expect(
        exit.targetTileY >= 0 && exit.targetTileY < target.height,
        `${exit.targetMapId} の移動先タイルYが範囲外`,
      ).toBe(true);
      const targetIndex = exit.targetTileY * target.width + exit.targetTileX;
      expect(
        target.collision?.[targetIndex] ?? 0,
        `${exit.targetMapId} の移動先タイル (${exit.targetTileX},${exit.targetTileY}) が通行不可`,
      ).toBe(0);
    }
  });
});

describe("序章の地図どうしのつながり", () => {
  it("出口の移動先が、移動先マップ自身の出口タイルと重ならない（着いた瞬間に押し戻される事故を防ぐ）", () => {
    for (const [mapId, data] of Object.entries(MAPS)) {
      for (const exit of data.exits ?? []) {
        const target = MAPS[exit.targetMapId];
        const bounceBack = target.exits?.some(
          (targetExit) => targetExit.tileX === exit.targetTileX && targetExit.tileY === exit.targetTileY,
        );
        expect(
          bounceBack,
          `${mapId} → ${exit.targetMapId} の移動先 (${exit.targetTileX},${exit.targetTileY}) が向こうの出口タイルと重なっている`,
        ).toBe(false);
      }
    }
  });
});
