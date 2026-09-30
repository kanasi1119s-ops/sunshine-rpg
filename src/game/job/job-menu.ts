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

export function moveJobMenu(state: JobMenuState, delta: number, memberCount: number): JobMenuState {
  if (!state.open) {
    return state;
  }
  if (state.stage === "member") {
    const n = Math.max(1, memberCount);
    return { ...state, memberCursor: (state.memberCursor + delta + n) % n };
  }
  const n = INITIAL_JOBS.length;
  return { ...state, jobCursor: (state.jobCursor + delta + n) % n };
}

/** 決定。仲間を選んだらジョブ選択へ進み、ジョブを選んだら選ばれたジョブIDを返す。 */
export function confirmJobMenu(state: JobMenuState): { state: JobMenuState; chosen?: JobId } {
  if (!state.open) {
    return { state };
  }
  if (state.stage === "member") {
    return { state: { ...state, stage: "job", jobCursor: 0 } };
  }
  return { state: { ...state, stage: "member" }, chosen: INITIAL_JOBS[state.jobCursor].id };
}

/** キャンセル。ジョブ選択なら仲間選択に戻り、仲間選択なら閉じる。 */
export function cancelJobMenu(state: JobMenuState): JobMenuState {
  if (!state.open) {
    return state;
  }
  return state.stage === "job" ? { ...state, stage: "member" } : { ...state, open: false };
}
