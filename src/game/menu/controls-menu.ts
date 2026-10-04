import { CONTROL_ACTIONS, type ControlAction } from "../../input/key-bindings";

/**
 * 「そうさ設定」画面（タイトル・メニューから開く）。動作を選んで決定→新しいキーを押す、で割り当てを変える。
 * 画面遷移と選択位置だけを持つ。キーの受けとりと保存は main.ts が行う。
 */
export interface ControlsMenuState {
  open: boolean;
  cursor: number;
  /** 新しいキーを待っているか（待っている間は、押したキーが設定になる）。 */
  capturing: boolean;
  message: string | null;
}

/** 動作の行 + 「もとにもどす」 + 「とじる」。 */
export const CONTROLS_ROW_COUNT = CONTROL_ACTIONS.length + 2;

export function createControlsMenuState(): ControlsMenuState {
  return { open: false, cursor: 0, capturing: false, message: null };
}

export function openControlsMenu(): ControlsMenuState {
  return { open: true, cursor: 0, capturing: false, message: null };
}

export function moveControlsCursor(state: ControlsMenuState, delta: number): ControlsMenuState {
  if (!state.open || state.capturing) return state;
  return { ...state, cursor: (state.cursor + delta + CONTROLS_ROW_COUNT) % CONTROLS_ROW_COUNT, message: null };
}

export type ControlsChoice = { kind: "capture"; action: ControlAction } | { kind: "reset" } | { kind: "close" } | null;

export function confirmControlsMenu(state: ControlsMenuState): { state: ControlsMenuState; choice: ControlsChoice } {
  if (!state.open || state.capturing) return { state, choice: null };
  if (state.cursor < CONTROL_ACTIONS.length) {
    return { state: { ...state, capturing: true, message: null }, choice: { kind: "capture", action: CONTROL_ACTIONS[state.cursor].id } };
  }
  if (state.cursor === CONTROL_ACTIONS.length) return { state: { ...state, message: "もとの操作にもどした" }, choice: { kind: "reset" } };
  return { state: { ...state, open: false }, choice: { kind: "close" } };
}

export function finishCapture(state: ControlsMenuState, message: string | null): ControlsMenuState {
  return { ...state, capturing: false, message };
}

export function closeControlsMenu(state: ControlsMenuState): ControlsMenuState {
  return { ...state, open: false, capturing: false, message: null };
}
