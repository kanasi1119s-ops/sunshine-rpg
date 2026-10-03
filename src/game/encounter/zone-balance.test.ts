import { describe, expect, it } from "vitest";
import { partyAtLevel, winRate } from "../battle/balance-helpers";
import { createRng } from "../random";
import { createEncounterEnemies, WORLD_ENCOUNTER_ZONES } from "./encounter";

/**
 * 世界地図の敵のバランス（roadmap 7-0s の申し送り）。想定レベルのパーティが、一団に勝てるかを300回シミュレーションして確かめる。
 * 想定レベルの仲間の人数は、その地方に来る頃の加入状況（本編の順）。
 * 目安: 想定レベルでは勝率95%以上、想定より4レベル低くても勝率40%以上（遠回りして挑む人が詰まらない）。
 */
const COMPANIONS: Record<string, number> = {
  "world-1": 1,
  "world-2": 2,
  "world-3": 4,
  "world-4": 4,
  "world-5": 5,
  "world-6": 5,
  "world-sea": 4,
  "world-air": 5,
};

function rateAt(id: string, level: number): number {
  const zone = WORLD_ENCOUNTER_ZONES[id];
  let n = 0;
  return winRate(partyAtLevel(level, COMPANIONS[id]), () => createEncounterEnemies(id, zone, createRng(n++ * 7 + 1)), 300).rate;
}

describe("世界地図の敵のバランス（300回のシミュレーション）", () => {
  it("すべての地方に仲間の人数が決めてある", () => {
    expect(Object.keys(COMPANIONS).sort()).toEqual(Object.keys(WORLD_ENCOUNTER_ZONES).sort());
  });

  for (const [id, zone] of Object.entries(WORLD_ENCOUNTER_ZONES)) {
    it(`${id}（想定Lv${zone.level}）`, () => {
      expect(rateAt(id, zone.level)).toBeGreaterThanOrEqual(0.95);
      expect(rateAt(id, Math.max(1, zone.level - 4))).toBeGreaterThanOrEqual(0.4);
    });
  }
});
