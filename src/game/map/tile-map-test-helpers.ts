import { describe, expect, it } from "vitest";
import type { TileMapData } from "./types";

/**
 * 章ごとの地図データの整合性チェック（章の外の情報を必要としないもの）。
 * 章のマップ用テストファイルから呼び出して使う。
 */
export function describeMapDataIntegrity(label: string, mapsById: Record<string, TileMapData>): void {
  describe.each(Object.entries(mapsById))(`${label}: %s`, (_id, data) => {
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

    it("出入り口は自分の地図内で通行可能なタイルに置かれている", () => {
      for (const exit of data.exits ?? []) {
        const index = exit.tileY * data.width + exit.tileX;
        expect(data.collision?.[index] ?? 0, `出入り口 (${exit.tileX},${exit.tileY}) が通行不可`).toBe(0);
      }
    });
  });
}

/**
 * 複数の章にまたがる出入り口の整合性チェック（他の地図の情報が必要なもの）。
 * すべての章の地図をまとめた「世界」全体のレジストリに対して1回だけ呼び出す。
 */
export function describeWorldExitIntegrity(label: string, worldMaps: Record<string, TileMapData>): void {
  describe(label, () => {
    it("出入り口の移動先は、すべて世界に実在する地図を指している", () => {
      for (const [mapId, data] of Object.entries(worldMaps)) {
        for (const exit of data.exits ?? []) {
          expect(
            Object.keys(worldMaps),
            `${mapId} の出入り口が指す "${exit.targetMapId}" という地図が存在しない`,
          ).toContain(exit.targetMapId);
        }
      }
    });

    it("出入り口の移動先タイルは範囲内・通行可能で、向こうの出口タイルと重ならない（往復事故の防止）", () => {
      for (const [mapId, data] of Object.entries(worldMaps)) {
        for (const exit of data.exits ?? []) {
          const target = worldMaps[exit.targetMapId];
          if (!target) {
            continue; // 前のテストで別途検出済み
          }
          expect(
            exit.targetTileX >= 0 && exit.targetTileX < target.width,
            `${mapId} → ${exit.targetMapId} の移動先タイルXが範囲外`,
          ).toBe(true);
          expect(
            exit.targetTileY >= 0 && exit.targetTileY < target.height,
            `${mapId} → ${exit.targetMapId} の移動先タイルYが範囲外`,
          ).toBe(true);
          const targetIndex = exit.targetTileY * target.width + exit.targetTileX;
          expect(
            target.collision?.[targetIndex] ?? 0,
            `${mapId} → ${exit.targetMapId} の移動先タイル (${exit.targetTileX},${exit.targetTileY}) が通行不可`,
          ).toBe(0);

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
}
