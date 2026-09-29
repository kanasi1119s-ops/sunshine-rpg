import type { NoteEvent, Track } from "./score";
import { REST } from "./score";

/**
 * 作曲ソフトのピアノロール用: トラック（休みを含む順番の音の列）と、位置つきの音の一覧を行き来する道具。
 * トラックは1度に1音しか鳴らせない（和音は複数のトラックで作る）ため、重なった音は、あとの音が始まる位置で切る。
 */
export interface RollNote {
  /** 始まりの位置（拍）。 */
  start: number;
  /** 長さ（拍）。 */
  dur: number;
  /** 音名（"C4" など）。 */
  note: string;
  velocity?: number;
}

const EPS = 1e-6;

export function trackTotalBeats(track: Track): number {
  return track.notes.reduce((s, n) => s + n.durationBeats, 0);
}

/** トラックから、休みをのぞいた音の一覧（位置つき）を取り出す。 */
export function trackToNotes(track: Track): RollNote[] {
  const out: RollNote[] = [];
  let at = 0;
  for (const n of track.notes) {
    if (n.note !== REST) {
      out.push({ start: at, dur: n.durationBeats, note: n.note, ...(n.velocity !== undefined ? { velocity: n.velocity } : {}) });
    }
    at += n.durationBeats;
  }
  return out;
}

/** 音の一覧から、トラックの音の列を作る。全体の長さ（totalBeats）にそろえて、間は休みで埋める。 */
export function notesToEvents(notes: RollNote[], totalBeats: number): NoteEvent[] {
  const sorted = [...notes].filter((n) => n.start < totalBeats - EPS).sort((a, b) => a.start - b.start);
  const events: NoteEvent[] = [];
  let cursor = 0;
  sorted.forEach((n, i) => {
    const next = sorted[i + 1];
    const limit = Math.min(next ? next.start : totalBeats, totalBeats);
    const dur = Math.min(n.dur, limit - n.start);
    if (dur <= EPS || n.start < cursor - EPS) {
      return;
    }
    if (n.start > cursor + EPS) {
      events.push({ note: REST, durationBeats: round(n.start - cursor) });
    }
    events.push({ note: n.note, durationBeats: round(dur), ...(n.velocity !== undefined ? { velocity: n.velocity } : {}) });
    cursor = n.start + dur;
  });
  if (totalBeats - cursor > EPS) {
    events.push({ note: REST, durationBeats: round(totalBeats - cursor) });
  }
  return events;
}

function round(x: number): number {
  return Math.round(x * 1e6) / 1e6;
}

/**
 * ピアノロールの1クリック: その位置（start）を覆う音があれば消し、なければ、音名 note・長さ dur の音を足す。
 * 返す値は、新しいトラック（元は変えない）。
 */
export function toggleNote(track: Track, start: number, note: string, dur: number, totalBeats: number): Track {
  const notes = trackToNotes(track);
  const hit = notes.findIndex((n) => n.start <= start + EPS && start < n.start + n.dur - EPS);
  if (hit >= 0) {
    notes.splice(hit, 1);
  } else {
    notes.push({ start, dur, note });
  }
  return { ...track, notes: notesToEvents(notes, totalBeats) };
}
