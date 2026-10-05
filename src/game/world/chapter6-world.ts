import { createShimoharaFacilityData, SHIMOHARA_FACILITY_LANDMARKS } from "../map/chapter6/shimohara-facility";
import { createShimoharaTownData, SHIMOHARA_TOWN_LANDMARKS } from "../map/chapter6/shimohara-town";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第6章（霜原）の世界。`docs/story/structure.md`「第6章（霜原）」・`docs/story/mystery.md`を反映。
 * 伏線 C-012（アヤメの観察者めいた態度）と C-013（ドルンの捨て台詞）を実装（roadmap 4-27）。
 * ボス「試作機の歪み」は4-28（`src/game/battle/chapter6-enemies.ts`）、専用BGMは4-29で追加予定（それまで灯里の町の曲を仮に流用）。
 * ジョブチェンジ・システムの解禁（`docs/design/jobs.md`）は、システム本体の実装後に別項目で行う。
 */
export const CHAPTER6_MAPS: Record<string, TileMapData> = {
  "shimohara-town": createShimoharaTownData(),
  "shimohara-facility": createShimoharaFacilityData(),
};

/** 霜原へ到着したとき、一度だけ流す場面つなぎ（`chapter6_intro_seen` フラグで管理）。 */
export const CHAPTER6_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――雪に閉ざされた北の町・霜原。" },
  {
    type: "message",
    text: "霧断崖の原本に残っていた、祖父の名。「静まりの年」に何があったのか、その痕跡が、大乱期の戦跡に眠っているという。",
  },
  { type: "message", text: "町の入口の白い門のそばに、古い石碑があった。戦った者たちの名が、勝った人も負けた人も、同じ大きさの文字で並んでいる。" },
  { type: "message", text: "……いい碑だと思います。どっちの家族も、ここに来て、名前をなでられるから。", speaker: "ユーリ" },
  { type: "message", text: "決めたくなかったのかもな。「悪い」と言い切れば、その家族は今も生きてるんだ。", speaker: "レト" },
  {
    type: "message",
    text: "白い息を吐きながら町に入ると、雪の中に、ひとり静かに立っている人影があった。",
  },
  { type: "setFlag", flag: "chapter6_intro_seen", value: true },
];

export const CHAPTER6_NPCS: Record<string, Npc[]> = {
  "shimohara-town": [
    {
      id: "shimohara-watchman",
      tileX: SHIMOHARA_TOWN_LANDMARKS.watchman.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.watchman.tileY,
      color: "#6a7a8a",
      commands: watchmanCommands(),
    },
    {
      id: "shimohara-innkeeper",
      tileX: SHIMOHARA_TOWN_LANDMARKS.innkeeper.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.innkeeper.tileY,
      color: "#9a7a5a",
      commands: innkeeperCommands(),
    },
    {
      id: "shimohara-ayame",
      tileX: SHIMOHARA_TOWN_LANDMARKS.hunter.tileX,
      tileY: SHIMOHARA_TOWN_LANDMARKS.hunter.tileY,
      color: "#9a8fd0",
      spriteName: "アヤメ",
      commands: ayameCommands(),
    },
  ],
  "shimohara-facility": [
    {
      id: "shimohara-log",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.log.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.log.tileY,
      color: "#b8a878",
      commands: logCommands(),
    },
    {
      id: "shimohara-panel",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.panel.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.panel.tileY,
      color: "#6a8a9a",
      commands: panelCommands(),
    },
    {
      id: "shimohara-dorun",
      tileX: SHIMOHARA_FACILITY_LANDMARKS.guard.tileX,
      tileY: SHIMOHARA_FACILITY_LANDMARKS.guard.tileY,
      color: "#5a3a6a",
      spriteName: "ドルン",
      commands: dorunCommands(),
    },
  ],
};

function watchmanCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_reported",
      equals: true,
      then: [
        { type: "message", text: "施設の入口は、番所で封をしました。雪がやめば、また静かな町に戻るでしょう。", speaker: "番所の守り" },
        { type: "message", text: "町を代表して、御礼を申し上げます。あなた方がいなければ、この冬は越せなかったかもしれません。", speaker: "番所の守り" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter6_quest_accepted",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter6_yugami_defeated",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "地下の光が消えたのですね。あの施設が、そんな恐ろしいものだったとは……。",
                  speaker: "番所の守り",
                },
                {
                  type: "message",
                  text: "戦跡の下に何かがあると、先代からは聞いていました。けれど中身までは、誰も知らなかった。",
                  speaker: "番所の守り",
                },
                { type: "message", text: "入口には封をしてください。当面は、誰も入らないほうがいいと思います。", speaker: "ユーリ" },
                { type: "message", text: "はい、番所で責任を持ちます。せめて今夜は、宿でゆっくりなさってください。宿代は番所で持ちますから。", speaker: "番所の守り" },
                { type: "setFlag", flag: "chapter6_reported", value: true },
              ],
              else: [
                {
                  type: "message",
                  text: "入口は町の北、古い柵の先です。雪の下から、鉄の蓋が顔を出しています。",
                  speaker: "番所の守り",
                },
                {
                  type: "message",
                  text: "夜ごと青白い光が漏れて、調べに入った者も「中の空気がおかしい」と戻ってきました。",
                  speaker: "番所の守り",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の方々ですね。霜原の番所を預かっています。", speaker: "番所の守り" },
            {
              type: "message",
              text: "ひと月前、北の戦跡の雪の下から、地下への鉄の蓋が顔を出しました。夜になると、青白い光が漏れるのです。",
              speaker: "番所の守り",
            },
            {
              type: "message",
              text: "近づいた猟師は、頭が痛み、目の前が青白くなったと言います。体調を崩した者も出ています。",
              speaker: "番所の守り",
            },
            {
              type: "message",
              text: "先代の番所長が遺しました。「戦跡の下には、何かがある。目を覚ましたら、外の人の手を借りなさい」と。",
              speaker: "番所の守り",
            },
            {
              type: "choice",
              text: "地下の施設を調べますか？",
              options: [
                {
                  label: "調べます",
                  commands: [
                    { type: "setFlag", flag: "chapter6_quest_accepted", value: true },
                    { type: "message", text: "やります。青白い光は、歪みのしるしです。放っておけません。", speaker: "ユーリ" },
                    { type: "message", text: "施設の中は、気になる所をぜんぶ調べて。記録も、機械も、壁の文字も。見落とさなければ、必ず答えにたどりつくわ。", speaker: "アヤメ" },
                    { type: "message", text: "ありがとうございます。入口までの案内は、アヤメさんが引き受けてくださいます。どうか、お気をつけて。", speaker: "番所の守り" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [{ type: "message", text: "お待ちしています。", speaker: "番所の守り" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function innkeeperCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_reported",
      equals: true,
      then: [
        { type: "message", text: "温かいスープでも飲んでいってください。今夜は、ゆっくり眠れそうです。", speaker: "宿屋の主人" },
        { type: "message", text: "……車は、納屋に預かっておきます。また立ち寄ってください。", speaker: "宿屋の主人" },
      ],
      else: [
        { type: "message", text: "……ようこそ、白樺亭へ。外に置いてあった車は、納屋に入れておいた。", speaker: "宿屋の主人" },
        { type: "message", text: "戦跡のそばの宿でね。昔から、雪の下で何かが唸る夜があると言われている。……荒れる日は、外に出ないことだ。", speaker: "宿屋の主人" },
      ],
    },
  ];
}

function ayameCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_ayame_joined",
      equals: true,
      then: [{ type: "message", text: "……行きましょう。みんなと一緒なら、怖さも、少しだけ軽いです。", speaker: "アヤメ" }],
      else: [
        {
          type: "if",
          flag: "chapter6_reported",
          equals: true,
          then: [
            {
              type: "message",
              text: "施設の奥で、ドルンの話を聞きました。待つと約束したのに、また、破ってしまいました。",
              speaker: "アヤメ",
            },
            { type: "message", text: "……わたしは、ただの案内人ではありません。", speaker: "アヤメ" },
            {
              type: "message",
              text: "祖父はハクエイ。「静まりの年」に姿を消した、三人のうちの一人です。わたしは、祖父に会ったことがありません。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "祖母が育ててくれました。祖母は三年前に亡くなり、わたしは灯芯都の記録庫で二年、祖父の消えた理由を調べました。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "祖父が消える直前に、何度も会っていた人が、合議会の内側にいます。名を言うのは、証拠が揃ってから。今はまだ、それだけしか。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "だから、あなた方に近づきました。ただの案内人、というのは嘘です。入口までと言ったのも、先に入ってもらうためでした。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "けれど、旅するあなた方を見ているうちに、調べる側でいるのが、苦しくなりました。……騙していて、ごめんなさい。",
              speaker: "アヤメ",
            },
            {
              type: "message",
              text: "怒ってないよ。ぼくも、会ったことのないおじいさんを探してる。目的は、同じだ。",
              speaker: "ユーリ",
            },
            {
              type: "choice",
              text: "アヤメの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てほしい",
                  commands: [
                    { type: "message", text: "調べる人としてじゃなく、仲間として来てほしい。二度も、約束を破ってぼくたちを守ってくれた。", speaker: "ユーリ" },
                    { type: "message", text: "……ありがとう。調べる相手ではなく、仲間として、お供します。", speaker: "アヤメ" },
                    { type: "setFlag", flag: "chapter6_ayame_joined", value: true },
                  ],
                },
                {
                  label: "少し考えさせてほしい",
                  commands: [{ type: "message", text: "分かりました。気持ちが決まったら、声をかけてください。", speaker: "アヤメ" }],
                },
              ],
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter6_quest_accepted",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "北の施設なら、入口まで案内します。中には、入りません。",
                  speaker: "アヤメ",
                },
                {
                  type: "message",
                  text: "わたしは、ただの案内人です。戦いの矢面には立ちません。……それが条件です。",
                  speaker: "アヤメ",
                },
              ],
              else: [
                { type: "message", text: "……灯りの相談所の方ですね。霜原の案内人、アヤメです。", speaker: "アヤメ" },
                {
                  type: "message",
                  text: "霧断崖で碑文の改ざんを暴いた方々。旅の噂は、北の街道にも届いています。",
                  speaker: "アヤメ",
                },
                {
                  type: "message",
                  text: "この町のことなら何でも。ただし、あなた方の事情には、深入りしません。",
                  speaker: "アヤメ",
                },
                { type: "message", text: "その腕輪、灯り石が、ほんのり光っていますね。……温かいのですか。", speaker: "アヤメ" },
                { type: "message", text: "はい。ずっと温かいんです。祖父の形見で。", speaker: "ユーリ" },
                { type: "message", text: "……そうですか。", speaker: "アヤメ" },
                { type: "message", text: "（表情がほとんど動かない。まるで、こちらを観察しているようだ）", speaker: "ミナ" },
                { type: "setFlag", flag: "chapter6_ayame_met", value: true },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function logCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_log_found",
      equals: true,
      then: [
        {
          type: "message",
          text: "試作機の運用記録。「静まりの年」の日付と、責任者の署名の欄が、黒く塗りつぶされている。最後の頁の走り書きは「これは、平和のための力である」。",
        },
      ],
      else: [
        { type: "message", text: "机の上に、凍りついた運用記録が積まれていた。" },
        {
          type: "message",
          text: "「統暦三九〇年、灯り石の暴走を人為的に起こす、発生装置。試作一号機。設計、完了」……。",
          speaker: "レト",
        },
        {
          type: "message",
          text: "「三九一年、試験運用を開始。異形、発生。三九二年、静まりの年。試験の成果を、実地に運用」……そこから先は、黒く塗りつぶされてる。",
          speaker: "レト",
        },
        { type: "message", text: "最後の頁に、震える字で走り書きがある。「これは、平和のための力である」。", speaker: "レト" },
        { type: "message", text: "歪みは、ここで「作られた」んだ。……自然に起きたものじゃなかった。", speaker: "ミナ" },
        { type: "message", text: "じゃあ、わたしの怒りは、どこへ向ければいいんですか。", speaker: "ミナ" },
        { type: "message", text: "ひとりで抱えなくていい。ぼくたちと一緒に、正しい場所へ向けよう。", speaker: "ユーリ" },
        { type: "setFlag", flag: "chapter6_log_found", value: true },
        { type: "message", text: "ここまで記録が残ってるなんて……隠す気がなかったのか、隠せる自信があったのか。どっちにしても、気味が悪い。", speaker: "ガイド" },
        { type: "message", text: "……この機械、鉱山の装置と作りが同じだ。部品の癖まで。", speaker: "オルカ" },
      ],
    },
  ];
}

function panelCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "操作盤の光は消え、静まり返っている。" }],
      else: [
        { type: "message", text: "操作盤が、いまも青白く点滅している。誰かが最近まで触れていたようだ。" },
        { type: "message", text: "ユーリの腕輪が、盤の石に応えるように、ふっと熱くなった。" },
        { type: "message", text: "祖父さんの形見が、ここの装置に反応してる。……ただの灯り石じゃないのかもな。", speaker: "レト" },
        { type: "message", text: "指示の記録がある。……送り先は「灯芯都」。他の施設と同じ宛先だ。", speaker: "レト" },
      ],
    },
  ];
}

function dorunCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter6_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter6_dorun_farewell",
          equals: true,
          then: [{ type: "message", text: "ドルンの姿はない。床に、砕けた白い石の粉が散っているだけだ。" }],
          else: [
            {
              type: "message",
              text: "ドルンは肩で息をしながら、壊れた装置にもたれかかっている。",
            },
            { type: "message", text: "……ここまでですか。あなた方は、思ったより厄介だ。", speaker: "ドルン" },
            { type: "message", text: "半分は、褒め言葉です。もう半分は、恨み言。二十年かけて維持した装置を、壊してくださって。", speaker: "ドルン" },
            { type: "message", text: "いつの間にか、階段の上にアヤメが立っていた。ドルンを、まばたきもせず見つめている。" },
            { type: "message", text: "……わたしの祖父は、ハクエイといいます。ご存じですか。", speaker: "アヤメ" },
            {
              type: "message",
              text: "名前だけは。装置の調整のとき、「対象者」の名簿で見ました。争いの芽になりうると判断された人々の、名簿です。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "この施設に、人が連れて来られたことはありません。その後どうなったかは、私も知らされていないのです。",
              speaker: "ドルン",
            },
            { type: "message", text: "……そうですか。", speaker: "アヤメ" },
            { type: "message", text: "これ以上は、あの方の領分だ。私の出る幕じゃない。", speaker: "ドルン" },
            { type: "message", text: "待ってください！ 「あの方」って、誰のことですか！", speaker: "ユーリ" },
            {
              type: "message",
              text: "ユーリさん。人は、あなたが思うほど、単純ではありません。……お気をつけて。",
              speaker: "ドルン",
            },
            { type: "message", text: "ドルンは白い石を砕き、まばゆい光の中に姿を消した。" },
            { type: "message", text: "二十年以上、隠れ続けてきた「あの方」か。……俺は、誰のことか、想像がついてる。", speaker: "レト" },
            { type: "message", text: "最後まで、笑ってたね。……あの笑い、商人のものじゃなかった。", speaker: "ガイド" },
            { type: "message", text: "……「あの方」。この先に、いるんだな。", speaker: "オルカ" },
            { type: "message", text: "ドルンさんも……ほんとは、こわかったのかな。", speaker: "ミナ" },
            { type: "setFlag", flag: "chapter6_dorun_farewell", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter6_log_found",
          equals: true,
          then: [
            { type: "message", text: "「おや、あなたたちでしたか。ちょうどいい、少し道を空けてもらえますか」――ドルンが装置の前で振り向いた。" },
            { type: "message", text: "ドルン！ この装置は、あなたが作ったんですか！", speaker: "ユーリ" },
            {
              type: "message",
              text: "作った？ 少し違いますね。私は「整備」を任されているだけです。壊れかけの試作機を、もう一度だけ。",
              speaker: "ドルン",
            },
            { type: "message", text: "歪みがどうやって生まれるのか、知っていたんですね。わたしの幼なじみのことも。", speaker: "ミナ" },
            { type: "message", text: "ええ。知っていて、続けました。理由を聞きたいのなら、少し昔話をしましょう。", speaker: "ドルン" },
            {
              type: "message",
              text: "十四歳の私は、浮嶼の廃屋で、ひとり壊れた灯り石を光らせて遊んでいました。誰も、話しかけてはくれなかった。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "そこへ、灯芯都の若い女の役人が来て言ったのです。「あなたには、才能がある」と。生まれて初めて、そう言われました。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "「平和のために、その才能を」。私は信じました。小さな痛みで大きな戦を防ぐ。そう教えられたのです。",
              speaker: "ドルン",
            },
            {
              type: "message",
              text: "考えなければ、痛くない。……そうして私は、考えないことに慣れました。",
              speaker: "ドルン",
            },
            { type: "message", text: "あなたは、今もその言葉を信じているんですか。", speaker: "ユーリ" },
            { type: "message", text: "……信じたいのです。ですが、話しすぎましたね。ここで、止まってもらいます。", speaker: "ドルン" },
            {
              type: "message",
              text: "ドルンが装置に灯り石を投げ込むと、青白い光が渦を巻き、歪みの姿になった！",
            },
            { type: "setFlag", flag: "chapter6_dorun_met", value: true },
            { type: "startBattle", battleId: "shimohara-yugami" },
          ],
          else: [{ type: "message", text: "奥の装置の前に、灰色の外套の男が立っている。まずは周りの記録を調べてからのほうがよさそうだ。" }],
        },
      ],
    },
  ];
}
