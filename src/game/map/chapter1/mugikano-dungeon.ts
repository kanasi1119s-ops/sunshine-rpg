import type { TileMapData } from "../types";
import { carveMap, type Rect } from "../carve-map";

/**
 * 第1章（麦香野）の、水源へ行くまでの道（水路沿いの農道 → 古い坑道）。村の北の門を出ると、水路に沿った農道があり、
 * そのさきの鉄格子の扉（鍵が要る）を抜けると、掘り跡の坑道、さらにその奥が水源（ボスの場所）。
 */
const GRASS = 1;
const PATH = 2;
const WATER = 3;
const TREE = 4;
const ROCK = 5;

const W = 22;
const H = 18;

// ---- 水路沿いの農道 ----
const CANAL_COLORS: Record<number, string> = { [GRASS]: "#4a7a3f", [PATH]: "#b79a68", [WATER]: "#3a6ea5", [TREE]: "#1f5c33", [ROCK]: "#5a5a5a" };
const CANAL_ART: Record<number, string> = { [GRASS]: "grass", [PATH]: "path", [WATER]: "water", [TREE]: "treeCanopy" };

export const CANAL_SOUTH = { x: 10, y: 17 };
export const CANAL_NORTH = { x: 10, y: 0 };

export function createMugikanoCanalData(): TileMapData {
  const rooms: Rect[] = [
    { x: 1, y: 11, w: 20, h: 6 }, // 村側の畑
    { x: 1, y: 1, w: 20, h: 6 }, // 北の畑
  ];
  const tiles: { x: number; y: number; tile: number; blocked?: boolean }[] = [];
  // 水路（東西にのびる。橋は中央の2マスだけ）
  for (let x = 1; x <= 20; x++) {
    for (const y of [7, 8, 9, 10]) {
      const bridge = x === 10 || x === 11;
      tiles.push({ x, y, tile: bridge ? PATH : WATER, blocked: !bridge });
    }
  }
  // 畑のあぜ・岩・木立で、道を折れ曲がらせる
  for (const [x, y] of [[4, 12], [5, 12], [6, 12], [14, 13], [15, 13], [16, 13], [8, 15], [9, 15], [3, 3], [4, 3], [5, 3], [14, 4], [15, 4], [16, 4], [8, 2], [12, 5], [17, 2]] as [number, number][]) {
    tiles.push({ x, y, tile: TREE, blocked: true });
  }
  for (const [x, y] of [[12, 12], [7, 4], [18, 15]] as [number, number][]) {
    tiles.push({ x, y, tile: ROCK, blocked: true });
  }
  return carveMap(
    {
      width: W,
      height: H,
      wall: TREE,
      floor: GRASS,
      rooms,
      paths: [{ tile: PATH, points: [[10, 17], [10, 13], [10, 11], [11, 6], [10, 1]] }],
      tiles,
      gates: [{ ...CANAL_SOUTH, tile: PATH }, { ...CANAL_NORTH, tile: PATH }],
    },
    {
      tileColors: CANAL_COLORS,
      tileArt: CANAL_ART,
      exits: [
        { tileX: CANAL_SOUTH.x, tileY: CANAL_SOUTH.y, targetMapId: "mugikano-village", targetTileX: 11, targetTileY: 1 },
        {
          tileX: CANAL_NORTH.x,
          tileY: CANAL_NORTH.y,
          targetMapId: "mugikano-tunnel",
          targetTileX: 10,
          targetTileY: 16,
          requireFlag: "chapter1_got_key",
          blockedMessage: "古い鉄格子の扉に、錠がかかっている。見張り小屋のあたりに、鍵が置いてあるかもしれない。",
        },
      ],
    },
  );
}

/** 村から入ってきたときの立ち位置。 */
export const MUGIKANO_CANAL_ENTRY = { tileX: 10, tileY: 16 };
export const MUGIKANO_CANAL_LANDMARKS = {
  farmer: { tileX: 6, tileY: 14 },
  chestGold: { tileX: 18, tileY: 13 },
  chestKey: { tileX: 18, tileY: 3 },
  sluiceStone: { tileX: 13, tileY: 11 },
  watchman: { tileX: 6, tileY: 5 },
};

// ---- 古い坑道 ----
const FLOOR = 1;
const WALL = 2;
const TUNNEL_COLORS: Record<number, string> = { [FLOOR]: "#5a4630", [WALL]: "#2a1f16" };

export const TUNNEL_SOUTH = { x: 10, y: 17 };
export const TUNNEL_NORTH = { x: 10, y: 0 };

export function createMugikanoTunnelData(): TileMapData {
  const rooms: Rect[] = [
    { x: 8, y: 13, w: 6, h: 4 }, // 入り口
    { x: 10, y: 9, w: 2, h: 5 }, // 坑道
    { x: 5, y: 5, w: 12, h: 5 }, // 大きな広間
    { x: 1, y: 6, w: 4, h: 3 }, // 西の小部屋（バルブ）
    { x: 17, y: 6, w: 4, h: 3 }, // 東の小部屋（バルブ）
    { x: 9, y: 1, w: 4, h: 5 }, // 奥へ
    { x: 14, y: 11, w: 6, h: 3 }, // 南東のくぼみ
    { x: 13, y: 10, w: 2, h: 2 }, // くぼみへの通路
  ];
  return carveMap(
    {
      width: W,
      height: H,
      wall: WALL,
      floor: FLOOR,
      rooms,
      gates: [{ ...TUNNEL_SOUTH, tile: FLOOR }, { ...TUNNEL_NORTH, tile: FLOOR }],
    },
    {
      tileColors: TUNNEL_COLORS,
      exits: [
        { tileX: TUNNEL_SOUTH.x, tileY: TUNNEL_SOUTH.y, targetMapId: "mugikano-canal", targetTileX: 10, targetTileY: 1 },
        {
          tileX: TUNNEL_NORTH.x,
          tileY: TUNNEL_NORTH.y,
          targetMapId: "mugikano-water-source",
          targetTileX: 9,
          targetTileY: 12,
          requireFlag: "chapter1_valves_open",
          blockedMessage: "奥の岩戸は、びくともしない。左右の部屋にある古いバルブ（赤い台）を回して、水を抜けば開きそうだ。",
        },
      ],
    },
  );
}

export const MUGIKANO_TUNNEL_LANDMARKS = {
  valveWest: { tileX: 2, tileY: 7 },
  valveEast: { tileX: 19, tileY: 7 },
  chest: { tileX: 18, tileY: 12 },
  wallMark: { tileX: 12, tileY: 3 },
};
