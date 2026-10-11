import { noteNameToMidi } from "./note";
import { REST, type NoteEvent, type Track } from "./score";
import { characteristicSemis, scalePitchClasses, scaleSemis, type Scale } from "./scales";

/**
 * 旋律が選んだ音階からはみ出していないかの点検（2026-10-11、docs/sound/scales-world-guide.md 提案 2・3）。
 * 警告は日本語の文章で、小節番号つき。入力の間違いではなく、直すとよくなるヒント。
 */

/** 音階の点検から外す楽器（打楽器・低音・自然音・効果音）。 */
const SKIP_INSTRUMENTS = new Set(["kick", "snare", "hihat", "crash", "tom", "bass", "slap", "sub808", "wind", "rain", "stream", "bird", "crickets", "impact", "swoosh", "sfxUp", "sfxDown", "cowbell"]);
const SKIP_ROLE = /ベース|bass|ドローン|drone|伴奏|コード|chord/i;

/** 旋律として点検するパートか。 */
export function isMelodicTrack(t: { instrument?: string; role?: string }): boolean {
  if (t.instrument && SKIP_INSTRUMENTS.has(t.instrument)) return false;
  if (t.role && SKIP_ROLE.test(t.role)) return false;
  return true;
}

export interface ScaleCheckOptions {
  beatsPerBar: number;
  /** 転調（atBeat 以降は semitones 上がる）。上がったあとの主音で判定する。 */
  modulate?: { semitones: number; atBeat: number } | null;
  /** 音階外の割合（拍の重み）がこの値を超えたら警告。既定 0.1。 */
  maxOffRatio?: number;
}

interface Placed { n: NoteEvent; start: number; midi: number }
const place = (notes: NoteEvent[]): Placed[] => {
  const out: Placed[] = [];
  let at = 0;
  for (const n of notes) {
    if (n.note !== REST) out.push({ n, start: at, midi: noteNameToMidi(n.note) });
    at += n.durationBeats;
  }
  return out;
};
const isBent = (n: NoteEvent): boolean => !!(n.bend || n.scoop || n.fall);

/** 音階の点検。tracks は { role, instrument, notes }。返り値は警告の文章（なければ空）。 */
export function checkScaleUsage(tracks: (Pick<Track, "notes" | "instrument"> & { role?: string })[], scale: Scale, tonic: number, opts: ScaleCheckOptions): string[] {
  const warnings: string[] = [];
  const bpb = opts.beatsPerBar;
  const maxOff = opts.maxOffRatio ?? 0.1;
  const pcsAt = (beat: number): Set<number> => new Set(scalePitchClasses(scale, (tonic + (opts.modulate && beat >= opts.modulate.atBeat ? opts.modulate.semitones : 0) + 120) % 12));
  const base = pcsAt(0);
  const afterPcs = opts.modulate ? pcsAt(opts.modulate.atBeat) : base;
  const inScale = (beat: number, midi: number): boolean => ((opts.modulate && beat >= opts.modulate.atBeat ? afterPcs : base).has(midi % 12));
  const charPcs = characteristicSemis(scale).map((s) => (s + tonic) % 12);
  const augSteps = scaleSemis(scale).map(Math.round).filter((v, i, a) => (a[i + 1] ?? 12) - v === 3 && a.length === 7).length;
  tracks.forEach((t) => {
    if (!isMelodicTrack(t)) return;
    const label = t.role ?? t.instrument ?? "パート";
    const placed = place(t.notes);
    if (!placed.length) return;
    let total = 0;
    let off = 0;
    const offNames = new Map<string, number>();
    const headBars: number[] = [];
    let hasChar = charPcs.length === 0;
    const augPerBar = new Map<number, number>();
    placed.forEach((p, i) => {
      const dur = p.n.durationBeats;
      total += dur;
      const ok = inScale(p.start, p.midi);
      const bent = isBent(p.n);
      if (!ok && !bent) {
        off += dur;
        const nm = p.n.note.replace(/-?\d+$/, "");
        offNames.set(nm, (offNames.get(nm) ?? 0) + 1);
        if (Math.abs(p.start / bpb - Math.round(p.start / bpb)) < 1e-6) headBars.push(Math.round(p.start / bpb) + 1);
      }
      if (!hasChar && ok && (dur >= 1 || Math.abs(p.start / bpb - Math.round(p.start / bpb)) < 1e-6) && charPcs.includes(p.midi % 12)) hasChar = true;
      if (augSteps > 0 && i > 0) {
        const prev = placed[i - 1];
        if (Math.abs(p.midi - prev.midi) === 3 && inScale(p.start, p.midi) && inScale(prev.start, prev.midi) && prev.start + prev.n.durationBeats <= p.start + 1e-6) {
          // 音階の中で隣り合う 2 音の間（間に音階の音がない）なら増 2 度
          const lo = Math.min(p.midi, prev.midi);
          if (!inScale(p.start, lo + 1) && !inScale(p.start, lo + 2)) {
            const bar = Math.floor(p.start / bpb);
            augPerBar.set(bar, (augPerBar.get(bar) ?? 0) + 1);
          }
        }
      }
    });
    const ratio = total > 0 ? off / total : 0;
    if (ratio > maxOff) {
      const list = [...offNames.entries()].sort((a, b) => b[1] - a[1]).slice(0, 4).map(([n, c]) => `${n}×${c}`).join("・");
      warnings.push(`${label}: ${scale.name}（主音 ${noteNameOf(tonic)}）の外の音が拍の ${Math.round(ratio * 100)}% あります（${list}）。意図した経過音かブルーノートでなければ、音階の音にそろえてください`);
    }
    if (headBars.length) warnings.push(`${label}: 小節の頭に音階外の音があります（${[...new Set(headBars)].slice(0, 6).join("・")}小節目）。頭は音階の音（和音の音）にすると落ち着きます`);
    if (!hasChar && ratio <= 1) warnings.push(`${label}: ${scale.name}の特性音（${characteristicSemis(scale).map((s) => noteNameOf((s + tonic) % 12)).join("・")}）が、長い音にも小節の頭にもありません。色を出すなら、1 回は置いてください`);
    for (const [bar, c] of augPerBar) if (c > 2) warnings.push(`${label}: ${bar + 1}小節目に増2度の動きが ${c} 回あります（目安は 1 小節に 1〜2 回）`);
  });
  return warnings;
}

const NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];
const noteNameOf = (pc: number): string => NAMES[((pc % 12) + 12) % 12];
