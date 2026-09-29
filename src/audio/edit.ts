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

/** 音の長さを変える: start の位置から始まる音の長さを dur（拍）にする。音がなければ元のまま。 */
export function resizeNote(track: Track, start: number, dur: number, totalBeats: number): Track {
  const notes = trackToNotes(track);
  const hit = notes.find((n) => Math.abs(n.start - start) < EPS);
  if (!hit || dur <= EPS) {
    return track;
  }
  hit.dur = dur;
  return { ...track, notes: notesToEvents(notes, totalBeats) };
}

/** その位置（start）を覆っている音の、始まりの位置を返す。なければ null。 */
export function noteStartAt(track: Track, start: number): number | null {
  const hit = trackToNotes(track).find((n) => n.start <= start + EPS && start < n.start + n.dur - EPS);
  return hit ? hit.start : null;
}

/** 音を足す（上書き）: 足す音と重なっている元の音は消してから入れる。 */
export function addNotes(track: Track, added: RollNote[], totalBeats: number): Track {
  const overlaps = (a: RollNote, b: RollNote): boolean => a.start < b.start + b.dur - EPS && b.start < a.start + a.dur - EPS;
  const kept = trackToNotes(track).filter((n) => !added.some((a) => overlaps(a, n)));
  return { ...track, notes: notesToEvents([...kept, ...added], totalBeats) };
}

/** 始まりの位置が starts に入っている音を消す。 */
export function removeNotes(track: Track, starts: number[]): Track {
  const total = trackTotalBeats(track);
  const notes = trackToNotes(track).filter((n) => !starts.some((s) => Math.abs(s - n.start) < EPS));
  return { ...track, notes: notesToEvents(notes, total) };
}

/** 範囲（拍 b0〜b1、音の高さ m0〜m1）にかかる音の、始まりの位置の一覧。音の高さを見ないときは m0,m1 を省く。 */
export function notesInRange(track: Track, b0: number, b1: number, m0 = -Infinity, m1 = Infinity, pitchOf: (note: string) => number = () => 0): number[] {
  const [lo, hi] = b0 <= b1 ? [b0, b1] : [b1, b0];
  const [plo, phi] = m0 <= m1 ? [m0, m1] : [m1, m0];
  return trackToNotes(track)
    .filter((n) => n.start < hi + EPS && n.start + n.dur > lo - EPS)
    .filter((n) => {
      const p = pitchOf(n.note);
      return p >= plo && p <= phi;
    })
    .map((n) => n.start);
}

/**
 * 選んだ音（始まりの位置 starts）を、dBeat 拍・dSemi 半音 動かす。曲の外へ出る音は、はみ出さないところで止める。
 * 返す値は、新しいトラックと、動かしたあとの始まりの位置の一覧。
 */
export function moveNotes(track: Track, starts: number[], dBeat: number, dSemi: number, transpose: (note: string, semi: number) => string): { track: Track; starts: number[] } {
  const total = trackTotalBeats(track);
  const all = trackToNotes(track);
  const picked = all.filter((n) => starts.some((s) => Math.abs(s - n.start) < EPS));
  if (picked.length === 0) return { track, starts: [] };
  const first = Math.min(...picked.map((n) => n.start));
  const last = Math.max(...picked.map((n) => n.start + n.dur));
  const shift = Math.max(-first, Math.min(total - last, dBeat));
  const moved = picked.map((n) => ({ ...n, start: round(n.start + shift), note: dSemi ? transpose(n.note, dSemi) : n.note }));
  const rest = all.filter((n) => !picked.includes(n));
  const base = { ...track, notes: notesToEvents(rest, total) };
  return { track: addNotes(base, moved, total), starts: moved.map((n) => n.start) };
}

/** 選んだ音を取り出す（コピー用）。位置は、いちばん早い音を0とした相対の位置にする。 */
export function copyNotes(track: Track, starts: number[]): RollNote[] {
  const picked = trackToNotes(track).filter((n) => starts.some((s) => Math.abs(s - n.start) < EPS));
  if (picked.length === 0) return [];
  const first = Math.min(...picked.map((n) => n.start));
  return picked.map((n) => ({ ...n, start: round(n.start - first) }));
}

/** コピーした音を、at 拍の位置に貼り付ける（曲の外にはみ出す音は切る）。返す値は、新しいトラックと、貼った音の始まりの位置。 */
export function pasteNotes(track: Track, clip: RollNote[], at: number): { track: Track; starts: number[] } {
  const total = trackTotalBeats(track);
  const placed = clip.map((n) => ({ ...n, start: round(n.start + at) })).filter((n) => n.start < total - EPS).map((n) => ({ ...n, dur: Math.min(n.dur, total - n.start) }));
  return { track: addNotes(track, placed, total), starts: placed.map((n) => n.start) };
}

/** 選んだ音の長さを、すべて dur 拍にそろえる。 */
export function setNotesLength(track: Track, starts: number[], dur: number): Track {
  const total = trackTotalBeats(track);
  const notes = trackToNotes(track).map((n) => (starts.some((s) => Math.abs(s - n.start) < EPS) ? { ...n, dur } : n));
  return { ...track, notes: notesToEvents(notes, total) };
}
