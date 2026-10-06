import { DEEP_LANDMARKS, DEEP_GATE } from "../map/chapter10/deep-maps";
import { CHEST, createKanouData, createTowerData } from "../map/chapter12/dungeons";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { gate, pedestal } from "./chapter10-world";
import { say } from "./side-story";

/**
 * 芯環塔（roadmap 6-8・6-9。2026-10-06 に3階 → 8階。風の回廊・頂の見晴らしで、外の景色が見える）と環奥・ラスト裏ボス「全環」（roadmap 6-10〜6-12）。`docs/story/secret-boss.md` 4・5章。
 * 入口は、8つの環の欠片で起動した深部の転移陣（`tower_gate_open`）。塔は昇る3階層（根→雲路→環光）で、
 * 環光の階の紋様で「世界の真実」を知り、最上部の裂け目から環奥（分岐する迷宮、4区画）へ進む。
 * 仮: 撃破・宝箱の報酬（伝説の装備）は「ごほうび（仮）」の会話のみ。ボスの絵は図形。地形は単色タイル。
 */
export const CHAPTER12_MAPS: Record<string, TileMapData> = {
  "tower-1": createTowerData(1),
  "tower-2": createTowerData(2),
  "tower-3": createTowerData(3),
  "tower-4": createTowerData(4),
  "tower-5": createTowerData(5),
  "tower-6": createTowerData(6),
  "tower-7": createTowerData(7),
  "tower-8": createTowerData(8),
  "kanou-1": createKanouData(1),
  "kanou-2": createKanouData(2),
  "kanou-3": createKanouData(3),
  "kanou-4": createKanouData(4),
};

const L = DEEP_LANDMARKS;
/** 塔の窓・欄干（東の壁ぎわ）。外が見える場所。 */
const WINDOW = { tileX: 18, tileY: 8 };
const ENTRY = { tileX: 10, tileY: 11 };
/** 途中の強敵の立ち位置（北の扉の前を通れるよう、来た道の真ん中には置かない）。 */
const GUARD = { tileX: 10, tileY: 6 };

/** 宝箱（伝説の装備アイテム。仮）。 */
function chest(id: string, flag: string, text: string, gold: number): Npc {
  return {
    id,
    ...CHEST,
    color: "#e8c860",
    commands: [
      {
        type: "if",
        flag,
        equals: true,
        then: [say(undefined, "宝箱は、すでに空だ。")],
        else: [
          say(undefined, text),
          { type: "giveGold", amount: gold },
          say(undefined, `【ごほうび】灯貨${gold}を手に入れた！`),
          say(undefined, "【ごほうび（仮）】伝説の装備アイテムも眠っていた。（装備の仕組みは、お店の装備のみ）"),
          { type: "setFlag", flag, value: true },
        ],
      },
    ],
  };
}

/** 固定シンボルの強敵。倒すと `<flag>` が立ち、道が静まる。 */
function guard(id: string, battleId: string, defeatedFlag: string, lines: string[], done: string): Npc {
  return {
    id,
    ...GUARD,
    color: "#7060a0",
    commands: [
      {
        type: "if",
        flag: defeatedFlag,
        equals: true,
        then: [say(undefined, done)],
        else: [...lines.map((t) => say(undefined, t)), { type: "startBattle", battleId }],
      },
    ],
  };
}

export const CHAPTER12_NPCS: Record<string, Npc[]> = {
  // ===== 芯環塔 =====
  "tower-1": [
    { id: "tower1-pedestal-a", ...L.pedestalA, color: "#9ad0ff", commands: pedestal("tower1", "a", "青白い鉱脈に触れると、灯り石の台が、遠い海鳴りのような音を立てて灯った。") },
    { id: "tower1-pedestal-b", ...L.pedestalB, color: "#9ad0ff", commands: pedestal("tower1", "b", "岩肌の割れ目から、青い光が滲み出して、二つ目の台をともした。") },
    { id: "tower1-lore", ...L.echo, color: "#607080", commands: [say(undefined, "灯り石に似ているが、違う。青白い鉱脈は、まるで塔全体の血管のように、壁いっぱいに走っている。"), say("レト", "嵐の音が、遠くで鳴ってる。ここは、塔のいちばん下の、根っこの部分なんだ。"), say("アヤメ", "誰も来たことがないはずなのに、石段の真ん中が、すり減っている。……わたしたちの前にも、誰かが、来ようとしていたのね。"), say("ユーリ", "ここで、ひと休みしよう。おじいちゃんが持たせてくれた麦茶、まだ、ほんのり温かい。")] },
    chest("tower1-chest", "tower1_treasure", "岩陰の宝箱を開けた。中には、青白く輝く伝説の装備が眠っていた。", 4000),
    { id: "tower1-gate", ...L.gate, color: "#9ad0ff", commands: gate("tower1", "tower-4", ENTRY) },
  ],
  "tower-2": [
    { id: "tower2-pedestal-a", ...L.pedestalA, color: "#ffffff", commands: pedestal("tower2", "a", "霧に隠れた足場を、灯りを頼りに渡った。台の灯り石が、白くまたたく。") },
    { id: "tower2-pedestal-b", ...L.pedestalB, color: "#ffffff", commands: pedestal("tower2", "b", "雲海の見える裂け目のそばで、二つ目の台をともした。風が、耳元でうなる。") },
    guard("tower2-guard", "tower2-guard", "tower2_guard_defeated", ["雲海の裂け目から、光の結晶でできた獣が、音もなく現れた！"], "結晶獣は砕けて、光の粒になった。道が静まっている。"),
    chest("tower2-chest", "tower2_treasure", "雲のかかった宝箱を開けた。中には、雲のように軽い伝説の装備があった。", 6000),
    { id: "tower2-gate", ...L.gate, color: "#ffffff", commands: gate("tower2", "tower-5", ENTRY) },
  ],
  "tower-3": [
    {
      id: "tower3-mural-a",
      ...L.pedestalA,
      color: "#fff0a0",
      commands: pedestal("tower3", "a", "壁一面の紋様を、指でなぞった。「灯の環は、この世界と、もうひとつの世界を隔てる、境目そのものだった」。"),
    },
    {
      id: "tower3-mural-b",
      ...L.pedestalB,
      color: "#fff0a0",
      commands: pedestal("tower3", "b", "もうひとつの紋様を読んだ。「四百年前、環は砕けた。芯だけが砕けきれず、海へ沈み、この塔として残った。砕けた境目からこぼれた揺らぎが、歪みとなった」。"),
    },
    {
      id: "tower3-truth",
      ...L.echo,
      color: "#e8e0c8",
      commands: [
        {
          type: "if",
          flag: "tower3_lit",
          equals: true,
          then: [
            say("アヤメ", "……初源の歪みは、揺らぎの最初の一滴。八柱の神は、砕けた破片が土地の記憶を吸って育った守り手。"),
            say("コハク", "蟲神だけが歪んだのは、見送られない死を、吸いすぎたからなんだね。他の神様も、運が良かっただけかもしれない。"),
            say("オルカ", "エドレアは、この自然の仕組みを真似ただけか。……罪が軽くなるわけじゃないが、原理を知ると、見え方が変わるな。"),
            say("レト", "知らずに憎むより、知って憎むほうが、正確だ。……正確に憎む。いい言葉だろ。"),
            say("ユーリ", "境目のもう半分が、環奥にある。……この先に、全部の始まりが、待ってる。"),
            { type: "setFlag", flag: "tower_truth_known", value: true },
          ],
          else: [say(undefined, "壁一面に、環の紋様が刻まれている。二つの紋様を読み解けば、何かが分かりそうだ。")],
        },
      ],
    },
    guard("tower3-guard", "tower3-guard", "tower3_guard_defeated", ["広間の奥の暗がりで、光の結晶が、ひときわ大きく輝いた。宝の番人が目を覚ます！"], "宝の番人は、静かに崩れ去った。"),
    chest("tower3-chest", "tower3_treasure", "広間の隅の宝箱を開けた。中には、環の紋様が刻まれた、最上位の伝説の装備が眠っていた。", 9000),
    { id: "tower3-gate", ...L.gate, color: "#fff0a0", commands: gate("tower3", "tower-7", ENTRY) },
  ],
  // ===== 芯環塔・足した階（2026-10-06、人間の指示「階層もっと増やしていい」「塔から外が見れる場所がほしい。塔の中のイベントに」）=====
  "tower-4": [
    { id: "tower4-pedestal-a", ...L.pedestalA, color: "#7ab8f0", commands: pedestal("tower4", "a", "らせんに巻く鉱脈の、いちばん太いところに触れた。台が、心臓の鼓動のように、とくん、と光る。") },
    { id: "tower4-pedestal-b", ...L.pedestalB, color: "#7ab8f0", commands: pedestal("tower4", "b", "鉱脈の光を、二つ目の台へみちびいた。青い光が、壁のらせんを、上へ上へとのぼっていく。") },
    { id: "tower4-lore", ...L.echo, color: "#506078", commands: [say(undefined, "壁を、青い鉱脈がらせんに巻きながら、上へのびている。塔そのものが、ひとつの大きな灯り石のようだ。"), say("オルカ", "……鉱山の脈と、同じ巻き方だ。いや、逆か。鉱山の脈のほうが、こいつを真似てるのかもしれん。"), say("コハク", "これ、ちょっと削って持って帰ったら……いや、なんでもない。なんでもないってば。")] },
    chest("tower4-chest", "tower4_treasure", "鉱脈のかげの宝箱を開けた。中には、青い光を宿した伝説の装備が眠っていた。", 5000),
    { id: "tower4-gate", ...L.gate, color: "#7ab8f0", commands: gate("tower4", "tower-2", ENTRY) },
  ],
  "tower-5": [
    { id: "tower5-pedestal-a", ...L.pedestalA, color: "#e8f4ff", commands: pedestal("tower5", "a", "吹きこむ風の中で、台に灯りを入れた。光が、風にあおられて、ゆらゆらと踊る。") },
    { id: "tower5-pedestal-b", ...L.pedestalB, color: "#e8f4ff", commands: pedestal("tower5", "b", "二つ目の台をともすと、回廊じゅうの窓が、いっせいに白く光った。") },
    { id: "tower5-window", ...WINDOW, color: "#e8f4ff", commands: cloudWindowCommands() },
    { id: "tower5-lore", ...L.echo, color: "#7a8ca8", commands: [say(undefined, "東の壁に、大きな石のアーチ窓が開いている。風が、そこから吹きこんでくる。"), say("ミナ", "外が、見えるみたい。……ちょっと、のぞいてみませんか？")] },
    { id: "tower5-gate", ...L.gate, color: "#e8f4ff", commands: gate("tower5", "tower-6", ENTRY) },
  ],
  "tower-6": [
    { id: "tower6-pedestal-a", ...L.pedestalA, color: "#c8c0ff", commands: pedestal("tower6", "a", "星図の棚の前の台をともすと、天井に、見たことのない星座が浮かびあがった。") },
    { id: "tower6-pedestal-b", ...L.pedestalB, color: "#c8c0ff", commands: pedestal("tower6", "b", "二つ目の台の光が、八つの星を結んだ。……八柱の神の、しるしだろうか。") },
    { id: "tower6-lore", ...L.echo, color: "#40406a", commands: [say(undefined, "棚には、石の板に刻まれた星図が、何百枚もならんでいる。どれも、空に浮かぶ大きな環を中心に描かれている。"), say("アヤメ", "四百年より前の空……。環が、まだ欠けていなかったころの星図ね。"), say("レト", "書いた奴は、毎晩、ここで空を見上げてたんだろうな。……ひとりで。")] },
    guard("tower6-guard", "tower6-guard", "tower6_guard_defeated", ["星図の棚がきしみ、石の板が宙に舞いあがった。書庫を守る番人が、目を覚ます！"], "書守は、星図の一枚にもどって、棚へおさまった。"),
    chest("tower6-chest", "tower6_treasure", "書庫の奥の宝箱を開けた。中には、星のかけらをちりばめた伝説の装備が眠っていた。", 7500),
    { id: "tower6-gate", ...L.gate, color: "#c8c0ff", commands: gate("tower6", "tower-3", ENTRY) },
  ],
  "tower-7": [
    { id: "tower7-pedestal-a", ...L.pedestalA, color: "#ffd0a0", commands: pedestal("tower7", "a", "外壁ぞいの段は、嵐の風がまともに吹きつける。両手で台をかばいながら、灯りを入れた。") },
    { id: "tower7-pedestal-b", ...L.pedestalB, color: "#ffd0a0", commands: pedestal("tower7", "b", "二つ目の台がともると、風が、ふっと弱まった。……頂が、近い。") },
    { id: "tower7-lore", ...L.echo, color: "#5a5468", commands: [say(undefined, "壁のすきまから、嵐の音がする。ずっと下で、雲海が渦を巻いているのが、ちらりと見えた。"), say("ユーリ", "足もとを見ないように……見ないように……。"), say("オルカ", "見るな。前だけ見ろ。俺の背中でもいい。")] },
    guard("tower7-guard", "tower7-guard", "tower7_guard_defeated", ["嵐が、ひとつの形に集まっていく。階段を守る番人が、風をまとって立ちふさがった！"], "嵐は、ただの風になって、空へ散っていった。"),
    { id: "tower7-gate", ...L.gate, color: "#ffd0a0", commands: gate("tower7", "tower-8", ENTRY) },
  ],
  "tower-8": [
    { id: "tower8-pedestal-a", ...L.pedestalA, color: "#ffe0b0", commands: pedestal("tower8", "a", "頂の台に灯りを入れた。空が、少しずつ、白みはじめている。") },
    { id: "tower8-pedestal-b", ...L.pedestalB, color: "#ffe0b0", commands: pedestal("tower8", "b", "最後の台がともると、塔の頂いっぱいに、朝の光が満ちた。北の扉の向こうで、空間が、かすかに裂けている。") },
    { id: "tower8-view", ...WINDOW, color: "#ffe0b0", commands: summitViewCommands() },
    { id: "tower8-lore", ...L.echo, color: "#8a7c98", commands: [say(undefined, "塔のいちばん上。石の欄干の向こうに、夜明けの空が広がっている。"), say("コハク", "ねえ、ちょっと。……欄干のところ、来てみてよ。すごいよ。")] },
    { id: "tower8-gate", ...L.gate, color: "#ffe0b0", commands: gate("tower8", "kanou-1", ENTRY) },
  ],
  // ===== 環奥 =====
  "kanou-1": [
    { id: "kanou1-pedestal-a", ...L.pedestalA, color: "#a8a8f0", commands: pedestal("kanou1", "a", "分かれ道の先で、灯り石の台を見つけた。光は、東の通路を、かすかに照らしている。") },
    { id: "kanou1-pedestal-b", ...L.pedestalB, color: "#a8a8f0", commands: pedestal("kanou1", "b", "もうひとつの台の光も、やはり、東の通路のほうへ、細く伸びている。") },
    {
      id: "kanou1-fork",
      ...L.gate,
      color: "#a8a8f0",
      commands: [
        {
          type: "if",
          flag: "kanou1_lit",
          equals: true,
          then: [
            {
              type: "choice",
              text: "分かれ道だ。迷ったら、みんなと手をつなぐように、灯りを頼りに進もう。どの通路へ進みますか？",
              options: [
                { label: "光が照らす東の通路", commands: [say(undefined, "灯り石の光をたどると、通路の景色が、少しずつ、静かに変わっていった。"), { type: "warp", mapId: "kanou-2", tileX: ENTRY.tileX, tileY: ENTRY.tileY }] },
                { label: "暗い西の通路", commands: [say(undefined, "歩いても、歩いても、同じ場所に戻ってきてしまう。灯り石の光を、頼りにしよう。")] },
                { label: "南の通路", commands: [say(undefined, "来た道に戻ってしまった。灯りの向きを、もう一度、確かめよう。")] },
              ],
            },
          ],
          else: [say(undefined, "通路が三つに分かれている。灯り石の台を灯して、道しるべを見つけないと、迷ってしまいそうだ。")],
        },
      ],
    },
  ],
  "kanou-2": [
    { id: "kanou2-pedestal-a", ...L.pedestalA, color: "#b0f0d8", commands: pedestal("kanou2", "a", "静かな広間の台に、灯り石をそっと置いた。柔らかな緑の光が広がる。") },
    { id: "kanou2-pedestal-b", ...L.pedestalB, color: "#b0f0d8", commands: pedestal("kanou2", "b", "誰かが座っていたような跡のそばの台を灯した。……ここには、確かに、誰かが、いた。") },
    { id: "kanou2-lore", ...L.echo, color: "#587068", commands: [say(undefined, "音のない広間に、人影とも、光ともつかない気配が、ゆらめいている。"), say("ミナ", "……悲しい場所じゃないの。ただ、すごく、静か。ずっと待っていた人たちの、気配みたい。")] },
    chest("kanou2-chest", "kanou2_treasure", "気配の足元の宝箱を開けた。中には、静けさを閉じ込めたような伝説の装備が眠っていた。", 12000),
    { id: "kanou2-gate", ...L.gate, color: "#b0f0d8", commands: gate("kanou2", "kanou-3", ENTRY) },
  ],
  "kanou-3": [
    { id: "kanou3-pedestal-a", ...L.pedestalA, color: "#f0b0d8", commands: pedestal("kanou3", "a", "境目の薄い庭の台を灯すと、ふたつの世界の景色が、重なって見えた。") },
    { id: "kanou3-pedestal-b", ...L.pedestalB, color: "#f0b0d8", commands: pedestal("kanou3", "b", "花のような光をまとった台を灯した。ここは、こんなにも、きれいな場所だったのか。") },
    guard("kanou3-guard", "kanou3-guard", "kanou3_guard_defeated", ["庭の奥から、境目を守る、光の守り手が、静かに立ちふさがった！"], "守り手は、安らかな光となって、庭の花に溶けていった。"),
    chest("kanou3-chest", "kanou3_treasure", "花の陰の宝箱を開けた。中には、ゲーム最強クラスの伝説の装備が眠っていた。", 16000),
    { id: "kanou3-gate", ...L.gate, color: "#f0b0d8", commands: gate("kanou3", "kanou-4", ENTRY) },
  ],
  "kanou-4": [
    { id: "kanou4-pedestal-a", ...L.pedestalA, color: "#d0a0ff", commands: pedestal("kanou4", "a", "白い台の灯り石は、触れる前から、優しく光っていた。") },
    { id: "kanou4-pedestal-b", ...L.pedestalB, color: "#d0a0ff", commands: pedestal("kanou4", "b", "もうひとつの台も、灯した。……大きな、静かな鼓動が、遠くで響いた。") },
    {
      id: "kanou4-boss",
      ...L.boss,
      color: "#7050c0",
      commands: zenkanCommands(),
    },
  ],
};

/** 風の回廊の窓から、雲海を見る（人間の指示「塔から外が見れる場所」）。 */
function cloudWindowCommands(): EventCommand[] {
  return [
    { type: "cinematic", on: true },
    say(undefined, "大きな石のアーチ窓から、外をのぞいた。"),
    { type: "vista", image: "clouds" },
    say(undefined, "――見わたすかぎりの、雲の海だった。"),
    say(undefined, "もこもことした雲が、白い波のように、地平の果てまでつづいている。その向こうに、青くかすんだ大陸の山なみ。"),
    say("ミナ", "……わあ。雲を、上から見てる。わたしたち、雲より高いところにいるんですね。"),
    say("コハク", "見て、右のほう！ 島が浮かんでる。あれ、浮嶼だよ。あんなに小さく見えるなんて。"),
    say("レト", "あのあたりの雲の下が霜原で、その手前が砂音か。……歩いたな。全部、歩いた。"),
    say("オルカ", "鉄鏈の煙も、ここからじゃ見えん。……見えんほうが、いいのかもしれん。"),
    say("アヤメ", "雲のすき間を、何かが飛んでいる。……小さな、空の船。わたしたちのほかにも、空を渡る人がいるのね。"),
    say("ユーリ", "母さんにも、見せてあげたいな。……灯里は、あの山の、ずっと向こうだ。"),
    say(undefined, "冷たい風が、六人の髪を、いっしょにゆらした。"),
    { type: "setFlag", flag: "tower5_view_seen", value: true },
  ];
}

/** 頂の欄干から、夜明けの世界を見る。空には、欠けた光の環の跡。 */
function summitViewCommands(): EventCommand[] {
  return [
    { type: "cinematic", on: true },
    say(undefined, "石の欄干に手をかけて、六人は、ならんで外を見た。"),
    { type: "vista", image: "summit" },
    say(undefined, "――夜明けだった。"),
    say(undefined, "海の向こうから、太陽が顔を出す。光の道が、波の上を、まっすぐこちらへのびてくる。"),
    say(undefined, "そして、まだ星の残る空に、大きな、大きな光の弧がかかっていた。ところどころが、欠けている。"),
    say("アヤメ", "……灯の環。いいえ、その跡。四百年前に砕けた、境目の名残りが、この高さからだと、見えるのね。"),
    say("レト", "地上からは、一度も見えなかった。……ずっと、頭の上にあったのか。"),
    say("ミナ", "大陸のほう。小さな灯りが、ぽつ、ぽつって。……あれ、町の灯りですよね。"),
    say("コハク", "左から、麦香野、硝子湖、鉄鏈……あっちが砂音で、霧断崖。いちばん右の、あれが、灯芯都の白い塔だよ、きっと。"),
    say("オルカ", "あの灯り、ひとつひとつに、人が暮らしてる。……俺たちが歩いた道も、あの灯りのあいだにある。"),
    say("ユーリ", "灯里は……見えないや。でも、あの光の道の、ずっと先にある気がする。"),
    say("ユーリ", "……行こう。環の欠けたところの、その先へ。帰るために。"),
    say(undefined, "朝の光が、欄干の石を、金色にそめていた。"),
    { type: "setFlag", flag: "tower8_view_seen", value: true },
  ];
}

function zenkanCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "zenkan_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "epilogue_all_seen",
          equals: true,
          then: [say(undefined, "全環の間は、静かな光に満ちている。もう、揺らぎは、起きない。")],
          else: [
            say(undefined, "全環の波が、ユーリたちを孤独の幻に引きこんだ。だが、ユーリの呼びかけで、六人の手が、つながった。"),
            say("全環", "……ひとりで、いい。わたしは、境目を守る。それが、わたしのすべて。……もう半分とは、二度と、会えない。"),
            say("ユーリ", "砕けた半身を、探していたんだね。……もう半分は、消えてない。山や海、人々の暮らし、八柱の神々になって、ずっと、世界を支えてきた。"),
            say("ミナ", "あなたのもう半分は、無事です。たくさんの人を、守ってきました。"),
            say("アヤメ", "四百年、ひとりで境目を守ってくれていたことを、わたしたちは、知らなかった。……ありがとう。"),
            say("オルカ", "ありがとう。"),
            say("レト", "口が悪いから、ちゃんと言えるか分かんねえが。……ありがとな。四百年、お疲れさん。"),
            say(undefined, "全環は、ゆっくりと、ひとつの光の環になり、境目の向こうへ、溶けていった。裂け目が、静かに、閉じていく。"),
            say("全環", "……ありがとう、と言われたのは、はじめてだ。四百年、ひとりだった。……もう、境目を、守らなくていいのですね。"),
            say("ユーリ", "はい。境目は、ぼくたちが、これからは、ちゃんと見ています。"),
            say("レト", "初源の歪みも、八柱の神も、静まりの年も。……全部、遠い根っこで、つながっていたんだ。"),
            say("ミナ", "みんな、それぞれの悲しみだったのに、同じ光の中に、還っていく。"),
            say("コハク", "これから、歪みは、自然には起こらなくなるんだね。……ちょっと寂しい気もするけど、いいことだよ。"),
            say("レト", "寂しい。仕事が減るしな。"),
            say("コハク", "仕事の心配かよ！"),
            say("オルカ", "エドレアの罪は、消えない。でも、世界の悲しみが、少し、軽くなった。それは、確かだ。"),
            say("アヤメ", "……終わったのね。ううん、ここからが、始まり。観察者じゃなくて、これからは、仲間として、見ていく。"),
            say("ユーリ", "帰ろう、みんなで。灯里に。"),
            say(undefined, "――三日の航海ののち、灯里の朝。海の塩気と、焼きたてのパンと、干し魚の匂いは、旅立ちの日と、同じだった。"),
            say(undefined, "左手首には、二つの腕輪。祖父の窓辺の麦茶、カセンの「よく、帰ってきた」。レトの兄の小言も、にぎやかに響いた。"),
            say("カセン", "さて、今日の依頼だ。迷子の猫の捜索、隣町の水車小屋の修理。それから、夜になると誰かの泣き声がする、って噂だよ。"),
            say("ユーリ", "まず、猫から行きましょう。順番に、ひとつずつ。……旅の続きは、また、ここから始まる。"),
            say(undefined, "★ すべての物語を終えました！ ここまで遊んでくれて、ありがとう！（仮のエンディング）"),
            { type: "setFlag", flag: "epilogue_all_seen", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "zenkan_told",
          equals: true,
          then: [say(undefined, "全環が、ふたたび、光を放った。"), { type: "startBattle", battleId: "zenkan" }],
          else: [
            say(undefined, "円い間の中央に、巨大な光の環が、静かに回っている。これが、境目のもう半分。全環。"),
            say("ユーリ", "……ずっと、ここにいたんだね。ひとりで、境目を、守って。"),
            say("アヤメ", "悪意は、ない。ただ、役目を果たそうとして、揺らぎが、あふれてしまうのね。"),
            say("レト", "鎮めよう。これ以上、誰も、悲しまないように。"),
            { type: "setFlag", flag: "zenkan_told", value: true },
            say(undefined, "光の環が、ゆっくりと、こちらへ傾いた。戦いが始まる！"),
            { type: "startBattle", battleId: "zenkan" },
          ],
        },
      ],
    },
  ];
}

export const TOWER_ENTRY = { tileX: 10, tileY: 11 };
export { DEEP_GATE };
