/**
 * パート別ミックスの設計（音量の目標・EQ・圧縮・残響の量）。
 * 作曲ソフトの曲を、パート（ドラム・ベース・ギター・鍵盤・弦…）ごとに別々に音にして、パートごとに音をととのえてから合わせるための表。
 * ここは計算とデータだけ（音を出す処理は tools/composer/render-node.mjs）。
 */

export type Group = "drums" | "bass" | "gtrRhythm" | "gtrLead" | "gtrClean" | "keys" | "orch" | "pad" | "lead" | "ethnic" | "perc" | "ambience";
export const GROUPS: readonly Group[] = ["drums", "bass", "gtrRhythm", "gtrLead", "gtrClean", "keys", "orch", "pad", "lead", "ethnic", "perc", "ambience"];

/** 楽器の音色（Instrument）→ パートの種類。 */
export function groupOf(instrument: string | undefined): Group {
  switch (instrument) {
    case "kick": case "snare": case "hihat": case "crash": case "tom":
      return "drums";
    case "bass": case "slap": case "sub808":
      return "bass";
    case "crunch": case "distGuitar":
      return "gtrRhythm";
    case "leadGuitar":
      return "gtrLead";
    case "guitar": case "echoGuitar":
      return "gtrClean";
    case "keys": case "piano": case "harpsichord": case "bell": case "chime":
      return "keys";
    case "strings": case "brass":
      return "orch";
    case "pad": case "choir":
      return "pad";
    case "lead":
      return "lead";
    case "sitar": case "koto": case "shamisen": case "banjo": case "harp": case "kalimba": case "panflute": case "shakuhachi": case "ocarina": case "fiddle": case "bagpipe":
      return "ethnic";
    case "cowbell":
      return "perc";
    case "wind": case "rain": case "stream": case "bird": case "crickets": case "sfxDown": case "sfxUp": case "impact": case "swoosh": case "pierce":
      return "ambience";
    default:
      return "lead";
  }
}

export interface Eq {
  /** 中心周波数（Hz）。 */
  f: number;
  /** 増減（dB）。 */
  g: number;
  /** 幅（Q）。 */
  q: number;
}
export interface Comp {
  /** しきい値（dBFS）。 */
  threshold: number;
  ratio: number;
  /** ミリ秒。 */
  attack: number;
  release: number;
}
export interface GroupMix {
  /** 音量の目標（dBFS。パートを鳴っている間だけ測ったRMS）。 */
  target: number;
  /** 低域をカットする周波数（Hz）。 */
  hp: number;
  /** 高域をカットする周波数（Hz）。 */
  lp: number;
  eq: Eq[];
  comp: Comp | null;
  /** 残響への送りの量（0〜1）。 */
  reverb: number;
  /** やまびこ（ディレイ）への送りの量（0〜1）と、間隔（拍に合わせるため、呼び出し側で決める）。 */
  delay: number;
  /** 飽和（歪み）を少し足す量（0〜1）。 */
  warmth: number;
  /** 左右の広がり（1が元のまま、1.3で広く、0で中央に寄せる）。 */
  width: number;
}

const BASE: Record<Group, GroupMix> = {
  drums:     { target: -21, hp: 30,  lp: 17000, eq: [{ f: 320, g: -2.5, q: 1 }, { f: 5000, g: 2, q: 0.8 }], comp: { threshold: -22, ratio: 3, attack: 12, release: 120 }, reverb: 0.1, delay: 0, warmth: 0.1, width: 1 },
  bass:      { target: -22, hp: 35,  lp: 4500,  eq: [{ f: 90, g: 2, q: 1 }, { f: 300, g: -2, q: 1 }, { f: 1500, g: 1.5, q: 1 }], comp: { threshold: -24, ratio: 4, attack: 20, release: 160 }, reverb: 0, delay: 0, warmth: 0.25, width: 0.1 },
  gtrRhythm: { target: -24, hp: 85,  lp: 9000,  eq: [{ f: 250, g: -3, q: 1 }, { f: 2800, g: 2, q: 1 }], comp: { threshold: -22, ratio: 2.5, attack: 25, release: 140 }, reverb: 0.05, delay: 0, warmth: 0.2, width: 1.15 },
  gtrLead:   { target: -23, hp: 150, lp: 11000, eq: [{ f: 400, g: -2, q: 1 }, { f: 3200, g: 2, q: 1 }], comp: { threshold: -24, ratio: 3, attack: 15, release: 130 }, reverb: 0.2, delay: 0.14, warmth: 0.1, width: 1 },
  gtrClean:  { target: -26, hp: 110, lp: 11000, eq: [{ f: 300, g: -2, q: 1 }, { f: 4000, g: 1.5, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 20, release: 140 }, reverb: 0.2, delay: 0.1, warmth: 0, width: 1.2 },
  keys:      { target: -26, hp: 100, lp: 12000, eq: [{ f: 350, g: -2, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 25, release: 160 }, reverb: 0.2, delay: 0, warmth: 0, width: 1.1 },
  orch:      { target: -26, hp: 120, lp: 11000, eq: [{ f: 300, g: -2, q: 1 }, { f: 5500, g: 1, q: 0.8 }], comp: { threshold: -26, ratio: 2, attack: 30, release: 200 }, reverb: 0.4, delay: 0, warmth: 0, width: 1.3 },
  pad:       { target: -29, hp: 150, lp: 9000,  eq: [{ f: 300, g: -3, q: 1 }, { f: 5000, g: 1.5, q: 0.8 }], comp: null, reverb: 0.45, delay: 0, warmth: 0, width: 1.3 },
  lead:      { target: -23, hp: 200, lp: 12000, eq: [{ f: 400, g: -2, q: 1 }, { f: 3000, g: 1.5, q: 1 }], comp: { threshold: -25, ratio: 2.5, attack: 15, release: 120 }, reverb: 0.25, delay: 0.1, warmth: 0, width: 1 },
  ethnic:    { target: -26, hp: 150, lp: 12000, eq: [{ f: 350, g: -2, q: 1 }], comp: { threshold: -26, ratio: 2, attack: 15, release: 140 }, reverb: 0.25, delay: 0, warmth: 0, width: 1.1 },
  perc:      { target: -30, hp: 300, lp: 12000, eq: [], comp: null, reverb: 0.1, delay: 0, warmth: 0, width: 1 },
  ambience:  { target: -34, hp: 100, lp: 10000, eq: [], comp: null, reverb: 0.3, delay: 0, warmth: 0, width: 1.4 },
};

/** 曲調ごとの、パートの音量の補正（dB）。重い曲調ではギターとドラムを前に、静かな曲調ではやわらかく。 */
const STYLE_OFFSET: Partial<Record<string, Partial<Record<Group, number>>>> = {
  metal: { drums: 1, gtrRhythm: 2, bass: 0.5, keys: -2, pad: -2 },
  deathmetal: { drums: 1.5, gtrRhythm: 2.5, bass: 0.5, keys: -3, pad: -3 },
  hardcore: { drums: 1, gtrRhythm: 2, bass: 1, keys: -3, pad: -3 },
  progmetal: { drums: 0.5, gtrRhythm: 1.5, keys: 0.5 },
  rock: { gtrRhythm: 1, drums: 0.5 },
  dancerock: { drums: 1, bass: 1, gtrRhythm: 0.5 },
  electro: { drums: 1.5, bass: 1.5, pad: 1, gtrRhythm: -2 },
  phonk: { drums: 1, bass: 3, perc: 3, pad: -2 },
  cleandance: { drums: 1, bass: 1.5 },
  classic: { orch: 3, keys: 2, drums: -4, bass: -2 },
  baroque: { keys: 3, orch: 2 },
  jazz: { drums: -2, bass: 1, keys: 1 },
  epic: { orch: 3, drums: 1, pad: 1 },
  space: { pad: 4, ambience: 3 },
  nature: { ambience: 6 },
  cafe: { keys: 2, drums: -2 },
};

/** 曲調・味つけから、パートごとのミックス設計を作る。 */
export function mixPlan(style: string | undefined, flavors: readonly string[] = []): Record<Group, GroupMix> {
  const plan = {} as Record<Group, GroupMix>;
  for (const g of GROUPS) plan[g] = { ...BASE[g], eq: BASE[g].eq.map((e) => ({ ...e })), comp: BASE[g].comp ? { ...BASE[g].comp! } : null };
  const off = (style && STYLE_OFFSET[style]) || {};
  for (const g of GROUPS) plan[g].target += off[g] ?? 0;
  // 味つけ: ラウド＝ギターを太く前に、オーケストラ＝弦とブラスを前に、和楽器＝和楽器を前に
  if (flavors.includes("loud")) {
    plan.gtrRhythm.target += 1.5;
    plan.gtrRhythm.warmth = Math.min(1, plan.gtrRhythm.warmth + 0.2);
    plan.drums.target += 1;
  }
  if (flavors.includes("orchestra")) {
    plan.orch.target += 3;
    plan.pad.target += 1;
  }
  if (flavors.includes("wagakki")) plan.ethnic.target += 4;
  return plan;
}

const f2 = (n: number): string => (Math.round(n * 100) / 100).toString();
const dbToLin = (db: number): number => Math.pow(10, db / 20);

/** 1パートぶんの FFmpeg フィルター（音をととのえる部分）。入力と出力のラベルは呼び出し側がつける。 */
export function dryChain(m: GroupMix): string {
  const f: string[] = [];
  f.push(`highpass=f=${f2(m.hp)}`);
  f.push(`lowpass=f=${f2(m.lp)}`);
  for (const e of m.eq) f.push(`equalizer=f=${f2(e.f)}:t=q:w=${f2(e.q)}:g=${f2(e.g)}`);
  if (m.warmth > 0) {
    // やわらかい飽和（真空管のような倍音）。入力を持ち上げて tanh で丸め、戻す
    const pre = 1 + m.warmth * 2.5;
    f.push(`volume=${f2(pre)}`, "asoftclip=type=tanh", `volume=${f2(1 / pre)}`);
  }
  if (m.comp) f.push(`acompressor=threshold=${f2(dbToLin(m.comp.threshold))}:ratio=${f2(m.comp.ratio)}:attack=${f2(m.comp.attack)}:release=${f2(m.comp.release)}:makeup=1`);
  if (m.width !== 1) f.push(`extrastereo=m=${f2(m.width)}:c=0`);
  return f.join(",");
}

/**
 * 音量の合わせ方: パートを鳴っている間だけ測ったRMS（dBFS）が目標になるような倍率（dB）。
 * 鳴っていない（ほぼ無音の）パートは null。ゲインは ±18dB に収める（極端な増幅でノイズを持ち上げない）。
 */
export function gainForTarget(measuredDb: number | null, targetDb: number): number | null {
  if (measuredDb === null || !Number.isFinite(measuredDb)) return null;
  return Math.max(-18, Math.min(18, targetDb - measuredDb));
}

/** 鳴っている間だけのRMS（dBFS）。無音の窓（-60dBFS未満）は数えない。鳴っていなければ null。 */
export function activeRmsDb(left: Float32Array, right: Float32Array, sampleRate: number, windowSec = 0.4): number | null {
  const win = Math.max(1, Math.floor(sampleRate * windowSec));
  let sum = 0;
  let count = 0;
  for (let i = 0; i + win <= left.length; i += win) {
    let s = 0;
    for (let j = i; j < i + win; j++) s += left[j] * left[j] + right[j] * right[j];
    const rms = Math.sqrt(s / (2 * win));
    if (rms > 0.001) {
      sum += s / (2 * win);
      count++;
    }
  }
  if (count === 0) return null;
  return 10 * Math.log10(sum / count);
}
