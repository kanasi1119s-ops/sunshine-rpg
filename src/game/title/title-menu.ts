/**
 * タイトル画面（はじめから／つづきから／あそびかた／クレジット）の状態。
 * 「つづきから」は、自動セーブ（`autosave`）があるときだけ選べる。
 */
export type TitleScreen = "menu" | "help" | "credits";
export type TitleItemId = "continue" | "new" | "help" | "credits";
export type TitleAction = "continue" | "new" | null;

export interface TitleState {
  open: boolean;
  screen: TitleScreen;
  cursor: number;
  hasSave: boolean;
}

export const TITLE_ITEMS: { id: TitleItemId; label: string }[] = [
  { id: "continue", label: "つづきから" },
  { id: "new", label: "はじめから" },
  { id: "help", label: "あそびかた" },
  { id: "credits", label: "クレジット" },
];

/** いま選べる項目（セーブが無いときは「つづきから」を出さない）。 */
export function titleItemsFor(hasSave: boolean): { id: TitleItemId; label: string }[] {
  return TITLE_ITEMS.filter((item) => item.id !== "continue" || hasSave);
}

export function createTitleState(hasSave: boolean): TitleState {
  return { open: true, screen: "menu", cursor: 0, hasSave };
}

export function moveTitleCursor(state: TitleState, delta: number): TitleState {
  if (!state.open || state.screen !== "menu") {
    return state;
  }
  const count = titleItemsFor(state.hasSave).length;
  return { ...state, cursor: (state.cursor + delta + count) % count };
}

/** 決定。ゲームを始める項目なら action を返し、タイトルを閉じる。説明・クレジットなら、その画面へ移る（画面の中では、決定で戻る）。 */
export function confirmTitle(state: TitleState): { state: TitleState; action: TitleAction } {
  if (!state.open) {
    return { state, action: null };
  }
  if (state.screen !== "menu") {
    return { state: { ...state, screen: "menu" }, action: null };
  }
  const item = titleItemsFor(state.hasSave)[state.cursor];
  switch (item?.id) {
    case "continue":
      return { state: { ...state, open: false }, action: "continue" };
    case "new":
      return { state: { ...state, open: false }, action: "new" };
    case "help":
      return { state: { ...state, screen: "help" }, action: null };
    case "credits":
      return { state: { ...state, screen: "credits" }, action: null };
    default:
      return { state, action: null };
  }
}

/** 「戻る」（Xキー・Escape）。説明・クレジットからメニューへ戻る。 */
export function backTitle(state: TitleState): TitleState {
  return state.open && state.screen !== "menu" ? { ...state, screen: "menu" } : state;
}
