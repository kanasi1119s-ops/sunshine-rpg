import {
  createMugikanoVillageData,
  MUGIKANO_VILLAGE_LANDMARKS,
} from "../map/chapter1/mugikano-village";
import {
  createMugikanoWaterSourceData,
  MUGIKANO_WATER_SOURCE_LANDMARKS,
} from "../map/chapter1/mugikano-water-source";
import {
  createMugikanoCanalData,
  createMugikanoTunnelData,
  MUGIKANO_CANAL_LANDMARKS,
  MUGIKANO_TUNNEL_LANDMARKS,
} from "../map/chapter1/mugikano-dungeon";
import { chestNpc, leverNpc, loreNpc } from "./dungeon-objects";
import type { TileMapData } from "../map/types";
import type { EventCommand } from "../event/types";
import type { Npc } from "../npc";

/**
 * 第1章（麦香野）の世界。`docs/story/structure.md`「第1章（麦香野）」・
 * `docs/story/mystery.md`（真相）・`docs/story/clue-ledger.md`（伏線 C-002）を反映。
 */
export const CHAPTER1_MAPS: Record<string, TileMapData> = {
  "mugikano-village": createMugikanoVillageData(),
  "mugikano-canal": createMugikanoCanalData(),
  "mugikano-tunnel": createMugikanoTunnelData(),
  "mugikano-water-source": createMugikanoWaterSourceData(),
};

/**
 * 麦香野へ到着したとき、一度だけ流す短い場面つなぎ（`chapter1_intro_seen` フラグで管理）。
 */
export const CHAPTER1_OPENING_COMMANDS: EventCommand[] = [
  { type: "message", text: "――灯里から東の街道を歩いて、丸二日。麦香野。" },
  {
    type: "message",
    text: "灯里支部に届いた「水路の水が涸れた。至急、調査員を求む」という依頼を受けて、ユーリとレトは村へ向かった。",
  },
  { type: "message", text: "風の中に、熟れかけた麦の、香ばしい匂いがまじっている。" },
  { type: "message", text: "麦香野には、ガキの頃に一回だけ来たことがある。兄貴に連れられて、手紙を届けにな。", speaker: "レト" },
  {
    type: "message",
    text: "……水路が、光っていない。灯り石を含んだ水が流れていれば、晴れた日は淡い青にきらめくはずなのに。",
  },
  {
    type: "message",
    text: "村に着くと、声をひそめた村人たちが、井戸のまわりに集まっていた。いちばん大きな音――水車の音が、していない。",
  },
  { type: "setFlag", flag: "chapter1_intro_seen", value: true },
];

export const CHAPTER1_NPCS: Record<string, Npc[]> = {
  "mugikano-village": [
    {
      id: "mugikano-elder",
      tileX: MUGIKANO_VILLAGE_LANDMARKS.elder.tileX,
      tileY: MUGIKANO_VILLAGE_LANDMARKS.elder.tileY,
      color: "#8a7a4a",
      commands: elderCommands(),
    },
    {
      id: "mugikano-miller",
      tileX: 15,
      tileY: 6,
      color: "#c0a878",
      commands: millerCommands(),
    },
    {
      id: "mugikano-mina",
      tileX: MUGIKANO_VILLAGE_LANDMARKS.mina.tileX,
      tileY: MUGIKANO_VILLAGE_LANDMARKS.mina.tileY,
      color: "#5a9ac9",
      spriteName: "ミナ",
      commands: minaCommands(),
    },
  ],
  "mugikano-canal": [
    {
      id: "mugikano-canal-farmer",
      tileX: MUGIKANO_CANAL_LANDMARKS.farmer.tileX,
      tileY: MUGIKANO_CANAL_LANDMARKS.farmer.tileY,
      color: "#a0b070",
      commands: [
        { type: "message", text: "水が来なくなって、畑がひび割れてきたよ。この水路は、北の水源からずっと引いているんだ。", speaker: "農夫" },
        { type: "message", text: "水がないのを誰のせいにするかで、村じゅう揉めとる。誰も悪い人じゃないんだがなあ。", speaker: "農夫" },
        {
          type: "message",
          text: "水源へ行く坑道の扉は、鍵がかかってる。鍵は、北の畑の見張り小屋に置いてあったはずだ。小屋の箱を探してごらん。",
          speaker: "農夫",
        },
        { type: "message", text: "それと、坑道の中は暗くて湿っている。獣も出るから、気をつけてな。", speaker: "農夫" },
      ],
    },
    {
      id: "mugikano-canal-watchman",
      tileX: MUGIKANO_CANAL_LANDMARKS.watchman.tileX,
      tileY: MUGIKANO_CANAL_LANDMARKS.watchman.tileY,
      color: "#8a9ab0",
      commands: [
        { type: "message", text: "見張り小屋の番をしている者だ。水が止まってから、毎日この水路を見て回っている。", speaker: "水路の見張り" },
        {
          type: "message",
          text: "水が止まる前の晩、水源の方角から、ごうんと地面が揺れるような音がした。あれは、ただの雷じゃなかった。",
          speaker: "水路の見張り",
        },
        { type: "message", text: "水源の坑道には、水を止める古いバルブが、左右の部屋にあるはずだ。水を抜けば、奥の岩戸が開く。", speaker: "水路の見張り" },
      ],
    },
    chestNpc("mugikano-canal-chest-gold", MUGIKANO_CANAL_LANDMARKS.chestGold, "chapter1_chest_canal_gold", { gold: 70 }, "畑のすみの宝箱を開けた！"),
    {
      id: "mugikano-canal-chest-key",
      openedFlag: "chapter1_got_key",
      tileX: MUGIKANO_CANAL_LANDMARKS.chestKey.tileX,
      tileY: MUGIKANO_CANAL_LANDMARKS.chestKey.tileY,
      color: "#e8c860",
      commands: [
        {
          type: "if",
          flag: "chapter1_got_key",
          equals: true,
          then: [{ type: "message", text: "見張り小屋の箱は、もう空だ。" }],
          else: [
            { type: "message", text: "見張り小屋の古い箱を開けた。中には、錆びた鍵が入っている。" },
            { type: "message", text: "【だいじなもの】坑道の鍵を手に入れた！" },
            { type: "setFlag", flag: "chapter1_got_key", value: true },
          ],
        },
      ],
    },
    loreNpc("mugikano-canal-lore-sluice", MUGIKANO_CANAL_LANDMARKS.sluiceStone, [
      "水路の石組みに、古い刻みがある。「水は北の坑より来たり。坑の戸は、ふたつの弁にて開く」",
      "昔の人が、この水路と坑道を一緒に作ったのだろう。",
    ]),
  ],
  "mugikano-tunnel": [
    leverNpc("mugikano-tunnel-panel-west", MUGIKANO_TUNNEL_LANDMARKS.valveWest, "chapter1_valve_west", "chapter1_valve_east", "chapter1_valves_open", {
      pull: "西の赤い台のバルブを、力いっぱい回す。ごぼごぼと水が抜ける音がした。",
      already: "西のバルブは、もう回してある。",
      opened: "東のバルブも回してある。坑道の水が一気に引き、奥で、岩戸の動く音がした！",
      waiting: "水の抜ける音がするが、まだ足りない。反対側にも、同じバルブがあるはずだ。",
    }),
    leverNpc("mugikano-tunnel-panel-east", MUGIKANO_TUNNEL_LANDMARKS.valveEast, "chapter1_valve_east", "chapter1_valve_west", "chapter1_valves_open", {
      pull: "東の赤い台のバルブを、力いっぱい回す。ごぼごぼと水が抜ける音がした。",
      already: "東のバルブは、もう回してある。",
      opened: "西のバルブも回してある。坑道の水が一気に引き、奥で、岩戸の動く音がした！",
      waiting: "水の抜ける音がするが、まだ足りない。反対側にも、同じバルブがあるはずだ。",
    }),
    chestNpc("mugikano-tunnel-chest-deep", MUGIKANO_TUNNEL_LANDMARKS.chest, "chapter1_chest_tunnel", { gold: 90, equipmentId: "treasure-10" }, "坑道のくぼみの宝箱を開けた！"),
    loreNpc("mugikano-tunnel-lore-wall", MUGIKANO_TUNNEL_LANDMARKS.wallMark, [
      "坑道の壁に、同じ間隔で刻まれた掘り跡がある。",
      "自然にできた洞穴ではない。人の手で、きちんと掘り進められた跡だ。",
      "ずいぶん古いはずなのに、刃の跡が妙に新しく見える……。",
    ]),
  ],
  "mugikano-water-source": [
    {
      id: "mugikano-excavation-mark",
      tileX: MUGIKANO_WATER_SOURCE_LANDMARKS.excavationMark.tileX,
      tileY: MUGIKANO_WATER_SOURCE_LANDMARKS.excavationMark.tileY,
      color: "#8a7a5a",
      commands: excavationMarkCommands(),
    },
    {
      id: "mugikano-yugami",
      tileX: MUGIKANO_WATER_SOURCE_LANDMARKS.yugami.tileX,
      tileY: MUGIKANO_WATER_SOURCE_LANDMARKS.yugami.tileY,
      color: "#8a4fd6",
      commands: mugikanoYugamiCommands(),
    },
  ],
};

function elderCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_yugami_defeated",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter1_reported_to_elder",
          equals: true,
          then: [
            {
              type: "message",
              text: "水路の水も戻って、村もようやく落ち着いたよ。ありがとうな、ユーリ殿、レト殿。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "番水帳には、新しい頁を足すことにした。水が少ないとき、来ないときの決まりをな。水があるうちに、皆で話しあえる。",
              speaker: "村長",
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter1_excavation_found",
              equals: true,
              then: [
                { type: "message", text: "戻ったか。水源はどうだった？", speaker: "村長" },
                {
                  type: "message",
                  text: "泉の奥の、古い採掘跡の坑道に、灯り石を使った輪のような装置がありました。それが歪みの根でした。",
                  speaker: "ユーリ",
                },
                { type: "message", text: "……採掘跡？　あの山に、灯り石の坑道があったのか。", speaker: "村長" },
                {
                  type: "message",
                  text: "わしの祖父が、「北の山に、掘り終わった穴がある」と言っていた覚えはある。それが、あれか。",
                  speaker: "村長",
                },
                {
                  type: "message",
                  text: "灯里の町外れで見た焼け跡と、似た感じがするんです。あそこも、歪みが起きた場所でした。古い坑口もありました。",
                  speaker: "ユーリ",
                },
                {
                  type: "message",
                  text: "歪みが出る場所には、決まって古い灯り石の採掘跡がある……そういうことか？",
                  speaker: "レト",
                },
                {
                  type: "message",
                  text: "偶然、では片付けられなさそうだな。カセンさんにも報告しておいた方がいい。",
                  speaker: "レト",
                },
                { type: "setFlag", flag: "chapter1_clue_c002_found", value: true },
                {
                  type: "message",
                  text: "村長。山や村の周りで、また変わったことがあったら、すぐ灯里の支部に知らせてください。",
                  speaker: "レト",
                },
                { type: "message", text: "分かった。必ず。", speaker: "村長" },
                {
                  type: "message",
                  text: "それと、さっきの寄り合いのことじゃが。シンが、みんなの前で詫びたよ。",
                  speaker: "村長",
                },
                {
                  type: "message",
                  text: "浚渫で輪を掘り出したが、怖くなって、夜のうちにひとりで埋めなおした、とな。",
                  speaker: "村長",
                },
                {
                  type: "message",
                  text: "するとゴンザが言った。「あの輪を、村の皆が触っていたら、どうなった」と。「ひとりで抱えるな。皆で、泥をかぶれ」とな。",
                  speaker: "村長",
                },
                {
                  type: "message",
                  text: "あの二人も、少しずつ変わってきたようじゃ。人は、怒る。争う。間違える。じゃが、また立ち上がる。",
                  speaker: "村長",
                },
                {
                  type: "message",
                  text: "とにかく、水路の水が戻ってくれて助かったよ。この十日あまりで、はじめて芯から眠れそうだ。本当にありがとう。",
                  speaker: "村長",
                },
                { type: "setFlag", flag: "chapter1_reported_to_elder", value: true },
              ],
              else: [
                { type: "message", text: "戻ったか。水源はどうだった？", speaker: "村長" },
                {
                  type: "message",
                  text: "しずめてきましたが……もう一度、水源の奥をよく見てみようと思います。",
                  speaker: "ユーリ",
                },
              ],
            },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter1_quest_accepted",
          equals: true,
          then: [
            {
              type: "message",
              text: "北の水源、頼んだよ。わしは足が悪うて、あの山道はもう登れん。危ないと思ったら、決して無理はしないでおくれ。",
              speaker: "村長",
            },
          ],
          else: [
            { type: "message", text: "灯りの相談所の人たちかい。よう来てくださった。村長のヨサクです。", speaker: "村長" },
            {
              type: "message",
              text: "九日前の朝、水路の水が、一夜にして止まった。前の晩まで、うるさいくらい流れとったのに。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "水車小屋の水も止まって、みんな気が立っておる。上手の田のゴンザと、下手の田のタヘイは、言い争いが絶えん。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "麦の刈り入れは、あと十日ほどじゃ。刈った麦は水車で挽く。水が来んと、パンにも粥にもならん。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "村の水は、北の山ぎわの「灯の泉」から引いておる。大昔から、絶えたことのない湧き水じゃ。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "実はな、ひと月ほど前、若い衆のシンが、泉の取水口のあたりを浚渫した。泥をさらう仕事じゃ。そのあと十日ほどで、水が止まった。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "村の中には、シンのせいだと言う者もおる。……あれは、わしが許した仕事じゃ。責めは、わしが負うべきなんじゃが。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "歪みというのは、灯り石の力が乱れて形を持ったもの。放っておけば、水源そのものが駄目になってしまう。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "水源の様子を見てきてほしい。北の道を行った先だ。もし歪みがいたら、しずめてもらえると助かる。",
              speaker: "村長",
            },
            {
              type: "message",
              text: "それと、水が涸れた原因になりそうなものがないか、よく見てきておくれ。",
              speaker: "村長",
            },
            {
              type: "choice",
              text: "依頼を受けますか？",
              options: [
                {
                  label: "受けます",
                  commands: [
                    { type: "setFlag", flag: "chapter1_quest_accepted", value: true },
                    { type: "message", text: "わかりました。まず、いちばん最初から話を聞かせてください。見てきます。", speaker: "ユーリ" },
                    {
                      type: "message",
                      text: "頼む。……ああ、それと、ミナという村の子が、水路のことなら誰より詳しい。自分も行きたがっていてな。",
                      speaker: "村長",
                    },
                    { type: "message", text: "危ないから止めてはいるんだが、話だけでも聞いてやってくれないか。", speaker: "村長" },
                  ],
                },
                {
                  label: "少し考えます",
                  commands: [
                    {
                      type: "message",
                      text: "そうか……。でも、あまり長くは待てそうにないんだ。頼むよ。",
                      speaker: "村長",
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

function minaCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_mina_joined",
      equals: true,
      then: [
        {
          type: "if",
          flag: "chapter1_mina_friend_hint_seen",
          equals: true,
          then: [
            {
              type: "message",
              text: "次はどこに行きましょうか。わたしも、できる限りお手伝いします。",
              speaker: "ミナ",
            },
          ],
          else: [
            { type: "message", text: "水源が元に戻って、本当によかったです。", speaker: "ミナ" },
            { type: "message", text: "……あの、歪みって、人を襲うことも、あるんですよね。", speaker: "ミナ" },
            { type: "message", text: "え、ええ。今回は、幸い誰も襲われていませんでしたが……", speaker: "ユーリ" },
            { type: "message", text: "そう、ですよね。……すみません、変なことを聞いて。", speaker: "ミナ" },
            {
              type: "message",
              text: "（ミナは、一瞬だけ表情を曇らせた。……その目の奥に、暗い光が見えた気がした）",
            },
            { type: "message", text: "……ユーリ。あの子は、まだ本当のことを言ってない。", speaker: "レト" },
            { type: "message", text: "分かってます。話してくれるまで、待ちます。", speaker: "ユーリ" },
            { type: "message", text: "……そうか。お前、先輩に向いてるよ。人が黙ってることを、待てる奴は貴重なんだ。", speaker: "レト" },
            {
              type: "message",
              text: "……いえ、なんでもないです！　それより、次はどこに向かうんですか？",
              speaker: "ミナ",
            },
            { type: "setFlag", flag: "chapter1_mina_friend_hint_seen", value: true },
          ],
        },
      ],
      else: [
        {
          type: "if",
          flag: "chapter1_reported_to_elder",
          equals: true,
          then: [
            { type: "message", text: "ユーリ。……あの、お願いがあるんです。", speaker: "ミナ" },
            {
              type: "message",
              text: "水は、戻りました。でも、まだ終わってない気がするんです。あの輪は、誰かがずっと前から置いていたものなんですよね。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "もし、ほかの場所にも同じものが埋まっていたら。……放っておきたくないんです。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "水紋系の術が使えます。水路のことも、薬草のことも、少しなら分かります。足手まといには、ならないようにします。",
              speaker: "ミナ",
            },
            { type: "message", text: "歪みのこと、もっと知りたいんです。", speaker: "ミナ" },
            {
              type: "message",
              text: "……ミナ。ひとつ、聞いてもいい？　水源へ行く道で、石橋の前を通るとき、きみは目をそらしていたよね。",
              speaker: "ユーリ",
            },
            { type: "message", text: "……気づいて、いたんですね。", speaker: "ミナ" },
            {
              type: "message",
              text: "ハルという、幼なじみがいたんです。隣の家の男の子で、生まれた日が、三日しか違わなくて。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "わたしのほうが、三日だけお姉さんでした。灯り石が大好きで、泉の岩場で拾った水色の欠片を、宝物にして、毎日握りしめていました。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "四年前の初夏の夕暮れ、ハルは、あの石橋のたもとで、歪みに遭って……いなくなったんです。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "見つかりませんでした。ハルの家族は、遠くの町へ移ってしまいました。でも、わたしは、待っていたいんです。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "待っているだけだと、苦しくて。だから、調べたいんです。ハルが、どうなったのか。",
              speaker: "ミナ",
            },
            {
              type: "message",
              text: "話してくれて、ありがとう。ミナが一人で持っていたものを、ぼくに分けてくれた。それは、大きいことだと思う。",
              speaker: "ユーリ",
            },
            {
              type: "choice",
              text: "ミナの申し出にどう答える？",
              options: [
                {
                  label: "一緒に来てください",
                  commands: [
                    { type: "message", text: "はい！　足を引っ張らないよう、頑張ります。", speaker: "ミナ" },
                    { type: "message", text: "ただし、約束を三つ。一つ、俺の後ろから出ない。", speaker: "レト" },
                    { type: "message", text: "二つ、俺が下がれと言ったら、理由を聞かずに下がる。", speaker: "レト" },
                    { type: "message", text: "三つ、怖くなったら、怖いと言う。我慢しない。", speaker: "レト" },
                    { type: "message", text: "……三つ目は、どうしてですか。", speaker: "ミナ" },
                    { type: "message", text: "我慢して黙ってる奴が、いちばん最初に死ぬからだ。", speaker: "レト" },
                    { type: "message", text: "……はい。守ります。大丈夫、わたしがついてます。……なんて、偉そうですね。", speaker: "ミナ" },
                    { type: "setFlag", flag: "chapter1_mina_joined", value: true },
                  ],
                },
                {
                  label: "危ないから村に残ってください",
                  commands: [
                    {
                      type: "message",
                      text: "……そう、ですよね。でも、やっぱり、力になりたいです。気が変わったら、いつでも声をかけてください。",
                      speaker: "ミナ",
                    },
                  ],
                },
              ],
            },
          ],
          else: [
            {
              type: "if",
              flag: "chapter1_quest_accepted",
              equals: true,
              then: [
                {
                  type: "if",
                  flag: "chapter1_mina_asked",
                  equals: true,
                  then: [
                    {
                      type: "message",
                      text: "水源のこと、お願いします。水路をさかのぼると、途中に古い石橋があります。そこから先は、道が細くなるので気をつけて。",
                      speaker: "ミナ",
                    },
                    { type: "message", text: "村長さんにも止められて。大人しく、待っています。", speaker: "ミナ" },
                  ],
                  else: [
                    {
                      type: "message",
                      text: "あの、水源へ行かれるんですよね。わたしも、連れていってもらえませんか。",
                      speaker: "ミナ",
                    },
                    {
                      type: "message",
                      text: "水源の水が止まった原因には、たぶん、危ないものが絡んでる。素人は連れていけないな。",
                      speaker: "レト",
                    },
                    {
                      type: "message",
                      text: "素人じゃありません。水路のことは、この村のだれより知っています。水紋系の術も、少し使えます。",
                      speaker: "ミナ",
                    },
                    { type: "message", text: "使ったこと、ある？", speaker: "レト" },
                    { type: "message", text: "……何度か、村の人の擦り傷に。", speaker: "ミナ" },
                    { type: "message", text: "擦り傷、ね。", speaker: "レト" },
                    { type: "message", text: "でも、擦り傷でも、ちゃんと治りました。", speaker: "ミナ" },
                    {
                      type: "message",
                      text: "そりゃ、いいことだ。……ただ、今日は無理だ。まず水源は、俺たちで見てくる。",
                      speaker: "レト",
                    },
                    {
                      type: "message",
                      text: "……はい。では、道だけでも教えます。水路をさかのぼって、古い石橋の先です。",
                      speaker: "ミナ",
                    },
                    { type: "message", text: "（石橋のことを話すとき、ミナは、そっと目をそらした）" },
                    { type: "setFlag", flag: "chapter1_mina_asked", value: true },
                  ],
                },
              ],
              else: [
                {
                  type: "message",
                  text: "はじめまして。麦香野で生まれ育った、ミナといいます。お水の管理を、お手伝いしているものです。",
                  speaker: "ミナ",
                },
                {
                  type: "message",
                  text: "今は、井戸の水を、お年寄りの家に届けてまわっているんです。水路の水が涸れて、みんな心配しています。",
                  speaker: "ミナ",
                },
              ],
            },
          ],
        },
      ],
    },
  ];
}

function excavationMarkCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_excavation_found",
      equals: true,
      then: [
        { type: "message", text: "掘り返された古い跡が、静かに広がっている。" },
        {
          type: "if",
          flag: "chapter1_yugami_defeated",
          equals: true,
          then: [
            { type: "message", text: "ひびの入った青銅の輪の縁から、レトが小さな欠片を折りとっていた。" },
            { type: "message", text: "欠片の裏には、円の中に一本の線が引かれた、すり減った刻印がある。" },
            { type: "message", text: "……まだ、分からん。ただ、今日のことは、ぜんぶ覚えておけ。ここの匂いも、輪の形も。", speaker: "レト" },
          ],
          else: [],
        },
      ],
      else: [
        { type: "message", text: "取水口のそばの地面が、大きく掘り返されている。浚渫の跡の奥に、古い坑道が口を開けている。" },
        { type: "message", text: "壁には、規則正しい鑿の跡。……これは、灯り石の採掘跡？　こんな所に？" },
        { type: "message", text: "灯里の町外れの、あの焦げ跡のそばにも、崩れかけた古い坑口があった。" },
        { type: "setFlag", flag: "chapter1_excavation_found", value: true },
      ],
    },
  ];
}

function mugikanoYugamiCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_yugami_defeated",
      equals: true,
      then: [{ type: "message", text: "水源はすっかり静かになった。水も、少しずつ戻り始めている。" }],
      else: [
        { type: "message", text: "涸れた水源の奥、掘り返された土の中から、何かがうごめいている。" },
        { type: "message", text: "「歪み」が、姿を現した！" },
        { type: "startBattle", battleId: "mugikano-yugami" },
      ],
    },
  ];
}

function millerCommands(): EventCommand[] {
  return [
    {
      type: "if",
      flag: "chapter1_heard_miller",
      equals: true,
      then: [
        { type: "message", text: "水源の坑道は、見張り小屋の鍵が要る。北の農道を行きなさい。水を抜くバルブは、坑道の左右の部屋だ。", speaker: "ロク" },
        { type: "message", text: "寄り合いの空気は、あんまり吸わんほうがええぞ。今の麦香野は、水より先に、みんなの堪忍袋が涸れとる。", speaker: "ロク" },
      ],
      else: [
        {
          type: "if",
          flag: "chapter1_quest_accepted",
          equals: true,
          then: [
            { type: "message", text: "村長の頼みを受けたのかい。なら、見たことを話しておこう。", speaker: "ロク" },
            {
              type: "message",
              text: "九日前の朝じゃ。前の晩まで、うるさいくらい流れとった水が、朝起きたら、水路の底が見えとった。",
              speaker: "ロク",
            },
            {
              type: "message",
              text: "日照りで涸れたんなら、上流から徐々に細るもんじゃ。それが、村じゅういっぺんに止まりおった。",
              speaker: "レト",
            },
            { type: "message", text: "ほう。あんた、若いのによう見とるな。", speaker: "ロク" },
            { type: "message", text: "（乾いた泥からは、土と、古い水と、焦げたような匂いがした。灯里の町外れで嗅いだ、あの匂いだ）" },
            {
              type: "message",
              text: "水源へは、北の農道を行って、古い坑道を通る。坑道の扉は鍵つきだが、鍵は見張り小屋の箱にあるはずだ。",
              speaker: "ロク",
            },
            { type: "message", text: "坑道の奥の岩戸は、左右にある古いバルブを両方回すと開くと、爺さんの代から聞いている。", speaker: "ロク" },
            { type: "setFlag", flag: "chapter1_heard_miller", value: true },
          ],
          else: [
            { type: "message", text: "わしはロク。ここの粉屋じゃ。六十年、この水車を回しとる。", speaker: "ロク" },
            {
              type: "message",
              text: "水車が止まって、仕事にならん。粉屋はな、村じゅうの胃袋の、いちばん最後の番人なんじゃよ。",
              speaker: "ロク",
            },
            { type: "message", text: "村長が、相談所の人を待っているはずだ。先に会ってやってくれ。", speaker: "ロク" },
          ],
        },
      ],
    },
  ];
}
