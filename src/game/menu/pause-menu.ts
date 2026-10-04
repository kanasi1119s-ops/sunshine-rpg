/**
 * ゲーム中のメニュー（Escape／Tab、スマホは「メニュー」ボタン）。つよさの確認・セーブ・タイトルへ戻る。
 * 画面遷移だけを持つ。実際のセーブやタイトルへ戻る処理は main.ts が行う。
 */
export type PauseScreen = "main" | "status";
export type PauseAction = "save" | "title" | "equip" | "keys" | null;

export interface PauseMenuState {
  open: boolean;
  screen: PauseScreen;
  cursor: number;
}

export const PAUSE_ITEMS: { id: "status" | "equip" | "keys" | "save" | "title" | "close"; label: string }[] = [
  { id: "status", label: "つよさ" },
  { id: "equip", label: "そうび" },
  { id: "keys", label: "そうさ設定" },
  { id: "save", label: "セーブする" },
  { id: "title", label: "タイトルへ戻る" },
  { id: "close", label: "とじる" },
];

export function createPauseMenuState(): PauseMenuState {
  return { open: false, screen: "main", cursor: 0 };
}

export function openPauseMenu(): PauseMenuState {
  return { open: true, screen: "main", cursor: 0 };
}

export function movePauseCursor(state: PauseMenuState, delta: number): PauseMenuState {
  if (!state.open || state.screen !== "main") {
    return state;
  }
  return { ...state, cursor: (state.cursor + delta + PAUSE_ITEMS.length) % PAUSE_ITEMS.length };
}

export function confirmPauseMenu(state: PauseMenuState): { state: PauseMenuState; action: PauseAction } {
  if (!state.open) {
    return { state, action: null };
  }
  if (state.screen === "status") {
    return { state: { ...state, screen: "main" }, action: null };
  }
  switch (PAUSE_ITEMS[state.cursor].id) {
    case "status":
      return { state: { ...state, screen: "status" }, action: null };
    case "equip":
      return { state, action: "equip" };
    case "keys":
      return { state, action: "keys" };
    case "save":
      return { state, action: "save" };
    case "title":
      return { state: { ...state, open: false }, action: "title" };
    default:
      return { state: { ...state, open: false }, action: null };
  }
}

/** 戻る（Xキー・Escape）: つよさ画面ならメニューへ、メニューなら閉じる。 */
export function backPauseMenu(state: PauseMenuState): PauseMenuState {
  if (!state.open) {
    return state;
  }
  return state.screen === "status" ? { ...state, screen: "main" } : { ...state, open: false };
}
