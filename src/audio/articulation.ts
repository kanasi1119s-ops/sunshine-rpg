import { noteNameToMidi } from "./note";
import { REST, type NoteEvent, type Track } from "./score";

/**
 * 奏法の自動付与（2026-10-11、docs/sound/instrument-realism-guide.md の提案 5）。
 * 楽器ごとの小さなルールを、seed つきで決定的に（同じ入力なら同じ結果）付ける。すでに指定のある音（強さ・長さ・ビブラートなど）は変えない。
 */

/** 0〜1 の疑似乱数（seed と添字から決まる）。 */
export function hash01(seed: string, i: number): number {
  let h = 2166136261 ^ i;
  for (let k = 0; k < seed.length; k++) h = Math.imul(h ^ seed.charCodeAt(k), 16777619);
  h ^= h >>> 15;
  h = Math.imul(h, 2246822519);
  h ^= h >>> 13;
  return ((h >>> 0) % 100000) / 100000;
}

const VIBRATO_INSTRUMENTS = new Set(["guitar", "leadGuitar", "strings", "brass", "lead"]);
const HAMMER_INSTRUMENTS = new Set(["guitar", "leadGuitar"]);
const MELODY_ROLE = /旋律|メロ|melody|lead|主役|歌/i;

/**
 * 1 つのパートの音の並びに奏法を付ける。
 * - guitar／leadGuitar／strings／brass／lead: 1.5 拍以上で、フレーズの最後（次が休符か終わり）の音に `~`（ビブラート）
 * - strings の旋律（役割に「旋律・メロディ」など）: 2 度以内で続く音に `_`（レガート）。内声には付けない
 * - guitar／leadGuitar: 短い（0.5 拍以内）上行・下行の 2 音は、50% の確率でハンマリング／プルオフ風に（2 音目を弱く、1 音目を `_`）
 * - slap: 拍頭に `!`、前の音よりオクターブ上の音に `'`
 */
export function autoArticulation(events: NoteEvent[], instrument: string, role = "", seed = ""): NoteEvent[] {
  const out = events.map((e) => ({ ...e }));
  const pitchOf = (e: NoteEvent): number => noteNameToMidi(e.note);
  let at = 0;
  const starts = out.map((e) => { const s = at; at += e.durationBeats; return s; });
  const contiguous = (i: number): boolean => i + 1 < out.length && out[i].note !== REST && out[i + 1].note !== REST;
  if (VIBRATO_INSTRUMENTS.has(instrument)) {
    out.forEach((e, i) => {
      if (e.note === REST || e.durationBeats < 1.5 || e.vibrato !== undefined || e.bend || e.fall) return;
      const next = out[i + 1];
      if (!next || next.note === REST) e.vibrato = 0.7;
    });
  }
  if (instrument === "strings" && MELODY_ROLE.test(role)) {
    out.forEach((e, i) => {
      if (!contiguous(i) || e.gate !== undefined) return;
      if (Math.abs(pitchOf(out[i + 1]) - pitchOf(e)) <= 2 && e.durationBeats >= 0.5) e.gate = 1.15;
    });
  }
  if (HAMMER_INSTRUMENTS.has(instrument)) {
    for (let i = 0; i + 1 < out.length; i++) {
      if (!contiguous(i)) continue;
      const a = out[i], b = out[i + 1];
      const d = Math.abs(pitchOf(b) - pitchOf(a));
      if (a.durationBeats > 0.5 || b.durationBeats > 0.5 || d < 1 || d > 4) continue;
      if (a.gate !== undefined || b.velocity !== undefined || b.gate !== undefined) continue;
      if (hash01(seed + instrument, i) < 0.5) {
        a.gate = 1.15;
        b.velocity = 0.7;
        i++; // 2 音目を次の組の 1 音目にしない
      }
    }
  }
  if (instrument === "slap") {
    let prev: number | null = null;
    out.forEach((e, i) => {
      if (e.note === REST) return;
      const m = pitchOf(e);
      if (prev !== null && m - prev === 12 && e.gate === undefined) e.gate = 0.4;
      else if (Math.abs(starts[i] - Math.round(starts[i])) < 1e-6 && e.velocity === undefined) e.velocity = 1.3;
      prev = m;
    });
  }
  return out;
}

const CHORD_ACCENT_INSTRUMENTS = new Set(["piano", "keys", "harp"]);

/**
 * ピアノ・エレピ・ハープの、同じ瞬間に始まる音（パートを重ねて和音にしたもの）の中の最高音を、旋律として少し強く（`!`）する。
 * flags[i] が true のパートだけが対象。すでに強さを指定した音は変えない。tracks を書き換えて返す。
 */
export function accentTopNotes(tracks: Track[], flags: boolean[]): Track[] {
  const byStart = new Map<string, { t: number; n: number; midi: number }[]>();
  tracks.forEach((t, ti) => {
    if (!flags[ti] || !t.instrument || !CHORD_ACCENT_INSTRUMENTS.has(t.instrument)) return;
    let at = 0;
    t.notes.forEach((n, ni) => {
      if (n.note !== REST) {
        const key = (Math.round(at * 1000) / 1000).toString();
        const list = byStart.get(key) ?? [];
        list.push({ t: ti, n: ni, midi: noteNameToMidi(n.note) });
        byStart.set(key, list);
      }
      at += n.durationBeats;
    });
  });
  const copies = new Map<number, NoteEvent[]>();
  for (const list of byStart.values()) {
    if (list.length < 2) continue;
    const top = list.reduce((a, b) => (b.midi > a.midi ? b : a));
    if (list.every((x) => x.midi === top.midi)) continue;
    const notes = copies.get(top.t) ?? tracks[top.t].notes.map((n) => ({ ...n }));
    if (notes[top.n].velocity === undefined) notes[top.n].velocity = 1.3;
    copies.set(top.t, notes);
  }
  return tracks.map((t, i) => (copies.has(i) ? { ...t, notes: copies.get(i)! } : t));
}
