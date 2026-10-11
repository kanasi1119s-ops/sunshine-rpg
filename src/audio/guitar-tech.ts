import type { AiPart } from "./ai-song";
import { REST, type NoteEvent } from "./score";
import { noteNameToMidi } from "./note";
import { parseChord } from "./newsong";
import { resolveScale, scalePitchClasses } from "./scales";
import { hash01 } from "./articulation";
import { strumVoicing, type ExpandCtx } from "./part-expand";

/**
 * ギターの奏法の糖衣記法・展開（2026-10-11）。docs/sound/guitar-techniques-rock-guide.md §7・guitar-techniques-world-guide.md §5・
 * guitar-technique-deep-guide.md §10 の「取り入れる提案」のうち、記法の展開で済むものをここにまとめた。
 * どれも、書かなければ何も変わない（今までの曲の音は変わらない）。
 *
 * - 音符の糖衣: `E2:2@gallop`（ギャロップ）・`@rgallop`・`@trem`（0.125 拍の同音）・`@trem16`（0.25 拍）
 * - パートの項目: rhythm・power(+oct)・palmMute・tremolo・swell・legato・ghost・harmonize・fingerpick・capo・mask・gtrStyle・vibrato・autoScoop
 * - 音符の記号（ai-song.ts の parseNotes）: x（デッドノート）・~.（弱いビブラート）・~~~・< >（スウェル）・^^@0.25（ベンドの形）・A4:1>D5（スライド）・D5:3^^u(E5)（ユニゾンベンド）
 */

const clamp = (v: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, v));
const fmt = (v: number): string => String(Math.round(v * 1e6) / 1e6);
const SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
/** MIDI 番号 → 音名（シャープ表記）。 */
export const midiToNoteName = (m: number): string => `${SHARP[((m % 12) + 12) % 12]}${Math.floor(m / 12) - 1}`;
const words = (s: unknown): string[] => String(s ?? "").trim().split(/\s+/).filter(Boolean);
const isRest = (n: string): boolean => n === "R" || n === "r";
const isPitch = (n: string): boolean => /^[A-G][#b]?-?\d+$/.test(n);

interface Tok { name: string; dur: number; marks: string }
const TOK = /^([^:\s]+):(\d+(?:\.\d+)?)(.*)$/;
function parseTok(raw: string): Tok | null {
  const m = TOK.exec(raw);
  return m ? { name: m[1], dur: Number(m[2]), marks: m[3] } : null;
}
const tokStr = (name: string, dur: number, marks = ""): string => `${name}:${fmt(dur)}${marks}`;

/** 記号を「強さ・長さ」（! , ' _ *）と「形」（~ ^ / \ < > @数字 .）に分ける。 */
function splitMarks(marks: string): { art: string; shape: string } {
  const art = (marks.match(/[!,'_*]/g) ?? []).join("");
  return { art, shape: marks.replace(/[!,'_*]/g, "") };
}

// ───────── デッドノート（x） ─────────
/**
 * デッドノートの音程。直前の音の高さを、G3（55）以下になるまで1オクターブずつ下げる（E2 より下にはしない）。
 * 高い音の「ピ」にならないよう、いつも低めの音域で鳴らす（banned-sounds.md の「短い単音の刻み・高い」を避ける）。
 */
export function deadNoteName(from: string | null): string {
  if (!from) return "E3";
  let m = noteNameToMidi(from);
  while (m > 55) m -= 12;
  while (m < 40) m += 12;
  return midiToNoteName(m);
}
/** デッドノートの強さ。`!`＝0.8、`,`＝0.3、ふつう 0.45。 */
export function deadNoteEvent(name: string, dur: number, marks = ""): NoteEvent {
  return { note: name, durationBeats: dur, velocity: marks.includes("!") ? 0.8 : marks.includes(",") ? 0.3 : 0.45, gate: 0.3, dead: true };
}

// ───────── ギャロップ・トレモロの糖衣 ─────────
const FIGURES: Record<string, number[]> = { gallop: [0.5, 0.25, 0.25], rgallop: [0.25, 0.25, 0.5], trem: [0.125], trem16: [0.25] };
const SUGAR = /^([^:@\s]+):(\d+(?:\.\d+)?)([^@\s]*)@(gallop|rgallop|trem|trem16)$/;

/** 1 つの音を、型（gallop・rgallop・trem・trem16）に展開した音の並び（トークン）にする。 */
export function figureTokens(name: string, dur: number, marks: string, kind: string): string[] {
  const unit = FIGURES[kind];
  if (isRest(name) || !unit) return [tokStr(name, dur, isRest(name) ? "" : marks)];
  const { art, shape } = splitMarks(marks);
  const plain = art.replace(/[!,]/g, "");
  const first = (extra: string): string => `${extra}${shape}`;
  const out: string[] = [];
  if (kind === "gallop" || kind === "rgallop") {
    const total = 1;
    const units = Math.floor(dur / total + 1e-9);
    if (units < 1) return [tokStr(name, dur, marks)];
    const strong = art.includes(",") ? art : `${plain}!`;
    for (let u = 0; u < units; u++) {
      unit.forEach((d, k) => {
        const accent = kind === "gallop" ? k === 0 : k === 2;
        const m = accent ? strong : plain;
        out.push(tokStr(name, d, u === 0 && k === 0 ? first(m) : m));
      });
    }
    const rem = dur - units * total;
    if (rem > 1e-9) out.push(tokStr(name, rem, plain));
    return out;
  }
  const step = unit[0];
  const count = Math.max(1, Math.round(dur / step));
  for (let k = 0; k < count; k++) {
    const d = k === count - 1 ? dur - (count - 1) * step : step;
    out.push(tokStr(name, d, k === 0 ? `${art}${shape}` : plain));
  }
  return out;
}

/** `E2:2@gallop` のような糖衣を、ふつうの音の並びに直す（糖衣のない曲では何も変わらない）。 */
export function expandNoteSugar(text: string): string {
  if (!text.includes("@")) return text;
  return words(text)
    .flatMap((raw) => {
      const m = SUGAR.exec(raw);
      return m ? figureTokens(m[1], Number(m[2]), m[3], m[4]) : [raw];
    })
    .join(" ");
}

// ───────── 型の名前の辞書（strum.pattern） ─────────
export interface StrumPreset { pattern: string; step: number; spreadMs: number; strings: number; sustain?: number; note: string }
/**
 * strum.pattern に書ける型の名前。pattern・step・spreadMs・strings の既定値を持つ（strum に書いた値が優先）。
 * 型の文字: D ダウン・d 弱いダウン・U/u アップ・x ミュート・g ゴースト（とても弱いミュート）・m パームミュート（短く切る）・> 次の1打をアクセント・. のばす・- 休み。
 */
export const STRUM_PRESETS: Record<string, StrumPreset> = {
  pop: { pattern: "D.DU.UDU", step: 0.5, spreadMs: 12, strings: 5, note: "定番の8分（初期値と同じ）" },
  folk6: { pattern: "D.DU.UDU", step: 0.5, spreadMs: 12, strings: 6, note: "フォークの6弦" },
  skank: { pattern: "-U-U-U-U", step: 0.5, spreadMs: 6, strings: 3, sustain: 0.4, note: "レゲエ・スカの裏打ち（3弦）" },
  rasgueado: { pattern: "DDDD............", step: 0.25, spreadMs: 8, strings: 5, note: "フラメンコ風の連打。1拍のあと3拍のばす" },
  bossa: { pattern: "D.d.-u.-", step: 0.25, spreadMs: 8, strings: 4, sustain: 1, note: "ボサノバのバチーダ（和音の層。拍1の頭と裏、拍2の2つ目の16分）" },
  "funk-cut": { pattern: "gxDgxDgxDgxDgxDx", step: 0.25, spreadMs: 4, strings: 4, sustain: 0.7, note: "ファンクの16分カッティング（3-3-3-3-4）。4音の和音・中低域で（banned-sounds.md の1を避ける）" },
  punk8: { pattern: "DDDDDDDD", step: 0.5, spreadMs: 8, strings: 6, note: "ポップパンクの8分ダウン" },
  waltz: { pattern: "D.d.d.", step: 0.5, spreadMs: 12, strings: 5, note: "3拍子（1小節＝3拍）" },
  ballad: { pattern: "D...D.dU", step: 0.5, spreadMs: 16, strings: 6, note: "ロックバラードのゆったりしたストローク" },
};
STRUM_PRESETS["pop-punk"] = STRUM_PRESETS.punk8;

/** strum の指定を、型の名前（STRUM_PRESETS）も含めて pattern・step・spreadMs・strings に直す。書いた値が優先。 */
export function resolveStrumSpec<T extends { pattern?: string; step?: number; spreadMs?: number; strings?: number }>(spec: T, warnings: string[], where: string): T & { sustainPreset?: number } {
  const key = String(spec.pattern ?? "").trim();
  const isName = /^[a-z][a-z0-9-]{2,}$/.test(key) && !/^[dDuUxXmMg]+$/.test(key);
  const preset = isName ? STRUM_PRESETS[key] : undefined;
  if (isName && !preset) {
    warnings.push(`${where}: strum.pattern の名前「${key}」は表にありません（${Object.keys(STRUM_PRESETS).join("・")}）。D d U u x g m > . - の文字で書くか、名前を直してください`);
  }
  if (!preset) return spec;
  return { ...spec, pattern: preset.pattern, step: spec.step ?? preset.step, spreadMs: spec.spreadMs ?? preset.spreadMs, strings: spec.strings ?? preset.strings, sustainPreset: preset.sustain };
}

// ───────── カポ ─────────
const NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"];
const NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
/** コード名の根音（と分数コードの低音）を半音ずらす。読めなければ null。 */
export function transposeChordName(name: string, semis: number): string | null {
  const c = parseChord(name);
  if (!c) return null;
  const m = /^([A-G][#b]?)(.*)$/.exec(name.split("/")[0]);
  if (!m) return null;
  const flatty = m[1].includes("b") || m[1] === "F";
  const table = flatty ? NAMES_FLAT : NAMES_SHARP;
  const head = `${table[(((c.root + semis) % 12) + 12) % 12]}${m[2]}`;
  return c.bass !== undefined ? `${head}/${table[(((c.bass + semis) % 12) + 12) % 12]}` : head;
}

/**
 * カポつきの弦の押さえ方。コード名は「鳴る和音」で、カポの分だけ下げた形（開放弦のフォーム）を押さえて、カポの分だけ上へずらす。
 * 例: capo 2 で D → C の形を 2 半音上げる。カポ 0 は strumVoicing と同じ。
 */
export function capoVoicing(chord: string, strings: number, capo: number): number[] | null {
  const k = clamp(Math.round(Number(capo) || 0), 0, 11);
  if (k === 0) return strumVoicing(chord, strings);
  const shape = transposeChordName(chord, -k);
  const v = shape ? strumVoicing(shape, strings) : null;
  return v ? v.map((m) => m + k) : null;
}

// ───────── チャンクと型 ─────────
export interface FingerpickSpec {
  /** 弾くコード（"C Am F G"）。書かなければ曲のコード進行。 */
  chords?: string;
  /** コード 1 つが続く小節数（chords を書いたときだけ。省略は 1）。 */
  bars?: number;
  /** 型の名前（travis・pima・pimi・arp6・bossaThumb）か、p q i m a - . の文字で書いた型。p＝親指（低い弦）・q＝親指（2番目に低い弦）・i m a＝人差し指・中指・薬指（高い弦3本）。 */
  pattern?: string;
  /** 1 ステップの長さ（拍）。省略は型の既定（0.5）。 */
  step?: number;
  /** 使う弦の数（3〜6。省略は5）。 */
  strings?: number;
  /** カポ（0〜11。コード名は鳴る和音で、押さえる形はカポの分だけ下げたもの）。 */
  capo?: number;
}
export const FINGERPICK_PATTERNS: Record<string, { pattern: string; step: number; note: string }> = {
  travis: { pattern: "piqmpiqm", step: 0.5, note: "親指が低音を交互に、指が裏を埋める（トラヴィス）" },
  pima: { pattern: "pimapima", step: 0.5, note: "p-i-m-a の上行アルペジオ" },
  pimi: { pattern: "pimipimi", step: 0.5, note: "p-i-m-i の往復" },
  arp6: { pattern: "pimami", step: 0.5, note: "6ステップ＝3拍（3拍子のアルペジオ）" },
  bossaThumb: { pattern: "p...q...", step: 0.25, note: "ボサノバの親指（拍1が根音、拍2が5度寄りの音）。和音の層は strum.pattern:\"bossa\" を別パートで重ねる" },
};

function chordSpans(spec: { chords?: string; bars?: number }, ctx: ExpandCtx): { chord: string; beats: number }[] {
  if (spec.chords && spec.chords.trim()) {
    const bars = Math.max(1, Math.round(Number(spec.bars) || 1));
    return spec.chords.trim().split(/[\s|]+/).map((c) => ({ chord: c.replace(/\*\d+$/, ""), beats: bars * ctx.beatsPerBar }));
  }
  return ctx.chordBars.map((c) => ({ chord: c, beats: ctx.beatsPerBar }));
}

/** fingerpick を、親指のパートと指のパートの 2 つに展開する。 */
export function expandFingerpick(p: AiPart, spec: FingerpickSpec, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const where = `parts（${p.role ?? p.instrument}）の fingerpick`;
  const { fingerpick: _f, ...rest } = p;
  const key = String(spec.pattern ?? "travis").trim();
  const named = FINGERPICK_PATTERNS[key];
  const pattern = named ? named.pattern : key;
  if (!pattern || !/^[pqima\-.]+$/.test(pattern)) {
    warnings.push(`${where}: pattern は ${Object.keys(FINGERPICK_PATTERNS).join("・")} か、p q i m a - . の文字で書きます「${key}」。指弾きにしませんでした`);
    return [rest as AiPart];
  }
  const step = clamp(Number(spec.step) || named?.step || 0.5, 0.125, 2);
  const stringsN = clamp(Math.round(Number(spec.strings) || 5), 3, 6);
  const capo = clamp(Math.round(Number(spec.capo ?? p.capo) || 0), 0, 11);
  const spans = chordSpans(spec, ctx);
  if (!spans.length) return [rest as AiPart];
  const forms: { v: number[]; beats: number }[] = [];
  let filled = 0;
  for (let i = 0; filled < ctx.totalBeats - 1e-6 && i < 4096; i++) {
    const s = spans[i % spans.length];
    const v = capoVoicing(s.chord, stringsN, capo);
    if (!v) {
      warnings.push(`${where}: コード「${s.chord}」を読めませんでした。fingerpick を使わず、notes のままにしました`);
      return [rest as AiPart];
    }
    forms.push({ v, beats: Math.min(s.beats, ctx.totalBeats - filled) });
    filled += s.beats;
  }
  const toks: { ch: string; steps: number }[] = [];
  for (const ch of pattern) {
    const last = toks[toks.length - 1];
    if (ch === "." && last && last.ch !== "-") last.steps++;
    else toks.push({ ch: ch === "." ? "-" : ch, steps: 1 });
  }
  const bass: string[] = [];
  const treble: string[] = [];
  let hasTreble = false;
  for (const f of forms) {
    const n = f.v.length;
    const pick = (ch: string): number => (ch === "p" ? f.v[0] : ch === "q" ? f.v[Math.min(1, n - 1)] : ch === "i" ? f.v[Math.max(0, n - 3)] : ch === "m" ? f.v[Math.max(0, n - 2)] : f.v[n - 1]);
    let t = 0;
    for (let ti = 0; t < f.beats - 1e-9; ti++) {
      const tok = toks[ti % toks.length];
      const dur = Math.min(tok.steps * step, f.beats - t);
      if (tok.ch === "-") { bass.push(tokStr("R", dur)); treble.push(tokStr("R", dur)); }
      else if (tok.ch === "p" || tok.ch === "q") { bass.push(tokStr(midiToNoteName(pick(tok.ch)), dur, t % 1 === 0 ? "!" : "")); treble.push(tokStr("R", dur)); }
      else { treble.push(tokStr(midiToNoteName(pick(tok.ch)), dur, ",")); bass.push(tokStr("R", dur)); hasTreble = true; }
      t += dur;
    }
  }
  const vol = Math.max(0.02, Math.round(((Number(p.volume) || 0.12) / Math.SQRT2) * 1000) / 1000);
  const mk = (suffix: string, notes: string[], sustain: number, pan: number): AiPart => ({ ...rest, role: `${p.role ?? p.instrument}・${suffix}`, volume: vol, pan, sustain: p.sustain ?? sustain, autoScoop: p.autoScoop ?? false, phrase: undefined, notes: notes.join(" ") } as AiPart);
  const out = [mk("親指", bass, 2.4, clamp((Number(p.pan) || 0) - 0.1, -1, 1))];
  if (hasTreble) out.push(mk("指", treble, 1.8, clamp((Number(p.pan) || 0) + 0.1, -1, 1)));
  return out;
}

// ───────── パワーコード ─────────
const NO_POWER = new Set(["distGuitar", "crunch"]);
/** パワーコード: notes の音を根音にして、5度（と oct:true ならオクターブ）のパートを足す。distGuitar／crunch は書き出しで 5度とオクターブが自動で重なるので展開しない。 */
export function expandPower(p: AiPart, warnings: string[]): AiPart[] {
  const spec = p.power;
  const { power: _p, oct: _o, ...rest } = p;
  if (NO_POWER.has(p.instrument)) {
    warnings.push(`parts（${p.role ?? p.instrument}）: ${p.instrument} は書き出しで5度とオクターブが自動で重なるので、power は使いません。根音だけを書いてください`);
    return [rest as AiPart];
  }
  const oct = p.oct === true || spec === "oct" || (typeof spec === "object" && spec !== null && (spec as { oct?: boolean }).oct === true);
  const offsets = oct ? [0, 7, 12] : [0, 7];
  const vol = Math.max(0.02, Math.round(((Number(p.volume) || 0.2) / Math.sqrt(offsets.length)) * 1000) / 1000);
  const labels = ["根音", "5度", "8度"];
  return offsets.map((off, k) => ({
    ...rest,
    role: `${p.role ?? p.instrument}・${labels[k]}`,
    volume: vol,
    autoScoop: p.autoScoop ?? false,
    phrase: undefined,
    notes: words(p.notes).map((raw) => {
      const t = parseTok(raw);
      if (!t || !isPitch(t.name) || off === 0) return raw;
      const m = noteNameToMidi(t.name) + off;
      // ベンド・しゃくり・ユニゾンは根音だけに付ける（5度・オクターブにまで付けると音程がぶつかる）
      return tokStr(midiToNoteName(m), t.dur, t.marks.replace(/[\^/\\](?:\.|@\d+(?:\.\d+)?)*/g, "").replace(/u\([^)]*\)/, ""));
    }).join(" "),
  } as AiPart));
}

// ───────── パームミュート・トレモロ・スウェル ─────────
/** palmMute: sustain を 0.8〜1.0 に、bright を -0.2。短い同音連打（禁止の音）にならず、「ズンズン」に寄せる。 */
export function applyPalmMute(p: AiPart): AiPart {
  const v = typeof p.palmMute === "number" ? clamp(p.palmMute, 0.8, 1) : 0.9;
  const { palmMute: _m, ...rest } = p;
  return { ...rest, sustain: p.sustain ?? v, bright: clamp((Number(p.bright) || 0) - 0.2, -1, 0.5) } as AiPart;
}

/** tremolo: 長い音（既定 1 拍以上）を、rate 拍（既定 0.25）の同音の連なりにする。余韻が重なるよう sustain の既定を 1.6 にする。 */
export function expandTremolo(p: AiPart): AiPart {
  const spec = typeof p.tremolo === "object" && p.tremolo ? p.tremolo : {};
  const rate = clamp(Number(spec.rate) || 0.25, 0.125, 0.5);
  const min = Math.max(rate * 2, Number(spec.min) || 1);
  const { tremolo: _t, ...rest } = p;
  const notes = words(p.notes).flatMap((raw) => {
    const t = parseTok(raw);
    if (!t || !isPitch(t.name) || t.dur < min - 1e-9) return [raw];
    const { art, shape } = splitMarks(t.marks);
    const out: string[] = [];
    const count = Math.max(1, Math.round(t.dur / rate));
    for (let k = 0; k < count; k++) out.push(tokStr(t.name, k === count - 1 ? t.dur - (count - 1) * rate : rate, k === 0 ? `${art}${shape}` : art.replace(/[!,]/g, "")));
    return out;
  });
  return { ...rest, sustain: p.sustain ?? 1.6, notes: notes.join(" ") } as AiPart;
}

/** swell: 長い音（既定 1 拍以上）に `<`（音量が立ち上がる）を付け、立ち上がり（attack）を遅くする。すでに < > を書いた音は変えない。 */
export function applySwellFlag(p: AiPart): AiPart {
  const min = typeof p.swell === "number" ? Math.max(0.5, p.swell) : 1;
  const { swell: _s, ...rest } = p;
  const notes = words(p.notes).map((raw) => {
    const t = parseTok(raw);
    if (!t || !isPitch(t.name) || t.dur < min - 1e-9 || /[<>]/.test(t.marks) || /u\(/.test(t.marks)) return raw;
    return tokStr(t.name, t.dur, `${t.marks}<`);
  });
  return { ...rest, attack: p.attack ?? 0.7, notes: notes.join(" ") } as AiPart;
}

/** rhythm:"gallop"（など）: 1 拍以上（トレモロは 0.5 拍以上）の音を型に展開する。 */
export function applyRhythmFigure(p: AiPart, warnings: string[]): AiPart {
  const kind = String(p.rhythm);
  const { rhythm: _r, ...rest } = p;
  if (!FIGURES[kind]) {
    warnings.push(`parts（${p.role ?? p.instrument}）: rhythm「${kind}」は使えません（${Object.keys(FIGURES).join("・")}）`);
    return rest as AiPart;
  }
  const min = kind.startsWith("trem") ? 0.5 : 1;
  const notes = words(p.notes).flatMap((raw) => {
    const t = parseTok(raw);
    return t && isPitch(t.name) && t.dur >= min - 1e-9 ? figureTokens(t.name, t.dur, t.marks, kind) : [raw];
  });
  return { ...rest, notes: notes.join(" ") } as AiPart;
}

// ───────── ユニゾンベンド ─────────
const UNISON = /u\(([A-G][#b]?-?\d)\)$/;
/** `D5:3!^^u(E5)`: D5 を E5 の高さまでベンドし、E5 を弾く別パートを作る。ベンド量は音程の差から自動で決める（食い違いは直す）。 */
export function expandUnisonBends(p: AiPart, warnings: string[]): AiPart[] {
  const toks = words(p.notes);
  if (!toks.some((w) => UNISON.test(w))) return [p];
  const main: string[] = [];
  const comp: string[] = [];
  for (const raw of toks) {
    const u = UNISON.exec(raw);
    const t = u ? parseTok(raw.replace(UNISON, "")) : null;
    if (!u || !t || !isPitch(t.name)) {
      main.push(raw);
      const r = parseTok(raw);
      comp.push(r ? tokStr("R", r.dur) : raw);
      continue;
    }
    const diff = noteNameToMidi(u[1]) - noteNameToMidi(t.name);
    if (!(diff >= 1 && diff <= 4)) {
      warnings.push(`parts（${p.role ?? p.instrument}）: ユニゾンベンド「${raw}」は、目標の音が上に1〜4半音のときだけ使えます。ふつうの音にしました`);
      main.push(raw.replace(UNISON, ""));
      comp.push(tokStr("R", t.dur));
      continue;
    }
    const declared = (t.marks.match(/\^(\.)?/g) ?? []).reduce((s, x) => s + (x.length > 1 ? 0.5 : 1), 0);
    if (declared && declared !== diff) warnings.push(`parts（${p.role ?? p.instrument}）: ユニゾンベンド「${raw}」のベンド量（${declared}半音）が音程の差（${diff}半音）と食い違うので、差に合わせました`);
    const marks = `${t.marks.replace(/\^\.?/g, "")}${"^".repeat(diff)}`;
    main.push(tokStr(t.name, t.dur, marks));
    comp.push(tokStr(u[1], t.dur, splitMarks(t.marks).art.replace(/[!]/g, "")));
  }
  return [
    { ...p, notes: main.join(" ") },
    { ...p, role: `${p.role ?? p.instrument}・ユニゾン`, notes: comp.join(" "), motif: undefined, autoScoop: p.autoScoop ?? false } as AiPart,
  ];
}

// ───────── ハーモナイザ ─────────
export interface HarmonizeSpec {
  /** 度数。-3（既定）＝3度下、3＝3度上、-6＝6度下。±2〜±8。 */
  interval?: number;
  /** 音階（"minor@E"・"dorian@D" など。scales.ts の名前）。省略は曲の scale／tonic。 */
  scale?: string;
  /** 主音（scale に @ がないとき）。 */
  tonic?: string;
  /** ハモリの音量（元のパートの何倍か。省略は 0.75）。 */
  volume?: number;
  /** ハモリの左右。省略は元のパートの反対側へ 0.3。 */
  pan?: number;
}
/** 音階の音だけで、midi から steps 個ぶん（符号で上下）動かす。音階外の音は、いちばん近い音階の音（同じ近さなら下）にそろえてから動かす。 */
export function diatonicShift(midi: number, steps: number, pcs: number[]): number {
  const set = new Set(pcs);
  if (!set.size) return midi;
  const has = (m: number): boolean => set.has(((m % 12) + 12) % 12);
  let base = midi;
  for (let d = 0; d <= 6; d++) {
    if (has(midi - d)) { base = midi - d; break; }
    if (has(midi + d)) { base = midi + d; break; }
  }
  const dir = Math.sign(steps);
  let m = base;
  for (let k = 0; k < Math.abs(steps); k++) {
    do { m += dir; } while (!has(m) && Math.abs(m - base) < 60);
  }
  return m;
}
/** harmonize: 元のパートと、音階に合わせて度数だけ離したハモリのパートに展開する。 */
export function expandHarmonize(p: AiPart, spec: HarmonizeSpec | true, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const s: HarmonizeSpec = spec === true ? {} : spec;
  const { harmonize: _h, ...rest } = p;
  const where = `parts（${p.role ?? p.instrument}）の harmonize`;
  const interval = Math.round(Number(s.interval ?? -3));
  if (!(Math.abs(interval) >= 2 && Math.abs(interval) <= 8)) {
    warnings.push(`${where}: interval は ±2〜±8 の度数にしてください（${String(s.interval)}）。ハモリを作りませんでした`);
    return [rest as AiPart];
  }
  const scale = s.scale ? resolveScale(String(s.scale), s.tonic) : ctx.scale;
  if (!scale) {
    warnings.push(s.scale ? `${where}: scale「${String(s.scale)}」は表にありません。ハモリを作りませんでした` : `${where}: scale（"minor@E" など）か、曲の scale と tonic が要ります。ハモリを作りませんでした`);
    return [rest as AiPart];
  }
  const pcs = scalePitchClasses(scale.scale, scale.tonic);
  const steps = Math.sign(interval) * (Math.abs(interval) - 1);
  const pan0 = Number(p.pan) || 0;
  const notes = words(p.notes).map((raw) => {
    const t = parseTok(raw);
    if (!t || !isPitch(t.name)) return raw;
    const m = diatonicShift(noteNameToMidi(t.name), steps, pcs);
    const marks = t.marks.replace(/[\^/\\](?:\.|@\d+(?:\.\d+)?)*/g, "").replace(/>[A-G][#b]?-?\d/, "").replace(/u\([^)]*\)/, "");
    return tokStr(midiToNoteName(m), t.dur, marks);
  });
  const harmony = {
    ...rest,
    role: `${p.role ?? p.instrument}・ハモリ`,
    volume: Math.max(0.02, Math.round((Number(p.volume) || 0.2) * clamp(Number(s.volume) || 0.75, 0.1, 1.5) * 1000) / 1000),
    pan: clamp(s.pan !== undefined ? Number(s.pan) : pan0 > 0.1 ? pan0 - 0.3 : pan0 + 0.3, -1, 1),
    motif: undefined,
    notes: notes.join(" "),
  } as AiPart;
  return [rest as AiPart, harmony];
}

// ───────── mask（歌の休符にだけ鳴らす） ─────────
interface Span { s: number; e: number }
function soundingSpans(notes: string, total: number): Span[] {
  const toks = words(notes).map(parseTok).filter((t): t is Tok => t !== null);
  const len = toks.reduce((a, t) => a + t.dur, 0);
  if (!(len > 0)) return [];
  const spans: Span[] = [];
  let at = 0;
  for (let i = 0; at < total - 1e-9 && i < 100000; i++) {
    const t = toks[i % toks.length];
    if (!isRest(t.name)) spans.push({ s: at, e: Math.min(total, at + t.dur) });
    at += t.dur;
  }
  spans.sort((a, b) => a.s - b.s);
  const merged: Span[] = [];
  for (const x of spans) {
    const last = merged[merged.length - 1];
    if (last && x.s <= last.e + 1e-9) last.e = Math.max(last.e, x.e);
    else merged.push({ ...x });
  }
  return merged;
}
/**
 * mask: ギターのパートから、指定した役割（role に含まれる文字）のパートが鳴っている間の音を消し、その休符だけを残す（duck の音符版）。
 * 歌のパートの鳴り始めまでで音を切る。gain を 0 より大きく書くと、消さずに弱く（`,,`）鳴らす。
 */
export function applyMask(list: AiPart[], ctx: ExpandCtx, warnings: string[], drums: Set<string>): AiPart[] {
  return list.map((p) => {
    if (!p.mask || drums.has(p.instrument)) return p;
    const spec = typeof p.mask === "string" ? { role: p.mask } : p.mask;
    const role = String(spec.role ?? "").trim();
    const { mask: _m, ...rest } = p;
    if (!role) { warnings.push(`parts（${p.role ?? p.instrument}）: mask には、避ける相手の役割（role に含まれる文字。例 "メロディ"）を書いてください`); return rest as AiPart; }
    const targets = list.filter((q) => q !== p && !q.mask && !drums.has(q.instrument) && String(q.role ?? "").includes(role));
    if (!targets.length) { warnings.push(`parts（${p.role ?? p.instrument}）: mask「${role}」にあたるパートがありません`); return rest as AiPart; }
    const vocal = targets.flatMap((q) => soundingSpans(String(q.notes ?? ""), ctx.totalBeats)).sort((a, b) => a.s - b.s);
    const gain = clamp(Number(spec.gain) || 0, 0, 1);
    const inVocal = (x: number): boolean => vocal.some((v) => x >= v.s - 1e-9 && x < v.e - 1e-9);
    const nextOnset = (x: number): number => vocal.find((v) => v.s > x + 1e-9)?.s ?? Infinity;
    const toks = words(p.notes).map(parseTok).filter((t): t is Tok => t !== null);
    const len = toks.reduce((a, t) => a + t.dur, 0);
    if (!(len > 0)) return rest as AiPart;
    const out: string[] = [];
    let at = 0;
    for (let i = 0; at < ctx.totalBeats - 1e-9 && i < 100000; i++) {
      const t = toks[i % toks.length];
      const dur = Math.min(t.dur, ctx.totalBeats - at);
      if (isRest(t.name)) out.push(tokStr("R", dur));
      else if (inVocal(at)) out.push(gain > 0 ? tokStr(t.name, dur, `${splitMarks(t.marks).art.replace(/[!,]/g, "")},,`) : tokStr("R", dur));
      else {
        const keep = Math.min(dur, nextOnset(at) - at);
        if (gain > 0 || keep >= dur - 1e-9) out.push(tokStr(t.name, dur, t.marks));
        else if (keep >= 0.125) { out.push(tokStr(t.name, keep, t.marks)); out.push(tokStr("R", dur - keep)); }
        else out.push(tokStr("R", dur));
      }
      at += dur;
    }
    return { ...rest, notes: out.join(" ") } as AiPart;
  });
}

// ───────── ギターの型（gtrStyle） ─────────
/** ジャンル別の一括設定。パートに書いた値が優先（amp は "auto" のときだけ置きかえる）。禁止の音（banned-sounds.md）の作り方は入れていない。 */
export const GTR_STYLES: Record<string, { note: string; set: Partial<AiPart> }> = {
  melocore: { note: "メロコア／ポップパンク: amp loudrock（punk・hardrock は使わない）・左右に厚み", set: { amp: "loudrock", doubleDetune: { cents: 6, spread: 0.8 }, bright: -0.1 } },
  thrash: { note: "スラッシュ／メタルの刻み: amp loudmetal・パームミュート・左右に厚み", set: { amp: "loudmetal", palmMute: true, doubleDetune: { cents: 5, spread: 0.9 } } },
  shoegaze: { note: "シューゲイザー: amp shoegaze・長い余韻・コーラス・スウェル", set: { amp: "shoegaze", sustain: 3, chorus: 0.6, reverb: 0.5, swell: true } },
  funkCut: { note: "ファンクのカッティング: amp crystal・ゴーストノート（3〜4音の和音にすること）", set: { amp: "crystal", sustain: 0.8, ghost: { density: 0.3 } } },
  ballad: { note: "ロックバラード: amp crystal・長い余韻・残響", set: { amp: "crystal", sustain: 2, reverb: 0.3 } },
  bossa: { note: "ボサノバ: ナイロン弦（patch nylonGuitar）＋amp crystal（ナイロンは crystal か delicate を付けること）", set: { amp: "crystal", patch: "nylonGuitar", sustain: 2 } },
};
function applyGtrStyle(p: AiPart, warnings: string[]): AiPart {
  const { gtrStyle: key, ...rest } = p;
  const st = GTR_STYLES[String(key)];
  if (!st) {
    warnings.push(`parts（${p.role ?? p.instrument}）: gtrStyle「${String(key)}」は使えません（${Object.keys(GTR_STYLES).join("・")}）`);
    return rest as AiPart;
  }
  const out: Record<string, unknown> = { ...rest };
  for (const [k, v] of Object.entries(st.set)) {
    if (out[k] === undefined || (k === "amp" && out[k] === "auto")) out[k] = v;
  }
  return out as unknown as AiPart;
}

const TECH_KEYS = ["gtrStyle", "rhythm", "tremolo", "swell", "palmMute", "harmonize", "power", "oct", "fingerpick"] as const;
/** 展開が要るパートか（要らなければ手を入れない）。 */
function needsTech(p: AiPart): boolean {
  return TECH_KEYS.some((k) => (p as unknown as Record<string, unknown>)[k] !== undefined && (p as unknown as Record<string, unknown>)[k] !== false) || String(p.notes ?? "").includes("@") || /u\([A-G]/.test(String(p.notes ?? ""));
}

/** ギターの奏法の展開（1 パート → 1 つ以上のパート）。drums は呼ばない。 */
export function expandGuitarTech(p: AiPart, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  if (!needsTech(p)) return [p];
  let cur: AiPart = { ...p };
  if (cur.gtrStyle !== undefined) cur = applyGtrStyle(cur, warnings);
  if (cur.fingerpick) return expandFingerpick(cur, cur.fingerpick, ctx, warnings);
  if (String(cur.notes ?? "").includes("@")) cur = { ...cur, notes: expandNoteSugar(String(cur.notes)) };
  if (cur.rhythm !== undefined) cur = applyRhythmFigure(cur, warnings);
  if (cur.tremolo) cur = expandTremolo(cur);
  else if (cur.tremolo !== undefined) delete cur.tremolo;
  if (cur.swell) cur = applySwellFlag(cur);
  else if (cur.swell !== undefined) delete cur.swell;
  if (cur.palmMute) cur = applyPalmMute(cur);
  else if (cur.palmMute !== undefined) delete cur.palmMute;
  let list = expandUnisonBends(cur, warnings);
  if (cur.harmonize) list = list.flatMap((q, i) => (i === 0 && q.harmonize ? expandHarmonize(q, q.harmonize, ctx, warnings) : [q]));
  if (cur.power || cur.oct) list = list.flatMap((q) => (q.power || q.oct ? expandPower(q, warnings) : [q]));
  return list;
}

// ───────── 音の列の自動処理（legato・ghost） ─────────
/** legato: 0.25 拍以下で続く3音以上を `_` でつなぎ、山なりの強弱（頭を強く→中ほどが最大→終わりへ引く）を付ける。強さを書いた音は変えない。 */
export function applyLegato(events: NoteEvent[]): NoteEvent[] {
  const out = events.map((e) => ({ ...e }));
  const fast = (e: NoteEvent): boolean => e.note !== REST && !e.dead && e.durationBeats <= 0.25 + 1e-9;
  for (let i = 0; i < out.length; ) {
    if (!fast(out[i])) { i++; continue; }
    let j = i;
    while (j + 1 < out.length && fast(out[j + 1])) j++;
    const n = j - i + 1;
    if (n >= 3) {
      for (let k = 0; k < n; k++) {
        const e = out[i + k];
        if (k < n - 1 && e.gate === undefined) e.gate = 1.15;
        if (e.velocity === undefined) e.velocity = Math.round((k === 0 ? 1.2 : 0.78 + 0.3 * Math.sin((Math.PI * k) / (n - 1))) * 1000) / 1000;
      }
    }
    i = j + 1;
  }
  return out;
}

/** ghost: 休符の 16 分の裏（拍の .25 と .75。.5 は半分の確率）に、弱いデッドノートを density の割合で足す。seed が同じなら同じ結果。 */
export function applyGhostNotes(events: NoteEvent[], density: number, seed: string): NoteEvent[] {
  const d = clamp(density, 0, 1);
  if (!(d > 0)) return events;
  const out: NoteEvent[] = [];
  let pos = 0;
  let lastPitch: string | null = null;
  const firstPitch = events.find((e) => e.note !== REST && !e.dead)?.note ?? null;
  let pendingRest = 0;
  const flush = (): void => { if (pendingRest > 1e-9) out.push({ note: REST, durationBeats: Math.round(pendingRest * 1e6) / 1e6 }); pendingRest = 0; };
  for (const e of events) {
    if (e.note !== REST) {
      flush();
      out.push(e);
      if (!e.dead) lastPitch = e.note;
      pos += e.durationBeats;
      continue;
    }
    let left = e.durationBeats;
    let q = pos;
    while (left > 1e-9) {
      const slice = Math.min(0.25, left);
      const frac = Math.round((q - Math.floor(q)) * 1000) / 1000;
      const weight = frac === 0.25 || frac === 0.75 ? d : frac === 0.5 ? d * 0.5 : 0;
      if (slice >= 0.25 - 1e-9 && weight > 0 && hash01(seed, Math.round(q * 4)) < weight) {
        flush();
        out.push(deadNoteEvent(deadNoteName(lastPitch ?? firstPitch), 0.25));
      } else pendingRest += slice;
      q += slice;
      left -= slice;
    }
    pos += e.durationBeats;
  }
  flush();
  return out;
}

/** パートの項目に従って、parseNotes のあとの音の列を直す（legato・ghost）。どちらも書かなければ何もしない。 */
export function applyGuitarEvents(events: NoteEvent[], p: AiPart, seed: string): NoteEvent[] {
  let out = events;
  if (p.legato) out = applyLegato(out);
  if (p.ghost) {
    const g = p.ghost;
    const density = typeof g === "number" ? g : typeof g === "object" && g !== null ? Number(g.density ?? 0.25) : 0.25;
    out = applyGhostNotes(out, density, `${seed}|${p.role ?? ""}`);
  }
  return out;
}

/** vibrato の指定（rate・depth・delay）を Track.vibratoSpec にする。 */
export function vibratoSpecOf(v: unknown): { rate?: number; depth?: number; delay?: number } | null {
  if (!v || typeof v !== "object") return null;
  const o = v as Record<string, unknown>;
  const num = (x: unknown): number | undefined => (x !== undefined && Number.isFinite(Number(x)) ? Number(x) : undefined);
  const rate = num(o.rate), depth = num(o.depth), delay = num(o.delay);
  return {
    ...(rate !== undefined ? { rate: clamp(rate, 3, 8) } : {}),
    ...(depth !== undefined ? { depth: clamp(depth, 8, 60) } : {}),
    ...(delay !== undefined ? { delay: clamp(delay, 0, 2) } : {}),
  };
}

/** glide の指定（depth・rate）を Track.glide にする。true なら既定値。 */
export function glideSpecOf(v: unknown): { depth?: number; rate?: number } | null {
  if (v === true) return {};
  if (!v || typeof v !== "object") return null;
  const o = v as Record<string, unknown>;
  const num = (x: unknown): number | undefined => (x !== undefined && Number.isFinite(Number(x)) ? Number(x) : undefined);
  const depth = num(o.depth), rate = num(o.rate);
  return {
    ...(depth !== undefined ? { depth: clamp(depth, 20, 150) } : {}),
    ...(rate !== undefined ? { rate: clamp(rate, 0.05, 1) } : {}),
  };
}

/** パート項目の型（AiPartExtras に混ぜる）。 */
export interface GuitarTechPartFields {
  /** パワーコード。true で、notes の音を根音として5度のパートを足す。"oct"（か oct:true）でオクターブも。distGuitar／crunch は書き出しで自動で重なるので不要。 */
  power?: boolean | "oct" | { oct?: boolean };
  oct?: boolean;
  /** パームミュート「ズンズン」。true か sustain の値（0.8〜1）。sustain を 0.9 に、bright を -0.2。 */
  palmMute?: boolean | number;
  /** トレモロ奏法。長い音（min 拍以上。既定 1）を rate 拍（既定 0.25）の同音に展開する。 */
  tremolo?: boolean | { rate?: number; min?: number };
  /** 音の型を一括で: "gallop"（0.5 0.25 0.25）・"rgallop"・"trem"（0.125 拍）・"trem16"（0.25 拍）。 */
  rhythm?: "gallop" | "rgallop" | "trem" | "trem16";
  /** ボリューム奏法。1 拍以上（数字ならその拍以上）の音に < を付け、attack を遅くする。 */
  swell?: boolean | number;
  /** 0.25 拍以下の速い音の連なりを自動で _ でつなぎ、山なりの強弱を付ける。 */
  legato?: boolean;
  /** 休符の16分の裏に、弱いデッドノートを自動で足す。数字か { density: 0〜1 }。 */
  ghost?: boolean | number | { density?: number };
  /** ハモリを自動で作る。{ interval: -3, scale: "minor@E" }。 */
  harmonize?: boolean | { interval?: number; scale?: string; tonic?: string; volume?: number; pan?: number };
  /** 指弾き。コード名から親指のパートと指のパートに展開する。 */
  fingerpick?: FingerpickSpec;
  /** カポ（0〜11）。strum／fingerpick のコード名は鳴る和音で、押さえる形をカポの分だけ下げる。 */
  capo?: number;
  /** 歌（などのパート）の鳴っている間の音を消す。避ける相手の役割（role に含まれる文字）か { role, gain }。 */
  mask?: string | { role: string; gain?: number };
  /** ジャンル別の一括設定: melocore・thrash・shoegaze・funkCut・ballad・bossa。 */
  gtrStyle?: string;
  /** ビブラートを自前で作る（ピッチベンドの正弦波）。rate Hz・depth セント・delay 拍。~ を付けた音（0.4 拍以上）に効く。 */
  vibrato?: { rate?: number; depth?: number; delay?: number };
  /** グライド（アームの揺れ）。1 拍以上の音の間じゅう、ゆっくり不規則に ±depth セント（既定100）揺れる。{ depth, rate(Hz。既定0.2) } か true。ベンドを書いた音には効かない。 */
  glide?: boolean | { depth?: number; rate?: number };
  /** false にすると、このパートだけギターの自動しゃくりを止める（true なら、曲が autoScoop:false でもこのパートだけ付ける）。 */
  autoScoop?: boolean;
}

const rec = { type: "object" } as const;
const bool = { type: "boolean" } as const;
export const GUITAR_TECH_PART_SCHEMA = {
  power: { anyOf: [bool, { type: "string", enum: ["oct"] }, rec] }, oct: bool, palmMute: { anyOf: [bool, { type: "number" }] },
  tremolo: { anyOf: [bool, rec] }, rhythm: { type: "string", enum: ["gallop", "rgallop", "trem", "trem16"] }, swell: { anyOf: [bool, { type: "number" }] },
  legato: bool, ghost: { anyOf: [bool, { type: "number" }, rec] }, harmonize: { anyOf: [bool, rec] }, fingerpick: rec, capo: { type: "number" },
  mask: { anyOf: [{ type: "string" }, rec] }, gtrStyle: { type: "string", enum: Object.keys(GTR_STYLES) }, vibrato: rec, glide: { anyOf: [bool, rec] }, autoScoop: bool,
} as const;

/** AI_SONG_GUIDE のあとに足す、ギターの奏法の説明（`song.mjs guide` が表示する）。詳しくは docs/sound/guitar-technique-deep-guide.md ほかの「実装状況」。 */
export const GUITAR_TECH_GUIDE = `
## ギターの奏法の追加機能（2026-10-11。すべて書いたときだけ働く。既存の曲の音は変わらない）
- 自動しゃくり: \`autoScoop\` はパートにも書ける（\`false\` でそのパートだけ止める）。**\`strum\`・\`power\`・\`fingerpick\` で展開した和音のパートは、既定で自動しゃくりがかからない**（\`strum.scoop:true\` で戻す）。
- パワーコード: \`{"instrument":"guitar","power":true,"notes":"A2:0.5 A2:0.5 C3:1"}\`。notes の音を根音にして5度のパートを足す（\`"power":"oct"\` か \`"oct":true\` でオクターブも。同時発音は6まで）。**distGuitar／crunch は書き出しで5度・オクターブが自動で重なるので使わない**（根音だけ書く）。
- ギャロップ／トレモロ: 音に \`@gallop\`（\`E2:2@gallop\`＝1拍ごとに 0.5! 0.25 0.25 を2回）・\`@rgallop\`（0.25 0.25 0.5!）・\`@trem\`（0.125拍の同音）・\`@trem16\`（0.25拍）。パートに \`"rhythm":"gallop"\` と書くと、1拍以上の音すべてに適用。\`tremolo:true\`（または \`{"rate":0.25,"min":1}\`）は長い音を同音の連なりに。短い同音の連打は禁止の音に近いので、sustain を 1 以上に（\`tremolo\` は 1.6 が既定）。
- パームミュート: \`"palmMute":true\`（または 0.8〜1 の sustain）。sustain 0.9・bright -0.2。\`'\`（スタッカート）の同音連打にしない。
- デッドノート: 音名のかわりに \`x\`（\`x:0.25\`、強く \`x:0.25!\`、弱く \`x:0.25,\`）。音程のない「チッ」を、直前の音を低く（G3 以下）した短い弱い音で鳴らす。パート項目 \`"ghost":0.3\`（または \`{"density":0.3}\`）で、休符の16分の裏に自動で弱いデッドノートを足す。ファンクは3〜4音の和音のパートで（禁止の音 1 に注意）。
- strum.pattern の型の名前: \`pop\`・\`folk6\`・\`skank\`・\`rasgueado\`・\`bossa\`・\`funk-cut\`・\`punk8\`（\`pop-punk\`）・\`waltz\`・\`ballad\`。step・spreadMs・strings の既定も付く（書いた値が優先）。型の文字に \`g\`（ゴースト）・\`m\`（パームミュート。短く切る）・\`>\`（次の1打をアクセント。例 \`>DxDU\`＝1打目だけアクセントのダウン）を追加。
- 指弾き: \`"fingerpick":{"chords":"C Am F G","pattern":"travis","capo":0}\` → 親指のパートと指のパートに展開。型は travis・pima・pimi・arp6・bossaThumb か、p q i m a - . の文字（p/q＝低い弦の親指、i m a＝高い弦3本）。
- カポ: \`strum.capo\`・\`fingerpick.capo\`・パートの \`capo\`（0〜11）。コード名は**鳴る和音**で、押さえる形をカポの分だけ下げて開放弦のフォームにし、鳴る高さは上げる。
- ハモリの自動生成: \`"harmonize":{"interval":-3,"scale":"minor@E"}\`（省略は曲の scale／tonic）。音階の音だけで3度下（\`-3\`）・6度下（\`-6\`）・3度上（\`3\`）を別パートで作る。
- 歌をよける: \`"mask":"メロディ"\`（role に含まれる文字）か \`{"role":"メロディ","gain":0.3}\`。そのパートが鳴っている間はこのパートの音を消し（gain があれば弱く）、休符だけ残す。
- グライド: パートに \`"glide":{"depth":100,"rate":0.2}\`（または true）で、1拍以上の音がゆっくり不規則に ±100セントほど揺れる（シューゲイザー）。ベンドを書いた音には効かない。
- ビブラートの段階: \`~.\`（弱）・\`~\`・\`~~\`・\`~~~\`（最大。ピッチベンドで ±30セントほど自前で揺らす）。パート項目 \`"vibrato":{"rate":5.5,"depth":30,"delay":0.4}\` は、~ を付けた音を自前の揺れ（速さHz・幅セント・遅れ拍）にする。ベンドした音に付けると、上がりきってから揺れる（ベンドビブラート）。
- ベンドの形: \`^^@0.25\`（0.25拍で上がる）、\`/@0.1\`（0.1拍でしゃくり上がる）、\`\\\\@0.5\`（音の半分から戻す。JSON 内では \`\\\\\\\\@0.5\`）。スライド \`A4:1>D5\`（同じ長さの中で D5 へなめらかに。範囲は±12半音）。ユニゾンベンド \`D5:3!u(E5)\`（D5 を E5 まで上げ、E5 を弾く別パートを作る。ベンド量は自動）。
- スウェル: 音に \`<\`（音量が立ち上がる）・\`>\`（減っていく）。パート項目 \`"swell":true\` は1拍以上の音に \`<\` を付け、attack を 0.7 にする。
- legato: パートに \`"legato":true\` で、0.25拍以下で続く3音以上を \`_\` でつなぎ山なりの強弱を付ける。
- ギターの型: \`"gtrStyle":"melocore"\`（thrash・shoegaze・funkCut・ballad・bossa）。amp・sustain・doubleDetune などを一括で入れる（パートに書いた値が優先。禁止の音の作り方は入れていない）。
- 検査（\`node tools/audio-check/score-check.mjs 曲.json\`）: ソロ（頂点の位置・休符の割合・~ ^ の予算）、表現の過多（短い音の ~・^、全音に ~、同じ深さの ~ の連続、同音の短い連打）、音域（歪みの刻みが A3 超など）を警告する。解析だけで、曲は変えない。
`;
