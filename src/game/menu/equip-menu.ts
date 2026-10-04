/**
 * そうび画面（メニューの「そうび」）。誰の → どの部位を → どの品を、の3段で選ぶ。
 * 画面遷移と選択位置だけを持つ。実際に装備を入れかえる処理は main.ts が行う。
 *  - "member": 仲間の中から選ぶ
 *  - "slot":   ぶき・ぼうぐ・かざり から選ぶ
 *  - "item":   持っている品（先頭は「はずす」）から選ぶ
 */
export type EquipStage = "member" | "slot" | "item";

export interface EquipMenuState {
  open: boolean;
  stage: EquipStage;
  member: number;
  slot: number;
  item: number;
}

export function createEquipMenuState(): EquipMenuState {
  return { open: false, stage: "member", member: 0, slot: 0, item: 0 };
}

export function openEquipMenu(): EquipMenuState {
  return { open: true, stage: "member", member: 0, slot: 0, item: 0 };
}

export interface EquipCounts {
  members: number;
  slots: number;
  /** 「はずす」を含む、選べる数。 */
  items: number;
}

function wrap(value: number, delta: number, count: number): number {
  return count <= 0 ? 0 : (value + delta + count) % count;
}

export function moveEquipCursor(state: EquipMenuState, delta: number, counts: EquipCounts): EquipMenuState {
  if (!state.open) return state;
  switch (state.stage) {
    case "member":
      return { ...state, member: wrap(state.member, delta, counts.members) };
    case "slot":
      return { ...state, slot: wrap(state.slot, delta, counts.slots) };
    default:
      return { ...state, item: wrap(state.item, delta, counts.items) };
  }
}

/** 決定。「item」で決定したときは apply を返す（入れかえは呼び出し側）。 */
export function confirmEquipMenu(state: EquipMenuState): { state: EquipMenuState; apply: boolean } {
  if (!state.open) return { state, apply: false };
  if (state.stage === "member") return { state: { ...state, stage: "slot", slot: 0 }, apply: false };
  if (state.stage === "slot") return { state: { ...state, stage: "item", item: 0 }, apply: false };
  return { state: { ...state, stage: "slot" }, apply: true };
}

/** もどる: item→slot→member→閉じる。 */
export function backEquipMenu(state: EquipMenuState): EquipMenuState {
  if (!state.open) return state;
  if (state.stage === "item") return { ...state, stage: "slot" };
  if (state.stage === "slot") return { ...state, stage: "member" };
  return { ...state, open: false };
}
