import type { Score } from "./score";
import { composeFinale, FINALES } from "./finale";
import { ps2Edition } from "./ps2-edition";
import { realEdition } from "./real-edition";
import { composeSong, type SongSpec, type Style } from "./songwriter";
import { STYLE_TRACKS } from "./style-tracks";

/**
 * ゲームで使うBGM52曲の一覧。場面（`scene`）ごとに1曲ずつ割り当てている。
 * 「作曲エンジン」（songwriter.ts）で作る曲は、設計図（調・速さ・曲調・乱数の種）から毎回同じ曲ができる。
 * 手で書いた7曲（style-tracks.ts）もここに含める。曲を差し替えるときは、この表の設計図（seedなど）を変える。
 */

export interface CatalogEntry {
  id: string;
  title: string;
  /** どの場面で鳴らすか。 */
  scene: string;
  /** 曲調の説明。 */
  styleLabel: string;
  /** 一覧のグループ（章など）。 */
  group: string;
  spec?: SongSpec;
  handmade?: Score;
  /** 3〜4分の特別な曲（ラスボス・裏ボスなど）の設計図のID。 */
  finale?: string;
}

const LABEL: Record<Style, string> = {
  rock: "ロック", metal: "メタル", classic: "クラシック", space: "空間系", cafe: "キーボード（カフェ）", discord: "不協和音", mystery: "不思議",
  epic: "オーケストラ風", folk: "フォーク（アコースティック）", baroque: "バロック協奏曲風", nature: "自然音楽", phonk: "フォンク", samba: "サンバ", jazz: "ジャズ", rnb: "R&B", electro: "エレクトリック",
  hardcore: "ハードコア", deathmetal: "デスメタル", progmetal: "プログレッシブメタル（7拍子）", jpop: "J-POP",
};

function song(group: string, id: string, title: string, scene: string, style: Style, tonic: string, minor: boolean, bpm: number, seed: number, extra: Partial<SongSpec> = {}): CatalogEntry {
  return {
    id, title, scene, group, styleLabel: LABEL[style],
    spec: { id, title, scene, style, tonic, minor, bpm, seed, ...(style === "progmetal" ? { beats: 7 as const } : {}), ...extra },
  };
}
function hand(group: string, id: string, scene: string, handId: string): CatalogEntry {
  const t = STYLE_TRACKS.find((x) => x.id === handId)!;
  return { id, title: t.title, scene, group, styleLabel: t.style, handmade: t.score };
}

function finaleEntry(group: string, id: string, styleLabel: string): CatalogEntry {
  const f = FINALES.find((x) => x.id === id)!;
  return { id, title: f.title, scene: f.scene, group, styleLabel, finale: id };
}

export const CATALOG: CatalogEntry[] = [
  // 序章 灯里
  song("序章 灯里", "title", "灯りの約束", "タイトル画面", "jpop", "C", false, 132, 101),
  song("序章 灯里", "town-touri", "灯里の朝", "灯里の町・灯里支部", "folk", "G", false, 96, 102),
  song("序章 灯里", "outskirts", "町外れの風", "町外れ（歪みの発生地点）", "nature", "D", true, 70, 103),
  song("序章 灯里", "battle", "戦いの合図", "通常戦闘", "hardcore", "E", true, 184, 104),
  song("序章 灯里", "boss-touri", "灯里の歪みとの決戦", "ボス戦「灯里の歪み」", "rock", "A", true, 172, 105, { drive: true }),
  // 第1章 麦香野
  song("第1章 麦香野", "town-mugikano", "麦香野の風車", "麦香野の村", "folk", "F", false, 104, 106),
  song("第1章 麦香野", "water-source", "涸れゆく水源", "水源（採掘跡）", "nature", "A", true, 64, 107),
  song("第1章 麦香野", "boss-mugikano", "水涸れの歪み", "ボス戦「水涸れの歪み」", "electro", "D", true, 176, 108, { drive: true }),
  // 第2章 硝子湖
  song("第2章 硝子湖", "town-garasuko", "硝子湖の港", "硝子湖の町", "jazz", "Bb", false, 112, 109),
  song("第2章 硝子湖", "warehouse", "夜の倉庫", "密輸倉庫", "rnb", "E", true, 84, 110),
  song("第2章 硝子湖", "boss-garasuko", "積荷の歪み", "ボス戦「積荷の歪み」", "progmetal", "E", true, 152, 111, { drive: true }),
  // 第3章 鉄鏈鉱山
  song("第3章 鉄鏈鉱山", "town-tetsu", "鉄鏈の町", "鉄鏈鉱山の町", "rock", "D", false, 116, 112),
  song("第3章 鉄鏈鉱山", "mine", "坑道の奥", "坑内", "electro", "C", true, 100, 113),
  song("第3章 鉄鏈鉱山", "boss-tetsu", "実験の歪み", "ボス戦「実験の歪み」", "deathmetal", "C", true, 214, 114, { drive: true }),
  // 第4章 砂音
  song("第4章 砂音", "town-sanone", "砂音の市場", "砂音の町", "samba", "G", false, 118, 115),
  song("第4章 砂音", "camp", "隊商の野営地", "隊商の野営地", "nature", "D", true, 76, 116),
  song("第4章 砂音", "boss-sanone", "砂嵐の歪み", "ボス戦「砂嵐の歪み」", "metal", "D", true, 186, 117, { drive: true }),
  // 第5章 霧断崖
  song("第5章 霧断崖", "town-kiri", "霧断崖の鐘", "霧断崖の町", "classic", "B", true, 84, 118),
  song("第5章 霧断崖", "archive", "記録の間", "記録の間", "mystery", "A", true, 88, 119),
  song("第5章 霧断崖", "boss-kiri", "予言の歪み", "ボス戦「予言の歪み」", "progmetal", "A", true, 148, 120, { drive: true }),
  // 第6章 霜原
  song("第6章 霜原", "town-shimo", "霜原の灯", "霜原の町", "space", "F#", true, 66, 121),
  song("第6章 霜原", "facility", "戦跡の施設", "戦跡の施設", "electro", "B", true, 108, 122),
  song("第6章 霜原", "boss-shimo", "試作機の歪み", "ボス戦「試作機の歪み」", "epic", "G", true, 176, 123, { drive: true }),
  // 手で書いた7曲
  hand("共通・フィールド", "field", "フィールド（町の外の道）", "rock-road"),
  hand("共通・戦闘", "elite", "強敵との戦闘", "metal-roar"),
  finaleEntry("共通・戦闘", "poly-1", "ポリメトリック（重量級のプログレッシブ）・特別曲"),
  finaleEntry("共通・戦闘", "prog-1", "プログレッシブ（変拍子・ユニゾン・鍵盤ソロ）・特別曲"),
  hand("共通・町", "castle", "城・王宮・議場", "classic-palace"),
  hand("共通・ダンジョン", "ruins", "遺跡・星空の場面", "space-corridor"),
  hand("共通・町", "inn", "宿屋・食堂・酒場", "keys-cafe"),
  hand("共通・イベント", "unease", "不穏なイベント・歪みの気配", "discord-whisper"),
  hand("共通・ダンジョン", "puzzle", "謎解きの迷宮", "mystery-clockwork"),
  // 第7章 浮嶼 / 第8章 灯芯都 / 終章
  song("第7章 浮嶼", "town-ukishima", "浮嶼の空", "浮嶼の町", "nature", "C", false, 78, 131),
  song("第7章 浮嶼", "ruins-ukishima", "浮嶼の遺構", "浮嶼の遺構", "mystery", "F#", true, 92, 132),
  song("第7章 浮嶼", "boss-ukishima", "浮嶼の主", "ボス戦（第7章）", "epic", "E", true, 180, 133, { drive: true }),
  song("第8章 灯芯都", "town-toushin", "灯芯都の光", "灯芯都の町", "electro", "A", false, 124, 134),
  song("第8章 灯芯都", "hall-gikai", "合議会堂", "合議会堂", "classic", "C", true, 84, 135, { beats: 3 }),
  song("第8章 灯芯都", "boss-toushin", "灯芯都の番人", "ボス戦（第8章）", "progmetal", "D", true, 160, 136, { drive: true }),
  finaleEntry("終章 虚灯宮", "boss-final", "メタル×プログレッシブ（7拍子・転調）・速い・特別曲"),
  finaleEntry("終章 虚灯宮", "boss-final-2", "ロマン派×ドゥーム・遅い（絶望）・特別曲"),
  finaleEntry("クリア後", "secret-boss", "虚無×ロマン派・遅い（絶望）・特別曲"),
  finaleEntry("クリア後", "secret-boss-2", "デスメタル×プログレッシブ・速い・特別曲"),
  finaleEntry("クリア後", "eight-gods", "プログレッシブメタル（8柱で転調）・速い・特別曲"),
  finaleEntry("クリア後", "eight-gods-2", "ロマン派×ドゥーム・遅い（絶望）・特別曲"),
  finaleEntry("イベント", "fate", "オーケストラ×メタル・短調から長調の勝利へ・特別曲"),
  song("終章 虚灯宮", "kyoto-road", "虚灯宮への道", "虚灯宮（前半）", "space", "D", true, 70, 137),
  song("クリア後", "kyoto-deep", "虚灯宮・深部", "虚灯宮・深部", "mystery", "Bb", true, 84, 141),
  song("イベント", "opening", "旅立ちの朝", "オープニング（旅立ち）", "baroque", "G", false, 132, 142),
  song("イベント", "sad", "別れの雨", "悲しい場面・別れ", "classic", "A", true, 60, 143),
  song("イベント", "deduction", "真相にたどりつく", "推理パート・真相の場面", "jazz", "D", true, 100, 144),
  song("イベント", "memory", "追憶の灯", "回想・思い出の場面", "folk", "A", false, 72, 145),
  song("イベント", "ending", "灯りのゆくえ", "エンディング", "jpop", "F", false, 120, 146),
  song("イベント", "staff-roll", "旅の終わりに", "スタッフロール", "classic", "G", false, 90, 147),
  song("イベント", "vehicle", "風をつかまえて", "乗り物（帆走車・船）で移動", "rock", "A", false, 138, 148),
  song("イベント", "bond", "仲間のちから", "仲間との絆・決意の場面", "jpop", "E", false, 146, 149),
  song("イベント", "chase", "追われる夜", "追跡・逃走イベント", "phonk", "A", true, 140, 151),
  song("第8章 灯芯都", "alley-toushin", "灯芯都の裏通り", "灯芯都の路地・裏取引の場面", "phonk", "D", true, 132, 152),
];

const cache = new Map<string, Score>();
/** 曲のデータを取り出す（初めて使うときに作って、以後は使い回す）。 */
export function getTrack(id: string): Score {
  let score = cache.get(id);
  if (!score) {
    const entry = CATALOG.find((e) => e.id === id);
    if (!entry) throw new Error(`曲がありません: ${id}`);
    score = entry.handmade ?? (entry.finale ? composeFinale(FINALES.find((f) => f.id === entry.finale)!) : composeSong(entry.spec!));
    cache.set(id, score);
  }
  return score;
}

export type Edition = "modern" | "ps2" | "real";
/** 曲を、指定した版で取り出す。ps2版は、同じ曲をPS2世代のサウンド（オーケストラの重ね・ホール残響）で、real版は、実際のバンド・オーケストラ・楽器の音色で作り直したもの。 */
export function getTrackEdition(id: string, edition: Edition): Score {
  if (edition === "modern") {
    return getTrack(id);
  }
  const key = `${id}|${edition}`;
  let score = cache.get(key);
  if (!score) {
    score = edition === "real" ? realEdition(getTrack(id)) : ps2Edition(getTrack(id));
    cache.set(key, score);
  }
  return score;
}
