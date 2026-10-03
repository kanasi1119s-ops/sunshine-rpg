import { describe, expect, it } from "vitest";
import {
  shapeForName,
  createEncounterState,
  ENCOUNTER_ZONES,
  encounterMonsterSpecs,
  enemyStatsForLevel,
  MAX_STEPS,
  MIN_STEPS,
  stepEncounter,
  WORLD_ENCOUNTER_ZONES,
  worldZoneIdAt,
} from "./encounter";
import { MONSTERS } from "../monster/monsters";
import { WORLD_MAPS } from "../world/world";
import { createRng } from "../random";
import { partyAtLevel, winRate } from "../battle/balance-helpers";

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

  it("想定レベルが上がるほど、敵の体力・攻撃・経験値は大きくなる", () => {
    for (let level = 2; level < 36; level += 2) {
      const a = enemyStatsForLevel(level);
      const b = enemyStatsForLevel(level + 2);
      expect(b.maxHp).toBeGreaterThan(a.maxHp);
      expect(b.attack).toBeGreaterThan(a.attack);
      expect(b.expReward).toBeGreaterThan(a.expReward);
    }
  });

  it("各地の敵は、その場所の想定レベルのパーティが、1〜3体の一団に高い確率で勝てる強さ（最悪の3体の一団でも90%以上）", () => {
    for (const [mapId, zone] of Object.entries(ENCOUNTER_ZONES)) {
      const companions = zone.level <= 5 ? 1 : zone.level <= 7 ? 2 : zone.level <= 9 ? 3 : zone.level <= 15 ? 4 : 5;
      const party = partyAtLevel(zone.level, companions);
      const stats = enemyStatsForLevel(zone.level);
      const group = (n: number) => () =>
        Array.from({ length: n }, (_, i) => ({
          id: `e${i}`, name: `e${i}`, maxHp: stats.maxHp, hp: stats.maxHp, maxMp: 0, mp: 0,
          attack: stats.attack, defense: stats.defense, speed: stats.speed, isEnemy: true, guarding: false,
        }));
      const worst = winRate(party, group(zone.level <= 6 ? 2 : 3), 100);
      expect(worst.rate, `${mapId}（Lv${zone.level}）の勝率 ${(worst.rate * 100).toFixed(0)}%`).toBeGreaterThanOrEqual(0.9);
      expect(worst.hpRatio, `${mapId} の戦闘後の残りHP ${(worst.hpRatio * 100).toFixed(0)}%`).toBeLessThanOrEqual(0.9);
    }
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

describe("雑魚の絵の形（名前の言葉から決まる）", () => {
  it("言葉に合う形になる", () => {
    expect(shapeForName("監視の目", 0)).toBe("eye");
    expect(shapeForName("砂サソリの影", 0)).toBe("scorpion");
    expect(shapeForName("野ねずみの影", 0)).toBe("rat");
    expect(shapeForName("採掘跡のこうもり", 0)).toBe("bat");
    expect(shapeForName("灯り石の虫", 0)).toBe("beetle");
    expect(shapeForName("光の結晶", 0)).toBe("shard");
    expect(shapeForName("水のしずく影", 0)).toBe("drop");
    expect(shapeForName("たゆたう影", 0)).toBe("ghost");
  });

  it("どの地方の敵の名前も、手描きの絵がある形（blob以外）に決まる、または理由のあるblob", () => {
    const names = Object.values(ENCOUNTER_ZONES).flatMap((z) => z.names.map((n, i) => shapeForName(n, i)));
    const withArt = names.filter((shape) => shape !== "blob").length;
    expect(withArt / names.length).toBeGreaterThan(0.85);
  });
});

describe("世界地図のエンカウント", () => {
  it("道の上では出会わず、地形と位置で地方が決まる", () => {
    expect(worldZoneIdAt(7, 10)).toBeNull();
    expect(worldZoneIdAt(2, 10)).toBe("world-1");
    expect(worldZoneIdAt(2, 50)).toBe("world-2");
    expect(worldZoneIdAt(2, 150, 40)).toBe("world-4");
    expect(worldZoneIdAt(2, 150, 140)).toBe("world-6");
    expect(worldZoneIdAt(18, 196, 170)).toBe("world-5");
    expect(worldZoneIdAt(5, 10)).toBe("world-3");
    expect(worldZoneIdAt(6, 10)).toBe("world-4");
  });

  it("世界地図の敵も、手描きの絵がある形で、絵の一覧に入る", () => {
    const specs = encounterMonsterSpecs();
    for (const [id, zone] of Object.entries(WORLD_ENCOUNTER_ZONES)) {
      for (let v = 0; v < zone.names.length; v++) {
        expect(specs[`enc-${id}-${v}`], `${id}-${v}`).toBeDefined();
        expect(shapeForName(zone.names[v], v)).not.toBe("blob");
      }
    }
  });

  it("世界地図の地方でも、歩いていれば出会う", () => {
    const rng = createRng(5);
    let state = createEncounterState(rng);
    let met = false;
    for (let i = 0; i < MAX_STEPS + 2 && !met; i++) {
      const r = stepEncounter(state, "world-2", rng);
      state = r.state;
      met = !!r.enemies;
    }
    expect(met).toBe(true);
  });
});
