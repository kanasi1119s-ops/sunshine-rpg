import { fillBeats, overwriteRange, pickFill, placeFill, type FillSize } from "./drum-fills";
import { midiToName } from "./compose";
import { noteNameToMidi } from "./note";
import { REST, type Instrument, type NoteEvent, type Track } from "./score";

/**
 * 自動の伴奏に「曲の起伏」をつける（セクション編曲）。
 * 曲をセクション（導入・Aメロ・Bメロ・サビ・間奏・Cメロ・終わり、ビルド・ブレイク・ドロップ・ソロ・余韻）に区切り、セクションごとに鳴らす楽器と強さを変える。
 * 自動の伴奏は最初から最後まで同じなので、そのままだと平らに聞こえる。これで「静か → 盛り上がる → サビで全部」の流れができる。
 *
 * 2026-10-11 の拡張（docs/sound/arrangement-deep.md §11）:
 * - 新しい種類 build / break / drop / solo / tag
 * - セクションごとのつなぎ（transition）: 1拍止める・1小節止める・助走（ライザー）・キメ
 * - 群の上書き（layers）、2回目の登場で足す（occurrence）、クラッシュの位置（crashAt）
 * - 手書きパートのセクション別の出し入れ（applyPartSections）、後半の転調（transposeTrack）
 * - 編曲チェッカー（checkArrangement）
 * 場面プリセット（scene）とエネルギー曲線（energy）は scene.ts。
 */
export type SectionKind = "intro" | "verse" | "pre" | "chorus" | "interlude" | "bridge" | "outro" | "build" | "break" | "drop" | "solo" | "tag";
/** この場面に入るときのつなぎ。fill＝おかず（既定）、none＝何もしない、stopBeat＝直前の1拍を全休止、riser＝直前の2小節で強くしてハイハットを16分に、break1bar＝直前の1小節を全休止、kime＝直前の1小節を全員で同じリズムのキメに。 */
export type Transition = "fill" | "none" | "stopBeat" | "riser" | "break1bar" | "kime";
export interface Section {
  kind: SectionKind;
  bars: number;
  /** この場面に入るときのつなぎ。省略は fill（break と drop の前は stopBeat）。 */
  from?: Transition;
  /** この場面の頭にクラッシュを置くか（true＝標準の強さ、数字＝強さ）。省略は crashAt の決まりに従う。 */
  crash?: boolean | number;
}

export const SECTION_KINDS: SectionKind[] = ["intro", "verse", "pre", "chorus", "interlude", "bridge", "outro", "build", "break", "drop", "solo", "tag"];
export const TRANSITIONS: Transition[] = ["fill", "none", "stopBeat", "riser", "break1bar", "kime"];
export const SECTION_LABELS: Record<SectionKind, string> = {
  intro: "導入", verse: "Aメロ", pre: "Bメロ", chorus: "サビ", interlude: "間奏", bridge: "Cメロ", outro: "終わり",
  build: "ビルド", break: "ブレイク", drop: "ドロップ", solo: "ソロ", tag: "余韻",
};

/** 自動の伴奏の楽器の群。pad・brass・perc は、layers で別々に出し入れしたいときだけ使う（指定がなければ pad・choir・brass は strings、tom は snare に含まれる）。 */
export type Group = "kick" | "hat" | "snare" | "bass" | "keys" | "guitar" | "strings" | "pad" | "brass" | "perc";
export const GROUPS: Group[] = ["kick", "hat", "snare", "bass", "keys", "guitar", "strings", "pad", "brass", "perc"];
const FINE_GROUPS: Group[] = ["pad", "brass", "perc"];
const GROUP_OF: Partial<Record<Instrument, Group>> = {
  kick: "kick", hihat: "hat", snare: "snare", tom: "snare", bass: "bass", sub808: "bass",
  piano: "keys", keys: "keys", harpsichord: "keys", bell: "keys", harp: "keys",
  guitar: "guitar", echoGuitar: "guitar", crunch: "guitar", distGuitar: "guitar",
  strings: "strings", pad: "strings", choir: "strings", brass: "strings",
};
const FINE_OF: Partial<Record<Instrument, Group>> = { pad: "pad", choir: "pad", brass: "brass", tom: "perc" };

export interface Layer {
  groups: Group[]; from: number; to: number;
  /** 頭の1拍の kick と bass を強く（ドロップの「同時復帰」）。 */
  accentFirst?: boolean;
  /** 1小節に最初の1音だけを、小節の長さまで伸ばす（長音のみ）。 */
  hold?: boolean;
  /** この場面の頭にクラッシュ。 */
  crash?: boolean;
}
/** layers の1件。群の並びだけ、または { groups, from, to, … }。 */
export type LayerSpec = Group[] | Partial<Layer>;
/** セクションごとの、鳴らす楽器の組と、強さ（始め → 終わり。1が元の強さ）。 */
const LAYERS: Record<SectionKind, Layer> = {
  intro: { groups: ["keys", "strings"], from: 0.75, to: 0.95 },
  verse: { groups: ["kick", "hat", "bass", "keys", "strings"], from: 0.85, to: 0.9 },
  pre: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 0.85, to: 1.0 },
  chorus: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 1.0, to: 1.0 },
  interlude: { groups: ["bass", "keys", "guitar", "strings"], from: 0.9, to: 0.9 },
  bridge: { groups: ["bass", "keys", "strings"], from: 0.8, to: 0.9 },
  outro: { groups: ["bass", "keys", "strings"], from: 0.9, to: 0.5 },
  // 以下は 2026-10-11 に追加
  build: { groups: ["kick", "hat", "snare", "bass"], from: 0.7, to: 1.0 },
  break: { groups: ["keys", "strings"], from: 0.6, to: 0.6 },
  drop: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 1.0, to: 1.0, accentFirst: true, crash: true },
  solo: { groups: ["kick", "hat", "snare", "bass", "guitar"], from: 0.7, to: 0.75 },
  tag: { groups: ["bass", "keys", "strings"], from: 0.7, to: 0.4, hold: true },
};
/** 同じ種類の2回目以降（occurrence: true のとき）に足す群。 */
const ADD_ON: Record<SectionKind, Group[]> = {
  intro: ["bass"], verse: ["guitar"], pre: [], chorus: [], interlude: ["hat"], bridge: ["guitar"], outro: [],
  build: [], break: [], drop: [], solo: ["strings"], tag: [],
};

export type CrashAt = SectionKind | "last" | "afterBridge";
export interface ArrangeOptions {
  /** 種類ごとの群の上書き。 */
  layers?: Partial<Record<SectionKind, LayerSpec>>;
  /** セクションの順番ごとの群（energy から作る）。layers より優先。 */
  perSection?: Layer[];
  /** true なら、同じ種類の2回目以降に ADD_ON の群を足して少し強くする。 */
  occurrence?: boolean;
  /** クラッシュを置くセクション。省略は ["chorus", "drop"]。"last"＝最後のサビ／ドロップを強く、"afterBridge"＝Cメロのあとの場面の頭。 */
  crashAt?: CrashAt[];
  /** true なら、セクションごとにベースの密度を変える（Aメロ＝4分・サビ＝8分の裏がオクターブ・終わり＝根音1音）。 */
  bassDensity?: boolean;
}

const mergeLayer = (base: Layer, spec: LayerSpec | undefined): Layer => (!spec ? base : Array.isArray(spec) ? { ...base, groups: spec } : { ...base, ...spec, groups: spec.groups ?? base.groups });

/** セクションごとの、実際に使う群と強さ。 */
export function resolveLayers(sections: Section[], opts: ArrangeOptions = {}): Layer[] {
  const seen: Partial<Record<SectionKind, number>> = {};
  return sections.map((s, i) => {
    const n = seen[s.kind] ?? 0;
    seen[s.kind] = n + 1;
    const ps = opts.perSection?.[i];
    if (ps) return ps;
    const base = mergeLayer(LAYERS[s.kind], opts.layers?.[s.kind]);
    if (!opts.occurrence || n === 0) return base;
    return { ...base, groups: [...new Set([...base.groups, ...ADD_ON[s.kind]])], from: Math.min(1.05, base.from + 0.05), to: Math.min(1.05, base.to + 0.05) };
  });
}

/** layers の生のJSONを確かめる。まちがいは warnings に足して、使えるものだけ返す。 */
export function parseLayers(raw: unknown, warnings: string[]): Partial<Record<SectionKind, LayerSpec>> | undefined {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return undefined;
  const out: Partial<Record<SectionKind, LayerSpec>> = {};
  for (const [k, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!SECTION_KINDS.includes(k as SectionKind)) { warnings.push(`layers.${k}: 「${k}」は使えません（${SECTION_KINDS.join("・")}）。無視しました`); continue; }
    const pick = (arr: unknown): Group[] => {
      const list = Array.isArray(arr) ? arr : [];
      const ok = list.filter((g): g is Group => GROUPS.includes(g as Group));
      if (ok.length !== list.length) warnings.push(`layers.${k}: 使えない群を無視しました（使える群: ${GROUPS.join("・")}）`);
      return ok;
    };
    if (Array.isArray(v)) out[k as SectionKind] = pick(v);
    else if (v && typeof v === "object") {
      const o = v as Record<string, unknown>;
      const spec: Partial<Layer> = {};
      if (o.groups !== undefined) spec.groups = pick(o.groups);
      if (Number.isFinite(Number(o.from)) && o.from !== undefined) spec.from = Math.max(0, Math.min(1.3, Number(o.from)));
      if (Number.isFinite(Number(o.to)) && o.to !== undefined) spec.to = Math.max(0, Math.min(1.3, Number(o.to)));
      if (o.accentFirst === true) spec.accentFirst = true;
      if (o.hold === true) spec.hold = true;
      if (o.crash === true) spec.crash = true;
      out[k as SectionKind] = spec;
    }
  }
  return Object.keys(out).length ? out : undefined;
}

/** sections の生のJSONを、Section の並びにする。まちがいは warnings に足す。 */
export function parseSections(raw: unknown, warnings: string[]): Section[] {
  const list: Section[] = [];
  if (!Array.isArray(raw)) return list;
  (raw as { kind?: unknown; bars?: unknown; from?: unknown; crash?: unknown }[]).forEach((x, i) => {
    const kind = (x?.kind ?? "") as SectionKind;
    const bars = Math.round(Number(x?.bars));
    if (!SECTION_KINDS.includes(kind)) { warnings.push(`sections[${i}]: 「${String(x?.kind)}」は使えません（${SECTION_KINDS.join("・")} のどれか）。Aメロにしました`); }
    if (!(bars >= 1)) { warnings.push(`sections[${i}]: bars は1以上の整数にしてください`); return; }
    const sec: Section = { kind: SECTION_KINDS.includes(kind) ? kind : "verse", bars };
    if (x?.from !== undefined) {
      if (TRANSITIONS.includes(x.from as Transition)) sec.from = x.from as Transition;
      else warnings.push(`sections[${i}]: from「${String(x.from)}」は使えません（${TRANSITIONS.join("・")}）。無視しました`);
    }
    if (typeof x?.crash === "boolean") sec.crash = x.crash;
    else if (x?.crash !== undefined && Number.isFinite(Number(x.crash))) sec.crash = Math.max(1, Math.min(127, Number(x.crash)));
    list.push(sec);
  });
  return list;
}

/** 小節数から、定番の構成（導入 → A → B → サビ → 間奏 → A → B → サビ → サビ → 終わり）を作る。 */
export function autoSections(totalBars: number): Section[] {
  const out: Section[] = [];
  let left = totalBars;
  const take = (kind: SectionKind, bars: number): void => {
    const n = Math.min(bars, left);
    if (n <= 0) return;
    out.push({ kind, bars: n });
    left -= n;
  };
  const outro = totalBars >= 24 ? 4 : 0;
  if (totalBars >= 16) take("intro", 4);
  left -= outro;
  const body: [SectionKind, number][] = [["verse", 8], ["pre", 4], ["chorus", 8], ["interlude", 4], ["verse", 8], ["pre", 4], ["chorus", 8], ["chorus", 8]];
  for (const [kind, bars] of body) {
    if (left <= 0) break;
    // 残りが2小節以下しかないなら、前のセクションに足す
    if (left - bars > 0 && left - bars < 2) take(kind, left); else take(kind, bars);
  }
  if (left > 0 && out.length) out[out.length - 1].bars += left;
  left = 0;
  if (outro) out.push({ kind: "outro", bars: outro });
  return out;
}

/** 指定されたセクションを、曲の小節数にそろえる。足りなければ最後を延ばし、多ければ切る。直したときは注意の文を返す。 */
export function fitSections(sections: Section[], totalBars: number): { sections: Section[]; warning?: string } {
  const sum = sections.reduce((s, x) => s + x.bars, 0);
  if (sum === totalBars) return { sections };
  const out: Section[] = [];
  let left = totalBars;
  for (const s of sections) {
    if (left <= 0) break;
    const bars = Math.min(s.bars, left);
    out.push({ ...s, bars });
    left -= bars;
  }
  if (left > 0 && out.length) out[out.length - 1].bars += left;
  return { sections: out, warning: `sections の小節数（${sum}）が曲の長さ（${totalBars}小節）とちがうので、${sum < totalBars ? "最後のセクションを延ばしました" : "後ろを切りました"}` };
}


const restOf = (beats: number): NoteEvent => ({ note: REST, durationBeats: beats });
const EPS = 1e-9;

/** 各セクションの始まりの拍と小節。 */
function startsOf(sections: Section[], beatsPerBar: number): { startBars: number[]; startBeats: number[]; totalBars: number } {
  const startBars: number[] = [];
  let at = 0;
  for (const s of sections) { startBars.push(at); at += s.bars; }
  return { startBars, startBeats: startBars.map((b) => b * beatsPerBar), totalBars: at };
}

/** セクション i に入るときのつなぎ（省略は、break・drop の前だけ stopBeat、ほかは fill）。 */
export function transitionInto(sections: Section[], i: number): Transition {
  const s = sections[i];
  if (!s || i === 0) return "none";
  return s.from ?? (s.kind === "break" || s.kind === "drop" ? "stopBeat" : "fill");
}

/** 全パートを止める範囲（拍）。stopBeat（直前の1拍）と break1bar（直前の1小節）。手書きのパートにも使う。 */
export function muteRanges(sections: Section[], beatsPerBar: number): [number, number][] {
  const { startBeats } = startsOf(sections, beatsPerBar);
  const out: [number, number][] = [];
  for (let i = 1; i < sections.length; i++) {
    const t = transitionInto(sections, i);
    if (t === "stopBeat") out.push([startBeats[i] - 1, startBeats[i]]);
    else if (t === "break1bar") out.push([startBeats[i] - beatsPerBar, startBeats[i]]);
  }
  return out.map(([a, b]) => [Math.max(0, a), b]);
}

/** 音の列の指定の範囲を休みにする（またがる音は切る）。 */
export function muteNotes(notes: NoteEvent[], from: number, to: number): NoteEvent[] {
  const total = notes.reduce((a, n) => a + n.durationBeats, 0);
  const end = Math.min(to, total);
  if (end - from <= EPS) return notes;
  return overwriteRange(notes, from, end, [restOf(end - from)]);
}

const firstPitchIn = (notes: NoteEvent[], from: number, to: number): NoteEvent | undefined => {
  let pos = 0;
  for (const n of notes) {
    if (pos >= to - EPS) break;
    if (pos >= from - EPS && n.note !== REST) return n;
    pos += n.durationBeats;
  }
  return undefined;
};

const scaleVel = (n: NoteEvent, g: number): NoteEvent => ({ ...n, velocity: n.velocity !== undefined ? n.velocity * g : g });

/** キメ: 1小節を、全員が同じ位置（1拍目・2拍目のウラ・3拍目）で短く打つ形にする。 */
function kimeBar(notes: NoteEvent[], barStart: number, bpb: number): NoteEvent[] {
  const proto = firstPitchIn(notes, barStart, barStart + bpb);
  if (!proto || bpb < 3) return notes;
  const hit = (): NoteEvent => ({ ...scaleVel(proto, 1.15), durationBeats: 0.5, gate: 0.6 });
  const repl: NoteEvent[] = [hit(), restOf(1), hit(), hit()];
  const used = 2.5;
  if (bpb - used > EPS) repl.push(restOf(bpb - used));
  return overwriteRange(notes, barStart, barStart + bpb, repl);
}

/** 助走（ライザー）: from〜to 拍で強さを 0.75 → 1.2 に上げ、ハイハットを16分にする。 */
function riserRange(tracks: Track[], from: number, to: number): Track[] {
  const span = Math.max(EPS, to - from);
  return tracks.map((t) => {
    if (t.instrument === "crash") return t;
    let pos = 0;
    let notes = t.notes.map((n) => {
      const p = pos;
      pos += n.durationBeats;
      if (n.note === REST || p < from - EPS || p >= to - EPS) return n;
      return scaleVel(n, 0.75 + 0.45 * ((p - from) / span));
    });
    if (t.instrument === "hihat") {
      const proto = firstPitchIn(notes, 0, Infinity);
      if (proto) {
        const cells = Math.round((to - from) / 0.25);
        const repl: NoteEvent[] = Array.from({ length: cells }, (_, k) => ({ ...proto, durationBeats: 0.25, velocity: 80 + 32 * (k / Math.max(1, cells - 1)), open: undefined }));
        notes = overwriteRange(notes, from, to, repl);
      }
    }
    return { ...t, notes };
  });
}

/** ビルドのスネア: 4分 → 8分 → 16分と密にして、強くする。 */
function buildSnare(notes: NoteEvent[], from: number, bars: number, bpb: number): NoteEvent[] {
  const proto = firstPitchIn(notes, 0, Infinity);
  if (!proto) return notes;
  let out = notes;
  for (let b = 0; b < bars; b++) {
    const p = bars > 1 ? b / (bars - 1) : 1;
    const step = p < 0.25 ? 1 : p < 0.75 ? 0.5 : 0.25;
    const count = Math.round(bpb / step);
    const repl: NoteEvent[] = Array.from({ length: count }, (_, k) => ({ ...proto, durationBeats: step, velocity: 66 + 46 * (p * 0.7 + 0.3 * (k / count)) }));
    out = overwriteRange(out, from + b * bpb, from + (b + 1) * bpb, repl);
  }
  return out;
}

/** 長音のみ: 小節ごとに最初の1音を小節の長さまで伸ばす。 */
function holdBars(notes: NoteEvent[], fromBar: number, bars: number, bpb: number): NoteEvent[] {
  let out = notes;
  for (let b = fromBar; b < fromBar + bars; b++) {
    const a = b * bpb;
    const proto = firstPitchIn(out, a, a + bpb);
    if (!proto) continue;
    out = overwriteRange(out, a, a + bpb, [{ ...proto, durationBeats: bpb, gate: 1.2 }]);
  }
  return out;
}

/** 自動の伴奏のトラックに、セクションごとの楽器の出し入れと強弱をかける。メロディなど自分で書いたパートには使わない。 */
export function applySections(tracks: Track[], sections: Section[], beatsPerBar: number, fills = true, opts: ArrangeOptions = {}): Track[] {
  const { startBars: starts, startBeats, totalBars } = startsOf(sections, beatsPerBar);
  const layers = resolveLayers(sections, opts);
  const fine = layers.map((l) => l.groups.some((g) => FINE_GROUPS.includes(g)));
  const sectionAt = (bar: number): number => {
    for (let i = sections.length - 1; i >= 0; i--) if (bar >= starts[i]) return i;
    return 0;
  };
  let crashVolume = 0.08;
  const out: Track[] = [];
  for (const t of tracks) {
    if (t.instrument === "crash") { crashVolume = t.volume || crashVolume; continue; }
    const coarse = t.instrument ? GROUP_OF[t.instrument] : undefined;
    if (!coarse) { out.push(t); continue; }
    let pos = 0;
    const notes: NoteEvent[] = [];
    const push = (n: NoteEvent): void => {
      const last = notes[notes.length - 1];
      if (n.note === REST && last && last.note === REST) last.durationBeats += n.durationBeats;
      else notes.push(n);
    };
    for (const n of t.notes) {
      const bar = Math.min(totalBars - 1, Math.floor(pos / beatsPerBar + 1e-9));
      const si = sectionAt(bar);
      const sec = sections[si];
      const layer = layers[si];
      // pad・brass・perc を別に出し入れする場面では、その楽器は細かい群で数える
      const group = fine[si] ? (FINE_OF[t.instrument as Instrument] ?? coarse) : coarse;
      const lastBar = bar === starts[si] + sec.bars - 1;
      const nextKind = sections[si + 1]?.kind;
      // サビの前の最後の小節は、スネアとキックを足して、サビへの助走にする
      const leadIn = lastBar && nextKind === "chorus" && (group === "snare" || group === "kick") && transitionInto(sections, si + 1) === "fill";
      const on = layer.groups.includes(group) || leadIn;
      if (!on || n.note === REST) push(n.note === REST ? n : restOf(n.durationBeats));
      else {
        const progress = sec.bars > 1 ? (bar - starts[si]) / (sec.bars - 1) : 1;
        let gain = layer.from + (layer.to - layer.from) * progress;
        if (leadIn) gain = Math.max(gain, 1) * (0.9 + 0.1 * ((pos % beatsPerBar) / beatsPerBar));
        // ドロップ: 頭の1拍は kick と bass を強く（同時に戻る）
        if (layer.accentFirst && (group === "kick" || group === "bass") && pos < startBeats[si] + 1 - EPS) gain *= 1.15;
        push({ ...n, ...(n.velocity !== undefined ? { velocity: n.velocity * gain } : gain < 1 || gain > 1 ? { velocity: gain } : {}) });
      }
      pos += n.durationBeats;
    }
    out.push({ ...t, notes: opts.bassDensity && (t.instrument === "bass" || t.instrument === "sub808") ? reshapeBass(notes, sections, starts, beatsPerBar, t.instrument === "bass") : notes });
  }
  // クラッシュ: 既定はサビ（とドロップ）の頭。crashAt・sections[].crash・energy で変えられる
  const crashAt = opts.crashAt ?? ["chorus", "drop"];
  const lastBig = (() => { for (let i = sections.length - 1; i >= 0; i--) if (sections[i].kind === "chorus" || sections[i].kind === "drop") return i; return -1; })();
  const crashNotes: NoteEvent[] = [];
  sections.forEach((s, i) => {
    const startBeat = startBeats[i];
    const doneBeat = crashNotes.reduce((a, n) => a + n.durationBeats, 0);
    let vel = 0;
    if (typeof s.crash === "number") vel = s.crash;
    else if (s.crash === true) vel = 110;
    else if (s.crash === false) vel = 0;
    else {
      const hit = crashAt.includes(s.kind) || layers[i].crash === true || (crashAt.includes("afterBridge") && sections[i - 1]?.kind === "bridge");
      if (hit) vel = 110;
      if (crashAt.includes("last") && i === lastBig && opts.crashAt) vel = 125;
    }
    if (!vel) return;
    if (startBeat > doneBeat + EPS) crashNotes.push(restOf(startBeat - doneBeat));
    else if (startBeat < doneBeat - EPS) return;
    crashNotes.push({ note: "C#3", durationBeats: Math.min(beatsPerBar, 4), velocity: vel });
  });
  const used = crashNotes.reduce((a, n) => a + n.durationBeats, 0);
  const totalBeats = totalBars * beatsPerBar;
  if (crashNotes.length && used < totalBeats - EPS) crashNotes.push(restOf(totalBeats - used));
  if (crashNotes.length) out.push({ waveform: "square", instrument: "crash", volume: crashVolume, pan: -0.3, notes: crashNotes });

  let result = out;
  const edit = (fn: (t: Track) => NoteEvent[], pick: (t: Track) => boolean): void => {
    result = result.map((t) => (pick(t) ? { ...t, notes: fn(t) } : t));
  };
  // おかず: 場面の変わり目（大きさは次の場面で決まる）と、長い場面の4小節ごとの区切り
  if (fills && beatsPerBar >= 3) {
    const counters: Record<FillSize, number> = { small: 0, medium: 0, big: 0, drop: 0 };
    sections.forEach((sec, si) => {
      const groups = layers[si].groups;
      if (!groups.includes("snare") && !groups.includes("kick")) return;
      const quiet = sec.kind === "build" || sec.kind === "break" || sec.kind === "tag";
      for (let b = 0; b < sec.bars; b++) {
        const lastBar = b === sec.bars - 1;
        const wantsFill = !lastBar || transitionInto(sections, si + 1) === "fill";
        const size = lastBar ? (wantsFill ? fillSizeAt(sec.kind, sections[si + 1]?.kind) : undefined) : !quiet && sec.bars >= 8 && b % 4 === 3 && sec.kind !== "intro" ? "small" : undefined;
        if (!size) continue;
        const fill = pickFill(size, counters[size]++, beatsPerBar);
        result = placeFill(result, fill, (starts[si] + b + 1) * beatsPerBar - fillBeats(fill), totalBars * beatsPerBar);
      }
    });
  }
  // ビルド: スネアを4分 → 8分 → 16分と密にする
  sections.forEach((sec, si) => {
    if (sec.kind !== "build" || !layers[si].groups.includes("snare")) return;
    edit((t) => buildSnare(t.notes, startBeats[si], sec.bars, beatsPerBar), (t) => t.instrument === "snare");
  });
  // 長音のみの場面（余韻）
  sections.forEach((sec, si) => {
    if (!layers[si].hold) return;
    edit((t) => holdBars(t.notes, starts[si], sec.bars, beatsPerBar), (t) => !!t.instrument && layers[si].groups.includes(GROUP_OF[t.instrument] ?? ("none" as Group)) && !["kick", "snare", "hihat", "crash", "tom"].includes(t.instrument));
  });
  // つなぎ: 次の場面に入る直前の形
  for (let i = 1; i < sections.length; i++) {
    const t = transitionInto(sections, i);
    const end = startBeats[i];
    if (t === "riser") result = riserRange(result, Math.max(startBeats[i - 1], end - 2 * beatsPerBar), end);
    else if (t === "kime") result = result.map((tr) => {
      if (tr.instrument === "crash" || !tr.instrument || !GROUP_OF[tr.instrument]) return tr;
      return { ...tr, notes: tr.instrument === "hihat" ? muteNotes(tr.notes, end - beatsPerBar, end) : kimeBar(tr.notes, end - beatsPerBar, beatsPerBar) };
    });
  }
  const mutes = muteRanges(sections, beatsPerBar);
  if (mutes.length) result = result.map((tr) => (tr.instrument === "crash" ? tr : { ...tr, notes: mutes.reduce((ns, [a, b]) => muteNotes(ns, a, b), tr.notes) }));
  return result;
}

/**
 * セクションごとのベースの密度（bassline-guide.md §4）: Aメロ＝拍の頭の音だけ（4分）、サビ＝8分の裏をオクターブ上へ（E1〜G3 に収まるときだけ）、
 * 終わり＝小節の頭の根音1音を伸ばす。Bメロ・間奏・Cメロはそのまま。小節をまたぐ音は無い前提（自動の伴奏のベース）。
 */
export function reshapeBass(notes: NoteEvent[], sections: Section[], starts: number[], beatsPerBar: number, octaveTop = true): NoteEvent[] {
  const out: NoteEvent[] = [];
  let pos = 0;
  const push = (n: NoteEvent): void => {
    const last = out[out.length - 1];
    if (n.note === REST && last && last.note === REST) last.durationBeats += n.durationBeats; else out.push(n);
  };
  const isBeat = (x: number): boolean => Math.abs(x - Math.round(x)) < 1e-6;
  const barOf = (x: number): number => Math.floor(x / beatsPerBar + 1e-9);
  const kindAt = (bar: number): SectionKind => {
    for (let i = sections.length - 1; i >= 0; i--) if (bar >= starts[i]) return sections[i].kind;
    return "verse";
  };
  const barFirst = new Map<number, boolean>();
  for (const n of notes) {
    const bar = barOf(pos);
    const kind = kindAt(bar);
    const offset = pos - bar * beatsPerBar;
    if (n.note === REST) { push(n); pos += n.durationBeats; continue; }
    if (kind === "verse" && !isBeat(offset)) push(restOf(n.durationBeats));
    else if (kind === "outro") {
      if (!barFirst.has(bar)) { barFirst.set(bar, true); push({ ...n, durationBeats: Math.min(beatsPerBar, n.durationBeats + (beatsPerBar - offset - n.durationBeats)) }); } else push(restOf(n.durationBeats));
    } else if (kind === "chorus" && octaveTop && Math.abs(offset - Math.floor(offset) - 0.5) < 1e-6) {
      const m = noteNameToMidi(n.note);
      push(m + 12 <= 55 ? { ...n, note: midiToName(m + 12) } : n);
    } else push(n);
    pos += n.durationBeats;
  }
  return out;
}

/** 場面の終わりに入れるおかずの大きさ。次がサビ・ドロップなら大きく（ブリッジからは「止める」）、サビが終わるときは中くらい。 */
function fillSizeAt(kind: SectionKind, next: SectionKind | undefined): FillSize | undefined {
  if (!next) return undefined;
  if (next === "chorus" || next === "drop") return kind === "bridge" ? "drop" : kind === "chorus" || kind === "drop" ? "medium" : "big";
  if (kind === "pre") return "big";
  return "medium";
}

// ───────── 手書きパートのセクション別の出し入れ ─────────
/** パートの sections の1件: 数字＝音量の倍率（0＝休み）、{ gain, octave }。 */
export type PartSectionSpec = Partial<Record<SectionKind, number | { gain?: number; octave?: number }>>;

/** parts[].sections の生のJSONを確かめる。 */
export function parsePartSections(raw: unknown, where: string, warnings: string[]): PartSectionSpec | undefined {
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) return undefined;
  const out: PartSectionSpec = {};
  for (const [k, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!SECTION_KINDS.includes(k as SectionKind)) { warnings.push(`${where}: sections の「${k}」は使えません（${SECTION_KINDS.join("・")}）。無視しました`); continue; }
    if (typeof v === "number" && Number.isFinite(v)) out[k as SectionKind] = Math.max(0, Math.min(2, v));
    else if (typeof v === "boolean") out[k as SectionKind] = v ? 1 : 0;
    else if (v && typeof v === "object") {
      const o = v as Record<string, unknown>;
      out[k as SectionKind] = {
        ...(o.gain !== undefined && Number.isFinite(Number(o.gain)) ? { gain: Math.max(0, Math.min(2, Number(o.gain))) } : {}),
        ...(o.octave !== undefined && Number.isFinite(Number(o.octave)) ? { octave: Math.max(-3, Math.min(3, Math.round(Number(o.octave)))) } : {}),
      };
    } else warnings.push(`${where}: sections.${k} は数字（音量の倍率。0＝休み）か { gain, octave } で書いてください`);
  }
  return Object.keys(out).length ? out : undefined;
}

const SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
/** 音名を半音ずらす。作曲ソフトの範囲（C0〜C8）に収まるようにオクターブを寄せる。読めない名前はそのまま返す。 */
export function transposeNoteName(name: string, semitones: number): string {
  let midi: number;
  try { midi = noteNameToMidi(name); } catch { return name; }
  midi += semitones;
  while (midi > 108) midi -= 12;
  while (midi < 12) midi += 12;
  return `${SHARP_NAMES[midi % 12]}${Math.floor(midi / 12) - 1}`;
}

const DRUM_INSTRUMENTS = new Set<string>(["kick", "snare", "hihat", "crash", "tom"]);
/** 手書きパートに、セクションごとの出し入れ（休む・音量・オクターブ）をかける。 */
export function applyPartSections(notes: NoteEvent[], sections: Section[], beatsPerBar: number, spec: PartSectionSpec, drum: boolean): NoteEvent[] {
  const { startBeats } = startsOf(sections, beatsPerBar);
  const sectionAtBeat = (beat: number): number => {
    for (let i = sections.length - 1; i >= 0; i--) if (beat >= startBeats[i] - EPS) return i;
    return 0;
  };
  let pos = 0;
  const out: NoteEvent[] = [];
  const push = (n: NoteEvent): void => {
    const last = out[out.length - 1];
    if (n.note === REST && last && last.note === REST) last.durationBeats += n.durationBeats;
    else out.push(n);
  };
  for (const n of notes) {
    const v = spec[sections[sectionAtBeat(pos)]?.kind];
    pos += n.durationBeats;
    const gain = v === undefined ? 1 : typeof v === "number" ? v : v.gain ?? 1;
    const octave = v === undefined || typeof v === "number" ? 0 : v.octave ?? 0;
    if (n.note === REST) { push(n); continue; }
    if (gain <= 0) { push(restOf(n.durationBeats)); continue; }
    push({ ...n, ...(drum || !octave ? {} : { note: transposeNoteName(n.note, octave * 12) }), ...(gain !== 1 ? { velocity: (n.velocity ?? 1) * gain } : {}) });
  }
  return out;
}

/** 全パート止めるつなぎ（stopBeat・break1bar）を、手書きパートにもかける。 */
export function applyMutesToNotes(notes: NoteEvent[], ranges: [number, number][]): NoteEvent[] {
  return ranges.reduce((ns, [a, b]) => muteNotes(ns, a, b), notes);
}

// ───────── 転調 ─────────
export interface Modulate {
  /** 転調する小節（1から数える）。 */
  atBar?: number;
  /** atBar のかわりに: 最後のサビ／ドロップの頭（"lastChorus"）か、Cメロ（ブリッジ）が終わった次の場面の頭（"afterBridge"）。 */
  at?: "lastChorus" | "afterBridge";
  /** 上げる半音の数（1＝半音、2＝全音、3＝短3度。-12〜12、0以外）。 */
  semitones: number;
}

/** modulate の生のJSONを確かめて、転調する拍と半音を返す。使えないときは null。 */
export function resolveModulate(raw: unknown, sections: Section[] | undefined, beatsPerBar: number, totalBars: number, warnings: string[]): { atBeat: number; semitones: number } | null {
  if (!raw || typeof raw !== "object") return null;
  const m = raw as Record<string, unknown>;
  const semitones = Math.round(Number(m.semitones));
  if (!(semitones >= -12 && semitones <= 12) || semitones === 0) { warnings.push("modulate.semitones は -12〜12 の0でない整数にしてください（1＝半音上げ、2＝全音上げ）。転調しません"); return null; }
  let bar: number | undefined;
  if (m.atBar !== undefined && Number.isFinite(Number(m.atBar))) bar = Math.round(Number(m.atBar));
  else if (m.at === "lastChorus" || m.at === "afterBridge") {
    if (!sections?.length) { warnings.push(`modulate.at「${m.at}」には sections（または scene）が必要です。転調しません`); return null; }
    const { startBars } = startsOf(sections, beatsPerBar);
    let idx = -1;
    if (m.at === "lastChorus") { for (let i = sections.length - 1; i >= 0; i--) if (sections[i].kind === "chorus" || sections[i].kind === "drop") { idx = i; break; } }
    else { for (let i = 1; i < sections.length; i++) if (sections[i - 1].kind === "bridge") { idx = i; break; } }
    if (idx < 0) { warnings.push(`modulate.at「${m.at}」に当たるセクションがないので、転調しません`); return null; }
    bar = startBars[idx] + 1;
  }
  if (bar === undefined) { warnings.push("modulate には atBar（小節番号）か at（lastChorus・afterBridge）が必要です。転調しません"); return null; }
  if (bar < 2 || bar > totalBars) { warnings.push(`modulate.atBar は 2〜${totalBars} の小節にしてください（${bar}）。転調しません`); return null; }
  return { atBeat: (bar - 1) * beatsPerBar, semitones };
}

/** atBeat 以降の音を半音ずらす（ドラムは動かさない）。 */
export function transposeTrack(track: Track, semitones: number, atBeat: number): Track {
  if (!semitones || (track.instrument && DRUM_INSTRUMENTS.has(track.instrument))) return track;
  let pos = 0;
  return { ...track, notes: track.notes.map((n) => { const p = pos; pos += n.durationBeats; return n.note === REST || p < atBeat - EPS ? n : { ...n, note: transposeNoteName(n.note, semitones) }; }) };
}

// ───────── 編曲チェッカー ─────────
/** 編曲の静的チェック。小節番号と直し方を添えた注意の文を返す。strict＝自分で決めた構成のとき（auto でないとき）だけ見る項目を含める。 */
export function checkArrangement(sections: Section[], beatsPerBar: number, opts: ArrangeOptions = {}, strict = true): string[] {
  const warnings: string[] = [];
  if (sections.length < 2) return warnings;
  const { startBars } = startsOf(sections, beatsPerBar);
  const layers = resolveLayers(sections, opts);
  const label = (i: number): string => SECTION_LABELS[sections[i].kind];
  // 1. 変わり目が弱い（群の差が1つ以下で、強さの段差も小さく、クラッシュや特別なつなぎもない）
  for (let i = 1; i < sections.length; i++) {
    const a = new Set(layers[i - 1].groups);
    const b = new Set(layers[i].groups);
    const diff = [...a].filter((g) => !b.has(g)).length + [...b].filter((g) => !a.has(g)).length;
    const jump = Math.abs(layers[i].from - layers[i - 1].to);
    const t = transitionInto(sections, i);
    const marked = (t !== "fill" && t !== "none") || sections[i].crash || layers[i].crash || ["chorus", "drop", "outro", "tag", "intro"].includes(sections[i].kind);
    if (diff <= 1 && jump < 0.08 && !marked) {
      warnings.push(`${startBars[i] + 1}小節目: 前のセクション（${label(i - 1)}）と鳴る楽器がほぼ同じで、変わり目が弱いです。hat を細かくする、strings を足す、sections の from に stopBeat や riser を指定する、のどれかを`);
    }
  }
  // 2. サビがAメロより薄い
  const firstVerse = sections.findIndex((s) => s.kind === "verse");
  const firstChorus = sections.findIndex((s) => s.kind === "chorus" || s.kind === "drop");
  if (firstVerse >= 0 && firstChorus >= 0 && (layers[firstChorus].groups.length < layers[firstVerse].groups.length || layers[firstChorus].to < layers[firstVerse].from - 1e-9)) {
    warnings.push(`${startBars[firstChorus] + 1}小節目: サビの鳴る楽器または強さが、Aメロ（${startBars[firstVerse] + 1}小節目）以下です。サビを一番厚くしてください（layers か energy で）`);
  }
  // 3. 最後のサビの前に、止める・減らす場所がない（自分で構成を決めた曲だけ）
  if (strict) {
    let last = -1;
    for (let i = sections.length - 1; i >= 1; i--) if (sections[i].kind === "chorus" || sections[i].kind === "drop") { last = i; break; }
    const chorusCount = sections.filter((s) => s.kind === "chorus" || s.kind === "drop").length;
    if (last >= 1 && chorusCount >= 2) {
      const t = transitionInto(sections, last);
      const reduced = layers[last - 1].groups.length < layers[last].groups.length || ["bridge", "break"].includes(sections[last - 1].kind);
      if (!reduced && t !== "stopBeat" && t !== "break1bar" && t !== "kime") {
        warnings.push(`${startBars[last] + 1}小節目: 最後のサビの直前に、止める・減らす場所がありません。直前に bridge か break を置くか、このサビに "from":"stopBeat" を付けてください`);
      }
    }
  }
  return warnings;
}
