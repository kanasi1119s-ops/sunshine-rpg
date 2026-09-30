import type { Instrument, Score, Track } from "./score";

/**
 * 「きれいな版」: 同じ曲を、歪みを使わないクリーントーンの、澄んだ音に作り直す（元の曲は変えない）。
 * - 歪んだ刻み・パワーコード（ディストーション・クランチ）は、クリーンギターの刻みに置きかえる
 * - リードギター・ベースも、クリーンのアンプで鳴らす（耳が痛くならない、なめらかな音）
 * - シンバル・ハイハットを少し控えめにし、曲全体にごく軽いコーラスとディレイをかけて、空気感を出す
 * ゲームの曲の一覧では、元の曲の ID に「-clean」を付けた別の曲として並ぶ（`catalog.ts`）。
 */
const DISTORTED: Instrument[] = ["distGuitar", "crunch"];
const CLEAN_AMP = { type: "clean" as const };

export function cleanEdition(score: Score): Score {
  const tracks: Track[] = score.tracks.map((t) => {
    const inst = t.instrument;
    const notes = t.notes.map((n) => ({ ...n }));
    if (inst && DISTORTED.includes(inst)) return { ...t, instrument: "guitar", amp: { ...CLEAN_AMP }, volume: Math.min(0.4, t.volume * 1.1), notes };
    if (inst === "leadGuitar") return { ...t, amp: { ...CLEAN_AMP, tone: -1 }, notes };
    if (inst === "guitar" || inst === "echoGuitar" || inst === "bass" || inst === "slap") return { ...t, amp: { ...CLEAN_AMP }, notes };
    if (inst === "crash") return { ...t, volume: t.volume * 0.85, notes };
    if (inst === "hihat") return { ...t, volume: t.volume * 0.9, notes };
    return { ...t, notes };
  });
  return { ...score, tracks, tone: "rock", fx: { chorus: 0.16, delay: { beats: 0.75, feedback: 0.22, mix: 0.09 }, ...(score.fx ?? {}) } };
}
