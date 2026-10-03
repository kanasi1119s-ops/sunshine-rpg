import { BEFORE_GATE, buildFloor, type Palette } from "../chapter10/deep-maps";
import type { TileMapData } from "../types";
import { WORLD_TOWER } from "../world/world-map.generated";

/**
 * 芯環塔（全3階層、roadmap 6-8）と環奥（異界の迷宮、全4区画、roadmap 6-10）。
 * 作りは虚灯宮・深部と同じ（灯り石の台2つ→北の封印の扉）。階層ごとに色・障害物・宝箱の位置が違う。
 */
export const TOWER_PALETTES: Palette[] = [
  { floor: "#6a7480", wall: "#1c2028", block: "#3a4a5a", glow: "#9ad0ff" }, // 根の階: 薄暗い岩肌と青白い鉱脈
  { floor: "#a8b8d0", wall: "#5a6a88", block: "#7a8aa8", glow: "#ffffff" }, // 雲路の階: 雲海の見える裂け目
  { floor: "#c8bc98", wall: "#4a4030", block: "#a89860", glow: "#fff0a0" }, // 環光の階: 環の紋様の広間
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

/** 各階層の南の出入り口が戻る先（塔・環奥の1階層目だけは、それぞれの入口の外へ戻る）。 */
const TOWER_BACK = [
  // 芯環塔の根の階から南へ出ると、海のまんなかの塔の島（世界地図）に戻る
  { targetMapId: "world-map", targetTileX: WORLD_TOWER.x, targetTileY: WORLD_TOWER.y + 1 },
  { targetMapId: "tower-1", ...{ targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY } },
  { targetMapId: "tower-2", ...{ targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY } },
];
const KANOU_BACK = [
  { targetMapId: "tower-3", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-1", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-2", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
  { targetMapId: "kanou-3", targetTileX: BEFORE_GATE.tileX, targetTileY: BEFORE_GATE.tileY },
];

export function createTowerData(floor: 1 | 2 | 3): TileMapData {
  return buildFloor(TOWER_PALETTES[floor - 1], BLOCKS[floor - 1], TOWER_BACK[floor - 1]);
}

export function createKanouData(area: 1 | 2 | 3 | 4): TileMapData {
  return buildFloor(KANOU_PALETTES[area - 1], BLOCKS[area - 1], KANOU_BACK[area - 1]);
}

/** 宝箱（伝説の装備アイテム）の座標。 */
export const CHEST = { tileX: 16, tileY: 10 };
