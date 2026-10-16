// 楽譜の点検（score-check.mjs・score-facts.mjs）と、曲の設計図・新しさの検査（tools/composer/*.mjs）が共通で使う道具。
// AIソング形式のJSONを、拍の位置つきの音の並びにする。
import path from "path";
import { fileURLToPath } from "url";

export const NAMES = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };
export const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
export const BASS_INST = new Set(["bass", "slap", "sub808"]);
export const NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
// 楽器の音域（作曲ソフトの手引きの音域）
export const RANGE = {
  bass: ["E1", "G3"], slap: ["E1", "G3"], sub808: ["C1", "C3"], guitar: ["E2", "E5"], crunch: ["E2", "E5"],
  distGuitar: ["E2", "E4"], leadGuitar: ["E3", "E6"], echoGuitar: ["E3", "E6"], keys: ["C2", "C6"], harpsichord: ["C2", "C6"],
  strings: ["C2", "C7"], pad: ["C2", "C6"], choir: ["C3", "C6"], brass: ["E2", "C6"], lead: ["C3", "C7"], bell: ["C4", "C7"],
  sitar: ["C3", "C6"], koto: ["C3", "C6"], shamisen: ["C3", "C6"], banjo: ["C3", "C6"], harp: ["C2", "C7"], xylophone: ["C4", "C8"], glockenspiel: ["G5", "C8"], accordion: ["F2", "A6"], kalimba: ["C4", "C7"],
  panflute: ["C4", "C7"], shakuhachi: ["C4", "C6"], ocarina: ["C4", "C7"], fiddle: ["G3", "E6"], bagpipe: ["A3", "A5"], piano: ["A0", "C8"],
};

export function midi(name) {
  const m = /^([A-G])([#b]?)(-?\d)$/.exec(name);
  if (!m) return null;
  return 12 * (Number(m[3]) + 1) + NAMES[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
}
export const midiName = (n) => `${["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][((n % 12) + 12) % 12]}${Math.floor(n / 12) - 1}`;
export const pcName = (pc) => NOTE_NAMES[((pc % 12) + 12) % 12];

/** "Am7"・"G/B"・"Bm7b5"・"C6"・"D9"・"Cadd9" → { root, bass, pcs(Set), minor }。読めなければ null */
export function chordPcs(name) {
  const [head, bassTok] = String(name).split("/");
  const m = /^([A-G])([#b]?)(.*)$/.exec(head);
  if (!m) return null;
  const root = (NAMES[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0) + 12) % 12;
  const q = m[3];
  let iv = [0, 4, 7];
  if (/^(m|min)(?!aj)/.test(q)) iv = [0, 3, 7];
  if (q.startsWith("dim")) iv = [0, 3, 6];
  if (q.startsWith("aug")) iv = [0, 4, 8];
  if (/^m7b5|^m7\(b5\)|^m7-5/.test(q)) iv = [0, 3, 6];
  if (q.includes("sus4")) iv = [0, 5, 7];
  else if (q.includes("sus2")) iv = [0, 2, 7];
  if (q === "5") iv = [0, 7];
  if (/dim7/.test(q)) iv = [...iv, 9];
  else if (/m7b5|m7\(b5\)|m7-5/.test(q)) iv = [...iv, 10];
  else if (/maj[79]|\(maj7\)|M7/.test(q) || /^mmaj/.test(q)) iv = [...iv, 11];
  else if (/7/.test(q) || (/9/.test(q) && !/add9/.test(q))) iv = [...iv, 10];
  if (/6/.test(q) && !/dim|7/.test(q)) iv = [...iv, 9];
  if (/add9|9/.test(q)) iv = [...iv, 2];
  const bm = bassTok ? /^([A-G])([#b]?)$/.exec(bassTok) : null;
  const bass = bm ? (NAMES[bm[1]] + (bm[2] === "#" ? 1 : bm[2] === "b" ? -1 : 0) + 12) % 12 : root;
  const pcs = new Set(iv.map((x) => (root + x) % 12));
  pcs.add(bass);
  return { root, bass, pcs, minor: iv.includes(3) && !iv.includes(4) };
}

/** 音の列（"E5:1 D5:0.5! R:0.5 C5:2" とドラムの "g:X...x..."）を読む。戻り値は { notes: [{t, dur, name, pitch, mark}], total } */
export function parseNotes(str, drum = false) {
  const out = [];
  let t = 0;
  for (const tok of String(str ?? "").trim().split(/\s+/)) {
    if (!tok) continue;
    if (drum && /^g:/i.test(tok)) {
      for (const c of tok.slice(2)) { if (c !== "." && c !== "-") out.push({ t, dur: 0.25, name: "x", pitch: null, mark: "" }); t += 0.25; }
      continue;
    }
    const [n, d = ""] = tok.split(":");
    const m = /^(\d+(?:\.\d+)?)([!,'_~^/\\*]*)$/.exec(d);
    if (!m) continue;
    const dur = Number(m[1]);
    if (!(dur > 0)) continue;
    out.push({ t, dur, name: n, pitch: n === "R" || n === "r" ? null : midi(n), mark: m[2], rest: n === "R" || n === "r" });
    t += dur;
  }
  return { notes: out, total: t };
}

/** 曲の長さにそろえてくり返した、音のならび（休みは除く） */
export function expand(part, totalBeats) {
  const { notes, total } = parseNotes(part.notes, DRUMS.has(part.instrument));
  if (total <= 0) return [];
  const out = [];
  for (let base = 0; base < totalBeats - 1e-9; base += total) {
    for (const n of notes) if (base + n.t < totalBeats - 1e-9 && !n.rest) out.push({ ...n, t: base + n.t });
  }
  return out;
}

/** パート1つぶんの長さ（拍）。 */
export function partLength(part) {
  return parseNotes(part.notes, DRUMS.has(part.instrument)).total;
}

/** 小節ごとのコード名の並び（barsPerChord・repeats を展開）。「Am*2」などは prepareSong のあとで1小節ずつになっている前提。 */
export function barChords(song) {
  const toks = String(song.chords ?? "").trim().split(/[\s|]+/).filter(Boolean).map((t) => t.replace(/\*\d+$/, ""));
  const bpc = song.barsPerChord === 2 ? 2 : 1;
  const one = toks.flatMap((c) => Array(bpc).fill(c));
  const out = [];
  for (let r = 0; r < Math.max(1, Number(song.repeats) || 1); r++) out.push(...one);
  return out;
}

/** 旋律のパート（役割に「メロディ」「旋律」を含み、「重ね」「下で」でないもの。なければ lead 系の最初の1つ） */
export function melodyParts(song, seqOf) {
  const all = song.parts.map((p) => ({ ...p, seq: DRUMS.has(p.instrument) ? [] : seqOf(p).filter((n) => n.pitch !== null) })).filter((p) => p.seq.length);
  const byRole = all.filter((p) => /メロディ|旋律/.test(p.role ?? "") && !/重ね|下で/.test(p.role ?? ""));
  if (byRole.length) return byRole;
  const lead = all.find((p) => ["lead", "leadGuitar"].includes(p.instrument));
  return lead ? [lead] : [];
}

/** 主音とモード（長短）の推定。chords はコード名の並び。 */
export function estimateKey(chordNames) {
  const cs = chordNames.map(chordPcs).filter(Boolean);
  if (!cs.length) return null;
  const MAJ = [[0, "M"], [2, "m"], [4, "m"], [5, "M"], [7, "M"], [9, "m"], [11, "d"]];
  const MIN = [[0, "m"], [2, "d"], [3, "M"], [5, "m"], [7, "m"], [7, "M"], [8, "M"], [10, "M"]];
  const kind = (c) => (c.pcs.has((c.root + 3) % 12) && c.pcs.has((c.root + 6) % 12) && !c.pcs.has((c.root + 7) % 12) ? "d" : c.minor ? "m" : "M");
  let best = null;
  for (let t = 0; t < 12; t++) {
    for (const mode of ["major", "minor"]) {
      const set = mode === "major" ? MAJ : MIN;
      let score = 0;
      for (const c of cs) if (set.some(([o, k]) => (t + o) % 12 === c.root && (k === kind(c) || (k === "m" && kind(c) === "d")))) score++;
      score /= cs.length;
      if (cs[0].root === t && (kind(cs[0]) === "m") === (mode === "minor")) score += 0.25;
      if (cs[cs.length - 1].root === t) score += 0.1;
      if (!best || score > best.score + 1e-9) best = { tonic: t, minor: mode === "minor", score };
    }
  }
  return best && { tonic: best.tonic, minor: best.minor, label: `${pcName(best.tonic)}${best.minor ? "短調" : "長調"}` };
}

/** Am*2・sectionChords・modulate・loopTail を使う曲は、ゲームと同じ前処理（src/audio/song-plan.ts）をかけてから返す。使っていなければそのまま。 */
export async function prepareForCheck(song) {
  const uses = /\*\d/.test(song.chords ?? "") || song.sectionChords || song.modulate || song.loopTail;
  if (!uses) return song;
  const { createServer } = await import("vite");
  const root = path.resolve(fileURLToPath(new URL("../../", import.meta.url)));
  const server = await createServer({ root, configFile: false, logLevel: "silent", server: { middlewareMode: true, hmr: false }, appType: "custom" });
  try {
    const { prepareSong } = await server.ssrLoadModule("/src/audio/song-plan.ts");
    return prepareSong(song, []);
  } finally {
    await server.close();
  }
}
