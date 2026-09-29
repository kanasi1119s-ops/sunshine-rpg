import { noteNameToMidi } from "./note";
import { REST, type Instrument, type Score } from "./score";
import { barBeats, timeSignatureOf } from "./time-signature";

/**
 * 楽譜のソフト（MuseScore など）で開ける MusicXML に書き出す。トラックごとに1パート。
 * 小節線をまたぐ音は、タイでつなぐ。半端な長さは、ふつうの音符（付点を含む）に分けてタイでつなぐ。
 */
const DIV = 48; // 4分音符 = 48
const TYPES: [number, string, boolean][] = [
  [192, "whole", false], [144, "half", true], [96, "half", false], [72, "quarter", true], [48, "quarter", false],
  [36, "eighth", true], [24, "eighth", false], [18, "16th", true], [12, "16th", false], [9, "32nd", true], [6, "32nd", false], [3, "64th", false],
];
const NAMES: Partial<Record<Instrument, string>> = {
  kick: "Bass Drum", snare: "Snare", hihat: "Hi-Hat", crash: "Crash", tom: "Tom", bass: "Bass", slap: "Slap Bass", sub808: "808 Bass",
  guitar: "Clean Guitar", crunch: "Crunch Guitar", distGuitar: "Distortion Guitar", leadGuitar: "Lead Guitar", echoGuitar: "Echo Guitar",
  keys: "E.Piano", piano: "Piano", harpsichord: "Harpsichord", strings: "Strings", pad: "Pad", choir: "Choir", brass: "Brass", bell: "Bells", lead: "Lead",
};
const DRUMS = new Set(["kick", "snare", "hihat", "crash", "tom"]);
const esc = (s: string): string => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** 長さ（分割の数）を、ふつうの音符の並びに分ける。 */
function pieces(len: number): [number, string, boolean][] {
  const out: [number, string, boolean][] = [];
  let left = len;
  while (left > 0) {
    const t = TYPES.find(([d]) => d <= left);
    if (!t) {
      out.push([left, "64th", false]);
      break;
    }
    out.push(t);
    left -= t[0];
  }
  return out;
}

export function scoreToMusicXml(score: Score, title = "Untitled"): string {
  const sig = timeSignatureOf(score);
  const barLen = Math.round(barBeats(sig) * DIV);
  const total = Math.max(...score.tracks.map((t) => t.notes.reduce((s, n) => s + n.durationBeats, 0)));
  const bars = Math.max(1, Math.ceil((total * DIV) / barLen - 1e-6));
  const parts = score.tracks.map((t, i) => ({ id: `P${i + 1}`, name: NAMES[t.instrument as Instrument] ?? `Track ${i + 1}`, track: t, drum: DRUMS.has(t.instrument ?? "") }));
  const lines: string[] = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">',
    '<score-partwise version="4.0">',
    `<work><work-title>${esc(title)}</work-title></work>`,
    "<identification><encoding><software>Sunshine Composer</software></encoding></identification>",
    "<part-list>",
    ...parts.map((p) => `<score-part id="${p.id}"><part-name>${esc(p.name)}</part-name></score-part>`),
    "</part-list>",
  ];
  for (const p of parts) {
    // 音を、位置（分割の数）つきの一覧にする
    const events: { start: number; len: number; midi: number | null }[] = [];
    let at = 0;
    for (const n of p.track.notes) {
      const len = Math.round(n.durationBeats * DIV);
      if (len > 0) events.push({ start: at, len, midi: n.note === REST ? null : p.drum ? 60 : noteNameToMidi(n.note) });
      at += len;
    }
    if (at < bars * barLen) events.push({ start: at, len: bars * barLen - at, midi: null });
    const lows = events.filter((e) => e.midi !== null).map((e) => e.midi!);
    const clef = !p.drum && lows.length && lows.reduce((s, m) => s + m, 0) / lows.length < 57 ? '<clef><sign>F</sign><line>4</line></clef>' : p.drum ? '<clef><sign>percussion</sign></clef>' : '<clef><sign>G</sign><line>2</line></clef>';
    lines.push(`<part id="${p.id}">`);
    for (let b = 0; b < bars; b++) {
      const from = b * barLen;
      const to = from + barLen;
      lines.push(`<measure number="${b + 1}">`);
      if (b === 0) {
        lines.push(`<attributes><divisions>${DIV}</divisions><key><fifths>0</fifths></key><time><beats>${sig.num}</beats><beat-type>${sig.den}</beat-type></time>${clef}</attributes>`);
        if (p.id === "P1") lines.push(`<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit><per-minute>${score.tempoBpm}</per-minute></metronome></direction-type><sound tempo="${score.tempoBpm}"/></direction>`);
      }
      for (const e of events) {
        const s = Math.max(e.start, from);
        const en = Math.min(e.start + e.len, to);
        if (en <= s) continue;
        const parts2 = pieces(en - s);
        parts2.forEach(([len, type, dot], k) => {
          const tieStart = e.midi !== null && (k < parts2.length - 1 || e.start + e.len > to);
          const tieStop = e.midi !== null && (k > 0 || e.start < from);
          let pitch = "<rest/>";
          if (e.midi !== null) {
            const steps = ["C", "C", "D", "D", "E", "F", "F", "G", "G", "A", "A", "B"];
            const alter = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0][e.midi % 12];
            pitch = p.drum ? "<unpitched><display-step>C</display-step><display-octave>5</display-octave></unpitched>" : `<pitch><step>${steps[e.midi % 12]}</step>${alter ? "<alter>1</alter>" : ""}<octave>${Math.floor(e.midi / 12) - 1}</octave></pitch>`;
          }
          const ties = `${tieStop ? '<tie type="stop"/>' : ""}${tieStart ? '<tie type="start"/>' : ""}`;
          const notations = tieStart || tieStop ? `<notations>${tieStop ? '<tied type="stop"/>' : ""}${tieStart ? '<tied type="start"/>' : ""}</notations>` : "";
          lines.push(`<note>${pitch}<duration>${len}</duration>${ties}<type>${type}</type>${dot ? "<dot/>" : ""}${notations}</note>`);
        });
      }
      lines.push("</measure>");
    }
    lines.push("</part>");
  }
  lines.push("</score-partwise>");
  return lines.join("\n");
}

/** 音の一覧（表計算ソフトで開ける CSV）。 */
export function scoreToCsv(score: Score): string {
  const rows = ["track,instrument,start_beat,duration_beats,note,midi,velocity"];
  score.tracks.forEach((t, i) => {
    let at = 0;
    for (const n of t.notes) {
      if (n.note !== REST) rows.push([i + 1, t.instrument ?? t.waveform, round(at), round(n.durationBeats), n.note, noteNameToMidi(n.note), n.velocity ?? 1].join(","));
      at += n.durationBeats;
    }
  });
  return rows.join("\n") + "\n";
}
const round = (x: number): number => Math.round(x * 1e6) / 1e6;
