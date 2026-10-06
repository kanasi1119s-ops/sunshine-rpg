import type { EquipmentItemData, ItemTrait } from "./types";

/**
 * サブストーリーのごほうび（2026-10-06、人間の指示「サイドストーリーが終わるたびに特殊なアイテム、装備もらえるようにしようか」）。
 * サブストーリー1本ごとに、そこでしか手に入らない装備が1つ（店では売っていない）。話の中身に合わせた名前と、特殊効果つき。
 * 強さは、その話がある章の店の装備より少し上。仲間の話では、その仲間が持てる武器になることがある。数値は仮。
 * キーはサブストーリーの key（`side-stories.ts`）。品物のIDは `side-<key>`。
 */
const G = (status: "poison" | "sleep" | "confuse"): ItemTrait => ({ kind: "guard", status });
type Def = Omit<EquipmentItemData, "id" | "price">;

const REWARDS: Record<string, Def> = {
  // 序章（灯里）
  s001: { name: "灯り貂の毛のお守り", category: "accessory", statBonus: { maxHp: 10 }, traits: [{ kind: "luck", value: 3 }], description: "灯り貂ルルの、ふわふわの抜け毛を編んだお守り。運がよくなる。" },
  s002: { name: "支部の封蝋ナイフ", category: "weapon", weaponType: "dagger", statBonus: { attack: 9 }, traits: [{ kind: "crit", value: 3 }], description: "レトが封筒を開けるのに使っていた小刀。よく切れる。会心が出やすい。" },
  // 第1章（麦香野）
  s003: { name: "水車の歯車盾", category: "shield", statBonus: { defense: 8 }, traits: [{ kind: "regenHp", percent: 2 }], description: "直した水車の、古い歯車でできた盾。毎ターンHPが少しもどる。" },
  s004: { name: "幼き日の約束の杖", category: "weapon", weaponType: "staff", statBonus: { attack: 16, maxMp: 6 }, traits: [{ kind: "regenMp", value: 1 }], description: "ミナが幼なじみと約束をした日の、小さな杖。魔力が少しずつもどる。" },
  s005: { name: "麦の穂の飾り", category: "accessory", statBonus: { maxHp: 18, speed: 2 }, traits: [{ kind: "regenHp", percent: 2 }], description: "水争いがおさまった麦畑の穂で編んだ飾り。" },
  // 第2章（硝子湖）
  s006: { name: "値切り上手の財布", category: "accessory", statBonus: { maxMp: 6 }, traits: [{ kind: "luck", value: 5 }], description: "湖上市場の名物おばあさんの財布。持つと運がよくなる。" },
  s007: { name: "従兄の古い弓", category: "weapon", weaponType: "bow", statBonus: { attack: 25 }, traits: [{ kind: "crit", value: 4 }], description: "コハクの従兄が使っていた、手になじむ弓。会心が出やすい。" },
  s008: { name: "渡し守の雨笠", category: "head", statBonus: { defense: 9 }, traits: [{ kind: "evade", value: 4 }], description: "湖の渡し守が昔かぶっていた笠。敵の攻撃がはずれやすい。" },
  // 第3章（鉄鎖）
  s009: { name: "組合長の印章の指輪", category: "accessory", statBonus: { maxMp: 10 }, traits: [{ kind: "regenMp", value: 2 }], description: "書類の山を片づけたお礼の指輪。魔力が少しずつもどる。" },
  s010: { name: "再会の髪かざり", category: "head", statBonus: { defense: 10, maxMp: 12 }, traits: [G("confuse")], description: "ミナが幼なじみからもらった髪かざり。心が乱れない（混乱しない）。" },
  s011: { name: "鎮魂の坑夫斧", category: "weapon", weaponType: "axe", statBonus: { attack: 34 }, traits: [G("poison")], description: "事故で亡くなった仲間をしのぶ、オルカの斧。毒をふせぐ。" },
  // 第4章（砂音）
  s012: { name: "風読みの外套", category: "armor", statBonus: { defense: 22, speed: 4 }, traits: [{ kind: "evade", value: 4 }], description: "隊商が風を読むときに着る外套。身軽になる。" },
  s013: { name: "隊商の護り札", category: "accessory", statBonus: { maxHp: 40 }, traits: [G("sleep")], description: "隊商の長がくれた札。眠らない。" },
  // 第5章（霧断崖）
  s015: { name: "支部長の古い剣", category: "weapon", weaponType: "sword", statBonus: { attack: 56 }, traits: [{ kind: "crit", value: 4 }], description: "カセン支部長が若いころ使っていた剣。会心が出やすい。" },
  s016: { name: "巡礼の灯り石", category: "accessory", statBonus: { maxMp: 18 }, traits: [{ kind: "regenMp", value: 3 }], description: "光をためた巡礼の石。魔力が少しずつもどる。" },
  s017: { name: "真実の片眼鏡", category: "head", statBonus: { defense: 14 }, traits: [{ kind: "crit", value: 5 }, G("confuse")], description: "記録の余白を読み解いた片眼鏡。会心が出やすく、混乱しない。" },
  s029: { name: "残り火のマント", category: "armor", statBonus: { defense: 28 }, traits: [{ kind: "regenHp", percent: 2 }], description: "灯を失った村に残っていた、ほのかに温かいマント。" },
  s030: { name: "合一を拒む護符", category: "accessory", statBonus: { maxHp: 45 }, traits: [G("confuse"), G("sleep")], description: "教団の秘技に心をあずけない護符。混乱も眠りもしない。" },
  // 第6章（霜原）
  s018: { name: "観察者の白槍", category: "weapon", weaponType: "spear", statBonus: { attack: 66, speed: 3 }, traits: [{ kind: "crit", value: 5 }], description: "アヤメの観察日記にえがかれていた白い槍。" },
  s019: { name: "戦跡の古盾", category: "shield", statBonus: { defense: 26 }, traits: [G("poison")], description: "大乱期の戦跡で見つかった盾。毒をふせぐ。" },
  s020: { name: "あたたかい毛布の外套", category: "armor", statBonus: { defense: 34, maxHp: 20 }, traits: [{ kind: "regenHp", percent: 3 }, G("sleep")], description: "遭難者を包んだ毛布で仕立てた外套。眠らず、HPが少しずつもどる。" },
  // 第7章（浮嶼）
  s021: { name: "測量士の遠眼鏡", category: "accessory", statBonus: { speed: 5 }, traits: [{ kind: "luck", value: 6 }, { kind: "crit", value: 6 }], description: "浮島をはかった遠眼鏡。急所がよく見える。" },
  s022: { name: "試作機の鉄籠手", category: "accessory", statBonus: { attack: 14, defense: 8 }, traits: [{ kind: "multi", value: 3 }], description: "老技術者が作った試作機の籠手。連続攻撃がしやすい。" },
  s023: { name: "避難民の守り布", category: "head", statBonus: { defense: 20, maxHp: 30 }, traits: [{ kind: "regenHp", percent: 2 }], description: "避難民の子どもたちが縫ってくれた守り布。" },
  s031: { name: "残り火を断つ短剣", category: "weapon", weaponType: "dagger", statBonus: { attack: 82 }, traits: [{ kind: "crit", value: 6 }], description: "教団の残り火を断った短剣。会心が出やすい。" },
  s033: { name: "空鳥の木彫り", category: "accessory", statBonus: { speed: 8 }, traits: [{ kind: "multi", value: 4 }, { kind: "evade", value: 6 }], description: "浮嶼の空鳥の木彫り。体が軽くなり、連続攻撃がしやすい。" },
  // 第8章（灯芯都）
  s024: { name: "合議会の銀の盾", category: "shield", statBonus: { defense: 34 }, traits: [G("confuse")], description: "合議会の下働きがこっそりくれた銀の盾。混乱しない。" },
  s025: { name: "灯里の便りの外套", category: "armor", statBonus: { defense: 40, maxHp: 40 }, traits: [{ kind: "regenHp", percent: 3 }], description: "灯里からの手紙といっしょに届いた外套。ふるさとの温かさがある。" },
  s026: { name: "祖父の遺した槍", category: "weapon", weaponType: "spear", statBonus: { attack: 100 }, traits: [{ kind: "crit", value: 6 }, { kind: "luck", value: 4 }], description: "アヤメの祖父が遺した槍。" },
  s032: { name: "静けさの鈴飾り", category: "accessory", statBonus: { maxMp: 30 }, traits: [G("poison"), G("sleep"), G("confuse")], description: "教団の終わりに鳴った鈴。毒・眠り・混乱をふせぐ。" },
  // クリア後
  s027: { name: "思い出の灯り輪", category: "accessory", statBonus: { maxHp: 80 }, traits: [{ kind: "regenHp", percent: 3 }, { kind: "luck", value: 6 }], description: "仲間たちとの思い出をこめた輪。" },
  s028: { name: "虚灯宮の鍵剣", category: "weapon", weaponType: "sword", statBonus: { attack: 115 }, traits: [{ kind: "crit", value: 6 }, { kind: "multi", value: 4 }], description: "虚灯宮の奥への道を開いた、鍵の形の剣。" },
};

export const SIDE_REWARD_ITEMS: EquipmentItemData[] = Object.entries(REWARDS).map(([key, d]) => ({ id: `side-${key}`, price: 0, ...d }));
export const SIDE_REWARD_ITEMS_BY_ID: Record<string, EquipmentItemData> = Object.fromEntries(SIDE_REWARD_ITEMS.map((i) => [i.id, i]));

/** そのサブストーリー（key）のごほうびの装備のID（無ければ undefined）。 */
export function sideRewardFor(key: string): string | undefined {
  return SIDE_REWARD_ITEMS_BY_ID[`side-${key}`] ? `side-${key}` : undefined;
}
