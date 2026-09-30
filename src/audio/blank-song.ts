import { REST, type Instrument, type Score, type Track } from "./score";
import { barBeats, type TimeSignature } from "./time-signature";

/** 1から曲を作るときの、はじめの編成。 */
export type BlankTemplate = "single" | "piano" | "band" | "orchestra" | "electronic";

export const BLANK_TEMPLATES: [BlankTemplate, string][] = [
  ["single", "トラック1つ（ピアノ）"],
  ["piano", "ピアノ（右手・左手）"],
  ["band", "バンド（ドラム・ベース・ギター2本・キーボード・メロディ）"],
  ["orchestra", "オーケストラ（弦3・ブラス・合唱・ピアノ・ティンパニ風のタム）"],
  ["electronic", "電子音楽（キック・スネア・ハット・808ベース・パッド・リード）"],
];

const TEMPLATES: Record<BlankTemplate, [Instrument, number, number][]> = {
  single: [["piano", 0.22, 0]],
  piano: [["piano", 0.22, 0.1], ["piano", 0.18, -0.1]],
  band: [["kick", 0.3, 0], ["snare", 0.22, 0], ["hihat", 0.12, 0.35], ["crash", 0.12, -0.3], ["bass", 0.28, 0], ["crunch", 0.18, -0.45], ["guitar", 0.16, 0.45], ["keys", 0.14, 0.2], ["leadGuitar", 0.22, 0]],
  orchestra: [["strings", 0.16, -0.35], ["strings", 0.14, 0], ["strings", 0.14, 0.35], ["brass", 0.16, 0.2], ["choir", 0.12, -0.15], ["piano", 0.16, 0.1], ["tom", 0.2, 0]],
  electronic: [["kick", 0.3, 0], ["snare", 0.2, 0], ["hihat", 0.12, 0.3], ["sub808", 0.3, 0], ["pad", 0.12, -0.2], ["lead", 0.22, 0.1]],
};
const DRUMS = new Set<Instrument>(["kick", "snare", "hihat", "crash", "tom", "clap", "openhat", "scratch"]);

/** 空の曲（休みだけ）を作る。長さ = 小節の数 × 1小節の拍。 */
export function createBlankScore(opts: { bpm: number; sig: TimeSignature; bars: number; template: BlankTemplate }): Score {
  const total = Math.max(1, Math.round(opts.bars)) * barBeats(opts.sig);
  const tracks: Track[] = TEMPLATES[opts.template].map(([instrument, volume, pan]) => ({
    waveform: DRUMS.has(instrument) ? "square" : "triangle",
    instrument,
    volume,
    pan,
    notes: [{ note: REST, durationBeats: total }],
  }));
  return { tempoBpm: Math.max(20, Math.min(300, Math.round(opts.bpm))), timeSig: { ...opts.sig }, loop: true, tone: "rock", drumKit: opts.template === "electronic" ? 25 : 0, synth: opts.template === "electronic" || undefined, tracks };
}
