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
const HEIGHT = 22;   // 2026-10-06 人間の指示「町を上に少し広げよう」で、上へ6マス広げた（16→22）

const WEST_GATE = { x: 0, y: 16 };
const EAST_GATE = { x: WIDTH - 1, y: 16 };
/** 町の北、崖の岩肌に掘られた記録の間（古文書庫）への入口。 */
const ARCHIVE_GATE_POS = { x: 12, y: 0 };
/** 環の聖堂（教会。絵は `prop:church`、足もとのまんなかがここ。横7マス×縦4マス（絵は右へ奥行きがのびる）。2026-10-06 に大きくし、足もとを (7,5) から下げた）と、巡礼者の宿坊（3x2）。 */
const CHURCH_FOOT = { x: 25, y: 12 };   // 2026-10-06 人間の指示「教会の場所変えよう右側の空間空いているからそこにしよう」。町を東へ広げた区域（x 24〜、town-expand.ts）
/** 聖堂の扉（足もとのすぐ下。上へ押すと中へ入る）。 */
export const KIRI_CHURCH_TOWN_DOOR = { x: CHURCH_FOOT.x, y: CHURCH_FOOT.y + 1 };
/** 民家（3x2 の壁のかたまり。町の家の絵になり、中がつく）。2026-10-06 人間の指示「民家を増やして」「ほかの町と同じ感じにして」:
 *  ほかの町と同じく、ならべず、間をあけて、ずらして散らす。いちばん目の家が巡礼者の宿坊。 */
const HOUSES: Array<[number, number]> = [[7, 6], [2, 3], [2, 10], [8, 12], [14, 3], [18, 6]];
const HOSTEL_ORIGIN = { x: HOUSES[0][0], y: HOUSES[0][1] };

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
    set(WIDTH - 1, y, y === EAST_GATE.y ? PATH : CLIFF);
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

  // 宿坊（外観のみ）。聖堂は、map-props.ts の飾りの絵（`church`、足もと CHURCH_FOOT）で置く（通れない範囲は絵の足もとから決まる）。
  for (let dx = 0; dx < 3; dx++) {
    for (let dy = 0; dy < 2; dy++) {
      set(HOSTEL_ORIGIN.x + dx, HOSTEL_ORIGIN.y + dy, CHAPEL);
    }
  }
  // 民家
  for (const [hx, hy] of HOUSES) {
    for (let dx = 0; dx < 3; dx++) for (let dy = 0; dy < 2; dy++) set(hx + dx, hy + dy, CHAPEL);
  }
  // 広場の石柱。
  for (const [x, y] of [[11, 18], [15, 18], [11, 14], [15, 14]] as [number, number][]) {   // 2026-10-06 町を広げて聖堂を東へ動かしたので、広場の石柱も
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
        // 東の街道を渡って、第6章の霜原へ。
        tileX: EAST_GATE.x,
        tileY: EAST_GATE.y,
        targetMapId: "shimohara-town",
        targetTileX: 2,
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
      {
        // 環の聖堂の扉から、中へ（2026-10-06 聖堂を町を広げた東の区域へ動かしたので、最初の出入り口にしない。最初の出入り口は、歩ける範囲を調べる出発点に使われるため）。
        tileX: KIRI_CHURCH_TOWN_DOOR.x,
        tileY: KIRI_CHURCH_TOWN_DOOR.y,
        targetMapId: "kiri-church",
        targetTileX: 6,
        targetTileY: 9,
        enter: "up",
      },
    ],
  };
}

/** 砂音から街道を渡ってきたときの立ち位置。 */
export const KIRI_TOWN_ENTRY = { tileX: WEST_GATE.x + 2, tileY: WEST_GATE.y };

/** 霜原から街道を戻ってきたときの立ち位置。 */
export const KIRI_TOWN_EAST_RETURN = { tileX: EAST_GATE.x - 2, tileY: EAST_GATE.y };

/** 記録の間から戻ってきたときの立ち位置。 */
export const KIRI_TOWN_ARCHIVE_RETURN = { tileX: ARCHIVE_GATE_POS.x, tileY: ARCHIVE_GATE_POS.y + 2 };

/** 町のNPCを置く座標（イベントデータ側で使う）。 */
export const KIRI_TOWN_LANDMARKS = {
  priest: { tileX: CHURCH_FOOT.x - 2, tileY: CHURCH_FOOT.y + 2 },
  pilgrim: { tileX: HOSTEL_ORIGIN.x + 1, tileY: HOSTEL_ORIGIN.y + 2 },
  scribe: { tileX: 8, tileY: WEST_GATE.y - 1 },
};
