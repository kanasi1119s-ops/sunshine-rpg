import type { AiPart } from "./ai-song";
import { SECTION_KINDS, SECTION_LABELS, transposeNoteName, type Section, type SectionKind } from "./arrangement";
import type { ExpandCtx } from "./part-expand";
import { noteNameToMidi } from "./note";
import { PART_RECIPES } from "./sound-sets";

/**
 * 2020年代J-POPのクリーンギターの音づくり・編曲の提案を実装したもの（2026-10-11、docs/sound/jpop-clean-guitar-guide.md の「実装状況」）。
 * どれも書いたパートにだけ効く（書かなければ今までの曲は変わらない）。part-expand.ts の expandParts から呼ばれる。
 *   recipe（名前付きの音づくり・提案 PART_RECIPES）／widen "dimension"（提案4）／sectionFx（提案5）／guitarPair（提案8）／
 *   bare（提案9）／pattern "cut16"（提案6）／reverbPre（提案12）。echo の ms・slap（提案3）は part-expand.ts の expandEcho。
 */

// ───────── 型・スキーマ ─────────
export interface WidenSpec {
  mode?: "dimension";
  /** 片側を遅らせる量（ミリ秒。5〜20。省略は 12）。 */
  ms?: number;
  /** 左右に振る量（0〜0.7。省略は 0.6。モノラルで痩せないよう 0.7 を上限にする）。 */
  width?: number;
  /** 遅らせた側にかける浅い chorus（0〜0.5。省略は 0.25）。 */
  chorus?: number;
}
export interface SectionFxSpec {
  reverb?: number;
  chorus?: number;
  bright?: number;
}
export interface GuitarPairSpec {
  /** 2本目の役: crunch＝浅いクランチの小音量／octave＝1オクターブ上のクリーン。省略は crunch。 */
  mode?: "crunch" | "octave";
  /** 2本目が鳴るセクションの種類。省略は ["chorus"]。 */
  only?: SectionKind[];
  /** 2本目の音量（0.02〜0.2。省略は 1本目の半分、上限 0.1）。 */
  volume?: number;
}
export type BareSpec = "mute" | "hold" | { mode?: "mute" | "hold"; kinds?: SectionKind[] };

export interface AiPartJpop {
  /** 名前付きの音づくり（PART_RECIPES のキー。sparkle-delay・crystal-wide・sparkle-wide-delay・jpop-arpeggio など）。amp が auto でなければ amp は書いた方を使い、reverb・chorus・bright・duck・sustain・echo・doubleDetune・widen は書いていないときだけ補う。 */
  recipe?: string;
  /** "dimension"＝ディメンションC型の広がり。同じ旋律を左右に置き、片側を 5〜20ms 遅らせて浅い chorus を掛ける。 */
  widen?: "dimension" | WidenSpec;
  /** セクションごとの残響・chorus・明るさ。{ intro: {reverb:0.4, chorus:0.4}, chorus: {reverb:0.15, chorus:0.05} }。曲の sections（または scene）が必要。 */
  sectionFx?: Partial<Record<SectionKind, SectionFxSpec>>;
  /** 2本目のギター。true か { mode, only, volume }。1本目は左・chorus、2本目は右で、指定したセクション（省略はサビ）だけ鳴る。 */
  guitarPair?: true | GuitarPairSpec;
  /** 引き算のセクション（曲の bare で指定したセクション。省略は Aメロ）でのふるまい。mute＝休む／hold＝各小節の最初の音だけを小節いっぱいにのばす（ルートだけ）。 */
  bare?: BareSpec;
  /** リバーブのプリディレイ（ミリ秒 0〜120。"room"＝10、"ballad"＝70）。本物のプリディレイではなく、遅らせた小さな複製に残響を載せて近づける。 */
  reverbPre?: number | "room" | "ballad";
  /** pattern: "cut16" の格子（16文字。X＝強く弾く・のばす、x＝弾いて切る、o＝弱い消す音、-＝前の音をのばす、.＝休み＝消す音）か名前（pop・sparse・drive）。 */
  cutGrid?: string;
}
export interface AiSongJpop {
  /** 引き算のセクション（true は Aメロ）。自動の伴奏はベース・鍵盤・ギター・弦が小節の頭の音だけをのばす。手書きのパートは parts[].bare で出し入れ。 */
  bare?: SectionKind[] | true;
}

const rec = { type: "object" } as const;
export const AI_PART_JPOP_SCHEMA = {
  recipe: { type: "string" },
  widen: { anyOf: [{ type: "string", enum: ["dimension"] }, rec] },
  sectionFx: rec,
  guitarPair: { anyOf: [{ type: "boolean" }, rec] },
  bare: { anyOf: [{ type: "string", enum: ["mute", "hold"] }, rec] },
  reverbPre: { anyOf: [{ type: "number" }, { type: "string", enum: ["room", "ballad"] }] },
  cutGrid: { type: "string" },
} as const;
export const AI_SONG_JPOP_SCHEMA = {
  bare: { anyOf: [{ type: "boolean" }, { type: "array", items: { type: "string", enum: SECTION_KINDS } }] },
} as const;

const clamp = (v: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, v));
const r3 = (v: number): number => Math.round(v * 1000) / 1000;
const num = (v: unknown): number | null => (v !== undefined && v !== null && v !== "" && Number.isFinite(Number(v)) ? Number(v) : null);
const nameOfPart = (p: AiPart): string => String(p.role ?? p.instrument);
/** ミリ秒を拍にする。 */
export const msToBeats = (ms: number, bpm: number): number => Math.round((ms / 1000) * (bpm / 60) * 1e6) / 1e6;

// ───────── 名前付きの音づくり（recipe） ─────────
/** recipe を AiPart に当てる。書いてある項目は変えず、書いていない項目だけ補う。 */
export function applyRecipe(p: AiPart, warnings: string[]): AiPart {
  if (p.recipe === undefined) return p;
  const { recipe, ...rest } = p;
  const r = PART_RECIPES[String(recipe)];
  if (!r) {
    warnings.push(`parts（${nameOfPart(p)}）: recipe「${String(recipe)}」は PART_RECIPES にありません（${Object.keys(PART_RECIPES).join("・")}）。無視しました`);
    return rest as AiPart;
  }
  const out: Record<string, unknown> = { ...rest };
  if ((out.amp === undefined || out.amp === "auto") && r.mix.amp && r.mix.amp.type !== "auto") out.amp = r.mix.amp.type;
  for (const k of ["reverb", "chorus", "bright", "duck"] as const) if (out[k] === undefined && r.mix[k] !== undefined) out[k] = r.mix[k];
  if (out.sustain === undefined && r.hint?.sustain !== undefined) out.sustain = r.hint.sustain;
  const fx = r.fx;
  if (fx) {
    if (out.echo === undefined && fx.echo) out.echo = { ...fx.echo };
    if (out.doubleDetune === undefined && fx.doubleDetune) out.doubleDetune = { ...fx.doubleDetune };
    if (out.widen === undefined && fx.widen) out.widen = { ...fx.widen };
  }
  return out as unknown as AiPart;
}

// ───────── ディメンションC型の広がり（widen） ─────────
export function expandWiden(p: AiPart, spec: "dimension" | WidenSpec, ctx: ExpandCtx): AiPart[] {
  const s: WidenSpec = spec === "dimension" ? {} : spec;
  const ms = clamp(num(s.ms) ?? 12, 5, 20);
  const width = clamp(num(s.width) ?? 0.6, 0, 0.7);
  const chorus = clamp(num(s.chorus) ?? 0.25, 0, 0.5);
  const { widen: _w, ...base } = p;
  const pan0 = Number(p.pan) || 0;
  const vol = Math.max(0.02, r3((Number(p.volume) || 0.2) * 0.75));
  const shift = r3((Number(p.shift) || 0) + msToBeats(ms, ctx.bpm));
  return [
    { ...base, role: `${nameOfPart(p)}・L`, volume: vol, pan: clamp(pan0 - width, -1, 1) } as AiPart,
    { ...base, role: `${nameOfPart(p)}・R`, volume: vol, pan: clamp(pan0 + width, -1, 1), shift, chorus: Math.max(Number(p.chorus) || 0, chorus) } as AiPart,
  ];
}

// ───────── セクション別のエフェクト量（sectionFx） ─────────
/** その部屋の分だけ、セクションの種類ごとに音量の倍率 0／1 のマスクを作る（書いてあった sections の指定は、鳴らす側にそのまま残す）。 */
function maskFor(p: AiPart, kinds: SectionKind[], on: SectionKind[]): NonNullable<AiPart["sections"]> {
  const prior = (p.sections ?? {}) as Record<string, unknown>;
  const out: Record<string, unknown> = { ...prior };
  for (const k of kinds) out[k] = on.includes(k) ? (prior[k] ?? 1) : 0;
  return out as NonNullable<AiPart["sections"]>;
}

export function expandSectionFx(p: AiPart, spec: Partial<Record<SectionKind, SectionFxSpec>>, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const { sectionFx: _s, ...base } = p;
  const where = `parts（${nameOfPart(p)}）の sectionFx`;
  if (!spec || typeof spec !== "object") return [base as AiPart];
  const sections: Section[] = ctx.sections ?? [];
  if (!sections.length) {
    warnings.push(`${where}: 曲の sections（または scene）が必要です。sectionFx は使わず、パートの reverb・chorus のままにしました`);
    return [base as AiPart];
  }
  const kinds = [...new Set(sections.map((s) => s.kind))];
  for (const k of Object.keys(spec)) if (!SECTION_KINDS.includes(k as SectionKind)) warnings.push(`${where}: 「${k}」は使えません（${SECTION_KINDS.join("・")}）。無視しました`);
  const fxOf = (kind: SectionKind): SectionFxSpec => {
    const o = (spec[kind] ?? {}) as SectionFxSpec;
    const reverb = num(o.reverb) ?? num(p.reverb);
    const chorus = num(o.chorus) ?? num(p.chorus);
    const bright = num(o.bright) ?? num(p.bright);
    return {
      ...(reverb !== null ? { reverb: clamp(reverb, 0, 1) } : {}),
      ...(chorus !== null ? { chorus: clamp(chorus, 0, 1) } : {}),
      ...(bright !== null ? { bright: clamp(bright, -1, 0.5) } : {}),
    };
  };
  const groups = new Map<string, { fx: SectionFxSpec; kinds: SectionKind[] }>();
  for (const kind of kinds) {
    const fx = fxOf(kind);
    const key = JSON.stringify(fx);
    const g = groups.get(key);
    if (g) g.kinds.push(kind);
    else groups.set(key, { fx, kinds: [kind] });
  }
  if (groups.size === 1) return [{ ...base, ...[...groups.values()][0].fx } as AiPart];
  return [...groups.values()].map((g) => ({
    ...base,
    ...g.fx,
    role: `${nameOfPart(p)}・${g.kinds.map((k) => SECTION_LABELS[k]).join("")}`,
    sections: maskFor(p, kinds, g.kinds),
  }) as AiPart);
}

// ───────── 2本目のギターの役割分担（guitarPair） ─────────
/** 音の並びの全部の音を半音ずらす。上限（maxMidi）をこえる音は動かさない。 */
export function transposeNotesText(notes: string, semitones: number, maxMidi = 127): string {
  return notes.trim().split(/\s+/).filter(Boolean).map((tok) => {
    const i = tok.indexOf(":");
    const name = i < 0 ? tok : tok.slice(0, i);
    if (!/^[A-G][#b]?-?\d$/.test(name)) return tok;
    const moved = transposeNoteName(name, semitones);
    let ok = true;
    try { ok = noteNameToMidi(moved) <= maxMidi; } catch { ok = false; }
    return (ok ? moved : name) + (i < 0 ? "" : tok.slice(i));
  }).join(" ");
}

export function expandGuitarPair(p: AiPart, spec: true | GuitarPairSpec, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const s: GuitarPairSpec = spec === true ? {} : spec;
  const { guitarPair: _g, ...base } = p;
  const where = `parts（${nameOfPart(p)}）の guitarPair`;
  const mode = s.mode === "octave" ? "octave" : "crunch";
  const only = (Array.isArray(s.only) && s.only.length ? s.only : ["chorus"]).filter((k): k is SectionKind => SECTION_KINDS.includes(k as SectionKind));
  const side = clamp(Math.abs(Number(p.pan) || 0) || 0.5, 0.3, 0.7);
  const kinds = [...new Set((ctx.sections ?? []).map((x) => x.kind))];
  if (!kinds.length) warnings.push(`${where}: 曲の sections（または scene）がないので、2本目は全体で鳴ります（サビだけにするには sections が必要です）`);
  const vol = clamp(num(s.volume) ?? Math.min(0.1, (Number(p.volume) || 0.16) * 0.5), 0.02, 0.2);
  const first: AiPart = { ...base, role: `${nameOfPart(p)}・クリーン`, pan: -side, chorus: num(p.chorus) ?? 0.3 } as AiPart;
  const second: AiPart = {
    ...base,
    role: `${nameOfPart(p)}・${mode === "crunch" ? "クランチ" : "オクターブ上"}`,
    pan: side,
    volume: r3(vol),
    chorus: 0,
    ...(mode === "crunch" ? { instrument: "crunch", amp: "crunch", sustain: p.sustain ?? 1.2 } : { notes: transposeNotesText(String(p.notes ?? ""), 12, noteNameToMidi("E5")) }),
    ...(kinds.length ? { sections: maskFor(p, kinds, only) } : {}),
  } as AiPart;
  return [first, second];
}

// ───────── リバーブのプリディレイ（reverbPre） ─────────
const PREDELAY_NAMES: Record<string, number> = { room: 10, ballad: 70 };

/**
 * 録音音源の残響の送りには、プリディレイの調整がない。そこで、元のパートは残響なし（直接音）にし、
 * 遅らせた小さな複製（音量 0.3 倍・暗め）に残響を載せる。5〜15ms は厚み、40〜100ms は奥行きの合図として聞こえる近似で、本物のプリディレイではない。
 */
export function expandReverbPre(p: AiPart, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const { reverbPre: raw, ...base } = p;
  const ms = typeof raw === "string" ? PREDELAY_NAMES[raw] : num(raw);
  if (ms === undefined || ms === null || !Number.isFinite(ms)) {
    warnings.push(`parts（${nameOfPart(p)}）: reverbPre は 0〜120 のミリ秒か "room"・"ballad" にしてください（${String(raw)}）。無視しました`);
    return [base as AiPart];
  }
  const delay = clamp(ms, 0, 120);
  if (delay <= 0) return [base as AiPart];
  const wetReverb = clamp((num(p.reverb) ?? 0.35) + 0.25, 0.3, 1);
  return [
    { ...base, reverb: 0 } as AiPart,
    {
      ...base,
      role: `${nameOfPart(p)}・残響`,
      volume: Math.max(0.02, r3((Number(p.volume) || 0.2) * 0.3)),
      reverb: wetReverb,
      bright: clamp((Number(p.bright) || 0) - 0.3, -1, 0.5),
      shift: r3((Number(p.shift) || 0) + msToBeats(delay, ctx.bpm)),
      chorus: 0,
    } as AiPart,
  ];
}

// ───────── 引き算のセクション（bare） ─────────
interface Tok { name: string; dur: number; marks: string }
const TOK = /^(\d+(?:\.\d+)?)(.*)$/;

/** 音の並びを、ちょうど total 拍まで広げた token の並びにする（短ければくり返し、長ければ切る）。ドラムのグリッド記法は扱わない。 */
function tokensOf(notes: string, total: number): Tok[] | null {
  const raw: Tok[] = [];
  for (const t of notes.trim().split(/\s+/).filter(Boolean)) {
    const i = t.indexOf(":");
    if (i < 0) return null;
    const m = TOK.exec(t.slice(i + 1));
    if (!m) return null;
    raw.push({ name: t.slice(0, i), dur: Number(m[1]), marks: m[2] });
  }
  const len = raw.reduce((s, e) => s + e.dur, 0);
  if (!raw.length || !(len > 0)) return null;
  const out: Tok[] = [];
  let at = 0;
  for (let i = 0; at < total - 1e-6 && i < 100000; i++) {
    const e = raw[i % raw.length];
    const dur = Math.min(e.dur, total - at);
    out.push({ ...e, dur: Math.round(dur * 1e6) / 1e6 });
    at += dur;
  }
  return out;
}
const fmtTok = (t: Tok): string => `${t.name}:${String(Math.round(t.dur * 1e6) / 1e6)}${t.marks}`;

/** 引き算の小節（[from,to) 拍）の音を、各小節の最初の音だけを小節いっぱいにのばす形にする。 */
export function holdFirstNotes(notes: string, total: number, beatsPerBar: number, ranges: [number, number][]): string | null {
  const toks = tokensOf(notes, total);
  if (!toks) return null;
  const inRange = (beat: number): [number, number] | undefined => ranges.find(([a, b]) => beat >= a - 1e-9 && beat < b - 1e-9);
  // 小節の境目で音を割る
  const split: (Tok & { at: number })[] = [];
  let at = 0;
  for (const t of toks) {
    let left = t.dur;
    let pos = at;
    while (left > 1e-9) {
      const barEnd = (Math.floor(pos / beatsPerBar + 1e-9) + 1) * beatsPerBar;
      const d = Math.min(left, barEnd - pos);
      split.push({ ...t, dur: d, at: pos });
      pos += d;
      left -= d;
    }
    at += t.dur;
  }
  const out: Tok[] = [];
  const seenBar = new Set<number>();
  for (const e of split) {
    const range = inRange(e.at);
    const bar = Math.floor(e.at / beatsPerBar + 1e-9);
    if (!range) { out.push(e); continue; }
    if (seenBar.has(bar)) continue;
    seenBar.add(bar);
    // その小節の最初の音（休み以外）を小節いっぱいに。小節の頭が休みなら、その小節は休み
    const first = split.find((x) => Math.floor(x.at / beatsPerBar + 1e-9) === bar && x.name !== "R" && x.name !== "r");
    out.push(first ? { name: first.name, dur: beatsPerBar, marks: first.marks.replace(/['!,]/g, "") } : { name: "R", dur: beatsPerBar, marks: "" });
  }
  return out.map(fmtTok).join(" ");
}

/** パートの bare が指す引き算のセクション。曲の bare を書いてあれば jpop-feel.ts の前処理がここに入れる。なければ Aメロ。 */
export function bareKindsOf(p: AiPart): SectionKind[] {
  const b = p.bare;
  const own = b && typeof b === "object" && Array.isArray(b.kinds) ? b.kinds.filter((k) => SECTION_KINDS.includes(k)) : [];
  return own.length ? own : ["verse"];
}

/** パートの bare を実行する。mute は sections のマスク、hold は音の並びの書き換え。 */
export function expandBare(p: AiPart, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const { bare, ...base } = p;
  const mode = typeof bare === "string" ? bare : bare && typeof bare === "object" ? bare.mode ?? "mute" : "mute";
  const where = `parts（${nameOfPart(p)}）の bare`;
  if (mode !== "mute" && mode !== "hold") {
    warnings.push(`${where}: mute か hold にしてください（${String(mode)}）。無視しました`);
    return [base as AiPart];
  }
  const sections = ctx.sections ?? [];
  if (!sections.length) {
    warnings.push(`${where}: 曲の sections（または scene）が必要です。bare は使いませんでした`);
    return [base as AiPart];
  }
  const kinds = bareKindsOf(p);
  const present = [...new Set(sections.map((s) => s.kind))];
  if (mode === "mute") {
    const bareHere = present.filter((k) => kinds.includes(k));
    if (!bareHere.length) return [base as AiPart];
    return [{ ...base, sections: maskFor(p, present, present.filter((k) => !kinds.includes(k))) } as AiPart];
  }
  // hold: bare のセクションの範囲（拍）を求め、各小節の最初の音をのばす
  const ranges: [number, number][] = [];
  let at = 0;
  for (const s of sections) {
    const end = at + s.bars * ctx.beatsPerBar;
    if (kinds.includes(s.kind)) ranges.push([at, end]);
    at = end;
  }
  if (!ranges.length) return [base as AiPart];
  const held = holdFirstNotes(String(p.notes ?? ""), ctx.totalBeats, ctx.beatsPerBar, ranges);
  if (held === null) {
    warnings.push(`${where}: notes を読めなかったので hold は使いませんでした`);
    return [base as AiPart];
  }
  return [{ ...base, notes: held } as AiPart];
}

// ───────── 消す音付きのカッティング（pattern: "cut16"） ─────────
/** 名前付きの格子（16文字＝16分音符16個。4拍子のとき）。X＝強く弾く（つづく - までのばす）、x＝弾いて切る、o＝弱い消す音、-＝前の音をのばす、.＝休み。 */
export const CUT16_GRIDS: Record<string, string> = {
  pop: "X-..x.ox..x.o.x.",
  sparse: "X---..x...o.x...",
  drive: "x.ox.xo.X-.x.xo.",
};
export const CUT16_DEFAULT = "pop";
const GRID_CHARS = /^[XxOo\-.]+$/;

/** 格子を、1小節ぶん（stepsPerBar ステップ）に合わせる（短ければくり返し、長ければ切る）。 */
function fitGrid(grid: string, steps: number): string {
  let g = "";
  while (g.length < steps) g += grid;
  return g.slice(0, steps);
}

/** 型の名前 cut16 を、和音の構成音（上の3声）のパートに展開する。voicingOf は part-expand の strumVoicing。 */
export function expandCut16(
  p: AiPart, ctx: ExpandCtx, warnings: string[], voicingOf: (chord: string, strings: number) => number[] | null,
): AiPart[] {
  const { pattern: _p, cutGrid, ...base } = p;
  const where = `parts（${nameOfPart(p)}）の cut16`;
  const gridText = cutGrid === undefined ? CUT16_GRIDS[CUT16_DEFAULT] : CUT16_GRIDS[String(cutGrid)] ?? String(cutGrid).replace(/\s+/g, "");
  if (!gridText || !GRID_CHARS.test(gridText)) {
    warnings.push(`${where}: cutGrid は X x o - . だけで書くか、名前（${Object.keys(CUT16_GRIDS).join("・")}）にしてください「${String(cutGrid)}」。cut16 は使いませんでした`);
    return [{ ...base, pattern: undefined } as AiPart];
  }
  if (!ctx.chordBars.length) {
    warnings.push(`${where}: 曲のコード進行が読めないので、cut16 は使いませんでした`);
    return [{ ...base, pattern: undefined } as AiPart];
  }
  const stepsPerBar = Math.max(1, Math.round(ctx.beatsPerBar * 4));
  const grid = fitGrid(gridText, stepsPerBar);
  const bars = Math.round(ctx.totalBeats / ctx.beatsPerBar);
  const voices = 3;
  const events: string[][] = Array.from({ length: voices }, () => []);
  const push = (v: number, name: string | null, beats: number, marks = ""): void => {
    if (beats <= 0) return;
    const last = events[v][events[v].length - 1];
    if (!name && last && last.startsWith("R:")) {
      events[v][events[v].length - 1] = `R:${String(Math.round((Number(last.slice(2)) + beats) * 1e6) / 1e6)}`;
      return;
    }
    events[v].push(name ? `${name}:${String(Math.round(beats * 1e6) / 1e6)}${marks}` : `R:${String(Math.round(beats * 1e6) / 1e6)}`);
  };
  const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const nameOf = (m: number): string => `${NAMES[m % 12]}${Math.floor(m / 12) - 1}`;
  for (let bar = 0; bar < bars; bar++) {
    const chord = ctx.chordBars[bar % ctx.chordBars.length];
    const form = voicingOf(chord, 5);
    if (!form) {
      warnings.push(`${where}: コード「${chord}」を読めませんでした。cut16 は使いませんでした`);
      return [{ ...base, pattern: undefined } as AiPart];
    }
    const top = form.slice(-voices);
    const offset = voices - top.length;
    for (let s = 0; s < stepsPerBar; s++) {
      const ch = grid[s];
      if (ch === "-") continue; // 前の音にのばしてある
      let len = 1;
      while (s + len < stepsPerBar && grid[s + len] === "-") len++;
      const beats = len * 0.25;
      for (let v = 0; v < voices; v++) {
        const idx = v - offset;
        if (ch === ".") { push(v, null, beats); continue; }
        if (idx < 0) { push(v, null, beats); continue; }
        // X＝強く（のばす）、x＝弾いて切る、o＝弱い消す音（短く）
        const marks = ch === "X" ? "!" : ch === "x" ? "'" : ",'";
        push(v, nameOf(top[idx]), beats, marks);
      }
    }
  }
  const vol = Math.max(0.02, (Number(p.volume) || 0.14) / Math.sqrt(voices));
  return events.map((evs, v) => ({
    ...base,
    role: `${nameOfPart(p)}・音${v + 1}`,
    volume: r3(vol),
    sustain: p.sustain ?? 1,
    phrase: undefined,
    notes: evs.join(" "),
  }) as AiPart);
}

// ───────── AIへの指示文（提案2） ─────────
/** AI_SONG_GUIDE の末尾に足す。J-POPのクリーンギターの出発点（docs/sound/jpop-clean-guitar-guide.md の§3・§4）。 */
export const AI_SONG_JPOP_GUIDE = `

## J-POPのクリーンギターの出発点（2026-10-11。詳しくは docs/sound/jpop-clean-guitar-guide.md）
J-POPやアニソン寄りの曲で、クリーンのギターを入れるときの組み合わせ例。数字は出発点で、耳で調整する。歪みは「サビ・ここぞ」だけにして、クリーンの刻み・アルペジオは歪ませない。**浅い chorus（0.25〜0.4）は許す**。電子的に聞こえるのは深い chorus で、浅く短くかけるぶんには音が自然に広がる。
- アルペジオ（イントロ・バラード・Aメロ）: instrument guitar、amp jpopClean（刺さりが気になるなら crystal、きらめきが欲しいなら sparkleClean）、volume 0.14〜0.2、pan ±0.3〜0.5（ピアノと反対側）、reverb 0.25〜0.35、chorus 0.25〜0.4、bright -0.1〜0.1、sustain 1.4〜1.8（スタッカートにしない）、音域は E3〜E5。開放弦を混ぜ、拍頭を ! で強く。例: \`{"instrument":"guitar","role":"アルペジオ","volume":0.16,"pan":-0.35,"amp":"jpopClean","reverb":0.3,"chorus":0.3,"sustain":1.6,"notes":"..."}\`。名前付きの音づくり \`"recipe":"jpop-arpeggio"\` で同じ値が入る。
- カッティング（Aメロ・サビ前）: amp jpopClean か funk、volume 0.1〜0.16、pan 0.4〜0.7、reverb 0.1〜0.18、chorus 0〜0.15。**弾く音は短く、消す音は休符**にして、連打の単音は避ける（和音の構成音で切る）。\`"pattern":"cut16"\`（\`"cutGrid":"pop"\`・\`"sparse"\`・\`"drive"\` か、X x o - . の16文字）を書くと、コード進行から消す音つきの刻みが3声で自動で作られる（notes は ""）。recipe は \`jpop-cutting\`。
- 8分のストローク（サビ）: amp jpopClean、\`"doubleDetune":{"cents":6,"spread":0.7}\`（左右にひらく）、volume 各 0.08〜0.11、reverb 0.15〜0.22、chorus 0〜0.1。recipe \`jpop-stroke\`。サビはバンド感を優先して残響を控えめに。
- 空間ギター（イントロのフック・間奏）: instrument echoGuitar、\`"echo":{"repeats":2,"time":"dotted8","decay":0.28}\`、reverb 0.3〜0.4。リピートは3回以上にしない。recipe \`jpop-space\`。
- ディメンションC風の広がり: \`"widen":"dimension"\`（同じ旋律を左右に置き、片側を 12ms 遅らせて浅い chorus。モノラルで痩せないよう pan は ±0.7 まで）。recipe \`jpop-dimension\`。
- 気に入られた3つ（名前付き）: \`"recipe":"sparkle-delay"\`＝sparkleClean＋弱いディレイ（repeats 1・decay 0.15）、\`"crystal-wide"\`＝crystal＋左右の厚み（doubleDetune）、\`"sparkle-wide-delay"\`＝sparkleClean＋厚み＋ディレイ。recipe は書いていない項目だけを補うので、volume・pan・notes は自分で書く。
- ディレイの言い方: echo の time は拍の数のほかに \`"slap"\`（約 0.07 拍・1 回・decay 0.8）と、\`"ms":30\`（ミリ秒。BPM に関係なく 40ms 未満は別の音でなく「厚み」に聞こえる）。例 \`"echo":{"ms":30,"repeats":1,"decay":0.8}\`。
- 引き算: 曲に \`"bare":["verse"]\`（true は Aメロ）と書くと、そのセクションで自動の伴奏のベース・鍵盤・ギター・弦が、各小節の最初の音だけをのばす（ルートとコードだけ）。手書きのパートは \`"bare":"mute"\`（休む。副旋律・オブリガード向け）か \`"hold"\`（最初の音だけをのばす）。足す前に引く。要 sections／scene。
- 出し入れ: \`"sectionFx":{"intro":{"reverb":0.4,"chorus":0.4},"chorus":{"reverb":0.15,"chorus":0.05}}\`＝イントロ・間奏で強め、サビで控えめ。2本目のギターは \`"guitarPair":true\`（1本目＝クリーン＋chorus を左、2本目＝浅い crunch の小音量を右、サビだけ。\`{"mode":"octave"}\` なら1オクターブ上のクリーン）。奥行きは \`"reverbPre":12\`（ミリ秒。ballad＝70）。
- 自動伴奏: \`"feel":"jpop"\`＝イントロはギター（jpopClean のアルペジオ）と鍵盤だけ、Aメロは引いてBメロでギターが入り、サビで全員。ギターはピアノと左右反対。
- 仕上げ（書き出し）: バンド編成のJ-POPは \`--master-preset jpop-band\`（rock-clean に 250Hz -1、2kHz +0.5、8kHz 高域 +1.5）。
`;
