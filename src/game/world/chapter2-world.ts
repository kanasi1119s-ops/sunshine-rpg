import {
  createGarasukoTownData,
  GARASUKO_TOWN_LANDMARKS,
} from "../map/chapter2/garasuko-town";
import {
  createGarasukoWarehouseData,
  GARASUKO_WAREHOUSE_LANDMARKS,
} from "../map/chapter2/garasuko-warehouse";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第2章（硝子湖）の世界。`docs/story/structure.md`「第2章（硝子湖）」・
 * `docs/story/mystery.md`（ドルンの初登場）・`docs/story/clue-ledger.md`
 * （伏線 C-003・C-004・C-005）を反映。
 */
export const CHAPTER2_MAPS: Record<string, TileMapData> = {
  "garasuko-town": createGarasukoTownData(),
  "garasuko-warehouse": createGarasukoWarehouseData(),
};

/**
 * 硝子湖へ到着したとき、一度だけ流す短い場面つなぎ（`chapter2_intro_seen` フラグで管理）。
 */
export const CHAPTER2_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――湖上の交易都市、硝子湖。" },
  {
    type: "message",
    text: "麦香野を発つ朝、カセンから「東の硝子湖に、灯り石の密輸がらみの妙な相談がある。様子を見てきて」と知らせが届いた。",
  },
  {
    type: "message",
    text: "素直なことと、疑わないことは、同じじゃないからね。それだけ、覚えておいで。",
    speaker: "カセン",
  },
  {
    type: "message",
    text: "街道を三日歩いて着いた橋の番小屋で、役人があくびをしていた。「最近、荷の数がどうも合わなくてね」。",
  },
  {
    type: "message",
    text: "湖に張り出した桟橋の先に、使われなくなったはずの倉庫がある。夜になると、そこに人の出入りがあるらしい。",
  },
  { type: "setFlag", flag: "chapter2_intro_seen", value: true },
];

export const CHAPTER2_NPCS: Record<string, Npc[]> = {
  "garasuko-town": [
    {
      id: "garasuko-guide",
      tileX: GARASUKO_TOWN_LANDMARKS.guide.tileX,
      tileY: GARASUKO_TOWN_LANDMARKS.guide.tileY,
      color: "#5a9ac9",
      spriteName: "コハク",
      commands: guideCommands(),
    },
  ],
  "garasuko-warehouse": [
    {
      id: "garasuko-crate-pile",
      tileX: GARASUKO_WAREHOUSE_LANDMARKS.cratePile.tileX,
      tileY: GARASUKO_WAREHOUSE_LANDMARKS.cratePile.tileY,
      color: "#8a6a3f",
      commands: cratePileCommands(),
    },
    {
      id: "garasuko-dorun",
      tileX: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileX,
      tileY: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
      hideWhenFlag: "chapter2_yugami_defeated",
    },
    {
      // ドルンが去ったあとの床の跡（粉と、環の文様のかけら）
      id: "garasuko-dorun-scorch-mark",
      tileX: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileX,
      tileY: GARASUKO_WAREHOUSE_LANDMARKS.dorun.tileY + 1,
      color: "#5a3a6a",
      commands: dorunCommands(),
      showWhenFlag: "chapter2_yugami_defeated",
    },
  ],
};

function guideCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter2_reported_to_guide",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter2_guide_cousin_hint_seen",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "次は東の鉄鏈鉱山だね。道と相場なら、あたしに任せてよ。",
                  speaker: "コハク",
                },
              ],
              else: [
                {
                  type: "message",
                  text: "なあ。倉庫にいた灰色の外套の男、ドルンというんだが。名前くらいは、知ってるんだろ？",
                  speaker: "レト",
                },
                {
                  type: "message",
                  text: "え？ いや、あんな怪しい奴、知り合うわけないでしょ。……知らないよ、本当に。",
                  speaker: "コハク",
                },
                {
                  type: "message",
                  text: "（少し、早口だった。嘘をついている感じではないけれど……何かを、言わないでいる）",
                  speaker: "ミナ",
                },
                {
                  type: "message",
                  text: "そうか、悪い。……ああ、船頭が言ってたぞ。あの書付の字は、丸っこい字だったとさ。",
                  speaker: "レト",
                },
                {
                  type: "message",
                  text: "……丸い字？ うちの帳場に、そんな字を書く人はいないよ。……いない、はず。",
                  speaker: "コハク",
                },
                {
                  type: "message",
                  text: "（疑うのは、嫌いになるためじゃない。ちゃんと知るためだ。今は、待とう）",
                  speaker: "ユーリ",
                },
                { type: "setFlag", flag: "chapter2_guide_cousin_hint_seen", value: true },
              ],
            },
          ],
          else: [
            {
              type: "message",
              text: "倉庫のこと、聞いたよ。灰色の外套の男は、逃げ足が速いね。……悔しいなあ。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "でも、倉庫の灯り石は片付いた。ありがとう、助かったよ。箱の焼き印も、うちのとは別物だったでしょ。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "あたしも、家業のためにずっとこの件を追ってた。……正直、一人じゃここまで来られなかった。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "それにあの男は、灯芯都からの依頼だって言ったんでしょ。この件は、この湖の中だけじゃ終わらない気がする。",
              speaker: "コハク",
            },
            {
              type: "choice",
              text: "コハクの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    {
                      type: "message",
                      text: "あなたの目と足が、必要です。ぼくが、コハクと一緒に来たいんです。",
                      speaker: "ユーリ",
                    },
                    {
                      type: "message",
                      text: "……そういう言い方、ずるいな。じゃあ条件ね。タダで手伝えとは言わないでしょ？",
                      speaker: "コハク",
                    },
                    {
                      type: "message",
                      text: "……なんてね、冗談。今回は貸しにしとく。次からは、ちゃんと取り立てるから。",
                      speaker: "コハク",
                    },
                    { type: "setFlag", flag: "chapter2_guide_joined", value: true },
                  ],
                },
                {
                  label: "商会の仕事を優先してほしい",
                  commands: [
                    {
                      type: "message",
                      text: "……そうか。まあ、気が変わったらいつでも声をかけて。桟橋のあたりにいるから。",
                      speaker: "コハク",
                    },
                  ],
                },
              ],
            },
            { type: "setFlag", flag: "chapter2_reported_to_guide", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter2_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "頼んだよ。桟橋の先の倉庫だから、気をつけてね。見張りは顔も隠してない。役人にも話が通ってるのかも。",
              speaker: "コハク",
            },
          ],
          else: [
            {
              type: "message",
              text: "よかった、相談所の人だよね。腕輪の紋章で、すぐにわかったよ。実は、頼みたいことがあるの。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "うちは三代続く、湖鳥商会。ここ半年、灯芯都へ出る石が、荷車三台分ずつ消えてるの。帳簿が合わないんだ。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "しかも荷には、うちの印つきの書付がついてる。誰かが、うちの名前を使ってるのよ。許せない。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "荷を追うと、いつも桟橋の先の倉庫に行きつくの。夜だけ人が出入りしてる。……街の人には、まだ内緒ね。",
              speaker: "コハク",
            },
            {
              type: "message",
              text: "うちの焼き印は、翼をたたんだ白い水鳥。翼の先が、内側に巻いてるのが目印だよ。",
              speaker: "コハク",
            },
            {
              type: "choice",
              text: "一緒に倉庫を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter2_quest_accepted", value: true },
                    { type: "message", text: "わかった。倉庫を調べてくる。", speaker: "ユーリ" },
                    { type: "message", text: "倉庫は、木箱の裏も、積み荷の底も、徹底的に調べて。商人の勘だけど、大事な物ほど目立たない所にあるの。", speaker: "コハク" },
                    {
                      type: "message",
                      text: "助かる。あたしは、帳簿をもう一度洗っておくね。……商人は、頼みごとの前に、正直に話すものなの。",
                      speaker: "コハク",
                    },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [
                    {
                      type: "message",
                      text: "急がなくてもいいけど、荷は毎晩動いてるの。あんまり長引くと、湖の人たちが困るから。頼むよ。",
                      speaker: "コハク",
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function cratePileCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_crates_found",
      equals: true,
      then: [{ type: "message", text: "片付けられた木箱の跡が残っている。" }],
      else: [
        { type: "message", text: "木箱の山だ。中には、表面に細かい溝を彫った灯り石が、ぎっしりと詰まっている。" },
        { type: "message", text: "どれも同じ大きさ、同じ模様。売り物ではなく、何かを組み立てる部品のようだ。" },
        { type: "message", text: "箱の側面に、翼をたたんだ白い水鳥の焼き印がある。……翼の先が、外に反っている。湖鳥商会の印とは、少しちがう。" },
        { type: "setFlag", flag: "chapter2_crates_found", value: true },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter2_yugami_defeated",
      equals: true,
      then: [
        { type: "message", text: "倉庫はすっかり静かになった。木箱の灯り石も、もう暴れ出す気配はない。" },
        {
          type: "if",
          flag: "chapter2_core_shard_taken",
          equals: true,
          then: [{ type: "message", text: "床には、青白い粉が雪のように積もっている。" }],
          else: [
            { type: "message", text: "床には、青白い粉が雪のように積もっている。その中に、環の文様を彫った石のかけらが落ちていた。" },
            { type: "message", text: "この文様……どこかで、見たことがある気がする。もっと、昔に。持ち帰って調べよう。", speaker: "レト" },
            { type: "setFlag", flag: "chapter2_core_shard_taken", value: true },
          ],
        },
      ],
      else: [
        { type: "cinematic", on: true },
        { type: "message", text: "闇の中から、静かな声がした。「……おや、お客様とは珍しい」" },
        { type: "message", text: "姿を見せたのは、人当たりのよさそうな、それでいてどこか底の読めない、灰色の外套の男だった。" },
        {
          type: "message",
          text: "驚かせてしまいましたね。仲介人、とでも言っておきましょう。ドルンといいます。",
          speaker: "ドルン",
        },
        { type: "setFlag", flag: "chapter2_clue_c003_found", value: true },
        { type: "message", text: "男の目が、ユーリの腕輪で、ほんの一瞬だけ止まった。" },
        { type: "message", text: "……ずいぶん、古い石ですね。ああ、ただの独り言です。お気になさらず。", speaker: "ドルン" },
        { type: "message", text: "灯り石をこんなに集めて、何に使うつもりだ。この円の文様は何だ。", speaker: "レト" },
        {
          type: "message",
          text: "さあ、何でしょうね。荷が何に使われるのかは、依頼主の領分でして。",
          speaker: "ドルン",
        },
        {
          type: "message",
          text: "灯芯都からの依頼でね。ちょっと、荷を動かしていただけです。……では、そろそろお暇を。",
          speaker: "ドルン",
        },
        { type: "setFlag", flag: "chapter2_clue_c004_found", value: true },
        { type: "message", text: "男が木箱に軽く触れて、指を鳴らした。積まれた灯り石が、いっせいに唸りを上げて歪み始めた！" },
        {
          type: "message",
          text: "後片付けは、こいつに任せます。……ごきげんよう。",
          speaker: "ドルン",
        },
        { type: "message", text: "男はそう言い残し、闇の中へ姿を消した。" },
        { type: "startBattle", battleId: "garasuko-yugami" },
      ],
    },
  ];
}
