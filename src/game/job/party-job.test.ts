import { describe, expect, it } from "vitest";
import { createInitialHeroStats } from "../battle/sample-battle";
import { awardVictoryMastery, changeJob, isJobSystemUnlocked, masteryFromVictoryExp, withJobBonus } from "./party-job";
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

  it("changeJob は状態のないキャラクターにも装備させる", () => {
    const states = changeJob({}, "mina", "ripple-mage");
    expect(states.mina.equipped).toBe("ripple-mage");
  });
});
