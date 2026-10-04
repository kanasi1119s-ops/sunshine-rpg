import type { Combatant } from "../battle/types";
import { expRequiredForLevel } from "../growth/exp-curve";
import type { MonsterShape, MonsterSpec } from "../monster/monsters";

/**
 * フィールド・ダンジョンでのランダムエンカウント（歩いていると、ときどき「歪みのかけら」に出くわす）。
 * 町・ボスの間・8神の禁域などでは起きない。強さは想定レベル（`level`）で決まり、章が進むほど敵も経験値も大きくなる。
 * 数値は仮（`docs/design/battle.md`）。想定レベルのパーティが1〜3体の一団に、約95%以上で勝てる強さにする（`encounter.test.ts`）。
 */
export interface EncounterZone {
  /** その場所を通る頃の、パーティの想定レベル（`boss-balance.test.ts`と同じ考え方。敵の強さと経験値はこれで決まる）。 */
  level: number;
  /** 出てくる敵の名前（6種。海と空は7種。出会うたびにこの中から選ぶ。2026-10-04 に3種から増やした＝人間の指示「雑魚敵は200種」）。 */
  names: string[];
  /** 敵の絵の色相（0〜360）。 */
  hue: number;
}

/** 地図ごとのエンカウント設定。ここに無い地図（町・ボスの間・禁域）では出会わない。 */
export const ENCOUNTER_ZONES: Record<string, EncounterZone> = {
  "touri-forest-1": { level: 2, names: ["野ねずみの影", "草むらの虫", "迷いこうもり", "小石のかけら", "ちいさな歪み", "ゆらぎの影"], hue: 120 },
  "touri-forest-2": { level: 3, names: ["祠の影", "苔むした石", "夜の羽虫", "ゆらぎの影", "野ねずみの影", "ちいさな歪み"], hue: 150 },
  "touri-outskirts": { level: 2, names: ["ちいさな歪み", "ゆらぎの影", "野ねずみの影", "草むらの虫", "迷いこうもり", "小石のかけら"], hue: 270 },
  "mugikano-canal": { level: 3, names: ["畑の虫", "水路の影", "あぜ道の石", "野ねずみの影", "用水路の虫", "ゆらぎの影"], hue: 90 },
  "mugikano-tunnel": { level: 4, names: ["坑道のこうもり", "湿った影", "水のしずく影", "涸れ田の歪み", "採掘跡の虫", "井戸の石"], hue: 190 },
  "mugikano-water-source": { level: 4, names: ["水のしずく影", "涸れ田の歪み", "採掘跡のこうもり", "用水路の虫", "泥のしずく", "井戸の石"], hue: 200 },
  "garasuko-warehouse": { level: 6, names: ["積荷ねずみ", "湿った歪み", "木箱の影", "縄かじり", "樽の石", "倉庫の羽虫"], hue: 30 },
  "tetsukusari-mine": { level: 8, names: ["岩かじり", "坑道の影", "灯り石の虫", "鉱車の機械", "落盤の石", "鉱夫の残響"], hue: 15 },
  "sanone-camp": { level: 10, names: ["砂ぬけ", "風の影", "砂サソリの影", "日照りのしずく", "骨の石", "砂嵐の羽"], hue: 45 },
  "kiri-archive": { level: 12, names: ["紙魚の影", "霧のささやき", "古文書の虫", "墨のしずく", "書架の番兵", "霧の羽"], hue: 170 },
  "shimohara-facility": { level: 14, names: ["霜の歪み", "氷の兵の影", "凍てた機械", "霜柱の結晶", "冷たい配管の虫", "白い羽の影"], hue: 190 },
  "fushima-base": { level: 16, names: ["雲の影", "配線の歪み", "監視の目", "浮き石", "雲の羽虫", "見張りの兵"], hue: 235 },
  "deep-1": { level: 22, names: ["大乱期の残響", "氷の兵の記憶", "折れた剣の影", "錆びた盾のかけら", "古戦場の虫", "凍った涙"], hue: 205 },
  "deep-2": { level: 23, names: ["静まりの残響", "議場の影", "消えた名前", "印章の石", "書記の虫", "黄金のしずく"], hue: 40 },
  "deep-3": { level: 24, names: ["歪みの断片", "水涸れの残り香", "番人のかけら", "紫の結晶", "渇きのしずく", "歪んだ羽"], hue: 290 },
  "deep-4": { level: 25, names: ["初源のしずく", "名前のない影", "悲しみの残響", "始まりの石", "夜明けの羽", "忘却の虫"], hue: 260 },
  "tower-1": { level: 30, names: ["光の結晶", "生きた石", "青い鉱脈の主", "塔の歯車機械", "光の羽虫", "根の番兵"], hue: 205 },
  "tower-2": { level: 31, names: ["雲路の結晶", "霧の足あと", "風をまとう石", "雲の歯車機械", "霧の兵", "雷のしずく"], hue: 215 },
  "tower-3": { level: 32, names: ["環のかけら", "紋様の影", "光の番兵", "金の歯車機械", "紋章の石", "光の羽"], hue: 50 },
  "kanou-1": { level: 33, names: ["境目の揺らぎ", "迷いの光", "たゆたう影", "境目の虫", "迷い羽", "境界の石"], hue: 250 },
  "kanou-2": { level: 34, names: ["静かな影", "待ち人の気配", "緑の光", "苔の石", "森のしずく", "葉の羽虫"], hue: 150 },
  "kanou-3": { level: 35, names: ["裂け目の花", "重なる景色", "薄い境目", "裂け目の虫", "鏡の結晶", "花のしずく"], hue: 320 },
  "kanou-4": { level: 36, names: ["全環のかけら", "白い揺らぎ", "環の残響", "白い羽", "環の結晶", "終わりのしずく"], hue: 280 },
  // 隠しダンジョンの小島（1階。2階は宝の間）。条件の章を終えた頃より、少しだけ手ごわい
  "islet-1-1": { level: 16, names: ["月影の残響", "庭の石像の影", "苔むした断片", "月のしずく", "夜の羽虫", "庭の番兵"], hue: 220 },
  "islet-2-1": { level: 18, names: ["熱の影", "溶けた石", "火の粉の虫", "炎の羽", "鉄の機械", "熱のしずく"], hue: 20 },
  "islet-3-1": { level: 20, names: ["潮風の影", "灯台のかけら", "波間の虫", "潮のしずく", "灯台の番兵", "海鳥の羽"], hue: 55 },
  "islet-4-1": { level: 22, names: ["旗の影", "砦の兵の影", "雲のかけら", "砦の機械", "弓兵の残響", "城壁の石"], hue: 280 },
  "islet-5-1": { level: 23, names: ["沈んだ影", "珊瑚の石", "海ほたるの虫", "深海のしずく", "貝の結晶", "泡の羽"], hue: 195 },
  "islet-6-1": { level: 25, names: ["溶岩の影", "焦げた石", "火の粉のこうもり", "噴煙の羽", "溶岩のしずく", "黒曜の兵"], hue: 10 },
};

/** 世界地図の、地方ごとのエンカウント（道の上では出会わない）。想定レベルは、そこから向かう町の少し手前。 */
export const WORLD_ENCOUNTER_ZONES: Record<string, EncounterZone> = {
  "world-1": { level: 3, names: ["野の虫", "街道の影", "野ねずみの影", "草原のしずく", "道ばたの石", "小鳥の羽"], hue: 120 },
  "world-2": { level: 7, names: ["峠の影", "湖畔のこうもり", "石の歪み", "湖のしずく", "峠の虫", "岩山の兵"], hue: 190 },
  "world-3": { level: 11, names: ["砂ぬけ", "熱風の影", "砂サソリの影", "砂丘の石", "蜃気楼のしずく", "砂漠の羽"], hue: 45 },
  "world-4": { level: 15, names: ["氷の兵の影", "霜の歪み", "白い影", "雪原の虫", "氷の結晶", "吹雪の羽"], hue: 195 },
  "world-5": { level: 24, names: ["火の粉の影", "溶岩の歪み", "灰かぶりの影", "灰の虫", "火山の石", "マグマのしずく"], hue: 15 },
  "world-6": { level: 18, names: ["荒野の影", "灯の消えた歪み", "古い機械の虫", "荒野の石", "錆びた機械", "枯れ野の羽"], hue: 30 },
  // 船で海を進むとき・飛空艇で空を飛ぶときの敵（船は砂音のあと、飛空艇は霜原のあとに手に入る）
  "world-sea": { level: 12, names: ["波間の影", "潮の石", "海ほたるの虫", "渦のしずく", "海の羽", "舟の残響", "沈没船の番兵"], hue: 200 },
  "world-air": { level: 17, names: ["風の羽の影", "雲のかけら", "雷雲の影", "空のしずく", "雷の結晶", "雲の虫", "嵐の羽"], hue: 235 },
};

/**
 * 世界地図の地形（タイルID。道=7、砂漠=5、雪=6・12、火山の灰=18）と位置から、エンカウントの地方を決める。道の上は null（出会わない）。
 * 平地は大陸ごと: 西の灯里大陸（x<45 は序盤の草原、そのさきは峠・湖）、北東の霧霜大陸、南東の灯芯大陸。
 */
export function worldZoneIdAt(tileId: number, tileX: number, tileY = 0): string | null {
  if (tileId === 7 || tileId === 10) {
    return null;
  }
  if (tileId === 18) {
    return "world-5";
  }
  if (tileId === 5) {
    return "world-3";
  }
  if (tileId === 6 || tileId === 12) {
    return "world-4";
  }
  if (tileX < 64) {
    return "world-1";
  }
  if (tileX < 158) {
    return "world-2";
  }
  return tileY < 127 ? "world-4" : "world-6";
}

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
  const zone = ENCOUNTER_ZONES[mapId] ?? WORLD_ENCOUNTER_ZONES[mapId];
  if (!zone) {
    return { state, enemies: null };
  }
  const stepsLeft = state.stepsLeft - 1;
  if (stepsLeft > 0) {
    return { state: { stepsLeft }, enemies: null };
  }
  return { state: { stepsLeft: nextThreshold(rng) }, enemies: createEncounterEnemies(mapId, zone, rng) };
}

/** 想定レベルごとの、雑魚1体の体力・攻撃（間の値は直線でつなぐ）。想定パーティが2体の一団に約96%で勝つ強さを、自動シミュレーションで確かめて決めた。 */
const MOB_ANCHORS: { level: number; maxHp: number; attack: number }[] = [
  { level: 2, maxHp: 18, attack: 10 },
  { level: 4, maxHp: 32, attack: 15 },
  { level: 6, maxHp: 64, attack: 21 },
  { level: 8, maxHp: 135, attack: 31 },
  { level: 10, maxHp: 210, attack: 39 },
  { level: 12, maxHp: 290, attack: 45 },
  { level: 14, maxHp: 340, attack: 52 },
  { level: 16, maxHp: 420, attack: 59 },
  { level: 22, maxHp: 640, attack: 74 },
  { level: 25, maxHp: 720, attack: 82 },
  { level: 30, maxHp: 850, attack: 96 },
  { level: 36, maxHp: 1050, attack: 112 },
];

function interpolate(level: number, key: "maxHp" | "attack"): number {
  const first = MOB_ANCHORS[0];
  const last = MOB_ANCHORS[MOB_ANCHORS.length - 1];
  if (level <= first.level) {
    return first[key];
  }
  if (level >= last.level) {
    return last[key];
  }
  for (let i = 1; i < MOB_ANCHORS.length; i++) {
    const a = MOB_ANCHORS[i - 1];
    const b = MOB_ANCHORS[i];
    if (level <= b.level) {
      return a[key] + ((b[key] - a[key]) * (level - a.level)) / (b.level - a.level);
    }
  }
  return last[key];
}

/** 経験値の割り算の数。序盤（Lv6まで）は5、Lv12以降は10で、間は直線でつなぐ（レベルが上がるほど経験値が減らないように）。 */
function expDivisor(level: number): number {
  return level <= 6 ? 5 : level >= 12 ? 10 : 5 + ((level - 6) * 5) / 6;
}

/** 想定レベルから、雑魚1体の強さを決める。経験値は、想定レベルのパーティが約5戦で1レベル上がる量（序盤〔想定Lv6まで〕は、レベルが上がる手ごたえがほしいので約2〜3戦）。 */
export function enemyStatsForLevel(level: number): { maxHp: number; attack: number; defense: number; speed: number; expReward: number } {
  return {
    maxHp: Math.round(interpolate(level, "maxHp")),
    attack: Math.round(interpolate(level, "attack")),
    defense: Math.round(4 + 0.5 * level),
    speed: Math.round(8 + 0.5 * level),
    expReward: Math.max(6, Math.round((expRequiredForLevel(level + 1) - expRequiredForLevel(level)) / expDivisor(level))),
  };
}

/** 出会うのは1〜3体（tierが低いうちは少なめ）。 */
export function createEncounterEnemies(mapId: string, zone: EncounterZone, rng: () => number): Combatant[] {
  const maxCount = zone.level <= 6 ? 2 : 3;
  const count = 1 + Math.floor(rng() * maxCount);
  const stats = enemyStatsForLevel(zone.level);
  const enemies: Combatant[] = [];
  for (let i = 0; i < count; i++) {
    const variant = Math.floor(rng() * zone.names.length);
    enemies.push({
      // 同じ種類が2体以上出ても、戦闘で別々に狙えるよう、IDに何体目かを付ける（絵の指定は `baseEnemyId` で元に戻す）
      id: `enc-${mapId}-${variant}#${i}`,
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

/** 名前の言葉から、敵の形を決める（当てはまる言葉が無いときは、種類ごとに塊としずくを使い分ける）。 */
export function shapeForName(name: string, variant: number): MonsterShape {
  const has = (words: string[]): boolean => words.some((w) => name.includes(w));
  if (has(["監視の目"])) return "eye";
  if (has(["サソリ"])) return "scorpion";
  if (has(["ねずみ"])) return "rat";
  if (has(["こうもり", "羽", "風", "雲", "霧"])) return "bat";
  if (has(["虫", "かじり", "砂ぬけ", "足あと", "紙魚"])) return "beetle";
  if (has(["結晶", "石", "機械", "兵", "剣", "鉱脈", "番兵", "かけら", "断片", "箱"])) return "shard";
  if (has(["しずく", "花", "光", "悲しみ", "涙", "香"])) return "drop";
  if (has(["影", "残響", "気配", "ささやき", "揺らぎ", "記憶", "消えた"])) return "ghost";
  return variant === 1 ? "drop" : "blob";
}

/** 敵の絵（手続き的なドット絵）の設計。3種の名前ごとに、とげの数・大きさを少しずつ変える。 */
export function encounterMonsterSpec(zone: EncounterZone, variant: number): MonsterSpec {
  return {
    body: hslToHex(zone.hue, 0.45, 0.32),
    core: hslToHex(zone.hue, 0.5, 0.65),
    eye: variant === 1 ? "#ffe066" : variant === 2 ? "#ff9a9a" : "#e8f4ff",
    spikeCount: 6 + variant * 2 + (zone.level % 3),
    spikeAmplitude: 0.25 + variant * 0.06,
    baseRadiusRatio: 0.7 + Math.min(0.2, zone.level * 0.006) + variant * 0.03,
    shape: shapeForName(zone.names[variant], variant),
  };
}

/** `MONSTERS`（敵の絵の一覧）に足す、ランダムエンカウントの敵の絵。 */
export function encounterMonsterSpecs(): Record<string, MonsterSpec> {
  const specs: Record<string, MonsterSpec> = {};
  for (const [mapId, zone] of Object.entries({ ...ENCOUNTER_ZONES, ...WORLD_ENCOUNTER_ZONES })) {
    for (let variant = 0; variant < zone.names.length; variant++) {
      specs[`enc-${mapId}-${variant}`] = encounterMonsterSpec(zone, variant);
    }
  }
  return specs;
}
