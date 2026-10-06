import type { Combatant } from "./types";

/**
 * 戦闘の並び（2026-10-06、人間の指示「戦闘画面の配置なんだけど横2列にしようか。あとなら並び順もかえれるようにしましょう」
 * 「前面は攻撃が強く、後面は防御が強くなるように」）。
 * 並び順の1〜3人目が前列、4人目からが後列。前列はこうげきが上がり、後列はしゅびが上がる。
 */
export const FRONT_ROW_SIZE = 3;
/** 前列のこうげきの倍率。 */
export const FRONT_ATTACK = 1.15;
/** 後列のしゅびの倍率。 */
export const BACK_DEFENSE = 1.2;

export function isFrontRow(index: number): boolean {
  return index < FRONT_ROW_SIZE;
}

/** 並び順（配列の順）にしたがって、前列・後列の強さを足した、新しい配列を返す。 */
export function applyFormation(party: Combatant[]): Combatant[] {
  return party.map((c, i) =>
    isFrontRow(i)
      ? { ...c, attack: Math.round(c.attack * FRONT_ATTACK) }
      : { ...c, defense: Math.round(c.defense * BACK_DEFENSE) },
  );
}

/** ids を、並び順 order にしたがって並べる（order に無い人は、もとの順のまま後ろへ）。 */
export function sortByOrder<T extends { id: string }>(members: T[], order: string[]): T[] {
  const rank = (id: string): number => {
    const k = order.indexOf(id);
    return k < 0 ? order.length + members.findIndex((m) => m.id === id) : k;
  };
  return [...members].sort((a, b) => rank(a.id) - rank(b.id));
}

/** 並び順の i 番目と j 番目を入れかえた、新しい並び順（ids は今の仲間全員の、今の並び）。 */
export function swapOrder(ids: string[], i: number, j: number): string[] {
  const next = [...ids];
  if (i < 0 || j < 0 || i >= next.length || j >= next.length) return next;
  [next[i], next[j]] = [next[j], next[i]];
  return next;
}

/**
 * 戦闘画面で、i 番目の人が立つ場所（ふだんの姿 16×32 の左はしと、足もと）。
 * 横2列: 前列（手前・下）に3人、後列（奥・上）に残り。左が敵に近い。後列は少し右へずらして、前列のあいだから見えるように。
 */
export function allySlot(index: number, screenWidth: number, groundY: number): { leftX: number; feetY: number } {
  const front = isFrontRow(index);
  const c = front ? index : index - FRONT_ROW_SIZE;
  const leftX = screenWidth - 104 + c * 30 + (front ? 0 : 14);
  const feetY = groundY - (front ? 0 : 22);
  return { leftX, feetY };
}
