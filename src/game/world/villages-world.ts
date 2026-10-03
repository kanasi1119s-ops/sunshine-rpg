import { WORLD_VILLAGES } from "../map/world/world-map.generated";
import { MAP_PROPS } from "../map/map-props";
import type { MapProp, TileMapData } from "../map/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 小さな町・村（世界地図に8か所）。どこも小さな1画面で、町の人が3人、土地のくらしと、大陸のうわさ（船・飛空艇・環灯台・小島のヒント）を話す。
 * 物語の進行には関わらない（いつ来てもよい）。大陸のあいだは海なので、船・飛空艇がないと、別の大陸の村へは行けない。
 */
type Theme = "grass" | "desert" | "snow";

interface VillageDef {
  theme: Theme;
  /** 3人の町の人: [名前, 性格の色, セリフ（複数）] */
  folks: Array<{ name: string; color: string; lines: string[]; pos: { tileX: number; tileY: number } }>;
}

const WIDTH = 18;
const HEIGHT = 13;
const GATE = { x: 9, y: HEIGHT - 1 };

const DEFS: Record<string, VillageDef> = {
  "village-namioto": {
    theme: "grass",
    folks: [
      { name: "漁師", color: "#e0a458", pos: { tileX: 6, tileY: 7 }, lines: ["ここは、灯里の東の浜さ。海の向こうが見えるだろう。", "沖のほうで、ずっと昔から渦が回りっぱなしでな。あの渦の真ん中に、塔があると、年寄りは言うんだ。"] },
      { name: "網つくろいの女", color: "#c8a0a0", pos: { tileX: 12, tileY: 8 }, lines: ["砂音の船大工のおじいさんは、昔は大きな船を出していたのよ。", "いまは、帆と舵がなくて、船を動かせないって、嘆いていたわ。"] },
      { name: "子ども", color: "#a0c8e0", pos: { tileX: 5, tileY: 10 }, lines: ["ねえ、海のむこうの小さな島、見えた？ あそこには、昔のお宝があるんだって！", "でも、船がないと行けないんだ。いいなあ、船。"] },
    ],
  },
  "village-kazami": {
    theme: "grass",
    folks: [
      { name: "風車守", color: "#d8c890", pos: { tileX: 7, tileY: 6 }, lines: ["この風車は、麦香野の水路が涸れる前から、ずっと回っていてね。", "風の道が見える丘だよ。風が歌うと、天気が分かる。"] },
      { name: "旅の絵描き", color: "#a0a0d8", pos: { tileX: 12, tileY: 9 }, lines: ["大陸の真ん中の高い山脈は、歩いては越えられない。道がある場所だけを通るんだ。", "山の向こうの、深い谷にも、行ってみたいが……落ちたら、戻れないそうだ。"] },
      { name: "少女", color: "#e8b0c8", pos: { tileX: 5, tileY: 10 }, lines: ["谷にはね、大きなひび割れがあるの。のぞくと、風の音がするんだよ。"] },
    ],
  },
  "village-tomoshimori": {
    theme: "grass",
    folks: [
      { name: "宿の主人", color: "#c89a68", pos: { tileX: 7, tileY: 6 }, lines: ["旅の方、ここは街道の宿場だ。ゆっくり休んでいくといい。（泊まる仕組みは、まだ仮だ）"] },
      { name: "行商人", color: "#d8b050", pos: { tileX: 12, tileY: 8 }, lines: ["大陸と大陸のあいだは、海さ。渡るには、船がいる。", "砂音の近くの海岸に、古い船が置いてあるそうだ。直せば、動くらしい。"] },
      { name: "物知りの老人", color: "#b8b8c8", pos: { tileX: 5, tileY: 10 }, lines: ["環灯台、というのを知っておるか。大陸の海辺に、八つある古い灯台じゃ。", "いまは、光がない。だが、昔は、ひとつの光の環をなしていたという。"] },
    ],
  },
  "village-samori": {
    theme: "desert",
    folks: [
      { name: "水汲みの男", color: "#c8b078", pos: { tileX: 7, tileY: 6 }, lines: ["この泉は、砂漠の民の命だ。砂音の町よりも、ずっと古いんだぞ。"] },
      { name: "帆職人の弟子", color: "#e0d0a0", pos: { tileX: 12, tileY: 8 }, lines: ["帆の布は、この泉の水で洗うと、丈夫になるんだ。", "砂音の帆職人のおかみさんは、ここの水で、世界一の帆を縫うんだよ。"] },
      { name: "ラクダ使い", color: "#a88858", pos: { tileX: 5, tileY: 10 }, lines: ["砂漠の風は、夜になると、ぴたりと止む。船乗りは、『風の歌が止むと、海も黙る』と言うな。"] },
    ],
  },
  "village-kirima": {
    theme: "grass",
    folks: [
      { name: "霧の番人", color: "#a8b8c8", pos: { tileX: 7, tileY: 6 }, lines: ["霧断崖の古都へ行くなら、霧の薄い朝がいい。昼は、足元も見えなくなる。"] },
      { name: "薬草売り", color: "#98c898", pos: { tileX: 12, tileY: 8 }, lines: ["崖の下の谷は、通れないよ。上の道を、まっすぐ行きなさい。", "この大陸は、山と谷が多いんだ。道を外れると、戻れなくなる。"] },
      { name: "猟師", color: "#a89880", pos: { tileX: 5, tileY: 10 }, lines: ["北の雪原では、ときどき、空を船のような影が飛んでいくのを見る。", "……いや、見間違いかもしれんがね。"] },
    ],
  },
  "village-yukimachi": {
    theme: "snow",
    folks: [
      { name: "老人", color: "#d8d8e0", pos: { tileX: 7, tileY: 6 }, lines: ["霜原の北には、大昔の戦の跡がある。雪の下には、いまも、折れた剣が眠っておる。"] },
      { name: "毛皮商人", color: "#b08868", pos: { tileX: 12, tileY: 8 }, lines: ["雪が深くなる前に、技師さんが、霜原の施設へよく通っていたよ。何かを組み立てているらしい。"] },
      { name: "子ども", color: "#c0d8f0", pos: { tileX: 5, tileY: 10 }, lines: ["雪の下にはね、空から落ちた石が埋まってるんだって！ ふわふわ浮くんだよ。"] },
    ],
  },
  "village-minori": {
    theme: "grass",
    folks: [
      { name: "農夫", color: "#c8b868", pos: { tileX: 7, tileY: 6 }, lines: ["灯芯都の南は、実りの豊かな土地さ。麦も、果物も、よく育つ。"] },
      { name: "騎士見習い", color: "#98a8c8", pos: { tileX: 12, tileY: 8 }, lines: ["東の荒れ地には、古い宮殿があるんだ。まだ、普通の人は近づけないんだよ。"] },
      { name: "行商人", color: "#d8b050", pos: { tileX: 5, tileY: 10 }, lines: ["大陸の東の空に、雲のような島が浮いている。あそこへは、空からでないと行けないそうだ。"] },
    ],
  },
  "village-arano": {
    theme: "desert",
    folks: [
      { name: "市の商人", color: "#d09848", pos: { tileX: 7, tileY: 6 }, lines: ["ここは、荒れ地の市。いろんな土地の品が集まるよ。"] },
      { name: "占い師", color: "#b898d8", pos: { tileX: 12, tileY: 8 }, lines: ["……見えるわ。八つの灯台に光がともるとき、海のまんなかの嵐が、道をあける。"] },
      { name: "傭兵", color: "#8890a0", pos: { tileX: 5, tileY: 10 }, lines: ["忘れられた砦の島は、空から行くしかない。海からでは、近づけないらしい。"] },
    ],
  },
};

const THEME_COLORS: Record<Theme, { ground: string; path: string; border: string }> = {
  grass: { ground: "#4a9a3a", path: "#b3853f", border: "#2f7a2a" },
  desert: { ground: "#d9bf82", path: "#c2a05c", border: "#857c74" },
  snow: { ground: "#e8eef2", path: "#b9b5a8", border: "#3a6a50" },
};
const THEME_ART: Record<Theme, { ground: string; path: string; border: string }> = {
  grass: { ground: "grass", path: "path", border: "worldforest" },
  desert: { ground: "tint:sand", path: "tint:sand", border: "mountain" },
  snow: { ground: "tint:snow", path: "tint:flagstone", border: "snowforest" },
};

function propsFor(theme: Theme): MapProp[] {
  const houseKinds: MapProp["kind"][] = theme === "snow" ? ["house-blue", "house-blue"] : theme === "desert" ? ["house", "house"] : ["house", "house-green"];
  const tree: MapProp["kind"] = theme === "snow" ? "tree-snow" : theme === "desert" ? "palm" : "tree";
  const rock: MapProp["kind"] = theme === "snow" ? "rock-snow" : "rock";
  return [
    { kind: houseKinds[0], tileX: 3, tileY: 4 },
    { kind: houseKinds[1], tileX: 14, tileY: 4 },
    { kind: tree, tileX: 2, tileY: 11 },
    { kind: tree, tileX: 15, tileY: 11 },
    { kind: rock, tileX: 16, tileY: 7 },
    { kind: theme === "snow" ? "tree-dead" : "lamp", tileX: 8, tileY: 6 },
    { kind: "barrel", tileX: 1, tileY: 7 },
    { kind: theme === "desert" ? "cactus" : "signpost", tileX: 10, tileY: 10 },
  ];
}

function createVillageData(theme: Theme): TileMapData {
  const ground = new Array(WIDTH * HEIGHT).fill(1);
  const collision = new Array(WIDTH * HEIGHT).fill(0);
  const set = (x: number, y: number, tile: number): void => {
    ground[y * WIDTH + x] = tile;
    collision[y * WIDTH + x] = tile === 4 ? 1 : 0;
  };
  for (let x = 0; x < WIDTH; x++) {
    set(x, 0, 4);
    set(x, HEIGHT - 1, x === GATE.x ? 2 : 4);
  }
  for (let y = 0; y < HEIGHT; y++) {
    set(0, y, 4);
    set(WIDTH - 1, y, 4);
  }
  for (let y = 1; y < HEIGHT; y++) set(GATE.x, y, 2);
  for (let x = 1; x < WIDTH - 1; x++) set(x, 7, 2);
  const c = THEME_COLORS[theme];
  const a = THEME_ART[theme];
  return {
    width: WIDTH,
    height: HEIGHT,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: { 1: c.ground, 2: c.path, 4: c.border },
    tileArt: { 1: a.ground, 2: a.path, 4: a.border },
    collision,
    // 世界地図への出入り口は、`connectWorldMap`（world-map-world.ts）が南の門に足す。ここでは、通路の最初の出入り口として仮に置く。
    exits: [{ tileX: GATE.x, tileY: GATE.y, targetMapId: "world-map", targetTileX: 0, targetTileY: 0 }],
    snowy: theme === "snow",
  };
}

export const VILLAGE_MAPS: Record<string, TileMapData> = Object.fromEntries(
  WORLD_VILLAGES.map((v) => [v.id, createVillageData(DEFS[v.id].theme)]),
);

for (const v of WORLD_VILLAGES) {
  MAP_PROPS[v.id] = propsFor(DEFS[v.id].theme);
}

export const VILLAGE_NPCS: Record<string, Npc[]> = Object.fromEntries(
  WORLD_VILLAGES.map((v) => [
    v.id,
    DEFS[v.id].folks.map((f, i) => ({
      id: `${v.id}-folk${i + 1}`,
      tileX: f.pos.tileX,
      tileY: f.pos.tileY,
      color: f.color,
      wander: true,
      commands: f.lines.map((t) => say(f.name, t)),
    })),
  ]),
);
