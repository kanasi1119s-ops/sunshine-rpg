import type { Combatant } from "../battle/types";
import type { MonsterSpec } from "../monster/monsters";

/**
 * フィールド・ダンジョンでのランダムエンカウント（歩いていると、ときどき「歪みのかけら」に出くわす）。
 * 町・ボスの間・8神の禁域などでは起きない。強さは地方（tier 1〜10）で決まり、章が進むほど敵も経験値も大きくなる。
 * 数値は仮（`docs/design/battle.md`）。ボスより十分に弱く、勝ってレベルを上げるための相手にする。
 */
export interface EncounterZone {
  /** 地方の強さ（1〜10）。 */
  tier: number;
  /** 出てくる敵の名前（3種。出会うたびにこの中から選ぶ）。 */
  names: [string, string, string];
  /** 敵の絵の色相（0〜360）。 */
  hue: number;
}

/** 地図ごとのエンカウント設定。ここに無い地図（町・ボスの間・禁域）では出会わない。 */
export const ENCOUNTER_ZONES: Record<string, EncounterZone> = {
  "touri-outskirts": { tier: 1, names: ["ちいさな歪み", "ゆらぎの影", "野ねずみの影"], hue: 270 },
  "mugikano-water-source": { tier: 1, names: ["水のしずく影", "涸れ田の歪み", "採掘跡のこうもり"], hue: 200 },
  "garasuko-warehouse": { tier: 2, names: ["積荷ねずみ", "湿った歪み", "木箱の影"], hue: 30 },
  "tetsukusari-mine": { tier: 3, names: ["岩かじり", "坑道の影", "灯り石の虫"], hue: 15 },
  "sanone-camp": { tier: 4, names: ["砂ぬけ", "風の影", "砂サソリの影"], hue: 45 },
  "kiri-archive": { tier: 5, names: ["紙魚の影", "霧のささやき", "古文書の虫"], hue: 170 },
  "shimohara-facility": { tier: 6, names: ["霜の歪み", "氷の兵の影", "凍てた機械"], hue: 190 },
  "fushima-base": { tier: 7, names: ["雲の影", "配線の歪み", "監視の目"], hue: 235 },
  "deep-1": { tier: 8, names: ["大乱期の残響", "氷の兵の記憶", "折れた剣の影"], hue: 205 },
  "deep-2": { tier: 8, names: ["静まりの残響", "議場の影", "消えた名前"], hue: 40 },
  "deep-3": { tier: 8, names: ["歪みの断片", "水涸れの残り香", "番人のかけら"], hue: 290 },
  "deep-4": { tier: 8, names: ["初源のしずく", "名前のない影", "悲しみの残響"], hue: 260 },
  "tower-1": { tier: 9, names: ["光の結晶", "生きた石", "青い鉱脈の主"], hue: 205 },
  "tower-2": { tier: 9, names: ["雲路の結晶", "霧の足あと", "風をまとう石"], hue: 215 },
  "tower-3": { tier: 9, names: ["環のかけら", "紋様の影", "光の番兵"], hue: 50 },
  "kanou-1": { tier: 10, names: ["境目の揺らぎ", "迷いの光", "たゆたう影"], hue: 250 },
  "kanou-2": { tier: 10, names: ["静かな影", "待ち人の気配", "緑の光"], hue: 150 },
  "kanou-3": { tier: 10, names: ["裂け目の花", "重なる景色", "薄い境目"], hue: 320 },
  "kanou-4": { tier: 10, names: ["全環のかけら", "白い揺らぎ", "環の残響"], hue: 280 },
};

/** 何歩目で出会うかのふれ幅。 */
export const MIN_STEPS = 12;
export const MAX_STEPS = 26;

export interface EncounterState {
  stepsLeft: number;
}

export function createEncounterState(rng: () => number): EncounterState {
  return { stepsLeft: nextThreshold(rng) };
}

function nextThreshold(rng: () => number): number {
  return MIN_STEPS + Math.floor(rng() * (MAX_STEPS - MIN_STEPS + 1));
}

/** 1歩ぶん進める。出会うとき（歩数が尽きた、かつエンカウントのある地図）は敵の一団を返し、次の歩数を決め直す。 */
export function stepEncounter(state: EncounterState, mapId: string, rng: () => number): { state: EncounterState; enemies: Combatant[] | null } {
  const zone = ENCOUNTER_ZONES[mapId];
  if (!zone) {
    return { state, enemies: null };
  }
  const stepsLeft = state.stepsLeft - 1;
  if (stepsLeft > 0) {
    return { state: { stepsLeft }, enemies: null };
  }
  return { state: { stepsLeft: nextThreshold(rng) }, enemies: createEncounterEnemies(mapId, zone, rng) };
}

/** 強さの目安（1体）。tierが上がるほど、体力・攻撃・経験値が大きくなる。 */
export function enemyStatsForTier(tier: number): { maxHp: number; attack: number; defense: number; speed: number; expReward: number } {
  return {
    maxHp: 16 + tier * 16,
    attack: 6 + tier * 2,
    defense: 2 + Math.floor(tier * 1.1),
    speed: 5 + Math.floor(tier * 0.8),
    expReward: Math.round(12 * Math.pow(tier, 1.5)) + 6,
  };
}

/** 出会うのは1〜3体（tierが低いうちは少なめ）。 */
function createEncounterEnemies(mapId: string, zone: EncounterZone, rng: () => number): Combatant[] {
  const maxCount = zone.tier <= 2 ? 2 : 3;
  const count = 1 + Math.floor(rng() * maxCount);
  const stats = enemyStatsForTier(zone.tier);
  const enemies: Combatant[] = [];
  for (let i = 0; i < count; i++) {
    const variant = Math.floor(rng() * zone.names.length);
    enemies.push({
      id: `enc-${mapId}-${variant}`,
      name: count > 1 ? `${zone.names[variant]}${String.fromCharCode(65 + i)}` : zone.names[variant],
      maxHp: stats.maxHp,
      hp: stats.maxHp,
      maxMp: 0,
      mp: 0,
      attack: stats.attack,
      defense: stats.defense,
      speed: stats.speed,
      isEnemy: true,
      guarding: false,
      expReward: stats.expReward,
    });
  }
  return enemies;
}

/** 色相から、敵の絵の色（`#rrggbb`）を作る。 */
function hslToHex(h: number, s: number, l: number): string {
  const k = (n: number): number => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = (n: number): number => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  const hex = (v: number): string => Math.round(v * 255).toString(16).padStart(2, "0");
  return `#${hex(f(0))}${hex(f(8))}${hex(f(4))}`;
}

/** 敵の絵（手続き的なドット絵）の設計。3種の名前ごとに、とげの数・大きさを少しずつ変える。 */
export function encounterMonsterSpec(zone: EncounterZone, variant: number): MonsterSpec {
  return {
    body: hslToHex(zone.hue, 0.45, 0.32),
    core: hslToHex(zone.hue, 0.5, 0.65),
    eye: variant === 1 ? "#ffe066" : variant === 2 ? "#ff9a9a" : "#e8f4ff",
    spikeCount: 6 + variant * 2 + (zone.tier % 3),
    spikeAmplitude: 0.25 + variant * 0.06,
    baseRadiusRatio: 0.7 + Math.min(0.2, zone.tier * 0.02) + variant * 0.03,
  };
}

/** `MONSTERS`（敵の絵の一覧）に足す、ランダムエンカウントの敵の絵。 */
export function encounterMonsterSpecs(): Record<string, MonsterSpec> {
  const specs: Record<string, MonsterSpec> = {};
  for (const [mapId, zone] of Object.entries(ENCOUNTER_ZONES)) {
    for (let variant = 0; variant < zone.names.length; variant++) {
      specs[`enc-${mapId}-${variant}`] = encounterMonsterSpec(zone, variant);
    }
  }
  return specs;
}
