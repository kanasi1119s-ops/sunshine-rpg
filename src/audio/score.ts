import type { AmpPresetName } from "./amp";
import type { AmpPluginDef } from "./amp-plugins";
import type { AudioTrack } from "./audio-clips";
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
  /** 音の伸び（鳴らす長さの倍率。1が標準、0.3は短く切る、2は次の音まで余韻を重ねる）。次の音の始まりは変わらない。省略時は1。 */
  gate?: number;
  /** ベンド（チョーキング）: 音が出てから、この半音数だけ音程を持ち上げる（1＝半音、2＝全音）。録音音源で鳴らすときに働く。 */
  bend?: number;
  /** しゃくり（スライドで入る）: この半音数だけ下から入って、本来の音程へすべり上がる（負の値なら上から下がる）。 */
  scoop?: number;
  /** フォール（落とす）: 音の終わりに向けて、この半音数だけ音程を下げていく。 */
  fall?: number;
  /** ビブラート（音の揺れ）の深さ 0〜1。音が出て少したってから揺れ始める。 */
  vibrato?: number;
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
  | "sub808" | "cowbell"
  // 民族楽器（2026-10-02）: 撥弦（sitar・koto・shamisen・banjo・harp・kalimba）、息の楽器（panflute・shakuhachi・ocarina）、擦弦・リード（fiddle・bagpipe）
  | "sitar" | "koto" | "shamisen" | "banjo" | "harp" | "kalimba" | "panflute" | "shakuhachi" | "ocarina" | "fiddle" | "bagpipe";

/**
 * ジャンル別のアンプ（2026-09-30 追加）。ジャズ・ブルース・ファンク・クランチ・ハードロック・パンク・ファズ・
 * シューゲイザー・ローファイ・レトロ8bit・ラジオ。作り方は `amp-rack.ts`、向いている場面は `docs/sound/composition-notes.md`。
 */
export type GenreAmpType = "jazz" | "blues" | "funk" | "crunch" | "hardrock" | "punk" | "fuzz" | "shoegaze" | "lofi" | "retro8bit" | "radio" | "loudmetal" | "loudrock" | "delicate";

/** ギターなどの音づくり（アンプ）の設定。`auto`は、曲の音色（tone）と楽器から自動で選ぶ。 */
export interface AmpSetting {
  type: "auto" | "clean" | "overdrive" | "distortion" | "metal" | "prs" | "nam" | GenreAmpType | "genre" | "plugin";
  /** type=plugin のとき、使うアンプ定義のID（`Score.ampPlugins` のキー）。 */
  plugin?: string;
  /** type=genre のとき、amp.ts のプリセット名（ジャンル別の種類は、なるべく上の直接の種類へ置きかえて鳴らす）。 */
  preset?: AmpPresetName;
  /** 歪みの深さの倍率（0.5〜2、既定1）。 */
  drive?: number;
  /** 高音の明るさ（dB。-6〜+6、既定0）。 */
  tone?: number;
  /** 出力の大きさの倍率（0.5〜1.5、既定1）。 */
  level?: number;
  /** type=nam のとき、使うNAMモデルの名前（`Score.namModels`のキー）。 */
  model?: string;
}

export interface Track {
  waveform: Waveform;
  /** 楽器の音色（省略時は`waveform`のまま）。 */
  instrument?: Instrument;
  /** 左右の位置（-1=左、0=中央、1=右）。省略時は中央。 */
  pan?: number;
  /** 音づくり（アンプ）の設定。省略時は自動。 */
  amp?: AmpSetting;
  /** 録音音源で鳴らすときの、GMの楽器番号の指定（省略時は`instrument`から決める）。実楽器版で使う。 */
  program?: number;
  /** 効果音用: 録音音源（GMの楽器番号）で鳴らす。準備ができていないときは、`instrument`・`waveform`の合成音で鳴らす。 */
  gm?: number;
  /** 効果音用: trueなら、音名は「GMドラムのキー番号」を表す（例: 36=C2=バスドラム）。 */
  gmDrum?: boolean;
  /** 0〜1。 */
  volume: number;
  /** タイミングのずれ（拍。-0.1〜0.1）。プラス＝あと乗り（少し遅らせる。スネアやバックビートに）、マイナス＝前のめり（少し早める。ハイハットに）。省略時は0。 */
  push?: number;
  notes: NoteEvent[];
}

/**
 * グルーブ（ノリ）による、音の始まりのずれ（拍）。`swing`＝裏拍を遅らせる量（0〜1。0.5くらいで三連寄りのはね）、`push`＝パートごとのずれ。
 * 8分の裏拍（0.5拍目）は swing/6 拍、16分の裏（0.25・0.75拍目）は swing/12 拍遅れる。
 */
export function grooveOffsetBeats(swing: number | undefined, push: number | undefined, startBeat: number): number {
  let off = push ?? 0;
  if (swing) {
    const frac = Math.round((startBeat - Math.floor(startBeat)) * 1000) / 1000;
    if (frac === 0.5) off += swing / 6;
    else if (frac === 0.25 || frac === 0.75) off += swing / 12;
  }
  return off;
}

export interface Score {
  /** 裏拍を遅らせる量（0〜1）。省略時は0（ずらさない）。 */
  swing?: number;
  /** 読み込んだNAMモデル（.namファイルの中身）。名前 → JSON文字列。 */
  namModels?: Record<string, string>;
  /** 録音したトラック（オーディオインターフェースから録った、実際の楽器・声）。作曲ソフトで鳴る（ゲーム本体では鳴らさない）。 */
  audioTracks?: AudioTrack[];
  /** 追加したアンプ（アンプ定義ファイルの中身）。ID → 定義。 */
  ampPlugins?: Record<string, AmpPluginDef>;
  /** 録音音源で鳴らすときのドラムセット（GMのドラムキット番号。0=標準、16=パワー、24=電子、25=TR-808、32=ジャズ）。省略時は0。 */
  drumKit?: number;
  /** trueなら、パッド・弦・合唱の音量をキックに合わせて周期的に凹ませる（電子音楽風のポンプ感）。 */
  pump?: boolean;
  /** trueなら、リードとパッドを電子的な音色にする（電子音楽向け）。省略時は生楽器に近い音色。 */
  synth?: boolean;
  /** ゲームで鳴らすときの、曲ごとの音量補正（dB）。曲どうしの音量差をそろえる（`bgm-trim.ts`）。省略は0。 */
  trimDb?: number;
  /** 音の版。modern=現代的な音（既定）、ps2=PS2世代のゲーム音楽（オーケストラの重ね・豊かなホール残響・高音をやや丸めた音）。 */
  edition?: "modern" | "ps2" | "real";
  /** 曲調（rock・classic・jazz など）。実楽器版で、楽器の割り当てを決めるために使う。 */
  style?: string;
  /** 楽器の音色の傾向。rock=オーバードライブ・温かいドラム、metal=メタルゾーンのギター・重低音のベース・締まったドラム、prs=特別曲用。粒立ちがよく歌うような、なめらかで澄んだギター（メタルの重さは保つ）。 */
  tone?: "rock" | "metal" | "prs";
  /** trueなら、曲の頭に強い一撃（全楽器の強いアタック、クラッシュ、バスドラム）を入れる。ループのたびに聴き手をつかむ。 */
  opening?: boolean;
  tempoBpm: number;
  /** 拍子（例: 4/4、3/4、7/8、5/4）。省略時は4/4。音の長さ（拍）は、いつも4分音符=1拍で数える。 */
  timeSig?: { num: number; den: number };
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

function flattenTrack(track: Track, tempoBpm: number, loop: boolean, swing?: number): ScheduledNote[] {
  const secPerBeat = 60 / tempoBpm;
  let t = 0;
  const events: ScheduledNote[] = [];
  for (const noteEvent of track.notes) {
    const durationSec = noteEvent.durationBeats * secPerBeat;
    if (noteEvent.note !== REST) {
      const soundSec = durationSec * (noteEvent.gate ?? 1);
      events.push({
        frequency: noteNameToFrequency(noteEvent.note),
        startSec: Math.max(0, t + grooveOffsetBeats(swing, track.push, t / secPerBeat) * secPerBeat),
        durationSec: soundSec,
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
  return score.tracks.flatMap((track) => flattenTrack(track, score.tempoBpm, score.loop, score.swing));
}
