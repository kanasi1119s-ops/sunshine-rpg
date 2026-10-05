import { describe, expect, it } from "vitest";
import { partyAtLevel, winRate } from "../battle/balance-helpers";
import { createRng } from "../random";
import { createEncounterEnemies, ENCOUNTER_ZONES, WORLD_ENCOUNTER_ZONES } from "./encounter";

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
  return winRate(partyAtLevel(level, COMPANIONS[id]), () => createEncounterEnemies(id, zone, createRng(n++ * 7 + 1), COMPANIONS[id]), 300).rate;
}

describe("世界地図の敵のバランス（300回のシミュレーション）", () => {
  it("すべての地方に仲間の人数が決めてある", () => {
    expect(Object.keys(COMPANIONS).sort()).toEqual(Object.keys(WORLD_ENCOUNTER_ZONES).sort());
  });

  for (const [id, zone] of Object.entries(WORLD_ENCOUNTER_ZONES)) {
    it(`${id}（想定Lv${zone.level}）`, () => {
      expect(rateAt(id, zone.level)).toBeGreaterThanOrEqual(0.85); // 2026-10-05: 仲間が増えるほど敵が強くなるので、0.95から下げた
      expect(rateAt(id, Math.max(1, zone.level - 4))).toBeGreaterThanOrEqual(0.4);
    });
  }
});

/** 通常のダンジョン（ENCOUNTER_ZONES）。仲間の人数は encounter.test.ts と同じ決め方。 */
function dungeonRateAt(id: string, level: number): number {
  const zone = ENCOUNTER_ZONES[id];
  const companions = zone.level <= 5 ? 1 : zone.level <= 7 ? 2 : zone.level <= 9 ? 3 : zone.level <= 15 ? 4 : 5;
  let n = 0;
  return winRate(partyAtLevel(level, companions), () => createEncounterEnemies(id, zone, createRng(n++ * 7 + 1), companions), 300).rate;
}

describe("ダンジョンの敵のバランス（想定より4レベル低くても詰まらない）", () => {
  for (const [id, zone] of Object.entries(ENCOUNTER_ZONES)) {
    it(`${id}（想定Lv${zone.level}）`, () => {
      expect(dungeonRateAt(id, Math.max(1, zone.level - 4))).toBeGreaterThanOrEqual(0.4);
    });
  }
});
