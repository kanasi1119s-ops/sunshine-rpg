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

/**
 * 楽器の音色。指定がなければ、`waveform`の波形をそのまま鳴らす（従来の音）。
 * 打楽器（kick・snare・hihat・crash）は音の高さを使わない（音名は何でもよい）。
 */
export type Instrument =
  | "kick" | "snare" | "hihat" | "crash"
  | "bass" | "guitar" | "echoGuitar" | "crunch" | "distGuitar" | "leadGuitar"
  | "keys" | "piano" | "harpsichord" | "strings" | "pad" | "bell" | "lead"
  // 効果音向け: 音程が滑る（sfxDown＝下がる／sfxUp＝上がる）、ノイズの衝撃音（impact）、風を切る音（swoosh）、金属的な鈴（chime）
  | "sfxDown" | "sfxUp" | "impact" | "swoosh" | "chime"
  // 自然音（風・雨・せせらぎ・鳥・虫）。音の高さは、風の吹く高さ・鳥の声の高さなど音色の目安として使う
  | "wind" | "rain" | "stream" | "bird" | "crickets"
  // フォンク向け: 重く歪んだ低音（808）とカウベル
  | "sub808" | "cowbell";

export interface Track {
  waveform: Waveform;
  /** 楽器の音色（省略時は`waveform`のまま）。 */
  instrument?: Instrument;
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
  instrument?: Instrument;
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
        instrument: track.instrument,
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
