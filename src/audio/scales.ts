import { parseChord } from "./newsong";
import { noteNameToMidi } from "./note";

/**
 * 音階・旋法のデータと、音階に関する小さな道具（2026-10-11、docs/sound/scales-world-guide.md の提案 1・4・5）。
 * 表は同ガイドの 2-1（42 種＋微分音 2 種）。C を主音にした音の並びを、半音数（semis）で持つ。
 * 微分音の 2 種（ラスト・バヤーティ）は semis に 1/4 音（.5）を含み、12 平均律では approx（近似）の並びで扱う。
 */
export interface Scale {
  id: string;
  name: string;
  /** 区分: western・eastern-europe・middle-east・pentatonic・symmetric・japan・india・southeast-asia・china */
  group: string;
  /** 別名（日本語・英語・ローマ字）。resolveScale で引ける。 */
  aliases: string[];
  /** 主音からの半音数（昇順。先頭は 0）。微分音は .5 を含む。 */
  semis: number[];
  /** 色彩（ガイドの表のまま）。 */
  note: string;
  /** 向く場面。 */
  scenes: string;
  /** その音階の色が出る進行の例（C 主音、chords 書式）。 */
  chords: string;
  micro?: boolean;
  /** 微分音の音階を 12 平均律で近似した半音数。 */
  approx?: number[];
}

export const SCALES: Scale[] = [
  { id: "ionian", name: "イオニアン", group: "western", aliases: ["major","長調","長音階","イオニアン"], semis: [0,2,4,5,7,9,11], note: "明るい・安定・解決した", scenes: "町・フィールド・勝利", chords: "C Am F G" },
  { id: "dorian", name: "ドリアン", group: "western", aliases: ["ドリアン"], semis: [0,2,3,5,7,9,10], note: "影はあるが前向き・洗練（6度が明るい）", scenes: "旅・古い街・謎の入口", chords: "Cm7 F Cm7 Bb" },
  { id: "phrygian", name: "フリジアン", group: "western", aliases: ["フリジアン"], semis: [0,1,3,5,7,8,10], note: "暗い・異国・不穏（2度が半音下）", scenes: "砂漠・遺跡・ボス前", chords: "Cm Db Cm Bb" },
  { id: "lydian", name: "リディアン", group: "western", aliases: ["リディアン"], semis: [0,2,4,6,7,9,11], note: "浮遊・驚き・神秘（4度が半音上）", scenes: "空・神殿・魔法・妖精", chords: "C D Cmaj7 D" },
  { id: "mixolydian", name: "ミクソリディアン", group: "western", aliases: ["ミクソリディアン"], semis: [0,2,4,5,7,9,10], note: "土の匂いの長調・冒険・ロック（7度が半音下）", scenes: "草原・旅立ち・酒場", chords: "C Bb F C" },
  { id: "aeolian", name: "エオリアン", group: "western", aliases: ["minor","短調","自然短音階","natural-minor","エオリアン"], semis: [0,2,3,5,7,8,10], note: "悲しい・内省", scenes: "別れ・回想・夜", chords: "Cm Ab Bb Cm" },
  { id: "locrian", name: "ロクリアン", group: "western", aliases: ["ロクリアン"], semis: [0,1,3,5,6,8,10], note: "不安定・崩れそう（主和音が dim）", scenes: "一瞬の恐怖・異界。短く挟む", chords: "Cm7b5 Db Cm7b5 Db" },
  { id: "harmonic-minor", name: "ハーモニックマイナー", group: "western", aliases: ["ハーモニックマイナー"], semis: [0,2,3,5,7,8,11], note: "古風・劇的・哀愁（導音あり、6→7が増2度）", scenes: "古城・悲劇・ボスの重み", chords: "Cm Fm G7 Cm" },
  { id: "melodic-minor", name: "メロディックマイナー", group: "western", aliases: ["メロディックマイナー","jazz-minor"], semis: [0,2,3,5,7,9,11], note: "上品な影・魔法的・ジャズの色", scenes: "魔法学院・幻想の夜", chords: "Cm Cm(maj7) F7 Cm" },
  { id: "dorian-b2", name: "ドリアン♭2", group: "western", aliases: ["ドリアン♭2","phrygian-natural6"], semis: [0,1,3,5,7,9,10], note: "暗いが希望の芽・東方の香り", scenes: "神秘の森・古い学び舎", chords: "Cm6 Db Cm6 Bb" },
  { id: "lydian-dominant", name: "リディアン・ドミナント", group: "western", aliases: ["リディアン・ドミナント"], semis: [0,2,4,6,7,9,10], note: "軽やかな冒険・ひねった明るさ", scenes: "空の旅・市場・コミカルな悪役", chords: "C7 D C7 D" },
  { id: "altered", name: "オルタード", group: "western", aliases: ["super-locrian","オルタード","スーパーロクリアン"], semis: [0,1,3,4,6,8,10], note: "緊張の極み・ジャズの毒", scenes: "爆発の直前・ボスの変身", chords: "C7 Db7 C7 Gb7" },
  { id: "lydian-augmented", name: "リディアン・オーグメント", group: "western", aliases: ["リディアン・オーグメント"], semis: [0,2,4,6,8,9,11], note: "超自然・夢の境目", scenes: "異世界の門・天界", chords: "Caug D Caug D" },
  { id: "harmonic-major", name: "ハーモニックメジャー", group: "western", aliases: ["ハーモニックメジャー"], semis: [0,2,4,5,7,8,11], note: "凛々しさ＋切なさ", scenes: "英雄の哀しみ・旅立ちの哀愁", chords: "C Fm G C" },
  { id: "mixolydian-b6", name: "ミクソリディアン♭6", group: "western", aliases: ["melodic-major","ミクソリディアン♭6","メロディックメジャー"], semis: [0,2,4,5,7,8,10], note: "ほろ苦い冒険", scenes: "夕暮れ・旅の別れ", chords: "C Fm Bb C" },
  { id: "ukrainian-dorian", name: "ウクライナ・ドリアン", group: "eastern-europe", aliases: ["dorian-#4","ウクライナ・ドリアン","ドリアン#4"], semis: [0,2,3,6,7,9,10], note: "東欧の哀愁・踊り", scenes: "異国の酒場・流浪の民", chords: "Cm D Cm D" },
  { id: "hungarian-minor", name: "ハンガリアンマイナー", group: "eastern-europe", aliases: ["ハンガリアンマイナー","gypsy-minor"], semis: [0,2,3,6,7,8,11], note: "不穏な優雅・吸血鬼", scenes: "呪われた城・舞踏会", chords: "Cm Ab G Cm" },
  { id: "phrygian-dominant", name: "フリジアン・ドミナント", group: "middle-east", aliases: ["hijaz","hijaz-spanish","spanish","フリジアン・ドミナント","ヒジャーズ","スペイン音階"], semis: [0,1,4,5,7,8,10], note: "異国・情熱・妖しい（1→2が半音、2→3が増2度）", scenes: "砂漠の街・市場・盗賊・フラメンコ", chords: "C Db C Fm" },
  { id: "double-harmonic", name: "ダブルハーモニック", group: "middle-east", aliases: ["byzantine","hijaz-kar","bhairav","gypsy-major","ダブルハーモニック","ビザンチン","ヒジャーズ・カール"], semis: [0,1,4,5,7,8,11], note: "異国の極み・妖艶・劇的（増2度が2か所）", scenes: "邪教・闇市・暗殺者", chords: "C Db Fm C" },
  { id: "major-pentatonic", name: "長調ペンタトニック", group: "pentatonic", aliases: ["pentatonic","長調ペンタトニック","ペンタトニック"], semis: [0,2,4,7,9], note: "素朴・開放・ほっとする", scenes: "村・自然・エンディング", chords: "C Am F G" },
  { id: "minor-pentatonic", name: "短調ペンタトニック", group: "pentatonic", aliases: ["短調ペンタトニック"], semis: [0,3,5,7,10], note: "渋い・ロック・民謡の骨組み", scenes: "戦い・荒野・酒場", chords: "Cm Eb Bb Cm" },
  { id: "blues", name: "ブルース", group: "pentatonic", aliases: ["minor-blues","ブルース","ブルース音階"], semis: [0,3,5,6,7,10], note: "泥臭い・粋・哀愁", scenes: "酒場・裏町・ジャズバー", chords: "C7 F7 C7 G7" },
  { id: "major-blues", name: "長調ブルース", group: "pentatonic", aliases: ["長調ブルース"], semis: [0,2,3,4,7,9], note: "陽気な泥臭さ", scenes: "港・カントリー・祭り", chords: "C7 F7 C7 G7" },
  { id: "whole-tone", name: "全音音階", group: "symmetric", aliases: ["全音音階"], semis: [0,2,4,6,8,10], note: "浮遊・夢・方向感を失う", scenes: "夢・幻惑・時間の歪み", chords: "Caug Daug Caug Daug" },
  { id: "diminished-wh", name: "ディミニッシュ", group: "symmetric", aliases: ["diminished","ディミニッシュ"], semis: [0,2,3,5,6,8,9,11], note: "緊迫・怪奇・出口がない", scenes: "不気味な探索・サスペンス", chords: "Cdim Ebdim Gbdim Adim" },
  { id: "diminished-hw", name: "コンビネーション・オブ・ディミニッシュ", group: "symmetric", aliases: ["dominant-diminished","コンビネーション・オブ・ディミニッシュ"], semis: [0,1,3,4,6,7,9,10], note: "ドミナント上の毒々しい緊張", scenes: "変身・暴走・クライマックス前", chords: "C7 Eb7 Gb7 A7" },
  { id: "messiaen3", name: "メシアン第3旋法", group: "symmetric", aliases: ["メシアン第3旋法","mode3"], semis: [0,2,3,4,6,7,8,10,11], note: "色彩豊か・神秘（ほぼ半音階）", scenes: "星空・天界・儀式", chords: "Cmaj7 Ebmaj7 Cmaj7 Abmaj7" },
  { id: "augmented", name: "オーグメント", group: "symmetric", aliases: ["オーグメント","augmented-hexatonic"], semis: [0,3,4,7,8,11], note: "短3度と半音の交代。不思議", scenes: "魔法・変身", chords: "Cm(maj7) Caug Abmaj7 Caug" },
  { id: "ro", name: "呂音階", group: "japan", aliases: ["yonanuki-major","呂音階","呂","ヨナ抜き長音階","ヨナ抜き"], semis: [0,2,4,7,9], note: "日本的な明るさ・懐かしさ", scenes: "里・田園・昼の村", chords: "C Am7 Dsus4 Gsus4" },
  { id: "ritsu", name: "律音階", group: "japan", aliases: ["律音階","律","chinese-zhi"], semis: [0,2,5,7,9], note: "雅・おだやか・古風", scenes: "神社・宮廷・静かな村", chords: "Csus2 Fsus2 Csus2 Gsus4" },
  { id: "minyo", name: "民謡音階", group: "japan", aliases: ["min-yo","民謡音階"], semis: [0,3,5,7,10], note: "素朴な哀愁（骨組みは C–F と G–C の4度。出典未確認）", scenes: "祭り・民家・収穫", chords: "Cm7 Fsus2 Cm7 Bbsus2" },
  { id: "miyako", name: "都節音階", group: "japan", aliases: ["miyako-bushi","in","in-scale","都節音階","都節","陰音階","陰旋法","インスケール"], semis: [0,1,5,7,8], note: "哀愁・影・日本的な暗さ", scenes: "夜・忍び・悲恋", chords: "Csus4 Db Csus4 Fm" },
  { id: "hirajoshi", name: "平調子", group: "japan", aliases: ["kumoi","yonanuki-minor","平調子","ヨナ抜き短音階","雲井"], semis: [0,2,3,7,8], note: "切なさ・やわらかい暗さ", scenes: "別れ・月夜・回想", chords: "Cm Ab Gsus4 Cm" },
  { id: "ryukyu", name: "琉球音階", group: "japan", aliases: ["okinawa","琉球音階","琉球"], semis: [0,4,5,7,11], note: "南国の明るさ・異国的（長3度と半音が目立つ）", scenes: "海辺・島・のどかな旅", chords: "Cmaj7 Fsus2 Cmaj7 Em" },
  { id: "iwato", name: "岩戸", group: "japan", aliases: ["岩戸"], semis: [0,1,5,6,10], note: "神秘・不穏・祈り（増4度が入る）", scenes: "封印・祭壇・夜の社", chords: "Fsus4 Gb Fsus4 Bbm" },
  { id: "insen", name: "陰音階の変種", group: "japan", aliases: ["陰音階の変種","インセン"], semis: [0,1,5,7,10], note: "厳しい哀しみ・修行", scenes: "山寺・修験・滝", chords: "Csus4 Fsus2 Csus4 Bbm" },
  { id: "todi", name: "ラーガ系 トーディ", group: "india", aliases: ["todi-thaat","トーディ","ラーガ系トーディ"], semis: [0,1,3,6,7,8,11], note: "重く悲しい・瞑想", scenes: "古代寺院・深い洞窟", chords: "Cm Db Cm Cm" },
  { id: "marva", name: "ラーガ系 マールヴァ", group: "india", aliases: ["marwa","マールヴァ","ラーガ系マールヴァ"], semis: [0,1,4,6,7,9,11], note: "緊張を含んだ夕暮れ", scenes: "黄昏の遺跡", chords: "C Db C Db" },
  { id: "pelog", name: "ペログ", group: "southeast-asia", aliases: ["ペログ"], semis: [0,1,3,7,8], note: "揺れる・水・儀式（実際の調律は楽器ごとに異なる）", scenes: "寺院・南海の祭", chords: "Cm Db Cm Ab" },
  { id: "slendro", name: "スレンドロ", group: "southeast-asia", aliases: ["スレンドロ"], semis: [0,2,5,7,9], note: "明るく平らな金属の響き（実際は5等分に近い）", scenes: "熱帯・儀式", chords: "Csus2 Fsus2 Csus2 Fsus2" },
  { id: "shang", name: "商調", group: "china", aliases: ["商調","シャン"], semis: [0,2,5,7,10], note: "透明なsus感・空のような", scenes: "山水・仙人・霧", chords: "Csus4 Bb Csus4 Fsus2" },
  { id: "jue", name: "角調", group: "china", aliases: ["角調","ジュエ"], semis: [0,3,5,8,10], note: "影のある静けさ", scenes: "夜の庭・書院", chords: "Cm7 Ab Cm7 Fm7" },
  { id: "rast", name: "ラスト", group: "middle-east", aliases: ["ラスト"], semis: [0,2,3.5,5,7,9,10.5], note: "上品・堂々・開いた長調風", scenes: "宮殿・市場の広場", chords: "", micro: true, approx: [0, 2, 4, 5, 7, 9, 11] },
  { id: "bayati", name: "バヤーティ", group: "middle-east", aliases: ["バヤーティ","bayat"], semis: [0,1.5,3,5,7,8,10], note: "親密・哀愁・歌心", scenes: "夜の街・語り", chords: "", micro: true, approx: [0, 1, 3, 5, 7, 8, 10] },
];

/** 音名の表（フラット表記。ガイドの表と同じ綴り）。 */
const PC_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
const PC_OF: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** 音名（"D"・"Bb"・"F#"・オクターブつきも可）→ 0〜11。読めなければ null。 */
export function pitchClassOf(name: string): number | null {
  const m = /^([A-Ga-g])([#b]?)(-?\d+)?$/.exec(name.trim());
  if (!m) return null;
  return (PC_OF[m[1].toUpperCase()] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 120) % 12;
}
export const pitchClassName = (pc: number): string => PC_NAMES[((pc % 12) + 12) % 12];

const byKey = new Map<string, Scale>();
for (const s of SCALES) {
  byKey.set(s.id.toLowerCase(), s);
  byKey.set(s.name.toLowerCase(), s);
  for (const a of s.aliases) byKey.set(a.toLowerCase(), s);
}

/** 名前（id・日本語名・別名）から音階を探す。 */
export function findScale(name: string): Scale | undefined {
  return byKey.get(name.trim().toLowerCase());
}

/** "miyako@D"・"都節@D"・"hirajoshi"（主音は省略可＝C）を、音階と主音（0〜11）にする。読めなければ null。 */
export function resolveScale(spec: string, tonic?: string): { scale: Scale; tonic: number } | null {
  const [n, t] = spec.split("@");
  const scale = findScale(n);
  if (!scale) return null;
  const tn = t ?? tonic;
  const tpc = tn === undefined || tn === "" ? 0 : pitchClassOf(tn);
  if (tpc === null) return null;
  return { scale, tonic: tpc };
}

/** 12 平均律で鳴らす半音数（微分音の音階は approx）。 */
export const scaleSemis = (scale: Scale): number[] => scale.approx ?? scale.semis;

/** 主音を tonic（0〜11）にしたときの、音階の音（0〜11、昇順に並べた集合）。 */
export function scalePitchClasses(scale: Scale, tonic = 0): number[] {
  return [...new Set(scaleSemis(scale).map((s) => (Math.round(s) + tonic) % 12))].sort((a, b) => a - b);
}

/** 音階の特性音（主音からの半音数）。西洋の旋法は手で決めた。ほかは「半音の動きの上側の音（主音を除く）」。 */
const CHARACTERISTIC: Record<string, number[]> = {
  ionian: [], aeolian: [], dorian: [9], phrygian: [1], lydian: [6], mixolydian: [10], locrian: [1, 6],
  "harmonic-minor": [11], "melodic-minor": [9, 11], "dorian-b2": [1], "lydian-dominant": [6, 10], altered: [1, 4], "lydian-augmented": [6, 8],
  "harmonic-major": [8], "mixolydian-b6": [8], "ukrainian-dorian": [6], "hungarian-minor": [6, 11], "phrygian-dominant": [1, 4], "double-harmonic": [1, 4],
  "major-pentatonic": [], "minor-pentatonic": [], "major-blues": [], ro: [], minyo: [], ritsu: [], slendro: [],
  blues: [6], "whole-tone": [], "diminished-wh": [], "diminished-hw": [], messiaen3: [], augmented: [],
};
export function characteristicSemis(scale: Scale): number[] {
  if (CHARACTERISTIC[scale.id]) return CHARACTERISTIC[scale.id];
  const s = scaleSemis(scale).map(Math.round);
  const out: number[] = [];
  for (let i = 1; i < s.length; i++) if (s[i] - s[i - 1] === 1) out.push(s[i]);
  return out;
}

export type SnapPolicy = "nearest" | "down" | "up";

/** 1 音を音階の音にそろえる。音階内ならそのまま返す。nearest で同じ近さなら下へ。 */
export function snapNote(name: string, scale: Scale, tonic = 0, policy: SnapPolicy = "nearest"): string {
  const midi = noteNameToMidi(name);
  const set = new Set(scalePitchClasses(scale, tonic));
  if (set.has(midi % 12)) return name;
  let down = 0;
  let up = 0;
  while (!set.has((midi - down + 120) % 12)) down++;
  while (!set.has((midi + up) % 12)) up++;
  const m = policy === "down" ? midi - down : policy === "up" ? midi + up : down <= up ? midi - down : midi + up;
  return `${PC_NAMES[m % 12]}${Math.floor(m / 12) - 1}`;
}

/**
 * notes の文字列の音名を、音階の音にそろえる。拍の数と、奏法の記号（! , ' _ ~ ^ / \ *）・休符 R・ドラムのグリッドはそのまま残す。
 * 書き換えた音の綴りはフラット表記（Db・Eb・Gb・Ab・Bb）。
 */
export function snapNotesToScale(text: string, scale: Scale, tonic = 0, policy: SnapPolicy = "nearest"): string {
  return text
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((token) => {
      const i = token.indexOf(":");
      const name = i < 0 ? token : token.slice(0, i);
      if (!/^[A-G][b#]?-?\d+$/.test(name)) return token;
      return snapNote(name, scale, tonic, policy) + (i < 0 ? "" : token.slice(i));
    })
    .join(" ");
}

/** 和音の種類（読める名前）。7sus4・5 は、完全に収まる和音の表（ガイド 2-3）に合わせて既定では数えない。 */
export const CHORD_QUALITIES = ["", "m", "dim", "aug", "sus2", "sus4", "7", "maj7", "m7", "m7b5", "dim7", "6", "m6", "add9", "madd9", "maj9", "m9", "9", "m(maj7)"];

/** 構成音がすべて音階に入る和音を、根音ごとに列挙する（根音の並びは音階順、種類は CHORD_QUALITIES の順）。 */
export function chordsInScale(scale: Scale, tonic = 0, qualities: string[] = CHORD_QUALITIES): string[] {
  const pcs = scalePitchClasses(scale, tonic);
  const set = new Set(pcs);
  const out: string[] = [];
  for (const root of pcs) {
    for (const q of qualities) {
      const name = pitchClassName(root) + q;
      const c = parseChord(name);
      if (c && c.intervals.every((iv) => set.has((root + iv) % 12))) out.push(name);
    }
  }
  return out;
}

const TRIADS: [string, number[]][] = [["", [0, 4, 7]], ["m", [0, 3, 7]], ["dim", [0, 3, 6]], ["aug", [0, 4, 8]]];
const SEVENTHS: [string, number[]][] = [["maj7", [0, 4, 7, 11]], ["7", [0, 4, 7, 10]], ["m7", [0, 3, 7, 10]], ["m7b5", [0, 3, 6, 10]], ["dim7", [0, 3, 6, 9]], ["m(maj7)", [0, 3, 7, 11]], ["maj7#5", [0, 4, 8, 11]]];

export interface HarmonizedChord {
  /** 度数（1〜7）。 */
  degree: number;
  /** 和音名（例 "Dm7"）。うちの書式で読めない種類は "Ebmaj7#5" のように書き、readable が false。 */
  name: string;
  /** 構成音（0〜11）。 */
  pcs: number[];
  readable: boolean;
}

/** 7 音の音階を 3 度ずつ積んだ和音（三和音／四和音）。7 音でなければ空。名前が決まらない積み方は name が "?"。 */
export function harmonize(scale: Scale, tonic = 0, size: 3 | 4 = 3): HarmonizedChord[] {
  const s = scaleSemis(scale).map(Math.round);
  if (s.length !== 7) return [];
  return s.map((_, i) => {
    const idx = size === 3 ? [0, 2, 4] : [0, 2, 4, 6];
    const rel = idx.map((k) => (s[(i + k) % 7] + (i + k >= 7 ? 12 : 0) - s[i] + 120) % 12);
    const table = size === 3 ? TRIADS : SEVENTHS;
    const hit = table.find(([, iv]) => iv.length === rel.length && iv.every((v, j) => v === rel[j]));
    const root = (s[i] + tonic) % 12;
    const name = hit ? pitchClassName(root) + hit[0] : "?";
    return { degree: i + 1, name, pcs: rel.map((r) => (root + r) % 12), readable: hit ? parseChord(name) !== null : false };
  });
}
