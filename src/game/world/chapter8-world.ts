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
  { type: "message", text: "――大陸の中央、灯芯都。浮嶼を発って二日め。空の船は、白い石畳の広場へ降りていった。" },
  {
    type: "message",
    text: "広場の北に、合議会堂の青い扉が見える。審問は、あすの朝。エドレアは「広間でお待ちしています」と言った。",
  },
  { type: "message", text: "二十年前、あの広場のどこかで、「疫病で亡くなりました」という紙が書かれた。……兄貴の名前で、な。", speaker: "レト" },
  { type: "message", text: "……なんだよ、慰めなくていいぞ。", speaker: "レト" },
  { type: "message", text: "慰めてません。ただ、ここに立っていたいだけです。", speaker: "ユーリ" },
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
        { type: "message", text: "二十年前の冬、女房の母が寝込んだとき、医者と薬を回してくださったのが、お若いエドレア様でね。", speaker: "宿屋の主人" },
        { type: "message", text: "おかげで母は助かった。……だけど、信じたいのと、信じていいのとは、別の話ですから。", speaker: "宿屋の主人" },
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
        { type: "message", text: "灯芯都は、わたしたちが守ります。", speaker: "議事官" },
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
              text: "実は、各地の歪みの件で、合議会の中にも「代表に説明を求めるべきだ」という声が上がっています。",
              speaker: "議事官",
            },
            { type: "message", text: "議長のセイラン様が、あすの朝、審問を開くと決められました。", speaker: "議事官" },
            {
              type: "message",
              text: "証人として、議長の前で、これまでに見聞きしたことを話していただけませんか。",
              speaker: "議事官",
            },
            {
              type: "message",
              text: "……実を言えば、わたしは怖いのです。代表が噂どおりの方なら、何十年、何を信じて働いてきたのか、と。",
              speaker: "議事官",
            },
            {
              type: "choice",
              text: "審問で証言しますか？",
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
  okTexts: string[] = [],
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
            ...okTexts.map((text): EventCommand => ({ type: "message", text })),
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
        { type: "message", text: "ドルンの図面は、持ったな。眠っている方々に障りが出ぬよう、慎重にな。", speaker: "議長セイラン" },
        {
          type: "choice",
          text: "虚灯宮へ向かいますか？",
          options: [
            {
              label: "向かう",
              commands: [
                { type: "message", text: "船の用意はできている。……どうか、ご無事で。", speaker: "議長セイラン" },
                { type: "warp", mapId: "kyotoukyu-court", tileX: 12, tileY: 13 },
              ],
            },
            { label: "まだ準備する", commands: [] },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter8_edrea_fled",
          equals: true,
          then: [
            { type: "message", text: "代表席に、灯芯都の紋章の書き付けが残されていたと聞いた。……虚灯宮、か。", speaker: "議長セイラン" },
            { type: "message", text: "合議会は、代表の職を停止すると決めた。賛成四十一、反対三、棄権四。ドルンは、保護のもとで勾留し、証言を続けさせる。", speaker: "議長セイラン" },
            { type: "message", text: "……我々は、二十年間、目を閉じていた。その罪を償うためにも、この街を立て直す。", speaker: "議長セイラン" },
            {
              type: "message",
              text: "虚灯宮は、統暦の初めから閉ざされた伝承の地。行き方は、合議会の古い記録の海図に残っていた。",
              speaker: "議長セイラン",
            },
            { type: "message", text: "ユーリ、君の祖父を取り戻してくれ。これは、合議会からの正式な依頼だ。仕事として受けてほしい。", speaker: "議長セイラン" },
            { type: "message", text: "はい、お受けします。……ありがとうございます。", speaker: "ユーリ" },
            { type: "message", text: "君の後ろには、合議会が立つ。君ひとりの旅では、なくなる。報酬は、些少になるが。", speaker: "議長セイラン" },
            { type: "message", text: "それから、これを。勾留所で、ドルンから預かった。静めの間の装置の図面だ。", speaker: "議長セイラン" },
            { type: "message", text: "余白には、こうある。「乱暴に止めると、眠っておられる方々に障りが出るやもしれません。どうか、慎重に」", speaker: "議長セイラン" },
            { type: "message", text: "船は、すぐに出せる。眠っている方々を連れ帰る大きな帆船は、三日後に、わたしが迎えに出そう。", speaker: "議長セイラン" },
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
    { type: "message", text: "代表エドレアも、席についている。……代表、先に、発言の機会を与える。", speaker: "議長セイラン" },
    { type: "message", text: "ありがとうございます、議長。わたしは、この審問を歓迎します。真実が明らかになるなら、それが何よりです。", speaker: "エドレア" },
    { type: "message", text: "議長、異議がある。証人は成人前の若者だ。真実が、もう一度大陸を火にする恐れもあるのだぞ。", speaker: "議員ロクジョウ" },
    { type: "message", text: "懸念はもっともだ。だが、疑いに蓋をし続けることも、同じくらい火種を育てる。異議は記録に残し、審問を続ける。", speaker: "議長セイラン" },
    { type: "message", text: "……では、証言を聞かせてもらおう。", speaker: "議長セイラン" },
    quizQuestion(
      "各地で起きた歪みは、いったい誰の指示で起きていたのでしょう？",
      "浮嶼の帳簿の支出が、毎回4999灯で、代表の決裁印と一致する",
      "chapter7_ledger_found",
      "chapter8_q1_ok",
      "浮嶼の隠れ拠点の帳簿を調べていれば、示せる",
      ["ドルンがひとりで企んだことだ", "各地の村人の逆恨みだ"],
      [
        "帳簿の材料代は、毎回、4999灯。五千灯を超えると議決が要る。その一灯手前で、十九年……。",
        "書記が決裁記録と照らし合わせた。「……一致します。決裁印は、代表のものです」",
      ],
    ),
    quizQuestion(
      "「静まりの年」に合議会の要人が消えたのは、なぜでしょう？",
      "碑の記録が書き換えられ、三人の失踪が「疫病」にされていた",
      "chapter5_record_found",
      "chapter8_q2_ok",
      "霧断崖の記録の間で碑文の写しを調べていれば、示せる",
      ["大乱の再来で、自然に混乱が起きた", "灯り石が尽きて、争いになった"],
      [
        "「当年春、合議会員四名、職を退く。うち三名は、所在不明」。それが「疫病の噂」に彫り直されていた。",
        "ソウイチ、トウマ。……そして、ハクエイ。アヤメが、祖父の名を、自分の声で読み上げた。",
      ],
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
    { type: "message", text: "そのとき、議場の脇の古い椅子から、しゃがれた声がした。「……疫病は、なかった」" },
    { type: "message", text: "わしは、トクヨウ。記録係を四十年、勤めた者じゃ。あの年の冬、医院の来診は、ふだんより少なかった。", speaker: "トクヨウ" },
    { type: "message", text: "それなのに、三人の「病没」の届けが、同じ筆跡、同じ書式で書庫に回ってきた。わしは、おかしいと思うた。……だが、黙っておった。", speaker: "トクヨウ" },
    { type: "message", text: "友を、見捨てたんじゃ。罰は受ける。その前に、真実を記録に残したい。", speaker: "トクヨウ" },
    { type: "message", text: "トクヨウ殿の証言を、記録せよ。……だが、これが代表個人の意思か、先代の指示かは、まだ霧の中だ。", speaker: "議長セイラン" },
    { type: "message", text: "ご賢明なご判断です、議長。……どうやら、もう一人、お話しになりたい方が、いらっしゃるようです。", speaker: "エドレア" },
    { type: "message", text: "傍聴席の階段から、ぼろぼろの外套の男が、脇腹を押さえて降りてきた。ドルンだ。" },
    { type: "message", text: "衛士が槍を向けた。セイランは言った。「槍を下ろしなさい。証言を求める者を、理由なく拘束してはならない」" },
    { type: "message", text: "これはこれは、皆さま。霜原以来でございますね。……議長閣下、傍聴の順番を待たずに、失礼いたします。", speaker: "ドルン" },
    { type: "message", text: "私は、各地の装置を、すべて作りました。罪は認めます。ですが、私ひとりの意思ではございません。", speaker: "ドルン" },
    { type: "message", text: "切り捨てられた男の言葉など、信用できないでしょう。ですから、証を持ってまいりました。二十年分の、指示書でございます。", speaker: "ドルン" },
    { type: "message", text: "どの紙にも、署名と、持ち主の石にだけ反応する灯り石の印が押してあります。代表の石を、近づけてくださいませ。", speaker: "ドルン" },
    { type: "message", text: "エドレアは、長い沈黙のあと、青い石を取り出し、指示書の上にかざした。何十枚もの印が、いっせいに青く燃えた。" },
    {
      type: "message",
      text: "……灯芯都からの依頼だと言ったのは、嘘ではございません。命じたのは、そこに座っている、代表でございます。",
      speaker: "ドルン",
    },
    { type: "message", text: "ドルンは、震える指でエドレアを指した。", speaker: undefined },
    { type: "message", text: "議事官の言い回し、商人の嘘と同じ癖。肝心なところだけ、ぼかすの。", speaker: "ガイド" },
    { type: "message", text: "あの方の目は、一度も揺れませんでした。……よく、練習された言葉です。", speaker: "アヤメ" },
    { type: "setFlag", flag: "chapter8_hearing_done", value: true },
    { type: "message", text: "エドレアが、ゆっくりと席を立った。（代表席のエドレアに話しかけよう）" },
  ];
}

function edreaCommands(): EventCommand[] {
  const e = (text: string): EventCommand => ({ type: "message", text, speaker: "エドレア" });
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
            { type: "message", text: "番人が崩れ落ちた。柱にもたれたドルンが、かすれた声で言った。「……お役に、立てましたでしょうか」" },
            { type: "message", text: "ドルンさんが、床の回路を乱してくれたから勝てました。ありがとうございます。", speaker: "ユーリ" },
            { type: "message", text: "私の罪が、消えるわけではございません。……それでも、あなたは、お変わりになりませんね。", speaker: "ドルン" },
            { type: "message", text: "消えません。でも、生きて、証言を続けてください。逃げないなら、ぼくは話を聞きます。", speaker: "ユーリ" },
            { type: "message", text: "議長セイランの声が響いた。「代表エドレアを、拘束せよ」。衛士たちが、エドレアを取り囲む。" },
            { type: "message", text: "この石を手放せば、二十年の均衡が崩れます。あの方たちが、突然、目覚めれば……何が起きるのか、わたしにも分かりません。", speaker: "エドレア" },
            { type: "message", text: "エドレアは、白い円の中に、傷ひとつない顔で立っていた。そして、静かに外套の襟を合わせた。" },
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
            { type: "message", text: "おじいちゃんは……生きてるの！? 答えてください、エドレアさん！", speaker: "ユーリ" },
            { type: "message", text: "エドレアは光の渦に包まれ、煙のように姿を消した。あとには、紋章の書き付けが一枚。書かれているのは「虚灯宮」の三文字だった。" },
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
                e("……ドルン。あなたは、最後まで、わたしの期待に応えてくれましたね。"),
                { type: "message", text: "その優しさを利用したのは、どなた様でしたか。", speaker: "ドルン" },
                e("わたしです。……認めます。"),
                e("歪みを起こしたのは、わたしです。「静まりの年」に要人を退けたのも、わたしです。"),
                e("弁解はしません。ただ、なぜそうしたのかを、聞いてください。"),
                e("わたしは、浮嶼平定戦の死者を、この手で数えました。雲海衆と兵を合わせて、四千二百八人です。"),
                e("開戦の会議は、驚くほど普通でした。悪人は、ひとりもいなかった。それでも、四千二百八人が死にました。"),
                e("戦は、善い人が、家族を守ろうとして起こします。灰渡の村は、口論から七日で、四十人が亡くなりました。"),
                e("三百九十二年の春、地方ごとの連合の動きを知りました。このままでは、十年のうちに、また戦になる。"),
                { type: "message", text: "だから、消したのか。三人を。", speaker: "レト" },
                e("殺してはいません。血は、一滴も流していません。四千二百八人よりは、ずっと少ない犠牲だと、考えました。"),
                { type: "message", text: "歪みは、なぜ起こしたんですか。", speaker: "ミナ" },
                e("争いの芽が育つ場所に、先に、共通の脅威を置く。人は、疑い合うより先に、恐ろしいものに力を合わせます。"),
                e("麦香野の装置は、計画外でした。わたしの見込みの甘さが招いた事故。……わたしの罪です。"),
                e("この二十年で、装置が原因で亡くなった方は、十九人。名前を、毎晩、書斎で読み上げています。"),
                e("大乱期の一日の死者は、千人を超えました。わたしは、それを、十九人に抑えたのです。"),
                {
                  type: "message",
                  text: "灯り石をめぐる争いが再燃すれば、大乱期の炎がまた大陸を焼く。争いの芽になる人を、先に表から消す。それが、いちばん血の流れない平和でした。",
                  speaker: "エドレア",
                },
                { type: "message", text: "そんなの、平和じゃない！ 人を消して、村を壊して……！", speaker: "ミナ" },
                { type: "message", text: "あなたは、わたしの村に、聞きましたか。水が足りなくなったらどうしたいか。一度でも。", speaker: "ミナ" },
                { type: "message", text: "わたしたちは、何百年も、喧嘩のあとに話し合って生きてきました。あなたは、それを信じなかっただけです。", speaker: "ミナ" },
                e("……信じられなかったのです。話し合っている間に、火は広がります。灰渡も、話し合おうとしていました。"),
                { type: "message", text: "わたしの祖父、ハクエイは、戦を望む人ではありませんでした。なぜ、祖父を。", speaker: "アヤメ" },
                e("優しい人は、争いの中心に置かれてしまうのです。ハクエイ殿のような方は、旗頭にされてしまう。"),
                { type: "message", text: "あなたのやり方は、争いの種を自分でまいていただけだ。それは、あなたの決めつけです。", speaker: "アヤメ" },
                { type: "message", text: "俺の兄貴は、あんたの部下の書記官だった。疫病で死んだと届いた。……兄貴は、生きてるのか。", speaker: "レト" },
                e("疫病の届けを書かせたのは、わたしです。……今は、お答えできません。答えれば、あなたは短剣を抜くでしょう。"),
                { type: "message", text: "レトさん。船の上で、言ってくれましたよね。「聞く」ってやつを、少しやってみる、って。", speaker: "ユーリ" },
                { type: "message", text: "……抜かねえよ。今は、まだ。", speaker: "レト" },
                { type: "message", text: "戦か、大きな戦かの二択ですか？ 時間をかけて信頼を育てる道が、あなたの計算には、最初から入っていない。", speaker: "ガイド" },
                { type: "message", text: "犠牲を数える者は、その数に、自分を入れたか。……外から数えているうちは、まだ、苦しみの外にいる。", speaker: "オルカ" },
                e("……わたしは、その数の中に、入っていないと思います。入ってしまえば、天秤が傾きますから。"),
                { type: "message", text: "あなたは、議会を信じなかった。それが最初の過ちだ。……だが、疑わず、平和に眠りたかった我々の怠惰も、罪だ。", speaker: "議長セイラン" },
                { type: "message", text: "エドレアさん。最後に祖父と話した日、祖父は、あなたに何と言いましたか。", speaker: "ユーリ" },
                e("……秋の終わりの夜でした。わたしが全部を話すと、ソウイチ殿は、何刻も、黙って聞いてくださった。"),
                e("そして、言ったのです。「それは、誰のための話ですか。あなたの怖さのための話では、ありませんか」と。"),
                e("「その怖さを、わたしは聞く。だから、ひとりで決めないでください。みんなで、怖がりましょう」と。"),
                e("わたしは、その言葉が、恐ろしくてたまりませんでした。みんなで怖がれば、怖さが、本物になってしまう。"),
                e("だから、眠らせました。あの方が危険だったからではありません。……あの方が、正しかったからです。"),
                { type: "message", text: "祖父は、あなたの怖さを聞こうとしたはずです。話を聞いてくれるはずだった人を、あなたが、眠らせたんだ。", speaker: "ユーリ" },
                e("……ええ。聞いてもらえる資格のある人は、この二十年、わたしの中にしか、いませんでした。"),
                e("お引き取りを願いましょう。この広間には、番人がおります。話は、そのあとで。"),
                { type: "message", text: "……あんたが、全部の糸を引いていたのか。", speaker: "オルカ" },
                { type: "message", text: "ずっと、にこにこ笑って……！", speaker: "ガイド" },
                { type: "message", text: "……やはり、あなたでしたか。", speaker: "アヤメ" },
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
