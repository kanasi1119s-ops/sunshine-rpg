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
}

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

