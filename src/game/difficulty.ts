/**
 * 難易度（モード）の設定。ブラウザに保存する（歩く速さと同じ）。
 *  - イージー: 戦闘が終わると、体力（HP）と魔力（MP）が全員元に戻る。
 *  - ノーマル: 戦闘で受けたダメージ・使った魔力がそのまま残る。宿屋・回復アイテム・回復魔法で戻す。
 */
export type Difficulty = "easy" | "normal";

export const DIFFICULTIES: ReadonlyArray<{ id: Difficulty; label: string; hint: string }> = [
  { id: "easy", label: "イージー", hint: "戦闘のあと、HP・MPが元にもどる" },
  { id: "normal", label: "ノーマル", hint: "ダメージはそのまま。宿屋やどうぐで回復" },
];

export const DEFAULT_DIFFICULTY: Difficulty = "easy";
const STORAGE_KEY = "sunshine-rpg-difficulty";

export function isDifficulty(value: unknown): value is Difficulty {
  return value === "easy" || value === "normal";
}

export function cycleDifficulty(current: Difficulty, delta: number): Difficulty {
  const index = DIFFICULTIES.findIndex((d) => d.id === current);
  return DIFFICULTIES[(index + delta + DIFFICULTIES.length) % DIFFICULTIES.length].id;
}

export function difficultyLabel(d: Difficulty): string {
  return DIFFICULTIES.find((x) => x.id === d)?.label ?? "イージー";
}

export function loadDifficulty(storage: Pick<Storage, "getItem"> | undefined): Difficulty {
  try {
    const text = storage?.getItem(STORAGE_KEY);
    return isDifficulty(text) ? text : DEFAULT_DIFFICULTY;
  } catch {
    return DEFAULT_DIFFICULTY;
  }
}

export function saveDifficulty(storage: Pick<Storage, "setItem"> | undefined, d: Difficulty): void {
  try {
    storage?.setItem(STORAGE_KEY, d);
  } catch {
    // 保存できなくても遊べる
  }
}
