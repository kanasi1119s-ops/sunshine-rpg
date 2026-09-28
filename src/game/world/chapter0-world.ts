import { createTouriTownData, TOURI_TOWN_SPAWN, TOURI_TOWN_LANDMARKS } from "../map/chapter0/touri-town";
import { createTouriBranchData, TOURI_BRANCH_LANDMARKS } from "../map/chapter0/touri-branch";
import { createTouriOutskirtsData, TOURI_OUTSKIRTS_LANDMARKS } from "../map/chapter0/touri-outskirts";
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
                  type: "message",
                  text: "町外れは物騒だって聞くよ。気をつけて行っておいで。",
                  speaker: "漁師",
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
              text: "町外れの歪みの件、頼んだよ。無理はしないようにね。",
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
              text: "調査と、できれば……そこにいる歪みをしずめてきてほしいんだ。",
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
