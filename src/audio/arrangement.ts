import { REST, type Instrument, type NoteEvent, type Track } from "./score";

/**
 * 自動の伴奏に「曲の起伏」をつける（セクション編曲）。
 * 曲をセクション（導入・Aメロ・Bメロ・サビ・間奏・Cメロ・終わり）に区切り、セクションごとに鳴らす楽器と強さを変える。
 * 自動の伴奏は最初から最後まで同じなので、そのままだと平らに聞こえる。これで「静か → 盛り上がる → サビで全部」の流れができる。
 */
export type SectionKind = "intro" | "verse" | "pre" | "chorus" | "interlude" | "bridge" | "outro";
export interface Section { kind: SectionKind; bars: number }

export const SECTION_KINDS: SectionKind[] = ["intro", "verse", "pre", "chorus", "interlude", "bridge", "outro"];
export const SECTION_LABELS: Record<SectionKind, string> = {
  intro: "導入", verse: "Aメロ", pre: "Bメロ", chorus: "サビ", interlude: "間奏", bridge: "Cメロ", outro: "終わり",
};

type Group = "kick" | "hat" | "snare" | "bass" | "keys" | "guitar" | "strings";
const GROUP_OF: Partial<Record<Instrument, Group>> = {
  kick: "kick", hihat: "hat", snare: "snare", tom: "snare", bass: "bass", sub808: "bass",
  piano: "keys", keys: "keys", harpsichord: "keys", bell: "keys", harp: "keys",
  guitar: "guitar", echoGuitar: "guitar", crunch: "guitar", distGuitar: "guitar",
  strings: "strings", pad: "strings", choir: "strings", brass: "strings",
};

interface Layer { groups: Group[]; from: number; to: number }
/** セクションごとの、鳴らす楽器の組と、強さ（始め → 終わり。1が元の強さ）。 */
const LAYERS: Record<SectionKind, Layer> = {
  intro: { groups: ["keys", "strings"], from: 0.75, to: 0.95 },
  verse: { groups: ["kick", "hat", "bass", "keys", "strings"], from: 0.85, to: 0.9 },
  pre: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 0.85, to: 1.0 },
  chorus: { groups: ["kick", "hat", "snare", "bass", "keys", "guitar", "strings"], from: 1.0, to: 1.0 },
  interlude: { groups: ["bass", "keys", "guitar", "strings"], from: 0.9, to: 0.9 },
  bridge: { groups: ["bass", "keys", "strings"], from: 0.8, to: 0.9 },
  outro: { groups: ["bass", "keys", "strings"], from: 0.9, to: 0.5 },
};

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
    out.push({ kind: s.kind, bars });
    left -= bars;
  }
  if (left > 0 && out.length) out[out.length - 1].bars += left;
  return { sections: out, warning: `sections の小節数（${sum}）が曲の長さ（${totalBars}小節）とちがうので、${sum < totalBars ? "最後のセクションを延ばしました" : "後ろを切りました"}` };
}

const restOf = (beats: number): NoteEvent => ({ note: REST, durationBeats: beats });

/** 自動の伴奏のトラックに、セクションごとの楽器の出し入れと強弱をかける。メロディなど自分で書いたパートには使わない。 */
export function applySections(tracks: Track[], sections: Section[], beatsPerBar: number): Track[] {
  const starts: number[] = [];
  let at = 0;
  for (const s of sections) { starts.push(at); at += s.bars; }
  const totalBars = at;
  const sectionAt = (bar: number): number => {
    for (let i = sections.length - 1; i >= 0; i--) if (bar >= starts[i]) return i;
    return 0;
  };
    let crashVolume = 0.08;
  const out: Track[] = [];
  for (const t of tracks) {
    if (t.instrument === "crash") { crashVolume = t.volume || crashVolume; continue; }
    const group = t.instrument ? GROUP_OF[t.instrument] : undefined;
    if (!group) { out.push(t); continue; }
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
      const layer = LAYERS[sec.kind];
      const lastBar = bar === starts[si] + sec.bars - 1;
      const nextKind = sections[si + 1]?.kind;
      // サビの前の最後の小節は、スネアとキックを足して、サビへの助走にする
      const leadIn = lastBar && nextKind === "chorus" && (group === "snare" || group === "kick");
      const on = layer.groups.includes(group) || leadIn;
      if (!on || n.note === REST) push(n.note === REST ? n : restOf(n.durationBeats));
      else {
        const progress = sec.bars > 1 ? (bar - starts[si]) / (sec.bars - 1) : 1;
        let gain = layer.from + (layer.to - layer.from) * progress;
        if (leadIn) gain = Math.max(gain, 1) * (0.9 + 0.1 * ((pos % beatsPerBar) / beatsPerBar));
        push({ ...n, ...(n.velocity !== undefined ? { velocity: n.velocity * gain } : gain < 1 ? { velocity: gain } : {}) });
      }
      pos += n.durationBeats;
    }
    out.push({ ...t, notes });
  }
  // クラッシュ: サビの頭だけ（元の伴奏のクラッシュは外す）
  const crashNotes: NoteEvent[] = [];
  sections.forEach((s, i) => {
    const startBeat = starts[i] * beatsPerBar;
    const doneBeat = crashNotes.reduce((a, n) => a + n.durationBeats, 0);
    if (s.kind !== "chorus") return;
    if (startBeat > doneBeat) crashNotes.push(restOf(startBeat - doneBeat));
    crashNotes.push({ note: "C#3", durationBeats: Math.min(beatsPerBar, 4), velocity: 110 });
  });
  const used = crashNotes.reduce((a, n) => a + n.durationBeats, 0);
  const totalBeats = totalBars * beatsPerBar;
  if (crashNotes.length && used < totalBeats) crashNotes.push(restOf(totalBeats - used));
  if (crashNotes.length) out.push({ waveform: "square", instrument: "crash", volume: crashVolume, pan: -0.3, notes: crashNotes });
  return out;
}
