import { arrange, midiToName, type Arrangement, type MelodySpec, type PartSpec, type Section } from "./compose";
import type { Score } from "./score";

/**
 * 曲の設計図（調・速さ・曲調・乱数の種）から、1〜1分半のオリジナル曲を組み立てる「作曲エンジン」。
 * コード進行は定番の型の組み合わせ、旋律は「コードの音を軸に音階を歩く」規則で作る。同じ設計図からは毎回同じ曲ができる。
 * 特定の既存曲の旋律・進行をなぞらない（`CLAUDE.md` 1-1）。曲の良し悪しは耳で聴いて設計図（種など）を調整する。
 */

export type Style =
  | "rock" | "metal" | "classic" | "space" | "cafe" | "discord" | "mystery" | "epic" | "folk"
  | "baroque" | "nature" | "phonk" | "samba" | "jazz" | "rnb" | "electro" | "hardcore" | "deathmetal" | "progmetal" | "jpop";

export interface SongSpec {
  id: string;
  title: string;
  /** 使う場面（例: 「第1章・麦香野の村」）。 */
  scene: string;
  style: Style;
  /** 主音（"C"・"F#"・"Bb" など）。 */
  tonic: string;
  minor: boolean;
  bpm: number;
  /** 乱数の種。旋律や進行を変えたいときに変える。 */
  seed: number;
  /** 1小節の拍数（既定4。クラシック調の3拍子などで3）。 */
  beats?: 3 | 4 | 7;
  /** 疾走感を出す（ボス戦向け）。16分の刻み・アルペジオ・8分のキックを足す。4拍子の曲だけ。 */
  drive?: boolean;
  /** 曲の長さの目安（秒。既定75）。 */
  targetSec?: number;
}

// ── 乱数（同じ種なら同じ結果） ──
export function makeRng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export type Rng = () => number;
export const pick = <T,>(rng: Rng, xs: readonly T[]): T => xs[Math.floor(rng() * xs.length)];

// ── 調・和音 ──
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const PC: Record<string, number> = { C: 0, "C#": 1, Db: 1, D: 2, "D#": 3, Eb: 3, E: 4, F: 5, "F#": 6, Gb: 6, G: 7, "G#": 8, Ab: 8, A: 9, "A#": 10, Bb: 10, B: 11 };
const MAJOR = [0, 2, 4, 5, 7, 9, 11];
const MINOR = [0, 2, 3, 5, 7, 8, 10];

export interface Key {
  tonic: number;
  scale: number[];
  minor: boolean;
}
export function keyOf(spec: { tonic: string; minor: boolean }): Key {
  return { tonic: PC[spec.tonic], scale: spec.minor ? MINOR : MAJOR, minor: spec.minor };
}
const degreeSemis = (k: Key, i: number): number => k.scale[i % 7] + 12 * Math.floor(i / 7);

/** 度数（1〜7）の和音の名前（"Am"・"G7"・"Fmaj7" など）。 */
export function chordName(k: Key, degree: number, sevenths: boolean, opts?: { leadingDim?: boolean }): string {
  const i = degree - 1;
  if (opts?.leadingDim && degree === 7 && k.minor) {
    return `${NAMES[(k.tonic + 11) % 12]}dim`;
  }
  const rootSemi = degreeSemis(k, i);
  const root = NAMES[(k.tonic + rootSemi) % 12];
  let t3 = degreeSemis(k, i + 2) - rootSemi;
  const t5 = degreeSemis(k, i + 4) - rootSemi;
  const t7 = degreeSemis(k, i + 6) - rootSemi;
  if (k.minor && degree === 5) {
    t3 = 4; // 短調の属和音は長三和音にして、主和音へ戻る力を出す
  }
  if (sevenths) {
    if (t3 === 4 && t7 === 11) return `${root}maj7`;
    if (t3 === 4 && t7 === 10) return `${root}7`;
    if (t3 === 3 && t7 === 10) return `${root}m7`;
  }
  if (t3 === 3 && t5 === 6) return `${root}dim`;
  return t3 === 3 ? `${root}m` : root;
}
/** 和音を構成する音の高さクラス（0〜11）。 */
function chordPitchClasses(name: string): number[] {
  const m = /^([A-G]#?)(maj7|m7|m|7|dim)?$/.exec(name);
  if (!m) throw new Error(`和音名を読めません: ${name}`);
  const root = PC[m[1]];
  const shape = { "": [0, 4, 7], m: [0, 3, 7], "7": [0, 4, 7, 10], maj7: [0, 4, 7, 11], m7: [0, 3, 7, 10], dim: [0, 3, 6] }[m[2] ?? ""]!;
  return shape.map((x) => (root + x) % 12);
}

// 定番のコード進行の型（度数）。4小節ずつ。
export const CELLS_MAJOR = [[1, 5, 6, 4], [1, 6, 4, 5], [6, 4, 1, 5], [1, 4, 5, 1], [2, 5, 1, 6], [1, 3, 4, 5], [4, 5, 3, 6], [1, 4, 6, 5], [1, 5, 4, 5], [6, 5, 4, 5]];
export const CELLS_MINOR = [[1, 6, 3, 7], [1, 4, 7, 3], [1, 7, 6, 7], [1, 4, 5, 1], [6, 7, 1, 1], [1, 6, 7, 1], [4, 7, 1, 5], [1, 3, 7, 6], [1, 4, 6, 5], [1, 7, 4, 5]];

type Kind = "intro" | "verse" | "bridge" | "chorus" | "solo" | "outro";

interface Plan {
  kinds: Kind[];
}
function planSections(bpm: number, beats: number, targetSec: number): Plan {
  const barsWanted = (targetSec * bpm) / 60 / beats;
  let k = Math.round((barsWanted - 4) / 8);
  k = Math.max(2, Math.min(8, k));
  const dur = (kk: number): number => ((4 + 8 * kk) * beats * 60) / bpm;
  while (dur(k) > 90 && k > 2) k--;
  while (dur(k) < 60 && k < 8) k++;
  const body: Kind[] = {
    2: ["verse", "chorus"],
    3: ["verse", "bridge", "chorus"],
    4: ["verse", "verse", "bridge", "chorus"],
    5: ["verse", "verse", "bridge", "chorus", "outro"],
    6: ["verse", "verse", "bridge", "chorus", "solo", "outro"],
    7: ["verse", "verse", "bridge", "chorus", "verse", "chorus", "outro"],
    8: ["verse", "verse", "bridge", "chorus", "verse", "bridge", "chorus", "outro"],
  }[k] as Kind[];
  return { kinds: ["intro", ...body] };
}

// ── 旋律 ──
const RHYTHM4 = [[2, 2], [1, 1, 2], [1, 1, 1, 1], [1.5, 0.5, 1, 1], [2, 1, 1], [1, 2, 1], [0.5, 0.5, 1, 2], [1, 1, 0.5, 0.5, 1], [3, 1], [1, 0.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2], [1.5, 1.5, 1]];
const RHYTHM3 = [[3], [2, 1], [1, 2], [1, 1, 1], [1.5, 0.5, 1], [1, 0.5, 0.5, 1], [2, 0.5, 0.5]];
const RHYTHM7 = [[2, 2, 3], [1.5, 1.5, 2, 2], [3, 2, 2], [1, 1, 1, 1, 3], [2, 1, 1, 3]];
const RHYTHM_SPARSE4 = [[4], [3, 1], [2, 2], [1, 3], [2, 1, 1]];
const RHYTHM_FAST4 = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 1, 1], [0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25]];

export interface MelodyOpts {
  /** 3拍子で、2小節を「2拍×3」でまとめる（ヘミオラ）。 */
  hemiola?: boolean;
  lo: number;
  hi: number;
  density: "normal" | "sparse" | "fast";
  restChance?: number;
}

export function generateMelody(rng: Rng, key: Key, chords: string[], beats: number, opts: MelodyOpts): string {
  const pool: number[] = [];
  for (let m = opts.lo; m <= opts.hi; m++) {
    if (key.scale.includes(((m - key.tonic) % 12 + 12) % 12)) pool.push(m);
  }
  const mid = (opts.lo + opts.hi) / 2;
  let cur = pool.reduce((best, m, i) => (Math.abs(m - mid) < Math.abs(pool[best] - mid) ? i : best), 0);
  const tables = beats === 7 ? [RHYTHM7] : beats === 3 ? [RHYTHM3] : opts.density === "sparse" ? [RHYTHM_SPARSE4] : opts.density === "fast" && beats === 4 ? [RHYTHM_FAST4] : [beats === 3 ? RHYTHM3 : RHYTHM4];
  const rhythmFor = (): number[] => pick(rng, tables[0]);
  const out: string[] = [];
  const rhythms: number[][] = [];
  const skip = new Set<number>();
  chords.forEach((chord, bar) => {
    if (skip.has(bar)) {
      return;
    }
    const tones = chordPitchClasses(chord);
    if (opts.hemiola && beats === 3 && bar % 2 === 0 && bar + 1 < chords.length - 1) {
      // ヘミオラ: 3拍子の2小節（6拍）を、2拍ずつの3つの音にまとめる
      skip.add(bar + 1);
      rhythms[bar] = [2, 2, 2];
      rhythms[bar + 1] = [2, 2, 2];
      const arch = mid + Math.sin(((bar % 8) / 8) * Math.PI) * ((opts.hi - opts.lo) * 0.28);
      [chord, chord, chords[bar + 1]].forEach((c, n) => {
        const t = chordPitchClasses(c);
        let best = cur;
        let bestScore = Infinity;
        for (let i = Math.max(0, cur - 4); i <= Math.min(pool.length - 1, cur + 4); i++) {
          if (!t.includes(pool[i] % 12) && n !== 1) continue;
          const score = Math.abs(i - cur) + Math.abs(pool[i] - arch) * 0.08 + rng() * 1.2;
          if (score < bestScore) {
            bestScore = score;
            best = i;
          }
        }
        cur = best;
        out.push(`${midiToName(pool[cur])}:2`);
      });
      return;
    }
    let rhythm: number[];
    if (bar === chords.length - 1) {
      rhythm = [1, beats - 1];
    } else if (bar % 4 === 3) {
      rhythm = beats === 3 ? [1, 2] : beats === 7 ? [1, 1, 5] : opts.density === "fast" ? rhythmFor() : [1, 1, 2];
    } else if (bar % 4 >= 2 && rng() < 0.65 && rhythms[bar - 2]?.reduce((a, b) => a + b, 0) === beats) {
      rhythm = rhythms[bar - 2];
    } else {
      rhythm = rhythmFor();
    }
    rhythms.push(rhythm);
    // 小節ごとの目標の高さ（フレーズが山なりになる）
    const arch = mid + Math.sin(((bar % 8) / 8) * Math.PI) * ((opts.hi - opts.lo) * 0.28) - (opts.hi - opts.lo) * 0.1;
    rhythm.forEach((dur, n) => {
      const strong = n === 0 || dur >= 2;
      if (strong || bar === chords.length - 1) {
        // 和音の音のうち、いまの音にいちばん近いものへ
        let best = cur;
        let bestScore = Infinity;
        for (let i = Math.max(0, cur - 4); i <= Math.min(pool.length - 1, cur + 4); i++) {
          if (!tones.includes(pool[i] % 12)) continue;
          const score = Math.abs(i - cur) + Math.abs(pool[i] - arch) * 0.08 + rng() * 1.2;
          if (score < bestScore) {
            bestScore = score;
            best = i;
          }
        }
        cur = best;
      } else {
        const r = rng();
        let step = r < 0.08 ? -2 : r < 0.4 ? -1 : r < 0.5 ? 0 : r < 0.82 ? 1 : r < 0.92 ? 2 : r < 0.96 ? -3 : 3;
        if (pool[cur] > arch + 4 && step > 0 && rng() < 0.6) step = -step;
        if (pool[cur] < arch - 4 && step < 0 && rng() < 0.6) step = -step;
        cur = Math.max(0, Math.min(pool.length - 1, cur + step));
      }
      const rest = opts.restChance && n > 0 && rng() < opts.restChance && bar !== chords.length - 1;
      out.push(rest ? `R:${dur}` : `${midiToName(pool[cur])}:${dur}`);
    });
  });
  return out.join(" ");
}

// ── 曲調ごとの楽器編成とパターン ──
interface KindPlan {
  parts: Record<string, string>;
  /** 旋律を鳴らすパート（同じ旋律を重ねるときは複数）。 */
  mel: string[];
  opts: MelodyOpts;
}
interface Template {
  parts: Record<string, PartSpec>;
  melodies: Record<string, MelodySpec>;
  sevenths: boolean;
  plan: (kind: Kind, bpb: number) => KindPlan;
}

const drum = (instrument: "kick" | "snare" | "hihat" | "crash", volume: number, fixed: string): PartSpec => ({ instrument, waveform: "sine", volume, octave: 2, step: 0.25, fixed });
const CRASH4 = "x............... ................ ................ ................";
const ROCK_V = { kick: "x.......x.x.....", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
const ROCK_C = { kick: "x.....x.x.x...x.", snare: "....x.......x...", hat: "xxxxxxxxxxxxxxxx" };
const KEYS3 = { k1: "a-------", k2: "b-------", k3: "c-------" };

const TEMPLATES: Record<Exclude<Style, "discord" | "mystery">, Template> = {
  baroque: {
    // バロック協奏曲風: 速い弦の音型、チェンバロの通奏低音、5度で下がる進行の反復。特定の曲の旋律は使っていない
    sevenths: false,
    parts: {
      cello: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.5 },
      hpsi: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.1, octave: 4, step: 0.25 },
      vf: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
      v2: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
      v3: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
    },
    melodies: { violin: { instrument: "strings", waveform: "sawtooth", volume: 0.15 }, hpsi2: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.14 } },
    plan: (kind) => {
      const walk = "RcbcRcbc";
      const arp = "abcbabcbabcbabcb";
      const fig = "acbcacbcacbcacbc";
      const inner = { v2: "b-------", v3: "c-------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { cello: walk, hpsi: arp, ...inner }, mel: ["violin"], opts: { lo: 67, hi: 88, density: "fast" } },
        verse: { parts: { cello: walk, hpsi: arp }, mel: ["violin"], opts: { lo: 64, hi: 86, density: "normal" } },
        bridge: { parts: { cello: walk, hpsi: arp, vf: fig }, mel: ["violin"], opts: { lo: 66, hi: 90, density: "fast" } },
        chorus: { parts: { cello: walk, hpsi: arp, vf: fig, ...inner }, mel: ["violin"], opts: { lo: 69, hi: 91, density: "fast" } },
        solo: { parts: { cello: walk, hpsi: arp, vf: fig }, mel: ["hpsi2"], opts: { lo: 67, hi: 93, density: "fast" } },
        outro: { parts: { cello: walk, hpsi: arp, vf: fig, ...inner }, mel: ["violin"], opts: { lo: 67, hi: 89, density: "fast" } },
      };
      return rest[kind];
    },
  },
  nature: {
    sevenths: true,
    parts: {
      p1: { instrument: "pad", waveform: "sine", volume: 0.08, octave: 3, step: 0.5 },
      p2: { instrument: "pad", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
      p3: { instrument: "pad", waveform: "sine", volume: 0.07, octave: 4, step: 0.5 },
      wind: { instrument: "wind", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      stream: { instrument: "stream", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      rain: { instrument: "rain", waveform: "sine", volume: 0.05, octave: 4, step: 0.5 },
      bird: { instrument: "bird", waveform: "sine", volume: 0.09, octave: 7, step: 0.5 },
      bug: { instrument: "crickets", waveform: "sine", volume: 0.04, octave: 8, step: 0.5 },
      harp: { instrument: "guitar", waveform: "triangle", volume: 0.1, octave: 4, step: 0.5 },
    },
    melodies: { flute: { instrument: "lead", waveform: "triangle", volume: 0.12 }, chimes: { instrument: "bell", waveform: "sine", volume: 0.08 } },
    plan: (kind) => {
      const bed = { wind: "R-------", stream: "R-------", p1: "a-------", p2: "b-------", p3: "c-------" };
      const birds = "R....... ........ ....R... ........";
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { wind: bed.wind, stream: bed.stream, p1: bed.p1 }, mel: [], opts: { lo: 64, hi: 82, density: "sparse" } },
        verse: { parts: { ...bed, harp: "a.b.c.b.", bird: birds }, mel: ["flute"], opts: { lo: 64, hi: 83, density: "sparse", restChance: 0.15 } },
        bridge: { parts: { ...bed, harp: "a.b.c.b.", rain: "R-------" }, mel: ["chimes"], opts: { lo: 69, hi: 90, density: "sparse" } },
        chorus: { parts: { ...bed, harp: "a.b.c.b.", bird: birds }, mel: ["flute", "chimes"], opts: { lo: 67, hi: 88, density: "sparse" } },
        solo: { parts: { ...bed, harp: "abcbabcb" }, mel: ["flute"], opts: { lo: 67, hi: 90, density: "normal" } },
        outro: { parts: { ...bed, bug: "R-------" }, mel: ["flute"], opts: { lo: 64, hi: 82, density: "sparse", restChance: 0.15 } },
      };
      return rest[kind];
    },
  },
  phonk: {
    // 暗い短調、808の重い低音、カウベルの旋律、ハイハットの連打。テンポは半分に数えるノリ
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), clap: drum("snare", 0.24, "C3"), hat: drum("hihat", 0.1, "C6"),
      sub: { instrument: "sub808", waveform: "sine", volume: 0.34, octave: 2, step: 0.25 },
      pad: { instrument: "pad", waveform: "sawtooth", volume: 0.06, octave: 3, step: 0.5 },
      pad2: { instrument: "pad", waveform: "sawtooth", volume: 0.06, octave: 3, step: 0.5 },
      chop: { instrument: "lead", waveform: "square", volume: 0.07, octave: 4, step: 0.25 },
    },
    melodies: { cow: { instrument: "cowbell", waveform: "square", volume: 0.16 }, vox: { instrument: "lead", waveform: "triangle", volume: 0.11 } },
    plan: (kind) => {
      const beat = { kick: "x..x....x.x.....", clap: "........x.......", hat: "x.x.x.x.x.xxxxxx" };
      const half = { kick: "x.......x.......", clap: "........x.......", hat: "x.x.x.x.x.x.x.x." };
      const sub = "R..R....R.R.....";
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { hat: "x.x.x.x.x.x.x.x.", pad: "a-------", pad2: "b-------", sub: "R---------------" }, mel: ["cow"], opts: { lo: 64, hi: 84, density: "sparse" } },
        verse: { parts: { ...half, sub, pad: "a-------", chop: "a..a..a.a..a...." }, mel: ["cow"], opts: { lo: 62, hi: 80, density: "sparse", restChance: 0.15 } },
        bridge: { parts: { ...beat, sub, pad: "a-------", pad2: "b-------" }, mel: ["vox"], opts: { lo: 65, hi: 84, density: "sparse", restChance: 0.2 } },
        chorus: { parts: { ...beat, sub, pad: "a-------", pad2: "b-------", chop: "a..a..a.a..a...." }, mel: ["cow"], opts: { lo: 67, hi: 88, density: "normal" } },
        solo: { parts: { ...beat, sub, pad: "a-------" }, mel: ["cow"], opts: { lo: 67, hi: 91, density: "fast" } },
        outro: { parts: { ...half, sub, pad: "a-------" }, mel: ["cow"], opts: { lo: 62, hi: 82, density: "sparse", restChance: 0.15 } },
      };
      return rest[kind];
    },
  },
  samba: {
    sevenths: true,
    parts: {
      kick: drum("kick", 0.26, "C2"), snare: drum("snare", 0.14, "C3"), hat: drum("hihat", 0.09, "C6"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.25 },
      gtr: { instrument: "guitar", waveform: "sawtooth", volume: 0.15, octave: 3, step: 0.25 },
      k1: { instrument: "piano", waveform: "triangle", volume: 0.09, octave: 4, step: 0.5 },
      k2: { instrument: "piano", waveform: "triangle", volume: 0.09, octave: 4, step: 0.5 },
      k3: { instrument: "piano", waveform: "triangle", volume: 0.09, octave: 4, step: 0.5 },
      bell: { instrument: "chime", waveform: "sine", volume: 0.06, octave: 6, step: 0.5 },
    },
    melodies: { flute: { instrument: "lead", waveform: "triangle", volume: 0.14 }, keysm: { instrument: "keys", waveform: "sine", volume: 0.15 } },
    plan: (kind) => {
      const dr = { kick: "x..x..x.x..x..x.", snare: "..x..x.x..x..x.x", hat: "x.xxx.xxx.xxx.xx" };
      const bass = "R..R..5.R..R..5.";
      const gtr = "a.bb.cb.a.bb.cb.";
      const comp = { k1: "a-b-a-b-", k2: "b-c-b-c-", k3: "c-a-c-a-" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...dr, bass }, mel: ["flute"], opts: { lo: 67, hi: 86, density: "normal" } },
        verse: { parts: { ...dr, bass, gtr }, mel: ["flute"], opts: { lo: 64, hi: 83, density: "normal" } },
        bridge: { parts: { ...dr, bass, gtr, ...comp }, mel: ["keysm"], opts: { lo: 66, hi: 86, density: "normal" } },
        chorus: { parts: { ...dr, bass, gtr, ...comp, bell: "a...c...b...a..." .slice(0, 8) }, mel: ["flute", "keysm"], opts: { lo: 69, hi: 90, density: "normal" } },
        solo: { parts: { ...dr, bass, gtr, ...comp }, mel: ["keysm"], opts: { lo: 69, hi: 92, density: "fast" } },
        outro: { parts: { ...dr, bass, gtr, ...comp }, mel: ["flute"], opts: { lo: 66, hi: 86, density: "normal" } },
      };
      return rest[kind];
    },
  },
  jazz: {
    sevenths: true,
    parts: {
      kick: { instrument: "kick", waveform: "sine", volume: 0.12, octave: 2, step: 1 / 3, fixed: "C2" },
      snare: { instrument: "snare", waveform: "sine", volume: 0.1, octave: 2, step: 1 / 3, fixed: "C3" },
      ride: { instrument: "hihat", waveform: "sine", volume: 0.09, octave: 2, step: 1 / 3, fixed: "C6" },
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 1 },
      comp: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      comp2: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      comp3: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      comp4: { instrument: "keys", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
    },
    melodies: { gtr: { instrument: "guitar", waveform: "sawtooth", volume: 0.17 }, keysm: { instrument: "keys", waveform: "sine", volume: 0.15 }, lead: { instrument: "lead", waveform: "triangle", volume: 0.13 } },
    plan: (kind) => {
      const swing = { ride: "x.xx.xx.xx.x", kick: "x..x..x..x..", snare: "..x.......x." };
      const walk = "abcb";
      const comp = { comp: "a--.a---", comp2: "b--.b---", comp3: "c--.c---", comp4: "d--.d---" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ride: swing.ride, bass: walk, ...comp }, mel: ["keysm"], opts: { lo: 64, hi: 82, density: "normal" } },
        verse: { parts: { ...swing, bass: walk, ...comp }, mel: ["gtr"], opts: { lo: 62, hi: 80, density: "normal" } },
        bridge: { parts: { ...swing, bass: walk, ...comp }, mel: ["lead"], opts: { lo: 64, hi: 84, density: "normal" } },
        chorus: { parts: { ...swing, bass: walk, ...comp }, mel: ["keysm"], opts: { lo: 66, hi: 86, density: "normal" } },
        solo: { parts: { ...swing, bass: walk, ...comp }, mel: ["gtr"], opts: { lo: 66, hi: 90, density: "fast" } },
        outro: { parts: { ride: swing.ride, bass: walk, ...comp }, mel: ["keysm"], opts: { lo: 62, hi: 82, density: "normal" } },
      };
      return rest[kind];
    },
  },
  rnb: {
    sevenths: true,
    parts: {
      kick: drum("kick", 0.26, "C2"), snare: drum("snare", 0.2, "C3"), hat: drum("hihat", 0.08, "C6"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.32, octave: 2, step: 0.5 },
      k1: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      k2: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      k3: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      k4: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      pad: { instrument: "pad", waveform: "sine", volume: 0.07, octave: 4, step: 0.5 },
    },
    melodies: { vox: { instrument: "lead", waveform: "triangle", volume: 0.15 }, keysm: { instrument: "keys", waveform: "sine", volume: 0.15 } },
    plan: (kind) => {
      const dr = { kick: "x.....x..x......", snare: "........x.......", hat: "x.xxx.xxx.xxx.xx" };
      const comp = { k1: "a--a---.", k2: "b--b---.", k3: "c--c---.", k4: "d--d---." };
      const bass = "R-.R--5-";
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...comp, pad: "a-------" }, mel: ["keysm"], opts: { lo: 64, hi: 82, density: "sparse", restChance: 0.2 } },
        verse: { parts: { ...dr, bass, ...comp }, mel: ["vox"], opts: { lo: 62, hi: 79, density: "sparse", restChance: 0.15 } },
        bridge: { parts: { ...dr, bass, ...comp, pad: "a-------" }, mel: ["vox"], opts: { lo: 65, hi: 84, density: "normal", restChance: 0.1 } },
        chorus: { parts: { ...dr, bass, ...comp, pad: "a-------" }, mel: ["vox", "keysm"], opts: { lo: 67, hi: 86, density: "normal", restChance: 0.1 } },
        solo: { parts: { ...dr, bass, ...comp }, mel: ["keysm"], opts: { lo: 67, hi: 88, density: "fast" } },
        outro: { parts: { ...comp, bass, pad: "a-------" }, mel: ["vox"], opts: { lo: 62, hi: 81, density: "sparse", restChance: 0.2 } },
      };
      return rest[kind];
    },
  },
  electro: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), snare: drum("snare", 0.2, "C3"), hat: drum("hihat", 0.1, "C6"), crash: drum("crash", 0.12, "C5"),
      bass: { instrument: "bass", waveform: "sawtooth", volume: 0.26, octave: 2, step: 0.25 },
      arp: { instrument: "lead", waveform: "square", volume: 0.09, octave: 4, step: 0.25 },
      pad: { instrument: "pad", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
      pad2: { instrument: "pad", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
      pad3: { instrument: "pad", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
    },
    melodies: { lead: { instrument: "lead", waveform: "sawtooth", volume: 0.13 }, bell: { instrument: "chime", waveform: "sine", volume: 0.1 } },
    plan: (kind) => {
      const four = { kick: "x...x...x...x...", hat: "..x...x...x...x." };
      const full = { ...four, snare: "....x.......x...", crash: CRASH4 };
      const bass = "R.R.RR.RR.R.RR.R";
      const arp = "abcdabcdabcdabcd";
      const pads = { pad: "a-------", pad2: "b-------", pad3: "c-------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { hat: four.hat, arp, ...pads }, mel: ["bell"], opts: { lo: 72, hi: 92, density: "sparse" } },
        verse: { parts: { ...four, bass, arp }, mel: ["lead"], opts: { lo: 64, hi: 82, density: "normal" } },
        bridge: { parts: { ...four, bass, arp, ...pads }, mel: ["lead"], opts: { lo: 67, hi: 86, density: "normal" } },
        chorus: { parts: { ...full, bass, arp, ...pads }, mel: ["lead"], opts: { lo: 69, hi: 90, density: "normal" } },
        solo: { parts: { ...full, bass, arp }, mel: ["lead"], opts: { lo: 69, hi: 93, density: "fast" } },
        outro: { parts: { ...full, bass, arp, ...pads }, mel: ["lead"], opts: { lo: 67, hi: 88, density: "normal" } },
      };
      return rest[kind];
    },
  },
  hardcore: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), snare: drum("snare", 0.3, "C3"), hat: drum("hihat", 0.11, "C6"), crash: drum("crash", 0.16, "C5"),
      gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.21, octave: 2, step: 0.25 },
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.25 },
    },
    melodies: { gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 } },
    plan: (kind) => {
      const dbeat = { kick: "x.xx..x.x.xx..x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
      const riff = "R.R.R.R.R.R.R.R.";
      const gallop = "R.RRR.RRR.RRR.RR";
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...dbeat, crash: CRASH4, gtrs: riff, bass: riff }, mel: ["gtr"], opts: { lo: 69, hi: 90, density: "sparse" } },
        verse: { parts: { ...dbeat, gtrs: gallop, bass: riff }, mel: [], opts: { lo: 62, hi: 79, density: "normal" } },
        bridge: { parts: { ...dbeat, gtrs: riff, bass: riff }, mel: ["gtr"], opts: { lo: 66, hi: 86, density: "normal" } },
        chorus: { parts: { ...dbeat, crash: CRASH4, gtrs: gallop, bass: riff }, mel: ["gtr"], opts: { lo: 69, hi: 91, density: "normal" } },
        solo: { parts: { ...dbeat, gtrs: gallop, bass: riff }, mel: ["gtr"], opts: { lo: 72, hi: 95, density: "fast" } },
        outro: { parts: { ...dbeat, crash: CRASH4, gtrs: gallop, bass: riff }, mel: ["gtr"], opts: { lo: 69, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  deathmetal: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.28, "C2"), snare: drum("snare", 0.26, "C3"), hat: drum("hihat", 0.1, "C6"), crash: drum("crash", 0.16, "C5"),
      gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.22, octave: 2, step: 0.25 },
      bass: { instrument: "bass", waveform: "sawtooth", volume: 0.26, octave: 1, step: 0.25 },
      s1: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 3, step: 0.25 },
      s2: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 3, step: 0.25 },
    },
    melodies: { gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.16 } },
    plan: (kind) => {
      const blast = { kick: "xxxxxxxxxxxxxxxx", snare: "x.x.x.x.x.x.x.x.", hat: "..x...x...x...x.", crash: CRASH4 };
      const half = { kick: "x.x.x.x.x.x.x.x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
      const trem = "RRRRRRRRRRRRRRRR";
      const slam = "R-------R---R---";
      const dim = { s1: "a---------------", s2: "b---------------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...half, gtrs: slam, bass: slam, ...dim }, mel: ["gtr"], opts: { lo: 62, hi: 82, density: "sparse" } },
        verse: { parts: { ...blast, gtrs: trem, bass: trem }, mel: [], opts: { lo: 58, hi: 76, density: "normal" } },
        bridge: { parts: { ...half, gtrs: slam, bass: slam, ...dim }, mel: ["gtr"], opts: { lo: 62, hi: 82, density: "normal" } },
        chorus: { parts: { ...blast, gtrs: trem, bass: trem, ...dim }, mel: ["gtr"], opts: { lo: 64, hi: 88, density: "normal" } },
        solo: { parts: { ...blast, gtrs: trem, bass: trem }, mel: ["gtr"], opts: { lo: 66, hi: 94, density: "fast" } },
        outro: { parts: { ...half, gtrs: slam, bass: slam }, mel: ["gtr"], opts: { lo: 62, hi: 84, density: "normal" } },
      };
      return rest[kind];
    },
  },
  progmetal: {
    // 7拍子（4+3）。ドラムは1拍を4分割、ほかは2分割で数える
    sevenths: false,
    parts: {
      kick: drum("kick", 0.28, "C2"), snare: drum("snare", 0.25, "C3"), hat: drum("hihat", 0.1, "C6"), crash: drum("crash", 0.15, "C5"),
      gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.2, octave: 2, step: 0.25 },
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.5 },
      keys: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      keys2: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      keys3: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      s1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      s2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      s3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
    },
    melodies: { gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 }, synth: { instrument: "lead", waveform: "square", volume: 0.12 } },
    plan: (kind) => {
      const dr = { kick: "x.....x.x.x.....x.....x.x...", snare: "....x.......x.......x.......", hat: "x.x.x.x.x.x.x.x.x.x.x.x.x.x." };
      const chug = "R.RR.RR.R.RR.RR.R.RR.RR.R.RR";
      const hit = "R-------R---R---R-------R---";
      const bass = "R.R.R.R.R.R.R.";
      const keys = { keys: "a-------------", keys2: "b-------------", keys3: "c-------------" };
      const st = { s1: "a-------------", s2: "b-------------", s3: "c-------------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...keys, bass: "R-------------" }, mel: ["synth"], opts: { lo: 67, hi: 88, density: "sparse" } },
        verse: { parts: { ...dr, gtrs: chug, bass }, mel: ["synth"], opts: { lo: 62, hi: 82, density: "normal" } },
        bridge: { parts: { ...dr, gtrs: hit, bass, ...keys }, mel: ["synth"], opts: { lo: 66, hi: 86, density: "normal" } },
        chorus: { parts: { ...dr, crash: "x...........................", gtrs: hit, bass, ...st }, mel: ["gtr"], opts: { lo: 69, hi: 91, density: "normal" } },
        solo: { parts: { ...dr, gtrs: chug, bass }, mel: ["gtr"], opts: { lo: 69, hi: 95, density: "normal" } },
        outro: { parts: { ...dr, gtrs: chug, bass, ...st }, mel: ["gtr"], opts: { lo: 66, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  jpop: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.27, "C2"), snare: drum("snare", 0.22, "C3"), hat: drum("hihat", 0.1, "C6"), crash: drum("crash", 0.14, "C5"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.5 },
      pn1: { instrument: "piano", waveform: "triangle", volume: 0.1, octave: 4, step: 0.5 },
      pn2: { instrument: "piano", waveform: "triangle", volume: 0.1, octave: 4, step: 0.5 },
      pn3: { instrument: "piano", waveform: "triangle", volume: 0.1, octave: 4, step: 0.5 },
      gtr: { instrument: "guitar", waveform: "sawtooth", volume: 0.13, octave: 3, step: 0.5 },
      st1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      st2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      st3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
    },
    melodies: { vox: { instrument: "lead", waveform: "triangle", volume: 0.16 }, gtrm: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.15 }, pnm: { instrument: "piano", waveform: "triangle", volume: 0.14 } },
    plan: (kind) => {
      const dr = { kick: "x...x...x...x...", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
      const chorusDr = { kick: "x.....x.x.x...x.", snare: "....x.......x...", hat: "xxxxxxxxxxxxxxxx", crash: CRASH4 };
      const pn = { pn1: "a-a-a-a-", pn2: "b-b-b-b-", pn3: "c-c-c-c-" };
      const st = { st1: "a-------", st2: "b-------", st3: "c-------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...pn, bass: "R-R-R-R-" }, mel: ["pnm"], opts: { lo: 67, hi: 86, density: "normal" } },
        verse: { parts: { ...dr, bass: "R.RR.R.R", ...pn, gtr: "abcbabcb" }, mel: ["vox"], opts: { lo: 62, hi: 80, density: "normal" } },
        bridge: { parts: { ...dr, bass: "R.RR.R.R", ...pn, gtr: "abcbabcb", ...st }, mel: ["vox"], opts: { lo: 65, hi: 84, density: "normal" } },
        chorus: { parts: { ...chorusDr, bass: "RRRRRRRR", ...pn, gtr: "abcdcbcd", ...st }, mel: ["vox", "gtrm"], opts: { lo: 69, hi: 90, density: "normal" } },
        solo: { parts: { ...chorusDr, bass: "RRRRRRRR", ...pn, ...st }, mel: ["gtrm"], opts: { lo: 69, hi: 92, density: "fast" } },
        outro: { parts: { ...chorusDr, bass: "RRRRRRRR", ...pn, gtr: "abcdcbcd", ...st }, mel: ["vox", "gtrm"], opts: { lo: 69, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  rock: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), snare: drum("snare", 0.26, "C3"), hat: drum("hihat", 0.12, "C6"), crash: drum("crash", 0.16, "C5"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.5 },
      crunch: { instrument: "crunch", waveform: "sawtooth", volume: 0.2, octave: 3, step: 0.5 },
      arp: { instrument: "guitar", waveform: "sawtooth", volume: 0.15, octave: 4, step: 0.5 },
      k1: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      k2: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
      k3: { instrument: "keys", waveform: "sine", volume: 0.1, octave: 4, step: 0.5 },
    },
    melodies: { lead: { instrument: "lead", waveform: "square", volume: 0.13 }, gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 } },
    plan: (kind) => {
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...ROCK_V, crash: CRASH4, bass: "R.RR.R.R", crunch: "R.RR.RR." }, mel: ["gtr"], opts: { lo: 66, hi: 86, density: "normal" } },
        verse: { parts: { ...ROCK_V, crash: CRASH4, bass: "R.RR.R.R", crunch: "R.RR.RR.", arp: "abcbabcb" }, mel: ["lead"], opts: { lo: 62, hi: 79, density: "normal" } },
        bridge: { parts: { ...ROCK_C, crash: CRASH4, bass: "R-R-R-5-", crunch: "R-------", arp: "abcdcbcd", ...KEYS3 }, mel: ["lead"], opts: { lo: 64, hi: 83, density: "normal" } },
        chorus: { parts: { ...ROCK_C, crash: CRASH4, bass: "RRRRRRRR", crunch: "R-R-R-R-", arp: "abcdcbcd", ...KEYS3 }, mel: ["gtr"], opts: { lo: 69, hi: 88, density: "normal" } },
        solo: { parts: { ...ROCK_C, crash: CRASH4, bass: "RRRRRRRR", crunch: "R-R-R-R-", ...KEYS3 }, mel: ["gtr"], opts: { lo: 69, hi: 91, density: "fast" } },
        outro: { parts: { ...ROCK_C, crash: CRASH4, bass: "RRRRRRRR", crunch: "R-R-R-R-", arp: "abcdcbcd", ...KEYS3 }, mel: ["gtr"], opts: { lo: 71, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  metal: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), snare: drum("snare", 0.27, "C3"), hat: drum("hihat", 0.11, "C6"), crash: drum("crash", 0.15, "C5"),
      gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.2, octave: 2, step: 0.25 },
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.25 },
      s1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
      s2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
      s3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.25 },
    },
    melodies: { lead: { instrument: "lead", waveform: "square", volume: 0.12 }, gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 } },
    plan: (kind) => {
      const dV = { kick: "x.xx..x.x.xx..x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
      const dC = { kick: "x.x.x.x.x.x.x.x.", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x.", crash: CRASH4 };
      const chug = "R.RR.RR.R.RR.RR.";
      const hit = "R-------R---R---";
      const bassE = "R.R.R.R.R.R.R.R.";
      const st = { s1: "a---------------", s2: "b---------------", s3: "c---------------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { ...dV, crash: CRASH4, gtrs: hit, bass: bassE }, mel: ["gtr"], opts: { lo: 69, hi: 88, density: "sparse" } },
        verse: { parts: { ...dV, gtrs: chug, bass: bassE }, mel: ["lead"], opts: { lo: 62, hi: 79, density: "normal" } },
        bridge: { parts: { ...dV, gtrs: chug, bass: bassE, ...st }, mel: ["lead"], opts: { lo: 64, hi: 84, density: "normal" } },
        chorus: { parts: { ...dC, gtrs: hit, bass: bassE, ...st }, mel: ["gtr"], opts: { lo: 69, hi: 90, density: "normal" } },
        solo: { parts: { ...dC, gtrs: chug, bass: bassE }, mel: ["gtr"], opts: { lo: 72, hi: 95, density: "fast" } },
        outro: { parts: { ...dC, gtrs: chug, bass: bassE }, mel: ["gtr"], opts: { lo: 69, hi: 88, density: "normal" } },
      };
      return rest[kind];
    },
  },
  classic: {
    sevenths: false,
    parts: {
      cello: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.5 },
      hpsi: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.12, octave: 4, step: 0.5 },
      v1: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      v2: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
      v3: { instrument: "strings", waveform: "sawtooth", volume: 0.07, octave: 4, step: 0.5 },
    },
    melodies: {
      violin: { instrument: "strings", waveform: "sawtooth", volume: 0.14 },
      piano: { instrument: "piano", waveform: "triangle", volume: 0.13 },
      hpsi2: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.14 },
    },
    plan: (kind, bpb) => {
      const three = bpb === 3;
      const hold = three ? "a-----" : "a-------";
      const cello1 = three ? "R-----" : "R-------";
      const cello2 = three ? "R--R--" : "R---R---";
      const arp = three ? "abcbcb" : "abcbabcb";
      const v = { v1: hold, v2: hold.replace("a", "b"), v3: hold.replace("a", "c") };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { cello: cello1, hpsi: arp }, mel: ["violin"], opts: { lo: 67, hi: 86, density: "sparse" } },
        verse: { parts: { cello: cello2, hpsi: arp, ...v }, mel: ["piano"], opts: { lo: 64, hi: 84, density: "normal" } },
        bridge: { parts: { cello: cello1, hpsi: arp, ...v }, mel: ["violin"], opts: { lo: 66, hi: 88, density: "normal" } },
        chorus: { parts: { cello: cello2, hpsi: arp, ...v }, mel: ["violin", "piano"], opts: { lo: 69, hi: 91, density: "normal" } },
        solo: { parts: { cello: cello2, hpsi: arp, ...v }, mel: ["hpsi2"], opts: { lo: 69, hi: 93, density: "fast" } },
        outro: { parts: { cello: cello2, hpsi: arp, ...v }, mel: ["violin", "piano"], opts: { lo: 67, hi: 88, density: "normal" } },
      };
      return rest[kind];
    },
  },
  space: {
    sevenths: true,
    parts: {
      p1: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 3, step: 0.5 },
      p2: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 3, step: 0.5 },
      p3: { instrument: "pad", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      p4: { instrument: "pad", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
      sub: { instrument: "pad", waveform: "sine", volume: 0.13, octave: 2, step: 0.5 },
      bells: { instrument: "bell", waveform: "sine", volume: 0.07, octave: 5, step: 0.5 },
    },
    melodies: { echo: { instrument: "echoGuitar", waveform: "sawtooth", volume: 0.14 }, lead: { instrument: "lead", waveform: "triangle", volume: 0.1 } },
    plan: (kind) => {
      const pads = { p1: "a-------", p2: "b-------", p3: "c-------", p4: "d-------", sub: "R-------" };
      const withBells = { ...pads, bells: "a..c..b." };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: pads, mel: [], opts: { lo: 64, hi: 80, density: "sparse" } },
        verse: { parts: withBells, mel: ["echo"], opts: { lo: 64, hi: 82, density: "sparse" } },
        bridge: { parts: withBells, mel: ["echo"], opts: { lo: 67, hi: 86, density: "sparse" } },
        chorus: { parts: withBells, mel: ["echo"], opts: { lo: 69, hi: 88, density: "sparse" } },
        solo: { parts: withBells, mel: ["lead"], opts: { lo: 67, hi: 88, density: "sparse" } },
        outro: { parts: withBells, mel: ["echo"], opts: { lo: 64, hi: 84, density: "sparse" } },
      };
      return rest[kind];
    },
  },
  cafe: {
    sevenths: true,
    parts: {
      kick: drum("kick", 0.24, "C2"), snare: drum("snare", 0.18, "C3"), hat: drum("hihat", 0.1, "C6"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 1 },
      k1: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      k2: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      k3: { instrument: "keys", waveform: "sine", volume: 0.09, octave: 4, step: 0.5 },
      k4: { instrument: "keys", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
      arp: { instrument: "guitar", waveform: "sawtooth", volume: 0.12, octave: 4, step: 0.5 },
      st1: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
      st2: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
      st3: { instrument: "strings", waveform: "sawtooth", volume: 0.06, octave: 4, step: 0.5 },
    },
    melodies: { keysm: { instrument: "keys", waveform: "sine", volume: 0.15 }, gtr: { instrument: "guitar", waveform: "sawtooth", volume: 0.17 }, lead: { instrument: "lead", waveform: "square", volume: 0.11 } },
    plan: (kind) => {
      const comp = { k1: "a--a--a-", k2: "b--b--b-", k3: "c--c--c-", k4: "d--d--d-" };
      const drums = { kick: "x.......x.x.....", snare: "....x.......x...", hat: "x.x.x.x.x.x.x.x." };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { bass: "abcb", ...comp, hat: "x.x.x.x.x.x.x.x." }, mel: ["keysm"], opts: { lo: 64, hi: 82, density: "normal" } },
        verse: { parts: { ...drums, bass: "abcb", ...comp }, mel: ["gtr"], opts: { lo: 62, hi: 80, density: "normal" } },
        bridge: { parts: { ...drums, bass: "abcb", ...comp, arp: "abcdcbcd" }, mel: ["lead"], opts: { lo: 65, hi: 84, density: "normal" } },
        chorus: { parts: { ...drums, bass: "abcb", ...comp, arp: "abcdcbcd", st1: "a-------", st2: "b-------", st3: "c-------" }, mel: ["keysm"], opts: { lo: 67, hi: 86, density: "normal" } },
        solo: { parts: { ...drums, bass: "abcb", ...comp, arp: "abcdcbcd" }, mel: ["gtr"], opts: { lo: 67, hi: 90, density: "fast" } },
        outro: { parts: { ...drums, bass: "abcb", ...comp }, mel: ["keysm"], opts: { lo: 64, hi: 82, density: "normal" } },
      };
      return rest[kind];
    },
  },
  epic: {
    sevenths: false,
    parts: {
      kick: drum("kick", 0.3, "C2"), snare: drum("snare", 0.24, "C3"), crash: drum("crash", 0.16, "C5"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.28, octave: 2, step: 0.5 },
      gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.5 },
      s1: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
      s2: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
      s3: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
      pad: { instrument: "pad", waveform: "sine", volume: 0.1, octave: 3, step: 0.5 },
    },
    melodies: { lead: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.15 }, vln: { instrument: "strings", waveform: "sawtooth", volume: 0.15 } },
    plan: (kind) => {
      const ost = { s1: "abcbabcb", s2: "bcbabcba", s3: "cbabcbab" };
      const timp = { kick: "x...............", snare: "................" };
      const beat = { kick: "x.....x.x.x...x.", snare: "....x.......x..." };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { pad: "a-------", bass: "R-------", ...timp }, mel: ["vln"], opts: { lo: 67, hi: 86, density: "sparse" } },
        verse: { parts: { ...ost, bass: "R.R.R.R.", ...timp }, mel: ["vln"], opts: { lo: 64, hi: 83, density: "normal" } },
        bridge: { parts: { ...ost, bass: "R.RR.R.R", ...beat, pad: "a-------" }, mel: ["vln"], opts: { lo: 66, hi: 86, density: "normal" } },
        chorus: { parts: { ...ost, bass: "RRRRRRRR", gtrs: "R-R-R-R-", ...beat, crash: CRASH4, pad: "a-------" }, mel: ["lead", "vln"], opts: { lo: 69, hi: 91, density: "normal" } },
        solo: { parts: { ...ost, bass: "RRRRRRRR", gtrs: "R-R-R-R-", ...beat }, mel: ["lead"], opts: { lo: 72, hi: 95, density: "fast" } },
        outro: { parts: { ...ost, bass: "RRRRRRRR", gtrs: "R-R-R-R-", ...beat, crash: CRASH4 }, mel: ["lead", "vln"], opts: { lo: 69, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  folk: {
    sevenths: false,
    parts: {
      arp: { instrument: "guitar", waveform: "sawtooth", volume: 0.15, octave: 3, step: 0.5 },
      bass: { instrument: "bass", waveform: "triangle", volume: 0.22, octave: 2, step: 1 },
      hat: drum("hihat", 0.06, "C6"),
      kick: drum("kick", 0.16, "C2"),
      k1: { instrument: "piano", waveform: "triangle", volume: 0.08, octave: 4, step: 0.5 },
      k2: { instrument: "piano", waveform: "triangle", volume: 0.08, octave: 4, step: 0.5 },
      k3: { instrument: "piano", waveform: "triangle", volume: 0.08, octave: 4, step: 0.5 },
    },
    melodies: { flute: { instrument: "lead", waveform: "triangle", volume: 0.14 }, bell: { instrument: "bell", waveform: "sine", volume: 0.1 } },
    plan: (kind) => {
      const arp = "abcbabcb";
      const lite = { kick: "x.......x.......", hat: "x...x...x...x..." };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { arp, bass: "R..R" }, mel: ["flute"], opts: { lo: 67, hi: 84, density: "normal" } },
        verse: { parts: { arp, bass: "R.5.", ...lite }, mel: ["flute"], opts: { lo: 64, hi: 81, density: "normal" } },
        bridge: { parts: { arp, bass: "R.5.", ...lite, k1: "a-------", k2: "b-------", k3: "c-------" }, mel: ["bell"], opts: { lo: 69, hi: 88, density: "sparse" } },
        chorus: { parts: { arp, bass: "R.5R", ...lite, k1: "a-------", k2: "b-------", k3: "c-------" }, mel: ["flute"], opts: { lo: 67, hi: 86, density: "normal" } },
        solo: { parts: { arp, bass: "R.5R", ...lite }, mel: ["flute"], opts: { lo: 67, hi: 88, density: "fast" } },
        outro: { parts: { arp, bass: "R..R" }, mel: ["flute"], opts: { lo: 64, hi: 82, density: "normal" } },
      };
      return rest[kind];
    },
  },
};

// ── 不協和音・不思議（特別な作り） ──
function discordScore(spec: SongSpec, rng: Rng, key: Key, kinds: Kind[]): Score {
  const beats = spec.beats ?? 4;
  const t = key.tonic;
  const lowName = (semi: number, oct: number): string => `${NAMES[(t + semi) % 12]}${oct}`;
  const sections: Section[] = kinds.map((kind, idx) => {
    const bars = kind === "intro" ? 4 : 8;
    const total = bars * beats;
    const chords = Array(bars).fill(`${NAMES[t]}dim`).join(" ");
    // 低い持続音: 主音と、半音上の音がぶつかってうなる
    const drone = (semi: number, oct: number): string => {
      const notes: string[] = [];
      let left = total;
      while (left > 0) {
        const len = Math.min(left, pick(rng, [8, 12, 16]));
        notes.push(`${lowName(semi, oct)}:${len}`);
        left -= len;
      }
      return notes.join(" ");
    };
    const bells: string[] = [];
    let cursor = 0;
    while (cursor < total) {
      const gap = Math.min(total - cursor, pick(rng, [2, 3, 4, 5.5, 7]));
      bells.push(`R:${gap}`);
      cursor += gap;
      if (cursor < total) {
        bells.push(`${lowName(pick(rng, [6, 6, 1, 11, 8]), pick(rng, [5, 6]))}:0.5`);
        cursor += 0.5;
      }
    }
    // 半音ずつはい回る弦
    const worm: string[] = [];
    let w = 0;
    cursor = 0;
    let semi = pick(rng, [0, 1, 6]);
    while (cursor < total) {
      const len = Math.min(total - cursor, pick(rng, [2, 3, 4]));
      if (idx === 0 && cursor < 8) {
        worm.push(`R:${len}`);
      } else if (rng() < 0.2) {
        worm.push(`R:${len}`);
      } else {
        semi = Math.max(0, Math.min(14, semi + pick(rng, [-1, 1, 1, -2, 6, -1])));
        worm.push(`${lowName(semi, 4)}:${len}`);
      }
      cursor += len;
      w++;
    }
    return {
      chords,
      parts: { heart: (kind === "chorus" ? "x.x.x.x.x.x.x.x." : "x.x.............") + "" },
      melody: { c1: drone(0, 3), c2: drone(1, 3), b1: bells.join(" "), w1: worm.join(" ") },
    };
  });
  const a: Arrangement = {
    tempoBpm: spec.bpm,
    beatsPerBar: beats,
    sections,
    parts: { heart: { instrument: "kick", waveform: "sine", volume: 0.22, octave: 2, step: 0.25, fixed: "C2" } },
    melodies: {
      c1: { instrument: "pad", waveform: "sine", volume: 0.12 },
      c2: { instrument: "pad", waveform: "sine", volume: 0.12 },
      b1: { instrument: "bell", waveform: "sine", volume: 0.1 },
      w1: { instrument: "strings", waveform: "sawtooth", volume: 0.09 },
    },
  };
  return arrange(a);
}

function mysteryScore(spec: SongSpec, rng: Rng, key: Key, kinds: Kind[]): Score {
  const beats = spec.beats ?? 4;
  const cache = new Map<Kind, { chords: string; melody: string }>();
  const sections: Section[] = kinds.map((kind) => {
    const bars = kind === "intro" ? 4 : 8;
    let entry = cache.get(kind);
    if (!entry) {
      const cells = key.minor ? CELLS_MINOR : CELLS_MAJOR;
      const cell = pick(rng, cells);
      const degrees = [...cell, ...cell].slice(0, bars);
      // ときどき導音の減七和音（ぐらつく響き）にする
      const chords = degrees.map((d, i) => (i % 4 === 3 || d === 5 ? chordName(key, d, false, { leadingDim: true }) : chordName(key, d, false))).map((c, i) => (i % 4 === 3 ? `${NAMES[(key.tonic + 11) % 12]}dim` : c));
      const melody = generateMelody(rng, key, chords, beats, { lo: 72, hi: 93, density: kind === "chorus" ? "normal" : "sparse", restChance: 0.15 });
      entry = { chords: chords.join(" "), melody };
      cache.set(kind, entry);
    }
    const dimBar = "R.......R.5.....";
    return {
      chords: entry.chords,
      parts: {
        tick: "x.x.x.x.x.x.x.x.",
        mb: "abcdcbab",
        pz: kind === "intro" ? dimBar : "R.R.5.R.R.R.5.R.",
        bass: "R---------------",
        ...(kind === "intro" ? {} : { pad: "a---------------" }),
      },
      melody: (kind === "intro" ? {} : { harp: entry.melody }) as Record<string, string>,
    };
  });
  return arrange({
    tempoBpm: spec.bpm,
    beatsPerBar: beats,
    sections,
    parts: {
      tick: { instrument: "hihat", waveform: "sine", volume: 0.09, octave: 2, step: 0.25, fixed: "C6" },
      mb: { instrument: "bell", waveform: "sine", volume: 0.07, octave: 5, step: 0.5 },
      pz: { instrument: "harpsichord", waveform: "sawtooth", volume: 0.1, octave: 3, step: 0.25 },
      bass: { instrument: "pad", waveform: "sine", volume: 0.1, octave: 2, step: 0.25 },
      pad: { instrument: "strings", waveform: "sawtooth", volume: 0.05, octave: 4, step: 0.25 },
    },
    melodies: { harp: { instrument: "bell", waveform: "sine", volume: 0.1 } },
  });
}

/** 曲調ごとのドラムセット（GMのドラムキット番号）。 */
const DRUM_KIT: Partial<Record<Style, number>> = {
  rock: 16, metal: 16, hardcore: 16, deathmetal: 16, progmetal: 16, epic: 48, jazz: 32, electro: 24, phonk: 25, rnb: 8, cafe: 8, samba: 8, jpop: 8, folk: 8,
};

// フィル（8小節のまとまりの最後の小節で、タムを回して次へつなぐ）
const FILL = { kick: "x.......x.......", snare: "....x.x.x.......", hat: "x.x.x.x.x.......", tomH: "..........x.x...", tomM: "..............x.", tomL: "...............x" };
const GHOST_STEPS = [2, 10, 15];

/** 8小節の区間の最後の小節をフィルにし、スネアにゴーストノート（弱い一打）を足す。 */
function applyDrumRealism(kp: KindPlan, kind: Kind, bars: number, style: Style, tpl: Template): KindPlan {
  const p = kp.parts;
  const snare = tpl.parts.snare;
  if (kind === "intro" || bars < 8 || !snare || snare.step !== 0.25 || !p.snare || p.snare.includes(" ")) return kp;
  const parts: Record<string, string> = { ...p };
  const withFill = (normal: string, fill: string): string => [...Array(bars - 1).fill(normal), fill].join(" ");
  if (["rock", "jpop", "cafe", "rnb", "samba", "folk"].includes(style) && (kind === "verse" || kind === "bridge")) {
    parts.snare = [...p.snare].map((ch, i) => (ch === "." && GHOST_STEPS.includes(i) ? "o" : ch)).join("");
  }
  parts.snare = withFill(parts.snare, FILL.snare);
  if (p.kick && p.kick.length === 16 && !p.kick.includes(" ")) parts.kick = withFill(p.kick, FILL.kick);
  if (p.hat && p.hat.length === 16 && !p.hat.includes(" ")) parts.hat = withFill(p.hat, FILL.hat);
  parts.tomH = withFill("................", FILL.tomH);
  parts.tomM = withFill("................", FILL.tomM);
  parts.tomL = withFill("................", FILL.tomL);
  return { ...kp, parts };
}

const TOM_PARTS: Record<string, PartSpec> = {
  tomH: { instrument: "tom", waveform: "sine", volume: 0.24, octave: 2, step: 0.25, fixed: "D3" },
  tomM: { instrument: "tom", waveform: "sine", volume: 0.24, octave: 2, step: 0.25, fixed: "B2" },
  tomL: { instrument: "tom", waveform: "sine", volume: 0.26, octave: 2, step: 0.25, fixed: "G2" },
};

/**
 * 疾走感（ボス戦向け）: 16分音符の低音の刻み、16分のアルペジオ、8分のキック、16分のハイハットを足す。
 * 静かな導入（intro）にはかけない。
 */
function applyDrive(kp: KindPlan, kind: Kind, tpl: Template, on: boolean): KindPlan {
  if (!on || kind === "intro") return kp;
  const parts: Record<string, string> = { ...kp.parts };
  delete parts.bass;
  parts.drvbass = kind === "bridge" ? "R.R.R.R.R.R.R.R." : "R.RRR.RRR.RRR.RR";
  parts.drv = kind === "chorus" || kind === "solo" || kind === "outro" ? "abcdabcdabcdabcd" : "a.b.c.b.a.b.c.b.";
  if ("kick" in tpl.parts && tpl.parts.kick.step === 0.25) parts.kick = "x.x.x.x.x.x.x.x.";
  if ("hat" in tpl.parts && tpl.parts.hat.step === 0.25) parts.hat = kind === "bridge" ? "x.x.x.x.x.x.x.x." : "xoxoxoxoxoxoxoxo";
  return { ...kp, parts };
}

/** 設計図から曲を作る。 */
export function composeSong(spec: SongSpec): Score {
  const rng = makeRng(spec.seed);
  const key = keyOf(spec);
  const beats = spec.beats ?? 4;
  const plan = planSections(spec.bpm, beats, spec.targetSec ?? 75);
  if (spec.style === "discord") return discordScore(spec, rng, key, plan.kinds);
  if (spec.style === "mystery") return mysteryScore(spec, rng, key, plan.kinds);
  const tpl = TEMPLATES[spec.style];
  const cells = key.minor ? CELLS_MINOR : CELLS_MAJOR;
  const cache = new Map<Kind, { chords: string[]; melody: string }>();
  const verseCell = pick(rng, cells);
  const bridgeCells = [pick(rng, cells), pick(rng, cells)];
  const chorusCells = [pick(rng, cells), pick(rng, cells)];
  const chordsFor = (kind: Kind): string[] => {
    const deg = (cell: number[]): string[] => cell.map((d) => chordName(key, d, tpl.sevenths));
    if (spec.style === "baroque") {
      // 5度ずつ下がる進行（I IV vii° iii vi ii V I）を軸にする
      const fifths = [1, 4, 7, 3, 6, 2, 5, 1];
      const other = [6, 2, 5, 1, 4, 5, 1, 1];
      const cad = [1, 6, 2, 5, 1, 4, 5, 1];
      const table: Record<Kind, number[]> = { intro: fifths.slice(0, 4), verse: fifths, bridge: other, chorus: cad, solo: fifths, outro: cad };
      return deg(table[kind]);
    }
    const variation = (cell: number[]): number[] => [...cell.slice(0, 3), pick(rng, [5, 4, cell[3]])];
    let degrees: number[];
    if (kind === "verse") degrees = [...verseCell, ...variation(verseCell)];
    else if (kind === "bridge") degrees = [...bridgeCells[0], ...bridgeCells[1]];
    else if (kind === "intro") degrees = verseCell;
    else degrees = [...chorusCells[0], ...chorusCells[1]];
    if (kind === "outro" || kind === "chorus") degrees = [...degrees.slice(0, degrees.length - 1), 1];
    return deg(degrees);
  };
  const driveParts: Record<string, PartSpec> = spec.drive && beats === 4
    ? {
        drvbass: { instrument: "bass", waveform: "sawtooth", volume: 0.24, octave: 2, step: 0.25 },
        drv: { instrument: "lead", waveform: "square", volume: 0.06, octave: 4, step: 0.25 },
      }
    : {};
  const sections: Section[] = plan.kinds.map((kind) => {
    const barsInSection = kind === "intro" ? 4 : 8;
    const base = applyDrive(tpl.plan(kind, beats), kind, tpl, spec.drive === true && beats === 4);
    const kp = beats === 4 && spec.style !== "jazz" ? applyDrumRealism(base, kind, barsInSection, spec.style, tpl) : base;
    let entry = cache.get(kind);
    if (!entry) {
      const chords = chordsFor(kind);
      entry = { chords, melody: kp.mel.length ? generateMelody(rng, key, chords, beats, kp.opts) : "" };
      cache.set(kind, entry);
    }
    const melody: Record<string, string> = {};
    for (const m of kp.mel) melody[m] = entry.melody;
    return { chords: entry.chords.join(" "), parts: kp.parts, melody };
  });
  const hasFills = beats === 4 && spec.style !== "jazz" && tpl.parts.snare?.step === 0.25;
  const score = arrange({ tempoBpm: spec.bpm, beatsPerBar: beats, sections, parts: { ...tpl.parts, ...driveParts, ...(hasFills ? TOM_PARTS : {}) }, melodies: tpl.melodies });
  score.drumKit = DRUM_KIT[spec.style] ?? 0;
  return score;
}
