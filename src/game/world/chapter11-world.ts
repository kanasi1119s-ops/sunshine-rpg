import { createShrineData, SHRINE_ENTRY, SHRINE_LANDMARKS, type ShrinePalette } from "../map/chapter11/god-shrines";
import { GODS } from "../battle/chapter11-enemies";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { say } from "./side-story";

/**
 * 8神（`docs/story/secret-boss.md` 3章、roadmap 6-4〜6-7）。裏ボス「初源の歪み」を倒したあと、各地方の禁域に挑める。
 * 各禁域は、その地方の地図にある「禁域の入口」から入る1部屋。神を倒し、奥の祭壇から「環の欠片」を持ち帰る。
 * 8つそろうと、虚灯宮・深部の転移陣が起動する（`chapter10-world.ts` の `deep4-circle`）。
 * 撃破報酬: 女神・純神・鬼神・蟲神は、天神・悪神ジョブの解放（`chapter{N}_defeated` フラグで、ジョブ画面に出る）。武神・無神・異神・冥神は、最強クラスの装備（仮。会話のみ）。ボスの絵は図形。
 */
interface GodShrine {
  palette: ShrinePalette;
  /** 入口を置く地方の地図と座標（すぐ下のタイルが、禁域から戻ってきたときの立ち位置）。 */
  entrance: { mapId: string; tileX: number; tileY: number };
  /** 入口の見た目・場所の説明。 */
  entranceText: string;
  intro: string[];
  lore: string;
  defeat: string[];
  /** 撃破報酬（仮）。 */
  reward: string;
}

const SHRINES: GodShrine[] = [
  {
    palette: { floor: "#b8c890", wall: "#3a4a30", pillar: "#7a9a60", altar: "#e8e0a0" },
    entrance: { mapId: "mugikano-water-source", tileX: 8, tileY: 4 },
    entranceText: "涸れた水源の最奥、水の音が止まった壁の前に、ひび割れた石扉がある。",
    intro: ["やわらかな水の光が満ちている。かつて涸れた水源の、いちばん奥。", "……水を、涸らした者たちの、子らですか。ここで、何を求めますか。", "この土地の恵みを預かる者として、確かめさせていただきます。"],
    lore: "壁に、水と麦穂の紋が刻まれている。「恵みは、返すものであって、奪うものではない」。",
    defeat: ["……よい心の持ち主たちです。恵みは、ふたたび、この土地に還りましょう。", "この欠片を、お持ちなさい。生命を預かる光の、ひとかけらです。"],
    reward: "天神ジョブ「女神の巫覡」を装備できるようになった！（ジョブ画面）",
  },
  {
    palette: { floor: "#8a9a70", wall: "#2a3020", pillar: "#5a6a3a", altar: "#c8d090" },
    entrance: { mapId: "garasuko-warehouse", tileX: 8, tileY: 4 },
    entranceText: "倉庫の奥、朽ちた葦原に続く、湿った通路がある。羽音のようなものが聞こえる。",
    intro: ["湿った葦の間に、無数の羽音が渦を巻いている。", "……ぶーん。ぶーん。……いつから、こんなに、遠い音になったのか。", "理由もなく、命を刈り取るのが、わたしの役目になってしまった。止めて、くれ。"],
    lore: "沈没船の骨組みに、小さな虫の骸が積もっている。ここは、命の終わりを見送る場所だった。",
    defeat: ["……ああ、羽音が、静かになっていく。もう、誰も、理由なく傷つけなくていい。", "この欠片を。……ありがとう、忘れられていた、わたしを。"],
    reward: "悪神ジョブ「蟲神の呪術師」を装備できるようになった！（ジョブ画面）",
  },
  {
    palette: { floor: "#7a4a3a", wall: "#2a1410", pillar: "#a05a3a", altar: "#ffb060" },
    entrance: { mapId: "tetsukusari-mine", tileX: 11, tileY: 4 },
    entranceText: "坑道の最深部、マグマの脈が走る壁に、焼けただれた扉がある。",
    intro: ["熱気が、肌を焼く。赤い脈が、床を這っている。", "壊し、鍛え、燃やす。それが、俺の在り方だ。……お前らは、何を鍛える。", "筋を通す相手には、拳で答えよう。かかってこい。"],
    lore: "壁の鉄板に、無数の槌の跡。「壊れたものは、鍛え直せばいい」と読める。",
    defeat: ["……筋は、通ったな。壊すだけが、鍛冶ではない。お前らは、それを、知っていた。", "持っていけ。俺の火の欠片だ。"],
    reward: "悪神ジョブ「鬼神の破戒者」を装備できるようになった！（ジョブ画面）",
  },
  {
    palette: { floor: "#c8b898", wall: "#5a5040", pillar: "#a89878", altar: "#f0e8d0" },
    entrance: { mapId: "sanone-camp", tileX: 8, tileY: 4 },
    entranceText: "風に埋もれた祠が、砂の下から、半分だけ顔をのぞかせている。",
    intro: ["風も、音も、砂も、すべてが止まっている。", "……歌が、あった。誰も知らない、名前のない歌が。", "消えていくものを、ただ、見送るのが、わたしだ。あなたたちは、消えないのか。"],
    lore: "祠の壁は、真っ白に磨かれている。何も刻まれていない。「空白」そのものが、祈りなのかもしれない。",
    defeat: ["……消えない、のですね。あなたたちは、忘れられても、また、歌を紡ぐ。", "その欠片は、わたしが見送ったものの、ひとかけら。持っていってください。"],
    reward: "神にちなんだ最強クラスの装備（仮）。",
  },
  {
    palette: { floor: "#e0e8f0", wall: "#5a6a80", pillar: "#a8b8d0", altar: "#ffffff" },
    entrance: { mapId: "kiri-town", tileX: 9, tileY: 6 },
    entranceText: "巡礼路の奥、霧の濃い場所に、白い石の門が立っている。",
    intro: ["白い霧が、静かに晴れる。清らかな光が、床いっぱいに広がる。", "誓いを、立てにいらしたのですか。それとも、疑いに来たのですか。", "どちらでも構いません。あなたたちの誓いを、見せてください。"],
    lore: "門の柱に、環の紋が彫られている。「誓いは、言葉ではなく、歩みで示すもの」。",
    defeat: ["……確かに、見届けました。あなたたちの誓いは、揺らがない。", "この欠片を、お持ちなさい。環信仰の、源流の光です。"],
    reward: "天神ジョブ「純神の聖騎士」を装備できるようになった！（ジョブ画面）",
  },
  {
    palette: { floor: "#70788a", wall: "#20242e", pillar: "#a0a8b8", altar: "#e0e8f8" },
    entrance: { mapId: "shimohara-facility", tileX: 9, tileY: 6 },
    entranceText: "戦跡の地下、氷に覆われた重い鉄の扉が、雪の下から現れている。",
    intro: ["氷と鉄と、折れた無数の剣。大乱期の戦の記憶が、渦を巻いている。", "勝ち続けて、勝ち続けて、それでも、誰も救えなかった。それが、わたしの咎だ。", "戦いの果てを、あなたたちの手で、見せてくれ。"],
    lore: "折れた剣に、兵士の名が彫られている。「ロウ」「ヒナ」「ゲンゼ」……。名もなき兵士たちの声が、まだここにある。",
    defeat: ["……負けた。ああ、負けるとは、こういうことか。ずっと、これが、欲しかった。", "持っていけ。わたしの、咎の欠片を。"],
    reward: "神にちなんだ最強クラスの装備（仮）。",
  },
  {
    palette: { floor: "#6a6a9a", wall: "#181830", pillar: "#8a8ac0", altar: "#a0f0e8" },
    entrance: { mapId: "fushima-base", tileX: 9, tileY: 6 },
    entranceText: "地図にない、雲の切れ間の浮島へ続く、細い空の橋が、拠点の奥に架かっている。",
    intro: ["ここは、地図の外。境界のない、空の果て。", "……見えているだろう。ずっと、渦の向こうに、何かが、あることを。", "わたしは、それを、見ぬふりをして、生きてきた。あなたたちは、見るか。"],
    lore: "床の模様が、少しずつ、動いている。境目が、あるのか、ないのか、分からない。",
    defeat: ["……見る、のだな。ならば、道を、開こう。渦の向こうに、待つものへ。", "この欠片を。……向こうで、会おう。"],
    reward: "神にちなんだ最強クラスの装備（仮）。",
  },
  {
    palette: { floor: "#404058", wall: "#0c0c18", pillar: "#606080", altar: "#c0c0e0" },
    entrance: { mapId: "toushin-hall", tileX: 9, tileY: 6 },
    entranceText: "議場の奥、合議会の書庫の、さらに奥に、封印された文書の間へ続く鉄の扉がある。",
    intro: ["紙の匂いと、静寂。閉じられた文書の間に、鐘の余韻だけが漂っている。", "……失踪した者たちの、気配が、まだ、ここに触れていく。", "終わりを、見送る者として、あなたたちの終わりを、問おう。"],
    lore: "封印文書の背表紙に、「静まりの年」の文字が並ぶ。開かれることのなかった、名前たちの棚。",
    defeat: ["……終わりを、恐れぬ者たちだ。いや、恐れながら、進む者たちか。", "その欠片を、持っていきなさい。無音の鐘は、もう、鳴らさなくていい。"],
    reward: "神にちなんだ最強クラスの装備（仮）。",
  },
];

const shrineMapId = (no: number): string => `god-shrine-${no}`;

export const CHAPTER11_MAPS: Record<string, TileMapData> = Object.fromEntries(
  SHRINES.map((shrine, i) => [
    shrineMapId(i + 1),
    createShrineData(shrine.palette, {
      mapId: shrine.entrance.mapId,
      tileX: shrine.entrance.tileX,
      tileY: shrine.entrance.tileY + 1,
    }),
  ]),
);

function entranceCommands(no: number, shrine: GodShrine): EventCommand[] {
  const god = GODS[no - 1];
  return [
    {
      type: "if",
      flag: "deep_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: `god${no}_fragment`,
          equals: true,
          then: [say(undefined, `${god.kind}の禁域は静まり、環の欠片はすでに持ち出された。`)],
          else: [
            say(undefined, shrine.entranceText),
            {
              type: "choice",
              text: `${god.kind}の禁域へ入りますか？`,
              options: [
                { label: "入る", commands: [{ type: "warp", mapId: shrineMapId(no), tileX: SHRINE_ENTRY.tileX, tileY: SHRINE_ENTRY.tileY }] },
                { label: "やめておく", commands: [] },
              ],
            },
          ],
        },
      ],
      else: [say(undefined, "古い石の壁だ。何も、特別なものは見当たらない。")],
    },
  ];
}

function godCommands(no: number, shrine: GodShrine): EventCommand[] {
  const god = GODS[no - 1];
  return [
    {
      type: "if",
      flag: `god${no}_defeated`,
      equals: true,
      then: [say(undefined, `${god.kind}「${god.name}」の姿は、もうない。静かな光だけが残っている。`)],
      else: [
        {
          type: "if",
          flag: `god${no}_told`,
          equals: true,
          then: [say(undefined, `${god.kind}が、ふたたび、こちらを向いた。`), { type: "startBattle", battleId: god.id }],
          else: [
            ...shrine.intro.map((t) => say(`${god.kind}「${god.name}」`, t)),
            { type: "setFlag", flag: `god${no}_told`, value: true },
            say(undefined, `${god.kind}との戦いが始まる！`),
            { type: "startBattle", battleId: god.id },
          ],
        },
      ],
    },
  ];
}

function altarCommands(no: number, shrine: GodShrine): EventCommand[] {
  const god = GODS[no - 1];
  return [
    {
      type: "if",
      flag: `god${no}_fragment`,
      equals: true,
      then: [say(undefined, "祭壇は空になっている。環の欠片は、もうここにない。")],
      else: [
        {
          type: "if",
          flag: `god${no}_defeated`,
          equals: true,
          then: [
            ...shrine.defeat.map((t) => say(`${god.kind}「${god.name}」`, t)),
            say(undefined, `環の欠片（${no}つ目）を手に入れた！`),
            { type: "giveGold", amount: 6000 },
            say(undefined, "【ごほうび】灯貨6000を手に入れた！"),
            say(undefined, `【ごほうび】${shrine.reward}`),
            { type: "setFlag", flag: `god${no}_fragment`, value: true },
          ],
          else: [say(undefined, "祭壇の上で、環の欠片が淡く光っている。だが、神が守っていて、近づけない。")],
        },
      ],
    },
  ];
}

export const CHAPTER11_NPCS: Record<string, Npc[]> = (() => {
  const result: Record<string, Npc[]> = {};
  const add = (mapId: string, npc: Npc): void => {
    (result[mapId] ??= []).push(npc);
  };
  SHRINES.forEach((shrine, i) => {
    const no = i + 1;
    add(shrine.entrance.mapId, {
      id: `god-${no}-entrance`,
      tileX: shrine.entrance.tileX,
      tileY: shrine.entrance.tileY,
      color: shrine.palette.altar,
      commands: entranceCommands(no, shrine),
    });
    add(shrineMapId(no), { id: `god-${no}-boss`, ...SHRINE_LANDMARKS.god, color: shrine.palette.pillar, commands: godCommands(no, shrine) });
    add(shrineMapId(no), { id: `god-${no}-altar`, ...SHRINE_LANDMARKS.altar, tileY: SHRINE_LANDMARKS.altar.tileY + 0, color: shrine.palette.altar, commands: altarCommands(no, shrine) });
    add(shrineMapId(no), { id: `god-${no}-lore`, ...SHRINE_LANDMARKS.lore, color: "#909090", commands: [say(undefined, shrine.lore)] });
  });
  return result;
})();
