import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const CONSOLE = 3;
const CABLE = 4;
const DOOR = 5;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#6f7a86",
  [WALL]: "#343a46",
  [CONSOLE]: "#4f7080",
  [CABLE]: "#7a6a8a",
  [DOOR]: "#5a5a66",
};

const NON_WALKABLE = new Set([WALL, CONSOLE, CABLE]);

const WIDTH = 20;
const HEIGHT = 14;

const SOUTH_DOOR = { x: 9, y: HEIGHT - 1 };
/** 奥の大きな監視卓（4x2）。大陸各地の歪みの発生点が光点で映る。 */
const CONSOLE_ORIGIN = { x: 8, y: 3 };

/**
 * 第7章の事件現場、浮島の裏側に隠された黒幕の拠点。
 * 大陸各地の歪みの発生と制御を見張っていた部屋で、これまでの事件がここでつながる。
 */
export function createFushimaBaseData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL);
    set(x, HEIGHT - 1, x === SOUTH_DOOR.x ? DOOR : WALL);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL);
    set(WIDTH - 1, y, WALL);
  }

  // 左右の壁ぎわの配線。
  for (let y = 2; y < 10; y++) {
    set(2, y, CABLE);
    set(WIDTH - 3, y, CABLE);
  }
  // 奥の監視卓。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(CONSOLE_ORIGIN.x + dx, CONSOLE_ORIGIN.y + dy, CONSOLE);
    }
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
        // 南の扉から、浮嶼の町へ。
        tileX: SOUTH_DOOR.x,
        tileY: SOUTH_DOOR.y,
        targetMapId: "fushima-town",
        targetTileX: 12,
        targetTileY: 2,
      },
    ],
  };
}

/** 町から入ってきたときの立ち位置。 */
export const FUSHIMA_BASE_ENTRY = { tileX: SOUTH_DOOR.x, tileY: SOUTH_DOOR.y - 2 };

/** 拠点内のNPC・仕掛けを置く座標（イベントデータ側で使う）。 */
export const FUSHIMA_BASE_LANDMARKS = {
  console: { tileX: CONSOLE_ORIGIN.x + 1, tileY: CONSOLE_ORIGIN.y + 2 },
  ledger: { tileX: 4, tileY: 5 },
  panel: { tileX: 15, tileY: 5 },
  guard: { tileX: 7, tileY: 7 },
};
