import { midiToName } from "./compose";
import { REST, type Instrument, type NoteEvent, type Score, type Track } from "./score";
import { barBeats, type TimeSignature } from "./time-signature";

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
  /** 伴奏の雰囲気（dance＝4つ打ちのキック・メロディのように動くベース・ピアノの分散和音・エコーギターの、きれいで現代的な伴奏）。 */
  feel: "rock" | "ballad" | "pop" | "dance";
  /** 拍子（指定すると beats より優先。例: 7/8）。 */
  sig?: TimeSignature;
  /** 空にしておくメロディのトラックの楽器。 */
  leadInstrument: Instrument;
}

const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const QUALITY: [string, number[]][] = [
  ["maj7", [0, 4, 7, 11]], ["m7", [0, 3, 7, 10]], ["dim", [0, 3, 6]], ["aug", [0, 4, 8]], ["sus4", [0, 5, 7]], ["sus2", [0, 2, 7]],
  ["m", [0, 3, 7]], ["7", [0, 4, 7, 10]], ["", [0, 4, 7]],
];

/** "Am"・"F#m7"・"Bb"・"Csus4" のようなコード名を、根音（0〜11）と構成音の間隔にする。読めなければ null。 */
export function parseChord(name: string): { root: number; intervals: number[] } | null {
  const m = /^([A-G])([#b]?)(.*)$/.exec(name.trim());
  if (!m) return null;
  const root = (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12;
  const q = QUALITY.find(([k]) => k === m[3]);
  return q ? { root, intervals: q[1] } : null;
}

const rest = (beats: number): NoteEvent => ({ note: REST, durationBeats: beats });
const note = (midi: number, beats: number, velocity?: number): NoteEvent => ({ note: midiToName(midi), durationBeats: beats, ...(velocity ? { velocity } : {}) });

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
  const octaveOf = (c: { root: number }, base: number): number => base + c.root;
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

  if (dance) return danceSong(spec, bars, beats, make, every, tones, octaveOf, kickPos, snarePos);
  const drums: Track[] = [
    { waveform: "sine", instrument: "kick", volume: 0.3, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (kickPos(i, 0.5) ? 36 : null), () => 112)) },
    { waveform: "square", instrument: "snare", volume: 0.22, pan: 0, notes: make((_c, b) => every(b, 0.5, (i) => (snarePos(i, 0.5) ? 38 : null), () => 108)) },
    { waveform: "square", instrument: "hihat", volume: 0.12, pan: 0.35, notes: make((_c, b) => every(b, ballad ? 1 : 0.5, () => 42, (i) => (i % 2 === 0 ? 96 : 70))) },
  ];
  const bass: Track = {
    waveform: "sawtooth", instrument: "bass", volume: 0.3, pan: 0,
    notes: make((c, b) => (ballad ? [note(octaveOf(c, 36), b, 100)] : every(b, 0.5, (i) => (i % 2 === 0 || rock ? octaveOf(c, 36) : null), (i) => (i % 2 === 0 ? 104 : 84)))),
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
  const padVoice = (k: number): Track => ({
    waveform: "sine", instrument: "strings", volume: 0.09, pan: k === 0 ? -0.25 : k === 1 ? 0.25 : 0,
    notes: make((c, b) => [note(48 + ((c.root + (c.intervals[k] ?? c.intervals[0])) % 12) + 12, b, 70)]),
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
  const strings = (k: number, pan: number): Track => ({
    waveform: "sine", instrument: "strings", volume: 0.09, pan,
    notes: make((c, b) => [note(48 + ((c.root + (c.intervals[k] ?? c.intervals[0])) % 12) + 12, b, 70)]),
  });
  const total = bars.length * beats;
  const lead: Track = { waveform: "square", instrument: spec.leadInstrument, volume: 0.22, pan: 0.05, notes: [rest(total)] };
  return { tempoBpm: spec.bpm, timeSig: spec.sig ?? { num: beats, den: 4 }, loop: true, drumKit: 8, tone: "rock", tracks: [...drums, bass, piano, guitar, strings(1, -0.75), strings(2, 0.75), lead] };
}
