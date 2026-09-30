import { INITIAL_JOBS } from "./jobs";
import type { JobId } from "./types";

/** ジョブ画面の状態。まず仲間を選び、次にそのキャラクターのジョブを選ぶ。 */
export interface JobMenuState {
  open: boolean;
  stage: "member" | "job";
  memberCursor: number;
  jobCursor: number;
}

export function createJobMenuState(): JobMenuState {
  return { open: false, stage: "member", memberCursor: 0, jobCursor: 0 };
}

export function openJobMenu(): JobMenuState {
  return { ...createJobMenuState(), open: true };
}

/** `jobCount` は、そのキャラクターがいま選べるジョブの数（初期ジョブ8種＋解放した上級ジョブ）。 */
export function moveJobMenu(state: JobMenuState, delta: number, memberCount: number, jobCount: number = INITIAL_JOBS.length): JobMenuState {
  if (!state.open) {
    return state;
  }
  if (state.stage === "member") {
    const n = Math.max(1, memberCount);
    return { ...state, memberCursor: (state.memberCursor + delta + n) % n };
  }
  const n = Math.max(1, jobCount);
  return { ...state, jobCursor: (state.jobCursor + delta + n) % n };
}

/** 決定。仲間を選んだらジョブ選択へ進み、ジョブを選んだら選ばれたジョブIDを返す。`jobIds` は、いま選べるジョブの並び。 */
export function confirmJobMenu(state: JobMenuState, jobIds: JobId[] = INITIAL_JOBS.map((j) => j.id)): { state: JobMenuState; chosen?: JobId } {
  if (!state.open) {
    return { state };
  }
  if (state.stage === "member") {
    return { state: { ...state, stage: "job", jobCursor: 0 } };
  }
  return { state: { ...state, stage: "member" }, chosen: jobIds[state.jobCursor] };
}

/** キャンセル。ジョブ選択なら仲間選択に戻り、仲間選択なら閉じる。 */
export function cancelJobMenu(state: JobMenuState): JobMenuState {
  if (!state.open) {
    return state;
  }
  return state.stage === "job" ? { ...state, stage: "member" } : { ...state, open: false };
}
