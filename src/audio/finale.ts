import { arrange, midiToName, type MelodySpec, type PartSpec, type Section } from "./compose";
import type { Score } from "./score";
import { CELLS_MAJOR, CELLS_MINOR, chordName, generateMelody, keyOf, makeRng, pick, type Key, type MelodyOpts, type Rng } from "./songwriter";

/**
 * ラスボス・裏ボス・ラスト裏ボス用の、3〜4分の特別な曲を作る。メタル調にプログレッシブ（7拍子・拍子の変化・転調）を混ぜ、
 * テンポの速い曲と、テンポの遅い絶望感のある曲を用意する。遅い曲や間奏には、19世紀ロマン派（ブラームスやショパン）を意識した
 * 書き方（ピアノの分散和音の上に長い旋律、弦の厚い和音、3拍子の2小節を2拍×3にまとめるヘミオラ、短調の半音の動き）を使う。
 * これらは作風・書き方の参考にとどめ、特定の作品の旋律・進行はなぞっていない（`CLAUDE.md` 1-1）。
 */

/** 1小節の拍数（4分音符の数）。3.5=7/8拍子、4.5=9/8拍子、5=5/4拍子など。 */
type Meter = 3 | 3.5 | 4 | 4.5 | 5 | 7;
type Texture = "poly" | "unison" | "ksolo" | "oddriff" | "gsolo" | "bsolo" | "dsolo" | "motif" | "triumph" | "intro" | "nocturne" | "brahms" | "doom" | "riff" | "gallop" | "chorus" | "solo" | "breakdown" | "blast" | "void" | "coda";

interface FSec {
  tex: Texture;
  bars: number;
  meter?: Meter;
  /** この区間だけの調（転調）。 */
  tonic?: string;
  minor?: boolean;
  /** 「motif」の進み方: fall=音が下がっていく、rise=上がっていく。 */
  variant?: "fall" | "rise" | "fast";
  /** 「poly」のリフの長さ（16分音符の数。5・7・9・11・13）。1小節（4/4なら16）とずれて、小節をまたいで回り続ける。 */
  cycle?: number;
}
export interface FinaleSpec {
  id: string;
  title: string;
  scene: string;
  bpm: number;
  tonic: string;
  seed: number;
  /** GMのドラムキット（48=オーケストラ、16=パワー）。 */
  drumKit: number;
  sections: FSec[];
}

const LEN: Record<Meter, number> = { 3: 12, 3.5: 14, 4: 16, 4.5: 18, 5: 20, 7: 28 };
const cycle = (pat: string, n: number): string => pat.repeat(Math.ceil(n / pat.length)).slice(0, n);
const hold = (ch: string, n: number): string => ch + "-".repeat(n - 1);
/** 拍子ごとに決めたパターンがあればそれを、なければ4/4のパターンを繰り返して、小節の長さに合わせる。 */
const by = (m: Meter, p: { 3: string; 4: string; 7: string }): string => (p as Record<number, string>)[m] ?? cycle(p[4], LEN[m]);

const KICK_HALF = { 3: "x...........", 4: "x.......x.......", 7: "x.......x.......x..........." };
const KICK_PROG = { 3: "x.xx..x.x...", 4: "x.xx..x.x.xx..x.", 7: "x.xx..x.x.xx..x.x.xx..x.x..." };
// スネアの裏拍にはアクセント（X）、その間にゴースト（o）を入れて、グルーブを出す
const SNARE_BACK = { 3: "....x.......", 4: "..o.X.o...o.X..o", 7: "..o.X.o...o.X..o....x......." };
const SNARE_HALF = { 3: "........x...", 4: "........x.......", 7: "........x.......x..........." };
const CHUG = { 3: "R.RR.RR.R.RR", 4: "R.RR.RR.R.RR.RR.", 7: "R.RR.RR.R.RR.RR.R.RR.RR.R.RR" };
const HIT = { 3: "R-------R---", 4: "R-------R---R---", 7: "R-------R---R---R-------R---" };
const GALLOP = { 3: "R.RRR.RRR.RR", 4: "R.RRR.RRR.RRR.RR", 7: "R.RRR.RRR.RRR.RRR.RRR.RRR.RR" };
const LH = "acdbdcdb"; // ピアノの左手の分散和音（和音の1・3・5・7番目の音を行き来する）

interface Look {
  parts: (m: Meter, bars: number, cycleLen?: number) => Record<string, string>;
  mel: string[];
  opts: MelodyOpts;
  minor?: boolean;
}

/** 区間の最初の小節だけにクラッシュを鳴らす、小節ごとのパターン。 */
const crashFirst = (m: Meter, bars: number): string => [`x${".".repeat(LEN[m] - 1)}`, ...Array(bars - 1).fill(".".repeat(LEN[m]))].join(" ");

const MOTIF_CELL = "R--RR-R-"; // 「長・短・中・中」の短い動機（1.5拍・0.5拍・1拍・1拍）
/** テクニカルなドラムソロ（8小節）。グルーブ→リニアなフレーズ→パラディドル→ツーバス→タムの回し→ストップタイムの順に展開する。 */
const DRUM_SOLO = {
  kick:  ["X..x..x..x.x....", "X..x..x.x..x.x..", "X..X....X.X.....", "X...............", "xxxxxxxxxxxxxxxx", "X..x..x..x..x..x", "............xxxx", "X.......X......."],
  snare: ["....X..o.o..X..o", "....X..o.o..X.oX", "..o.X.o...o.X.o.", "X.o.X.o.........", "........X.......", "....X.......X...", "................", "....X.......X.XX"],
  hat:   ["x.xxx.xxx.xxx.xx", "x.xxx.xxx.xxxoxx", "x.x.x.x.x.x.x.x.", "................", "x.x.x.x.x.x.x.x.", "xxxxxxxxxxxxxxxx", "................", "................"],
  tomH:  ["................", "................", "................", "....X.o.X.o.....", "................", "................", "xxxx............", "................"],
  tomM:  ["................", "................", "................", "........X.o.X.o.", "................", "................", "....xxxx........", "................"],
  tomL:  ["................", "................", "................", "............X.oX", "................", "................", "........xxxx....", "................"],
  crash: ["x...............", "................", "................", "................", "x...............", "................", "................", "x..............."],
  bass:  ["R.....R...R.....", "R.....R.R.......", "R..R....R.R.....", "................", "R...............", "R..R..R..R..R..R", "................", "R.......R......."],
};
const bars8 = (a: string[], bars: number): string => Array.from({ length: bars }, (_, i) => a[i % a.length]).join(" ");

/** ポリメトリック（ずれて回るリフ）用の、16分音符のリフ。北欧の重量級プログレッシブ・メタルのような「拍とずれて聞こえる」刻み。 */
const POLY_RIFFS: Record<number, string> = { 5: "R.RR.", 7: "R.RR.R.", 9: "R..R.RR.R", 11: "R.R..RR.R..", 13: "R..R.R.RR.R.." };
function polyParts(m: Meter, bars: number, cycleLen: number): Record<string, string> {
  const q = LEN[m];
  const riff = POLY_RIFFS[cycleLen] ?? POLY_RIFFS[7];
  const n = riff.length;
  const seq = Array.from({ length: q * bars }, (_, i) => riff[i % n]);
  const slices = (chars: string[]): string => Array.from({ length: bars }, (_, b) => chars.slice(b * q, (b + 1) * q).join("")).join(" ");
  // キックはリフの音のうち1つおきにそろえる（ギターとキックが噛み合って、重く歩く）
  let ordinal = 0;
  const kick = seq.map((c) => (c === "R" ? (ordinal++ % 2 === 0 ? "x" : ".") : "."));
  const snare = Array.from({ length: q * bars }, (_, i) => (i % q) % 8 === 4 ? "X" : ".");
  return { gtrs: slices(seq), gtrs2: slices(seq), bass: slices(seq), kick: slices(kick), snare: slices(snare), hat: cycle("x.", q), crash: crashFirst(m, bars) };
}

const LOOKS: Record<Exclude<Texture, "void">, Look> = {
  poly: {
    // ポリメトリック: ギター・ベース・キックが、小節の長さと違う長さのリフを回し続け、スネアだけが拍を守る
    parts: (m, bars, cycleLen) => polyParts(m, bars, cycleLen ?? 7),
    mel: ["lead"], opts: { lo: 66, hi: 88, density: "sparse" },
  },
  oddriff: {
    // 変拍子のリフ: 3+3+2 の区切りで刻み、キックがそれに噛み合う
    parts: (m, bars) => ({ gtrs: cycle("R..R..R.", LEN[m]), gtrs2: cycle("R..R..R.", LEN[m]), bass: cycle("R..R..R.", LEN[m]), kick: cycle("x..x..x.", LEN[m]), snare: cycle("....X...", LEN[m]), hat: cycle("x.", LEN[m]), crash: crashFirst(m, bars) }),
    mel: ["synth"], opts: { lo: 62, hi: 86, density: "normal" },
  },
  unison: {
    // ギターと鍵盤が、速い旋律を同じ音でそろえて弾く（複雑なユニゾン）
    parts: (m, bars) => ({ gtrs: cycle("R.RR.RR.", LEN[m]), gtrs2: cycle("R.RR.RR.", LEN[m]), bass: cycle("R.", LEN[m]), kick: cycle("x..x..x.", LEN[m]), snare: cycle("....X...", LEN[m]), hat: cycle("xo", LEN[m]), crash: crashFirst(m, bars), s1: hold("a", LEN[m] / 2), pnL: cycle(LH, LEN[m] / 2) }),
    mel: ["lead", "synth"], opts: { lo: 64, hi: 94, density: "fast" },
  },
  ksolo: {
    // 鍵盤ソロ: シンセの速いフレーズを、ピアノの分散和音とリズム隊が支える
    parts: (m, bars) => ({ gtrs: cycle("R.RR.RR.", LEN[m]), bass: cycle("R.", LEN[m]), kick: cycle("x..x..x.", LEN[m]), snare: cycle("....X...", LEN[m]), hat: cycle("xo", LEN[m]), crash: crashFirst(m, bars), pnL: cycle(LH, LEN[m] / 2), pad: hold("a", LEN[m] / 2) }),
    mel: ["synth", "pnm"], opts: { lo: 66, hi: 96, density: "fast" },
  },
  gsolo: {
    // 遅いギターソロ: 長く伸ばす音とベンドで、泣くように歌う
    parts: (m, bars) => ({ gtrs: hold("R", LEN[m]), bass: hold("R", LEN[m]), kick: by(m, KICK_HALF), snare: by(m, SNARE_HALF), crash: crashFirst(m, bars), pad: hold("a", LEN[m] / 2), s1: hold("b", LEN[m] / 2), s2: hold("c", LEN[m] / 2), pnL: cycle(LH, LEN[m] / 2) }),
    mel: ["lead"], opts: { lo: 62, hi: 90, density: "sparse" },
  },
  bsolo: {
    // ベースソロ: 低音の旋律を主役にして、ドラムはグルーブで支える。速い曲はスラップ、遅い曲は指弾き
    parts: (m, bars) => ({ kick: by(m, KICK_PROG), snare: by(m, SNARE_BACK), hat: cycle("xo", LEN[m]), crash: crashFirst(m, bars), pad: hold("a", LEN[m] / 2), gtrs: hold("R", LEN[m]) }),
    mel: ["bassm"], opts: { lo: 36, hi: 66, density: "fast" },
  },
  dsolo: {
    parts: (_m, bars) => ({ kick: bars8(DRUM_SOLO.kick, bars), snare: bars8(DRUM_SOLO.snare, bars), hat: bars8(DRUM_SOLO.hat, bars), tomH: bars8(DRUM_SOLO.tomH, bars), tomM: bars8(DRUM_SOLO.tomM, bars), tomL: bars8(DRUM_SOLO.tomL, bars), crash: bars8(DRUM_SOLO.crash, bars), bass: bars8(DRUM_SOLO.bass, bars), pad: hold("a", 8) }),
    mel: [], opts: { lo: 62, hi: 84, density: "normal" },
  },
  motif: {
    // 運命に立ち向かう短い動機を、弦・低弦・ギター・ティンパニでそろえて叩きつける
    parts: (m, bars) => ({ cello: MOTIF_CELL, s1: MOTIF_CELL, s2: MOTIF_CELL.replace(/R/g, "c"), gtrs: "R-----R-R---R---", kick: "x.....x.x...x...", crash: crashFirst(m, bars), pad: hold("a", LEN[m] / 2) }),
    mel: ["lead", "vln"], opts: { lo: 72, hi: 90, density: "normal" },
  },
  triumph: {
    // 闇を抜けた先の長調の勝利。ブラスと弦と合唱が高らかに歌う
    parts: (m, bars) => ({ gtrs: by(m, HIT), gtrs2: by(m, HIT), bass: cycle("R.", LEN[m]), kick: cycle("x.", LEN[m]), snare: by(m, SNARE_BACK), hat: cycle("x.", LEN[m]), crash: crashFirst(m, bars), s1: hold("a", LEN[m] / 2), s2: hold("b", LEN[m] / 2), s3: hold("c", LEN[m] / 2), pad: hold("a", LEN[m] / 2), pnL: cycle(LH, LEN[m] / 2) }),
    mel: ["brass", "vln"], opts: { lo: 67, hi: 92, density: "normal" },
  },
  intro: {
    parts: (m, bars) => ({ kick: by(m, KICK_HALF), crash: crashFirst(m, bars), pad: hold("a", LEN[m] / 2), pnL: cycle(LH, LEN[m] / 2), s1: hold("b", LEN[m] / 2) }),
    mel: ["pnm"], opts: { lo: 64, hi: 86, density: "sparse" },
  },
  nocturne: {
    // ショパンの夜想曲を意識: 左手の広い分散和音の上に、装飾的な長い旋律
    parts: (m) => ({ pnL: cycle(LH, LEN[m] / 2), pad: hold("a", LEN[m] / 2), s1: hold("c", LEN[m] / 2) }),
    mel: ["pnm"], opts: { lo: 64, hi: 90, density: "normal" },
  },
  brahms: {
    // ブラームスを意識: 弦の厚い和音、低弦の持続、3拍子ではヘミオラ
    parts: (m) => ({ cello: hold("R", LEN[m] / 2), s1: hold("a", LEN[m] / 2), s2: hold("b", LEN[m] / 2), s3: hold("c", LEN[m] / 2), pnL: cycle("acbcdcbc", LEN[m] / 2) }),
    mel: ["vln"], opts: { lo: 62, hi: 86, density: "normal", hemiola: true },
  },
  doom: {
    parts: (m, bars) => ({ gtrs: cycle("R", LEN[m]).replace(/R+/, hold("R", LEN[m])), gtrs2: hold("R", LEN[m]), bass: hold("R", LEN[m]), kick: by(m, KICK_HALF), snare: by(m, SNARE_HALF), crash: crashFirst(m, bars), pad: hold("a", LEN[m] / 2) }),
    mel: ["lead"], opts: { lo: 58, hi: 82, density: "sparse" },
  },
  riff: {
    parts: (m, bars) => ({ gtrs: by(m, CHUG), gtrs2: by(m, CHUG), bass: cycle("R.", LEN[m]), kick: by(m, KICK_PROG), snare: by(m, SNARE_BACK), hat: cycle("x.", LEN[m]), crash: crashFirst(m, bars) }),
    mel: ["synth"], opts: { lo: 62, hi: 84, density: "normal" },
  },
  gallop: {
    parts: (m, bars) => ({ gtrs: by(m, GALLOP), gtrs2: by(m, GALLOP), bass: by(m, GALLOP), kick: cycle("x.", LEN[m]), snare: by(m, SNARE_BACK), hat: cycle("xo", LEN[m]), crash: crashFirst(m, bars), s1: hold("a", LEN[m] / 2), s2: hold("b", LEN[m] / 2) }),
    mel: [], opts: { lo: 62, hi: 84, density: "normal" },
  },
  chorus: {
    parts: (m, bars) => ({ gtrs: by(m, HIT), gtrs2: by(m, HIT), bass: cycle("R.", LEN[m]), kick: cycle("x.", LEN[m]), snare: by(m, SNARE_BACK), hat: cycle("x.", LEN[m]), crash: crashFirst(m, bars), s1: hold("a", LEN[m] / 2), s2: hold("b", LEN[m] / 2), s3: hold("c", LEN[m] / 2), pad: hold("a", LEN[m] / 2), pnL: cycle(LH, LEN[m] / 2) }),
    mel: ["lead", "vln"], opts: { lo: 69, hi: 92, density: "normal" },
  },
  solo: {
    parts: (m, bars) => ({ gtrs: by(m, CHUG), gtrs2: by(m, CHUG), bass: cycle("R.", LEN[m]), kick: cycle("x.", LEN[m]), snare: by(m, SNARE_BACK), hat: cycle("xo", LEN[m]), crash: crashFirst(m, bars), s1: hold("a", LEN[m] / 2), s2: hold("c", LEN[m] / 2) }),
    mel: ["lead"], opts: { lo: 72, hi: 96, density: "fast" },
  },
  breakdown: {
    parts: (m, bars) => ({ gtrs: hold("R", LEN[m]), gtrs2: hold("R", LEN[m]), bass: hold("R", LEN[m]), kick: by(m, KICK_PROG), snare: by(m, SNARE_HALF), crash: crashFirst(m, bars) }),
    mel: ["synth"], opts: { lo: 58, hi: 78, density: "sparse" },
  },
  blast: {
    parts: (m, bars) => ({ gtrs: cycle("R", LEN[m]), gtrs2: cycle("R", LEN[m]), bass: cycle("R", LEN[m]), kick: cycle("x", LEN[m]), snare: cycle("x.", LEN[m]), crash: crashFirst(m, bars) }),
    mel: ["lead"], opts: { lo: 64, hi: 90, density: "fast" },
  },
  coda: {
    parts: (m) => ({ pnL: cycle(LH, LEN[m] / 2), pad: hold("a", LEN[m] / 2), s1: hold("b", LEN[m] / 2) }),
    mel: ["pnm"], opts: { lo: 62, hi: 84, density: "sparse" },
  },
};

const PARTS: Record<string, PartSpec> = {
  kick: { instrument: "kick", waveform: "sine", volume: 0.3, octave: 2, step: 0.25, fixed: "C2" },
  snare: { instrument: "snare", waveform: "sine", volume: 0.27, octave: 2, step: 0.25, fixed: "C3" },
  hat: { instrument: "hihat", waveform: "sine", volume: 0.11, octave: 2, step: 0.25, fixed: "C6" },
  crash: { instrument: "crash", waveform: "sine", volume: 0.18, octave: 2, step: 0.25, fixed: "C5" },
  gtrs: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.2, octave: 2, step: 0.25 },
  gtrs2: { instrument: "distGuitar", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.25 },
  bass: { instrument: "bass", waveform: "triangle", volume: 0.3, octave: 2, step: 0.25 },
  cello: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 2, step: 0.5 },
  s1: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
  s2: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
  s3: { instrument: "strings", waveform: "sawtooth", volume: 0.08, octave: 4, step: 0.5 },
  pnL: { instrument: "piano", waveform: "triangle", volume: 0.12, octave: 2, step: 0.5 },
  pad: { instrument: "choir", waveform: "sine", volume: 0.09, octave: 3, step: 0.5 },
  tomH: { instrument: "tom", waveform: "sine", volume: 0.26, octave: 2, step: 0.25, fixed: "D3" },
  tomM: { instrument: "tom", waveform: "sine", volume: 0.26, octave: 2, step: 0.25, fixed: "B2" },
  tomL: { instrument: "tom", waveform: "sine", volume: 0.28, octave: 2, step: 0.25, fixed: "G2" },
  opn1: { instrument: "brass", waveform: "sawtooth", volume: 0.24, octave: 3, step: 0.5 },
  opn2: { instrument: "strings", waveform: "sawtooth", volume: 0.16, octave: 3, step: 0.5 },
  opn3: { instrument: "brass", waveform: "sawtooth", volume: 0.2, octave: 4, step: 0.5 },
};
const MELODIES: Record<string, MelodySpec> = {
  lead: { instrument: "leadGuitar", waveform: "sawtooth", volume: 0.17 },
  synth: { instrument: "lead", waveform: "square", volume: 0.12 },
  vln: { instrument: "strings", waveform: "sawtooth", volume: 0.15 },
  pnm: { instrument: "piano", waveform: "triangle", volume: 0.15 },
  w1: { instrument: "strings", waveform: "sawtooth", volume: 0.09 },
  b1: { instrument: "bell", waveform: "sine", volume: 0.1 },
  slapm: { instrument: "slap", waveform: "triangle", volume: 0.34 },
  bassm: { instrument: "bass", waveform: "triangle", volume: 0.34 },
  brass: { instrument: "brass", waveform: "sawtooth", volume: 0.17 },
};

const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

/** 「虚無」の区間: 減和音の重なり、半音ではい回る弦、悪魔の音程の鐘。 */
function voidSection(rng: Rng, tonic: number, meter: Meter, bars: number): Section {
  const total = bars * meter;
  const name = (semi: number, oct: number): string => `${NAMES[(tonic + semi) % 12]}${oct}`;
  const worm: string[] = [];
  const bells: string[] = [];
  let cursor = 0;
  let semi = pick(rng, [0, 1, 6]);
  while (cursor < total) {
    const len = Math.min(total - cursor, pick(rng, [2, 3, 4]));
    if (rng() < 0.18) worm.push(`R:${len}`);
    else {
      semi = Math.max(0, Math.min(14, semi + pick(rng, [-1, 1, 1, -2, 6, -1])));
      worm.push(`${name(semi, 4)}:${len}`);
    }
    cursor += len;
  }
  cursor = 0;
  while (cursor < total) {
    const gap = Math.min(total - cursor, pick(rng, [2, 3, 4, 5.5, 7]));
    bells.push(`R:${gap}`);
    cursor += gap;
    if (cursor < total) {
      bells.push(`${name(pick(rng, [6, 6, 1, 11, 8]), pick(rng, [5, 6]))}:0.5`);
      cursor += 0.5;
    }
  }
  const dimChord = `${NAMES[tonic]}dim`;
  return {
    chords: Array(bars).fill(dimChord).join(" "),
    beatsPerBar: meter,
    parts: { pad: hold("a", LEN[meter] / 2), s1: hold("b", LEN[meter] / 2), s2: hold("c", LEN[meter] / 2), kick: cycle("x...............", LEN[meter]) },
    melody: { w1: worm.join(" "), b1: bells.join(" ") },
  };
}

/** 冷たい旋律: 半音・減5度・短6度をまぜた、まばらな高音（休みも多い）。 */
function coldMelody(rng: Rng, tonic: number, total: number): string {
  const out: string[] = [];
  let cursor = 0;
  while (cursor < total) {
    const len = Math.min(total - cursor, pick(rng, [1, 1.5, 2, 3, 4]));
    if (rng() < 0.3) out.push(`R:${len}`);
    else out.push(`${NAMES[(tonic + pick(rng, [0, 1, 3, 6, 7, 8, 10, 11])) % 12]}${pick(rng, [5, 5, 6])}:${len}`);
    cursor += len;
  }
  return out.join(" ");
}

/** 動機（長・短・中・中）を、度数 d の和音の上に1小節ぶん書く。 */
function motifBar(key: Key, d: number): string {
  const semi = (i: number): number => key.scale[i % 7] + 12 * Math.floor(i / 7);
  const notes = [d - 1, d, d + 2, d + 1].map((i) => midiToName(60 + key.tonic + semi(i + 7)));
  return `${notes[0]}:1.5 ${notes[1]}:0.5 ${notes[2]}:1 ${notes[3]}:1`;
}

/** 設計図から、3〜4分の特別な曲を作る。 */
export function composeFinale(spec: FinaleSpec): Score {
  const rng = makeRng(spec.seed);
  const cache = new Map<string, { chords: string[]; melody: string }>();
  const sections: Section[] = spec.sections.map((sec) => {
    const meter: Meter = sec.meter ?? 4;
    const tonic = sec.tonic ?? spec.tonic;
    const key = keyOf({ tonic, minor: sec.minor ?? (sec.tex !== "triumph") });
    if (sec.tex === "void") return voidSection(rng, key.tonic, meter, sec.bars);
    const look0 = LOOKS[sec.tex];
    // ベースソロは、速い曲ではスラップ、遅い曲では指弾き。曲の最初の区間には、駆け上がる出だしの音型をつける
    const look: Look = sec.tex === "bsolo" ? { ...look0, mel: [sec.variant === "fast" ? "slapm" : "bassm"], opts: { ...look0.opts, density: sec.variant === "fast" ? "fast" : "normal" } } : look0;
    const isFirst = spec.sections[0] === sec;
    const melOpts: MelodyOpts = isFirst && sec.tex !== "motif" ? { ...look.opts, opening: "run" } : look.opts;
    const id = `${sec.tex}|${meter}|${tonic}|${sec.bars}|${sec.variant ?? ""}|${sec.cycle ?? ""}`;
    let entry = cache.get(id);
    if (!entry) {
      if (sec.tex === "poly") {
        // 根音を保ち、ときどき半音上・下の和音に落ちる（重く単調で、冷たい）
        const seq = [1, 1, 1, 1, 1, 1, 6, 1];
        const degrees = Array.from({ length: sec.bars }, (_, i) => seq[i % seq.length]);
        const chords = degrees.map((d) => chordName(key, d, false));
        entry = { chords, melody: coldMelody(rng, key.tonic, sec.bars * meter) };
      } else if (sec.tex === "motif") {
        // 動機を1小節ごとに、音が下がる（または上がる）順序で移していく
        const seq = sec.variant === "rise" ? [1, 2, 3, 4, 5, 5, 5, 5] : [1, 1, 7, 7, 6, 6, 5, 5];
        const degrees = Array.from({ length: sec.bars }, (_, i) => seq[i % seq.length]);
        const chords = degrees.map((d) => chordName(key, d, false));
        entry = { chords, melody: degrees.map((d) => motifBar(key, d)).join(" ") };
      } else {
        const cell = pick(rng, key.minor ? CELLS_MINOR : CELLS_MAJOR);
        const second = [...cell.slice(0, 3), pick(rng, [5, 4, cell[3]])];
        const degrees = [...cell, ...second, ...cell, ...second].slice(0, sec.bars);
        const chords = degrees.map((d) => chordName(key, d, false));
        entry = { chords, melody: look.mel.length ? generateMelody(rng, key, chords, meter, melOpts) : "" };
      }
      cache.set(id, entry);
    }
    const melody: Record<string, string> = {};
    for (const m of look.mel) melody[m] = entry.melody;
    const parts = look.parts(meter, sec.bars, sec.cycle);
    if (isFirst) {
      // 曲の頭の一撃（全員で和音を長く鳴らす）
      const len = meter * 2;
      const once = (ch: string): string => [ch + "-".repeat(len - 1), ...Array(sec.bars - 1).fill(".".repeat(len))].join(" ");
      Object.assign(parts, { opn1: once("R"), opn2: once("5"), opn3: once("O") });
    }
    return { chords: entry.chords.join(" "), beatsPerBar: meter, parts, melody };
  });
  const score = arrange({ tempoBpm: spec.bpm, beatsPerBar: 4, sections, parts: PARTS, melodies: MELODIES });
  score.drumKit = spec.drumKit;
  score.opening = true;
  return score;
}

const S = (tex: Texture, bars: number, meter: Meter = 4, extra: Partial<FSec> = {}): FSec => ({ tex, bars, meter, ...extra });

export const FINALES: FinaleSpec[] = [
  // ラスボス（速い）: 拍子を7/4と4/4で行き来し、間奏はブラームス風の3拍子、最後のサビは全音上へ転調
  {
    id: "boss-final", title: "終わりの灯", scene: "最終ボス戦（第1形態・速い）", bpm: 172, tonic: "E", seed: 201, drumKit: 16,
    sections: [S("intro", 8), S("riff", 8, 7), S("poly", 8, 4, { cycle: 7 }), S("gallop", 8), S("chorus", 16), S("brahms", 8, 3), S("unison", 8, 3.5), S("solo", 16), S("bsolo", 8, 4, { variant: "fast" }), S("dsolo", 8), S("breakdown", 8, 7), S("gallop", 8), S("chorus", 16), S("chorus", 16, 4, { tonic: "F#" }), S("coda", 8)],
  },
  // ラスボス（遅い・絶望）: ショパン風の夜想曲、ブラームス風の弦、ドゥーム調のギター
  {
    id: "boss-final-2", title: "灯の環、砕けるとき", scene: "最終ボス戦（第2形態・絶望）", bpm: 74, tonic: "C", seed: 202, drumKit: 48,
    sections: [S("intro", 8), S("nocturne", 8), S("brahms", 8), S("doom", 8), S("brahms", 8, 3), S("doom", 8), S("gsolo", 8), S("bsolo", 8), S("coda", 8)],
  },
  // 裏ボス（遅い・絶望）: 虚無の響きと、ロマン派のピアノ・弦
  {
    id: "secret-boss", title: "初源の歪み", scene: "裏ボス「初源の歪み」（絶望）", bpm: 66, tonic: "F#", seed: 203, drumKit: 48,
    sections: [S("void", 8), S("nocturne", 8), S("doom", 8), S("bsolo", 8), S("brahms", 8, 3), S("doom", 8), S("gsolo", 8), S("coda", 8)],
  },
  // 裏ボス（速い）: ブラストビートと7拍子
  {
    id: "secret-boss-2", title: "歪みの深淵", scene: "裏ボス「初源の歪み」（速い）", bpm: 200, tonic: "D", seed: 204, drumKit: 16,
    sections: [S("intro", 8), S("blast", 8), S("riff", 8, 7), S("poly", 8, 4, { cycle: 9 }), S("chorus", 16), S("solo", 16), S("bsolo", 8, 4, { variant: "fast" }), S("dsolo", 8), S("breakdown", 8, 7), S("riff", 8, 7), S("gallop", 8), S("chorus", 16), S("blast", 8), S("riff", 8, 7), S("gallop", 8), S("coda", 8)],
  },
  // ラスト裏ボス「八神」（速い）: 8柱それぞれの区間で調が上がっていく
  {
    id: "eight-gods", title: "八神の試練", scene: "ラスト裏ボス「八神」（速い）", bpm: 184, tonic: "E", seed: 205, drumKit: 16,
    sections: [
      S("intro", 8), S("riff", 8, 7, { tonic: "E" }), S("poly", 8, 4, { tonic: "F#", cycle: 11 }), S("riff", 8, 7, { tonic: "G" }), S("gallop", 8, 4, { tonic: "A" }),
      S("riff", 8, 7, { tonic: "B" }), S("blast", 8, 4, { tonic: "C" }), S("riff", 8, 7, { tonic: "D" }), S("gallop", 8, 4, { tonic: "E" }),
      S("chorus", 16), S("ksolo", 8, 3.5), S("solo", 16), S("bsolo", 8, 4, { variant: "fast" }), S("dsolo", 8), S("brahms", 8, 3), S("chorus", 16, 4, { tonic: "G" }), S("coda", 8),
    ],
  },
  // ラスト裏ボス「八神」（遅い・絶望）
  {
    id: "eight-gods-2", title: "八神、沈黙", scene: "ラスト裏ボス「八神」（絶望）", bpm: 60, tonic: "B", seed: 206, drumKit: 48,
    sections: [S("nocturne", 8), S("brahms", 8), S("doom", 8), S("brahms", 8, 3), S("gsolo", 8), S("bsolo", 8), S("coda", 8)],
  },
];

// 運命に立ち向かう曲: 短い動機が叩きつけられ、嵐と迷いを抜けて、短調から長調の勝利へ（闇から光へ、という気持ちの流れ）
FINALES.push({
  id: "fate", title: "運命の扉", scene: "運命に立ち向かう場面・終盤の決意", bpm: 112, tonic: "C", seed: 207, drumKit: 48,
  sections: [
    S("motif", 8), S("motif", 8, 4, { variant: "rise" }), S("riff", 8), S("brahms", 8, 3), S("gallop", 8), S("solo", 8), S("bsolo", 8, 4, { variant: "fast" }), S("motif", 8, 4, { variant: "rise", tonic: "G" }),
    S("triumph", 16), S("triumph", 16, 4, { tonic: "D" }), S("triumph", 8),
  ],
});

// 難関のボス・強敵向けの、プログレッシブな長い曲。(1)夢幻回廊: 変拍子（7/8・5/4・9/8）の行き来、ギターと鍵盤の複雑なユニゾン、鍵盤ソロ、ギターソロ、叙情的な3拍子の間奏、大きなサビ。
// (2)歯車の咆哮: ポリメトリック（小節と違う長さのリフが、ずれながら回り続ける）、重く冷たい刻み、ドゥーム調の重い間奏。
FINALES.push(
  {
    id: "prog-1", title: "夢幻回廊", scene: "難関ダンジョンのボス（変拍子・ユニゾン・鍵盤ソロ）", bpm: 150, tonic: "D", seed: 208, drumKit: 16,
    sections: [
      S("intro", 8), S("oddriff", 8, 3.5), S("oddriff", 8, 5), S("unison", 8), S("chorus", 16), S("ksolo", 16, 3.5), S("solo", 16), S("bsolo", 8, 4, { variant: "fast" }), S("dsolo", 8), S("unison", 8, 4.5),
      S("nocturne", 8, 3), S("oddriff", 8, 3.5), S("chorus", 16), S("coda", 8),
    ],
  },
  {
    id: "poly-1", title: "歯車の咆哮", scene: "強敵との戦闘（ポリメトリック・重量級）", bpm: 138, tonic: "F", seed: 209, drumKit: 16,
    sections: [
      S("intro", 8), S("poly", 8, 4, { cycle: 7 }), S("poly", 8, 4, { cycle: 9 }), S("poly", 8, 4, { cycle: 5 }), S("poly", 8, 4, { cycle: 13 }), S("doom", 8),
      S("poly", 8, 4, { cycle: 7 }), S("poly", 8, 4, { cycle: 11 }), S("solo", 16), S("bsolo", 8, 4, { variant: "fast" }), S("poly", 16, 4, { cycle: 9 }), S("doom", 8), S("coda", 8),
    ],
  },
);

/** `midiToName` を再輸出（未使用警告の回避）。 */
export { midiToName };
