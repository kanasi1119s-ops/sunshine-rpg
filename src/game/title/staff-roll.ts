import { CREDIT_LINES } from "./title-text";

/**
 * エンディングのスタッフロール（下から上へ流れる文字）。決定キーで飛ばせる。
 * 仮: 文は簡易。曲は `staff-roll`（`src/audio/catalog.ts`）。
 */
export const STAFF_ROLL_LINES: string[] = [
  "サンシャインRPG（仮題）",
  "",
  "――灯りの相談所の旅は、ここでひとつの終わりを迎えました――",
  "",
  "登場した人たち",
  "ユーリ　　レト　　ミナ",
  "ガイド　　オルカ　　アヤメ",
  "カセン　　エドレア　　ドルン　　ソウイチ",
  "",
  "制作",
  "サンシャインソフトウェア",
  "運営　旭洋平",
  "",
  ...CREDIT_LINES.filter((line) => !line.startsWith("【クレジット】") && !line.startsWith("制作") && !line.startsWith("　　　（運営")),
  "",
  "遊んでくださって、",
  "ほんとうに、ありがとうございました。",
  "",
  "――おわり――",
];

export const STAFF_LINE_HEIGHT = 16;
/** 1秒に進むピクセル数。 */
export const STAFF_SPEED = 22;

export interface StaffRollState {
  open: boolean;
  /** 上へ流れたピクセル数。 */
  offset: number;
}

export function createStaffRollState(): StaffRollState {
  return { open: false, offset: 0 };
}

export function startStaffRoll(): StaffRollState {
  return { open: true, offset: 0 };
}

/** 全体の長さ（画面の高さぶんの余白を含む）。 */
export function staffRollLength(screenHeight: number): number {
  return STAFF_ROLL_LINES.length * STAFF_LINE_HEIGHT + screenHeight;
}

export function updateStaffRoll(state: StaffRollState, dtMs: number, screenHeight: number): StaffRollState {
  if (!state.open) {
    return state;
  }
  const offset = state.offset + (STAFF_SPEED * dtMs) / 1000;
  return offset >= staffRollLength(screenHeight) ? { open: false, offset: 0 } : { open: true, offset };
}

export function skipStaffRoll(): StaffRollState {
  return { open: false, offset: 0 };
}
