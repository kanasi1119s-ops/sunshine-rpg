import type { Instrument, Score, Track } from "./score";

/**
 * PS2世代のゲーム音楽らしい版（別編成）に作り直す。
 * - 主旋律（リード・リードギター・ブラス・鐘・チェンバロ）を、弦楽器がなぞって重ねる（オーケストラの厚み）
 * - ベースを、低弦（チェロ）が重ねて支える
 * - 再生時には、豊かなホール残響と、高音を少し丸めた音（当時のサンプルの帯域）をかける（`audio-engine.ts`の`applyEdition`）
 * 元の曲（modern版）は変えず、新しい曲データとして返す。
 */
const MELODIC: Instrument[] = ["lead", "leadGuitar", "brass", "bell", "harpsichord"];
const BASSES: Instrument[] = ["bass", "slap"];

export function ps2Edition(score: Score): Score {
  const extra: Track[] = [];
  for (const t of score.tracks) {
    const inst = t.instrument;
    if (!inst || t.notes.every((n) => n.note === "R")) {
      continue;
    }
    if (MELODIC.includes(inst)) {
      extra.push({ ...t, instrument: "strings", waveform: "sawtooth", volume: t.volume * 0.55, pan: 0, gm: undefined, gmDrum: undefined, notes: t.notes.map((n) => ({ ...n })) });
    } else if (BASSES.includes(inst)) {
      extra.push({ ...t, instrument: "strings", waveform: "sawtooth", volume: t.volume * 0.45, pan: 0, gm: undefined, gmDrum: undefined, notes: t.notes.map((n) => ({ ...n })) });
    }
  }
  return { ...score, tracks: [...score.tracks.map((t) => ({ ...t })), ...extra], edition: "ps2" };
}
