import type { SlotSummary } from "../save/slots";
import type { SaveSlotId } from "../save/storage";

/**
 * セーブ・ロードの場所えらび（5か所＋ロードのときは自動セーブ）。上下で選び、決定で実行、Xでもどる。
 * 実際のセーブ・ロードは main.ts が行う。
 */
export interface SlotMenuState {
  open: boolean;
  mode: "save" | "load";
  rows: SlotSummary[];
  cursor: number;
  message: string | null;
}

export function createSlotMenuState(): SlotMenuState {
  return { open: false, mode: "load", rows: [], cursor: 0, message: null };
}

export function openSlotMenu(mode: "save" | "load", rows: SlotSummary[]): SlotMenuState {
  const first = rows.findIndex((r) => mode === "save" || !r.empty);
  return { open: true, mode, rows, cursor: Math.max(0, first), message: rows.every((r) => r.empty) && mode === "load" ? "セーブデータが ありません" : null };
}

export function moveSlotCursor(state: SlotMenuState, delta: number): SlotMenuState {
  if (!state.open || state.rows.length === 0) return state;
  return { ...state, cursor: (state.cursor + delta + state.rows.length) % state.rows.length, message: null };
}

/** 決定。ロードで、からっぽの場所は選べない。 */
export function confirmSlot(state: SlotMenuState): SaveSlotId | null {
  const row = state.rows[state.cursor];
  if (!state.open || !row) return null;
  if (state.mode === "load" && row.empty) return null;
  return row.id;
}

export function closeSlotMenu(state: SlotMenuState): SlotMenuState {
  return { ...state, open: false, message: null };
}

export function withSlotRows(state: SlotMenuState, rows: SlotSummary[], message: string | null): SlotMenuState {
  return { ...state, rows, message };
}
