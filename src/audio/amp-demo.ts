import { AMP_PRESET_NAMES, type AmpPresetName } from "./amp";
import { REST, type NoteEvent, type Score } from "./score";

/**
 * アンプシミュレーターの試聴用デモ。ジャンル別プリセットを聞き比べるための、短い16拍のフレーズ。
 * フレーズは全プリセットで同じ（音色の違いだけを聞き比べるため）。マイナー・ペンタトニックの
 * 音を並べただけのオリジナルの練習フレーズで、既存曲のメロディではない（CLAUDE.md 1-1）。
 * 本編の曲ではないので、ゲーム内のどこにも自動では使われない（開発中の `a` キーで試聴できる）。
 */

function notes(spec: string): NoteEvent[] {
  return spec.split(" ").map((token) => {
    const [name, beats] = token.split(":");
    return { note: name === "R" ? REST : name, durationBeats: Number(beats) };
  });
}

/** 低い刻みのリフ（根音）。合計16拍。 */
const RIFF_ROOT =
  "A2:0.5 A2:0.5 C3:0.5 A2:0.5 D3:1 C3:0.5 A2:0.5 " +
  "E3:1 D3:0.5 C3:0.5 A2:1 R:1 " +
  "A2:0.5 A2:0.5 C3:0.5 A2:0.5 G3:1 E3:0.5 D3:0.5 " +
  "C3:1 A2:1 A2:2";

/** 5度上を重ねる（パワーコードのような厚み）。 */
const RIFF_FIFTH =
  "E3:0.5 E3:0.5 G3:0.5 E3:0.5 A3:1 G3:0.5 E3:0.5 " +
  "B3:1 A3:0.5 G3:0.5 E3:1 R:1 " +
  "E3:0.5 E3:0.5 G3:0.5 E3:0.5 D4:1 B3:0.5 A3:0.5 " +
  "G3:1 E3:1 E3:2";

/** 低音（アンプは通さない）。 */
const BASS = "A1:2 A1:2 A1:2 R:1 A1:1 A1:2 A1:2 A1:2 A1:2";

export function makeAmpDemoScore(amp: AmpPresetName): Score {
  return {
    tempoBpm: 112,
    loop: true,
    tracks: [
      { waveform: "sawtooth", volume: 0.2, notes: notes(RIFF_ROOT), amp },
      { waveform: "sawtooth", volume: 0.2, notes: notes(RIFF_FIFTH), amp },
      { waveform: "triangle", volume: 0.2, notes: notes(BASS) },
    ],
  };
}

export const AMP_DEMO_SCORES: Record<AmpPresetName, Score> = Object.fromEntries(
  AMP_PRESET_NAMES.map((name) => [name, makeAmpDemoScore(name)]),
) as Record<AmpPresetName, Score>;
