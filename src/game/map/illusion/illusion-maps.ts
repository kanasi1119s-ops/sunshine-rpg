import type { TileMapData } from "../types";

/**
 * 幻想の禁域「まぼろしの回廊」（2026-10-06、人間の指示「禁域幻想空間的なダンジョンも追加しよう。作るときドット絵にこだわりを持ってね」
 * 「幻想のダンジョンには謎解きもほしいかも」）。星の海に水晶の板が浮かぶ、3つの階。
 * 地面の絵は `assets-src/pixel-practice/r33-illusion/illusion_tex.py`（terrain:illusion-*。128×128、つながる模様）。
 * タイル: 1=水晶の床、2=水晶の柱の壁、4=虚空（通れない）、5=扉、6=光の道（ルーンの床）、7=見えない道（虚空に見えるが通れる）。
 */
const FLOOR = 1;
const WALL = 2;
const VOID = 4;
const DOOR = 5;
const RUNE = 6;
const HIDDEN = 7;

const W = 21;
const H = 15;
export const ILLUSION_GATE = { tileX: 10, tileY: 2 };
export const ILLUSION_ENTRY = { tileX: 10, tileY: H - 2 };

interface Exit { x: number; y: number; targetMapId: string; targetTileX: number; targetTileY: number }

function build(decorate: (set: (x: number, y: number, t: number) => void) => void, south: Exit): TileMapData {
  const ground = new Array(W * H).fill(FLOOR);
  const collision = new Array(W * H).fill(0);
  const set = (x: number, y: number, t: number): void => {
    ground[y * W + x] = t;
    collision[y * W + x] = t === WALL || t === VOID ? 1 : 0;
  };
  for (let x = 0; x < W; x++) { set(x, 0, WALL); set(x, H - 1, WALL); }
  for (let y = 0; y < H; y++) { set(0, y, WALL); set(W - 1, y, WALL); }
  // 北の扉の手前を柱の壁で仕切り、扉のマスだけ通れる（扉に立つ人物に話すと、次の階へ）
  for (let x = 1; x < W - 1; x++) if (x !== ILLUSION_GATE.tileX) set(x, ILLUSION_GATE.tileY, WALL);
  for (let y = 1; y < ILLUSION_GATE.tileY; y++) set(ILLUSION_GATE.tileX, y, RUNE);
  decorate(set);
  set(south.x, south.y, DOOR);
  return {
    width: W,
    height: H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { [FLOOR]: "#5e6cba", [WALL]: "#40318a", [VOID]: "#0b0a26", [DOOR]: "#c8b46a", [RUNE]: "#70e0f0", [HIDDEN]: "#0b0a26" },
    tileTexture: { [FLOOR]: "terrain:illusion-floor", [WALL]: "terrain:illusion-wall", [VOID]: "terrain:illusion-void", [RUNE]: "terrain:illusion-rune", [HIDDEN]: "terrain:illusion-hidden" },
    collision,
    exits: [{ tileX: south.x, tileY: south.y, targetMapId: south.targetMapId, targetTileX: south.targetTileX, targetTileY: south.targetTileY }],
  };
}

const SOUTH = { x: 10, y: H - 1 };
const back = (mapId: string, tileX: number, tileY: number): Exit => ({ ...SOUTH, targetMapId: mapId, targetTileX: tileX, targetTileY: tileY });

/** 1階「色の間」: まわりは虚空。3本の水晶の柱の色を、詩のとおりに合わせる。 */
export function createIllusion1Data(): TileMapData {
  return build((set) => {
    for (let y = 3; y < H - 1; y++) for (const x of [1, 2, 18, 19]) set(x, y, VOID);
    for (const [x, y] of [[3, 4], [17, 4], [3, 12], [17, 12]]) set(x, y, VOID);
    for (let y = 9; y < H - 1; y++) set(10, y, RUNE);
    for (let x = 5; x <= 15; x++) set(x, 7, RUNE);
  }, back("kyotoukyu-court", 17, 7));
}

/** 2階「虚空の道」の、見えない道（南の島から北の島へ、くねくね）。 */
export const HIDDEN_PATH: [number, number][] = [
  [10, 10], [10, 9], [9, 9], [8, 9], [7, 9], [7, 8], [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7], [13, 6], [13, 5], [12, 5], [11, 5], [10, 5], [10, 4],
];

/** 2階「虚空の道」: 南と北の小さな水晶の島のあいだは、ぜんぶ虚空。見えない道だけが通れる。 */
export function createIllusion2Data(): TileMapData {
  return build((set) => {
    for (let y = 3; y < H - 1; y++) for (let x = 1; x < W - 1; x++) set(x, y, VOID);
    // 南の島
    for (let y = 11; y < H - 1; y++) for (let x = 7; x <= 13; x++) set(x, y, FLOOR);
    set(10, 12, RUNE);
    // 北の島（扉の前）
    for (let x = 8; x <= 12; x++) set(x, 3, FLOOR);
    for (const [x, y] of HIDDEN_PATH) set(x, y, HIDDEN);
  }, back("illusion-1", ILLUSION_GATE.tileX, ILLUSION_GATE.tileY + 2));
}

/** 3階「問いの間」: 問いの扉が3つならび、その奥に、まぼろしの主。 */
export function createIllusion3Data(): TileMapData {
  return build((set) => {
    for (let y = 3; y < H - 1; y++) for (const x of [1, 19]) set(x, y, VOID);
    for (let y = 3; y < H - 1; y++) set(10, y, RUNE);
    // 問いの扉の列（扉のマスだけ空いている。扉に立つ人物が道をふさぐ）
    for (const y of [11, 8, 5]) for (let x = 2; x < W - 2; x++) if (x !== 10) set(x, y, WALL);
  }, back("illusion-2", ILLUSION_GATE.tileX, ILLUSION_GATE.tileY + 2));
}

export const ILLUSION_LANDMARKS = {
  pillars: [{ tileX: 5, tileY: 6 }, { tileX: 10, tileY: 5 }, { tileX: 15, tileY: 6 }],
  poem: { tileX: 7, tileY: 11 },
  stele2: { tileX: 12, tileY: 12 },
  doors: [{ tileX: 10, tileY: 11 }, { tileX: 10, tileY: 8 }, { tileX: 10, tileY: 5 }],
  boss: { tileX: 10, tileY: 3 },
};
