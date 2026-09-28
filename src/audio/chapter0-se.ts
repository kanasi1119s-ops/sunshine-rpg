import type { Score } from "./score";

/**
 * 序章の効果音一式（`docs/sound/tracks.md`）。すべてオリジナルの短い音で、
 * 動作確認用データ（`sample-tracks.ts`）とは別に、実際の画面で使うために作った。
 */

export const CHAPTER0_CONFIRM_SE: Score = {
  tempoBpm: 200,
  loop: false,
  tracks: [
    {
      waveform: "square",
      volume: 0.35,
      notes: [
        { note: "C6", durationBeats: 0.5 },
        { note: "E6", durationBeats: 0.5 },
      ],
    },
  ],
};

/** メニュー・選択肢のカーソル移動音。 */
export const CHAPTER0_CURSOR_SE: Score = {
  tempoBpm: 200,
  loop: false,
  tracks: [
    {
      waveform: "square",
      volume: 0.2,
      notes: [{ note: "A5", durationBeats: 0.4 }],
    },
  ],
};

/** マップの出入り口（扉・出口）をくぐったときの音。 */
export const CHAPTER0_DOOR_SE: Score = {
  tempoBpm: 200,
  loop: false,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.28,
      notes: [
        { note: "G4", durationBeats: 0.5 },
        { note: "D4", durationBeats: 0.7 },
      ],
    },
  ],
};

/** 戦闘勝利のファンファーレ。 */
export const CHAPTER0_VICTORY_SE: Score = {
  tempoBpm: 200,
  loop: false,
  tracks: [
    {
      waveform: "square",
      volume: 0.32,
      notes: [
        { note: "C5", durationBeats: 0.5 },
        { note: "E5", durationBeats: 0.5 },
        { note: "G5", durationBeats: 0.5 },
        { note: "C6", durationBeats: 1.5 },
      ],
    },
  ],
};

/** 全滅したときの音（全滅時の専用画面はまだ無いため、現時点では未接続）。 */
export const CHAPTER0_DEFEAT_SE: Score = {
  tempoBpm: 160,
  loop: false,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.28,
      notes: [
        { note: "G4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "C4", durationBeats: 2 },
      ],
    },
  ],
};

/**
 * 攻撃・ダメージの効果音（作成済み・現時点では未接続）。
 * 戦闘ログが文字列（`BattleState.log`）だけを持つ形になっており、
 * 「攻撃」「ダメージ」「会心」などを型で区別できないため、
 * 文字列の中身を見て判定する不安定な方法は避け、接続を見送った。
 * 接続するには、まず戦闘ログにイベント種別を持たせる設計変更が要る
 * （`docs/design/battle.md` に申し送り済み）。
 */
export const CHAPTER0_ATTACK_SE: Score = {
  tempoBpm: 200,
  loop: false,
  tracks: [
    {
      waveform: "sawtooth",
      volume: 0.3,
      notes: [{ note: "C3", durationBeats: 0.4 }],
    },
  ],
};
