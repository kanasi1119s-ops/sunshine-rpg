import type { TileMapData } from "../types";

const FLOOR = 1;
const WALL = 2;
const DOOR = 3;

const TILE_COLORS: Record<number, string> = {
  [FLOOR]: "#8a7458",
  [WALL]: "#332e2a",
  [DOOR]: "#6b4a2b",
};

const WIDTH = 17;
const HEIGHT = 12;
const DOOR_X = 8;

/**
 * 支部の家具（調べられる物。`chapter0-world.ts` で、同じ名前の物として置く）。
 * id のことばで絵がきまる（desk=事務机、cabinet=資料棚、papers=書類の山、reception=受付カウンター、shelf=本棚）。
 * wide は、絵が左右のマスにもかかる家具（そのマスも通れなくする）。
 */
export interface BranchFurniture {
  id: string;
  tileX: number;
  tileY: number;
  wide: 0 | 1;
  text: string;
}

export const TOURI_BRANCH_FURNITURE: BranchFurniture[] = [
  // 奥の壁ぎわ: 左は資料の棚（資料室のすみ）、まんなかは支部長の机、右は本棚と資料棚
  { id: "touri-branch-cabinet-1", tileX: 2, tileY: 2, wide: 1, text: "資料棚。各地から届いた依頼の記録が、年ごとに帳面にとじてある。" },
  { id: "touri-branch-cabinet-2", tileX: 5, tileY: 2, wide: 1, text: "古い資料の棚。下の段の木箱には、何十年も前の記録が入っているらしい。" },
  { id: "touri-branch-desk-kasen", tileX: 8, tileY: 2, wide: 1, text: "支部長の机。書きかけの報告書と、灯り石のランプ。インクのにおいがする。" },
  { id: "touri-branch-shelf-1", tileX: 11, tileY: 2, wide: 1, text: "本棚。歪みのしらべ方、灯り石の手入れ、各地の地図……調査員の勉強のための本がならぶ。" },
  { id: "touri-branch-cabinet-3", tileX: 14, tileY: 2, wide: 1, text: "資料棚。巻いた地図と、町ごとの「困りごと帳」がしまってある。" },
  // 右: 職員の机と書類
  { id: "touri-branch-desk-1", tileX: 11, tileY: 5, wide: 1, text: "職員の机。依頼の受付の帳面が、きちんとそろえて置いてある。" },
  { id: "touri-branch-desk-2", tileX: 14, tileY: 5, wide: 1, text: "職員の机。返事を書く手紙が、何通も重なっている。" },
  { id: "touri-branch-papers-1", tileX: 15, tileY: 8, wide: 0, text: "書類の山。ひもでしばった束に「済」の札がついている。" },
  { id: "touri-branch-papers-2", tileX: 15, tileY: 9, wide: 0, text: "書類の山。いちばん上に、港の漁師組合からの礼状がのっている。" },
  // 左: 読みもの机と書類
  { id: "touri-branch-desk-3", tileX: 3, tileY: 6, wide: 1, text: "資料を読むための机。読みかけの記録が、ひらいたままになっている。" },
  { id: "touri-branch-papers-3", tileX: 1, tileY: 9, wide: 0, text: "書類の山。いちばん下の帳面は、表紙が日に焼けて、色があせている。" },
  // 受付カウンター（話しかけると、受付の人と話す）
  { id: "touri-branch-reception", tileX: 8, tileY: 7, wide: 1, text: "" },
];

/**
 * 灯りの相談所 灯里支部の内部（序章の依頼受注イベントの舞台）。2026-10-06 に広げた（人間の指示「支部の部屋もっと大きくして
 * カウンター、机、棚、資料を置くように」）: 17×12。奥に支部長の机と資料棚、まんなかに受付カウンター、右に職員の机。
 * カセン支部長・レトがここにいる（NPC配置はイベントデータ側で行う）。
 */
export function createTouriBranchData(): TileMapData {
  const ground: number[] = new Array(WIDTH * HEIGHT).fill(FLOOR);
  const collision: number[] = new Array(WIDTH * HEIGHT).fill(0);

  const set = (x: number, y: number, tile: number, walkable: boolean): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = walkable ? 0 : 1;
  };

  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, WALL, false);
    set(x, 1, WALL, false);   // 奥の壁は2段（家具を、壁にぴったりつけて置くため）
    set(x, HEIGHT - 1, WALL, false);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, WALL, false);
    set(WIDTH - 1, y, WALL, false);
  }
  set(DOOR_X, HEIGHT - 1, DOOR, true);
  // 横にはばのある家具は、となりのマスも通れなくする（家具の上を歩かないように）
  for (const f of TOURI_BRANCH_FURNITURE) {
    if (!f.wide) continue;
    for (const dx of [-1, 1]) {
      const x = f.tileX + dx;
      if (x > 0 && x < WIDTH - 1) collision[f.tileY * WIDTH + x] = 1;
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
        tileX: DOOR_X,
        tileY: HEIGHT - 1,
        targetMapId: "touri-town",
        targetTileX: 5,
        targetTileY: 6,
      },
    ],
  };
}

/** 入口から入ったときの立ち位置（ドアのすぐ内側）。 */
export const TOURI_BRANCH_ENTRY = { tileX: DOOR_X, tileY: HEIGHT - 2 };

/** カセン支部長・レト・受付・職員を置く座標（イベントデータ側で使う）。 */
export const TOURI_BRANCH_LANDMARKS = {
  kasen: { tileX: 8, tileY: 3 },
  reto: { tileX: 5, tileY: 4 },
  clerk: { tileX: 8, tileY: 6 },
  /** S-002「レトの忘れ物」: 資料棚の一番下（棚のすぐ前のマス）。 */
  oldShelf: { tileX: 5, tileY: 3 },
  /** S-002 のホセ（職員の机のそば）。 */
  hose: { tileX: 12, tileY: 6 },
  /** S-027 の支部の職員。 */
  staff: { tileX: 13, tileY: 9 },
};
