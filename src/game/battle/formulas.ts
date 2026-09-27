const CRITICAL_CHANCE = 0.0625;
const VARIANCE_MIN = 0.9;
const VARIANCE_RANGE = 0.2;

export interface DamageResult {
  amount: number;
  critical: boolean;
}

export function computeDamage(
  attack: number,
  defense: number,
  powerMultiplier: number,
  rng: () => number,
): DamageResult {
  const base = Math.max(1, attack * powerMultiplier - defense / 2);
  const variance = VARIANCE_MIN + rng() * VARIANCE_RANGE;
  const critical = rng() < CRITICAL_CHANCE;
  const amount = Math.max(1, Math.round(base * variance * (critical ? 2 : 1)));
  return { amount, critical };
}

export function computeFleeChance(partySpeed: number, enemySpeed: number): number {
  const chance = 0.5 + (partySpeed - enemySpeed) / 100;
  return Math.min(0.9, Math.max(0.1, chance));
}
