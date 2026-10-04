import type { TileMapData } from "../types";
import { carveMap } from "../carve-map";
import { serpentineLayout, type Landmarks } from "../serpentine";

/**
 * 第1章（麦香野）の、水源へ行くまでの道（水路沿いの農道 → 古い坑道）。村の北の門を出ると、水路に沿った長い農道があり、
 * そのさきの鉄格子の扉（鍵が要る）を抜けると、掘り跡の長い坑道、さらにその奥が水源（ボスの場所）。
 * どちらも、フィールドを旅するように長く折れ曲がる道（`serpentine.ts`）。
 */
const GRASS = 1;
const PATH = 2;
const TREE = 4;

const CANAL_COLORS: Record<number, string> = { [GRASS]: "#4a7a3f", [PATH]: "#b79a68", [TREE]: "#1f5c33", 5: "#5a5a5a" };
const CANAL_ART: Record<number, string> = { [GRASS]: "grass", [PATH]: "path", [TREE]: "treeCanopy" };

const CANAL = serpentineLayout({ lanes: 5, wall: TREE, floor: GRASS, path: PATH, seed: 21 });

const FLOOR = 1;
const WALL = 2;
const TUNNEL_COLORS: Record<number, string> = { [FLOOR]: "#5a4630", [WALL]: "#2a1f16" };
const TUNNEL = serpentineLayout({ lanes: 5, wall: WALL, floor: FLOOR, seed: 22 });

const at = (l: Landmarks, i: number): { tileX: number; tileY: number } => l.alcoves[Math.min(i, l.alcoves.length - 1)];

export function createMugikanoCanalData(): TileMapData {
  const l = CANAL.landmarks;
  return carveMap(CANAL.spec, {
    tileColors: CANAL_COLORS,
    tileArt: CANAL_ART,
    exits: [
      { tileX: l.south.x, tileY: l.south.y, targetMapId: "mugikano-village", targetTileX: 11, targetTileY: 1 },
      {
        tileX: l.north.x,
        tileY: l.north.y,
        targetMapId: "mugikano-tunnel",
        targetTileX: TUNNEL.landmarks.southArrival.tileX,
        targetTileY: TUNNEL.landmarks.southArrival.tileY,
        requireFlag: "chapter1_got_key",
        blockedMessage: "古い鉄格子の扉に、錠がかかっている。農道の見張り小屋のあたりに、鍵が置いてあるかもしれない。",
      },
    ],
  });
}

/** 村から入ってきたときの立ち位置。 */
export const MUGIKANO_CANAL_ENTRY = CANAL.landmarks.southArrival;
export const MUGIKANO_CANAL_LANDMARKS = {
  farmer: CANAL.landmarks.nearEntry,
  chestGold: at(CANAL.landmarks, 2),
  chestKey: at(CANAL.landmarks, 6),
  sluiceStone: CANAL.landmarks.nearExit,
  watchman: at(CANAL.landmarks, 3),
};

export function createMugikanoTunnelData(): TileMapData {
  const l = TUNNEL.landmarks;
  return carveMap(TUNNEL.spec, {
    tileColors: TUNNEL_COLORS,
    exits: [
      { tileX: l.south.x, tileY: l.south.y, targetMapId: "mugikano-canal", targetTileX: CANAL.landmarks.northArrival.tileX, targetTileY: CANAL.landmarks.northArrival.tileY },
      {
        tileX: l.north.x,
        tileY: l.north.y,
        targetMapId: "mugikano-water-source",
        targetTileX: 9,
        targetTileY: 12,
        requireFlag: "chapter1_valves_open",
        blockedMessage: "奥の岩戸は、びくともしない。坑道のあちこちにある古いバルブ（赤い台）を、2つとも回して水を抜けば開きそうだ。",
      },
    ],
  });
}

/** 水源から戻ってきたときの立ち位置。 */
export const MUGIKANO_TUNNEL_NORTH_ENTRY = TUNNEL.landmarks.northArrival;
export const MUGIKANO_TUNNEL_LANDMARKS = {
  valveWest: at(TUNNEL.landmarks, 1),
  valveEast: at(TUNNEL.landmarks, 6),
  chest: at(TUNNEL.landmarks, 4),
  wallMark: TUNNEL.landmarks.nearExit,
};
