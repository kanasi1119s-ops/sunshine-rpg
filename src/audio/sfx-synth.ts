import { analyzeSamples, applyFilter, dbToGain, envAt, envLength, makeRng, noiseGen, pathAt, waveAt, type EnvSpec, type FilterSpec, type NoiseColor, type SeAnalysis, type Wave } from "./synth-dsp";
import { findScale, scalePitchClasses, type Scale } from "./scales";

/**
 * 純合成の効果音（SE）の仕組み（2026-10-11、docs/sound/synth-sfx-guide.md の提案 1〜6）。
 * レシピ（SfxRecipe）＝層（Layer）の並びのデータ。renderSfx がそれを波形（Float32Array）に描く（Web Audio を使わないので、
 * Node のテスト・WAV 書き出し・ブラウザのどれでも同じ音）。ブラウザでは sfxBuffer / playSfx で AudioBuffer にして鳴らす。
 * レシピ本体（58 種）は sfx-recipes.ts。
 */

export interface LayerBase {
  /** 鳴らし始める時刻（秒）。 */
  at: number;
  /** その SE でいちばん大きい層に対する相対音量（dB）。 */
  db: number;
  env: EnvSpec;
  /** 層にかけるフィルター（直列）。 */
  filter?: FilterSpec[];
  /** 音量を揺らす（トレモロ／きしみの刻み）。depth＝揺れの深さ（0〜1）、shape＝sine か square。 */
  am?: { hz: number; depth: number; shape?: "sine" | "square" };
  /** 調に合わせる対象（※調）。tuneSe がこの層の周波数を音階の音へ寄せる。 */
  tune?: boolean;
}
export interface ToneLayer extends LayerBase {
  kind: "tone";
  wave: Wave;
  f0: number;
  /** 周波数が動く先。glide 秒で指数的に。 */
  f1?: number;
  glide?: number;
  /** 折れ線の動き [[秒, Hz], ...]。あれば f0・f1 のかわり。 */
  fpath?: [number, number][];
  /** ユニゾン（セントのずれの並び）。音量は 1/√本数。 */
  detunes?: number[];
}
export interface NoiseLayer extends LayerBase {
  kind: "noise";
  color: NoiseColor;
}
export interface FmLayer extends LayerBase {
  kind: "fm";
  fc: number;
  ratio: number;
  /** 変調指数（キャリア周波数に対する倍率）。i0 から i1 へ sweep 秒で指数的に下がる＝頭だけ明るい。 */
  i0: number;
  i1: number;
  sweep: number;
}
export type Layer = ToneLayer | NoiseLayer | FmLayer;

export type SeKind = "ui" | "notice" | "impact" | "magic" | "fanfare";
export type DuckLevel = "none" | "notice" | "warning" | "fanfare";

export interface SfxRecipe {
  id: string;
  group: string;
  name: string;
  kind: SeKind;
  /** 想定の長さ（秒）。 */
  lengthSec: number;
  layers: Layer[];
  /** 全体にかけるフィルター（直列）。 */
  filter?: FilterSpec[];
  /** 全体の音量の揺れ。 */
  am?: { hz: number; depth: number; shape?: "sine" | "square" };
  /** 残響（尾を長くする）。decay＝秒、mix＝0〜1。 */
  reverb?: { decay: number; mix: number };
  /** 山の高さ（dBFS）。省略は ui −6・それ以外 −4.5。 */
  peakDb?: number;
  /** 立ち上がりがゆっくりなのが正しい SE（詠唱・ライザーなど）。検査の「立ち上がり」を免除する。 */
  soft?: boolean;
  /** 変化づけの幅（毎回の発音のゆれ）。 */
  vary?: { pitch?: number; gainDb?: number; filter?: number };
  /** 同じ SE を再び鳴らすまで空ける最短の間隔（ミリ秒）。 */
  throttleMs?: number;
  /** BGM を下げる量の段階。省略は kind から（ui・impact・magic＝なし、notice＝通知、fanfare＝ファンファーレ）。 */
  duck?: DuckLevel;
  /** 乱数の種（バブル・きらめきなど、レシピ内のランダムな層を固定するため）。 */
  seed?: number;
}

const hashId = (s: string): number => { let h = 2166136261; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h >>> 0; };

// ───────── 描画 ─────────
function amValue(am: NonNullable<SfxRecipe["am"]>, t: number): number {
  const ph = (t * am.hz) % 1;
  const w = am.shape === "square" ? (ph < 0.5 ? 1 : 0) : 0.5 + 0.5 * Math.cos(2 * Math.PI * ph);
  return 1 - am.depth * (1 - w);
}

/** 1 つの層を、層の長さぶんのバッファに描く（フィルター・包絡・AM を掛けたもの。音量 db は掛けてある）。 */
function renderLayer(layer: Layer, sr: number, rng: () => number): Float32Array {
  const len = Math.max(1, Math.ceil(envLength(layer.env) * sr) + 8);
  const buf = new Float32Array(len);
  if (layer.kind === "noise") {
    const gen = noiseGen(layer.color, rng);
    for (let i = 0; i < len; i++) buf[i] = gen();
  } else if (layer.kind === "tone") {
    const voices = layer.detunes && layer.detunes.length ? layer.detunes : [0];
    const phases = voices.map((_, k) => (k * 0.37) % 1);
    const glide = Math.max(1e-3, layer.glide ?? 0.1);
    const norm = 1 / Math.sqrt(voices.length);
    for (let i = 0; i < len; i++) {
      const t = i / sr;
      const f = layer.fpath ? pathAt(layer.fpath, t) : layer.f1 ? layer.f0 * (layer.f1 / layer.f0) ** Math.min(1, t / glide) : layer.f0;
      let sum = 0;
      for (let k = 0; k < voices.length; k++) {
        const fk = f * 2 ** (voices[k] / 1200);
        const dt = fk / sr;
        phases[k] = (phases[k] + dt) % 1;
        sum += waveAt(layer.wave, phases[k], dt);
      }
      buf[i] = sum * norm;
    }
  } else {
    let pc = 0, pm = 0;
    const fm = layer.fc * layer.ratio;
    const beta0 = layer.i0 / layer.ratio, beta1 = Math.max(layer.i1, 0.0001) / layer.ratio;
    for (let i = 0; i < len; i++) {
      const t = i / sr;
      const beta = layer.i1 > 0 ? beta0 * (beta1 / beta0) ** Math.min(1, t / Math.max(1e-3, layer.sweep)) : beta0 * Math.max(0, 1 - t / Math.max(1e-3, layer.sweep));
      pc = (pc + layer.fc / sr) % 1;
      pm = (pm + fm / sr) % 1;
      buf[i] = Math.sin(2 * Math.PI * pc + beta * Math.sin(2 * Math.PI * pm));
    }
  }
  for (const f of layer.filter ?? []) applyFilter(buf, f, sr);
  const gain = dbToGain(layer.db);
  for (let i = 0; i < len; i++) {
    const t = i / sr;
    buf[i] *= envAt(layer.env, t) * gain * (layer.am ? amValue(layer.am, t) : 1);
  }
  return buf;
}

/** 簡単な残響（4 本のコムフィルターと 2 本のオールパス）。 */
function reverb(x: Float32Array, sr: number, decay: number, mix: number): Float32Array {
  const out = new Float32Array(x.length);
  const combs = [0.0297, 0.0371, 0.0411, 0.0437].map((d) => ({ n: Math.round(d * sr), buf: new Float32Array(Math.round(d * sr)), i: 0, g: 0.001 ** (d / Math.max(0.1, decay)) }));
  const allpass = [0.005, 0.0017].map((d) => ({ n: Math.round(d * sr), buf: new Float32Array(Math.round(d * sr)), i: 0 }));
  for (let i = 0; i < x.length; i++) {
    let s = 0;
    for (const c of combs) { const y = c.buf[c.i]; c.buf[c.i] = x[i] + y * c.g; c.i = (c.i + 1) % c.n; s += y; }
    s *= 0.25;
    for (const a of allpass) { const y = a.buf[a.i]; const v = s + y * 0.5; a.buf[a.i] = v; s = y - 0.5 * v; a.i = (a.i + 1) % a.n; }
    out[i] = x[i] * (1 - mix) + s * mix * 2.2;
  }
  return out;
}

/** レシピの長さ（秒）。層の終わりの最大＋残響の尾。 */
export function recipeDuration(r: SfxRecipe): number {
  let end = 0.05;
  for (const l of r.layers) end = Math.max(end, l.at + envLength(l.env));
  return end + (r.reverb ? r.reverb.decay * 0.6 : 0);
}

/** レシピを波形に描く。山は peakDb にそろえる（レシピごとの音量の目安）。 */
export function renderSfx(recipe: SfxRecipe, sr = 44100): Float32Array {
  const rng = makeRng(recipe.seed ?? hashId(recipe.id));
  const out = new Float32Array(Math.ceil(recipeDuration(recipe) * sr) + 1);
  for (const layer of recipe.layers) {
    const buf = renderLayer(layer, sr, rng);
    const off = Math.round(layer.at * sr);
    for (let i = 0; i < buf.length && off + i < out.length; i++) out[off + i] += buf[i];
  }
  let mix: Float32Array = out;
  for (const f of recipe.filter ?? []) applyFilter(mix, f, sr);
  if (recipe.am) for (let i = 0; i < mix.length; i++) mix[i] *= amValue(recipe.am, i / sr);
  if (recipe.reverb) mix = reverb(mix, sr, recipe.reverb.decay, recipe.reverb.mix);
  let peak = 0;
  for (let i = 0; i < mix.length; i++) peak = Math.max(peak, Math.abs(mix[i]));
  const target = dbToGain(recipe.peakDb ?? (recipe.kind === "ui" ? -6 : -4.5));
  if (peak > 0) {
    const g = target / peak;
    for (let i = 0; i < mix.length; i++) mix[i] *= g;
  }
  // 先頭と終わりのクリック防止（0.5ms のフェード）
  const fade = Math.min(Math.round(0.0005 * sr), mix.length >> 1);
  for (let i = 0; i < fade; i++) { mix[mix.length - 1 - i] *= i / fade; }
  return mix;
}

// ───────── 検査 ─────────
/** SE の種類ごとの長さの上限（秒）。ガイド 10-3 の UI 0.4・衝撃 0.8・魔法 1.6・ファンファーレ 4 に、通知 1.0 を足した。 */
export const SE_MAX_SEC: Record<SeKind, number> = { ui: 0.4, notice: 1.0, impact: 0.8, magic: 1.6, fanfare: 4 };

/** 分析結果と、レシピの種類から、警告の文章を返す（山 −3dBFS 以下・長さ・立ち上がり 10ms・直流・UI の 1〜4kHz）。 */
export function checkSe(a: SeAnalysis, recipe: Pick<SfxRecipe, "id" | "kind" | "soft">): string[] {
  const out: string[] = [];
  const name = recipe.id;
  if (a.peakDb > -3) out.push(`${name}: 山が ${a.peakDb.toFixed(1)}dBFS です（−3dBFS 以下に）`);
  const max = SE_MAX_SEC[recipe.kind];
  if (a.lengthSec > max) out.push(`${name}: 長さが ${a.lengthSec.toFixed(2)} 秒です（${recipe.kind} は ${max} 秒まで）`);
  if (!recipe.soft && a.attackMs > 10) out.push(`${name}: 立ち上がりに ${a.attackMs.toFixed(0)}ms かかっています（10ms 以内が目安。ゆっくりが意図なら soft:true）`);
  if (a.dc > 0.02) out.push(`${name}: 直流成分があります（山の ${(a.dc * 100).toFixed(1)}%）`);
  if (recipe.kind === "ui" && a.band1to4k < 0.15) out.push(`${name}: UI の音なのに 1〜4kHz のエネルギーが ${(a.band1to4k * 100).toFixed(0)}% しかありません（聞き取りやすい帯域）`);
  return out;
}

/** レシピを描いて分析し、検査まで通す。 */
export function inspectSe(recipe: SfxRecipe, sr = 22050): { analysis: SeAnalysis; warnings: string[]; samples: Float32Array } {
  const samples = renderSfx(recipe, sr);
  const analysis = analyzeSamples(samples, sr);
  return { analysis, warnings: checkSe(analysis, recipe), samples };
}

// ───────── 変化づけ ─────────
const scaleFreq = (l: Layer, k: number): Layer => {
  if (l.kind === "tone") return { ...l, f0: l.f0 * k, f1: l.f1 ? l.f1 * k : undefined, fpath: l.fpath?.map(([t, f]) => [t, f * k] as [number, number]) };
  if (l.kind === "fm") return { ...l, fc: l.fc * k };
  return l;
};
const scaleFilter = (f: FilterSpec, k: number): FilterSpec => ({ ...f, f0: f.f0 * k, f1: f.f1 ? f.f1 * k : undefined, path: f.path?.map(([t, v]) => [t, v * k] as [number, number]) });

/**
 * 発音のたびの変化づけ（純関数。rng を差し替えられる）。ピッチ ±vary.pitch、音量 ±vary.gainDb、フィルター中心 ±vary.filter。
 * vary が無いレシピはそのまま返す。
 */
export function varySe(recipe: SfxRecipe, rng: () => number): SfxRecipe {
  const v = recipe.vary;
  if (!v) return recipe;
  const pitch = 1 + (rng() * 2 - 1) * (v.pitch ?? 0);
  const filt = 1 + (rng() * 2 - 1) * (v.filter ?? 0);
  const gain = (rng() * 2 - 1) * (v.gainDb ?? 0);
  return {
    ...recipe,
    layers: recipe.layers.map((l, i) => {
      const moved = scaleFreq(l, pitch);
      return { ...moved, db: moved.db + (i === 0 ? gain : 0), filter: moved.filter?.map((f) => scaleFilter(f, filt)) };
    }),
  };
}

/** SE ラボのスライダー用の調整。pitch＝周波数の倍率、time＝時間の倍率（at・包絡の A/D/保持/R）、attack/release＝A・R の倍率、peakDb＝山の高さ（−3 を超えない）。 */
export interface SeAdjust { pitch?: number; time?: number; attack?: number; release?: number; peakDb?: number }
export function adjustSe(recipe: SfxRecipe, a: SeAdjust): SfxRecipe {
  const pitch = a.pitch ?? 1, time = a.time ?? 1, atk = a.attack ?? 1, rel = a.release ?? 1;
  const layers = recipe.layers.map((l0) => {
    const l = pitch === 1 ? l0 : scaleFreq(l0, pitch);
    const e = l.env;
    return { ...l, at: l.at * time, env: { ...e, a: e.a * time * atk, d: e.d * time, r: e.r * time * rel, ...(e.hold ? { hold: e.hold * time } : {}) } } as Layer;
  });
  return { ...recipe, layers, lengthSec: recipe.lengthSec * time, ...(a.peakDb !== undefined ? { peakDb: Math.min(-3, a.peakDb) } : {}) };
}

/** 変種を n 個作る（足音など。ラウンドロビンで回す）。種が同じなら同じ変種。 */
export function makeVariants(recipe: SfxRecipe, n = 4, seed = 1): SfxRecipe[] {
  const rng = makeRng(seed ^ hashId(recipe.id));
  return Array.from({ length: n }, () => varySe(recipe, rng));
}

/** 再発音の間引き。同じ id を minGapMs 以内に鳴らそうとしたら false。 */
export class SeThrottle {
  private last = new Map<string, number>();
  allow(id: string, nowMs: number, minGapMs: number): boolean {
    const prev = this.last.get(id);
    if (prev !== undefined && nowMs - prev < minGapMs) return false;
    this.last.set(id, nowMs);
    return true;
  }
}

/** ラウンドロビン（id ごとに 0..n-1 を順に返す）。 */
export class RoundRobin {
  private i = new Map<string, number>();
  next(id: string, n: number): number {
    const k = (this.i.get(id) ?? -1) + 1;
    const v = k % Math.max(1, n);
    this.i.set(id, v);
    return v;
  }
}

// ───────── 調に合わせる ─────────
/** 周波数を、音階の音のいちばん近い所へ寄せる（最大 ±maxSemi 半音。範囲に音階の音がなければそのまま）。 */
export function snapFrequency(f: number, pcs: number[], maxSemi = 2): number {
  const midi = 69 + 12 * Math.log2(f / 440);
  const r = Math.round(midi);
  if (Math.abs(midi - r) > 0.5 + 1e-9) return f;
  const set = new Set(pcs);
  for (let d = 0; d <= maxSemi; d++) {
    for (const m of d === 0 ? [r] : [r - d, r + d]) if (set.has(((m % 12) + 12) % 12)) return 440 * 2 ** ((m - 69) / 12);
  }
  return f;
}

/**
 * ※調の SE（tune:true の層）の周波数を、BGM の調の音階の音へ寄せる（最大 ±2 半音）。
 * tonic＝主音（0〜11）、scale＝音階（既定は長調）。短調なら "aeolian"、和風なら "miyako" など。
 */
export function tuneSe(recipe: SfxRecipe, tonic: number, scale: Scale | string = "ionian"): SfxRecipe {
  const sc = typeof scale === "string" ? findScale(scale) : scale;
  if (!sc) return recipe;
  const pcs = scalePitchClasses(sc, tonic);
  const retune = (l: Layer): Layer => {
    if (!l.tune) return l;
    if (l.kind === "tone") {
      const f0 = snapFrequency(l.f0, pcs);
      const k = f0 / l.f0;
      return { ...l, f0, f1: l.f1 ? l.f1 * k : undefined, fpath: l.fpath?.map(([t, f]) => [t, f * k] as [number, number]) };
    }
    if (l.kind === "fm") return { ...l, fc: snapFrequency(l.fc, pcs) };
    return l;
  };
  return { ...recipe, layers: recipe.layers.map(retune) };
}

// ───────── BGM のダッキング ─────────
/** BGM を下げる量（dB）。ガイド 10-6: UI＝なし、通知＝−2、警告＝−4、ファンファーレ＝−8。 */
export const DUCK_DB: Record<DuckLevel, number> = { none: 0, notice: -2, warning: -4, fanfare: -8 };
export const DUCK_ATTACK_SEC = 0.01;
export const DUCK_RELEASE_SEC = 0.5;

export function duckLevelOf(recipe: Pick<SfxRecipe, "kind" | "duck">): DuckLevel {
  return recipe.duck ?? (recipe.kind === "fanfare" ? "fanfare" : recipe.kind === "notice" ? "notice" : "none");
}

/** AudioParam のように setTargetAtTime を持つもの（テストでは記録用の偽物を渡せる）。 */
export interface DuckParam {
  setTargetAtTime(target: number, startTime: number, timeConstant: number): unknown;
}

/**
 * BGM のバスのゲインを、SE の間だけ level の分だけ下げ、holdSec 後に元（1）へ戻す。
 * アタック 10ms（時定数 3ms）、戻り 約 0.5 秒（時定数 0.15）。none なら何もしない。返り値は下げた量（リニア）。
 */
export function duckBgmForSe(param: DuckParam, level: DuckLevel, now: number, holdSec: number): number {
  const db = DUCK_DB[level];
  if (!db) return 1;
  const g = dbToGain(db);
  param.setTargetAtTime(g, now, DUCK_ATTACK_SEC / 3);
  param.setTargetAtTime(1, now + Math.max(0.05, holdSec), DUCK_RELEASE_SEC / 3);
  return g;
}

// ───────── Web Audio で鳴らす ─────────
const bufferCache = new WeakMap<BaseAudioContext, Map<string, AudioBuffer>>();

/** レシピを AudioBuffer にする（同じ文脈・同じ内容はキャッシュ）。 */
export function sfxBuffer(ctx: BaseAudioContext, recipe: SfxRecipe, cacheKey = recipe.id): AudioBuffer {
  let m = bufferCache.get(ctx);
  if (!m) { m = new Map(); bufferCache.set(ctx, m); }
  let buf = m.get(cacheKey);
  if (!buf) {
    const data = renderSfx(recipe, ctx.sampleRate);
    buf = ctx.createBuffer(1, data.length, ctx.sampleRate);
    buf.getChannelData(0).set(data);
    m.set(cacheKey, buf);
  }
  return buf;
}

/** 鳴らす。gainDb は音量の調整、pan は左右。返り値は再生ノード。 */
export function playSfx(ctx: BaseAudioContext, dest: AudioNode, recipe: SfxRecipe, when = ctx.currentTime, opts: { gainDb?: number; pan?: number; cacheKey?: string } = {}): AudioBufferSourceNode {
  const src = ctx.createBufferSource();
  src.buffer = sfxBuffer(ctx, recipe, opts.cacheKey);
  const g = ctx.createGain();
  g.gain.value = dbToGain(opts.gainDb ?? 0);
  src.connect(g);
  let node: AudioNode = g;
  if (opts.pan && "createStereoPanner" in ctx) {
    const p = (ctx as AudioContext).createStereoPanner();
    p.pan.value = Math.max(-1, Math.min(1, opts.pan));
    g.connect(p);
    node = p;
  }
  node.connect(dest);
  src.start(when);
  return src;
}
