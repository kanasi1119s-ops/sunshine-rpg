/**
 * 戦闘のメッセージ（ログ1行）から、画面に出す短い演出を決める。
 * 味方がダメージを受けたら画面がゆれ、敵に当てたら敵が白く光り、回復は緑に光る。
 * 効果音（`battle-se.ts`）と同じく、メッセージが出るたびに1回だけ始める。
 */
export type BattleEffectKind = "shake" | "hit" | "crit" | "heal" | "down";

export interface BattleEffect {
  kind: BattleEffectKind;
  /** 演出の長さ（ミリ秒） */
  duration: number;
}

const DURATIONS: Record<BattleEffectKind, number> = {
  shake: 260,
  hit: 180,
  crit: 320,
  heal: 380,
  down: 300,
};

export function battleEffectFor(text: string, partyNames: string[]): BattleEffect | null {
  const make = (kind: BattleEffectKind): BattleEffect => ({ kind, duration: DURATIONS[kind] });
  if (text.includes("のHPが") && text.includes("回復した")) {
    return make("heal");
  }
  const killed = /^(.+) を倒した！$/.exec(text);
  if (killed) {
    return partyNames.includes(killed[1]) ? null : make("down");
  }
  const damage = /^(.+?) の(.+?)！ (?:会心の一撃！ )?(.+) に \d+ のダメージ$/.exec(text);
  if (damage) {
    if (partyNames.includes(damage[3])) {
      return make("shake");
    }
    return make(text.includes("会心の一撃") ? "crit" : "hit");
  }
  return null;
}

/** 演出の経過（0〜1）から、画面のゆれ幅（ピクセル）を返す。だんだん小さくなる。 */
export function shakeOffset(progress: number, elapsedMs: number): number {
  if (progress >= 1) {
    return 0;
  }
  const amplitude = 4 * (1 - progress);
  return Math.round(Math.sin(elapsedMs / 16) * amplitude);
}
