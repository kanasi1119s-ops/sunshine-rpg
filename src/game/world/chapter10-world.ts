import { createDeep1Data, createDeep2Data, createDeep3Data, createDeep4Data, DEEP_LANDMARKS } from "../map/chapter10/deep-maps";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * クリア後ダンジョン「虚灯宮・深部」（全4階層）と裏ボス「初源の歪み」（`docs/story/secret-boss.md`、roadmap 6-1〜6-3）。
 * 入口は、S-028を終えたあとの奥の間の階段。各階層は、灯り石の台を2つともらすと、北の封印の扉が開く。
 * 第1階層で C-018（大乱期の利用の形跡）、第2階層で C-019（封印記録）を回収し、第4階層の奥で C-021 の刻印を見る。
 * 仮: セリフは簡易、地形は単色タイル、ボスの絵は図形、クリア後の報酬（装備・称号）は未実装。
 */
export const CHAPTER10_MAPS: Record<string, TileMapData> = {
  "deep-1": createDeep1Data(),
  "deep-2": createDeep2Data(),
  "deep-3": createDeep3Data(),
  "deep-4": createDeep4Data(),
};

const L = DEEP_LANDMARKS;

/** 灯り石の台。調べると点灯し、2つともらすと `deep<層>_lit` が立つ。 */
function pedestal(floor: number, which: "a" | "b", text: string): EventCommand[] {
  const own = `deep${floor}_pedestal_${which}`;
  const other = `deep${floor}_pedestal_${which === "a" ? "b" : "a"}`;
  return [
    {
      type: "if",
      flag: own,
      equals: true,
      then: [say(undefined, "灯り石の台は、すでに明るく灯っている。")],
      else: [
        say(undefined, text),
        { type: "setFlag", flag: own, value: true },
        {
          type: "if",
          flag: other,
          equals: true,
          then: [
            say(undefined, "ふたつの灯りがそろった。北の封印の扉が、静かに軋んで、開く準備を整えた。"),
            { type: "setFlag", flag: `deep${floor}_lit`, value: true },
          ],
          else: [say(undefined, "もうひとつの台も、灯さなければ、扉は開かないようだ。")],
        },
      ],
    },
  ];
}

/** 北の封印の扉。灯り石を2つともらしていれば、次の階層へ進む。 */
function gate(floor: number, nextMapId: string, nextTile: { tileX: number; tileY: number }): EventCommand[] {
  return [
    {
      type: "if",
      flag: `deep${floor}_lit`,
      equals: true,
      then: [
        say(undefined, "封印の扉が開いた。冷たい光が、奥から流れてくる。"),
        { type: "warp", mapId: nextMapId, tileX: nextTile.tileX, tileY: nextTile.tileY },
      ],
      else: [say(undefined, "封印の扉が閉ざされている。左右の灯り石の台を、灯さなければ開かない。")],
    },
  ];
}

/** 環の欠片（8神を倒すと1つずつ手に入る）が8つそろっていれば、転移陣が起動する。 */
function fragmentsCheck(): EventCommand[] {
  let inner: EventCommand[] = [
    say(undefined, "八つの環の欠片が、ひとつに共鳴して、転移陣が強く光った。渦の塔への道が、開かれようとしている。"),
    say(undefined, "★ 転移陣が起動した！（芯環塔は、まだ準備中）"),
    { type: "setFlag", flag: "tower_gate_open", value: true },
  ];
  for (let no = 8; no >= 1; no--) {
    inner = [{ type: "if", flag: `god${no}_fragment`, equals: true, then: inner, else: [say(undefined, "環の欠片は、まだ足りない。八柱の神を鎮めて、欠片を集めよう。")] }];
  }
  return inner;
}

const ENTRY_TILE = { tileX: 10, tileY: 11 };

export const CHAPTER10_NPCS: Record<string, Npc[]> = {
  "deep-1": [
    { id: "deep1-pedestal-a", ...L.pedestalA, color: "#e0f0ff", commands: pedestal(1, "a", "氷に閉ざされた台に、そっと触れた。灯り石が、ぽっと青白く光る。") },
    { id: "deep1-pedestal-b", ...L.pedestalB, color: "#e0f0ff", commands: pedestal(1, "b", "瓦礫の下の台を掘り起こして、灯り石をともした。あたたかな光が広がる。") },
    {
      id: "deep1-tablet",
      ...L.echo,
      color: "#9aa8b8",
      commands: [
        say(undefined, "氷の下に、古い石碑が眠っている。大乱期の文字が、うっすらと読める。"),
        say(undefined, "「統暦一九六年。領主ゲンゼは、虚灯宮の封印を解き、その力を戦に用いんとした。だが、力は応えず、兵の半ばが影に呑まれた」"),
        say("アヤメ", "……軍事に使おうとしたのね。霜原の戦跡で聞いた話と、つながる。"),
        say("オルカ", "封印は、それでより厳重になったのか。人は、同じ過ちを、繰り返す。"),
        { type: "setFlag", flag: "deep1_tablet_read", value: true },
      ],
    },
    { id: "deep1-gate", ...L.gate, color: "#c8d8e8", commands: gate(1, "deep-2", ENTRY_TILE) },
  ],
  "deep-2": [
    { id: "deep2-pedestal-a", ...L.pedestalA, color: "#f0e0a0", commands: pedestal(2, "a", "石の卓に置かれた灯り石が、かすかな熱を帯びて、ともった。") },
    { id: "deep2-pedestal-b", ...L.pedestalB, color: "#f0e0a0", commands: pedestal(2, "b", "議席の陰の台に灯り石があった。触れると、ふわりと、白い光がのぼる。") },
    {
      id: "deep2-echo",
      ...L.echo,
      color: "#b0a890",
      commands: [
        say(undefined, "ぼんやりとした人影が、円い卓を囲んでいる。二十年前の灯芯都の、合議会の残響だ。"),
        say(undefined, "「……この封印記録を、写してよいのは、代表のみだ」「はい。ありがとうございます」。若き日のエドレアの声が、遠くで響いた。"),
        say("レト", "エドレアの技術の元ネタは、合議会の古い封印記録だったのか。あの人は、それを一人で研究してた。"),
        say("アヤメ", "……祖父たちが消えた夜も、この広間の残響に、混ざっている気がする。"),
        { type: "setFlag", flag: "deep2_record_read", value: true },
      ],
    },
    { id: "deep2-gate", ...L.gate, color: "#c8c0a0", commands: gate(2, "deep-3", ENTRY_TILE) },
  ],
  "deep-3": [
    { id: "deep3-pedestal-a", ...L.pedestalA, color: "#c8a0f0", commands: pedestal(3, "a", "ゆらめく紫の台の上で、灯り石がひときわ強く光った。") },
    { id: "deep3-pedestal-b", ...L.pedestalB, color: "#c8a0f0", commands: pedestal(3, "b", "台の影から現れかけた歪みを、灯り石の光で退けた。") },
    {
      id: "deep3-echo",
      ...L.echo,
      color: "#8a6aa0",
      commands: [
        {
          type: "if",
          flag: "deep3_yugami_defeated",
          equals: true,
          then: [say(undefined, "歪みの残響は静まった。紫の霞が晴れ、道が見える。")],
          else: [
            say(undefined, "紫の霞の中で、これまで戦った歪みの姿が、ゆらめいている。水涸れ、積荷、実験、砂嵐、予言、試作機、監視卓、番人……。"),
            say("ミナ", "全部、覚えてる。あのときの怖さも、みんなの顔も。"),
            say("ガイド", "でも、あのときの自分たちは、もういない。……行くよ。"),
            say(undefined, "歪みたちが一つに溶け合い、巨大な残響となって襲いかかってきた！"),
            { type: "startBattle", battleId: "deep3-yugami" },
          ],
        },
      ],
    },
    { id: "deep3-gate", ...L.gate, color: "#d0b0f0", commands: gate(3, "deep-4", ENTRY_TILE) },
  ],
  "deep-4": [
    { id: "deep4-pedestal-a", ...L.pedestalA, color: "#ffffff", commands: pedestal(4, "a", "白い台の灯り石は、触れる前から、涙のように光っていた。") },
    { id: "deep4-pedestal-b", ...L.pedestalB, color: "#ffffff", commands: pedestal(4, "b", "黒い台の灯り石を灯すと、かすかな鐘の音が、遠くで響いた。") },
    {
      id: "deep4-boss",
      ...L.boss,
      color: "#20182c",
      commands: [
        {
          type: "if",
          flag: "deep_yugami_defeated",
          equals: true,
          then: [say(undefined, "初源の歪みは、静かな光の粒となって、天井へのぼっていった。もう、何も、いない。")],
          else: [
            {
              type: "if",
              flag: "deep_boss_told",
              equals: true,
              then: [say(undefined, "初源の歪みが、ゆっくりと、こちらを向いた。"), { type: "startBattle", battleId: "deep-yugami" }],
              else: [
                say(undefined, "円い間の中央に、名前のない影が、ゆらめいている。何かを話しかけるでもなく、ただ、そこにある。"),
                say("ユーリ", "……これが、初源の歪み。四百年、ここで、ずっと眠っていたのか。"),
                say("レト", "悪意は、感じない。ただ、たくさんの悲しみの残響が、寄り集まってる。"),
                say("アヤメ", "鎮めましょう。誰かのためじゃなくて、ここで眠っている、みんなのために。"),
                { type: "setFlag", flag: "deep_boss_told", value: true },
                say(undefined, "影が、静かに、こちらへ揺れた。戦いが始まる！"),
                { type: "startBattle", battleId: "deep-yugami" },
              ],
            },
          ],
        },
      ],
    },
    {
      id: "deep4-circle",
      ...L.circle,
      color: "#a0c8ff",
      commands: [
        {
          type: "if",
          flag: "deep_yugami_defeated",
          equals: true,
          then: [
            say(undefined, "初源の歪みが消えた跡に、埃をかぶった転移陣が現れた。刻印が、淡く光っている。"),
            say(undefined, "「八柱の神を鎮め、八つの環の欠片をここに捧げよ。さすれば、渦の塔への道が開かれる」"),
            say("ユーリ", "八柱の神と、八つの欠片……。まだ、何かが、眠ってる。おじいちゃんが言ったのは、このことか。"),
            { type: "setFlag", flag: "deep_cleared", value: true },
            say(undefined, "★ 裏ボス「初源の歪み」を鎮めた！"),
            ...fragmentsCheck(),
          ],
          else: [say(undefined, "奥の扉は閉ざされている。初源の歪みを、鎮めなければ、進めない。")],
        },
      ],
    },
  ],
};
