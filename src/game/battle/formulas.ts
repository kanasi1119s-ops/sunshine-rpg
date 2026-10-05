const CRITICAL_CHANCE = 0.0625;
const VARIANCE_MIN = 0.9;
const VARIANCE_RANGE = 0.2;

export interface DamageResult {
  amount: number;
  critical: boolean;
}

/** 会心の一撃の出る確率（運が高いほど出やすい）。 */
export function criticalChance(luck: number): number {
  return Math.min(0.3, Math.max(0.02, CRITICAL_CHANCE + (luck - 5) * 0.005));
}

/** 攻撃がはずれる（ミス）確率。相手の運・すばやさが高いほど、自分が低いほど、はずれやすい。 */
export function missChance(attackerLuck: number, targetLuck: number): number {
  return Math.min(0.2, Math.max(0.02, 0.05 + (targetLuck - attackerLuck) * 0.004));
}

/** すばやさが相手よりこれだけ高いと、1回の攻撃で2回・3回・4回こうげきできる。 */
export const MULTI_ATTACK_GAPS = [12, 24, 40] as const;

/** すばやさの差（自分−相手）から、1回の攻撃での回数（1〜4）。 */
export function attackCount(speedGap: number): number {
  return 1 + MULTI_ATTACK_GAPS.filter((gap) => speedGap >= gap).length;
}

export function computeDamage(
  attack: number,
  defense: number,
  powerMultiplier: number,
  rng: () => number,
  critChance: number = CRITICAL_CHANCE,
): DamageResult {
  const base = Math.max(1, attack * powerMultiplier - defense / 2);
  const variance = VARIANCE_MIN + rng() * VARIANCE_RANGE;
  const critical = rng() < critChance;
  const amount = Math.max(1, Math.round(base * variance * (critical ? 2 : 1)));
  return { amount, critical };
}

export function computeFleeChance(partySpeed: number, enemySpeed: number): number {
  const chance = 0.5 + (partySpeed - enemySpeed) / 100;
  return Math.min(0.9, Math.max(0.1, chance));
}
