/**
 * キャビネット近似（cabApprox）: スピーカーの箱の「ものすごく複雑なEQの曲線」を、少数のバイクアッド（BiquadFilterNode）で近づける。
 * 外部のIR（音声ファイル）は使わない。考え方は `docs/sound/amp-sim-guide.md` §4。特定の機材の再現ではない（CLAUDE.md 1-1）。
 *
 * 要点: ローパスは1枚だと1オクターブで12dBしか落ちず、歪みの8〜12kHzの倍音が残って「ピー」「ジャリ」になる。
 * そこで、周波数を少しずつずらした2〜4枚を重ねて、実際のスピーカーのように急に落とす（`punk` と同じ方式）。
 */

/** 箱の性格。closed=締まる、open=開放的、dark=暗い（ジャズ・シューゲイザー向き）、bright=明るい（ファンク・クリーン向き）。 */
export type CabKind = "closed" | "open" | "dark" | "bright";
/** マイクの位置。center=正面で明るく直接的、edge=端寄りで暗く丸い、off=斜めで低音が増え暗く温かい、far=遠くで低音も高音も柔らかい。 */
export type MicPos = "center" | "edge" | "off" | "far";

export const CAB_KINDS: CabKind[] = ["closed", "open", "dark", "bright"];
export const MIC_POSITIONS: MicPos[] = ["center", "edge", "off", "far"];

export interface CabFilterSpec {
  type: "highpass" | "lowpass" | "peaking";
  freq: number;
  gain: number;
  q: number;
}

/** 箱ごとの目安（ローパスの中心、段数、低域の山、前に出る山の高さ）。 */
const KIND: Record<CabKind, { lp: number; stages: number; lowDb: number; presenceDb: number; mudDb: number }> = {
  closed: { lp: 4800, stages: 4, lowDb: 3, presenceDb: 2.5, mudDb: -2 },
  open: { lp: 5200, stages: 3, lowDb: 1.5, presenceDb: 2.5, mudDb: -1 },
  dark: { lp: 3600, stages: 4, lowDb: 2, presenceDb: 1.5, mudDb: -1.5 },
  bright: { lp: 5800, stages: 3, lowDb: 1.5, presenceDb: 3, mudDb: -1 },
};
/** マイク位置の補正（ローパスの倍率、前に出る山の増減dB、低域の山の増減dB、ハイパス、ローパスのQ）。 */
const MIC: Record<MicPos, { lpScale: number; presenceDb: number; lowDb: number; hp: number; lpQ: number }> = {
  center: { lpScale: 1.1, presenceDb: 0.5, lowDb: 0, hp: 90, lpQ: 0.7 },
  edge: { lpScale: 0.85, presenceDb: -2, lowDb: 0, hp: 90, lpQ: 0.7 },
  off: { lpScale: 0.75, presenceDb: -1.5, lowDb: 1.5, hp: 85, lpQ: 0.65 },
  far: { lpScale: 0.85, presenceDb: -2.5, lowDb: -1.5, hp: 110, lpQ: 0.55 },
};
/** ローパスを少しずつずらす倍率（そろえると共通のQで肩に山が出る）。 */
const LP_SPREAD = [0.92, 1.0, 1.1, 1.22];

/** 箱とマイク位置から、通すフィルターの並びを返す（Web Audio に依存しない純粋な関数）。 */
export function cabApproxSpec(kind: CabKind = "closed", mic: MicPos = "center"): CabFilterSpec[] {
  const k = KIND[kind];
  const m = MIC[mic];
  const list: CabFilterSpec[] = [
    { type: "highpass", freq: m.hp, gain: 0, q: 0.9 },
    { type: "peaking", freq: 110, gain: k.lowDb + m.lowDb, q: 1 },
    { type: "peaking", freq: 350, gain: k.mudDb, q: 0.8 },
    { type: "peaking", freq: 2800, gain: k.presenceDb + m.presenceDb, q: 1 },
  ];
  const stages = mic === "far" ? Math.min(k.stages, 3) : k.stages;
  for (let i = 0; i < stages; i++) list.push({ type: "lowpass", freq: Math.round(k.lp * m.lpScale * LP_SPREAD[i]), gain: 0, q: m.lpQ });
  // 7kHz付近の戻りを少し抑える（valvewizard 方式の浅いノッチ）
  list.push({ type: "peaking", freq: 7000, gain: -8, q: 1.5 });
  return list;
}
