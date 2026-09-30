import type { JobData, JobId } from "./types";

/** 熟練度の最大（☆）。上級ジョブの解放条件（15☆）と同じ値。 */
export const MAX_STARS = 15;

/** 初期ジョブ8種（`docs/design/jobs.md` 2章）。数値は仮で、今後シミュレーションで調整する。 */
export const INITIAL_JOBS: JobData[] = [
  {
    id: "sword-guard",
    name: "剣衛士",
    reading: "けんえいし",
    role: "攻防のバランスが良い近接アタッカー兼盾役",
    statBonus: { attack: 3, defense: 3 },
    bonusPerStar: { attack: 1, defense: 1 },
    skills: [
      { name: "踏み込み斬り", requiredStars: 2, description: "一歩踏み込んで敵1体を強く斬る", battle: { mpCost: 2, powerMultiplier: 1.5 } },
      { name: "受け流し", requiredStars: 5, description: "3ターンのあいだ自分の守りを上げる", battle: { mpCost: 2, powerMultiplier: 0, effect: "buff", stat: "defense", mult: 1.4, turns: 3 } },
      { name: "守りの構え斬り", requiredStars: 9, description: "守りを固めたまま、敵1体を斬る", battle: { mpCost: 4, powerMultiplier: 2.0 } },
    ],
  },
  {
    id: "fist-fighter",
    name: "拳闘士",
    reading: "けんとうし",
    role: "連続攻撃が得意な高速アタッカー",
    statBonus: { attack: 2, speed: 4 },
    bonusPerStar: { attack: 1, speed: 1 },
    skills: [
      { name: "二連打", requiredStars: 2, description: "敵1体に2回続けて殴る", battle: { mpCost: 3, powerMultiplier: 1.0, effect: "multi", hits: 2 } },
      { name: "足さばき", requiredStars: 5, description: "自分のすばやさを少し上げる", battle: { mpCost: 2, powerMultiplier: 0, effect: "buff", stat: "speed", mult: 1.3, turns: 3 } },
      { name: "乱れ打ち", requiredStars: 9, description: "敵1体に3回続けて殴る", battle: { mpCost: 7, powerMultiplier: 1.1, effect: "multi", hits: 3 } },
    ],
  },
  {
    id: "archer",
    name: "弓術士",
    reading: "きゅうじゅつし",
    role: "会心が出やすい遠距離アタッカー",
    statBonus: { attack: 3, speed: 2 },
    bonusPerStar: { attack: 1, speed: 1 },
    skills: [
      { name: "狙い撃ち", requiredStars: 2, description: "当たりやすく、会心が出やすい一射", battle: { mpCost: 2, powerMultiplier: 1.4 } },
      { name: "足止めの矢", requiredStars: 5, description: "敵1体のすばやさを下げる", battle: { mpCost: 3, powerMultiplier: 0, effect: "debuff", stat: "speed", mult: 0.7, turns: 3, chance: 0.85 } },
      { name: "急所の一矢", requiredStars: 9, description: "急所をねらう強力な一射で、敵1体を撃つ", battle: { mpCost: 6, powerMultiplier: 2.4 } },
    ],
  },
  {
    id: "flame-mage",
    name: "火照術士",
    reading: "かしょうじゅつし",
    role: "攻撃呪文に特化した、MP効率の良い術士",
    statBonus: { maxMp: 8, attack: 1 },
    bonusPerStar: { maxMp: 3 },
    skills: [
      { name: "火照の灯", requiredStars: 2, description: "小さな火で敵1体を焼く", battle: { mpCost: 2, powerMultiplier: 1.5 } },
      { name: "火照の波", requiredStars: 5, description: "熱の波で敵全体を焼く", battle: { mpCost: 5, powerMultiplier: 1.0, effect: "damageAll" } },
      { name: "火照の奔流", requiredStars: 9, description: "強い火で敵1体を焼き尽くす", battle: { mpCost: 8, powerMultiplier: 2.6 } },
    ],
  },
  {
    id: "ripple-mage",
    name: "水紋術士",
    reading: "すいもんじゅつし",
    role: "回復と防御の呪文に特化した術士",
    statBonus: { maxMp: 8, defense: 1 },
    bonusPerStar: { maxMp: 3 },
    skills: [
      { name: "水紋の癒し", requiredStars: 2, description: "味方1人のHPを回復する", battle: { mpCost: 3, powerMultiplier: 0, effect: "heal", healRatio: 1.6 } },
      { name: "水紋の膜", requiredStars: 5, description: "味方1人の守りを上げる", battle: { mpCost: 4, powerMultiplier: 0, effect: "buff", stat: "defense", mult: 1.4, turns: 3 } },
      { name: "水紋の慈雨", requiredStars: 9, description: "味方全体のHPを少し回復する", battle: { mpCost: 8, powerMultiplier: 0, effect: "healAll", healRatio: 1.0 } },
    ],
  },
  {
    id: "wind-mage",
    name: "風唱術士",
    reading: "ふうしょうじゅつし",
    role: "すばやさ強化と状態異常が得意な術士",
    statBonus: { maxMp: 6, speed: 3 },
    bonusPerStar: { maxMp: 2, speed: 1 },
    skills: [
      { name: "風唱の追い風", requiredStars: 2, description: "味方1人のすばやさを上げる", battle: { mpCost: 3, powerMultiplier: 0, effect: "buff", stat: "speed", mult: 1.3, turns: 3 } },
      { name: "風唱の眠り唄", requiredStars: 5, description: "敵1体を眠らせることがある（体力の大きい敵には効かない）", battle: { mpCost: 5, powerMultiplier: 0, effect: "sleep", chance: 0.6, turns: 2 } },
      { name: "風唱の刃", requiredStars: 9, description: "風の刃で敵全体を切る", battle: { mpCost: 8, powerMultiplier: 1.2, effect: "damageAll" } },
    ],
  },
  {
    id: "earth-guard",
    name: "地固衛士",
    reading: "ちこえいし",
    role: "防御と拘束に特化した、パーティ最高クラスの耐久",
    statBonus: { maxHp: 10, defense: 3 },
    bonusPerStar: { maxHp: 4, defense: 1 },
    skills: [
      { name: "地固の壁", requiredStars: 2, description: "自分の守りを大きく上げる", battle: { mpCost: 3, powerMultiplier: 0, effect: "buff", stat: "defense", mult: 1.6, turns: 3 } },
      { name: "かばう", requiredStars: 5, description: "1ターンのあいだ、仲間の代わりに攻撃を受ける" },
      { name: "地固の縛り", requiredStars: 9, description: "敵1体の動きを止めることがある（体力の大きい敵には効かない）", battle: { mpCost: 6, powerMultiplier: 0, effect: "sleep", chance: 0.5, turns: 2 } },
    ],
  },
  {
    id: "wanderer",
    name: "旅芸人",
    reading: "たびげいにん",
    role: "支援と変則の効果を扱う、器用貧乏だが腐らない芸人",
    statBonus: { maxHp: 6, maxMp: 4, speed: 1 },
    bonusPerStar: { maxHp: 2, maxMp: 1 },
    skills: [
      { name: "はやし立て", requiredStars: 2, description: "味方全体の攻撃を少し上げる", battle: { mpCost: 6, powerMultiplier: 0, effect: "buffAll", stat: "attack", mult: 1.25, turns: 3 } },
      { name: "びっくり箱", requiredStars: 5, description: "何が起きるか分からない。良いことも悪いことも起きる" },
      { name: "目くらまし", requiredStars: 9, description: "敵全体の攻撃を下げる", battle: { mpCost: 8, powerMultiplier: 0, effect: "debuffAll", stat: "attack", mult: 0.75, turns: 3, chance: 0.8 } },
    ],
  },
];

/**
 * 上級ジョブ8種（`docs/design/jobs.md` 3章）。初期ジョブを最大の☆まで育てると解放され、以後は切り替えて使える。
 * 「初期ジョブの、同じ方向性のままの底上げ」（同6章）。特技は、効果つきの特技（複数回・全体・回復）で、すべて戦闘で使える。数値は仮。
 */
export const ADVANCED_JOBS: JobData[] = [
  {
    id: "sword-saint", baseJob: "sword-guard", name: "剛剣聖", reading: "ごうけんせい", role: "攻防とも一段強い、パーティの主力アタッカー兼壁",
    statBonus: { attack: 7, defense: 6 }, bonusPerStar: { attack: 2, defense: 1 },
    skills: [
      { name: "断空斬", requiredStars: 2, description: "空ごと断つ一太刀で敵1体を斬る", battle: { mpCost: 4, powerMultiplier: 2.0 } },
      { name: "烈風の連撃", requiredStars: 5, description: "敵1体に2回続けて斬りつける", battle: { mpCost: 6, powerMultiplier: 1.3, effect: "multi", hits: 2 } },
      { name: "不動の一刀", requiredStars: 9, description: "渾身の一刀で敵1体を斬り伏せる", battle: { mpCost: 9, powerMultiplier: 3.0 } },
    ],
  },
  {
    id: "sky-fist", baseJob: "fist-fighter", name: "天翔拳士", reading: "てんしょうけんし", role: "最速クラスの行動回数を稼ぐ、乱れ撃ちの拳士",
    statBonus: { attack: 4, speed: 8 }, bonusPerStar: { attack: 1, speed: 2 },
    skills: [
      { name: "疾風三連", requiredStars: 2, description: "敵1体に3回続けて殴る", battle: { mpCost: 5, powerMultiplier: 0.9, effect: "multi", hits: 3 } },
      { name: "天翔ノ舞", requiredStars: 5, description: "敵1体に4回続けて殴る", battle: { mpCost: 8, powerMultiplier: 0.85, effect: "multi", hits: 4 } },
      { name: "千手乱舞", requiredStars: 9, description: "敵1体に5回続けて殴る", battle: { mpCost: 12, powerMultiplier: 0.8, effect: "multi", hits: 5 } },
    ],
  },
  {
    id: "hundred-archer", baseJob: "archer", name: "百矢の射手", reading: "ひゃくしのいて", role: "敵全体をまとめて狙える弓の名手",
    statBonus: { attack: 6, speed: 4 }, bonusPerStar: { attack: 2, speed: 1 },
    skills: [
      { name: "貫きの矢", requiredStars: 2, description: "鋭い一射で敵1体を貫く", battle: { mpCost: 3, powerMultiplier: 1.8 } },
      { name: "雨矢", requiredStars: 5, description: "矢の雨で敵全体を射る", battle: { mpCost: 7, powerMultiplier: 1.0, effect: "damageAll" } },
      { name: "百矢", requiredStars: 9, description: "百の矢で敵全体を射抜く", battle: { mpCost: 12, powerMultiplier: 1.6, effect: "damageAll" } },
    ],
  },
  {
    id: "inferno-guide", baseJob: "flame-mage", name: "業火導師", reading: "ごうかどうし", role: "範囲攻撃呪文を極めた炎の導き手",
    statBonus: { maxMp: 16, attack: 2 }, bonusPerStar: { maxMp: 4 },
    skills: [
      { name: "業火", requiredStars: 2, description: "激しい炎で敵1体を焼く", battle: { mpCost: 5, powerMultiplier: 2.2 } },
      { name: "炎の渦", requiredStars: 5, description: "炎の渦で敵全体を焼く", battle: { mpCost: 9, powerMultiplier: 1.5, effect: "damageAll" } },
      { name: "灼熱の滅", requiredStars: 9, description: "すべてを灼く炎で敵1体を焼き尽くす", battle: { mpCost: 14, powerMultiplier: 3.4 } },
    ],
  },
  {
    id: "stream-sage", baseJob: "ripple-mage", name: "清流賢者", reading: "せいりゅうけんじゃ", role: "全体回復を極めた、水の賢者",
    statBonus: { maxMp: 16, defense: 2 }, bonusPerStar: { maxMp: 4 },
    skills: [
      { name: "清流の癒し", requiredStars: 2, description: "味方1人のHPを大きく回復する", battle: { mpCost: 5, powerMultiplier: 0, effect: "heal", healRatio: 2.4 } },
      { name: "清流の慈雨", requiredStars: 5, description: "味方全体のHPを回復する", battle: { mpCost: 10, powerMultiplier: 0, effect: "healAll", healRatio: 1.6 } },
      { name: "甦りの雫", requiredStars: 9, description: "味方1人のHPを、ほとんど全快させる", battle: { mpCost: 14, powerMultiplier: 0, effect: "heal", healRatio: 4.0 } },
    ],
  },
  {
    id: "gale-dancer", baseJob: "wind-mage", name: "疾風の舞手", reading: "しっぷうのまいて", role: "風の刃で敵全体を切る、すばやい舞い手",
    statBonus: { maxMp: 12, speed: 6 }, bonusPerStar: { maxMp: 3, speed: 2 },
    skills: [
      { name: "疾風の刃", requiredStars: 2, description: "風の刃で敵全体を切る", battle: { mpCost: 7, powerMultiplier: 1.4, effect: "damageAll" } },
      { name: "風の舞", requiredStars: 5, description: "舞うように敵1体を3回切る", battle: { mpCost: 8, powerMultiplier: 1.1, effect: "multi", hits: 3 } },
      { name: "颶風", requiredStars: 9, description: "大きな風で敵全体を吹き飛ばす", battle: { mpCost: 13, powerMultiplier: 2.0, effect: "damageAll" } },
    ],
  },
  {
    id: "immovable-guardian", baseJob: "earth-guard", name: "不動の守人", reading: "ふどうのもりびと", role: "だれよりも硬い、大地の守り手",
    statBonus: { maxHp: 20, defense: 6 }, bonusPerStar: { maxHp: 6, defense: 2 },
    skills: [
      { name: "不動の一撃", requiredStars: 2, description: "重い拳で敵1体を打つ", battle: { mpCost: 3, powerMultiplier: 1.8 } },
      { name: "岩砕き", requiredStars: 5, description: "岩をも砕く一撃で敵1体を打つ", battle: { mpCost: 6, powerMultiplier: 2.4 } },
      { name: "大地の怒り", requiredStars: 9, description: "大地を揺らして敵全体を打つ", battle: { mpCost: 10, powerMultiplier: 1.6, effect: "damageAll" } },
    ],
  },
  {
    id: "many-faced-artist", baseJob: "wanderer", name: "千変の遊芸師", reading: "せんぺんのゆうげいし", role: "何が飛び出すか分からない、器用な芸人",
    statBonus: { maxHp: 12, maxMp: 8, speed: 2 }, bonusPerStar: { maxHp: 3, maxMp: 2 },
    skills: [
      { name: "千変の一手", requiredStars: 2, description: "思いがけない一手で敵1体を打つ", battle: { mpCost: 4, powerMultiplier: 2.0 } },
      { name: "びっくり乱れ打ち", requiredStars: 5, description: "小道具で敵1体を3回打つ", battle: { mpCost: 7, powerMultiplier: 1.0, effect: "multi", hits: 3 } },
      { name: "大道芸の締め", requiredStars: 9, description: "大がかりな芸で敵全体を打つ", battle: { mpCost: 11, powerMultiplier: 1.8, effect: "damageAll" } },
    ],
  },
];

/**
 * 天神ジョブ2種・悪神ジョブ2種（`docs/design/jobs.md` 5章）。8神のうち特に対照的な4柱を倒すと、だれでも装備できる。
 * 「上級ジョブより強い」のではなく、「上級ジョブにはない役割と、必ず弱点がある」形（同6章）。数値は仮。
 * - 天神: 女神の巫覡（最高クラスの回復。攻撃は弱い）、純神の聖騎士（最高クラスの守り。攻撃は控えめ）
 * - 悪神: 鬼神の破戒者（最高クラスの攻撃。使うたびにHPを支払う）、蟲神の呪術師（一撃で倒すチャンス。強敵には効かず、確実性がない）
 */
export const DIVINE_JOBS: JobData[] = [
  {
    id: "goddess-shaman", unlockFlag: "god1_defeated", name: "女神の巫覡", reading: "めがみのふげき", role: "最高クラスの回復。ただし攻撃は弱い",
    statBonus: { maxMp: 20, defense: 2, attack: -4 }, bonusPerStar: { maxMp: 5 },
    skills: [
      { name: "恵みの光", requiredStars: 2, description: "味方1人のHPを、たっぷり回復する", battle: { mpCost: 6, powerMultiplier: 0, effect: "heal", healRatio: 3.0 } },
      { name: "命の雨", requiredStars: 5, description: "味方全体のHPを回復する", battle: { mpCost: 12, powerMultiplier: 0, effect: "healAll", healRatio: 2.0 } },
      { name: "女神の祝福", requiredStars: 9, description: "味方全体のHPを、大きく回復する", battle: { mpCost: 18, powerMultiplier: 0, effect: "healAll", healRatio: 3.5 } },
    ],
  },
  {
    id: "pure-paladin", unlockFlag: "god5_defeated", name: "純神の聖騎士", reading: "じゅんしんのせいきし", role: "最高クラスの守りと反撃。攻撃の伸びは控えめ",
    statBonus: { defense: 10, maxHp: 30, attack: -2 }, bonusPerStar: { defense: 2, maxHp: 6 },
    skills: [
      { name: "聖なる反撃", requiredStars: 2, description: "守りの構えから、敵1体を打つ", battle: { mpCost: 4, powerMultiplier: 2.0 } },
      { name: "誓いの一閃", requiredStars: 5, description: "誓いをこめた一撃で、敵1体を斬る", battle: { mpCost: 7, powerMultiplier: 2.6 } },
      { name: "純白の裁き", requiredStars: 9, description: "白い光で敵全体を裁く", battle: { mpCost: 11, powerMultiplier: 1.8, effect: "damageAll" } },
    ],
  },
  {
    id: "demon-breaker", unlockFlag: "god3_defeated", name: "鬼神の破戒者", reading: "きしんのはかいしゃ", role: "最高クラスの攻撃力。ただし、使うたびに自分のHPを支払う",
    statBonus: { attack: 14, defense: -3 }, bonusPerStar: { attack: 3 },
    skills: [
      { name: "破戒の一撃", requiredStars: 2, description: "HPを支払って、敵1体に強烈な一撃", battle: { mpCost: 3, powerMultiplier: 2.8, hpCost: 0.1 } },
      { name: "鬼哭", requiredStars: 5, description: "HPを支払って、敵全体に叫びをぶつける", battle: { mpCost: 6, powerMultiplier: 2.0, effect: "damageAll", hpCost: 0.12 } },
      { name: "修羅の滅", requiredStars: 9, description: "大きくHPを支払って、敵1体を打ち砕く", battle: { mpCost: 8, powerMultiplier: 4.5, hpCost: 0.2 } },
    ],
  },
  {
    id: "bug-curser", unlockFlag: "god2_defeated", name: "蟲神の呪術師", reading: "ちゅうしんのじゅじゅつし", role: "一撃で倒すチャンスを持つ。ただし強敵には効かず、確実ではない",
    statBonus: { maxMp: 14, speed: 6, defense: -2 }, bonusPerStar: { maxMp: 3, speed: 1 },
    skills: [
      { name: "蟲の囁き", requiredStars: 2, description: "小さな蟲の毒で、敵1体を弱らせる", battle: { mpCost: 3, powerMultiplier: 1.6 } },
      { name: "理不尽の羽音", requiredStars: 5, description: "理由もなく命を刈る羽音。敵1体を、ときどき一撃で倒す（強敵には効かない）", battle: { mpCost: 8, powerMultiplier: 1.0, koChance: 0.18 } },
      { name: "蟲の大群", requiredStars: 9, description: "蟲の群れで敵全体を襲う", battle: { mpCost: 12, powerMultiplier: 2.0, effect: "damageAll" } },
    ],
  },
];

/**
 * レジェンドジョブ「灯心継承者」（主人公専用、`docs/design/jobs.md` 4章）。5系統すべてを、やや高いMPで扱える「何でも屋」。
 * 1点特化の強さは無く、上級ジョブを陳腐化させない。
 * 解放条件: 本編クリア後、仲間4人（レト・ミナ・ガイド・オルカ）との絆（それぞれの寄り道サブストーリー）がそろい、カセンの手紙（S-025）を読んでいる。
 * （信頼度の数値は作らず、サブストーリーの完了で数える。`docs/decisions.md`）
 */
export const LEGEND_UNLOCK_FLAGS: string[] = [
  "chapter9_cleared",
  "side_s002_done", // レト
  "side_s004_done", "side_s010_done", // ミナ（幼なじみ前編・後編）
  "side_s006_done", "side_s007_done", // ガイド
  "side_s009_done", "side_s011_done", // オルカ
  "side_s025_done", // カセンの手紙
];

export const LEGEND_JOBS: JobData[] = [
  {
    id: "torch-heir", unlockFlags: LEGEND_UNLOCK_FLAGS, heroOnly: true, name: "灯心継承者", reading: "とうしんけいしょうしゃ", role: "五系統の呪文をやや高いMPで扱う何でも屋",
    statBonus: { maxHp: 10, maxMp: 12, attack: 5, defense: 4, speed: 3 }, bonusPerStar: { maxHp: 2, maxMp: 3, attack: 1, defense: 1, speed: 1 },
    skills: [
      { name: "灯の一閃", requiredStars: 2, description: "灯りをまとった一撃で敵1体を斬る", battle: { mpCost: 5, powerMultiplier: 1.9 } },
      { name: "灯の癒し", requiredStars: 4, description: "灯りで味方1人のHPを回復する", battle: { mpCost: 8, powerMultiplier: 0, effect: "heal", healRatio: 2.0 } },
      { name: "灯の波", requiredStars: 6, description: "灯りの波で敵全体を打つ", battle: { mpCost: 10, powerMultiplier: 1.3, effect: "damageAll" } },
      { name: "灯の慈雨", requiredStars: 8, description: "灯りの雨で味方全体を癒す", battle: { mpCost: 14, powerMultiplier: 0, effect: "healAll", healRatio: 1.3 } },
      { name: "灯心の共鳴", requiredStars: 10, description: "五つの系統を重ねて、敵1体に放つ", battle: { mpCost: 16, powerMultiplier: 3.2 } },
    ],
  },
];

export const JOBS_BY_ID: Record<JobId, JobData> = Object.fromEntries(
  [...INITIAL_JOBS, ...ADVANCED_JOBS, ...DIVINE_JOBS, ...LEGEND_JOBS].map((job) => [job.id, job]),
) as Record<JobId, JobData>;

/**
 * そのキャラクターがいま装備できるジョブ（初期ジョブ8種と、初期ジョブを最大の☆まで育てて解放した上級ジョブ）。
 * 上級ジョブは初期ジョブの直後、天神・悪神ジョブ（8神を倒すと解放）、レジェンドジョブ（主人公だけ）はその後ろに並ぶ。
 */
export function availableJobs(
  masteryStars: (jobId: JobId) => number,
  flags: Record<string, boolean | undefined> = {},
  memberId?: string,
): JobData[] {
  return [
    ...INITIAL_JOBS,
    ...ADVANCED_JOBS.filter((job) => job.baseJob !== undefined && masteryStars(job.baseJob) >= MAX_STARS),
    ...DIVINE_JOBS.filter((job) => job.unlockFlag !== undefined && flags[job.unlockFlag] === true),
    ...LEGEND_JOBS.filter((job) => (!job.heroOnly || memberId === "hero") && (job.unlockFlags ?? []).every((f) => flags[f] === true)),
  ];
}

