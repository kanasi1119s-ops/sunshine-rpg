import { noteNameToMidi } from "./note";
import { REST, type NoteEvent, type Track } from "./score";

/**
 * 楽器ごとの音域・同時発音・息継ぎの点検（2026-10-11、docs/sound/instrument-realism-guide.md の提案 1〜4）。
 * 数字は同ガイド §5 の表（hard＝奏者がふつうに出せる範囲、safe＝音色が自然な範囲。safe は「補」＝目安）。
 * 警告は日本語で、小節番号つき。入力の間違いではなく、直すと本物らしくなるヒント。
 */
export interface InstrumentRange {
  hard: [string, string];
  safe: [string, string];
}
const R = (hl: string, hh: string, sl = hl, sh = hh): InstrumentRange => ({ hard: [hl, hh], safe: [sl, sh] });

export const INSTRUMENT_RANGES: Record<string, InstrumentRange> = {
  bass: R("B0", "G4", "E1", "D3"), slap: R("B0", "G4", "E1", "G3"), sub808: R("C1", "C3", "E1", "C3"),
  guitar: R("E2", "E6", "E2", "E5"), crunch: R("E2", "E6", "E2", "E5"), distGuitar: R("E2", "E5", "E2", "E4"),
  leadGuitar: R("E2", "E6", "E3", "E6"), echoGuitar: R("E2", "E6", "E3", "E5"),
  piano: R("A0", "C8", "C2", "C7"), keys: R("C2", "C6", "C3", "C6"), harpsichord: R("F1", "F6", "C2", "C6"),
  strings: R("E1", "E7", "C2", "E6"), pad: R("C2", "C6", "C2", "C5"), choir: R("E2", "A5", "C3", "G5"),
  brass: R("E2", "Bb5", "G2", "Bb4"), lead: R("C4", "C7", "C4", "C6"), bell: R("C4", "C7"),
  xylophone: R("F3", "C8", "C4", "C7"), glockenspiel: R("C5", "C8", "G5", "C8"), accordion: R("F2", "A6", "F3", "C6"),
  fmBell: R("C3", "C8", "C4", "C7"), fmEpiano: R("C2", "C7", "C3", "C6"), drawbarOrgan: R("C2", "C7", "C2", "C6"), unisonSaw: R("C1", "C7", "C2", "C6"), rotoTom: R("F1", "C4", "F2", "B3"), cannonTom: R("F1", "C4", "F2", "B3"), inchTom: R("F1", "C4", "F2", "B3"), cajon: R("A2", "G3", "A2", "G3"), kickTrigger: R("C1", "B3"), impactHit: R("E1", "C4"),
  sitar: R("C3", "C6", "C3", "C5"), koto: R("D3", "A5"), shamisen: R("C3", "C6", "C3", "C5"), banjo: R("D3", "C6", "D3", "G5"),
  harp: R("B0", "G#7", "C2", "C7"), kalimba: R("C4", "E6"), panflute: R("C4", "C7", "C4", "C6"),
  shakuhachi: R("D4", "E7", "D4", "D6"), ocarina: R("C4", "C7"), fiddle: R("G3", "E7", "G3", "B5"), bagpipe: R("A3", "A5", "G4", "A5"),
};

const midi = (n: string): number => noteNameToMidi(n);
const NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const nameOf = (m: number): string => `${NAMES[m % 12]}${Math.floor(m / 12) - 1}`;

type PartLike = Pick<Track, "notes" | "instrument"> & { role?: string };
const labelOf = (t: PartLike): string => t.role ?? t.instrument ?? "パート";
interface Placed { n: NoteEvent; start: number; end: number; midi: number }
function place(notes: NoteEvent[], pitched: boolean): Placed[] {
  const out: Placed[] = [];
  let at = 0;
  for (const n of notes) {
    if (n.note !== REST) out.push({ n, start: at, end: at + n.durationBeats, midi: pitched ? midi(n.note) : 0 });
    at += n.durationBeats;
  }
  return out;
}
const barOf = (beat: number, bpb: number): number => Math.floor(beat / bpb + 1e-9) + 1;
const joinBars = (bars: number[], max = 6): string => {
  const u = [...new Set(bars)];
  return u.slice(0, max).join("・") + (u.length > max ? `…ほか${u.length - max}か所` : "") + "小節目";
};

/** 音域の点検。hard の外は「出ません」、safe の外は「無理があります」。 */
export function checkInstrumentRange(tracks: PartLike[], beatsPerBar: number): string[] {
  const out: string[] = [];
  for (const t of tracks) {
    const r = t.instrument ? INSTRUMENT_RANGES[t.instrument] : undefined;
    if (!r) continue;
    const hardLo = midi(r.hard[0]), hardHi = midi(r.hard[1]), safeLo = midi(r.safe[0]), safeHi = midi(r.safe[1]);
    const hard: Placed[] = [], soft: Placed[] = [];
    for (const p of place(t.notes, true)) {
      if (p.midi < hardLo || p.midi > hardHi) hard.push(p);
      else if (p.midi < safeLo || p.midi > safeHi) soft.push(p);
    }
    const describe = (list: Placed[]): string => {
      const names = [...new Set(list.map((p) => p.n.note))].slice(0, 4).join("・");
      return `${names}（${joinBars(list.map((p) => barOf(p.start, beatsPerBar)))}）`;
    };
    if (hard.length) out.push(`${labelOf(t)}: ${t.instrument} の音域（${r.hard[0]}〜${r.hard[1]}）の外の音があります: ${describe(hard)}。出ない音なので、オクターブを移すか別の楽器に`);
    if (soft.length) out.push(`注意 ${labelOf(t)}: ${t.instrument} の自然な音域（${r.safe[0]}〜${r.safe[1]}）の外の音があります: ${describe(soft)}`);
  }
  return out;
}

/** 楽器グループごとの、同時に鳴らせる音の数の上限（異なる音の数）。 */
export const POLYPHONY_LIMITS: { name: string; members: string[]; max: number }[] = [
  { name: "ギター", members: ["guitar", "crunch", "distGuitar", "leadGuitar", "echoGuitar"], max: 6 },
  { name: "ハープ", members: ["harp"], max: 8 },
  { name: "ピアノ", members: ["piano", "keys", "harpsichord"], max: 10 },
  { name: "バンジョー", members: ["banjo"], max: 5 },
];

/** 同じ瞬間に鳴っている音の組を、変化点ごとに列挙する。 */
function* snapshots(placed: Placed[]): Generator<{ at: number; active: Placed[] }> {
  const points = [...new Set(placed.map((p) => p.start))].sort((a, b) => a - b);
  for (const at of points) yield { at, active: placed.filter((p) => p.start <= at + 1e-9 && p.end > at + 1e-9) };
}

/** 同時発音の点検（ギター 6・ハープ 8・ピアノ 10・ドラムは手足 4 つ、手は 2 つ）。 */
export function checkPolyphony(tracks: PartLike[], beatsPerBar: number): string[] {
  const out: string[] = [];
  for (const g of POLYPHONY_LIMITS) {
    const members = tracks.filter((t) => t.instrument && g.members.includes(t.instrument));
    if (!members.length) continue;
    const placed = members.flatMap((t) => place(t.notes, true));
    const bad: number[] = [];
    const clash: number[] = [];
    let worst = 0;
    for (const s of snapshots(placed)) {
      const distinct = new Set(s.active.map((p) => p.midi));
      if (distinct.size > g.max) { bad.push(barOf(s.at, beatsPerBar)); worst = Math.max(worst, distinct.size); }
      if (g.name === "ギター") {
        const ms = [...distinct].sort((a, b) => a - b);
        if (ms.some((m, i) => i > 0 && m - ms[i - 1] === 1)) clash.push(barOf(s.at, beatsPerBar));
      }
    }
    if (bad.length) out.push(`${g.name}（${members.map(labelOf).join("・")}）: 同時に ${worst} 音が鳴る所があります（上限 ${g.max}。${joinBars(bad)}）。弾けない重なりです`);
    if (clash.length) out.push(`注意 ${g.name}: 半音ちがいの 2 音が同時に鳴っています（${joinBars(clash)}）。1 本のギターでは同じ弦に当たるので、同じ音か、2 度以上はなしてください`);
  }
  // ドラム: 手は 2 本（スネア・ハイハット・タム・クラッシュ）、足 2 本（キック・ハイハットのペダル）。同時に 4 つまで
  const drums = tracks.filter((t) => t.instrument && ["kick", "snare", "hihat", "crash", "tom"].includes(t.instrument));
  if (drums.length) {
    const placed = drums.flatMap((t) => place(t.notes, false).map((p) => ({ ...p, midi: 0, inst: t.instrument! })));
    const hands = new Set<number>(), five = new Set<number>(), crashHat = new Set<number>();
    for (const s of snapshots(placed)) {
      const insts = new Set((s.active as (Placed & { inst: string })[]).filter((p) => Math.abs(p.start - s.at) < 1e-9).map((p) => p.inst));
      const handCount = ["snare", "hihat", "tom", "crash"].filter((x) => insts.has(x)).length;
      if (insts.size >= 5) five.add(barOf(s.at, beatsPerBar));
      else if (handCount > 2) hands.add(barOf(s.at, beatsPerBar));
      if (insts.has("crash") && insts.has("hihat") && handCount <= 2) crashHat.add(barOf(s.at, beatsPerBar));
    }
    if (five.size) out.push(`ドラム: 5 つの太鼓が同時に鳴る所があります（${joinBars([...five])}）。手足は 4 本です`);
    if (hands.size) out.push(`ドラム: スネア・ハイハット・タム・クラッシュのうち 3 つ以上が同時です（${joinBars([...hands])}）。手は 2 本なので、1〜2 つに`);
    if (crashHat.size) out.push(`注意 ドラム: クラッシュとハイハットが同時に鳴っています（${joinBars([...crashHat])}）。両手がふさがるので、ほかの太鼓はキックだけに`);
  }
  return out;
}

/** 息継ぎが要る楽器（連続して鳴らせる長さに限りがある）。 */
export const BREATH_INSTRUMENTS = new Set(["lead", "brass", "choir", "shakuhachi", "ocarina", "panflute"]);
/** 息継ぎなしで鳴らせる長さの目安（秒）。 */
export const BREATH_LIMIT_SEC = 10;

/** 休みなしで続く音の最長（秒）と、その始まりの拍。休符・0.1 拍より長い隙間で切れる。 */
export function longestRun(notes: NoteEvent[], bpm: number): { sec: number; startBeat: number } {
  let at = 0, runStart = -1, runEnd = 0, best = { sec: 0, startBeat: 0 };
  const close = (): void => {
    if (runStart >= 0) {
      const sec = ((runEnd - runStart) * 60) / bpm;
      if (sec > best.sec) best = { sec, startBeat: runStart };
    }
    runStart = -1;
  };
  for (const n of notes) {
    if (n.note === REST) {
      if (n.durationBeats >= 0.1) close();
    } else {
      const eff = Math.min(n.durationBeats, n.durationBeats * Math.min(1, n.gate ?? 1));
      if (runStart < 0) runStart = at;
      runEnd = at + eff;
    }
    at += n.durationBeats;
  }
  close();
  return best;
}

/** 息継ぎの点検。BREATH_INSTRUMENTS が 10 秒以上休まず鳴り続けていたら警告。 */
export function checkBreath(tracks: PartLike[], bpm: number, beatsPerBar: number, limitSec = BREATH_LIMIT_SEC): string[] {
  const out: string[] = [];
  for (const t of tracks) {
    if (!t.instrument || !BREATH_INSTRUMENTS.has(t.instrument)) continue;
    const r = longestRun(t.notes, bpm);
    if (r.sec > limitSec) out.push(`${labelOf(t)}: ${t.instrument} が ${r.sec.toFixed(1)} 秒休まず鳴っています（${barOf(r.startBeat, beatsPerBar)}小節目から。目安 ${limitSec} 秒）。息継ぎの休符を入れるか、breath:true を付けてください`);
  }
  return out;
}

/**
 * 息継ぎを自動で作る。休まず鳴る時間が maxSec（既定 6 秒）を超えたら、1 拍以上の音（なければ 0.75 拍以上）の終わりを 0.25 拍切って、休符にする。
 * 音の並びの長さは変わらない。
 */
export function applyBreath(events: NoteEvent[], bpm: number, maxSec = 6): NoteEvent[] {
  const out: NoteEvent[] = [];
  let runBeats = 0;
  const limitBeats = (maxSec * bpm) / 60;
  for (const e of events) {
    if (e.note === REST) {
      out.push(e);
      if (e.durationBeats >= 0.1) runBeats = 0;
      continue;
    }
    runBeats += e.durationBeats;
    const need = runBeats >= limitBeats;
    if (need && e.durationBeats >= (runBeats >= limitBeats * 1.5 ? 0.75 : 1)) {
      out.push({ ...e, durationBeats: Math.round((e.durationBeats - 0.25) * 1e6) / 1e6 }, { note: REST, durationBeats: 0.25 });
      runBeats = 0;
    } else out.push(e);
  }
  return out;
}

/** 和楽器の基準の音階（0〜11）。koto は平調子（D Eb G A Bb）、shakuhachi は五音（D F G A C）。 */
export const WORLD_INSTRUMENT_PCS: Record<string, number[]> = { koto: [2, 3, 7, 9, 10], shakuhachi: [2, 5, 7, 9, 0] };

/** 和楽器・民族楽器の音階の点検。基準の音階から外れる音の割合が maxOff（既定 20%）以上なら注意。ベンド・しゃくり付きの音（押し手・メリ）は許す。 */
export function checkWorldInstrumentScale(tracks: PartLike[], maxOff = 0.2): string[] {
  const out: string[] = [];
  for (const t of tracks) {
    const base = t.instrument ? WORLD_INSTRUMENT_PCS[t.instrument] : undefined;
    if (!base) continue;
    let total = 0, off = 0;
    for (const p of place(t.notes, true)) {
      total += p.n.durationBeats;
      if (!base.includes(p.midi % 12) && !(p.n.bend || p.n.scoop || p.n.fall)) off += p.n.durationBeats;
    }
    if (total > 0 && off / total >= maxOff) out.push(`注意 ${labelOf(t)}: ${t.instrument} の基準の音階（${base.map((m) => nameOf(60 + m).replace(/\d/, "")).join(" ")}）から外れた音が ${Math.round((off / total) * 100)}% あります。押し手（^）やメリ（/）で作る音でなければ、音階に合わせてください`);
  }
  return out;
}

/** 手書きのパートをまとめて点検する。 */
export function checkInstrumentUsage(tracks: PartLike[], bpm: number, beatsPerBar: number): string[] {
  return [...checkInstrumentRange(tracks, beatsPerBar), ...checkPolyphony(tracks, beatsPerBar), ...checkBreath(tracks, bpm, beatsPerBar), ...checkWorldInstrumentScale(tracks)];
}
