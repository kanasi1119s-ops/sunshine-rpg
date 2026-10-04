/**
 * 戦闘に入るときの演出。ふつうの戦闘は短い（画面がひらめいて、うずまくように暗くなり、戦闘画面がひらく）。
 * ボス・強敵（ストーリーの戦闘）は長い特別な登場（画面がゆれ、黒い帯が入り、名前が出て、白くひらめいて戦闘へ）。
 * 時間の進みだけを持つ。絵は `render/battle-transition-renderer.ts`。
 */
export interface BattleTransition {
  /** 経過時間（ms）。 */
  ms: number;
  boss: boolean;
  /** ボスの名前（ボス登場のときだけ）。 */
  name: string;
}

/** 演出の前半（フィールドの絵の上に重ねる）の長さ（ms）。 */
export const COVER_MS = { normal: 560, boss: 2800 } as const;
/** 後半（戦闘画面がひらいていく）の長さ（ms）。 */
export const REVEAL_MS = { normal: 360, boss: 700 } as const;

export function startBattleTransition(boss: boolean, name = ""): BattleTransition {
  return { ms: 0, boss, name };
}

export function coverMs(t: BattleTransition): number {
  return t.boss ? COVER_MS.boss : COVER_MS.normal;
}

export function totalMs(t: BattleTransition): number {
  return coverMs(t) + (t.boss ? REVEAL_MS.boss : REVEAL_MS.normal);
}

/** 前半（フィールドを見せている間）か。 */
export function isCoverPhase(t: BattleTransition): boolean {
  return t.ms < coverMs(t);
}

/** 進める。終わったら null。 */
export function advanceBattleTransition(t: BattleTransition, dtMs: number): BattleTransition | null {
  const next = { ...t, ms: t.ms + dtMs };
  return next.ms >= totalMs(next) ? null : next;
}

/** 決定ボタンでとばせるか（ふつうの戦闘は短いのでとばさない。ボス登場は、名前が出たあとなら）。 */
export function canSkipTransition(t: BattleTransition): boolean {
  return t.boss && t.ms > 900;
}

/** とばす: 前半の終わりまで進める。 */
export function skipToReveal(t: BattleTransition): BattleTransition {
  return isCoverPhase(t) ? { ...t, ms: coverMs(t) } : t;
}
