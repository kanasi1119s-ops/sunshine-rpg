import { hashCell } from "../color-utils";
import type { Npc } from "../npc";
import { isHouse } from "../map/map-props";
import type { MapProp, TileMapData } from "../map/types";
import { chestNpc } from "./dungeon-objects";
import { DUNGEON_PARENT } from "./dungeon-parent";

/**
 * 町・村の家に、全部入れるようにする（2026-10-04、人間の依頼）。
 * 家の玄関（家の足元のすぐ下のマス）が出入り口になり、家の中（小さな部屋）へ入る。家の中には、住んでいる人が1人いて、
 * 3軒に1軒は、すみに宝箱（小さな灯貨）がある。部屋は軒ごとに、家具の置き方がかわる。
 */
const FLOOR = 1;
const WALL = 2;
const W = 11;
const H = 8;
const DOOR_X = 5;

const RESIDENTS: { name: string; line: string }[] = [
  { name: "おばあさん", line: "いらっしゃい。お茶でも飲んでいくかい？ 外は、風がつめたくなってきたねえ。" },
  { name: "おじいさん", line: "この家は、わしの爺さんの代から、ずっとここにあるんじゃよ。" },
  { name: "主婦", line: "ちょうど、スープができたところなの。あとで近所にも、おすそ分けしなくちゃ。" },
  { name: "少年", line: "ぼく、大きくなったら調査員になるんだ！ 灯りの相談所って、かっこいいよね。" },
  { name: "旅の人", line: "宿が満員でね。この家に、泊めてもらっているんだ。" },
  { name: "職人", line: "ひと仕事、終わったところさ。灯り石をみがくのは、根気のいる仕事でね。" },
  { name: "むすめ", line: "窓から見える夕方の空の色が好きなの。毎日ちがう色なのよ。" },
  { name: "おじさん", line: "うちの猫を見なかったかい？ ……ああ、そこの棚の上にいたよ。" },
];

const SHELF_LINES = [
  "本棚には、古い本がならんでいる。『湖のほとりの釣りのコツ』という本がある。",
  "本棚には、灯り石の手入れの本がならんでいる。読んだあとが、たくさん残っている。",
  "本棚には、子ども向けの絵本がならんでいる。『灯の環のおはなし』という本がある。",
  "本棚には、旅の地図と、すりきれた日記帳がならんでいる。",
];
const TANSU_LINES = [
  "箪笥には、きれいにたたんだ服が入っている。",
  "箪笥の上に、小さな写し絵がかざってある。家族のようだ。",
  "引き出しには、ほしぶどうと、くるみが入っている。",
  "箪笥には、冬用の厚い上着がしまってある。",
];
const TABLE_LINES = [
  "テーブルの上に、お茶のしたくがしてある。ポットは、まだあたたかい。",
  "テーブルの上に、ろうそくと、飲みかけのお茶がある。",
  "テーブルには、きれいなクロスがかけてある。ふちの赤い刺しゅうが、かわいい。",
  "テーブルの上に、焼きたてのパンが、かごに入っている。",
];
const BED_LINES = [
  "ふかふかのベッドだ。お日さまのにおいがする。",
  "きれいにととのえられたベッドだ。",
  "まくらもとに、読みかけの本が置いてある。",
  "あたたかそうなベッドだ。ちょっと眠くなる。",
];

const FURNITURE: MapProp["kind"][] = ["barrel", "crates", "bench", "flowerbed", "barrel", "crates"];

function isTown(mapId: string): boolean {
  return (/-(town|village)$/.test(mapId) || /^village-/.test(mapId)) && mapId !== "world-map";
}

function interiorMap(town: string, ret: { x: number; y: number }, seed: number): TileMapData {
  const ground = new Array<number>(W * H).fill(FLOOR);
  const collision = new Array<number>(W * H).fill(0);
  for (let x = 0; x < W; x++) {
    ground[x] = WALL;
    collision[x] = 1;
    ground[(H - 1) * W + x] = WALL;
    collision[(H - 1) * W + x] = 1;
  }
  for (let y = 0; y < H; y++) {
    ground[y * W] = WALL;
    collision[y * W] = 1;
    ground[y * W + W - 1] = WALL;
    collision[y * W + W - 1] = 1;
  }
  // 横にはばのある家具（本棚・箪笥・ベッド・テーブル）が、歩ける床にはみ出さないよう、となりのマスも通れなくする
  for (const [fx, fy] of [[1, 2], [3, 2], [4, 2], [6, 2], [7, 2], [9, 2], [7, 5], [9, 5]]) collision[fy * W + fx] = 1;
  ground[(H - 1) * W + DOOR_X] = FLOOR; // 玄関
  collision[(H - 1) * W + DOOR_X] = 0;
  // 家具: 奥の壁ぎわの左右に、種類・位置がかわる
  const props: MapProp[] = [];
  const spots: Array<[number, number]> = [[1, 5], [1, 6], [2, 6], [9, 6], [8, 6]];
  const used: Array<[number, number]> = [];
  for (let i = 0; i < 2; i++) {
    const [x, y] = spots[(hashCell(seed + i, 3) + i * 2) % spots.length];
    if (used.some(([ux, uy]) => ux === x && uy === y)) continue;
    used.push([x, y]);
    props.push({ kind: FURNITURE[hashCell(seed, i + 9) % FURNITURE.length], tileX: x, tileY: y });
    collision[y * W + x] = 1;
  }
  return {
    width: W,
    height: H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { [FLOOR]: "#9a7a4a", [WALL]: "#6a5a4a" },
    tileArt: { [FLOOR]: "tint:plank", [WALL]: "tint:brick" },
    theme: "interior",
    collision,
    props,
    exits: [{ tileX: DOOR_X, tileY: H - 1, targetMapId: town, targetTileX: ret.x, targetTileY: ret.y }],
  };
}

export function addHouseInteriors(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  for (const [mapId, data] of Object.entries(maps)) {
    if (!isTown(mapId) || !data.props || !data.collision) continue;
    const w = data.width;
    const h = data.height;
    const exits = data.exits ?? (data.exits = []);
    const npcs = npcsByMap[mapId] ?? [];
    const exitAt = (x: number, y: number): boolean => exits.some((e) => e.tileX === x && e.tileY === y);
    const walkable = (x: number, y: number): boolean => x >= 0 && y >= 0 && x < w && y < h && data.collision![y * w + x] === 0;
    let n = 0;
    for (const prop of [...data.props]) {
      if (!isHouse(prop.kind)) continue;
      const door = { x: prop.tileX, y: prop.tileY + 1 };
      if (!walkable(door.x, door.y) || exitAt(door.x, door.y) || npcs.some((p) => p.tileX === door.x && p.tileY === door.y)) continue;
      // 玄関の前に、すでに別の出入り口があるとき（相談所など）は、そちらにまかせる
      if (exits.some((e) => Math.abs(e.tileX - door.x) <= 1 && Math.abs(e.tileY - door.y) <= 1)) continue;
      n++;
      const id = `house-${mapId}-${n}`;
      const seed = hashCell(prop.tileX * 31 + n, prop.tileY * 17 + mapId.length);
      // 外へ出たときの立ち位置: 玄関の前の、あいている（人も出入り口もない）マス
      const free = (x: number, y: number): boolean => walkable(x, y) && !exitAt(x, y) && !npcs.some((p) => p.tileX === x && p.tileY === y);
      const ret = [[0, 1], [-1, 1], [1, 1], [0, 2], [-1, 0], [1, 0], [-2, 1], [2, 1]]
        .map(([dx, dy]) => ({ x: door.x + dx, y: door.y + dy }))
        .find((c) => free(c.x, c.y));
      if (!ret) continue;
      exits.push({ tileX: door.x, tileY: door.y, targetMapId: id, targetTileX: DOOR_X, targetTileY: H - 2, enter: "up" });
      maps[id] = interiorMap(mapId, ret, seed);
      DUNGEON_PARENT[id] = mapId; // 曲は、町と同じ
      const resident = RESIDENTS[seed % RESIDENTS.length];
      const list: Npc[] = [
        {
          id: `${id}-resident`,
          tileX: 3 + (seed % 3),
          tileY: 4,
          color: ["#c08060", "#6a8ab0", "#a0a070", "#b07090", "#7a9a6a"][seed % 5],
          commands: [{ type: "message", text: resident.line, speaker: resident.name }],
        },
      ];
      // 家具（調べられる）: 奥の壁ぎわに、本棚・箪笥・ベッド。箪笥には、小さな灯貨が入っていることがある
      list.push({ id: `${id}-shelf`, tileX: 2, tileY: 2, color: "#7a5228", commands: [{ type: "message", text: SHELF_LINES[seed % SHELF_LINES.length] }] });
      if (seed % 3 === 0) {
        const gold = 15 + (seed % 4) * 10;
        list.push(chestNpc(`${id}-tansu`, { tileX: 5, tileY: 2 }, `${id}_tansu`, { gold }, "箪笥の引き出しを開けた！"));
      } else {
        list.push({ id: `${id}-tansu`, tileX: 5, tileY: 2, color: "#b07a44", commands: [{ type: "message", text: TANSU_LINES[seed % TANSU_LINES.length] }] });
      }
      list.push({ id: `${id}-table`, tileX: 8, tileY: 5, color: "#d8cbb0", commands: [{ type: "message", text: TABLE_LINES[seed % TABLE_LINES.length] }] });
      list.push({ id: `${id}-bed`, tileX: 8, tileY: 2, color: ["#6a8ab0", "#b07090", "#7a9a6a", "#c0a050"][seed % 4], commands: [{ type: "message", text: BED_LINES[seed % BED_LINES.length] }] });
      npcsByMap[id] = list;
    }
  }
}
