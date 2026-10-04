import { describe, expect, it } from "vitest";
import { WORLD_NPCS } from "./world";

describe("すべての町に宿屋の主人がいる", () => {
  const towns = ["touri-town", "mugikano-village", "garasuko-town", "tetsukusari-town", "sanone-town", "kiri-town", "shimohara-town", "fushima-town", "toushin-town"];
  for (const id of towns) {
    it(`${id}: 宿屋の主人にとまる選択がある`, () => {
      const keeper = (WORLD_NPCS[id] ?? []).find((n) => /-innkeeper$/.test(n.id));
      expect(keeper, id).toBeDefined();
      expect(keeper!.commands.some((c) => c.type === "inn")).toBe(true);
    });
  }
});
