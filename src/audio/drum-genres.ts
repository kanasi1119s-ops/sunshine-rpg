/**
 * ジャンル別のドラムの設定表と、ドラムの型を作る小さな道具（docs/sound/drum-genre-guide.md の §2・§7 を実装）。
 * - DRUM_GENRES: ジャンルごとの drumMix・ドラム音源（--drums）・swing・human・ベース音源・目安のテンポ・16分の型。曲JSONの drumMix にそのまま展開できる。
 * - swingFromPercent / jazzSwingForBpm: swing の換算。
 * - blastPattern / gallop / breakdownHalftime / limitDensity: メタルの型。速いテンポでは 16分を 8分に落とす。
 * - trapRoll: トラップのハイハットのロール（拍つき表記）。
 * - hihatPattern: ハイハットの強弱の型を小節ごとに回して返す。
 * - placeGhosts: スネアのゴーストノートを置く位置（キックと同時・バックビートの直前を除き、3つ続けない）。
 * 型は、ジャンルの一般的な基本形を16分の位置に置き直したもので、特定の曲の写しではない（CLAUDE.md 1-1）。
 */
import type { Score } from "./score";

export type DrumMix = NonNullable<Score["drumMix"]>;
export interface DrumGrooveGrids { kick: string; snare: string; hat: string }
export interface DrumGenre {
  id: string;
  label: string;
  /** 曲JSONの drumMix にそのまま入れられる。 */
  drumMix: DrumMix;
  /** `--drums` の音源（std・muldjord・rock・metal・jazz・jpop・supra）。 */
  drums: "std" | "muldjord" | "rock" | "metal" | "jazz" | "jpop" | "supra";
  /** `--bass` の音源（std・finger・pick・rock・metal・jazz・jpop）。bassline-guide.md §6 に対応。 */
  bass: "std" | "finger" | "pick" | "rock" | "metal" | "jazz" | "jpop";
  /** swing（曲全体）。範囲のときは [遅いテンポ側, 速いテンポ側]。 */
  swing: number | [number, number];
  human: number;
  bpm: [number, number];
  /** 基本の1小節の型（16マス）。 */
  grids: DrumGrooveGrids;
}

const G = (kick: string, snare: string, hat: string): DrumGrooveGrids => ({ kick, snare, hat });

export const DRUM_GENRES: Record<string, DrumGenre> = {
  rock: { id: "rock", label: "ロック", drumMix: { hat: { level: 0.8, pan: -0.3 }, snare: { reverb: 0.2 }, tom: { spread: 0.7, tune: -2 }, crash: { level: 0.9, pan: 0.3, reverb: 0.2 } }, drums: "rock", bass: "pick", swing: 0, human: 0.35, bpm: [100, 140], grids: G("X.......X.x.....", "....X.......X...", "X.x.X.x.X.x.X.x.") },
  hardrock: { id: "hardrock", label: "ハードロック", drumMix: { kick: { level: 1.1 }, hat: { level: 0.8, pan: -0.3 }, snare: { reverb: 0.25, tune: -1 }, tom: { spread: 0.7, tune: -3 }, crash: { level: 1.0, reverb: 0.25 } }, drums: "rock", bass: "rock", swing: 0, human: 0.3, bpm: [70, 110], grids: G("X.......x.x.....", "........X.......", "x.x.x.x.x.x.x.x.") },
  punk: { id: "punk", label: "パンク", drumMix: { hat: { level: 1.0, pan: -0.3 }, snare: { level: 1.1, tune: 1, reverb: 0.15 }, tom: { spread: 0.6, tune: -3 }, crash: { level: 1.0, pan: 0.3, reverb: 0.25 } }, drums: "rock", bass: "pick", swing: 0, human: 0.4, bpm: [150, 210], grids: G("x...x...x...x...", "..x...x...x...x.", "x.X.x.X.x.X.x.X.") },
  metal: { id: "metal", label: "メタル", drumMix: { kick: { level: 1.2 }, snare: { level: 1.1, reverb: 0.1 }, hat: { level: 0.7, pan: -0.3 }, tom: { spread: 0.8, tune: -3 }, crash: { level: 0.8, pan: 0.3, reverb: 0.15 } }, drums: "metal", bass: "metal", swing: 0, human: 0.15, bpm: [140, 200], grids: G("XxXxXxXxXxXxXxXx", "....X.......X...", "x.x.x.x.x.x.x.x.") },
  pop: { id: "pop", label: "ポップ", drumMix: { hat: { level: 0.75, pan: -0.35 }, snare: { level: 1.0, reverb: 0.25 }, tom: { spread: 0.5 }, crash: { level: 0.85, pan: 0.3 } }, drums: "jpop", bass: "jpop", swing: 0, human: 0.3, bpm: [90, 125], grids: G("X.......X.x.....", "....X.......X...", "X.x.X.x.X.x.X.x.") },
  jpop: { id: "jpop", label: "J-POP・アニソン", drumMix: { kick: { level: 1.1 }, hat: { level: 0.85, pan: -0.3 }, snare: { level: 1.1, tune: 0.5, reverb: 0.2 }, tom: { spread: 0.6, tune: -2 }, crash: { level: 0.9, pan: 0.3 } }, drums: "jpop", bass: "jpop", swing: 0, human: 0.35, bpm: [120, 190], grids: G("X.....x...x.....", "....X.......X..o", "XoxoXoxoXoxoXoxo") },
  vocaloid: { id: "vocaloid", label: "ボカロ・高速ポップ", drumMix: { kick: { level: 1.1 }, hat: { level: 0.85, pan: -0.3 }, snare: { level: 1.1, tune: 0.5, reverb: 0.12 }, tom: { spread: 0.6, tune: -2 }, crash: { level: 0.9, pan: 0.3 } }, drums: "jpop", bass: "jpop", swing: 0, human: 0.2, bpm: [160, 200], grids: G("X..x..x.X..x..x.", "....X.......X...", "XoxoXoxoXoxoXoxo") },
  ballad: { id: "ballad", label: "バラード", drumMix: { kick: { level: 0.8 }, snare: { level: 0.75, tune: 2, reverb: 0.3 }, hat: { level: 0.55, pan: -0.3 }, tom: { spread: 0.6, tune: -2 }, crash: { level: 0.7, reverb: 0.3 } }, drums: "std", bass: "finger", swing: 0, human: 0.5, bpm: [60, 80], grids: G("X.......x.x.....", "....x.......x...", "o.o.o.o.o.o.o.o.") },
  jazz: { id: "jazz", label: "ジャズ（スウィング）", drumMix: { kick: { level: 0.5 }, snare: { level: 0.6, reverb: 0.1 }, hat: { level: 0.9, pan: 0.1 }, tom: { spread: 0.5 } }, drums: "jazz", bass: "jazz", swing: [0.9, 0.4], human: 0.55, bpm: [120, 220], grids: G("o...o...o...o...", "..o.....o.o.....", "x...x.x.x...x.x.") },
  funk: { id: "funk", label: "ファンク", drumMix: { kick: { level: 0.95 }, snare: { level: 1.0, tune: 1, reverb: 0.08 }, hat: { level: 0.8, pan: -0.3 }, tom: { spread: 0.5 } }, drums: "supra", bass: "std", swing: 0.2, human: 0.4, bpm: [95, 115], grids: G("X.x.......x.....", "o..oX..o.o.X..o.", "xoxoxoxoxoxoxoxo") },
  rnb: { id: "rnb", label: "R&B・ネオソウル", drumMix: { kick: { level: 0.9 }, snare: { level: 0.9, reverb: 0.2 }, hat: { level: 0.6, pan: -0.3 } }, drums: "std", bass: "finger", swing: 0.3, human: 0.45, bpm: [65, 100], grids: G("X.....o...X..o..", "....X..o....X...", "o.x.o.x.o.x.o.x.") },
  hiphop: { id: "hiphop", label: "ヒップホップ（ブーンバップ）", drumMix: { kick: { level: 1.1 }, snare: { level: 1.0, reverb: 0.12 }, hat: { level: 0.65, pan: -0.3 } }, drums: "std", bass: "std", swing: 0.4, human: 0.35, bpm: [80, 95], grids: G("X..o......x.....", "....X.......X...", "x.x.x.x.x.x.x.x.") },
  trap: { id: "trap", label: "トラップ", drumMix: { kick: { level: 1.1 }, snare: { level: 1.0, reverb: 0.2 }, hat: { level: 0.75, pan: -0.2 } }, drums: "jpop", bass: "std", swing: 0, human: 0.15, bpm: [130, 160], grids: G("X.....x.....x...", "........X.......", "x.x.x.x.x.x.x.x.") },
  house: { id: "house", label: "ハウス（4つ打ち）", drumMix: { kick: { level: 1.1 }, snare: { level: 0.9, reverb: 0.15 }, hat: { level: 0.7, pan: -0.25 }, crash: { level: 0.7 } }, drums: "jpop", bass: "std", swing: 0.15, human: 0.1, bpm: [120, 128], grids: G("X...X...X...X...", "....X.......X...", "o.O.o.O.o.O.o.O.") },
  disco: { id: "disco", label: "ディスコ", drumMix: { kick: { level: 1.1 }, snare: { level: 1.0, reverb: 0.15 }, hat: { level: 0.7, pan: -0.25 }, crash: { level: 0.7 } }, drums: "std", bass: "finger", swing: 0, human: 0.2, bpm: [110, 125], grids: G("X...X...X...X...", "....X.......X...", "x.O.x.O.x.O.x.O.") },
  dnb: { id: "dnb", label: "ドラムンベース（2ステップ）", drumMix: { kick: { level: 1.1 }, snare: { level: 1.1, reverb: 0.1 }, hat: { level: 0.7, pan: -0.2 } }, drums: "metal", bass: "std", swing: 0, human: 0.1, bpm: [165, 180], grids: G("X.........x.....", "....X.......X...", "x.x.x.x.x.x.x.x.") },
  dubstep: { id: "dubstep", label: "ダブステップ・ハーフタイム", drumMix: { kick: { level: 1.1 }, snare: { level: 1.1, reverb: 0.1 }, hat: { level: 0.7, pan: -0.2 } }, drums: "supra", bass: "std", swing: 0, human: 0.1, bpm: [138, 145], grids: G("X.........x.....", "........X.......", "x.x.x.x.x.x.x.x.") },
  reggae: { id: "reggae", label: "レゲエ（ワンドロップ）", drumMix: { snare: { level: 0.95, tune: 3, reverb: 0.12 }, kick: { level: 0.9 }, hat: { level: 0.7, pan: -0.3 }, tom: { spread: 0.4, tune: -1 } }, drums: "supra", bass: "finger", swing: [0.3, 0], human: 0.5, bpm: [65, 90], grids: G("........X.......", "........X.......", "x.x.x.X.x.x.x.X.") },
  bossa: { id: "bossa", label: "ボサノバ", drumMix: { kick: { level: 0.55 }, snare: { level: 0.55, tune: 3, reverb: 0.1 }, hat: { level: 0.6, pan: -0.2 } }, drums: "jazz", bass: "finger", swing: 0.15, human: 0.45, bpm: [100, 150], grids: G("x.....x.x.....x.", "x.....x.....x...", "x.x.x.x.x.x.x.x.") },
  dembow: { id: "dembow", label: "ダンボウ（ラテン・レゲトン系）", drumMix: { kick: { level: 1.1 }, snare: { level: 1.0, tune: 1 } }, drums: "std", bass: "std", swing: 0, human: 0.2, bpm: [85, 100], grids: G("X...X...X...X...", "...x..x....x..x.", "x.x.x.x.x.x.x.x.") },
  field: { id: "field", label: "ゲーム: フィールド", drumMix: { kick: { level: 0.7 }, snare: { level: 0.6, reverb: 0.2 }, hat: { level: 0.5 } }, drums: "std", bass: "finger", swing: 0, human: 0.4, bpm: [90, 120], grids: G("X.......x.......", "....o.......o...", "o...o...o...o...") },
  battle: { id: "battle", label: "ゲーム: 通常戦闘", drumMix: { kick: { level: 1.05 }, snare: { level: 1.1, reverb: 0.15 }, hat: { level: 0.85 }, tom: { spread: 0.7, tune: -3 } }, drums: "rock", bass: "pick", swing: 0, human: 0.25, bpm: [140, 180], grids: G("X...X...X.x.X...", "....X.......X...", "x.x.x.x.x.x.x.x.") },
  boss: { id: "boss", label: "ゲーム: ボス", drumMix: { kick: { level: 1.2 }, snare: { level: 1.1, reverb: 0.2 }, tom: { spread: 0.8, tune: -4 }, crash: { level: 1.0, reverb: 0.25 } }, drums: "metal", bass: "metal", swing: 0, human: 0.2, bpm: [150, 200], grids: G("XxXxXxXxXxXxXxXx", "....X.......X...", "x.x.x.x.x.x.x.x.") },
};

/** 曲JSONの drumMix に入れる値（コピー）。ジャンル名がなければ undefined。 */
export function drumMixFor(genre: string): DrumMix | undefined {
  const g = DRUM_GENRES[genre];
  return g ? (JSON.parse(JSON.stringify(g.drumMix)) as DrumMix) : undefined;
}

/** MPC風のパーセント（50＝まっすぐ、66＝三連）から、うちの swing（0〜1）へ。(pct-50)/16.7 を 0〜1 に収める。 */
export function swingFromPercent(pct: number): number {
  return Math.max(0, Math.min(1, Math.round(((pct - 50) / 16.7) * 100) / 100));
}

/** ジャズのテンポ別 swing。遅いほどはねる（60〜120＝0.8〜1.0、140〜180＝0.5〜0.7、200以上＝0.3〜0.5）。間は直線でつなぐ。 */
export function jazzSwingForBpm(bpm: number): number {
  const pts: [number, number][] = [[60, 1.0], [120, 0.8], [140, 0.7], [180, 0.5], [200, 0.5], [260, 0.3]];
  if (bpm <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) {
    if (bpm <= pts[i][0]) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
      return Math.round((y0 + ((y1 - y0) * (bpm - x0)) / (x1 - x0)) * 100) / 100;
    }
  }
  return pts[pts.length - 1][1];
}

/** ジャンルの swing の値（範囲ならテンポで補間。ジャズは jazzSwingForBpm）。 */
export function swingForGenre(genre: string, bpm: number): number {
  const g = DRUM_GENRES[genre];
  if (!g) return 0;
  if (genre === "jazz") return jazzSwingForBpm(bpm);
  if (typeof g.swing === "number") return g.swing;
  const [slow, fast] = g.swing;
  const [lo, hi] = g.bpm;
  const t = Math.max(0, Math.min(1, (bpm - lo) / Math.max(1, hi - lo)));
  return Math.round((slow + (fast - slow) * t) * 100) / 100;
}

/**
 * 速いテンポでは16分の連打が濁るので、偶数マス（8分）だけ残す。
 * 目安: 16分のキック／ハイハットは bpm 190 まで。200 以上のブラストは 8分に落とす。
 */
export function limitDensity(grid: string, bpm: number, maxSixteenthBpm = 190): string {
  if (bpm <= maxSixteenthBpm) return grid;
  return [...grid].map((c, i) => (i % 2 === 0 ? c : ".")).join("");
}

export type BlastType = "alternating" | "hammer" | "bomb";
/** ブラストビート（激しい場面。長く続けない：4〜8小節）。bpm が速いときは自動で 8分に落とす。 */
export function blastPattern(type: BlastType, bpm = 180): DrumGrooveGrids {
  const g = type === "alternating" ? G("x...x...x...x...", "..x...x...x...x.", "x.x.x.x.x.x.x.x.")
    : type === "hammer" ? G("x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.x.x.")
      : G("xxxxxxxxxxxxxxxx", "x.x.x.x.x.x.x.x.", "................");
  return { kick: limitDensity(g.kick, bpm, 200), snare: g.snare, hat: g.hat };
}
/** ギャロップ（8分＋16分2つ。ツーバスより軽く、走って聞こえる）。 */
export function gallop(): DrumGrooveGrids { return G("X.xxX.xxX.xxX.xx", "....X.......X...", "x.x.x.x.x.x.x.x."); }
/** ツーバス16分。 */
export function twoBass(bpm = 160): DrumGrooveGrids { return G(limitDensity("XxXxXxXxXxXxXxXx", bpm), "....X.......X...", "x.x.x.x.x.x.x.x."); }
/** ブレイクダウン（ハーフタイム＋重いキック）。 */
export function breakdownHalftime(): DrumGrooveGrids { return G("X.......X.x...x.", "........X.......", "x...x...x...x..."); }

export type TrapRollKind = "triplet" | "thirtysecond";
/**
 * トラップのハイハットのロール（拍つき表記。合計4拍の1小節ぶん）。
 * triplet＝最後の1拍が三連、thirtysecond＝最後の半拍が32分。中の音は弱く（,）、最後の1発は強く（!）。
 */
export function trapRoll(kind: TrapRollKind = "triplet"): string {
  if (kind === "triplet") return "x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.333, x:0.333, x:0.334!";
  return "x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.125, x:0.125, x:0.125, x:0.125!";
}
/** ロールの拍の合計（検査用）。 */
export function trapRollBeats(roll: string): number {
  return roll.split(/\s+/).reduce((s, t) => s + Number(/:([\d.]+)/.exec(t)?.[1] ?? 0), 0);
}

function seeded(seed: number): () => number {
  let a = (seed * 2654435761) >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * スネアのゴーストノート（弱い音 o）を置いた1小節の格子を返す。
 * - バックビート（既に X か x のマス）とキックと同じマスには置かない。
 * - バックビートの直前のマス（速いテンポ bpm>=140）には置かない。
 * - 3つ続けて置かない。density（0〜1）で確率が決まり、同じ小節番号なら同じ結果。
 */
export function placeGhosts(snare: string, kick: string, density: number, barIndex: number, bpm = 100): string {
  const rnd = seeded(barIndex + 1);
  const cells = [...snare];
  const hit = (i: number): boolean => cells[i] !== ".";
  const candidates = [3, 5, 7, 9, 11, 13, 15, 2, 6, 10, 14].filter((i) => i < cells.length);
  let run = 0;
  for (let i = 0; i < cells.length; i++) {
    if (hit(i)) { run = 0; continue; }
    if (!candidates.includes(i) || kick[i] !== "." && kick[i] !== undefined) { run = 0; continue; }
    const nextBack = cells[i + 1] === "X" || cells[i + 1] === "x";
    if (bpm >= 140 && nextBack) { run = 0; continue; }
    if (run >= 2) { run = 0; continue; }
    if (rnd() < density) { cells[i] = "o"; run++; } else run = 0;
  }
  return cells.join("");
}

/**
 * ハイハットの強弱の型。小節ごとに型を回し（同じ小節の繰り返しを避ける）、4小節目に開いたハイハット（O）を1つだけ置く。
 * section: verse＝半分の密度、chorus＝16分に細かく。省略は基本の型。
 */
export function hihatPattern(genre: string, barIndex: number, section?: "verse" | "pre" | "chorus"): string {
  const base = DRUM_GENRES[genre]?.grids.hat ?? "x.x.x.x.x.x.x.x.";
  let pat = base;
  if (section === "verse") pat = [...base].map((c, i) => (i % 4 === 0 ? c : ".")).join("");
  else if (section === "chorus" && !base.includes("o")) pat = [...base].map((c, i) => (i % 2 === 1 ? "o" : c === "." ? "x" : c)).join("");
  const cells = [...pat];
  if (barIndex % 2 === 1) for (let i = 0; i < cells.length; i++) if (cells[i] === "X" && i % 8 !== 0) cells[i] = "x";
  if (barIndex % 4 === 3 && cells[14] !== "." && !cells.includes("O")) cells[14] = "O";
  return cells.join("");
}

/** 16文字でない格子（検査用）。拍子つき: 4/4＝16、3拍子＝12。 */
export function gridLengthOk(grid: string, beats = 4): boolean {
  return grid.length === Math.round(beats * 4);
}
