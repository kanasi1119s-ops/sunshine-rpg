import { DEEP_LANDMARKS, DEEP_GATE } from "../map/chapter10/deep-maps";
import { CHEST, createKanouData, createTowerData } from "../map/chapter12/dungeons";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { gate, pedestal } from "./chapter10-world";
import { say } from "./side-story";

/**
 * 芯環塔（roadmap 6-8・6-9）と環奥・ラスト裏ボス「全環」（roadmap 6-10〜6-12）。`docs/story/secret-boss.md` 4・5章。
 * 入口は、8つの環の欠片で起動した深部の転移陣（`tower_gate_open`）。塔は昇る3階層（根→雲路→環光）で、
 * 環光の階の紋様で「世界の真実」を知り、最上部の裂け目から環奥（分岐する迷宮、4区画）へ進む。
 * 仮: 撃破・宝箱の報酬（伝説の装備）は「ごほうび（仮）」の会話のみ。ボスの絵は図形。地形は単色タイル。
 */
export const CHAPTER12_MAPS: Record<string, TileMapData> = {
  "tower-1": createTowerData(1),
  "tower-2": createTowerData(2),
  "tower-3": createTowerData(3),
  "kanou-1": createKanouData(1),
  "kanou-2": createKanouData(2),
  "kanou-3": createKanouData(3),
  "kanou-4": createKanouData(4),
};

const L = DEEP_LANDMARKS;
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
    { id: "tower1-gate", ...L.gate, color: "#9ad0ff", commands: gate("tower1", "tower-2", ENTRY) },
  ],
  "tower-2": [
    { id: "tower2-pedestal-a", ...L.pedestalA, color: "#ffffff", commands: pedestal("tower2", "a", "霧に隠れた足場を、灯りを頼りに渡った。台の灯り石が、白くまたたく。") },
    { id: "tower2-pedestal-b", ...L.pedestalB, color: "#ffffff", commands: pedestal("tower2", "b", "雲海の見える裂け目のそばで、二つ目の台をともした。風が、耳元でうなる。") },
    guard("tower2-guard", "tower2-guard", "tower2_guard_defeated", ["雲海の裂け目から、光の結晶でできた獣が、音もなく現れた！"], "結晶獣は砕けて、光の粒になった。道が静まっている。"),
    chest("tower2-chest", "tower2_treasure", "雲のかかった宝箱を開けた。中には、雲のように軽い伝説の装備があった。", 6000),
    { id: "tower2-gate", ...L.gate, color: "#ffffff", commands: gate("tower2", "tower-3", ENTRY) },
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
    { id: "tower3-gate", ...L.gate, color: "#fff0a0", commands: gate("tower3", "kanou-1", ENTRY) },
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
