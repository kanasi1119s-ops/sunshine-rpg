import type { Combatant } from "../battle/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";
import { placeName } from "../save/slots";
import type { QuestEntry } from "./side-quest-log";
import { say } from "./side-story";

/**
 * 禁域の鍵（2026-10-06、人間の指示「禁域に入るための条件がさらにあるといいかも」→ 案A「禁域ごとに鍵を集める」、
 * 「頼みごとの難易度を高くしよう」）。
 * 8神の禁域の扉は、初源の歪みを倒しただけでは開かない。その土地の依頼人から頼みごとを受け、地方の奥にいる
 * 「試練の番人」2体（どちらも8神に近い強さ。2体目は1体目を倒したあとでないと挑めない）を倒して報告すると、鍵がもらえる。
 * フラグ: `god<N>_key_accepted`（受けた）→ `god<N>_trial1_defeated` → `god<N>_trial2_defeated` → `god<N>_key`（鍵）。
 * 番人の絵は図形（仮）。
 */
export interface ShrineKey {
  /** 8神の番号（1〜8）。 */
  no: number;
  keyName: string;
  giver: { name: string; mapId: string; tileX: number; tileY: number; color: string };
  offer: string[];
  hint: string;
  complete: string[];
  after: string;
  trials: [ShrineTrial, ShrineTrial];
}

export interface ShrineTrial {
  name: string;
  mapId: string;
  tileX: number;
  tileY: number;
  /** 番人の前に立ったときの一文。 */
  intro: string;
}

export const SHRINE_KEYS: ShrineKey[] = [
  {
    no: 1,
    keyName: "泉守りの鍵石",
    giver: { name: "水番のセツ", mapId: "mugikano-village", tileX: 17, tileY: 6, color: "#7aa0c0" },
    offer: [
      "水源の奥の、ひび割れた石扉。あれを開ける鍵石は、代々、水番の家が預かってきたんだよ。",
      "けれどね、鍵石は、試しを越えた者にしか渡しちゃいけない決まりなんだ。水路と隧道の奥に、古い番人が二つ、眠っている。",
      "どちらも、並の歪みとは格がちがう。……それでも行くかい？",
    ],
    hint: "水路の奥と、隧道の奥。番人は、水の止まった場所を守っているよ。",
    complete: ["……本当に、二つとも鎮めてきたのかい。水の音が、昔の高さにもどった気がするよ。", "鍵石を、持っておいき。恵みは、返すもの。忘れるんじゃないよ。"],
    after: "水が、よく流れてるだろう？ あんたたちのおかげさ。",
    trials: [
      { name: "涸れ穂の番人", mapId: "mugikano-canal", tileX: 1, tileY: 18, intro: "枯れた麦穂を束ねたような影が、水路の行き止まりで、ゆっくりと立ち上がった。" },
      { name: "逆さ水の番人", mapId: "mugikano-tunnel", tileX: 39, tileY: 5, intro: "天井から、水が、下から上へと流れている。その流れの中心で、何かが目を開いた。" },
    ],
  },
  {
    no: 2,
    keyName: "葦笛の鍵",
    giver: { name: "葦刈りのトモエ", mapId: "garasuko-town", tileX: 19, tileY: 8, color: "#8aa070" },
    offer: [
      "倉庫の奥の葦原の通路……あそこは、葦笛を吹かないと、扉が開かないんだ。笛は、うちの家に伝わってる。",
      "でも、笛を鳴らせる人は、湖の洞窟の主を二つ、鎮めた人だけ。ばあちゃんが、そう言ってた。",
      "一つ目は洞窟の浅いところ、二つ目は、いちばん深いところ。……どっちも、帰ってこなかった人がいるよ。",
    ],
    hint: "湖の洞窟。浅いほうと、深いほう。羽音が大きくなるほうへ。",
    complete: ["ほんとに……！ 洞窟の羽音が、ぴたりとやんだって、漁師さんたちが騒いでたよ。", "葦笛、持ってって。吹くときは、怖がらないで。息を、まっすぐにね。"],
    after: "湖の朝が、静かになったよ。ありがとう。",
    trials: [
      { name: "湖底の殻もぐり", mapId: "garasuko-cave-1", tileX: 27, tileY: 1, intro: "固い殻をまとった大きな影が、水たまりから、ぬるりと這い出してきた。" },
      { name: "千羽の葦影", mapId: "garasuko-cave-2", tileX: 35, tileY: 13, intro: "無数の羽音が、一つの形に寄り集まっていく。葦の影が、人の背丈の三倍にふくらんだ。" },
    ],
  },
  {
    no: 3,
    keyName: "焼き入れの鉄符",
    giver: { name: "老鍛冶のゲンタ", mapId: "tetsukusari-town", tileX: 19, tileY: 6, color: "#a07050" },
    offer: [
      "坑道の底の、焼けただれた扉か。あれは、わしの師匠の、そのまた師匠が打った扉だ。鉄符がなけりゃ、びくともせん。",
      "鉄符は、焼きを入れなおさにゃ使えん。焼き入れに要るのは、洞窟の奥の火の番人どもの、火の芯だ。二つな。",
      "あいつらは、組合の若い衆が束になっても歯が立たなかった。……覚悟はあるか。",
    ],
    hint: "鉱山の洞窟、手前と奥。熱いほうへ、熱いほうへ進め。",
    complete: ["……火の芯が、二つ。本当に取ってきやがったか。よし、焼きを入れるぞ。", "ほれ、鉄符だ。まだ熱い。……お前らの筋は、通ってる。"],
    after: "槌の音が、今日はよく響くわい。",
    trials: [
      { name: "赤熱の岩喰い", mapId: "tetsukusari-cave-1", tileX: 8, tileY: 34, intro: "赤く焼けた岩が、ばりばりと音を立てて、ひとりでに転がりはじめた。" },
      { name: "炉心の大槌兵", mapId: "tetsukusari-cave-2", tileX: 1, tileY: 8, intro: "溶けた鉄の中から、大槌をかついだ巨きな影が、ゆっくりと身を起こした。" },
    ],
  },
  {
    no: 4,
    keyName: "無銘の砂時計",
    giver: { name: "語り部のサラ", mapId: "sanone-town", tileX: 15, tileY: 8, color: "#c0a878" },
    offer: [
      "砂に埋もれた祠の扉は、砂時計をひっくり返したときにだけ、開くのよ。名前のない、古い砂時計。",
      "でもその砂は、遺跡の奥の二つの影に、吸い取られてしまったの。歌を食べる影と、歌そのものを消す嵐。",
      "わたしの声では、届かなかった。……あなたたちの足なら、届くかしら。",
    ],
    hint: "砂の遺跡の、上の層と、下の層。歌の消えたほうへ。",
    complete: ["……砂が、もどってきた。さらさら、さらさら。ああ、この音、歌みたい。", "砂時計を。ひっくり返すときは、何か、好きな歌を口ずさんでね。"],
    after: "今日は、新しい歌を一つ、思いついたの。",
    trials: [
      { name: "砂に溶けた影", mapId: "sanone-ruins-1", tileX: 33, tileY: 21, intro: "足もとの砂が、人の形に盛り上がった。顔のない影が、こちらを見ている。" },
      { name: "歌を喰う砂嵐", mapId: "sanone-ruins-2", tileX: 43, tileY: 10, intro: "風がやんだ。次の瞬間、音という音が、渦の中へ吸いこまれていった。" },
    ],
  },
  {
    no: 5,
    keyName: "白霧の誓い札",
    giver: { name: "老巡礼のイオリ", mapId: "kiri-town", tileX: 19, tileY: 10, color: "#d0d8e8" },
    offer: [
      "巡礼路の奥の白い門。あそこをくぐれるのは、誓い札を持つ者だけです。札は、塔の頂で、誓いを立てた者に授けられる。",
      "けれど今、塔には、誓いを忘れた番人が二つ、居座っております。鐘を守る者と、祈りを忘れた像。",
      "わたしは足が弱って、もう塔を登れません。……代わりに、登っていただけませんか。",
    ],
    hint: "霧の塔の、下の階と、上の階。鐘の音のするほうへ。",
    complete: ["……鐘が、鳴りました。二十年ぶりに、ほんとうの音で。", "誓い札を、お受け取りください。誓いは言葉でなく、歩みで示すもの。あなたたちは、もう、示しました。"],
    after: "朝の鐘が、よく聞こえるようになりました。",
    trials: [
      { name: "霧鐘の守り手", mapId: "kiri-tower-1", tileX: 15, tileY: 5, intro: "霧の中から、ひびの入った大きな鐘を背負った影が現れた。鐘が、低く、うなる。" },
      { name: "祈りを忘れた像", mapId: "kiri-tower-2", tileX: 33, tileY: 1, intro: "手を組んだ石の像が、ぎしり、と首をこちらへ向けた。その手は、もう祈っていない。" },
    ],
  },
  {
    no: 6,
    keyName: "折れ剣の鍔",
    giver: { name: "元兵士のガロウ", mapId: "shimohara-town", tileX: 18, tileY: 9, color: "#8a98a8" },
    offer: [
      "戦跡の地下の、氷の鉄扉か。あれには、鍵穴がない。……代わりに、鍔をはめるくぼみがある。",
      "大乱期の将の、折れ剣の鍔だ。鍔は今、戦跡の奥で、凍った軍旗と、剣の群れに守られている。",
      "わしの隊は、そこで、半分が戻らなかった。……すまん。若い者に頼むことじゃないのは、分かっとる。",
    ],
    hint: "雪の戦跡、外の層と、奥の層。旗の立つほうへ。",
    complete: ["……鍔だ。あの日、将が握っていた、そのものだ。", "持っていってくれ。わしの隊の、帰れなかった連中の分まで。……ありがとう。"],
    after: "今朝は、久しぶりに、ぐっすり眠れた。",
    trials: [
      { name: "凍てついた軍旗", mapId: "shimohara-ruins-1", tileX: 25, tileY: 26, intro: "氷に閉じこめられた軍旗が、風もないのに、ばさりとはためいた。" },
      { name: "千本剣の亡霊", mapId: "shimohara-ruins-2", tileX: 7, tileY: 18, intro: "地面に突き立った無数の剣が、一斉に抜け、ひとつの影の背に集まっていく。" },
    ],
  },
  {
    no: 7,
    keyName: "境見の羅針",
    giver: { name: "雲読みのシズク", mapId: "fushima-town", tileX: 22, tileY: 8, color: "#9090c8" },
    offer: [
      "拠点の奥の空の橋は、羅針がないと、渡るそばから消えてしまうの。地図の外へ行く針、境見の羅針。",
      "羅針の針は、雲の塔の奥にいる二つのものが、飲みこんでしまったわ。迷子の大きな鯨と、境目をはう影。",
      "わたしの雲読みでは、帰ってこられる見こみは、三割。……それでも、行く？",
    ],
    hint: "雲の塔の、下と上。雲が渦を巻くほうへ。",
    complete: ["針が、もどった……。北でも南でもない方角を、まっすぐ指してる。", "羅針を、あげる。迷ったら、針じゃなくて、隣の人の顔を見るのよ。"],
    after: "雲の流れが、素直になったわ。",
    trials: [
      { name: "雲間の迷い鯨", mapId: "fushima-tower-1", tileX: 43, tileY: 14, intro: "雲の床が大きく波打ち、山のように大きな背が、ぬうっと浮かびあがった。" },
      { name: "境目をはう影", mapId: "fushima-tower-2", tileX: 7, tileY: 30, intro: "床の模様の境目から、平たい影がはがれ、立ち上がった。どこまでが床で、どこからが影なのか、分からない。" },
    ],
  },
  {
    no: 8,
    keyName: "封印文書の鍵",
    giver: { name: "書庫番のフミ", mapId: "toushin-town", tileX: 20, tileY: 8, color: "#606080" },
    offer: [
      "合議会の書庫の、いちばん奥の鉄扉。あの鍵は、書庫番が代々、塔の上の書見台に封じてきました。",
      "けれど、塔には今、頁を閉ざす者と、名を喰う鐘がおります。静まりの年に、名前を消された人たちの気配を、吸って育ったものです。",
      "議長からも、行かせるなと言われています。……それでも、あなたたちなら、と、わたしは思ってしまう。",
    ],
    hint: "都の塔の、下の階と、上の階。紙のめくれる音のするほうへ。",
    complete: ["……書見台の封が、解けました。鍵が、ここに。", "お持ちください。開かれなかった名前たちの棚を、どうか、見てきてください。"],
    after: "書庫に、風を通しました。紙が、よろこんでいる気がします。",
    trials: [
      { name: "頁を閉ざす者", mapId: "toushin-tower-1", tileX: 27, tileY: 26, intro: "無数の紙が舞い上がり、人の形に重なった。その顔には、何も書かれていない。" },
      { name: "名を喰う鐘", mapId: "toushin-tower-2", tileX: 17, tileY: 1, intro: "鐘が、音もなく揺れた。耳の奥で、誰かの名前が、ひとつ、消えた気がした。" },
    ],
  },
];

export const keyFlag = (no: number): string => `god${no}_key`;
export const keyAcceptedFlag = (no: number): string => `god${no}_key_accepted`;
export const trialFlag = (no: number, k: 1 | 2): string => `god${no}_trial${k}_defeated`;
export const trialBattleId = (no: number, k: 1 | 2): string => `shrine-trial-${no}-${k}`;

/**
 * 試練の番人の強さ。8神（HP約6400・攻撃100）に近い強さにし、2体目・後の番号ほど強い（人間の指示「難易度を高くしよう」）。
 * 1体目と2体目のあいだで宿に戻れるので、2体を合わせて、神1体より少し重いくらいの手ごたえ。
 */
export function trialStats(no: number, k: 1 | 2): { maxHp: number; attack: number; defense: number; speed: number; expReward: number } {
  return k === 1
    ? { maxHp: 5000 + 150 * no, attack: 94 + no, defense: 32, speed: 27, expReward: 8000 + 200 * no }
    : { maxHp: 5800 + 180 * no, attack: 100 + no, defense: 33 + (no > 4 ? 1 : 0), speed: 29, expReward: 9500 + 250 * no };
}

export function createTrialEnemy(no: number, k: 1 | 2): Combatant {
  const key = SHRINE_KEYS[no - 1];
  const s = trialStats(no, k);
  return { id: trialBattleId(no, k), name: key.trials[k - 1].name, hp: s.maxHp, maxMp: 0, mp: 0, isEnemy: true, guarding: false, ...s };
}

/** 依頼人の会話（受ける前 → 受けた（すすみ具合）→ 報告して鍵 → そのあと）。 */
function giverCommands(key: ShrineKey): EventCommand[] {
  const who = key.giver.name;
  const t1 = trialFlag(key.no, 1);
  const t2 = trialFlag(key.no, 2);
  return [
    {
      type: "if",
      flag: keyFlag(key.no),
      equals: true,
      then: [say(who, key.after)],
      else: [
        {
          type: "if",
          flag: keyAcceptedFlag(key.no),
          equals: true,
          then: [
            {
              type: "if",
              flag: t2,
              equals: true,
              then: [
                ...key.complete.map((t) => say(who, t)),
                say(undefined, `「${key.keyName}」を手に入れた！ 禁域の扉が、開くようになった。`),
                { type: "setFlag", flag: keyFlag(key.no), value: true },
              ],
              else: [
                say(who, key.hint),
                {
                  type: "if",
                  flag: t1,
                  equals: true,
                  then: [say(undefined, `（試練の番人: 1体目「${key.trials[0].name}」を倒した。のこりは「${key.trials[1].name}」）`)],
                  else: [say(undefined, `（試練の番人: まず「${key.trials[0].name}」、つぎに「${key.trials[1].name}」）`)],
                },
              ],
            },
          ],
          else: [
            ...key.offer.map((t) => say(who, t)),
            {
              type: "choice",
              text: `「${key.keyName}」のための試練を受けますか？`,
              options: [
                {
                  label: "受ける",
                  commands: [
                    { type: "setFlag", flag: keyAcceptedFlag(key.no), value: true },
                    say(who, key.hint),
                    say(undefined, "（とても強い相手です。じゅうぶんに育ててから、挑みましょう）"),
                  ],
                },
                { label: "やめておく", commands: [say(who, "無理はしないことだよ。気が向いたら、また来ておくれ。")] },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function trialCommands(key: ShrineKey, k: 1 | 2): EventCommand[] {
  const trial = key.trials[k - 1];
  const fight: EventCommand[] = [
    say(undefined, trial.intro),
    {
      type: "choice",
      text: `「${trial.name}」と戦いますか？`,
      options: [
        { label: "戦う", commands: [{ type: "startBattle", battleId: trialBattleId(key.no, k) }] },
        { label: "やめておく", commands: [] },
      ],
    },
  ];
  if (k === 1) return fight;
  return [
    {
      type: "if",
      flag: trialFlag(key.no, 1),
      equals: true,
      then: fight,
      else: [say(undefined, `重い気配が、行く手をふさいでいる。……先に「${key.trials[0].name}」を鎮めないと、近づけないようだ。`)],
    },
  ];
}

export const SHRINE_KEY_NPCS: Record<string, Npc[]> = (() => {
  const result: Record<string, Npc[]> = {};
  const add = (mapId: string, npc: Npc): void => {
    (result[mapId] ??= []).push(npc);
  };
  for (const key of SHRINE_KEYS) {
    add(key.giver.mapId, {
      id: `god-${key.no}-key-giver`,
      tileX: key.giver.tileX,
      tileY: key.giver.tileY,
      color: key.giver.color,
      showWhenFlag: "deep_yugami_defeated",
      commands: giverCommands(key),
    });
    for (const k of [1, 2] as const) {
      const trial = key.trials[k - 1];
      add(trial.mapId, {
        id: `god-${key.no}-trial-${k}`,
        tileX: trial.tileX,
        tileY: trial.tileY,
        color: "#5a3a6a",
        showWhenFlag: keyAcceptedFlag(key.no),
        hideWhenFlag: trialFlag(key.no, k),
        commands: trialCommands(key, k),
      });
    }
  }
  return result;
})();

/** 禁域の扉の前で、鍵がないときの会話。 */
export function lockedDoorCommands(no: number): EventCommand[] {
  const key = SHRINE_KEYS[no - 1];
  return [
    say(undefined, `扉には、封印の紋が刻まれている。「${key.keyName}」がなければ、開きそうにない。`),
    say(undefined, `（${placeName(key.giver.mapId)}の「${key.giver.name}」が、何か知っているらしい）`),
  ];
}

/** 「依頼の記録」に出す、禁域の鍵の頼みごと（初源の歪みを倒したあと）。 */
export function shrineKeyQuestLog(flags: Record<string, boolean | undefined>): QuestEntry[] {
  if (!flags["deep_yugami_defeated"]) return [];
  return SHRINE_KEYS.map((key): QuestEntry => {
    const done = flags[keyFlag(key.no)] === true;
    const accepted = flags[keyAcceptedFlag(key.no)] === true;
    const steps = [1, 2].filter((k) => flags[trialFlag(key.no, k as 1 | 2)] === true).length;
    const status = done ? "done" : accepted ? (steps >= 2 ? "report" : "progress") : "available";
    const nextTrial = key.trials[steps];
    return {
      id: `禁域${key.no}`,
      title: `禁域の鍵「${key.keyName}」`,
      status,
      giver: key.giver.name,
      place: placeName(key.giver.mapId),
      stepsDone: steps,
      stepsTotal: 2,
      ...(status === "progress" ? { hint: key.hint, next: nextTrial ? placeName(nextTrial.mapId) : undefined } : {}),
    };
  });
}
