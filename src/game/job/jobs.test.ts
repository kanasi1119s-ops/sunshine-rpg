import { describe, expect, it } from "vitest";
import { INITIAL_JOBS, JOBS_BY_ID, MAX_STARS } from "./jobs";
import {
  computeJobBonus,
  createJobState,
  equipJob,
  gainMastery,
  learnedSkills,
  masteryExpForStar,
  starsForExp,
  starsOf,
  unequipJob,
} from "./mastery";

describe("初期ジョブのデータ", () => {
  it("8種そろっていて、IDと名前が重複しない", () => {
    expect(INITIAL_JOBS).toHaveLength(8);
    expect(new Set(INITIAL_JOBS.map((j) => j.id)).size).toBe(8);
    expect(new Set(INITIAL_JOBS.map((j) => j.name)).size).toBe(8);
  });

  it("特技の習得☆が1〜MAX_STARSで、昇順に並ぶ", () => {
    for (const job of INITIAL_JOBS) {
      expect(job.skills.length).toBeGreaterThan(0);
      const stars = job.skills.map((s) => s.requiredStars);
      expect(stars).toEqual([...stars].sort((a, b) => a - b));
      for (const s of stars) {
        expect(s).toBeGreaterThanOrEqual(2);
        expect(s).toBeLessThanOrEqual(MAX_STARS);
      }
    }
  });

  it("全ジョブの特技名が重複しない", () => {
    const names = INITIAL_JOBS.flatMap((j) => j.skills.map((s) => s.name));
    expect(new Set(names).size).toBe(names.length);
  });

  it("全項目で最強のジョブは無い（各ジョブの基本ボーナスの合計が近い範囲におさまる）", () => {
    const totals = INITIAL_JOBS.map((j) =>
      Object.values(j.statBonus).reduce((sum, v) => sum + (v ?? 0), 0),
    );
    expect(Math.max(...totals) - Math.min(...totals)).toBeLessThanOrEqual(12);
  });
});

describe("熟練度", () => {
  it("経験値と☆が対応する", () => {
    expect(starsForExp(0)).toBe(1);
    expect(starsForExp(masteryExpForStar(2))).toBe(2);
    expect(starsForExp(masteryExpForStar(2) - 1)).toBe(1);
    expect(starsForExp(10 ** 9)).toBe(MAX_STARS);
  });

  it("装備中のジョブにだけ経験値が入る", () => {
    let state = createJobState();
    expect(gainMastery(state, 10)).toEqual(state);
    state = equipJob(state, "archer");
    state = gainMastery(state, 10);
    expect(state.mastery.archer).toBe(10);
    expect(state.mastery["sword-guard"]).toBeUndefined();
  });

  it("経験値は最大☆ぶんで頭打ちになる", () => {
    let state = equipJob(createJobState(), "wanderer");
    state = gainMastery(state, 10 ** 9);
    expect(starsOf(state, "wanderer")).toBe(MAX_STARS);
    expect(state.mastery.wanderer).toBe(masteryExpForStar(MAX_STARS));
  });

  it("特技は習得すると、ジョブを外しても使える", () => {
    let state = equipJob(createJobState(), "fist-fighter");
    expect(learnedSkills(state)).toHaveLength(0);
    state = gainMastery(state, masteryExpForStar(2));
    state = unequipJob(state);
    expect(learnedSkills(state).map((s) => s.name)).toEqual(["二連打"]);
  });

  it("能力値ボーナスは装備中だけ有効で、☆が上がると増える", () => {
    let state = createJobState();
    expect(computeJobBonus(state)).toEqual({});
    state = equipJob(state, "sword-guard");
    expect(computeJobBonus(state)).toEqual({ attack: 3, defense: 3 });
    state = gainMastery(state, masteryExpForStar(3));
    expect(computeJobBonus(state)).toEqual({ attack: 5, defense: 5 });
    expect(computeJobBonus(unequipJob(state))).toEqual({});
  });

  it("JOBS_BY_ID がINITIAL_JOBSと一致する", () => {
    for (const job of INITIAL_JOBS) {
      expect(JOBS_BY_ID[job.id]).toBe(job);
    }
  });
});
