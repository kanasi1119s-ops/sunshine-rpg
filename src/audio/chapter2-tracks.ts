import type { Score } from "./score";

/**
 * 第2章（硝子湖）のBGM。`docs/sound/tracks.md`の方針
 * （16bit風チップチューン×現代的な音づくり。全パートの合計拍数が
 * 揃うように作り、ループのつなぎ目で不自然に途切れないようにしている）
 * に沿ってオリジナルで作曲した。既存曲のメロディ・コード進行は使っていない。
 */

/**
 * 硝子湖の町（BGM）。
 * 現代的な工夫: メロディとは別パートに、和音を細かく刻むアルペジオ
 * （8分音符でG→C→Dの三和音を上下させる）を重ね、「硝子（ガラス）のように
 * 澄んだ湖面に光がきらめく」情景を表現した。麦香野の村テーマ（低音ドローン＋
 * テンション和音）とは違う手法で、明るい交易都市らしい賑わいを出している。
 */
export const CHAPTER2_TOWN_THEME: Score = {
  tempoBpm: 112,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.24,
      notes: [
        { note: "G4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "B4", durationBeats: 1 },
        { note: "D5", durationBeats: 1 },
        { note: "C5", durationBeats: 1 },
        { note: "B4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
        { note: "A4", durationBeats: 1 },
        { note: "B4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 1 },
        { note: "E5", durationBeats: 1 },
        { note: "D5", durationBeats: 1 },
        { note: "B4", durationBeats: 1 },
        { note: "G4", durationBeats: 2 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.15,
      notes: [
        { note: "G3", durationBeats: 4 },
        { note: "C3", durationBeats: 4 },
        { note: "D3", durationBeats: 4 },
        { note: "G3", durationBeats: 4 },
      ],
    },
    {
      // 湖面のきらめき: G→C→D→Gの三和音を8分音符のアルペジオで刻む。
      waveform: "sine",
      volume: 0.09,
      notes: [
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "E5", durationBeats: 0.5 },
        { note: "G5", durationBeats: 0.5 },
        { note: "E5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "E5", durationBeats: 0.5 },
        { note: "G5", durationBeats: 0.5 },
        { note: "E5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "F#5", durationBeats: 0.5 },
        { note: "A5", durationBeats: 0.5 },
        { note: "F#5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "F#5", durationBeats: 0.5 },
        { note: "A5", durationBeats: 0.5 },
        { note: "F#5", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "B4", durationBeats: 0.5 },
      ],
    },
  ],
};

/**
 * 密輸倉庫（BGM）。木箱の山に紛れて調査する、緊張感のある場面。
 * 現代的な工夫: 低音ドローン（D2）にAb3のトライトーンを重ねる手法
 * （麦香野の水源と同系統）に加え、拍の裏にだけ短い低音を置く
 * シンコペーションのパルスを重ね、「気配を探りながら忍び歩く」ような
 * 落ち着かないリズムを作った。
 */
export const CHAPTER2_WAREHOUSE_THEME: Score = {
  tempoBpm: 86,
  loop: true,
  tracks: [
    {
      waveform: "triangle",
      volume: 0.18,
      notes: [
        { note: "D4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "A4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "G4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "E4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "D4", durationBeats: 1 },
        { note: "C4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D4", durationBeats: 1 },
        { note: "R", durationBeats: 1 },
        { note: "F4", durationBeats: 1 },
        { note: "E4", durationBeats: 1 },
        { note: "D4", durationBeats: 3 },
      ],
    },
    {
      waveform: "sine",
      volume: 0.08,
      notes: [{ note: "D2", durationBeats: 16 }],
    },
    {
      // ドローン（D2）とトライトーンでぶつかる音。
      waveform: "sawtooth",
      volume: 0.05,
      notes: [
        { note: "Ab3", durationBeats: 8 },
        { note: "A3", durationBeats: 8 },
      ],
    },
    {
      // 拍の裏だけに短い低音を置く、忍び足のようなパルス。
      waveform: "square",
      volume: 0.06,
      notes: [
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
      ],
    },
  ],
};

/**
 * ボス戦「積荷の歪み」（BGM）。
 * 現代的な工夫: 序章・第1章のボス戦と同じ「根音とトライトーンの低音を
 * 交互に鳴らす」系統の手法を使いつつ、G〜Dbのトライトーンから
 * Ab〜Dのトライトーンへ半音ずらす（序章はD〜Ab、第1章はE〜BbとF〜Bを使用、
 * 章ごとに軸をずらして描き分けている）。木箱が次々と崩れ落ちるような
 * 前のめりのリズムにした。
 */
export const CHAPTER2_BOSS_THEME: Score = {
  tempoBpm: 146,
  loop: true,
  tracks: [
    {
      waveform: "square",
      volume: 0.3,
      notes: [
        { note: "G4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "Db5", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "Db5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "Db5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "F4", durationBeats: 0.5 },
        { note: "G4", durationBeats: 0.5 },
        { note: "R", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "Eb5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "Eb5", durationBeats: 0.5 },
        { note: "Eb5", durationBeats: 0.5 },
        { note: "D5", durationBeats: 0.5 },
        { note: "C5", durationBeats: 0.5 },
        { note: "Bb4", durationBeats: 0.5 },
        { note: "Ab4", durationBeats: 1 },
        { note: "G4", durationBeats: 1 },
      ],
    },
    {
      waveform: "triangle",
      volume: 0.22,
      notes: [
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "Ab2", durationBeats: 0.5 },
        { note: "D3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 0.5 },
        { note: "Db3", durationBeats: 0.5 },
        { note: "G2", durationBeats: 1 },
        { note: "Db3", durationBeats: 1 },
        { note: "G2", durationBeats: 2 },
      ],
    },
    {
      waveform: "sawtooth",
      volume: 0.09,
      notes: [
        { note: "G3", durationBeats: 8 },
        { note: "Db4", durationBeats: 8 },
      ],
    },
  ],
};
