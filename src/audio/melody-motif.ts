import { midiToName } from "./compose";

/**
 * モチーフ展開型のメロディ生成。
 * 小節ごとに音をランダムに歩かせるのではなく、「2小節のモチーフ（リズム＋音の動き）」を1つ作り、それを
 *   A（提示）→ A'（くり返し＋答え）→ B（1段上へ移して展開）→ C（終止）
 * と発展させて、8小節のまとまった旋律にする。サビは高く・長い音を多く、Aメロは低く狭く、Bメロは上へ向かう。
 * 強い拍の音はその小節のコードの音に合わせ、2小節ごとに息つぎ（歌のとき）、最後の小節は長い音でおさめる。
 * 同じ設計（乱数の種）なら、いつも同じ旋律になる。
 */

export type MotifRole = "verse" | "bridge" | "chorus" | "solo" | "intro" | "outro";

export interface MotifOpts {
  lo: number;
  hi: number;
  role: MotifRole;
  /** 歌えるメロディにする（最短0.5拍・跳躍を小さく・フレーズの終わりに息つぎ）。 */
  singable?: boolean;
  /** 音の細かさ。solo は細かく、intro・outro は少なめ。 */
  density?: "normal" | "sparse" | "fast";
}

type Rng = () => number;
const pick = <T,>(rng: Rng, xs: readonly T[]): T => xs[Math.floor(rng() * xs.length)];

// 1小節のリズム（拍数の合計がちょうど1小節になる並び）。
const CELLS: Record<number, number[][]> = {
  4: [[1, 1, 1, 1], [1.5, 0.5, 1, 1], [1, 0.5, 0.5, 2], [2, 1, 1], [0.5, 0.5, 1, 1, 1], [1, 1, 2], [1.5, 0.5, 2], [0.5, 1, 0.5, 2], [1, 0.5, 0.5, 1, 1], [2, 2], [0.5, 0.5, 0.5, 0.5, 1, 1], [1, 1, 1, 0.5, 0.5]],
  3: [[1, 1, 1], [2, 1], [1, 2], [1.5, 0.5, 1], [0.5, 0.5, 1, 1], [1, 0.5, 0.5, 1], [3]],
  7: [[2, 2, 3], [1.5, 1.5, 2, 2], [3, 2, 2], [1, 1, 1, 1, 3], [2, 1, 1, 3], [1, 1, 2, 3]],
};
const CELLS_FAST4 = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 1, 1], [0.5, 0.5, 1, 0.5, 0.5, 1], [0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25], [1, 0.5, 0.5, 0.5, 0.5, 1]];
const CELLS_SPARSE4 = [[2, 2], [4], [3, 1], [2, 1, 1], [1, 3]];

function cellsFor(beats: number, density: "normal" | "sparse" | "fast", singable: boolean): number[][] {
  let list: number[][];
  if (beats === 4 && density === "fast") list = CELLS_FAST4;
  else if (beats === 4 && density === "sparse") list = CELLS_SPARSE4;
  else list = CELLS[beats] ?? CELLS[4];
  if (singable) list = list.filter((c) => c.every((d) => d >= 0.5));
  return list.length ? list : (CELLS[beats] ?? CELLS[4]);
}

const chordPcs = (name: string): number[] => {
  const PC: Record<string, number> = { C: 0, "C#": 1, D: 2, "D#": 3, E: 4, F: 5, "F#": 6, G: 7, "G#": 8, A: 9, "A#": 10, B: 11 };
  const m = /^([A-G]#?)(maj7|m7|m|7|dim)?$/.exec(name);
  if (!m) throw new Error(`和音名を読めません: ${name}`);
  const shape = { "": [0, 4, 7], m: [0, 3, 7], "7": [0, 4, 7, 10], maj7: [0, 4, 7, 11], m7: [0, 3, 7, 10], dim: [0, 3, 6] }[m[2] ?? ""]!;
  return shape.map((x) => (PC[m[1]] + x) % 12);
};

interface BarSpec {
  rhythm: number[];
  /** 前の音からの、音階の段の動き（先頭の音は anchor からの動き）。 */
  steps: number[];
  /** 小節の先頭の音を、この段（pool の添字）から始める。undefined なら前の音から続ける。 */
  anchor?: number;
  /** 2小節のフレーズの終わり（息つぎの場所）。 */
  phraseEnd?: boolean;
}

/** 次の「段」の動きを選ぶ（順次進行が多く、大きな跳躍のあとは逆向きに戻る）。 */
function nextStep(rng: Rng, prev: number, singable: boolean): number {
  const leapCap = singable ? 4 : 5;
  let step: number;
  const r = rng();
  if (r < 0.12) step = 0;
  else if (r < 0.4) step = 1;
  else if (r < 0.68) step = -1;
  else if (r < 0.78) step = 2;
  else if (r < 0.88) step = -2;
  else if (r < 0.93) step = 3;
  else if (r < 0.97) step = -3;
  else step = rng() < 0.5 ? leapCap : -leapCap;
  // 大きな跳躍（3段以上）のあとは、反対向きに小さく戻る
  if (Math.abs(prev) >= 3 && Math.sign(step) === Math.sign(prev) && step !== 0) step = -Math.sign(prev) * Math.min(2, Math.abs(step));
  return step;
}

function makeSteps(rng: Rng, rhythm: number[], singable: boolean, first: number, lastPrev = 0): number[] {
  const steps: number[] = [];
  let prev = lastPrev;
  rhythm.forEach((_, i) => {
    const s = i === 0 ? first : nextStep(rng, prev, singable);
    steps.push(s);
    prev = s;
  });
  return steps;
}

/** メロディを作る。返す文字列は "C4:1 E4:0.5 R:0.5 …" の形（音名:拍）。 */
export function generateMotifMelody(rng: Rng, scale: readonly number[], tonic: number, chords: string[], beats: number, opts: MotifOpts): string {
  const singable = opts.singable === true;
  const density = opts.density ?? (opts.role === "solo" ? "fast" : opts.role === "intro" || opts.role === "outro" ? "sparse" : "normal");
  const pool: number[] = [];
  for (let m = opts.lo; m <= opts.hi; m++) if (scale.includes(((m - tonic) % 12 + 12) % 12)) pool.push(m);
  const nBars = chords.length;
  const cells = cellsFor(beats, density, singable);
  const at = (frac: number): number => Math.max(0, Math.min(pool.length - 1, Math.round(frac * (pool.length - 1))));
  const snap = (idx: number, bar: number, maxShift = 2): number => {
    const pcs = chordPcs(chords[Math.min(bar, nBars - 1)]);
    let best = idx;
    let bestD = Infinity;
    for (let i = Math.max(0, idx - maxShift); i <= Math.min(pool.length - 1, idx + maxShift); i++) {
      if (!pcs.includes(pool[i] % 12)) continue;
      const d = Math.abs(i - idx) + rng() * 0.3;
      if (d < bestD) {
        bestD = d;
        best = i;
      }
    }
    return best;
  };

  // 役割ごとの音域の目安（pool の割合）
  const home = { verse: 0.34, bridge: 0.46, chorus: 0.62, solo: 0.55, intro: 0.45, outro: 0.4 }[opts.role];
  const rise = { verse: 2, bridge: 3, chorus: 3, solo: 2, intro: 1, outro: 1 }[opts.role];

  // 1) 2小節のモチーフ
  // 1小節目は、長さの違う音が混ざるもの（拍の動きが単調にならない）。2小節目は、終わりが長い音（息をつける）
  const varied = cells.filter((c) => new Set(c).size >= 2);
  const longEnd = cells.filter((c) => c[c.length - 1] >= 2 && c.length >= 2);
  const r1 = pick(rng, varied.length ? varied : cells);
  const endPool = longEnd.filter((c) => JSON.stringify(c) !== JSON.stringify(r1));
  const r2 = pick(rng, endPool.length ? endPool : longEnd.length ? longEnd : cells);
  const m1 = makeSteps(rng, r1, singable, 0);
  const m2 = makeSteps(rng, r2, singable, nextStep(rng, m1[m1.length - 1], singable));
  const endRhythm = beats === 4 ? [1, 3] : beats === 3 ? [1, 2] : [3, 4];
  const cadenceRhythm = opts.role === "chorus" || opts.role === "outro" ? (beats === 4 ? [2, 2] : beats === 3 ? [3] : [3, 4]) : endRhythm;

  const a0 = snap(at(home), 0);
  const bars: BarSpec[] = [];
  const bar = (rhythm: number[], steps: number[], anchor?: number, phraseEnd = false): void => {
    bars.push({ rhythm, steps, anchor, phraseEnd });
  };

  if (nBars >= 8) {
    // A（提示）
    bar(r1, m1, a0);
    bar(r2, m2, undefined, true);
    // A'（くり返し。2小節目の動きだけ新しくして「答え」にする）
    bar(r1, m1, a0);
    bar(r2, makeSteps(rng, r2, singable, nextStep(rng, m1[m1.length - 1], singable)), undefined, true);
    // B（モチーフを rise 段上へ移す。2小節目は反行（上下を逆にした動き））
    const b0 = snap(Math.min(pool.length - 1, a0 + rise), 4);
    bar(r1, m1, b0);
    bar(r2, m2.map((s, i) => (i === 0 ? s : -s)), undefined, true);
    // C（終止。モチーフの頭をもう一度、最後は長い音でおさめる）
    bar(opts.role === "chorus" ? r1 : r2, opts.role === "chorus" ? m1 : makeSteps(rng, r2, singable, 1), snap(Math.min(pool.length - 1, a0 + (opts.role === "chorus" ? rise - 1 : 1)), 6));
    bar(cadenceRhythm, cadenceRhythm.map((_, i) => (i === 0 ? pick(rng, [-1, -2, 1]) : pick(rng, [0, -1, 1]))), undefined, true);
  } else {
    // 4小節（イントロなど）: A, A', 終止
    bar(r1, m1, a0);
    bar(r2, m2, undefined, true);
    bar(r1, m1, snap(Math.min(pool.length - 1, a0 + 1), 2));
    bar(cadenceRhythm, cadenceRhythm.map((_, i) => (i === 0 ? pick(rng, [-1, -2, 1]) : pick(rng, [0, -1, 1]))), undefined, true);
  }

  // 2) 音にする。強い拍の音は、その小節のコードの音に寄せる。
  const out: string[] = [];
  let idx = a0;
  let climax = 0;
  for (let b = 0; b < nBars; b++) {
    const spec = bars[b] ?? bars[bars.length - 1];
    let pos = 0;
    let barNotes: { idx: number; dur: number }[] = [];
    spec.rhythm.forEach((dur, i) => {
      if (i === 0 && spec.anchor !== undefined) idx = spec.anchor;
      else idx += spec.steps[i] ?? 0;
      if (idx < 0) idx = -idx;
      if (idx > pool.length - 1) idx = 2 * (pool.length - 1) - idx;
      idx = Math.max(0, Math.min(pool.length - 1, idx));
      const strong = (i === 0 && spec.anchor === undefined) || pos === 0 || dur >= 2 || (beats === 4 && pos === 2);
      if (strong) idx = snap(idx, b, spec.anchor !== undefined && i === 0 ? 1 : 2);
      barNotes.push({ idx, dur });
      pos += dur;
    });
    // 最後の小節の最後の音: コードの音（サビ・アウトロは主音側）で長くおさめる
    if (b === nBars - 1) {
      const last = barNotes[barNotes.length - 1];
      const pcs = chordPcs(chords[b]);
      const preferRoot = opts.role === "chorus" || opts.role === "outro";
      let best = last.idx;
      let bestD = Infinity;
      for (let i = 0; i < pool.length; i++) {
        if (!pcs.includes(pool[i] % 12)) continue;
        const d = Math.abs(i - at(home)) + (preferRoot && pool[i] % 12 !== pcs[0] ? 3 : 0);
        if (d < bestD) {
          bestD = d;
          best = i;
        }
      }
      last.idx = best;
      idx = best;
    }
    // 歌のとき: 2小節ごとの終わりで、最後の音を半拍短くして息つぎ（休符）を入れる
    let rest = 0;
    if (singable && spec.phraseEnd && b < nBars - 1) {
      const last = barNotes[barNotes.length - 1];
      if (last.dur >= 1.5) {
        last.dur -= 0.5;
        rest = 0.5;
      }
    }
    for (const n of barNotes) {
      climax = Math.max(climax, n.idx);
      out.push(`${midiToName(pool[n.idx])}:${n.dur}`);
    }
    if (rest > 0) out.push(`R:${rest}`);
    barNotes = [];
  }
  void climax;
  return out.join(" ");
}
