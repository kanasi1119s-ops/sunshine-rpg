/**
 * 拍子の拡張（docs/sound/rhythm-groove-guide.md §10 提案6）。
 * - AIソングの `beats` を 2〜12 の整数にする（5拍子・9拍子・11拍子・12拍子など。4分音符を1拍と数える）。
 * - `grouping: [2,2,3]` のように、小節をまとまり（拍の数）に分ける。自動伴奏のドラムは、まとまりの頭にキック・スネア、ハットはまとまりの頭を強くする。
 * - `grouping: "auto"` なら、拍の数ごとの定番の分け方（5＝3+2、7＝2+2+3、9＝3+3+3、11＝3+3+3+2）。
 */
import { REST, type NoteEvent, type Track } from "./score";

export const MIN_BEATS = 2;
export const MAX_BEATS = 12;
export const BEATS_CHOICES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] as const;

const AUTO_GROUPING: Record<number, number[]> = {
  2: [1, 1], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [2, 2, 3], 8: [3, 3, 2], 9: [3, 3, 3], 10: [3, 3, 2, 2], 11: [3, 3, 3, 2], 12: [3, 3, 3, 3],
};

/** 拍の数ごとの定番の分け方。 */
export function defaultGrouping(beats: number): number[] {
  return [...(AUTO_GROUPING[beats] ?? [beats])];
}

/** 曲の beats が使える値か。 */
export function beatsOk(beats: unknown): boolean {
  const n = Number(beats);
  return Number.isInteger(n) && n >= MIN_BEATS && n <= MAX_BEATS;
}

/** grouping の指定を、確かめて配列にする。"auto" か数の並び。合計が beats と違う・読めないときは warnings に足して null。 */
export function parseGrouping(spec: unknown, beats: number, warnings: string[]): number[] | null {
  if (spec === undefined || spec === null || spec === false) return null;
  if (spec === "auto" || spec === true) return defaultGrouping(beats);
  if (!Array.isArray(spec) || spec.length === 0 || !spec.every((x) => Number.isFinite(Number(x)) && Number(x) >= 1 && Number(x) <= beats)) {
    warnings.push(`grouping は "auto" か [2,2,3] のような拍の数の並びです。使いませんでした`);
    return null;
  }
  const g = spec.map(Number);
  const sum = g.reduce((s, x) => s + x, 0);
  if (Math.abs(sum - beats) > 1e-9) {
    warnings.push(`grouping ${JSON.stringify(g)} の合計（${sum}）が beats（${beats}）と違います。使いませんでした`);
    return null;
  }
  return g;
}

/** まとまりの頭の拍位置。[2,2,3] → [0,2,4]。 */
export function groupStarts(grouping: readonly number[]): number[] {
  const out: number[] = [];
  let at = 0;
  for (const g of grouping) {
    out.push(at);
    at += g;
  }
  return out;
}

const hit = (dur: number, velocity?: number): NoteEvent => ({ note: "C2", durationBeats: dur, ...(velocity !== undefined && velocity !== 1 ? { velocity } : {}) });
const rest = (dur: number): NoteEvent => ({ note: REST, durationBeats: dur });

/**
 * まとまりに沿った1小節のドラム（8分の格子）。
 * キック＝奇数番目（1つめ・3つめ…）のまとまりの頭、スネア＝偶数番目のまとまりの頭、ハット＝8分で、まとまりの頭を強く。
 * 1つしかまとまりがない（3拍の1まとまりなど）ときは、キックの頭とスネアを最後の拍に。
 */
export function groupingBar(grouping: readonly number[], beats: number): Record<"kick" | "snare" | "hihat", NoteEvent[]> {
  const starts = groupStarts(grouping);
  const cells = Math.round(beats * 2);
  const kickAt = new Set<number>();
  const snareAt = new Set<number>();
  starts.forEach((s, i) => (i % 2 === 0 ? kickAt : snareAt).add(Math.round(s * 2)));
  if (starts.length === 1) snareAt.add(Math.round((beats - 1) * 2));
  const headAt = new Set(starts.map((s) => Math.round(s * 2)));
  const make = (on: (i: number) => number | null): NoteEvent[] => Array.from({ length: cells }, (_, i) => {
    const v = on(i);
    return v === null ? rest(0.5) : hit(0.5, v);
  });
  return {
    kick: make((i) => (kickAt.has(i) ? 1.2 : null)),
    snare: make((i) => (snareAt.has(i) ? 1.1 : null)),
    hihat: make((i) => (headAt.has(i) ? 1.3 : i % 2 === 1 ? 0.7 : 1)),
  };
}

/** 自動伴奏の kick・snare・hihat を、まとまりに沿ったパターンに入れ替える（長さはそのまま）。ほかのパートは変えない。 */
export function applyGroupingToDrums(tracks: Track[], grouping: readonly number[], beatsPerBar: number): Track[] {
  const bar = groupingBar(grouping, beatsPerBar);
  return tracks.map((t) => {
    if (t.instrument !== "kick" && t.instrument !== "snare" && t.instrument !== "hihat") return t;
    const total = t.notes.reduce((s, n) => s + n.durationBeats, 0);
    const bars = Math.round(total / beatsPerBar);
    if (bars < 1) return t;
    const one = bar[t.instrument];
    return { ...t, notes: Array.from({ length: bars }, () => one.map((n) => ({ ...n }))).flat() };
  });
}

/** 拍つきの音の列で、グループの頭の拍位置にアクセント（velocity 1.3）が付いているかの割合（検査用）。 */
export function accentOnGroupHeads(notes: readonly NoteEvent[], grouping: readonly number[], beatsPerBar: number): number {
  const heads = groupStarts(grouping);
  let at = 0, onHead = 0, headCount = 0;
  for (const n of notes) {
    const pos = at % beatsPerBar;
    if (n.note !== REST && heads.some((h) => Math.abs(h - pos) < 1e-6)) {
      headCount++;
      if ((n.velocity ?? 1) >= 1.2) onHead++;
    }
    at += n.durationBeats;
  }
  return headCount === 0 ? 0 : onHead / headCount;
}
