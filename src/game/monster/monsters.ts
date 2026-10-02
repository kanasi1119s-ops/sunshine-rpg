import { shadeColor } from "../color-utils";
import { encounterMonsterSpecs } from "../encounter/encounter";

/**
 * 戦闘中の敵グラフィック（ドット絵）。`docs/decisions.md`（ドット絵の
 * クオリティを高める方針）に基づき、単色四角の代わりに使う。
 * 「歪み」（`docs/story/bible.md` 8）はアメーバ状の異形という設定のため、
 * キャラクターの顔グラフィック（`portrait/portraits.ts`）とは別に、
 * 中心からの角度と距離だけで輪郭を決める、いびつな塊のグリッドを作る。
 * 既存作品のモンスターデザインは参照していない。
 */
export interface MonsterSpec {
  /** 輪郭寄りの色。 */
  body: string;
  /** 中心に近い色（塊の芯）。 */
  core: string;
  /** 目にあたる、光る点の色。 */
  eye: string;
  /** 輪郭のとげ・触手状の突起の数。 */
  spikeCount: number;
  /** 突起の深さ（0〜1、半径に対する割合）。大きいほどいびつになる。 */
  spikeAmplitude: number;
  /** グリッドに対する基本半径の割合（0〜1）。 */
  baseRadiusRatio: number;
  /** 輪郭の形。省略時は従来の「いびつな塊（blob）」。雑魚は名前に合わせて変える。 */
  shape?: MonsterShape;
}

/**
 * blob=いびつな塊、bat=羽ばたく影、beetle=足のある虫、shard=結晶、drop=しずく（水の玉）、
 * ghost=かげ（ぼろ布の幽霊）、rat=ねずみ、scorpion=サソリ、eye=め（宙に浮く目玉）。
 * 戦闘画面では64×64の手描きの絵（`mob:*`）で描く。手描きの絵が出せない場面では、20×20の手続き的な絵に代える。
 */
export type MonsterShape = "blob" | "bat" | "beetle" | "shard" | "drop" | "ghost" | "rat" | "scorpion" | "eye";

/** 手続き的な絵の形（`insideShape`）。手描きだけの形は、近い形で代用する。 */
const PROCEDURAL_SHAPE: Record<Exclude<MonsterShape, "blob">, "bat" | "beetle" | "shard" | "drop"> = {
  bat: "bat",
  beetle: "beetle",
  shard: "shard",
  drop: "drop",
  ghost: "drop",
  rat: "beetle",
  scorpion: "beetle",
  eye: "shard",
};

/** 形ごとの輪郭。u・vは中心を0とし、-1〜1に正規化した座標（vは下が正）。 */
function insideShape(shape: "bat" | "beetle" | "shard" | "drop", u: number, v: number): boolean {
  const au = Math.abs(u);
  switch (shape) {
    case "bat": {
      if (au < 0.28) return Math.abs(v + 0.05) < 0.5 * Math.sqrt(1 - (au / 0.28) ** 2 * 0.6);
      const top = -0.55 + 0.6 * (au - 0.28);
      const bottom = 0.2 + 0.28 * Math.cos((au - 0.28) * 11);
      return au <= 0.95 && v >= top && v <= bottom;
    }
    case "beetle": {
      if ((u / 0.78) ** 2 + ((v + 0.1) / 0.5) ** 2 <= 1) return true;
      return v > 0.3 && v < 0.85 && [0.3, 0.55, 0.8].some((x) => Math.abs(au - x) < 0.07 + (v < 0.5 ? 0.05 : 0));
    }
    case "shard":
      return au / 0.62 + Math.abs(v) / 0.92 <= 1 && !(au < 0.08 && v > 0.55);
    case "drop":
      return v < 0.1 ? v > -0.92 && au < 0.62 * ((v + 0.92) / 1.02) ** 1.3 : (u / 0.66) ** 2 + ((v - 0.1) / 0.7) ** 2 <= 1;
    default:
      return true;
  }
}

/** 形ごとの目の位置（vは中心から。uは左右の間隔）。 */
const EYE_POS: Record<"bat" | "beetle" | "shard" | "drop", { v: number; u: number }> = {
  bat: { v: -0.12, u: 0.13 },
  beetle: { v: -0.22, u: 0.25 },
  shard: { v: -0.12, u: 0.2 },
  drop: { v: 0.12, u: 0.25 },
};

export const MONSTER_GRID_SIZE = 20;

export interface MonsterCell {
  row: number;
  col: number;
  color: string;
}

/**
 * 中心からの角度・距離だけで輪郭を決めるので、`docs/story/characters.md`の
 * ような左右対称の顔とは違い、いびつで生物らしくない「歪み」の見た目になる。
 */
export function buildMonsterCells(spec: MonsterSpec): MonsterCell[] {
  const size = MONSTER_GRID_SIZE;
  const center = (size - 1) / 2;
  const maxRadius = size / 2;
  const baseRadius = maxRadius * spec.baseRadiusRatio;
  const cells: MonsterCell[] = [];
  if (spec.shape && spec.shape !== "blob") {
    return buildShapedCells(spec, PROCEDURAL_SHAPE[spec.shape]);
  }

  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      const dx = col - center;
      const dy = row - center;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const angle = Math.atan2(dy, dx);
      const spike = 1 + spec.spikeAmplitude * Math.cos(spec.spikeCount * angle);
      const edgeRadius = baseRadius * spike;
      if (dist > edgeRadius) {
        continue;
      }

      const coreRadius = edgeRadius * 0.45;
      const isCore = dist <= coreRadius;
      const baseColor = isCore ? spec.core : spec.body;

      // 中心が明るく、輪郭に近いほど暗くなる（立体感を付ける）。
      const shadeAmount = 0.15 - 0.35 * Math.min(1, dist / edgeRadius);
      let color = shadeColor(baseColor, shadeAmount);

      // 目（中心よりやや上、左右に2つ）を光る点として最後に重ねる。
      const eyeRow = Math.round(center - baseRadius * 0.15);
      const eyeOffset = Math.max(1, Math.round(baseRadius * 0.3));
      if (row === eyeRow && (col === Math.round(center - eyeOffset) || col === Math.round(center + eyeOffset))) {
        color = spec.eye;
      }

      cells.push({ row, col, color });
    }
  }

  return cells;
}

/** blob以外の形。輪郭の1マス内側を暗く縁取り、中心ほど明るくして立体感を出す。 */
function buildShapedCells(spec: MonsterSpec, shape: "bat" | "beetle" | "shard" | "drop"): MonsterCell[] {
  const size = MONSTER_GRID_SIZE;
  const half = size / 2;
  const inside = (row: number, col: number): boolean =>
    row >= 0 && row < size && col >= 0 && col < size && insideShape(shape, (col + 0.5 - half) / half, (row + 0.5 - half) / half);
  const eyePos = EYE_POS[shape];
  const cells: MonsterCell[] = [];
  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      if (!inside(row, col)) continue;
      const u = (col + 0.5 - half) / half;
      const v = (row + 0.5 - half) / half;
      const edge = !inside(row - 1, col) || !inside(row + 1, col) || !inside(row, col - 1) || !inside(row, col + 1);
      let color: string;
      if (edge) {
        color = shadeColor(spec.body, -0.35);
      } else {
        const lit = 0.18 - 0.2 * (u + v + 1) / 2 - 0.18 * Math.min(1, Math.hypot(u, v));
        color = shadeColor(Math.hypot(u, v) < 0.38 ? spec.core : spec.body, lit);
      }
      cells.push({ row, col, color });
    }
  }
  const eyeRow = Math.round(half + eyePos.v * half - 0.5);
  const eyeOffset = Math.max(1, Math.round(eyePos.u * half));
  for (const cell of cells) {
    if (cell.row === eyeRow && (cell.col === Math.round(half - 0.5 - eyeOffset) || cell.col === Math.round(half - 0.5 + eyeOffset))) {
      cell.color = spec.eye;
    }
  }
  return cells;
}

/** 戦闘に登場するCombatantのid（`chapter0-enemies.ts`等）をキーにした登録一覧。 */
export const MONSTERS: Record<string, MonsterSpec> = {
  "chapter0-yugami": {
    body: "#6a3fa8",
    core: "#b98fe0",
    eye: "#f2c14e",
    spikeCount: 7,
    spikeAmplitude: 0.35,
    baseRadiusRatio: 0.8,
  },
  "mugikano-yugami": {
    body: "#2f6a8a",
    core: "#7fc4d9",
    eye: "#e0e0f2",
    spikeCount: 9,
    spikeAmplitude: 0.3,
    baseRadiusRatio: 0.85,
  },
  "garasuko-yugami": {
    body: "#8a5a2f",
    core: "#e0a84f",
    eye: "#6adfd0",
    spikeCount: 11,
    spikeAmplitude: 0.4,
    baseRadiusRatio: 0.9,
  },
};

/** 色相と、とげの数から、敵の絵の設計を作る（第3章以降のボスなど、絵の設計が未登録の敵に使う）。 */
function bossSpec(hue: number, spikes: number, ratio = 0.85): MonsterSpec {
  const hsl = (h: number, sat: number, l: number): string => {
    const k = (n: number): number => (n + h / 30) % 12;
    const a = sat * Math.min(l, 1 - l);
    const f = (n: number): number => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
    const hex = (v: number): string => Math.round(v * 255).toString(16).padStart(2, "0");
    return `#${hex(f(0))}${hex(f(8))}${hex(f(4))}`;
  };
  return { body: hsl(hue, 0.5, 0.3), core: hsl(hue, 0.55, 0.65), eye: "#fff2a0", spikeCount: spikes, spikeAmplitude: 0.35, baseRadiusRatio: ratio };
}

/** ボス・裏ボス・8神など、これまでに絵の設計が無かった敵（仮の絵。色とぎざぎざだけを変えた歪みの姿）。 */
const EXTRA_BOSS_SPECS: Record<string, MonsterSpec> = {
  "tetsukusari-yugami": bossSpec(15, 8),
  "sanone-yugami": bossSpec(45, 10),
  "kiri-yugami": bossSpec(170, 9),
  "shimohara-yugami": bossSpec(195, 12),
  "fushima-yugami": bossSpec(235, 11),
  "toushin-yugami": bossSpec(220, 13),
  "kyotoukyu-yugami": bossSpec(275, 14, 0.9),
  "deep3-yugami": bossSpec(300, 10),
  "deep-yugami": bossSpec(260, 15, 0.92),
  "god-1": bossSpec(110, 8),
  "god-2": bossSpec(80, 16),
  "god-3": bossSpec(10, 9),
  "god-4": bossSpec(40, 7),
  "god-5": bossSpec(200, 6),
  "god-6": bossSpec(215, 10),
  "god-7": bossSpec(265, 12),
  "god-8": bossSpec(250, 5),
  "tower2-guard": bossSpec(210, 9),
  "tower3-guard": bossSpec(50, 11),
  "kanou3-guard": bossSpec(320, 10),
  zenkan: bossSpec(280, 6, 0.95),
};

for (const [id, spec] of Object.entries({ ...EXTRA_BOSS_SPECS, ...encounterMonsterSpecs() })) {
  if (!(id in MONSTERS)) {
    MONSTERS[id] = spec;
  }
}

