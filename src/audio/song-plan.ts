/**
 * 曲の前処理（2026-10-11、docs/sound/chord-theory-deep.md の提案 3・4・8・10）。
 * AIソング形式の次の書き方を、ふつうの形（コードを1小節ずつ並べた chords・barsPerChord 1・repeats 1）に直してから、組み立てに渡す。
 *   - chords の「Am*2」: そのコードを2小節続ける（コードごとの長さ。*N は小節数）
 *   - sectionChords: セクションごとの進行（{ verse: "C Am F G", chorus: "F G Em Am" }）。sections を配列で書いたときだけ効く
 *   - modulate: { atBar: 17, semitones: 1 } … atBar 小節目（1から数える）以降のコードと、ドラム以外のパートの音を半音数だけ移す
 *   - loopTail: "dominant" | "deceptive" … 最後の小節のコードを V7（頭へ戻りたくなる）か vi（偽終止）に置き換える
 * どれも書かなければ、何も変えずにそのまま返す（今までの曲に影響しない）。
 */
import { midiToName } from "./compose";
import { noteNameToMidi } from "./note";
import type { SectionKind } from "./arrangement";

export interface PlanFields {
  chords: string;
  barsPerChord: number;
  repeats: number;
  beats: number;
  sections?: unknown;
  sectionChords?: Record<string, string>;
  modulate?: { atBar?: number; at?: string; semitones: number };
  loopTail?: "deceptive" | "dominant";
  parts: { instrument: string; notes: string }[];
}

const DRUM_SET = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
const SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"];

/** 進行の文字列を、1小節ごとのコード名の並びにする。「Am*2」は2小節、そうでなければ barsPerChord 小節。 */
export function expandBars(text: string, barsPerChord: number): string[] {
  const out: string[] = [];
  for (const tok of text.split(/[\s|]+/).filter(Boolean)) {
    const m = /^(.+?)\*(\d+)$/.exec(tok);
    const name = m ? m[1] : tok;
    const n = m ? Number(m[2]) : Math.max(1, barsPerChord);
    if (!(n >= 1 && n <= 32)) throw new Error(`コードの小節数は1〜32にしてください「${tok}」`);
    for (let i = 0; i < n; i++) out.push(name);
  }
  return out;
}

/** コード名を半音だけ移す（分数コードの低音も）。読めなければそのまま返す。 */
export function transposeChord(name: string, semitones: number): string {
  const one = (s: string, rest: boolean): string => {
    const m = /^([A-G])([#b]?)(.*)$/.exec(s);
    if (!m || (!rest && m[3])) return s;
    const pc = (((PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + semitones) % 12) + 12) % 12;
    return (m[2] === "b" ? FLAT : SHARP)[pc] + (rest ? m[3] : "");
  };
  const [head, bass, ...extra] = name.split("/");
  if (extra.length) return name;
  return bass === undefined ? one(head, true) : `${one(head, true)}/${one(bass, false)}`;
}

function tonicOf(chord: string): { root: number; minor: boolean } | null {
  const m = /^([A-G])([#b]?)(.*)$/.exec(chord.split("/")[0]);
  if (!m) return null;
  return { root: (PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12, minor: /^m(?!aj)/.test(m[3]) };
}

function transposeNotes(notes: string, beatsPerBar: number, fromBar: number, total: number, semitones: number, warnings: string[], where: string): string {
  const toks = notes.trim().split(/\s+/).filter(Boolean);
  const dur = (t: string): number => { const m = /:(\d+(?:\.\d+)?)/.exec(t); return m ? Number(m[1]) : 0; };
  const len = toks.reduce((s, t) => s + dur(t), 0);
  if (!(len > 0)) return notes;
  const out: string[] = [];
  let pos = 0;
  const from = (fromBar - 1) * beatsPerBar;
  let bad = 0;
  for (let i = 0; pos < total - 1e-9; i++) {
    const t = toks[i % toks.length];
    const d = dur(t);
    if (!(d > 0)) { if (i > toks.length * 2) break; continue; }
    const [name, ...rest] = t.split(":");
    if (pos >= from - 1e-9 && /^[A-G][#b]?-?\d$/.test(name)) {
      try {
        const m = noteNameToMidi(name) + semitones;
        if (m < 12 || m > 108) throw new Error("range");
        out.push([midiToName(m), ...rest].join(":"));
      } catch { bad++; out.push(t); }
    } else out.push(t);
    pos += d;
  }
  if (bad) warnings.push(`${where}: 転調で音域の外に出る音が${bad}個あったので、その音は移していません`);
  return out.join(" ");
}

/** 上の書き方をふつうの形に直す。warnings に注意を足す。何も使っていなければ、同じものをそのまま返す。 */
export function prepareSong<T extends PlanFields>(song: T, warnings: string[] = []): T {
  if (!song || typeof song !== "object" || typeof song.chords !== "string") return song;
  const uses = /\*\d/.test(song.chords) || song.sectionChords || (song.modulate && song.modulate.atBar !== undefined) || song.loopTail;
  if (!uses) return song;
  const bpc = song.barsPerChord === 2 ? 2 : 1;
  let bars: string[];
  if (song.sectionChords && typeof song.sectionChords === "object" && Array.isArray(song.sections)) {
    bars = [];
    const seen: Record<string, number> = {};
    (song.sections as { kind: SectionKind; bars: number }[]).forEach((x, i) => {
      const kind = String(x?.kind ?? "verse");
      const n = Math.round(Number(x?.bars));
      if (!(n >= 1)) return;
      seen[kind] = (seen[kind] ?? 0) + 1;
      const text = song.sectionChords![seen[kind] > 1 ? `${kind}${seen[kind]}` : kind] ?? song.sectionChords![kind] ?? song.chords;
      const pat = expandBars(String(text), bpc);
      if (!pat.length) throw new Error(`sectionChords の「${kind}」(sections[${i}]) が空です`);
      for (let b = 0; b < n; b++) bars.push(pat[b % pat.length]);
    });
    if (song.repeats > 1) warnings.push("sectionChords を使うときは sections の小節数の合計が曲の長さになるので、repeats は使われません");
  } else {
    if (song.sectionChords) warnings.push("sectionChords は、sections を配列（{kind, bars} の並び）で書いたときだけ効きます。chords をそのまま使いました");
    const one = expandBars(song.chords, bpc);
    bars = [];
    for (let r = 0; r < Math.max(1, Math.round(Number(song.repeats) || 1)); r++) bars.push(...one);
  }
  if (!bars.length) throw new Error("chords: コード進行を入力してください");

  if (song.loopTail && bars.length >= 2) {
    const t = tonicOf(bars[0]);
    if (t && (song.loopTail === "dominant" || song.loopTail === "deceptive")) {
      const names = SHARP;
      const flat = [5, 10, 3, 8, 1].includes(t.root) && !t.minor || [2, 7, 0, 5, 10].includes(t.root) && t.minor;
      const nm = (pc: number): string => (flat ? FLAT : names)[(pc + 12) % 12];
      bars[bars.length - 1] = song.loopTail === "dominant" ? `${nm(t.root + 7)}7` : t.minor ? nm(t.root + 8) : `${nm(t.root + 9)}m`;
    } else if (song.loopTail) warnings.push(`loopTail は "dominant" か "deceptive" にしてください（${String(song.loopTail)}）`);
  }

  let parts = song.parts;
  const mod = song.modulate && song.modulate.atBar !== undefined ? song.modulate : undefined; // at: "lastChorus" などは arrangement 側で処理
  if (mod) {
    const atBar = Math.round(Number(mod.atBar)), semi = Math.round(Number(mod.semitones));
    if (!(atBar >= 2 && atBar <= bars.length) || !(semi !== 0 && Math.abs(semi) <= 12)) {
      warnings.push(`modulate は atBar が2〜${bars.length}（1から数える）、semitones が -12〜12（0以外）の整数にしてください。転調しませんでした`);
    } else {
      for (let i = atBar - 1; i < bars.length; i++) bars[i] = transposeChord(bars[i], semi);
      const total = bars.length * Number(song.beats);
      parts = song.parts.map((p, i) => (DRUM_SET.has(p?.instrument) || (p as { modulate?: boolean })?.modulate === false || typeof p?.notes !== "string" ? p : { ...p, notes: transposeNotes(p.notes, Number(song.beats), atBar, total, semi, warnings, `parts[${i}]`) }));
    }
  }
  const out = { ...song, chords: bars.join(" "), barsPerChord: 1, repeats: 1, parts };
  if (mod) delete out.modulate; // atBar はここで展開済み（arrangement で二重に移さない）
  return out;
}
