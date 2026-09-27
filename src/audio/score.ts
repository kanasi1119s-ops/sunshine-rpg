import { noteNameToFrequency } from "./note";

/** 音を鳴らさない拍（休符）。 */
export const REST = "R";

export interface NoteEvent {
  /** "C4" のような音名、または休符（REST）。 */
  note: string;
  /** 何拍分の長さか（4分音符=1、8分音符=0.5など）。 */
  durationBeats: number;
}

export type Waveform = "square" | "triangle" | "sawtooth" | "sine";

export interface Track {
  waveform: Waveform;
  /** 0〜1。 */
  volume: number;
  notes: NoteEvent[];
}

export interface Score {
  tempoBpm: number;
  loop: boolean;
  tracks: Track[];
}

export interface ScheduledNote {
  frequency: number;
  startSec: number;
  durationSec: number;
  waveform: Waveform;
  volume: number;
}

function trackDurationBeats(track: Track): number {
  return track.notes.reduce((sum, n) => sum + n.durationBeats, 0);
}

/** 曲1回分の長さ（秒）。パートごとに長さが違う場合は一番長いものに合わせる。 */
export function getScoreDurationSec(score: Score): number {
  const secPerBeat = 60 / score.tempoBpm;
  const longestBeats = Math.max(0, ...score.tracks.map(trackDurationBeats));
  return longestBeats * secPerBeat;
}

function flattenTrack(track: Track, tempoBpm: number): ScheduledNote[] {
  const secPerBeat = 60 / tempoBpm;
  let t = 0;
  const events: ScheduledNote[] = [];
  for (const noteEvent of track.notes) {
    const durationSec = noteEvent.durationBeats * secPerBeat;
    if (noteEvent.note !== REST) {
      events.push({
        frequency: noteNameToFrequency(noteEvent.note),
        startSec: t,
        durationSec,
        waveform: track.waveform,
        volume: track.volume,
      });
    }
    t += durationSec;
  }
  return events;
}

/** 曲を「いつ・どの高さ・どれくらいの長さで鳴らすか」の一覧に変換する。 */
export function flattenScore(score: Score): ScheduledNote[] {
  return score.tracks.flatMap((track) => flattenTrack(track, score.tempoBpm));
}
