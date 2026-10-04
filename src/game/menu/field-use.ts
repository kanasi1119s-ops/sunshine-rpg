import type { Skill } from "../battle/types";

/**
 * フィールドで「どうぐ」（回復アイテム）と「まほう」（回復魔法）を使う画面の状態。
 * 一覧から選び（pick）、だれに使うか選ぶ（target）。全員に効く魔法は、対象を選ばない。
 * 実際に回復する処理は main.ts が行う（この中は選択位置だけ）。
 */
export type FieldUseMode = "items" | "spells";

export interface FieldUseOption {
  key: string;
  label: string;
  note: string;
  /** どうぐ: 品のID。 */
  itemId?: string;
  /** まほう: 使う人と、特技。 */
  casterId?: string;
  skill?: Skill;
}

export interface FieldUseState {
  open: boolean;
  mode: FieldUseMode;
  options: FieldUseOption[];
  stage: "pick" | "target";
  cursor: number;
  targetCursor: number;
  message: string | null;
}

export function createFieldUseState(): FieldUseState {
  return { open: false, mode: "items", options: [], stage: "pick", cursor: 0, targetCursor: 0, message: null };
}

export function openFieldUse(mode: FieldUseMode, options: FieldUseOption[]): FieldUseState {
  return { open: true, mode, options, stage: "pick", cursor: 0, targetCursor: 0, message: options.length === 0 ? (mode === "items" ? "つかえる どうぐを もっていない" : "つかえる まほうが ない") : null };
}

export function moveFieldUse(state: FieldUseState, delta: number, memberCount: number): FieldUseState {
  if (!state.open) return state;
  if (state.stage === "target") {
    return { ...state, targetCursor: (state.targetCursor + delta + memberCount) % Math.max(1, memberCount), message: null };
  }
  if (state.options.length === 0) return state;
  return { ...state, cursor: (state.cursor + delta + state.options.length) % state.options.length, message: null };
}

/** 全員に効く魔法か（対象を選ばない）。 */
export function isAllTargets(option: FieldUseOption | undefined): boolean {
  return option?.skill?.effect === "healAll";
}

export type FieldUseApply = { option: FieldUseOption; targetIndex: number | null };

/** 決定。一覧なら対象選びへ（全員魔法はすぐ使う）、対象選びなら使う。 */
export function confirmFieldUse(state: FieldUseState): { state: FieldUseState; apply: FieldUseApply | null } {
  if (!state.open) return { state, apply: null };
  const option = state.options[state.cursor];
  if (!option) return { state, apply: null };
  if (state.stage === "pick") {
    if (isAllTargets(option)) return { state, apply: { option, targetIndex: null } };
    return { state: { ...state, stage: "target", targetCursor: 0, message: null }, apply: null };
  }
  return { state, apply: { option, targetIndex: state.targetCursor } };
}

/** もどる。対象選び→一覧、一覧→閉じる。 */
export function backFieldUse(state: FieldUseState): FieldUseState {
  if (!state.open) return state;
  if (state.stage === "target") return { ...state, stage: "pick", message: null };
  return { ...state, open: false, message: null };
}

/** 使ったあとの一覧に作りなおす（数が減る・なくなる）。カーソルは範囲に収める。 */
export function refreshFieldUse(state: FieldUseState, options: FieldUseOption[], message: string): FieldUseState {
  return { ...state, options, cursor: Math.min(state.cursor, Math.max(0, options.length - 1)), stage: options.length === 0 ? "pick" : state.stage, message };
}
