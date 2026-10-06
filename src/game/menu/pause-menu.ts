/**
 * ゲーム中のメニュー（Escape／Tab、スマホは「メニュー」ボタン）。つよさの確認・セーブ・タイトルへ戻る。
 * 画面遷移だけを持つ。実際のセーブやタイトルへ戻る処理は main.ts が行う。
 */
export type PauseScreen = "main" | "status" | "items" | "order";
export type PauseAction = "save" | "title" | "equip" | "keys" | "use" | "magic" | "unstick" | "swap" | null;

export interface PauseMenuState {
  open: boolean;
  screen: PauseScreen;
  cursor: number;
  /** 「ならびかえ」の画面で、いま指している人（並び順の番号）と、先に選んだ人（入れかえる相手を待っている）。 */
  orderCursor?: number;
  orderPick?: number | null;
}

export const PAUSE_ITEMS: { id: "status" | "items" | "use" | "magic" | "equip" | "order" | "keys" | "save" | "unstick" | "title" | "close"; label: string }[] = [
  { id: "status", label: "つよさ" },
  { id: "items", label: "もちもの" },
  { id: "use", label: "どうぐ" },
  { id: "magic", label: "まほう" },
  { id: "equip", label: "そうび" },
  { id: "order", label: "ならびかえ" },
  { id: "keys", label: "そうさ設定" },
  { id: "save", label: "セーブする" },
  { id: "unstick", label: "動けないとき" },
  { id: "title", label: "タイトルへ戻る" },
  { id: "close", label: "とじる" },
];

export function createPauseMenuState(): PauseMenuState {
  return { open: false, screen: "main", cursor: 0 };
}

export function openPauseMenu(): PauseMenuState {
  return { open: true, screen: "main", cursor: 0 };
}

/** カーソルを動かす。「ならびかえ」の画面では、memberCount 人のあいだを動く。 */
export function movePauseCursor(state: PauseMenuState, delta: number, memberCount = 0): PauseMenuState {
  if (state.open && state.screen === "order" && memberCount > 0) {
    return { ...state, orderCursor: ((state.orderCursor ?? 0) + delta + memberCount) % memberCount };
  }
  if (!state.open || state.screen !== "main") {
    return state;
  }
  return { ...state, cursor: (state.cursor + delta + PAUSE_ITEMS.length) % PAUSE_ITEMS.length };
}

/**
 * 決定。「ならびかえ」の画面では、1人目を選び、2人目を選ぶと入れかえる（action "swap" と、入れかえる2人の番号）。
 * 同じ人をもう一度選ぶと、選ぶのをやめる。
 */
export function confirmPauseMenu(state: PauseMenuState): { state: PauseMenuState; action: PauseAction; swap?: [number, number] } {
  if (!state.open) {
    return { state, action: null };
  }
  if (state.screen === "order") {
    const cur = state.orderCursor ?? 0;
    const pick = state.orderPick ?? null;
    if (pick === null) return { state: { ...state, orderPick: cur }, action: null };
    if (pick === cur) return { state: { ...state, orderPick: null }, action: null };
    return { state: { ...state, orderPick: null }, action: "swap", swap: [pick, cur] };
  }
  if (state.screen === "status" || state.screen === "items") {
    return { state: { ...state, screen: "main" }, action: null };
  }
  switch (PAUSE_ITEMS[state.cursor].id) {
    case "status":
      return { state: { ...state, screen: "status" }, action: null };
    case "items":
      return { state: { ...state, screen: "items" }, action: null };
    case "use":
      return { state, action: "use" };
    case "magic":
      return { state, action: "magic" };
    case "equip":
      return { state, action: "equip" };
    case "order":
      return { state: { ...state, screen: "order", orderCursor: 0, orderPick: null }, action: null };
    case "keys":
      return { state, action: "keys" };
    case "save":
      return { state, action: "save" };
    case "unstick":
      return { state: { ...state, open: false }, action: "unstick" };
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
  if (state.screen === "order" && state.orderPick !== null && state.orderPick !== undefined) {
    return { ...state, orderPick: null };
  }
  return state.screen !== "main" ? { ...state, screen: "main" } : { ...state, open: false };
}
