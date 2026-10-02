import type { Flavor, Style } from "./songwriter";

/**
 * スタイル指定の文章（"melodic metal, twin guitars, 150 BPM, E minor" や「ロック×和楽器、疾走感」など）から、
 * 作曲エンジン（songwriter.ts）の設計図に必要な「曲調・味つけ・テンポ・拍子・調」を決める。
 * 日本語・英語どちらのキーワードも読める。決まらなかった項目は、曲調ごとの標準値を使う。
 * APIキーや外部サービスは使わない（ただの言葉の照らし合わせ）。
 */

export interface StyleChoice {
  style: Style;
  /** 重ねる味つけ（ラウド・オーケストラ・和楽器）。 */
  flavors: Flavor[];
  bpm: number;
  beats: 3 | 4 | 7;
  tonic: string;
  minor: boolean;
  /** 何の言葉から、何を決めたか（確認用）。 */
  matched: string[];
  /** 注意（味つけが使えない拍子など）。 */
  warnings: string[];
}

interface Defaults {
  bpm: number;
  tonic: string;
  minor: boolean;
  beats?: 3 | 4 | 7;
}

/** 曲調ごとの標準値（テンポ・主音・長短）。 */
export const STYLE_DEFAULTS: Partial<Record<Style, Defaults>> = {
  rock: { bpm: 132, tonic: "E", minor: true },
  metal: { bpm: 165, tonic: "E", minor: true },
  deathmetal: { bpm: 190, tonic: "C#", minor: true },
  hardcore: { bpm: 180, tonic: "D", minor: true },
  progmetal: { bpm: 150, tonic: "E", minor: true, beats: 7 },
  phonk: { bpm: 140, tonic: "F", minor: true },
  dancerock: { bpm: 128, tonic: "A", minor: true },
  epic: { bpm: 112, tonic: "D", minor: true },
  jpop: { bpm: 128, tonic: "C", minor: false },
  electro: { bpm: 128, tonic: "A", minor: true },
  cleandance: { bpm: 124, tonic: "C", minor: false },
  jazz: { bpm: 120, tonic: "F", minor: false },
  rnb: { bpm: 92, tonic: "Bb", minor: true },
  samba: { bpm: 100, tonic: "C", minor: false },
  folk: { bpm: 100, tonic: "G", minor: false },
  space: { bpm: 72, tonic: "A", minor: true },
  cafe: { bpm: 88, tonic: "F", minor: false },
  nature: { bpm: 70, tonic: "G", minor: false },
  classic: { bpm: 100, tonic: "D", minor: false },
  baroque: { bpm: 112, tonic: "D", minor: true },
};

// 上から順に最初に合ったものを採用する（重い・具体的なジャンルを先に置く）。
// ロックは、「electronic drums」「soulful」などの飾りの言葉でほかの曲調に取られないよう、エレクトロ・ソウル系より前に置く。
const STYLE_RULES: { re: RegExp; style: Style; label: string }[] = [
  { re: /death\s*-?\s*metal|デス\s*メタル|growl|グロウル|ガテラル|blast\s*-?\s*beat|ブラストビート/i, style: "deathmetal", label: "デスメタル" },
  { re: /hard\s*-?\s*core|ハードコア|gang\s*vocal|ギャングボーカル/i, style: "hardcore", label: "ハードコア" },
  { re: /\bprog(ressive)?\s*-?\s*(metal|rock)\b|\bprog\b|プログレ|変拍子|odd\s*-?\s*(meter|time)|\b7\s*\/\s*[48]\b/i, style: "progmetal", label: "プログレ（7拍子）" },
  { re: /phonk|フォンク|cow\s*bell|カウベル/i, style: "phonk", label: "フォンク" },
  { re: /dance\s*-?\s*rock|ダンス\s*[×x✕・＋+]?\s*ロック|electro\s*-?\s*rock|エレクトロ\s*ロック/i, style: "dancerock", label: "ダンス×ロック" },
  { re: /metal|メタル|djent|thrash|スラッシュ/i, style: "metal", label: "メタル" },
  { re: /rock|ロック|punk|パンク|grunge|グランジ/i, style: "rock", label: "ロック" },
  { re: /samba|サンバ|bossa|ボサノバ/i, style: "samba", label: "サンバ・ボサノバ" },
  { re: /jazz|ジャズ|swing|スウィング/i, style: "jazz", label: "ジャズ" },
  { re: /\br\s*&\s*b\b|\brnb\b|\bsoul\b|ソウル|\bfunk\b|ファンク|hip\s*-?\s*hop|ヒップホップ|\btrap\b|トラップ/i, style: "rnb", label: "R&B・ソウル・ヒップホップ" },
  { re: /\bedm\b|electro|エレクトロ|techno|テクノ|trance|トランス|house|ハウス|synth\s*-?\s*wave|シンセウェイブ/i, style: "electro", label: "エレクトロニック" },
  { re: /dance|ダンス|disco|ディスコ/i, style: "cleandance", label: "ダンス" },
  { re: /j\s*-?\s*pop|ポップ|\bpop\b|アイドル|anime|アニソン/i, style: "jpop", label: "ポップ" },
  { re: /baroque|バロック/i, style: "baroque", label: "バロック" },
  { re: /classic(al)?|クラシック|piano|ピアノ/i, style: "classic", label: "クラシック" },
  { re: /folk|フォーク|acoustic|アコースティック|country|カントリー|celtic|ケルト|world|ワールド|民族|ethnic/i, style: "folk", label: "フォーク・ワールド" },
  { re: /ambient|アンビエント|drone|ドローン|space|宇宙/i, style: "space", label: "アンビエント" },
  { re: /lo\s*-?\s*fi|ローファイ|cafe|カフェ|chill|チル/i, style: "cafe", label: "ローファイ・カフェ" },
  { re: /nature|自然|forest|森/i, style: "nature", label: "自然音" },
  { re: /epic|エピック|cinematic|シネマティック|soundtrack|サウンドトラック|劇伴|film\s*score|battle|boss/i, style: "epic", label: "劇伴・エピック" },
];

const FLAVOR_RULES: { re: RegExp; flavor: Flavor; label: string }[] = [
  { re: /loud|ラウド/i, flavor: "loud", label: "ラウド" },
  { re: /orchestra|オーケストラ|symphon|シンフォニック|strings\s*(&|and)\s*brass|管弦楽/i, flavor: "orchestra", label: "オーケストラ" },
  { re: /wagakki|和楽器|shamisen|三味線|koto|琴|箏|shakuhachi|尺八|taiko|和太鼓|japanese\s*traditional|和風/i, flavor: "wagakki", label: "和楽器" },
];

const clamp = (n: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, n));
const FLAT: Record<string, string> = { "♭": "b", "♯": "#" };

/** "E minor"・"Em"・"F# major"・"ホ短調" のような調の指定を読む。 */
export function parseKey(text: string): { tonic: string; minor: boolean } | null {
  const t = text.normalize("NFKC");
  const m = /\b([A-G][#b♭♯]?)\s*[- ]?\s*(minor|min|major|maj|m)\b(?!\w)/i.exec(t) ?? /\b([A-G][#b]?)(m)(?![a-z])/.exec(t);
  if (m) {
    const tonic = m[1][0].toUpperCase() + (FLAT[m[1][1]] ?? m[1][1] ?? "");
    const kind = m[2].toLowerCase();
    return { tonic, minor: kind === "m" ? m[2] === "m" : kind.startsWith("min") };
  }
  const j = /([A-G])\s*(マイナー|短調)|([A-G])\s*(メジャー|長調)/.exec(t);
  if (j) return j[1] ? { tonic: j[1], minor: true } : { tonic: j[3], minor: false };
  return null;
}

/** "150 BPM"・"BPM 150"・「テンポ150」からテンポを読む。 */
export function parseBpm(text: string): number | null {
  const t = text.normalize("NFKC");
  const m = /(\d{2,3})\s*bpm/i.exec(t) ?? /bpm\s*[:=]?\s*(\d{2,3})/i.exec(t) ?? /テンポ\s*[:=]?\s*(\d{2,3})/.exec(t);
  return m ? clamp(Number(m[1]), 50, 220) : null;
}

export interface StyleOverrides {
  /** 設計図（songs.json）で決まっているテンポ。あれば文章より優先する。 */
  bpm?: number;
  /** 設計図で決まっている調（"E minor" など）。 */
  keyScale?: string;
  /** 設計図で決まっている拍子（"4"・"7" など）。 */
  timeSignature?: string | number;
}

export function parseStylePrompt(text: string, overrides: StyleOverrides = {}): StyleChoice {
  const t = text.normalize("NFKC");
  const matched: string[] = [];
  const warnings: string[] = [];

  const flavors: Flavor[] = [];
  for (const r of FLAVOR_RULES) {
    if (r.re.test(t)) {
      flavors.push(r.flavor);
      matched.push(`味つけ: ${r.label}`);
    }
  }

  let style: Style | null = null;
  for (const r of STYLE_RULES) {
    if (r.re.test(t)) {
      style = r.style;
      matched.push(`曲調: ${r.label}`);
      break;
    }
  }
  // 「ロック×オーケストラ」「ロック×和楽器」のように味つけだけが決まったときは、土台をロックにする。
  // 「オーケストラ」だけのときは、劇伴（エピック）にする。「ラウド」だけのときは、ロックにする。
  if (!style) {
    if (flavors.includes("orchestra") && flavors.length === 1) {
      style = "epic";
      flavors.splice(flavors.indexOf("orchestra"), 1);
      matched.push("曲調: 劇伴・エピック（オーケストラのみの指定）");
    } else {
      style = "rock";
      matched.push("曲調: ロック（土台の指定がなかったため）");
    }
  }

  const d = STYLE_DEFAULTS[style] ?? { bpm: 120, tonic: "C", minor: false };
  const keyText = overrides.keyScale ? parseKey(overrides.keyScale) : null;
  const key = keyText ?? parseKey(text) ?? { tonic: d.tonic, minor: d.minor };
  const bpm = clamp(overrides.bpm ?? parseBpm(text) ?? d.bpm, 50, 220);
  let beats: 3 | 4 | 7 = d.beats ?? 4;
  const sig = overrides.timeSignature !== undefined ? Number(String(overrides.timeSignature).split("/")[0]) : null;
  if (sig === 3 || sig === 4 || sig === 7) beats = style === "progmetal" ? 7 : sig;
  if (style === "progmetal") beats = 7; // プログレ曲調は7拍子の型だけを持つ
  if (beats !== 4 && flavors.some((f) => f !== "loud")) {
    warnings.push(`オーケストラ・和楽器の重ねは、4拍子の曲だけに使えます（この曲は${beats}拍子のため、ラウド以外の味つけは付きません）。`);
  }
  return { style, flavors, bpm, beats, tonic: key.tonic, minor: key.minor, matched, warnings };
}
