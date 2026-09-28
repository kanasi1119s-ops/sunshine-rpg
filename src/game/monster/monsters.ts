import { shadeColor } from "../color-utils";

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
};
