import { describe, expect, it } from "vitest";
import { INN_SPOTS } from "../map/town-decor";
import { INN_H, INN_W } from "./inn-interiors";
import { WORLD_MAPS, WORLD_NPCS } from "./world";

describe("宿屋の建物", () => {
  const towns = ["touri-town", "mugikano-village", "garasuko-town", "tetsukusari-town", "sanone-town", "kiri-town", "shimohara-town", "fushima-town", "toushin-town"];
  for (const town of towns) {
    it(`${town}: 2階建ての宿屋があり、受付で「とまる」を選べる`, () => {
      expect(INN_SPOTS.has(town), `${town} に宿屋の建物がない`).toBe(true);
      const f1 = `inn-${town}-1f`, f2 = `inn-${town}-2f`;
      expect(WORLD_MAPS[f1]).toBeDefined();
      expect(WORLD_MAPS[f2]).toBeDefined();
      // 町から入れる
      const spot = INN_SPOTS.get(town)!;
      expect(WORLD_MAPS[town].exits?.some((e) => e.targetMapId === f1 && e.tileX === spot.x && e.tileY === spot.y + 1)).toBe(true);
      // 1階: カウンターの前で話すと、とまる選択。奥に店員、大部屋にベッド6つ
      const n1 = WORLD_NPCS[f1];
      const counters = n1.filter((n) => n.id.includes("-counter-"));
      expect(counters.length).toBeGreaterThanOrEqual(4);
      expect(counters.every((c) => c.commands.some((x) => x.type === "inn"))).toBe(true);
      const clerk = n1.find((n) => n.id.endsWith("-clerk"))!;
      expect(clerk.tileY).toBeLessThan(counters[0].tileY);          // 店員はカウンターの奥
      expect(n1.filter((n) => n.id.includes("-bed-"))).toHaveLength(6);
      // 2階: ベッド2つずつの部屋が2つ（ベッド4つ）。部屋ごとにテーブルと棚
      const n2 = WORLD_NPCS[f2];
      expect(n2.filter((n) => n.id.includes("-bed-"))).toHaveLength(4);
      expect(n2.filter((n) => n.id.includes("-table-"))).toHaveLength(2);
      expect(n2.filter((n) => n.id.includes("-shelf-"))).toHaveLength(2);
      // 広さ: ふつうの家（11×8）の8倍ほど（1階・2階あわせて）
      expect((INN_W * INN_H * 2) / (11 * 8)).toBeGreaterThanOrEqual(7.5);
      // 階段でつながる
      expect(WORLD_MAPS[f1].exits?.some((e) => e.targetMapId === f2)).toBe(true);
      expect(WORLD_MAPS[f2].exits?.some((e) => e.targetMapId === f1)).toBe(true);
    });
  }
});
