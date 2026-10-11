import { INTRO_TYPES, OUTRO_TYPES } from "./song-meta";

/**
 * 導入・終わりの型の記録と重複チェック（docs/sound/form-structure-guide.md §12 の提案5）。
 * 曲のJSONの introType（I1〜I10）・outroType（E1〜E10）を、直前の3曲と比べて、同じ型が続いたら注意する。
 * 型を書いていない曲は、導入は音の並びから「推測」する（inferIntroType）。終わりは書いてあるものだけを見る（推測しない）。
 * 書いていない曲同士は何も言わない（型の記録がない曲は無警告）。
 */
export interface TypedSong {
  name: string;
  introType?: string;
  outroType?: string;
  /** 型を推測するための曲のJSON（parts・beats・sections）。 */
  song?: { beats?: number; parts?: { instrument?: string; notes?: string }[]; sections?: unknown; chords?: string; barsPerChord?: number; repeats?: number };
}

const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const TOKEN = /^([^:]+):(\d+(?:\.\d+)?)/;

function firstBars(notes: string, bars: number, beatsPerBar: number): { t: number; d: number; name: string }[] {
  const out: { t: number; d: number; name: string }[] = [];
  const limit = bars * beatsPerBar;
  let pos = 0;
  const toks = notes.trim().split(/\s+/).filter(Boolean);
  for (let i = 0; pos < limit - 1e-9 && i < 5000; i++) {
    const tok = toks[i % Math.max(1, toks.length)];
    if (/^g:/i.test(tok ?? "")) {
      // ドラムのグリッド記法は 1文字＝0.25拍
      for (const c of tok.slice(2)) { if (pos >= limit) break; if (/[xXoO]/.test(c)) out.push({ t: pos, d: 0.25, name: "x" }); pos += 0.25; }
      continue;
    }
    const m = tok ? TOKEN.exec(tok) : null;
    if (!m) { if (i > toks.length * 2) break; continue; }
    const d = Number(m[2]);
    if (!(d > 0)) continue;
    if (m[1] !== "R" && m[1] !== "r") out.push({ t: pos, d, name: m[1] });
    pos += d;
  }
  return out;
}

/** 導入の型を、曲の最初の2小節の鳴り方から推測する。決められなければ undefined。 */
export function inferIntroType(song: NonNullable<TypedSong["song"]>): string | undefined {
  const beats = Number(song.beats) || 4;
  const parts = (song.parts ?? []).filter((p) => typeof p?.notes === "string");
  if (!parts.length) return undefined;
  if (Array.isArray(song.sections) && (song.sections as { kind?: string; bars?: number }[])[0]?.kind === "chorus" && Number((song.sections as { bars?: number }[])[0].bars) <= 4) return "I3";
  const ev = parts.map((p) => ({ p, e: firstBars(p.notes!, 2, beats) }));
  const active1 = ev.filter((x) => x.e.some((n) => n.t < beats));
  const active2 = ev.filter((x) => x.e.length);
  const n = ev.length;
  if (!active1.length && active2.length / n >= 0.6) return "I4";
  if (n >= 3 && active1.length / n >= 0.8) return "I1";
  if (active2.length && active2.every((x) => DRUMS.has(String(x.p.instrument)))) return "I6";
  if (active2.length === 1) {
    const x = active2[0];
    const mean = x.e.reduce((s, q) => s + q.d, 0) / x.e.length;
    return mean >= beats * 0.75 ? "I5" : "I2";
  }
  if (active2.length / n <= 0.45) return "I9";
  return undefined;
}

export interface TypeRepeat { kind: "intro" | "outro"; type: string; with: string; inferred: boolean }

/** 新しい曲の型を、直前の曲（新しい順）と比べる。 */
export function findTypeRepeats(current: TypedSong, recent: TypedSong[]): TypeRepeat[] {
  const out: TypeRepeat[] = [];
  const intro = (s: TypedSong): { type?: string; inferred: boolean } => (s.introType ? { type: s.introType, inferred: false } : { type: s.song ? inferIntroType(s.song) : undefined, inferred: true });
  const me = intro(current);
  for (const r of recent) {
    const o = intro(r);
    if (me.type && o.type && me.type === o.type) out.push({ kind: "intro", type: me.type, with: r.name, inferred: me.inferred || o.inferred });
    if (current.outroType && r.outroType && current.outroType === r.outroType) out.push({ kind: "outro", type: current.outroType, with: r.name, inferred: false });
  }
  return out;
}

export function typeWarnings(current: TypedSong, recent: TypedSong[]): string[] {
  return findTypeRepeats(current, recent).map((r) => {
    const label = r.kind === "intro" ? INTRO_TYPES[r.type] : OUTRO_TYPES[r.type];
    return `${r.kind === "intro" ? "導入" : "終わり"}の型が直前の曲「${r.with}」と同じです（${r.type}: ${label}${r.inferred ? "。音の並びからの推測を含む" : ""}）。直前の3曲と違う型にすると、毎日の曲の個性が出ます（form-structure-guide.md §6・§7）`;
  });
}

/** tracks.md の「| ID | 導入の型 | 終わりの型 |」の表を読む。空欄は無視。 */
export function readTrackTypes(markdown: string): TypedSong[] {
  const out: TypedSong[] = [];
  let inTable = false;
  for (const line of markdown.split("\n")) {
    if (/^\|\s*ID\s*\|\s*導入の型\s*\|\s*終わりの型\s*\|/.test(line)) { inTable = true; continue; }
    if (!inTable) continue;
    if (!line.startsWith("|")) { inTable = false; continue; }
    const cells = line.split("|").slice(1, -1).map((c) => c.trim());
    if (cells.length < 3 || /^-+$/.test(cells[0]) || /^:?-+:?$/.test(cells[0])) continue;
    const intro = /^I(10|[1-9])$/i.test(cells[1]) ? cells[1].toUpperCase() : undefined;
    const outro = /^E(10|[1-9])$/i.test(cells[2]) ? cells[2].toUpperCase() : undefined;
    if (cells[0] && (intro || outro)) out.push({ name: cells[0], introType: intro, outroType: outro });
  }
  return out;
}
