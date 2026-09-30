import type { JobData, JobId } from "./types";

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
      { name: "受け流し", requiredStars: 5, description: "1ターンのあいだ受けるダメージを減らす" },
      { name: "守りの構え斬り", requiredStars: 9, description: "防御を保ったまま反撃する" },
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
      { name: "足さばき", requiredStars: 5, description: "自分のすばやさを少し上げる" },
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
      { name: "足止めの矢", requiredStars: 5, description: "敵1体のすばやさを下げる" },
      { name: "急所の一矢", requiredStars: 9, description: "会心が出やすい強力な一射" },
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
      { name: "水紋の膜", requiredStars: 5, description: "味方1人の守りを上げる" },
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
      { name: "風唱の追い風", requiredStars: 2, description: "味方1人のすばやさを上げる" },
      { name: "風唱の眠り唄", requiredStars: 5, description: "敵1体を眠らせることがある" },
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
      { name: "地固の壁", requiredStars: 2, description: "自分の守りを大きく上げる" },
      { name: "かばう", requiredStars: 5, description: "1ターンのあいだ、仲間の代わりに攻撃を受ける" },
      { name: "地固の縛り", requiredStars: 9, description: "敵1体の動きを止めることがある" },
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
      { name: "はやし立て", requiredStars: 2, description: "味方全体の攻撃を少し上げる" },
      { name: "びっくり箱", requiredStars: 5, description: "何が起きるか分からない。良いことも悪いことも起きる" },
      { name: "目くらまし", requiredStars: 9, description: "敵全体の命中を下げる" },
    ],
  },
];

export const JOBS_BY_ID: Record<JobId, JobData> = Object.fromEntries(
  INITIAL_JOBS.map((job) => [job.id, job]),
) as Record<JobId, JobData>;

/** 熟練度の最大（☆）。上級ジョブの解放条件（15☆）と同じ値。 */
export const MAX_STARS = 15;
