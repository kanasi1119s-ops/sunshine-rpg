import { WORLD_AIRSHIP_START, WORLD_BEACONS, WORLD_ISLETS, WORLD_SHIP_DOCK, WORLD_TOWER, WORLD_TOWNS, WORLD_VILLAGES } from "../map/world/world-map.generated";
import { DEEP_ENTRY } from "../map/chapter10/deep-maps";
import { isletRequirementHint } from "./islets-world";
import { GODS } from "../battle/chapter11-enemies";
import type { EventCommand } from "../event/types";
import type { MapProp, TileMapData } from "../map/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 世界地図（大陸アルテシア）のつなぎと、クリア後の「渦への航路」のイベント（`docs/story/secret-boss.md` 4-2b）。
 *  - 各町の南の門と、世界地図の町のアイコンをつなぐ。
 *  - 8神の欠片を、各地方にある「環灯台」にささげる（8つ）。8つともともると、渦を覆う常嵐が割れ、渡し場から芯環塔へ船が出る。
 *  - 虚灯宮・深部の転移陣（`chapter10-world.ts`）は、欠片8つに加えて、この航路が開いていないと起動しない。
 */

/** 世界地図から町へ入るために、前の章を終えている必要があるフラグ（なければ入れない）。章は、この順に進む。 */
export const WORLD_ENTRY_FLAG: Record<string, string> = {
  "mugikano-village": "chapter0_reported_to_kasen",
  "garasuko-town": "chapter1_reported_to_elder",
  "tetsukusari-town": "chapter2_reported_to_guide",
  "sanone-town": "chapter3_reported_to_orca",
  "kiri-town": "chapter4_reported",
  "shimohara-town": "chapter5_reported",
  "fushima-town": "chapter6_reported",
  "toushin-town": "chapter7_reported",
  "kyotoukyu-court": "chapter8_reported",
};

/**
 * 世界地図の出入り口に入るための条件が足りないとき、そのヒント（複数）を返す。空なら入れる。
 *  - 町: 前の章を終えていること（章は順番に進む）。
 *  - 霧断崖・霜原（北東の大陸）: 船が要る／浮嶼（空の島々）: 飛空艇が要る（行き方そのものが、乗り物を要求する）。
 *  - 隠しダンジョンの小島: 乗り物と、物語の進み具合（`islets-world.ts`）。
 *  - 芯環塔: 8つの環灯台がともり、渦の嵐が割れていること。
 */
export function worldEntryProblems(targetMapId: string, flags: Record<string, boolean>): string[] {
  if (targetMapId.startsWith("islet-")) {
    return isletRequirementHint(targetMapId, flags);
  }
  if (targetMapId === "tower-1") {
    return flags["vortex_route_open"] ? [] : ["渦を覆う嵐が、行く手をふさいでいる。8つの環灯台に、光をともさなければ。"];
  }
  const need = WORLD_ENTRY_FLAG[targetMapId];
  return need && !flags[need] ? ["まだ、この先へ進む時ではない気がする。いまの町で、やるべきことを終えてから来よう。"] : [];
}

/** 環灯台の番号（神の番号）と、置かれる地方。 */
const BEACON_REGIONS = ["麦香野", "硝子湖", "鉄鏈鉱山", "砂音", "霧断崖", "霜原", "浮嶼", "灯芯都"];

/** 環灯台に灯る光の色（神ごと）。 */
export const BEACON_COLORS = ["#a8e070", "#7ad0e8", "#f08a3c", "#c8c0f0", "#f4f0d8", "#e0584c", "#d890f0", "#8a98c8"];

const ROUTE_LINES = [
  "ひとつ、水は高みから低みへ。流れに逆らわず、海へ出よ。",
  "ふたつ、羽音の止む朝に、霧は薄れる。",
  "みっつ、火は海を照らす道となる。",
  "よっつ、風の歌の止む夜に、海は黙る。",
  "いつつ、誓いは羅針となる。",
  "むっつ、争いの果ての岸辺を過ぎよ。",
  "ななつ、境を見ぬ者が、渦の目を教える。",
  "やっつ、鐘の鳴らぬ潮に、舟は沈まない。",
];

const beaconFlag = (no: number): string => `beacon${no}_lit`;

function allLitThen(then: EventCommand[], no: number): EventCommand[] {
  // 自分以外の7つが、すでにともっているか。
  let inner: EventCommand[] = then;
  for (let n = 8; n >= 1; n--) {
    if (n === no) continue;
    inner = [{ type: "if", flag: beaconFlag(n), equals: true, then: inner }];
  }
  return inner;
}

function beacon(no: number, pos: { x: number; y: number }): Npc {
  const god = GODS[no - 1];
  const region = BEACON_REGIONS[no - 1];
  return {
    id: `world-beacon-${no}`,
    tileX: pos.x,
    tileY: pos.y,
    color: BEACON_COLORS[no - 1],
    commands: [
      {
        type: "if",
        flag: "deep_yugami_defeated",
        equals: true,
        then: [
          {
            type: "if",
            flag: beaconFlag(no),
            equals: true,
            then: [say(undefined, `${region}の環灯台は、${god.kind}の光で、海をまっすぐに照らしている。`), say(undefined, `「${ROUTE_LINES[no - 1]}」`)],
            else: [
              {
                type: "if",
                flag: `god${no}_fragment`,
                equals: true,
                then: [
                  say(undefined, `${region}の海辺に、古い灯台が立っている。台座のくぼみが、${god.kind}の欠片と、ぴったり合う。`),
                  say(undefined, `欠片を台座に置くと、${god.kind}の光が塔をかけ上がり、海へ、一本の光の道をのばした。`),
                  say(undefined, `台座に、古い文字が浮かぶ。「${ROUTE_LINES[no - 1]}」`),
                  { type: "setFlag", flag: beaconFlag(no), value: true },
                  ...allLitThen(
                    [
                      say(undefined, "八つの環灯台の光が、海の上で、ひとつの環になった。"),
                      say(undefined, "遠い水平線で、渦を覆っていた常嵐が、音もなく、割れていく。"),
                      say(undefined, "★ 渦への航路が開いた！ 東の渡し場へ行こう。"),
                      { type: "setFlag", flag: "vortex_route_open", value: true },
                    ],
                    no,
                  ),
                ],
                else: [
                  say(undefined, `${region}の海辺に、古い灯台が立っている。台座のくぼみは、まだ空だ。`),
                  say(undefined, `${god.kind}を鎮めて、環の欠片を持ち帰れば、ここに光がともるだろう。`),
                ],
              },
            ],
          },
        ],
        else: [say(undefined, `${region}の海辺に、光のない古い灯台が立っている。いまは、ただの古い石塔だ。`)],
      },
    ],
  };
}

/** 船大工。船の部品（帆・舵）がそろい、砂音の件が終わっていれば、帆走船「渡り鳥号」を渡してくれる。 */
function shipwright(): Npc {
  return {
    id: "world-shipwright",
    tileX: WORLD_SHIP_DOCK.x,
    tileY: WORLD_SHIP_DOCK.y,
    color: "#8a6a40",
    commands: [
      {
        type: "if",
        flag: "has_ship",
        equals: true,
        then: [say("船大工", "渡り鳥号は、桟橋につないである。海へ出るなら、船のところまで歩いていきな。海岸ぞいに着けば、自分で降りられる。")],
        else: [
          {
            type: "if",
            flag: "chapter4_reported",
            equals: true,
            then: [
              {
                type: "if",
                flag: "ship_sail",
                equals: true,
                then: [
                  {
                    type: "if",
                    flag: "ship_helm",
                    equals: true,
                    then: [
                      say("船大工", "おお、砂音の帆と、鉄鏈の舵か。……ぴったりだ。これで、わしの船が、また海に出られる。"),
                      say(undefined, "古い帆走船が、桟橋で、ゆっくり帆を広げた。環の輪の紋様が、風をはらむ。"),
                      say("船大工", "名前は『渡り鳥号』。陸のあちこちへ、渡ってゆけ。海には、陸とは違う魔物もいる。気をつけな。"),
                      say(undefined, "★ 船を手に入れた！ 桟橋のとなりの海で、船にのれる。船は、海と、海ぞいの陸を行ける。"),
                      { type: "setFlag", flag: "has_ship", value: true },
                    ],
                    else: [say("船大工", "帆はそろったが、舵がない。鉄鏈鉱山の鍛冶屋が、舵を打てると聞いた。会ってきてくれ。")],
                  },
                ],
                else: [
                  {
                    type: "if",
                    flag: "ship_helm",
                    equals: true,
                    then: [say("船大工", "舵はそろったな。あとは、帆だ。砂音の帆職人なら、砂漠の風で鍛えた丈夫な帆を縫える。")],
                    else: [say("船大工", "船は直せる。だが、帆と舵がない。帆は砂音の帆職人、舵は鉄鏈鉱山の鍛冶屋を訪ねてくれ。")],
                  },
                ],
              },
            ],
            else: [say("船大工", "古い船が1隻ある。直せば海に出られるが、部品を集めるあてがなくてな。……砂音の件が片づいたら、また来てくれ。")],
          },
        ],
      },
    ],
  };
}

/** 飛空艇の技師。霜原の件が終わり、船を手に入れていれば、飛空艇を渡してくれる。 */
function airshipEngineer(): Npc {
  return {
    id: "world-airship-engineer",
    tileX: WORLD_AIRSHIP_START.x - 1,
    tileY: WORLD_AIRSHIP_START.y,
    color: "#7a8aa0",
    commands: [
      {
        type: "if",
        flag: "has_airship",
        equals: true,
        then: [say("技師", "『風切り号』は、いつでも飛べる。空では、上昇するのも降りるのも、船より自由だ。降りたいところで、決定ボタンを押せばいい。")],
        else: [
          {
            type: "if",
            flag: "chapter6_reported",
            equals: true,
            then: [
              {
                type: "if",
                flag: "has_ship",
                equals: true,
                then: [
                  say("技師", "霜原の施設で見つけた浮力の石を、この船体に組みこんでみた。海を渡ってきたあんたたちなら、乗りこなせるだろう。"),
                  say(undefined, "雪原に、翼のある船が横たわっている。灯の環の輪が、機体に刻まれている。"),
                  say("技師", "名前は『風切り号』。空を行けば、浮嶼にも渡れる。嵐のそばは、まだ危ない。気をつけな。"),
                  say(undefined, "★ 飛空艇を手に入れた！ 地図の飛空艇に乗って、決定ボタンで着陸できる。空には、空の魔物がいる。"),
                  { type: "setFlag", flag: "has_airship", value: true },
                ],
                else: [say("技師", "浮力の石を組みこんだ船体はできた。だが、海を越える経験のない者に、空は任せられん。まず、船で海を渡ってこい。")],
              },
            ],
            else: [say("技師", "雪原の施設の奥から、不思議な石が見つかってな。この船体に使えそうなんだが、まだ誰にも任せられない。霜原の件が片づいたら、また来てくれ。")],
          },
        ],
      },
    ],
  };
}

/** 砂音の帆職人・鉄鏈鉱山の鍛冶屋（船の部品をくれる人）。町の地図に足す。 */
export const SHIP_PART_NPCS: Record<string, Npc[]> = {
  "sanone-town": [
    {
      id: "sanone-sailmaker",
      tileX: 4,
      tileY: 9,
      color: "#d8c890",
      commands: [
        {
          type: "if",
          flag: "ship_sail",
          equals: true,
          then: [say("帆職人", "帆は渡したね。風をつかむ帆だよ。海でも、きっと丈夫さ。")],
          else: [
            {
              type: "if",
              flag: "chapter4_reported",
              equals: true,
              then: [
                say("帆職人", "船大工が、帆を探している？ ……そうかい、あの古い船が、また海へ出るのかい。"),
                say("帆職人", "砂嵐に何度も耐えた布で縫った、とっておきの帆がある。持っていきな。船乗りが、帆に力を借りるのを、昔はよく見たもんだ。"),
                say(undefined, "★ 帆を手に入れた！（船の部品 1/2）"),
                { type: "setFlag", flag: "ship_sail", value: true },
              ],
              else: [say("帆職人", "砂漠の風は、気まぐれだよ。この町の件が、落ち着いたら、また話を聞かせておくれ。")],
            },
          ],
        },
      ],
    },
  ],
  "tetsukusari-town": [
    {
      id: "tetsukusari-helmsmith",
      tileX: 17,
      tileY: 9,
      color: "#9a7a5a",
      commands: [
        {
          type: "if",
          flag: "ship_helm",
          equals: true,
          then: [say("鍛冶屋", "舵は渡したな。鉄鏈でも錆びない鉄で打った、自慢の舵だ。")],
          else: [
            {
              type: "if",
              flag: "chapter4_reported",
              equals: true,
              then: [
                say("鍛冶屋", "船の舵？ ……この鉱山の鉄で、か。いい仕事だ。灯り石の粉を混ぜて、海の塩にも負けないように打ってある。持っていけ。"),
                say(undefined, "★ 舵を手に入れた！（船の部品 2/2）"),
                { type: "setFlag", flag: "ship_helm", value: true },
              ],
              else: [say("鍛冶屋", "いまは、鉱山の騒ぎで手がいっぱいだ。砂音の件が片づいてからなら、舵くらい打ってやる。")],
            },
          ],
        },
      ],
    },
  ],
};

export const WORLD_MAP_NPCS: Record<string, Npc[]> = {
  "world-map": WORLD_BEACONS.map((pos, i) => beacon(i + 1, pos)),
};

/**
 * 船大工・飛空艇の技師の住まい（2026-10-05、人間の指示「飛空艇をくれた人と、船をくれた人には祠に住んでもらい、祠の中で話す」
 * →「船をくれる人は小屋の方がいいか。小屋を丁寧に作って」）。技師は祠、船大工は桟橋のとなりの小屋（`prop:icon-hut`）。
 * 世界地図のもとの立ち位置のとなりにアイコンを置き、入ると小さな部屋。話は部屋の中でする。
 */
export const KEEPER_SHRINES: { mapId: string; icon: MapProp["kind"]; style: "hut" | "shrine"; world: { x: number; y: number }; back: { x: number; y: number }; npc: () => Npc; banner: MapProp["kind"] }[] = [
  { mapId: "shipwright-hut", icon: "icon-hut", style: "hut", world: { x: WORLD_SHIP_DOCK.x - 1, y: WORLD_SHIP_DOCK.y }, back: { x: WORLD_SHIP_DOCK.x - 1, y: WORLD_SHIP_DOCK.y + 1 }, npc: shipwright, banner: "banner-red" },
  { mapId: "keeper-shrine-sky", icon: "icon-shrine", style: "shrine", world: { x: WORLD_AIRSHIP_START.x - 2, y: WORLD_AIRSHIP_START.y }, back: { x: WORLD_AIRSHIP_START.x - 2, y: WORLD_AIRSHIP_START.y + 1 }, npc: airshipEngineer, banner: "banner-purple" },
];
const KS_W = 11;
const KS_H = 8;
const KS_DOOR_X = 5;

function keeperShrineMap(back: { x: number; y: number }, banner: MapProp["kind"], style: "hut" | "shrine"): TileMapData {
  const FLOOR = 1;
  const WALL = 2;
  const ground = new Array<number>(KS_W * KS_H).fill(FLOOR);
  const collision = new Array<number>(KS_W * KS_H).fill(0);
  const block = (x: number, y: number): void => {
    collision[y * KS_W + x] = 1;
  };
  for (let x = 0; x < KS_W; x++) {
    for (const y of [0, 1, KS_H - 1]) {
      ground[y * KS_W + x] = WALL;
      block(x, y);
    }
  }
  for (let y = 0; y < KS_H; y++) {
    ground[y * KS_W] = WALL;
    ground[y * KS_W + KS_W - 1] = WALL;
    block(0, y);
    block(KS_W - 1, y);
  }
  ground[(KS_H - 1) * KS_W + KS_DOOR_X] = FLOOR;
  collision[(KS_H - 1) * KS_W + KS_DOOR_X] = 0;
  // 小屋: 船大工の仕事場（樽・木箱・作業台がわりの長いす・灯・道しるべ（船の図面板））
  const hutProps: MapProp[] = [
    { kind: "crates", tileX: 1, tileY: 2 },
    { kind: "barrel", tileX: 2, tileY: 2 },
    { kind: "bench", tileX: 4, tileY: 2 },
    { kind: "noticeboard", tileX: 6, tileY: 2 },
    { kind: "lamp", tileX: 8, tileY: 2 },
    { kind: "barrel", tileX: 9, tileY: 2 },
    { kind: "crates", tileX: 9, tileY: 6 },
    { kind: "barrel", tileX: 1, tileY: 6 },
  ];
  // 祠: 奥のまんなかに小さな祭壇（灯の環）、左右に燭台・柱・旗、手前の角に火皿
  const props: MapProp[] = style === "hut" ? hutProps : [
    { kind: "shrine", tileX: 5, tileY: 2 },
    { kind: "candelabra", tileX: 3, tileY: 2 },
    { kind: "candelabra", tileX: 7, tileY: 2 },
    { kind: "pillar", tileX: 1, tileY: 2 },
    { kind: "pillar", tileX: 9, tileY: 2 },
    { kind: banner, tileX: 2, tileY: 2 },
    { kind: banner, tileX: 8, tileY: 2 },
    { kind: "brazier", tileX: 1, tileY: 6 },
    { kind: "brazier", tileX: 9, tileY: 6 },
  ];
  for (const p of props) block(p.tileX, p.tileY);
  return {
    width: KS_W,
    height: KS_H,
    tileWidth: 16,
    tileHeight: 16,
    layers: [{ name: "ground", data: ground }],
    tileColors: style === "hut" ? { [FLOOR]: "#9a7a4a", [WALL]: "#6a4a2c" } : { [FLOOR]: "#8a8478", [WALL]: "#5a5450" },
    tileArt: style === "hut" ? { [FLOOR]: "tint:plank", [WALL]: "tint:plank" } : { [FLOOR]: "tint:flagstone", [WALL]: "tint:brick" },
    theme: "interior",
    collision,
    props,
    exits: [{ tileX: KS_DOOR_X, tileY: KS_H - 1, targetMapId: "world-map", targetTileX: back.x, targetTileY: back.y }],
  };
}

/** 祠を世界地図に置き、中の地図と、住む人を足す。世界地図をつないだあと（connectWorldMap のあと）に呼ぶ。 */
export function addKeeperShrines(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  const world = maps["world-map"];
  for (const k of KEEPER_SHRINES) {
    maps[k.mapId] = keeperShrineMap(k.back, k.banner, k.style);
    npcsByMap[k.mapId] = [{ ...k.npc(), tileX: KS_DOOR_X, tileY: 4 }];
    (world.props ??= []).push({ kind: k.icon, tileX: k.world.x, tileY: k.world.y });
    (world.exits ??= []).push({ tileX: k.world.x, tileY: k.world.y, targetMapId: k.mapId, targetTileX: KS_DOOR_X, targetTileY: KS_H - 2, enter: "up" });
  }
}

/**
 * 世界地図と各町を、出入り口でつなぐ。町の地図の南のふち（真ん中から近い、通れる場所）に門を開け、
 * 世界地図の町のアイコンの下に着く。地図・飾りを作ったあとに呼ぶ。
 */
export function connectWorldMap(maps: Record<string, TileMapData>, npcsByMap: Record<string, Npc[]>): void {
  const world = maps["world-map"];
  if (!world) {
    return;
  }
  const places: Array<[string, { x: number; y: number }]> = [...Object.entries(WORLD_TOWNS), ...WORLD_VILLAGES.map((v) => [v.id, v] as [string, { x: number; y: number }])];
  for (const [townId, pos] of places) {
    const data = maps[townId];
    if (!data) {
      continue;
    }
    // 村の仮の出入り口（行き先 0,0）は、歩ける範囲を調べる出発点にだけ使い、門ができたら取り除く
    const start = data.exits?.[0];
    data.exits = (data.exits ?? []).filter((e) => !(e.targetMapId === "world-map" && e.targetTileX === 0 && e.targetTileY === 0));
    const gate = findSouthGate(data, npcsByMap[townId] ?? [], start);
    if (!gate) {
      continue;
    }
    const w = data.width;
    // 町の側: 南のふちに門を開ける（下の通れるタイルと同じ地面にする）
    const below = (gate.y - 1) * w + gate.x;
    data.layers[0].data[gate.y * w + gate.x] = data.layers[0].data[below];
    data.collision![gate.y * w + gate.x] = 0;
    data.exits = [...(data.exits ?? []), { tileX: gate.x, tileY: gate.y, targetMapId: "world-map", targetTileX: pos.x, targetTileY: pos.y + 1 }];
    // 町と町を直接つなぐ街道の出口（東・西の端など）は、次の町へ瞬間移動せず、世界地図の自分の町のそばに出る（道を歩いて次の町へ行く）。
    data.exits = data.exits.map((e) =>
      e.targetMapId !== townId && e.targetMapId in WORLD_TOWNS ? { ...e, targetMapId: "world-map", targetTileX: pos.x, targetTileY: pos.y + 1 } : e,
    );
    // 世界地図の側: 町のアイコンの上が出入り口
    world.exits = [...(world.exits ?? []), { tileX: pos.x, tileY: pos.y, targetMapId: townId, targetTileX: gate.x, targetTileY: gate.y - 1 }];
  }
  connectDungeonsToWorld(world, maps);
  // 隠しダンジョンの小島の入口（島の中心）と、海のまんなかの芯環塔の入口
  for (const islet of WORLD_ISLETS) {
    world.exits = [...(world.exits ?? []), { tileX: islet.x, tileY: islet.y, targetMapId: `${islet.id}-1`, targetTileX: DEEP_ENTRY.tileX, targetTileY: DEEP_ENTRY.tileY }];
  }
  world.exits = [...(world.exits ?? []), { tileX: WORLD_TOWER.x, tileY: WORLD_TOWER.y, targetMapId: "tower-1", targetTileX: 10, targetTileY: 11 }];
}

/**
 * 章のダンジョンの入口は、町の門ではなく、世界地図の町のそば（フィールド）に置く（人間の指示「町の中からそのままダンジョンに行けるのはどうにかしたい」、2026-10-05）。
 * 町の側: ダンジョンへの門は、世界地図へ出る出口に変える。世界地図の側: 町から歩いて行ける、町のそばの地面にアイコンと入口を置く
 * （入るための条件 requireFlag はそのまま）。ダンジョンの側: 町へもどる出口は、世界地図の入口のそばに出る。
 */
export const DUNGEON_FROM_TOWN: Record<string, { dungeon: string; icon: MapProp["kind"] }> = {
  "touri-town": { dungeon: "touri-forest-1", icon: "icon-bigtree" },
  "mugikano-village": { dungeon: "mugikano-canal", icon: "icon-stones" },
  "garasuko-town": { dungeon: "garasuko-cave-1", icon: "icon-cave" },
  "tetsukusari-town": { dungeon: "tetsukusari-cave-1", icon: "icon-mine" },
  "sanone-town": { dungeon: "sanone-ruins-1", icon: "icon-ruin" },
  "kiri-town": { dungeon: "kiri-tower-1", icon: "icon-spire" },
  "shimohara-town": { dungeon: "shimohara-ruins-1", icon: "icon-ruin" },
  "fushima-town": { dungeon: "fushima-tower-1", icon: "icon-spire" },
  "toushin-town": { dungeon: "toushin-tower-1", icon: "icon-shrine" },
};

/** 世界地図で、町から歩いて行ける、町から3〜9マスはなれた地面（入口）と、そのすぐ手前の立つ場所。北（ダンジョンの門があった向き）を少し優先する。 */
function dungeonSpot(world: TileMapData, town: { x: number; y: number }, taken: Set<number>): { gate: { x: number; y: number }; stand: { x: number; y: number } } | null {
  const w = world.width, h = world.height;
  const col = world.collision ?? [];
  const start = { x: town.x, y: town.y + 1 };
  const prev = new Map<number, number>();
  const dist = new Map<number, number>([[start.y * w + start.x, 0]]);
  const queue = [start.y * w + start.x];
  let best: { i: number; score: number } | null = null;
  while (queue.length) {
    const i = queue.shift()!;
    const d = dist.get(i)!;
    if (d > 14) continue;
    const x = i % w, y = Math.floor(i / w);
    const cheb = Math.max(Math.abs(x - town.x), Math.abs(y - town.y));
    if (cheb >= 3 && cheb <= 9 && !taken.has(i) && d >= 3) {
      const score = d + (y > town.y ? 3 : 0) + Math.abs(cheb - 5);
      if (!best || score < best.score) best = { i, score };
    }
    for (const [dx, dy] of [[0, -1], [1, 0], [-1, 0], [0, 1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
      const j = ny * w + nx;
      if (col[j] === 1 || dist.has(j) || taken.has(j)) continue;
      dist.set(j, d + 1);
      prev.set(j, i);
      queue.push(j);
    }
  }
  if (!best) return null;
  const standI = prev.get(best.i) ?? best.i;
  return { gate: { x: best.i % w, y: Math.floor(best.i / w) }, stand: { x: standI % w, y: Math.floor(standI / w) } };
}

function connectDungeonsToWorld(world: TileMapData, maps: Record<string, TileMapData>): void {
  const w = world.width;
  const taken = new Set<number>();
  for (const e of world.exits ?? []) taken.add(e.tileY * w + e.tileX);
  for (const p of world.props ?? []) taken.add(p.tileY * w + p.tileX);
  for (const [townId, { dungeon, icon }] of Object.entries(DUNGEON_FROM_TOWN)) {
    const town = maps[townId];
    const pos = (WORLD_TOWNS as Record<string, { x: number; y: number }>)[townId] ?? WORLD_VILLAGES.find((v) => v.id === townId);
    if (!town || !pos || !maps[dungeon]) continue;
    const door = (town.exits ?? []).find((e) => e.targetMapId === dungeon);
    if (!door) continue;
    const spot = dungeonSpot(world, pos, taken);
    if (!spot) continue;
    taken.add(spot.gate.y * w + spot.gate.x);
    // 町の側: ダンジョンへの門は、世界地図（町のそば）へ出る出口に
    town.exits = (town.exits ?? []).map((e) =>
      e === door ? { tileX: e.tileX, tileY: e.tileY, targetMapId: "world-map", targetTileX: pos.x, targetTileY: pos.y + 1 } : e,
    );
    // 世界地図の側: アイコンと入口（条件はもとの門と同じ）
    world.props = [...(world.props ?? []), { kind: icon, tileX: spot.gate.x, tileY: spot.gate.y }];
    world.exits = [...(world.exits ?? []), {
      tileX: spot.gate.x, tileY: spot.gate.y, targetMapId: dungeon, targetTileX: door.targetTileX, targetTileY: door.targetTileY,
      ...(door.requireFlag ? { requireFlag: door.requireFlag } : {}),
      ...(door.blockedMessage ? { blockedMessage: door.blockedMessage } : {}),
    }];
    // ダンジョンの側: 町へもどる出口は、世界地図の入口の手前に出る
    for (const id of Object.keys(maps)) {
      if (id === townId || id === "world-map") continue;
      const m = maps[id];
      if (!m.exits?.some((e) => e.targetMapId === townId)) continue;
      if (!(id === dungeon || id.startsWith(dungeon.replace(/-1$/, "")))) continue;
      m.exits = m.exits.map((e) => (e.targetMapId === townId ? { ...e, targetMapId: "world-map", targetTileX: spot.stand.x, targetTileY: spot.stand.y } : e));
    }
  }
}

function findSouthGate(data: TileMapData, npcs: Npc[], first?: { tileX: number; tileY: number }): { x: number; y: number } | null {
  const { width: w, height: h } = data;
  const collision = data.collision ?? [];
  const exitAt = (x: number, yy: number): boolean => (data.exits ?? []).some((e) => e.tileX === x && e.tileY === yy);
  // 出入り口（最初のもの）から歩いて行ける場所だけを候補にする
  const start = first ?? data.exits?.[0];
  const reachable = new Set<number>();
  if (start) {
    const stack: Array<[number, number]> = [[start.tileX, start.tileY]];
    reachable.add(start.tileY * w + start.tileX);
    while (stack.length) {
      const [x, yy] = stack.pop()!;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = x + dx, ny = yy + dy;
        if (nx < 0 || ny < 0 || nx >= w || ny >= h || collision[ny * w + nx] === 1 || reachable.has(ny * w + nx)) continue;
        reachable.add(ny * w + nx);
        stack.push([nx, ny]);
      }
    }
  }
  // 歩ける場所の、いちばん下の「広い段」（3マス以上つながる段）のすぐ下に、門を開ける
  let broadRow = -1;
  for (let yy = 0; yy < h; yy++) {
    let n = 0;
    for (let xx = 0; xx < w; xx++) if (reachable.has(yy * w + xx)) n++;
    if (n >= 3) broadRow = yy;
  }
  const y = broadRow + 1;
  if (broadRow < 0 || y >= h) {
    return null;
  }
  const order = Array.from({ length: w - 2 }, (_, i) => i + 1).sort((a, b) => Math.abs(a - w / 2) - Math.abs(b - w / 2));
  for (const x of order) {
    const clear = (cx: number, cy: number): boolean => !npcs.some((n) => Math.abs(n.tileX - cx) <= 1 && Math.abs(n.tileY - cy) <= 1);
    if (reachable.has((y - 1) * w + x) && !exitAt(x, y) && !exitAt(x, y - 1) && clear(x, y - 1) && clear(x, y - 2)) {
      return { x, y };
    }
  }
  return null;
}
