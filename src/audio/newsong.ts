import { midiToName } from "./compose";
import { REST, type Instrument, type NoteEvent, type Score, type Track } from "./score";
import { barBeats, type TimeSignature } from "./time-signature";
import { placeGhosts } from "./drum-genres";

/** 自動伴奏の雰囲気の一覧（ai-song.ts の検証・JSON schema・作曲ソフトの選択肢が、ここを共通で使う）。 */
export const NEW_SONG_FEELS = ["rock", "pop", "ballad", "dance", "vocaloid", "funk", "reggae", "bossa", "jazz", "shuffle", "metal", "disco", "hiphop", "trap", "dnb", "halftime"] as const;
export type NewSongFeel = (typeof NEW_SONG_FEELS)[number];
/** ジャンル別の型で作る feel（docs/sound/bassline-guide.md・drum-genre-guide.md）。 */
export const GENRE_FEELS = ["funk", "reggae", "bossa", "jazz", "shuffle", "metal", "disco", "hiphop", "trap", "dnb", "halftime"] as const;
const isGenreFeel = (f: NewSongFeel): f is (typeof GENRE_FEELS)[number] => (GENRE_FEELS as readonly string[]).includes(f);
/** feel ごとの、ベース音源（--bass）の目安。bassline-guide.md §6 に対応。 */
export const FEEL_BASS_OVERLAY: Record<NewSongFeel, string> = {
  rock: "pick", pop: "jpop", ballad: "finger", dance: "std", vocaloid: "jpop",
  funk: "std", reggae: "finger", bossa: "finger", jazz: "jazz", shuffle: "finger", metal: "metal", disco: "finger", hiphop: "std", trap: "std", dnb: "std", halftime: "std",
};
/** feel ごとの、ドラム音源（--drums）の目安と drumMix のジャンル名（drum-genres.ts）。 */
export const FEEL_DRUM_GENRE: Partial<Record<NewSongFeel, string>> = {
  rock: "rock", pop: "pop", ballad: "ballad", vocaloid: "vocaloid", funk: "funk", reggae: "reggae", bossa: "bossa", jazz: "jazz", shuffle: "rock", metal: "metal", disco: "disco", hiphop: "hiphop", trap: "trap", dnb: "dnb", halftime: "dubstep", dance: "house",
};

/** 作曲ソフトの「新しい曲」: コード進行から、バンド編成の伴奏（と、空のメロディのトラック）を作る。 */
export interface NewSongSpec {
  bpm: number;
  /** 1小節の拍の数（3・4・6・7など）。 */
  beats: number;
  /** コード進行。空白か「|」でくぎる（例: "Am F C G"）。 */
  chords: string;
  /** 各コードの小節数。 */
  barsPerChord: number;
  /** 進行をくり返す回数。 */
  repeats: number;
  /** 伴奏の雰囲気（funk・reggae・bossa・jazz（ウォーキングベース）・shuffle・metal・disco・hiphop・trap・dnb・halftime＝ジャンル別のドラムとベース。vocaloid＝ボカロ曲のようなバック（歌なし）: 高速・16分の詰まったドラムとピアノ・動くベース・ギターの刻み・左右の弦。dance＝4つ打ちのキック・メロディのように動くベース・ピアノの分散和音・エコーギターの、きれいで現代的な伴奏）。 */
  feel: NewSongFeel;
  /** ゴーストノート（弱い音）をどれくらい足すか（0〜1）。funk・hiphop などのベースとスネア。省略はジャンルごとの標準。 */
  ghostDensity?: number;
  /** true なら、rock・pop・ballad のベースも、4・8小節目の最後に次のコードの根音へ近づく音（アプローチ）を置く。省略は置かない（従来どおり）。新しいジャンルは常に置く。 */
  approach?: boolean;
  /** 拍子（指定すると beats より優先。例: 7/8）。 */
  sig?: TimeSignature;
  /** 空にしておくメロディのトラックの楽器。 */
  leadInstrument: Instrument;
}

const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const QUALITY: [string, number[]][] = [
  ["maj7", [0, 4, 7, 11]], ["m7", [0, 3, 7, 10]], ["dim", [0, 3, 6]], ["aug", [0, 4, 8]], ["sus4", [0, 5, 7]], ["sus2", [0, 2, 7]],
  ["m", [0, 3, 7]], ["7", [0, 4, 7, 10]], ["", [0, 4, 7]],
  // 2026-10-11 追加: 6・9・add9・m7♭5・7sus4 など（コード進行の幅を広げる）
  ["m7b5", [0, 3, 6, 10]], ["m7(b5)", [0, 3, 6, 10]], ["dim7", [0, 3, 6, 9]], ["7sus4", [0, 5, 7, 10]],
  ["maj9", [0, 4, 7, 11, 2]], ["m9", [0, 3, 7, 10, 2]], ["9", [0, 4, 7, 10, 2]], ["add9", [0, 4, 7, 2]],
  ["m6", [0, 3, 7, 9]], ["6", [0, 4, 7, 9]], ["madd9", [0, 3, 7, 2]], ["m(maj7)", [0, 3, 7, 11]],
  // 2026-10-11 追加（第1弾の積み残し）: パワーコード `5`（根音と5度）、m7-5・m7♭5 の別の書き方、mmaj7・mM7（短七の長7度）、M7
  ["5", [0, 7]], ["m7-5", [0, 3, 6, 10]], ["m7♭5", [0, 3, 6, 10]], ["mmaj7", [0, 3, 7, 11]], ["mM7", [0, 3, 7, 11]], ["M7", [0, 4, 7, 11]],
];

/** "Am"・"F#m7"・"Bb"・"Csus4" のようなコード名を、根音（0〜11）と構成音の間隔にする。読めなければ null。 */
export function parseChord(name: string): { root: number; intervals: number[]; bass?: number } | null {
  // 分数コード（G/B など）: 和音は左側、ベースの音は右側
  const slash = name.trim().split("/");
  if (slash.length > 2) return null;
  const m = /^([A-G])([#b]?)(.*)$/.exec(slash[0]);
  if (!m) return null;
  const root = (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12;
  const q = QUALITY.find(([k]) => k === m[3]);
  if (!q) return null;
  if (slash.length === 2) {
    const b = /^([A-G])([#b]?)$/.exec(slash[1]);
    if (!b) return null;
    return { root, intervals: q[1], bass: (PC[b[1]] + (b[2] === "#" ? 1 : b[2] === "b" ? -1 : 0) + 12) % 12 };
  }
  return { root, intervals: q[1] };
}

const rest = (beats: number): NoteEvent => ({ note: REST, durationBeats: beats });
const note = (midi: number, beats: number, velocity?: number): NoteEvent => ({ note: midiToName(midi), durationBeats: beats, ...(velocity ? { velocity } : {}) });


/**
 * 声部のなめらかな動き（ボイスリーディング）: コードが変わるとき、各声部がなるべく近い音へ動くように、和音の音を選ぶ。
 * 各コードの先頭 voices 個の構成音を、音域 [lo, hi] の中で、前の和音からの移動量の合計がいちばん小さい並べ方で割り当てる。
 * 返り値は小節ごとの、声部ごとの音（MIDI番号）。同じ和音が続けば、同じ音のまま動かない。
 */
export function voiceLead(bars: { root: number; intervals: number[] }[], voices: number, lo = 52, hi = 79): number[][] {
  const result: number[][] = [];
  let prev: number[] | null = null;
  for (const c of bars) {
    const pcs = c.intervals.slice(0, voices).map((iv) => (c.root + iv) % 12);
    while (pcs.length < voices) pcs.push(pcs[pcs.length - 1]);
    // 各構成音の、音域内の候補（オクターブ違い）
    const cands = pcs.map((pc) => { const o: number[] = []; for (let m = lo; m <= hi; m++) if (m % 12 === pc) o.push(m); return o; });
    const targets = prev ?? pcs.map((_, i) => 60 + (i - 1) * 4);
    let best: number[] = [];
    let bestCost = Infinity;
    // 声部 v に構成音 perm[v] を割り当てる全ての並べ替え（最大4!）を試す
    const perms = (arr: number[]): number[][] => (arr.length <= 1 ? [arr] : arr.flatMap((x, i) => perms([...arr.slice(0, i), ...arr.slice(i + 1)]).map((r) => [x, ...r])));
    for (const perm of perms(pcs.map((_, i) => i))) {
      const pick = perm.map((ci, v) => cands[ci].reduce((b, m) => (Math.abs(m - targets[v]) < Math.abs(b - targets[v]) ? m : b), cands[ci][0]));
      if (new Set(pick).size < pick.length) continue;
      const cost = pick.reduce((sum, m, v) => sum + Math.abs(m - targets[v]), 0) + (prev ? 0 : Math.abs(Math.max(...pick) - Math.min(...pick)) * 0.3);
      if (cost < bestCost) { bestCost = cost; best = pick; }
    }
    if (!best.length) best = cands.map((o, v) => o.reduce((b, m) => (Math.abs(m - targets[v]) < Math.abs(b - targets[v]) ? m : b), o[0]));
    result.push(best);
    prev = best;
  }
  return result;
}

export function buildNewSong(spec: NewSongSpec): Score {
  const chords = spec.chords.split(/[\s|]+/).filter(Boolean).map((c) => ({ name: c, chord: parseChord(c) }));
  const bad = chords.find((c) => !c.chord);
  if (chords.length === 0) throw new Error("コード進行を入力してください");
  if (bad) throw new Error(`読めないコードがあります: ${bad.name}`);
  const beats = spec.sig ? barBeats(spec.sig) : Math.max(2, Math.min(12, Math.round(spec.beats)));
  const bars: { root: number; intervals: number[]; bar: number }[] = [];
  for (let r = 0; r < Math.max(1, spec.repeats); r++) {
    for (const c of chords) {
      for (let b = 0; b < Math.max(1, spec.barsPerChord); b++) bars.push({ ...c.chord!, bar: b });
    }
  }
  const make = (fn: (c: { root: number; intervals: number[]; bar: number }, beats: number, index: number) => NoteEvent[]): NoteEvent[] => bars.flatMap((c, i) => fn(c, beats, i));
  const every = (beatsPerBar: number, step: number, pitch: (i: number) => number | null, vel?: (i: number) => number | undefined): NoteEvent[] => {
    const out: NoteEvent[] = [];
    const n = Math.round(beatsPerBar / step);
    for (let i = 0; i < n; i++) {
      const p = pitch(i);
      out.push(p === null ? rest(step) : note(p, step, vel?.(i)));
    }
    return out;
  };
  const tones = (c: { root: number; intervals: number[] }, base: number): number[] => c.intervals.map((iv) => base + ((c.root + iv) % 12));
  const octaveOf = (c: { root: number; bass?: number }, base: number): number => base + (c.bass ?? c.root);
  const ballad = spec.feel === "ballad";
  const rock = spec.feel === "rock";
  const dance = spec.feel === "dance";

  const kickPos = (i: number, step: number): boolean => {
    const at = i * step;
    if (ballad) return at === 0;
    if (dance) return Math.abs(at - Math.round(at)) < 1e-9;
    if (rock) return at === 0 || (beats >= 4 && at === 2) || (beats >= 4 && at === 2.5);
    return at === 0 || (beats >= 4 && at === 2);
  };
  const snarePos = (i: number, step: number): boolean => {
    const at = i * step;
    return beats >= 4 ? at === 1 || at === 3 : beats === 3 ? at === 2 : at === Math.floor(beats / 2);
  };

  if (isGenreFeel(spec.feel)) return genreSong(spec, bars, beats);
  if (spec.feel === "vocaloid") return vocaloidSong(spec, bars, beats, make, every, tones, octaveOf);
  if (dance) return danceSong(spec, bars, beats, make, every, tones, octaveOf, kickPos, snarePos);
  const drums: Track[] = [
    { waveform: "sine", instrument: "kick", volume: 0.3, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (kickPos(i, 0.5) ? 36 : null), () => 112)) },
    { waveform: "square", instrument: "snare", volume: 0.22, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (snarePos(i, 0.5) ? 38 : null), () => 108)) },
    { waveform: "square", instrument: "hihat", volume: 0.12, pan: 0.35, notes: make((_c, b) => every(b, ballad ? 1 : 0.5, () => 42, (i) => (i % 2 === 0 ? 96 : 70))) },
  ];
  const bass: Track = {
    waveform: "sawtooth", instrument: "bass", volume: 0.3, pan: 0,
    notes: make((c, b, index) => {
      const line = ballad ? [note(octaveOf(c, 36), b, 100)] : every(b, 0.5, (i) => (i % 2 === 0 || rock ? octaveOf(c, 36) : null), (i) => (i % 2 === 0 ? 104 : 84));
      // 小節末のアプローチ（spec.approach のときだけ。4・8小節目の最後の8分を、次の根音へ近づく音にする）
      if (!spec.approach || index % 4 !== 3) return line;
      const ap = approachNote(octaveOf(c, 36), octaveOf(bars[(index + 1) % bars.length], 36));
      const head = line.slice(0, -1);
      const last = line[line.length - 1];
      return last.durationBeats > 0.5 ? [...head, { ...last, durationBeats: last.durationBeats - 0.5 }, note(ap, 0.5, 96)] : [...head, note(ap, last.durationBeats, 96)];
    }),
  };
  const guitar: Track = {
    waveform: "sawtooth", instrument: rock ? "crunch" : "guitar", volume: 0.2, pan: -0.4,
    notes: make((c, b) => {
      const t = tones(c, 48);
      return every(b, ballad ? 1 : 0.5, (i) => t[i % t.length], (i) => (i % 2 === 0 ? 96 : 76));
    }),
  };
  const piano: Track = {
    waveform: "triangle", instrument: "piano", volume: 0.16, pan: 0.3,
    notes: make((c, b) => [note(octaveOf(c, 60) + (c.intervals[1] ?? 4), b, 84)]),
  };
  // 弦の3声は、コードが変わるとき近い音へ動く（ボイスリーディング）
  const padVoicing = voiceLead(bars, 3);
  const padVoice = (k: number): Track => ({
    waveform: "sine", instrument: "strings", volume: 0.09, pan: k === 0 ? -0.25 : k === 1 ? 0.25 : 0,
    notes: make((_c, b, index) => [note(padVoicing[index][k], b, 70)]),
  });
  const total = bars.length * beats;
  const lead: Track = { waveform: "square", instrument: spec.leadInstrument, volume: 0.22, pan: 0, notes: [rest(total)] };
  return { tempoBpm: spec.bpm, timeSig: spec.sig ?? { num: beats, den: 4 }, loop: true, drumKit: rock ? 16 : 0, tone: "rock", tracks: [...drums, bass, guitar, piano, padVoice(0), padVoice(1), padVoice(2), lead] };
}

type Bar = { root: number; intervals: number[]; bar: number };
/**
 * 「dance」の伴奏: やわらかい4つ打ち・裏拍のハイハット・バックビート、メロディのように動くベース（根音→5度→オクターブ→10度→次の小節の根音へ向かう音）、
 * ピアノの16分の分散和音（左）、付点8分のエコーギター（右）、左右に広げた弦（docs/sound/reference-nihonichi-bgm.md の目安）。
 */
function danceSong(
  spec: NewSongSpec, bars: Bar[], beats: number,
  make: (fn: (c: Bar, beats: number, index: number) => NoteEvent[]) => NoteEvent[],
  every: (beatsPerBar: number, step: number, pitch: (i: number) => number | null, vel?: (i: number) => number | undefined) => NoteEvent[],
  tones: (c: { root: number; intervals: number[] }, base: number) => number[],
  octaveOf: (c: { root: number }, base: number) => number,
  kickPos: (i: number, step: number) => boolean, snarePos: (i: number, step: number) => boolean,
): Score {
  const fold = (m: number): number => (m > 55 ? m - 12 : m < 28 ? m + 12 : m);
  const drums: Track[] = [
    { waveform: "sine", instrument: "kick", volume: 0.22, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (kickPos(i, 0.5) ? 36 : null), () => 104)) },
    { waveform: "square", instrument: "snare", volume: 0.15, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (snarePos(i, 0.5) ? 38 : null), () => 96)) },
    { waveform: "square", instrument: "hihat", volume: 0.08, pan: 0.3, notes: make((_c, b) => every(b, 0.5, (i) => (i % 2 === 1 ? 46 : null), () => 84)) },
  ];
  const bass: Track = {
    waveform: "triangle", instrument: "bass", volume: 0.18, pan: 0,
    notes: make((c, b, index) => {
      const r = octaveOf(c, 36);
      const third = r + 12 + (c.intervals[1] ?? 4);
      const next = bars[(index + 1) % bars.length];
      const nextRoot = octaveOf(next, 36);
      const approach = nextRoot + (nextRoot > third ? -2 : 2);
      const line = [r, r + 7, r + 12, third, approach].map(fold);
      if (b < 4) return every(b, 1, (i) => line[i % line.length], () => 100);
      const lens = [1, 0.5, 0.5, 1, 1];
      const out: NoteEvent[] = line.map((m, i) => note(m, lens[i], i === 0 ? 104 : 90));
      const extra = b - 4;
      if (extra > 0) out.push(note(r, extra, 90));
      return out;
    }),
  };
  const piano: Track = {
    waveform: "triangle", instrument: "piano", volume: 0.09, pan: -0.6,
    notes: make((c, b) => {
      const t = tones(c, 60);
      const seq = [t[0], t[1], t[2], t[0] + 12, t[2], t[1], t[2], t[0] + 12];
      return every(b, 0.25, (i) => seq[i % seq.length], (i) => (i % 4 === 0 ? 84 : 66));
    }),
  };
  const guitar: Track = {
    waveform: "triangle", instrument: "echoGuitar", volume: 0.08, pan: 0.75,
    notes: make((c, b) => {
      const t = tones(c, 60);
      const up = [t[2], t[1], t[0]];
      const out: NoteEvent[] = [];
      let left = b;
      let k = 0;
      for (const len of [0.75, 0.75, 0.5, 0.75, 0.75, 0.5]) {
        if (left <= 1e-9) break;
        const d = Math.min(len, left);
        out.push(note(up[k++ % 3], d, 80));
        left -= d;
      }
      if (left > 1e-9) out.push(rest(left));
      return out;
    }),
  };
  const padVoicing = voiceLead(bars, 3);
  const strings = (k: number, pan: number): Track => ({
    waveform: "sine", instrument: "strings", volume: 0.09, pan,
    notes: make((_c, b, index) => [note(padVoicing[index][k], b, 70)]),
  });
  const total = bars.length * beats;
  const lead: Track = { waveform: "square", instrument: spec.leadInstrument, volume: 0.22, pan: 0.05, notes: [rest(total)] };
  return { tempoBpm: spec.bpm, timeSig: spec.sig ?? { num: beats, den: 4 }, loop: true, drumKit: 8, tone: "rock", tracks: [...drums, bass, piano, guitar, strings(1, -0.75), strings(2, 0.75), lead] };
}


/**
 * 「vocaloid」の伴奏（歌なしのバック）: 疾走感のある、音の詰まったバンド編成。
 * ドラムは1・3拍目寄りのキックと2・4拍目のスネア、16分のハイハット（強弱つき）、4小節ごとのフィルとクラッシュ。
 * ベースは根音の8分に、オクターブの跳躍と次のコードへ向かう音。ピアノは16分の分散和音（左）、ギターは8分の刻み（右）、左右に広げた弦（背景）。
 * メロディ（歌のパート）は空のトラックとして最後に置く。声（合唱など）は使わない。
 */
function vocaloidSong(
  spec: NewSongSpec, bars: Bar[], beats: number,
  make: (fn: (c: Bar, beats: number, index: number) => NoteEvent[]) => NoteEvent[],
  every: (beatsPerBar: number, step: number, pitch: (i: number) => number | null, vel?: (i: number) => number | undefined) => NoteEvent[],
  tones: (c: { root: number; intervals: number[] }, base: number) => number[],
  octaveOf: (c: { root: number }, base: number) => number,
): Score {
  const fold = (m: number): number => (m > 55 ? m - 12 : m < 28 ? m + 12 : m);
  // 16分のグリッド（1小節16マス。4拍子以外は先頭から数える）
  const KICK_A = "x.x...x.x.x.....";
  const KICK_B = "x.....x.x.x...x.";
  const hit = (pat: string, i: number): boolean => pat[i % 16] === "x";
  const fillBar = (index: number): boolean => index % 4 === 3;
  const kick: Track = {
    waveform: "sine", instrument: "kick", volume: 0.24, pan: 0,
    notes: make((_c, b, index) => every(b, 0.25, (i) => (hit(index % 2 === 0 ? KICK_A : KICK_B, i) ? 36 : null), (i) => (i % 16 === 0 ? 118 : 104))),
  };
  const snare: Track = {
    waveform: "square", instrument: "snare", volume: 0.17, pan: 0,
    notes: make((_c, b, index) => every(b, 0.25, (i) => {
      const at = (i % 16) * 0.25;
      // 4小節目の最後の1拍は、スネアの16分のフィル（だんだん強く）
      if (fillBar(index) && beats >= 4 && at >= beats - 1) return 38;
      return beats >= 4 ? (at === 1 || at === 3 ? 38 : null) : at === Math.floor(beats / 2) ? 38 : null;
    }, (i) => {
      const at = (i % 16) * 0.25;
      return fillBar(index) && beats >= 4 && at >= beats - 1 ? 84 + Math.round((at - (beats - 1)) * 40) : 110;
    })),
  };
  const hihat: Track = {
    waveform: "square", instrument: "hihat", volume: 0.07, pan: 0.3,
    notes: make((_c, b) => every(b, 0.25, () => 42, (i) => (i % 4 === 0 ? 100 : i % 2 === 0 ? 78 : 56))),
  };
  const crash: Track = {
    waveform: "square", instrument: "crash", volume: 0.08, pan: -0.3,
    notes: make((_c, b, index) => (index % 4 === 0 ? [note(49, Math.min(b, 4), 110), ...(b > 4 ? [rest(b - 4)] : [])] : [rest(b)])),
  };
  const bass: Track = {
    waveform: "sawtooth", instrument: "bass", volume: 0.19, pan: 0,
    notes: make((c, b, index) => {
      const r = fold(octaveOf(c, 36));
      const next = bars[(index + 1) % bars.length];
      const nextRoot = fold(octaveOf(next, 36));
      const approach = nextRoot + (nextRoot > r ? -1 : nextRoot < r ? 1 : 2);
      // 2026-10-11: オクターブ上の音が音域（E1〜G3）をこえないように収める（根音が G♯2 以上のとき、以前は A3 などに上がっていた）
      const line = [r, r, r + 12, r, r + 7, r, r + 12, approach].map((m) => foldInto(m, BASS_LO, BASS_HI));
      return every(b, 0.5, (i) => line[i % line.length], (i) => (i % 2 === 0 ? 104 : 88));
    }),
  };
  const piano: Track = {
    waveform: "triangle", instrument: "piano", volume: 0.1, pan: -0.55,
    notes: make((c, b) => {
      const t = tones(c, 60);
      const seq = [t[0], t[2], t[1], t[2], t[0] + 12, t[2], t[1], t[2], t[0], t[2], t[1], t[2], t[0] + 12, t[1] + 12, t[0] + 12, t[2]];
      return every(b, 0.25, (i) => seq[i % seq.length], (i) => (i % 4 === 0 ? 90 : 68));
    }),
  };
  const guitar: Track = {
    waveform: "sawtooth", instrument: "crunch", volume: 0.08, pan: 0.75,
    notes: make((c, b) => {
      const root = fold(octaveOf(c, 48)) < 40 ? fold(octaveOf(c, 48)) + 12 : fold(octaveOf(c, 48));
      return every(b, 0.5, () => root, (i) => (i % 2 === 0 ? 98 : 76));
    }),
  };
  const padVoicing = voiceLead(bars, 3);
  const strings = (k: number, pan: number): Track => ({
    waveform: "sine", instrument: "strings", volume: 0.09, pan,
    notes: make((_c, b, index) => [note(padVoicing[index][k], b, 70)]),
  });
  const total = bars.length * beats;
  const lead: Track = { waveform: "square", instrument: spec.leadInstrument, volume: 0.22, pan: 0, notes: [rest(total)] };
  return { tempoBpm: spec.bpm, timeSig: spec.sig ?? { num: beats, den: 4 }, loop: true, drumKit: 8, tone: "rock", tracks: [kick, snare, hihat, crash, bass, piano, guitar, strings(1, -0.8), strings(2, 0.8), lead] };
}

// ───────────────────────── ジャンル別の自動伴奏（2026-10-11） ─────────────────────────
// docs/sound/bassline-guide.md §3・§8、docs/sound/drum-genre-guide.md §2・§7 を、16分の格子（セル）で書いたもの。
// 1小節＝beats×4 セル。格子は16文字の型を `i % 16` でくり返す（4拍子以外は先頭から数える）。

/** 次のコードの根音へ近づく音（アプローチ）: 次の根音が高ければ半音下から、低ければ半音上から、同じなら半音下から。全 feel 共通。 */
export function approachNote(current: number, next: number): number {
  return next > current ? next - 1 : next < current ? next + 1 : next - 1;
}

/** 音を音域 [lo, hi] に収める（オクターブ単位）。 */
export function foldInto(m: number, lo: number, hi: number): number {
  let x = m;
  while (x > hi) x -= 12;
  while (x < lo) x += 12;
  return x;
}
export const BASS_LO = 28; // E1
export const BASS_HI = 55; // G3
export const SUB808_LO = 24; // C1
export const SUB808_HI = 48; // C3

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
 * キックの格子からベースの格子を作る（bassline-guide §8 の 3）。
 * キックのあるマスにはキック用の音（既定は根音 r）、ないマスには filler の音を置く。
 * ベースの記号: r 根音(強) q 根音(弱) o ゴースト(弱く短く) O オクターブ 5 5度(上) d 5度(下) 3 3度 6 6度 7 ♭7 a アプローチ - 休み . 前の音を伸ばす
 */
export function bassFromKick(kick: string, filler: string, kickToken: (cell: number) => string = () => "r"): string {
  const out: string[] = [];
  const n = Math.max(kick.length, filler.length);
  for (let i = 0; i < n; i++) {
    const k = kick[i % kick.length];
    out.push(k !== "." && k !== undefined && k !== "o" ? kickToken(i) : (filler[i % filler.length] ?? "."));
  }
  return out.join("");
}

interface GenreCfg {
  kick: string[]; snare: string[]; hat: string[];
  /** バックビートのゴーストを足す標準の確率（なければ足さない）。 */
  ghostSnare?: number;
  fill?: boolean; crash?: boolean;
  drumKit: number; drumVol: { kick: number; snare: number; hat: number };
  bass: { inst: "bass" | "sub808"; vol: number; filler: string[]; kickSync: boolean; kickToken?: (cell: number) => string; own?: string[]; ghost?: number; approach: boolean; baseOctave: number; wave: "sawtooth" | "triangle" | "sine" };
  comps: { inst: Instrument; vol: number; pan: number; tpl: string[]; base: number; vel: [number, number]; gate?: number }[];
  pad: number;
  swing?: number;
  tone?: Score["tone"];
}

const WALK_A = "r...3...5...a...";
const WALK_B = "r...5...3...a...";

const CFG: Record<(typeof GENRE_FEELS)[number], GenreCfg> = {
  funk: {
    kick: ["X.x.......x.....", "X.x.....x.x.....", "X.x.......x...x.", "X.x.....x.x.x..."],
    snare: ["....X.......X...", "....X.......X...", "....X.......X..o", "....X.......X..."],
    hat: ["xoxoxoxoxoxoxoxo", "xoxoxoxoxoxoxOxo", "xoxoxoxoxoxoxoxo", "xoxoxoxoxoxoxoxO"],
    ghostSnare: 0.6, fill: true, crash: false, drumKit: 0, drumVol: { kick: 0.28, snare: 0.2, hat: 0.1 },
    bass: { inst: "bass", vol: 0.3, wave: "sawtooth", kickSync: true, filler: ["..o.O.o...o.5.o.", "..o.O.o.o...5.o.", "o.o.O...o.o.5.o.", "..o.O.o...o.5.o."], ghost: 0.8, approach: true, baseOctave: 36 },
    comps: [
      { inst: "guitar", vol: 0.14, pan: -0.45, tpl: ["0--0-0--0--0-0--"], base: 55, vel: [92, 62], gate: 0.4 },
      { inst: "piano", vol: 0.12, pan: 0.4, tpl: ["--1.--1.--2.--1-"], base: 60, vel: [86, 70], gate: 0.5 },
    ],
    pad: 0.07, swing: 0.2,
  },
  reggae: {
    kick: ["........X......."], snare: ["........X......."], hat: ["x.x.x.X.x.x.x.X."],
    drumKit: 0, drumVol: { kick: 0.24, snare: 0.2, hat: 0.09 },
    bass: { inst: "bass", vol: 0.3, wave: "triangle", kickSync: true, filler: ["....q.q.....5...", "....q.q.....5...", "....q.q.....5...", "....q.q.3...5.a."], approach: true, baseOctave: 36 },
    comps: [
      { inst: "guitar", vol: 0.13, pan: -0.5, tpl: ["--0.--0.--0.--0."], base: 55, vel: [90, 74], gate: 0.3 },
      { inst: "keys", vol: 0.1, pan: 0.45, tpl: ["--2.--1.--2.--1."], base: 60, vel: [80, 64], gate: 0.45 },
    ],
    pad: 0.06, swing: 0.1,
  },
  bossa: {
    kick: ["x.....x.x.....x."], snare: ["x.....x.....x...", "....x.....x....."], hat: ["x.x.x.x.x.x.x.x."],
    drumKit: 0, drumVol: { kick: 0.18, snare: 0.1, hat: 0.07 },
    bass: { inst: "bass", vol: 0.28, wave: "triangle", kickSync: true, kickToken: (c) => (c % 8 === 0 ? "r" : "d"), filler: ["................"], approach: true, baseOctave: 36 },
    comps: [
      { inst: "guitar", vol: 0.15, pan: -0.35, tpl: ["1--1--1---1--1--", "2--2--2---1--2--"], base: 55, vel: [84, 66], gate: 0.6 },
      { inst: "piano", vol: 0.1, pan: 0.4, tpl: ["2...............", "........1......."], base: 62, vel: [78, 64], gate: 1 },
    ],
    pad: 0.06, swing: 0.15,
  },
  jazz: {
    kick: ["o...o...o...o..."], snare: ["..o.....o.o.....", "..o.......o.o...", "..o.....o......."], hat: ["x...x.x.x...x.x."],
    ghostSnare: 0, drumKit: 0, drumVol: { kick: 0.12, snare: 0.1, hat: 0.1 },
    bass: { inst: "bass", vol: 0.3, wave: "triangle", kickSync: false, own: [WALK_A, WALK_B], filler: [], approach: true, baseOctave: 36 },
    comps: [
      { inst: "piano", vol: 0.14, pan: 0.35, tpl: ["--1---1.--------", "-.2---------1-2-"], base: 60, vel: [86, 68], gate: 0.7 },
    ],
    pad: 0.05, swing: 0.6,
  },
  shuffle: {
    kick: ["X.......X.......", "X.......X.x....."], snare: ["....X.......X..."], hat: ["x.x.x.x.x.x.x.x."],
    fill: true, crash: false, drumKit: 0, drumVol: { kick: 0.28, snare: 0.2, hat: 0.11 },
    bass: { inst: "bass", vol: 0.3, wave: "sawtooth", kickSync: false, own: ["r.3.5.6.7.6.5.3."], filler: [], approach: true, baseOctave: 36 },
    comps: [
      { inst: "crunch", vol: 0.14, pan: -0.4, tpl: ["0.0.1.0.0.0.1.0."], base: 52, vel: [92, 72], gate: 0.7 },
      { inst: "piano", vol: 0.12, pan: 0.35, tpl: ["--2.--2.--2.--2."], base: 60, vel: [84, 66], gate: 0.5 },
    ],
    pad: 0.07, swing: 0.6,
  },
  metal: {
    kick: ["XxXxXxXxXxXxXxXx", "XxXxXxXxXxXxXxXx", "X.xxX.xxX.xxX.xx", "XxXxXxXxXxXxXxXx"],
    snare: ["....X.......X..."], hat: ["x.x.x.x.x.x.x.x."],
    fill: true, crash: true, drumKit: 16, drumVol: { kick: 0.3, snare: 0.22, hat: 0.1 },
    bass: { inst: "bass", vol: 0.28, wave: "sawtooth", kickSync: true, filler: ["................"], approach: false, baseOctave: 36 },
    comps: [
      { inst: "distGuitar", vol: 0.09, pan: -0.8, tpl: ["0"], base: 40, vel: [100, 84], gate: 0.6 },
      { inst: "distGuitar", vol: 0.09, pan: 0.8, tpl: ["0"], base: 40, vel: [100, 84], gate: 0.6 },
    ],
    pad: 0.1, tone: "metal",
  },
  disco: {
    kick: ["X...X...X...X..."], snare: ["....X.......X..."], hat: ["x.O.x.O.x.O.x.O."],
    fill: true, crash: true, drumKit: 8, drumVol: { kick: 0.24, snare: 0.17, hat: 0.09 },
    bass: { inst: "bass", vol: 0.28, wave: "triangle", kickSync: false, own: ["r.O.r.O.r.O.r.O.", "r.O.r.O.r.O.r.5."], filler: [], approach: true, baseOctave: 36 },
    comps: [
      { inst: "guitar", vol: 0.12, pan: -0.5, tpl: ["0-0-0-0-0-0-0-0-"], base: 55, vel: [90, 70], gate: 0.4 },
      { inst: "piano", vol: 0.1, pan: 0.45, tpl: ["--1---1---1---1-"], base: 62, vel: [82, 66], gate: 0.5 },
    ],
    pad: 0.09,
  },
  hiphop: {
    kick: ["X..o......x.....", "X..o......x...o.", "X.......o.x.....", "X..o....o.x....."],
    snare: ["....X.......X..."], hat: ["x.x.x.x.x.x.x.x."],
    ghostSnare: 0.35, drumKit: 0, drumVol: { kick: 0.3, snare: 0.2, hat: 0.09 },
    bass: { inst: "bass", vol: 0.3, wave: "sine", kickSync: true, filler: ["................", "............5...", "................", "..............O."], approach: false, baseOctave: 36 },
    comps: [
      { inst: "piano", vol: 0.12, pan: 0.3, tpl: ["0.....1.....2...", "0.......1.....2."], base: 62, vel: [80, 66], gate: 1.2 },
      { inst: "bell", vol: 0.05, pan: -0.4, tpl: ["--------2-------"], base: 72, vel: [70, 60], gate: 1.5 },
    ],
    pad: 0.07, swing: 0.4,
  },
  trap: {
    kick: ["X.....x.....x...", "X.....x.......x.", "X.x...x.....x..."],
    snare: ["........X......."], hat: ["x.x.x.x.x.x.x.x.", "x.x.x.x.xxx.x.x.", "x.xxx.x.x.x.x.x."],
    drumKit: 0, drumVol: { kick: 0.24, snare: 0.18, hat: 0.1 },
    bass: { inst: "sub808", vol: 0.26, wave: "sine", kickSync: true, filler: ["................"], approach: false, baseOctave: 24 },
    comps: [
      { inst: "bell", vol: 0.07, pan: 0.35, tpl: ["0---2---1---2---"], base: 72, vel: [76, 62], gate: 1.5 },
    ],
    pad: 0.08, swing: 0,
  },
  dnb: {
    kick: ["X.........x.....", "X.........x...x.", "X.......x.x....."],
    snare: ["....X.......X..."], hat: ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.xox."],
    ghostSnare: 0.3, fill: true, crash: true, drumKit: 8, drumVol: { kick: 0.24, snare: 0.19, hat: 0.09 },
    bass: { inst: "bass", vol: 0.3, wave: "sawtooth", kickSync: true, filler: ["................", "......5.........", "................", "..............5."], approach: true, baseOctave: 36 },
    comps: [
      { inst: "keys", vol: 0.09, pan: 0.35, tpl: ["--1-----------1-"], base: 62, vel: [80, 64], gate: 1 },
    ],
    pad: 0.09,
  },
  halftime: {
    kick: ["X.........x.....", "X.........x...x."],
    snare: ["........X......."], hat: ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.x.xxxx"],
    drumKit: 8, drumVol: { kick: 0.26, snare: 0.2, hat: 0.08 },
    bass: { inst: "sub808", vol: 0.28, wave: "sine", kickSync: true, filler: ["................"], approach: false, baseOctave: 24 },
    comps: [
      { inst: "keys", vol: 0.08, pan: 0.3, tpl: ["0.......2......."], base: 62, vel: [78, 64], gate: 1.5 },
    ],
    pad: 0.1, swing: 0,
  },
};

/** ジャンルごとの feel で、既定の swing（曲に swing の指定がないときに使う）。 */
export const FEEL_SWING: Partial<Record<NewSongFeel, number>> = Object.fromEntries(
  GENRE_FEELS.filter((f) => (CFG as Record<string, GenreCfg>)[f]?.swing).map((f) => [f, (CFG as Record<string, GenreCfg>)[f].swing]),
);

/** 速いテンポで16分の連打が詰まるのを避ける（8分に落とす）。 */
const thin = (grid: string, bpm: number, limit: number): string => (bpm <= limit ? grid : [...grid].map((c, i) => (i % 2 === 0 ? c : ".")).join(""));

function genreSong(spec: NewSongSpec, bars: Bar[], beats: number): Score {
  const feel = spec.feel as (typeof GENRE_FEELS)[number];
  const cfg = CFG[feel];
  const octaveOf = (c: { root: number; bass?: number }, base: number): number => base + (c.bass ?? c.root);
  const tones = (c: { root: number; intervals: number[] }, base: number): number[] => c.intervals.map((iv) => base + ((c.root + iv) % 12));
  const cells = Math.round(beats * 4);
  const bpm = spec.bpm;
  const ghostDensity = Math.max(0, Math.min(1, spec.ghostDensity ?? cfg.ghostSnare ?? 0));
  const bassGhost = Math.max(0, Math.min(1, spec.ghostDensity ?? cfg.bass.ghost ?? 0));
  const velOf = (c: string, kind: "kick" | "snare" | "hat"): number | null => {
    if (c === ".") return null;
    if (c === "X") return kind === "kick" ? 118 : kind === "snare" ? 112 : 100;
    if (c === "o") return kind === "kick" ? 62 : kind === "snare" ? 46 : 56;
    return kind === "kick" ? 104 : kind === "snare" ? 100 : 78; // x と O
  };
  const kickGrid = (bar: number): string => {
    const g = cfg.kick[bar % cfg.kick.length];
    return feel === "metal" ? thin(g, bpm, 190) : g;
  };
  const snareGrid = (bar: number): string => {
    const g = cfg.snare[bar % cfg.snare.length];
    return ghostDensity > 0 ? placeGhosts(g, kickGrid(bar), ghostDensity, bar, bpm) : g;
  };
  const hatGrid = (bar: number): string => cfg.hat[bar % cfg.hat.length];
  const fillBar = (bar: number): boolean => !!cfg.fill && bar % 4 === 3 && beats >= 4;

  /** 格子の文字列を、16分ごとの NoteEvent にする（セルごとに1つ。休みは休符）。 */
  const drumTrack = (instrument: "kick" | "snare" | "hihat", kind: "kick" | "snare" | "hat", pitch: number, grid: (bar: number) => string, volume: number, pan: number, wave: "sine" | "square"): Track => ({
    waveform: wave, instrument, volume, pan,
    notes: bars.flatMap((_c, bar) => {
      const g = grid(bar);
      const out: NoteEvent[] = [];
      for (let i = 0; i < cells; i++) {
        const ch = g[i % g.length];
        const at = i * 0.25;
        // 小節末の1拍はスネアのフィル（だんだん強く）
        if (kind === "snare" && fillBar(bar) && at >= beats - 1) { out.push(note(pitch, 0.25, 84 + Math.round((at - (beats - 1)) * 40))); continue; }
        const v = velOf(ch, kind);
        out.push(v === null ? rest(0.25) : note(kind === "hat" && ch === "O" ? 46 : pitch, 0.25, v));
      }
      return out;
    }),
  });
  const drums: Track[] = [
    drumTrack("kick", "kick", 36, kickGrid, cfg.drumVol.kick, 0, "sine"),
    drumTrack("snare", "snare", 38, snareGrid, cfg.drumVol.snare, 0, "square"),
    drumTrack("hihat", "hat", 42, hatGrid, cfg.drumVol.hat, 0.3, "square"),
  ];
  if (cfg.crash) {
    drums.push({ waveform: "square", instrument: "crash", volume: 0.08, pan: -0.3, notes: bars.flatMap((_c, bar) => (bar % 4 === 0 ? [note(49, Math.min(beats, 4), 110), ...(beats > 4 ? [rest(beats - 4)] : [])] : [rest(beats)])) });
  }

  // ── ベース ──
  const bcfg = cfg.bass;
  const [lo, hi] = bcfg.inst === "sub808" ? [SUB808_LO, SUB808_HI] : [BASS_LO, BASS_HI];
  const rootOf = (c: Bar): number => foldInto(octaveOf(c, bcfg.baseOctave), lo, hi);
  const bassTrack: Track = {
    waveform: bcfg.wave, instrument: bcfg.inst, volume: bcfg.vol, pan: 0,
    notes: bars.flatMap((c, bar) => {
      const rnd = seeded(bar * 7 + 3);
      const kg = kickGrid(bar);
      let tpl = bcfg.kickSync
        ? bassFromKick(kg, bcfg.filler[bar % bcfg.filler.length], bcfg.kickToken)
        : (bcfg.own ?? [])[bar % (bcfg.own?.length ?? 1)] ?? "r...............";
      // 長い音のジャンルは、キックの数だけ根音を置く。速いテンポで16分の根音が詰まるときは8分に落とす
      if (feel === "metal") tpl = thin(tpl, bpm, 190);
      const arr = [...tpl.padEnd(cells, ".")];
      // 小節末のアプローチ（4・8小節目。全ジャンル共通。bass の approach が false のジャンルは置かない）
      if (bcfg.approach && bar % 4 === 3 && cells >= 8) {
        if (feel === "jazz") { /* ウォーキングは4拍目に既にある */ } else { arr[cells - 2] = "a"; arr[cells - 1] = "."; }
      }
      const next = bars[(bar + 1) % bars.length];
      const r = rootOf(c);
      const nextRoot = rootOf(next);
      const third = c.intervals[1] ?? 4;
      const fifth = c.intervals[2] ?? 7;
      let prevMidi = -1;
      const resolveRaw = (tok: string): { midi: number; vel: number; gate?: number } | null => {
        switch (tok) {
          case "r": return { midi: r, vel: 106 };
          case "q": return { midi: r, vel: 92 };
          case "o": return rnd() < bassGhost ? { midi: r, vel: 50, gate: 0.45 } : null;
          case "O": return { midi: foldInto(r + 12, lo, hi), vel: 92, gate: 0.7 };
          case "5": return { midi: foldInto(r + fifth, lo, hi), vel: 90 };
          case "d": return { midi: foldInto(r + fifth - 12, lo, hi), vel: 88, gate: 0.6 };
          case "3": return { midi: foldInto(r + third, lo, hi), vel: 90 };
          case "6": return { midi: foldInto(r + 9, lo, hi), vel: 88 };
          case "7": return { midi: foldInto(r + 10, lo, hi), vel: 86 };
          case "a": {
            // 直前の音と同じ高さになるときは、反対側（半音上／下）から近づく
            let m = foldInto(approachNote(r, nextRoot), lo, hi);
            if (m === prevMidi) m = foldInto(m === nextRoot - 1 ? nextRoot + 1 : nextRoot - 1, lo, hi);
            return { midi: m, vel: 96, gate: 0.8 };
          }
          default: return null;
        }
      };
      const resolve = (tok: string): { midi: number; vel: number; gate?: number } | null => {
        const out = resolveRaw(tok);
        if (out) prevMidi = out.midi;
        return out;
      };
      return cellEvents(arr.slice(0, cells).join(""), resolve);
    }),
  };

  // ── 和音・コード楽器（セルの文字: 数字＝コードの何番目の音か、- 休み、. 伸ばす） ──
  const compTrack = (k: (typeof cfg.comps)[number], idx: number): Track => ({
    waveform: "triangle", instrument: k.inst, volume: k.vol, pan: k.pan,
    notes: bars.flatMap((c, bar) => {
      const t = tones(c, k.base);
      const tpl = k.tpl[bar % k.tpl.length];
      const arr = [...tpl.padEnd(cells, "-")].slice(0, cells).join("");
      void idx;
      return cellEvents(arr, (tok) => {
        if (!/[0-9]/.test(tok)) return null;
        const m = t[Number(tok) % t.length];
        return { midi: feel === "metal" ? foldInto(m, 40, 52) : m, vel: bar % 2 === 0 ? k.vel[0] : k.vel[1], gate: k.gate };
      }, true);
    }),
  });

  // metal はコードの根音をベースの動きに合わせて刻む（ギターは kick に合わせた8分／16分）
  const comps = cfg.comps.map((k, i) => {
    if (feel !== "metal") return compTrack(k, i);
    const tr = compTrack({ ...k, tpl: ["0"] }, i);
    return { ...tr, notes: bars.flatMap((c, bar) => {
      const t = tones(c, k.base);
      const kg = thin(kickGrid(bar), bpm, 190);
      const arr = [...kg.padEnd(cells, ".")].slice(0, cells).map((ch, ci) => (ch === "." ? (ci % 2 === 0 ? "0" : "-") : "0"));
      arr[0] = "0";
      return cellEvents(arr.join(""), (tok) => (tok === "0" ? { midi: foldInto(t[0], 40, 52), vel: bar % 2 === 0 ? 100 : 92, gate: 0.6 } : null), true);
    }) };
  });

  const padVoicing = voiceLead(bars, 3);
  const padVoice = (k: number): Track => ({
    waveform: "sine", instrument: "strings", volume: cfg.pad, pan: k === 0 ? -0.25 : k === 1 ? 0.25 : 0,
    notes: bars.map((_c, index) => note(padVoicing[index][k], beats, 68)),
  });
  const total = bars.length * beats;
  const lead: Track = { waveform: "square", instrument: spec.leadInstrument, volume: 0.22, pan: 0, notes: [rest(total)] };
  const swing = FEEL_SWING[feel];
  return {
    tempoBpm: spec.bpm, timeSig: spec.sig ?? { num: beats, den: 4 }, loop: true, drumKit: cfg.drumKit, tone: cfg.tone ?? "rock",
    ...(swing ? { swing } : {}),
    tracks: [...drums, bassTrack, ...comps, padVoice(0), padVoice(1), padVoice(2), lead],
  };
}

/** セルの文字列（1文字＝16分）を NoteEvent の並びにする。'.' は前の音（または休み）を伸ばす。restDash=true なら '-' は休符。 */
function cellEvents(cellStr: string, resolve: (tok: string) => { midi: number; vel: number; gate?: number } | null, _restDash = false): NoteEvent[] {
  const out: NoteEvent[] = [];
  let i = 0;
  const n = cellStr.length;
  while (i < n) {
    let j = i + 1;
    while (j < n && cellStr[j] === ".") j++;
    const tok = cellStr[i] === "." ? "-" : cellStr[i];
    const dur = (j - i) * 0.25;
    const r = resolve(tok);
    if (!r) {
      const last = out[out.length - 1];
      if (last && last.note === REST) last.durationBeats += dur; else out.push(rest(dur));
    } else {
      out.push({ ...note(r.midi, dur, r.vel), ...(r.gate ? { gate: r.gate } : {}) });
    }
    i = j;
  }
  return out;
}
