import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 町の人たち（各町に3人）。1人目は「道案内」で、いまの進み具合（依頼の前・調査中・報告前・報告後）に合わせて次の行き先を教える。
 * 2人目・3人目は、その町の暮らしや、この世界の言い伝えを話す（サブストーリーの依頼人とは別）。
 * 仮: セリフは簡易。
 */
interface TownAmbient {
  mapId: string;
  /** 依頼を出す人（道案内のセリフに出る）。 */
  giver: string;
  /** 調査する場所。 */
  place: string;
  /** 次の行き先。 */
  next: string;
  /** 章のフラグ。 */
  accepted: string;
  defeated: string;
  reported: string;
  guide: { name: string; tileX: number; tileY: number };
  locals: { name: string; tileX: number; tileY: number; lines: string[]; color: string }[];
}

const TOWNS: TownAmbient[] = [
  {
    mapId: "touri-town", giver: "灯りの相談所の支部長カセン", place: "町外れ（歪みの発生地点）", next: "東の街道の先の、麦香野の村",
    accepted: "chapter0_quest_accepted", defeated: "chapter0_yugami_defeated", reported: "chapter0_reported_to_kasen",
    guide: { name: "港の案内人", tileX: 4, tileY: 8 },
    locals: [
      { name: "漁師", tileX: 14, tileY: 4, color: "#7a9ab0", lines: ["今朝は、いい潮だったよ。灯里の魚は、灯り石の光を浴びて育つから、夜でもほんのり光るんだ。", "町の外れに、変な靄が出るようになってね。船を出すのも、少し気味が悪いよ。"] },
      { name: "パン屋", tileX: 7, tileY: 2, color: "#c8a070", lines: ["焼きたてのパンは、灯り石のかまどで焼くんだよ。ふわっと、いい香りがするだろう？", "相談所の新人さんかい？ 疲れたら、うちのパンを食べていきな。"] },
    ],
  },
  {
    mapId: "mugikano-village", giver: "村長", place: "北の水源", next: "東の街道の先の、硝子湖の町",
    accepted: "chapter1_quest_accepted", defeated: "chapter1_yugami_defeated", reported: "chapter1_reported_to_elder",
    guide: { name: "旅の行商人", tileX: 6, tileY: 6 },
    locals: [
      { name: "農婦", tileX: 15, tileY: 12, color: "#a0b070", lines: ["麦は、水と風の恵みだよ。水路が止まると、村じゅうが困ってしまうんだ。", "収穫祭では、麦の穂の飾りを、みんなで持ち寄るんだよ。"] },
      { name: "水車小屋の子", tileX: 3, tileY: 3, color: "#e0c890", lines: ["水車の音を聞くとね、ぼく、落ち着くんだ。", "大きくなったら、水車を直す仕事がしたいな。"] },
    ],
  },
  {
    mapId: "garasuko-town", giver: "ガイド", place: "密輸倉庫", next: "東の街道の先の、鉄鏈鉱山の町",
    accepted: "chapter2_quest_accepted", defeated: "chapter2_yugami_defeated", reported: "chapter2_reported_to_guide",
    guide: { name: "湖の水先案内人", tileX: 13, tileY: 5 },
    locals: [
      { name: "織り子", tileX: 9, tileY: 3, color: "#b080a0", lines: ["この町の布は、湖の光を織りこんであるんだよ。夕方に見ると、きらきらするのさ。", "船の帆も、うちで織るんだ。風をよくはらむ、いい布だろう？"] },
      { name: "釣り人", tileX: 17, tileY: 3, color: "#809ab0", lines: ["湖の底には、昔の町が沈んでるって話だよ。真夜中に、鐘の音が聞こえることがあるんだ。", "今日は、ぜんぜん釣れないなあ。"] },
    ],
  },
  {
    mapId: "tetsukusari-town", giver: "組合代表のオルカ", place: "北の坑道", next: "東の街道の先の、砂音の町",
    accepted: "chapter3_quest_accepted", defeated: "chapter3_yugami_defeated", reported: "chapter3_reported_to_orca",
    guide: { name: "坑道の案内人", tileX: 4, tileY: 12 },
    locals: [
      { name: "鉱夫の妻", tileX: 6, tileY: 10, color: "#a08070", lines: ["うちの人は、毎朝、暗いうちに坑道へ入るの。無事に帰ってくるまで、気が気でなくてね。", "この町では、鉄鎖を「命綱」って呼ぶのよ。"] },
      { name: "鍛冶屋の弟子", tileX: 16, tileY: 10, color: "#c08050", lines: ["親方が言うんだ。「鉄は、叩かれるほど強くなる」って。おれも、そうなりたいな。", "火の色を見れば、鉄の機嫌がわかるんだってさ。まだ、ぜんぜんわからないけど。"] },
    ],
  },
  {
    mapId: "sanone-town", giver: "隊商の組合長", place: "隊商の野営地", next: "東の街道の先の、霧断崖の町",
    accepted: "chapter4_quest_accepted", defeated: "chapter4_yugami_defeated", reported: "chapter4_reported",
    guide: { name: "砂漠の道案内", tileX: 5, tileY: 7 },
    locals: [
      { name: "香辛料商人", tileX: 17, tileY: 7, color: "#d09050", lines: ["砂音の市場は、日が沈んでからが本番さ。灯りがともると、店がずらっと並ぶんだ。", "この赤い粉は、ひとつまみで、料理がぐっと引きしまるよ。"] },
      { name: "ラクダ番", tileX: 11, tileY: 7, color: "#b09060", lines: ["うちのラクダは、風の向きを読むのがうまいんだ。ひと吠えしたら、砂嵐が近いってことさ。", "ラクダは頑固だけど、いちど仲良くなれば、一生の相棒だよ。"] },
    ],
  },
  {
    mapId: "kiri-town", giver: "司祭", place: "北の記録の間", next: "東の街道の先の、霜原の町",
    accepted: "chapter5_quest_accepted", defeated: "chapter5_yugami_defeated", reported: "chapter5_reported",
    guide: { name: "巡礼の案内人", tileX: 3, tileY: 6 },
    locals: [
      { name: "鐘つき", tileX: 12, tileY: 6, color: "#a0a8c0", lines: ["朝と夕、鐘をつくのが、わたしの仕事。霧の日は、鐘の音を頼りに、旅の人が町へ戻ってくるんだよ。", "鐘の音がやんだら、それは、霧が濃すぎるっていう合図さ。"] },
      { name: "巡礼の老婆", tileX: 15, tileY: 3, color: "#b0a0b0", lines: ["環の祠に、毎朝ひとつ、灯りをともすの。三十年、続けているのよ。", "灯りはね、誰かを照らすためだけじゃなく、自分の心を照らすためにもあるのよ。"] },
    ],
  },
  {
    mapId: "shimohara-town", giver: "番所の守り", place: "戦跡の施設", next: "空の乗り物で行く、浮嶼",
    accepted: "chapter6_quest_accepted", defeated: "chapter6_yugami_defeated", reported: "chapter6_reported",
    guide: { name: "雪原の道案内", tileX: 5, tileY: 6 },
    locals: [
      { name: "薪割りの少年", tileX: 14, tileY: 7, color: "#a0b0c8", lines: ["冬の間は、薪がいのちだよ。ぼく、毎日、百本割るんだ。", "雪が降ると、世界がしんと静かになるんだ。それが好きなんだよ。"] },
      { name: "織物の老人", tileX: 20, tileY: 7, color: "#a0a0b8", lines: ["霜原の毛織物は、暖かいことで有名じゃ。わしが若いころは、大乱期の兵隊さんの外套も織ったもんじゃよ。", "戦のあとの雪は、何もかもを、白く覆ってくれる。良いことも、悪いこともな。"] },
    ],
  },
  {
    mapId: "fushima-town", giver: "雲海衆の長老", place: "北の整備区画", next: "空の乗り物で行く、灯芯都",
    accepted: "chapter7_quest_accepted", defeated: "chapter7_yugami_defeated", reported: "chapter7_reported",
    guide: { name: "島の案内人", tileX: 5, tileY: 7 },
    locals: [
      { name: "凧職人", tileX: 12, tileY: 6, color: "#90b0d0", lines: ["この島の子どもたちは、凧を上げて遊ぶんだ。糸が切れたら、雲の海へ落ちていってしまうけどね。", "風の強い日は、いい凧が作れるんだよ。"] },
      { name: "雲海衆の若者", tileX: 18, tileY: 7, color: "#8090b0", lines: ["おれたちの祖先は、空を渡っていた民なんだ。今は島に暮らしてるけど、風の匂いは、忘れないよ。", "雲の上から見る朝日は、世界でいちばんきれいだと思う。"] },
    ],
  },
  {
    mapId: "toushin-town", giver: "議事官", place: "合議会堂", next: "議長の許しが出たあとの、最果ての虚灯宮",
    accepted: "chapter8_quest_accepted", defeated: "chapter8_yugami_defeated", reported: "chapter8_reported",
    guide: { name: "都の案内人", tileX: 3, tileY: 10 },
    locals: [
      { name: "書記見習い", tileX: 20, tileY: 10, color: "#8a90b0", lines: ["合議会堂の書庫には、大陸じゅうの記録が眠っているんだ。全部読むには、百年かかるって言われてるよ。", "おれ、いつか、記録をまとめて、本にするのが夢なんだ。"] },
      { name: "花売りの娘", tileX: 8, tileY: 14, color: "#d0a0b0", lines: ["噴水のそばの花は、毎朝、わたしが替えているのよ。灯芯都には、いつも、花が似合うでしょう？", "都は、とても大きくて、にぎやか。でも、ときどき、少しだけ、寂しい街に見えるの。"] },
    ],
  },
];

function guideCommands(town: TownAmbient, name: string): EventCommand[] {
  return [
    {
      type: "if",
      flag: town.reported,
      equals: true,
      then: [say(name, `${town.giver}への報告は、もう済んだね。次の目的地は、${town.next}だよ。準備ができたら、向かうといい。`)],
      else: [
        {
          type: "if",
          flag: town.defeated,
          equals: true,
          then: [say(name, `無事に片づけたんだね！ ${town.giver}のところへ戻って、報告しよう。`)],
          else: [
            {
              type: "if",
              flag: town.accepted,
              equals: true,
              then: [
                say(name, `調べるのは、${town.place}だよ。敵に出会ったら、たたかってレベルを上げておくと、奥のボスも戦いやすくなる。`),
                say(name, "メニュー（Tabキー）で、みんなのつよさが見られるよ。"),
              ],
              else: [say(name, `まずは、${town.giver}に話を聞いてみるといい。依頼をこなして、この町の事件を解決しよう。`)],
            },
          ],
        },
      ],
    },
  ];
}

export const AMBIENT_NPCS: Record<string, Npc[]> = Object.fromEntries(
  TOWNS.map((town) => [
    town.mapId,
    [
      {
        id: `ambient-${town.mapId}-guide`,
        tileX: town.guide.tileX,
        tileY: town.guide.tileY,
        color: "#e0e0a0",
        commands: guideCommands(town, town.guide.name),
      },
      ...town.locals.map((local, i) => ({
        id: `ambient-${town.mapId}-local${i + 1}`,
        tileX: local.tileX,
        tileY: local.tileY,
        color: local.color,
        commands: local.lines.map((text) => say(local.name, text)),
      })),
    ],
  ]),
);
