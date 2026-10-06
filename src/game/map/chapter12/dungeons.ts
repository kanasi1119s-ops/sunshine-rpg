import { BEFORE_GATE, buildFloor, type Palette } from "../chapter10/deep-maps";
import type { TileMapData } from "../types";

/**
 * 芯環塔（全8階層。もとは3階層、roadmap 6-8）と環奥（異界の迷宮、全4区画、roadmap 6-10）。
 * 作りは虚灯宮・深部と同じ（灯り石の台2つ→北の封印の扉）。階層ごとに色・障害物・宝箱の位置が違う。
 */
export const TOWER_PALETTES: Palette[] = [
  { floor: "#6a7480", wall: "#1c2028", block: "#3a4a5a", glow: "#9ad0ff" }, // 1 根の階: 薄暗い岩肌と青白い鉱脈
  { floor: "#a8b8d0", wall: "#5a6a88", block: "#7a8aa8", glow: "#ffffff" }, // 2 雲路の階: 雲海の見える裂け目
  { floor: "#c8bc98", wall: "#4a4030", block: "#a89860", glow: "#fff0a0" }, // 3 環光の階: 環の紋様の広間
  { floor: "#58687a", wall: "#141a24", block: "#2e4058", glow: "#7ab8f0" }, // 4 鉱脈の螺旋: 青い鉱脈がらせんに巻く
  { floor: "#9aaac0", wall: "#465670", block: "#6a7c98", glow: "#e8f4ff" }, // 5 風の回廊: 大きな窓から雲海が見える
  { floor: "#3a3a58", wall: "#101020", block: "#28284a", glow: "#c8c0ff" }, // 6 星の書庫: 星図の棚がならぶ暗い広間
  { floor: "#6a6478", wall: "#24202e", block: "#4a4458", glow: "#ffd0a0" }, // 7 嵐の階段: 風の吹きこむ外壁ぞいの段
  { floor: "#b0a4b8", wall: "#3a3044", block: "#8a7c98", glow: "#ffe0b0" }, // 8 頂の見晴らし: 夜明けの欄干
];

/**
 * 塔を昇る順（2026-10-06、人間の指示「階層もっと増やしていい。あんなに高いんだし」で、3階 → 8階に）。
 * 地図の名前（tower-1〜3）は、前からのセーブと合うよう、そのまま残し、あいだと上に tower-4〜8 を足した。
 */
export const TOWER_ORDER = ["tower-1", "tower-4", "tower-2", "tower-5", "tower-6", "tower-3", "tower-7", "tower-8"] as const;
export type TowerMapId = (typeof TOWER_ORDER)[number];

const TOWER_BLOCKS: [number, number][][] = [
  [[5, 8], [14, 8], [3, 11], [16, 4]],
  [[6, 5], [13, 5], [9, 9], [2, 10]],
  [[4, 4], [15, 4], [7, 9], [12, 9]],
  [[3, 4], [7, 5], [12, 7], [16, 9], [5, 10]],
  [[2, 4], [2, 9], [8, 6], [12, 6]],
  [[3, 5], [5, 5], [14, 5], [16, 5], [3, 9], [16, 9]],
  [[6, 4], [13, 4], [4, 8], [15, 8], [8, 11]],
  [[3, 4], [16, 4], [3, 10], [16, 10]],
];

export const KANOU_PALETTES: Palette[] = [
  { floor: "#484868", wall: "#141420", block: "#30304a", glow: "#a8a8f0" }, // 迷いの回廊
  { floor: "#587068", wall: "#18241e", block: "#3a5048", glow: "#b0f0d8" }, // 静けさの間
  { floor: "#705868", wall: "#241820", block: "#503a48", glow: "#f0b0d8" }, // 裂け目の庭
  { floor: "#b8b8d8", wall: "#0a0a12", block: "#8080a8", glow: "#ffffff" }, // 全環の間
];

const BLOCKS: [number, number][][] = [
  [[5, 8], [14, 8], [3, 11], [16, 4]],
  [[6, 5], [13, 5], [9, 9], [2, 10]],
  [[4, 4], [15, 4], [7, 9], [12, 9]],
  [[7, 8], [12, 8], [5, 11], [14, 11]],
];

/** 塔の各階の南の出入り口が戻る先（ひとつ下の階の、北の扉の手前）。根の階から南へ出ると、転移してきた深部の転移陣の前に戻る（塔には世界地図からの入口がない。2026-10-05）。 */
function towerBack(mapId: TowerMapId) {
  const i = TOWER_ORDER.indexOf(mapId);
  return i === 0
    ? { targetMapId: "deep-4", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY + 1 }
    : { targetMapId: TOWER_ORDER[i - 1], targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY };
}
const KANOU_BACK = [
  { targetMapId: "tower-8", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-1", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-2", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-3", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
];

export function createTowerData(floor: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8): TileMapData {
  return buildFloor(TOWER_PALETTES[floor - 1], TOWER_BLOCKS[floor - 1], towerBack(`tower-${floor}` as TowerMapId));
}

export function createKanouData(area: 1 | 2 | 3 | 4): TileMapData {
  return buildFloor(KANOU_PALETTES[area - 1], BLOCKS[area - 1], KANOU_BACK[area - 1]);
}

/** 宝箱（伝説の装備アイテム）の座標。 */
export const CHEST = { tileX: 16, tileY: 10 };
