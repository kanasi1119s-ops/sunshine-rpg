import motifFile from "../../docs/sound/data/motifs.json";
import { midiToName } from "./compose";

/**
 * 主題台帳と度数ヘルパ（docs/sound/form-structure-guide.md §12 の提案6・7、game-music-guide.md §4）。
 * 主題は「度数＋リズム」で持つので、どの調・どの音域でも書ける。台帳は docs/sound/data/motifs.json。
 * 度数の書き方（長音階が基準）: "1"〜"7"、前に b か # で半音、後ろに ' で1オクターブ上・, で1オクターブ下、R は休み。
 * 変形（transform）: augment（音価2倍）・diminish（半分）・invert（反行）・retrograde（逆行）・head／tail（前半／後半。head:2 のように音数も）・
 *   transpose:N（度数でNだけ移す）・octave:N・mode:minor／mode:major（3・6・7度を半音下げる／戻す）。
 * 曲のJSONでは parts[].motif に { "id": "akari", "at": "chorus", "transform": ["diminish"] } と書くと、その塊の頭から主題の音列が置かれる（song-expand.ts）。
 */
export interface MotifDef {
  id: string;
  name: string;
  meaning: string;
  degrees: string[];
  rhythm: number[];
  baseKey: string;
  baseBpm: number;
  mode: "major" | "minor";
  variantOf?: string;
  where?: string;
  note?: string;
}

export const MOTIFS: MotifDef[] = (motifFile as unknown as { motifs: MotifDef[] }).motifs;
export const MOTIF_IDS: string[] = MOTIFS.map((m) => m.id);
export function getMotif(id: string): MotifDef | undefined {
  return MOTIFS.find((m) => m.id === id);
}

const MAJOR = [0, 2, 4, 5, 7, 9, 11];
const PC: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

export interface MotifStep {
  /** 音階上の位置（0＝主音、7＝1オクターブ上の主音）。休みは null。 */
  idx: number | null;
  /** 半音の増減（b＝-1、#＝+1、短調化など）。 */
  alt: number;
  beats: number;
}

/** 度数の文字を読む。読めなければ null。 */
export function parseDegree(text: string): { idx: number | null; alt: number } | null {
  const s = String(text).trim();
  if (s.toUpperCase() === "R") return { idx: null, alt: 0 };
  const m = /^([b#]?)([1-7])([',]*)$/.exec(s);
  if (!m) return null;
  const oct = (m[3].match(/'/g) ?? []).length - (m[3].match(/,/g) ?? []).length;
  return { idx: Number(m[2]) - 1 + 7 * oct, alt: m[1] === "b" ? -1 : m[1] === "#" ? 1 : 0 };
}

/** 台帳の定義を、変形の前の音の並び（MotifStep）にする。 */
export function baseSteps(def: MotifDef): MotifStep[] {
  return def.degrees.map((d, i) => {
    const p = parseDegree(d);
    if (!p) throw new Error(`主題「${def.id}」の度数「${d}」が読めません`);
    return { idx: p.idx, alt: p.alt, beats: Number(def.rhythm[i] ?? def.rhythm[def.rhythm.length - 1] ?? 1) };
  });
}

export interface MotifOptions {
  /** 主音（C・F#・Bb など）。省略は台帳の baseKey。 */
  key?: string;
  /** 主音のオクターブ（4＝C4 が中央のド）。省略は4。 */
  octave?: number;
  /** 曲の長短。minor なら 3・6・7度を半音下げる。省略は major。 */
  mode?: "major" | "minor";
  transform?: string[];
}

const minorize = (s: MotifStep): MotifStep => (s.idx !== null && s.alt === 0 && [2, 5, 6].includes(((s.idx % 7) + 7) % 7) ? { ...s, alt: -1 } : s);
const majorize = (s: MotifStep): MotifStep => (s.idx !== null && s.alt === -1 && [2, 5, 6].includes(((s.idx % 7) + 7) % 7) ? { ...s, alt: 0 } : s);

/** 変形を順に当てる。 */
export function applyTransforms(steps: MotifStep[], transforms: string[], warnings: string[] = []): MotifStep[] {
  let out = steps.map((s) => ({ ...s }));
  for (const raw of transforms) {
    const [name, argRaw] = String(raw).split(":");
    const arg = argRaw === undefined ? undefined : Number(argRaw);
    switch (name) {
      case "augment": out = out.map((s) => ({ ...s, beats: s.beats * 2 })); break;
      case "diminish": out = out.map((s) => ({ ...s, beats: s.beats / 2 })); break;
      case "invert": {
        const pivot = out.find((s) => s.idx !== null)?.idx;
        if (pivot === undefined || pivot === null) break;
        out = out.map((s) => (s.idx === null ? s : { ...s, idx: 2 * pivot - s.idx, alt: -s.alt }));
        break;
      }
      case "retrograde": out = [...out].reverse(); break;
      case "head": { const n = arg && arg >= 1 ? Math.round(arg) : Math.ceil(out.length / 2); out = out.slice(0, n); break; }
      case "tail": { const n = arg && arg >= 1 ? Math.round(arg) : Math.floor(out.length / 2); out = out.slice(Math.max(0, out.length - n)); break; }
      case "transpose": out = out.map((s) => (s.idx === null ? s : { ...s, idx: s.idx + Math.round(arg ?? 0) })); break;
      case "octave": out = out.map((s) => (s.idx === null ? s : { ...s, idx: s.idx + 7 * Math.round(arg ?? 0) })); break;
      case "mode": {
        if (argRaw === "minor") out = out.map(minorize);
        else if (argRaw === "major") out = out.map(majorize);
        else warnings.push(`変形「${raw}」: mode:minor か mode:major と書いてください`);
        break;
      }
      default: warnings.push(`変形「${raw}」は使えません（augment・diminish・invert・retrograde・head・tail・transpose:N・octave:N・mode:minor）。無視しました`);
    }
  }
  return out;
}

const fmt = (x: number): string => String(Math.round(x * 10000) / 10000);

/** 休みの音符（1つの音符は64拍までなので、長いときは分ける）。 */
export function restTokens(beats: number): string[] {
  const out: string[] = [];
  let left = beats;
  while (left > 1e-9) { const d = Math.min(32, left); out.push(`R:${fmt(d)}`); left -= d; }
  return out;
}

/** 主題を音名:拍の並びにする。 */
export function motifToNotes(id: string, opts: MotifOptions = {}, warnings: string[] = []): { tokens: string[]; beats: number } {
  const def = getMotif(id);
  if (!def) throw new Error(`主題「${id}」が台帳（docs/sound/data/motifs.json）にありません（${MOTIF_IDS.join("・")}）`);
  const m = /^([A-G])([#b]?)$/.exec(opts.key ?? def.baseKey);
  if (!m) throw new Error(`主題の key「${String(opts.key)}」は C・F#・Bb のように書いてください`);
  const tonic = 12 * (Math.round(opts.octave ?? 4) + 1) + PC[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
  let steps = baseSteps(def);
  if (opts.mode === "minor") steps = steps.map(minorize);
  steps = applyTransforms(steps, opts.transform ?? [], warnings);
  const tokens: string[] = [];
  let beats = 0;
  for (const s of steps) {
    if (s.idx === null) tokens.push(`R:${fmt(s.beats)}`);
    else {
      const midi = tonic + 12 * Math.floor(s.idx / 7) + MAJOR[((s.idx % 7) + 7) % 7] + s.alt;
      if (midi < 12 || midi > 108) { warnings.push(`主題「${id}」の音が音域の外に出たので休みにしました（${midi}）`); tokens.push(`R:${fmt(s.beats)}`); }
      else tokens.push(`${midiToName(midi)}:${fmt(s.beats)}`);
    }
    beats += s.beats;
  }
  return { tokens, beats };
}

// ───────── 手書きの音の並びに、主題を差し込む ─────────
const TOKEN = /^([^:]+):(\d+(?:\.\d+)?)(.*)$/;

/** notes（音名:拍の並び。曲の長さより短ければくり返す）の startBeat から、主題の音を差し込んだ新しい notes を返す。 */
export function spliceNotes(notes: string, total: number, startBeat: number, motifTokens: string[], motifBeats: number): string {
  const toks = notes.trim().split(/\s+/).filter(Boolean);
  const before: string[] = [], after: string[] = [];
  const end = startBeat + motifBeats;
  let pos = 0;
  const hasDur = toks.some((t) => TOKEN.test(t));
  for (let i = 0; hasDur && pos < total - 1e-9 && i < 200000; i++) {
    const tok = toks[i % toks.length];
    const m = TOKEN.exec(tok);
    if (!m) continue;
    const d = Number(m[2]);
    if (!(d > 0)) continue;
    const a = pos, z = pos + d;
    if (z <= startBeat + 1e-9) before.push(tok);
    else if (a >= end - 1e-9) after.push(tok);
    else {
      if (a < startBeat - 1e-9) { if (/^r$/i.test(m[1])) before.push(...restTokens(startBeat - a)); else before.push(`${m[1]}:${fmt(startBeat - a)}${m[3]}`); }
      if (z > end + 1e-9) after.push(...restTokens(z - end));
    }
    pos = z;
  }
  if (!hasDur) { if (startBeat > 1e-9) before.push(...restTokens(startBeat)); if (total - end > 1e-9) after.push(...restTokens(total - end)); }
  else if (pos < startBeat - 1e-9) before.push(...restTokens(startBeat - pos));
  return [...before, ...motifTokens, ...after].join(" ");
}

// ───────── 台帳（使用一覧） ─────────
export interface MotifUse { id: string; at?: string | number; transform: string[] }

/** 曲のJSONから、使っている主題を集める（parts[].motif と、曲の motifs の一覧）。 */
export function motifUses(song: { motifs?: unknown; parts?: unknown }): MotifUse[] {
  const out: MotifUse[] = [];
  const add = (x: unknown): void => {
    if (!x || typeof x !== "object") return;
    const o = x as { id?: unknown; at?: unknown; transform?: unknown };
    if (typeof o.id !== "string") return;
    out.push({ id: o.id, at: typeof o.at === "string" || typeof o.at === "number" ? o.at : undefined, transform: Array.isArray(o.transform) ? o.transform.map(String) : [] });
  };
  if (Array.isArray(song.parts)) for (const p of song.parts as { motif?: unknown }[]) { if (Array.isArray(p?.motif)) p.motif.forEach(add); else add(p?.motif); }
  if (Array.isArray(song.motifs)) for (const id of song.motifs) if (typeof id === "string" && !out.some((u) => u.id === id)) out.push({ id, transform: [] });
  return out;
}

export interface LedgerSong { name: string; uses: MotifUse[] }

/** 台帳と曲の食い違いなどの注意。 */
export function checkLedger(songs: LedgerSong[], catalog: MotifDef[] = MOTIFS): string[] {
  const w: string[] = [];
  const ids = new Set(catalog.map((m) => m.id));
  for (const s of songs) for (const u of s.uses) if (!ids.has(u.id)) w.push(`曲「${s.name}」が使っている主題「${u.id}」が台帳にありません`);
  for (const m of catalog) if (!songs.some((s) => s.uses.some((u) => u.id === m.id))) w.push(`主題「${m.id}」（${m.name}）を使っている曲がありません`);
  if (songs.length >= 4) {
    const withMotif = songs.filter((s) => s.uses.length).length;
    if (withMotif < songs.length / 2) w.push(`主題の断片がある曲が ${withMotif}/${songs.length} 曲です。半分程度の曲に断片を入れると、世界が一つに聞こえます`);
    if (withMotif === songs.length && catalog.length >= 2 && new Set(songs.flatMap((s) => s.uses.map((u) => u.id))).size === 1) w.push("全部の曲が同じ主題だけです。主題を使い分けてください");
  }
  // 同じ主題が、続く曲で同じ変形（なし含む）のまま
  const last = new Map<string, string>();
  for (const s of songs) {
    for (const u of s.uses) {
      const key = u.transform.join(",") || "（変形なし）";
      if (last.get(u.id) === key && songs.indexOf(s) > 0) w.push(`主題「${u.id}」が、前に使った曲に続いて「${s.name}」でも同じ変形（${key}）です。1〜2軸は変えてください`);
      last.set(u.id, key);
    }
  }
  return w;
}

/** 台帳（docs/sound/motif-ledger.md）の中身。 */
export function ledgerMarkdown(songs: LedgerSong[], catalog: MotifDef[] = MOTIFS): string {
  const lines: string[] = [
    "# 主題の使用一覧（自動で作った表）",
    "",
    "`node tools/composer/song.mjs motif-ledger` が、`assets-src/ai-songs/*.json` の `parts[].motif` と `motifs` から作ります。手で直さないでください（台帳の本体は `docs/sound/data/motifs.json`）。",
    "",
    "| 主題 | 意味 | 度数 | リズム（拍） | 使った曲と変形 |",
    "|---|---|---|---|---|",
  ];
  for (const m of catalog) {
    const used = songs.filter((s) => s.uses.some((u) => u.id === m.id)).map((s) => `${s.name}（${s.uses.filter((u) => u.id === m.id).map((u) => u.transform.join("+") || "原型").join("／")}）`);
    lines.push(`| ${m.id}（${m.name}） | ${m.meaning} | ${m.degrees.join(" ")} | ${m.rhythm.join(" ")} | ${used.join("、") || "（まだなし）"} |`);
  }
  const w = checkLedger(songs, catalog);
  lines.push("", "## 注意", "", ...(w.length ? w.map((x) => `- ${x}`) : ["- なし"]), "");
  return lines.join("\n");
}
