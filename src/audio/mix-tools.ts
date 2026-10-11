// ミックスの道具（2026-10-11）。docs/sound/mix-patterns.md の提案 5・6・11 と、sound-design-basics.md の提案 6・7・9・10 の実装。
// 数字は docs/sound/mix-patterns.md（M08 の duck・§4 の症状・§6 のチェックリスト）と sound-design-basics.md（§3-3 のテンポ同期、§5 のゲーム内の音量の関係）から。
// 書き出し（song-lib の build）の警告と、作曲ソフトの画面の目安に使う。曲の中身（旋律・コード）には触らない。
import type { Instrument, Score, Track } from "./score";

// ── テンポ同期（BPM から秒数） ──

export interface SyncTimes {
  bpm: number;
  /** 4分音符（1拍） */
  quarter: number;
  dottedQuarter: number;
  eighth: number;
  /** 付点8分（ディレイの定番） */
  dottedEighth: number;
  /** 8分の3連 */
  eighthTriplet: number;
  sixteenth: number;
  /** 2分音符 */
  half: number;
  /** 1小節（4/4） */
  bar: number;
}

/** BPM から、ディレイ・LFO・リリースに使う各音価の長さ（秒）。1 拍 = 60 ÷ BPM。 */
export function syncDelaySeconds(bpm: number): SyncTimes {
  if (!(bpm > 0)) throw new Error("BPM は 0 より大きい数");
  const q = 60 / bpm;
  const r = (v: number) => Math.round(v * 1e6) / 1e6;
  return { bpm, quarter: r(q), dottedQuarter: r(q * 1.5), eighth: r(q / 2), dottedEighth: r((q * 3) / 4), eighthTriplet: r(q / 3), sixteenth: r(q / 4), half: r(q * 2), bar: r(q * 4) };
}

/** 残響の長さの目安（秒）: 1 拍の 0.5〜1 倍（速い曲は短く、遅い曲は長く）。 */
export function reverbDecayHint(bpm: number): { min: number; max: number } {
  const q = 60 / bpm;
  return { min: Math.round(q * 0.5 * 100) / 100, max: Math.round(q * 1.0 * 100) / 100 };
}

// ── サイドチェイン風 duck の推奨値 ──

/** duck（キックに合わせて凹む深さ）が戻るまでの時間（ms）。約 0.45 拍（mix-patterns M08）。 */
export const duckRecoverMs = (bpm: number): number => Math.round((60000 / bpm) * 0.45);

export type DuckRole = "bass" | "sub808" | "pad" | "strings" | "keys" | "guitar" | "choir";
export type DuckGenre = "rock" | "pop" | "punk" | "metal" | "edm" | "hiphop" | "jazz" | "ambient" | "ballad" | "game";

/** 役割別の基本値（mix-patterns M08・layering-guide: ベース .15〜.3、パッド・弦 .2〜.4）。 */
const DUCK_BASE: Record<DuckRole, [number, number]> = { bass: [0.15, 0.3], sub808: [0.2, 0.3], pad: [0.2, 0.4], strings: [0.2, 0.35], keys: [0.15, 0.3], guitar: [0.05, 0.15], choir: [0.15, 0.3] };
/** ジャンルでの掛け率（EDM は深く、ジャズ・アンビエントは使わない〜浅く） */
const DUCK_GENRE: Record<DuckGenre, number> = { rock: 1, pop: 1, punk: 0.55, metal: 1.1, edm: 1.4, hiphop: 1, jazz: 0.3, ambient: 0.25, ballad: 0.4, game: 0.9 };

export interface DuckAdvice {
  /** 推奨する duck の値（0〜1） */
  duck: number;
  /** 範囲（浅い〜深い） */
  range: [number, number];
  /** 戻りの時間の目安（ms） */
  recoverMs: number;
  /** 注意（BPM が速くて戻りきらない、など） */
  notes: string[];
}

/** 役割・ジャンル・BPM から duck の推奨値を出す。EDM 以外では 0.4 を超えない（ポンピングが目立つ）。 */
export function recommendDuck(role: DuckRole, genre: DuckGenre, bpm: number): DuckAdvice {
  const k = DUCK_GENRE[genre];
  const [lo0, hi0] = DUCK_BASE[role];
  const cap = genre === "edm" ? 0.6 : 0.4;
  const round = (v: number) => Math.round(Math.min(cap, v) * 100) / 100;
  const range: [number, number] = [round(lo0 * k), round(hi0 * k)];
  const duck = round(((lo0 + hi0) / 2) * k);
  const recoverMs = duckRecoverMs(bpm);
  const notes: string[] = [];
  if (recoverMs < 150) notes.push(`BPM ${bpm} だと戻りが約 ${recoverMs}ms で短く、ポンピングが目立ちやすい。duck を ${Math.max(0.1, Math.round(duck * 0.7 * 100) / 100)} 前後まで浅くする`);
  if (recoverMs > 400) notes.push(`BPM ${bpm} だと戻りが約 ${recoverMs}ms と長く、ベースが引っ込んだままに聞こえやすい。ベースの音を短く切る（sustain .6〜.8）`);
  if (genre !== "edm" && duck >= 0.35) notes.push("0.4 以上はポンピングが目立つ（EDM 向け）");
  return { duck, range, recoverMs, notes };
}

// ── 楽譜の検査（150Hz 以下のモノ化・席の重なり・音量の合計） ──

const LOW_MONO = new Set<string>(["kick", "bass", "sub808", "slap"]);
const NO_MIX = new Set<string>(["sfxDown", "sfxUp", "impact", "swoosh", "pierce", "wind", "rain", "stream", "bird", "crickets"]);
const DRUMS = new Set<string>(["kick", "snare", "hihat", "crash", "tom", "cowbell"]);
const label = (t: Track, i: number) => `${t.instrument ?? t.waveform}（${i + 1}番目）`;

/**
 * ミックスの検査（mix-patterns §6 のチェックリストのうち、楽譜から分かるもの）。警告だけで、曲は作れる。
 *  - 低域のパート（kick・bass・sub808）が中央でない／残響が多い（150Hz 以下はモノにする、濁る）
 *  - 低域のパートが 3 つを超える
 *  - 音量の合計が 0.9 超（自動で縮む）
 *  - 主役（最大の音量）が違う楽器で同じ値のまま 2 つ以上
 *  - 同じ側（左／右）に 3 パート以上
 */
export function checkMixRoles(score: Score): string[] {
  const w: string[] = [];
  const tracks = score.tracks;
  tracks.forEach((t, i) => {
    const inst = t.instrument ?? "";
    if (LOW_MONO.has(inst) && Math.abs(t.pan ?? 0) > 0.1) w.push(`${label(t, i)}が中央にありません（pan ${t.pan}）。150Hz 以下は中央（モノ）に置かないと、モノで聞いたときに低音が痩せます。`);
    if (LOW_MONO.has(inst) && (t.reverb ?? 0) > 0.1) w.push(`${label(t, i)}の reverb が ${t.reverb} です。低音に残響を足すと濁ります（0〜0.05 に）。`);
  });
  const lows = tracks.filter((t) => LOW_MONO.has(t.instrument ?? "")).length;
  if (lows > 3) w.push(`低域を担うパート（kick・bass・sub808）が ${lows} 個あります。3 個までにすると濁りにくくなります。`);
  const sum = tracks.reduce((a, t) => a + t.volume, 0);
  if (sum > 0.9) w.push(`パートの volume の合計が ${sum.toFixed(2)} で 0.9 を超えています（0.7〜0.8 が安全。超えると書き出しの前に縮められます）。`);
  const mel = tracks.filter((t) => !DRUMS.has(t.instrument ?? "") && !NO_MIX.has(t.instrument ?? ""));
  if (mel.length >= 2) {
    const max = Math.max(...mel.map((t) => t.volume));
    const top = mel.filter((t) => Math.abs(t.volume - max) < 0.0005);
    const kinds = new Set(top.map((t) => t.instrument));
    if (top.length >= 2 && kinds.size >= 2) w.push(`主役級の音量が違う楽器で同じ値のまま ${top.length} つあります（${[...kinds].join("・")}）。主役を 1 つ決めて、ほかを ×0.6〜0.8 に。`);
  }
  const side = (sign: number) => mel.filter((t) => (t.pan ?? 0) * sign > 0.3).length;
  if (side(-1) >= 3) w.push(`左側（pan -0.3 より外）に ${side(-1)} パートが集まっています。似た帯域を同じ側に積むと濁ります。`);
  if (side(1) >= 3) w.push(`右側（pan 0.3 より外）に ${side(1)} パートが集まっています。似た帯域を同じ側に積むと濁ります。`);
  return w;
}

// ── ゴースト層（パラレル圧縮の代用）・ゲーム用の席空け ──

/**
 * ゴースト層（mix-patterns M03）: 指定した楽器のパートを複製し、小さく・奥に・暗くする。聞いて決めるための試作。
 * volume ×0.25、reverb +0.25（上限 1）、bright −0.25（下限 −1）。元の曲は変えない。複製が無ければ何もしない。
 */
export function addGhostLayer(score: Score, instrument: Instrument, opts: { gain?: number; reverb?: number; bright?: number } = {}): Score {
  const { gain = 0.25, reverb = 0.25, bright = -0.25 } = opts;
  const extra: Track[] = [];
  for (const t of score.tracks) {
    if (t.instrument !== instrument) continue;
    extra.push({ ...t, volume: Math.round(t.volume * gain * 10000) / 10000, reverb: Math.min(1, (t.reverb ?? 0) + reverb), bright: Math.max(-1, (t.bright ?? 0) + bright), notes: t.notes.map((n) => ({ ...n })) });
  }
  return extra.length ? { ...score, tracks: [...score.tracks, ...extra] } : score;
}

/** 1〜4kHz を担うパート（効果音・会話と帯域が重なる） */
export const MIDRANGE_PARTS: Instrument[] = ["lead", "leadGuitar", "distGuitar", "crunch", "bell", "brass"];

/**
 * ゲーム用の席空け（sound-design-basics 提案 7）: 1〜4kHz を担うパートの volume を db（既定 2.5dB）下げ、伴奏の bright を少し下げる。
 * 元の曲は変えず、通常版とゲーム版の 2 通りを書き出すために使う。
 */
export function applyGameDuck(score: Score, db = 2.5): Score {
  const k = Math.pow(10, -db / 20);
  const tracks = score.tracks.map((t) => {
    if (t.instrument && MIDRANGE_PARTS.includes(t.instrument)) return { ...t, volume: Math.round(t.volume * k * 10000) / 10000 };
    if (t.instrument && !DRUMS.has(t.instrument) && !LOW_MONO.has(t.instrument) && !NO_MIX.has(t.instrument) && t.instrument !== "pad" && t.instrument !== "strings") return { ...t, bright: Math.max(-1, (t.bright ?? 0) - 0.1) };
    return t;
  });
  return { ...score, tracks };
}

// ── 役割から初期値（ミックスの下書き） ──

export type PartRole = "bass" | "chord" | "melody" | "ornament" | "space" | "drums";

export interface PartDefaults { volume: number; pan: number; reverb: number; bright: number; duck: number }

/** 役割ごとの初期値（mix-patterns §5 の階層: 主役1／準主役.6／脇役.35／空気.2 を、clear-guitar-rock の目盛り 0.1 を主役として換算）。 */
export const ROLE_DEFAULTS: Record<PartRole, PartDefaults> = {
  melody: { volume: 0.1, pan: 0, reverb: 0.2, bright: 0, duck: 0 },
  bass: { volume: 0.09, pan: 0, reverb: 0, bright: 0.1, duck: 0.25 },
  chord: { volume: 0.06, pan: 0.4, reverb: 0.2, bright: -0.1, duck: 0.15 },
  ornament: { volume: 0.035, pan: 0.5, reverb: 0.4, bright: -0.1, duck: 0 },
  space: { volume: 0.02, pan: 0.4, reverb: 0.5, bright: -0.25, duck: 0.3 },
  drums: { volume: 0.06, pan: 0, reverb: 0.1, bright: 0, duck: 0 },
};

/** 役割から初期値を返す。pan は side（-1 左／1 右）を掛けた向きつき。 */
export function suggestPartDefaults(role: PartRole, side: -1 | 0 | 1 = 1): PartDefaults {
  const d = ROLE_DEFAULTS[role];
  return { ...d, pan: role === "bass" || role === "melody" || role === "drums" ? 0 : Math.round(d.pan * side * 100) / 100 };
}
