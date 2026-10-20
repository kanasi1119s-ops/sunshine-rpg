import type { AiPart } from "./ai-song";
import { REST, type NoteEvent, type Track } from "./score";
import { INSTRUMENT_RANGES } from "./instrument-range";
import { parseChord } from "./newsong";
import { noteNameToMidi } from "./note";
import { findScale, pitchClassOf, resolveScale, snapNotesToScale, type Scale, type SnapPolicy } from "./scales";
import { realizeRhythm, rhythmPatternLayers } from "./world-rhythms";
import { applyMask, capoVoicing, expandGuitarTech, resolveStrumSpec, vibratoSpecOf, glideSpecOf } from "./guitar-tech";
import type { Section } from "./arrangement";
import { applyRecipe, expandBare, expandCut16, expandGuitarPair, expandReverbPre, expandSectionFx, expandWiden } from "./jpop-clean";

/**
 * パートの「展開」（2026-10-11）。AiPart に書かれた便利な指定を、ふつうのパート（notes つき）に直す。
 * ストローク（strum）・エコー（echo）・自動ダブル（doubleDetune）・ドローン（drone）・リズムの型（pattern）・音階への補正（snap）。
 * 出力は AiPart の並びなので、あとの処理（parseNotes・セクション・転調）はふつうのパートと同じ。展開で増えたパートは 8 パートの数に入れない。
 * docs/sound/instrument-realism-guide.md 提案 6、scales-world-guide.md 提案 8・10、sound-design-basics.md 第 1 弾の積み残し。
 */
export interface ExpandCtx {
  bpm: number;
  beatsPerBar: number;
  /** 曲の長さ（拍）。 */
  totalBeats: number;
  /** 1 小節ごとのコード名（進行をくり返しまで広げたもの）。 */
  chordBars: string[];
  /** 曲の調（0〜11）。ドローンの根音。書かなければ最初のコードの根音。 */
  tonic: number | null;
  /** 曲の音階（snap の補正に使う）。 */
  scale: { scale: Scale; tonic: number } | null;
  /** 曲のセクション（sectionFx・guitarPair・bare が使う。なければ未指定）。 */
  sections?: Section[];
}

export interface StrumSpec {
  /** 弾くコード（"C G Am F"）。書かなければ曲のコード進行。 */
  chords?: string;
  /** コード 1 つが続く小節数（chords を書いたときだけ。省略は 1）。 */
  bars?: number;
  /** 型か型の名前（pop・folk6・skank・rasgueado・bossa・funk-cut・punk8・waltz・ballad。guitar-tech.ts）。1 文字＝1 ステップ。D＝ダウン、d＝弱いダウン、U/u＝アップ（高い弦だけ・弱く）、x＝ミュートしたかき鳴らし、g＝ゴースト（とても弱いミュート）、m＝パームミュート（短く切る）、>＝次の1打をアクセント、.＝前の音をのばす、-＝休み。省略は "D.DU.UDU"（8 分 8 つ）。 */
  pattern?: string;
  /** 1 ステップの長さ（拍）。省略は 0.5。 */
  step?: number;
  /** 弦と弦のずれ（ミリ秒。1 弦あたり）。省略は 12。 */
  spreadMs?: number;
  /** 使う弦の数（3〜6。省略は 5）。 */
  strings?: number;
  /** 弦を次にはじく（またはコードが変わる）まで鳴らし続ける（省略は true）。false で従来の「1ステップ分だけ」。 */
  ring?: boolean;
  /** ring のとき、1 つの音をのばす上限（拍。省略は 2）。 */
  ringMax?: number;
  /** カポ（0〜11。コード名は鳴る和音で、押さえる形をカポの分だけ下げる。パートの capo でもよい）。 */
  capo?: number;
  /** true にすると、展開した和音のパートにも自動しゃくり（autoScoop）をかける（省略は、かけない）。 */
  scoop?: boolean;
}

export interface EchoSpec {
  /** 繰り返す回数（1〜4。省略は 2）。 */
  repeats?: number;
  /** 遅れ。"dotted8"（付点8分。省略）・"quarter"・"eighth"・"triplet8"・"slap"（約 0.07 拍・1 回・decay 0.8）か、拍の数。 */
  time?: string | number;
  /** 遅れをミリ秒で（1〜400。BPM に関係ない。40ms 未満は別の音でなく厚みに聞こえる）。書くと time より優先。decay は 0.95 まで使える。 */
  ms?: number;
  /** 1 回ごとの音量の倍率（0.1〜0.6。省略は 0.3。ms／slap のときは 0.95 まで）。 */
  decay?: number;
}

export interface DoubleDetuneSpec {
  /** ずらす音程（セント。省略は 8）。 */
  cents?: number;
  /** 左右に振る量（0〜1。省略は 0.5）。 */
  spread?: number;
}

const clamp = (v: number, lo: number, hi: number): number => Math.max(lo, Math.min(hi, v));
const fmt = (v: number): string => String(Math.round(v * 1e6) / 1e6);

// ───────── ストローク ─────────
const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nameOf = (m: number): string => `${NOTE_NAMES[m % 12]}${Math.floor(m / 12) - 1}`;
const N = (s: string): number => noteNameToMidi(s);

/** 開放弦のコードフォーム（ガイド 4.1 の表と同じ。低い弦から。鳴らさない弦は含めない）。 */
export const OPEN_CHORD_FORMS: Record<string, number[]> = {
  C: [N("C3"), N("E3"), N("G3"), N("C4"), N("E4")], G: [N("G2"), N("B2"), N("D3"), N("G3"), N("B3"), N("G4")],
  Am: [N("A2"), N("E3"), N("A3"), N("C4"), N("E4")], Em: [N("E2"), N("B2"), N("E3"), N("G3"), N("B3"), N("E4")],
  D: [N("D3"), N("A3"), N("D4"), N("F#4")], Dm: [N("D3"), N("A3"), N("D4"), N("F4")],
  E: [N("E2"), N("B2"), N("E3"), N("G#3"), N("B3"), N("E4")], A: [N("A2"), N("E3"), N("A3"), N("C#4"), N("E4")],
  F: [N("F2"), N("C3"), N("F3"), N("A3"), N("C4"), N("F4")], G7: [N("G2"), N("B2"), N("D3"), N("G3"), N("B3"), N("F4")],
  Am7: [N("A2"), N("E3"), N("G3"), N("C4"), N("E4")], Cmaj7: [N("C3"), N("E3"), N("G3"), N("B3"), N("E4")],
  Fmaj7: [N("F3"), N("A3"), N("C4"), N("E4")], D7: [N("D3"), N("A3"), N("C4"), N("F#4")], E7: [N("E2"), N("B2"), N("D3"), N("G#3"), N("B3"), N("E4")],
  A7: [N("A2"), N("E3"), N("G3"), N("C#4"), N("E4")], Dm7: [N("D3"), N("A3"), N("C4"), N("F4")], Em7: [N("E2"), N("B2"), N("D3"), N("G3"), N("B3"), N("E4")],
};

/** 開放弦のフォームがなければ、根音を E2〜D#3 に置き、5度・根音・3度・5度・根音の順に上へ重ねる（バレーコードの形）。 */
function movableVoicing(name: string): number[] | null {
  const c = parseChord(name);
  if (!c) return null;
  const iv = c.intervals;
  const order = iv.length <= 2 ? [0, 1, 0, 1] : iv.length === 3 ? [0, 2, 0, 1, 2, 0] : [0, 2, 3, 1, 2, 0];
  let m = 40 + ((((c.bass ?? c.root) - 4) % 12) + 12) % 12;
  const out = [m];
  for (const idx of order.slice(1)) {
    const pc = (c.root + iv[idx]) % 12;
    let next = out[out.length - 1] + 1;
    while (next % 12 !== pc) next++;
    out.push(next);
    m = next;
  }
  return out;
}

/** コード名 → 低い弦から高い弦の MIDI 番号（最大 strings 本。多いときは、いちばん低い音と高い音を残して間引く）。 */
export function strumVoicing(chord: string, strings = 5): number[] | null {
  const full = OPEN_CHORD_FORMS[chord] ?? movableVoicing(chord);
  if (!full) return null;
  const n = clamp(Math.round(strings), 3, 6);
  // 弦が多いときは、同じ音名のかさなり（オクターブ違い）から先に間引く（最低音と最高音は残す）。なければ真ん中あたりを間引く
  const out = [...full];
  while (out.length > n) {
    let drop = -1;
    for (let i = 1; i < out.length - 1 && drop < 0; i++) if (out.some((m, j) => j !== i && m % 12 === out[i] % 12)) drop = i;
    if (drop < 0) drop = Math.floor(out.length / 2);
    out.splice(drop, 1);
  }
  return out;
}

const STROKE_CHARS = /^[DdUuxXmMgG>.\-]+$/;

/** ストローク指定を、弦ごとのパート（3〜6 本）に展開する。 */
export function expandStrum(p: AiPart, rawSpec: StrumSpec, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const where = `parts（${p.role ?? p.instrument}）の strum`;
  const spec = resolveStrumSpec(rawSpec, warnings, where);
  const capo = spec.capo ?? p.capo;
  const pattern = (spec.pattern ?? "D.DU.UDU").replace(/[\s|]/g, "");
  if (!pattern || !STROKE_CHARS.test(pattern)) {
    warnings.push(`${where}: pattern は D d U u x . - だけで書きます「${spec.pattern}」。ストロークを作れませんでした`);
    return [p];
  }
  const step = clamp(Number(spec.step) || 0.5, 0.125, 2);
  const stringsN = clamp(Math.round(Number(spec.strings) || 5), 3, 6);
  const TICKS = 960;
  const stepT = Math.round(step * TICKS);
  // コードの並び（1 つ = 何拍か）
  let spans: { chord: string; beats: number }[];
  if (spec.chords && spec.chords.trim()) {
    const bars = Math.max(1, Math.round(Number(spec.bars) || 1));
    spans = spec.chords.trim().split(/[\s|]+/).map((c) => ({ chord: c.replace(/\*\d+$/, ""), beats: bars * ctx.beatsPerBar }));
  } else spans = ctx.chordBars.map((c) => ({ chord: c, beats: ctx.beatsPerBar }));
  if (!spans.length) return [p];
  // 展開した全体の長さが曲より短いときは、くり返す
  const forms: { voicing: number[]; beats: number }[] = [];
  let filled = 0;
  for (let i = 0; filled < ctx.totalBeats - 1e-6 && i < 4096; i++) {
    const s = spans[i % spans.length];
    const voicing = capo ? capoVoicing(s.chord, stringsN, capo) : strumVoicing(s.chord, stringsN);
    if (!voicing) {
      warnings.push(`${where}: コード「${s.chord}」を読めませんでした。strum を使わず、notes のままにしました`);
      return [p];
    }
    forms.push({ voicing, beats: Math.min(s.beats, ctx.totalBeats - filled) });
    filled += s.beats;
  }
  const voiceCount = Math.max(...forms.map((f) => f.voicing.length));
  const spreadBeats = Math.min((clamp(Number(spec.spreadMs) || 12, 0, 60) / 1000) * (ctx.bpm / 60), 0.1 / Math.max(1, voiceCount - 1));
  const spreadT = Math.round(spreadBeats * TICKS);
  // 型を「打つ音（のばしを含む）」と「休み」のならびにする。先頭の「.」は休み扱い
  const tokens: { ch: string; steps: number; accent?: boolean }[] = [];
  let accentNext = false;
  for (const ch of pattern) {
    if (ch === ">") { accentNext = true; continue; }
    const last = tokens[tokens.length - 1];
    if (ch === "." && last && last.ch !== "-") last.steps++;
    else tokens.push({ ch: ch === "." ? "-" : ch, steps: 1, ...(accentNext && ch !== "." && ch !== "-" ? { accent: true } : {}) });
    accentNext = false;
  }
  const events: string[][] = Array.from({ length: voiceCount }, () => []);
  const push = (v: number, name: string | null, ticks: number, marks = ""): void => {
    if (ticks <= 0) return;
    events[v].push(name ? `${name}:${fmt(ticks / TICKS)}${marks}` : `R:${fmt(ticks / TICKS)}`);
  };
  // 実際のギターは、弦をはじいたら次にその弦をはじくまで（またはコードが変わるまで）鳴り続ける。ring（既定: 入）はそれをまねる
  const ring = spec.ring !== false;
  const ringMaxT = Math.round(clamp(Number(spec.ringMax) || 2, 0.25, 8) * TICKS);
  const gapT = Math.round(0.03 * TICKS);
  const palmT = Math.round(0.25 * TICKS);
  type Hit = { t: number; name: string; marks: string; dur: number; short: boolean };
  for (const f of forms) {
    const spanT = Math.round(f.beats * TICKS);
    const vs = f.voicing;
    const hits: Hit[][] = Array.from({ length: voiceCount }, () => []);
    let t = 0;
    for (let ti = 0; t < spanT; ti++) {
      const tok = tokens[ti % tokens.length];
      const dur = Math.min(tok.steps * stepT, spanT - t);
      if (tok.ch === "-") { t += dur; continue; }
      const ch = tok.ch;
      const up = ch === "U" || ch === "u";
      const muted = ch === "x" || ch === "X";
      const ghost = ch === "g" || ch === "G";
      const palm = ch === "m" || ch === "M";
      // 強さ: 1拍目と 2・4 拍（バックビート）を強く、アップは弱く
      const onBeat = t % TICKS === 0;
      const beatNo = Math.floor(t / TICKS) % 4;
      const marks = muted ? (tok.accent ? "!'" : ",'") : ghost ? ",,'" : palm ? (tok.accent ? "!" : ",") : tok.accent ? "!" : up || ch === "d" ? "," : onBeat && (beatNo === 0 || !ring) ? "!" : "";
      // アップは高い弦だけ（半分、少なくとも 2 本）
      const played = up ? vs.map((_, i) => i).slice(-Math.min(vs.length, Math.max(2, Math.ceil(vs.length / 2)))) : vs.map((_, i) => i);
      for (let v = 0; v < voiceCount; v++) {
        const idx = v - (voiceCount - vs.length);
        if (idx < 0 || !played.includes(idx)) continue;
        // ダウンは低い弦から、アップは高い弦から順にずらす（アップは速く）
        const order = up ? played.length - 1 - played.indexOf(idx) : idx - (played[0] ?? 0);
        const off = Math.min(Math.round(order * spreadT * (up ? 0.65 : 1)), Math.floor(dur / 2));
        hits[v].push({ t: t + off, name: nameOf(vs[idx]), marks, dur: dur - off, short: muted || ghost || palm });
      }
      t += dur;
    }
    for (let v = 0; v < voiceCount; v++) {
      let cur = 0;
      const hs = hits[v];
      for (let i = 0; i < hs.length; i++) {
        const h = hs[i];
        if (h.t > cur) push(v, null, h.t - cur);
        const nextT = i + 1 < hs.length ? hs[i + 1].t : spanT;
        let len: number;
        if (!ring) len = h.short ? h.dur : h.dur;
        else if (h.short) len = Math.min(h.dur, palmT);
        else len = Math.min(nextT - h.t - gapT, ringMaxT);
        len = Math.max(Math.round(0.06 * TICKS), Math.min(len, nextT - h.t));
        // パームミュートは、音を短く切ったあと、次の打つまで休む（普通に弾いた直後にいきなりミュートにしない）
        if (!ring && h.short) len = Math.max(1, Math.round(h.dur * 0.7));
        push(v, h.name, len, h.marks);
        cur = h.t + len;
      }
      if (spanT > cur) push(v, null, spanT - cur);
    }
  }
  const vol = Math.max(0.02, (Number(p.volume) || 0.2) / Math.sqrt(voiceCount));
  return events.map((evs, v) => {
    const { strum: _s, ...rest } = p;
    // 展開した和音には、自動しゃくり（キュイン）をかけない（strum.scoop:true で戻す）
    return { ...rest, role: `${p.role ?? p.instrument}・弦${v + 1}`, volume: Math.round(vol * 1000) / 1000, sustain: p.sustain ?? spec.sustainPreset ?? 1.5, ...(spec.scoop ? {} : { autoScoop: p.autoScoop ?? false }), phrase: undefined, notes: evs.join(" ") } as AiPart;
  });
}

// ───────── エコー・自動ダブル ─────────
const ECHO_TIMES: Record<string, number> = { dotted8: 0.75, quarter: 1, eighth: 0.5, triplet8: 1 / 3, slap: 0.07 };

/** エコー: 元のパートの後ろに、遅れて小さくなるコピーを足す。コピーは左右交互に振り、回ごとに暗くする。 */
export function expandEcho(p: AiPart, spec: EchoSpec, warnings: string[], bpm = 120): AiPart[] {
  // ms（ミリ秒）と slap は、短い遅れ用（jpop-clean-guitar-guide.md 提案3）。repeats は 1、decay は 0.8 が標準
  const msGiven = spec.ms !== undefined && Number.isFinite(Number(spec.ms));
  const short = msGiven || spec.time === "slap";
  const delay = msGiven ? Math.round((clamp(Number(spec.ms), 1, 400) / 1000) * (bpm / 60) * 1e6) / 1e6 : typeof spec.time === "number" ? spec.time : ECHO_TIMES[String(spec.time ?? "dotted8")];
  if (!(delay > 0 && delay <= 4)) {
    warnings.push(`echo.time は dotted8・quarter・eighth・triplet8・slap か、0〜4 の拍の数にしてください（${String(spec.time)}）。エコーは付けませんでした`);
    return [p];
  }
  const repeats = clamp(Math.round(Number(spec.repeats) || (short ? 1 : 2)), 1, 4);
  const decay = short ? clamp(Number(spec.decay) || 0.8, 0.1, 0.95) : clamp(Number(spec.decay) || 0.3, 0.1, 0.6);
  const { echo: _e, ...base } = p;
  const out: AiPart[] = [base as AiPart];
  for (let n = 1; n <= repeats; n++) {
    out.push({
      ...base,
      role: `${p.role ?? p.instrument}・エコー${n}`,
      volume: Math.max(0.02, Math.round((Number(p.volume) || 0.2) * decay ** n * 1000) / 1000),
      pan: clamp((Number(p.pan) || 0) + (n % 2 ? 0.4 : -0.4), -1, 1),
      bright: clamp((Number(p.bright) || 0) - 0.2 * n, -1, 0.5),
      shift: Math.round(((Number(p.shift) || 0) + delay * n) * 1e6) / 1e6,
      phrase: p.phrase,
    } as AiPart);
  }
  return out;
}

/** 自動ダブル: 同じ旋律を 2 パートにし、左右に振って、音程を ±cents セントずらす（スーパーソー風の厚み）。 */
export function expandDoubleDetune(p: AiPart, spec: DoubleDetuneSpec | true): AiPart[] {
  const s = spec === true ? {} : spec;
  const cents = clamp(Number(s.cents) || 8, 1, 30);
  const spread = clamp(s.spread === undefined ? 0.5 : Number(s.spread), 0, 1);
  const { doubleDetune: _d, ...base } = p;
  const pan0 = Number(p.pan) || 0;
  const vol = Math.max(0.02, Math.round((Number(p.volume) || 0.2) * 0.75 * 1000) / 1000);
  return [
    { ...base, role: `${p.role ?? p.instrument}・L`, volume: vol, pan: clamp(pan0 - spread, -1, 1), detune: -cents } as AiPart,
    { ...base, role: `${p.role ?? p.instrument}・R`, volume: vol, pan: clamp(pan0 + spread, -1, 1), detune: cents } as AiPart,
  ];
}

/**
 * ダブルトラック（2026-10-20 ラウドロック）: 同じリフを 2 回別々に弾いたように、左右いっぱいの 2 パートにする。
 * 本物の重ね録りは「同じ音を同じタイミングで」ではなく、1音ごとに 5〜20ms ずれ、強さも違う。
 * MIDI の書き出しはチャンネルごとに別のばらつき（midi-export の trackSeed）を使うので、左右を別チャンネルにし、ずれ（humanTiming）を大きくする。
 * 音程は ±2 セントだけ（doubleDetune の ±8 セントのような「うなり」を出さない）。右は別のIR・少し暗い音色・少し浅い歪み（別のマイク・別の弾き方）。
 */
export function expandDoubleTrack(p: AiPart, spec: true | { spread?: number; irR?: string; timing?: number }): AiPart[] {
  const s = spec === true ? {} : spec;
  const spread = clamp(s.spread === undefined ? 1 : Number(s.spread), 0, 1);
  const timing = clamp(s.timing === undefined ? 1.8 : Number(s.timing), 0.5, 3);
  const { double: _d, ...base } = p;
  const pan0 = Number(p.pan) || 0;
  const vol = Math.max(0.02, Math.round((Number(p.volume) || 0.2) * 0.8 * 1000) / 1000);
  const ir = typeof p.ampCabIr === "string" ? p.ampCabIr : undefined;
  const irR = s.irR ?? (ir && ir.includes("+") ? ir.split("+").reverse().join("+") + "+dfc-mixxx" : ir);
  const humanTiming = (Number(p.humanTiming) || 1) * timing;
  return [
    { ...base, role: `${p.role ?? p.instrument}・L`, volume: vol, pan: clamp(pan0 - spread, -1, 1), detune: -2, humanTiming } as AiPart,
    { ...base, role: `${p.role ?? p.instrument}・R`, volume: vol, pan: clamp(pan0 + spread, -1, 1), detune: 2, humanTiming,
      ...(irR ? { ampCabIr: irR } : {}), ampTone: (Number(p.ampTone) || 0) - 0.8, ...(Number(p.ampDrive) > 0 ? { ampDrive: Number(p.ampDrive) * 0.92 } : { ampDrive: 0.92 }) } as AiPart,
  ];
}

// ───────── ドローン・リズムの型・音階への補正 ─────────
/** ドローン: 主音（または主音＋5度）の長い持続音。曲の長さにぴったり合わせる（8 小節ずつ区切る）。 */
export function expandDrone(p: AiPart, ctx: ExpandCtx, warnings: string[]): AiPart[] {
  const kind = p.drone === "root5" ? "root5" : "root";
  let tonic = ctx.tonic;
  if (tonic === null) {
    const c = ctx.chordBars[0] ? parseChord(ctx.chordBars[0]) : null;
    if (c) tonic = c.root;
  }
  if (tonic === null) {
    warnings.push(`parts（${p.role ?? p.instrument}）の drone: 主音（tonic）もコードも読めなかったので、ドローンは作りませんでした`);
    return [p];
  }
  if (String(p.notes ?? "").trim()) warnings.push(`parts（${p.role ?? p.instrument}）: drone を書いたので、notes は使いません`);
  const lo = INSTRUMENT_RANGES[p.instrument]?.safe[0];
  const floor = lo ? noteNameToMidi(lo) : 36;
  let root = floor;
  while (root % 12 !== tonic) root++;
  const chunkBeats = ctx.beatsPerBar * 8;
  const notesFor = (midi: number): string => {
    const toks: string[] = [];
    for (let at = 0; at < ctx.totalBeats - 1e-9; at += chunkBeats) toks.push(`${nameOf(midi)}:${fmt(Math.min(chunkBeats, ctx.totalBeats - at))}`);
    return toks.join(" ");
  };
  const { drone: _d, ...base } = p;
  const first = { ...base, notes: notesFor(root) } as AiPart;
  if (kind === "root") return [first];
  return [first, { ...base, role: `${p.role ?? p.instrument}・5度`, volume: Math.round((Number(p.volume) || 0.1) * 0.8 * 1000) / 1000, notes: notesFor(root + 7) } as AiPart];
}

/** リズムの型の名前を notes に展開する。"taiko2" は 2 つのパート（地打ち・表打ち）になる。 */
export function expandPattern(p: AiPart, drum: boolean, warnings: string[]): AiPart[] {
  const layers = rhythmPatternLayers(String(p.pattern));
  if (!layers.length) {
    warnings.push(`parts（${p.role ?? p.instrument}）: pattern「${String(p.pattern)}」は使えません（son32・rumba32・tresillo・bembe・soleaCompas・taikoJi・taikoOmote・taiko2）`);
    return [p];
  }
  const { pattern: _p, ...base } = p;
  return layers.map((l, i) => ({
    ...base,
    ...(layers.length > 1 ? { role: `${p.role ?? p.instrument}・${l.name}`, pan: i === 0 ? -0.2 : 0.2 } : {}),
    notes: realizeRhythm(l, drum, p.patternNote),
  } as AiPart));
}

/** まとめて展開する。 */
export function expandParts(parts: AiPart[], ctx: ExpandCtx, warnings: string[], drums: Set<string>): AiPart[] {
  const out: AiPart[] = [];
  for (const given of parts) {
    if (!given || typeof given !== "object") { out.push(given); continue; }
    const orig = applyRecipe(given, warnings);
    let list: AiPart[] = [orig];
    const drum = drums.has(orig.instrument);
    if (orig.pattern === "cut16" && !drum) list = list.flatMap((p) => expandCut16(p, ctx, warnings, strumVoicing));
    else if (orig.pattern !== undefined) list = list.flatMap((p) => expandPattern(p, drum, warnings));
    if (orig.bare !== undefined && !drum) list = list.flatMap((p) => (p.bare !== undefined ? expandBare(p, ctx, warnings) : [p]));
    if (orig.guitarPair && !drum) list = list.flatMap((p) => (p.guitarPair ? expandGuitarPair(p, p.guitarPair, ctx, warnings) : [p]));
    if (orig.drone) list = list.flatMap((p) => (p.drone ? expandDrone(p, ctx, warnings) : [p]));
    if (orig.snap && ctx.scale && !drum) {
      const policy: SnapPolicy = orig.snap === "down" || orig.snap === "up" ? orig.snap : "nearest";
      list = list.map((p) => ({ ...p, snap: undefined, notes: snapNotesToScale(String(p.notes ?? ""), ctx.scale!.scale, ctx.scale!.tonic, policy) }));
    } else if (orig.snap && !ctx.scale) warnings.push(`parts（${orig.role ?? orig.instrument}）: snap には、曲の scale（と tonic）を書いてください`);
    if (!drum) list = list.flatMap((p) => expandGuitarTech(p, ctx, warnings));
    if (orig.strum && !drum) list = list.flatMap((p) => (p.strum ? expandStrum(p, p.strum, ctx, warnings) : [p]));
    if (orig.doubleDetune || orig.gtrStyle) list = list.flatMap((p) => (p.doubleDetune ? expandDoubleDetune(p, p.doubleDetune) : [p]));
    if (orig.double && !drum) list = list.flatMap((p) => (p.double ? expandDoubleTrack(p, p.double) : [p]));
    if (orig.widen && !drum) list = list.flatMap((p) => (p.widen ? expandWiden(p, p.widen, ctx) : [p]));
    if (orig.echo) list = list.flatMap((p) => (p.echo ? expandEcho(p, p.echo, warnings, ctx.bpm) : [p]));
    if (orig.sectionFx && !drum) list = list.flatMap((p) => (p.sectionFx ? expandSectionFx(p, p.sectionFx, ctx, warnings) : [p]));
    if (orig.reverbPre !== undefined && !drum) list = list.flatMap((p) => (p.reverbPre !== undefined ? expandReverbPre(p, ctx, warnings) : [p]));
    out.push(...list);
  }
  return out.some((p) => p && typeof p === "object" && p.mask) ? applyMask(out, ctx, warnings, drums) : out;
}

/** 曲のコード進行を、1 小節 1 コードの並びにする（barsPerChord とくり返しを反映）。 */
export function chordBarsOf(chords: string, barsPerChord: number, repeats: number): string[] {
  const toks = String(chords ?? "").split(/[\s|]+/).filter(Boolean).map((c) => c.replace(/\*\d+$/, ""));
  const bars: string[] = [];
  for (const t of toks) for (let i = 0; i < (barsPerChord === 2 ? 2 : 1); i++) bars.push(t);
  const all: string[] = [];
  for (let r = 0; r < Math.max(1, Math.round(repeats) || 1); r++) all.push(...bars);
  return all;
}

/** 曲の scale／tonic の指定を読む。書いていなければ null。読めなければ warnings に足して null。 */
export function readSongScale(scale: unknown, tonic: unknown, warnings: string[]): { scale: Scale; tonic: number } | null {
  if (scale === undefined || scale === null || scale === "") return null;
  const r = resolveScale(String(scale), tonic === undefined ? undefined : String(tonic));
  if (!r) {
    const name = String(scale).split("@")[0];
    warnings.push(findScale(name) ? `tonic「${String(tonic)}」を主音として読めません（例 D, Bb, F#）。音階の点検をしませんでした` : `scale「${String(scale)}」は表にありません（例 miyako, dorian, 都節, hijaz）。音階の点検をしませんでした`);
    return null;
  }
  return r;
}

export { pitchClassOf };

/** 音の並びを beats 拍だけ後ろへずらす（先頭に休符を足し、はみ出した分は切る）。長さは変わらない。 */
export function shiftEvents(events: NoteEvent[], beats: number): NoteEvent[] {
  if (!(beats > 0)) return events;
  const total = events.reduce((s, e) => s + e.durationBeats, 0);
  const out: NoteEvent[] = [{ note: REST, durationBeats: Math.min(beats, total) }];
  let at = Math.min(beats, total);
  for (const e of events) {
    if (at >= total - 1e-9) break;
    const dur = Math.min(e.durationBeats, total - at);
    out.push({ ...e, durationBeats: Math.round(dur * 1e6) / 1e6 });
    at += dur;
  }
  return out;
}

/** ペダルを踏み替える拍（chord＝コードが変わる小節の頭、bar＝毎小節の頭）。 */
export function pedalChanges(mode: "chord" | "bar", chordBars: string[], beatsPerBar: number): number[] {
  const out: number[] = [];
  chordBars.forEach((c, i) => {
    if (i > 0 && (mode === "bar" || c !== chordBars[i - 1])) out.push(i * beatsPerBar);
  });
  return out;
}

/** パートの指定を、Track の項目（detune・attack・release・pedal）にする。 */
export function partTrackExtras(p: AiPart, chordBars: string[], beatsPerBar: number): Partial<Track> {
  const out: Partial<Track> = {};
  const num = (v: unknown): number | null => (v !== undefined && Number.isFinite(Number(v)) ? Number(v) : null);
  const detune = num(p.detune);
  if (detune) out.detune = clamp(detune, -50, 50);
  const attack = num(p.attack);
  if (attack !== null) out.attack = clamp(attack, 0, 1);
  const release = num(p.release);
  if (release !== null) out.release = clamp(release, 0, 1);
  if (typeof p.autoScoop === "boolean") out.autoScoop = p.autoScoop;
  if (p.powerChord === false) out.noPower = true;
  const vib = vibratoSpecOf(p.vibrato);
  if (vib) out.vibratoSpec = vib;
  const gl = glideSpecOf(p.glide);
  if (gl) out.glide = gl;
  if ((p.instrument === "piano" || p.instrument === "keys") && (p.pedal === "chord" || p.pedal === "bar" || p.pedal === "none")) {
    out.pedal = { mode: p.pedal, changes: p.pedal === "none" ? [] : pedalChanges(p.pedal, chordBars, beatsPerBar) };
  }
  return out;
}
