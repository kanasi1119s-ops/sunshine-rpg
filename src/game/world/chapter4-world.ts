import { createSanoneCampData, SANONE_CAMP_LANDMARKS } from "../map/chapter4/sanone-camp";
import { createSanoneTownData, SANONE_TOWN_LANDMARKS } from "../map/chapter4/sanone-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第4章（砂音）の世界。`docs/story/structure.md`「第4章（砂音）」・`docs/story/mystery.md`を反映。
 * 伏線 C-005（ガイドの潔白）の回収と C-008（合議会関係者の噂）を実装（roadmap 4-17）。
 * ボス戦は4-18で追加（専用BGMは4-19まで、第3章のボス曲を仮に流用）。
 */
export const CHAPTER4_MAPS: Record<string, TileMapData> = {
  "sanone-town": createSanoneTownData(),
  "sanone-camp": createSanoneCampData(),
};

/** 砂音へ到着したとき、一度だけ流す場面つなぎ（`chapter4_intro_seen` フラグで管理）。 */
export const CHAPTER4_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――砂の海に浮かぶ、隊商の都・砂音。" },
  {
    type: "message",
    text: "鉄鏈鉱山で見つけた「静まりの年」の紙切れ。その手がかりを求めて、ユーリたちは物資の集まるこの町を訪ねた。",
  },
  { type: "message", text: "門の立て札には、隊商の掟の三行が刻まれている。「水は分けよ。火は絶やすな。荷は嘘をつかぬ」" },
  { type: "message", text: "日が傾くと、砂丘が低くうなりはじめた。これが「砂音」。町の名の由来だ。" },
  {
    type: "message",
    text: "町は隊商の荷が行き交い、にぎやかだ。けれど荷の数が合わず、人々は互いの荷に疑いの目を向けている。",
  },
  { type: "setFlag", flag: "chapter4_intro_seen", value: true },
];

export const CHAPTER4_NPCS: Record<string, Npc[]> = {
  "sanone-town": [
    {
      id: "sanone-guildmaster",
      tileX: SANONE_TOWN_LANDMARKS.guildMaster.tileX,
      tileY: SANONE_TOWN_LANDMARKS.guildMaster.tileY,
      color: "#8a5a3a",
      commands: guildMasterCommands(),
    },
    {
      id: "sanone-merchant",
      tileX: SANONE_TOWN_LANDMARKS.merchant.tileX,
      tileY: SANONE_TOWN_LANDMARKS.merchant.tileY,
      color: "#6a8a5a",
      commands: merchantCommands(),
    },
    {
      id: "sanone-informant",
      tileX: SANONE_TOWN_LANDMARKS.informant.tileX,
      tileY: SANONE_TOWN_LANDMARKS.informant.tileY,
      color: "#4a4a5a",
      commands: informantCommands(),
    },
  ],
  "sanone-camp": [
    {
      id: "sanone-wagon",
      tileX: SANONE_CAMP_LANDMARKS.wagon.tileX,
      tileY: SANONE_CAMP_LANDMARKS.wagon.tileY,
      color: "#7a5a3a",
      commands: wagonCommands(),
    },
    {
      id: "sanone-dorun",
      tileX: SANONE_CAMP_LANDMARKS.dorun.tileX,
      tileY: SANONE_CAMP_LANDMARKS.dorun.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
      hideWhenFlag: "chapter4_yugami_defeated",
    },
    {
      // ドルンが去ったあとの跡（人は残さない）
      id: "sanone-dorun-scorch-mark",
      tileX: SANONE_CAMP_LANDMARKS.dorun.tileX,
      tileY: SANONE_CAMP_LANDMARKS.dorun.tileY + 1,
      color: "#5a3a6a",
      commands: dorunCommands(),
      showWhenFlag: "chapter4_yugami_defeated",
    },
  ],
};

function guildMasterCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_reported",
      equals: true,
      then: [
        {
          type: "message",
          text: "帆走車は好きに使ってくれ。乗り物は、使われてこそ生きる。",
          speaker: "組合長",
        },
        {
          type: "message",
          text: "困ったときは、いつでも砂音へ戻りなさい。この町は、いつでも水を分ける。",
          speaker: "組合長",
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter4_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter4_yugami_defeated",
              equals: true,
              then: [
                { type: "message", text: "……野営地で、あの男に会ったのか。詳しく聞かせてくれ。", speaker: "組合長" },
                {
                  type: "message",
                  text: "ユーリたちは、二重底の荷、縁に波の模様のない偽の印、そしてドルンのことを話した。",
                },
                {
                  type: "message",
                  text: "そこへ、印刻みの弟子のトビが名乗り出た。師匠の薬を人質に、灰青色の指輪の男に偽の印を彫らされたという。",
                },
                {
                  type: "message",
                  text: "トビの師匠は、わしの古い友人だ。気づけたはずなのに、わしは確かめなかった。……済まなかった。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "脅されて彫った罪は軽くない。だが自分から語ったことを重く見る。師匠の薬は組合が手配しよう。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "トビには、印の保管所で三年、本物の印を守る仕事を命じる。これで、どうか。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "天幕の大人たちは、ためらいがちにうなずいた。罰でありながら、居場所を与える裁きだった。",
                },
                {
                  type: "message",
                  text: "ガイドくん。君の名を聞いたとき、わしも一度は疑った。名前ひとつで、人は目の前の人が見えなくなる。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "ユーリたちはケイスの案内で、分け水の泉のさらに東、風待ちの岩屋へ向かい、火の番をしていたトキオに会った。",
                },
                {
                  type: "message",
                  text: "白紙の保証状に名を書いたのは、俺の失敗だ。脅されて逃げたことも、ずっと悔やんでいた。",
                  speaker: "トキオ",
                },
                {
                  type: "message",
                  text: "町へ戻ったトキオは、天幕で包み隠さず語った。三年かけて集めた記録も、組合に差し出した。",
                },
                {
                  type: "message",
                  text: "帳面の字は、三年前にトキオが署名した書類と違う。トキオは、名前を使われただけだ。ガイドくんの家も無関係だ。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "ただし掟には「名を貸した者は、名の責めを負う」とある。トキオには、一年、風待ちの岩屋の火の番を命じる。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "三年、自分で選んで務めた火の番だ。これからは、掟の役目として組合が支える。罰であり、感謝でもある。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "紫の帯の男が進み出て、ガイドに頭を下げた。「怖くて、誰かのせいにしたかった。悪かった」",
                },
                {
                  type: "message",
                  text: "顔を上げてください。あたしも、従兄を疑ったんです。あなたの気持ちは、分かる気がします。",
                  speaker: "ガイド",
                },
                { type: "message", text: "……そうか。よかった。ずっと胸につかえていたの。", speaker: "ガイド" },
                { type: "message", text: "（疑いのあとに、詫びる人と、受け止める人がいる。それで、人はまた水を分け合えるんだね）", speaker: "ミナ" },
                { type: "setFlag", flag: "chapter4_guide_cleared", value: true },
                {
                  type: "message",
                  text: "礼に、組合の一番古い帆走車を預けよう。砂の上でも、風に乗ってどこまでも走れる。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "風をつかまえるコツは、帆を欲張らないことだ。商売と同じさ。",
                  speaker: "組合長",
                },
                { type: "setFlag", flag: "chapter4_sailcar_obtained", value: true },
                {
                  type: "message",
                  text: "そのとき、紺の外套の使者が、荷獣を駆って現れた。胸に、灯芯都の合議会の紋章がある。",
                },
                {
                  type: "message",
                  text: "灯りの相談所のユーリさまとお見受けします。合議会代表・エドレアさまの言葉を、お伝えします。",
                  speaker: "使者",
                },
                {
                  type: "message",
                  text: "「各地でのご活躍、うかがっております。わたしの言葉を信じるかどうかは、あなた方次第です」",
                  speaker: "使者",
                },
                {
                  type: "message",
                  text: "「ただ、いつか直接お会いして、お話ししたいことがあります。灯芯都まで、お越しください」",
                  speaker: "使者",
                },
                {
                  type: "message",
                  text: "「あなた方が見てきたものは、おそらく、真実の一部です。全部ではありません」",
                  speaker: "使者",
                },
                {
                  type: "message",
                  text: "……合議会の代表が、ぼくたちに？ 真実の、一部……。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "ずいぶんご丁寧なことだ。嘘はつかない相手ほど、隠し事は山ほどあるもんだぜ。",
                  speaker: "レト",
                },
                {
                  type: "message",
                  text: "あの使者、嘘は言ってなかった。でも、全部を話してもいないよ。手を見れば分かるの。",
                  speaker: "ガイド",
                },
                {
                  type: "message",
                  text: "ありがとうございます。まずは「静まりの年」の手がかりを追います。灯芯都へは、そのあとで。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "上に立つ者の言葉は、優しいほど慎重に聞くものだ。気をつけて行きなさい。",
                  speaker: "組合長",
                },
                { type: "setFlag", flag: "chapter4_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "調べは、南の野営地の荷馬車列から頼む。あそこの帳面に、答えがあるはずだ。",
                  speaker: "組合長",
                },
                {
                  type: "message",
                  text: "「水は分けよ。火は絶やすな。荷は嘘をつかぬ」。この掟を、わしは信じておる。",
                  speaker: "組合長",
                },
              ],
            },
          ],
          else: [
            {
              type: "message",
              text: "灯りの相談所の方々か。わしは隊商組合の長、ザイドという。遠いところを、よく来てくれた。",
              speaker: "組合長",
            },
            {
              type: "message",
              text: "近ごろ、帳面にない荷が、組合の印つきで隊商に紛れ込んでいる。わしが押した覚えのない印だ。",
              speaker: "組合長",
            },
            {
              type: "message",
              text: "荷の中身は、加工された灯り石だ。これが隊商同士の疑い合いを生み、組合が割れかけている。",
              speaker: "組合長",
            },
            {
              type: "message",
              text: "割れれば、水場も荷の預け合いも立ちゆかん。あんたたちは、どの隊にも肩入れしない。だから頼みたい。",
              speaker: "組合長",
            },
            { type: "message", text: "天幕の大人たちの視線が、ちらりとガイドに集まった。ガイドは黙って、うなずいた。" },
            {
              type: "choice",
              text: "野営地の荷馬車列を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter4_quest_accepted", value: true },
                    { type: "message", text: "引き受けます。野営地の荷馬車列を、調べさせてください。", speaker: "ユーリ" },
                    { type: "message", text: "頼もしいな。野営地は、町の南の門の先だ。案内を一人つけよう。", speaker: "組合長" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "決まったら、また声をかけてくれ。水を出して待っておる。", speaker: "組合長" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function merchantCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_sailcar_obtained",
      equals: true,
      then: [{ type: "message", text: "帆走車かい。風をつかまえるコツは、帆を欲張らないことさ。", speaker: "商人" }],
      else: [
        { type: "message", text: "いらっしゃい！ 砂漠の香辛料に、干した果物、なんでもあるよ。", speaker: "商人" },
        {
          type: "message",
          text: "ただ最近、荷の数が帳面と合わなくてねえ。隊商のあいだで、みんな疑心暗鬼さ。",
          speaker: "商人",
        },
        {
          type: "message",
          text: "噂ひとつで、隣の店の人まで疑っちまう。……いやな空気だよ、まったく。",
          speaker: "商人",
        },
      ],
    },
  ];
}

function informantCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_rumor_heard",
      equals: true,
      then: [{ type: "message", text: "噂は噂さ。信じるも信じないも、あんたたち次第だよ。", speaker: "情報屋" }],
      else: [
        {
          type: "message",
          text: "おっと、灯りの相談所の人かい。町の隅で耳を貸して暮らす者さ。名前は勘弁を。耳寄りな話がある。銭はいらないよ。",
          speaker: "情報屋",
        },
        {
          type: "message",
          text: "隊商の抜け荷を仕切ってる男の後ろに、もっと上の依頼主がいる、って噂だ。それも、灯芯都の合議会に近い人物らしい。",
          speaker: "情報屋",
        },
        { type: "message", text: "合議会の……？ まさか。", speaker: "レト" },
        { type: "message", text: "あくまで噂だよ。名前までは、わたしの耳にも入らない。", speaker: "情報屋" },
        { type: "setFlag", flag: "chapter4_rumor_heard", value: true },
      ],
    },
  ];
}

function wagonCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_wagon_found",
      equals: true,
      then: [{ type: "message", text: "荷馬車の帳面は、預かった。組合長に見せよう。" }],
      else: [
        { type: "message", text: "野営地の荷馬車の底に、二重の板が仕込まれている。外すと、灯り石の木箱がぎっしり並んでいた。" },
        { type: "message", text: "木箱には、組合の印が押してある。でも、この印……少し歪んでないですか？", speaker: "ミナ" },
        {
          type: "message",
          text: "本物の組合の印は、縁に波の模様が入ってるの。これは、ただの丸。偽の印だよ。",
          speaker: "ガイド",
        },
        {
          type: "message",
          text: "隊商の誰かを疑わせるために、わざとこう作ってある。疑い合いまで、荷の狙いの一部なんだ。",
          speaker: "ユーリ",
        },
        { type: "message", text: "箱の下に、帳面もあるよ。最後の頁の署名は……「トキオ」。あたしの従兄の名前なの。", speaker: "ガイド" },
        {
          type: "message",
          text: "……でも、この字は兄さんのじゃない。兄さんの「キ」のはらいは、いつも右に流れるの。",
          speaker: "ガイド",
        },
        {
          type: "message",
          text: "身内の言葉だけじゃ、証拠にならない。それがこの町の掟だ。帳面は預かって、組合長に見せよう。",
          speaker: "レト",
        },
        { type: "setFlag", flag: "chapter4_wagon_found", value: true },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter4_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "男の姿はもうない。砂の上に、足跡だけが残っている。" }],
      else: [
        {
          type: "if",
          flag: "chapter4_wagon_found",
          equals: true,
          then: [
            { type: "message", text: "「おや、荷馬車の底を見つけましたか。さすがですね」――ドルンが、天幕の陰から現れた。" },
            { type: "message", text: "また、あんたか。今度は何を企んでいる！", speaker: "レト" },
            {
              type: "message",
              text: "またとは、ひどい。私は、頼まれた仕事をこなしているだけです。皆さんの荷が、人助けの役に立つように。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "灯り石は、必要とする方の手に渡ったほうが、幸せでしょう？ ……簡単な仕事ですよ。",
              speaker: "ドルン",
            },
            { type: "message", text: "頼まれた……？ 誰に頼まれた！", speaker: "ユーリ" },
            {
              type: "message",
              text: "それは言えません。ただ、私の上にも、さらに上の方がいる。とだけ申し上げておきましょう。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "ドルンが荷の灯り石を踏み砕くと、砂が渦を巻いて立ち上がり、歪みの姿になった！",
            },
            { type: "setFlag", flag: "chapter4_dorun_met", value: true },
            { type: "startBattle", battleId: "sanone-yugami" },
          ],
          else: [{ type: "message", text: "焚き火のそばで、見慣れない男が背を向けて座っている。今は話しかけづらい雰囲気だ。" }],
        },
      ],
    },
  ];
}
