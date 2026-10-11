import type { Group, Section } from "./arrangement";
import { GROUPS } from "./arrangement";
import { midiToName } from "./compose";
import { restTokens } from "./motif";
import { noteNameToMidi } from "./note";
import { resampleEnergy, sceneSections, type EnergyCurve } from "./scene";
import { expandBars } from "./song-plan";

/**
 * 周回の差分 lap2（docs/sound/form-structure-guide.md §12 の提案9、game-music-guide.md §10 の提案5）。
 * 曲全体を2〜4周分に展開して、2周目以降に「楽器を足す・強さを上げる・旋律を1オクターブ上げる・おかず（旋律）を替える」差をつける。
 * 短い曲を、飽きさせずに延ばす手段。occurrence の上位互換（周回ごとに、群・音量・パートごとの差を指定できる）。
 *
 *   "laps": 2,
 *   "lap2": { "add": ["guitar"], "gain": 0.05, "energyDelta": 1,
 *             "parts": { "lead": { "octave": 1 }, "pad": { "notes": "C4:4 …（2周目のぶんの音）" } },
 *             "addParts": [ { "instrument": "bell", "role": "鐘", "volume": 0.12, "pan": 0.4, "notes": "C6:2 R:2" } ] }
 *   "laps": "auto"  … scene ごとの標準の周回数（町・村・フィールド・ダンジョン・城・神殿・謎・宿屋・戦闘は2周）
 * 3周目以降は lap3・lap4 があればそれ、なければ lap2 の差を使う。書かなければ（laps なし）何も変えない。
 */
export interface LapDiff {
  /** 足す群（sections の add になる）。 */
  add?: string[];
  /** 強さに足す量（sections の gain。-0.3〜0.3）。 */
  gain?: number;
  /** energy を使っている曲で、この周の energy に足す値。 */
  energyDelta?: number;
  /** パートごとの差。キーは role か instrument。 */
  parts?: Record<string, { octave?: number; notes?: string }>;
  /** この周から鳴らす新しいパート（その周の頭から。前の周は休み）。 */
  addParts?: ({ instrument: string; role?: string; volume?: number; pan?: number; notes: string } & Record<string, unknown>)[];
}

export interface LapsFields {
  laps?: unknown;
  lap2?: unknown;
  lap3?: unknown;
  lap4?: unknown;
  scene?: string;
  chords: string;
  barsPerChord: number;
  repeats: number;
  sections?: unknown;
  sectionChords?: Record<string, string>;
  energy?: unknown;
  occurrence?: boolean;
  beats: number;
  parts: { instrument: string; role?: string; notes: string }[];
}

/** laps: "auto" のときの、scene ごとの標準の周回数。 */
export const SCENE_LAPS: Record<string, number> = { town: 2, village: 2, field: 2, dungeon: 2, castle: 2, shrine: 2, mystery: 2, inn: 2, battle: 2 };

const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const TOKEN = /^([^:]+):(\d+(?:\.\d+)?)(.*)$/;
const fmt = (x: number): string => String(Math.round(x * 10000) / 10000);

/** 音の並びを、ちょうど beats 拍ぶんの並びにする（短ければくり返す、長ければ切る）。 */
export function fitTokens(notes: string, beats: number): string[] {
  const toks = notes.trim().split(/\s+/).filter(Boolean);
  const out: string[] = [];
  if (!toks.some((t) => TOKEN.test(t))) return restTokens(beats);
  let pos = 0;
  for (let i = 0; pos < beats - 1e-9 && i < 100000; i++) {
    const tok = toks[i % toks.length];
    const m = TOKEN.exec(tok);
    if (!m) continue;
    const d = Number(m[2]);
    if (!(d > 0)) continue;
    if (pos + d > beats + 1e-9) { if (m[1] === "R" || m[1] === "r") out.push(...restTokens(beats - pos)); else out.push(`${m[1]}:${fmt(beats - pos)}${m[3]}`); pos = beats; break; }
    out.push(tok);
    pos += d;
  }
  return out;
}

function shiftOctave(tokens: string[], oct: number): string[] {
  if (!oct) return tokens;
  return tokens.map((t) => {
    const m = TOKEN.exec(t);
    if (!m || m[1] === "R" || m[1] === "r" || !/^[A-G][#b]?-?\d$/.test(m[1])) return t;
    try {
      const midi = noteNameToMidi(m[1]) + 12 * oct;
      return midi < 12 || midi > 108 ? t : `${midiToName(midi)}:${m[2]}${m[3]}`;
    } catch { return t; }
  });
}

const sumBeats = (notes: string): number => notes.trim().split(/\s+/).reduce((s, t) => s + (TOKEN.exec(t) ? Number(TOKEN.exec(t)![2]) : 0), 0);

export function expandLaps<T extends LapsFields>(song: T, warnings: string[] = []): T {
  if (!song || typeof song !== "object" || song.laps === undefined || song.laps === null) return song;
  let n: number;
  if (song.laps === "auto") {
    n = song.scene ? SCENE_LAPS[song.scene] ?? 1 : 1;
  } else n = Math.round(Number(song.laps));
  if (!(n >= 1 && n <= 4)) { warnings.push(`laps は 2〜4 の整数か "auto" にしてください（${String(song.laps)}）。無視しました`); return song; }
  if (n === 1) return song;
  const beats = Number(song.beats) || 4;
  const bpc = song.barsPerChord === 2 ? 2 : 1;
  const out: T = { ...song };

  // 1周ぶんの小節数と、sections（明示）
  let lapBars: number;
  let lapSections: Section[] | undefined;
  if (Array.isArray(song.sections)) {
    lapSections = (song.sections as Section[]).map((s) => ({ ...s }));
    lapBars = lapSections.reduce((a, s) => a + (Number(s.bars) || 0), 0);
  } else {
    try { lapBars = expandBars(song.chords, bpc).length * Math.max(1, Math.round(Number(song.repeats) || 1)); } catch { warnings.push("laps: chords が読めないので展開しませんでした"); return song; }
    if (song.sections === undefined && song.scene) lapSections = sceneSections(song.scene, lapBars);
  }
  if (!(lapBars >= 1)) return song;
  const lapBeats = lapBars * beats;

  const diffOf = (k: number): LapDiff => {
    const raw = (k >= 4 ? song.lap4 ?? song.lap3 ?? song.lap2 : k === 3 ? song.lap3 ?? song.lap2 : song.lap2) as LapDiff | undefined;
    return raw && typeof raw === "object" ? raw : {};
  };

  // sections: 周ごとにコピーして、add・gain を付ける
  if (lapSections) {
    const all: Section[] = [];
    for (let k = 1; k <= n; k++) {
      const d = k > 1 ? diffOf(k) : {};
      const add = (d.add ?? []).filter((g): g is Group => GROUPS.includes(g as Group));
      if (d.add && add.length !== d.add.length) warnings.push(`lap${k}.add に使えない群があったので無視しました（${GROUPS.join("・")}）`);
      for (const s of lapSections) {
        const sec: Section = { ...s };
        if (add.length) sec.add = [...new Set([...(s.add ?? []), ...add])];
        if (Number.isFinite(Number(d.gain)) && d.gain) sec.gain = Math.max(-0.3, Math.min(0.3, (s.gain ?? 0) + Number(d.gain)));
        all.push(sec);
      }
    }
    out.sections = all;
  } else if (diffOf(2).add || diffOf(2).gain) {
    warnings.push("laps: lap2 の add・gain を使うには sections（または scene）が必要です。パートの差だけ入れました");
  }

  // コードと長さ
  if (song.sectionChords && Array.isArray(song.sections)) {
    // sectionChords は sections から進行を作るので、sections を増やすだけでよい
  } else out.repeats = Math.max(1, Math.round(Number(song.repeats) || 1)) * n;

  // energy: 周ごとにコピー（曲線の名前は、1周の sections の数に展開してから）
  if (song.energy !== undefined && lapSections) {
    const count = lapSections.length;
    let lv: number[] | null = null;
    if (Array.isArray(song.energy) && song.energy.length && song.energy.every((x) => Number.isFinite(Number(x)))) lv = resampleEnergy(song.energy.map(Number), count);
    else if (typeof song.energy === "string") { try { lv = resampleEnergy(song.energy as EnergyCurve, count); } catch { lv = null; } }
    if (lv && lv.length) {
      const all: number[] = [];
      for (let k = 1; k <= n; k++) { const d = k > 1 ? Number(diffOf(k).energyDelta) || 0 : 0; all.push(...lv.map((x) => Math.max(1, Math.min(10, x + d)))); }
      out.energy = all;
    }
  }
  if (out.occurrence === undefined && lapSections) out.occurrence = true;

  // パート
  const newParts: LapsFields["parts"] = [];
  const fullKey = (p: LapsFields["parts"][number]): string[] => [String(p.role ?? ""), String(p.instrument)];
  for (const p of song.parts ?? []) {
    if (!p || typeof p.notes !== "string") { newParts.push(p); continue; }
    const has = (k: number): boolean => { const d = diffOf(k).parts; return !!d && fullKey(p).some((key) => key && d[key]); };
    const drum = DRUMS.has(String(p.instrument));
    const len = sumBeats(p.notes);
    // 手書きが n 周ぶんの長さなら、そのまま使う
    if (len > lapBeats + 1e-6) {
      if (Array.from({ length: n - 1 }, (_, i) => has(i + 2)).some(Boolean)) warnings.push(`laps: パート「${p.role ?? p.instrument}」の notes が1周（${lapBeats}拍）より長いので、lap の parts の差は使いませんでした`);
      newParts.push(p);
      continue;
    }
    if (drum && !Array.from({ length: n - 1 }, (_, i) => has(i + 2)).some(Boolean)) { newParts.push(p); continue; }
    if (drum && /(^|\s)g:/i.test(p.notes)) { newParts.push(p); continue; }
    const base = fitTokens(p.notes, lapBeats);
    const all: string[] = [...base];
    for (let k = 2; k <= n; k++) {
      const d = diffOf(k).parts;
      const key = d ? fullKey(p).find((x) => x && d[x]) : undefined;
      const spec = key ? d![key] : undefined;
      let toks = spec?.notes ? fitTokens(spec.notes, lapBeats) : base;
      if (spec?.octave) toks = shiftOctave(toks, Math.round(spec.octave));
      all.push(...toks);
    }
    newParts.push({ ...p, notes: all.join(" ") });
  }
  // 周回から入る新しいパート
  for (let k = 2; k <= n; k++) {
    for (const ap of diffOf(k).addParts ?? []) {
      if (!ap || typeof ap.notes !== "string" || !ap.instrument) { warnings.push(`lap${k}.addParts: instrument と notes が必要です。飛ばしました`); continue; }
      const mine = newParts.find((x) => (x as { __lapAdd?: string }).__lapAdd === `${ap.instrument}/${ap.role ?? ""}`);
      const body = fitTokens(ap.notes, lapBeats);
      if (mine && k > 2) { mine.notes = `${mine.notes} ${body.join(" ")}`; continue; }
      const lead = lapBeats * (k - 1);
      newParts.push({ volume: 0.15, pan: 0, role: "足したパート", amp: "auto", ...ap, notes: `${restTokens(lead).join(" ")} ${body.join(" ")}`, __lapAdd: `${ap.instrument}/${ap.role ?? ""}` } as LapsFields["parts"][number]);
    }
  }
  // 足したパートが後の周にも続く場合は、前の周の分を休みで埋める
  for (const p of newParts) {
    const tag = (p as { __lapAdd?: string }).__lapAdd;
    if (!tag) continue;
    delete (p as { __lapAdd?: string }).__lapAdd;
    const have = sumBeats(p.notes);
    if (have < lapBeats * n - 1e-6) p.notes = `${p.notes} ${restTokens(lapBeats * n - have).join(" ")}`;
  }
  out.parts = newParts as T["parts"];
  return out;
}
