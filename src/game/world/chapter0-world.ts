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
  { type: "message", text: "――統暦412年、春の終わり。大陸アルテシア、港町・灯里。" },
  {
    type: "message",
    text: "ユーリは「灯りの相談所」灯里支部の新人調査員。16歳。左手首には、祖父の形見の腕輪がある。",
  },
  {
    type: "message",
    text: "祖父のソウイチは、ユーリが生まれる前の「静まりの年」に姿を消した。ユーリは、会ったことがない。",
  },
  { type: "message", text: "腕輪の石は、くすんだ青色で、いつもほんのり温かい。" },
  { type: "message", text: "祖父は消える前に、「いつか生まれる孫に、この腕輪を頼む」と言い残したのだと、母から聞いている。" },
  {
    type: "message",
    text: "ここ十日ほど、町外れで「歪み」――灯り石の力が乱れて生まれる異形――が、いつになく頻繁に現れているという。",
  },
  { type: "message", text: "支部長のカセンが、朝いちばんに来てほしいと呼んでいる。相談所へ向かおう。" },
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
              text: "町外れの歪みがおとなしくなったって聞いたよ。ユーリのおかげかい？",
              speaker: "ガンジ",
            },
            { type: "message", text: "港の魚も安心して獲れるってもんだ。ありがとよ。", speaker: "ガンジ" },
            {
              type: "message",
              text: "……おまえは、ソウイチさんに似てきたなあ。人のために走るところがよ。",
              speaker: "ガンジ",
            },
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
                      speaker: "ガンジ",
                    },
                  ],
                  else: [
                    {
                      type: "message",
                      text: "ああ、相談所の依頼を受けたのかい。なら、先に話しておくよ。",
                      speaker: "ガンジ",
                    },
                    {
                      type: "message",
                      text: "うちの若いのが、夜釣りの帰りに、町外れの草地で紫の光を見たんだ。耳鳴りみたいな音もしたそうだ。",
                      speaker: "ガンジ",
                    },
                    {
                      type: "message",
                      text: "草地へ行くには、北の森を抜ける。森は昼でも暗いし、古い祠の門は、左右の石の台を動かさないと開かないらしい。",
                      speaker: "ガンジ",
                    },
                    {
                      type: "message",
                      text: "森に入るなら、灯守りの爺さんに会っていきな。祠の灯りを預かってる人だ。",
                      speaker: "ガンジ",
                    },
                    {
                      type: "message",
                      text: "……それから、気をつけてな。おまえの祖父さん、ソウイチさんには、俺も世話になった。",
                      speaker: "ガンジ",
                    },
                    { type: "setFlag", flag: "chapter0_heard_rumor", value: true },
                  ],
                },
              ],
              else: [
                {
                  type: "message",
                  text: "おう、ユーリ。今朝もいい天気だぞ。……ところでな、最近、町外れの草地で、妙な光や音がするって噂だ。",
                  speaker: "ガンジ",
                },
                {
                  type: "message",
                  text: "夜釣りの帰りに、ぼうっと紫の光が見えたとか、耳鳴りみたいな音がしたとか。歪みが増えてるんじゃねえかってな。",
                  speaker: "ガンジ",
                },
                {
                  type: "message",
                  text: "おまえ、相談所の人間だろう。ちょっと気にしといてくれ。支部長も、今朝は呼んでるはずだ。",
                  speaker: "ガンジ",
                },
                {
                  type: "message",
                  text: "ハルカさんも、いい息子を持ったもんだ。……そういや、おまえの祖父さんのソウイチさんに、俺は網の結び方を教わったんだ。",
                  speaker: "ガンジ",
                },
                { type: "message", text: "祖父を知っているんですか。", speaker: "ユーリ" },
                {
                  type: "message",
                  text: "ああ。あの人には世話になった。だから、あの年のことは、今でもたまに夢に見る。",
                  speaker: "ガンジ",
                },
                {
                  type: "message",
                  text: "灯芯都に出かけて、それきりだったろう。たしか、疫病が流行って、連絡もつかなくなって……いや、すまねえ。湿っぽい話だった。",
                  speaker: "ガンジ",
                },
                {
                  type: "message",
                  text: "（祖父の話をしかけて、みんなやめてしまう。……いつか、ちゃんと聞かせてもらおう）",
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
              text: "あんた、旅に出るんだってね。……さっきは言いすぎたよ。怖かったんだ、あたしも。",
              speaker: "布屋の女将",
            },
            {
              type: "message",
              text: "レトさんと組むのかい。あの人は口は悪いが腕は確かだよ。ほら、旅の途中で食べな。",
              speaker: "布屋の女将",
            },
            { type: "message", text: "干し杏の入った小さな袋をもらった。" },
            {
              type: "message",
              text: "ふん。ちゃんと戻ってきなよ。じゃないと、干し杏の代金を取りっぱぐれるからね。",
              speaker: "布屋の女将",
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter0_yugami_defeated",
              equals: true,
              then: [
                {
                  type: "message",
                  text: "町外れの歪みを、しずめてくれたんだってね。……やっとうちの商売も、落ち着きそうだよ。",
                  speaker: "布屋の女将",
                },
                {
                  type: "message",
                  text: "相談所がどうのと、きついことを言ったね。あれは怖さが言わせたのさ。気にしないどくれ。",
                  speaker: "布屋の女将",
                },
              ],
              else: [
                {
                  type: "message",
                  text: "あんたたち相談所は、何をやってるんだい。町の近くで歪みだなんて、商売あがったりだよ。",
                  speaker: "布屋の女将",
                },
                {
                  type: "message",
                  text: "雑貨屋のドウマさんも、町外れの倉庫から青い顔で戻ってきてね。店を閉めっぱなしさ。",
                  speaker: "布屋の女将",
                },
                {
                  type: "message",
                  text: "……ふん。言い方がきつかったね。ほら、干し杏だ。朝ごはんは食べたかい？　じゃあ、おやつだよ。",
                  speaker: "布屋の女将",
                },
                { type: "message", text: "干し杏をひとつもらった。ほんの少し酸っぱく、それから甘い。" },
                { type: "message", text: "（この町の人は、怒りながら、やさしい）" },
              ],
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
            { type: "message", text: "焦げ臭さもない。かわりに、雨上がりの石のような、冷たい匂いがする。" },
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
              type: "if",
              flag: "chapter0_reto_joined",
              equals: true,
              then: [
                {
                  type: "if",
                  flag: "chapter0_kasen_farewell",
                  equals: true,
                  then: [
                    {
                      type: "message",
                      text: "気をつけて行っておいで。怖くなったら、逃げるんじゃなくて、帰っておいで。ここは、あんたの帰る場所だよ。",
                      speaker: "カセン",
                    },
                  ],
                  else: [
                    {
                      type: "message",
                      text: "旅に出ると聞いたよ。歪みのことと、静まりの年のこと……ソウイチさんのことも調べたいんだね。",
                      speaker: "カセン",
                    },
                    {
                      type: "message",
                      text: "ソウイチさんは、私の同僚だった。朝が早くて、歌が下手で、石ころを拾ってきては机に並べる人だったよ。",
                      speaker: "カセン",
                    },
                    { type: "message", text: "母も、同じことを言っていました。", speaker: "ユーリ" },
                    {
                      type: "message",
                      text: "あの年のことは、まだ話せない。……いや、話す資格が、私にはないのかもしれない。あの年、私は何もできなかった。",
                      speaker: "カセン",
                    },
                    {
                      type: "message",
                      text: "ひとつだけ言っておくよ。歪みを人の手で起こす者が、もしいるなら、きっと、どこかで見ている。",
                      speaker: "カセン",
                    },
                    {
                      type: "message",
                      text: "あんたたちが動けば、向こうも動く。誰が味方で誰が敵か、簡単には分からないからね。",
                      speaker: "カセン",
                    },
                    {
                      type: "message",
                      text: "これを持っておゆき。通行手形と、小さな灯り石が三つ。いざというとき、私に声を届けられる。",
                      speaker: "カセン",
                    },
                    { type: "message", text: "「通行手形」と「通信用の灯り石」を受け取った。" },
                    {
                      type: "message",
                      text: "傷薬と灯り草の煎じ薬も入れておいたよ。それから……無茶は、しないこと。",
                      speaker: "カセン",
                    },
                    { type: "message", text: "はい。……あ、その返事が、いちばん信用ならないんですよね。", speaker: "ユーリ" },
                    { type: "message", text: "分かっているじゃないか。気をつけて行っておいで。", speaker: "カセン" },
                    { type: "setFlag", flag: "chapter0_kasen_farewell", value: true },
                  ],
                },
              ],
              else: [
                {
                  type: "message",
                  text: "今日も無茶をしてきそうな顔だね、君たちは。レトにも、あとで声をかけてやっておくれ。",
                  speaker: "カセン",
                },
              ],
            },
          ],
          else: [
            { type: "message", text: "戻ったか。それで、町外れの歪みは……", speaker: "カセン" },
            {
              type: "message",
              text: "しずめてきました。はぐれ歪みが三体、そのあとに大きなものが一体。ドウマさんの倉庫の荷物も、もう大丈夫です。",
              speaker: "ユーリ",
            },
            { type: "message", text: "そうか。……ふたりとも、本当によくやってくれたね。", speaker: "カセン" },
            { type: "message", text: "それと、気になるものを見つけたんです。", speaker: "ユーリ" },
            {
              type: "message",
              text: "草地の焦げ跡は、輪郭がまっすぐで、焦げた匂いもしませんでした。中心には、灯り石の粉で描いた溝の図が。",
              speaker: "ユーリ",
            },
            { type: "message", text: "北の端に埋まっていた灰色の石も、持ってきた。", speaker: "レト" },
            { type: "message", text: "（レトが、布に包んだ灰色の石を机に置いた）" },
            {
              type: "message",
              text: "あれは、自然に歪みが起きたようには見えませんでした。",
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
            { type: "message", text: "支部長。今、静まりの年って。", speaker: "レト" },
            { type: "message", text: "……言ったかね？　年を取ると、口がすべるんだよ。", speaker: "カセン" },
            { type: "message", text: "……いや、なんでもない。昔のことだ、忘れておくれ。", speaker: "カセン" },
            {
              type: "message",
              text: "とにかく、よくやってくれた。この件は、念のため灯芯都にも報告しておく。その石は預かるよ。",
              speaker: "カセン",
            },
            { type: "message", text: "今日は休みなさい。ふたりとも、疲れているだろう。", speaker: "カセン" },
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
              text: "町外れの歪みの件、頼んだよ。出発の前に、漁師のガンジと灯守りのおじいさんに話を聞くのを忘れずに。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "それから、無茶はしないこと。その「しませんよ」が、いちばん信用ならないんだけどね。",
              speaker: "カセン",
            },
          ],
          else: [
            { type: "message", text: "おや、来たね。今日も無茶をしてきそうな顔だ、君は。", speaker: "カセン" },
            { type: "message", text: "さっき、ガンジさんに会ったろう。顔に「心配ごとを聞かされました」と書いてあるよ。", speaker: "カセン" },
            {
              type: "message",
              text: "呼び立てて悪いね。実は、町外れで歪みの出る頻度が、急に増えていてね。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "ここ十日ほどで、確認できただけでも三度。町外れの草地と、旧い街道の脇だ。ごく小さなものばかりだった。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "ところが昨日の夕方、雑貨屋のドウマさんが倉庫に行ったとき、大きめのに出くわしてね。逃げてきて無事だったが、荷物は置いたままだ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "「歪み」は、灯り石の力が乱れて、輪郭のさだまらない形をとったものだ。ふつうは、山奥や古い坑道で出る。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "近づいた人を迷わせたり、襲ったりする。放っておくと、少しずつ広がっていくんだ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "けれど、この町の外れに古い坑道はない。少なくとも、私は知らない。だから、おかしいんだよ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "頼みたいことは二つ。ひとつは、町外れの歪みをしずめること。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "もうひとつは、なぜ急に増えたのか、現場に手がかりが残っていないか調べることだ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "調べるときの心得を、ひとつ教えておく。現場は、徹底的に調べるんだ。見えているものだけで済ませてはいけないよ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "調べたい物の前に立って、決定ボタンを押す。草むら、壁、荷物、足もとに落ちている物……ひとつひとつ、全部だ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "手がかりは、目立たない場所ほど深く隠れているものさ。同じ場所でも、何度か調べてみると、新しいことに気づくこともある。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "真相に近づく人は、いつも見落とさない人だ。急がず、隅々まで。それが調査の基本だよ。",
              speaker: "カセン",
            },
            { type: "message", text: "はい。ひとつも見落とさないように、隅々まで調べます。", speaker: "ユーリ" },
            {
              type: "message",
              text: "歪みは、灯り石の力に打ち勝てば、しずめられる。危険はあるが、ひとりでは行かせないよ。レトを付ける。「新人指導」ってやつさ。",
              speaker: "カセン",
            },
            {
              type: "message",
              text: "……あの子も、たまには誰かと歩いたほうがいいからね。",
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
                    { type: "message", text: "頼もしいね。傷薬と灯り草の煎じ薬、それと飴玉だ。持っておいき。", speaker: "カセン" },
                    {
                      type: "message",
                      text: "飴玉は、孫にやるつもりで買ったんだがね。あの子は、甘いものを食べすぎだ。",
                      speaker: "カセン",
                    },
                    {
                      type: "message",
                      text: "草地へ行くには、北の森を通る。暗くて道も入り組んでいる。出発の前に、港の漁師と、灯守りのおじいさんに話を聞いておくといい。",
                      speaker: "カセン",
                    },
                    { type: "message", text: "武具屋で装備を整えるのも、忘れずにね。レトにも声をかけておくれ。", speaker: "カセン" },
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
              text: "レトさん。支部長に言われて来ました。今日から、よろしくお願いします。",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "はいはい、そういうのは現場に着いてから言ってくれる？　先に行ってるよ。",
              speaker: "レト",
            },
            {
              type: "message",
              text: "じゃあ、現場に着いてから、もう一度言います。",
              speaker: "ユーリ",
            },
            {
              type: "message",
              text: "……おう。ひとつだけ教えとく。歪みを見るところは三つ。足元と、輪郭と、呼吸だ。",
              speaker: "レト",
            },
            {
              type: "message",
              text: "輪郭の濃いところは硬い。薄いところは剣が通る。歪みも息をする。縮む直前に、ほんのわずか止まる。そこが間合いだ。",
              speaker: "レト",
            },
            {
              type: "message",
              text: "怖いか？　怖いのは正しい。怖くないやつは死ぬ。怖がりすぎるやつも死ぬ。ちょうどいい怖がり方を覚えな。",
              speaker: "レト",
            },
          ],
          else: [
            { type: "message", text: "お前が新人か。……その剣の握りの凹み、毎日振ってる証拠だな。", speaker: "レト" },
            {
              type: "message",
              text: "力が入ると、先に手がこわばる。次の稽古では、握るとき小指から意識してみな。",
              speaker: "レト",
            },
            { type: "message", text: "それと、靴ひもがほどけてる。", speaker: "レト" },
            { type: "message", text: "あっ、本当だ！", speaker: "ユーリ" },
            {
              type: "message",
              text: "悪い、ほめるつもりだったのに、順番を間違えた。……歪みの件は、まず支部長の話を聞いてきな。",
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
    { type: "message", text: "……なあ。夕方の港で、少し話をしていいか。", speaker: "レト" },
    { type: "message", text: "（ふたりは、夕暮れの港へ歩いた。突堤の先で、波が石を洗っている）" },
    { type: "message", text: "俺は、あの「静まりの年」を調べてる。身内を、あの年に亡くしてな。", speaker: "レト" },
    {
      type: "message",
      text: "兄貴だ。俺が六つのとき。灯芯都の合議会で、書記官をやってた。頭がよくて、優しい人だった。",
      speaker: "レト",
    },
    {
      type: "message",
      text: "役所から「疫病で亡くなった」と知らせが来た。それだけだ。遺体は見せてもらえず、葬式もなかった。",
      speaker: "レト",
    },
    {
      type: "message",
      text: "でも、疫病なんて流行ってなかった。兄貴と同じ職場の人たちも、次々に消えた。だから、大人になって調べ始めた。",
      speaker: "レト",
    },
    {
      type: "message",
      text: "お前を巻き込むつもりはなかった。ただ、あの草地に立って確信した。あれは、静まりの年に繋がる話だ。",
      speaker: "レト",
    },
    { type: "message", text: "だから、隠しごとをしたまま組むのは、筋が通らない。", speaker: "レト" },
    { type: "message", text: "レトさん。……ぼくにも、知りたいことがあります。祖父のことです。", speaker: "ユーリ" },
    {
      type: "message",
      text: "祖父も、静まりの年にいなくなりました。ぼくが生まれる四年前です。だから、会ったことがありません。",
      speaker: "ユーリ",
    },
    {
      type: "message",
      text: "母は言っていました。祖父は消える前の晩、「いつか生まれる孫に、この腕輪を頼む」と言ったって。",
      speaker: "ユーリ",
    },
    {
      type: "message",
      text: "今日、歪みの目の中に、誰かの影が見えた気がしたんです。あれが何だったのか、知りたい。",
      speaker: "ユーリ",
    },
    { type: "message", text: "一緒に行きます。静まりの年のことを調べる旅に。", speaker: "ユーリ" },
    { type: "message", text: "……ありがとな。", speaker: "レト" },
    {
      type: "message",
      text: "……悪い、ちょっと先走った。素直に言うよ。これからも、お前の調査に付き合わせてくれ。",
      speaker: "レト",
    },
    { type: "message", text: "はい、よろしくお願いします！", speaker: "ユーリ" },
    { type: "message", text: "お前、返事だけは立派だな。……いや、ほめてるんだ。", speaker: "レト" },
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
              text: "……これは。歪みが生まれた中心に、細い溝が刻まれている。中心から広がる直線と、それを囲む円だ。",
            },
            { type: "message", text: "溝の底には、灯り石の粉が薄く敷きつめられている。誰かが、図を描いたのだ。" },
            { type: "message", text: "円の北の端には、灰色の石が埋まっていた。描いた人が、場所を覚えるための目印だろうか。" },
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
