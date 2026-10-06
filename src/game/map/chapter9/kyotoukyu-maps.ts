import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const PILLAR = 3;
const VOID = 4;
const DOOR = 5;
const GLOW = 6;
const MURAL = 7;
const BED = 8;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8e8aa0",
  [WALL]: "#2e2c3c",
  [PILLAR]: "#5c5a72",
  [VOID]: "#14121e",
  [DOOR]: "#c8b46a",
  [GLOW]: "#a8d4e8",
  [MURAL]: "#7a5a8a",
  [BED]: "#b8a8c8",
};

const NON_WALKABLE = new Set([WALL, PILLAR, VOID, MURAL, BED]);

interface Exit {
  x: number;
  y: number;
  targetMapId: string;
  targetTileX: number;
  targetTileY: number;
}

/** 外周を壁で囲んだ床に、飾りタイルと出入り口を置いて地図データにする。 */
function buildMap(
  width: number,
  height: number,
  decorate: (set: (x: number, y: number, tile: number) => void) => void,
  exits: Exit[],
): TileMapData {
  const ground: number[] = new Array(width * height).fill(FLOOR);
  const collision: number[] = new Array(width * height).fill(0);
  const set = (x: number, y: number, tile: number): void => {
    ground[y * width + x] = tile;
    collision[y * width + x] = NON_WALKABLE.has(tile) ? 1 : 0;
  };
  for (let x = 0; x < width; x++) {
    set(x, 0, WALL);
    set(x, height - 1, WALL);
  }
  for (let y = 0; y < height; y++) {
    set(0, y, WALL);
    set(width - 1, y, WALL);
  }
  decorate(set);
  for (const exit of exits) {
    set(exit.x, exit.y, DOOR);
  }
  return {
    width,
    height,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: TILE_COLORS,
    collision,
    exits: exits.map((e) => ({ tileX: e.x, tileY: e.y, targetMapId: e.targetMapId, targetTileX: e.targetTileX, targetTileY: e.targetTileY })),
  };
}

const COURT_W = 24;
const COURT_H = 16;
const COURT_SOUTH = { x: 12, y: COURT_H - 1 };
const COURT_NORTH = { x: 12, y: 0 };

/**
 * 終章の舞台、虚灯宮の外庭。空に浮かぶ白い回廊が、光る床のまわりに続く。
 * 南の門から灯芯都へ戻れ、北の扉が環の回廊へ通じる。
 */
export function createKyotoukyuCourtData(): TileMapData {
  return buildMap(
    COURT_W,
    COURT_H,
    (set) => {
      for (let y = 2; y < COURT_H - 2; y++) {
        for (const x of [3, 4, 19, 20]) {
          set(x, y, VOID);
        }
      }
      for (const y of [4, 8, 12]) {
        set(8, y, PILLAR);
        set(15, y, PILLAR);
      }
      for (let y = 1; y < COURT_H - 1; y++) {
        set(11, y, GLOW);
        set(13, y, GLOW);
      }
      set(COURT_NORTH.x, 0, DOOR);
    },
    [
      { x: COURT_SOUTH.x, y: COURT_SOUTH.y, targetMapId: "toushin-town", targetTileX: 13, targetTileY: 15 },
      { x: COURT_NORTH.x, y: COURT_NORTH.y, targetMapId: "kyotoukyu-stair", targetTileX: STAIR_SOUTH.x, targetTileY: STAIR_SOUTH.y - 1 },
    ],
  );
}
export const KYOTOUKYU_COURT_ENTRY = { tileX: COURT_SOUTH.x, tileY: COURT_SOUTH.y - 2 };
export const KYOTOUKYU_COURT_LANDMARKS = {
  keeper: { tileX: 10, tileY: 12 },
};

const COR_W = 13;
const COR_H = 22;
const COR_SOUTH = { x: 6, y: COR_H - 1 };
const COR_NORTH = { x: 6, y: 0 };

/** 環の回廊。壁画に「灯の環」と歪みの由来が刻まれている。 */
export function createKyotoukyuCorridorData(): TileMapData {
  return buildMap(
    COR_W,
    COR_H,
    (set) => {
      for (let y = 2; y < COR_H - 2; y += 3) {
        set(2, y, PILLAR);
        set(10, y, PILLAR);
      }
      // 奥の壁画（左右の壁ぎわ）。
      for (let y = 8; y < 12; y++) {
        set(1, y, MURAL);
        set(11, y, MURAL);
      }
      for (let y = 1; y < COR_H - 1; y++) {
        set(6, y, GLOW);
      }
    },
    [
      { x: COR_SOUTH.x, y: COR_SOUTH.y, targetMapId: "kyotoukyu-stair", targetTileX: STAIR_NORTH.x, targetTileY: STAIR_NORTH.y + 1 },
      { x: COR_NORTH.x, y: COR_NORTH.y, targetMapId: "kyotoukyu-dream", targetTileX: DREAM_SOUTH.x, targetTileY: DREAM_SOUTH.y - 1 },
    ],
  );
}
export const KYOTOUKYU_CORRIDOR_ENTRY = { tileX: COR_SOUTH.x, tileY: COR_SOUTH.y - 2 };
export const KYOTOUKYU_CORRIDOR_LANDMARKS = {
  muralLeft: { tileX: 2, tileY: 9 },
  muralRight: { tileX: 10, tileY: 10 },
};

const SAN_W = 19;
const SAN_H = 13;
const SAN_SOUTH = { x: 9, y: SAN_H - 1 };

/** 奥の間。祖父ソウイチが眠る寝台と、エドレアが待つ祭壇がある。 */
export function createKyotoukyuSanctumData(): TileMapData {
  return buildMap(
    SAN_W,
    SAN_H,
    (set) => {
      for (let x = 7; x < 12; x++) {
        set(x, 2, GLOW);
      }
      // 祖父の寝台（2x1）。
      set(3, 3, BED);
      set(4, 3, BED);
      for (const [x, y] of [[2, 6], [16, 6], [2, 9], [16, 9]]) {
        set(x, y, PILLAR);
      }
    },
    [{ x: SAN_SOUTH.x, y: SAN_SOUTH.y, targetMapId: "kyotoukyu-dream", targetTileX: DREAM_GATE.tileX, targetTileY: DREAM_GATE.tileY + 2 }],
  );
}
export const KYOTOUKYU_SANCTUM_ENTRY = { tileX: SAN_SOUTH.x, tileY: SAN_SOUTH.y - 2 };
export const KYOTOUKYU_SANCTUM_LANDMARKS = {
  grandfather: { tileX: 4, tileY: 4 },
  edrea: { tileX: 9, tileY: 4 },
};

// ===== 終章を厚くするために足した地図（2026-10-06、人間の指示「8章クリアしてからのエドレアバトルが簡単すぎる。何か間色々入れたい」）=====
// 外庭 → 光の階段（謎解き・光の守り手）→ 環の回廊（壁画）→ 眠りの回廊（仲間の夢）→ 奥の間（エドレア）

const STAIR_W = 17;
const STAIR_H = 24;
const STAIR_SOUTH = { x: 8, y: STAIR_H - 1 };
const STAIR_NORTH = { x: 8, y: 0 };
/** 光の階段の、底の見えない裂け目（この行と上下1行）。光の橋がかかるまで渡れない。 */
const STAIR_CHASM_Y = 11;

/**
 * 光の階段。南の半分で、3つの灯り石の台を正しい順にともすと、裂け目に光の橋がかかる（橋の手前に立つ「橋のたもと」の
 * 人物（NPC）に話すと渡れる）。北の半分は細い通路になっていて、光の守り手が道をふさいでいる。
 */
export function createKyotoukyuStairData(): TileMapData {
  return buildMap(
    STAIR_W,
    STAIR_H,
    (set) => {
      // 裂け目（3行ぶん、端から端まで）
      for (let y = STAIR_CHASM_Y - 1; y <= STAIR_CHASM_Y + 1; y++) {
        for (let x = 1; x < STAIR_W - 1; x++) set(x, y, VOID);
      }
      // 南の広間の柱と、光のすじ
      for (const [x, y] of [[3, 15], [13, 15], [3, 19], [13, 19]]) set(x, y, PILLAR);
      for (let y = STAIR_CHASM_Y + 2; y < STAIR_H - 1; y++) set(8, y, GLOW);
      // 北の細い通路（守り手が立つ所は1マスだけ）
      for (let y = 1; y <= 4; y++) {
        for (let x = 1; x < STAIR_W - 1; x++) if (x !== 8) set(x, y, y === 4 ? PILLAR : VOID);
      }
      for (let y = 5; y < STAIR_CHASM_Y - 1; y++) {
        for (const x of [1, 2, 14, 15]) set(x, y, VOID);
      }
    },
    [
      { x: STAIR_SOUTH.x, y: STAIR_SOUTH.y, targetMapId: "kyotoukyu-court", targetTileX: COURT_NORTH.x, targetTileY: COURT_NORTH.y + 1 },
      { x: STAIR_NORTH.x, y: STAIR_NORTH.y, targetMapId: "kyotoukyu-corridor", targetTileX: COR_SOUTH.x, targetTileY: COR_SOUTH.y - 1 },
    ],
  );
}
export const KYOTOUKYU_STAIR_ENTRY = { tileX: STAIR_SOUTH.x, tileY: STAIR_SOUTH.y - 1 };
export const KYOTOUKYU_STAIR_LANDMARKS = {
  /** 月・星・陽の台（南の広間）。 */
  moon: { tileX: 4, tileY: 17 },
  star: { tileX: 12, tileY: 17 },
  sun: { tileX: 8, tileY: 20 },
  /** 台の順番の手がかりの石碑。 */
  stele: { tileX: 5, tileY: 21 },
  /** 橋のたもと（裂け目のすぐ南）。話すと、橋がかかっていれば、北へ渡る。 */
  bridge: { tileX: 8, tileY: STAIR_CHASM_Y + 2 },
  /** 渡った先。 */
  across: { tileX: 8, tileY: STAIR_CHASM_Y - 2 },
  /** 光の守り手（北の細い通路の1マス）。 */
  guardian: { tileX: 8, tileY: 4 },
};

const DREAM_W = 21;
const DREAM_H = 14;
const DREAM_SOUTH = { x: 10, y: DREAM_H - 1 };
/** 眠りの回廊の、北の扉（夢をすべて越えると開く。扉に話すと奥の間へ）。 */
const DREAM_GATE = { tileX: 10, tileY: 2 };

/** 眠りの回廊。静めの間の力が漏れ、仲間ひとりひとりに「眠りの誘い」の夢を見せる扉が5つならぶ。 */
export function createKyotoukyuDreamData(): TileMapData {
  return buildMap(
    DREAM_W,
    DREAM_H,
    (set) => {
      for (let x = 1; x < DREAM_W - 1; x++) if (x !== DREAM_GATE.tileX) set(x, DREAM_GATE.tileY, WALL);
      for (let y = 1; y < DREAM_GATE.tileY; y++) set(DREAM_GATE.tileX, y, GLOW);
      for (const [x, y] of [[2, 8], [18, 8], [6, 10], [14, 10]]) set(x, y, PILLAR);
      // 寝台のならぶ壁ぎわ（眠りの気配）
      for (const x of [1, 19]) for (let y = 4; y <= 6; y++) set(x, y, BED);
      for (let y = 3; y < DREAM_H - 1; y++) set(10, y, GLOW);
    },
    [{ x: DREAM_SOUTH.x, y: DREAM_SOUTH.y, targetMapId: "kyotoukyu-corridor", targetTileX: COR_NORTH.x, targetTileY: COR_NORTH.y + 1 }],
  );
}
export const KYOTOUKYU_DREAM_ENTRY = { tileX: DREAM_SOUTH.x, tileY: DREAM_SOUTH.y - 1 };
export const KYOTOUKYU_DREAM_LANDMARKS = {
  gate: DREAM_GATE,
  /** 夢の扉（ミナ・オルカ・コハク・レト・アヤメ）。 */
  doors: [
    { tileX: 3, tileY: 4 },
    { tileX: 6, tileY: 4 },
    { tileX: 14, tileY: 4 },
    { tileX: 17, tileY: 4 },
    { tileX: 10, tileY: 8 },
  ],
};
