import { autoSections, type Section, type SectionKind, SECTION_KINDS } from "./arrangement";
import { expandForm, type FormFields } from "./form-helper";
import { expandLaps, type LapsFields } from "./laps";
import { getMotif, motifToNotes, spliceNotes } from "./motif";
import { sceneSections } from "./scene";
import { expandBars } from "./song-plan";

/**
 * 曲のJSONの「展開」の前処理（form → laps → 主題）。aiSongToScore の最初に呼ばれる。
 * どれも、書かなければ何も変えない（今までの曲に影響しない）。
 */
export interface ExpandFields extends FormFields, LapsFields {
  motifs?: unknown;
  scene?: string;
  bpm?: number;
}

const SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** 曲全体の小節数（sectionChords＋sections のときは sections の合計）。読めなければ 0。 */
export function totalBarsOf(song: { chords: string; barsPerChord: number; repeats: number; sections?: unknown; sectionChords?: unknown }): number {
  if (song.sectionChords && Array.isArray(song.sections)) return (song.sections as { bars?: unknown }[]).reduce((a, s) => a + Math.max(0, Math.round(Number(s?.bars)) || 0), 0);
  try { return expandBars(song.chords, song.barsPerChord === 2 ? 2 : 1).length * Math.max(1, Math.round(Number(song.repeats) || 1)); } catch { return 0; }
}

/** 最初のコードから、曲の主音と長短を推測する。 */
export function guessKey(chords: string): { key: string; mode: "major" | "minor" } {
  const first = chords.trim().split(/[\s|]+/)[0] ?? "C";
  const m = /^([A-G])([#b]?)(.*?)(?:\*\d+)?$/.exec(first.split("/")[0]);
  if (!m) return { key: "C", mode: "major" };
  const pc = ((PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0)) % 12 + 12) % 12;
  const key = m[2] === "b" ? ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"][pc] : SHARP[pc];
  return { key, mode: /^m(?!aj)/.test(m[3]) ? "minor" : "major" };
}

const OCTAVE_OF: Record<string, number> = { xylophone: 5, glockenspiel: 6, accordion: 4, bass: 2, slap: 2, sub808: 2, guitar: 4, crunch: 4, distGuitar: 3, leadGuitar: 4, piano: 4, keys: 4, strings: 4, pad: 4, choir: 4, brass: 4, harpsichord: 4, lead: 5, bell: 5, harp: 5, kalimba: 5, koto: 4, shamisen: 4 };

interface MotifRef { id: string; at?: unknown; offset?: unknown; key?: string; octave?: number; transform?: unknown; repeat?: unknown; fill?: unknown }

/** 主題（parts[].motif）を、その塊の頭から音列として差し込む。使った主題IDは motifs に足す。 */
export function expandMotifs<T extends ExpandFields>(song: T, warnings: string[] = []): T {
  if (!song || !Array.isArray(song.parts) || !song.parts.some((p) => p && (p as { motif?: unknown }).motif)) return song;
  const beats = Number(song.beats) || 4;
  const totalBars = totalBarsOf(song);
  if (!totalBars) return song;
  const total = totalBars * beats;
  let sections: Section[] | undefined;
  if (Array.isArray(song.sections)) sections = (song.sections as Section[]).filter((s) => SECTION_KINDS.includes(s?.kind as SectionKind));
  else if (song.sections === "auto") sections = autoSections(totalBars);
  else if (song.scene) sections = sceneSections(song.scene, totalBars);
  const starts: number[] = [];
  if (sections) { let b = 0; for (const s of sections) { starts.push(b); b += s.bars; } }
  const guess = guessKey(song.chords);
  const used = new Set<string>(Array.isArray(song.motifs) ? song.motifs.map(String) : []);

  const resolveAt = (at: unknown, where: string): { bar: number; end: number } | null => {
    if (typeof at === "number" && Number.isFinite(at)) return { bar: Math.round(at) - 1, end: totalBars };
    const s = String(at ?? "1").trim();
    const mb = /^(?:bar:)?(\d+)$/.exec(s);
    if (mb) return { bar: Number(mb[1]) - 1, end: totalBars };
    const mk = /^([a-z]+?)(\d*)$/.exec(s);
    if (mk && SECTION_KINDS.includes(mk[1] as SectionKind)) {
      if (!sections) { warnings.push(`${where}: at「${s}」を使うには sections（または scene）が必要です`); return null; }
      const nth = mk[2] ? Number(mk[2]) : 1;
      let seen = 0;
      for (let i = 0; i < sections.length; i++) if (sections[i].kind === mk[1] && ++seen === nth) return { bar: starts[i], end: starts[i] + sections[i].bars };
      warnings.push(`${where}: at「${s}」に当たるセクションがありません`);
      return null;
    }
    warnings.push(`${where}: at「${s}」が読めません（小節番号、"bar:17"、"chorus"、"chorus2" のように）`);
    return null;
  };

  const parts = song.parts.map((p, pi) => {
    const raw = (p as { motif?: unknown }).motif;
    if (!raw) return p;
    const refs = (Array.isArray(raw) ? raw : [raw]) as MotifRef[];
    let notes = String(p.notes ?? "");
    const where = `parts[${pi}]（${p.role ?? p.instrument}）の主題`;
    if (["kick", "snare", "hihat", "crash", "tom"].includes(String(p.instrument))) { warnings.push(`${where}: ドラムには主題を置けません`); return p; }
    for (const ref of refs) {
      if (!ref || typeof ref.id !== "string" || !getMotif(ref.id)) { warnings.push(`${where}: 主題「${String(ref?.id)}」が台帳にありません`); continue; }
      const pos = resolveAt(ref.at ?? 1, where);
      if (!pos) continue;
      const startBar = pos.bar + (Number(ref.offset) || 0);
      if (!(startBar >= 0 && startBar < totalBars)) { warnings.push(`${where}: 位置（${startBar + 1}小節目）が曲の範囲の外です`); continue; }
      const local: string[] = [];
      const one = motifToNotes(ref.id, {
        key: ref.key ?? guess.key,
        octave: ref.octave ?? OCTAVE_OF[String(p.instrument)] ?? 4,
        mode: guess.mode,
        transform: Array.isArray(ref.transform) ? ref.transform.map(String) : typeof ref.transform === "string" ? [ref.transform] : [],
      }, local);
      warnings.push(...local.map((x) => `${where}: ${x}`));
      const room = (Math.min(pos.end, totalBars) - startBar) * beats;
      const times = ref.fill === true ? Math.max(1, Math.floor(room / one.beats)) : Math.max(1, Math.min(32, Math.round(Number(ref.repeat) || 1)));
      let tokens: string[] = [], len = 0;
      for (let i = 0; i < times && len + one.beats <= total - startBar * beats + 1e-9; i++) { tokens = tokens.concat(one.tokens); len += one.beats; }
      if (!tokens.length) { warnings.push(`${where}: 主題（${one.beats}拍）が曲の残りに入りません`); continue; }
      if (len > room + 1e-9 && ref.at !== undefined && typeof ref.at === "string" && SECTION_KINDS.includes(ref.at.replace(/\d+$/, "") as SectionKind)) warnings.push(`${where}: 主題（${len}拍）が「${ref.at}」の長さ（${room}拍）をはみ出します`);
      notes = spliceNotes(notes, total, startBar * beats, tokens, len);
      used.add(ref.id);
    }
    return { ...p, notes };
  });
  return { ...song, parts, ...(used.size ? { motifs: [...used] } : {}) };
}

/** form → laps → 主題 の順に展開する。 */
export function expandSongExtras<T extends ExpandFields>(song: T, warnings: string[] = []): T {
  if (!song || typeof song !== "object") return song;
  return expandMotifs(expandLaps(expandForm(song, warnings), warnings), warnings);
}

