/** 歩く速さの設定（そうさ設定で変える。ブラウザに保存）。 */
export const MOVE_SPEEDS = [
  { label: "ゆっくり", factor: 0.75 },
  { label: "ふつう", factor: 1 },
  { label: "はやい", factor: 1.35 },
  { label: "とてもはやい", factor: 1.75 },
] as const;

export const DEFAULT_MOVE_SPEED = 1;
const STORAGE_KEY = "sunshine-rpg-move-speed";

export function cycleMoveSpeed(index: number, delta: number): number {
  return (index + delta + MOVE_SPEEDS.length) % MOVE_SPEEDS.length;
}

export function loadMoveSpeed(storage: Pick<Storage, "getItem"> | undefined): number {
  try {
    const text = storage?.getItem(STORAGE_KEY);
    if (text == null) return DEFAULT_MOVE_SPEED;
    const raw = Number(text);
    return Number.isInteger(raw) && raw >= 0 && raw < MOVE_SPEEDS.length ? raw : DEFAULT_MOVE_SPEED;
  } catch {
    return DEFAULT_MOVE_SPEED;
  }
}

export function saveMoveSpeed(storage: Pick<Storage, "setItem"> | undefined, index: number): void {
  try {
    storage?.setItem(STORAGE_KEY, String(index));
  } catch {
    // 保存できなくても遊べる
  }
}
