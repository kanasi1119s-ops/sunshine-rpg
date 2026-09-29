import type { TileMapData } from "../types";

const STONE = 1;
const PATH = 2;
const CLIFF = 3;
const MIST = 4;
const CHAPEL = 5;
const PILLAR = 6;
const ARCHIVE_GATE = 7;

const TILE_COLORS: Record<number, string> = {
  [STONE]: "#a7a9ad",
  [PATH]: "#c9c4b4",
  [CLIFF]: "#5b5f68",
  [MIST]: "#d6dde4",
  [CHAPEL]: "#e3ddd0",
  [PILLAR]: "#8c8f96",
  [ARCHIVE_GATE]: "#6a5a4a",
};

const NON_WALKABLE = new Set([CLIFF, MIST, CHAPEL, PILLAR]);

const WIDTH = 24;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 10 };
/** 町の北、崖の岩肌に掘られた記録の間（古文書庫）への入口。 */
const ARCHIVE_GATE_POS = { x: 12, y: 0 };
/** 環の聖堂（4x2）と、巡礼者の宿坊（3x2）。 */
const CHAPEL_ORIGIN = { x: 5, y: 4 };
const HOSTEL_ORIGIN = { x: 17, y: 4 };

/**
 * 第5章の舞台、断崖に張り付く古い宗教都市・霧断崖（`docs/story/structure.md`「第5章（霧断崖）」参照）。
 * 町の南は霧の立ちこめる断崖。北の岩壁に、古い記録を納めた「記録の間」の入口がある。
 */
export function createKiriTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(STONE);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周: 崖で囲み、西（砂音からの街道）と北（記録の間）だけ開ける。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === ARCHIVE_GATE_POS.x ? ARCHIVE_GATE : CLIFF);
    set(x, HEIGHT - 1, MIST);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? PATH : CLIFF);
    set(WIDTH - 1, y, CLIFF);
  }
  // 南の断崖の縁（霧で足元が見えない）。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, HEIGHT - 2, MIST);
  }

  // 西の街道から広場へ、広場から記録の間へ。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, WEST_GATE.y, PATH);
  }
  for (let y = 1; y < WEST_GATE.y; y++) {
    set(ARCHIVE_GATE_POS.x, y, PATH);
  }

  // 聖堂と宿坊（外観のみ）。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(CHAPEL_ORIGIN.x + dx, CHAPEL_ORIGIN.y + dy, CHAPEL);
    }
  }
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(HOSTEL_ORIGIN.x + dx, HOSTEL_ORIGIN.y + dy, CHAPEL);
    }
  }
  // 広場の石柱。
  for (const [x, y] of [[10, 8], [14, 8], [10, 12], [14, 12]] as [number, number][]) {
    set(x, y, PILLAR);
  }

  return {
    width: WIDTH,
    height: HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: [
      {
        // 砂音へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "sanone-town",
        targetTileX: 21,
        targetTileY: 10,
      },
      {
        // 北の岩壁の入口から、記録の間へ。
        tileX: ARCHIVE_GATE_POS.x,
        tileY: ARCHIVE_GATE_POS.y,
        targetMapId: "kiri-archive",
        targetTileX: 9,
        targetTileY: 12,
      },
    ],
  };
}

/** 砂音から街道を渡ってきたときの立ち位置。 */
export const KIRI_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 記録の間から戻ってきたときの立ち位置。 */
export const KIRI_TOWN_ARCHIVE_RETURN = { tileX: ARCHIVE_GATE_POS.x, tileY: ARCHIVE_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const KIRI_TOWN_LANDMARKS = {
  priest: { tileX: CHAPEL_ORIGIN.x + 1, tileY: CHAPEL_ORIGIN.y + 2 },
  pilgrim: { tileX: HOSTEL_ORIGIN.x + 1, tileY: HOSTEL_ORIGIN.y + 2 },
  scribe: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
