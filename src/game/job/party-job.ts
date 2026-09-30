import { applyStatBonus } from "../items/equipment";
import type { LeveledStats } from "../growth/types";
import { computeJobBonus, equipJob, gainMastery, createJobState } from "./mastery";
import type { JobId, JobState } from "./types";

/** このフラグが立つと、ジョブチェンジ機能が使える（第6章でアヤメが仲間に加わったとき）。 */
export const JOB_UNLOCK_FLAG = "chapter6_ayame_joined";

/** ジョブ画面に並べるキャラクター（主人公は "hero"）。 */
export function isJobSystemUnlocked(flags: Record<string, boolean | undefined>): boolean {
  return flags[JOB_UNLOCK_FLAG] === true;
}

/** 戦闘用の能力値に、装備中ジョブのボーナスを足す。ジョブ未装備・機能未解禁ならそのまま返す。 */
export function withJobBonus(
  stats: LeveledStats,
  state: JobState | undefined,
  unlocked: boolean,
): LeveledStats {
  if (!unlocked || !state?.equipped) {
    return stats;
  }
  return applyStatBonus(stats, computeJobBonus(state));
}

/** 戦闘に勝ったとき、その戦闘に出た全員の装備中ジョブの熟練度経験値を増やす（数値は仮）。 */
export function masteryFromVictoryExp(expGained: number): number {
  return Math.max(1, Math.round(expGained / 2));
}

export function awardVictoryMastery(
  states: Record<string, JobState>,
  memberIds: string[],
  expGained: number,
): Record<string, JobState> {
  const amount = masteryFromVictoryExp(expGained);
  const next = { ...states };
  for (const id of memberIds) {
    const state = next[id];
    if (state) {
      next[id] = gainMastery(state, amount);
    }
  }
  return next;
}

/** ジョブ画面で選ぶ。まだ状態を持たないキャラクターには新しい状態を作る。 */
export function changeJob(
  states: Record<string, JobState>,
  memberId: string,
  jobId: JobId,
): Record<string, JobState> {
  return { ...states, [memberId]: equipJob(states[memberId] ?? createJobState(), jobId) };
}
