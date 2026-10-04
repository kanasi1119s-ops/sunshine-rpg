import { createTouriTownData, TOURI_TOWN_SPAWN, TOURI_TOWN_LANDMARKS } from "../map/chapter0/touri-town";
import { createTouriBranchData, TOURI_BRANCH_LANDMARKS } from "../map/chapter0/touri-branch";
import { createTouriOutskirtsData, TOURI_OUTSKIRTS_LANDMARKS } from "../map/chapter0/touri-outskirts";
import {
  createTouriForest1Data,
  createTouriForest2Data,
  TOURI_FOREST1_LANDMARKS,
  TOURI_FOREST2_LANDMARKS,
} from "../map/chapter0/touri-forest";
import { chestNpc, leverNpc, loreNpc } from "./dungeon-objects";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 序章（灯里）の世界。`docs/story/structure.md`「序章（灯里）」・
 * `docs/story/mystery.md`（真相）・`docs/story/clue-ledger.md`（伏線 C-001, C-009）を
 * 反映した、はじめて遊べる本編の内容（工程表フェーズ3）。
 */
export const CHAPTER0_MAPS: Record<string, TileMapData> = {
  "touri-town": createTouriTownData(),
  "touri-branch": createTouriBranchData(),
  "touri-forest-1": createTouriForest1Data(),
  "touri-forest-2": createTouriForest2Data(),
  "touri-outskirts": createTouriOutskirtsData(),
};

export const CHAPTER0_START = {
  mapId: "touri-town",
  tileX: TOURI_TOWN_SPAWN.tileX,
  tileY: TOURI_TOWN_SPAWN.tileY,
};

/**
 * ゲーム開始時に一度だけ流すオープニング（`chapter0_intro_seen` フラグで管理）。
 * 呼び出し側（main.ts）が、フラグが立っていなければ起動直後に流す。
 */
export const CHAPTER0_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――大陸アルテシア、港町・灯里。" },
  {
    type: "message",
    text: "ユーリは「灯りの相談所」灯里支部の新人調査員。左手首には、亡き祖父の形見の腕輪が光っている。",
  },
  {
    type: "message",
    text: "ここ数日、町外れで「歪み」――灯り石の力が乱れて生まれる異形――が、いつになく頻繁に現れているという。",
  },
  { type: "message", text: "支部長のカセンが、話を聞かせてほしいと呼んでいる。相談所へ向かおう。" },
  { type: "setFlag", flag: "chapter0_intro_seen", value: true },
];

export const CHAPTER0_NPCS: Record<string, Npc[]> = {
  "touri-town": [
    {
      id: "touri-fisherman",
      tileX: TOURI_TOWN_LANDMARKS.fisherman.tileX,
      tileY: TOURI_TOWN_LANDMARKS.fisherman.tileY,
      color: "#e0a458",
      commands: [
        {
          type: "if",
          flag: "chapter0_yugami_defeated",
          equals: true,
          then: [
            {
              type: "message",
              text: "町外れの歪みがおとなしくなったって聞いたよ。ユーリちゃんのおかげかい？",
              speaker: "漁師",
            },
            { type: "message", text: "港の魚も安心して獲れるってもんだ。ありがとよ。", speaker: "漁師" },
          ],
          else: [
            {
              type: "if",
              flag: "chapter0_quest_accepted",
              equals: true,
              then: [
                {
                  type: "if",
                  flag: "chapter0_heard_rumor",
                  equals: true,
                  then: [
                    {
                      type: "message",
                      text: "森の祠は、灯守りの爺さんが昔から世話をしてるよ。あの爺さんなら、森を歩くための灯りを貸してくれるはずだ。",
                      speaker: "漁師",
                    },
                  ],
                  else: [
                    {
                      type: "message",
                      text: "ああ、相談所の依頼を受けたのかい。なら、先に話しておくよ。",
                      speaker: "漁師",
                    },
                    {
                      type: "message",
                      text: "歪みが出るのは、北の森を抜けた先だ。森は昼でも暗いし、古い祠の門は、左右の石の台を動かさないと開かないらしい。",
                      speaker: "漁師",
                    },
                    {
                      type: "message",
                      text: "うちの網にも、紫がかった靄が絡みついてた夜があってね。あれは、森の奥から流れてくるんだと思う。",
                      speaker: "漁師",
                    },
                    {
                      type: "message",
                      text: "森に入るなら、灯守りの爺さんに会っていきな。祠の灯りを預かってる人だ。",
                      speaker: "漁師",
                    },
                    { type: "setFlag", flag: "chapter0_heard_rumor", value: true },
                  ],
                },
              ],
              else: [
                {
                  type: "message",
                  text: "最近、町外れで妙な光や音がするって噂だよ。歪みが増えてるんじゃないかねえ。",
                  speaker: "漁師",
                },
                {
                  type: "message",
                  text: "気になるなら、相談所に行ってみるといい。",
                  speaker: "漁師",
                },
              ],
            },
          ],
        },
      ],
    },
    {
      id: "touri-neighbor",
      tileX: TOURI_TOWN_LANDMARKS.innkeeperNeighbor.tileX,
      tileY: TOURI_TOWN_LANDMARKS.innkeeperNeighbor.tileY,
      color: "#c98fb0",
      commands: [
        {
          type: "if",
          flag: "chapter0_reto_joined",
          equals: true,
          then: [
            {
              type: "message",
              text: "レトさんとユーリちゃんが組むのかい。あの人は口は悪いが腕は確かだよ。",
              speaker: "宿屋の隣人",
            },
          ],
          else: [
            {
              type: "message",
              text: "宿屋の予約はまだまだ先まで埋まってないから、いつでもどうぞ（と言っても、まだ泊まれる部屋の準備はできていないみたいだけど）。",
              speaker: "宿屋の隣人",
            },
            {
              type: "message",
              text: "相談所のレトさんは、新人指導って言いつつ、いつも一人で調べ物をしてるみたいだね。",
              speaker: "宿屋の隣人",
            },
          ],
        },
      ],
    },
    {
      id: "touri-lampkeeper",
      tileX: 13,
      tileY: 3,
      color: "#b8a070",
      commands: lampkeeperCommands(),
    },
  ],
  "touri-branch": [
    {
      id: "touri-kasen",
      tileX: TOURI_BRANCH_LANDMARKS.kasen.tileX,
      tileY: TOURI_BRANCH_LANDMARKS.kasen.tileY,
      color: "#7a8fa6",
      spriteName: "カセン",
      commands: kasenCommands(),
    },
    {
      id: "touri-reto",
      tileX: TOURI_BRANCH_LANDMARKS.reto.tileX,
      tileY: TOURI_BRANCH_LANDMARKS.reto.tileY,
      color: "#a65a5a",
      spriteName: "レト",
      commands: retoCommands(),
    },
  ],
  "touri-forest-1": [
    loreNpc("touri-forest-signpost-lore", TOURI_FOREST1_LANDMARKS.signpost, [
      "古い木の看板がある。「この先、灯守りの森。祠の門は、ふたつの石の台が目覚めるとき開く」",
      "文字の下に、小さな灯りの模様が彫られている。",
    ]),
    {
      id: "touri-forest-traveler",
      tileX: TOURI_FOREST1_LANDMARKS.traveler.tileX,
      tileY: TOURI_FOREST1_LANDMARKS.traveler.tileY,
      color: "#7a9ab0",
      commands: [
        { type: "message", text: "おや、相談所の人かい。この先の森は、ここ数日、獣の気配が荒いよ。", speaker: "旅人" },
        {
          type: "message",
          text: "東の脇道に、旅人が置いていったらしい宝箱がある。それと、南西の茂みの奥にも、何かが隠れてたな。",
          speaker: "旅人",
        },
        { type: "message", text: "先へ進む前に、体力に余裕があるうちに寄り道しておくといい。", speaker: "旅人" },
      ],
    },
    chestNpc("touri-forest-chest-east", TOURI_FOREST1_LANDMARKS.chestEast, "chapter0_chest_forest_east", { gold: 40 }, "木の根元の宝箱を開けた！"),
    chestNpc(
      "touri-forest-chest-hidden",
      TOURI_FOREST1_LANDMARKS.chestHidden,
      "chapter0_chest_forest_hidden",
      { equipmentId: "treasure-7" },
      "茂みの奥の宝箱を開けた！",
    ),
  ],
  "touri-forest-2": [
    leverNpc("touri-forest-panel-west", TOURI_FOREST2_LANDMARKS.leverWest, "chapter0_lever_west", "chapter0_lever_east", "chapter0_shrine_open", {
      pull: "西の石の台に、灯り石をはめる穴がある。ランタンの灯りをかざすと、石が淡く光り、低い音が響いた。",
      already: "西の石の台は、もう淡く光っている。",
      opened: "東の台もすでに光っている。ふたつの光が呼び合い、北の方で、重い門の動く音がした！",
      waiting: "どこか遠くで、まだ眠っている石の気配がする。反対側にも、同じ台があるはずだ。",
    }),
    leverNpc("touri-forest-panel-east", TOURI_FOREST2_LANDMARKS.leverEast, "chapter0_lever_east", "chapter0_lever_west", "chapter0_shrine_open", {
      pull: "東の石の台に、ランタンの灯りをかざす。石が淡く光り、低い音が響いた。",
      already: "東の石の台は、もう淡く光っている。",
      opened: "西の台もすでに光っている。ふたつの光が呼び合い、北の方で、重い門の動く音がした！",
      waiting: "どこか遠くで、まだ眠っている石の気配がする。反対側にも、同じ台があるはずだ。",
    }),
    chestNpc("touri-forest-chest-shrine", TOURI_FOREST2_LANDMARKS.chest, "chapter0_chest_shrine", { gold: 60, equipmentId: "treasure-8" }, "祠の脇の宝箱を開けた！"),
    loreNpc("touri-forest-lore-shrine", TOURI_FOREST2_LANDMARKS.inscription, [
      "古い石碑に、擦れた文字が刻まれている。",
      "「環の欠片、森に降りて眠る。乱れた灯は、静まる夜を待て」",
      "この先に、乱れた灯り石の力――「歪み」が溜まっているのだろう。",
    ]),
  ],
  "touri-outskirts": [
    {
      id: "touri-scorch-mark",
      tileX: TOURI_OUTSKIRTS_LANDMARKS.scorchMark.tileX,
      tileY: TOURI_OUTSKIRTS_LANDMARKS.scorchMark.tileY,
      color: "#3a3a3a",
      commands: [
        {
          type: "if",
          flag: "chapter0_scorch_mark_found",
          equals: true,
          then: [{ type: "message", text: "焦げたような跡が、地面にくっきりと残っている。" }],
          else: [
            { type: "message", text: "地面に、何かが焼け焦げたような跡がある。" },
            { type: "message", text: "自然にできたにしては、輪郭がやけにまっすぐだ……。" },
            { type: "setFlag", flag: "chapter0_scorch_mark_found", value: true },
          ],
        },
      ],
    },
    {
      id: "chapter0-yugami",
      tileX: TOURI_OUTSKIRTS_LANDMARKS.yugami.tileX,
      tileY: TOURI_OUTSKIRTS_LANDMARKS.yugami.tileY,
      color: "#8a4fd6",
      commands: yugamiCommands(),
    },
  ],
};

function kasenCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter0_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter0_reported_to_kasen",
          equals: true,
          then: [
            {
              type: "message",
              text: "今日も無茶をしてきそうな顔だね、君たちは。次の依頼が来たら、また声をかけるよ。",
              speaker: "カセン",
            },
          ],
          else: [
            { type: "message", text: "戻ったか。それで、町外れの歪みは……", speaker: "カセン" },
            { type: "message", text: "しずめてきました。それと、気になるものを見つけたんです。", speaker: "ユーリ" },
            {
              type: "message",
              text: "地面に焼け焦げたような跡があって……あれは、自然に歪みが起きたようには見えませんでした。",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "……そうか。人の手で歪みを起こす方法があるとしたら、穏やかじゃないな。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "……昔、似たような話を聞いたことがある。あれは確か、「静まりの年」の頃に――",
              speaker: "カセン",
            },
            { type: "message", text: "……いや、なんでもない。昔のことだ、忘れてくれ。", speaker: "カセン" },
            {
              type: "message",
              text: "とにかく、よくやってくれた。この件は、念のため灯芯都にも報告しておくよ。",
              speaker: "カセン",
            },
            { type: "setFlag", flag: "chapter0_reported_to_kasen", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter0_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "町外れの歪みの件、頼んだよ。出発の前に、漁師と灯守りのおじいさんに話を聞くのを忘れずに。無理はしないようにね。",
              speaker: "カセン",
            },
          ],
          else: [
            {
              type: "message",
              text: "呼び立てて悪いね。実は、町外れで歪みの出る頻度が急に増えていてね。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "「歪み」というのは、灯り石の力が乱れて、形を持ってしまったものだ。獣のようだったり、影のようだったり、姿は場所によって変わる。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "近づいた人を迷わせたり、襲ったりする。放っておくと、少しずつ広がっていくんだ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "これまでは年に一度あるかないかだった。それが、この三週間で何度も出ている。夜になると、町外れの方角に紫がかった靄が見えると、漁師たちも怖がっていてね。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "頼みたいことは二つ。ひとつは、町外れの歪みをしずめること。もうひとつは、なぜ急に増えたのか、現場に手がかりが残っていないか調べることだ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "歪みは、灯り石の力に打ち勝てば、しずめられる。危険は確かにあるが、レトを一緒に行かせるから、ひとりにはしないよ。",
              speaker: "カセン",
            },
            {
              type: "choice",
              text: "依頼を受けますか？",
              options: [
                {
                  label: "受けます",
                  commands: [
                    { type: "setFlag", flag: "chapter0_quest_accepted", value: true },
                    {
                      type: "message",
                      text: "わかりました……でも、ちゃんと最後まで話を聞かせてください。",
                      speaker: "ユーリ",
                    },
                    { type: "message", text: "頼もしいね。レトも一緒に行かせるよ。", speaker: "カセン" },
                    {
                      type: "message",
                      text: "ただ、町の北の森は暗くて道も入り組んでいる。出発の前に、港の漁師と、灯守りのおじいさんに話を聞いておくといい。",
                      speaker: "カセン",
                    },
                    { type: "message", text: "武具屋で装備を整えるのも、忘れずにね。", speaker: "カセン" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [
                    {
                      type: "message",
                      text: "そうか、無理にとは言わないよ。気が向いたら声をかけておくれ。",
                      speaker: "カセン",
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

function retoCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter0_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter0_reto_joined",
          equals: true,
          then: [
            {
              type: "message",
              text: "次はどこへ行く？　……って、決めるのはお前だけどな。",
              speaker: "レト",
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter0_clue_c001_found",
              equals: true,
              then: reasoningQuizCommands(),
              else: [
                {
                  type: "message",
                  text: "戻ってきたか。……その前に、さっきの現場をもう一度見ておいで。何か気づくかもしれない。",
                  speaker: "レト",
                },
              ],
            },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter0_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "はいはい、そういうのは現場に着いてから言ってくれる？　先に行ってるよ。",
              speaker: "レト",
            },
          ],
          else: [
            { type: "message", text: "新人指導係のレトだ。まあ、よろしく。", speaker: "レト" },
            {
              type: "message",
              text: "……なんて、建前はどうでもいいか。歪みの件、詳しく話を聞いてやりな。",
              speaker: "レト",
            },
          ],
        },
      ],
    },
  ];
}

/**
 * 序章の推理パート（簡易版・チュートリアル）。`docs/story/mystery.md` 3の方針どおり、
 * 手がかり（C-001、歪みの人為的な痕跡）を使った選択式の問いを1つ置く。
 * 正解しなくても物語（レトの仲間加入）はそのまま進む。
 */
function reasoningQuizCommands(): EventCommand[] {
  return [
    {
      type: "message",
      text: "せっかくだから、一つ聞かせてくれ。あの歪み、どうしてこんな所に急に現れたと思う？",
      speaker: "レト",
    },
    {
      type: "choice",
      text: "レトにどう答える？",
      options: [
        {
          label: "誰かが意図して起こしたんだと思います",
          commands: [
            { type: "setFlag", flag: "chapter0_reasoning_correct", value: true },
            {
              type: "message",
              text: "誰かが意図して起こしたんだと思います。あの焼け跡、あまりにも整いすぎていました。",
              speaker: "ユーリ",
            },
          ],
        },
        {
          label: "灯り石の力が、たまたま乱れただけだと思います",
          commands: [
            { type: "setFlag", flag: "chapter0_reasoning_correct", value: false },
            {
              type: "message",
              text: "灯り石の力が、たまたま乱れただけだと思います。",
              speaker: "ユーリ",
            },
          ],
        },
        {
          label: "正直、まだ判断がつきません",
          commands: [
            { type: "setFlag", flag: "chapter0_reasoning_correct", value: false },
            { type: "message", text: "正直、まだ判断がつきません……。", speaker: "ユーリ" },
          ],
        },
      ],
    },
    {
      type: "if",
      flag: "chapter0_reasoning_correct",
      equals: true,
      then: [
        { type: "message", text: "その通りだと思う。手がかりから考える、その調子だ。", speaker: "レト" },
      ],
      else: [
        {
          type: "message",
          text: "……惜しいな。さっきの焼け跡、思い出してみろ。あんなにまっすぐな形、自然にできると思うか？",
          speaker: "レト",
        },
        {
          type: "message",
          text: "手がかりは、ちゃんと見返せば答えに繋がってる。次は気づけるといいな。",
          speaker: "レト",
        },
      ],
    },
    { type: "message", text: "やるじゃないか。思ったよりちゃんとやれるみたいだな。", speaker: "レト" },
    {
      type: "message",
      text: "……悪い、ちょっと先走った。素直に言うよ。これからも、お前の調査に付き合わせてくれ。",
      speaker: "レト",
    },
    { type: "message", text: "はい、よろしくお願いします！", speaker: "ユーリ" },
    { type: "setFlag", flag: "chapter0_reto_joined", value: true },
  ];
}

function yugamiCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter0_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter0_clue_c001_found",
          equals: true,
          then: [{ type: "message", text: "歪みが消えた場所は、今は静かなものだ。" }],
          else: [
            { type: "message", text: "歪みが消えたあとを、もう一度調べてみる。" },
            {
              type: "message",
              text: "……これは。歪みが生まれた中心に、規則正しく並んだ焼け跡がある。",
            },
            { type: "message", text: "自然に歪みが起きたにしては、あまりにも人為的だ……。" },
            { type: "setFlag", flag: "chapter0_clue_c001_found", value: true },
          ],
        },
      ],
      else: [
        { type: "message", text: "空気が歪み、紫色の光がうねっている。" },
        { type: "message", text: "「歪み」が、姿を現した！" },
        { type: "startBattle", battleId: "chapter0-yugami" },
      ],
    },
  ];
}

function lampkeeperCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter0_got_lamp",
      equals: true,
      then: [
        { type: "message", text: "森では、迷ったら道の灯りをたどりなさい。そして、祠の石の台を、ふたつとも目覚めさせるんだ。", speaker: "灯守り" },
        { type: "message", text: "武具屋で装備を整えるのも、忘れずにな。", speaker: "灯守り" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter0_heard_rumor",
          equals: true,
          then: [
            { type: "message", text: "ほう、漁師から聞いたのかい。ちょうど、森へ入る人に灯りを貸しておるところだ。", speaker: "灯守り" },
            {
              type: "message",
              text: "この灯り石のランタンは、森の祠の石の台にも反応する。灯りをかざせば、台が目覚めるはずだ。",
              speaker: "灯守り",
            },
            { type: "message", text: "「灯り石のランタン」を受け取った。これで、森へ入れる。", speaker: undefined },
            { type: "setFlag", flag: "chapter0_got_lamp", value: true },
            { type: "message", text: "森の奥の「歪み」は、あの祠の下に溜まっておる。気をつけて行くんだよ。", speaker: "灯守り" },
          ],
          else: [
            {
              type: "if",
              flag: "chapter0_quest_accepted",
              equals: true,
              then: [
                { type: "message", text: "相談所の新しい子かい。森へ入りたいなら、まず港の漁師の話を聞いておいで。", speaker: "灯守り" },
                { type: "message", text: "あの子は、森の様子に詳しい。話を聞いたら、またここへおいで。", speaker: "灯守り" },
              ],
              else: [
                { type: "message", text: "町の北の森は、ふだんは静かな場所だ。だが最近は、様子がおかしくてな。", speaker: "灯守り" },
                { type: "message", text: "相談所で依頼を受けたなら、ここへ来なさい。灯りを貸してあげよう。", speaker: "灯守り" },
              ],
            },
          ],
        },
      ],
    },
  ];
}
