import type { Score } from "./score";

/**
 * 音響エンジンの動作確認用データ。
 * 本物の曲・効果音は作曲・サウンド担当の工程（`docs/sound/tracks.md`）で作る。
 */
export const SAMPLE_CONFIRM_SE: Score = {
  tempoBpm: 240,
  loop: false,
  tracks: [
    {
      waveform: "square",
      volume: 0.4,
      notes: [
        { note: "C6", durationBeats: 0.5 },
        { note: "G6", durationBeats: 0.5 },
      ],
    },
  ],
};

export const SAMPLE_BGM_LOOP: Score = {
  tempoBpm: 130,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.22,
      notes: [
        { note: "C4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "A3", durationBeats: 1 },
        { note: "C4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "C4", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.18,
      notes: [
        { note: "C3", durationBeats: 4 },
        { note: "A2", durationBeats: 4 },
      ],
    },
  ],
};
