import { arrange, midiToName, type Arrangement, type MelodySpec, type PartSpec, type Section } from "./compose";
import { noteNameToMidi } from "./note";
import { REST, type NoteEvent, type Score } from "./score";

/**
 * 曲の設計図（調・速さ・曲調・乱数の種）から、1〜1分半のオリジナル曲を組み立てる「作曲エンジン」。
 * コード進行は定番の型の組み合わせ、旋律は「コードの音を軸に音階を歩く」規則で作る。同じ設計図からは毎回同じ曲ができる。
 * 特定の既存曲の旋律・進行をなぞらない（`CLAUDE.md` 1-1）。曲の良し悪しは耳で聴いて設計図（種など）を調整する。
 */

export type Style =
  | "rock" | "metal" | "classic" | "space" | "cafe" | "discord" | "mystery" | "epic" | "folk"
  | "baroque" | "nature" | "phonk" | "samba" | "jazz" | "rnb" | "electro" | "hardcore" | "deathmetal" | "progmetal" | "jpop"
  | "dancerock" | "cleandance";

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
  /** 曲の長さの目安（秒。既定75）。90秒を超えると「長尺モード」（イントロ→A→サビ→間奏→ラストサビ→アウトロ）で組む。 */
  targetSec?: number;
  /** 曲調に重ねる味つけ（ラウド＝ギターを左右に倍にして専用アンプ／オーケストラ＝弦・ブラス・合唱・ティンパニ／和楽器＝琴・三味線・尺八・太鼓）。 */
  flavor?: Flavor | Flavor[];
  /** trueなら、歌（ボーカル）のメロディも作る（composeSong の第2引数 extra.vocal に入る）。楽器の曲は変わらない。 */
  vocal?: boolean;
}

/** 歌のメロディ（Aメロ・Bメロ・サビだけ）。声に合わせて、女声の歌いやすい高さ（D4〜G5）にする。 */
export interface VocalSection {
  kind: "verse" | "bridge" | "chorus";
  /** 曲の頭から、この区間の頭までの拍。 */
  startBeat: number;
  /** "C4:1 R:0.5 …"（音名:拍）の並び。 */
  melody: string;
}

const VOCAL_RANGE = { verse: { lo: 60, hi: 74 }, bridge: { lo: 62, hi: 77 }, chorus: { lo: 65, hi: 79 } } as const;

/** 曲調（Style）に重ねる味つけ。 */
export type Flavor = "loud" | "orchestra" | "wagakki";

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
  if (targetSec > 90) return { kinds: longKinds(bpm, beats, targetSec) };
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

/**
 * 長尺モード（targetSec > 90）の構成。イントロ（4小節）のあとに、8小節ずつの区間を k 個並べる（最後はアウトロ）。
 * 流れ: A, A, B, サビ → A, B, サビ（くり返し）→ 間奏（ソロ）→ サビ, サビ（ラストは2回続けて盛り上げる）→ アウトロ。
 * k は目標の長さに最も近くなるように決める（最短6区間）。
 */
function longKinds(bpm: number, beats: number, targetSec: number): Kind[] {
  const barsWanted = (targetSec * bpm) / 60 / beats;
  const k = Math.max(6, Math.round((barsWanted - 4) / 8));
  const n = k - 1; // アウトロの前までの区間数
  const first: Kind[] = ["verse", "verse", "bridge", "chorus"];
  const cycle: Kind[] = ["verse", "bridge", "chorus"];
  const body: Kind[] = Array.from({ length: n }, (_, i) => (i < first.length ? first[i] : cycle[(i - first.length) % cycle.length]));
  if (n >= 7) body[Math.round(n * 0.62)] = "solo";
  if (n >= 8) {
    body[n - 1] = "chorus";
    body[n - 2] = "chorus";
    // サビが3回続かないようにする。直前がBなら、Aを挟む（B・Bと同じ区間が並ばないようにする）
    if (body[n - 3] === "chorus") body[n - 3] = body[n - 4] === "bridge" ? "verse" : "bridge";
  }
  return ["intro", ...body, "outro"];
}

/** 曲の構成（区間の並び）。テストや外部ツールが、長さと構成を確かめるために使う。 */
export function planKinds(bpm: number, beats: number, targetSec: number): string[] {
  return planSections(bpm, beats, targetSec).kinds;
}

// ── 旋律 ──
const RHYTHM4 = [[2, 2], [1, 1, 2], [1, 1, 1, 1], [1.5, 0.5, 1, 1], [2, 1, 1], [1, 2, 1], [0.5, 0.5, 1, 2], [1, 1, 0.5, 0.5, 1], [3, 1], [1, 0.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 2], [1.5, 1.5, 1]];
const RHYTHM3 = [[3], [2, 1], [1, 2], [1, 1, 1], [1.5, 0.5, 1], [1, 0.5, 0.5, 1], [2, 0.5, 0.5]];
const RHYTHM7 = [[2, 2, 3], [1.5, 1.5, 2, 2], [3, 2, 2], [1, 1, 1, 1, 3], [2, 1, 1, 3]];
const RHYTHM35 = [[1.5, 1, 1], [1, 1, 1, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [2, 1.5], [0.5, 0.5, 1, 1, 0.5]];
const RHYTHM45 = [[1.5, 1.5, 1.5], [1, 1, 1, 1, 0.5], [2, 2, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [1, 0.5, 1, 0.5, 1.5]];
const RHYTHM5 = [[2, 3], [1.5, 1.5, 2], [1, 1, 1, 1, 1], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [2, 1, 2]];
const RHYTHM_SPARSE4 = [[4], [3, 1], [2, 2], [1, 3], [2, 1, 1]];
const RHYTHM_FAST4 = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 1, 1], [0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25]];

export interface MelodyOpts {
  /** 曲の頭の1小節を、コードの音を駆け上がる速い音型（アルペジオ）にする（クラシックの勢いのある出だし）。 */
  opening?: "run";
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
  const tables = beats === 7 ? [RHYTHM7] : beats === 3.5 ? [RHYTHM35] : beats === 4.5 ? [RHYTHM45] : beats === 5 ? [RHYTHM5] : beats === 3 ? [RHYTHM3] : opts.density === "sparse" ? [RHYTHM_SPARSE4] : opts.density === "fast" && beats === 4 ? [RHYTHM_FAST4] : [beats === 3 ? RHYTHM3 : RHYTHM4];
  const rhythmFor = (): number[] => pick(rng, tables[0]);
  const out: string[] = [];
  const rhythms: number[][] = [];
  const skip = new Set<number>();
  const barTokens: string[][] = [];
  chords.forEach((chord, bar) => {
    if (skip.has(bar)) {
      return;
    }
    const startLen = out.length;
    // 耳に残るフレーズ: 2小節前と同じ拍の並びなら、音もそのまま繰り返すことがある（フック）
    if (bar % 4 >= 2 && bar < chords.length - 1 && barTokens[bar - 2] && beats !== 7 && rng() < 0.5 && rhythms[bar - 2]?.reduce((a, b) => a + b, 0) === beats) {
      out.push(...barTokens[bar - 2]);
      rhythms.push(rhythms[bar - 2]);
      barTokens[bar] = barTokens[bar - 2];
      return;
    }
    const tones = chordPitchClasses(chord);
    if (opts.opening === "run" && bar === 0 && (beats === 4 || beats === 3)) {
      // 勢いのある出だし: 和音の音を、下から一気に駆け上がる（16分音符）
      const ascending = pool.filter((m) => tones.includes(m % 12)).slice(0, Math.max(6, beats * 4));
      const notes = Array.from({ length: beats * 4 }, (_, i) => ascending[Math.min(ascending.length - 1, Math.floor((i * ascending.length) / (beats * 4)))]);
      notes.forEach((m) => out.push(`${midiToName(m)}:0.25`));
      cur = pool.indexOf(notes[notes.length - 1]);
      rhythms.push([0.25]);
      return;
    }
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
      rhythm = beats === 3 ? [1, 2] : beats !== 4 ? [1, 1, beats - 2] : opts.density === "fast" ? rhythmFor() : [1, 1, 2];
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
    barTokens[bar] = out.slice(startLen);
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
  /** パートごとの左右の位置（書いたパートだけ、自動の振り分けを上書きする）。 */
  pans?: Record<string, number>;
  /** ベースをメロディのように動かす（小節の最後の音を、次の小節の最初の音へ向かう経過音にする）パート。 */
  walkingBass?: string;
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
  dancerock: {
    // ダンス×ロック: 4つ打ちのキックと裏拍のハイハット・16分のシンセのアルペジオ（ダンス）に、
    // 左右に分けた歪んだギター・リードギター・バックビートのスネア（ロック）、弦・合唱・ブラス（壮大さ）を重ねる。
    // 「間奏（solo）」はドラムを抜いてピアノだけにし、曲の途中で一度引く（docs/sound/reference-nihonichi-bgm.md 4-5）
    sevenths: false,
    parts: {
      kick: drum("kick", 0.28, "C2"), snare: drum("snare", 0.2, "C3"), hat: drum("hihat", 0.09, "C6"), crash: drum("crash", 0.11, "C5"),
      bass: { instrument: "bass", waveform: "sawtooth", volume: 0.2, octave: 2, step: 0.5 },
      gtrL: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.018, octave: 3, step: 0.5 },
      gtrR: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.018, octave: 3, step: 0.5 },
      arp: { instrument: "lead", waveform: "square", volume: 0.028, octave: 4, step: 0.25 },
      str: { instrument: "strings", waveform: "sawtooth", volume: 0.1, octave: 4, step: 0.5 },
      choir: { instrument: "choir", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
      brass: { instrument: "brass", waveform: "sawtooth", volume: 0.1, octave: 3, step: 0.5 },
    },
    melodies: {
      syn: { instrument: "lead", waveform: "sawtooth", volume: 0.1 },
      gtr: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.11 },
      strm: { instrument: "strings", waveform: "sawtooth", volume: 0.08 },
      pno: { instrument: "piano", waveform: "triangle", volume: 0.16 },
    },
    pans: { hat: 0.3, crash: -0.3, gtrL: -0.9, gtrR: 0.9, arp: 0.55, str: -0.6, choir: 0.35, brass: -0.4, syn: 0.05, gtr: 0.1, strm: -0.2, pno: 0.15 },
    walkingBass: "bass",
    plan: (kind) => {
      const four = { kick: "x...x...x...x...", hat: "..x...x...x...x." };
      const back = "....x.......x...";
      const arp = "abcOabcOabcOabcO";
      const bed = { str: "b-------", choir: "a-------" };
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { arp, ...bed, hat: four.hat }, mel: [], opts: { lo: 67, hi: 86, density: "sparse" } },
        verse: { parts: { ...four, snare: back, bass: "R-5OB-R-", gtrL: "RRRRRRRR", gtrR: "55555555", arp, str: bed.str }, mel: ["syn"], opts: { lo: 64, hi: 83, density: "normal" } },
        bridge: { parts: { kick: four.kick, hat: "x.x.x.x.x.x.x.x.", snare: back, bass: "R-R-5-O-", gtrL: "R-------", gtrR: "5-------", arp, ...bed }, mel: ["syn"], opts: { lo: 67, hi: 87, density: "normal" } },
        chorus: { parts: { ...four, hat: "xoxoxoxoxoxoxoxo", snare: back, crash: CRASH4, bass: "ROROBO5-", gtrL: "R-.RR-R.", gtrR: "5-.55-5.", arp, ...bed, brass: "R...R.R." }, mel: ["gtr", "strm"], opts: { lo: 69, hi: 90, density: "normal" } },
        solo: { parts: { bass: "R-------", ...bed }, mel: ["pno"], opts: { lo: 64, hi: 84, density: "sparse" } },
        outro: { parts: { ...four, hat: "xoxoxoxoxoxoxoxo", snare: back, crash: CRASH4, bass: "ROROBO5-", gtrL: "R-.RR-R.", gtrR: "5-.55-5.", arp, ...bed, brass: "R...R.R." }, mel: ["gtr", "strm"], opts: { lo: 69, hi: 90, density: "normal" } },
      };
      return rest[kind];
    },
  },
  cleandance: {
    // きれいで現代的なダンス: やわらかい4つ打ちに、ピアノの分散和音・付点8分のエコーギター・弦・パッド・合唱を
    // 左右に広げて重ねる。歪んだギターとシンセのリードは使わない。旋律はピアノ（Aメロ）と弦＋鐘（サビ）。
    // ベースはメロディのように動く。「間奏（solo）」はドラムを抜いて一度引く（docs/sound/reference-nihonichi-bgm.md）
    sevenths: false,
    parts: {
      kick: drum("kick", 0.2, "C2"), snare: drum("snare", 0.14, "C3"), hat: drum("hihat", 0.075, "C6"), crash: drum("crash", 0.09, "C5"),
      bass: { instrument: "bass", waveform: "triangle", volume: 0.17, octave: 2, step: 0.5 },
      parp: { instrument: "piano", waveform: "triangle", volume: 0.09, octave: 4, step: 0.25 },
      egtr: { instrument: "echoGuitar", waveform: "triangle", volume: 0.08, octave: 4, step: 0.25 },
      strl: { instrument: "strings", waveform: "sawtooth", volume: 0.1, octave: 3, step: 0.5 },
      pad: { instrument: "pad", waveform: "sine", volume: 0.07, octave: 4, step: 0.5 },
      choir: { instrument: "choir", waveform: "sine", volume: 0.08, octave: 4, step: 0.5 },
    },
    melodies: {
      pmel: { instrument: "piano", waveform: "triangle", volume: 0.17 },
      smel: { instrument: "strings", waveform: "sawtooth", volume: 0.15 },
      bell: { instrument: "bell", waveform: "sine", volume: 0.05 },
    },
    pans: { hat: 0.3, crash: -0.3, parp: -0.6, egtr: 0.75, strl: -0.75, pad: 0.8, choir: -0.3, pmel: 0.05, smel: 0.15, bell: 0.5 },
    walkingBass: "bass",
    plan: (kind) => {
      const four = { kick: "x...x...x...x...", hat: "..x...x...x...x." };
      const back = "....x.......x...";
      const parp = "abcAcbcAabcAcbcA";
      const egtr = "c..b..a.c..b..a.";
      const rest: Record<Kind, KindPlan> = {
        intro: { parts: { parp, pad: "c-------", choir: "a-------" }, mel: [], opts: { lo: 67, hi: 86, density: "sparse" } },
        verse: { parts: { ...four, bass: "R-5OB-R-", parp, egtr, strl: "b-------" }, mel: ["pmel"], opts: { lo: 64, hi: 83, density: "normal" } },
        bridge: { parts: { ...four, hat: "x.x.x.x.x.x.x.x.", snare: back, bass: "R-R-5-O-", parp, egtr, strl: "b-------", pad: "c-------" }, mel: ["pmel"], opts: { lo: 67, hi: 87, density: "normal" } },
        chorus: { parts: { ...four, hat: "xoxoxoxoxoxoxoxo", snare: back, crash: CRASH4, bass: "R-.5OB5-", parp, egtr, strl: "b-------", pad: "c-------", choir: "a-------" }, mel: ["smel", "bell"], opts: { lo: 69, hi: 88, density: "normal" } },
        solo: { parts: { bass: "R-------", pad: "c-------", choir: "a-------" }, mel: ["pmel"], opts: { lo: 64, hi: 84, density: "sparse" } },
        outro: { parts: { ...four, hat: "xoxoxoxoxoxoxoxo", snare: back, crash: CRASH4, bass: "R-.5OB5-", parp, egtr, strl: "b-------", pad: "c-------", choir: "a-------" }, mel: ["smel", "bell"], opts: { lo: 69, hi: 88, density: "normal" } },
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
  dancerock: 16, cleandance: 8,
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

/** 曲の頭に一撃を入れる曲調（クラシックの勢いのある出だしのように、聴き手をつかむ）。 */
const METAL_STYLES: Style[] = ["metal", "hardcore", "deathmetal", "progmetal"];
const OPENING_STYLES: Style[] = ["rock", "metal", "hardcore", "deathmetal", "progmetal", "epic", "electro", "jpop", "baroque", "classic"];
const RUN_STYLES: Style[] = ["baroque", "classic", "epic"];
/** 一撃の和音（ブラス・弦・低い根音）。曲の最初の小節だけ、全員で長く鳴らす。 */
const STRIKE_PARTS: Record<string, PartSpec> = {
  opn1: { instrument: "brass", waveform: "sawtooth", volume: 0.24, octave: 3, step: 0.5 },
  opn2: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 3, step: 0.5 },
  opn3: { instrument: "brass", waveform: "sawtooth", volume: 0.2, octave: 4, step: 0.5 },
};

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

/**
 * ベースをメロディのように動かす: 各小節の最後の音（1拍以内）を、次の小節の最初の音へ1音ずつ近づく経過音にする。
 * 経過音は調の音階から選び、その小節の和音の音と半音でぶつかる音は避ける（例: 短調の属和音の3度の半音下）。
 * あわせて、ベースの音域（E1〜G3）に収める。
 */
export function walkBass(notes: NoteEvent[], barChords: string[], beats: number, key: Key): NoteEvent[] {
  const LOW = 28, HIGH = 55;
  const fold = (m: number): number => {
    let x = m;
    while (x > HIGH) x -= 12;
    while (x < LOW) x += 12;
    return x;
  };
  const out = notes.map((n) => (n.note === REST ? { ...n } : { ...n, note: midiToName(fold(noteNameToMidi(n.note))) }));
  const starts: number[] = [];
  let t = 0;
  for (const n of out) {
    starts.push(t);
    t += n.durationBeats;
  }
  const scalePcs = key.scale.map((s) => (key.tonic + s) % 12);
  for (let bar = 0; bar < barChords.length; bar++) {
    const end = (bar + 1) * beats;
    const lastIdx = out.findIndex((n, i) => Math.abs(starts[i] + n.durationBeats - end) < 1e-9 && starts[i] >= bar * beats - 1e-9);
    const nextIdx = out.findIndex((_, i) => Math.abs(starts[i] - end) < 1e-9);
    if (lastIdx <= 0 || nextIdx < 0) continue;
    const last = out[lastIdx], prev = out[lastIdx - 1], next = out[nextIdx];
    if (last.note === REST || prev.note === REST || next.note === REST || last.durationBeats > 1 + 1e-9 || starts[lastIdx - 1] < bar * beats - 1e-9) continue;
    const chord = chordPitchClasses(barChords[bar]);
    const clash = (pc: number): boolean => !chord.includes(pc) && chord.some((c) => (pc - c + 12) % 12 === 1 || (c - pc + 12) % 12 === 1);
    const allowed = scalePcs.filter((pc) => !clash(pc)).concat(chord);
    const target = noteNameToMidi(next.note);
    const from = noteNameToMidi(prev.note);
    const dir = from < target ? -1 : 1;
    // 前の音の側から近づく音を探し、見つからなければ反対側から（例: 導音で主音へ）
    const found = [dir, -dir].flatMap((dd) => [1, 2, 3].map((d) => target + dd * d))
      .find((m) => allowed.includes(((m % 12) + 12) % 12) && m >= LOW && m <= HIGH && m !== from);
    if (found !== undefined) out[lastIdx] = { ...last, note: midiToName(found) };
  }
  return out;
}

// ── 味つけ（flavor）: 曲調に重ねる ──
// 4拍子（1小節＝16マス）のパターン。a・b・c＝コードの1・2・3番目の音、R＝根音、5＝5度、x＝打つ、-＝のばす、.＝休み。
const L1 = (c: string): string => c + "---------------";
const FLAVOR_PARTS: Record<"orchestra" | "wagakki", Record<string, PartSpec>> = {
  orchestra: {
    os1: { instrument: "strings", waveform: "sawtooth", volume: 0.1, octave: 3, step: 0.25 },
    os2: { instrument: "strings", waveform: "sawtooth", volume: 0.1, octave: 4, step: 0.25 },
    os3: { instrument: "strings", waveform: "sawtooth", volume: 0.09, octave: 4, step: 0.25 },
    obr: { instrument: "brass", waveform: "sawtooth", volume: 0.11, octave: 3, step: 0.25 },
    och: { instrument: "choir", waveform: "sine", volume: 0.1, octave: 4, step: 0.25 },
    otp: { instrument: "tom", waveform: "sine", volume: 0.2, octave: 2, step: 0.25, fixed: "D2" },
  },
  wagakki: {
    wko: { instrument: "koto", waveform: "triangle", volume: 0.16, octave: 4, step: 0.25 },
    wsh: { instrument: "shamisen", waveform: "sawtooth", volume: 0.14, octave: 3, step: 0.25 },
    wsk: { instrument: "shakuhachi", waveform: "sine", volume: 0.13, octave: 4, step: 0.25 },
    wtk: { instrument: "tom", waveform: "sine", volume: 0.22, octave: 2, step: 0.25, fixed: "A1" },
  },
};
const FLAVOR_PLANS: Record<"orchestra" | "wagakki", (kind: Kind) => Record<string, string>> = {
  orchestra: (kind) => {
    const timpHit = "x...............";
    const timpDrive = "x.......x.x.x...";
    const table: Record<Kind, Record<string, string>> = {
      intro: { os1: L1("R"), os2: L1("a"), otp: timpHit },
      verse: { os1: L1("R"), os2: L1("a") },
      bridge: { os1: L1("R"), os2: L1("a"), os3: L1("c"), och: L1("b") },
      chorus: { os1: "R-------R-------", os2: L1("a"), os3: L1("c"), obr: "R-------R---R---", och: L1("b"), otp: timpDrive },
      solo: { os1: L1("R"), os2: L1("a"), obr: "R-------R---R---", otp: timpDrive },
      outro: { os1: L1("R"), os2: L1("a"), och: L1("b"), otp: timpHit },
    };
    return table[kind];
  },
  wagakki: (kind) => {
    const arpS = "a.b.c.b.a.b.c.b.";
    const arpF = "abcbabcbabcbabcb";
    const table: Record<Kind, Record<string, string>> = {
      intro: { wsk: L1("a"), wtk: "x...............", wko: arpS },
      verse: { wko: arpS, wsh: "R...R...R.R....." },
      bridge: { wko: arpF, wsk: "a-------b-------" },
      chorus: { wko: arpF, wsh: "R..R..R.R..R..R.", wsk: L1("c"), wtk: "x.......x.x.x..." },
      solo: { wko: arpF, wsh: "R..R..R.R..R..R.", wtk: "x.......x.x.x..." },
      outro: { wsk: L1("a"), wko: "a...b...c...b...", wtk: "x..............." },
    };
    return table[kind];
  },
};

/**
 * ラウド: リズムギター（ディストーション／クランチ）を同じ刻みで2本に倍にして、左右いっぱい（-0.9／0.9）に振り、
 * ラウド専用のアンプ（メタル系は loudmetal、ロック系は loudrock）を通す。歪みギターは音割れしやすいので、1本ずつの音量は小さく抑える。
 */
function applyLoud(score: Score): void {
  const amp = score.tone === "metal" ? "loudmetal" : "loudrock";
  const out: Score["tracks"] = [];
  for (const t of score.tracks) {
    if (t.instrument === "distGuitar" || t.instrument === "crunch") {
      const volume = Math.min(t.volume, 0.1);
      out.push({ ...t, volume, pan: -0.9, amp: { type: amp }, notes: t.notes.map((n) => ({ ...n })) });
      out.push({ ...t, volume, pan: 0.9, amp: { type: amp }, notes: t.notes.map((n) => ({ ...n })) });
    } else out.push(t);
  }
  score.tracks = out;
}

/** 設計図から曲を作る。 */
/**
 * 曲の起伏: 出だしは小さく始めて少しずつ上げ、間奏では一度引き、サビで元の大きさに戻す。
 * 小節ごとに全パートの強さ（velocity）へ倍率をかける。
 */
export function applyDynamics(score: Score, kinds: readonly Kind[], beats: number): void {
  const bars: number[] = [];
  for (const kind of kinds) {
    const n = kind === "intro" ? 4 : 8;
    for (let i = 0; i < n; i++) {
      const t = i / Math.max(1, n - 1);
      let g = 1;
      if (kind === "intro") g = 0.55 + 0.3 * t; // 約-5dB → -1.5dB
      else if (kind === "verse") g = 0.82 + 0.1 * t;
      else if (kind === "bridge") g = 0.9 + 0.1 * t;
      else if (kind === "solo") g = i < 4 ? 0.72 : 0.72 + 0.28 * ((i - 3) / 4); // 引いてから戻す
      else if (kind === "outro") g = 1 - 0.3 * t;
      bars.push(g);
    }
  }
  for (const track of score.tracks) {
    let pos = 0;
    for (const ev of track.notes) {
      const bar = Math.min(bars.length - 1, Math.floor(pos / beats));
      if (bars.length) ev.velocity = (ev.velocity ?? 1) * bars[bar];
      pos += ev.durationBeats;
    }
  }
}

export function composeSong(spec: SongSpec, extra?: { vocal?: VocalSection[] }): Score {
  const rng = makeRng(spec.seed);
  const key = keyOf(spec);
  const beats = spec.beats ?? 4;
  const plan = planSections(spec.bpm, beats, spec.targetSec ?? 75);
  if (spec.style === "discord") return discordScore(spec, rng, key, plan.kinds);
  if (spec.style === "mystery") return mysteryScore(spec, rng, key, plan.kinds);
  const tpl = TEMPLATES[spec.style];
  const cells = key.minor ? CELLS_MINOR : CELLS_MAJOR;
  const cache = new Map<string, { chords: string[]; melody: string }>();
  const longForm = (spec.targetSec ?? 75) > 90;
  const flavors: Flavor[] = ([] as Flavor[]).concat(spec.flavor ?? []);
  const seen = new Map<Kind, number>();
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
  // 歌のメロディは、楽器の乱数とは別の乱数で作る（vocal を付けても、楽器の曲は変わらない）
  const vrng = makeRng((spec.seed ^ 0x5eed1234) >>> 0);
  const vcache = new Map<string, string>();
  let barCursor = 0;
  const sections: Section[] = plan.kinds.map((kind) => {
    const barsInSection = kind === "intro" ? 4 : 8;
    const sectionStartBar = barCursor;
    barCursor += barsInSection;
    const base = applyDrive(tpl.plan(kind, beats), kind, tpl, spec.drive === true && beats === 4);
    const kp0 = beats === 4 && spec.style !== "jazz" ? applyDrumRealism(base, kind, barsInSection, spec.style, tpl) : base;
    let kp = kp0;
    if (kind === "intro" && OPENING_STYLES.includes(spec.style)) {
      const len = beats * 2;
      const once = (ch: string): string => [ch + "-".repeat(len - 1), ...Array(barsInSection - 1).fill(".".repeat(len))].join(" ");
      kp = { ...kp0, parts: { ...kp0.parts, opn1: once("R"), opn2: once("5"), opn3: once("O") } };
      if (RUN_STYLES.includes(spec.style)) kp = { ...kp, opts: { ...kp.opts, opening: "run" } };
    }
    const occurrence = seen.get(kind) ?? 0;
    seen.set(kind, occurrence + 1);
    // 長尺では、Aは3種類・B／間奏は2種類の旋律を順にまわして、くり返しの単調さを減らす（サビは同じ旋律のまま＝耳に残す）
    const variant = longForm ? (kind === "verse" ? occurrence % 3 : kind === "bridge" || kind === "solo" ? occurrence % 2 : 0) : 0;
    const cacheKey = `${kind}:${variant}`;
    if (beats === 4) for (const f of flavors) if (f !== "loud") kp = { ...kp, parts: { ...kp.parts, ...FLAVOR_PLANS[f](kind) } };
    let entry = cache.get(cacheKey);
    if (!entry) {
      const chords = chordsFor(kind);
      entry = { chords, melody: kp.mel.length ? generateMelody(rng, key, chords, beats, kp.opts) : "" };
      cache.set(cacheKey, entry);
    }
    const melody: Record<string, string> = {};
    for (const m of kp.mel) melody[m] = entry.melody;
    if (spec.vocal && extra && (kind === "verse" || kind === "bridge" || kind === "chorus")) {
      let vm = vcache.get(cacheKey);
      if (vm === undefined) {
        vm = generateMelody(vrng, key, entry.chords, beats, { ...VOCAL_RANGE[kind], density: "normal" });
        vcache.set(cacheKey, vm);
      }
      (extra.vocal ??= []).push({ kind, startBeat: sectionStartBar * beats, melody: vm });
    }
    return { chords: entry.chords.join(" "), parts: kp.parts, melody };
  });
  const hasFills = beats === 4 && spec.style !== "jazz" && tpl.parts.snare?.step === 0.25;
  const flavorParts: Record<string, PartSpec> = {};
  if (beats === 4) for (const f of flavors) if (f !== "loud") Object.assign(flavorParts, FLAVOR_PARTS[f]);
  const allParts = { ...tpl.parts, ...driveParts, ...flavorParts, ...(hasFills ? TOM_PARTS : {}), ...(OPENING_STYLES.includes(spec.style) ? STRIKE_PARTS : {}) };
  const score = arrange({ tempoBpm: spec.bpm, beatsPerBar: beats, sections, parts: allParts, melodies: tpl.melodies });
  // 曲調ごとの左右の位置と、メロディのように動くベース
  const trackKeys = [...Object.keys(allParts), ...Object.keys(tpl.melodies)];
  if (tpl.pans) {
    trackKeys.forEach((k, i) => {
      if (tpl.pans![k] !== undefined && score.tracks[i]) score.tracks[i].pan = tpl.pans![k];
    });
  }
  if (tpl.walkingBass) {
    const i = trackKeys.indexOf(tpl.walkingBass);
    const barChords = sections.flatMap((s) => s.chords.split(/\s+/).filter(Boolean));
    if (i >= 0 && score.tracks[i]) score.tracks[i].notes = walkBass(score.tracks[i].notes, barChords, beats, key);
  }
  applyDynamics(score, plan.kinds, beats);
  score.drumKit = DRUM_KIT[spec.style] ?? 0;
  if (spec.style === "electro" || spec.style === "jpop" || spec.style === "dancerock") score.pump = true;
  if (OPENING_STYLES.includes(spec.style)) score.opening = true;
  score.style = spec.style;
  score.tone = METAL_STYLES.includes(spec.style) ? "metal" : "rock";
  if (flavors.includes("loud")) applyLoud(score);
  if (["electro", "phonk", "progmetal"].includes(spec.style)) score.synth = true;
  return score;
}
