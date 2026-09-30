import { describe, expect, it } from "vitest";
import { createInitialHeroStats } from "../battle/sample-battle";
import { battleSkillsOf, awardVictoryMastery, changeJob, isJobSystemUnlocked, masteryFromVictoryExp, withJobBonus } from "./party-job";
import { createJobState, equipJob, starsOf } from "./mastery";

describe("ジョブの戦闘への接続", () => {
  it("アヤメ加入前は解禁されず、加入後に解禁される", () => {
    expect(isJobSystemUnlocked({})).toBe(false);
    expect(isJobSystemUnlocked({ chapter6_ayame_joined: true })).toBe(true);
  });

  it("未解禁・未装備なら能力値は変わらず、解禁＋装備でボーナスが乗る", () => {
    const base = createInitialHeroStats();
    const state = equipJob(createJobState(), "sword-guard");
    expect(withJobBonus(base, state, false)).toBe(base);
    expect(withJobBonus(base, createJobState(), true)).toBe(base);
    const boosted = withJobBonus(base, state, true);
    expect(boosted.attack).toBeGreaterThan(base.attack);
    expect(boosted.defense).toBeGreaterThan(base.defense);
  });

  it("勝利で、装備中のジョブだけ熟練度が増える", () => {
    const states = {
      hero: equipJob(createJobState(), "archer"),
      reto: createJobState(),
    };
    const next = awardVictoryMastery(states, ["hero", "reto", "nobody"], 40);
    expect(next.hero.mastery.archer).toBe(masteryFromVictoryExp(40));
    expect(next.reto.mastery).toEqual({});
    expect(states.hero.mastery.archer).toBeUndefined();
  });

  it("経験値が0でも最低1は入り、何度か勝つと☆が上がる", () => {
    expect(masteryFromVictoryExp(0)).toBe(1);
    let states = changeJob({}, "hero", "flame-mage");
    for (let i = 0; i < 10; i++) {
      states = awardVictoryMastery(states, ["hero"], 30);
    }
    expect(starsOf(states.hero, "flame-mage")).toBeGreaterThan(1);
  });

  it("効果つきの特技（全体攻撃・複数回・回復）も、戦闘用の特技として効果の種類が引き継がれる", () => {
    const fist = { equipped: "fist-fighter" as const, mastery: { "fist-fighter": 100000 } };
    const ripple = { equipped: "ripple-mage" as const, mastery: { "ripple-mage": 100000 } };
    const wave = battleSkillsOf({ equipped: "flame-mage" as const, mastery: { "flame-mage": 100000 } }, true).find((x) => x.name === "火照の波");
    expect(wave?.effect).toBe("damageAll");
    const combo = battleSkillsOf(fist, true).find((x) => x.name === "乱れ打ち");
    expect(combo).toMatchObject({ effect: "multi", hits: 3 });
    const heal = battleSkillsOf(ripple, true).find((x) => x.name === "水紋の癒し");
    expect(heal).toMatchObject({ effect: "heal", healRatio: 1.6 });
  });

  it("changeJob は状態のないキャラクターにも装備させる", () => {
    const states = changeJob({}, "mina", "ripple-mage");
    expect(states.mina.equipped).toBe("ripple-mage");
  });

  it("習得済みで戦闘に使える特技だけが、戦闘用の特技になる", () => {
    const learned = { equipped: "flame-mage" as const, mastery: { "flame-mage": 100000 } };
    const names = battleSkillsOf(learned, true).map((x) => x.name);
    expect(names).toContain("火照の灯");
    expect(names).toContain("火照の波");
    expect(names).toContain("火照の奔流");
    expect(battleSkillsOf(learned, false)).toEqual([]);
    expect(battleSkillsOf(undefined, true)).toEqual([]);
    expect(battleSkillsOf(createJobState(), true)).toEqual([]);
  });
});
