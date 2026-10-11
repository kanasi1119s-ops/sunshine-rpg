/**
 * ドラムの積み残し（docs/sound/drum-genre-guide.md §10 の入れなかった／道具だけだったもの）。
 * - applyHihatSections：セクションごとのハイハットの型（hihatPattern を自動伴奏のハイハットに当てる）。
 * - applyTrapRolls：トラップのハイハットのロールを、小節末に自動で入れる（拍つきの音の列を直接書き換えるので、格子と混ぜる問題がない）。
 * - BOSS_PHASES／bossPhasePlan：ボス曲のフェーズ表（フェーズごとのテンポ上げ。テンポマップで実現）。
 */
import type { Section, SectionKind } from "./arrangement";
import { hihatPattern } from "./drum-genres";
import { REST, type NoteEvent, type Track } from "./score";
import type { TempoPoint } from "./tempo-map";

// ---- セクション別ハイハット -----------------------------------------

/** セクションの種類 → hihatPattern の section。 */
export function hatSectionOf(kind: SectionKind): "verse" | "pre" | "chorus" | undefined {
  switch (kind) {
    case "intro": case "verse": case "outro": case "tag": return "verse";
    case "pre": return "pre";
    case "chorus": case "drop": case "build": return "chorus";
    default: return undefined;
  }
}

/** 小節ごとの種類。sections を1小節ずつに広げる。 */
export function barKindsOf(sections: readonly Section[]): SectionKind[] {
  return sections.flatMap((s) => Array.from({ length: Math.max(0, Math.round(s.bars)) }, () => s.kind));
}

/** 自動伴奏のハイハットを、ジャンルの型でセクションごとに作り直す（verse＝4分、chorus＝16分に細かく、4小節ごとにオープン）。 */
export function applyHihatSections(tracks: Track[], sections: readonly Section[], beatsPerBar: number, genre: string): Track[] {
  const kinds = barKindsOf(sections);
  const cells = Math.round(beatsPerBar * 4);
  // 強さは 1 が標準の尺度（X＝1.0、x＝0.78、o＝0.56。genreSong の 100・78・56 を 100 で割った値。dynamics: "natural" が 1.5 超を 100 で割るのと同じ）
  const vel = (c: string): number | null => (c === "." || c === "-" ? null : c === "X" ? 1 : c === "o" ? 0.56 : 0.78);
  return tracks.map((t) => {
    if (t.instrument !== "hihat") return t;
    const total = t.notes.reduce((s, n) => s + n.durationBeats, 0);
    const bars = Math.round(total / beatsPerBar);
    if (bars < 1) return t;
    const notes: NoteEvent[] = [];
    for (let bar = 0; bar < bars; bar++) {
      const grid = hihatPattern(genre, bar, hatSectionOf(kinds[Math.min(bar, kinds.length - 1)] ?? "verse"));
      for (let i = 0; i < cells; i++) {
        const c = grid[i % grid.length];
        const v = vel(c);
        if (v === null) notes.push({ note: REST, durationBeats: 0.25 });
        else notes.push({ note: "F#2", durationBeats: 0.25, velocity: v, ...(c === "O" ? { open: true } : {}) });
      }
    }
    return { ...t, notes };
  });
}

// ---- トラップのロール ------------------------------------------------

export type RollKind = "triplet" | "thirtysecond" | "auto";
export interface TrapRollOptions {
  /** 何小節ごとの最後の小節に入れるか（既定 4）。 */
  every?: number;
  /** triplet＝最後の1拍が三連、thirtysecond＝最後の半拍が32分、auto＝交互。 */
  kind?: RollKind;
}

/** notes の [from, to) 拍を replacement に置き換える（またぐ音は切る）。 */
export function replaceBeatRange(notes: readonly NoteEvent[], from: number, to: number, replacement: readonly NoteEvent[]): NoteEvent[] {
  const out: NoteEvent[] = [];
  let at = 0;
  let inserted = false;
  const insert = (): void => { if (!inserted) { out.push(...replacement); inserted = true; } };
  for (const n of notes) {
    const s = at, e = at + n.durationBeats;
    at = e;
    if (e <= from + 1e-9) { out.push(n); continue; }
    if (s >= to - 1e-9) { insert(); out.push(n); continue; }
    if (s < from - 1e-9) out.push({ ...n, durationBeats: Math.round((from - s) * 1e6) / 1e6 });
    insert();
    if (e > to + 1e-9) out.push({ ...n, durationBeats: Math.round((e - to) * 1e6) / 1e6 });
  }
  insert();
  return out;
}

function rollNotes(kind: "triplet" | "thirtysecond", base: number): NoteEvent[] {
  const hit = (d: number, v: number): NoteEvent => ({ note: "F#2", durationBeats: d, velocity: Math.round(v * 1000) / 1000 });
  // 中の音は弱く、最後の1発は強く（トラップのロールの山谷）
  if (kind === "triplet") return [hit(0.3333, base * 0.7), hit(0.3333, base * 0.7), hit(0.3334, base * 1.3)];
  return [hit(0.125, base * 0.6), hit(0.125, base * 0.7), hit(0.125, base * 0.8), hit(0.125, base * 1.3)];
}

/** ハイハットの代表の強さ（休符を除く強さの中央値。無ければ1）。 */
function baseVelocity(notes: readonly NoteEvent[]): number {
  const v = notes.filter((n) => n.note !== REST).map((n) => n.velocity ?? 1).sort((a, b) => a - b);
  return v.length ? v[Math.floor(v.length / 2)] : 1;
}

/** ハイハットのパートの、小節末（every 小節ごとの最後の小節の最後の1拍／半拍）にロールを入れる。 */
export function applyTrapRolls(tracks: Track[], beatsPerBar: number, options: TrapRollOptions = {}): Track[] {
  const every = Math.max(1, Math.round(options.every ?? 4));
  const kind = options.kind ?? "auto";
  return tracks.map((t) => {
    if (t.instrument !== "hihat") return t;
    const total = t.notes.reduce((s, n) => s + n.durationBeats, 0);
    const bars = Math.round(total / beatsPerBar);
    const base = baseVelocity(t.notes);
    let notes = t.notes as NoteEvent[];
    let count = 0;
    for (let bar = every - 1; bar < bars; bar += every) {
      const k: "triplet" | "thirtysecond" = kind === "auto" ? (count % 2 === 0 ? "triplet" : "thirtysecond") : kind;
      const end = (bar + 1) * beatsPerBar;
      const from = k === "triplet" ? end - 1 : end - 0.5;
      notes = replaceBeatRange(notes, from, end, rollNotes(k, base));
      count++;
    }
    return count ? { ...t, notes } : t;
  });
}

// ---- ボス曲のフェーズ表 ---------------------------------------------

export interface BossPhase {
  id: string;
  label: string;
  /** フェーズの始まり（曲全体の長さに対する割合 0〜1。いちばん近いセクションの頭にそろえる）。 */
  at: number;
  /** テンポの倍率（基準のテンポに掛ける）。 */
  bpmScale: number;
  /** 聴こえ方の目安（文書用）。 */
  note: string;
}

/** 3段（山を3回作る）のフェーズ表。docs/sound/rhythm-groove-guide.md §8 と scene.ts の boss に合わせた出発点。 */
export const BOSS_PHASES: readonly BossPhase[] = [
  { id: "p1", label: "第1形態", at: 0, bpmScale: 1, note: "基準のテンポ。ハイハットは8分、サビで16分に細かく" },
  { id: "p2", label: "第2形態", at: 0.3, bpmScale: 1.05, note: "5%速く。ハットが密になり、ギターの刻みが増える" },
  { id: "p3", label: "最終形態", at: 0.65, bpmScale: 1.1, note: "10%速く。全員で押し切る。曲の終わりでは基準のテンポに戻してループへ" },
];

export interface BossPlanOptions {
  /** 上書きするフェーズ表（`[{ at: 0.4, bpmScale: 1.08 }]` のように、bar（1始まり）でも指定できる）。 */
  phases?: { at?: number; bar?: number; bpmScale: number }[];
  /** 最後の2小節で基準のテンポに戻す（既定 true。ループの継ぎ目をなめらかに）。 */
  loopBack?: boolean;
}

export interface BossPlan {
  tempo: TempoPoint[];
  /** フェーズごとの始まりの小節（0始まり）とテンポ。 */
  phases: { bar: number; bpm: number; label: string }[];
}

/** セクションの頭の小節（0始まり）。 */
function sectionStarts(sections: readonly Section[]): number[] {
  const out: number[] = [];
  let at = 0;
  for (const s of sections) {
    out.push(at);
    at += Math.max(0, Math.round(s.bars));
  }
  return out;
}

/**
 * ボス曲のフェーズ表から、テンポマップを作る。フェーズの頭は、いちばん近いセクションの頭にそろえる（sections が無ければ4小節の頭）。
 * 最後の2小節で基準のテンポへ戻す（loopBack）。
 */
export function bossPhasePlan(bpm: number, totalBars: number, beatsPerBar: number, sections?: readonly Section[], options: BossPlanOptions = {}): BossPlan {
  const starts = sections && sections.length ? sectionStarts(sections) : Array.from({ length: Math.ceil(totalBars / 4) }, (_, i) => i * 4);
  const snap = (bar: number): number => starts.reduce((best, s) => (Math.abs(s - bar) < Math.abs(best - bar) ? s : best), 0);
  const list: { at?: number; bar?: number; bpmScale: number }[] = options.phases && options.phases.length ? options.phases : BOSS_PHASES.map((p) => ({ at: p.at, bpmScale: p.bpmScale }));
  const tempo: TempoPoint[] = [];
  const phases: BossPlan["phases"] = [];
  let lastBar = -1;
  list.forEach((p, i) => {
    const raw = p.bar !== undefined ? p.bar - 1 : Math.round((p.at ?? 0) * totalBars);
    const bar = i === 0 ? 0 : snap(Math.max(0, Math.min(totalBars - 1, raw)));
    if (bar <= lastBar) return;
    lastBar = bar;
    const scale = Math.max(0.5, Math.min(2, Number(p.bpmScale) || 1));
    const label = BOSS_PHASES[i]?.label ?? `第${i + 1}段`;
    phases.push({ bar, bpm: Math.round(bpm * scale * 100) / 100, label });
    if (bar > 0 || scale !== 1) tempo.push({ beat: bar * beatsPerBar, bpm: bpm * scale });
  });
  if (options.loopBack !== false && totalBars >= 4 && tempo.length) {
    const from = (totalBars - 2) * beatsPerBar;
    if (from > (tempo[tempo.length - 1].beat ?? 0)) tempo.push({ beat: from, bpm, ramp: 2 * beatsPerBar });
  }
  return { tempo, phases };
}
