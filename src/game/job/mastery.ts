import type { StatBonus } from "../items/equipment";
import { JOBS_BY_ID, MAX_STARS, maxStarsOf } from "./jobs";
import type { JobId, JobSkill, JobState } from "./types";

/** ☆Nに到達するために必要な累計の熟練度経験値。 */
export function masteryExpForStar(star: number): number {
  return star <= 1 ? 0 : Math.floor(6 * Math.pow(star - 1, 2));
}

/** 熟練度経験値から、いま何☆かを求める（1〜max。max は省略で MAX_STARS）。 */
export function starsForExp(exp: number, max = MAX_STARS): number {
  let star = 1;
  while (star < max && masteryExpForStar(star + 1) <= exp) {
    star++;
  }
  return star;
}

export function createJobState(): JobState {
  return { mastery: {} };
}

/** ジョブを装備する。 */
export function equipJob(state: JobState, jobId: JobId): JobState {
  return { ...state, equipped: jobId };
}

/** 装備しているジョブを外す。 */
export function unequipJob(state: JobState): JobState {
  const next = { ...state };
  delete next.equipped;
  return next;
}

/** 戦闘勝利で、装備中のジョブの熟練度経験値を増やす。未装備なら何も変わらない。 */
export function gainMastery(state: JobState, amount: number): JobState {
  if (!state.equipped || amount <= 0) {
    return state;
  }
  const current = state.mastery[state.equipped] ?? 0;
  const max = masteryExpForStar(maxStarsOf(state.equipped));
  return {
    ...state,
    mastery: { ...state.mastery, [state.equipped]: Math.min(current + amount, max) },
  };
}

export function starsOf(state: JobState, jobId: JobId): number {
  return starsForExp(state.mastery[jobId] ?? 0, maxStarsOf(jobId));
}

/**
 * 習得済みの特技。ジョブを外しても使い続けられるので、装備の有無に関係なく全ジョブぶん集める。
 * ☆1の特技があるので、一度でも装備した（熟練度の記録がある）ジョブだけを数える。
 */
export function learnedSkills(state: JobState): JobSkill[] {
  const result: JobSkill[] = [];
  for (const jobId of Object.keys(JOBS_BY_ID) as JobId[]) {
    if (state.mastery[jobId] === undefined && state.equipped !== jobId) continue;
    const stars = starsOf(state, jobId);
    for (const skill of JOBS_BY_ID[jobId].skills) {
      if (stars >= skill.requiredStars) {
        result.push(skill);
      }
    }
  }
  return result;
}

/** 装備中のジョブの能力値ボーナス（基本＋熟練度ぶん）。装備品と同じく「都度計算」する。 */
export function computeJobBonus(state: JobState): StatBonus {
  if (!state.equipped) {
    return {};
  }
  const job = JOBS_BY_ID[state.equipped];
  const stars = starsOf(state, state.equipped);
  const bonus: StatBonus = { ...job.statBonus };
  for (const [key, value] of Object.entries(job.bonusPerStar) as [keyof StatBonus, number][]) {
    bonus[key] = (bonus[key] ?? 0) + value * (stars - 1);
  }
  return bonus;
}
