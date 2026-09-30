import { createToushinHallData, TOUSHIN_HALL_LANDMARKS } from "../map/chapter8/toushin-hall";
import { createToushinTownData, TOUSHIN_TOWN_LANDMARKS } from "../map/chapter8/toushin-town";
import type { TileMapData } from "../map/types";
import type { ChoiceOption, EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第8章（灯芯都）の世界。`docs/story/structure.md`「第8章（灯芯都）」・`docs/story/mystery.md`を反映。
 * 議長の審問で集めた手がかりを突きつける推理パート（正解しなくても進む）→ エドレアの正体・動機の告白（伏線 C-016）
 * → ボス「灯芯都の番人の歪み」（4-38、`src/game/battle/chapter8-enemies.ts`）→ エドレアが虚灯宮へ去る（章の引き）。
 * 仮: 町の人のセリフは簡易、地形は単色タイル。
 */
export const CHAPTER8_MAPS: Record<string, TileMapData> = {
  "toushin-town": createToushinTownData(),
  "toushin-hall": createToushinHallData(),
};

/** 灯芯都へ着いたとき、一度だけ流す場面つなぎ（`chapter8_intro_seen` フラグで管理）。 */
export const CHAPTER8_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――大陸の中央、灯芯都。" },
  {
    type: "message",
    text: "白い石畳の広場の北に、合議会堂の青い扉が見える。エドレアは「広間でお待ちしています」と言った。",
  },
  {
    type: "message",
    text: "ここまでに集めた手がかりが、すべてこの街につながっている。レトもミナも、黙ってうなずいた。",
  },
  { type: "setFlag", flag: "chapter8_intro_seen", value: true },
];

export const CHAPTER8_NPCS: Record<string, Npc[]> = {
  "toushin-town": [
    {
      id: "toushin-clerk",
      tileX: TOUSHIN_TOWN_LANDMARKS.clerk.tileX,
      tileY: TOUSHIN_TOWN_LANDMARKS.clerk.tileY,
      color: "#5a6a9a",
      commands: clerkCommands(),
    },
    {
      id: "toushin-guard",
      tileX: TOUSHIN_TOWN_LANDMARKS.guard.tileX,
      tileY: TOUSHIN_TOWN_LANDMARKS.guard.tileY,
      color: "#8a8a9a",
      commands: guardCommands(),
    },
    {
      id: "toushin-innkeeper",
      tileX: TOUSHIN_TOWN_LANDMARKS.innkeeper.tileX,
      tileY: TOUSHIN_TOWN_LANDMARKS.innkeeper.tileY,
      color: "#9a7a5a",
      commands: [
        { type: "message", text: "灯芯都へようこそ。今日は合議会の審問があるとかで、街じゅうその話で持ちきりですよ。", speaker: "宿屋の主人" },
        { type: "message", text: "エドレア様は公正なお方だ。何があっても、きっと正しく裁いてくださる。……そう信じたいですがね。", speaker: "宿屋の主人" },
      ],
    },
  ],
  "toushin-hall": [
    {
      id: "toushin-chair",
      tileX: TOUSHIN_HALL_LANDMARKS.chair.tileX,
      tileY: TOUSHIN_HALL_LANDMARKS.chair.tileY,
      color: "#6a5a8a",
      commands: chairCommands(),
    },
    {
      id: "toushin-edrea",
      tileX: TOUSHIN_HALL_LANDMARKS.edrea.tileX,
      tileY: TOUSHIN_HALL_LANDMARKS.edrea.tileY,
      color: "#3a4a7a",
      spriteName: "エドレア",
      commands: edreaCommands(),
    },
    {
      id: "toushin-hall-clerk",
      tileX: TOUSHIN_HALL_LANDMARKS.clerk.tileX,
      tileY: TOUSHIN_HALL_LANDMARKS.clerk.tileY,
      color: "#7a7a8a",
      commands: [
        {
          type: "if",
          flag: "chapter8_reported",
          equals: true,
          then: [{ type: "message", text: "議事録には、代表の席が空いたと記されました。……長い一日でした。", speaker: "書記" }],
          else: [{ type: "message", text: "議事録は、すべて書き留めています。どうぞ、思うところを堂々とお話しください。", speaker: "書記" }],
        },
      ],
    },
  ],
};

function guardCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter8_reported",
      equals: true,
      then: [{ type: "message", text: "代表が行方をくらました。街は落ち着かないが、あなた方のおかげで、真実は明るみに出た。", speaker: "衛兵" }],
      else: [{ type: "message", text: "ここは合議会堂の前だ。審問を受ける方は、議事官に声をかけてから中へどうぞ。", speaker: "衛兵" }],
    },
  ];
}

function clerkCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter8_reported",
      equals: true,
      then: [
        { type: "message", text: "議長から話は聞きました。虚灯宮……伝承の最果てへ行かれるのですね。どうか、ご無事で。", speaker: "議事官" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter8_quest_accepted",
          equals: true,
          then: [{ type: "message", text: "審問は合議会堂の議長席で行います。集めた手がかりを、議長へお示しください。", speaker: "議事官" }],
          else: [
            { type: "message", text: "灯りの相談所の方々ですね。エドレア代表から、お通しするよう言いつかっております。", speaker: "議事官" },
            {
              type: "message",
              text: "実は、各地の歪みの件で、合議会の中にも「代表に説明を求めるべきだ」という声が上がっています。今日はその審問の日です。",
              speaker: "議事官",
            },
            {
              type: "message",
              text: "証人として、議長の前で、これまでに見聞きしたことを話していただけませんか。",
              speaker: "議事官",
            },
            {
              type: "choice",
              text: "審問で証言しますか?",
              options: [
                {
                  label: "証言します",
                  commands: [
                    { type: "message", text: "ありがとうございます。北の青い扉が合議会堂です。議長がお待ちです。", speaker: "議事官" },
                    { type: "setFlag", flag: "chapter8_quest_accepted", value: true },
                  ],
                },
                {
                  label: "もう少し準備する",
                  commands: [{ type: "message", text: "分かりました。準備ができましたら、またお声がけください。", speaker: "議事官" }],
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

/** 審問の1問。正解の選択肢は、必要な手がかりのフラグが立っているときだけ「証拠を示せた」ことになる。 */
function quizQuestion(
  text: string,
  correctLabel: string,
  requiredFlag: string,
  okFlag: string,
  hint: string,
  wrongLabels: string[],
): EventCommand {
  const wrong = (label: string): ChoiceOption => ({
    label,
    commands: [{ type: "message", text: `それを裏づける記録は、ありませんな。（${hint}）`, speaker: "議長セイラン" }],
  });
  const options: ChoiceOption[] = [
    {
      label: correctLabel,
      commands: [
        {
          type: "if",
          flag: requiredFlag,
          equals: true,
          then: [
            { type: "message", text: "議場がどよめいた。示された証拠は、たしかに筋が通っている。", speaker: "議長セイラン" },
            { type: "setFlag", flag: okFlag, value: true },
          ],
          else: [
            {
              type: "message",
              text: `その証拠は、まだ手元にない。（${hint}）`,
              speaker: "議長セイラン",
            },
          ],
        },
      ],
    },
    ...wrongLabels.map(wrong),
  ];
  // 選択肢の並びを固定（正解を先頭にしない）。正解を2番目に置く。
  const [first, ...rest] = options;
  return { type: "choice", text, options: [rest[0], first, ...rest.slice(1)] };
}

function chairCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter8_reported",
      equals: true,
      then: [
        { type: "message", text: "エドレアは虚灯宮へ去った。合議会は、あなた方の旅を全力で支えよう。", speaker: "議長セイラン" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter8_edrea_fled",
          equals: true,
          then: [
            { type: "message", text: "代表席に、灯芯都の紋章の書き付けが残されていたと聞いた。……虚灯宮、か。", speaker: "議長セイラン" },
            {
              type: "message",
              text: "あの場所は、統暦の初めから閉ざされた伝承の地。だが、行き方は合議会の古い記録に残っている。あとはわたしが手配しよう。",
              speaker: "議長セイラン",
            },
            { type: "message", text: "ユーリ、君の祖父を取り戻してくれ。それは、合議会からの依頼でもある。", speaker: "議長セイラン" },
            { type: "message", text: "虚灯宮への道が開かれた！（次の章へ進めるようになった）" },
            { type: "setFlag", flag: "chapter8_kyotoukyu_open", value: true },
            { type: "setFlag", flag: "chapter8_reported", value: true },
          ],
          else: [
            {
              type: "if",
              flag: "chapter8_hearing_done",
              equals: true,
              then: [{ type: "message", text: "審問は続いている。エドレア代表の言葉を、最後まで聞こう。", speaker: "議長セイラン" }],
              else: [
                {
                  type: "if",
                  flag: "chapter8_quest_accepted",
                  equals: true,
                  then: hearingCommands(),
                  else: [
                    { type: "message", text: "議長のセイランだ。審問の証人になる方は、まず広場の議事官に声をかけてほしい。", speaker: "議長セイラン" },
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

function hearingCommands(): EventCommand[] {
  return [
    { type: "message", text: "灯りの相談所の方々か。これより、各地の歪みについての審問を始める。", speaker: "議長セイラン" },
    { type: "message", text: "代表エドレアも、席についている。……では、証言を聞かせてもらおう。", speaker: "議長セイラン" },
    quizQuestion(
      "各地で起きた歪みは、いったい誰の指示で起きていたのでしょう?",
      "浮嶼の帳簿に、計画の印と代表の署名の跡があった",
      "chapter7_ledger_found",
      "chapter8_q1_ok",
      "浮嶼の隠れ拠点の帳簿を調べていれば、示せる",
      ["ドルンがひとりで企んだことだ", "各地の村人の逆恨みだ"],
    ),
    quizQuestion(
      "「静まりの年」に合議会の要人が消えたのは、なぜでしょう?",
      "記録が書き換えられ、失踪の事実が隠されていた",
      "chapter5_record_found",
      "chapter8_q2_ok",
      "霧断崖の記録の間で碑文の写しを調べていれば、示せる",
      ["大乱の再来で、自然に混乱が起きた", "灯り石が尽きて、争いになった"],
    ),
    {
      type: "if",
      flag: "chapter8_q1_ok",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter8_q2_ok",
          equals: true,
          then: [
            { type: "message", text: "二つの証拠は、どちらも動かない。議場のだれもが、代表席のエドレアへ目を向けた。", speaker: "議長セイラン" },
            { type: "setFlag", flag: "chapter8_quiz_perfect", value: true },
          ],
          else: [{ type: "message", text: "帳簿の証拠は確かだ。だが、「静まりの年」のことは、まだ霧の中だな。", speaker: "議長セイラン" }],
        },
      ],
      else: [
        {
          type: "message",
          text: "決め手には欠けるが……。代表、あなたからも、話を聞かせてもらおうか。",
          speaker: "議長セイラン",
        },
      ],
    },
    {
      type: "message",
      text: "そのとき、傍聴席の奥から、ぼろぼろの外套の男が進み出た。ドルンだ。",
    },
    {
      type: "message",
      text: "……俺は、切り捨てられた。灯芯都からの依頼だと言ったのは、嘘じゃない。命じたのは、そこに座っている代表だ。",
      speaker: "ドルン",
    },
    { type: "message", text: "ドルンは、震える指でエドレアを指した。", speaker: undefined },
    { type: "setFlag", flag: "chapter8_hearing_done", value: true },
    { type: "message", text: "エドレアが、ゆっくりと席を立った。（代表席のエドレアに話しかけよう）" },
  ];
}

function edreaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter8_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter8_edrea_fled",
          equals: true,
          then: [{ type: "message", text: "代表席は空だ。机の上に、灯芯都の紋章の入った書き付けだけが残っている。" }],
          else: [
            { type: "message", text: "番人が崩れ落ちた。エドレアは、傷ひとつない顔で、静かに外套を羽織った。" },
            {
              type: "message",
              text: "……ここまでにしましょう。あなた方が「正しさ」を選ぶのなら、わたしは、わたしの平和を守るだけです。",
              speaker: "エドレア",
            },
            {
              type: "message",
              text: "ソウイチ殿に会いたければ、虚灯宮へいらっしゃい。あの方は、いまも奥で眠っておられる。二十年前と同じ姿で。",
              speaker: "エドレア",
            },
            { type: "message", text: "おじいちゃんは……生きてるの!?", speaker: "ユーリ" },
            { type: "message", text: "エドレアは煙のように姿を消した。あとには、紋章の書き付けが一枚。書かれているのは「虚灯宮」の三文字だった。" },
            { type: "setFlag", flag: "chapter8_edrea_fled", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter8_hearing_done",
          equals: true,
          then: [
            {
              type: "if",
              flag: "chapter8_edrea_revealed",
              equals: true,
              then: [
                { type: "message", text: "まだ、続けますか。ならば、この広間の番人が相手をします。", speaker: "エドレア" },
                { type: "startBattle", battleId: "toushin-yugami" },
              ],
              else: [
                { type: "message", text: "……そう。すべて、ご存じでしたか。", speaker: "エドレア" },
                {
                  type: "message",
                  text: "認めましょう。歪みを起こしたのは、わたしです。「静まりの年」に要人を退けたのも、わたしです。",
                  speaker: "エドレア",
                },
                {
                  type: "message",
                  text: "灯り石をめぐる争いが再燃すれば、大乱期の炎がまた大陸を焼く。争いの芽になる人を、先に表から消す。それが、いちばん血の流れない平和でした。",
                  speaker: "エドレア",
                },
                { type: "message", text: "そんなの、平和じゃない! 人を消して、村を壊して……!", speaker: "ミナ" },
                { type: "message", text: "あなたのやり方は、争いの種を自分でまいていただけだ。", speaker: "アヤメ" },
                {
                  type: "message",
                  text: "お引き取りを願いましょう。この広間には、番人がおります。話は、そのあとで。",
                  speaker: "エドレア",
                },
                { type: "setFlag", flag: "chapter8_edrea_revealed", value: true },
                { type: "message", text: "エドレアが指を鳴らすと、議場の床が青白く光り、歪みの姿となって襲いかかってきた！" },
                { type: "startBattle", battleId: "toushin-yugami" },
              ],
            },
          ],
          else: [{ type: "message", text: "審問が始まるまで、お待ちなさい。……わたしは、逃げも隠れもしませんよ。", speaker: "エドレア" }],
        },
      ],
    },
  ];
}
