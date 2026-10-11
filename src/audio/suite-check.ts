import { barChordsOf, chordRootPc } from "./loop-check";
import { ENERGY_CURVES, type EnergyCurve } from "./scene";
import { guessKey, totalBarsOf } from "./song-expand";

/**
 * 組曲の定義と検査（docs/sound/form-structure-guide.md §12 の提案10、§9.4）。
 * assets-src/suites/*.json に、曲の並び・つなぎの種類（拍の頭／スティンガー／セグエ）・テンポの比・調の関係を書き、
 * checkSuite が ①テンポ比（1:1・2:1・3:2・3:4） ②調の関係（同じ・5度上下・平行調・同主調）
 * ③最後のコードと次の最初のコードの関係（同じ・属和音） ④つなぎの種類の記録 ⑤全体の強さの曲線（組曲を1曲と見た山と谷）を点検する。
 *
 * {
 *   "name": "虚灯宮の組曲",
 *   "songs": [
 *     { "file": "kyoto-1", "link": "beat" },                       // assets-src/ai-songs/kyoto-1.json から bpm・調・コード・強さを読む
 *     { "id": "kyoto-2", "bpm": 150, "key": "D", "mode": "minor", "firstChord": "Dm", "lastChord": "A7", "bars": 32, "energy": [3, 6, 9], "link": "stinger", "stinger": "sting-1" }
 *   ]
 * }
 */
export type LinkKind = "beat" | "stinger" | "segue";
export interface SuiteSong {
  id: string;
  bpm: number;
  /** 主音（C・F#・Bb など）と長短。 */
  key?: string;
  mode?: "major" | "minor";
  bars?: number;
  firstChord?: string;
  lastChord?: string;
  /** セクション順の強さ（1〜10）。 */
  energy?: number[];
  /** この曲の「前の曲からの」つなぎ。 */
  link?: LinkKind;
  stinger?: string;
}
export interface SuiteDef {
  name?: string;
  songs: (Partial<SuiteSong> & { file?: string })[];
}

const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
export const keyPc = (key: string): number | null => {
  const m = /^([A-G])([#b]?)$/.exec(key);
  return m ? (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12 : null;
};

/** 許す簡単な比（a:b）。 */
export const TEMPO_RATIOS: [number, number][] = [[1, 1], [2, 1], [1, 2], [3, 2], [2, 3], [3, 4], [4, 3]];
export function tempoRatio(a: number, b: number, tol = 0.02): [number, number] | null {
  if (!(a > 0 && b > 0)) return null;
  const r = b / a;
  for (const [p, q] of TEMPO_RATIOS) if (Math.abs(r - p / q) / (p / q) <= tol) return [p, q];
  return null;
}

/** 調の関係。 */
export function keyRelation(a: { key: string; mode: "major" | "minor" }, b: { key: string; mode: "major" | "minor" }): "same" | "fifth" | "relative" | "parallel" | null {
  const pa = keyPc(a.key), pb = keyPc(b.key);
  if (pa === null || pb === null) return null;
  const d = (((pb - pa) % 12) + 12) % 12;
  if (a.mode === b.mode) {
    if (d === 0) return "same";
    if (d === 7 || d === 5) return "fifth";
    return null;
  }
  // 平行調: 長調の主音の3半音下が短調の主音
  const majPc = a.mode === "major" ? pa : pb, minPc = a.mode === "minor" ? pa : pb;
  if ((majPc - minPc + 12) % 12 === 3) return "relative";
  if (pa === pb) return "parallel";
  return null;
}

/** 最後のコードと次の最初のコードの関係。同じ根音か、最後が次の属和音（根音が5度上）。 */
export function chordLink(last: string, first: string): "same" | "dominant" | null {
  const a = chordRootPc(last), b = chordRootPc(first);
  if (a === null || b === null) return null;
  if (a === b) return "same";
  return (a - b + 12) % 12 === 7 ? "dominant" : null;
}

/** AIソング形式の曲のJSON（展開・前処理ずみ）から、組曲の検査に使う値を取り出す。 */
export function suiteFieldsFromSong(song: { bpm?: unknown; beats?: unknown; chords: string; barsPerChord: number; repeats: number; energy?: unknown; sections?: unknown; sectionChords?: unknown }): Partial<SuiteSong> {
  const bars = barChordsOf(song.chords, song.barsPerChord, song.repeats);
  const k = guessKey(song.chords);
  const energy = Array.isArray(song.energy) && song.energy.every((x) => Number.isFinite(Number(x))) ? song.energy.map(Number) : typeof song.energy === "string" && song.energy in ENERGY_CURVES ? ENERGY_CURVES[song.energy as EnergyCurve] : undefined;
  return {
    bpm: Number(song.bpm), key: k.key, mode: k.mode, bars: totalBarsOf(song) || bars.length,
    firstChord: bars[0], lastChord: bars[bars.length - 1], ...(energy ? { energy } : {}),
  };
}

export interface SuiteReport { lines: string[]; warnings: string[]; songs: SuiteSong[] }

/** readSong: file 名から曲のJSON（前処理ずみ）を返す。なければ null。 */
export function resolveSuite(def: SuiteDef, readSong?: (file: string) => Parameters<typeof suiteFieldsFromSong>[0] | null, warnings: string[] = []): SuiteSong[] {
  const out: SuiteSong[] = [];
  def.songs.forEach((s, i) => {
    let fields: Partial<SuiteSong> = {};
    if (s.file) {
      const song = readSong?.(s.file);
      if (!song) { warnings.push(`songs[${i}]: ファイル「${s.file}」の曲が読めません`); }
      else fields = suiteFieldsFromSong(song);
    }
    const merged: Partial<SuiteSong> = { ...fields, ...Object.fromEntries(Object.entries(s).filter(([k]) => k !== "file")) };
    const id = merged.id ?? s.file ?? `song${i + 1}`;
    if (!(Number(merged.bpm) > 0)) { warnings.push(`songs[${i}]（${id}）: bpm がありません`); return; }
    out.push({ ...merged, id, bpm: Number(merged.bpm) } as SuiteSong);
  });
  return out;
}

export function checkSuite(def: SuiteDef, readSong?: (file: string) => Parameters<typeof suiteFieldsFromSong>[0] | null): SuiteReport {
  const warnings: string[] = [];
  const songs = resolveSuite(def, readSong, warnings);
  const lines: string[] = [];
  if (songs.length < 2) warnings.push("組曲には2曲以上が必要です");
  for (let i = 1; i < songs.length; i++) {
    const a = songs[i - 1], b = songs[i];
    const head = `${a.id} → ${b.id}`;
    const parts: string[] = [];
    // ① テンポ比
    const r = tempoRatio(a.bpm, b.bpm);
    parts.push(`テンポ ${a.bpm}→${b.bpm}（${r ? `${r[0]}:${r[1]}` : "簡単な比でない"}）`);
    if (!r) warnings.push(`${head}: テンポの比が簡単でありません（${a.bpm}→${b.bpm}。1:1・2:1・3:2・3:4 のどれかにすると自然につながります）`);
    // ② 調の関係
    if (a.key && b.key) {
      const kr = keyRelation({ key: a.key, mode: a.mode ?? "major" }, { key: b.key, mode: b.mode ?? "major" });
      const label = { same: "同じ調", fifth: "5度上下", relative: "平行調", parallel: "同主調" }[kr ?? "same"];
      parts.push(`調 ${a.key}${a.mode === "minor" ? "m" : ""}→${b.key}${b.mode === "minor" ? "m" : ""}（${kr ? label : "遠い調"}）`);
      if (!kr) warnings.push(`${head}: 調が遠いです（${a.key}${a.mode === "minor" ? "m" : ""}→${b.key}${b.mode === "minor" ? "m" : ""}）。5度上下・平行調・同主調にするか、間にスティンガー（link: "stinger"）を置いてください`);
    }
    // ③ 最後のコード → 次の最初のコード
    if (a.lastChord && b.firstChord) {
      const cl = chordLink(a.lastChord, b.firstChord);
      parts.push(`和音 ${a.lastChord}→${b.firstChord}（${cl === "same" ? "同じ" : cl === "dominant" ? "属和音" : "つながりにくい"}）`);
      if (!cl) warnings.push(`${head}: 最後のコード ${a.lastChord} が、次の最初のコード ${b.firstChord} の属和音でも同じ和音でもありません。最後を ${b.firstChord} の V（5度上）にするとなめらかです`);
    }
    // ④ つなぎの種類
    if (!b.link) warnings.push(`${head}: つなぎの種類（link: beat／stinger／segue）が書かれていません`);
    else {
      parts.push(`つなぎ ${{ beat: "拍の頭で切り替え", stinger: "スティンガー", segue: "セグエ" }[b.link]}`);
      if (b.link === "stinger" && !b.stinger) warnings.push(`${head}: link が stinger ですが、stinger（効果音の名前）が書かれていません`);
    }
    lines.push(`${head}: ${parts.join("・")}`);
  }
  // ⑤ 全体の強さの曲線
  const curve = songs.flatMap((s) => s.energy ?? []);
  if (curve.length >= 4) {
    const max = Math.max(...curve), min = Math.min(...curve);
    const lastPeakAt = curve.lastIndexOf(max);
    lines.push(`強さの曲線: ${curve.join(",")}（山 ${max}・谷 ${min}）`);
    if (max - min < 3) warnings.push(`組曲全体の強さの幅が ${max - min} と小さいです（山と谷を作ってください）`);
    if (lastPeakAt < curve.length * 0.5) warnings.push(`組曲全体で最高の強さ（${max}）が前半にあります。山は後ほど高くしてください`);
    let deepest = Infinity;
    for (let i = 1; i < lastPeakAt; i++) deepest = Math.min(deepest, curve[i]);
    if (lastPeakAt >= 2 && !(deepest <= max - 3)) warnings.push("最後の山の前に谷（最高点より3段以上低い所）がありません");
  } else if (songs.length >= 2) lines.push("強さの曲線: energy が書かれていないので点検しません");
  return { lines, warnings, songs };
}

export function formatSuiteReport(name: string, r: SuiteReport): string {
  return [`■ 組曲${name ? `「${name}」` : ""}（${r.songs.length}曲）`, ...r.lines.map((l) => `  ${l}`), ...(r.warnings.length ? r.warnings.map((w) => `  注意: ${w}`) : ["  ○ 注意なし"])].join("\n");
}
