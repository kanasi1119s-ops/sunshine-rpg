import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import type { TileMapData } from "../map/types";
import { DUNGEON_PARENT } from "./dungeon-parent";

/**
 * ユーリの家（2026-10-06、人間の指示「ユーリの自宅を作ってください」）。
 * 灯里の町の、2階建ての屋敷（家の絵の足もと (17,4)、玄関 (16,5)）。1階は台所（かまど・調理台・食器棚）と食卓（母のハルカがいる）、
 * 階段で2階へ。2階は、母の部屋（ベッド・箪笥）と、屋根の下のユーリの部屋（机・ベッド）。
 * 2026-10-06 人間の指示「家だったらお母さんの部屋もほしいしベッドも必要だよね。家のオブジェクト2階のやつにしようか」「キッチンもないとおかしいよね」で、
 * 宿屋の西どなりの平屋 (20,8) から、この屋敷へ移した（屋敷は横に広く、平屋の場所には宿屋と重なって置けないため）。小説（序章）の「屋根裏の小さな窓」「階段をおりると台所から麦粥の湯気」にそろえた（梯子 → 階段。2026-10-06）。
 * ゲームは屋根裏から始まる（`CHAPTER0_START`）。屋根裏のベッドでは、ただで休める。
 */
const FLOOR = 1;
const WALL = 2;

export const YURI_HOME = "yuri-home";
export const YURI_ATTIC = "yuri-home-attic";
/** 灯里の町の、ユーリの家の玄関。 */
export const YURI_HOME_DOOR = { x: 16, y: 5 };
/** 1階: 玄関のすぐ内がわ・階段の下。2階: 階段のとなり・はじめに立つ所。 */
export const YURI_HOME_ENTRY = { tileX: 7, tileY: 8 };
export const YURI_HOME_LADDER_FOOT = { tileX: 11, tileY: 3 };
export const YURI_ATTIC_LADDER_TOP = { tileX: 10, tileY: 6 };
export const YURI_ATTIC_START = { tileX: 11, tileY: 4 };
/** 階段のマス（1階は上り口、屋根裏は下り口）。2026-10-06 人間の指示「ユーリ自分の部屋から出れないよ」「階段もちゃんとしたのを作ろう」:
 *  梯子（向き合って調べる）をやめ、歩いて乗ると上り下りできる階段にした。1階は壁ぞいに右へ上がる3マス幅の階段（prop:stairs-up。
 *  いちばん左の段が上り口）、屋根裏は床の下り口（prop:stairs-down）。 */
export const YURI_HOME_LADDER = { tileX: 11, tileY: 2 };
export const YURI_ATTIC_LADDER = { tileX: 9, tileY: 6 };

interface Furniture {
  id: string;
  x: number;
  y: number;
  wide?: boolean;
  commands: EventCommand[];
}

const say = (text: string): EventCommand => ({ type: "message", text });

function room(w: number, h: number, door: number | null, furniture: Furniture[]): Pick<TileMapData, "width" | "height" | "layers" | "collision"> {
  const ground = new Array<number>(w * h).fill(FLOOR);
  const collision = new Array<number>(w * h).fill(0);
  const wall = (x: number, y: number): void => {
    ground[y * w + x] = WALL;
    collision[y * w + x] = 1;
  };
  for (let x = 0; x < w; x++) {
    wall(x, 0);
    wall(x, 1);   // 奥の壁は2段（家具を、壁にぴったりつけて置く）
    wall(x, h - 1);
  }
  for (let y = 0; y < h; y++) {
    wall(0, y);
    wall(w - 1, y);
  }
  if (door !== null) {
    ground[(h - 1) * w + door] = FLOOR;
    collision[(h - 1) * w + door] = 0;
  }
  for (const f of furniture) {
    if (!f.wide) continue;
    for (const dx of [-1, 1]) if (f.x + dx > 0 && f.x + dx < w - 1) collision[f.y * w + f.x + dx] = 1;
  }
  return { width: w, height: h, layers: [{ name: "ground", data: ground }], collision };
}

const FLOOR_FURNITURE: Furniture[] = [
  { id: "yuri-home-hearth", x: 2, y: 2, wide: true, commands: [say("かまど。母の手入れで、れんがのすみまで、きれいにみがかれている。鍋から、麦粥のいい匂い。")] },
  { id: "yuri-home-kitchen", x: 5, y: 2, wide: true, commands: [say("台所の調理台。石の流しに、くんだばかりの水。まな板の上には、今日の野菜が並んでいる。")] },
  { id: "yuri-home-cupboard", x: 8, y: 2, wide: true, commands: [say("食器棚。ふたり分の皿とおわんが、きちんと重ねてある。いちばん上には、祖父の使っていた湯のみ。")] },
  { id: "yuri-home-table", x: 6, y: 5, commands: [say("食卓。ふたり分の椀と匙が、いつもの場所に置いてある。")] },
];

/** 2階（ゲームの地図の名前は、前のまま yuri-home-attic）。左が母の部屋、右が屋根の下のユーリの部屋。あいだの壁の (7,5) が出入り口。 */
const ATTIC_FURNITURE: Furniture[] = [
  { id: "yuri-mother-bed", x: 2, y: 2, wide: true, commands: [say("母のベッド。きちんと整えられて、日なたの匂いがする。")] },
  { id: "yuri-mother-tansu", x: 5, y: 2, wide: true, commands: [say("母の箪笥。エプロンと、洗いたての手ぬぐい。いちばん下の引き出しには、古い手紙の束がしまってある。")] },
  { id: "yuri-attic-desk", x: 9, y: 2, wide: true, commands: [say("ユーリの机。「調査員の手引き」と、書きかけの日記。小さな窓から、港の灯りが見える。")] },
  { id: "yuri-attic-papers", x: 13, y: 5, commands: [say("町で聞いた話を書きとめた帳面。表紙に、大きな字で「困っている人がいたら、まず話を聞く」と書いてある。")] },
  { id: "yuri-attic-bed", x: 12, y: 2, wide: true, commands: [say("自分のベッドだ。"), { type: "inn", price: 0, home: true }] },
];

const HARUKA_TALK: EventCommand[] = [
  {
    type: "if",
    flag: "chapter1_intro_seen",
    equals: true,
    then: [
      { type: "message", speaker: "ハルカ", text: "お帰りなさい。旅は、どう？　……ううん、話したいときに話してくれれば、それでいいの。" },
      { type: "message", speaker: "ハルカ", text: "疲れたら、屋根裏で休んでいきなさい。ここは、あなたが帰ってくる場所なんだから。" },
    ],
    else: [
      {
        type: "if",
        flag: "chapter0_quest_accepted",
        equals: true,
        then: [{ type: "message", speaker: "ハルカ", text: "仕事の途中でしょう？　ほら、寄り道しないで。……でも、ちゃんとお昼は食べるのよ。" }],
        else: [{ type: "message", speaker: "ハルカ", text: "支部長さんに、朝いちばんに呼ばれてるんでしょう？　遅れないようにね。" }],
      },
    ],
  },
];

/** 1階の階段: 上り口（いちばん左の段）より右の2段は、通れない。 */
function stairBlock(r: ReturnType<typeof room>): ReturnType<typeof room> {
  for (const dx of [1, 2]) if (r.collision) r.collision[YURI_HOME_LADDER.tileY * r.width + YURI_HOME_LADDER.tileX + dx] = 1;
  return r;
}

function furnitureNpcs(list: Furniture[]): Npc[] {
  return list.map((f) => ({ id: f.id, tileX: f.x, tileY: f.y, color: "#7a5228", commands: f.commands }));
}

const look = {
  tileWidth: 16,
  tileHeight: 16,
  tileColors: { [FLOOR]: "#9a7a4a", [WALL]: "#6a5a4a" },
  tileArt: { [FLOOR]: "tint:plank", [WALL]: "tint:brick" },
  theme: "interior" as const,
};

/**
 * 灯里の町の家（玄関 (20,8)）を、ユーリの家にする。`addHouseInteriors` のあとで呼ぶ（その家のふつうの中身を、ユーリの家に入れかえる）。
 */
export function addYuriHome(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  const town = maps["touri-town"];
  const door = town?.exits?.find((e) => e.tileX === YURI_HOME_DOOR.x && e.tileY === YURI_HOME_DOOR.y);
  if (!town || !door) return;
  const old = door.targetMapId;
  const ret = maps[old]?.exits?.[0];
  const back = ret ? { x: ret.targetTileX, y: ret.targetTileY } : { x: YURI_HOME_DOOR.x, y: YURI_HOME_DOOR.y + 1 };
  if (old !== YURI_HOME) {
    delete maps[old];
    delete npcsByMap[old];
  }
  door.targetMapId = YURI_HOME;
  door.targetTileX = YURI_HOME_ENTRY.tileX;
  door.targetTileY = YURI_HOME_ENTRY.tileY;
  maps[YURI_HOME] = {
    ...stairBlock(room(15, 10, 7, FLOOR_FURNITURE)),
    ...look,
    exits: [
      { tileX: 7, tileY: 9, targetMapId: "touri-town", targetTileX: back.x, targetTileY: back.y },
      { tileX: YURI_HOME_LADDER.tileX, tileY: YURI_HOME_LADDER.tileY, targetMapId: YURI_ATTIC, targetTileX: YURI_ATTIC_LADDER_TOP.tileX, targetTileY: YURI_ATTIC_LADDER_TOP.tileY },
    ],
    props: [{ kind: "stairs-up", tileX: YURI_HOME_LADDER.tileX + 1, tileY: YURI_HOME_LADDER.tileY }],
  };
  const up = room(15, 8, null, ATTIC_FURNITURE);
  for (let y = 2; y <= 6; y++) {
    if (y === 5) continue;                                     // 母の部屋とユーリの部屋のあいだの出入り口
    up.layers[0].data[y * 15 + 7] = WALL;
    if (up.collision) up.collision[y * 15 + 7] = 1;
  }
  maps[YURI_ATTIC] = {
    ...up,
    ...look,
    exits: [{ tileX: YURI_ATTIC_LADDER.tileX, tileY: YURI_ATTIC_LADDER.tileY, targetMapId: YURI_HOME, targetTileX: YURI_HOME_LADDER_FOOT.tileX, targetTileY: YURI_HOME_LADDER_FOOT.tileY }],
    props: [{ kind: "stairs-down", tileX: YURI_ATTIC_LADDER.tileX, tileY: YURI_ATTIC_LADDER.tileY }],
  };
  DUNGEON_PARENT[YURI_HOME] = "touri-town";
  DUNGEON_PARENT[YURI_ATTIC] = "touri-town";
  npcsByMap[YURI_HOME] = [
    { id: "yuri-home-haruka", tileX: 4, tileY: 5, color: "#c08a70", spriteName: "ハルカ", commands: HARUKA_TALK },
    ...furnitureNpcs(FLOOR_FURNITURE),
  ];
  npcsByMap[YURI_ATTIC] = furnitureNpcs(ATTIC_FURNITURE);
}
