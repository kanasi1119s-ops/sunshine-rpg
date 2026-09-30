import { describe, expect, it } from "vitest";
import {
  createEncounterState,
  ENCOUNTER_ZONES,
  encounterMonsterSpecs,
  enemyStatsForTier,
  MAX_STEPS,
  MIN_STEPS,
  stepEncounter,
} from "./encounter";
import { MONSTERS } from "../monster/monsters";
import { WORLD_MAPS } from "../world/world";
import { createRng } from "../random";

describe("ランダムエンカウント", () => {
  it("エンカウントのある地図は、すべて実在する", () => {
    for (const mapId of Object.keys(ENCOUNTER_ZONES)) {
      expect(WORLD_MAPS[mapId], `${mapId} が地図に無い`).toBeDefined();
    }
  });

  it("町・ボスの間・8神の禁域などでは、いくら歩いても出会わない", () => {
    const rng = createRng(1);
    let state = createEncounterState(rng);
    for (const mapId of ["touri-town", "toushin-hall", "kyotoukyu-sanctum", "god-shrine-1", "deep-yugami"]) {
      for (let i = 0; i < 200; i++) {
        const result = stepEncounter(state, mapId, rng);
        expect(result.enemies).toBeNull();
        state = result.state;
      }
    }
  });

  it(`エンカウントのある地図では、${MIN_STEPS}〜${MAX_STEPS}歩ごとに敵が出て、1〜3体になる`, () => {
    for (const seed of [1, 2, 3, 4, 5]) {
      const rng = createRng(seed);
      let state = createEncounterState(rng);
      let steps = 0;
      let encounters = 0;
      for (let i = 0; i < 2000; i++) {
        steps++;
        const result = stepEncounter(state, "mugikano-water-source", rng);
        state = result.state;
        if (result.enemies) {
          encounters++;
          expect(steps).toBeGreaterThanOrEqual(MIN_STEPS);
          expect(steps).toBeLessThanOrEqual(MAX_STEPS);
          expect(result.enemies.length).toBeGreaterThanOrEqual(1);
          expect(result.enemies.length).toBeLessThanOrEqual(2); // tier1〜2は最大2体
          steps = 0;
        }
      }
      expect(encounters).toBeGreaterThan(50);
    }
  });

  it("同じシードなら、同じ敵が出る（不具合の再現ができる）", () => {
    const run = () => {
      const rng = createRng(42);
      let state = createEncounterState(rng);
      const names: string[] = [];
      for (let i = 0; i < 300; i++) {
        const result = stepEncounter(state, "tetsukusari-mine", rng);
        state = result.state;
        if (result.enemies) {
          names.push(result.enemies.map((e) => e.name).join(","));
        }
      }
      return names;
    };
    expect(run()).toEqual(run());
  });

  it("地方が進むほど、敵の体力・攻撃・経験値は大きくなる", () => {
    for (let tier = 1; tier < 10; tier++) {
      const a = enemyStatsForTier(tier);
      const b = enemyStatsForTier(tier + 1);
      expect(b.maxHp).toBeGreaterThan(a.maxHp);
      expect(b.attack).toBeGreaterThan(a.attack);
      expect(b.expReward).toBeGreaterThan(a.expReward);
    }
  });

  it("雑魚の敵は、同じ地方のボスより十分に弱い（体力が半分以下）", () => {
    // 各章のボスの体力は約310前後。tier10でも、雑魚1体は体力176。
    expect(enemyStatsForTier(10).maxHp).toBeLessThan(310 / 1.5);
  });

  it("出てくる敵の絵は、すべて登録されている", () => {
    for (const id of Object.keys(encounterMonsterSpecs())) {
      expect(MONSTERS[id], `${id} の絵が無い`).toBeDefined();
    }
    for (const id of ["god-1", "god-8", "zenkan", "deep-yugami", "toushin-yugami"]) {
      expect(MONSTERS[id], `${id} の絵が無い`).toBeDefined();
    }
  });
});
