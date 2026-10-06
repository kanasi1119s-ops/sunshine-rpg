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
        expect(s).toBeGreaterThanOrEqual(1);
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
    // 装備した時点で、☆1の特技を覚えている
    expect(learnedSkills(state).map((s) => s.name)).toEqual(["軽打"]);
    state = gainMastery(state, masteryExpForStar(2));
    state = unequipJob(state);
    expect(learnedSkills(state).map((s) => s.name)).toEqual(["軽打", "二連打"]);
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

import { ADVANCED_JOBS, availableJobs, INITIAL_JOBS as INITIAL, JOBS_BY_ID as JOBS, MAX_STARS as MAX } from "./jobs";

describe("上級ジョブ", () => {
  it("初期ジョブ8種に対応する上級ジョブが8種あり、名前・IDが重ならない", () => {
    expect(ADVANCED_JOBS).toHaveLength(8);
    const ids = [...INITIAL, ...ADVANCED_JOBS].map((j) => j.id);
    expect(new Set(ids).size).toBe(16);
    expect(new Set([...INITIAL, ...ADVANCED_JOBS].map((j) => j.name)).size).toBe(16);
    for (const job of ADVANCED_JOBS) {
      expect(INITIAL.map((j) => j.id)).toContain(job.baseJob);
      expect(JOBS[job.id]).toBe(job);
    }
  });

  it("初期ジョブを最大の☆まで育てると、対応する上級ジョブだけが選べるようになる", () => {
    expect(availableJobs(() => 1)).toHaveLength(8);
    expect(availableJobs((id) => (id === "sword-guard" ? MAX : 1)).map((j) => j.id)).toContain("sword-saint");
    expect(availableJobs((id) => (id === "sword-guard" ? MAX : 1))).toHaveLength(9);
    expect(availableJobs(() => MAX)).toHaveLength(16);
    expect(availableJobs((id) => (id === "sword-guard" ? MAX - 1 : 1))).toHaveLength(8);
  });

  it("上級ジョブは、同じ方向性の初期ジョブより能力値ボーナスが大きく、特技はすべて戦闘で使える", () => {
    for (const job of ADVANCED_JOBS) {
      const base = JOBS[job.baseJob!];
      const total = (b: Record<string, number | undefined>) => Object.values(b).reduce<number>((a, v) => a + (v ?? 0), 0);
      expect(total(job.statBonus)).toBeGreaterThan(total(base.statBonus));
      expect(job.skills.length).toBe(15);
      for (const skill of job.skills) {
        expect(skill.battle, `${job.name} の ${skill.name}`).toBeDefined();
      }
    }
  });
});

import { DIVINE_JOBS } from "./jobs";

describe("天神・悪神ジョブ", () => {
  it("4種あり、対応する神を倒したフラグで、だれでも選べるようになる", () => {
    expect(DIVINE_JOBS.map((j) => j.id).sort()).toEqual(["bug-curser", "demon-breaker", "goddess-shaman", "pure-paladin"]);
    expect(availableJobs(() => 1)).toHaveLength(8);
    const withGods = availableJobs(() => 1, { god1_defeated: true, god3_defeated: true });
    expect(withGods.map((j) => j.id)).toEqual(expect.arrayContaining(["goddess-shaman", "demon-breaker"]));
    expect(withGods).toHaveLength(10);
    expect(availableJobs(() => MAX, { god1_defeated: true, god2_defeated: true, god3_defeated: true, god5_defeated: true })).toHaveLength(20);
  });

  it("どのジョブにも弱点がある（能力値ボーナスに負の値がある）。特技はすべて戦闘で使える", () => {
    for (const job of DIVINE_JOBS) {
      expect(Object.values(job.statBonus).some((v) => (v ?? 0) < 0), `${job.name} に弱点が無い`).toBe(true);
      for (const skill of job.skills) {
        expect(skill.battle, `${job.name} の ${skill.name}`).toBeDefined();
      }
    }
  });

  it("鬼神の破戒者の特技はHPを支払い、蟲神の呪術師には一撃で倒すチャンスがある", () => {
    const demon = DIVINE_JOBS.find((j) => j.id === "demon-breaker")!;
    // 敵を打つ特技は、すべてHPを支払う
    expect(demon.skills.filter((s) => (s.battle?.powerMultiplier ?? 0) > 0).every((s) => (s.battle?.hpCost ?? 0) > 0)).toBe(true);
    const bug = DIVINE_JOBS.find((j) => j.id === "bug-curser")!;
    expect(bug.skills.some((s) => (s.battle?.koChance ?? 0) > 0)).toBe(true);
  });
});

import { LEGEND_JOBS, LEGEND_UNLOCK_FLAGS } from "./jobs";

describe("レジェンドジョブ「灯心継承者」", () => {
  const all = Object.fromEntries(LEGEND_UNLOCK_FLAGS.map((f) => [f, true]));

  it("主人公だけが、条件（本編クリア・仲間4人の寄り道・カセンの手紙）がそろうと選べる", () => {
    expect(availableJobs(() => 1, all, "hero").map((j) => j.id)).toContain("torch-heir");
    expect(availableJobs(() => 1, all, "reto").map((j) => j.id)).not.toContain("torch-heir");
    expect(availableJobs(() => 1, all).map((j) => j.id)).not.toContain("torch-heir");
    for (const missing of LEGEND_UNLOCK_FLAGS) {
      const partial = { ...all, [missing]: false };
      expect(availableJobs(() => 1, partial, "hero").map((j) => j.id), `${missing} が無いのに解放された`).not.toContain("torch-heir");
    }
  });

  it("上級ジョブより1点特化の強さは無い（能力値の合計が、上級ジョブの最大より小さい）。5つの特技はすべて戦闘で使える", () => {
    const total = (b: Record<string, number | undefined>) => Object.values(b).reduce<number>((a, v) => a + (v ?? 0), 0);
    const legend = LEGEND_JOBS[0];
    expect(legend.skills).toHaveLength(15);
    for (const skill of legend.skills) {
      expect(skill.battle).toBeDefined();
    }
    const maxSpecialist = Math.max(...ADVANCED_JOBS.map((j) => Math.max(...Object.values(j.statBonus).map((v) => v ?? 0))));
    expect(Math.max(...Object.values(legend.statBonus).map((v) => v ?? 0))).toBeLessThan(maxSpecialist);
    expect(total(legend.statBonus)).toBeGreaterThan(0);
  });
});

import { DIVINE_MAX_STARS, maxStarsOf } from "./jobs";

describe("ジョブの特技の数（2026-10-06「1ジョブ大して少なくとも15個は覚える」「天神、悪神は☆10までね」）", () => {
  const ALL = Object.values(JOBS);
  it("どのジョブも15個以上の特技を覚え、すべて戦闘で使える。☆ごとに1つ以上覚える", () => {
    for (const job of ALL) {
      expect(job.skills.length, job.name).toBeGreaterThanOrEqual(15);
      for (const skill of job.skills) expect(skill.battle, `${job.name} の ${skill.name}`).toBeDefined();
      for (let star = 1; star <= maxStarsOf(job.id); star++) {
        expect(job.skills.some((s) => s.requiredStars === star), `${job.name} ☆${star}`).toBe(true);
      }
    }
  });
  it("天神・悪神ジョブは☆10まで（特技も☆10までに全部覚える）。ほかは☆15まで", () => {
    for (const job of ALL) {
      const divine = DIVINE_JOBS.includes(job);
      expect(maxStarsOf(job.id), job.name).toBe(divine ? DIVINE_MAX_STARS : MAX);
      expect(Math.max(...job.skills.map((s) => s.requiredStars)), job.name).toBe(maxStarsOf(job.id));
    }
    let state = equipJob(createJobState(), "goddess-shaman");
    state = gainMastery(state, 10 ** 9);
    expect(starsOf(state, "goddess-shaman")).toBe(DIVINE_MAX_STARS);
    expect(learnedSkills(state)).toHaveLength(15);
  });
  it("特技の名前は、全ジョブで重ならない", () => {
    const names = ALL.flatMap((j) => j.skills.map((s) => s.name));
    expect(new Set(names).size).toBe(names.length);
  });
  it("一度も装備していないジョブの☆1の特技は、覚えていない", () => {
    expect(learnedSkills(createJobState())).toHaveLength(0);
  });
});
