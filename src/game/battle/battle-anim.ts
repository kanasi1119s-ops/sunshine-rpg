import type { WeaponType } from "../items/types";
import type { BattleState, Combatant } from "./types";

/**
 * 戦闘のメッセージ（ログ1行）から、画面に出す「動き」を決める。
 *  - 味方が攻撃するとき: 武器ごとの動き（剣=ふる／短剣=さす／斧=ふりおろす／槍=つく／弓=矢をはなつ／杖=かざす）。
 *  - 魔法・とくぎ・回復・状態異常: 対象の上に、種類ごとのエフェクト。
 *  - 味方がダメージを受けたとき: 味方がのけぞる。
 * 効果音（`battle-se.ts`）・演出（`battle-effect.ts`）と同じく、メッセージが出るたびに1回だけ始める。
 */
export type WeaponMotion = "slash" | "stab" | "cast" | "shoot" | "chop" | "thrust";
export type FxId = "fire" | "water" | "light" | "wind" | "ice" | "bolt" | "rock" | "burst" | "heal" | "buff" | "debuff" | "sleep" | "poison" | "confuse";

export interface BattleAnimSpec {
  /** 動く味方（敵の行動のときは無い）。 */
  actorId?: string;
  motion: WeaponMotion | null;
  targetIds: string[];
  fx: FxId | null;
  /** 対象が味方で、ダメージを受けた（のけぞる）。 */
  hurt: boolean;
  /** 動き全体の長さ（ミリ秒）。 */
  durationMs: number;
  /** エフェクトが始まる位置（0〜1）。矢は飛んで当たったあと、魔法はかざしたあとに始まる。 */
  fxStart: number;
}

const MOTION_OF_WEAPON: Record<WeaponType, WeaponMotion> = { sword: "slash", dagger: "stab", staff: "cast", bow: "shoot", axe: "chop", spear: "thrust" };
export const MOTION_DURATION: Record<WeaponMotion, number> = { slash: 520, stab: 420, cast: 760, shoot: 760, chop: 620, thrust: 480 };

/** 魔法使い枠。たたかう以外の技は、杖（槍）をかざして唱える動きになる。 */
const CASTERS = new Set(["mina", "ayame"]);

/** とくぎ・魔法の名前から、エフェクトの種類を決める。 */
export function fxForSkillName(name: string): FxId {
  if (/火|炎|灼|業|滅|照/.test(name)) return "fire";
  if (/雷|電/.test(name)) return "bolt";
  if (/氷|霜|凍/.test(name)) return "ice";
  if (/風|疾|颶|刃|矢/.test(name)) return "wind";
  if (/水|雫|波|雨|流|潮|紋/.test(name)) return "water";
  if (/光|灯|閃|断/.test(name)) return "light";
  if (/土|岩|砂|地|鉄/.test(name)) return "rock";
  return "burst";
}

function byName(state: BattleState, name: string): Combatant | undefined {
  return [...state.party, ...state.enemies].find((c) => c.name === name);
}

export function battleAnimFor(text: string, state: BattleState, weaponOf: (id: string) => WeaponType | undefined): BattleAnimSpec | null {
  const make = (p: Partial<BattleAnimSpec> & { targetIds: string[] }): BattleAnimSpec => {
    const motion = p.motion ?? null;
    return { actorId: undefined, motion, fx: null, hurt: false, durationMs: motion ? MOTION_DURATION[motion] : 600, fxStart: motion === "cast" ? 0.4 : motion === "shoot" ? 0.55 : motion ? 0.5 : 0, ...p };
  };
  const allyActor = (name: string): Combatant | undefined => {
    const c = byName(state, name);
    return c && !c.isEnemy ? c : undefined;
  };

  // 味方がダメージを受けた / 敵にダメージを与えた
  const damage = /^(.+?) の(.+?)！ (?:会心の一撃！ )?(.+) に \d+ のダメージ$/.exec(text);
  if (damage) {
    const [, actorName, skillName, targetName] = damage;
    const actor = allyActor(actorName);
    const target = byName(state, targetName);
    if (!target) return null;
    if (!actor) {
      // 敵の攻撃: 味方がのけぞる
      return target.isEnemy ? null : make({ targetIds: [target.id], hurt: true, durationMs: 420 });
    }
    const weapon = weaponOf(actor.id);
    if (skillName === "たたかう") {
      return make({ actorId: actor.id, motion: MOTION_OF_WEAPON[weapon ?? "sword"], targetIds: [target.id] });
    }
    const caster = CASTERS.has(actor.id);
    return make({
      actorId: actor.id,
      motion: caster ? "cast" : MOTION_OF_WEAPON[weapon ?? "sword"],
      targetIds: [target.id],
      fx: fxForSkillName(skillName),
    });
  }

  // 回復の魔法
  const heal = /^(.+?) の(.+?)！ (.+) のHPが \d+ 回復した$/.exec(text);
  if (heal) {
    const actor = allyActor(heal[1]);
    const target = byName(state, heal[3]);
    if (!target) return null;
    return make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "heal" });
  }
  // どうぐ
  const item = /^(.+?) は (.+?) を使った。(.+?) の/.exec(text);
  if (item) {
    const target = byName(state, item[3]);
    return target ? make({ targetIds: [target.id], fx: "heal", durationMs: 600, fxStart: 0 }) : null;
  }
  // 強化・弱体
  const mod = /^(.+?) の(.+?)！ (.+) の(?:こうげき|しゅび|すばやさ)が(上がった|下がった)$/.exec(text);
  if (mod) {
    const actor = allyActor(mod[1]);
    const target = byName(state, mod[3]);
    if (!target) return null;
    return make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: mod[4] === "上がった" ? "buff" : "debuff" });
  }
  // 状態異常
  const sleepy = /^(?:(.+?) の(.+?)！ )?(.+) は眠ってしまった$/.exec(text);
  if (sleepy) {
    const target = byName(state, sleepy[3]);
    const actor = sleepy[1] ? allyActor(sleepy[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "sleep" }) : null;
  }
  const poisoned = /^(?:(.+?) の(.+?)！ )?(.+) は毒におかされた！$/.exec(text);
  if (poisoned) {
    const target = byName(state, poisoned[3]);
    const actor = poisoned[1] ? allyActor(poisoned[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "poison" }) : null;
  }
  const confused = /^(?:(.+?) の(.+?)！ )?(.+) は混乱した！$/.exec(text);
  if (confused) {
    const target = byName(state, confused[3]);
    const actor = confused[1] ? allyActor(confused[1]) : undefined;
    return target ? make({ actorId: actor?.id, motion: actor ? "cast" : null, targetIds: [target.id], fx: "confuse" }) : null;
  }
  const poisonDamage = /^(.+) は毒のダメージを受けた/.exec(text);
  if (poisonDamage) {
    const target = byName(state, poisonDamage[1]);
    return target ? make({ targetIds: [target.id], fx: "poison", durationMs: 500, fxStart: 0 }) : null;
  }
  return null;
}
