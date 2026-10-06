import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import type { TileMapData } from "../map/types";
import { DUNGEON_PARENT } from "./dungeon-parent";

/**
 * ユーリの家（2026-10-06、人間の指示「ユーリの自宅を作ってください」）。
 * 灯里の町の、宿屋の西どなりの家（家の絵の足もと (20,7)、玄関 (20,8)）。1階は台所と食卓（母のハルカがいる）、
 * 梯子で屋根裏のユーリの部屋へ上がる。小説（序章）の「屋根裏の小さな窓」「梯子をおりると台所から麦粥の湯気」にそろえた。
 * ゲームは屋根裏から始まる（`CHAPTER0_START`）。屋根裏のベッドでは、ただで休める。
 */
const FLOOR = 1;
const WALL = 2;

export const YURI_HOME = "yuri-home";
export const YURI_ATTIC = "yuri-home-attic";
/** 灯里の町の、ユーリの家の玄関。 */
export const YURI_HOME_DOOR = { x: 20, y: 8 };
/** 1階: 玄関のすぐ内がわ・梯子の下。屋根裏: 梯子のとなり・はじめに立つ所。 */
export const YURI_HOME_ENTRY = { tileX: 6, tileY: 7 };
export const YURI_HOME_LADDER_FOOT = { tileX: 10, tileY: 3 };
export const YURI_ATTIC_LADDER_TOP = { tileX: 3, tileY: 5 };
export const YURI_ATTIC_START = { tileX: 4, tileY: 4 };

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
  { id: "yuri-home-hearth", x: 2, y: 2, wide: true, commands: [say("かまど。母の手入れで、れんがのすみまで、きれいにみがかれている。")] },
  { id: "yuri-home-tansu", x: 5, y: 2, wide: true, commands: [say("箪笥。母のエプロンと、洗いたての手ぬぐいがしまってある。")] },
  { id: "yuri-home-shelf", x: 8, y: 2, wide: true, commands: [say("本棚。古い本が、ほこりひとつなく並んでいる。母が、毎日ふいているらしい。")] },
  {
    id: "yuri-home-ladder",
    x: 11,
    y: 2,
    commands: [say("梯子をのぼって、屋根裏の自分の部屋へ。"), { type: "warp", mapId: YURI_ATTIC, ...YURI_ATTIC_LADDER_TOP }],
  },
  { id: "yuri-home-table", x: 6, y: 5, commands: [say("食卓。ふたり分の椀と匙が、いつもの場所に置いてある。")] },
];

const ATTIC_FURNITURE: Furniture[] = [
  { id: "yuri-attic-desk", x: 2, y: 2, wide: true, commands: [say("ユーリの机。「調査員の手引き」と、書きかけの日記。小さな窓から、港の灯りが見える。")] },
  { id: "yuri-attic-papers", x: 4, y: 2, commands: [say("町で聞いた話を書きとめた帳面。表紙に、大きな字で「困っている人がいたら、まず話を聞く」と書いてある。")] },
  { id: "yuri-attic-bed", x: 6, y: 2, wide: true, commands: [say("自分のベッドだ。"), { type: "inn", price: 0, home: true }] },
  {
    id: "yuri-attic-ladder",
    x: 2,
    y: 5,
    commands: [say("梯子をおりて、台所へ。"), { type: "warp", mapId: YURI_HOME, ...YURI_HOME_LADDER_FOOT }],
  },
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
    ...room(13, 9, 6, FLOOR_FURNITURE),
    ...look,
    exits: [{ tileX: 6, tileY: 8, targetMapId: "touri-town", targetTileX: back.x, targetTileY: back.y }],
  };
  maps[YURI_ATTIC] = { ...room(9, 7, null, ATTIC_FURNITURE), ...look, exits: [] };
  DUNGEON_PARENT[YURI_HOME] = "touri-town";
  DUNGEON_PARENT[YURI_ATTIC] = "touri-town";
  npcsByMap[YURI_HOME] = [
    { id: "yuri-home-haruka", tileX: 4, tileY: 4, color: "#c08a70", spriteName: "ハルカ", commands: HARUKA_TALK },
    ...furnitureNpcs(FLOOR_FURNITURE),
  ];
  npcsByMap[YURI_ATTIC] = furnitureNpcs(ATTIC_FURNITURE);
}
