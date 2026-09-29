import { noteNameToMidi } from "./note";
import { REST, type Instrument, type NoteEvent, type Score, type Track, type Waveform } from "./score";

/**
 * 長めの曲（1〜1分半）を、コード進行とリズムの型（パターン）から組み立てる小さな道具。
 * 旋律は手で書き、伴奏（ベース・ドラム・ギター・鍵盤など）は「コード進行×パターン」で作る。
 *
 * パターン文字（1文字が `step` 拍ぶん。コード1つにつき1小節ぶん。空白で区切ると小節ごとに変えられる）:
 *   R=根音  5=5度  O=1オクターブ上の根音  a〜d=コードの1〜4番目の音（大文字は1オクターブ上）
 *   x=打楽器の一打（`fixed`つきのパートだけ）  o=弱い一打（ゴーストノート）  X=強いアクセント  -=前の音をのばす  .=休み
 */

const KINDS = {
  maj: [0, 4, 7],
  min: [0, 3, 7],
  "5": [0, 7, 12],
  maj7: [0, 4, 7, 11],
  min7: [0, 3, 7, 10],
  dom7: [0, 4, 7, 10],
  sus2: [0, 2, 7],
  dim: [0, 3, 6],
} as const;
type Kind = keyof typeof KINDS;

const SUFFIX: Record<string, Kind> = { "": "maj", m: "min", "5": "5", maj7: "maj7", m7: "min7", "7": "dom7", sus2: "sus2", dim: "dim" };
const PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

interface Chord {
  pitchClass: number;
  kind: Kind;
}

/** "Am7 F G7" のようなコード進行を読む。 */
export function parseChords(spec: string): Chord[] {
  return spec.split(/\s+/).filter(Boolean).map((token) => {
    const m = /^([A-G][#b]?)(maj7|m7|m|7|5|sus2|dim)?$/.exec(token);
    if (!m) {
      throw new Error(`不正なコード名です: ${token}`);
    }
    return { pitchClass: noteNameToMidi(`${m[1]}4`) % 12, kind: SUFFIX[m[2] ?? ""] };
  });
}

export function midiToName(midi: number): string {
  return `${PITCH_NAMES[midi % 12]}${Math.floor(midi / 12) - 1}`;
}

function toneOffset(ch: string, kind: Kind): number | null {
  const tones = KINDS[kind];
  if (ch === "R") return 0;
  if (ch === "5") return 7;
  if (ch === "O") return 12;
  const lower = ch.toLowerCase();
  const idx = "abcd".indexOf(lower);
  if (idx < 0) return null;
  const octaves = Math.floor(idx / tones.length);
  return tones[idx % tones.length] + 12 * octaves + (ch !== lower ? 12 : 0);
}

export interface PartSpec {
  instrument?: Instrument;
  waveform: Waveform;
  volume: number;
  /** 根音を置くオクターブ（C4が真ん中のド）。 */
  octave: number;
  /** パターン1文字ぶんの拍数。 */
  step: number;
  /** 打楽器用: 「x」で鳴らす固定の音名。 */
  fixed?: string;
}
export interface MelodySpec {
  instrument?: Instrument;
  waveform: Waveform;
  volume: number;
}
export interface Section {
  /** 1小節に1つのコード。 */
  chords: string;
  /** この区間だけの1小節の拍数（拍子の変わり目。省略時は曲全体の拍数）。 */
  beatsPerBar?: number;
  /** パート名 → パターン。書かなかったパートは、この区間は休み。 */
  parts?: Record<string, string>;
  /** 旋律パート名 → "音名:拍数 ..." の列（区間の拍数とぴったり一致させる）。 */
  melody?: Record<string, string>;
}
export interface Arrangement {
  tempoBpm: number;
  beatsPerBar: number;
  sections: Section[];
  parts: Record<string, PartSpec>;
  melodies: Record<string, MelodySpec>;
}

export function parseNotes(spec: string): NoteEvent[] {
  return spec.split(/\s+/).filter(Boolean).map((token) => {
    const [name, beats] = token.split(":");
    return { note: name === "R" ? REST : name, durationBeats: Number(beats) };
  });
}

function pushEvent(events: NoteEvent[], note: string, beats: number): void {
  const last = events[events.length - 1];
  if (note === REST && last && last.note === REST) {
    last.durationBeats += beats;
  } else {
    events.push({ note, durationBeats: beats });
  }
}

function renderBar(events: NoteEvent[], pattern: string, chord: Chord, spec: PartSpec, beatsPerBar: number): void {
  if (Math.abs(pattern.length * spec.step - beatsPerBar) > 1e-9) {
    throw new Error(`パターン「${pattern}」の長さが1小節（${beatsPerBar}拍）に合いません`);
  }
  const root = chord.pitchClass + 12 * (spec.octave + 1);
  for (const ch of pattern) {
    if (ch === "-") {
      const last = events[events.length - 1];
      if (!last) throw new Error("先頭に「-」は置けません");
      last.durationBeats += spec.step;
    } else if (ch === ".") {
      pushEvent(events, REST, spec.step);
    } else if ((ch === "x" || ch === "o" || ch === "X") && spec.fixed) {
      // x=標準、o=弱い（ゴースト）、X=強いアクセント
      events.push({ note: spec.fixed, durationBeats: spec.step, ...(ch === "o" ? { velocity: 0.5 } : ch === "X" ? { velocity: 1.25 } : {}) });
    } else {
      const offset = toneOffset(ch, chord.kind);
      if (offset === null) throw new Error(`不正なパターン文字です: ${ch}`);
      events.push({ note: midiToName(root + offset), durationBeats: spec.step });
    }
  }
}

/** 楽器ごとの標準の左右位置。同じ楽器のパートが複数あるときは、左右に振り分けて広がりを出す。 */
const BASE_PAN: Partial<Record<Instrument, number>> = {
  hihat: 0.35, crash: -0.3, crunch: -0.5, distGuitar: -0.55, guitar: 0.3, echoGuitar: 0.25, keys: -0.25, piano: -0.15,
  harpsichord: -0.3, strings: 0, pad: 0, bell: 0.4, bird: 0.6, wind: -0.5, stream: 0.5, rain: 0, crickets: 0.4, chime: 0.3,
};
function assignPan(tracks: Track[]): void {
  const seen = new Map<Instrument, number>();
  for (const t of tracks) {
    if (!t.instrument || !(t.instrument in BASE_PAN)) continue;
    const n = seen.get(t.instrument) ?? 0;
    seen.set(t.instrument, n + 1);
    const spread = n === 0 ? 0 : (n % 2 === 1 ? 1 : -1) * Math.ceil(n / 2) * (t.instrument === "distGuitar" || t.instrument === "crunch" ? 1.1 : 0.4);
    t.pan = Math.max(-0.9, Math.min(0.9, (BASE_PAN[t.instrument] ?? 0) + spread));
  }
}

/** 全パートの拍数がそろった、ループする曲を作る。 */
export function arrange(a: Arrangement): Score {
  const tracks: Track[] = [];
  const build = (spec: { instrument?: Instrument; waveform: Waveform; volume: number }, events: NoteEvent[]): void => {
    tracks.push({ waveform: spec.waveform, instrument: spec.instrument, volume: spec.volume, notes: events });
  };
  for (const [key, spec] of Object.entries(a.parts)) {
    const events: NoteEvent[] = [];
    for (const section of a.sections) {
      const chords = parseChords(section.chords);
      const bpb = section.beatsPerBar ?? a.beatsPerBar;
      const pattern = section.parts?.[key];
      if (!pattern) {
        pushEvent(events, REST, chords.length * bpb);
        continue;
      }
      const bars = pattern.split(" ");
      chords.forEach((chord, i) => renderBar(events, bars[i % bars.length], chord, spec, bpb));
    }
    build(spec, events);
  }
  for (const [key, spec] of Object.entries(a.melodies)) {
    const events: NoteEvent[] = [];
    a.sections.forEach((section, index) => {
      const beats = parseChords(section.chords).length * (section.beatsPerBar ?? a.beatsPerBar);
      const notes = section.melody?.[key];
      if (!notes) {
        pushEvent(events, REST, beats);
        return;
      }
      const parsed = parseNotes(notes);
      const sum = parsed.reduce((s, n) => s + n.durationBeats, 0);
      if (Math.abs(sum - beats) > 1e-9) {
        throw new Error(`旋律「${key}」の第${index + 1}区間の拍数が合いません（${sum}拍。必要なのは${beats}拍）`);
      }
      events.push(...parsed);
    });
    build(spec, events);
  }
  assignPan(tracks);
  return { tempoBpm: a.tempoBpm, loop: true, tracks };
}
