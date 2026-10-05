import { createTetsukusariMineData, TETSUKUSARI_MINE_LANDMARKS } from "../map/chapter3/tetsukusari-mine";
import { createTetsukusariTownData, TETSUKUSARI_TOWN_LANDMARKS } from "../map/chapter3/tetsukusari-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第3章（鉄鏈鉱山）の世界。`docs/story/structure.md`「第3章（鉄鏈鉱山）」・
 * `docs/story/mystery.md`・`docs/story/clue-ledger.md`（伏線 C-006・C-007）を反映。
 */
export const CHAPTER3_MAPS: Record<string, TileMapData> = {
  "tetsukusari-town": createTetsukusariTownData(),
  "tetsukusari-mine": createTetsukusariMineData(),
};

/** 鉄鏈鉱山へ到着したとき、一度だけ流す短い場面つなぎ（`chapter3_intro_seen` フラグで管理）。 */
export const CHAPTER3_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――灯り石の鉱山町、鉄鏈鉱山。" },
  {
    type: "message",
    text: "硝子湖の倉庫の石は、東の鉱山から来ていた。ユーリたちは、灯り石の出どころを確かめるため、大陸いちの産地を訪ねた。",
  },
  {
    type: "message",
    text: "空は鉛色。町の入口の鉄の門には、亡くなった坑夫たちの名を刻んだ鎖が、何百と下がっている。",
  },
  {
    type: "message",
    text: "町は、鉱山会社と労働組合の睨み合いでぴりぴりしている。北の十二番坑は、三か月も閉ざされているらしい。",
  },
  { type: "setFlag", flag: "chapter3_intro_seen", value: true },
];

export const CHAPTER3_NPCS: Record<string, Npc[]> = {
  "tetsukusari-town": [
    {
      id: "tetsukusari-orca",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.orca.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.orca.tileY,
      color: "#7a5a3a",
      spriteName: "オルカ",
      commands: orcaCommands(),
    },
    {
      id: "tetsukusari-clerk",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.officeClerk.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.officeClerk.tileY,
      color: "#6a7a8a",
      commands: clerkCommands(),
    },
    {
      id: "tetsukusari-miner",
      tileX: TETSUKUSARI_TOWN_LANDMARKS.miner.tileX,
      tileY: TETSUKUSARI_TOWN_LANDMARKS.miner.tileY,
      color: "#9a8a5a",
      commands: minerCommands(),
    },
  ],
  "tetsukusari-mine": [
    {
      id: "tetsukusari-machine",
      tileX: TETSUKUSARI_MINE_LANDMARKS.machine.tileX,
      tileY: TETSUKUSARI_MINE_LANDMARKS.machine.tileY,
      color: "#5a4a70",
      commands: machineCommands(),
    },
    {
      id: "tetsukusari-dorun",
      tileX: TETSUKUSARI_MINE_LANDMARKS.dorun.tileX,
      tileY: TETSUKUSARI_MINE_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
      hideWhenFlag: "chapter3_yugami_defeated",
    },
    {
      // ドルンが去ったあとの跡（人は残さない）
      id: "tetsukusari-dorun-scorch-mark",
      tileX: TETSUKUSARI_MINE_LANDMARKS.dorun.tileX,
      tileY: TETSUKUSARI_MINE_LANDMARKS.dorun.tileY - 1,
      color: "#5a3a6a",
      commands: dorunCommands(),
      showWhenFlag: "chapter3_yugami_defeated",
    },
  ],
};

function orcaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter3_reported_to_orca",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter3_orca_hint_seen",
              equals: true,
              then: [{ type: "message", text: "……行くぞ。立ち止まっている暇はない。", speaker: "オルカ" }],
              else: [
                { type: "message", text: "オルカさん、三番坑の入口を、ずっと見てましたね。", speaker: "ミナ" },
                { type: "message", text: "……十二年前、あそこで落盤があった。それだけだ。", speaker: "オルカ" },
                { type: "message", text: "（それだけ、という顔ではなかった）", speaker: "レト" },
                { type: "setFlag", flag: "chapter3_orca_hint_seen", value: true },
              ],
            },
          ],
          else: [
            {
              type: "message",
              text: "七人は、全員戻った。数えた。……全員いる。礼を言う。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "トウゴは、広場で皆に頭を下げた。許しはしない。だが、逃がさない。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "点検は十日に一度、組合が立ち会う。給金は灯貨で払う。店券はやめさせる。そう約束させた。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "争議は、煙幕だった。組合が叫んでいるあいだ、奥であんなものが動いていた。気づけなかった。代表として、恥じている。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "『静まりの年』と書いた紙があったと聞いた。あの機械を造った奴らを、放っておけない。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "頼みがある。この件の続きを追うなら、旅に連れていってくれ。町は、副代表のスズに任せる。",
              speaker: "オルカ",
            },
            {
              type: "choice",
              text: "オルカの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    { type: "message", text: "歓迎します、オルカさん。あなたの声と力が、必要です。", speaker: "ユーリ" },
                    { type: "message", text: "……やる。俺も行く。足は引っ張らん。", speaker: "オルカ" },
                    { type: "setFlag", flag: "chapter3_orca_joined", value: true },
                  ],
                },
                {
                  label: "まず町のことを優先してほしい",
                  commands: [
                    {
                      type: "message",
                      text: "……そうか。町には、まだ約束が残っている。気が変わったら、詰め所に来い。",
                      speaker: "オルカ",
                    },
                  ],
                },
              ],
            },
            { type: "setFlag", flag: "chapter3_reported_to_orca", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter3_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "十二番坑は北の崖の中腹だ。奥に、見慣れない装置があるらしい。気をつけろ。",
              speaker: "オルカ",
            },
          ],
          else: [
            { type: "message", text: "……調査員か。鉄鏈坑夫組合の代表、オルカだ。", speaker: "オルカ" },
            {
              type: "message",
              text: "ここ三か月で、組合の者が七人消えた。会社は「出稼ぎに出た」と言う。だが、誰も家族に連絡をよこさん。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "北の坑道、十二番坑は、会社が「安全点検」で閉めた。だが、入口の梁は新しい。夜には、奥から機械の唸りと、妙な光がする。",
              speaker: "オルカ",
            },
            {
              type: "message",
              text: "七人は、夜番の特別手当に釣られた。日当は三倍。伝票を切ったのは、灯芯都の本社だ。",
              speaker: "オルカ",
            },
            {
              type: "choice",
              text: "坑道の奥を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter3_quest_accepted", value: true },
                    { type: "message", text: "わかりました。十二番坑を調べてきます。", speaker: "ユーリ" },
                    { type: "message", text: "……坑道は暗い。目で見える所だけを見るな。壁も、床も、機械の下も、全部だ。見落としは事故のもとになる。", speaker: "オルカ" },
                    { type: "message", text: "……頼む。入口は町の北、崖の中腹だ。", speaker: "オルカ" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "……急いでくれ。暮らしは、待ってくれん。", speaker: "オルカ" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function clerkCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        { type: "message", text: "坑道の件、上から「立ち入り禁止を解く」と連絡がありました。支配人は、皆さんの前で頭を下げるそうです。", speaker: "事務員" },
        { type: "message", text: "……私は何も知らなかったんです、本当に。", speaker: "事務員" },
      ],
      else: [
        { type: "message", text: "組合の方々は誤解しています。十二番坑は、ただの安全点検で閉じているだけですよ。", speaker: "事務員" },
        { type: "message", text: "……点検の指示書は本社からで、支配人も、私も、中身は見せてもらえないんです。", speaker: "事務員" },
        { type: "message", text: "そういえば支配人が、今朝、北の裏門の鍵を落としたそうで。拾った方が使うのは、私の知るところではありません。", speaker: "事務員" },
      ],
    },
  ];
}

function minerCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        { type: "message", text: "坑道の唸り声が止んだな。あんたたちのおかげか。ありがとよ。" },
        { type: "message", text: "支配人が頭を下げたそうだ。許すかどうかは、まだ別の話だがな。でも、鐘は、前より明るく聞こえる。" },
      ],
      else: [
        { type: "message", text: "給金の一部は、会社の店でしか使えねえ店券で払われる。三か月で紙切れだ。働くほど借金が増えるんだ。" },
        { type: "message", text: "おれたちは灯り石を掘りたいだけなんだがな。最近の石は、掘り出すたびに妙な熱を持ってやがる。気味が悪い。" },
      ],
    },
  ];
}

function machineCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter3_clue_c007_found",
          equals: true,
          then: [{ type: "message", text: "装置は沈黙している。散らばった指示書は、すべて拾い集めた。" }],
          else: [
            { type: "message", text: "装置の奥の小部屋で、行方不明だった七人の坑夫が見つかった。顔色は青白いが、みな生きている。" },
            { type: "message", text: "灯素に酔っているだけです。ここを出て、きれいな空気を吸って水を飲めば、ゆっくり治ります。", speaker: "ミナ" },
            { type: "message", text: "壊れた装置の下に、焦げた紙束が落ちている。" },
            { type: "message", text: "「――実験計画書。目的：静まりの年の再現に向けた、発生装置の出力調整――」" },
            { type: "message", text: "「前回の手法における不安定要素を洗い出し、規模を段階的に拡大する」……。" },
            { type: "message", text: "「静まりの年」……祖父が消えた年だ。その年を、誰かが、もう一度つくろうとしている……？", speaker: "ユーリ" },
            { type: "message", text: "……ああ。ただの鉱山の事件じゃないな、これは。……この紙は、俺が預かる。", speaker: "レト" },
            { type: "message", text: "レトは紙を折りたたみ、胸元の封筒の隣にしまった。その指先が、かすかに震えていた。" },
            { type: "message", text: "（今は、何も聞かない。レトさんが話してくれる日を、待とう）", speaker: "ユーリ" },
            { type: "setFlag", flag: "chapter3_clue_c007_found", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter3_machine_found",
          equals: true,
          then: [{ type: "message", text: "灯り石を吸い込んで唸る装置。近づくと、肌がちりちりする。" }],
          else: [
            { type: "message", text: "坑道の奥に、見慣れない大きな装置があった。管が何本も、鉱脈の灯り石につながっている。" },
            { type: "message", text: "荷車の石は、みんな選外石だ。力が乱れた、売り物にならないクズ石だよ。歪みの材料に、なるんじゃない？", speaker: "ガイド" },
            { type: "message", text: "灯り石が、泣いてるみたい……。力を吸い上げて、何かを作り出している。", speaker: "ミナ" },
            { type: "message", text: "これは、歪みを人の手で作る装置だ。灯里の草地の歪みも、きっと……。", speaker: "ユーリ" },
            { type: "message", text: "……この機械が歪みを作っているなら。四年前の、あの日も。", speaker: "ミナ" },
            { type: "setFlag", flag: "chapter3_machine_found", value: true },
          ],
        },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter3_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "男の姿はもうない。足跡だけが、坑道の奥の闇へ消えている。" }],
      else: [
        { type: "cinematic", on: true },
        { type: "message", text: "「ようこそ、客間まで。また、お会いしましたね」――穏やかな声が、坑道に響いた。" },
        { type: "message", text: "……ドルン！ 硝子湖の倉庫にいた男ですね。", speaker: "ユーリ" },
        {
          type: "message",
          text: "労働争議は、いい煙幕だったよ。みんな会社と組合の喧嘩に気を取られて、奥で何をしているか、誰も見ない。",
          speaker: "ドルン",
        },
        { type: "message", text: "この装置で何をしている！ 答えろ！", speaker: "レト" },
        {
          type: "message",
          text: "調整ですよ、ただの。平和のために必要なことだと、頼まれましてね。",
          speaker: "ドルン",
        },
        { type: "message", text: "誰に、頼まれた。", speaker: "レト" },
        { type: "message", text: "それは、わたくしの口からは申せません。", speaker: "ドルン" },
        {
          type: "message",
          text: "今日はここまでにしましょう。後始末は、装置に任せます。",
          speaker: "ドルン",
        },
        { type: "message", text: "男が装置の栓を引き抜くと、灯り石が悲鳴のような音を立てて歪み始めた！" },
        { type: "message", text: "ああ、ユーリ君。……祖父君に、よろしく。", speaker: "ドルン" },
        { type: "message", text: "祖父を、知っている……？ 待て！", speaker: "ユーリ" },
        { type: "startBattle", battleId: "tetsukusari-yugami" },
      ],
    },
  ];
}
