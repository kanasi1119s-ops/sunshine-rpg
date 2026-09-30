import { midiToName } from "./compose";
import { GM_PROGRAM, USED_GM_PROGRAMS } from "./gm-map";
import { REST, type Instrument, type NoteEvent, type Score, type Track } from "./score";
import { barBeats, DENOMINATORS, type TimeSignature } from "./time-signature";

/**
 * 標準MIDIファイル（.mid）を読み込んで、作曲ソフトの曲（Score）にする。
 * 1つのトラックは1度に1音しか鳴らせないので、和音は、同じ楽器の複数のトラックに分ける。
 */
interface RawNote {
  ch: number;
  pitch: number;
  start: number;
  end: number;
  vel: number;
  program: number;
}

export interface MidiImportResult {
  score: Score;
  /** 読み込んだ音の数・トラックの数・注意。 */
  notes: number;
  warnings: string[];
}

const MAX_TRACKS = 48;
/** 位置と長さを、この細かさ（1拍の1/48）にそろえる。 */
const STEP = 1 / 48;

function readVlq(d: Uint8Array, at: number): [number, number] {
  let v = 0;
  for (let i = 0; i < 4; i++) {
    const b = d[at++];
    v = (v << 7) | (b & 0x7f);
    if (!(b & 0x80)) break;
  }
  return [v, at];
}

export function midiToScore(bytes: Uint8Array): MidiImportResult {
  const d = bytes;
  const str = (at: number, n: number): string => String.fromCharCode(...d.slice(at, at + n));
  const u32 = (at: number): number => (d[at] << 24) | (d[at + 1] << 16) | (d[at + 2] << 8) | d[at + 3];
  const u16 = (at: number): number => (d[at] << 8) | d[at + 1];
  if (d.length < 14 || str(0, 4) !== "MThd") throw new Error("MIDIファイルではありません");
  const ntrks = u16(10);
  const division = u16(12);
  if (division & 0x8000) throw new Error("この種類のMIDI（SMPTEの時間）には対応していません");
  const ppq = division;
  let at = 8 + u32(4);
  const notes: RawNote[] = [];
  let tempo = 0;
  let sig: TimeSignature | null = null;
  const warnings: string[] = [];
  for (let t = 0; t < ntrks && at + 8 <= d.length; t++) {
    if (str(at, 4) !== "MTrk") throw new Error("MIDIファイルが壊れています（トラックの見出し）");
    const len = u32(at + 4);
    let p = at + 8;
    const end = Math.min(d.length, p + len);
    at = p + len;
    let tick = 0;
    let status = 0;
    const programs = new Array(16).fill(0);
    const open = new Map<number, { start: number; vel: number; program: number }[]>();
    while (p < end) {
      let delta;
      [delta, p] = readVlq(d, p);
      tick += delta;
      let b = d[p];
      if (b & 0x80) {
        status = b;
        p++;
      } else if (status < 0x80) {
        throw new Error("MIDIファイルが壊れています（イベント）");
      }
      b = status;
      if (b === 0xff) {
        const type = d[p++];
        let n;
        [n, p] = readVlq(d, p);
        if (type === 0x51 && n === 3 && !tempo) tempo = 60_000_000 / ((d[p] << 16) | (d[p + 1] << 8) | d[p + 2]);
        if (type === 0x58 && n >= 2 && !sig) sig = { num: d[p], den: 2 ** d[p + 1] };
        p += n;
        status = 0;
      } else if (b === 0xf0 || b === 0xf7) {
        let n;
        [n, p] = readVlq(d, p);
        p += n;
        status = 0;
      } else {
        const kind = b & 0xf0;
        const ch = b & 0x0f;
        const a1 = d[p];
        const a2 = kind === 0xc0 || kind === 0xd0 ? 0 : d[p + 1];
        p += kind === 0xc0 || kind === 0xd0 ? 1 : 2;
        const key = ch * 128 + a1;
        if (kind === 0xc0) programs[ch] = a1;
        else if (kind === 0x90 && a2 > 0) {
          const list = open.get(key) ?? [];
          list.push({ start: tick, vel: a2, program: programs[ch] });
          open.set(key, list);
        } else if (kind === 0x80 || (kind === 0x90 && a2 === 0)) {
          const on = open.get(key)?.shift();
          if (on && tick > on.start) notes.push({ ch, pitch: a1, start: on.start / ppq, end: tick / ppq, vel: on.vel, program: on.program });
        }
      }
    }
    // 離されないままの音は、そのトラックの終わりで切る
    for (const [key, list] of open) for (const on of list) if (tick > on.start) notes.push({ ch: key >> 7, pitch: key & 127, start: on.start / ppq, end: tick / ppq, vel: on.vel, program: on.program });
  }
  if (notes.length === 0) throw new Error("音が1つもありません");

  const snap = (x: number): number => Math.round(x / STEP) * STEP;
  const timeSig = sig && sig.num >= 1 && sig.num <= 32 && DENOMINATORS.includes(sig.den) ? sig : { num: 4, den: 4 };
  const lastEnd = Math.max(...notes.map((n) => snap(n.end)));
  const bar = barBeats(timeSig);
  const total = Math.max(bar, Math.ceil(lastEnd / bar - 1e-6) * bar);

  // 楽器（とドラムの種類）ごとに分け、重なる音は別の声部（トラック）へ
  const groups = new Map<string, { instrument: Instrument; program?: number; drum: boolean; notes: RawNote[] }>();
  for (const n of notes) {
    const drum = n.ch === 9;
    const instrument = drum ? drumInstrument(n.pitch) : programToInstrument(n.program);
    const key = drum ? `d:${instrument}` : `${n.ch}:${n.program}`;
    let g = groups.get(key);
    if (!g) {
      const program = !drum && USED_GM_PROGRAMS.includes(n.program) && GM_PROGRAM[instrument] !== n.program ? n.program : undefined;
      g = { instrument, program, drum, notes: [] };
      groups.set(key, g);
    }
    g.notes.push(n);
  }
  const tracks: Track[] = [];
  let dropped = 0;
  for (const g of groups.values()) {
    const sorted = g.notes.map((n) => ({ ...n, start: snap(n.start), end: Math.max(snap(n.start) + STEP, snap(n.end)) })).sort((a, b) => a.start - b.start || b.pitch - a.pitch);
    const voices: { end: number; list: typeof sorted }[] = [];
    for (const n of sorted) {
      // ドラムは、同じ位置の同じ打楽器が重なっても1つでよい。音程楽器は、空いている声部に入れる
      const v = voices.find((x) => x.end <= n.start + 1e-9);
      if (v) {
        v.list.push(n);
        v.end = n.end;
      } else if (g.drum && voices.length > 0) {
        continue;
      } else {
        voices.push({ end: n.end, list: [n] });
      }
    }
    for (const v of voices) {
      if (tracks.length >= MAX_TRACKS) {
        dropped += v.list.length;
        continue;
      }
      const events: NoteEvent[] = [];
      let cursor = 0;
      v.list.forEach((n, i) => {
        const next = v.list[i + 1];
        const end = Math.min(n.end, next ? next.start : total, total);
        if (n.start > cursor + 1e-9) events.push({ note: REST, durationBeats: round(n.start - cursor) });
        const dur = round(end - n.start);
        if (dur <= 0) return;
        events.push({ note: g.drum ? "C2" : midiToName(Math.max(12, Math.min(108, n.pitch))), durationBeats: dur, velocity: Math.round((n.vel / 100) * 100) / 100 });
        cursor = end;
      });
      if (total - cursor > 1e-9) events.push({ note: REST, durationBeats: round(total - cursor) });
      tracks.push({ waveform: g.drum ? "square" : "triangle", instrument: g.instrument, ...(g.program !== undefined ? { program: g.program } : {}), volume: g.drum ? 0.24 : 0.18, pan: 0, notes: events });
    }
  }
  if (dropped) warnings.push(`トラックが多すぎるので、${dropped}音を読み込みませんでした（最大${MAX_TRACKS}トラック）`);
  const bpm = Math.round(tempo || 120);
  return { score: { tempoBpm: Math.max(20, Math.min(300, bpm)), timeSig, loop: true, tracks }, notes: notes.length - dropped, warnings };
}

function round(x: number): number {
  return Math.round(x * 1e6) / 1e6;
}

function drumInstrument(pitch: number): Instrument {
  if (pitch === 35 || pitch === 36) return "kick";
  if (pitch === 39) return "clap";
  if (pitch === 29 || pitch === 30) return "scratch";
  if (pitch === 46) return "openhat";
  if (pitch === 37 || pitch === 38 || pitch === 40) return "snare";
  if (pitch === 42 || pitch === 44) return "hihat";
  if ([41, 43, 45, 47, 48, 50].includes(pitch)) return "tom";
  return "crash";
}

/** GMの楽器番号から、いちばん近い楽器を選ぶ。 */
export function programToInstrument(program: number): Instrument {
  for (const [inst, p] of Object.entries(GM_PROGRAM)) if (p === program && !["echoGuitar", "leadGuitar", "cowbell", "wind", "stream", "rain", "bird", "crickets", "chime", "pad"].includes(inst)) return inst as Instrument;
  if (program <= 3) return "piano";
  if (program <= 5) return "keys";
  if (program <= 7) return "harpsichord";
  if (program <= 15) return "bell";
  if (program <= 23) return "keys";
  if (program <= 28) return "guitar";
  if (program === 29) return "crunch";
  if (program <= 31) return "distGuitar";
  if (program <= 35) return "bass";
  if (program <= 37) return "slap";
  if (program <= 39) return "sub808";
  if (program <= 51) return "strings";
  if (program <= 54) return "choir";
  if (program === 55) return "strings";
  if (program <= 63) return "brass";
  if (program <= 87) return "lead";
  if (program <= 103) return "pad";
  if (program <= 111) return "guitar";
  if (program <= 119) return "bell";
  return "pad";
}
