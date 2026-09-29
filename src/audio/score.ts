import { noteNameToFrequency } from "./note";

/** 音を鳴らさない拍（休符）。 */
export const REST = "R";

export interface NoteEvent {
  /** "C4" のような音名、または休符（REST）。 */
  note: string;
  /** 何拍分の長さか（4分音符=1、8分音符=0.5など）。 */
  durationBeats: number;
  /** 強さ（1が標準。ゴーストノートなど弱い音は0.5など）。省略時は1。 */
  velocity?: number;
}

export type Waveform = "square" | "triangle" | "sawtooth" | "sine";

/**
 * 楽器の音色。指定がなければ、`waveform`の波形をそのまま鳴らす（従来の音）。
 * 打楽器（kick・snare・hihat・crash）は音の高さを使わない（音名は何でもよい）。
 */
export type Instrument =
  | "kick" | "snare" | "hihat" | "crash" | "tom"
  | "bass" | "guitar" | "echoGuitar" | "crunch" | "distGuitar" | "leadGuitar"
  | "keys" | "piano" | "harpsichord" | "strings" | "pad" | "choir" | "brass" | "bell" | "lead"
  // 効果音向け: 音程が滑る（sfxDown＝下がる／sfxUp＝上がる）、ノイズの衝撃音（impact）、風を切る音（swoosh）、金属的な鈴（chime）
  | "sfxDown" | "sfxUp" | "impact" | "swoosh" | "chime"
  // 自然音（風・雨・せせらぎ・鳥・虫）。音の高さは、風の吹く高さ・鳥の声の高さなど音色の目安として使う
  | "pierce" | "slap" | "wind" | "rain" | "stream" | "bird" | "crickets"
  // フォンク向け: 重く歪んだ低音（808）とカウベル
  | "sub808" | "cowbell";

export interface Track {
  waveform: Waveform;
  /** 楽器の音色（省略時は`waveform`のまま）。 */
  instrument?: Instrument;
  /** 左右の位置（-1=左、0=中央、1=右）。省略時は中央。 */
  pan?: number;
  /** 効果音用: 録音音源（GMの楽器番号）で鳴らす。準備ができていないときは、`instrument`・`waveform`の合成音で鳴らす。 */
  gm?: number;
  /** 効果音用: trueなら、音名は「GMドラムのキー番号」を表す（例: 36=C2=バスドラム）。 */
  gmDrum?: boolean;
  /** 0〜1。 */
  volume: number;
  notes: NoteEvent[];
}

export interface Score {
  /** 録音音源で鳴らすときのドラムセット（GMのドラムキット番号。0=標準、16=パワー、24=電子、25=TR-808、32=ジャズ）。省略時は0。 */
  drumKit?: number;
  /** trueなら、パッド・弦・合唱の音量をキックに合わせて周期的に凹ませる（電子音楽風のポンプ感）。 */
  pump?: boolean;
  /** 楽器の音色の傾向。rock=オーバードライブ・温かいドラム、metal=メタルゾーンのギター・重低音のベース・締まったドラム。 */
  tone?: "rock" | "metal";
  /** trueなら、曲の頭に強い一撃（全楽器の強いアタック、クラッシュ、バスドラム）を入れる。ループのたびに聴き手をつかむ。 */
  opening?: boolean;
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
  pan?: number;
  /** 1拍の長さ（秒）。テンポに合わせたエコーなどに使う。 */
  beatSec: number;
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

/** 同じ入力なら同じ結果になる、ごく小さな強さのゆらぎ（機械的な均一さをやわらげる）。 */
export function humanize(startSec: number): number {
  const x = Math.sin(startSec * 12.9898 + 78.233) * 43758.5453;
  return 0.93 + 0.14 * (x - Math.floor(x));
}

function flattenTrack(track: Track, tempoBpm: number, loop: boolean): ScheduledNote[] {
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
        volume: track.volume * (noteEvent.velocity ?? 1) * (loop && track.instrument ? humanize(t) : 1),
        pan: track.pan,
        beatSec: secPerBeat,
      });
    }
    t += durationSec;
  }
  return events;
}

/** 曲を「いつ・どの高さ・どれくらいの長さで鳴らすか」の一覧に変換する。 */
export function flattenScore(score: Score): ScheduledNote[] {
  return score.tracks.flatMap((track) => flattenTrack(track, score.tempoBpm, score.loop));
}
