import type { TileMapData } from "../types";

const DECK = 1;
const CLOUD = 2;
const ROPE = 3;
const HOUSE = 4;
const HANGAR_GATE = 5;
const CRATE = 6;

const TILE_COLORS: Record<number, string> = {
  [DECK]: "#b8a88a",
  [CLOUD]: "#cfe3f2",
  [ROPE]: "#8a7a5a",
  [HOUSE]: "#7a6a58",
  [HANGAR_GATE]: "#5a5a66",
  [CRATE]: "#9a8058",
};

const NON_WALKABLE = new Set([CLOUD, ROPE, HOUSE, CRATE]);

const WIDTH = 24;
const HEIGHT = 16;

const WEST_GATE = { x: 0, y: 10 };
/** 町の北、浮島の裏側へ通じる整備区画（黒幕の隠れ拠点）への入口。 */
const BASE_GATE_POS = { x: 12, y: 0 };
/** 雲海衆の集会所（4x2）と、宿屋（3x2）。 */
const HALL_ORIGIN = { x: 5, y: 4 };
const INN_ORIGIN = { x: 17, y: 4 };

/**
 * 第7章の舞台、空に浮かぶ島の町・浮嶼（`docs/story/structure.md`「第7章（浮嶼）」参照）。
 * 板張りの通りが雲の海に浮かぶ。西の街道から入り、北に黒幕の隠れ拠点への入口がある。
 */
export function createFushimaTownData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(DECK);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };

  // 外周: 雲の海で囲み、西（霜原からの街道）と北（拠点）だけ開ける。
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, x === BASE_GATE_POS.x ? HANGAR_GATE : CLOUD);
    set(x, HEIGHT - 1, CLOUD);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, y === WEST_GATE.y ? DECK : CLOUD);
    set(WIDTH - 1, y, CLOUD);
  }

  // 島の縁（南北の帯は雲がのぞく）。
  for (let x = 1; x < WIDTH - 1; x++) {
    set(x, 1, x === BASE_GATE_POS.x ? DECK : CLOUD);
    set(x, HEIGHT - 2, CLOUD);
  }

  // 拠点への通り。
  for (let y = 2; y < WEST_GATE.y; y++) {
    set(BASE_GATE_POS.x, y, DECK);
  }
  set(BASE_GATE_POS.x, 1, DECK);

  // 集会所と宿屋（外観のみ）。
  for (let dx = 0; dx < 4; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(HALL_ORIGIN.x + dx, HALL_ORIGIN.y + dy, HOUSE);
    }
  }
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(INN_ORIGIN.x + dx, INN_ORIGIN.y + dy, HOUSE);
    }
  }
  // 荷積みの木箱と、係留のロープ。
  for (const [x, y] of [[15, 12], [16, 12], [16, 13]]) {
    set(x, y, CRATE);
  }
  for (const y of [12, 13]) {
    set(4, y, ROPE);
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
        // 霜原へ戻る街道。
        tileX: WEST_GATE.x,
        tileY: WEST_GATE.y,
        targetMapId: "shimohara-town",
        targetTileX: 21,
        targetTileY: 10,
      },
      {
        // 北の整備区画から、隠れ拠点へ。
        tileX: BASE_GATE_POS.x,
        tileY: BASE_GATE_POS.y,
        targetMapId: "fushima-base",
        targetTileX: 9,
        targetTileY: 12,
      },
    ],
  };
}

/** 霜原から街道を渡ってきたときの立ち位置。 */
export const FUSHIMA_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 拠点から戻ってきたときの立ち位置。 */
export const FUSHIMA_TOWN_BASE_RETURN = { tileX: BASE_GATE_POS.x, tileY: BASE_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const FUSHIMA_TOWN_LANDMARKS = {
  elder: { tileX: HALL_ORIGIN.x + 1, tileY: HALL_ORIGIN.y + 2 },
  innkeeper: { tileX: INN_ORIGIN.x + 1, tileY: INN_ORIGIN.y + 2 },
  ferryman: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
